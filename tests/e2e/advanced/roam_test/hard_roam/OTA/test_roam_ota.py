import pytest
import allure
import time

pytestmark = [pytest.mark.roam_test, pytest.mark.bridge, pytest.mark.roam_ota]

setup_params_general = {
    "mode": "BRIDGE",
    "roam": True,
    "ft+psk": True,
    "ft-otd": False,
    "ft-dot1x": False,
    "ft-dot1x_sha256": True,
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "RoamAP2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "RoamAP5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [{"ssid_name": "RoamAP6g", "appliedRadios": ["6G"], "security_key": "something"}]
    },
    "rf": {},
    "radius": False
}
@allure.suite("Hard Roam over the air")
@allure.feature("Roam Test")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")


class TestRoamOTA(object):

    @pytest.mark.hard_roam_5g_ota
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    def test_multi_hard_roam_5g_to_5g_ft_psk_wpa2(self, get_configuration, lf_test, lf_reports, lf_tools,
                                                  run_lf, add_env_properties,
                                                  instantiate_profile, get_controller_logs, get_ap_config_slots,
                                                  get_lf_logs,
                                                  roaming_delay, iteration, client, duration):

        instantiate_profile_obj = instantiate_profile(controller_data=get_configuration['controller'],
                                                      timeout="10",
                                                      ap_data=get_configuration['access_point'],
                                                      type=0)
        print("shut down 2g and 6g band")
        instantiate_profile_obj.ap_2ghz_shutdown()
        instantiate_profile_obj.ap_6ghz_shutdown()
        print("enable only 5g")
        instantiate_profile_obj.no_ap_5ghz_shutdown()


        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        print("disable wlan ")
        instantiate_profile_obj.disable_wlan(wlan=setup_params_general["ssid_modes"]["wpa2_personal"][0]["ssid_name"])
        instantiate_profile_obj.disable_wlan(wlan=setup_params_general["ssid_modes"]["wpa3_personal"][0]["ssid_name"])
        dut_name = []
        for i in range(len(get_configuration["access_point"])):
            dut_name.append(get_configuration["access_point"][i]["ap_name"])

        print("dut names", dut_name)
        # check channel

        lf_test.create_n_clients(sta_prefix="wlan1", num_sta=1, dut_ssid=ssid_name,
                                 dut_security=security, dut_passwd=security_key, band="fiveg",
                                 lf_tools=lf_tools, type="11r")
        sta_list = lf_tools.get_station_list()
        print(sta_list)
        val = lf_test.wait_for_ip(station=sta_list)
        ch = ""
        if val:
            for sta_name in sta_list:
                sta = sta_name.split(".")[2]
                time.sleep(5)
                ch = lf_tools.station_data_query(station_name=str(sta), query="channel")
            print(ch)
            lf_test.Client_disconnect(station_name=sta_list)

        else:
            pytest.exit("station failed to get ip")
            assert False

        lf_test.hard_roam(run_lf=run_lf, get_configuration=get_configuration, lf_tools=lf_tools,
                          instantiate_profile=instantiate_profile, lf_reports=lf_reports,
                          ssid_name=ssid_name, security=security, security_key=security_key,
                          band=band, test="5g",
                          iteration=int(iteration), num_sta=int(client), roaming_delay=roaming_delay,
                          option="ota", channel=ch, duration=duration, duration_based=False,
                          iteration_based=True, dut_name=dut_name)

    @pytest.mark.hard_roam_2g_ota
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    def test_multi_hard_roam_2g_to_2g_ft_psk_wpa2(self, get_configuration, lf_test, lf_reports, lf_tools,
                                                  run_lf, add_env_properties,
                                                  instantiate_profile, get_controller_logs, get_ap_config_slots,
                                                  get_lf_logs,
                                                  roaming_delay, iteration, client, duration):
        instantiate_profile_obj = instantiate_profile(controller_data=get_configuration['controller'],
                                                      timeout="10",
                                                      ap_data=get_configuration['access_point'],
                                                      type=0)
        print("shut down 5g and 6g band")
        instantiate_profile_obj.ap_5ghz_shutdown()
        instantiate_profile_obj.ap_6ghz_shutdown()
        print("enable only 2g")
        instantiate_profile_obj.no_ap_2ghz_shutdown()
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        print("disable wlan ")
        instantiate_profile_obj.disable_wlan(wlan=setup_params_general["ssid_modes"]["wpa2_personal"][1]["ssid_name"])
        instantiate_profile_obj.disable_wlan(wlan=setup_params_general["ssid_modes"]["wpa3_personal"][0]["ssid_name"])
        dut_name = []
        for i in range(len(get_configuration["access_point"])):
            dut_name.append(get_configuration["access_point"][i]["ap_name"])

        print("dut names", dut_name)
        # check channel

        lf_test.create_n_clients(sta_prefix="wlan", num_sta=1, dut_ssid=ssid_name,
                                 dut_security=security, dut_passwd=security_key, band="twog",
                                 lf_tools=lf_tools, type="11r")
        sta_list = lf_tools.get_station_list()
        print(sta_list)
        val = lf_test.wait_for_ip(station=sta_list)
        ch = ""
        if val:
            for sta_name in sta_list:
                sta = sta_name.split(".")[2]
                time.sleep(5)
                ch = lf_tools.station_data_query(station_name=str(sta), query="channel")
            print(ch)
            lf_test.Client_disconnect(station_name=sta_list)

        else:
            pytest.exit("station failed to get ip")
            assert False

        lf_test.hard_roam(run_lf=run_lf, get_configuration=get_configuration, lf_tools=lf_tools,
                          instantiate_profile=instantiate_profile, lf_reports=lf_reports,
                          ssid_name=ssid_name, security=security, security_key=security_key,
                          band=band, test="2g",
                          iteration=int(iteration), num_sta=int(client), roaming_delay=roaming_delay,
                          option="ota", channel=ch, duration=duration, duration_based=False,
                          iteration_based=True, dut_name=dut_name)

    @pytest.mark.hard_roam_6g_to_6g_dot1x_sha256
    @pytest.mark.wpa2_personal
    @pytest.mark.wpa3_personal
    def test_multi_hard_roam_6g_to_6g_802dot1x_sha256_wpa3(self, get_configuration, lf_test, lf_reports, lf_tools,
                                                           run_lf, add_env_properties,
                                                           instantiate_profile, get_controller_logs,
                                                           get_ap_config_slots,
                                                           get_lf_logs,
                                                           roaming_delay, iteration, client, duration, radius_info):
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        instantiate_profile_obj = instantiate_profile(controller_data=get_configuration['controller'],
                                                      timeout="10",
                                                      ap_data=get_configuration['access_point'],
                                                      type=0)
        print("shut down 2g  band")
        instantiate_profile_obj.ap_2ghz_shutdown()
        print("enable only 5g and 6g")
        instantiate_profile_obj.no_ap_5ghz_shutdown()
        instantiate_profile_obj.no_ap_6ghz_shutdown()

        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "sixg"
        vlan = 1
        print("disable wlan ")
        instantiate_profile_obj.disable_wlan(wlan=setup_params_general["ssid_modes"]["wpa2_personal"][0]["ssid_name"])
        instantiate_profile_obj.disable_wlan(wlan=setup_params_general["ssid_modes"]["wpa2_personal"][1]["ssid_name"])
        dut_name = []
        for i in range(len(get_configuration["access_point"])):
            dut_name.append(get_configuration["access_point"][i]["ap_name"])

        print("dut names", dut_name)

        # check channel
        lf_test.create_n_clients(sta_prefix="wlan1", num_sta=1, dut_ssid=ssid_name,
                                 dut_security=security, dut_passwd=security_key, band="sixg",
                                 lf_tools=lf_tools, type="11r-sae-802.1x")
        sta_list = lf_tools.get_station_list()
        print(sta_list)
        val = lf_test.wait_for_ip(station=sta_list)
        ch = ""
        if val:
            for sta_name in sta_list:
                sta = sta_name.split(".")[2]
                time.sleep(5)
                ch = lf_tools.station_data_query(station_name=str(sta), query="channel")
            print(ch)
            lf_test.Client_disconnect(station_name=sta_list)

        else:
            pytest.exit("station failed to get ip")
            assert False

        lf_test.hard_roam(run_lf=run_lf, get_configuration=get_configuration, lf_tools=lf_tools,
                          lf_reports=lf_reports,
                          instantiate_profile=instantiate_profile,
                          ssid_name=ssid_name, security=security, security_key=security_key,
                          band=band, test="6g",
                          iteration=int(iteration), num_sta=int(client), roaming_delay=roaming_delay,
                          option="ota", channel=ch, duration=duration, iteration_based=True,
                          duration_based=False, dut_name=dut_name, identity=identity, ttls_passwd=ttls_passwd)


