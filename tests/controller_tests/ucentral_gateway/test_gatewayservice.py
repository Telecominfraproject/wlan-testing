"""

    UCentral Gateway Services Rest API Tests

"""
import pytest
import json
import allure


@pytest.mark.uc_sanity
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
        resp = setup_controller.request("gw", "devices", "GET", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw list devices", body=body)
        if resp.status_code != 200:
            assert False
        devices = json.loads(resp.text)
        print(devices)

    @pytest.mark.sdk_restapi
    def test_gwservice_createdevice(self, setup_controller):
        """
            Test the create device endpoint
            WIFI-3453
        """

        payload = {'serialNumber': 'deadbeef0011',
                   'UUID': '123456',
                   'configuration': self.configuration,
                   'deviceType': 'AP',
                   'location': '',
                   'macAddress': 'DE:AD:BE:EF:00:11',
                   'manufacturer': 'Testing',
                   'owner': ''}
        print(json.dumps(payload))
        resp = setup_controller.request("gw", "device/deadbeef0011", "POST", None, json.dumps(payload))
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw create devices", body=body)
        if resp.status_code != 200:
            assert False
        devices = json.loads(resp.text)
        print(devices)

        resp = setup_controller.request("gw", "device/deadbeef0011", "GET", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw create device verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_controller.request("gw", "device/deadbeef0011", "DELETE", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw create device delete", body=body)
        if resp.status_code != 200:
            assert False
    '''
    @pytest.mark.sdk_restapi
    def test_gwservice_updatedevice(self, setup_controller):
        """
            Test the update device endpoint
            WIFI-3454
        """
        payload = {'serialNumber': 'deadbeef0011',
                   'UUID': '123456',
                   'configuration': self.configuration,
                   'deviceType': 'AP',
                   'location': '',
                   'macAddress': 'DE:AD:BE:EF:00:11',
                   'manufacturer': 'Testing',
                   'owner': ''}
        resp = setup_controller.request("gw", "device/deadbeef0011", "POST", None, json.dumps(payload))
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw create devices", body=body)
        if resp.status_code != 200:
            assert False
        devices = json.loads(resp.text)
        print(devices)

        payload = {'serialNumber': 'deadbeef0011',
                   'notes': [{"note": "This is a test"}]}
        resp = setup_controller.request("gw", "device/deadbeef0011", "PUT", None, json.dumps(payload))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw get device", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_controller.request("gw", "device/deadbeef0011", "GET", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw create device verify", body=body)
        if resp.status_code != 200:
            assert False

        device = json.loads(resp.text)
        print(device)

        resp = setup_controller.request("gw", "device/deadbeef0011", "DELETE", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="gw get device", body=body)
        if resp.status_code != 200:
            assert False

        @pytest.mark.sdk_restapi
        def test_gwservice_deletedevice(self, setup_controller):
            """
                Test the delete device endpoint
                WIFI-3455
            """
            payload = {'serialNumber': 'deadbeef0011',
                       'UUID': '123456',
                       'configuration': self.configuration,
                       'deviceType': 'AP',
                       'location': 'testing',
                       'macAddress': 'DE:AD:BE:EF:00:11',
                       'manufacturer': 'Testing',
                       'owner': ''}
            resp = setup_controller.request("gw", "device/deadbeef0011", "POST", None, json.dumps(payload))
            body = resp.url + "," + str(resp.status_code) + ',' + resp.text
            allure.attach(name="gw create devices", body=body)
            if resp.status_code != 200:
                assert False
            devices = json.loads(resp.text)
            print(devices)

            resp = setup_controller.request("gw", "device/deadbeef0011", "DELETE", None, None)
            body = resp.url + "," + str(resp.status_code) + ',' + resp.text
            allure.attach(name="gw get device", body=body)
            if resp.status_code != 200:
                assert False
    '''

    @pytest.mark.system_info_gw
    def test_system_info_gw(self, setup_controller):
        system_info = setup_controller.get_system_gw()
        print(system_info.json())
        allure.attach(name="system info", body=system_info.json(),attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200

    @pytest.mark.system_info_gw
    def test_system_info_fms(self, setup_controller):
        system_info = setup_controller.get_system_fms()
        print(system_info.json())
        allure.attach(name="system info", body=system_info.json(), attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200