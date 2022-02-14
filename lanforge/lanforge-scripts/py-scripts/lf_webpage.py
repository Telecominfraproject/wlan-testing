#!/usr/bin/env python3
"""
This script will create 40 clients on 5Ghz , 2.4Ghz and Both and generate layer4 traffic on LANforge ,The Webpage
 Download Test is designed to test the performance of the  Access Point.The goal is to  check whether the webpage
 loading time meets the expectation when clients connected on single radio as well as dual radio.

how to run -
./lf_webpage.py --mgr <ip_address> --fiveg_ssid <5G_ssid> --fiveg_security wpa2 --fiveg_passwd <passwd>
--twog_ssid <2G_ssid> --twog_security wpa2 --twog_passwd <passwd> --fiveg_radio wiphy0 --twog_radio wiphy1
--num_stations 5 --upstream_port eth1 --duration 1

Copyright 2021 Candela Technologies Inc 04 - April - 2021
"""

import sys
import os
import importlib
import time
import argparse
import paramiko
from datetime import datetime
import pandas as pd
import logging


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
PortUtils = realm.PortUtils
lf_report = importlib.import_module("py-scripts.lf_report")
lf_graph = importlib.import_module("py-scripts.lf_graph")
lf_kpi_csv = importlib.import_module("py-scripts.lf_kpi_csv")
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")


