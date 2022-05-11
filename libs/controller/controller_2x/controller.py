"""

    Base Library for Ucentral

"""
import datetime
import json
import ssl
import sys
import time
from urllib.parse import urlparse
import pytest
import allure
import requests
from operator import itemgetter
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
        self.gw_host, self.fms_host, self.prov_host = self.get_gw_endpoint()
        if self.gw_host == "" or self.fms_host == "" or self.prov_host == "":
            time.sleep(60)
            self.gw_host, self.fms_host, self.prov_host = self.get_gw_endpoint()
            if self.gw_host == "" or self.fms_host == "" or self.prov_host == "":
                self.logout()
                print(self.gw_host, self.fms_host, self.prov_host)
                pytest.exit("All Endpoints not available in Controller Service")
                sys.exit()

    def build_uri_sec(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.host.hostname, self.host.port, path)
        print(new_uri)
        return new_uri

    def build_url_fms(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.fms_host.hostname, self.fms_host.port, path)
        print(new_uri)
        return new_uri

    def build_uri(self, path):

        new_uri = 'https://%s:%d/api/v1/%s' % (self.gw_host.hostname, self.gw_host.port, path)
        print(new_uri)
        return new_uri

    def build_url_prov(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.prov_host.hostname, self.prov_host.port, path)
        print(new_uri)
        return new_uri



    def request(self, service, command, method, params, payload):
        if service == "sec":
            uri = self.build_uri_sec(command)
        elif service == "gw":
            uri = self.build_uri(command)
        elif service == "fms":
            uri = self.build_url_fms(command)
        elif service == "prov":
            uri = self.build_url_prov(command)
        else:
            raise NameError("Invalid service code for request.")

        print(uri)
        params = params
        if method == "GET":
            resp = requests.get(uri, headers=self.make_headers(), params=params, verify=False, timeout=100)
        elif method == "POST":
            print(uri, payload, params)
            resp = requests.post(uri, params=params, data=payload, headers=self.make_headers(), verify=False,
                                 timeout=100)
        elif method == "PUT":
            resp = requests.put(uri, params=params, data=payload, verify=False, timeout=100)
        elif method == "DELETE":
            resp = requests.delete(uri, headers=self.make_headers(), params=params, verify=False, timeout=100)

        self.check_response(method, resp, self.make_headers(), payload, uri)
        print(resp)
        return resp

    def login(self):
        uri = self.build_uri_sec("oauth2")
        # self.session.mount(uri, HTTPAdapter(max_retries=15))
        payload = json.dumps({"userId": self.username, "password": self.password})
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("POST", resp, "", payload, uri)
        token = resp.json()
        self.access_token = token["access_token"]
        print(token)
        if resp.status_code != 200:
            print(resp.status_code)
            print(resp.json())
            pytest.exit(str(resp.json()))
        # self.session.headers.update({'Authorization': self.access_token})
        return resp

    def get_gw_endpoint(self):
        uri = self.build_uri_sec("systemEndpoints")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        print(resp)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        services = resp.json()
        print(services)
        gw_host = ""
        fms_host = ""
        for service in services['endpoints']:
            if service['type'] == "owgw":
                gw_host = urlparse(service["uri"])
            if service['type'] == "owfms":
                fms_host = urlparse(service["uri"])
            if service['type'] == "owprov":
                prov_host = urlparse(service["uri"])
        return gw_host, fms_host, prov_host

    def logout(self):
        uri = self.build_uri_sec('oauth2/%s' % self.access_token)
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        print('Logged out:', resp.status_code)
        return resp

    def make_headers(self):
        headers = {'Authorization': 'Bearer %s' % self.access_token,
                   "Connection": "keep-alive",
                   "Content-Type": "application/json",
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


class Controller(ConfigureController):

    def __init__(self, controller_data=None):
        super().__init__(controller_data)

    def get_devices(self):
        uri = self.build_uri("devices/")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_device_by_serial_number(self, serial_number):
        uri = self.build_uri("device/" + serial_number)
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_sdk_version(self):
        uri = self.build_uri("system/?command=info")
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        version = resp.json()
        print(version)
        # resp.close()()
        return version['version']

    def get_system_gw(self):
        uri = self.build_uri("system/?command=info")
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_system_fms(self):
        uri = self.build_url_fms("system/?command=info")
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_system_prov(self):
        uri = self.build_url_prov("system/?command=info")
        allure.attach(name="Url of Prov UI:", body=str(uri))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_device_uuid(self, serial_number):
        device_info = self.get_device_by_serial_number(serial_number=serial_number)
        return device_info["UUID"]

    def add_device_to_gw(self, serial_number, payload):
        uri = self.build_uri("device/" + serial_number)
        print(uri)
        print(payload)
        payload = json.dumps(payload)
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=100)
        print(resp)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def delete_device_from_gw(self, device_name):
        uri = self.build_uri("device/" + device_name)
        print(uri)
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def get_commands(self):
        uri = self.build_uri("commands")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_device_logs(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/logs")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_device_health_checks(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/healthchecks")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_device_capabilities(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/capabilities")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_device_statistics(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/statistics")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_device_status(self, serial_number):
        uri = self.build_uri("device/" + serial_number + "/status")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp


