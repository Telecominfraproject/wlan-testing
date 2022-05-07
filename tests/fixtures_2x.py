""" Python Inbuilt Libraries """
import random
import string

import allure
import pytest
import sys
import os
import json
import time

import requests

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
from controller.controller_2x.controller import FMSUtils
from controller.controller_2x.controller import ProvUtils
from configuration import CONFIGURATION
from configuration import RADIUS_SERVER_DATA
from configuration import RADIUS_ACCOUNTING_DATA


class Fixtures_2x:

    def __init__(self, configuration={}, run_lf=False):
        self.lab_info = configuration
        print(self.lab_info)
        print("2.X")
        self.run_lf = run_lf
        self.controller_obj=""
        if not run_lf:
            try:
                self.controller_obj = Controller(controller_data=self.lab_info["controller"])
                self.prov_controller_obj = ProvUtils(controller_data=self.lab_info["controller"])
                self.fw_client = FMSUtils(sdk_client=self.controller_obj)
            except Exception as e:
                print(e)
                allure.attach(body=str(e), name="Controller Instantiation Failed: ")
                sdk_client = False
                pytest.exit("unable to communicate to Controller" + str(e))

    def disconnect(self):
        if not self.run_lf:
            self.controller_obj.logout()

    def setup_firmware(self, get_apnos, get_configuration, request=""):
        # Query AP Firmware
        upgrade_status = []
        for ap in get_configuration['access_point']:

            ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
            # If specified as URL
            try:
                response = requests.get(ap['version'])
                print("URL is valid and exists on the internet")
                allure.attach(name="firmware url: ", body=str(ap['version']))
                target_revision_commit = ap['version'].split("-")[-2]
                ap_version = ap_ssh.get_ap_version_ucentral()
                current_version_commit = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

                # if AP is already in target Version then skip upgrade unless force upgrade is specified
                if target_revision_commit in current_version_commit:
                    continue
                self.fw_client.upgrade_firmware(serial=ap['serial'], url=str(ap['version']))

                items = list(range(0, 300))
                l = len(items)
                ap_version = ap_ssh.get_ap_version_ucentral()
                current_version_commit = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                if target_revision_commit in current_version_commit:
                    upgrade_status.append([ap['serial'], target_revision_commit, current_version_commit])
                    print("Firmware Upgraded to :", ap_version)
                else:
                    print("firmware upgraded failed: ", target_revision)
                    upgrade_status.append([ap['serial'], target_revision_commit, current_version_commit])
                break
            except Exception as e:
                print("URL does not exist on Internet")
            # else Specified as "branch-commit_id" / "branch-latest"
            firmware_url = ""
            ap_version = ap_ssh.get_ap_version_ucentral()
            response = self.fw_client.get_latest_fw(model=ap["model"])
            # if the target version specified is "branch-latest"
            if ap['version'].split('-')[1] == "latest":
                # get the latest branch
                firmware_list = self.fw_client.get_firmwares(model=ap['model'], branch="", commit_id='')
                firmware_list.reverse()

                for firmware in firmware_list:
                    if firmware['image'] == "":
                        continue
                    if str(firmware['image']).__contains__("upgrade.bin"):
                        temp = firmware['image'].split("-")
                        temp.pop(-1)
                        temp = "-".join(temp)
                        firmware['image'] = temp
                    if ap['version'].split('-')[0] == 'release':
                        if firmware['revision'].split("/")[1].replace(" ", "").split('-')[1].__contains__('v2.'):
                            print("Target Firmware: \n", firmware)
                            allure.attach(name="Target firmware : ", body=str(firmware))
                            target_revision = firmware['revision'].split("/")[1].replace(" ", "")

                            # check the current AP Revision before upgrade
                            ap_version = ap_ssh.get_ap_version_ucentral()
                            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

                            # print and report the firmware versions before upgrade
                            allure.attach(name="Before Firmware Upgrade Request: ",
                                          body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                            print("current revision: ", current_version, "\ntarget revision: ", target_revision)

                            # if AP is already in target Version then skip upgrade unless force upgrade is specified
                            if current_version == target_revision:
                                upgrade_status.append([ap['serial'], target_revision, current_version, 'skip'])
                                print("Skipping Upgrade! AP is already in target version")
                                allure.attach(name="Skipping Upgrade because AP is already in the target Version",
                                              body="")
                                break

                            self.fw_client.upgrade_firmware(serial=ap['serial'], url=str(firmware['uri']))
                            # wait for 300 seconds after firmware upgrade
                            print("waiting for 300 Sec for Firmware Upgrade")
                            time.sleep(300)

                            # check the current AP Revision again
                            ap_version = ap_ssh.get_ap_version_ucentral()
                            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                            # print and report the Firmware versions after upgrade
                            allure.attach(name="After Firmware Upgrade Request: ",
                                          body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                            print("current revision: ", current_version, "\ntarget revision: ", target_revision)
                            if current_version == target_revision:
                                upgrade_status.append([ap['serial'], target_revision, current_version])
                                print("firmware upgraded successfully: ", target_revision)
                            else:
                                upgrade_status.append([ap['serial'], target_revision, current_version])
                                print("firmware upgraded failed: ", target_revision)
                            break
                    print("shivam", firmware['image'].split("-"), ap['version'].split('-')[0])
                    if firmware['image'].split("-")[-2] == ap['version'].split('-')[0]:
                        print("Target Firmware: \n", firmware)
                        allure.attach(name="Target firmware : ", body=str(firmware))

                        target_revision = firmware['revision'].split("/")[1].replace(" ", "")

                        # check the current AP Revision before upgrade
                        ap_version = ap_ssh.get_ap_version_ucentral()
                        current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

                        # print and report the firmware versions before upgrade
                        allure.attach(name="Before Firmware Upgrade Request: ",
                                      body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                        print("current revision: ", current_version, "\ntarget revision: ", target_revision)

                        # if AP is already in target Version then skip upgrade unless force upgrade is specified
                        if current_version == target_revision:
                            upgrade_status.append([ap['serial'], target_revision, current_version, 'skip'])
                            print("Skipping Upgrade! AP is already in target version")
                            allure.attach(name="Skipping Upgrade because AP is already in the target Version", body="")
                            break

                        self.fw_client.upgrade_firmware(serial=ap['serial'], url=str(firmware['uri']))
                        # wait for 300 seconds after firmware upgrade
                        print("waiting for 300 Sec for Firmware Upgrade")
                        time.sleep(500)

                        # check the current AP Revision again
                        ap_version = ap_ssh.get_ap_version_ucentral()
                        current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                        # print and report the Firmware versions after upgrade
                        allure.attach(name="After Firmware Upgrade Request: ",
                                      body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                        print("current revision: ", current_version, "\ntarget revision: ", target_revision)
                        if current_version == target_revision:
                            upgrade_status.append([ap['serial'], target_revision, current_version])
                            print("firmware upgraded successfully: ", target_revision)
                        else:
                            upgrade_status.append([ap['serial'], target_revision, current_version])
                            print("firmware upgraded failed: ", target_revision)
                        break
            # if branch-commit is specified
            else:
                firmware_list = self.fw_client.get_firmwares(model=ap['model'], branch="", commit_id='')
                fw_list = []
                # getting the list of firmwares in fw_list that has the commit id specified as an input
                for firmware in firmware_list:
                    if firmware['revision'].split("/")[1].replace(" ", "").split('-')[-1] == ap['version'].split('-')[
                        1]:
                        fw_list.append(firmware)

                # If there is only 1 commit ID in fw_list
                if len(fw_list) == 1:

                    print("Target Firmware: \n", fw_list[0])
                    allure.attach(name="Target firmware : ", body=str(fw_list[0]))

                    url = fw_list[0]['uri']
                    target_revision = fw_list[0]['revision'].split("/")[1].replace(" ", "")

                    # check the current AP Revision before upgrade
                    ap_version = ap_ssh.get_ap_version_ucentral()
                    current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

                    # print and report the firmware versions before upgrade
                    allure.attach(name="Before Firmware Upgrade Request: ",
                                  body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                    print("current revision: ", current_version, "\ntarget revision: ", target_revision)

                    # if AP is already in target Version then skip upgrade unless force upgrade is specified
                    if current_version == target_revision:
                        upgrade_status.append([ap['serial'], target_revision, current_version, 'skip'])
                        print("Skipping Upgrade! AP is already in target version")
                        allure.attach(name="Skipping Upgrade because AP is already in the target Version", body="")
                        break

                    # upgrade the firmware in another condition
                    else:
                        self.fw_client.upgrade_firmware(serial=ap['serial'], url=str(url))

                        # wait for 300 seconds after firmware upgrade
                        print("waiting for 300 Sec for Firmware Upgrade")
                        time.sleep(300)

                        # check the current AP Revision again
                        ap_version = ap_ssh.get_ap_version_ucentral()
                        current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                        # print and report the Firmware versions after upgrade
                        allure.attach(name="After Firmware Upgrade Request: ",
                                      body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                        print("current revision: ", current_version, "\ntarget revision: ", target_revision)
                        if current_version == target_revision:
                            upgrade_status.append([ap['serial'], target_revision, current_version])
                            print("firmware upgraded successfully: ", target_revision)
                        else:
                            upgrade_status.append([ap['serial'], target_revision, current_version])
                            print("firmware upgraded failed: ", target_revision)
                        break

                # if there are 1+ firmware images in fw_list then check for branch
                else:
                    target_fw = ""
                    for firmware in fw_list:
                        if ap['version'].split('-')[0] == 'release':
                            if firmware['revision'].split("/")[1].replace(" ", "").split('-')[1].__contains__('v2.'):
                                target_fw = firmware
                                break
                        if firmware['image'].split("-")[-2] == ap['version'].split('-')[0]:
                            target_fw = firmware
                            break
                    firmware = target_fw
                    print("Target Firmware: \n", firmware)
                    allure.attach(name="Target firmware : ", body=str(firmware))

                    target_revision = firmware['revision'].split("/")[1].replace(" ", "")

                    # check the current AP Revision before upgrade
                    ap_version = ap_ssh.get_ap_version_ucentral()
                    current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

                    # print and report the firmware versions before upgrade
                    allure.attach(name="Before Firmware Upgrade Request: ",
                                  body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                    print("current revision: ", current_version, "\ntarget revision: ", target_revision)

                    # if AP is already in target Version then skip upgrade unless force upgrade is specified
                    if current_version == target_revision:
                        upgrade_status.append([ap['serial'], target_revision, current_version, 'skip'])
                        print("Skipping Upgrade! AP is already in target version")
                        allure.attach(name="Skipping Upgrade because AP is already in the target Version", body="")
                        break

                    self.fw_client.upgrade_firmware(serial=ap['serial'], url=str(firmware['uri']))
                    # wait for 300 seconds after firmware upgrade

                    print("waiting for 300 Sec for Firmware Upgrade")
                    time.sleep(300)

                    # check the current AP Revision again
                    ap_version = ap_ssh.get_ap_version_ucentral()
                    current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                    # print and report the Firmware versions after upgrade
                    allure.attach(name="After Firmware Upgrade Request: ",
                                  body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                    print("current revision: ", current_version, "\ntarget revision: ", target_revision)
                    if current_version == target_revision:
                        upgrade_status.append([target_revision, current_version])
                        print("firmware upgraded successfully: ", target_revision)
                    else:
                        upgrade_status.append([target_revision, current_version])
                        print("firmware upgraded failed: ", target_revision)
                    break
        return upgrade_status

    def get_ap_cloud_connectivity_status(self, get_configuration, get_apnos):
        status_data = []
        self.ubus_connection = []
        for access_point_info in get_configuration['access_point']:
            ap_ssh = get_apnos(access_point_info, sdk="2.x")
            status = ap_ssh.get_ucentral_status()
            print(status)
            status_data.append(status)
            connectivity_data = ap_ssh.run_generic_command(cmd="ubus call ucentral status")
            self.ubus_connection.append(['Serial Number: ' + access_point_info['serial'], connectivity_data])
        return status_data

    def get_ap_version(self, get_apnos, get_configuration):

        version_list = []
        if not self.run_lf:
            for access_point_info in get_configuration['access_point']:
                ap_ssh = get_apnos(access_point_info)
                version = ap_ssh.get_ap_version_ucentral()
                version_list.append(version)
        return version_list

    def get_uci_show(self, get_apnos, get_configuration):
        version_list = []
        for access_point_info in get_configuration['access_point']:
            ap_ssh = get_apnos(access_point_info)
            connectivity_data = ap_ssh.run_generic_command(cmd="uci show ucentral.config.server")
            # connectivity_data.pop(0)
            # connectivity_data.pop(1)
            break
            # version_list.append(connectivity_data)
        return connectivity_data[1]

    def dfs(self, get_apnos, get_configuration):
        for access_point_info in get_configuration['access_point']:
            ap_ssh = get_apnos(access_point_info, sdk="2.x")
        return ap_ssh

    def get_ap_status_logs(self, get_configuration, get_apnos):
        connected = 0
        redirector_data = None
        for access_point_info in get_configuration['access_point']:
            ap_ssh = get_apnos(access_point_info, sdk="2.x")
            # for i in range(15):
            connectivity_data = ap_ssh.run_generic_command(cmd="ubus call ucentral status")
            if "disconnected" in str(connectivity_data):
                print("AP in disconnected state, sleeping for 30 sec")
                # time.sleep(30)
                connected = 0
                # # if i == 10:
                # print("rebooting AP")
                # ap_ssh.reboot()
                # print("sleep for 300 sec")
                # time.sleep(300)
            else:
                connected = 1

            redirector_data = ap_ssh.run_generic_command(cmd="cat /etc/ucentral/redirector.json")
        return connected, redirector_data

    def get_sdk_version(self):
        version = self.controller_obj.get_sdk_version()
        return version

    def setup_profiles(self, request, param, setup_controller, testbed, get_equipment_ref,
                       instantiate_profile, get_markers, create_lanforge_chamberview_dut, lf_tools,
                       get_security_flags, get_configuration, radius_info, get_apnos,
                       radius_accounting_info, skip_lf=False, run_lf=False, open_flow=None):
        if run_lf:
           return 0
        instantiate_profile_obj = instantiate_profile(sdk_client=setup_controller)
        print(1, instantiate_profile_obj.sdk_client)
        vlan_id, mode = 0, 0
        parameter = dict(param)
        print("parameter", parameter)
        test_cases = {}
        profile_data = {}
        var = ""
        if len(parameter['rf']) > 0:
            instantiate_profile_obj.set_radio_config(radio_config=parameter['rf'])
        else:
            instantiate_profile_obj.set_radio_config()
        if parameter['mode'] not in ["BRIDGE", "NAT", "VLAN"]:
            print("Invalid Mode: ", parameter['mode'])
            return test_cases



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
                    if "radius_auth_data" in j:
                        var = True
                    else:
                        var = False
                for j in profile_data["ssid"][mode]:
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            j["appliedRadios"] = list(set(j["appliedRadios"]))
                            j['security'] = 'wpa2'

                            if var :
                                RADIUS_SERVER_DATA = j["radius_auth_data"]
                                RADIUS_ACCOUNTING_DATA = j['radius_acc_data']
                                creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j, radius=True,
                                                                                   radius_auth_data=RADIUS_SERVER_DATA,
                                                                                   radius_accounting_data=RADIUS_ACCOUNTING_DATA)
                                test_cases["wpa_2g"] = True
                            else:
                                RADIUS_SERVER_DATA = radius_info
                                RADIUS_ACCOUNTING_DATA = radius_accounting_info
                                creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j, radius=True,
                                                                                   radius_auth_data=RADIUS_SERVER_DATA,
                                                                                   radius_accounting_data=RADIUS_ACCOUNTING_DATA)
                                test_cases["wpa_2g"] = True
                        except Exception as e:
                            print(e)
                            test_cases["wpa2_personal"] = False
            if mode == "wpa3_enterprise":
                for j in profile_data["ssid"][mode]:
                    if "radius_auth_data" in j:
                        var = True
                    else:
                        var = False
                for j in profile_data["ssid"][mode]:
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            j["appliedRadios"] = list(set(j["appliedRadios"]))
                            j['security'] = 'wpa3'
                            if var :
                                RADIUS_SERVER_DATA = j["radius_auth_data"]
                                RADIUS_ACCOUNTING_DATA = j['radius_acc_data']
                                creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j, radius=True,
                                                                                   radius_auth_data=RADIUS_SERVER_DATA,
                                                                                   radius_accounting_data=RADIUS_ACCOUNTING_DATA)
                                test_cases["wpa_2g"] = True
                            else:
                                RADIUS_SERVER_DATA = radius_info
                                RADIUS_ACCOUNTING_DATA = radius_accounting_info
                                creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j, radius=True,
                                                                                   radius_auth_data=RADIUS_SERVER_DATA,
                                                                                   radius_accounting_data=RADIUS_ACCOUNTING_DATA)
                                test_cases["wpa3_eap"] = True
                        except Exception as e:
                            print(e)
                            test_cases["wpa3_eap"] = False
            if mode == "wpa_enterprise":  # -------WPA Enterprise----------------
                for j in profile_data["ssid"][mode]:
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            j["appliedRadios"] = list(set(j["appliedRadios"]))
                            j['security'] = 'wpa'
                            RADIUS_SERVER_DATA = radius_info
                            RADIUS_ACCOUNTING_DATA = radius_accounting_info
                            creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j, radius=True,
                                                                               radius_auth_data=RADIUS_SERVER_DATA,
                                                                               radius_accounting_data=RADIUS_ACCOUNTING_DATA)
                            test_cases["wpa_eap"] = True
                        except Exception as e:
                            print(e)
                            test_cases["wpa_eap"] = False
            if mode == "wpa_wpa2_enterprise_mixed":  # -------WPA WPA2 Enterprise Mixed----------------
                for j in profile_data["ssid"][mode]:
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            j["appliedRadios"] = list(set(j["appliedRadios"]))
                            j['security'] = "wpa-mixed"
                            RADIUS_SERVER_DATA = radius_info
                            RADIUS_ACCOUNTING_DATA = radius_accounting_info
                            creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j, radius=True,
                                                                               radius_auth_data=RADIUS_SERVER_DATA,
                                                                               radius_accounting_data=RADIUS_ACCOUNTING_DATA)
                            test_cases["wpa_eap"] = True
                        except Exception as e:
                            print(e)
                            test_cases["wpa_eap"] = False
            if mode == "wpa3_enterprise_mixed":  # -------WPA3 Enterprise Mixed----------------
                for j in profile_data["ssid"][mode]:
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            j["appliedRadios"] = list(set(j["appliedRadios"]))
                            j['security'] = "wpa3-mixed"
                            RADIUS_SERVER_DATA = radius_info
                            RADIUS_ACCOUNTING_DATA = radius_accounting_info
                            creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j, radius=True,
                                                                               radius_auth_data=RADIUS_SERVER_DATA,
                                                                               radius_accounting_data=RADIUS_ACCOUNTING_DATA)
                            test_cases["wpa_eap"] = True
                        except Exception as e:
                            print(e)
                            test_cases["wpa_eap"] = False
            if mode == "wpa3_192_enterprise":  # -------WPA3 192 Enterprise Mixed----------------
                for j in profile_data["ssid"][mode]:
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            j["appliedRadios"] = list(set(j["appliedRadios"]))
                            j['security'] = "wpa3-192"
                            RADIUS_SERVER_DATA = radius_info
                            RADIUS_ACCOUNTING_DATA = radius_accounting_info
                            creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j, radius=True,
                                                                               radius_auth_data=RADIUS_SERVER_DATA,
                                                                               radius_accounting_data=RADIUS_ACCOUNTING_DATA)
                            test_cases["wpa_eap"] = True
                        except Exception as e:
                            print(e)
                            test_cases["wpa_eap"] = False
        try:
            if parameter['express-wifi']:
                instantiate_profile_obj.set_express_wifi(open_flow=open_flow)
        except Exception as e:
            pass

        try:
            if parameter['captive_portal']:
                instantiate_profile_obj.set_captive_portal()
                # print(json.loads(str(instantiate_profile_obj.base_profile_config).replace(" ", "").replace("'", '"')))
        except:
            pass

        ap_ssh = get_apnos(get_configuration['access_point'][0], pwd="../libs/apnos/", sdk="2.x")

        # Get ucentral status
        connected, latest, active = ap_ssh.get_ucentral_status()

        if connected == False:
            output = ap_ssh.run_generic_command(cmd="ubus call ucentral status")
            allure.attach(name="ubus call ucentral status: ", body=str(output))
            # pytest.exit("AP is disconnected from UC Gateway")

        connected, latest, active = ap_ssh.get_ucentral_status()
        latest_old = latest

        if latest != active:
            active_cfg = ap_ssh.run_generic_command(cmd="cat /etc/ucentral/ucentral.active")
            allure.attach(name="Active Config: ", body=str(active_cfg))
            active_cfg = ap_ssh.run_generic_command(cmd="cat /etc/ucentral/ucentral.cfg." + str(latest))
            allure.attach(name="Latest Config: ", body=str(active_cfg))
            ap_logs = ap_ssh.logread()
            allure.attach(body=ap_logs, name="FAILURE: AP Logs: ")
            pytest.fail("AP latest and active are different")

        S = 10

        # Add logger command before config push
        instance_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
        ap_ssh.run_generic_command(cmd="logger start testcase: " + instance_name)



        # Adding memory Profile code before applying config
        output = ap_ssh.run_generic_command(cmd="ucode /usr/share/ucentral/sysinfo.uc")
        allure.attach(name="ucode /usr/share/ucentral/sysinfo.uc ", body=str(output))

        time_1 = time.time()

        # Apply config
        instantiate_profile_obj.push_config(serial_number=get_equipment_ref[0])

        print(instantiate_profile_obj.base_profile_config)

        config = json.loads(str(instantiate_profile_obj.base_profile_config).replace(" ", "").replace("'", '"').replace("True", "true"))
        config["uuid"] = 0

        # Attach the config that is sent from API
        allure.attach(name="Config Sent from API: ", body=str(config), attachment_type=allure.attachment_type.JSON)

        ap_config_latest = ap_ssh.get_uc_latest_config()
        try:
            ap_config_latest["uuid"] = 0
        except Exception as e:
            print(e)
            pass
        x = 1

        # Check if ucentral gw has pushed the config into latest
        connected, latest, active = ap_ssh.get_ucentral_status()
        while latest_old == latest:
            time.sleep(5)
            x += 1
            print("old config: ", latest_old)
            print("latest: ", latest)
            connected, latest, active = ap_ssh.get_ucentral_status()
            if x == 5:
                break
        onnected, latest, active = ap_ssh.get_ucentral_status()
        if latest == latest_old:
            latest_cfg = ap_ssh.run_generic_command(cmd="cat /etc/ucentral/ucentral.cfg." + str(latest))
            allure.attach(name="Latest Config Received by AP: ",
                          body=str(latest_cfg),
                          attachment_type=allure.attachment_type.JSON)
            ap_logs = ap_ssh.get_logread(start_ref="start testcase: " + instance_name,
                                         stop_ref="stop testcase: " + instance_name)
            allure.attach(body=ap_logs, name="AP Log: ")
            print("Config from ucentral gw is not sent to AP")
        else:
            print("Config is sent to AP from ucentral gw")

        x = 1
        latest_cfg = ap_ssh.run_generic_command(cmd="cat /etc/ucentral/ucentral.cfg." + str(latest))
        allure.attach(name="Latest Config Received by AP: ",
                      body=str(latest_cfg),
                      attachment_type=allure.attachment_type.JSON)

        while active != latest:
            connected, latest, active = ap_ssh.get_ucentral_status()
            time.sleep(20)
            x += 1
            print("active: ", active)
            print("latest: ", latest)
            if x == 10:
                break

        connected, latest, active = ap_ssh.get_ucentral_status()
        if latest == active:
            print("Config properly Applied on AP")
        else:
            print("Config is not Applied on AP")

        time_2 = time.time()
        time_interval = time_2 - time_1
        allure.attach(name="Time Took to apply Config: " + str(time_interval), body="")

        time.sleep(60)

        ap_config_latest = ap_ssh.get_uc_latest_config()
        ap_config_active = ap_ssh.get_uc_active_config()
        if x < 19:
            print("AP is Broadcasting Applied Config")
            allure.attach(name="Success : Active Config in AP: ", body=str(ap_config_active))

        else:
            print("AP is Not Broadcasting Applied Config")
            allure.attach(name="Failed to Apply Config : Active Config in AP : ", body=str(ap_config_active))
        time.sleep(50)
        try:
            iwinfo = ap_ssh.iwinfo()
            allure.attach(name="iwinfo: ", body=str(iwinfo))
        except:
            pass
        ap_ssh.run_generic_command(cmd="logger stop testcase: " + instance_name)
        ap_logs = ap_ssh.get_logread(start_ref="start testcase: " + instance_name,
                                     stop_ref="stop testcase: " + instance_name)
        allure.attach(body=ap_logs, name="AP Log: ")

        wifi_status = ap_ssh.get_wifi_status()
        allure.attach(name="wifi status", body=str(wifi_status))

        try:
            ssid_info_sdk = instantiate_profile_obj.get_ssid_info()

            ap_wifi_data = ap_ssh.get_iwinfo()

            for p in ap_wifi_data:
                for q in ssid_info_sdk:
                    if ap_wifi_data[p][0] == q[0] and ap_wifi_data[p][2] == q[3]:
                        q.append(ap_wifi_data[p][1])

            ssid_data = []
            idx_mapping = {}
            print(ssid_info_sdk)
            for interface in range(len(ssid_info_sdk)):
                ssid = ["ssid_idx=" + str(interface) +
                        " ssid=" + ssid_info_sdk[interface][0] +
                        " security=" + ssid_info_sdk[interface][1].upper() +
                        " password=" + ssid_info_sdk[interface][2] +
                        " bssid=" + ssid_info_sdk[interface][4].lower()
                        ]
                idx_mapping[str(interface)] = [ssid_info_sdk[interface][0],
                                               ssid_info_sdk[interface][2],
                                               ssid_info_sdk[interface][1],
                                               ssid_info_sdk[interface][3],
                                               ssid_info_sdk[interface][4].lower()
                                               ]
                ssid_data.append(ssid)
                lf_tools.ssid_list.append(ssid_info_sdk[interface][0])
            if not skip_lf:
                lf_tools.dut_idx_mapping = idx_mapping
                lf_tools.update_ssid(ssid_data=ssid_data)
        except Exception as e:
            print(e)
            pass

        # Adding memory Profile code after applying config
        output = ap_ssh.run_generic_command(cmd="ucode /usr/share/ucentral/sysinfo.uc")
        allure.attach(name="ucode /usr/share/ucentral/sysinfo.uc ", body=str(output))

        def teardown_session():
            wifi_status = ap_ssh.get_wifi_status()
            allure.attach(name="wifi status", body=str(wifi_status))

            iwinfo = ap_ssh.iwinfo()
            allure.attach(name="iwinfo: ", body=str(iwinfo))

            print("\nTeardown")

        request.addfinalizer(teardown_session)
        return test_cases

    def setup_mesh_profile(self, request, param, get_apnos, get_configuration, setup_controller, instantiate_profile,
                           get_markers, get_equipment_ref, lf_tools, skip_lf=False, open_flow=None):

        instantiate_profile_obj = instantiate_profile(sdk_client=setup_controller)
        print(1, instantiate_profile_obj.sdk_client)
        vlan_id, mode = 0, 0
        parameter = dict(param)
        print("parameter", parameter)
        print(list(parameter["ssid_modes"])[0])
        ssid_info_sdk = instantiate_profile_obj.get_ssid_info()
        print(ssid_info_sdk)
        test_cases = {}
        profile_data = {}
        var = ""
        if parameter['mode'] not in ["BRIDGE", "NAT", "VLAN"]:
            print("Invalid Mode: ", parameter['mode'])
            return test_cases
        instantiate_profile_obj.set_radio_config()
        if parameter['mode'] == "NAT":
            mode = "NAT"
            instantiate_profile_obj.set_mode(mode=mode, mesh=True)
            vlan_id = 1
        if parameter['mode'] == "BRIDGE":
            mode = "BRIDGE"
            instantiate_profile_obj.set_mode(mode=mode, mesh=True)
            vlan_id = 1
        if parameter['mode'] == "VLAN":
            mode = "VLAN"
            instantiate_profile_obj.set_mode(mode=mode, mesh=True)

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

        try:
            if parameter['mesh']:
                print("yes")
                instantiate_profile_obj.set_mesh_services()
        except Exception as e:
            pass


        dut_data = []
        ssid_data = []
        # this will return configuration of your testbed from tests/conftest.py get_configuration fixtures
        print("get configuration", get_configuration)
        print(len(get_configuration['access_point']))
        print(get_configuration['access_point'])
        for length in range(0, len(get_configuration['access_point'])):
            ap_ssh = get_apnos(credentials=get_configuration['access_point'][length], pwd="../libs/apnos/", sdk="2.x")
            connected, latest, active = ap_ssh.get_ucentral_status()
            print("connected", connected)
            print("latest", latest)
            print("active", active)
            latest_old = latest
            if connected == False:
                output = ap_ssh.run_generic_command(cmd="ubus call ucentral status")
                allure.attach(name="ubus call ucentral status: ", body=str(output))
                pytest.exit("AP is disconnected from UC Gateway")

            if latest != active:
                allure.attach(name="FAIL : ubus call ucentral status: ",
                              body="connected: " + str(connected) + "\nlatest: " + str(latest) + "\nactive: " + str(
                                  active))
                ap_logs = ap_ssh.logread()
                allure.attach(body=ap_logs, name="FAILURE: AP LOgs: ")
                pytest.fail("AP is disconnected from UC Gateway")

            S = 10

            # Add logger command before config push
            instance_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
            ap_ssh.run_generic_command(cmd="logger start testcase: " + instance_name)

            time_1 = time.time()

            # Apply config
            print("get equipment id ref ", get_equipment_ref)
            print("get equipment id ref [0]", get_equipment_ref[length])
            instantiate_profile_obj.push_config(serial_number=get_equipment_ref[length])

            config = json.loads(str(instantiate_profile_obj.base_profile_config).replace(" ", "").replace("'", '"'))
            config["uuid"] = 0

            # Attach the config that is sent from API
            allure.attach(name="Config Sent from API: ", body=str(config), attachment_type=allure.attachment_type.JSON)

            ap_config_latest = ap_ssh.get_uc_latest_config()
            try:
                ap_config_latest["uuid"] = 0
            except Exception as e:
                print(e)
                pass
            x = 1

            # Check if ucentral gw has pushed the config into latest
            connected, latest, active = ap_ssh.get_ucentral_status()
            while latest_old == latest:
                time.sleep(5)
                x += 1
                print("old config: ", latest_old)
                print("latest: ", latest)
                connected, latest, active = ap_ssh.get_ucentral_status()
                if x == 5:
                    break
            onnected, latest, active = ap_ssh.get_ucentral_status()
            if latest == latest_old:
                latest_cfg = ap_ssh.run_generic_command(cmd="cat /etc/ucentral/ucentral.cfg." + str(latest))
                allure.attach(name="Latest Config Received by AP: ",
                              body=str(latest_cfg),
                              attachment_type=allure.attachment_type.JSON)
                ap_logs = ap_ssh.get_logread(start_ref="start testcase: " + instance_name,
                                             stop_ref="stop testcase: " + instance_name)
                allure.attach(body=ap_logs, name="AP Log: ")
                print("Config from ucentral gw is not sent to AP")
            else:
                print("Config is sent to AP from ucentral gw")

            x = 1
            latest_cfg = ap_ssh.run_generic_command(cmd="cat /etc/ucentral/ucentral.cfg." + str(latest))
            allure.attach(name="Latest Config Received by AP: ",
                          body=str(latest_cfg),
                          attachment_type=allure.attachment_type.JSON)

            while active != latest:
                connected, latest, active = ap_ssh.get_ucentral_status()
                time.sleep(20)
                x += 1
                print("active: ", active)
                print("latest: ", latest)
                if x == 10:
                    break

            connected, latest, active = ap_ssh.get_ucentral_status()
            if latest == active:
                print("Config properly Applied on AP")
            else:
                print("Config is not Applied on AP")

            time_2 = time.time()
            time_interval = time_2 - time_1
            allure.attach(name="Time Took to apply Config: " + str(time_interval), body="")

            time.sleep(60)

            ap_config_latest = ap_ssh.get_uc_latest_config()
            ap_config_active = ap_ssh.get_uc_active_config()
            if x < 19:
                print("AP is Broadcasting Applied Config")
                allure.attach(name="Success : Active Config in AP: ", body=str(ap_config_active))

            else:
                print("AP is Not Broadcasting Applied Config")
                allure.attach(name="Failed to Apply Config : Active Config in AP : ", body=str(ap_config_active))
            time.sleep(10)

            try:
                iwinfo = ap_ssh.iwinfo()
                allure.attach(name="iwinfo: ", body=str(iwinfo))
            except:
                pass
            ap_ssh.run_generic_command(cmd="logger stop testcase: " + instance_name)
            ap_logs = ap_ssh.get_logread(start_ref="start testcase: " + instance_name,
                                         stop_ref="stop testcase: " + instance_name)
            allure.attach(body=ap_logs, name="AP Log: ")

            wifi_status = ap_ssh.get_wifi_status()
            allure.attach(name="wifi status", body=str(wifi_status))

            try:
                ssid_info_sdk = instantiate_profile_obj.get_ssid_info()
                print("ssid_info_sdk", ssid_info_sdk)
                ap_wifi_data = ap_ssh.get_iwinfo()
                print("ap_wifi_data", ap_wifi_data)
                print(type(ap_wifi_data))

                for p in ap_wifi_data:
                    print(p)
                    for q in ssid_info_sdk:
                        if ap_wifi_data[p][0] == q[0] and ap_wifi_data[p][2] == q[3]:
                            q.append(ap_wifi_data[p][1])


                idx_mapping = {}
                print(ssid_info_sdk)
                dut_data.append(ssid_info_sdk)

            except Exception as e:
                print(e)
                pass
        print("ssid_data", ssid_data)
        print("dut", dut_data)
        dut_ssid_data = []
        dut_final_data = []
        dut_1 = []
        dut_2 = []
        dut_3 = []
        for dut in range(len(dut_data)):
            for interface in range(len(dut_data[dut])):
                ssid = ["ssid_idx=" + str(interface) +
                        " ssid=" + dut_data[dut][interface][0] +
                        " security=" + dut_data[dut][interface][1].upper() +
                        " password=" + dut_data[dut][interface][2] +
                        " bssid=" + dut_data[dut][interface][4].lower()
                        ]
                #print(ssid)
                dut_ssid_data.append(ssid)
        # print("dut ssid data", dut_ssid_data)
        dut_1.append(dut_ssid_data[0])
        dut_1.append(dut_ssid_data[1])
        dut_2.append(dut_ssid_data[2])
        dut_2.append(dut_ssid_data[3])
        dut_3.append(dut_ssid_data[4])
        dut_3.append(dut_ssid_data[5])
        dut_final_data.append(dut_1)
        dut_final_data.append(dut_2)
        dut_final_data.append(dut_3)
        print("dut_final_data", dut_final_data)
        # dut_final_data = [[['ssid_idx=0 ssid=ssid_wpa2_2g security=WPA2 password=something bssid=34:ef:b6:af:4a:84'], ['ssid_idx=1 ssid=ssid_wpa2_5g security=WPA2 password=something bssid=34:ef:b6:af:4a:7c']], [['ssid_idx=0 ssid=ssid_wpa2_2g security=WPA2 password=something bssid=34:ef:b6:af:49:0d'], ['ssid_idx=1 ssid=ssid_wpa2_5g security=WPA2 password=something bssid=34:ef:b6:af:49:05']], [['ssid_idx=0 ssid=ssid_wpa2_2g security=WPA2 password=something bssid=90:3c:b3:9d:69:36'], ['ssid_idx=1 ssid=ssid_wpa2_5g security=WPA2 password=something bssid=90:3c:b3:9d:69:2e']]]

        # dut creation for mesh
        # dut_ssid_data =  [[['ssid_idx=0 ssid=ssid_wpa2_2g security=WPA2 password=something bssid=34:ef:b6:af:4a:84'], ['ssid_idx=1 ssid=ssid_wpa2_5g security=WPA2 password=something bssid=34:ef:b6:af:4a:7c']], [['ssid_idx=0 ssid=ssid_wpa2_2g security=WPA2 password=something bssid=34:ef:b6:af:49:0d'], ['ssid_idx=1 ssid=ssid_wpa2_5g security=WPA2 password=something bssid=34:ef:b6:af:49:05']], [['ssid_idx=0 ssid=ssid_wpa2_2g security=WPA2 password=something bssid=90:3c:b3:9d:69:36'], ['ssid_idx=1 ssid=ssid_wpa2_5g security=WPA2 password=something bssid=90:3c:b3:9d:69:2e']]]
        create_dut = lf_tools.create_mesh_dut(ssid_data=dut_final_data)

        #create mesh scenario
        mesh_scenario = lf_tools.create_mesh_scenario()

        #check for all ap are connected and is pinging
        for length in range(0, len(get_configuration['access_point'])):
            ap_ssh = get_apnos(credentials=get_configuration['access_point'][length], pwd="../libs/apnos/", sdk="2.x")
            print("checking again if all ap's are connected and able to reach internet")
            connected, latest, active = ap_ssh.get_ucentral_status()
            print("connected", connected)
            print("latest", latest)
            print("active", active)
            latest_old = latest
            if connected == False:
                output = ap_ssh.run_generic_command(cmd="ubus call ucentral status")
                allure.attach(name="ubus call ucentral status: ", body=str(output))
                pytest.exit("AP is disconnected from UC Gateway")
            if latest != active:
                allure.attach(name="FAIL : ubus call ucentral status: ",
                              body="connected: " + str(connected) + "\nlatest: " + str(latest) + "\nactive: " + str(active))
                ap_logs = ap_ssh.logread()
                allure.attach(body=ap_logs, name="FAILURE: AP LOgs: ")
                pytest.fail("AP is disconnected from UC Gateway")


        #create a mesh scenario with dhcp disable option to node-1 and node-2
        dhcp_dis = lf_tools.create_mesh_scenario_dhcp_disable()






