#!/usr/bin/env python3

import sys
import os
import importlib
import time

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
add_monitor = importlib.import_module("py-json.LANforge.add_monitor")
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
set_wifi_radio = importlib.import_module("py-json.LANforge.set_wifi_radio")
set_radio_mode = set_wifi_radio.set_radio_mode


class WifiMonitor:
    def __init__(self, lfclient_url, local_realm, up=True, debug_=False, resource_=1):
        self.debug = debug_
        self.lfclient_url = lfclient_url
        self.up = up
        self.local_realm = local_realm
        self.monitor_name = None
        self.resource = resource_
        self.flag_names = []
        self.flag_mask_names = []
        self.flags_mask = add_monitor.default_flags_mask
        self.aid = "NA"  # used when sniffing /ax radios
        self.bssid = "00:00:00:00:00:00"  # used when sniffing on /ax radios

    def create(self, resource_=1, channel=None, mode="AUTO", radio_="wiphy0", name_="moni0"):
        radio_eid = self.local_realm.name_to_eid(radio_)
        radio_shelf = radio_eid[0]
        self.resource = radio_eid[1]
        radio_ = radio_eid[2]
        print("Creating monitor " + name_)
        self.monitor_name = name_
        computed_flags = 0
        for flag_n in self.flag_names:
            computed_flags += add_monitor.flags[flag_n]

        # we want to query the existing country code of the radio
        # there's no reason to change it but we get hollering from server
        # if we don't provide a value for the parameter
        jr = self.local_realm.json_get("/radiostatus/1/%s/%s?fields=channel,frequency,country" % (self.resource, radio_),
                                       debug_=self.debug)
        if jr is None:
            raise ValueError("No radio %s.%s found" % (self.resource, radio_))

        # frequency = 0
        country = 0
        if radio_ in jr:
            country = jr[radio_]["country"]

        data = {
            "shelf": radio_shelf,
            "resource": self.resource,
            "radio": radio_,
            "mode": set_radio_mode[mode],  # "NA", #0 for AUTO or "NA"
            "channel": channel,
            "country": country,
            "frequency": self.local_realm.channel_freq(channel_=channel)

        }
        self.local_realm.json_post("/cli-json/set_wifi_radio", _data=data)
        time.sleep(1)
        self.local_realm.json_post("/cli-json/add_monitor", {
            "shelf": radio_shelf,
            "resource": self.resource,
            "radio": radio_,
            "ap_name": self.monitor_name,
            "flags": computed_flags,
            "flags_mask": self.flags_mask
        })

    def set_flag(self, param_name, value):
        if param_name not in add_monitor.flags:
            raise ValueError("Flag '%s' does not exist for add_monitor, consult add_monitor.py" % param_name)
        if (value == 1) and (param_name not in self.flag_names):
            self.flag_names.append(param_name)
        elif (value == 0) and (param_name in self.flag_names):
            del self.flag_names[param_name]
            self.flags_mask |= add_monitor.flags[param_name]

    def cleanup(self, desired_ports=None):
        print("Cleaning up monitors")
        if (desired_ports is None) or (len(desired_ports) < 1):
            if (self.monitor_name is None) or (self.monitor_name == ""):
                print("No monitor name set to delete")
                return
            LFUtils.removePort(resource=self.resource,
                               port_name=self.monitor_name,
                               baseurl=self.lfclient_url,
                               debug=self.debug)
        else:
            names = ",".join(desired_ports)
            existing_ports = self.local_realm.json_get("/port/1/%d/%s?fields=alias" % (self.resource, names), debug_=False)
            if (existing_ports is None) or ("interfaces" not in existing_ports) or ("interface" not in existing_ports):
                print("No monitor names found to delete")
                return
            if "interfaces" in existing_ports:
                for eid, info in existing_ports["interfaces"].items():
                    LFUtils.removePort(resource=self.resource,
                                       port_name=info["alias"],
                                       baseurl=self.lfclient_url,
                                       debug=self.debug)
            if "interface" in existing_ports:
                for eid, info in existing_ports["interface"].items():
                    LFUtils.removePort(resource=self.resource,
                                       port_name=info["alias"],
                                       baseurl=self.lfclient_url,
                                       debug=self.debug)

    def admin_up(self):
        up_request = LFUtils.port_up_request(resource_id=self.resource, port_name=self.monitor_name)
        self.local_realm.json_post("/cli-json/set_port", up_request)
        self.local_realm.json_post("/cli-json/set_port", up_request)

    def admin_down(self):
        down_request = LFUtils.portDownRequest(resource_id=self.resource, port_name=self.monitor_name)
        self.local_realm.json_post("/cli-json/set_port", down_request)

    def start_sniff(self, capname=None, duration_sec=60):
        if capname is None:
            raise ValueError("Need a capture file name")
        data = {
            "shelf": 1,
            "resource": self.resource,
            "port": self.monitor_name,
            "display": "NA",
            "flags": 0x2,
            "outfile": capname,
            "duration": duration_sec
        }
        self.local_realm.json_post("/cli-json/sniff_port", _data=data)
