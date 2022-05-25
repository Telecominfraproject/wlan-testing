"""

    UCentral Gateway Services Rest API Tests

"""

import string
import random

import pytest
import json
import allure


@pytest.mark.uc_sanity
@pytest.mark.gw_all_api
@allure.feature("SDK REST API")
class TestUcentralGatewayService(object):
    """
    """
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
                              "services": [ "lldp" ],
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
                              "services": [ "ssh", "lldp" ],
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
                              "types": [ "ssids", "lldp", "clients" ]
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
    def test_gwservice_listdevices(self, setup_controller):
        """
            Test the list devices endpoint
            WIFI-3452
        """
        resp = setup_controller.get_devices()
        print(resp.json())
        allure.attach(name="Devices", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.sdk_restapi
    @pytest.mark.gw_lsdev
    def test_gwservice_createdevice(self, setup_controller, testbed):
        """
            Test the create device endpoint
            WIFI-3453
        """
        device_mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                     random.randint(0, 255),
                                     random.randint(0, 255))
        device_name = device_mac.replace(":", "")
        # device_name = "deadbeef0011" + testbed.replace("-","")
        payload = {'serialNumber': device_name,
                   'UUID': '123456',
                   'configuration': self.configuration,
                   'deviceType': 'AP',
                   'location': '',
                   'macAddress': device_mac,
                   'manufacturer': 'Testing through Automation',
                   'owner': ''}
        print(json.dumps(payload))
        resp = setup_controller.add_device_to_gw(device_name, payload)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Gateway create device", body=body)
        if resp.status_code != 200:
            assert False
        devices = json.loads(resp.text)
        print(devices)

        resp = setup_controller.get_device_by_serial_number(device_name)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Gateway create device-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_controller.delete_device_from_gw(device_name)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw created device-delete", body=body)
        if resp.status_code != 200:
            assert False


    @pytest.mark.system_info_gw
    def test_system_info_gw(self, setup_controller):
        system_info = setup_controller.get_system_gw()
        print(system_info.json())
        allure.attach(name="system info", body=str(system_info.json()),attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200

