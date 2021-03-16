import pytest

@pytest.mark.usefixtures('setup_cloudsdk')
@pytest.mark.usefixtures('update_firmware')
@pytest.mark.nat_mode_client_connectivity
class TestNATModeClientConnectivity(object):

    @pytest.mark.nat_mode_single_client_connectivity
    @pytest.mark.nightly
    @pytest.mark.nightly_nat
    def test_single_client(self, setup_cloudsdk, update_firmware, setup_nat_mode, disconnect_cloudsdk):
        print("Run Client Connectivity Here - NAT Mode")
        if setup_nat_mode[0] == setup_nat_mode[1]:
            assert True
        else:
            assert False

    @pytest.mark.nat_mode_multi_client_connectivity
    def test_multi_client(self):
        pass

