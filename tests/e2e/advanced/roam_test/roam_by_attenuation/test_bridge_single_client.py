import time

import pytest
import allure
# from configuration import CONFIGURATION

pytestmark = [pytest.mark.roam_test, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "roam": False,
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["6G"], "security_key": "something"}
        ]},
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

class TestBasicRoam(object):


    @pytest.mark.roam_2g
    @pytest.mark.wpa2_personal
    def test_basic_roam_2g(self, get_configuration, lf_test, station_names_twog, lf_tools, run_lf, add_env_properties,
                           instantiate_profile, get_controller_logs, get_ap_config_slots, get_lf_logs):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1

        # calling basic roam from lf_test
        roam =lf_test.basic_roam(run_lf=run_lf, get_configuration=get_configuration, lf_tools=lf_tools, instantiate_profile=instantiate_profile,
                                 ssid_name=ssid_name, security=security, security_key=security_key,
                                 mode=mode, band=band, station_name=station_names_twog, vlan=vlan, test="2g")
        if roam:
            assert True
        else:
            assert False


    @pytest.mark.roam_5g
    @pytest.mark.wpa2_personal
    def test_basic_roam_5g(self, get_configuration, lf_test, station_names_fiveg, lf_tools, run_lf, add_env_properties,
                           instantiate_profile, get_controller_logs, get_ap_config_slots, get_lf_logs):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        roam = lf_test.basic_roam(run_lf=run_lf, get_configuration=get_configuration, lf_tools=lf_tools,
                                  instantiate_profile=instantiate_profile,
                                  ssid_name=ssid_name, security=security, security_key=security_key,
                                  mode=mode, band=band, station_name=station_names_fiveg, vlan=vlan, test="5g")
        if roam:
            assert True
        else:
            assert False

    @pytest.mark.sixg
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    def test_basic_roam_6g(self):
        pass




























    # @pytest.mark.multi_roam_2g
    # @pytest.mark.wpa2_personl
    # def test_multiple_roam_2g(self, get_configuration, lf_test, station_names_twog, lf_tools, run_lf, add_env_properties,
    #                           instantiate_profile, get_controller_logs, get_ap_config_slots, get_lf_logs):
    #     profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "wpa2"
    #     mode = "BRIDGE"
    #     band = "twog"
    #     vlan = 1
    #     c1_2g_bssid = ""
    #     c2_2g_bssid = ""
    #     if run_lf:
    #         c1_2g_bssid = get_configuration["access_point"][0]["ssid"]["2g-bssid"]
    #         allure.attach(name="bssid of ap1", body=c1_2g_bssid)
    #         c2_2g_bssid = get_configuration["access_point"][1]["ssid"]["2g-bssid"]
    #         allure.attach(name="bssid of ap2", body=c2_2g_bssid)
    #         ssid_name = get_configuration["access_point"][0]["ssid"]["2g-ssid"]
    #     else:
    #         for ap_name in range(len(get_configuration['access_point'])):
    #             instantiate_profile_obj = instantiate_profile(controller_data=get_configuration['controller'],
    #                                                           timeout="10", ap_data=get_configuration['access_point'], type=ap_name)
    #             bssid_2g = instantiate_profile_obj.cal_bssid_2g()
    #             if ap_name == 0 :
    #                 c1_2g_bssid = bssid_2g
    #             if ap_name == 1:
    #                 c2_2g_bssid = bssid_2g
    #     print("bssid of c1 ", c1_2g_bssid)
    #     allure.attach(name="bssid of ap1", body=c1_2g_bssid)
    #     print("bssid of c2",  c2_2g_bssid)
    #     allure.attach(name="bssid of ap2", body=c2_2g_bssid)
    #
    #
    #     ser_no = lf_test.attenuator_serial()
    #     print(ser_no[0])
    #     ser_1 = ser_no[0].split(".")[2]
    #     ser_2 = ser_no[1].split(".")[2]
    #     lf_tools.add_stations(band="2G", num_stations=3, dut=lf_tools.dut_name, ssid_name=ssid_name)
    #     lf_tools.Chamber_View()
    #     sta_list = lf_tools.get_station_list()
    #     print("sta_list", sta_list)
    #     lf_tools.admin_up_down(sta_list=sta_list, option="up")
    #     station = lf_test.wait_for_ip(station=sta_list)
    #     station_before = ""
    #     station_list = []
    #     for i in range(len(sta_list)):
    #         station_list.append(sta_list[i].split(".")[2])
    #         print(station_list)
    #     if station:
    #         lf_test.attach_stationdata_to_allure(name="staion info before roam", station_name=sta_list)
    #         for i in station_list:
    #             bssid = lf_tools.station_data_query(station_name=str(i), query="ap")
    #             formated_bssid = bssid.lower()
    #             if formated_bssid == c1_2g_bssid:
    #                 print("station connected to chamber1 ap")
    #                 station_before = formated_bssid
    #             elif formated_bssid == c2_2g_bssid:
    #                 print("station connected to chamber 2 ap")
    #                 station_before = formated_bssid
    #             # logic to decrease c1 attenuation and increase c2 attenuation
    #         for atten_val1, atten_val2 in zip([0, 100, 300, 500, 750, 950], [950, 750, 500, 300, 100, 0]):
    #             print(atten_val1)
    #             print(atten_val2)
    #             for i in range(4):
    #                 lf_test.attenuator_modify(int(ser_1), i, atten_val1)
    #                 lf_test.attenuator_modify(int(ser_2), i, atten_val2)
    #             time.sleep(10)
    #             lf_tools.admin_up_down(sta_list=station_list, option="down")
    #             time.sleep(15)
    #             lf_tools.admin_up_down(sta_list=station_list, option="up")
    #             time.sleep(15)
    #             for i in station_list:
    #                 bssid = lf_tools.station_data_query(station_name=str(i), query="ap")
    #                 station_after = bssid.lower()
    #                 if station_after == station_before:
    #                     continue
    #                 elif station_after != station_before:
    #                     print("client performed roam")
    #                     lf_test.attach_stationdata_to_allure(name="staion info after roam", station_name=i)
    #                     allure.attach(name="attenuation_data", body="ap1 was at attenuation value " + str(atten_val2) + "ddbm and ap2 was at attenuation value " + str(atten_val1) + "ddbm")
    #                     break
    #
    #     else:
    #         allure.attach(name="FAIL", body="stations failed to get ip")
    #         assert False
    #











