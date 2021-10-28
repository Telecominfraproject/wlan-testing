# !/usr/bin/env python3
import sys
import os
import importlib

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
add_dut = importlib.import_module("py-json.LANforge.add_dut")
add_dut_flags = add_dut.add_dut_flags


class cv_dut(LFCliBase):
    def __init__(self,
                 lfclient_host="localhost",
                 lfclient_port=8080,
                 sw_version="NA",
                 hw_version="NA",
                 serial_num="NA",
                 model_num="NA",
                 desired_dut_flags=None,
                 desired_dut_flags_mask=None
                 ):
        super().__init__(_lfjson_host=lfclient_host,
                         _lfjson_port=lfclient_port)
        self.cv_dut_name = "DUT"
        self.flags = "4098"
        self.sw_version = sw_version
        self.hw_version = hw_version
        self.model_num = model_num
        self.serial_num = serial_num
        self.serial_port = "[BLANK]"
        self.wan_port = "[BLANK]"
        self.lan_port = "[BLANK]"
        self.api_id = "0"
        self.flags_mask = "NA"
        if desired_dut_flags is not None:
            self.dut_flags = desired_dut_flags
            self.dut_flags_mask = desired_dut_flags_mask

    def add_named_flags(self, desired_list, command_ref):
        if desired_list is None:
            raise ValueError("addNamedFlags wants a list of desired flag names")
        if len(desired_list) < 1:
            print("addNamedFlags: empty desired list")
            return 0
        if (command_ref is None) or (len(command_ref) < 1):
            raise ValueError("addNamedFlags wants a maps of flag values")

        result = 0
        for name in desired_list:
            if (name is None) or (name == ""):
                continue
            if name not in command_ref:
                if self.debug:
                    print(command_ref)
                raise ValueError("flag %s not in map" % name)
            result += command_ref[name]

        return result

    def create_dut(self,
                   ssid1="[BLANK]",
                   pass1="[BLANK]",
                   ssid2="[BLANK]",
                   pass2="[BLANK]",
                   ssid3="[BLANK]",
                   pass3="[BLANK]",
                   bssid1="00:00:00:00:00:00",
                   bssid2="00:00:00:00:00:00",
                   bssid3="00:00:00:00:00:00",
                   mgt_ip="0.0.0.0",
                   eap_id="[BLANK]",
                   top_left_x="NA",
                   top_left_y="NA",
                   ):
        try:
            self.flags = self.add_named_flags(self.dut_flags, add_dut_flags)
            self.flags_mask = self.add_named_flags(self.dut_flags_mask, add_dut_flags)
        except:
            pass
        response_json = []
        req_url = "/cli-json/add_dut"
        data = {
            "name": self.cv_dut_name,
            "flags": self.flags,
            "img_file": "NONE",
            "sw_version": self.sw_version,
            "hw_version": self.hw_version,
            "model_num": self.model_num,
            "serial_num": self.serial_num,
            "serial_port": self.serial_port,
            "wan_port": self.wan_port,
            "lan_port": self.lan_port,
            "ssid1": ssid1,
            "passwd1": pass1,
            "ssid2": ssid2,
            "passwd2": pass2,
            "ssid3": ssid3,
            "passwd3": pass3,
            "mgt_ip": mgt_ip,
            "api_id": self.api_id,
            "flags_mask": self.flags_mask,
            "antenna_count1": "0",
            "antenna_count2": "0",
            "antenna_count3": "0",
            "bssid1": bssid1,
            "bssid2": bssid2,
            "bssid3": bssid3,
            "top_left_x": top_left_x,
            "top_left_y": top_left_y,
            "eap_id": eap_id,
        }
        rsp = self.json_post(req_url, data, debug_=False, response_json_list_=response_json)
        return rsp

    def add_ssid(self,
                 dut_name="DUT",
                 ssid_idx=0,
                 ssid='[BLANK]',
                 passwd='[BLANK]',
                 bssid='00:00:00:00:00:00',
                 ssid_flags=0,
                 ssid_flags_mask=0xFFFFFFFF):
        req_url = "/cli-json/add_dut_ssid"
        print("name:" + dut_name,
              "ssid_idx:" + ssid_idx,
              "ssid:" + ssid,
              "passwd:" + passwd,
              "bssid:" + bssid,
              "ssid_flags:" + str(ssid_flags),
              "ssid_flags_mask:" + str(ssid_flags_mask))

        self.json_post(req_url, {
            "name": dut_name,
            "ssid_idx": ssid_idx,
            "ssid": ssid,
            "passwd": passwd,
            "bssid": bssid,
            "ssid_flags": ssid_flags,
            "ssid_flags_mask": ssid_flags_mask,
        })
