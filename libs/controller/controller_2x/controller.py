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
        self.gw_host, self.fms_host = self.get_gw_endpoint()
        if self.gw_host == "" or self.fms_host == "":
            time.sleep(60)
            self.gw_host, self.fms_host = self.get_gw_endpoint()
            if self.gw_host == "" or self.fms_host == "":
                self.logout()
                print(self.gw_host, self.fms_host)
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

    def request(self, service, command, method, params, payload):
        if service == "sec":
            uri = self.build_uri_sec(command)
        elif service == "gw":
            uri = self.build_uri(command)
        elif service == "fms":
            uri = self.build_url_fms(command)
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
        resp = requests.post(uri, data=payload, verify=False, timeout=100)
        self.check_response("POST", resp, "", payload, uri)
        token = resp.json()
        self.access_token = token["access_token"]
        print(token)

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
        return gw_host, fms_host

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


class Controller(ConfigureController):

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

    def get_sdk_version(self):
        uri = self.build_uri("system/?command=info")
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        version = resp.json()
        print(version)
        # resp.close()()
        return version['version']

    def get_device_uuid(self, serial_number):
        device_info = self.get_device_by_serial_number(serial_number=serial_number)
        return device_info["UUID"]


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
            if str(device).__contains__(model):
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

    def set_express_wifi(self):
        if self.mode == "NAT":
            self.base_profile_config["interfaces"][0]["services"] = ["lldp", "ssh"]
            self.base_profile_config["interfaces"][1]["services"] = ["ssh", "lldp", "open-flow"]
            self.base_profile_config["interfaces"][1]["ipv4"]["subnet"] = "192.168.97.1/24"
            self.base_profile_config["interfaces"][1]["ipv4"]["dhcp"]["lease-count"] = 100

            services = {
                'lldp': {
                    'describe': 'OpenWiFi - expressWiFi',
                    'location': 'Hotspot'
                },
                'ssh': {
                    'port': 22
                },
                'open-flow': {
                    'controller': "3.69.15.5",
                    'mode': 'ssl',
                    'ca-certificate': "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURiRENDQWxTZ0F3SUJBZ0lRVm1ySStwZTFUMDRROC9ZRXlRclFyekFOQmdrcWhraUc5dzBCQVFzRkFEQlAKTVJRd0VnWURWUVFLREF0dmNHVnVkMmxtYVMxaWNqRWhNQjhHQTFVRUN3d1liM0JsYm5kcFpta3RZbkl1WlhodwpjbVZ6YzE5M2FXWnBNUlF3RWdZRFZRUUREQXR2Y0dWdWQybG1hUzFpY2pBZ0Z3MHlNVEE0TWpRd09ESTBNekZhCkdBOHlNRGN4TURneU5EQTVNalF6TVZvd1R6RVVNQklHQTFVRUNnd0xiM0JsYm5kcFpta3RZbkl4SVRBZkJnTlYKQkFzTUdHOXdaVzUzYVdacExXSnlMbVY0Y0hKbGMzTmZkMmxtYVRFVU1CSUdBMVVFQXd3TGIzQmxibmRwWm1rdApZbkl3Z2dFaU1BMEdDU3FHU0liM0RRRUJBUVVBQTRJQkR3QXdnZ0VLQW9JQkFRQ2txbWR6T21NdkxCTThXTmdYCmFwOC94QWtzWmFkTGRNRVRXdGJkTWlTcDZjc2lVV0NZdVNzTXJQaFk5RXpiL0RVTzE4cC9MSHhzbU11Q01LZU4KVy9GMU81WmFlZTBoYVBaMkcxd2IyQlB3bGxkSk85L1pwNEYvMUQvd0I5S0FFTXFUK1ZHbXVCM0Fucm1kbDk5UQpkNHN6M05QOU9Qa1Uzak1hME1WSjhIMlNqMDNpVmdKYVYxc2U5NTdDa2dIWEw4WnVwQVMvS2JOMWJFaVRtc3JWCkg0TUtKN2NxODZNeVIyam83RWlBZ3kvR1psTDUwY2lZTDF4aVRBRG9UNTF5R25jd0JXWWJqMmwrU0gyMDlnbUIKblZRN3M1MWg5R3Nkc1ZLVHhIKzRqamoyWGdtSnZqc1F2NVNDN1V6ME5oSTFlallSWXV0MndESXZuSk45aG1NZQpQQkVoQWdNQkFBR2pRakJBTUE4R0ExVWRFd0VCL3dRRk1BTUJBZjh3SFFZRFZSME9CQllFRktUTytNWTFlckw4ClJsbnhnaTY1MXZpUlA1S05NQTRHQTFVZER3RUIvd1FFQXdJQmhqQU5CZ2txaGtpRzl3MEJBUXNGQUFPQ0FRRUEKU2FGRURpK3QyNFZUV0dyZzRldDluK2xHdm5STDdOTEU5QmREWFRrZzZ6YmNJN01UWExOMXpTNkVIZEI5QU4yNgpiQ3N4QTQzY0UyTkxCRzdNb0FqZktDOWdYNjdiVk9IK09PWmNEZzJOLzdrSkI3UzNSYlp1UHFGRU0weWFrL01sCnpqQlYwV1JBYnJDRit6UDhyT2pESTZZQWU0NHVESWQyWWxqUjVkdVpZM3dyMk1Rblk5U0UxS3B3eFZqTTB5Y3IKWTFDTVQ2Nm53QTVaS1F4dEJUb1ZWa1dCOW5OTEl6RHdhcVl4dHNmcGhDWHR0WUVZMTBzbmlMbmpWeDJ5aFgxYwplOFRTTXExY2FVQzVRdHBpbTYwRjVuNWNJc1hMbnRTRlpsNzJEUXpqOEp2Y0R4dmsxYjRETWRKUjNHM0M4bVZMCm9wNWhZVHZNdUFVQThvS0dPMkU4MVE9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCgo=",
                    'ssl-certificate': "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUV4ekNDQTYrZ0F3SUJBZ0lSQUpLUWZCSkxJZ2QvMUxpRGJaSU1EeGd3RFFZSktvWklodmNOQVFFTEJRQXcKVHpFVU1CSUdBMVVFQ2d3TGIzQmxibmRwWm1rdFluSXhJVEFmQmdOVkJBc01HRzl3Wlc1M2FXWnBMV0p5TG1WNApjSEpsYzNOZmQybG1hVEVVTUJJR0ExVUVBd3dMYjNCbGJuZHBabWt0WW5Jd0lCY05NakV3T0RJME1USXhOREE1CldoZ1BNakExTVRBNE1qUXhNekUwTURsYU1HOHhGekFWQmdOVkJBb01Ea1poWTJWaWIyOXJMQ0JKYm1NdU1SVXcKRXdZRFZRUUxEQXhsZUhCeVpYTnpJSGRwWm1reEd6QVpCZ05WQkFNTUVrTk1TVVZPVkY5dmNHVnVkMmxtYVMxaQpjakVMTUFrR0ExVUVCaE1DUVZVeEV6QVJCZ05WQkFnTUNsTnZiV1V0VTNSaGRHVXdnZ0lpTUEwR0NTcUdTSWIzCkRRRUJBUVVBQTRJQ0R3QXdnZ0lLQW9JQ0FRRFhNT0dIdWpycUZWUVpWMDJNcEVvblRsNHVpWmk4RnZSaEtFdEYKa0RZQ2FuMlNhMTA4azVDOU5CZnEzTjlBelk3bWdPNTB6blJRR0w1WVd5Y2FadmR6MFBMV1dHV1NIOE96dXpNYgp4N0hqZ05UaWpFVHdLNEU1MlJVU2lrT3dCN25lcHFEdmltbDJlSXNXZS9mdGxoc3dsU3UwVlpFbVhhcEt2T09zCkpHRTI2Uzd5MXIyNGxraE91RHRyYjVYK1h2NVJEVzZBVGNUVjJ6RHVhWGUycUs4MXNOVjlQYW5tNWlYQTZ2V1EKelVRVEpXRzJIU29mMFZVTVhqS0ZUakNZOS81NU9ab0lYclMvdnNiSUpPSWVxVVFXMkk3N1NRV2JPUk9sOUkzTgpHYjdkWnhsNHl4RUdrV2ZUUG5rYzFzNWFLSmJUekJ0NzZ2TUxnak5CdVZOSUhNOTNZbHNrSG5zVFAxWE9Ka1M3CktRc2tVRlNqUUZIelB3SC92TGk2bm9MUFJCelB3dzhLc0lLNjd3QnB0WDR6SVZvWmpMdjRaTTA0emVWR09yL2wKTHFXeXo4K05CRnlXOFQwWUNDdWROK1pZdXdiZGd5Qkp6aEd4VnEwUHY3VmFhVzlqZzZNMU1DMGI2ZTJ3YWNGawp3OUdWVWFENkxSY2V5alNwWHlZRW5vTVRBL1Azd1hNU29mUEd4eEIwaHlhMStKSnFLYzhOdER3RTY4U3pMcEtECkZtY3ZxMlI2ckdaVTNvVzlkTEdZblp1ODEwVTlvU3dadlMxcU0vOHZRYi81ZHlsM2k2WnN5QUF4YXdDWGdhaEsKTnBIUlIyeElWTmpLNFhJQlVUeHdjQVVyTWJLT25xd2JRQ3NjQmVkazZnYkordm5HRzB0eVN1Q0RydS8xQWh3VApwK2VFVVFJREFRQUJvM3d3ZWpBSkJnTlZIUk1FQWpBQU1COEdBMVVkSXdRWU1CYUFGS1RPK01ZMWVyTDhSbG54CmdpNjUxdmlSUDVLTk1CMEdBMVVkRGdRV0JCU3V4S3hQcWkvV2h6RXZIbUdMMjc2d2FyUkpFVEFPQmdOVkhROEIKQWY4RUJBTUNCYUF3SFFZRFZSMGxCQll3RkFZSUt3WUJCUVVIQXdFR0NDc0dBUVVGQndNQ01BMEdDU3FHU0liMwpEUUVCQ3dVQUE0SUJBUUJ0WkNNaFRZRTI3V29Gc0pVdGJvem5kTlpMdUs1QmVLckRuVDhMaFVuM1ZVRDI3d3p3CmNsQmxVandLVHlxQUtITU9lb1JZQTQvODlVd3YvRzZ5aWRhRzVjcWRZdnpUUzFHZ2hwT0x4emlkc0VOS25rTW8KVXBYV2FWMGltVzhWZjZRMm1DdUV0b1prTzBnZ3Q4RzFiQU9SaWYrc2JTcVJvNjJRYXhTa2ZQQUVZMmZKLy9SRQpZQ0JQbjJIaE1PaFhPSmRCMSswdE5TVFczWkVuajZBWUlRalFiNzV6MHVvMjRRYlc0bW5GQzJ2OENjbkFDcXBICmtZOHpNSExRczF4MG9RWVN6OVN2Qnh3SXNhL0wvS0FObFBiSFpEcEJJYmMrM0lHYUZCNGhwT0N3YTFaVHlvbXkKM3NHTDBLQjZ0eFNqWHJ3WDJrL0ExaUtUUk0zRi9ZSy96NXd1Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0KCg==",
                    'private-key': "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tDQpNSUlKUXdJQkFEQU5CZ2txaGtpRzl3MEJBUUVGQUFTQ0NTMHdnZ2twQWdFQUFvSUNBUURYTU9HSHVqcnFGVlFaDQpWMDJNcEVvblRsNHVpWmk4RnZSaEtFdEZrRFlDYW4yU2ExMDhrNUM5TkJmcTNOOUF6WTdtZ081MHpuUlFHTDVZDQpXeWNhWnZkejBQTFdXR1dTSDhPenV6TWJ4N0hqZ05UaWpFVHdLNEU1MlJVU2lrT3dCN25lcHFEdmltbDJlSXNXDQplL2Z0bGhzd2xTdTBWWkVtWGFwS3ZPT3NKR0UyNlM3eTFyMjRsa2hPdUR0cmI1WCtYdjVSRFc2QVRjVFYyekR1DQphWGUycUs4MXNOVjlQYW5tNWlYQTZ2V1F6VVFUSldHMkhTb2YwVlVNWGpLRlRqQ1k5LzU1T1pvSVhyUy92c2JJDQpKT0llcVVRVzJJNzdTUVdiT1JPbDlJM05HYjdkWnhsNHl4RUdrV2ZUUG5rYzFzNWFLSmJUekJ0NzZ2TUxnak5CDQp1Vk5JSE05M1lsc2tIbnNUUDFYT0prUzdLUXNrVUZTalFGSHpQd0gvdkxpNm5vTFBSQnpQd3c4S3NJSzY3d0JwDQp0WDR6SVZvWmpMdjRaTTA0emVWR09yL2xMcVd5ejgrTkJGeVc4VDBZQ0N1ZE4rWll1d2JkZ3lCSnpoR3hWcTBQDQp2N1ZhYVc5amc2TTFNQzBiNmUyd2FjRmt3OUdWVWFENkxSY2V5alNwWHlZRW5vTVRBL1Azd1hNU29mUEd4eEIwDQpoeWExK0pKcUtjOE50RHdFNjhTekxwS0RGbWN2cTJSNnJHWlUzb1c5ZExHWW5adTgxMFU5b1N3WnZTMXFNLzh2DQpRYi81ZHlsM2k2WnN5QUF4YXdDWGdhaEtOcEhSUjJ4SVZOaks0WElCVVR4d2NBVXJNYktPbnF3YlFDc2NCZWRrDQo2Z2JKK3ZuR0cwdHlTdUNEcnUvMUFod1RwK2VFVVFJREFRQUJBb0lDQVFDU3hQRWQzS1B3SWtudzJyMjJ6aHNSDQpnZjcwcUw1Mmt3VnMrc21VRVk3MHlPTUtxWlczQ2tLdStVZlMxWUNqdDAvZTRWTkNjY21kRTdOSG1pd3FjczRWDQp2UTdUcVFqbHlDcDNmSmVZTy9TVllicFJKakNpeWxsaU5qQ01LNmVNK1VnSmx3YXZPbTFCODJlU0YwMTdTMlVTDQpGcnZ2VEdrcWpMbm9MYnJ2SHdUN0tjSHV1UTQvUnFqY29BVk8rcFdJSUF3L0JmVTNKMU80Tkw3RDdVVk1YUExiDQpvTmVMaXpKRm5QVmxCaHdrL2d1UEwzRGNnRG5KNThHbEpONDZVNkVMeENGWlZ6TTZ3RFZ4amxJUUVpL3pqNmswDQpGOUkxaTVGNlZFeVZaUjRPSktBc2EvUlFrZGZ6N2RxdGxxK09QdWdSVUJ2SEt6QVhyYURGV2JGU0EyL05BSEZ6DQpEMWpwcDE0aG1iUVdBdWdiUHR6R09OeWRHM1hPQnA1MEs3UWRYaFQvMWVNQkp3TEoxejhkMkl1OTVEczZNdWpaDQorY3ZQS21mckkrR1kyYmE4VGZvS3h3VS9YaDd5c1BMMzB5eERESkdsanFXdjhjZHZ5SUl0cmZjOTNFb0Fqb3ZYDQpZaHVUbTlCWVFiTDgzTmJ2QWNPOEQzVitBWXdFSHNlYnlBMnVpVVhWRi8xUGVnenZVTVprQ2lZK1VMYnlFblQ0DQoyRnNzRlo2VXVLY3MvZW56RktMRk81ZmVsMXRPS2xRWElmVldPVkhJMzZqR1BFWGp5d2hIdm92Q3BHaDFRY3IvDQpPSkh1Nm1uMnNPQ3JVZ3d6Njl4VVJWd0hORWkwMjlZVSt2KzdjZHBOR25obVhWSHg0dWtIazY5ZFRVSUI2aHN5DQovVi9WeU11ZEwzRTBhRzlLdUcyQVVRS0NBUUVBLzZOd0UzK2tjNDAwcjlzR25nejNJTWlYbmF3cGQxV0ZUQVY0DQo5UGpIdklQNG5QNGdRTEtXbDFrL0pvcm5TTmNPcWJpUDB6MlNNZnhuRW05OEYzTHdBeHVNVkRkQkVrakxHSDY5DQpBZlJHeEtEcGNNTnR2VWpNcXhyRGc5dlRtNHZNcE5UTGV2VHhXajJ1YVVaNVV4YndXTVBLbURQd0p2Q2N2V05zDQpPUEpkSmM3NFBrcEJYdnNsSEVPem91T3REU0ZSaHlaak4xVzlXVGZTQjlKQXFhL3Y4c3pyTTBuWnFIYjdLUWdjDQpIK2RtNUJPWVF2MWl5WUlZRnk2bXJaL0xFUmRCbzlYYy9yaVY0azVrN1RvUVdkTEhNWERTYjh0YnVEbEVNRmlVDQp3bnNJTmE2QmFZSVVNQWdyYXRaYThWdC9pUUN1VGtyOVZqdldxRmtEVDlkd2ZYNGlUUUtDQVFFQTEzN01RQXBIDQpJdG1wbERTQ21obmlXek5nalZUY01NUGJuOGdwRFNaMDhzeTBxTkFIQ0UrMitrN0prQStPdWloT3BEdW1WMFprDQpINFdzSmpidmtwVkNPVU1UeXJsVlFNSjFRVURFbWRMc3lSc3VjNzEyZUp1TFVjSU5XaEtxN3hxL2xkU2c2UHpnDQp2a0VFYWZ6ZGJYakc1S2s0YUMvQVFMK0V6cjZmZTBaa1o3V2hURUdVYVd0cFRZQ002dVh2U3oySVZMNzNGREppDQo2RE45enBCZjJRQXo1RzdpaENMKzhGVlNOVkxEbHlaN3dLNmJ1UmhsT0MxekhwQndla1JQY1hZSkdUR1d6TkhmDQplZ1BsR1NIcFNxMnBqa1RWaXZuQ3J2REovejBidEdFYmRkQXhXUTk3R00xZDlPMDNKTmpRdC96RGVHSXBkTU9kDQpRNkM3bG40d1o5dUVGUUtDQVFFQXVuKytFRHVhK2tJV0lnV2tla0h6T1JPZXFRVWs2MDZWQkxVcFhXN3lLUElPDQp1bG9icFpla2paNHFtQy9XTkNuUkpMamxGTE5pcU56L1JVL1lORE5DTHNJMlNtcFZLc1c0aFpKUXlkQXdvTnJUDQo4OVJmaHl4SlJMc3QwRkRidkNydGpZTkJQOTdiQlg3aWN5TmE5K2RRU1RIdDU4UmNlOHdtVFhUdlMweGw4R05pDQpiKzgwYWRySFpDdHdMbkh6bWhTb3FmU3poWGNqd0tjY3IyQVFsTHNxVHZSNDB0NFowUEdjb242c0pncG40aFQ1DQpqRVhYZ0ROTTUveTgxUVl5MjdFZnppc0VJMEQrK0M5QkttQ2w5U0gwK0hqYXpYeUsyWWZOMjRlRVg2M3FlMTlvDQpRbFVIN1ZMSWVoVVFHKzBveWdhWkk3MUp2VlBDY3VjZHAyNEJQMHg2TVFLQ0FRQm1hYUpVUlE0dHA5Z0owVExJDQpYY2pQb3drZDRkaUxiR2x4OUVSZU5ZcWE0V0p5WC9zWG5ock50cWZnU1NTQm9DcFBydkdNeEsxTXRkQnNrT3NtDQpkTHoyVGNTWU1hQXNtTDMwOXZ6NFJkKzJhNjZWM3RMdzJxdEpmYm11dHZSNWtmSy9HRUFvdWhWdEZhVXRZYmt5DQpENVlta2ExM0JrcU4rdmI0OG1zRXdSMXlsRVZGNGx6UUJQWVVtU1ZmZFV0V0xMWWY0R200TllILzdJaTdwSzJJDQppYW9mdy9ydTVWclhpUlQ2dG95eHh0NUZZallycjBaYmZtNFpkbmVlQTl6bGhUMHB0Z0YrOGJjTlc5Q0RNelNXDQpBeFp6d0k3ajczTHdoUXJhdklYd0liNVZMVTVtanc3bmFLSmdobVFRcE9IOHJxbVBDc2U4OEVKTEk1WkRIVkdQDQo2aWxKQW9JQkFDSjNua09zKzR5Rkg2cnRSOExEdG1heWNqUVJ6WlRVUS8yem1CZXM3VUpPN3VHK1JtK2JXUmZrDQpQNDA1U29acEJ5eVpWbEt6dUh1Q2JHOVBWUUl5amU0MytiYVFGRTlLTnBQUWNiUVZWejJqTERTNFJYK1lPZDMvDQpMcHNsVHJhMGVOdFhNellocS9mY1V3cWI5YWxTOGFqODh6ZjFQM2tMK3QvaEpLa3RseERLVkdvL1ZycncwWEl1DQoxZkU0ZUExWXFPOE83UVQ3N1Z1SmRJNUp2TWtyalhBcEpIaFlxQ3VMYzFWSzR6anRCd1dpRkFnL1BrQ3poWDRPDQpiQVFYQWx6WnVpVTNDWHN5MzQzenpaSTZaanRUNFhjZlYxWFNKekE2RVNmdTZqSmVobE5DUzA0WkJ2ckhDaFp6DQpPSllTZEoxNmNGWTRta05yM3NEZmt6bW95UmFuNXY0PQ0KLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLQ=="
                }
            }
            self.base_profile_config['services'] = services
            wifi_frames = {
                'filters': ["probe",
                            "auth",
                            "assoc",
                            "disassoc",
                            "deauth",
                            "local-deauth",
                            "inactive-deauth",
                            "key-mismatch",
                            "beacon-report",
                            "radar-detected"
                            ]
            }

            dhcp_snooping = {
                "filters": ["ack",
                            "discover",
                            "offer",
                            "request",
                            "solicit",
                            "reply",
                            "renew"
                            ]
            }
            self.base_profile_config['metrics']['wifi-frames'] = wifi_frames
            self.base_profile_config['metrics']['dhcp-snooping'] = dhcp_snooping
        print(self.base_profile_config)


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

    def set_radio_config(self, radio_config=None):
        self.base_profile_config["radios"].append({
            "band": "2G",
            "country": "US",
            # "channel-mode": "HE",
            "channel-width": 40,
            # "channel": 11
        })
        self.base_profile_config["radios"].append({
            "band": "5G",
            "country": "US",
            # "channel-mode": "HE",
            "channel-width": 80,
            # "channel": "auto"
        })

        self.vlan_section["ssids"] = []
        self.vlan_ids = []

    def set_mode(self, mode):
        self.mode = mode
        if mode == "NAT":
            self.base_profile_config['interfaces'][1]['ssids'] = []
        elif mode == "BRIDGE":
            self.base_profile_config['interfaces'][0]['ssids'] = []
        elif mode == "VLAN":
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
        payload = {"configuration": self.base_profile_config, "serialNumber": serial_number, "UUID": 0}

        uri = self.sdk_client.build_uri("device/" + serial_number + "/configure")
        basic_cfg_str = json.dumps(payload)
        print(self.base_profile_config)
        allure.attach(name="ucentral_config: ",
                      body=str(self.base_profile_config).replace("'", '"'),
                      attachment_type=allure.attachment_type.JSON)
        print(self.base_profile_config)
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
        'url': 'https://sec-ucentral-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
        'username': "tip@ucentral.com",
        'password': 'openwifi',
    }
    obj = Controller(controller_data=controller)
    print(obj.get_sdk_version())
    # fms = FMSUtils(sdk_client=obj)
    # new = fms.get_firmwares(model='ecw5410')
    # for i in new:
    #     print(i)
    # print(len(new))


    # print(profile.get_ssid_info())
    # # print(obj.get_devices())
    obj.logout()
