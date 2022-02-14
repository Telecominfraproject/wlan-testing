#!/usr/bin/env python3
import sys
import os
import importlib
from pprint import pprint
from pprint import pformat
import base64
import logging


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
add_dut = importlib.import_module("py-json.LANforge.add_dut")

logger = logging.getLogger(__name__)


class DUTProfile(LFCliBase):
    def __init__(self, lfclient_host, lfclient_port, local_realm, debug_=False):
        super().__init__(lfclient_host, lfclient_port, debug_, _local_realm=local_realm)
        self.name = "NA"
        self.flags = "NA"
        self.img_file = "NA"
        self.sw_version = "NA"
        self.hw_version = "NA"
        self.model_num = "NA"
        self.serial_num = "NA"
        self.serial_port = "NA"
        self.wan_port = "NA"
        self.lan_port = "NA"
        self.ssid1 = "NA"
        self.ssid2 = "NA"
        self.ssid3 = "NA"
        self.passwd1 = "NA"
        self.passwd2 = "NA"
        self.passwd3 = "NA"
        self.mgt_ip = "NA"
        self.api_id = "NA"
        self.flags_mask = "NA"
        self.antenna_count1 = "NA"
        self.antenna_count2 = "NA"
        self.antenna_count3 = "NA"
        self.bssid1 = "NA"
        self.bssid2 = "NA"
        self.bssid3 = "NA"
        self.top_left_x = "NA"
        self.top_left_y = "NA"
        self.eap_id = "NA"
        self.flags = 0
        self.flags_mask = 0
        self.notes = []
        self.append = []

    def set_param(self, name, value):
        if name in self.__dict__:
            self.__dict__[name] = value

    def create(self, name=None, flags=None, flags_mask=None):
        data = {}
        if (name is not None) and (name != ""):
            data["name"] = name
        elif (self.name is not None) and (self.name != ""):
            data["name"] = self.name
        else:
            logger.critical("cannot create/update DUT record lacking a name")
            raise ValueError("cannot create/update DUT record lacking a name")

        for param in add_dut.dut_params:
            if param.name in self.__dict__:
                if (self.__dict__[param.name] is not None) \
                        and (self.__dict__[param.name] != "NA"):
                    data[param.name] = self.__dict__[param.name]
            else:
                logger.error("---------------------------------------------------------")
                logger.error(pformat(self.__dict__[param.name]))
                logger.error("---------------------------------------------------------")
                logger.critical("parameter %s not in dut_profile" % param)
                raise ValueError("parameter %s not in dut_profile" % param)

        if (flags is not None) and (int(flags) > -1):
            data["flags"] = flags
        elif (self.flags is not None) and (self.flags > -1):
            data["flags"] = self.flags

        if (flags_mask is not None) and (int(flags_mask) > -1):
            data["flags_mask"] = flags_mask
        elif (self.flags_mask is not None) and (int(self.flags_mask) > -1):
            data["flags_mask"] = self.flags_mask

        url = "/cli-json/add_dut"
        if self.debug:
            logger.debug("---- DATA -----------------------------------------------")
            logger.debug(pformat(data))
            logger.debug(pformat(self.notes))
            logger.debug(pformat(self.append))
            logger.debug("---------------------------------------------------------")
        self.json_post(url, data, debug_=self.debug)

        if (self.notes is not None) and (len(self.notes) > 0):
            self.json_post("/cli-json/add_dut_notes", {
                "dut": self.name,
                "text": "[BLANK]"
            }, self.debug)
            for line in self.notes:
                notebytes = base64.b64encode(line.encode('ascii'))
                if self.debug:
                    logger.debug("------ NOTES ---------------------------------------------------")
                    logger.debug(pformat(self.notes))
                    logger.debug(pformat(str(notebytes)))
                    logger.debug("---------------------------------------------------------")
                self.json_post("/cli-json/add_dut_notes", {
                    "dut": self.name,
                    "text-64": notebytes.decode('ascii')
                }, self.debug)
        if (self.append is not None) and (len(self.append) > 0):
            for line in self.append:
                notebytes = base64.b64encode(line.encode('ascii'))
                if self.debug:
                    logger.debug("----- APPEND ----------------------------------------------------")
                    logger.debug(pformat(line))
                    logger.debug(pformat(str(notebytes)))
                    logger.debug("---------------------------------------------------------")
                self.json_post("/cli-json/add_dut_notes", {
                    "dut": self.name,
                    "text-64": notebytes.decode('ascii')
                }, self.debug)