class HttpDownload(Realm):
    def __init__(self, lfclient_host, lfclient_port, upstream, num_sta, security, ssid, password,
                 target_per_ten, file_size, bands, start_id=0, twog_radio=None, fiveg_radio=None, _debug_on=False, _exit_on_error=False,
                 _exit_on_fail=False):
        self.host = lfclient_host
        self.port = lfclient_port
        self.upstream = upstream
        self.num_sta = num_sta
        self.security = security
        self.ssid = ssid
        self.sta_start_id = start_id
        self.password = password
        self.twog_radio = twog_radio
        self.fiveg_radio = fiveg_radio
        self.target_per_ten = target_per_ten
        self.file_size = file_size
        self.bands = bands
        self.debug = _debug_on
        print(bands)

        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.http_profile = self.local_realm.new_http_profile()
        self.http_profile.requests_per_ten = self.target_per_ten
        # self.http_profile.url = self.url
        self.port_util = PortUtils(self.local_realm)
        self.http_profile.debug = _debug_on
        self.created_cx = {}
        self.station_list = []
        self.radio = []

    def set_values(self):
        # This method will set values according user input
        if self.bands == "5G":
            self.radio = [self.fiveg_radio]
            self.station_list = [LFUtils.portNameSeries(prefix_="fiveg_sta", start_id_=self.sta_start_id,
                                                            end_id_=self.num_sta - 1, padding_number_=10000,
                                                            radio=self.fiveg_radio)]
        elif self.bands == "2.4G":
            self.radio = [self.twog_radio]
            self.station_list = [LFUtils.portNameSeries(prefix_="twog_sta", start_id_=self.sta_start_id,
                                                       end_id_=self.num_sta - 1, padding_number_=10000,
                                                       radio=self.twog_radio)]
        elif self.bands == "Both":
            self.radio = [self.twog_radio, self.fiveg_radio]
            print(self.radio)
            # self.num_sta = self.num_sta // 2
            self.station_list = [
                                 LFUtils.portNameSeries(prefix_="twog_sta", start_id_=self.sta_start_id,
                                                        end_id_=self.num_sta - 1, padding_number_=10000,
                                                        radio=self.twog_radio),
                                 LFUtils.portNameSeries(prefix_="fiveg_sta", start_id_=self.sta_start_id,
                                                        end_id_=self.num_sta - 1, padding_number_=10000,
                                                        radio=self.fiveg_radio)
                                 ]

    def precleanup(self):
        self.count = 0
        for rad in range(len(self.radio)):
            print("radio", self.radio[rad])
            if self.radio[rad] == self.fiveg_radio:
                # select an mode
                self.station_profile.mode = 10
                self.count = self.count + 1
            elif self.radio[rad] == self.twog_radio:
                # select an mode
                self.station_profile.mode = 6
                self.count = self.count + 1

            if self.count == 2:
                self.sta_start_id = self.num_sta
                self.num_sta = 2 * (self.num_sta)
                self.station_profile.mode = 10
                self.http_profile.cleanup()
                # cleanup station list which started sta_id 20
                self.station_profile.cleanup(self.station_list[rad], debug_=self.local_realm.debug)
                LFUtils.wait_until_ports_disappear(base_url=self.local_realm.lfclient_url,
                                                   port_list=self.station_list[rad],
                                                   debug=self.local_realm.debug)
                return
            # clean dlayer4 ftp traffic
            self.http_profile.cleanup()

            # cleans stations
            self.station_profile.cleanup(self.station_list[rad], delay=1, debug_=self.local_realm.debug)
            LFUtils.wait_until_ports_disappear(base_url=self.local_realm.lfclient_url,
                                               port_list=self.station_list[rad],
                                               debug=self.local_realm.debug)
            time.sleep(1)
        print("precleanup done")

    def build(self):
        # enable http on ethernet
        self.port_util.set_http(port_name=self.local_realm.name_to_eid(self.upstream)[2],
                                resource=self.local_realm.name_to_eid(self.upstream)[1], on=True)
        for rad in range(len(self.radio)):
            print(self.station_list[rad])
            self.station_profile.use_security(self.security[rad], self.ssid[rad], self.password[rad])
            self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
            self.station_profile.set_command_param("set_port", "report_timer", 1500)
            self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
            self.station_profile.create(radio=self.radio[rad], sta_names_=self.station_list[rad], debug=self.local_realm.debug)
            self.local_realm.wait_until_ports_appear(sta_list=self.station_list[rad])
            self.station_profile.admin_up()
            if self.local_realm.wait_for_ip(self.station_list[rad], timeout_sec=60):
                self.local_realm._pass("All stations got IPs")
            else:
                self.local_realm._fail("Stations failed to get IPs")
            # building layer4
            self.http_profile.direction = 'dl'
            self.http_profile.dest = '/dev/null'
            data = self.local_realm.json_get("ports/list?fields=IP")

            # getting eth ip
            eid = self.local_realm.name_to_eid(self.upstream)
            for i in data["interfaces"]:
                for j in i:
                    if "{shelf}.{resource}.{port}".format(shelf=eid[0], resource=eid[1], port=eid[2]) == j:
                        ip_upstream = i["{shelf}.{resource}.{port}".format(
                            shelf=eid[0], resource=eid[1], port=eid[2])]['ip']

            # create http profile
            self.http_profile.create(ports=self.station_profile.station_names, sleep_time=.5,
                                     suppress_related_commands_=None, http=True,
                                     http_ip=ip_upstream + "/webpage.html")
            if self.count == 2:
                self.station_profile.mode = 6
        print("Test Build done")

    def start(self):
        print("Test Started")
        self.http_profile.start_cx()
        try:
            for i in self.http_profile.created_cx.keys():
                while self.local_realm.json_get("/cx/" + i).get(i).get('state') != 'Run':
                    continue
        except Exception as e:
            pass

    def stop(self):
        self.http_profile.stop_cx()

    def my_monitor(self, data_mon):
        # data in json format
        data = self.local_realm.json_get("layer4/%s/list?fields=%s" %
                                         (','.join(self.http_profile.created_cx.keys()), data_mon.replace(' ', '+')))
        # print(data)
        data1 = []
        data = data['endpoint']
        if self.num_sta == 1:
            data1.append(data[data_mon])
        else:
            for cx in self.http_profile.created_cx.keys():
                for info in data:
                    if cx in info:
                        data1.append(info[cx][data_mon])
        # print(data_mon, data1)
        return data1

    def postcleanup(self):
        self.http_profile.cleanup()
        self.station_profile.cleanup()
        LFUtils.wait_until_ports_disappear(base_url=self.local_realm.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)

    def file_create(self, ssh_port):
        ip = self.host
        user = "root"
        pswd = "lanforge"
        port = ssh_port
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=port, username=user, password=pswd, banner_timeout=600)
        cmd = '[ -f /usr/local/lanforge/nginx/html/webpage.html ] && echo "True" || echo "False"'
        stdin, stdout, stderr = ssh.exec_command(str(cmd))
        output = stdout.readlines()
        print(output)
        if output == ["True\n"]:
            cmd1 = "rm /usr/local/lanforge/nginx/html/webpage.html"
            stdin, stdout, stderr = ssh.exec_command(str(cmd1))
            output = stdout.readlines()
            time.sleep(10)
            cmd2 = "sudo fallocate -l " + self.file_size + " /usr/local/lanforge/nginx/html/webpage.html"
            stdin, stdout, stderr = ssh.exec_command(str(cmd2))
            print("File creation done", self.file_size)
            output = stdout.readlines()
        else:
            cmd2 = "sudo fallocate -l " + self.file_size + " /usr/local/lanforge/nginx/html/webpage.html"
            stdin, stdout, stderr = ssh.exec_command(str(cmd2))
            print("File creation done", self.file_size)
            output = stdout.readlines()
        ssh.close()
        time.sleep(1)
        return output

    def download_time_in_sec(self, result_data):
        self.result_data = result_data
        download_time = dict.fromkeys(result_data.keys())
        for i in download_time:
            try:
                download_time[i] = result_data[i]['dl_time']
            except BaseException:
                download_time[i] = []
        print("dl_times: ", download_time)
        lst = []
        lst1 = []
        lst2 = []
        dwnld_time = dict.fromkeys(result_data.keys())
        dataset = []
        for i in download_time:
            if i == "5G":
                for j in download_time[i]:
                    x = (j / 1000)
                    y = round(x, 1)
                    lst.append(y)
                print(lst)
                dwnld_time["5G"] = lst
                dataset.append(dwnld_time["5G"])
            if i == "2.4G":
                for j in download_time[i]:
                    x = (j / 1000)
                    y = round(x, 1)
                    lst1.append(y)
                print(lst)
                dwnld_time["2.4G"] = lst1
                dataset.append(dwnld_time["2.4G"])
            if i == "Both":
                # print("yes", download_time[i])
                for j in download_time[i]:
                    x = (j / 1000)
                    y = round(x, 1)
                    lst2.append(y)
                # print(lst2)
                dwnld_time["Both"] = lst2
                dataset.append(dwnld_time["Both"])
        return dataset

    def speed_in_Mbps(self, result_data):
        self.result_data = result_data
        speed = dict.fromkeys(result_data.keys())
        for i in speed:
            try:
                speed[i] = result_data[i]['speed']
            except BaseException:
                speed[i] = []
        print(speed)
        lst = []
        lst1 = []
        lst2 = []
        speed_ = dict.fromkeys(result_data.keys())
        dataset = []
        for i in speed:
            if i == "5G":
                for j in speed[i]:
                    x = (j / 1000000)
                    y = round(x, 1)
                    lst.append(y)
                print("hi", lst)
                speed_["5G"] = lst
                dataset.append(speed_["5G"])
            if i == "2.4G":
                for j in speed[i]:
                    x = (j / 1000000)
                    y = round(x, 1)
                    lst1.append(y)
                print("yes", lst1)
                speed_["2.4G"] = lst1
                dataset.append(speed_["2.4G"])
            if i == "Both":
                # print("yes", speed[i])
                for j in speed[i]:
                    x = (j / 1000000)
                    y = round(x, 1)
                    lst2.append(y)
                print(lst2)
                speed_["Both"] = lst2
                dataset.append(speed_["Both"])
        return dataset

    def summary_calculation(self, result_data, bands, threshold_5g, threshold_2g, threshold_both):
        self.result_data = result_data

        avg_dl_time = []
        html_struct = dict.fromkeys(list(result_data.keys()))
        for fcc in list(result_data.keys()):
            fcc_type = result_data[fcc]["avg"]
            for i in fcc_type:
                avg_dl_time.append(i)

        avg_dl_time_per_thou = []
        for i in avg_dl_time:
            i = i / 1000
            avg_dl_time_per_thou.append(i)

        avg_time_rounded = []
        for i in avg_dl_time_per_thou:
            i = str(round(i, 1))
            avg_time_rounded.append(i)

        pass_fail_list = []
        sumry2 = []
        sumry5 = []
        sumryB = []
        data = []

        for band in range(len(bands)):
            if bands[band] == "2.4G":
                # 2.4G
                if float(avg_time_rounded[band]) == 0.0 or float(avg_time_rounded[band]) > float(threshold_2g):
                    var = "FAIL"
                    pass_fail_list.append(var)
                    sumry2.append("FAIL")
                elif float(avg_time_rounded[band]) < float(threshold_2g):
                    pass_fail_list.append("PASS")
                    sumry2.append("PASS")
                data.append(','.join(sumry2))

            elif bands[band] == "5G":
                # 5G
                if float(avg_time_rounded[band]) == 0.0 or float(avg_time_rounded[band]) > float(threshold_5g):
                    print("FAIL")
                    pass_fail_list.append("FAIL")
                    sumry5.append("FAIL")
                elif float(avg_time_rounded[band]) < float(threshold_5g):
                    print("PASS")
                    pass_fail_list.append("PASS")
                    sumry5.append("PASS")
                data.append(','.join(sumry5))

            elif bands[band] == "Both":
                # BOTH
                if float(avg_time_rounded[band]) == 0.0 or float(avg_time_rounded[band]) > float(threshold_both):
                    var = "FAIL"
                    pass_fail_list.append(var)
                    sumryB.append("FAIL")
                elif float(avg_time_rounded[band]) < float(threshold_both):
                    pass_fail_list.append("PASS")
                    sumryB.append("PASS")
                data.append(','.join(sumryB))

        return data

    def check_station_ip(self):
        pass

    def generate_graph(self, dataset, lis, bands):
        graph = lf_graph.lf_bar_graph(_data_set=dataset, _xaxis_name="Stations", _yaxis_name="Time in Seconds",
                                      _xaxis_categories=lis, _label=bands, _xticks_font=8,
                                      _graph_image_name="webpage download time graph",
                                      _color=['forestgreen', 'darkorange', 'blueviolet'], _color_edge='black', _figsize=(14, 5),
                                      _grp_title="Download time taken by each client", _xaxis_step=1, _show_bar_value=True,
                                      _text_font=6, _text_rotation=60,
                                      _legend_loc="upper right",
                                      _legend_box=(1, 1.15),
                                      _enable_csv=True
                                      )
        graph_png = graph.build_bar_graph()
        print("graph name {}".format(graph_png))
        return graph_png

    def graph_2(self, dataset2, lis, bands):
        graph_2 = lf_graph.lf_bar_graph(_data_set=dataset2, _xaxis_name="Stations", _yaxis_name="Download Rate in Mbps",
                                        _xaxis_categories=lis, _label=bands, _xticks_font=8,
                                        _graph_image_name="webpage_speed_graph",
                                        _color=['forestgreen', 'darkorange', 'blueviolet'], _color_edge='black',
                                        _figsize=(14, 5),
                                        _grp_title="Download rate for each client (Mbps)", _xaxis_step=1, _show_bar_value=True,
                                        _text_font=6, _text_rotation=60,
                                        _legend_loc="upper right",
                                        _legend_box=(1, 1.15),
                                        _enable_csv=True
                                        )
        graph_png = graph_2.build_bar_graph()
        return graph_png

    def generate_report(self, date, num_stations, duration, test_setup_info, dataset, lis, bands, threshold_2g,
                        threshold_5g, threshold_both, dataset2, summary_table_value, result_data, test_rig,
                        test_tag, dut_hw_version, dut_sw_version, dut_model_num, dut_serial_num, test_id,
                        test_input_infor, csv_outfile):
        report = lf_report.lf_report(_results_dir_name="webpage_test", _output_html="Webpage.html", _output_pdf="Webpage.pdf")

        if bands == "Both":
            num_stations = num_stations * 2
        report.set_title("WEBPAGE DOWNLOAD TEST")
        report.set_date(date)
        report.build_banner()
        report.set_table_title("Test Setup Information")
        report.build_table_title()

        report.test_setup_table(value="Device under test", test_setup_data=test_setup_info)

        report.set_obj_html("Objective", "The Webpage Download Test is designed to test the performance of the "
                            "Access Point. The goal is to check whether the webpage loading time of all the "
                            + str(num_stations) +
                            "clients which are downloading at the same time meets the expectation when clients"
                            "connected on single radio as well as dual radio")
        report.build_objective()
        report.set_obj_html("Download Time Graph", "The below graph provides information about the download time taken "
                            "by each client to download webpage for test duration of  " + str(duration) + " min")
        report.build_objective()

        graph = self.generate_graph(dataset=dataset, lis=lis, bands=bands)
        report.set_graph_image(graph)
        report.set_csv_filename(graph)
        report.move_csv_file()
        report.move_graph_image()
        report.build_graph()
        report.set_obj_html("Download Rate Graph", "The below graph provides information about the download rate in "
                            "Mbps of each client to download the webpage for test duration of " + str(duration) + " min")
        report.build_objective()
        graph2 = self.graph_2(dataset2, lis=lis, bands=bands)
        print("graph name {}".format(graph2))
        report.set_graph_image(graph2)
        report.set_csv_filename(graph2)
        report.move_csv_file()
        report.move_graph_image()
        report.build_graph()
        report.set_obj_html("Summary Table Description", "This Table shows you the summary "
                            "result of Webpage Download Test as PASS or FAIL criteria. If the average time taken by " +
                            str(num_stations) + " clients to access the webpage is less than " + str( threshold_2g) +
                            "s it's a PASS criteria for 2.4 ghz clients, If the average time taken by " + "" +
                            str( num_stations) + " clients to access the webpage is less than " + str( threshold_5g) +
                            "s it's a PASS criteria for 5 ghz clients and If the average time taken by " + str( num_stations) +
                            " clients to access the webpage is less than " + str(threshold_both) +
                            "s it's a PASS criteria for 2.4 ghz and 5ghz clients")

        report.build_objective()
        test_setup1 = pd.DataFrame(summary_table_value)
        report.set_table_dataframe(test_setup1)
        report.build_table()

        report.set_obj_html("Download Time Table Description", "This Table will provide you information of the "
                            "minimum, maximum and the average time taken by clients to download a webpage in seconds")

        report.build_objective()
        x = []
        for fcc in list(result_data.keys()):
            fcc_type = result_data[fcc]["min"]
            # print(fcc_type)
            for i in fcc_type:
                x.append(i)
            # print(x)
        y = []
        for i in x:
            i = i / 1000
            y.append(i)
        z = []
        for i in y:
            i = str(round(i, 1))
            z.append(i)
        # rint(z)
        x1 = []

        for fcc in list(result_data.keys()):
            fcc_type = result_data[fcc]["max"]
            # print(fcc_type)
            for i in fcc_type:
                x1.append(i)
            # print(x1)
        y1 = []
        for i in x1:
            i = i / 1000
            y1.append(i)
        z1 = []
        for i in y1:
            i = str(round(i, 1))
            z1.append(i)
        # print(z1)
        x2 = []

        for fcc in list(result_data.keys()):
            fcc_type = result_data[fcc]["avg"]
            # print(fcc_type)
            for i in fcc_type:
                x2.append(i)
            # print(x2)
        y2 = []
        for i in x2:
            i = i / 1000
            y2.append(i)
        z2 = []
        for i in y2:
            i = str(round(i, 1))
            z2.append(i)

        download_table_value = {
            "Band": bands,
            "Minimum": z,
            "Maximum": z1,
            "Average": z2
        }

        # Get the report path to create the kpi.csv path
        kpi_path = report.get_report_path()
        print("kpi_path :{kpi_path}".format(kpi_path=kpi_path))

        kpi_csv = lf_kpi_csv.lf_kpi_csv(
            _kpi_path=kpi_path,
            _kpi_test_rig=test_rig,
            _kpi_test_tag=test_tag,
            _kpi_dut_hw_version=dut_hw_version,
            _kpi_dut_sw_version=dut_sw_version,
            _kpi_dut_model_num=dut_model_num,
            _kpi_dut_serial_num=dut_serial_num,
            _kpi_test_id=test_id)
        kpi_csv.kpi_dict['Units'] = "Mbps"
        for band in range(len(download_table_value["Band"])):
            kpi_csv.kpi_csv_get_dict_update_time()
            kpi_csv.kpi_dict['Graph-Group'] = "Webpage Download {band}".format(
                band=download_table_value['Band'][band])
            kpi_csv.kpi_dict['short-description'] = "Webpage download {band} Minimum".format(
                band=download_table_value['Band'][band])
            kpi_csv.kpi_dict['numeric-score'] = "{min}".format(min=download_table_value['Minimum'][band])
            kpi_csv.kpi_csv_write_dict(kpi_csv.kpi_dict)
            kpi_csv.kpi_dict['short-description'] = "Webpage download {band} Maximum".format(
                band=download_table_value['Band'][band])
            kpi_csv.kpi_dict['numeric-score'] = "{max}".format(max=download_table_value['Maximum'][band])
            kpi_csv.kpi_csv_write_dict(kpi_csv.kpi_dict)
            kpi_csv.kpi_dict['short-description'] = "Webpage download {band} Average".format(
                band=download_table_value['Band'][band])
            kpi_csv.kpi_dict['numeric-score'] = "{avg}".format(avg=download_table_value['Average'][band])
            kpi_csv.kpi_csv_write_dict(kpi_csv.kpi_dict)

        if csv_outfile is not None:
            current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
            csv_outfile = "{}_{}-test_l3_longevity.csv".format(
                csv_outfile, current_time)
            csv_outfile = report.file_add_path(csv_outfile)
            print("csv output file : {}".format(csv_outfile))

        test_setup = pd.DataFrame(download_table_value)
        report.set_table_dataframe(test_setup)
        report.build_table()
        report.set_table_title("Test input Information")
        report.build_table_title()
        report.test_setup_table(value="Information", test_setup_data=test_input_infor)
        report.build_footer()
        html_file = report.write_html()
        print("returned file {}".format(html_file))
        print(html_file)
        report.write_pdf_with_timestamp(_page_size='A4', _orientation='Landscape')


