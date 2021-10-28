#!/usr/bin/python3
'''

NAME:
ap_ctl.py

PURPOSE:
Script that logs into an AP via Serial, SSH, or Telnet to read data or execute commands

EXAMPLE:

./ap_ctl.py --scheme "serial" "--tty "Serial port for accessing AP" --prompt "#" --dest <ip if using SSH or Telnet> --port <port , none for serial>  --user <user name>
        --passwd <password> --action <command>

In a program: 
ap_info= subprocess.run(["./ap_ctl.py", "--scheme", ap_dict['ap_scheme'], "--prompt", ap_dict['ap_prompt'],"--dest", ap_dict['ap_ip'], "--port", ap_dict["ap_port"],
                                                        "--user", ap_dict['ap_user'], "--passwd", ap_dict['ap_pw'],"--action", "powercfg"],stdout=subprocess.PIPE)
                                
NOTES: 

LANforge 192.168.100.178
Controller at 192.168.100.112 admin/Cisco123
Controller is 192.1.0.10
AP is on serial port /dev/ttyUSB1 or /dev/ttyUSB2  9600 8 n 1 

make sure pexpect is installed:
$ sudo yum install python3-pexpect

You might need to install pexpect-serial using pip:
$ pip3 install pexpect-serial

$ sudo pip3 install pexpect-serial

./ap_ctl.py 
'''


import sys
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

import logging
import time
from time import sleep
import argparse
import pexpect
import serial
from pexpect_serial import SerialSpawn

# pip install pexpect-serial  (on Ubuntu)
# sudo pip install pexpect-serial (on Ubuntu for everyone)

default_host = "localhost"
default_ports = {
    "serial": None,
    "ssh":   22,
    "telnet": 23
}
NL = "\n"
CR = "\r\n"
Q = '"'
A = "'"
FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'
band = "a"
logfile = "stdout"

# regex101.com  , 
# this will be in the tx_power script
# ^\s+1\s+6\s+\S+\s+\S+\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+) 

def usage():
    print("$0 used connect to Cisco AP:")
    print("-a|--ap:  AP to act upon")
    print("-d|--dest:  destination host")
    print("-o|--port:  destination port")
    print("-u|--user:  AP login name")
    print("-p|--pass:  AP password")
    print("-s|--scheme (serial|telnet|ssh): connect to controller via serial, ssh or telnet")
    print("--tty Serial port for accessing AP")
    print("-l|--log file: log messages here")
    print("-b|--baud:  serial baud rate")
    print("-z|--action: action")
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

