#!/usr/bin/env python3

"""
NAME: test_ipv4_l4_urls_per_ten.py

PURPOSE:
test_ipv4_l4_urls_per_ten.py will create stations and endpoints to generate and verify layer-4 traffic

This script will monitor the urls/s attribute of the endpoints. If the the monitored value does not continually increase, this test will not pass.

EXAMPLE:
./test_ipv4_l4_urls_per_ten.py --upstream_port eth1 --radio wiphy0 --num_stations 3 --security {open|wep|wpa|wpa2|wpa3}
    --ssid netgear --passwd admin123 --requests_per_ten 600 --mode   1 --num_tests 1 --url "dl http://10.40.0.1 /dev/null"
    --ap "00:0e:8e:78:e1:76" --target_per_ten 600 --output_format csv --report_file ~/Documents/results.csv --test_duration 2m
    --debug


Use './test_ipv4_l4_urls_per_ten.py --help' to see command line usage and options
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
from LANforge import LFUtils
import realm
import time
import datetime
from realm import TestGroupProfile


class IPV4L4(LFCliBase):
    def __init__(self, 
                host="localhost", 
                port=8080,  
                ssid=None, 
                security=None, 
                password=None, 
                url=None, 
                requests_per_ten=None, 
                station_list=None, 
                test_duration="2m",
                ap=None,
                mode=0,
                target_requests_per_ten=60, 
                number_template="00000", 
                num_tests=1, 
                radio="wiphy0",
                _debug_on=False, 
                upstream_port="eth1",
                _exit_on_error=False,
                _exit_on_fail=False):
        super().__init__(host, port, _debug=_debug_on, _exit_on_fail=_exit_on_fail)

        self.host = host
        self.port = port
        self.radio = radio
        self.upstream_port = upstream_port
        self.ssid = ssid
        self.security = security
        self.password = password
        self.url = url
        self.mode=mode
        self.ap=ap
        self.debug=_debug_on
        self.requests_per_ten = int(requests_per_ten)
        self.number_template = number_template
        self.test_duration=test_duration
        self.sta_list = station_list
        self.num_tests = int(num_tests)
        self.target_requests_per_ten = int(target_requests_per_ten)

        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.l4cxprofile=realm.L4CXProfile(lfclient_host=host,
                                        lfclient_port=port,local_realm=self.local_realm)
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
        self.cx_profile.requests_per_ten = self.requests_per_ten


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
        temp_stas = self.sta_list.copy()
        # temp_stas.append(self.local_realm.name_to_eid(self.upstream_port)[2])

        self.station_profile.admin_up()
        if self.local_realm.wait_for_ip(temp_stas):
            self._pass("All stations got IPs", print_pass)
        else:
            self._fail("Stations failed to get IPs", print_fail)
            exit(1)
        self.cx_profile.start_cx()
        print("Starting test...")
    
    def stop(self):
        self.cx_profile.stop_cx()
        self.station_profile.admin_down()

    def cleanup(self, sta_list):
        self.cx_profile.cleanup()
        self.station_profile.cleanup(sta_list)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=sta_list,
                                           debug=self.debug)


def main():
    parser = LFCliBase.create_basic_argparse(
        prog='test_ipv4_l4_urls_per_ten',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            Create layer-4 endpoints to connect to a url and test that urls/s are meeting or exceeding the target rate
                ''',
        description='''\
    test_ipv4_l4_urls_per_ten.py:
--------------------
Generic command example:
python3 ./test_ipv4_l4_urls_per_ten.py 
    --upstream_port eth1 \\
    --radio wiphy0 \\
    --num_stations 3 \\
    --security {open|wep|wpa|wpa2|wpa3} \\
    --ssid netgear \\
    --passwd admin123 \\
    --requests_per_ten 600 \\
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
                "bgnAX"  : "13"} \\
    --num_tests 1 \\
    --url "dl http://10.40.0.1 /dev/null" \\
    --ap "00:0e:8e:78:e1:76"
    --target_per_ten 600 \\
    --output_format csv \\
    --report_file ~/Documents/results.csv \\
    --test_duration 2m \\
    --debug
            ''')
    required = None
    for agroup in parser._action_groups:
        if agroup.title == "required arguments":
            required = agroup
    #if required is not None:

    optional = None
    for agroup in parser._action_groups:
        if agroup.title == "optional arguments":
            optional = agroup

    if optional is not None:
        optional.add_argument('--requests_per_ten', help='--requests_per_ten number of request per ten minutes', default=600)
        optional.add_argument('--num_tests', help='--num_tests number of tests to run. Each test runs 10 minutes', default=1)
        optional.add_argument('--url', help='--url specifies upload/download, address, and dest',default="dl http://10.40.0.1 /dev/null")
        optional.add_argument('--test_duration', help='duration of test',default="2m")
        optional.add_argument('--target_per_ten', help='--target_per_ten target number of request per ten minutes. test will check for 90 percent this value',default=600)
        optional.add_argument('--mode',help='Used to force mode of stations')
        optional.add_argument('--ap',help='Used to force a connection to a particular AP')
        optional.add_argument('--report_file',help='where you want to store results')
        optional.add_argument('--output_format', help='choose csv or xlsx') #update once other forms are completed
    
    args = parser.parse_args()

    num_sta = 2
    if (args.num_stations is not None) and (int(args.num_stations) > 0):
        num_stations_converted = int(args.num_stations)
        num_sta = num_stations_converted
    if args.report_file is None:
        if args.output_format in ['csv','json','html','hdf','stata','pickle','pdf','parquet','png','df','xlsx']:
            output_form=args.output_format.lower()
            print("Defaulting file output placement to /home/lanforge.")
            rpt_file='/home/data.' + output_form
        else:
            print("Defaulting data file output type to Excel")
            rpt_file='/home/lanforge/data.xlsx'
            output_form='xlsx'

    else:
        rpt_file=args.report_file
        if args.output_format is None:
            output_form=str(args.report_file).split('.')[-1]
        else:
            output_form=args.output_format 


    #Create directory
    if args.report_file is None:
        try:
            homedir = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")).replace(':','-')+'test_ipv4_l4_urls_per_ten'
            path = os.path.join('/home/lanforge/report-data/',homedir)
            os.mkdir(path)
        except:
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            print('Saving file to local directory')
    else:
        pass

    if args.report_file is None:
        if args.output_format in ['csv','json','html','hdf','stata','pickle','pdf','png','df','parquet','xlsx']:
            rpt_file=path+'/data.' + args.output_format
            output=args.output_format
        else:
            print('Defaulting data file output type to Excel')
            rpt_file=path+'/data.xlsx'
            output='xlsx'
    else:
        rpt_file=args.report_file
        if args.output_format is None:
            output=str(args.report_file).split('.')[-1]
        else:
            output=args.output_format


    station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=num_sta-1, padding_number_=10000,
                                          radio=args.radio)

    ip_test = IPV4L4(host=args.mgr, port=args.mgr_port,
                     ssid=args.ssid,
                     password=args.passwd,
                     radio=args.radio,
                     upstream_port=args.upstream_port,
                     security=args.security,
                     station_list=station_list,
                     url=args.url,
                     mode=args.mode,
                     ap=args.ap,
                     _debug_on=args.debug,
                     test_duration=args.test_duration,
                     num_tests=args.num_tests,
                     target_requests_per_ten=args.target_per_ten,
                     requests_per_ten=args.requests_per_ten)
    ip_test.cleanup(station_list)
    ip_test.build()
    ip_test.start()

    try:
        layer4traffic=','.join([[*x.keys()][0] for x in ip_test.local_realm.json_get('layer4')['endpoint']])
    except:
        pass
    ip_test.l4cxprofile.monitor(col_names=['bytes-rd', 'urls/s'],
                                report_file=rpt_file,
                                duration_sec=ip_test.local_realm.parse_time(args.test_duration).total_seconds(),
                                created_cx=layer4traffic,
                                output_format=output_form,
                                script_name='test_ipv4_l4_urls_per_ten', 
                                arguments=args,
                                debug=args.debug)
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
