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
    "disable_data_rate":True,
    "radius": False
}


@allure.suite("Data Rates")
@allure.feature("Data Rates Test")
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

class TestDataRates(object):

    @pytest.mark.sixg
    @pytest.mark.wpa2_personal
    @pytest.mark.data_rate
    def test_data_rates_fiveg(self,get_configuration, lf_test,disabled_data_rate,
                                                          station_names_fiveg, lf_tools,
                                                          instantiate_ap_profile,
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
        check_pass_fail=lf_test.verify_disabled_data_rates(instantiate_profile,instantiate_ap_profile, get_configuration,
                                                    ssid=ssid_name, password=security_key, disabled_data_rate=disabled_data_rate,
                                                    security=security_type,
                                                    station_list=station_names_fiveg, test_dur=test_duration,
                                                    band=band)
        if check_pass_fail >0:
            assert False
        elif check_pass_fail == 0:
            assert True
