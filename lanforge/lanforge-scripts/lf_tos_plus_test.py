#!/usr/bin/python3
'''

Create connections using stations with different a/b/g/n/AC/AX modes,
traffic with different QoS, packet size, requested rate, and tcp or udp protocol.
Report the latency and other throughput values.

Optionally start packet-capture on secondary radio(s) and upstream port.

When specifying ports, if the port starts with [Number]., like 1.eth1, then the 1 specifies
the resource ID.

The --cx argument is defined as:  station-radio, station-port, mode, upstream-port, protocol, pkt-size, speed_ul, speed_dl, QoS.
Pass this argument multiple times to create multiple connections.
The --radio argument is defined as: radio, spatial-streams, channel
Use NA if you do not want to change from current values.  Use 0 for any channel.

Supported modes are: a, b, g, abg, abgn, bgn, bg, abgnAC, anAC, an, bgnAC, abgnAX, bgnAX, anAX

If sniffer_radios is specified, then the lf_sniff.py script will be started in the background once
the stations have become admin-up, and the sniff will run for the entire duration time specified
(there is not a good way to stop the capture early based on packets-sent since on-the-air frames
are very likely more than the PDU count)

# Run connections on wlan0 and sta0 for 1 minute, set radio wiphy0 to use any frequency
# and 2 spatial streams.  Use wiphy2 as a sniffer, stop traffic after 10,000 PDUs
# have been sent.  Sniffer radio will automatically change to the correct settings
# to sniff the first station. --wait_sniffer 1 tells the script to pause until the
# sniffer process has completed.

./lf_tos_plus_test.py --dur 1 --lfmgr 192.168.100.156 --ssid NETGEAR68-5G --passwd aquaticbug712 \
  --radio "1.wiphy0 2 0" --txpkts 9999 --wait_sniffer 1 \
  --cx "1.wiphy0 1.wlan0 an 1.eth1 udp 1024 10000 500000000 BK" \
  --cx "1.wiphy0 1.wlan0 an 1.eth1 udp MTU 10000 500000000 VI" \
  --cx "1.wiphy0 1.sta0 anAC 1.eth1 tcp 1472 56000 2000000 BK" \
  --sniffer_radios "1.wiphy2"

# You can also create connections between non-station endpoints.
./lf_tos_plus_test.py --dur 1 --lfmgr 192.168.100.156 --txpkts 99 \
 --cx "NA 1.rddVR0 NA 1.rddVR1 tcp MTU 1000000 2000000 0"  --wait_sniffer 1

make sure pexpect, pandas is installed:
$ sudo yum install python3-pandas
$ sudo yum install python3-pexpect
$ sudo yum install python3-xlsxwriter

You might need to install pexpect-serial using pip:
$ pip3 install pexpect-serial
$ pip3 install XlsxWriter

'''

# TODO:  Maybe HTML output too?
# TODO:  Allow selecting tabs or commas for output files

import sys
import os
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
import datetime
import pandas as pd
from subprocess import PIPE

NL = "\n"
CR = "\r\n"
Q = '"'
A = "'"
FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'

lfmgr = "127.0.0.1"
cx_strs = []  # station-radio, station-port, mode, upstream-port, protocol, pkt-size, speed_ul, speed_dl, QoS.
outfile = "tos+_results.xlsx"
dur = 5 * 60
passwd = ""
ssid = "Test-SSID"
security = "open"
radio_strs = []  # Radios to modify:  radio nss channel
txpkts = "0" # 0 == Run forever
sniffer_radios = ""
wait_sniffer = False

# rssi_adjust = (current_nf - nf_at_calibration)

def usage():
   print("$0 ")
   print("--outfile: Write results here.")
   print("--cx: Connection tuple: station-radio station-port mode upstream-port protocol pkt-size speed_ul speed_dl QoS")
   print("--radio: Radio tuple:  radio nss channel");
   print("--lfmgr: LANforge manager IP address")
   print("--duration: Duration to run traffic, in minutes")
   print("--ssid: AP's SSID")
   print("--passwd: Optional: password (do not add this option for OPEN)")
   print("--security: Default is 'open', or if passwd is configured, default is wpa2.  wpa3 is also valid option")
   print("--txpkts: Optional: amount of packets to transmit (and then stop the data connections)")
   print("--sniffer_radios: Optional: list of radios to sniff wifi traffic \"1.wiphy2 1.wiphy4\")")
   print("--wait_sniffer: Optional: 1 means wait on sniffer to finish before existing script")
   print("-h|--help")

