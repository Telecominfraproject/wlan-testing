#!/usr/bin/env python3
import sys
import os
import importlib
import time
import logging


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFRequest = importlib.import_module("py-json.LANforge.LFRequest")
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
logger = logging.getLogger(__name__)


class ATTENUATORProfile(LFCliBase):
    def __init__(self, lfclient_host, lfclient_port, debug_=False):
        super().__init__(lfclient_host, lfclient_port, debug_)
        self.lfclient_host = lfclient_host
        self.COMMANDS = ["show_attenuators", "set_attenuator"]
        self.atten_serno = None
        self.atten_idx = None
        self.atten_val = None
        self.atten_data = {
            "shelf": 1,
            "resource": 1,
            "serno": self.atten_serno,
            "atten_idx": self.atten_idx,
            "val": self.atten_val,
            "mode": None,
            "pulse_width_us5": None,
            "pulse_interval_ms": None,
            "pulse_count": None,
            "pulse_time_ms": None
        }
        self.debug = debug_

    def set_command_param(self, command_name, param_name, param_value):
        # we have to check what the param name is
        if not command_name:
            raise ValueError("Command Name is required")
        if not param_name:
            raise ValueError("Paramater is required")
        if command_name not in self.COMMANDS:
            raise ValueError("Command name name [%s] not defined in %s" % (command_name, self.COMMANDS))
        if command_name == "set_attenuator":
            self.atten_data[param_name] = param_value

    def show(self):
        logger.info("Show Attenuators.........")
        response = self.json_get("/attenuators/")
        time.sleep(0.01)
        if response is None:
            logger.critical(response)
            logger.critical("Cannot find any endpoints")
            raise ValueError("Cannot find any endpoints")
        elif 'attenuator' or 'attenuators' in response.keys():
            try:
                attenuator_resp = response["attenuators"]
            except KeyError:
                attenuator_resp = [response["attenuator"]]
            for attenuator in attenuator_resp:
                for key, val in attenuator.items():
                    if key == "entity id":
                        serial_num = val.split(".")
                        logger.info("Serial-num : %s" % serial_num[-1])
                    logger.info("%s : %s" % (key, val))

        else:
            logger.critical('No attenuators in response')
            raise ValueError('No attenuators in response')

    def create(self):
        if self.atten_idx == 'all':
            self.atten_idx = 8
        if int(self.atten_val) > 955:
            logger.critical("Attenuation ddB value must be 955 or less")
            raise ValueError("Attenuation ddB value must be 955 or less")
        if int(self.atten_idx) > 7:
            logger.critical("Attenuation idx value must be 7 or less")
            raise ValueError("Attenuation idx value must be 7 or less")
        logger.info("Setting Attenuator...")
        self.set_command_param("set_attenuator", "serno", self.atten_serno)
        self.set_command_param("set_attenuator", "atten_idx", self.atten_idx)
        self.set_command_param("set_attenuator", "val", self.atten_val)
        set_attenuators = LFRequest.LFRequest(self.lfclient_url + "/cli-json/set_attenuator", debug_=self.debug)
        set_attenuators.addPostData(self.atten_data)
        time.sleep(0.01)
        set_attenuators.jsonPost(self.debug)
        time.sleep(10)
        print("\n")
