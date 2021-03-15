import pytest

@pytest.mark.usefixtures('setup_cloudsdk')
@pytest.mark.usefixtures('update_firmware')
@pytest.mark.vlan_mode_client_connectivity
class TestVLANModeClientConnectivity(object):

    @pytest.mark.vlan_mode_single_client_connectivity
    @pytest.mark.nightly
    @pytest.mark.nightly_vlan
    def test_single_client(self, setup_cloudsdk, update_firmware, setup_bridge_profile, disconnect_cloudsdk):
        assert setup_cloudsdk != -1

    @pytest.mark.vlan_mode_multi_client_connectivity
    def test_multi_client(self):
        pass

