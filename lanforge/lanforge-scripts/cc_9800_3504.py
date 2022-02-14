#!/usr/bin/env python3

"""
NAME: cc_9800_3504.py

PURPOSE:
wrapper class to provide common interface to a controller,
    class methods will hold login information and common commands

SETUP:
None

EXAMPLE:
    There is a unit test included to try sample command scenarios


COPYWRITE
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

INCLUDE_IN_README
"""

import sys
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

import argparse
import logging
import importlib
import os
import subprocess
from pprint import pformat

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../")))

logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

# This name must be generic.


class create_controller_series_object:
    def __init__(self,
                 scheme=None,
                 dest=None,
                 user=None,
                 passwd=None,
                 prompt=None,
                 series=None,
                 band=None,
                 ap=None,
                 port=None,
                 timeout=None
                 ):
        if scheme is None:
            raise ValueError('Controller scheme must be set: serial, ssh or telnet')
        else:
            self.scheme = scheme
        if dest is None:
            raise ValueError('Controller dest must be set: and IP or localhost')
        else:
            self.dest = dest
        if user is None:
            raise ValueError('Controller user must be set')
        else:
            self.user = user
        if passwd is None:
            raise ValueError('Controller passwd must be set')
        else:
            self.passwd = passwd
        if prompt is None:
            raise ValueError('Controller prompt must be set: WLC1')
        else:
            self.prompt = prompt
        if series is None:
            raise ValueError('Controller series must be set: 9800 or 3504')
        else:
            self.series = series
        
        if ap is None:
            raise ValueError('Controller AP  must be set')
        else:
            self.ap = ap
        if band is None:
            raise ValueError('Controller band  must be set')
        else:
            self.band = band
        if port is None:
            raise ValueError('Controller port  must be set')
        else:
            self.port = port

        if timeout is None:
            logger.info("timeout not set default to 10 sec")
            self.timeout = '10'
        else:
            self.timeout = timeout

        self.bandwidth = None
        self.wlanSSID = None
        self.wlanpw = None
        self.tag_policy = None
        self.policy_profile = None
        self.tx_power = None
        self.channel = None
        self.bandwidth = None
        self.action = None
        self.value = None
        self.command = []
        self.info = "Cisco 9800 Controller Series"


    # TODO update the wifi_ctl_9800_3504 to use 24g, 5g, 6g
    def convert_band(self):
        if self.band == '24g':
            self.band = 'b'
        elif self.band == '5g':
            self.band = 'a'
        elif self.band == '6g':
            self.band = '6g'
        elif self.band == 'a' or self.band == 'b':
            pass
        else:
            logger.critical("band needs to be set 24g 5g or 6g")
            raise ValueError("band needs to be set 24g 5g or 6g")


    def send_command(self):
        # for backward compatibility wifi_ctl_9800_3504 expects 'a' for 5g and 'b' for 24b
        self.convert_band()
        
        # Generate command
        if self.action == 'cmd':
            logger.debug("action {action}".format(action=self.action))
            logger.info(("./wifi_ctl_9800_3504.py --scheme {scheme} --dest {dest} --user {user} --passwd {passwd} --ap {ap} --band {band}"
                     " --action {action} --value {value} --series {series} --port {port} --prompt  {prompt}").format(
                    scheme=self.scheme, dest=self.dest, user=self.user, passwd=self.passwd, ap=self.ap, band=self.band,
                    action=self.action, value=self.value, series=self.series, port=self.port, prompt=self.prompt))

            self.command = ["./wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--dest", self.dest,
                "--user", self.user, "--passwd", self.passwd, "--ap", self.ap, "--band", self.band,
                "--action", self.action, "--value", self.value, "--series", self.series, "--port", self.port, "--prompt", self.prompt]
        else:
            logger.debug("action {action}".format(action=self.action))
            logger.info(("./wifi_ctl_9800_3504.py --scheme {scheme} --dest {dest} --user {user} --passwd {passwd} --ap {ap} --band {band}"
                     " --action {action} --series {series} --port {port} --prompt  {prompt}").format(
                    scheme=self.scheme, dest=self.dest, user=self.user, passwd=self.passwd, ap=self.ap, band=self.band,
                    action=self.action, series=self.series, port=self.port, prompt=self.prompt))

            self.command = ["./wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--dest", self.dest,
                "--user", self.user, "--passwd", self.passwd, "--ap", self.ap, "--band", self.band,
                "--action", self.action, "--series", self.series, "--port", self.port, "--prompt", self.prompt]

        
        logger.info(self.command)
        # for now do not capture all the output,  have the logger to the work
        advanced = subprocess.run(self.command, capture_output=False, check=True)
        # advanced = subprocess.run(self.command, capture_output=True, check=True) if need to capture output and process

    def show_ap_config_slots(self):
        logger.info("show ap config slots")
        self.action = "cmd"
        self.value = "show ap config slots"
        self.send_command()

    def show_ap_summary(self):
        logger.info("show ap summary")
        self.action = "summary"
        self.send_command()

    # this command will disable debug logging to the terminal which causes issues with pexpect
    def no_logging_console(self):
        logger.info("no_logging_console")
        self.action = "no_logging_console"
        self.send_command()

    # The use of "line console 0" command is to connect a switch/router through medium console. 
    # If there is only one console port, you can only choose "line console 0". 
    # However if you have more than the number goes as 1,2,3,4 ... You can set different or same password to all your console ports.
    # Note: needed to be set for tx power script 
    def line_console_0(self):
        logger.info("line_console_0")
        self.action = "line_console_0"
        self.send_command()

    def show_wlan_summary(self):
        logger.info("show_wlan_summary")
        self.action = "show_wlan_summary"
        self.send_command()

    def show_ap_dot11_5gz_summary(self):
        logger.info("show_ap_dot11_5gz_summary")
        # TODO advanced was for legacy to 3504, refactor 
        self.action = "advanced"
        self.send_command()


