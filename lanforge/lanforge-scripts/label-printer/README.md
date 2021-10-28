**label-printer.py**

This is a small python webserver intended to run on a testing network resource where the `lf_kinstall.pl` script can post build machine information to. A useful place to install this script would be on an APU2 being used as a VPN gateway.

Use these commands to install **LaTeX** and **html2ps**:
    `apt install perlmagick libwww-perl libhtml-parser-perl libpaper-utils ghostscript weblint-perl texlive-base postscript-viewer xhtml2ps html2ps`

Consider these commands to install printer drivers:

**Dymo LabelWriter-450:**
    `apt install printer-driver-dymo`

**Brother QL-800:**
    `$ sudo apt install brother-cups-wrapper-common brother-cups-wrapper-extra brother-lpr-drivers-common brother-lpr-drivers-extra`

Download drivers here:
​  https://support.brother.com/g/b/downloadtop.aspx?c=us&lang=en&prod=lpql800eus

Install driver using:
    `$ sudo dpkg -i dymo*.dpkg`

Use these commands to install the script:

    $ sudo cp label-printer.py /usr/local/bin
    $ sudo chmod a+x /usr/local/bin/label-printer.py
    
    $ sudo cp label-printer.service /lib/systemd/system
    $ sudo systemctl add-wants multi-user.target label-printer.service
    $ sudo systemctl daemon-reload
    $ sudo systemctl restart label-printer.service

At this point, if you use `ss -ntlp` you should see this script listening on port 8082.

If you are running `ufw` on your label-printer host, please use this command to allow
traffic to port 8082:

`$ sudo ufw allow 8082/tcp`
`$ sudo ufw reload`

**Using kinstall to print labels:**

Dymo LabelWriter:
    `$ ./lf_kinstall.pl --print-label http://192.168.9.1:8082/ --printer LabelWriter-450`

Brother QL-800:
    `$ ./lf_kinstall.pl --print-label http://192.168.9.1:8082/ --printer QL-800`

Note that the QL-800 printer driver installs an *example* printer queue named **QL800** which is misleading. Please ignore that. When the printer is plugged in, a **QL-800** printer queue will be created, which is the true queue to print to.
