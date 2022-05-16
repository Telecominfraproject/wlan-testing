#########################################################################################################
# Used by Nightly_Sanity
# This has different types of old_pytest like Single client connectivity, Single_Client_EAP, testrail_retest
#########################################################################################################
import datetime
import sys
import os
import threading

import allure
import pytest
import importlib

sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)
if "libs" not in sys.path:
    sys.path.append(f'../libs')
for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../../lanforge/lanforge-scripts/{folder}')

sys.path.append(f"../lanforge/lanforge-scripts/py-scripts/tip-cicd-sanity")

sys.path.append(f'../libs')
sys.path.append(f'../tools')
sys.path.append(f'../libs/lanforge/')
from sta_connect2 import StaConnect2
import time
import string
import random
import csv
from datetime import datetime
from pull_report import Report
from scp_util import SCP_File

S = 12
# from eap_connect import EAPConnect
from test_ipv4_ttls import TTLSTest
from lf_wifi_capacity_test import WiFiCapacityTest
from create_station import CreateStation
import lf_ap_auto_test
import lf_dataplane_test
from lf_dataplane_test import DataplaneTest
from lf_rx_sensitivity_test import RxSensitivityTest
from lf_ap_auto_test import ApAutoTest
from csv_to_influx import CSVtoInflux
# from influx import RecordInflux
from lf_multipsk import MultiPsk
from lf_rvr_test import RvrTest
from attenuator_serial import AttenuatorSerial
from lf_atten_mod_test import CreateAttenuator
from lf_mesh_test import MeshTest
from LANforge.lfcli_base import LFCliBase
from lf_tr398_test import TR398Test
from lf_pcap import LfPcap
from sta_scan_test import StaScan
from lf_sniff_radio import SniffRadio

