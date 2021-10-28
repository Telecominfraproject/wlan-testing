#!/usr/bin/env python3
# Example of how to instantiate StaConnect and run the test
import sys
import os
import importlib
import time
import argparse

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

# if you lack __init__.py in this directory you will not find sta_connect module
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
sta_connect = importlib.import_module("py-scripts.sta_connect")
StaConnect = sta_connect.StaConnect


def main():
    parser = LFCliBase.create_basic_argparse(
        prog='sta_connect_example.py',
        formatter_class=argparse.RawTextHelpFormatter
    )
    required_args=None
    for group in parser._action_groups:
        if group.title == "required arguments":
            required_args=group
            break;

    optional_args=None
    for group in parser._action_groups:
        if group.title == "optional arguments":
            optional_args=group
            break;

    args = parser.parse_args()
    if args.upstream_port is None:
        args.upstream_port = "eth2"
    if args.ssid is None:
        args.ssid = "Default-SSID-2g"
    if args.passwd is None:
        args.passwd = "12345678"
    if args.security is None:
        args.security = sta_connect.WPA2
    if args.radio is None:
        args.radio = "wiphy0"
    staConnect = StaConnect("localhost", 8080, _debugOn=False)
    staConnect.sta_mode = 0
    staConnect.upstream_resource = 1
    staConnect.upstream_port = args.upstream_port
    staConnect.radio = args.radio
    staConnect.resource = 1
    staConnect.dut_security = args.security
    staConnect.dut_ssid = args.ssid
    staConnect.dut_passwd = args.passwd
    staConnect.station_names = [ "sta000" ]
    staConnect.setup()
    staConnect.start()
    time.sleep(20)
    staConnect.stop()
    #staConnect.finish()
    staConnect.cleanup()
    is_passing = staConnect.passes()
    if is_passing == False:
        # run_results = staConnect.get_failed_result_list()
        fail_message = staConnect.get_fail_message()
        print("Some tests failed:\n" + fail_message)
    else:
        print("Tests pass")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


if __name__ == '__main__':
    main()

#
