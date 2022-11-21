#!/usr/bin/env python3
import sys
import os
import importlib
from pprint import pprint
from pprint import pformat
import time
import logging

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFRequest = importlib.import_module("py-json.LANforge.LFRequest")
add_vap = importlib.import_module("py-json.LANforge.add_vap")
set_port = importlib.import_module("py-json.LANforge.set_port")
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
logger = logging.getLogger(__name__)

class VAPProfile(LFCliBase):
    def __init__(self, lfclient_host, lfclient_port, local_realm,
                 vap_name="",
                 ssid="NA",
                 ssid_pass="NA",
                 mode=0,
                 debug_=False):
        super().__init__(_lfjson_host=lfclient_host, _lfjson_port=lfclient_port, _debug=debug_)
        self.debug = debug_
        # self.lfclient_url = lfclient_url # done in super()
        self.ssid = ssid
        self.ssid_pass = ssid_pass
        self.mode = mode
        self.local_realm = local_realm
        self.vap_name = vap_name
        self.COMMANDS = ["add_vap", "set_port"]
        self.desired_add_vap_flags = ["wpa2_enable", "80211u_enable", "create_admin_down"]
        self.desired_add_vap_flags_mask = ["wpa2_enable", "80211u_enable", "create_admin_down"]
        self.shelf = 1
        self.resource = 1

        self.add_vap_data = {
            "shelf": self.shelf,
            "resource": self.resource,
            "radio": None,
            "ap_name": None,
            "flags": 0,
            "flags_mask": 0,
            "mode": 0,
            "ssid": None,
            "key": None,
            "mac": "xx:xx:xx:xx:*:xx"
        }

        self.desired_set_port_cmd_flags = []
        self.desired_set_port_current_flags = ["if_down"]
        self.desired_set_port_interest_flags = ["current_flags", "ifdown"]
        self.set_port_data = {
            "shelf": self.shelf,
            "resource": self.resource,
            "port": None,
            "current_flags": 0,
            "interest": 0,  # (0x2 + 0x4000 + 0x800000)  # current, dhcp, down
        }
        self.wifi_extra_data_modified = False
        self.wifi_extra_data = {
            "shelf": self.shelf,
            "resource": self.resource,
            "port": None,
            "key_mgmt": None,
            "eap": None,
            "hessid": None,
            "identity": None,
            "password": None,
            "realm": None,
            "domain": None
        }

    def set_wifi_extra(self,
                       key_mgmt="WPA-EAP",
                       pairwise="DEFAULT",
                       group="DEFAULT",
                       psk="[BLANK]",
                       eap="TTLS",
                       identity="testuser",
                       passwd="testpasswd",
                       realm="localhost.localdomain",
                       domain="localhost.localdomain",
                       hessid="00:00:00:00:00:01"):
        self.wifi_extra_data_modified = True
        self.wifi_extra_data["key_mgmt"] = key_mgmt
        self.wifi_extra_data["eap"] = eap
        self.wifi_extra_data["identity"] = identity
        self.wifi_extra_data["password"] = passwd
        self.wifi_extra_data["realm"] = realm
        self.wifi_extra_data["domain"] = domain
        self.wifi_extra_data["hessid"] = hessid

    # TODO:  remove 'resource' so we can just use EIDs
    def admin_up(self, resource):
        eid = "%s.%s.%s" % (1, resource, LFUtils.name_to_eid(self.vap_name)[2])
        self.local_realm.admin_up(eid)

    def admin_down(self, resource):
        eid = "%s.%s.%s" % (1, resource, LFUtils.name_to_eid(self.vap_name)[2])
        self.local_realm.admin_down(eid)

    def use_security(self, security_type, ssid=None, passwd=None):
        types = {"wep": "wep_enable", "wpa": "wpa_enable", "wpa2": "wpa2_enable", "wpa3": "use-wpa3", "open": "[BLANK]"}
        self.add_vap_data["ssid"] = ssid
        if security_type in types.keys():
            if (ssid is None) or (ssid == ""):
                raise ValueError("use_security: %s requires ssid" % security_type)
            if (passwd is None) or (passwd == ""):
                raise ValueError("use_security: %s requires passphrase or [BLANK]" % security_type)
            for name in types.values():
                if name in self.desired_add_vap_flags and name in self.desired_add_vap_flags_mask:
                    self.desired_add_vap_flags.remove(name)
                    self.desired_add_vap_flags_mask.remove(name)
            if security_type != "open":
                self.desired_add_vap_flags.append(types[security_type])
                self.desired_add_vap_flags_mask.append(types[security_type])
            else:
                passwd = "[BLANK]"
            self.set_command_param("add_vap", "ssid", ssid)
            self.set_command_param("add_vap", "key", passwd)
            # unset any other security flag before setting our present flags
            if security_type == "wpa3":
                self.set_command_param("add_vap", "ieee80211w", 2)

    def set_command_flag(self, command_name, param_name, value):
        # we have to check what the param name is
        if (command_name is None) or (command_name == ""):
            return
        if (param_name is None) or (param_name == ""):
            return
        if command_name not in self.COMMANDS:
            print("Command name name [%s] not defined in %s" % (command_name, self.COMMANDS))
            return
        if command_name == "add_vap":
            if param_name not in add_vap.add_vap_flags:
                print("Parameter name [%s] not defined in add_vap.py" % param_name)
                if self.debug:
                    pprint(add_vap.add_vap_flags)
                return
            if (value == 1) and (param_name not in self.desired_add_vap_flags):
                self.desired_add_vap_flags.append(param_name)
                self.desired_add_vap_flags_mask.append(param_name)
            elif value == 0:
                self.desired_add_vap_flags.remove(param_name)
                self.desired_add_vap_flags_mask.append(param_name)

        elif command_name == "set_port":
            if (param_name not in set_port.set_port_current_flags) and (
                    param_name not in set_port.set_port_cmd_flags) and (
                    param_name not in set_port.set_port_interest_flags):
                print("Parameter name [%s] not defined in set_port.py" % param_name)
                if self.debug:
                    pprint(set_port.set_port_cmd_flags)
                    pprint(set_port.set_port_current_flags)
                    pprint(set_port.set_port_interest_flags)
                return
            if param_name in set_port.set_port_cmd_flags:
                if (value == 1) and (param_name not in self.desired_set_port_cmd_flags):
                    self.desired_set_port_cmd_flags.append(param_name)
                elif value == 0:
                    self.desired_set_port_cmd_flags.remove(param_name)
            elif param_name in set_port.set_port_current_flags:
                if (value == 1) and (param_name not in self.desired_set_port_current_flags):
                    self.desired_set_port_current_flags.append(param_name)
                elif value == 0:
                    self.desired_set_port_current_flags.remove(param_name)
            elif param_name in set_port.set_port_interest_flags:
                if (value == 1) and (param_name not in self.desired_set_port_interest_flags):
                    self.desired_set_port_interest_flags.append(param_name)
                elif value == 0:
                    self.desired_set_port_interest_flags.remove(param_name)
            else:
                raise ValueError("Unknown param name: " + param_name)

    def set_command_param(self, command_name, param_name, param_value):
        # we have to check what the param name is
        if (command_name is None) or (command_name == ""):
            return
        if (param_name is None) or (param_name == ""):
            return
        if command_name not in self.COMMANDS:
            self.error("Command name name [%s] not defined in %s" % (command_name, self.COMMANDS))
            return
        if command_name == "add_vap":
            self.add_vap_data[param_name] = param_value
        elif command_name == "set_port":
            self.set_port_data[param_name] = param_value

    def add_named_flags(self, desired_list, command_ref):
        if desired_list is None:
            raise ValueError("addNamedFlags wants a list of desired flag names")
        if len(desired_list) < 1:
            logger.info("addNamedFlags: empty desired list")
            return 0
        if (command_ref is None) or (len(command_ref) < 1):
            raise ValueError("addNamedFlags wants a maps of flag values")

        result = 0
        for name in desired_list:
            if (name is None) or (name == ""):
                continue
            if name not in command_ref:
                if self.debug:
                    pprint(command_ref)
                raise ValueError("flag %s not in map" % name)
            # print("add-named-flags: %s  %i"%(name, command_ref[name]))
            result |= command_ref[name]

        return result

    # NOTE:  This method does not have enough knowledge of desired setup to build or modify
    # a bridge, so work-flow would be to create vap, then create bridge to hold the VAP.
    def create(self, resource, radio, channel=None, up=False, debug=False, use_ht40=True, use_ht80=True,
               use_ht160=False,
               suppress_related_commands_=True, use_radius=False, hs20_enable=False):
        eid = LFUtils.name_to_eid(radio)
        self.shelf = eid[0]
        self.resource = eid[1]
        radio = eid[2]

        if resource:
            self.resource = resource
        resource = self.resource

        # Removes port if it exists already.
        # TODO:  Make this optional, that way this profile could modify existing VAP in place.
        port_list = self.local_realm.json_get("port/1/%s/list" % (resource))
        if port_list is not None:
            port_list = port_list['interfaces']
            for port in port_list:
                for k, v in port.items():
                    if v['alias'] == LFUtils.name_to_eid(self.vap_name)[2]:
                        self.local_realm.rm_port(k, check_exists=False)

        if use_ht160:
            self.desired_add_vap_flags.append("enable_80211d")
            self.desired_add_vap_flags_mask.append("enable_80211d")
            self.desired_add_vap_flags.append("80211h_enable")
            self.desired_add_vap_flags_mask.append("80211h_enable")
            self.desired_add_vap_flags.append("ht160_enable")
            self.desired_add_vap_flags_mask.append("ht160_enable")
        if not use_ht40:
            self.desired_add_vap_flags.append("disable_ht40")
            self.desired_add_vap_flags_mask.append("disable_ht40")
        if not use_ht80:
            self.desired_add_vap_flags.append("disable_ht80")
            self.desired_add_vap_flags_mask.append("disable_ht80")
        if use_radius:
            self.desired_add_vap_flags.append("8021x_radius")
            self.desired_add_vap_flags_mask.append("8021x_radius")
        if hs20_enable:
            self.desired_add_vap_flags.append("hs20_enable")
            self.desired_add_vap_flags_mask.append("hs20_enable")

        # print("MODE ========= ", self.mode)

        jr = self.local_realm.json_get("/radiostatus/1/%s/%s?fields=channel,frequency,country" % (self.resource, radio),
                                       debug_=self.debug)
        if jr is None:
            raise ValueError("No radio %s.%s found" % (self.resource, radio))

        eid_2 = "1.%s.%s" % (self.resource, radio)
        country = 0
        if eid_2 in jr:
            country = jr[eid_2]["country"]

        data = {
            "shelf": self.shelf,
            "resource": self.resource,
            "radio": radio,
            "mode": self.mode,  # "NA", #0 for AUTO or "NA"
            "channel": channel,
            "country": country,
            "frequency": self.local_realm.channel_freq(channel_=channel)
        }
        self.local_realm.json_post("/cli-json/set_wifi_radio", _data=data)
        if up:
            if "create_admin_down" in self.desired_add_vap_flags:
                del self.desired_add_vap_flags[self.desired_add_vap_flags.index("create_admin_down")]
        elif "create_admin_down" not in self.desired_add_vap_flags:
            self.desired_add_vap_flags.append("create_admin_down")

        # create vaps down, do set_port on them, then set vaps up
        self.add_vap_data["mode"] = self.mode
        self.add_vap_data["flags"] = self.add_named_flags(self.desired_add_vap_flags, add_vap.add_vap_flags)
        self.add_vap_data["flags_mask"] = self.add_named_flags(self.desired_add_vap_flags_mask, add_vap.add_vap_flags)
        self.add_vap_data["radio"] = radio
        # TODO: add_vap_data should not hold shelf and resource; duplicate
        self.add_vap_data["resource"] = resource
        self.set_port_data["current_flags"] = self.add_named_flags(self.desired_set_port_current_flags,
                                                                   set_port.set_port_current_flags)
        self.set_port_data["interest"] = self.add_named_flags(self.desired_set_port_interest_flags,
                                                              set_port.set_port_interest_flags)
        # these are unactivated LFRequest objects that we can modify and
        # re-use inside a loop, reducing the number of object creations
        add_vap_r = LFRequest.LFRequest(self.lfclient_url + "/cli-json/add_vap")
        set_port_r = LFRequest.LFRequest(self.lfclient_url + "/cli-json/set_port")
        wifi_extra_r = LFRequest.LFRequest(self.lfclient_url + "/cli-json/set_wifi_extra")
        if suppress_related_commands_:
            self.add_vap_data["suppress_preexec_cli"] = "yes"
            self.add_vap_data["suppress_preexec_method"] = 1
            self.set_port_data["suppress_preexec_cli"] = "yes"
            self.set_port_data["suppress_preexec_method"] = 1

        # pprint(self.station_names)
        # exit(1)
        self.set_port_data["port"] = LFUtils.name_to_eid(self.vap_name)[2]
        self.add_vap_data["ap_name"] = LFUtils.name_to_eid(self.vap_name)[2]
        add_vap_r.addPostData(self.add_vap_data)
        if debug:
            print("- 1502 - %s- - - - - - - - - - - - - - - - - - " % self.vap_name)
            pprint(self.add_vap_data)
            pprint(self.set_port_data)
            pprint(add_vap_r)
            print("- ~1502 - - - - - - - - - - - - - - - - - - - ")

        add_vap_r.jsonPost(debug)
        set_port_r.addPostData(self.set_port_data)
        set_port_r.jsonPost(debug)

        self.wifi_extra_data["resource"] = resource
        self.wifi_extra_data["port"] = LFUtils.name_to_eid(self.vap_name)[2]
        if self.wifi_extra_data_modified:
            wifi_extra_r.addPostData(self.wifi_extra_data)
            wifi_extra_r.jsonPost(debug)

        desired_ports = ["1.%s.%s" % (resource, LFUtils.name_to_eid(self.vap_name)[2])]
        if LFUtils.wait_until_ports_appear(base_url=self.lfclient_url, port_list=desired_ports, debug=debug):
            if up:
                self.admin_up(resource)
            
                if LFUtils.wait_until_ports_admin_up(base_url=self.lfclient_url, port_list=desired_ports, debug_=debug):
                    return True
                else:
                    return False # Ports did not go admin up
            else:
                return True # We are not trying to admin them up
        else:
            return False # Ports did not appear
            
    def modify(self, radio):
        self.add_vap_data["flags"] = self.add_named_flags(self.desired_add_vap_flags, add_vap.add_vap_flags)
        self.add_vap_data["flags_mask"] = self.add_named_flags(self.desired_add_vap_flags_mask, add_vap.add_vap_flags)
        self.add_vap_data["radio"] = radio
        self.add_vap_data["ap_name"] = self.vap_name
        self.add_vap_data["ssid"] = 'NA'
        self.add_vap_data["key"] = 'NA'
        self.add_vap_data['mac'] = self.mac
        # self.add_vap_data['mac'] = 'NA'

        add_vap_r = LFRequest.LFRequest(self.lfclient_url + "/cli-json/add_vap", debug_=self.debug)
        logger.debug(self.add_vap_data)
        add_vap_r.addPostData(self.add_vap_data)
        # inputs to jsonPost self, show_error=True, debug=False, die_on_error_=False, response_json_list_=None, method_='POST'
        json_response = add_vap_r.jsonPost(show_error=True, debug=self.debug)
        return json_response

    def cleanup(self, resource):
        print("Cleaning up VAP")

        desired_ports = ["1.%s.%s" % (resource, LFUtils.name_to_eid(self.vap_name)[2])]

        # First, request remove on the list.
        for port_eid in desired_ports:
            self.local_realm.rm_port(port_eid, check_exists=True)

        # And now see if they are gone
        return LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=desired_ports)
