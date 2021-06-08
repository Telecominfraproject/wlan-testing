"""

    Base Library for Ucentral

"""
import json
import ssl
import sys
from urllib.parse import urlparse
import pytest
import allure
import requests
from pathlib import Path


class ConfigureController:

    def __init__(self, controller_data):
        self.username = controller_data["username"]
        self.password = controller_data["password"]
        self.host = urlparse(controller_data["url"])
        self.access_token = ""
        self.login()

    def build_uri(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.host.hostname, self.host.port, path)
        return new_uri

    def login(self):

        uri = self.build_uri("oauth2")
        payload = json.dumps({"userId": self.username, "password": self.password})
        resp = requests.post(uri, data=payload, verify="")
        self.check_response("POST", resp, "", payload, uri)
        token = resp.json()
        self.access_token = token["access_token"]

    def logout(self):
        global access_token
        uri = self.build_uri('oauth2/%s' % access_token)
        resp = requests.delete(uri, headers=self.make_headers(), verify=False)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        print('Logged out:', resp.status_code)

    def make_headers(self):
        headers = {'Authorization': 'Bearer %s' % self.access_token}
        return headers

    def check_response(self, cmd, response, headers, data_str, url):
        if response.status_code >= 400:
            if response.status_code >= 400:
                print("check-response: ERROR, url: ", url)
            else:
                print("check-response: url: ", url)
            print("Command: ", cmd)
            print("response-status: ", response.status_code)
            print("response-headers: ", response.headers)
            print("response-content: ", response.content)
            print("headers: ", headers)
            print("data-str: ", data_str)

        if response.status_code >= 400:
            # if True:
            raise NameError("Invalid response code.")
        return True


class Controller(ConfigureController):

    def __init__(self, controller_data=None):
        super().__init__(controller_data)

    def get_devices(self):
        uri = self.build_uri("devices/")
        resp = requests.get(uri, headers=self.make_headers(), verify=False)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        devices = resp.json()
        return devices

    def get_device_by_serial_number(self, serial_number=None):
        uri = self.build_uri("devices/"+serial_number)
        resp = requests.get(uri, headers=self.make_headers(), verify=False)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        device = resp.json()
        return device

class ProfileUtility:

    def __init__(self, sdk_client=None, controller_data=None):
        if sdk_client is None:
            self.sdk_client = Controller(controller_data=controller_data)
        self.sdk_client=sdk_client
        self.base_profile_config = {
            "uuid": 1,
            "radios": [{},{}],
            "interfaces": [{}, {}],
            "metrics": {},
            "services": {},
        }

    def set_radio_config(self, radio_config):
        for i in radio_config:
            self.base_profile_config["radios"][0] = {
                "band": "2G",
                "country": "US",
                "channel-mode": "HE",
                "channel-width": 20,
                "channel": 11
            }
        pass







UCENTRAL_BASE_CFG = {
    "uuid": 1,
    "radios": [
        {
            "band": "2G",
            "country": "US",
            "channel-mode": "HE",
            "channel-width": 20,
            "channel": 11
        },
        {
            "band": "5G",
            "country": "US",
            "channel-mode": "HE",
            "channel-width": 80,
            "channel": 36
        }
    ],  # Similar to RF Profile

    "interfaces": [
        {
            "name": "WAN",
            "role": "upstream",
            "services": ["lldp"],
            "ethernet": [
                {
                    "select-ports": [
                        "WAN*"
                    ]
                }
            ],
            "ipv4": {
                "addressing": "dynamic"
            },
            "ssids": [
                {
                    "name": "OpenWifi",
                    "wifi-bands": [
                        "2G"
                    ],
                    "bss-mode": "ap",
                    "encryption": {
                        "proto": "psk2",
                        "key": "OpenWifi",
                        "ieee80211w": "optional"
                    }
                },
                {
                    "name": "OpenWifi",
                    "wifi-bands": [
                        "5G"
                    ],
                    "bss-mode": "ap",
                    "encryption": {
                        "proto": "psk2",
                        "key": "OpenWifi",
                        "ieee80211w": "optional"
                    }
                }
            ]
        },  # SSID Information is here
        {
            "name": "LAN",
            "role": "downstream",
            "services": ["ssh", "lldp"],
            "ethernet": [
                {
                    "select-ports": [
                        "LAN*"
                    ]
                }
            ],
            "ipv4": {
                "addressing": "static",
                "subnet": "192.168.1.1/16",
                "dhcp": {
                    "lease-first": 10,
                    "lease-count": 10000,
                    "lease-time": "6h"
                }
            },
            "ssids": [
                {
                    "name": "OpenWifi",
                    "wifi-bands": [
                        "2G"
                    ],
                    "bss-mode": "ap",
                    "encryption": {
                        "proto": "psk2",
                        "key": "OpenWifi",
                        "ieee80211w": "optional"
                    }
                },
                {
                    "name": "OpenWifi",
                    "wifi-bands": [
                        "5G"
                    ],
                    "bss-mode": "ap",
                    "encryption": {
                        "proto": "psk2",
                        "key": "OpenWifi",
                        "ieee80211w": "optional"
                    }
                }
            ]

        }  # LAN/WAN Information is here
    ],
    "metrics": {
        "statistics": {
            "interval": 120,
            "types": ["ssids", "lldp", "clients"]
        },
        "health": {
            "interval": 120
        }
    },
    "services": {
        "lldp": {
            "describe": "uCentral",
            "location": "universe"
        },
        "ssh": {
            "port": 22
        }
    }
}



