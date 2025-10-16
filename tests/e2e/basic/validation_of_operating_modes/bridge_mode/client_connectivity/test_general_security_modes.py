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


@allure.feature("Client Connectivity")
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
                                                get_test_device_logs, num_stations, check_connectivity,
                                                setup_configuration, client_type):
        """
            BRIDGE Mode Client Connectivity Test with open encryption 2.4 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_2g_br", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, client_type=client_type)

        assert passes == "PASS", result

    @pytest.mark.open
    @pytest.mark.fiveg
    @allure.story('OPEN 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with open encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2801", name="JIRA LINK")
    def test_bridge_open_5g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                                get_test_device_logs, num_stations, check_connectivity,
                                                setup_configuration, client_type):
        """
            BRIDGE Mode Client Connectivity Test with open encryption 5 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and open and fiveg"
        """
        profile_data = {"ssid_name": "ssid_open_5g_br", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, client_type=client_type)

        assert passes == "PASS", result

    #

    @pytest.mark.wpa
    @pytest.mark.twog
    @allure.story('wpa 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2801", name="JIRA LINK")
    def test_bridge_wpa_2g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                               num_stations, check_connectivity, setup_configuration, client_type):
        """
            BRIDGE Mode Client Connectivity Test with wpa encryption 2.4 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa_2g_br", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, client_type=client_type)

        assert passes == "PASS", result

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @allure.story('wpa 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa encryption 5 GHz Band")
    def test_bridge_wpa_5g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, check_connectivity,
                                               setup_configuration, client_type):
        """
            BRIDGE Mode Client Connectivity Test with wpa encryption 5 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa_5g_br", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, client_type=client_type)

        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa2_personal encryption 2.4 GHz Band")
    def test_bridge_wpa2_personal_2g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, check_connectivity,
                                                         setup_configuration, client_type):
        """
            BRIDGE Mode Client Connectivity Test with wpa2_personal encryption 2.4 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_br", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, client_type=client_type)

        assert passes == "PASS", result

    #

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa2_personal encryption 5 GHz Band")
    def test_bridge_wpa2_personal_5g_client_connectivity(self, get_test_library, get_test_device_logs,
                                                         get_dut_logs_per_test_case,
                                                         num_stations, check_connectivity, setup_configuration,
                                                         client_type):
        """
            BRIDGE Mode Client Connectivity Test with wpa2_personal encryption 5 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa2_personal and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_br", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, client_type=client_type)

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


@allure.feature("Client Connectivity")
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
                                                         get_test_device_logs, num_stations, check_connectivity,
                                                         setup_configuration, client_type):
        """
            BRIDGE Mode Client Connectivity Test with wpa3_personal encryption 2.4 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa3_p_2g_br", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, client_type=client_type)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @allure.story('wpa3_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa3_personal encryption 5 GHz Band")
    def test_bridge_wpa3_personal_5g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, check_connectivity,
                                                         setup_configuration, client_type):
        """
            BRIDGE Mode Client Connectivity Test with wpa3_personal encryption 5 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa3_personal and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa3_p_5g_br", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, client_type=client_type)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal
    @pytest.mark.sixg
    @allure.story('wpa3_personal 6 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa3_personal encryption 6 GHz Band")
    def test_bridge_wpa3_personal_6g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, check_connectivity,
                                                         setup_configuration, client_type):
        """
            BRIDGE Mode Client Connectivity Test with wpa3_personal encryption 6 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa3_personal and sixg"
        """
        profile_data = {"ssid_name": "ssid_wpa3_p_6g_br", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        band = "sixg"
        mode = "BRIDGE"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, client_type=client_type)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa3_personal_mixed 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa3_personal_mixed encryption 2.4 GHz Band")
    def test_bridge_wpa3_personal_mixed_2g_client_connectivity(self, get_test_library,
                                                               get_dut_logs_per_test_case, get_test_device_logs,
                                                               num_stations, check_connectivity, setup_configuration,
                                                               client_type):
        """
            BRIDGE Mode Client Connectivity Test with wpa3_personal_mixed encryption 2.4 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa3_personal_mixed and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa3_p_m_2g_br", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, client_type=client_type)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.fiveg
    @allure.story('wpa3_personal_mixed 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa3_personal_mixed encryption 5 GHz Band")
    def test_bridge_wpa3_personal_mixed_5g_client_connectivity(self, get_test_library,
                                                               get_dut_logs_per_test_case, get_test_device_logs,
                                                               num_stations, check_connectivity, setup_configuration,
                                                               client_type):
        """
            BRIDGE Mode Client Connectivity Test with wpa3_personal_mixed encryption 5 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa3_personal_mixed and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa3_p_m_5g_br", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, client_type=client_type)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa wpa2 personal mixed 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa_wpa2_personal_mixed encryption 2.4 GHz Band")
    def test_bridge_wpa_wpa2_personal_mixed_2g_client_connectivity(self, get_test_library,
                                                                   get_dut_logs_per_test_case, get_test_device_logs,
                                                                   num_stations, check_connectivity, setup_configuration,
                                                                   client_type):
        """
            BRIDGE Mode Client Connectivity Test with wpa_wpa2_personal_mixed encryption 2.4 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa_wpa2_personal_mixed and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa_wpa2_p_m_2g_br", "appliedRadios": ["2G"], "security_key": "something"}
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
                                                                   num_sta=num_stations, client_type=client_type)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.fiveg
    @allure.story('wpa wpa2 personal mixed 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with wpa_wpa2_personal_mixed encryption 5 GHz Band")
    def test_bridge_wpa_wpa2_personal_mixed_5g_client_connectivity(self, get_test_library,
                                                                   get_dut_logs_per_test_case, get_test_device_logs,
                                                                   num_stations, check_connectivity, setup_configuration,
                                                                   client_type):
        """
            BRIDGE Mode Client Connectivity Test with wpa_wpa2_personal_mixed encryption 5 GHz Band
            pytest -m "client_connectivity_tests and bridge and general and wpa_wpa2_personal_mixed and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa_wpa2_p_m_5g_br", "appliedRadios": ["5G"], "security_key": "something"}
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
                                                                   num_sta=num_stations, client_type=client_type)

        assert passes == "PASS", result



setup_params_owe_br = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "owe": [
            {"ssid_name": "ssid_owe_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_owe_5g_br", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid_owe_6g_br", "appliedRadios": ["6G"], "security_key": "something"},

        ]
    },
    "rf": {},
    "radius": False
}

@allure.feature("Client Connectivity")
@allure.parent_suite("Client Connectivity Tests")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="OWE security mode Client Connectivity")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_owe_br],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestBridgeModeConnectivityOWE(object):
    """
        Bridge Client Connectivity (OWE)
        pytest -m "client_connectivity_tests and bridge and owe"
    """

    @pytest.mark.owe
    @pytest.mark.twog
    @allure.story('OWE 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with OWE encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13669", name="WIFI-13669")
    def test_bridge_owe_2g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, check_connectivity,
                                               setup_configuration, client_type):
        """
            BRIDGE Mode Client Connectivity Test with OWE encryption 2.4 GHz Band
            marker:- client_connectivity_tests and bridge and owe and twog
        """
        profile_data = {"ssid_name": "ssid_owe_2g_br", "appliedRadios": ["2G"], "security_key": ""}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "owe"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connectivity_test(
            ssid=ssid_name, security=security,
            dut_data=setup_configuration,
            passkey=security_key, mode=mode, band=band,
            num_sta=num_stations, client_type=client_type, extra_sta_rows=["security"]
        )
        assert passes == "PASS", result

    @pytest.mark.owe
    @pytest.mark.fiveg
    @allure.story('OWE 5 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with OWE encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13669", name="WIFI-13669")
    def test_bridge_owe_5g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, check_connectivity,
                                               setup_configuration, client_type):
        """
            BRIDGE Mode Client Connectivity Test with OWE encryption 5 GHz Band
            marker:- client_connectivity_tests and bridge and owe and fiveg
        """
        profile_data = {"ssid_name": "ssid_owe_5g_br", "appliedRadios": ["5G"], "security_key": ""}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "owe"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connectivity_test(
            ssid=ssid_name, security=security,
            dut_data=setup_configuration,
            passkey=security_key, mode=mode, band=band,
            num_sta=num_stations, client_type=client_type, extra_sta_rows=["security"]
        )
        assert passes == "PASS", result

    @pytest.mark.owe
    @pytest.mark.twog
    @pytest.mark.sixg
    @allure.story('OWE 6 GHZ Band')
    @allure.title("BRIDGE Mode Client Connectivity Test with OWE encryption 6 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13669", name="WIFI-13669")
    def test_bridge_owe_6g_client_connectivity(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, check_connectivity,
                                               setup_configuration, client_type):
        """
            BRIDGE Mode Client Connectivity Test with OWE encryption 6 GHz Band
            marker:- client_connectivity_tests and bridge and owe and sixg
        """
        profile_data = {"ssid_name": "ssid_owe_6g_br", "appliedRadios": ["6G"], "security_key": ""}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "owe"
        mode = "BRIDGE"
        band = "sixg"

        passes, result = get_test_library.client_connectivity_test(
            ssid=ssid_name, security=security,
            dut_data=setup_configuration,
            passkey=security_key, mode=mode, band=band,
            num_sta=num_stations, client_type=client_type, extra_sta_rows=["security"]
        )
        assert passes == "PASS", result



setup_params_owe_transition_br = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "owe_transition": [
            {"ssid_name": "ssid_owe_transition_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_owe_transition_5g_br", "appliedRadios": ["5G"], "security_key": "something"}

        ]
    },
    "rf": {},
    "radius": False
}

@allure.feature("Client Connectivity")
@allure.parent_suite("Client Connectivity Tests")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="OWE-Transition security mode Client Connectivity")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_owe_transition_br],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestBridgeModeConnectivityOWETransition(object):
    """
        Bridge Client Connectivity (OWE-Transition)
        pytest -m "client_connectivity_tests and bridge and owe_transition"
    """

    @pytest.mark.owe_transition
    @pytest.mark.twog
    @pytest.mark.owe_client
    @allure.story('OWE-Transition 2.4 GHZ Band - OWE Client')
    @allure.title("BRIDGE Mode OWE-Transition: OWE client connects to hidden SSID")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13674", name="WIFI-13674")
    def test_bridge_owe_transition_2g_owe_client(self, get_test_library, get_dut_logs_per_test_case,
                                                 get_test_device_logs, num_stations, check_connectivity,
                                                 setup_configuration, client_type):
        """
            BRIDGE Mode OWE-Transition: OWE client connects to SSID in OWE mode
            marker:- client_connectivity_tests and bridge and owe_transition and twog and owe_client
        """
        profile_data = {"ssid_name": "ssid_owe_transition_2g_br", "appliedRadios": ["2G"], "security_key": ""}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "owe"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connectivity_test(
            ssid=ssid_name, security=security,
            dut_data=setup_configuration,
            passkey=security_key, mode=mode, band=band,
            num_sta=num_stations, client_type=client_type, extra_sta_rows=["security"]
        )
        assert passes == "PASS", result

    @pytest.mark.owe_transition
    @pytest.mark.twog
    @pytest.mark.non_owe_client
    @allure.story('OWE-Transition 2.4 GHZ Band - Non-OWE Client')
    @allure.title("BRIDGE Mode OWE-Transition: Non-OWE client connects to SSID in open mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13673", name="WIFI-13673")
    def test_bridge_owe_transition_2g_non_owe_client(self, get_test_library, get_dut_logs_per_test_case,
                                                     get_test_device_logs, num_stations, check_connectivity,
                                                     setup_configuration, client_type):
        """
            BRIDGE Mode OWE-Transition: Non-OWE client connects to SSID in open mode
            marker:- client_connectivity_tests and bridge and owe_transition and twog and non_owe_client
        """
        profile_data = {"ssid_name": "ssid_owe_transition_2g_br", "appliedRadios": ["2G"], "security_key": ""}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "BRIDGE"
        band = "twog"

        passes, result = get_test_library.client_connectivity_test(
            ssid=ssid_name, security=security,
            dut_data=setup_configuration,
            passkey=security_key, mode=mode, band=band,
            num_sta=num_stations, client_type=client_type, extra_sta_rows=["security"]
        )
        assert passes == "PASS", result

    @pytest.mark.owe_transition
    @pytest.mark.fiveg
    @pytest.mark.owe_client
    @allure.story('OWE-Transition 5 GHZ Band - OWE Client')
    @allure.title("BRIDGE Mode OWE-Transition: OWE client connects to hidden SSID")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13674", name="WIFI-13674")
    def test_bridge_owe_transition_5g_owe_client(self, get_test_library, get_dut_logs_per_test_case,
                                                 get_test_device_logs, num_stations, check_connectivity,
                                                 setup_configuration, client_type):
        """
            BRIDGE Mode OWE-Transition: OWE client connects to SSID in OWE mode
            marker:- client_connectivity_tests and bridge and owe_transition and fiveg and owe_client
        """
        profile_data = {"ssid_name": "ssid_owe_transition_5g_br", "appliedRadios": ["5G"], "security_key": ""}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "owe"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connectivity_test(
            ssid=ssid_name, security=security,
            dut_data=setup_configuration,
            passkey=security_key, mode=mode, band=band,
            num_sta=num_stations, client_type=client_type, extra_sta_rows=["security"]
        )
        assert passes == "PASS", result

    @pytest.mark.owe_transition
    @pytest.mark.fiveg
    @pytest.mark.non_owe_client
    @allure.story('OWE-Transition 5 GHZ Band - Non-OWE Client')
    @allure.title("BRIDGE Mode OWE-Transition: Non-OWE client connects to SSID in open mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13673", name="WIFI-13673")
    def test_bridge_owe_transition_5g_non_owe_client(self, get_test_library, get_dut_logs_per_test_case,
                                                     get_test_device_logs, num_stations, check_connectivity,
                                                     setup_configuration, client_type):
        """
            BRIDGE Mode OWE-Transition: Non-OWE client connects to SSID in open mode
            marker:- client_connectivity_tests and bridge and owe_transition and fiveg and non_owe_client
        """
        profile_data = {"ssid_name": "ssid_owe_transition_5g_br", "appliedRadios": ["5G"], "security_key": ""}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "BRIDGE"
        band = "fiveg"

        passes, result = get_test_library.client_connectivity_test(
            ssid=ssid_name, security=security,
            dut_data=setup_configuration,
            passkey=security_key, mode=mode, band=band,
            num_sta=num_stations, client_type=client_type, extra_sta_rows=["security"]
        )
        assert passes == "PASS", result








