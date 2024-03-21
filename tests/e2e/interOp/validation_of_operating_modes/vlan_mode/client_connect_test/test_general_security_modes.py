"""

    Client Connect and tcp-udp Traffic Test: VLAN Mode
    pytest -m "client_connect_tests and vlan and general"

"""
import logging
import random
import string
import time

import allure
import pytest

pytestmark = [pytest.mark.client_connect_tests, pytest.mark.vlan, pytest.mark.general]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
                 {"ssid_name": "ssid_open_5g_vlan", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],
        "wpa": [{"ssid_name": "ssid_wpa_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
                {"ssid_name": "ssid_wpa_5g_vlan", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa2_5g_vlan", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}]},
    "rf": {},
    "radius": False
}
for sec_modes in setup_params_general['ssid_modes'].keys():
    for i in range(len(setup_params_general['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                              string.digits, k=N))) + str(int(time.time_ns()) % 10000)
        setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] = \
            setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] + "_" + rand_string


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@allure.parent_suite("Client Connect Tests : InterOp")
@allure.suite(suite_name="VLAN Mode")
@allure.sub_suite(sub_suite_name="General security mode Client Connect")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestVLANModeConnectSuiteA(object):
    """
        VLAN Client Connect(open. wpa. wpa2_personal) (twog, fiveg)
        pytest -m "client_connect and vlan and general "
    """

    @pytest.mark.open
    @pytest.mark.twog
    @allure.story('OPEN 2.4 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with open encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4606", name="JIRA LINK")
    def test_vlan_open_2g_client_connect(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                              get_test_device_logs,
                                              setup_configuration):
        """
            VLAN Mode Client Connect Test with open encryption 2.4 GHz Band
            pytest -m "client_connect_tests and vlan and general and open and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        passes, result = get_test_library.client_connect(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.open
    @pytest.mark.fiveg
    @allure.story('OPEN 5 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with open encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4607", name="JIRA LINK")
    def test_vlan_open_5g_client_connect(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                              get_test_device_logs,
                                              setup_configuration):
        """
            VLAN Mode Client Connect Test with open encryption 5 GHz Band
            pytest -m "client_connect_tests and vlan and general and open and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        passes, result = get_test_library.client_connect(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result


    @pytest.mark.wpa
    @pytest.mark.twog
    @allure.story('wpa 2.4 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with wpa encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4609", name="JIRA LINK")
    def test_vlan_wpa_2g_client_connect(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                             get_test_device_logs,
                                             setup_configuration):
        """
            VLAN Mode Client Connect Test with wpa encryption 2.4 GHz Band
            pytest -m "client_connect_tests and vlan and general and wpa and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        passes, result = get_test_library.client_connect(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @allure.story('wpa 5 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with wpa encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4611", name="JIRA LINK")
    def test_vlan_wpa_5g_client_connect(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                             get_test_device_logs,
                                             setup_configuration):
        """
            VLAN Mode Client Connect Test with wpa encryption 5 GHz Band
            pytest -m "client_connect_tests and vlan and general and wpa and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        passes, result = get_test_library.client_connect(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with wpa2_personal encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4612", name="JIRA LINK")
    def test_vlan_wpa2_personal_2g_client_connect(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                                       get_test_device_logs,
                                                       setup_configuration):
        """
            VLAN Mode Client Connect Test with wpa2_personal encryption 2.4 GHz Band
            pytest -m "client_connect_tests and vlan and general and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        passes, result = get_test_library.client_connect(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result


    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with wpa2_personal encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4613", name="JIRA LINK")
    def test_vlan_wpa2_personal_5g_client_connect(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                                       get_test_device_logs,
                                                       setup_configuration):
        """
            VLAN Mode Client Connect Test with wpa2_personal encryption 5 GHz Band
            pytest -m "client_connect_tests and vlan and general and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        passes, result = get_test_library.client_connect(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result


setup_params_general_two_vlan = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa3_p_5g_vlan", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],
        "wpa3_personal_mixed": [
            {"ssid_name": "ssid_wpa3_p_m_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa3_p_m_5g_vlan", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],
        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g_vlan", "appliedRadios": ["2G"], "security_key": "something",
             "vlan": 100},
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g_vlan", "appliedRadios": ["5G"], "security_key": "something",
             "vlan": 100}]
    },
    "rf": {},
    "radius": False
}
for sec_modes in setup_params_general_two_vlan['ssid_modes'].keys():
    for i in range(len(setup_params_general_two_vlan['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                              string.digits, k=N))) + str(int(time.time_ns()) % 10000)
        setup_params_general_two_vlan['ssid_modes'][sec_modes][i]['ssid_name'] = \
            setup_params_general_two_vlan['ssid_modes'][sec_modes][i]['ssid_name'] + "_" + rand_string

@allure.feature("VLAN MODE CLIENT CONNECT")
@allure.parent_suite("Client Connect Tests : InterOp")
@allure.suite(suite_name="VLAN Mode")
@allure.sub_suite(sub_suite_name="General security mode Client Connect")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_two_vlan],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestVLANModeConnectSuiteTwo(object):
    """"
        VLAN Client Connect (wpa3_personal. wpa3_personal_mixed. wpa_wpa2_personal_mixed) (twog, fiveg)
        pytest -m "client_connect_tests and vlan and general"
    """

    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @allure.story('wpa3_personal 2.4 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with wpa3_personal encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4616", name="JIRA LINK")
    def test_vlan_wpa3_personal_2g_client_connect(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                                       get_test_device_logs,
                                                       setup_configuration):
        """
            VLAN Mode Client Connect Test with wpa3_personal encryption 2.4 GHz Band
            pytest -m "client_connect_tests and vlan and general and wpa3_personal and twog"
        """
        profile_data = setup_params_general_two_vlan["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        passes, result = get_test_library.client_connect(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @allure.story('wpa3_personal 5 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with wpa3_personal encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4617", name="JIRA LINK")
    def test_vlan_wpa3_personal_5g_client_connect(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                                       get_test_device_logs,
                                                       setup_configuration):
        """
            VLAN Mode Client Connect Test with wpa3_personal encryption 5 GHz Band
            pytest -m "client_connect_tests and vlan and general and wpa3_personal and fiveg"
        """
        profile_data = setup_params_general_two_vlan["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        passes, result = get_test_library.client_connect(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result


    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa3_personal_mixed 2.4 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with wpa3_personal_mixed encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4621", name="JIRA LINK")
    def test_vlan_wpa3_personal_mixed_2g_client_connect(self, get_test_library,
                                                             num_stations, get_dut_logs_per_test_case,
                                                             get_test_device_logs,
                                                             setup_configuration):
        """
            VLAN Mode Client Connect Test with wpa3_personal_mixed encryption 2.4 GHz Band
            pytest -m "client_connect_tests and vlan and general and wpa3_personal_mixed and twog"
        """
        profile_data = setup_params_general_two_vlan["ssid_modes"]["wpa3_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        passes, result = get_test_library.client_connect(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.fiveg
    @allure.story('wpa3_personal_mixed 5 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with wpa3_personal_mixed encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4623", name="JIRA LINK")
    def test_vlan_wpa3_personal_mixed_5g_client_connect(self, get_test_library,
                                                             num_stations, get_dut_logs_per_test_case,
                                                             get_test_device_logs,
                                                             setup_configuration):
        """
            VLAN Mode Client Connect Test with wpa3_personal_mixed encryption 5 GHz Band
            pytest -m "client_connect_tests and vlan and general and wpa3_personal_mixed and fiveg"
        """
        profile_data = setup_params_general_two_vlan["ssid_modes"]["wpa3_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        passes, result = get_test_library.client_connect(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa wpa2 personal mixed 2.4 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with wpa_wpa2_personal_mixed encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4624", name="JIRA LINK")
    def test_vlan_wpa_wpa2_personal_mixed_2g_client_connect(self, get_test_library,
                                                                 num_stations, get_dut_logs_per_test_case,
                                                                 get_test_device_logs,
                                                                 setup_configuration):
        """
            VLAN Mode Client Connect Test with wpa_wpa2_personal_mixed encryption 2.4 GHz Band
            pytest -m "client_connect_tests and vlan and general and wpa_wpa2_personal_mixed and twog"
        """
        profile_data = setup_params_general_two_vlan["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        passes, result = get_test_library.client_connect(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   extra_securities=extra_secu,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.fiveg
    @allure.story('wpa wpa2 personal mixed 5 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with wpa_wpa2_personal_mixed encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4625", name="JIRA LINK")
    def test_vlan_wpa_wpa2_personal_mixed_5g_client_connect(self, get_test_library,
                                                                 num_stations, get_dut_logs_per_test_case,
                                                                 get_test_device_logs,
                                                                 setup_configuration):
        """
            VLAN Mode Client Connect Test with wpa_wpa2_personal_mixed encryption 5 GHz Band
            pytest -m "client_connect_tests and vlan and general and wpa_wpa2_personal_mixed and fiveg"
        """
        profile_data = setup_params_general_two_vlan["ssid_modes"]["wpa_wpa2_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        passes, result = get_test_library.client_connect(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   extra_securities=extra_secu,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result