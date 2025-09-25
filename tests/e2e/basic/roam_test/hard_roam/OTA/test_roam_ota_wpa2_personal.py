import datetime
import json
import logging
import os
import re

import pytest
import allure
import time
import copy
import requests

pytestmark = [pytest.mark.roam_test, pytest.mark.bridge, pytest.mark.roam_ota, pytest.mark.hard_roam_ota, pytest.mark.ow_regression_lf]

# Get the directory of the current test config file
test_file_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path relative to the config file directory
file_path = os.path.join(test_file_dir, 'roam-config.json')
with open(file_path, 'r') as file:
    json_string = file.read()
    config_data = json.loads(json_string)

@allure.feature("Roam Test")
@allure.suite("11r Roaming over the air")
@allure.parent_suite("Roam Test")
@allure.sub_suite("wpa2_personal")

@pytest.mark.wpa2_personal
@pytest.mark.roam
@pytest.mark.ota
class TestRoamOTA(object):
    @pytest.mark.same_channel
    @pytest.mark.twog
    def test_roam_2g_to_2g_sc_psk_wpa2(self, get_target_object, get_test_library, get_lab_info, selected_testbed):
        """
            Test Roaming between two APs, Same channel, 2G, WPA2 Personal
            pytest -m "roam and twog and same_channel and wpa2_personal and ota"
        """
        ap_data = dict()
        dut_list = [str(selected_testbed)]
        dut_names = list()
        bssid_list = list()
        freqs_ = ""
        testbed_info = get_lab_info.CONFIGURATION
        config = copy.deepcopy(config_data)
        temp_list = list()
        for key, val in testbed_info.items():
            tb_type, tb_name = selected_testbed.split("-")
            if tb_type in key and tb_name[0] in key:
                temp_list.append(key)
        temp_list.sort()
        dut_list = [temp_list[idx] for idx in range(len(temp_list)) if idx <= 1]
        logging.info(f"---dut list: {dut_list}---")
        config['radios'] = [
            {"band": "2G", "channel": 11, "channel-mode": "HE", "channel-width": 40, "country": "CA"}]
        config['interfaces'][0]["ssids"][0]["wifi-bands"] = ["2G"]
        if len(dut_list) < 2:
            logging.error(
                f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}")
            assert False, f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}"
        for ap in range(len(dut_list)):
            serial_number = testbed_info[dut_list[ap]]["device_under_tests"][0]['identifier']
            dut_names.append(testbed_info[dut_list[ap]]["device_under_tests"][0]['model'])
            logging.info(config)
            payload = {"configuration": json.dumps(config), "serialNumber": serial_number, "UUID": 2}
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
            ap_iwinfo = get_target_object.dut_library_object.get_iwinfo(attach_allure=True)
            if str(ap_iwinfo) != "Error: pop from empty list":
                include_essid = config['interfaces'][0]["ssids"][0]["name"]
                re_obj = re.compile(
                    rf'(wlan\d(?:-\d)?)\s+ESSID: "{re.escape(include_essid)}".*?\s+Access Point:\s+([0-9A-Fa-f:]+).*?Channel:\s+('
                    r'\d+)\s+\(([\d.]+) GHz\)',
                    re.DOTALL
                )
                # find all matches
                interface_matches = re_obj.finditer(ap_iwinfo)
                if interface_matches:
                    for match in interface_matches:
                        interface_name = match.group(1)
                        access_point = match.group(2)
                        channel = match.group(3)
                        frequency = match.group(4).replace('.', '')
                        ap_data.update(
                            {serial_number: {'Access Point': access_point, 'Channel': channel, 'frequency': frequency}})
                    logging.info(f"AP Data from iwinfo: {ap_data}")
                else:
                    logging.error("Failed to get iwinfo")
                    pytest.exit("Failed to get iwinfo")
            elif ap_iwinfo == {}:
                pytest.fail("Empty iwinfo reponse from AP through minicom")
            else:
                pytest.fail("Failed to get iwinfo from minicom")
        for serial in ap_data:
            bssid_list.append(ap_data[serial]['Access Point'])
            if not ap_data[serial]['frequency'].endswith(","):
                freqs_ = freqs_ + ap_data[serial]['frequency'] + ","
            else:
                freqs_ = freqs_ + ap_data[serial]['frequency']
        ssid = config['interfaces'][0]["ssids"][0]["name"]
        key = config['interfaces'][0]["ssids"][0]["encryption"]["key"]
        pass_fail, message = True, "Test Passed"
        try:
            pass_fail, message = get_test_library.roam_test(ap1_bssid=bssid_list[0], ap2_bssid=bssid_list[1],
                                                            scan_freq=freqs_,
                                                            band="twog", num_sta=1, security="wpa2", security_key=key,
                                                            ssid=ssid, upstream="1.1.eth1", duration=None,
                                                            iteration=1, channel="11", option="ota", dut_name=dut_names,
                                                            traffic_type="lf_udp", sta_type="11r")
        except Exception as e:
            logging.error(f"Exception in roam test : {e}")
            pass_fail, message = False, e
        finally:
            get_target_object.dut_library_object.get_dut_logs(print_log=False)
        if not pass_fail:
            pytest.fail(f"Test failed with the following reasons: \n{message}")
        else:
            assert True

    @pytest.mark.different_channel
    @pytest.mark.twog
    def test_roam_2g_to_2g_dc_psk_wpa2(self, get_target_object, get_test_library, get_lab_info, selected_testbed):
        """
            Test Roaming between two APs, Different channel, 2G, WPA2 Personal
            pytest -m "roam and twog and different_channel and wpa2_personal and ota"
        """
        ap_data = dict()
        dut_list = [str(selected_testbed)]
        dut_names = list()
        bssid_list = list()
        freqs_ = ""
        testbed_info = get_lab_info.CONFIGURATION
        config = copy.deepcopy(config_data)
        temp_list = list()
        for key, val in testbed_info.items():
            tb_type, tb_name = selected_testbed.split("-")
            if tb_type in key and tb_name[0] in key:
                temp_list.append(key)
        temp_list.sort()
        dut_list = [temp_list[idx] for idx in range(len(temp_list)) if idx <= 1]
        config['radios'] = [
            {"band": "2G", "channel": 11, "channel-mode": "HE", "channel-width": 40, "country": "CA"}]
        config['interfaces'][0]["ssids"][0]["wifi-bands"] = ["2G"]
        if len(dut_list) < 2:
            logging.error(
                f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}")
            assert False, f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}"
        for ap in range(len(dut_list)):
            serial_number = testbed_info[dut_list[ap]]["device_under_tests"][0]['identifier']
            dut_names.append(testbed_info[dut_list[ap]]["device_under_tests"][0]['model'])
            if ap == 1:
                config['radios'] = [
                    {"band": "2G", "channel": 1, "channel-mode": "HE", "channel-width": 20, "country": "CA"}]
            logging.info(config)
            payload = {"configuration": json.dumps(config), "serialNumber": serial_number, "UUID": 2}
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
            ap_iwinfo = get_target_object.dut_library_object.get_iwinfo(attach_allure=True)
            if str(ap_iwinfo) != "Error: pop from empty list":
                include_essid = config['interfaces'][0]["ssids"][0]["name"]
                re_obj = re.compile(
                    rf'(wlan\d(?:-\d)?)\s+ESSID: "{re.escape(include_essid)}".*?\s+Access Point:\s+([0-9A-Fa-f:]+).*?Channel:\s+('
                    r'\d+)\s+\(([\d.]+) GHz\)',
                    re.DOTALL
                )
                # find all matches
                interface_matches = re_obj.finditer(ap_iwinfo)
                if interface_matches:
                    for match in interface_matches:
                        interface_name = match.group(1)
                        access_point = match.group(2)
                        channel = match.group(3)
                        frequency = match.group(4).replace('.', '')
                        ap_data.update(
                            {serial_number: {'Access Point': access_point, 'Channel': channel, 'frequency': frequency}})
                    logging.info(f"AP Data from iwinfo: {ap_data}")
                else:
                    logging.error("Failed to get iwinfo")
                    pytest.exit("Failed to get iwinfo")
            elif ap_iwinfo == {}:
                pytest.fail("Empty iwinfo reponse from AP through minicom")
            else:
                pytest.fail("Failed to get iwinfo from minicom")
        for serial in ap_data:
            bssid_list.append(ap_data[serial]['Access Point'])
            if not ap_data[serial]['frequency'].endswith(","):
                freqs_ = freqs_ + ap_data[serial]['frequency'] + ","
            else:
                freqs_ = freqs_ + ap_data[serial]['frequency']
        ssid = config['interfaces'][0]["ssids"][0]["name"]
        key = config['interfaces'][0]["ssids"][0]["encryption"]["key"]
        try:
            pass_fail, message = get_test_library.roam_test(ap1_bssid=bssid_list[0], ap2_bssid=bssid_list[1],
                                                            scan_freq=freqs_,
                                                            band="twog", num_sta=1, security="wpa2", security_key=key,
                                                            ssid=ssid, upstream="1.1.eth1", duration=None,
                                                            iteration=1, channel="1", option="ota", dut_name=dut_names,
                                                            traffic_type="lf_udp", sta_type="11r")
        except Exception as e:
            logging.error(f"Exception in roam test : {e}")
            pass_fail, message = False, e
        finally:
            get_target_object.dut_library_object.get_dut_logs(print_log=False)
        if not pass_fail:
            pytest.fail(f"Test failed with the following reasons: \n{message}")
        else:
            assert True

    @pytest.mark.same_channel
    @pytest.mark.fiveg
    def test_roam_5g_to_5g_sc_psk_wpa2(self, get_target_object, get_test_library, get_lab_info, selected_testbed):
        """
            Test Roaming between two APs, Same channel, 5G, WPA2 Personal
            pytest -m "roam and fiveg and same_channel and wpa2_personal and ota"
        """
        ap_data = dict()
        dut_list = [str(selected_testbed)]
        dut_names = list()
        bssid_list = list()
        freqs_ = ""
        testbed_info = get_lab_info.CONFIGURATION
        config = copy.deepcopy(config_data)
        temp_list = list()
        for key, val in testbed_info.items():
            tb_type, tb_name = selected_testbed.split("-")
            if tb_type in key and tb_name[0] in key:
                temp_list.append(key)
        temp_list.sort()
        dut_list = [temp_list[idx] for idx in range(len(temp_list)) if idx <= 1]
        config['radios'] = [
            {"band": "5G", "channel": 36, "channel-mode": "HE", "channel-width": 80, "country": "CA"}]
        config['interfaces'][0]["ssids"][0]["wifi-bands"] = ["5G"]
        if len(dut_list) < 2:
            logging.error(
                f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}")
            assert False, f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}"
        for ap in range(len(dut_list)):
            serial_number = testbed_info[dut_list[ap]]["device_under_tests"][0]['identifier']
            dut_names.append(testbed_info[dut_list[ap]]["device_under_tests"][0]['model'])
            logging.info(config)
            payload = {"configuration": json.dumps(config), "serialNumber": serial_number, "UUID": 2}
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
            ap_iwinfo = get_target_object.dut_library_object.get_iwinfo(attach_allure=True)
            if str(ap_iwinfo) != "Error: pop from empty list":
                include_essid = config['interfaces'][0]["ssids"][0]["name"]
                re_obj = re.compile(
                    rf'(wlan\d(?:-\d)?)\s+ESSID: "{re.escape(include_essid)}".*?\s+Access Point:\s+([0-9A-Fa-f:]+).*?Channel:\s+('
                    r'\d+)\s+\(([\d.]+) GHz\)',
                    re.DOTALL
                )
                # find all matches
                interface_matches = re_obj.finditer(ap_iwinfo)
                if interface_matches:
                    for match in interface_matches:
                        interface_name = match.group(1)
                        access_point = match.group(2)
                        channel = match.group(3)
                        frequency = match.group(4).replace('.', '')
                        ap_data.update(
                            {serial_number: {'Access Point': access_point, 'Channel': channel, 'frequency': frequency}})
                    logging.info(f"AP Data from iwinfo: {ap_data}")
                else:
                    logging.error("Failed to get iwinfo")
                    pytest.exit("Failed to get iwinfo")
            elif ap_iwinfo == {}:
                pytest.fail("Empty iwinfo reponse from AP through minicom")
            else:
                pytest.fail("Failed to get iwinfo from minicom")
        for serial in ap_data:
            bssid_list.append(ap_data[serial]['Access Point'])
            if not ap_data[serial]['frequency'].endswith(","):
                freqs_ = freqs_ + ap_data[serial]['frequency'] + ","
            else:
                freqs_ = freqs_ + ap_data[serial]['frequency']
        ssid = config['interfaces'][0]["ssids"][0]["name"]
        key = config['interfaces'][0]["ssids"][0]["encryption"]["key"]
        pass_fail, message = True, "Test Passed"
        try:
            pass_fail, message = get_test_library.roam_test(ap1_bssid=bssid_list[0], ap2_bssid=bssid_list[1],
                                                            scan_freq=freqs_,
                                                            band="fiveg", num_sta=1, security="wpa2", security_key=key,
                                                            ssid=ssid, upstream="1.1.eth1", duration=None,
                                                            iteration=1, channel="36", option="ota", dut_name=dut_names,
                                                            traffic_type="lf_udp", sta_type="11r")
        except Exception as e:
            logging.error(f"Exception in roam test : {e}")
            pass_fail, message = False, e
        finally:
            get_target_object.dut_library_object.get_dut_logs(print_log=False)
        if not pass_fail:
            pytest.fail(f"Test failed with the following reasons: \n{message}")
        else:
            assert True

    @pytest.mark.different_channel
    @pytest.mark.fiveg
    def test_roam_5g_to_5g_dc_psk_wpa2(self, get_target_object, get_test_library, get_lab_info, selected_testbed):
        """
            Test Roaming between two APs, Different channel, 5G, WPA2 Personal
            pytest -m "roam and fiveg and different_channel and wpa2_personal and ota"
        """
        ap_data = dict()
        dut_list = [str(selected_testbed)]
        dut_names = list()
        bssid_list = list()
        freqs_ = ""
        testbed_info = get_lab_info.CONFIGURATION
        config = copy.deepcopy(config_data)
        temp_list = list()
        for key, val in testbed_info.items():
            tb_type, tb_name = selected_testbed.split("-")
            if tb_type in key and tb_name[0] in key:
                temp_list.append(key)
        temp_list.sort()
        dut_list = [temp_list[idx] for idx in range(len(temp_list)) if idx <= 1]
        config['radios'] = [
            {"band": "5G", "channel": 36, "channel-mode": "HE", "channel-width": 80, "country": "CA"}]
        config['interfaces'][0]["ssids"][0]["wifi-bands"] = ["5G"]
        if len(dut_list) < 2:
            logging.error(
                f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}")
            assert False, f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}"
        for ap in range(len(dut_list)):
            serial_number = testbed_info[dut_list[ap]]["device_under_tests"][0]['identifier']
            dut_names.append(testbed_info[dut_list[ap]]["device_under_tests"][0]['model'])
            if ap == 1:
                config['radios'] = [
                    {"band": "5G", "channel": 149, "channel-mode": "HE", "channel-width": 80, "country": "CA"}]
            logging.info(config)
            payload = {"configuration": json.dumps(config), "serialNumber": serial_number, "UUID": 2}
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
            ap_iwinfo = get_target_object.dut_library_object.get_iwinfo(attach_allure=True)
            if str(ap_iwinfo) != "Error: pop from empty list":
                include_essid = config['interfaces'][0]["ssids"][0]["name"]
                re_obj = re.compile(
                    rf'(wlan\d(?:-\d)?)\s+ESSID: "{re.escape(include_essid)}".*?\s+Access Point:\s+([0-9A-Fa-f:]+).*?Channel:\s+('
                    r'\d+)\s+\(([\d.]+) GHz\)',
                    re.DOTALL
                )
                # find all matches
                interface_matches = re_obj.finditer(ap_iwinfo)
                if interface_matches:
                    for match in interface_matches:
                        interface_name = match.group(1)
                        access_point = match.group(2)
                        channel = match.group(3)
                        frequency = match.group(4).replace('.', '')
                        ap_data.update(
                            {serial_number: {'Access Point': access_point, 'Channel': channel, 'frequency': frequency}})
                    logging.info(f"AP Data from iwinfo: {ap_data}")
                else:
                    logging.error("Failed to get iwinfo")
                    pytest.exit("Failed to get iwinfo")
            elif ap_iwinfo == {}:
                pytest.fail("Empty iwinfo reponse from AP through minicom")
            else:
                pytest.fail("Failed to get iwinfo from minicom")
        for serial in ap_data:
            bssid_list.append(ap_data[serial]['Access Point'])
            if not ap_data[serial]['frequency'].endswith(","):
                freqs_ = freqs_ + ap_data[serial]['frequency'] + ","
            else:
                freqs_ = freqs_ + ap_data[serial]['frequency']
        ssid = config['interfaces'][0]["ssids"][0]["name"]
        key = config['interfaces'][0]["ssids"][0]["encryption"]["key"]
        try:
            pass_fail, message = get_test_library.roam_test(ap1_bssid=bssid_list[0], ap2_bssid=bssid_list[1],
                                                            scan_freq=freqs_,
                                                            band="fiveg", num_sta=1, security="wpa2", security_key=key,
                                                            ssid=ssid, upstream="1.1.eth1", duration=None,
                                                            iteration=1, channel="36", option="ota", dut_name=dut_names,
                                                            traffic_type="lf_udp", sta_type="11r")
        except Exception as e:
            logging.error(f"Exception in roam test : {e}")
            pass_fail, message = False, e
        finally:
            get_target_object.dut_library_object.get_dut_logs(print_log=False)
        if not pass_fail:
            pytest.fail(f"Test failed with the following reasons: \n{message}")
        else:
            assert True

    @pytest.mark.fiveg
    @pytest.mark.twog
    def test_roam_5g_and_2g_wpa2psk(self, get_target_object, get_test_library, get_lab_info, selected_testbed):
        """
            Test Roaming between two APs, 2G & 5G, WPA2 Personal
            pytest -m "roam and fiveg and twog and wpa2_personal and ota"
        """
        ap_data = dict()
        dut_list = [str(selected_testbed)]
        dut_names = list()
        bssid_list = list()
        freqs_ = ""
        testbed_info = get_lab_info.CONFIGURATION
        config = copy.deepcopy(config_data)
        temp_list = list()
        for key, val in testbed_info.items():
            tb_type, tb_name = selected_testbed.split("-")
            if tb_type in key and tb_name[0] in key:
                temp_list.append(key)
        temp_list.sort()
        dut_list = [temp_list[idx] for idx in range(len(temp_list)) if idx <= 1]
        config['radios'] = [
            {"band": "5G", "channel": 36, "channel-mode": "HE", "channel-width": 80, "country": "CA"}]
        config['interfaces'][0]["ssids"][0]["wifi-bands"] = ["5G"]
        if len(dut_list) < 2:
            logging.error(
                f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}")
            assert False, f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}"
        for ap in range(len(dut_list)):
            serial_number = testbed_info[dut_list[ap]]["device_under_tests"][0]['identifier']
            dut_names.append(testbed_info[dut_list[ap]]["device_under_tests"][0]['model'])
            if ap == 1:
                config['interfaces'][0]["ssids"][0]["wifi-bands"] = ["2G"]
                config['radios'] = [
                    {"band": "2G", "channel": 11, "channel-mode": "HE", "channel-width": 20, "country": "CA"}]
            logging.info(config)
            payload = {"configuration": json.dumps(config), "serialNumber": serial_number, "UUID": 2}
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
            ap_iwinfo = get_target_object.dut_library_object.get_iwinfo(attach_allure=True)
            if str(ap_iwinfo) != "Error: pop from empty list":
                include_essid = config['interfaces'][0]["ssids"][0]["name"]
                re_obj = re.compile(
                    rf'(wlan\d(?:-\d)?)\s+ESSID: "{re.escape(include_essid)}".*?\s+Access Point:\s+([0-9A-Fa-f:]+).*?Channel:\s+('
                    r'\d+)\s+\(([\d.]+) GHz\)',
                    re.DOTALL
                )
                # find all matches
                interface_matches = re_obj.finditer(ap_iwinfo)
                if interface_matches:
                    for match in interface_matches:
                        interface_name = match.group(1)
                        access_point = match.group(2)
                        channel = match.group(3)
                        frequency = match.group(4).replace('.', '')
                        ap_data.update(
                            {serial_number: {'Access Point': access_point, 'Channel': channel, 'frequency': frequency}})
                    logging.info(f"AP Data from iwinfo: {ap_data}")
                else:
                    logging.error("Failed to get iwinfo")
                    pytest.exit("Failed to get iwinfo")
            elif ap_iwinfo == {}:
                pytest.fail("Empty iwinfo reponse from AP through minicom")
            else:
                pytest.fail("Failed to get iwinfo from minicom")
        for serial in ap_data:
            bssid_list.append(ap_data[serial]['Access Point'])
            if not ap_data[serial]['frequency'].endswith(","):
                freqs_ = freqs_ + ap_data[serial]['frequency'] + ","
            else:
                freqs_ = freqs_ + ap_data[serial]['frequency']
        ssid = config['interfaces'][0]["ssids"][0]["name"]
        key = config['interfaces'][0]["ssids"][0]["encryption"]["key"]
        try:
            pass_fail, message = get_test_library.roam_test(ap1_bssid=bssid_list[0], ap2_bssid=bssid_list[1],
                                                            scan_freq=freqs_,
                                                            band="both", num_sta=2, security="wpa2", security_key=key,
                                                            ssid=ssid, upstream="1.1.eth1", duration=None,
                                                            iteration=1, channel="36", option="ota", dut_name=dut_names,
                                                            traffic_type="lf_udp", sta_type="11r")
        except Exception as e:
            logging.error(f"Exception in roam test : {e}")
            pass_fail, message = False, e
        finally:
            get_target_object.dut_library_object.get_dut_logs(print_log=False)
        if not pass_fail:
            pytest.fail(f"Test failed with the following reasons: \n{message}")
        else:
            assert True