# !/usr/bin/env python3
import sys
import os
import importlib
from pprint import pprint
import time

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFRequest = importlib.import_module("py-json.LANforge.LFRequest")
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
set_port = importlib.import_module("py-json.LANforge.set_port")
add_sta = importlib.import_module("py-json.LANforge.add_sta")


# Uncomment below to include autogen library.
# if os.environ.get("LF_USE_AUTOGEN") == 1:
#         lf_json_autogen = importlib.import_module("py-json.LANforge.lf_json_autogen")
#         LFJsonPost = jf_json_autogen.LFJsonPost

# use the station profile to set the combination of features you want on your stations
# once this combination is configured, build the stations with the build(resource, radio, number) call
# build() calls will fail if the station already exists. Please survey and clean your resource
# before calling build()
#         realm = importlib.import_module("py-json.realm")
#         Realm = realm.Realm
#         survey = Realm.findStations(resource=1)
#         Realm.removeStations(survey)
#         profile = Realm.newStationProfile()
#         profile.set...
#         profile.build(resource, radio, 64)


class StationProfile:
    def __init__(self, lfclient_url, local_realm,
                 ssid="NA",
                 ssid_pass="NA",
                 security="open",
                 number_template_="00000",
                 mode=0,
                 up=True,
                 resource=1,
                 shelf=1,
                 dhcp=True,
                 debug_=False,
                 use_ht160=False):
        self.debug = debug_
        self.lfclient_url = lfclient_url
        self.ssid = ssid
        self.ssid_pass = ssid_pass
        self.mode = mode
        self.up = up
        self.resource = resource
        self.shelf = shelf
        self.dhcp = dhcp
        self.security = security
        self.local_realm = local_realm
        self.use_ht160 = use_ht160
        self.COMMANDS = ["add_sta", "set_port"]
        self.desired_add_sta_flags = ["wpa2_enable", "80211u_enable", "create_admin_down"]
        self.desired_add_sta_flags_mask = ["wpa2_enable", "80211u_enable", "create_admin_down"]
        self.number_template = number_template_
        self.station_names = []  # eids, these are created station names
        self.add_sta_data = {
            "shelf": 1,
            "resource": 1,
            "radio": None,
            "sta_name": None,
            "ssid": None,
            "key": None,
            "mode": 0,
            "mac": "xx:xx:xx:xx:*:xx",
            "flags": 0,  # (0x400 + 0x20000 + 0x1000000000)  # create admin down
            "flags_mask": 0
        }
        self.desired_set_port_cmd_flags = []
        self.desired_set_port_current_flags = ["if_down"]
        self.desired_set_port_interest_flags = ["current_flags", "ifdown"]
        if self.dhcp:
            self.desired_set_port_current_flags.append("use_dhcp")
            self.desired_set_port_interest_flags.append("dhcp")

        self.set_port_data = {
            "shelf": 1,
            "resource": 1,
            "port": None,
            "current_flags": 0,
            "interest": 0,  # (0x2 + 0x4000 + 0x800000)  # current, dhcp, down,
        }
        self.wifi_extra_data_modified = False
        self.wifi_extra_data = {
            "shelf": 1,
            "resource": 1,
            "port": None,
            "key_mgmt": None,
            "eap": None,
            "hessid": None,
            "identity": None,
            "password": None,
            "realm": None,
            "domain": None
        }
        self.wifi_txo_data_modified = False
        self.wifi_txo_data = {
            "shelf": 1,
            "resource": 1,
            "port": None,
            "txo_enable": None,
            "txo_txpower": None,
            "txo_pream": None,
            "txo_mcs": None,
            "txo_nss": None,
            "txo_bw": None,
            "txo_retries": None,
            "txo_sgi": None
        }

        self.reset_port_extra_data = {
            "shelf": 1,
            "resource": 1,
            "port": None,
            "test_duration": 0,
            "reset_port_enable": False,
            "reset_port_time_min": 0,
            "reset_port_time_max": 0,
            "reset_port_timer_started": False,
            "port_to_reset": 0,
            "seconds_till_reset": 0
        }

    def set_wifi_txo(self, txo_ena=1,
                     tx_power=255,
                     pream=0,
                     mcs=0,
                     nss=0,
                     bw=0,
                     retries=1,
                     sgi=0):
        self.wifi_txo_data_modified = True
        self.wifi_txo_data["txo_enable"] = txo_ena
        self.wifi_txo_data["txo_txpower"] = tx_power
        self.wifi_txo_data["txo_pream"] = pream
        self.wifi_txo_data["txo_mcs"] = mcs
        self.wifi_txo_data["txo_nss"] = nss
        self.wifi_txo_data["txo_bw"] = bw
        self.wifi_txo_data["txo_retries"] = retries
        self.wifi_txo_data["txo_sgi"] = sgi

    def set_wifi_extra(self, key_mgmt="WPA-EAP",
                       pairwise="CCMP TKIP",
                       group="CCMP TKIP",
                       psk="[BLANK]",
                       wep_key="[BLANK]",  # wep key
                       ca_cert="[BLANK]",
                       eap="TTLS",
                       identity="testuser",
                       anonymous_identity="[BLANK]",
                       phase1="NA",  # outter auth
                       phase2="NA",  # inner auth
                       passwd="testpasswd",  # eap passphrase
                       pin="NA",
                       pac_file="NA",
                       private_key="NA",
                       pk_password="NA",  # priv key password
                       hessid="00:00:00:00:00:01",
                       realm="localhost.localdomain",
                       client_cert="NA",
                       imsi="NA",
                       milenage="NA",
                       domain="localhost.localdomain",
                       roaming_consortium="NA",
                       venue_group="NA",
                       network_type="NA",
                       ipaddr_type_avail="NA",
                       network_auth_type="NA",
                       anqp_3gpp_cell_net="NA"
                       ):
        self.wifi_extra_data_modified = True
        self.wifi_extra_data["key_mgmt"] = key_mgmt
        self.wifi_extra_data["pairwise"] = pairwise
        self.wifi_extra_data["group"] = group
        self.wifi_extra_data["psk"] = psk
        self.wifi_extra_data["key"] = wep_key
        self.wifi_extra_data["ca_cert"] = ca_cert
        self.wifi_extra_data["eap"] = eap
        self.wifi_extra_data["identity"] = identity
        self.wifi_extra_data["anonymous_identity"] = anonymous_identity
        self.wifi_extra_data["phase1"] = phase1
        self.wifi_extra_data["phase2"] = phase2
        self.wifi_extra_data["password"] = passwd
        self.wifi_extra_data["pin"] = pin
        self.wifi_extra_data["pac_file"] = pac_file
        self.wifi_extra_data["private_key"] = private_key
        self.wifi_extra_data["pk_passwd"] = pk_password
        self.wifi_extra_data["hessid"] = hessid
        self.wifi_extra_data["realm"] = realm
        self.wifi_extra_data["client_cert"] = client_cert
        self.wifi_extra_data["imsi"] = imsi
        self.wifi_extra_data["milenage"] = milenage
        self.wifi_extra_data["domain"] = domain
        self.wifi_extra_data["roaming_consortium"] = roaming_consortium
        self.wifi_extra_data["venue_group"] = venue_group
        self.wifi_extra_data["network_type"] = network_type
        self.wifi_extra_data["ipaddr_type_avail"] = ipaddr_type_avail
        self.wifi_extra_data["network_auth_type"] = network_auth_type
        self.wifi_extra_data["anqp_3gpp_cell_net"] = anqp_3gpp_cell_net

    def set_reset_extra(self, reset_port_enable=False, test_duration=0, reset_port_min_time=0, reset_port_max_time=0,
                        reset_port_timer_start=False, port_to_reset=0, time_till_reset=0):
        self.reset_port_extra_data["reset_port_enable"] = reset_port_enable
        self.reset_port_extra_data["test_duration"] = test_duration
        self.reset_port_extra_data["reset_port_time_min"] = reset_port_min_time
        self.reset_port_extra_data["reset_port_time_max"] = reset_port_max_time

    def use_security(self, security_type, ssid=None, passwd=None):
        types = {"wep": "wep_enable", "wpa": "wpa_enable", "wpa2": "wpa2_enable", "wpa3": "use-wpa3", "open": "[BLANK]"}
        self.add_sta_data["ssid"] = ssid
        if security_type in types.keys():
            if (ssid is None) or (ssid == ""):
                raise ValueError("use_security: %s requires ssid" % security_type)
            if (passwd is None) or (passwd == ""):
                raise ValueError("use_security: %s requires passphrase or [BLANK]" % security_type)
            for name in types.values():
                if name in self.desired_add_sta_flags and name in self.desired_add_sta_flags_mask:
                    self.desired_add_sta_flags.remove(name)
                    self.desired_add_sta_flags_mask.remove(name)
            if security_type != "open":
                self.desired_add_sta_flags.append(types[security_type])
                # self.set_command_flag("add_sta", types[security_type], 1)
                self.desired_add_sta_flags_mask.append(types[security_type])
            else:
                passwd = "[BLANK]"
            self.set_command_param("add_sta", "ssid", ssid)
            self.set_command_param("add_sta", "key", passwd)
            # unset any other security flag before setting our present flags
            if security_type == "wpa3":
                self.set_command_param("add_sta", "ieee80211w", 2)
            # self.add_sta_data["key"] = passwd

    def station_mode_to_number(self, mode):
        modes = ['a', 'b', 'g', 'abg', 'an', 'abgn', 'bgn', 'bg', 'abgn-AC', 'bgn-AC', 'an-AC']
        return modes.index(mode) + 1

    def add_security_extra(self, security):
        types = {"wep": "wep_enable", "wpa": "wpa_enable", "wpa2": "wpa2_enable", "wpa3": "use-wpa3", "open": "[BLANK]"}
        if self.desired_add_sta_flags.__contains__(types[security]) and \
                self.desired_add_sta_flags_mask.__contains__(types[security]):
            self.desired_add_sta_flags.remove(types[security])
            self.desired_add_sta_flags_mask.remove(types[security])
        self.desired_add_sta_flags.append(types[security])
        self.desired_add_sta_flags_mask.append(types[security])
        if security == "wpa3":
            self.set_command_param("add_sta", "ieee80211w", 2)

    def set_command_param(self, command_name, param_name, param_value):
        # we have to check what the param name is
        if (command_name is None) or (command_name == ""):
            return
        if (param_name is None) or (param_name == ""):
            return
        if command_name not in self.COMMANDS:
            raise ValueError("Command name name [%s] not defined in %s" % (command_name, self.COMMANDS))
            # return
        if command_name == "add_sta":
            self.add_sta_data[param_name] = param_value
        elif command_name == "set_port":
            self.set_port_data[param_name] = param_value

    def set_command_flag(self, command_name, param_name, value):
        # we have to check what the param name is
        if (command_name is None) or (command_name == ""):
            return
        if (param_name is None) or (param_name == ""):
            return
        if command_name not in self.COMMANDS:
            print("Command name name [%s] not defined in %s" % (command_name, self.COMMANDS))
            return
        if command_name == "add_sta":
            if (param_name not in add_sta.add_sta_flags) and (param_name not in add_sta.add_sta_modes):
                print("Parameter name [%s] not defined in add_sta.py" % param_name)
                if self.debug:
                    pprint(add_sta.add_sta_flags)
                return
            if (value == 1) and (param_name not in self.desired_add_sta_flags):
                self.desired_add_sta_flags.append(param_name)
                self.desired_add_sta_flags_mask.append(param_name)
            elif value == 0:
                self.desired_add_sta_flags.remove(param_name)
                self.desired_add_sta_flags_mask.append(param_name)

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
            if (param_name in set_port.set_port_cmd_flags):
                if (value == 1) and (param_name not in self.desired_set_port_cmd_flags):
                    self.desired_set_port_cmd_flags.append(param_name)
                elif value == 0:
                    self.desired_set_port_cmd_flags.remove(param_name)
            elif (param_name in set_port.set_port_current_flags):
                if (value == 1) and (param_name not in self.desired_set_port_current_flags):
                    self.desired_set_port_current_flags.append(param_name)
                elif value == 0:
                    self.desired_set_port_current_flags.remove(param_name)
            elif (param_name in set_port.set_port_interest_flags):
                if (value == 1) and (param_name not in self.desired_set_port_interest_flags):
                    self.desired_set_port_interest_flags.append(param_name)
                elif value == 0:
                    self.desired_set_port_interest_flags.remove(param_name)
            else:
                raise ValueError("Unknown param name: " + param_name)

    # use this for hinting station name; stations begin with 'sta', the
    # stations created with a prefix '0100' indicate value 10100 + n with
    # resulting substring(1,) applied; station 900 becomes 'sta1000'
    def set_number_template(self, pref):
        self.number_template = pref

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
                    pprint(command_ref)
                raise ValueError("flag %s not in map" % name)
            result += command_ref[name]

        return result

    def admin_up(self):
        for eid in self.station_names:
            # print("3139: admin_up sta "+eid)
            # time.sleep(2)
            self.local_realm.admin_up(eid)
            time.sleep(0.005)

    def admin_down(self):
        for sta_name in self.station_names:
            self.local_realm.admin_down(sta_name)

    def cleanup(self, desired_stations=None, delay=0.03, debug_=False):
        print("Cleaning up stations")

        if (desired_stations is None):
            desired_stations = self.station_names

        if len(desired_stations) < 1:
            print("ERROR:  StationProfile cleanup, list is empty")
            return

        # First, request remove on the list.
        for port_eid in desired_stations:
            self.local_realm.rm_port(port_eid, check_exists=True, debug_=debug_)
            time.sleep(delay)
        # And now see if they are gone
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=desired_stations)

    # Checks for errors in initialization values and creates specified number of stations using init parameters
    def create(self, radio,
               num_stations=0,
               sta_names_=None,
               dry_run=False,
               up_=None,
               debug=False,
               suppress_related_commands_=True,
               use_radius=False,
               hs20_enable=False,
               sleep_time=0.02):
        if (radio is None) or (radio == ""):
            raise ValueError("station_profile.create: will not create stations without radio")
        radio_eid = self.local_realm.name_to_eid(radio)
        radio_shelf = radio_eid[0]
        radio_resource = radio_eid[1]
        radio_port = radio_eid[2]

        if self.use_ht160:
            self.desired_add_sta_flags.append("ht160_enable")
            self.desired_add_sta_flags_mask.append("ht160_enable")
        if self.mode is not None:
            self.add_sta_data["mode"] = self.mode
        if use_radius:
            self.desired_add_sta_flags.append("8021x_radius")
            self.desired_add_sta_flags_mask.append("8021x_radius")
        if hs20_enable:
            self.desired_add_sta_flags.append("hs20_enable")
            self.desired_add_sta_flags_mask.append("hs20_enable")
        if up_ is not None:
            self.up = up_

        if (sta_names_ is None) and (num_stations == 0):
            raise ValueError("StationProfile.create needs either num_stations= or sta_names_= specified")

        if self.up:
            if "create_admin_down" in self.desired_add_sta_flags:
                del self.desired_add_sta_flags[self.desired_add_sta_flags.index("create_admin_down")]
        elif "create_admin_down" not in self.desired_add_sta_flags:
            self.desired_add_sta_flags.append("create_admin_down")

        # create stations down, do set_port on them, then set stations up
        self.add_sta_data["flags"] = self.add_named_flags(self.desired_add_sta_flags, add_sta.add_sta_flags)
        self.add_sta_data["flags_mask"] = self.add_named_flags(self.desired_add_sta_flags_mask, add_sta.add_sta_flags)
        self.add_sta_data["radio"] = radio_port

        self.add_sta_data["resource"] = radio_resource
        self.add_sta_data["shelf"] = radio_shelf
        self.set_port_data["resource"] = radio_resource
        self.set_port_data["shelf"] = radio_shelf
        self.set_port_data["current_flags"] = self.add_named_flags(self.desired_set_port_current_flags,
                                                                   set_port.set_port_current_flags)
        self.set_port_data["interest"] = self.add_named_flags(self.desired_set_port_interest_flags,
                                                              set_port.set_port_interest_flags)
        self.wifi_extra_data["resource"] = radio_resource
        self.wifi_extra_data["shelf"] = radio_shelf
        self.wifi_txo_data["resource"] = radio_resource
        self.wifi_txo_data["shelf"] = radio_shelf
        self.reset_port_extra_data["resource"] = radio_resource
        self.reset_port_extra_data["shelf"] = radio_shelf

        # these are unactivated LFRequest objects that we can modify and
        # re-use inside a loop, reducing the number of object creations
        add_sta_r = LFRequest.LFRequest(self.lfclient_url + "/cli-json/add_sta", debug_=debug)
        set_port_r = LFRequest.LFRequest(self.lfclient_url + "/cli-json/set_port", debug_=debug)
        wifi_extra_r = LFRequest.LFRequest(self.lfclient_url + "/cli-json/set_wifi_extra", debug_=debug)
        wifi_txo_r = LFRequest.LFRequest(self.lfclient_url + "/cli-json/set_wifi_txo", debug_=debug)
        my_sta_names = []
        # add radio here
        if (num_stations > 0) and (len(sta_names_) < 1):
            # print("CREATING MORE STA NAMES == == == == == == == == == == == == == == == == == == == == == == == ==")
            my_sta_names = LFUtils.portNameSeries("sta", 0, num_stations - 1, int("1" + self.number_template))
            # print("CREATING MORE STA NAMES == == == == == == == == == == == == == == == == == == == == == == == ==")
        else:
            my_sta_names = sta_names_

        if (len(my_sta_names) >= 15) or (suppress_related_commands_ == True):
            self.add_sta_data["suppress_preexec_cli"] = "yes"
            self.add_sta_data["suppress_preexec_method"] = 1
            self.set_port_data["suppress_preexec_cli"] = "yes"
            self.set_port_data["suppress_preexec_method"] = 1

        num = 0
        if debug:
            print("== == Created STA names == == == == == == == == == == == == == == == == == == == == == == == ==")
            pprint(self.station_names)
            print("== == vs Pending STA names == ==")
            pprint(my_sta_names)
            print("== == == == == == == == == == == == == == == == == == == == == == == == == ==")

        # track the names of stations in case we have stations added multiple times
        finished_sta = []

        for eidn in my_sta_names:
            if eidn in self.station_names:
                print("Station %s already created, skipping." % eidn)
                continue

            # print (" EIDN "+eidn);
            if eidn in finished_sta:
                # pprint(my_sta_names)
                # raise ValueError("************ duplicate ****************** "+eidn)
                if self.debug:
                    print("Station %s already created" % eidn)
                continue

            eid = self.local_realm.name_to_eid(eidn)
            name = eid[2]
            num += 1
            self.add_sta_data["shelf"] = radio_shelf
            self.add_sta_data["resource"] = radio_resource
            self.add_sta_data["radio"] = radio_port
            self.add_sta_data["sta_name"] = name  # for create station calls
            self.set_port_data["port"] = name  # for set_port calls.
            self.set_port_data["shelf"] = radio_shelf
            self.set_port_data["resource"] = radio_resource

            add_sta_r.addPostData(self.add_sta_data)
            if debug:
                print("- 3254 - %s- - - - - - - - - - - - - - - - - - " % eidn)
                pprint(add_sta_r.requested_url)
                pprint(add_sta_r.proxies)
                pprint(self.add_sta_data)
                print(self.set_port_data)
                print("- ~3254 - - - - - - - - - - - - - - - - - - - ")
            if dry_run:
                print("dry run: not creating " + eidn)
                continue

            # print("- 3264 - ## %s ##  add_sta_r.jsonPost - - - - - - - - - - - - - - - - - - "%eidn)
            json_response = add_sta_r.jsonPost(debug=self.debug)
            finished_sta.append(eidn)
            # print("- ~3264 - %s - add_sta_r.jsonPost - - - - - - - - - - - - - - - - - - "%eidn)
            time.sleep(0.01)
            set_port_r.addPostData(self.set_port_data)
            # print("- 3270 -- %s --  set_port_r.jsonPost - - - - - - - - - - - - - - - - - - "%eidn)
            json_response = set_port_r.jsonPost(debug)
            # print("- ~3270 - %s - set_port_r.jsonPost - - - - - - - - - - - - - - - - - - "%eidn)
            time.sleep(0.01)

            self.wifi_extra_data["resource"] = radio_resource
            self.wifi_extra_data["port"] = name
            self.wifi_txo_data["resource"] = radio_resource
            self.wifi_txo_data["port"] = name
            if self.wifi_extra_data_modified:
                wifi_extra_r.addPostData(self.wifi_extra_data)
                json_response = wifi_extra_r.jsonPost(debug)
            if self.wifi_txo_data_modified:
                wifi_txo_r.addPostData(self.wifi_txo_data)
                json_response = wifi_txo_r.jsonPost(debug)

            # append created stations to self.station_names
            self.station_names.append("%s.%s.%s" % (radio_shelf, radio_resource, name))
            time.sleep(sleep_time)

        # print("- ~3287 - waitUntilPortsAppear - - - - - - - - - - - - - - - - - - "%eidn)
        LFUtils.wait_until_ports_appear(self.lfclient_url, my_sta_names)

        # and set ports up
        if dry_run:
            return
        if (self.up):
            self.admin_up()

        # for sta_name in self.station_names:
        #     req = LFUtils.portUpRequest(resource, sta_name, debug_on=False)
        #     set_port_r.addPostData(req)
        #     json_response = set_port_r.jsonPost(debug)
        #     time.sleep(0.03)
        if self.debug:
            print("created %s stations" % num)

    def modify(self, radio):
        for station in self.station_names:
            print(station)
            self.add_sta_data["flags"] = self.add_named_flags(self.desired_add_sta_flags, add_sta.add_sta_flags)
            self.add_sta_data["flags_mask"] = self.add_named_flags(self.desired_add_sta_flags_mask,
                                                                   add_sta.add_sta_flags)
            self.add_sta_data["radio"] = radio
            self.add_sta_data["sta_name"] = station
            self.add_sta_data["ssid"] = 'NA'
            self.add_sta_data["key"] = 'NA'
            self.add_sta_data['mac'] = 'NA'
            self.add_sta_data['mode'] = 'NA'
            self.add_sta_data['suppress_preexec_cli'] = 'NA'
            self.add_sta_data['suppress_preexec_method'] = 'NA'

            add_sta_r = LFRequest.LFRequest(self.lfclient_url + "/cli-json/add_sta")
            if self.debug:
                print(self.lfclient_url + "/cli_json/add_sta")
                print(self.add_sta_data)
            add_sta_r.addPostData(self.add_sta_data)
            json_response = add_sta_r.jsonPost(self.debug)
