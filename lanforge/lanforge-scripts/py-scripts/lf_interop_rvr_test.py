#!/usr/bin/env python3

"""
NAME: lf_interop_rvr_test.py

PURPOSE: lf_interop_rvr_test.py will measure the performance of stations over a certain distance of the DUT. Distance is emulated
        using programmable attenuators and throughput test is run at each distance/RSSI step.

python3 lf_interop_rvr_test.py --mgr 192.168.200.232 --mgr_port 8080 --upstream eth1 --security wpa2 --ssid NETGEAR63 --password Password@123 --atten_serno 3104 --atten_idx all --atten_val 0..5..5 --test_duration 1m --ap_model NETGEAR63 --traffic 10 --traffic_type lf_tcp --traffic_direction bidirectional

Use './lf_interop_rvr_test.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""

import sys
import os
import importlib
import logging
import time
import pandas as pd
import random

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
lf_report = importlib.import_module("py-scripts.lf_report")
lf_report = lf_report.lf_report
cv_test_manager = importlib.import_module("py-json.cv_test_manager")
cv_test = cv_test_manager.cv_test
cv_add_base_parser = cv_test_manager.cv_add_base_parser
cv_base_adjust_parser = cv_test_manager.cv_base_adjust_parser
lf_graph = importlib.import_module("py-scripts.lf_graph")
lf_bar_graph = lf_graph.lf_bar_graph
interop_modify = importlib.import_module("py-scripts.lf_interop_modify")

import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

import argparse

if 'py-json' not in sys.path:
    sys.path.append(os.path.join(os.path.abspath('..'), 'py-json'))


# from lf_graph import lf_bar_graph, lf_line_graph
# from datetime import datetime, timedelta


class RvR(Realm):
    def __init__(self, ssid=None, security=None, password="", create_sta=True, name_prefix=None, upstream=None,
                 host="localhost", port=8080,
                 mode=0, ap_model="", traffic_type="lf_tcp,lf_udp", traffic_direction="bidirectional",
                 side_a_min_rate=0, side_a_max_rate=0,
                 sta_names=None, side_b_min_rate=56, side_b_max_rate=0, number_template="00000", test_duration="2m",
                 sta_list=[1, 1],
                 serial_number='2222', indices="all", atten_val="0", traffic=500, radio_list=['wiphy0', 'wiphy3'],
                 _debug_on=False, _exit_on_error=False, _exit_on_fail=False):
        super().__init__(lfclient_host=host,
                         lfclient_port=port),
        self.upstream = upstream
        self.host = host
        self.port = port
        self.ssid = ssid
        self.security = security
        self.password = password
        self.radio = radio_list
        self.sta_list = sta_list
        self.num_stations = sum(self.sta_list)
        self.station_names = sta_names
        self.create_sta = create_sta
        self.mode = mode
        self.ap_model = ap_model
        self.traffic_type = traffic_type.split(",")
        self.traffic_direction = traffic_direction
        self.traffic = traffic
        self.number_template = number_template
        self.debug = _debug_on
        self.name_prefix = name_prefix
        self.test_duration = test_duration
        self.station_profile = self.new_station_profile()
        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.debug = self.debug
        self.station_profile.mode = mode
        self.cx_profile = self.new_l3_cx_profile()
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = side_a_min_rate // self.num_stations
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate // self.num_stations
        self.cx_profile.side_b_max_bps = side_b_max_rate
        self.attenuator_profile = self.new_attenuator_profile()
        self.serial_number = serial_number
        self.indices = indices.split(",")
        self.atten_values = atten_val
        self.list_of_data = None
        self.attenuator_db_signal = []
        self.throughput_phone = None

    def initialize_attenuator(self):
        self.attenuator_profile.atten_serno = self.serial_number
        self.attenuator_profile.atten_idx = "all"
        self.attenuator_profile.atten_val = '0'
        self.attenuator_profile.mode = None
        self.attenuator_profile.pulse_width_us5 = None
        self.attenuator_profile.pulse_interval_ms = None,
        self.attenuator_profile.pulse_count = None,
        self.attenuator_profile.pulse_time_ms = None
        self.attenuator_profile.create()
        # self.attenuator_profile.show()

    def set_attenuation(self, value):
        self.attenuator_profile.atten_serno = self.serial_number
        self.attenuator_profile.atten_idx = "all"
        self.attenuator_profile.atten_val = str(int(value) * 10)
        self.attenuator_profile.create()
        # self.attenuator_profile.show()

    def start_l3(self):
        if len(self.cx_profile.created_cx) > 0:
            self.json_post("/cli-json/clear_cx_counters", {"cx_name": 'all'})
            for cx in self.cx_profile.created_cx.keys():
                req_url = "cli-json/set_cx_report_timer"
                data = {
                    "test_mgr": "all",
                    "cx_name": cx,
                    "milliseconds": 1000
                }
                self.json_post(req_url, data)
        time.sleep(5)
        self.cx_profile.start_cx()
        logger.info("Monitoring CX's & Endpoints for %s seconds" % self.test_duration)

    def stop_l3(self):
        self.cx_profile.stop_cx()
        # self.station_profile.admin_down()

    def reset_l3(self):
        if len(self.cx_profile.created_cx) > 0:
            clear_endp = "cli-json/clear_endp_counters"
            data = {
                "endp_name": "all"
            }
            self.json_post(clear_endp, data)
            clear_cx = "cli-json/clear_cx_counters"
            data = {
                "cx_name": "all"
            }
            self.json_post(clear_cx, data)

    def cleanup(self):
        if len(self.cx_profile.created_cx) > 0:
            self.cx_profile.cleanup()

    def build(self):
        throughput_dbm = {}
        throughput_phone = {}
        phone_signal = {}
        if len(self.traffic_type) == 2:
            throughput_dbm = {f"{self.traffic_type[0]}": {}, f"{self.traffic_type[1]}": {}}
            throughput_phone = {f"{self.traffic_type[0]}": {}, f"{self.traffic_type[1]}": {}}
        elif len(self.traffic_type) == 1:
            throughput_dbm = {f"{self.traffic_type[0]}": {}}
            throughput_phone = {f"{self.traffic_type[0]}": {}}
        self.list_of_data = self.get_resource_data()
        self.station_profile.station_names = self.list_of_data[5]
        for traffic in self.traffic_type:
            self.cx_profile.create(endp_type=traffic, side_a=self.station_profile.station_names,
                                   side_b=self.upstream,
                                   sleep_time=0)
            self.initialize_attenuator()
            phone_list = self.list_of_data[1]
            for val in self.atten_values:
                self.attenuator_db_signal.append(f"{val} dB")
                throughput = {'upload': [], 'download': []}
                signal = []
                self.set_attenuation(value=val)
                self.start_l3()
                time.sleep(20)
                upload, download = self.monitor()
                # self.stop_l3()
                self.reset_l3()
                throughput['upload'] = upload
                throughput['download'] = download
                throughput['signal'] = signal
                eid_data = self.json_get("ports?fields=alias,signal")
                for alias in eid_data["interfaces"]:
                    for i in alias:
                        if int(i.split(".")[1]) > 1 and alias[i]["alias"] == 'wlan0':
                            # resource_hw_data = self.json_get("/resource/" + i.split(".")[0] + "/" + i.split(".")[1])
                            signal.append(int(alias[i]["signal"]))

                for i in range(len(phone_list)):
                    if throughput_phone[''.join(traffic)].get(phone_list[i]) is None:
                        throughput_phone[''.join(traffic)][phone_list[i]] = {"upload": [upload[i]],
                                                                             "download": [download[i]],
                                                                             "Signal Strength": [signal[i]]}
                    else:
                        throughput_phone[''.join(traffic)][phone_list[i]]["upload"].append(upload[i])
                        throughput_phone[''.join(traffic)][phone_list[i]]["download"].append(download[i])
                        throughput_phone[''.join(traffic)][phone_list[i]]["Signal Strength"].append(signal[i])
                throughput_dbm[''.join(traffic)][f"{val} dB"] = throughput
        self.throughput_phone = throughput_phone
        logger.info(throughput_dbm)
        return throughput_dbm

    def get_resource_data(self):
        resource_id_list = []
        phone_name_list = []
        mac_address = []
        user_name = []
        phone_radio = []
        rx_rate = []
        tx_rate = []
        station_name = []
        ssid = []
        eid_data = self.json_get("ports?fields=alias,mac,mode,Parent Dev,rx-rate,tx-rate,ssid,signal")
        for alias in eid_data["interfaces"]:
            for i in alias:
                if int(i.split(".")[1]) > 1 and alias[i]["alias"] == 'wlan0':
                    station_name.append(i)
                    resource_id_list.append(i.split(".")[1])
                    resource_hw_data = self.json_get("/resource/" + i.split(".")[0] + "/" + i.split(".")[1])
                    # Getting MAC address
                    mac = alias[i]["mac"]

                    rx = "Unknown" if alias[i]["rx-rate"] == 0 else alias[i]["rx-rate"]
                    tx = "Unknown" if alias[i]["tx-rate"] == 0 else alias[i]["tx-rate"]
                    ssid.append(alias[i]["ssid"])
                    rx_rate.append(rx)
                    tx_rate.append(tx)
                    # Getting username
                    user = resource_hw_data['resource']['user']
                    user_name.append(user)
                    # Getting user Hardware details/Name
                    hw_name = resource_hw_data['resource']['hw version'].split(" ")
                    name = " ".join(hw_name[0:2])
                    phone_name_list.append(name)
                    mac_address.append(mac)
                if int(i.split(".")[1]) > 1 and alias[i]["alias"] == 'wlan0' and alias[i]["parent dev"] == 'wiphy0':
                    # phone_radio.append(alias[i]['mode'])
                    # Mapping Radio Name in human readable format
                    if 'a' not in alias[i]['mode'] or "20" in alias[i]['mode']:
                        phone_radio.append('2G')
                    elif 'AUTO' in alias[i]['mode']:
                        phone_radio.append("AUTO")
                    else:
                        phone_radio.append('2G/5G')
        return [resource_id_list, phone_name_list, mac_address, user_name, phone_radio, station_name, rx_rate, tx_rate,
                ssid]

    def monitor(self):
        throughput, upload, download = {}, [], []
        if (self.test_duration is None) or (int(self.test_duration) <= 1):
            raise ValueError("Monitor test duration should be > 1 second")
        if self.cx_profile.created_cx is None:
            raise ValueError("Monitor needs a list of Layer 3 connections")
        # monitor columns
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=int(self.test_duration))
        index = -1
        connections = dict.fromkeys(list(self.cx_profile.created_cx.keys()), float(0))
        [(upload.append([]), download.append([])) for i in range(len(self.cx_profile.created_cx))]
        while datetime.now() < end_time:
            index += 1
            response = list(
                self.json_get('/cx/%s?fields=%s' % (
                    ','.join(self.cx_profile.created_cx.keys()), ",".join(['bps rx a', 'bps rx b']))).values())[2:]
            throughput[index] = list(
                map(lambda i: [x for x in i.values()], response))
            time.sleep(1)
        # # rx_rate list is calculated
        for index, key in enumerate(throughput):
            for i in range(len(throughput[key])):
                upload[i].append(throughput[key][i][0])
                download[i].append(throughput[key][i][1])
        logger.info("Upload values", upload)
        logger.info("Download Values", download)
        upload_throughput = [float(f"{(sum(i) / 1000000) / len(i): .2f}") for i in upload]
        download_throughput = [float(f"{(sum(i) / 1000000) / len(i): .2f}") for i in download]
        logger.info("upload: ", upload_throughput)
        logger.info("download: ", download_throughput)
        return upload_throughput, download_throughput

    def set_report_data(self, data):
        res = {}
        if data is not None:
            res = data
        else:
            logger.error("No Data found to generate report!")
            exit(1)
        if self.traffic_type is not None:
            if self.traffic_direction == 'upload':
                for traffic in self.traffic_type:
                    for key in res[traffic]:
                        if 'download' in res[traffic][key]:
                            res[traffic][key].pop('download')
            elif self.traffic_direction == 'download':
                for traffic in self.traffic_type:
                    for key in res[traffic]:
                        if 'download' in res[traffic][key]:
                            res[traffic][key].pop('upload')
            table_df = {}
            num_stations = []
            mode = []
            graph_df = {}
            if len(self.traffic_type) == 2:
                graph_df = {f"{self.traffic_type[0]}": {}, f"{self.traffic_type[1]}": {}}
            elif len(self.traffic_type) == 1:
                graph_df = {f"{self.traffic_type[0]}": {}}
            for traffic in self.traffic_type:
                dataset, label, color = [], [], []
                direction = ""
                if self.traffic_direction == 'upload':
                    dataset.append([float(f"{sum(res[traffic][i]['upload']):.2f}") for i in res[traffic]])
                    label = ['upload']
                    color = ['olivedrab']
                    direction = "upload"
                elif self.traffic_direction == 'download':
                    dataset.append([float(f"{sum(res[traffic][i]['download']):.2f}") for i in res[traffic]])
                    label = ['download']
                    color = ['orangered']
                    direction = "download"
                elif self.traffic_direction == 'bidirectional':
                    dataset.append([float(f"{sum(res[traffic][i]['upload']):.2f}") for i in res[traffic]])
                    dataset.append([float(f"{sum(res[traffic][i]['download']):.2f}") for i in res[traffic]])
                    label = ['upload', 'download']
                    color = ['olivedrab', 'orangered']
                    direction = "upload and download"
                graph_df[traffic].update({"dataset": dataset})
                graph_df[traffic].update({"label": label})
                graph_df[traffic].update({"color": color})
                graph_df[traffic].update({"direction": direction})
            # res.update({"throughput_table_df": table_df})
            res.update({"graph_df": graph_df})
        return res

    def generate_report(self, data, test_setup_info, input_setup_info):
        each_phone_data = self.set_report_data(self.throughput_phone)
        res = self.set_report_data(data)
        report = lf_report(_output_pdf="lf_interop_rvr_test.pdf",
                           _output_html="lf_interop_rvr_test.html",
                           _results_dir_name="Interop_RvR_Test")
        report_path = report.get_path()
        report_path_date_time = report.get_path_date_time()
        logger.info("path: {}".format(report_path))
        logger.info("path_date_time: {}".format(report_path_date_time))
        report.set_title("LANforge InterOp Rate vs Range")
        report.build_banner()
        # objective title and description
        report.set_obj_html(_obj_title="Objective", _obj="LANforge InterOp measures the performances of each real "
                                                         "client over a certain distance of the DUT. Distance is emulated using programmable attenuators and "
                                                         "throughput test is run at each attenuation/RSSI step. This test measures the performance over distance"
                                                         " of the Device Under Test. The test allows the user to plot RSSI curves both upstream and downstream"
                                                         " for different types of traffic and different station types.")
        report.build_objective()
        report.test_setup_table(test_setup_data=test_setup_info, value="Device Under Test")
        report.end_content_div()
        phone_info = {
            # "Resource ID": self.list_of_data[0],
            "Phone Name": self.list_of_data[1],
            "MAC Address": self.list_of_data[2],
            "User Name": self.list_of_data[3],
            "Phone Radio": self.list_of_data[4],
            "Rx Rate (Mbps) ": self.list_of_data[6],
            "Tx Rate (Mbps)": self.list_of_data[7],
            "SSID": self.list_of_data[8],
        }
        phone_details = pd.DataFrame(phone_info)

        report.build_text()
        report.end_content_div()
        for traffic_type in res["graph_df"]:
            report.set_obj_html(
                _obj_title="Overall {} throughput for {} real clients using {} traffic."
                .format(res["graph_df"][traffic_type]["direction"], len(self.list_of_data[0]), "TCP" if traffic_type ==
                                                                                                        "lf_tcp" else "UDP" if traffic_type == "lf_udp" else "TCP and UDP"),
                _obj="The below graph represents overall {} throughput for different attenuation levels ".format(
                    res["graph_df"][traffic_type]["direction"]))
            report.build_objective()
            graph = lf_graph.lf_line_graph(_data_set=res["graph_df"][traffic_type]["dataset"],
                                           _xaxis_name="Attenuation",
                                           _yaxis_name="Throughput(in Mbps)",
                                           _xaxis_categories=[str(traffic_type) for traffic_type in
                                                              res[traffic_type].keys()],
                                           _graph_image_name=f"rvr_{traffic_type}_{self.traffic_direction}",
                                           _label=res["graph_df"][traffic_type]["label"],
                                           _color=res["graph_df"][traffic_type]["color"],
                                           _xaxis_step=1,
                                           _graph_title="Overall Throughput vs Attenuation",
                                           _title_size=16,
                                           _figsize=(18, 6),
                                           _marker=['o', '+', '*', '.', 'x', '|', 's', 'd', '^', 'v', '>',
                                                    '<', 'p', 'h'][random.randrange(0, 13)],
                                           _legend_loc="best",
                                           _legend_box=None,
                                           _dpi=200,
                                           _enable_csv=True)
            graph_png = graph.build_line_graph()

            logger.info("graph name {}".format(graph_png))

            report.set_graph_image(graph_png)
            # need to move the graph image to the results directory
            report.move_graph_image()
            report.set_csv_filename(graph_png)
            report.move_csv_file()
            report.build_graph()

            len_data = len(res["graph_df"][traffic_type]["dataset"][0])
            # print("Upload: ", [res["graph_df"][traffic_type]["dataset"][0][i] for i in range(len_data)])
            # print("Download: ", [res["graph_df"][traffic_type]["dataset"][1][i] for i in range(len_data)])
            report.start_content_div()
            report.set_table_title("<h3>Table for Graph")
            report.build_table_title()
            if self.traffic_direction == "bidirectional":
                data = pd.DataFrame({
                    "Attenuation Step(dB)": self.attenuator_db_signal,
                    "Upload Throughput(mbps)": [res["graph_df"][traffic_type]["dataset"][0][i] for i in
                                                range(len_data)],
                    "Download Throughput(mbps)": [res["graph_df"][traffic_type]["dataset"][1][i] for i in
                                                  range(len_data)],
                })
            elif self.traffic_direction == "upload":
                data = pd.DataFrame({
                    "Attenuation Step(dB)": self.attenuator_db_signal,
                    "Upload Throughput(mbps)": [res["graph_df"][traffic_type]["dataset"][0][i] for i in
                                                range(len_data)],
                    # "Download Throughput(mbps)": [res["graph_df"][traffic_type]["dataset"][1][i] for i in
                    #                               range(len_data)],
                })
            elif self.traffic_direction == "download":
                data = pd.DataFrame({
                    "Attenuation Step(dB)": self.attenuator_db_signal,
                    # "Upload Throughput(mbps)": [res["graph_df"][traffic_type]["dataset"][0][i] for i in
                    #                             range(len_data)],
                    "Download Throughput(mbps)": [res["graph_df"][traffic_type]["dataset"][1][i] for i in
                                                  range(len_data)],
                })
            report.set_table_dataframe(data)
            report.build_table()
            report.end_content_div()

        self.generate_individual_graphs(report, res, each_phone_data)
        report.set_table_title("<h3>Supported Device information:")
        report.build_table_title()
        report.set_text("<h5> The below table shows a list of all the Real clients which are connected to LANForge "
                        "server in the tabular format which also show the various details of the real-clients (phones) "
                        "such as phone name, MAC address, Username, Phone Radio, Rx link rate, Tx link rate and "
                        "Resource id.")
        report.build_text()
        report.set_table_dataframe(phone_details)
        report.build_table()
        report.test_setup_table(test_setup_data=input_setup_info, value="Information")
        report.build_custom()
        report.build_footer()
        report.write_html()
        report.write_pdf()

    def generate_individual_graphs(self, report, res, phone_x):
        if len(res.keys()) > 0:
            if "graph_df" in res:
                res.pop("graph_df")
        if len(res.keys()) > 0:
            if "graph_df" in phone_x:
                phone_x.pop("graph_df")
        RSSISignal = {}
        Throughput = {}
        for traffic_type in phone_x:
            for phone in phone_x[traffic_type]:
                for direction in phone_x[traffic_type][phone]:
                    if "RSSI Strength(in dBm)" == 'Throughput(in Mbps)' if (
                            direction == 'upload' or direction == 'download') else 'RSSI Strength(in dBm)':
                        RSSISignal[phone] = phone_x[traffic_type][phone][direction]
                    else:
                        Throughput[phone] = phone_x[traffic_type][phone][direction]

        # for traffic_type in phone_x:
        #     for phone in phone_x[traffic_type]:
        #         for direction in phone_x[traffic_type][phone]:
        #             if 'RSSI Strength(in dBm)' is not 'Throughput(in Mbps)' if (direction == 'upload' or direction == 'download') else 'RSSI Strength(in dBm)':
        #                 Throughput[phone] = phone_x[traffic_type][phone][direction]

        for traffic_type in phone_x:
            for phone in phone_x[traffic_type]:
                for direction in phone_x[traffic_type][phone]:
                    traffic_name = "TCP" if (traffic_type == "lf_tcp") else "UDP" if (
                            traffic_type == "lf_udp") else "TCP and UDP"
                    report.set_obj_html(_obj_title=f"{phone} : {traffic_name} {direction}", _obj="")
                    report.build_objective()
                    line_graph = lf_graph.lf_line_graph(_data_set=[phone_x[traffic_type][phone][direction]],
                                                        _xaxis_name="Attenuation",
                                                        _yaxis_name='Throughput(in Mbps)' if (
                                                                direction == 'upload' or direction == 'download') else 'RSSI Strength(in dBm)',
                                                        _xaxis_categories=self.attenuator_db_signal,
                                                        _graph_image_name=f"rvr_{traffic_type}_{phone}_{direction}",
                                                        _label=[
                                                            'upload' if direction == 'upload' else 'download' if direction == "download" else 'RSSI Strength'],
                                                        _color=[
                                                            'olivedrab' if direction == 'upload' else 'orangered' if direction == 'download' else 'mediumblue'],
                                                        _xaxis_step=1,
                                                        _graph_title="Throughput vs Attenuation" if (
                                                                direction == 'upload' or direction == 'download') else "RSSI Signal Strength(in dBm)",
                                                        _title_size=16,
                                                        _figsize=(18, 6),
                                                        _legend_loc="best",
                                                        _marker=['o', '+', '*', '.', 'x', '|', 's', 'd', '^', 'v', '>',
                                                                 '<', 'p', 'h'][random.randrange(0, 13)],
                                                        _legend_box=None,
                                                        _dpi=200,
                                                        _enable_csv=True)
                    line_graph_png = line_graph.build_line_graph()

                    logger.info("graph name {}".format(line_graph_png))

                    report.set_graph_image(line_graph_png)
                    # need to move the graph image to the results directory
                    report.move_graph_image()
                    report.set_csv_filename(line_graph_png)
                    report.move_csv_file()
                    report.build_graph()

                    print("Attenuator ", self.attenuator_db_signal)
                    print("Data ", phone_x[traffic_type][phone][direction])
                    print("Signal ", self.list_of_data[1])
                    report.start_content_div()
                    report.set_table_title("<h3>Table for Graph")
                    report.build_table_title()
                    data = pd.DataFrame({
                        "Attenuation Step(dB)": self.attenuator_db_signal,
                        "RSSI Strength (in dBm)": RSSISignal[phone],
                        "Throughput(in Mbps)": Throughput[phone],
                    })
                    report.set_table_dataframe(data)
                    report.build_table()
                    report.end_content_div()

        for traffic_type in res:
            for attenuation in res[traffic_type]:
                for direction in res[traffic_type][attenuation]:
                    if direction == "upload" or direction == "download":
                        report.set_obj_html(
                            _obj_title=f"Individual {direction} Throughput for {len(self.list_of_data[0])} clients using {'TCP' if traffic_type == 'lf_tcp' else 'UDP' if traffic_type == 'lf_udp' else 'TCP and UDP'} traffic over {attenuation} attenuation",
                            _obj=f"The below graph represents Individual {direction} throughput of all stations when attenuation set to {attenuation}")
                        report.build_objective()
                        graph = lf_bar_graph(_data_set=[res[traffic_type][attenuation][direction]],
                                             _xaxis_name="No.of Stations",
                                             _yaxis_name="Throughput(in Mbps)",
                                             _xaxis_categories=self.list_of_data[1],
                                             _graph_image_name=f"rvr_{traffic_type}_{attenuation}_{direction}",
                                             _label=['upload' if direction == 'upload' else
                                                     'download'],
                                             _color=['olivedrab' if direction == 'upload' else 'orangered'],
                                             _color_edge='grey',
                                             _xaxis_step=1,
                                             _graph_title=f"Individual throughput with {attenuation} attenuation",
                                             _title_size=16,
                                             _bar_width=0.15,
                                             _figsize=(18, 6),
                                             _legend_loc="best",
                                             _legend_box=None,
                                             _dpi=96,
                                             _show_bar_value=True,
                                             _enable_csv=True)
                        graph_png = graph.build_bar_graph()

                        logger.info("graph name {}".format(graph_png))

                        report.set_graph_image(graph_png)
                        # need to move the graph image to the results directory
                        report.move_graph_image()
                        report.set_csv_filename(graph_png)
                        report.move_csv_file()
                        report.build_graph()

                        print("Attenuation Step(dB) ", self.attenuator_db_signal, "\nThroughput(mbps) ",
                              res[traffic_type][attenuation][direction], )
                        report.start_content_div()
                        report.set_table_title("<h3>Table for Graph")
                        report.build_table_title()
                        data = pd.DataFrame({
                            "Attenuation Step(dB)": [attenuation] * len(res[traffic_type][attenuation][direction]),
                            "Phone": self.list_of_data[1],
                            "Throughput(mbps)": res[traffic_type][attenuation][direction],
                            "Traffic Direction": ['upload' if direction == 'upload' else 'download'] * len(
                                res[traffic_type][attenuation][direction]),
                            "Traffic type": [
                                                'TCP' if traffic_type == 'lf_tcp' else 'UDP' if traffic_type == 'lf_udp' else 'TCP and UDP'] * len(
                                res[traffic_type][attenuation][direction]),
                        })
                        report.set_table_dataframe(data)
                        report.build_table()
                        report.end_content_div()


def main():
    parser = argparse.ArgumentParser(description='''\
    rvr_test.py:
    --------------------
    Generic command layout:
    =====================================================================
    sudo python3 rvr_test.py --mgr localhost --mgr_port 8080 --upstream eth1 --num_stations 40 
    --security wpa2 --ssid NETGEAR73-5G --password fancylotus986 --radio wiphy3 --atten_serno 2222 --atten_idx all
    --atten_val 10 --test_duration 1m --ap_model WAX610 --traffic 100''', allow_abbrev=False)
    optional = parser.add_argument_group('optional arguments')
    required = parser.add_argument_group('required arguments')
    optional.add_argument('--mgr', help='hostname for where LANforge GUI is running', default='localhost')
    optional.add_argument('--mgr_port', help='port LANforge GUI HTTP service is running on', default=8080)
    optional.add_argument('--upstream', help='non-station port that generates traffic: <resource>.<port>, '
                                             'e.g: 1.eth1', default='eth1')
    optional.add_argument('--mode', help='used to force mode of stations', default="0")
    required.add_argument('--ssid', help="ssid for client association with Access Point", required=True)
    required.add_argument('--security', help="security type of ssid, ex: wpa || wpa2 || wpa3 || open", required=True)
    required.add_argument('--password', help="password of ssid", required=True)
    required.add_argument('--traffic_type', help='provide the traffic Type lf_udp, lf_tcp', default='lf_tcp')
    optional.add_argument('--traffic_direction', help='Traffic direction i.e upload or download or bidirectional',
                          default="bidirectional")
    required.add_argument('--traffic', help='traffic to be created for the given number of clients (in Mbps)',
                          required=True)
    required.add_argument('--test_duration', help='sets the duration of the test ex: 2s --> two seconds || 2m '
                                                  '--> two minutes || 2h --> two hours', required=True)
    optional.add_argument('--create_sta', help="used to create stations if you do not prefer existing stations",
                          default=True)
    optional.add_argument('--sta_names',
                          help='used to provide existing station names from the port manager, prefer only if '
                               'create_sta is False',
                          default="sta0000")
    optional.add_argument('--ap_model', help="AP Model Name", default="Test-AP")
    # required.add_argument('--num_stations', help='number of stations to create, works only if create_sta is True',
    #                       required=True)
    optional.add_argument('-as', '--atten_serno', help='Serial number for requested Attenuator', default='2222')
    optional.add_argument('-ai', '--atten_idx',
                          help='Attenuator index eg. For module 1 = 0,module 2 = 1 --> --atten_idx 0,1',
                          default='all')
    optional.add_argument('-av', '--atten_val',
                          help='Requested attenuation in dB ex:--> --atten_val 0..10..40 (here attenuation start '
                               'from 0 and end with 50 with increment value of 10 each time)', default='0')
    optional.add_argument('--debug', help="to enable debug", default=False)
    # logging configuration:
    parser.add_argument('--log_level', default=None,
                        help='Set logging level: debug | info | warning | error | critical')

    parser.add_argument("--lf_logger_config_json",
                        help="--lf_logger_config_json <json file> , json configuration of logger")
    args = parser.parse_args()
    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    # set the logger level to debug
    if args.log_level:
        logger_config.set_level(level=args.log_level)

    # lf_logger_config_json will take presidence to changing debug levels
    if args.lf_logger_config_json:
        # logger_config.lf_logger_config_json = "lf_logger_config.json"
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()

    test_start_time = datetime.now().strftime("%b %d %H:%M:%S")
    logger.info("Test started at ", test_start_time)
    print(parser.parse_args())
    if args.test_duration.endswith('s') or args.test_duration.endswith('S'):
        args.test_duration = abs(int(float(args.test_duration[0:-1])))
    elif args.test_duration.endswith('m') or args.test_duration.endswith('M'):
        args.test_duration = abs(int(float(args.test_duration[0:-1]) * 60))
    elif args.test_duration.endswith('h') or args.test_duration.endswith('H'):
        args.test_duration = abs(int(float(args.test_duration[0:-1]) * 60 * 60))
    elif args.test_duration.endswith(''):
        args.test_duration = abs(int(float(args.test_duration)))

    start = int(args.atten_val.split('..')[0])
    interval = int(args.atten_val.split('..')[1])
    end = int(args.atten_val.split('..')[2])
    temp = ['0']
    for i in range(start, end + 1, interval):
        if str(i) not in temp:
            temp.append(str(i))
    args.atten_val = temp

    if args.traffic is not None and int(args.traffic) < 0:
        raise ValueError("Traffic should be greater than 0 Mbps")

    side_a, side_b = 25, 25
    if args.traffic_direction == "upload":
        side_a = 0
        side_b = abs(int(float(args.traffic) * 1000000))
    elif args.traffic_direction == "download":
        side_a = abs(int(float(args.traffic) * 1000000))
        side_b = 0
    elif args.traffic_direction == "bidirectional":
        side_a = abs(int(float(args.traffic) * 1000000))
        side_b = abs(int(float(args.traffic) * 1000000))

    rvr_obj = RvR(host=args.mgr,
                  port=args.mgr_port,
                  number_template="0000",
                  create_sta=args.create_sta,
                  name_prefix="RvR-",
                  upstream=args.upstream,
                  ssid=args.ssid,
                  password=args.password,
                  security=args.security,
                  test_duration=args.test_duration,
                  traffic=abs(int(args.traffic)),
                  side_a_min_rate=side_a,
                  side_b_min_rate=side_b,
                  mode=args.mode,
                  ap_model=args.ap_model,
                  serial_number=args.atten_serno,
                  indices=args.atten_idx,
                  atten_val=args.atten_val,
                  traffic_type=args.traffic_type,
                  traffic_direction=args.traffic_direction,
                  _debug_on=args.debug)

    data = rvr_obj.build()
    rvr_obj.stop_l3()

    test_end_time = datetime.now().strftime("%b %d %H:%M:%S")
    logger.info("Test ended at: ", test_end_time)

    test_setup_info = {
        "AP Model": rvr_obj.ap_model,
        "Number of Real Stations": len(rvr_obj.list_of_data[0]),
        "SSID": rvr_obj.ssid,
        "Password": rvr_obj.password,
        "Traffic Pumped for each Station": f"{rvr_obj.traffic} Mbps",
        "Test Duration": datetime.strptime(test_end_time, "%b %d %H:%M:%S") - datetime.strptime(
            test_start_time, "%b %d %H:%M:%S")
    }

    input_setup_info = {
        "contact": "support@candelatech.com"
    }
    rvr_obj.generate_report(data=data, test_setup_info=test_setup_info, input_setup_info=input_setup_info, )
    rvr_obj.cleanup()


if __name__ == "__main__":
    main()
