"""

    Client Connectivity and tcp-udp Traffic Test: VLAN Mode
    pytest -m "client_connectivity_tests and vlan and general"

"""
import logging

import allure
import pytest

pytestmark = [pytest.mark.client_connectivity_tests, pytest.mark.vlan, pytest.mark.general, pytest.mark.ow_sanity_lf]

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


@allure.feature("Client Connectivity")
@allure.parent_suite("Client Connectivity Tests")
@allure.suite(suite_name="VLAN Mode")
@allure.sub_suite(sub_suite_name="General security mode Client Connectivity")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestVLANModeConnectivitySuiteA(object):
    """
        VLAN Client Connectivity (open. wpa. wpa2_personal) (twog, fiveg)
        pytest -m "client_connectivity and vlan and general "
    """

    @pytest.mark.open
    @pytest.mark.twog
    @allure.story('OPEN 2.4 GHZ Band')
    @allure.title("VLAN Mode Client Connectivity Test with Open Encryption 2.4GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10608", name="WIFI-10608")
    def test_vlan_open_2g_client_connectivity(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                              get_test_device_logs,
                                              check_connectivity, setup_configuration):
        """
            To verify that a client created on 2G radio connects to AP in VLAN mode (i.e VLAN-100) with open authentication
           Unique Marker: pytest -m "client_connectivity_tests and vlan and general and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_2g_vlan", "appliedRadios": ["2G"], "security_key": "something",
                        "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.open
    @pytest.mark.fiveg
    @allure.story('OPEN 5 GHZ Band')
    @allure.title("VLAN Mode Client Connectivity Test with Open Encryption 5GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10622", name="WIFI-10622")
    def test_vlan_open_5g_client_connectivity(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                              get_test_device_logs,
                                              check_connectivity, setup_configuration):
        """
            To verify that a client created on 5G radio connects to AP in VLAN mode (VLAM-100) with open authentication
           Unique Marker: pytest -m "client_connectivity_tests and vlan and general and open and fiveg"
        """
        profile_data = {"ssid_name": "ssid_open_5g_vlan", "appliedRadios": ["5G"], "security_key": "something",
                        "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    #

    @pytest.mark.wpa
    @pytest.mark.twog
    @allure.story('wpa 2.4 GHZ Band')
    @allure.title("VLAN Mode Client Connectivity Test with WPA Encryption 2.4GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2125", name="WIFI-2125")
    def test_vlan_wpa_2g_client_connectivity(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                             get_test_device_logs,
                                             check_connectivity, setup_configuration):
        """
            To verify that a client created on 2G radio connects to AP in VLAN mode (i.e VLAN-100) with WPA personal authentication
            Unique Marker: pytest -m "client_connectivity_tests and vlan and general and wpa and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa_2g_vlan", "appliedRadios": ["2G"], "security_key": "something",
                        "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @allure.story('wpa 5 GHZ Band')
    @allure.title("VLAN Mode Client Connectivity Test with WPA Encryption 5GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2134", name="WIFI-2134")
    def test_vlan_wpa_5g_client_connectivity(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                             get_test_device_logs,
                                             check_connectivity, setup_configuration):
        """
            To verify that a client created on 5G radio connects to AP in VLAN mode (i.e VLAN-100) with WPA authentication
          Unique Marker: pytest -m "client_connectivity_tests and vlan and general and wpa and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa_5g_vlan", "appliedRadios": ["5G"], "security_key": "something",
                        "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("VLAN Mode Client Connectivity Test with WPA2-Personal Encryption 2.4GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2124", name="WIFI-2124")
    def test_vlan_wpa2_personal_2g_client_connectivity(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                                       get_test_device_logs,
                                                       check_connectivity, setup_configuration):
        """
            To verify that a client created on 2G radio connects to AP in VLAN mode with WPA2-Personal authentication
           Unique Marker: pytest -m "client_connectivity_tests and vlan and general and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_vlan", "appliedRadios": ["2G"], "security_key": "something",
                        "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    #

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("VLAN Mode Client Connectivity Test with WPA2-Personal Encryption 5GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2140", name="WIFI-2140")
    def test_vlan_wpa2_personal_5g_client_connectivity(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                                       get_test_device_logs,
                                                       check_connectivity, setup_configuration):
        """
            To verify that a client created on 5G radio connects to AP in VLAN mode (i.e VLAN-100) with WPA2-Personal authentication
           Unique Marker: pytest -m "client_connectivity_tests and vlan and general and wpa2_personal and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_vlan", "appliedRadios": ["5G"], "security_key": "something",
                        "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result


setup_params_general_two_vlan = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa3_p_5g_vlan", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa3_p_6g_vlan", "appliedRadios": ["6G"], "security_key": "something", "vlan": 100}],
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


@allure.feature("Client Connectivity")
@allure.parent_suite("Client Connectivity Tests")
@allure.suite(suite_name="VLAN Mode")
@allure.sub_suite(sub_suite_name="General security mode Client Connectivity")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_two_vlan],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestVLANModeConnectivitySuiteTwo(object):
    """"
        VLAN Client Connectivity (wpa3_personal. wpa3_personal_mixed. wpa_wpa2_personal_mixed) (twog, fiveg)
        sixg is also available in wpa3_personal band
        pytest -m "client_connectivity_tests and vlan and general"
    """

    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @allure.story('wpa3_personal 2.4 GHZ Band')
    @allure.title("VLAN Mode Client Connectivity Test with WPA3-Personal Encryption 2.4GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10627", name="WIFI-10627")
    def test_vlan_wpa3_personal_2g_client_connectivity(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                                       get_test_device_logs,
                                                       check_connectivity, setup_configuration):
        """
            To verify that a client created on 2G radio connects to AP in VLAN mode (i.e VLAN-100) with WPA3-Personal authentication
           Unique Marker: pytest -m "client_connectivity_tests and vlan and general and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa3_p_2g_vlan", "appliedRadios": ["2G"], "security_key": "something",
                        "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @allure.story('wpa3_personal 5 GHZ Band')
    @allure.title("VLAN Mode Client Connectivity Test with WPA3-Personal Encryption 5GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10629", name="WIFI-10629")
    def test_vlan_wpa3_personal_5g_client_connectivity(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                                       get_test_device_logs,
                                                       check_connectivity, setup_configuration):
        """
            To verify that a client created on 5G radio connects to AP in VLAN mode (i.e VLAN-100) with WPA3-Personal authentication
           Unique Marker: pytest -m "client_connectivity_tests and vlan and general and wpa3_personal and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa3_p_5g_vlan", "appliedRadios": ["5G"], "security_key": "something",
                        "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal
    @pytest.mark.sixg
    @allure.story('wpa3_personal 6 GHZ Band')
    @allure.title("VLAN Mode Client Connectivity Test with WPA3-Personal Encryption 6GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10764", name="WIFI-10764")
    def test_vlan_wpa3_personal_6g_client_connectivity(self, get_test_library, num_stations, get_dut_logs_per_test_case,
                                                       get_test_device_logs,
                                                       check_connectivity, setup_configuration):
        """
            To verify that a client created on 6G radio connects to AP in VLAN mode (i.e VLAN-100) with WPA3-Personal authentication
           Unique Marker: pytest -m "client_connectivity_tests and vlan and general and wpa3_personal and sixg"
        """
        profile_data = {"ssid_name": "ssid_wpa3_p_6g_vlan", "appliedRadios": ["6G"], "security_key": "something",
                        "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        band = "sixg"
        mode = "VLAN"
        vlan = [100]
        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa3_personal_mixed 2.4 GHZ Band')
    @allure.title("VLAN Mode Client Connectivity Test with WPA3-Personal-Mixed Encryption 2.4GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10630", name="WIFI-10630")
    def test_vlan_wpa3_personal_mixed_2g_client_connectivity(self, get_test_library,
                                                             num_stations, get_dut_logs_per_test_case,
                                                             get_test_device_logs,
                                                             check_connectivity, setup_configuration):
        """
            To verify that a client created on 2G radio connects to AP in VLAN mode (i.e VLAN-100) with WPA3-Personal-Mixed authentication
            Unique Marker: pytest -m "client_connectivity_tests and vlan and general and wpa3_personal_mixed and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa3_p_m_2g_vlan", "appliedRadios": ["2G"], "security_key": "something",
                        "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.fiveg
    @allure.story('wpa3_personal_mixed 5 GHZ Band')
    @allure.title("VLAN Mode Client Connectivity Test with WPA3-Personal-Mixed Encryption 5GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10631", name="WIFI-10631")
    def test_vlan_wpa3_personal_mixed_5g_client_connectivity(self, get_test_library,
                                                             num_stations, get_dut_logs_per_test_case,
                                                             get_test_device_logs,
                                                             check_connectivity, setup_configuration):
        """
            To verify that a client created on 5G radio connects to AP in VLAN mode (i.e VLAN-100) with WPA3-Personal-Mixed authentication
           Unique Marker: pytest -m "client_connectivity_tests and vlan and general and wpa3_personal_mixed and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa3_p_m_5g_vlan", "appliedRadios": ["5G"], "security_key": "something",
                        "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa wpa2 personal mixed 2.4 GHZ Band')
    @allure.title("VLAN Mode Client Connectivity Test with WPA-WPA2-Personal-Mixed Encryption 2.4GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10632", name="WIFI-10632")
    def test_vlan_wpa_wpa2_personal_mixed_2g_client_connectivity(self, get_test_library,
                                                                 num_stations, get_dut_logs_per_test_case,
                                                                 get_test_device_logs,
                                                                 check_connectivity, setup_configuration):
        """
            To verify that a client created on 2G radio connects to AP in VLAN mode (i.e VLAN-100) with WPA-WPA2-Personal-Mixed authentication
            Unique Marker: pytest -m "client_connectivity_tests and vlan and general and wpa_wpa2_personal_mixed and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa_wpa2_p_m_2g_vlan", "appliedRadios": ["2G"], "security_key": "something",
                        "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   extra_securities=extra_secu,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.fiveg
    @allure.story('wpa wpa2 personal mixed 5 GHZ Band')
    @allure.title("VLAN Mode Client Connectivity Test with WPA-WPA2-Personal-Mixed Encryption 5GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10633", name="WIFI-10633")
    def test_vlan_wpa_wpa2_personal_mixed_5g_client_connectivity(self, get_test_library,
                                                                 num_stations, get_dut_logs_per_test_case,
                                                                 get_test_device_logs,
                                                                 check_connectivity, setup_configuration):
        """
            To verify that a client created on 5G radio connects to AP in VLAN mode (i.e VLAN-100) with WPA-WPA2-Personal-Mixed  authentication
            Unique Marker: pytest -m "client_connectivity_tests and vlan and general and wpa_wpa2_personal_mixed and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa_wpa2_p_m_5g_vlan", "appliedRadios": ["5G"], "security_key": "something",
                        "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   extra_securities=extra_secu,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=num_stations, vlan_id=vlan)

        assert passes == "PASS", result

