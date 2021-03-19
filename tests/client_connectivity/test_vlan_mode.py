import pytest
import time
@pytest.mark.usefixtures('setup_cloudsdk')
@pytest.mark.usefixtures('upgrade_firmware')
class TestVLANModeClientConnectivity(object):

    @pytest.mark.vlan
    @pytest.mark.open
    @pytest.mark.wpa
    @pytest.mark.wpa2
    @pytest.mark.eap
    def test_single_client(self, setup_cloudsdk, upgrade_firmware, setup_vlan_mode, disconnect_cloudsdk):
        print("Run Client Connectivity Here - VLAN Mode")
        time.sleep(30)
        if setup_vlan_mode[0] == setup_vlan_mode[1]:
            assert True
        else:
            assert False


