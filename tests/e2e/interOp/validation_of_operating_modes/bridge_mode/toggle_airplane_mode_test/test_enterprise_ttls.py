"""

    Client Connect : BRIDGE Mode
    pytest -m "client_connect_tests and nat and general"

"""
import logging

import allure
import pytest

import random
import string
import time

pytestmark = [pytest.mark.toggle_airplane_tests, pytest.mark.bridge, pytest.mark.enterprise]

setup_params_enterprise = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa_enterprise": [
            {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_wpa_eap_5g", "appliedRadios": ["5G"]}],
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"]}],
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"]}]},

    "rf": {},
    "radius": True
}

for sec_modes in setup_params_enterprise['ssid_modes'].keys():
    for i in range(len(setup_params_enterprise['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                              string.digits, k=N))) + str(int(time.time_ns()) % 10000)
        setup_params_enterprise['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_enterprise['ssid_modes'][sec_modes][i]['ssid_name'] + "_" + rand_string

@allure.feature("BRIDGE MODE TOGGLE AIRPLANE")
@allure.parent_suite("Toggle Airplane Tests")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="Enterprise ttls Toggle Airplane")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestBridgeModeToggleAirplaneEnterpriseTTLSSuiteOne(object):
    """ Client Connect SuiteA
        pytest -m "client_connect and bridge and InteropsuiteA"
    """

    @pytest.mark.wpa_enterprise
    @pytest.mark.twog
    @allure.story('wpa enterprise 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Toggle Airplane Test with wpa enterprise encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-11102", name="JIRA LINK")
    def test_bridge_wpa_enterprise_2g_toggle_airplane(self, get_test_library, get_dut_logs_per_test_case,
                                                      get_test_device_logs, num_stations, setup_configuration,
                                                      radius_info):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        # security_key = "[BLANK]"
        security = "wpa"
        mode = "BRIDGE"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info["user"]
        passes, result = get_test_library.enterprise_toggle_airplane_mode_test(ssid=ssid_name, identity=identity,
                                                                          ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))

        assert passes == "PASS", result

    @pytest.mark.wpa_enterprise
    @pytest.mark.fiveg
    @allure.story('wpa enterprise 5 GHZ Band')
    @allure.title("BRIDGE Mode Toggle Airplane Test with wpa enterprise encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-11102", name="JIRA LINK")
    def test_bridge_wpa_enterprise_5g_toggle_airplane(self, get_test_library, get_dut_logs_per_test_case,
                                                      get_test_device_logs, num_stations, setup_configuration,
                                                      radius_info):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        # security_key = "[BLANK]"
        security = "wpa"
        mode = "BRIDGE"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info["user"]
        passes, result = get_test_library.enterprise_toggle_airplane_mode_test(ssid=ssid_name, identity=identity,
                                                                          ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))

        assert passes == "PASS", result


    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.story('wpa2 enterprise 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Toggle Airplane Test with wpa2 enterprise encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-11102", name="JIRA LINK")
    def test_bridge_wpa2_enterprise_2g_toggle_airplane(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration, radius_info):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        # security_key = "[BLANK]"
        security = "wpa"
        mode = "BRIDGE"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info["user"]
        passes, result = get_test_library.enterprise_toggle_airplane_mode_test(ssid=ssid_name, identity=identity,
                                                                ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))

        assert passes == "PASS", result


    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.story('wpa2 enterprise 5 GHZ Band')
    @allure.title("BRIDGE Mode Toggle Airplane Test with wpa2 enterprise encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-11102", name="JIRA LINK")
    def test_bridge_wpa2_enterprise_5g_toggle_airplane(self, get_test_library, get_dut_logs_per_test_case,
                                                       get_test_device_logs, num_stations, setup_configuration,
                                                       radius_info):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        # security_key = "[BLANK]"
        security = "wpa"
        mode = "BRIDGE"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info["user"]
        passes, result = get_test_library.enterprise_toggle_airplane_mode_test(ssid=ssid_name, identity=identity,
                                                                          ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    @allure.story('wpa3 enterprise 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Toggle Airplane Test with wpa3 enterprise encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-11102", name="JIRA LINK")
    def test_bridge_wpa3_enterprise_2g_toggle_airplane(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration, radius_info):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        # security_key = "[BLANK]"
        security = "wpa"
        mode = "BRIDGE"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info["user"]
        passes, result = get_test_library.enterprise_toggle_airplane_mode_test(ssid=ssid_name, identity=identity,
                                                                ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    @allure.story('wpa3 enterprise 5 GHZ Band')
    @allure.title("BRIDGE Mode Toggle Airplane Test with wpa3 enterprise encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-11102", name="JIRA LINK")
    def test_bridge_wpa3_enterprise_5g_toggle_airplane(self, get_test_library, get_dut_logs_per_test_case,
                                                       get_test_device_logs, num_stations, setup_configuration,
                                                       radius_info):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        # security_key = "[BLANK]"
        security = "wpa"
        mode = "BRIDGE"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info["user"]
        passes, result = get_test_library.enterprise_toggle_airplane_mode_test(ssid=ssid_name, identity=identity,
                                                                          ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))

        assert passes == "PASS", result

setup_params_enterprise_two_br = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa_wpa2_enterprise_mixed": [
            {"ssid_name": "wpa_wpa2_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "wpa_wpa2_eap_5g", "appliedRadios": ["5G"]}],
        "wpa3_enterprise_mixed": [
            {"ssid_name": "wpa3_m_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "wpa3_m_eap_5g", "appliedRadios": ["5G"]}]
    },
    "rf": {},
    "radius": True
}

for sec_modes in setup_params_enterprise_two_br['ssid_modes'].keys():
    for i in range(len(setup_params_enterprise_two_br['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_enterprise_two_br['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_enterprise_two_br['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string

@allure.feature("BRIDGE MODE TOGGLE AIRPLANE")
@allure.parent_suite("Toggle Airplane Tests")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="Enterprise ttls Toggle Airplane")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_enterprise_two_br],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestBridgeModeEnterpriseTTLSSuiteTwo(object):
    """ SuiteA Enterprise Test Cases
        pytest -m "client_connectivity and bridge and enterprise and ttls and suiteB"
    """

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.twog
    @allure.story('wpa_wpa2_enterprise_mixed 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Toggle Airplane Test with wpa_wpa2_enterprise_mixed encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4565", name="JIRA LINK")
    def test_bridge_wpa_wpa2_enterprise_mixed_2g_toggle_airplane(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration, radius_info):

        profile_data = setup_params_enterprise_two_br["ssid_modes"]["wpa_wpa2_enterprise_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        # security_key = profile_data["#security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info["user"]
        passes, result = get_test_library.enterprise_toggle_airplane_mode_test(ssid=ssid_name, identity=identity,
                                                                    ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.fiveg
    @allure.story('wpa_wpa2_enterprise_mixed 5 GHZ Band')
    @allure.title("BRIDGE Mode Toggle Airplane Test with wpa_wpa2_enterprise_mixed encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-11102", name="JIRA LINK")
    def test_bridge_wpa_wpa2_enterprise_mixed_5g_toggle_airplane(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration, radius_info):
        profile_data = setup_params_enterprise_two_br["ssid_modes"]["wpa_wpa2_enterprise_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        # security_key = profile_data["#security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info["user"]
        passes, result = get_test_library.enterprise_toggle_airplane_mode_test(ssid=ssid_name, identity=identity,
                                                         ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.twog
    @allure.story('wpa3_enterprise_mixed 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Toggle Airplane Test with wpa3_enterprise_mixed encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-11102", name="JIRA LINK")
    def test_bridge_wpa3_enterprise_mixed_2g_toggle_airplane(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration, radius_info):
        profile_data = setup_params_enterprise_two_br["ssid_modes"]["wpa3_enterprise_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        # security_key = profile_data["#security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info["user"]
        passes, result = get_test_library.enterprise_toggle_airplane_mode_test(ssid=ssid_name, identity=identity,
                                                         ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.fiveg
    @allure.story('wpa3_enterprise_mixed 5 GHZ Band')
    @allure.title("BRIDGE Mode Toggle Airplane Test with wpa3_enterprise_mixed encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-11102", name="JIRA LINK")
    def test_bridge_wpa3_enterprise_mixed_5g_toggle_airplane(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration, radius_info):
        profile_data = setup_params_enterprise_two_br["ssid_modes"]["wpa3_enterprise_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        # security_key = profile_data["#security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info["user"]
        passes, result = get_test_library.enterprise_toggle_airplane_mode_test(ssid=ssid_name, identity=identity,
                                                         ttls_passwd=ttls_passwd)
        allure.attach(name="Test result", body=str(result))

        assert passes == "PASS", result