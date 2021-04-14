import pytest


@pytest.mark.sanity
@pytest.mark.wifi_capacity_test
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    'setup_profiles',
    (["BRIDGE"]),
    indirect=True
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeClientConnectivity(object):

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_client_wpa_2g(self, request, get_lanforge_data, setup_profile_data):
        assert True
