#!/usr/bin/python3
'''

Create connections with different QoS, run them, and report the latency
and other throughput values.

make sure pexpect is installed:
$ sudo yum install python3-pexpect
$ sudo yum install python3-xlsxwriter

You might need to install pexpect-serial using pip:
$ pip3 install pexpect-serial
$ pip3 install XlsxWriter

The user is responsible for setting up the stations oustide of this script, however.

When specifying ports, if the port starts with [Number]., like 1.eth1, then the 1 specifies
the resource ID.

./lf_tos_test.py --lfmgr 192.168.100.178 \
  --station "1.wlan0 1.wlan1" --tos "BK BE VI VO" --proto udp \
  --speed_mbps 1000 --upstream_port 1.eth2 --duration_min 5

'''

# TODO:  Maybe HTML output too?
# TODO:  Allow selecting tabs or commas for output files

import sys
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

import re
import logging
import time
from time import sleep
import pprint
import argparse
import subprocess
import xlsxwriter
from subprocess import PIPE

NL = "\n"
CR = "\r\n"
Q = '"'
A = "'"
FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'

lfmgr = "127.0.0.1"
lfstation = "1.wlan0"
outfile = "tos_results.xlsx"
upstream_port = "1.eth1"
speed = 1000000000
proto = "udp"
dur = 5 * 60
tos = "BK";

# rssi_adjust = (current_nf - nf_at_calibration)

def usage():
   print("$0 ")
   print("--outfile: Write results here.")
   print("--station: LANforge station names (1.wlan0 1.wlan1 ...)")
   print("--upstream_port: LANforge upstream port name (1.eth1)")
   print("--lfmgr: LANforge manager IP address")
   print("--tos: IP Type of Service: BK BE VI VO")
   print("--speed_mbps: Total requested transmit speed, in Mbps")
   print("--duration: Duration to run traffic, in minutes")
   print("--proto: List of protocols (udp, tcp)")
   print("-h|--help")

