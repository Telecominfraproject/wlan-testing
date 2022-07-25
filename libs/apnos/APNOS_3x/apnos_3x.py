import sys

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

import logging
import importlib
import subprocess
import os
import paramiko
import random

sys.path.append(os.path.join(os.path.abspath("../../../lanforge/lanforge-scripts/")))
logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")
series = importlib.import_module("ap_module_9800_3504")


class CCap:
    def __init__(self, controller_data, ap_data=None, timeout=None, ssid_data=None, type=None):
        self.controller_data = controller_data
        self.ap_data = ap_data
        self.type = type
        print("type", type)
        print(self.ap_data)
        self.ip = self.controller_data["ip"]
        self.user = self.ap_data[0]["access_point_username"]
        self.password = self.ap_data[0]["access_point_password"]
        self.port = "23204"
        self.type = self.controller_data["series"]
        self.prompt = self.ap_data[0]["ap_name"]
        self.dest_ip = self.ap_data[0]["ip"]
        self.dest_username = self.ap_data[0]["username"]
        self.dest_password = self.ap_data[0]["password"]
        self.dest_port = self.ap_data[0]["port"]
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

        self.scheme = self.ap_data[0]["access_point_scheme"]
        self.timeout = timeout
        self.ssid_data = ssid_data
        print("ssid data", self.ssid_data)

        self.cc = series.create_ap_series_object(
            scheme=self.scheme,
            dest=self.dest_ip,
            user=self.user,
            passwd=self.password,
            prompt=self.prompt,
            # series=self.type,
            ap=self.ap_name,
            port=self.port,
            # band=self.band,
            timeout=self.timeout
        )

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
        # self.cc.pwd = "../../../lanforge/lanforge-scripts"

    def no_logging_console(self):
        log = self.cc.no_logging_console()
        print(log)
        return log

    def line_console(self):
        line = self.cc.line_console_0()
        return line

    def gen_random_port_num(self,len=1):
        randomlist = random.sample(range(23200, 23206),len)
        print(randomlist)
        return randomlist

    def ap_login(self,jump_host=""):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.dest_ip, port=self.dest_port, username=self.dest_username,
                    password=self.dest_password, timeout=300)
        # port_num=self.gen_random_port_num(len=len(self.ap_data))
        ssh.exec_command("fuser -k 23204/tcp")
        stdin, stdout, stderr = ssh.exec_command(
            f"cd git/mux_serial/ && ./mux_server.py --device /dev/ttyUSB{jump_host[-1]} --baud 11200 --port 23204")

        output = stdout.readlines()
        stdin.close()

        print(output)
        return ssh

    def show_data_rates_config_from_ap_24g(self,jump_host_detail="",ap=""):
        ssh_client = self.ap_login(jump_host=jump_host_detail)
        self.cc.ap = ap
        val = "0"
        data_rate_response = self.cc.show_data_rates(value=val)
        ssh_client.close()
        return data_rate_response

    def show_data_rates_config_from_ap_5g(self,jump_host_detail="",ap=""):
        ssh_client = self.ap_login(jump_host=jump_host_detail)
        self.cc.ap = ap
        val = "1"
        data_rate_response = self.cc.show_data_rates(value=val)
        ssh_client.close()
        return data_rate_response

    def show_data_rates_config_from_ap_6g(self,jump_host_detail="",ap=""):
        ssh_client = self.ap_login(jump_host=jump_host_detail)
        self.cc.ap = ap
        val = "2"
        data_rate_response = self.cc.show_data_rates(value=val)
        ssh_client.close()
        return data_rate_response


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
            "tag_policy": "RM204-TB2",
            "access_point_username": "admin",  # pwd="/home/mahesh/cisco_280322/wlan-testing/lanforge/lanforge-scripts"
            "access_point_password": "Admin123",
            "access_point_scheme": "mux_client",
            "policy_profile": "myflexpolicy",
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
    obj = CCap(controller_data=controller, ap_data=access_point, timeout="10", ssid_data=None)
    # obj.get_ap_bssid_2g()
    # obj.no_logging_console()
    # ret = obj.set_dtim_5ghz(wlan='mcast-wpa2', value='7')
    # ret = obj.show_wireless_client_mac_detail(sta_mac="04:f0:21:9f:39:69")
    # print("return from controller...", ret)
    # ret_res = obj.set_eap_bcast_interval_in_sec(value='270')
    # print("return from controller...", ret_res)
    summary = obj.show_data_rates_config_from_ap()
    print(summary)
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
