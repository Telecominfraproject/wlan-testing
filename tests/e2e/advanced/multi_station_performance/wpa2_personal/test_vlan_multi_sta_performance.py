"""
    Test Multi-Station Performance: Bridge Mode
    pytest -m multistaperf_vlan
"""
import pytest
import allure
import os
import time
import pandas as pd

pytestmark = [pytest.mark.advance, pytest.mark.multistaperf_vlan, pytest.mark.vlan]

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

@allure.feature("VLAN MODE MULTI-STATION PERFORMANCE")
@allure.parent_suite("MULTI STATION PERFORMANCE")
@allure.suite(suite_name="VLAN MODE")
@allure.sub_suite(sub_suite_name="WPA2_personal MULTI STATION PERFORMANCE")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMultiStaPerfVlan(object):

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5942", name="WIFI-5942")
    @pytest.mark.vlan_msp
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_dis_nss1_2g
    def test_multi_station_VLAN_udp_upload_10dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
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
        get_test_library.add_vlan(vlan_ids=[vlan])
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        data = {"shelf": shelf, "resource": resource, "radio": values[2], "antenna": 1}
        get_test_library.json_post(_req_url="cli-json/set_wifi_radio", data=data)
        sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"], radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False, "test failed due to no station ip"
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_upload_10dB_dis_nss1_2g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")
        if sta_ip:
            assert True

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5944", name="WIFI-5944")
    @pytest.mark.vlan_msp
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_38dB_dis_nss1_2g
    def test_multi_station_VLAN_udp_upload_10dB_38dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = get_test_library.twog_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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
            sta_ip = get_test_library.client_connect_using_radio(ssid=ssid_name, passkey=profile_data["security_key"], radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False, "test failed due to no station ip"
            time.sleep(0.5)
        for i in range(4):
            get_test_library.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_upload_10dB_38dB_dis_nss1_2g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB,48DdB(NSS-1) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5945", name="WIFI-5945")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_38dB_48dB_dis_nss1_2g
    def test_multi_station_VLAN_udp_upload_10dB_38dB_48dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = get_test_library.twog_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_upload_10dB_38dB_48dB_dis_nss1_2g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title(
        "BRIDGE Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5949", name="WIFI-5949")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_dis_nss1_2g
    def test_multi_station_VLAN_udp_download_10dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
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
        get_test_library.add_vlan(vlan_ids=[vlan])
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
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_download_10dB_dis_nss1_2g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5950", name="WIFI-5950")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_38dB_dis_nss1_2g
    def test_multi_station_VLAN_udp_download_10dB_38dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = get_test_library.twog_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_download_10dB_38dB_dis_nss1_2g", mode=mode, vlan_id=[vlan],
                                        download_rate="1Gbps", batch_size="3,6",
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB,48DdB(NSS-1) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6085", name="WIFI-6085")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_38dB_48dB_dis_nss1_2g
    def test_multi_station_VLAN_udp_download_10dB_38dB_48dB_dis_nss1_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = get_test_library.twog_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_download_10dB_38dB_48dB_dis_nss1_2g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6092", name="WIFI-6092")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_dis_nss1_5g
    def test_multi_station_VLAN_udp_upload_10dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
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
        get_test_library.add_vlan(vlan_ids=[vlan])
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
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_upload_10dB_dis_nss1_5g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6093", name="WIFI-6093")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_25dB_dis_nss1_5g
    def test_multi_station_VLAN_udp_upload_10dB_25dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_upload_10dB_25dB_dis_nss1_5g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6094", name="WIFI-6094")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_25dB_35dB_dis_nss1_5g
    def test_multi_station_VLAN_udp_upload_10dB_25dB_35dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_upload_10dB_25dB_35dB_dis_nss1_5g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5946", name="WIFI-5946")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_dis_nss1_5g
    def test_multi_station_VLAN_udp_download_10dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
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
        get_test_library.add_vlan(vlan_ids=[vlan])
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
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_download_10dB_dis_nss1_5g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5947", name="WIFI-5947")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_25dB_dis_nss1_5g
    def test_multi_station_VLAN_udp_download_10dB_25dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_upload_10dB_25dB_dis_nss1_5g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB,35dB(NSS-1) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5948", name="WIFI-5948")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_25dB_35dB_dis_nss1_5g
    def test_multi_station_VLAN_udp_download_10dB_25dB_35dB_dis_nss1_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_download_10dB_25dB_35dB_dis_nss1_5g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5951", name="WIFI-5951")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_dis_nss2_2g
    def test_multi_station_VLAN_udp_upload_10dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
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
        get_test_library.add_vlan(vlan_ids=[vlan])
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
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_upload_10dB_dis_nss2_2g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5966", name="WIFI-5966")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_38dB_dis_nss2_2g
    def test_multi_station_VLAN_udp_upload_10dB_38dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = get_test_library.twog_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_upload_10dB_38dB_dis_nss2_2g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-2) distance UDP-upload 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5954", name="WIFI-5954")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_upload_10dB_38dB_48dB_dis_nss2_2g
    def test_multi_station_VLAN_udp_upload_10dB_38dB_48dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = get_test_library.twog_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_upload_10dB_38dB_48dB_dis_nss2_2g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5969", name="WIFI-5969")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_dis_nss2_2g
    def test_multi_station_VLAN_udp_download_10dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
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
        get_test_library.add_vlan(vlan_ids=[vlan])
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
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_download_10dB_dis_nss2_2g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5968", name="WIFI-5968")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_38dB_dis_nss2_2g
    def test_multi_station_VLAN_udp_download_10dB_38dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = get_test_library.twog_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_download_10dB_38dB_dis_nss2_2g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,38dB,48dB(NSS-2) distance UDP-download 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5967", name="WIFI-5967")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.udp_download_10dB_38dB_48dB_dis_nss2_2g
    def test_multi_station_VLAN_udp_download_10dB_38dB_48dB_dis_nss2_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = get_test_library.twog_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_download_10dB_38dB_48dB_dis_nss2_2g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5952", name="WIFI-5952")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_dis_nss2_5g
    def test_multi_station_VLAN_udp_upload_10dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
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
        get_test_library.add_vlan(vlan_ids=[vlan])
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
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_upload_10dB_dis_nss2_5g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5953", name="WIFI-5953")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_25dB_dis_nss2_5g
    def test_multi_station_VLAN_udp_upload_10dB_25dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_upload_10dB_25dB_dis_nss2_5g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,40dB,50dB(NSS-2) distance UDP-upload 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5973", name="WIFI-5973")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_10dB_25dB_35dB_dis_nss2_5g
    def test_multi_station_VLAN_udp_upload_10dB_40dB_50dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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
            get_test_library.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                get_test_library.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_upload_10dB_40dB_50dB_dis_nss2_5g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB(NSS-2) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5971", name="WIFI-5971")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_dis_nss2_5g
    def test_multi_station_VLAN_udp_download_10dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
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
        get_test_library.add_vlan(vlan_ids=[vlan])
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
        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_download_10dB_dis_nss2_5g", mode=mode, vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,25dB(NSS-2) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5970", name="WIFI-5970")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_25dB_dis_nss2_5g
    def test_multi_station_VLAN_udp_download_10dB_25dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_download_10dB_25dB_dis_nss2_5g", mode=mode,
                                        vlan_id=[vlan],
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("BRIDGE Mode Multi Station Performance Test with 10dB,40dB,50dB(NSS-2) distance UDP-download 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5972", name="WIFI-5972")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.udp_download_10dB_40dB_50dB_dis_nss2_5g
    def test_multi_station_VLAN_udp_download_10dB_40dB_50dB_dis_nss2_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        get_test_library.chamber_view()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = get_test_library.fiveg_prefix
        atten_sr = get_test_library.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        get_test_library.add_vlan(vlan_ids=[vlan])
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

        wct_obj = get_test_library.wifi_capacity(instance_name="udp_VLAN_download_10dB_40dB_50dB_dis_nss2_5g", mode=mode,
                                        vlan_id=[vlan],
                                        download_rate="1Gbps", batch_size="3,6,9",
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
        if not csv_val:
            print("csv file does not exist, Test failed")
            allure.attach(name="Csv Data", body="csv file does not exist, Test failed")
            assert False, "csv file does not exist, Test failed"
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")
