import sys
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

import logging
import importlib
import subprocess
import os

sys.path.append(os.path.join(os.path.abspath("../../../lanforge/lanforge-scripts/")))
logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

class CController:
    def __init__(self, controller_data, ap_data=None, timeout=None, ssid_data=None, type=None):
        self.controller_data = controller_data
        self.ap_data = ap_data
        self.type = type
        print("type", type)
        print(self.ap_data)
        self.ip = self.controller_data["ip"]
        self.user = self.controller_data["username"]
        self.password = self.controller_data["password"]
        self.port = self.controller_data["ssh_port"]
        self.type = self.controller_data["series"]
        self.prompt = self.controller_data["prompt"]
        # for i in range(controller_data["ap_name"]):
        #     self.ap_name = self.controller_data["ap_name"][i]
        # for band in range(controller_data["band"]):
        #     self.band = self.controller_data["band"][i]
        # self.ap_name = self.controller_data["ap_name"][0]["ap_name"]   # hard coded
        self.ap_name = None
        if self.ap_name == None:
            self.ap_name = self.ap_data[0]['ap_name']
        if type == 0:
            print("yes")
            self.ap_name = self.ap_data[0]['ap_name']
            print(self.ap_data[0]['ap_name'])
        if type == 1:
            self.ap_name = self.ap_data[1]['ap_name']
            print(self.ap_data[1]['ap_name'])

        print("ap_name ", self.ap_name)
        self.band = self.controller_data["band"][0]

        self.scheme = self.controller_data["scheme"]
        self.timeout = timeout
        self.ssid_data= ssid_data
        print("ssid data", self.ssid_data)

        series = importlib.import_module("cc_module_9800_3504")
        self.cc = series.create_controller_series_object(
                    scheme=self.scheme,
                    dest=self.ip,
                    user=self.user,
                    passwd=self.password,
                    prompt=self.prompt,
                    series=self.type,
                    ap=self.ap_name,
                    port=self.port,
                    band=self.band,
                    timeout=self.timeout)
        self.cc.bandwidth = None
        if ssid_data is None:
            self.cc.wlan = None
            self.cc.wlanID = None
            self.cc.wlanSSID = None
            self.cc.security_key = None
        else:
            for i in range(len(ssid_data)):
                print(i)
                if ssid_data[i]["appliedRadios"] == ["2G"]:
                    self.cc.wlan = ssid_data[i]['ssid_name']
                    self.cc.wlanID = "1"
                    self.cc.wlanSSID = ssid_data[i]['ssid_name']
                    self.cc.security_key = ssid_data[i]['security_key']
                    print("ss", self.cc.wlan)
                elif ssid_data[i]["appliedRadios"] == ["5G"]:
                    self.cc.wlan = ssid_data[i]['ssid_name']
                    self.cc.wlanID = "2"  # hard coded
                    self.cc.wlanSSID = ssid_data[i]['ssid_name']
                    self.cc.security_key = ssid_data[i]['security_key']
                    print("ss", self.cc.wlan)
                elif ssid_data[i]["appliedRadios"] == ["6G"]:
                    self.cc.wlan = ssid_data[i]['ssid_name']
                    self.cc.wlanID = "3"
                    self.cc.wlanSSID = ssid_data[i]['ssid_name']
                    self.cc.security_key = ssid_data[i]['security_key']

        self.cc.wlanpw = None
        if type == 0:
            self.cc.tag_policy = self.ap_data[0]['tag_policy']
            self.cc.policy_profile = self.ap_data[0]['policy_profile']
        if type == 1:
            self.cc.tag_policy = self.ap_data[1]['tag_policy']
            self.cc.policy_profile = self.ap_data[1]['policy_profile']
        self.cc.tx_power = None
        self.cc.channel = None
        self.cc.bandwidth = None
        self.cc.action = None
        self.cc.value = None
        self.cc.command = []
        self.cc.command_extend = []
        self.cc.info = "Cisco 9800 Controller Series"
        self.cc.pwd = "../lanforge/lanforge-scripts"


    def no_logging_console(self):
        log = self.cc.no_logging_console()
        print(log)
        return log

    def line_console(self):
        line = self.cc.line_console_0()
        return line

    def show_shutdown_5ghz_ap(self):
        self.cc.ap_band_slot = "2"
        fiveghz = self.cc.show_ap_dot11_5gz_shutdown()
        print(fiveghz)
        return fiveghz

    def show_shutdown_2ghz_ap(self):
        fiveghz = self.cc.show_ap_dot11_24gz_shutdown()
        return fiveghz

    def show_shutdown_6ghz_ap(self):
        self.cc.ap_band_slot = "3"
        sixg = self.cc.show_ap_dot11_6gz_shutdown()
        print(sixg)
        return sixg


    def disable_wlan(self, wlan):
        self.cc.wlan = wlan
        print(wlan)
        print("disable wlan")
        print("wlan", wlan)
        wlan1 = self.cc.wlan_shutdown()
        return wlan1

    def ap_5ghz_shutdown(self):
        print("shutdown 5ghz network")
        shut = self.cc.ap_dot11_5ghz_shutdown()
        return shut

    def ap_2ghz_shutdown(self):
        print("shutdown 2ghz network")
        shut = self.cc.ap_dot11_24ghz_shutdown()
        return shut

    def ap_6ghz_shutdown(self):
        print("shut down 6ghz network")
        shut = self.cc.ap_dot11_6ghz_shutdown()
        return shut

    def get_ssids(self):
        print("show ssid's present")
        wlan_summary = self.cc.show_wlan_summary()
        print(wlan_summary)
        return wlan_summary

    def delete_wlan(self, ssid):
        print("delete wlan")
        self.cc.wlan = ssid
        wlan = self.cc.config_no_wlan()
        return wlan

    def create_wlan_wpa2(self,id, wlan, wlanssid, key):
        print("create a new wpa2 wlan")
        self.cc.wlan = wlan
        self.cc.wlanID = id
        self.cc.wlanSSID = wlanssid
        self.cc.security_key = key
        ssid = self.cc.config_wlan_wpa2()
        return ssid

    def create_wlan_wpa3(self,id, wlan, wlanssid, key):
        self.cc.wlan = wlan
        self.cc.wlanID = id
        self.cc.wlanSSID = wlanssid
        self.cc.security_key = key
        ssid = self.cc.config_wlan_wpa3()
        return ssid

    def config_wireless_tag_policy_and_policy_profile(self, wlan):
        self.cc.wlan = wlan
        policy = self.cc.config_wireless_tag_policy_and_policy_profile()
        return policy

    def enable_wlan(self,  wlan):
        self.cc.wlan = wlan
        enable = self.cc.config_enable_wlan_send_no_shutdown()
        return enable

    def enable_5ghz_netwrk(self, id, wlan, wlanssid, key):
        self.cc.wlan = wlan
        self.cc.wlanID = id
        self.cc.wlanSSID = wlanssid
        self.cc.security_key = key
        en_net = self.cc.config_no_ap_dot11_5ghz_shutdown()
        return en_net

    def enable_2ghz_netwrk(self, id, wlan, wlanssid, key):
        self.cc.wlan = wlan
        self.cc.wlanID = id
        self.cc.wlanSSID = wlanssid
        self.cc.security_key = key
        en_net = self.cc.config_no_ap_dot11_24ghz_shutdown()
        return en_net

    def enable_6ghz_netwrk(self, id, wlan, wlanssid, key):
        self.cc.wlan = wlan
        self.cc.wlanID = id
        self.cc.wlanSSID = wlanssid
        self.cc.security_key = key
        en_net = self.cc.config_no_ap_dot11_6ghz_shutdown()
        return en_net

    def enable_ap_5ghz(self):
        ap = self.cc.config_ap_no_dot11_5ghz_shutdown()
        return ap

    def enable_ap_2ghz(self):
        ap = self.cc.config_ap_no_dot11_24ghz_shutdown()
        return ap

    def enable_ap_6ghz(self):
        ap = self.cc.config_ap_no_dot11_6ghz_shutdown()
        return ap


    def show_5ghz_summary(self):
        sum= self.cc.show_ap_dot11_5gz_summary()
        return sum

    def create_wlan_open(self):
        open = self.cc.config_wlan_open()
        return open

    def get_number_of_wlan_present(self):
        wlan_summary = self.cc.show_wlan_summary()
        # value = wlan_summary.decode("utf-8")
        ele_list = [y for y in (x.strip() for x in wlan_summary.splitlines()) if y]
        indices = [i for i, s in enumerate(ele_list) if 'Number of WLANs' in s]
        number = ele_list[22][17:18].strip()
        print(number, "ssid's are present")
        return number
        # do some formatting here and return actual data

    def show_5ghz_summary(self):
        pass

    def calculate_data(self, place):
        wlan_number = self.get_number_of_wlan_present()
        print(wlan_number)
        for number in range(len(wlan_number)):
            pass
        wlan_sumry = self.get_ssids()
        ele_list = [y for y in (x.strip() for x in wlan_sumry.splitlines()) if y]
        indices = [i for i, s in enumerate(ele_list) if 'Profile Name' in s]
        # print(indices)
        data = indices[1]
        data2 = data + 1
        data3 = data + 2
        data4 = data + 3
        data5 = data + 4
        acc_data = ele_list[int(data)]
        acc_data2 = ele_list[int(data2)]
        acc_data3 = ele_list[int(data3)]
        acc_data4 = ele_list[int(data4)]
        acc_data5 = ele_list[int(data5)]
        print("data 4 ",acc_data4)
        print("data 5",acc_data5)
        ident_list = []
        if acc_data == 'ID   Profile Name                     SSID                             Status Security':
            if acc_data2 == "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------":
                id_list = acc_data3.split()
                print(id_list)
                if id_list[0] == "1":
                    ident_list.append(id_list[int(place)])
                else:
                    ident_list.append("0")
                id_list2 = acc_data4.split()
                print(id_list2)
                if id_list2[0] == "2":
                    ident_list.append(id_list2[int(place)])
                else:
                    ident_list.append("0")
                id_list3 = acc_data5.split()
                print("hi",id_list3)
                if id_list3[0] == "3":
                    ident_list.append(id_list3[int(place)])
                    print("ident_list 1", ident_list)
                elif id_list2[0] == "3":
                    ident_list.append(id_list2[int(place)])
                    print("ident_list 2", ident_list)
                elif id_list[0] == "3":
                    ident_list.append(id_list[int(place)])
                    print("ident_list 3", ident_list)

                else:
                    print("ident_list", ident_list)
                    ident_list.append("0")
        else:
            print("There is no Profile name")
        # print(ident_list)
        return ident_list

    def get_ap_bssid_2g(self):
        bssid_2g = self.cc.show_ap_bssid_24ghz()
        return bssid_2g

    def get_ap_bssid_5g(self):
        bssid_5g = self.cc.show_ap_bssid_5ghz()
        return bssid_5g

    def cal_bssid_2g(self):
        wlan_sumry = self.get_ap_bssid_2g()
        print("wlan_sumry", wlan_sumry)
        ele_list = [y for y in (x.strip() for x in wlan_sumry.splitlines()) if y]
        indices = [i for i, s in enumerate(ele_list) if 'BSSID' in s]
        data = indices[1]
        data2 = data + 1
        data3 = data + 2
        data4 = data + 3
        data5 = data + 4
        data6 = data + 4
        acc_data = ele_list[int(data)]
        acc_data2 = ele_list[int(data2)]
        acc_data3 = ele_list[int(data3)]
        acc_data4 = ele_list[int(data4)]
        acc_data5 = ele_list[int(data5)]
        acc_data6 = ele_list[int(data6)]
        print(acc_data3)
        print(acc_data4)
        print(acc_data5)
        print(acc_data6)
        id_list = acc_data3.split()
        id_list1 = acc_data4.split()
        id_list2 = acc_data5.split()
        #print(id_list)
        print(id_list, id_list1, id_list2)
        wlan_id_list = []
        wlan_bssid = []
        if acc_data == "WLAN ID    BSSID":
            if acc_data2 == "-------------------------":
                if id_list[0] == "1":
                    wlan_id_list.append(id_list)
                    wlan_bssid.append(id_list[1])
                elif id_list1[0] == "1":
                    wlan_id_list.append(id_list1)
                    wlan_bssid.append(id_list1[1])
                elif id_list2[0] == "1":
                    wlan_id_list.append(id_list2)
                    wlan_bssid.append(id_list2[1])
                else:
                    print("no wlan on slot 1 present")
        y = wlan_bssid[0].replace(".", '')
        bssid = ':'.join(a + b for a, b in zip(y[::2], y[1::2]))
        return bssid

    def cal_bssid_5g(self):
        wlan_sumry = self.get_ap_bssid_5g()
        ele_list = [y for y in (x.strip() for x in wlan_sumry.splitlines()) if y]
        indices = [i for i, s in enumerate(ele_list) if 'BSSID' in s]
        data = indices[1]
        data2 = data + 1
        data3 = data + 2
        data4 = data + 3
        data5 = data + 4
        data6 = data + 5
        acc_data = ele_list[int(data)]
        acc_data2 = ele_list[int(data2)]
        acc_data3 = ele_list[int(data3)]
        acc_data4 = ele_list[int(data4)]
        acc_data5 = ele_list[int(data5)]
        acc_data6 = ele_list[int(data6)]
        id_list = acc_data3.split()
        id_list1 = acc_data4.split()
        id_list2 = acc_data5.split()
        id_list3 = acc_data6.split()
        wlan_id_list = []
        wlan_bssid = []
        if acc_data == "WLAN ID    BSSID":
            if acc_data2 == "-------------------------":

                # print(id_list)
                if id_list[0] == "2":
                    wlan_id_list.append(id_list)
                    wlan_bssid.append(id_list[1])
                elif id_list1[0] == "2":
                    wlan_id_list.append(id_list1)
                    wlan_bssid.append(id_list1[1])
                elif id_list2[0] == "2":
                    wlan_id_list.append(id_list2)
                    wlan_bssid.append(id_list2[1])
                elif id_list3[0] == "2":
                    wlan_id_list.append(id_list3)
                    wlan_bssid.append(id_list3[1])
                else:
                    print("no wlan on slot 2 present")
        y = wlan_bssid[0].replace(".", '')
        bssid = ':'.join(a + b for a, b in zip(y[::2], y[1::2]))
        return bssid


    def get_slot_id_wlan(self):
        id = self.calculate_data(place=0)
        return id

    def get_ssid_name_on_id(self):
        ssid = self.calculate_data(place=1)
        return ssid


    def show_ap_summary(self):
        summary = self.cc.show_ap_summary()
        return summary

    def show_ap_config_slots(self):
        slot = self.cc.show_ap_config_slots()
        return slot

    # gives info of ap wlan bssid and state
    def show_ap_wlan_summary(self):
        w_sum = self.cc.show_ap_wlan_summary()
        print(w_sum)
        return w_sum

    def show_11r_log(self):
        show = self.cc.show_11r_logs()
        print(show)
        return show

    def enable_ft_psk(self, ssid, key):
        self.cc.wlan = ssid
        self.cc.security_key = key
        en = self.cc.enable_ft_psk_cc()
        return en

    def enable_ft_sae(self, ssid, key):
        self.cc.wlan = ssid
        self.cc.security_key = key
        en = self.cc.enable_ft_sae_cc()
        return en

    def set_dtim_5ghz(self, wlan, value):
        self.cc.wlan = wlan
        self.value = value
        dtim = self.cc.config_dtim_dot11_5ghz()
        return dtim


