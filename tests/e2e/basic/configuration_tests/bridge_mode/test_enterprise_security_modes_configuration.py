"""

    Profile Configuration : Enterprise SSID's Bridge Mode

"""
import time

import pytest
import allure

pytestmark = [pytest.mark.setup, pytest.mark.bridge, pytest.mark.sanity, pytest.mark.enterprise,
              pytest.mark.usefixtures("setup_test_run")]

setup_params_enterprise = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa_enterprise": [
            {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}]},

    "rf": {},
    "radius": True
}


@pytest.mark.suiteA
@allure.feature("BRIDGE MODE ENTERPRISE SETUP")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestSetupBridgeEnterpriseSuiteA(object):
    """ Enterprise SSID Suite-A"""

    @pytest.mark.wpa_enterprise
    @pytest.mark.twog
    def test_setup_wpa_enterprise_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        """ WPA Enterprise SSID 2.4G """
        if setup_profiles['wpa_enterprise_2g']:
            update_report.update_testrail(case_id=test_cases["ssid_2g_wpa_eap_bridge"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_enterprise_2g']
        else:
            update_report.update_testrail(case_id=test_cases["ssid_2g_wpa_eap_bridge"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa_enterprise
    @pytest.mark.fiveg
    def test_setup_wpa_enterprise_5g_ssid_profile(self, setup_profiles, update_report, test_cases):
        """ WPA Enterprise SSID 5G """
        if setup_profiles['wpa_enterprise_5g']:
            update_report.update_testrail(case_id=test_cases["ssid_5g_wpa_eap_bridge"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_enterprise_5g']
        else:
            update_report.update_testrail(case_id=test_cases["ssid_5g_wpa_eap_bridge"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.sanity_55
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    def test_setup_wpa2_enterprise_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        """ WPA2 Enterprise SSID 2.4G """
        if setup_profiles['wpa2_enterprise_2g']:
            update_report.update_testrail(case_id=test_cases["ssid_2g_wpa2_eap_bridge"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_enterprise_2g']
        else:
            update_report.update_testrail(case_id=test_cases["ssid_2g_wpa2_eap_bridge"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.sanity_55
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    def test_setup_wpa2_enterprise_5g_ssid_profile(self, setup_profiles, update_report, test_cases):
        """ WPA2 Enterprise SSID 5G """
        if setup_profiles['wpa2_enterprise_5g']:
            update_report.update_testrail(case_id=test_cases["ssid_5g_wpa2_eap_bridge"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_enterprise_5g']
        else:
            update_report.update_testrail(case_id=test_cases["ssid_5g_wpa2_eap_bridge"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    def test_setup_wpa3_enterprise_2g_ssid_profile(self, setup_profiles, update_report,
                                                   test_cases):
        """ WPA3 Enterprise SSID 2.4G """
        if setup_profiles['wpa3_enterprise_2g']:
            update_report.update_testrail(case_id=test_cases["ssid_2g_wpa3_eap_bridge"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa3_enterprise_2g']
        else:
            update_report.update_testrail(case_id=test_cases["ssid_2g_wpa3_eap_bridge"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    def test_setup_wpa3_enterprise_5g_ssid_profile(self, setup_profiles, update_report,
                                                   test_cases):
        """ WPA3 Enterprise SSID 5G """
        if setup_profiles['wpa3_enterprise_5g']:
            update_report.update_testrail(case_id=test_cases["ssid_5g_wpa3_eap_bridge"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa3_enterprise_5g']
        else:
            update_report.update_testrail(case_id=test_cases["ssid_5g_wpa3_eap_bridge"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    def test_setup_equipment_ap_profile(self, setup_profiles, update_report,
                                        test_cases):
        """ Equipment AP Profile Suite A Enterprise """
        if setup_profiles['equipment_ap']:
            update_report.update_testrail(case_id=test_cases["ap_profile_bridge"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['equipment_ap']
        else:
            update_report.update_testrail(case_id=test_cases["ap_profile_bridge"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    def test_verify_vif_config(self, setup_profiles, update_report,
                               test_cases):
        """ VIF Config Suite A Enterprise """
        if setup_profiles['vifc']:
            update_report.update_testrail(case_id=test_cases["bridge_vifc"],
                                          status_id=1,
                                          msg='profile pushed successfully')
            assert setup_profiles['vifc']
        else:
            update_report.update_testrail(case_id=test_cases["bridge_vifc"],
                                          status_id=5,
                                          msg='Failed to push profile')
            assert False

    @allure.severity(allure.severity_level.BLOCKER)
    def test_verify_vif_state(self, setup_profiles, update_report,
                              test_cases):
        """ VIF Config Suite B Enterprise """
        time.sleep(200)
        if setup_profiles['vifs']:
            update_report.update_testrail(case_id=test_cases["bridge_vifs"],
                                          status_id=1,
                                          msg='profile pushed successfully')
            assert setup_profiles['vifs']
        else:
            update_report.update_testrail(case_id=test_cases["bridge_vifs"],
                                          status_id=5,
                                          msg='Failed to push profile')
            assert False


setup_params_enterprise_two = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa_wpa2_enterprise_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_eap_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa_wpa2_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa3_enterprise_mixed": [
            {"ssid_name": "ssid_wpa3_mixed_eap_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa3_mixed_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}]
    },
    "rf": {},
    "radius": True
}


@pytest.mark.suiteB
@allure.feature("BRIDGE MODE ENTERPRISE SETUP")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestSetupBridgeEnterpriseSuiteB(object):

    """ Enterprise SSID Suite-B"""

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.twog
    def test_setup_wpa_wpa2_enterprise_mixed_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        """ WPA WPA2 Enterprise SSID 2.4G """
        if setup_profiles['wpa_wpa2_enterprise_mixed_2g']:
            update_report.update_testrail(case_id=test_cases["ssid_2g_wpa_wpa2_enterprise_mixed_bridge"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa_wpa2_enterprise_mixed_2g']
        else:
            update_report.update_testrail(case_id=test_cases["ssid_2g_wpa_wpa2_enterprise_mixed_bridge"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.fiveg
    def test_setup_wpa_wpa2_enterprise_mixed_5g_ssid_profile(self, setup_profiles, update_report, test_cases):
        """ WPA WPA2 Enterprise SSID 5G """
        if setup_profiles['wpa_wpa2_enterprise_mixed_5g']:
            update_report.update_testrail(case_id=test_cases["ssid_5g_wpa_wpa2_enterprise_mixed_bridge"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa_wpa2_enterprise_mixed_5g']
        else:
            update_report.update_testrail(case_id=test_cases["ssid_5g_wpa_wpa2_enterprise_mixed_bridge"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.twog
    def test_setup_wpa3_enterprise_mixed_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        """ WPA3 Enterprise Mixed SSID 2.4G """
        if setup_profiles['wpa3_enterprise_mixed_2g']:
            update_report.update_testrail(case_id=test_cases["ssid_2g_wpa3_enterprise_mixed_bridge"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa3_enterprise_mixed_2g']
        else:
            update_report.update_testrail(case_id=test_cases["ssid_2g_wpa3_enterprise_mixed_bridge"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.fiveg
    def test_setup_wpa3_enterprise_mixed_5g_ssid_profile(self, setup_profiles, update_report,
                                                         test_cases):
        """ WPA3 Enterprise Mixed SSID 5G """
        if setup_profiles['wpa3_enterprise_mixed_5g']:
            update_report.update_testrail(case_id=test_cases["ssid_5g_wpa3_enterprise_mixed_bridge"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa3_enterprise_mixed_5g']
        else:
            update_report.update_testrail(case_id=test_cases["ssid_5g_wpa3_enterprise_mixed_bridge"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    def test_setup_equipment_ap_profile(self, setup_profiles, update_report,
                                        test_cases):
        """ Equipment AP Profile Suite B Enterprise """
        if setup_profiles['equipment_ap']:
            update_report.update_testrail(case_id=test_cases["ap_profile_bridge"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['equipment_ap']
        else:
            update_report.update_testrail(case_id=test_cases["ap_profile_bridge"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    def test_verify_vif_config(self, setup_profiles, update_report,
                               test_cases):
        """ VIF Config Suite B Enterprise """
        if setup_profiles['vifc']:
            update_report.update_testrail(case_id=test_cases["bridge_vifc"],
                                          status_id=1,
                                          msg='profile pushed successfully')
            assert setup_profiles['vifc']
        else:
            update_report.update_testrail(case_id=test_cases["bridge_vifc"],
                                          status_id=5,
                                          msg='Failed to push profile')
            assert False

    @allure.severity(allure.severity_level.BLOCKER)
    def test_verify_vif_state(self, setup_profiles, update_report,
                              test_cases):
        """ VIF State Suite B Enterprise """
        time.sleep(200)
        if setup_profiles['vifs']:
            update_report.update_testrail(case_id=test_cases["bridge_vifs"],
                                          status_id=1,
                                          msg='profile pushed successfully')
            assert setup_profiles['vifs']
        else:
            update_report.update_testrail(case_id=test_cases["bridge_vifs"],
                                          status_id=5,
                                          msg='Failed to push profile')
            assert False
