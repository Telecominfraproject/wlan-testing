import pytest
import allure
import os
import time
import pandas as pd

pytestmark = [pytest.mark.dfs, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "dfs":{
        "channel": 52,
        "channel_bandwidth": 20
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

class TestDFS(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5733", name="WIFI-5733")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_60
    def test_dfs(self, lf_test, lf_tools, station_names_fiveg, dfs_start):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        vlan = 1
        print("station_names_fiveg :", station_names_fiveg)
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)
        channel1 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
        print("channel before dfs: ", channel1)
        dfs_start.dfs()
        time.sleep(10)
        channel2 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
        log = dfs_start.dfs_logread()
        if channel1 is not channel2:
            print(log)
            print("channel after dfs: ", channel2)
            allure.attach(name="log Data", body=log)
        else:
            print(log)
            print("dfs not happened")
            allure.attach(name="log Data", body=log)

        dfs_start.reboot()
        connected, latest, active = dfs_start.get_ucentral_status()
        while(not connected):
            print("In while")
            connected, latest, active = dfs_start.get_ucentral_status()