class FMSUtils:

    def __init__(self, sdk_client=None, controller_data=None):
        if sdk_client is None:
            self.sdk_client = Controller(controller_data=controller_data)
        self.sdk_client = sdk_client

    def upgrade_firmware(self, serial="", url=""):
        response = self.sdk_client.request(service="gw", command="device/" + serial + "/upgrade",
                                           method="POST", params="serialNumber=" + serial,
                                           payload="{ \"serialNumber\" : " + "\"" + serial + "\"" +
                                                   " , \"uri\" : " + "\"" + url + "\"" +
                                                   ", \"when\" : 0" + " }")
        print(response.json())
        allure.attach(name="REST - firmware upgrade response: ",
                      body=str(response.status_code) + "\n" +
                           str(response.json()) + "\n"
                      )

        print(response)

    def ap_model_lookup(self, model=""):
        devices = self.get_device_set()
        model_name = ""
        for device in devices['deviceTypes']:
            if str(device).__eq__(model):
                model_name = device
        return model_name

    def get_revisions(self):
        response = self.sdk_client.request(service="fms", command="firmwares/", method="GET", params="revisionSet=true",
                                           payload="")
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def get_latest_fw(self, model=""):

        device_type = self.ap_model_lookup(model=model)

        response = self.sdk_client.request(service="fms", command="firmwares/", method="GET",
                                           params="latestOnly=true&deviceType=" + device_type,
                                           payload="")
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def get_device_set(self):
        response = self.sdk_client.request(service="fms", command="firmwares/", method="GET", params="deviceSet=true",
                                           payload="")
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def get_firmwares(self, limit="10000", model="", latestonly="", branch="", commit_id="", offset="3000"):

        deviceType = self.ap_model_lookup(model=model)
        params = "limit=" + limit + \
                 "&deviceType=" + deviceType + \
                 "&latestonly=" + latestonly + \
                 "offset=" + offset
        command = "firmwares/"
        response = self.sdk_client.request(service="fms", command=command, method="GET", params=params, payload="")
        allure.attach(name=command + params,
                      body=str(response.status_code) + "\n" + str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        if response.status_code == 200:
            data = response.json()
            newlist = sorted(data['firmwares'], key=itemgetter('created'))
            # for i in newlist:
            #     print(i['uri'])
            #     print(i['revision'])
            # print(newlist)

            return newlist
            # print(data)

        return "error"

class ProvUtils(ConfigureController):

    def __init__(self, controller_data=None):
        super().__init__(controller_data)

    def build_url_prov(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.prov_host.hostname, self.prov_host.port, path)
        print(new_uri)
        return new_uri

    def get_inventory(self):
        uri = self.build_url_prov("inventory")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_inventory_by_device(self, device_name):
        uri = self.build_url_prov("inventory/" + device_name)
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_system_prov(self):
        uri = self.build_url_prov("system/?command=info")
        allure.attach(name="Url of Prov UI:", body=str(uri))
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def add_device_to_inventory(self, device_name, payload):
        uri = self.build_url_prov("inventory/" + device_name)
        print(uri)
        print(payload)
        payload = json.dumps(payload)
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=100)
        print(resp)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def delete_device_from_inventory(self, device_name):
        uri = self.build_url_prov("inventory/" + device_name)
        print(uri)
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def get_entity(self):
        uri = self.build_url_prov("entity")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_entity_by_id(self,entity_id):
        uri = self.build_url_prov("entity/" + entity_id)
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def add_entity(self, payload):
        uri = self.build_url_prov("entity/1")
        print(uri)
        print(payload)
        payload = json.dumps(payload)
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=100)
        print(resp)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def delete_entity(self, entity_id):
        uri = self.build_url_prov("entity/" + entity_id)
        print(uri)
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def edit_device_from_inventory(self, device_name, payload):
        uri = self.build_url_prov("inventory/" + device_name)
        print(uri)
        print(payload)
        payload = json.dumps(payload)
        resp = requests.put(uri, data=payload, headers=self.make_headers(), verify=False, timeout=100)
        print(resp)
        self.check_response("PUT", resp, self.make_headers(), payload, uri)
        return resp

    def edit_entity(self, payload, entity_id):
        uri = self.build_url_prov("entity/" + entity_id)
        print(uri)
        print(payload)
        payload = json.dumps(payload)
        resp = requests.put(uri, data=payload, headers=self.make_headers(), verify=False, timeout=100)
        print(resp)
        self.check_response("PUT", resp, self.make_headers(), payload, uri)
        return resp

    def get_contact(self):
        uri = self.build_url_prov("contact")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_contact_by_id(self, contact_id):
        uri = self.build_url_prov("contact/" + contact_id)
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def add_contact(self, payload):
        uri = self.build_url_prov("contact/1")
        print(uri)
        print(payload)
        payload = json.dumps(payload)
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=100)
        print(resp)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def delete_contact(self, contact_id):
        uri = self.build_url_prov("contact/" + contact_id)
        print(uri)
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def edit_contact(self, payload, contact_id):
        uri = self.build_url_prov("contact/" + contact_id)
        print(uri)
        print(payload)
        payload = json.dumps(payload)
        resp = requests.put(uri, data=payload, headers=self.make_headers(), verify=False, timeout=100)
        print(resp)
        self.check_response("PUT", resp, self.make_headers(), payload, uri)
        return resp

    def get_location(self):
        uri = self.build_url_prov("location")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_location_by_id(self, location_id):
        uri = self.build_url_prov("location/" + location_id)
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def add_location(self, payload):
        uri = self.build_url_prov("location/1")
        print(uri)
        print(payload)
        payload = json.dumps(payload)
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=100)
        print(resp)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def delete_location(self, location_id):
        uri = self.build_url_prov("location/" + location_id)
        print(uri)
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def edit_location(self, payload, location_id):
        uri = self.build_url_prov("location/" + location_id)
        print(uri)
        print(payload)
        payload = json.dumps(payload)
        resp = requests.put(uri, data=payload, headers=self.make_headers(), verify=False, timeout=100)
        print(resp)
        self.check_response("PUT", resp, self.make_headers(), payload, uri)
        return resp

    def get_venue(self):
        uri = self.build_url_prov("venue/")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def get_venue_by_id(self, venue_id):
        uri = self.build_url_prov("venue/" + venue_id)
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        return resp

    def add_venue(self, payload):
        uri = self.build_url_prov("venue/0")
        print(uri)
        print(payload)
        payload = json.dumps(payload)
        resp = requests.post(uri, data=payload, headers=self.make_headers(), verify=False, timeout=100)
        print(resp)
        self.check_response("POST", resp, self.make_headers(), payload, uri)
        return resp

    def delete_venue(self, venue_id):
        uri = self.build_url_prov("venue/" + venue_id)
        print(uri)
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        return resp

    def edit_venue(self, payload, venue_id):
        uri = self.build_url_prov("venue/" + venue_id)
        print(uri)
        print(payload)
        payload = json.dumps(payload)
        resp = requests.put(uri, data=payload, headers=self.make_headers(), verify=False, timeout=100)
        print(resp)
        self.check_response("PUT", resp, self.make_headers(), payload, uri)
        return resp

