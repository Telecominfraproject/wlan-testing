"""

    Advanced  Test: Rate v/s Range test under various combinations: Bridge Mode
    pytest -m "ratevsrange and bridge " -s -vvv --skip-testrail --testbed=basic-01 --alluredir=../allure_reports
    --> allure serve ../allure_reports/


"""
import os
import time
import pytest
import allure
import os.path

pytestmark = [pytest.mark.advance, pytest.mark.ratevsrange, pytest.mark.bridge]


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

@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.Mhz20
class TestRatevsRangeBridge(object):

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
        print("Cleanup existing clients and traffic")
        lf_tools.reset_scenario()
        lf_test.Client_disconnect(clean_l3_traffic=True)
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
        ser_no = lf_test.attenuator_serial()
        print(ser_no)
        val = [['modes: 802.11b'], ['pkts: MTU'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types:;TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: ' + str(ser_no[0])], ['attenuator2: ' + str(ser_no[1])],
               ['attenuations: 0 100 210..+100..630'], ['attenuations2: 0 100 210..+100..630'],['chamber: DUT-Chamber'], ['tt_deg: 0']]
        if station:
            rvr_o = lf_test.ratevsrange(station_name=station_names_twog, mode=mode, download_rate="1Gpbs", duration='5000',
                                       instance_name="MODEBRIDGE_RVR_11B_TWOG_modified",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            print("report name ", report_name)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries",entries)
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            kpi = "kpi.csv"
            pass_value = {"strong": 100, "medium": 95, "weak": 14}
            atn = [0, 10, 21, 24, 27,30,33,36,39,42,45,48,51,54,57,60,63]
            if kpi in entries:
                kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
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

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.client11g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2496", name="WIFI-2496")
    def test_client_wpa2_personal_2g_11g(self,
                                         lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                         get_configuration, lf_tools):
        """

        pytest -m "ratevsrange and bridge and client11g" -s -vvv --skip-testrail --testbed=advanced-02
        jira- wifi-2496
        """
        lf_tools.reset_scenario()
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
        ser_no = lf_test.attenuator_serial()
        print(ser_no)
        val = [['modes: 802.11g'], ['pkts: MTU'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types: TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: ' + str(ser_no[0])], ['attenuator2: ' + str(ser_no[1])],
               ['attenuations: 0 100 210..+30..630'], ['attenuations2: 0 100 210..+30..630'],['chamber: DUT-Chamber'], ['tt_deg: 0']]
        if station:
            time.sleep(3)
            rvr_o = lf_test.ratevsrange(station_name=station_names_twog, mode=mode, download_rate="1Gpbs",
                                        instance_name="MODEBRIDGE_RVR_11G_TWOG_modified",
                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            print("report name ", report_name)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            kpi = "kpi.csv"
            pass_value = {"strong": 100, "medium": 95, "weak": 14}
            atn = [0, 10, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63]
            if kpi in entries:
                kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
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

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.client11a
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2497", name="WIFI-2497")
    def test_client_wpa2_personal_5g_11a(self,
                                         lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                         get_configuration,lf_tools):
        """

        pytest -m "ratevsrange and bridge and client11a" -s -vvv --skip-testrail --testbed=advanced-02
        jira- wifi-2497
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)
        ser_no = lf_test.attenuator_serial()
        print(ser_no)
        val = [['modes: 802.11a'], ['pkts: MTU'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types:TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: ' + str(ser_no[0])], ['attenuator2: ' + str(ser_no[1])],
               ['attenuations: 0 100 210..+30..540'], ['attenuations2: 0 100 210..+30..540'],['chamber: DUT-Chamber'], ['tt_deg: 0']]
        if station:
            time.sleep(3)
            rvr_o = lf_test.ratevsrange(station_name=station_names_fiveg, mode=mode,download_rate="1Gpbs",
                                        instance_name="MODEBRIDGE_RVR_11A_FIVEG_modified",
                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            print("report name ", report_name)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            kpi = "kpi.csv"
            pass_value = {"strong": 100, "medium": 95, "weak": 14}
            atn = [0, 10, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63]
            if kpi in entries:
                kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
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

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.client11an
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2498", name="WIFI-2498")
    def test_client_wpa2_personal_5g_11an(self,
                                         lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                         get_configuration, lf_tools):
        """

        pytest -m "ratevsrange and bridge and client11an" -s -vvv --skip-testrail --testbed=advanced-02
        jira- wifi-2498
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)
        ser_no = lf_test.attenuator_serial()
        print(ser_no)
        val = [['modes: 802.11an'], ['pkts: MTU'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types:TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: ' + str(ser_no[0])], ['attenuator2: ' + str(ser_no[1])],
               ['attenuations: 0 100 210..+30..540'], ['attenuations2: 0 100 210..+30..540'],['chamber: DUT-Chamber'], ['tt_deg: 0']]
        if station:
            time.sleep(3)
            rvr_o = lf_test.ratevsrange(station_name=station_names_fiveg, mode=mode,download_rate="1Gpbs",
                                        instance_name="MODEBRIDGE_RVR_11AN_FIVEG_modified",
                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            print("report name ", report_name)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            kpi = "kpi.csv"
            pass_value = {"strong": 100, "medium": 95, "weak": 14}
            atn = [0, 10, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63]
            if kpi in entries:
                kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
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
    @pytest.mark.client11ac
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2499", name="WIFI-2499")
    def test_client_wpa2_personal_5g_11ac(self, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration, lf_tools):
        """

        pytest -m "ratevsrange and bridge and client11ac" -s -vvv --skip-testrail --testbed=advanced-02
        jira- wifi-2499
        """
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)
        ser_no = lf_test.attenuator_serial()
        print(ser_no)
        val = [['modes: 802.11an-AC'], ['pkts: MTU'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types:TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: ' + str(ser_no[0])], ['attenuator2: ' + str(ser_no[1])],
               ['attenuations: 0 100 210..+30..540'],['attenuations2: 0 100 210..+30..540'],['chamber: DUT-Chamber'], ['tt_deg: 0']]

        if station:
            time.sleep(3)
            rvr_o = lf_test.ratevsrange(station_name=station_names_fiveg, mode=mode,download_rate="1Gpbs",
                                        instance_name="MODEBRIDGE_RVR_11AC_FIVEG_modified",
                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            print("report name ", report_name)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            kpi = "kpi.csv"
            pass_value = {"strong": 100, "medium": 95, "weak": 14}
            atn = [0, 10, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63]
            if kpi in entries:
                kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
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
