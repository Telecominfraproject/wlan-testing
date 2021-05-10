"""
    Test Case Module:  setup test cases for bridge mode sanity
    Details:    bridge mode setup

"""
import time

import pytest


@pytest.mark.sanity
@pytest.mark.setup_bridge
@pytest.mark.bridge
@pytest.mark.parametrize(
    'setup_profiles, create_profiles',
    [(["BRIDGE"], ["BRIDGE"])],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.usefixtures("create_profiles")
class TestSetupBridge:

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_setup_wpa_2g_ssid_profile(self, create_profiles, instantiate_testrail, instantiate_project, test_cases):
        if create_profiles['ssid_2g_wpa_bridge']:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_2g_wpa_bridge"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['ssid_2g_wpa_bridge']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_2g_wpa_bridge"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to create profile')
            assert False

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_setup_wpa_5g_ssid_profile(self, create_profiles, instantiate_testrail, instantiate_project, test_cases):

        if create_profiles['ssid_5g_wpa_bridge']:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_5g_wpa_bridge"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['ssid_5g_wpa_bridge']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_5g_wpa_bridge"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to create profile')
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_setup_wpa2_personal_2g_ssid_profile(self, create_profiles, instantiate_testrail, instantiate_project,
                                                 test_cases):

        if create_profiles['ssid_2g_wpa2_bridge']:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_2g_wpa2_bridge"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['ssid_2g_wpa2_bridge']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_2g_wpa2_bridge"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to create profile')
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_setup_wpa2_personal_5g_ssid_profile(self, create_profiles, instantiate_testrail, instantiate_project,
                                                 test_cases):

        if create_profiles['ssid_5g_wpa2_bridge']:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_5g_wpa2_bridge"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['ssid_5g_wpa2_bridge']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_5g_wpa2_bridge"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to create profile')
            assert False

    @pytest.mark.radius
    def test_setup_radius_profile(self, create_profiles, instantiate_testrail, instantiate_project, test_cases):

        if create_profiles['radius_profile']:
            instantiate_testrail.update_testrail(case_id=test_cases["radius_profile"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['radius_profile']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["radius_profile"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to create profile')
            assert False

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.radius
    def test_setup_wpa2_enterprise_2g_ssid_profile(self, create_profiles, instantiate_testrail, instantiate_project,
                                                   test_cases):

        if create_profiles['ssid_2g_eap_bridge']:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_2g_eap_bridge"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['ssid_2g_eap_bridge']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_2g_eap_bridge"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to create profile')
            assert False

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.radius
    def test_setup_wpa2_enterprise_5g_ssid_profile(self, create_profiles, instantiate_testrail, instantiate_project,
                                                   test_cases):

        if create_profiles['ssid_5g_eap_bridge']:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_5g_eap_bridge"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['ssid_5g_eap_bridge']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_5g_eap_bridge"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to create profile')
            assert False

    def test_setup_equipment_ap_profile(self, create_profiles, instantiate_testrail, instantiate_project,
                                        test_cases):

        if create_profiles['ap_bridge']:
            instantiate_testrail.update_testrail(case_id=test_cases["ap_bridge"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['ap_bridge']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["ap_bridge"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to create profile')
            assert False

    def test_verify_vif_config(self, setup_profiles, instantiate_testrail, instantiate_project,
                               test_cases):

        if setup_profiles['bridge_vifc']:
            instantiate_testrail.update_testrail(case_id=test_cases["bridge_vifc"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile pushed successfully')
            assert setup_profiles['bridge_vifc']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["bridge_vifc"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to push profile')
            assert False

    def test_verify_vif_state(self, setup_profiles, instantiate_testrail, instantiate_project,
                              test_cases):
        if setup_profiles['bridge_vifs']:
            instantiate_testrail.update_testrail(case_id=test_cases["bridge_vifs"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile pushed successfully')
            time.sleep(100)
            assert setup_profiles['bridge_vifs']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["bridge_vifs"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to push profile')
            time.sleep(100)
            assert False
