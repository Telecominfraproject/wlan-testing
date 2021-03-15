import pytest

@pytest.mark.usefixtures('setup_cloudsdk')
@pytest.mark.usefixtures('update_firmware')
@pytest.mark.nat_mode_client_connectivity
class TestNATModeClientConnectivity(object):

    @pytest.mark.nat_mode_single_client_connectivity
    @pytest.mark.nightly
    @pytest.mark.nightly_nat
    def test_single_client(self, setup_cloudsdk, update_firmware, setup_bridge_profile, disconnect_cloudsdk):
        assert setup_cloudsdk != -1

    @pytest.mark.nat_mode_multi_client_connectivity
    def test_multi_client(self):
        pass

