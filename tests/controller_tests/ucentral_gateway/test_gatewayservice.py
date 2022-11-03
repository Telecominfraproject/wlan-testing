"""

    UCentral Gateway Services Rest API Tests

"""

import json
import random

import allure
import pytest


@pytest.mark.uc_sanity
@pytest.mark.ow_sdk_tests
@pytest.mark.ow_sanity_lf
@pytest.mark.ow_sdk_load_tests
@pytest.mark.owgw_api_tests
@allure.parent_suite("OpenWifi SDK Tests")
@allure.suite("OpenWifi Gateway Service Tests")
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

    @allure.title("Get All Devices")
    def test_gwservice_listdevices(self, get_target_object):
        """
            Test the list devices endpoint
            WIFI-3452
        """
        resp = get_target_object.controller_library_object.get_devices()
        # print(resp.json())
        # allure.attach(name="Devices", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_crud_dev
    @allure.title("CRUD Device")
    def test_gwservice_create_edit_delete_device(self, get_target_object, selected_testbed):
        """
            Test the creation & updation and delete device endpoint
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
        # print(json.dumps(payload))
        resp = get_target_object.controller_library_object.add_device_to_gw(device_name, payload)
        # allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        # allure.attach(name="Gateway create device", body=body)
        if resp.status_code != 200:
            assert False
        devices = json.loads(resp.text)
        # print(devices)

        resp = get_target_object.controller_library_object.get_device_by_serial_number(device_name)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        # allure.attach(name="Gateway create device-verify", body=body)
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
        # print(json.dumps(editing_payload))
        resp = get_target_object.controller_library_object.edit_device_on_gw(device_name, editing_payload)
        # allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        # allure.attach(name="Gateway edited device", body=body)
        if resp.status_code != 200:
            assert False
        devices = json.loads(resp.text)
        # print(devices)

        resp = get_target_object.controller_library_object.get_device_by_serial_number(device_name)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        # allure.attach(name="Gateway edited device-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = get_target_object.controller_library_object.delete_device_from_gw(device_name)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        # allure.attach(name="gw created device-delete", body=body)
        if resp.status_code != 200:
            assert False

    @pytest.mark.system_info_gw
    @allure.title("System Info OW Gateway Service")
    def test_system_info_gw(self, get_target_object):
        system_info = get_target_object.controller_library_object.get_system_gw()
        # print(system_info.json())
        # allure.attach(name="system info", body=str(system_info.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert system_info.status_code == 200

    @pytest.mark.gw_commands
    @allure.title("Get OW Gateway Commands")
    def test_gw_commands(self, get_target_object, get_testbed_details):
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        resp = get_target_object.controller_library_object.get_commands(device_name)
        # print(resp.json())
        # allure.attach(name="Gateway list of commands", body=str(system_info.json()),
        assert resp.status_code == 200

    @pytest.mark.gw_device_logs
    @allure.title("Get Device Logs")
    def test_gw_service_get_logs(self, get_target_object, get_testbed_details):
        """
            Test the device logs present in Gateway UI
        """
        print("XXXXXXX", get_testbed_details)
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        resp = get_target_object.controller_library_object.get_device_logs(device_name)
        # print(resp.json())
        # allure.attach(name="Device Logs", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_device_health_checks
    @allure.title("Get Health Checks")
    def test_gw_service_get_health_checks(self, get_target_object, get_testbed_details):
        """
            Test the device health checks present in Gateway UI
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        resp = get_target_object.controller_library_object.get_device_health_checks(device_name)
        # print(resp.json())
        # allure.attach(name="Device Health checks", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_device_capabilities
    @allure.title("Get Capabilities")
    def test_gw_service_get_capabilities(self, get_target_object, get_testbed_details):
        """
            Test the device capabilities present in Gateway UI
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        resp = get_target_object.controller_library_object.get_device_capabilities(device_name)
        # print(resp.json())
        # allure.attach(name="Device capabilities", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_device_statistics
    @allure.title("Get Statistics")
    def test_gw_service_get_statistics(self, get_target_object, get_testbed_details):
        """
            Test the device statistics present in Gateway UI
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        resp = get_target_object.controller_library_object.get_device_statistics(device_name)
        # print(resp.json())
        # allure.attach(name="Device statistics", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_device_status
    @allure.title("Get Device Status")
    def test_gw_service_get_status(self, get_target_object, get_testbed_details):
        """
            Test the device status present in Gateway UI
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        resp = get_target_object.controller_library_object.get_device_status(device_name)
        # print(resp.json())
        # allure.attach(name="Device status", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_ping_device
    @allure.title("Ping Device")
    def test_gw_service_ping_device(self, get_target_object, get_testbed_details):
        """
            Test to Ping device present in Gateway UI
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        payload = {
            "serialNumber": device_name
        }
        # print(json.dumps(payload))
        resp = get_target_object.controller_library_object.ping_device(device_name, payload)
        # print(resp.json())
        # allure.attach(name="Device Ping status", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_led_blink_device
    @allure.title("Blink LED API")
    def test_gw_service_led_blink_device(self, get_target_object, get_testbed_details):
        """
            Test to Blink led on device present in Gateway UI
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        payload = {
            "serialNumber": device_name,
            "when": 0,
            "duration": 1,
            "pattern": "on"
        }
        # print(json.dumps(payload))
        resp = get_target_object.controller_library_object.led_blink_device(device_name, payload)
        # print(resp.json())
        # allure.attach(name="Device Blink led status", body=str(resp.json()),
        # attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_trace_device
    @allure.title("Trace Command")
    def test_gw_service_trace_device(self, get_target_object, get_testbed_details):
        """
            Test to trace device present in Gateway UI
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        payload = {
            "serialNumber": device_name,
            "when": 0,
            "duration": 1,
            "numberOfPackets": 0,
            "network": "string",
            "interface": "string"
        }
        # print(json.dumps(payload))
        resp = get_target_object.controller_library_object.trace_device(device_name, payload)
        # print(resp.json())
        # allure.attach(name="Device trace status", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_wifi_scan_device
    @allure.title("Wi-Fi Scan Device")
    def test_gw_service_wifi_scan_device(self, get_target_object, get_testbed_details):
        """
            Test to Wifi scan device present in Gateway UI
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
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
        # print(json.dumps(payload))
        resp = get_target_object.controller_library_object.wifi_scan_device(device_name, payload)
        # print(resp.json())
        # allure.attach(name="Device Wifi scan status", body=str(resp.json()),
        # attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_request_msg_device
    @allure.title("Request Message Device")
    def test_gw_service_request_msg_device(self, get_target_object, get_testbed_details):
        """
            Test to Request specific msg from device present in Gateway UI
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        payload = {
            "serialNumber": device_name,
            "when": 0,
            "message": "state"
        }
        # print(json.dumps(payload))
        resp = get_target_object.controller_library_object.request_specific_msg_from_device(device_name, payload)
        # print(resp.json())
        # allure.attach(name="Device Request specific msg status", body=str(resp.json()),
        # attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_event_queue_device
    @allure.title("Get Event Queue of Device")
    def test_gw_service_event_queue_device(self, get_target_object, get_testbed_details):
        """
            Test to Request Event Queue from device present in Gateway UI
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        payload = {
            "serialNumber": device_name,
            "types": [
                "dhcp"
            ]
        }
        # print(json.dumps(payload))
        resp = get_target_object.controller_library_object.event_queue(device_name, payload)
        # print(resp.json())
        # allure.attach(name="Device Request Event Queue status", body=str(resp.json()),
        # attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_telemetry_device
    @allure.title("Telemetry Device")
    def test_gw_service_telemetry_device(self, get_target_object, get_testbed_details):
        """
            Test to Request telemetry from device present in Gateway UI
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
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
        # print(json.dumps(payload))
        resp = get_target_object.controller_library_object.telemetry(device_name, payload)
        # print(resp.json())
        # allure.attach(name="Device telemetry status", body=str(resp.json()),
        # attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200


@pytest.mark.gw_rtty
@pytest.mark.ow_sdk_load_tests
@pytest.mark.owgw_api_tests
@allure.title("RTTY API")
def test_gw_service_get_rtty(self, get_target_object, get_testbed_details):
    """
        Test the device rtty parameters in Gateway UI
    """
    device_name = get_testbed_details['device_under_tests'][0]['identifier']
    resp = get_target_object.controller_library_object.get_rtty_params(device_name)
    # print(resp.json())
    # allure.attach(name="Device RTTY parameters", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
    assert resp.status_code == 200
