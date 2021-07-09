"""

    Base Library for Ucentral

"""
import json
import ssl
import sys
import time
from urllib.parse import urlparse
import pytest
import allure
import requests
from pathlib import Path

from requests.adapters import HTTPAdapter
import logging

logging.basicConfig(level=logging.DEBUG)
from http.client import HTTPConnection
HTTPConnection.debuglevel = 1
requests.logging.getLogger()
class ConfigureController:

    def __init__(self, controller_data):
        self.username = controller_data["username"]
        self.password = controller_data["password"]
        self.host = urlparse(controller_data["url"])
        self.access_token = ""
        # self.session = requests.Session()

        self.login_resp = self.login()

    def build_uri(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.host.hostname, self.host.port, path)
        print(new_uri)
        return new_uri

    def login(self):
        uri = self.build_uri("oauth2")
        # self.session.mount(uri, HTTPAdapter(max_retries=15))
        payload = json.dumps({"userId": self.username, "password": self.password})
        resp = requests.post(uri, data=payload, verify=False, timeout=100)
        self.check_response("POST", resp, "", payload, uri)
        token = resp.json()
        self.access_token = token["access_token"]
        print(resp)
        # self.session.headers.update({'Authorization': self.access_token})
        return resp

    def logout(self):
        uri = self.build_uri('oauth2/%s' % self.access_token)
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        print('Logged out:', resp.status_code)
        return resp

    def make_headers(self):
        headers = {'Authorization': 'Bearer %s' % self.access_token,
                   "Connection": "keep-alive",
                   "Keep-Alive": "timeout=10, max=1000"
                   }
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


class UController(ConfigureController):

    def __init__(self, controller_data=None):
        super().__init__(controller_data)

    def get_devices(self):
        uri = self.build_uri("devices/")
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        devices = resp.json()
        # resp.close()()
        return devices

    def get_device_by_serial_number(self, serial_number=None):
        uri = self.build_uri("device/" + serial_number)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        device = resp.json()
        # resp.close()()
        return device

    def get_device_uuid(self, serial_number):
        device_info = self.get_device_by_serial_number(serial_number=serial_number)
        return device_info["UUID"]


