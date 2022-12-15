"""

    Test Rate v/s Range : Bridge Mode
    pytest -m "rate_vs_range"
"""
import os
import time
import pytest
import allure
import os.path
import logging

pytestmark = [pytest.mark.advance, pytest.mark.rate_vs_range, pytest.mark.bridge]


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

@allure.feature("BRIDGE MODE RATE VS RANGE")
@allure.parent_suite("RATE VS RANGE")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="WPA2_personal RATE VS RANGE")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.Mhz20
class Test_RatevsRange_Bridge(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tarun2
    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("Bridge Mode Rate vs Range Test 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2495", name="WIFI-2495")
    def test_rvr_bridge_wpa2_personal_2g(self, setup_configuration, get_test_library, num_stations,
                                          get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        logging.info("Cleanup existing clients and traffic")
        chamber_view_obj, dut_name = get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        station_names_twog = get_test_library.twog_prefix
        station = get_test_library.client_connect(ssid=ssid_name, security=security,passkey=security_key, mode=mode,
                                                  band=band, num_sta=1, vlan_id=vlan, dut_data=setup_configuration)
        ser_no = get_test_library.attenuator_serial()
        print(ser_no)
        atn2 = ser_no[1].split(".")[2]
        print(f"antenuation-2 : {atn2}")
        # for i in range(4):
        #     lf_test.attenuator_modify(int(atn2), i, 955)
        #     time.sleep(0.5)
        val = [['modes: Auto'], ['pkts: MTU'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types:;TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: 2'], ['attenuator: ' + str(ser_no[0])], ['attenuator2: ' + str(ser_no[1])],
               ['attenuations: 0 100 210..+30..630'], ['attenuations2: 0 100 210..+30..630'], ['chamber: 0'], ['tt_deg: 0']]
        if station:
            rvr_o = get_test_library.rate_vs_range_test(station_name=station_names_twog, mode=mode, download_rate="100%",
                                                        duration='60000',instance_name="MODEBRIDGE_RVR_TWOG",vlan_id=vlan,
                                                        dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            print("report name ", report_name)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries",entries)
            get_test_library.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            print("Test Completed... Cleaning up Stations")
            get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            kpi = "kpi.csv"
            pass_value = {"strong": 100, "medium": 95, "weak": 14}
            atn = [0, 10, 21, 24, 27,30,33,36,39,42,45,48,51,54,57,60,63]
            if kpi in entries:
                kpi_val = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
                print(kpi_val)
                if str(kpi_val) == "empty":
                    print("Throughput value from kpi.csv is empty, Test failed")
                    allure.attach(name="CSV Data", body="Throughput value from kpi.csv is empty, Test failed")
                    assert False, "Throughput value from kpi.csv is empty, Test failed"
                else:
                    allure.attach(name="CSV Data", body="Throughput value : " + str(kpi_val))
                    start, thrpt_val, pass_fail = 0, {}, []
                    for i in pass_value:
                        # count = 0
                        direction = "DUT-TX"
                        for j in range(start, len(kpi_val), len(atn)):
                            thrpt_val[f"{atn[start]}--{direction}"] = kpi_val[j][0]
                            if kpi_val[j][0] >= pass_value[i]:
                                pass_fail.append("PASS")
                            else:
                                pass_fail.append("FAIL")
                            # count += 1
                            direction = "DUT-RX"
                        start += 7
                    print(pass_fail,"\nThroughput value-->",thrpt_val)
                    if "FAIL" in pass_fail:
                        print("Test failed due to lesser value")
                        assert False, "Test failed due to lesser value"
                    else:
                        print("Test passed successfully")
                        assert True
            else:
                print("csv file does not exist, Test failed")
                allure.attach(name="CSV Data", body="csv file does not exist")
                assert False, "csv file does not exist"
        else:
            print("Test failed due to no station ip")
            assert False, "Test failed due to no station ip"

    @pytest.mark.performance_advanced
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tarun2
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("Bridge Mode Rate vs Range Test 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2499", name="WIFI-2499")
    def test_rvr_bridge_wpa2_personal_5g(self, setup_configuration, get_test_library, num_stations,
                                          get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        logging.info("Cleanup existing clients and traffic")
        chamber_view_obj, dut_name = get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        station_names_fiveg = get_test_library.fiveg_prefix
        station = get_test_library.client_connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)
        ser_no = get_test_library.attenuator_serial()
        print(ser_no)
        atn2 = ser_no[1].split(".")[2]
        print(f"antenuation-2 : {atn2}")
        # for i in range(4):
        #     lf_test.attenuator_modify(int(atn2), i, 955)
        #     time.sleep(0.5)
        val = [['modes: 802.11an-AC'], ['pkts: MTU'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types:TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: 2'], ['attenuator: ' + str(ser_no[0])], ['attenuator2: '+ str(ser_no[1])],
               ['attenuations: 0 100 210..+30..540'],['attenuations2: 0 100 210..+30..540'],['chamber: 0'], ['tt_deg: 0']]

        if station:
            time.sleep(3)
            rvr_o = get_test_library.rate_vs_range_test(station_name=station_names_fiveg, mode=mode,download_rate="100%",
                                                        duration='60000',instance_name="MODEBRIDGE_RVR_FIVEG",vlan_id=vlan,
                                                        dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            print("report name ", report_name)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            get_test_library.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            print("Test Completed... Cleaning up Stations")
            get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            kpi = "kpi.csv"
            pass_value = {"strong": 560, "medium": 220, "weak": 5}
            atn = [0, 10, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54]
            if kpi in entries:
                kpi_val = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
                print(kpi_val)
                if str(kpi_val) == "empty":
                    print("Throughput value from kpi.csv is empty, Test failed")
                    allure.attach(name="CSV Data", body="Throughput value from kpi.csv is empty, Test failed")
                    assert False, "Throughput value from kpi.csv is empty, Test failed"
                else:
                    allure.attach(name="CSV Data", body="Throughput value : " + str(kpi_val))
                    start, thrpt_val, pass_fail = 0, {}, []
                    for i in pass_value:
                        # count = 0
                        direction = "DUT-TX"
                        for j in range(start, len(kpi_val), len(atn)):
                            thrpt_val[f"{atn[start]}--{direction}"] = kpi_val[j][0]
                            if kpi_val[j][0] >= pass_value[i]:
                                pass_fail.append("PASS")
                            else:
                                pass_fail.append("FAIL")
                            # count += 1
                            direction = "DUT-RX"
                        start += 6
                    print(pass_fail,"\nThroughput value-->",thrpt_val)
                    if "FAIL" in pass_fail:
                        print("Test failed due to lesser value")
                        assert False, "Test failed due to lesser value"
                    else:
                        print("Test passed successfully")
                        assert True
            else:
                print("csv file does not exist, Test failed")
                allure.attach(name="CSV Data", body="csv file does not exist")
                assert False, "csv file does not exist"
        else:
            print("Test failed due to no station ip")
            assert False, "Test failed due to no station ip"
