"""

    Test Rate v/s Orientation : Nat Mode
    pytest -m "rate_vs_orientation_tests"
"""
import logging
import os
import time
import pytest
import allure
import os.path

pytestmark = [pytest.mark.advance, pytest.mark.rate_vs_orientation_tests, pytest.mark.nat, pytest.mark.wpa2_personal]


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
@allure.feature("NAT MODE RATE VS ORIENTATION")
@allure.parent_suite("RATE VS ORIENTATION")
@allure.suite(suite_name="NAT MODE")
@allure.sub_suite(sub_suite_name="WPA2_personal RATE VS ORIENTATION")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestRateVsOrientationNat(object):
    """
    Nat Mode : Test Rate v/s Orientation
    pytest -m "rate_vs_orientation_tests and wpa2_personal and nat"
    """
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("Nat Mode Rate vs Orientation Test 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5431", name="WIFI-5431")
    def test_rvo_tcp_dl_nss2_wpa2_personal_5g(self, get_test_library, setup_configuration, check_connectivity):
        """
            pytest -m "rate_vs_orientation_tests and wpa2_personal and nat and fiveg"
        """
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "fiveg"
        vlan = 1
        chamber_view_obj, dut_name = get_test_library.chamber_view()

        station = get_test_library.client_connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                  band=band, num_sta=1, vlan_id=vlan, dut_data=setup_configuration)
        # station = {'1.1.ath10k_5g00': {'4way time (us)': 875, 'channel': '149', 'cx time (us)': 133934, 'dhcp (ms)': 7468, 'ip': '192.168.34.86', 'signal': '-41 dBm'}}
        ser_no = get_test_library.attenuator_serial()
        logging.info(f"Attenuators - {ser_no}")
        val = [['modes: 802.11an-AC'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:TCP'],
               ['bandw_options: 80'], ['spatial_streams: 2'], ['attenuator: ' + str(ser_no[0])],
               ['attenuator2: ' + str(ser_no[1])], ['attenuations: 100'],
               ['attenuations2: 100'], ['chamber: DUT-Chamber'], ['tt_deg: 0..+30..359']] #210..+30..540 #0..+30..359

        if station:
            rvr_o, report_name = get_test_library.rate_vs_range_test(station_name=list(station.keys())[0], mode=mode,
                                        instance_name="ORIENTATION_RVR_NAT_11_AC",
                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            # report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            # entries = ['canvil.ico', 'kpi.csv', 'chart-2-print.png', 'text-csv-3.csv', 'kpi-chart-3-print.png', 'text-tab-0.csv', 'report.css', 'chart-8.png', 'chart-5.png', 'chart-6.png', 'text-tab-2.csv', 'index.html', 'custom.css', 'index-print.html', 'chart-7.png', 'chart-7-print.png', 'chart-2.png', 'rate-vs-range-vs-orientation-report-2022-12-16-01-34-17.pdf', 'text-tab-3.csv', 'text-tab-1.csv', 'logo.png', 'chart-8-print.png', 'report_banner-1000x205.jpg', 'text-csv-0.csv', 'kpi-chart-0.png', 'chart-4.png', 'chart-1-print.png', 'chart-5-print.png', 'text-csv-1.csv', 'text-csv-2.csv', 'chart-1.png', 'csv-data', 'CenturyGothic.woff', 'kpi-chart-3.png', 'CandelaLogo2-90dpi-200x90-trans.png', 'chart-4-print.png', 'chart-6-print.png', 'kpi-chart-0-print.png', 'candela_swirl_small-72h.png']
            get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            kpi = "kpi.csv"
            pass_value = {"strong":500}
            atn, deg = [10], [0,30,60,90,120,150,180,210,240,270,300,330] #
            if kpi in entries:
                kpi_val = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
                # kpi_val = [[93.856416], [92.763538], [93.591643], [93.601009], [93.510303], [92.895905], [93.438518], [93.060875], [93.697596], [92.740075], [93.005289], [93.113691]]
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
                    # thrpt_val = {'10atn-0deg': 93.856416, '10atn-30deg': 92.763538, '10atn-60deg': 93.591643, '10atn-90deg': 93.601009, '10atn-120deg': 93.510303, '10atn-150deg': 92.895905, '10atn-180deg': 93.438518, '10atn-210deg': 93.060875, '10atn-240deg': 93.697596, '10atn-270deg': 92.740075, '10atn-300deg': 93.005289, '10atn-330deg': 93.113691}
                    # pass_fail = ['FAIL', 'FAIL', 'FAIL', 'FAIL', 'FAIL', 'FAIL', 'FAIL', 'FAIL', 'FAIL', 'FAIL', 'FAIL', 'FAIL']
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
    @allure.title("Nat Mode Rate vs Orientation Test 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5431", name="WIFI-5431")
    def test_client_tcp_dl_nss2_wpa2_personal_2g(self, get_test_library, setup_configuration, check_connectivity):
        """
                    pytest -m "rate_vs_orientation_tests and wpa2_personal and nat and twog"
        """
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "twog"
        vlan = 1
        chamber_view_obj, dut_name = get_test_library.chamber_view()

        station = get_test_library.client_connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                                  band=band, num_sta=1, vlan_id=vlan, dut_data=setup_configuration)
        ser_no = get_test_library.attenuator_serial()
        val = [['modes: 802.11bgn-AC'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:TCP'],
               ['bandw_options: 80'], ['spatial_streams: 2'], ['attenuator: ' + str(ser_no[0])],
               ['attenuator2: ' + str(ser_no[1])], ['attenuations: 100'],
               ['attenuations2: 100'], ['chamber: DUT-Chamber'], ['tt_deg: 0..+30..359']]  # 210..+30..540 #0..+30..359

        if station:
            rvr_o, report_name = get_test_library.rate_vs_range_test(station_name=list(station.keys())[0], mode=mode,
                                        instance_name="ORIENTATION_RVR_NAT_11_AC",
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

