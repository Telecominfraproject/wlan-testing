"""

    Client Connect : BRIDGE Mode
    pytest -m "client_connect_tests and nat and general"

"""
import logging
import random
import string
import time

import allure
import pytest

pytestmark = [pytest.mark.client_connect_tests, pytest.mark.bridge, pytest.mark.general, pytest.mark.ow_sanity_interop]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "open_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
                 {"ssid_name": "open_5g_br", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa": [{"ssid_name": "wpa_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "wpa_5g_br", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa2_personal": [{"ssid_name": "wpa2_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "wpa2_5g_br", "appliedRadios": ["5G"], "security_key": "something"}]},
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

@allure.feature("BRIDGE MODE CLIENT CONNECT")
@allure.parent_suite("Client Connect Tests")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="General security mode Client Connect")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestBridgeModeConnectSuiteA(object):
    """
        Bridge Client Connect (open. wpa. wpa2_personal) (twog, fiveg)
        pytest -m "client_connect_tests and bridge and general"
    """

    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.general_securtiy
    @allure.story('OPEN 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connect Test with open encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4565", name="JIRA LINK")
    def test_bridge_open_2g_client_connect(self, get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library):
        """
            BRIDGE Mode Client Connect Test with open encryption 2.4 GHz Band
            pytest -m "client_connect_tests and bridge and general and open and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    @pytest.mark.open
    @pytest.mark.fiveg
    @pytest.mark.general_securtiy
    @allure.story('OPEN 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connect Test with open encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4566", name="JIRA LINK")
    def test_bridge_open_5g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                                get_test_device_logs, num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connect Test with open encryption 5 GHz Band
            pytest -m "client_connect_tests and bridge and general and open and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result


    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.general_securtiy
    @allure.story('wpa 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connect Test with wpa encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4567", name="JIRA LINK")
    def test_bridge_wpa_2g_client_connect(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                               num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connect Test with wpa encryption 2.4 GHz Band
            pytest -m "client_connect_tests and bridge and general and wpa and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @pytest.mark.general_securtiy
    @allure.story('wpa 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connect Test with wpa encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4568", name="JIRA LINK")
    def test_bridge_wpa_5g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connect Test with wpa encryption 5 GHz Band
            pytest -m "client_connect_tests and bridge and general and wpa and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.general_securtiy
    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connect Test with wpa2_personal encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4569", name="JIRA LINK")
    def test_bridge_wpa2_personal_2g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connect Test with wpa2_personal encryption 2.4 GHz Band
            pytest -m "client_connect_tests and bridge and general and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    #

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.general_securtiy
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connect Test with wpa2_personal encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4570", name="JIRA LINK")
    def test_bridge_wpa2_personal_5g_client_connect(self, get_test_device_logs, get_dut_logs_per_test_case,
                                                    num_stations, setup_configuration, get_test_library):
        """
            BRIDGE Mode Client Connect Test with wpa2_personal encryption 5 GHz Band
            pytest -m "client_connect_tests and bridge and general and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result


setup_params_general_two_br = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "wpa3_p_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "wpa3_p_5g_br", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa3_personal_mixed": [
            {"ssid_name": "wpa3_p_m_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "wpa3_p_m_5g_br", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "wpa_wpa2_p_m_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "wpa_wpa2_p_m_5g_br", "appliedRadios": ["5G"], "security_key": "something"}]
    },
    "rf": {},
    "radius": False
}
for sec_modes in setup_params_general_two_br['ssid_modes'].keys():
    for i in range(len(setup_params_general_two_br['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                              string.digits, k=N))) + str(int(time.time_ns()) % 10000)
        setup_params_general_two_br['ssid_modes'][sec_modes][i]['ssid_name'] = \
            setup_params_general_two_br['ssid_modes'][sec_modes][i]['ssid_name'] + "_" + rand_string

@allure.feature("BRIDGE MODE CLIENT CONNECT")
@allure.parent_suite("Client Connect Tests")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="General security mode Client Connect")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_two_br],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestBridgeModeConnectSuiteTwo(object):
    """ Client Connect SuiteA
        pytest -m "client_connect_tests and bridge and suiteB"
    """

    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @allure.story('wpa3_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connect Test with wpa3_personal encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4571", name="JIRA LINK")
    def test_bridge_wpa3_personal_2g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connect Test with wpa3_personal encryption 2.4 GHz Band
            pytest -m "client_connect_tests and bridge and general and wpa3_personal and twog"
        """
        profile_data = setup_params_general_two_br["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @allure.story('wpa3_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connect Test with wpa3_personal encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4572", name="JIRA LINK")
    def test_bridge_wpa3_personal_5g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connect Test with wpa3_personal encryption 5 GHz Band
            pytest -m "client_connect_tests and bridge and general and wpa3_personal and fiveg"
        """
        profile_data = setup_params_general_two_br["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result


    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa3_personal_mixed 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connect Test with wpa3_personal_mixed encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4573", name="JIRA LINK")
    def test_bridge_wpa3_personal_mixed_2g_client_connect(self, get_test_library,
                                                               get_dut_logs_per_test_case, get_test_device_logs,
                                                               num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connect Test with wpa3_personal_mixed encryption 2.4 GHz Band
            pytest -m "client_connect_tests and bridge and general and wpa3_personal_mixed and twog"
        """
        profile_data = setup_params_general_two_br["ssid_modes"]["wpa3_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.fiveg
    @allure.story('wpa3_personal_mixed 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connect Test with wpa3_personal_mixed encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4574", name="JIRA LINK")
    def test_bridge_wpa3_personal_mixed_5g_client_connect(self, get_test_library,
                                                               get_dut_logs_per_test_case, get_test_device_logs,
                                                               num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connect Test with wpa3_personal_mixed encryption 5 GHz Band
            pytest -m "client_connect_tests and bridge and general and wpa3_personal_mixed and fiveg"
        """
        profile_data = setup_params_general_two_br["ssid_modes"]["wpa3_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa wpa2 personal mixed 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connect Test with wpa_wpa2_personal_mixed encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4575", name="JIRA LINK")
    def test_bridge_wpa_wpa2_personal_mixed_2g_client_connect(self, get_test_library,
                                                                   get_dut_logs_per_test_case, get_test_device_logs,
                                                                   num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connect Test with wpa_wpa2_personal_mixed encryption 2.4 GHz Band
            pytest -m "client_connect_tests and bridge and general and wpa_wpa2_personal_mixed and twog"
        """
        profile_data = setup_params_general_two_br["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.fiveg
    @allure.story('wpa wpa2 personal mixed 5 GHZ Band')
    @allure.title("BRIDGE Mode Client ConnectTest with wpa_wpa2_personal_mixed encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4576", name="JIRA LINK")
    def test_bridge_wpa_wpa2_personal_mixed_5g_client_connect(self, get_test_library,
                                                                   get_dut_logs_per_test_case, get_test_device_logs,
                                                                   num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connect Test with wpa_wpa2_personal_mixed encryption 5 GHz Band
            pytest -m "client_connect_tests and bridge and general and wpa_wpa2_personal_mixed and fiveg"
        """
        profile_data = setup_params_general_two_br["ssid_modes"]["wpa_wpa2_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connect(ssid=ssid_name, passkey=security_key)

        assert passes == "PASS", result