import pytest
import allure
import os
import time
import pandas as pd
import logging

pytestmark = [pytest.mark.advance, pytest.mark.atf, pytest.mark.bridge, pytest.mark.report]

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
class TestAtfBridge(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6394", name="WIFI-6394")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.atf_2g
    def test_atf_2g(self, lf_test, lf_tools, station_names_twog):
        allure.attach(name="Definition",
                      body="Airtime Fairness test intends to verify the capacity of Wi-Fi device to ensure the fairness of " \
                           "airtime usage.")
        allure.attach(name="Procedure",
                      body="This test case definition states that Create 2 stations of greenfeild mode and 1 station of legacy mode"
                           " on 2.4Ghz radio. Run TCP download for station_1 as throughpt_1, station_2 as throughpt_2, "
                           "station_2 with attenuation as throughpt_3, station_3 as throughpt_4, UDP download for station_1 + station_2"
                           "of data_rates 40% of throughput_1 and 40% of throughput_2 as throughput_5, station_1 + station_2 with attenuation"
                           "of data_rates 40% of throughput_1 and 40% of throughput_3 as throughput_6, station_1 + station_3"
                           "of data_rates 40% of throughput_1 and 40% of throughput_4 as throughput_7.")
        print("Cleanup existing clients and traffic")
        lf_tools.reset_scenario()
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        station_name = station_names_twog[0]
        sta, thrpt = [], {"sta0_tcp_dl":20,"sta1_tcp_dl":30,"sta1_tcp_dl_atn":None,"sta2_tcp_dl":None,
                        "sta0+1_udp":None,"sta0+1_udp_atn":None,"sta0+2":None}
        no_of_iter = list(thrpt.keys())

        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        atten_serial = lf_test.attenuator_serial_2g_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                          radio=lf_tools.twog_radios[0], atn_val=170,
                                                          sta_mode=0, station_name=[sta[2]], lf_tools_obj=lf_tools)
        atten_serial_split = atten_serial[1].split(".")
        # for i in range(2):
        #     lf_test.attenuator_modify(int(atten_serial_split[2]), i, 0)
        for i in range(len(lf_tools.twog_radios)):
            if i == 2:
                pass
                # mode = 2 will create legacy client
                create_sta = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                                radio=lf_tools.twog_radios[i], station_name=[sta[i]],
                                                                sta_mode=2)
            else:
                # mode = 11 will create bgn-AC client
                create_sta = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                    radio=lf_tools.twog_radios[i], station_name=[sta[i]], sta_mode=11)
            if create_sta == False:
                logging.info(f"Test failed due to no IP for {sta[i]}")
                assert False, f"Test failed due to no IP for {sta[i]}"
        # sta_ip2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
        #                                             radio=radio_name2, station_name=sta[1:2], sta_mode=11)
        else:
            lf_sta = list(create_sta.station_map().keys()) # lf_test.map_existing_stations()
            def wifi_cap(sta=None, down=None, up=0, proto=None, thrpt_key=None, wifi_cap=False, atn=None, l3_trf=False):
                if atn:
                    for i in range(2):
                        lf_test.attenuator_modify(int(atten_serial_split[2]), i, int(atn))
                        time.sleep(0.5)
                if wifi_cap:
                    wct_obj = lf_test.wifi_capacity(instance_name="atf_sta1_greenfieldmode_sta2_atten30dB_2g", mode=mode,
                                      vlan_id=vlan, download_rate=down, batch_size="1", stations=f"{sta}", create_stations=False,
                                      upload_rate=up, protocol=proto, duration="60000", sort="linear")
                    report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
                    lf_tools.attach_report_graphs(report_name=report_name)
                    entries = os.listdir("../reports/" + report_name + '/')
                    if "kpi.csv" in entries:
                        thrpt[thrpt_key] = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)[0][0]
                if l3_trf:
                    lf_test.Client_disconnect(clean_l3_traffic=True)
                    lf_test.layer3_traffic(station_name=sta[0:1], tcp_traff=False, udp_traff=True, start_both_traffic=False,
                                           side_a_min_bps=0, side_b_min_bps=int(down[0]), udp_clean=False)
                    thrpt[thrpt_key] = lf_test.layer3_traffic(station_name=sta[1:2], tcp_traff=False, udp_traff=True,
                                                              start_both_traffic=False, start_traffic_time=60, side_a_min_bps=0,
                                                              side_b_min_bps=int(down[1]), udp_clean=False)[0]

            #station_0 TCP down throughtput
            wifi_cap(down="1Gbps",sta=f"{lf_sta[0]}",up="0Gbps",proto="TCP-IPv4",thrpt_key=f"{no_of_iter[0]}",wifi_cap=True)
            # station_1 TCP down throughtput
            wifi_cap(down="1Gbps", sta=f"{lf_sta[1]}", up="0Gbps", proto="TCP-IPv4", thrpt_key=f"{no_of_iter[1]}",wifi_cap=True)
            # station_1 with medium distance TCP down throughtput
            wifi_cap(down="1Gbps", sta=f"{lf_sta[1]}", up="0Gbps", proto="TCP-IPv4", thrpt_key=f"{no_of_iter[2]}",wifi_cap=True,atn=380)
            # station_2 TCP down throughtput
            wifi_cap(down="1Gbps", sta=f"{lf_sta[2]}", up="0Gbps", proto="TCP-IPv4", thrpt_key=f"{no_of_iter[3]}",wifi_cap=True,atn='170')
            # UDP traffic for station_0 of data-rate 40% of sta0_data_rate and station_1 of data-rate 40% of sta1_data_rate
            wifi_cap(down=[(thrpt["sta0_tcp_dl"] * 0.01) * 4E7 ,(thrpt["sta1_tcp_dl"] * 0.01) * 4E7], sta=sta[0:2], up="0Gbps",
                     thrpt_key=f"{no_of_iter[4]}", l3_trf=True)
            # UDP traffic for station_0 of data-rate 40% of sta0_data_rate and medium distance station_1 of data-rate 40% of sta1_data_rate
            wifi_cap(down=[(thrpt["sta0_tcp_dl"] * 0.01) * 4E7,(thrpt["sta1_tcp_dl_atn"] * 0.01) * 4E7], sta=sta[0:2], up="0Gbps",
                     thrpt_key=f"{no_of_iter[5]}", l3_trf=True,atn=380)
            # UDP traffic for station_0 of data-rate 40% of sta0_data_rate and station_2 of data-rate 40% of sta2_data_rate
            wifi_cap(down=[(thrpt["sta0_tcp_dl"] * 0.01) * 4E7, (thrpt["sta2_tcp_dl"] * 0.01) * 4E7], sta=sta[0:3:2],
                     up="0Gbps", thrpt_key=f"{no_of_iter[6]}", l3_trf=True)
            print("Throughput values: \n",thrpt)
            allure.attach(name="Throughput Data", body="Throughput value : " + str(thrpt))
            lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            if sum(thrpt["sta0+1_udp"]) >= 80 and sum(thrpt["sta0+1_udp_atn"]) >= 80 and sum(thrpt["sta0+2"]) >= 48:
                assert True
            else:
                assert False, "Failed due to Lesser value"
            # lf_tools.attach_report_graphs(report_name=report_name)

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6394", name="WIFI-6394")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.atf_5g
    def test_atf_5g(self, lf_test, lf_tools, station_names_fiveg):
        allure.attach(name="Definition",
                      body="Airtime Fairness test intends to verify the capacity of Wi-Fi device to ensure the fairness of " \
                           "airtime usage.")
        allure.attach(name="Procedure",
                      body="This test case definition states that Create 2 stations of greenfeild mode and 1 station of legacy mode"
                           " on 5Ghz radio. Run TCP download for station_1 as throughpt_1, station_2 as throughpt_2, "
                           "station_2 with attenuation as throughpt_3, station_3 as throughpt_4, UDP download for station_1 + station_2"
                           "of data_rates 40% of throughput_1 and 40% of throughput_2 as throughput_5, station_1 + station_2 with attenuation"
                           "of data_rates 40% of throughput_1 and 40% of throughput_3 as throughput_6, station_1 + station_3"
                           "of data_rates 40% of throughput_1 and 40% of throughput_4 as throughput_7.")
        print("Cleanup existing clients and traffic")
        lf_tools.reset_scenario()
        lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        station_name = station_names_fiveg[0]
        sta, thrpt = [], {"sta0_tcp_dl": 20, "sta1_tcp_dl": 30, "sta1_tcp_dl_atn": None, "sta2_tcp_dl": None,
                          "sta0+1_udp": None, "sta0+1_udp_atn": None, "sta0+2": None}
        no_of_iter = list(thrpt.keys())

        for i in range(3):
            sta.append(station_name + str(i))
        print(sta)
        atten_serial = lf_test.attenuator_serial_5g_radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                          radio=lf_tools.fiveg_radios[0], atn_val=170,
                                                          sta_mode=0, station_name=[sta[2]], lf_tools_obj=lf_tools)
        atten_serial_split = atten_serial[1].split(".")
        for i in range(len(lf_tools.fiveg_radios)):
            if i == 2:
                pass
                # mode = 2 will create legacy client
                create_sta = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                                radio=lf_tools.fiveg_radios[i], station_name=[sta[i]],
                                                                sta_mode=1)
            else:
                # mode = 11 will create bgn-AC client
                create_sta = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
                                                                radio=lf_tools.fiveg_radios[i], station_name=[sta[i]],
                                                                sta_mode=9)
            if create_sta == False:
                logging.info(f"Test failed due to no IP for {sta[i]}")
                assert False, f"Test failed due to no IP for {sta[i]}"
        else:
            lf_sta = list(create_sta.station_map().keys())  # lf_test.map_existing_stations()

            def wifi_cap(sta=None, down=None, up=0, proto=None, thrpt_key=None, wifi_cap=False, atn=None, l3_trf=False):
                if atn:
                    for i in range(2):
                        lf_test.attenuator_modify(int(atten_serial_split[2]), i, int(atn))
                        time.sleep(0.5)
                if wifi_cap:
                    wct_obj = lf_test.wifi_capacity(instance_name="atf_5g", mode=mode, vlan_id=vlan, download_rate=down,
                                                    batch_size="1", stations=f"{sta}", create_stations=False,
                                                    upload_rate=up, protocol=proto, duration="60000", sort="linear")
                    report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
                    lf_tools.attach_report_graphs(report_name=report_name)
                    entries = os.listdir("../reports/" + report_name + '/')
                    if "kpi.csv" in entries:
                        thrpt[thrpt_key] = \
                        lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)[0][0]
                if l3_trf:
                    lf_test.Client_disconnect(clean_l3_traffic=True)
                    lf_test.layer3_traffic(station_name=sta[0:1], tcp_traff=False, udp_traff=True,
                                           start_both_traffic=False,
                                           side_a_min_bps=0, side_b_min_bps=int(down[0]), udp_clean=False)
                    thrpt[thrpt_key] = lf_test.layer3_traffic(station_name=sta[1:2], tcp_traff=False, udp_traff=True,
                                                              start_both_traffic=False, start_traffic_time=60,
                                                              side_a_min_bps=0,
                                                              side_b_min_bps=int(down[1]), udp_clean=False)[0]

            # station_0 TCP down throughtput
            wifi_cap(down="1Gbps", sta=f"{lf_sta[0]}", up="0Gbps", proto="TCP-IPv4", thrpt_key=f"{no_of_iter[0]}",
                     wifi_cap=True)
            # station_1 TCP down throughtput
            wifi_cap(down="1Gbps", sta=f"{lf_sta[1]}", up="0Gbps", proto="TCP-IPv4", thrpt_key=f"{no_of_iter[1]}",
                     wifi_cap=True)
            # station_1 with medium distance TCP down throughtput
            wifi_cap(down="1Gbps", sta=f"{lf_sta[1]}", up="0Gbps", proto="TCP-IPv4", thrpt_key=f"{no_of_iter[2]}",
                     wifi_cap=True, atn=250)
            # station_2 TCP down throughtput
            wifi_cap(down="1Gbps", sta=f"{lf_sta[2]}", up="0Gbps", proto="TCP-IPv4", thrpt_key=f"{no_of_iter[3]}",
                     wifi_cap=True, atn='170')
            # UDP traffic for station_0 of data-rate 40% of sta0_data_rate and station_1 of data-rate 40% of sta1_data_rate
            wifi_cap(down=[(thrpt["sta0_tcp_dl"] * 0.01) * 4E7, (thrpt["sta1_tcp_dl"] * 0.01) * 4E7], sta=sta[0:2],
                     up="0Gbps", thrpt_key=f"{no_of_iter[4]}", l3_trf=True)
            # UDP traffic for station_0 of data-rate 40% of sta0_data_rate and medium distance station_1 of data-rate 40% of sta1_data_rate
            wifi_cap(down=[(thrpt["sta0_tcp_dl"] * 0.01) * 4E7, (thrpt["sta1_tcp_dl_atn"] * 0.01) * 4E7], sta=sta[0:2],
                     up="0Gbps", thrpt_key=f"{no_of_iter[5]}", l3_trf=True, atn=250)
            # UDP traffic for station_0 of data-rate 40% of sta0_data_rate and station_2 of data-rate 40% of sta2_data_rate
            wifi_cap(down=[(thrpt["sta0_tcp_dl"] * 0.01) * 4E7, (thrpt["sta2_tcp_dl"] * 0.01) * 4E7], sta=sta[0:3:2],
                     up="0Gbps", thrpt_key=f"{no_of_iter[6]}", l3_trf=True)
            print("Throughput values: \n", thrpt)
            allure.attach(name="Throughput Data", body="Throughput value : " + str(thrpt))
            lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            if sum(thrpt["sta0+1_udp"]) >= 500 and sum(thrpt["sta0+1_udp_atn"]) >= 470 and sum(thrpt["sta0+2"]) >= 260:
                assert True
            else:
                assert False, "Failed due to Lesser value"
            # lf_tools.attach_report_graphs(report_name=report_name)

    # @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6395", name="WIFI-6395")
    # @pytest.mark.wpa2_personal
    # @pytest.mark.twog
    # @pytest.mark.atf_sta1_greenfieldmode_sta2_legacymode_2g
    # def test_atf_sta1_greenfieldmode_sta2_legacymode_2g(self, lf_test, lf_tools, station_names_twog):
    #     # lf_tools.reset_scenario()
    #     profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     mode = "BRIDGE"
    #     vlan = 1
    #     station_name = station_names_twog[0]
    #     radio_name1 = lf_tools.twog_radios[0]
    #     radio_name2 = lf_tools.twog_radios[1]
    #     sta = []
    #     for i in range(2):
    #         sta.append(station_name + str(i))
    #     print(sta)
    #     sta_ip1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
    #                                                  radio=radio_name1, station_name=sta[0:1], sta_mode=11)
    #     sta_ip2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
    #                                                  radio=radio_name2, station_name=sta[1:2], sta_mode=2)
    #     if (not sta_ip1) or (not sta_ip2):
    #         print("test failed due to no station ip")
    #         assert False
    #     lf_test.local_realm.station_map()
    #     wct_obj = lf_test.wifi_capacity(instance_name="atf_sta1_greenfieldmode_sta2_legacymode_2g", mode=mode, vlan_id=vlan,
    #                                     download_rate="1Gbps", batch_size="1,2", stations=f"{sta[0]}", create_stations=False,
    #                                     upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000", sort="linear")
    #     lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
    #     report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
    #     lf_tools.attach_report_graphs(report_name=report_name)
    #
    # @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6396", name="WIFI-6396")
    # @pytest.mark.wpa2_personal
    # @pytest.mark.fiveg
    # @pytest.mark.atf_sta1_greenfieldmode_sta2_atten30dB_5g
    # def test_atf_sta1_greenfieldmode_sta2_atten30dB_5g(self, lf_test, lf_tools, station_names_fiveg):
    #     lf_tools.reset_scenario()
    #     profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
    #     ssid_name = profile_data["ssid_name"]
    #     mode = "BRIDGE"
    #     vlan = 1
    #     station_name = station_names_fiveg[0]
    #     radio_name1 = lf_tools.fiveg_radios[0]
    #     radio_name2 = lf_tools.fiveg_radios[1]
    #     sta = []
    #     for i in range(2):
    #         sta.append(station_name + str(i))
    #     print(sta)
    #     atten_serial = lf_test.attenuator_serial_5g_radio(ssid=ssid_name, passkey=profile_data["security_key"],
    #                                                       station_name=station_names_fiveg, lf_tools_obj=lf_tools)
    #     atten_serial_split = atten_serial[1].split(".")
    #     sta_ip1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
    #                                                  radio=radio_name1, station_name=sta[0:1], sta_mode=9)
    #     sta_ip2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
    #                                                  radio=radio_name2, station_name=sta[1:2], sta_mode=9)
    #     if (not sta_ip1) or (not sta_ip2):
    #         print("test failed due to no station ip")
    #         assert False
    #     for i in range(2):
    #         lf_test.attenuator_modify(int(atten_serial_split[2]), i, 300)
    #         time.sleep(0.5)
    #     wct_obj = lf_test.wifi_capacity(instance_name="atf_sta1_greenfieldmode_sta2_atten30dB_5g", mode=mode,
    #                                     vlan_id=vlan,
    #                                     download_rate="1Gbps", batch_size="1,2",
    #                                     upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000", sort="linear")
    #     lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
    #     report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
    #     lf_tools.attach_report_graphs(report_name=report_name)
    #
    # @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6397", name="WIFI-6397")
    # @pytest.mark.wpa2_personal
    # @pytest.mark.fiveg
    # @pytest.mark.atf_sta1_greenfieldmode_sta2_legacymode_5g
    # def test_atf_sta1_greenfieldmode_sta2_legacymode_5g(self, lf_test, lf_tools, station_names_fiveg):
    #     lf_tools.reset_scenario()
    #     profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
    #     ssid_name = profile_data["ssid_name"]
    #     mode = "BRIDGE"
    #     vlan = 1
    #     station_name = station_names_fiveg[0]
    #     radio_name1 = lf_tools.fiveg_radios[0]
    #     radio_name2 = lf_tools.fiveg_radios[1]
    #     sta = []
    #     for i in range(2):
    #         sta.append(station_name + str(i))
    #     print(sta)
    #     sta_ip1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
    #                                                  radio=radio_name1, station_name=sta[0:1], sta_mode=9)
    #     sta_ip2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
    #                                                  radio=radio_name2, station_name=sta[1:2], sta_mode=1)
    #     if (not sta_ip1) or (not sta_ip2):
    #         print("test failed due to no station ip")
    #         assert False
    #     wct_obj = lf_test.wifi_capacity(instance_name="atf_sta1_greenfieldmode_sta2_legacymode_5g", mode=mode,
    #                                     vlan_id=vlan,
    #                                     download_rate="1Gbps", batch_size="1,2",
    #                                     upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000", sort="linear")
    #     lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
    #     report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
    #     lf_tools.attach_report_graphs(report_name=report_name)