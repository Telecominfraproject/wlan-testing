"""

    Multi Station throughput vs Packet Size test: Bridge Mode
    pytest -m "multi_sta_thpt and wpa2_personal and bridge and fiveg"

"""

import os
import allure
import pytest

pytestmark = [pytest.mark.performance, pytest.mark.multi_sta_thpt, pytest.mark.wpa2_personal, pytest.mark.bridge,
              pytest.mark.fiveg]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.suite("performance")
@allure.feature("BRIDGE MODE WPA2 PERSONAL Multi_Station_Throughput")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMultiStaThptbridge(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_udp_dl_5g_1",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3632")
    def test_mstathpt_wpa2p_bridge_udp_dl_5g_1(self, get_vif_state, lf_tools,
                                               create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:200,512,1024,MTU'], ['capacities:1,2,5'], ['tput_multi_tcp:0'], ['tput_multi_dl:1'],
                     ['tput_multi_udp:1'], ['tput_multi_ul:0']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_1", raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_tcp_dl_5g_2",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3634")
    def test_mstathpt_wpa2p_bridge_tcp_dl_5g_2(self, get_vif_state, lf_tools,
                                               create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal  and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'],
                     ['pkt_loss_thresh:500000'],
                     ['frame_sizes:200,512,1024,MTU'], ['capacities:1,2,5'], ['tput_multi_tcp:1'], ['tput_multi_dl:1'],
                     ['tput_multi_udp:0'], ['tput_multi_ul:0']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_2",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name,
                                      pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_udp_ul_5g_3",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3636")
    def test_mstathpt_wpa2p_bridge_udp_ul_5g_3(self, get_vif_state, lf_tools,
                                               create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:200,512,1024,MTU'], ['capacities:1,2,5'], ['tput_multi_tcp:0'], ['tput_multi_dl:0'],
                     ['tput_multi_udp:1'], ['tput_multi_ul:1']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_3", raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_tcp_ul_5g_4",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3638")
    def test_mstathpt_wpa2p_bridge_tcp_ul_5g_4(self, get_vif_state, lf_tools,
                                               create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:200,512,1024,MTU'], ['capacities:1,2,5'], ['tput_multi_tcp:1'], ['tput_multi_dl:0'],
                     ['tput_multi_udp:0'], ['tput_multi_ul:1']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_4", raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.multi_sta_perf_throughput
    @pytest.mark.tcp_udp_ul_dl
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_udp_dl_5g_5",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3640")
    def test_mstathpt_wpa2p_bridge_udp_dl_5g_5(self, get_vif_state, lf_tools,
                                               create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:200,512,1024,MTU'], ['capacities:MAX'], ['tput_multi_tcp:0'], ['tput_multi_dl:1'],
                     ['tput_multi_udp:1'], ['tput_multi_ul:1']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_5", raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.multi_sta_perf_throughput
    @pytest.mark.tcp_udp_ul_dl
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_tcp_dl_5g_6",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3642")
    def test_mstathpt_wpa2p_bridge_tcp_dl_5g_6(self, get_vif_state, lf_tools,
                                               create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:200,512,1024,MTU'], ['capacities:MAX'], ['tput_multi_tcp:1'], ['tput_multi_dl:1'],
                     ['tput_multi_udp:0'], ['tput_multi_ul:0']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_6", raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.multi_sta_perf_throughput
    @pytest.mark.tcp_udp_ul_dl
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_udp_ul_5g_7",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3644")
    def test_mstathpt_wpa2p_bridge_udp_ul_5g_7(self, get_vif_state, lf_tools,
                                               create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:200,512,1024,MTU'], ['capacities:MAX'], ['tput_multi_tcp:0'], ['tput_multi_dl:0'],
                     ['tput_multi_udp:1'], ['tput_multi_ul:1']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_7", raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.multi_sta_perf_throughput
    @pytest.mark.tcp_udp_ul_dl
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_tcp_ul_5g_8",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3646")
    def test_mstathpt_wpa2p_bridge_tcp_ul_5g_8(self, get_vif_state, lf_tools,
                                               create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:200,512,1024,MTU'], ['capacities:MAX'], ['tput_multi_tcp:1'], ['tput_multi_dl:0'],
                     ['tput_multi_udp:0'], ['tput_multi_ul:1']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_8", raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_udp_dl_5g_9",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3782")
    def test_mstathpt_wpa2p_bridge_udp_dl_5g_9(self, get_vif_state, lf_tools,
                                               create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:200,512'], ['capacities:1,2,5'], ['tput_multi_tcp:0'], ['tput_multi_dl:1'],
                     ['tput_multi_udp:1'], ['tput_multi_ul:0']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_9", raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_tcp_dl_5g_10",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3784")
    def test_mstathpt_wpa2p_bridge_tcp_dl_5g_10(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:200'], ['capacities:1,2,5'], ['tput_multi_tcp:1'], ['tput_multi_dl:1'],
                     ['tput_multi_udp:0'], ['tput_multi_ul:0']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_10",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_udp_ul_5g_11",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3787")
    def test_mstathpt_wpa2p_bridge_udp_ul_5g_11(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:200'], ['capacities:1,2,5'], ['tput_multi_tcp:0'], ['tput_multi_dl:0'],
                     ['tput_multi_udp:1'], ['tput_multi_ul:1']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_11",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_udp_ul_5g_12",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3789")
    def test_mstathpt_wpa2p_bridge_tcp_ul_5g_12(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:200'], ['capacities:1,2,5'], ['tput_multi_tcp:1'], ['tput_multi_dl:0'],
                     ['tput_multi_udp:0'], ['tput_multi_ul:1']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_12",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_udp_dl_5g_13",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3792")
    def test_mstathpt_wpa2p_bridge_udp_dl_5g_13(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:512'], ['capacities:1,2,5'], ['tput_multi_tcp:0'], ['tput_multi_dl:1'],
                     ['tput_multi_udp:1'], ['tput_multi_ul:0']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_13",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_tcp_dl_5g_14",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3794")
    def test_mstathpt_wpa2p_bridge_tcp_dl_5g_14(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:512'], ['capacities:1,2,5'], ['tput_multi_tcp:1'], ['tput_multi_dl:1'],
                     ['tput_multi_udp:0'], ['tput_multi_ul:0']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_14",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_udp_ul_5g_15",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3799")
    def test_mstathpt_wpa2p_bridge_udp_ul_5g_15(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:512'], ['capacities:1,2,5'], ['tput_multi_tcp:0'], ['tput_multi_dl:0'],
                     ['tput_multi_udp:1'], ['tput_multi_ul:1']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_15",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_tcp_ul_5g_16",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3801")
    def test_mstathpt_wpa2p_bridge_tcp_ul_5g_16(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:512'], ['capacities:1,2,5'], ['tput_multi_tcp:1'], ['tput_multi_dl:0'],
                     ['tput_multi_udp:0'], ['tput_multi_ul:1']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_16",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_udp_dl_5g_17",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3803")
    def test_mstathpt_wpa2p_bridge_udp_ul_5g_17(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:1024'], ['capacities:1,2,5'], ['tput_multi_tcp:0'], ['tput_multi_dl:1'],
                     ['tput_multi_udp:1'], ['tput_multi_ul:0']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_17",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_tcp_dl_5g_18",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3805")
    def test_mstathpt_wpa2p_bridge_tcp_dl_5g_18(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:1024'], ['capacities:1,2,5'], ['tput_multi_tcp:1'], ['tput_multi_dl:1'],
                     ['tput_multi_udp:0'], ['tput_multi_ul:0']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_18",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_udp_ul_5g_19",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3807")
    def test_mstathpt_wpa2p_bridge_udp_ul_5g_19(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:1024'], ['capacities:1,2,5'], ['tput_multi_tcp:0'], ['tput_multi_dl:0'],
                     ['tput_multi_udp:1'], ['tput_multi_ul:1']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_19",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_tcp_ul_5g_20",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3811")
    def test_mstathpt_wpa2p_bridge_tcp_ul_5g_20(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:1024'], ['capacities:1,2,5'], ['tput_multi_tcp:1'], ['tput_multi_dl:0'],
                     ['tput_multi_udp:0'], ['tput_multi_ul:1']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_20",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_udp_dl_5g_21",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3813")
    def test_mstathpt_wpa2p_bridge_udp_dl_5g_21(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:MTU'], ['capacities:1,2,5'], ['tput_multi_tcp:0'], ['tput_multi_dl:1'],
                     ['tput_multi_udp:1'], ['tput_multi_ul:0']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_21",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_tcp_dl_5g_22",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3816")
    def test_mstathpt_wpa2p_bridge_tcp_dl_5g_22(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:MTU'], ['capacities:1,2,5'], ['tput_multi_tcp:1'], ['tput_multi_dl:1'],
                     ['tput_multi_udp:0'], ['tput_multi_ul:0']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_22",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_udp_ul_5g_23",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3818")
    def test_mstathpt_wpa2p_bridge_udp_ul_5g_23(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:MTU'], ['capacities:1,2,5'], ['tput_multi_tcp:0'], ['tput_multi_dl:0'],
                     ['tput_multi_udp:1'], ['tput_multi_ul:1']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_23",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(name="test_mstathpt_wpa2p_bridge_tcp_ul_5g_24",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3820")
    def test_mstathpt_wpa2p_bridge_tcp_ul_5g_24(self, get_vif_state, lf_tools,
                                                create_lanforge_chamberview_dut, lf_test, get_configuration):
        """
        pytest -m "multi_sta_thpt and bridge and wpa2_personal and fiveg"

        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]

        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)

        if ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        raw_lines = [['skip_2:1'], ['skip_dual:1'], ['hunt_retries:1'], ['hunt_iter:20'], ['pkt_loss_thresh:500000'],
                     ['frame_sizes:MTU'], ['capacities:1,2,5'], ['tput_multi_tcp:1'], ['tput_multi_dl:0'],
                     ['tput_multi_udp:0'], ['tput_multi_ul:1']]

        msthpt_obj = lf_test.multi_sta_thpt(mode=mode, ssid_2G="", ssid_5G=ssid_5G,
                                            instance_name="multistathpt_instance_wpa2p_5g_bridge_24",
                                            raw_line=raw_lines,
                                            vlan_id=vlan, dut_5g=dut_5g, dut_2g="")

        report_name = msthpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Multi Station Throughput vs Packet Size Test")
        assert True
