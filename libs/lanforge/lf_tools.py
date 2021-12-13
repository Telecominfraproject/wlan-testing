import re
import sys
import os

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
import allure
from sta_connect2 import StaConnect2
from create_chamberview import CreateChamberview
from create_chamberview_dut import DUT
import time
from LANforge.lfcli_base import LFCliBase
import json
import os
import pandas as pd


class ChamberView:

    def __init__(self, lanforge_data=None, access_point_data=None, debug=True, testbed=None):
        print("lanforge data",lanforge_data)
        print("access point data", access_point_data)
        self.access_point_data = access_point_data
        print("testbed", testbed)
        if "type" in lanforge_data.keys():
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
                self.delete_old_scenario = True
                self.debug = debug
                self.testbed = "mesh"
                self.scenario_name = "TIP-" + self.testbed
                self.raw_line = [
                    ["profile_link " + self.upstream_resource_1 + " upstream-dhcp 1 NA NA " + self.upstream_port_1.split(".")[2] + ",AUTO -1 NA"],
                    ["profile_link " + self.uplink_resource_1 + " uplink-nat 1 'DUT: upstream LAN " + self.upstream_subnet + "' NA " + self.uplink_port_1.split(".")[2] + "," + self.upstream_port_1.split(".")[2] + " -1 NA"]
                    ]
                self.CreateChamberview = CreateChamberview(self.lanforge_ip, self.lanforge_port)
        else:
            self.lanforge_ip = lanforge_data["ip"]
            self.lanforge_port = lanforge_data["port"]
            self.twog_radios = lanforge_data["2.4G-Radio"]
            self.fiveg_radios = lanforge_data["5G-Radio"]
            self.ax_radios = lanforge_data["AX-Radio"]
            self.upstream_port = lanforge_data["upstream"]
            self.twog_prefix = lanforge_data["2.4G-Station-Name"]
            self.fiveg_prefix = lanforge_data["5G-Station-Name"]
            self.ax_prefix = lanforge_data["AX-Station-Name"]
            self.uplink_port = lanforge_data["uplink"]  # eth2
            self.upstream_subnet = lanforge_data["upstream_subnet"]
            self.testbed = testbed
            self.upstream_resources = self.upstream_port.split(".")[0] + "." + self.upstream_port.split(".")[1]
            self.uplink_resources = self.uplink_port.split(".")[0] + "." + self.uplink_port.split(".")[1]
            self.delete_old_scenario = True
            # For chamber view
            self.scenario_name = "TIP-" + self.testbed
            self.debug = debug
            self.exit_on_error = False
            self.dut_idx_mapping = {}
            self.ssid_list = []
            self.staConnect = StaConnect2(self.lanforge_ip, self.lanforge_port, debug_=self.debug)
            self.raw_line = [
            ["profile_link " + self.upstream_resources + " upstream-dhcp 1 NA NA " + self.upstream_port.split(".")
            [2] + ",AUTO -1 NA"],
            ["profile_link " + self.uplink_resources + " uplink-nat 1 'DUT: upstream LAN " + self.upstream_subnet
             + "' NA " + self.uplink_port.split(".")[2] + "," + self.upstream_port.split(".")[2] + " -1 NA"]
            ]

            # This is for rawline input | see create_chamberview_dut.py for more details

            self.CreateChamberview = CreateChamberview(self.lanforge_ip, self.lanforge_port)

            if access_point_data:
                # for DUT
                self.dut_name = testbed
                self.ap_model = access_point_data[0]["model"]
                self.version = access_point_data[0]["version"].split("/")[-1]
                self.serial = access_point_data[0]["serial"]

                self.CreateDut = DUT(lfmgr=self.lanforge_ip,
                                     port=self.lanforge_port,
                                     dut_name=self.testbed,
                                     sw_version=self.version,
                                     hw_version=self.ap_model,
                                     model_num=self.ap_model,
                                     serial_num=self.serial
                                     )
                self.CreateDut.ssid = []

    def reset_scenario(self):
        self.raw_line = [
            ["profile_link " + self.upstream_resources + " upstream-dhcp 1 NA NA " + self.upstream_port.split(".")
            [2] + ",AUTO -1 NA"],
            ["profile_link " + self.uplink_resources + " uplink-nat 1 'DUT: upstream LAN " + self.upstream_subnet
             + "' NA " + self.uplink_port.split(".")[2] + "," + self.upstream_port.split(".")[2] + " -1 NA"]
        ]
        print(self.raw_line)
        self.Chamber_View()

    def reset_dut(self):
        temp = []
        for i in range(0, 8):
            temp.append(['ssid_idx=' + str(i) + ' ssid=-'])
        print(temp)
        self.CreateDut.ssid = temp
        self.CreateDut.add_ssids()

    def get_station_list(self):
        realm_obj = self.staConnect.localrealm
        sta = realm_obj.station_list()
        sta_list = []
        for i in sta:
            for j in i:
                sta_list.append(j)
        return sta_list

    def admin_up_down(self, sta_list=[], option="up"):
        realm_obj = self.staConnect.localrealm
        if option == "up":
            for i in sta_list:
                realm_obj.admin_up(i)
                time.sleep(0.005)
        elif option == "down":
            for j in sta_list:
                realm_obj.admin_down(j)
                time.sleep(0.005)
        time.sleep(2)

    def Chamber_View(self):
        if self.delete_old_scenario:
            self.CreateChamberview.clean_cv_scenario(type="Network-Connectivity", scenario_name=self.scenario_name)
        self.CreateChamberview.setup(create_scenario=self.scenario_name,
                                     raw_line=self.raw_line
                                     )
        self.CreateChamberview.build(self.scenario_name)
        self.CreateChamberview.sync_cv()
        time.sleep(2)
        self.CreateChamberview.show_text_blob(None, None, True)  # Show changes on GUI
        self.CreateChamberview.sync_cv()
        return self.CreateChamberview, self.scenario_name

    def add_vlan(self, vlan_ids=[]):
        data = self.staConnect.json_get("/port/all")
        flag = 0
        for vlans in vlan_ids:
            for i in data["interfaces"]:
                if list(i.keys())[0] != self.upstream_port + "." + str(vlans):
                    flag = 1
        if flag == 1:
            for vlans in vlan_ids:
                self.raw_line.append(["profile_link 1.1 " + "vlan-100 1 " + self.upstream_port
                                      + " NA " + self.upstream_port.split(".")[2] + ",AUTO -1 " + str(vlans)])
            self.Chamber_View()

    def add_stations(self, band="2G", num_stations="max", dut="NA", ssid_name=[]):
        idx = 0
        print(self.dut_idx_mapping)
        for i in self.dut_idx_mapping:
            if self.dut_idx_mapping[i][0] == ssid_name and self.dut_idx_mapping[i][3] == band:
                idx = i
        max_stations = 0
        print(idx)
        if band == "2G":
            if num_stations != "max":
                if num_stations > 64:
                    num_stations = int(num_stations / len(self.twog_radios))
                    for radio in self.twog_radios:
                        station_data = ["profile_link " + radio.split(".")[0] + "." + radio.split(".")[1] +
                                        " STA-AUTO " + str(num_stations) + " 'DUT: " + dut + " Radio-" +
                                        str(int(idx) + 1) + "'" + " NA " + radio.split(".")[2]]
                        self.raw_line.append(station_data)
                else:
                    num_stations = num_stations
                    station_data = ["profile_link " + self.fiveg_radios[0].split(".")[0] + "." +
                                    self.fiveg_radios[0].split(".")[1] +
                                    " STA-AUTO " + str(num_stations) + " 'DUT: " + dut + " Radio-" +
                                    str(int(idx) + 1) + "'" + " NA " + self.twog_radios[0].split(".")[2]]
                    self.raw_line.append(station_data)
            if num_stations == "max":
                for radio in self.twog_radios:
                    num_stations = 64
                    station_data = ["profile_link " + radio.split(".")[0] + "." + radio.split(".")[1] +
                                    " STA-AUTO " + str(num_stations) + " 'DUT: " + dut + " Radio-" +
                                    str(int(idx) + 1) + "'" + " NA " + radio.split(".")[2]]
                    self.raw_line.append(station_data)

        if band == "5G":
            if num_stations != "max":
                if num_stations > 64:
                    num_stations = int(num_stations / len(self.fiveg_radios))
                    for radio in self.fiveg_radios:
                        station_data = ["profile_link " + radio.split(".")[0] + "." + radio.split(".")[1] +
                                        " STA-AUTO " + str(num_stations) + " 'DUT: " + dut + " Radio-" +
                                        str(int(idx) + 1) + "'" + " NA " + radio.split(".")[2]]
                        print(station_data)
                        self.raw_line.append(station_data)
                else:
                    num_stations = num_stations
                    station_data = ["profile_link " + self.fiveg_radios[0].split(".")[0] + "." +
                                    self.fiveg_radios[0].split(".")[1] +
                                    " STA-AUTO " + str(num_stations) + " 'DUT: " + dut + " Radio-" +
                                    str(int(idx) + 1) + "'" + " NA " + self.fiveg_radios[0].split(".")[2]]
                    print(station_data)
                    self.raw_line.append(station_data)
            if num_stations == "max":
                for radio in self.fiveg_radios:
                    num_stations = 64
                    station_data = ["profile_link " + radio.split(".")[0] + "." + radio.split(".")[1] +
                                    " STA-AUTO " + str(num_stations) + " 'DUT: " + dut + " Radio-" +
                                    str(int(idx) + 1) + "'" + " NA " + radio.split(".")[2]]
                    print(station_data)
                    self.raw_line.append(station_data)

        if band == "ax":
            if num_stations != "max":
                if num_stations > 1:
                    num_stations = int(num_stations / len(self.ax_radios))
                    for radio in self.ax_radios:
                        station_data = ["profile_link 1.1 STA-AUTO " + str(num_stations) + " 'DUT: " + dut + " Radio-" +
                                        str(int(idx) + 1) + "'" + " NA " + radio]
                        self.raw_line.append(station_data)
                else:
                    num_stations = num_stations
                    station_data = ["profile_link 1.1 STA-AUTO " + str(num_stations) + " 'DUT: " + dut + " Radio-" +
                                    str(int(idx) + 1) + "'" + " NA " + self.ax_radios[0]]
                    self.raw_line.append(station_data)
            if num_stations == "max":
                for radio in self.ax_radios:
                    num_stations = 1
                    station_data = ["profile_link 1.1 STA-AUTO " + str(num_stations) + " 'DUT: " + dut + " Radio-" +
                                    str(int(idx) + 1) + "'" + " NA " + radio]
                    self.raw_line.append(station_data)

    def Create_Dut(self):
        self.CreateDut.setup()
        self.CreateDut.add_ssids()
        self.CreateDut.cv_test.show_text_blob(None, None, True)  # Show changes on GUI
        self.CreateDut.cv_test.sync_cv()
        time.sleep(2)
        self.CreateDut.cv_test.show_text_blob(None, None, True)  # Show changes on GUI
        self.CreateDut.cv_test.sync_cv()
        return self.CreateDut, self.dut_name

    def update_ssid(self, ssid_data=[]):
        self.CreateDut.ssid = ssid_data
        self.CreateDut.add_ssids()
        # SSID data should be in this format
        # [
        # ['ssid_idx=0 ssid=Default-SSID-2g security=WPA|WEP| password=12345678 bssid=90:3c:b3:94:48:58'],
        # ['ssid_idx=1 ssid=Default-SSID-5gl password=12345678 bssid=90:3c:b3:94:48:59']
        #  ]
        pass

    def json_get(self, _req_url="/"):
        cli_base = LFCliBase(_lfjson_host=self.lanforge_ip, _lfjson_port=self.lanforge_port, )
        json_response = cli_base.json_get(_req_url=_req_url)
        return json_response

    def json_post(self, req_url, shelf, resources, port, current, intrest):
        data = {
            "shelf": shelf,
            "resource": resources,
            "port": port,
            "current_flags": current,
            "interest": intrest
        }
        cli_base = LFCliBase(_lfjson_host=self.lanforge_ip, _lfjson_port=self.lanforge_port, )
        return cli_base.json_post(req_url, data)

    def read_kpi_file(self, column_name, dir_name):
        if column_name == None:
            df = pd.read_csv("../reports/" + str(dir_name) + "/kpi.csv", sep=r'\t', engine='python')
            if df.empty == True:
                return "empty"
            else:
                return df
        else:
            df = pd.read_csv("../reports/" + str(dir_name) + "/kpi.csv", sep=r'\t', usecols=column_name,
                             engine='python')
            if df.empty == True:
                return "empty"
            else:
                result = df[column_name].values.tolist()
                return result

    def read_csv_individual_station_throughput(self, dir_name, option):
        try:
            df = pd.read_csv("../reports/" + str(dir_name) + "/csv-data/data-Combined_bps__60_second_running_average-1.csv", sep=r'\t', engine='python')
            print("csv file opened")
        except FileNotFoundError:
            print("csv file does not exist")
            return False

        dict_data = {}
        if option == "download":
            csv_sta_names = df.iloc[[0]].values.tolist()
            csv_throughput_values = df.iloc[[1]].values.tolist()
        elif option == "upload":
            csv_sta_names = df.iloc[[0]].values.tolist()
            csv_throughput_values = df.iloc[[2]].values.tolist()
        else:
            print("Provide proper option: download or upload")
            return

        sta_list = csv_sta_names[0][0][:-1].replace('"', '').split(",")
        th_list = list(map(float, csv_throughput_values[0][0].split(",")))
        for i in range(len(sta_list)):
            dict_data[sta_list[i]] = th_list[i]

        return dict_data

    def attach_report_graphs(self, report_name=None, pdf_name="WIFI Capacity Test PDF Report"):
        relevant_path = "../reports/" + report_name + "/"
        entries = os.listdir("../reports/" + report_name + '/')
        pdf = False
        for i in entries:
            if ".pdf" in i:
                pdf = i
        if pdf:
            allure.attach.file(source=relevant_path + pdf,
                               name=pdf_name)

        included_extensions = ['png']
        file_names = [fn for fn in os.listdir(relevant_path)
                      if any(fn.endswith(ext) for ext in included_extensions)]

        a = [item for item in file_names if 'print' not in item]
        a = [item for item in a if 'logo' not in item]
        a = [item for item in a if 'Logo' not in item]
        a = [item for item in a if 'candela' not in item]

        a.sort()
        for i in a:
            allure.attach.file(source=relevant_path + i,
                               name=i,
                               attachment_type="image/png", extension=None)

    def create_mesh(self):
        upstream_list = []
        for data in range(0,len(self.access_point_data)):
            self.CreateDut = DUT(lfmgr=self.lanforge_ip,
                                 port=self.lanforge_port,
                                 dut_name="upstream" + str(data))
            self.CreateDut.lan_port = "10.28.2.1/24"
            name = "upstream" + str(data)
            upstream_list.append(name)

            self.CreateDut.setup()
            data  = data + 1
        self.raw_line = [
            ["profile_link " + self.upstream_resource_2 + " upstream-dhcp 1 NA NA " + self.upstream_port_2.split(".")[2] + ",AUTO -1 NA"],
            ["profile_link " + self.uplink_resource_2 + " uplink-nat 1 'DUT: " + str(upstream_list[0]) +  " LAN " + self.upstream_subnet + "' NA " + self.uplink_port_2.split(".")[2] + "," + self.upstream_port_2.split(".")[2] + " -1 NA"],
            ["profile_link " + self.upstream_resource_3 + " upstream-dhcp 1 NA NA " + self.upstream_port_3.split(".")[2] + ",AUTO -1 NA"],
            ["profile_link " + self.uplink_resource_3 + " uplink-nat 1 'DUT: " + str(upstream_list[1]) +  " LAN " + self.upstream_subnet + "' NA " + self.uplink_port_3.split(".")[2] + "," + self.upstream_port_3.split(".")[2] + " -1 NA"],
            ["profile_link " + self.upstream_resource_4 + " upstream-dhcp 1 NA NA " + self.upstream_port_4.split(".")[2] + ",AUTO -1 NA"],
            ["profile_link " + self.uplink_resource_4 + " uplink-nat 1 'DUT: " + str(upstream_list[2]) +  " LAN " + self.upstream_subnet + "' NA " + self.uplink_port_4.split(".")[2] + "," + self.upstream_port_4.split(".")[2] + " -1 NA"]
        ]
        print(self.raw_line)
        mesh = self.Chamber_View()
        return mesh

    def create_mesh_dut(self):
        for ap in self.access_point_data:
            # print(ap)
            self.dut_name = ap["type"]
            print(self.dut_name)
            self.ap_model = ap["model"]
            self.version = ap["version"].split("/")[-1]
            self.serial = ap["serial"]
            self.CreateDut = DUT(lfmgr=self.lanforge_ip,
                                 port=self.lanforge_port,
                                 dut_name=self.dut_name,
                                 hw_version=self.ap_model,
                                 model_num=self.ap_model,
                                 serial_num=self.serial
                                 )
            self.Create_Dut()

