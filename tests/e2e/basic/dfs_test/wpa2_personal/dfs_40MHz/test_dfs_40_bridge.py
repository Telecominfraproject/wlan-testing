import pytest
import allure
import os
import time
import pandas as pd

pytestmark = [pytest.mark.ow_regression_lf,
              pytest.mark.ow_dfs_tests_lf,
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
    'setup_profiles',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")

class TestDFSChannel52Bw40(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6209", name="WIFI-6209")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_52_bw_40
    def test_dfs_channel_52_bw_40(self, lf_test, lf_tools, station_names_fiveg, dfs_start):
        lf_tools.reset_scenario()
        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        channel = setup_params_general1["rf"]["5G"]["channel"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        vlan = 1
        dfs_fail = True
        print("station_names_fiveg :", station_names_fiveg)
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)
        channel1 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
        print("channel before dfs: ", channel1)
        if channel1 == str(channel):
            dfs_start.dfs()
            time.sleep(15)
        else:
            print("Station not connected to applied channel")
            allure.attach(name="log Data", body="Station not connected to applied channel")
            assert False
        channel2 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
        log = dfs_start.dfs_logread()
        if channel1 != channel2:
            print(log)
            print("channel after dfs: ", channel2)
            allure.attach(name="log Data", body=log)
        else:
            print(log)
            print("dfs not happened")
            allure.attach(name="log Data", body=log)
            dfs_fail = False
        dfs_start.reboot()
        time.sleep(200)
        while True:
            connected, latest, active = dfs_start.get_ucentral_status()
            if connected is True:
                print("status is connected after reboot: ", connected)
                break
            time.sleep(1)
        if not dfs_fail:
            assert False

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
    'setup_profiles',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")

class TestDFSChannel100Bw40(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6310", name="WIFI-6310")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_100_bw_40
    def test_dfs_channel_100_bw_40(self, lf_test, lf_tools, station_names_fiveg, dfs_start):
        lf_tools.reset_scenario()
        profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        channel = setup_params_general2["rf"]["5G"]["channel"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        vlan = 1
        dfs_fail = True
        print("station_names_fiveg :", station_names_fiveg)
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)
        channel1 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
        print("channel before dfs: ", channel1)
        if channel1 == str(channel):
            dfs_start.dfs()
            time.sleep(15)
        else:
            print("Station not connected to applied channel")
            allure.attach(name="log Data", body="Station not connected to applied channel")
            assert False
        channel2 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
        log = dfs_start.dfs_logread()
        if channel1 != channel2:
            print(log)
            print("channel after dfs: ", channel2)
            allure.attach(name="log Data", body=log)
        else:
            print(log)
            print("dfs not happened")
            allure.attach(name="log Data", body=log)
            dfs_fail = False
        dfs_start.reboot()
        time.sleep(200)
        while True:
            connected, latest, active = dfs_start.get_ucentral_status()
            if connected is True:
                print("status is connected after reboot: ", connected)
                break
            time.sleep(1)
        if not dfs_fail:
            assert False

# setup_params_general3 = {
#     "mode": "BRIDGE",
#     "ssid_modes": {
#         "wpa2_personal": [
#             {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
#         ]
#     },
#     "dfs": {
#         "channel": 104,
#         "channel_bandwidth": 40
#     },
#     "rf": {},
#     "radius": False
# }
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general3],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")
#
# class TestDFSChannel104Bw40(object):
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6312", name="WIFI-6312")
#     @pytest.mark.wpa2_personal
#     @pytest.mark.fiveg
#     @pytest.mark.dfs_channel_104_bw_40
#     def test_dfs_channel_104_bw_40(self, lf_test, lf_tools, station_names_fiveg, dfs_start):
#         lf_tools.reset_scenario()
#         profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][0]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         channel = setup_params_general3["dfs"]["channel"]
#         security = "wpa2"
#         band = "fiveg"
#         mode = "BRIDGE"
#         vlan = 1
#         dfs_fail = True
#         print("station_names_fiveg :", station_names_fiveg)
#         station = lf_test.Client_Connect(ssid=ssid_name, security=security,
#                                          passkey=security_key, mode=mode, band=band,
#                                          station_name=station_names_fiveg, vlan_id=vlan)
#         print("station", station)
#         channel1 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         print("channel before dfs: ", channel1)
#         if channel1 == str(channel):
#             dfs_start.dfs()
#             time.sleep(15)
#         else:
#             print("Station not connected to applied channel")
#             allure.attach(name="log Data", body="Station not connected to applied channel")
#             assert False
#         channel2 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         log = dfs_start.dfs_logread()
#         if channel1 != channel2:
#             print(log)
#             print("channel after dfs: ", channel2)
#             allure.attach(name="log Data", body=log)
#         else:
#             print(log)
#             print("dfs not happened")
#             allure.attach(name="log Data", body=log)
#             dfs_fail = False
#         dfs_start.reboot()
#         time.sleep(200)
#         while True:
#             connected, latest, active = dfs_start.get_ucentral_status()
#             if connected is True:
#                 print("status is connected after reboot: ", connected)
#                 break
#             time.sleep(1)
#         if not dfs_fail:
#             assert False

# setup_params_general4 = {
#     "mode": "BRIDGE",
#     "ssid_modes": {
#         "wpa2_personal": [
#             {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
#         ]
#     },
#     "dfs": {
#         "channel": 56,
#         "channel_bandwidth": 40
#     },
#     "rf": {},
#     "radius": False
# }
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general4],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")
#
# class TestDFSChannel56Bw40(object):
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6314", name="WIFI-6314")
#     @pytest.mark.wpa2_personal
#     @pytest.mark.fiveg
#     @pytest.mark.dfs_channel_56_bw_40
#     def test_dfs_channel_56_bw_40(self, lf_test, lf_tools, station_names_fiveg, dfs_start):
#         lf_tools.reset_scenario()
#         profile_data = setup_params_general4["ssid_modes"]["wpa2_personal"][0]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         channel = setup_params_general4["dfs"]["channel"]
#         security = "wpa2"
#         band = "fiveg"
#         mode = "BRIDGE"
#         vlan = 1
#         dfs_fail = True
#         print("station_names_fiveg :", station_names_fiveg)
#         station = lf_test.Client_Connect(ssid=ssid_name, security=security,
#                                          passkey=security_key, mode=mode, band=band,
#                                          station_name=station_names_fiveg, vlan_id=vlan)
#         print("station", station)
#         channel1 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         print("channel before dfs: ", channel1)
#         if channel1 == str(channel):
#             dfs_start.dfs()
#             time.sleep(15)
#         else:
#             print("Station not connected to applied channel")
#             allure.attach(name="log Data", body="Station not connected to applied channel")
#             assert False
#         channel2 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         log = dfs_start.dfs_logread()
#         if channel1 != channel2:
#             print(log)
#             print("channel after dfs: ", channel2)
#             allure.attach(name="log Data", body=log)
#         else:
#             print(log)
#             print("dfs not happened")
#             allure.attach(name="log Data", body=log)
#             dfs_fail = False
#         dfs_start.reboot()
#         time.sleep(200)
#         while True:
#             connected, latest, active = dfs_start.get_ucentral_status()
#             if connected is True:
#                 print("status is connected after reboot: ", connected)
#                 break
#             time.sleep(1)
#         if not dfs_fail:
#             assert False

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
    'setup_profiles',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")

class TestDFSChannel60Bw40(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6315", name="WIFI-6315")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_60_bw_40
    def test_dfs_channel_60_bw_40(self, lf_test, lf_tools, station_names_fiveg, dfs_start):
        lf_tools.reset_scenario()
        profile_data = setup_params_general5["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        channel = setup_params_general5["rf"]["5G"]["channel"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        vlan = 1
        dfs_fail = True
        print("station_names_fiveg :", station_names_fiveg)
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)
        channel1 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
        print("channel before dfs: ", channel1)
        if channel1 == str(channel):
            dfs_start.dfs()
            time.sleep(15)
        else:
            print("Station not connected to applied channel")
            allure.attach(name="log Data", body="Station not connected to applied channel")
            assert False
        channel2 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
        log = dfs_start.dfs_logread()
        if channel1 != channel2:
            print(log)
            print("channel after dfs: ", channel2)
            allure.attach(name="log Data", body=log)
        else:
            print(log)
            print("dfs not happened")
            allure.attach(name="log Data", body=log)
            dfs_fail = False
        dfs_start.reboot()
        time.sleep(200)
        while True:
            connected, latest, active = dfs_start.get_ucentral_status()
            if connected is True:
                print("status is connected after reboot: ", connected)
                break
            time.sleep(1)
        if not dfs_fail:
            assert False

# setup_params_general6 = {
#     "mode": "BRIDGE",
#     "ssid_modes": {
#         "wpa2_personal": [
#             {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
#         ]
#     },
#     "dfs": {
#         "channel": 64,
#         "channel_bandwidth": 40
#     },
#     "rf": {},
#     "radius": False
# }
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general6],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")
#
# class TestDFSChannel64Bw40(object):
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6316", name="WIFI-6316")
#     @pytest.mark.wpa2_personal
#     @pytest.mark.fiveg
#     @pytest.mark.dfs_channel_64_bw_40
#     def test_dfs_channel_64_bw_40(self, lf_test, lf_tools, station_names_fiveg, dfs_start):
#         lf_tools.reset_scenario()
#         profile_data = setup_params_general6["ssid_modes"]["wpa2_personal"][0]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         channel = setup_params_general6["dfs"]["channel"]
#         security = "wpa2"
#         band = "fiveg"
#         mode = "BRIDGE"
#         vlan = 1
#         dfs_fail = True
#         print("station_names_fiveg :", station_names_fiveg)
#         station = lf_test.Client_Connect(ssid=ssid_name, security=security,
#                                          passkey=security_key, mode=mode, band=band,
#                                          station_name=station_names_fiveg, vlan_id=vlan)
#         print("station", station)
#         channel1 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         print("channel before dfs: ", channel1)
#         if channel1 == str(channel):
#             dfs_start.dfs()
#             time.sleep(15)
#         else:
#             print("Station not connected to applied channel")
#             allure.attach(name="log Data", body="Station not connected to applied channel")
#             assert False
#         channel2 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         log = dfs_start.dfs_logread()
#         if channel1 != channel2:
#             print(log)
#             print("channel after dfs: ", channel2)
#             allure.attach(name="log Data", body=log)
#         else:
#             print(log)
#             print("dfs not happened")
#             allure.attach(name="log Data", body=log)
#             dfs_fail = False
#         dfs_start.reboot()
#         time.sleep(200)
#         while True:
#             connected, latest, active = dfs_start.get_ucentral_status()
#             if connected is True:
#                 print("status is connected after reboot: ", connected)
#                 break
#             time.sleep(1)
#         if not dfs_fail:
#             assert False

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
    'setup_profiles',
    [setup_params_general7],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")

class TestDFSChannel108Bw40(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6317", name="WIFI-6317")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_108_bw_40
    def test_dfs_channel_108_bw_40(self, lf_test, lf_tools, station_names_fiveg, dfs_start):
        lf_tools.reset_scenario()
        profile_data = setup_params_general7["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        channel = setup_params_general7["rf"]["5G"]["channel"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        vlan = 1
        dfs_fail = True
        print("station_names_fiveg :", station_names_fiveg)
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)
        channel1 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
        print("channel before dfs: ", channel1)
        if channel1 == str(channel):
            dfs_start.dfs()
            time.sleep(15)
        else:
            print("Station not connected to applied channel")
            allure.attach(name="log Data", body="Station not connected to applied channel")
            assert False
        channel2 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
        log = dfs_start.dfs_logread()
        if channel1 != channel2:
            print(log)
            print("channel after dfs: ", channel2)
            allure.attach(name="log Data", body=log)
        else:
            print(log)
            print("dfs not happened")
            allure.attach(name="log Data", body=log)
            dfs_fail = False
        dfs_start.reboot()
        time.sleep(200)
        while True:
            connected, latest, active = dfs_start.get_ucentral_status()
            if connected is True:
                print("status is connected after reboot: ", connected)
                break
            time.sleep(1)
        if not dfs_fail:
            assert False

# setup_params_general8 = {
#     "mode": "BRIDGE",
#     "ssid_modes": {
#         "wpa2_personal": [
#             {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
#         ]
#     },
#     "dfs": {
#         "channel": 120,
#         "channel_bandwidth": 40
#     },
#     "rf": {},
#     "radius": False
# }
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general8],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")
#
# class TestDFSChannel120Bw40(object):
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6318", name="WIFI-6318")
#     @pytest.mark.wpa2_personal
#     @pytest.mark.fiveg
#     @pytest.mark.dfs_channel_120_bw_40
#     def test_dfs_channel_120_bw_40(self, lf_test, lf_tools, station_names_fiveg, dfs_start):
#         lf_tools.reset_scenario()
#         profile_data = setup_params_general8["ssid_modes"]["wpa2_personal"][0]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         channel = setup_params_general8["dfs"]["channel"]
#         security = "wpa2"
#         band = "fiveg"
#         mode = "BRIDGE"
#         vlan = 1
#         dfs_fail = True
#         print("station_names_fiveg :", station_names_fiveg)
#         station = lf_test.Client_Connect(ssid=ssid_name, security=security,
#                                          passkey=security_key, mode=mode, band=band,
#                                          station_name=station_names_fiveg, vlan_id=vlan)
#         print("station", station)
#         channel1 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         print("channel before dfs: ", channel1)
#         if channel1 == str(channel):
#             dfs_start.dfs()
#             time.sleep(15)
#         else:
#             print("Station not connected to applied channel")
#             allure.attach(name="log Data", body="Station not connected to applied channel")
#             assert False
#         channel2 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         log = dfs_start.dfs_logread()
#         if channel1 != channel2:
#             print(log)
#             print("channel after dfs: ", channel2)
#             allure.attach(name="log Data", body=log)
#         else:
#             print(log)
#             print("dfs not happened")
#             allure.attach(name="log Data", body=log)
#             dfs_fail = False
#         dfs_start.reboot()
#         time.sleep(200)
#         while True:
#             connected, latest, active = dfs_start.get_ucentral_status()
#             if connected is True:
#                 print("status is connected after reboot: ", connected)
#                 break
#             time.sleep(1)
#         if not dfs_fail:
#             assert False

# setup_params_general9 = {
#     "mode": "BRIDGE",
#     "ssid_modes": {
#         "wpa2_personal": [
#             {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
#         ]
#     },
#     "dfs": {
#         "channel": 124,
#         "channel_bandwidth": 40
#     },
#     "rf": {},
#     "radius": False
# }
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general9],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")
#
# class TestDFSChannel124Bw40(object):
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6319", name="WIFI-6319")
#     @pytest.mark.wpa2_personal
#     @pytest.mark.fiveg
#     @pytest.mark.dfs_channel_124_bw_40
#     def test_dfs_channel_124_bw_40(self, lf_test, lf_tools, station_names_fiveg, dfs_start):
#         lf_tools.reset_scenario()
#         profile_data = setup_params_general9["ssid_modes"]["wpa2_personal"][0]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         channel = setup_params_general9["dfs"]["channel"]
#         security = "wpa2"
#         band = "fiveg"
#         mode = "BRIDGE"
#         vlan = 1
#         dfs_fail = True
#         print("station_names_fiveg :", station_names_fiveg)
#         station = lf_test.Client_Connect(ssid=ssid_name, security=security,
#                                          passkey=security_key, mode=mode, band=band,
#                                          station_name=station_names_fiveg, vlan_id=vlan)
#         print("station", station)
#         channel1 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         print("channel before dfs: ", channel1)
#         if channel1 == str(channel):
#             dfs_start.dfs()
#             time.sleep(15)
#         else:
#             print("Station not connected to applied channel")
#             allure.attach(name="log Data", body="Station not connected to applied channel")
#             assert False
#         channel2 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         log = dfs_start.dfs_logread()
#         if channel1 != channel2:
#             print(log)
#             print("channel after dfs: ", channel2)
#             allure.attach(name="log Data", body=log)
#         else:
#             print(log)
#             print("dfs not happened")
#             allure.attach(name="log Data", body=log)
#             dfs_fail = False
#         dfs_start.reboot()
#         time.sleep(200)
#         while True:
#             connected, latest, active = dfs_start.get_ucentral_status()
#             if connected is True:
#                 print("status is connected after reboot: ", connected)
#                 break
#             time.sleep(1)
#         if not dfs_fail:
#             assert False

