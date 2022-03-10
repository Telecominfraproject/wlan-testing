import time

import pytest
import allure
# from configuration import CONFIGURATION

pytestmark = [pytest.mark.roam_test, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "roam": False,
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {},
    "radius": False
}
@allure.suite("Roam Test with attenuator")
@allure.feature("Roam Test")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
# @allure.step
# def nested_step_allure(bssid, rssi):
#     pass

class TestBasicRoam(object):

    @pytest.mark.roam_5g
    @pytest.mark.bob
    @pytest.mark.wpa2_personal
    def test_basic_roam_5g_to_5g(self, get_configuration, lf_test, lf_reports,  station_names_fiveg, lf_tools, run_lf, add_env_properties,
                           instantiate_profile, get_controller_logs, get_ap_config_slots, get_lf_logs):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        lf_test.basic_roam(run_lf=run_lf, get_configuration=get_configuration, lf_tools=lf_tools,
                           lf_reports=lf_reports,
                           instantiate_profile=instantiate_profile,
                           ssid_name=ssid_name, security=security, security_key=security_key,
                           mode=mode, band=band, station_name=station_names_fiveg, vlan=vlan, test="5g")


    @pytest.mark.multi_roam
    @pytest.mark.wpa2_personal
    def test_multi_roam_5g_to_5g(self,  get_configuration, lf_test, lf_reports,  station_names_fiveg, lf_tools, run_lf, add_env_properties,
                           instantiate_profile, get_controller_logs, get_ap_config_slots, get_lf_logs):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        lf_test.multi_roam(run_lf=run_lf, get_configuration=get_configuration, lf_tools=lf_tools,
                           lf_reports=lf_reports,
                           instantiate_profile=instantiate_profile,
                           ssid_name=ssid_name, security=security, security_key=security_key,
                           mode=mode, band=band, station_name=station_names_fiveg, vlan=vlan, test="5g")

    @pytest.mark.nik
    def test_nikita(self, lf_test, get_configuration, instantiate_profile):
        lf_test.roam_11r(instantiate_profile=instantiate_profile, get_configuration=get_configuration)















































