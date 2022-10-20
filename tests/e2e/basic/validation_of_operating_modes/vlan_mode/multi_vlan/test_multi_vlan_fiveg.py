"""
    Create VLAN ,connect stations and flow traffic through it : vlan Mode
    pytest -m multi_vlan_tests
"""

import allure
import pytest

pytestmark=[pytest.mark.ow_regression_lf,
            pytest.mark.multi_vlan_tests,
            pytest.mark.fiveg]

setup_params_general={
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"], "vlan": 100}],

        "wpa": [{"ssid_name": "ssid_wpa_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 125}],

        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 200}],

        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g", "appliedRadios": ["5G"], "security_key": "something",
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
@allure.parent_suite("OpenWifi MULTI VLAN Test")
@allure.suite("VLAN Mode")
@allure.sub_suite("5Ghz")
@pytest.mark.usefixtures("setup_configuration")
class TestMultiVlan(object):

    @pytest.mark.open
    @pytest.mark.fiveg
    @pytest.mark.multi_vlan
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2161", name="WIFI-2161")
    @allure.title("Test VLAN with Open Security Mode")
    def test_multi_vlan_open_5g(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs, num_stations, setup_configuration):
        """
                    Multi VLAN Test with open encryption 2.4 GHz Band
                    pytest -m "multi_vlan_tests and open and fiveg"
        """
        profile_data={"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"], "vlan": 100}
        ssid_name=profile_data["ssid_name"]
        security_key="[BLANK]"
        security="open"
        mode="VLAN"
        band="fiveg"
        vlan=[profile_data["vlan"]]

        passes, result=get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                 dut_data=setup_configuration,
                                                                 passkey=security_key, mode=mode, band=band,
                                                                 num_sta=1, vlan_id=vlan)
        assert passes == "PASS", result

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @pytest.mark.multi_vlan
    @pytest.mark.ow_sanity_lf
    @allure.testcase(name="WIFI-2169",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2169")
    @allure.title("Test VLAN with WPA Security Mode")
    def test_multi_vlan_wpa_5g(self, get_test_library, get_dut_logs_per_test_case,
                               get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
                    Multi VLAN Test with open encryption 2.4 GHz Band
                    pytest -m "multi_vlan_tests and open and fiveg"
        """
        profile_data={"ssid_name": "ssid_wpa_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 125}
        ssid_name=profile_data["ssid_name"]
        security_key=profile_data["security_key"]
        security="open"
        mode="VLAN"
        band="fiveg"
        vlan=[profile_data["vlan"]]

        passes, result=get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                 dut_data=setup_configuration,
                                                                 passkey=security_key, mode=mode, band=band,
                                                                 num_sta=1, vlan_id=vlan)
        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.multi_vlan
    @pytest.mark.ow_sanity_lf
    @allure.testcase(name="WIFI-2157",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2157")
    @allure.title("Test VLAN with WPA2 Personal Security Mode")
    def test_multi_vlan_wpa2_personal_5g(self, get_test_library, get_dut_logs_per_test_case,
                                         get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
                    Multi VLAN Test with open encryption 2.4 GHz Band
                    pytest -m "multi_vlan_tests and open and fiveg"
        """
        profile_data={"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 200}
        ssid_name=profile_data["ssid_name"]
        security_key=profile_data["security_key"]
        security="open"
        mode="VLAN"
        band="fiveg"
        vlan=[profile_data["vlan"]]

        passes, result=get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                 dut_data=setup_configuration,
                                                                 passkey=security_key, mode=mode, band=band,
                                                                 num_sta=1, vlan_id=vlan)
        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.fiveg
    @pytest.mark.multi_vlan
    @allure.testcase(name="WIFI-2167",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2167")
    @allure.title("Test VLAN with WPA-WPA2 Persoanl Security ")
    def test_multi_vlan_wpa_wpa2_personal_5g(self, get_test_library, get_dut_logs_per_test_case,
                                             get_test_device_logs, num_stations, setup_configuration):
        """
                    Multi VLAN Test with open encryption 2.4 GHz Band
                    pytest -m "multi_vlan_tests and open and fiveg"
        """
        profile_data={"ssid_name": "ssid_wpa_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 150}
        ssid_name=profile_data["ssid_name"]
        security_key=profile_data["security_key"]
        security="open"
        mode="VLAN"
        band="fiveg"
        vlan=[profile_data["vlan"]]

        passes, result=get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                 dut_data=setup_configuration,
                                                                 passkey=security_key, mode=mode, band=band,
                                                                 num_sta=1, vlan_id=vlan)
        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.disable_vlan_fiveg  # wifi-2174
    @pytest.mark.ow_sanity_lf
    @allure.testcase(name="test_disable_vlan_wpa2_ssid_5g",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-2174")
    @allure.title("Test Disabled VLAN with WPA2 Security Mode")
    def test_disable_vlan_wpa2_5g(self, get_test_library, get_dut_logs_per_test_case,
                                  get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Client connectivity using vlan, wpa2, fiveg
            pytest -m disable_vlan_fiveg
        """
        """
                            Multi VLAN Test with open encryption 2.4 GHz Band
                            pytest -m "multi_vlan_tests and open and fiveg"
                """
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 200}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = [profile_data["vlan"]]

        passes, result = get_test_library.client_connectivity_test(ssid=ssid_name, security=security,
                                                                   dut_data=setup_configuration,
                                                                   passkey=security_key, mode=mode, band=band,
                                                                   num_sta=1, vlan_id=None)
        assert passes == "PASS", result