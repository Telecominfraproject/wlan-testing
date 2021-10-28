import pytest
import allure
import os
import time
import pandas as pd

pytestmark = [pytest.mark.spatialconsistency, pytest.mark.bridge]

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
class Test_SpatialConsistency_Bridge(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5052", name="WIFI-5052")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.nss1
    def test_nss1_wpa2_personal_2g_10db_0degree(self, setup_profiles, lf_tools, lf_test, station_names_twog, create_lanforge_chamberview_dut, get_configuration ):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        print("station", station)
        val = [['modes: Auto'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:UDP'],
               ['bandw_options: AUTO'], ['spatial_streams: 1'], ['attenuator: 1.1.3034'],['attenuator2: 1.1.3059'],
               ['attenuations: 100'],['attenuations2: 100'],['chamber: DUT-Chamber'], ['tt_deg: 0']]
        if station:
            time.sleep(3)
            rvr_o = lf_test.ratevsrange(station_name=station_names_twog, mode=mode,
                                        instance_name="SPATIAL_NSS1_RVR1",
                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            print("report name ", report_name)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            lf_tools.attach_report_graphs(report_name=report_name,
                                              pdf_name="Rate vs Range Test - UDP 2.4G")
            kpi = False
            for i in entries:
                if "kpi.csv" in i:
                    kpi = i
            if kpi:
                allure.attach.file(source="../reports/" + report_name + "/" + kpi,
                                   name="kpi.csv")

            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)

            kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
            print(type(kpi_val))
            print(str(kpi_val))
            val = kpi_val.split(" ")
            print(val)
            #print(type(val))
            print(val[5])
            if str(kpi_val) == "empty":
                print("kpi is empty, station did not got ip, Test failed")
                allure.attach(name="Kpi Data", body="station did not got ip Test failed.")
                assert False
            else:
                if float(val[5]) > float(45):
                    print("Test passed successfully")
                    allure.attach(name="Kpi Data", body=str(kpi_val))
                    assert True
                else :
                    print(" valueTest faled due to lesser")
                    allure.attach(name="Kpi Data", body=str(kpi_val))
                    assert False
        else:
            print("test failed due to no station ip")
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5070", name="WIFI-5070")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.nss2
    def test_nss2_wpa2_personal_2g_10db_0degree(self, setup_profiles, lf_tools, lf_test, station_names_twog,
                                                create_lanforge_chamberview_dut, get_configuration):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        print("station", station)
        val = [['modes: Auto'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:UDP'],
               ['bandw_options: AUTO'], ['spatial_streams: 2'], ['attenuator: 1.1.3034'], ['attenuator2: 1.1.3059'],
               ['attenuations: 100'], ['attenuations2: 100'], ['chamber: DUT-Chamber'], ['tt_deg: 0']]
        if station:
            time.sleep(3)
            rvr_o = lf_test.ratevsrange(station_name=station_names_twog, mode=mode,
                                        instance_name="SPATIAL_NSS2_RVR1",
                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            print("report name ", report_name)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            lf_tools.attach_report_graphs(report_name=report_name,
                                          pdf_name="Rate vs Range Test - UDP 2.4G")
            kpi = False
            for i in entries:
                if "kpi.csv" in i:
                    kpi = i
            if kpi:
                allure.attach.file(source="../reports/" + report_name + "/" + kpi,
                                   name="kpi.csv")

            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)

            kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
            print(type(kpi_val))
            print(str(kpi_val))
            val = kpi_val.split(" ")
            print(val)
            # print(type(val))
            print(val[5])
            if str(kpi_val) == "empty":
                print("kpi is empty, station did not got ip, Test failed")
                allure.attach(name="Kpi Data", body="station did not got ip Test failed.")
                assert False
            else:
                if float(val[5]) > float(90):
                    print("Test passed successfully")
                    allure.attach(name="Kpi Data", body=str(kpi_val))
                    assert True
                else:
                    print(" valueTest faled due to lesser")
                    allure.attach(name="Kpi Data", body=str(kpi_val))
                    assert False
        else:
            print("test failed due to no station ip")
            assert False
