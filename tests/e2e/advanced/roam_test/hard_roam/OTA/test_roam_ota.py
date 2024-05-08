import datetime
import json
import logging
import os
import re

import pytest
import allure
import time

import requests

pytestmark = [pytest.mark.roam_test, pytest.mark.bridge, pytest.mark.roam_ota]

# Get the directory of the current test config file
test_file_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path relative to the config file directory
file_path = os.path.join(test_file_dir, 'roam-config.json')
with open(file_path, 'r') as file:
    json_string = file.read()
    config_data = json.loads(json_string)


@allure.suite("11r Roaming over the air")
@allure.feature("Roam Test")
class TestRoamOTA(object):
    @pytest.mark.same_channel
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.roam
    def test_roam_2g_to_2g_sc_psk_wpa2(self, get_target_object, get_test_library, get_lab_info, selected_testbed):
        """
            Test Roaming between two APs, Same channel, 2G, WPA2 Personal
            pytest -m "roam and twog and same_channel and wpa2_personal"
        """
        ap_data = dict()
        dut_list = [str(selected_testbed)]
        dut_names = list()
        bssid_list = list()
        testbed_info = get_lab_info.CONFIGURATION
        if str(selected_testbed + 'a') in testbed_info:
            dut_list.append(str(selected_testbed + 'a'))
        logging.info(f"dut list: {dut_list}--")
        for i in range(len(config_data["radios"])):
            if config_data['radios'][i]["band"] == "5G":
                config_data['radios'].pop(i)
        if "5G" in config_data['interfaces'][0]["ssids"][0]["wifi-bands"]:
            config_data['interfaces'][0]["ssids"][0]["wifi-bands"].remove("5G")
        if len(dut_list) < 2:
            logging.error(f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}")
            assert False, f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}"
        for ap in range(len(dut_list)):
            serial_number = testbed_info[dut_list[ap]]["device_under_tests"][0]['identifier']
            dut_names.append(testbed_info[dut_list[ap]]["device_under_tests"][0]['model'])
            logging.info(config_data)
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 2}
            uri = get_target_object.controller_library_object.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.controller_library_object.make_headers()))
            allure.attach(name=f"Push roam config on {serial_number}: ", body="Sending Command: " + str(uri) + "\n" +
                                                                              "TimeStamp: " + str(
                datetime.datetime.utcnow()) + "\n" +
                                                                              "Data: " + str(payload) + "\n" +
                                                                              "Headers: " + str(
                get_target_object.controller_library_object.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload, indent=2),
                                 headers=get_target_object.controller_library_object.make_headers(),
                                 verify=False, timeout=120)
            time.sleep(10)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code} {resp.reason}", body=str(resp.json()))
            if resp.status_code != 200:
                if resp.status_code == 400 and "Device is already executing a command. Please try later." in resp.json()["ErrorDescription"]:
                    time.sleep(30)
                    resp = requests.post(uri, data=json.dumps(payload, indent=2),
                                         headers=get_target_object.controller_library_object.make_headers(),
                                         verify=False, timeout=120)
                    time.sleep(10)
                    logging.info(resp.json())
                else:
                    assert False, f"push configuration to {serial_number} got failed"
            get_target_object.dut_library_object.device_under_tests_data = testbed_info[dut_list[ap]]["device_under_tests"]
            ap_iwinfo = get_target_object.dut_library_object.get_iwinfo(attach_allure=False)
            if str(ap_iwinfo) != "Error: pop from empty list":
                interfaces = {}
                interface_matches = re.finditer(
                    r'wlan\d\s+ESSID:\s+".*?"\s+Access Point:\s+([0-9A-Fa-f:]+).*?Channel:\s+([\d\s]+)', ap_iwinfo,
                    re.DOTALL)
                logging.info(str(interface_matches))
                if interface_matches:
                    for match in interface_matches:
                        interface_name = f'wlan{match.group(0)[4]}'
                        access_point = match.group(1)
                        channel = match.group(2).strip()
                        interfaces[interface_name] = {'Access Point': access_point, 'Channel': channel}
                        ap_data.update({serial_number: {'Access Point': access_point, 'Channel': channel}})
                    logging.info(interfaces)
                else:
                    logging.error("Failed to get iwinfo")
                    pytest.exit("Failed to get iwinfo")
            elif ap_iwinfo == {}:
                assert False, "Empty iwinfo reponse from AP through minicom"
            else:
                assert False, "Failed to get iwinfo from minicom"
        logging.info(f"AP Data from iwinfo: {ap_data}")
        for serial in ap_data:
            bssid_list.append(ap_data[serial]['Access Point'])
        ssid = config_data['interfaces'][0]["ssids"][0]["name"]
        key = config_data['interfaces'][0]["ssids"][0]["encryption"]["key"]
        pass_fail, message = get_test_library.roam_test(ap1_bssid=bssid_list[0], ap2_bssid=bssid_list[1],
              band="twog", num_sta=1, security="wpa2", security_key=key, ssid=ssid, upstream="1.1.eth1", duration=None,
              iteration=1, channel="11", option="ota", dut_name=dut_names, traffic_type="lf_udp", sta_type="11r")
        assert pass_fail, message

    @pytest.mark.different_channel
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.roam
    def test_roam_2g_to_2g_dc_psk_wpa2(self, get_target_object, get_test_library, get_lab_info, selected_testbed):
        """
            Test Roaming between two APs, Different channel, 2G, WPA2 Personal
            pytest -m "roam and twog and same_channel and wpa2_personal"
        """
        ap_data = dict()
        dut_list = [str(selected_testbed)]
        dut_names = list()
        bssid_list = list()
        testbed_info = get_lab_info.CONFIGURATION
        if str(selected_testbed + 'a') in testbed_info:
            dut_list.append(str(selected_testbed + 'a'))
        logging.info(f"dut list: {dut_list}--")
        for i in range(len(config_data["radios"])):
            if config_data['radios'][i]["band"] == "5G":
                config_data['radios'].pop(i)
                config_data['radios'].append({"band": "2G", "channel": 1, "channel-mode": "HE", "channel-width": 20, "country": "CA"})
        if "5G" in config_data['interfaces'][0]["ssids"][0]["wifi-bands"]:
            config_data['interfaces'][0]["ssids"][0]["wifi-bands"].remove("5G")
        if len(dut_list) < 2:
            logging.error(
                f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}")
            assert False, f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}"
        for ap in range(len(dut_list)):
            serial_number = testbed_info[dut_list[ap]]["device_under_tests"][0]['identifier']
            dut_names.append(testbed_info[dut_list[ap]]["device_under_tests"][0]['model'])
            logging.info(config_data)
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 2}
            uri = get_target_object.controller_library_object.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.controller_library_object.make_headers()))
            allure.attach(name=f"Push roam config on {serial_number}: ", body="Sending Command: " + str(uri) + "\n" +
                                                                              "TimeStamp: " + str(
                datetime.datetime.utcnow()) + "\n" +
                                                                              "Data: " + str(payload) + "\n" +
                                                                              "Headers: " + str(
                get_target_object.controller_library_object.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload, indent=2),
                                 headers=get_target_object.controller_library_object.make_headers(),
                                 verify=False, timeout=120)
            time.sleep(10)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code} {resp.reason}", body=str(resp.json()))
            if resp.status_code != 200:
                if resp.status_code == 400 and "Device is already executing a command. Please try later." in \
                        resp.json()["ErrorDescription"]:
                    time.sleep(30)
                    resp = requests.post(uri, data=json.dumps(payload, indent=2),
                                         headers=get_target_object.controller_library_object.make_headers(),
                                         verify=False, timeout=120)
                    time.sleep(10)
                    logging.info(resp.json())
                else:
                    assert False, f"push configuration to {serial_number} got failed"
            get_target_object.dut_library_object.device_under_tests_data = testbed_info[dut_list[ap]][
                "device_under_tests"]
            ap_iwinfo = get_target_object.dut_library_object.get_iwinfo(attach_allure=False)
            if str(ap_iwinfo) != "Error: pop from empty list":
                interfaces = {}
                interface_matches = re.finditer(
                    r'wlan\d\s+ESSID:\s+".*?"\s+Access Point:\s+([0-9A-Fa-f:]+).*?Channel:\s+([\d\s]+)', ap_iwinfo,
                    re.DOTALL)
                logging.info(str(interface_matches))
                if interface_matches:
                    for match in interface_matches:
                        interface_name = f'wlan{match.group(0)[4]}'
                        access_point = match.group(1)
                        channel = match.group(2).strip()
                        interfaces[interface_name] = {'Access Point': access_point, 'Channel': channel}
                        ap_data.update({serial_number: {'Access Point': access_point, 'Channel': channel}})
                    logging.info(interfaces)
                else:
                    logging.error("Failed to get iwinfo")
                    pytest.exit("Failed to get iwinfo")
            elif ap_iwinfo == {}:
                assert False, "Empty iwinfo reponse from AP through minicom"
            else:
                assert False, "Failed to get iwinfo from minicom"
        logging.info(f"AP Data from iwinfo: {ap_data}")
        for serial in ap_data:
            bssid_list.append(ap_data[serial]['Access Point'])
        ssid = config_data['interfaces'][0]["ssids"][0]["name"]
        key = config_data['interfaces'][0]["ssids"][0]["encryption"]["key"]
        pass_fail, message = get_test_library.roam_test(ap1_bssid=bssid_list[0], ap2_bssid=bssid_list[1],
                                                        band="twog", num_sta=1, security="wpa2", security_key=key,
                                                        ssid=ssid, upstream="1.1.eth1", duration=None,
                                                        iteration=1, channel="11", option="ota", dut_name=dut_names,
                                                        traffic_type="lf_udp", sta_type="11r")
        assert pass_fail, message

    @pytest.mark.same_channel
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.roam
    def test_roam_5g_to_5g_sc_psk_wpa2(self, get_target_object, get_test_library, get_lab_info, selected_testbed):
        """
            Test Roaming between two APs, Same channel, 5G, WPA2 Personal
            pytest -m "roam and fiveg and same_channel and wpa2_personal"
        """
        ap_data = dict()
        dut_list = [str(selected_testbed)]
        dut_names = list()
        bssid_list = list()
        testbed_info = get_lab_info.CONFIGURATION
        if str(selected_testbed + 'a') in testbed_info:
            dut_list.append(str(selected_testbed + 'a'))
        logging.info(f"dut list: {dut_list}--")
        for i in range(len(config_data["radios"])):
            if config_data['radios'][i]["band"] == "2G":
                config_data['radios'].pop(i)
        if "2G" in config_data['interfaces'][0]["ssids"][0]["wifi-bands"]:
            config_data['interfaces'][0]["ssids"][0]["wifi-bands"].remove("2G")
        if len(dut_list) < 2:
            logging.error(f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}")
            assert False, f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}"
        for ap in range(len(dut_list)):
            serial_number = testbed_info[dut_list[ap]]["device_under_tests"][0]['identifier']
            dut_names.append(testbed_info[dut_list[ap]]["device_under_tests"][0]['model'])
            logging.info(config_data)
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 2}
            uri = get_target_object.controller_library_object.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.controller_library_object.make_headers()))
            allure.attach(name=f"Push roam config on {serial_number}: ", body="Sending Command: " + str(uri) + "\n" +
                                                                              "TimeStamp: " + str(
                datetime.datetime.utcnow()) + "\n" +
                                                                              "Data: " + str(payload) + "\n" +
                                                                              "Headers: " + str(
                get_target_object.controller_library_object.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload, indent=2),
                                 headers=get_target_object.controller_library_object.make_headers(),
                                 verify=False, timeout=120)
            time.sleep(10)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code} {resp.reason}", body=str(resp.json()))
            if resp.status_code != 200:
                if resp.status_code == 400 and "Device is already executing a command. Please try later." in resp.json()["ErrorDescription"]:
                    time.sleep(30)
                    resp = requests.post(uri, data=json.dumps(payload, indent=2),
                                         headers=get_target_object.controller_library_object.make_headers(),
                                         verify=False, timeout=120)
                    time.sleep(10)
                    logging.info(resp.json())
                else:
                    assert False, f"push configuration to {serial_number} got failed"
            get_target_object.dut_library_object.device_under_tests_data = testbed_info[dut_list[ap]]["device_under_tests"]
            ap_iwinfo = get_target_object.dut_library_object.get_iwinfo(attach_allure=False)
            if str(ap_iwinfo) != "Error: pop from empty list":
                interfaces = {}
                interface_matches = re.finditer(
                    r'wlan\d\s+ESSID:\s+".*?"\s+Access Point:\s+([0-9A-Fa-f:]+).*?Channel:\s+([\d\s]+)', ap_iwinfo,
                    re.DOTALL)
                logging.info(str(interface_matches))
                if interface_matches:
                    for match in interface_matches:
                        interface_name = f'wlan{match.group(0)[4]}'
                        access_point = match.group(1)
                        channel = match.group(2).strip()
                        interfaces[interface_name] = {'Access Point': access_point, 'Channel': channel}
                        ap_data.update({serial_number: {'Access Point': access_point, 'Channel': channel}})
                    logging.info(interfaces)
                else:
                    logging.error("Failed to get iwinfo")
                    pytest.exit("Failed to get iwinfo")
            elif ap_iwinfo == {}:
                assert False, "Empty iwinfo reponse from AP through minicom"
            else:
                assert False, "Failed to get iwinfo from minicom"
        logging.info(f"AP Data from iwinfo: {ap_data}")
        for serial in ap_data:
            bssid_list.append(ap_data[serial]['Access Point'])
        ssid = config_data['interfaces'][0]["ssids"][0]["name"]
        key = config_data['interfaces'][0]["ssids"][0]["encryption"]["key"]
        pass_fail, message = get_test_library.roam_test(ap1_bssid=bssid_list[0], ap2_bssid=bssid_list[1],
              band="fiveg", num_sta=1, security="wpa2", security_key=key, ssid=ssid, upstream="1.1.eth1", duration=None,
              iteration=1, channel="36", option="ota", dut_name=dut_names, traffic_type="lf_udp", sta_type="11r")
        assert pass_fail, message