# unit test for 9800 3504 controller
def main():
    # arguments
    parser = argparse.ArgumentParser(
        prog='cc_9800_3504.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            cc_9800_3504.py: wrapper for interface to a controller library
            ''',
        description='''\
NAME: cc_9800_3504.py

PURPOSE:
wrapper class to provide common interface to a controller,
    class methods will hold login information and common commands

SETUP:
None

EXAMPLE:
    There is a unit test included to try sample command scenarios


COPYWRITE
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

INCLUDE_IN_README
---------
            ''')

# sample command
# ./wifi_ctl_9800_3504.py --scheme ssh --dest localhost --port 8887 --user admin --passwd Cisco123 --ap APA453.0E7B.CF9C --series 9800  --action cmd --value "show ap config slots" --prompt "WLC1" --timeout 10
# ./cc_9800_3504.py --scheme ssh --dest localhost --port 8887 --user admin --passwd Cisco123 --ap APA453.0E7B.CF9C --series 9800 --prompt "WLC1" --timeout 10

    parser.add_argument("--dest", type=str, help="address of the cisco controller", required=True)
    parser.add_argument("--port", type=str, help="control port on the controller", required=True)
    parser.add_argument("--user", type=str, help="credential login/username", required=True)
    parser.add_argument("--passwd", type=str, help="credential password", required=True)
    parser.add_argument("--ap", type=str, help="ap name APA453.0E7B.CF9C", required=True)
    parser.add_argument("--prompt", type=str, help="controller prompt", required=True)
    parser.add_argument("--band", type=str, help="band to test 24g, 5g, 6g", required=True)
    parser.add_argument("--series", type=str, help="controller series", choices=["9800","3504"], required=True)
    parser.add_argument("--scheme", type=str, choices=["serial", "ssh", "telnet"], help="Connect via serial, ssh or telnet")
    parser.add_argument("--timeout", type=str, help="timeout value", default=3)

    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    cs = create_controller_series_object(
        scheme=args.scheme,
        dest=args.dest,
        user=args.user,
        passwd=args.passwd,
        prompt=args.prompt,
        series=args.series,
        ap=args.ap,
        port=args.port,
        band=args.band,
        timeout=args.timeout)

    # cs.show_ap_config_slots()
    # cs.show_ap_summary()
    # cs.no_logging_console()
    # cs.line_console_0()
    cs.show_wlan_summary()
    cs.show_ap_dot11_5gz_summary()


if __name__ == "__main__":
    main()