class UProfileUtility:

    def __init__(self, sdk_client=None, controller_data=None):
        if sdk_client is None:
            self.sdk_client = UController(controller_data=controller_data)
        self.sdk_client = sdk_client
        self.base_profile_config = {
            "uuid": 1,
            "radios": [],
            "interfaces": [{
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
                }
            },
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
                }],
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
        self.vlan_section = {
            "name": "WAN100",
            "role": "upstream",
            "vlan": {
                "id": 100
            },
            "ethernet": [
                {
                    "select-ports": [
                        "WAN*"
                    ]
                }
            ],
            "ipv4": {
                "addressing": "dynamic"
            }
        }
        self.mode = None

    def set_radio_config(self, radio_config=None):
        self.base_profile_config["radios"].append({
            "band": "2G",
            "country": "US",
            # "channel-mode": "HE",
            "channel-width": 20,
            # "channel": 11
        })
        self.base_profile_config["radios"].append({
            "band": "5G",
            "country": "US",
            # "channel-mode": "HE",
            "channel-width": 80,
            # "channel": 36
        })

        self.vlan_section["ssids"] = []
        self.vlan_ids = []

    def set_mode(self, mode):
        self.mode = mode
        if mode == "NAT":
            self.base_profile_config['interfaces'][1]['ssids'] = []

        elif mode == "BRIDGE":
            del self.base_profile_config['interfaces'][1]
            self.base_profile_config['interfaces'][0]['ssids'] = []
        elif mode == "VLAN":
            del self.base_profile_config['interfaces'][1]
            self.base_profile_config['interfaces'][0]['ssids'] = []
            self.base_profile_config['interfaces'] = []
        else:
            print("Invalid Mode")
            return 0

    def add_ssid(self, ssid_data, radius=False, radius_auth_data={}, radius_accounting_data={}):
        print("ssid data : ", ssid_data)
        ssid_info = {'name': ssid_data["ssid_name"], "bss-mode": "ap", "wifi-bands": []}
        for i in ssid_data["appliedRadios"]:
            ssid_info["wifi-bands"].append(i)
        ssid_info['encryption'] = {}
        ssid_info['encryption']['proto'] = ssid_data["security"]
        try:
            ssid_info['encryption']['key'] = ssid_data["security_key"]
        except:
            pass
        ssid_info['encryption']['ieee80211w'] = "optional"
        if radius:
            ssid_info["radius"] = {}
            ssid_info["radius"]["authentication"] = {
                "host": radius_auth_data["ip"],
                "port": radius_auth_data["port"],
                "secret": radius_auth_data["secret"]
            }
            ssid_info["radius"]["accounting"] = {
                "host": radius_accounting_data["ip"],
                "port": radius_accounting_data["port"],
                "secret": radius_accounting_data["secret"]
            }
        if self.mode == "NAT":
            self.base_profile_config['interfaces'][1]['ssids'].append(ssid_info)
        elif self.mode == "BRIDGE":
            self.base_profile_config['interfaces'][0]['ssids'].append(ssid_info)
        elif self.mode == "VLAN":
            vid = ssid_data["vlan"]
            self.vlan_section = {
                "name": "WAN100",
                "role": "upstream",
                "vlan": {
                    "id": 100
                },
                "ethernet": [
                    {
                        "select-ports": [
                            "WAN*"
                        ]
                    }
                ],
                "ipv4": {
                    "addressing": "dynamic"
                }
            }
            vlan_section = self.vlan_section
            if vid in self.vlan_ids:
                print("sss", self.vlan_ids)
                for i in self.base_profile_config['interfaces']:
                    if i["name"] == "WANv%s" % (vid):
                        i["ssids"].append(ssid_info)
            else:
                print(self.vlan_ids)
                self.vlan_ids.append(vid)
                vlan_section['name'] = "WANv%s" % (vid)
                vlan_section['vlan']['id'] = int(vid)
                vlan_section["ssids"] = []
                vlan_section["ssids"].append(ssid_info)
                self.base_profile_config['interfaces'].append(vlan_section)
                print(vlan_section)
                vsection = 0
            # Add to the ssid section
            # print(self.base_profile_config)
            # self.base_profile_config['interfaces'][vsection]['vlan'] = {'id': int(vid)}
            # self.base_profile_config['interfaces'][vsection]['ssids'].append(ssid_info)
        else:
            print("invalid mode")
            pytest.exit("invalid Operating Mode")

    def push_config(self, serial_number):
        payload = {"configuration": self.base_profile_config, 'serialNumber': serial_number, 'UUID': 0}

        uri = self.sdk_client.build_uri("device/" + serial_number + "/configure")
        basic_cfg_str = json.dumps(payload)
        print(self.base_profile_config)
        resp = requests.post(uri, data=basic_cfg_str, headers=self.sdk_client.make_headers(),
                             verify=False, timeout=100)
        self.sdk_client.check_response("POST", resp, self.sdk_client.make_headers(), basic_cfg_str, uri)
        print(resp.url)
        # resp.close()()
        print(resp)


