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

    def setup_profiles(self, request, param, run_lf, instantiate_profile, get_configuration, get_markers, lf_tools):
        if run_lf:
            return 0
        print("check params")
        # gives parameter value of setup_params_general
        parameter = dict(param)
        print("parameter", parameter)


        test_cases = {}
        profile_data= {}
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

        # profile data will give ssid data like {'ssid': {'wpa2_personal': [{'ssid_name': 'ssid_wpa2_2g', 'appliedRadios': ['2G'], 'security_key': 'something'}, {'ssid_name': 'ssid_wpa2_5g', 'appliedRadios': ['5G'], 'security_key': 'something'}], 'wpa3_personal': [{'ssid_name': 'ssid_wpa2_5g', 'appliedRadios': ['6G'], 'security_key': 'something'}]}}
        print("profile data", profile_data)


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
                            if j["appliedRadios"].__contains__("6G"):
                                lf_dut_data.append(j)
                            j["appliedRadios"] = list(set(j["appliedRadios"]))
                            j['security'] = 'wpa2'
                            # print("dut data", lf_dut_data)
                            test_cases["wpa_2g"] = True
                        except Exception as e:
                            print(e)
                            test_cases["wpa2_personal"] = False
            if mode == "wpa3_personal":
                for j in profile_data["ssid"][mode]:
                    if mode in get_markers.keys() and get_markers[mode]:
                        print( profile_data["ssid"][mode])
                        print(j)
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("6G"):
                                lf_dut_data.append(j)
                                print(lf_dut_data)
                            j["appliedRadios"] = list(set(j["appliedRadios"]))
                            j['security'] = 'wpa3'
                            test_cases["wpa_2g"] = True
                        except Exception as e:
                            print(e)
                            test_cases["wpa3_personal"] = False

        # lf dut data [{'ssid_name': 'ssid_wpa2_2g', 'appliedRadios': ['2G'], 'security_key': 'something', 'security': 'wpa2'}, {'ssid_name': 'ssid_wpa2_5g', 'appliedRadios': ['5G'], 'security_key': 'something', 'security': 'wpa2'}, {'ssid_name': 'ssid_wpa2_5g', 'appliedRadios': ['6G'], 'security_key': 'something', 'security': 'wpa3'}]
        print("lf dut data", lf_dut_data)

        # if parameter["roam"] == True:
        print("create 3 wlans on slot1,2 and 3")
        for ap_name in range(len(self.lab_info['access_point'])):
            print("ap ", ap_name)
            # instantiate controller object
            instantiate_profile_obj = instantiate_profile(controller_data=get_configuration['controller'],
                                                          timeout="10", ssid_data=lf_dut_data,
                                                          ap_data=self.lab_info['access_point'], type=ap_name)
            if ap_name == 0:
                for band in range(len(lf_dut_data)):
                    if lf_dut_data[band]["appliedRadios"] == ["2G"]:
                        instantiate_profile_obj.no_logging_console()
                        instantiate_profile_obj.line_console()
                        id_slot = instantiate_profile_obj.get_slot_id_wlan()
                        ssid_name = instantiate_profile_obj.get_ssid_name_on_id()
                        if id_slot[0] == "1":
                            instantiate_profile_obj.show_shutdown_2ghz_ap()
                            instantiate_profile_obj.disable_wlan(wlan=ssid_name[0])
                            instantiate_profile_obj.ap_2ghz_shutdown()
                            instantiate_profile_obj.get_ssids()
                            instantiate_profile_obj.delete_wlan(ssid=ssid_name[0])
                            instantiate_profile_obj.get_ssids()
                            instantiate_profile_obj.create_wlan_wpa2(id="1", wlan=lf_dut_data[0]['ssid_name'],
                                                                     wlanssid=lf_dut_data[0]['ssid_name'],
                                                                     key=lf_dut_data[0]['security_key'])
                        else:
                            print(lf_dut_data[0]['ssid_name'])
                            instantiate_profile_obj.get_ssids()
                            instantiate_profile_obj.show_shutdown_2ghz_ap()
                            instantiate_profile_obj.get_ssids()
                            instantiate_profile_obj.create_wlan_wpa2(id="1", wlan=lf_dut_data[0]['ssid_name'],
                                                                     wlanssid=lf_dut_data[0]['ssid_name'],
                                                                     key=lf_dut_data[0]['security_key'])
                            instantiate_profile_obj.get_ssids()

                        if "roam_type" not in list_key:
                            # add wlan to single ap
                            instantiate_profile_obj.config_wireless_tag_policy_and_policy_profile(wlan=lf_dut_data[0]['ssid_name'])
                        instantiate_profile_obj.enable_wlan( wlan=lf_dut_data[0]['ssid_name'])
                        instantiate_profile_obj.enable_2ghz_netwrk(id="1", wlan=lf_dut_data[0]['ssid_name'],
                                                                   wlanssid=lf_dut_data[0]['ssid_name'],
                                                                   key=lf_dut_data[0]['security_key'])
                        instantiate_profile_obj.enable_ap_2ghz()
                        if parameter["ft+psk"] == True:
                            instantiate_profile_obj.enable_ft_psk(ssid=lf_dut_data[0]['ssid_name'], key=lf_dut_data[0]['security_key'])
                        if 'dtim' in list_key:
                            instantiate_profile_obj.set_dtim_2ghz(wlan=lf_dut_data[0]['ssid_name'], value=parameter["dtim"])
                        instantiate_profile_obj.get_ssids()

                    if lf_dut_data[band]["appliedRadios"] == ["5G"]:
                        instantiate_profile_obj.no_logging_console()
                        instantiate_profile_obj.line_console()
                        id_slot = instantiate_profile_obj.get_slot_id_wlan()
                        print(id_slot)
                        ssid_name = instantiate_profile_obj.get_ssid_name_on_id()
                        print(ssid_name)
                        if id_slot[1] == "2":
                            # if ssid present on slot 2 delete it and create new
                            instantiate_profile_obj.show_shutdown_5ghz_ap()
                            instantiate_profile_obj.disable_wlan(wlan=ssid_name[1])
                            instantiate_profile_obj.ap_5ghz_shutdown()
                            instantiate_profile_obj.get_ssids()
                            instantiate_profile_obj.delete_wlan(ssid=ssid_name[1])
                            instantiate_profile_obj.get_ssids()
                            instantiate_profile_obj.create_wlan_wpa2(id="2", wlan=lf_dut_data[1]['ssid_name'],
                                                                     wlanssid=lf_dut_data[1]['ssid_name'],
                                                                     key=lf_dut_data[1]['security_key'])
                        else:
                            print(lf_dut_data[1]['ssid_name'])
                            instantiate_profile_obj.get_ssids()
                            instantiate_profile_obj.show_shutdown_5ghz_ap()
                            instantiate_profile_obj.get_ssids()
                            instantiate_profile_obj.create_wlan_wpa2(id="2", wlan=lf_dut_data[1]['ssid_name'],
                                                                     wlanssid=lf_dut_data[1]['ssid_name'],
                                                                     key=lf_dut_data[1]['security_key'])
                            instantiate_profile_obj.get_ssids()

                        if "roam_type" not in list_key:
                            instantiate_profile_obj.config_wireless_tag_policy_and_policy_profile(wlan=lf_dut_data[1]['ssid_name'])
                        instantiate_profile_obj.enable_wlan(wlan=lf_dut_data[1]['ssid_name'])
                        instantiate_profile_obj.enable_5ghz_netwrk(id="2", wlan=lf_dut_data[1]['ssid_name'],
                                                                   wlanssid=lf_dut_data[1]['ssid_name'],
                                                                   key=lf_dut_data[1]['security_key'])
                        instantiate_profile_obj.enable_ap_5ghz()
                        if parameter["ft+psk"] == True:
                            instantiate_profile_obj.enable_ft_psk(ssid=lf_dut_data[1]['ssid_name'], key=lf_dut_data[1]['security_key'])
                        if 'dtim' in list_key:
                            instantiate_profile_obj.set_dtim_5ghz(wlan=lf_dut_data[1]['ssid_name'], value=parameter["dtim"])

                        instantiate_profile_obj.get_ssids()
                    if lf_dut_data[band]["appliedRadios"] == ["6G"]:
                        instantiate_profile_obj.no_logging_console()
                        instantiate_profile_obj.line_console()
                        id_slot = instantiate_profile_obj.get_slot_id_wlan()
                        print(id_slot)
                        ssid_name = instantiate_profile_obj.get_ssid_name_on_id()
                        print(ssid_name)
                        if id_slot[2] == "3":
                            instantiate_profile_obj.show_shutdown_6ghz_ap()
                            # instantiate_profile_obj.show_shutdown_5ghz_ap()
                            # instantiate_profile_obj.show_shutdown_2ghz_ap()
                            instantiate_profile_obj.disable_wlan(wlan=ssid_name[2])
                            instantiate_profile_obj.ap_6ghz_shutdown()
                            instantiate_profile_obj.get_ssids()
                            instantiate_profile_obj.delete_wlan(ssid=ssid_name[2])
                            instantiate_profile_obj.get_ssids()
                            instantiate_profile_obj.create_wlan_wpa3(id="3", wlan=lf_dut_data[2]['ssid_name'],
                                                                              wlanssid=lf_dut_data[2]['ssid_name'],
                                                                              key=lf_dut_data[2]['security_key'])
                        else:
                            instantiate_profile_obj.get_ssids()
                            instantiate_profile_obj.show_shutdown_6ghz_ap()
                            instantiate_profile_obj.get_ssids()
                            instantiate_profile_obj.create_wlan_wpa3(id="3", wlan=lf_dut_data[2]['ssid_name'],
                                                                     wlanssid=lf_dut_data[2]['ssid_name'],
                                                                     key=lf_dut_data[2]['security_key'])
                            instantiate_profile_obj.get_ssids()

                        if "roam_type" not in list_key:
                            instantiate_profile_obj.config_wireless_tag_policy_and_policy_profile(
                                wlan=lf_dut_data[2]['ssid_name'])
                        instantiate_profile_obj.enable_wlan( wlan=lf_dut_data[2]['ssid_name'])
                        instantiate_profile_obj.enable_6ghz_netwrk(id="3", wlan=lf_dut_data[2]['ssid_name'],
                                                                   wlanssid=lf_dut_data[2]['ssid_name'],
                                                                   key=lf_dut_data[2]['security_key'])
                        instantiate_profile_obj.enable_ap_6ghz()
                        # if parameter["ft+psk"] == True:
                        #      instantiate_profile_obj.enable_ft_sae(ssid=lf_dut_data[2]['ssid_name'], key=lf_dut_data[2]['security_key'])
                        instantiate_profile_obj.get_ssids()

        if "roam_type" in list_key:
            print("after creating wlan's assign wlan to respective tag policy")
            for ap_name in range(len(self.lab_info['access_point'])):
                print("ap ", ap_name)
                instantiate_profile_obj = instantiate_profile(controller_data=get_configuration['controller'], timeout="10",
                                                              ssid_data=lf_dut_data, ap_data=self.lab_info['access_point'],
                                                              type=ap_name)
                if parameter["roam_type"] == "fiveg_to_fiveg":
                    # add 5g wlan to both ap's
                    instantiate_profile_obj.config_wireless_tag_policy_and_policy_profile(wlan=lf_dut_data[1]['ssid_name'])
                if parameter["roam_type"] == "fiveg_to_sixg":
                    if ap_name == 0:
                        # add 5g ssid to 5g ap
                        instantiate_profile_obj.config_wireless_tag_policy_and_policy_profile(wlan=lf_dut_data[1]['ssid_name'])
                    if ap_name == 1:
                        # add 6g ssid to 6g ap
                        instantiate_profile_obj.config_wireless_tag_policy_and_policy_profile(wlan=lf_dut_data[2]['ssid_name'])
                else:
                    instantiate_profile_obj.config_wireless_tag_policy_and_policy_profile(
                        wlan=lf_dut_data[0]['ssid_name'])
                    instantiate_profile_obj.config_wireless_tag_policy_and_policy_profile(
                        wlan=lf_dut_data[1]['ssid_name'])
                    instantiate_profile_obj.config_wireless_tag_policy_and_policy_profile(
                        wlan=lf_dut_data[2]['ssid_name'])


        bssid_list_2g = []
        bssid_list_5g = []
        ssid_data_list = []

        for ap_name in range(len(self.lab_info['access_point'])):
            print("ap ", ap_name)
            # instantiate controller object
            instantiate_profile_obj = instantiate_profile(controller_data=get_configuration['controller'], timeout="10",
                                                      ssid_data=lf_dut_data, ap_data=self.lab_info['access_point'], type=ap_name)
            bssid_2g = instantiate_profile_obj.cal_bssid_2g()
            print("bssid 2g", bssid_2g)
            lst_2g = bssid_list_2g.append(bssid_2g)

            bssid_5g = instantiate_profile_obj.cal_bssid_5g()
            print("bssid 5g ", bssid_5g)
            lst_5g = bssid_list_5g.append(bssid_5g)
            # print(bssid_5g)
            # print(bssid_list_2g)
            # print(bssid_list_5g)
            ssid_data = []
            try:
                idx_mapping = {}
                bssid = ""
                for interface in range(len(lf_dut_data)):
                    if interface == 0:
                        bssid = bssid_2g
                    if interface == 1:
                        bssid = bssid_5g
                    if lf_dut_data[interface]['security'] == "psk2":
                        lf_dut_data[interface]['security'] = "WPA2"
                    ssid = ["ssid_idx=" + str(interface) +
                            " ssid=" + lf_dut_data[interface]['ssid_name'] +
                            " security=" + lf_dut_data[interface]['security'] +
                            " password=" + lf_dut_data[interface]['security_key'] +
                            " bssid=" + bssid
                            ]
                    ssid_data.append(ssid)

            except Exception as e:
                print(e)
                pass
            # print("nikita",ssid_data)
            ssid_data_list.append(ssid_data)
        print("final ssid data", ssid_data_list)
        # ssid_data = [[['ssid_idx=0 ssid=ssid_wpa2_2g security=WPA2 password=something bssid=68:7d:b4:5f:5c:30'],
        #               ['ssid_idx=1 ssid=ssid_wpa2_5g security=WPA2 password=something bssid=68:7d:b4:5f:5c:3e']],
        #              [['ssid_idx=0 ssid=ssid_wpa2_2g security=WPA2 password=something bssid=14:16:9d:53:58:c0'],
        #               ['ssid_idx=1 ssid=ssid_wpa2_5g security=WPA2 password=something bssid=14:16:9d:53:58:ce']]]
        lf_tools.create_non_meh_dut(ssid_data=ssid_data_list)








