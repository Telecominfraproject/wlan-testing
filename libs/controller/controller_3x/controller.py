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
    def __init__(self, controller_data, timeout):
        self.controller_data = controller_data
        self.ip = self.controller_data["ip"]
        self.user = self.controller_data["username"]
        self.password = self.controller_data["password"]
        self.port = self.controller_data["port"]
        self.type = self.controller_data["series"]
        self.prompt = self.controller_data["prompt"]
        self.ap_name = self.controller_data["ap_name"]
        self.band = self.controller_data["band"]
        self.scheme = self.controller_data["scheme"]
        self.timeout = timeout

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

    def create_wlan_wpa2(self):
        ssid = self.cc.config_wlan_open()
        return ssid

    def no_logging_console(self):
        log = self.cc.no_logging_console()
        print(log)
        return log

    def line_console(self):
        line = self.cc.line_console_0()
        return line

    def get_ssids(self):
        wlan_summary = self.cc.show_wlan_summary()
        print(wlan_summary)
        return wlan_summary

    def get_number_of_wlan_present(self):
        wlan_summary = self.cc.show_wlan_summary()
        value = wlan_summary.decode("utf-8")
        ele_list = [y for y in (x.strip() for x in value.splitlines()) if y]
        indices = [i for i, s in enumerate(ele_list) if 'Number of WLANs' in s]
        number = ele_list[22][17:18].strip()
        print(number, "ssid's are present")
        return number
        # do some formatting here and return actual data


if __name__ == '__main__':
    controller = {
        'ip': "localhost",                  # '172.16.0.2'
        'username': "admin",
        'password': 'xyz',
        'port': "8888",   # 22
        'series': "9800",
        'prompt': "WLC2",
        'ap_name': "AP2C57.4152.385C",
        'band': "5g",
        'scheme': "ssh"
        }
    obj = CController(controller_data=controller, timeout="20")
    # obj.no_logging_console()
    # obj.get_ssids()
    obj.get_number_of_wlan_present()


# if __name__ == '__main__':
#     logger_config = lf_logger_config.lf_logger_config()
#     series = importlib.import_module("cc_module_9800_3504")
#     cc = series.create_controller_series_object(
#             scheme="ssh",
#             dest="localhost",
#             user="admin",
#             passwd="Cisco123",
#             prompt="WLC2",
#             series="9800",
#             ap="AP2C57.4152.385C",
#             port="8888",
#             band="5g",
#             timeout="10")
#     cc.show_ap_config_slots()
#     cc.show_wlan_summary()
#
