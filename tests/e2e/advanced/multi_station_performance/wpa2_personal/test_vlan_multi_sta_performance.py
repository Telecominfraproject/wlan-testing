import pytest
import allure
import os
import time
import pandas as pd

pytestmark = [pytest.mark.advance, pytest.mark.multistaperf, pytest.mark.vlan]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan":100},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan":100}
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
class TestMultiStaPerfVlan(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5942", name="WIFI-5942")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_upload_10dB_dis_nss1_2g
    def test_multi_station_VLAN_tcp_upload_10dB_dis_nss1_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3"
        station_name = station_names_twog[0]
        radio_name = lf_tools.twog_radios[0]
        print(radio_name)
        print(station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = lf_test.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 1)
        sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"], radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_upload_10dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (35 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5944", name="WIFI-5944")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_upload_10dB_40dB_dis_nss1_2g
    def test_multi_station_VLAN_tcp_upload_10dB_40dB_dis_nss1_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)

        for i in range(2):
            radio_name = lf_tools.twog_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 1)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"], radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_upload_10dB_40dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (30 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5945", name="WIFI-5945")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_upload_10dB_40dB_50dB_dis_nss1_2g
    def test_multi_station_VLAN_tcp_upload_10dB_40dB_50dB_dis_nss1_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = lf_tools.twog_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 1)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                lf_test.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_upload_10dB_40dB_50dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (25 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5949", name="WIFI-5949")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_download_10dB_dis_nss1_2g
    def test_multi_station_VLAN_tcp_download_10dB_dis_nss1_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3"
        station_name = station_names_twog[0]
        radio_name = lf_tools.twog_radios[0]
        print(radio_name)
        print(station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = lf_test.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 1)
        sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_download_10dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (35 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5950", name="WIFI-5950")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_download_10dB_40dB_dis_nss1_2g
    def test_multi_station_VLAN_tcp_download_10dB_40dB_dis_nss1_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)

        for i in range(2):
            radio_name = lf_tools.twog_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 1)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_download_10dB_40dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="3,6",
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (30 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6085", name="WIFI-6085")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_download_10dB_40dB_50dB_dis_nss1_2g
    def test_multi_station_VLAN_tcp_download_10dB_40dB_50dB_dis_nss1_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = lf_tools.twog_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 1)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                lf_test.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_download_10dB_40dB_50dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (25 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6092", name="WIFI-6092")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_upload_10dB_dis_nss1_5g
    def test_multi_station_VLAN_tcp_upload_10dB_dis_nss1_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3"
        station_name = station_names_fiveg[0]
        radio_name = lf_tools.fiveg_radios[0]
        print(radio_name)
        print(station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = lf_test.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 1)
        sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_upload_10dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (250 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6093", name="WIFI-6093")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_upload_10dB_40dB_dis_nss1_5g
    def test_multi_station_VLAN_tcp_upload_10dB_40dB_dis_nss1_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)

        for i in range(2):
            radio_name = lf_tools.fiveg_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 1)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_upload_10dB_40dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (250 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6094", name="WIFI-6094")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_upload_10dB_40dB_50dB_dis_nss1_5g
    def test_multi_station_VLAN_tcp_upload_10dB_40dB_50dB_dis_nss1_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = lf_tools.fiveg_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 1)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                lf_test.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_upload_10dB_40dB_50dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (200 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5946", name="WIFI-5946")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_download_10dB_dis_nss1_5g
    def test_multi_station_VLAN_tcp_download_10dB_dis_nss1_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3"
        station_name = station_names_fiveg[0]
        radio_name = lf_tools.fiveg_radios[0]
        print(radio_name)
        print(station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = lf_test.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 1)
        sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_download_10dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (250 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5947", name="WIFI-5947")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_download_10dB_40dB_dis_nss1_5g
    def test_multi_station_VLAN_tcp_download_10dB_40dB_dis_nss1_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)

        for i in range(2):
            radio_name = lf_tools.fiveg_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 1)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_upload_10dB_40dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (250 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5948", name="WIFI-5948")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_download_10dB_40dB_50dB_dis_nss1_5g
    def test_multi_station_VLAN_tcp_download_10dB_40dB_50dB_dis_nss1_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = lf_tools.fiveg_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 1)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                lf_test.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_download_10dB_40dB_50dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (200 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5951", name="WIFI-5951")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_upload_10dB_dis_nss2_2g
    def test_multi_station_VLAN_tcp_upload_10dB_dis_nss2_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3"
        station_name = station_names_twog[0]
        radio_name = lf_tools.twog_radios[0]
        print(radio_name)
        print(station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = lf_test.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 4)
        sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_upload_10dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (70 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5966", name="WIFI-5966")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_upload_10dB_40dB_dis_nss2_2g
    def test_multi_station_VLAN_tcp_upload_10dB_40dB_dis_nss2_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)

        for i in range(2):
            radio_name = lf_tools.twog_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 4)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_upload_10dB_40dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (60 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5954", name="WIFI-5954")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_upload_10dB_40dB_50dB_dis_nss2_2g
    def test_multi_station_VLAN_tcp_upload_10dB_40dB_50dB_dis_nss2_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = lf_tools.twog_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 4)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                lf_test.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_upload_10dB_40dB_50dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (50 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5969", name="WIFI-5969")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_download_10dB_dis_nss2_2g
    def test_multi_station_VLAN_tcp_download_10dB_dis_nss2_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3"
        station_name = station_names_twog[0]
        radio_name = lf_tools.twog_radios[0]
        print(radio_name)
        print(station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = lf_test.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 4)
        sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_download_10dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (70 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5968", name="WIFI-5968")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_download_10dB_40dB_dis_nss2_2g
    def test_multi_station_VLAN_tcp_download_10dB_40dB_dis_nss2_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)

        for i in range(2):
            radio_name = lf_tools.twog_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 4)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_download_10dB_40dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (60 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5967", name="WIFI-5967")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_download_10dB_40dB_50dB_dis_nss2_2g
    def test_multi_station_VLAN_tcp_download_10dB_40dB_50dB_dis_nss2_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = lf_tools.twog_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 4)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                lf_test.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_download_10dB_40dB_50dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (50 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5952", name="WIFI-5952")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_upload_10dB_dis_nss2_5g
    def test_multi_station_VLAN_tcp_upload_10dB_dis_nss2_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3"
        station_name = station_names_fiveg[0]
        radio_name = lf_tools.fiveg_radios[0]
        print(radio_name)
        print(station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = lf_test.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 4)
        sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_upload_10dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (500 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5953", name="WIFI-5953")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_upload_10dB_40dB_dis_nss2_5g
    def test_multi_station_VLAN_tcp_upload_10dB_40dB_dis_nss2_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)

        for i in range(2):
            radio_name = lf_tools.fiveg_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 4)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_upload_10dB_40dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (500 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5973", name="WIFI-5973")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_upload_10dB_40dB_50dB_dis_nss2_5g
    def test_multi_station_VLAN_tcp_upload_10dB_40dB_50dB_dis_nss2_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = lf_tools.fiveg_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 4)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                lf_test.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_upload_10dB_40dB_50dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size=batch_size,
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (400 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Up"].values())[-1]))
            if list(csv_val["Up"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5971", name="WIFI-5971")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_download_10dB_dis_nss2_5g
    def test_multi_station_VLAN_tcp_download_10dB_dis_nss2_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3"
        station_name = station_names_fiveg[0]
        radio_name = lf_tools.fiveg_radios[0]
        print(radio_name)
        print(station_name)
        values = radio_name.split(".")
        shelf = int(values[0])
        resource = int(values[1])
        print(shelf, resource)
        atten_sr = lf_test.attenuator_serial()
        atten_sr1 = atten_sr[1].split(".")
        print(atten_sr1)
        print(atten_sr)
        sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 4)
        sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=radio_name, station_name=sta)
        if not sta_ip:
            print("test failed due to no station ip")
            assert False
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_download_10dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (500 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5970", name="WIFI-5970")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_download_10dB_40dB_dis_nss2_5g
    def test_multi_station_VLAN_tcp_download_10dB_40dB_dis_nss2_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6"
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(6):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)

        for i in range(2):
            radio_name = lf_tools.fiveg_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 4)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_download_10dB_40dB_dis_nss2_5g", mode=mode,
                                        vlan_id=vlan,
                                        download_rate="1Gbps", batch_size=batch_size,
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (500 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5972", name="WIFI-5972")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_download_10dB_40dB_50dB_dis_nss2_5g
    def test_multi_station_VLAN_tcp_download_10dB_40dB_50dB_dis_nss2_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "VLAN"
        vlan = 100
        batch_size = "3,6,9"
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
        print(atten_sr)
        atten_sr1 = atten_sr[1].split(".")
        atten_sr2 = atten_sr[0].split(".")
        print(atten_sr1, atten_sr2)
        sta = []
        list_three_sta = []
        lf_tools.add_vlan(vlan_ids=[vlan])
        for i in range(9):
            list_three_sta.append(station_name + str(i))
            if (i != 0) and (((i + 1) % 3) == 0):
                sta.append(list_three_sta)
                list_three_sta = []
        print(sta)
        for i in range(3):
            radio_name = lf_tools.fiveg_radios[i]
            print(radio_name)
            print(station_name)
            values = radio_name.split(".")
            shelf = int(values[0])
            resource = int(values[1])
            print(shelf, resource)
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 4)
            time.sleep(0.5)
            sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                        radio=radio_name, station_name=sta[i])
            if not sta_ip:
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)
            if i >= 2:
                lf_test.attenuator_modify(int(atten_sr2[2]), i, 500)
                time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_VLAN_download_10dB_40dB_50dB_dis_nss2_5g", mode=mode,
                                        vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="3,6,9",
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=batch_size)
        print(csv_val)
        pass_value = (400 * 0.7)
        print("pass value ", pass_value)
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        if not csv_val:
            print("csv file does not exist, station did not got ip, Test failed")
            allure.attach(name="Csv Data", body="station did not got ip Test failed.")
            assert False
        else:
            allure.attach(name="Csv Data", body=str(list(csv_val["Down"].values())[-1]))
            if list(csv_val["Down"].values())[-1] >= pass_value:
                print("Test passed successfully")
                assert True
            else:
                print("Test failed due to lesser value")
                assert False
        print("Test Completed... Cleaning up Stations")
