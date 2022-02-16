"""

    Performance Test: Throughput vs Various Pkt Size Test : Nat Mode
    pytest -m "throughput_vs_pkt and nat"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.throughput_vs_pkt, pytest.mark.nat, pytest.mark.wpa2]


setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestThroughputVsPktWpa2Nat2G(object):
    """Throughput vs Various Pkt Size Test nat mode
       pytest -m "throughput_vs_pkt and nat"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2547", name="WIFI-2547")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.pkt60
    def test_client_wpa2_personal_nat_pkt_60_2g(self, lf_tools, lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                   get_configuration):
        """Throughput Vs Pkt Sizes Nat Mode
           pytest -m "throughput_vs_pkt and Nat and wpa2_personal and twog and pkt60"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
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
                                       instance_name="TIP_PERF_DPT_WPA2_2G_60",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2547", name="WIFI-2547")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.pkt142
    def test_client_wpa2_personal_nat_pkt_142_2g(self, lf_tools, lf_test, station_names_twog,
                                                   create_lanforge_chamberview_dut,
                                                   get_configuration):
        """Throughput Vs Pkt Sizes Nat Mode
           pytest -m "throughput_vs_pkt and Nat and wpa2_personal and twog and pkt142"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
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
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2547", name="WIFI-2547")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.pkt256
    def test_client_wpa2_personal_nat_pkt_256_2g(self, lf_tools, lf_test, station_names_twog,
                                                   create_lanforge_chamberview_dut,
                                                   get_configuration):
        """Throughput Vs Pkt Sizes Nat Mode
           pytest -m "throughput_vs_pkt and Nat and wpa2_personal and twog and pkt256"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
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
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2547", name="WIFI-2547")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.pkt512
    def test_client_wpa2_personal_nat_pkt_512_2g(self, lf_tools, lf_test, station_names_twog,
                                                   create_lanforge_chamberview_dut,
                                                   get_configuration):
        """Throughput Vs Pkt Sizes Nat Mode
           pytest -m "throughput_vs_pkt and Nat and wpa2_personal and twog and pkt512"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
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
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2547", name="WIFI-2547")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.pkt1024
    def test_client_wpa2_personal_nat_pkt_1024_2g(self, lf_tools, lf_test, station_names_twog,
                                                   create_lanforge_chamberview_dut,
                                                   get_configuration):
        """Throughput Vs Pkt Sizes Nat Mode
           pytest -m "throughput_vs_pkt and Nat and wpa2_personal and twog and pkt1024"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
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
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2547", name="WIFI-2547")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.pktMTU
    def test_client_wpa2_personal_nat_pkt_MTU_2g(self, lf_tools, lf_test, station_names_twog,
                                                   create_lanforge_chamberview_dut,
                                                   get_configuration):
        """Throughput Vs Pkt Sizes Nat Mode
           pytest -m "throughput_vs_pkt and Nat and wpa2_personal and twog and pktMTU"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
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
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
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
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_5g],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestThroughputVsPktWpa2Nat5G(object):
    """Throughput vs Various Pkt Size Test nat mode
           pytest -m "throughput_vs_pkt and nat"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2547", name="WIFI-2547")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.pkt60
    def test_client_wpa2_personal_nat_pkt_60_5g(self, lf_tools, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                   get_configuration):
        """Throughput Vs Pkt Sizes nat Mode
           pytest -m "throughput_vs_pkt and nat and wpa2 and fiveg and pkt60"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
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
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2547", name="WIFI-2547")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.pkt142
    def test_client_wpa2_personal_nat_pkt_142_5g(self, lf_tools, lf_test, station_names_fiveg,
                                                create_lanforge_chamberview_dut,
                                                get_configuration):
        """Throughput Vs Pkt Sizes nat Mode
           pytest -m "throughput_vs_pkt and nat and wpa2 and fiveg and pkt142"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
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
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2547", name="WIFI-2547")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.pkt256
    def test_client_wpa2_personal_nat_pkt_256_5g(self, lf_tools, lf_test, station_names_fiveg,
                                                create_lanforge_chamberview_dut,
                                                get_configuration):
        """Throughput Vs Pkt Sizes nat Mode
           pytest -m "throughput_vs_pkt and nat and wpa2 and fiveg and pkt256"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
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
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2547", name="WIFI-2547")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.pkt512
    def test_client_wpa2_personal_nat_pkt_512_5g(self, lf_tools, lf_test, station_names_fiveg,
                                                create_lanforge_chamberview_dut,
                                                get_configuration):
        """Throughput Vs Pkt Sizes nat Mode
           pytest -m "throughput_vs_pkt and nat and wpa2 and fiveg and pkt512"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
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
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2547", name="WIFI-2547")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.pkt1024
    def test_client_wpa2_personal_nat_pkt_1024_5g(self, lf_tools, lf_test, station_names_fiveg,
                                                create_lanforge_chamberview_dut,
                                                get_configuration):
        """Throughput Vs Pkt Sizes nat Mode
           pytest -m "throughput_vs_pkt and nat and wpa2 and fiveg and pkt1024"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
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
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2547", name="WIFI-2547")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.pktMTU
    def test_client_wpa2_personal_nat_pkt_MTU_5g(self, lf_tools, lf_test, station_names_fiveg,
                                                create_lanforge_chamberview_dut,
                                                get_configuration):
        """Throughput Vs Pkt Sizes nat Mode
           pytest -m "throughput_vs_pkt and nat and wpa2 and fiveg and pktMTU"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
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
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
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