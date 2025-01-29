"""
    Create VLAN ,connect stations and flow traffic through it : vlan Mode
    pytest -m multi_vlan_tests
"""

import allure
import pytest

pytestmark = [pytest.mark.multi_vlan_tests, pytest.mark.sixg]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 200},
            {"ssid_name": "ssid_wpa3_p_6g_vlan", "appliedRadios": ["6G"], "security_key": "something", "vlan": 200}],
    },
    "rf": {
        "6G": {
            "band": "6G",
            "channel-mode": "EHT",
            "channel-width": 80,
        }
    },
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
@allure.sub_suite("6Ghz")
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.wpa3_personal
@pytest.mark.twog
class TestMultiVlan(object):

    @pytest.mark.wpa3_personal
    @pytest.mark.sixg
    @pytest.mark.multi_vlan
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14358", name="WIFI-14358")
    @allure.title("Test VLAN with WPA3 Personal Security Mode")
    def test_multi_vlan_wpa3_6g(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs, num_stations, setup_configuration):
        """
                    To verify that a client operating with WPA3(personal) security will connect or not using Multi VLANS
            pytest -m "multi_vlan and wpa3_personal and sixg and ow_sanity_lf"
        """
        profile_data = {"ssid_name": "ssid_wpa3_p_6g_vlan", "appliedRadios": ["6G"], "security_key": "something", "vlan": 200}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "sixg"
        vlan = [200]

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=1, vlan_id=vlan)
        assert passes == "PASS", result

    @pytest.mark.wpa3_personal
    @pytest.mark.sixg
    @pytest.mark.disable_vlan_sixg  # wifi-2174
    @pytest.mark.ow_sanity_lf
    @allure.testcase(name="WIFI-14361",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-14361")
    @allure.title("Test Disabled VLAN with WPA3 Security Mode")
    def test_disable_vlan_wpa3_6g(self, get_test_library, get_dut_logs_per_test_case,
                                  get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            To verify that a client operating with WPA3 security will connect or not by disabling the VLAN
            pytest -m "disable_vlan_sixg and wpa3_personal and sixg and ow_sanity_lf"
        """
        profile_data = {"ssid_name": "ssid_wpa3_p_6g_vlan", "appliedRadios": ["6G"], "security_key": "something", "vlan": 200}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "sixg"
        vlan = [250]

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=1, vlan_id=vlan)
        assert passes == "FAIL", result
