"""
    Create VLAN ,connect stations and flow traffic through it : vlan Mode
    pytest -m multi_vlan_tests
"""

import allure
import pytest

pytestmark = [pytest.mark.ow_regression_lf,
              pytest.mark.multi_vlan_tests,
              pytest.mark.twog]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"], "vlan": 100}],

        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 125}],

        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 200}],

        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g", "appliedRadios": ["2G"], "security_key": "something",
             "vlan": 150}],
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
@allure.feature("Multi VLAN Test")
@allure.parent_suite("Multi VLAN Test")
@allure.suite("VLAN Mode")
@allure.sub_suite("2.4 Ghz")
@pytest.mark.usefixtures("setup_configuration")
class TestMultiVlan(object):

    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.multi_vlan
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2160", name="WIFI-2160")
    @allure.title("Test VLAN with Open Security Mode")
    def test_multi_vlan_open_2g(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs, num_stations, setup_configuration):
        """
                    To verify that a client operating with open security will connect or not using multi vlans.
                    pytest -m "open and multi_vlan and twog"
        """
        profile_data = {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"], "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = [100]

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=1, vlan_id=vlan)
        assert passes == "PASS", result

    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.multi_vlan
    @pytest.mark.ow_sanity_lf
    @allure.testcase(name="WIFI-2168",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2168")
    @allure.title("Test VLAN with WPA Security Mode")
    def test_multi_vlan_wpa_2g(self, get_test_library, get_dut_logs_per_test_case,
                               get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
                    Multi VLAN Test with wpa encryption 2.4 GHz Band
                    pytest -m "multi_vlan_tests and wpa and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 125}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "VLAN"
        band = "twog"
        vlan = [125]

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=1, vlan_id=vlan)
        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.multi_vlan
    @pytest.mark.ow_sanity_lf
    @allure.testcase(name="WIFI-2156",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2156")
    @allure.title("Test VLAN with WPA2 Personal Security Mode")
    def test_multi_vlan_wpa2_personal_2g(self, get_test_library, get_dut_logs_per_test_case,
                                         get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
                    Multi VLAN Test with wpa2_personal encryption 2.4 GHz Band
                    pytest -m "multi_vlan_tests and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 200}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = [250]

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=1, vlan_id=vlan)
        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.twog
    @pytest.mark.multi_vlan
    @allure.testcase(name="WIFI-2166",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2166")
    @allure.title("Test VLAN with WPA-WPA2 Persoanl Security ")
    def test_multi_vlan_wpa_wpa2_personal_2g(self, get_test_library, get_dut_logs_per_test_case,
                                             get_test_device_logs, num_stations, setup_configuration):
        """
                    To verify that a client operating with wpa mixed(personal) security will connect or not using multi vlans.
                    pytest -m "multi_vlan_tests and wpa_wpa2_personal_mixed and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa_wpa2_p_m_2g", "appliedRadios": ["2G"], "security_key": "something",
                        "vlan": 150}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_sec = ["wpa2"]
        mode = "VLAN"
        band = "twog"
        vlan = [150]

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   extra_securities=extra_sec,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=1, vlan_id=vlan)
        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.disable_vlan_twog  # wifi-2172
    @pytest.mark.ow_sanity_lf
    @allure.testcase(name="WIFI-2172",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2172")
    @allure.title("Test Disabled VLAN with WPA2 Security Mode")
    def test_disable_vlan_wpa2_2g(self, get_test_library, get_dut_logs_per_test_case,
                                  get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            To verify that a client operating with wpa2(personal) security will connect or not by disabling VLAN.
            Unique marker:pytest -m "disable_vlan_twog and twog and wpa2_personal and ow_sanity_lf"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 200}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = [250]

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=1, vlan_id=vlan)
        assert passes == "FAIL", result

