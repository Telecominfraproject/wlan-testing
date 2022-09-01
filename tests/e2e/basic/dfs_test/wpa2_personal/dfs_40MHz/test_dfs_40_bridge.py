import pytest
import allure
import os
import time
import pandas as pd

pytestmark = [pytest.mark.ow_regression_lf,
              pytest.mark.dfs_tests,
              pytest.mark.bandwidth_40MHz]

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
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 40,
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
@allure.parent_suite("OpenWifi DFS Test")
@allure.suite("BRIDGE Mode(40 MHz)")
@allure.sub_suite("Channel-52")
class TestDFSChannel52Bw40(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6209", name="WIFI-6209")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_52_bw_40
    @allure.title("Test for Channel 52 and bandwidth 40")
    def test_dfs_channel_52_bw_40(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                  num_stations, setup_configuration, get_target_object):
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
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 40,
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
@allure.parent_suite("OpenWifi DFS Test")
@allure.suite("BRIDGE Mode(40 MHz)")
@allure.sub_suite("Channel-100")
class TestDFSChannel100Bw40(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6310", name="WIFI-6310")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_100_bw_40
    @allure.title("Test for Channel 100 and bandwidth 40")
    def test_dfs_channel_100_bw_40(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                   num_stations, setup_configuration, get_target_object):
        profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        vlan = 1
        get_test_library.dfs_test(ssid=ssid_name, security=security,
                                  passkey=security_key, mode=mode, band=band,
                                  num_sta=1, dut_data=setup_configuration, tip_2x_obj=get_target_object)
        get_target_object.reboot()
        time.sleep(200)


setup_params_general5 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 40,
            "channel": 60
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.parent_suite("OpenWifi DFS Test")
@allure.suite("BRIDGE Mode(40 MHz)")
@allure.sub_suite("Channel-60")
class TestDFSChannel60Bw40(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6315", name="WIFI-6315")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_60_bw_40
    @allure.title("Test for Channel 60 and bandwidth 40")
    def test_dfs_channel_60_bw_40(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                  num_stations, setup_configuration, get_target_object):
        profile_data = setup_params_general5["ssid_modes"]["wpa2_personal"][0]
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


setup_params_general7 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 40,
            "channel": 108
        }
    },
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general7],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.parent_suite("OpenWifi DFS Test")
@allure.suite("BRIDGE Mode(40 MHz)")
@allure.sub_suite("Channel-108")
class TestDFSChannel108Bw40(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6317", name="WIFI-6317")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_108_bw_40
    @allure.title("Test for Channel 108 and bandwidth 40")
    def test_dfs_channel_108_bw_40(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                   num_stations, setup_configuration, get_target_object):
        profile_data = setup_params_general7["ssid_modes"]["wpa2_personal"][0]
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
            "country": "CA",
            "allow-dfs": True,
            "channel-mode": "VHT",
            "channel-width": 40,
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
@allure.parent_suite("OpenWifi DFS Test")
@allure.suite("BRIDGE Mode(40 MHz)")
@allure.sub_suite("Channel-132")
class TestDFSChannel132Bw40(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6321", name="WIFI-6321")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_132_bw_40
    @allure.title("Test for Channel 132 and bandwidth 40")
    def test_dfs_channel_132_bw_40(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                   num_stations, setup_configuration, get_target_object):
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
