import pytest
import allure

pytestmark = [pytest.mark.client_connectivity, pytest.mark.bridge, pytest.mark.configuration, pytest.mark.basic]

setup_params_general = {
    "mode": "BRIDGE",
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


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_client_connectivity',
    [setup_params_general],
    indirect=True,
    scope="package"
)
@pytest.mark.usefixtures("setup_client_connectivity")
class TestBridgeModeConfiguration(object):

    @pytest.mark.open
    @pytest.mark.twog
    @allure.story('open 2.4 GHZ Band')
    def test_open_ssid_2g_config(self, setup_client_connectivity):
        allure.attach(str(setup_client_connectivity["open_2g"]), 'OPEN SSID 2.4 GHz Creation : ')
        assert setup_client_connectivity["open_2g"]

    @pytest.mark.open
    @pytest.mark.fiveg
    @allure.story('open 5 GHZ Band')
    def test_open_ssid_5g_config(self, setup_client_connectivity):
        allure.attach(str(setup_client_connectivity["open_5g"]), 'OPEN SSID 5 GHz Creation : ')
        assert setup_client_connectivity["open_5g"]

    @pytest.mark.wpa
    @pytest.mark.twog
    @allure.story('wpa 2.4 GHZ Band')
    def test_wpa_ssid_2g_config(self, setup_client_connectivity):
        print(setup_client_connectivity)
        allure.attach(str(setup_client_connectivity["wpa_2g"]), 'WPA SSID 2.4 GHz Creation : ')
        assert setup_client_connectivity["wpa_2g"]

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @allure.story('wpa 5 GHZ Band')
    def test_wpa_ssid_5g_config(self, setup_client_connectivity):
        allure.attach(str(setup_client_connectivity["wpa_5g"]), 'WPA SSID 5 GHz Creation : ')
        assert setup_client_connectivity["wpa_5g"]

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    def test_wpa2_personal_ssid_2g_config(self, setup_client_connectivity):
        allure.attach(str(setup_client_connectivity["wpa2_personal_2g"]), 'WPA2 Personal SSID 2.4 GHz Creation : ')
        assert setup_client_connectivity["wpa2_personal_2g"]

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    def test_wpa2_personal_ssid_5g_config(self, setup_client_connectivity):
        allure.attach(str(setup_client_connectivity["wpa2_personal_5g"]), 'WPA2 Personal SSID 5 GHz Creation : ')
        assert setup_client_connectivity["wpa2_personal_5g"]

    @allure.story('equipment AP Configuration')
    def test_equipment_ap_profile_configuration(self, setup_client_connectivity):
        allure.attach(str(setup_client_connectivity["equipment_ap"]), 'Equipment AP Profile Creation : ')
        assert setup_client_connectivity["equipment_ap"]

    @allure.story('Config push from controller to AP')
    def test_verify_vif_config(self, setup_client_connectivity):
        allure.attach(str(setup_client_connectivity["vifc"]), 'Profile Push from Controller to AP : ')
        assert setup_client_connectivity["vifc"]

    @allure.story('Config in VIF State')
    def test_verify_vif_state(self, setup_client_connectivity):
        allure.attach(str(setup_client_connectivity["vifs"]), 'VIF CONFIG AND VIF STATE ARE SAME : ')
        assert setup_client_connectivity["vifs"]


