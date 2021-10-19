"""

    Performance Test: Receiver Sensitivity Test: nat Mode
    pytest -m "rx_sensitivity_test and nat"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.rx_sensitivity_test, pytest.mark.nat,
              pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_WPA2_2G", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_WPA2_2G", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}]},
    "rf": {
        "is5GHz": {"channelBandwidth": "is20MHz"},
        "is5GHzL": {"channelBandwidth": "is20MHz"},
        "is5GHzU": {"channelBandwidth": "is20MHz"}},
    "radius": False,

    "attenuator": {
        "attenuator": "1.1.3059",
        "attenuator2": "1.1.3034"}

}


@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestRxSensitivityNAT2G(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2446", name="WIFI-2446")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs0
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs0_nss1_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 0 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 1'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2],
                     ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS0_NSS0",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2447", name="WIFI-2447")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs1
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs1_nss1_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 1 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 1'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS1_NSS1",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2448", name="WIFI-2448")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs2
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs2_nss1_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 2 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 1'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS2_NSS1",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2449", name="WIFI-2449")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs3
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs3_nss1_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 3 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 1'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS3_NSS1",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2450", name="WIFI-2450")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs4
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs4_nss1_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 4 OFDM, HT, VHT'],
                     ['spatial_streams: 1'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS4_NSS1",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2451", name="WIFI-2451")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs5
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs5_nss1_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 5 OFDM, HT, VHT'],
                     ['spatial_streams: 1'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS5_NSS1",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2452", name="WIFI-2452")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs6
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs6_nss1_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 6 OFDM, HT, VHT'],
                     ['spatial_streams: 1'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS6_NSS1",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2453", name="WIFI-2453")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs7
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs7_nss1_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 7 OFDM, HT, VHT'],
                     ['spatial_streams: 1'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS7_NSS1",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2454", name="WIFI-2454")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs8
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs8_nss1_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 8 VHT'],
                     ['spatial_streams: 1'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS8_NSS1",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2455", name="WIFI-2455")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs9
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs9_nss1_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 9 VHT'],
                     ['spatial_streams: 1'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS9_NSS1",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    # Test case for mcs0-9,Nss 2, bw 20MHz
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2458", name="WIFI-2458")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs0
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs0_nss2_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 0 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 2'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS0_NSS2",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2459", name="WIFI-2459")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs1
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs1_nss2_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 1 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 2'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS1_NSS2",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2460", name="WIFI-2460")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs2
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs2_nss2_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 2 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 2'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS2_NSS2",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2461", name="WIFI-2461")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs3
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs3_nss2_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 3 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 2'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS3_NSS2",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2462", name="WIFI-2462")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs4
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs4_nss2_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 4 OFDM, HT, VHT'],
                     ['spatial_streams: 1'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS4_NSS2",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2463", name="WIFI-2463")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs5
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs5_nss2_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 5 OFDM, HT, VHT'],
                     ['spatial_streams: 2'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS5_NSS2",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2464", name="WIFI-2464")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs6
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs6_nss2_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 6 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 2'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS6_NSS2",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2465", name="WIFI-2465")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs7
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs7_nss2_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 7 OFDM, HT, VHT'],
                     ['spatial_streams: 2'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS7_NSS2",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2466", name="WIFI-2466")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs8
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs8_nss2_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 8 VHT'],
                     ['spatial_streams: 2'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS8_NSS2",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2467", name="WIFI-2467")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs9
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs9_nss2_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 9 VHT'],
                     ['spatial_streams: 2'], ['bandw_options: 20'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS9_NSS2",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    # Test case for mcs0-9,Nss 3, bw 20MHz
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2470", name="WIFI-2470")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs0
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs0_nss3_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 0 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 3'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS0_NSS3",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2471", name="WIFI-2471")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs1
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs1_nss3_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 1 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 3'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS1_NSS3",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2472", name="WIFI-2472")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs2
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs2_nss3_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 2 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 3'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS2_NSS3",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2473", name="WIFI-2473")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs3
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs3_nss3_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 3 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 3'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS3_NSS3",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2474", name="WIFI-2474")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs4
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs4_nss3_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 4 OFDM, HT, VHT'],
                     ['spatial_streams: 3'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS4_NSS3",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2475", name="WIFI-2475")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs5
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs5_nss3_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 5 OFDM, HT, VHT'],
                     ['spatial_streams: 3'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS5_NSS3",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2476", name="WIFI-2476")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs6
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs6_nss3_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 6 OFDM, HT, VHT'],
                     ['spatial_streams: 3'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS6_NSS3",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2477", name="WIFI-2477")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs7
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs7_nss3_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 7 OFDM, HT, VHT'],
                     ['spatial_streams: 3'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS7_NSS3",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2478", name="WIFI-2478")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs8
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs8_nss3_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 8 VHT'],
                     ['spatial_streams: 3'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS8_NSS3",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2479", name="WIFI-2479")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs9
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs9_nss3_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 9 VHT'],
                     ['spatial_streams: 3'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS9_NSS3",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    # Test case for mcs0-9,Nss 4, bw 20MHz
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2482", name="WIFI-2482")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs0
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs0_nss4_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 0 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 4'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS0_NSS4",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2483", name="WIFI-2483")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs1
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs1_nss4_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 1 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 4'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS1_NSS4",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2484", name="WIFI-2484")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs2
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs2_nss4_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 2 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 4'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS2_NSS4",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2485", name="WIFI-2485")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs3
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs3_nss4_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 3 CCK, OFDM, HT, VHT'],
                     ['spatial_streams: 4'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS3_NSS4",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2486", name="WIFI-2486")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs4
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs4_nss4_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 4 OFDM, HT, VHT'],
                     ['spatial_streams: 4'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS4_NSS4",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2487", name="WIFI-2487")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs5
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs5_nss4_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 5 OFDM, HT, VHT'],
                     ['spatial_streams: 4'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS5_NSS4",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2488", name="WIFI-2488")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs6
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs6_nss4_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 6 OFDM, HT, VHT'],
                     ['spatial_streams: 4'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS6_NSS4",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2489", name="WIFI-2489")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs7
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs7_nss4_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 7 OFDM, HT, VHT'],
                     ['spatial_streams: 4'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS7_NSS4",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2490", name="WIFI-2490")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs8
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs8_nss4_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 8 VHT'],
                     ['spatial_streams: 4'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS8_NSS4",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2491", name="WIFI-2491")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.mcs9
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs9_nss4_5g(self, get_vif_state,
                                               lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                               get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 9 VHT'],
                     ['spatial_streams: 4'], ['bandw_options: 80'], ['txo_sgi: ON'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2], ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_2G_MCS9_NSS4",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[0].split("/")[-1]
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
