import pytest


@pytest.mark.sanity
@pytest.mark.setup_nat
@pytest.mark.nat
@pytest.mark.parametrize(
    'setup_profiles, create_profiles',
    [(["NAT"], ["NAT"])],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.usefixtures("create_profiles")
class TestSetupnat:

    # @pytest.mark.open
    # @pytest.mark.twog
    # def test_setup_open_2g_ssid_profile(self, create_profiles):
    #     try:
    #         assert create_profiles['ssid_2g_open_nat']
    #     except:
    #         assert False
    #
    # @pytest.mark.open
    # @pytest.mark.fiveg
    # def test_setup_open_5g_ssid_profile(self, create_profiles):
    #     try:
    #         assert create_profiles['ssid_5g_open_nat']
    #     except:
    #         assert False

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_setup_wpa_2g_ssid_profile(self, create_profiles, instantiate_testrail, instantiate_project, test_cases):
        if create_profiles['ssid_2g_wpa_nat']:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_2g_wpa_nat"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['ssid_2g_wpa_nat']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_2g_wpa_nat"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to create profile')
            assert False

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_setup_wpa_5g_ssid_profile(self, create_profiles, instantiate_testrail, instantiate_project, test_cases):

        if create_profiles['ssid_5g_wpa_nat']:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_5g_wpa_nat"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['ssid_5g_wpa_nat']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_5g_wpa_nat"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to create profile')
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_setup_wpa2_personal_2g_ssid_profile(self, create_profiles, instantiate_testrail, instantiate_project,
                                                 test_cases):

        if create_profiles['ssid_2g_wpa2_nat']:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_2g_wpa2_nat"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['ssid_2g_wpa2_nat']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_2g_wpa2_nat"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to create profile')
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_setup_wpa2_personal_5g_ssid_profile(self, create_profiles, instantiate_testrail, instantiate_project,
                                                 test_cases):

        if create_profiles['ssid_5g_wpa2_nat']:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_5g_wpa2_nat"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['ssid_5g_wpa2_nat']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_5g_wpa2_nat"], run_id=instantiate_project,
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

        if create_profiles['ssid_2g_eap_nat']:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_2g_eap_nat"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['ssid_2g_eap_nat']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_2g_eap_nat"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to create profile')
            assert False

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.radius
    def test_setup_wpa2_enterprise_5g_ssid_profile(self, create_profiles, instantiate_testrail, instantiate_project,
                                                   test_cases):

        if create_profiles['ssid_5g_eap_nat']:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_5g_eap_nat"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['ssid_5g_eap_nat']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["ssid_5g_eap_nat"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to create profile')
            assert False

    def test_setup_equipment_ap_profile(self, create_profiles, instantiate_testrail, instantiate_project,
                                        test_cases):

        if create_profiles['ap_nat']:
            instantiate_testrail.update_testrail(case_id=test_cases["ap_nat"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile created successfully')
            assert create_profiles['ap_nat']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["ap_nat"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to create profile')
            assert False

    def test_verify_vif_config(self, setup_profiles, instantiate_testrail, instantiate_project,
                               test_cases):

        if setup_profiles['nat_vifc']:
            instantiate_testrail.update_testrail(case_id=test_cases["nat_vifc"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile pushed successfully')
            assert setup_profiles['nat_vifc']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["nat_vifc"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to push profile')
            assert False

    def test_verify_vif_state(self, setup_profiles, instantiate_testrail, instantiate_project,
                              test_cases):
        if setup_profiles['nat_vifs']:
            instantiate_testrail.update_testrail(case_id=test_cases["nat_vifs"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='profile pushed successfully')
            assert setup_profiles['nat_vifs']
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["nat_vifs"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Failed to push profile')
            assert False
