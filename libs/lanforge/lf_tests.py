#########################################################################################################
# Used by Nightly_Sanity
# This has different types of old_pytest like Single client connectivity, Single_Client_EAP, testrail_retest
#########################################################################################################
import sys
import os

import allure

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
sys.path.append(f'../libs/lanforge/')
from sta_connect2 import StaConnect2
import time
# from eap_connect import EAPConnect
from test_ipv4_ttls import TTLSTest
from lf_wifi_capacity_test import WiFiCapacityTest
from create_station import CreateStation
import lf_ap_auto_test
import lf_dataplane_test
from lf_dataplane_test import DataplaneTest
from lf_ap_auto_test import ApAutoTest
from csv_to_influx import CSVtoInflux
from influx2 import RecordInflux


class RunTest:

    def __init__(self, lanforge_data=None, local_report_path="../reports/", influx_params=None, debug=False):
        self.lanforge_ip = lanforge_data["ip"]
        self.lanforge_port = lanforge_data["port"]
        self.twog_radios = lanforge_data["2.4G-Radio"]
        self.fiveg_radios = lanforge_data["5G-Radio"]
        self.ax_radios = lanforge_data["AX-Radio"]
        self.upstream_port = lanforge_data["upstream"].split(".")[2]
        self.twog_prefix = lanforge_data["2.4G-Station-Name"]
        self.fiveg_prefix = lanforge_data["5G-Station-Name"]
        self.ax_prefix = lanforge_data["AX-Station-Name"]
        self.debug = debug
        self.lf_ssh_port = lanforge_data["ssh_port"]
        self.staConnect = None
        self.dataplane_obj = None
        self.dualbandptest_obj = None
        self.influx_params = influx_params
        self.influxdb = RecordInflux(_influx_host=influx_params["influx_host"],
                                     _influx_port=influx_params["influx_port"],
                                     _influx_org=influx_params["influx_org"],
                                     _influx_token=influx_params["influx_token"],
                                     _influx_bucket=influx_params["influx_bucket"])
        self.local_report_path = local_report_path
        if not os.path.exists(self.local_report_path):
            os.mkdir(self.local_report_path)
        # self.staConnect = StaConnect2(self.lanforge_ip, self.lanforge_port, debug_=self.debug)

    def Client_Connectivity(self, ssid="[BLANK]", passkey="[BLANK]", security="open", extra_securities=[],
                            station_name=[], mode="BRIDGE", vlan_id=1, band="twog"):
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
            self.staConnect.radio = self.twog_radios[0]
            self.staConnect.sta_prefix = self.twog_prefix
        if band == "fiveg":
            self.staConnect.radio = self.fiveg_radios[0]
            self.staConnect.sta_prefix = self.fiveg_prefix
        self.staConnect.resource = 1
        self.staConnect.dut_ssid = ssid
        self.staConnect.dut_passwd = passkey
        self.staConnect.dut_security = security
        self.staConnect.station_names = station_name
        self.staConnect.runtime_secs = 40
        self.staConnect.bringup_time_sec = 80
        self.staConnect.cleanup_on_exit = True
        # self.staConnect.cleanup()
        self.staConnect.setup(extra_securities=extra_securities)
        self.staConnect.start()
        print("napping %f sec" % self.staConnect.runtime_secs)
        time.sleep(self.staConnect.runtime_secs)
        for sta_name in self.staConnect.station_names:
            try:
                station_data_str = ""
                sta_url = self.staConnect.get_station_url(sta_name)
                station_info = self.staConnect.json_get(sta_url)
                for i in station_info["interface"]:
                    try:
                        station_data_str = station_data_str + i + "  :  " + str(station_info["interface"][i]) + "\n"
                    except Exception as e:
                        print(e)
                allure.attach(name=str(sta_name), body=str(station_data_str))
            except Exception as e:
                print(e)
        self.staConnect.stop()
        self.staConnect.cleanup()
        run_results = self.staConnect.get_result_list()
        for result in run_results:
            print("test result: " + result)
        result = True
        print("Client Connectivity :", self.staConnect.passes)
        if self.staConnect.passes():
            print("client connection to", self.staConnect.dut_ssid, "successful. Test Passed")
        else:
            print("client connection to", self.staConnect.dut_ssid, "unsuccessful. Test Failed")
            result = False
        time.sleep(3)
        return self.staConnect.passes(), result

    def EAP_Connect(self, ssid="[BLANK]", passkey="[BLANK]", security="wpa2", extra_securities=[],
                    mode="BRIDGE", band="twog", vlan_id=100,
                    station_name=[], key_mgmt="WPA-EAP",
                    pairwise="NA", group="NA", wpa_psk="DEFAULT",
                    ttls_passwd="nolastart", ieee80211w=1,
                    wep_key="NA", ca_cert="NA", eap="TTLS", identity="nolaradius"):
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
            self.eap_connect.radio = self.twog_radios[0]
            # self.eap_connect.sta_prefix = self.twog_prefix
        if band == "fiveg":
            self.eap_connect.radio = self.fiveg_radios[0]
            # self.eap_connect.sta_prefix = self.fiveg_prefix
        # self.eap_connect.resource = 1
        if eap == "TTLS":
            self.eap_connect.ieee80211w = ieee80211w
            self.eap_connect.key_mgmt = key_mgmt
            self.eap_connect.station_profile.set_command_flag("add_sta", "80211u_enable", 0)
            self.eap_connect.identity = identity
            self.eap_connect.ttls_passwd = ttls_passwd
            self.eap_connect.pairwise = pairwise
            self.eap_connect.group = group
        if eap == "TLS":
            self.eap_connect.key_mgmt = "WPA-EAP-SUITE-B"
            self.eap_connect.station_profile.set_command_flag("add_sta", "80211u_enable", 0)
            self.eap_connect.pairwise = "TKIP"
            self.eap_connect.group = "TKIP"
            self.eap_connect.eap = "EAP-TLS"

        # self.eap_connect.hs20_enable = False
        self.eap_connect.ssid = ssid
        self.eap_connect.password = passkey
        self.eap_connect.security = security
        self.eap_connect.sta_list = station_name
        self.eap_connect.build(extra_securities=extra_securities)
        self.eap_connect.start(station_name, True, True)
        for sta_name in station_name:
            # try:
            station_data_str = ""
            # sta_url = self.eap_connect.get_station_url(sta_name)
            # station_info = self.eap_connect.json_get(sta_url)
            station_info = self.eap_connect.json_get("port/1/1/" + sta_name)
            for i in station_info["interface"]:
                try:
                    station_data_str = station_data_str + i + "  :  " + str(station_info["interface"][i]) + "\n"
                except Exception as e:
                    print(e)
            allure.attach(name=str(sta_name), body=str(station_data_str))
            # except Exception as e:
            #     print(e)

        self.eap_connect.stop()
        endp_data = []
        for i in self.eap_connect.resulting_endpoints:
            endp_data.append(self.eap_connect.resulting_endpoints[i]["endpoint"])
        cx_data = ""
        for i in endp_data:
            for j in i:
                cx_data = cx_data + str(j) + " : " + str(i[j]) + "\n"
            cx_data = cx_data + "\n"
        allure.attach(name="cx_data", body=str(cx_data))
        self.eap_connect.cleanup(station_name)
        return self.eap_connect.passes()

    def wifi_capacity(self, mode="BRIDGE", vlan_id=100, instance_name="wct_instance", download_rate="1Gbps",
                      upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000"):
        if mode == "BRIDGE":
            upstream_port = self.upstream_port
        elif mode == "NAT":
            upstream_port = self.upstream_port
        elif mode == "VLAN":
            upstream_port = self.upstream_port + "." + str(vlan_id)
        '''SINGLE WIFI CAPACITY using lf_wifi_capacity.py'''
        wificapacity_obj = WiFiCapacityTest(lfclient_host=self.lanforge_ip,
                                            lf_port=self.lanforge_port,
                                            lf_user="lanforge",
                                            lf_password="lanforge",
                                            local_lf_report_dir=self.local_report_path,
                                            instance_name=instance_name,
                                            config_name="wifi_config",
                                            upstream="1.1." + upstream_port,
                                            batch_size="1,5,10,20,40,64",
                                            loop_iter="1",
                                            protocol=protocol,
                                            duration=duration,
                                            pull_report=True,
                                            load_old_cfg=False,
                                            upload_rate=upload_rate,
                                            download_rate=download_rate,
                                            sort="interleave",
                                            # stations=stations,
                                            create_stations=True,
                                            radio=None,
                                            security=None,
                                            paswd=None,
                                            ssid=None,
                                            enables=[],
                                            disables=[],
                                            raw_lines=[],
                                            raw_lines_file="",
                                            sets=[])

        wificapacity_obj.setup()
        wificapacity_obj.run()

        report_name = wificapacity_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        influx = CSVtoInflux(influxdb=self.influxdb, _influx_tag=self.influx_params["influx_tag"],
                             target_csv=self.local_report_path + report_name + "/kpi.csv")
        influx.post_to_influx()
        return wificapacity_obj

    def Client_Connect(self, ssid="[BLANK]", passkey="[BLANK]", security="wpa2", mode="BRIDGE", band="twog",
                       vlan_id=100,
                       station_name=[]):

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
        self.client_connect.build()
        self.client_connect.wait_for_ip(station_name)
        print(self.client_connect.wait_for_ip(station_name))
        if self.client_connect.wait_for_ip(station_name):
            self.client_connect._pass("ALL Stations got IP's", print_=True)
            return self.client_connect
        else:
            return False

    def Client_disconnect(self, station_name=[]):
        self.client_dis = CreateStation(_host=self.lanforge_ip, _port=self.lanforge_port,
                                        _sta_list=station_name, _password="passkey", _ssid="ssid", _security="security")
        self.client_dis.station_profile.cleanup(station_name)
        return True

    def dataplane(self, station_name=None, mode="BRIDGE", vlan_id=100, download_rate="85%", dut_name="TIP",
                  upload_rate="85%", duration="1m", instance_name="test_demo", raw_lines=None):
        if mode == "BRIDGE":
            self.client_connect.upstream_port = self.upstream_port
        elif mode == "NAT":
            self.client_connect.upstream_port = self.upstream_port
        elif mode == "VLAN":
            self.client_connect.upstream_port = self.upstream_port + "." + str(vlan_id)

        if raw_lines is None:
            raw_lines = [['pkts: MTU'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types: UDP;TCP'],
                         ["show_3s: 1"], ["show_ll_graphs: 1"], ["show_log: 1"]]

        self.dataplane_obj = DataplaneTest(lf_host=self.lanforge_ip,
                                           lf_port=self.lanforge_port,
                                           ssh_port=self.lf_ssh_port,
                                           local_path=self.local_report_path,
                                           lf_user="lanforge",
                                           lf_password="lanforge",
                                           instance_name=instance_name,
                                           config_name="dpt_config",
                                           upstream="1.1." + self.upstream_port,
                                           pull_report=True,
                                           load_old_cfg=False,
                                           download_speed=download_rate,
                                           upload_speed=upload_rate,
                                           duration=duration,
                                           dut=dut_name,
                                           station="1.1." + station_name[0],
                                           raw_lines=raw_lines)

        self.dataplane_obj.setup()
        self.dataplane_obj.run()
        report_name = self.dataplane_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        influx = CSVtoInflux(influxdb=self.influxdb, _influx_tag=self.influx_params["influx_tag"],
                             target_csv=self.local_report_path + report_name + "/kpi.csv")
        influx.post_to_influx()

        return self.dataplane_obj

    def dualbandperformancetest(self, ssid_5G="[BLANK]", ssid_2G="[BLANK]", mode="BRIDGE", vlan_id=100, dut_name="TIP",
                                instance_name="test_demo"):
        if mode == "BRIDGE":
            self.client_connect.upstream_port = self.upstream_port
        elif mode == "NAT":
            self.client_connect.upstream_port = self.upstream_port
        else:
            self.client_connect.upstream_port = self.upstream_port + "." + str(vlan_id)

        self.dualbandptest_obj = ApAutoTest(lf_host=self.lanforge_ip,
                                            lf_port=self.lanforge_port,
                                            lf_user="lanforge",
                                            lf_password="lanforge",
                                            instance_name=instance_name,
                                            config_name="dbp_config",
                                            upstream="1.1." + self.upstream_port,
                                            pull_report=True,
                                            dut5_0=dut_name + ' ' + ssid_5G,
                                            dut2_0=dut_name + ' ' + ssid_2G,
                                            load_old_cfg=False,
                                            max_stations_2=1,
                                            max_stations_5=1,
                                            max_stations_dual=2,
                                            radio2=[["1.1.wiphy0"]],
                                            radio5=[["1.1.wiphy1"]],
                                            sets=[['Basic Client Connectivity', '0'], ['Multi Band Performance', '1'],
                                                  ['Throughput vs Pkt Size', '0'], ['Capacity', '0'],
                                                  ['Stability', '0'],
                                                  ['Band-Steering', '0'], ['Multi-Station Throughput vs Pkt Size', '0'],
                                                  ['Long-Term', '0']]
                                            )
        self.dualbandptest_obj.setup()
        self.dualbandptest_obj.run()
        report_name = self.dataplane_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        influx = CSVtoInflux(influxdb=self.influxdb,
                             _influx_tag=self.influx_params["influx_tag"],
                             target_csv=self.local_report_path + report_name + "/kpi.csv")
        influx.post_to_influx()
        return self.dualbandptest_obj


if __name__ == '__main__':
    lanforge_data = {
        "ip": "localhost",
        "port": 8801,
        "ssh_port": 22,
        "2.4G-Radio": ["wiphy0"],
        "5G-Radio": ["wiphy1"],
        "AX-Radio": ["wiphy2"],
        "upstream": "1.1.eth1",
        "2.4G-Station-Name": "wlan0",
        "5G-Station-Name": "wlan0",
        "AX-Station-Name": "ax",
    }
    obj = RunTest(lanforge_data=lanforge_data, debug=False)
    # a = obj.staConnect.json_get("/events/since/")
    # print(a)
    # print(obj.eap_connect.json_get("port/1/1/sta0000?fields=ap,ip"))
    # obj.EAP_Connect(station_name=["sta0000", "sta0001"], eap="TTLS", ssid="testing_radius")
