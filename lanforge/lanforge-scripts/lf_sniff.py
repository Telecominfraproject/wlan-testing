#!/usr/bin/python3
'''

Sniff stations on one set of radios using secondary radios.

make sure pexpect is installed:
$ sudo yum install python3-pexpect
$ sudo yum install python3-xlsxwriter

You might need to install pexpect-serial using pip:
$ pip3 install pexpect-serial
$ pip3 install XlsxWriter

The user is responsible for setting up the stations oustide of this script, however.

When specifying ports, if the port starts with [Number]., like 1.eth1, then the 1 specifies
the resource ID.

./lf_sniff.py --lfmgr 192.168.100.178 \
  --station "1.wlan0 1.wlan1" --sniffer_radios "2.wiphy0 2.wiphy1" \
  --duration 5

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
sniffer_radios = "2.wiphy0"
upstream = ""
dur = 5 * 60
moni_flags = "0x100000000" # 160Mhz mode enabled

# rssi_adjust = (current_nf - nf_at_calibration)

def usage():
   print("$0 ")
   print("--station: LANforge station names (1.wlan0 1.wlan1 ...)")
   print("--sniffer_radios: LANforge radios to use as sniffers (2.wiphy0 2.wiphy1 ...)")
   print("--lfmgr: LANforge manager IP address")
   print("--duration: Duration to run traffic, in minutes")
   print("--moni_flags: Monitor flags (see LANforge CLI help for set_wifi_monitor command)  Default enables 160Mhz")
   print("--upstreams: Upstream ports to sniff (1.eth1 ...)")
   print("-h|--help")

def main():
   global lfmgr
   global lfstation
   global upstream
   global sniffer_radios
   global dur
   global moni_flags

   parser = argparse.ArgumentParser(description="Sniffer control Script")
   parser.add_argument("--sniffer_radios",  type=str, help="LANforge sniffer radios to use (2.wiphy0 2.wiphy1 ...)")
   parser.add_argument("--station",        type=str, help="LANforge stations to use (1.wlan0 1.wlan1 etc)")
   parser.add_argument("--lfmgr",        type=str, help="LANforge Manager IP address")
   parser.add_argument("--duration",     type=float, help="Duration to sniff, in minutes")
   parser.add_argument("--moni_flags",   type=str, help="Monitor port flags, see LANforge CLI help for set_wifi_monitor.  Default enables 160Mhz")
   parser.add_argument("--upstreams",    type=str, help="Upstream ports to sniff (1.eth1 ...)")
   parser.add_argument("--moni_idx", type=str, help="Optional monitor number", default=None)
   
   args = None
   try:
      args = parser.parse_args()
      if (args.station != None):
          lfstation = args.station
      if (args.upstreams != None):
          upstream = args.upstreams
      if (args.sniffer_radios != None):
          sniffer_radios = args.sniffer_radios
      if (args.lfmgr != None):
          lfmgr = args.lfmgr
      if (args.duration != None):
          dur = args.duration * 60
      if (args.moni_flags != None):
          moni_flags = args.moni_flags
      filehandler = None
   except Exception as e:
      logging.exception(e);
      usage()
      exit(2);

   # Use subprocess.check_output("Cmd") to utilize existing LF scripts.

   upstreams = upstream.split()
   lfstations = lfstation.split()
   radios = sniffer_radios.split()
   monis_n = []  # monitor device names
   monis_r = []  # monitor device resources

   idx = 0
   for sta in lfstations:
       sta_resource = "1"
       sta_name = sta;
       if sta[0].isdigit():
           tmpa = sta.split(".", 1);
           sta_resource = tmpa[0];
           sta_name = tmpa[1];

       # Assume station is up and/or something else is bringing it up

       channel = 36
       bsssid = "00:00:00:00:00:00"

       i = 0
       wait_ip_print = False;
       wait_assoc_print = False;
       # Wait until LANforge station connects
       while True:
           port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  sta_resource, "--port_name", sta_name,
                                        "--show_port", "AP,IP,Mode,NSS,Bandwidth,Probed-Channel,Signal,Noise,Status,RX-Rate"], stdout=PIPE, stderr=PIPE);
           pss = port_stats.stdout.decode('utf-8', 'ignore');

           _status = None
           _ip = None

           for line in pss.splitlines():
               #print("line: %s\n"%line)
               m = re.search('AP:\s+(.*)', line)
               if (m != None):
                   bssid = m.group(1)
               m = re.search('Status:\s+(.*)', line)
               if (m != None):
                   _status = m.group(1)
               m = re.search('Probed-Channel:\s+(.*)', line)
               if (m != None):
                   channel = m.group(1)
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

       # Get station AID and other info

       port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr,
                                    "--cli_cmd", "probe_port 1 %s %s"%(sta_resource, sta_name)], stdout=PIPE, stderr=PIPE);
       pss = port_stats.stdout.decode('utf-8', 'ignore');

       aid = 0
       for line in pss.splitlines():
           m = re.search('Local-AID:\s+(.*)', line)
           if (m != None):
               aid = m.group(1)
               break

       # Create monitor on radio X
       rad = radios[idx]
       rad_resource = "1"
       rad_name = rad;
       #print("idx: %i moni: %s\n"%(idx, moni))
       if rad[0].isdigit():
           tmpa = rad.split(".", 1)
           rad_resource = tmpa[0]
           rad_name = tmpa[1]

       # Set channel on the radio
       subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  rad_resource, "--port_name", rad_name,
                       "--set_channel", "%s"%channel]);

       # Get radio index so we can name the monitor similar to how the system would auto-create them
       port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  rad_resource, "--port_name", rad_name,
                                    "--show_port", "Port"], stdout=PIPE, stderr=PIPE);
       pss = port_stats.stdout.decode('utf-8', 'ignore');


       moni_idx = args.moni_idx
       if args.moni_idx is None:
           for line in pss.splitlines():
               m = re.search('Port:\s+(.*)', line)
               if (m != None):
                   moni_idx = m.group(1)

       # Create monitor interface
       mname = "moni%sa"%(moni_idx);
       subprocess.run(["./lf_portmod.pl", "--manager", lfmgr,
                       "--cli_cmd", "add_monitor 1 %s %s %s %s 0xFFFFFFFFFFFF %s %s"%(rad_resource, rad_name, mname, moni_flags, aid, bssid)])

       print("Created monitor interface: %s on resource %s\n"%(mname, rad_resource))
       monis_n.append(mname)
       monis_r.append(rad_resource)

       idx = idx + 1

   # Start sniffing on all monitor ports
   idx = 0
   sflags = "0x02"  # dumpcap, no terminal
   for m in monis_n:
       r = monis_r[idx]

       # Wait for monitor to be non-phantom
       isph = True
       while isph:
           port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  r, "--port_name", m,
                                        "--show_port", "Current"], stdout=PIPE, stderr=PIPE);
           pss = port_stats.stdout.decode('utf-8', 'ignore');
           for line in pss.splitlines():
               #print("line: %s\n"%line)
               ma = re.search('Current:\s+(.*)', line)
               if (ma != None):
                   cf = ma.group(1);
                   isph = False
                   for f in cf.split():
                       if (f == "PHANTOM"):
                           isph = True
                           break
           if isph:
               print("Waiting for monitor port %s.%s to become non-phantom\n"%(r, m));
               sleep(1)

       
       print("Starting sniffer on port %s.%s for %s seconds, saving to file %s.pcap on resource %s\n"%(r, m, dur, m, r))
       subprocess.run(["./lf_portmod.pl", "--manager", lfmgr,
                       "--cli_cmd", "sniff_port 1 %s %s NA %s %s.pcap %i"%(r, m, sflags, m, float(dur))]);
       idx = idx + 1

   # Start sniffing on all upstream ports
   for u in upstreams:
       u_resource = "1"
       u_name = u;
       if u[0].isdigit():
           tmpa = u.split(".", 1);
           u_resource = tmpa[0];
           u_name = tmpa[1];
           
       print("Starting sniffer on upstream port %s.%s for %s seconds, saving to file %s.pcap on resource %s\n"%(u_resource, u_name, dur, u_name, u_resource))
       subprocess.run(["./lf_portmod.pl", "--manager", lfmgr,
                       "--cli_cmd", "sniff_port 1 %s %s NA %s %s.pcap %i"%(u_resource, u_name, sflags, u_name, float(dur))]);

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
if __name__ == '__main__':
    main()

####
####
####
