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


class TestCloudPush(object):

    @pytest.mark.run(order=10)
    def test_apnos_profile_push_bridge(self, push_profile):
        if push_profile:
            pass
            # pass
        else:
            pass
            # Fail
        assert push_profile

    @pytest.mark.run(order=16)
    def test_apnos_profile_push_nat(self, push_profile):
        if push_profile:
            pass
            # pass
        else:
            pass
            # Fail
        assert push_profile

    def test_apnos_profile_push_vlan(self, push_profile):
        if push_profile:
            pass
            # pass
        else:
            pass
            # Fail
        assert push_profile


class TestCloudVifConfig(object):

    @pytest.mark.run(order=11)
    @pytest.mark.vif_config_test
    def test_vif_config_cloud_bridge(self, get_current_profile_cloud):
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
        assert PASS

    @pytest.mark.run(order=17)
    def test_vif_config_cloud_nat(self, get_current_profile_cloud):
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
        assert PASS

    def test_vif_config_cloud_vlan(self, create_ap_profile_vlan, instantiate_profile):
        assert True


class TestCloudVifState(object):

    @pytest.mark.run(order=12)
    @pytest.mark.vif_config_test
    def test_vif_state_cloud(self):
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
        assert PASS

    @pytest.mark.run(order=18)
    def test_apnos_profile_push_nat(self):
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
        assert PASS

    def test_apnos_profile_push_vlan(self, create_ap_profile_vlan, instantiate_profile):
        assert True
