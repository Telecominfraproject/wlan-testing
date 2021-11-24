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
    def test_multi_station_udp_upload_2g(self, lf_test, lf_tools, create_lanforge_chamberview_dut):
        # run wifi capacity test here
        def thread_fun(station_list):
            print(station_list)
            time.sleep(60)
            lf_tools.admin_up_down(sta_list=station_list, option="down")
            print("stations down")
            time.sleep(10)
            lf_tools.admin_up_down(sta_list=station_list, option="up")
            print("stations up")

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

        kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
        print(type(kpi_val))
        print(str(kpi_val))
        val = kpi_val.split(" ")
        print(val)
        pass_value = 32 * 0.999
        print("pass value ", pass_value)
        print(val[12])
        if str(kpi_val) == "empty":
            print("kpi is empty, station did not got ip, Test failed")
            allure.attach(name="Kpi Data", body="station did not got ip Test failed.")
            assert False
        else:

            if float(val[12]) >= float(pass_value):
                print("Test passed successfully")
                allure.attach(name="Kpi Data", body=str(kpi_val))
                assert True
            else:
                print(" valueTest faled due to lesser")
                allure.attach(name="Kpi Data", body=str(kpi_val))
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5692", name="WIFI-5692")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_2g
    def test_multi_station_udp_download_2g(self, lf_test, lf_tools, create_lanforge_chamberview_dut):
        # run wifi capacity test here
        def thread_fun(station_list):
            print(station_list)
            time.sleep(60)
            lf_tools.admin_up_down(sta_list=station_list, option="down")
            print("stations down")
            time.sleep(10)
            lf_tools.admin_up_down(sta_list=station_list, option="up")
            print("stations up")

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
        val = [['dl_rate_sel: Per-Station Download Rate:']]
        thr1 = threading.Thread(target=thread_fun, args=(sta_list[8:16],))
        thr1.start()
        wct_obj = lf_test.wifi_capacity(instance_name="udp_download_2g", mode=mode, vlan_id=vlan,
                                        download_rate="4Mbps", stations=sel_stations, raw_lines=val, batch_size="8",
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000",
                                        create_stations=False)

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)

        kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
        print(type(kpi_val))
        print(str(kpi_val))
        val = kpi_val.split(" ")
        print(val)
        pass_value = 32 * 0.999
        print("pass value ", pass_value)
        print(val[6])
        if str(kpi_val) == "empty":
            print("kpi is empty, station did not got ip, Test failed")
            allure.attach(name="Kpi Data", body="station did not got ip Test failed.")
            assert False
        else:

            if float(val[6]) >= float(pass_value):
                print("Test passed successfully")
                allure.attach(name="Kpi Data", body=str(kpi_val))
                assert True
            else:
                print(" valueTest faled due to lesser")
                allure.attach(name="Kpi Data", body=str(kpi_val))
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5693", name="WIFI-5693")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_5g
    def test_multi_station_udp_upload_5g(self, lf_test, lf_tools, create_lanforge_chamberview_dut):
        # run wifi capacity test here
        def thread_fun(station_list):
            print(station_list)
            time.sleep(60)
            lf_tools.admin_up_down(sta_list=station_list, option="down")
            print("stations down")
            time.sleep(10)
            lf_tools.admin_up_down(sta_list=station_list, option="up")
            print("stations up")

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

        kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
        print(type(kpi_val))
        print(str(kpi_val))
        val = kpi_val.split(" ")
        print(val)
        pass_value = 64 * 0.999
        print("pass value ", pass_value)
        print(val[12])
        if str(kpi_val) == "empty":
            print("kpi is empty, station did not got ip, Test failed")
            allure.attach(name="Kpi Data", body="station did not got ip Test failed.")
            assert False
        else:

            if float(val[12]) >= float(pass_value):
                print("Test passed successfully")
                allure.attach(name="Kpi Data", body=str(kpi_val))
                assert True
            else:
                print(" valueTest faled due to lesser")
                allure.attach(name="Kpi Data", body=str(kpi_val))
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5694", name="WIFI-5694")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_5g
    def test_multi_station_udp_download_5g(self, lf_test, lf_tools, create_lanforge_chamberview_dut):
        # run wifi capacity test here
        def thread_fun(station_list):
            print(station_list)
            time.sleep(60)
            lf_tools.admin_up_down(sta_list=station_list, option="down")
            print("stations down")
            time.sleep(10)
            lf_tools.admin_up_down(sta_list=station_list, option="up")
            print("stations up")

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

        kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
        print(type(kpi_val))
        #print(str(kpi_val))
        print(kpi_val)
        print(kpi_val[0])
        #val = kpi_val.split(" ")
        #print(val)
        pass_value = 64 * 0.999
        print("pass value ", pass_value)
        #print(val[6])
        if not any(kpi_val):
            print("kpi is empty, station did not got ip, Test failed")
            allure.attach(name="Kpi Data", body="station did not got ip Test failed.")
            assert False
        else:

            if float(str(kpi_val[0])[1:-1]) >= float(pass_value):
                print("Test passed successfully")
                allure.attach(name="Kpi Data", body=str(kpi_val))
                assert True
            else:
                print(" valueTest faled due to lesser")
                allure.attach(name="Kpi Data", body=str(kpi_val))
                assert False
        print("Test Completed... Cleaning up Stations")


