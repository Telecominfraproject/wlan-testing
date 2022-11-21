#!/usr/bin/python3
'''
LANforge 172.19.27.91
Controller at 172.19.27.95 2013 cisco/Cisco123
Controller is 192.1.0.10
AP is 172.19.27.95 2014

make sure pexpect is installed:
$ sudo yum install python3-pexpect

You might need to install pexpect-serial using pip:
$ pip3 install pexpect-serial

./wifi_ctl_9800_3504.py -d 172.19.27.95 -o 2013 -l stdout -a AxelMain -u cisco -p Cisco123 -s telnet

# For LANforge lab system.
./wifi_ctl_9800_3504.py --scheme ssh -d 192.168.100.112 --user admin --passwd Cisco123 --ap APA453.0E7B.CF9C  --series 3504  --action cmd --value "show ap config general APA453.0E7B.CF9C" --prompt "(Cisco Controller)"
./wifi_ctl_9800_3504.py --scheme ssh -d 192.168.100.112 --user admin --passwd Cisco123 --ap APA453.0E7B.CF9C  --series 3504  --action summary --prompt "(Cisco Controller)"

# For LANforge 3-chamber automation lab.
# Set up jumphost connection:
ssh -L 8888:172.16.0.2:22 root@192.168.100.109

# List all AP info
./wifi_ctl_9800_3504.py --scheme ssh -d localhost --port 8888 --user admin --passwd Cisco123 --ap APA453.0E7B.CF9C --series 9800  --action cmd --value "show ap config slots" --prompt "WLC2" --timeout 10



telnet 172.19.36.168(Pwd:), go to the privileged mode and execute the command “clear line 43”.

Cisco uses 9130 AP
show controllers dot11Radio 1 wlan

AP
Command on AP to erase the config:"capwap ap erase all"

TODO:
Consolidate the login for Telnet and SSH for 9800 if possible.
Note: trying to simplify the login process lead to lockups and made it more difficult to understand what stage
of the login was locking up.  The timing was determined emperically.

TODO setting the number of spatial streams.


no ap dot11 6ghz dot11ax mcs tx index 7 spatial-stream 1
no ap dot11 6ghz dot11ax mcs tx index 9 spatial-stream 1
no ap dot11 6ghz dot11ax mcs tx index 11 spatial-stream 1
no ap dot11 6ghz dot11ax mcs tx index 7 spatial-stream 2
no ap dot11 6ghz dot11ax mcs tx index 9 spatial-stream 2
no ap dot11 6ghz dot11ax mcs tx index 11 spatial-stream 2
no ap dot11 6ghz dot11ax mcs tx index 7 spatial-stream 3
no ap dot11 6ghz dot11ax mcs tx index 9 spatial-stream 3
no ap dot11 6ghz dot11ax mcs tx index 11 spatial-stream 3
no ap dot11 6ghz dot11ax mcs tx index 7 spatial-stream 4
no ap dot11 6ghz dot11ax mcs tx index 9 spatial-stream 4
no ap dot11 6ghz dot11ax mcs tx index 11 spatial-stream 4

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
import importlib
import os


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../")))

# TODO change the name from logg to logger
# to match consistency with other files.
logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")


default_host = "localhost"
default_ports = {
    "serial": None,
    "ssh": 22,
    "telnet": 23
}
NL = "\n"
CR = "\r\n"
Q = '"'
A = "'"
FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'
band = "a"
egg = None  # think "eggpect"  Need global scope for recovery


def usage():
    print("$0 used connect to controller:")
    print("-d|--dest:  destination host")
    print("-o|--port:  destination port")
    print("--prompt:   prompt to expect, ie \"\\(Cisco Controller\\) >\"")
    print("--series: cisco controller series, ie \"9800\"")

    print("-u|--user:  login name")
    print("-p|--pass:  password")
    print("-s|--scheme (serial|telnet|ssh): connect via serial, ssh or telnet")
    print("-l|--log file: log messages here ")
    print("-b|--band:  a (5Ghz) or b (2.4Ghz) or abgn for dual-band 2.4Ghz AP")
    print("-w|--wlan:  WLAN name")
    print("-i|--wlanID:  WLAN ID")
    print("-i|--wlanSSID:  WLAN SSID")

    print("-h|--help")

# see https://stackoverflow.com/a/13306095/11014343

# Used by pexpect
# TODO need to change as all pexpect has line number of the write


class FileAdapter(object):
    def __init__(self, logger):
        self.logger = logger

    def write(self, data):
        # NOTE: data can be a partial line, multiple lines
        data = data.strip()  # ignore leading/trailing whitespace
        if data:  # non-blank
            # 6/3/2022 set to debug 
            self.logger.info(data)

    def flush(self):
        pass  # leave it to logging to flush properly



# TODO make OO
def main():
    parser = argparse.ArgumentParser(description="Cisco AP Control Script")
    parser.add_argument("-d", "--dest", type=str, help="address of the cisco controller")
    parser.add_argument("-o", "--port", type=int, help="control port on the controller")
    parser.add_argument("--prompt", type=str, help="Prompt to expect", default="WLC")  # (Cisco Controller)#
    parser.add_argument("--timeout", type=int, help="expect prompt matching timeout", default=3)
    parser.add_argument("--series", type=str, help="cisco controller series", default="9800")
    parser.add_argument("-u", "--user", type=str, help="credential login/username")
    parser.add_argument("-p", "--passwd", type=str, help="credential password")
    parser.add_argument("-s", "--scheme", type=str, choices=["serial", "ssh", "telnet"], help="Connect via serial, ssh or telnet")
    parser.add_argument("-t", "--tty", type=str, help="tty serial device")
    parser.add_argument("-l", "--log", type=str, help="logfile for messages, stdout means output to console", default="stdout")
    # parser.add_argument("-r", "--radio",   type=str, help="select radio")
    parser.add_argument("-w", "--wlan", "--wlan_name", type=str, dest="wlan", help="wlan open-wlan , wlan name", default=None)
    parser.add_argument("-i", "--wlanID", type=str, help="wlan ID")
    parser.add_argument("--wlanSSID", type=str, help="wlan SSID")
    parser.add_argument("--security_key", type=str, help="wlan security_key")
    parser.add_argument("-a", "--ap", type=str, help="select AP", required=True)
    # TODO Should the Slot be passed for every command? or just check with 6g
    parser.add_argument("--ap_band_slot", type=str, help="select AP ap slot 24g = 0, 5g = 1 , 6g = 2 or 3")
    parser.add_argument("-b", "--band", type=str, help="Select band (a | b | abgn | 6g | 5g | 24g)",
                        choices=["dual_band_6g", "dual_band_5g", "6g", "5g", "24g", "a", "b", "abgn"])
    parser.add_argument("--tag_policy", type=str, help="--tag_policy default-tag-policy")
    # parser.add_argument("--tag_policy",     type=str, help="--tag_policy default-tag-policy", default="RM204-TB2")
    parser.add_argument("--policy_profile", type=str, help="--policy_profile default-policy-profile")
    # parser.add_argument("--wlan_name", type=str, help="--wlan_name open-wlan", default="open-wlan")
    parser.add_argument("--spatial_stream", help="--spatial_stream 1 , 2, 3, or 4 , configure controller for specific number of spatial streams")
    parser.add_argument("--mcs_tx_index", help="--mcs_tx_index 7, 9  or 11 to , configure controller for specific number of spatial streams")


    parser.add_argument("--action", type=str, help="perform action",
                        choices=["config", "dtim", "debug_disable_all", "no_logging_console", "line_console_0", "country", "ap_country", 
                                 "enable_operation_status", "disable_operation_status", "summary", "advanced",
                                 "cmd", "txPower", "bandwidth", "manual", "auto", "no_wlan", "show_ap_wlan_summary", "show_wlan_summary", "show_radio",
                                 "ap_channel", "auto_rf", "channel", "show", "create_wlan", "create_wlan_wpa2", "create_wlan_wpa3", "enable_wlan", "disable_wlan", "wlan_qos",
                                 "disable_network_dual_band_6ghz","disable_network_dual_band_5ghz","disable_network_6ghz", "disable_network_5ghz", "disable_network_24ghz",
                                 "enable_network_dual_band_6ghz","enable_network_dual_band_5ghz","enable_network_6ghz", "enable_network_5ghz", "enable_network_24ghz",
                                 "wireless_tag_policy", "no_wlan_wireless_tag_policy", "delete_wlan",
                                 "show_ap_name_config_role",
                                 "show_ap_bssid_dual_band_6g", "show_ap_bssid_dual_band_5g", "show_ap_bssid_6g", "show_ap_bssid_5g", "show_ap_bssid_24g",  
                                 "11r_logs", "enable_ft_akm_ftpsk", "enable_ftotd_akm_ftpsk",
                                 "config_dual_band_mode","dual_band_no_mode_shutdown","dual_band_mode_shutdown",
                                 "enable_ft_akm_ftsae","enable_ft_wpa3_dot1x","enable_ft_wpa3_dot1x_sha256",
                                 "ap_dot11_dot11ax_mcs_tx_index_spatial_stream", "no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream",
                                 "show_wireless_client_sumry", 'show_client_macadd_detail','debug_wieless_mac',
                                 'no_debug_wieless_mac','get_ra_trace_files','get_data_ra_trace_files', 'del_ra_trace_file',
                                 "show_ap_status","show_ap_tx_power_config"
                                 ])
    parser.add_argument("--value", type=str, help="set value")
    # logging configuration
    parser.add_argument(
        "--lf_logger_config_json",
        help="--lf_logger_config_json <json file> , json configuration of logger")

    args = None
    try:
        args = parser.parse_args()
        host = args.dest
        scheme = args.scheme
        port = args.port
        # port = (default_ports[scheme], args.port)[args.port != None]
        user = args.user
        passwd = args.passwd
        logfile = args.log
        if (args.band is not None):
            band = args.band
            if band == 'a':
                band = '5g'
            elif band == 'b':
                band = '24g'
    except Exception as e:
        logging.exception(e)
        exit(2)

    # configuation band confersion
    if band == '24g':
        config_band = '24ghz'
    elif band == '5g':
        config_band = '5ghz'
    elif band == '6g':
        config_band = '6ghz'
    elif band == 'dual_band_5g':
        config_band = 'dual-band'
    elif band == 'dual_band_6g':
        config_band = 'dual-band'
    else:
        logger.critical("band needs to be set 24g 5g 6g dual_band_5g, dual_band_6g")
        raise ValueError("band needs to be set 24g 5g 6g dual_band_5g or dual_band_6g")


    # set up logger
    logger_config = lf_logger_config.lf_logger_config()
    if args.lf_logger_config_json:
        # logger_config.lf_logger_config_json = "lf_logger_config.json"
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()

    if args.series == "9800":
        SEND_MORE = ' '
    else:
        SEND_MORE = NL  # Not sure about this.

    timeout = args.timeout
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(FORMAT)
    logg = logging.getLogger(__name__)
    
    logg.info("wifi_ctl command timeout set to {timeout}".format(timeout=timeout))

    # TODO Refactor for script to work must have output go to console_handler
    # This does work since it is a subordinate to the root logger
    # logg.setLevel(logging.DEBUG)
    # WARNING : pexpect uses the expect uses the fileadapter
    # TODO refactor pexpect
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

    print("cisco series {}".format(args.series))
    print("scheme {}".format(args.scheme))

    CCPROMPT = args.prompt + " >"  # '\(Voice-Talwar\) >'
    LOGOUTPROMPT = 'User:'
    EXITPROMPT = "Would you like to save them now? (y/N)"
    AREYOUSURE = "Are you sure you want to continue? (y/n)"
    CLOSEDBYREMOTE = "closed by remote host."
    CLOSEDCX = "Connection to .* closed."

    # 9800 series PROMPTS
    CCP = args.prompt + ">"                     # WLC>
    CCP_EN = args.prompt + "#"                     # WLC#
    CCP_CONFIG = args.prompt + "(config)#"  # WLC(config)#
    CCP_CONFIG_WLAN = args.prompt + "(config-wlan)#"  # WLC(config- wlan)#
    CCP_POLICY_TAG = args.prompt + "(config-policy-tag)#"  # WLC(config-policy-tag)#
    CCP_CONFIG_LINE = args.prompt + "(config-line)#"  # WLC(config-line)#
    CCP_FINGERPRINT = "you want to continue connecting (yes/no/[fingerprint])?"
    CCP_BAD_IP = "% Bad IP address or host name% Unknown command or computer name, or unable to find computer address"

    '''print("CCP {}".format(CCP))
   print("CCP_EN {}".format(CCP_EN))
   print("CCP_CONFIG {}".format(CCP_CONFIG))
   print("CCP_CONFIG_WLAN {}".format(CCP_CONFIG_WLAN))
   print("CCP_POLICY_TAG {}".format(CCP_POLICY_TAG))
   print("CCP_CONFIG_LINE {}".format(CCP_CONFIG_LINE))'''

    # DTIM , dtim, Delivery Traffic Indication Message
    # dtim dot11 5ghz
    # (config-wlan)#dtim dot11 5ghz ? <DTIM> Period

    # TODO do some command verification
    # if args.band is '6g' and args.ap_band_slot is None:
    #    raise ValueError('6g needs slot passed in ')

    try:
        if (scheme == "serial"):
            # eggspect = pexpect.fdpexpect.fdspan(telcon, logfile=sys.stdout.buffer)
            import serial
            from pexpect_serial import SerialSpawn
            with serial.Serial('/dev/ttyUSB0', 115200, timeout=5) as ser:
                egg = SerialSpawn(ser)
                egg.logfile = FileAdapter(logg)
                print("logg {}".format(logg))
                egg.sendline(NL)
                time.sleep(0.1)
                egg.expect('login:', timeout=3)
                time.sleep(0.1)
                egg.sendline(user)
                time.sleep(0.1)
                egg.expect('ssword:')

        elif (scheme == "ssh"):
            if (port is None):
                port = 22
            cmd = "ssh -p%d -o PubkeyAuthentication=no %s@%s" % (port, user, host)
            logg.info("Spawn: " + cmd + NL)
            egg = pexpect.spawn(cmd)
            # egg.logfile_read = sys.stdout.buffer
            egg.logfile = FileAdapter(logg)
            print("logg {}".format(logg))
            time.sleep(0.1)
            logged_in_9800 = False
            loop_count = 0
            found_escape = False
            # 9800 series
            if args.series == "9800":
                while logged_in_9800 == False and loop_count <= 4:
                    loop_count += 1
                    # logg.info("9800 establishing Telnet egg {} ".format(egg))
                    # sleep(2)
                    # TODO:  These next two lines do not work in Ferndale lab with ssh connection. --Ben
                    # egg.sendline(CR)
                    # sleep(0.4)
                    try:
                        i = egg.expect_exact(["Escape character is '^]'.", CCP, CCP_EN, "User:", "Password:", CCP_CONFIG, "Bad secrets", CCP_FINGERPRINT, pexpect.TIMEOUT],
                                             timeout=timeout)
                    except Exception as e:
                        logg.info('connection failed. or refused Connection open by other process')
                        logging.exception(e)
                        exit(1)

                    if i == 0:
                        logg.info("9800 SSH found Escape character is '^] i:{} before: {} after: {}".format(i, egg.before, egg.after))
                        # egg.sendline(CR)
                        found_escape = True
                        sleep(0.1)
                        j = egg.expect_exact([CCP, CCP_EN, "User:", "Password:", CCP_CONFIG, pexpect.TIMEOUT], timeout=timeout)
                        sleep(0.1)
                        if j == 0:
                            logg.info("9800 SSH found {}  will elevate loging i:{} j:{} before {} after {}".format(CCP, i, j, egg.before, egg.after))
                            egg.sendline("en")
                            sleep(0.1)
                            k = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("9800 SSH received password prompt will send password: {} i:{} j:{} k:{} before {} after {}".format(args.passwd, i, j, k, egg.before, egg.after))
                                egg.sendline(args.passwd)
                                sleep(0.1)
                                l = egg.expect_exact([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                                if l == 0:
                                    logg.info("9800 SSH Successfully received # prompt i:{} j:{} k:{} l:{}".format(i, j, k, l))
                                    logged_in_9800 = True
                                    egg.sendline("terminal length 0")  # Disable --More-- stuff for easier scripting
                                    egg.expect_exact([CCP_EN, pexpect.TIMEOUT], timeout=1)
                                if l == 1:
                                    logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                            if k == 1:
                                logg.info("9800 SSH received timeout after looking for password: prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 1:
                            logg.info("9800 found # so logged in can start sending commands i:{} j:{}".format(i, j))
                            logged_in_9800 = True
                        if j == 2:
                            logg.info("9800 found User: will put in args.user {} i:{} j:{}".format(args.user, i, j))
                            egg.sendline(args.user)
                            sleep(0.1)
                            k = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("9800 received password prompt after sending User, sending password: {} i:{} j:{} k:{}".format(args.passwd, i, j, k))
                                egg.sendline(args.passwd)
                                sleep(0.1)
                                l = egg.expect_exact([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                                if l == 0:
                                    logg.info("8900 SSH Successfully received # prompt i:{} j:{} k:{} l:{}".format(i, j, k, l))
                                    logged_in_9800 = True
                                if l == 1:
                                    logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                            if k == 1:
                                logg.info("9800 received timeout after looking for password after sending user i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 3:
                            sleep(0.1)
                            logg.info("9800 received Password prompt will send password {} i:{} j:{} before {} after {}".format(args.passwd, i, j, egg.before, egg.after))
                            egg.sendline(args.passwd)
                            sleep(0.1)
                            k = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("8900 SSH Successfully received # prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                                logged_in_9800 = True
                            if k == 1:
                                logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 4:
                            logg.info("9800 received {} prompt doing some cleanup".format(CCP_CONFIG))
                            egg.sendline("exit")
                            sleep(0.1)
                            k = egg.expect_exact([CCP, CCP_EN, "User:", "Password:", pexpect.TIMEOUT], timeout=timeout)
                            sleep(0.1)
                            if k == 0:
                                logg.info("9800 found CCP  will elevate loging i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                                egg.sendline("en")
                                sleep(0.1)
                                l = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                                if l == 0:
                                    logg.info("9800 received password prompt will send password: {} i:{} j:{} k:{} l:{} before {} after {}".format(args.passwd, i, j, k, l, egg.before, egg.after))
                                    egg.sendline(args.passwd)
                                    sleep(0.1)
                                    m = egg.expect_exact([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                                    if m == 0:
                                        logg.info("9800 SSH Successfully received # prompt i:{} j:{} k:{} l:{} m:{}".format(i, j, k, l, m))
                                        logged_in_9800 = True
                                    if m == 1:
                                        logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} l:{} m:{} before {} after {}".format(i, j, k, l, m, egg.before, egg.after))
                                if l == 1:
                                    logg.info("8900 received timeout after looking for password: prompt i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                            if k == 1:
                                logg.info("9800 found # so logged in can start sending commands i:{} j:{} k:{}".format(i, j, k))
                                logged_in_9800 = True
                            if k == 2:
                                logg.info("9800 found User: will put in args.user {}  i:{} j:{} k:{}".format(args.user, i, j, k))
                                egg.sendline(args.user)
                                sleep(0.1)
                                l = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                                if l == 0:
                                    logg.info("9800 received password prompt after sending User, sending password: {} i:{} j:{} k:{} l:{}".format(args.passwd, i, j, k, l))
                                    egg.sendline(args.passwd)
                                    sleep(0.1)
                                    m = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                                    if m == 0:
                                        logg.info("9800 SSH Successfully received # prompt i:{} j:{} k:{} l:{} m:{}".format(i, j, k, l, m))
                                        logged_in_9800 = True
                                    if m == 1:
                                        logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} l:{} m:{} before {} after {}".format(i, j, k, l, m, egg.before, egg.after))
                                if l == 1:
                                    logg.info("9800 received timeout after looking for password after sending user i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                            if k == 3:
                                sleep(0.1)
                                logg.info("9800 received Password prompt will send password {} i:{} j:{} k:{}  before {} after {}".format(args.passwd, i, j, k, egg.before, egg.after))
                                egg.sendline(args.passwd)
                                sleep(0.1)
                                l = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                                if l == 0:
                                    logg.info("8900 SSH Successfully received # prompt i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                                    logged_in_9800 = True
                                if l == 1:
                                    logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                            if k == 4:
                                logg.info("9800 timed out looking {}, {}, User:, Password:  i:{} j:{} k:{} before {} after {}".format(CCP, CCP_EN, i, j, k, egg.before, egg.after))
                                logg.info("9800 Timed out waiting for initial prompt send logout loop_count: {} i: {} j: {} k:{} before {} after {}".format(loop_count, i, j, k, egg.before, egg.after))
                                logg.info("9800  Closing the connection and try to re-establish, ")
                                egg.close(force=True)
                                sleep(1)
                                egg.close(force=True)
                                sleep(1)

                                # re establish ssh
                                cmd = "ssh -p%d %s@%s" % (port, user, host)
                                logg.info("Spawn: " + cmd + NL)
                                egg = pexpect.spawn(cmd)
                                egg.logfile = FileAdapter(logg)
                                time.sleep(2)
                                logged_in_9800 = False
                                found_escape = False

                        if j == 5:
                            logg.info(
                                "9800 timed out looking for CCP :{},CCP_EN: {},CCP_CONFIG: {} loop_count {} i {} j {}  before {} after {}".format(
                                    CCP, CCP_EN, CCP_CONFIG, loop_count, i, j, egg.before, egg.after))
                            logg.info("9800  Closing the connection and try to re-establish loop_count {} i {} j {}".format(loop_count, i, j))
                            egg.close(force=True)
                            sleep(1)
                            egg.close(force=True)
                            sleep(1)

                            # re establish ssh
                            cmd = "ssh -p%d %s@%s" % (port, user, host)
                            logg.info("Spawn: " + cmd + NL)
                            egg = pexpect.spawn(cmd)
                            egg.logfile = FileAdapter(logg)
                            time.sleep(2)
                            logged_in_9800 = False
                            found_escape = False

                    if i == 1:
                        logg.info("9800 found {}  will elevate loging i:{} before {} after {}".format(CCP, i, egg.before, egg.after))
                        egg.sendline("en")
                        sleep(0.1)
                        j = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                        if j == 0:
                            logg.info("9800 received password prompt will send password: {} i:{} j:{} before {} after {}".format(args.passwd, i, j, egg.before, egg.after))
                            egg.sendline(args.passwd)
                            sleep(0.1)
                            k = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("9800 SSH Successfully received # prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                                logged_in_9800 = True
                            if k == 1:
                                logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 1:
                            logg.info("8900 received timeout after looking for password: prompt  i:{} j:{} k:{}  before {} after {}".format(i, j, k, egg.before, egg.after))

                    if i == 2:
                        logg.info("9800 found {} This implies in incorrect logout or killed prior run test i:{} before {} after {}".format(CCP_EN, i, egg.before, egg.after))
                        logged_in_9800 = True

                    if i == 3:
                        logg.info("9800 found User will put in args.user {} i:{} j:{} before {} after {}".format(args.user, i, j, egg.before, egg.after))
                        egg.sendline(args.user)
                        sleep(0.1)
                        j = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                        if j == 0:
                            logg.info("9800 received password prompt after sending User, sending password: {} i:{} j:{} before {} after {}".format(args.passwd, i, k, egg.before, egg.after))
                            egg.sendline(args.passwd)
                            sleep(0.1)
                            l = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("9800 SSH Successfully received # prompt i:{} j:{} k:{}".format(i, j, k))
                                logged_in_9800 = True
                            if k == 1:
                                logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 1:
                            logg.info("9800 received timeout after looking for password after sending user i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))

                    if i == 4:
                        logg.info("9800 received password prompt will send password: {} i:{} before {} after {}".format(args.passwd, i, egg.before, egg.after))
                        egg.sendline(args.passwd)
                        sleep(0.1)
                        j = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                        if j == 0:
                            logg.info("9800 SSH Successfully received # prompt i:{} j:{} before {} after {}".format(i, j, egg.before, egg.after))
                            logged_in_9800 = True
                        if j == 1:
                            logg.info("9800 Timed out waiting for # prompt i:{} j:{} before {} after {}".format(i, j, egg.before, egg.after))

                    if i == 5:
                        logg.info("9800 received {} prompt doing some cleanup".format(CCP_CONFIG))
                        egg.sendline("exit")
                        sleep(0.1)
                        j = egg.expect_exact([CCP, CCP_EN, "User:", "Password:", pexpect.TIMEOUT], timeout=timeout)
                        sleep(0.1)
                        if j == 0:
                            logg.info("9800 found {}  will elevate loging i:{} j:{} before {} after {}".format(CCP, i, j, egg.before, egg.after))
                            egg.sendline("en")
                            sleep(0.1)
                            k = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("9800 received password prompt will send password: {}  i:{} j:{} k:{} before {} after {}".format(args.passwd, i, j, k, egg.before, egg.after))
                                egg.sendline(args.passwd)
                                sleep(0.1)
                                l = egg.expect_exact([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                                if l == 0:
                                    logg.info("9800 SSH Successfully received # prompt i:{} j:{} k:{} l:{}".format(i, j, k, l))
                                    logged_in_9800 = True
                                if l == 1:
                                    logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                            if k == 1:
                                logg.info("8900 received timeout after looking for password: prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 1:
                            logg.info("9800 found # so logged in can start sending commands i:{} j:{}".format(i, j))
                            logged_in_9800 = True
                        if j == 2:
                            logg.info("9800 found User: will put in args.user {}  i:{} j:{}".format(args.user, i, j))
                            egg.sendline(args.user)
                            sleep(0.1)
                            k = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("9800 received password prompt after sending User, sending password: {} i:{} j:{} k:{}".format(args.passwd, i, j, k))
                                egg.sendline(args.passwd)
                                sleep(0.1)
                                l = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                                if l == 0:
                                    logg.info("9800 SSH Successfully received # prompt i:{} j:{} k:{} l:{}".format(i, j, k, l))
                                    logged_in_9800 = True
                                if l == 1:
                                    logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                            if k == 1:
                                logg.info("9800 received timeout after looking for password after sending user i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 3:
                            sleep(0.1)
                            logg.info("9800 received Password prompt will send password {} i:{} j:{}  before {} after {}".format(args.passwd, i, j, egg.before, egg.after))
                            egg.sendline(args.passwd)
                            sleep(0.1)
                            k = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("8900 SSH Successfully received # prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                                logged_in_9800 = True
                            if k == 1:
                                logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 4:
                            logg.info("9800 timed out looking {}, {}, User:, Password:  i:{} j:{} before {} after {}".format(CCP, CCP_EN, i, j, egg.before, egg.after))
                            logg.info("9800 Timed out waiting for initial prompt send logout loop_count: {} i: {} j: {} before {} after {}".format(loop_count, i, j, egg.before, egg.after))
                            logg.info("9800  Closing the connection and try to re-establish, ")
                            egg.close(force=True)
                            sleep(1)
                            egg.close(force=True)
                            sleep(1)

                            # re establish ssh
                            cmd = "ssh -p%d %s@%s" % (port, user, host)
                            logg.info("Spawn: " + cmd + NL)
                            egg = pexpect.spawn(cmd)
                            egg.logfile = FileAdapter(logg)
                            time.sleep(2)
                            logged_in_9800 = False
                            found_escape = False
                    if i == 6:
                        logg.info("9800 recieved Bad secrets, to many password attempts i: {} before {} after {}".format(i, egg.before, egg.after))
                        egg.sendline(CR)
                        sleep(0.2)
                    if i == 7:
                        logg.info("9800 recieved Are you sure you want to continue connecting (yes/no/[fingerprint])? i: {} before {} after {}".format(i, egg.before, egg.after))
                        egg.sendline('yes')
                        sleep(0.2)
                    if i == 8:
                        logg.info("9800 Timed out waiting for initial prompt send logout loop_count: {} i: {} before {} after {}".format(loop_count, i, egg.before, egg.after))
                        logg.info("9800  Closing the connection and try to re-establish, ")
                        egg.close(force=True)
                        sleep(1)
                        egg.close(force=True)
                        sleep(1)

                        # re establish ssh
                        cmd = "ssh -p%d %s@%s" % (port, user, host)
                        logg.info("Spawn: " + cmd + NL)
                        egg = pexpect.spawn(cmd)
                        egg.logfile = FileAdapter(logg)
                        time.sleep(2)
                        logged_in_9800 = False
                        found_escape = False

                if loop_count >= 6:
                    if found_escape == True:
                        logg.info("9800 initial prompt and log messages interfering")
                        logg.info("9800 will send escape to close telnet")
                        egg.close(force=True)
                        exit(1)
                    else:
                        logg.info("9800 the telnet session may need to be cleared will try to send logout")
                        egg.sendline("logout")
                        logg.info("9800 did not find the initial escape... exiting")
                        egg.close(force=True)
                        exit(1)

            # 3504 series
            else:
                i = egg.expect(["ssword:", "continue connecting (yes/no)?"], timeout=timeout)
                time.sleep(0.1)
                if i == 1:
                    egg.sendline('yes')
                    sleep(0.1)
                    egg.expect('ssword:')
                sleep(0.1)
                egg.sendline(passwd)
                sleep(0.1)

        elif (scheme == "telnet"):
            sleep(1)
            if (port is None):
                port = 23
            cmd = "telnet %s %d" % (host, port)
            logg.info("Spawn: " + cmd + NL)
            egg = pexpect.spawn(cmd)
            egg.logfile = FileAdapter(logg)
            time.sleep(2)
            logged_in_9800 = False
            loop_count = 0
            found_escape = False
            CONFIG_I = "%SYS-5-CONFIG_I: Configured from console by console"
            PRESS_RETURN = "Press RETURN to get started."

            # 9800 series
            if args.series == "9800":
                while logged_in_9800 == False and loop_count <= 7:
                    loop_count += 1
                    logg.info("9800 loop_count {}".format(loop_count))
                    # logg.info("9800 establishing Telnet egg {} ".format(egg))
                    # sleep(2)
                    egg.sendline(CR)
                    sleep(0.4)
                    try:
                        i = egg.expect_exact(["Escape character is '^]'.", CCP, CCP_EN, "Username:", "Password:", CCP_CONFIG, "Bad secrets", PRESS_RETURN, CONFIG_I, pexpect.TIMEOUT],
                                             timeout=timeout)
                    except Exception as e:
                        logg.info('AP connection failed. or refused Connection open by other process')
                        logg.exception(e)
                        exit(1)

                    if i == 0:
                        logg.info("9800 found Escape character is '^] i:{} before: {} after: {}".format(i, egg.before, egg.after))
                        egg.sendline(CR)
                        found_escape = True
                        sleep(0.2)
                        j = egg.expect_exact([CCP, CCP_EN, "User:", "Password:", CCP_CONFIG, pexpect.TIMEOUT], timeout=timeout)
                        sleep(0.1)
                        if j == 0:
                            logg.info("9800 found {} will elevate loging i:{} j:{} before {} after {}".format(CCP, i, j, egg.before, egg.after))
                            egg.sendline("en")
                            sleep(0.1)
                            k = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("9800 received password prompt will send password: {} i:{} j:{} k:{} before {} after {}".format(args.passwd, i, j, k, egg.before, egg.after))
                                egg.sendline(args.passwd)
                                sleep(0.1)
                                l = egg.expect_exact([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                                if l == 0:
                                    logg.info("9800 TELNET Successfully received {} prompt i:{} j:{} k:{} l:{}".format(CCP_EN, i, j, k, l))
                                    logged_in_9800 = True
                                if l == 1:
                                    logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                            if k == 1:
                                logg.info("8900 received timeout after looking for password: prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 1:
                            logg.info("9800 found # so logged in can start sending commands i:{} j:{}".format(i, j))
                            logged_in_9800 = True
                        if j == 2:
                            logg.info("9800 found User: will put in args.user {} i:{} j:{}".format(args.user, i, j))
                            egg.sendline(args.user)
                            sleep(0.1)
                            k = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("9800 received password prompt after sending User, sending password: {} i:{} j:{} k:{}".format(args.passwd, i, j, k))
                                egg.sendline(args.passwd)
                                sleep(0.1)
                                l = egg.expect_exact([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                                if l == 0:
                                    logg.info("9800 TELNET Successfully received # prompt i:{} j:{} k:{} l:{}".format(i, j, k, l))
                                    logged_in_9800 = True
                                if l == 1:
                                    logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                            if k == 1:
                                logg.info("9800 received timeout after looking for password after sending user i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 3:
                            sleep(0.1)
                            logg.info("9800 received Password prompt will send password {} i:{} j:{} before {} after {}".format(args.passwd, i, j, egg.before, egg.after))
                            egg.sendline(args.passwd)
                            sleep(0.1)
                            k = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("9800 TELNET Successfully received # prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                                logged_in_9800 = True
                            if k == 1:
                                logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 4:
                            logg.info("9800 received {} prompt doing some cleanup i = {} j = {}".format(CCP_CONFIG, i, j))
                            egg.sendline("end")
                            sleep(0.1)
                            k = egg.expect_exact([CCP, CCP_EN, "User:", "Password:", pexpect.TIMEOUT], timeout=timeout)
                            sleep(0.1)
                            if k == 0:
                                logg.info("9800 found {} will elevate loging i:{} j:{} k:{} before {} after {}".format(CCP, i, j, k, egg.before, egg.after))
                                egg.sendline("en")
                                sleep(0.1)
                                l = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                                if l == 0:
                                    logg.info("9800 received password prompt will send password: {}  i:{} j:{} k:{} l:{} before {} after {}".format(args.passwd, i, j, k, l, egg.before, egg.after))
                                    egg.sendline(args.passwd)
                                    sleep(0.1)
                                    m = egg.expect_exact([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                                    if m == 0:
                                        logg.info("9800 TELNET Successfully received # prompt i:{} j:{} k:{} l:{} m:{}".format(i, j, k, l, m))
                                        logged_in_9800 = True
                                    if m == 1:
                                        logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} l:{} m:{} before {} after {}".format(i, j, k, l, m, egg.before, egg.after))
                                if l == 1:
                                    logg.info("8900 received timeout after looking for password: prompt i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                            if k == 1:
                                logg.info("9800 found # so logged in can start sending commands i:{} j:{} k:{}".format(i, j, k))
                                logged_in_9800 = True
                            if k == 2:
                                logg.info("9800 found User: will put in args.user {}  i:{} j:{} k:{}".format(args.user, i, j, k))
                                egg.sendline(args.user)
                                sleep(0.1)
                                l = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                                if l == 0:
                                    logg.info("9800 received password prompt after sending User, sending password: {} i:{} j:{} k:{} l:{}".format(args.passwd, i, j, k, l))
                                    egg.sendline(args.passwd)
                                    sleep(0.1)
                                    m = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                                    if m == 0:
                                        logg.info("9800 TELNET Successfully received # prompt i:{} j:{} k:{} l:{} m:{}".format(i, j, k, l, m))
                                        logged_in_9800 = True
                                    if m == 1:
                                        logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} l:{} m:{} before {} after {}".format(i, j, k, l, m, egg.before, egg.after))
                                if l == 1:
                                    logg.info("9800 received timeout after looking for password after sending user i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                            if k == 3:
                                sleep(0.1)
                                logg.info("9800 received Password prompt will send password {} i:{} j:{} k:{}  before {} after {}".format(args.passwd, i, j, k, egg.before, egg.after))
                                egg.sendline(args.passwd)
                                sleep(0.1)
                                l = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                                if l == 0:
                                    logg.info("9800 TELNET Successfully received # prompt i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                                    logged_in_9800 = True
                                if l == 1:
                                    logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                            if k == 4:
                                logg.info("9800 timed out looking {}, {}, User:, Password:  i:{} j:{} k:{} before {} after {}".format(CCP, CCP_EN, i, j, k, egg.before, egg.after))
                                logg.info("9800 Timed out waiting for initial prompt send logout loop_count: {} i: {} j: {} k:{} before {} after {}".format(loop_count, i, j, k, egg.before, egg.after))
                                logg.info("9800  Closing the connection and try to re-establish, ")
                                egg.close(force=True)
                                sleep(1)
                                egg.close(force=True)
                                sleep(1)

                                # re establish telnet
                                cmd = "telnet %s %d" % (host, port)
                                logg.info("Spawn: " + cmd + NL)
                                egg = pexpect.spawn(cmd)
                                egg.logfile = FileAdapter(logg)
                                time.sleep(2)
                                logged_in_9800 = False
                                found_escape = False

                        if j == 5:
                            logg.info("9800 timed out looking for {}, {},User:,Password: loop_count {} i {} j {}  before {} after {}".format(CCP, CCP_EN, loop_count, i, j, egg.before, egg.after))
                            logg.info("9800  Closing the connection and try to re-establish loop_count {} i {} j {}".format(loop_count, i, j))
                            egg.close(force=True)
                            sleep(1)
                            egg.close(force=True)
                            sleep(1)
                            # re establish telnet
                            cmd = "telnet %s %d" % (host, port)
                            logg.info("Spawn: " + cmd + NL)
                            egg = pexpect.spawn(cmd)
                            egg.logfile = FileAdapter(logg)
                            time.sleep(2)
                            logged_in_9800 = False
                            found_escape = False

                    if i == 1:
                        logg.info("9800 found {} will elevate loging i:{} before {} after {}".format(CCP, i, egg.before, egg.after))
                        egg.sendline("en")
                        sleep(0.1)
                        j = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                        if j == 0:
                            logg.info("9800 received password prompt will send password: {} i:{} j:{} before {} after {}".format(args.passwd, i, j, egg.before, egg.after))
                            egg.sendline(args.passwd)
                            sleep(0.1)
                            k = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("9800 TELNET Successfully received # prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                                logged_in_9800 = True
                            if k == 1:
                                logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 1:
                            logg.info("8900 received timeout after looking for password: prompt  i:{} j:{} k:{}  before {} after {}".format(i, j, k, egg.before, egg.after))

                    if i == 2:
                        logg.info("9800 found {} This implies in incorrect logout or killed prior run test i:{} before {} after {}".format(CCP_EN, i, egg.before, egg.after))
                        logged_in_9800 = True

                    if i == 3:
                        logg.info("9800 found User will put in args.user {} i:{} j:{} before {} after {}".format(args.user, i, j, egg.before, egg.after))
                        egg.sendline(args.user)
                        sleep(0.1)
                        j = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                        if j == 0:
                            logg.info("9800 received password prompt after sending User, sending password: {} i:{} j:{} before {} after {}".format(args.passwd, i, j, egg.before, egg.after))
                            egg.sendline(args.passwd)
                            sleep(0.1)
                            l = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("9800 TELNET Successfully received # prompt i:{} j:{} k:{}".format(i, j, k))
                                logged_in_9800 = True
                            if k == 1:
                                logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 1:
                            logg.info("9800 received timeout after looking for password after sending user i:{} j:{} before {} after {}".format(i, j, egg.before, egg.after))

                    if i == 4:
                        logg.info("9800 received password prompt will send password: {}   i:{}  before {} after {}".format(args.passwd, i, egg.before, egg.after))
                        egg.sendline(args.passwd)
                        sleep(0.1)
                        j = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                        if j == 0:
                            logg.info("9800 TELNET Successfully received # prompt i:{} j:{} before {} after {}".format(i, j, egg.before, egg.after))
                            logged_in_9800 = True
                        if j == 1:
                            logg.info("9800 Timed out waiting for # prompt i:{} j:{} before {} after {}".format(i, j, egg.before, egg.after))

                    if i == 5:
                        logg.info("9800 received {} prompt doing some cleanup".format(CCP_CONFIG))
                        egg.sendline("end")
                        sleep(0.3)
                        j = egg.expect_exact([CCP, CCP_EN, "User:", "Password:", pexpect.TIMEOUT], timeout=timeout)
                        sleep(0.1)
                        if j == 0:
                            logg.info("9800 found {} will elevate loging i:{} j:{} before {} after {}".format(CCP, i, j, egg.before, egg.after))
                            egg.sendline("en")
                            sleep(0.1)
                            k = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("9800 received password prompt will send password: {}  i:{} j:{} k:{} before {} after {}".format(args.passwd, i, j, k, egg.before, egg.after))
                                egg.sendline(args.passwd)
                                sleep(0.1)
                                l = egg.expect_exact([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                                if l == 0:
                                    logg.info("9800 TELNET Successfully received # prompt i:{} j:{} k:{} l:{}".format(i, j, k, l))
                                    logged_in_9800 = True
                                if l == 1:
                                    logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                            if k == 1:
                                logg.info("8900 received timeout after looking for password: prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 1:
                            logg.info("9800 found # so logged in can start sending commands i:{} j:{}".format(i, j))
                            logged_in_9800 = True
                        if j == 2:
                            logg.info("9800 found User: will put in args.user {}  i:{} j:{}".format(args.user, i, j))
                            egg.sendline(args.user)
                            sleep(0.1)
                            k = egg.expect_exact(["Password:", pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("9800 received password prompt after sending User, sending password: {} i:{} j:{} k:{}".format(args.passwd, i, j, k))
                                egg.sendline(args.passwd)
                                sleep(0.1)
                                l = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                                if l == 0:
                                    logg.info("9800 TELNET Successfully received # prompt i:{} j:{} k:{} l:{}".format(i, j, k, l))
                                    logged_in_9800 = True
                                if l == 1:
                                    logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} l:{} before {} after {}".format(i, j, k, l, egg.before, egg.after))
                            if k == 1:
                                logg.info("9800 received timeout after looking for password after sending user i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 3:
                            sleep(0.1)
                            logg.info("9800 received Password prompt will send password {} i:{} j:{}  before {} after {}".format(args.passwd, i, j, egg.before, egg.after))
                            egg.sendline(args.passwd)
                            sleep(0.1)
                            k = egg.expect([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                            if k == 0:
                                logg.info("9800 TELNET Successfully received # prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                                logged_in_9800 = True
                            if k == 1:
                                logg.info("9800 Timed out waiting for # prompt i:{} j:{} k:{} before {} after {}".format(i, j, k, egg.before, egg.after))
                        if j == 4:
                            logg.info("9800 timed out looking {}, {}, User:, Password:  i:{} j:{} before {} after {}".format(CCP, CCP_EN, i, j, egg.before, egg.after))
                            logg.info("9800 Timed out waiting for initial prompt send logout loop_count: {} i: {} j: {} before {} after {}".format(loop_count, i, j, egg.before, egg.after))
                            logg.info("9800  Closing the connection and try to re-establish, ")
                            egg.close(force=True)
                            sleep(1)
                            egg.close(force=True)
                            sleep(1)

                            # re establish telnet
                            cmd = "telnet %s %d" % (host, port)
                            logg.info("Spawn: " + cmd + NL)
                            egg = pexpect.spawn(cmd)
                            egg.logfile = FileAdapter(logg)
                            time.sleep(2)
                            logged_in_9800 = False
                            found_escape = False
                    if i == 6:
                        logg.info("9800 recieved Bad secrets, to many password attempts i: {} before {} after {}".format(i, egg.before, egg.after))
                        egg.sendline(CR)
                        sleep(0.2)
                    if i == 7:
                        logg.info("9800 received: {}  i: {} before {} after {}  send cr".format(PRESS_RETURN, i, egg.before, egg.after))
                        egg.sentline(CR)
                        sleep(0.2)
                    if i == 8:
                        logg.info("9800 received: {} i: {} before {} after {} send cr".format(CONFIG_I, i, egg.before, egg.after))
                        egg.sentline(CR)
                        sleep(0.2)
                    if i == 9:
                        logg.info(
                            "9800 Timed out waiting for initial prompt, Log message from controller interfering with expected prompts loop_count: {} i: {} before {} after {}".format(
                                loop_count,
                                i,
                                egg.before,
                                egg.after))
                        logg.info("9800  Closing the connection and try to re-establish, ")
                        egg.close(force=True)
                        sleep(1)
                        egg.close(force=True)
                        sleep(1)

                        # re establish telnet
                        cmd = "telnet %s %d" % (host, port)
                        logg.info("Spawn: " + cmd + NL)
                        egg = pexpect.spawn(cmd)
                        egg.logfile = FileAdapter(logg)
                        time.sleep(2)
                        logged_in_9800 = False
                        found_escape = False

                if loop_count >= 8:
                    if found_escape == True:
                        logg.info("9800 outside major loop loop_count {}".format(loop_count))
                        logg.info("9800 will look one more time for {}".format(CCP_EN))
                        egg.sentline(CR)
                        sleep(0.2)
                        r = egg.expect_exact([CCP_EN, pexpect.TIMEOUT], timeout=timeout)
                        if r == 0:
                            logg.info("Found {} r {} before {}  after {} can move forward".format(CCP_EN, r, egg.before, egg.after))
                        if r == 1:
                            egg.sendline("\x1b\r")
                            egg.sendline("logout")
                            logg.info("9800 the excape was found yet could not loging... close egg session")
                            egg.close(force=True)
                            exit(1)
                    else:
                        logg.info("9800 the telnet session may need to be cleared will try to send logout")
                        egg.sendline("logout")
                        logg.info("9800 did not find the initial escape... exiting")
                        egg.close(force=True)
                        exit(1)

            # 3504 series
            else:
                egg.sendline(' ')
                egg.expect('User\\:', timeout=3)
                egg.sendline(user)
                egg.expect('Password\\:', timeout=3)
                egg.sendline(passwd)
                # if args.prompt in CCP_EN or args.prompt in CCP:
                #   egg.sendline("enable")
                #   time.sleep(0.1)
                egg.sendline('config paging disable')
                # egg.expect('(Voice-Talwar) >', timeout=3)
                # time.sleep(0.1)
                # egg.sendline(user)
                # time.sleep(0.1)
                # egg.expect('ssword:')
                # time.sleep(0.1)
                # egg.sendline(passwd)
        else:
            usage()
            exit(1)
    except Exception as e:
        logging.exception(e)

    command = None
    time.sleep(0.1)

    sleep(0.1)
    if args.series == "9800":
        pass
    else:
        # TODO  clean up
        logg.info("waiting for prompt: {}".format(CCPROMPT))
        egg.expect(">", timeout=3)

    logg.info("Command to Process :: Ap[%s] Action[%s] Value[%s] " % (args.ap, args.action, args.value))
    print("Ap[%s] Action[%s] Value[%s]" % (args.ap, args.action, args.value))

    if ((args.action == "show") and (args.value is None)):
        raise Exception("show requires value, like 'country' or 'ap summary'")

    if (args.action == "show"):
        command = "show " + args.value

    if (args.action == "cmd"):
        if (args.value is None):
            raise Exception("cmd requires value to be set.")
        command = "%s" % (args.value)

    # TODO add
    # show controllers dot11Radio 0
    # show controllers dot11Radio 0 wlan
    # if (args.action == "show_radio"):
    #    command = "show controllers dot11Radio 0 wlan"

    if (args.action == "show_ap_wlan_summary"):
        if args.series == "9800":
            command = "show ap wlan summary"
        else:
            # untested on 3504
            command = "show ap wlan summary"

    if (args.action == "summary"):
        command = "show ap summary"

    if (args.action == "show_ap_status"):
        command = "show ap status"

    if (args.action == "show_ap_name_config_role"):
        command = "show ap name %s config slot %s | inc Role" % (args.ap, args.ap_band_slot)

    if (args.action == "show_ap_tx_power_config"):
        command = "show ap name %s config dot11 %s | sec Tx" % (args.ap, config_band)


    if (args.action == "advanced"):
        if args.series == "9800":
            if band == 'dual_band_5g' or band == 'dual_band_6g':
                command = "show ap dot11 dual-band summary"
            elif band == '6g':
                command = "show ap dot11 6ghz summary"
            elif band == '5g':
                command = "show ap dot11 5ghz summary"
            else:
                command = "show ap dot11 24ghz summary"
        else:
            command = "show advanced 802.11%s summary" % (band)

    if (args.action == "show_ap_bssid_24g"):
        if args.series == "9800":
            command = "show ap name %s wlan dot11 24ghz" % (args.ap)

    if (args.action == "show_ap_bssid_5g"):
        if args.series == "9800":
            command = "show ap name %s wlan dot11 5ghz" % (args.ap)

    if (args.action == "show_ap_bssid_dual_band_6g" or args.action == "show_ap_bssid_dual_band_5g"):
        if args.series == "9800":
            command = "show ap name %s wlan dot11 dual-band" % (args.ap)

    if (args.action == "show_ap_bssid_6g"):
        if args.series == "9800":
            command = "show ap name %s wlan dot11 6ghz" % (args.ap)

    if (args.action == "show_wireless_client_sumry"):
        if args.series == "9800":
            command = "show  wireless client summary"

    if (args.action == 'show_client_macadd_detail'):
        print("args.value", args.value)
        if args.series == "9800":
            command = "show wireless client mac-address %s  detail" % (args.value)

    if (args.action == 'debug_wieless_mac'):
        print("args.value", args.value)
        if args.series == "9800":
            command = "debug wireless mac %s" % (args.value)

    if (args.action == 'no_debug_wieless_mac'):
        print("args.value", args.value)
        if args.series == "9800":
            command = "no debug wireless mac  %s" % (args.value)

    if (args.action == 'get_ra_trace_files'):
        if args.series == "9800":
            command = "dir bootflash: | i ra_trace"

    if (args.action == 'del_ra_trace_file'):
        print("args.value", args.value)
        if args.series == "9800":
            command = "delete /force bootflash:%s" % (args.value)

    if (args.action == 'get_data_ra_trace_files'):
        print("args.value", args.value)
        if args.series == "9800":
            command = "more bootflash:%s" % (args.value)


    if ((args.action == "auto_rf") and ((args.ap is None))):
        raise Exception("auto_rf requires AP name")

    if (args.action == "auto_rf"):
        command = "show ap auto-rf 802.11a %s" % (args.ap)
        egg.sendline(command)
        command_done = False
        loop_count = 0
        while command_done == False and loop_count <= 10:
            i = egg.expect_exact(["--More--", CCP, pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                print(egg.before.decode('utf-8', 'ignore'))
                egg.send(SEND_MORE)
            if i == 1:
                print(egg.before.decode('utf-8', 'ignore'))
                command_done = True
            if i == 2:
                print(egg.before.decode('utf-8', 'ignore'))
                command_done = True
        command = None  # so additional command will not be sent

    if ((args.action == "ap_country") and ((args.value is None) or (args.ap is None))):
        raise Exception("ap_country requires country and AP name")

    if (args.action == "ap_country"):
        command = "config ap country %s %s" % (args.value, args.ap)

    if ((args.action == "country") and ((args.value is None))):
        raise Exception("country requires country value")

    if (args.action == "country"):
        command = "config country %s" % (args.value)

    if (args.action == "ap_dot11_dot11ax_mcs_tx_index_spatial_stream" and (args.spatial_stream is None or args.mcs_tx_index is None)):
        raise Exception("action requires spatial_stream and mcs_tx_index to be set: {action}".format(action=action))
    if (args.action == "ap_dot11_dot11ax_mcs_tx_index_spatial_stream"):
        if args.series == "9800":
            if (args.band == '6g' or args.band == 'dual_band_6g'):
                command = "ap dot11 6ghz dot11ax mcs tx index {index} spatial-stream {stream}".format(index=args.mcs_tx_index,stream=args.spatial_stream)
            elif (args.band == '5g' or args.band == 'dual_band_5g'):
                command = "ap dot11 5ghz dot11ax mcs tx index {index} spatial-stream {stream}".format(index=args.mcs_tx_index,stream=args.spatial_stream)
            elif (args.band == '24g'):
                command = "ap dot11 24ghz dot11ax mcs tx index {index} spatial-stream {stream}".format(index=args.mcs_tx_index,stream=args.spatial_stream)

            egg.sendline("config t")
            sleep(0.1)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                egg.sendline(command)
                sleep(0.1)
            if i == 1:
                logg.info("timed out on (config)# command: {command}".format(command=command))

    if (args.action == "no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream" and (args.spatial_stream is None or args.mcs_tx_index is None)):
        raise Exception("action requires spatial_stream and mcs_tx_index to be set: {action}".format(action=action))
    if (args.action == "no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream"):
        if args.series == "9800":
            if (args.band == '6g' or args.band == 'dual_band_6g'):
                command = "no ap dot11 6ghz dot11ax mcs tx index {index} spatial-stream {stream}".format(index=args.mcs_tx_index,stream=args.spatial_stream)
            elif (args.band == '5g' or args.band == 'dual_band_5g'):
                command = "no ap dot11 5ghz dot11ax mcs tx index {index} spatial-stream {stream}".format(index=args.mcs_tx_index,stream=args.spatial_stream)
            elif (args.band == '24g'):
                command = "no ap dot11 24ghz dot11ax mcs tx index {index} spatial-stream {stream}".format(index=args.mcs_tx_index,stream=args.spatial_stream)

            egg.sendline("config t")
            sleep(0.1)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                egg.sendline(command)
                sleep(0.1)
            if i == 1:
                logg.info("timed out on (config)# command: {command}".format(command=command))

    if (args.action == "manual" and args.ap is None):
        raise Exception("action requires AP name")
    if (args.action == "manual"):
        if args.series == "9800":
            if band == "dual_band_6g" or band == "dual_band_5g":
                command = "ap name %s dot11 dual-band slot %s role manual client-serving" % (args.ap, args.ap_band_slot)
            elif band == "6g":
                command = "ap name %s dot11 6ghz slot %s radio role manual client-serving" % (args.ap, args.ap_band_slot)
            elif band == '5g':
                command = "ap name %s dot11 5ghz slot %s radio role manual client-serving" % (args.ap, args.ap_band_slot)
            else:
                command = "ap name %s dot11 24ghz slot %s radio role manual client-serving" % (args.ap, args.ap_band_slot)

    if (args.action == "auto" and args.ap is None):
        raise Exception("action requires AP name")
    if (args.action == "auto"):
        if args.series == "9800":
            if band == "dual_band_6g" or band == "dual_band_5g":
                command = "ap name %s dot11 dual-band slot %s radio role auto" % (args.ap, args.ap_band_slot)
            elif band == "6g":
                command = "ap name %s dot11 6ghz slot %s radio role auto" % (args.ap, args.ap_band_slot)
            elif band == '5g':
                command = "ap name %s dot11 5ghz slot %s radio role auto" % (args.ap, args.ap_band_slot)
            else:
                command = "ap name %s dot11 24ghz slot %s radio role auto" % (args.ap, args.ap_band_slot)

    if (args.action == "disable_network_dual_band_5ghz" or args.action == 'disable_network_dual_band_6ghz'):
        if args.series == "9800":
            command = "ap name %s dot11 dual-band slot %s shutdown" % (args.ap, args.ap_band_slot) 
            egg.sendline(command)
            sleep(0.1)
            i = egg.expect_exact(["Are you sure you want to continue? (y/n)[y]:", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                logg.info("did get Are you sure you want to continue? (y/n)[y]:")
                egg.sendline("y")
                sleep(0.5)
            if i == 1:
                logg.info("did not get Are you sure you want to continue? (y/n)[y]:")
                egg.sendline("y")
                sleep(0.5)

    
    if (args.action == "disable_network_6ghz"):
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.1)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                command = "ap dot11 6ghz shutdown"
                egg.sendline(command)
                sleep(0.1)
                i = egg.expect_exact(["Are you sure you want to continue? (y/n)[y]:", pexpect.TIMEOUT], timeout=timeout)
                if j == 0:
                    logg.info("did get Are you sure you want to continue? (y/n)[y]:")
                    egg.sendline("y")
                    sleep(0.5)
                if j == 1:
                    logg.info("did not get Are you sure you want to continue? (y/n)[y]:")
                    egg.sendline("y")
                    sleep(0.5)
            if i == 1:
                logg.info("timed out on (config)# disable_network_6ghz")

    if (args.action == "disable_network_5ghz"):
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.1)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                egg.sendline("ap dot11 5ghz shutdown")
                sleep(0.1)
                i = egg.expect_exact(["Are you sure you want to continue? (y/n)[y]:", pexpect.TIMEOUT], timeout=timeout)
                if j == 0:
                    logg.info("did get Are you sure you want to continue? (y/n)[y]:")
                    egg.sendline("y")
                    sleep(0.5)
                if j == 1:
                    logg.info("did not get Are you sure you want to continue? (y/n)[y]:")
                    egg.sendline("y")
                    sleep(0.5)
            if i == 1:
                logg.info("timed out on (config)# disable_network_5ghz")
        # 3504
        else:
            logg.info("3504 disable_network_5ghz")
            command = 'config 802.11a disable network'

    if (args.action == "disable_network_24ghz"):
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.1)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                egg.sendline("ap dot11 24ghz shutdown")
                sleep(0.5)
                i = egg.expect_exact(["Are you sure you want to continue? (y/n)[y]:", pexpect.TIMEOUT], timeout=timeout)
                if j == 0:
                    logg.info("did get Are you sure you want to continue? (y/n)[y]:")
                    egg.sendline("y")
                    sleep(0.5)
                if j == 1:
                    logg.info("did not get Are you sure you want to continue? (y/n)[y]:")
                    egg.sendline("y")
                    sleep(0.5)
            if i == 1:
                logg.info("timed out on (config)# disable_network_24ghz")
        # 3504
        else:
            logg.info("3504 disable_network_24ghz")
            command = 'config 802.11a disable network'

    if (args.action == "enable_network_dual_band_5ghz" or args.action == "enable_network_dual_band_6ghz"):
        if args.series == "9800":
            command = "ap name %s no dot11 dual-band slot %s shutdown" % (args.ap, args.ap_band_slot) 

    if (args.action == "enable_network_6ghz"):
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.1)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                egg.sendline("no ap dot11 6ghz shutdown")
                sleep(0.1)
            if i == 1:
                logg.info("timed out on (config) prompt")

    if (args.action == "enable_network_5ghz"):
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.1)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                egg.sendline("no ap dot11 5ghz shutdown")
                sleep(0.1)
            if i == 1:
                logg.info("timed out on (config) prompt")
        else:
            logg.info("3504 enable_network_5ghz")
            command = "config 802.11a enable network"

    if (args.action == "enable_network_24ghz"):
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.1)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                egg.sendline("no ap dot11 24ghz shutdown")
                sleep(0.1)
            if i == 1:
                logg.info("timed out on (config) prompt")
        else:
            logg.info("3504 enable_network_24ghz")
            command = "config 802.11b enable network"


    # This will shut down the dual band 

    # for dual-band 6g
    # ap name CM66 dot11 dual-band shutdown    
    # ap name CM66 dot11 dual-band slot 2 band 6ghz 
    # ap name CM66 no dot11 dual-band shutdown 

    # for dual-band 5g
    # ap name CM66 dot11 dual-band shutdown    
    # ap name CM66 dot11 dual-band slot 2 band 5ghz 
    # ap name CM66 no dot11 dual-band shutdown 

    # shutdown dual-band mode
    if (args.action == "dual_band_mode_shutdown" and (args.ap is None or args.ap_band_slot is None)):
        raise Exception("action requires AP name and ap band slot")
    if (args.action == "dual_band_mode_shutdown"):
        logg.info("command: ap name %s dot11 dual-band shutdown , slot %s : %s " % (args.ap, args.ap_band_slot, band))

        if args.series == "9800":
            if band == "dual_band_6g":
                command = "ap name %s dot11 dual-band shutdown" % (args.ap)
            elif band == "dual_band_5g":
                command = "ap name %s dot11 dual-band shutdown" % (args.ap)

    # shutdown dual-band mode
    if (args.action == "dual_band_no_mode_shutdown" and (args.ap is None or args.ap_band_slot is None)):
        raise Exception("action requires AP name and ap band slot")
    if (args.action == "dual_band_no_mode_shutdown"):
        logg.info("command: ap name %s no dot11 dual-band shutdown , slot %s : %s " % (args.ap, args.ap_band_slot, band))

        if args.series == "9800":
            if band == "dual_band_6g":
                command = "ap name %s no dot11 dual-band shutdown" % (args.ap)
            elif band == "dual_band_5g":
                command = "ap name %s no dot11 dual-band shutdown" % (args.ap)


    # configure the dual band mode 
    if (args.action == "config_dual_band_mode" and (args.ap is None or args.ap_band_slot is None)):
        raise Exception("action requires AP name and ap band slot")
    if (args.action == "config_dual_band_mode"):
        logg.info("send command to set the dual band mode : ap name %s no dot11 dual-ban slot %s : %s " % (args.ap, args.ap_band_slot, band))

        if args.series == "9800":
            if band == "dual_band_6g":
                command = "ap name %s dot11 dual-band slot %s band 6ghz" % (args.ap, args.ap_band_slot)
            elif band == "dual_band_5g":
                command = "ap name %s dot11 dual-band slot %s band 5ghz" % (args.ap, args.ap_band_slot)
            

    # This will take the operation status down 
    if (args.action == "enable_operation_status" and (args.ap is None)):
        raise Exception("action requires AP name")
    if (args.action == "enable_operation_status"):
        logg.info("send command to enable operation status: ap name %s no dot11 %shz slot %s shutdown" % (args.ap, band, args.ap_band_slot))

        if args.series == "9800":
            if band == "dual_band_6g" or band == "dual_band_5g":
                command = "ap name %s no dot11 dual-band slot %s shutdown" % (args.ap, args.ap_band_slot)
            elif band == "6g":
                command = "ap name %s no dot11 6ghz slot %s shutdown" % (args.ap, args.ap_band_slot)
            elif band == '5g':
                command = "ap name %s no dot11 5ghz slot %s shutdown" % (args.ap, args.ap_band_slot)
            elif band == '24g':
                command = "ap name %s no dot11 24ghz slot %s shutdown" % (args.ap, args.ap_band_slot)
        else:
            command = "config 802.11%s enable %s" % (band, args.ap)

    # TODO change disable to shutdown
    if (args.action == "disable_operation_status" and (args.ap is None)):
        raise Exception("action requires AP name")
    if (args.action == "disable_operation_status"):
        logg.info("send command to disable  operation status: ap name %s dot11 %shz slot %s shutdown" % (args.ap, band, args.ap_band_slot))
        if args.series == "9800":
            # TODO use the 24g 5g 6g notation, also support abgn (dual band?)
            if band == 'dual_band_6g' or band == 'dual_band_5g':
                command = "ap name %s dot11 dual-band slot %s shutdown" % (args.ap, args.ap_band_slot)
            elif band == '6g':
                command = "ap name %s dot11 6ghz slot %s shutdown" % (args.ap, args.ap_band_slot)
            elif band == '5g':
                command = "ap name %s dot11 5ghz slot %s shutdown" % (args.ap, args.ap_band_slot)
            elif band == '24g':
                command = "ap name %s dot11 24ghz slot %s shutdown" % (args.ap, args.ap_band_slot)
        else:
            command = "config 802.11%s disable %s" % (band, args.ap)

    if (args.action == "txPower" and ((args.ap is None) or (args.value is None))):
        raise Exception("txPower requires ap and value")
    if (args.action == "txPower"):
        if args.series == "9800":
            if band == "dual_band_6g" or band == "dual_band_5g":
                command = "ap name %s dot11 dual-band slot %s txpower %s" % (args.ap, args.ap_band_slot, args.value)
            elif band == "6g":
                command = "ap name %s dot11 6ghz slot %s txpower %s" % (args.ap, args.ap_band_slot, args.value)
            elif band == "5g":
                command = "ap name %s dot11 5ghz slot %s txpower %s" % (args.ap, args.ap_band_slot, args.value)
            elif band == "24g":
                command = "ap name %s dot11 24ghz slot %s txpower %s" % (args.ap, args.ap_band_slot, args.value)
            else:
                raise Exception("txPower requires ap and value")

        else:
            command = "config 802.11%s txPower ap %s %s" % (band, args.ap, args.value)

    if (args.action == "bandwidth" and ((args.ap is None) or (args.value is None))):
        raise Exception("bandwidth requires ap and value (20, 40, 80, 160)")
    if (args.action == "bandwidth"):
        if args.series == "9800":
            if band == "dual_band_6g" or band == "dual_band_5g":
                command = "ap name %s dot11 dual-band slot %s channel width %s" % (args.ap, args.ap_band_slot, args.value)
            elif band == "6g":
                command = "ap name %s dot11 6ghz slot %s channel width %s" % (args.ap, args.ap_band_slot, args.value)
            elif band == "5g" :
                command = "ap name %s dot11 5ghz slot %s channel width %s" % (args.ap, args.ap_band_slot, args.value)
            elif band == "24g":
                command = "ap name %s dot11 24ghz slot %s channel width %s" % (args.ap, args.ap_band_slot, args.value)
            else:
                raise Exception("bandwidth requires a band 24g, 5g, 6g")
        else:
            command = "config 802.11%s chan_width %s %s" % (band, args.ap, args.value)

    if (args.action == "channel" and ((args.ap is None) or (args.value is None))):
        raise Exception("channel requires ap and value 5Ghz ")
    if (args.action == "channel"):
        if args.series == "9800":
            if band == "dual_band_6g" or band == "dual_band_5g":
                command = "ap name %s dot11 dual-band slot %s channel %s" % (args.ap, args.ap_band_slot, args.value)
            elif band == "6g":
                command = "ap name %s dot11 6ghz slot %s channel %s" % (args.ap, args.ap_band_slot, args.value)
            elif band == "5g":
                command = "ap name %s dot11 5ghz slot %s channel %s" % (args.ap, args.ap_band_slot, args.value)
            elif band == "24g":
                command = "ap name %s dot11 24ghz slot %s channel %s" % (args.ap, args.ap_band_slot, args.value)
            else:
                raise Exception("channel requires a band 24g, 5g, 6g")
        else:
            command = "config 802.11%s channel ap %s %s" % (band, args.ap, args.value)

    if (args.action == "ap_channel" and (args.ap is None)):
        raise Exception("ap_channel requires ap")
    if (args.action == "ap_channel"):
        if args.series == "9800":
            if band == "dual_band_6g" or band == "dual_band_5g":
                command = "show ap dot11 dual-band summary"
            elif band == "6g":
                command = "show ap dot11 6ghz summary"
            elif band == '5g':
                command = "show ap dot11 5ghz summary"
            else:
                command = "show ap dot11 24ghz summary"
        else:
            command = "show ap channel %s" % (args.ap)

    if (args.action == "no_wlan_wireless_tag_policy" and (args.wlan is None)):
        raise Exception("wlan is required")
    if (args.action == "no_wlan_wireless_tag_policy"):
        logg.info("send wireless tag policy no wlan")
        logg.info("send wireless tag policy no wlan , for wlan {}".format(args.wlan))
        egg.sendline("config t")
        sleep(0.1)
        i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
        if i == 0:
            for command in ["wireless tag policy {policy_tag}".format(policy_tag=args.tag_policy), "wlan {wlan_name} policy {policy_profile}".format(wlan_name=args.wlan, policy_profile=args.policy_profile)]:
                egg.sendline(command)
                sleep(1)
                j = egg.expect_exact([CCP_POLICY_TAG, pexpect.TIMEOUT], timeout=timeout)
                if j == 0:
                    logg.info("command sent: {}".format(command))
                if j == 1:
                    logg.info("timed out on command prompt (config-policy-tag)# for command {}".format(command))
        if i == 1:
            logg.info("did not get the (config)# prompt")

    if (args.action == "wireless_tag_policy" and (args.wlan is None)):
        raise Exception("wlan is required")
    if (args.action == "wireless_tag_policy"):
        logg.info("send wireless tag policy")
        egg.sendline("config t")
        sleep(0.1)
        i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
        if i == 0:
            # RM204-TB2
            # for command in ["wireless tag policy default-policy-tag","wlan open-wlan policy default-policy-profile"]:
            for command in ["wireless tag policy {policy_tag}".format(policy_tag=args.tag_policy), "wlan {wlan_name} policy {policy_profile}".format(wlan_name=args.wlan, policy_profile=args.policy_profile)]:
                egg.sendline(command)
                sleep(1)
                j = egg.expect_exact([CCP_POLICY_TAG, pexpect.TIMEOUT], timeout=timeout)
                if j == 0:
                    logg.info("command sent: {}".format(command))
                if j == 1:
                    logg.info("timed out on command prompt (config-policy-tag)# for command {}".format(command))
        if i == 1:
            logg.info("did not get the (config)# prompt")
    if (args.action == "debug_disable_all"):
        if args.series == "9800":
            logg.info("action {} not avilable on 9800".format(args.action))
        else:
            command = "debug disable-all"

    if (args.action == "no_logging_console"):
        if args.series == "9800":
            logg.info("send no logging console")
            egg.sendline("config t")
            sleep(0.2)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                egg.sendline("no logging console")
                sleep(0.2)
            if i == 1:
                logg.info("did not get the (config)# prompt")
        else:
            command = "config logging debug console disable"

    if (args.action == "line_console_0"):
        logg.info("send: line console 0")
        egg.sendline("config t")
        sleep(0.2)
        i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
        if i == 0:
            egg.sendline("line console 0")
            sleep(0.1)
        if i == 1:
            logg.info("did not get the (config)# prompt")

    if (args.action == "no_wlan" and (args.wlan is None)):
        raise Exception("wlan is required")
    if (args.action == "no_wlan"):
        egg.sendline("config t")
        sleep(0.1)
        i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
        if i == 0:
            command = "no wlan %s" % (args.wlan)
            egg.sendline(command)
            sleep(0.1)
        if i == 1:
            logg.info("did not get the (config)# prompt")

    if (args.action == "show_wlan_summary"):
        print("command show wlan summary ")
        command = "show wlan summary"

    # used for 11r log reading
    if (args.action == "11r_logs"):
        if args.series == "9800":
            command = "sh wi stats client detail | inc 11r"

    # need the wlan name to elevate the prompt
    # WLC1#config t
    # Enter configuration commands, one per line.  End with CNTL/Z.
    # WLC1(config)#wlan open-wlan-15
    # WLC1(config-wlan)#
    # WLC1(config-wlan)#dtim dot11 5ghz ?
    #  <1-255>  DTIM Period
    # WLC1(config-wlan)#dtim dot11 5ghz 3
    # % WLAN needs to be disabled before performing this operation.

    if (args.action == "dtim" and ((args.value is None) or (args.wlan is None))):
        raise Exception("dtim a value 1 - 255 required")
    if (args.action == "dtim"):
        logg.info("(config-wlan)# dtim dot11 {band}hz  {value} ".format(band=args.band,value=args.value))
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.4)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                logg.info("elevated to (config)#")

                logg.info("elevated to (config)#")
                # for create wlan <name> <ID> <ssid>
                command = "wlan {wlan}".format(wlan=args.wlan)
                egg.sendline(command)
                sleep(0.4)
                j = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                if j == 0:
                    if args.band == '6g':
                        command = "dtim dot11 6ghz {value}".format(value=args.value)
                    elif args.band == '5g':
                        command = "dtim dot11 5ghz {value}".format(value=args.value)
                    logg.info("dtim command:  {command}".format(command=command))
                    egg.sendline(command)
                    sleep(0.4)
                if j == 1:
                    logg.info("did not get the (config-wlan)# prompt")
            if i == 0:
                logg.info("did not get the (config)# prompt")
        else:
            command = "dtim {value}".format(value=args.value)

    if (args.action == "create_wlan_wpa2" and ((args.wlanID is None) or (args.wlan is None) or (args.wlanSSID is None) or (args.security_key is None))):
        raise Exception("create_wlan_wpa2 wlanID, wlan, wlanSSID are required an")
    if (args.action == "create_wlan_wpa2"):
        logg.info("create_wlan_wpa2 wlan {} wlanID {} wlanSSID {}".format(args.wlan, args.wlanID, args.wlanSSID))
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.4)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                logg.info("elevated to (config)#")
                # for create wlan <name> <ID> <ssid>
                command = "wlan {} {} {}".format(args.wlan, args.wlanID, args.wlanSSID)
                logg.info("wpa2 network command {}".format(command))
                egg.sendline(command)
                sleep(0.4)
                j = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                if j == 0:
                    # previous commands for command in ["shutdown","no security ft","no security wpa","no security wpa wpa2","no security wpa wpa2 ciphers aes",
                    #      "no security wpa akm dot1x","no shutdown"]:

                    # 2/12/2022 - Cisco suggestion
                    for command in [
                        "assisted-roaming dual-list",
                        "bss-transition dual-list",
                        "radio policy dot11 24ghz",
                        "radio policy dot11 5ghz",
                        "security wpa psk set-key ascii 0 {security_key}".format(security_key=args.security_key),
                        "no security wpa akm dot1x",
                        "security wpa akm psk",
                            "no shutdown"]:
                        egg.sendline(command)
                        sleep(1)
                        k = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                        if k == 0:
                            logg.info("command sent: {}".format(command))
                        if k == 1:
                            logg.info("command time out: {}".format(command))
                if j == 1:
                    logg.info("did not get the (config-wlan)# prompt")
            if i == 0:
                logg.info("did not get the (config)# prompt")
        else:
            command = "config wlan create {} {} {}".format(args.wlanID, args.wlan, args.wlanSSID)


    if (args.action == "enable_ft_akm_ftpsk" and  (args.wlan is None) ):
        raise Exception("enable ft wlanID, wlan, wlanSSID are required")
    if (args.action == "enable_ft_akm_ftpsk"):
        logg.info("enable ft and select ft + psk akm  wlan {} wlanID {} wlanSSID {}".format(args.wlan, args.wlanID, args.wlanSSID))
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.4)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                logg.info("elevated to (config)#")
                # for create wlan <name> <ID> <ssid>
                command = "wlan {wlan}".format(wlan=args.wlan)
                egg.sendline(command)
                sleep(0.4)
                j = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                if j == 0:

                    for command in ["shutdown",
                                    "security ft",
                                    "security wpa psk set-key ascii 0 {security_key}".format(security_key=args.security_key),
                                    "no security wpa akm psk",
                                    "security wpa akm ft psk",
                                    "no shutdown"
                                    ]:
                        egg.sendline(command)
                        sleep(1)
                        k = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                        if k == 0:
                            logg.info("command sent: {}".format(command))
                        if k == 1:
                            logg.info("command time out: {}".format(command))
                if j == 1:
                    logg.info("did not get the (config-wlan)# prompt")
            if i == 0:
                logg.info("did not get the (config)# prompt")

    # argument to set dot1x on ft enabled for 6e wlan also to add authentication list as default
    if (args.action == "enable_ft_wpa3_dot1x" and (args.wlan is None)):
        raise Exception("enable ft wlanID, wlan, wlanSSID are required")
    if (args.action == "enable_ft_wpa3_dot1x"):
        logg.info("enable ft and select ft + dot1x  akm  wlan {} wlanID {} wlanSSID {}".format(args.wlan, args.wlanID,
                                                                                               args.wlanSSID))
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.4)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                logg.info("elevated to (config)#")
                # for create wlan <name> <ID> <ssid>
                command = "wlan {wlan}".format(wlan=args.wlan)
                egg.sendline(command)
                sleep(0.4)
                j = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                if j == 0:

                    for command in ["shutdown",
                                    "security ft",
                                    "no security wpa akm sae",
                                    "security wpa akm ft dot1x",
                                    "security dot1x authentication-list default",
                                    "no shutdown"
                                    ]:
                        egg.sendline(command)
                        sleep(1)
                        k = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                        if k == 0:
                            logg.info("command sent: {}".format(command))
                        if k == 1:
                            logg.info("command time out: {}".format(command))
                if j == 1:
                    logg.info("did not get the (config-wlan)# prompt")
            if i == 0:
                logg.info("did not get the (config)# prompt")

    if (args.action == "enable_ft_wpa3_dot1x_sha256" and (args.wlan is None)):
        raise Exception("enable ft wlanID, wlan, wlanSSID are required")
    if (args.action == "enable_ft_wpa3_dot1x_sha256"):
        logg.info("enable ft and select ft + dot1x and sha256  akm  wlan {} wlanID {} wlanSSID {}".format(args.wlan,
                                                                                                          args.wlanID,
                                                                                                          args.wlanSSID))
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.4)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                logg.info("elevated to (config)#")
                # for create wlan <name> <ID> <ssid>
                command = "wlan {wlan}".format(wlan=args.wlan)
                egg.sendline(command)
                sleep(0.4)
                j = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                if j == 0:

                    for command in ["shutdown",
                                    "security ft",
                                    "no security wpa akm sae",
                                    "security wpa akm dot1x-sha256",
                                    "security wpa akm ft dot1x",
                                    "security dot1x authentication-list  {value}".format(value=args.value),
                                    "no shutdown"
                                    ]:
                        egg.sendline(command)
                        sleep(1)
                        k = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                        if k == 0:
                            logg.info("command sent: {}".format(command))
                        if k == 1:
                            logg.info("command time out: {}".format(command))
                if j == 1:
                    logg.info("did not get the (config-wlan)# prompt")
            if i == 0:
                logg.info("did not get the (config)# prompt")

    if (args.action == "enable_ft_akm_ftsae" and  (args.wlan is None) ):
        raise Exception("enable ft wlanID, wlan, wlanSSID are required")
    if (args.action == "enable_ft_akm_ftsae"):
        logg.info("enable ft and select ft + sae akm  wlan {} wlanID {} wlanSSID {}".format(args.wlan, args.wlanID, args.wlanSSID))
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.4)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                logg.info("elevated to (config)#")
                # for create wlan <name> <ID> <ssid>
                command = "wlan {wlan}".format(wlan=args.wlan)
                egg.sendline(command)
                sleep(0.4)
                j = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                if j == 0:

                    for command in ["shutdown",
                                    "security ft",
                                    "security wpa psk set-key ascii 0 {security_key}".format(security_key=args.security_key),
                                    "no security wpa akm sae",
                                    "security wpa akm ft sae",
                                    "no shutdown"
                                    ]:
                        egg.sendline(command)
                        sleep(1)
                        k = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                        if k == 0:
                            logg.info("command sent: {}".format(command))
                        if k == 1:
                            logg.info("command time out: {}".format(command))
                if j == 1:
                    logg.info("did not get the (config-wlan)# prompt")
            if i == 0:
                logg.info("did not get the (config)# prompt")


    if (args.action == "enable_ftotd_akm_ftpsk" and (args.wlan is None)):
        raise Exception("enable ft wlan is required")
    if (args.action == "enable_ftotd_akm_ftpsk"):
        logg.info("enable ft, ft over the ds and select ft + psk akm  wlan {} wlanID {} wlanSSID {}".format(args.wlan,
                                                                                                            args.wlanID,
                                                                                                            args.wlanSSID))
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.4)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                logg.info("elevated to (config)#")
                # for create wlan <name> <ID> <ssid>
                command = "wlan {wlan}".format(wlan=args.wlan)
                egg.sendline(command)
                sleep(0.4)
                j = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                if j == 0:

                    for command in ["shutdown",
                                    "security ft",
                                    "security ft over-the-ds",
                                    "security wpa psk set-key ascii 0 {security_key}".format(
                                        security_key=args.security_key),
                                    "no security wpa akm psk",
                                    "security wpa akm ft psk",
                                    "no shutdown"
                                    ]:
                        egg.sendline(command)
                        sleep(1)
                        k = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                        if k == 0:
                            logg.info("command sent: {}".format(command))
                        if k == 1:
                            logg.info("command time out: {}".format(command))
                if j == 1:
                    logg.info("did not get the (config-wlan)# prompt")
            if i == 0:
                logg.info("did not get the (config)# prompt")

    if (args.action == "create_wlan_wpa3" and ((args.wlanID is None) or (args.wlan is None) or (args.wlanSSID is None) or (args.security_key is None))):
        raise Exception("create_wlan_wpa3 wlanID, wlan, wlanSSID are required an")
    if (args.action == "create_wlan_wpa3"):
        logg.info("create_wlan_wpa3 wlan {} wlanID {} wlanSSID {} security_key {}".format(args.wlan, args.wlanID, args.wlanSSID, args.security_key))
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.4)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                logg.info("elevated to (config)#")
                # for create wlan <name> <ID> <ssid>
                command = "wlan {} {} {}".format(args.wlan, args.wlanID, args.wlanSSID)
                logg.info("wpa2 network command {}".format(command))
                egg.sendline(command)
                sleep(0.4)
                j = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                if j == 0:
                    # previous commands for command in ["shutdown","no security ft","no security wpa","no security wpa wpa2","no security wpa wpa2 ciphers aes",
                    #      "no security wpa akm dot1x","no shutdown"]:

                    # 2/12/2022 - Cisco suggestion
                    for command in [
                        "assisted-roaming dual-list",
                        "radio policy dot11 6ghz",
                        "no security ft adaptive",
                        "no security wpa wpa2",
                        "security wpa psk set-key ascii 0 {security_key}".format(security_key=args.security_key),
                        "no security wpa akm dot1x",
                        "security wpa akm sae",
                        "security wpa akm sae pwe h2e",
                        "security wpa wpa3",
                        "security pmf mandatory",
                            "no shutdown"]:
                        egg.sendline(command)
                        sleep(1)
                        k = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                        if k == 0:
                            logg.info("command sent: {}".format(command))
                        if k == 1:
                            logg.info("command time out: {}".format(command))
                if j == 1:
                    logg.info("did not get the (config-wlan)# prompt")
            if i == 0:
                logg.info("did not get the (config)# prompt")
        else:
            command = "config wlan create {} {} {}".format(args.wlanID, args.wlan, args.wlanSSID)

    if (args.action == "create_wlan" and ((args.wlanID is None) or (args.wlan is None) or (args.wlanSSID is None))):
        raise Exception("wlanID, wlan, wlanSSID are required an")
    if (args.action == "create_wlan"):
        logg.info("create_wlan wlan {} wlanID {} wlanSSID {}".format(args.wlan, args.wlanID, args.wlanSSID))
        if args.series == "9800":
            egg.sendline("config t")
            sleep(0.4)
            i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
            if i == 0:
                logg.info("elevated to (config)#")
                # for create wlan <name> <ID> <ssid>
                command = "wlan {} {} {}".format(args.wlan, args.wlanID, args.wlanSSID)
                logg.info("open network command {}".format(command))
                egg.sendline(command)
                sleep(0.4)
                j = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                if j == 0:
                    # previous commands for command in ["shutdown","no security ft","no security wpa","no security wpa wpa2","no security wpa wpa2 ciphers aes",
                    #      "no security wpa akm dot1x","no shutdown"]:

                    # 1/14/2021 - Cisco suggestion
                    # We are basically disabling all the possible security parameters for Authentication
                    for command in [
                        "no security ft",
                        "no security ft adaptive",
                        "no security wpa",
                        "no security wpa wpa2",
                        "no security wpa wpa1",
                        "no security wpa wpa2 ciphers aes"
                        "no security dot1x authentication-list",
                        "no security wpa akm dot1x",
                            "no shutdown"]:
                        egg.sendline(command)
                        sleep(1)
                        k = egg.expect_exact([CCP_CONFIG_WLAN, pexpect.TIMEOUT], timeout=timeout)
                        if k == 0:
                            logg.info("command sent: {}".format(command))
                        if k == 1:
                            logg.info("command time out: {}".format(command))
                if j == 1:
                    logg.info("did not get the (config-wlan)# prompt")
            if i == 0:
                logg.info("did not get the (config)# prompt")
        else:
            command = "config wlan create {} {} {}".format(args.wlanID, args.wlan, args.wlanSSID)

    if (args.action == "delete_wlan"):
        if args.series == "9800":
            if (args.wlan is None):
                raise Exception("9800 series wlan is required")
            else:
                egg.sendline("config t")
                sleep(0.4)
                i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
                if i == 0:
                    logg.info("elevated to (config)#")
                    cmd = "no wlan %s" % (args.wlan)
                    egg.sendline(cmd)
                    sleep(0.4)
                if i == 1:
                    logg.info("did not get the (config)# prompt")
        else:
            if (args.action == "delete_wlan" and (args.wlanID is None)):
                raise Exception("wlan ID is required")
            command = "config wlan delete {}".format(args.wlanID)

    logg.info("action {} series {}".format(args.action, args.series))
    if (args.action == "enable_wlan"):
        if args.series == "9800":
            if (args.wlan is None):
                raise Exception("9800 series wlan is required")
            else:
                logg.info("sendline config t")
                egg.sendline("config t")
                sleep(0.3)
                i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
                if i == 0:
                    logg.info("elevated to (config)#")
                    cmd = "wlan %s" % (args.wlan)
                    egg.sendline(cmd)
                    sleep(0.1)
                    j = egg.expect_exact(["(config-wlan)#", pexpect.TIMEOUT], timeout=timeout)
                    if j == 0:
                        logg.info("enable_wlan send no shutdown")
                        cmd = "no shutdown"
                        egg.sendline(cmd)
                        sleep(0.1)
                    if j == 1:
                        logg.info("did not get the (config-wlan)# prompt")
                if i == 1:
                    logg.info("did not get the (config)# prompt")
        else:
            if (args.wlan is None):
                raise Exception("wlan ID is required")
            logg.info("send: config wlan enable {}".format(args.wlan))
            command = "config wlan enable %s" % (args.wlan)

    if (args.action == "disable_wlan"):
        if args.series == "9800":
            if (args.wlan is None):
                raise Exception("9800 series wlan is required")
            else:
                logg.info("sendline config t")
                egg.sendline("config t")
                sleep(0.3)
                i = egg.expect_exact(["(config)#", pexpect.TIMEOUT], timeout=timeout)
                if i == 0:
                    logg.info("elevated to (config)#")
                    cmd = "wlan %s" % (args.wlan)
                    egg.sendline(cmd)
                    sleep(0.1)
                    j = egg.expect_exact(["(config-wlan)#", pexpect.TIMEOUT], timeout=timeout)
                    if j == 0:
                        logg.info("disable_wlan send shutdown")
                        cmd = "shutdown"
                        egg.sendline(cmd)
                        sleep(0.1)
                    if j == 1:
                        logg.info("did not get the (config-wlan)# prompt")
                if i == 1:
                    logg.info("did not get the (config)# prompt")
        else:
            if (args.wlan is None):
                raise Exception("wlan ID is required")
            logg.info("send: config wlan disable {}".format(args.wlan))
            command = "config wlan disable %s" % (args.wlan)

    if (args.action == "wlan_qos" and (args.wlan is None)):
        raise Exception("wlan ID is required")
    if (args.action == "wlan_qos"):
        command = "config wlan qos %s %s" % (args.wlanID, args.value)

    # separate the 3504 and 9800 logouts as the are conflicting
    if (args.series == "9800"):
        if (command is None):
            sleep(0.5)
            logg.info("9800 Command processed earlier will logout")
        else:
            logg.info("Command[%s]" % command)
            egg.sendline(command)
            sleep(0.5)
            logg.info("command sent {}".format(command))
        logged_out_9800 = False
        loop_count = 0
        while logged_out_9800 == False and loop_count <= 5:
            loop_count += 1
            i = egg.expect_exact([CCP, CCP_EN, CCP_CONFIG, CCP_CONFIG_WLAN, CCP_POLICY_TAG, CCP_CONFIG_LINE, "--More--", CCP_BAD_IP, pexpect.TIMEOUT], timeout=timeout)
            logg.info("expect index: %s" % i)
            print(egg.before.decode('utf-8', 'ignore'))  # allows program that calls from subprocess to see output from command
            if i == 0:
                logg.info("{} prompt received can send logout, loop_count: {}".format(CCP, loop_count))
                egg.sendline("logout")
                sleep(0.1)
                logged_out_9800 = True
                break
            if i == 1:
                logg.info("{} prompt received will send logout, loop_count: {}".format(CCP_EN, loop_count))
                try:
                    egg.sendline("logout")
                    sleep(0.1)
                    logged_out_9800 = True
                except BaseException:
                    logg.info("9800 exception on logout")
                    sleep(0.1)
                break
            if i == 2:
                logg.info("{} prompt received will send exit, loop_count: {}".format(CCP_CONFIG, loop_count))
                try:
                    # exit will go one prompt up
                    egg.sendline("exit")
                    sleep(0.2)
                    logged_out_9800 = True
                except BaseException:
                    logg.info("9800 exception on end")
                    sleep(0.1)
            if i == 3:
                logg.info("{} prompt received will send end, loop_count: {}".format(CCP_CONFIG_WLAN, loop_count))
                try:
                    # end will go to the # prompt
                    egg.sendline("end")
                    sleep(0.2)
                except BaseException:
                    logg.info("9800 exception on end")
                    sleep(0.1)
            if i == 4:
                logg.info("(config-policy-tag)# prompt received will send end, loop_count: {}".format(loop_count))
                try:
                    egg.sendline("end")
                    sleep(0.2)
                except BaseException:
                    logg.info("9800 exception on end")
                    sleep(0.1)
            if i == 5:
                logg.info("{} prompt received will send end, loop_count: {}".format(CCP_CONFIG_LINE, loop_count))
                try:
                    egg.sendline("end")
                    sleep(0.2)
                except BaseException:
                    logg.info("9800 exception on end")
                    sleep(0.1)
            if i == 6:  # --More--
                logg.info("9800 found --More--, sending space")
                egg.send(SEND_MORE)
            if i == 7: # BAD IP
                logg.info("9800 expect timeout loop_count: {}".format(loop_count))
                egg.sendline("exit")
                logged_out_9800 = True
            # Timeout - try to exit
            if i == 8:
                logg.info("9800 expect timeout loop_count: {}".format(loop_count))
                # a timeout , tray again.
                # egg.sendline("exit")
                # logged_out_9800 = True


        if(logged_out_9800 == False):
            logg.info("######################################################################################")
            logg.info("9800 did not send logout at end of command processing this could tie up the connection")
            logg.info("######################################################################################")

        if(scheme == "telnet"):
            egg.sendline("\x1b\r")
            logg.info("send escape to exit connection")
            sleep(0.2)
        logg.info("send close to the egg child process")
        egg.close(force=True)
        sleep(0.1)
    # 3504
    else:
        if (command is None):
            sleep(0.5)
            logg.info("No command specified, going to log out.")
        else:
            logg.info("Command[%s]" % command)
            egg.sendline(command)
            sleep(0.5)
            logg.info("command sent {}".format(command))
            egg.expect([pexpect.TIMEOUT], timeout=1)
            print(egg.before.decode('utf-8', 'ignore'))

        command_sent = False
        loop_count = 0
        while command_sent == False and loop_count <= 3:
            loop_count += 1
            try:
                i = egg.expect_exact([CCPROMPT, AREYOUSURE, '--More-- or', 'config paging disable', pexpect.TIMEOUT], timeout=timeout)
                logg.info("before {} after {}".format(egg.before.decode('utf-8', 'ignore'), egg.after.decode('utf-8', 'ignore')))

                print(egg.before.decode('utf-8', 'ignore'))
                if i == 0:
                    logg.info("{} prompt received after command sent".format(CCPROMPT))
                    # granted the break will exit the loop
                    command_sent = True
                if i == 2:
                    egg.sendline("y")
                    command_sent = True
                if i == 3:
                    egg.send(SEND_MORE)
                    logg.info("received --More-- or")
                if i == 4:
                    egg.sendline(NL)
                    logg.info("received: config paging disable ")

                if i == 5:
                    egg.sendline(NL)
                    logg.info(" Check to see if logging to console is disabled")
                    command_sent = True

            except BaseException:
                logg.info("closing connection logout loop {}".format(CCPROMPT))
        try:
            egg.sendline("logout")
            logg.info("logout")
            logg.info("send close to the egg child process")
            egg.close(force=True)
            sleep(0.1)
        except BaseException:
            logg.info("closing connection on logout")


# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
if __name__ == '__main__':
    main()

####
####
####
