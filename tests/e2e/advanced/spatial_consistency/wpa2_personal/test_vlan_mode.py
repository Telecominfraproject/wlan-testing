"""

    Test Spacial Consistency: Vlan Mode
    pytest -m spatial_consistency
"""

import pytest
import allure
import logging
import os

pytestmark = [pytest.mark.advance, pytest.mark.spatial_consistency, pytest.mark.vlan]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan":100},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan":100}
        ]
    },
    "rf": {
        "5G":{
            "channel-width": 80},
        "2G":{
            "channel-width": 20}
    },
    "radius": False
}
@allure.feature("VLAN MODE SPACIAL CONSISTENCY")
@allure.parent_suite("SPACIAL CONSISTENCY")
@allure.suite(suite_name="VLAN MODE")
@allure.sub_suite(sub_suite_name="WPA2_personal SPACIAL CONSISTENCY")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test_SpatialConsistency_Bridge(object):

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("Vlan Mode Spacial Consistency Test (NSS-1) UDP-Download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5052", name="WIFI-5052")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.nss1
    def test_udp_download_nss1_wpa2_personal_2g(self, setup_configuration, get_test_library, num_stations,
                                          get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        logging.info("Cleanup existing clients and traffic")
        chamber_view_obj, dut_name = get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = 1
        station = get_test_library.client_connect(ssid=ssid_name, security=security,passkey=security_key, mode=mode,
                                                  band=band,num_sta=1, vlan_id=vlan, dut_data=setup_configuration)
        sta_name = list(station.keys())
        ser_no = get_test_library.attenuator_serial()
        print(ser_no)
        val = [['modes: Auto'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:UDP'],
               ['bandw_options: AUTO'], ['spatial_streams: 1'], ['attenuator: ' + str(ser_no[0])], ['attenuator2: ' + str(ser_no[1])],
               ['attenuations: 100 380 480'],['attenuations2: 100 380 480'],['chamber: DUT-Chamber'], ['tt_deg: 0..+60..300']]
        if station:
            rvr_o, report_name = get_test_library.rate_vs_range_test(station_name=sta_name[0], mode=mode, download_rate="100%",
                                                        instance_name="SPATIAL_NSS1_RVR1_TWOG", duration="60000",vlan_id=vlan,
                                                        dut_name=dut_name, raw_lines=val)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            logging.info("Test Completed... Cleaning up Stations")
            kpi = "kpi.csv"
            pass_value = {"strong": 45, "medium": 35, "weak": 17}
            atn, deg = [10, 38, 48], [0, 60, 120, 180, 240, 300]
            if kpi in entries:
                kpi_val = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
                print(kpi_val)
                if str(kpi_val) == "empty":
                    logging.info("TEST FAILED, Throughput value from kpi.csv is empty.")
                    allure.attach(name="CSV Data", body="TEST FAILED, Throughput value from kpi.csv is empty.")
                    assert False, "TEST FAILED, Throughput value from kpi.csv is empty."
                else:
                    allure.attach(name="CSV Data", body="Throughput value : " + str(kpi_val))
                    start, thrpt_val, pass_fail = 0, {}, []
                    for i in pass_value:
                        count = 0
                        for j in range(start, len(kpi_val), len(atn)):
                            thrpt_val[f"{atn[start]}atn-{deg[count]}deg"] = kpi_val[j][0]
                            if kpi_val[j][0] >= pass_value[i]:
                                pass_fail.append("PASS")
                            else:
                                pass_fail.append("FAIL")
                            count += 1
                        # start += 6
                    print(thrpt_val, "\n", pass_fail)
                    if "FAIL" in pass_fail:
                        logging.info("TEST FAILED, Actual throughput is lesser than Expected.")
                        assert False, "TEST FAILED, Actual throughput is lesser than Expected."
                    else:
                        logging.info("Test PASSED successfully")
                        assert True
            else:
                logging.info("csv file does not exist, Test failed")
                allure.attach(name="CSV Data", body="csv file does not exist")
                assert False, "csv file does not exist"
        else:
            logging.info("TEST FAILED,due to no station ip")
            assert False, "TEST FAILED,due to no station ip"

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("Vlan Mode Spacial Consistency Test (NSS-2) UDP-Download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5068", name="WIFI-5068")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.nss2
    def test_udp_download_nss2_wpa2_personal_2g(self,setup_configuration, get_test_library, num_stations,
                                          get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        logging.info("Cleanup existing clients and traffic")
        chamber_view_obj, dut_name = get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = 1
        station = get_test_library.client_connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                  band=band, num_sta=1, vlan_id=vlan, dut_data=setup_configuration)
        sta_name = list(station.keys())
        ser_no = get_test_library.attenuator_serial()
        print(ser_no)
        val = [['modes: Auto'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:UDP'],
               ['bandw_options: AUTO'], ['spatial_streams: 2'], ['attenuator: ' + str(ser_no[0])], ['attenuator2: ' + str(ser_no[1])],
               ['attenuations: 100 380 480'], ['attenuations2: 100 380 480'], ['chamber: DUT-Chamber'], ['tt_deg: 0..+60..300']]
        if station:
            rvr_o, report_name = get_test_library.rate_vs_range_test(station_name=sta_name[0], mode=mode, download_rate="100%",
                                                        instance_name="SPATIAL_NSS2_RVR1_TWOG",duration="60000",vlan_id=vlan,
                                                        dut_name=dut_name,raw_lines=val)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            logging.info("Test Completed... Cleaning up Stations")
            kpi = "kpi.csv"
            pass_value = {"strong": 90, "medium": 70, "weak": 35}
            atn, deg = [10, 38, 48], [0, 60, 120, 180, 240, 300]
            if kpi in entries:
                kpi_val = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
                print(kpi_val)
                if str(kpi_val) == "empty":
                    logging.info("TEST FAILED, Throughput value from kpi.csv is empty.")
                    allure.attach(name="CSV Data", body="TEST FAILED, Throughput value from kpi.csv is empty.")
                    assert False, "TEST FAILED, Throughput value from kpi.csv is empty."
                else:
                    allure.attach(name="CSV Data", body="Throughput value : " + str(kpi_val))
                    start, thrpt_val, pass_fail = 0, {}, []
                    for i in pass_value:
                        count = 0
                        for j in range(start, len(kpi_val), len(atn)):
                            thrpt_val[f"{atn[start]}atn-{deg[count]}deg"] = kpi_val[j][0]
                            if kpi_val[j][0] >= pass_value[i]:
                                pass_fail.append("PASS")
                            else:
                                pass_fail.append("FAIL")
                            count += 1
                        # start += 6
                    print(thrpt_val, "\n", pass_fail)
                    if "FAIL" in pass_fail:
                        logging.info("TEST FAILED, Actual throughput is lesser than Expected.")
                        assert False, "TEST FAILED, Actual throughput is lesser than Expected."
                    else:
                        logging.info("Test PASSED successfully")
                        assert True
            else:
                logging.info("csv file does not exist, Test failed")
                allure.attach(name="CSV Data", body="csv file does not exist")
                assert False, "csv file does not exist"
        else:
            logging.info("TEST FAILED,due to no station ip")
            assert False, "TEST FAILED,due to no station ip"

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("Vlan Mode Spacial Consistency Test (NSS-1) UDP-Download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5067", name="WIFI-5067")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.nss1
    def test_udp_download_nss1_wpa2_personal_5g(self, setup_configuration, get_test_library, num_stations,
                                          get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        logging.info("Cleanup existing clients and traffic")
        chamber_view_obj, dut_name = get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data =  {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = 1
        station = get_test_library.client_connect(ssid=ssid_name, security=security,passkey=security_key, mode=mode,
                                                  band=band,num_sta=1, vlan_id=vlan, dut_data=setup_configuration)

        sta_name = list(station.keys())
        ser_no = get_test_library.attenuator_serial()
        print(ser_no)
        val = [['modes: Auto'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:UDP'],
               ['bandw_options: AUTO'], ['spatial_streams: 1'], ['attenuator: ' + str(ser_no[0])], ['attenuator2: ' + str(ser_no[1])],
               ['attenuations: 100 250 350'], ['attenuations2: 100 250 350'], ['chamber: DUT-Chamber'], ['tt_deg: 0..+60..300']]
        if station:
            rvr_o, report_name = get_test_library.rate_vs_range_test(station_name=sta_name[0], mode=mode, download_rate="100%",
                                                        instance_name="SPATIAL_NSS1_RVR1_FIVEG",duration="60000",vlan_id=vlan,
                                                        dut_name=dut_name, raw_lines=val)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            logging.info("Test Completed... Cleaning up Stations")
            kpi = "kpi.csv"
            pass_value = {"strong": 250, "medium": 150, "weak": 75}
            atn, deg = [10, 25, 35], [0, 60, 120, 180, 240, 300]
            if kpi in entries:
                kpi_val = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
                print(kpi_val)
                if str(kpi_val) == "empty":
                    logging.info("TEST FAILED, Throughput value from kpi.csv is empty.")
                    allure.attach(name="CSV Data", body="TEST FAILED, Throughput value from kpi.csv is empty.")
                    assert False, "TEST FAILED, Throughput value from kpi.csv is empty."
                else:
                    allure.attach(name="CSV Data", body="Throughput value : " + str(kpi_val))
                    start, thrpt_val, pass_fail = 0, {}, []
                    for i in pass_value:
                        count = 0
                        for j in range(start, len(kpi_val), len(atn)):
                            thrpt_val[f"{atn[start]}atn-{deg[count]}deg"] = kpi_val[j][0]
                            if kpi_val[j][0] >= pass_value[i]:
                                pass_fail.append("PASS")
                            else:
                                pass_fail.append("FAIL")
                            count += 1
                        # start += 6
                    print(thrpt_val, "\n", pass_fail)
                    if "FAIL" in pass_fail:
                        logging.info("TEST FAILED, Actual throughput is lesser than Expected.")
                        assert False, "TEST FAILED, Actual throughput is lesser than Expected."
                    else:
                        logging.info("Test PASSED successfully")
                        assert True
            else:
                logging.info("csv file does not exist, Test failed")
                allure.attach(name="CSV Data", body="csv file does not exist")
                assert False, "csv file does not exist"
        else:
            logging.info("TEST FAILED,due to no station ip")
            assert False, "TEST FAILED,due to no station ip"

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("Vlan Mode Spacial Consistency Test (NSS-2) UDP-Download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5066", name="WIFI-5066")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.nss2
    def test_udp_download_nss2_wpa2_personal_5g(self, setup_configuration, get_test_library, num_stations,
                                          get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        logging.info("Cleanup existing clients and traffic")
        chamber_view_obj, dut_name = get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = 1
        station = get_test_library.client_connect(ssid=ssid_name, security=security,passkey=security_key, mode=mode,
                                                  band=band,num_sta=1, vlan_id=vlan, dut_data=setup_configuration)
        print("station", station)
        ser_no = get_test_library.attenuator_serial()
        print(ser_no)
        val = [['modes: Auto'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:UDP'],
               ['bandw_options: AUTO'], ['spatial_streams: 2'], ['attenuator: ' + str(ser_no[0])],
               ['attenuator2: ' + str(ser_no[1])],
               ['attenuations: 100 250 350'], ['attenuations2: 100 250 350'], ['chamber: DUT-Chamber'], ['tt_deg: 0..+60..300']]
        if station:
            rvr_o, report_name = get_test_library.rate_vs_range_test(station_name=station[0], mode=mode, download_rate="100%",
                                                        instance_name="SPATIAL_NSS2_RVR1_FIVEG",duration="60000",vlan_id=vlan,
                                                        dut_name=dut_name, raw_lines=val)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            logging.info("Test Completed... Cleaning up Stations")
            kpi = "kpi.csv"
            pass_value = {"strong": 500, "medium": 300, "weak": 150}
            atn, deg = [10, 25, 35], [0, 60, 120, 180, 240, 300]
            if kpi in entries:
                kpi_val = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
                print(kpi_val)
                if str(kpi_val) == "empty":
                    logging.info("TEST FAILED, Throughput value from kpi.csv is empty.")
                    allure.attach(name="CSV Data", body="TEST FAILED, Throughput value from kpi.csv is empty.")
                    assert False, "TEST FAILED, Throughput value from kpi.csv is empty."
                else:
                    allure.attach(name="CSV Data", body="Throughput value : " + str(kpi_val))
                    start, thrpt_val, pass_fail = 0, {}, []
                    for i in pass_value:
                        count = 0
                        for j in range(start, len(kpi_val), len(atn)):
                            thrpt_val[f"{atn[start]}atn-{deg[count]}deg"] = kpi_val[j][0]
                            if kpi_val[j][0] >= pass_value[i]:
                                pass_fail.append("PASS")
                            else:
                                pass_fail.append("FAIL")
                            count += 1
                        # start += 6
                    print(thrpt_val, "\n", pass_fail)
                    if "FAIL" in pass_fail:
                        logging.info("TEST FAILED, Actual throughput is lesser than Expected.")
                        assert False, "TEST FAILED, Actual throughput is lesser than Expected."
                    else:
                        logging.info("Test PASSED successfully")
                        assert True
            else:
                logging.info("csv file does not exist, Test failed")
                allure.attach(name="CSV Data", body="csv file does not exist")
                assert False, "csv file does not exist"
        else:
            logging.info("TEST FAILED,due to no station ip")
            assert False, "TEST FAILED,due to no station ip"

