import pytest


# @pytest.mark.sanity
@pytest.mark.wifi_capacity_test
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    'setup_profiles, create_profiles',
    [(["NAT"], ["NAT"])],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.usefixtures("create_profiles")
class TestBridgeModeClientConnectivity(object):

    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.fiveg
    def test_client_wpa_2g(self, get_lanforge_data, setup_profile_data):
        assert True

    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.fiveg
    def test_client_wpa_2g(self, get_lanforge_data, setup_profile_data):
        assert True
