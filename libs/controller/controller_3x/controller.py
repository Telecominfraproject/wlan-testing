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
    def __init__(self, controller_data, timeout, ssid_data=None):
        self.controller_data = controller_data
        self.ip = self.controller_data["ip"]
        self.user = self.controller_data["username"]
        self.password = self.controller_data["password"]
        self.port = self.controller_data["ssh_port"]
        self.type = self.controller_data["series"]
        self.prompt = self.controller_data["prompt"]
        self.ap_name = self.controller_data["ap_name"]
        self.band = self.controller_data["band"]
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
            self.cc.wlan = ssid_data[1]['ssid_name']
            self.cc.wlanID = "1"
            self.cc.wlanSSID = ssid_data[1]['ssid_name']
            self.cc.security_key = ssid_data[1]['security_key']
        self.cc.wlanpw = None
        self.cc.tag_policy = 'RM204-TB2'
        self.cc.policy_profile = 'default-policy-profile'
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
        fiveghz = self.cc.show_ap_dot11_5gz_shutdown()
        return fiveghz

    def disable_wlan(self):
        wlan = self.cc.wlan_shutdown()
        return wlan

    def ap_5ghz_shutdown(self):
        shut = self.cc.ap_dot11_5ghz_shutdown()
        return shut

    def get_ssids(self):
        wlan_summary = self.cc.show_wlan_summary()
        print(wlan_summary)
        return wlan_summary

    def delete_wlan(self):
        wlan = self.cc.config_no_wlan()
        return wlan

    def create_wlan_wpa2(self):
        ssid = self.cc.config_wlan_wpa2()
        return ssid

    def config_wireless_tag_policy_and_policy_profile(self):
        policy = self.cc.config_wireless_tag_policy_and_policy_profile()
        return policy

    def enable_wlan(self):
        enable = self.cc.config_enable_wlan_send_no_shutdown()
        return enable

    def enable_5ghz_netwrk(self):
        en_net = self.cc.config_no_ap_dot11_5ghz_shutdown()
        return en_net

    def enable_ap_5ghz(self):
        ap = self.cc.config_ap_no_dot11_5ghz_shutdown()
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

    def get_all_ssids_from_controller(self):
        wlan_summary = self.cc.show_wlan_summary()
        # print(wlan_summary)
        ele_list = [y for y in (x.strip() for x in wlan_summary.splitlines()) if y]
        indices = [i for i, s in enumerate(ele_list) if 'Profile Name' in s]
        print(indices)
        main_idx = indices[1]
        idx = main_idx + 2
        print(idx)
        print(ele_list[idx])
        ssid_count = self.get_number_of_wlan_present()
        print(ssid_count)
        ssid_list =[]
        count = 0
        for id in ssid_count:
            print(id)
        print(ele_list[int(indices[1])])
        return wlan_summary




if __name__ == '__main__':
    controller = {
        'ip': "localhost",                  # '172.16.0.2'
        'username': "admin",
        'password': 'yz',
        'ssh_port': "8888",   # 22
        'series': "9800",
        'prompt': "WLC2",
        'ap_name': "AP2C57.4152.385C",
        'band': "5g",
        'scheme': "ssh"
        }
    obj = CController(controller_data=controller, timeout="10", ssid_data=None)
    # x = obj.get_all_ssids_from_controller()
    # print(x)
    # obj.no_logging_console()
    # obj.line_console()
    # obj.delete_wlan()
    # obj.no_logging_console()
    obj.get_ssids()
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
