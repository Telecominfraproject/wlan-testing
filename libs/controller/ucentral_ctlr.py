"""

    Base Library for Ucentral

"""
import sys

import pytest
import allure
import requests
from ucentral_gw import swagger_client


class ConfigureController:

    def __init__(self):
        self.configuration = swagger_client.Configuration()

    def set_credentials(self, controller_data=None):
        if dict(controller_data).keys().__contains__("username") and dict(controller_data).keys().__contains__(
                "password"):
            self.configuration.username = "support@example.com"
            self.configuration.password = "support"
            print("Login Credentials set to default: \n user_id: %s\n password: %s\n" % ("support@example.com",
                                                                                         "support"))
            return False
        else:
            self.configuration.username = controller_data["username"]
            self.configuration.password = controller_data["password"]
            print("Login Credentials set to custom: \n user_id: %s\n password: %s\n" % (controller_data['userId'],
                                                                                        controller_data['password']))
            return True

    def select_controller_data(self, controller_data=None):
        if dict(controller_data).keys().__contains__("url") is None:
            print("No controller_data Selected")
            exit()
        self.sdk_base_url = controller_data["url"]
        self.configuration.host = self.sdk_base_url
        print("controller_data Selected: %s\n SDK_BASE_URL: %s\n" % (controller_data["url"], self.sdk_base_url))
        return True

    def set_sdk_base_url(self, sdk_base_url=None):
        if sdk_base_url is None:
            print("URL is None")
            exit()
        self.configuration.host = sdk_base_url
        return True


class Controller(ConfigureController):
    def __init__(self, controller_data=None, customer_id=None):
        super().__init__()
        self.controller_data = controller_data
        self.customer_id = customer_id
        if customer_id is None:
            self.customer_id = 2
            print("Setting to default Customer ID 2")
        #
        # Setting the Controller Client Configuration
        self.select_controller_data(controller_data=controller_data)
        self.set_credentials(controller_data=controller_data)
        # self.configuration.refresh_api_key_hook = self.get_bearer_token
        #
        # # Connecting to Controller
        # self.api_client = swagger_client.ApiClient(self.configuration)
        # self.login_client = swagger_client.LoginApi(api_client=self.api_client)
        # self.bearer = False
        # self.disconnect = False
        # # Token expiry in seconds
        # self.token_expiry = 1000
        # self.token_timestamp = time.time()
        # try:
        #
        #     self.bearer = self.get_bearer_token()
        #     # t1 = threading.Thread(target=self.refresh_instance)
        #     # t1.start()
        #     self.api_client.default_headers['Authorization'] = "Bearer " + self.bearer._access_token
        #     self.status_client = swagger_client.StatusApi(api_client=self.api_client)
        #     self.equipment_client = swagger_client.EquipmentApi(self.api_client)
        #     self.profile_client = swagger_client.ProfileApi(self.api_client)
        #     self.api_client.configuration.api_key_prefix = {
        #         "Authorization": "Bearer " + self.bearer._access_token
        #     }
        #     self.api_client.configuration.refresh_api_key_hook = self.refresh_instance
        # except Exception as e:
        #     self.bearer = False
        #     print(e)

        print("Connected to Controller Server")



controller = {
        'url': "https://wlan-portal-svc-nola-01.cicd.lab.wlan.tip.build",  # API base url for the controller
        'username': 'support@example.com',
        'password': 'support',
        'version': "1.1.0-SNAPSHOT",
        'commit_date': "2021-04-27"
}
Controller(controller_data=controller)


















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
#         },  # SSID Information is here
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
#         }  # LAN/WAN Information is here
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
