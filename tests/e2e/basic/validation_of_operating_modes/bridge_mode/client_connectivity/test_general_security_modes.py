"""

    Client Connectivity and tcp-udp Traffic Test: BRIDGE Mode
    pytest -m "client_connectivity_tests and nat and general"

"""
import logging

import allure
import pytest

pytestmark = [pytest.mark.client_connectivity_tests, pytest.mark.bridge, pytest.mark.general]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
                 {"ssid_name": "ssid_open_5g_br", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa": [{"ssid_name": "ssid_wpa_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g_br", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "ssid_wpa2_5g_br", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@allure.parent_suite("Client Connectivity Tests")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="General security mode Client Connectivity")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestBridgeModeConnectivitySuiteA(object):
    """
        Bridge Client Connectivity (open. wpa. wpa2_personal) (twog, fiveg)
        pytest -m "client_connectivity_tests and bridge and general"
    """

    @pytest.mark.open
    @pytest.mark.twog
    @allure.story('OPEN 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with open encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2809", name="JIRA LINK")
    def test_bridge_open_2g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                                get_test_device_logs, num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connectivity Test with open encryption 2.4 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and open and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=1)

        assert passes == "PASS", result

    @pytest.mark.open
    @pytest.mark.fiveg
    @allure.story('OPEN 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with open encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2801", name="JIRA LINK")
    def test_bridge_open_5g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                                get_test_device_logs, num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connectivity Test with open encryption 5 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and open and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=1)

        assert passes == "PASS", result

    #

    @pytest.mark.wpa
    @pytest.mark.twog
    @allure.story('wpa 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2801", name="JIRA LINK")
    def test_bridge_wpa_2g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                               num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connectivity Test with wpa encryption 2.4 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations)

        assert passes == "PASS", result

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @allure.story('wpa 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa encryption 5 GHz Band")
    def test_bridge_wpa_5g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connectivity Test with wpa encryption 5 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations)

        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa2_personal encryption 2.4 GHz Band")
    def test_bridge_wpa2_personal_2g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connectivity Test with wpa2_personal encryption 2.4 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations)

        assert passes == "PASS", result

    #

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa2_personal encryption 5 GHz Band")
    def test_bridge_wpa2_personal_5g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connectivity Test with wpa2_personal encryption 5 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations)

        assert passes == "PASS", result


setup_params_general_two_br = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_5g_br", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_6g_br", "appliedRadios": ["6G"], "security_key": "something"}],
        "wpa3_personal_mixed": [
            {"ssid_name": "ssid_wpa3_p_m_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_m_5g_br", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g_br", "appliedRadios": ["5G"], "security_key": "something"}]
    },
    "rf": {},
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@allure.parent_suite("Client Connectivity Tests")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="General security mode Client Connectivity")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_two_br],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestBridgeModeConnectivitySuiteTwo(object):
    """ Client Connectivity SuiteA
        pytest -m "client_connectivity_tests and bridge and suiteB"
    """

    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @allure.story('wpa3_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa3_personal encryption 2.4 GHz Band")
    def test_bridge_wpa3_personal_2g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connectivity Test with wpa3_personal encryption 2.4 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa3_personal and twog"
        """
        logging.critical("shivam_debug" + str(setup_params_general_two_br))
        profile_data = setup_params_general_two_br["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @allure.story('wpa3_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa3_personal encryption 5 GHz Band")
    def test_bridge_wpa3_personal_5g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connectivity Test with wpa3_personal encryption 5 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa3_personal and fiveg"
        """
        logging.critical("shivam_debug" + str(setup_params_general_two_br))
        profile_data = setup_params_general_two_br["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal
    @pytest.mark.sixg
    @allure.story('wpa3_personal 6 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa3_personal encryption 6 GHz Band")
    def test_bridge_wpa3_personal_6g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connectivity Test with wpa3_personal encryption 6 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa3_personal and sixg"
        """
        logging.critical("shivam_debug" + str(setup_params_general_two_br))
        profile_data = setup_params_general_two_br["ssid_modes"]["wpa3_personal"][2]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        band = "sixg"
        mode = "BRIDGE"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa3_personal_mixed 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa3_personal_mixed encryption 2.4 GHz Band")
    def test_bridge_wpa3_personal_mixed_2g_client_connectivity(self, get_test_library,
                                                               get_dut_logs_per_test_case, get_test_device_logs,
                                                               num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connectivity Test with wpa3_personal_mixed encryption 2.4 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa3_personal_mixed and twog"
        """
        profile_data = setup_params_general_two_br["ssid_modes"]["wpa3_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.fiveg
    @allure.story('wpa3_personal_mixed 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa3_personal_mixed encryption 5 GHz Band")
    def test_bridge_wpa3_personal_mixed_5g_client_connectivity(self, get_test_library,
                                                               get_dut_logs_per_test_case, get_test_device_logs,
                                                               num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connectivity Test with wpa3_personal_mixed encryption 5 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa3_personal_mixed and fiveg"
        """
        profile_data = setup_params_general_two_br["ssid_modes"]["wpa3_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa wpa2 personal mixed 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa3_personal_mixed encryption 5 GHz Band")
    def test_bridge_wpa_wpa2_personal_mixed_2g_client_connectivity(self, get_test_library,
                                                                   get_dut_logs_per_test_case, get_test_device_logs,
                                                                   num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connectivity Test with wpa_wpa2_personal_mixed encryption 2.4 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa_wpa2_personal_mixed and twog"
        """
        profile_data = setup_params_general_two_br["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   extra_securities=extra_secu,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.fiveg
    @allure.story('wpa wpa2 personal mixed 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa3_personal_mixed encryption 5 GHz Band")
    def test_bridge_wpa_wpa2_personal_mixed_5g_client_connectivity(self, get_test_library,
                                                                   get_dut_logs_per_test_case, get_test_device_logs,
                                                                   num_stations, setup_configuration):
        """
            BRIDGE Mode Client Connectivity Test with wpa_wpa2_personal_mixed encryption 5 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa_wpa2_personal_mixed and fiveg"
        """
        profile_data = setup_params_general_two_br["ssid_modes"]["wpa_wpa2_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   extra_securities=extra_secu,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations)

        assert passes == "PASS", result
