#!/usr/bin/env python3
"""
NAME: test_l4.py

PURPOSE:
test_l4.py will create stations and endpoints to generate and verify layer-4 traffic

This script will monitor the urls/s, bytes-rd, or bytes-wr attribute of the endpoints.
These attributes can be tested over FTP using a --ftp flag.
If the monitored value does not continually increase, this test will not pass.

This script replaces the functionality of test_ipv4_l4.py, test_ipv4_l4_ftp_upload.py, test_ipv4_l4_ftp_urls_per_ten.py,
test_ipv4_l4_ftp_wifi.py, test_ipv4_l4_urls_per_ten.py, test_ipv4_l4_urls_per_ten.py, test_ipv4_l4_wifi.py

EXAMPLE (urls/s):
    ./test_l4.py --upstream_port eth1 --radio wiphy0 --num_stations 3 --security {open|wep|wpa|wpa2|wpa3}
                 --ssid netgear --passwd admin123 --requests_per_ten 600 --mode   1 --num_tests 1 --test_type 'urls'
                 --url "dl http://10.40.0.1 /dev/null" --ap "00:0e:8e:78:e1:76" --target_per_ten 600 --output_format csv
                 --report_file ~/Documents/results.csv --test_duration 2m --debug

EXAMPLE (bytes-wr):
    ./test_l4.py --upstream_port eth1 --radio wiphy0 --num_stations 3 --security {open|wep|wpa|wpa2|wpa3}
                 --ssid netgear --passwd admin123 --test_duration 2m --url "ul http://10.40.0.1 /dev/null"
                 --requests_per_ten 600 --test_type bytes-wr --debug

EXAMPLE (bytes-rd):
    ./test_l4.py --upstream_port eth1 (optional) --radio wiphy0  (required) --num_stations 3 (optional)
                 --security {open|wep|wpa|wpa2|wpa3} (required) --ssid netgear (required)
                 --url "dl http://10.40.0.1 /dev/null" (required) --password admin123 (required)
                 --test_duration 2m (optional) --test_type bytes-rd --debug (optional)

EXAMPLE (ftp urls/s):
    ./test_l4.py --upstream_port eth1 --radio wiphy0 --num_stations 3 --security {open|wep|wpa|wpa2|wpa3}
                 --ssid netgear --passwd admin123 --test_duration 2m --interval 1s --mode 1 --ap "00:0e:8e:78:e1:76"
                 --requests_per_ten 600 --num_tests 1 --ftp --test_type 'urls'
                 --url "ul ftp://lanforge:lanforge@10.40.0.1/example.txt  /home/lanforge/example.txt" --debug

EXAMPLE (ftp bytes-wr):
    ./test_l4.py --upstream_port eth1 --radio wiphy0 --num_stations 3 --security {open|wep|wpa|wpa2|wpa3}
                 --ssid netgear --passwd admin123 --test_duration 2m --url "ul ftp://10.40.0.1 /dev/null"
                 --requests_per_ten 600 --ftp --test_type bytes-wr --debug

EXAMPLE (ftp bytes-rd):
    ./test_l4.py --upstream_port eth1 (optional) --radio wiphy0  (required) --num_stations 3 (optional)
                 --security {open|wep|wpa|wpa2|wpa3} (required) --ssid netgear (required)
                 --url "dl ftp://10.40.0.1 /dev/null" (required) --password admin123 (required)
                 --test_duration 2m (optional) --ftp --test_type bytes-rd --debug (optional)

Use './test_l4.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""
import sys
import os
import importlib
import time
import argparse
import datetime

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
TestGroupProfile = realm.TestGroupProfile
port_utils = importlib.import_module("py-json.port_utils")
PortUtils = port_utils.PortUtils
lf_kpi_csv = importlib.import_module("py-scripts.lf_kpi_csv")
lf_report = importlib.import_module("py-scripts.lf_report")


class IPV4L4(Realm):
    def __init__(self,
                 host="localhost",
                 port=8080,
                 ssid=None,
                 security=None,
                 password=None,
                 url=None,
                 ftp_user=None,
                 ftp_passwd=None,
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
                 ftp=False,
                 source=None,
                 dest=None,
                 test_type=None,
                 test_rig=None,
                 test_tag=None,
                 dut_hw_version=None,
                 dut_sw_version=None,
                 dut_model_num=None,
                 dut_serial_num=None,
                 test_id=None,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(lfclient_host=host, lfclient_port=port, debug_=_debug_on)

        self.host = host
        self.port = port
        self.radio = radio
        self.upstream_port = upstream_port
        self.ssid = ssid
        self.security = security
        self.password = password
        self.url = url
        self.mode = mode
        self.ap = ap
        self.debug = _debug_on
        self.requests_per_ten = int(requests_per_ten)
        self.number_template = number_template
        self.test_duration = test_duration
        self.sta_list = station_list
        self.num_tests = int(num_tests)
        self.target_requests_per_ten = int(target_requests_per_ten)

        self.station_profile = self.new_station_profile()
        self.cx_profile = self.new_l4_cx_profile()

        self.port_util = PortUtils(self)

        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.mode = self.mode
        self.test_type = test_type
        self.ftp_user = ftp_user
        self.ftp_passwd = ftp_passwd
        self.source = source
        self.dest = dest
        if self.ap is not None:
            self.station_profile.set_command_param("add_sta", "ap", self.ap)

        self.cx_profile.url = self.url
        self.cx_profile.test_type = self.test_type
        self.cx_profile.requests_per_ten = self.requests_per_ten
        self.cx_profile.target_requests_per_ten = self.target_requests_per_ten

        self.ftp = ftp
        if self.ftp and 'ftp://' not in self.url:
            print("WARNING! FTP test chosen, but ftp:// not present in url!")

        test_types = {'urls', 'bytes-wr', 'bytes-rd'}
        if self.test_type not in test_types:
            raise ValueError(
                "Unknown test type: %s\nValid test types are urls, bytes-rd, or bytes-wr" % self.test_type)

        self.report = lf_report.lf_report(_results_dir_name="test_l4", _output_html="ftp_test.html", _output_pdf="ftp_test.pdf")

        kpi_path = self.report.get_report_path()
        self.kpi_csv = lf_kpi_csv.lf_kpi_csv(
            _kpi_path=kpi_path,
            _kpi_test_rig=test_rig,
            _kpi_test_tag=test_tag,
            _kpi_dut_hw_version=dut_hw_version,
            _kpi_dut_sw_version=dut_sw_version,
            _kpi_dut_model_num=dut_model_num,
            _kpi_dut_serial_num=dut_serial_num,
            _kpi_test_id=test_id)

    def build(self):
        # Build stations
        self.station_profile.use_security(self.security, self.ssid, self.password)
        print("Creating stations")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio, sta_names_=self.sta_list, debug=self.debug)
        self._pass("PASS: Station build finished")

        temp_url = self.url.split(" ")
        if temp_url[0] == 'ul' or temp_url[0] == 'dl':
            if len(temp_url) == 2:
                if self.url.startswith("ul") and self.source not in self.url:
                    self.cx_profile.url += " " + self.source
                elif self.url.startswith("dl") and self.dest not in self.url:
                    self.cx_profile.url += " " + self.dest
        else:
            raise ValueError("ul or dl required in url to indicate direction")
        if self.ftp:
            if self.ftp_user is not None and self.ftp_passwd is not None:
                if ("%s:%s" % (self.ftp_user, self.ftp_passwd)) not in self.url:
                    temp_url = self.url.split("//")
                    temp_url = ("//%s:%s@" % (self.ftp_user, self.ftp_passwd)).join(temp_url)
                    self.cx_profile.url = temp_url
            self.cx_profile.create(ports=self.station_profile.station_names, sleep_time=.5, debug_=self.debug,
                                   suppress_related_commands_=True)
        else:
            self.cx_profile.create(ports=self.station_profile.station_names, sleep_time=.5, debug_=self.debug,
                                   suppress_related_commands_=None)

    def start(self, print_pass=False, print_fail=False):
        if self.ftp:
            self.port_util.set_ftp(port_name=self.name_to_eid(self.upstream_port)[2], resource=1, on=True)
        temp_stas = self.sta_list.copy()

        self.station_profile.admin_up()
        if self.wait_for_ip(temp_stas):
            self._pass("All stations got IPs", print_pass)
        else:
            self._fail("Stations failed to get IPs", print_fail)
            exit(1)

        self.cx_profile.start_cx()
        print("Starting test")

    def stop(self):
        cx_list = self.json_get('layer4/sta0000_l4,sta0001_l4?urls%2Fs,rx-bps')['endpoint']
        cx_map = dict()
        for sub in cx_list:
                for key in sub:
                    cx_map[key] = sub[key]
                cx_map[key].pop('name')
        print(cx_map)
        urls = 0
        rx_bps = 0

        for value in cx_map.values():
            urls += value['urls/s']
            rx_bps += value['rx rate']


        self.kpi_csv.kpi_csv_get_dict_update_time()
        self.kpi_csv.kpi_dict['Graph-Group'] = "Average URLs per Second"
        self.kpi_csv.kpi_dict['short-description'] = "Average URLs per Second"
        self.kpi_csv.kpi_dict['numeric-score'] = urls
        self.kpi_csv.kpi_dict['Units'] = "urls/s"
        self.kpi_csv.kpi_csv_write_dict(self.kpi_csv.kpi_dict)


        self.kpi_csv.kpi_dict['Graph-Group'] = "RX BPS"
        self.kpi_csv.kpi_dict['short-description'] = "RX BPS"
        self.kpi_csv.kpi_dict['numeric-score'] = rx_bps
        self.kpi_csv.kpi_dict['Units'] = "bps"
        self.kpi_csv.kpi_csv_write_dict(self.kpi_csv.kpi_dict)

        self.cx_profile.stop_cx()
        if self.ftp:
            self.port_util.set_ftp(port_name=self.name_to_eid(self.upstream_port)[2], resource=1, on=False)
        self.station_profile.admin_down()

    def cleanup(self, sta_list):
        self.cx_profile.cleanup()
        self.station_profile.cleanup(sta_list)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=sta_list,
                                           debug=self.debug)


def main():
    parser = Realm.create_basic_argparse(
        prog='test_l4',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
               This script will monitor the urls/s, bytes-rd, or bytes-wr attribute of the endpoints.
               ''',
        description='''\
---------------------------
Layer-4 Test Script - test_l4.py
---------------------------
Summary:
This script will create stations and endpoints to generate and verify layer-4 traffic by monitoring the urls/s, 
 bytes-rd, or bytes-wr attribute of the endpoints.
---------------------------
Generic command example:
./test_l4.py --mgr <ip_address> --upstream_port eth1 --radio wiphy0 --num_stations 3 --security wpa2 
--ssid <ssid> --passwd <password> --test_duration 2m --url "ul http://<ap_ip_address> /dev/null" 
--requests_per_ten 600 --test_type bytes-wr --debug
---------------------------

            ''')
    parser.add_argument('--requests_per_ten', help='--requests_per_ten number of request per ten minutes',
                        default=600)
    parser.add_argument('--num_tests', help='--num_tests number of tests to run. Each test runs 10 minutes',
                        default=1)
    parser.add_argument('--url', help='--url specifies upload/download, address, and dest',
                        default="dl http://10.40.0.1 /dev/null")
    parser.add_argument('--test_duration', help='duration of test', default="2m")
    parser.add_argument('--target_per_ten',
                        help='--target_per_ten target number of request per ten minutes. test will check for 90 percent this value',
                        default=600)
    parser.add_argument('--mode', help='Used to force mode of stations')
    parser.add_argument('--ap', help='Used to force a connection to a particular AP')
    parser.add_argument('--report_file', help='where you want to store results')
    parser.add_argument('--output_format', help='choose csv or xlsx')  # update once other forms are completed
    parser.add_argument('--ftp', help='Use ftp for the test', action='store_true')
    parser.add_argument('--test_type', help='Choose type of test to run {urls, bytes-rd, bytes-wr}',
                        default='bytes-rd')
    parser.add_argument('--ftp_user', help='--ftp_user sets the username to be used for ftp', default=None)
    parser.add_argument('--ftp_passwd', help='--ftp_user sets the password to be used for ftp', default=None)
    parser.add_argument('--dest',
                        help='--dest specifies the destination for the file, should be used when downloading',
                        default="/dev/null")
    parser.add_argument('--source',
                        help='--source specifies the source of the file, should be used when uploading',
                        default="/var/www/html/data_slug_4K.bin")
    # kpi_csv arguments
    parser.add_argument(
        "--test_rig",
        default="",
        help="test rig for kpi.csv, testbed that the tests are run on")
    parser.add_argument(
        "--test_tag",
        default="",
        help="test tag for kpi.csv,  test specific information to differenciate the test")
    parser.add_argument(
        "--dut_hw_version",
        default="",
        help="dut hw version for kpi.csv, hardware version of the device under test")
    parser.add_argument(
        "--dut_sw_version",
        default="",
        help="dut sw version for kpi.csv, software version of the device under test")
    parser.add_argument(
        "--dut_model_num",
        default="",
        help="dut model for kpi.csv,  model number / name of the device under test")
    parser.add_argument(
        "--dut_serial_num",
        default="",
        help="dut serial for kpi.csv, serial number / serial number of the device under test")
    parser.add_argument(
        "--test_priority",
        default="",
        help="dut model for kpi.csv,  test-priority is arbitrary number")
    parser.add_argument(
        '--csv_outfile',
        help="--csv_outfile <Output file for csv data>",
        default="")

    args = parser.parse_args()

    num_sta = 2
    if (args.num_stations is not None) and (int(args.num_stations) > 0):
        num_stations_converted = int(args.num_stations)
        num_sta = num_stations_converted
    if args.report_file is None:
        if args.output_format in ['csv', 'json', 'html', 'hdf', 'stata', 'pickle', 'pdf', 'parquet', 'png', 'df',
                                  'xlsx']:
            output_form = args.output_format.lower()
        else:
            print("Defaulting data file output type to Excel")
            output_form = 'xlsx'

    else:
        if args.output_format is None:
            output_form = str(args.report_file).split('.')[-1]
        else:
            output_form = args.output_format

            # Create directory
    if args.report_file is None:
        if os.path.isdir('/home/lanforge/report-data'):
            homedir = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")).replace(':', '-') + 'test_l4'
            path = os.path.join('/home/lanforge/report-data/', homedir)
            os.mkdir(path)
        else:
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            print('Saving file to local directory')
        if args.output_format in ['csv', 'json', 'html', 'hdf', 'stata', 'pickle', 'pdf', 'png', 'df', 'parquet',
                                  'xlsx']:
            rpt_file = path + '/data.' + args.output_format
        else:
            print('Defaulting data file output type to Excel')
            rpt_file = path + '/data.xlsx'
    else:
        rpt_file = args.report_file

    station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=num_sta - 1, padding_number_=10000,
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
                     ftp=args.ftp,
                     ftp_user=args.ftp_user,
                     ftp_passwd=args.ftp_passwd,
                     source=args.source,
                     dest=args.dest,
                     test_type=args.test_type,
                     _debug_on=args.debug,
                     test_duration=args.test_duration,
                     num_tests=args.num_tests,
                     target_requests_per_ten=args.target_per_ten,
                     requests_per_ten=args.requests_per_ten)
    ip_test.cleanup(station_list)
    ip_test.build()
    ip_test.start()

    layer4traffic = ','.join([[*x.keys()][0] for x in ip_test.json_get('layer4')['endpoint']])
    ip_test.cx_profile.monitor(col_names=['name', 'bytes-rd', 'urls/s', 'bytes-wr'],
                               report_file=rpt_file,
                               duration_sec=args.test_duration,
                               created_cx=layer4traffic,
                               output_format=output_form,
                               script_name='test_l4',
                               arguments=args,
                               debug=args.debug)
    ip_test.stop()
    if not ip_test.passes():
        print(ip_test.get_fail_message())
        exit(1)
    time.sleep(30)
    ip_test.cleanup(station_list)
    if ip_test.passes():
        print("Full test passed")


if __name__ == "__main__":
    main()
