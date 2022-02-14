#!/usr/bin/env python3
"""
Base Class to be used for Chamber View Tests

Methods:
    1.) Add a CV Profile
    2.) Remove a CV Profile
    3.) Add a DUT
    4.) Show a CV Profile
"""
import sys
import os
import importlib

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase


class ChamberViewBase(LFCliBase):

    def __init__(self, _lfjson_host="localhost", _lfjson_port=8080, _debug=False):
        super().__init__(_lfjson_host=_lfjson_host, _lfjson_port=_lfjson_port, _debug=_debug)

    def remove_text_blobs(self):
        pass

    def add_text_blobs(self, text_type="", name="", data="", debug=False):
        data = {'type': text_type,
                'name': name,
                "text": data
                }
        self.json_post("/cli-json/add_text_blob/", data, debug_=debug)

    def get_text_blob(self, text_type="", name="", debug=False):
        data = {'type': text_type,
                'name': name,
                }
        return self.json_post("/cli-json/show_text_blob/", data, debug_=debug)

    def add_dut(self):
        """
        //for DUT

            /cli-json/add_dut

            (
            {
            "name": Dut name which we want to give,
            "flags": "4098",
            "img_file" : "NONE",
            "sw_version" : "[BLANK]",
            "hw_version": "[BLANK]",
            "model_num":"[BLANK]",
            "serial_num":"[BLANK]",
            "serial_port":"[BLANK]",
            "wan_port":"[BLANK]",
            "lan_port": "[BLANK]",
            "ssid1": SSIDname1,
            "passwd1": SSIDpassword1,
            "ssid2": SSIDname2,
            "passwd2": SSIDpassword2,
            "ssid3":"[BLANK]",
            "passwd3" :"[BLANK]",
            "mgt_ip" : "0.0.0.0",
            "api_id": "0",
            "flags_mask" : "NA",
            "antenna_count1" : "0",
            "antenna_count2":"0",
            "antenna_count3":"0",
            "bssid1" : "00:00:00:00:00:00",
            "bssid2" : "00:00:00:00:00:00",
            "bssid3" : "00:00:00:00:00:00",
            "top_left_x": "0",
            "top_left_y": "0",
            "eap_id": "[BLANK]",
            }
            )
        """
        pass
