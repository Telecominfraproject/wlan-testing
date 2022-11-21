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
                 resource=1,
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
        self.timeout_sec = 60
        self.resource = resource
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

        # if self.outfile is not None:
        #     results = self.outfile[:-4]
        #     results = results + "-results.csv"
        #     self.csv_results_file = open(results, "w")
        #     self.csv_results_writer = csv.writer(self.csv_results_file, delimiter=",")

        # TODO: check for the various extentions 
        results = self.outfile
        if results.split('.')[-1] == '':
            logger.debug("report_file has no file extension will add .csv")

        # check the file extension and compare to the mode set

        self.csv_results_file = open(results, "w")
        self.csv_results_writer = csv.writer(self.csv_results_file, delimiter=",")


    def get_kpi_results(self):
        # make json call to get kpi results
        endp_list = self.json_get(
            "endp?fields=name,eid,delay,jitter,rx+rate,rx+rate+ll,rx+bytes,rx+drop+%25,rx+pkts+ll",
            debug_=False)
        logger.info("endp_list: {endp_list}".format(endp_list=endp_list))

    def get_csv_name(self):
        logger.info("self.csv_results_file {}".format(self.csv_results_file.name))
        return self.csv_results_file.name

    # Query all endpoints to generate rx and other stats, returned
    # as an array of objects.
    def get_rx_values(self):
        endp_list = self.json_get(
            "endp?fields=name,eid,delay,jitter,rx+rate,rx+rate+ll,rx+bytes,rx+drop+%25,rx+pkts+ll",
            debug_=True)
        # logger.info("endp_list: {endp_list}".format(endp_list=endp_list))
        endp_rx_drop_map = {}
        endp_rx_map = {}
        endps = []

        total_ul = 0
        total_ul_ll = 0
        total_dl = 0
        total_dl_ll = 0
        udp_dl = 0
        tcp_dl = 0
        udp_ul = 0
        tcp_ul = 0

        '''
        for e in self.cx_profile.created_endp.keys():
            our_endps[e] = e
        print("our_endps {our_endps}".format(our_endps=our_endps))
        '''
        for endp_name in endp_list['endpoint']:
            if endp_name != 'uri' and endp_name != 'handler':
                for item, endp_value in endp_name.items():
                    # if item in our_endps:
                    if True:
                        endps.append(endp_value)
                        logger.debug("endpoint: {item} value:\n".format(item=item))
                        # logger.debug(endp_value)
                        # logger.info("item {item}".format(item=item))

                        for value_name, value in endp_value.items():
                            if value_name == 'rx bytes':
                                endp_rx_map[item] = value
                                logger.info("rx_rate {value}".format(value=value))
                            if value_name == 'rx rate':
                                endp_rx_map[item] = value
                                logger.info("rx_rate {value}".format(value=value))
                            if value_name == 'rx rate ll':
                                endp_rx_map[item] = value
                                logger.info("rx_rate_ll {value}".format(value=value))
                            if value_name == 'rx pkts ll':
                                endp_rx_map[item] = value
                            if value_name == 'rx drop %':
                                endp_rx_drop_map[item] = value
                            if value_name == 'rx rate':

                                # This hack breaks for mcast or if someone names endpoints weirdly.
                                # logger.info("item: ", item, " rx-bps: ", value_rx_bps)
                                # info for upload test data
                                logger.info(self.traffic_type)
                                if self.traffic_type.endswith("udp") and item.endswith("0-A"):
                                    udp_ul += int(value)
                                    # logger.info(udp_ul)
                                elif self.traffic_type.endswith("udp") and item.endswith("1-A"):
                                    udp_ul += int(value)
                                    # logger.info(udp_ul)
                                elif self.traffic_type.endswith("tcp") and item.endswith("0-A"):
                                    tcp_ul += int(value)
                                    # logger.info(total_ul)
                                elif self.traffic_type.endswith("tcp") and item.endswith("1-A"):
                                    tcp_ul += int(value)
                                    # logger.info(total_ul)

                                # info for download test data
                                if self.traffic_type.endswith("udp") and item.endswith("0-B"):
                                    udp_dl += int(value)
                                    # logger.info(udp_dl)
                                elif self.traffic_type.endswith("udp") and item.endswith("1-B"):
                                    udp_dl += int(value)
                                    # logger.info(udp_dl)
                                elif self.traffic_type.endswith("tcp") and item.endswith("0-B"):
                                    tcp_dl += int(value)
                                    # logger.info(tcp_dl)
                                elif self.traffic_type.endswith("tcp") and item.endswith("1-B"):
                                    tcp_dl += int(value)
                                    # logger.info(tcp_dl)
                                # combine total download (tcp&udp) and upload (tcp&udp) test data
                                if item.endswith("-A"):
                                    total_ul += int(value)
                                    # logger.info(total_dl)
                                else:
                                    total_dl += int(value)
                                    # logger.info(total_ul)
                            if value_name == 'rx rate ll':
                                # This hack breaks for mcast or if someone
                                # names endpoints weirdly.
                                if item.endswith("-A"):
                                    total_ul_ll += int(value)
                                else:
                                    total_dl_ll += int(value)

        # logger.debug("total-dl: ", total_dl, " total-ul: ", total_ul, "\n")
        return endp_rx_map, endp_rx_drop_map, endps, udp_dl, tcp_dl, udp_ul, tcp_ul, total_dl, total_ul, total_dl_ll, total_ul_ll

    # Common code to generate timestamp for CSV files.
    def time_stamp(self):
        return time.strftime('%m_%d_%Y_%H_%M_%S', time.localtime(self.epoch_time))

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
        try:
            self.csv_add_column_headers()
        except:
            logger.debug("csv result file is None")
        temp_stas = self.station_profile.station_names.copy()
        # logger.info("temp_stas {temp_stas}".format(temp_stas=temp_stas))
        if self.wait_for_ip(temp_stas, ipv4=not self.ipv6, ipv6=self.ipv6, debug=self.debug):
            logger.debug("temp_stas {temp_stas}".format(temp_stas=temp_stas))
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            #self.exit_fail()
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

    def build(self):
        for i in range(len(self.upstream)):
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

            self.cx_profile.create(endp_type=self.traffic_type, side_a=self.sta_list[i],
                                       side_b=self.upstream[i],
                                       sleep_time=0)

    def run(self):
        if self.report_file is None:
            # new_file_path = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-h-%M-m-%S-s")).replace(':','-') + '_test_ip_variable_time'
            # create path name
            new_file_path = self.kpi_path
            # new_file_path = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-h-%M-m-%S-s")).replace(':','-') + \
            #                 '_test_ip_variable_time'  # create path name
            if os.path.exists('/home/lanforge/report-data'):
                path = os.path.join('/home/lanforge/report-data/', new_file_path)
                if os.path.exists(path):
                    pass
                else:
                    os.mkdir(path)
            else:
                logger.info(new_file_path)
                # curr_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                # curr_dir_path += '/py-scripts'
                # path = os.path.join(curr_dir_path, new_file_path)
                # os.mkdir(path)
            # systeminfopath = str(path) + '/systeminfo.txt'
            systeminfopath = str(new_file_path) + '/systeminfo.txt'

            if self.output_format in ['csv', 'json', 'html', 'hdf', 'stata', 'pickle', 'pdf', 'png', 'parquet',
                                      'xlsx']:
                # report_f = str(path) + '/data.' + self.output_format
                report_f = str(new_file_path) + '/data.' + self.output_format
                output = self.output_format
            else:
                logger.info(
                    'Not supporting this report format or cannot find report format provided. Defaulting to csv data file '
                    'output type, naming it data.csv.')
                # report_f = str(path) + '/data.csv'
                report_f = str(new_file_path) + '/data.csv'
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
            raise ValueError('Unable to find layer 3 connections.')

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

        # remove endpoints from layer3connections that do not begin with 'VT' prefix:
        logger.info(layer3connections)
        # convert layer3connections to list:
        split_l3_endps = layer3connections.split(",")
        # logger.info(split_l3_endps)
        new_l3_endps_list = []

        for item in split_l3_endps:
            if item.startswith('VT'):
                new_l3_endps_list.append(item)
                # logger.info(new_l3_endps_list)
                # convert new_l3_endps_list to str:
                layer3endps = ','.join(str(l3endps) for l3endps in new_l3_endps_list)
                # logger.info(layer3endps)
        # for i in range(len(self.upstream)):
        comp_sta_list = []
        list(map(comp_sta_list.extend,self.sta_list))
        self.cx_profile.monitor(layer3_cols=layer3_cols,
                                sta_list=comp_sta_list,
                                port_mgr_cols=port_mgr_cols,
                                report_file=report_f,
                                systeminfopath=systeminfopath,
                                duration_sec=self.test_duration,
                                monitor_interval_ms=monitor_interval,
                                created_cx=layer3endps,
                                output_format=output,
                                compared_report=compared_rept,
                                script_name='test_ip_variable_time',
                                debug=self.debug)

        # fill out data kpi.csv and results reports
        temp_stations_list = []
        temp_stations_list.extend(self.station_profile.station_names.copy())
        total_test = len(self.get_result_list())
        total_pass = len(self.get_passed_result_list())
        endp_rx_map, endp_rx_drop_map, endps, udp_dl, tcp_dl, udp_ul, tcp_ul, total_dl, total_ul, total_dl_ll, total_ul_ll = self.get_rx_values()
        self.record_kpi_csv(temp_stations_list, total_test, total_pass, udp_dl, tcp_dl, udp_ul, tcp_ul, total_dl, total_ul)
        self.record_results(len(temp_stations_list), udp_dl, tcp_dl, udp_ul, tcp_ul, total_dl, total_ul)

        self.stop()
        if not self.use_existing_sta:
            if not self.passes():
                logger.info(self.get_fail_message())
                self.exit_fail()

            if self.passes():
                self.success()

        logger.info(report_f)
        logger.info(compared_rept)
        logger.info(port_mgr_cols)
        logger.info(output)

        if not self.no_cleanup:
            self.cleanup()
        logger.info("Leaving existing stations...")
        logger.info("IP Variable Time Test Report Data: {}".format(report_f))

    def run_only(self):
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

    # builds test data into kpi.csv report
    def record_kpi_csv(
            self,
            tmp_sta_list,
            total_test,
            total_pass,
            udp_dl,
            tcp_dl,
            udp_ul,
            tcp_ul,
            total_dl,
            total_ul):
        '''

        logger.debug(
            "NOTE:  Adding kpi to kpi.csv, sta_count {sta_list}  total-download-bps:{total_dl}  upload: {total_ul}  bi-directional: {total}\n".format(
                sta_list=sta_list, total_dl=total_dl, total_ul=total_ul,
                total=(total_ul + total_dl)))

        logger.debug(
            "NOTE:  Adding kpi to kpi.csv, sta_count {sta_list}  total-download-bps:{total_dl_ll_bps}  upload: {total_ul_ll_bps}
                    bi-directional: {total_ll}\n".format(sta_list=sta_list, total_dl_ll_bps=total_dl_ll_bps, total_ul_ll_bps=total_ul_ll_bps,
                    total_ll=(total_ul_ll_bps + total_dl_ll_bps)))
        '''
        # the short description will allow for more data to show up in one test-tag graph

        sta_list = len(tmp_sta_list)
        # logic for Subtest-Pass & Subtest-Fail columns
        subpass_udp_dl = 0
        subpass_udp_ul = 0
        subpass_tcp_dl = 0
        subpass_tcp_ul = 0
        subfail_udp_dl = 1
        subfail_udp_ul = 1
        subfail_tcp_dl = 1
        subfail_tcp_ul = 1

        if udp_dl > 0:
            subpass_udp_dl = 1
            subfail_udp_dl = 0
        if udp_ul > 0:
            subpass_udp_ul = 1
            subfail_udp_ul = 0
        if tcp_dl > 0:
            subpass_tcp_dl = 1
            subfail_tcp_dl = 0
        if tcp_ul > 0:
            subpass_tcp_ul = 1
            subfail_tcp_ul = 0

        # logic for pass/fail column
        # total_test & total_pass values from lfcli_base.py
        if total_test == total_pass:
            pass_fail = "PASS"
        else:
            pass_fail = "FAIL"

        # mode = []
        for stas in tmp_sta_list:
            # logger.info(stas)
            entity_id = self.local_realm.name_to_eid(stas)
            # entity_id[0]=shelf, entity_id[1]=resource, entity_id[2]=port
            # logger.info(entity_id)
            resource_val = str(entity_id[1])

            sta_data = self.json_get("port/1/" + resource_val + "/" + entity_id[2], debug_=True)
            # logger.info("sta_data: {sta_data}".format(sta_data=sta_data))
            # get the wifi 802.11 mode from sta_data:
            mode = sta_data['interface']['mode']
            # logger.info(mode)
            '''
            for sta_info in sta_data['interface']:
                logger.info(sta_info)
                if sta_info == 'mode':
                    mode = sta_data['interface'][sta_info]
                    logger.info(mode)
            '''

        # logger.info("mode: {mode}".format(mode=mode))

        # kpi data for TCP download traffic
        if self.traffic_type.endswith("tcp"):
            results_dict = self.kpi_csv.kpi_csv_get_dict_update_time()
            results_dict['Graph-Group'] = "TCP Download Rate"
            results_dict['pass/fail'] = pass_fail
            results_dict['Subtest-Pass'] = subpass_tcp_dl
            results_dict['Subtest-Fail'] = subfail_tcp_dl
            results_dict['short-description'] = "Mode {mode}  TCP-DL {side_a_min_rate} bps  {sta_list} STA".format(mode=mode, side_a_min_rate=self.side_a_min_rate, sta_list=sta_list)
            results_dict['numeric-score'] = "{}".format(total_dl)
            results_dict['Units'] = "bps"
            self.kpi_csv.kpi_csv_write_dict(results_dict)

            # kpi data for TCP upload traffic
            results_dict['Graph-Group'] = "TCP Upload Rate"
            results_dict['pass/fail'] = pass_fail
            results_dict['Subtest-Pass'] = subpass_tcp_ul
            results_dict['Subtest-Fail'] = subfail_tcp_ul
            results_dict['short-description'] = "Mode {mode}  TCP-UL {side_a_min_rate} bps  {sta_list} STA".format(mode=mode, side_a_min_rate=self.side_a_min_rate, sta_list=sta_list)
            results_dict['numeric-score'] = "{}".format(total_ul)
            results_dict['Units'] = "bps"
            self.kpi_csv.kpi_csv_write_dict(results_dict)

        # kpi data for UDP download traffic
        elif self.traffic_type.endswith("udp"):
            results_dict = self.kpi_csv.kpi_csv_get_dict_update_time()
            results_dict['Graph-Group'] = "UDP Download Rate"
            results_dict['pass/fail'] = pass_fail
            results_dict['Subtest-Pass'] = subpass_udp_dl
            results_dict['Subtest-Fail'] = subfail_udp_dl
            results_dict['short-description'] = "Mode {mode}  UDP-DL {side_a_min_rate} bps  {sta_list} STA".format(mode=mode, side_a_min_rate=self.side_a_min_rate, sta_list=sta_list)
            results_dict['numeric-score'] = "{}".format(total_dl)
            results_dict['Units'] = "bps"
            self.kpi_csv.kpi_csv_write_dict(results_dict)

            # kpi data for UDP upload traffic
            results_dict['Graph-Group'] = "UDP Upload Rate"
            results_dict['pass/fail'] = pass_fail
            results_dict['Subtest-Pass'] = subpass_udp_ul
            results_dict['Subtest-Fail'] = subfail_udp_ul
            results_dict['short-description'] = "Mode {mode}  UDP-UL {side_a_min_rate} bps  {sta_list} STA".format(mode=mode, side_a_min_rate=self.side_a_min_rate, sta_list=sta_list)
            results_dict['numeric-score'] = "{}".format(total_ul)
            results_dict['Units'] = "bps"
            self.kpi_csv.kpi_csv_write_dict(results_dict)

    # record results for .html & .pdf reports
    def record_results(
            self,
            sta_count,
            udp_dl,
            tcp_dl,
            udp_ul,
            tcp_ul,
            total_dl_bps,
            total_ul_bps):

        dl = self.side_a_min_rate
        ul = self.side_b_min_rate

        tags = dict()
        tags['requested-ul-bps'] = ul
        tags['requested-dl-bps'] = dl
        tags['station-count'] = sta_count
        # tags['attenuation'] = atten
        tags["script"] = 'test_ip_variable_time'

        # now = str(datetime.datetime.utcnow().isoformat())

        if self.traffic_type.endswith("tcp"):
            if self.csv_results_file:
                row = [self.epoch_time, self.time_stamp(), sta_count,
                       ul, ul, dl, dl, tcp_ul, tcp_dl,
                       total_ul_bps, total_dl_bps, (total_ul_bps + total_dl_bps)
                       ]
                self.csv_results_writer.writerow(row)
                self.csv_results_file.flush()
        elif self.traffic_type.endswith("udp"):
            if self.csv_results_file:
                row = [self.epoch_time, self.time_stamp(), sta_count,
                       ul, ul, dl, dl, udp_ul, udp_dl,
                       total_ul_bps, total_dl_bps, (total_ul_bps + total_dl_bps)
                       ]
                self.csv_results_writer.writerow(row)
                self.csv_results_file.flush()

    def csv_generate_results_column_headers(self):
        if self.traffic_type.endswith("tcp"):
            csv_rx_headers = [
            'Time epoch',
            'Time',
            'Station-Count',
            'UL-Min-Requested',
            'UL-Max-Requested',
            'DL-Min-Requested',
            'DL-Max-Requested',
            # 'Attenuation',
            'TCP-Upload-bps',
            'TCP-Download-bps',
            'Total-TCP-Upload-bps',
            'Total-TCP-Download-bps',
            'Total-TCP-UL/DL-bps']
        elif self.traffic_type.endswith("udp"):
            csv_rx_headers = [
            'Time epoch',
            'Time',
            'Station-Count',
            'UL-Min-Requested',
            'UL-Max-Requested',
            'DL-Min-Requested',
            'DL-Max-Requested',
            # 'Attenuation',
            'UDP-Upload-bps',
            'UDP-Download-bps',
            'Total-UDP-Upload-bps',
            'Total-UDP-Download-bps',
            'Total-UDP-UL/DL-bps']

        return csv_rx_headers

    # Write initial headers to csv file.
    def csv_add_column_headers(self):
        if self.csv_results_file is not None:
            self.csv_results_writer.writerow(
                self.csv_generate_results_column_headers())
            self.csv_results_file.flush()


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
    --ssid <ssid>
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
    certain columns in the GUI in your final report, please match the according GUI column displayed to it's counterpart to have the additional columns correctly displayed
    in your report. Note that the report will prepend "l3-" to the supplied layer3_col flags.

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
    1. Use Existing station ,  Note: put the shelf.resource.wifi-sta  (below is 1.1.wlan4),
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
    
    4. Create Multiple stations and run traffic with different upstream port
    ./test_ip_variable_time.py --mgr 192.168.200.37  --radio wiphy0 wiphy0 --ssid ssid_2g ssid_5g 
        --test_duration 60s --output_format csv  --traffic_type lf_tcp --a_min 600000000 --b_min 600000000  
        --upstream_port eth2 eth1 --mode '5' --num_stations 1 --passwd pass_2g pass_5g --security wpa2 wpa2


            ''')
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
    optional.add_argument('--num_stations', type=int, default=0,
                          help='Number of stations to create')
    optional.add_argument('--test_id',
                          default="webconsole",
                          help='Test ID (intended to use for ws events)')
    optional.add_argument('-d', '--debug', action="store_true",
                          help='Enable debugging')
    optional.add_argument('--log_level', default=None,
                          help='Set logging level: debug | info | warning | error | critical')
    optional.add_argument('--lf_logger_config_json',
                          help="--lf_logger_config_json <json file> , json configuration of logger")
    optional.add_argument('--proxy', nargs='?', default=None,
                          help="Connection proxy like http://proxy.localnet:80 \n"
                               + " or https://user:pass@proxy.localnet:3128")
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
    optional.add_argument('--no_cleanup', help='Do not cleanup before exit',  action='store_true')

    #-----required---------------
    required.add_argument('--radio', nargs="+", help='radio EID, e.g: --radio wiphy0 wiphy2')
    required.add_argument('--security', nargs="+", default=["open"],
                          help='WiFi Security protocol: < open | wep | wpa | wpa2 | wpa3 >  e.g: --security open wpa')
    required.add_argument('--ssid', nargs="+", help='WiFi SSID for script objects to associate to e.g: --ssid ap1_ssid ap2_ssid')
    required.add_argument('--passwd', '--password', '--key', nargs="+", default=["[BLANK]"],
                          help='WiFi passphrase/password/key e.g: --passwd [BLANK] passwd@123')

    optional.add_argument('--mode', nargs="+", help='Used to force mode of stations e.g: --mode 11 9')
    optional.add_argument('--ap', nargs="+", help='Used to force a connection to a particular AP')
    optional.add_argument('--traffic_type', help='Select the Traffic Type [lf_udp, lf_tcp, udp, tcp], type will be '
                                               'adjusted automatically between ipv4 and ipv6 based on use of --ipv6 flag',
                        required=True)
    optional.add_argument('--output_format', help='choose either csv or xlsx')
    optional.add_argument('--report_file', help='where you want to store results', default=None)
    optional.add_argument('--a_min', help='--a_min bps rate minimum for side_a', default=256000)
    optional.add_argument('--b_min', help='--b_min bps rate minimum for side_b', default=256000)
    optional.add_argument('--test_duration', help='--test_duration sets the duration of the test', default="2m")
    optional.add_argument('--layer3_cols', help='Additional columns wished to be monitored from the layer 3 endpoint tab for reporting',
                        default=['name', 'tx bytes', 'rx bytes', 'tx rate', 'rx rate'])
    optional.add_argument('--port_mgr_cols', help='Additional columns wished to be monitored from port manager tab for reporting',
                        default=['alias', 'ap', 'ip', 'parent dev', 'rx-rate'])
    optional.add_argument('--compared_report', help='report path and file which is wished to be compared with new report',
                        default=None)
    optional.add_argument('--monitor_interval',
                        help='how frequently do you want your monitor function to take measurements, 35s, 2h',
                        default='10s')
    optional.add_argument('--ipv6', help='Sets the test to use IPv6 traffic instead of IPv4', action='store_true')
    optional.add_argument('--influx_host')
    optional.add_argument('--influx_token', help='Username for your Influx database')
    optional.add_argument('--influx_bucket', help='Password for your Influx database')
    optional.add_argument('--influx_org', help='Name of your Influx database')
    optional.add_argument('--influx_port', help='Port where your influx database is located', default=8086)
    optional.add_argument('--influx_tag', action='append', nargs=2,
                        help='--influx_tag <key> <val>   Can add more than one of these.')
    optional.add_argument('--influx_mgr',
                        help='IP address of the server your Influx database is hosted if different from your LANforge Manager',
                        default=None)
    parser.add_argument('--use_existing_sta', help='Used an existing stations to a particular AP', action='store_true')
    parser.add_argument('--sta_names', help='Used to force a connection to a particular AP', default="sta0000")
    parser.add_argument('--local_lf_report_dir',
                        help='--local_lf_report_dir override the report path, primary use when running test in test suite',
                        default="")
    parser.add_argument("--resource", type=str, help="LANforge Station resource ID to use, default is 1", default="1")

    # kpi_csv arguments:
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
        help="--csv_outfile <prepend input to generated file for csv data>",
        default="csv_outfile")

    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    # set the logger level to requested level
    logger_config.set_level(level=args.log_level)

    # lf_logger_config_json will take presidence to changing debug levels
    if args.lf_logger_config_json:
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()


    # for kpi.csv generation
    local_lf_report_dir = args.local_lf_report_dir
    test_rig = args.test_rig
    test_tag = args.test_tag
    dut_hw_version = args.dut_hw_version
    dut_sw_version = args.dut_sw_version
    dut_model_num = args.dut_model_num
    dut_serial_num = args.dut_serial_num
    # test_priority = args.test_priority  # this may need to be set per test
    test_id = args.test_id

    if local_lf_report_dir != "":
        report = lf_report.lf_report(
            _path=local_lf_report_dir,
            _results_dir_name="test_ip_variable_time",
            _output_html="test_ip_variable_time.html",
            _output_pdf="test_ip_variable_time.pdf")
    else:
        report = lf_report.lf_report(
            _results_dir_name="test_ip_variable_time",
            _output_html="test_ip_variable_time.html",
            _output_pdf="test_ip_variable_time.pdf")

    kpi_path = report.get_report_path()
    # kpi_filename = "kpi.csv"
    logger.info("kpi_path :{kpi_path}".format(kpi_path=kpi_path))

    kpi_csv = lf_kpi_csv.lf_kpi_csv(
        _kpi_path=kpi_path,
        _kpi_test_rig=test_rig,
        _kpi_test_tag=test_tag,
        _kpi_dut_hw_version=dut_hw_version,
        _kpi_dut_sw_version=dut_sw_version,
        _kpi_dut_model_num=dut_model_num,
        _kpi_dut_serial_num=dut_serial_num,
        _kpi_test_id=test_id)

    # if args.csv_outfile is None:
    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    csv_outfile = "{}_{}-test_ip_variable_time.csv".format(
        args.csv_outfile, current_time)
    csv_outfile = report.file_add_path(csv_outfile)
    logger.info("csv output file : {}".format(csv_outfile))

    if len(args.upstream_port) and len(args.radio) and len(args.ssid) and len(args.security) != len(args.passwd):
        raise ValueError(f"Upstream-ports - {args.upstream_port}\nradio - {args.radio}\nSSID - {args.ssid}\n"
                         f"Security - {args.security}\nPassword - {args.passwd}\n"
                         f"Value given to upstream_port,radio,ssid,security,passwd should be equal in number")
    num_sta = 1
    if args.num_stations:
        logger.info("one")
        num_sta = int(args.num_stations)
    if not args.use_existing_sta:
        logger.info("two")
        station_list = []
        for i in args.radio:
            station_list.append(LFUtils.portNameSeries(prefix_="R"+str(args.radio.index(i))+"-sta", start_id_=0, end_id_=num_sta - 1,
                                                  padding_number_=10000, radio=i))
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
                                 no_cleanup=args.no_cleanup,
                                 report_file=args.report_file,
                                 output_format=args.output_format,
                                 layer3_cols=args.layer3_cols,
                                 port_mgr_cols=args.port_mgr_cols,
                                 monitor_interval=args.monitor_interval,
                                 kpi_csv=kpi_csv,
                                 kpi_path=kpi_path,
                                 outfile=csv_outfile,
                                 influx_host=args.influx_host,
                                 influx_port=args.influx_port,
                                 influx_org=args.influx_org,
                                 influx_token=args.influx_token,
                                 influx_bucket=args.influx_bucket,
                                 influx_tag=args.influx_tag,
                                 compared_report=args.compared_report,
                                 ipv6=args.ipv6,
                                 traffic_type=args.traffic_type,
                                 resource=args.resource,
                                 _debug_on=args.debug)
    # work in progress - may delete in the future
    # ip_var_test.set_wifi_radio(radio=args.radio)
    ip_var_test.run()

    # Reporting Results (.pdf & .html)
    csv_results_file = ip_var_test.get_csv_name()
    logger.info("csv_results_file: {}".format(csv_results_file))
    # csv_results_file = kpi_path + "/" + kpi_filename
    report.set_title("L3 Test IP Variable Time")
    # report.build_banner()
    # report.set_table_title("L3 IP Variable Time Key Performance Indexes")

    report.build_banner_left()
    report.start_content_div2()

    report.set_obj_html("Objective", "The IP Variable Time Test is designed to test the performance of the "
                                     "Access Point by createing a variable number of stations with layer 3 "
                                     "cross-connects and enpoints. The test will then monitor for increased "
                                     "traffic at regular intervals, and if all stations increase traffic "
                                     "over the full test duration, the test will pass."
                                     )
    report.build_objective()

    test_setup_info = {
        "DUT Name": args.dut_model_num,
        "DUT Hardware Version": args.dut_hw_version,
        "DUT Software Version": args.dut_sw_version,
        "DUT Serial Number": args.dut_serial_num,
        "SSID": args.ssid,
    }

    report.set_table_title("Device Under Test Information")
    report.build_table_title()
    report.test_setup_table(value="Device Under Test", test_setup_data=test_setup_info)

    test_input_info = {
        "LANforge ip": args.mgr,
        "LANforge port": "8080",
        "LANforge resource": args.resource,
        "Upstream": args.upstream_port,
        "Radio": args.radio,
        "SSID": args.ssid,
        "Security": args.security,
        "Traffic Type": args.traffic_type,
        "Download bps": args.b_min,
        "Upload bps": args.a_min,
        "Test Duration": args.test_duration,
    }

    report.set_table_title("Test Configuration")
    report.build_table_title()
    report.test_setup_table(value="Test Configuration", test_setup_data=test_input_info)

    report.set_table_title("IP Variable Time Test Results")
    report.build_table_title()
    report.set_table_dataframe_from_csv(csv_results_file)
    report.build_table()
    report.write_html_with_timestamp()
    report.write_index_html()
    # report.write_pdf(_page_size = 'A3', _orientation='Landscape')
    # report.write_pdf_with_timestamp(_page_size='A4', _orientation='Portrait')
    report.write_pdf_with_timestamp(_page_size='A4', _orientation='Landscape')


if __name__ == "__main__":
    main()
