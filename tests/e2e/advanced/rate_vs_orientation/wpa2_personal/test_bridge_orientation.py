"""

    Test Rate v/s Orientation : Bridge Mode
    pytest -m "rate_vs_orientation_tests"
"""
import logging
import os
import time
import pytest
import allure
import os.path

pytestmark = [pytest.mark.advance, pytest.mark.rate_vs_orientation_tests, pytest.mark.bridge, pytest.mark.wpa2_personal]


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
@allure.feature("BRIDGE MODE RATE VS ORIENTATION")
@allure.parent_suite("RATE VS ORIENTATION")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="WPA2_personal RATE VS ORIENTATION")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestRateVsOrientationBridge(object):
    """
    Bridge Mode : Test Rate v/s Orientation
    pytest -m "rate_vs_orientation_tests and wpa2_personal and bridge"
    """
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("Bridge Mode Rate vs Orientation Test (NSS-2) 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5431", name="WIFI-5431")
    def test_rvo_tcp_dl_nss2_wpa2_personal_5g(self, get_test_library, setup_configuration, check_connectivity):
        """
            pytest -m "rate_vs_orientation_tests and wpa2_personal and bridge and fiveg"
        """
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = list(setup_configuration.keys())[0]
        # station = {'1.1.ath10k_5g00': {'4way time (us)': 0, 'channel': '149', 'cx time (us)': 0, 'dhcp (ms)': 1540, 'ip': '172.16.230.16', 'signal': '-41 dBm'}}
        station = get_test_library.client_connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                  band=band, num_sta=1, vlan_id=vlan, dut_data=setup_configuration)
        ser_no = get_test_library.attenuator_serial() # ['1.1.3022', '1.1.3025']
        # ser_no = ['1.1.3022', '1.1.3025']
        logging.info(f"Attenuators - {ser_no}")
        val = [['modes: 802.11an-AC'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:TCP'],
               ['bandw_options: 80'], ['spatial_streams: 2'], ['attenuator: ' + str(ser_no[0])],
               ['attenuator2: ' + str(ser_no[1])], ['attenuations: 100'],
               ['attenuations2: 100'], ['chamber: DUT-Chamber'], ['tt_deg: 0..+30..359']] #210..+30..540 #0..+30..359

        if station:
            rvr_o, report_name = get_test_library.rate_vs_range_test(station_name=list(station.keys())[0], mode=mode,
                                        instance_name="ORIENTATION_RVR_BRIDGE_11_AC",
                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            # report_name = rvr_o[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            kpi = "kpi.csv"
            pass_value = {"strong":500}
            atn, deg = [10], [0,30,60,90,120,150,180,210,240,270,300,330] #
            if kpi in entries:
                kpi_val = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
                logging.info(f"kpi-csv value- {kpi_val}")
                # allure.attach.file(source="../reports/" + report_name + "/" + kpi, name="kpi.csv")
                if str(kpi_val) == "empty":
                    assert False, "Throughput value from kpi.csv is empty, Test failed"
                else:
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
                    logging.info(f"Throughtput-value - {thrpt_val}\nPass-fail - {pass_fail}")
                    get_test_library.allure_report_table_format(dict_data=thrpt_val, key="attenuation-orientation",
                                                                value="Throughput values", name="Test_results")
                    if "FAIL" in pass_fail:
                        assert False, "Test failed due to lesser value"
                    else:
                        assert True
            else:
                assert False, "CSV file does not exist"
        else:
            assert False, "Test failed due to no station ip"

    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("Bridge Mode Rate vs Orientation Test (NSS-2) 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5431", name="WIFI-5431")
    def test_client_tcp_dl_nss2_wpa2_personal_2g(self, get_test_library, setup_configuration, check_connectivity):
        """
                    pytest -m "rate_vs_orientation_tests and wpa2_personal and bridge and twog"
        """
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        dut_name = list(setup_configuration.keys())[0]

        station = get_test_library.client_connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                  band=band, num_sta=1, vlan_id=vlan, dut_data=setup_configuration)
        ser_no = get_test_library.attenuator_serial()
        val = [['modes: 802.11bgn-AC'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:TCP'],
               ['bandw_options: 80'], ['spatial_streams: 2'], ['attenuator: ' + str(ser_no[0])],
               ['attenuator2: ' + str(ser_no[1])], ['attenuations: 100'],
               ['attenuations2: 100'], ['chamber: DUT-Chamber'], ['tt_deg: 0..+30..359']]  # 210..+30..540 #0..+30..359

        if station:
            rvr_o, report_name = get_test_library.rate_vs_range_test(station_name=list(station.keys())[0], mode=mode,
                                        instance_name="ORIENTATION_RVR_BRIDGE_11_AC",
                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            # report_name = rvr_o[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            kpi = "kpi.csv"
            pass_value = {"strong": 90}
            atn, deg = [10], [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]  #
            if kpi in entries:
                kpi_val = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
                logging.info(f"kpi-csv value- {kpi_val}")
                # allure.attach.file(source="../reports/" + report_name + "/" + kpi, name="kpi.csv")
                if str(kpi_val) == "empty":
                    print("Throughput value from kpi.csv is empty, Test failed")
                    allure.attach(name="CSV Data", body="Throughput value from kpi.csv is empty, Test failed")
                    assert False, "Throughput value from kpi.csv is empty, Test failed"
                else:
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
                    logging.info(f"Throughtput-value - {thrpt_val}\nPass-fail - {pass_fail}")
                    get_test_library.allure_report_table_format(dict_data=thrpt_val, key="attenuation-orientation",
                                                                value="Throughput values", name="Test_results")
                    if "FAIL" in pass_fail:
                        assert False, "Test failed due to lesser value"
                    else:
                        assert True
            else:
                assert False, "CSV file does not exist"
        else:
            assert False, "Test failed due to no station ip"
