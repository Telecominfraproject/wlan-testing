"""

    Performance Test: throughput test under various combinations: VLAN Mode
    pytest -m "throughput_benchmark_test and vlan" -s -vvv --skip-testrail --testbed=basic-01


"""
import os
import time

import pytest
import allure

pytestmark = [pytest.mark.performance, pytest.mark.throughput_benchmark_test, pytest.mark.vlan] # pytest.mark.usefixtures("setup_test_run")]


setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["is2dot4GHz"],"vlan":100},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something", "vlan": 125},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
                 "security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something","vlan": 100},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something","vlan": 100}]},
    "rf": {
        "is5GHz": {"channelBandwidth": "is20MHz"},
        "is5GHzL": {"channelBandwidth": "is20MHz"},
        "is5GHzU": {"channelBandwidth": "is20MHz"}
    },
    "radius": False
}

@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")

@pytest.mark.parametrize(
    "create_vlan",
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("create_vlan")
@pytest.mark.Mhz20
class TestThroughputUnderCombinationsVlan20MHz(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.upstream
    @pytest.mark.nss2
    @pytest.mark.udp
    def test_client_wpa2_personal_2g_up_nss2_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_twog, create_lanforge_chamberview_dut,
                                     get_configuration):
        """Dataplane THroughput VLAN Mode
           pytest -m "throughput_benchmark_test and VLAN and wpa2_personal and twog and upstream "
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = 100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Receive'], ['traffic_types: UDP'],['bandw_options: 20'], ['spatial_streams: 2']]
        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
                                       vlan_id=vlan, dut_name=dut_name,raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False


    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.upstream
    @pytest.mark.nss2
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_up_nss2_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Receive'], ['traffic_types: UDP'], ['bandw_options: 20'], ['spatial_streams: 2']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                              vlan_id=vlan, dut_name=dut_name,raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/"+report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf, name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.downstream
    @pytest.mark.nss2
    @pytest.mark.udp
    def test_client_wpa2_personal_2g_down_nss2_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_twog, create_lanforge_chamberview_dut,
                                     get_configuration):
        """Dataplane THroughput VLAN Mode
           pytest -m "throughput_benchmark_test and VLAN and wpa2_personal and twog and downstream "
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit'], ['traffic_types: UDP'],
               ['bandw_options: 20'], ['spatial_streams: 2']]
        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.downstream
    @pytest.mark.nss2
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_down_nss2_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit'], ['traffic_types: UDP'],
               ['bandw_options: 20'], ['spatial_streams: 2']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.bidirectional
    @pytest.mark.nss2
    @pytest.mark.udp
    def test_client_wpa2_personal_2g_bi_nss2_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_twog, create_lanforge_chamberview_dut,
                                     get_configuration):
        """Dataplane THroughput VLAN Mode
           pytest -m "throughput_benchmark_test and VLAN and wpa2_personal and twog and bidirectional "
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit;DUT Receive'], ['traffic_types: UDP'],
               ['bandw_options: 20'], ['spatial_streams: 2']]
        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.bidirectional
    @pytest.mark.nss2
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_bi_nss2_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit;DUT Receive'], ['traffic_types: UDP'],
               ['bandw_options: 20'], ['spatial_streams: 2']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.upstream
    @pytest.mark.nss2
    @pytest.mark.tcp
    def test_client_wpa2_personal_2g_up_nss2_tcp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_twog, create_lanforge_chamberview_dut,
                                     get_configuration):
        """Dataplane THroughput VLAN Mode
           pytest -m "throughput_benchmark_test and VLAN and wpa2_personal and twog and upstream and tcp "
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Receive'], ['traffic_types: TCP'],
               ['bandw_options: 20'], ['spatial_streams: 2']]
        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.upstream
    @pytest.mark.nss2
    @pytest.mark.tcp
    def test_client_wpa2_personal_5g_up_nss2_tcp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Receive'], ['traffic_types: TCP'],
               ['bandw_options: 20'], ['spatial_streams: 2']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.downstream
    @pytest.mark.nss2
    @pytest.mark.tcp
    def test_client_wpa2_personal_2g_down_nss2_tcp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_twog, create_lanforge_chamberview_dut,
                                     get_configuration):
        """Dataplane THroughput VLAN Mode
           pytest -m "throughput_benchmark_test and VLAN and wpa2_personal and twog and downstream and tcp"
           jira-WIFI-2564
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit'], ['traffic_types: TCP'],
               ['bandw_options: 20'], ['spatial_streams: 2']]
        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.downstream
    @pytest.mark.nss2
    @pytest.mark.tcp
    def test_client_wpa2_personal_5g_down_nss2_tcp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit'], ['traffic_types: TCP'],
               ['bandw_options: 20'], ['spatial_streams: 2']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.bidirectional
    @pytest.mark.nss2
    @pytest.mark.tcp
    def test_client_wpa2_personal_2g_bi_nss2_tcp(self, get_vif_state,
                                     lf_test, create_vlan , station_names_twog, create_lanforge_chamberview_dut,
                                     get_configuration):
        """Dataplane THroughput VLAN Mode
           pytest -m "throughput_benchmark_test and VLAN and wpa2_personal and twog and bidirectional "
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit;DUT Receive'], ['traffic_types: TCP'],
               ['bandw_options: 20'], ['spatial_streams: 2']]
        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.bidirectional
    @pytest.mark.nss2
    @pytest.mark.tcp
    def test_client_wpa2_personal_5g_bi_nss2_tcp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit;DUT Receive'], ['traffic_types: TCP'],
               ['bandw_options: 20'], ['spatial_streams: 2']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["is2dot4GHz"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
                 "security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something","vlan": 100},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something","vlan": 100}]},
    "rf": {
        "is5GHz": {"channelBandwidth": "is80MHz"},
        "is5GHzL": {"channelBandwidth": "is80MHz"},
        "is5GHzU": {"channelBandwidth": "is80MHz"}
    },
    "radius": False
}