def main():
   global lfmgr
   global lfstation
   global outfile
   global upstream_port
   global speed
   global proto;
   global dur;
   global tos;

   parser = argparse.ArgumentParser(description="ToS report Script")
   parser.add_argument("--upstream_port",  type=str, help="LANforge upsteram-port to use (1.eth1, etc)")
   parser.add_argument("--station",        type=str, help="LANforge stations to use (1.wlan0 1.wlan1 etc)")
   parser.add_argument("--lfmgr",        type=str, help="LANforge Manager IP address")
   parser.add_argument("--outfile",     type=str, help="Output file for csv data")
   parser.add_argument("--tos",     type=str, help="IP Type of Service: BK BE VI VO")
   parser.add_argument("--speed_mbps",     type=int, help="Total requested transmit speed, in Mbps")
   parser.add_argument("--duration",     type=float, help="Duration to run traffic, in minutes")
   parser.add_argument("--proto",     type=str, help="List of protocols (udp tcp)")
   
   args = None
   try:
      args = parser.parse_args()
      if (args.station != None):
          lfstation = args.station
      if (args.upstream_port != None):
          upstream_port = args.upstream_port
      if (args.lfmgr != None):
          lfmgr = args.lfmgr
      if (args.tos != None):
          tos = args.tos
      if (args.proto != None):
          proto = args.proto
      if (args.speed_mbps != None):
          speed = args.speed_mbps * 1000000
      if (args.duration != None):
          dur = args.duration * 60
      if (args.outfile != None):
          outfile = args.outfile
      filehandler = None
   except Exception as e:
      logging.exception(e);
      usage()
      exit(2);

   # XLSX file
   workbook = xlsxwriter.Workbook(outfile)
   worksheet = workbook.add_worksheet()

   bold = workbook.add_format({'bold': True, 'align': 'center'})
   dblue_bold = workbook.add_format({'bold': True, 'align': 'center'})
   dblue_bold.set_bg_color("#b8cbe4")
   dblue_bold.set_border(1)
   dtan_bold = workbook.add_format({'bold': True, 'align': 'center'})
   dtan_bold.set_bg_color("#dcd8c3")
   dtan_bold.set_border(1)
   dpeach_bold = workbook.add_format({'bold': True, 'align': 'center'})
   dpeach_bold.set_bg_color("#ffd8bb")
   dpeach_bold.set_border(1)
   dpink_bold = workbook.add_format({'bold': True, 'align': 'center'})
   dpink_bold.set_bg_color("#fcc8ca")
   dpink_bold.set_border(1)
   dyel_bold = workbook.add_format({'bold': True, 'align': 'center'})
   dyel_bold.set_bg_color("#ffe699")
   dyel_bold.set_border(1)
   dgreen_bold = workbook.add_format({'bold': True, 'align': 'center'})
   dgreen_bold.set_bg_color("#c6e0b4")
   dgreen_bold.set_border(1)
   dgreen_bold_left = workbook.add_format({'bold': True, 'align': 'left'})
   dgreen_bold_left.set_bg_color("#c6e0b4")
   dgreen_bold_left.set_border(1)
   center = workbook.add_format({'align': 'center'})
   center_blue = workbook.add_format({'align': 'center'})
   center_blue.set_bg_color("#dbe5f1")
   center_blue.set_border(1)
   center_tan = workbook.add_format({'align': 'center'})
   center_tan.set_bg_color("#edede1")
   center_tan.set_border(1)
   center_peach = workbook.add_format({'align': 'center'})
   center_peach.set_bg_color("#fce4d6")
   center_peach.set_border(1)
   center_yel = workbook.add_format({'align': 'center'})
   center_yel.set_bg_color("#fdf2cc")
   center_yel.set_border(1)
   center_yel_red = workbook.add_format({'align': 'center', 'color': 'red'})
   center_yel_red.set_bg_color("#fdf2cc")
   center_yel_red.set_border(1)
   center_pink = workbook.add_format({'align': 'center'})
   center_pink.set_bg_color("ffd2d3")
   center_pink.set_border(1)
   red = workbook.add_format({'color': 'red', 'align': 'center'})
   red.set_bg_color("#e0efda")
   red.set_border(1)
   red_left = workbook.add_format({'color': 'red', 'align': 'left'})
   red_left.set_bg_color("#e0efda")
   red_left.set_border(1)
   green = workbook.add_format({'color': 'green', 'align': 'center'})
   green.set_bg_color("#e0efda")
   green.set_border(1)
   green_left = workbook.add_format({'color': 'green', 'align': 'left'})
   green_left.set_bg_color("#e0efda")
   green_left.set_border(1)

   worksheet.set_row(0, 45) # Set height

   bucket_hdrs = "0 1 2-3 4-7 8-15 16-31 32-63 64-127 128-255 256-511 512-1023 1024-2047 2048-4095 4096-8191 8192-16383 16384-32767 32768-65535".split()
   col = 0
   row = 0

   dwidth = 13 # Set width to 13 for all columns by default

   worksheet.set_column(col, col, dwidth)
   worksheet.write(row, col, 'CX-Name', dblue_bold); col += 1
   worksheet.set_column(col, col, 15)
   worksheet.write(row, col, 'Endp-Name', dblue_bold); col += 1
   worksheet.set_column(col, col, 12)
   worksheet.write(row, col, 'Port', dblue_bold); col += 1
   worksheet.set_column(col, col, dwidth)
   worksheet.write(row, col, 'Protocol', dblue_bold); col += 1
   worksheet.set_column(col, col, dwidth)
   worksheet.write(row, col, 'ToS', dblue_bold); col += 1
   worksheet.set_column(col, col, 20)
   worksheet.write(row, col, 'AP BSSID', dblue_bold); col += 1
   worksheet.set_column(col, col, dwidth)
   worksheet.write(row, col, 'Band\nwidth', dblue_bold); col += 1
   worksheet.set_column(col, col, dwidth)
   worksheet.write(row, col, 'Mode', dblue_bold); col += 1
   worksheet.set_column(col, col, dwidth)
   worksheet.write(row, col, 'Last MCS\nRx', dblue_bold); col += 1
   worksheet.set_column(col, col, dwidth)
   worksheet.write(row, col, 'Combined\nRSSI', dblue_bold); col += 1
   worksheet.set_column(col, col, dwidth)
   worksheet.write(row, col, 'Endpoint\nOffered\nLoad', dtan_bold); col += 1
   worksheet.set_column(col, col, dwidth)
   worksheet.write(row, col, 'Endpoint\nRx\nThroughput', dtan_bold); col += 1
   worksheet.set_column(col, col, dwidth)
   worksheet.write(row, col, 'Cx\nOffered\nLoad', dtan_bold); col += 1
   worksheet.set_column(col, col, dwidth)
   worksheet.write(row, col, 'Cx\nRx\nThroughput', dtan_bold); col += 1
   worksheet.set_column(col, col, dwidth)
   worksheet.write(row, col, 'Avg\nLatency', dyel_bold); col += 1
   worksheet.set_column(col, col, dwidth)
   worksheet.write(row, col, 'Min\nLatency', dyel_bold); col += 1
   worksheet.set_column(col, col, dwidth)
   worksheet.write(row, col, 'Max\nLatency', dyel_bold); col += 1
   for i in range(17):
       btitle = "Latency\nRange\n%s"%(bucket_hdrs[i])
       worksheet.set_column(col, col, dwidth)
       worksheet.write(row, col, btitle, dpeach_bold); col += 1

   worksheet.set_column(col, col, 50)
   worksheet.write(row, col, 'Warnings and Errors', dgreen_bold_left); col += 1
   row += 1

   # Use subprocess.check_output("Cmd") to utilize existing LF scripts.

   lfstations = lfstation.split()
   toss = tos.split()
   protos = proto.split()

   u_name = upstream_port
   u_resource = 1
   if (upstream_port[0].isdigit()):
       tmpa = upstream_port.split(".", 1)
       u_resource = tmpa[0]
       u_name = tmpa[1]

   mcount = len(lfstations) * len(toss) * len(protos);
   cx_speed = int(speed / mcount);
   opposite_speed = 56000
   count = 0
   cxnames = []
   for sta in lfstations:
       e_tot = ""
       sta_resource = "1"
       sta_name = sta;
       if sta[0].isdigit():
           tmpa = sta.split(".", 1);
           sta_resource = tmpa[0];
           sta_name = tmpa[1];

       # Up station
       subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  sta_resource, "--port_name", sta_name,
                       "--set_ifstate", "up"]); 

       i = 0
       wait_ip_print = False;
       wait_assoc_print = False;
       # Wait untill LANforge station connects
       while True:
           port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  sta_resource, "--port_name", sta_name,
                                        "--show_port", "AP,IP,Mode,NSS,Bandwidth,Channel,Signal,Noise,Status,RX-Rate"], stdout=PIPE, stderr=PIPE);
           pss = port_stats.stdout.decode('utf-8', 'ignore');

           _status = None
           _ip = None

           for line in pss.splitlines():
               m = re.search('Status:\s+(.*)', line)
               if (m != None):
                   _status = m.group(1)
               m = re.search('IP:\s+(.*)', line)
               if (m != None):
                   _ip = m.group(1)

           #print("IP %s  Status %s"%(_ip, _status))

           if (_status == "Authorized"):
               if ((_ip != None) and (_ip != "0.0.0.0")):
                   print("Station is associated with IP address.")
                   break
               else:
                   if (not wait_ip_print):
                       print("Waiting for station %s.%s to get IP Address."%(sta_resource, sta_name))
                       wait_ip_print = True
           else:
               if (not wait_assoc_print):
                   print("Waiting up to 180s for station %s.%s to associate."%(sta_resource, sta_name))
               wait_assoc_print = True

           i = i + 1
           # We wait a fairly long time since AP will take a long time to start on a CAC channel.
           if (i > 180):
               err = "ERROR:  Station did not connect within 180 seconds."
               print(err)
               e_tot += err
               e_tot += "  "
               if (args.wait_forever):
                   print("Will continue waiting, you may wish to debug the system...")
                   i = 0
               else:
                   break

           time.sleep(1)

       for p in protos:
           for t in toss:
               e_tot2 = e_tot
               # Create connections.
               # First, delete any old ones
               cxn = "scr-tos-%i"%count
               ena = "scr-tos-%i-A"%count
               enb = "scr-tos-%i-B"%count

               cxnames.append(cxn)

               subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--action", "do_cmd",
                               "--cmd", "rm_cx ALL %s"%cxn], stderr=PIPE, stdout=PIPE);
               subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--action", "do_cmd",
                               "--cmd", "rm_endp %s"%ena], stderr=PIPE, stdout=PIPE);
               subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--action", "do_cmd",
                               "--cmd", "rm_endp %s"%enb], stderr=PIPE, stdout=PIPE);

               cx_proto = p;
               if (cx_proto == "udp"):
                   cx_proto = "lf_udp"
               if (cx_proto == "tcp"):
                   cx_proto = "lf_tcp"

               # Now, create the new connection
               subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  "%s"%sta_resource, "--action", "create_endp", "--port_name", sta_name,
                               "--endp_type", cx_proto, "--endp_name", ena, "--speed", "%s"%opposite_speed, "--report_timer", "1000", "--tos", t,
                               "--multicon", "1"])#, capture_output=True);
               subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  "%s"%u_resource, "--action", "create_endp", "--port_name", u_name,
                               "--endp_type", cx_proto, "--endp_name", enb, "--speed", "%s"%cx_speed, "--report_timer", "1000", "--tos", t,
                               "--multicon", "1"])#  capture_output=True);

               # Enable Multi-Helper
               subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--action", "do_cmd", "--cmd",
                               "set_endp_flag %s AutoHelper 1"%(ena)])
               subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--action", "do_cmd", "--cmd",
                               "set_endp_flag %s AutoHelper 1"%(enb)])

               subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--action", "do_cmd", "--cmd",
                                "add_cx %s default_tm %s %s"%(cxn, ena, enb)])# capture_output=True);

               # Start traffic
               subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--action", "do_cmd",
                               "--cmd", "set_cx_state all %s RUNNING"%cxn]);

               count = count + 1

   # Traffic is started, wait requested amount of time
   print("Waiting %s seconds to let traffic run for a bit"%(dur))
   time.sleep(dur)

   # Gather probe results and record data, verify NSS, BW, Channel
   count = 0
   for sta in lfstations:
       sta_resource = "1"
       sta_name = sta;
       if sta[0].isdigit():
           tmpa = sta.split(".", 1);
           sta_resource = tmpa[0];
           sta_name = tmpa[1];

       port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  sta_resource, "--port_name", sta_name,
                                    "--show_port", "AP,Mode,Bandwidth,Signal,Status,RX-Rate"], stderr=PIPE, stdout=PIPE);
       pss = port_stats.stdout.decode('utf-8', 'ignore');

       _ap = None
       _bw = None
       _mode = None
       _rxrate = None
       _signal = None

       for line in pss.splitlines():
           m = re.search('AP:\s+(.*)', line)
           if (m != None):
               _ap = m.group(1)
           m = re.search('Bandwidth:\s+(.*)Mhz', line)
           if (m != None):
               _bw = m.group(1)
           m = re.search('Mode:\s+(.*)', line)
           if (m != None):
               _mode = m.group(1)
           m = re.search('RX-Rate:\s+(.*)', line)
           if (m != None):
               _rxrate = m.group(1)
           m = re.search('Signal:\s+(.*)', line)
           if (m != None):
               _signal = m.group(1)

       count = 0
       for p in protos:
           for t in toss:
               cxn = cxnames[count]
               count = count + 1

               # Results:  tx_bytes, rx_bytes, tx_bps, rx_bps, tx_pkts, rx_pkts, Latency
               resultsA = ["0"] * 7
               resultsB = ["0"] * 7

               ena = "%s-A"%cxn;
               enb = "%s-B"%cxn;
               enames = [ena, enb]
               for ename in enames:
                   results = [""] * 7

                   endp_stats = subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--endp_vals", "tx_bps,rx_bps,Tx Bytes,Rx Bytes,Tx Pkts,Rx Pkts,Latency",
                                                "--endp_name", ename], stderr=PIPE, stdout=PIPE);
                   pss = endp_stats.stdout.decode('utf-8', 'ignore');

                   for line in pss.splitlines():
                       #print("probe-line, endp: %s: %s"%(ename, line))
                       m = re.search('Rx Bytes:\s+(\d+)', line)
                       if (m != None):
                           results[1] = int(m.group(1))
                           if (results[1] == 0):
                               err = "ERROR:  No bytes received by data connection %s, test results may not be valid."%(ename)
                               e_tot2 += err
                               e_tot2 += "  "
                       m = re.search('Tx Bytes:\s+(\d+)', line)
                       if (m != None):
                           results[0] = int(m.group(1))
                           if (results[0] == 0):
                               err = "ERROR:  No bytes transmitted by data connection %s, test results may not be valid."%(ename)
                               e_tot2 += err
                               e_tot2 += "  "
                   
                       m = re.search('tx_bps:\s+(.*)', line)
                       if (m != None):
                           results[2] = m.group(1)

                       m = re.search('rx_bps:\s+(.*)', line)
                       if (m != None):
                           results[3] = m.group(1)

                       m = re.search('Tx Pkts:\s+(.*)', line)
                       if (m != None):
                           results[4] = m.group(1)

                       m = re.search('Rx Pkts:\s+(.*)', line)
                       if (m != None):
                           results[5] = m.group(1)

                       m = re.search('Latency:\s+(.*)', line)
                       if (m != None):
                           results[6] = m.group(1)

                       if (ena == ename):
                           resultsA = results.copy()
                       else:
                           resultsB = results.copy()

               # Now that we know both latencies, we can normalize them.
               endp_statsA = subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--action", "normalize_latency",
                                             "--lat1", resultsA[6], "--lat2", resultsB[6]], stderr=PIPE, stdout=PIPE);
               pssA = endp_statsA.stdout.decode('utf-8', 'ignore');
               endp_statsB = subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--action", "normalize_latency",
                                             "--lat1", resultsB[6], "--lat2", resultsA[6]], stderr=PIPE, stdout=PIPE);
               pssB = endp_statsB.stdout.decode('utf-8', 'ignore');

               #print("%s: latA: %s"%(cxn, resultsA[6]))
               #print("%s: latB: %s"%(cxn, resultsB[6]))
               #print("%s: pssA: %s"%(cxn, pssA))
               #print("%s: pssB: %s"%(cxn, pssB))

               for line in pssA.splitlines():
                   m = re.search('Normalized-Latency:\s+(.*)', line)
                   if (m != None):
                       resultsA[6] = m.group(1);

               for line in pssB.splitlines():
                   m = re.search('Normalized-Latency:\s+(.*)', line)
                   if (m != None):
                       resultsB[6] = m.group(1);

               for ename in enames:
                   col = 0

                   if (ena == ename):
                       results = resultsA.copy()
                   else:
                       results = resultsB.copy()

                   lat_cols = results[6].split() # min, max, avg, columns....

                   worksheet.write(row, col, cxn, center_blue); col += 1
                   worksheet.write(row, col, ename, center_blue); col += 1
                   if ename == ena:
                       worksheet.write(row, col, "%s.%s"%(sta_resource, sta_name), center_blue); col += 1
                   else:
                       worksheet.write(row, col, "%s.%s"%(u_resource, u_name), center_blue); col += 1
                   worksheet.write(row, col, p, center_blue); col += 1
                   worksheet.write(row, col, t, center_blue); col += 1
                   if ename == ena:
                       worksheet.write(row, col, _ap, center_blue); col += 1
                       worksheet.write(row, col, _bw, center_blue); col += 1
                       worksheet.write(row, col, _mode, center_blue); col += 1
                       worksheet.write(row, col, _rxrate, center_blue); col += 1
                       worksheet.write(row, col, _signal, center_blue); col += 1
                   else:
                       # Upstream is likely wired, don't print station info
                       worksheet.write(row, col, "", center_blue); col += 1
                       worksheet.write(row, col, "", center_blue); col += 1
                       worksheet.write(row, col, "", center_blue); col += 1
                       worksheet.write(row, col, "", center_blue); col += 1
                       worksheet.write(row, col, "", center_blue); col += 1

                   #print("results[2]:%s  3: %s"%(results[2], results[3]))

                   worksheet.write(row, col, "%.2f"%(float(results[2]) / 1000000), center_tan); col += 1
                   worksheet.write(row, col, "%.2f"%(float(results[3]) / 1000000), center_tan); col += 1
                   worksheet.write(row, col, "%.2f"%((float(resultsA[2]) + float(resultsB[2])) / 1000000), center_tan); col += 1
                   worksheet.write(row, col, "%.2f"%((float(resultsA[3]) + float(resultsB[3])) / 1000000), center_tan); col += 1
                   worksheet.write(row, col, lat_cols[2], center_yel); col += 1
                   worksheet.write(row, col, lat_cols[0], center_yel); col += 1
                   worksheet.write(row, col, lat_cols[1], center_yel); col += 1
                   for x in range(17):
                       worksheet.write(row, col, lat_cols[x + 3], center_peach); col += 1

                   if (e_tot2 == ""):
                       worksheet.write(row, col, e_tot2, green_left); col += 1
                   else:
                       worksheet.write(row, col, e_tot2, red_left); col += 1
                   row += 1

   # Stop traffic
   for cxn in cxnames:
       cmd = "set_cx_state all %s STOPPED"%cxn
       #print("Stopping CX: %s with command: %s"%(cxn, cmd));

       subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--action", "do_cmd",
                       "--cmd", cmd]);

   workbook.close()


# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
if __name__ == '__main__':
    main()
    print("Xlsx results stored in %s"%(outfile))

####
####
####
