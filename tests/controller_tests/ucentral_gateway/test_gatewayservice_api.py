"""

    UCentral Gateway Services Rest API Tests

"""

import string
import random

import pytest
import json
import allure


@pytest.mark.uc_sanity
@pytest.mark.ow_sanity_lf
@pytest.mark.owgw_api_tests
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
    @pytest.mark.gw_cred_dev
    def test_gwservice_create_edit_delete_device(self, setup_controller, testbed):
        """
            Test the create & edit and delete device endpoint
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

        editing_payload = {
                          "id": device_name,
                          "notes": [
                            {
                              "note": "Testing through Automation"
                            }
                          ]
                        }
        print(json.dumps(editing_payload))
        resp = setup_controller.edit_device_on_gw(device_name, editing_payload)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Gateway edited device", body=body)
        if resp.status_code != 200:
            assert False
        devices = json.loads(resp.text)
        print(devices)

        resp = setup_controller.get_device_by_serial_number(device_name)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Gateway edited device-verify", body=body)
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

    @pytest.mark.gw_commands
    def test_gw_commands(self, setup_controller):
        system_info = setup_controller.get_commands()
        print(system_info.json())
        allure.attach(name="Gateway list of commands", body=str(system_info.json()), attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200

    @pytest.mark.gw_device_logs
    def test_gw_service_get_logs(self, setup_controller, get_configuration):
        """
            Test the device logs present in Gateway UI
        """
        device_name = get_configuration['access_point'][0]['serial']
        resp = setup_controller.get_device_logs(device_name)
        print(resp.json())
        allure.attach(name="Device Logs", body=str(resp.json()),attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_device_health_checks
    def test_gw_service_get_health_checks(self, setup_controller, get_configuration):
        """
            Test the device health checks present in Gateway UI
        """
        device_name = get_configuration['access_point'][0]['serial']
        resp = setup_controller.get_device_health_checks(device_name)
        print(resp.json())
        allure.attach(name="Device Health checks", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_device_capabilities
    def test_gw_service_get_capabilities(self, setup_controller, get_configuration):
        """
            Test the device capabilities present in Gateway UI
        """
        device_name = get_configuration['access_point'][0]['serial']
        resp = setup_controller.get_device_capabilities(device_name)
        print(resp.json())
        allure.attach(name="Device capabilities", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_device_statistics
    def test_gw_service_get_statistics(self, setup_controller, get_configuration):
        """
            Test the device statistics present in Gateway UI
        """
        device_name = get_configuration['access_point'][0]['serial']
        resp = setup_controller.get_device_statistics(device_name)
        print(resp.json())
        allure.attach(name="Device statistics", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_device_status
    def test_gw_service_get_status(self, setup_controller, get_configuration):
        """
            Test the device status present in Gateway UI
        """
        device_name = get_configuration['access_point'][0]['serial']
        resp = setup_controller.get_device_status(device_name)
        print(resp.json())
        allure.attach(name="Device status", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)

    @pytest.mark.gw_ping_device
    def test_gw_service_ping_device(self, setup_controller, get_configuration):
        """
            Test to Ping device present in Gateway UI
        """
        device_name = get_configuration['access_point'][0]['serial']
        payload = {
                  "serialNumber": device_name
                }
        print(json.dumps(payload))
        resp = setup_controller.ping_device(device_name, payload)
        print(resp.json())
        allure.attach(name="Device Ping status", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)

    @pytest.mark.gw_led_blink_device
    def test_gw_service_led_blink_device(self, setup_controller, get_configuration):
        """
            Test to Blink led on device present in Gateway UI
        """
        device_name = get_configuration['access_point'][0]['serial']
        payload = {
                  "serialNumber": device_name,
                  "when": 0,
                  "duration": 1,
                  "pattern": "on"
                }
        print(json.dumps(payload))
        resp = setup_controller.led_blink_device(device_name, payload)
        print(resp.json())
        allure.attach(name="Device Blink led status", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)

    @pytest.mark.gw_trace_device
    def test_gw_service_trace_device(self, setup_controller, get_configuration):
        """
            Test to trace device present in Gateway UI
        """
        device_name = get_configuration['access_point'][0]['serial']
        payload = {
                  "serialNumber": device_name,
                  "when": 0,
                  "duration": 1,
                  "numberOfPackets": 0,
                  "network": "string",
                  "interface": "string"
                }
        print(json.dumps(payload))
        resp = setup_controller.trace_device(device_name, payload)
        print(resp.json())
        allure.attach(name="Device trace status", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)

    @pytest.mark.gw_wifi_scan_device
    def test_gw_service_wifi_scan_device(self, setup_controller, get_configuration):
        """
            Test to Wifi scan device present in Gateway UI
        """
        device_name = get_configuration['access_point'][0]['serial']
        payload = {
                  "serialNumber": device_name,
                  "verbose": True,
                  "activeScan": True,
                  "selector": {
                    "bands": [
                      "2"
                    ]
                  }
                }
        print(json.dumps(payload))
        resp = setup_controller.wifi_scan_device(device_name, payload)
        print(resp.json())
        allure.attach(name="Device Wifi scan status", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)

    @pytest.mark.gw_request_msg_device
    def test_gw_service_request_msg_device(self, setup_controller, get_configuration):
        """
            Test to Request specific msg from device present in Gateway UI
        """
        device_name = get_configuration['access_point'][0]['serial']
        payload = {
                  "serialNumber": device_name,
                  "when": 0,
                  "message": "state"
                }
        print(json.dumps(payload))
        resp = setup_controller.request_specific_msg_from_device(device_name, payload)
        print(resp.json())
        allure.attach(name="Device Request specific msg status", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)

    @pytest.mark.gw_event_queue_device
    def test_gw_service_event_queue_device(self, setup_controller, get_configuration):
        """
            Test to Request Event Queue from device present in Gateway UI
        """
        device_name = get_configuration['access_point'][0]['serial']
        payload = {
                  "serialNumber": device_name,
                  "types": [
                    "dhcp"
                  ]
                }
        print(json.dumps(payload))
        resp = setup_controller.event_queue(device_name, payload)
        print(resp.json())
        allure.attach(name="Device Request Event Queue status", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)

    @pytest.mark.gw_telemetry_device
    def test_gw_service_telemetry_device(self, setup_controller, get_configuration):
        """
            Test to Request telemetry from device present in Gateway UI
        """
        device_name = get_configuration['access_point'][0]['serial']
        payload = {
                  "serialNumber": device_name,
                  "interval": 0,
                  "lifetime": 0,
                  "kafka": False,
                  "types": [
                    "dhcp-snooping"
                  ],
                  "uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                }
        print(json.dumps(payload))
        resp = setup_controller.telemetry(device_name, payload)
        print(resp.json())
        allure.attach(name="Device telemetry status", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)

    @pytest.mark.gw_rtty
    def test_gw_service_get_rtty(self, setup_controller, get_configuration):
        """
            Test the device rtty parameters in Gateway UI
        """
        device_name = get_configuration['access_point'][0]['serial']
        resp = setup_controller.get_rtty_params(device_name)
        print(resp.json())
        allure.attach(name="Device RTTY parameters", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200