# Test command if lanforge connected ttyUSB0
# sudo ./ap_ctl.py -a lanforge -d 0 -o 0 -u "lanforge" -p "lanforge" -s "serial" -t "/dev/ttyUSB0"
# sample for lanforge 192.168.100.178
# sudo ./ap_ctl.py -a APA53.0E7B.EF9C -d 0 -o 0 -u "admin" -p "Admin123" -s "serial" -t "/dev/ttyUSB2" -z "show_log"
def main():

    global logfile

    AP_ESCAPE       = "Escape character is '^]'."
    AP_USERNAME     = "Username:"
    AP_PASSWORD     = "Password:"
    AP_EN           = "en"
    AP_MORE         = "--More--"
    AP_EXIT         = "exit"
    LF_PROMPT       = "$"
    CR = "\r\n"

    
    parser = argparse.ArgumentParser(description="Cisco AP Control Script")
    parser.add_argument("-a", "--prompt",  type=str, help="ap prompt")
    parser.add_argument("-d", "--dest",    type=str, help="address of the AP  172.19.27.55")
    parser.add_argument("-o", "--port",    type=int, help="control port on the AP, 2008")
    parser.add_argument("-u", "--user",    type=str, help="credential login/username, admin")
    parser.add_argument("-p", "--passwd",  type=str, help="credential password Wnbulab@123")
    parser.add_argument("-s", "--scheme",  type=str, choices=["serial", "ssh", "telnet"], help="Connect via serial, ssh or telnet")
    parser.add_argument("-t", "--tty",     type=str, help="tty serial device for connecting to AP")
    parser.add_argument("-l", "--log",     type=str, help="logfile for messages, stdout means output to console",default="stdout")
    parser.add_argument("-z", "--action",  type=str, help="action,  current action is powercfg")
    parser.add_argument("-b", "--baud",    type=str, help="action,  baud rate lanforge: 115200  cisco: 9600")

    args = None
    try:
        args = parser.parse_args()
        host = args.dest
        scheme = args.scheme
        port = (default_ports[scheme], args.port)[args.port != None]
        user = args.user
        if (args.log != None):
            logfile = args.log
    except Exception as e:
        logging.exception(e)
        usage()
        exit(2)
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
    egg = None # think "eggpect"
    ser = None
    try:
        if (scheme == "serial"):
            #eggspect = pexpect.fdpexpect.fdspan(telcon, logfile=sys.stdout.buffer)
            ser = serial.Serial(args.tty, int(args.baud), timeout=5)
            print("Created serial connection on %s, open: %s"%(args.tty, ser.is_open))
            egg = SerialSpawn(ser)
            egg.logfile = FileAdapter(logg)
            time.sleep(1)
            egg.sendline(CR)
            time.sleep(1)

        elif (scheme == "ssh"):
            if (port is None):
                port = 22
            cmd = "ssh -p%d %s@%s"%(port, user, host)
            logg.info("Spawn: "+cmd+NL)
            egg = pexpect.spawn(cmd)
            #egg.logfile_read = sys.stdout.buffer
            egg.logfile = FileAdapter(logg)
        elif (scheme == "telnet"):
            if (port is None):
                port = 23
            cmd = "telnet {} {}".format(host, port)
            logg.info("Spawn: "+cmd+NL)
            egg = pexpect.spawn(cmd)
            egg.logfile = FileAdapter(logg)
            # Will login below as needed.
        else:
            usage()
            exit(1)
    except Exception as e:
        logging.exception(e)
    
    AP_PROMPT       = "{}>".format(args.prompt)
    AP_HASH         = "{}#".format(args.prompt)
    time.sleep(0.1)
    logged_in  = False
    loop_count = 0
    while (loop_count <= 8 and logged_in == False):
        loop_count += 1
        i = egg.expect_exact([AP_ESCAPE,AP_PROMPT,AP_HASH,AP_USERNAME,AP_PASSWORD,AP_MORE,LF_PROMPT,pexpect.TIMEOUT],timeout=5)
        if i == 0:
            logg.info("Expect: {} i: {} before: {} after: {}".format(AP_ESCAPE,i,egg.before,egg.after))
            egg.sendline(CR) # Needed after Escape or should just do timeout and then a CR?
            sleep(1)
        if i == 1:
            logg.info("Expect: {} i: {} before: {} after: {}".format(AP_PROMPT,i,egg.before,egg.after))
            egg.sendline(AP_EN) 
            sleep(1)
            j = egg.expect_exact([AP_PASSWORD,pexpect.TIMEOUT],timeout=5)
            if j == 0:
                logg.info("Expect: {} i: {} j: {} before: {} after: {}".format(AP_PASSWORD,i,j,egg.before,egg.after))
                egg.sendline(args.passwd) 
                sleep(1)
                k = egg.expect_exact([AP_HASH,pexpect.TIMEOUT],timeout=5)
                if k == 0:
                    logg.info("Expect: {} i: {} j: {} k: {} before: {} after: {}".format(AP_PASSWORD,i,j,k,egg.before,egg.after))
                    logged_in = True
                if k == 1:
                    logg.info("Expect: {} i: {} j: {} k: {} before: {} after: {}".format("Timeout",i,j,k,egg.before,egg.after))
            if j == 1:
                logg.info("Expect: {} i: {} j: {} before: {} after: {}".format("Timeout",i,j,egg.before,egg.after))

        if i == 2:
            logg.info("Expect: {} i: {} before: {} after: {}".format(AP_HASH,i,egg.before,egg.after))
            logged_in = True 
            sleep(1)
        if i == 3:
            logg.info("Expect: {} i: {} before: {} after: {}".format(AP_USERNAME,i,egg.before,egg.after))
            egg.sendline(args.user) 
            sleep(1)
        if i == 4:
            logg.info("Expect: {} i: {} before: {} after: {}".format(AP_PASSWORD,i,egg.before,egg.after))
            egg.sendline(args.passwd) 
            sleep(1)
        if i == 5:
            logg.info("Expect: {} i: {} before: {} after: {}".format(AP_MORE,i,egg.before,egg.after))
            if (scheme == "serial"):
                egg.sendline("r")
            else:
                egg.sendcontrol('c')
            sleep(1)
        # for Testing serial connection using Lanforge
        if i == 6:
            logg.info("Expect: {} i: {} before: {} after: {}".format(LF_PROMPT,i,egg.before.decode('utf-8', 'ignore'),egg.after.decode('utf-8', 'ignore')))
            if (loop_count < 3):
                egg.send("ls -lrt")
                sleep(1)
            if (loop_count > 4):
                logged_in = True # basically a test mode using lanforge serial
        if i == 7:
            logg.info("Expect: {} i: {} before: {} after: {}".format("Timeout",i,egg.before,egg.after))
            egg.sendline(CR) 
            sleep(1)


    if (args.action == "powercfg"):
        logg.info("execute: show controllers dot11Radio 1 powercfg | g T1")
        egg.sendline('show controllers dot11Radio 1 powercfg | g T1')
        egg.expect([pexpect.TIMEOUT], timeout=3)  # do not delete this for it allows for subprocess to see output
        print(egg.before.decode('utf-8', 'ignore')) # do not delete this for it  allows for subprocess to see output
        i = egg.expect_exact([AP_MORE,pexpect.TIMEOUT],timeout=5)
        if i == 0:
            egg.sendcontrol('c')
        if i == 1:
            logg.info("send cntl c anyway")
            egg.sendcontrol('c')

    elif (args.action == "clear_log"):
        logg.info("execute: clear log")
        egg.sendline('clear log')
        sleep(0.4)
        egg.sendline('show log')
        egg.expect([pexpect.TIMEOUT], timeout=2)  # do not delete this for it allows for subprocess to see output
        print(egg.before.decode('utf-8', 'ignore')) # do not delete this for it  allows for subprocess to see output
        # allow for normal logout below

    elif (args.action == "show_log"):
        logg.info("execute: show log")
        egg.sendline('show log')
        sleep(0.4)
        egg.expect([pexpect.TIMEOUT], timeout=2)  # do not delete this for it allows for subprocess to see output
        print(egg.before.decode('utf-8', 'ignore')) # do not delete this for it  allows for subprocess to see output
        i = egg.expect_exact([AP_MORE,pexpect.TIMEOUT],timeout=4)
        if i == 0:
            egg.sendline('r')
            egg.expect([pexpect.TIMEOUT], timeout=4)  # do not delete this for it allows for subprocess to see output
            print(egg.before.decode('utf-8', 'ignore')) # do not delete this for it  allows for subprocess to see output
        if i == 1:
            print(egg.before.decode('utf-8', 'ignore')) # do not delete this for it  allows for subprocess to see output
        # allow for normal logout below
        # show log | g DOT11_DRV

    # CAC_EXPIRY_EVT: CAC finished on DFS channel 52
    elif (args.action == "cac_expiry_evt"):
        logg.info("execute: show log | g CAC_EXPIRY_EVT")    
        egg.sendline('show log | g CAC_EXPIRY_EVT')
        sleep(0.4)
        egg.expect([pexpect.TIMEOUT], timeout=2)  # do not delete this for it allows for subprocess to see output
        print(egg.before.decode('utf-8', 'ignore')) # do not delete this for it  allows for subprocess to see output
        i = egg.expect_exact([AP_MORE,pexpect.TIMEOUT],timeout=4)
        if i == 0:
            egg.sendline('r')
            egg.expect([pexpect.TIMEOUT], timeout=4)  # do not delete this for it allows for subprocess to see output
            print(egg.before.decode('utf-8', 'ignore')) # do not delete this for it  allows for subprocess to see output
        if i == 1:
            print(egg.before.decode('utf-8', 'ignore')) # do not delete this for it  allows for subprocess to see output

    elif (args.action == "ds_data_5ghz"):
        logg.info("execute: wl -i wl1 bs_data")
        egg.sendline('wl -i wl1 bs_data')
        egg.expect([pexpect.TIMEOUT], timeout=4) # do not detete this for it allow for subprocess to read
        print(egg.before.decode('utf-8','ignore')) # do not delete this for it  allows for subprocess to see output


    elif (args.action == "ds_data_24ghz"):
        logg.info("execute: wl -i wl0 bs_data")
        egg.sendline('wl -i wl1 bs_data')
        egg.expect([pexpect.TIMEOUT], timeout=4) # do not detete this for it allow for subprocess to read
        print(egg.before.decode('utf-8','ignore')) # do not delete this for it  allows for subprocess to see output


    else: # no other command at this time so send the same power command
        #logg.info("no action so execute: show controllers dot11Radio 1 powercfg | g T1")
        logg.info("no action")

    i = egg.expect_exact([AP_PROMPT,AP_HASH,pexpect.TIMEOUT],timeout=1)
    if i == 0:
        logg.info("received {} we are done send exit".format(AP_PROMPT))
        egg.sendline(AP_EXIT)
    if i == 1:
        logg.info("received {} send exit".format(AP_HASH))
        egg.sendline(AP_EXIT)
    if i == 2:
        logg.info("timed out waiting for {} or {}".format(AP_PROMPT,AP_HASH))
        
    #             ctlr.execute(cn_cmd)

