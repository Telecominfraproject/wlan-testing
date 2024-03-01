"""

    UCentral Gateway Services Rest API Tests

"""

import json
import logging
import random
import datetime
import re
import time
from time import sleep

import allure
import pytest
import requests


@pytest.mark.uc_sanity
@pytest.mark.ow_sdk_tests
@pytest.mark.ow_sdk_load_tests
@pytest.mark.owgw_api_tests
@allure.parent_suite("SDK Tests")
@allure.suite("Gateway Service Tests")
class TestUcentralGatewayService(object):
    """
    """
    configuration = {
        "uuid": 2,
        "radios": [
            {
                "band": "5G",
                "channel": 52,
                "channel-mode": "HE",
                "channel-width": 80,
                "country": "CA"
            },
            {
                "band": "2G",
                "channel": 11,
                "channel-mode": "HE",
                "channel-width": 20,
                "country": "CA"
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
                            "2G", "5G"
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
                }
            }
        ],
        "metrics": {
            "statistics": {
                "interval": 120,
                "types": ["ssids", "lldp", "clients"]
            },
            "health": {
                "interval": 120
            },
            "wifi-frames": {
                "filters": ["probe", "auth"]
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

    @allure.title("Get All Devices")
    @allure.testcase(name="WIFI-11399",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-11399")
    @pytest.mark.get_all_devices
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_sanity_lf
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
    @pytest.mark.ow_regression_lf
    @pytest.mark.asb_tests
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
    @pytest.mark.ow_regression_lf
    @pytest.mark.asb_tests
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

    @pytest.mark.gw_list_of_OUIs
    @allure.title("Get a list of OUIs")
    @allure.testcase(name="WIFI-12554",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12554")
    def test_gw_service_get_list_of_OUIs(self, get_target_object, get_testbed_details):
        """
            Get a list of OUIs
            Unique marker:pytest -m "gw_list_of_OUIs"
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        mac_list = ':'.join(device_name[i:i + 2] for i in range(0, len(device_name), 2))
        resp = get_target_object.controller_library_object.get_list_of_OUIs(maclist=mac_list)
        assert resp.status_code == 200

    @pytest.mark.gw_list_of_scripts
    @allure.title("Get a list scripts")
    @allure.testcase(name="WIFI-12555",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12555")
    def test_gw_service_get_list_of_scripts(self, get_target_object, get_testbed_details):
        """
            Get a list scripts
            Unique marker:pytest -m "gw_list_of_scripts"
        """
        resp = get_target_object.controller_library_object.get_list_of_scripts()
        assert resp.status_code == 200

    @pytest.mark.gw_delete_update_read_radius_proxy_configuration
    @allure.title("Delete, Update, Read RADIUS Proxy configuration")
    @allure.testcase(name="WIFI-12557",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12557")
    def test_gw_service_delete_update_read_radius_proxy_configuration(self, get_target_object, get_testbed_details):
        """
            Delete, Update, read RADIUS Proxy configuration
            Unique marker:pytest -m "gw_delete_update_read_radius_proxy_configuration"
        """
        # Delete RADIUS Proxy configuration
        resp = get_target_object.controller_library_object.delete_radius_proxy_configuration()
        assert resp.status_code == 200
        # Modify RADIUS Proxy configuration
        editing_payload = {
            "pools": [
                {
                    "acctConfig": {
                        "methodParameters": [],
                        "monitor": False,
                        "monitorMethod": "none",
                        "servers": [
                            {
                                "allowSelfSigned": False,
                                "certificate": "",
                                "ignore": False,
                                "ip": "10.10.1.221",
                                "name": "svr1",
                                "port": 1813,
                                "radsec": False,
                                "radsecCacerts": [],
                                "radsecCert": "",
                                "radsecKey": "",
                                "radsecPort": 2083,
                                "radsecRealms": [],
                                "radsecSecret": "",
                                "secret": "testing123",
                                "weight": 10
                            },
                            {
                                "allowSelfSigned": False,
                                "certificate": "",
                                "ignore": False,
                                "ip": "10.10.1.221",
                                "name": "svr2",
                                "port": 1813,
                                "radsec": False,
                                "radsecCacerts": [],
                                "radsecCert": "",
                                "radsecKey": "",
                                "radsecPort": 2083,
                                "radsecRealms": [],
                                "radsecSecret": "",
                                "secret": "testing123",
                                "weight": 20
                            }
                        ],
                        "strategy": "random"
                    },
                    "authConfig": {
                        "methodParameters": [],
                        "monitor": False,
                        "monitorMethod": "none",
                        "servers": [
                            {
                                "allowSelfSigned": False,
                                "certificate": "",
                                "ignore": False,
                                "ip": "10.10.1.221",
                                "name": "svr1",
                                "port": 1812,
                                "radsec": False,
                                "radsecCacerts": [],
                                "radsecCert": "",
                                "radsecKey": "",
                                "radsecPort": 2083,
                                "radsecRealms": [],
                                "radsecSecret": "",
                                "secret": "testing123",
                                "weight": 10
                            },
                            {
                                "allowSelfSigned": False,
                                "certificate": "",
                                "ignore": False,
                                "ip": "10.10.1.221",
                                "name": "svr2",
                                "port": 1812,
                                "radsec": False,
                                "radsecCacerts": [],
                                "radsecCert": "",
                                "radsecKey": "",
                                "radsecPort": 2083,
                                "radsecRealms": [],
                                "radsecSecret": "",
                                "secret": "testing123",
                                "weight": 20
                            }
                        ],
                        "strategy": "weighted"
                    },
                    "coaConfig": {
                        "methodParameters": [],
                        "monitor": False,
                        "monitorMethod": "none",
                        "servers": [
                            {
                                "allowSelfSigned": False,
                                "certificate": "",
                                "ignore": False,
                                "ip": "10.10.1.221",
                                "name": "svr1",
                                "port": 3799,
                                "radsec": False,
                                "radsecCacerts": [],
                                "radsecCert": "",
                                "radsecKey": "",
                                "radsecPort": 2083,
                                "radsecRealms": [],
                                "radsecSecret": "",
                                "secret": "testing123",
                                "weight": 10
                            },
                            {
                                "allowSelfSigned": False,
                                "certificate": "",
                                "ignore": False,
                                "ip": "10.10.1.221",
                                "name": "svr2",
                                "port": 3799,
                                "radsec": False,
                                "radsecCacerts": [],
                                "radsecCert": "",
                                "radsecKey": "",
                                "radsecPort": 2083,
                                "radsecRealms": [],
                                "radsecSecret": "",
                                "secret": "testing123",
                                "weight": 20
                            }
                        ],
                        "strategy": "round_robin"
                    },
                    "description": "master pool",
                    "name": "master",
                    "useByDefault": True
                }
            ]
        }
        resp = get_target_object.controller_library_object.modify_radius_proxy_configuration(editing_payload)
        assert resp.status_code == 200
        # Retrieve RADIUS Proxy configuration
        resp = get_target_object.controller_library_object.get_radius_proxy_configuration()
        assert resp.status_code == 200

    @pytest.mark.gw_country_code_for_ip_address
    @allure.title("Get the country code for an IP address")
    @allure.testcase(name="WIFI-12558",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12558")
    def test_gw_service_get_country_code_for_ip_address(self, get_target_object, get_testbed_details):
        """
            Get the country code for an IP address
            Unique marker:pytest -m "gw_country_code_for_ip_address"
        """
        iplist = get_testbed_details['device_under_tests'][0]['host_ip']
        print("iplist", iplist)
        resp = get_target_object.controller_library_object.get_country_code_for_ip_address(iplist=iplist)
        assert resp.status_code == 200

    @pytest.mark.gw_lists_of_all_default_configurations
    @allure.title("Get lists of all default configurations")
    @allure.testcase(name="WIFI-12553",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12553")
    def test_gw_service_get_lists_of_all_default_configurations(self, get_target_object, get_testbed_details):
        """
            Retrieve the lists of all default configurations
            Unique marker:pytest -m "gw_lists_of_all_default_configurations"
        """
        resp = get_target_object.controller_library_object.get_lists_of_all_default_configurations()
        assert resp.status_code == 200

    @allure.title("CRUD a default configuration")
    @allure.testcase(name="WIFI-12619",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12619")
    @pytest.mark.gw_crud_default_configuration
    def test_gw_service_create_read_edit_delete_default_configuration(self, get_target_object, get_testbed_details):
        """
            Test to create,read,edit and delete default configuration
            Unique marker: pytest -m "gw_crud_default_configuration"
        """
        device_mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                                  random.randint(0, 255),
                                                  random.randint(0, 255))
        device_name = device_mac.replace(":", "")
        model = get_testbed_details['device_under_tests'][0]['model']
        # device_name = "deadbeef0011" + testbed.replace("-","")
        payload = {'name': device_name,
                   "modelIds": [model],
                   "description": "Testing through Automation",
                   'configuration': self.configuration,
                   "created": 0,
                   "lastModified": 0
                   }
        resp = get_target_object.controller_library_object.create_default_configuration(device_name, payload)
        if resp.status_code != 200:
            assert False
        resp = get_target_object.controller_library_object.get_default_configuration(device_name)
        if resp.status_code != 200:
            assert False

        editing_payload = {
            "description": "edit_default_configuration"
        }
        # print(json.dumps(editing_payload))
        resp = get_target_object.controller_library_object.edit_default_configuration(device_name, editing_payload)
        if resp.status_code != 200:
            assert False

        resp = get_target_object.controller_library_object.delete_default_configuration(device_name)
        if resp.status_code != 200:
            assert False

    @pytest.mark.gw_list_of_blacklisted_devices
    @allure.title("Get list blacklisted devices")
    @allure.testcase(name="WIFI-12556",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12556")
    def test_gw_service_get_list_of_blacklisted_devices(self, get_target_object, get_testbed_details):
        """
            Get a list blacklisted devices
            Unique marker:pytest -m "gw_list_of_blacklisted_devices"
        """
        resp = get_target_object.controller_library_object.get_list_of_blacklisted_devices()
        assert resp.status_code == 200

    @allure.title("CRUD a  blacklist entry")
    @allure.testcase(name="WIFI-12620",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12620")
    @pytest.mark.gw_crud_blacklist_entry
    def test_gw_service_create_read_edit_delete_blacklist_entry(self, get_target_object, get_testbed_details):
        """
            Test to create,read,edit and delete blacklist entry
            Unique marker: pytest -m "gw_crud_blacklist_entry"
        """
        device_mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                                  random.randint(0, 255),
                                                  random.randint(0, 255))
        device_name = device_mac.replace(":", "")
        # Adding dummy ap
        payload = {'serialNumber': device_name,
                   'UUID': '123456',
                   'configuration': self.configuration,
                   'deviceType': 'AP',
                   'location': '',
                   'macAddress': device_mac,
                   'manufacturer': 'Testing through Automation',
                   'owner': ''}
        resp = get_target_object.controller_library_object.add_device_to_gw(device_name, payload)
        if resp.status_code != 200:
            assert False

        # Testing blacklist
        payload_blacklist = {'serialNumber': device_name,
                             'reason': 'Testing through Automation'
                             }
        resp = get_target_object.controller_library_object.create_to_the_blacklist(device_name, payload_blacklist)
        if resp.status_code != 200:
            assert False

        resp = get_target_object.controller_library_object.get_blacklist_entry(device_name)
        if resp.status_code != 200:
            assert False

        editing_payload = {
            "reason": "edit blacklist entry"
        }
        resp = get_target_object.controller_library_object.modify_to_the_blacklist(device_name, editing_payload)
        if resp.status_code != 200:
            assert False

        resp = get_target_object.controller_library_object.delete_from_blacklist(device_name)
        if resp.status_code != 200:
            assert False

        # deleting dummy ap
        resp = get_target_object.controller_library_object.delete_device_from_gw(device_name)
        if resp.status_code != 200:
            assert False

    @pytest.mark.gw_debug_device
    @allure.title("Debug a device")
    @allure.testcase(name="WIFI-12628",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12628")
    def test_gw_service_debug_device(self, get_target_object, get_testbed_details):
        """
            Get a file from the upload directory
            Unique marker: pytest -m "gw_debug_device"
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        # Running one script
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
        resp = get_target_object.controller_library_object.debug_device(device_name, payload)
        if resp.status_code != 200:
            assert False

    @pytest.mark.gw_get_delete_files
    @allure.title("Get and Delete file from the upload directory")
    @allure.testcase(name="WIFI-12629",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12629")
    def test_gw_service_get_delete_files(self, get_target_object, get_testbed_details):
        """
            Get and Delete file from the upload directory
            Unique marker: pytest -m "gw_get_delete_files"
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        # Running one script
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
        # Running diagnostic script for uuid
        resp = get_target_object.controller_library_object.debug_device(device_name, payload)
        if resp.status_code != 200:
            assert False
        resp = resp.json()
        uuid = resp['UUID']

        # get file
        resp = get_target_object.controller_library_object.get_file(device_name, uuid)
        if resp.status_code != 200:
            assert False
        # Delete file
        resp = get_target_object.controller_library_object.delete_file(device_name, uuid)
        if resp.status_code != 200:
            assert False

    @pytest.mark.gw_system
    @allure.title("Perform some system wide commands")
    @allure.testcase(name="WIFI-12627",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12627")
    def test_gw_service_gw_system(self, get_target_object, get_testbed_details):
        """
            Perform some system wide commands
            Unique marker:pytest -m "gw_system"
        """
        payload = {
            "command": "setloglevel",
            "subsystems": [
                {
                    "tag": "",
                    "value": ""
                }
            ]
        }
        resp = get_target_object.controller_library_object.perform_system_wide_commands(payload)
        if resp.status_code != 200:
            assert False

    @allure.title("Delete commands, device logs, health checks, capabilities and statistics")
    @allure.testcase(name="WIFI-12626",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12626")
    @pytest.mark.gw_delete_commands_logs_healthchecks_capabilities_statistics
    def test_gw_service_delete_commands_logs_healthchecks_capabilities_statistics(self, get_target_object,
                                                                                  get_testbed_details):
        """
            Delete commands, device logs, health checks, capabilities and statistics
            Unique marker: pytest -m "gw_delete_commands_logs_healthchecks_capabilities_statistics"
        """
        device_mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                                  random.randint(0, 255),
                                                  random.randint(0, 255))
        device_name = device_mac.replace(":", "")
        # Adding dummy ap
        payload = {'serialNumber': device_name,
                   'UUID': '123456',
                   'configuration': self.configuration,
                   'deviceType': 'AP',
                   'location': '',
                   'macAddress': device_mac,
                   'manufacturer': 'Testing through Automation',
                   'owner': ''}
        resp = get_target_object.controller_library_object.add_device_to_gw(device_name, payload)
        if resp.status_code != 200:
            assert False

        # Deleting Delete some commands
        resp = get_target_object.controller_library_object.delete_some_commands(device_name)
        if resp.status_code != 200:
            assert False

        # Delete some device logs
        resp = get_target_object.controller_library_object.delete_some_device_logs(device_name)
        if resp.status_code != 200:
            assert False
        # Delete some device health checks
        resp = get_target_object.controller_library_object.delete_some_device_health_checks(device_name)
        if resp.status_code != 200:
            assert False
        # Delete the capabilities for a given device
        resp = get_target_object.controller_library_object.delete_capabilities_device(device_name)
        if resp.status_code != 200:
            assert False
        # Get the latest statistics for a given device
        resp = get_target_object.controller_library_object.delete_statistics_device(device_name)
        if resp.status_code != 200:
            assert False
        # Deleting dummy ap
        resp = get_target_object.controller_library_object.delete_device_from_gw(device_name)
        if resp.status_code != 200:
            assert False

    @pytest.mark.gw_get_radius_sessions
    @allure.title("Get RADIUS sessions for a given AP")
    @allure.testcase(name="WIFI-12642",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12642")
    def test_gw_service_get_radius_sessions(self, get_target_object, get_testbed_details):
        """
            Get RADIUS sessions for a given AP
            Unique marker:pytest -m "gw_get_radius_sessions"
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        resp = get_target_object.controller_library_object.get_radius_sessions(device_name)
        assert resp.status_code == 200

    @pytest.mark.rrmcmd
    @pytest.mark.rrmcmd_tx_power
    @allure.title("Verify Dynamic change of Tx Power using RRM action command")
    @allure.testcase(name="WIFI-13350",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-13350")
    def test_rrmcmd_tx_power(self, get_target_object, get_testbed_details):
        """
            Test to SEND RRM commands from device present in Gateway UI
            Unique marker:pytest -m "rrmcmd_tx_power"
        """
        action_body = {
            "actions": [
                {
                    "action": "tx_power",
                    "bssid": "",
                    "level": 20
                }
            ]
        }
        serial_number = get_target_object.device_under_tests_info[0]["identifier"]
        for i in range(len(self.configuration['radios'])):
            self.configuration['radios'][i]["tx-power"] = 23
        payload = {"configuration": self.configuration, "serialNumber": serial_number, "UUID": 1}
        uri = get_target_object.controller_library_object.build_uri("device/" + serial_number + "/configure")
        basic_cfg_str = json.dumps(payload)
        logging.info("Sending Command: Configure " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                     "Headers: " + str(get_target_object.controller_library_object.make_headers()))
        allure.attach(name="Sending Command: Configure", body="Sending Command: " + "\n" +
                                                              "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                              "URI: " + str(uri) + "\n" +
                                                              "Data: " + str(payload) + "\n" +
                                                              "Headers: " + str(
            get_target_object.controller_library_object.make_headers()))
        logging.info("wait until the configuration get's applied...")
        resp = requests.post(uri, data=basic_cfg_str, verify=False, timeout=240,
                             headers=get_target_object.controller_library_object.make_headers())
        if resp and resp.status_code == 200:
            logging.info(f"Status:{resp.status_code} - Configuration push successful")
            logging.info(resp.json())
        else:
            logging.error("Failed to push the config")
            pytest.exit(f"Reason:{resp.reason} - Error while pushing the configuration")
        logging.info("iwinfo before applying Tx Power using RRM action command: \n")
        cmd_response = get_target_object.get_dut_library_object().get_iwinfo(attach_allure=False)
        allure.attach(body=cmd_response, name="iwinfo before applying Tx Power using RRM action command:")
        if str(cmd_response) != "pop from empty list":
            interfaces = {}
            interface_matches = re.finditer(
                r'wlan\d\s+ESSID:\s+".*?"\s+Access Point:\s+([0-9A-Fa-f:]+).*?Tx-Power:\s+([\d\s]+)', cmd_response,
                re.DOTALL)
            if interface_matches:
                for match in interface_matches:
                    interface_name = f'wlan{match.group(0)[4]}'
                    access_point = match.group(1)
                    tx_power = match.group(2).strip()
                    interfaces[interface_name] = {'Access Point': access_point, 'Tx-Power': tx_power}
                logging.info(interfaces)
            else:
                logging.error("Failed to get iwinfo")
                pytest.exit("Failed to get iwinfo")
            for i in interfaces:
                action_body["actions"][0]["bssid"] = interfaces[i]['Access Point']
                action_body["actions"][0]["level"] = 20
                response = get_target_object.controller_library_object.rrm_command(payload=action_body,
                                                                                   serial_number=serial_number)
                logging.info(response.json())
                time.sleep(2)
                allure.attach(name=f"Response: {response.status_code} - {response.reason}", body=str(response.json()),
                              attachment_type=allure.attachment_type.JSON)
            time.sleep(3)
            logging.info("iwinfo After applying Tx Power using RRM action command: \n")
            cmd_response1 = get_target_object.get_dut_library_object().get_iwinfo(attach_allure=False)
            allure.attach(body=cmd_response1, name="iwinfo before applying Tx Power using RRM action command:")
            if cmd_response1 == {}:
                assert False, "Empty iwinfo reponse from AP through minicom"
            interfaces1 = {}
            interface_matches1 = re.finditer(
                r'wlan\d\s+ESSID:\s+".*?"\s+Access Point:\s+([0-9A-Fa-f:]+).*?Tx-Power:\s+([\d\s]+)', cmd_response1,
                re.DOTALL)
            if interface_matches1:
                for match1 in interface_matches1:
                    interface_name1 = f'wlan{match1.group(0)[4]}'
                    access_point1 = match1.group(1)
                    tx_power1 = match1.group(2).strip()
                    interfaces1[interface_name1] = {'Access Point': access_point1, 'Tx-Power': tx_power1}
                logging.info(interfaces1)
            else:
                logging.error("Failed to get iwinfo")
                pytest.exit("Failed to get iwinfo")
            key_to_check = ('Tx-Power', '20')
            logging.info(interfaces1.items())
            for key, value in interfaces1.items():
                logging.info(key, value)
                if key_to_check in value:
                    assert True
                else:
                    assert False, "failed to set tx power using RRM CMD"
        elif cmd_response == {}:
            assert False, "Empty iwinfo reponse from AP through minicom"
        else:
            assert False, "Failed to get iwinfo from minicom"

    @pytest.mark.rrmcmd
    @pytest.mark.rrmcmd_channel_switch
    @allure.title("Verify Dynamic change of Channel using RRM action command")
    @allure.testcase(name="WIFI-13348",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-13348")
    def test_rrmcmd_channel_switch(self, get_target_object, get_testbed_details):
        """
            Test to SEND RRM commands from device present in Gateway UI
            Unique marker:pytest -m "rrmcmd_channel_switch"
        """
        action_body = {
            "actions": [
                {
                    "action": "channel_switch",
                    "bssid": "",
                    "channel": 0
                }
            ]
        }
        serial_number = get_target_object.device_under_tests_info[0]["identifier"]
        for i in range(len(self.configuration['radios'])):
            if self.configuration['radios'][i]["band"] == "5G":
                self.configuration['radios'][i]['channel'] = 36
            if self.configuration['radios'][i]["band"] == "2G":
                self.configuration['radios'][i]['channel'] = 6
        payload = {"configuration": self.configuration, "serialNumber": serial_number, "UUID": 1}
        uri = get_target_object.controller_library_object.build_uri("device/" + serial_number + "/configure")
        basic_cfg_str = json.dumps(payload)
        logging.info("Sending Command: Configure " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                     "Headers: " + str(get_target_object.controller_library_object.make_headers()))
        allure.attach(name="Sending Command: Configure", body="Sending Command: " + "\n" +
                                                              "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                              "URI: " + str(uri) + "\n" +
                                                              "Data: " + str(payload) + "\n" +
                                                              "Headers: " + str(
            get_target_object.controller_library_object.make_headers()))
        logging.info("wait until the configuration push get's applied...")
        resp = requests.post(uri, data=basic_cfg_str, verify=False, timeout=240,
                             headers=get_target_object.controller_library_object.make_headers())
        if resp and resp.status_code == 200:
            logging.info(f"Status:{resp.status_code} - Configuration push successful")
            logging.info(resp.json())
        else:
            logging.error("Failed to push the config")
            pytest.exit(f"Reason:{resp.reason} - Error while pushing the configuration")
        logging.info("iwinfo before changing Channel using RRM action command: \n")
        cmd_response = get_target_object.get_dut_library_object().get_iwinfo(attach_allure=False)
        allure.attach(body=cmd_response, name="iwinfo before changing Channel using RRM action command:")
        if str(cmd_response) != "pop from empty list":
            interfaces = {}
            interface_matches = re.finditer(
                r'wlan\d\s+ESSID:\s+".*?"\s+Access Point:\s+([0-9A-Fa-f:]+).*?Channel:\s+([\d\s]+)', cmd_response,
                re.DOTALL)
            if interface_matches:
                for match in interface_matches:
                    interface_name = f'wlan{match.group(0)[4]}'
                    access_point = match.group(1)
                    channel = match.group(2).strip()
                    interfaces[interface_name] = {'Access Point': access_point, 'Channel': channel}
                logging.info(interfaces)
            else:
                logging.error("Failed to get iwinfo")
                pytest.exit("Failed to get iwinfo")
            for i in interfaces:
                action_body["actions"][0]["bssid"] = interfaces[i]['Access Point']
                action_body["actions"][0]["channel"] = 6
                response = get_target_object.controller_library_object.rrm_command(payload=action_body,
                                                                                   serial_number=serial_number)
                logging.info(response.json())
                time.sleep(2)
                allure.attach(name=f"Response: {response.status_code} - {response.reason}", body=str(response.json()),
                              attachment_type=allure.attachment_type.JSON)
            time.sleep(3)
            logging.info("iwinfo after changing channel using RRM action command: \n")
            cmd_response1 = get_target_object.get_dut_library_object().get_iwinfo(attach_allure=False)
            allure.attach(body=cmd_response1, name="iwinfo after changing channel using RRM action command:")
            if cmd_response1 == {}:
                assert False, "Empty iwinfo reponse from AP through minicom"
            interfaces1 = {}
            interface_matches1 = re.finditer(
                r'wlan\d\s+ESSID:\s+".*?"\s+Access Point:\s+([0-9A-Fa-f:]+).*?Channel:\s+([\d\s]+)', cmd_response1,
                re.DOTALL)
            if interface_matches1:
                for match1 in interface_matches1:
                    interface_name1 = f'wlan{match1.group(0)[4]}'
                    access_point1 = match1.group(1)
                    channel1 = match1.group(2).strip()
                    interfaces1[interface_name1] = {'Access Point': access_point1, 'Channel': channel1}
                logging.info(interfaces1)
            else:
                logging.error("Failed to get iwinfo")
                pytest.exit("Failed to get iwinfo")
            key_to_check = ('Channel', '6')
            logging.info(interfaces1.items())
            for key, value in interfaces1.items():
                logging.info(key, value)
                if key_to_check in value:
                    assert True
                else:
                    assert False, "failed to set channel using RRM CMD"
        elif cmd_response == {}:
            assert False, "Empty iwinfo reponse from AP through minicom"
        else:
            assert False, "Failed to get iwinfo from minicom"

    @pytest.mark.rrmcmd
    @pytest.mark.rrmcmd_kick_and_ban
    @allure.title("Verify Kick and Ban of a Client using RRM action command")
    @allure.testcase(name="WIFI-13349",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-13349")
    def test_rrmcmd_kick_and_ban(self, get_target_object, get_testbed_details, get_test_library):
        """
            Test to SEND RRM commands from device present in Gateway UI
            Unique marker:pytest -m "rrmcmd_kick_and_ban"
        """
        action_body = {
            "actions": [
                {
                    "action": "kick",
                    "addr": "",
                    "reason": 5,
                    "ban_time": 10
                }
            ]
        }
        ssid, passwd = self.configuration["interfaces"][0]["ssids"][0]["name"], \
            self.configuration["interfaces"][0]["ssids"][0]["encryption"]["key"]
        serial_number = get_target_object.device_under_tests_info[0]["identifier"]
        payload = {"configuration": self.configuration, "serialNumber": serial_number, "UUID": 1}
        uri = get_target_object.controller_library_object.build_uri("device/" + serial_number + "/configure")
        basic_cfg_str = json.dumps(payload)
        logging.info("Sending Command: Configure " + "\n" +
                     "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                     "URI: " + str(uri) + "\n" +
                     "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                     "Headers: " + str(get_target_object.controller_library_object.make_headers()))
        allure.attach(name="Sending Command: Configure", body="Sending Command: " + "\n" +
                                                              "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                                                              "URI: " + str(uri) + "\n" +
                                                              "Data: " + str(payload) + "\n" +
                                                              "Headers: " + str(
            get_target_object.controller_library_object.make_headers()))
        logging.info("wait until the configuration push get's applied...")
        resp = requests.post(uri, data=basic_cfg_str, verify=False, timeout=240,
                             headers=get_target_object.controller_library_object.make_headers())
        if resp and resp.status_code == 200:
            logging.info(f"Status:{resp.status_code} - Configuration push successful")
            logging.info(resp.json())
        else:
            logging.error("Failed to push the config")
            pytest.exit(f"Reason:{resp.reason} - Error while pushing the configuration")
        sta_created = get_test_library.client_connect_using_radio(ssid=ssid, passkey=passwd, security="wpa2",
                                                                  mode="BRIDGE", radio="wiphy0",
                                                                  station_name=["sta100"],
                                                                  create_vlan=False)
        if not sta_created:
            logging.info("Failed in creation of Station")
            pytest.fail("Station creation failed")
        link = 'ports/all'
        a = get_test_library.json_get("/wifi-msgs/last/1")
        last_timestamp = a['wifi-messages']['time-stamp']
        logging.info(f"Last WiFi Message Time Stamp: {last_timestamp}")
        port_links = get_test_library.json_get('/ports?fields=alias,_links')
        logging.info(f"port info: {port_links}")
        if "interfaces" in port_links:
            for i in range(len(port_links['interfaces'])):
                for k, v in port_links['interfaces'][i].items():
                    if v['alias'] == 'sta100':
                        link = v['_links']
                        logging.info(f"----link url------: {link}")
                        break
        sta_info = get_test_library.json_get(f'{link}')['interface']
        logging.info(sta_info)
        allure.attach(name=f"station info:", body=str(sta_info),
                      attachment_type=allure.attachment_type.TEXT)
        logging.info("get the client mac address")
        client_mac = sta_info['mac']
        action_body['actions'][0]['addr'] = str(client_mac)
        logging.info(f'rrm cmd payload: {action_body}')
        response = get_target_object.controller_library_object.rrm_command(payload=action_body,
                                                                           serial_number=serial_number)
        logging.info(response.json())
        time.sleep(10)
        allure.attach(name=f"RRM CMD Response: {response.status_code} - {response.reason}", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        logging.info("Checking Wifi-Messages to verify Client Disconnection Messages: \n")
        wifi_messages = get_test_library.json_get("/wifi-msgs/since=time/" + str(last_timestamp))
        allure.attach(name=f"wifi-messages:", body=str(wifi_messages),
                      attachment_type=allure.attachment_type.TEXT)
        msg_to_check1 = 'Reason 5; disassociated as AP is unable to handle all connected STA'
        msg_to_check2 = f"IFNAME=sta100 <3>CTRL-EVENT-DISCONNECTED bssid={str(client_mac)} reason=5"
        if msg_to_check1 in wifi_messages or msg_to_check2 in wifi_messages:
            logging.info("AP kicked off the STA successfully using RRM kick and ban CMD")
            assert True
        else:
            assert False, 'AP failed to kick & ban the client using RRM CMD'
