import pytest
import allure
import os
import time
import pandas as pd

pytestmark = [pytest.mark.ow_regression_lf,
              pytest.mark.ow_sanity_lf,
              pytest.mark.dfs_tests,
              pytest.mark.bandwidth_80MHz]

setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "US",
            "allow-dfs": True,
            "channel-width": 80,
            "channel": 52
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("BRIDGE Mode(80 MHz)")
@allure.sub_suite("Channel-52")
class TestDFSChannel52Bw80(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6376", name="WIFI-6376")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_52_bw_80
    @allure.title("Verify DFS Test of Channel 52 and Bandwidth 80MHz in 5GHz Band")
    def test_dfs_channel_52_bw_80(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                  num_stations, setup_configuration, check_connectivity, get_target_object):
        """
        To verify that a 5G client operating on channel 52 shifts to a non-DFS channel if radar is detected
        Unique Marker: pytest -m "bandwidth_80MHz and ow_sanity_lf and dfs_channel_52_bw_80"
        """
        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)


setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "US",
            "allow-dfs": True,
            "channel-width": 80,
            "channel": 100
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("BRIDGE Mode(80 MHz)")
@allure.sub_suite("Channel-100")
class TestDFSChannel100Bw80(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6311", name="WIFI-6311")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_100_bw_80
    @allure.title("Verify DFS Test of Channel 100 and Bandwidth 80MHz in 5GHz Band")
    def test_dfs_channel_100_bw_80(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                   num_stations, setup_configuration, check_connectivity, get_target_object):
        """
        To verify that a 5G client operating on channel 100 shifts to a non-DFS channel if radar is detected
        Unique Marker: pytest -m "bandwidth_80MHz and ow_sanity_lf and dfs_channel_100_bw_80"
        """
        profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)


setup_params_general11 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "US",
            "allow-dfs": True,
            "channel-width": 80,
            "channel": 132
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general11],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("DFS Test")
@allure.parent_suite("DFS Test")
@allure.suite("BRIDGE Mode(80 MHz)")
@allure.sub_suite("Channel-132")
class TestDFSChannel132Bw80(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6384", name="WIFI-6384")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_132_bw_80
    @allure.title("Verify DFS Test of Channel 132 and Bandwidth 80MHz in 5GHz Band")
    def test_dfs_channel_132_bw_80(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                   num_stations, setup_configuration, check_connectivity, get_target_object):
        """
        To verify that a 5G client operating on channel 132 shifts to a non-DFS channel if radar is detected
        Unique Marker: pytest -m "bandwidth_80MHz and ow_sanity_lf and dfs_channel_132_bw_80"

        """
        profile_data = setup_params_general11["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)
