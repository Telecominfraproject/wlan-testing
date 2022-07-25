"""
    Telecom Infra Project OpenWifi 2.X (Ucentral libraries for Test Automation)


"""
import importlib
import json

import allure
import pytest

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
        OpenWifi 2.x Specific Variables that will be only scoped in tip_2x Library

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

    def __init__(self, controller_data=None, target=None,
                 device_under_tests_info=[], logging_level=logging.INFO):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging_level)
        if target != self.target:
            logging.error("Target version is : " + target + " Expected target is tip_2x")
            pytest.exit("Target should be 'tip_2x', Current Target is : " + target)
        if controller_data is None:
            controller_data = {}
        self.controller_data = controller_data
        self.device_under_tests_info = device_under_tests_info
        self.setup_metadata()

    """
        Controller and Access Point specific metadata that is related to OpenWifi 2.x
    """

    def setup_metadata(self):
        logging.info("setting up the Controller metadata for tip_2x Library: " + str(self.controller_data))
        logging.info("setting up the DUT metadata for tip_2x Library: " + str(self.device_under_tests_info))
        logging.info("Number of DUT's configured: " + str(len(self.device_under_tests_info)))
        self.ow_sec_url = self.controller_data["url"]
        self.ow_sec_login_username = self.controller_data["username"]
        self.ow_sec_login_password = self.controller_data["password"]

    def setup_objects(self):
        try:
            self.controller_library_object = Controller(controller_data=self.lab_info["controller"])
            self.prov_library_object = ProvUtils(sdk_client=self.controller_obj)
            self.firmware_library_object = FMSUtils(sdk_client=self.controller_obj)
        except Exception as e:
            logging.error("Exception in setting up Controller objects:" + str(e))
        try:
            self.dut_library_object = APLIBS()
        except Exception as e:
            logging.error("Exception in setting up Access Point Library object:" + str(e))

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

    def setup_configuration(self, configuration=None,
                            requested_combination=None):

        if configuration is None:
            pytest.exit("No Configuration Received")
        if requested_combination is None:
            pytest.exit("No requested_combination Received")
        print(configuration, "\n", requested_combination)
        rf_data = None
        if configuration.keys().__contains__("rf"):
            rf_data = configuration["rf"]

        mode = configuration["mode"]
        base_band_keys = ["2G", "5G", "6G", "5G-lower", "5G-upper"]
        base_dict = dict.fromkeys(base_band_keys)
        for i in base_dict:
            base_dict[i] = []
        for i in requested_combination:
            if i[0] in base_band_keys:
                base_dict[i[0]].append(self.tip_2x_specific_encryption_translation[i[1]])
            if i[1] in base_band_keys:
                base_dict[i[1]].append((self.tip_2x_specific_encryption_translation[i[0]]))


        temp =[]
        for i in list(base_dict.values()):
            for j in i:
                temp.append(j)
        temp_conf = configuration["ssid_modes"].copy()
        for i in temp_conf:
            if self.tip_2x_specific_encryption_translation[i] not in temp:
                configuration["ssid_modes"].pop(i)
        print(json.dumps(configuration, indent=2))

        temp_conf = configuration["ssid_modes"].copy()
        print(base_dict)
        for i in temp_conf:
            for j in range(len(temp_conf[i])):
                print("shivam")
                print(temp_conf[i], j)
                for k in temp_conf[i][j]["appliedRadios"]:
                    if self.tip_2x_specific_encryption_translation[i] not in base_dict[k]:
                        print(i, temp_conf[i][j], k)















            configuration["ssid_modes"][i][j]["appliedRadios"]

        print(json.dumps(configuration, indent=2))

            # if i in base_dict[temp[i]["appliedRadios"]]:
            #     pass





        exit()
        # print("gogo" + configuration)

        for ssids in configuration["ssid_modes"]:
            for i in configuration["ssid_modes"][ssids]:
                i["security"] = self.tip_2x_specific_encryption_translation[ssids]
                print(i, i['appliedRadios'])

            # i['appliedRadios']

        # Setup Profile Object
        profile_object = UProfileUtility(sdk_client=self.controller_library_object)

        # Setup Radio Scenario
        if rf_data != {}:
            profile_object.set_radio_config(radio_config=rf_data)
        else:
            profile_object.set_radio_config()

        # Setup mode
        if mode in ["BRIDGE", "NAT", "VLAN"]:
            profile_object.set_mode(mode=mode)
        else:
            logging.warning("Unsupported Mode Specified: " + mode)
            pytest.skip("Unsupported Mode Specified: " + mode)
        dta = {'ssid_name': 'ssid_wpa2_5g_br', 'appliedRadios': ['5G'], 'security_key': 'something', "security": "psk2"}
        profile_object.add_ssid(dta)

        logging.info(str(json.dumps(profile_object.base_profile_config, indent=2)))
        # ssid_encryptions = list(configuration["ssid_modes"].keys())
        # for comb in requested_combination:
        #     for enc in ssid_encryptions:
        #
        #         if enc in comb:
        #
        # for encryption in ssid_encryptions:
        #     band = []
        #     enc = None
        #     for value in requested_combination:
        #         for val in value:
        #             # print(self.supported_bands, val)
        #             if val in self.supported_bands:
        #                 band.append(val)
        #             if val in self.supported_encryption:
        #                 enc = val
        #     print(band, enc)
        #     # if band in configuration["ssid_modes"][enc]["appliedRadios"]:
        #     print(configuration["ssid_modes"][enc])
        logging.info("Setting up the DUT for Configuration: ")
        return 0

    def get_dut_version(self):
        pass

    def get_controller_version(self):
        pass

    # def get_controller_logs(self):
    #     pass
    #
    # def setup_configuration(self):
    #     pass


if __name__ == '__main__':
    basic_1 = {
        "target": "tip_2x",
        "controller": {
            "url": "https://sec-qa01.cicd.lab.wlan.tip.build:16001",
            "username": "tip@ucentral.com",
            "password": "OpenWifi%123"
        },
        "device_under_tests": [{
            "model": "wallys_dr40x9",
            "mode": "wifi5",
            "serial": "c44bd1005b30",
            "jumphost": True,
            "ip": "10.28.3.100",
            "username": "lanforge",
            "password": "pumpkin77",
            "port": 22,
            "serial_tty": "/dev/ttyAP8",
            "version": "next-latest"
        }],
        "traffic_generator": {}
    }
    var = tip_2x(controller_data=basic_1["controller"],
                 device_under_tests_info=basic_1["device_under_tests"],
                 target=basic_1["target"])
    setup_params_general = {
        "mode": "BRIDGE",
        "ssid_modes": {
            "open": [{"ssid_name": "ssid_open_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
                     {"ssid_name": "ssid_open_5g_br", "appliedRadios": ["5G"],
                      "security_key": "something"}],
            "wpa": [{"ssid_name": "ssid_wpa_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
                    {"ssid_name": "ssid_wpa_5g_br", "appliedRadios": ["5G"],
                     "security_key": "something"}],
            "wpa2_personal": [
                {"ssid_name": "ssid_wpa2_2g_br", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid_wpa2_5g_br", "appliedRadios": ["5G"],
                 "security_key": "something"}]},
        "rf": {"2G": {}, "5G": {}, "6G": {}},
        "radius": False
    }
    target = [['2G', 'wpa'], ['5G', 'open'], ['5G', 'wpa']]
    var.setup_configuration(configuration=setup_params_general, requested_combination=target)
