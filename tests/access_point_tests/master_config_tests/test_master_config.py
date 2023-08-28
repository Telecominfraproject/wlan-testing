"""
    Master Configuration Tests:
    pytest -m master_config_tests
"""
import json
import os
import logging
import re
import time

import allure
import pytest
import requests
from datetime import datetime

# Get the directory of the current test config file
test_file_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path relative to the config file directory
file_path = os.path.join(test_file_dir, 'master-config-1.json')
with open(file_path, 'r') as file:
    json_string = file.read()
    config_data_1 = json.loads(json_string)

file_path2 = os.path.join(test_file_dir, 'master-config-2.json')
with open(file_path, 'r') as file:
    json_string = file.read()
    config_data_2 = json.loads(json_string)


pytestmark = [pytest.mark.master_config]


@allure.feature("Master Configurations Test")
@allure.parent_suite("Master Configuration")
@allure.sub_suite(sub_suite_name="Test Master Configurations with Various Services")
class TestMasterConfig(object):
    """
        Master Configuration Tests:
        pytest -m master_config_tests
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12752", name="WIFI-12752")
    @pytest.mark.wpa_personal
    @pytest.mark.master_config1
    def test_master_config_one(self, get_test_library, check_connectivity, get_target_object):
        """
            Master Config One
            pytest -m "master_config1"
        """
        for ap in range(len(get_target_object.device_under_tests_info)):
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            logging.info(config_data_1)
            payload = {"configuration": json.dumps(config_data_1), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Push Config:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))
            if int(resp.status_code) == 200:
                time.sleep(120)
            else:
                pytest.exit("Configuration Push Failed")

            # check RX message from AP after config push
            after_config_push = get_target_object.dut_library_object.get_dut_logs()
            logging.info(after_config_push)

            # get pushed config from ap
            config_pushed = get_target_object.dut_library_object.run_generic_command(cmd="cat /etc/ucentral/ucentral"
                                                                                         ".active", attach_allure=True)
            logging.info(config_pushed)
            # check ssid info in iwinfo
            configured_ssids = config_data_1
            iw_info = get_target_object.dut_library_object.get_iwinfo()
            if iw_info is not None:
                interface_pattern = r'(\S+)\s+ESSID:\s+"(.*?)"'
                matches = re.findall(interface_pattern, iw_info)
                logging.info(matches)
                if matches and len(matches) != 0:
                    data = {interface: essid for interface, essid in matches}
                else:
                    pytest.fail("Some or ALL Configured SSID's are not present in iwinfo")

        assert True


    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12753", name="WIFI-12753")
    @pytest.mark.wpa_personal
    @pytest.mark.master_config2
    def test_master_config_two(self, get_test_library, check_connectivity, get_target_object):
        """
            Master Config Two
            pytest -m "master_config2"
        """
        for ap in range(len(get_target_object.device_under_tests_info)):
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            logging.info(config_data_1)
            payload = {"configuration": json.dumps(config_data_1), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Push Config:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                    "TimeStamp: " + str(datetime.utcnow()) + "\n" +
                                                    "Data: " + str(payload) + "\n" +
                                                    "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))
            if int(resp.status_code) == 200:
                time.sleep(120)
            else:
                pytest.exit("Configuration Push Failed")

            # check RX message from AP after config push
            after_config_push = get_target_object.dut_library_object.get_dut_logs()
            logging.info(after_config_push)

            # get pushed config from ap
            config_pushed = get_target_object.dut_library_object.run_generic_command(cmd="cat /etc/ucentral/ucentral"
                                                                                         ".active", attach_allure=True)
            logging.info(config_pushed)
            # check ssid info in iwinfo
            configured_ssids = config_data_2
            iw_info = get_target_object.dut_library_object.get_iwinfo()
            if iw_info is not None:
                interface_pattern = r'(\S+)\s+ESSID:\s+"(.*?)"'
                matches = re.findall(interface_pattern, iw_info)
                logging.info(matches)
                if matches and len(matches) != 0:
                    data = {interface: essid for interface, essid in matches}
                else:
                    pytest.fail("Some or ALL Configured SSID's are not present in iwinfo")

        assert True
