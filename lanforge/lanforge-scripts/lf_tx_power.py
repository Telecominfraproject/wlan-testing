#!/usr/bin/python3
'''
LANforge 192.168.100.178
Controller at 192.168.100.112 admin/Cisco123
Controller is 192.1.0.10
AP is 192.1.0.2'''

EPILOG = '''\

##############################################################################################
# Support History 
##############################################################################################    

##############################################################################
Sample script to run create station, wlan and talk to ap 1/26/2021 run on 9800
carriage returns specifically left out
##############################################################################
./lf_tx_power.py -d 172.19.27.55 -u admin -p Wnbulab@123 --port 2013 --scheme telnet --ap 9120_Candela --bandwidth "20" --channel "52 100 104" --nss 4 --txpower "1" --pathloss 56 --antenna_gain 6 --band a --upstream_port eth2 --series 9800 --radio wiphy5 --slot 1 --ssid open-wlan --prompt "katar_candela" --create_station sta0001 --ssidpw [BLANK] --security open --verbose  --wlan open-wlan --wlanID 1 --wlanSSID open-wlan --ap_info "ap_scheme==telnet ap_prompt==9120_Candela ap_ip==172.19.27.55 ap_port==2008 ap_user==admin ap_pw==Wnbulab@123"



#############################################################
Sample to test pf_ignore_offset switch 1/27/2021 run on 9800
carriage returns specifically left out
#############################################################
./lf_tx_power.py -d 172.19.27.55 -u admin -p Wnbulab@123 --port 2013 --scheme telnet --ap 9120_Candela --bandwidth "20" --channel "36 52 100 104 161" --nss 4 --txpower "1" --pathloss 56 --antenna_gain 6 --band a --upstream_port eth2 --series 9800 --radio wiphy5 --slot 1 --ssid open-wlan --prompt "katar_candela" --create_station sta0001 --ssidpw [BLANK] --security open --verbose  --wlan open-wlan --wlanID 1 --wlanSSID open-wlan --pf_ignore_offset "35"


##############################################################################################
##############################################################################################

make sure pexpect is installed:
$ sudo yum install python3-pexpect
$ sudo yum install python3-xlsxwriter

You might need to install pexpect-serial using pip: 
$ pip3 install pexpect-serial 
$ pip3 install XlsxWriter 

This script will automatically create and start a layer-3 UDP connection between the
configured upstream port and station.

The user also has the option of setting up the station oustide of this script, however.

# Examples:
# See cisco_power_results.txt when complete.
# See cisco_power_results.xlsx when complete.
NOTE:  Telnet port 23 unless specified ,  ssh  port 22 unless specified,  scheme defaults to ssh


##############################################################################################
# read AP for powercfg values using : show controllers dot11Radio 1 powercfg | g T1'
##############################################################################################

./lf_tx_power.py -d 172.19.27.55 -u admin -p Wnbulab@123 --port 2013 --scheme telnet \
    --ap 9120_Candela --bandwidth "20" --channel "149" --nss 4 --txpower "1" \
    --pathloss 56 --band a --upstream_port eth2 --series 9800 --radio wiphy5 --slot 1 --ssid open-wlan \
    --prompt "katar_candela" --create_station sta0001 --ssidpw [BLANK] --security open --verbose \
    --antenna_gain "6" --wlanID 1 --wlan open-wlan --wlanSSID open-wlan\
    --ap_info "ap_scheme==telnet ap_prompt==9120_Candela ap_ip==172.19.27.55 ap_port==2008 ap_user==admin ap_pw==Wnbulab@123"


##############################################################################################
# send email and or text on --exit_on_fail
##############################################################################################

./lf_tx_power.py -d 192.168.100.112 -u admin -p Cisco123 -s ssh --port 22 -a APA453.0E7B.CF9C --lfmgr 192.168.100.178 \
    --bandwidth "80" --channel "144" --nss 4 --txpower "1" --pathloss 51 --antenna_gain 10 --lfmgr 192.168.100.178 --band a \
    --upstream_port eth3 --outfile cisco_power_results --create_station sta0001 --radio wiphy1 --ssid test_candela --ssidpw [BLANK] \
    --security open -l out_file2  -D 14 --exit_on_fail \
    --email "user==lanforgetest@gmail.com passwd==lanforge123 to==2082868321@vtext.com smtp==smtp.gmail.com port==465"\
    --email "user==lanforgetest@gmail.com passwd==lanforge123 to==lanforgetest@gmail.com  smtp==smtp.gmail.com port==465"\
    --series "3504" --prompt "(Cisco Controler)"

##############################################################################################
# Long duration test -- need to create the ---wlanID 1 --wlan open-wlan --wlanSSID open-wlan 
##############################################################################################

./lf_tx_power.py -d 172.19.36.168 -u admin -p Wnbulab@123 --port 23 --scheme telnet --ap "APA453.0E7B.CF60" \ 
    --bandwidth "20 40 80" --channel "36 40 44 48 52 56 60 64 100 104 108 112 116 120 124 128 132 136 140 144 149 153 157 161 165" \
    --nss 4 --txpower "1 2 3 4 5 6 7 8" --pathloss 54 --antenna_gain 6 --band a --upstream_port eth2 --series 9800  \
    --wlanID 1 --wlan open-wlan --wlanSSID open-wlan --create_station sta0001 --radio wiphy1 --ssid  open-wlan --ssidpw [BLANK] --security open \
    --outfile cisco_power_results_60_chan_ALL  --cleanup --slot 1 --verbose


##############################################################################################
# Per-channel path-loss example station present
##############################################################################################

./lf_tx_power.py -d 192.168.100.112 -u admin -p Cisco123 -s ssh --port 22 -a VC --lfmgr 192.168.100.178 \
  --station sta00000 --bandwidth "20 40 80 160" --channel "36:64 149:60" --antenna_gain 5 --nss 4 --txpower "1 2 3 4 5 6 7 8" --pathloss 64 \
  --band a --upstream_port eth2 --lfresource2 2 --verbose

##############################################################################################
# To create a station run test against station create open-wlan
##############################################################################################

./lf_tx_power.py -d <router IP> -u admin -p Cisco123 -port 23 --scheme telnet --ap AP6C71.0DE6.45D0 \
--station sta2222 --bandwidth "20" --channel "36" --nss 4 --txpower "1 2 3 4 5 6 7 8" --pathloss 54 --antenna_gain 6 --band a \
--upstream_port eth2 --series 9800 --wlanID 1 --wlan open-wlan --wlanSSID open-wlan --create_station sta2222 --radio wiphy1 --ssid open-wlan \
--ssidpw [BLANK] --security open --verbose

##############################################################################################
# station already present
##############################################################################################

./lf_tx_power.py -d <router IP> -u admin -p Cisco123 -port 23 --scheme telnet --ap AP6C71.0DE6.45D0 \
--station sta0000 --bandwidth "20" --channel "36" --nss 4 --txpower "1 2 3 4 5 6 7 8" --pathloss 64 --antenna_gain 5 --band a \
--upstream_port eth2 --series 9800 --wlanID 1 --wlan open-wlan --wlanSSID open-wlan --verbose


##############################################################################################
# to create a station 
##############################################################################################

./lf_associate_ap.pl --radio wiphy1 --ssid open-wlan --passphrase [BLANK] ssecurity open --upstream eth1 \
--first_ip DHCP --first_sta sta0001 --duration 5 --cxtype udp

Changing regulatory domain should happen outside of this script.  

##############################################################################################
# If wish to send Text after test completion follow the email format based on carrier
##############################################################################################
Text message via email:

T-Mobile – number@tmomail.net
Virgin Mobile – number@vmobl.com
AT&T – number@txt.att.net
Sprint – number@messaging.sprintpcs.com
Verizon – number@vtext.com
Tracfone – number@mmst5.tracfone.com
Ting – number@message.ting.com
Boost Mobile – number@myboostmobile.com
U.S. Cellular – number@email.uscc.net
Metro PCS – number@mymetropcs.com

##############################################################################################
# OUTPUT in XLSX file - Spread sheet how values determined
##############################################################################################

Tx Power                             : Input from command line (1-8)
Allowed Per Path                     : Read from the Controller
Cabling Pathloss                     : Input from command line, best if verified prior to testing
Antenna Gain                         : Input from command line, if AP cannot detect antenna connection
Beacon RSSI (beacon_sig)             : From Lanforge probe, command ./lf_portmod.pl with cli parameter probe_port 1 (~line 1183, ~line 1209)
Combined RSSI User (sig)             : From Lanforge probe, command ./lf_portmod.pl with cli parameter probe_port 1 (~line 1183, ~line 1193)
RSSI 1, RSSI 2, RSSI 3, RSSI 4       : (~line 1160)
    ants[q] (antX) read from Lanforge probe, command ./lf_portmod.pl with cli parameter probe_port 1

Ant 1, Ant 2, Ant 3, Ant 4 : ()
    Starting Value for antX read from lanforge probe, using command ./lf_portmod.pl with cli parameter porbe_port 1

    _noise_bear (_noise_i) = from Lanforge returning NOISE from command (!line 1070) lf_portmod.pl reading --show_port 
    "AP, IP, Mode, NSS, Bandwith, Channel, Signal, NOISE, Status, RX-Rate

    rssi_adj (only used if --adjust_nf and _noise_bare != None) (~line 1263)  _noise_i(_noise_bear) - nf_at_calibration (fixed value of -105)

    Thus calc_antX =  int(antX read from Lanforge) + pi (path loss from command line) + rssi_adj + ag (antenna gain from command line)

    calc_antX is put on the spread sheet under Ant X

Offset 1, Offset 2, Offset 3, Offset 4: which in the code is diff_aX = calc_antX - allowed_per_path (adjusted based on number of streams)

Pass/Fail : (~line 1286) If the diff / offset is greater than the pfrange determins the pass or fail

'''

import sys
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

import re
import logging
import time
from time import sleep
import argparse
import subprocess
import xlsxwriter
import math

NL = "\n"
CR = "\r\n"
Q = '"'
A = "'"
FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'

lfmgr = "127.0.0.1"
lfstation = "sta00000"
lfresource = "1"
lfresource2 = "1"
outfile = "cisco_power_results.txt"
full_outfile = "cisco_power_results_full.txt"
outfile_xlsx = "cisco_power_results.xlsx"
upstream_port = "eth1"
pf_dbm = 6

# Allow one chain to have a lower signal, since customer's DUT has
# lower tx-power on one chain when doing high MCS at 4x4.
pf_ignore_offset = 0

# Threshold for allowing a pass
failed_low_threshold = 0

# This below is only used when --adjust_nf is used.
# Noise floor on ch 36 where we calibrated -54 path loss (based on hard-coded -95 noise-floor in driver)
nf_at_calibration = -105
# older ath10k driver hard-codes noise-floor to -95 when calculating RSSI
# RSSI = NF + reported_power
# Shift RSSI by difference in actual vs calibrated noise-floor since driver hard-codes
# the noise floor.

# rssi_adjust = (current_nf - nf_at_calibration)