cv_test_reports = importlib.import_module("py-json.cv_test_reports")
lf_report = cv_test_reports.lanforge_reports
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class RunTest:

    def __init__(self, configuration_data=None, local_report_path="../reports/", influx_params=None, run_lf=False,
                 debug=False, skip_pcap=False):
        if "type" in configuration_data['traffic_generator'].keys():
            if lanforge_data["type"] == "mesh":
                self.lanforge_ip = lanforge_data["ip"]
                self.lanforge_port = lanforge_data["port"]
                self.ssh_port = lanforge_data["ssh_port"]
                self.upstream_port_1 = lanforge_data["upstream-mobile-sta"]
                self.upstream_port_2 = lanforge_data["upstream-root"]
                self.upstream_port_3 = lanforge_data["upstream-node-1"]
                self.upstream_port_4 = lanforge_data["upstream-node-2"]
                self.uplink_port_1 = lanforge_data["uplink-mobile-sta"]
                self.uplink_port_2 = lanforge_data["uplink-root"]
                self.uplink_port_3 = lanforge_data["uplink--node-1"]
                self.uplink_port_4 = lanforge_data["uplink--node-2"]
                self.upstream_resource_1 = self.upstream_port_1.split(".")[0] + "." + self.upstream_port_1.split(".")[1]
                self.upstream_resource_2 = self.upstream_port_2.split(".")[0] + "." + self.upstream_port_2.split(".")[1]
                self.upstream_resource_3 = self.upstream_port_3.split(".")[0] + "." + self.upstream_port_3.split(".")[1]
                self.upstream_resource_4 = self.upstream_port_4.split(".")[0] + "." + self.upstream_port_4.split(".")[1]
                self.uplink_resource_1 = self.uplink_port_1.split(".")[0] + "." + self.uplink_port_1.split(".")[1]
                self.uplink_resource_2 = self.uplink_port_2.split(".")[0] + "." + self.uplink_port_2.split(".")[1]
                self.uplink_resource_3 = self.uplink_port_3.split(".")[0] + "." + self.uplink_port_3.split(".")[1]
                self.uplink_resource_4 = self.uplink_port_4.split(".")[0] + "." + self.uplink_port_4.split(".")[1]
                self.upstream_subnet = lanforge_data["upstream_subnet-mobile-sta"]
                self.lf_ssh_port = lanforge_data["ssh_port"]
                print("hi", self.lanforge_port)
                self.local_report_path = local_report_path

        else:
            self.lanforge_ip = configuration_data['traffic_generator']['details']["ip"]
            self.lanforge_port = configuration_data['traffic_generator']['details']["port"]
            self.lanforge_ssh_port = configuration_data['traffic_generator']['details']["ssh_port"]
            self.twog_radios = configuration_data['traffic_generator']['details']["2.4G-Radio"]
            self.fiveg_radios = configuration_data['traffic_generator']['details']["5G-Radio"]
            self.ax_radios = configuration_data['traffic_generator']['details']["AX-Radio"]
            self.upstream_port = configuration_data['traffic_generator']['details']["upstream"].split(".")[2]
            self.twog_prefix = configuration_data['traffic_generator']['details']["2.4G-Station-Name"]
            self.fiveg_prefix = configuration_data['traffic_generator']['details']["5G-Station-Name"]
            self.ax_prefix = configuration_data['traffic_generator']['details']["AX-Station-Name"]
            self.debug = debug
            self.run_lf = run_lf
            self.skip_pcap = skip_pcap
            if self.run_lf:
                self.ssid_data = configuration_data['access_point'][0]['ssid']
            self.lf_ssh_port = configuration_data['traffic_generator']['details']["ssh_port"]
            self.staConnect = None
            self.dataplane_obj = None
            self.rx_sensitivity_obj = None
            self.dualbandptest_obj = None
            self.msthpt_obj = None
            self.cvtest_obj = None
            self.pcap_obj = None
            self.influx_params = influx_params
            # self.influxdb = RecordInflux(_influx_host=influx_params["influx_host"],
            #                              _influx_port=influx_params["influx_port"],
            #                              _influx_org=influx_params["influx_org"],
            #                              _influx_token=influx_params["influx_token"],
            #                              _influx_bucket=influx_params["influx_bucket"])
            self.local_report_path = local_report_path
            if not os.path.exists(self.local_report_path):
                os.mkdir(self.local_report_path)

    def Client_Connectivity(self, ssid="[BLANK]", passkey="[BLANK]", security="open", extra_securities=[],
                            station_name=[], mode="BRIDGE", vlan_id=1, band="twog", ssid_channel=None):
        """SINGLE CLIENT CONNECTIVITY using test_connect2.py"""
        self.staConnect = StaConnect2(self.lanforge_ip, self.lanforge_port, debug_=self.debug)

        self.staConnect.sta_mode = 0
        self.staConnect.upstream_resource = 1
        if mode == "BRIDGE":
            self.staConnect.upstream_port = self.upstream_port
        elif mode == "NAT":
            self.staConnect.upstream_port = self.upstream_port
        else:
            self.staConnect.upstream_port = self.upstream_port + "." + str(vlan_id)
        if band == "twog":
            if self.run_lf:
                ssid = self.ssid_data["2g-ssid"]
                passkey = self.ssid_data["2g-password"]
                security = self.ssid_data["2g-encryption"].lower()
                print(ssid)
            self.staConnect.radio = self.twog_radios[0]
            self.staConnect.admin_down(self.staConnect.radio)
            self.staConnect.admin_up(self.staConnect.radio)
            self.staConnect.sta_prefix = self.twog_prefix
        if band == "fiveg":
            if self.run_lf:
                ssid = self.ssid_data["5g-ssid"]
                passkey = self.ssid_data["5g-password"]
                security = self.ssid_data["5g-encryption"].lower()
            self.staConnect.radio = self.fiveg_radios[0]
            self.staConnect.reset_port(self.staConnect.radio)
            self.staConnect.sta_prefix = self.fiveg_prefix
        self.set_radio_channel(radio=self.staConnect.radio, channel=ssid_channel)
        print("scan ssid radio", self.staConnect.radio.split(".")[2])
        self.data_scan_ssid = self.scan_ssid(radio=self.staConnect.radio.split(".")[2])
        print("ssid scan data :- ", self.data_scan_ssid)
        result = self.check_ssid_available_scan_result(scan_ssid_data=self.data_scan_ssid, ssid=ssid)
        print("ssid available:-", result)
        if not result and ssid_channel:
            if not self.skip_pcap:
                print("sniff radio", self.ax_radios[0].split(".")[2])
                self.start_sniffer(radio_channel=ssid_channel, radio=self.ax_radios[0].split(".")[2], duration=30)
                time.sleep(30)
                self.stop_sniffer()
            print("ssid not available in scan result")
            return "FAIL", "ssid not available in scan result"
        self.staConnect.resource = 1
        self.staConnect.dut_ssid = ssid
        self.staConnect.dut_passwd = passkey
        self.staConnect.dut_security = security
        self.staConnect.station_names = station_name
        self.staConnect.runtime_secs = 40
        self.staConnect.bringup_time_sec = 80
        self.staConnect.cleanup_on_exit = True
        data_table = ""
        dict_table = {}
        self.staConnect.setup(extra_securities=extra_securities)
        for sta_name in self.staConnect.station_names:
            try:
                sta_url = self.staConnect.get_station_url(sta_name)
                station_info = self.staConnect.json_get(sta_url)
                dict_data = station_info["interface"]
                dict_table[""] = list(dict_data.keys())
                dict_table["Before"] = list(dict_data.values())
            except Exception as e:
                print(e)
        if ssid_channel:
            if not self.skip_pcap:
                print("sniff radio", self.ax_radios[0].split(".")[2])
                self.start_sniffer(radio_channel=ssid_channel, radio=self.ax_radios[0].split(".")[2], duration=30)
        self.staConnect.start()
        print("napping %f sec" % self.staConnect.runtime_secs)
        time.sleep(self.staConnect.runtime_secs)
        report_obj = Report()
        for sta_name in self.staConnect.station_names:
            try:
                sta_url = self.staConnect.get_station_url(sta_name)
                station_info = self.staConnect.json_get(sta_url)
                self.station_ip = station_info["interface"]["ip"]
                dict_data = station_info["interface"]
                dict_table["After"] = list(dict_data.values())
                try:
                    data_table = report_obj.table2(table=dict_table, headers='keys')
                except Exception as e:
                    print(e)
                allure.attach(name=str(sta_name), body=data_table)
            except Exception as e:
                print(e)
        self.staConnect.stop()
        run_results = self.staConnect.get_result_list()
        if not self.staConnect.passes():
            if self.debug:
                for result in run_results:
                    print("test result: " + result)
                pytest.exit("Test Failed: Debug True")
        self.staConnect.cleanup()
        try:
            supplicant = "/home/lanforge/wifi/wpa_supplicant_log_" + self.staConnect.radio.split(".")[2] + ".txt"
            obj = SCP_File(ip=self.lanforge_ip, port=self.lanforge_ssh_port, username="root", password="lanforge",
                           remote_path=supplicant,
                           local_path=".")
            obj.pull_file()
            allure.attach.file(source="wpa_supplicant_log_" + self.staConnect.radio.split(".")[2] + ".txt",
                               name="supplicant_log")
        except Exception as e:
            print(e)

        for result in run_results:
            print("test result: " + result)
        result = "PASS"
        description = "Unknown error"
        dict_table = {}
        print("Client Connectivity :", self.staConnect.passes)
        endp_data = []
        for i in self.staConnect.resulting_endpoints:
            endp_data.append(self.staConnect.resulting_endpoints[i]["endpoint"])
        dict_table["key"] = [i for s in [d.keys() for d in endp_data] for i in s]
        dict_table["value"] = [i for s in [d.values() for d in endp_data] for i in s]
        data_table = report_obj.table2(table=dict_table, headers='keys')
        allure.attach(name="cx_data", body=data_table)
        for i in range(len(run_results)):
            if i == 0:
                if "FAILED" in run_results[i]:
                    result = "FAIL"
                    description = "Station did not get an ip"
                    break
            else:
                if "FAILED" in run_results[i]:
                    result = "FAIL"
                    description = "did not report traffic"

        if self.staConnect.passes():
            print("client connection to", self.staConnect.dut_ssid, "successful. Test Passed")
            result = "PASS"
        else:
            print("client connection to", self.staConnect.dut_ssid, "unsuccessful. Test Failed")
            result = "FAIL"
        time.sleep(3)
        if ssid_channel:
            if not self.skip_pcap:
                self.stop_sniffer()
        self.set_radio_channel(radio=self.staConnect.radio, channel="AUTO")
        return result, description

    def EAP_Connect(self, ssid="[BLANK]", passkey="[BLANK]", security="wpa2", extra_securities=[],
                    mode="BRIDGE", band="twog", vlan_id=100,
                    station_name=[], key_mgmt="WPA-EAP",
                    pairwise="NA", group="NA", wpa_psk="DEFAULT",
                    ttls_passwd="nolastart", ieee80211w=1,
                    wep_key="NA", ca_cert="NA", eap="TTLS", identity="nolaradius", d_vlan=False, cleanup=True,
                    ssid_channel=None):
        self.eap_connect = TTLSTest(host=self.lanforge_ip, port=self.lanforge_port,
                                    sta_list=station_name, vap=False, _debug_on=self.debug)

        self.eap_connect.station_profile.sta_mode = 0
        self.eap_connect.upstream_resource = 1
        if mode == "BRIDGE":
            self.eap_connect.l3_cx_obj_udp.upstream = self.upstream_port
            self.eap_connect.l3_cx_obj_tcp.upstream = self.upstream_port
        elif mode == "NAT":
            self.eap_connect.l3_cx_obj_udp.upstream = self.upstream_port
            self.eap_connect.l3_cx_obj_tcp.upstream = self.upstream_port
        else:
            self.eap_connect.l3_cx_obj_udp.upstream = self.upstream_port + "." + str(vlan_id)
            self.eap_connect.l3_cx_obj_tcp.upstream = self.upstream_port + "." + str(vlan_id)
        if band == "twog":
            if self.run_lf:
                ssid = self.ssid_data["2g-ssid"]
                passkey = self.ssid_data["2g-password"]
                security = self.ssid_data["2g-encryption"]
            self.eap_connect.radio = self.twog_radios[0]
            self.eap_connect.admin_down(self.eap_connect.radio)
            self.eap_connect.admin_up(self.eap_connect.radio)
            # self.eap_connect.sta_prefix = self.twog_prefix
        if band == "fiveg":
            if self.run_lf:
                ssid = self.ssid_data["5g-ssid"]
                passkey = self.ssid_data["5g-password"]
                security = self.ssid_data["5g-encryption"]
            self.eap_connect.radio = self.fiveg_radios[0]
            self.eap_connect.admin_down(self.eap_connect.radio)
            self.eap_connect.admin_up(self.eap_connect.radio)
            # self.eap_connect.sta_prefix = self.fiveg_prefix
        # self.eap_connect.resource = 1
        self.set_radio_channel(radio=self.eap_connect.radio, channel=ssid_channel)
        print("scan ssid radio", self.eap_connect.radio.split(".")[2])
        self.data_scan_ssid = self.scan_ssid(radio=self.eap_connect.radio.split(".")[2])
        print("ssid scan data :- ", self.data_scan_ssid)
        result = self.check_ssid_available_scan_result(scan_ssid_data=self.data_scan_ssid, ssid=ssid)
        print("ssid available:-", result)
        if not result and ssid_channel:
            if not self.skip_pcap:
                print("sniff radio", self.ax_radios[0].split(".")[2])
                self.start_sniffer(radio_channel=ssid_channel, radio=self.ax_radios[0].split(".")[2], duration=30)
                time.sleep(30)
                self.stop_sniffer()
            print("ssid not available in scan result")
            return "FAIL", "ssid not available in scan result"
        if eap == "TTLS":
            self.eap_connect.ieee80211w = ieee80211w
            self.eap_connect.key_mgmt = key_mgmt
            self.eap_connect.station_profile.set_command_flag("add_sta", "80211u_enable", 0)
            self.eap_connect.identity = identity
            self.eap_connect.ttls_passwd = ttls_passwd
            self.eap_connect.pairwise = pairwise
            self.eap_connect.group = group
        if eap == "TLS":
            self.eap_connect.key_mgmt = key_mgmt
            self.eap_connect.station_profile.set_command_flag("add_sta", "80211u_enable", 0)
            self.eap_connect.eap = eap
            self.eap_connect.identity = "user"
            self.eap_connect.ttls_passwd = "password"
            self.eap_connect.private_key = "/home/lanforge/client.p12"
            self.eap_connect.ca_cert = "/home/lanforge/ca.pem"
            self.eap_connect.pk_passwd = "whatever"
            self.eap_connect.ieee80211w = 1

        # self.eap_connect.hs20_enable = False
        self.eap_connect.ssid = ssid
        self.eap_connect.password = passkey
        self.eap_connect.security = security
        self.eap_connect.sta_list = station_name
        self.eap_connect.build(extra_securities=extra_securities)
        dict_table = {}
        report_obj = Report()
        data_table = ""
        for sta_name in station_name:
            try:
                station_info = self.eap_connect.json_get("port/1/1/" + sta_name)
                dict_data = station_info["interface"]
                dict_table[""] = list(dict_data.keys())
                dict_table["Before"] = list(dict_data.values())
            except Exception as e:
                print(e)
        if ssid_channel:
            if not self.skip_pcap:
                print("sniff radio", self.ax_radios[0].split(".")[2])
                self.start_sniffer(radio_channel=ssid_channel, radio=self.ax_radios[0].split(".")[2], duration=30)
        self.eap_connect.start(station_name, True, True)
        if d_vlan:
            self.station_ip = {}
        for sta_name in station_name:
            # try:
            station_data_str = ""
            # sta_url = self.eap_connect.get_station_url(sta_name)
            # station_info = self.eap_connect.json_get(sta_url)
            station_info = self.eap_connect.json_get("port/1/1/" + sta_name)
            if d_vlan:
                if "ip" in station_info["interface"].keys():
                    self.station_ip[sta_name] = station_info["interface"]["ip"]

            dict_data = station_info["interface"]
            dict_table["After"] = list(dict_data.values())
            try:
                data_table = report_obj.table2(table=dict_table, headers='keys')
            except Exception as e:
                print(e)
            allure.attach(name=str(sta_name), body=data_table)
            # except Exception as e:
            #     print(e)

        self.eap_connect.stop()
        run_results = self.eap_connect.get_result_list()[1:]
        try:
            supplicant = "/home/lanforge/wifi/wpa_supplicant_log_" + self.eap_connect.radio.split(".")[2] + ".txt"
            obj = SCP_File(ip=self.lanforge_ip, port=self.lanforge_ssh_port, username="root", password="lanforge",
                           remote_path=supplicant,
                           local_path=".")
            obj.pull_file()
            allure.attach.file(source="wpa_supplicant_log_" + self.eap_connect.radio.split(".")[2] + ".txt",
                               name="supplicant_log")
        except Exception as e:
            print(e)

        if not self.eap_connect.passes():
            if self.debug:
                print("test result: " + self.eap_connect.passes())
                pytest.exit("Test Failed: Debug True")
        endp_data = []
        result = "PASS"
        description = "Unknown error"
        dict_table = {}
        for i in self.eap_connect.resulting_endpoints:
            endp_data.append(self.eap_connect.resulting_endpoints[i]["endpoint"])
        # finding all keys and values
        dict_table["key"] = [i for s in [d.keys() for d in endp_data] for i in s]
        dict_table["value"] = [i for s in [d.values() for d in endp_data] for i in s]
        data_table = report_obj.table2(table=dict_table, headers='keys')
        allure.attach(name="cx_data", body=data_table)
        for i in range(len(run_results)):
            if i == 0:
                if "FAILED" in run_results[i]:
                    result = "FAIL"
                    description = "Station did not get an ip"
                    break
            else:
                if "FAILED" in run_results[i]:
                    result = "FAIL"
                    description = "did not report traffic"
        if cleanup:
            self.eap_connect.cleanup(station_name)
        if self.eap_connect.passes():
            result = "PASS"
        else:
            result = "FAIL"
        if ssid_channel:
            if not self.skip_pcap:
                self.stop_sniffer()
        self.set_radio_channel(radio=self.eap_connect.radio, channel="AUTO")
        return result, description

    def wifi_capacity(self, mode="BRIDGE", vlan_id=100, batch_size="1,5,10,20,40,64,128",
                      instance_name="wct_instance", download_rate="1Gbps", influx_tags="",
                      upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000", stations="", create_stations=True,
                      sort="interleave", raw_lines=[], sets=[]):
        instance_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
        if mode == "BRIDGE":
            upstream_port = self.upstream_port
        elif mode == "NAT":
            upstream_port = self.upstream_port
        elif mode == "VLAN":
            upstream_port = self.upstream_port + "." + str(vlan_id)
        '''SINGLE WIFI CAPACITY using lf_wifi_capacity.py'''
        wificapacity_obj = WiFiCapacityTest(lfclient_host=self.lanforge_ip,
                                            lf_port=self.lanforge_port,
                                            ssh_port=self.lf_ssh_port,
                                            lf_user="lanforge",
                                            lf_password="lanforge",
                                            local_lf_report_dir=self.local_report_path,
                                            instance_name=instance_name,
                                            config_name="wifi_config",
                                            upstream="1.1." + upstream_port,
                                            batch_size=batch_size,
                                            loop_iter="1",
                                            protocol=protocol,
                                            duration=duration,
                                            pull_report=True,
                                            load_old_cfg=False,
                                            upload_rate=upload_rate,
                                            download_rate=download_rate,
                                            sort=sort,
                                            stations=stations,
                                            create_stations=create_stations,
                                            radio=None,
                                            security=None,
                                            paswd=None,
                                            ssid=None,
                                            enables=[],
                                            disables=[],
                                            raw_lines=raw_lines,
                                            raw_lines_file="",
                                            test_tag=influx_tags,
                                            sets=sets)
        wificapacity_obj.setup()
        wificapacity_obj.run()

        report_name = "../reports/" + wificapacity_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        influx = CSVtoInflux(influx_host=self.influx_params["influx_host"],
                             influx_port=self.influx_params["influx_port"],
                             influx_org=self.influx_params["influx_org"],
                             influx_token=self.influx_params["influx_token"],
                             influx_bucket=self.influx_params["influx_bucket"],
                             path=report_name)

        influx.glob()
        return wificapacity_obj

    def Client_Connect(self, ssid="[BLANK]", passkey="[BLANK]", security="wpa2", mode="BRIDGE", band="twog",
                       vlan_id=100,
                       station_name=[]):
        if band == "twog":
            if self.run_lf:
                ssid = self.ssid_data["2g-ssid"]
                passkey = self.ssid_data["2g-password"]
                security = self.ssid_data["2g-encryption"].lower()
        if band == "fiveg":
            if self.run_lf:
                ssid = self.ssid_data["5g-ssid"]
                passkey = self.ssid_data["5g-password"]
                security = self.ssid_data["5g-encryption"].lower()
        self.client_connect = CreateStation(_host=self.lanforge_ip, _port=self.lanforge_port,
                                            _sta_list=station_name, _password=passkey, _ssid=ssid, _security=security)
        self.client_connect.station_profile.sta_mode = 0
        self.client_connect.upstream_resource = 1
        if mode == "BRIDGE":
            self.client_connect.upstream_port = self.upstream_port
        elif mode == "NAT":
            self.client_connect.upstream_port = self.upstream_port
        else:
            self.client_connect.upstream_port = self.upstream_port + "." + str(vlan_id)
        if band == "twog":
            self.client_connect.radio = self.twog_radios[0]
            # self.client_connect.sta_prefix = self.twog_prefix
        if band == "fiveg":
            self.client_connect.radio = self.fiveg_radios[0]
        if band == "ax":
            self.client_connect.radio = self.ax_radios[0]
        print("scan ssid radio", self.client_connect.radio.split(".")[2])
        self.data_scan_ssid = self.scan_ssid(radio=self.client_connect.radio.split(".")[2])
        print("ssid scan data :- ", self.data_scan_ssid)
        self.client_connect.build()
        self.client_connect.wait_for_ip(station_name)
        print(self.client_connect.wait_for_ip(station_name))
        if self.client_connect.wait_for_ip(station_name):
            self.client_connect._pass("ALL Stations got IP's", print_=True)
            return self.client_connect
        else:
            return False

    def attach_stationdata_to_allure(self, station_name=[], name=""):
        self.sta_url_map = None
        for sta_name_ in station_name:
            if sta_name_ is None:
                raise ValueError("get_station_url wants a station name")
            if self.sta_url_map is None:
                self.sta_url_map = {}
                for sta_name in station_name:
                    self.sta_url_map[sta_name] = "port/1/%s/%s" % (str(1), sta_name)
                    print(self.sta_url_map)

        for sta_name in station_name:
            try:
                station_data_str = ""
                # sta_url = self.staConnect.get_station_url(sta_name)
                cli_base = LFCliBase(_lfjson_host=self.lanforge_ip, _lfjson_port=self.lanforge_port, )
                station_info = cli_base.json_get(_req_url=self.sta_url_map[sta_name])
                print("station info", station_info)
                for i in station_info["interface"]:
                    try:
                        station_data_str = station_data_str + i + "  :  " + str(station_info["interface"][i]) + "\n"
                    except Exception as e:
                        print(e)
                print("sta name", sta_name)
                allure.attach(name=name, body=str(station_data_str))
            except Exception as e:
                print(e)

    def Client_Connect_Using_Radio(self, ssid="[BLANK]", passkey="[BLANK]", security="wpa2", mode="BRIDGE",
                                   vlan_id=100, radio=None, sta_mode=0,
                                   station_name=[]):
        self.client_connect = CreateStation(_host=self.lanforge_ip, _port=self.lanforge_port, _mode=sta_mode,
                                            _sta_list=station_name, _password=passkey, _ssid=ssid, _security=security)

        # self.client_connect.station_profile.sta_mode = sta_mode
        self.client_connect.upstream_resource = 1
        if mode == "BRIDGE":
            self.client_connect.upstream_port = self.upstream_port
        elif mode == "NAT":
            self.client_connect.upstream_port = self.upstream_port
        else:
            self.client_connect.upstream_port = self.upstream_port + "." + str(vlan_id)

        self.client_connect.radio = radio
        self.client_connect.build()
        self.client_connect.wait_for_ip(station_name)
        print(self.client_connect.wait_for_ip(station_name))
        if self.client_connect.wait_for_ip(station_name):
            self.client_connect._pass("ALL Stations got IP's", print_=True)
            return self.client_connect
        else:
            return False

    def wait_for_ip(self, station=[]):
        self.local_realm = realm.Realm(lfclient_host=self.lanforge_ip, lfclient_port=self.lanforge_port)
        print(station)
        if self.local_realm.wait_for_ip(station_list=station):
            self.local_realm._pass("ALL Stations got IP's", print_=True)
            return True
        else:
            return False

    def Client_disconnect(self, station_name=[]):
        self.client_dis = CreateStation(_host=self.lanforge_ip, _port=self.lanforge_port,
                                        _sta_list=station_name, _password="passkey", _ssid="ssid", _security="security")
        self.client_dis.station_profile.cleanup(station_name)
        return True

    def dataplane(self, station_name=None, mode="BRIDGE", vlan_id=100, download_rate="85%", dut_name="TIP",
                  upload_rate="0", duration="15s", instance_name="test_demo", raw_lines=None, influx_tags=""):
        instance_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

        if mode == "BRIDGE":
            upstream_port = self.upstream_port
        elif mode == "NAT":

            upstream_port = self.upstream_port
        elif mode == "VLAN":
            # self.upstream_port = self.upstream_port + "." + str(vlan_id)
            upstream_port = self.upstream_port + "." + str(vlan_id)

        if raw_lines is None:
            raw_lines = [['pkts: 60;142;256;512;1024;MTU;4000'], ['directions: DUT Transmit;DUT Receive'],
                         ['traffic_types: UDP;TCP'],
                         ["show_3s: 1"], ["show_ll_graphs: 1"], ["show_log: 1"]]
            self.client_connect.upstream_port = upstream_port
        elif mode == "VLAN":
            self.client_connect.upstream_port = upstream_port + "." + str(vlan_id)

        if raw_lines is None:
            raw_lines = [['pkts: 60;142;256;512;1024;MTU;4000'], ['directions: DUT Transmit;DUT Receive'],
                         ['traffic_types: UDP;TCP'],
                         ["show_3s: 1"], ["show_ll_graphs: 1"], ["show_log: 1"]]

        self.dataplane_obj = DataplaneTest(lf_host=self.lanforge_ip,
                                           lf_port=self.lanforge_port,
                                           ssh_port=self.lf_ssh_port,
                                           local_lf_report_dir=self.local_report_path,
                                           lf_user="lanforge",
                                           lf_password="lanforge",
                                           instance_name=instance_name,
                                           config_name="dpt_config",
                                           upstream="1.1." + upstream_port,
                                           pull_report=True,
                                           load_old_cfg=False,
                                           download_speed=download_rate,
                                           upload_speed=upload_rate,
                                           duration=duration,
                                           dut=dut_name,
                                           station="1.1." + station_name[0],
                                           test_tag=influx_tags,
                                           raw_lines=raw_lines)

        self.dataplane_obj.setup()
        self.dataplane_obj.run()
        report_name = self.dataplane_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        influx = CSVtoInflux(influx_host=self.influx_params["influx_host"],
                             influx_port=self.influx_params["influx_port"],
                             influx_org=self.influx_params["influx_org"],
                             influx_token=self.influx_params["influx_token"],
                             influx_bucket=self.influx_params["influx_bucket"],
                             path=report_name)

        influx.glob()

        return self.dataplane_obj

    def dualbandperformancetest(self, ssid_5G="[BLANK]", ssid_2G="[BLANK]", mode="BRIDGE", vlan_id=100, dut_name="TIP",
                                instance_name="test_demo", dut_5g="", dut_2g="", influx_tags=""):
        instance_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

        if mode == "BRIDGE":
            self.upstream_port = self.upstream_port
        elif mode == "NAT":
            self.upstream_port = self.upstream_port
        else:
            self.upstream_port = self.upstream_port + "." + str(vlan_id)

        self.dualbandptest_obj = ApAutoTest(lf_host=self.lanforge_ip,
                                            lf_port=self.lanforge_port,
                                            lf_user="lanforge",
                                            lf_password="lanforge",
                                            ssh_port=self.lf_ssh_port,
                                            instance_name=instance_name,
                                            config_name="dbp_config",
                                            upstream="1.1." + self.upstream_port,
                                            pull_report=True,
                                            dut5_0=dut_5g,
                                            dut2_0=dut_2g,
                                            load_old_cfg=False,
                                            local_lf_report_dir=self.local_report_path,
                                            max_stations_2=64,
                                            max_stations_5=64,
                                            max_stations_dual=124,
                                            radio2=[self.twog_radios],
                                            radio5=[self.fiveg_radios],
                                            test_tag=influx_tags,
                                            sets=[['Basic Client Connectivity', '0'], ['Multi Band Performance', '1'],
                                                  ['Throughput vs Pkt Size', '0'], ['Capacity', '0'],
                                                  ['Skip 2.4Ghz Tests', '1'],
                                                  ['Skip 5Ghz Tests', '1'],
                                                  ['Stability', '0'],
                                                  ['Band-Steering', '0'], ['Multi-Station Throughput vs Pkt Size', '0'],
                                                  ['Long-Term', '0']]
                                            )
        self.dualbandptest_obj.setup()
        self.dualbandptest_obj.run()
        report_name = self.dualbandptest_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        influx = CSVtoInflux(influx_host=self.influx_params["influx_host"],
                             influx_port=self.influx_params["influx_port"],
                             influx_org=self.influx_params["influx_org"],
                             influx_token=self.influx_params["influx_token"],
                             influx_bucket=self.influx_params["influx_bucket"],
                             path=report_name)

        influx.glob()
        return self.dualbandptest_obj

    def apstabilitytest(self, ssid_5G="[BLANK]", ssid_2G="[BLANK]", mode="BRIDGE", vlan_id=100, dut_name="TIP",
                        instance_name="test_demo", dut_5g="", dut_2g=""):
        instance_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

        if mode == "BRIDGE":
            self.upstream_port = self.upstream_port
        elif mode == "NAT":
            self.upstream_port = self.upstream_port
        else:
            self.upstream_port = self.upstream_port + "." + str(vlan_id)

        self.apstab_obj = ApAutoTest(lf_host=self.lanforge_ip,
                                     lf_port=self.lanforge_port,
                                     lf_user="lanforge",
                                     lf_password="lanforge",
                                     instance_name=instance_name,
                                     config_name="dbp_config",
                                     upstream="1.1." + self.upstream_port,
                                     pull_report=True,
                                     dut5_0=dut_5g,
                                     dut2_0=dut_2g,
                                     load_old_cfg=False,
                                     local_lf_report_dir=self.local_report_path,
                                     max_stations_2=5,
                                     max_stations_5=5,
                                     max_stations_dual=10,
                                     radio2=[self.twog_radios],
                                     radio5=[self.fiveg_radios],
                                     sets=[['Basic Client Connectivity', '0'], ['Multi Band Performance', '0'],
                                           ['Throughput vs Pkt Size', '0'], ['Capacity', '0'],
                                           ['Stability', '1'],
                                           ['Band-Steering', '0'], ['Multi-Station Throughput vs Pkt Size', '0'],
                                           ['Long-Term', '0']],
                                     raw_lines=[['reset_dur:300'], ['reset_batch_size:2']]
                                     )
        self.apstab_obj.setup()
        self.apstab_obj.run()
        report_name = self.apstab_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        influx = CSVtoInflux(influx_host=self.influx_params["influx_host"],
                             influx_port=self.influx_params["influx_port"],
                             influx_org=self.influx_params["influx_org"],
                             influx_token=self.influx_params["influx_token"],
                             influx_bucket=self.influx_params["influx_bucket"],
                             path=report_name)

        influx.glob()
        return self.apstab_obj

    def ratevsrange(self, station_name=None, mode="BRIDGE", vlan_id=100, download_rate="85%", dut_name="TIP",
                    upload_rate="0", duration="1m", instance_name="test_demo", raw_lines=None):
        if mode == "BRIDGE":
            self.client_connect.upstream_port = self.upstream_port
        elif mode == "NAT":
            self.client_connect.upstream_port = self.upstream_port
        elif mode == "VLAN":
            self.client_connect.upstream_port = self.upstream_port + "." + str(vlan_id)

        self.rvr_obj = RvrTest(lf_host=self.lanforge_ip,
                               lf_port=self.lanforge_port,
                               ssh_port=self.lf_ssh_port,
                               lf_user="lanforge",
                               local_lf_report_dir=self.local_report_path,
                               lf_password="lanforge",
                               instance_name=instance_name,
                               config_name="rvr_config",
                               upstream="1.1." + self.upstream_port,
                               pull_report=True,
                               load_old_cfg=False,
                               upload_speed=upload_rate,
                               download_speed=download_rate,
                               duration=duration,
                               station="1.1." + station_name[0],
                               dut=dut_name,
                               raw_lines=raw_lines)
        self.rvr_obj.setup()
        self.rvr_obj.run()
        report_name = self.rvr_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        influx = CSVtoInflux(influx_host=self.influx_params["influx_host"],
                             influx_port=self.influx_params["influx_port"],
                             influx_org=self.influx_params["influx_org"],
                             influx_token=self.influx_params["influx_token"],
                             influx_bucket=self.influx_params["influx_bucket"],
                             path=report_name)

        influx.glob()
        return self.rvr_obj

    def rx_sensitivity(self, station_name=None, mode="BRIDGE", vlan_id=100, download_rate="100%", dut_name="TIP",
                       upload_rate="0kbps", duration="30s", instance_name="test_demo", raw_lines=None):
        if mode == "BRIDGE":
            self.client_connect.upstream_port = self.upstream_port
        elif mode == "NAT":
            self.client_connect.upstream_port = self.upstream_port
        else:
            self.client_connect.upstream_port = self.upstream_port + "." + str(vlan_id)
        if raw_lines is None:
            raw_lines = [['txo_preamble: VHT'],
                         ['txo_mcs: 4 OFDM, HT, VHT;5 OFDM, HT, VHT;6 OFDM, HT, VHT;7 OFDM, HT, VHT'],
                         ['spatial_streams: 3'], ['bandw_options: 80'], ['txo_sgi: ON'],
                         ['txo_retries: No Retry'], ["show_3s: 1"], ['txo_txpower: 17'],
                         ["show_ll_graphs: 1"], ["show_log: 1"]]

        self.rx_sensitivity_obj = RxSensitivityTest(lf_host=self.lanforge_ip,
                                                    lf_port=self.lanforge_port,
                                                    ssh_port=self.lf_ssh_port,
                                                    local_path=self.local_report_path,
                                                    lf_user="lanforge",
                                                    lf_password="lanforge",
                                                    instance_name=instance_name,
                                                    config_name="rx_sen_config",
                                                    upstream="1.1." + self.upstream_port,
                                                    pull_report=True,
                                                    load_old_cfg=False,
                                                    download_speed=download_rate,
                                                    upload_speed=upload_rate,
                                                    duration=duration,
                                                    dut=dut_name,
                                                    station="1.1." + station_name[0],
                                                    raw_lines=raw_lines)
        self.rx_sensitivity_obj.setup()
        self.rx_sensitivity_obj.run()
        report_name = self.rx_sensitivity_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        influx = CSVtoInflux(influx_host=self.influx_params["influx_host"],
                             influx_port=self.influx_params["influx_port"],
                             influx_org=self.influx_params["influx_org"],
                             influx_token=self.influx_params["influx_token"],
                             influx_bucket=self.influx_params["influx_bucket"],
                             path=report_name)

        influx.glob()
        return self.rx_sensitivity_obj

    def multipsk(self, ssid="[BLANK]", security=None, mode=None, key1=None, vlan_id=None, key2=None, band="twog",
                 station_name=None, n_vlan="1", key3=None):
        global result1, sta_name
        if mode == "BRIDGE":
            self.upstream_port = self.upstream_port
        elif mode == "NAT":
            self.upstream_port = self.upstream_port
        if band == "twog":
            radio = self.twog_radios[0]
        elif band == "fiveg":
            radio = self.fiveg_radios[0]
        print("vlan id", vlan_id)

        if n_vlan == "1":
            input_data = [{
                "password": key1,
                "upstream": str(self.upstream_port) + "." + str(vlan_id[0]),
                "mac": "",
                "num_station": 1,
                "radio": str(radio)
            },
                {
                    "password": key2,
                    "upstream": str(self.upstream_port),
                    "mac": "",
                    "num_station": 1,
                    "radio": str(radio)
                },
            ]
        else:
            input_data = [{
                "password": key1,
                "upstream": str(self.upstream_port) + "." + str(vlan_id[0]),
                "mac": "",
                "num_station": 1,
                "radio": str(radio)
            },
                {
                    "password": key2,
                    "upstream": str(self.upstream_port) + "." + str(vlan_id[1]),
                    "mac": "",
                    "num_station": 1,
                    "radio": str(radio)
                },
                {
                    "password": key3,
                    "upstream": str(self.upstream_port),
                    "mac": "",
                    "num_station": 1,
                    "radio": str(radio)
                },
            ]
        print("station name", station_name)

        self.multi_obj = MultiPsk(host=self.lanforge_ip,
                                  port=self.lanforge_port,
                                  ssid=ssid,
                                  input=input_data,
                                  security=security, )
        self.sta_url_map = None
        self.multi_obj.build()
        self.multi_obj.start()
        time.sleep(60)
        self.multi_obj.monitor_vlan_ip()
        if n_vlan == "1":
            self.multi_obj.get_sta_ip()
        else:
            self.multi_obj.get_sta_ip_for_more_vlan()

        result = self.multi_obj.compare_ip()
        print("checking for vlan ips")
        if result == "Pass":
            print("Test pass")
        else:
            print("Test Fail")
        print("now checking ip for non vlan port")
        self.multi_obj.monitor_non_vlan_ip()
        self.multi_obj.get_non_vlan_sta_ip()
        print("mode", mode)
        if mode == "BRIDGE":
            result1 = self.multi_obj.compare_nonvlan_ip_bridge()
        elif mode == "NAT":
            result1 = self.multi_obj.compare_nonvlan_ip_nat()
        # station_name =  ['sta100', 'sta200', 'sta00']
        for sta_name_ in station_name:
            if sta_name_ is None:
                raise ValueError("get_station_url wants a station name")
            if self.sta_url_map is None:
                self.sta_url_map = {}
                for sta_name in station_name:
                    self.sta_url_map[sta_name] = "port/1/%s/%s" % (str(1), sta_name)
                    print(self.sta_url_map)

        for sta_name in station_name:
            try:
                station_data_str = ""
                # sta_url = self.staConnect.get_station_url(sta_name)
                station_info = self.multi_obj.local_realm.json_get(self.sta_url_map[sta_name])
                print("station info", station_info)
                for i in station_info["interface"]:
                    try:
                        station_data_str = station_data_str + i + "  :  " + str(station_info["interface"][i]) + "\n"
                    except Exception as e:
                        print(e)
                print("sta name", sta_name)
                allure.attach(name=str(sta_name), body=str(station_data_str))
            except Exception as e:
                print(e)
        if result1 == "Pass":
            print("Test passed for non vlan ip ")
        else:
            print("Test failed for non vlan ip")
        print("all result gathered")
        print("clean up")
        self.multi_obj.postcleanup()
        if result == result1:
            return True
        else:
            return False

    def multi_sta_thpt(self, ssid_5G="[BLANK]", ssid_2G="[BLANK]", mode="BRIDGE", vlan_id=100, dut_name="TIP",
                       raw_line=[], instance_name="test_demo", dut_5g="", dut_2g=""):

        inst_name = instance_name.split('_')[0]
        instance_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

        if mode == "BRIDGE":
            self.upstream_port = self.upstream_port
        elif mode == "NAT":
            self.upstream_port = self.upstream_port
        else:
            self.upstream_port = self.upstream_port + "." + str(vlan_id)

        sets = [['Basic Client Connectivity', '0'], ['Multi Band Performance', '0'],
                ['Throughput vs Pkt Size', '0'], ['Capacity', '0'],
                ['Stability', '0'],
                ['Band-Steering', '0'], ['Multi-Station Throughput vs Pkt Size', '1'],
                ['Long-Term', '0']]

        if len(self.twog_radios) == 1:
            twog_radios = [[self.twog_radios[0]]]

        elif len(self.twog_radios) > 1:
            twog_radio = []
            for i in range(0, len(self.twog_radios)):
                twog_radio.append([self.twog_radios[i]])
            twog_radios = twog_radio

        if len(self.fiveg_radios) == 1:
            fiveg_radios = [[self.fiveg_radios[0]]]

        elif len(self.fiveg_radios) > 1:
            fiveg_radio = []
            for i in range(0, len(self.fiveg_radios)):
                fiveg_radio.append([self.fiveg_radios[i]])
            fiveg_radios = fiveg_radio

        self.msthpt_obj = ApAutoTest(lf_host=self.lanforge_ip,
                                     lf_port=self.lanforge_port,
                                     ssh_port=self.lf_ssh_port,

                                     lf_user="lanforge",
                                     lf_password="lanforge",
                                     instance_name=instance_name,
                                     config_name="dbp_config",
                                     upstream="1.1." + self.upstream_port,
                                     pull_report=True,
                                     dut5_0=dut_5g,
                                     dut2_0=dut_2g,
                                     load_old_cfg=False,
                                     local_lf_report_dir=self.local_report_path,
                                     radio2=twog_radios,
                                     radio5=fiveg_radios,
                                     sets=sets,
                                     raw_lines=raw_line
                                     )
        self.msthpt_obj.setup()
        self.msthpt_obj.run()
        report_name = self.msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        influx = CSVtoInflux(influx_host=self.influx_params["influx_host"],
                             influx_port=self.influx_params["influx_port"],
                             influx_org=self.influx_params["influx_org"],
                             influx_token=self.influx_params["influx_token"],
                             influx_bucket=self.influx_params["influx_bucket"],
                             path=report_name)

        influx.glob()
        return self.msthpt_obj

    def attenuator_serial(self):
        self.obj = AttenuatorSerial(
            lfclient_host=self.lanforge_ip,
            lfclient_port=self.lanforge_port
        )
        val = self.obj.show()
        return val

    def attenuator_modify(self, serno, idx, val):
        atten_obj = CreateAttenuator(self.lanforge_ip, self.lanforge_port, serno, idx, val)
        atten_obj.build()

    def mesh_test(self, instance_name=None, raw_lines=None, duration="60s"):
        self.mesh_obj = MeshTest(
            lf_host=self.lanforge_ip,
            lf_port=self.lanforge_port,
            ssh_port=self.lf_ssh_port,
            local_lf_report_dir=self.local_report_path,
            lf_user="lanforge",
            lf_password="lanforge",
            instance_name=instance_name,
            duration=duration,
            config_name="mesh_config",
            upstream="1.2.2 eth2",
            upload_speed="85%",
            download_speed="85%",
            pull_report=True,
            load_old_cfg=False,
            raw_lines=raw_lines,
        )
        self.mesh_obj.setup()
        self.mesh_obj.run()
        return self.mesh_obj

    def attenuator_serial_2g_radio(self, ssid="[BLANK]", passkey="[BLANK]", security="wpa2", mode="BRIDGE",
                                   vlan_id=100, sta_mode=0, station_name=[], lf_tools_obj=None):
        radio = self.twog_radios[0]
        # index 0 of atten_serial_radio will ser no of 1st 2g radio and index 1 will ser no of 2nd and 3rd 2g radio
        atten_serial_radio = []
        atten_serial = self.attenuator_serial()
        self.Client_Connect_Using_Radio(ssid=ssid, passkey=passkey, security=security, mode=mode,
                                        vlan_id=vlan_id, radio=radio, sta_mode=sta_mode,
                                        station_name=station_name)
        signal1 = lf_tools_obj.station_data_query(station_name=station_name[0], query="signal")
        atten_sr = atten_serial[0].split(".")
        for i in range(4):
            self.attenuator_modify(int(atten_sr[2]), i, 400)
            time.sleep(0.5)
        signal2 = lf_tools_obj.station_data_query(station_name=station_name[0], query="signal")
        if abs(int(signal2.split(" ")[0])) - abs(int(signal1.split(" ")[0])) >= 5:
            atten_serial_radio = atten_serial
        else:
            atten_serial_radio = atten_serial[::-1]
        self.Client_disconnect(station_name=station_name)
        return atten_serial_radio

    def attenuator_serial_5g_radio(self, ssid="[BLANK]", passkey="[BLANK]", security="wpa2", mode="BRIDGE",
                                   vlan_id=100, sta_mode=0, station_name=[], lf_tools_obj=None):
        radio = self.fiveg_radios[0]
        # index 0 of atten_serial_radio will ser no of 1st 5g radio and index 1 will ser no of 2nd and 3rd 5g radio
        atten_serial_radio = []
        atten_serial = self.attenuator_serial()
        self.Client_Connect_Using_Radio(ssid=ssid, passkey=passkey, security=security, mode=mode,
                                        vlan_id=vlan_id, radio=radio, sta_mode=sta_mode,
                                        station_name=station_name)
        signal1 = lf_tools_obj.station_data_query(station_name=station_name[0], query="signal")
        atten_sr = atten_serial[0].split(".")
        for i in range(4):
            self.attenuator_modify(int(atten_sr[2]), i, 400)
            time.sleep(0.5)
        signal2 = lf_tools_obj.station_data_query(station_name=station_name[0], query="signal")
        if abs(int(signal2.split(" ")[0])) - abs(int(signal1.split(" ")[0])) >= 5:
            atten_serial_radio = atten_serial
        else:
            atten_serial_radio = atten_serial[::-1]
        self.Client_disconnect(station_name=station_name)
        return atten_serial_radio


    def set_radio_country_channel(self,_radio="wiphy0",_channel=0,_country_num=840,): # 840 - US
        data = {
            "shelf": _radio[0],
            "resource": _radio[1],
            "radio": _radio[2],
            "mode": "NA",
            "channel": _channel,
            "country": _country_num
        }
        print(f"Lanforge-radio Country changed {_country_num}")
        self.local_realm.json_post("/cli-json/set_wifi_radio", _data=data)

    def downlink_mu_mimo(self, radios_2g=[], radios_5g=[], radios_ax=[], dut_name="TIP", dut_5g="", dut_2g="",
                         mode="BRIDGE", vlan_id=1, skip_2g=True, skip_5g=False):
        raw_line = []
        skip_twog = '1' if skip_2g else '0'
        skip_fiveg = '1' if skip_5g else '0'
        sniff_radio = 'wiphy6'
        channel = 149 if skip_2g else 11
        upstream_port = self.upstream_port

        sets = [['Calibrate Attenuators', '0'], ['Receiver Sensitivity', '0'], ['Maximum Connection', '0'],
                ['Maximum Throughput', '0'], ['Airtime Fairness', '0'], ['Range Versus Rate', '0'],
                ['Spatial Consistency', '0'],
                ['Multiple STAs Performance', '0'], ['Multiple Assoc Stability', '0'], ['Downlink MU-MIMO', '1'],
                ['AP Coexistence', '0'], ['Long Term Stability', '0'], ['Skip 2.4Ghz Tests', f'{skip_twog}'],
                ['Skip 5Ghz Tests', f'{skip_fiveg}'], ['2.4Ghz Channel', 'AUTO'], ['5Ghz Channel', 'AUTO']]
        for i in range(6):
            if i == 0 or i == 2:
                raw_line.append([f'radio-{i}: {radios_5g[0] if i == 0 else radios_5g[1]}'])
            if i == 1 or i == 3:
                raw_line.append([f'radio-{i}: {radios_2g[0] if i == 1 else radios_2g[1]}'])
            if i == 4 or i == 5:
                raw_line.append([f'radio-{i}: {radios_ax[0] if i == 4 else radios_ax[1]}'])

        if len(raw_line) != 6:
            raw_line = [['radio-0: 1.1.5 wiphy1'], ['radio-1: 1.1.4 wiphy0'], ['radio-2: 1.1.7 wiphy3'],
                        ['radio-3: 1.1.6 wiphy2'], ['radio-4: 1.1.8 wiphy4'], ['radio-5: 1.1.9 wiphy5']]
        instance_name = "tr398-instance-{}".format(str(random.randint(0, 100000)))

        if not os.path.exists("mu-mimo-config.txt"):
            with open("mu-mimo-config.txt", "wt") as f:
                for i in raw_line:
                    f.write(str(i[0]) + "\n")
                f.close()

        if mode == "BRIDGE" or mode == "NAT":
            upstream_port = self.upstream_port
        else:
            upstream_port = self.upstream_port + "." + str(vlan_id)
        print("Upstream Port: ", self.upstream_port)

        self.pcap_obj = LfPcap(host=self.lanforge_ip, port=self.lanforge_port)
        self.cvtest_obj = TR398Test(lf_host=self.lanforge_ip,
                                    lf_port=self.lanforge_port,
                                    lf_user="lanforge",
                                    lf_password="lanforge",
                                    instance_name=instance_name,
                                    config_name="cv_dflt_cfg",
                                    upstream="1.1." + upstream_port,
                                    pull_report=True,
                                    local_lf_report_dir=self.local_report_path,
                                    load_old_cfg=False,
                                    dut2=dut_2g,
                                    dut5=dut_5g,
                                    raw_lines_file="mu-mimo-config.txt",
                                    enables=[],
                                    disables=[],
                                    raw_lines=[],
                                    sets=sets,
                                    test_rig=dut_name
                                    )
        self.cvtest_obj.setup()
        t1 = threading.Thread(target=self.cvtest_obj.run)
        t1.start()
        # t2 = threading.Thread(target=self.pcap_obj.sniff_packets, args=(sniff_radio, "mu-mimo", channel, 60))
        # if t1.is_alive():
        #     time.sleep(180)
        #     t2.start()
        while t1.is_alive():
            time.sleep(1)
        if os.path.exists("mu-mimo-config.txt"):
            os.remove("mu-mimo-config.txt")

        report_name = self.cvtest_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        influx = CSVtoInflux(influx_host=self.influx_params["influx_host"],
                             influx_port=self.influx_params["influx_port"],
                             influx_org=self.influx_params["influx_org"],
                             influx_token=self.influx_params["influx_token"],
                             influx_bucket=self.influx_params["influx_bucket"],
                             path=report_name)
        influx.glob()
        return self.cvtest_obj

        print(f"Lanforge-radio Country changed {_country_num}")
        self.local_realm.json_post("/cli-json/set_wifi_radio", _data=data)

    def scan_ssid(self, radio=""):
        '''This method for scan ssid data'''
        list_data = []
        obj_scan = StaScan(host=self.lanforge_ip, port=self.lanforge_port, ssid="fake ssid", security="open",
                           password="[BLANK]", radio=radio, sta_list=["sta0000"], csv_output="scan_ssid.csv")
        obj_scan.pre_cleanup()
        time1 = datetime.now()
        first = time.mktime(time1.timetuple()) * 1000
        obj_scan.build()
        obj_scan.start()
        time2 = datetime.now()
        second = time.mktime(time2.timetuple()) * 1000
        diff = int(second - first)
        try:
            with open(obj_scan.csv_output, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[1] == "age":
                        list_data.append(row)
                        continue
                    elif int(row[1]) < diff:
                        list_data.append(row)
        except Exception as e:
            print(e)
        report_obj = Report()
        csv_data_table = report_obj.table2(list_data)
        allure.attach(name="scan_ssid_data", body=csv_data_table)
        obj_scan.cleanup()
        return list_data

    def start_sniffer(self, radio_channel=None, radio=None, test_name="sniff_radio", duration=60):
        self.pcap_name = test_name + ".pcap"
        self.pcap_obj = SniffRadio(lfclient_host=self.lanforge_ip, lfclient_port=self.lanforge_port, radio=radio,
                                   channel=radio_channel)
        self.pcap_obj.setup(0, 0, 0)
        time.sleep(5)
        self.pcap_obj.monitor.admin_up()
        time.sleep(5)
        self.pcap_obj.monitor.start_sniff(capname=self.pcap_name, duration_sec=duration)

    def stop_sniffer(self):
        self.pcap_obj.monitor.admin_down()
        time.sleep(2)
        self.pcap_obj.cleanup()
        lf_report.pull_reports(hostname=self.lanforge_ip, port=self.lanforge_ssh_port, username="lanforge",
                               password="lanforge",
                               report_location="/home/lanforge/" + self.pcap_name,
                               report_dir=".")
        allure.attach.file(source=self.pcap_name,
                           name="pcap_file", attachment_type=allure.attachment_type.PCAP)
        print("pcap file name : ", self.pcap_name)
        return self.pcap_name

    def check_ssid_available_scan_result(self, scan_ssid_data=None, ssid=None):
        '''This method will check ssid available or not in scan ssid data'''
        try:
            flag = False
            for i in scan_ssid_data:
                if ssid in i:
                    flag = True
            if flag:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def country_code_channel_division(self, ssid = "[BLANK]", passkey='[BLANK]', security="wpa2", mode="BRIDGE",
                                      band='2G', station_name=[], vlan_id=100, channel='1', channel_width=20,
                                      country_num=392, country='United States(US)'):
        self.local_realm = realm.Realm(lfclient_host=self.lanforge_ip, lfclient_port=self.lanforge_port)
        radio = (self.fiveg_radios[0] if band == "fiveg" else self.twog_radios[0]).split('.')
        self.set_radio_country_channel(_radio=radio,_country_num=country_num)
        station = self.Client_Connect(ssid=ssid, passkey=passkey, security=security, mode=mode, band=band,
                                      station_name=station_name, vlan_id=vlan_id)
        if station:
            for i in range(10):
                station_info = station.json_get(f"/port/1/1/{station_name[0]}")
                if station_info['interface']['ip'] == '0.0.0.0':
                    time.sleep(5)
                else:
                    break
            print(f"station {station_name[0]} IP: {station_info['interface']['ip']}\n"
                  f"connected channel: {station_info['interface']['channel']}\n"
                  f"and expected channel: {channel}")
            allure.attach(name="Definition",
                          body="Country code channel test intends to verify stability of Wi-Fi device " \
                               "where the AP is configured with different countries with different channels.")
            allure.attach(name="Procedure",
                          body=f"This test case definition states that we push the basic {mode.lower()} mode config on the AP to "
                               f"be tested by configuring it with {country} on {channel_width}MHz channel width and "
                               f"channel {channel}. Create a client on {'5' if band=='fiveg' else '2.4'} GHz radio. Pass/ fail criteria: "
                               f"The client created on {'5' if band=='fiveg' else '2.4'} GHz radio should get associated to the AP")
            allure.attach(name="Details",
                          body=f"Country code : {country[country.find('(')+1:-1]}\n"
                               f"Bandwidth : {channel_width}Mhz\n"
                               f"Channel : {channel}\n")
            station_data_str = ""
            for i in station_info["interface"]:
                try:
                    station_data_str += i + "  :  " + str(station_info["interface"][i]) + "\n"
                except Exception as e:
                    print(e)
            allure.attach(name=str(station_name[0]), body=str(station_data_str))
            station.station_profile.cleanup()
            self.set_radio_country_channel(_radio=radio)
            if station_info['interface']['ip'] and station_info['interface']['channel'] == str(channel):
                return True
            else:
                return False

    def set_radio_channel(self, radio="1.1.wiphy0", channel="AUTO"):
        try:
            radio = radio.split(".")
            shelf = radio[0]
            resource = radio[1]
            radio_ = radio[2]
            print("radio %s channel %s" % (radio, channel))
            local_realm_obj = realm.Realm(lfclient_host=self.lanforge_ip, lfclient_port=self.lanforge_port)
            data = {
                "shelf": shelf,
                "resource": resource,
                "radio": radio_,
                "mode": "NA",
                "channel": channel
            }
            local_realm_obj.json_post("/cli-json/set_wifi_radio", _data=data)
            time.sleep(2)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    influx_host = "influx.cicd.lab.wlan.tip.build"
    influx_port = 80
    influx_token = "TCkdATXAbHmNbn4QyNaj43WpGBYxFrzV"
    influx_bucket = "tip-cicd"
    influx_org = "tip"
    influx_params = {
        "influx_host": influx_host,
        "influx_port": influx_port,
        "influx_token": influx_token,
        "influx_bucket": influx_bucket,
        "influx_org": influx_org,
        "influx_tag": ["basic-03", "ec420"],
    }
    lanforge_data = {
        "ip": "10.28.3.6",
        "port": 8080,
        "ssh_port": 22,
        "2.4G-Radio": ["1.1.wiphy4"],
        "5G-Radio": ["1.1.wiphy5"],
        "AX-Radio": ["1.1.wiphy0", "1.1.wiphy1", "1.1.wiphy2", "1.1.wiphy3"],
        "upstream": "1.1.eth2",
        "upstream_subnet": "10.28.2.1/24",
        "uplink": "1.1.eth3",
        "2.4G-Station-Name": "wlan0",
        "5G-Station-Name": "wlan1",
        "AX-Station-Name": "ax"
    }
    obj = RunTest(lanforge_data=lanforge_data, debug=False, influx_params=influx_params)
    upstream = lanforge_data['upstream']
    # data = obj.staConnect.json_get("/port/all")
    obj.eap_connect.admin_down("1.1.wiphy4")
    obj.eap_connect.admin_up("1.1.wiphy4")
    # print(dict(list(data['interfaces'])).keys())
    # print(obj.staConnect.json_get("/port/" + upstream.split(".")[0] +
    #                         "/" + upstream.split(".")[1] +
    #                         "/" + upstream.split(".")[2] + "/" + "10"))
    # print("/port/" + upstream.split(".")[0] +
    #                         "/" + upstream.split(".")[1] +
    #                         "/" + upstream.split(".")[2] + "/" + "100")
    # obj.Client_Connect(ssid="ssid_wpa_5g_br", passkey="something", security="wpa", station_name=['sta0000'])
    # obj.dataplane(station_name=["sta0000"])
    # a = obj.staConnect.json_get("/events/since/")
    # print(a)
    # print(obj.eap_connect.json_get("port/1/1/sta0000?fields=ap,ip"))
    # obj.EAP_Connect(station_name=["sta0000", "sta0001"], eap="TTLS", ssid="testing_radius")