class UProfileUtility:

    def __init__(self, sdk_client=None, controller_data=None):
        if sdk_client is None:
            self.sdk_client = Controller(controller_data=controller_data)
        self.sdk_client = sdk_client
        self.base_profile_config = {
            "uuid": 1,
            "radios": [],
            "interfaces": [{
                "name": "WAN",
                "role": "upstream",
                "services": ["ssh", "lldp", "dhcp-snooping"],
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
                    "services": ["ssh", "lldp", "dhcp-snooping"],
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
                    "interval": 60,
                    "types": ["ssids", "lldp", "clients"]
                },
                "health": {
                    "interval": 120
                },
                "wifi-frames": {
                    "filters": ["probe",
                                "auth",
                                "assoc",
                                "disassoc",
                                "deauth",
                                "local-deauth",
                                "inactive-deauth",
                                "key-mismatch",
                                "beacon-report",
                                "radar-detected"]
                },
                "dhcp-snooping": {
                    "filters": ["ack", "discover", "offer", "request", "solicit", "reply", "renew"]
                }
            },
            "services": {
                "lldp": {
                    "describe": "TIP OpenWiFi",
                    "location": "QA"
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

    def set_mesh_services(self):
        self.base_profile_config["interfaces"][1]["ipv4"]["subnet"] = "192.168.97.1/24"
        self.base_profile_config["interfaces"][1]["ipv4"]["dhcp"]["lease-count"] = 100
        del self.base_profile_config['metrics']['wifi-frames']
        del self.base_profile_config['metrics']['dhcp-snooping']
        var = {
            "filters": ["probe",
                        "auth"]
        }
        self.base_profile_config["metrics"]['wifi-frames'] = var
        del self.base_profile_config['services']
        var2 = {
            "lldp": {
                "describe": "uCentral",
                "location": "universe"
            },
            "ssh": {
                "port": 22
            }
        }
        self.base_profile_config['services'] = var2

    def set_express_wifi(self, open_flow=None):
        if self.mode == "NAT":
            self.base_profile_config["interfaces"][1]["services"] = ["ssh", "lldp", "open-flow"]
            self.base_profile_config["interfaces"][1]["ipv4"]["subnet"] = "192.168.97.1/24"
            self.base_profile_config["interfaces"][1]["ipv4"]["dhcp"]["lease-count"] = 100
            self.base_profile_config['services']["open-flow"] = open_flow
            self.base_profile_config['services']['lldp']['describe'] = "OpenWiFi - expressWiFi"
            self.base_profile_config['services']['lldp']['location'] = "Hotspot"

    def set_captive_portal(self):

        if self.mode == "NAT":
            max_client = {
                "max-clients": 32
            }
            # sourceFile = open('captive_config.py', 'w')

            self.base_profile_config["interfaces"][1]["name"] = "captive"
            self.base_profile_config["interfaces"][1]["ipv4"]["subnet"] = "192.168.2.1/24"
            self.base_profile_config["interfaces"][1]["captive"] = max_client
            del self.base_profile_config["interfaces"][1]["ethernet"]
            del self.base_profile_config["interfaces"][1]["services"]
            del self.base_profile_config["metrics"]["wifi-frames"]
            del self.base_profile_config["metrics"]["dhcp-snooping"]
            # print(self.base_profile_config)
            # print(self.base_profile_config, file=sourceFile)
            # sourceFile.close()

    def encryption_lookup(self, encryption="psk"):
        encryption_mapping = {
            "none": "open",
            "psk": "wpa",
            "psk2": "wpa2",
            "sae": "wpa3",
            "psk-mixed": "wpa|wpa2",
            "sae-mixed": "wpa3",
            "wpa": 'wap',
            "wpa2": "eap",
            "wpa3": "eap",
            "wpa-mixed": "eap",
            "wpa3-mixed": "sae"
        }
        if encryption in encryption_mapping.keys():
            return encryption_mapping[encryption]
        else:
            return False

    def get_ssid_info(self):
        ssid_info = []
        for interfaces in self.base_profile_config["interfaces"]:
            if "ssids" in interfaces.keys():
                for ssid_data in interfaces["ssids"]:
                    for band in ssid_data["wifi-bands"]:
                        temp = [ssid_data["name"]]
                        if ssid_data["encryption"]["proto"] == "none" or "radius" in ssid_data.keys():
                            temp.append(self.encryption_lookup(encryption=ssid_data["encryption"]["proto"]))
                            temp.append('[BLANK]')
                        else:
                            temp.append(self.encryption_lookup(encryption=ssid_data["encryption"]["proto"]))
                            temp.append(ssid_data["encryption"]["key"])
                        temp.append(band)
                        ssid_info.append(temp)
        return ssid_info

    def set_radio_config(self, radio_config={}):
        base_radio_config_2g = {
            "band": "2G",
            "country": "CA",
            "channel-mode": "HE",
            "channel": "auto"
        }
        base_radio_config_5g = {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "HE",
            "channel": "auto"
        }
        for band in radio_config:
            if band == "2G":
                for keys in radio_config[band]:
                    base_radio_config_2g[keys] = radio_config[band][keys]
            if band == "5G":
                for keys in radio_config[band]:
                    base_radio_config_5g[keys] = radio_config[band][keys]
            # if band == "6G":
            #     for keys in radio_config[band]:
            #         base_radio_config_6g[keys] = radio_config[band][keys]


        self.base_profile_config["radios"].append(base_radio_config_2g)
        self.base_profile_config["radios"].append(base_radio_config_5g)
        print(self.base_profile_config)
        self.vlan_section["ssids"] = []
        self.vlan_ids = []

    def set_mode(self, mode, mesh=False):
        self.mode = mode
        if mode == "NAT":
            if mesh:
                self.base_profile_config['interfaces'][0]['tunnel'] = {
                    "proto": "mesh"
                }
            self.base_profile_config['interfaces'][1]['ssids'] = []
        elif mode == "BRIDGE":
            if mesh:
                self.base_profile_config['interfaces'][0]['tunnel'] = {
                    "proto": "mesh"
                }
            self.base_profile_config['interfaces'][0]['ssids'] = []
        elif mode == "VLAN":
            if mesh:
                self.base_profile_config['interfaces'][0]['tunnel'] = {
                    "proto": "mesh"
                }
            del self.base_profile_config['interfaces'][1]
            self.base_profile_config['interfaces'][0]['ssids'] = []
            self.base_profile_config['interfaces'] = []
            wan_section_vlan = {
                "name": "WAN",
                "role": "upstream",
                "services": ["lldp", "ssh", "dhcp-snooping"],
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
        ssid_info = {'name': ssid_data["ssid_name"], "bss-mode": "ap", "wifi-bands": [], "services": ["wifi-frames"]}
        for options in ssid_data:
            if options == "multi-psk":
                ssid_info[options] = ssid_data[options]
                print("hi", ssid_info)
            if options == "rate-limit":
                ssid_info[options] = ssid_data[options]
        for i in ssid_data["appliedRadios"]:
            ssid_info["wifi-bands"].append(i)
        ssid_info['encryption'] = {}
        ssid_info['encryption']['proto'] = ssid_data["security"]
        try:
            ssid_info['encryption']['key'] = ssid_data["security_key"]
        except Exception as e:
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
                "services": ["lldp", "dhcp-snooping"],
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
        payload = {"configuration": self.base_profile_config, "serialNumber": serial_number, "UUID": 1}

        uri = self.sdk_client.build_uri("device/" + serial_number + "/configure")
        basic_cfg_str = json.dumps(payload)
        allure.attach(name="ucentral_config: ",
                      body=str(basic_cfg_str),
                      attachment_type=allure.attachment_type.JSON)
        print("JSON Post Configure: " + str(basic_cfg_str))
        print("Sending Configure Command: ", datetime.datetime.utcnow())
        resp = requests.post(uri, data=basic_cfg_str, headers=self.sdk_client.make_headers(),
                             verify=False, timeout=100)
        print(resp.json())
        print(resp.status_code)
        allure.attach(name="/configure response: " + str(resp.status_code), body=str(resp.json()),
                      attachment_type=allure.attachment_type.JSON)
        self.sdk_client.check_response("POST", resp, self.sdk_client.make_headers(), basic_cfg_str, uri)
        # print(resp.url)
        resp.close()
        print(resp)


if __name__ == '__main__':
    controller = {
        'url': 'https://sec-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
        'username': "tip@ucentral.com",
        'password': 'OpenWifi%123',
    }
    obj = Controller(controller_data=controller)
    # up = UProfileUtility(sdk_client=obj, controller_data=controller)
    # up.set_mode(mode="BRIDGE")
    # up.set_radio_config()
    # up.add_ssid(ssid_data={"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "security": "psk2"})
    # up.push_config(serial_number="3c2c99f44e77")
    # print(obj.get_device_by_serial_number(serial_number="3c2c99f44e77"))
    # print(datetime.datetime.utcnow())
    # fms = FMSUtils(sdk_client=obj)
    # new = fms.get_firmwares(model='ecw5410')
    # for i in new:
    #     print(i)
    # print(len(new))

    # print(profile.get_ssid_info())
    # # print(obj.get_devices())
    # obj.logout()