''' NOTES for AP DFS

#############################

1. Do "show AP summary" on the controller to see the list of AP's connected.
2. Now, check the channel configured on the AP using the commend "show ap  channel <AP-Name>"

3. Check for the current channel and Channel width for Slot id 1. See the output of this command.

4. Before making any changes, please connect at least 1 client to this AP in 5GHz radio. 
Keep running the ping traffic to the default gateway of the AP.

4. Now, configure dfs channel for this AP with 20MHz as channel width.

6. After CAC Expiry, Client should connect back - Verify the pings are passing through or not.
Note time:  
"show logging" in the AP will show the CAC timer details. You can grep for "DFS CAC timer enabled time 60" and "changed to DFS channel 52, running CAC for 60 seconds.
Wait for 60 sec and check for this log "CAC_EXPIRY_EVT: CAC finished on DFS channel 52"

[*07/07/2020 23:37:48.1460] changed to DFS channel 52, running CAC for 60 seconds.
[*07/07/2020 23:38:48.7240] CAC_EXPIRY_EVT: CAC finished on DFS channel 52

"make a note of the time and check the CAC timer expired in 60-61 seconds.

7. Now, trigger the radar on Channel 52. AP should move to another channel.
 Also, When the radar is triggered, capture the CSA frames and verify the CSA count is set to 10 or not.

 8. Now, verify the black-list time of the channel for this AP.  : show ap auto-rf 802.11a <AP-Name>
 In the controller, give the command "show ap auto-rf 802.11a <AP-Name>" under Radar information you should see the "Detected Channels and Blacklist Times" . 
Black list time will be 1800 seconds which is 30 minutes.

Radar Information
    DFS stats on serving radio................... 0
    DFS stats on RHL radio....................... 0
    DFS stats triggered.......................... 0
    Cumulative stats on serving radio............ 0
    Cumulative stats on RHL radio................ 0
    Cumulative stats triggered................... 0
    Detected Channels
      Channel 100................................    5 seconds ago
    Blacklist Times
      Channel 100................................ 1795 seconds remaining

(Cisco Controller) >show ap channel APA453.0E7B.CF9C

  Slot Id ..................................... 0
  802.11b/g Current Channel ..................... 11*
  Allowed Channel List........................... 1,2,3,4,5,6,7,8,9,10,11

  Slot Id ..................................... 1
  802.11a Current Channel ....................... (36,40)  40MHz / Cap 160MHz 
  Allowed Channel List........................... 36,40,44,48,52,56,60,64,100,
                      ........................... 104,108,112,116,120,124,128,
                      ........................... 132,136,140,144,149,153,157,
                      ........................... 161,165




###########################

Password: [*02/09/2021 14:30:04.2290] Radio [1] Admininstrative state ENABLED  change to DISABLED 
[*02/09/2021 14:30:04.2300] DOT11_DRV[1]: Stop Radio1
[*02/09/2021 14:30:04.2520] DOT11_DRV[1]: DFS CAC timer enabled time 60
[*02/09/2021 14:30:04.2740] DOT11_DRV[1]: DFS CAC timer enabled time 60
[*02/09/2021 14:30:04.2740] Stopped Radio 1
[*02/09/2021 14:30:36.2810] Radio [1] Admininstrative state DISABLED  change to ENABLED 
[*02/09/2021 14:30:36.3160] DOT11_DRV[1]: set_channel Channel set to 52/20  <<<<<<   ????
[*02/09/2021 14:30:36.3390] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 14:30:36.4420] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 14:30:36.5440] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 14:30:36.6490] DOT11_DRV[1]: DFS CAC timer enabled time 60   <<<<<<  ????
[*02/09/2021 14:30:37.2100] wl0: wlc_iovar_ext: vap_amsdu_rx_max: BCME -23
[*02/09/2021 14:30:37.2100] wl: Unsupported
[*02/09/2021 14:30:37.2100] ERROR: return from vap_amsdu_rx_max was -45
[*02/09/2021 14:30:37.4100] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 14:30:37.5040] DOT11_CFG[1]: Starting radio 1
[*02/09/2021 14:30:37.5050] DOT11_DRV[1]: Start Radio1                             <<<<<<<<<
[*02/09/2021 14:30:37.5120] DOT11_DRV[1]: set_channel Channel set to 52/20
[*02/09/2021 14:30:37.5340] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 14:30:37.6360] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 14:30:37.7370] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 14:30:37.8410] DOT11_DRV[1]: DFS CAC timer enabled time 60              <<<<<<<
[*02/09/2021 14:30:37.8650] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 14:30:37.9800] changed to DFS channel 52, running CAC for 60 seconds.   <<<<<  Note use this one
[*02/09/2021 14:30:38.0020] Started Radio 1                                          <<<<< After start radio
[*02/09/2021 14:31:07.4650] wl0: wlc_iovar_ext: olpc_cal_force: BCME -16
[*02/09/2021 14:31:38.4210] CAC_EXPIRY_EVT: CAC finished on DFS channel 52    <<<<<<   Start with this very unique CAC finished 
[*02/09/2021 14:31:48.2850] chatter: client_ip_table :: ClientIPTable no client entry found, dropping packet 04:F0:21:F

# note lf_hackrf.py begins transmitting immediately... see if that is what is to happen?

[*02/09/2021 15:20:53.7470] wcp/dfs :: RadarDetection: radar detected       <<<<<  Radar detected
[*02/09/2021 15:20:53.7470] wcp/dfs :: RadarDetection: sending packet out to capwapd, slotId=1, msgLen=386, chanCnt=1 2
[*02/09/2021 15:20:53.7720] DOT11_DRV[1]: DFS CAC timer disabled time 0
[*02/09/2021 15:20:53.7780] Enabling Channel and channel width Switch Announcement on current channel 
[*02/09/2021 15:20:53.7870] DOT11_DRV[1]: set_dfs Channel set to 36/20, CSA count 6         <<<<<<<   Channel Set
[*02/09/2021 15:20:53.8530] DOT11_DRV[1]: DFS CAC timer enabled time 60


Trying another station
*02/09/2021 15:25:32.6130] Radio [1] Admininstrative state ENABLED  change to DISABLED 
[*02/09/2021 15:25:32.6450] DOT11_DRV[1]: Stop Radio1
[*02/09/2021 15:25:32.6590] Stopped Radio 1
[*02/09/2021 15:25:52.1700] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:26:04.6640] Radio [1] Admininstrative state DISABLED  change to ENABLED 
[*02/09/2021 15:26:04.6850] DOT11_DRV[1]: set_channel Channel set to 36/20
[*02/09/2021 15:26:04.7070] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:26:04.8090] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:26:04.9090] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:26:05.5620] wl0: wlc_iovar_ext: vap_amsdu_rx_max: BCME -23
[*02/09/2021 15:26:05.5620] wl: Unsupported
[*02/09/2021 15:26:05.5620] ERROR: return from vap_amsdu_rx_max was -45
[*02/09/2021 15:26:05.7600] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:26:05.8530] DOT11_CFG[1]: Starting radio 1
[*02/09/2021 15:26:05.8540] DOT11_DRV[1]: Start Radio1
[*02/09/2021 15:26:05.8610] DOT11_DRV[1]: set_channel Channel set to 36/20
[*02/09/2021 15:26:05.8830] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:26:05.9890] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:26:06.0900] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:26:06.2080] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:26:06.5350] Started Radio 1
[*02/09/2021 15:26:15.9750] chatter: client_ip_table :: ClientIPTable no client entry found, dropping packet 04:F0:21:




Username: [*02/09/2021 15:33:49.8680] Radio [1] Admininstrative state ENABLED  change to DISABLED 
[*02/09/2021 15:33:49.9010] DOT11_DRV[1]: Stop Radio1
[*02/09/2021 15:33:49.9160] Stopped Radio 1
[*02/09/2021 15:34:14.4150] DOT11_DRV[1]: set_channel Channel set to 56/20
[*02/09/2021 15:34:14.4370] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:34:14.5390] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:34:14.6400] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:34:14.7450] DOT11_DRV[1]: DFS CAC timer enabled time 60
[*02/09/2021 15:34:21.9160] Radio [1] Admininstrative state DISABLED  change to ENABLED 
[*02/09/2021 15:34:21.9370] DOT11_DRV[1]: set_channel Channel set to 56/20
[*02/09/2021 15:34:21.9590] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:34:22.0610] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:34:22.1610] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:34:22.2650] DOT11_DRV[1]: DFS CAC timer enabled time 60
[*02/09/2021 15:34:22.8270] wl0: wlc_iovar_ext: vap_amsdu_rx_max: BCME -23
[*02/09/2021 15:34:22.8270] wl: Unsupported
[*02/09/2021 15:34:22.8270] ERROR: return from vap_amsdu_rx_max was -45
[*02/09/2021 15:34:23.0280] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:34:23.1210] DOT11_CFG[1]: Starting radio 1
[*02/09/2021 15:34:23.1210] DOT11_DRV[1]: Start Radio1
[*02/09/2021 15:34:23.1280] DOT11_DRV[1]: set_channel Channel set to 56/20
[*02/09/2021 15:34:23.1510] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:34:23.2520] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:34:23.3520] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:34:23.4560] DOT11_DRV[1]: DFS CAC timer enabled time 60
[*02/09/2021 15:34:23.4800] wlc_ucode_download: wl0: Loading 129 MU ucode
[*02/09/2021 15:34:23.5960] changed to DFS channel 56, running CAC for 60 seconds.
[*02/09/2021 15:34:23.6180] Started Radio 1

'''
if __name__ == '__main__':
    main()

####
####
####
