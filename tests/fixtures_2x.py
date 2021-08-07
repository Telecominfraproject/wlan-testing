""" Python Inbuilt Libraries """
import allure
import pytest
import sys
import os
import json
import time

""" Environment Paths """
if "libs" not in sys.path:
    sys.path.append(f'../libs')
for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../lanforge/lanforge-scripts/{folder}')

sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)
sys.path.append(f"../lanforge/lanforge-scripts/py-scripts/tip-cicd-sanity")

sys.path.append(f'../libs')
sys.path.append(f'../libs/lanforge/')

from LANforge.LFUtils import *

if 'py-json' not in sys.path:
    sys.path.append('../py-scripts')
from apnos.apnos import APNOS
from controller.controller_2x.controller import Controller
from configuration import CONFIGURATION
from configuration import RADIUS_SERVER_DATA
from configuration import RADIUS_ACCOUNTING_DATA


class Fixtures_2x:

    def __init__(self, configuration={}):
        self.lab_info = configuration
        print(self.lab_info)
        print("2.X")
        try:
            self.controller_obj = Controller(controller_data=self.lab_info["controller"])
        except Exception as e:
            print(e)
            allure.attach(body=str(e), name="Controller Instantiation Failed: ")
            sdk_client = False
            pytest.exit("unable to communicate to Controller" + str(e))

    def disconnect(self):
        self.controller_obj.logout()

    def setup_firmware(self):
        pass

    def get_ap_version(self, get_apnos, get_configuration):
        version_list = []
        for access_point_info in get_configuration['access_point']:
            ap_ssh = get_apnos(access_point_info)
            version = ap_ssh.get_ap_version_ucentral()
            version_list.append(version)
        return version_list

    def setup_profiles(self, request, param, setup_controller, testbed, setup_vlan, get_equipment_id,
                       instantiate_profile, get_markers, create_lanforge_chamberview_dut, lf_tools,
                       get_security_flags, get_configuration, radius_info, get_apnos, radius_accounting_info):
        print("inside conftest_2x")
        if not request.config.getoption("1.x"):
            instantiate_profile_obj = instantiate_profile(sdk_client=setup_controller)
            print("garbage")
            print(1, instantiate_profile_obj.sdk_client)
            vlan_id, mode = 0, 0
            parameter = dict(param)
            print("hola", parameter)
            test_cases = {}
            profile_data = {}

            if parameter['mode'] not in ["BRIDGE", "NAT", "VLAN"]:
                print("Invalid Mode: ", parameter['mode'])
                return test_cases

            instantiate_profile_obj.set_radio_config()

            if parameter['mode'] == "NAT":
                mode = "NAT"
                instantiate_profile_obj.set_mode(mode=mode)
                vlan_id = 1
            if parameter['mode'] == "BRIDGE":
                mode = "BRIDGE"
                instantiate_profile_obj.set_mode(mode=mode)
                vlan_id = 1
            if parameter['mode'] == "VLAN":
                mode = "VLAN"
                instantiate_profile_obj.set_mode(mode=mode)
                vlan_id = setup_vlan
            profile_data["ssid"] = {}

            for i in parameter["ssid_modes"]:
                profile_data["ssid"][i] = []
                for j in range(len(parameter["ssid_modes"][i])):
                    data = parameter["ssid_modes"][i][j]
                    profile_data["ssid"][i].append(data)
            lf_dut_data = []
            for mode in profile_data['ssid']:
                if mode == "open":
                    for j in profile_data["ssid"][mode]:
                        if mode in get_markers.keys() and get_markers[mode]:
                            try:
                                if j["appliedRadios"].__contains__("2G"):
                                    lf_dut_data.append(j)
                                if j["appliedRadios"].__contains__("5G"):
                                    lf_dut_data.append(j)
                                j["appliedRadios"] = list(set(j["appliedRadios"]))
                                j['security'] = 'none'
                                creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j)
                                test_cases["wpa_2g"] = True
                            except Exception as e:
                                print(e)
                                test_cases["wpa_2g"] = False
                if mode == "wpa":
                    for j in profile_data["ssid"][mode]:
                        if mode in get_markers.keys() and get_markers[mode]:
                            try:
                                if j["appliedRadios"].__contains__("2G"):
                                    lf_dut_data.append(j)
                                if j["appliedRadios"].__contains__("5G"):
                                    lf_dut_data.append(j)
                                j["appliedRadios"] = list(set(j["appliedRadios"]))
                                j['security'] = 'psk'
                                creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j)
                                test_cases["wpa_2g"] = True
                            except Exception as e:
                                print(e)
                                test_cases["wpa_2g"] = False
                if mode == "wpa2_personal":
                    for j in profile_data["ssid"][mode]:
                        if mode in get_markers.keys() and get_markers[mode]:
                            try:
                                if j["appliedRadios"].__contains__("2G"):
                                    lf_dut_data.append(j)
                                if j["appliedRadios"].__contains__("5G"):
                                    lf_dut_data.append(j)
                                j["appliedRadios"] = list(set(j["appliedRadios"]))
                                j['security'] = 'psk2'
                                creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j)
                                test_cases["wpa_2g"] = True
                            except Exception as e:
                                print(e)
                                test_cases["wpa2_personal"] = False
                if mode == "wpa_wpa2_personal_mixed":
                    for j in profile_data["ssid"][mode]:
                        if mode in get_markers.keys() and get_markers[mode]:
                            try:
                                if j["appliedRadios"].__contains__("2G"):
                                    lf_dut_data.append(j)
                                if j["appliedRadios"].__contains__("5G"):
                                    lf_dut_data.append(j)
                                j["appliedRadios"] = list(set(j["appliedRadios"]))
                                j['security'] = 'psk-mixed'
                                creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j)
                                test_cases["wpa_2g"] = True
                            except Exception as e:
                                print(e)
                                test_cases["wpa2_personal"] = False
                if mode == "wpa3_personal":
                    for j in profile_data["ssid"][mode]:
                        if mode in get_markers.keys() and get_markers[mode]:
                            try:
                                if j["appliedRadios"].__contains__("2G"):
                                    lf_dut_data.append(j)
                                if j["appliedRadios"].__contains__("5G"):
                                    lf_dut_data.append(j)
                                j["appliedRadios"] = list(set(j["appliedRadios"]))
                                j['security'] = 'sae'
                                creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j)
                                test_cases["wpa_2g"] = True
                            except Exception as e:
                                print(e)
                                test_cases["wpa2_personal"] = False
                if mode == "wpa3_personal_mixed":
                    for j in profile_data["ssid"][mode]:
                        if mode in get_markers.keys() and get_markers[mode]:
                            try:
                                if j["appliedRadios"].__contains__("2G"):
                                    lf_dut_data.append(j)
                                if j["appliedRadios"].__contains__("5G"):
                                    lf_dut_data.append(j)
                                j["appliedRadios"] = list(set(j["appliedRadios"]))
                                j['security'] = 'sae-mixed'
                                creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j)
                                test_cases["wpa_2g"] = True
                            except Exception as e:
                                print(e)
                                test_cases["wpa2_personal"] = False
                # EAP SSID Modes
                if mode == "wpa2_enterprise":
                    for j in profile_data["ssid"][mode]:
                        if mode in get_markers.keys() and get_markers[mode]:
                            try:
                                if j["appliedRadios"].__contains__("2G"):
                                    lf_dut_data.append(j)
                                if j["appliedRadios"].__contains__("5G"):
                                    lf_dut_data.append(j)
                                j["appliedRadios"] = list(set(j["appliedRadios"]))
                                j['security'] = 'wpa2'
                                RADIUS_SERVER_DATA = radius_info
                                RADIUS_ACCOUNTING_DATA = radius_accounting_info
                                creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j, radius=True,
                                                                                   radius_auth_data=RADIUS_SERVER_DATA,
                                                                                   radius_accounting_data=RADIUS_ACCOUNTING_DATA)
                                test_cases["wpa_2g"] = True
                            except Exception as e:
                                print(e)
                                test_cases["wpa2_personal"] = False
            ap_ssh = get_apnos(get_configuration['access_point'][0], pwd="../libs/apnos/", sdk="2.x")
            connected, latest, active = ap_ssh.get_ucentral_status()
            if connected == False:
                pytest.exit("AP is disconnected from UC Gateway")
            if latest != active:
                allure.attach(name="FAIL : ubus call ucentral status: ",
                              body="connected: " + str(connected) + "\nlatest: " + str(latest) + "\nactive: " + str(active))
                ap_logs = ap_ssh.logread()
                allure.attach(body=ap_logs, name="FAILURE: AP LOgs: ")
                pytest.fail("AP is disconnected from UC Gateway")
            instantiate_profile_obj.push_config(serial_number=get_equipment_id[0])
            time_1 = time.time()
            config = json.loads(str(instantiate_profile_obj.base_profile_config).replace(" ", "").replace("'", '"'))
            config["uuid"] = 0
            ap_config_latest = ap_ssh.get_uc_latest_config()
            try:
                ap_config_latest["uuid"] = 0
            except Exception as e:
                print(e)
                pass
            x = 1
            old_config = latest
            connected, latest, active = ap_ssh.get_ucentral_status()
            while old_config == latest:
                time.sleep(5)
                x += 1
                print("old config: " , old_config)
                print("latest: " , latest)
                connected, latest, active = ap_ssh.get_ucentral_status()
                if x == 19:
                    break
            connected, latest, active = ap_ssh.get_ucentral_status()
            x = 1
            while active != latest:
                connected, latest, active = ap_ssh.get_ucentral_status()
                time.sleep(10)
                x += 1
                print("active: ", active)
                print("latest: ", latest)
                if x == 19:
                    break
            if x < 19:
                print("Config properly applied into AP", config)
            ap_config_latest = ap_ssh.get_uc_latest_config()
            ap_config_latest["uuid"] = 0

            ap_config_active = ap_ssh.get_uc_active_config()
            ap_config_active["uuid"] = 0
            x = 1
            while ap_config_active != ap_config_latest:
                time.sleep(5)
                x += 1
                ap_config_latest = ap_ssh.get_uc_latest_config()
                ap_config_latest["uuid"] = 0

                ap_config_active = ap_ssh.get_uc_active_config()
                print("latest config:   ", ap_config_latest)
                print("Active config:  ", ap_config_active)
                ap_config_active["uuid"] = 0
                if x == 19:
                    break
            allure_body = "AP config status: \n" + \
                          "Active Config: " + str(ap_ssh.get_uc_active_config()) + "\n" \
                                                                                   "Latest Config: ", str(
                ap_ssh.get_uc_latest_config()) + "\n" \
                                                 "Applied Config: ", str(config)

            if x < 19:
                print("AP is Broadcasting Applied Config")
                allure.attach(name="AP is Broadcasting Applied Config", body="")
                allure.attach(name="Config Info", body="Applied Config: " + str(ap_config_active))
                allure.attach(name="Config Info",
                              body="AP is Broadc3asting Applied Config: " + str(ap_ssh.get_uc_active_config()))
                allure.attach(name="Config Info", body="AP is Broadcasting Applied Config: " + str(allure_body))

            else:
                print("AP is Not Broadcasting Applied Config")
                allure.attach(name="AP is Not Broadcasting Applied Config", body="")
                allure.attach(name="Config Info", body="Applied Config: " + str(ap_config_active))
                allure.attach(name="Config Info",
                              body="AP is Broadc3asting Applied Config: " + str(ap_ssh.get_uc_active_config()))
                allure.attach(name="Config Info", body="AP is Broadcasting Applied Config: " + str(allure_body))
            time_2 = time.time()
            time_interval = time_2 - time_1
            allure.attach(name="Time Took to apply Config: " + str(time_interval), body="")
            ap_logs = ap_ssh.logread()
            allure.attach(body=ap_logs, name="AP LOgs: ")
            ap_wifi_data = ap_ssh.get_interface_details()
            idx_mapping = {}
            ssid_data = []
            ap_interfaces = list(ap_wifi_data.keys())
            for interface in range(len(ap_interfaces)):
                if ap_wifi_data[ap_interfaces[interface]][1] == "none":
                    ssid = ["ssid_idx=" + str(interface) +
                            " ssid=" + ap_wifi_data[ap_interfaces[interface]][0] +
                            " security=OPEN" +
                            " bssid=" + ap_wifi_data[ap_interfaces[interface]][3][0]
                            ]
                    idx_mapping[str(interface)] = [ap_wifi_data[ap_interfaces[interface]][0],
                                                   ap_wifi_data[ap_interfaces[interface]][2],
                                                   ap_wifi_data[ap_interfaces[interface]][1],
                                                   ap_wifi_data[ap_interfaces[interface]][3][1],
                                                   ap_wifi_data[ap_interfaces[interface]][3][0]
                                                   ]
                    # pass
                if ap_wifi_data[ap_interfaces[interface]][1] == "psk":
                    ssid = ["ssid_idx=" + str(interface) +
                            " ssid=" + ap_wifi_data[ap_interfaces[interface]][0] +
                            " security=WPA" +
                            " password=" + ap_wifi_data[ap_interfaces[interface]][2] +
                            " bssid=" + ap_wifi_data[ap_interfaces[interface]][3][0]
                            ]
                    idx_mapping[str(interface)] = [ap_wifi_data[ap_interfaces[interface]][0],
                                                   ap_wifi_data[ap_interfaces[interface]][2],
                                                   ap_wifi_data[ap_interfaces[interface]][1],
                                                   ap_wifi_data[ap_interfaces[interface]][3][1],
                                                   ap_wifi_data[ap_interfaces[interface]][3][0]
                                                   ]
                    # pass
                if ap_wifi_data[ap_interfaces[interface]][1] == "psk-mixed":
                    ssid = ["ssid_idx=" + str(interface) +
                            " ssid=" + ap_wifi_data[ap_interfaces[interface]][0] +
                            " security=WPA|WPA2" +
                            " password=" + ap_wifi_data[ap_interfaces[interface]][2] +
                            " bssid=" + ap_wifi_data[ap_interfaces[interface]][3][0]
                            ]
                    idx_mapping[str(interface)] = [ap_wifi_data[ap_interfaces[interface]][0],
                                                   ap_wifi_data[ap_interfaces[interface]][2],
                                                   ap_wifi_data[ap_interfaces[interface]][1],
                                                   ap_wifi_data[ap_interfaces[interface]][3][1],
                                                   ap_wifi_data[ap_interfaces[interface]][3][0]
                                                   ]
                    # pass
                if ap_wifi_data[ap_interfaces[interface]][1] == "psk2":
                    ssid = ["ssid_idx=" + str(interface) +
                            " ssid=" + ap_wifi_data[ap_interfaces[interface]][0] +
                            " security=WPA2" +
                            " password=" + ap_wifi_data[ap_interfaces[interface]][2] +
                            " bssid=" + str(ap_wifi_data[ap_interfaces[interface]][3][0]).lower()
                            ]
                    print(ssid)
                    idx_mapping[str(interface)] = [ap_wifi_data[ap_interfaces[interface]][0],
                                                   ap_wifi_data[ap_interfaces[interface]][2],
                                                   ap_wifi_data[ap_interfaces[interface]][1],
                                                   ap_wifi_data[ap_interfaces[interface]][3][1],
                                                   ap_wifi_data[ap_interfaces[interface]][3][0]
                                                   ]
                    # pass
                if ap_wifi_data[ap_interfaces[interface]][1] == "sae":
                    ssid = ["ssid_idx=" + str(interface) +
                            " ssid=" + ap_wifi_data[ap_interfaces[interface]][0] +
                            " security=WPA3" +
                            " password=" + ap_wifi_data[ap_interfaces[interface]][2] +
                            " bssid=" + ap_wifi_data[ap_interfaces[interface]][3][0]
                            ]
                    idx_mapping[str(interface)] = [ap_wifi_data[ap_interfaces[interface]][0],
                                                   ap_wifi_data[ap_interfaces[interface]][2],
                                                   ap_wifi_data[ap_interfaces[interface]][1],
                                                   ap_wifi_data[ap_interfaces[interface]][3][1],
                                                   ap_wifi_data[ap_interfaces[interface]][3][0]
                                                   ]
                    # pass
                if ap_wifi_data[ap_interfaces[interface]][1] == "sae-mixed":
                    ssid = ["ssid_idx=" + str(interface) +
                            " ssid=" + ap_wifi_data[ap_interfaces[interface]][0] +
                            " security=WPA3" +
                            " password=" + ap_wifi_data[ap_interfaces[interface]][2] +
                            " bssid=" + ap_wifi_data[ap_interfaces[interface]][3][0]
                            ]
                    idx_mapping[str(interface)] = [ap_wifi_data[ap_interfaces[interface]][0],
                                                   ap_wifi_data[ap_interfaces[interface]][2],
                                                   ap_wifi_data[ap_interfaces[interface]][1],
                                                   ap_wifi_data[ap_interfaces[interface]][3][1],
                                                   ap_wifi_data[ap_interfaces[interface]][3][0]
                                                   ]
                    # pass
                if ap_wifi_data[ap_interfaces[interface]][1] == "wpa2":
                    ssid = ["ssid_idx=" + str(interface) +
                            " ssid=" + ap_wifi_data[ap_interfaces[interface]][0] +
                            " security=EAP-TTLS" +
                            " bssid=" + str(ap_wifi_data[ap_interfaces[interface]][3][0]).lower()
                            ]

                    idx_mapping[str(interface)] = [ap_wifi_data[ap_interfaces[interface]][0],
                                                   ap_wifi_data[ap_interfaces[interface]][2],
                                                   ap_wifi_data[ap_interfaces[interface]][1],
                                                   ap_wifi_data[ap_interfaces[interface]][3][1],
                                                   ap_wifi_data[ap_interfaces[interface]][3][0]
                                                   ]
                    # pass
                ssid_data.append(ssid)
                lf_tools.ssid_list.append(ap_wifi_data[ap_interfaces[interface]][0])
            lf_tools.dut_idx_mapping = idx_mapping
            print(ssid_data)
            lf_tools.reset_scenario()
            lf_tools.update_ssid(ssid_data=ssid_data)
            return test_cases
        else:
            return False
