#!/usr/bin/env python3
"""
This is a small python webserver intended to run on a testing network resource
where the lf_kinstall.pl script can post build machine information to. A useful
place to install this script would be on an APU2 being used as a VPN gateway.

Use these commands to install LaTeX and html2ps
    apt install perlmagick libwww-perl libhtml-parser-perl libpaper-utils ghostscript weblint-perl texlive-base postscript-viewer xhtml2ps html2ps

Consider these commands to install printer drivers:

Dymo LabelWriter-450:
    apt install printer-driver-dymo
Brother QL-800:
    # apt install brother-cups-wrapper-common brother-cups-wrapper-extra brother-lpr-drivers-common brother-lpr-drivers-extra
    Download drivers here:
    https://support.brother.com/g/b/downloadtop.aspx?c=us&lang=en&prod=lpql800eus
    * download driver
    * install driver using
        $ sudo dpkg -i dymo*.dpkg

Use these commands to install the script:

    $ sudo cp label-printer.py /usr/local/bin
    $ sudo chmod a+x /usr/local/bin/label-printer.py

    $ sudo cp label-printer.service /lib/systemd/system
    $ sudo systemctl add-wants multi-user.target label-printer.service
    $ sudo systemctl daemon-reload
    $ sudo systemctl restart label-printer.service

At this point, if you use `ss -ntlp` you should see this script listening on port 8082.

If you are running ufw on your label-printer host, please use this command to allow
traffice to port 8082:
$ sudo ufw allow 8082/tcp
$ sudo ufw reload

Using kinstall to print labels:
Dymo LabelWriter:
    $ ./lf_kinstall.pl --print-label http://192.168.9.1:8082/ --printer LabelWriter-450

Brother QL-800:
    $ ./lf_kinstall.pl --print-label http://192.168.9.1:8082/ --printer QL800


"""
import os
import logging
import math
from datetime import datetime
from http import server
from http.server import HTTPServer, BaseHTTPRequestHandler
from ssl import wrap_socket
from urllib.parse import urlparse, parse_qs
import pprint
from pprint import pprint

class LabelPrinterRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200);
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self.send_response(200);
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def popstr(self, param):
        #print ("""TYPE : "%s" """%type(param))
        #print ("""TYPE0: "%s" """%type(param[0]))
        if type(param) is list:
            #print("""LIST: "%s", """%param[0])
            return str(param[0])
        return str(param)

    def do_POST(self):
        html_filename = "/tmp/label.html"
        printer = ""
        hostname = "";
        mac_address = "";
        model = "";
        serial = "";
        
        length = int(self.headers['Content-Length'])
        field_data = self.rfile.read(length).decode("utf-8")
        print("Field_data: %s\n"%field_data);
        fields = parse_qs(field_data)
        #pprint(fields)
        
        #for name in fields:
        #    print("""key %s: "%s" %s""" % (name, self.popstr(fields[name]), type(fields[name])))
        if "printer" in fields:
            printer = self.popstr(fields["printer"])
            if (printer is None) or ("" == printer):
                err_msg = "printer empty or unset"
                self.send_resonse(400)
                self.send_header("X-Error", err_msg)
                self.end_headers()
                self.wfile.write(b"<html><body><li> %s\n"%err_msg)
                return
        else:
            err_msg = "printer not submitted"
            self.send_response(400)
            self.send_header("X-Error", err_msg)
            self.end_headers();
            self.wfile.write(b"<html><body><li>%s\n" % err_msg);
            return

        if "mac" in fields:
            mac_address = self.popstr(fields["mac"])
            if (mac_address is None) or ("" == mac_address):
                err_msg = "mac address empty or unset"
                self.send_resonse(400)
                self.send_header("X-Error", err_msg)
                self.end_headers()
                self.wfile.write(b"<html><body><li> %s\n"%err_msg)
                return
        else:
            err_msg = "mac address not submitted"
            self.send_response(400)
            self.send_header("X-Error", err_msg)
            self.end_headers();
            self.wfile.write(b"<html><body><li>%s\n" % err_msg);
            return
        
        if "model" in fields:
            model = self.popstr(fields["model"])
            if (model is None) or (model == ""):
                err_msg = "model name not submitted"
                self.send_reponse(400)
                self.send_header("X-Error", err_msg)
                self.end_headers()
                self.wfile.write(b"<html><body><li> %s\n"%err_msg)
                return
        else:
            err_msg = "model name not submitted"
            self.send_response(400)
            self.send_header("X-Error", err_msg)
            self.wfile.write(b"<html><body><li>%s\n" % err_msg);
            return

        if "hostname" in fields:
            hostname = self.popstr(fields["hostname"])
        else:
            suffix = mac_address[-5:].replace(":", "")
            hostname = "%s-%s"%(model, suffix)

        if "serial" in fields:
            serial = self.popstr(fields["serial"])
        else:
            serial = hostname

        now = datetime.now()
        datestr = now.strftime("%Y-%m")

        self.send_response(200);
        self.send_header("Content-type", "text/html")
        self.end_headers()
        label_html = self.html_template(model_=model, mac_=mac_address, hostname_=hostname, serial_=serial, datestr_=datestr)

        if os.path.exists(html_filename):
            try:
                os.remove(html_filename)
            except:
                err_msg = "unable to remove html file"
                self.send_response(400)
                self.send_header("X-Error", err_msg)
                self.wfile.write(b"<html><body><li>%s\n" % err_msg);
                return

        try:
            file = open(html_filename, "w")
            file.write(label_html)
            file.close()
        except:
            err_msg = "unable to write html file"
            self.send_response(400)
            self.send_header("X-Error", err_msg)
            self.wfile.write(b"<html><body><li>%s\n" % err_msg);
            return

        self.print_pdf(printer=printer, html=html_filename)

        self.wfile.write(b"<html><body>Success\n")

    def html_template(self, model_="unset", mac_="unset", hostname_="unset", serial_="unset", datestr_="unset"):
        template = """<html><head></head><body style='margin:0;padding:0;'>
<table border='1' cellpadding='2' cellspacing='0' height="90" style="margin:0;padding:0;float:left;clear:none;">
  <tr>
   <td width="1in" style="font-size: 5pt;">Model:</td>
   <td width="2in" style="font-family: 'Courier New',Courier; font-size: 8pt;"><b><tt>%s</tt></b> <small>(%s)</small></td>
  </tr>
  <tr>
   <td style="font-size: 5pt;">MAC:</td>
   <td style="font-family: 'Courier New',Courier; font-size: 8pt;"><b><tt>%s</tt></b></td>
  <tr>
   <td style="font-size: 5pt;">Hostname:</td>
   <td style="font-family: 'Courier New',Courier; font-size: 8pt;"><b><tt>%s</tt></b></td>
  <tr>
   <td style="font-size: 5pt;">Serial:</td>
   <td style="font-family: 'Courier New',Courier; font-size: 8pt;"><b><tt>#%s</tt></b></td>
  </tr>
</table></body></html>""" % (model_, datestr_, mac_, hostname_, serial_)
        return template

    def print_pdf(self, printer, html ):
        """

        :param printer:
        :param html:
        :return:
        """
        """ Below is shell script that worked:

w_inches="3.45"
h_inches="1.125"
w_points=`echo "scale=0; ($w_inches * 72)/1" | bc -l`
w_px=`echo "scale=0; ($w_inches * 720)/1" | bc -l`
h_points=`echo "scale=0; ($h_inches * 72)/1" | bc -l`
h_px=`echo "scale=0; ($h_inches * 720)/1" | bc -l`

echo "Page size in Points: $w_points x $h_points"
echo "Page size in pixels: $w_px x $h_px"

rm -f label.pdf

set -x
html2ps -L label.html \
| gs -o label.pdf \
   -g${h_px}x${w_px} \
   -sDEVICE=pdfwrite \
   -dFIXEDMEDIA \
   -dPDFFitPage \
   -dFitPage \
   -c '<</PageOffset [-80 -44]>> setpagedevice' \
   -f -
"""
        w_inches = 3.45
        h_inches = 1.125
        w_points = math.floor(w_inches * 72)
        w_px = math.floor(w_inches * 720)
        h_points = math.floor(h_inches * 72)
        h_px = math.floor(h_inches * 720)
        pdf_file = "/tmp/label.pdf"
        pageoffset = "<</PageOffset [-80 -44]>> setpagedevice"
        geometry = "-g{}x{}".format(h_px, w_px)
        if os.path.exists(pdf_file):
            try:
                os.remove(pdf_file)
            except:
                err_msg = "unable to remove html file"
                self.send_response(400)
                self.send_header("X-Error", err_msg)
                self.wfile.write(b"<html><body><li>%s\n" % err_msg);
                return

        cmd = """html2ps -L "%s" | gs -o "%s" %s -sDEVICE=pdfwrite -dFIXEDMEDIA -dPDFFitPage -dFitPage -c '%s' -f -""" \
              % (html, pdf_file, geometry, pageoffset)
        print("CMD: "+cmd)
        try:
            os.system(cmd)
            os.system("""lp -d "%s" -- "%s" """%(printer, pdf_file))
        except:
            err_msg = "trouble printing pdf"
            self.send_response(500)
            self.send_header("X-Error", err_msg)
            self.wfile.write(b"<html><body><li>%s\n" % err_msg);
            return




def __main__():
    logging.info("Main Method. Creating CGI Handler")   
    httpd = HTTPServer(('', 8082), LabelPrinterRequestHandler)
    print("Starting LabelPrinter service...")
    httpd.serve_forever()

if __name__ == "__main__":
    __main__()

