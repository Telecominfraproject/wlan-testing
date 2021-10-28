#!/usr/bin/env python3

"""
NAME: sta_scan_test.py

PURPOSE:
Creates a station with specified ssid info (can be real or fake ssid, if fake use open for security), then
starts a scan and waits 15 seconds, finally scan results are printed to console

Use './sta_scan_test.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""

import sys
import os

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
sys.path.append(os.path.join(os.path.abspath('..'), 'py-json'))

if 'py-dashboard' not in sys.path:
sys.path.append(os.path.join(os.path.abspath('..'), 'py-dashboard'))

import argparse
from LANforge import LFUtils
from realm import Realm
import time


class StaScan(Realm):
    def __init__(self,
                 ssid=None,
                 security=None,
                 password=None,
                 sta_list=[],
                 upstream=None,
                 radio=None,
                 host="localhost",
                 port=8080,
                 mode=0,
                 number_template="00000",
                 use_ht160=False,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(lfclient_host=host,
                         lfclient_port=port),
        self.upstream = upstream
        self.host = host
        self.port = port
        self.ssid = ssid
        self.sta_list = sta_list
        self.security = security
        self.password = password
        self.radio = radio
        self.mode = mode
        self.number_template = number_template
        self.debug = _debug_on
        self.station_profile = self.new_station_profile()
        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.debug = self.debug

        self.station_profile.use_ht160 = use_ht160
        if self.station_profile.use_ht160:
            self.station_profile.mode = 9
        self.station_profile.mode = mode

    def start(self):
        self.station_profile.admin_up()
        print(self.sta_list)
        print("Sleeping 15s while waiting for scan")
        data = {
            "shelf": 1,
            "resource": 1,
            "port": self.sta_list
        }
        self.json_post("/cli-json/scan_wifi", data)
        time.sleep(15)
        scan_results = self.json_get("scanresults/1/1/%s" % ','.join(self.sta_list))

        print("{0:<23}".format("BSS"), "{0:<7}".format("Signal"), "{0:<5}".format("SSID"))
        for result in scan_results['scan-results']:
            for name, info in result.items():
                print("%s\t%s\t%s" % (info['bss'], info['signal'], info['ssid']))



    def pre_cleanup(self):
        for sta in self.sta_list:
            self.rm_port(sta, check_exists=True)

    def cleanup(self):
        self.station_profile.cleanup()
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)

    def build(self):
        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template(self.number_template)
        print("Creating stations")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio, sta_names_=self.sta_list, num_stations=1, debug=self.debug)
        self._pass("PASS: Station build finished")
        LFUtils.wait_until_ports_appear(','.join(self.sta_list))


def main():
    parser = Realm.create_basic_argparse(
        prog='sta_scan_test.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        Used to scan for ssids after creating a station
            ''',
        description='''\
        Creates a station with specified ssid info (can be real or fake ssid, if fake use open for security), then 
        starts a scan and waits 15 seconds, finally scan results are printed to console 
        
        Example:
        ./sta_scan_test.py --ssid test_name --security open --radio wiphy0
        ''')

    parser.add_argument('--mode', help='Used to force mode of stations')
    parser.add_argument('--sta_name', help='Name of station to be used', default=["sta0000"])

    args = parser.parse_args()

    station_list = args.sta_name
    sta_scan_test = StaScan(host=args.mgr,
                            port=args.mgr_port,
                            number_template="0000",
                            sta_list=station_list,
                            upstream=args.upstream_port,
                            ssid=args.ssid,
                            password=args.passwd,
                            radio=args.radio,
                            security=args.security,
                            use_ht160=False,
                            mode=args.mode,
                            _debug_on=args.debug)

    sta_scan_test.pre_cleanup()

    sta_scan_test.build()
    # exit()
    if not sta_scan_test.passes():
        print(sta_scan_test.get_fail_message())
        sta_scan_test.exit_fail()

    sta_scan_test.start()
    sta_scan_test.cleanup()


if __name__ == "__main__":
    main()