# UCENTRAL_BASE_CFG = {
#     "uuid": 1,
#     "radios": [
#         {
#             "band": "2G",
#             "country": "US",
#             "channel-mode": "HE",
#             "channel-width": 20,
#             "channel": 11
#         },
#         {
#             "band": "5G",
#             "country": "US",
#             "channel-mode": "HE",
#             "channel-width": 80,
#             "channel": 36
#         }
#     ],  # Similar to RF Profile
#
#     "interfaces": [
#         {
#             "name": "WAN",
#             "role": "upstream",
#             "services": ["lldp"],
#             "ethernet": [
#                 {
#                     "select-ports": [
#                         "WAN*"
#                     ]
#                 }
#             ],
#             "ipv4": {
#                 "addressing": "dynamic"
#             },
#             "ssids": [
#                 {
#                     "name": "OpenWifi",
#                     "wifi-bands": [
#                         "2G"
#                     ],
#                     "bss-mode": "ap",
#                     "encryption": {
#                         "proto": "psk2",
#                         "key": "OpenWifi",
#                         "ieee80211w": "optional"
#                     }
#                 },
#                 {
#                     "name": "OpenWifi",
#                     "wifi-bands": [
#                         "5G"
#                     ],
#                     "bss-mode": "ap",
#                     "encryption": {
#                         "proto": "psk2",
#                         "key": "OpenWifi",
#                         "ieee80211w": "optional"
#                     }
#                 }
#             ]
#         },
#         {
#             "name": "LAN",
#             "role": "downstream",
#             "services": ["ssh", "lldp"],
#             "ethernet": [
#                 {
#                     "select-ports": [
#                         "LAN*"
#                     ]
#                 }
#             ],
#             "ipv4": {
#                 "addressing": "static",
#                 "subnet": "192.168.1.1/16",
#                 "dhcp": {
#                     "lease-first": 10,
#                     "lease-count": 10000,
#                     "lease-time": "6h"
#                 }
#             },
#             "ssids": [
#                 {
#                     "name": "OpenWifi",
#                     "wifi-bands": [
#                         "2G"
#                     ],
#                     "bss-mode": "ap",
#                     "encryption": {
#                         "proto": "psk2",
#                         "key": "OpenWifi",
#                         "ieee80211w": "optional"
#                     }
#                 },
#                 {
#                     "name": "OpenWifi",
#                     "wifi-bands": [
#                         "5G"
#                     ],
#                     "bss-mode": "ap",
#                     "encryption": {
#                         "proto": "psk2",
#                         "key": "OpenWifi",
#                         "ieee80211w": "optional"
#                     }
#                 }
#             ]
#
#         }
#     ],
#     "metrics": {
#         "statistics": {
#             "interval": 120,
#             "types": ["ssids", "lldp", "clients"]
#         },
#         "health": {
#             "interval": 120
#         }
#     },
#     "services": {
#         "lldp": {
#             "describe": "uCentral",
#             "location": "universe"
#         },
#         "ssh": {
#             "port": 22
#         }
#     }
# }
#
RADIUS_SERVER_DATA = {
    "ip": "10.10.10.72",
    "port": 1812,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
}

RADIUS_ACCOUNTING_DATA = {
    "ip": "10.10.10.72",
    "port": 1813,
    "secret": "testing123",
    "user": "user",
    "password": "password",
    "pk_password": "whatever"
}
controller = {
    # 'url': "https://tip-f34.candelatech.com:16001/api/v1/oauth2",  # API base url for the controller
    'url': 'https://sdk-ucentral-2.cicd.lab.wlan.tip.build:16001/api/v1/oauth2',
    'username': "tip@ucentral.com",
    'password': 'openwifi',
    # 'version': "1.1.0-SNAPSHOT",
    # 'commit_date': "2021-04-27"
}
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
# obj = UController(controller_data=controller)
# # # # time.sleep(10)
# # # obj.logout()
# # # # # # # # # # print(obj.get_devices())
# # # # # # # # # # print(obj.get_device_uuid(serial_number="903cb3944873"))
# # # # # # # # # # # obj.get_device_uuid(serial_number="c4411ef53f23")
# profile_client = UProfileUtility(sdk_client=obj)
# profile_client.set_radio_config()
# profile_client.set_mode(mode="BRIDGE")
# ssid_data = {"ssid_name": "ssid_shivam_psk", "appliedRadios": ["2G", "5G", "6G"], "security_key": "something", "security": "wpa2"} # sae # sae-mixed
# profile_client.add_ssid(ssid_data=ssid_data, radius=True, radius_auth_data=RADIUS_SERVER_DATA, radius_accounting_data=RADIUS_ACCOUNTING_DATA)
# # # # # ssid_data = {"ssid_name": "ssid_wpa_test_4_vlan", "vlan": 100, "appliedRadios": ["2G", "5G"], "security_key": "something", "security": "none"}
# # # # # profile_client.add_ssid(ssid_data=ssid_data)
# # # # print(profile_client.base_profile_config)
# profile_client.push_config(serial_number="903cb39d6918")
# # b = json.loads(str(profile_client.base_profile_config).replace(" ", "").replace("'", '"'))#, json.dumps(b, sort_keys=True)
# print(b["interfaces"])#, b["interfaces"])
# # print(profile_client.base_profile_config)
# # equipments = obj.get_devices()
# print(equipments)
# for i in equipments:
#     for j in equipments[i]:
#         for k in j:
#             print(k, j[k])
# print(equipments)

# obj.logout()
# #

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
