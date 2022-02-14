#!/usr/bin/env python3
"""
NAME: test_ip_variable_time.py

PURPOSE:
test_ip_variable_time.py will create stations and endpoints to generate and verify layer-3 traffic over ipv4 or ipv6.
This script replaces the functionality of test_ipv4_variable_time.py and test_ipv6_variable_time.py
This Script has two working modes:
    Mode 1:
        When station is not available,

        This script will create a variable number of stations each with their own set of cross-connects and endpoints.
        It will then create layer 3 traffic over a specified amount of time, testing for increased traffic at regular intervals.
        This test will pass if all stations increase traffic over the full test duration.

    Mode 2:

        When station is already available This script will create layer3 cross-connects and endpoints It will then
        create layer 3 traffic over a specified amount of time, testing for increased traffic at regular intervals.
        This test will pass if all stations increase traffic over the full test duration.

Use './test_ip_variable_time.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""
import sys
import os
import importlib
import argparse
import datetime
import logging

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
InfluxRequest = importlib.import_module('py-dashboard.InfluxRequest')
RecordInflux = InfluxRequest.RecordInflux
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")


logger = logging.getLogger(__name__)


class IPVariableTime(Realm):
    def __init__(self,
                 ssid=None,
                 security=None,
                 password=None,
                 sta_list=None,
                 use_existing_sta=False,
                 name_prefix=None,
                 upstream=None,
                 radio=None,
                 host="localhost",
                 port=8080,
                 mode=0,
                 ap=None,
                 traffic_type=None,
                 side_a_min_rate=256000, side_a_max_rate=0,
                 side_b_min_rate=256000, side_b_max_rate=0,
                 number_template="00000",
                 test_duration="5m",
                 use_ht160=False,
                 report_file=None,
                 output_format=None,
                 layer3_cols=None,
                 port_mgr_cols=None,
                 monitor_interval='10s',
                 influx_host=None,
                 influx_port=None,
                 influx_org=None,
                 influx_token=None,
                 influx_bucket=None,
                 influx_tag=None,
                 compared_report=None,
                 ipv6=False,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        if sta_list is None:
            sta_list = []
        if layer3_cols is None:
            layer3_cols = ['name', 'tx bytes', 'rx bytes', 'tx rate', 'rx rate']
        super().__init__(lfclient_host=host,
                         lfclient_port=port,
                         debug_=_debug_on),
        self.upstream = upstream
        self.host = host
        self.port = port
        self.ssid = ssid
        self.sta_list = sta_list
        self.use_existing_sta = use_existing_sta
        self.security = security
        self.password = password
        self.radio = radio
        self.mode = mode
        self.ap = ap
        self.traffic_type = traffic_type
        self.number_template = number_template
        self.debug = _debug_on
        # self.json_post("/cli-json/set_resource", {
        #     "shelf":1,
        #     "resource":all,
        #     "max_staged_bringup": 30,
        #     "max_trying_ifup": 15,
        #     "max_station_bringup": 6
        # })

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
        if self.ap:
            self.station_profile.set_command_param("add_sta", "ap", self.ap)
        if self.use_existing_sta:
            self.station_profile.station_names = self.sta_list

        self.name_prefix = name_prefix
        self.test_duration = test_duration
        self.cx_profile = self.new_l3_cx_profile()
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.ipv6 = ipv6
        self.report_file = report_file
        self.output_format = output_format
        self.layer3_cols = layer3_cols
        self.port_mgr_cols = port_mgr_cols
        self.monitor_interval = monitor_interval
        self.influx_host = influx_host
        self.influx_port = influx_port
        self.influx_org = influx_org
        self.influx_token = influx_token
        self.influx_bucket = influx_bucket
        self.influx_tag = influx_tag
        self.compared_report = compared_report
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = side_a_min_rate
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate
        self.cx_profile.side_b_max_bps = side_b_max_rate

    def set_wifi_radio(self, country=0, resource=1, mode="NA", radio="wiphy6", channel=5):
        data = {
            "shelf": 1,
            "resource": resource,
            "radio": radio,
            "mode": mode,  # "NA", #0 for AUTO or "NA"
            "channel": channel,
            "country": 0,
            "frequency": super().channel_freq(channel_=channel)
        }
        super().json_post("/cli-json/set_wifi_radio", _data=data)

    def start(self):
        # if self.use_existing_station:
        # to-do- check here if upstream port got IP
        self.station_profile.admin_up()
        temp_stas = self.station_profile.station_names.copy()
        logger.info("temp_stas {temp_stas}".format(temp_stas=temp_stas))
        if self.wait_for_ip(temp_stas, ipv4=not self.ipv6, ipv6=self.ipv6, debug=self.debug):
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            self.exit_fail()
        self.cx_profile.start_cx()

    def stop(self):
        self.cx_profile.stop_cx()
        self.station_profile.admin_down()

    def pre_cleanup(self):
        self.cx_profile.cleanup_prefix()
        # do not clean up station if existed prior to test
        if not self.use_existing_sta:
            for sta in self.sta_list:
                self.rm_port(sta, check_exists=True, debug_=self.debug)

    def cleanup(self):
        self.cx_profile.cleanup()
        if not self.use_existing_sta:
            self.station_profile.cleanup()
            LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                               debug=self.debug)

    def build(self):
        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template(self.number_template)
        # logger.info("sta_list {}".format(self.sta_list))
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)

        if self.use_existing_sta:
            logger.info("Use Existing Stations: {sta_list}".format(sta_list=self.sta_list))
        else:
            logger.info("Creating stations")
            self.station_profile.create(radio=self.radio, sta_names_=self.sta_list, debug=self.debug)
            self._pass("PASS: Station build finished")

        self.cx_profile.create(endp_type=self.traffic_type, side_a=self.sta_list,
                               side_b=self.upstream,
                               sleep_time=0)

    def run(self):
        if self.report_file is None:
            new_file_path = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-h-%M-m-%S-s")).replace(':',
                                                                                                     '-') + '_test_ip_variable_time'  # create path name
            if os.path.exists('/home/lanforge/report-data'):
                path = os.path.join('/home/lanforge/report-data/', new_file_path)
                os.mkdir(path)
            else:
                curr_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                path = os.path.join(curr_dir_path, new_file_path)
                os.mkdir(path)
            systeminfopath = str(path) + '/systeminfo.txt'

            if self.output_format in ['csv', 'json', 'html', 'hdf', 'stata', 'pickle', 'pdf', 'png', 'parquet',
                                      'xlsx']:
                report_f = str(path) + '/data.' + self.output_format
                output = self.output_format
            else:
                logger.info(
                    'Not supporting this report format or cannot find report format provided. Defaulting to csv data file '
                    'output type, naming it data.csv.')
                report_f = str(path) + '/data.csv'
                output = 'csv'
        else:
            systeminfopath = str(self.report_file).split('/')[-1]
            report_f = self.report_file
            if self.output_format is None:
                output = str(self.report_file).split('.')[-1]
            else:
                output = self.output_format
        self.pre_cleanup()

        self.build()
        # exit()
        # CMR What is this code doing
        if not self.use_existing_sta:
            if not self.passes():
                logger.error(self.get_fail_message())
                self.exit_fail()

        try:
            layer3connections = ','.join([[*x.keys()][0] for x in self.json_get('endp')['endpoint']])
        except ValueError:
            raise ValueError('Try setting the upstream port flag if your device does not have an eth1 port')

        if type(self.layer3_cols) is not list:
            layer3_cols = list(self.layer3_cols.split(","))
            # send col names here to file to reformat
        else:
            layer3_cols = self.layer3_cols
            # send col names here to file to reformat
        if type(self.port_mgr_cols) is not list:
            port_mgr_cols = list(self.port_mgr_cols.split(","))
            # send col names here to file to reformat
        else:
            port_mgr_cols = self.port_mgr_cols
            # send col names here to file to reformat
        if self.debug:
            logger.debug("Layer 3 Endp column names are...")
            logger.debug(layer3_cols)
            logger.debug("Port Manager column names are...")
            logger.debug(port_mgr_cols)

        try:
            monitor_interval = Realm.parse_time(self.monitor_interval).total_seconds()
        except ValueError as error:
            logger.critical(error)
            logger.critical(
                "The time string provided for monitor_interval argument is invalid. Please see supported time stamp increments and inputs for monitor_interval in --help. ")
            return ValueError(
                "The time string provided for monitor_interval argument is invalid. Please see supported time stamp increments and inputs for monitor_interval in --help. ")
        self.start()

        if self.influx_org is not None:
            grapher = RecordInflux(_influx_host=self.influx_host,
                                   _influx_port=self.influx_port,
                                   _influx_org=self.influx_org,
                                   _influx_token=self.influx_token,
                                   _influx_bucket=self.influx_bucket)
            devices = [station.split('.')[-1] for station in self.sta_list]
            tags = dict()
            tags['script'] = 'test_ip_variable_time'
            if self.influx_tag:
                for k in self.influx_tag:
                    tags[k[0]] = k[1]
            grapher.monitor_port_data(longevity=Realm.parse_time(self.test_duration).total_seconds(),
                                      devices=devices,
                                      monitor_interval=Realm.parse_time(self.monitor_interval).total_seconds(),
                                      tags=tags)

        # Retrieve last data file
        compared_rept = None
        if self.compared_report:
            compared_report_format = self.compared_report.split('.')[-1]
            # if compared_report_format not in ['csv', 'json', 'dta', 'pkl','html','xlsx','parquet','h5']:
            if compared_report_format != 'csv':
                logger.critical("Cannot process this file type. Please select a different file and re-run script.")
                raise ValueError("Cannot process this file type. Please select a different file and re-run script.")
            else:
                compared_rept = self.compared_report

        self.cx_profile.monitor(layer3_cols=layer3_cols,
                                sta_list=self.sta_list,
                                port_mgr_cols=port_mgr_cols,
                                report_file=report_f,
                                systeminfopath=systeminfopath,
                                duration_sec=self.test_duration,
                                monitor_interval_ms=monitor_interval,
                                created_cx=layer3connections,
                                output_format=output,
                                compared_report=compared_rept,
                                script_name='test_ip_variable_time',
                                debug=self.debug)

        self.stop()
        if not self.use_existing_sta:
            if not self.passes():
                logger.info(self.get_fail_message())
                self.exit_fail()

            if self.passes():
                self.success()
        self.cleanup()
        logger.info("IP Variable Time Test Report Data: {}".format(report_f))


def main():
    # Realm args parser is one directory up then traverse into /py-json/LANforge/lfcli_base.py
    # search for create_basic_argsparse
    # --mgr --mgr_port --upstream_port --num_stations --radio --security --ssid --passwd
    parser = Realm.create_basic_argparse(
        prog='test_ip_variable_time.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            Create stations to test connection and traffic on VAPs of varying security types (WEP, WPA, WPA2, WPA3, Open)
            over ipv4 or ipv6
            ''',
        description='''\
test_ip_variable_time.py:
--------------------
Report:
The report will be in /home/lanforge/report-data/<timestamp>_test_ip_variable_time .
if the directory it not present it "should" place it in the local directory from where the script was run.

Generic command layout:

python3 ./test_ip_variable_time.py
    --upstream_port eth1
    --radio wiphy0
    --num_stations 32
    --security {open|wep|wpa|wpa2|wpa3}
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
        "bgnAX"  : "13"}
    --ssid netgear
    --password admin123
    --test_duration 2m (default)
    --monitor_interval_ms
    --a_min 3000
    --b_min 1000
    --ap "00:0e:8e:78:e1:76"
    --output_format csv
    --traffic_type lf_udp
    --report_file ~/Documents/results.csv                       (Example of csv file output  - please use another extension for other file formats)
    --compared_report ~/Documents/results_prev.csv              (Example of csv file retrieval - please use another extension for other file formats) - UNDER CONSTRUCTION
    --layer3_cols 'name','tx bytes','rx bytes','dropped'          (column names from the GUI to print on report -  please read below to know what to put here according to preferences)
    --port_mgr_cols 'ap','ip'                                    (column names from the GUI to print on report -  please read below to know what to put here according to preferences)
    --debug

    python3 ./test_ip_variable_time.py
    --upstream_port eth1        (upstream Port)
    --traffic_type lf_udp       (traffic type, lf_udp | lf_tcp)
    --test_duration 5m          (duration to run traffic 5m --> 5 Minutes)
    --create_sta False          (False, means it will not create stations and use the sta_names specified below)
    --sta_names sta000,sta001,sta002 (used if --create_sta False, comma separated names of stations)

    Example Command:
    python3  ./test_ip_variable_time.py  --mgr 192.168.100.116 --radio wiphy1
        --ssid asus11ax-5 --passwd hello123 --security wpa2 --test_duration 60s
        --output_format excel  --traffic_type lf_tcp --a_min 1000000 --b_min 1000000
        --upstream_port eth2  --mode "5" --layer3_cols 'name','tx rate','rx rate'
        --port_mgr_cols 'alias','channel','activity','mode'

===============================================================================
 ** FURTHER INFORMATION **
    Using the layer3_cols flag:

    Currently the output function does not support inputting the columns in layer3_cols the way they are displayed in the GUI. This quirk is under construction. To output
    certain columns in the GUI in your final report, please match the according GUI column display to it's counterpart to have the columns correctly displayed in
    your report.

    GUI Column Display       Layer3_cols argument to type in (to print in report)

    Name                |  'name'
    EID                 |  'eid'
    Run                 |  'run'
    Mng                 |  'mng'
    Script              |  'script'
    Tx Rate             |  'tx rate'
    Tx Rate (1 min)     |  'tx rate (1&nbsp;min)'
    Tx Rate (last)      |  'tx rate (last)'
    Tx Rate LL          |  'tx rate ll'
    Rx Rate             |  'rx rate'
    Rx Rate (1 min)     |  'rx rate (1&nbsp;min)'
    Rx Rate (last)      |  'rx rate (last)'
    Rx Rate LL          |  'rx rate ll'
    Rx Drop %           |  'rx drop %'
    Tx PDUs             |  'tx pdus'
    Tx Pkts LL          |  'tx pkts ll'
    PDU/s TX            |  'pdu/s tx'
    Pps TX LL           |  'pps tx ll'
    Rx PDUs             |  'rx pdus'
    Rx Pkts LL          |  'pps rx ll'
    PDU/s RX            |  'pdu/s tx'
    Pps RX LL           |  'pps rx ll'
    Delay               |  'delay'
    Dropped             |  'dropped'
    Jitter              |  'jitter'
    Tx Bytes            |  'tx bytes'
    Rx Bytes            |  'rx bytes'
    Replays             |  'replays'
    TCP Rtx             |  'tcp rtx'
    Dup Pkts            |  'dup pkts'
    Rx Dup %            |  'rx dup %'
    OOO Pkts            |  'ooo pkts'
    Rx OOO %            |  'rx ooo %'
    RX Wrong Dev        |  'rx wrong dev'
    CRC Fail            |  'crc fail'
    RX BER              |  'rx ber'
    CX Active           |  'cx active'
    CX Estab/s          |  'cx estab/s'
    1st RX              |  '1st rx'
    CX TO               |  'cx to'
    Pattern             |  'pattern'
    Min PDU             |  'min pdu'
    Max PDU             |  'max pdu'
    Min Rate            |  'min rate'
    Max Rate            |  'max rate'
    Send Buf            |  'send buf'
    Rcv Buf             |  'rcv buf'
    CWND                |  'cwnd'
    TCP MSS             |  'tcp mss'
    Bursty              |  'bursty'
    A/B                 |  'a/b'
    Elapsed             |  'elapsed'
    Destination Addr    |  'destination addr'
    Source Addr         |  'source addr'

    Using the port_mgr_cols flag:
         '4way time (us)'
         'activity'
         'alias'
         'anqp time (us)'
         'ap'
         'beacon'
         'bps rx'
         'bps rx ll'
         'bps tx'
         'bps tx ll'
         'bytes rx ll'
         'bytes tx ll'
         'channel'
         'collisions'
         'connections'
         'crypt'
         'cx ago'
         'cx time (us)'
         'device'
         'dhcp (ms)'
         'down'
         'entity id'
         'gateway ip'
         'ip'
         'ipv6 address'
         'ipv6 gateway'
         'key/phrase'
         'login-fail'
         'login-ok'
         'logout-fail'
         'logout-ok'
         'mac'
         'mask'
         'misc'
         'mode'
         'mtu'
         'no cx (us)'
         'noise'
         'parent dev'
         'phantom'
         'port'
         'port type'
         'pps rx'
         'pps tx'
         'qlen'
         'reset'
         'retry failed'
         'rx bytes'
         'rx crc'
         'rx drop'
         'rx errors'
         'rx fifo'
         'rx frame'
         'rx length'
         'rx miss'
         'rx over'
         'rx pkts'
         'rx-rate'
         'sec'
         'signal'
         'ssid'
         'status'
         'time-stamp'
         'tx abort'
         'tx bytes'
         'tx crr'
         'tx errors'
         'tx fifo'
         'tx hb'
         'tx pkts'
         'tx wind'
         'tx-failed %'
         'tx-rate'
         'wifi retries'

    Can't decide what columns to use? You can just use 'all' to select all available columns from both tables.

    This script uses two args parsers one in the script the second is Realm args parser
    Realm args parser is one directory up then traverse into /py-json/LANforge/lfcli_base.py
    search for create_basic_argsparse
     --mgr --mgr_port --upstream_port --num_stations --radio --security --ssid --passwd


    Example command:
    1. Use Existing station ,  Note: put the resource.shelf.wifi-sta  (below is 1.1.wlan4),
        The station needs to configured with the ssid, passwd, security and mode in the LANforge GUI
    ./test_ip_variable_time.py  --mgr 192.168.0.100  --radio wiphy4 --ssid ssid_5g --passwd pass_5g
        --security wpa2 --test_duration 60s --output_format csv  --traffic_type lf_tcp
        --a_min 600000000 --b_min 600000000  --upstream_port eth2 --mode '5'
        --layer3_cols 'name','tx rate','rx rate'  --port_mgr_cols 'alias','channel','activity','mode'
        --use_existing_sta --sta_names 1.1.wlan4

    2. Create a one station (script default is 1 if --num_stations not entered)
    ./test_ip_variable_time.py  --mgr 192.168.0.100    --radio wiphy6 --ssid ssid_5g --passwd pass_5g
        --security wpa2 --test_duration 60s --output_format csv  --traffic_type lf_tcp
        --a_min 600000000 --b_min 600000000  --upstream_port eth2 --mode '5'
        --layer3_cols 'name','tx rate','rx rate'  --port_mgr_cols 'alias','channel','activity','mode'

    3. Create two stations
    ./test_ip_variable_time.py  --mgr 192.168.0.100    --radio wiphy1 --ssid ssid_5g --passwd pass_5g
        --security wpa2 --test_duration 60s --output_format csv  --traffic_type lf_tcp
        --a_min 600000000 --b_min 600000000  --upstream_port eth2 --mode '5'
        --layer3_cols 'name','tx rate','rx rate'  --port_mgr_cols 'alias','channel','activity','mode'
        --num_stations 2

            ''')

    # Realm args parser is one directory up then traverse into /py-json/LANforge/lfcli_base.py
    # search for create_basic_argsparse
    # --mgr --mgr_port --upstream_port --num_stations --radio --security --ssid --passwd
    parser.add_argument('--mode', help='Used to force mode of stations')
    parser.add_argument('--ap', help='Used to force a connection to a particular AP')
    parser.add_argument('--traffic_type', help='Select the Traffic Type [lf_udp, lf_tcp, udp, tcp], type will be '
                                               'adjusted automatically between ipv4 and ipv6 based on use of --ipv6 flag',
                        required=True)
    parser.add_argument('--output_format', help='choose either csv or xlsx')
    parser.add_argument('--report_file', help='where you want to store results', default=None)
    parser.add_argument('--a_min', help='--a_min bps rate minimum for side_a', default=256000)
    parser.add_argument('--b_min', help='--b_min bps rate minimum for side_b', default=256000)
    parser.add_argument('--test_duration', help='--test_duration sets the duration of the test', default="2m")
    parser.add_argument('--layer3_cols', help='Columns wished to be monitored from layer 3 endpoint tab',
                        default=['name', 'tx bytes', 'rx bytes', 'tx rate', 'rx rate'])
    parser.add_argument('--port_mgr_cols', help='Columns wished to be monitored from port manager tab',
                        default=['alias', 'ap', 'ip', 'parent dev', 'rx-rate'])
    parser.add_argument('--compared_report', help='report path and file which is wished to be compared with new report',
                        default=None)
    parser.add_argument('--monitor_interval',
                        help='how frequently do you want your monitor function to take measurements, 35s, 2h',
                        default='10s')
    parser.add_argument('--ipv6', help='Sets the test to use IPv6 traffic instead of IPv4', action='store_true')
    parser.add_argument('--influx_host')
    parser.add_argument('--influx_token', help='Username for your Influx database')
    parser.add_argument('--influx_bucket', help='Password for your Influx database')
    parser.add_argument('--influx_org', help='Name of your Influx database')
    parser.add_argument('--influx_port', help='Port where your influx database is located', default=8086)
    parser.add_argument('--influx_tag', action='append', nargs=2,
                        help='--influx_tag <key> <val>   Can add more than one of these.')
    parser.add_argument('--influx_mgr',
                        help='IP address of the server your Influx database is hosted if different from your LANforge Manager',
                        default=None)
    parser.add_argument('--use_existing_sta', help='Used an existing stationsto a particular AP', action='store_true')
    parser.add_argument('--sta_names', help='Used to force a connection to a particular AP', default="sta0000")
    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    # set the logger level to requested level
    logger_config.set_level(level=args.log_level)

    # lf_logger_config_json will take presidence to changing debug levels
    if args.lf_logger_config_json:
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()

    num_sta = 1
    if args.num_stations:
        logger.info("one")
        num_sta = int(args.num_stations)
    if not args.use_existing_sta:
        logger.info("two")
        station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=num_sta - 1,
                                              padding_number_=10000,
                                              radio=args.radio)
    else:
        logger.info("three")
        station_list = args.sta_names.split(",")

    logger.info("args.num_stations: {create}".format(create=args.num_stations))
    logger.info("args.sta_names: {create}".format(create=args.sta_names))
    logger.info("args.use_existing_sta: {create} {typeof}".format(create=args.use_existing_sta, typeof=type(args.use_existing_sta)))
    logger.info("station_list: {sta}".format(sta=station_list))

    # Create directory
    # if file path with output file extension is not given...
    # check if home/lanforge/report-data exists. if not, save
    # in new folder based in current file's directory

    CX_TYPES = ("tcp", "udp", "lf_tcp", "lf_udp")

    if not args.traffic_type or (args.traffic_type not in CX_TYPES):
        logger.error("cx_type needs to be lf_tcp, lf_udp, tcp, or udp, bye")
        exit(1)

    if args.ipv6:
        if args.traffic_type == "tcp" or args.traffic_type == "lf_tcp":
            args.traffic_type = "lf_tcp6"
        if args.traffic_type == "udp" or args.traffic_type == "lf_udp":
            args.traffic_type = "lf_udp6"
    else:
        if args.traffic_type == "tcp":
            args.traffic_type = "lf_tcp"
        if args.traffic_type == "udp":
            args.traffic_type = "lf_udp"

    ip_var_test = IPVariableTime(host=args.mgr,
                                 port=args.mgr_port,
                                 number_template="0000",
                                 sta_list=station_list,
                                 use_existing_sta=args.use_existing_sta,
                                 name_prefix="VT",
                                 upstream=args.upstream_port,
                                 ssid=args.ssid,
                                 password=args.passwd,
                                 radio=args.radio,
                                 security=args.security,
                                 test_duration=args.test_duration,
                                 use_ht160=False,
                                 side_a_min_rate=args.a_min,
                                 side_b_min_rate=args.b_min,
                                 mode=args.mode,
                                 ap=args.ap,
                                 report_file=args.report_file,
                                 output_format=args.output_format,
                                 layer3_cols=args.layer3_cols,
                                 port_mgr_cols=args.port_mgr_cols,
                                 monitor_interval=args.monitor_interval,
                                 influx_host=args.influx_host,
                                 influx_port=args.influx_port,
                                 influx_org=args.influx_org,
                                 influx_token=args.influx_token,
                                 influx_bucket=args.influx_bucket,
                                 influx_tag=args.influx_tag,
                                 compared_report=args.compared_report,
                                 ipv6=args.ipv6,
                                 traffic_type=args.traffic_type,
                                 _debug_on=args.debug)
    # work in progress - may delete in the future
    # ip_var_test.set_wifi_radio(radio=args.radio)
    ip_var_test.run()


if __name__ == "__main__":
    main()
