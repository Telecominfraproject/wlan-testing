import allure
import pytest
import time

pytestmark = [pytest.mark.setup, pytest.mark.NAT, pytest.mark.sanity]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["is2dot4GHz"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
                 "security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@pytest.mark.basic
@allure.feature("NAT MODE SETUP")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestSetupNAT(object):

    @pytest.mark.open
    @pytest.mark.twog
    def test_setup_wpa_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        if setup_profiles['open_2g']:
            update_report.update_testrail(case_id=test_cases["open_2g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['open_2g']
        else:
            update_report.update_testrail(case_id=test_cases["open_2g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.open
    @pytest.mark.fiveg
    def test_setup_wpa_5g_ssid_profile(self, setup_profiles, update_report, test_cases):

        if setup_profiles['open_5g']:
            update_report.update_testrail(case_id=test_cases["open_5g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['open_5g']
        else:
            update_report.update_testrail(case_id=test_cases["open_5g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_setup_wpa_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        if setup_profiles['wpa_2g']:
            update_report.update_testrail(case_id=test_cases["wpa_2g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa_2g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa_2g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_setup_wpa_5g_ssid_profile(self, setup_profiles, update_report, test_cases):

        if setup_profiles['wpa_5g']:
            update_report.update_testrail(case_id=test_cases["wpa_5g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa_5g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa_5g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_setup_wpa2_personal_2g_ssid_profile(self, setup_profiles, update_report,
                                                 test_cases):

        if setup_profiles['wpa2_personal_2g']:
            update_report.update_testrail(case_id=test_cases["wpa2_personal_2g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_personal_2g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa2_personal_2g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_setup_wpa2_personal_5g_ssid_profile(self, setup_profiles, update_report,
                                                 test_cases):

        if setup_profiles['wpa2_personal_5g']:
            update_report.update_testrail(case_id=test_cases["wpa2_personal_5g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_personal_5g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa2_personal_5g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    def test_setup_equipment_ap_profile(self, setup_profiles, update_report,
                                        test_cases):

        if setup_profiles['equipment_ap']:
            update_report.update_testrail(case_id=test_cases["equipment_ap"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['equipment_ap']
        else:
            update_report.update_testrail(case_id=test_cases["equipment_ap"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    def test_verify_vif_config(self, setup_profiles, update_report,
                               test_cases):

        if setup_profiles['vifc']:
            update_report.update_testrail(case_id=test_cases["vifc"],
                                          status_id=1,
                                          msg='profile pushed successfully')
            assert setup_profiles['vifc']
        else:
            update_report.update_testrail(case_id=test_cases["vifc"],
                                          status_id=5,
                                          msg='Failed to push profile')
            assert False

    def test_verify_vif_state(self, setup_profiles, update_report,
                              test_cases):
        if setup_profiles['vifs']:
            update_report.update_testrail(case_id=test_cases["vifs"],
                                          status_id=1,
                                          msg='profile pushed successfully')
            time.sleep(100)
            assert setup_profiles['vifs']
        else:
            update_report.update_testrail(case_id=test_cases["vifs"],
                                          status_id=5,
                                          msg='Failed to push profile')
            time.sleep(100)
            assert False


setup_params_general_two = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}],
        "wpa3_personal_mixed": [
            {"ssid_name": "ssid_wpa3_p_m_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_m_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}],
        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}]
    },
    "rf": {},
    "radius": False
}


@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestNATModeConnectivitySuiteTwo(object):

    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    def test_setup_wpa3_personal_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        if setup_profiles['open_2g']:
            update_report.update_testrail(case_id=test_cases["open_2g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['open_2g']
        else:
            update_report.update_testrail(case_id=test_cases["open_2g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    def test_setup_wpa3_personal_5g_ssid_profile(self, setup_profiles, update_report, test_cases):

        if setup_profiles['open_5g']:
            update_report.update_testrail(case_id=test_cases["open_5g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['open_5g']
        else:
            update_report.update_testrail(case_id=test_cases["open_5g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.twog
    def test_setup_wpa3_personal_mixed_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        if setup_profiles['wpa_2g']:
            update_report.update_testrail(case_id=test_cases["wpa_2g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa_2g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa_2g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.fiveg
    def test_setup_wpa3_personal_mixed_5g_ssid_profile(self, setup_profiles, update_report, test_cases):

        if setup_profiles['wpa_5g']:
            update_report.update_testrail(case_id=test_cases["wpa_5g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa_5g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa_5g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.twog
    def test_setup_wpa_wpa2_personal_mixed_2g_ssid_profile(self, setup_profiles, update_report,
                                                           test_cases):

        if setup_profiles['wpa2_personal_2g']:
            update_report.update_testrail(case_id=test_cases["wpa_wpa2_personal_mixed_2g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_personal_2g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa_wpa2_personal_mixed_2g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.fiveg
    def test_setup_wpa_wpa2_personal_mixed_5g_ssid_profile(self, setup_profiles, update_report,
                                                           test_cases):

        if setup_profiles['wpa2_personal_5g']:
            update_report.update_testrail(case_id=test_cases["wpa_wpa2_personal_mixed_5g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_personal_5g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa_wpa2_personal_mixed_5g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    def test_setup_equipment_ap_profile(self, setup_profiles, update_report,
                                        test_cases):

        if setup_profiles['equipment_ap']:
            update_report.update_testrail(case_id=test_cases["equipment_ap"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['equipment_ap']
        else:
            update_report.update_testrail(case_id=test_cases["equipment_ap"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    def test_verify_vif_config(self, setup_profiles, update_report,
                               test_cases):

        if setup_profiles['vifc']:
            update_report.update_testrail(case_id=test_cases["vifc"],
                                          status_id=1,
                                          msg='profile pushed successfully')
            assert setup_profiles['vifc']
        else:
            update_report.update_testrail(case_id=test_cases["vifc"],
                                          status_id=5,
                                          msg='Failed to push profile')
            assert False

    def test_verify_vif_state(self, setup_profiles, update_report,
                              test_cases):
        if setup_profiles['vifs']:
            update_report.update_testrail(case_id=test_cases["vifs"],
                                          status_id=1,
                                          msg='profile pushed successfully')
            time.sleep(100)
            assert setup_profiles['vifs']
        else:
            update_report.update_testrail(case_id=test_cases["vifs"],
                                          status_id=5,
                                          msg='Failed to push profile')
            time.sleep(100)
            assert False


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
    def test_setup_wpa2_enterprise_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        if setup_profiles['wpa_enterprise_2g']:
            update_report.update_testrail(case_id=test_cases["wpa2_enterprise_2g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_enterprise_2g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa2_enterprise_2g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa_enterprise
    @pytest.mark.fiveg
    def test_setup_wpa2_enterprise_5g_ssid_profile(self, setup_profiles, update_report, test_cases):

        if setup_profiles['wpa_enterprise_5g']:
            update_report.update_testrail(case_id=test_cases["wpa2_enterprise_5g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_enterprise_5g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa2_enterprise_5g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    def test_setup_wpa2_enterprise_2g_ssid_profile(self, setup_profiles, update_report, test_cases):
        if setup_profiles['wpa2_enterprise_2g']:
            update_report.update_testrail(case_id=test_cases["wpa2_enterprise_2g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_enterprise_2g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa2_enterprise_2g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    def test_setup_wpa2_enterprise_5g_ssid_profile(self, setup_profiles, update_report, test_cases):

        if setup_profiles['wpa2_enterprise_5g']:
            update_report.update_testrail(case_id=test_cases["wpa2_enterprise_5g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa2_enterprise_5g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa2_enterprise_5g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    def test_setup_wpa3_enterprise_2g_ssid_profile(self, setup_profiles, update_report,
                                                   test_cases):

        if setup_profiles['wpa3_enterprise_2g']:
            update_report.update_testrail(case_id=test_cases["wpa3_enterprise_2g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa3_enterprise_2g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa3_enterprise_2g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    def test_setup_wpa3_enterprise_5g_ssid_profile(self, setup_profiles, update_report,
                                                   test_cases):

        if setup_profiles['wpa3_enterprise_5g']:
            update_report.update_testrail(case_id=test_cases["wpa3_enterprise_5g"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['wpa3_enterprise_5g']
        else:
            update_report.update_testrail(case_id=test_cases["wpa3_enterprise_5g"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    def test_setup_equipment_ap_profile(self, setup_profiles, update_report,
                                        test_cases):

        if setup_profiles['equipment_ap']:
            update_report.update_testrail(case_id=test_cases["equipment_ap"],
                                          status_id=1,
                                          msg='profile created successfully')
            assert setup_profiles['equipment_ap']
        else:
            update_report.update_testrail(case_id=test_cases["equipment_ap"],
                                          status_id=5,
                                          msg='Failed to create profile')
            assert False

    def test_verify_vif_config(self, setup_profiles, update_report,
                               test_cases):

        if setup_profiles['vifc']:
            update_report.update_testrail(case_id=test_cases["vifc"],
                                          status_id=1,
                                          msg='profile pushed successfully')
            assert setup_profiles['vifc']
        else:
            update_report.update_testrail(case_id=test_cases["vifc"],
                                          status_id=5,
                                          msg='Failed to push profile')
            assert False

    def test_verify_vif_state(self, setup_profiles, update_report,
                              test_cases):
        if setup_profiles['vifs']:
            update_report.update_testrail(case_id=test_cases["vifs"],
                                          status_id=1,
                                          msg='profile pushed successfully')
            time.sleep(100)
            assert setup_profiles['vifs']
        else:
            update_report.update_testrail(case_id=test_cases["vifs"],
                                          status_id=5,
                                          msg='Failed to push profile')
            time.sleep(100)
            assert False
