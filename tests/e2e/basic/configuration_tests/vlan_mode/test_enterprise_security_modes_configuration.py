"""

    Profile Configuration : Enterprise SSID's vlan Mode

"""
import time

import pytest
import allure

pytestmark = [pytest.mark.setup, pytest.mark.vlan, pytest.mark.sanity, pytest.mark.enterprise,
              pytest.mark.usefixtures("setup_test_run")]

setup_params_enterprise = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa_enterprise": [
            {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa_eap_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "vlan": 100}]},

    "rf": {},
    "radius": True
}


@pytest.mark.suiteA
@allure.feature("VLAN MODE ENTERPRISE SETUP")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestSetupVLANEnterpriseSuiteA(object):
    """ Enterprise SSID Suite-A"""

    @pytest.mark.wpa_enterprise
    @pytest.mark.twog
    def test_setup_wpa_enterprise_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        """ WPA Enterprise SSID 2.4G """
        assert setup_profiles['wpa2_enterprise_2g']

    @pytest.mark.wpa_enterprise
    @pytest.mark.fiveg
    def test_setup_wpa_enterprise_5g_ssid_profile(self, setup_profiles, update_report, test_cases):
        """ WPA Enterprise SSID 5G """

        assert setup_profiles['wpa2_enterprise_5g']

    @pytest.mark.sanity_light
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    def test_setup_wpa2_enterprise_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        """ WPA2 Enterprise SSID 2.4G """

        assert setup_profiles['wpa2_enterprise_2g']

    @pytest.mark.sanity_light
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    def test_setup_wpa2_enterprise_5g_ssid_profile(self, setup_profiles, update_report, test_cases):
        """ WPA2 Enterprise SSID 5G """
        assert setup_profiles['wpa2_enterprise_5g']

    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    def test_setup_wpa3_enterprise_2g_ssid_profile(self, setup_profiles, update_report,
                                                   test_cases):
        """ WPA3 Enterprise SSID 2.4G """
        assert setup_profiles['wpa3_enterprise_2g']

    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    def test_setup_wpa3_enterprise_5g_ssid_profile(self, setup_profiles, update_report,
                                                   test_cases):
        """ WPA3 Enterprise SSID 5G """
        assert setup_profiles['wpa3_enterprise_5g']

    @pytest.mark.sanity_light
    def test_setup_equipment_ap_profile(self, setup_profiles, update_report,
                                        test_cases):
        """ Equipment AP Profile Suite A Enterprise """
        assert setup_profiles['equipment_ap']

    @pytest.mark.sanity_light
    def test_verify_vif_config(self, setup_profiles, update_report,
                               test_cases):
        """ VIF Config Suite A Enterprise """
        assert setup_profiles['vifc']

    @pytest.mark.sanity_light
    @allure.severity(allure.severity_level.BLOCKER)
    def test_verify_vif_state(self, setup_profiles, update_report,
                              test_cases):
        """ VIF Config Suite B Enterprise """
        time.sleep(200)
        assert setup_profiles['vifs']


setup_params_enterprise_two = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa_wpa2_enterprise_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa_wpa2_eap_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa3_enterprise_mixed": [
            {"ssid_name": "ssid_wpa3_mixed_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa3_mixed_eap_5g", "appliedRadios": ["5G"], "vlan": 100}]
    },
    "rf": {},
    "radius": True
}


@pytest.mark.suiteB
@allure.feature("VLAN MODE ENTERPRISE SETUP")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestSetupVLANEnterpriseSuiteB(object):

    """ Enterprise SSID Suite-B"""

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.twog
    def test_setup_wpa_wpa2_enterprise_mixed_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        """ WPA WPA2 Enterprise SSID 2.4G """
        assert setup_profiles['wpa_wpa2_enterprise_mixed_2g']

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.fiveg
    def test_setup_wpa_wpa2_enterprise_mixed_5g_ssid_profile(self, setup_profiles, update_report, test_cases):
        """ WPA WPA2 Enterprise SSID 5G """
        assert setup_profiles['wpa_wpa2_enterprise_mixed_5g']

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.twog
    def test_setup_wpa3_enterprise_mixed_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        """ WPA3 Enterprise Mixed SSID 2.4G """
        assert setup_profiles['wpa3_enterprise_mixed_2g']

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.fiveg
    def test_setup_wpa3_enterprise_mixed_5g_ssid_profile(self, setup_profiles, update_report,
                                                         test_cases):
        """ WPA3 Enterprise Mixed SSID 5G """
        assert setup_profiles['wpa3_enterprise_mixed_5g']

    def test_setup_equipment_ap_profile(self, setup_profiles, update_report,
                                        test_cases):
        """ Equipment AP Profile Suite B Enterprise """
        assert setup_profiles['equipment_ap']

    def test_verify_vif_config(self, setup_profiles, update_report,
                               test_cases):
        """ VIF Config Suite B Enterprise """
        assert setup_profiles['vifc']

    @allure.severity(allure.severity_level.BLOCKER)
    def test_verify_vif_state(self, setup_profiles, update_report,
                              test_cases):
        """ VIF State Suite B Enterprise """
        time.sleep(200)
        assert setup_profiles['vifs']
