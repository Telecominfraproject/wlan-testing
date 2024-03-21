"""

    Performance Test: Throughput vs Various Pkt Size Test: Bridge Mode
    pytest -m "throughput_vs_pkt and bridge"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.throughput_vs_pkt, pytest.mark.Bridge, pytest.mark.wpa3,]
              # pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]},

    "rf": {},
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@allure.parent_suite("Throughput Benchmark Test: Throughput v/s Varying Packet Sizes Tests : WPA3 Personal Security")
@allure.suite("Bridge Mode")
@allure.sub_suite("2.4GHz Band")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestThroughputVsPktWpa3Bridge2G(object):
    """Throughput vs Various Pkt Size Test Bridge mode
       pytest -m "throughput_vs_pkt and bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2549", name="WIFI-2549")
    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @pytest.mark.pkt60
    def test_client_wpa3_personal_pkt_bridge_60_2g(self, lf_tools, lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                            get_configuration):
        """Throughput Vs Pkt Sizes Bridge Mode
           pytest -m "throughput_vs_pkt and bridge and wpa3_personal and twog and pkt60"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 60'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA3_2G_60",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            # entries = os.listdir("../reports/" + report_name + '/')
            # pdf = False
            # for i in entries:
            #     if ".pdf" in i:
            #         pdf = i
            # if pdf:
            #     allure.attach.file(source="../reports/" + report_name + "/" + pdf,
            #                        name=get_configuration["access_point"][0]["model"] + "_dataplane")
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2549", name="WIFI-2549")
    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @pytest.mark.pkt142
    def test_client_wpa3_personal_pkt_bridge_142_2g(self, lf_tools, lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                             get_configuration):
        """Throughput Vs Pkt Sizes Bridge Mode
           pytest -m "throughput_vs_pkt and bridge and wpa3_personal and twog and pkt142"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 142'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA3_2G_142",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            # entries = os.listdir("../reports/" + report_name + '/')
            # pdf = False
            # for i in entries:
            #     if ".pdf" in i:
            #         pdf = i
            # if pdf:
            #     allure.attach.file(source="../reports/" + report_name + "/" + pdf,
            #                        name=get_configuration["access_point"][0]["model"] + "_dataplane")
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2549", name="WIFI-2549")
    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @pytest.mark.pkt256
    def test_client_wpa3_personal_pkt_bridge_256_2g(self, lf_tools, lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                             get_configuration):
        """Throughput Vs Pkt Sizes Bridge Mode
           pytest -m "throughput_vs_pkt and bridge and wpa3_personal and twog and pkt256"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 256'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA3_2G_256",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            # entries = os.listdir("../reports/" + report_name + '/')
            # pdf = False
            # for i in entries:
            #     if ".pdf" in i:
            #         pdf = i
            # if pdf:
            #     allure.attach.file(source="../reports/" + report_name + "/" + pdf,
            #                        name=get_configuration["access_point"][0]["model"] + "_dataplane")
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2549", name="WIFI-2549")
    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @pytest.mark.pkt512
    def test_client_wpa3_personal_pkt_bridge_512_2g(self, lf_tools, lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                             get_configuration):
        """Throughput Vs Pkt Sizes Bridge Mode
           pytest -m "throughput_vs_pkt and bridge and wpa3_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 512'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA3_2G_512",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            # entries = os.listdir("../reports/" + report_name + '/')
            # pdf = False
            # for i in entries:
            #     if ".pdf" in i:
            #         pdf = i
            # if pdf:
            #     allure.attach.file(source="../reports/" + report_name + "/" + pdf,
            #                        name=get_configuration["access_point"][0]["model"] + "_dataplane")
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2549", name="WIFI-2549")
    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @pytest.mark.pkt1024
    def test_client_wpa3_personal_pkt_bridge_1024_2g(self, lf_tools, lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                              get_configuration):
        """Throughput Vs Pkt Sizes Bridge Mode
           pytest -m "throughput_vs_pkt and bridge and wpa3_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 1024'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA3_2G_1024",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            # entries = os.listdir("../reports/" + report_name + '/')
            # pdf = False
            # for i in entries:
            #     if ".pdf" in i:
            #         pdf = i
            # if pdf:
            #     allure.attach.file(source="../reports/" + report_name + "/" + pdf,
            #                        name=get_configuration["access_point"][0]["model"] + "_dataplane")
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2549", name="WIFI-2549")
    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @pytest.mark.pktMTU
    def test_client_wpa3_personal_pkt_bridge_MTU_2g(self, lf_tools, lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                             get_configuration):
        """Throughput Vs Pkt Sizes Bridge Mode
           pytest -m "throughput_vs_pkt and bridge and wpa3_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: MTU'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA3_2G_MTU",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            # entries = os.listdir("../reports/" + report_name + '/')
            # pdf = False
            # for i in entries:
            #     if ".pdf" in i:
            #         pdf = i
            # if pdf:
            #     allure.attach.file(source="../reports/" + report_name + "/" + pdf,
            #                        name=get_configuration["access_point"][0]["model"] + "_dataplane")
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False


