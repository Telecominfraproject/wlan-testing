"""
    Telecom Infra Project OpenWifi 2.X (Ucentral libraries for Test Automation)


"""
import importlib

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
    dut_library_object = object()

    def __init__(self, controller_data=None, target=None,
                 device_under_tests_info=[], logging_level=logging.INFO):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging_level)
        if target != self.target:
            logging.error("Target version is : " + target + " Expected target is tip_2x.")
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
        self.controller_library_object = Controller()
        self.dut_library_object = APLIBS()

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

    def setup_configuration(self):
        pass

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
    var = tip_2x(controller_data=basic_1["controller"], device_under_tests_info=basic_1["device_under_tests"])