def usage():
   print("############  USAGE ############")
   print("-d|--dest:  destination host, address of the controller")
   print("-o|--port:  destination port, default = 23")
   print("-u|--user:  login name or username")
   print("-p|--passwd:  password")
   print("-s|--scheme (serial|telnet|ssh): connect via serial, ssh or telnet")
   print("-t|--tty tty serial device")
   print("-l|--log <store true> log has same namelog messages here ,stdout means output to console, default stdout")
   print("-a|--ap select AP")
   print("-b|--bandwidth: List of bandwidths to test: 20 40 80 160, NA means no change, 160 can only do 2x2 spatial streams due to radio limitations")
   print("-c|--channel: List of channels, with optional path-loss to test: 36:64 100:60 , NA means no change")
   print("-n|--nss: List of spatial streams to test: 1x1 2x2 3x3 4x4, NA means no change")
   print("-T|--txpower: List of TX power values to test: 1 2 3 4 5 6 7 8, NA means no change, 1 is highest power, the power is halved for each subsquent setting")
   print("-k|--keep_state <store true>  keep the state, no configuration change at the end of the test, store true flage present ")
   print("--station: LANforge station name for test(sta0000), use if station present and --create_station not used")
   print("--upstream_port: LANforge upstream port name (eth1)")
   print("--lfmgr: LANforge manager IP address")
   print("--lfresource: LANforge resource ID for station")
   print("--lfresource2: LANforge resource ID for upstream port")
   print("--outfile: Output file for txt and xlsx data, default cisco_power_results")
   print("--pathloss:  Calculated path-loss between LANforge station and AP")
   print("--antenna_gain: Antenna gain for AP, if no Antenna attached then antenna gain needs to be taken into account, default 0")
   print("--band:  Select band (a | b | abgn), a means 5Ghz, b means 2.4, abgn means 2.4 on dual-band AP, default a")
   print("--pf_dbm: Pass/Fail range, default is 6")
   print("--pf_ignore_offset: Allow one chain to use lower tx-power and still pass when doing 4x4, default 100. so disabled")
   print("--wait_forever: <store true> Wait forever for station to associate, may aid debugging if STA cannot associate properly")
   print("--adjust_nf: <store true> Adjust RSSI based on noise-floor.  ath10k without the use-real-noise-floor fix needs this option")
   print("--wlan: for 9800, wlan identifier ")
   print("--wlanID: wlanID  for 9800 , defaults to 1")
   print("--wlanSSID: wlanSSID  for 9800")
   print("--series: controller series  9800 , defaults to 3504")
   print("--slot: 9800 AP slot defaults to 1")
   print("--create_station", "create LANforge station at the beginning of the test")
   print("--radio" ,"radio to create LANforge station on at the beginning of the test")
   print("--ssid", "ssid default open-wlan")
   print("--ssidpw", "ssidpw default [BLANK]")
   print("--security", "security default open")
   print("--cleanup", "<store true> Clean up all stations after test completes, only need switch for True, Defaults False")
   print("--vht160", "<store true> Enables VHT160 in lanforge, only need switch for True, Defaults False")
   print("--verbose","<store ture> switch the cisco controller output will be captured")
   print("--exit_on_fail","--exit_on_fail,  exit on test failure")
   print("--exit_on_error","--exit_on_error, exit on test error, test mechanics failed")
   print('-e','--email', "--email user==<from email> passwd==<email password> to==<to email> smtp==<smtp server> port==<smtp port> 465 (SSL)")
   print('-ccp','--prompt', "--prompt controller prompt default WLC")
   print('--beacon_dbm_diff', "--beacon_dbm_diff <value>  is the delta that is allowed between the controller tx and the beacon measured")
   print('--show_lf_portmod',"<store_true> show the output of lf_portmod after traffic to verify RSSI values measured by lanforge")
   print('-api','--ap_info', "--ap_info ap_scheme==<telnet,ssh or serial> ap_prompt==<ap_prompt> ap_ip==<ap ip> ap_port==<ap port number> ap_user==<ap user> ap_pw==<ap password>")



   print("-h|--help")

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

def exit_test(workbook):
   workbook.close()
   sleep(0.5)
   exit(1)


