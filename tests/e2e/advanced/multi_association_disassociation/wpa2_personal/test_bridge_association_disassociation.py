import pytest
import allure
import os
import time
import pandas as pd
import threading

pytestmark = [pytest.mark.advance, pytest.mark.multiassodisasso, pytest.mark.bridge]

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
class TestMultiAssoDisassoBridge(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5691", name="WIFI-5691")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_2g
    def test_multi_station_udp_upload_2g(self, lf_test, lf_tools):
        allure.attach(name="Definition",
                      body="Multiple association/disassociation stability test intends to measure stability of Wi-Fi device " \
                           "under a dynamic environment with frequent change of connection status.")
        allure.attach(name="Procedure",
                      body="This test case definition states that we Create 16 stations on 2.4Ghz radio and all of these 16 stations should be on same radio." \
                           " Run Wifi-capacity test for first 8 stations. " \
                           "8 stations are picked for sending/receiving packets while the other 8 STAs are picked to do a dis-association/re-association process during the test" \
                           " Enable uplink 4 Mbps UDP flow from DUT to each of the 8 traffic stations" \
                           "Disassociate the other 8 stations. Wait for 30 seconds, after that Re-associate the 8 stations.")
        # run wifi capacity test here
        def thread_fun(station_list):
            print(station_list)
            time.sleep(60)
            lf_tools.admin_up_down(sta_list=station_list, option="down")
            print("stations down")
            time.sleep(10)
            lf_tools.admin_up_down(sta_list=station_list, option="up")
            print("stations up")

        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        print(ssid_name)
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="2G", num_stations=16, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        sta_list = lf_tools.get_station_list()
        print(sta_list)
        lf_tools.admin_up_down(sta_list=sta_list, option="up")

        sel_stations = ",".join(sta_list[0:8])
        val = [['ul_rate_sel: Per-Station Upload Rate:']]
        thr1 = threading.Thread(target=thread_fun, args=(sta_list[8:16],))
        thr1.start()
        wct_obj = lf_test.wifi_capacity(instance_name="udp_upload_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", stations=sel_stations, raw_lines=val, batch_size="8",
                                        upload_rate="4Mbps", protocol="UDP-IPv4", duration="120000", create_stations=False)

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)

        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option="upload")
        print(type(csv_val))
        print(csv_val)
        pass_value = 4 * 0.99
        print("pass value ", pass_value)
        pass_fail = []
        allure.attach(name="Pass Fail Criteria",
                      body="UDP traffic rate is at least 99% of the configured rate for each station. Here configured " \
                           "traffic rate is 4 Mbps so traffic for each station should be 3.96 Mbps ")
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            for i in csv_val.values():
                if i >= pass_value:
                    pass_fail.append(1)
                else:
                    pass_fail.append(0)
            if pass_fail.count(0) == 0:
                print("Test passed successfully")
                allure.attach(name="Csv Data", body=str(csv_val))
                assert True
            else:
                print(" valueTest failed due to lesser")
                allure.attach(name="Csv Data", body=str(csv_val))
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5692", name="WIFI-5692")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_2g
    def test_multi_station_udp_download_2g(self, lf_test, lf_tools):
        allure.attach(name="Definition",
                      body="Multiple association/disassociation stability test intends to measure stability of Wi-Fi device " \
                           "under a dynamic environment with frequent change of connection status.")
        allure.attach(name="Procedure",
                      body="This test case definition states that we Create 16 stations on 2.4Ghz radio and all of these 16 stations should be on same radio." \
                           " Run Wifi-capacity test for first 8 stations. " \
                           "8 stations are picked for sending/receiving packets while the other 8 STAs are picked to do a dis-association/re-association process during the test" \
                           " Enable downlink 4 Mbps UDP flow from DUT to each of the 8 traffic stations" \
                           "Disassociate the other 8 stations. Wait for 30 seconds, after that Re-associate the 8 stations.")
        # run wifi capacity test here
        def thread_fun(station_list):
            print(station_list)
            time.sleep(60)
            lf_tools.admin_up_down(sta_list=station_list, option="down")
            print("stations down")
            time.sleep(10)
            lf_tools.admin_up_down(sta_list=station_list, option="up")
            print("stations up")

        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        print(ssid_name)
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="2G", num_stations=16, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        time.sleep(10)
        sta_list = lf_tools.get_station_list()
        lf_tools.admin_up_down(sta_list=sta_list, option="up")
        sel_stations = ",".join(sta_list[0:8])
        val = [['dl_rate_sel: Per-Station Download Rate:']]
        thr1 = threading.Thread(target=thread_fun, args=(sta_list[8:16],))
        thr1.start()
        wct_obj = lf_test.wifi_capacity(instance_name="udp_download_2g", mode=mode, vlan_id=vlan,
                                        download_rate="4Mbps", stations=sel_stations, raw_lines=val, batch_size="8",
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000",
                                        create_stations=False)

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)

        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option="download")
        print(type(csv_val))
        print(csv_val)
        pass_value = 4 * 0.99
        print("pass value ", pass_value)
        pass_fail = []
        allure.attach(name="Pass Fail Criteria",
                      body="UDP traffic rate is at least 99% of the configured rate for each station. Here configured " \
                           "traffic rate is 4 Mbps so traffic for each station should be 3.96 Mbps ")
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            for i in csv_val.values():
                if i >= pass_value:
                    pass_fail.append(1)
                else:
                    pass_fail.append(0)
            if pass_fail.count(0) == 0:
                print("Test passed successfully")
                allure.attach(name="Csv Data", body=str(csv_val))
                assert True
            else:
                print(" valueTest failed due to lesser")
                allure.attach(name="Csv Data", body=str(csv_val))
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5693", name="WIFI-5693")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_5g
    def test_multi_station_udp_upload_5g(self, lf_test, lf_tools):
        allure.attach(name="Definition",
                      body="Multiple association/disassociation stability test intends to measure stability of Wi-Fi device " \
                           "under a dynamic environment with frequent change of connection status.")
        allure.attach(name="Procedure",
                      body="This test case definition states that we Create 16 stations on 5Ghz radio and all of these 16 stations should be on same radio." \
                           " Run Wifi-capacity test for first 8 stations. " \
                           "8 stations are picked for sending/receiving packets while the other 8 STAs are picked to do a dis-association/re-association process during the test" \
                           " Enable uplink 8 Mbps UDP flow from DUT to each of the 8 traffic stations" \
                           "Disassociate the other 8 stations. Wait for 30 seconds, after that Re-associate the 8 stations.")
        # run wifi capacity test here
        def thread_fun(station_list):
            print(station_list)
            time.sleep(60)
            lf_tools.admin_up_down(sta_list=station_list, option="down")
            print("stations down")
            time.sleep(10)
            lf_tools.admin_up_down(sta_list=station_list, option="up")
            print("stations up")

        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        print(ssid_name)
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="5G", num_stations=16, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        sta_list = lf_tools.get_station_list()
        print(sta_list)
        lf_tools.admin_up_down(sta_list=sta_list, option="up")
        sel_stations = ",".join(sta_list[0:8])
        val = [['ul_rate_sel: Per-Station Upload Rate:']]
        thr1 = threading.Thread(target=thread_fun, args=(sta_list[8:16],))
        thr1.start()
        wct_obj = lf_test.wifi_capacity(instance_name="udp_upload_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", stations=sel_stations, raw_lines=val, batch_size="8",
                                        upload_rate="8Mbps", protocol="UDP-IPv4", duration="120000",
                                        create_stations=False)

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)

        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option="upload")
        print(type(csv_val))
        print(csv_val)
        pass_value = 8 * 0.99
        print("pass value ", pass_value)
        pass_fail = []
        allure.attach(name="Pass Fail Criteria",
                      body="UDP traffic rate is at least 99% of the configured rate for each station. Here configured " \
                           "traffic rate is 8 Mbps so traffic for each station should be 7.92 Mbps ")
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            for i in csv_val.values():
                if i >= pass_value:
                    pass_fail.append(1)
                else:
                    pass_fail.append(0)
            if pass_fail.count(0) == 0:
                print("Test passed successfully")
                allure.attach(name="Csv Data", body=str(csv_val))
                assert True
            else:
                print(" valueTest failed due to lesser")
                allure.attach(name="Csv Data", body=str(csv_val))
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5694", name="WIFI-5694")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_5g
    def test_multi_station_udp_download_5g(self, lf_test, lf_tools):
        allure.attach(name="Definition",
                      body="Multiple association/disassociation stability test intends to measure stability of Wi-Fi device " \
                           "under a dynamic environment with frequent change of connection status.")
        allure.attach(name="Procedure",
                      body="This test case definition states that we Create 16 stations on 5Ghz radio and all of these 16 stations should be on same radio." \
                           " Run Wifi-capacity test for first 8 stations. " \
                           "8 stations are picked for sending/receiving packets while the other 8 STAs are picked to do a dis-association/re-association process during the test" \
                           " Enable downlink 8 Mbps UDP flow from DUT to each of the 8 traffic stations" \
                           "Disassociate the other 8 stations. Wait for 30 seconds, after that Re-associate the 8 stations.")
        # run wifi capacity test here
        def thread_fun(station_list):
            print(station_list)
            time.sleep(60)
            lf_tools.admin_up_down(sta_list=station_list, option="down")
            print("stations down")
            time.sleep(10)
            lf_tools.admin_up_down(sta_list=station_list, option="up")
            print("stations up")

        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        print(ssid_name)
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="5G", num_stations=16, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        sta_list = lf_tools.get_station_list()
        print(sta_list)
        lf_tools.admin_up_down(sta_list=sta_list, option="up")
        sel_stations = ",".join(sta_list[0:8])
        val = [['dl_rate_sel: Per-Station Download Rate:']]
        thr1 = threading.Thread(target=thread_fun, args=(sta_list[8:16],))
        thr1.start()
        wct_obj = lf_test.wifi_capacity(instance_name="udp_download_5g", mode=mode, vlan_id=vlan,
                                        download_rate="8Mbps", stations=sel_stations, raw_lines=val, batch_size="8",
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000",
                                        create_stations=False)

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)

        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option="download")
        print(type(csv_val))
        print(csv_val)
        pass_value = 8 * 0.99
        print("pass value ", pass_value)
        pass_fail = []
        allure.attach(name="Pass Fail Criteria",
                      body="UDP traffic rate is at least 99% of the configured rate for each station. Here configured " \
                           "traffic rate is 8 Mbps so traffic for each station should be 7.92 Mbps ")
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            for i in csv_val.values():
                if i >= pass_value:
                    pass_fail.append(1)
                else:
                    pass_fail.append(0)
            if pass_fail.count(0) == 0:
                print("Test passed successfully")
                allure.attach(name="Csv Data", body=str(csv_val))
                assert True
            else:
                print(" valueTest failed due to lesser")
                allure.attach(name="Csv Data", body=str(csv_val))
                assert False
        print("Test Completed... Cleaning up Stations")


