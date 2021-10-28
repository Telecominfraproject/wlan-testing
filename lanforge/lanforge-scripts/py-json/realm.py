#!/usr/bin/env python3
# The Realm Class is inherited by most python tests.  Realm Class inherites from LFCliBase.
# The Realm Class contains the configurable components for LANforge,
# For example L3 / L4 cross connects, stations.  Also contains helper methods
# http://www.candelatech.com/cookbook.php?vol=cli&book=Python_Create_Test_Scripts_With_the_Realm_Class

# Written by Candela Technologies Inc.
#  Updated by:

import sys
import os
import importlib
import re
import time
from pprint import pprint

# ---- ---- ---- ---- LANforge Base Imports ---- ---- ---- ----

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LANforge = importlib.import_module("py-json.LANforge")
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase

# ---- ---- ---- ---- Profile Imports ---- ---- ---- ----

l3_cxprofile = importlib.import_module("py-json.l3_cxprofile")
L3CXProfile = l3_cxprofile.L3CXProfile
l3_cxprofile2 = importlib.import_module("py-json.l3_cxprofile2")
L3CXProfile2 = l3_cxprofile2.L3CXProfile2
l4_cxprofile = importlib.import_module("py-json.l4_cxprofile")
L4CXProfile = l4_cxprofile.L4CXProfile
lf_attenmod = importlib.import_module("py-json.lf_attenmod")
ATTENUATORProfile = lf_attenmod.ATTENUATORProfile
multicast_profile = importlib.import_module("py-json.multicast_profile")
MULTICASTProfile = multicast_profile.MULTICASTProfile
http_profile = importlib.import_module("py-json.http_profile")
HTTPProfile = http_profile.HTTPProfile
station_profile = importlib.import_module("py-json.station_profile")
StationProfile = station_profile.StationProfile
fio_endp_profile = importlib.import_module("py-json.fio_endp_profile")
FIOEndpProfile = fio_endp_profile.FIOEndpProfile
test_group_profile = importlib.import_module("py-json.test_group_profile")
TestGroupProfile = test_group_profile.TestGroupProfile
dut_profile = importlib.import_module("py-json.dut_profile")
DUTProfile = dut_profile.DUTProfile
vap_profile = importlib.import_module("py-json.vap_profile")
VAPProfile = vap_profile.VAPProfile
mac_vlan_profile = importlib.import_module("py-json.mac_vlan_profile")
MACVLANProfile = mac_vlan_profile.MACVLANProfile
wifi_monitor_profile = importlib.import_module("py-json.wifi_monitor_profile")
WifiMonitor = wifi_monitor_profile.WifiMonitor
gen_cxprofile = importlib.import_module("py-json.gen_cxprofile")
GenCXProfile = gen_cxprofile.GenCXProfile
qvlan_profile = importlib.import_module("py-json.qvlan_profile")
QVLANProfile = qvlan_profile.QVLANProfile
port_utils = importlib.import_module("py-json.port_utils")
PortUtils = port_utils.PortUtils
lfdata = importlib.import_module("py-json.lfdata")
LFDataCollection = lfdata.LFDataCollection


def wpa_ent_list():
    return [
        "DEFAULT",
        "NONE",
        "WPA-PSK",
        "FT-PSK",
        "FT-EAP",
        "FT-SAE",
        "FT-EAP-SHA384",
        "WPA-EAP",
        "OSEN",
        "IEEE8021X",
        "WPA-PSK-SHA256",
        "WPA-EAP-SHA256",
        "WPA-PSK WPA-EAP",
        "WPA-PSK-SHA256 WPA-EAP-SHA256",
        "WPA-PSK WPA-EAP WPA-PSK-SHA256 WPA-EAP-SHA256"
        "SAE",
        "WPA-EAP-SUITE-B",
        "WPA-EAP-SUITE-B-192",
        "FILS-SHA256",
        "FILS-SHA384",
        "OWE"
    ]


