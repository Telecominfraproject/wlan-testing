#!/usr/bin/env python3

"""

Name: lf_roam_test.py

purpose :
 lf__roam_test works on both roaming methods i.e. hard/forced roaming and also attenuation based roaming (soft roam)  specific to 11r
       - This script will give results of 11r roam test pdf along with all the packet captures generated after the roam test by default it functions as hard roaming process to
       perform soft roam soft_roam parameter needs to be set true
       - still under progress do not overwrite

LICENSE:
    Free to distribute and modify. LANforge systems must be licensed.
    Copyright 2021 Candela Technologies Inc
"""

import sys
import os
import importlib
import logging
import time
import datetime
from datetime import datetime
import pandas as pd
import paramiko
from itertools import chain
import argparse

logger = logging.getLogger(__name__)
if sys.version_info[0] != 3:
    logger.critical("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")
cv_test_reports = importlib.import_module("py-json.cv_test_reports")
lf_report = cv_test_reports.lanforge_reports
lf_report_pdf = importlib.import_module("py-scripts.lf_report")
lf_csv = importlib.import_module("py-scripts.lf_csv")
lf_pcap = importlib.import_module("py-scripts.lf_pcap")
lf_graph = importlib.import_module("py-scripts.lf_graph")
sniff_radio = importlib.import_module("py-scripts.lf_sniff_radio")
sta_connect = importlib.import_module("py-scripts.sta_connect2")
lf_clean = importlib.import_module("py-scripts.lf_cleanup")
series = importlib.import_module("cc_module_9800_3504")
attenuator = importlib.import_module("py-scripts.attenuator_serial")
modify = importlib.import_module("py-scripts.lf_atten_mod_test")


