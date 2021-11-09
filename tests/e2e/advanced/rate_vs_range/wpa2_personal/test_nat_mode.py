"""

    Advanced  Test: Rate v/s Range test under various combinations: NAT Mode
    pytest -m "ratevsrange and NAT " -s -vvv --skip-testrail --testbed=basic-01 --alluredir=../allure_reports
    --> allure serve ../allure_reports/


"""
import os
import time

import pytest
import allure
import os.path
import csv
import pandas as pd

# pytestmark = [pytest.mark.advance, pytest.mark.ratevsrange, pytest.mark.nat]


setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}

@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestRatevsRangeNat(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.client11b
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2495", name="WIFI-2495")
    def test_client_wpa2_personal_2g_11b(self, lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                 get_configuration, lf_tools):
        """

        pytest -m "ratevsrange and client11b" -s -vvv --skip-testrail --testbed=advanced-02
        jira- wifi-2495
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        print("station", station)

        val = [['modes: 802.11b'], ['pkts: 60;142;256;512;1024;MTU;4000;9000'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types:UDP;TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: 1.1.3034'], ['attenuator2: 1.1.3059'],
               ['attenuations: 0..+50..950'], ['attenuations2: 0..+50..950']]
        if station:
            time.sleep(3)
            rvr_o = lf_test.ratevsrange(station_name=station_names_twog, mode=mode,
                                       instance_name="NAT_RVR_11B_TWOG",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            print("report name ", report_name)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries",entries)
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "ratevsrange")


            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)

            kpi_val = lf_tools.read_kpi_file(column_name=None, dir_name=report_name)
            print(str(kpi_val))
            if str(kpi_val) == "empty":
                print("kpi is empty, station did not got ip, Test failed")
                allure.attach(name="Kpi Data", body="station did not got ip Test failed.")
                assert False
            else:
                print("Test passed successfully")
                allure.attach(name="Kpi Data", body=str(kpi_val))
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.client11g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2496", name="WIFI-2496")
    def test_client_wpa2_personal_2g_11g(self,
                                         lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                         get_configuration, lf_tools):
        """

        pytest -m "ratevsrange and NAT and client11g" -s -vvv --skip-testrail --testbed=advanced-02
        jira- wifi-2496
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        print("station", station)

        val = [['modes: 802.11g'], ['pkts: 60;142;256;512;1024;MTU;4000;9000'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types:UDP;TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: 1.1.3034'], ['attenuator2: 1.1.3059'],
               ['attenuations: 0..+50..950'], ['attenuations2: 0..+50..950']]
        if station:
            time.sleep(3)
            rvr_o = lf_test.ratevsrange(station_name=station_names_twog, mode=mode,
                                        instance_name="NAT_RVR_11G_TWOG",
                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "ratevsrange")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            script_dir = os.path.dirname(__file__)  # Script directory
            print(script_dir)
            kpi_val = lf_tools.read_kpi_file(column_name=None, dir_name=report_name)
            print(str(kpi_val))
            if str(kpi_val) == "empty":
                print("kpi is empty, station did not got ip, Test failed")
                allure.attach(name="Kpi Data", body="station did not got ip Test failed.")
                assert False
            else:
                print("Test passed successfully")
                allure.attach(name="Kpi Data", body=str(kpi_val))
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.client11a
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2497", name="WIFI-2497")
    def test_client_wpa2_personal_5g_11a(self,
                                         lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                         get_configuration,lf_tools):
        """

        pytest -m "ratevsrange and NAT and client11a" -s -vvv --skip-testrail --testbed=advanced-02
        jira- wifi-2497
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['modes: 802.11a'], ['pkts: 60;142;256;512;1024;MTU;4000;9000'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types:UDP;TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: 1.1.3034'], ['attenuator2: 1.1.3059'],
               ['attenuations: 0..+50..950'], ['attenuations2: 0..+50..950']]
        if station:
            time.sleep(3)
            rvr_o = lf_test.ratevsrange(station_name=station_names_fiveg, mode=mode,
                                        instance_name="NAT_RVR_11A_FIVEG",
                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "ratevsrange")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            kpi_val = lf_tools.read_kpi_file(column_name=['numeric-score'], dir_name=report_name)
            print(str(kpi_val))
            if str(kpi_val) == "empty":
                print("kpi is empty, station did not got ip, Test failed")
                allure.attach(name="Kpi Data", body="station did not got ip Test failed.")
                assert False
            else:
                print("Test passed successfully")
                allure.attach(name="Kpi Data", body=str(kpi_val))
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.client11an
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2498", name="WIFI-2498")
    def test_client_wpa2_personal_5g_11an(self,
                                         lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                         get_configuration, lf_tools):
        """

        pytest -m "ratevsrange and NAT and client11an" -s -vvv --skip-testrail --testbed=advanced-02
        jira- wifi-2498
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['modes: 802.11an'], ['pkts: 60;142;256;512;1024;MTU;4000;9000'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types:UDP;TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: 1.1.3034'], ['attenuator2: 1.1.3059'],
               ['attenuations: 0..+50..950'], ['attenuations2: 0..+50..950']]
        if station:
            time.sleep(3)
            rvr_o = lf_test.ratevsrange(station_name=station_names_fiveg, mode=mode,
                                        instance_name="NAT_RVR_11AN_FIVEG",
                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "ratevsrange")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            kpi_val = lf_tools.read_kpi_file(column_name=None, dir_name=report_name)
            print(str(kpi_val))
            if str(kpi_val) == "empty":
                print("kpi is empty, station did not got ip, Test failed")
                allure.attach(name="Kpi Data", body="station did not got ip Test failed.")
                assert False
            else:
                print("Test passed successfully")
                allure.attach(name="Kpi Data", body=str(kpi_val))
            assert station
        else:
            assert False

    @pytest.mark.performance_advanced
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.client11ac
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2499", name="WIFI-2499")
    def test_client_wpa2_personal_5g_11ac(self, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration, lf_tools):
        """

        pytest -m "ratevsrange and NAT and client11ac" -s -vvv --skip-testrail --testbed=advanced-02
        jira- wifi-2499
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['modes: 802.11an-AC'], ['pkts: 60;142;256;512;1024;MTU;4000;9000'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types:UDP;TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: 1.1.3034'] ,['attenuator2: 1.1.3059'], ['attenuations: 0..+50..950'],['attenuations2: 0..+50..950']]

        if station:
            time.sleep(3)
            rvr_o = lf_test.ratevsrange(station_name=station_names_fiveg, mode=mode,
                                        instance_name="NAT_RVR_11AC_FIVEG",
                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "ratevsrange")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            kpi_val = lf_tools.read_kpi_file(column_name=None, dir_name=report_name)
            print(str(kpi_val))
            if str(kpi_val) == "empty":
                print("kpi is empty, station did not got ip, Test failed")
                allure.attach(name="Kpi Data", body="station did not got ip Test failed.")
                assert False
            else:
                print("Test passed successfully")
                allure.attach(name="Kpi Data", body=str(kpi_val))
            assert station
        else:
            assert False