controller = {
    'url': "https://tip-f34.candelatech.com:16001/api/v1/oauth2",  # API base url for the controller
    'username': "tip@ucentral.com",
    'password': 'openwifi',
    # 'version': "1.1.0-SNAPSHOT",
    # 'commit_date': "2021-04-27"
}

obj = Controller(controller_data=controller)
equipments = obj.get_equipment()
print(equipments)
for i in equipments:
    for j in equipments[i]:
        print(j)
# print(equipments)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# print(sys.path)
# exit()

#
# profile_data = {
#     "mode": "BRIDGE",
#     "ssid_modes": {
#         "wpa2_personal": [
#             {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
#             {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
#              "security_key": "something"}]},
#     "rf": {},
#     "radius": False
# }
#
# uri = "https://" + "tip-f34.candelatech.com" + ":16001/api/v1/oauth2"
# username = "tip@ucentral.com"
# password = "openwifi"
#
# def build_uri(path):
#     global host
#     new_uri = 'https://%s:%d/api/v1/%s' % (host.hostname, host.port, path)
#     return new_uri
# def make_headers():
#     global access_token
#     headers = {'Authorization': 'Bearer %s' % access_token}
#     return headers
# def check_response(cmd, response, headers, data_str, url):
#     if response.status_code >= 400 or args.verbose:
#         if response.status_code >= 400:
#             print("check-response: ERROR, url: ", url)
#         else:
#             print("check-response: url: ", url)
#         print("Command: ", cmd)
#         print("response-status: ", response.status_code)
#         print("response-headers: ", response.headers)
#         print("response-content: ", response.content)
#         print("headers: ", headers)
#         print("data-str: ", data_str)
#
#     if response.status_code >= 400:
#         if assert_bad_response:
#             raise NameError("Invalid response code.")
#         return False
#     return True
#
# def get_devices():
#     uri = build_uri("devices")
#     resp = requests.get(uri, headers=make_headers(), verify=False)
#     check_response("GET", resp, make_headers(), "", uri)
#     data = resp.json()
#     devices = data["devices"]
#     return devices
#
# class UController:
#
#     def __init__(self, profile_data=None):
#         # self.base_cfg = UCENTRAL_BASE_CFG
#         self.login()
#
#
#
#         # if profile_data is None:
#         #     exit(1)
#         # self.profile_data = profile_data
#
#     def login(self):
#         uri = build_uri("oauth2")
#         payload = json.dumps({"userId": username, "password": password})
#         resp = requests.post(uri, data=payload, verify=cert)
#         check_response("POST", resp, "", payload, uri)
#         token = resp.json()
#         access_token = token["access_token"]
#
#     def setup_config(self):
#         if self.profile_data["mode"] == "BRIDGE":
#             del self.base_cfg["interfaces"][1]
#
#             for security in self.profile_data["ssid_modes"]:
#                 if security == "wpa2_personal":
#                     for ssid_index in range(len(self.profile_data["ssid_modes"][security])):
#                         self.base_cfg['interfaces'][0]['ssids'][ssid_index]['name'] = \
#                             self.profile_data["ssid_modes"][security][ssid_index]["ssid_name"]
#                         self.base_cfg['interfaces'][0]['ssids'][ssid_index]['encryption']['proto'] = "psk2"
#                         self.base_cfg['interfaces'][0]['ssids'][ssid_index]['encryption']['key'] = \
#                             self.profile_data["ssid_modes"][security][ssid_index]["security_key"]
#
#         print(self.base_cfg)
#
#     def push_config(self):
#         pass
#
#
# if __name__ == '__main__':
#     u_obj = UController(profile_data=profile_data)
#     u_obj.setup_config()
#
#
#