class HardRoam(Realm):
    def __init__(self, lanforge_ip=None,
                 lanforge_port=None,
                 lanforge_ssh_port=None,
                 c1_bssid=None,
                 c2_bssid=None,
                 fiveg_radio=None,
                 twog_radio=None,
                 sixg_radio=None,
                 band=None,
                 sniff_radio=None,
                 num_sta=None,
                 security=None,
                 security_key=None,
                 ssid=None,
                 upstream=None,
                 duration=None,
                 iteration=None,
                 channel=None,
                 option=None,
                 duration_based=None,
                 iteration_based=None,
                 dut_name=[],
                 traffic_type="lf_udp",
                 roaming_delay=None,
                 path="../",
                 scheme="ssh",
                 dest="localhost",
                 user="admin",
                 passwd="Cisco123",
                 prompt="WLC2",
                 series_cc="9800",
                 ap="AP687D.B45C.1D1C",
                 port="8888",
                 band_cc="5g",
                 timeout="10",
                 identity=None,
                 ttls_pass=None,
                 debug=False,
                 soft_roam=False
                 ):
        super().__init__(lanforge_ip,
                         lanforge_port)
        self.lanforge_ip = lanforge_ip
        self.lanforge_port = lanforge_port
        self.lanforge_ssh_port = lanforge_ssh_port
        self.c1_bssid = c1_bssid
        self.c2_bssid = c2_bssid
        self.fiveg_radios = fiveg_radio
        self.twog_radios = twog_radio
        self.sixg_radios = sixg_radio
        self.band = band
        self.sniff_radio = sniff_radio
        self.num_sta = num_sta
        self.ssid_name = ssid
        self.security = security
        self.security_key = security_key
        self.upstream = upstream
        self.duration = duration
        self.iteration = iteration
        self.channel = channel
        self.option = option
        self.iteration_based = iteration_based
        self.duration_based = duration_based
        self.local_realm = realm.Realm(lfclient_host=self.lanforge_ip, lfclient_port=self.lanforge_port)
        self.staConnect = sta_connect.StaConnect2(self.lanforge_ip, self.lanforge_port)
        self.final_bssid = []
        self.pcap_obj_2 = None
        self.pcap_name = None
        self.test_duration = None
        self.client_list = []
        self.dut_name = dut_name
        self.pcap_obj = lf_pcap.LfPcap()
        self.lf_csv_obj = lf_csv.lf_csv()
        self.traffic_type = traffic_type
        self.roam_delay = roaming_delay
        self.cx_profile = self.local_realm.new_l3_cx_profile()
        self.cc = None
        self.cc = series.create_controller_series_object(
            scheme=scheme,
            dest=dest,
            user=user,
            passwd=passwd,
            prompt=prompt,
            series=series_cc,
            ap=ap,
            port=port,
            band=band_cc,
            timeout=timeout)
        self.cc.pwd = path
        # self.cc.pwd = "../lanforge/lanforge-scripts"
        self.start_time = None
        self.end_time = None
        self.identity = identity
        self.ttls_pass = ttls_pass
        self.debug = debug
        self.mac_data = None
        self.soft_roam = soft_roam
        print("iteration", self.iteration)

        # logging.basicConfig(filename='roam.log', filemode='w', level=logging.INFO, force=True)

    # start debugger of controller
    def start_debug_(self, mac_list):
        mac = mac_list
        for i in mac:
            y = self.cc.debug_wireless_mac_cc(mac=str(i))
            print(y)

    # stop debugger of controller
    def stop_debug_(self, mac_list):
        mac = mac_list
        for i in mac:
            y = self.cc.no_debug_wireless_mac_cc(mac=str(i))
            print(y)

    # get trace file names from controller
    def get_ra_trace_file(self):
        ra = self.cc.get_ra_trace_files__cc()
        print(ra)
        ele_list = [y for y in (x.strip() for x in ra.splitlines()) if y]
        print(ele_list)
        return ele_list

    # get trace file names from controller with respect to number of clients
    def get_file_name(self, client):
        file_name = []
        if not self.debug:
            for i in range(client):
                file_name.append("debug disabled")
        else:
            file = self.get_ra_trace_file()
            indices = [i for i, s in enumerate(file) if 'dir bootflash: | i ra_trace' in s]
            # print(indices)
            y = indices[-1]

            if client == 1:
                z = file[y + 1]
                list_ = []
                list_.append(z)
                m = list_[0].split(" ")
                print(m)
                print(len(m))
                print(m[-1])
                if m[-1].isnumeric():
                    print("log file not available")
                    file_name.append("file not found")
                file_name.append(m[-1])
            else:
                z = file[y + (int(0) + 1)]
                list_ = []
                list_.append(z)
                m = list_[0].split(" ")
                print(m)
                print(len(m))
                print(m[-1])
                if m[-1].isnumeric():
                    print("log file not available")
                    for i in range(client):
                        file_name.append("file not found")
                else:
                    for i in range(client):
                        z = file[y + (int(i) + 1)]
                        list_ = []
                        list_.append(z)
                        m = list_[0].split(" ")
                        print(m)
                        print(len(m))
                        print(m[-1])
                        if m[-1].isnumeric():
                            print("log file not available")
                            file_name.append("file not found")
                        file_name.append(m[-1])
            print("file_name", file_name)
            file_name.reverse()

        return file_name

    # delete trace file from controller
    def delete_trace_file(self, file):
        # file = self.get_file_name()
        self.cc.del_ra_trace_file_cc(file=file)

    # get station list from lf
    def get_station_list(self):
        sta = self.staConnect.station_list()
        if sta == "no response":
            return "no response"
        sta_list = []
        for i in sta:
            for j in i:
                sta_list.append(j)
        return sta_list

    # create n number of clients of advanced configuration on lf
    def create_n_clients(self, start_id=0, sta_prefix=None, num_sta=None, dut_ssid=None,
                         dut_security=None, dut_passwd=None, radio=None, type=None):

        local_realm = realm.Realm(lfclient_host=self.lanforge_ip, lfclient_port=self.lanforge_port)
        station_profile = local_realm.new_station_profile()
        if self.band == "fiveg":
            radio = self.fiveg_radios
        if self.band == "twog":
            radio = self.twog_radios
        if self.band == "sixg":
            radio = self.sixg_radios

        # pre clean
        sta_list = self.get_station_list()
        print(sta_list)
        logging.info(str(sta_list))
        if not sta_list:
            print("no stations on lanforge")
            logging.info("no stations on lanforge")
        else:
            station_profile.cleanup(sta_list, delay=1)
            LFUtils.wait_until_ports_disappear(base_url=local_realm.lfclient_url,
                                               port_list=sta_list,
                                               debug=True)
            # time.sleep(2)
            print("pre cleanup done")
            logging.info("pre cleanup done")

        print("Creating stations.")
        logging.info("Creating stations.")
        station_list = LFUtils.portNameSeries(prefix_=sta_prefix, start_id_=start_id,
                                              end_id_=num_sta - 1, padding_number_=10000,
                                              radio=radio)

        if type == "11r-sae-802.1x":
            dut_passwd = "[BLANK]"
        station_profile.use_security(dut_security, dut_ssid, dut_passwd)
        station_profile.set_number_template("00")

        station_profile.set_command_flag("add_sta", "create_admin_down", 1)

        station_profile.set_command_param("set_port", "report_timer", 1500)

        # connect station to particular bssid
        # self.station_profile.set_command_param("add_sta", "ap", self.bssid[0])

        station_profile.set_command_flag("set_port", "rpt_timer", 1)
        if type == "11r":
            station_profile.set_command_flag("add_sta", "80211u_enable", 0)
            station_profile.set_command_flag("add_sta", "8021x_radius", 1)
            if not self.soft_roam:
                station_profile.set_command_flag("add_sta", "disable_roam", 1)
            if self.soft_roam:
                print("soft roam true")
                logging.info("soft roam true")
                if self.option == "otds":
                    print("otds present")
                    station_profile.set_command_flag("add_sta", "ft-roam-over-ds", 1)
            station_profile.set_command_flag("add_sta", "power_save_enable", 1)
            station_profile.set_wifi_extra(key_mgmt="FT-PSK     ",
                                           pairwise="",
                                           group="",
                                           psk="",
                                           eap="",
                                           identity="",
                                           passwd="",
                                           pin=""
                                           )
        if type == "11r-sae":
            station_profile.set_command_flag("add_sta", "ieee80211w", 2)
            station_profile.set_command_flag("add_sta", "80211u_enable", 0)
            station_profile.set_command_flag("add_sta", "8021x_radius", 1)
            # station_profile.set_command_flag("add_sta", "disable_roam", 1)
            if not self.soft_roam:
                station_profile.set_command_flag("add_sta", "disable_roam", 1)
            if self.soft_roam:
                if self.option == "otds":
                    station_profile.set_command_flag("add_sta", "ft-roam-over-ds", 1)
            station_profile.set_command_flag("add_sta", "power_save_enable", 1)
            station_profile.set_wifi_extra(key_mgmt="FT-SAE     ",
                                           pairwise="",
                                           group="",
                                           psk="",
                                           eap="",
                                           identity="",
                                           passwd="",
                                           pin=""
                                           )

        if type == "11r-sae-802.1x":
            station_profile.set_command_flag("set_port", "rpt_timer", 1)
            station_profile.set_command_flag("add_sta", "ieee80211w", 2)
            station_profile.set_command_flag("add_sta", "80211u_enable", 0)
            station_profile.set_command_flag("add_sta", "8021x_radius", 1)
            if not self.soft_roam:
                station_profile.set_command_flag("add_sta", "disable_roam", 1)
            if self.soft_roam:
                if self.option == "otds":
                    station_profile.set_command_flag("add_sta", "ft-roam-over-ds", 1)
            # station_profile.set_command_flag("add_sta", "disable_roam", 1)
            station_profile.set_command_flag("add_sta", "power_save_enable", 1)
            # station_profile.set_command_flag("add_sta", "ap", "68:7d:b4:5f:5c:3f")
            station_profile.set_wifi_extra(key_mgmt="FT-EAP     ",
                                           pairwise="[BLANK]",
                                           group="[BLANK]",
                                           psk="[BLANK]",
                                           eap="TTLS",
                                           identity=self.identity,
                                           passwd=self.ttls_pass,
                                           pin=""
                                           )

        station_profile.create(radio=radio, sta_names_=station_list)
        print("Waiting for ports to appear")
        logging.info("Waiting for ports to appear")
        local_realm.wait_until_ports_appear(sta_list=station_list)

        if self.soft_roam:
            for sta_name in station_list:
                sta = sta_name.split(".")[2]  # TODO:  Use name_to_eid
                # wpa_cmd = "roam " + str(checker2)

                bgscan = {
                    "shelf": 1,
                    "resource": 1,  # TODO:  Do not hard-code resource, get it from radio eid I think.
                    "port": str(sta),
                    "type": 'NA',
                    "text": 'bgscan="simple:30:-65:300"'
                }

                print(bgscan)
                logging.info(str(bgscan))
                self.local_realm.json_post("/cli-json/set_wifi_custom", bgscan)
                # time.sleep(2)

        station_profile.admin_up()
        print("Waiting for ports to admin up")
        logging.info("Waiting for ports to admin up")
        if local_realm.wait_for_ip(station_list):
            print("All stations got IPs")
            logging.info("All stations got IPs")
            # exit()
            return True
        else:
            print("Stations failed to get IPs")
            logging.info("Stations failed to get IPs")
            return False

    # create layer3 traffic on clients
    def create_layer3(self, side_a_min_rate, side_a_max_rate, side_b_min_rate, side_b_max_rate, side_a_min_pdu,
                      side_b_min_pdu,
                      traffic_type, sta_list):
        # checked
        print(sta_list)
        logging.info(str(sta_list))
        print(type(sta_list))
        print(self.upstream)
        logging.info(str(self.upstream))
        # cx_profile = self.local_realm.new_l3_cx_profile()
        self.cx_profile.host = self.lanforge_ip
        self.cx_profile.port = self.lanforge_port
        # layer3_cols = ['name', 'tx bytes', 'rx bytes', 'tx rate', 'rx rate']
        self.cx_profile.side_a_min_bps = side_a_min_rate
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate
        self.cx_profile.side_b_max_bps = side_b_max_rate
        self.cx_profile.side_a_min_pdu = side_a_min_pdu,
        self.cx_profile.side_b_min_pdu = side_b_min_pdu,

        # create
        print("Creating endpoints")
        logging.info("Creating endpoints")
        self.cx_profile.create(endp_type=traffic_type, side_a=sta_list,
                               side_b=self.upstream, sleep_time=0)
        self.cx_profile.start_cx()

    # get layer3 values
    def get_layer3_values(self, cx_name=None, query=None):
        url = f"/cx/{cx_name}"
        response = self.json_get(_req_url=url)
        result = response[str(cx_name)][str(query)]
        return result

    # get cross connect names
    def get_cx_list(self):
        layer3_result = self.local_realm.cx_list()
        layer3_names = [item["name"] for item in layer3_result.values() if "_links" in item]
        print(layer3_names)
        return layer3_names

    # get endpoint values
    def get_endp_values(self, endp="A", cx_name="niki", query="tx bytes"):
        # self.get_cx_list()
        # self.json_get("http://192.168.100.131:8080/endp/Unsetwlan000-0-B?fields=rx%20rate")
        url = f"/endp/{cx_name}-{endp}?fields={query}"
        response = self.json_get(_req_url=url)
        print(response)
        if (response is None) or ("endpoint" not in response):
            print("incomplete response:")
            exit(1)
        final = response["endpoint"][query]
        print(final)
        return final

    # precleanup on lanforge
    def precleanup(self):
        obj = lf_clean.lf_clean(host=self.lanforge_ip,
                                port=self.lanforge_port,
                                clean_cxs=True,
                                clean_endp=True)
        obj.resource = "all"
        obj.cxs_clean()
        obj.endp_clean()

    # get client data from lf
    def station_data_query(self, station_name="wlan0", query="channel"):
        url = f"/port/{1}/{1}/{station_name}?fields={query}"
        # print("url//////", url)
        response = self.local_realm.json_get(_req_url=url)
        print("response: ", response)
        if (response is None) or ("interface" not in response):
            print("station_list: incomplete response:")
            # pprint(response)
            exit(1)
        y = response["interface"][query]
        return y

    # start packet capture on lf
    # TODO:  Check if other monitor ports exist on this radio already.  If so, delete those
    # before adding new monitor port (or just use the existing monitor port without creating
    # a new one. --Ben
    def start_sniffer(self, radio_channel=None, radio=None, test_name="sniff_radio", duration=60):
        self.pcap_name = test_name + str(datetime.now().strftime("%Y-%m-%d-%H-%M")).replace(':', '-') + ".pcap"
        self.pcap_obj_2 = sniff_radio.SniffRadio(lfclient_host=self.lanforge_ip, lfclient_port=self.lanforge_port,
                                                 radio=radio, channel=radio_channel, monitor_name="monitor", channel_bw="20")
        self.pcap_obj_2.setup(0, 0, 0)
        time.sleep(5)
        self.pcap_obj_2.monitor.admin_up()
        time.sleep(5)
        self.pcap_obj_2.monitor.start_sniff(capname=self.pcap_name, duration_sec=duration)

    # stop packet capture and get file name
    def stop_sniffer(self):
        print("in stop_sniffer")
        directory = None
        directory_name = "pcap"
        if directory_name:
            directory = os.path.join("", str(directory_name))
        try:

            if not os.path.exists(directory):
                os.mkdir(directory)
        except Exception as x:
            print(x)

        self.pcap_obj_2.monitor.admin_down()
        time.sleep(2)
        self.pcap_obj_2.cleanup()
        lf_report.pull_reports(hostname=self.lanforge_ip, port=self.lanforge_ssh_port, username="lanforge",
                               password="lanforge",
                               report_location="/home/lanforge/" + self.pcap_name,
                               report_dir="pcap")
        time.sleep(10)

        return self.pcap_name

    # generate csv files at the begining
    def generate_csv(self):
        file_name = []
        for i in range(self.num_sta):
            file = 'test_client_' + str(i) + '.csv'
            lf_csv_obj = lf_csv.lf_csv(_columns=['Iterations', 'bssid1', 'bssid2', "Roam Time(ms)",
                                                 "PASS/FAIL", "Pcap file Name", "Log File", "Remark"], _rows=[],
                                       _filename=file)
            # "Packet loss",
            file_name.append(file)
            lf_csv_obj.generate_csv()
        return file_name

    # get journal ctl logs/ kernel logs
    def journal_ctl_logs(self, file):
        jor_lst = []
        name = "kernel_log" + file + ".txt"
        jor_lst.append(name)
        try:
            ssh = paramiko.SSHClient()
            command = "journalctl --since '5 minutes ago' > kernel_log" + file + ".txt"
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.lanforge_ip, port=self.lanforge_ssh_port, username="lanforge",
                        password="lanforge", banner_timeout=600)
            stdin, stdout, stderr = ssh.exec_command(str(command))
            stdout.readlines()
            ssh.close()
            kernel_log = "/home/lanforge/kernel_log" + file + ".txt"
            lf_report.pull_reports(hostname=self.lanforge_ip, port=self.lanforge_ssh_port, username="lanforge",
                                   password="lanforge", report_location=kernel_log, report_dir=".")
        except Exception as e:
            print(e)
        return jor_lst

    # gives wlan management status of pcap file
    def get_wlan_mgt_status(self, file_name,
                            filter="(wlan.fc.type_subtype eq 3 && wlan.fixed.status_code == 0x0000 && wlan.tag.number == 55)"):
        query_reasso_response = self.pcap_obj.get_wlan_mgt_status_code(pcap_file=str(file_name),
                                                                       filter=filter)
        print("query", query_reasso_response)
        return query_reasso_response

    # get attenuator serial number
    def attenuator_serial(self):
        obj = attenuator.AttenuatorSerial(
            lfclient_host=self.lanforge_ip,
            lfclient_port=self.lanforge_port
        )
        val = obj.show()
        return val

    def attenuator_modify(self, serno, idx, val):
        atten_obj = modify.CreateAttenuator(self.lanforge_ip, self.lanforge_port, serno, idx, val)
        atten_obj.build()

    # main roam fun
    def run(self, file_n=None):
        try:
            print("make both attenuators set to zero attenuation at the begining")
            logging.info("make both attenuators set to zero attenuation at the begining")
            ser_no = self.attenuator_serial()
            print(ser_no[0], ser_no[1])
            logging.info(str(ser_no[0]) + " , " + str(ser_no[1]))
            ser_1 = ser_no[0].split(".")[2]
            ser_2 = ser_no[1].split(".")[2]
            # set attenuation to zero in first attenuator and high in second attenuator
            self.attenuator_modify(ser_1, "all", 0)
            self.attenuator_modify(ser_2, "all", 0)
            kernel_log = []
            # start timer
            test_time = datetime.now()
            test_time = test_time.strftime("%b %d %H:%M:%S")
            print("Test started at ", test_time)
            logging.info("Test started at " + str(test_time))
            self.start_time = test_time
            # get two bssids for roam
            self.final_bssid.extend([self.c1_bssid, self.c2_bssid])
            print("final bssid", self.final_bssid)
            logging.info("final bssid" + str(self.final_bssid))
            print("Calling precleanup.")
            logging.info("Calling precleanup.")
            self.precleanup()
            message = None, None

            # if soft roam is selected set attenuator to zero initiallly
            if self.soft_roam:
                print("make both attenuators set to zero attenuation at the begining")
                logging.info("make both attenuators set to zero attenuation at the begining")
                ser_no = self.attenuator_serial()
                print(ser_no[0], ser_no[1])
                logging.info(str(ser_no[0]) + " , " + str(ser_no[1]))
                ser_1 = ser_no[0].split(".")[2]
                ser_2 = ser_no[1].split(".")[2]
                # set attenuation to zero in first attenuator and high in second attenuator
                self.attenuator_modify(ser_1, "all", 0)
                self.attenuator_modify(ser_2, "all", 0)

            # create clients with respect to bands
            print("start sniffing for initial connection")
            logging.info("start sniffing for initial connection")
            self.start_sniffer(radio_channel=int(self.channel), radio=self.sniff_radio,
                               test_name="roam_11r_" + str(self.option) + "start" + "_",
                               duration=3600)
            if self.band == "twog":
                self.local_realm.reset_port(self.twog_radios)
                self.create_n_clients(sta_prefix="wlan1", num_sta=self.num_sta, dut_ssid=self.ssid_name,
                                      dut_security=self.security, dut_passwd=self.security_key, radio=self.twog_radios,
                                      type="11r")

            if self.band == "fiveg":
                self.local_realm.reset_port(self.fiveg_radios)
                self.create_n_clients(sta_prefix="wlan", num_sta=self.num_sta, dut_ssid=self.ssid_name,
                                      dut_security=self.security, dut_passwd=self.security_key, radio=self.fiveg_radios,
                                      type="11r")
            if self.band == "sixg":
                self.local_realm.reset_port(self.sixg_radios)
                self.create_n_clients(sta_prefix="wlan", num_sta=self.num_sta, dut_ssid=self.ssid_name,
                                      dut_security=self.security, radio=self.sixg_radios,
                                      type="11r-sae-802.1x")

            # check if all stations have ip
            sta_list = self.get_station_list()
            print("checking for IP, station list", sta_list)
            logging.info("checking for IP, station list " + str(sta_list))
            if sta_list == "no response":
                print("no response")
                logging.info("no response")
            else:
                val = self.wait_for_ip(sta_list)

                mac_list = []
                for sta_name in sta_list:
                    sta = sta_name.split(".")[2]  # use name_to_eid
                    # time.sleep(0.5)
                    mac = self.station_data_query(station_name=str(sta), query="mac")
                    mac_list.append(mac)

                print("mac address list of all stations", mac_list)
                logging.info("mac address list of all stations " + str(mac_list))
                self.mac_data = mac_list

                # if self.debug:
                #     print("start debug")
                #     self.start_debug_(mac_list=mac_list)
                # print("check for 30 min")
                # time.sleep(1800)
                print("stop sniff")
                logging.info("stop sniff")
                file_name_ = self.stop_sniffer()
                file_name = "./pcap/" + str(file_name_)
                print("pcap file name", file_name)
                logging.info("pcap file name " +  str(file_name))
                # if self.debug:
                #     print("stop debugger")
                #     self.stop_debug_(mac_list=mac_list)
                #     # time.sleep(40)
                # exit()

                # if all stations got ip check mac address
                if val:
                    print("all stations got ip")
                    logging.info("all stations got ip")
                    print("check if all stations are connected one ap")
                    logging.info("check if all stations are connected one ap")

                    # get bssids of all stations
                    print("get bssids of all stations")
                    logging.info("get bssids of all stations")
                    check = []
                    for sta_name in sta_list:
                        sta = sta_name.split(".")[2]
                        bssid = self.station_data_query(station_name=str(sta), query="ap")
                        print(bssid)
                        logging.info(str(bssid))
                        check.append(bssid)
                    print(check)
                    logging.info(str(check))

                    # check if all element of bssid list has same bssid's
                    print("check if all bssids are same or not")
                    logging.info("check if all bssids are same or not")
                    result = all(element == check[0] for element in check)
                    #  if yes
                    if result:
                        self.create_layer3(side_a_min_rate=1000000, side_a_max_rate=0, side_b_min_rate=1000000,
                                           side_b_max_rate=0,
                                           sta_list=sta_list, traffic_type=self.traffic_type, side_a_min_pdu=1250,
                                           side_b_min_pdu=1250)

                    else:
                        #  if bssid's are not same move try to move all clients to one ap
                        print("try to move all clients to one ap before roam ")
                        logging.info("try to move all clients to one ap before roam ")
                        count1 = check.count(self.c1_bssid.upper())
                        count2 = check.count(self.c2_bssid.upper())
                        checker, new_sta_list, checker2 = None, [], None
                        if count1 > count2:
                            print("station connected mostly to ap1")
                            logging.info("station connected mostly to ap1")
                            checker = self.c2_bssid.upper()
                            checker2 = self.c1_bssid.upper()
                        else:
                            checker = self.c1_bssid.upper()
                            checker2 = self.c2_bssid.upper()
                        index_count = [i for i, x in enumerate(check) if x == checker]
                        print(index_count)
                        logging.info(str(index_count))
                        for i in index_count:
                            new_sta_list.append(sta_list[i])
                        print("new_sta_list", new_sta_list)
                        logging.info("new_sta_list " + str(new_sta_list))

                        for sta_name in new_sta_list:
                            eid = self.name_to_eid(sta_name)
                            print("eid", eid)
                            # sta = sta_name.split(".")[2]  # TODO: use name-to-eid
                            sta = eid[2]
                            print(sta)
                            logging.info(sta)
                            wpa_cmd = "roam " + str(checker2)
                            wifi_cli_cmd_data1 = {
                                "shelf": eid[0],
                                "resource": eid[1],  # TODO: do not hard-code
                                "port": str(sta),
                                "wpa_cli_cmd": 'scan trigger freq 5180 5300'
                            }
                            wifi_cli_cmd_data = {
                                "shelf": eid[0],
                                "resource": eid[1],
                                "port": str(sta),
                                "wpa_cli_cmd": wpa_cmd
                            }
                            print(wifi_cli_cmd_data)
                            logging.info(str(wifi_cli_cmd_data))
                            self.local_realm.json_post("/cli-json/wifi_cli_cmd", wifi_cli_cmd_data1)
                            # TODO:  LANforge sta on same radio will share scan results, so you only need to scan on one STA per
                            # radio, and then sleep should be 5 seconds, then roam every station that needs to roam.
                            # You do not need this sleep and scan for each STA.
                            time.sleep(2)
                            self.local_realm.json_post("/cli-json/wifi_cli_cmd", wifi_cli_cmd_data)

                        self.create_layer3(side_a_min_rate=1000000, side_a_max_rate=0, side_b_min_rate=1000000,
                                           side_b_max_rate=0,
                                           sta_list=sta_list, traffic_type=self.traffic_type, side_a_min_pdu=1250,
                                           side_b_min_pdu=1250)

                    timeout, variable, iterable_var = None, None, None

                    if self.duration_based:
                        timeout = time.time() + 60 * float(self.duration)
                        # iteration_dur = 50000000
                        iterable_var = 50000000
                        variable = -1

                    if self.iteration_based:
                        variable = self.iteration
                        iterable_var = self.iteration
                    # post_bssid = None
                    #  roam iteration loop starts here
                    while variable:
                        print("variable", variable)
                        logging.info("variable " + str(variable))
                        iter, number, ser_1, ser_2 = None, None, None, None
                        if variable != -1:
                            iter = iterable_var - variable
                            variable = variable - 1

                        if variable == -1:
                            # need to write duration iteration logic
                            # iter = iterable_var - iteration_dur
                            if self.duration is not None:
                                if time.time() > timeout:
                                    break
                        time.sleep(1)
                        #  get serial nummber of attenuators from lf
                        ser_no = self.attenuator_serial()
                        print(ser_no[0])
                        logging.info(str(ser_no[0]))
                        ser_1 = ser_no[0].split(".")[2]
                        ser_2 = ser_no[1].split(".")[2]
                        if self.soft_roam:
                            if iter % 2 == 0:
                                print("even set c1 to lowest and c2 to highest attenuation ")
                                logging.info("even set c1 to lowest and c2 to highest attenuation ")
                                number = "even"
                                print("number", number)
                                logging.info("number " + str(number))

                                # set attenuation to zero in first attenuator and high in second attenuator
                                self.attenuator_modify(ser_1, "all", 950)
                                self.attenuator_modify(ser_2, "all", 0)
                            else:
                                print("odd,  c1 is already at  highest and c2 is at  lowest")
                                logging.info("odd,  c1 is already at  highest and c2 is at  lowest")
                                number = "odd"
                                print("number", number)
                                logging.info("number " + str(number))
                        try:
                            # define ro list per iteration
                            row_list = []
                            sta_list = self.get_station_list()
                            print(sta_list)
                            logging.info(str(sta_list))
                            if sta_list == "no response":
                                print("no response")
                                logging.info("no response")
                                pass
                            else:
                                station = self.wait_for_ip(sta_list)
                                time.sleep(20)
                                if self.debug:
                                    print("start debug")
                                    logging.info("start debug")
                                    self.start_debug_(mac_list=mac_list)
                                if station:
                                    print("all stations got ip")
                                    logging.info("all stations got ip")
                                    # get bssid's of all stations connected
                                    bssid_list = []
                                    for sta_name in sta_list:
                                        sta = sta_name.split(".")[2]
                                        bssid = self.station_data_query(station_name=str(sta), query="ap")
                                        bssid_list.append(bssid)
                                    print(bssid_list)
                                    logging.info(str(bssid_list))
                                    pass_fail_list = []
                                    pcap_file_list = []
                                    roam_time1 = []
                                    # packet_loss_lst = []
                                    remark = []
                                    log_file = []

                                    # check if all element of bssid list has same bssid's
                                    result = all(element == bssid_list[0] for element in bssid_list)

                                    if not result:
                                        #  for a iteration if client is not connected to same ap try to connect them
                                        print("giving a try to connect")
                                        logging.info("giving a try to connect")
                                        print("move all clients to one ap")
                                        logging.info("move all clients to one ap")
                                        count3 = bssid_list.count(self.c1_bssid.upper())
                                        count4 = bssid_list.count(self.c2_bssid.upper())
                                        print("count3", count3)
                                        logging.info("count3 " + str(count3))
                                        print("count4", count4)
                                        logging.info("count4 " + str(count4))
                                        checker, new_sta_list, checker2 = None, [], None
                                        if count3 > count4:
                                            print("station connected mostly to ap1")
                                            logging.info("station connected mostly to ap1")
                                            checker = self.c2_bssid.upper()
                                            checker2 = self.c1_bssid.upper()
                                        else:
                                            checker = self.c1_bssid.upper()
                                            checker2 = self.c2_bssid.upper()
                                        index_count = [i for i, x in enumerate(bssid_list) if x == checker]
                                        print(index_count)
                                        logging.info(str(index_count))
                                        for i in index_count:
                                            new_sta_list.append(sta_list[i])
                                        print("new_sta_list", new_sta_list)
                                        logging.info("new_sta_list " + str(new_sta_list))
                                        # for i, x in zip(bssid_list, sta_list):
                                        #     if i == checker:
                                        #         index_count = bssid_list.index(checker)
                                        #         new_sta_list.append(sta_list[index_count])
                                        # print("new_sta_list", new_sta_list)

                                        for sta_name in new_sta_list:
                                            # sta = sta_name.split(".")[2]
                                            eid = self.name_to_eid(sta_name)
                                            sta = eid[2]
                                            print(sta)
                                            logging.info(str(sta))
                                            wpa_cmd = "roam " + str(checker2)

                                            wifi_cli_cmd_data1 = {
                                                "shelf": eid[0],
                                                "resource": eid[1],
                                                "port": str(sta),
                                                "wpa_cli_cmd": 'scan trigger freq 5180 5300'
                                            }
                                            wifi_cli_cmd_data = {
                                                "shelf": eid[0],
                                                "resource": eid[1],
                                                "port": str(sta),
                                                "wpa_cli_cmd": wpa_cmd
                                            }
                                            print(wifi_cli_cmd_data)
                                            logging.info(str(wifi_cli_cmd_data))
                                            self.local_realm.json_post("/cli-json/wifi_cli_cmd", wifi_cli_cmd_data1)
                                            time.sleep(2)
                                            self.local_realm.json_post("/cli-json/wifi_cli_cmd", wifi_cli_cmd_data)

                                    # check bssid before
                                    before_bssid = []
                                    for sta_name in sta_list:
                                        sta = sta_name.split(".")[2]
                                        before_bss = self.station_data_query(station_name=str(sta), query="ap")
                                        print(before_bss)
                                        logging.info(str(before_bss))
                                        before_bssid.append(before_bss)
                                    print("bssid 1", before_bssid)
                                    logging.info("bssid 1 " + str(before_bssid))

                                    if before_bssid[0] == str(self.c1_bssid.upper()):
                                        post_bssid = self.c2_bssid.upper()
                                    else:
                                        post_bssid = self.c1_bssid.upper()
                                    print("station are connected to post bssid", post_bssid)
                                    logging.info("station are connected to post bssid " + str(post_bssid))
                                    result1 = all(element == before_bssid[0] for element in before_bssid)

                                    if result1:
                                        print("All stations connected to one ap")
                                        logging.info("All stations connected to one ap")
                                        for i in before_bssid:
                                            local_row_list = [str(iter)]
                                            local_row_list.append(i)
                                            print(local_row_list)
                                            logging.info(str(local_row_list))
                                            row_list.append(local_row_list)
                                        print(row_list)
                                        logging.info(str(row_list))
                                        #  if all bssid are equal then do check to which ap it is connected
                                        formated_bssid = before_bssid[0].lower()
                                        station_before = ""
                                        if formated_bssid == self.c1_bssid:
                                            print("station connected to chamber1 ap")
                                            logging.info("station connected to chamber1 ap")
                                            station_before = formated_bssid
                                        elif formated_bssid == self.c2_bssid:
                                            print("station connected to chamber 2 ap")
                                            logging.info("station connected to chamber 2 ap")
                                            station_before = formated_bssid
                                        print(station_before)
                                        logging.info(str(station_before))
                                        # after checking all conditions start roam and start snifffer
                                        print("starting snifer")
                                        logging.info("starting snifer")
                                        self.start_sniffer(radio_channel=int(self.channel), radio=self.sniff_radio,
                                                           test_name="roam_11r_" + str(self.option) + "_iteration_" + str(
                                                               iter) + "_",
                                                           duration=3600)
                                        if self.soft_roam:
                                            ser_num = None
                                            ser_num2 = None
                                            if number == "even":
                                                ser_num = ser_1
                                                ser_num2 = ser_2
                                                print("even", ser_num)
                                                logging.info("even " + str(ser_num))
                                            elif number == "odd":
                                                ser_num = ser_2
                                                ser_num2 = ser_1
                                                print("odd", ser_num)
                                                logging.info("odd " +  str(ser_num))
                                            # logic to decrease c2 attenuation till 10 db using 1dbm steps
                                            status = None
                                            print("checking attenuation")
                                            logging.info("checking attenuation")
                                            print("ser num", ser_num)
                                            logging.info("ser num " + str(ser_num))
                                            for atten_val2 in range(900, 0, -50):
                                                # print("hi")
                                                self.attenuator_modify(int(ser_num), "all", atten_val2)
                                                # TODO:  You are changing in 1db increments.  So, sleep for only 4 seconds
                                                # should be enough.
                                                print("wait for 4  secs")
                                                logging.info("wait for 4  secs")
                                                time.sleep(4)
                                                #  query bssid's of all stations
                                                bssid_check = []
                                                for sta_name in sta_list:
                                                    sta = sta_name.split(".")[2]
                                                    bssid = self.station_data_query(station_name=str(sta), query="ap")
                                                    if bssid == "NA":
                                                        time.sleep(10)
                                                    bssid_check.append(bssid)
                                                print(bssid_check)
                                                logging.info(str(bssid_check))

                                                # check if all are equal
                                                resulta = all(element == bssid_check[0] for element in bssid_check)
                                                if resulta:
                                                    station_after = bssid_check[0].lower()
                                                    if station_after == "N/A" or station_after == "na":
                                                        status = "station did not roamed"
                                                        print("station did not roamed")
                                                        logging.info("station did not roamed")
                                                        continue
                                                    if station_after == station_before:
                                                        status = "station did not roamed"
                                                        print("station did not roamed")
                                                        logging.info("station did not roamed")
                                                        continue
                                                    elif station_after != station_before:
                                                        print("client performed roam")
                                                        logging.info("client performed roam")
                                                        break

                                            if status == "station did not roamed":
                                                # set c1 to high
                                                for atten_val1 in (range(0, 950, 50)):
                                                    print(atten_val1)
                                                    logging.info(str(atten_val1))
                                                    self.attenuator_modify(int(ser_num2), "all", atten_val1)
                                                    # TODO:  You are changing in 1db increments.  So, sleep for only 4 seconds
                                                    # should be enough.
                                                    # TODO:  Add attenuation step to logs to make it more obvious what script is doing.
                                                    print("wait for 4  secs")
                                                    logging.info("wait for 4  secs")
                                                    time.sleep(4)
                                                    bssid_check2 = []
                                                    for sta_name in sta_list:
                                                        sta = sta_name.split(".")[2]
                                                        bssid = self.station_data_query(station_name=str(sta),
                                                                                        query="ap")
                                                        if bssid == "NA":
                                                            time.sleep(10)
                                                        bssid_check2.append(bssid)
                                                    print(bssid_check2)
                                                    logging.info(str(bssid_check2))
                                                    # check if all are equal
                                                    result = all(element == bssid_check2[0] for element in bssid_check2)
                                                    if result:
                                                        station_after = bssid_check2[0].lower()
                                                        if station_after == "N/A" or station_after == "na":
                                                            status = "station did not roamed"
                                                            print("station did not roamed")
                                                            logging.info("station did not roamed")
                                                            continue
                                                        if station_after == station_before:
                                                            status = "station did not roamed"
                                                            print("station did not roamed")
                                                            logging.info("station did not roamed")
                                                            continue
                                                        else:
                                                            print('station roamed')
                                                            logging.info('station roamed')
                                                            break


                                        else:
                                            if station_before == self.final_bssid[0]:
                                                print("connected stations bssid is same to bssid list first element")
                                                logging.info("connected stations bssid is same to bssid list first element")
                                                for sta_name in sta_list:
                                                    sta = sta_name.split(".")[2]
                                                    print(sta)
                                                    logging.info(str(sta))
                                                    wpa_cmd = ""
                                                    if self.option == "ota":
                                                        wpa_cmd = "roam " + str(self.final_bssid[1])
                                                    if self.option == "otds":
                                                        wpa_cmd = "ft_ds " + str(self.final_bssid[1])
                                                    # wpa_cmd = "roam " + str(self.final_bssid[1])
                                                    wifi_cli_cmd_data1 = {
                                                        "shelf": 1,
                                                        "resource": 1,
                                                        "port": str(sta),
                                                        "wpa_cli_cmd": 'scan trigger freq 5180 5300'
                                                    }
                                                    wifi_cli_cmd_data = {
                                                        "shelf": 1,
                                                        "resource": 1,
                                                        "port": str(sta),
                                                        "wpa_cli_cmd": wpa_cmd
                                                    }
                                                    print(wifi_cli_cmd_data)
                                                    logging.info(str(wifi_cli_cmd_data))
                                                    self.local_realm.json_post("/cli-json/wifi_cli_cmd", wifi_cli_cmd_data1)
                                                    # TODO:  See note in similar code above about only needing to scan once per radio
                                                    time.sleep(2)
                                                    self.local_realm.json_post("/cli-json/wifi_cli_cmd", wifi_cli_cmd_data)
                                                    time.sleep(20)

                                            else:
                                                print("connected stations bssid is same to bssid list second  element")
                                                logging.info("connected stations bssid is same to bssid list second  element")
                                                for sta_name in sta_list:
                                                    sta = sta_name.split(".")[2]
                                                    wifi_cmd = ""
                                                    if self.option == "ota":
                                                        wifi_cmd = "roam " + str(self.final_bssid[0])
                                                    if self.option == "otds":
                                                        wifi_cmd = "ft_ds " + str(self.final_bssid[0])
                                                    print(sta)
                                                    logging.info(str(sta))
                                                    wifi_cli_cmd_data1 = {
                                                        "shelf": 1,
                                                        "resource": 1,
                                                        "port": str(sta),
                                                        "wpa_cli_cmd": 'scan trigger freq 5180 5300'
                                                    }
                                                    wifi_cli_cmd_data = {
                                                        "shelf": 1,
                                                        "resource": 1,
                                                        "port": str(sta),
                                                        "wpa_cli_cmd": wifi_cmd
                                                    }
                                                    print(wifi_cli_cmd_data)
                                                    logging.info(str(wifi_cli_cmd_data))
                                                    self.local_realm.json_post("/cli-json/wifi_cli_cmd", wifi_cli_cmd_data1)
                                                    # TODO:  See note in similar code above about only needing to scan once per radio
                                                    time.sleep(2)
                                                    self.local_realm.json_post("/cli-json/wifi_cli_cmd", wifi_cli_cmd_data)
                                                    time.sleep(20)

                                        # krnel logs
                                        kernel = self.journal_ctl_logs(file=str(iter))
                                        for i in kernel:
                                            kernel_log.append(i)
                                        # stop sniff and attach data
                                        time.sleep(30)
                                        print("stop sniff")
                                        logging.info("stop sniff")
                                        file_name_ = self.stop_sniffer()
                                        file_name = "./pcap/" + str(file_name_)
                                        print("pcap file name", file_name)
                                        logging.info("pcap file name " + str(file_name))
                                        if self.debug:
                                            print("stop debugger")
                                            logging.info("stop debugger")
                                            self.stop_debug_(mac_list=mac_list)
                                            time.sleep(40)
                                        else:
                                            print("debug is  disabled")
                                            logging.info("debug is  disabled")

                                        self.wait_for_ip(sta_list)
                                        bssid_list_1 = []
                                        for sta_name in sta_list:
                                            sta = sta_name.split(".")[2]
                                            bssid = self.station_data_query(station_name=str(sta), query="ap")
                                            bssid_list_1.append(bssid)
                                        print(bssid_list_1)
                                        logging.info(str(bssid_list_1))
                                        for i, x in zip(row_list, bssid_list_1):
                                            i.append(x)
                                        print("row list", row_list)
                                        logging.info("row list " + str(row_list))
                                        time.sleep(60)
                                        trace = self.get_file_name(client=self.num_sta)
                                        log_file.append(trace)
                                        # check if all are equal
                                        all(element == bssid_list_1[0] for element in bssid_list_1)

                                        res = ""
                                        station_before_ = before_bssid
                                        print("station before", station_before_)
                                        logging.info("station before " + str(station_before_))
                                        # for each mac address query data from pcap
                                        for i, x in zip(mac_list, range(len(station_before_))):
                                            print("mac ", i)
                                            logging.info("mac " + str(i))
                                            print(x)
                                            print(bssid_list_1)
                                            logging.info(str(bssid_list_1))
                                            query_action_frame_time, auth_time = None, None
                                            station_after = bssid_list_1[x]
                                            print("station_after", station_after)
                                            logging.info("station_after " + str(station_after))
                                            if station_after == station_before_[x] or station_after == "na":
                                                print("station did not roamed")
                                                logging.info("station did not roamed")
                                                res = "FAIL"
                                            elif station_after != station_before_[x]:
                                                print("client performed roam")
                                                logging.info("client performed roam")
                                                res = "PASS"
                                            if res == "FAIL":
                                                res = "FAIL"
                                            if res == "PASS":
                                                query_reasso_response = self.get_wlan_mgt_status(file_name=file_name,
                                                                                                 filter="(wlan.fc.type_subtype eq 3 && wlan.fixed.status_code == 0x0000 && wlan.tag.number == 55) && (wlan.da == %s)" % (
                                                                                                     str(i)))
                                                print(query_reasso_response)
                                                logging.info(str(query_reasso_response))
                                                if len(query_reasso_response) != 0 and query_reasso_response != "empty":
                                                    if query_reasso_response == "Successful":
                                                        print("re-association status is successful")
                                                        logging.info("re-association status is successful")
                                                        reasso_t = self.pcap_obj.read_time(pcap_file=str(file_name),
                                                                                           filter="(wlan.fc.type_subtype eq 3 && wlan.fixed.status_code == 0x0000 && wlan.tag.number == 55) && (wlan.da == %s)" % (
                                                                                               str(i)))
                                                        print("reassociation time is", reasso_t)
                                                        logging.info("reassociation time is " + str(reasso_t))
                                                        if self.option == "otds":
                                                            print("check for action frame")
                                                            logging.info("check for action frame")

                                                            # action frame check
                                                            query_action_frame = self.pcap_obj.check_frame_present(
                                                                pcap_file=str(file_name),
                                                                filter="(wlan.fixed.category_code == 6)  && (wlan.sa == %s)" % (
                                                                    str(i)))
                                                            if len(query_action_frame) != 0 and query_action_frame != "empty":
                                                                print("Action frame  is present")
                                                                logging.info("Action frame is present")
                                                                query_action_frame_time = self.pcap_obj.read_time(
                                                                    pcap_file=str(file_name),
                                                                    filter="(wlan.fixed.category_code == 6)  && (wlan.sa == %s)" % (
                                                                        str(i)))
                                                                print("action frame  time is", query_action_frame_time)
                                                                logging.info("action frame) time is " + str(reasso_t))
                                                            else:
                                                                roam_time1.append("No Action frame")
                                                                pass_fail_list.append("FAIL")
                                                                pcap_file_list.append(str(file_name))
                                                                remark.append("No Action Frame")
                                                                print("row list", row_list)
                                                                logging.info("row list " + str(row_list))




                                                        else:
                                                            print("check for auth frame")
                                                            logging.info("check for auth frame")
                                                            query_auth_response = self.pcap_obj.get_wlan_mgt_status_code(
                                                                pcap_file=str(file_name),
                                                                filter="(wlan.fixed.auth.alg == 2 && wlan.fixed.status_code == 0x0000 && wlan.fixed.auth_seq == 0x0001) && (wlan.sa == %s)" % (
                                                                    str(i)))
                                                            if len(query_auth_response) != 0 and query_auth_response != "empty":
                                                                if query_auth_response == "Successful":
                                                                    print("authentication request is present")
                                                                    logging.info("authentication request is present")
                                                                    auth_time = self.pcap_obj.read_time(
                                                                        pcap_file=str(file_name),
                                                                        filter="(wlan.fixed.auth.alg == 2 && wlan.fixed.status_code == 0x0000 && wlan.fixed.auth_seq == 0x0001)  && (wlan.sa == %s)" % (
                                                                            str(i)))
                                                                    print("auth time is", auth_time)
                                                                    logging.info("auth time is " + str(auth_time))
                                                                else:
                                                                    roam_time1.append('Auth Fail')
                                                                    pass_fail_list.append("FAIL")
                                                                    pcap_file_list.append(str(file_name))
                                                                    remark.append(" auth failure")
                                                            else:
                                                                roam_time1.append("No Auth frame")
                                                                pass_fail_list.append("FAIL")
                                                                pcap_file_list.append(str(file_name))
                                                                remark.append("No Auth frame")
                                                                print("row list", row_list)
                                                                logging.info("row list " + str(row_list))
                                                        # roam_time = None
                                                        if self.option == "otds":
                                                            roam_time = reasso_t - query_action_frame_time
                                                        else:
                                                            roam_time = reasso_t - auth_time
                                                        print("roam time ms", roam_time)
                                                        logging.info("roam time ms " + str(roam_time))
                                                        roam_time1.append(roam_time)
                                                        if self.option == "ota":

                                                            if roam_time < 50:
                                                                pass_fail_list.append("PASS")
                                                                pcap_file_list.append(str(file_name))
                                                                remark.append("Passed all criteria")

                                                            else:
                                                                pass_fail_list.append("FAIL")
                                                                pcap_file_list.append(str(file_name))
                                                                remark.append("Roam time is greater then 50 ms")
                                                        else:
                                                            pass_fail_list.append("PASS")
                                                            pcap_file_list.append(str(file_name))
                                                            remark.append("Passed all criteria")


                                                    else:
                                                        roam_time1.append('Reassociation Fail')
                                                        pass_fail_list.append("FAIL")
                                                        pcap_file_list.append(str(file_name))
                                                        remark.append("Reassociation failure")
                                                        print("pcap_file name for fail instance of iteration value ")
                                                        logging.info("pcap_file name for fail instance of iteration value ")

                                                else:
                                                    roam_time1.append("No Reassociation")
                                                    pass_fail_list.append("FAIL")
                                                    pcap_file_list.append(str(file_name))
                                                    remark.append("No Reasso response")
                                                    print("row list", row_list)
                                                    logging.info("row list " + str(row_list))
                                            else:
                                                query_reasso_response = self.get_wlan_mgt_status(file_name=file_name,
                                                                                                 filter="(wlan.fc.type_subtype eq 3 && wlan.fixed.status_code == 0x0000 && wlan.tag.number == 55) && (wlan.da == %s)" % (
                                                                                                     str(i)))
                                                print(query_reasso_response)
                                                logging.info(str(query_reasso_response))
                                                if len(query_reasso_response) != 0 and query_reasso_response != 'empty':
                                                    if query_reasso_response == "Successful":
                                                        print("re-association status is successful")
                                                        logging.info("re-association status is successful")
                                                        reasso_t = self.pcap_obj.read_time(pcap_file=str(file_name),
                                                                                           filter="(wlan.fc.type_subtype eq 3 && wlan.fixed.status_code == 0x0000 && wlan.tag.number == 55) && (wlan.da == %s)" % (
                                                                                               str(i)))
                                                        print("reassociation time is", reasso_t)
                                                        logging.info("reassociation time is " + str(reasso_t))
                                                        if self.option == "otds":
                                                            print("check for action frame")
                                                            logging.info("check for action frame")

                                                            # action frame check
                                                            query_action_frame = self.pcap_obj.check_frame_present(
                                                                pcap_file=str(file_name),
                                                                filter="(wlan.fixed.category_code == 6)  && (wlan.sa == %s)" % (
                                                                    str(i)))
                                                            if len(query_action_frame) != 0 and query_action_frame != "empty":
                                                                print("Action frame  is present")
                                                                logging.info("Action frame is present")
                                                                query_action_frame_time = self.pcap_obj.read_time(
                                                                    pcap_file=str(file_name),
                                                                    filter="(wlan.fixed.category_code == 6)  && (wlan.sa == %s)" % (
                                                                        str(i)))
                                                                print("action frame  time is", query_action_frame_time)
                                                                logging.info("action frame) time is " + str(reasso_t))
                                                            else:
                                                                roam_time1.append("No Action frame")
                                                                pass_fail_list.append("FAIL")
                                                                pcap_file_list.append(str(file_name))
                                                                remark.append("bssid miNo Action Frame")
                                                                print("row list", row_list)
                                                                logging.info("row list " + str(row_list))
                                                        else:
                                                            print("check for auth frame")
                                                            logging.info("check for auth frame")
                                                            query_auth_response = self.pcap_obj.get_wlan_mgt_status_code(
                                                                pcap_file=str(file_name),
                                                                filter="(wlan.fixed.auth.alg == 2 && wlan.fixed.status_code == 0x0000 && wlan.fixed.auth_seq == 0x0001) && (wlan.sa == %s)" % (
                                                                    str(i)))
                                                            if len(query_auth_response) != 0 and query_auth_response != "empty":
                                                                if query_auth_response == "Successful":
                                                                    print("authentication request is present")
                                                                    logging.info("authentication request is present")
                                                                    auth_time = self.pcap_obj.read_time(
                                                                        pcap_file=str(file_name),
                                                                        filter="(wlan.fixed.auth.alg == 2 && wlan.fixed.status_code == 0x0000 && wlan.fixed.auth_seq == 0x0001)  && (wlan.sa == %s)" % (
                                                                            str(i)))
                                                                    print("auth time is", auth_time)
                                                                    logging.info("auth time is " + str(auth_time))
                                                                else:
                                                                    roam_time1.append('Auth Fail')
                                                                    pass_fail_list.append("FAIL")
                                                                    pcap_file_list.append(str(file_name))
                                                                    remark.append("bssid mismatch  auth failure")
                                                            else:
                                                                roam_time1.append("No Auth frame")
                                                                pass_fail_list.append("FAIL")
                                                                pcap_file_list.append(str(file_name))
                                                                remark.append("bssid mismatched No Auth frame")
                                                                print("row list", row_list)
                                                                logging.info("row list " + str(row_list))
                                                        # roam_time = None
                                                        if self.option == "otds":
                                                            roam_time = reasso_t - query_action_frame_time
                                                        else:
                                                            roam_time = reasso_t - auth_time
                                                        print("roam time ms", roam_time)
                                                        logging.info("roam time ms " + str(roam_time))
                                                        roam_time1.append(roam_time)
                                                        if self.option == "ota":

                                                            if roam_time < 50:
                                                                pass_fail_list.append("FAIL")
                                                                pcap_file_list.append(str(file_name))
                                                                remark.append(
                                                                    "(bssid mismatched)Client disconnected after roaming")
                                                            else:
                                                                pass_fail_list.append("FAIL")
                                                                pcap_file_list.append(str(file_name))
                                                                remark.append(
                                                                    "(bssid mis matched)Roam time is greater then 50 ms,")
                                                        else:
                                                            pass_fail_list.append("FAIL")
                                                            pcap_file_list.append(str(file_name))
                                                            remark.append("bssid mismatched")
                                                    else:
                                                        roam_time1.append('Reassociation Fail')
                                                        pass_fail_list.append("FAIL")
                                                        pcap_file_list.append(str(file_name))
                                                        remark.append("bssid mismatched  Reassociation failure")
                                                else:
                                                    roam_time1.append("No Reassociation")
                                                    pass_fail_list.append("FAIL")
                                                    pcap_file_list.append(str(file_name))
                                                    remark.append("bssid mismatched , No Reasso response")

                                                    print("row list", row_list)
                                                    logging.info("row list " + str(row_list))

                                        for i, x in zip(row_list, roam_time1):
                                            i.append(x)
                                        print("row list", row_list)
                                        logging.info("row list " + str(row_list))
                                        # for i, x in zip(row_list, packet_loss_lst):
                                        #     i.append(x)
                                        for i, x in zip(row_list, pass_fail_list):
                                            i.append(x)
                                        print("row list", row_list)
                                        logging.info("row list " + str(row_list))
                                        for i, x in zip(row_list, pcap_file_list):
                                            i.append(x)

                                        print("log file", log_file)
                                        logging.info("log file " + str(log_file))
                                        my_unnested_list = list(chain(*log_file))
                                        print(my_unnested_list)
                                        logging.info(str(my_unnested_list))
                                        for i, x in zip(row_list, my_unnested_list):
                                            i.append(x)
                                        print("row list", row_list)
                                        for i, x in zip(row_list, remark):
                                            i.append(x)
                                        print("row list", row_list)
                                        logging.info("row list " + str(row_list))
                                        for i, x in zip(file_n, row_list):
                                            self.lf_csv_obj.open_csv_append(fields=x, name=i)


                                    else:

                                        message = "all stations are not connected to same ap for iteration " + str(iter)
                                        print("all stations are not connected to same ap")
                                        logging.info("all stations are not connected to same ap")
                                        print("starting snifer")
                                        logging.info("starting snifer")
                                        self.start_sniffer(radio_channel=int(self.channel), radio=self.sniff_radio,
                                                           test_name="roam_11r_" + str(self.option) + "_iteration_" + str(
                                                               iter) + "_",
                                                           duration=3600)
                                        print("stop sniff")
                                        logging.info("stop sniff")
                                        self.stop_sniffer()
                                        kernel = self.journal_ctl_logs(file=str(iter))
                                        for i in kernel:
                                            kernel_log.append(i)
                                        bssid_list2 = []
                                        for sta_name in sta_list:
                                            # local_row_list = [0, "68"]
                                            local_row_list = [str(iter)]
                                            sta = sta_name.split(".")[2]
                                            before_bssid_ = self.station_data_query(station_name=str(sta), query="ap")
                                            print(before_bssid_)
                                            logging.info(str(before_bssid_))
                                            bssid_list2.append(before_bssid_)
                                            local_row_list.append(before_bssid_)
                                            print(local_row_list)
                                            logging.info(str(local_row_list))
                                            row_list.append(local_row_list)
                                        print(row_list)
                                        logging.info(str(row_list))
                                        for i, x in zip(row_list, bssid_list2):
                                            i.append(x)
                                        print("row list", row_list)
                                        logging.info("row list " + str(row_list))
                                        for i in row_list:
                                            i.append("No Roam Time")
                                        print("row list", row_list)
                                        logging.info("row list " + str(row_list))
                                        for a in row_list:
                                            a.append("FAIL")
                                        print("row list", row_list)
                                        logging.info("row list " + str(row_list))
                                        # pcap
                                        for i in row_list:
                                            i.append("N/A")
                                        print("row list", row_list)
                                        logging.info("row list " + str(row_list))
                                        if self.debug:
                                            print("stop debugger")
                                            logging.info("stop debugger")
                                            self.stop_debug_(mac_list=mac_list)

                                        else:
                                            print("debug is  disabled")
                                            logging.info("debug is  disabled")

                                        time.sleep(60)
                                        trace = self.get_file_name(client=self.num_sta)
                                        log_file.append(trace)
                                        print("log file", log_file)
                                        logging.info("log file " + str(log_file))
                                        my_unnested_list = list(chain(*log_file))
                                        print(my_unnested_list)
                                        logging.info(str(my_unnested_list))
                                        for i, x in zip(row_list, my_unnested_list):
                                            i.append(x)
                                        print("row list", row_list)
                                        logging.info("row list " + str(row_list))
                                        for i in row_list:
                                            i.append("no roam performed all stations are not connected to same ap")
                                        print("row list", row_list)
                                        logging.info("row list " + str(row_list))
                                        for i, x in zip(file_n, row_list):
                                            self.lf_csv_obj.open_csv_append(fields=x, name=i)

                                else:
                                    message = "station's failed to get ip  after the test start"
                                    print("station's failed to get ip after test starts")
                                    logging.info("station's failed to get ip after test starts")
                                if self.duration_based:
                                    if time.time() > timeout:
                                        break
                        except Exception as e:
                            # print(e)
                            logging.warning(str(e))
                            pass

                    else:
                        message = "station's failed to get ip  at the begining"
                        print("station's failed to get associate at the begining")
                        logging.info("station's failed to get associate at the begining")
                else:
                    print("stations failed to get ip")
                    logging.info("stations failed to get ip")

            test_end = datetime.now()
            test_end = test_end.strftime("%b %d %H:%M:%S")
            print("Test ended at ", test_end)
            logging.info("Test ended at " + str(test_end))
            self.end_time = test_end
            s1 = test_time
            s2 = test_end  # for example
            FMT = '%b %d %H:%M:%S'
            self.test_duration = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
            return kernel_log, message
        except Exception as e:
            logging.warning(str(e))

    # graph function
    def generate_client_pass_fail_graph(self, csv_list=None):
        try:
            print("csv_list", csv_list)
            logging.info("csv_list " + str(csv_list))
            x_axis_category = []
            for i in range(self.num_sta):
                x_axis_category.append(i + 1)
            print(x_axis_category)
            logging.info(str(x_axis_category))
            pass_list = []
            fail_list = []
            dataset = []
            for i in csv_list:
                print("i", i)
                logging.info("i, " + i)
                lf_csv_obj = lf_csv.lf_csv()
                h = lf_csv_obj.read_csv(file_name=i, column="PASS/FAIL")
                count = h.count("PASS")
                print(count)
                logging.info(str(count))
                count_ = h.count("FAIL")
                print(count_)
                logging.info(str(count_))
                pass_list.append(count)
                fail_list.append(count_)
            dataset.append(pass_list)
            dataset.append(fail_list)
            print(dataset)
            logging.info(str(dataset))

            # it will contain per station pass and fail number eg [[9, 7], [3, 4]] here 9, 7 are pass number for clients  3 and 4 are fail number
            # dataset = [[9, 7 , 4], [3, 4,9]]
            graph = lf_graph.lf_bar_graph(_data_set=dataset, _xaxis_name="Stations = " + str(self.num_sta),
                                          _yaxis_name="Total iterations = " + str(self.iteration),
                                          _xaxis_categories=x_axis_category,
                                          _label=["Pass", "Fail"], _xticks_font=8,
                                          _graph_image_name="11r roam client per iteration graph",
                                          _color=['forestgreen', 'darkorange', 'blueviolet'], _color_edge='black',
                                          _figsize=(12, 4),
                                          _grp_title="client per iteration graph", _xaxis_step=1,
                                          _show_bar_value=True,
                                          _text_font=6, _text_rotation=60,
                                          _legend_loc="upper right",
                                          _legend_box=(1, 1.15),
                                          _enable_csv=True
                                          )
            graph_png = graph.build_bar_graph()
            print("graph name {}".format(graph_png))
            logging.info(str("graph name {}".format(graph_png)))
            return graph_png
        except Exception as e:
            logging.info(str(e))
            print(str(e))

    # report generation function
    def generate_report(self, csv_list, kernel_lst, current_path=None):
        try:
            option, band_ , station_, iteration__= None, None, None, None
            if self.option == 'ota':
                option = "OTA"
            else:
                option = "OTD"
            if self.band == "fiveg":
                band_ = "5G"
            elif self.band == "twog":
                band_ = "2G"
            elif self.band == "sixg":
                band_ = "6G"
            if int(self.num_sta) > 1:
                station_ = "Multi"
            else:
                station_ = "Single"

            if int(self.iteration) > 1:
                iteration__ = "Multi"
            else:
                iteration__ = "Single"
            if self.soft_roam:
                dir_name = "Soft_Roam_Test_" + str(band_) + "_" + str(option) + "_" + str(station_) + "Client_" + str(iteration__) + "_Iteration"
                out_html = "soft_roam.html"
                pdf_name = "soft_roam_test.pdf"
            else:
                dir_name = "Hard_Roam_Test_" + str(band_) + "_" + str(option) + "_" + str(station_) + "Client_" + str(iteration__) + "_Iteration"
                out_html = "hard_roam.html"
                pdf_name = "Hard_roam_test.pdf"
            report = lf_report_pdf.lf_report(_path="", _results_dir_name=dir_name, _output_html=out_html,
                                             _output_pdf=pdf_name)
            if current_path is not None:
                report.current_path = os.path.dirname(os.path.abspath(current_path))
            report_path = report.get_report_path()
            report.build_x_directory(directory_name="csv_data")
            report.build_x_directory(directory_name="kernel_log")
            for i in kernel_lst:
                report.move_data(directory="kernel_log", _file_name=str(i))

            date = str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
            test_setup_info = {
                "DUT Name": self.dut_name,
                "SSID": self.ssid_name,
                "Test Duration": self.test_duration,
            }
            if self.soft_roam:
                report.set_title("SOFT ROAM (11r) TEST")
            else:
                report.set_title("HARD ROAM (11r) TEST")
            report.set_date(date)
            report.build_banner()
            report.set_table_title("Test Setup Information")
            report.build_table_title()

            report.test_setup_table(value="Device under test", test_setup_data=test_setup_info)

            report.set_obj_html("Objective", "Roaming (11r) Test is designed to test the performance of the "
                                             "Access Point. The goal is to check whether the 11r configuration of AP for  all the "
                                + str(self.num_sta) +
                                " clients are working as expected or not")
            report.build_objective()

            report.set_obj_html("Client per iteration Graph",
                                "The below graph provides information about out of total iterations how many times each client got Pass or Fail")
            report.build_objective()

            graph = self.generate_client_pass_fail_graph(csv_list=csv_list)
            report.set_graph_image(graph)
            report.set_csv_filename(graph)
            report.move_csv_file()
            report.move_graph_image()
            report.build_graph()
            for i in csv_list:
                report.move_data(directory="csv_data", _file_name=str(i))

            report.move_data(directory_name="pcap")

            for i, x in zip(range(self.num_sta), csv_list):
                # report.set_table_title("Client information  " + str(i))
                # report.build_table_title()
                report.set_obj_html("Client " + str(i + 1) + "  Information", "This Table gives detailed information  "
                                                                              "of client " + str(
                    i + 1) + " like the bssid it was before roam," +
                                    " bssid it was after roam, " +
                                    "roam time, capture file name and ra_trace file name along with remarks ")

                report.build_objective()
                lf_csv_obj = lf_csv.lf_csv()
                y = lf_csv_obj.read_csv(file_name=str(report_path) + "/csv_data/" + str(x), column="Iterations")
                z = lf_csv_obj.read_csv(file_name=str(report_path) + "/csv_data/" + str(x), column="bssid1")
                u = lf_csv_obj.read_csv(file_name=str(report_path) + "/csv_data/" + str(x), column="bssid2")
                t = lf_csv_obj.read_csv(file_name=str(report_path) + "/csv_data/" + str(x), column="Roam Time(ms)")
                # l = lf_csv_obj.read_csv(file_name=str(report_path) + "/csv_data/" + str(x), column="Packet loss")
                h = lf_csv_obj.read_csv(file_name=str(report_path) + "/csv_data/" + str(x), column="PASS/FAIL")
                p = lf_csv_obj.read_csv(file_name=str(report_path) + "/csv_data/" + str(x), column="Pcap file Name")
                lf = lf_csv_obj.read_csv(file_name=str(report_path) + "/csv_data/" + str(x), column="Log File")
                r = lf_csv_obj.read_csv(file_name=str(report_path) + "/csv_data/" + str(x), column="Remark")
                table = {
                    "iterations": y,
                    "Bssid before": z,
                    "Bssid After": u,
                    "Roam Time(ms)": t,
                    "PASS/FAIL": h,
                    "pcap file name": p,
                    "Log File": lf,
                    "Remark": r
                }
                test_setup = pd.DataFrame(table)
                report.set_table_dataframe(test_setup)
                report.build_table()

            if self.option == 'ota':
                testname = 'over the air'
            else:
                testname = 'over the ds'
            test_input_infor = {
                "LANforge ip": self.lanforge_ip,
                "LANforge port": self.lanforge_port,
                "test start time": self.start_time,
                "test end time": self.end_time,
                "Bands": self.band,
                "Upstream": self.upstream,
                "Stations": self.num_sta,
                "iterations": self.iteration,
                "SSID": self.ssid_name,
                "Security": self.security,
                "Client mac": self.mac_data,
                'Test': testname,
                "Contact": "support@candelatech.com"
            }
            report.set_table_title("Test basic Information")
            report.build_table_title()
            report.test_setup_table(value="Information", test_setup_data=test_input_infor)

            report.build_footer()
            report.write_html()
            report.write_pdf_with_timestamp(_page_size='A4', _orientation='Landscape')
            return report_path
        except Exception as e:
            print(str(e))
            logging.info(str(e))


