import pytest

@pytest.mark.usefixtures('setup_cloudsdk')
@pytest.mark.usefixtures('update_firmware')
@pytest.mark.bridge_mode_client_connectivity
class TestBridgeModeClientConnectivity(object):

    @pytest.mark.bridge_mode_single_client_connectivity
    @pytest.mark.nightly
    @pytest.mark.nightly_bridge
    def test_single_client(self, setup_cloudsdk, update_firmware, setup_bridge_profile, disconnect_cloudsdk):
        assert setup_cloudsdk != -1

    @pytest.mark.bridge_mode_multi_client_connectivity
    def test_multi_client(self):
        pass


# """
# Bridge mode:
#     testbed name, customer_id, equipment_id, jfrog-credentials, cloudsdk_tests-credentials, skip-open, skip-wpa, skip-wpa2, skip-radius
#     Create a CloudSDK Instance and verify login
#     Get Equipment by Id
#     upgrade firmware if not latest
#     create bridge mode ssid's
#     LANforge Tests
#
# NAT mode:
#
# """
# """
#
# Cloudsdk and AP Test cases are seperate
#
# Bridge Mode:
#     WPA, WPA2-PERSONAL, WPA2-ENTERPRISE
#     2.4/5, 2.4/5, 2.4/5
# """