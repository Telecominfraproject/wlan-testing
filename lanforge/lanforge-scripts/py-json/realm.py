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
from pprint import pformat
import logging

logger = logging.getLogger(__name__)

# ---- ---- ---- ---- LANforge Base Imports ---- ---- ---- ----


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LANforge = importlib.import_module("py-json.LANforge")
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase

# ---- ---- ---- ---- Profile Imports ---- ---- ---- ----

l3_cxprofile = importlib.import_module("py-json.l3_cxprofile")
L3CXProfile = l3_cxprofile.L3CXProfile
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
                 _capture_signal_list=None):
        super().__init__(_lfjson_host=lfclient_host,
                         _lfjson_port=lfclient_port,
                         _debug=debug_,
                         _exit_on_error=_exit_on_error,
                         _exit_on_fail=_exit_on_fail,
                         _proxy_str=_proxy_str,
                         _capture_signal_list=_capture_signal_list)

        if _capture_signal_list is None:
            _capture_signal_list = []
        self.debug = debug_
        # if debug_:
        #     logger.debug("Realm _proxy_str: %s" % _proxy_str)
        #     logger.debug(pformat(_proxy_str))
        self.check_connect()
        self.chan_to_freq = {}
        self.freq_to_chan = {}
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

    def wait_until_ports_appear(self, sta_list=None, debug_=False, timeout=360):
        if (sta_list is None) or (len(sta_list) < 1):
            logger.info("realm.wait_until_ports_appear: no stations provided")
            return
        LFUtils.wait_until_ports_appear(base_url=self.lfclient_url,
                                        port_list=sta_list,
                                        debug=debug_,
                                        timeout=timeout)

    def wait_until_ports_disappear(self, sta_list=None, debug_=False):
        if (sta_list is None) or (len(sta_list) < 1):
            logger.info("realm.wait_until_ports_appear: no stations provided")
            return

        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                           port_list=sta_list,
                                           debug=debug_)

    def rm_port(self, port_eid, check_exists=True, debug_=None):
        if port_eid is None:
            logger.critical("realm.rm_port: want a port eid like 1.1.eth1")
            raise ValueError("realm.rm_port: want a port eid like 1.1.eth1")
        if debug_ is None:
            debug_ = self.debug
        req_url = "/cli-json/rm_vlan"
        eid = self.name_to_eid(port_eid)
        if check_exists:
            if not self.port_exists(port_eid, debug=False):
                return False

        data = {
            "shelf": eid[0],
            "resource": eid[1],
            "port": eid[2]
        }
        self.json_post(req_url, data, debug_=debug_)
        return True

    def port_exists(self, port_eid, debug=None):
        if debug is None:
            debug = self.debug
        eid = self.name_to_eid(port_eid)
        current_stations = self.json_get("/port/%s/%s/%s?fields=alias" % (eid[0], eid[1], eid[2]),
                                         debug_=debug)
        if current_stations:
            return True
        return False

    def admin_up(self, port_eid):
        # logger.info("186 admin_up port_eid: "+port_eid)
        eid = self.name_to_eid(port_eid)
        resource = eid[1]
        port = eid[2]
        request = LFUtils.port_up_request(resource_id=resource, port_name=port, debug_on=self.debug)
        # logger.info("192.admin_up request: resource: %s port_name %s"%(resource, port))
        dbg_param = ""
        if logger.getEffectiveLevel() == logging.DEBUG:
            #logger.info("enabling url debugging")
            dbg_param = "?__debug=1"
        collected_responses = list()
        self.json_post("/cli-json/set_port%s" % dbg_param, request, debug_=self.debug,
                       response_json_list_=collected_responses)
        # TODO: when doing admin-up ath10k radios, want a LF complaint about a license exception
        # if len(collected_responses) > 0: ...

    def admin_down(self, port_eid):
        eid = self.name_to_eid(port_eid)
        resource = eid[1]
        port = eid[2]
        request = LFUtils.port_down_request(resource_id=resource, port_name=port)
        self.json_post("/cli-json/set_port", request)

    def reset_port(self, port_eid):
        eid = self.name_to_eid(port_eid)
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
        if cx_list:
            for cx_name in cx_list:
                if cx_name.startswith(prefix):
                    self.rm_cx(cx_name)

        endp_list = self.json_get("/endp/list")
        if endp_list:
            if 'endpoint' in endp_list:
                endp_list = list(endp_list['endpoint'])
                for idx in range(len(endp_list)):
                    endp_name = list(endp_list[idx])[0]
                    if endp_name.startswith(prefix):
                        self.rm_endp(endp_name)
            else:
                if self.debug:
                    logger.debug("cleanup_cxe_prefix no endpoints: endp_list{}".format(endp_list))

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

        while last_response != "YES":
            self.json_post("/gui-json/cmd%s" % dbg_param, data, debug_=debug_, response_json_list_=response_json)
            # logger.info(pformat(response_json))
            last_response = response_json[0]["LAST"]["response"]
            if last_response != "YES":
                last_response = None
                response_json = []
                time.sleep(1)
            else:
                return
        return

    # loads a database
    def load(self, name):
        if (name is None) or (name == ""):
            logger.critical(
                "Realm::load: wants a test scenario database name, please find one in the Status tab of the GUI")
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

    def waitUntilEndpsAppear(self, these_endp, debug=False, timeout=300):
        return self.wait_until_endps_appear(these_endp, debug=debug, timeout=timeout)

    def wait_until_endps_appear(self, these_endp, debug=False, timeout=100):
        wait_more = True
        count = 0
        while wait_more:
            wait_more = False
            endp_list = self.json_get("/endp/list")
            found_endps = {}
            if debug:
                logger.debug("Waiting on endpoint endp_list {}".format(endp_list))
            if endp_list and ("items" not in endp_list):
                try:
                    endp_list = list(endp_list['endpoint'])
                    for idx in range(len(endp_list)):
                        name = list(endp_list[idx])[0]
                        found_endps[name] = name
                except:
                    logger.info(
                        "non-fatal exception endp_list = list(endp_list['endpoint'] did not exist, will wait some more")
                    pprint(endp_list)

            for req in these_endp:
                if req not in found_endps:
                    if debug:
                        logger.debug("Waiting on endpoint: %s" % req)
                    wait_more = True
            count += 1
            if count > timeout:
                logger.error("ERROR:  Could not find all endpoints: %s" % these_endp)
                return False
            if wait_more:
                time.sleep(1)

        return True

    def waitUntilCxsAppear(self, these_cx, debug=False, timeout=100):
        return self.wait_until_cxs_appear(these_cx, debug=debug, timeout=timeout)

    def wait_until_cxs_appear(self, these_cx, debug=False, timeout=100):
        wait_more = True
        count = 0
        while wait_more:
            wait_more = False
            found_cxs = {}
            cx_list = self.cx_list()
            not_cx = ['warnings', 'errors', 'handler', 'uri', 'items']
            if cx_list:
                for cx_name in cx_list:
                    if cx_name in not_cx:
                        continue
                    found_cxs[cx_name] = cx_name

            for req in these_cx:
                if req not in found_cxs:
                    if debug:
                        logger.debug("Waiting on CX: %s" % req)
                    wait_more = True
            count += 1
            if count > timeout:
                if debug:
                    logger.error("ERROR:  Failed to find all cxs: %s" % these_cx)
                return False
            if wait_more:
                time.sleep(1)

        return True

    # def wait_until_database_loaded(self):

    # Returns map of all stations with port+type == WIFI-STATION
    # Key is the EID, value is the map of key/values for the port values.
    def station_map(self):
        response = super().json_get("/port/list?fields=port,_links,alias,device,port+type")
        if (response is None) or ("interfaces" not in response):
            logger.critical(pformat(response))
            logger.critical("station_list: incomplete response, halting")
            exit(1)
        sta_map = {}
        temp_map = LFUtils.portListToAliasMap(response)
        for k, v in temp_map.items():
            if v['port type'] == "WIFI-STA":
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
            logger.critical("station_list: incomplete response:")
            logger.critical(pformat(response))
            exit(1)

        for x in range(len(response['interfaces'])):
            for k, v in response['interfaces'][x].items():
                if v['port type'] == "WIFI-STA":
                    sta_list.append(response['interfaces'][x])
        del response
        return sta_list

    # Returns list of all ports
    def port_list(self):
        response = super().json_get("/port/list?fields=all")
        if (response is None) or ("interfaces" not in response):
            logger.info("port_list: incomplete response:")
            logger.info(pformat(response))
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
            "atten_idx": eid_toks[3],
            "val": atten_ddb,
        }
        self.json_post(req_url, data)

    # removes port by eid/eidpn
    def remove_vlan_by_eid(self, eid):
        if (eid is None) or (eid == ""):
            logger.critical("removeVlanByEid wants eid like 1.1.sta0 but given[%s]" % eid)
            raise ValueError("removeVlanByEid wants eid like 1.1.sta0 but given[%s]" % eid)
        hunks = self.name_to_eid(eid)
        # logger.info("- - - - - - - - - - - - - - - - -")
        # logger.info(pformat(hunks))
        # logger.info(pformat(self.lfclient_url))
        # logger.info("- - - - - - - - - - - - - - - - -")
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
            logger.debug("# find_ports_like r:%s, u:%s #" % (resource, url))
            logger.debug(pformat(response))
        alias_map = LFUtils.portListToAliasMap(response, debug_=debug_)
        if debug_:
            logger.debug(pformat(alias_map))
        prelim_map = {}
        matched_map = {}
        for name, record in alias_map.items():
            try:
                if debug_:
                    logger.debug("- prelim - - - - - - - - - - - - - - - - - - -")
                    logger.debug(pformat(record))
                if record["port type"] == "WIFI-STA":
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
                        logger.debug("name:", port_eid, " Group 1: ", match.group(1))
                    if port_eid.find(prefix) >= 0:
                        matched_map[port_eid] = record

            elif pattern.find("*") > 0:
                match = re.search(r"^([^\*]+)[*]$", pattern)
                if match.group(1):
                    prefix = match.group(1)
                    if debug_:
                        logger.debug("group 1: ", prefix)
                for port_eid, record in prelim_map.items():
                    if port_eid.find(prefix) >= 0:
                        matched_map[port_eid] = record

            elif pattern.find("[") > 0:
                # TODO: regex below might have too many hack escapes
                match = re.search(r"^([^\[]+)\[(\d+)\.\.(\d+)\]$", pattern)
                if match.group(0):
                    if debug_:
                        logger.debug("[group1]: ", match.group(1))
                        logger.debug("[group2]: ", match.group(2))
                        logger.debug("[group3]: ", match.group(3))
                    prefix = match.group(1)
                    for port_eid, record in prelim_map.items():
                        if port_eid.find(prefix) >= 0:
                            port_suf = record["device"][len(prefix):]
                            if (port_suf >= match.group(2)) and (port_suf <= match.group(3)):
                                # logger.info("%s: suffix[%s] between %s:%s" % (port_name, port_name, match.group(2), match.group(3))
                                matched_map[port_eid] = record
        except ValueError as e:
            self.error(e)

        return matched_map

    def name_to_eid(self, eid, debug=False, non_port=False):
        if debug:
            self.logg(level="debug", mesg="name_to_eid: " + str(eid))
        if (type(eid) is list) or (type(eid) is tuple):
            return eid
        return LFUtils.name_to_eid(eid, non_port=non_port)

    def dump_all_port_info(self):
        return self.json_get('/port/all')

    # timemout_sec of -1 means auto-calculate based on number of stations.
    def wait_for_ip(self, station_list=None, ipv4=True, ipv6=False, timeout_sec=360, debug=False):
        timeout_auto = False

        if not (ipv4 or ipv6):
            raise ValueError("wait_for_ip: ipv4 and/or ipv6 must be set!")
        if timeout_sec >= 0:
            if debug:
                logger.debug("Waiting for ips, timeout: %i..." % timeout_sec)
        else:
            timeout_auto = True
            timeout_sec = 60 + len(station_list) * 5
            if debug:
                logger.debug("Auto-Timeout requested, using: %s" % timeout_sec)

        stas_without_ip4s = {}
        stas_without_ip6s = {}

        sec_elapsed = 0
        time_extended = False
        # logger.info(station_list)
        waiting_states = ["0.0.0.0", "NA", "", 'DELETED', 'AUTO']
        if (station_list is None) or (len(station_list) < 1):
            logger.critical("wait_for_ip: expects non-empty list of ports")
            raise ValueError("wait_for_ip: expects non-empty list of ports")
        wait_more = True

        while wait_more and (sec_elapsed <= timeout_sec):
            wait_more = False
            some_passed = False
            stas_without_ip4s = {}
            stas_without_ip6s = {}

            for sta_eid in station_list:
                eid = self.name_to_eid(sta_eid)

                response = super().json_get("/port/%s/%s/%s?fields=alias,ip,port+type,ipv6+address" %
                                            (eid[0], eid[1], eid[2]))
                # logger.info(pformat(response))

                if (response is None) or ("interface" not in response):
                    logger.info("station_list: incomplete response for eid: %s:" % sta_eid)
                    logger.info(pformat(response))
                    wait_more = True
                    break

                if ipv4:
                    v = response['interface']
                    if v['ip'] in waiting_states:
                        wait_more = True
                        stas_without_ip4s[sta_eid] = True
                        if debug:
                            logger.debug("Waiting for port %s to get IPv4 Address try %s / %s" % (sta_eid, sec_elapsed, timeout_sec))
                    else:
                        some_passed = True
                        if debug:
                            logger.debug("Found IP: %s on port: %s" % (v['ip'], sta_eid))

                if ipv6:
                    v = response['interface']
                    # logger.info(v)
                    ip6a = v['ipv6_address']
                    if ip6a != 'DELETED' and not ip6a.startswith('fe80') and ip6a != 'AUTO':
                        some_passed = True
                        if debug:
                            logger.debug("Found IPv6: %s on port: %s" % (ip6a, sta_eid))
                    else:
                        stas_without_ip6s[sta_eid] = True
                        wait_more = True
                        if debug:
                            logger.debug("Waiting for port %s to get IPv6 Address try %s / %s, reported: %s." % (sta_eid, sec_elapsed, timeout_sec, ip6a))

            if wait_more:
                if timeout_auto and not some_passed:
                    if sec_elapsed > 60:
                        # Nothing has gotten IP for 60 seconds, consider timeout reached.
                        break
                time.sleep(1)
                sec_elapsed += 1

        # If not all ports got IP addresses before timeout, and debugging is enabled, then
        # add logging.
        if len(stas_without_ip4s) + len(stas_without_ip6s) > 0:
            if debug:
                if len(stas_without_ip4s) > 0:
                    logger.info('%s did not acquire IPv4 addresses' % stas_without_ip4s.keys())
                if len(stas_without_ip6s) > 0:
                    logger.info('%s did not acquire IPv6 addresses' % stas_without_ip6s.keys())
                port_info = self.dump_all_port_info()
                logger.debug(pformat(self.dump_all_port_info()))
            return False
        else:
            if debug:
                logger.debug("Found IPs for all requested ports.")
            return True

    def get_curr_num_ips(self, num_sta_with_ips=0, station_list=None, ipv4=True, ipv6=False, debug=False):
        if debug:
            logger.debug("checking number of stations with ips...")
        waiting_states = ["0.0.0.0", "NA", ""]
        if (station_list is None) or (len(station_list) < 1):
            raise ValueError("check for num curr ips expects non-empty list of ports")
        for sta_eid in station_list:
            if debug:
                logger.debug("checking sta-eid: %s" % sta_eid)
            eid = self.name_to_eid(sta_eid)
            response = super().json_get("/port/%s/%s/%s?fields=alias,ip,port+type,ipv6+address" %
                                        (eid[0], eid[1], eid[2]))
            if debug:
                logger.debug(pformat(response))
            if (response is None) or ("interface" not in response):
                logger.info("station_list: incomplete response:")
                logger.info(pformat(response))
                # wait_more = True
                break
            if ipv4:
                v = response['interface']
                if v['ip'] in waiting_states:
                    if debug:
                        logger.debug("Waiting for port %s to get IPv4 Address." % sta_eid)
                else:
                    if debug:
                        logger.debug("Found IP: %s on port: %s" % (v['ip'], sta_eid))
                        logger.debug("Incrementing stations with IP addresses found")
                        num_sta_with_ips += 1
                    else:
                        num_sta_with_ips += 1
            if ipv6:
                v = response['interface']
                if v['ip'] in waiting_states:
                    if debug:
                        logger.debug("Waiting for port %s to get IPv6 Address." % sta_eid)

                else:
                    if debug:
                        logger.debug("Found IP: %s on port: %s" % (v['ip'], sta_eid))
                        logger.debug("Incrementing stations with IP addresses found")
                        num_sta_with_ips += 1
                    else:
                        num_sta_with_ips += 1
        return num_sta_with_ips

    @staticmethod
    def duration_time_to_seconds(time_string):
        if isinstance(time_string, str):
            pattern = re.compile("^(\d+)([dhms]$)")
            td = pattern.match(time_string)
            if td:
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
        if port_list:
            logger.info("Removing all stations")
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
        if endp_list:
            logger.info("Removing all endps")
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
        if self.cx_list():
            cx_list = list(self.cx_list())
            not_cx = ['warnings', 'errors', 'handler', 'uri', 'items', 'empty']
            if cx_list:
                logger.info("Removing all cxs")
                for cx_name in cx_list:
                    if cx_name in not_cx:
                        continue
                    req_url = "cli-json/rm_cx"
                    data = {
                        "test_mgr": "default_tm",
                        "cx_name": cx_name
                    }
                    self.json_post(req_url, data)
        else:
            logger.info("no cxs to remove")

        if remove_all_endpoints:
            self.remove_all_endps()
            req_url = "cli-json/nc_show_endpoints"
            data = {
                "endpoint": "all"
            }
            self.json_post(req_url, data)

    def parse_link(self, link):
        link = self.lfclient_url + link
        info = ()

    @staticmethod
    def get_events(event_log, value):
        results = []
        if event_log:
            for event in event_log['events']:
                if event.values():
                    results.append(list(event.values())[0][value])
        return results

    # Find events since the given the last number from the original list of events
    def find_new_events(self, previous_event_id):
        return self.json_get('/events/since/%s' % previous_event_id)

    def new_station_profile(self, ipv6=False):
        return StationProfile(self.lfclient_url, local_realm=self, debug_=self.debug, ipv6=ipv6, up=False)

    def new_multicast_profile(self):
        return MULTICASTProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug,
                                report_timer_=3000)

    def new_wifi_monitor_profile(self, resource_=1, debug_=False, up_=False):
        return WifiMonitor(self.lfclient_url,
                           local_realm=self,
                           resource_=resource_,
                           up=up_,
                           debug_=(self.debug or debug_))

    def new_l3_cx_profile(self):
        return L3CXProfile(self.lfclient_host,
                           self.lfclient_port,
                           local_realm=self,
                           debug_=self.debug,
                           report_timer_=3000)

    def new_l4_cx_profile(self):
        return L4CXProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)

    def new_attenuator_profile(self):
        return ATTENUATORProfile(self.lfclient_host, self.lfclient_port, debug_=self.debug)

    def new_generic_endp_profile(self):
        return GenCXProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)

    def new_generic_cx_profile(self):
        """
        @deprecated
        :return: new GenCXProfile
        """
        return GenCXProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)

    def new_vap_profile(self):
        return VAPProfile(lfclient_host=self.lfclient_host, lfclient_port=self.lfclient_port, local_realm=self,
                          debug_=self.debug)

    # def new_vr_profile(self):
    # return VRProfile(local_realm=self,
    # debug=self.debug)

    def new_http_profile(self):
        return HTTPProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)

    def new_fio_endp_profile(self):
        return FIOEndpProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)

    def new_dut_profile(self):
        return DUTProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)

    def new_mvlan_profile(self):
        return MACVLANProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)

    def new_qvlan_profile(self):
        return QVLANProfile(self.host, self.port, local_realm=self, debug_=self.debug)

    def new_test_group_profile(self):
        return TestGroupProfile(self.lfclient_host, self.lfclient_port, local_realm=self, debug_=self.debug)

    def new_lf_data_collection(self):
        return LFDataCollection(local_realm=self)


class PacketFilter:

    @staticmethod
    def get_filter_wlan_assoc_packets(ap_mac, sta_mac):
        return "-T fields -e wlan.fc.type_subtype -e wlan.addr -e wlan.fc.pwrmgt " \
               "-Y \"(wlan.addr==%s or wlan.addr==%s) and wlan.fc.type_subtype<=3\" " % (ap_mac, sta_mac)

    @staticmethod
    def get_filter_wlan_null_packets(ap_mac, sta_mac):
        return "-T fields -e wlan.fc.type_subtype -e wlan.addr -e wlan.fc.pwrmgt " \
               "-Y \"(wlan.addr==%s or wlan.addr==%s) and wlan.fc.type_subtype==44\" " % (ap_mac, sta_mac)

    @staticmethod
    def run_filter(pcap_file, file_filter):
        filename = "/tmp/tshark_dump.txt"
        cmd = "tshark -r %s %s > %s" % (pcap_file, file_filter, filename)
        # logger.info("CMD: ", cmd)
        os.system(cmd)
        lines = []
        with open(filename) as tshark_file:
            for line in tshark_file:
                lines.append(line.rstrip())

        return lines