def main():
    # lanforge_data = {'ip': 'localhost', 'port': 8802, 'ssh_port': 8804, '2.4G-Radio': ['1.1.wiphy0', '1.1.wiphy2'], '5G-Radio': ['1.1.wiphy1', '1.1.wiphy3'], 'AX-Radio': ['1.1.wiphy4', '1.1.wiphy5', '1.1.wiphy6', '1.1.wiphy7'], 'upstream': '1.1.eth2', 'upstream_subnet': '10.28.2.1/24', 'uplink': '1.1.eth1', '2.4G-Station-Name': 'sta00', '5G-Station-Name': 'sta10', 'AX-Station-Name': 'ax'}
    lanforge_data = {
                "type": "mesh",
                "ip": "localhost",  # 10.28.3.14
                "port": 8802,  # 8080
                "ssh_port": 8804,
                "2.4G-Radio-mobile-sta": ["1.1.wiphy0", "1.1.wiphy2"],
                "5G-Radio-mobile-sta": ["1.1.wiphy1", "1.1.wiphy3"],
                "AX-Radio-mobile-sta": ["1.1.wiphy4", "1.1.wiphy5", "1.1.wiphy6", "1.1.wiphy7"],
                "upstream-mobile-sta": "1.1.eth2",
                "upstream_subnet-mobile-sta": "10.28.2.1/24",
                "uplink-mobile-sta": "1.1.eth3",
                "2.4G-Radio-root": ["1.2.wiphy0"],
                "5G-Radio-root": ["1.2.wiphy1"],
                "AX-Radio-root": [],
                "upstream-root": "1.2.eth2",
                "upstream_subnet-root": "10.28.2.1/24",
                "uplink-root": "1.2.eth3",
                "2.4G-Radio-node-1": ["1.3.wiphy0"],
                "5G-Radio-node-1": ["1.3.wiphy1"],
                "AX-Radio-node-1": [],
                "upstream-node-1": "1.3.eth2",
                "upstream_subnet-node-1": "10.28.2.1/24",
                "uplink--node-1": "1.3.eth3",
                "2.4G-Radio-node-2": ["1.4.wiphy0"],
                "5G-Radio-node-2": ["1.4.wiphy1"],
                "AX-Radio-node-2": [],
                "upstream-node-2": "1.4.eth2",
                "upstream_subnet-node-2": "10.28.2.1/24",
                "uplink--node-2": "1.4.eth3",
                "2.4G-Station-Name": "wlan0",
                "5G-Station-Name": "wlan0",
                "AX-Station-Name": "ax"
            }
    # ap_data = [{'model': 'wf188n', 'mode': 'wifi6', 'serial': '0000c1018812', 'jumphost': True, 'ip': 'localhost', 'username': 'lanforge', 'password': 'pumpkin77', 'port': 8803, 'jumphost_tty': '/dev/ttyAP1', 'version': 'https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/uCentral/cig_wf188/20210729-cig_wf188-v2.0.0-rc2-ec3662e-upgrade.bin'}]
    ap_data = [
            {
                'type' : 'root',
                'model': 'eap101',
                'mode': 'wifi6',
                'serial': '34efb6af4a7a',
                'jumphost': True,
                'ip': "localhost",  # 10\.28\.3\.101
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 8803,  # 22
                'jumphost_tty': '/dev/ttyAP2',
                'version': "latest"
            },
            {
                'type': 'node-1',
                'model': 'eap101',
                'mode': 'wifi6',
                'serial': '34efb6af4903',
                'jumphost': True,
                'ip': "localhost", #10\.28\.3\.101
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 8803,  # 22
                'jumphost_tty': '/dev/ttyAP3',
                'version': "latest"
            },
            {
                'type' : 'node-2',
                'model': 'eap102',
                'mode': 'wifi6',
                'serial': '34efb6af4a7a',
                'jumphost': True,
                'ip': "localhost",  # 10\.28\.3\.101
                'username': "lanforge",
                'password': "pumpkin77",
                'port': 8803,  # 22
                'jumphost_tty': '/dev/ttyAP4',
                'version': "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/eap101/trunk/eap101-1.1.0.tar.gz"
            }
        ]
    testbed = "mesh"
    obj = ChamberView(lanforge_data=lanforge_data, access_point_data=ap_data, testbed="mesh")
    obj.create_mesh_dut()
    obj.create_mesh()

if __name__ == '__main__':
    main()