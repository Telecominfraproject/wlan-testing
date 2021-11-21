"""

    Performance Test: Receiver Sensitivity Test: bridge Mode
    pytest -m "rxsensitivity and bridge"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.advance, pytest.mark.rxsensitivity, pytest.mark.bridge]

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

@allure.feature("BRIDGE MODE RECEIVER SENSITIVITY TEST")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestRxSensitivityBridge(object):


    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2445", name="WIFI-2445")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.all_mcs
    def test_client_wpa2_personal_bridge_all_mcs_5g(self, lf_test,  lf_tools, station_names_fiveg, create_lanforge_chamberview_dut,
                                                    get_configuration):
        """
            Receiver Sensitivity Bridge Mode
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        ser_no = lf_test.attenuator_serial()
        print(ser_no)
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 0 CCK, OFDM, HT, VHT;1 CCK, OFDM, HT, VHT;2 CCK, OFDM, HT, VHT;3 CCK, OFDM, HT, VHT;'
                      '4 OFDM, HT, VHT;5 OFDM, HT, VHT;6 OFDM, HT, VHT;7 OFDM, HT, VHT;8 VHT;9 VHT'],
                     ['spatial_streams: 2'], ['bandw_options: 80'], ['txo_sgi: OFF'],
                     ['txo_retries: No Retry'], ['attenuator: ' + str(ser_no[0])], ['attenuator2: ' + str(ser_no[1])],
                     ['attenuations: 0..+50..800'], ['attenuations2: 0..+50..800'],
                     ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            obj = lf_test.rx_sensitivity(station_name=station_names_fiveg, mode=mode,
                                            instance_name="RECEIVER_SENSITIVITY_BRIDGE_5G",
                                            vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Receiver sensitivity test")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2445", name="WIFI-2445")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.all_mcs
    def test_client_wpa2_personal_bridge_all_mcs_2g(self, lf_test, lf_tools, station_names_twog,
                                                    create_lanforge_chamberview_dut,
                                                    get_configuration):
        """
            Receiver Sensitivity Bridge Mode
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        ser_no = lf_test.attenuator_serial()
        print(ser_no)
        raw_lines = [['txo_preamble: VHT'],
                     ['txo_mcs: 0 CCK, OFDM, HT, VHT;1 CCK, OFDM, HT, VHT;2 CCK, OFDM, HT, VHT;3 CCK, OFDM, HT, VHT;'
                      '4 OFDM, HT, VHT;5 OFDM, HT, VHT;6 OFDM, HT, VHT;7 OFDM, HT, VHT;8 VHT;9 VHT'],
                     ['spatial_streams: 2'], ['bandw_options: 80'], ['txo_sgi: OFF'],
                     ['txo_retries: No Retry'], ['attenuator: ' + str(ser_no[0])], ['attenuator2: ' + str(ser_no[1])],
                     ['attenuations: 0..+50..800'], ['attenuations2: 0..+50..800'],
                     ["show_3s: 1"], ['txo_txpower: 17'],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            obj = lf_test.rx_sensitivity(station_name=station_names_twog, mode=mode,
                                         instance_name="RECEIVER_SENSITIVITY_BRIDGE_2G",
                                         vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Receiver sensitivity test")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False