setup_params_5g = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@allure.parent_suite("Throughput Benchmark Test: Throughput v/s Varying Packet Sizes Tests : WPA3 Personal Security")
@allure.suite("Bridge Mode")
@allure.sub_suite("5GHz Band")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_5g],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestThroughputVsPktBridgeWpa35G(object):
    """Throughput vs Various Pkt Size Test Bridge mode
       pytest -m "throughput_vs_pkt and bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2549", name="WIFI-2549")
    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @pytest.mark.pkt60
    def test_client_wpa3_personal_pkt_bridge_60_5g(self, lf_tools, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                            get_configuration):
        """Throughput Vs Pkt Sizes Bridge Mode
           pytest -m "throughput_vs_pkt and bridge and wpa3_personal and fiveg"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 60'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA3_5G_60",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            # entries = os.listdir("../reports/" + report_name + '/')
            # pdf = False
            # for i in entries:
            #     if ".pdf" in i:
            #         pdf = i
            # if pdf:
            #     allure.attach.file(source="../reports/" + report_name + "/" + pdf,
            #                        name=get_configuration["access_point"][0]["model"] + "_dataplane")
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2549", name="WIFI-2549")
    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @pytest.mark.pkt142
    def test_client_wpa3_personal_pkt_bridge_142_5g(self, lf_tools, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                             get_configuration):
        """Throughput Vs Pkt Sizes Bridge Mode
           pytest -m "throughput_vs_pkt and bridge and wpa3_personal and fiveg"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 142'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA3_5G_142",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            # entries = os.listdir("../reports/" + report_name + '/')
            # pdf = False
            # for i in entries:
            #     if ".pdf" in i:
            #         pdf = i
            # if pdf:
            #     allure.attach.file(source="../reports/" + report_name + "/" + pdf,
            #                        name=get_configuration["access_point"][0]["model"] + "_dataplane")
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2549", name="WIFI-2549")
    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @pytest.mark.pkt256
    def test_client_wpa3_personal_pkt_bridge_256_5g(self, lf_tools, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                             get_configuration):
        """Throughput Vs Pkt Sizes Bridge Mode
           pytest -m "throughput_vs_pkt and bridge and wpa3_personal and fiveg"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 256'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA3_5G_256",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            # entries = os.listdir("../reports/" + report_name + '/')
            # pdf = False
            # for i in entries:
            #     if ".pdf" in i:
            #         pdf = i
            # if pdf:
            #     allure.attach.file(source="../reports/" + report_name + "/" + pdf,
            #                        name=get_configuration["access_point"][0]["model"] + "_dataplane")
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2549", name="WIFI-2549")
    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @pytest.mark.pkt512
    def test_client_wpa3_personal_pkt_bridge_512_5g(self, lf_tools, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                             get_configuration):
        """Throughput Vs Pkt Sizes Bridge Mode
           pytest -m "throughput_vs_pkt and bridge and wpa3_personal and fiveg"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 512'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA3_5G_512",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            # entries = os.listdir("../reports/" + report_name + '/')
            # pdf = False
            # for i in entries:
            #     if ".pdf" in i:
            #         pdf = i
            # if pdf:
            #     allure.attach.file(source="../reports/" + report_name + "/" + pdf,
            #                        name=get_configuration["access_point"][0]["model"] + "_dataplane")
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2549", name="WIFI-2549")
    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @pytest.mark.pkt1024
    def test_client_wpa3_personal_pkt_bridge_1024_5g(self, lf_tools, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                              get_configuration):
        """Throughput Vs Pkt Sizes Bridge Mode
           pytest -m "throughput_vs_pkt and bridge and wpa3_personal and fiveg"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 1024'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA3_5G_1024",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            # entries = os.listdir("../reports/" + report_name + '/')
            # pdf = False
            # for i in entries:
            #     if ".pdf" in i:
            #         pdf = i
            # if pdf:
            #     allure.attach.file(source="../reports/" + report_name + "/" + pdf,
            #                        name=get_configuration["access_point"][0]["model"] + "_dataplane")
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2549", name="WIFI-2549")
    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @pytest.mark.pktMTU
    def test_client_wpa3_personal_pkt_bridge_MTU_5g(self, lf_tools, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                             get_configuration):
        """Throughput Vs Pkt Sizes Bridge Mode
           pytest -m "throughput_vs_pkt and bridge and wpa3_personal and fiveg"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: MTU'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA3_5G_MTU",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            # entries = os.listdir("../reports/" + report_name + '/')
            # pdf = False
            # for i in entries:
            #     if ".pdf" in i:
            #         pdf = i
            # if pdf:
            #     allure.attach.file(source="../reports/" + report_name + "/" + pdf,
            #                        name=get_configuration["access_point"][0]["model"] + "_dataplane")
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False
