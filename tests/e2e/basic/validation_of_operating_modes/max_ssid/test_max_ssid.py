"""
    Config AP with maximum no.of SSIDs Test: Bridge Mode
    pytest -m max_ssid
"""
import logging
import os
import time
from datetime import datetime

import allure
import pytest
import json

import requests

# Get the directory of the current test config file
test_file_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path relative to the config file directory
file_path = os.path.join(test_file_dir, 'multi-security-test-config.json')
with open(file_path, 'r') as file:
    json_string = file.read()
    config_data = json.loads(json_string)

pytestmark = [pytest.mark.max_ssid, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"]}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMaxEightSsid2G(object):
    """Config AP with maximum no.of SSIDs Test Bridge mode
           pytest -m "max_ssid and bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.open
    @pytest.mark.wpa
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    @pytest.mark.eight_ssid_2g
    @pytest.mark.twog
    def test_max_eight_ssid_2g(self, lf_test, station_names_twog, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        scan_ssid = True
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        count_security, sta_count = 0, 0
        pass_list = []
        security_key = "something"
        security_list = ["open", "wpa", "wpa2", "wpa3"]
        sta_list = []
        for i in setup_params_general["ssid_modes"]:
            for j in range(len(setup_params_general["ssid_modes"][i])):
                profile_data = setup_params_general["ssid_modes"][i][j]
                ssid_name = profile_data["ssid_name"]
                security = security_list[count_security]
                station_names = station_names_twog[0] + str(int(station_names_twog[0][-1]) + sta_count)
                passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                band=band, station_name=[station_names], vlan_id=vlan,
                                                scan_ssid=scan_ssid)
                scan_ssid = False
                pass_list.append(passes)
                sta_list.append(station_names)
                sta_count += 1
            count_security += 1
        fail_list = list(filter(lambda x: x == False, pass_list))
        if len(fail_list) == 0:
            lf_test.layer3_traffic(ssid_num=len(pass_list), band="2.4 Ghz", station_name=sta_list)
            assert True
        else:
            assert False


setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"]},
            {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"]}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMaxEightSsid5G(object):
    """Config AP with maximum no.of SSIDs Test Bridge mode
           pytest -m "max_ssid and bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.open
    @pytest.mark.wpa
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    @pytest.mark.eight_ssid_5g
    @pytest.mark.fiveg
    def test_max_eight_ssid_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and fiveg"
        """
        scan_ssid = True
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        count_security, sta_count = 0, 0
        pass_list = []
        security_key = "something"
        security_list = ["open", "wpa", "wpa2", "wpa3"]
        sta_list = []
        for i in setup_params_general1["ssid_modes"]:
            for j in range(len(setup_params_general1["ssid_modes"][i])):
                profile_data = setup_params_general1["ssid_modes"][i][j]
                ssid_name = profile_data["ssid_name"]
                security = security_list[count_security]
                station_names = station_names_fiveg[0] + str(int(station_names_fiveg[0][-1]) + sta_count)
                passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                band=band, station_name=[station_names], vlan_id=vlan,
                                                scan_ssid=scan_ssid)
                scan_ssid = False
                pass_list.append(passes)
                sta_list.append(station_names)
                sta_count += 1
            count_security += 1
        fail_list = list(filter(lambda x: x == False, pass_list))
        if len(fail_list) == 0:
            lf_test.layer3_traffic(ssid_num=len(pass_list), band="5 Ghz", station_name=sta_list)
            assert True
        else:
            assert False


setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"]}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid3_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMoreThanEightSsid2G(object):
    """Config AP with maximum no.of SSIDs Test Bridge mode
           pytest -m "max_ssid and bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.open
    @pytest.mark.wpa
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    @pytest.mark.more_than_eight_ssid_2g
    @pytest.mark.twog
    def test_more_than_eight_ssid_2g(self, lf_test, station_names_twog, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        scan_ssid = True
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        count_security, sta_count = 0, 0
        pass_list = []
        security_key = "something"
        security_list = ["open", "wpa", "wpa2", "wpa3"]
        sta_list = []
        for i in setup_params_general2["ssid_modes"]:
            for j in range(len(setup_params_general2["ssid_modes"][i])):
                profile_data = setup_params_general2["ssid_modes"][i][j]
                ssid_name = profile_data["ssid_name"]
                security = security_list[count_security]
                station_names = station_names_twog[0] + str(int(station_names_twog[0][-1]) + sta_count)
                passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                band=band, station_name=[station_names], vlan_id=vlan,
                                                scan_ssid=scan_ssid)
                scan_ssid = False
                pass_list.append(passes)
                sta_list.append(station_names)
                sta_count += 1
            count_security += 1
        fail_list = list(filter(lambda x: x == False, pass_list))
        if len(fail_list) == len(pass_list):
            lf_test.Client_disconnect(sta_list)
            allure.attach(name="Definition",
                          body="Max-SSID test intends to verify stability of Wi-Fi device " \
                               "where the AP is configured with max no.of SSIDs with different security modes.")
            allure.attach(name="Procedure",
                          body=f"This test case definition states that we need to push the basic bridge mode config on the "
                               f"AP to be tested by configuring it with maximum {len(pass_list)} SSIDs in {band} radio. "
                               f"Create client on each SSIDs and run Layer-3 traffic. Pass/ fail criteria: "
                               f"The client created should not get associated to the AP")
            # lf_test.layer3_traffic(ssid_num=len(pass_list), band="2.4 Ghz", station_name=sta_list)
            assert True
        else:
            assert False


setup_params_general3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"]},
            {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"]}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid3_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general3],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMoreThanEightSsid5G(object):
    """Config AP with maximum no.of SSIDs Test Bridge mode
           pytest -m "max_ssid and bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.open
    @pytest.mark.wpa
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    @pytest.mark.more_than_eight_ssid_5g
    @pytest.mark.fiveg
    def test_more_than_eight_ssid_5g(self, lf_test, station_names_fiveg, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and fiveg"
        """
        scan_ssid = True
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        count_security, sta_count = 0, 0
        pass_list = []
        security_key = "something"
        security_list = ["open", "wpa", "wpa2", "wpa3"]
        sta_list = []
        for i in setup_params_general3["ssid_modes"]:
            for j in range(len(setup_params_general3["ssid_modes"][i])):
                profile_data = setup_params_general3["ssid_modes"][i][j]
                ssid_name = profile_data["ssid_name"]
                security = security_list[count_security]
                station_names = station_names_fiveg[0] + str(int(station_names_fiveg[0][-1]) + sta_count)
                passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                band=band, station_name=[station_names], vlan_id=vlan,
                                                scan_ssid=scan_ssid)
                scan_ssid = False
                pass_list.append(passes)
                sta_list.append(station_names)
                sta_count += 1
            count_security += 1
        fail_list = list(filter(lambda x: x == False, pass_list))
        if len(fail_list) == len(pass_list):
            lf_test.Client_disconnect(sta_list)
            allure.attach(name="Definition",
                          body="Max-SSID test intends to verify stability of Wi-Fi device " \
                               "where the AP is configured with max no.of SSIDs with different security modes.")
            allure.attach(name="Procedure",
                          body=f"This test case definition states that we need to push the basic bridge mode config on the "
                               f"AP to be tested by configuring it with maximum {len(pass_list)} SSIDs in {band} radio. "
                               f"Create client on each SSIDs and run Layer-3 traffic. Pass/ fail criteria: "
                               f"The client created should not get associated to the AP")
            # lf_test.layer3_traffic(ssid_num=len(pass_list), band="5 Ghz", station_name=sta_list)
            assert True
        else:
            assert False


setup_params_general4 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"]},
                 {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"]}],

        "wpa": [{"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"},
                {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general4],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMaxSixteenSsid(object):
    """Config AP with maximum no.of SSIDs Test Bridge mode
       pytest -m "max_ssid and bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.open
    @pytest.mark.wpa
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    @pytest.mark.sixteen_ssid_2g_5g
    @pytest.mark.twog
    @pytest.mark.fiveg
    def test_max_sixteen_2g_5g(self, lf_test, station_names_twog, station_names_fiveg, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog and fiveg"
        """
        scan_ssid = True
        mode = "BRIDGE"
        band_name = (lambda bnd: '2G' if bnd == 'twog' else '5G')
        vlan = 1
        count_security, sta_count = 0, 0
        pass_list = []
        security_key = "something"
        security_list = ["open", "wpa", "wpa2", "wpa3"]
        sta_list = []
        for i in setup_params_general4["ssid_modes"]:
            for j in range(len(setup_params_general4["ssid_modes"][i])):
                profile_data = setup_params_general4["ssid_modes"][i][j]
                ssid_name = profile_data["ssid_name"]
                security = security_list[count_security]
                if profile_data["appliedRadios"] == ['2G']:
                    band = 'twog'
                    sta_name = station_names_twog
                elif profile_data["appliedRadios"] == ['5G']:
                    band = 'fiveg'
                    sta_name = station_names_fiveg
                station_names = band_name(band) + sta_name[0] + str(int(sta_name[0][-1]) + sta_count)
                passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                band=band, station_name=[station_names], vlan_id=vlan,
                                                scan_ssid=scan_ssid)
                scan_ssid = False
                pass_list.append(passes)
                sta_list.append(station_names)
                sta_count += 1
            count_security += 1
        fail_list = list(filter(lambda x: x == False, pass_list))
        if len(fail_list) == 0:
            lf_test.layer3_traffic(ssid_num=len(pass_list), band="2.4 Ghz and 5 Ghz", station_name=sta_list)
            assert True
        else:
            assert False


setup_params_general5 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"]},
                 {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"]}],

        "wpa": [{"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"},
                {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid3_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid3_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMoreThanSixteenSsid(object):
    """Config AP with maximum no.of SSIDs Test Bridge mode
       pytest -m "max_ssid and bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.open
    @pytest.mark.wpa
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    @pytest.mark.more_than_sixteen_ssid_2g_5g
    @pytest.mark.twog
    @pytest.mark.fiveg
    def test_more_than_sixteen_2g_5g(self, lf_test, station_names_twog, station_names_fiveg, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog and fiveg"
        """
        scan_ssid = True
        mode = "BRIDGE"
        band_name = (lambda bnd: '2G' if bnd == 'twog' else '5G')
        vlan = 1
        count_security, sta_count = 0, 0
        pass_list = []
        security_key = "something"
        security_list = ["open", "wpa", "wpa2", "wpa3"]
        sta_list = []
        for i in setup_params_general5["ssid_modes"]:
            for j in range(len(setup_params_general5["ssid_modes"][i])):
                profile_data = setup_params_general5["ssid_modes"][i][j]
                ssid_name = profile_data["ssid_name"]
                security = security_list[count_security]
                if profile_data["appliedRadios"] == ['2G']:
                    band = 'twog'
                    sta_name = station_names_twog
                elif profile_data["appliedRadios"] == ['5G']:
                    band = 'fiveg'
                    sta_name = station_names_fiveg
                station_names = band_name(band) + sta_name[0] + str(int(sta_name[0][-1]) + sta_count)
                passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                band=band, station_name=[station_names], vlan_id=vlan,
                                                scan_ssid=scan_ssid)
                scan_ssid = False
                pass_list.append(passes)
                sta_list.append(station_names)
                sta_count += 1
            count_security += 1
        fail_list = list(filter(lambda x: x == False, pass_list))
        if len(fail_list) == len(pass_list):
            lf_test.Client_disconnect(sta_list)
            allure.attach(name="Definition",
                          body="Max-SSID test intends to verify stability of Wi-Fi device " \
                               "where the AP is configured with max no.of SSIDs with different security modes.")
            allure.attach(name="Procedure",
                          body=f"This test case definition states that we need to push the basic bridge mode config on the "
                               f"AP to be tested by configuring it with maximum {len(pass_list)} SSIDs in 2.4 Ghz and 5 Ghz radio. "
                               f"Create client on each SSIDs and run Layer-3 traffic. Pass/ fail criteria: "
                               f"The client created should not get associated to the AP")
            # lf_test.layer3_traffic(ssid_num=len(pass_list), band="2.4 Ghz and 5 Ghz", station_name=sta_list)
            assert True
        else:
            assert False


class TestMultiSecurityConfig(object):
    """
        Test Config with various Security Modes
        pytest -m "multi_security_config and bridge "
    """
    @allure.title("Test Config with Multiple Securities")
    @pytest.mark.multi_security_config
    def test_multi_security_config(self, get_target_object, get_test_library, check_connectivity):
        configured_ssid_data = config_data["interfaces"][0]["ssids"]
        for ap in range(len(get_target_object.device_under_tests_info)):
            serial_number = get_target_object.device_under_tests_info[ap]['identifier']
            logging.info(config_data)
            payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
            uri = get_target_object.firmware_library_object.sdk_client.build_uri(
                "device/" + serial_number + "/configure")
            logging.info("Sending Command: " + str(uri) + "\n" +
                         "TimeStamp: " + str(datetime.utcnow()) + "\n" +
                         "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                         "Headers: " + str(get_target_object.firmware_library_object.sdk_client.make_headers()))
            allure.attach(name="Sending Command:", body="Sending Command: " + str(uri) + "\n" +
                                                        "TimeStamp: " + str(datetime.utcnow()) + "\n" +
                                                        "Data: " + str(payload) + "\n" +
                                                        "Headers: " + str(
                get_target_object.firmware_library_object.sdk_client.make_headers()))
            resp = requests.post(uri, data=json.dumps(payload),
                                 headers=get_target_object.firmware_library_object.sdk_client.make_headers(),
                                 verify=False, timeout=120)
            logging.info(resp.json())
            allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))
            if resp.status_code != 200:
                pytest.fail(f"configuration push failed, Error - {resp.reason}")
            get_test_library.set_radio_channel(radio="1.1.wiphy0", channel="36", country=None, antenna=None)
            for i in range(len(configured_ssid_data)):
                get_test_library.scan_ssid(radio="wiphy0", retry=1, allure_attach=True, scan_time=30,
                                           ssid=configured_ssid_data[i]["name"], ssid_channel=None)
        assert True