def main():
    # set up logger
    logger_config = lf_logger_config.lf_logger_config()
    parser = argparse.ArgumentParser(
        prog="lf_webpage.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description='''
---------------------------
LANforge Webpage Download Test Script - lf_webpage.py
---------------------------
Summary:
This script will create 40 clients on 5Ghz , 2.4Ghz and Both and generate layer4 traffic on LANforge ,The Webpage
 Download Test is designed to test the performance of the  Access Point. The goal is to  check whether the webpage
 loading time meets the expectation when clients connected on single radio as well as dual radio.
---------------------------
CLI Example: 
./lf_webpage.py --mgr <ip_address> --fiveg_ssid <5G_ssid> --fiveg_security wpa2 --fiveg_passwd <passwd> 
--twog_ssid <2G_ssid> --twog_security wpa2 --twog_passwd <passwd> --fiveg_radio wiphy0 --twog_radio wiphy1 
--num_stations 5 --upstream_port eth1 --duration 1  
---------------------------         
        ''')
    parser.add_argument('--mgr', help='hostname for where LANforge GUI is running', default='localhost')
    parser.add_argument('--mgr_port', help='port LANforge GUI HTTP service is running on', default=8080)
    parser.add_argument('--upstream_port', help='non-station port that generates traffic: eg: eth1', default='eth2')
    parser.add_argument('--num_stations', type=int, help='number of stations to create', default=1)
    parser.add_argument('--twog_radio', help='specify radio for 2.4G clients', default='wiphy3')
    parser.add_argument('--fiveg_radio', help='specify radio for 5 GHz client', default='wiphy0')
    parser.add_argument('--twog_security', help='WiFi Security protocol: {open|wep|wpa2|wpa3} for 2.4G clients')
    parser.add_argument('--twog_ssid', help='WiFi SSID for script object to associate for 2.4G clients')
    parser.add_argument('--twog_passwd', help='WiFi passphrase/password/key for 2.4G clients')
    parser.add_argument('--fiveg_security', help='WiFi Security protocol: {open|wep|wpa2|wpa3} for 5G clients')
    parser.add_argument('--fiveg_ssid', help='WiFi SSID for script object to associate for 5G clients')
    parser.add_argument('--fiveg_passwd', help='WiFi passphrase/password/key for 5G clients')
    parser.add_argument('--target_per_ten', help='number of request per 10 minutes', default=100)
    parser.add_argument('--file_size', type=str, help='specify the size of file you want to download', default='5MB')
    parser.add_argument('--bands', nargs="+", help='specify which band testing you want to run eg 5G OR 2.4G OR Both',
                        default=["5G", "2.4G"])
    parser.add_argument('--duration', type=int, help='time to run traffic')
    parser.add_argument('--threshold_5g', help="Enter the threshold value for 5G Pass/Fail criteria", default="60")
    parser.add_argument('--threshold_2g', help="Enter the threshold value for 2.4G Pass/Fail criteria", default="90")
    parser.add_argument('--threshold_both', help="Enter the threshold value for Both Pass/Fail criteria", default="50")
    parser.add_argument('--ap_name', help="specify the ap model ", default="TestAP")
    parser.add_argument('--ssh_port', type=int, help="specify the ssh port eg 22", default=22)
    parser.add_argument("--test_rig", default="", help="test rig for kpi.csv, testbed that the tests are run on")
    parser.add_argument("--test_tag", default="",
                        help="test tag for kpi.csv,  test specific information to differentiate the test")
    parser.add_argument("--dut_hw_version", default="",
                        help="dut hw version for kpi.csv, hardware version of the device under test")
    parser.add_argument("--dut_sw_version", default="",
                        help="dut sw version for kpi.csv, software version of the device under test")
    parser.add_argument("--dut_model_num", default="",
                        help="dut model for kpi.csv,  model number / name of the device under test")
    parser.add_argument("--dut_serial_num", default="",
                        help="dut serial for kpi.csv, serial number / serial number of the device under test")
    parser.add_argument("--test_priority", default="", help="dut model for kpi.csv,  test-priority is arbitrary number")
    parser.add_argument("--test_id", default="lf_webpage", help="test-id for kpi.csv,  script or test name")
    parser.add_argument('--csv_outfile', help="--csv_outfile <Output file for csv data>", default="")

    args = parser.parse_args()
    args.bands.sort()

    # Error checking to prevent case issues
    for band in range(len(args.bands)):
        args.bands[band] = args.bands[band].upper()
        if args.bands[band] == "BOTH":
            args.bands[band] = "Both"

    # Error checking for non-existent bands
    valid_bands = ['2.4G', '5G', 'Both']
    for band in args.bands:
        if band not in valid_bands:
            raise ValueError("Invalid band '%s' used in bands argument!" % band)

    # Check for Both being used independently
    if len(args.bands) > 1 and "Both" in args.bands:
        raise ValueError("'Both' test type must be used independently!")

    test_time = datetime.now()
    test_time = test_time.strftime("%b %d %H:%M:%S")
    print("Test started at ", test_time)
    list5G = []
    list5G_bytes = []
    list5G_speed = []
    list2G = []
    list2G_bytes = []
    list2G_speed = []
    Both = []
    Both_bytes = []
    Both_speed = []
    dict_keys = []
    dict_keys.extend(args.bands)
    # print(dict_keys)
    final_dict = dict.fromkeys(dict_keys)
    # print(final_dict)
    dict1_keys = ['dl_time', 'min', 'max', 'avg', 'bytes_rd', 'speed']
    for i in final_dict:
        final_dict[i] = dict.fromkeys(dict1_keys)
    print(final_dict)
    min5 = []
    min2 = []
    min_both = []
    max5 = []
    max2 = []
    max_both = []
    avg2 = []
    avg5 = []
    avg_both = []

    for bands in args.bands:
        if bands == "2.4G":
            security = [args.twog_security]
            ssid = [args.twog_ssid]
            passwd = [args.twog_passwd]
        elif bands == "5G":
            security = [args.fiveg_security]
            ssid = [args.fiveg_ssid]
            passwd = [args.fiveg_passwd]
        elif bands == "Both":
            security = [args.twog_security, args.fiveg_security]
            ssid = [args.twog_ssid, args.fiveg_ssid]
            passwd = [args.twog_passwd, args.fiveg_passwd]
        http = HttpDownload(lfclient_host=args.mgr, lfclient_port=args.mgr_port,
                            upstream=args.upstream_port, num_sta=args.num_stations,
                            security=security,
                            ssid=ssid, password=passwd,
                            target_per_ten=args.target_per_ten,
                            file_size=args.file_size, bands=bands,
                            twog_radio=args.twog_radio,
                            fiveg_radio=args.fiveg_radio
                            )
        http.file_create(ssh_port=args.ssh_port)
        http.set_values()
        http.precleanup()
        http.build()
        http.start()
        duration = args.duration
        duration = 60 * duration
        print("time in seconds ", duration)
        time.sleep(duration)
        http.stop()
        uc_avg_val = http.my_monitor('uc-avg')
        rx_bytes_val = http.my_monitor('bytes-rd')
        rx_rate_val = http.my_monitor('rx rate')
        http.postcleanup()

        if bands == "5G":
            print("yes")
            list5G.extend(uc_avg_val)
            list5G_bytes.extend(rx_bytes_val)
            list5G_speed.extend(rx_rate_val)
            print(list5G)
            print(list5G_bytes)
            print(list5G_speed)
            final_dict['5G']['dl_time'] = list5G
            min5.append(min(list5G))
            final_dict['5G']['min'] = min5
            max5.append(max(list5G))
            final_dict['5G']['max'] = max5
            avg5.append((sum(list5G) / args.num_stations))
            final_dict['5G']['avg'] = avg5
            final_dict['5G']['bytes_rd'] = list5G_bytes
            final_dict['5G']['speed'] = list5G_speed
        elif bands == "2.4G":
            print("no")
            list2G.extend(uc_avg_val)
            list2G_bytes.extend(rx_bytes_val)
            list2G_speed.extend(rx_rate_val)
            print(list2G)
            print(list2G_bytes)
            print(list2G_speed)
            final_dict['2.4G']['dl_time'] = list2G
            min2.append(min(list2G))
            final_dict['2.4G']['min'] = min2
            max2.append(max(list2G))
            final_dict['2.4G']['max'] = max2
            avg2.append((sum(list2G) / args.num_stations))
            final_dict['2.4G']['avg'] = avg2
            final_dict['2.4G']['bytes_rd'] = list2G_bytes
            final_dict['2.4G']['speed'] = list2G_speed
        elif bands == "Both":
            Both.extend(uc_avg_val)
            Both_bytes.extend(rx_bytes_val)
            Both_speed.extend(rx_rate_val)
            final_dict['Both']['dl_time'] = Both
            min_both.append(min(Both))
            final_dict['Both']['min'] = min_both
            max_both.append(max(Both))
            final_dict['Both']['max'] = max_both
            avg_both.append((sum(Both) / args.num_stations))
            final_dict['Both']['avg'] = avg_both
            final_dict['Both']['bytes_rd'] = Both_bytes
            final_dict['Both']['speed'] = Both_speed

    result_data = final_dict
    print("result", result_data)
    print("Test Finished")
    test_end = datetime.now()
    test_end = test_end.strftime("%b %d %H:%M:%S")
    print("Test ended at ", test_end)
    s1 = test_time
    s2 = test_end  # for example
    FMT = '%b %d %H:%M:%S'
    test_duration = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)

    info_ssid = []
    info_security = []
    for band in args.bands:
        if band == "2.4G":
            info_ssid.append(args.twog_ssid)
            info_security.append(args.twog_security)
        elif band == "5G":
            info_ssid.append(args.fiveg_ssid)
            info_security.append(args.fiveg_security)
        elif band == "Both":
            info_ssid.append(args.fiveg_ssid)
            info_security.append(args.fiveg_security)
            info_ssid.append(args.twog_ssid)
            info_security.append(args.twog_security)

    print("total test duration ", test_duration)
    date = str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
    test_setup_info = {
        "DUT Name": args.ap_name,
        "SSID": ', '.join(info_ssid),
        "Test Duration": test_duration,
    }
    test_input_infor = {
        "LANforge ip": args.mgr,
        "File Size": args.file_size,
        "Bands": args.bands,
        "Upstream": args.upstream_port,
        "Stations": args.num_stations,
        "SSID": ','.join(info_ssid),
        "Security": ', '.join(info_security),
        "Duration": args.duration,
        "Contact": "support@candelatech.com"
    }

    dataset = http.download_time_in_sec(result_data=result_data)
    lis = []
    if bands == "Both":
        for i in range(1, args.num_stations*2 + 1):
            lis.append(i)
    else:
        for i in range(1, args.num_stations + 1):
            lis.append(i)

    dataset2 = http.speed_in_Mbps(result_data=result_data)

    data = http.summary_calculation(
        result_data=result_data,
        bands=args.bands,
        threshold_5g=args.threshold_5g,
        threshold_2g=args.threshold_2g,
        threshold_both=args.threshold_both)
    summary_table_value = {
        "": args.bands,
        "PASS/FAIL": data
    }

    http.generate_report(date, num_stations=args.num_stations,
                          duration=args.duration, test_setup_info=test_setup_info, dataset=dataset, lis=lis,
                          bands=args.bands, threshold_2g=args.threshold_2g, threshold_5g=args.threshold_5g,
                          threshold_both=args.threshold_both, dataset2=dataset2,
                          summary_table_value=summary_table_value, result_data=result_data,
                          test_rig=args.test_rig, test_tag=args.test_tag, dut_hw_version=args.dut_hw_version,
                          dut_sw_version=args.dut_sw_version, dut_model_num=args.dut_model_num,
                          dut_serial_num=args.dut_serial_num, test_id=args.test_id,
                          test_input_infor=test_input_infor, csv_outfile=args.csv_outfile)


if __name__ == '__main__':
    main()
