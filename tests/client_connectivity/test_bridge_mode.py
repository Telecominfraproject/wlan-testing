import pytest


@pytest.mark.usefixtures('setup_cloudsdk')
@pytest.mark.usefixtures('update_firmware')
@pytest.mark.bridge_mode_client_connectivity
class TestBridgeModeClientConnectivity(object):

    @pytest.mark.bridge_mode_single_client_connectivity
    @pytest.mark.nightly
    @pytest.mark.nightly_bridge
    def test_single_client(self, setup_cloudsdk, update_firmware, setup_bridge_mode, disconnect_cloudsdk):
        print("Run Client Connectivity Here - BRIDGE Mode")
        if setup_bridge_mode[0] == setup_bridge_mode[1]:
            assert True
        else:
            assert False


    @pytest.mark.bridge_mode_multi_client_connectivity
    def test_multi_client(self):
        assert 1 == 1