def main():
    parser = argparse.ArgumentParser(
        prog='lf_hard_roam_test.py',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            lf_hard_roam_test.py
            ''',
        description='''\
            lf_hard_roam_test.py - under development
            '''
    )
    args = parser.parse_args()

    obj = HardRoam(lanforge_ip="192.168.100.131",
                   lanforge_port=8080,
                   lanforge_ssh_port=22,
                   c1_bssid="68:7d:b4:5f:5c:3a",
                   c2_bssid="14:16:9d:53:58:ca",
                   fiveg_radio="1.1.wiphy1",
                   twog_radio=None,
                   sixg_radio=None,
                   band="fiveg",
                   sniff_radio="wiphy2",
                   num_sta=1,
                   security="wpa2",
                   security_key="something",
                   ssid="ssid_5g",
                   upstream="eth2",
                   duration=None,
                   iteration=1,
                   channel=40,
                   option="ota",
                   duration_based=False,
                   iteration_based=True,
                   dut_name=["AP687D.B45C.1D1C", "AP2C57.4152.385C"],
                   traffic_type="lf_udp",
                   scheme="ssh",
                   dest="localhost",
                   user="admin",
                   passwd="Cisco123",
                   prompt="WLC2",
                   series_cc="9800",
                   ap="AP687D.B45C.1D1C",
                   port="8888",
                   band_cc="5g",
                   timeout="10",
                   identity="testuser",
                   ttls_pass="testpasswd",
                   soft_roam=True
                   )
    x = os.getcwd()
    print(x)
    file = obj.generate_csv()
    kernel, message = obj.run(file_n=file)
    report_dir_name = obj.generate_report(csv_list=file, kernel_lst=kernel, current_path=str(x) + "/tests")
    print(report_dir_name)

    # file = obj.generate_csv()
    # obj.run(file_n=file)
    # obj.generate_report(csv_list=file)
    # obj.generate_client_pass_fail_graph()
    # obj.controller_class()
    # obj.stop_debug_()
    # obj.get_file_name()
    # obj.delete_trace_file()
    # lst = obj.journal_ctl_logs(file="nik")
    # file = []
    # obj.generate_report(csv_list=file, kernel_lst=lst)
    # obj.get_file_name(client=1)


if __name__ == '__main__':
    main()
