import sys
import os
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
from controller.controller_1x.controller import Controller
from controller.controller_1x.controller import FirmwareUtility
import pytest
from cv_test_manager import cv_test
from configuration import CONFIGURATION
from configuration import RADIUS_SERVER_DATA
from configuration import RADIUS_ACCOUNTING_DATA
from testrails.testrail_api import APIClient
from testrails.reporting import Reporting
from lf_tools import ChamberView
from sta_connect2 import StaConnect2
from os import path
from typing import Any, Callable, Optional

import time
import allure
import pytest

class Fixtures_1x:

    def __init__(self, configuration={}):
        self.lab_info = configuration
        print(self.lab_info)
        print("1.X")
        try:
            self.controller_obj = Controller(controller_data=self.lab_info["controller"])
        except Exception as e:
            print(e)
            allure.attach(body=str(e), name="Controller Instantiation Failed: ")
            sdk_client = False
            pytest.exit("unable to communicate to Controller" + str(e))

    def disconnect(self):
        self.controller_obj.disconnect_Controller()

    def setup_firmware(self):
        pass

    def get_sdk_version(self):
        version = self.controller_obj.get_sdk_version()
        return version

    def get_ap_cloud_connectivity_status(self, get_configuration, get_apnos):
        mgr_status = []
        for access_point_info in get_configuration['access_point']:
            ap_ssh = get_apnos(access_point_info, sdk="1.x")
            status = ap_ssh.get_manager_state()
            if "ACTIVE" not in status:
                time.sleep(30)
                ap_ssh = APNOS(access_point_info)
                status = ap_ssh.get_manager_state()
            mgr_status.append(status)
        return mgr_status

    def get_ap_version(self, get_apnos, get_configuration):
