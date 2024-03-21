"""

    Client Connect : Nat Mode
    pytest -m "client_connect_tests and nat and general"

"""
import logging
import random
import string
import time

import allure
import pytest

pytestmark = [pytest.mark.client_connect_tests, pytest.mark.nat, pytest.mark.general]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g_nat", "appliedRadios": ["2G"], "security_key": "something"},
                 {"ssid_name": "ssid_open_5g_nat", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa": [{"ssid_name": "ssid_wpa_2g_nat", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g_nat", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g_nat", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g_nat", "appliedRadios": ["5G"], "security_key": "something"}]},
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

@allure.feature("NAT MODE CLIENT CONNECT")
@allure.parent_suite("Client Connect Tests : InterOp")
@allure.suite(suite_name="NAT Mode")
@allure.sub_suite(sub_suite_name="General security mode Client Connect")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestNatModeConnectSuiteA(object):
    """
        Nat Client Connect (open. wpa. wpa2_personal) (twog, fiveg)
        pytest -m "client_connect_tests and nat and general"
    """

    @pytest.mark.open
    @pytest.mark.twog
    @allure.story('OPEN 2.4 GHZ Band')
    @allure.title("Nat Mode Client Connect Test with open encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4503", name="JIRA LINK")
    def test_nat_open_2g_client_connect(self, get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        """
            NAT Mode Client Connect Test with open encryption 2.4 GHz Band
            pytest -m "client_connect_tests and nat and general and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_2g_br", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "NAT"
        band = "twog"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    @pytest.mark.open
    @pytest.mark.fiveg
    @allure.story('OPEN 5 GHZ Band')
    @allure.title("NAT Mode Client Connect Test with open encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4504", name="JIRA LINK")
    def test_nat_open_5g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                                get_test_device_logs, num_stations, setup_configuration):
        """
            NAT Mode Client Connect Test with open encryption 5 GHz Band
            pytest -m "client_connect_tests and nat and general and open and fiveg"
        """
        profile_data = {"ssid_name": "ssid_open_5g_br", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "NAT"
        band = "fiveg"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result


    @pytest.mark.wpa
    @pytest.mark.twog
    @allure.story('wpa 2.4 GHZ Band')
    @allure.title("NAT Mode Client Connect Test with wpa encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4505", name="JIRA LINK")
    def test_nat_wpa_2g_client_connect(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                               num_stations, setup_configuration):
        """
            NAT Mode Client Connect Test with wpa encryption 2.4 GHz Band
            pytest -m "client_connectivity_tests and nat and general and wpa and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa_2g_br", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "NAT"
        band = "twog"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @allure.story('wpa 5 GHZ Band')
    @allure.title("NAT Mode Client Connect Test with wpa encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4507", name="JIRA LINK")
    def test_nat_wpa_5g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration):
        """
            NAT Mode Client Connect Test with wpa encryption 5 GHz Band
            pytest -m "client_connect_tests and nat and general and wpa and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa_5g_br", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "NAT"
        band = "fiveg"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("NAT Mode Client Connect Test with wpa2_personal encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4509", name="JIRA LINK")
    def test_nat_wpa2_personal_2g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration):
        """
            NAT Mode Client Connect Test with wpa2_personal encryption 2.4 GHz Band
            pytest -m "client_connect_tests and nat and general and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_br", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "twog"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    #

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("NAT Mode Client Connect Test with wpa2_personal encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4510", name="JIRA LINK")
    def test_bridge_wpa2_personal_5g_client_connect(self, get_test_device_logs, get_dut_logs_per_test_case,
                                                    num_stations, setup_configuration, get_test_library):
        """
            NAT Mode Client Connect Test with wpa2_personal encryption 5 GHz Band
            pytest -m "client_connect_tests and nat and general and wpa2_personal and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_br", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result


setup_params_general_two_nat = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g_nat", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_5g_nat", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa3_personal_mixed": [
            {"ssid_name": "ssid_wpa3_p_m_2g_nat", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_m_5g_nat", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g_nat", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g_nat", "appliedRadios": ["5G"], "security_key": "something"}]
    },
    "rf": {},
    "radius": False
}
for sec_modes in setup_params_general_two_nat['ssid_modes'].keys():
    for i in range(len(setup_params_general_two_nat['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                              string.digits, k=N))) + str(int(time.time_ns()) % 10000)
        setup_params_general_two_nat['ssid_modes'][sec_modes][i]['ssid_name'] = \
            setup_params_general_two_nat['ssid_modes'][sec_modes][i]['ssid_name'] + "_" + rand_string

@allure.feature("NAT MODE CLIENT CONNECT")
@allure.parent_suite("Client Connect Tests : InterOp")
@allure.suite(suite_name="NAT Mode")
@allure.sub_suite(sub_suite_name="General security mode Client Connect")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_two_nat],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestNatModeConnectSuiteTwo(object):
    """ Client Connect SuiteA
        pytest -m "client_connect_tests and nat and suiteB"
    """

    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @allure.story('wpa3_personal 2.4 GHZ Band')
    @allure.title("NAT Mode Client Connect Test with wpa3_personal encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4515", name="JIRA LINK")
    def test_nat_wpa3_personal_2g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration):
        """
            NAT Mode Client Connect Test with wpa3_personal encryption 2.4 GHz Band
            pytest -m "client_connect_tests and nat and general and wpa3_personal and twog"
        """
        profile_data = setup_params_general_two_nat["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "NAT"
        band = "twog"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @allure.story('wpa3_personal 5 GHZ Band')
    @allure.title("NAT Mode Client Connect Test with wpa3_personal encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4516", name="JIRA LINK")
    def test_nat_wpa3_personal_5g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration):
        """
            NAT Mode Client Connect Test with wpa3_personal encryption 5 GHz Band
            pytest -m "client_connect_tests and nat and general and wpa3_personal and fiveg"
        """
        profile_data = setup_params_general_two_nat["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "NAT"
        band = "fiveg"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result


    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa3_personal_mixed 2.4 GHZ Band')
    @allure.title("NAT Mode Client Connect Test with wpa3_personal_mixed encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4519", name="JIRA LINK")
    def test_nat_wpa3_personal_mixed_2g_client_connect(self, get_test_library,
                                                               get_dut_logs_per_test_case, get_test_device_logs,
                                                               num_stations, setup_configuration):
        """
            NAT Mode Client Connect Test with wpa3_personal_mixed encryption 2.4 GHz Band
            pytest -m "client_connect_tests and nat and general and wpa3_personal_mixed and twog"
        """
        profile_data = setup_params_general_two_nat["ssid_modes"]["wpa3_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "NAT"
        band = "twog"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.fiveg
    @allure.story('wpa3_personal_mixed 5 GHZ Band')
    @allure.title("NAT Mode Client Connect Test with wpa3_personal_mixed encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4521", name="JIRA LINK")
    def test_nat_wpa3_personal_mixed_5g_client_connect(self, get_test_library,
                                                               get_dut_logs_per_test_case, get_test_device_logs,
                                                               num_stations, setup_configuration):
        """
            NAT Mode Client Connect Test with wpa3_personal_mixed encryption 5 GHz Band
            pytest -m "client_connect_tests and nat and general and wpa3_personal_mixed and fiveg"
        """
        profile_data = setup_params_general_two_nat["ssid_modes"]["wpa3_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "NAT"
        band = "fiveg"

        passes, result = get_test_library.get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa wpa2 personal mixed 2.4 GHZ Band')
    @allure.title("NAT Mode Client Connect Test with wpa_wpa2_personal_mixed encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4523", name="JIRA LINK")
    def test_nat_wpa_wpa2_personal_mixed_2g_client_connect(self, get_test_library,
                                                                   get_dut_logs_per_test_case, get_test_device_logs,
                                                                   num_stations, setup_configuration):
        """
            NAT Mode Client Connect Test with wpa_wpa2_personal_mixed encryption 2.4 GHz Band
            pytest -m "client_connect_tests and nat and general and wpa_wpa2_personal_mixed and twog"
        """
        profile_data = setup_params_general_two_nat["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "NAT"
        band = "twog"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.fiveg
    @allure.story('wpa wpa2 personal mixed 5 GHZ Band')
    @allure.title("NAT Mode Client ConnectTest with wpa_wpa2_personal_mixed encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4524", name="JIRA LINK")
    def test_nat_wpa_wpa2_personal_mixed_5g_client_connect(self, get_test_library,
                                                                   get_dut_logs_per_test_case, get_test_device_logs,
                                                                   num_stations, setup_configuration):
        """
            NAT Mode Client Connect Test with wpa_wpa2_personal_mixed encryption 5 GHz Band
            pytest -m "client_connect_tests and nat and general and wpa_wpa2_personal_mixed and fiveg"
        """
        profile_data = setup_params_general_two_nat["ssid_modes"]["wpa_wpa2_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "NAT"
        band = "fiveg"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result
