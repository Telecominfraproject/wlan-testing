import pytest
import allure

pytestmark = [pytest.mark.setup, pytest.mark.nat, pytest.mark.sanity, pytest.mark.enterprise, pytest.mark.usefixtures("setup_test_run")]

setup_params_enterprise = {
    "mode": "NAT",
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


@pytest.mark.enterprise
@allure.feature("NAT MODE ENTERPRISE SETUP")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestSetupNATEnterprise(object):

    @pytest.mark.wpa_enterprise
    @pytest.mark.twog
    def test_setup_wpa_enterprise_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        if setup_profiles['wpa_enterprise_2g']:
            update_report.update_testrail(case_id=test_cases["wpa_enterprise_2g_nat"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_enterprise_2g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa_enterprise_2g_nat"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa_enterprise
    @pytest.mark.fiveg
    def test_setup_wpa_enterprise_5g_ssid_profile(self, setup_profiles, update_report, test_cases):

        if setup_profiles['wpa_enterprise_5g']:
            update_report.update_testrail(case_id=test_cases["wpa_enterprise_5g_nat"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_enterprise_5g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa_enterprise_5g_nat"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    def test_setup_wpa2_enterprise_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        if setup_profiles['wpa2_enterprise_2g']:
            update_report.update_testrail(case_id=test_cases["wpa2_enterprise_2g_nat"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_enterprise_2g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa2_enterprise_2g_nat"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    def test_setup_wpa2_enterprise_5g_ssid_profile(self, setup_profiles, update_report, test_cases):

        if setup_profiles['wpa2_enterprise_5g']:
            update_report.update_testrail(case_id=test_cases["wpa2_enterprise_5g_nat"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_enterprise_5g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa2_enterprise_5g_nat"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    def test_setup_wpa3_enterprise_2g_ssid_profile(self, setup_profiles, update_report,
                                                   test_cases):

        if setup_profiles['wpa3_enterprise_2g']:
            update_report.update_testrail(case_id=test_cases["wpa3_enterprise_2g_nat"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa3_enterprise_2g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa3_enterprise_2g_nat"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    def test_setup_wpa3_enterprise_5g_ssid_profile(self, setup_profiles, update_report,
                                                   test_cases):

        if setup_profiles['wpa3_enterprise_5g']:
            update_report.update_testrail(case_id=test_cases["wpa3_enterprise_5g_nat"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa3_enterprise_5g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa3_enterprise_5g_nat"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    def test_setup_equipment_ap_profile(self, setup_profiles, update_report,
                                        test_cases):

        if setup_profiles['equipment_ap']:
            update_report.update_testrail(case_id=test_cases["equipment_ap_nat"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['equipment_ap']
        else:
            update_report.update_testrail(case_id=test_cases["equipment_ap_nat"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    def test_verify_vif_config(self, setup_profiles, update_report,
                               test_cases):

        if setup_profiles['vifc']:
            update_report.update_testrail(case_id=test_cases["nat_vifc"],
                                          status_id=1,
                                          msg='profile pushed successfully')
            assert setup_profiles['vifc']
        else:
            update_report.update_testrail(case_id=test_cases["nat_vifc"],
                                          status_id=5,
                                          msg='Failed to push profile')
            assert False

    def test_verify_vif_state(self, setup_profiles, update_report,
                              test_cases):
        if setup_profiles['vifs']:
            update_report.update_testrail(case_id=test_cases["nat_vifs"],
                                          status_id=1,
                                          msg='profile pushed successfully')
            assert setup_profiles['vifs']
        else:
            update_report.update_testrail(case_id=test_cases["nat_vifs"],
                                          status_id=5,
                                          msg='Failed to push profile')
            assert False