# setup_params_general10 = {
#     "mode": "BRIDGE",
#     "ssid_modes": {
#         "wpa2_personal": [
#             {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
#         ]
#     },
#     "dfs": {
#         "channel": 128,
#         "channel_bandwidth": 40
#     },
#     "rf": {},
#     "radius": False
# }
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general10],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")
#
# class TestDFSChannel128Bw40(object):
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6320", name="WIFI-6320")
#     @pytest.mark.wpa2_personal
#     @pytest.mark.fiveg
#     @pytest.mark.dfs_channel_128_bw_40
#     def test_dfs_channel_128_bw_40(self, lf_test, lf_tools, station_names_fiveg, dfs_start):
#         lf_tools.reset_scenario()
#         profile_data = setup_params_general10["ssid_modes"]["wpa2_personal"][0]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         channel = setup_params_general10["dfs"]["channel"]
#         security = "wpa2"
#         band = "fiveg"
#         mode = "BRIDGE"
#         vlan = 1
#         dfs_fail = True
#         print("station_names_fiveg :", station_names_fiveg)
#         station = lf_test.Client_Connect(ssid=ssid_name, security=security,
#                                          passkey=security_key, mode=mode, band=band,
#                                          station_name=station_names_fiveg, vlan_id=vlan)
#         print("station", station)
#         channel1 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         print("channel before dfs: ", channel1)
#         if channel1 == str(channel):
#             dfs_start.dfs()
#             time.sleep(15)
#         else:
#             print("Station not connected to applied channel")
#             allure.attach(name="log Data", body="Station not connected to applied channel")
#             assert False
#         channel2 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         log = dfs_start.dfs_logread()
#         if channel1 != channel2:
#             print(log)
#             print("channel after dfs: ", channel2)
#             allure.attach(name="log Data", body=log)
#         else:
#             print(log)
#             print("dfs not happened")
#             allure.attach(name="log Data", body=log)
#             dfs_fail = False
#         dfs_start.reboot()
#         time.sleep(200)
#         while True:
#             connected, latest, active = dfs_start.get_ucentral_status()
#             if connected is True:
#                 print("status is connected after reboot: ", connected)
#                 break
#             time.sleep(1)
#         if not dfs_fail:
#             assert False

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
    'setup_profiles',
    [setup_params_general11],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")

