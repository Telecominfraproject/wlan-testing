"""

    Provision Services Rest API Tests

"""

import string
import random

import pytest
import json
import allure


@pytest.mark.uc_sanity
@allure.feature("SDK PROV REST API")
class TestUcentralProvisionService(object):

    configuration = {
        "uuid": 1,
        "radios": [
            {
                "band": "5G",
                "country": "CA",
                "channel-mode": "HE",
                "channel-width": 80
            }
        ],

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
                    "subnet": "192.168.1.1/24",
                    "dhcp": {
                        "lease-first": 10,
                        "lease-count": 100,
                        "lease-time": "6h"
                    }
                },
                "ssids": [
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

            }
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
                "describe": "2.x",
                "location": "universe"
            },
            "ssh": {
                "port": 22
            }
        }
    }

    @pytest.mark.sdk_restapi
    @pytest.mark.prov_api
    def test_provservice_inventorylist(self, setup_controller):
        """
            Test the list of devices present in Provisioning UI
        """
        resp = setup_controller.request("prov", "inventory", "GET", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="prov inventory list", body=body)
        if resp.status_code != 200:
            assert False
        inven = json.loads(resp.text)
        print(inven)

    @pytest.mark.prov_api_test
    def test_prov_service_create_inventory_device(self, setup_controller, testbed):
        """
            Test the create device in provision Inventory
        """
        device_mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                     random.randint(0, 255),
                                     random.randint(0, 255))
        device_name = device_mac.replace(":", "")
        # device_name = "deadbeef0011" + testbed.replace("-","")
        payload = {'serialNumber': device_name,
                   'devClass': 'any',
                   'rrm': 'off',
                   'deviceConfiguration': self.configuration,
                   'deviceType': 'edgecore_eap101',
                   'location': '',
                   'name': 'Testing'}
        print(json.dumps(payload))
        resp = setup_controller.request("prov", "inventory/" + device_name, "POST", None, json.dumps(payload))
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create devices", body=body)
        if resp.status_code != 200:
            assert False
        devices = json.loads(resp.text)
        print(devices)

        resp = setup_controller.request("prov", "inventory/" + device_name, "GET", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create device verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_controller.request("prov", "inventory/" + device_name, "DELETE", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create device delete", body=body)
        if resp.status_code != 200:
            assert False

    @pytest.mark.system_info_prov
    def test_system_info_prov(self, setup_controller):
        system_info = setup_controller.get_system_prov()
        print(system_info.json())
        allure.attach(name="system info", body=str(system_info.json()), attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200
