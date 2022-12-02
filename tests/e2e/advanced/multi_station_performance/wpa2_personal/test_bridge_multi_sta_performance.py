"""
    Test Multi-Station Performance: Bridge Mode
    pytest -m multistaperf
"""
import pytest
import allure
import time

pytestmark = [pytest.mark.advance, pytest.mark.multistaperf, pytest.mark.bridge, pytest.mark.report]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "channel-width": 80},
        "2G": {
            "channel-width": 20}
    },
    "radius": False
}

@allure.feature("BRIDGE MODE MULTI-STATION PERFORMANCE")
@allure.parent_suite("MULTI STATION PERFORMANCE")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="WPA2_personal MULTI STATION PERFORMANCE")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMultiStaPerfBridge(object):
    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5733", name="WIFI-5733")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tps
    @pytest.mark.udp_upload_10dB_dis_nss1_2g
    def test_multi_station_udp_upload_10dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3"
        station_name = get_test_library.twog_prefix
        radio_name = get_test_library.wave2_2g_radios[0]
        print("radio:", radio_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = get_test_library.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 1}
        get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
        sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                                                       radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False, "test failed due to no station ip"
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_upload_10dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (35 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 35 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (2G)",
                                                            value="Shorter Distance (10dB)", name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (2G)",
                                                            value="Shorter Distance (10dB)", name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5844", name="WIFI-5844")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsm
    @pytest.mark.udp_upload_10dB_38dB_dis_nss1_2g
    def test_multi_station_udp_upload_10dB_38dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6"
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        station_name = get_test_library.twog_prefix
        sta = []
        list_three_sta = []
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)

        for i in range(2):
            radio_name = get_test_library.wave2_2g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 1}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                                 radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 380)
            time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_upload_10dB_38dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (30 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 38dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 30 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (2G)",
                                                            value="Shorter & Medium Distance (10dB, 38dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (2G)",
                                                            value="Shorter & Medium Distance (10dB, 38dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5877", name="WIFI-5877")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsml
    @pytest.mark.udp_upload_10dB_38dB_48dB_dis_nss1_2g
    def test_multi_station_udp_upload_10dB_38dB_48dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6,9"
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        station_name = get_test_library.twog_prefix
        sta = []
        list_three_sta = []
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = get_test_library.wave2_2g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 1}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 380)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 480)
                time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_upload_10dB_38dB_48dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (25 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 38dB ,48dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 25 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (2G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 38dB, 48dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (2G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 38dB, 48dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5881", name="WIFI-5881")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tps
    @pytest.mark.udp_download_10dB_dis_nss1_2g
    def test_multi_station_udp_download_10dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3"
        radio_name = get_test_library.wave2_2g_radios[0]
        station_name = get_test_library.twog_prefix
        print(radio_name)
        print(station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = get_test_library.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 1}
        get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
        sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False, "test failed due to no station ip"
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_download_10dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (35 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 35 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (2G)",
                                                            value="Shorter Distance (10dB)", name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (2G)",
                                                            value="Shorter Distance (10dB)", name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5882", name="WIFI-5882")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsm
    @pytest.mark.udp_download_10dB_38dB_dis_nss1_2g
    def test_multi_station_udp_download_10dB_38dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6"
        station_name = get_test_library.twog_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(2):
            radio_name = get_test_library.wave2_2g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 1}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 380)
            time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_download_10dB_38dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (30 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 38dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 30 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (2G)",
                                                            value="Shorter & Medium Distance (10dB, 38dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (2G)",
                                                            value="Shorter & Medium Distance (10dB, 38dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6083", name="WIFI-6083")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsml
    @pytest.mark.udp_download_10dB_38dB_48dB_dis_nss1_2g
    def test_multi_station_udp_download_10dB_38dB_48dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6,9"
        station_name = get_test_library.twog_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = get_test_library.wave2_2g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 1}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 380)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 480)
                time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_download_10dB_38dB_48dB_dis_nss1_2g", mode=mode,
                                        vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (25 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 38dB ,48dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 25 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (2G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 38dB, 48dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (2G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 38dB, 48dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6086", name="WIFI-6086")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tps
    @pytest.mark.udp_upload_10dB_dis_nss1_5g
    def test_multi_station_udp_upload_10dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3"
        station_name = get_test_library.fiveg_prefix
        radio_name = get_test_library.wave2_5g_radios[0]
        print(radio_name)
        print(station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = get_test_library.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 1}
        get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
        sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False, "test failed due to no station ip"
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_upload_10dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (250 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 250 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (5G)",
                                                            value="Shorter Distance (10dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (5G)",
                                                            value="Shorter Distance (10dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB(NSS-1) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6087", name="WIFI-6087")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsm
    @pytest.mark.udp_upload_10dB_25dB_dis_nss1_5g
    def test_multi_station_udp_upload_10dB_25dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)

        for i in range(2):
            radio_name = get_test_library.wave2_5g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 1}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 250)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_upload_10dB_25dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (250 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 25dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 250 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (5G)",
                                                            value="Shorter & Medium Distance (10dB, 25dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (5G)",
                                                            value="Shorter & Medium Distance (10dB, 25dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-1) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6088", name="WIFI-6088")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsml
    @pytest.mark.udp_upload_10dB_25dB_35dB_dis_nss1_5g
    def test_multi_station_udp_upload_10dB_25dB_35dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6,9"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = get_test_library.wave2_5g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 1}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 250)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 350)
                time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_upload_10dB_25dB_35dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (200 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 25dB ,35dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 200 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (5G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 25dB ,35dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (5G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 25dB ,35dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5878", name="WIFI-5878")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tps
    @pytest.mark.udp_download_10dB_dis_nss1_5g
    def test_multi_station_udp_download_10dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3"
        station_name = get_test_library.fiveg_prefix
        radio_name = get_test_library.wave2_5g_radios[0]
        print(radio_name)
        print(station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = get_test_library.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 1}
        get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
        sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False, "test failed due to no station ip"
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_download_10dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (250 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 250 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (5G)",
                                                            value="Shorter Distance (10dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (5G)",
                                                            value="Shorter Distance (10dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5879", name="WIFI-5879")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsm
    @pytest.mark.udp_download_10dB_25dB_dis_nss1_5g
    def test_multi_station_udp_download_10dB_25dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(2):
            radio_name = get_test_library.wave2_5g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 1}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 250)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_download_10dB_25dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (250 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 25dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 250 Mbpsps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (5G)",
                                                            value="Shorter & Medium Distance (10dB, 25dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (5G)",
                                                            value="Shorter & Medium Distance (10dB, 25dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5880", name="WIFI-5880")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsml
    @pytest.mark.udp_download_10dB_25dB_35dB_dis_nss1_5g
    def test_multi_station_udp_download_10dB_25dB_35dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6,9"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = get_test_library.wave2_5g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 1}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 250)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 350)
                time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_download_10dB_25dB_35dB_dis_nss1_5g", mode=mode,
                                        vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (200 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 25dB ,35dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 200 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (5G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 25dB ,35dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-1 (5G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 25dB ,35dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5883", name="WIFI-5883")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tps
    @pytest.mark.udp_upload_10dB_dis_nss2_2g
    def test_multi_station_udp_upload_10dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3"
        station_name = get_test_library.twog_prefix
        radio_name = get_test_library.wave2_2g_radios[0]
        print(radio_name, "\n", station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = get_test_library.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 4}
        get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
        sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False, "test failed due to no station ip"
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_upload_10dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (70 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 70 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (2G)",
                                                            value="Shorter Distance (10dB)", name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (2G)",
                                                            value="Shorter Distance (10dB)", name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5887", name="WIFI-5887")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsm
    @pytest.mark.udp_upload_10dB_38dB_dis_nss2_2g
    def test_multi_station_udp_upload_10dB_38dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6"
        station_name = get_test_library.twog_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(2):
            radio_name = get_test_library.wave2_2g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 4}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 380)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_upload_10dB_38dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (60 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 38dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 60 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (2G)",
                                                            value="Shorter & Medium Distance (10dB, 38dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (2G)",
                                                            value="Shorter & Medium Distance (10dB, 38dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5886", name="WIFI-5886")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsml
    @pytest.mark.udp_upload_10dB_38dB_48dB_dis_nss2_2g
    def test_multi_station_udp_upload_10dB_38dB_48dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6,9"
        station_name = get_test_library.twog_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = get_test_library.wave2_2g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 4}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 380)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 480)
                time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_upload_10dB_38dB_48dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (50 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 38dB ,48dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 50 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (2G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 38dB, 48dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (2G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 38dB, 48dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5890", name="WIFI-5890")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tps
    @pytest.mark.udp_download_10dB_dis_nss2_2g
    def test_multi_station_udp_download_10dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3"
        station_name = get_test_library.twog_prefix
        radio_name = get_test_library.wave2_2g_radios[0]
        print(radio_name)
        print(station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = get_test_library.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 4}
        get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
        sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False, "test failed due to no station ip"
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_download_10dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (70 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 70 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (2G)",
                                                            value="Shorter Distance (10dB)", name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (2G)",
                                                            value="Shorter Distance (10dB)", name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5889", name="WIFI-5889")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsm
    @pytest.mark.udp_download_10dB_38dB_dis_nss2_2g
    def test_multi_station_udp_download_10dB_38dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6"
        station_name = get_test_library.twog_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(2):
            radio_name = get_test_library.wave2_2g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 4}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 380)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_download_10dB_38dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (60 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 38dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 60 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (2G)",
                                                            value="Shorter & Medium Distance (10dB, 38dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (2G)",
                                                            value="Shorter & Medium Distance (10dB, 38dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5888", name="WIFI-5888")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tpsml
    @pytest.mark.udp_download_10dB_38dB_48dB_dis_nss2_2g
    def test_multi_station_udp_download_10dB_38dB_48dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6,9"
        station_name = get_test_library.twog_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = get_test_library.wave2_2g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 4}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 380)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 480)
                time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_download_10dB_38dB_48dB_dis_nss2_2g", mode=mode,
                                        vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (50 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 38dB ,48dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 50 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (2G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 38dB, 48dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (2G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 38dB, 48dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5884", name="WIFI-5884")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tps
    @pytest.mark.udp_upload_10dB_dis_nss2_5g
    def test_multi_station_udp_upload_10dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3"
        station_name = get_test_library.fiveg_prefix
        radio_name = get_test_library.wave2_5g_radios[0]
        print(radio_name)
        print(station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = get_test_library.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 4}
        get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
        sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False, "test failed due to no station ip"
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_upload_10dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (500 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 500 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (5G)",
                                                            value="Shorter Distance (10dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (5G)",
                                                            value="Shorter Distance (10dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5885", name="WIFI-5885")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsm
    @pytest.mark.udp_upload_10dB_25dB_dis_nss2_5g
    def test_multi_station_udp_upload_10dB_25dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)

        for i in range(2):
            radio_name = get_test_library.wave2_5g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 4}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 250)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_upload_10dB_25dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (500 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 25dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 500 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (5G)",
                                                            value="Shorter & Medium Distance (10dB, 25dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (5G)",
                                                            value="Shorter & Medium Distance (10dB, 25dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5896", name="WIFI-5896")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsml
    @pytest.mark.udp_upload_10dB_25dB_35dB_dis_nss2_5g
    def test_multi_station_udp_upload_10dB_25dB_35dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6,9"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = get_test_library.wave2_5g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 4}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 250)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 350)
                time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_upload_10dB_25dB_35dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (400 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 25dB ,35dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 400 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (5G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 25dB, 35dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (5G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 25dB, 35dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5892", name="WIFI-5892")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tps
    @pytest.mark.udp_download_10dB_dis_nss2_5g
    def test_multi_station_udp_download_10dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3"
        station_name = get_test_library.fiveg_prefix
        radio_name = get_test_library.wave2_5g_radios[0]
        print(radio_name)
        print(station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = get_test_library.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 4}
        get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
        sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False, "test failed due to no station ip"
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_download_10dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (500 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 500 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (5G)",
                                                            value="Shorter Distance (10dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (5G)",
                                                            value="Shorter Distance (10dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB(NSS-2) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5891", name="WIFI-5891")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsm
    @pytest.mark.udp_download_10dB_25dB_dis_nss2_5g
    def test_multi_station_udp_download_10dB_25dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)

        for i in range(2):
            radio_name = get_test_library.wave2_5g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 4}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 250)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_download_10dB_25dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (500 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 25dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 500 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (5G)",
                                                            value="Shorter & Medium Distance (10dB, 25dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (5G)",
                                                            value="Shorter & Medium Distance (10dB, 25dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-2) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5895", name="WIFI-5895")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tpsml
    @pytest.mark.udp_download_10dB_25dB_35dB_dis_nss2_5g
    def test_multi_station_udp_download_10dB_25dB_35dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        get_test_library.client_disconnect(clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        batch_size = "3,6,9"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = get_test_library.wave2_5g_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 4}
            get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
            time.sleep(0.5)
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 250)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 350)
                time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_download_10dB_25dB_35dB_dis_nss2_5g", mode=mode,
                                        vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        get_test_library.attach_report_graphs(report_name=report_name)
        csv_val = get_test_library.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (400 * 0.7)
        print("pass value ", pass_value)
        get_test_library.client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        table_data = {"Attenuation (dB)": "10dB, 25dB ,35dB",
                       "Expected Throughput (Mbps)": str(pass_value) + " (70% of 400 Mbps)",
                       "Actual Throughput (Mbps)": str(list(csv_val["Up"].values())[-1])}
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body="Throughput value : " + str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (5G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 25dB, 35dB)",
                                                            name="Test_results")
                print("Test passed successfully")
                assert True
            else:
                get_test_library.allure_report_table_format(dict_data=table_data, key="NSS-2 (5G)",
                                                            value="Shorter & Medium & Long Distance (10dB, 25dB, 35dB)",
                                                            name="Test_results")
                print("Test failed due to lesser value")
                assert False, "Test failed due to lesser value"
        print("Test Completed... Cleaning up Stations")
