# import pytest
# import sys
#
# for folder in 'py-json', 'py-scripts':
#     if folder not in sys.path:
#         sys.path.append(f'../lanforge/lanforge-scripts/{folder}')
#
# sys.path.append(f"../lanforge/lanforge-scripts/py-scripts/tip-cicd-something")
#
# sys.path.append(f'../libs')
# sys.path.append(f'../libs/lanforge/')
#
# from LANforge.LFUtils import *
#
# if 'py-json' not in sys.path:
#     sys.path.append('../py-scripts')
#
# import sta_connect2
# from sta_connect2 import StaConnect2
# import eap_connect
# from eap_connect import EAPConnect
# import time
#
#
# @pytest.mark.usefixtures('setup_cloudsdk')
# @pytest.mark.usefixtures('upgrade_firmware')
# class TestVLANModeClientConnectivity(object):
#
#     @pytest.mark.something
#     @pytest.mark.vlan
#     @pytest.mark.wpa2_personal
#     @pytest.mark.wpa2_personal_5g
#     def test_single_client_wpa2_personal_5g(self, setup_cloudsdk, upgrade_firmware, setup_vlan_mode,
#                                             disconnect_cloudsdk, get_lanforge_data):
#         profile_data = setup_vlan_mode[3]['wpa2_personal']['5g']
#         staConnect = StaConnect2(get_lanforge_data["lanforge_ip"], int(get_lanforge_data["lanforge-port-number"]),
#                                  debug_=False)
#         staConnect.sta_mode = 0
#         staConnect.upstream_resource = 1
#         staConnect.upstream_port = get_lanforge_data["lanforge_vlan_port"]
#         staConnect.radio = get_lanforge_data["lanforge_5g"]
#         staConnect.resource = 1
#         staConnect.dut_ssid = profile_data["ssid_name"]
#         staConnect.dut_passwd = profile_data["security_key"]
#         staConnect.dut_security = profile_data["security_key"].split("-")[1].split("_")[0].lower()
#         staConnect.station_names = [get_lanforge_data["lanforge_5g_station"]]
#         staConnect.sta_prefix = get_lanforge_data["lanforge_5g_prefix"]
#         staConnect.runtime_secs = 10
#         staConnect.bringup_time_sec = 60
#         staConnect.cleanup_on_exit = True
#         # staConnect.cleanup()
#         staConnect.setup()
#         staConnect.start()
#         print("napping %f sec" % staConnect.runtime_secs)
#         time.sleep(staConnect.runtime_secs)
#         staConnect.stop()
#         staConnect.cleanup()
#         run_results = staConnect.get_result_list()
#         for result in run_results:
#             print("test result: " + result)
#         # result = 'pass'
#         print("Single Client Connectivity :", staConnect.passes)
#         assert staConnect.passes()
#         # C5248
#
#     @pytest.mark.something
#     @pytest.mark.vlan
#     @pytest.mark.wpa2_personal
#     @pytest.mark.wpa2_personal_2g
#     def test_single_client_wpa2_personal_2g(self, setup_cloudsdk, upgrade_firmware, setup_vlan_mode,
#                                             disconnect_cloudsdk, get_lanforge_data):
#         profile_data = setup_vlan_mode[3]['wpa2_personal']['2g']
#         staConnect = StaConnect2(get_lanforge_data["lanforge_ip"], int(get_lanforge_data["lanforge-port-number"]),
#                                  debug_=False)
#         staConnect.sta_mode = 0
#         staConnect.upstream_resource = 1
#         staConnect.upstream_port = get_lanforge_data["lanforge_vlan_port"]
#         staConnect.radio = get_lanforge_data["lanforge_5g"]
#         staConnect.resource = 1
#         staConnect.dut_ssid = profile_data["ssid_name"]
#         staConnect.dut_passwd = profile_data["security_key"]
#         staConnect.dut_security = profile_data["security_key"].split("-")[1].split("_")[0].lower()
#         staConnect.station_names = [get_lanforge_data["lanforge_5g_station"]]
#         staConnect.sta_prefix = get_lanforge_data["lanforge_5g_prefix"]
#         staConnect.runtime_secs = 10
#         staConnect.bringup_time_sec = 60
#         staConnect.cleanup_on_exit = True
#         # staConnect.cleanup()
#         staConnect.setup()
#         staConnect.start()
#         print("napping %f sec" % staConnect.runtime_secs)
#         time.sleep(staConnect.runtime_secs)
#         staConnect.stop()
#         staConnect.cleanup()
#         run_results = staConnect.get_result_list()
#         for result in run_results:
#             print("test result: " + result)
#         # result = 'pass'
#         print("Single Client Connectivity :", staConnect.passes)
#         assert staConnect.passes()
#         # C5251
#
#     @pytest.mark.something
#     @pytest.mark.vlan
#     @pytest.mark.wpa
#     @pytest.mark.wpa_5g
#     def test_single_client_wpa_5g(self, setup_cloudsdk, upgrade_firmware, setup_vlan_mode,
#                                   disconnect_cloudsdk, get_lanforge_data):
#         profile_data = setup_vlan_mode[3]['wpa']['5g']
#         staConnect = StaConnect2(get_lanforge_data["lanforge_ip"], int(get_lanforge_data["lanforge-port-number"]),
#                                  debug_=False)
#         staConnect.sta_mode = 0
#         staConnect.upstream_resource = 1
#         staConnect.upstream_port = get_lanforge_data["lanforge_vlan_port"]
#         staConnect.radio = get_lanforge_data["lanforge_5g"]
#         staConnect.resource = 1
#         staConnect.dut_ssid = profile_data["ssid_name"]
#         staConnect.dut_passwd = profile_data["security_key"]
#         staConnect.dut_security = profile_data["security_key"].split("-")[1].split("_")[0].lower()
#         staConnect.station_names = [get_lanforge_data["lanforge_5g_station"]]
#         staConnect.sta_prefix = get_lanforge_data["lanforge_5g_prefix"]
#         staConnect.runtime_secs = 10
#         staConnect.bringup_time_sec = 60
#         staConnect.cleanup_on_exit = True
#         # staConnect.cleanup()
#         staConnect.setup()
#         staConnect.start()
#         print("napping %f sec" % staConnect.runtime_secs)
#         time.sleep(staConnect.runtime_secs)
#         staConnect.stop()
#         staConnect.cleanup()
#         run_results = staConnect.get_result_list()
#         for result in run_results:
#             print("test result: " + result)
#         # result = 'pass'
#         print("Single Client Connectivity :", staConnect.passes)
#         assert staConnect.passes()
#         # C5249
#
#     @pytest.mark.something
#     @pytest.mark.vlan
#     @pytest.mark.wpa
#     @pytest.mark.wpa_2g
#     def test_single_client_wpa_2g(self, setup_cloudsdk, upgrade_firmware, setup_vlan_mode,
#                                   disconnect_cloudsdk, get_lanforge_data):
#         profile_data = setup_vlan_mode[3]['wpa']['2g']
#         staConnect = StaConnect2(get_lanforge_data["lanforge_ip"], int(get_lanforge_data["lanforge-port-number"]),
#                                  debug_=False)
#         staConnect.sta_mode = 0
#         staConnect.upstream_resource = 1
#         staConnect.upstream_port = get_lanforge_data["lanforge_vlan_port"]
#         staConnect.radio = get_lanforge_data["lanforge_5g"]
#         staConnect.resource = 1
#         staConnect.dut_ssid = profile_data["ssid_name"]
#         staConnect.dut_passwd = profile_data["security_key"]
#         staConnect.dut_security = profile_data["security_key"].split("-")[1].split("_")[0].lower()
#         staConnect.station_names = [get_lanforge_data["lanforge_5g_station"]]
#         staConnect.sta_prefix = get_lanforge_data["lanforge_5g_prefix"]
#         staConnect.runtime_secs = 10
#         staConnect.bringup_time_sec = 60
#         staConnect.cleanup_on_exit = True
#         # staConnect.cleanup()
#         staConnect.setup()
#         staConnect.start()
#         print("napping %f sec" % staConnect.runtime_secs)
#         time.sleep(staConnect.runtime_secs)
#         staConnect.stop()
#         staConnect.cleanup()
#         run_results = staConnect.get_result_list()
#         for result in run_results:
#             print("test result: " + result)
#         # result = 'pass'
#         print("Single Client Connectivity :", staConnect.passes)
#         assert staConnect.passes()
#         # C5252
#
#     @pytest.mark.something
#     @pytest.mark.vlan
#     @pytest.mark.wpa2_enterprise
#     @pytest.mark.wpa2_enterprise_5g
#     def test_single_client_wpa2_enterprise_5g(self, setup_cloudsdk, upgrade_firmware, setup_vlan_mode,
#                                               disconnect_cloudsdk, get_lanforge_data):
#         profile_data = setup_vlan_mode[3]['wpa2_enterprise']['5g']
#         eap_connect = EAPConnect(get_lanforge_data["lanforge_ip"], get_lanforge_data["lanforge-port-number"])
#         eap_connect.upstream_resource = 1
#         eap_connect.upstream_port = get_lanforge_data["lanforge_vlan_port"]
#         eap_connect.security = "wpa2"
#         eap_connect.sta_list = [get_lanforge_data["lanforge_5g_station"]]
#         eap_connect.station_names = [get_lanforge_data["lanforge_5g_station"]]
#         eap_connect.sta_prefix = get_lanforge_data["lanforge_5g_prefix"]
#         eap_connect.ssid = profile_data["ssid_name"]
#         eap_connect.radio = get_lanforge_data["lanforge_5g"]
#         eap_connect.eap = "TTLS"
#         eap_connect.identity = "nolaradius"
#         eap_connect.ttls_passwd = "nolastart"
#         eap_connect.runtime_secs = 10
#         eap_connect.setup()
#         eap_connect.start()
#         print("napping %f sec" % eap_connect.runtime_secs)
#         time.sleep(eap_connect.runtime_secs)
#         eap_connect.stop()
#         eap_connect.cleanup()
#         run_results = eap_connect.get_result_list()
#         for result in run_results:
#             print("test result: " + result)
#         # result = 'pass'
#         print("Single Client Connectivity :", eap_connect.passes)
#         assert eap_connect.passes()
#         # C5250
#
#     @pytest.mark.something
#     @pytest.mark.vlan
#     @pytest.mark.wpa2_enterprise
#     @pytest.mark.wpa2_enterprise_2g
#     def test_single_client_wpa2_enterprise_2g(self, setup_cloudsdk, upgrade_firmware, setup_vlan_mode,
#                                               disconnect_cloudsdk, get_lanforge_data):
#         profile_data = setup_vlan_mode[3]['wpa2_enterprise']['2g']
#         eap_connect = EAPConnect(get_lanforge_data["lanforge_ip"], get_lanforge_data["lanforge-port-number"])
#         eap_connect.upstream_resource = 1
#         eap_connect.upstream_port = get_lanforge_data["lanforge_vlan_port"]
#         eap_connect.security = "wpa2"
#         eap_connect.sta_list = [get_lanforge_data["lanforge_5g_station"]]
#         eap_connect.station_names = [get_lanforge_data["lanforge_5g_station"]]
#         eap_connect.sta_prefix = get_lanforge_data["lanforge_5g_prefix"]
#         eap_connect.ssid = profile_data["ssid_name"]
#         eap_connect.radio = get_lanforge_data["lanforge_5g"]
#         eap_connect.eap = "TTLS"
#         eap_connect.identity = "nolaradius"
#         eap_connect.ttls_passwd = "nolastart"
#         eap_connect.runtime_secs = 10
#         eap_connect.setup()
#         eap_connect.start()
#         print("napping %f sec" % eap_connect.runtime_secs)
#         time.sleep(eap_connect.runtime_secs)
#         eap_connect.stop()
#         eap_connect.cleanup()
#         run_results = eap_connect.get_result_list()
#         for result in run_results:
#             print("test result: " + result)
#         # result = 'pass'
#         print("Single Client Connectivity :", eap_connect.passes)
#         assert eap_connect.passes()
#         # C5253
