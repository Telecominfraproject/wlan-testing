""" lf_ftp.py will verify that N clients connected on specified band and can simultaneously download/upload some amount of file from FTP server and measuring the time taken by client to download/upload the file.
    cli- python3 lf_ftp.py --mgr localhost --mgr_port 8080 --upstream_port eth1 --ssid FTP --security open --passwd BLANK --ap_name WAC505 --ap_ip 192.168.213.90 --bands Both --directions Download --twog_radio wiphy1 --fiveg_radio wiphy0 --file_size 2MB --num_stations 40 --Both_duration 1 --traffic_duration 2 --ssh_port 22_
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.
"""
import sys
import importlib
import paramiko
import argparse
from datetime import datetime
import time
import os
import matplotlib.patches as mpatches

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


class FtpTest(LFCliBase):
    def __init__(self, lfclient_host="localhost", lfclient_port=8080, sta_prefix="sta", start_id=0, num_sta=None,
                 dut_ssid=None, dut_security=None, dut_passwd=None, file_size=None, band=None, twog_radio=None,
                 fiveg_radio=None, upstream="eth1", _debug_on=False, _exit_on_error=False, _exit_on_fail=False,
                 direction=None, duration=None, traffic_duration=None, ssh_port=None):
        super().__init__(lfclient_host, lfclient_port, _debug=_debug_on, _exit_on_fail=_exit_on_fail)
        print("Test is about to start")
        self.host = lfclient_host
        self.port = lfclient_port
        # self.radio = radio
        self.upstream = upstream
        self.sta_prefix = sta_prefix
        self.sta_start_id = start_id
        self.num_sta = num_sta
        self.ssid = dut_ssid
        self.security = dut_security
        self.password = dut_passwd
        self.requests_per_ten = 1
        self.band = band
        self.file_size = file_size
        self.direction = direction
        self.twog_radio = twog_radio
        self.fiveg_radio = fiveg_radio
        self.duration = duration
        self.traffic_duration = traffic_duration
        self.ssh_port = ssh_port
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.cx_profile = self.local_realm.new_http_profile()
        self.port_util = realm.PortUtils(self.local_realm)
        self.cx_profile.requests_per_ten = self.requests_per_ten

        print("Test is Initialized")

    def set_values(self):
        '''This method will set values according user input'''

        if self.band == "5G":
            self.radio = [self.fiveg_radio]
        elif self.band == "2.4G":
            self.radio = [self.twog_radio]
        elif self.band == "Both":
            self.radio = [self.fiveg_radio, self.twog_radio]

            # if Both then number of stations are half for 2.4G and half for 5G
            self.num_sta = self.num_sta // 2

        # converting minutes into time stamp
        self.pass_fail_duration = self.duration
        self.duration = self.convert_min_in_time(self.duration)
        self.traffic_duration = self.convert_min_in_time(self.traffic_duration)

        # file size in Bytes
        self.file_size_bytes = int(self.convert_file_size_in_Bytes(self.file_size))

    def precleanup(self):
        self.count = 0

        # delete everything in the GUI before starting the script
        '''try:
            self.local_realm.load("BLANK")
        except:
            print("Couldn't load 'BLANK' Test configurations")'''

        for rad in self.radio:
            if rad == self.fiveg_radio:

                # select mode(All stations will connects to 5G)
                self.station_profile.mode = 9
                self.count = self.count + 1

            elif rad == self.twog_radio:

                # select mode(All stations will connects to 2.4G)
                self.station_profile.mode = 6
                self.count = self.count + 1

            # check Both band if both band then for 2G station id start with 20
            if self.count == 2:
                self.sta_start_id = self.num_sta
                self.num_sta = 2 * (self.num_sta)

                # if Both band then first 20 stations will connects to 5G
                self.station_profile.mode = 9

                self.cx_profile.cleanup()

                # create station list with sta_id 20
                self.station_list1 = LFUtils.portNameSeries(prefix_=self.sta_prefix, start_id_=self.sta_start_id,
                                                            end_id_=self.num_sta - 1, padding_number_=10000,
                                                            radio=rad)

                # cleanup station list which started sta_id 20
                self.station_profile.cleanup(self.station_list1, debug_=self.debug)
                LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                                   port_list=self.station_list,
                                                   debug=self.debug)
                return
            # clean layer4 ftp traffic
            self.cx_profile.cleanup()
            self.station_list = LFUtils.portNameSeries(prefix_=self.sta_prefix, start_id_=self.sta_start_id,
                                                       end_id_=self.num_sta - 1, padding_number_=10000,
                                                       radio=rad)

            # cleans stations
            self.station_profile.cleanup(self.station_list, delay=1.5, debug_=self.debug)
            LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                               port_list=self.station_list,
                                               debug=self.debug)
            time.sleep(1)

        print("precleanup done")

    def build(self):
        # set ftp
        self.port_util.set_ftp(port_name=self.local_realm.name_to_eid(self.upstream)[2], resource=1, on=True)

        for rad in self.radio:

            # station build
            self.station_profile.use_security(self.security, self.ssid, self.password)
            self.station_profile.set_number_template("00")
            self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
            self.station_profile.set_command_param("set_port", "report_timer", 1500)
            self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
            self.station_profile.create(radio=rad, sta_names_=self.station_list, debug=self.debug)
            self.local_realm.wait_until_ports_appear(sta_list=self.station_list)
            self.station_profile.admin_up()
            if self.local_realm.wait_for_ip(self.station_list):
                self._pass("All stations got IPs")
            else:
                self._fail("Stations failed to get IPs")
                # exit(1)

            # building layer4
            self.cx_profile.direction = "dl"
            self.cx_profile.dest = "/dev/null"
            print('Direction:', self.direction)

            if self.direction == "Download":

                # data from GUI for find out ip addr of upstream port
                data = self.json_get("ports/list?fields=IP")

                for i in data["interfaces"]:
                    for j in i:
                        if "1.1." + self.upstream == j:
                            ip_upstream = i["1.1." + self.upstream]['ip']

                self.cx_profile.create(ports=self.station_profile.station_names, ftp_ip=ip_upstream + "/ftp_test.txt",
                                       sleep_time=.5, debug_=self.debug, suppress_related_commands_=True, ftp=True,
                                       user="lanforge",
                                       passwd="lanforge", source="")


            elif self.direction == "Upload":
                dict_sta_and_ip = {}

                # data from GUI for find out ip addr of each station
                data = self.json_get("ports/list?fields=IP")

                # This loop for find out proper ip addr and station name
                for i in self.station_list:
                    for j in data['interfaces']:
                        for k in j:
                            if i == k:
                                dict_sta_and_ip[k] = j[i]['ip']

                # list of ip addr of all stations
                ip = list(dict_sta_and_ip.values())

                eth_list = []
                client_list = []

                # list of all stations
                for i in range(len(self.station_list)):
                    client_list.append(self.station_list[i][4:])

                # list of upstream port
                eth_list.append(self.upstream)

                # create layer for connection for upload
                for client_num in range(len(self.station_list)):
                    self.cx_profile.create(ports=eth_list, ftp_ip=ip[client_num] + "/ftp_test.txt", sleep_time=.5,
                                           debug_=self.debug, suppress_related_commands_=True, ftp=True,
                                           user="lanforge", passwd="lanforge",
                                           source="", upload_name=client_list[client_num])

            # check Both band present then build stations with another station list
            if self.count == 2:
                self.station_list = self.station_list1

                # if Both band then another 20 stations will connects to 2.4G
                self.station_profile.mode = 6
        print("Test Build done")

    def start(self, print_pass=False, print_fail=False):
        for rad in self.radio:
            self.cx_profile.start_cx()

        print("Test Started")

    def stop(self):
        self.cx_profile.stop_cx()
        self.station_profile.admin_down()

    def postcleanup(self):
        self.cx_profile.cleanup()
        # self.local_realm.load("BLANK")
        self.station_profile.cleanup(self.station_profile.station_names, delay=1.5, debug_=self.debug)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)

    def file_create(self):
        '''This method will Create file for given file size'''

        ip = self.host
        user = "root"
        pswd = "lanforge"
        port = self.ssh_port
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=port, username=user, password=pswd, banner_timeout=600)
        cmd = '[ -f /home/lanforge/ftp_test.txt ] && echo "True" || echo "False"'
        stdin, stdout, stderr = ssh.exec_command(str(cmd))
        output = stdout.readlines()
        print(output)
        if output == ["True\n"]:
            cmd1 = "rm /home/lanforge/ftp_test.txt"
            stdin, stdout, stderr = ssh.exec_command(str(cmd1))
            output = stdout.readlines()
            time.sleep(10)
            cmd2 = "sudo fallocate -l " + self.file_size + " /home/lanforge/ftp_test.txt"
            stdin, stdout, stderr = ssh.exec_command(str(cmd2))
            print("File creation done %s" % self.file_size)
            output = stdout.readlines()
        else:
            cmd2 = "sudo fallocate -l " + self.file_size + " /home/lanforge/ftp_test.txt"
            stdin, stdout, stderr = ssh.exec_command(str(cmd2))
            print("File creation done %s" % self.file_size)
            output = stdout.readlines()
        ssh.close()
        time.sleep(1)
        return output

    def convert_file_size_in_Bytes(self, size):
        '''convert file size MB or GB into Bytes'''

        if (size.endswith("MB")) or (size.endswith("Mb")) or (size.endswith("GB")) or (size.endswith("Gb")):
            if (size.endswith("MB")) or (size.endswith("Mb")):
                return float(size[:-2]) * 10 ** 6
            elif (size.endswith("GB")) or (size.endswith("Gb")):
                return float(size[:-2]) * 10 ** 9

    def my_monitor(self, time1):
        # data in json format
        data = self.json_get("layer4/list?fields=bytes-rd")

        # list of layer 4 connections name
        self.data1 = []

        for i in range(self.num_sta):
            self.data1.append((str(list(data['endpoint'][i].keys())))[2:-2])

        data2 = self.data1
        list_of_time = []
        list1 = []
        list2 = []
        counter = 0

        for i in range(self.num_sta):
            list_of_time.append(0)
        #running layer 4 traffic upto user given time
        while str(datetime.datetime.now() - time1) <= self.traffic_duration:
            if list_of_time.count(0) == 0:
                break

            while list_of_time.count(0) != 0:

                # run script upto given time
                if counter == 0:
                    if str(datetime.datetime.now() - time1) >= self.duration:
                        counter = counter + 1
                        break
                else:
                    if str(datetime.datetime.now() - time1) >= self.traffic_duration:
                        break

                for i in range(self.num_sta):
                    data = self.json_get("layer4/list?fields=bytes-rd")

                    # reading uc-avg data in json format
                    uc_avg = self.json_get("layer4/list?fields=uc-avg")
                    if data['endpoint'][i][data2[i]]['bytes-rd'] <= self.file_size_bytes:
                        data = self.json_get("layer4/list?fields=bytes-rd")
                    if data['endpoint'][i][data2[i]]['bytes-rd'] >= self.file_size_bytes:
                        list1.append(i)
                        if list1.count(i) == 1:
                            list2.append(i)
                            list1 = list2

                            # stop station after download or upload file with particular size
                            self.json_post("/cli-json/set_cx_state", {
                                "test_mgr": "default_tm",
                                "cx_name": "CX_" + data2[i],
                                "cx_state": "STOPPED"
                            }, debug_=self.debug)

                            list_of_time[i] = round(int(uc_avg['endpoint'][i][data2[i]]['uc-avg']) / 1000, 1)
                time.sleep(0.5)

        # method calling for throughput calculation
        self.throughput_calculation()

        # return list of download/upload time in seconds
        return list_of_time

    def throughput_calculation(self):
        '''Method for calculate throughput of each station'''

        self.list_of_throughput = []
        data = self.json_get("layer4/list?fields=bytes-rd")
        for i in range(self.num_sta):
            throughput = data['endpoint'][i][self.data1[i]]['bytes-rd'] / 10 ** 6
            if isinstance(throughput, float):
                self.list_of_throughput.append(round(throughput, 2))
            else:
                self.list_of_throughput.append(throughput)

    def ftp_test_data(self, list_time, pass_fail, bands, file_sizes, directions, num_stations):
        '''Method for arrange ftp download/upload time data in dictionary'''

        # creating dictionary for single iteration
        create_dict = {}

        create_dict["band"] = self.band
        create_dict["direction"] = self.direction
        create_dict["file_size"] = self.file_size
        create_dict["time"] = list_time
        create_dict["duration"] = self.pass_fail_duration
        create_dict["result"] = pass_fail
        create_dict["bands"] = bands
        create_dict["file_sizes"] = file_sizes
        create_dict["directions"] = directions
        create_dict["num_stations"] = num_stations
        create_dict["throughput"] = self.list_of_throughput

        return create_dict

    def convert_min_in_time(self, total_minutes):
        # Get hours with floor division
        hours = total_minutes // 60

        # Get additional minutes with modulus
        minutes = total_minutes % 60

        # Create time as a string
        time_string = str("%d:%02d" % (divmod(total_minutes, 60))) + ":00" + ":000000"

        return time_string

    def pass_fail_check(self, time_list):
        if max(time_list) < (self.pass_fail_duration * 60):
            return "Pass"
        else:
            return "Fail"

    def add_pass_fail_table(self, result_data):
        '''Method for create dict for pass/fail table for report'''

        self.column_head = []
        self.rows_head = []
        self.bands = result_data[1]["bands"]
        self.file_sizes = result_data[1]["file_sizes"]
        self.directions = result_data[1]["directions"]
        self.num_stations = result_data[1]["num_stations"]

        for size in self.file_sizes:
            for direction in self.directions:
                self.column_head.append(size + " " + direction)
        for band in self.bands:
            if band != "Both":
                self.rows_head.append(str(self.num_stations) + " Clients-" + band)
            else:
                self.rows_head.append(str(self.num_stations // 2) + "+" + str(self.num_stations // 2) + " Clients-2.4G+5G")

        #creating dict for a table
        table_dict_pass_fail = {}
        i = 0
        table_dict_pass_fail[""] = self.rows_head
        for size in self.file_sizes:
            for d in self.directions:
                list_data = []
                for b in self.bands:
                    for data in result_data.values():
                        if data["band"] == b and data["direction"] == d and data["file_size"] == size:
                            list_data.append(data["result"])

                table_dict_pass_fail[self.column_head[i]] = list_data
                i = i + 1

        return table_dict_pass_fail

    def download_upload_time_table(self,result_data):
        '''Method for create dict for download/upload table for report'''

        table_dict_time = {}
        string_data = ""
        i = 0
        table_dict_time[""] = self.rows_head

        for size in self.file_sizes:
            for d in self.directions:
                list_data = []
                for b in self.bands:
                    for data in result_data.values():
                        data_time = data['time']
                        if data_time.count(0) == 0:
                            Min = min(data_time)
                            Max = max(data_time)
                            Sum = int(sum(data_time))
                            Len = len(data_time)
                            Avg = round(Sum / Len, 2)
                        elif data_time.count(0) == len(data_time):
                            Min = "-"
                            Max = "-"
                            Avg = "-"
                        else:
                            data_time = [i for i in data_time if i != 0]
                            Min = min(data_time)
                            Max = max(data_time)
                            Sum = int(sum(data_time))
                            Len = len(data_time)
                            Avg = round(Sum / Len, 2)
                        string_data = "Min=" + str(Min) + ",Max=" + str(Max) + ",Avg=" + str(Avg) + " (sec)"

                        if data["band"] == b and data["direction"] == d and data["file_size"] == size:
                            list_data.append(string_data)

                table_dict_time[self.column_head[i]] = list_data
                i = i + 1

        return table_dict_time

    def generate_graph_time(self,result_data, x_axis, band, size):
        '''Method for generating graph for time'''

        num_stations = result_data[1]["num_stations"]
        dataset = []
        labels = []
        color = []
        graph_name = ""
        graph_description = ""
        count = 0
        handles = []
        for data in result_data.values():
            if data["band"] == band and data["file_size"] == size and data["direction"] == "Download":
                dataset.append(data["time"])
                labels.append("Download")

                #Adding red bar if client unable to download/upload file
                color_list = []
                #converting minutes in seconds
                duration = data["duration"] * 60
                for i in data["time"]:
                    if i < duration:
                        color_list.append("orange")
                    else:
                        color_list.append("red")
                if color_list.count("red") == 0:
                    handles.append(mpatches.Patch(color='orange', label='Download <= threshold time'))
                    num_col = 1
                    box = (1, 1.15)
                else:
                    handles.append(mpatches.Patch(color='orange', label='Download <= threshold time'))
                    handles.append(mpatches.Patch(color='red', label='Download > threshold time'))
                    num_col = 2
                    box = (1, 1.15)
                color.append(color_list)
                graph_name = "File size " + size + " " + str(
                    num_stations) + " Clients " + band + "-File Download Times(secs)"
                fail_count = len([i for i in data["time"] if i > (data["duration"] * 60)])
                graph_description = "Out of " + str(data["num_stations"]) + " clients, " + str(
                    data["num_stations"] - fail_count) + " are able to download " + "within " + str(
                    data["duration"]) + " min."
                count = count + 1
            if data["band"] == band and data["file_size"] == size and data["direction"] == "Upload":
                dataset.append(data["time"])
                labels.append("Upload")

                # Adding red bar if client unable to download/upload file
                color_list = []
                duration = data["duration"] * 60
                for i in data["time"]:
                    if i < duration:
                        color_list.append("blue")
                    else:
                        color_list.append("red")
                if color_list.count("red") == 0:
                    handles.append(mpatches.Patch(color='blue', label='Upload <= threshold time'))
                    num_col = 1
                    box = (1, 1.15)
                else:
                    handles.append(mpatches.Patch(color='blue', label='Upload <= threshold time'))
                    handles.append(mpatches.Patch(color='red', label='Upload < threshold time'))
                    num_col = 2
                    box = (1, 1.15)
                color.append(color_list)

                graph_name = "File size " + size + " " + str(
                    num_stations) + " Clients " + band + "-File Upload Times(secs)"
                fail_count = len([i for i in data["time"] if i > (data["duration"] * 60)])
                graph_description = graph_description + "Out of " + str(data["num_stations"]) + " clients, " + str(
                    data["num_stations"] - fail_count) + " are able to upload " + "within " + str(
                    data["duration"]) + " min."
                count = count + 1
        if count == 2:
            graph_name = "File size " + size + " " + str(
                num_stations) + " Clients " + band + "-File Download and Upload Times(secs)"
            handles = []
            for i in labels:
                if i == "Upload":
                    c = "blue"
                else:
                    c = "orange"
                handles.append(mpatches.Patch(color=c, label=i + " <= threshold time"))
            num_col = 2
            box = (1, 1.15)
            if (color[0].count("red") >= 1) or (color[1].count("red") >= 1):
                num_col = 3
                box = (1, 1.15)
                if labels[0] == "Download":
                    handles.append(mpatches.Patch(color='red', label='Download/Upload > threshold time'))
                else:
                    handles.append(mpatches.Patch(color='red', label='Upload/Download > threshold time'))


        self.report.set_obj_html(graph_name, graph_description)
        self.report.build_objective()
        image_name = "image"+band+size
        x_axis_name = "Stations"
        y_axis_name = "Time in seconds"
        self.bar_graph(x_axis, image_name, dataset, color, labels, x_axis_name, y_axis_name, handles, ncol=num_col, box=box, fontsize=12)

    def generate_graph_throughput(self, result_data, x_axis, band, size):
        '''Method for generating graph for time'''

        num_stations = result_data[1]["num_stations"]
        dataset = []
        labels = []
        color = []
        graph_name = ""
        graph_description = ""
        count = 0
        for data in result_data.values():
            if data["band"] == band and data["file_size"] == size and data["direction"] == "Download":
                dataset.append(data["throughput"])
                labels.append("Download")
                color.append("Orange")
                graph_name = "File size " + size + " " + str(
                    num_stations) + " Clients " + band + "-File Download Throughput(MB)"
                graph_description = str(data["num_stations"] - data["time"].count(0)) + " clients are able to download " + data["file_size"] + " file."
                count = count + 1
            if data["band"] == band and data["file_size"] == size and data["direction"] == "Upload":
                dataset.append(data["throughput"])
                labels.append("Upload")
                color.append("Blue")
                graph_name = "File size " + size + " " + str(
                    num_stations) + " Clients " + band + "-File Upload Throughput(MB)"
                graph_description = graph_description + str(data["num_stations"] - data["time"].count(0)) + " clients are able to upload " + data["file_size"] + " file."
                count = count + 1
        if count == 2:
            graph_name = "File size " + size + " " + str(
                num_stations) + " Clients " + band + "-File Download and Upload Throughput(MB)"

        self.report.set_obj_html(graph_name, graph_description)
        self.report.build_objective()
        image_name = "image" + band + size + "throughput"
        x_axis_name = "Stations"
        y_axis_name = "Throughput in MB"
        box = (1.1, 1.05)
        self.bar_graph(x_axis, image_name, dataset, color, labels, x_axis_name, y_axis_name, handles=None, ncol=1, box=box, fontsize=None)

    def bar_graph(self, x_axis, image_name, dataset, color, labels, x_axis_name, y_axis_name,handles, ncol, box, fontsize):
        '''This Method will plot bar graph'''

        graph = lf_bar_graph(_data_set=dataset,
                             _xaxis_name=x_axis_name,
                             _yaxis_name=y_axis_name,
                             _xaxis_categories=x_axis,
                             _label=labels,
                             _graph_image_name=image_name,
                             _figsize=(18, 6),
                             _color=color,
                             _show_bar_value=False,
                             _xaxis_step=None,
                             _legend_handles=handles,
                             _color_edge=None,
                             _text_rotation=40,
                             _legend_loc="upper right",
                             _legend_box=box,
                             _legend_ncol=ncol,
                             _legend_fontsize=fontsize,
                             _enable_csv=True)

        graph_png = graph.build_bar_graph()

        print("graph name {}".format(graph_png))

        self.report.set_graph_image(graph_png)
        # need to move the graph image to the results
        self.report.move_graph_image()
        self.report.set_csv_filename(graph_png)
        self.report.move_csv_file()

        self.report.build_graph()

    def generate_graph(self, result_data):
        '''This method will generate bar graph of time and throughput'''

        x_axis = []
        for i in range(1, self.num_stations + 1, 1):
            x_axis.append(i)

        for b in self.bands:
            for size in self.file_sizes:
                self.generate_graph_time(result_data, x_axis, b, size)
                self.generate_graph_throughput(result_data, x_axis, b, size)

    def generate_report(self, ftp_data, date,test_setup_info, input_setup_info):
        '''Method for generate the report'''

        self.report = lf_report(_results_dir_name="ftp_test", _output_html="ftp_test.html", _output_pdf="ftp_test.pdf")
        self.report.set_title("FTP Test")
        self.report.set_date(date)
        self.report.build_banner()
        self.report.set_table_title("Test Setup Information")
        self.report.build_table_title()
        self.report.test_setup_table(value="Device under test", test_setup_data=test_setup_info)

        self.report.set_obj_html("Objective",
                            "This FTP Test is used to Verify that N clients connected on Specified band and can simultaneously download/upload some amount of file from FTP server and measuring the time taken by client to Download/Upload the file.")
        self.report.build_objective()
        self.report.set_obj_html("PASS/FAIL Results",
                            "This Table will give Pass/Fail results.")
        self.report.build_objective()
        dataframe1 = pd.DataFrame(self.add_pass_fail_table(ftp_data))
        self.report.set_table_dataframe(dataframe1)
        self.report.build_table()
        self.report.set_obj_html("File Download/Upload Time (sec)",
                            "This Table will  give FTP Download/Upload Time of Clients.")
        self.report.build_objective()
        dataframe2 = pd.DataFrame(self.download_upload_time_table(ftp_data))
        self.report.set_table_dataframe(dataframe2)
        self.report.build_table()
        self.generate_graph(ftp_data)
        self.report.set_table_title("Test input Information")
        self.report.build_table_title()
        self.report.test_setup_table(value="Information", test_setup_data=input_setup_info)
        self.report.build_footer()
        html_file = self.report.write_html()
        print("returned file {}".format(html_file))
        print(html_file)
        self.report.write_pdf()







def main():
    parser = argparse.ArgumentParser(
        prog='lf_ftp.py',
        formatter_class=argparse.RawTextHelpFormatter,
        description="FTP Test Script")
    parser.add_argument('--mgr', help='hostname for where LANforge GUI is running', default='localhost')
    parser.add_argument('--mgr_port', help='port LANforge GUI HTTP service is running on', default=8080)
    parser.add_argument('--upstream_port', help='non-station port that generates traffic: eg: eth1', default='eth1')
    parser.add_argument('--ssid', type=str, help='--ssid')
    parser.add_argument('--passwd', type=str, help='--passwd')
    parser.add_argument('--security', type=str, help='--security')
    parser.add_argument('--ap_name', type=str, help='--ap_name')
    parser.add_argument('--ap_ip', type=str, help='--ap_ip')
    parser.add_argument('--twog_radio', type=str, help='specify radio for 2.4G clients', default='wiphy1')
    parser.add_argument('--fiveg_radio', type=str, help='specify radio for 5G client', default='wiphy0')
    parser.add_argument('--twog_duration', nargs="+", help='Pass and Fail duration for 2.4G band in minutes')
    parser.add_argument('--fiveg_duration', nargs="+", help='Pass and Fail duration for 5G band in minutes')
    parser.add_argument('--Both_duration', nargs="+", help='Pass and Fail duration for Both band in minutes')
    parser.add_argument('--traffic_duration', type=int, help='duration for layer 4 traffic running')
    parser.add_argument('--ssh_port', type=int, help="specify the shh port eg 22", default=22)

    # Test variables
    parser.add_argument('--bands', nargs="+", help='--bands defaults ["5G","2.4G","Both"]',
                        default=["5G", "2.4G", "Both"])
    parser.add_argument('--directions', nargs="+", help='--directions defaults ["Download","Upload"]',
                        default=["Download", "Upload"])
    parser.add_argument('--file_sizes', nargs="+", help='--File Size defaults ["2MB","500MB","1000MB"]',
                        default=["2MB", "500MB", "1000MB"])
    parser.add_argument('--num_stations', type=int, help='--num_stations is number of stations', default=40)

    args = parser.parse_args()

    # 1st time stamp for test duration
    time_stamp1 = datetime.datetime.now()

    # use for creating ftp_test dictionary
    iteraration_num = 0

    # empty dictionary for whole test data
    ftp_data = {}

    def pass_fail_duration(band, file_size):
        '''Method for set duration according file size and band which are given by user'''

        if band == "2.4G":
            if len(args.file_sizes) is not len(args.twog_duration):
                raise Exception("Give proper Pass or Fail duration for 2.4G band")

            for size in args.file_sizes:
                if size == file_size:
                    index = list(args.file_sizes).index(size)
                    duration = args.twog_duration[index]
        elif band == "5G":
            if len(args.file_sizes) is not len(args.fiveg_duration):
                raise Exception("Give proper Pass or Fail duration for 5G band")
            for size in args.file_sizes:
                if size == file_size:
                    index = list(args.file_sizes).index(size)
                    duration = args.fiveg_duration[index]
        else:
            if len(args.file_sizes) is not len(args.Both_duration):
                raise Exception("Give proper Pass or Fail duration for 5G band")
            for size in args.file_sizes:
                if size == file_size:
                    index = list(args.file_sizes).index(size)
                    duration = args.Both_duration[index]
        if duration.isdigit():
            duration = int(duration)
        else:
            duration = float(duration)

        return duration

    # For all combinations ftp_data of directions, file size and client counts, run the test
    for band in args.bands:
        for direction in args.directions:
            for file_size in args.file_sizes:
                # Start Test
                obj = FtpTest(lfclient_host=args.mgr,
                              lfclient_port=args.mgr_port,
                              upstream=args.upstream_port,
                              dut_ssid=args.ssid,
                              dut_passwd=args.passwd,
                              dut_security=args.security,
                              num_sta=args.num_stations,
                              band=band,
                              file_size=file_size,
                              direction=direction,
                              twog_radio=args.twog_radio,
                              fiveg_radio=args.fiveg_radio,
                              duration=pass_fail_duration(band, file_size),
                              traffic_duration=args.traffic_duration,
                              ssh_port=args.ssh_port
                              )

                iteraration_num = iteraration_num + 1
                obj.file_create()
                obj.set_values()
                obj.precleanup()
                obj.build()
                if not obj.passes():
                    print(obj.get_fail_message())
                    exit(1)

                # First time stamp
                time1 = datetime.datetime.now()

                obj.start(False, False)

                # return list of download/upload completed time stamp
                time_list = obj.my_monitor(time1)

                # check pass or fail
                pass_fail = obj.pass_fail_check(time_list)

                # dictionary of whole data
                ftp_data[iteraration_num] = obj.ftp_test_data(time_list, pass_fail, args.bands, args.file_sizes,
                                                              args.directions, args.num_stations)

                obj.stop()
                obj.postcleanup()

    # 2nd time stamp for test duration
    time_stamp2 = datetime.datetime.now()

    # total time for test duration
    test_duration = str(time_stamp2 - time_stamp1)[:-7]

    date = str(datetime.datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]

    #print(ftp_data)

    test_setup_info = {
        "AP Name": args.ap_name,
        "SSID": args.ssid,
        "Test Duration": test_duration
    }

    input_setup_info = {
        "AP IP": args.ap_ip,
        "File Size": args.file_sizes,
        "Bands": args.bands,
        "Direction": args.directions,
        "Stations": args.num_stations,
        "Upstream": args.upstream_port,
        "SSID": args.ssid,
        "Security": args.security,
        "Contact": "support@candelatech.com"
    }
    obj.generate_report(ftp_data,
                    date,
                    test_setup_info,
                    input_setup_info)


if __name__ == '__main__':
    main()

