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


@allure.suite("Hard Roam over the air")
@allure.feature("Roam Test")
class TestRoamOTA(object):
    @pytest.mark.same_channel
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.roam
    def test_roam_2g_to_2g_ft_psk_wpa2(self, get_target_object, get_test_library, get_lab_info, selected_testbed):
        """
            Test Roaming between two APs, Same channel, 2G, WPA2 Personal
            pytest -m "roam and twog and same_channel and wpa2_personal"
        """
        dut_list =[]
        logging.info("----------lab-info----------------")
        logging.info(str(get_lab_info.CONFIGURATION))
        logging.info(str(selected_testbed))
        logging.info("----------lab-info----------------")
        dut_list.append(str(selected_testbed))
        testbed_info = get_lab_info.CONFIGURATION
        if str(selected_testbed + 'a') in testbed_info:
            dut_list.append(str(selected_testbed + 'a'))
        logging.info(f"--dut list: {dut_list}--")
        if len(dut_list) < 2:
            logging.error(f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}")
            assert False, f"This test need two AP's but number of DUT's available in the selected testbed is {dut_list}"
        for ap in range(len(dut_list)):
            serial_number = testbed_info[dut_list[ap]]["device_under_tests"][0]['identifier']
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
                assert False, f"push configuration to {serial_number} got failed"
            ap1_iwinfo = get_target_object.dut_library_object.get_iwinfo(attach_allure=False)
            if str(ap1_iwinfo) != "pop from empty list":
                interfaces = {}
                interface_matches = re.finditer(
                    r'wlan\d\s+ESSID:\s+".*?"\s+Access Point:\s+([0-9A-Fa-f:]+).*?Channel:\s+([\d\s]+)', ap1_iwinfo,
                    re.DOTALL)
                logging.info(str(interface_matches))
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
            elif ap1_iwinfo == {}:
                assert False, "Empty iwinfo reponse from AP through minicom"
            else:
                assert False, "Failed to get iwinfo from minicom"
            get_test_library.roam_test(ap1_bssid="90:3c:b3:6c:46:dd", ap2_bssid="90:3c:b3:6c:47:2d", fiveg_radio="1.1.wiphy4",
                  twog_radio="1.1.wiphy4", sixg_radio="1.1.wiphy4",
                  band="twog", sniff_radio_="1.1.wiphy5", num_sta=1, security="wpa2", security_key="Openwifi",
                  ssid="OpenWifi", upstream="1.1.eth1", duration=None, iteration=1, channel="11", option="ota",
                  dut_name=["edgecore_eap101", "edgecore_eap102"], traffic_type="lf_udp", identity="identity",
                  ttls_pass="ttls_pass", sta_type="11r")
        assert True

    @pytest.mark.hard_roam_2g_ota
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    def test_multi_hard_roam_2g_to_2g_ft_psk_wpa2(self, get_configuration, lf_test, lf_reports, lf_tools,
                                                  run_lf, add_env_properties,
                                                  instantiate_profile, get_controller_logs, get_ap_config_slots,
                                                  get_lf_logs,
                                                  roaming_delay, iteration, client, duration):
        instantiate_profile_obj = instantiate_profile(controller_data=get_configuration['controller'],
                                                      timeout="10",
                                                      ap_data=get_configuration['access_point'],
                                                      type=0)
        print("shut down 5g and 6g band")
        instantiate_profile_obj.ap_5ghz_shutdown()
        instantiate_profile_obj.ap_6ghz_shutdown()
        print("enable only 2g")
        instantiate_profile_obj.no_ap_2ghz_shutdown()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        print("disable wlan ")
        instantiate_profile_obj.disable_wlan(wlan=setup_params_general["ssid_modes"]["wpa2_personal"][1]["ssid_name"])
        instantiate_profile_obj.disable_wlan(wlan=setup_params_general["ssid_modes"]["wpa3_personal"][0]["ssid_name"])
        dut_name = []
        for i in range(len(get_configuration["access_point"])):
            dut_name.append(get_configuration["access_point"][i]["ap_name"])

        print("dut names", dut_name)
        # check channel

        lf_test.create_n_clients(sta_prefix="wlan", num_sta=1, dut_ssid=ssid_name,
                                 dut_security=security, dut_passwd=security_key, band="twog",
                                 lf_tools=lf_tools, type="11r")
        sta_list = lf_tools.get_station_list()
        print(sta_list)
        val = lf_test.wait_for_ip(station=sta_list)
        ch = ""
        if val:
            for sta_name in sta_list:
                sta = sta_name.split(".")[2]
                time.sleep(5)
                ch = lf_tools.station_data_query(station_name=str(sta), query="channel")
            print(ch)
            lf_test.Client_disconnect(station_name=sta_list)

        else:
            pytest.exit("station failed to get ip")
            assert False

        lf_test.hard_roam(run_lf=run_lf, get_configuration=get_configuration, lf_tools=lf_tools,
                          instantiate_profile=instantiate_profile, lf_reports=lf_reports,
                          ssid_name=ssid_name, security=security, security_key=security_key,
                          band=band, test="2g",
                          iteration=int(iteration), num_sta=int(client), roaming_delay=roaming_delay,
                          option="ota", channel=ch, duration=duration, duration_based=False,
                          iteration_based=True, dut_name=dut_name)

    @pytest.mark.hard_roam_6g_to_6g_dot1x_sha256
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    def test_multi_hard_roam_6g_to_6g_802dot1x_sha256_wpa3(self, get_configuration, lf_test, lf_reports, lf_tools,
                                                           run_lf, add_env_properties,
                                                           instantiate_profile, get_controller_logs,
                                                           get_ap_config_slots,
                                                           get_lf_logs,
                                                           roaming_delay, iteration, client, duration, radius_info):
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        instantiate_profile_obj = instantiate_profile(controller_data=get_configuration['controller'],
                                                      timeout="10",
                                                      ap_data=get_configuration['access_point'],
                                                      type=0)
        print("shut down 2g  band")
        instantiate_profile_obj.ap_2ghz_shutdown()
        print("enable only 5g and 6g")
        instantiate_profile_obj.no_ap_5ghz_shutdown()
        instantiate_profile_obj.no_ap_6ghz_shutdown()

        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "sixg"
        vlan = 1
        print("disable wlan ")
        instantiate_profile_obj.disable_wlan(wlan=setup_params_general["ssid_modes"]["wpa2_personal"][0]["ssid_name"])
        instantiate_profile_obj.disable_wlan(wlan=setup_params_general["ssid_modes"]["wpa2_personal"][1]["ssid_name"])
        dut_name = []
        for i in range(len(get_configuration["access_point"])):
            dut_name.append(get_configuration["access_point"][i]["ap_name"])

        print("dut names", dut_name)

        # check channel
        lf_test.create_n_clients(sta_prefix="wlan1", num_sta=1, dut_ssid=ssid_name,
                                 dut_security=security, dut_passwd=security_key, band="sixg",
                                 lf_tools=lf_tools, type="11r-sae-802.1x")
        sta_list = lf_tools.get_station_list()
        print(sta_list)
        val = lf_test.wait_for_ip(station=sta_list)
        ch = ""
        if val:
            for sta_name in sta_list:
                sta = sta_name.split(".")[2]
                time.sleep(5)
                ch = lf_tools.station_data_query(station_name=str(sta), query="channel")
            print(ch)
            lf_test.Client_disconnect(station_name=sta_list)

        else:
            pytest.exit("station failed to get ip")
            assert False

        lf_test.hard_roam(run_lf=run_lf, get_configuration=get_configuration, lf_tools=lf_tools,
                          lf_reports=lf_reports,
                          instantiate_profile=instantiate_profile,
                          ssid_name=ssid_name, security=security, security_key=security_key,
                          band=band, test="6g",
                          iteration=int(iteration), num_sta=int(client), roaming_delay=roaming_delay,
                          option="ota", channel=ch, duration=duration, iteration_based=True,
                          duration_based=False, dut_name=dut_name, identity=identity, ttls_passwd=ttls_passwd)
