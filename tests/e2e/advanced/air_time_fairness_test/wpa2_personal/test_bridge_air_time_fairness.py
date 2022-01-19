import pytest
import allure
import os
import time
import pandas as pd

pytestmark = [pytest.mark.advance, pytest.mark.atf, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestAtfBridge(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5733", name="WIFI-5733")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.atf
    def test_air_time_fairness_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        i = attenuator_serial_2g_radio(ssid=ssid_name, passkey=profile_data["security_key"], station_name=station_names_twog)
        print(i)