def main():
   global lfmgr
   global cx_strs
   global outfile
   global dur
   global passwd
   global ssid
   global security
   global radio_strs
   global txpkts
   global sniffer_radios
   global wait_sniffer

   do_sniff = False

   parser = argparse.ArgumentParser(description="ToS++ report Script")
   parser.add_argument("--cx",  type=str, action='append', help="Connection tuple: station-radio station-port mode upstream-port protocol pkt-size speed_ul speed_dl QoS")
   parser.add_argument("--radio",  type=str, action='append', help="Radio tuple:  radio nss channel")
   parser.add_argument("--lfmgr",        type=str, help="LANforge Manager IP address")
   parser.add_argument("--outfile",     type=str, help="Output file for csv data")
   parser.add_argument("--duration",     type=float, help="Duration to run traffic, in minutes.  If txpkts is specified, that may stop the test earlier.")
   parser.add_argument("--ssid",         type=str, help="AP's SSID")
   parser.add_argument("--passwd",       type=str, help="AP's password if using PSK authentication, skip this argement for OPEN")
   parser.add_argument("--security",     type=str, help="Default is 'open', or if passwd is configured, default is wpa2.  wpa3 is also valid option")
   parser.add_argument("--txpkts",       type=str, help="Optional:  Packets (PDUs) to send before stopping data connections  Default (0) means infinite")
   parser.add_argument("--sniffer_radios", type=str, help="Optional:  list of radios to sniff wifi traffic \"1.wiphy2 1.wiphy4\"")
   parser.add_argument("--wait_sniffer", type=str, help="Optional: 1 means wait on sniffer to finish before existing script.\"")
   
   args = None
   try:
      args = parser.parse_args()
      cx_strs = args.cx.copy()
      if (args.radio != None):
          radio_strs = args.radio.copy()
      if (args.lfmgr != None):
          lfmgr = args.lfmgr
      if (args.duration != None):
          dur = args.duration * 60
      if (args.ssid != None):
          ssid = args.ssid
      if (args.passwd != None):
          passwd = args.passwd
          security = "wpa2"
      if (args.security != None):
          security = args.security
      if (args.outfile != None):
          outfile = args.outfile
      if (args.txpkts != None):
          txpkts = args.txpkts
      if (args.sniffer_radios != None):
          sniffer_radios = args.sniffer_radios
          do_sniff = True
      if (args.wait_sniffer != None):
          do_sniff = True
          wait_sniffer = args.wait_sniffer == "1"
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
   worksheet.write(row, col, 'Endpoint\nTX Pkt\nSize', dtan_bold); col += 1
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

   sta_to_mode = {}  # map station name to mode
   cxnames = []      # list of all cxnames
   endpnames = []
   endp_to_port = {}
   endp_to_pktsz = {}
   endp_to_proto = {}
   endp_to_tos = {}

   e_tot = ""

   opposite_speed = 56000
   count = 0

   # Configure radios as requested
   for rad in radio_strs:
       ra = rad.split()
       radio = ra[0]
       nss = ra[1]
       ch = ra[2]

       rad_resource = "1"
       rad_name = radio;
       if radio[0].isdigit():
           tmpa = radio.split(".", 1);
           rad_resource = tmpa[0];
           rad_name = tmpa[1];

       print("Setting radio %s.%s NSS %s Channel %s"%(rad_resource, rad_name, nss, ch))
       subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  rad_resource, "--port_name", rad_name,
                       "--set_nss", nss, "--set_channel", ch]);

   upstreams = []
   stations = []
   for cx in cx_strs:
       cxa = cx.split()
       #station-radio, station-port, mode, upstream-port, protocol, pkt-size, speed_ul, speed_dl, QoS.
       radio = cxa[0]
       sta = cxa[1]
       mode = cxa[2]
       upstream_port = cxa[3]
       p = cxa[4]
       pkt_sz = cxa[5]
       cx_speed_ul = cxa[6]
       cx_speed_dl = cxa[7]
       t = cxa[8]  # qos

       u_name = upstream_port
       u_resource = 1
       if (upstream_port[0].isdigit()):
           tmpa = upstream_port.split(".", 1)
           u_resource = tmpa[0]
           u_name = tmpa[1]

       sta_resource = "1"
       sta_name = sta;
       if sta[0].isdigit():
           tmpa = sta.split(".", 1);
           sta_resource = tmpa[0];
           sta_name = tmpa[1];

       sta_key = "%s.%s"%(sta_resource, sta_name)
       if sta_key in sta_to_mode:
           old_mode = sta_to_mode[sta_key]
           if old_mode != mode:
               emsg = ("ERROR:  Skipping connection: \"%s\", mode conflicts with previous mode: %s"%(cx, old_mode))
               e_tot.append(cxa)
               print(emsg)
               continue
       else:
           sta_to_mode[sta_key] = mode
           stations.append(sta_key)

       ukey = "%s.%s"%(u_resource, u_name)
       if not ukey in upstreams:
           upstreams.append(ukey)

       if radio != "NA":
           rad_resource = "1"
           rad_name = radio;
           if radio[0].isdigit():
               tmpa = radio.split(".", 1);
               rad_resource = tmpa[0];
               rad_name = tmpa[1];

           # Create or update station with requested mode
           subprocess.run(["./lf_associate_ap.pl", "--mgr", lfmgr, "--resource", rad_resource, "--action", "add",
                           "--radio", rad_name, "--ssid", ssid, "--passphrase", passwd, "--security", security,
                           "--first_sta", sta_name, "--first_ip", "DHCP", "--wifi_mode", mode, "--num_stations", "1"])
       else:
           # Assume it should be sniffed.
           ukey = "%s.%s"%(sta_resource, sta_name)
           if not ukey in upstreams:
               upstreams.append(ukey)

       # Up station / A-side Port
       subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  sta_resource, "--port_name", sta_name,
                       "--set_ifstate", "up"]); 

       i = 0
       wait_ip_print = False;
       wait_assoc_print = False;
       # Wait until LANforge station connects
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

           if sta_name.startswith("wlan") or sta_name.startswith("sta"):
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
           else:
               if ((_ip != None) and (_ip != "0.0.0.0")):
                   print("Port is associated with IP address.")
                   break
               else:
                   if (not wait_ip_print):
                       print("Waiting for port %s.%s to get IP Address."%(sta_resource, sta_name))
                       wait_ip_print = True

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

       # Station is up, create connection
       # Create connections.
       # First, delete any old ones
       cxn = "scr-tos-%i"%count
       ena = "scr-tos-%i-A"%count
       enb = "scr-tos-%i-B"%count

       cxnames.append(cxn)
       endpnames.append(ena)
       endpnames.append(enb)

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

       endp_to_port[ena] = "%s.%s"%(sta_resource, sta_name);
       endp_to_pktsz[ena] = pkt_sz
       endp_to_proto[ena] = p;
       endp_to_tos[ena] = t;
       endp_to_port[enb] = "%s.%s"%(u_resource, u_name);
       endp_to_pktsz[enb] = pkt_sz
       endp_to_proto[enb] = p;
       endp_to_tos[enb] = t;

       # Now, create the new connection
       subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  "%s"%sta_resource, "--action", "create_endp", "--port_name", sta_name,
                       "--endp_type", cx_proto, "--endp_name", ena, "--speed", "%s"%cx_speed_ul, "--report_timer", "1000", "--tos", t,
                       "--min_pkt_sz", pkt_sz, "--multicon", "1", "--pkts_to_send", txpkts])#, capture_output=True);
       subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  "%s"%u_resource, "--action", "create_endp", "--port_name", u_name,
                       "--endp_type", cx_proto, "--endp_name", enb, "--speed", "%s"%cx_speed_dl, "--report_timer", "1000", "--tos", t,
                       "--min_pkt_sz", pkt_sz, "--multicon", "1", "--pkts_to_send", txpkts])#  capture_output=True);

       # Enable Multi-Helper
       subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--action", "do_cmd", "--cmd",
                       "set_endp_flag %s AutoHelper 1"%(ena)])
       subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--action", "do_cmd", "--cmd",
                       "set_endp_flag %s AutoHelper 1"%(enb)])
       
       subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--action", "do_cmd", "--cmd",
                       "add_cx %s default_tm %s %s"%(cxn, ena, enb)])# capture_output=True);
       count = count + 1

   # Start sniffer?
   if do_sniff:
       lfstations = ""
       lfupstreams = ""
       if sniffer_radios != "":
           radios = sniffer_radios.split()
           ri = 0
           for r in radios:
               lfstations = lfstations + " " + stations[ri]
               ri = ri + 1

       for u in upstreams:
           lfupstreams = lfupstreams + " " + u

       # Add 15 seconds to capture length in case it takes a bit of time to start all
       # of the connections.
       cmd = ["./lf_sniff.py", "--lfmgr", lfmgr, "--duration", "%f"%((dur + 15) / 60)]
       if lfstations != "":
           cmd.extend(["--station", lfstations, "--sniffer_radios", sniffer_radios])
       if lfupstreams != "":
           cmd.extend(["--upstreams", lfupstreams])

       subprocess.run(cmd)

   sniff_done_at = time.time() + dur + 15;
   
   # All traffic connects are created, now start them all
   for cxn in cxnames:
       # Start traffic
       subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--action", "do_cmd",
                       "--cmd", "set_cx_state all %s RUNNING"%cxn]);

   # Traffic is started, wait requested amount of time
   stop_at = time.time() + dur;
   if txpkts == 0:
       print("Waiting %s seconds to let traffic run for a bit"%(dur))
       time.sleep(dur)
   else:
       # Wait until connections are done transmitting and all are stopped
       print("Waiting until all connections have finished transmitting %s PDUs and have stopped themselves."%txpkts);
       done = False
       while not done:
           if time.time() > stop_at:
               print("Duration expired, stop waiting for Endpoints to quiesce.")
               break

           foundone = False
           for ename in endpnames:
               #print("Checking endpoint: %s"%ename)

               endp_stats = subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--endp_name", ename,
                                            "--endp_vals", "Endpoint-flags"], stderr=PIPE, stdout=PIPE);
               ess = endp_stats.stdout.decode('utf-8', 'ignore');
               for line in ess.splitlines():
                   #print("endp-stats line: %s"%line)
                   m = re.search('Endpoint-flags:\s+(.*)', line)
                   if (m != None):
                       flags = m.group(1)
                       if not "NOT_RUNNING" in flags:
                           foundone = True
                           #print("Flags, was running: %s"%flags)
                           break
                       #else:
                           #print("Flags, was not running: %s"%flags)

               if foundone:
                   break
           if not foundone:
               print("All endpoints stopped, continuing on.")
               done = True
               break
           sleep(3)  # wait 3 seconds, then poll again                   
       
   # Gather probe results and record data, verify NSS, BW, Channel
   sta_stats = {}  # Key is resource.station, holds array of values

   for sta in sta_to_mode:
       sta_resource = "1"
       sta_name = sta;
       if sta[0].isdigit():
           tmpa = sta.split(".", 1);
           sta_resource = tmpa[0];
           sta_name = tmpa[1];

       sta_key = "%s.%s"%(sta_resource, sta_name)
       print("Checking station stats, key: %s"%(sta_key))

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

       sta_stats[sta_key] = [_ap, _bw, _mode, _rxrate, _signal];
       print("sta-stats found: %s, mode: %s  bw: %s"%(sta_key, _mode, _bw));

   for cxn in cxnames:
       # Results:  tx_bytes, rx_bytes, tx_bps, rx_bps, tx_pkts, rx_pkts, Latency
       resultsA = ["0"] * 7
       resultsB = ["0"] * 7
       e_tot2 = ""

       ena = "%s-A"%cxn;
       enb = "%s-B"%cxn;
       enames = [ena, enb]
       for ename in enames:
           results = [""] * 7

           endp_stats = subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--endp_vals", "RealTxRate,RealRxRate,Tx Bytes,Rx Bytes,Tx Pkts,Rx Pkts,Latency",
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

               m = re.search('RealTxRate:\s+(.*)bps', line)
               if (m != None):
                   results[2] = m.group(1)

               m = re.search('RealRxRate:\s+(.*)bps', line)
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

           en_port = endp_to_port[ename]
           worksheet.write(row, col, en_port, center_blue); col += 1

           worksheet.write(row, col, endp_to_proto[ename], center_blue); col += 1
           worksheet.write(row, col, endp_to_tos[ename], center_blue); col += 1

           if ename == ena:
               key = en_port
               #print("endp, key: %s"%(key));
               sta_rpt = sta_stats[key]
               worksheet.write(row, col, sta_rpt[0], center_blue); col += 1
               worksheet.write(row, col, sta_rpt[1], center_blue); col += 1
               worksheet.write(row, col, sta_rpt[2], center_blue); col += 1
               worksheet.write(row, col, sta_rpt[3], center_blue); col += 1
               worksheet.write(row, col, sta_rpt[4], center_blue); col += 1
           else:
               # Upstream is likely wired, don't print station info
               worksheet.write(row, col, "", center_blue); col += 1
               worksheet.write(row, col, "", center_blue); col += 1
               worksheet.write(row, col, "", center_blue); col += 1
               worksheet.write(row, col, "", center_blue); col += 1
               worksheet.write(row, col, "", center_blue); col += 1

           #print("results[2]:%s  3: %s"%(results[2], results[3]))
           
           worksheet.write(row, col, endp_to_pktsz[ename], center_tan); col += 1
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

   # Convert workbook to csv

   csvfname = "%s.csv"%(outfile)
   csv = open(csvfname, "w")
   df = pd.read_excel(outfile)
   
   list_of_columns = df.columns.values

   # Print header
   for c in range(len(list_of_columns)):
       cell = list_of_columns[c]
       if cell != cell:
           cell = ""
       # convert newlines to spaces
       if isinstance(cell, str):
           cell = cell.replace('\n', ' ')
           cell = cell.replace('\r', '')
           # Remove commas
           cell = cell.replace(',', '')
       if c == 0:
           csv.write(cell)
       else:
           csv.write(",%s"%(cell))
   csv.write("\n")

   for r in range (len(df)):
       for c in range(len(list_of_columns)):
           #print("list-of-columns[c]: %s"%(list_of_columns[c]))
           cell = df[list_of_columns[c]][r]
           #print("cell: %s  c: %i r: %i"%(cell, c, r))
           # NAN check
           if cell != cell:
               cell = ""
           if isinstance(cell, str):
               # convert newlines to spaces
               cell = cell.replace('\n', ' ')
               cell = cell.replace('\r', '')
               # Remove commas
               cell = cell.replace(',', '')
           if c == 0:
               csv.write(cell)
           else:
               csv.write(",%s"%(cell))
       csv.write("\n");
   csv.close()
   print("CSV report data saved to: %s"%(csvfname))

   tstr = ""
   if sniffer_radios != "":
       now = time.time()
       if now < sniff_done_at:
           waitfor = int(sniff_done_at - now);
           if wait_sniffer:
               print("Waiting %i seconds until sniffer completes."%(waitfor))
               sleep(waitfor)

               # move capture files into a new directory
               tstr = time.strftime("%Y-%m-%d-%H:%M:%S")
               os.mkdir(tstr)
               os.system("mv /home/lanforge/*.pcap %s"%(tstr))
               print("Captures are found in directory: %s"%tstr)
           else:
               print("Sniffer will complete in %f seconds."%(waitfor))


   # Create a file easily sourced by a shell script to communicate the directory
   # name and such.
   fname = "TOS_PLUS.sh"
   sh = open(fname, "w")
   sh.write("CAPTURE_DIR=%s\n"%(tstr))
   sh.write("CSV_FILE=%s\n"%(csvfname))
   sh.write("XLSX_FILE=%s\n"%(outfile))

   sh.close()

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
if __name__ == '__main__':
    main()
    print("Xlsx results stored in %s"%(outfile))

####
####
####