class Realm(LFCliBase):
    def __init__(self,
                 lfclient_host="localhost",
                 lfclient_port=8080,
                 debug_=False,
                 _exit_on_error=False,
                 _exit_on_fail=False,
                 _proxy_str=None,
                 _capture_signal_list=[]):
        super().__init__(_lfjson_host=lfclient_host,
                         _lfjson_port=lfclient_port,
                         _debug=debug_,
                         _exit_on_error=_exit_on_error,
                         _exit_on_fail=_exit_on_fail,
                         _proxy_str=_proxy_str,
                         _capture_signal_list=_capture_signal_list)

        self.debug = debug_
        # if debug_:
        #     print("Realm _proxy_str: %s" % _proxy_str)
        #     pprint(_proxy_str)
        self.check_connect()
        self.chan_to_freq = {}
        self.freq_to_chan = {}
        freq = 0
        chan = 1
        for freq in range(2412, 2472, 5):
            self.freq_to_chan[freq] = chan
            self.chan_to_freq[chan] = freq
            chan += 1

        self.chan_to_freq[14] = 2484
        self.chan_to_freq[34] = 5170
        self.chan_to_freq[36] = 5180
        self.chan_to_freq[38] = 5190
        self.chan_to_freq[40] = 5200
        self.chan_to_freq[42] = 5210
        self.chan_to_freq[44] = 5220
        self.chan_to_freq[46] = 5230
        self.chan_to_freq[48] = 5240
        self.chan_to_freq[52] = 5260
        self.chan_to_freq[56] = 5280
        self.chan_to_freq[60] = 5300
        self.chan_to_freq[64] = 5320
        self.chan_to_freq[100] = 5500
        self.chan_to_freq[104] = 5520
        self.chan_to_freq[108] = 5540
        self.chan_to_freq[112] = 5560
        self.chan_to_freq[116] = 5580
        self.chan_to_freq[120] = 5600
        self.chan_to_freq[124] = 5620
        self.chan_to_freq[128] = 5640
        self.chan_to_freq[132] = 5660
        self.chan_to_freq[136] = 5680
        self.chan_to_freq[140] = 5700
        self.chan_to_freq[144] = 5720
        self.chan_to_freq[149] = 5745
        self.chan_to_freq[153] = 5765
        self.chan_to_freq[157] = 5785
        self.chan_to_freq[161] = 5805
        self.chan_to_freq[165] = 5825
        self.chan_to_freq[169] = 5845
        self.chan_to_freq[173] = 5865

        self.freq_to_chan[2484] = 14
        self.freq_to_chan[5170] = 34
        self.freq_to_chan[5180] = 36
        self.freq_to_chan[5190] = 38
        self.freq_to_chan[5200] = 40
        self.freq_to_chan[5210] = 42
        self.freq_to_chan[5220] = 44
        self.freq_to_chan[5230] = 46
        self.freq_to_chan[5240] = 48
        self.freq_to_chan[5260] = 52
        self.freq_to_chan[5280] = 56
        self.freq_to_chan[5300] = 60
        self.freq_to_chan[5320] = 64
        self.freq_to_chan[5500] = 100
        self.freq_to_chan[5520] = 104
        self.freq_to_chan[5540] = 108
        self.freq_to_chan[5560] = 112
        self.freq_to_chan[5580] = 116
        self.freq_to_chan[5600] = 120
        self.freq_to_chan[5620] = 124
        self.freq_to_chan[5640] = 128
        self.freq_to_chan[5660] = 132
        self.freq_to_chan[5680] = 136
        self.freq_to_chan[5700] = 140
        self.freq_to_chan[5720] = 144
        self.freq_to_chan[5745] = 149
        self.freq_to_chan[5765] = 153
        self.freq_to_chan[5785] = 157
        self.freq_to_chan[5805] = 161
        self.freq_to_chan[5825] = 165
        self.freq_to_chan[5845] = 169
        self.freq_to_chan[5865] = 173

        # 4.9Ghz police band
        self.chan_to_freq[183] = 4915
        self.chan_to_freq[184] = 4920
        self.chan_to_freq[185] = 4925
        self.chan_to_freq[187] = 4935
        self.chan_to_freq[188] = 4940
        self.chan_to_freq[189] = 4945
        self.chan_to_freq[192] = 4960
        self.chan_to_freq[194] = 4970
        self.chan_to_freq[196] = 4980

        self.freq_to_chan[4915] = 183
        self.freq_to_chan[4920] = 184
        self.freq_to_chan[4925] = 185
        self.freq_to_chan[4935] = 187
        self.freq_to_chan[4940] = 188
        self.freq_to_chan[4945] = 189
        self.freq_to_chan[4960] = 192
        self.freq_to_chan[4970] = 194
        self.freq_to_chan[4980] = 196

    def wait_until_ports_appear(self, sta_list=None, debug_=False):
        if (sta_list is None) or (len(sta_list) < 1):
            print("realm.wait_until_ports_appear: no stations provided")
            return
        LFUtils.wait_until_ports_appear(base_url=self.lfclient_url,
                                        port_list=sta_list,
                                        debug=debug_)

    def wait_until_ports_disappear(self, sta_list=None, debug_=False):
        if (sta_list is None) or (len(sta_list) < 1):
            print("realm.wait_until_ports_appear: no stations provided")
            return

        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                           port_list=sta_list,
                                           debug=debug_)

    def rm_port(self, port_eid, check_exists=True, debug_=False):
        if port_eid is None:
            raise ValueError("realm.rm_port: want a port eid like 1.1.eth1")
        debug_ |= self.debug
        req_url = "/cli-json/rm_vlan"
        eid = self.name_to_eid(port_eid)
        if check_exists:
            if not self.port_exists(port_eid):
                return False

        data = {
            "shelf": eid[0],
            "resource": eid[1],
            "port": eid[2]
            }
        rsp = self.json_post(req_url, data, debug_=debug_)
        return True

    def port_exists(self, port_eid):
        eid = self.name_to_eid(port_eid)
        current_stations = self.json_get("/port/%s/%s/%s?fields=alias" % (eid[0], eid[1], eid[2]))
        if not current_stations is None:
            return True
        return False

    def admin_up(self, port_eid):
        # print("186 admin_up port_eid: "+port_eid)
        eid = self.name_to_eid(port_eid)
        shelf = eid[0]
        resource = eid[1]
        port = eid[2]
        request = LFUtils.port_up_request(resource_id=resource, port_name=port)
        # print("192.admin_up request: resource: %s port_name %s"%(resource, port))
        # time.sleep(2)
        self.json_post("/cli-json/set_port", request)

    def admin_down(self, port_eid):
        eid = self.name_to_eid(port_eid)
        shelf = eid[0]
        resource = eid[1]
        port = eid[2]
        request = LFUtils.port_down_request(resource_id=resource, port_name=port)
        self.json_post("/cli-json/set_port", request)

    def reset_port(self, port_eid):
        eid = self.name_to_eid(port_eid)
        shelf = eid[0]
        resource = eid[1]
        port = eid[2]
        request = LFUtils.port_reset_request(resource_id=resource, port_name=port)
        self.json_post("cli-json/reset_port", request)

    def rm_cx(self, cx_name):
        req_url = "cli-json/rm_cx"
        data = {
            "test_mgr": "ALL",
            "cx_name": cx_name
        }
        self.json_post(req_url, data)

    def rm_endp(self, ename, debug_=False, suppress_related_commands_=True):
        req_url = "cli-json/rm_endp"
        data = {
            "endp_name": ename
        }
        self.json_post(req_url, data, debug_=debug_, suppress_related_commands_=suppress_related_commands_)

    def set_endp_tos(self, ename, _tos, debug_=False, suppress_related_commands_=True):
        req_url = "cli-json/set_endp_tos"
        tos = _tos
        # Convert some human readable values to numeric needed by LANforge.
        if _tos == "BK":
            tos = "64"
        if _tos == "BE":
            tos = "96"
        if _tos == "VI":
            tos = "128"
        if _tos == "VO":
            tos = "192"
        data = {
            "name": ename,
            "tos": tos
        }
        self.json_post(req_url, data, debug_=debug_, suppress_related_commands_=suppress_related_commands_)

    def stop_cx(self, cx_name):
        self.json_post("/cli-json/set_cx_state", {
            "test_mgr": "ALL",
            "cx_name": cx_name,
            "cx_state": "STOPPED"
        }, debug_=self.debug)

    def cleanup_cxe_prefix(self, prefix):
        cx_list = self.cx_list()
        if cx_list is not None:
            for cx_name in cx_list:
                if cx_name.startswith(prefix):
                    self.rm_cx(cx_name)

        endp_list = self.json_get("/endp/list")
        if endp_list is not None:
            if 'endpoint' in endp_list:
                endp_list = list(endp_list['endpoint'])
                for idx in range(len(endp_list)):
                    endp_name = list(endp_list[idx])[0]
                    if endp_name.startswith(prefix):
                        self.rm_endp(endp_name)
            else:
                if self.debug:
                    print("cleanup_cxe_prefix no endpoints: endp_list{}".format(endp_list))

    def channel_freq(self, channel_=0):
        return self.chan_to_freq[channel_]

    def freq_channel(self, freq_=0):
        return self.freq_to_chan[freq_]

    # checks for OK or BUSY when querying cli-json/cv+is_built
    def wait_while_building(self, debug_=False):
        response_json = []
        data = {
            "cmd": "cv is_built"
        }
        last_response = "BUSY"
        dbg_param = ""
        if debug_:
            dbg_param = "?__debug=1"

        while (last_response != "YES"):
            response = self.json_post("/gui-json/cmd%s" % dbg_param, data, debug_=debug_,
                                      response_json_list_=response_json)
            # LFUtils.debug_printer.pprint(response_json)
            last_response = response_json[0]["LAST"]["response"]
            if (last_response != "YES"):
                last_response = None
                response_json = []
                time.sleep(1)
            else:
                return
        return

    # loads a database
    def load(self, name):
        if (name is None) or (name == ""):
            raise ValueError(
                "Realm::load: wants a test scenario database name, please find one in the Status tab of the GUI")

        data = {
            "name": name,
            "action": "overwrite",
            "clean_dut": "yes",
            "clean_chambers": "yes"
        }
        self.json_post("/cli-json/load", _data=data, debug_=self.debug)
        time.sleep(1)

    # Returns json response from webpage of all layer 3 cross connects
    def cx_list(self):
        response = self.json_get("/cx/list")
        return response

    def waitUntilEndpsAppear(self, these_endp, debug=False):
        return self.wait_until_endps_appear(these_endp, debug=debug)

    def wait_until_endps_appear(self, these_endp, debug=False):
        wait_more = True
        count = 0
        while wait_more:
            time.sleep(1)
            wait_more = False
            endp_list = self.json_get("/endp/list")
            found_endps = {}
            if debug:
                print("Waiting on endpoint endp_list {}".format(endp_list))
            if (endp_list is not None) and ("items" not in endp_list):
                try:
                    endp_list = list(endp_list['endpoint'])
                    for idx in range(len(endp_list)):
                        name = list(endp_list[idx])[0]
                        found_endps[name] = name
                except:
                    print("non-fatal exception endp_list = list(endp_list['endpoint'] did not exist, will wait some more")

            for req in these_endp:
                if not req in found_endps:
                    if debug:
                        print("Waiting on endpoint: %s" % (req))
                    wait_more = True
            count += 1
            if (count > 100):
                break

        return not wait_more

    def waitUntilCxsAppear(self, these_cx, debug=False):
        return self.wait_until_cxs_appear(these_cx, debug=debug)

    def wait_until_cxs_appear(self, these_cx, debug=False):
        wait_more = True
        count = 0
        while wait_more:
            time.sleep(1)
            wait_more = False
            found_cxs = {}
            cx_list = self.cx_list()
            not_cx = ['warnings', 'errors', 'handler', 'uri', 'items']
            if cx_list is not None:
                for cx_name in cx_list:
                    if cx_name in not_cx:
                        continue
                    found_cxs[cx_name] = cx_name

            for req in these_cx:
                if not req in found_cxs:
                    if debug:
                        print("Waiting on CX: %s" % (req))
                    wait_more = True
            count += 1
            if (count > 100):
                break

        return not wait_more

    # Returns map of all stations with port+type == WIFI-STATION
    # Key is the EID, value is the map of key/values for the port values.
    def station_map(self):
        response = super().json_get("/port/list?fields=port,_links,alias,device,port+type")
        if (response is None) or ("interfaces" not in response):
            pprint(response)
            print("station_list: incomplete response, halting")
            exit(1)
        sta_map = {}
        temp_map = LFUtils.portListToAliasMap(response)
        for k, v in temp_map.items():
            if (v['port type'] == "WIFI-STA"):
                sta_map[k] = v
        temp_map.clear()
        del temp_map
        del response
        return sta_map

    # Returns list of all stations with port+type == WIFI-STATION
    def station_list(self):
        sta_list = []
        response = super().json_get("/port/list?fields=_links,alias,device,port+type")
        if (response is None) or ("interfaces" not in response):
            print("station_list: incomplete response:")
            pprint(response)
            exit(1)

        for x in range(len(response['interfaces'])):
            for k, v in response['interfaces'][x].items():
                if v['port type'] == "WIFI-STA":
                    sta_list.append(response['interfaces'][x])
        del response
        return sta_list

    # Returns list of all ports
    def port_list(self):
        sta_list = []
        response = super().json_get("/port/list?fields=all")
        if (response is None) or ("interfaces" not in response):
            print("port_list: incomplete response:")
            pprint(response)
            return None

        return response['interfaces']

    # Returns list of all VAPs with "vap" in their name
    def vap_list(self):
        sta_list = []
        response = super().json_get("/port/list?fields=_links,alias,device,port+type")
        for x in range(len(response['interfaces'])):
            for k, v in response['interfaces'][x].items():
                if "vap" in v['device']:
                    sta_list.append(response['interfaces'][x])

        return sta_list

    # Returns all attenuators
    def atten_list(self):
        response = super().json_get("/atten/list")
        return response['attenuators']

    # EID is shelf.resource.atten-serno.atten-idx
    def set_atten(self, eid, atten_ddb):
        eid_toks = self.name_to_eid(eid, non_port=True)
        req_url = "cli-json/set_attenuator"
        data = {
            "shelf": eid_toks[0],
            "resource": eid_toks[1],
            "serno": eid_toks[2],
            "atten_idx":eid_toks[3],
            "val":atten_ddb,
            }
        self.json_post(req_url, data)

    # removes port by eid/eidpn
    def remove_vlan_by_eid(self, eid):
        if (eid is None) or ("" == eid):
            raise ValueError("removeVlanByEid wants eid like 1.1.sta0 but given[%s]" % eid)
        hunks = self.name_to_eid(eid)
        # print("- - - - - - - - - - - - - - - - -")
        # pprint(hunks)
        # pprint(self.lfclient_url)
        # print("- - - - - - - - - - - - - - - - -")
        if (len(hunks) > 3) or (len(hunks) < 2):
            raise ValueError("removeVlanByEid wants eid like 1.1.sta0 but given[%s]" % eid)
        elif len(hunks) == 3:
            LFUtils.removePort(hunks[1], hunks[2], self.lfclient_url)
        else:
            LFUtils.removePort(hunks[0], hunks[1], self.lfclient_url)

    # Searches for ports that match a given pattern and returns a list of names
    def find_ports_like(self, pattern="", _fields="_links,alias,device,port+type", resource=0, debug_=False):
        if resource == 0:
            url = "/port/1/list?fields=%s" % _fields
        else:
            url = "/port/1/%s/list?fields=%s" % (resource, _fields)
        response = self.json_get(url)
        if debug_:
            print("# find_ports_like r:%s, u:%s #" % (resource, url))
            pprint(response)
        alias_map = LFUtils.portListToAliasMap(response, debug_=debug_)
        if debug_:
            pprint(alias_map)
        prelim_map = {}
        matched_map = {}
        for name, record in alias_map.items():
            try:
                if debug_:
                    print("- prelim - - - - - - - - - - - - - - - - - - -")
                    pprint(record)
                if (record["port type"] == "WIFI-STA"):
                    prelim_map[name] = record

            except Exception as x:
                self.error(x)

        prefix = ""
        try:
            if pattern.find("+") > 0:
                match = re.search(r"^([^+]+)[+]$", pattern)
                if match.group(1):
                    prefix = match.group(1)
                for port_eid, record in prelim_map.items():
                    if debug_:
                        print("name:", port_eid, " Group 1: ", match.group(1))
                    if port_eid.find(prefix) >= 0:
                        matched_map[port_eid] = record

            elif pattern.find("*") > 0:
                match = re.search(r"^([^\*]+)[*]$", pattern)
                if match.group(1):
                    prefix = match.group(1)
                    if debug_:
                        print("group 1: ", prefix)
                for port_eid, record in prelim_map.items():
                    if port_eid.find(prefix) >= 0:
                        matched_map[port_eid] = record

            elif pattern.find("[") > 0:
                # TODO: regex below might have too many hack escapes
                match = re.search(r"^([^\[]+)\[(\d+)\.\.(\d+)\]$", pattern)
                if match.group(0):
                    if debug_:
                        print("[group1]: ", match.group(1))
                        print("[group2]: ", match.group(2))
                        print("[group3]: ", match.group(3))
                    prefix = match.group(1)
                    for port_eid, record in prelim_map.items():
                        if port_eid.find(prefix) >= 0:
                            port_suf = record["device"][len(prefix):]
                            if (port_suf >= match.group(2)) and (port_suf <= match.group(3)):
                                # print("%s: suffix[%s] between %s:%s" % (port_name, port_name, match.group(2), match.group(3))
                                matched_map[port_eid] = record
        except ValueError as e:
            self.error(e)

        return matched_map

    def name_to_eid(self, eid, debug=False, non_port=False):
        if debug:
            self.logg(level="debug", mesg="name_to_eid: "+str(eid))
        if (type(eid) is list) or (type(eid) is tuple):
            return eid
        return LFUtils.name_to_eid(eid, non_port=non_port)

    def wait_for_ip(self, station_list=None, ipv4=True, ipv6=False, timeout_sec=360, debug=False):
        if not (ipv4 or ipv6):
            raise ValueError("wait_for_ip: ipv4 and/or ipv6 must be set!")
        if timeout_sec >= 0:
            print("Waiting for ips, timeout: %i..." % timeout_sec)
        else:
            print("Determining wait time based on mean station association time of stations. "
                  "Will not wait more that 60 seconds without single association")
        stas_with_ips = {}
        sec_elapsed = 0
        time_extended = False
        # print(station_list)
        waiting_states = ["0.0.0.0", "NA", ""]
        if (station_list is None) or (len(station_list) < 1):
            raise ValueError("wait_for_ip: expects non-empty list of ports")
        wait_more = True

        while wait_more and (sec_elapsed <= timeout_sec or timeout_sec == -1):
            wait_more = False

            if not time_extended and timeout_sec == -1:
                wait_more = True
                num_with_ips = len(stas_with_ips)
                if sec_elapsed >= 10 and num_with_ips > 0:
                    time_extended = True
                    # print(sec_elapsed, num_with_ips, int(sec_elapsed / num_with_ips), len(station_list))
                    timeout_sec = int(sec_elapsed / num_with_ips * len(station_list))
                    print("New timeout is %d seconds" % timeout_sec)
                elif sec_elapsed > 60 and num_with_ips == 0:
                    timeout_sec = 60
                    wait_more = False

            for sta_eid in station_list:
                if debug:
                    print("checking sta-eid: %s" % (sta_eid))
                eid = self.name_to_eid(sta_eid)

                response = super().json_get("/port/%s/%s/%s?fields=alias,ip,port+type,ipv6+address" %
                                            (eid[0], eid[1], eid[2]))
                # pprint(response)

                if (response is None) or ("interface" not in response):
                    print("station_list: incomplete response:")
                    pprint(response)
                    wait_more = True
                    break

                if ipv4:
                    v = response['interface']
                    if v['ip'] in waiting_states:
                        wait_more = True
                        if debug:
                            print("Waiting for port %s to get IPv4 Address." % (sta_eid))
                    else:
                        if sta_eid not in stas_with_ips:
                            stas_with_ips[sta_eid] = {'ipv4': v['ip']}
                        if debug:
                            print("Found IP: %s on port: %s" % (v['ip'], sta_eid))

                if ipv6:
                    v = response['interface']
                    # print(v)
                    if v['ipv6 address'] != 'DELETED' and not v['ipv6 address'].startswith('fe80') \
                            and v['ipv6 address'] != 'AUTO':
                        if sta_eid not in stas_with_ips:
                            stas_with_ips[sta_eid] = {'ipv6': v['ip']}
                        if debug:
                            print("Found IPv6: %s on port: %s" % (v['ipv6 address'], sta_eid))
                    else:
                        wait_more = True
                        if debug:
                            print("Waiting for port %s to get IPv6 Address." % (sta_eid))

            if wait_more:
                time.sleep(1)
                sec_elapsed += 1

        return not wait_more

    def get_curr_num_ips(self, num_sta_with_ips=0, station_list=None, ipv4=True, ipv6=False, debug=False):
        if debug:
            print("checking number of stations with ips...")
        waiting_states = ["0.0.0.0", "NA", ""]
        if (station_list is None) or (len(station_list) < 1):
            raise ValueError("check for num curr ips expects non-empty list of ports")
        for sta_eid in station_list:
            if debug:
                print("checking sta-eid: %s" % (sta_eid))
            eid = self.name_to_eid(sta_eid)
            response = super().json_get("/port/%s/%s/%s?fields=alias,ip,port+type,ipv6+address" %
                                        (eid[0], eid[1], eid[2]))
            if debug:
                pprint(response)
            if (response is None) or ("interface" not in response):
                print("station_list: incomplete response:")
                pprint(response)
                # wait_more = True
                break
            if ipv4:
                v = response['interface']
                if (v['ip'] in waiting_states):
                    if debug:
                        print("Waiting for port %s to get IPv4 Address." % (sta_eid))
                else:
                    if debug:
                        print("Found IP: %s on port: %s" % (v['ip'], sta_eid))
                        print("Incrementing stations with IP addresses found")
                        num_sta_with_ips += 1
                    else:
                        num_sta_with_ips += 1
            if ipv6:
                v = response['interface']
                if (v['ip'] in waiting_states):
                    if debug:
                        print("Waiting for port %s to get IPv6 Address." % (sta_eid))

                else:
                    if debug:
                        print("Found IP: %s on port: %s" % (v['ip'], sta_eid))
                        print("Incrementing stations with IP addresses found")
                        num_sta_with_ips += 1
                    else:
                        num_sta_with_ips += 1
        return num_sta_with_ips

    def duration_time_to_seconds(self, time_string):
        if isinstance(time_string, str):
            pattern = re.compile("^(\d+)([dhms]$)")
            td = pattern.match(time_string)
            if td is not None:
                dur_time = int(td.group(1))
                dur_measure = str(td.group(2))
                if dur_measure == "d":
                    duration_sec = dur_time * 24 * 60 * 60
                elif dur_measure == "h":
                    duration_sec = dur_time * 60 * 60
                elif dur_measure == "m":
                    duration_sec = dur_time * 60
                else:
                    duration_sec = dur_time * 1
            else:
                raise ValueError("Unknown value for time_string: %s" % time_string)
        else:
            raise ValueError("time_string must be of type str. Type %s provided" % type(time_string))
        return duration_sec


    def remove_all_stations(self, resource):
        port_list = self.station_list()
        sta_list = []
        if sta_list is not None:
            print("Removing all stations")
            for item in list(port_list):
                if "sta" in list(item)[0]:
                    sta_list.append(self.name_to_eid(list(item)[0])[2])

            for sta_name in sta_list:
                req_url = "cli-json/rm_vlan"
                data = {
                    "shelf": 1,
                    "resource": resource,
                    "port": sta_name
                }
                self.json_post(req_url, data)

    def remove_all_endps(self):
        endp_list = self.json_get("/endp/list")
        if "items" in endp_list or "empty" in endp_list:
            return
        if endp_list is not None or endp_list:
            print("Removing all endps")
            endp_list = list(endp_list['endpoint'])
            for endp_name in range(len(endp_list)):
                name = list(endp_list[endp_name])[0]
                req_url = "cli-json/rm_endp"
                data = {
                    "endp_name": name
                }
                self.json_post(req_url, data)

    def remove_all_cxs(self, remove_all_endpoints=False):
        # remove cross connects
        # remove endpoints
        # nc show endpoints
        # nc show cross connects
        try:
            cx_list = list(self.cx_list())
            not_cx = ['warnings', 'errors', 'handler', 'uri', 'items', 'empty']
            if cx_list is not None:
                print("Removing all cxs")
                for cx_name in cx_list:
                    if cx_name in not_cx:
                        continue
                    req_url = "cli-json/rm_cx"
                    data = {
                        "test_mgr": "default_tm",
                        "cx_name": cx_name
                    }
                    self.json_post(req_url, data)
        except:
            print("no cxs to remove")

        if remove_all_endpoints:
            self.remove_all_endps()
            req_url = "cli-json/nc_show_endpoints"
            data = {
                "endpoint": "all"
            }
            self.json_post(req_url, data)
            req_url = "cli-json/show_cx"
            data = {
                "test_mgr": "all",
                "cross_connect": "all"
            }

    def parse_link(self, link):
        link = self.lfclient_url + link
        info = ()

    def new_station_profile(self, ver = 1):
        if ver == 1:
            station_prof = StationProfile(self.lfclient_url, local_realm=self, debug_=self.debug, up=False)
        #elif ver == 2:
            # import station_profile2
            # station_prof = station_profile2.StationProfile2(self.lfclient_url, local_realm=self, debug_=self.debug, up=False)
        return station_prof

    def new_multicast_profile(self, ver = 1):
        if ver == 1:
            multi_prof = MULTICASTProfile(self.lfclient_host, self.lfclient_port,
                                      local_realm=self, debug_=self.debug, report_timer_=3000)
        #elif ver == 2:
            # import multicast_profile2
            # multi_prof = multicast_profile2.MULTICASTProfile2(self.lfclient_host, self.lfclient_port,
            #                           local_realm=self, debug_=self.debug, report_timer_=3000)
        return multi_prof

    def new_wifi_monitor_profile(self, resource_=1, debug_=False, up_=False, ver = 1):
        if ver == 1:
            wifi_mon_prof = WifiMonitor(self.lfclient_url,
                                    local_realm=self,
                                    resource_=resource_,
                                    up=up_,
                                    debug_=(self.debug or debug_))
        #elif ver == 2:
            # import wifi_monitor_profile2
            # wifi_mon_prof = wifi_monitor_profile2.WifiMonitor2(self.lfclient_url,
            #                         local_realm=self,
            #                         resource_=resource_,
            #                         up=up_,
            #                         debug_=(self.debug or debug_))
        return wifi_mon_prof

    def new_l3_cx_profile(self, ver=1):
        if ver == 1:
            cx_prof = L3CXProfile(self.lfclient_host,
                              self.lfclient_port,
                              local_realm=self,
                              debug_=self.debug,
                              report_timer_=3000)
        elif ver == 2:
            cx_prof = L3CXProfile2(self.lfclient_host,
                              self.lfclient_port,
                              local_realm=self,
                              debug_=self.debug,
                              report_timer_=3000)
        return cx_prof

    def new_l4_cx_profile(self, ver=1):
        if ver == 1:
            cx_prof = L4CXProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)
        #elif ver == 2:
            # import l4_cxprofile2
            # cx_prof = l4_cxprofile2.L4CXProfile2(self.lfclient_host,
            #                   self.lfclient_port,
            #                   local_realm=self,
            #                   debug_=self.debug,
            #                   report_timer_=3000)
        return cx_prof
    def new_attenuator_profile(self, ver=1):
        if ver == 1:
            atten_prof = ATTENUATORProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)
        return  atten_prof
    def new_generic_endp_profile(self, ver=1):
        if ver == 1 :
            endp_prof = GenCXProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)
        #elif ver == 2:
            # import gen_cxprofile2
            # endp_prof = gen_cxprofile2.GenCXProfile(self.lfclient_host,
            #                   self.lfclient_port,
            #                   local_realm=self,
            #                   debug_=self.debug,
            #                   report_timer_=3000)
        return endp_prof

    def new_generic_cx_profile(self, ver=1):
        """
        @deprecated
        :return: new GenCXProfile
        """
        if ver == 1:
            cx_prof = GenCXProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)
        #elif ver == 2:
            # import gen_cxprofile2
            # cx_prof = gen_cxprofile2.GenCXProfile(self.lfclient_host,
            #                   self.lfclient_port,
            #                   local_realm=self,
            #                   debug_=self.debug,
            #                   report_timer_=3000)
        return cx_prof

    def new_vap_profile(self, ver=1):
        if ver == 1:
            vap_prof = VAPProfile(lfclient_host=self.lfclient_host, lfclient_port=self.lfclient_port, local_realm=self,
                              debug_=self.debug)
        # elif ver == 2:
        #     import vap_profile2
        #     vap_prof = vap_profile2.VAPProfile2(lfclient_host=self.lfclient_host, lfclient_port=self.lfclient_port, local_realm=self,
        #                       debug_=self.debug)
        return vap_prof

    def new_vr_profile(self, ver=2):
        if ver == 2:
            from vr_profile2 import VRProfile
            vap_prof = VRProfile(local_realm=self,
                                 debug=self.debug)
        return vap_prof

    def new_http_profile(self, ver = 1):
        if ver == 1:
            http_prof = HTTPProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)
        # elif ver == 2:
        #     import http_profile2
        #     http_prof = http_profile2.HTTPProfile2(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)
        return http_prof

    def new_fio_endp_profile(self, ver = 1):
        if ver == 1:
            cx_prof = FIOEndpProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)
        # elif ver == 2:
        #     import fio_endp_profile2
        #     cx_prof = fio_endp_profile2.FIOEndpProfile2(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)
        return cx_prof

    def new_dut_profile(self, ver = 1):
        if ver == 1:
            dut_profile = DUTProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)
        # elif ver == 2:
        #     import dut_profile2
        #     dut_profile = dut_profile2.DUTProfile2(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)
        return dut_profile

    def new_mvlan_profile(self, ver = 1):
        if ver == 1:
            mac_vlan_profile = MACVLANProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)
        # elif ver == 2:
        #     import mac_vlan_profile2
        #     mac_vlan_profile = mac_vlan_profile2.MACVLANProfile2(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)
        return mac_vlan_profile

    def new_qvlan_profile(self):
        return QVLANProfile(self.host, self.port, local_realm=self, debug_=self.debug)

    def new_test_group_profile(self, ver = 1):
        if ver == 1:
            test_group_profile = TestGroupProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)
        # elif ver == 2:
        #     import test_group_profile2
        #     test_group_profile = test_group_profile2.TestGroupProfile2(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)
        return test_group_profile

    def new_lf_data_collection(self):
        return LFDataCollection(local_realm=self)

class PacketFilter():

    def get_filter_wlan_assoc_packets(self, ap_mac, sta_mac):
        filter = "-T fields -e wlan.fc.type_subtype -e wlan.addr -e wlan.fc.pwrmgt " \
                 "-Y \"(wlan.addr==%s or wlan.addr==%s) and wlan.fc.type_subtype<=3\" " % (ap_mac, sta_mac)
        return filter

    def get_filter_wlan_null_packets(self, ap_mac, sta_mac):
        filter = "-T fields -e wlan.fc.type_subtype -e wlan.addr -e wlan.fc.pwrmgt " \
                 "-Y \"(wlan.addr==%s or wlan.addr==%s) and wlan.fc.type_subtype==44\" " % (ap_mac, sta_mac)
        return filter

    def run_filter(self, pcap_file, filter):
        filename = "/tmp/tshark_dump.txt"
        cmd = "tshark -r %s %s > %s" % (pcap_file, filter, filename)
        # print("CMD: ", cmd)
        os.system(cmd)
        lines = []
        with open(filename) as tshark_file:
            for line in tshark_file:
                lines.append(line.rstrip())

        return lines
