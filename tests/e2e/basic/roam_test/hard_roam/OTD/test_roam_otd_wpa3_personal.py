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

pytestmark = [pytest.mark.roam_test, pytest.mark.bridge, pytest.mark.hard_roam_otd, pytest.mark.ow_regression_lf]

# Get the directory of the current test config file
test_file_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path relative to the config file directory
file_path = os.path.join(test_file_dir, 'roam-config.json')
with open(file_path, 'r') as file:
    json_string = file.read()
    config_data = json.loads(json_string)


@allure.feature("Roam Test")
@allure.suite("11r Roaming over the DS")
@allure.parent_suite("Roam Test")
@allure.sub_suite("wpa3_personal")

@pytest.mark.wpa3_personal
@pytest.mark.sae
class TestRoamOTD(object):
    @pytest.mark.same_channel
    @pytest.mark.twog
    def test_roam_2g_to_2g_sc_wpa3_psk(self, get_target_object, get_test_library, get_lab_info, selected_testbed):
        """
            Test Roaming between two APs, Same channel, 2G, WPA3 Personal
            pytest -m "hard_roam_otd and twog and same_channel and wpa3_personal"
        """
        ap_data = dict()
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
        logging.info(f"temp_list:{temp_list}")
        dut_list = []
        idx = temp_list.index(selected_testbed)
        dut_list = [temp_list[idx]]
        if idx + 1 < len(temp_list):
            dut_list.append(temp_list[idx + 1])

        logging.info(f"---dut list: {dut_list}---")
        if len(dut_list) < 2:
            logging.error(
                f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}")
            assert False, f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}"
        # change ssid config data to sae
        config['radios'] = [
            {"band": "2G", "channel": 11, "channel-mode": "HE", "channel-width": 40, "country": "CA"}]
        config['interfaces'][0]["ssids"][0]["wifi-bands"] = ["2G"]
        config['interfaces'][0]["ssids"][0]["encryption"]["proto"] = "sae"
        for ap in range(len(dut_list)):
            serial_number = testbed_info[dut_list[ap]]["device_under_tests"][0]['identifier']
            dut_names.append(testbed_info[dut_list[ap]]["device_under_tests"][0]['model'])
            logging.info(f"config:{config}")
            payload = {"configuration": json.dumps(config), "serialNumber": serial_number, "UUID": 2}
            uri = get_target_object.controller_library_object.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.controller_library_object.make_headers()))
            allure.attach(name=f"Push roam config on AP{ap+1}:{serial_number}: ", body="Sending Command: " + str(uri) + "\n" +
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
                    rf'([a-zA-Z0-9-]+)\s+ESSID: "{re.escape(include_essid)}".*?\s+Access Point:\s+([0-9A-Fa-f:]+).*?Channel:\s+('
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
        logging.info(f"AP Data from iwinfo: {ap_data}")
        for serial in ap_data:
            bssid_list.append(ap_data[serial]['Access Point'])
            if not ap_data[serial]['frequency'].endswith(","):
                freqs_ = freqs_ + ap_data[serial]['frequency'] + ","
            else:
                freqs_ = freqs_ + ap_data[serial]['frequency']
        ssid = config['interfaces'][0]["ssids"][0]["name"]
        key = config['interfaces'][0]["ssids"][0]["encryption"]["key"]
        pass_fail, message = True, "Test Passed"
        twog_radio = list(get_test_library.get_radio_availabilities(num_stations_2g=1)[0].keys())[0]
        logging.info(f"twog_radio from testcase:{twog_radio}")
        try:
            pass_fail, message = get_test_library.roam_test(ap1_bssid=bssid_list[0], ap2_bssid=bssid_list[1],
                                                            scan_freq=freqs_, twog_radio=twog_radio,
                                                            band="twog", num_sta=1, security="wpa3", security_key=key,
                                                            ssid=ssid, upstream="1.1.eth1", duration=None,
                                                            iteration=1, channel="11", option="otd", dut_name=dut_names,
                                                            traffic_type="lf_udp", sta_type="11r-sae")
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
    def test_roam_5g_to_5g_sc_wpa3_psk(self, get_target_object, get_test_library, get_lab_info, selected_testbed):
        """
            Test Roaming between two APs, Same channel, 5G, WPA3 Personal
            pytest -m "hard_roam_otd and fiveg and same_channel and wpa3_personal"
        """
        get_test_library.check_band_ap("fiveg")
        ap_data = dict()
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
        logging.info(f"temp_list:{temp_list}")
        dut_list = []
        idx = temp_list.index(selected_testbed)
        dut_list = [temp_list[idx]]
        if idx + 1 < len(temp_list):
            dut_list.append(temp_list[idx + 1])

        logging.info(f"---dut list: {dut_list}---")

        if len(dut_list) < 2:
            logging.error(
                f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}")
            assert False, f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}"
        # change ssid config data to sae
        config['radios'] = [
            {"band": "5G", "channel": 36, "channel-mode": "HE", "channel-width": 80, "country": "CA"}]
        config['interfaces'][0]["ssids"][0]["wifi-bands"] = ["5G"]
        config['interfaces'][0]["ssids"][0]["encryption"]["proto"] = "sae"
        for ap in range(len(dut_list)):
            serial_number = testbed_info[dut_list[ap]]["device_under_tests"][0]['identifier']
            dut_names.append(testbed_info[dut_list[ap]]["device_under_tests"][0]['model'])
            logging.info(f"config:{config}")
            payload = {"configuration": json.dumps(config), "serialNumber": serial_number, "UUID": 2}
            uri = get_target_object.controller_library_object.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.controller_library_object.make_headers()))
            allure.attach(name=f"Push roam config on AP{ap+1}:{serial_number}: ", body="Sending Command: " + str(uri) + "\n" +
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
                    rf'([a-zA-Z0-9-]+)\s+ESSID: "{re.escape(include_essid)}".*?\s+Access Point:\s+([0-9A-Fa-f:]+).*?Channel:\s+('
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
        logging.info(f"AP Data from iwinfo: {ap_data}")
        for serial in ap_data:
            bssid_list.append(ap_data[serial]['Access Point'])
            if not ap_data[serial]['frequency'].endswith(","):
                freqs_ = freqs_ + ap_data[serial]['frequency'] + ","
            else:
                freqs_ = freqs_ + ap_data[serial]['frequency']
        ssid = config['interfaces'][0]["ssids"][0]["name"]
        key = config['interfaces'][0]["ssids"][0]["encryption"]["key"]
        pass_fail, message = True, "Test Passed"
        fiveg_radio = list(get_test_library.get_radio_availabilities(num_stations_5g=1)[0].keys())[0]
        logging.info(f"fiveg_radio from testcase:{fiveg_radio}")
        try:
            pass_fail, message = get_test_library.roam_test(ap1_bssid=bssid_list[0], ap2_bssid=bssid_list[1],
                                                            scan_freq=freqs_, fiveg_radio=fiveg_radio,
                                                            band="fiveg", num_sta=1, security="wpa3", security_key=key,
                                                            ssid=ssid, upstream="1.1.eth1", duration=None,
                                                            iteration=1, channel="11", option="otd", dut_name=dut_names,
                                                            traffic_type="lf_udp", sta_type="11r-sae")
        except Exception as e:
            logging.error(f"Exception in roam test : {e}")
            pass_fail, message = False, e
        finally:
            get_target_object.dut_library_object.get_dut_logs(print_log=False)
        if not pass_fail:
            pytest.fail(f"Test failed with the following reasons: \n{message}")
        else:
            assert True

    @pytest.mark.sixg
    @pytest.mark.same_channel
    def test_roam_6g_to_6g_sc_wpa3_psk(self, get_target_object, get_test_library, get_lab_info, selected_testbed):
        """
            Test Roaming between two APs, Same channel, 6G, WPA3 Personal
            pytest -m "hard_roam_otd and sixg and same_channel and wpa3_personal"
        """

        ap_data = dict()
        dut_names = list()
        bssid_list = list()
        band = "sixg"
        freqs_ = ""
        testbed_info = get_lab_info.CONFIGURATION
        config = copy.deepcopy(config_data)
        temp_list = list()
        for key, val in testbed_info.items():
            tb_type, tb_name = selected_testbed.split("-")
            if tb_type in key and tb_name[0] in key:
                temp_list.append(key)
        temp_list.sort()
        logging.info(f"temp_list:{temp_list}")
        ap_modes = {ap: testbed_info[ap]["device_under_tests"][0]["mode"].lower() for ap in temp_list}

        wifi7 = [ap for ap, m in ap_modes.items() if "wifi7" in m]
        wifi6e = [ap for ap, m in ap_modes.items() if "wifi6e" in m]
        wifi6 = [ap for ap, m in ap_modes.items() if "wifi6" in m and "wifi6e" not in m]

        logging.info(f"Available APs by type -> WiFi7: {wifi7}, WiFi6E: {wifi6e}, WiFi6: {wifi6}")
        try:
            if band == "sixg":
                sixg_aps = wifi7 + wifi6e
                if len(sixg_aps) < 2:
                    raise ValueError("Not enough 6GHz-capable APs")
                dut_list = sixg_aps[:2]
            else:
                ap2 = (wifi7 or wifi6e or [None])[0] if "sixg" in band else None
                ap1 = (wifi6 or wifi7 or wifi6e or [None])[0] if any(b in band for b in ["twog", "fiveg"]) else None
                if not ap1 or (("sixg" in band) and not ap2):
                    raise ValueError("Required APs not found")
                dut_list = [ap for ap in [ap1, ap2] if ap]

        except ValueError as e:
            logging.warning(f"No available APs satisfy the required band '{band}': {e}")
            pytest.skip(f"No available APs satisfy the required band '{band}': {e}")
            dut_list = []
        logging.info(f"Selected DUTs for band='{band}': {dut_list}")
        logging.info(f"---dut list: {dut_list}---")

        # change wifi-band and security type to sae
        for ap in range(len(dut_list)):
            serial_number = testbed_info[dut_list[ap]]["device_under_tests"][0]['identifier']
            dut_names.append(testbed_info[dut_list[ap]]["device_under_tests"][0]['model'])
            ap_mode = testbed_info[dut_list[ap]]["device_under_tests"][0]['mode']
            logging.info(f"ap_mode:{ap_mode}")
            channel_mode = "EHT" if "wifi7" in ap_mode else "HE"
            config['radios'] = [
                {"band": "6G", "channel": 161, "channel-mode": channel_mode, "channel-width": 80, "country": "US"}]
            config['interfaces'][0]["ssids"][0]["wifi-bands"] = ["6G"]
            config['interfaces'][0]["ssids"][0]["encryption"]["proto"] = "sae"

            logging.info(f"config:{config}")
            payload = {"configuration": json.dumps(config), "serialNumber": serial_number, "UUID": 2}
            uri = get_target_object.controller_library_object.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.controller_library_object.make_headers()))
            allure.attach(name=f"Push roam config on AP{ap+1}:{serial_number}: ", body="Sending Command: " + str(uri) + "\n" +
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
                    rf'([a-zA-Z0-9-]+)\s+ESSID: "{re.escape(include_essid)}".*?\s+Access Point:\s+([0-9A-Fa-f:]+).*?Channel:\s+('
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
                    logging.info(f"Extracted AP Data from iwinfo: {ap_data}")
                if ap_data == {}:
                    logging.error("Failed to get required iwinfo from minicom")
                    pytest.fail("Failed to get required iwinfo from minicom")
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
        sixg_radio = list(get_test_library.get_radio_availabilities(num_stations_6g=1)[0].keys())[0]
        logging.info(f"sixg_radio from testcase:{sixg_radio}")
        try:
            pass_fail, message = get_test_library.roam_test(ap1_bssid=bssid_list[0], ap2_bssid=bssid_list[1],
                                                            scan_freq=freqs_, sixg_radio=sixg_radio,
                                                            band="sixg", num_sta=1, security="wpa3", security_key=key,
                                                            ssid=ssid, upstream="1.1.eth1", duration=None,
                                                            iteration=1, channel="11", option="otd", dut_name=dut_names,
                                                            traffic_type="lf_udp", sta_type="11r-sae")
        except Exception as e:
            logging.error(f"Exception in roam test : {e}")
            pass_fail, message = False, e
        finally:
            get_target_object.dut_library_object.get_dut_logs(print_log=False)
        if not pass_fail:
            pytest.fail(f"Test failed with the following reasons: \n{message}")
        else:
            assert True