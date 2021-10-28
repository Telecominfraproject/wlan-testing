#!/usr/bin/env python3

"""
NAME: test_ipv4_l4_ftp_urls_per_ten.py

PURPOSE:
test_ipv4_l4_ftp_urls_per_ten.py will create stations and endpoints to generate and verify layer-4 traffic over an ftp connection

This script will monitor the urls/s attribute of the endpoints. If the the monitored value does not continually increase, this test will not pass.

EXAMPLE:
    ./test_ipv4_l4_ftp_urls_per_ten.py --upstream_port eth1 --radio wiphy0 --num_stations 3 --security {open|wep|wpa|wpa2|wpa3}
    --ssid netgear --passwd admin123 --test_duration 2m --interval 1s --mode 1 --ap "00:0e:8e:78:e1:76" --requests_per_ten 600
    --num_tests 1 --url "ul ftp://lanforge:lanforge@10.40.0.1/example.txt  /home/lanforge/example.txt" --debug

Use './test_ipv4_l4_ftp_urls_per_ten.py --help' to see command line usage and options
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

import argparse
from LANforge.lfcli_base import LFCliBase
from LANforge.LFUtils import *
from LANforge import LFUtils
import realm
import time
import datetime


class IPV4L4(LFCliBase):
    def __init__(self, ssid, security, password, url, requests_per_ten, station_list,test_duration="2m",host="localhost", port=8080, 
                 number_template="00000", num_tests=1, radio="wiphy0", mode=0, ap=None,
                 _debug_on=False, upstream_port="eth1",
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, 
        port, 
        _debug=_debug_on, 
        _local_realm = realm.Realm(lfclient_host=host, lfclient_port=port), 
        _exit_on_fail=_exit_on_fail)
        self.host = host
        self.port = port
        self.radio = radio
        self.upstream_port = upstream_port
        self.ssid = ssid
        self.security = security
        self.password = password
        self.mode = mode
        self.ap=ap
        self.url = url
        self.requests_per_ten = requests_per_ten
        self.number_template = number_template
        self.sta_list = station_list
        self.num_tests = num_tests
        self.target_requests_per_ten = requests_per_ten
        self.test_duration = test_duration

        self.station_profile = self.local_realm.new_station_profile()
        self.cx_profile = self.local_realm.new_l4_cx_profile()

        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password,
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.mode = self.mode
        if self.ap is not None:
            self.station_profile.set_command_param("add_sta", "ap",self.ap) 
        self.cx_profile.url = self.url
        print(self.cx_profile.url)
        self.cx_profile.requests_per_ten = self.requests_per_ten

        self.port_util = realm.PortUtils(self.local_realm)

    def __check_request_rate(self):
        endp_list = self.json_get("layer4/list?fields=urls/s")
        expected_passes = 0
        passes = 0
        if endp_list is not None and endp_list['endpoint'] is not None:
            endp_list = endp_list['endpoint']
            for item in endp_list:
                for name, info in item.items():
                    if name in self.cx_profile.created_cx.keys():
                        expected_passes += 1
                        if info['urls/s'] * self.requests_per_ten >= self.target_requests_per_ten * .9:
                            # print(name, info['urls/s'], info['urls/s'] * self.requests_per_ten, self.target_requests_per_ten * .9)
                            passes += 1

        return passes == expected_passes

    def build(self):
        # Build stations
        self.station_profile.use_security(self.security, self.ssid, self.password)
        print("Creating stations")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio, sta_names_=self.sta_list, debug=self.debug)
        self._pass("PASS: Station build finished")

        self.cx_profile.create(ports=self.station_profile.station_names, sleep_time=.5, debug_=self.debug, suppress_related_commands_=None)

    def start(self, print_pass=False, print_fail=False):
        self.port_util.set_ftp(port_name=self.local_realm.name_to_eid(self.upstream_port)[2], resource=1, on=True)
        temp_stas = self.sta_list.copy()

        self.station_profile.admin_up()
        if self.local_realm.wait_for_ip(temp_stas):
            self._pass("All stations got IPs", print_pass)
        else:
            self._fail("Stations failed to get IPs", print_fail)
            exit(1)
        self.cx_profile.start_cx()
        print("Starting test")
        curr_time = datetime.datetime.now()
        end_time = self.local_realm.parse_time(self.test_duration) + curr_time
        sleep_interval = self.local_realm.parse_time(self.test_duration) // 5
        passes = 0
        expected_passes = 0
        for test in range(self.num_tests):
            expected_passes += 1
            while curr_time < end_time:
                time.sleep(sleep_interval.total_seconds())
                curr_time = datetime.datetime.now()

            if self.cx_profile.check_errors(self.debug):
                if self.__check_request_rate():
                    passes += 1
                else:
                    self._fail("FAIL: Request rate did not exceed 90% target rate", print_fail)
                    break
            else:
                self._fail("FAIL: Errors found getting to %s " % self.url, print_fail)
                break
        if passes == expected_passes:
            self._pass("PASS: All tests passes", print_pass)

    def stop(self):
        self.cx_profile.stop_cx()
        self.port_util.set_ftp(port_name=self.local_realm.name_to_eid(self.upstream_port)[2], resource=1, on=False)
        self.station_profile.admin_down()

    def cleanup(self, sta_list):
        self.cx_profile.cleanup()
        self.station_profile.cleanup(sta_list)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=sta_list,
                                           debug=self.debug)


def main():
    lfjson_port = 8080
    parser = LFCliBase.create_basic_argparse(
        prog='test_ipv4_l4_urls_per_ten',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
                Create layer-4 endpoints to connect to an ftp server and test that urls/s are meeting or exceeding the target rate
                ''',

        description='''\
        test_ipv4_l4_ftp_urls_per_ten.py
--------------------
Generic command example:
python3 ./test_ipv4_l4_ftp_urls_per_ten.py --upstream_port eth1 \\
    --radio wiphy0 \\
    --num_stations 3 \\
    --security {open|wep|wpa|wpa2|wpa3} \\
    --ssid netgear \\
    --passwd admin123 \\
    --test_duration 2m \\ {2m | 30s | 3h | 1d ...etc}
    --interval 1s \\
    --mode   1      
                {"auto"   : "0",
                "a"      : "1",
                "b"      : "2",
                "g"      : "3",
                "abg"    : "4",
                "abgn"   : "5",
                "bgn"    : "6",
                "bg"     : "7",
                "abgnAC" : "8",
                "anAC"   : "9",
                "an"     : "10",
                "bgnAC"  : "11",
                "abgnAX" : "12",
                "bgnAX"  : "13",
    --ap "00:0e:8e:78:e1:76"
    --requests_per_ten 600 \\
    --num_tests 1 \\
    --url "ul ftp://lanforge:lanforge@10.40.0.1/example.txt  /home/lanforge/example.txt"
    --debug
            ''')
    optional = parser.add_argument_group('optional arguments')
    required = parser.add_argument_group('required arguments')
    required.add_argument('--security', help='WiFi Security protocol: < open | wep | wpa | wpa2 | wpa3 >', required=True)
    parser.add_argument('--requests_per_ten', help='--requests_per_ten number of request per ten minutes', default=600)
    parser.add_argument('--test_duration', help='--test duration of a single test', default=600)
    parser.add_argument('--num_tests', help='--num_tests number of tests to run. Each test runs 10 minutes', default=1)
    parser.add_argument('--url', help='--url specifies upload/download, address, and dest',
                        default="dl http://10.40.0.1 /dev/null")
    optional.add_argument('--mode',help='Used to force mode of stations')
    optional.add_argument('--ap',help='Used to force a connection to a particular AP')
    #parser.add_argument('--target_per_ten', help='--target_per_ten target number of request per ten minutes. test will check for 90 percent of this value',
                        #default=600)
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
                     upstream_port=args.upstream_port,
                     radio= args.radio,
                     security=args.security,
                     station_list=station_list,
                     url=args.url,
                     mode=args.mode,
                     ap=args.ap,
                     num_tests=args.num_tests,
                     requests_per_ten=args.requests_per_ten,
                     test_duration=args.test_duration,
                     _debug_on=args.debug)
    ip_test.cleanup(station_list)
    ip_test.build()
    ip_test.start()
    ip_test.stop()
    if not ip_test.passes():
        print(ip_test.get_fail_message())
        exit(1)
    time.sleep(30)
    ip_test.cleanup(station_list)
    if ip_test.passes():
        print("Full test passed, all endpoints met or exceeded 90 percent of the target rate")

if __name__ == "__main__":
    main()
