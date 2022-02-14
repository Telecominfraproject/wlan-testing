#!/usr/bin/python3
'''

make sure pexpect is installed:
$ sudo yum install python3-pexpect

You might need to install pexpect-serial using pip:
$ pip3 install pexpect-serial

./tos_plus_auto.py
'''


import sys
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

import os
import re
import logging
import time
from time import sleep
import pprint
import telnetlib
import argparse
import pexpect
import subprocess

ptype="QCA"
tos="BE" #Allowed values are BE/BK/VI/VO

FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'

def usage():
   print("$0 used connect to automated a test case using cisco controller and LANforge tos-plus script:")
   print("-p|--ptype:  AP Hardware type")
   print("--tos:  TOS type we are testing, used to find output in csv data: BE BK VI VO")
   print("-h|--help")
   print("-l|--log file: log messages here")

# see https://stackoverflow.com/a/13306095/11014343
class FileAdapter(object):
    def __init__(self, logger):
        self.logger = logger
    def write(self, data):
        # NOTE: data can be a partial line, multiple lines
        data = data.strip() # ignore leading/trailing whitespace
        if data: # non-blank
           self.logger.info(data)
    def flush(self):
        pass  # leave it to logging to flush properly

def main():
   global ptype
   global tos

   parser = argparse.ArgumentParser(description="TOS Plus automation script")
   parser.add_argument("-p", "--ptype",    type=str, help="AP Hardware type")
   parser.add_argument("-l", "--log",     type=str, help="logfile for messages, stdout means output to console")
   parser.add_argument("-t", "--tos",     type=str, help="TOS type we are testing, used to find output in csv data: BE BK VI VO")
   
   args = None
   try:
      args = parser.parse_args()
      if (args.ptype != None):
         ptype = args.ptype
      logfile = args.log
      
   except Exception as e:
      logging.exception(e);
      usage()
      exit(2);


   console_handler = logging.StreamHandler()
   formatter = logging.Formatter(FORMAT)
   logg = logging.getLogger(__name__)
   logg.setLevel(logging.DEBUG)
   file_handler = None
   if (logfile is not None):
       if (logfile != "stdout"):
           file_handler = logging.FileHandler(logfile, "w")
           file_handler.setLevel(logging.DEBUG)
           file_handler.setFormatter(formatter)
           logg.addHandler(file_handler)
           logging.basicConfig(format=FORMAT, handlers=[file_handler])
       else:
           # stdout logging
           logging.basicConfig(format=FORMAT, handlers=[console_handler]) 

   # Set up cisco controller.  For now, variables are hard-coded.
   dest = '172.19.27.95'
   port = '2013'
   port_ap = '2014'
   ap = 'AxelMain'
   user = 'cisco'
   passwd = 'Cisco123'
   user_ap = 'cisco'
   passwd_ap = 'Cisco123'
   wlan = 'wlan_open'
   wlanID = '6'

   subprocess.run(["./wifi_ctl_9800_3504.py", "-d", dest, "-o", port, "-s", "telnet", "-l", "stdout", "-a", ap, "-u", "cisco", "-p", "Cisco123", "-w", wlan, "-i", wlanID,
                  "--action", "wlan"], capture_output=True)
   subprocess.run(["./wifi_ctl_9800_3504.py", "-d", dest, "-o", port, "-s", "telnet", "-l", "stdout", "-a", ap, "-u", "cisco", "-p", "Cisco123", "-w", wlan, "-i", wlanID,
                  "--action", "wlan_security"], capture_output=True)
   subprocess.run(["./wifi_ctl_9800_3504.py", "-d", dest, "-o", port, "-s", "telnet", "-l", "stdout", "-a", ap, "-u", "cisco", "-p", "Cisco123", "-w", wlan, "-i", wlanID,
                  "--action", "wlan_qos", "--value", "platinum"], capture_output=True)
   subprocess.run(["./wifi_ctl_9800_3504.py", "-d", dest, "-o", port, "-s", "telnet", "-l", "stdout", "-a", ap, "-u", "cisco", "-p", "Cisco123", "-w", wlan, "-i", wlanID,
                  "--action", "enable_wlan"], capture_output=True)
   output01 = subprocess.run(["./wifi_ctl_9800_3504.py", "-d", dest, "-o", port, "-s", "telnet", "-l", "stdout", "-a", ap, "-u", "cisco", "-p", "Cisco123", "--action", "show", 
                  "--value", "wlan summary"], capture_output=True)
   #pss = output01.stdout.decode('utf-8', 'ignore');
   #print(pss)
   print(output01)
   subprocess.run(["./wifi_ctl_9800_3504.py", "-d", dest, "-o", port, "-s", "telnet", "-l", "stdout", "-a", ap, "-u", "cisco", "-p", "Cisco123", "-b", "b", "--action", 
                  "disable"], capture_output=True)
   subprocess.run(["./wifi_ctl_9800_3504.py", "-d", dest, "-o", port, "-s", "telnet", "-l", "stdout", "-a", ap, "-u", "cisco", "-p", "Cisco123", "-b", "a", "--action", 
                  "disable"], capture_output=True)
   subprocess.run(["./wifi_ctl_9800_3504.py", "-d", dest, "-o", port, "-s", "telnet", "-l", "stdout", "-a", ap, "-u", "cisco", "-p", "Cisco123", "-b", "a", "--action", 
                  "channel", "--value", "149"], capture_output=True)
   subprocess.run(["./wifi_ctl_9800_3504.py", "-d", dest, "-o", port, "-s", "telnet", "-l", "stdout", "-a", ap, "-u", "cisco", "-p", "Cisco123", "-b", "a", "--action", 
                  "bandwidth", "--value", "80"], capture_output=True)
   subprocess.run(["./wifi_ctl_9800_3504.py", "-d", dest, "-o", port, "-s", "telnet", "-l", "stdout", "-a", ap, "-u", "cisco", "-p", "Cisco123", "-b", "a", "--action", 
                  "enable"], capture_output=True)
   #subprocess.run("python3 wifi_ctl_9800_3504.py -d %s  -o %s -s telnet -l stdout -a %s -u %s -p %s -w %s -i %s --action wlan"%(dest, port, ap, user, passwd, wlan, wlanID))
   #subprocess.run("./wifi_ctl_9800_3504.py", "-d %s  -o %s -s telnet -l stdout -a %s -u %s -p %s -w %s -i %s --action wlan_qos --value platinum"%(dest, port, ap, user, passwd, wlan, wlanID))
   #subprocess.run("python3 wifi_ctl_9800_3504.py -d %s  -o %s -s telnet -l stdout -a %s -u %s -p %s --action show --value \"wlan summary\""%(dest, port, ap, user, passwd))
   #subprocess.run("python3 wifi_ctl_9800_3504.py -d %s  -o %s -s telnet -l stdout -a %s -u %s -p %s -b b --action disable"%(dest, port, ap, user, passwd))
   #subprocess.run("python3 wifi_ctl_9800_3504.py -d %s  -o %s -s telnet -l stdout -a %s -u %s -p %s -b a --action disable"%(dest, port, ap, user, passwd))
   #subprocess.run("python3 wifi_ctl_9800_3504.py -d %s  -o %s -s telnet -l stdout -a %s -u %s -p %s -b a --action channel --value 149"%(dest, port, ap, user, passwd))
   #subprocess.run("python3 wifi_ctl_9800_3504.py -d %s  -o %s -s telnet -l stdout -a %s -u %s -p %s -b a --action bandwidth --value 80"%(dest, port, ap, user, passwd))
   #subprocess.run("python3 wifi_ctl_9800_3504.py -d %s  -o %s -s telnet -l stdout -a %s -u %s -p %s -b a --action enable"%(dest, port, ap, user, passwd))

   #Clear Stormbreaker stats on AP
   subprocess.run(["./cisco_ap.py", "-d", dest, "-o", port_ap, "-s", "telnet", "-l", "stdout", "-a", ap, "-u", "cisco", "-p", "Cisco123", "--action", "clear_counter"], capture_output=True)
   
   # Run the tos plus script to generate traffic and grab capture files.
   # You may edit this command as needed for different behaviour.
   os.system('python3 ./lf_tos_plus_test.py --dur 1 --lfmgr localhost --ssid wlan_open --radio "1.wiphy0 2 0" --txpkts 9999 --wait_sniffer 1  --cx "1.wiphy0 1.wlan0 anAX 1.eth2 udp 1024 10000 5000000000 184" --sniffer_radios "1.wiphy2"')
   #output02 = subprocess.run(["./lf_tos_plus_test.py", "--dur", "1", "--lfmgr", "localhost", "--ssid", wlan, "--radio", "1.wiphy0 2 0", "--txpkts", "10000", 
   #               "--wait_sniffer", "1", "--cx", "1.wiphy0 1.wlan0 anAX 1.eth2 udp 1024 10000 50000000 184", "--sniffer_radios", "1.wiphy2"], capture_output=True)

   #Read Stormbreaker exported stats after the test
   output02 = subprocess.run(["./cisco_ap.py", "-d", dest, "-o", port_ap, "-s", "telnet", "-l", "stdout", "-a", ap, "-u", "cisco", "-p", "Cisco123", "--action", "show", 
                              "--value", "interfaces dot11Radio 1 traffic distribution periodic data exported"], capture_output=True)
   rslt = output02.stdout.decode('utf-8', 'ignore');

   ap_at_us = -1
   ap_lat_us = -1
   in_pkg2 = False
   in_pkg3 = False
   pkg_prefix = ""
   if (tos == "BK"):
       pkg_prefix = "Background"
   elif (tos == "BE"):
       pkg_prefix = "Best"
   elif (tos == "VI"):
       pkg_prefix = "Video"
   elif (tos == "VO"):
       pkg_prefix = "Voice"

   for line in rslt.splitlines():
       if line.startswith("Pkg 2"):
           in_pkg2 = True
           in_pkg3 = False
       elif line.startswith("Pkg 3"):
           in_pkg3 = True
           in_pkg2 = False
       else:
           toks = line.split()
           if toks[0] == "1": # Something like: 1 Background  TX      11ax Good-RSSI 457013940       3683370
               us_idx = 6
               lat_idx = 4
               offset = 0
               if toks[1] == "Best":
                   # Tokenization is broken due to space, work-around
                   offset = 1

               if toks[1] == pkg_prefix:
                   if in_pkg2:
                       if toks[2 + offset] == "TX" and toks[3 + offset] == "11ax":
                           ap_at_us = int(toks[us_idx + offset])
                   elif in_pkg3:
                       ap_lat_us = int(toks[lat_idx + offset])
       
   if ap_at_us == -1:
       print("ERROR:  Could not find AP airtime, tos: %s  pkg_prefix: %s"%(tos, pkg_prefix))
       exit(1)

   if ap_lat_us == -1:
       print("ERROR:  Could not find AP avg latency, tos: %s  pkg_prefix: %s"%(tos, pkg_prefix))
       exit(2)

   file1 = open('TOS_PLUS.sh', 'r') 
   lines = file1.readlines()


   csv_file = ""
   capture_dir = ""
   # Strips the newline character 
   for line in lines:
       tok_val = line.split("=", 1)
       if tok_val[0] == "CAPTURE_DIR":
           capture_dir = tok_val[1]
       elif tok_val[0] == "CSV_FILE":
           capture_dir = tok_val[1]

   # Remove  third-party tool's tmp file tmp file
   os.unlink("stormbreaker.log")

   # Run third-party tool to process the capture files.
   os.system('python3 sb -p %s -subdir %s'%(ptype, capture_dir))
  
   # Print out one-way latency reported by LANforge
   file2 = open(csv_file, 'r')
   lines = file2.readlines()

   avglat = 0  # Assumes single connection
   # Strips the newline character 
   for line in lines:
       cols = line.split("\t")
       # Print out endp-name and avg latency
       print("%s\t%s"%(cols[1], cols[15]))
       if cols[1].endswith("-A"):
           avglat = cols[15]

   # Compare pcap csv data
   file3 = open("airtime.csv", 'r')
   lines = file3.readlines()

   at_row = []
   # Strips the newline character 
   for line in lines:
       cols = line.split(",")
       if cols[0].endswith(tos):
           at_row = line.split(",")
           break

   #at_row holds air-time fairness csv row created by pcap analyzer
   #avglat is AVG one-way download latency reported by LANforge
   #ap_at_lat is airtime in usec reported by AP for the specified type-of-service
   #ap_lat_us is latency in usec reported by AP for the specified type-of-service

   # Check latency
   avglat *= 1000  # Convert LF latency to usec
   latdiff = abs(avglat - ap_lat_us)
   if latdiff <= 2000:
       # Assume 2ms is close enough
       print("AVG-LAT:  PASSED  ## Within 2ms, AP Reports: %ius  Candela reports: %ius"%(ap_at_lat, avglat))
   else:
       upper = ap_lat_us * 1.2
       lower = ap_lat_us * 0.8

       if avglat >= lower and avglat <= upper:
            print("AVG-LAT:  PASSED  ## Within +-20%, AP Reports: %ius  LANforge reports: %ius"%(ap_at_lat, avglat))
       else:
           print("AVG-LAT:  FAILED  ## AP Reports: %ius  LANforge reports: %ius"%(ap_at_lat, avglat))

   # Check Airtime
   # TODO:  Not sure what at_row column(s) to compare


   #Clear config on WLAN
   subprocess.run(["./wifi_ctl_9800_3504.py", "-d", dest, "-o", port, "-s", "telnet", "-l", "stdout", "-a", ap, "-u", "cisco", "-p", "Cisco123", "-w", wlan, "-i", wlanID,
                  "--action", "delete_wlan"], capture_output=True)
     #subprocess.run("python3 wifi_ctl_9800_3504.py -d %s  -o %s -s telnet -l stdout -a %s -u %s -p %s -w wlan_open -i 6 --action delete_wlan"%(dest, port, ap, user, passwd))

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
if __name__ == '__main__':
    main()

####
####
####
