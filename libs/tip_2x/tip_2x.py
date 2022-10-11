"""
    Telecom Infra Project OpenWifi 2.X (Ucentral libraries for Test Automation)


"""
import importlib
import json
import random
import string
import time

import allure
import pytest
import requests

logging = importlib.import_module("logging")

ap_lib = importlib.import_module("ap_lib")
controller = importlib.import_module("controller")

"""
    Custom Class Imports needed for OpenWifi 2.X
"""

ConfigureController = controller.ConfigureController
Controller = controller.Controller
FMSUtils = controller.FMSUtils
ProvUtils = controller.ProvUtils
UProfileUtility = controller.UProfileUtility
APLIBS = ap_lib.APLIBS


class tip_2x:
    """
        Standard OpenWifi wlan-testing specific variables

    """
    controller_data = {}
    device_under_tests_info = []
    """
        OpenWifi 2.x Specific Variables that will be only scoped in dut_lib_template Library

    """
    ow_sec_url = ""
    ow_sec_login_username = ""
    ow_sec_login_password = ""
    target = "tip_2x"
    controller_library_object = object()
    prov_library_object = object()
    firmware_library_object = object()
    dut_library_object = object()
    supported_bands = ["2G", "5G", "6G", "5G-lower", "5G-upper"]
    supported_modes = ["BRIDGE", "NAT", "VLAN"]
    supported_encryption = ["open",
                            "wpa",
                            "wpa2_personal",
                            "wpa3_personal",
                            "wpa_wpa2_personal_mixed",
                            "wpa3_personal_mixed",
                            "wpa_enterprise",
                            "wpa2_enterprise",
                            "wpa3_enterprise",
                            "wpa_wpa2_enterprise_mixed",
                            "wpa3_enterprise_mixed",
                            "wpa3_enterprise_192"
                            ]
    tip_2x_specific_encryption_translation = {"open": "none",
                                              "wpa": "psk",
                                              "wpa2_personal": "psk2",
                                              "wpa3_personal": "sae",
                                              "wpa3_personal_mixed": "sae-mixed",
                                              "wpa_wpa2_personal_mixed": "psk-mixed",
                                              "wpa_enterprise": "wpa",
                                              "wpa2_enterprise": "wpa2",
                                              "wpa3_enterprise": "wpa3",
                                              "wpa_wpa2_enterprise_mixed": "wpa-mixed",
                                              "wpa3_enterprise_mixed": "wpa3-mixed",
                                              "wpa3_enterprise_192": "wpa3-192"
                                              }

    def __init__(self, controller_data=None, target=None, configuration=None,
                 device_under_tests_info=[], logging_level=logging.INFO):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging_level)
        if target != self.target:
            logging.error("Target version is : " + target + " Expected target is tip_2x")
            pytest.exit("Target should be 'tip_2x', Current Target is : " + target)
        if controller_data is None:
            controller_data = {}
        self.controller_data = controller_data
        self.configuration = configuration
        self.device_under_tests_info = device_under_tests_info
        self.setup_metadata()
        self.setup_objects()
        self.setup_environment_properties()

    """
        Controller and Access Point specific metadata that is related to OpenWifi 2.x
    """

    def setup_metadata(self):
        logging.info(
            "Setting up the Controller metadata for tip_2x Library: " + str(json.dumps(self.controller_data, indent=2)))
        logging.info("Setting up the DUT metadata for tip_2x Library: " + str(
            json.dumps(self.device_under_tests_info, indent=2)))
        logging.info("Number of DUT's in lab_info.json: " + str(len(self.device_under_tests_info)))
        self.ow_sec_url = self.controller_data["url"]
        self.ow_sec_login_username = self.controller_data["username"]
        self.ow_sec_login_password = self.controller_data["password"]

    def setup_objects(self):
        try:
            self.controller_library_object = Controller(controller_data=self.controller_data)
            self.prov_library_object = ProvUtils(sdk_client=self.controller_library_object)
            self.firmware_library_object = FMSUtils(sdk_client=self.controller_library_object)
        except Exception as e:
            pytest.fail("Unable to setup Controller Objects")
            logging.error("Exception in setting up Controller objects:" + str(e))
        try:
            self.dut_library_object = APLIBS(dut_data=self.device_under_tests_info)
        except Exception as e:
            logging.error("Exception in setting up Access Point Library object:" + str(e))
            pytest.fail("Unable to setup AP Objects")

    def teardown_objects(self):
        self.controller_library_object.logout()

    """ Standard getter methods. Should be available for all type of libraries. Commonly used by wlan-testing"""

    def get_dut_library_object(self):
        return self.dut_library_object

    def get_controller_library_object(self):
        return self.controller_library_object

    def get_controller_data(self):
        return self.controller_data

    def get_device_under_tests_info(self):
        return self.device_under_tests_info

    def get_number_of_dut(self):
        return len(self.device_under_tests_info)

    def get_dut_logs(self, dut_idx=0):
        return self.dut_library_object.get_logs(idx=0)

    def get_controller_logs(self):
        pass

    def get_dut_max_clients(self):
        pass

    def setup_configuration_data(self, configuration=None,
                                 requested_combination=None):
        c_data = configuration.copy()
        if c_data is None:
            pytest.exit("No Configuration Received")
        if requested_combination is None:
            pytest.exit("No requested_combination Received")
        rf_data = None
        if c_data.keys().__contains__("rf"):
            rf_data = c_data["rf"]
        # base_band_keys = ["2G", "5G", "6G", "5G-lower", "5G-upper"]
        base_dict = dict.fromkeys(self.supported_bands)
        for i in base_dict:
            base_dict[i] = []
        for i in requested_combination:
            if i[0] in self.supported_bands:
                base_dict[i[0]].append(self.tip_2x_specific_encryption_translation[i[1]])
            if i[1] in self.supported_bands:
                base_dict[i[1]].append((self.tip_2x_specific_encryption_translation[i[0]]))
        temp = []
        for i in list(base_dict.values()):
            for j in i:
                temp.append(j)
        temp_conf = c_data["ssid_modes"].copy()
        for i in temp_conf:
            if self.tip_2x_specific_encryption_translation[i] not in temp:
                c_data["ssid_modes"].pop(i)

        temp_conf = c_data["ssid_modes"].copy()
        print(self.tip_2x_specific_encryption_translation)
        for i in temp_conf:
            for j in range(len(temp_conf[i])):
                for k in temp_conf[i][j]["appliedRadios"]:
                    if self.tip_2x_specific_encryption_translation[i] not in base_dict[k]:
                        c_data["ssid_modes"][i][j]["appliedRadios"].remove(k)
                        if c_data["ssid_modes"][i][j]["appliedRadios"] == []:
                            c_data["ssid_modes"][i][j] = {}  # .popi.popitem())  # .popitem()

        for i in c_data["ssid_modes"]:
            c_data["ssid_modes"][i] = [x for x in c_data["ssid_modes"][i] if x != {}]
        for ssids in c_data["ssid_modes"]:
            for i in c_data["ssid_modes"][ssids]:
                if i is not {}:
                    i["security"] = self.tip_2x_specific_encryption_translation[ssids]
        temp_conf = c_data.copy()
        for i in range(0, len(self.device_under_tests_info)):
            if c_data["mode"] not in self.device_under_tests_info[i]["supported_modes"]:
                pytest.skip(c_data["mode"] + " is not Supported by DUT")
            for enc in c_data["ssid_modes"]:
                for idx in c_data["ssid_modes"][enc]:
                    check = all(
                        item in self.device_under_tests_info[i]["supported_bands"] for item in idx["appliedRadios"])
                    if not check:
                        temp_conf["ssid_modes"][enc].remove(idx)
        for key in c_data["rf"]:
            if key not in self.device_under_tests_info[i]["supported_bands"]:
                print(key)
                temp_conf["rf"][key] = None

        return temp_conf

    """
        setup_basic_configuration - Method to configure AP in basic operating modes with multiple SSID's and multiple AP's
                                This covers, basic and advanced test cases
    """

    def setup_basic_configuration(self, configuration=None,
                                  requested_combination=None):
        f_conf = self.setup_configuration_data(configuration=configuration,
                                               requested_combination=requested_combination)

        logging.info("Selected Configuration: " + str(json.dumps(f_conf, indent=2)))
        final_configuration = f_conf.copy()
        # Setup Mode
        profile_object = UProfileUtility(sdk_client=self.controller_library_object)
        if final_configuration["mode"] in self.supported_modes:
            profile_object.set_mode(mode=final_configuration["mode"])
        else:
            pytest.skip(final_configuration["mode"] + " Mode is not supported")

        # Setup Radio Scenario
        if final_configuration["rf"] != {}:
            profile_object.set_radio_config(radio_config=final_configuration["rf"])
        else:
            final_configuration["rf"] = {"2G": {}, "5G": {}, "6G": {}}
            profile_object.set_radio_config()
        for ssid in final_configuration["ssid_modes"]:
            for ssid_data in final_configuration["ssid_modes"][ssid]:
                if final_configuration["radius"]:
                    if "radius_auth_data" in ssid_data:
                        RADIUS_SERVER_DATA = ssid_data["radius_auth_data"]
                        RADIUS_ACCOUNTING_DATA = ssid_data["radius_acc_data"]
                    else:
                        RADIUS_SERVER_DATA = self.configuration.RADIUS_SERVER_DATA
                        RADIUS_ACCOUNTING_DATA = self.configuration.RADIUS_ACCOUNTING_DATA
                    profile_object.add_ssid(ssid_data=ssid_data, radius=True, radius_auth_data=RADIUS_SERVER_DATA,
                                            radius_accounting_data=RADIUS_ACCOUNTING_DATA)
                else:
                    profile_object.add_ssid(ssid_data=ssid_data, radius=False)
        logging.info(
            "Configuration That is getting pushed: " + json.dumps(profile_object.base_profile_config, indent=2))
        # Setup Config Apply on all AP's
        ret_val = dict()
        for i in range(0, len(self.device_under_tests_info)):
            self.pre_apply_check(idx=i)  # Do check AP before pushing the configuration

            S = 9
            instance_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
            for i in range(len(self.device_under_tests_info)):
                self.get_dut_library_object().run_generic_command(
                    cmd="logger start testcase: " + instance_name,
                    idx=i)

            # Check the latest uuid
            r_data = self.dut_library_object.ubus_call_ucentral_status(idx=i, print_log=True, attach_allure=False)
            uuid_before_apply = r_data["latest"]

            # Apply the Config
            resp = profile_object.push_config(serial_number=self.device_under_tests_info[i]["identifier"])
            logging.info("Response for Config apply: " + str(resp.status_code))
            if resp.status_code != 200:
                logging.info("Failed to apply Configuration to AP. Response Code" +
                             str(resp.status_code) +
                             "Retrying in 5 Seconds... ")
                time.sleep(5)
                resp = profile_object.push_config(serial_number=self.device_under_tests_info[i]["identifier"])
                if resp.status_code != 200:
                    logging.error("Failed to apply Config, Response code:" + str(resp.status_code))
                    pytest.fail("Failed to apply Config, Response code :" + str(resp.status_code))

            r_data = self.dut_library_object.ubus_call_ucentral_status(idx=i, print_log=True, attach_allure=False)
            uuid_after_apply = r_data["latest"]
            x = 0
            while uuid_before_apply == uuid_after_apply:
                time.sleep(10)
                x += 1
                logging.info("uuid_before_apply: " + str(uuid_before_apply))
                logging.info("uuid_after_apply: " + str(uuid_after_apply))
                r_data = self.dut_library_object.ubus_call_ucentral_status(idx=i, print_log=False, attach_allure=False)
                uuid_after_apply = r_data["latest"]
                if x == 5:
                    break
            time.sleep(5)
            r_data = self.dut_library_object.ubus_call_ucentral_status(idx=i, print_log=False, attach_allure=False)
            uuid_after_apply = r_data["latest"]
            if uuid_after_apply == uuid_before_apply:
                logging.error("Config is not received by AP")
                logging.info("uuid_before_apply: " + str(uuid_before_apply))
                logging.info("uuid_after_apply: " + str(uuid_after_apply))
                self.dut_library_object.get_dut_logs(idx=i, print_log=False, attach_allure=True)
                pytest.fail("Config sent from Gateway is not received by AP")
            self.dut_library_object.get_latest_config_recieved(idx=i, print_log=True, attach_allure=False)

            r_data = self.dut_library_object.ubus_call_ucentral_status(idx=i, print_log=False, attach_allure=False)
            latest_uuid = r_data["latest"]

            r_data = self.dut_library_object.ubus_call_ucentral_status(idx=i, print_log=False, attach_allure=False)
            active_uuid = r_data["active"]

            x = 0
            while latest_uuid == active_uuid:
                time.sleep(10)
                x += 1
                logging.info("active_uuid: " + str(active_uuid))
                logging.info("latest_uuid: " + str(latest_uuid))
                r_data = self.dut_library_object.ubus_call_ucentral_status(idx=i, print_log=False, attach_allure=False)
                active_uuid = r_data["active"]
                if x == 5:
                    break
            if latest_uuid != active_uuid:
                logging.error("Config is not received by AP")
                logging.info("uuid_before_apply: " + str(uuid_before_apply))
                logging.info("uuid_after_apply: " + str(uuid_after_apply))
                self.dut_library_object.get_dut_logs(idx=i, print_log=False, attach_allure=True)
                pytest.fail("Config sent from Gateway is Received by AP, But not Applied by AP")
            self.dut_library_object.get_active_config(idx=i, print_log=True, attach_allure=False)

            logging.info("Config is Properly Applied on AP, Waiting for 30 Seconds for All interfaces to come up")
            # wait time interfaces to come up
            time.sleep(30)

            self.post_apply_check(idx=i)  # Do check AP after pushing the configuration

            for i in range(len(self.device_under_tests_info)):
                self.get_dut_library_object().run_generic_command(
                    cmd="logger stop testcase: " + instance_name,
                    idx=i)
                ap_logs = self.get_dut_library_object().get_logread(
                    start_ref="start testcase: " + instance_name,
                    stop_ref="stop testcase: " + instance_name)
                allure.attach(name='Logs - ' + self.device_under_tests_info[i]["identifier"],
                              body=str(ap_logs))

            ret_val[self.device_under_tests_info[i]["identifier"]] = self.get_applied_ssid_info(idx=i,
                                                                                                profile_object=profile_object)

        temp_data = ret_val.copy()
        for dut in temp_data:
            ret_val[dut] = dict.fromkeys(["ssid_data", "radio_data"])
            ret_val[dut]["radio_data"] = temp_data[dut][-1]
            temp_data[dut].pop(-1)
            n = len(temp_data[dut])
            lst = list(range(0, n))
            ret_val[dut]["ssid_data"] = dict.fromkeys(lst)
            for j in ret_val[dut]["ssid_data"]:
                a = temp_data[dut][j].copy()
                a = dict.fromkeys(["ssid", "encryption", "password", "band", "bssid"])
                a["ssid"] = temp_data[dut][j][0]
                a["encryption"] = temp_data[dut][j][1]
                a["password"] = temp_data[dut][j][2]
                a["band"] = temp_data[dut][j][3]
                a["bssid"] = temp_data[dut][j][4]
                ret_val[dut]["ssid_data"][j] = a
            temp = ret_val[dut]["radio_data"].copy()
            for j in temp:
                a = dict.fromkeys(["channel", "bandwidth", "frequency"])
                if temp[j] != None:
                    a["channel"] = temp[j][0]
                    a["bandwidth"] = temp[j][1]
                    a["frequency"] = temp[j][2]
                ret_val[dut]["radio_data"][j] = a
        return ret_val

    """
        setup_special_configuration - Method to configure APs in mesh operating modes with multiple SSID's and multiple AP's
                                    This covers, mesh and other roaming scenarios which includes any special type of modes
                                    multiple AP's with WDS and Wifi Steering scenarios are also covered here
    """

    def setup_special_configuration(self, configuration=None,
                                    requested_combination=None):
        final_configuration = self.setup_configuration_data(configuration=configuration,
                                                            requested_combination=requested_combination)

        logging.info("Selected Configuration: " + str(json.dumps(final_configuration, indent=2)))

        profile_object = UProfileUtility(sdk_client=self.controller_library_object)
        if final_configuration["mode"] in self.supported_modes:
            profile_object.set_mode(mode=final_configuration["mode"])
        else:
            pytest.skip(final_configuration["mode"] + " Mode is not supported")

        # Setup Radio Scenario
        if final_configuration["rf"] != {}:
            profile_object.set_radio_config(radio_config=final_configuration["rf"])
        else:
            profile_object.set_radio_config()
        for ssid in final_configuration["ssid_modes"]:
            for ssid_data in final_configuration["ssid_modes"][ssid]:
                profile_object.add_ssid(ssid_data=ssid_data)
        logging.info(
            "Configuration That is getting pushed: " + json.dumps(profile_object.base_profile_config, indent=2))
        r_val = False

        # Do check AP before pushing the configuration
        # TODO
        self.dut_library_object.check_serial_connection()
        """  
        serial connection check
        ubus call ucentral status
        save the current uuid
        uci show ucentral
        ifconfig
        wifi status
        start logger to collect ap logs before config apply        
        Timestamp before doing config apply
        """

        for dut in self.device_under_tests_info:
            resp = profile_object.push_config(serial_number=dut["identifier"])
            logging.info("Response for Config apply: " + str(resp.status_code))
            if resp.status_code != 200:
                logging.info("Failed to apply Configuration to AP. Response Code" +
                             str(resp.status_code) +
                             "Retrying in 5 Seconds... ")
                time.sleep(5)
                resp = profile_object.push_config(serial_number=dut["identifier"])
                if resp.status_code != 200:
                    logging.info("Failed to apply Config, Response code:" + str(resp.status_code))
                    pytest.fail("Failed to apply Config, Response code :" + str(resp.status_code))
        if resp.status_code == 200:
            r_val = True
        # TODO
        """ 
        serial connection check
        ubus call ucentral status
        save the current uuid and compare with the one before config apply
        save the active config and compare with the latest apply
        uci show 
        ifconfig
        iwinfo
        wifi status
        start logger to collect ap logs before config apply        
        Timestamp after doing config apply
        """
        return r_val

    def get_dut_channel_data(self, idx):
        try:
            d = self.dut_library_object.run_generic_command(cmd="iw dev | grep channel", idx=idx)
            d = d.replace("\n", "").replace("\t", "").replace(" ", "").split("channel")
            d.pop(0)
            d = list(set(d))
            data = dict.fromkeys(["2G", "5G", "6G"])
            for i in d:
                channel = int(i.split("(")[0])
                bandwidth = int(i.split(":")[1].split("MHz")[0])
                center_freq = int(i.split(":")[-1].replace("MHz", ""))
                if 2401 < center_freq < 2495:
                    data["2G"] = [channel, bandwidth, center_freq]
                elif center_freq in [5955, 5975, 5995] and channel <= 9:
                    data["6G"] = [channel, bandwidth, center_freq]
                elif 5030 < center_freq < 5990:
                    data["5G"] = [channel, bandwidth, center_freq]
                elif 5995 < center_freq < 7125:
                    data["6G"] = [channel, bandwidth, center_freq]
                else:
                    pass
        except Exception as e:
            logging.error("Exception in getting DUT Channel and bw data, Retrying again!")
            try:
                d = self.dut_library_object.run_generic_command(cmd="iw dev | grep channel", idx=idx)
                d = d.replace("\n", "").replace("\t", "").replace(" ", "").split("channel")
                d.pop(0)
                data = dict.fromkeys(["2G", "5G", "6G"])
                for i in d:
                    channel = int(i.split("(")[0])
                    bandwidth = int(i.split(":")[1].split("MHz")[0])
                    center_freq = int(i.split(":")[-1].replace("MHz", ""))
                    if 2401 < center_freq < 2495:
                        data["2G"] = [channel, bandwidth, center_freq]
                    elif center_freq in [5955, 5975, 5995] and channel <= 9:
                        data["6G"] = [channel, bandwidth, center_freq]
                    elif 5030 < center_freq < 5990:
                        data["5G"] = [channel, bandwidth, center_freq]
                    elif 5995 < center_freq < 7125:
                        data["6G"] = [channel, bandwidth, center_freq]
                    else:
                        pass
            except Exception as e:
                logging.error("Exception in getting DUT Channel and bw data.")
        return data

    def get_applied_ssid_info(self, profile_object=None, idx=0):
        if profile_object is None:
            logging.error("Profile object is None, Unable to fetch ssid info from AP")
            return None
        ssid_info_sdk = profile_object.get_ssid_info()
        ap_wifi_data = self.dut_library_object.get_iwinfo(idx=idx)
        channel_info = self.get_dut_channel_data(idx=idx)
        o = ap_wifi_data.split()
        iwinfo_bssid_data = {}
        for i in range(len(o)):
            if o[i].__contains__("ESSID"):
                if o[i + 9].__contains__("2.4"):
                    band = "2G"
                else:
                    band = "5G"
                iwinfo_bssid_data[o[i - 1]] = [o[i + 1].replace('"', ''), o[i + 4], band]
        for p in iwinfo_bssid_data:
            for q in ssid_info_sdk:
                if iwinfo_bssid_data[p][0] == q[0] and iwinfo_bssid_data[p][2] == q[3]:
                    q.append(iwinfo_bssid_data[p][1])
        ssid_info_sdk.append(channel_info)
        return ssid_info_sdk

    def get_dut_version(self):
        version_info = []
        for ap in range(len(self.device_under_tests_info)):
            version_info.append(self.dut_library_object.get_ap_version(idx=ap, print_log=True))
        return version_info

    def get_controller_version(self):
        version_info = dict()
        version_info["ow_fms"] = self.controller_library_object.get_sdk_version_fms()
        version_info["ow_gw"] = self.controller_library_object.get_sdk_version_gw()
        version_info["ow_sec"] = self.controller_library_object.get_sdk_version_sec()
        version_info["ow_prov"] = self.controller_library_object.get_sdk_version_prov()
        # version_info["ow_rrm"] = self.controller_library_object.get_sdk_version_owrrm()
        # version_info["ow_analytics"] = self.controller_library_object.get_sdk_version_ow_analytics()
        # version_info["ow_sub"] = self.controller_library_object.get_sdk_version_owsub()
        return version_info

    # TODO: Get the vlans info such as vlan-ids
    #  Jitendra

    def vlans_needed(self):
        pass

    # TODO: Get the wireless info data structure such as (ssid, bssid, passkey, encryption, band, channel)
    #  Jitendra

    def pre_apply_check(self, idx=0):
        """
                    serial connection check
                    ubus call ucentral status
                    save the current uuid
                    uci show ucentral
                    ifconfig
                    wifi status
                    start logger to collect ap logs before config apply
                    Timestamp before doing config apply
                    """

        self.dut_library_object.check_serial_connection(idx=idx)
        self.dut_library_object.setup_serial_environment(idx=idx)
        self.dut_library_object.verify_certificates(idx=idx)
        ret_val = self.dut_library_object.ubus_call_ucentral_status(idx=idx, attach_allure=False, retry=10)
        wifi_status = self.dut_library_object.get_wifi_status(idx=idx, attach_allure=False)
        allure.attach(name="wifi_status_before_apply: ", body=str(json.dumps(wifi_status, indent=2)))
        if not ret_val["connected"] or ret_val["connected"] is None:
            self.dut_library_object.check_connectivity(idx=idx)
            self.dut_library_object.restart_ucentral_service(idx=idx, attach_allure=False)
            time.sleep(30)
            ret_val = self.dut_library_object.ubus_call_ucentral_status(idx=idx, attach_allure=False, retry=10)
            if not ret_val["connected"] or ret_val["connected"] is None:
                self.dut_library_object.check_connectivity(idx=idx)
                pytest.fail("AP is in disconnected state from Ucentral gateway!!!")
            else:
                allure.step("Connected to Gateway after Restarting the ucentral Process!!!")

            # TODO: check the connectivity (if it is not connected, then check the lanforge wan port and bring it
            #  up if lanforge eth is in down state. Also check the link state of eth port with ip address
            #  reload the scenario in case it is messed up)
            #  if wan is available, then run (/etc/init.d/ucentral restart) to retry the connection and check the
            #  status again in next 30 seconds if still disconnected, then fail and attach the logs,
            #  Jitendra
            # pytest.fail("AP is in disconnected state from Ucentral gateway!!!")

    def post_apply_check(self, idx=0):
        """
                    ubus call ucentral status
                    ifconfig - check if up0v0 has ip address
                    wifi status - check if all phy radios are up
        """
        ret_val = self.dut_library_object.ubus_call_ucentral_status(idx=idx, retry=10)
        if not ret_val["connected"] or ret_val["connected"] is None:
            logging.error(" AP Went to Disconnected State after Applying Config, Checking again after 30 Seconds")
            time.sleep(30)
            ret_val = self.dut_library_object.ubus_call_ucentral_status(idx=idx)
            if not ret_val["connected"] or ret_val["connected"] is None:
                logging.error("Dang !!!, AP is still in Disconnected State. Your Config Messed up.")
                logging.error("Failed the post apply check on: " + self.device_under_tests_info[idx]["identifier"])
                self.dut_library_object.check_connectivity(idx=idx, attach_allure=False)
        self.dut_library_object.check_connectivity(idx=idx)
        r_data = self.dut_library_object.get_wifi_status(idx=idx, attach_allure=False)
        allure.attach(name="wifi_status_after_apply: ", body=str(json.dumps(r_data, indent=2)))
        logging.info("Checking Wifi Status after Config Apply...")
        for radio in r_data:
            if not r_data[radio]["up"]:
                logging.error(radio + " is in down State...")
                pytest.fail(radio + " is in down State after config apply")
            else:
                logging.info(radio + " is up and running")

    def setup_environment_properties(self, add_allure_environment_property=None):
        if add_allure_environment_property is None:
            return
        add_allure_environment_property('Cloud-Controller-SDK-URL', self.controller_data.get("url"))
        sdk_version_data = self.get_controller_version()
        for microservice in sdk_version_data:
            add_allure_environment_property(microservice + '-version',
                                            str(sdk_version_data.get(microservice)))
        dut_versions = self.get_dut_version()
        for i in range(len(self.device_under_tests_info)):
            add_allure_environment_property("Firmware-Version_" + self.device_under_tests_info[i]["identifier"],
                                            str(dut_versions[i]))

        for dut in self.device_under_tests_info:
            models = []
            identifiers = []
            models.append(dut["model"])
            identifiers.append(dut["identifier"])
        add_allure_environment_property('DUT-Model/s', ", ".join(models))
        add_allure_environment_property('Serial-Number/s', ", ".join(identifiers))

    def setup_firmware(self):
        # Query AP Firmware
        upgrade_status = []
        for ap in range(len(self.device_under_tests_info)):

            # If specified as URL
            try:
                response = requests.get(self.device_under_tests_info[ap]['firmware_version'])
                logging.info("URL is valid and exists on the internet")
                allure.attach(name="firmware url: ", body=str(self.device_under_tests_info[ap]['firmware_version']))
                target_revision_commit = self.device_under_tests_info[ap]['firmware_version'].split("-")[-2]
                ap_version = self.dut_library_object.get_ap_version(idx=ap)
                current_version_commit = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

                # if AP is already in target Version then skip upgrade unless force upgrade is specified
                if target_revision_commit in current_version_commit:
                    continue
                self.firmware_library_object.upgrade_firmware(serial=self.device_under_tests_info[ap]['identifier'],
                                                              url=str(
                                                                  self.device_under_tests_info[ap]['firmware_version']))

                items = list(range(0, 300))
                l = len(items)
                ap_version = self.dut_library_object.get_ap_version(idx=ap)
                current_version_commit = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                if target_revision_commit in current_version_commit:
                    upgrade_status.append([self.device_under_tests_info[ap]['identifier'], target_revision_commit,
                                           current_version_commit])
                    logging.info("Firmware Upgraded to : " + str(ap_version))
                else:
                    logging.info("firmware upgraded failed: " + str(target_revision))
                    upgrade_status.append([self.device_under_tests_info[ap]['identifier'], target_revision_commit,
                                           current_version_commit])
                break
            except Exception as e:
                logging.error("URL does not exist on Internet")
            # else Specified as "branch-commit_id" / "branch-latest"
            firmware_url = ""
            ap_version = self.dut_library_object.get_ap_version(idx=ap)
            response = self.firmware_library_object.get_latest_fw(model=self.device_under_tests_info[ap]['model'])
            # if the target version specified is "branch-latest"
            if self.device_under_tests_info[ap]['firmware_version'].split('-')[1] == "latest":
                # get the latest branch
                firmware_list = self.firmware_library_object.get_firmwares(
                    model=self.device_under_tests_info[ap]['model'], branch="", commit_id='')
                firmware_list.reverse()

                for firmware in firmware_list:
                    if firmware['image'] == "":
                        continue
                    if str(firmware['image']).__contains__("upgrade.bin"):
                        temp = firmware['image'].split("-")
                        temp.pop(-1)
                        temp = "-".join(temp)
                        firmware['image'] = temp
                    if self.device_under_tests_info[ap]['firmware_version'].split('-')[0] == 'release':
                        if firmware['revision'].split("/")[1].replace(" ", "").split('-')[1].__contains__('v2.'):
                            logging.info("Target Firmware: \n" + str(firmware))
                            allure.attach(name="Target firmware : ", body=str(firmware))
                            target_revision = firmware['revision'].split("/")[1].replace(" ", "")

                            # check the current AP Revision before upgrade

                            ap_version = self.dut_library_object.get_ap_version(idx=ap)
                            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

                            # print and report the firmware versions before upgrade
                            allure.attach(name="Before Firmware Upgrade Request: ",
                                          body="current revision: " + str(
                                              current_version) + "\ntarget revision: " + str(target_revision))
                            logging.info("current revision: " + str(current_version) + "\ntarget revision: " + str(
                                target_revision))

                            # if AP is already in target Version then skip upgrade unless force upgrade is specified
                            if current_version == target_revision:
                                upgrade_status.append([self.device_under_tests_info[ap]['identifier'], target_revision,
                                                       current_version, 'skip'])
                                logging.info("Skipping Upgrade! AP is already in target version")
                                allure.attach(name="Skipping Upgrade because AP is already in the target Version",
                                              body="")
                                break

                            self.firmware_library_object.upgrade_firmware(
                                serial=self.device_under_tests_info[ap]['identifier'],
                                url=str(firmware['uri']))
                            # wait for 300 seconds after firmware upgrade
                            logging.info("waiting for 300 Sec for Firmware Upgrade")
                            time.sleep(300)

                            # check the current AP Revision again
                            ap_version = self.dut_library_object.get_ap_version(idx=ap)
                            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                            # print and report the Firmware versions after upgrade
                            allure.attach(name="After Firmware Upgrade Request: ",
                                          body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                            logging.info("current revision: " + str(current_version) +
                                         "\ntarget revision: " + str(target_revision))
                            if current_version == target_revision:
                                upgrade_status.append(
                                    [self.device_under_tests_info[ap]['identifier'], target_revision, current_version])
                                logging.info("firmware upgraded successfully: " + target_revision)
                            else:
                                upgrade_status.append(
                                    [self.device_under_tests_info[ap]['identifier'], target_revision, current_version])
                                logging.info("firmware upgraded failed: ", target_revision)
                            break
                    if firmware['image'].split("-")[-2] == \
                            self.device_under_tests_info[ap]['firmware_version'].split('-')[0]:
                        logging.info("Target Firmware: \n" + firmware)
                        allure.attach(name="Target firmware : ", body=str(firmware))

                        target_revision = firmware['revision'].split("/")[1].replace(" ", "")

                        # check the current AP Revision before upgrade
                        ap_version = self.dut_library_object.get_ap_version(idx=ap)
                        current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

                        # print and report the firmware versions before upgrade
                        allure.attach(name="Before Firmware Upgrade Request: ",
                                      body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                        logging.info("current revision: " + current_version + "\ntarget revision: " + target_revision)

                        # if AP is already in target Version then skip upgrade unless force upgrade is specified
                        if current_version == target_revision:
                            upgrade_status.append(
                                [self.device_under_tests_info[ap]['identifier'], target_revision, current_version,
                                 'skip'])
                            logging.info("Skipping Upgrade! AP is already in target version")
                            allure.attach(name="Skipping Upgrade because AP is already in the target Version", body="")
                            break

                        self.firmware_library_object.upgrade_firmware(
                            serial=self.device_under_tests_info[ap]['identifier'], url=str(firmware['uri']))
                        # wait for 300 seconds after firmware upgrade
                        logging.info("waiting for 300 Sec for Firmware Upgrade")
                        time.sleep(500)

                        # check the current AP Revision again
                        ap_version = self.dut_library_object.get_ap_version(idx=ap)
                        current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                        # print and report the Firmware versions after upgrade
                        allure.attach(name="After Firmware Upgrade Request: ",
                                      body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                        logging.info("current revision: " + current_version + "\ntarget revision: " + target_revision)
                        if current_version == target_revision:
                            upgrade_status.append(
                                [self.device_under_tests_info[ap]['identifier'], target_revision, current_version])
                            logging.info("firmware upgraded successfully: " + str(target_revision))
                        else:
                            upgrade_status.append(
                                [self.device_under_tests_info[ap]['identifier'], target_revision, current_version])
                            logging.info("firmware upgraded failed: " + str(target_revision))
                        break
            # if branch-commit is specified
            else:
                firmware_list = self.firmware_library_object.get_firmwares(
                    model=self.device_under_tests_info[ap]['model'],
                    branch="", commit_id='')
                fw_list = []
                # getting the list of firmwares in fw_list that has the commit id specified as an input
                for firmware in firmware_list:
                    if firmware['revision'].split("/")[1].replace(" ", "").split('-')[-1] == \
                            self.device_under_tests_info[ap]['firmware_version'].split('-')[1]:
                        fw_list.append(firmware)

                # If there is only 1 commit ID in fw_list
                if len(fw_list) == 1:

                    logging.info("Target Firmware: \n" + str(fw_list[0]))
                    allure.attach(name="Target firmware : ", body=str(fw_list[0]))

                    url = fw_list[0]['uri']
                    target_revision = fw_list[0]['revision'].split("/")[1].replace(" ", "")

                    # check the current AP Revision before upgrade
                    ap_version = self.dut_library_object.get_ap_version(idx=ap)
                    current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

                    # print and report the firmware versions before upgrade
                    allure.attach(name="Before Firmware Upgrade Request: ",
                                  body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                    logging.info(
                        "current revision: " + str(current_version) + "\ntarget revision: " + str(target_revision))

                    # if AP is already in target Version then skip upgrade unless force upgrade is specified
                    if current_version == target_revision:
                        upgrade_status.append(
                            [self.device_under_tests_info[ap]['identifier'], target_revision, current_version, 'skip'])
                        logging.info("Skipping Upgrade! AP is already in target version")
                        allure.attach(name="Skipping Upgrade because AP is already in the target Version", body="")
                        break

                    # upgrade the firmware in another condition
                    else:
                        self.firmware_library_object.upgrade_firmware(
                            serial=self.device_under_tests_info[ap]['identifier'], url=str(url))

                        # wait for 300 seconds after firmware upgrade
                        logging.info("waiting for 300 Sec for Firmware Upgrade")
                        time.sleep(300)

                        # check the current AP Revision again
                        ap_version = self.dut_library_object.get_ap_version(idx=ap)
                        current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                        # print and report the Firmware versions after upgrade
                        allure.attach(name="After Firmware Upgrade Request: ",
                                      body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                        logging.info(
                            "current revision: " + str(current_version) + "\ntarget revision: " + target_revision)
                        if current_version == target_revision:
                            upgrade_status.append(
                                [self.device_under_tests_info[ap]['identifier'], target_revision, current_version])
                            logging.info("firmware upgraded successfully: " + target_revision)
                        else:
                            upgrade_status.append(
                                [self.device_under_tests_info[ap]['identifier'], target_revision, current_version])
                            logging.info("firmware upgraded failed: " + str(target_revision))
                        break

                # if there are 1+ firmware images in fw_list then check for branch
                else:
                    target_fw = ""
                    for firmware in fw_list:
                        if self.device_under_tests_info[ap]['firmware_version'].split('-')[0] == 'release':
                            if firmware['revision'].split("/")[1].replace(" ", "").split('-')[1].__contains__('v2.'):
                                target_fw = firmware
                                break
                        if firmware['image'].split("-")[-2] == \
                                self.device_under_tests_info[ap]['firmware_version'].split('-')[0]:
                            target_fw = firmware
                            break
                    firmware = target_fw
                    logging.info("Target Firmware: \n" + firmware)
                    allure.attach(name="Target firmware : ", body=str(firmware))

                    target_revision = firmware['revision'].split("/")[1].replace(" ", "")

                    # check the current AP Revision before upgrade
                    ap_version = self.dut_library_object.get_ap_version(idx=ap)
                    current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

                    # print and report the firmware versions before upgrade
                    allure.attach(name="Before Firmware Upgrade Request: ",
                                  body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                    logging.info("current revision: ", current_version, "\ntarget revision: ", target_revision)

                    # if AP is already in target Version then skip upgrade unless force upgrade is specified
                    if current_version == target_revision:
                        upgrade_status.append(
                            [self.device_under_tests_info[ap]['identifier'], target_revision, current_version, 'skip'])
                        logging.info("Skipping Upgrade! AP is already in target version")
                        allure.attach(name="Skipping Upgrade because AP is already in the target Version", body="")
                        break

                    self.firmware_library_object.upgrade_firmware(serial=self.device_under_tests_info[ap]['identifier'],
                                                                  url=str(firmware['uri']))
                    # wait for 300 seconds after firmware upgrade

                    logging.info("waiting for 300 Sec for Firmware Upgrade")
                    time.sleep(300)

                    # check the current AP Revision again
                    ap_version = self.dut_library_object.get_ap_version(idx=ap)
                    current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                    # print and report the Firmware versions after upgrade
                    allure.attach(name="After Firmware Upgrade Request: ",
                                  body="current revision: " + current_version + "\ntarget revision: " + target_revision)
                    logging.info("current revision: ", current_version, "\ntarget revision: ", target_revision)
                    if current_version == target_revision:
                        upgrade_status.append([target_revision, current_version])
                        logging.info("firmware upgraded successfully: ", target_revision)
                    else:
                        upgrade_status.append([target_revision, current_version])
                        logging.info("firmware upgraded failed: ", target_revision)
                    break
        return upgrade_status

    def simulate_radar(self, idx=0):
        """Simulate radar command for DFS"""
        ret = self.dut_library_object.dfs(idx=idx)
        return ret

    def get_dfs_logs(self, idx=0):
        """Get the ap logs after Simulate radar command"""
        logs = self.dut_library_object.dfs_logread(idx=idx)
        return logs

    def reboot(self, idx=0):
        """Reboot the AP"""
        ret = self.dut_library_object.reboot(idx=idx)
        return ret


if __name__ == '__main__':
    basic_05 = {
        "target": "tip_2x",
        "controller": {
            "url": "https://sec-qa01.cicd.lab.wlan.tip.build:16001",
            "username": "tip@ucentral.com",
            "password": "OpenWifi%123"
        },
        "device_under_tests": [{
            "model": "cig_wf188n",
            "supported_bands": ["2G", "5G"],
            "supported_modes": ["BRIDGE", "NAT", "VLAN"],
            "wan_port": "1.1.eth2",
            "ssid": {
                "mode": "BRIDGE",
                "2g-ssid": "OpenWifi",
                "5g-ssid": "OpenWifi",
                "6g-ssid": "OpenWifi",
                "2g-password": "OpenWifi",
                "5g-password": "OpenWifi",
                "6g-password": "OpenWifi",
                "2g-encryption": "WPA2",
                "5g-encryption": "WPA2",
                "6g-encryption": "WPA3",
                "2g-bssid": "68:7d:b4:5f:5c:31",
                "5g-bssid": "68:7d:b4:5f:5c:3c",
                "6g-bssid": "68:7d:b4:5f:5c:38"
            },
            "mode": "wifi6",
            "identifier": "0000c1018812",
            "method": "serial",
            "host_ip": "10.28.3.103",
            "host_username": "lanforge",
            "host_password": "pumpkin77",
            "host_ssh_port": 22,
            "serial_tty": "/dev/ttyAP1",
            "firmware_version": "next-latest"
        }],
        "traffic_generator": {
            "name": "lanforge",
            "testbed": "basic",
            "scenario": "dhcp-bridge",
            "details": {
                "manager_ip": "10.28.3.28",
                "http_port": 8080,
                "ssh_port": 22,
                "setup": {"method": "build", "DB": "Test_Scenario_Automation"},
                "wan_ports": {
                    "1.1.eth2": {"addressing": "dhcp-server", "subnet": "172.16.0.1/16", "dhcp": {
                        "lease-first": 10,
                        "lease-count": 10000,
                        "lease-time": "6h"
                    }
                                 }
                },
                "lan_ports": {
                    "1.1.eth1": {"addressing": "dynamic"}
                },
                "uplink_nat_ports": {
                    "1.1.eth1": {"addressing": "static",
                                 "subnet": "10.28.2.16/24",
                                 "gateway_ip": "10.28.2.1",
                                 "ip_mask": "255.255.255.0"
                                 }
                }
            }
        }
    }
    var = tip_2x(controller_data=basic_05["controller"],
                 device_under_tests_info=basic_05["device_under_tests"],
                 target=basic_05["target"])

    # var.setup_objects()
    setup_params_enterprise = {
        "mode": "BRIDGE",
        "ssid_modes": {
            "wpa_enterprise": [
                {"ssid_name": "tls_ssid_wpa_eap_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "tls_ssid_wpa_eap_5g", "appliedRadios": ["5G"], "security_key": "something"}],
            "wpa2_enterprise": [
                {"ssid_name": "tls_ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "tls_ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "security_key": "something"}],
            "wpa3_enterprise": [
                {"ssid_name": "tls_ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "tls_ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "security_key": "something"}]},

        "rf": {},
        "radius": True
    }
    target = [['6G', 'wpa3_personal']]
    # d = var.setup_configuration_data(configuration=setup_params_general_two, requested_combination=target)
    d = var.setup_basic_configuration(configuration=setup_params_enterprise, requested_combination=target)
    print(d)
    # var.setup_firmware()
    # var.teardown_objects()