def main():
   global lfmgr
   global lfstation
   global lfresource
   global lfresource2
   global outfile
   global outfile_xlsx
   global full_outfile
   global upstream_port
   global pf_dbm
   global pf_ignore_offset
   global failed_low_threshold

   scheme = "ssh"

   parser = argparse.ArgumentParser(description="Cisco TX Power report Script",epilog=EPILOG,
      formatter_class=argparse.RawTextHelpFormatter)
   parser.add_argument("-d", "--dest",       type=str, help="address of the cisco controller",required=True)
   parser.add_argument("-o", "--port",       type=str, help="control port on the controller",required=True)
   parser.add_argument("-u", "--user",       type=str, help="credential login/username",required=True)
   parser.add_argument("-p", "--passwd",     type=str, help="credential password",required=True)
   parser.add_argument("-s", "--scheme",     type=str, choices=["serial", "ssh", "telnet"], help="Connect via serial, ssh or telnet")
   parser.add_argument("-t", "--tty",        type=str, help="tty serial device")
   parser.add_argument("-l", "--log",        action='store_true', help="create logfile for messages, default stdout")
   parser.add_argument("-a", "--ap",         type=str, help="select AP")
   parser.add_argument("-b", "--bandwidth",  type=str, help="List of bandwidths to test. NA means no change")
   parser.add_argument("-c", "--channel",    type=str, help="List of channels to test, with optional path-loss, 36:64 149:60. NA means no change")
   parser.add_argument("-n", "--nss",        type=str, help="List of spatial streams to test.  NA means no change")
   parser.add_argument("-T", "--txpower",    type=str, help="List of txpowers to test.  NA means no change")
   parser.add_argument("-k","--keep_state",  action="store_true",help="keep the state, no configuration change at the end of the test")
   parser.add_argument('-D','--duration',    type=str, help='--traffic <how long to run in seconds>  example -t 20 (seconds) default: 20 ',default='20')
   parser.add_argument("--station",          type=str, help="LANforge station to use (sta0000, etc) use if station present and --create_station not used")
   parser.add_argument("--upstream_port",    type=str, help="LANforge upsteram-port to use (eth1, etc)")
   parser.add_argument("--lfmgr",            type=str, help="LANforge Manager IP address")
   parser.add_argument("--lfresource",       type=str, help="LANforge resource ID for the station")
   parser.add_argument("--lfresource2",      type=str, help="LANforge resource ID for the upstream port system")
   parser.add_argument("--outfile",          type=str, help="Output file for csv data",default="cisco_power_results")
   parser.add_argument("--pathloss",         type=str, help="Calculated pathloss between LANforge Station and AP")
   parser.add_argument("--antenna_gain",     type=str, help="Antenna gain,  take into account the gain due to the antenna",default="0")
   parser.add_argument("--band",             type=str, help="Select band (a | b), a means 5Ghz, b means 2.4Ghz.  Default is a",
                       choices=["a", "b", "abgn"])
   parser.add_argument("--pf_dbm",           type=str, help="Pass/Fail threshold.  Default is 6",default="6" )
   parser.add_argument("--pf_ignore_offset",    type=str, help="Allow a chain to have lower tx-power and still pass. default 0 so disabled",default="0")
   parser.add_argument("--wait_forever",     action='store_true', help="Wait forever for station to associate, may aid debugging if STA cannot associate properly")
   parser.add_argument("--adjust_nf",        action='store_true', help="Adjust RSSI based on noise-floor.  ath10k without the use-real-noise-floor fix needs this option")
   parser.add_argument("--wlan",             type=str, help="--wlan  9800, wlan identifier",required=True)
   parser.add_argument("--wlanID",           type=str, help="--wlanID  9800 , defaults to 1",default="1",required=True)
   parser.add_argument("--wlanSSID",         type=str, help="--wlan  9800, wlan SSID, this must match the -ssid , ssid for station",required=True)
   parser.add_argument("--series",           type=str, help="--series  9800 or 3504, defaults to 9800",default="9800")
   parser.add_argument("--slot",             type=str, help="--slot 1 , 9800 AP slot defaults to 1",default="1")
   parser.add_argument("--create_station",   type=str, help="create LANforge station at the beginning of the test")
   parser.add_argument("--radio",            type=str, help="radio to create LANforge station on at the beginning of the test")
   parser.add_argument("--ssid",             type=str, help="ssid, this must patch the wlan",required=True)
   parser.add_argument("--ssidpw",           type=str, help="ssidpw",required=True)
   parser.add_argument("--security",         type=str, help="security",required=True)
   parser.add_argument("--cleanup",          action='store_true',help="--cleanup , Clean up stations after test completes ")
   parser.add_argument("--vht160",           action='store_true',help="--vht160 , Enable VHT160 in lanforge ")
   parser.add_argument('--verbose',          action='store_true',help='--verbose , switch the cisco controller output will be captured')
   parser.add_argument("--exit_on_fail",     action='store_true',help="--exit_on_fail,  exit on test failure")
   parser.add_argument("--exit_on_error",    action='store_true',help="--exit_on_error, exit on test error, test mechanics failed")
   parser.add_argument('-e','--email',       action='append', nargs=1, type=str, help="--email user==<from email> passwd==<email password> to==<to email> smtp==<smtp server> port==<smtp port> 465 (SSL)")
   parser.add_argument('-ccp','--prompt',    type=str,help="controller prompt",required=True)
   parser.add_argument('--beacon_dbm_diff',  type=str,help="--beacon_dbm_diff <value>  is the delta that is allowed between the controller tx and the beacon measured",default="7")
   parser.add_argument('--show_lf_portmod',  action='store_true',help="--show_lf_portmod,  show the output of lf_portmod after traffic to verify RSSI values measured by lanforge")
   parser.add_argument('-api','--ap_info',   action='append', nargs=1, type=str, help="--ap_info ap_scheme==<telnet,ssh or serial> ap_prompt==<ap_prompt> ap_ip==<ap ip> ap_port==<ap port number> ap_user==<ap user> ap_pw==<ap password>")


   #current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "{:.3f}".format(time.time() - (math.floor(time.time())))[1:]  
   #print(current_time)
   #usage()
   args = None
   try:
      # Parcing the input parameters and assignment
      args = parser.parse_args()
      if (args.scheme != None):
         scheme = args.scheme
      #logfile = args.log
      if (args.station != None):
          lfstation = args.station
      if (args.create_station != None):
          lfstation = args.create_station
          if (args.station != None):
              print("NOTE: both station: {} and create_station: {} on command line, test will use create_station {} ".format(args.station, args.create_station, args.create_station))
      if (args.upstream_port != None):
          upstream_port = args.upstream_port
      if (args.lfmgr != None):
          lfmgr = args.lfmgr
      if (args.lfresource != None):
          lfresource = args.lfresource
      if (args.lfresource2 != None):
          lfresource2 = args.lfresource2
      if (args.outfile != None):
          outfile = args.outfile
          full_outfile = "full-%s"%(outfile)
          outfile_xlsx = "%s.xlsx"%(outfile)
      if (args.band != None):
          band = args.band
      else:
          band = "a"
      if (args.pf_dbm != None):
          pf_dbm = int(args.pf_dbm)
      if (args.pf_ignore_offset != None):
          pf_ignore_offset = int(args.pf_ignore_offset)
      if (args.verbose):
          # capture the controller output , thus won't go to stdout some output always present
          cap_ctl_out = False
      else:
          cap_ctl_out = True 
      if (args.wlanSSID != args.ssid):
          print("####### ERROR ################################")
          print("wlanSSID: {} must equial the station ssid: {}".format(args.wlanSSID,args.ssid))
          print("####### ERROR ################################")
          exit(1)                      
      # note: there would always be an args.outfile due to the default
      current_time = time.strftime("%m_%d_%Y_%H_%M_%S", time.localtime())
      outfile = "{}_{}.txt".format(args.outfile,current_time)
      full_outfile = "{}_full_{}.txt".format(args.outfile,current_time)
      outfile_xlsx = "{}_{}.xlsx".format(args.outfile,current_time)
      print("output file: {}".format(outfile))
      print("output file full: {}".format(full_outfile))
      print("output file xlsx: {}".format(outfile_xlsx))
      if args.log:
        outfile_log = "{}_{}_output_log.log".format(args.outfile,current_time)
        print("output file log: {}".format(outfile_log))

      ap_dict = []
      if args.ap_info:
          ap_info = args.ap_info
          for _ap_info in ap_info:
              print("ap_info {}".format(_ap_info))
              ap_keys = ['ap_scheme','ap_prompt','ap_ip','ap_port','ap_user','ap_pw']
              ap_dict = dict(map(lambda x: x.split('=='), str(_ap_info).replace('[','').replace(']','').replace("'","").split()))
              for key in ap_keys:
                    if key not in ap_dict:
                        print("missing ap config, for the {}, all these need to be set {} ".format(key,ap_keys))
                        exit(1)
              print("ap_dict: {}".format(ap_dict))

      email_dicts = []
      if args.email:
        emails = args.email
        for _email in emails:
           #print("email {}".format(_email))
           email_keys = ['user','passwd','to','smtp','port']
           _email_dict = dict(map(lambda x: x.split('=='), str(_email).replace('[','').replace(']','').replace("'","").split()))
           #print("email_dict {}".format(_email_dict))
           for key in email_keys:
              if key not in _email_dict:
                print("missing config, for the {}, all of the following need to be present {} ".format(key,email_keys))
                exit(1)
           email_dicts.append(_email_dict)
           print("email_dicts: {}".format(email_dicts))    
        
   except Exception as e:
      logging.exception(e)
      usage()
      exit(2)

   
   console_handler = logging.StreamHandler()
   formatter = logging.Formatter(FORMAT)
   logg = logging.getLogger(__name__)
   logg.setLevel(logging.DEBUG)

   file_handler = None
   # Setting up log file if specified
   if args.log:
       file_handler = logging.FileHandler(outfile_log, "w")
       file_handler.setLevel(logging.DEBUG)
       file_handler.setFormatter(formatter)
       logg.addHandler(file_handler)
       logg.addHandler(logging.StreamHandler(sys.stdout)) # allows to logging to file and stderr
       #logging.basicConfig(format=FORMAT, handlers=[console_handler])

   else:
       #pass
       # stdout logging
       logging.basicConfig(format=FORMAT, handlers=[console_handler])
       #logg.addHandler(logging.StreamHandler()) # allows to logging to file and stderr

   if bool(ap_dict):
       logg.info("ap_dict {}".format(ap_dict))

   if bool(email_dicts):
       logg.info("email_dicts {}".format(email_dicts))

   if args.outfile != None:
       logg.info("output file: {}".format(outfile))
       logg.info("output file full: {}".format(full_outfile))
       logg.info("output file xlsx: {}".format(outfile_xlsx))

   if args.log:
       logg.info("output file log: {}".format(outfile_log))


   if (args.bandwidth == None):
       usage()
       logg.info("ERROR:  Must specify bandwidths")
       exit(1)

   if (args.channel == None):
       usage()
       logg.info("ERROR:  Must specify channels")
       exit(1)

   if (args.nss == None):
       usage()
       logg.info("ERROR:  Must specify NSS")
       exit(1)

   if (args.txpower == None):
       usage()
       logg.info("ERROR:  Must specify txpower")
       exit(1)

   if (args.pathloss == None):
       logg.info("ERROR:  Pathloss must be specified.")
       exit(1)

   if (args.antenna_gain == None):
       usage()
       logg.info("ERROR: Antenna gain must be specified.")
       exit(1)

   # Full spread-sheet data
   csv = open(full_outfile, "w")
   csv.write("Regulatory Domain\tCabling Pathloss\tAntenna Gain\tCfg-Channel\tCfg-NSS\tCfg-AP-BW\tTx Power\tBeacon-Signal\tCombined-Signal\tRSSI 1\tRSSI 2\tRSSI 3\tRSSI 4\tAP-BSSID\tRpt-BW\tRpt-Channel\tRpt-Mode\tRpt-NSS\tRpt-Noise\tRpt-Rxrate\tCtrl-AP-MAC\tCtrl-Channel\tCtrl-Power\tCtrl-dBm\tCalc-dBm-Combined\tDiff-dBm-Combined\tAnt-1\tAnt-2\tAnt-3\tAnt-4\tOffset-1\tOffset-2\tOffset-3\tOffset-4\tPASS/FAIL(+-%sdB)\tTimeStamp\tWarnings-and-Errors"%(pf_dbm))
   csv.write("\n");
   csv.flush()

   # Summary spread-sheet data
   csvs = open(outfile, "w")
   csvs.write("Regulatory Domain\tCabling Pathloss\tAntenna Gain\tAP Channel\tNSS\tAP BW\tTx Power\tAllowed Per-Path\tRSSI 1\tRSSI 2\tRSSI 3\tRSSI 4\tAnt-1\tAnt-2\tAnt-3\tAnt-4\tOffset-1\tOffset-2\tOffset-3\tOffset-4\tPASS/FAIL(+-%sdB)\tTimeStamp\tWarnings-and-Errors"%(pf_dbm))
   csvs.write("\n");
   csvs.flush()

   # XLSX file
   workbook = xlsxwriter.Workbook(outfile_xlsx)
   worksheet = workbook.add_worksheet()

   #bold = workbook.add_format({'bold': True, 'align': 'center'})
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
   #center = workbook.add_format({'align': 'center'})
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
   orange_left = workbook.add_format({'color': 'orange', 'align': 'left'})
   orange_left.set_bg_color("#e0efda")
   orange_left.set_border(1)


   worksheet.set_row(0, 45) # Set height
   worksheet.set_column(0, 0, 10) # Set width

   col = 0
   row = 0
   worksheet.write(row, col, 'Regulatory\nDomain', dblue_bold); col += 1
   worksheet.set_column(col, col, 10) # Set width
   worksheet.write(row, col, 'Controller', dblue_bold); col += 1
   worksheet.set_column(col, col, 12) # Set width
   worksheet.write(row, col, 'Controller\nChannel', dblue_bold); col += 1
   worksheet.write(row, col, 'AP\nChannel', dblue_bold); col += 1
   worksheet.write(row, col, 'NSS', dblue_bold); col += 1
   worksheet.set_column(col, col, 10) # Set width
   worksheet.write(row, col, 'Controller\nBW', dblue_bold); col += 1
   worksheet.write(row, col, 'STA\nRpt\nBW', dblue_bold); col += 1
   worksheet.write(row, col, 'Tx\nPower', dtan_bold); col += 1
   worksheet.write(row, col, 'Allowed\nPer\nPath', dtan_bold); col += 1
   worksheet.write(row, col, 'Cabling\nPathloss', dtan_bold); col += 1
   worksheet.write(row, col, 'Antenna\nGain', dtan_bold); col += 1
   worksheet.write(row, col, 'Noise\n', dpeach_bold); col += 1
   if (args.adjust_nf):
       worksheet.write(row, col, 'Noise\nAdjust\n(vs -105)', dpeach_bold); col += 1

   worksheet.set_column(col, col, 15) # Set width
   worksheet.write(row, col, 'Last\nMCS\n', dpeach_bold); col += 1
   worksheet.set_column(col, col, 10) # Set width
   worksheet.write(row, col, 'Beacon\nRSSI\n', dpeach_bold); col += 1
   worksheet.set_column(col, col, 10) # Set width
   worksheet.write(row, col, 'Combined\nRSSI\n', dpeach_bold); col += 1
   worksheet.write(row, col, 'RSSI\n1', dpeach_bold); col += 1
   worksheet.write(row, col, 'RSSI\n2', dpeach_bold); col += 1
   worksheet.write(row, col, 'RSSI\n3', dpeach_bold); col += 1
   worksheet.write(row, col, 'RSSI\n4', dpeach_bold); col += 1
   worksheet.write(row, col, 'Ant\n1', dpink_bold); col += 1
   worksheet.write(row, col, 'Ant\n2', dpink_bold); col += 1
   worksheet.write(row, col, 'Ant\n3', dpink_bold); col += 1
   worksheet.write(row, col, 'Ant\n4', dpink_bold); col += 1
   worksheet.write(row, col, 'Offset\n1', dyel_bold); col += 1
   worksheet.write(row, col, 'Offset\n2', dyel_bold); col += 1
   worksheet.write(row, col, 'Offset\n3', dyel_bold); col += 1
   worksheet.write(row, col, 'Offset\n4', dyel_bold); col += 1
   worksheet.set_column(col, col, 10) # Set width
   worksheet.write(row, col, 'Controller\n dBm', dblue_bold); col += 1
   worksheet.set_column(col, col, 10) # Set width
   worksheet.write(row, col, 'Calculated\n dBm\n Beacon', dblue_bold); col += 1
   worksheet.set_column(col, col, 18) # Set width
   worksheet.write(row, col, 'Diff Controller dBm\n & Beacon dBm \n (+/- {} dBm)'.format(args.beacon_dbm_diff), dblue_bold); col += 1
   worksheet.set_column(col, col, 14) # Set width
   worksheet.write(row, col, 'Calculated\n dBm\n Combined', dblue_bold); col += 1
   worksheet.set_column(col, col, 14) # Set width
   worksheet.write(row, col, 'Diff\nController dBm\n & Combined', dblue_bold); col += 1
   worksheet.set_column(col, col, 12) # Set width
   worksheet.write(row, col, "PASS /\nFAIL\n( += %s dBm)"%(pf_dbm), dgreen_bold); col += 1
   worksheet.set_column(col, col, 24) # Set width
   worksheet.write(row, col, 'Time Stamp\n', dgreen_bold); col += 1
   worksheet.set_column(col, col, 100) # Set width
   worksheet.write(row, col, 'Information, Warnings, Errors', dgreen_bold_left); col += 1
   row += 1

   bandwidths = args.bandwidth.split()
   channels = args.channel.split()
   nss = args.nss.split()
   txpowers = args.txpower.split()
       
   # The script has the ability to create a station if one does not exist     
   if (args.create_station != None):
       if (args.radio == None):
           logg.info("WARNING --create needs a radio")
           exit_test(workbook)
       elif (args.vht160):
           logg.info("creating station with VHT160 set: {} on radio {}".format(args.create_station,args.radio))
           subprocess.run(["./lf_associate_ap.pl", "--radio", args.radio, "--ssid", args.ssid , "--passphrase", args.ssidpw,
                   "--security", args.security, "--upstream", args.upstream_port, "--first_ip", "DHCP",
                   "--first_sta",args.create_station,"--action","add","--xsec","ht160_enable"], timeout=20, capture_output=True)
           sleep(3)
       else:    
           logg.info("creating station: {} on radio {}".format(args.create_station,args.radio))
           subprocess.run(["./lf_associate_ap.pl", "--radio", args.radio, "--ssid", args.ssid , "--passphrase", args.ssidpw,
                   "--security", args.security, "--upstream", args.upstream_port, "--first_ip", "DHCP",
                   "--first_sta",args.create_station,"--action","add"], timeout=20, capture_output=True)
           sleep(3)


   # Find LANforge station parent radio
   parent = None
   port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  lfresource, "--port_name", lfstation,
                                "--show_port", "Parent/Peer"], capture_output=True);
   pss = port_stats.stdout.decode('utf-8', 'ignore');
   for line in pss.splitlines():
       m = re.search('Parent/Peer:\s+(.*)', line)
       if (m != None):
           parent = m.group(1)


   # Create downstream connection
   # First, delete any old one
   subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  lfresource, "--action", "do_cmd",
                   "--cmd", "rm_cx all c-udp-power"], capture_output=True);
   subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  lfresource, "--action", "do_cmd",
                   "--cmd", "rm_endp c-udp-power-A"], capture_output=True);
   subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  lfresource2, "--action", "do_cmd",
                   "--cmd", "rm_endp c-udp-power-B"], capture_output=True);

   # Now, create the new connection
   subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  lfresource, "--action", "create_endp", "--port_name", lfstation,
                   "--endp_type", "lf_udp", "--endp_name", "c-udp-power-A", "--speed", "0", "--report_timer", "1000"], capture_output=True);
   subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  lfresource2, "--action", "create_endp", "--port_name", upstream_port,
                   "--endp_type", "lf_udp", "--endp_name", "c-udp-power-B", "--speed", "1000000", "--report_timer", "1000"], capture_output=True);
   subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  lfresource, "--action", "create_cx", "--cx_name", "c-udp-power",
                   "--cx_endps", "c-udp-power-A,c-udp-power-B", "--report_timer", "1000"], capture_output=True);

   myrd = ""
   # The script supports both the 9800 series controller and the 3504 series controller ,  the controllers have different interfaces
   if args.series == "9800": 

      try:
         logg.info("9800 wifi_ctl_9800_3504.py: no_logging_console")
         advanced = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                    "--action", "no_logging_console","--series",args.series,"--port",args.port,"--prompt",args.prompt], capture_output=True, check=True)
         pss = advanced.stdout.decode('utf-8', 'ignore');
         logg.info(pss)
      except subprocess.CalledProcessError as process_error:
         logg.info("####################################################################################################") 
         logg.info("# CHECK IF CONTROLLER HAS TELNET CONNECTION ALREADY ACTIVE") 
         logg.info("####################################################################################################") 

         logg.info("####################################################################################################") 
         logg.info("# Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
         logg.info("####################################################################################################") 
         exit_test(workbook)

      try:
         logg.info("9800 wifi_ctl_9800_3504.py: line_console_0")
         advanced = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                    "--action", "line_console_0","--series",args.series,"--port",args.port,"--prompt",args.prompt], capture_output=True, check=True)
         pss = advanced.stdout.decode('utf-8', 'ignore');
         logg.info(pss)
      except subprocess.CalledProcessError as process_error:
         logg.info("Controller unable to commicate to AP or unable to communicate to controller error code {}  output {}".format(process_error.returncode, process_error.output))
         exit_test(workbook)


   try:
      logg.info("9800/3504 wifi_ctl_9800_3504.py: summary")
      advanced = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                 "--action", "summary","--series",args.series,"--port",args.port,"--prompt",args.prompt], capture_output=True, check=True)
      pss = advanced.stdout.decode('utf-8', 'ignore');
      logg.info(pss)
   except subprocess.CalledProcessError as process_error:
      logg.info("Controller unable to commicate to AP or unable to communicate to controller error code {}  output {}".format(process_error.returncode, process_error.output))
      exit_test(workbook)
         
   # Find our current regulatory domain so we can report it properly
   searchap = False
   for line in pss.splitlines():
       if (line.startswith("---------")):
           searchap = True
           continue
       # the summaries are different between the 9800 series controller and the 3504 series
       # if the output changes then the following pattern/regular expression parcing needs to be changed
       # this site may help: https://regex101.com/  
       # when using https://regex101.com/ for tool beginning of string begins with ^
       if (searchap):
           if args.series == "9800":
               pat = "%s\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(\S+)"%(args.ap)
           else:
               pat = "%s\s+\S+\s+\S+\s+\S+\s+\S+.*  (\S+)\s+\S+\s*\S+\s+\["%(args.ap)
           m = re.search(pat, line)
           if (m != None):
               myrd = m.group(1)

   # Loop through all iterations and run txpower tests.
   # The is the main loop of loops:   Channels, spatial streams (nss), bandwidth (bw), txpowers (tx)
   # Note: supports 9800 and 3504 controllers
   wlan_created = False
   for ch in channels:
       pathloss = args.pathloss
       antenna_gain = args.antenna_gain
       ch_colon = ch.count(":")
       if (ch_colon == 1):
           cha = ch.split(":")
           pathloss = cha[1]
           ch = cha[0]
       for n in nss:
           for bw in bandwidths:
               if (n != "NA"):
                   ni = int(n)
                   if (parent == None):
                       logg.info("ERROR:  Skipping setting the spatial streams because cannot find Parent radio for station: %s."%(lfstation))
                   else:
                       # Set nss on LANforge Station, not sure it can be done on AP
                       if (bw == "160"):
                           # 9984 hardware needs 2 chains to do one NSS at 160Mhz
                           if (ni > 2):
                               if(args.vht160):
                                   ni = 2
                                   logg.info("NOTE: --vht160 set will set ni : {}".format(ni))
                                   # Set radio to 2x requested value
                                   ni *=2
                                   logg.info("NOTE: --vht160 set will set  ni * 2 : {}".format(ni))
                               else:    
                                   logg.info("NOTE: Skipping NSS %s for 160Mhz, LANforge radios do not support more than 2NSS at 160Mhz currently."%(n))
                                   logg.info("NOTE: use --vht160 to force 2NSS at 160Mhz")
                                   continue
                           else:
                               # Set radio to 2x requested value for 160Mhz
                               ni *= 2
                   antset = 0 # all available
                   if (ni == 1):
                       antset = 1
                   if (ni == 2):
                       antset = 4
                   if (ni == 3):
                       antset = 7
                   set_cmd = "set_wifi_radio 1 %s %s NA NA NA NA NA NA NA NA NA %s"%(lfresource, parent, antset)
                   logg.info("Setting LANforge radio to %s NSS with command: %s"%(ni, set_cmd))
                   subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  lfresource, "--port_name", parent,
                                   "--cli_cmd", set_cmd], capture_output=True)
               # tx power 1 is the highest power ,  2 power is 1/2 of 1 power etc till power 8 the lowest.
               for tx in txpowers:
                   # e_tot is the errors, w_tot is the warning, i_tot is information
                   e_tot = ""
                   w_tot = ""
                   i_tot = ""

                   # Stop traffic , if traffic was running ,  this is on the lanforge side.  Commands that start with lf_ are directed 
                   # towards the lanforge
                   subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  lfresource, "--action", "do_cmd",
                                   "--cmd", "set_cx_state all c-udp-power STOPPED"], capture_output=True);

                   # Down station
                   port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  lfresource, "--port_name", lfstation,
                                                "--set_ifstate", "down"]);
                   
                   # Disable AP, apply settings, enable AP
                   try:
                       logg.info("3504/9800 wifi_ctl_9800_3504.py: disable AP {}".format(args.ap))
                       ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                       "--action", "disable","--series",args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)
                       if cap_ctl_out:   
                          pss = ctl_output.stdout.decode('utf-8', 'ignore')
                          logg.info(pss) 
                   except subprocess.CalledProcessError as process_error:
                       logg.info("####################################################################################################") 
                       logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                       logg.info("####################################################################################################") 
                       logg.info("####################################################################################################") 
                       logg.info("#CHECK IF CONTROLLER HAS TELNET CONNECTION ALREADY ACTIVE") 
                       logg.info("####################################################################################################") 

                       exit_test(workbook)

                   if args.series == "9800": 
                       # 9800 series need to  "Configure radio for manual channel assignment"
                       logg.info("9800 Configure radio for manual channel assignment")

                       try:
                          logg.info("9800 wifi_ctl_9800_3504.py: disable_wlan")
                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                   "--action", "disable_wlan","--wlan", args.wlan, "--wlanID", args.wlanID, "--wlanSSID", args.wlanSSID, 
                                   "--series",args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)
                          if cap_ctl_out:   
                             pss = ctl_output.stdout.decode('utf-8', 'ignore')
                             logg.info(pss) 

                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                          exit_test(workbook)
                       try:
                          logg.info("9800 wifi_ctl_9800_3504.py: disable_network_5ghz")
                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                   "--action", "disable_network_5ghz","--series",args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)
                          if cap_ctl_out:   
                             pss = ctl_output.stdout.decode('utf-8', 'ignore')
                             logg.info(pss) 
                          
                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                          exit_test(workbook)

                       try:
                          logg.info("9800 wifi_ctl_9800_3504.py: disable_network_24ghz")
                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                   "--action", "disable_network_24ghz","--series",args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)
                          if cap_ctl_out:   
                             pss = ctl_output.stdout.decode('utf-8', 'ignore')
                             logg.info(pss) 
                                      
                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                          exit_test(workbook)

                       try:
                          logg.info("9800 wifi_ctl_9800_3504.py: manual")
                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                   "--action", "manual","--series",args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)
                          if cap_ctl_out:   
                             pss = ctl_output.stdout.decode('utf-8', 'ignore')
                             logg.info(pss) 

                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                          exit_test(workbook)
                   else:
                       try:
                          logg.info("3504 wifi_ctl_9800_3504.py: config 802.11a disable network")
                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                   "--action", "cmd", "--value", "config 802.11a disable network","--series",args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)
                          if cap_ctl_out:   
                             pss = ctl_output.stdout.decode('utf-8', 'ignore')
                             logg.info(pss) 

                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                          exit_test(workbook)
 
                       try:
                          logg.info("3504 wifi_ctl_9800_3504.py: config 802.11b disable network")
                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                   "--action", "cmd", "--value", "config 802.11b disable network","--series",args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)
                         
                          if cap_ctl_out:   
                             pss = ctl_output.stdout.decode('utf-8', 'ignore')
                             logg.info(pss) 

                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
                          exit_test(workbook) 

                   logg.info("9800/3504 test_parameters_summary: set : tx: {} ch: {} bw: {}".format(tx,ch,bw))
                   if (tx != "NA"):
                       logg.info("9800/3504 test_parameters: set txPower: {}".format(tx))
                       try:
                          logg.info("9800/3504 wifi_ctl_9800_3504.py: txPower {}".format(tx))
                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                       "--action", "txPower", "--value", tx, "--series" , args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)
                          if cap_ctl_out:   
                             pss = ctl_output.stdout.decode('utf-8', 'ignore')
                             logg.info(pss) 

                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                          exit_test(workbook)

                   if (bw != "NA"):
                       try:
                          logg.info("9800/3504 wifi_ctl_9800_3504.py: bandwidth 20 prior to setting channel, some channels only support 20")
                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                       "--action", "bandwidth", "--value", "20", "--series" , args.series,"--port", args.port,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True)
                          if cap_ctl_out:
                             pss = ctl_output.stdout.decode('utf-8', 'ignore')
                             logg.info(pss)
             
                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
                          exit_test(workbook)


                   # NSS is set on the station earlier...
                   if (ch != "NA"):
                       logg.info("9800/3504 test_parameters set channel: {}".format(ch))
                       try:
                          logg.info("9800/3504 wifi_ctl_9800_3504.py: channel {}".format(ch))
                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                       "--action", "channel", "--value", ch, "--series" , args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)
                          if cap_ctl_out:   
                             pss = ctl_output.stdout.decode('utf-8', 'ignore')
                             logg.info(pss) 

                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                          exit_test(workbook)

                   if (bw != "NA"):
                       logg.info("9800/3504 test_parameters bandwidth: set : {}".format(bw))
                       try:
                          logg.info("9800/3504 wifi_ctl_9800_3504.py: bandwidth {}".format(bw))
                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                       "--action", "bandwidth", "--value", bw, "--series" , args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)
                          if cap_ctl_out:   
                             pss = ctl_output.stdout.decode('utf-8', 'ignore')
                             logg.info(pss) 

                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
                          exit_test(workbook) 

                   # only create the wlan the first time  
                   if args.series == "9800":
                       if wlan_created:
                          logg.info("wlan already present, no need to create wlanID {} wlan {} wlanSSID {} port {}".format(args.wlanID, args.wlan, args.wlanSSID, args.port)) 
                          pass
                       else:
                          # Verify that a wlan does not exist on wlanID
                          # delete the wlan if already exists
                          try:
                             logg.info("9800 wifi_ctl_9800_3504.py: show_wlan_summary") 
                             wlan_info = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                                 "--action", "show_wlan_summary","--series" , args.series,"--port", args.port,"--prompt",args.prompt], capture_output=True, check=True)
                             pss = wlan_info.stdout.decode('utf-8', 'ignore')
                             logg.info(pss)
                          except subprocess.CalledProcessError as process_error:
                             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                             exit_test(workbook)

                          #  "number of WLANs:\s+(\S+)"   
                          search_wlan = False
                          for line in pss.splitlines():
                              logg.info(line)
                              if (line.startswith("---------")):
                                  search_wlan = True
                                  continue
                              if (search_wlan):
                                  pat = "{}\s+(\S+)\s+(\S+)".format(args.wlanID)
                                  m = re.search(pat, line)
                                  if (m != None):
                                      cc_wlan      = m.group(1)
                                      cc_wlan_ssid = m.group(2)
                                      # wlanID is in use
                                      logg.info("###############################################################################")
                                      logg.info("Need to remove wlanID: {} cc_wlan: {} cc_wlan_ssid: {}".format(args.wlanID, cc_wlan, cc_wlan_ssid))
                                      logg.info("###############################################################################")
                                      try:
                                          logg.info("9800 wifi_ctl_9800_3504.py: delete_wlan, wlan present at start of test: wlanID: {} cc_wlan {} cc_wlan_ssid: {}".format(args.wlanID, cc_wlan, cc_wlan_ssid))
                                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                                    "--action", "delete_wlan","--series",args.series, "--wlanID", args.wlanID, "--wlan", cc_wlan, "--wlanSSID", cc_wlan_ssid, 
                                                    "--port",args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)    
                                          if cap_ctl_out:
                                               pss = ctl_output.stdout.decode('utf-8', 'ignore')
                                               logg.info(pss)
   
                                      except subprocess.CalledProcessError as process_error:
                                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
                                          exit_test(workbook) 

                          # Create wlan  
                          wlan_created = True 
                          logg.info("create wlan {} wlanID {} port {}".format(args.wlan, args.wlanID, args.port)) 
                          try:
                              logg.info("9800 wifi_ctl_9800_3504.py: create_wlan wlan {} wlanID {} wlanSSID {} port {}".format(args.wlan, args.wlanID, args.wlanSSID, args.port))
                              ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                      "--action", "create_wlan","--series",args.series, "--wlanID", args.wlanID, "--wlan", args.wlan, "--wlanSSID", args.wlanSSID, "--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)    
                              if cap_ctl_out:   
                                 pss = ctl_output.stdout.decode('utf-8', 'ignore')
                                 logg.info(pss) 

                          except subprocess.CalledProcessError as process_error:
                             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                             exit_test(workbook)
   
                          try:
                              logg.info("9800 wifi_ctl_9800_3504.py: wireless_tag_policy")
                              ctl_output =subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                      "--action", "wireless_tag_policy","--series",args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True) 
                              if cap_ctl_out:   
                                 pss = ctl_output.stdout.decode('utf-8', 'ignore')
                                 logg.info(pss) 

                          except subprocess.CalledProcessError as process_error:
                             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                             exit_test(workbook)
                       try:
                          logg.info("9800 wifi_ctl_9800_3504.py: enable_wlan")
                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                   "--action", "enable_wlan", "--wlanID", args.wlanID, "--wlan", args.wlan, "--wlanSSID", args.wlanSSID, 
                                   "--series",args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)                 
                          if cap_ctl_out:   
                              pss = ctl_output.stdout.decode('utf-8', 'ignore')
                              logg.info(pss) 

                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                          exit_test(workbook)

                   # enable transmission for the entier 802.11z network
                   if args.series == "9800":
                       try:  
                          logg.info("9800 wifi_ctl_9800_3504.py: enable_network_5ghz")
                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                   "--action", "enable_network_5ghz","--series",args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)   
                          if cap_ctl_out:   
                            pss = ctl_output.stdout.decode('utf-8', 'ignore')
                            logg.info(pss) 

                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                          exit_test(workbook)

                       try:
                          logg.info("9800 wifi_ctl_9800_3504.py: enable_network_24ghz")
                          ctl_output =subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                   "--action", "enable_network_24ghz","--series",args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)                 
                          if cap_ctl_out:   
                              pss = ctl_output.stdout.decode('utf-8', 'ignore')
                              logg.info(pss) 

                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                          exit_test(workbook)
                   else:    
                       try:
                          logg.info("3504 wifi_ctl_9800_3504.py: config 802.11a enable network")
                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                   "--action", "cmd", "--value", "config 802.11a enable network","--port", args.port,"--series",args.series,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)
                          if cap_ctl_out:   
                              pss = ctl_output.stdout.decode('utf-8', 'ignore')
                              logg.info(pss) 

                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                          exit_test(workbook)

                       try:
                          logg.info("3504 wifi_ctl_9800_3504.py: config 802.11a enable network")
                          ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                   "--action", "cmd", "--value", "config 802.11b enable network","--port", args.port,"--series",args.series,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)
                          if cap_ctl_out:   
                              pss = ctl_output.stdout.decode('utf-8', 'ignore')
                              logg.info(pss) 

                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                          exit_test(workbook)

                   try: 
                      logg.info("9800/3504 wifi_ctl_9800_3504.py: enable")
                      ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                   "--action", "enable", "--series" , args.series,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)
                      if cap_ctl_out:   
                         pss = ctl_output.stdout.decode('utf-8', 'ignore')
                         logg.info(pss) 

                   except subprocess.CalledProcessError as process_error:
                      logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                      exit_test(workbook)

                   # Wait a bit for AP to come back up
                   time.sleep(3)
                   loop_count = 0
                   cc_dbm_rcv = False
                   if args.series == "9800":
                       while cc_dbm_rcv == False and loop_count <=3:
                          logg.info("9800 read controller dBm") 
                          loop_count +=1
                          time.sleep(1)
                          try:
                             logg.info("9800 wifi_ctl_9800_3504.py: advanced")
                             advanced = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                                 "--action", "advanced","--series" , args.series,"--port", args.port,"--prompt",args.prompt], capture_output=True, check=True)
                             pss = advanced.stdout.decode('utf-8', 'ignore')
                             logg.info(pss)
                          except subprocess.CalledProcessError as process_error:
                             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                             exit_test(workbook)
   
                          searchap = False
                          cc_mac = ""
                          cc_ch = ""
                          cc_bw = ""
                          cc_power = ""
                          cc_dbm = ""
                          for line in pss.splitlines():
                              if (line.startswith("---------")):
                                  searchap = True
                                  continue
                              # if the pattern changes save the output of the advanced command and re parse https://regex101.com
                              if (searchap):
                                  pat = "%s\s+(\S+)\s+(%s)\s+\S+\s+\S+\s+(\S+)\s+(\S+)\s+(\S+)\s+dBm\)+\s+(\S+)+\s"%(args.ap,args.slot)
                                  m = re.search(pat, line)
                                  if (m != None):
                                      if(m.group(2) == args.slot):
                                          cc_mac = m.group(1)
                                          cc_slot = m.group(2)
                                          cc_ch = m.group(6);  # (132,136,140,144)
                                          cc_power = m.group(4)
                                          cc_power = cc_power.replace("/", " of ") # spread-sheets turn 1/8 into a date
                                          cc_dbm = m.group(5)
                                          cc_dbm = cc_dbm.replace("(","")
   
                                          cc_ch_count = cc_ch.count(",") + 1
                                          cc_bw = m.group(3)
                                          logg.info("group 1: {} 2: {} 3: {} 4: {} 5: {} 6: {}".format(m.group(1),m.group(2),m.group(3),m.group(4),m.group(5),m.group(6)))
                                          logg.info("9800 test_parameters_summary:  read: tx: {} ch: {} bw: {}".format(tx,ch,bw))
   
                                          logg.info("9800 test_parameters cc_mac: read : {}".format(cc_mac))
                                          logg.info("9800 test_parameters cc_slot: read : {}".format(cc_slot))
                                          logg.info("9800 test_parameters cc_count: read : {}".format(cc_ch_count))
                                          logg.info("9800 test_parameters cc_bw: read : {}".format(cc_bw))
                                          logg.info("9800 test_parameters cc_power: read : {}".format(cc_power))
                                          logg.info("9800 test_parameters cc_dbm: read : {}".format(cc_dbm))
                                          logg.info("9800 test_parameters cc_ch: read : {}".format(cc_ch))
                                          break
   
                          if (cc_dbm == ""):
                             if loop_count >= 3: 
                                # Could not talk to controller? Not this may not be a reason to exit
                                # Some of the tests run for 32 plus hours ,  do not kill the whole test unless trying to 
                                # debug an issue with the test.  Sometimes the controller is taking time to configure.
                                err = "ERROR:  Could not query dBm from controller, maybe controller died?"
                                logg.info(err)
                                logg.info("Check controller and AP , Command on AP to erase the config: capwap ap erase all")
                                e_tot += err
                                e_tot += "  "
                             else:
                                logg.info("9800 read controller dBm loop_count {} try again".format(loop_count)) 
                          else:
                             cc_dbm_rcv = True    
                       try:
                          logg.info("9800 wifi_ctl_9800_3504.py: show_wlan_summary")
                          wlan_summary = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                              "--action", "show_wlan_summary","--series" , args.series,"--port", args.port,"--prompt",args.prompt], capture_output=True, check=True)
                          pss = wlan_summary.stdout.decode('utf-8', 'ignore')
                          logg.info(pss)
                       except subprocess.CalledProcessError as process_error:
                          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                   else:
                       try:
                           logg.info("3504 wifi_ctl_9800_3504.py: advanced")
                           advanced = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                              "--action", "advanced","--port", args.port,"--series" , args.series,"--prompt",args.prompt], capture_output=True, check=True)
                           pss = advanced.stdout.decode('utf-8', 'ignore')
                           logg.info(pss)
                       except subprocess.CalledProcessError as process_error:
                           logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                           exit_test(workbook)

                       searchap = False
                       cc_mac = ""
                       cc_ch = ""
                       cc_bw = ""
                       cc_power = ""
                       cc_dbm = ""
                       ch_count = ""
                       for line in pss.splitlines():
                           if (line.startswith("---------")):
                               searchap = True
                               continue

                           if (searchap):
                               pat = "%s\s+(\S+)\s+\S+\s+\S+\s+\S+\s+(\S+)\s+(\S+)\s+\(\s*(\S+)\s+dBm"%(args.ap)
                               m = re.search(pat, line)
                               if (m != None):
                                   cc_mac = m.group(1)
                                   cc_ch = m.group(2);  # (132,136,140,144)
                                   cc_power = m.group(3)
                                   cc_power = cc_power.replace("/", " of ", 1) # spread-sheets turn 1/8 into a date
                                   cc_dbm = m.group(4)

                                   ch_count = cc_ch.count(",")
                                   cc_bw = 20 * (ch_count + 1)
                                   
                                   break
                                
                       if (cc_dbm == ""):
                          # Could not talk to controller?
                          err = "ERROR:  Could not query dBm from controller, maybe controller died?"
                          logg.info(err)
                          e_tot += err
                          e_tot += "  "

                       logg.info("3504 test_parameters cc_mac: read : {}".format(cc_mac))
                       logg.info("3504 test_parameters cc_count: read : {}".format(ch_count))
                       logg.info("3504 test_parameters cc_bw: read : {}".format(cc_bw))
                       logg.info("3504 test_parameters cc_power: read : {}".format(cc_power))
                       logg.info("3504 test_parameters cc_dbm: read : {}".format(cc_dbm))
                       logg.info("3504 test_parameters cc_ch: read : {}".format(cc_ch))


                   # Up station
                   subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  lfresource, "--port_name", lfstation,
                                   "--set_ifstate", "up"]);

                   i = 0
                   wait_ip_print = False;
                   wait_assoc_print = False;
                   # Wait untill LANforge station connects
                   while True:
                       port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  lfresource, "--port_name", lfstation,
                                                    "--show_port", "AP,IP,Mode,NSS,Bandwidth,Channel,Signal,Noise,Status,RX-Rate"],capture_output=True, check=True)
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

                       #logg.info("IP %s  Status %s"%(_ip, _status))
                       
                       if (_status == "Authorized"):
                           if ((_ip != None) and (_ip != "0.0.0.0")):
                               logg.info("Station is associated with IP address.")
                               break
                           else:
                               if (not wait_ip_print):
                                   logg.info("Waiting for station to get IP Address.")
                                   wait_ip_print = True
                       else:
                           if (not wait_assoc_print):
                               logg.info("Waiting up to 180s for station to associate.")
                               wait_assoc_print = True

                       i += 1
                       # We wait a fairly long time since AP will take a long time to start on a CAC channel.
                       if (i > 180):
                           err = "ERROR:  Station did not connect within 180 seconds."
                           logg.info(err)
                           e_tot += err
                           e_tot += "  "
                           if args.series == "9800":
                               try:
                                  logg.info("9800 wifi_ctl_9800_3504.py: advanced")
                                  advanced = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                              "--action", "advanced","--series" , args.series,"--port", args.port,"--prompt",args.prompt], capture_output=True, check=True)
                                  pss = advanced.stdout.decode('utf-8', 'ignore')
                                  logg.info(pss)
                               except subprocess.CalledProcessError as process_error:
                                  logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
                                  exit_test(workbook)

                           if (args.wait_forever):
                               logg.info("Will continue waiting, you may wish to debug the system...")
                               i = 0
                           else:
                               break

                       time.sleep(1)

                   # Start traffic
                   subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  lfresource, "--action", "do_cmd",
                                   "--cmd", "set_cx_state all c-udp-power RUNNING"], capture_output=True, check=True)

                   # Wait configured number of seconds more seconds
                   logg.info("Waiting {} seconds to let traffic run for a bit, Channel {} NSS {} BW {} TX-Power {}".format(args.duration,ch, n, bw, tx))
                   time.sleep(int(args.duration))

                   # Gather probe results and record data, verify NSS, BW, Channel
                   i = 0
                   beacon_sig = None
                   sig = None
                   pf = 1
                   ants = []
                   while True:                       
                       time.sleep(1)
                       port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  lfresource, "--port_name", lfstation,
                                                    "--cli_cmd", "probe_port 1 %s %s"%(lfresource, lfstation)],capture_output=True, check=True)
                       pss = port_stats.stdout.decode('utf-8', 'ignore')
                       # for debug: print the output of lf_portmod.pl and the command used 
                       if (args.show_lf_portmod):
                           logg.info("./lf_portmod.pl --manager {} --card {} --port_name {} --cli_cmd probe_port 1 {} {}".format(lfmgr, lfresource, lfstation,lfresource,lfstation))
                           logg.info(pss)

                       foundit = False
                       for line in pss.splitlines():
                           #logg.info("probe-line: %s"%(line))
                           m = re.search('signal avg:\s+(\S+)\s+\[(.*)\]\s+dBm', line)
                           if (m != None):
                               logg.info("search: signal ave: resulted in m = {}".format(m))
                               sig = m.group(1)
                               ants = m.group(2).split()
                               q = 0
                               for a in ants:
                                   ants[q] = ants[q].replace(",", "", 1)
                                   q += 1

                               logg.info("sig: %s  ants: %s ants-len: %s n: %s"%(sig, m.group(2), len(ants), n))

                               if (len(ants) == int(n)):
                                   foundit = True
                               else:
                                   logg.info("Looking for %s spatial streams, signal avg reported fewer: %s"%(n, m.group(1)))

                           m = re.search('beacon signal avg:\s+(\S+)\s+dBm', line)
                           if (m != None):
                               logg.info("search: beacon signal avg: resulted in m = {}".format(m))
                               beacon_sig = m.group(1)
                               logg.info("beacon_sig: %s "%(beacon_sig))
                               
                       if (foundit):
                           break

                       i += 1
                       if (i > 10):
                           err = "Tried and failed 10 times to find correct spatial streams, continuing."
                           logg.info(err)
                           e_tot += err
                           e_tot += "  "
                           while (len(ants) < int(n)):
                               ants.append("")
                           break

                   endp_stats = subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  lfresource, "--endp_vals", "rx_bps",
                                                "--cx_name", "c-udp-power"],capture_output=True, check=True)

                   pss = endp_stats.stdout.decode('utf-8', 'ignore')
                   #logg.info(pss)

                   for line in pss.splitlines():
                       #logg.info("probe-line: %s"%(line))From Lanforge probe, command ./lf_portmod.pl with cli parameter probe_port 1 (about line 1150)
                       m = re.search('Rx Bytes:\s+(\d+)', line)
                       if (m != None):
                           logg.info("Rx Bytes: result {}".format(m))
                           rx_bytes = int(m.group(1))
                           if (rx_bytes == 0):
                               err = "ERROR:  No bytes received by data connection, test results may not be valid."
                               e_tot += err
                               e_tot += "  "

                   # Stop traffic
                   subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  lfresource, "--action", "do_cmd",
                                   "--cmd", "set_cx_state all c-udp-power STOPPED"],capture_output=True, check=True)

                   antstr = ""
                   for x in range(4):
                       if (x < int(n)):
                           logg.info("x: %s n: %s  len(ants): %s"%(x, n, len(ants)))
                           antstr += ants[x]
                       else:
                           antstr += " "
                       antstr += "\t"

                   port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card",  lfresource, "--port_name", lfstation,
                                                "--show_port", "AP,IP,Mode,NSS,Bandwidth,Channel,Signal,Noise,Status,RX-Rate"], capture_output=True, check=True)
                   pss = port_stats.stdout.decode('utf-8', 'ignore');

                   _ap = None
                   _bw = None
                   _ch = None
                   _mode = None
                   _nss = None
                   _noise = None
                   _rxrate = None
                   _noise_bare = None

                   for line in pss.splitlines():
                       m = re.search('AP:\s+(.*)', line)
                       if (m != None):
                           _ap = m.group(1)
                           logg.info("AP: {}".format(m))
                       m = re.search('Bandwidth:\s+(.*)Mhz', line)
                       if (m != None):
                           _bw = m.group(1)
                           logg.info("Bandwidth: {}".format(m))
                       m = re.search('Channel:\s+(.*)', line)
                       if (m != None):
                           _ch = m.group(1)
                           logg.info("Channel: {}".format(m))
                       m = re.search('Mode:\s+(.*)', line)
                       if (m != None):
                           _mode = m.group(1)
                           logg.info("Mode: {}".format(m))
                       m = re.search('NSS:\s+(.*)', line)
                       if (m != None):
                           _nss = m.group(1)
                           logg.info("NSS: {}".format(m))
                       m = re.search('Noise:\s+(.*)', line)
                       if (m != None):
                           _noise = m.group(1)
                           logg.info("Noise: {}".format(m))
                       m = re.search('Noise:\s+(.*)dBm', line)
                       if (m != None):
                           _noise_bare = m.group(1)
                           logg.info("Noise Bare: {}".format(m))
                       m = re.search('RX-Rate:\s+(.*)', line)
                       if (m != None):
                           _rxrate = m.group(1)
                           logg.info("RX-Rate: {}".format(m))

                   # ath10k radios now take noise-floor into account, so adjust_nf
                   # should remain set to false when using those radios.  Possibly other
                   # radios would need this, so leave code in place.
                   rssi_adj = 0
                   if (args.adjust_nf and _noise_bare != None):
                       _noise_i = int(_noise_bare)
                       if (_noise_i == 0):
                           # Guess we could not detect noise properly?
                           e_tot += "WARNING:  Invalid noise-floor, calculations may be inaccurate.  "
                           pf = 0
                       else:
                           rssi_adj = (_noise_i - nf_at_calibration)

                   if (sig == None):
                       e_tot += "ERROR:  Could not detect signal level.  "
                       sig = -100
                       pf = 0

                   if (beacon_sig == None):   
                       e_tot += "ERROR:  Could not detect beacon signal level.  "
                       beacon_sig = -100
                       pf = 0

                   pi = int(pathloss)
                   ag = int(antenna_gain)   
                   calc_dbm_beacon = int(beacon_sig) + pi + rssi_adj + ag
                   logg.info("calc_dbm_beacon {}".format(calc_dbm_beacon))

                   logg.info("sig: %s"%sig)
                   calc_dbm = int(sig) + pi + rssi_adj + ag
                   logg.info("calc_dbm %s"%(calc_dbm))


                   # Calculated per-antenna power is what we calculate the AP transmitted
                   # at (rssi + pathloss + antenna_gain ).  So, if we see -30 rssi, with pathloss of 44 ,
                   # with antenna gain of 6 
                   # then we calculate AP transmitted at +20
                   calc_ant1 = 0
                   if (ants[0] != ""):
                       calc_ant1 = int(ants[0]) + pi + rssi_adj + ag
                       logg.info("calc_ant1: {} = ants[0]: {} + pi: {} + rssi_adj: {} + ag: {}".format(calc_ant1,ants[0],pi, rssi_adj,ag))
                   calc_ant2 = 0
                   calc_ant3 = 0
                   calc_ant4 = 0
                   if (len(ants) > 1 and ants[1] != ""):
                       calc_ant2 = int(ants[1]) + pi + rssi_adj + ag
                       logg.info("calc_ant2: {} = ants[1]: {} + pi: {} + rssi_adj: {} + ag: {}".format(calc_ant2,ants[1],pi, rssi_adj,ag))

                   if (len(ants) > 2 and ants[2] != ""):
                       calc_ant3 = int(ants[2]) + pi + rssi_adj + ag
                       logg.info("calc_ant3: {} = ants[2]: {} + pi: {} + rssi_adj: {} + ag: {}".format(calc_ant3,ants[2],pi, rssi_adj,ag))

                   if (len(ants) > 3 and ants[3] != ""):
                       calc_ant4 = int(ants[3]) + pi + rssi_adj + ag
                       logg.info("calc_ant4: {} = ants[3]: {} + pi: {} + rssi_adj: {} + ag: {}".format(calc_ant4,ants[3],pi, rssi_adj,ag))


                   diff_a1 = ""
                   diff_a2 = ""
                   diff_a3 = ""
                   diff_a4 = ""

                   if (cc_dbm == ""):
                      cc_dbmi = 0
                   else:
                      cc_dbmi = int(cc_dbm)
                   diff_dbm = calc_dbm - cc_dbmi 
                   logg.info("diff_dbm {} calc_dbm {} - cc_dbmi {}".format(diff_dbm, calc_dbm, cc_dbmi))
                   diff_dbm_beacon = calc_dbm_beacon - cc_dbmi
                   logg.info("diff_dbm_beacon {} calc_dbm_beacon {} - cc_dbmi {}".format(diff_dbm_beacon, calc_dbm_beacon, cc_dbmi))

                   if(int(abs(diff_dbm_beacon)) > int(args.beacon_dbm_diff)):
                      w_tot = "WARNING: Controller dBm and Calculated dBm Beacon power different by greater than +/- {} dBm".format(args.beacon_dbm_diff) 

                   pfs = "PASS"
                   pfrange = pf_dbm



                   # Allowed per path is what we expect the AP should be transmitting at.
                   # calc_ant1 is what we calculated it actually transmitted at based on rssi
                   # pathloss and antenna gain.  Allowed per-path is modified taking into account that multi
                   # NSS tranmission will mean that each chain should be decreased so that sum total
                   # of all chains is equal to the maximum allowed txpower.
                   allowed_per_path = cc_dbmi
                   logg.info("allowed_per_path: {}  = cc_dbmi: {}".format(allowed_per_path,cc_dbmi))
                   if (int(_nss) == 1):
                       diff_a1 = calc_ant1 - cc_dbmi
                       logg.info("(Offset 1) diff_a1 (): {} = calc_ant1: {} - allowed_per_path: {}".format(diff_a1, calc_ant1, allowed_per_path))

                       if (abs(diff_a1) > pfrange):
                           pf = 0
                   if (int(_nss) == 2):
                       # NSS of 2 means each chain should transmit at 1/2 total power, thus the '- 3'
                       allowed_per_path = cc_dbmi - 3
                       logg.info("allowed_per_path: {}  = cc_dbmi: {} - 3".format(allowed_per_path,cc_dbmi))

                       diff_a1 = calc_ant1 - allowed_per_path
                       logg.info("(Offset 1) diff_a1: {} = calc_ant1: {} - allowed_per_path: {}".format(diff_a1, calc_ant1, allowed_per_path))

                       diff_a2 = calc_ant2 - allowed_per_path
                       logg.info("(Offset 2) diff_a2: {} = calc_ant2: {} - allowed_per_path: {}".format(diff_a2, calc_ant2, allowed_per_path))

                       if ((abs(diff_a1) > pfrange) or
                           (abs(diff_a2) > pfrange)):
                           pf = 0
                   if (int(_nss) == 3):
                       # NSS of 3 means each chain should transmit at 1/3 total power, thus the '- 5'
                       allowed_per_path = cc_dbmi - 5
                       logg.info("allowed_per_path: {}  = cc_dbmi: {} - 5".format(allowed_per_path,cc_dbmi))

                       diff_a1 = calc_ant1 - allowed_per_path
                       logg.info("(Offset 1) diff_a1: {} = calc_ant1: {} - allowed_per_path: {}".format(diff_a1, calc_ant1, allowed_per_path))

                       diff_a2 = calc_ant2 - allowed_per_path
                       logg.info("(Offset 2) diff_a2: {} = calc_ant2: {} - allowed_per_path: {}".format(diff_a2, calc_ant2, allowed_per_path))

                       diff_a3 = calc_ant3 - allowed_per_path
                       logg.info("(Offset 3) diff_a3: {} = calc_ant3: {} - allowed_per_path: {}".format(diff_a3, calc_ant3, allowed_per_path))

                       if ((abs(diff_a1) > pfrange) or
                           (abs(diff_a2) > pfrange) or
                           (abs(diff_a3) > pfrange)):
                           pf = 0
                   if (int(_nss) == 4):
                       # NSS of 4 means each chain should transmit at 1/4 total power, thus the '- 6'
                       allowed_per_path = cc_dbmi - 6
                       logg.info("allowed_per_path: {}  = cc_dbmi: {} - 6".format(allowed_per_path,cc_dbmi))

                       diff_a1 = calc_ant1 - allowed_per_path
                       logg.info("(Offset 1) diff_a1: {} = calc_ant1: {} - allowed_per_path: {}".format(diff_a1, calc_ant1, allowed_per_path))

                       diff_a2 = calc_ant2 - allowed_per_path
                       logg.info("(Offset 2) diff_a2: {} = calc_ant2: {} - allowed_per_path: {}".format(diff_a2, calc_ant2, allowed_per_path))

                       diff_a3 = calc_ant3 - allowed_per_path
                       logg.info("(Offset 3) diff_a3: {} = calc_ant3: {} - allowed_per_path: {}".format(diff_a3, calc_ant3, allowed_per_path))

                       diff_a4 = calc_ant4 - allowed_per_path
                       logg.info("(Offset 4) diff_a4: {} = calc_ant4: {} - allowed_per_path: {}".format(diff_a4, calc_ant4, allowed_per_path))

                       # Read AP to determine if there are less chains or spatial steams then expected
                       # Thus provide a passing result 
                       failed_low = 0
                       # least = 0
                       if (diff_a1 < -pfrange):
                           failed_low += 1
                           #least = diff_a1 #leave in code if want to move to least 
                       if (diff_a2 < -pfrange):
                           failed_low += 1
                           #least = min(least, diff_a2)
                       if (diff_a3 < -pfrange):
                           failed_low += 1
                           #least = min(least, diff_a3)
                       if (diff_a4 < -pfrange):
                           failed_low += 1
                           #least = min(least, diff_a4)

                       failed_low_threshold = 0
                       # 
                       #
                       # If the ap dictionary is set the read the AP to see the number
                       # of spatial streams used.  For tx power 1 the AP may determine to use
                       # fewer spatial streams
                       #
                       #
                       P1 = None
                       T1 = None
                       P2 = None
                       T2 = None
                       P3 = None
                       T3 = None
                       P4 = None
                       T4 = None
                       N_ANT = None
                       DAA_Pwr = None
                       DAA_N_TX = None
                       DAA_Total_pwr = None
                       if(bool(ap_dict)):
                            logg.info("ap_dict {}".format(ap_dict))
                            logg.info("Read AP ap_scheme: {} ap_ip: {} ap_port: {} ap_user: {} ap_pw: {}".format(ap_dict['ap_scheme'],ap_dict['ap_ip'],ap_dict["ap_port"],
                                                         ap_dict['ap_user'],ap_dict['ap_pw']))
                            logg.info("####################################################################################################") 
                            logg.info("# READ AP POWERCFG") 
                            logg.info("####################################################################################################") 

                            try:
                                logg.info("ap_ctl.py: read AP power information")
                                ap_info= subprocess.run(["./ap_ctl.py", "--scheme", ap_dict['ap_scheme'], "--prompt", ap_dict['ap_prompt'],"--dest", ap_dict['ap_ip'], "--port", ap_dict["ap_port"],
                                                          "--user", ap_dict['ap_user'], "--passwd", ap_dict['ap_pw'],"--action", "powercfg"],stdout=subprocess.PIPE)
                                try:
                                    pss = ap_info.stdout.decode('utf-8', 'ignore')
                                except:
                                    logg.info("ap_info was of type NoneType will set pss empty")
                                    pss = "empty"

                            except subprocess.CalledProcessError as process_error:
                                logg.info("####################################################################################################") 
                                logg.info("# CHECK IF AP HAS TELNET CONNECTION ALREADY ACTIVE") 
                                logg.info("####################################################################################################") 
                      
                                logg.info("####################################################################################################") 
                                logg.info("# Unable to commicate to AP error code: {} output {}".format(process_error.returncode, process_error.output)) 
                                logg.info("####################################################################################################") 
                                #exit_test(workbook)
                                pss = "empty_process_error"

                            logg.info(pss)
                            for line in pss.splitlines():
                                logg.info("ap {}".format(line))
                                pat = '^\s+1\s+6\s+\S+\s+\S+\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)'
                                m = re.search(pat, line)
                                if (m != None):
                                    P1 = m.group(1)
                                    T1 = m.group(2)
                                    P2 = m.group(3)
                                    T2 = m.group(4)
                                    P3 = m.group(5)
                                    T3 = m.group(6)
                                    P4 = m.group(7)
                                    T4 = m.group(8)
                                    N_ANT = m.group(9)
                                    DAA_Pwr = m.group(10)
                                    DAA_N_TX = m.group(11) # number of spatial streams
                                    DAA_Total_pwr = m.group(12)
                                    # adjust the fail criterial based on the number of spatial streams
                                    if DAA_N_TX == "4":
                                        failed_low_threshold = 0
                                        logg.info("4 failed_low_threshold {}".format(failed_low_threshold))
                                    if DAA_N_TX == "3":
                                        failed_low_threshold = 1
                                        logg.info("3 failed_low_threshold {}".format(failed_low_threshold))
                                    if DAA_N_TX == "2":
                                        failed_low_threshold = 2
                                        logg.info("2 failed_low_threshold {}".format(failed_low_threshold))
                                    if DAA_N_TX == "1":
                                        failed_low_threshold = 3
                                        logg.info("1 failed_low_threshold {}".format(failed_low_threshold))



                                    i_tot = "P1: {} T1: {} P2: {} T2: {} P3: {} T3: {} P4: {} T4: {} N_ANT: {} DAA_Pwr: {} DAA_N_TX: {} DAA_Total_pwr: {}  ".format(
                                        P1,T1,P2,T2,P3,T3,P4,T4,N_ANT,DAA_Pwr,DAA_N_TX,DAA_Total_pwr)
                                    print(i_tot)
                                    logg.info(i_tot)
                                else:
                                    logg.info("AP Check using regular expressions")


                       #
                       #  The controller may adjust the number of spatial streams to allow for the 
                       #  best power values
                       #
                       # for 4 spatial streams if the AP is read and the failed threshold is met then there is a failure
                       # the failure will be caugh below if the range is not correct. 
                       # range check and reading the data from the AP may be used in conjunction thus it is coded to be non-exclusive
                       logg.info("failed_low: {} failed_low_threshold: {}".format(failed_low,failed_low_threshold))
                       if bool(ap_dict) and failed_low > failed_low_threshold:
                           logg.info("failed_low: {} > failed_low_threshold: {}".format(failed_low,failed_low_threshold))
                           pf = 0
                       
                       if(pf_ignore_offset != 0):
                           logg.info("diff_a1: {} diff_a2: {} diff_a3: {} diff_a4: {} pfrange: {} pf_ignore_offset: {}".format(diff_a1,diff_a2,diff_a3,diff_a4,pfrange,pf_ignore_offset))
                           if (diff_a1 < -pfrange):
                               if(diff_a1 < (-pfrange - pf_ignore_offset)):
                                   logg.info("diff_a1: {} < -pfrange: {} - pf_ignore_offset: {}".format(diff_a1, pfrange, pf_ignore_offset))
                                   i_tot += "PASSED diff_a1({}) < -pfrange({}) - pf_ignore_offset({})  ".format(diff_a1, pfrange, pf_ignore_offset) 
                                   logg.info("i_tot {}".format(i_tot))
                               else:    
                                   logg.info("diff_a1: {} failure".format(diff_a1))
                                   pf = 0
                           if (diff_a2 < -pfrange):
                               if(diff_a2 < (-pfrange - pf_ignore_offset)):
                                   logg.info("diff_a2: {} < -pfrange: {} - pf_ignore_offset: {}".format(diff_a2, pfrange, pf_ignore_offset))
                                   i_tot += "PASSED diff_a2({}) < -pfrange({}) - pf_ignore_offset({})  ".format(diff_a2, pfrange, pf_ignore_offset) 
                                   logg.info("i_tot {}".format(i_tot))
                               else:
                                   logg.info("diff_a2: {} failure".format(diff_a2))
                                   pf = 0
                           if (diff_a3 < -pfrange):
                               if(diff_a3 < (-pfrange - pf_ignore_offset)):
                                   logg.info("diff_a3: {} < -pfrange: {} - pf_ignore_offset: {}".format(diff_a3, pfrange, pf_ignore_offset))
                                   i_tot += "PASSED diff_a3({}) < -pfrange({}) - pf_ignore_offset({})  ".format(diff_a3, pfrange, pf_ignore_offset) 
                                   logg.info("i_tot {}".format(i_tot))
                               else:
                                   logg.info("diff_a3: {} failure".format(diff_a3))
                                   pf = 0
                           if (diff_a4 < -pfrange):
                               if(diff_a4 < (-pfrange - pf_ignore_offset)):
                                   logg.info("diff_a4: {} < -pfrange: {} - pf_ignore_offset: {}".format(diff_a4, pfrange, pf_ignore_offset))
                                   i_tot += "PASSED diff_a4({}) < -pfrange({}) - pf_ignore_offset({})  ".format(diff_a4, pfrange, pf_ignore_offset) 
                                   logg.info("i_tot {}".format(i_tot))
                               else:                            
                                   logg.info("diff_a4: {} failure".format(diff_a4))
                                   pf = 0

                       # check for range to high
                       if (diff_a1 > pfrange):
                           pf = 0
                       if (diff_a2 > pfrange):
                           pf = 0
                       if (diff_a3 > pfrange):
                           pf = 0
                       if (diff_a4 > pfrange):
                           pf = 0
                       
                   logg.info("_nss {}  allowed_per_path (AP should be transmitting at) {}".format(_nss, allowed_per_path))

                   if (pf == 0 or e_tot != ""):
                       pfs = "FAIL"

                   time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "{:.3f}".format(time.time() - (math.floor(time.time())))[1:]  
                   ln = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(
                       myrd, pathloss, antenna_gain, ch, n, bw, tx, beacon_sig, sig,
                       antstr, _ap, _bw, _ch, _mode, _nss, _noise, _rxrate,
                       cc_mac, cc_ch, cc_power, cc_dbm,
                       calc_dbm, diff_dbm, calc_ant1, calc_ant2, calc_ant3, calc_ant4,
                       diff_a1, diff_a2, diff_a3, diff_a4, pfs, time_stamp
                     )

                   #logg.info("RESULT: %s"%(ln))
                   csv.write(ln)
                   csv.write("\t")

                   ln = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(
                       myrd, pathloss, antenna_gain, _ch, _nss, _bw, tx, allowed_per_path,
                       antstr,
                       calc_ant1, calc_ant2, calc_ant3, calc_ant4,
                       diff_a1, diff_a2, diff_a3, diff_a4, pfs, time_stamp
                       )
                   csvs.write(ln)
                   csvs.write("\t")
                   

                   col = 0
                   worksheet.write(row, col, myrd, center_blue); col += 1
                   worksheet.write(row, col, args.series, center_blue); col += 1
                   worksheet.write(row, col, cc_ch, center_blue); col += 1
                   worksheet.write(row, col, _ch, center_blue); col += 1
                   worksheet.write(row, col, _nss, center_blue); col += 1
                   worksheet.write(row, col, cc_bw, center_blue); col += 1
                   worksheet.write(row, col, _bw, center_blue); col += 1
                   worksheet.write(row, col, tx, center_tan); col += 1
                   worksheet.write(row, col, allowed_per_path, center_tan); col += 1
                   worksheet.write(row, col, pathloss, center_tan); col += 1
                   worksheet.write(row, col, antenna_gain, center_tan); col += 1
                   worksheet.write(row, col, _noise, center_tan); col += 1
                   if (args.adjust_nf):
                       worksheet.write(row, col, rssi_adj, center_tan); col += 1
                   worksheet.write(row, col, _rxrate, center_tan); col += 1
                   worksheet.write(row, col, beacon_sig, center_tan); col += 1
                   worksheet.write(row, col, sig, center_tan); col += 1
                   for x in range(4):
                       if (x < int(n)):
                           worksheet.write(row, col, ants[x], center_peach); col += 1
                       else:
                           worksheet.write(row, col, " ", center_peach); col += 1
                   worksheet.write(row, col, calc_ant1, center_pink); col += 1
                   worksheet.write(row, col, calc_ant2, center_pink); col += 1
                   worksheet.write(row, col, calc_ant3, center_pink); col += 1
                   worksheet.write(row, col, calc_ant4, center_pink); col += 1

                   if (diff_a1 != "" and abs(diff_a1) > pfrange):
                       worksheet.write(row, col, diff_a1, center_yel_red); col += 1
                   else:
                       worksheet.write(row, col, diff_a1, center_yel); col += 1
                   if (diff_a2 != "" and abs(diff_a2) > pfrange):
                       worksheet.write(row, col, diff_a2, center_yel_red); col += 1
                   else:
                       worksheet.write(row, col, diff_a2, center_yel); col += 1
                   if (diff_a3 != "" and abs(diff_a3) > pfrange):
                       worksheet.write(row, col, diff_a3, center_yel_red); col += 1
                   else:
                       worksheet.write(row, col, diff_a3, center_yel); col += 1
                   if (diff_a4 != "" and abs(diff_a4) > pfrange):
                       worksheet.write(row, col, diff_a4, center_yel_red); col += 1
                   else:
                       worksheet.write(row, col, diff_a4, center_yel); col += 1
                   worksheet.write(row, col, cc_dbmi, center_blue); col +=1
                   worksheet.write(row, col, calc_dbm_beacon, center_blue); col +=1
                   worksheet.write(row, col, diff_dbm_beacon, center_blue); col +=1
                   worksheet.write(row, col, calc_dbm, center_blue); col +=1
                   worksheet.write(row, col, diff_dbm, center_blue); col +=1
                       
                   if (pfs == "FAIL"):
                       worksheet.write(row, col, pfs, red); col += 1
                   else:
                       worksheet.write(row, col, pfs, green); col += 1
                   worksheet.write(row, col, time_stamp, green); col += 1
                   if (_bw != bw):
                       err = "ERROR:  Requested bandwidth: %s != station's reported bandwidth: %s.  "%(bw, _bw)
                       e_tot += err
                       logg.info(err)
                       csv.write(err)
                       csvs.write(err)
                   if (_nss != n):
                       err = "ERROR:  Station NSS: %s != configured: %s.  "%(_nss, n)
                       logg.info(err)
                       csv.write(err)
                       csvs.write(err)
                       e_tot += err

                   if (e_tot == ""):
                       e_w_tot = e_tot + w_tot + i_tot
                       if(w_tot == ""):
                           worksheet.write(row, col, e_w_tot, green_left); col += 1
                       else:
                           worksheet.write(row, col, e_w_tot, orange_left); col += 1
                   else:
                       e_w_tot = e_tot + w_tot + i_tot
                       worksheet.write(row, col, e_w_tot, red_left); col += 1
                   row += 1

                   csv.write("\n");
                   csv.flush()

                   csvs.write("\n");
                   csvs.flush()

                   # write out the data and exit on error : error takes presidence over failure
                   if (e_tot != ""):
                       if(args.exit_on_error):
                           logg.info("EXITING ON ERROR, exit_on_error err: {} ".format(e_tot))
                           if bool(email_dicts):
                               for email_dict in email_dicts:
                                  try:
                                     logg.info("Sending Email ")
                                     subject = "Lanforge: Error {}".format(outfile_xlsx)
                                     body    = "Lanforeg: Error: AP: {} Channel: {} NSS: {} BW: {} TX-Power {}, pfs: {} time_stamp: {}  {}".format(args.ap, ch, n, bw, tx, pfs, time_stamp, outfile_xlsx)
                                     email_out = subprocess.run(["./lf_mail.py", "--user", email_dict['user'] , "--passwd", email_dict['passwd'], "--to",email_dict['to'] , 
                                       "--subject", subject, "--body", body , "--smtp", email_dict['smtp'], "--port", email_dict['port'] ], capture_output=cap_ctl_out, check=True)
                                     pss = email_out.stdout.decode('utf-8','ignore')
                                     logg.info(pss)
                                  except subprocess.CalledProcessError as process_error:
                                    logg.info("Unable to send email smtp {} port {} error code: {} output {}".format(email_dict['smtp'],email_dict['port'],process_error.returncode, process_error.output))
                           exit_test(workbook)


                   # write out the data and exit on failure
                   if (pf == 0):
                       if(args.exit_on_fail):
                           if(e_tot != ""):
                               logg.info("EXITING ON FAILURE as a result of  err {}".format(e_tot))
                           else:
                               logg.info("EXITING ON FAILURE, exit_on_fail set there was no err ")
                           if bool(email_dicts):
                               for email_dict in email_dicts: 
                                   try:
                                      logg.info("Sending Email ")
                                      subject = "Lanforge: Failure Found {}".format(outfile_xlsx)
                                      body    = "Lanforge: Failure Found:  AP: {} Channel: {} NSS: {} BW: {} TX-Power {}, pfs: {} time_stamp: {} {}".format(args.ap,ch, n, bw, tx, pfs, time_stamp,outfile_xlsx)
                                      email_out =subprocess.run(["./lf_mail.py", "--user", email_dict['user'] , "--passwd", email_dict['passwd'], "--to",email_dict['to'] , 
                                         "--subject", subject, "--body", body , "--smtp", email_dict['smtp'], "--port", email_dict['port'] ], capture_output=cap_ctl_out, check=True)
                                      if cap_ctl_out:   
                                         pss = email_out.stdout.decode('utf-8','ignore')
                                         logg.info(pss)
                                   except subprocess.CalledProcessError as process_error:
                                       logg.info("Unable to send email smtp {} port {} error code: {} output {}".format(email_dict['smtp'],email_dict['port'],process_error.returncode, process_error.output))

                           exit_test(workbook)
                            

   if bool(email_dicts):
       for email_dict in email_dicts:
           try:
               logg.info("Sending Email ")
               subject = "Lanforge Test Compete {}".format(outfile_xlsx)
               body    = "Lanforeg Test Complete : AP: {} time_stamp: {}  {}".format(args.ap, time_stamp, outfile_xlsx)
               email_out = subprocess.run(["./lf_mail.py", "--user", email_dict['user'] , "--passwd", email_dict['passwd'], "--to",email_dict['to'] , 
               "--subject", subject, "--body", body , "--smtp", email_dict['smtp'], "--port", email_dict['port'] ], capture_output=cap_ctl_out, check=True)
               if cap_ctl_out:
                  pss = email_out.stdout.decode('utf-8','ignore')
                  logg.info(pss)
           except subprocess.CalledProcessError as process_error:
               logg.info("Unable to send email smtp {} port {} error code: {} output {}".format(email_dict['smtp'],email_dict['port'],process_error.returncode, process_error.output))


   workbook.close()

   # check if keeping the existing state
   if(args.keep_state):
       logg.info("9800/3504 flag --keep_state set thus keeping state")
       try:
          logg.info("9800/3504 wifi_ctl_9800_3504.py: advanced")
          advanced = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
             "--action", "advanced","--series" , args.series,"--port", args.port,"--prompt",args.prompt], capture_output=True, check=True)
          pss = advanced.stdout.decode('utf-8', 'ignore')
          logg.info(pss)
       except subprocess.CalledProcessError as process_error:
          logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
          exit_test(workbook) 
       try:
          logg.info("9800/3504 wifi_ctl_9800_3504.py: summary")
          advanced = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
             "--action", "summary","--series" , args.series,"--port", args.port,"--prompt",args.prompt], capture_output=True, check=True)
          pss = advanced.stdout.decode('utf-8', 'ignore')
          logg.info(pss)
       except subprocess.CalledProcessError as process_error:
           logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
           exit_test(workbook) 

       exit_test(workbook)
   else:
      # Set things back to defaults
      # remove the station
      if(args.cleanup):
          logg.info("--cleanup set Deleting all stations on radio {}".format(args.radio))
          subprocess.run(["./lf_associate_ap.pl", "--action", "del_all_phy","--port_del", args.radio], timeout=20, capture_output=True)
   
      # Disable AP, apply settings, enable AP
      try:
         logg.info("9800/3504 wifi_ctl_9800_3504.py: disable AP {}".format(args.ap))
         ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                      "--action", "disable", "--series" , args.series,"--port", args.port,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True)
         if cap_ctl_out:
             pss = ctl_output.stdout.decode('utf-8', 'ignore')
             logg.info(pss)
   
      except subprocess.CalledProcessError as process_error:
         logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
         exit_test(workbook) 
   
      if args.series == "9800":
   
          try:
             logg.info("9800 wifi_ctl_9800_3504.py: no_wlan_wireless_tag_policy")
             ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                             "--action", "no_wlan_wireless_tag_policy","--series",args.series,"--wlan", args.wlan,"--port", args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True) 
             if cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)
   
          except subprocess.CalledProcessError as process_error:
             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output)) 
             #exit_test(workbook)
   
          try:
             logg.info("9800 wifi_ctl_9800_3504.py: delete_wlan")
             ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                         "--action", "delete_wlan","--series",args.series, "--wlanID", args.wlanID, "--wlan", args.wlan, "--wlanSSID", args.wlanSSID,
                         "--port",args.port,"--prompt",args.prompt], capture_output=cap_ctl_out, check=True)    
             if cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)
   
          except subprocess.CalledProcessError as process_error:
             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
             #exit_test(workbook) 
   
          try:
             logg.info("9800 wifi_ctl_9800_3504.py: disable_network_5ghz")
             ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                      "--action", "disable_network_5ghz","--series",args.series,"--port", args.port,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True)      
             if cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)
   
          except subprocess.CalledProcessError as process_error:
             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
             #exit_test(workbook) 
   
          try:
             logg.info("9800 wifi_ctl_9800_3504.py: disable_network_24ghz")
             ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                      "--action", "disable_network_24ghz","--series",args.series,"--port", args.port,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True)                 
             if cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)
   
          except subprocess.CalledProcessError as process_error:
             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
             #exit_test(workbook) 
   
      else:
          try:
             logg.info("3504 wifi_ctl_9800_3504.py: config 802.11a disable network")
             ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                      "--action", "cmd", "--value", "config 802.11a disable network","--series" , args.series,"--port", args.port,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True)
             if cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)
   
          except subprocess.CalledProcessError as process_error:
             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
             #exit_test(workbook) 
   
          try:
             logg.info("3504 wifi_ctl_9800_3504.py: config 802.11b disable network")
             ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                      "--action", "cmd", "--value", "config 802.11b disable network","--port", args.port,"--series" , args.series,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True)
             if cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)
   
          except subprocess.CalledProcessError as process_error:
             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
             #exit_test(workbook) 
   
      if (tx != "NA"):
          try: 
             logg.info("9800/3504 wifi_ctl_9800_3504.py: txPower tx 1")
             ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                          "--action", "txPower", "--value", "1", "--series" , args.series,"--port", args.port,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True)
             if cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)
   
          except subprocess.CalledProcessError as process_error:
             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
             #exit_test(workbook) 
   
      # NSS is set on the station earlier...
      if (ch != "NA"):
          try:
             logg.info("9800/3504 wifi_ctl_9800_3504.py: channel 36")
             ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                          "--action", "channel", "--value", "36", "--series" , args.series,"--port", args.port,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True)
             if cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)
   
          except subprocess.CalledProcessError as process_error:
             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
             #exit_test(workbook) 
   
      if (bw != "NA"):
          try:
             logg.info("9800/3504 wifi_ctl_9800_3504.py: bandwidth 20")
             ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                          "--action", "bandwidth", "--value", "20", "--series" , args.series,"--port", args.port,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True)
             if cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)
   
          except subprocess.CalledProcessError as process_error:
             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
             #exit_test(workbook)
   
      if args.series == "9800":
          try:
             logg.info("9800 wifi_ctl_9800_3504.py: enable_network_5ghz")
             ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                      "--action", "enable_network_5ghz","--series",args.series,"--port", args.port,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True)         
             if cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)
   
          except subprocess.CalledProcessError as process_error:
             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
             #exit_test(workbook) 
   
          try:
             logg.info("9800 wifi_ctl_9800_3504.py: enable_network_24ghz")
             ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                      "--action", "enable_network_24ghz","--series",args.series,"--port", args.port,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True) 
             if cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)
   
          except subprocess.CalledProcessError as process_error:
             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
             #exit_test(workbook) 
   
          try:
             logg.info("9800 wifi_ctl_9800_3504.py: auto")
             ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                      "--action", "auto","--series",args.series,"--port", args.port,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True)
             if cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)
   
          except subprocess.CalledProcessError as process_error:
             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
             #exit_test(workbook) 
   
      else:     
          try:
             logg.info("3504 wifi_ctl_9800_3504.py: config 802.11a enable network")
             ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                      "--action", "cmd", "--value", "config 802.11a enable network","--port", args.port, "--series" , args.series,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True)
             if cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)
   
          except subprocess.CalledProcessError as process_error:
             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
             exit_test(workbook) 
   
          try:
             logg.info("3504 wifi_ctl_9800_3504.py: config 802.11b enable network")
             ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                      "--action", "cmd", "--value", "config 802.11b enable network","--series" , args.series,"--port", args.port,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True)
             if cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)
   
          except subprocess.CalledProcessError as process_error:
             logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
             exit_test(workbook) 
   
      try:
         logg.info("9800/3504 wifi_ctl_9800_3504.py: enable")
         ctl_output = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                      "--action", "enable", "--series" , args.series,"--port", args.port,"--prompt",args.prompt],capture_output=cap_ctl_out, check=True)
         if cap_ctl_out:
            pss = ctl_output.stdout.decode('utf-8', 'ignore')
            logg.info(pss)
   
      except subprocess.CalledProcessError as process_error:
         logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
         exit_test(workbook) 
   
      # Remove LANforge traffic connection
      subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  lfresource, "--action", "do_cmd",
                      "--cmd", "set_cx_state all c-udp-power DELETED"], capture_output=True);
      subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  lfresource, "--action", "do_cmd",
                      "--cmd", "rm_endp c-udp-power-A"], capture_output=True);
      subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource",  lfresource, "--action", "do_cmd",
                      "--cmd", "rm_endp c-udp-power-B"], capture_output=True);
   
      # Show controller status
      try:
         logg.info("9800/3504 wifi_ctl_9800_3504.py: advanced")
         advanced = subprocess.run(["./wifi_ctl_9800_3504.py", "--scheme", scheme, "-d", args.dest, "-u", args.user, "-p", args.passwd, "-a", args.ap, "--band", band,
                                 "--action", "advanced", "--series" , args.series,"--port", args.port,"--prompt",args.prompt], capture_output=True, check=True)
         pss = advanced.stdout.decode('utf-8', 'ignore');
         logg.info(pss)
      except subprocess.CalledProcessError as process_error:
         logg.info("Controller unable to commicate to AP or unable to communicate to controller error code: {} output {}".format(process_error.returncode, process_error.output))
         exit_test(workbook) 
   
   
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
if __name__ == '__main__':
   main()
   print("Summary results stored in %s, full results in %s, xlsx file in %s"%(outfile, full_outfile, outfile_xlsx))
   
####
####
####
   
