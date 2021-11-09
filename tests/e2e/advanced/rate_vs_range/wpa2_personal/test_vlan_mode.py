# """
#
#     Advanced  Test: Rate v/s Range test under various combinations: VLAN Mode
#     pytest -m "throughput_benchmark_test and vlan" -s -vvv --skip-testrail --testbed=basic-01
#
#
# """
# import os
# import time
#
# import pytest
# import allure
#
# pytestmark = [pytest.mark.ratevsrange, pytest.mark.vlan ,pytest.mark.usefixtures("setup_test_run")]
#
#
# setup_params_general = {
#     "mode": "VLAN",
#     "ssid_modes": {
#         "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["is2dot4GHz"]},
#                  {"ssid_name": "ssid_open_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
#         "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
#                 {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
#                  "security_key": "something"}],
#         "wpa2_personal": [
#             {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
#             {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
#              "security_key": "something"}]},
#     "rf": {
#         "is5GHz": {"channelBandwidth": "is20MHz"},
#         "is5GHzL": {"channelBandwidth": "is20MHz"},
#         "is5GHzU": {"channelBandwidth": "is20MHz"}
#     },
#     "radius": False
# }
#
# @allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")
# @pytest.mark.Mhz20
# class TestRatevsRangeVlan(object):
#
#     @pytest.mark.wpa2_personal
#     @pytest.mark.twog
#     @pytest.mark.client11b
#     def test_client_wpa2_personal_2g_11b(self, get_vif_state,
#                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
#                                                  get_configuration, lf_tools):
#         """
#
#         pytest -m "ratevsrange and vlan and 11bclient" -s -vvv --skip-testrail --testbed=advanced-02
#         jira- wifi-2495
#         """
#         profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "wpa2"
#         mode = "VLAN"
#         band = "twog"
#         vlan = 100
#         dut_name = create_lanforge_chamberview_dut
#         if ssid_name not in get_vif_state:
#             allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
#             pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
#         station = lf_test.Client_Connect(ssid=ssid_name, security=security,
#                                          passkey=security_key, mode=mode, band=band,
#                                          station_name=station_names_twog, vlan_id=vlan)
#         print("station", station)
#
#         val = [['modes: 802.11b'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:TCP'],
#                ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: 1.1.3034'], ['attenuator2: 1.1.3059'],
#                ['attenuations: 0..+50..950'], ['attenuations2: 0..+50..950']]
#         if station:
#             time.sleep(3)
#             rvr_o = lf_test.ratevsrange(station_name=station_names_twog, mode=mode,
#                                        instance_name="VLAN_RVR_11B",
#                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
#             report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
#             entries = os.listdir("../reports/" + report_name + '/')
#             pdf = False
#             for i in entries:
#                 if ".pdf" in i:
#                     pdf = i
#             if pdf:
#                 allure.attach.file(source="../reports/" + report_name + "/" + pdf,
#                                    name=get_configuration["access_point"][0]["model"] + "ratevsrange")
#             print("Test Completed... Cleaning up Stations")
#             lf_test.Client_disconnect(station_name=station_names_twog)
#             kpi_val = lf_tools.read_kpi_file(column_name=None, dir_name=report_name)
#             print(str(kpi_val))
#             allure.attach(name="Kpi Data", body=str(kpi_val))
#             assert station
#         else:
#             assert False
#
#     @pytest.mark.wpa2_personal
#     @pytest.mark.twog
#     @pytest.mark.client11g
#     def test_client_wpa2_personal_2g_11g(self, get_vif_state,
#                                          lf_test, station_names_twog, create_lanforge_chamberview_dut,
#                                          get_configuration, lf_tools):
#         """
#
#         pytest -m "ratevsrange and vlan and client11g" -s -vvv --skip-testrail --testbed=advanced-02
#         jira- wifi-2496
#         """
#         profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "wpa2"
#         mode = "VLAN"
#         band = "twog"
#         vlan = 100
#         dut_name = create_lanforge_chamberview_dut
#         if ssid_name not in get_vif_state:
#             allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
#             pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
#         station = lf_test.Client_Connect(ssid=ssid_name, security=security,
#                                          passkey=security_key, mode=mode, band=band,
#                                          station_name=station_names_twog, vlan_id=vlan)
#         print("station", station)
#
#         val = [['modes: 802.11g'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:TCP'],
#                ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: 1.1.3034'], ['attenuator2: 1.1.3059'],
#                ['attenuations: 0..+50..950'], ['attenuations2: 0..+50..950']]
#
#         if station:
#             time.sleep(3)
#             rvr_o = lf_test.ratevsrange(station_name=station_names_twog, mode=mode,
#                                         instance_name="VLAN_RVR_11G",
#                                         vlan_id=vlan, dut_name=dut_name, raw_lines=val)
#             report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
#             entries = os.listdir("../reports/" + report_name + '/')
#             pdf = False
#             for i in entries:
#                 if ".pdf" in i:
#                     pdf = i
#             if pdf:
#                 allure.attach.file(source="../reports/" + report_name + "/" + pdf,
#                                    name=get_configuration["access_point"][0]["model"] + "ratevsrange")
#             print("Test Completed... Cleaning up Stations")
#             lf_test.Client_disconnect(station_name=station_names_twog)
#             kpi_val = lf_tools.read_kpi_file(column_name=None, dir_name=report_name)
#             print(str(kpi_val))
#             allure.attach(name="Kpi Data", body=str(kpi_val))
#             assert station
#         else:
#             assert False
#
#     @pytest.mark.wpa2_personal
#     @pytest.mark.fiveg
#     @pytest.mark.client11a
#     def test_client_wpa2_personal_5g_11a(self, get_vif_state,
#                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
#                                          get_configuration, lf_tools):
#         """
#
#         pytest -m "ratevsrange and vlan  and client11a" -s -vvv --skip-testrail --testbed=advanced-02
#         jira- wifi-2497
#         """
#         profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "wpa2"
#         mode = "VLAN"
#         band = "fiveg"
#         vlan = 100
#         dut_name = create_lanforge_chamberview_dut
#         if ssid_name not in get_vif_state:
#             allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
#             pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
#         station = lf_test.Client_Connect(ssid=ssid_name, security=security,
#                                          passkey=security_key, mode=mode, band=band,
#                                          station_name=station_names_fiveg, vlan_id=vlan)
#         print("station", station)
#
#         val = [['modes: 802.11a'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:TCP'],
#                ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: 1.1.3034'], ['attenuator2: 1.1.3059'],
#                ['attenuations: 0..+50..950'], ['attenuations2: 0..+50..950']]
#         if station:
#             time.sleep(3)
#             rvr_o = lf_test.ratevsrange(station_name=station_names_fiveg, mode=mode,
#                                         instance_name="VLAN_RVR_11A",
#                                         vlan_id=vlan, dut_name=dut_name, raw_lines=val)
#             report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
#             entries = os.listdir("../reports/" + report_name + '/')
#             pdf = False
#             for i in entries:
#                 if ".pdf" in i:
#                     pdf = i
#             if pdf:
#                 allure.attach.file(source="../reports/" + report_name + "/" + pdf,
#                                    name=get_configuration["access_point"][0]["model"] + "ratevsrange")
#             print("Test Completed... Cleaning up Stations")
#             lf_test.Client_disconnect(station_name=station_names_fiveg)
#             kpi_val = lf_tools.read_kpi_file(column_name=None, dir_name=report_name)
#             print(str(kpi_val))
#             allure.attach(name="Kpi Data", body=str(kpi_val))
#             assert station
#         else:
#             assert False
#
#     @pytest.mark.wpa2_personal
#     @pytest.mark.fiveg
#     @pytest.mark.client11an
#     def test_client_wpa2_personal_5g_11an(self, get_vif_state,
#                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
#                                          get_configuration,lf_tools):
#         """
#
#         pytest -m "ratevsrange and vlan and client11an" -s -vvv --skip-testrail --testbed=advanced-02
#         jira- wifi-2498
#         """
#         profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "wpa2"
#         mode = "VLAN"
#         band = "fiveg"
#         vlan = 100
#         dut_name = create_lanforge_chamberview_dut
#         if ssid_name not in get_vif_state:
#             allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
#             pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
#         station = lf_test.Client_Connect(ssid=ssid_name, security=security,
#                                          passkey=security_key, mode=mode, band=band,
#                                          station_name=station_names_fiveg, vlan_id=vlan)
#         print("station", station)
#
#         val = [['modes: 802.11an'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:TCP'],
#                ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: 1.1.3034'], ['attenuator2: 1.1.3059'],
#                ['attenuations: 0..+50..950'], ['attenuations2: 0..+50..950']]
#         if station:
#             time.sleep(3)
#             rvr_o = lf_test.ratevsrange(station_name=station_names_fiveg, mode=mode,
#                                         instance_name="VLAN_RVR_11AN",
#                                         vlan_id=vlan, dut_name=dut_name, raw_lines=val)
#             report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
#             entries = os.listdir("../reports/" + report_name + '/')
#             pdf = False
#             for i in entries:
#                 if ".pdf" in i:
#                     pdf = i
#             if pdf:
#                 allure.attach.file(source="../reports/" + report_name + "/" + pdf,
#                                    name=get_configuration["access_point"][0]["model"] + "ratevsrange")
#             print("Test Completed... Cleaning up Stations")
#             lf_test.Client_disconnect(station_name=station_names_fiveg)
#             kpi_val = lf_tools.read_kpi_file(column_name=None, dir_name=report_name)
#             print(str(kpi_val))
#             allure.attach(name="Kpi Data", body=str(kpi_val))
#             assert station
#         else:
#             assert False
#
#     @pytest.mark.performance_advanced
#     @pytest.mark.wpa2_personal
#     @pytest.mark.fiveg
#     @pytest.mark.client11ac
#     def test_client_wpa2_personal_5g_11ac(self, get_vif_state,
#                                           lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
#                                           get_configuration, lf_tools):
#         """
#
#         pytest -m "ratevsrange and vlan and client11ac" -s -vvv --skip-testrail --testbed=advanced-02
#         jira- wifi-2499
#         """
#         profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "wpa2"
#         mode = "VLAN"
#         band = "fiveg"
#         vlan = 1
#         dut_name = create_lanforge_chamberview_dut
#         if ssid_name not in get_vif_state:
#             allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
#             pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
#         station = lf_test.Client_Connect(ssid=ssid_name, security=security,
#                                          passkey=security_key, mode=mode, band=band,
#                                          station_name=station_names_fiveg, vlan_id=vlan)
#         print("station", station)
#
#         val = [['modes: 802.11an-AC'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:TCP'],
#                ['bandw_options: AUTO'], ['spatial_streams: AUTO'], ['attenuator: 1.1.3034'], ['attenuator2: 1.1.3059'],
#                ['attenuations: 0..+50..950'], ['attenuations2: 0..+50..950']]
#
#         if station:
#             time.sleep(3)
#             rvr_o = lf_test.ratevsrange(station_name=station_names_fiveg, mode=mode,
#                                         instance_name="VLAN_RVR_11AC",
#                                         vlan_id=vlan, dut_name=dut_name, raw_lines=val)
#             report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
#             entries = os.listdir("../reports/" + report_name + '/')
#             pdf = False
#             for i in entries:
#                 if ".pdf" in i:
#                     pdf = i
#             if pdf:
#                 allure.attach.file(source="../reports/" + report_name + "/" + pdf,
#                                    name=get_configuration["access_point"][0]["model"] + "ratevsrange")
#             print("Test Completed... Cleaning up Stations")
#             lf_test.Client_disconnect(station_name=station_names_fiveg)
#             kpi_val = lf_tools.read_kpi_file(column_name=None, dir_name=report_name)
#             print(str(kpi_val))
#             allure.attach(name="Kpi Data", body=str(kpi_val))
#             assert station
#         else:
#             assert False
