import allure
import pytest
import os
import sys
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
sys.path.append(f'../lanforge/lanforge-scripts')

from LANforge.LFUtils import *

if 'py-json' not in sys.path:
    sys.path.append('../py-scripts')
from controller.controller_3x.controller import CController


class Fixtures_3x:

    def __init__(self, configuration={}, run_lf=False, cc_1=False):
        self.lab_info = configuration
        self.run_lf = run_lf
        self.cc_1 = cc_1
        # print(self.lab_info)
        print("cc.1")
        self.controller_obj = ""
        if not run_lf:
            try:
                self.controller_obj = CController(controller_data=self.lab_info["controller"], timeout="10")
            except Exception as e:
                print(e)
                allure.attach(body=str(e), name="Controller Instantiation Failed: ")
                sdk_client = False
                pytest.exit("unable to communicate to Controller" + str(e))

    def get_ap_version(self, get_apnos, get_configuration):

        version_list = []
        if self.cc_1:
            version_list.append(get_configuration['access_point']['version'])
        if not self.run_lf and not self.cc_1:
            for access_point_info in get_configuration['access_point']:
                ap_ssh = get_apnos(access_point_info)
                version = ap_ssh.get_ap_version_ucentral()
                version_list.append(version)
        return version_list


    def setup_profiles(self, request, param, run_lf, instantiate_profile, get_configuration, get_markers):
        if run_lf:
            return 0
        print("hi nikita")
        parameter = dict(param)
        print("parameter", parameter)
        # print(get_configuration)
        instantiate_profile_obj = instantiate_profile(controller_data=get_configuration['controller'], timeout="10")
        print(1, instantiate_profile_obj)
        vlan_id, mode = 0, 0

        test_cases = {}
        profile_data = {}
        var = ""
        list_key = list(parameter.keys())
        if parameter['mode'] not in ["BRIDGE", "NAT", "VLAN"]:
            print("Invalid Mode: ", parameter['mode'])
            return test_cases
        profile_data["ssid"] = {}
        lf_dut_data = []
        for i in parameter["ssid_modes"]:
            profile_data["ssid"][i] = []
            for j in range(len(parameter["ssid_modes"][i])):
                data = parameter["ssid_modes"][i][j]
                profile_data["ssid"][i].append(data)
        print(profile_data)

        # create wlan
        for mode in profile_data['ssid']:
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
                            # print("dut data", lf_dut_data)
                            test_cases["wpa_2g"] = True
                        except Exception as e:
                            print(e)
                            test_cases["wpa2_personal"] = False

        print("lf dut data", lf_dut_data)
        instantiate_profile_obj = instantiate_profile(controller_data=get_configuration['controller'], timeout="10",
                                                      ssid_data=lf_dut_data)
        instantiate_profile_obj.no_logging_console()
        instantiate_profile_obj.line_console()
        instantiate_profile_obj.show_shutdown_5ghz_ap()
        instantiate_profile_obj.disable_wlan()
        instantiate_profile_obj.ap_5ghz_shutdown()
        instantiate_profile_obj.get_ssids()
        instantiate_profile_obj.delete_wlan()
        instantiate_profile_obj.get_ssids()
        instantiate_profile_obj.create_wlan_wpa2()
        instantiate_profile_obj.config_wireless_tag_policy_and_policy_profile()
        instantiate_profile_obj.enable_wlan()
        instantiate_profile_obj.enable_5ghz_netwrk()
        instantiate_profile_obj.enable_ap_5ghz()
        instantiate_profile_obj.show_5ghz_summary()
        instantiate_profile_obj.get_ssids()
