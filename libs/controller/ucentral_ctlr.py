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

# logging.basicConfig(level=logging.DEBUG)
# from http.client import HTTPConnection
#
# HTTPConnection.debuglevel = 1
# requests.logging.getLogger()


class ConfigureController:

    def __init__(self, controller_data):
        self.username = controller_data["username"]
        self.password = controller_data["password"]
        self.host = urlparse(controller_data["url"])
        print(self.host)
        self.access_token = ""
        # self.session = requests.Session()
        self.login_resp = self.login()
        self.gw_host = self.get_endpoint()

    def build_uri_sec(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.host.hostname, self.host.port, path)
        print(new_uri)
        return new_uri

    def build_uri(self, path):

        new_uri = 'https://%s:%d/api/v1/%s' % (self.gw_host.hostname, self.gw_host.port, path)
        print(new_uri)
        return new_uri

    def login(self):
        uri = self.build_uri_sec("oauth2")
        # self.session.mount(uri, HTTPAdapter(max_retries=15))
        payload = json.dumps({"userId": self.username, "password": self.password})
        resp = requests.post(uri, data=payload, verify=False, timeout=100)
        self.check_response("POST", resp, "", payload, uri)
        token = resp.json()
        self.access_token = token["access_token"]
        print(token)

        # self.session.headers.update({'Authorization': self.access_token})
        return resp

    def get_endpoint(self):
        uri = self.build_uri_sec("systemEndpoints")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        print(resp)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        devices = resp.json()
        print(devices["endpoints"][0]["uri"])
        gw_host = urlparse(devices["endpoints"][0]["uri"])
        return gw_host

    def logout(self):
        uri = self.build_uri_sec('oauth2/%s' % self.access_token)
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
            wan_section_vlan = {
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
            }
            self.base_profile_config['interfaces'].append(wan_section_vlan)
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
        else:
            print("invalid mode")
            pytest.exit("invalid Operating Mode")

    def push_config(self, serial_number):
        payload = {"configuration": self.base_profile_config, 'serialNumber': serial_number, 'UUID': 0}

        uri = self.sdk_client.build_uri("device/" + serial_number + "/configure")
        basic_cfg_str = json.dumps(payload)
        # print(self.base_profile_config)
        resp = requests.post(uri, data=basic_cfg_str, headers=self.sdk_client.make_headers(),
                             verify=False, timeout=100)
        self.sdk_client.check_response("POST", resp, self.sdk_client.make_headers(), basic_cfg_str, uri)
        print(resp.url)
        resp.close()
        print(resp)


if __name__ == '__main__':


    controller = {
    'url': 'https://sec-ucentral-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
    'username': "tip@ucentral.com",
    'password': 'openwifi',
    }
    obj = UController(controller_data=controller)
    profile = UProfileUtility(sdk_client=obj)
    profile.set_mode(mode="VLAN")
    profile.set_radio_config()
    ssid = {"ssid_name": "ssid_wpa2_2g_nat", "appliedRadios": ["2G"], "security": "psk", "security_key": "something", "vlan": 100}
    profile.add_ssid(ssid_data=ssid)
    # profile.push_config(serial_number="903cb39d6918")
    # print(obj.get_devices())
    obj.logout()
