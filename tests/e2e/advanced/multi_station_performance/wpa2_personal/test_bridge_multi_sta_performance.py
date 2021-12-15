import pytest
import allure
import os
import time
import pandas as pd

pytestmark = [pytest.mark.advance, pytest.mark.multistaperf, pytest.mark.bridge]

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
class TestMultiStaPerfBridge(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5733", name="WIFI-5733")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_upload_10dB_dis_nss1_2g
    def test_multi_station_tcp_upload_10dB_dis_nss1_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
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
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_upload_10dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="3",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")


        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if sta_ip:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5844", name="WIFI-5844")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_upload_10dB_40dB_dis_nss1_2g
    def test_multi_station_tcp_upload_10dB_40dB_dis_nss1_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_upload_10dB_40dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="3,6",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")


        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5877", name="WIFI-5877")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_upload_10dB_40dB_50dB_dis_nss1_2g
    def test_multi_station_tcp_upload_10dB_40dB_50dB_dis_nss1_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
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

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_upload_10dB_40dB_50dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="3,6,9",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5878", name="WIFI-5878")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_download_10dB_dis_nss1_5g
    def test_multi_station_tcp_download_10dB_dis_nss1_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
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
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_download_10dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="3",
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if sta_ip:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5879", name="WIFI-5879")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_download_10dB_40dB_dis_nss1_5g
    def test_multi_station_tcp_download_10dB_40dB_dis_nss1_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_download_10dB_40dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="3,6",
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5880", name="WIFI-5880")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_download_10dB_40dB_50dB_dis_nss1_5g
    def test_multi_station_tcp_download_10dB_40dB_50dB_dis_nss1_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
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

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_download_10dB_40dB_50dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="3,6,9",
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5881", name="WIFI-5881")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_download_10dB_dis_nss1_2g
    def test_multi_station_tcp_download_10dB_dis_nss1_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
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
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_download_10dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="3",
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if sta_ip:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5882", name="WIFI-5882")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_download_10dB_40dB_dis_nss1_2g
    def test_multi_station_tcp_download_10dB_40dB_dis_nss1_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_download_10dB_40dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="3,6",
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6083", name="WIFI-6083")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_download_10dB_40dB_50dB_dis_nss1_2g
    def test_multi_station_tcp_download_10dB_40dB_50dB_dis_nss1_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
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

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_download_10dB_40dB_50dB_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="3,6,9",
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6086", name="WIFI-6086")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_upload_10dB_dis_nss1_5g
    def test_multi_station_tcp_upload_10dB_dis_nss1_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
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
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_upload_10dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="3",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if sta_ip:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6087", name="WIFI-6087")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_upload_10dB_40dB_dis_nss1_5g
    def test_multi_station_tcp_upload_10dB_40dB_dis_nss1_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_upload_10dB_40dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="3,6",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6088", name="WIFI-6088")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_upload_10dB_40dB_50dB_dis_nss1_5g
    def test_multi_station_tcp_upload_10dB_40dB_50dB_dis_nss1_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
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

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_upload_10dB_40dB_50dB_dis_nss1_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="3,6,9",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5883", name="WIFI-5883")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_upload_10dB_dis_nss2_2g
    def test_multi_station_tcp_upload_10dB_dis_nss2_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
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
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_upload_10dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="3",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if sta_ip:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5887", name="WIFI-5887")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_upload_10dB_40dB_dis_nss2_2g
    def test_multi_station_tcp_upload_10dB_40dB_dis_nss2_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_upload_10dB_40dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="3,6",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5886", name="WIFI-5886")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_upload_10dB_40dB_50dB_dis_nss2_2g
    def test_multi_station_tcp_upload_10dB_40dB_50dB_dis_nss2_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
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

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_upload_10dB_40dB_50dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="3,6,9",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5892", name="WIFI-5892")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_download_10dB_dis_nss2_5g
    def test_multi_station_tcp_download_10dB_dis_nss2_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
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
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_download_10dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="3",
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if sta_ip:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5891", name="WIFI-5891")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_download_10dB_40dB_dis_nss2_5g
    def test_multi_station_tcp_download_10dB_40dB_dis_nss2_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_download_10dB_40dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="3,6",
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5895", name="WIFI-5895")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_download_10dB_40dB_50dB_dis_nss2_5g
    def test_multi_station_tcp_download_10dB_40dB_50dB_dis_nss2_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
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

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_download_10dB_40dB_50dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="3,6,9",
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5890", name="WIFI-5890")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_download_10dB_dis_nss2_2g
    def test_multi_station_tcp_download_10dB_dis_nss2_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
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
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_download_10dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="3",
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if sta_ip:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5889", name="WIFI-5889")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_download_10dB_40dB_dis_nss2_2g
    def test_multi_station_tcp_download_10dB_40dB_dis_nss2_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_download_10dB_40dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="3,6",
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5888", name="WIFI-5888")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.tcp_download_10dB_40dB_50dB_dis_nss2_2g
    def test_multi_station_tcp_download_10dB_40dB_50dB_dis_nss2_2g(self, lf_test, lf_tools, station_names_twog):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_twog[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
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

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_download_10dB_40dB_50dB_dis_nss2_2g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="3,6,9",
                                        upload_rate="0Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5884", name="WIFI-5884")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_upload_10dB_dis_nss2_5g
    def test_multi_station_tcp_upload_10dB_dis_nss2_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
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
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_upload_10dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="3",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if sta_ip:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5885", name="WIFI-5885")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_upload_10dB_40dB_dis_nss2_5g
    def test_multi_station_tcp_upload_10dB_40dB_dis_nss2_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
                print("test failed due to no station ip")
                assert False
            time.sleep(0.5)
        for i in range(4):
            lf_test.attenuator_modify(int(atten_sr1[2]), i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_test.attenuator_modify(int(atten_sr2[2]), i, 400)
            time.sleep(0.5)

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_upload_10dB_40dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="3,6",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5896", name="WIFI-5896")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.tcp_upload_10dB_40dB_50dB_dis_nss2_5g
    def test_multi_station_tcp_upload_10dB_40dB_50dB_dis_nss2_5g(self, lf_test, lf_tools, station_names_fiveg):
        lf_tools.reset_scenario()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        pass_condn = True
        station_name = station_names_fiveg[0]
        atten_sr = lf_test.attenuator_serial()
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
                pass_condn = False
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

        wct_obj = lf_test.wifi_capacity(instance_name="tcp_upload_10dB_40dB_50dB_dis_nss2_5g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="3,6,9",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="120000", sort="linear")
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        if pass_condn:
            assert True
