#!/usr/bin/env python3

#########################################################################################################
# Built to allow connection and test of clients using EAP-TTLS.
# Functions can be called to create a station, create TCP and UDP traffic, run it a short amount of time.
#
# Used by Nightly_Sanity and Throughput_Test ############################################################
#########################################################################################################

#  This will create a station, create TCP and UDP traffic, run it a short amount of time,
#  and verify whether traffic was sent and received.  It also verifies the station connected
#  to the requested BSSID if bssid is specified as an argument.
#  The script will clean up the station and connections at the end of the test.
import sys
import os
import importlib
import time
import argparse
import pprint

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
removeCX = LFUtils.removeCX
removeEndps = LFUtils.removeEndps
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm

OPEN = "open"
WEP = "wep"
WPA = "wpa"
WPA2 = "wpa2"
MODE_AUTO = 0


class EAPConnect(LFCliBase):
    def __init__(self, host, port, security=None, ssid=None, sta_list=None, number_template="00000", _debug_on=False, _dut_bssid="",
                 _exit_on_error=False, _sta_name=None, _resource=1, radio="wiphy0", key_mgmt="WPA-EAP", eap="", identity="",
                 ttls_passwd="", hessid=None, ttls_realm="", domain="", _sta_prefix='eap', _exit_on_fail=False, _cleanup_on_exit=True):
        super().__init__(host, port, _debug=_debug_on, _exit_on_fail=_exit_on_fail)
        self.host = host
        self.port = port
        self.ssid = ssid
        self.radio = radio
        self.security = security
        #self.password = password
        self.sta_list = sta_list
        self.key_mgmt = key_mgmt
        self.eap = eap
        self.sta_prefix = _sta_prefix
        self.identity = identity
        self.ttls_passwd = ttls_passwd
        self.ttls_realm = ttls_realm
        self.domain = domain
        self.hessid = hessid
        self.dut_bssid = _dut_bssid
        self.timeout = 120
        self.number_template = number_template
        self.debug = _debug_on
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.mode = 0
        #Added to test_ipv4_ttls code
        self.upstream_url = None  # defer construction
        self.sta_url_map = None
        self.upstream_resource = None
        self.upstream_port = "eth2"
        self.station_names = []
        if _sta_name is not None:
            self.station_names = [_sta_name]
        self.localrealm = Realm(lfclient_host=host, lfclient_port=port)
        self.resource = _resource
        self.cleanup_on_exit = _cleanup_on_exit
        self.resulting_stations = {}
        self.resulting_endpoints = {}
        self.station_profile = None
        self.l3_udp_profile = None
        self.l3_tcp_profile = None

    # def get_realm(self) -> Realm: # py > 3.6
    def get_realm(self):
        return self.localrealm

    def get_station_url(self, sta_name_=None):
        if sta_name_ is None:
            raise ValueError("get_station_url wants a station name")
        if self.sta_url_map is None:
            self.sta_url_map = {}
            for sta_name in self.station_names:
                self.sta_url_map[sta_name] = "port/1/%s/%s" % (self.resource, sta_name)
        return self.sta_url_map[sta_name_]

    def get_upstream_url(self):
        if self.upstream_url is None:
            self.upstream_url = "port/1/%s/%s" % (self.upstream_resource, self.upstream_port)
        return self.upstream_url

    # Compare pre-test values to post-test values
    def compare_vals(self, name, postVal, print_pass=False, print_fail=True):
        # print(f"Comparing {name}")
        if postVal > 0:
            self._pass("%s %s" % (name, postVal), print_pass)
        else:
            self._fail("%s did not report traffic: %s" % (name, postVal), print_fail)

    def remove_stations(self):
        for name in self.station_names:
            LFUtils.removePort(self.resource, name, self.lfclient_url)

    def num_associated(self, bssid):
        counter = 0
        # print("there are %d results" % len(self.station_results))
        fields = "_links,port,alias,ip,ap,port+type"
        self.station_results = self.localrealm.find_ports_like("%s*"%self.sta_prefix, fields, debug_=False)
        if (self.station_results is None) or (len(self.station_results) < 1):
            self.get_failed_result_list()
        for eid,record in self.station_results.items():
            #print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- ")
            #pprint(eid)
            #pprint(record)
            if record["ap"] == bssid:
                counter += 1
            #print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- ")
        return counter

    def clear_test_results(self):
        self.resulting_stations = {}
        self.resulting_endpoints = {}
        super().clear_test_results()
        #super(StaConnect, self).clear_test_results().test_results.clear()

    def setup(self):
        self.clear_test_results()
        self.check_connect()
        upstream_json = self.json_get("%s?fields=alias,phantom,down,port,ip" % self.get_upstream_url(), debug_=False)

        if upstream_json is None:
            self._fail(message="Unable to query %s, bye" % self.upstream_port, print_=True)
            return False

        if upstream_json['interface']['ip'] == "0.0.0.0":
            if self.debug:
                pprint.pprint(upstream_json)
            self._fail("Warning: %s lacks ip address" % self.get_upstream_url(), print_=True)
            return False

        # remove old stations
        print("Removing old stations")
        for sta_name in self.station_names:
            sta_url = self.get_station_url(sta_name)
            response = self.json_get(sta_url)
            if (response is not None) and (response["interface"] is not None):
                for sta_name in self.station_names:
                    LFUtils.removePort(self.resource, sta_name, self.lfclient_url)
        LFUtils.wait_until_ports_disappear(self.lfclient_url, self.station_names)

        # Create stations and turn dhcp on
        self.station_profile = self.localrealm.new_station_profile()

        # Build stations
        self.station_profile.use_security(self.security, self.ssid, passwd="[BLANK]")
        self.station_profile.set_number_template(self.number_template)
        print("Creating stations")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.set_wifi_extra(key_mgmt=self.key_mgmt, eap=self.eap, identity=self.identity,
                                            passwd=self.ttls_passwd,
                                            realm=self.ttls_realm, domain=self.domain,
                                            hessid=self.hessid)
        self.station_profile.create(radio=self.radio, sta_names_=self.sta_list, debug=self.debug, use_radius=True, hs20_enable=False)
        self._pass("PASS: Station build finished")

        # Create UDP endpoints
        self.l3_udp_profile = self.localrealm.new_l3_cx_profile()
        self.l3_udp_profile.side_a_min_bps = 128000
        self.l3_udp_profile.side_b_min_bps = 128000
        self.l3_udp_profile.side_a_min_pdu = 1200
        self.l3_udp_profile.side_b_min_pdu = 1500
        self.l3_udp_profile.report_timer = 1000
        self.l3_udp_profile.name_prefix = "udp"
        self.l3_udp_profile.create(endp_type="lf_udp",
                                   side_a=list(self.localrealm.find_ports_like("%s*"%self.sta_prefix)),
                                   side_b="%d.%s" % (self.resource, self.upstream_port),
                                   suppress_related_commands=True)

        # Create TCP endpoints
        self.l3_tcp_profile = self.localrealm.new_l3_cx_profile()
        self.l3_tcp_profile.side_a_min_bps = 128000
        self.l3_tcp_profile.side_b_min_bps = 56000
        self.l3_tcp_profile.name_prefix = "tcp"
        self.l3_tcp_profile.report_timer = 1000
        self.l3_tcp_profile.create(endp_type="lf_tcp",
                                   side_a=list(self.localrealm.find_ports_like("%s*"%self.sta_prefix)),
                                   side_b="%d.%s" % (self.resource, self.upstream_port),
                                   suppress_related_commands=True)

    def start(self):
        if self.station_profile is None:
            self._fail("Incorrect setup")
        pprint.pprint(self.station_profile)
        if self.station_profile.up is None:
            self._fail("Incorrect station profile, missing profile.up")
        if self.station_profile.up == False:
            print("\nBringing ports up...")
            data = {"shelf": 1,
                     "resource": self.resource,
                     "port": "ALL",
                     "probe_flags": 1}
            self.json_post("/cli-json/nc_show_ports", data)
            self.station_profile.admin_up()
            LFUtils.waitUntilPortsAdminUp(self.resource, self.lfclient_url, self.station_names)

        # station_info = self.jsonGet(self.mgr_url, "%s?fields=port,ip,ap" % (self.getStaUrl()))
        duration = 0
        maxTime = 60
        ip = "0.0.0.0"
        ap = ""
        print("Waiting for %s stations to associate to AP: " % len(self.station_names), end="")
        connected_stations = {}
        while (len(connected_stations.keys()) < len(self.station_names)) and (duration < maxTime):
            duration += 3
            time.sleep(3)
            print(".", end="")
            for sta_name in self.station_names:
                sta_url = self.get_station_url(sta_name)
                station_info = self.json_get(sta_url + "?fields=port,ip,ap")

                # LFUtils.debug_printer.pprint(station_info)
                if (station_info is not None) and ("interface" in station_info):
                    if "ip" in station_info["interface"]:
                        ip = station_info["interface"]["ip"]
                    if "ap" in station_info["interface"]:
                        ap = station_info["interface"]["ap"]

                if (ap == "Not-Associated") or (ap == ""):
                    if self.debug:
                        print(" -%s," % sta_name, end="")
                else:
                    if ip == "0.0.0.0":
                        if self.debug:
                            print(" %s (0.0.0.0)" % sta_name, end="")
                    else:
                        connected_stations[sta_name] = sta_url
            data = {
                "shelf":1,
                "resource": self.resource,
                "port": "ALL",
                "probe_flags": 1
            }
            self.json_post("/cli-json/nc_show_ports", data)

        for sta_name in self.station_names:
            sta_url = self.get_station_url(sta_name)
            station_info = self.json_get(sta_url) # + "?fields=port,ip,ap")
            if station_info is None:
                print("unable to query %s" % sta_url)
            self.resulting_stations[sta_url] = station_info
            ap = station_info["interface"]["ap"]
            ip = station_info["interface"]["ip"]
            if (ap != "") and (ap != "Not-Associated"):
                print(" %s +AP %s, " % (sta_name, ap), end="")
                if self.dut_bssid != "":
                    if self.dut_bssid.lower() == ap.lower():
                        self._pass(sta_name+" connected to BSSID: " + ap)
                        # self.test_results.append("PASSED: )
                        # print("PASSED: Connected to BSSID: "+ap)
                    else:
                        self._fail("%s connected to wrong BSSID, requested: %s  Actual: %s" % (sta_name, self.dut_bssid, ap))
            else:
                self._fail(sta_name+" did not connect to AP")
                return False

            if ip == "0.0.0.0":
                self._fail("%s did not get an ip. Ending test" % sta_name)
            else:
                self._pass("%s connected to AP: %s  With IP: %s" % (sta_name, ap, ip))

        if self.passes() == False:
            if self.cleanup_on_exit:
                print("Cleaning up...")
                self.remove_stations()
            return False

        # start cx traffic
        print("\nStarting CX Traffic")
        self.l3_udp_profile.start_cx()
        self.l3_tcp_profile.start_cx()
        time.sleep(1)
        # Refresh stats
        self.l3_udp_profile.refresh_cx()
        self.l3_tcp_profile.refresh_cx()

    def collect_endp_stats(self, endp_map):
        print("Collecting Data")
        fields="?fields=name,tx+bytes,rx+bytes"
        for (cx_name, endps) in endp_map.items():
            try:
                endp_url = "/endp/%s%s" % (endps[0], fields)
                endp_json = self.json_get(endp_url)
                self.resulting_endpoints[endp_url] = endp_json
                ptest_a_tx = endp_json['endpoint']['tx bytes']
                ptest_a_rx = endp_json['endpoint']['rx bytes']

                #ptest = self.json_get("/endp/%s?fields=tx+bytes,rx+bytes" % cx_names[cx_name]["b"])
                endp_url = "/endp/%s%s" % (endps[1], fields)
                endp_json = self.json_get(endp_url)
                self.resulting_endpoints[endp_url] = endp_json

                ptest_b_tx = endp_json['endpoint']['tx bytes']
                ptest_b_rx = endp_json['endpoint']['rx bytes']

                self.compare_vals("testTCP-A TX", ptest_a_tx)
                self.compare_vals("testTCP-A RX", ptest_a_rx)

                self.compare_vals("testTCP-B TX", ptest_b_tx)
                self.compare_vals("testTCP-B RX", ptest_b_rx)

            except Exception as e:
                print("Is this the function having the error?")
                self.error(e)


    def stop(self):
        # stop cx traffic
        print("Stopping CX Traffic")
        self.l3_udp_profile.stop_cx()
        self.l3_tcp_profile.stop_cx()

        # Refresh stats
        print("\nRefresh CX stats")
        self.l3_udp_profile.refresh_cx()
        self.l3_tcp_profile.refresh_cx()

        print("Sleeping for 5 seconds")
        time.sleep(5)

        # get data for endpoints JSON
        self.collect_endp_stats(self.l3_udp_profile.created_cx)
        self.collect_endp_stats(self.l3_tcp_profile.created_cx)
        # print("\n")

    def cleanup(self):
        # remove all endpoints and cxs
        if self.cleanup_on_exit:
            for sta_name in self.station_names:
                LFUtils.removePort(self.resource, sta_name, self.lfclient_url)
            curr_endp_names = []
            removeCX(self.lfclient_url, self.l3_udp_profile.get_cx_names())
            removeCX(self.lfclient_url, self.l3_tcp_profile.get_cx_names())
            for (cx_name, endp_names) in self.l3_udp_profile.created_cx.items():
                curr_endp_names.append(endp_names[0])
                curr_endp_names.append(endp_names[1])
            for (cx_name, endp_names) in self.l3_tcp_profile.created_cx.items():
                curr_endp_names.append(endp_names[0])
                curr_endp_names.append(endp_names[1])        
            removeEndps(self.lfclient_url, curr_endp_names, debug= self.debug)

# ~class



if __name__ == "__main__":
    main()