# setup_params_general_two = {
#     "mode": "BRIDGE",
#     "roam": True,
#     "ft+psk": True,
#     "ft-otd": False,
#     "ft-dot1x": False,
#     "ft-dot1x_sha256": True,
#     "ssid_modes": {
#         "wpa2_personal": [{"ssid_name": "RoamAP2g", "appliedRadios": ["2G"], "security_key": "something"},
#                           {"ssid_name": "RoamAP5g", "appliedRadios": ["5G"], "security_key": "something"}],
#
#         "wpa3_personal": [{"ssid_name": "RoamAP6g", "appliedRadios": ["6G"], "security_key": "something"}]
#     },
#     "rf": {},
#     "radius": False
# }
#
# @allure.suite("Hard Roam over the air")
# @allure.feature("Roam Test")
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general_two],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")
# class TestRoamOTAdot1xSha256(object):
#
#     @pytest.mark.hard_roam_6g_to_6g_dot1x_sha256
#     @pytest.mark.wpa2_personal
#     @pytest.mark.wpa3_personal
#     def test_multi_hard_roam_6g_to_6g_802dot1x_sha256_wpa3(self, get_configuration, lf_test, lf_reports, lf_tools,
#                                                            run_lf, add_env_properties,
#                                                            instantiate_profile, get_controller_logs,
#                                                            get_ap_config_slots,
#                                                            get_lf_logs,
#                                                            roaming_delay, iteration, client, duration, radius_info):
#         ttls_passwd = radius_info["password"]
#         identity = radius_info['user']
#         instantiate_profile_obj = instantiate_profile(controller_data=get_configuration['controller'],
#                                                       timeout="10",
#                                                       ap_data=get_configuration['access_point'],
#                                                       type=0)
#         print("shut down 2g  band")
#         instantiate_profile_obj.ap_2ghz_shutdown()
#         print("enable only 5g and 6g")
#         instantiate_profile_obj.no_ap_5ghz_shutdown()
#         instantiate_profile_obj.no_ap_6ghz_shutdown()
#
#         profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][0]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "wpa3"
#         mode = "BRIDGE"
#         band = "sixg"
#         vlan = 1
#         dut_name = []
#         for i in range(len(get_configuration["access_point"])):
#             dut_name.append(get_configuration["access_point"][i]["ap_name"])
#
#         print("dut names", dut_name)
#
#         # check channel
#         lf_test.create_n_clients(sta_prefix="wlan1", num_sta=1, dut_ssid=ssid_name,
#                                  dut_security=security, dut_passwd=security_key, band="sixg",
#                                  lf_tools=lf_tools, type="11r-sae-802.1x")
#         sta_list = lf_tools.get_station_list()
#         print(sta_list)
#         val = lf_test.wait_for_ip(station=sta_list)
#         ch = ""
#         if val:
#             for sta_name in sta_list:
#                 sta = sta_name.split(".")[2]
#                 time.sleep(5)
#                 ch = lf_tools.station_data_query(station_name=str(sta), query="channel")
#             print(ch)
#             lf_test.Client_disconnect(station_name=sta_list)
#
#         else:
#             pytest.exit("station failed to get ip")
#             assert False
#
#         lf_test.hard_roam(run_lf=run_lf, get_configuration=get_configuration, lf_tools=lf_tools,
#                           lf_reports=lf_reports,
#                           instantiate_profile=instantiate_profile,
#                           ssid_name=ssid_name, security=security, security_key=security_key,
#                           band=band, test="6g",
#                           iteration=int(iteration), num_sta=int(client), roaming_delay=roaming_delay,
#                           option="ota", channel=ch, duration=duration, iteration_based=True,
#                           duration_based=False, dut_name=dut_name, identity=identity, ttls_passwd=ttls_passwd)
#
#
#
