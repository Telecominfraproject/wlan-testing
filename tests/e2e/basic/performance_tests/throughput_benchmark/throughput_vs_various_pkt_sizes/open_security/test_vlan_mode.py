"""

    Performance Test: Throughput vs Various Pkt Size Test: VLAN Mode
    pytest -m "throughput_vs_pkt and VLAN"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.throughput_vs_pkt, pytest.mark.vlan, pytest.mark.open,]
              # pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"], "vlan": 100},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"], "vlan": 100}]},
    "rf": {},
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
class TestThroughputVsPktVLAN2G(object):
    """Throughput vs Various Pkt Size Test VLAN mode
       pytest -m "throughput_vs_pkt and VLAN"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-2546")
    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.pkt60
    def test_client_open_pkt_60_2g(self, lf_tools, lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                   get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and open and twog and pkt60"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = 100
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 60'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_2G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-2546")
    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.pkt142
    def test_client_open_pkt_142_2g(self, lf_tools, lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                    get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and open and twog and pkt142"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]

        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = 100
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 142'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_2G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-2546")
    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.pkt256
    def test_client_open_pkt_256_2g(self, lf_tools, lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                    get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and open and twog and pkt256"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]

        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = 100
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 256'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_2G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-2546")
    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.pkt512
    def test_client_open_pkt_512_2g(self, lf_tools, lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                    get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and open and twog and pkt512"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]

        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = 100
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 512'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_2G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-2546")
    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.pkt1024
    def test_client_open_pkt_1024_2g(self, lf_tools, lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                     get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and open and twog and pkt1024"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]

        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = 100
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 1024'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_2G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-2546")
    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.pktMTU
    def test_client_open_pkt_MTU_2g(self, lf_tools, lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                    get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and open and twog and pktMTU"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]

        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = 100
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: MTU'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_2G",
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
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"], "vlan": 100},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"], "vlan": 100}]},
    "rf": {},
    "radius": False
}


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_5g],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestThroughputVsPktVLAN5G(object):
    """Throughput vs Various Pkt Size Test VLAN mode
       pytest -m "throughput_vs_pkt and VLAN"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-2546")
    @pytest.mark.open
    @pytest.mark.fiveg
    @pytest.mark.pkt60
    def test_client_open_pkt_60_5g(self, lf_tools, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                   get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and open and fiveg and pkt60"
        """
        profile_data = setup_params_5g["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]

        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 60'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_PKT_60_OPEN_5G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-2546")
    @pytest.mark.open
    @pytest.mark.fiveg
    @pytest.mark.pkt142
    def test_client_open_pkt_142_5g(self, lf_tools, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                    get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and open and fiveg and pkt142"
        """
        profile_data = setup_params_5g["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]

        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 142'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_PKT_142_OPEN_5G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-2546")
    @pytest.mark.open
    @pytest.mark.fiveg
    @pytest.mark.pkt256
    def test_client_open_pkt_256_5g(self, lf_tools, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                    get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and open and fiveg and pkt256"
        """
        profile_data = setup_params_5g["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]

        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 256'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_PKT_256_OPEN_5G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-2546")
    @pytest.mark.open
    @pytest.mark.fiveg
    @pytest.mark.pkt512
    def test_client_open_pkt_512_5g(self, lf_tools, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                    get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and open and fiveg and pkt512"
        """
        profile_data = setup_params_5g["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]

        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 512'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_PKT_512_OPEN_5G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-2546")
    @pytest.mark.open
    @pytest.mark.fiveg
    @pytest.mark.pkt1024
    def test_client_open_pkt_1024_5g(self, lf_tools, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                     get_configuration):
        """Throughput Vs Pkt Sizes VLAN Mode
           pytest -m "throughput_vs_pkt and VLAN and open and fiveg"
        """
        profile_data = setup_params_5g["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]

        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 1024'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_PKT_1024_OPEN_5G",
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-2546")
    @pytest.mark.open
    @pytest.mark.fiveg
    @pytest.mark.pktMTU
    def test_client_open_pkt_MTU_5g(self, lf_tools, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                    get_configuration):
        """Throughput Vs Pkt Sizes VLAN Mode
           pytest -m "throughput_vs_pkt and VLAN and open and fiveg"
        """
        profile_data = setup_params_5g["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]

        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: MTU'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_PKT_MTU_OPEN_5G",
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
