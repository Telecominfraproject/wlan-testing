import pytest
import allure

pytestmark = [pytest.mark.client_connectivity, pytest.mark.vlan, pytest.mark.configuration]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["is2dot4GHz"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
                 "security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_client_connectivity',
    [setup_params_general],
    indirect=True,
    scope="package"
)
@pytest.mark.usefixtures("setup_client_connectivity")
class TestVLANModeConnectivity(object):


    @pytest.mark.open
    @pytest.mark.twog
    @allure.story('open 2.4 GHZ Band')
    def test_open_ssid_2g(self, setup_client_connectivity):
        ssid_data = setup_params_general["ssid_modes"]["open"][0]
        allure.attach(str(setup_client_connectivity), 'Hello, World')
        assert setup_client_connectivity

    @pytest.mark.open
    @pytest.mark.fiveg
    @allure.story('open 5 GHZ Band')
    def test_open_ssid_5g(self, setup_client_connectivity):
        ssid_data = setup_params_general["ssid_modes"]["open"][1]
        assert setup_client_connectivity

    @pytest.mark.wpa
    @pytest.mark.twog
    @allure.story('wpa 2.4 GHZ Band')
    def test_wpa_ssid_2g(self, setup_client_connectivity):
        ssid_data = setup_params_general["ssid_modes"]["wpa"][0]
        print(setup_client_connectivity)
        assert setup_client_connectivity

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @allure.story('wpa 5 GHZ Band')
    def test_wpa_ssid_5g(self, setup_client_connectivity):
        ssid_data = setup_params_general["ssid_modes"]["wpa"][1]
        assert setup_client_connectivity

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    def test_wpa2_personal_ssid_2g(self, setup_client_connectivity):
        ssid_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        print(setup_client_connectivity)
        assert setup_client_connectivity

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    def test_wpa2_personal_ssid_5g(self, setup_client_connectivity):
        ssid_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        assert setup_client_connectivity

