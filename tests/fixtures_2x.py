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
            self.fw_client = FMSUtils(sdk_client=self.controller_obj)
        except Exception as e:
            print(e)
            allure.attach(body=str(e), name="Controller Instantiation Failed: ")
            sdk_client = False
            pytest.exit("unable to communicate to Controller" + str(e))

    def disconnect(self):
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
                    upgrade_status.append([ap['serial'],target_revision_commit, current_version_commit])
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
        for access_point_info in get_configuration['access_point']:
            ap_ssh = get_apnos(access_point_info)
            version = ap_ssh.get_ap_version_ucentral()
            version_list.append(version)
        return version_list

    def get_sdk_version(self):
        version = self.controller_obj.get_sdk_version()
        return version

    def setup_profiles(self, request, param, setup_controller, testbed, get_equipment_ref,
                       instantiate_profile, get_markers, create_lanforge_chamberview_dut, lf_tools,
                       get_security_flags, get_configuration, radius_info, get_apnos, radius_accounting_info):

        instantiate_profile_obj = instantiate_profile(sdk_client=setup_controller)
        print(1, instantiate_profile_obj.sdk_client)
        vlan_id, mode = 0, 0
        parameter = dict(param)
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
            if mode == "wpa3_enterprise":
                for j in profile_data["ssid"][mode]:
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:
                            if j["appliedRadios"].__contains__("2G"):
                                lf_dut_data.append(j)
                            if j["appliedRadios"].__contains__("5G"):
                                lf_dut_data.append(j)
                            j["appliedRadios"] = list(set(j["appliedRadios"]))
                            j['security'] = 'wpa3'
                            RADIUS_SERVER_DATA = radius_info
                            RADIUS_ACCOUNTING_DATA = radius_accounting_info
                            creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j, radius=True,
                                                                               radius_auth_data=RADIUS_SERVER_DATA,
                                                                               radius_accounting_data=RADIUS_ACCOUNTING_DATA)
                            test_cases["wpa3_eap"] = True
                        except Exception as e:
                            print(e)
                            test_cases["wpa3_eap"] = False
        ap_ssh = get_apnos(get_configuration['access_point'][0], pwd="../libs/apnos/", sdk="2.x")
        connected, latest, active = ap_ssh.get_ucentral_status()
        msg = "uCentral status before push :: connected = " + str(connected) + ", latest = " + str(latest) + \
              ", active = " + str(active)
        print(msg)
        allure.attach(name=str(msg), body="")

        if connected == False:
            pytest.exit("AP is disconnected from UC Gateway")
        if latest != active:
            allure.attach(name="FAIL : ubus call ucentral status: ",
                          body="connected: " + str(connected) + "\nlatest: " + str(latest) + "\nactive: " + str(active))
            ap_logs = ap_ssh.logread()
            allure.attach(body=ap_logs, name="FAILURE: AP LOgs: ")
            pytest.fail("AP is disconnected from UC Gateway")
        S = 9
        instance_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
        ap_ssh.run_generic_command(cmd="logger start testcase: " + instance_name)
        instantiate_profile_obj.push_config(serial_number=get_equipment_ref[0])
        time_1 = time.time()
        time.sleep(90)
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
        print("Initial old_config :: ", old_config)
        connected, latest, active = ap_ssh.get_ucentral_status()
        print("active: ", active)
        print("latest: ", latest)

        while old_config == latest:
            time.sleep(5)
            x += 1
            print("old config: ", old_config)
            print("latest: ", latest)
            connected, latest, active = ap_ssh.get_ucentral_status()
            if x == 40:
                break

        if x < 40:
            print("SUCCESS :: Latest Config UPDATED into AP :: old_config == latest ", config)
        else:
            print("FAILED :: Latest Config NOT updated into AP after 200 sec : old_config != latest ", config)

        connected, latest, active = ap_ssh.get_ucentral_status()
        print("active: ", active)
        print("latest: ", latest)
        x = 1
        while active != latest:
            connected, latest, active = ap_ssh.get_ucentral_status()
            time.sleep(10)
            x += 1
            print("active: ", active)
            print("latest: ", latest)
            if x == 20:
                break

        if x < 20:
            print("SUCCESS :: Latest Config properly APPLIED into AP :: active == latest", config)
        else:
            print("FAILED :: Latest Config NOT applied into AP after 200 sec :: active != latest", config)

        time_2 = time.time()
        time_interval = time_2 - time_1
        msg = "Time Took to apply Config :: " + str(time_interval)
        print(msg)
        allure.attach(name=str(msg), body="")

        ap_config_latest = ap_ssh.get_uc_latest_config()
        ap_config_latest["uuid"] = 0

        ap_config_active = ap_ssh.get_uc_active_config()
        ap_config_active["uuid"] = 0

        test_time = 420
        start_time = time.time()
        while time.time() - start_time < test_time:
            ap_config_latest = ap_ssh.get_uc_latest_config()
            msg = "Latest_Config ::   " + str(ap_config_latest)
            print(msg)
            allure.attach(name=str(msg), body=str(ap_config_latest))
            ap_config_latest["uuid"] = 0

            ap_config_active = ap_ssh.get_uc_active_config()
            msg = "Active_Config in AP :: " + str(ap_config_active)
            print(msg)
            allure.attach(name=str(msg), body=str(ap_config_active))
            ap_config_active["uuid"] = 0

            if ap_config_latest == {'uuid': 0} and ap_config_active == {'uuid': 0}:
                msg = "RETRY :: ap_config_latest and ap_config_active contains only {'uuid': 0} , waiting for 5 sec.."
                print(msg)
                allure.attach(name=str(msg), body=str(ap_config_active))
                time.sleep(5)
                continue

            if ap_config_active == ap_config_latest:
                msg = "SUCCESS :: AP is Broadcasting Applied Config"
                print(msg)
                allure.attach(name=str(msg), body=str(ap_config_active))
                msg = "Time taken to reflect latest config in AP :: " + str((time.time() - start_time))
                print(msg)
                allure.attach(name=str(msg), body='')
                break
            msg = "Config still not applied, waiting for 5 sec..."
            print(msg)
            allure.attach(name=str(msg), body='')
            time.sleep(5)

        else:
            print("FAILED :: AP FAILED to apply config after 420 sec, current active config  is  :: ",
                  str(ap_config_active))
            allure.attach(name="FAILED :: AP FAILED to apply config after 420 sec, current active config  is :: ",
                          body=str(ap_config_active))

        msg = "Waiting 30 sec for iwinfo to come up..."
        print(msg)
        allure.attach(name=str(msg), body='')
        time.sleep(30)

        try:
            iwinfo = ap_ssh.iwinfo()
            print("iwinfo :: \n", iwinfo)
            allure.attach(name="iwinfo: ", body=str(iwinfo))

            # tx_power, name = ap_ssh.gettxpower()
            # allure.attach(name="interface name: ", body=str(name))
            # allure.attach(name="tx power: ", body=str(tx_power))
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
            lf_tools.dut_idx_mapping = idx_mapping
            lf_tools.update_ssid(ssid_data=ssid_data)
        except Exception as e:
            print(e)
            pass

        def teardown_session():
            wifi_status = ap_ssh.get_wifi_status()
            allure.attach(name="wifi status", body=str(wifi_status))
            print("\nTeardown")

        request.addfinalizer(teardown_session)
        return test_cases