class TestDFSChannel132Bw40(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6321", name="WIFI-6321")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dfs_channel_132_bw_40
    def test_dfs_channel_132_bw_40(self, lf_test, lf_tools, station_names_fiveg, dfs_start):
        lf_tools.reset_scenario()
        profile_data = setup_params_general11["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        channel = setup_params_general11["rf"]["5G"]["channel"]
        security = "wpa2"
        band = "fiveg"
        mode = "BRIDGE"
        vlan = 1
        dfs_fail = True
        print("station_names_fiveg :", station_names_fiveg)
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)
        channel1 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
        print("channel before dfs: ", channel1)
        if channel1 == str(channel):
            dfs_start.dfs()
            time.sleep(15)
        else:
            print("Station not connected to applied channel")
            allure.attach(name="log Data", body="Station not connected to applied channel")
            assert False
        channel2 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
        log = dfs_start.dfs_logread()
        if channel1 != channel2:
            print(log)
            print("channel after dfs: ", channel2)
            allure.attach(name="log Data", body=log)
        else:
            print(log)
            print("dfs not happened")
            allure.attach(name="log Data", body=log)
            dfs_fail = False
        dfs_start.reboot()
        time.sleep(200)
        while True:
            connected, latest, active = dfs_start.get_ucentral_status()
            if connected is True:
                print("status is connected after reboot: ", connected)
                break
            time.sleep(1)
        if not dfs_fail:
            assert False

# setup_params_general12 = {
#     "mode": "BRIDGE",
#     "ssid_modes": {
#         "wpa2_personal": [
#             {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
#         ]
#     },
#     "dfs": {
#         "channel": 140,
#         "channel_bandwidth": 40
#     },
#     "rf": {},
#     "radius": False
# }
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general12],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")
#
# class TestDFSChannel140Bw40(object):
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6321", name="WIFI-6321")
#     @pytest.mark.wpa2_personal
#     @pytest.mark.fiveg
#     @pytest.mark.dfs_channel_140_bw_40
#     def test_dfs_channel_140_bw_40(self, lf_test, lf_tools, station_names_fiveg, dfs_start):
#         lf_tools.reset_scenario()
#         profile_data = setup_params_general12["ssid_modes"]["wpa2_personal"][0]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         channel = setup_params_general12["dfs"]["channel"]
#         security = "wpa2"
#         band = "fiveg"
#         mode = "BRIDGE"
#         vlan = 1
#         dfs_fail = True
#         print("station_names_fiveg :", station_names_fiveg)
#         station = lf_test.Client_Connect(ssid=ssid_name, security=security,
#                                          passkey=security_key, mode=mode, band=band,
#                                          station_name=station_names_fiveg, vlan_id=vlan)
#         print("station", station)
#         channel1 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         print("channel before dfs: ", channel1)
#         if channel1 == str(channel):
#             dfs_start.dfs()
#             time.sleep(15)
#         else:
#             print("Station not connected to applied channel")
#             allure.attach(name="log Data", body="Station not connected to applied channel")
#             assert False
#         channel2 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         log = dfs_start.dfs_logread()
#         if channel1 != channel2:
#             print(log)
#             print("channel after dfs: ", channel2)
#             allure.attach(name="log Data", body=log)
#         else:
#             print(log)
#             print("dfs not happened")
#             allure.attach(name="log Data", body=log)
#             dfs_fail = False
#         dfs_start.reboot()
#         time.sleep(200)
#         while True:
#             connected, latest, active = dfs_start.get_ucentral_status()
#             if connected is True:
#                 print("status is connected after reboot: ", connected)
#                 break
#             time.sleep(1)
#         if not dfs_fail:
#             assert False

