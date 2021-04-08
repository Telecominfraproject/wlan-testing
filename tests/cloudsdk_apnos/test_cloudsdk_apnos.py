import time

import pytest
import sys

if 'apnos' not in sys.path:
    sys.path.append(f'../libs/apnos')

if 'cloudsdk_tests' not in sys.path:
    sys.path.append(f'../../libs/cloudsdk')
from cloudsdk import CloudSDK
from configuration_data import TEST_CASES
from apnos import APNOS
from configuration_data import APNOS_CREDENTIAL_DATA


@pytest.mark.profile_push
class TestCloudPush(object):

    @pytest.mark.run(order=10)
    @pytest.mark.bridge
    @pytest.mark.fiveg
    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa2_enterprise
    def test_apnos_profile_push_bridge(self, push_profile):
        assert push_profile

    @pytest.mark.run(order=16)
    @pytest.mark.nat
    @pytest.mark.fiveg
    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa2_enterprise
    def test_apnos_profile_push_nat(self, push_profile):
        assert push_profile

    @pytest.mark.run(order=22)
    @pytest.mark.vlan
    @pytest.mark.fiveg
    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa2_enterprise
    def test_apnos_profile_push_vlan(self, push_profile):
        assert push_profile


@pytest.mark.vif_config_test
class TestCloudVifConfig(object):

    @pytest.mark.run(order=11)
    @pytest.mark.bridge
    def test_vif_config_cloud_bridge(self, get_current_profile_cloud, instantiate_testrail, instantiate_project):
        ap_ssh = APNOS(APNOS_CREDENTIAL_DATA)
        get_current_profile_cloud.sort()
        PASS = False
        for i in range(0, 18):
            vif_config = list(ap_ssh.get_vif_config_ssids())
            vif_config.sort()
            print(vif_config)
            print(get_current_profile_cloud)
            if get_current_profile_cloud == vif_config:
                PASS = True
                break
            time.sleep(10)
        if PASS:
            instantiate_testrail.update_testrail(case_id=TEST_CASES["bridge_vifc"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='Profiles Matched with vif config bridge mode- passed')
        else:
            instantiate_testrail.update_testrail(case_id=TEST_CASES["bridge_vifc"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Profiles does not with vif config bridge mode- failed')
        assert PASS

    @pytest.mark.run(order=17)
    @pytest.mark.nat
    def test_vif_config_cloud_nat(self, get_current_profile_cloud, instantiate_testrail, instantiate_project):
        ap_ssh = APNOS(APNOS_CREDENTIAL_DATA)
        get_current_profile_cloud.sort()
        PASS = False
        for i in range(0, 18):
            vif_config = list(ap_ssh.get_vif_config_ssids())
            vif_config.sort()
            print(vif_config)
            print(get_current_profile_cloud)
            if get_current_profile_cloud == vif_config:
                PASS = True
                break
            time.sleep(10)
        if PASS:
            instantiate_testrail.update_testrail(case_id=TEST_CASES["nat_vifc"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='Profiles Matched with vif config nat mode- passed')
        else:
            instantiate_testrail.update_testrail(case_id=TEST_CASES["nat_vifc"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Profiles does not with vif config nat mode - failed')
        assert PASS

    @pytest.mark.run(order=23)
    @pytest.mark.vlan
    def test_vif_config_cloud_vlan(self, get_current_profile_cloud, instantiate_testrail, instantiate_project):
        ap_ssh = APNOS(APNOS_CREDENTIAL_DATA)
        get_current_profile_cloud.sort()
        PASS = False
        for i in range(0, 18):
            vif_config = list(ap_ssh.get_vif_config_ssids())
            vif_config.sort()
            print(vif_config)
            print(get_current_profile_cloud)
            if get_current_profile_cloud == vif_config:
                PASS = True
                break
            time.sleep(10)
        if PASS:
            instantiate_testrail.update_testrail(case_id=TEST_CASES["vlan_vifc"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='Profiles Matched with vif config vlan mode- passed')
        else:
            instantiate_testrail.update_testrail(case_id=TEST_CASES["vlan_vifc"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Profiles Matched with vif config vlan mode - failed')
        assert PASS


@pytest.mark.vif_state_test
class TestCloudVifState(object):

    @pytest.mark.run(order=12)
    @pytest.mark.bridge
    @pytest.mark.fiveg
    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa2_enterprise
    def test_vif_state_cloud_bridge(self, instantiate_testrail, instantiate_project):
        ap_ssh = APNOS(APNOS_CREDENTIAL_DATA)
        PASS = False
        for i in range(0, 18):
            vif_state = list(ap_ssh.get_vif_state_ssids())
            vif_state.sort()
            vif_config = list(ap_ssh.get_vif_config_ssids())
            vif_config.sort()
            print(vif_config)
            print(vif_state)
            if vif_state == vif_config:
                PASS = True
                break
            time.sleep(10)
        if PASS:
            instantiate_testrail.update_testrail(case_id=TEST_CASES["bridge_vifs"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='vif config mateches with vif state bridge mode - passed')
        else:
            instantiate_testrail.update_testrail(case_id=TEST_CASES["bridge_vifs"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='vif config mateches with vif state bridge mode - failed')
        assert PASS

    @pytest.mark.run(order=18)
    @pytest.mark.nat
    @pytest.mark.fiveg
    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa2_enterprise
    def test_vif_state_cloud_nat(self, instantiate_testrail, instantiate_project):
        ap_ssh = APNOS(APNOS_CREDENTIAL_DATA)
        PASS = False
        for i in range(0, 18):
            vif_state = list(ap_ssh.get_vif_state_ssids())
            vif_state.sort()
            vif_config = list(ap_ssh.get_vif_config_ssids())
            vif_config.sort()
            print(vif_config)
            print(vif_state)
            if vif_state == vif_config:
                PASS = True
                break
            time.sleep(10)
        if PASS:
            instantiate_testrail.update_testrail(case_id=TEST_CASES["nat_vifs"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='vif config mateches with vif state nat mode - passed')
        else:
            instantiate_testrail.update_testrail(case_id=TEST_CASES["nat_vifs"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='vif config mateches with vif state nat mode - failed')
        assert PASS

    @pytest.mark.run(order=24)
    @pytest.mark.vlan
    @pytest.mark.fiveg
    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa2_enterprise
    def test_vif_state_cloud_vlan(self, instantiate_testrail, instantiate_project):
        ap_ssh = APNOS(APNOS_CREDENTIAL_DATA)
        PASS = False
        for i in range(0, 18):
            vif_state = list(ap_ssh.get_vif_state_ssids())
            vif_state.sort()
            vif_config = list(ap_ssh.get_vif_config_ssids())
            vif_config.sort()
            print(vif_config)
            print(vif_state)
            if vif_state == vif_config:
                PASS = True
                break
            time.sleep(10)
        if PASS:
            instantiate_testrail.update_testrail(case_id=TEST_CASES["vlan_vifs"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='vif config mateches with vif state vlan mode - passed')
        else:
            instantiate_testrail.update_testrail(case_id=TEST_CASES["vlan_vifs"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='vif config mateches with vif state vlan mode - failed')
        assert PASS
