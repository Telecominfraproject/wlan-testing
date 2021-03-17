import pytest
import time
@pytest.mark.usefixtures('setup_cloudsdk')
@pytest.mark.usefixtures('update_firmware')
@pytest.mark.vlan_mode_client_connectivity
class TestVLANModeClientConnectivity(object):

    @pytest.mark.vlan_mode_single_client_connectivity
    @pytest.mark.nightly
    @pytest.mark.nightly_vlan
    def test_single_client(self, setup_cloudsdk, update_firmware, setup_vlan_mode, disconnect_cloudsdk):
        print("Run Client Connectivity Here - VLAN Mode")
        time.sleep(30)
        if setup_vlan_mode[0] == setup_vlan_mode[1]:
            assert True
        else:
            assert False

    @pytest.mark.vlan_mode_multi_client_connectivity
    def test_multi_client(self):
        pass

