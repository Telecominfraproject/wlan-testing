import time

import pytest
import allure

# from configuration import CONFIGURATION

pytestmark = [pytest.mark.gtk_rotation_with_multicast_test, pytest.mark.bridge]
setup_params_general = {
    "mode": "BRIDGE",
    "roam": False,
    "ft+psk": False,
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "mcast2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "mcast5g", "appliedRadios": ["5G"], "security_key": "something"}]
    },
    "rf": {},
    "gtk_interval_in_sec": True,
    "radius": False
}


@allure.suite("GTK Rotation with Multicast")
@allure.feature("Multicast Test")
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

class TestGTKrotationMulticastwithPowerSave(object):

    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    @pytest.mark.mahesh
    # def test_multicast_with_power_save_fiveg(self, get_configuration, lf_test, lf_reports, station_names_fiveg,
    #                                          lf_tools,
    #                                          run_lf,
    #                                          add_env_properties,
    #                                          instantiate_profile, get_controller_logs, get_ap_config_slots,
    #                                          get_lf_logs):
    def test_gtk_rotation_multicast_with_power_save_fiveg(self,gtk_interval, get_configuration, lf_test,
                                                          station_names_fiveg, lf_tools,
                                                          run_lf,test_duration,
                                                          add_env_properties,
                                                          instantiate_profile, get_controller_logs, get_ap_config_slots,
                                                          get_lf_logs):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security_type = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        gtk_eap_interval = gtk_interval
        lf_test.verify_gtk_with_multicast_powersave(instantiate_profile, get_configuration, gtk_eap_interval,
                                                    ssid=ssid_name, password=security_key, security=security_type,
                                                    station_list=station_names_fiveg, test_dur=test_duration,
                                                    band=band)

    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    # def test_multicast_with_power_save_fiveg(self, get_configuration, lf_test, lf_reports, station_names_fiveg,
    #                                          lf_tools,
    #                                          run_lf,
    #                                          add_env_properties,
    #                                          instantiate_profile, get_controller_logs, get_ap_config_slots,
    #                                          get_lf_logs):
    def test_gtk_rotation_multicast_with_power_save_twog(self, gtk_interval, get_configuration, lf_test,
                                                         station_names_twog, lf_tools,
                                                         run_lf,test_duration,
                                                         add_env_properties,
                                                         instantiate_profile, get_controller_logs, get_ap_config_slots,
                                                         get_lf_logs):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security_type = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        gtk_eap_interval = gtk_interval
        lf_test.verify_gtk_with_multicast_powersave(instantiate_profile, get_configuration, gtk_eap_interval,
                                                    ssid=ssid_name,
                                                    password=security_key, security=security_type,
                                                    station_list=station_names_twog, test_dur=test_duration,
                                                    band=band)
