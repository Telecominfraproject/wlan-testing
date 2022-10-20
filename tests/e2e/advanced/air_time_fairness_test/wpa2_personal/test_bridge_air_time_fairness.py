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
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@allure.feature("Air Time Fairness Test")
@allure.parent_suite("Air Time Fairness Test")
@allure.suite("BRIDGE Mode")
@allure.sub_suite("WPA2 Personal Security")
@pytest.mark.usefixtures("setup_configuration")
class TestAtfBridge(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6394", name="WIFI-6394")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.atf_sta1_greenfieldmode_sta2_atten30dB_2g
    @allure.title("Test for station 1 green field mode and station 2 with attenuation 30 dB 2.4 GHz")
    def test_atf_sta1_greenfieldmode_sta2_atten30dB_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        station_name = station_names_twog[0]
        radio_name1 = lf_tools.twog_radios[0]
        radio_name2 = lf_tools.twog_radios[1]
        sta = []
        for i in range(2):
            sta.append(station_name + str(i))
        print(sta)
        atten_serial = lf_test.attenuator_serial_2g_radio(ssid=ssid_name, passkey=profile_data["security_key"], station_name=station_names_twog, lf_tools_obj=lf_tools)
        atten_serial_split = atten_serial[1].split(".")
        sta_ip1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name1, station_name=sta[0:1], sta_mode=11)
        sta_ip2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name2, station_name=sta[1:2], sta_mode=11)
        if (not sta_ip1) or (not sta_ip2):
            print("test failed due to no station ip")
            assert False
        for i in range(2):
            lf_test.attenuator_modify(int(atten_serial_split[2]), i, 300)
            time.sleep(0.5)
        wct_obj = lf_test.wifi_capacity(instance_name="atf_sta1_greenfieldmode_sta2_atten30dB_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000", sort="linear")
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6395", name="WIFI-6395")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.atf_sta1_greenfieldmode_sta2_legacymode_2g
    @allure.title("Test for station 1 green field mode and station 2 legacy mode 2.4 GHz")
    def test_atf_sta1_greenfieldmode_sta2_legacymode_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        station_name = station_names_twog[0]
        radio_name1 = lf_tools.twog_radios[0]
        radio_name2 = lf_tools.twog_radios[1]
        sta = []
        for i in range(2):
            sta.append(station_name + str(i))
        print(sta)
        sta_ip1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                     radio=radio_name1, station_name=sta[0:1], sta_mode=11)
        sta_ip2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                     radio=radio_name2, station_name=sta[1:2], sta_mode=2)
        if (not sta_ip1) or (not sta_ip2):
            print("test failed due to no station ip")
            assert False
        wct_obj = lf_test.wifi_capacity(instance_name="atf_sta1_greenfieldmode_sta2_legacymode_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000", sort="linear")
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6396", name="WIFI-6396")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.atf_sta1_greenfieldmode_sta2_atten30dB_5g
    @allure.title("Test for station 1 green field mode and station 2 with attenuation 30 dB 5 GHz")
    def test_atf_sta1_greenfieldmode_sta2_atten30dB_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        station_name = station_names_fiveg[0]
        radio_name1 = lf_tools.fiveg_radios[0]
        radio_name2 = lf_tools.fiveg_radios[1]
        sta = []
        for i in range(2):
            sta.append(station_name + str(i))
        print(sta)
        atten_serial = lf_test.attenuator_serial_5g_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                          station_name=station_names_fiveg, lf_tools_obj=lf_tools)
        atten_serial_split = atten_serial[1].split(".")
        sta_ip1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                     radio=radio_name1, station_name=sta[0:1], sta_mode=9)
        sta_ip2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                     radio=radio_name2, station_name=sta[1:2], sta_mode=9)
        if (not sta_ip1) or (not sta_ip2):
            print("test failed due to no station ip")
            assert False
        for i in range(2):
            lf_test.attenuator_modify(int(atten_serial_split[2]), i, 300)
            time.sleep(0.5)
        wct_obj = lf_test.wifi_capacity(instance_name="atf_sta1_greenfieldmode_sta2_atten30dB_5g", mode=mode,
                                        vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000", sort="linear")
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6397", name="WIFI-6397")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.atf_sta1_greenfieldmode_sta2_legacymode_5g
    @allure.title("Test for station 1 green field mode and station 2 legacy mode 5 GHz")
    def test_atf_sta1_greenfieldmode_sta2_legacymode_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        station_name = station_names_fiveg[0]
        radio_name1 = lf_tools.fiveg_radios[0]
        radio_name2 = lf_tools.fiveg_radios[1]
        sta = []
        for i in range(2):
            sta.append(station_name + str(i))
        print(sta)
        sta_ip1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                     radio=radio_name1, station_name=sta[0:1], sta_mode=9)
        sta_ip2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                     radio=radio_name2, station_name=sta[1:2], sta_mode=1)
        if (not sta_ip1) or (not sta_ip2):
            print("test failed due to no station ip")
            assert False
        wct_obj = lf_test.wifi_capacity(instance_name="atf_sta1_greenfieldmode_sta2_legacymode_5g", mode=mode,
                                        vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000", sort="linear")
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
