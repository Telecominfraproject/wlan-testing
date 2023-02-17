"""

    UCentral Gateway Services Rest API Tests

"""

import json
import logging
import random
from time import sleep

import allure
import pytest


@pytest.mark.uc_sanity
@pytest.mark.ow_sdk_tests
@pytest.mark.ow_sanity_lf
@pytest.mark.ow_sdk_load_tests
@pytest.mark.owgw_api_tests
@allure.parent_suite("SDK Tests")
@allure.suite("Gateway Service Tests")
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
    @allure.testcase(name="WIFI-11399",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11399")
    @pytest.mark.get_all_devices
    def test_gwservice_listdevices(self, get_target_object):
        """
            Test the list of devices endpoint
            Unique marker: pytest -m "get_all_devices"
        """
        resp = get_target_object.controller_library_object.get_devices()
        # print(resp.json())
        # allure.attach(name="Devices", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_crud_dev
    @allure.title("CRUD Device")
    @allure.testcase(name="WIFI-11399",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11399")
    @pytest.mark.CRUD
    def test_gwservice_create_read_edit_delete_device(self, get_target_object, selected_testbed):
        """
            Test to create,read,edit and delete device endpoint
            Unique marker: pytest -m "CRUD"
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
    @allure.testcase(name="WIFI-11436",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11436")
    @pytest.mark.OW_gateway_service
    def test_system_info_gw(self, get_target_object):
        """
        Test to verify OW gateway services
        Unique marker: pytest -m "OW_gateway_service"
        """
        system_info = get_target_object.controller_library_object.get_system_gw()
        # print(system_info.json())
        # allure.attach(name="system info", body=str(system_info.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert system_info.status_code == 200

    @pytest.mark.gw_commands
    @allure.title("Get OW Gateway Commands")
    @allure.testcase(name="WIFI-11437",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11437")
    def test_gw_commands(self, get_target_object, get_testbed_details):
        """
        Test to verify OW gateway commands executed
        Unique marker: pytest -m "gw_commands"
        """

        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        resp = get_target_object.controller_library_object.get_commands(device_name)
        # print(resp.json())
        # allure.attach(name="Gateway list of commands", body=str(system_info.json()),
        assert resp.status_code == 200

    @pytest.mark.gw_device_logs
    @allure.title("Get Device Logs")
    @allure.testcase(name="WIFI-11438",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11438")
    def test_gw_service_get_logs(self, get_target_object, get_testbed_details):
        """
            Test the device logs present in Gateway UI
            Unique marker:pytest -m "gw_device_logs"
        """
        print("XXXXXXX", get_testbed_details)
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        resp = get_target_object.controller_library_object.get_device_logs(device_name)
        # print(resp.json())
        # allure.attach(name="Device Logs", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_device_health_checks
    @allure.title("Get Health Checks")
    @allure.testcase(name="WIFI-11439",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11439")
    def test_gw_service_get_health_checks(self, get_target_object, get_testbed_details):
        """
            Test the device health checks present in Gateway UI
            Unique marker:pytest -m "gw_device_health_checks"
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        resp = get_target_object.controller_library_object.get_device_health_checks(device_name)
        # print(resp.json())
        # allure.attach(name="Device Health checks", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_device_capabilities
    @allure.title("Get Capabilities")
    @allure.testcase(name="WIFI-11441",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11441")
    def test_gw_service_get_capabilities(self, get_target_object, get_testbed_details):
        """
            Test the device capabilities present in Gateway UI
            Unique marker:pytest -m "gw_device_capabilities"
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        resp = get_target_object.controller_library_object.get_device_capabilities(device_name)
        # print(resp.json())
        # allure.attach(name="Device capabilities", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200
        return resp

    @pytest.mark.gw_device_statistics
    @allure.title("Get Statistics")
    @allure.testcase(name="WIFI-11442",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11442")
    def test_gw_service_get_statistics(self, get_target_object, get_testbed_details):
        """
            Test the device statistics present in Gateway UI
            Unique marker: pytest -m "gw_device_statistics"
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        resp = get_target_object.controller_library_object.get_device_statistics(device_name)
        # print(resp.json())
        # allure.attach(name="Device statistics", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_device_status
    @allure.title("Get Device Status")
    @allure.testcase(name="WIFI-11443",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11443")
    def test_gw_service_get_status(self, get_target_object, get_testbed_details):
        """
            Test the device status present in Gateway UI
            Unique marker: pytest -m "gw_device_status"
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        resp = get_target_object.controller_library_object.get_device_status(device_name)
        # print(resp.json())
        # allure.attach(name="Device status", body=str(resp.json()), #attachment_type=#allure.#attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.gw_ping_device
    @allure.title("Ping Device")
    @allure.testcase(name="WIFI-11444",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11444")
    def test_gw_service_ping_device(self, get_target_object, get_testbed_details):
        """
            Test to Ping device present in Gateway UI
            Unique marker:pytest -m "gw_ping_device"
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
    @allure.testcase(name="WIFI-11445",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11445")
    def test_gw_service_led_blink_device(self, get_target_object, get_testbed_details):
        """
            Test to Blink led on device present in Gateway UI
            Unique marker: pytest -m "gw_led_blink_device"
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
    @allure.testcase(name="WIFI-11446",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11446")
    def test_gw_service_trace_device(self, get_target_object, get_testbed_details):
        """
            Test to trace device present in Gateway UI
            Unique marker:pytest -m "gw_trace_device"
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
    @allure.testcase(name="WIFI-11447",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11447")
    def test_gw_service_wifi_scan_device(self, get_target_object, get_testbed_details):
        """
            Test to Wi-Fi scan device present in Gateway UI
            Unique marker:pytest -m "gw_wifi_scan_device"
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
    @allure.testcase(name="WIFI-11448",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11448")
    def test_gw_service_request_msg_device(self, get_target_object, get_testbed_details):
        """
            Test to Request specific msg from device present in Gateway UI
            Unique marker:pytest -m "gw_request_msg_device"
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
    @allure.testcase(name="WIFI-11452",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11452")
    def test_gw_service_event_queue_device(self, get_target_object, get_testbed_details):
        """
            Test to Request Event Queue from device present in Gateway UI
            Unique marker:pytest -m "gw_event_queue_device"
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
    @allure.testcase(name="WIFI-11453",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11453")
    def test_gw_service_telemetry_device(self, get_target_object, get_testbed_details):
        """
            Test to Request telemetry from device present in Gateway UI
            Unique marker:pytest -m "gw_telemetry_device"
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

    @pytest.mark.gw_asb_non_restricted
    @allure.title("Asb script on non restricted AP")
    @allure.testcase(name="WIFI-12235", url="https://telecominfraproject.atlassian.net/browse/WIFI-12235")
    def test_asb_on_non_restricted_ap(self, get_target_object, get_testbed_details):
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        payload = {
            "serialNumber": device_name,
            "timeout": 30,
            "type": "diagnostic",
            "script": "",
            "scriptId": "",
            "when": 0,
            "signature": "",
            "deferred": True,
            "uri": ""
        }
        resp = resp = get_target_object.controller_library_object.check_restrictions(device_name)
        if not resp:
            logging.info("AP is in not restricted and we can trigger script")
            uuid = get_target_object.controller_library_object.asb_script(device_name, payload)
            resp = get_target_object.controller_library_object.get_file(device_name, uuid)
            assert resp.status_code == 200
        else:
            logging.info("AP is restricted, Removing Restrictions")
            output = get_target_object.get_dut_library_object().remove_restrictions()
            resp = resp = get_target_object.controller_library_object.check_restrictions(device_name)
            if not resp:
                logging.info("Removed Restrictions")
                uuid = get_target_object.controller_library_object.asb_script(device_name, payload)
                resp = get_target_object.controller_library_object.get_file(device_name, uuid)
                assert resp.status_code == 200
            else:
                logging.info("Unable to remove restrictions")
                assert False

    @pytest.mark.gw_asb_restricted
    @allure.title("Asb script on restricted AP")
    @allure.testcase(name="WIFI-12236", url="https://telecominfraproject.atlassian.net/browse/WIFI-12236")
    def test_asb_on_restricted_ap(self, get_target_object, get_testbed_details):
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        payload = {
            "serialNumber": device_name,
            "timeout": 30,
            "type": "diagnostic",
            "script": "",
            "scriptId": "",
            "when": 0,
            "signature": "",
            "deferred": True,
            "uri": ""
        }
        restrictions_file = 'echo \"{\\"country\\":[\\"US\\", \\"CA\\"],\\"dfs\\": true,\\"rtty\\": true,\\"tty\\": ' \
                            'true,\\"developer\\": true,\\"sysupgrade\\": true,\\"commands\\": true,\\"key_info\\": {' \
                            '\\"vendor\\": \\"dummy\\",\\"algo\\": \\"static\\"}}\" > /certificates/restrictions.json ' \
                            '&& echo \"True\"'
        developer_mode = "fw_setenv developer 0"
        output = get_target_object.get_dut_library_object().add_restrictions(restrictions_file=restrictions_file,
                                                                             developer_mode=developer_mode)
        resp = resp = get_target_object.controller_library_object.check_restrictions(device_name)
        if resp:
            logging.info("From GW it's confirmed that AP is restricted now")
            uuid = get_target_object.controller_library_object.asb_script(device_name, payload)
            resp = get_target_object.controller_library_object.get_file(device_name, uuid)
            assert resp.status_code == 200
        else:
            assert False
        output = get_target_object.get_dut_library_object().remove_restrictions()
        resp = resp = get_target_object.controller_library_object.check_restrictions(device_name)
        if resp:
            logging.info("Unable to remove restrictions in the AP")
            assert False
        else:
            logging.info("Removed Restrictions")



