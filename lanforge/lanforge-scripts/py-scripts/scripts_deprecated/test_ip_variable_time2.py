#!/usr/bin/env python3
"""
NAME: test_ip_variable_time2.py

Note: If you want to create multiple layer3 traffic without disturbing existing layer3 traffic then this script can
 be used. for multiple layer3 on same time run this script on multiple terminals.

PURPOSE:
test_ip_variable_time2.py will create stations and endpoints to generate and verify layer-3 traffic over ipv4 or ipv6.
This script replaces the functionality of test_ipv4_variable_time.py and test_ipv6_variable_time.py
This Script has two working modes:
    Mode 1:
        When station is not available,

        This script will create a variable number of stations each with their own set of cross-connects and endpoints.
        It will then create layer 3 traffic over a specified amount of time, testing for increased traffic at regular intervals.
        This test will pass if all stations increase traffic over the full test duration.

        ex. --mgr 192.168.1.101 --radio wiphy1 --ssid vap --test_duration 60s --traffic_type lf_udp --a_min 600000000
        --b_min 600000000 --upstream_port vap0000 --mode '5' --num_stations 2

    Mode 2:

        When station is already available This script will create layer3 cross-connects and endpoints It will then
        create layer 3 traffic over a specified amount of time, testing for increased traffic at regular intervals.
        This test will pass if all stations increase traffic over the full test duration.

        ex. --mgr 192.168.1.101 --radio wiphy1 --ssid vap --test_duration 60s --traffic_type lf_udp --a_min 600000000
        --b_min 600000000 --upstream_port vap0000 --mode '5' --use_existing_sta --sta_names sta0000

Use './test_ip_variable_time.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""
import sys
import os
import importlib
import argparse
import logging
import time
import csv

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
lf_report = importlib.import_module("py-scripts.lf_report")
lf_graph = importlib.import_module("py-scripts.lf_graph")
lf_kpi_csv = importlib.import_module("py-scripts.lf_kpi_csv")

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
                 no_cleanup=None,
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
                 kpi_csv=None,
                 kpi_path=None,
                 outfile=None,
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
        self.no_cleanup = no_cleanup
        self.traffic_type = traffic_type
        self.side_a_min_rate = side_a_min_rate
        self.side_b_min_rate = side_b_min_rate
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
        # self.station_profile.mode = mode
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
        self.outfile = outfile
        self.kpi_csv = kpi_csv
        self.kpi_path = kpi_path
        self.epoch_time = int(time.time())
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
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)

        if self.outfile is not None:
            results = self.outfile[:-4]
            results = results + "-results.csv"
            self.csv_results_file = open(results, "w")
            self.csv_results_writer = csv.writer(self.csv_results_file, delimiter=",")

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
        # self.csv_add_column_headers()
        temp_stas = self.station_profile.station_names.copy()
        # logger.info("temp_stas {temp_stas}".format(temp_stas=temp_stas))
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
            for sta_list in self.sta_list:
                for sta in sta_list:
                    self.rm_port(sta, check_exists=True, debug_=self.debug)

    def cleanup(self):
        self.cx_profile.cleanup()
        if not self.use_existing_sta:
            self.station_profile.cleanup()
            LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                               debug=self.debug)

    def build(self, i):  # To use this function only to build stations
        if self.use_existing_sta:
            self.sta_list[i] = [self.sta_list[i]]
            logger.info("Use Existing Stations: {sta_list}".format(sta_list=self.sta_list))
            self.station_profile.station_names = self.sta_list[i]

        else:
            self.station_profile.use_security(self.security[i], self.ssid[i], self.password[i])
            self.station_profile.set_number_template(self.number_template)
            logger.info("sta_list {}".format(self.sta_list))
            self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
            self.station_profile.set_command_param("set_port", "report_timer", 1500)
            self.station_profile.set_command_flag("set_port", "rpt_timer", 1)

            logger.info("Creating stations")
            try:
                self.station_profile.mode = self.mode[i]
            except Exception as e:
                self.station_profile.mode = 0
            self.station_profile.create(radio=self.radio[i], sta_names_=self.sta_list[i], debug=self.debug)
            self._pass("PASS: Station build finished")

        # self.cx_profile.create(endp_type=self.traffic_type, side_a=self.sta_list[i],
        #                        side_b=self.upstream[i],
        #                        sleep_time=0)

    def create_cx_profile(self,i):
        self.cx_profile.create(endp_type=self.traffic_type, side_a=self.sta_list[i],
                               side_b=self.upstream[i],
                               sleep_time=0)

    def start_cx_profile(self):
        self.start()

    def run(self):


        # self.pre_cleanup()

        # self.build()
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

        split_l3_endps = layer3connections.split(",")
        new_l3_endps_list = []

        for item in split_l3_endps:
            if item.startswith('VT'):
                new_l3_endps_list.append(item)
                layer3endps = ','.join(str(l3endps) for l3endps in new_l3_endps_list)


        comp_sta_list = []
        list(map(comp_sta_list.extend, self.sta_list))
        self.cx_profile.monitor_without_disturbing_other_monitor(layer3_cols=layer3_cols,
                                sta_list=comp_sta_list,
                                port_mgr_cols=port_mgr_cols,
                                duration_sec=self.test_duration,
                                monitor_interval_ms=monitor_interval,
                                created_cx=layer3endps,
                                script_name='test_ip_variable_time2',
                                debug=self.debug)

        # fill out data kpi.csv and results reports
        temp_stations_list = []
        temp_stations_list.extend(self.station_profile.station_names.copy())

        self.stop()

        if not self.use_existing_sta:
            if not self.passes():
                logger.info(self.get_fail_message())
                self.exit_fail()

            if self.passes():
                self.success()

        if not self.no_cleanup:
            self.cleanup()
            logger.info("Leaving existing stations...")


def main():
    # Realm args parser is one directory up then traverse into /py-json/LANforge/lfcli_base.py
    # search for create_basic_argsparse
    # --mgr --mgr_port --upstream_port --num_stations --radio --security --ssid --passwd
    parser = argparse.ArgumentParser(
        prog='test_ip_variable_time.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            Create stations to test connection and traffic on VAPs of varying security types (WEP, WPA, WPA2, WPA3, Open)
            over ipv4 or ipv6
            ''',
        description='')

    optional = parser.add_argument_group('optional arguments')
    required = parser.add_argument_group('required arguments')
    # Realm args parser is one directory up then traverse into /py-json/LANforge/lfcli_base.py
    # search for create_basic_argsparse
    # --mgr --mgr_port --upstream_port --num_stations --radio --security --ssid --passwd
    optional.add_argument('--mgr', '--lfmgr', default='localhost',
                          help='hostname for where LANforge GUI is running')
    optional.add_argument('--mgr_port', '--port', default=8080,
                          help='port LANforge GUI HTTP service is running on')
    optional.add_argument('-u', '--upstream_port', nargs="+", default=['eth1'],
                          help='non-station port that generates traffic: <resource>.<port>, e.g: --u eth1 eth2')


    optional.add_argument('-d', '--debug', action="store_true",
                          help='Enable debugging')
    optional.add_argument('--log_level', default=None,
                          help='Set logging level: debug | info | warning | error | critical')

    optional.add_argument('--debugging', nargs="+", action="append",
                          help="Indicate what areas you would like express debug output:\n"
                               + " - digest - print terse indications of lanforge_api calls\n"
                               + " - json - print url and json data\n"
                               + " - http - print HTTP headers\n"
                               + " - gui - ask the GUI for extra debugging in responses\n"
                               + " - method:method_name - enable by_method() debugging (if present)\n"
                               + " - tag:tagname - enable matching by_tag() debug output\n"
                          )
    optional.add_argument('--debug_log', default=None,
                          help="Specify a file to send debug output to")

    optional.add_argument('--no_cleanup', help='Do not cleanup before exit', action='store_true')

    # -----required---------------
    required.add_argument('--radio', nargs="+", help='radio EID, e.g: --radio wiphy0 wiphy2')
    required.add_argument('--security', nargs="+", default=["open"],
                          help='WiFi Security protocol: < open | wep | wpa | wpa2 | wpa3 >  e.g: --security open wpa')
    required.add_argument('--ssid', nargs="+",
                          help='WiFi SSID for script objects to associate to e.g: --ssid ap1_ssid ap2_ssid')
    required.add_argument('--passwd', '--password', '--key', nargs="+", default=["[BLANK]"],
                          help='WiFi passphrase/password/key e.g: --passwd [BLANK] passwd@123')

    optional.add_argument('--mode', nargs="+", help='Used to force mode of stations e.g: --mode 11 9')
    optional.add_argument('--ap', nargs="+", help='Used to force a connection to a particular AP')
    optional.add_argument('--traffic_type', help='Select the Traffic Type [lf_udp, lf_tcp, udp, tcp], type will be '
                                                 'adjusted automatically between ipv4 and ipv6 based on use of --ipv6 flag',
                          required=True)

    optional.add_argument('--a_min', help='--a_min bps rate minimum for side_a', default=256000)
    optional.add_argument('--b_min', help='--b_min bps rate minimum for side_b', default=256000)
    optional.add_argument('--test_duration', help='--test_duration sets the duration of the test', default="2m")
    optional.add_argument('--layer3_cols', help='Columns wished to be monitored from layer 3 endpoint tab',
                          default=['name', 'tx bytes', 'rx bytes', 'tx rate', 'rx rate'])
    optional.add_argument('--port_mgr_cols', help='Columns wished to be monitored from port manager tab',
                          default=['alias', 'ap', 'ip', 'parent dev', 'rx-rate'])

    optional.add_argument('--monitor_interval',
                          help='how frequently do you want your monitor function to take measurements, 35s, 2h',
                          default='10s')
    optional.add_argument('--ipv6', help='Sets the test to use IPv6 traffic instead of IPv4', action='store_true')

    parser.add_argument('--use_existing_sta', help='Used an existing stations to a particular AP', action='store_true')
    parser.add_argument('--sta_names', help='Used to force a connection to a particular AP', default="sta0000")
    optional.add_argument('--num_stations', type=int, default=0,
                          help='Number of stations to create')

    args = parser.parse_args()


    if len(args.upstream_port) and len(args.radio) and len(args.ssid) and len(args.security) != len(args.passwd):
        raise ValueError(f"Upstream-ports - {args.upstream_port}\nradio - {args.radio}\nSSID - {args.ssid}\n"
                         f"Security - {args.security}\nPassword - {args.passwd}\n"
                         f"Value given to upstream_port,radio,ssid,security,passwd should be equal in number")
    num_sta = 1
    if args.num_stations:
        # logger.info("one")
        num_sta = int(args.num_stations)

    if not args.use_existing_sta:
        # logger.info("two")
        station_list = []

        for i in args.radio:

            station_list.append(LFUtils.portNameSeries(prefix_="R" + str(str(i)[-1]) + "-sta", start_id_=0,
                                                       end_id_=num_sta - 1,
                                                       padding_number_=10000, radio=i))
            print(station_list)

    else:
        logger.info("three")
        station_list = args.sta_names.split(",")


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
                                 no_cleanup=args.no_cleanup,
                                 layer3_cols=args.layer3_cols,
                                 port_mgr_cols=args.port_mgr_cols,
                                 monitor_interval=args.monitor_interval,
                                 ipv6=args.ipv6,
                                 traffic_type=args.traffic_type,
                                 _debug_on=args.debug)

    for i in range(len(args.radio)):
        ip_var_test.build(i)
        ip_var_test.create_cx_profile(i)

    ip_var_test.run()



if __name__ == "__main__":
    main()