# setup_params_general13 = {
#     "mode": "BRIDGE",
#     "ssid_modes": {
#         "wpa2_personal": [
#             {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
#         ]
#     },
#     "dfs": {
#         "channel": 144,
#         "channel_bandwidth": 40
#     },
#     "rf": {},
#     "radius": False
# }
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general13],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")
#
# class TestDFSChannel144Bw40(object):
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6322", name="WIFI-6322")
#     @pytest.mark.wpa2_personal
#     @pytest.mark.fiveg
#     @pytest.mark.dfs_channel_144_bw_40
#     def test_dfs_channel_144_bw_40(self, lf_test, lf_tools, station_names_fiveg, dfs_start):
#         lf_tools.reset_scenario()
#         profile_data = setup_params_general13["ssid_modes"]["wpa2_personal"][0]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         channel = setup_params_general13["dfs"]["channel"]
#         security = "wpa2"
#         band = "fiveg"
#         mode = "BRIDGE"
#         vlan = 1
#         dfs_fail = True
#         print("station_names_fiveg :", station_names_fiveg)
#         station = lf_test.Client_Connect(ssid=ssid_name, security=security,
#                                          passkey=security_key, mode=mode, band=band,
#                                          station_name=station_names_fiveg, vlan_id=vlan)
#         print("station", station)
#         channel1 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         print("channel before dfs: ", channel1)
#         if channel1 == str(channel):
#             dfs_start.dfs()
#             time.sleep(15)
#         else:
#             print("Station not connected to applied channel")
#             allure.attach(name="log Data", body="Station not connected to applied channel")
#             assert False
#         channel2 = lf_tools.station_data_query(station_name=station_names_fiveg[0], query="channel")
#         log = dfs_start.dfs_logread()
#         if channel1 != channel2:
#             print(log)
#             print("channel after dfs: ", channel2)
#             allure.attach(name="log Data", body=log)
#         else:
#             print(log)
#             print("dfs not happened")
#             allure.attach(name="log Data", body=log)
#             dfs_fail = False
#         dfs_start.reboot()
#         time.sleep(200)
#         while True:
#             connected, latest, active = dfs_start.get_ucentral_status()
#             if connected is True:
#                 print("status is connected after reboot: ", connected)
#                 break
#             time.sleep(1)
#         if not dfs_fail:
#             assert False