#!/usr/bin/env python3

"""
throughput.py will create stations and layer-3 traffic to calculate the throughput of AP.

This script will create a VAP and apply some load by creating stations in AP's channel under VAP in order to make the channel
utilized after the channel utilized to specific level again create specific number of stations each with their own set of cross-connects and endpoints.
It will then create layer 3 traffic over a specified amount of time, testing for increased traffic at regular intervals.
This test will pass if all stations increase traffic over the full test duration.

Use './throughput_ver_2.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""

import sys
import importlib
import paramiko
import argparse
import pprint
from datetime import datetime
import time
import traceback
import os
import matplotlib.patches as mpatches
import pandas as pd
import logging

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
lf_report = importlib.import_module("py-scripts.lf_report")
lf_graph = importlib.import_module("py-scripts.lf_graph")
lf_kpi_csv = importlib.import_module("py-scripts.lf_kpi_csv")
logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")
create_bridge = importlib.import_module("py-scripts.create_bridge")
CreateBridge = create_bridge.CreateBridge

'''
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append(os.path.join(os.path.abspath('..'), 'py-json'))

import argparse
from LANforge import LFUtils
from realm import Realm
from LANforge import LFRequest
from station_profile import StationProfile
from LANforge import set_port
import throughput_report
#import create_vap
import time,datetime,traceback
import pandas as pd
from lf_report import lf_report
from lf_graph import lf_bar_graph
from lf_csv import lf_csv
'''

# this class create VAP, station, and traffic
class IPV4VariableTime(Realm):
    def __init__(self, ssid=None,   security=None,       password=None,   sta_list=[],   name_prefix=None,   upstream=None,
                 radio=None,        host="localhost",    port=8080,       mode=0,        ap=None,            side_a_min_rate= 56,
                 side_a_max_rate=0, side_b_min_rate=56,  side_b_max_rate=0,              number_template="00000",
                 test_duration="5m", use_ht160=False,    _debug_on=False,                _exit_on_error=False,
                 _exit_on_fail=False, _vap_radio=None,   _vap_list = 'vap0000', _dhcp = True ):
        super().__init__(lfclient_host=host, lfclient_port=port),
        self.upstream = upstream
        self.host = host
        self.port = port
        self.ssid = ssid
        self.sta_list = sta_list
        self.vap_list = _vap_list
        self.security = security
        self.password = password
        self.radio = radio
        self.vap_radio = _vap_radio
        self.mode = mode
        self.ap = ap
        self.number_template = number_template
        self.debug = _debug_on
        self.name_prefix = name_prefix
        self.test_duration = test_duration
        self._dhcp = _dhcp
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)

        # initializing station profile
        '''
        self.station_profile = StationProfile(lfclient_url=self.lfclient_url,   local_realm=super(), debug_=self.debug,     up=False,
                                              dhcp = self._dhcp,                ssid = self.ssid,    ssid_pass = self.password,
                                              security = self.security,         number_template_ = self.number_template,    use_ht160 = use_ht160)#self.new_station_profile()##
        '''
        self.station_profile = self.local_realm.new_station_profile()

        if self.station_profile.use_ht160:
            self.station_profile.mode = 9
        self.station_profile.mode = mode


        # initializing VAP profile
        self.vap_profile = self.new_vap_profile()
        self.vap_profile.vap_name = self.vap_list
        self.vap_profile.ssid = self.ssid
        self.vap_profile.security = self.security
        self.vap_profile.ssid_pass = self.password
        self.vap_profile.mode = self.mode
        if self.debug:
            logger.info("----- VAP List ----- ----- ----- ----- ----- ----- \n")
            pprint.pprint(self.vap_list)
            logger.info("---- ~VAP List ----- ----- ----- ----- ----- ----- \n")

        # initializing traffic profile
        self.cx_profile = self.new_l3_cx_profile()
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = side_a_min_rate
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate
        self.cx_profile.side_b_max_bps = side_b_max_rate


    def start(self, print_pass=False, print_fail=False):
        self.station_profile.admin_up() # admin up the stations
        # to-do- check here if upstream port got IP
        temp_stas = self.station_profile.station_names.copy()

        if self.wait_for_ip(temp_stas):
            logger.info("admin-up....")
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            self.exit_fail()
        self.cx_profile.start_cx()  # run the traffic

    def stop(self,trf = True, ad_dwn = True):
        if trf:
            self.cx_profile.stop_cx()   # stop the traffic
        if ad_dwn:
            self.station_profile.admin_down()   # admin down the stations

    def pre_cleanup(self):
        # deleting the previously created stations
        logger.info("clearing...")
        exist_sta = []
        for u in self.json_get("/port/?fields=port+type,alias")['interfaces']:
            if list(u.values())[0]['port type'] not in ['Ethernet', 'WIFI-Radio', 'NA']:
                exist_sta.append(list(u.values())[0]['alias'])
        self.station_profile.cleanup(desired_stations=exist_sta)
        # deleting the previously created traffic
        try:
            exist_l3 = list(filter(lambda cx_name: cx_name if (cx_name != 'handler' and cx_name != 'uri') else False,
                                   self.json_get("/cx/?fields=name")))
            list(map(lambda i: self.rm_cx(cx_name=i), exist_l3))
            list(map(lambda cx_name: [self.rm_endp(ename=i) for i in [f"{cx_name}-A", f"{cx_name}-B"]], exist_l3))
        except Exception as e:
            print("###",e,'###')

    def build_vaps(self,chn = 36):
        # create VAPs with static IP_addr, netmask, gateway_IP
        self.vap_profile.use_security(self.security, self.ssid, passwd=self.password)
        self.vap_profile.set_command_param("set_port", "ip_addr", "192.168.0.1")
        self.vap_profile.set_command_flag("set_port", "ip_address", 1)
        self.vap_profile.set_command_param("set_port", "netmask", "255.255.255.0")
        self.vap_profile.set_command_flag("set_port", "ip_Mask", 1)
        self.vap_profile.set_command_param("set_port", "gateway", "192.168.0.1")
        self.vap_profile.set_command_flag("set_port", "ip_gateway", 1)
        # self.vap_profile.set_command_param("set_port", "dhcp_client_id", "enabled")
        self.vap_profile.set_command_flag("set_port", "use_dhcp", 1)
        logger.info("Creating VAPs")
        '''
        self.vap_profile.create(resource = 1,   radio = self.vap_radio,     channel = int(chn),       up_ = True,     debug = False,
                                suppress_related_commands_ = True,          use_radius = True,  hs20_enable = False,
                                create_bridge = False)
        '''
        self.vap_profile.create(resource=1, radio=self.vap_radio, channel=int(chn), up=True, debug=False,
                                suppress_related_commands_=True, use_radius=True, hs20_enable=False)
        self._pass("PASS: VAP build finished")

        logger.info("Creating Bridge")
        self.create_bridge = CreateBridge(_host=args.mgr,
                                 _port=args.mgr_port,
                                 _bridge_list=bridge_list,
                                 _debug_on=args.debug,
                                 target_device=args.target_device)

    def build(self):
        # creating stations using static IP and DHCP enabled stations
        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template(self.number_template)
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        logger.info("Creating stations")
        start_ip = 2
        if self._dhcp:
            self.station_profile.create(radio=self.radio, sta_names_=self.sta_list, debug=self.debug)
        else:
            for sta_name in self.sta_list:
                ip = "192.168.0."+ str(start_ip)
                self.station_profile.set_command_param("set_port", "ip_addr", ip)
                self.station_profile.set_command_flag("set_port", "ip_address", 1)
                self.station_profile.set_command_param("set_port", "netmask", "255.255.255.0")
                self.station_profile.set_command_flag("set_port", "ip_Mask", 1)
                self.station_profile.set_command_param("set_port", "gateway", "192.168.0.1")
                self.station_profile.set_command_flag("set_port", "ip_gateway", 1)

                self.station_profile.create(radio=self.radio, sta_names_=[sta_name], debug=self.debug)
                start_ip += 1
        self.cx_profile.create(endp_type="lf_udp", side_a=self.station_profile.station_names, side_b=self.upstream, sleep_time=0)
        self._pass("PASS: Station build finished")

    def chn_util(self,ssh_root, ssh_passwd,channnel=0):
        # To find the channel utilization
        cmd = 'iwpriv wifi1vap0 get_chutil'     # command to get channel utilization
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ssh_root, 22, 'root', ssh_passwd)
            time.sleep(20)
            #ssh.exec_command(f"conf_set system:wlanSettings:wlanSettingTable:wlan1:channel {channnel}")
            stdout = ssh.exec_command(cmd)
            stdout = (((stdout[1].readlines())[0].split(':'))[1].split(' '))[0]
            print(stdout, "----- channel utilization")
            return int(stdout)
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            logger.info("#### %s ####", e)
            exit(1)
        except TimeoutError as e:
            # print("####", e, "####")
            exit(1)

    def re_run_traff(self, adj_trf_rate, add_sub_rate):
        # if channel utilization level is not met re-run the traffic
        logger.info("Re-run the traffic...")
        self.cx_profile.cleanup_prefix()
        time.sleep(.5)
        # give data rate to run the traffic
        if add_sub_rate == "sub":
            self.cx_profile.side_a_min_bps = abs(int(self.cx_profile.side_a_min_bps) - adj_trf_rate)
            self.cx_profile.side_b_min_bps = abs(int(self.cx_profile.side_b_min_bps) - adj_trf_rate)
        elif add_sub_rate == "add":
            self.cx_profile.side_a_min_bps = int(self.cx_profile.side_a_min_bps) + adj_trf_rate
            self.cx_profile.side_b_min_bps = int(self.cx_profile.side_b_min_bps) + adj_trf_rate
        self.cx_profile.created_cx.clear()
        self.cx_profile.create(endp_type="lf_udp", side_a=self.station_profile.station_names, side_b=self.upstream,
                               sleep_time=0)
        self.cx_profile.start_cx()
        print(f"-------side_a_min_bps  {self.cx_profile.side_a_min_bps}\n-------side_b_min_bps  {self.cx_profile.side_b_min_bps}")

    def table(self,report, title, data, dis=""):
        # creating table
        report.set_obj_html(_obj_title="",_obj=dis)
        report.set_table_title(title)
        report.build_table_title()
        report.build_objective()
        report.set_table_dataframe(data)
        report.build_table()

    def grph(self,report, dis="", data_set=None, xaxis_name="stations", yaxis_name="Throughput 2 (Mbps)",
             xaxis_categories=None, label=None, graph_image_name="", multi_bar_width = 0,
             xticks_font=10,step = 1):
        # creating bar graph
        report.set_obj_html(_obj_title=graph_image_name, _obj=dis)
        #report.set_graph_title(graph_image_name)
        #report.build_graph_title()
        report.build_objective()
        graph = lf_graph.lf_bar_graph(_data_set = data_set,
                             _xaxis_name = xaxis_name,
                             _yaxis_name = yaxis_name,
                             _xaxis_categories = xaxis_categories,
                             _graph_image_name = graph_image_name.replace(" ","_"),
                             _label = label,
                             _color = ['darkorange','forestgreen','blueviolet'],
                             _color_edge = 'black',
                             _figsize = (10, 5),
                             _xticks_font= xticks_font,_xaxis_value_location=multi_bar_width,
                             _xaxis_step = step,_legend_handles=None, _legend_loc="best", _legend_box=(1.0,0.5), _legend_ncol=1)
        graph_png = graph.build_bar_graph()
        logger.info("graph name {}".format(graph_png))
        report.set_graph_image(graph_png)
        report.move_graph_image()
        report.build_graph()

    def generates_csv(self, _columns=None, _rows=None, _filename='test.csv' ):
        if _columns is None:
            _columns = ['Stations', 'bk', 'be', 'vi', 'vo']
        if _rows is None:
            _rows = [['sta0001', 'sta0002', 'sta0003', 'sta0004', 'sta0005'],
                     [1, 2, 3, 4, 5],
                     [11, 22, 33, 44, 55],
                     [6, 7, 8, 9, 10],
                     [66, 77, 88, 99, 100]]
        rows = _rows
        columns = _columns
        filename = _filename

        df = {}
        for i in range(len(columns)):
            df[columns[i]] = rows[i]
        csv_df = pd.DataFrame(df)
        logger.info(csv_df)
        csv_df.to_csv(filename, index=False, encoding='utf-8', na_rep='NA', float_format='%.2f')

    def report(self,util, sta_num, bps_rx_a,bps_rx_b, rep_title, upload = 1000000, download = 1000000,
              test_setup_info = None,input_setup_info = None,threshold=None):
        '''if len(threshold) < len(util):
            for i in range(len(util)):
                try:
                    tmp = threshold[i]
                except IndexError as e:
                    print(f"Threshold {threshold} and utilization {util}")
                    threshold.append(100 - int(util[i]))
        print(f"threshold {threshold} and utilization {util}")'''
        rx_a,rx_b,pas_fail_up,pas_fail_down,pas_fail_info_up,pas_fail_info_down = [],[],[],[],[],[]
        thrp_b = upload * len(sta_num)  # get overall upload values
        thrp_a = download * len(sta_num)  # get overall download values
        print(f"given upload--{thrp_b} and download--{thrp_a} values")
        index = -1
        for a in bps_rx_a:
            index += 1
            if len(a):
                rx_a.append(f'Min: {min(a)} | Max: {max(a)} | Avg: {(sum(a) / len(a)):.2f} | Total: {sum(a):.2f}')
                if thrp_a:
                    print(f"Expected throughput for util-{util[index]} and threshold-{threshold[index]}---- "
                          f"{(thrp_a / 100) * (int(threshold[index]))} \nGot overall download values for util "
                          f"'{util[index]}'----- {sum(a)} \n ")
                    if (thrp_a / 100) * int(threshold[index]) <= sum(a) and min(a) != 0:
                        pas_fail_down.append(f"PASS")# {len(sta_num)}-stations ran download traffic and met threshold")
                        #pas_fail_info_down.append(f"")
                    else:
                        pas_fail_down.append(f"FAIL")# {a.count(0)}-stations got zero throughput and overall throughput- {sum(a):.2f}")
                        #pas_fail_info_down.append(f"")
            else:
                pas_fail_down.append("NA")
                rx_a.append(0)

            if len(bps_rx_b[index]):
                rx_b.append(f'Min: {min(bps_rx_b[index])} | Max: {max(bps_rx_b[index])} | '
                            f'Avg: {(sum(bps_rx_b[index]) / len(bps_rx_b[index])):.2f} | Total: {sum(bps_rx_b[index]):.2f}')
                if thrp_b:
                    print(f"Expected throughput for util-{util[index]} and threshold-{threshold[index]}---- "
                          f"{(thrp_b / 100) * (int(threshold[index]))} \nGot overall upload values for util "
                          f"'{util[index]}'----- {sum(bps_rx_b[index])} \n ")
                    if (thrp_b / 100) * int(threshold[index]) <= sum(bps_rx_b[index]) and min(bps_rx_b[index])!= 0:
                        pas_fail_up.append(f"PASS")# {len(sta_num)}-stations ran upload traffic and met threshold")
                        #pas_fail_info_up.append()
                    else:
                        pas_fail_up.append(f"FAIL")# {bps_rx_b[index].count(0)}-stations got zero throughput and overall throughput- "
                                           #f"{sum(bps_rx_b[index]):.2f}")
                        #pas_fail_info_up.append(f"")
            else:
                pas_fail_up.append("NA")
                rx_b.append(0)

            util[index] = f'{util[index]}%'  # append % to the util values

        overall_tab = pd.DataFrame({
            'Channel Utilization (%)': util, "No.of.clients": [len(sta_num)] * len(util),
            'Intended Throughput(Mbps)': [f'upload: {upload} | download: {download}'] * len(util),
            'Achieved Upload Throughput(Mbps)': rx_b, 'Achieved Download Throughput(Mbps)': rx_a
        })
        print(f"overall table \n{overall_tab}")

        pasfail_tab = pd.DataFrame({
            'Channel Utilization (%)': util,
            'Upload': pas_fail_up,
            'Download': pas_fail_down
        })
        print(f"pass-fail table \n {pasfail_tab}")
        report = lf_report(_results_dir_name="Throughput_Under_Channel_Load",_output_html="throughput_channel_load.html",
                           _output_pdf="throughput_channel_load.pdf")
        report.set_title(rep_title)
        report.build_banner()
        report.set_obj_html(_obj_title="Objective",
                            _obj=f"This test is designed to measure the throughput of {len(sta_num)} clients connected on 5GHz"
                                 " radio when the channel was already utilized with different percentage")
        report.build_objective()
        # test setup information
        report.set_table_title("Test Setup Information")
        report.build_table_title()
        report.test_setup_table(test_setup_data=test_setup_info, value="Device Under Test")
        self.table(report, "Min, Max, Avg Throughput", overall_tab,
              dis=f"The below table gives the information about Min, Max, and Avg throughput "
                  f"for the clients when channel utilized with {', '.join(util)}")
        self.table(report, "Pass/Fail Criteria", pasfail_tab, dis=f"This table briefs about Pass/Fail criteria  "
             f"for {', '.join(util)} channel utilization. If all the stations are able to run traffic and the overall throughput "
             f"should meet the given threshold then the test is considered to be PASS. The test fails if the overall throughput "
            f"is below the threshold value also if any one of the station is not able to run the layer-3 traffic.")
        if download:
            self.grph(report,
                 data_set=[[min(i) for i in bps_rx_a], [max(i) for i in bps_rx_a], [sum(i) / len(i) for i in bps_rx_a]],
                 dis=f"This graph represents the minimum, maximum and average throughput of "
                     f"stations when channel was utilized with {', '.join(util)} for download traffic",
                 xaxis_name="Utilizations", yaxis_name="Throughput (Mbps)",
                 xaxis_categories=util, label=["min", "max", 'avg'],multi_bar_width = 0.25,
                 graph_image_name="Download Throughput for all channel utilizations",step=1)
        if upload:
            self.grph(report,
                 data_set=[[min(i) for i in bps_rx_b], [max(i) for i in bps_rx_b], [sum(i) / len(i) for i in bps_rx_b]],
                 dis=f"This graph represents the minimum, maximum and average throughput of "
                     f"stations when channel was utilized with {', '.join(util)} for upload traffic",
                 xaxis_name="Utilizations", yaxis_name="Throughput (Mbps)",
                 xaxis_categories=util, label=["min", "max", 'avg'],multi_bar_width = 0.25,
                 graph_image_name="Upload Throughput for all channel utilization",step= 1)
        if len(sta_num) <= 40:
            step = 1
        elif 40 < len(sta_num) <= 80:
            step = 3
        elif 80 < len(sta_num) <= 100:
            step = 5
        else:
            step = 10
        for i in range(len(util)):
            if download:
                self.grph(report, data_set=[bps_rx_a[i]],
                     dis=f"The graph shows the individual throughput for all the connected stations on 5GHz radio "
                         f"when channel was utilized with {util[i]} in download traffic",
                     xaxis_name="Stations",yaxis_name="Throughput (Mbps)", xaxis_categories=range(1, len(sta_num) + 1,step),
                     label=[util[i]], graph_image_name=f"Individual download throughput - CH{util[i]}", xticks_font=7,step = step
                    ,multi_bar_width = 0)
            if upload:
                self.grph(report, data_set=[bps_rx_b[i]],
                     dis=f"The graph shows the individual throughput for all the connected stations on 5GHz radio "
                         f"when channel was utilized with {util[i]} in upload traffic",
                     xaxis_name="stations", yaxis_name="Throughput (Mbps)", xaxis_categories=range(1, len(sta_num) + 1,step),
                     label=[util[i]], graph_image_name=f"Individual upload throughput - CH{util[i]}", xticks_font=7,step = step
                    ,multi_bar_width = 0)
        # input setup information
        report.set_table_title("Input Setup Information")
        report.build_table_title()
        report.test_setup_table(test_setup_data=input_setup_info, value="Information")
        report.build_footer()
        html_file = report.write_html()
        logger.info("returned file {}".format(html_file))
        logger.info(html_file)
        report.write_pdf()
        colmn = ['Stations']#'No.of.times(download/upload']
        colmn.extend(range(1, len(self.bps_rx) + 1))
        data = list(self.bps_rx.values())
        data.insert(0, self.sta_list)
        csv = self.generates_csv(_columns= colmn, _rows= data,
                                 _filename='throughput_under_channel_load.csv')
        csv.generate_csv()
        report.csv_file_name = "throughput_under_channel_load.csv"
        report.move_csv_file()

    def monitor(self, duration_sec, monitor_interval, created_cx, col_names, iterations):
        try:
            duration_sec = Realm.parse_time(duration_sec).seconds
        except:
            if (duration_sec is None) or (duration_sec <= 1):
                raise ValueError("L3CXProfile::monitor wants duration_sec > 1 second")
            if (duration_sec <= monitor_interval):
                raise ValueError("L3CXProfile::monitor wants duration_sec > monitor_interval")
        if created_cx == None:
            raise ValueError("Monitor needs a list of Layer 3 connections")
        if (monitor_interval is None) or (monitor_interval < 1):
            raise ValueError("L3CXProfile::monitor wants monitor_interval >= 1 second")

        # monitor columns
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=duration_sec)
        # bps-rx-a (download) and bps-rx-b(upload) values are taken
        self.bps_rx_a, self.bps_rx_b, self.bps_rx, index = [], [], {}, -1
        bps_rx_a_avg,bps_rx_b_avg = [],[]
        [(self.bps_rx_a.append([]), self.bps_rx_b.append([])) for i in range(len(created_cx))]
        for test in range(1 + iterations):
            while datetime.datetime.now() < end_time:
                index += 1
                response = list(self.json_get('/cx/%s?fields=%s' % (','.join(created_cx),",".join(col_names))).values())[2:]
                self.bps_rx[index] = list(map(lambda i: [float(f"{x / (1000000):.2f}") for x in i.values()],response))
                time.sleep(monitor_interval)
        # bps_rx list is calculated
        print("rx rate values are with [bps-rx-a, bps-rx-b] :-\n", self.bps_rx,"\n\n")
        for index, key in enumerate(self.bps_rx):
            for i in range(len(self.bps_rx[key])):
                if self.cx_profile.side_b_min_bps != '0' and self.cx_profile.side_b_min_bps != 0:
                    self.bps_rx_a[i].append(self.bps_rx[key][i][0])
                if self.cx_profile.side_a_min_bps != '0' and self.cx_profile.side_a_min_bps != 0:
                    self.bps_rx_b[i].append(self.bps_rx[key][i][1])
        print(f"bps-rx-a values-: \n{self.bps_rx_a}\nbps-rx-b values-: \n{self.bps_rx_b}")
        if self.cx_profile.side_a_min_bps != '0' and self.cx_profile.side_a_min_bps != 0:
            bps_rx_b_avg = [float(f"{sum(i) / len(i): .2f}") for i in self.bps_rx_b]
        if self.cx_profile.side_b_min_bps != '0' and self.cx_profile.side_b_min_bps != 0:
            bps_rx_a_avg = [float(f"{sum(i) / len(i): .2f}") for i in self.bps_rx_a]
        return bps_rx_a_avg,bps_rx_b_avg

    def check_util(self,real_cli_obj = None, util_list = None, real_cli = None,
                   ssh_root = None, ssh_passwd = None,test_time = 0,up_down = [0],threshold=None,channnel=0):
        # check the utilization and run the traffic
        bps_rx_a,bps_rx_b,sta_create,count = [],[],1,0
        for util in util_list:  #  get throughput for every utilization values
            if count > 0:
                if len(up_down) > 0: # give data rate value and delete aggigned
                    self.cx_profile.side_a_min_bps, self.cx_profile.side_b_min_bps = int(float(up_down[0])),int(float( up_down[0]))
                    up_down.pop(0)
            count += 1
            stop_channel_load = 0
            util_flag = 1
            '''Loop until the expected channel utilization will get'''
            while util_flag:
                stop_channel_load += 1
                '''STOP the script if unable to set the utilization for 20 times'''
                if stop_channel_load >= 20:
                    print(f"Tried loading the channel with {util}% for {stop_channel_load} times...\n"
                          f"Unable to load the channel with {util}%\nScript exiting...")
                    exit(1)

                util_val = self.chn_util(ssh_root, ssh_passwd, channnel=channnel)  # find the channel utilization
                if (util - 3) <= util_val <= (util + 3):
                    util_flag = 0
                    if sta_create:
                        sta_create = 0
                        real_cli_obj.build()    # create specified no.of clients once
                    real_cli_obj.start(False, False)
                    time.sleep(20)
                    _bps_rx_a, _bps_rx_b = real_cli_obj.monitor(duration_sec=float(self.test_duration) * 60, monitor_interval=1,
                                 created_cx=real_cli_obj.cx_profile.created_cx.keys(),
                                 col_names=['bps rx a', 'bps rx b'], iterations=0)
                    #_bps_rx_a, _bps_rx_b = real_cli_obj.throughput(util,real_cli)
                    bps_rx_a.append(_bps_rx_a)
                    bps_rx_b.append(_bps_rx_b)
                    real_cli_obj.stop(trf=True,ad_dwn=False)
                else:
                    # channel utilization is less than the expected utilization value
                    if util_val < (util - 3):
                        logger.info("less than {}% util...".format(util))
                        if ((util ) - util_val) <= 4:
                            self.re_run_traff(100000, "add")
                        elif ((util ) - util_val) <= 8:
                            self.re_run_traff(300000, "add")
                        elif ((util ) - util_val) <= 12:
                            self.re_run_traff(500000, "add")
                        elif (util ) - util_val <= 16:
                            self.re_run_traff(1000000, "add")
                        elif (util ) - util_val > 16:
                            self.re_run_traff(1500000, "add")

                    # channel utilization is less than the expected utilization value
                    elif util_val > (util + 3):
                        logger.info("greater than {}% util...".format(util))
                        if (util_val - (util )) <= 4:
                            self.re_run_traff(100000, "sub")
                        elif (util_val - (util )) <= 8:
                            self.re_run_traff(300000, "sub")
                        elif (util_val - (util )) <= 12:
                            self.re_run_traff(500000, "sub")
                        elif util_val - (util ) <= 16:
                            self.re_run_traff(1000000, "sub")
                        elif util_val - (util ) > 16:
                            self.re_run_traff(1500000, "sub")

        print(f"bps_rx_a {bps_rx_a}\nbps_rx_b {bps_rx_b}")

        test_end = datetime.datetime.now().strftime("%b %d %H:%M:%S")
        logger.info("Test ended at %s", test_end)

        if len(threshold) < len(util_list):
            for i in range(len(util_list)):
                try:
                    tmp = threshold[i]
                except IndexError as e:
                    print(f"Threshold {threshold} and utilization {util_list}")
                    threshold.append(100 - int(util_list[i]))
        print(f"threshold {threshold} and utilization {util_list}")
        test_setup_info = {
            "AP Name": self.ap,
            "SSID": real_cli_obj.ssid,
            'No.of stations': len(real_cli),
            'Vap channel': channnel,
            'Utilization': ', '.join(map(str,util_list)),
            'Threshold': ', '.join(map(str,threshold)),
            "Total Test Duration": datetime.datetime.strptime(test_end, '%b %d %H:%M:%S') - datetime.datetime.strptime(test_time, '%b %d %H:%M:%S')
        }

        input_setup_info = {
            "Contact": "support@candelatech.com"
        }
        # send all the collected data to genarate report
        real_cli_obj.report(util = util_list, sta_num = real_cli,
                                    bps_rx_a = bps_rx_a, bps_rx_b= bps_rx_b,
                                    rep_title = "Throughput Under Channel Load",
                                    upload = int(real_cli_obj.cx_profile.side_a_min_bps)/1000000,
                                    download = int(real_cli_obj.cx_profile.side_b_min_bps)/1000000,
                                    test_setup_info = test_setup_info,input_setup_info = input_setup_info,threshold= threshold)


def main():
    try:
        optional,required = [],[]
        optional.append({'name': '--mode', 'help': 'Used to force mode of stations','default': 9})
        optional.append({'name': '--ap_name', 'help': 'AP name'})
        required.append({'name': '--ap_ip', 'help': 'IP of AP which was connected'})
        optional.append({'name': '--test_duration', 'help': 'Sets the duration of the test in minutes', 'default': 1})
        optional.append({'name':'--vap_channel', 'help':'To create VAP provide the AP channel', 'default': 36})
        required.append({'name':'--vap_radio', 'help':'VAP radio', 'default': "wiphy3"})
        optional.append({'name':'--util', 'help':'Channel utilization(provide whole number eg: 11,23,30,etc) with data_rate(bps) for that utilization',
                         'default': "20-3000000,40-6000000"})
        optional.append({'name':'--threshold', 'help':'Set the threshold for each utilization. '
                          'By default it will take 100-util_value (eg: 100-20=80) in case user not providing the Threshold'})
        required.append({'name':'--ap_password','help':'Password for AP'})
        optional.append({'name': '--upload', 'help': 'Upload bps rate minimum for side_a of netgear', 'default': 0})
        optional.append({'name': '--download', 'help': 'Download bps rate minimum for side_b of netgear', 'default': 0})
        parser = Realm.create_basic_argparse(
            prog='throughput.py',
            formatter_class=argparse.RawTextHelpFormatter,
            epilog='''\
                Measure the throughput for no.of clients when the channel was already utilized by specific load
                ''',
            description='''\
    throughput.py:
    --------------------
    Generic command layout:
    Note:- 
    **** In case user providing 'Fractional part' to the input values while running, the script will automatically truncate 
    the Fractional part except the test_duration.
    **** The script will automatically stop its execution when the channel is unable to load.
    python3 ./throughput.py
        --mode 1 {"auto"   : "0",
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
        --upstream_port eth1
        --vap_radio wiphy0
        --vap_channel 36
        --radio wiphy1
        --num_stations 40
        --security {open|wep|wpa|wpa2|wpa3}
        --ssid netgear
        --password admin123
        --test_duration 1 (default)
        --upload 3000000
        --download 3000000
        --util 20-2000000,40-000000
        --threshold 80,50
        --ap_ip 192.168.208.22
        --ap_name WAC505
        --ap_password Password@123xzsawq@!
        --debug
    ===============================================================================
        ''', more_optional=optional, more_required = required)

        args = parser.parse_args()

        # set up logger
        logger_config = lf_logger_config.lf_logger_config()
        if args.lf_logger_config_json:
            # logger_config.lf_logger_config_json = "lf_logger_config.json"
            logger_config.lf_logger_config_json = args.lf_logger_config_json
            logger_config.load_lf_logger_config()

        bridge_list = "br0"
        create_bridge = CreateBridge(_host=args.mgr,
                            _port=args.mgr_port,
                            _bridge_list=bridge_list,
                            _debug_on=args.debug,
                            target_device=args.target_device)

        util_rate = args.util.split(',')
        if args.threshold != None:
            threshold = [int(float(i)) for i in args.threshold.split(',')]
        else:
            threshold = []
        util_list, rate_list = [],[]
        for i in range(len(util_rate)):
            util_list.append(util_rate[i].split('-')[0])
            rate_list.append(util_rate[i].split('-')[1])
        util_list = [int(float(i)) for i in util_list]
        num_sta = lambda ars: ars if (ars != None and ars != 0) else 40    # if num station is None by deafault it create 2 stations

        # 4 stations created under VAP by default
        station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_= 3 , padding_number_=10000, radio=args.radio)
        # vap name
        vap_name = 'vap0000'
        print("List of stations under VAP--",station_list,'\nVAP name--',vap_name)
        # traffic data rate for stations under vap
        vap_sta_upload, vap_sta_download = int(float(rate_list[0])), int(float(rate_list[0]))
        rate_list.pop(0)

        # create stations and run traffic under VAP
        ip_var_test = IPV4VariableTime(host=args.mgr,           port=args.mgr_port,         number_template="0000",
                                       sta_list=station_list,   name_prefix="VT",           upstream=vap_name,
                                       ssid="vap_ssid",          password='[BLANK]',       radio=args.radio,
                                       security='open',         test_duration=args.test_duration,
                                       use_ht160=False,         side_a_min_rate= vap_sta_upload,
                                       side_b_min_rate=vap_sta_download,
                                       mode=args.mode,          ap=args.ap_name,                 _debug_on=args.debug,
                                       _vap_list = vap_name, _vap_radio = args.vap_radio, _dhcp = False)

        # ip_var_test.stop()
        # time.sleep(30)
        # test_time = datetime.datetime.now().strftime("%b %d %H:%M:%S")
        test_time = datetime.now().strftime("%b %d %H:%M:%S")
        logger.info("Test started at %s", test_time)

        ip_var_test.pre_cleanup() # clear existing clients
        ip_var_test.build_vaps(chn = int(float(args.vap_channel)))  # create VAPs
        # maybe create def for bridge creation?:
        # create_bridge.build_bridge()
        ip_var_test.build()     # create Stations and traffic

        if not ip_var_test.passes():
            logger.info(ip_var_test.get_fail_message())
            ip_var_test.exit_fail()

        try:
            layer3connections = ','.join([[*x.keys()][0] for x in ip_var_test.json_get('endp')['endpoint']])
        except:
            raise ValueError('Try setting the upstream port flag if your device does not have an eth1 port')

        ip_var_test.start(False, False)  # start the traffic and admin-up the sta

        station_list1 = LFUtils.portNameSeries(prefix_="Thsta", start_id_=0, end_id_=int(num_sta(args.num_stations))-1, padding_number_=10000,
                                               radio=args.radio)
        logger.info("Station list for netgear AP.....\n%s", station_list1)
        ip_var_test1 = IPV4VariableTime(host=args.mgr,          port=args.mgr_port,         number_template="0000",
                                        sta_list=station_list1, name_prefix="Thrp",         upstream=args.upstream_port,
                                        ssid= args.ssid,   password=args.passwd,       radio=args.radio,
                                        security=args.security,                    test_duration=args.test_duration,
                                        use_ht160=False,      side_a_min_rate=int(float(args.upload)),    side_b_min_rate=int(float(args.download)),
                                        mode=args.mode,       ap=args.ap_name,             _debug_on=args.debug,   _dhcp = True)

        # check the channel utilization
        ip_var_test.check_util(real_cli_obj = ip_var_test1, util_list = util_list,real_cli = station_list1, ssh_root = args.ap_ip,
           ssh_passwd = args.ap_password,test_time = test_time, up_down=rate_list,threshold = threshold,channnel = int(float(args.vap_channel)))

        if not ip_var_test.passes():
            logger.info(ip_var_test.get_fail_message())
            ip_var_test.exit_fail()

        ip_var_test.pre_cleanup() # clean the existing sta and traffics
        if ip_var_test.passes():
            ip_var_test.exit_success()

    except Exception as e:
        '''
        logger.info("### %s ###\nUnable to run the script...\nProvide the right values with the help of --help command\n"
                      "OR Re-run the script if the script stopped by some unexpected behavior..", e)
        '''
        logger.info("### %s ###", e)
        logger.info("Unable to run the script...")
        logger.info("Provide the right values with the help of --help command")
        logger.info("OR Re-run the script if the script stopped by some unexpected behavior..")
        logger.info(traceback.format_exc())


if __name__ == "__main__":
    main()
