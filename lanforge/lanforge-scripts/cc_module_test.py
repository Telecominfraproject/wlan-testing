#!/usr/bin/env python3

"""
NAME: cc_module_test.py

PURPOSE:
to test the dynamic import of a controller module

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

import subprocess
import argparse
import logging
import importlib
import os
import subprocess
from pprint import pformat

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../")))

logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")


# unit test for controller wrapper
def main():
    # arguments
    parser = argparse.ArgumentParser(
        prog='cc_module_test.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            cc_module_test.py: wrapper for interface to a series of controllers
            ''',
        description='''\
NAME: cc_module_test.py

PURPOSE:
to test the dynamic import of a controller module

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

#./cc_module_test.py --scheme ssh --dest localhost --port 8887 --user admin --passwd Cisco123 --ap APA453.0E7B.CF9C --series 9800 --prompt "WLC1" --timeout 10 --band '5g' --module "cc_module_9800_3504"
 
    # These commands are just needed to interact it can be done in class methods.abs(
    parser.add_argument("--dest", type=str, help="address of the cisco controller", required=True)
    parser.add_argument("--port", type=str, help="control port on the controller", required=True)
    parser.add_argument("--user", type=str, help="credential login/username", required=True)
    parser.add_argument("--passwd", type=str, help="credential password", required=True)
    parser.add_argument("--ap", type=str, help="ap name APA453.0E7B.CF9C", required=True)
    parser.add_argument("--prompt", type=str, help="controller prompt", required=True)
    parser.add_argument("--band", type=str, help="band to test 24g, 5g, 6g", required=True)
    parser.add_argument("--series", type=str, help="controller series", choices=["9800", "3504"], required=True)
    parser.add_argument("--scheme", type=str, choices=["serial", "ssh", "telnet"], help="Connect via serial, ssh or telnet")
    parser.add_argument("--timeout", type=str, help="timeout value", default=3)
    parser.add_argument("--module", type=str, help="series module", required=True)

    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    # dynamic import of the controller module
    series = importlib.import_module(args.module)

    # create the controller
    cc = series.create_controller_series_object(
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

    cc.show_ap_config_slots()
    # cc.show_ap_summary()
    # cc.no_logging_console()
    # cc.line_console_0()
    # cc.show_wlan_summary()
    # cc.show_ap_dot11_5gz_summary()


if __name__ == "__main__":
    main()
