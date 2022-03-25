import time

import pytest
import allure
# from configuration import CONFIGURATION

pytestmark = [pytest.mark.roam_test, pytest.mark.bridge]

# setup_params_general = {
#     "mode": "BRIDGE",
#     "roam": False,
#     "ssid_modes": {
#         "wpa2_personal": [
#             {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
#             {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}]},
#     "rf": {},
#     "radius": False
# }
setup_params_general = {
    "mode": "BRIDGE",
    "roam": True,
    "ft+psk": True,
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "RoamAP2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "RoamAP5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [{"ssid_name": "RoamAP6g", "appliedRadios": ["6G"], "security_key": "something"}]
    },
    # "roam_type": "fiveg_to_fiveg",
    "rf": {},
    "radius": False
}
@allure.suite("Roam Test with attenuator")
@allure.feature("Roam Test")
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")
# @allure.step
# def nested_step_allure(bssid, rssi):
#     pass

class TestBasicRoam(object):

    @pytest.mark.roam_5g
    @pytest.mark.bob
    @pytest.mark.wpa2_personal
    def test_basic_roam_5g_to_5g(self, get_configuration, lf_test, lf_reports,  station_names_fiveg, lf_tools, run_lf, add_env_properties,
                           instantiate_profile, get_controller_logs, get_ap_config_slots, get_lf_logs):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        lf_test.basic_roam(run_lf=run_lf, get_configuration=get_configuration, lf_tools=lf_tools,
                           lf_reports=lf_reports,
                           instantiate_profile=instantiate_profile,
                           ssid_name=ssid_name, security=security, security_key=security_key,
                           mode=mode, band=band, station_name=station_names_fiveg, vlan=vlan, test="5g")


    @pytest.mark.multi_roam
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    def test_multi_roam_5g_to_5g_soft_roam_11r(self,  get_configuration, lf_test, lf_reports,  station_names_fiveg, lf_tools, run_lf, add_env_properties,
                           instantiate_profile, get_controller_logs, get_ap_config_slots, get_lf_logs):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        print("starting snifer")
        # lf_test.start_sniffer(radio_channel=36, radio="wiphy2", test_name="roam_11r", duration=3600)
        lf_test.create_n_clients(sta_prefix="wlan", num_sta=2, dut_ssid=ssid_name,
                         dut_security=security, dut_passwd=security_key, radio="wiphy1", lf_tools=lf_tools,
                                  type="11r")

        # lf_test.multi_roam(run_lf=run_lf, get_configuration=get_configuration, lf_tools=lf_tools,
        #                    lf_reports=lf_reports,
        #                    instantiate_profile=instantiate_profile,
        #                    ssid_name=ssid_name, security=security, security_key=security_key,
        #                    mode=mode, band=band, station_name=station_names_fiveg, vlan=vlan, test="5g")
        #
        # print("stop sniff")
        # file_name = lf_test.stop_sniffer()
        # print(file_name)
        # print("wait for logs to be attached")
        # file_name = "roam_11r2022-03-23-00-02.pcap"
        # time.sleep(10)
        # query_auth  = lf_test. query_sniff_data(pcap_file=str(file_name), filter="wlan.fc.type_subtype==0x000b")
        # print("query", query_auth)
        # allure.attach(name="authentication", body=str(query_auth))
        # query_asso = lf_test.query_sniff_data(pcap_file=str(file_name), filter="wlan.fc.type_subtype==0x0000")
        # print("query", query_asso)
        # allure.attach(name="authentication", body=str(query_asso))
        # query_reasso_response = lf_test.query_sniff_data(pcap_file=str(file_name), filter="(wlan.fc.type_subtype==3) && (wlan.tag.number==55)")
        # print("query", query_reasso_response)
        # allure.attach(name="authentication", body=str(query_reasso_response))
        # query_4way  = lf_test.query_sniff_data(pcap_file=str(file_name), filter="eapol")
        # print("query", query_4way)
        # allure.attach(name="authentication", body=str(query_4way))
        #

    @pytest.mark.hard
    @pytest.mark.wpa2_personal
    def test_multi_hard_roam_5g_to_5g(self,  get_configuration, lf_test, lf_reports,  station_names_fiveg, lf_tools, run_lf, add_env_properties,
                           instantiate_profile, get_controller_logs, get_ap_config_slots, get_lf_logs):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        lf_test.multi_hard_roam(run_lf=run_lf, get_configuration=get_configuration, lf_tools=lf_tools,
                           lf_reports=lf_reports,
                           instantiate_profile=instantiate_profile,
                           ssid_name=ssid_name, security=security, security_key=security_key,
                           mode=mode, band=band, station_name=station_names_fiveg, vlan=vlan, test="5g", iteration=2, num_sta=1)

    @pytest.mark.testing
    def test_testing(self, lf_test):
        ret = lf_test.sniff_full_data(pcap_file="roam_11r2022-03-25-13-27.pcap")
        print(ret)







