if __name__ == '__main__':
    controller = {
        "url": "https://172.16.0.2",
        "ip": "localhost",
        "username": "admin",
        "password": "Cisco123",
        "ssh_port": "8888",
        "series": "9800",
        "prompt": "WLC2",
        "band": ["5g"],
        "scheme": "ssh"
    }
    access_point = [
        {
            "ap_name": "AP687D.B45C.1D1C",
            "chamber": "C1",
            "model": "cisco9136i",
            "mode": "wifi6",
            "serial": "FOC25322JQP",
            "tag_policy": "RM204-TB2-AP1",
            "policy_profile": "default-policy-profile",
            "ssid": {
                "2g-ssid": "candela2ghz",
                "5g-ssid": "open-wlan",
                "6g-ssid": "candela6ghz",
                "2g-password": "hello123",
                "5g-password": "[BLANK]",
                "6g-password": "hello123",
                "2g-encryption": "WPA2",
                "5g-encryption": "open",
                "6g-encryption": "WPA3",
                "2g-bssid": "68:7d:b4:5f:5c:31 ",
                "5g-bssid": "68:7d:b4:5f:5c:3c",
                "6g-bssid": "68:7d:b4:5f:5c:38"
            },

            "ip": "192.168.100.109",
            "username": "lanforge",
            "password": "lanforge",
            "port": 22,
            "jumphost_tty": "/dev/ttyAP1",
            "version": "17.7.1.11"
        }]
    obj = CController(controller_data=controller, ap_data=access_point, timeout="10", ssid_data=None)
    obj.get_ap_bssid_2g()
    # x = obj.get_all_ssids_from_controller()
    # print(x)
    # obj.no_logging_console()
    # obj.line_console()
    # obj.delete_wlan()
    # obj.no_logging_console()
    # obj.get_ssids()
    # obj.delete_wlan()
    # obj.create_wlan_open()
    # obj.get_ssids()
    # obj.get_number_of_wlan_present()


# if __name__ == '__main__':
#     logger_config = lf_logger_config.lf_logger_config()
#     series = importlib.import_module("cc_module_9800_3504")
#     cc = series.create_controller_series_object(
#             scheme="ssh",
#             dest="localhost",
#             user="admin",
#             passwd="xyz",
#             prompt="WLC2",
#             series="9800",
#             ap="AP2C57.4152.385C",
#             port="8888",
#             band="5g",
#             timeout="10")
#     cc.show_ap_config_slots()
#     cc.show_wlan_summary()
#