#         version_list = []
#         for access_point_info in get_configuration['access_point']:
#             ap_ssh = get_apnos(access_point_info)
#             version = ap_ssh.get_ap_version_ucentral()
#             version_list.append(version)
        return ["-\n-"]

    def setup_profiles(self, request, param, setup_controller, testbed, get_equipment_ref, instantiate_profile,
                     get_markers, create_lanforge_chamberview_dut, lf_tools,
                     get_security_flags, get_configuration, radius_info, get_apnos, radius_accounting_info, skip_lf=False):

        instantiate_profile = instantiate_profile(sdk_client=setup_controller)
        vlan_id, mode = 0, 0
        instantiate_profile.cleanup_objects()
        parameter = dict(param)
        print(parameter)
        test_cases = {}
        profile_data = {}
        if parameter['mode'] not in ["BRIDGE", "NAT", "VLAN"]:
            print("Invalid Mode: ", parameter['mode'])
            allure.attach(body=parameter['mode'], name="Invalid Mode: ")
            return test_cases

        if parameter['mode'] == "NAT":
            mode = "NAT"
            vlan_id = 1
        if parameter['mode'] == "BRIDGE":
            mode = "BRIDGE"
            vlan_id = 1
        if parameter['mode'] == "VLAN":
            mode = "BRIDGE"

        instantiate_profile.delete_profile_by_name(profile_name=testbed + "-Equipment-AP-" + parameter['mode'])

        profile_data["equipment_ap"] = {"profile_name": testbed + "-Equipment-AP-" + parameter['mode']}
        profile_data["ssid"] = {}
        for i in parameter["ssid_modes"]:
            profile_data["ssid"][i] = []
            for j in range(len(parameter["ssid_modes"][i])):
                profile_name = testbed + "-SSID-" + i + "-" + str(j) + "-" + parameter['mode']
                data = parameter["ssid_modes"][i][j]
                data["profile_name"] = profile_name
                if "mode" not in dict(data).keys():
                    data["mode"] = mode
                if "vlan" not in dict(data).keys():
                    data["vlan"] = vlan_id
                instantiate_profile.delete_profile_by_name(profile_name=profile_name)
                profile_data["ssid"][i].append(data)
        #         print(profile_name)
        # print(profile_data)

        instantiate_profile.delete_profile_by_name(profile_name=testbed + "-Automation-Radius-Profile-" + mode)
        time.sleep(10)
        """
          Setting up rf profile
        """
        rf_profile_data = {
            "name": "RF-Profile-" + testbed + "-" + parameter['mode'] + "-" +
                    get_configuration['access_point'][0]['mode']
        }

        for i in parameter["rf"]:
            rf_profile_data[i] = parameter['rf'][i]
        # print(rf_profile_data)

        try:
            instantiate_profile.delete_profile_by_name(profile_name=rf_profile_data['name'])
            instantiate_profile.set_rf_profile(profile_data=rf_profile_data,
                                               mode=get_configuration['access_point'][0]['mode'])
            allure.attach(body=str(rf_profile_data),
                          name="RF Profile Created : " + get_configuration['access_point'][0]['mode'])
        except Exception as e:
            print(e)
            allure.attach(body=str(e), name="Exception ")

        # Radius Profile Creation
        if parameter["radius"]:
            radius_info = radius_info
            radius_info["name"] = testbed + "-Automation-Radius-Profile-" + mode
            instantiate_profile.delete_profile_by_name(profile_name=testbed + "-Automation-Radius-Profile-" + mode)
            try:
                instantiate_profile.create_radius_profile(radius_info=radius_info)
                allure.attach(body=str(radius_info),
                              name="Radius Profile Created")
                test_cases['radius_profile'] = True
            except Exception as e:
                print(e)
                test_cases['radius_profile'] = False

        # SSID Profile Creation
        lf_dut_data = []
        for mode in profile_data['ssid']:
            if mode == "open":
                for j in profile_data["ssid"][mode]:
                    # print(j)
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            for i in range(len(j["appliedRadios"])):
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GU", "is5GHzU")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GL", "is5GHzL")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5G", "is5GHz")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("2G", "is2dot4GHz")
                            creates_profile = instantiate_profile.create_open_ssid_profile(profile_data=j)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["open_2g"] = True
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["open_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                        except Exception as e:
                            print(e)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["open_2g"] = False
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["open_5g"] = False
                            allure.attach(body=str(e),
                                          name="SSID Profile Creation Failed")

            if mode == "wpa":
                for j in profile_data["ssid"][mode]:
                    # print(j)
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            for i in range(len(j["appliedRadios"])):
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GU", "is5GHzU")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GL", "is5GHzL")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5G", "is5GHz")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("2G", "is2dot4GHz")
                            creates_profile = instantiate_profile.create_wpa_ssid_profile(profile_data=j)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa_2g"] = True
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                        except Exception as e:
                            print(e)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa_2g"] = False
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa_5g"] = False
                            allure.attach(body=str(e),
                                          name="SSID Profile Creation Failed")

            if mode == "wpa2_personal":
                for j in profile_data["ssid"][mode]:
                    # print(j)

                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            for i in range(len(j["appliedRadios"])):
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GU", "is5GHzU")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GL", "is5GHzL")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5G", "is5GHz")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("2G", "is2dot4GHz")
                            creates_profile = instantiate_profile.create_wpa2_personal_ssid_profile(profile_data=j)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa2_personal_2g"] = True
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa2_personal_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                        except Exception as e:
                            print(e)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa2_personal_2g"] = False
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa2_personal_5g"] = False
                            allure.attach(body=str(e),
                                          name="SSID Profile Creation Failed")

            if mode == "wpa_wpa2_personal_mixed":
                for j in profile_data["ssid"][mode]:
                    # print(j)
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            for i in range(len(j["appliedRadios"])):
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GU", "is5GHzU")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GL", "is5GHzL")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5G", "is5GHz")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("2G", "is2dot4GHz")

                            creates_profile = instantiate_profile.create_wpa_wpa2_personal_mixed_ssid_profile(
                                profile_data=j)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa_wpa2_personal_mixed_2g"] = True
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa_wpa2_personal_mixed_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                        except Exception as e:
                            print(e)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa_wpa2_personal_mixed_2g"] = False
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa_wpa2_personal_mixed_5g"] = False
                            allure.attach(body=str(e),
                                          name="SSID Profile Creation Failed")

            if mode == "wpa3_personal":
                for j in profile_data["ssid"][mode]:
                    print(j)
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            for i in range(len(j["appliedRadios"])):
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GU", "is5GHzU")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GL", "is5GHzL")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5G", "is5GHz")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("2G", "is2dot4GHz")

                            creates_profile = instantiate_profile.create_wpa3_personal_ssid_profile(profile_data=j)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa3_personal_2g"] = True
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa3_personal_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                        except Exception as e:
                            print(e)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa3_personal_2g"] = False
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa3_personal_5g"] = False
                            allure.attach(body=str(e),
                                          name="SSID Profile Creation Failed")
            if mode == "wpa3_personal_mixed":
                for j in profile_data["ssid"][mode]:
                    print(j)
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            for i in range(len(j["appliedRadios"])):
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GU", "is5GHzU")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GL", "is5GHzL")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5G", "is5GHz")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("2G", "is2dot4GHz")
                            creates_profile = instantiate_profile.create_wpa3_personal_mixed_ssid_profile(
                                profile_data=j)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa3_personal_mixed_2g"] = True
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa3_personal_mixed_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                        except Exception as e:
                            print(e)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa3_personal_mixed_2g"] = False
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa3_personal_mixed_5g"] = False
                            allure.attach(body=str(e),
                                          name="SSID Profile Creation Failed")

            if mode == "wpa_enterprise":
                for j in profile_data["ssid"][mode]:

                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            for i in range(len(j["appliedRadios"])):
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GU", "is5GHzU")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GL", "is5GHzL")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5G", "is5GHz")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("2G", "is2dot4GHz")
                            creates_profile = instantiate_profile.create_wpa_enterprise_ssid_profile(profile_data=j)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa_enterprise_2g"] = True
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa_enterprise_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")

                        except Exception as e:
                            print(e)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa_enterprise_2g"] = False
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa_enterprise_5g"] = False
                            allure.attach(body=str(e),
                                          name="SSID Profile Creation Failed")
            if mode == "wpa2_enterprise":
                for j in profile_data["ssid"][mode]:
                    # print(j)
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            for i in range(len(j["appliedRadios"])):
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GU", "is5GHzU")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GL", "is5GHzL")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5G", "is5GHz")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("2G", "is2dot4GHz")
                            creates_profile = instantiate_profile.create_wpa2_enterprise_ssid_profile(profile_data=j)

                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa2_enterprise_2g"] = True
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa2_enterprise_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                        except Exception as e:
                            print(e)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa2_enterprise_2g"] = False
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa2_enterprise_5g"] = False
                            allure.attach(body=str(e),
                                          name="SSID Profile Creation Failed")
            if mode == "wpa3_enterprise":
                for j in profile_data["ssid"][mode]:
                    # print(j)
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            for i in range(len(j["appliedRadios"])):
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GU", "is5GHzU")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GL", "is5GHzL")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5G", "is5GHz")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("2G", "is2dot4GHz")
                            creates_profile = instantiate_profile.create_wpa3_enterprise_ssid_profile(profile_data=j)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa3_enterprise_2g"] = True
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa3_enterprise_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                        except Exception as e:
                            print(e)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa3_enterprise_2g"] = False
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa3_enterprise_5g"] = False
                            allure.attach(body=str(e),
                                          name="SSID Profile Creation Failed")

            if mode == "wpa_wpa2_enterprise_mixed":
                for j in profile_data["ssid"][mode]:
                    # print(j)
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            for i in range(len(j["appliedRadios"])):
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GU", "is5GHzU")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GL", "is5GHzL")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5G", "is5GHz")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("2G", "is2dot4GHz")
                            creates_profile = instantiate_profile.create_wpa_wpa2_enterprise_mixed_ssid_profile(
                                profile_data=j)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa_wpa2_enterprise_mixed_2g"] = True
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa_wpa2_enterprise_mixed_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                        except Exception as e:
                            print(e)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa_wpa2_enterprise_mixed_2g"] = False
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa_wpa2_enterprise_mixed_5g"] = False
                            allure.attach(body=str(e),
                                          name="SSID Profile Creation Failed")
            if mode == "wpa3_enterprise_mixed":
                for j in profile_data["ssid"][mode]:
                    # print(j)
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            for i in range(len(j["appliedRadios"])):
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GU", "is5GHzU")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GL", "is5GHzL")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5G", "is5GHz")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("2G", "is2dot4GHz")
                            creates_profile = instantiate_profile.create_wpa3_enterprise_mixed_ssid_profile(
                                profile_data=j)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa3_enterprise_mixed_2g"] = True
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa3_enterprise_mixed_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                        except Exception as e:
                            print(e)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wpa3_enterprise_mixed_2g"] = False
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wpa3_enterprise_mixed_5g"] = False
                            allure.attach(body=str(e),
                                          name="SSID Profile Creation Failed")

            if mode == "wep":
                for j in profile_data["ssid"][mode]:
                    # print(j)
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            for i in range(len(j["appliedRadios"])):
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GU", "is5GHzU")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5GL", "is5GHzL")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("5G", "is5GHz")
                                j["appliedRadios"][i] = j["appliedRadios"][i].replace("2G", "is2dot4GHz")
                            creates_profile = instantiate_profile.create_wep_ssid_profile(profile_data=j)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wep_2g"] = True
                            if j["appliedRadios"].__contains__("is5GHzU"):
                                test_cases["wep_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                        except Exception as e:
                            print(e)
                            if j["appliedRadios"].__contains__("is2dot4GHz"):
                                test_cases["wep_2g"] = False
                            if j["appliedRadios"].__contains__("is5GHz"):
                                test_cases["wep_5g"] = False
                            allure.attach(body=str(e),
                                          name="SSID Profile Creation Failed")
        # Equipment AP Profile Creation
        try:
            instantiate_profile.set_ap_profile(profile_data=profile_data['equipment_ap'])
            test_cases["equipment_ap"] = True
            allure.attach(body=str(profile_data['equipment_ap']),
                          name="Equipment AP Profile Created")
        except Exception as e:
            print(e)
            test_cases["equipment_ap"] = False
            allure.attach(body=str(e),
                          name="Equipment AP Profile Creation Failed")

        # Push the Equipment AP Profile to AP
        try:
            for i in get_equipment_ref:
                instantiate_profile.push_profile_old_method(equipment_id=i)
        except Exception as e:
            print(e)
            print("failed to create AP Profile")

        ap_ssh = get_apnos(get_configuration['access_point'][0], pwd="../libs/apnos/", sdk="1.x")
        # ssid_names = []
        # for i in instantiate_profile.profile_creation_ids["ssid"]:
        #     ssid_names.append(instantiate_profile.get_ssid_name_by_profile_id(profile_id=i))
        # ssid_names.sort()
        ssid_names = []
        for i in lf_dut_data:
            ssid_names.append(i["ssid_name"])
        ssid_names.sort()
        # This loop will check the VIF Config with cloud profile
        vif_config = []
        test_cases['vifc'] = False
        for i in range(0, 18):
            vif_config = list(ap_ssh.get_vif_config_ssids())
            vif_config.sort()
            print(vif_config)
            print(ssid_names)
            if ssid_names == vif_config:
                test_cases['vifc'] = True
                break
            time.sleep(10)
        allure.attach(
            body=str("VIF Config: " + str(vif_config) + "\n" + "SSID Pushed from Controller: " + str(ssid_names)),
            name="SSID Profiles in VIF Config and Controller: ")
        ap_ssh = get_apnos(get_configuration['access_point'][0], pwd="../libs/apnos/", sdk="1.x")

        # This loop will check the VIF Config with VIF State
        test_cases['vifs'] = False
        for i in range(0, 18):
            vif_state = list(ap_ssh.get_vif_state_ssids())
            vif_state.sort()
            vif_config = list(ap_ssh.get_vif_config_ssids())
            vif_config.sort()
            print(vif_config)
            print(vif_state)
            if vif_state == vif_config:
                test_cases['vifs'] = True
                break
            time.sleep(10)
        allure.attach(body=str("VIF Config: " + str(vif_config) + "\n" + "VIF State: " + str(vif_state)),
                      name="SSID Profiles in VIF Config and VIF State: ")

        ap_logs = ap_ssh.logread()
        allure.attach(body=ap_logs, name="AP LOgs: ")
        # ssid_info = ap_ssh.get_ssid_info()
        # ssid_data = []
        # print(ssid_info)
        # band_mapping = ap_ssh.get_bssid_band_mapping()
        # print(band_mapping)
        # idx_mapping = {}
        # for i in range(0, len(ssid_info)):
        #     if ssid_info[i][1] == "OPEN":
        #         ssid_info[i].append("")
        #     if ssid_info[i][1] == "OPEN":
        #         ssid = ["ssid_idx=" + str(i) + " ssid=" + ssid_info[i][3] + " security=OPEN" +
        #                 " password=" + ssid_info[i][2] + " bssid=" + ssid_info[i][0]]
        #         idx_mapping[str(i)] = [ssid_info[i][3], ssid_info[i][2], ssid_info[i][1], band_mapping[ssid_info[i][0]],
        #                                ssid_info[i][0]]
        #
        #     if ssid_info[i][1] == "WPA":
        #         ssid = ["ssid_idx=" + str(i) + " ssid=" + ssid_info[i][3] + " security=WPA" +
        #                 " password=" + ssid_info[i][2] + " bssid=" + ssid_info[i][0]]
        #         idx_mapping[str(i)] = [ssid_info[i][3], ssid_info[i][2], ssid_info[i][1], band_mapping[ssid_info[i][0]],
        #                                ssid_info[i][0]]
        #     if ssid_info[i][1] == "WPA2":
        #         ssid = ["ssid_idx=" + str(i) + " ssid=" + ssid_info[i][3] + " security=WPA2" +
        #                 " password=" + ssid_info[i][2] + " bssid=" + ssid_info[i][0]]
        #         idx_mapping[str(i)] = [ssid_info[i][3], ssid_info[i][2], ssid_info[i][1], band_mapping[ssid_info[i][0]],
        #                                ssid_info[i][0]]
        #     if ssid_info[i][1] == "WPA3_PERSONAL":
        #         ssid = ["ssid_idx=" + str(i) + " ssid=" + ssid_info[i][3] + " security=WPA3" +
        #                 " password=" + ssid_info[i][2] + " bssid=" + ssid_info[i][0]]
        #         idx_mapping[str(i)] = [ssid_info[i][3], ssid_info[i][2], ssid_info[i][1], band_mapping[ssid_info[i][0]],
        #                                ssid_info[i][0]]
        #
        #     if ssid_info[i][1] == "WPA | WPA2":
        #         ssid = ["ssid_idx=" + str(i) + " ssid=" + ssid_info[i][3] + " security=WPA|WPA2" +
        #                 " password=" + ssid_info[i][2] + " bssid=" + ssid_info[i][0]]
        #         idx_mapping[str(i)] = [ssid_info[i][3], ssid_info[i][2], ssid_info[i][1], band_mapping[ssid_info[i][0]],
        #                                ssid_info[i][0]]
        #
        #     if ssid_info[i][1] == "EAP-TTLS":
        #         ssid = ["ssid_idx=" + str(i) + " ssid=" + ssid_info[i][3] + " security=EAP-TTLS" +
        #                 " password=" + ssid_info[i][2] + " bssid=" + ssid_info[i][0]]
        #         idx_mapping[str(i)] = [ssid_info[i][3], ssid_info[i][2], ssid_info[i][1], band_mapping[ssid_info[i][0]],
        #                                ssid_info[i][0]]
        #     ssid_data.append(ssid)
        # lf_tools.dut_idx_mapping = idx_mapping
        # # Add bssid password and security from iwinfo data
        # # Format SSID Data in the below format
        # # ssid_data = [
        # #     ['ssid_idx=0 ssid=Default-SSID-2g security=WPA|WEP| password=12345678 bssid=90:3c:b3:94:48:58'],
        # #     ['ssid_idx=1 ssid=Default-SSID-5gl password=12345678 bssid=90:3c:b3:94:48:59']
        # # ]
        # allure.attach(name="SSID DATA IN LF DUT", body=str(ssid_data))
        # lf_tools.update_ssid(ssid_data=ssid_data)

        def teardown_session():
            print("\nRemoving Profiles")
            instantiate_profile.delete_profile_by_name(profile_name=profile_data['equipment_ap']['profile_name'])
            instantiate_profile.delete_profile(instantiate_profile.profile_creation_ids["ssid"])
            instantiate_profile.delete_profile(instantiate_profile.profile_creation_ids["radius"])
            instantiate_profile.delete_profile(instantiate_profile.profile_creation_ids["rf"])
            allure.attach(body=str(profile_data['equipment_ap']['profile_name'] + "\n"),
                          name="Tear Down in Profiles ")
            time.sleep(20)

        request.addfinalizer(teardown_session)
        return test_cases
