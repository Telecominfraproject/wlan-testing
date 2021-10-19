"""

    Performance Test: Receiver Sensitivity Test: NAT Mode
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
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
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
class TestRxSensitivityNATAllMcs5G(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2445", name="WIFI-2445")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.all_mcs
    def test_client_wpa2_personal_nat_all_mcs_5g(self, get_vif_state,
                                                    lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                                    get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        attenuator = setup_params_general["attenuator"]["attenuator"]
        attenuator2 = setup_params_general["attenuator"]["attenuator2"]
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 0 CCK, OFDM, HT, VHT;1 CCK, OFDM, HT, VHT;2 CCK, OFDM, HT, VHT;3 CCK, OFDM, HT, VHT'
                      '4 OFDM, HT, VHT;5 OFDM, HT, VHT;6 OFDM, HT, VHT;7 OFDM, HT, VHT;8 VHT;9 VHT'],
                     ['spatial_streams: 1'], ['bandw_options: 20'], ['txo_sgi: OFF'],
                     ['txo_retries: No Retry'], ['attenuator: %s' % attenuator], ['attenuator2: %s' % attenuator2],
                     ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_fiveg, mode=mode,
                                            instance_name="TIP_PERF_RX_SEN_WPA2_NAT_5G_ALL_MCS",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
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

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2445", name="WIFI-2445")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.all_mcs
    def test_client_wpa2_personal_nat_all_mcs_2g(self, get_vif_state,
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
                     ['txo_mcs: 0 CCK, OFDM, HT, VHT;1 CCK, OFDM, HT, VHT;2 CCK, OFDM, HT, VHT;3 CCK, OFDM, HT, VHT'
                      '4 OFDM, HT, VHT;5 OFDM, HT, VHT;6 OFDM, HT, VHT;7 OFDM, HT, VHT;8 VHT;9 VHT'],
                     ['spatial_streams: 1'], ['bandw_options: 20'], ['txo_sgi: OFF'],
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
                                            instance_name="TIP_PERF_RX_SEN_WPA2_NAT_2G_ALL_MCS",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
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
