#!/usr/bin/env python3

"""
NAME: port_probe.py

PURPOSE:
Probes a port for information. If a station is used, an ssid, radio, and security type must be specified

Use './port_probe.py --help' to see command line usage and options
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
import datetime
import time
import pprint


class PortProbe(Realm):
    def __init__(self,
                 ssid=None,
                 security=None,
                 password=None,
                 port_name=None,
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
        self.port_name = port_name
        self.security = security
        self.password = password
        self.radio = radio
        self.mode = mode
        self.debug = _debug_on
        if 'sta' in self.port_name:
            self.number_template = number_template
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
        if 'sta' in self.port_name:
            self.station_profile.admin_up()
        print("Probing %s" % self.port_name)
        port_info = self.name_to_eid(self.port_name)
        data = {
            "shelf": 1,
            "resource": 1,
            "port": self.port_name,
            "key": "probe_port.quiet.%d.%d.%s" % (port_info[0], port_info[1], port_info[2])
        }
        self.json_post("/cli-json/probe_port", data)
        time.sleep(10)
        probe_results = self.json_get("probe/1/1/%s" % self.port_name)

        print(probe_results)

    def cleanup(self):
        if 'sta' in self.port_name:
            self.station_profile.cleanup()
            LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)

    def build(self):
        if 'sta' in self.port_name:
            self.station_profile.use_security(self.security, self.ssid, self.password)
            self.station_profile.set_number_template(self.number_template)
            print("Creating stations")
            self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
            self.station_profile.set_command_param("set_port", "report_timer", 1500)
            self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
            self.station_profile.create(radio=self.radio, sta_names_=[self.port_name], num_stations=1, debug=self.debug)
            LFUtils.wait_until_ports_appear(self.port_name)
        self._pass("PASS: Station build finished")


def main():
    parser = Realm.create_basic_argparse(
        prog='port_probe_test.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        Used to probe ports for information
            ''',
        description='''\
        Probes a port for information. If a station is used, an ssid, radio, and security type must be specified

        Example:
        ./port_probe.py --ssid test_name --security open --radio wiphy0
        ''')

    parser.add_argument('--mode', help='Used to force mode of stations')
    parser.add_argument('--port_name', help='Name of station to be used', default="sta0000")

    args = parser.parse_args()

    port_probe = PortProbe(host=args.mgr,
                           port=args.mgr_port,
                           number_template="0000",
                           port_name=args.port_name,
                           upstream=args.upstream_port,
                           ssid=args.ssid,
                           password=args.passwd,
                           radio=args.radio,
                           security=args.security,
                           use_ht160=False,
                           mode=args.mode,
                           _debug_on=args.debug)

    port_probe.build()
    # exit()
    if not port_probe.passes():
        print(port_probe.get_fail_message())
        port_probe.exit_fail()

    port_probe.start()
    port_probe.cleanup()


if __name__ == "__main__":
    main()
