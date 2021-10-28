#!/usr/bin/env python3

"""
NAME: test_ipv4_l4_ftp_wifi.py

PURPOSE:
test_ipv4_l4_ftp_wifi.py will create stations and endpoints to generate and verify layer-4 traffic over an ftp connection

This script will monitor the bytes-wr attribute of the endpoints. If the the monitored value does not continually increase, this test will not pass.

EXAMPLE:
./test_ipv4_l4_ftp_wifi.py --upstream_port eth1 --radio wiphy0 --num_stations 3 --security {open|wep|wpa|wpa2|wpa3}
    --ssid netgear --passwd admin123 --dest 10.40.0.1 --test_duration 2m --interval 1s --requests_per_ten 600
    --dest /var/www/html/data_slug_4K.bin --source /tmp/data_slug_4K.bin --ftp_user lanforge --ftp_passwd lanforge
    --debug
    
Use './test_ipv4_l4_ftp_wifi.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""

import sys

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append('../py-json')

import argparse
from LANforge.lfcli_base import LFCliBase
from LANforge.LFUtils import *
from LANforge import LFUtils
import realm
import time
import datetime


class IPV4L4(LFCliBase):
    def __init__(self, host, port, ssid, security, password, requests_per_ten, station_list, number_template="00000",
                 upstream_port="eth1", radio="wiphy0", ftp_user="localhost", ftp_passwd="localhost",
                 source="", dest="",
                 test_duration="5m",
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, port, _debug=_debug_on, _exit_on_fail=_exit_on_fail)
        self.host = host
        self.port = port
        self.ssid = ssid
        self.radio = radio
        self.upstream_port = upstream_port
        self.security = security
        self.password = password
        self.requests_per_ten = requests_per_ten
        self.number_template = number_template
        self.sta_list = station_list
        self.test_duration = test_duration

        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.cx_profile = self.local_realm.new_http_profile()

        self.station_profile.lfclient_url = self.lfclient_url
        self.ftp_user = ftp_user
        self.ftp_passwd = ftp_passwd
        self.source = source
        self.dest = dest
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password,
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.mode = 0

        self.cx_profile.requests_per_ten = self.requests_per_ten

        self.port_util = realm.PortUtils(self.local_realm)

    def __compare_vals(self, old_list, new_list):
        passes = 0
        expected_passes = 0
        if len(old_list) == len(new_list):
            for item, value in old_list.items():
                expected_passes += 1
                if new_list[item] > old_list[item]:
                    passes += 1
                # print(item, old_list[item], new_list[item], passes, expected_passes)

            if passes == expected_passes:
                return True
            else:
                return False
        else:
            return False

    def __get_values(self):
        time.sleep(1)
        cx_list = self.json_get("layer4/list?fields=name,bytes-wr", debug_=self.debug)
        # print("==============\n", cx_list, "\n==============")
        cx_map = {}
        for cx_name in cx_list['endpoint']:
            if cx_name != 'uri' and cx_name != 'handler':
                for item, value in cx_name.items():
                    for value_name, value_rx in value.items():
                        if item in self.cx_profile.created_cx.keys() and value_name == 'bytes-wr':
                            cx_map[item] = value_rx
        return cx_map

    def build(self):
        # Build stations
        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template(self.number_template)
        print("Creating stations")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio, sta_names_=self.sta_list, debug=self.debug)
        self._pass("PASS: Station build finished")

        self.station_profile.admin_up()
        if self.local_realm.wait_for_ip(self.sta_list):
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            exit(1)
        self.cx_profile.direction = "ul"
        self.cx_profile.dest = self.dest
        self.cx_profile.create(ports=self.station_profile.station_names, sleep_time=.5, debug_=self.debug,
                               suppress_related_commands_=True, ftp=True, user=self.ftp_user, passwd=self.ftp_passwd,
                               source=self.source)

    def start(self, print_pass=False, print_fail=False):
        print("Starting Test...")
        self.cx_profile.start_cx()
        cur_time = datetime.datetime.now()
        old_rx_values = self.__get_values()
        end_time = self.local_realm.parse_time(self.test_duration) + cur_time
        passes = 0
        expected_passes = 0
        while cur_time < end_time:
            interval_time = cur_time + datetime.timedelta(minutes=1)
            while cur_time < interval_time:
                cur_time = datetime.datetime.now()
                time.sleep(1)

            new_rx_values = self.__get_values()
            # print(old_rx_values, new_rx_values)
            # print("\n-----------------------------------")
            # print(cur_time, end_time, cur_time + datetime.timedelta(minutes=1))
            # print("-----------------------------------\n")
            expected_passes += 1
            if self.__compare_vals(old_rx_values, new_rx_values):
                passes += 1
            else:
                self._fail("FAIL: Not all stations increased traffic", print_fail)
                break
            old_rx_values = new_rx_values
            cur_time = datetime.datetime.now()
        if passes == expected_passes:
            self._pass("PASS: All tests passes", print_pass)

    def stop(self):
        self.cx_profile.stop_cx()
        self.station_profile.admin_down()

    def cleanup(self, sta_list):
        self.cx_profile.cleanup()
        self.station_profile.cleanup(sta_list)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=sta_list,
                                           debug=self.debug)


def main():
    lfjson_port = 8080

    parser = LFCliBase.create_basic_argparse(
        prog='test_ipv4_l4_ftp_wifi.py',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
                Create layer-4 endpoints and test that the bytes-wr from the chosen URL are increasing over the
                duration of the test
                ''',

        description='''\
        test_ipv4_l4_ftp_wifi.py
--------------------
Generic command example:
python3 ./test_ipv4_l4_ftp_wifi.py --upstream_port eth1 \\
    --radio wiphy0 \\
    --num_stations 3 \\
    --security {open|wep|wpa|wpa2|wpa3} \\
    --ssid netgear \\
    --passwd admin123 \\
    --dest 10.40.0.1 \\
    --test_duration 2m \\
    --interval 1s \\
    --requests_per_ten 600 \\
    --dest /var/www/html/data_slug_4K.bin \\
    --source /tmp/data_slug_4K.bin \\
    --ftp_user lanforge \\
    --ftp_passwd lanforge \\
    --debug
            ''')

    parser.add_argument('--test_duration', help='--test_duration sets the duration of the test', default="5m")
    parser.add_argument('--requests_per_ten', help='--requests_per_ten number of request per ten minutes', default=600)
    parser.add_argument('--dest', help='--dest specifies the destination for the file', default="/var/www/html/data_slug_4K.bin")
    parser.add_argument('--source', help='--source specifies the source of the file',
                        default="/tmp/data_slug_4K.bin")
    parser.add_argument('--ftp_user', help='--ftp_user sets the username to be used for ftp', default="lanforge")
    parser.add_argument('--ftp_passwd', help='--ftp_user sets the password to be used for ftp', default="lanforge")

    args = parser.parse_args()
    num_sta = 2
    if (args.num_stations is not None) and (int(args.num_stations) > 0):
        num_stations_converted = int(args.num_stations)
        num_sta = num_stations_converted
        
    station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=num_sta-1, padding_number_=10000,
                                          radio=args.radio)

    ip_test = IPV4L4(host=args.mgr, port=args.mgr_port,
                     ssid=args.ssid,
                     password=args.passwd,
                     security=args.security,
                     station_list=station_list,
                     test_duration=args.test_duration,
                     requests_per_ten=args.requests_per_ten,
                     _debug_on=args.debug,
                     upstream_port=args.upstream_port,
                     ftp_user=args.ftp_user,
                     ftp_passwd=args.ftp_passwd,
                     dest=args.dest,
                     source=args.source)
    ip_test.cleanup(station_list)
    ip_test.build()
    if not ip_test.passes():
        print(ip_test.get_fail_message())
        exit(1)
    ip_test.start(False, False)
    ip_test.stop()
    if not ip_test.passes():
        print(ip_test.get_fail_message())
        exit(1)
    time.sleep(30)
    ip_test.cleanup(station_list)
    if ip_test.passes():
        print("Full test passed, all endpoints had increased bytes-wr throughout test duration")


if __name__ == "__main__":
    main()