@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.parametrize(
    "create_vlan",
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("create_vlan")

@pytest.mark.Mhz80
class TestThroughputUnderCombinationsVLAN80MHz(object):


    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.upstream
    @pytest.mark.nss2
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_up_nss2_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Dataplane THroughput VLAN Mode
                   pytest -m "throughput_benchmark_test and VLAN and Mhz80 and wpa2_personal and fiveg and upstream and nss2 and udp "
                   jira-wifi-2566
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Receive'], ['traffic_types: UDP'],
               ['bandw_options: 80'], ['spatial_streams: 2']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.downstream
    @pytest.mark.nss2
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_down_nss2_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Dataplane THroughput VLAN Mode
                           pytest -m "throughput_benchmark_test and VLAN and Mhz80 and wpa2_personal and fiveg and downstream and nss2 and udp "
                           jira-wifi-2567
                """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit'], ['traffic_types: UDP'],
               ['bandw_options: 80'], ['spatial_streams: 2']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.bidirectional
    @pytest.mark.nss2
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_bi_nss2_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit;DUT Receive'], ['traffic_types: UDP'],
               ['bandw_options: 80'], ['spatial_streams: 2']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.upstream
    @pytest.mark.nss2
    @pytest.mark.tcp
    def test_client_wpa2_personal_5g_up_nss2_tcp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Receive'], ['traffic_types: TCP'],
               ['bandw_options: 80'], ['spatial_streams: 2']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.downstream
    @pytest.mark.nss2
    @pytest.mark.tcp
    def test_client_wpa2_personal_5g_down_nss2_tcp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit'], ['traffic_types: TCP'],
               ['bandw_options: 80'], ['spatial_streams: 2']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.bidirectional
    @pytest.mark.nss2
    @pytest.mark.tcp
    def test_client_wpa2_personal_2g_bi_nss2_tcp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_twog, create_lanforge_chamberview_dut,
                                     get_configuration):
        """Dataplane THroughput VLAN Mode
           pytest -m "throughput_benchmark_test and VLAN and wpa2_personal and twog and bidirectional "
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit;DUT Receive'], ['traffic_types: TCP'],
               ['bandw_options: 80'], ['spatial_streams: 2']]
        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.upstream
    @pytest.mark.nss3
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_up_nss3_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Dataplane THroughput VLAN Mode
                   pytest -m "throughput_benchmark_test and VLAN and Mhz80 and wpa2_personal and fiveg and upstream and nss2 and udp and nss3"
                   jira-wifi-2572
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Receive'], ['traffic_types: UDP'],
               ['bandw_options: 80'], ['spatial_streams: 3']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.downstream
    @pytest.mark.nss3
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_down_nss3_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Dataplane THroughput VLAN Mode
                           pytest -m "throughput_benchmark_test and VLAN and Mhz80 and wpa2_personal and fiveg and downstream and nss2 and udp and nss3 "
                           jira-wifi-2573
                """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit'], ['traffic_types: UDP'],
               ['bandw_options: 80'], ['spatial_streams: 3']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.bidirectional
    @pytest.mark.nss3
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_bi_nss3_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit;DUT Receive'], ['traffic_types: UDP'],
               ['bandw_options: 80'], ['spatial_streams: 3']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.upstream
    @pytest.mark.nss3
    @pytest.mark.tcp
    def test_client_wpa2_personal_5g_up_nss3_tcp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Receive'], ['traffic_types: TCP'],
               ['bandw_options: 80'], ['spatial_streams: 3']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.downstream
    @pytest.mark.nss3
    @pytest.mark.tcp
    def test_client_wpa2_personal_5g_down_nss3_tcp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit'], ['traffic_types: TCP'],
               ['bandw_options: 80'], ['spatial_streams: 3']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.bidirectional
    @pytest.mark.nss3
    @pytest.mark.tcp
    def test_client_wpa2_personal_5g_bi_nss3_tcp(self, get_vif_state,
                                                 lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut,
                                                 get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit;DUT Receive'], ['traffic_types: TCP'],
               ['bandw_options: 80'], ['spatial_streams: 3']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False


setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["is2dot4GHz"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
                 "security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something","vlan": 100},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something","vlan": 100}]},
    "rf": {
        "is5GHz": {"channelBandwidth": "is160MHz"},
        "is5GHzL": {"channelBandwidth": "is160MHz"},
        "is5GHzU": {"channelBandwidth": "is160MHz"}
    },
    "radius": False
}

@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.parametrize(
    "create_vlan",
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("create_vlan")

@pytest.mark.Mhz160
class TestThroughputUnderCombinationsVLAN160MHz(object):


    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.upstream
    @pytest.mark.nss3
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_up_nss3_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Dataplane THroughput VLAN Mode
                   pytest -m "throughput_benchmark_test and VLAN and Mhz80 and wpa2_personal and fiveg and upstream and nss2 and udp "
                   jira-wifi-2578
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Receive'], ['traffic_types: UDP'],
               ['bandw_options: 160'], ['spatial_streams: 3']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.downstream
    @pytest.mark.nss3
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_down_nss3_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Dataplane THroughput VLAN Mode
                           pytest -m "throughput_benchmark_test and VLAN and Mhz80 and wpa2_personal and fiveg and downstream and nss2 and udp "
                           jira-wifi-2567
                """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit'], ['traffic_types: UDP'],
               ['bandw_options: 160'], ['spatial_streams: 3']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.bidirectional
    @pytest.mark.nss3
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_bi_nss3_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit;DUT Receive'], ['traffic_types: UDP'],
               ['bandw_options: 160'], ['spatial_streams: 3']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.upstream
    @pytest.mark.nss3
    @pytest.mark.tcp
    def test_client_wpa2_personal_5g_up_nss3_tcp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Receive'], ['traffic_types: TCP'],
               ['bandw_options: 160'], ['spatial_streams: 3']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.upstream
    @pytest.mark.nss4
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_up_nss4_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Receive'], ['traffic_types: UDP'],
               ['bandw_options: 160'], ['spatial_streams: 4']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.downstream
    @pytest.mark.nss4
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_down_nss4_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Dataplane THroughput VLAN Mode
                           pytest -m "throughput_benchmark_test and VLAN and Mhz80 and wpa2_personal and fiveg and downstream and nss2 and udp "
                           jira-wifi-2567
                """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit'], ['traffic_types: UDP'],
               ['bandw_options: 160'], ['spatial_streams: 4']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.bidirectional
    @pytest.mark.nss4
    @pytest.mark.udp
    def test_client_wpa2_personal_5g_bi_nss4_udp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit;DUT Receive'], ['traffic_types: UDP'],
               ['bandw_options: 160'], ['spatial_streams: 4']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.upstream
    @pytest.mark.nss4
    @pytest.mark.tcp
    def test_client_wpa2_personal_5g_up_nss4_tcp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Receive'], ['traffic_types: TCP'],
               ['bandw_options: 160'], ['spatial_streams: 4']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.downstream
    @pytest.mark.nss4
    @pytest.mark.tcp
    def test_client_wpa2_personal_5g_down_nss4_tcp(self, get_vif_state,
                                     lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit'], ['traffic_types: TCP'],
               ['bandw_options: 160'], ['spatial_streams: 4']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.bidirectional
    @pytest.mark.nss4
    @pytest.mark.tcp
    def test_client_wpa2_personal_5g_bi_nss4_tcp(self, get_vif_state,
                                                 lf_test, create_vlan, station_names_fiveg, create_lanforge_chamberview_dut,
                                                 get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan =100
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)

        val = [['pkts: 60'], ['cust_pkt_sz: 88 '], ['directions: DUT Transmit;DUT Receive'], ['traffic_types: TCP'],
               ['bandw_options: 160'], ['spatial_streams: 4']]

        if station:
            time.sleep(3)
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode, instance_name="TIP3_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_data=val)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False
