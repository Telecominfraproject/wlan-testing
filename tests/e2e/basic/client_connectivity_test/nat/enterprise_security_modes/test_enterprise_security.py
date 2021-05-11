import pytest
import allure

pytestmark = [pytest.mark.client_connectivity, pytest.mark.enterprise, pytest.mark.nat]

setup_params_enterprise = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}],
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}]},

    "rf": {},
    "radius": True
}


@pytest.mark.parametrize(
    'setup_client_connectivity',
    [setup_params_enterprise],
    indirect=True,
    scope="package"
)
@pytest.mark.usefixtures("setup_client_connectivity")
class TestNATModeEnterprise(object):

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    def test_wpa2_enterprise_2g(self,):
        # print(setup_client_connectivity)
        assert "setup_client_connectivity"

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    def test_wpa2_enterprise_5g(self):
        assert "setup_client_connectivity"

    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    def test_wpa3_enterprise_2g(self):
        # print(setup_client_connectivity)
        assert "setup_client_connectivity"

    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    def test_wpa3_enterprise_5g(self):
        assert "setup_client_connectivity"




