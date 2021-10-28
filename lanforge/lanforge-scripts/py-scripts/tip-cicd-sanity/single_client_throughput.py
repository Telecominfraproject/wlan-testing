#!/usr/bin/env python3

####################################################################################
# Script is based off of LANForge sta_connect2.py
# Script built for max throughput testing on a single client
#  The main function of the script creates a station, then tests:
#   1. UDP Downstream (AP to STA)
#   2. UDP Upstream (STA to AP)
#   3. TCP Downstream (AP to STA)
#   4. TCP Upstream (STA to AP)
#  The script will clean up the station and connections at the end of the test.
#
# Used by Throughput_Test ###########################################################
####################################################################################

# Script is based off of sta_connect2.py
# Script built for max throughput testing on a single client
#  The main function of the script creates a station, then tests:
#   1. UDP Downstream (AP to STA)
#   2. UDP Upstream (STA to AP)
#   3. TCP Downstream (AP to STA)
#   4. TCP Upstream (STA to AP)
#  The script will clean up the station and connections at the end of the test.
import sys
import os
import importlib
import csv
import argparse
import pprint
import time

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
removeCX = LFUtils.removeCX
removeEndps = LFUtils.removeEndps
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm

OPEN = "open"
WEP = "wep"
WPA = "wpa"
WPA2 = "wpa2"
MODE_AUTO = 0


class SingleClient(LFCliBase):
    def __init__(self, host, port, _dut_ssid="jedway-open-1", _dut_passwd="NA", _dut_bssid="",
                 _user="", _passwd="", _sta_mode="0", _radio="wiphy0",
                 _resource=1, _upstream_resource=1, _upstream_port="eth1",
                 _sta_name=None, debug_=False, _dut_security=OPEN, _exit_on_error=False,
                 _cleanup_on_exit=True, _runtime_sec=60, _exit_on_fail=False):
        # do not use `super(LFCLiBase,self).__init__(self, host, port, _debugOn)
        # that is py2 era syntax and will force self into the host variable, making you
        # very confused.
        super().__init__(host, port, _debug=debug_, _exit_on_fail=_exit_on_fail)
        self.debug = debug_
        self.dut_security = _dut_security
        self.dut_ssid = _dut_ssid
        self.dut_passwd = _dut_passwd
        self.dut_bssid = _dut_bssid
        self.user = _user
        self.passwd = _passwd
        self.sta_mode = _sta_mode  # See add_sta LANforge CLI users guide entry
        self.radio = _radio
        self.resource = _resource
        self.upstream_resource = _upstream_resource
        self.upstream_port = _upstream_port
        self.runtime_secs = _runtime_sec
        self.cleanup_on_exit = _cleanup_on_exit
        self.sta_url_map = None  # defer construction
        self.upstream_url = None  # defer construction
        self.station_names = []
        if _sta_name is not None:
            self.station_names = [ _sta_name ]
        # self.localrealm :Realm = Realm(lfclient_host=host, lfclient_port=port) # py > 3.6
        self.localrealm = Realm(lfclient_host=host, lfclient_port=port) # py > 3.6
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
        self.station_results = self.localrealm.find_ports_like("sta*", fields, debug_=False)
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

        if self.dut_security == WPA2:
            self.station_profile.use_security(security_type="wpa2", ssid=self.dut_ssid, passwd=self.dut_passwd)
        elif self.dut_security == WPA:
            self.station_profile.use_security(security_type="wpa", ssid=self.dut_ssid, passwd=self.dut_passwd)
        elif self.dut_security == OPEN:
            self.station_profile.use_security(security_type="open", ssid=self.dut_ssid, passwd="[BLANK]")
        elif self.dut_security == WPA:
            self.station_profile.use_security(security_type="wpa", ssid=self.dut_ssid, passwd=self.dut_passwd)
        elif self.dut_security == WEP:
            self.station_profile.use_security(security_type="wep", ssid=self.dut_ssid, passwd=self.dut_passwd)
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)

        print("Adding new stations ", end="")
        self.station_profile.create(radio=self.radio, sta_names_=self.station_names, up_=False, debug=self.debug, suppress_related_commands_=True)
        LFUtils.wait_until_ports_appear(self.lfclient_url, self.station_names, debug=self.debug)

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
        maxTime = 100
        ip = "0.0.0.0"
        ap = ""
        print("Waiting for %s stations to associate to AP: " % len(self.station_names), end="")
        connected_stations = {}
        while (len(connected_stations.keys()) < len(self.station_names)) and (duration < maxTime):
            duration += 3
            time.sleep(10)
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

    def udp_profile(self, side_a_min_bps, side_b_min_bps, side_a_min_pdu, side_b_min_pdu):
        # Create UDP endpoint - Alex's code!
        self.l3_udp_tput_profile = self.localrealm.new_l3_cx_profile()
        self.l3_udp_tput_profile.side_a_min_bps = side_a_min_bps
        self.l3_udp_tput_profile.side_b_min_bps = side_b_min_bps
        self.l3_udp_tput_profile.side_a_min_pdu = side_a_min_pdu
        self.l3_udp_tput_profile.side_b_min_pdu = side_b_min_pdu
        self.l3_udp_tput_profile.report_timer = 1000
        self.l3_udp_tput_profile.name_prefix = "udp"
        self.l3_udp_tput_profile.create(endp_type="lf_udp",
                                      side_a=list(self.localrealm.find_ports_like("tput+")),
                                      side_b="%d.%s" % (self.resource, self.upstream_port),
                                      suppress_related_commands=True)

    def tcp_profile(self, side_a_min_bps, side_b_min_bps):
        # Create TCP endpoints - original code!
        self.l3_tcp_tput_profile = self.localrealm.new_l3_cx_profile()
        self.l3_tcp_tput_profile.side_a_min_bps = side_a_min_bps
        self.l3_tcp_tput_profile.side_b_min_bps = side_b_min_bps
        self.l3_tcp_tput_profile.name_prefix = "tcp"
        self.l3_tcp_tput_profile.report_timer = 1000
        self.l3_tcp_tput_profile.create(endp_type="lf_tcp",
                                    side_a=list(self.localrealm.find_ports_like("tput+")),
                                    side_b="%d.%s" % (self.resource, self.upstream_port),
                                    suppress_related_commands=True)

    # Start UDP Downstream Traffic
    def udp_throughput(self):
        print("\nStarting UDP Traffic")
        self.l3_udp_tput_profile.start_cx()
        time.sleep(1)
        self.l3_udp_tput_profile.refresh_cx()

    def tcp_throughput(self):
        print("\nStarting TCP Traffic")
        self.l3_tcp_tput_profile.start_cx()
        time.sleep(1)
        self.l3_tcp_tput_profile.refresh_cx()

    def udp_stop(self):
        # stop cx traffic
        print("Stopping CX Traffic")
        self.l3_udp_tput_profile.stop_cx()

        # Refresh stats
        print("\nRefresh CX stats")
        self.l3_udp_tput_profile.refresh_cx()

        print("Sleeping for 5 seconds")
        time.sleep(5)

        # get data for endpoints JSON
        return self.collect_client_stats(self.l3_udp_tput_profile.created_cx)
        # print("\n")

    def tcp_stop(self):
        # stop cx traffic
        print("Stopping CX Traffic")
        self.l3_tcp_tput_profile.stop_cx()

        # Refresh stats
        print("\nRefresh CX stats")
        self.l3_tcp_tput_profile.refresh_cx()

        print("Sleeping for 5 seconds")
        time.sleep(5)

        # get data for endpoints JSON
        return self.collect_client_stats(self.l3_tcp_tput_profile.created_cx)
        # print("\n")

    # New Endpoint code to print TX and RX numbers
    def collect_client_stats(self, endp_map):
        print("Collecting Data")
        fields="?fields=name,tx+bytes,rx+bytes"
        for (cx_name, endps) in endp_map.items():
            try:
                endp_url = "/endp/%s%s" % (endps[0], fields)
                endp_json = self.json_get(endp_url)
                self.resulting_endpoints[endp_url] = endp_json
                ptest_a_tx = endp_json['endpoint']['tx bytes']
                ptest_a_rx = endp_json['endpoint']['rx bytes']

                # ptest = self.json_get("/endp/%s?fields=tx+bytes,rx+bytes" % cx_names[cx_name]["b"])
                endp_url = "/endp/%s%s" % (endps[1], fields)
                endp_json = self.json_get(endp_url)
                self.resulting_endpoints[endp_url] = endp_json
                ptest_b_tx = endp_json['endpoint']['tx bytes']
                ptest_b_rx = endp_json['endpoint']['rx bytes']

                byte_values = []
                byte_values.append("Station TX: " + str(ptest_a_tx))
                byte_values.append("Station RX: " + str(ptest_a_rx))
                byte_values.append("AP TX: " + str(ptest_b_tx))
                byte_values.append("AP RX: " + str(ptest_b_rx))

                return byte_values

            except Exception as e:
                self.error(e)

    def cleanup_udp(self):
        # remove all endpoints and cxs
        if self.cleanup_on_exit:
            for sta_name in self.station_names:
                LFUtils.removePort(self.resource, sta_name, self.lfclient_url)
            curr_endp_names = []
            removeCX(self.lfclient_url, self.l3_udp_tput_profile.get_cx_names())
            for (cx_name, endp_names) in self.l3_udp_tput_profile.created_cx.items():
                curr_endp_names.append(endp_names[0])
                curr_endp_names.append(endp_names[1])
            removeEndps(self.lfclient_url, curr_endp_names, debug= self.debug)

    def cleanup_tcp(self):
        # remove all endpoints and cxs
        if self.cleanup_on_exit:
            for sta_name in self.station_names:
                LFUtils.removePort(self.resource, sta_name, self.lfclient_url)
            curr_endp_names = []
            removeCX(self.lfclient_url, self.l3_tcp_tput_profile.get_cx_names())
            for (cx_name, endp_names) in self.l3_tcp_tput_profile.created_cx.items():
                curr_endp_names.append(endp_names[0])
                curr_endp_names.append(endp_names[1])
            removeEndps(self.lfclient_url, curr_endp_names, debug= self.debug)

    def cleanup(self):
        # remove all endpoints and cxs
        if self.cleanup_on_exit:
            for sta_name in self.station_names:
                LFUtils.removePort(self.resource, sta_name, self.lfclient_url)
            curr_endp_names = []
            removeCX(self.lfclient_url, self.l3_tcp_tput_profile.get_cx_names())
            removeCX(self.lfclient_url, self.l3_udp_tput_profile.get_cx_names())
            for (cx_name, endp_names) in self.l3_tcp_tput_profile.created_cx.items():
                curr_endp_names.append(endp_names[0])
                curr_endp_names.append(endp_names[1])
            for (cx_name, endp_names) in self.l3_udp_tput_profile.created_cx.items():
                curr_endp_names.append(endp_names[0])
                curr_endp_names.append(endp_names[1])
            removeEndps(self.lfclient_url, curr_endp_names, debug=self.debug)

    def udp_unidirectional(self, side_a_min_bps, side_b_min_bps, side_a_min_pdu, side_b_min_pdu, direction, values_line):
        self.udp_profile(side_a_min_bps, side_b_min_bps, side_a_min_pdu, side_b_min_pdu)
        self.start()
        print("Running", direction, "Traffic for %s seconds" % self.runtime_secs)
        self.udp_throughput()
        print("napping %f sec" % self.runtime_secs)
        time.sleep(self.runtime_secs)
        values = self.udp_stop()
        print(values)
        # Get value required for measurement
        bytes = values[values_line]
        # Get value in Bits and convert to Mbps
        bits = (int(bytes.split(": ", 1)[1])) * 8
        mpbs = round((bits / 1000000) / self.runtime_secs, 2)
        return mpbs

    def tcp_unidirectional(self, side_a_min_bps, side_b_min_bps, direction, values_line):
        self.tcp_profile(side_a_min_bps, side_b_min_bps)
        self.start()
        print("Running", direction, "Traffic for %s seconds" % self.runtime_secs)
        self.tcp_throughput()
        print("napping %f sec" % self.runtime_secs)
        time.sleep(self.runtime_secs)
        values = self.tcp_stop()
        print(values)
        # Get value required for measurement
        bytes = values[values_line]
        # Get value in Bits and convert to Mbps
        bits = (int(bytes.split(": ", 1)[1])) * 8
        mpbs = round((bits / 1000000) / self.runtime_secs, 2)
        return mpbs

    def throughput_csv(csv_file, ssid_name, ap_model, firmware, security, udp_ds, udp_us, tcp_ds, tcp_us):
           # Find band for CSV ---> This code is not great, it SHOULD get that info from LANForge!
        if "5G" in ssid_name:
            frequency = "5 GHz"

        elif "2dot4G" in ssid_name:
            frequency = "2.4 GHz"

        else:
            frequency = "Unknown"

        # Append row to top of CSV file
        row = [ap_model, firmware, frequency, security, udp_ds, udp_us, tcp_ds, tcp_us]

        with open(csv_file, 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            lines.insert(1, row)

        with open(csv_file, 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)

        readFile.close()
        writeFile.close()


class SingleClientEAP(LFCliBase):
    def __init__(self, host, port, security=None, ssid=None, sta_list=None, number_template="00000", _debug_on=False, _dut_bssid="",
                 _exit_on_error=False, _sta_name=None, _resource=1, radio="wiphy0", key_mgmt="WPA-EAP", eap="", identity="",
                 ttls_passwd="", hessid=None, ttls_realm="", domain="", _exit_on_fail=False, _cleanup_on_exit=True):
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
        self.upstream_port = None
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
        self.station_results = self.localrealm.find_ports_like("eap*", fields, debug_=False)
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
        maxTime = 30
        ip = "0.0.0.0"
        ap = ""
        print("Waiting for %s stations to associate to AP: " % len(self.station_names), end="")
        connected_stations = {}
        while (len(connected_stations.keys()) < len(self.station_names)) and (duration < maxTime):
            duration += 3
            time.sleep(10)
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

    def udp_profile(self, side_a_min_bps, side_b_min_bps, side_a_min_pdu, side_b_min_pdu):
        # Create UDP endpoint - Alex's code!
        self.l3_udp_tput_profile = self.localrealm.new_l3_cx_profile()
        self.l3_udp_tput_profile.side_a_min_bps = side_a_min_bps
        self.l3_udp_tput_profile.side_b_min_bps = side_b_min_bps
        self.l3_udp_tput_profile.side_a_min_pdu = side_a_min_pdu
        self.l3_udp_tput_profile.side_b_min_pdu = side_b_min_pdu
        self.l3_udp_tput_profile.report_timer = 1000
        self.l3_udp_tput_profile.name_prefix = "udp"
        self.l3_udp_tput_profile.create(endp_type="lf_udp",
                                      side_a=list(self.localrealm.find_ports_like("tput+")),
                                      side_b="%d.%s" % (self.resource, self.upstream_port),
                                      suppress_related_commands=True)

    def tcp_profile(self, side_a_min_bps, side_b_min_bps):
        # Create TCP endpoints - original code!
        self.l3_tcp_tput_profile = self.localrealm.new_l3_cx_profile()
        self.l3_tcp_tput_profile.side_a_min_bps = side_a_min_bps
        self.l3_tcp_tput_profile.side_b_min_bps = side_b_min_bps
        self.l3_tcp_tput_profile.name_prefix = "tcp"
        self.l3_tcp_tput_profile.report_timer = 1000
        self.l3_tcp_tput_profile.create(endp_type="lf_tcp",
                                    side_a=list(self.localrealm.find_ports_like("tput+")),
                                    side_b="%d.%s" % (self.resource, self.upstream_port),
                                    suppress_related_commands=True)

    # Start UDP Downstream Traffic
    def udp_throughput(self):
        print("\nStarting UDP Traffic")
        self.l3_udp_tput_profile.start_cx()
        time.sleep(1)
        self.l3_udp_tput_profile.refresh_cx()

    def tcp_throughput(self):
        print("\nStarting TCP Traffic")
        self.l3_tcp_tput_profile.start_cx()
        time.sleep(1)
        self.l3_tcp_tput_profile.refresh_cx()

    def udp_stop(self):
        # stop cx traffic
        print("Stopping CX Traffic")
        self.l3_udp_tput_profile.stop_cx()

        # Refresh stats
        print("\nRefresh CX stats")
        self.l3_udp_tput_profile.refresh_cx()

        print("Sleeping for 5 seconds")
        time.sleep(5)

        # get data for endpoints JSON
        return self.collect_client_stats(self.l3_udp_tput_profile.created_cx)
        # print("\n")

    def tcp_stop(self):
        # stop cx traffic
        print("Stopping CX Traffic")
        self.l3_tcp_tput_profile.stop_cx()

        # Refresh stats
        print("\nRefresh CX stats")
        self.l3_tcp_tput_profile.refresh_cx()

        print("Sleeping for 5 seconds")
        time.sleep(5)

        # get data for endpoints JSON
        return self.collect_client_stats(self.l3_tcp_tput_profile.created_cx)
        # print("\n")

    # New Endpoint code to print TX and RX numbers
    def collect_client_stats(self, endp_map):
        print("Collecting Data")
        fields="?fields=name,tx+bytes,rx+bytes"
        for (cx_name, endps) in endp_map.items():
            try:
                endp_url = "/endp/%s%s" % (endps[0], fields)
                endp_json = self.json_get(endp_url)
                self.resulting_endpoints[endp_url] = endp_json
                ptest_a_tx = endp_json['endpoint']['tx bytes']
                ptest_a_rx = endp_json['endpoint']['rx bytes']

                # ptest = self.json_get("/endp/%s?fields=tx+bytes,rx+bytes" % cx_names[cx_name]["b"])
                endp_url = "/endp/%s%s" % (endps[1], fields)
                endp_json = self.json_get(endp_url)
                self.resulting_endpoints[endp_url] = endp_json
                ptest_b_tx = endp_json['endpoint']['tx bytes']
                ptest_b_rx = endp_json['endpoint']['rx bytes']

                byte_values = []
                byte_values.append("Station TX: " + str(ptest_a_tx))
                byte_values.append("Station RX: " + str(ptest_a_rx))
                byte_values.append("AP TX: " + str(ptest_b_tx))
                byte_values.append("AP RX: " + str(ptest_b_rx))

                return byte_values

            except Exception as e:
                self.error(e)

    def cleanup_udp(self):
        # remove all endpoints and cxs
        if self.cleanup_on_exit:
            for sta_name in self.station_names:
                LFUtils.removePort(self.resource, sta_name, self.lfclient_url)
            curr_endp_names = []
            removeCX(self.lfclient_url, self.l3_udp_tput_profile.get_cx_names())
            for (cx_name, endp_names) in self.l3_udp_tput_profile.created_cx.items():
                curr_endp_names.append(endp_names[0])
                curr_endp_names.append(endp_names[1])
            removeEndps(self.lfclient_url, curr_endp_names, debug= self.debug)

    def cleanup_tcp(self):
        # remove all endpoints and cxs
        if self.cleanup_on_exit:
            for sta_name in self.station_names:
                LFUtils.removePort(self.resource, sta_name, self.lfclient_url)
            curr_endp_names = []
            removeCX(self.lfclient_url, self.l3_tcp_tput_profile.get_cx_names())
            for (cx_name, endp_names) in self.l3_tcp_tput_profile.created_cx.items():
                curr_endp_names.append(endp_names[0])
                curr_endp_names.append(endp_names[1])
            removeEndps(self.lfclient_url, curr_endp_names, debug= self.debug)

    def cleanup(self):
        # remove all endpoints and cxs
        if self.cleanup_on_exit:
            for sta_name in self.station_names:
                LFUtils.removePort(self.resource, sta_name, self.lfclient_url)
            curr_endp_names = []
            removeCX(self.lfclient_url, self.l3_tcp_tput_profile.get_cx_names())
            removeCX(self.lfclient_url, self.l3_udp_tput_profile.get_cx_names())
            for (cx_name, endp_names) in self.l3_tcp_tput_profile.created_cx.items():
                curr_endp_names.append(endp_names[0])
                curr_endp_names.append(endp_names[1])
            for (cx_name, endp_names) in self.l3_udp_tput_profile.created_cx.items():
                curr_endp_names.append(endp_names[0])
                curr_endp_names.append(endp_names[1])
            removeEndps(self.lfclient_url, curr_endp_names, debug=self.debug)

    def udp_unidirectional(self, side_a_min_bps, side_b_min_bps, side_a_min_pdu, side_b_min_pdu, direction, values_line):
        self.udp_profile(side_a_min_bps, side_b_min_bps, side_a_min_pdu, side_b_min_pdu)
        self.start()
        print("Running", direction, "Traffic for %s seconds" % self.runtime_secs)
        self.udp_throughput()
        print("napping %f sec" % self.runtime_secs)
        time.sleep(self.runtime_secs)
        values = self.udp_stop()
        print(values)
        # Get value required for measurement
        bytes = values[values_line]
        # Get value in Bits and convert to Mbps
        bits = (int(bytes.split(": ", 1)[1])) * 8
        mpbs = round((bits / 1000000) / self.runtime_secs, 2)
        return mpbs

    def tcp_unidirectional(self, side_a_min_bps, side_b_min_bps, direction, values_line):
        self.tcp_profile(side_a_min_bps, side_b_min_bps)
        self.start()
        print("Running", direction, "Traffic for %s seconds" % self.runtime_secs)
        self.tcp_throughput()
        print("napping %f sec" % self.runtime_secs)
        time.sleep(self.runtime_secs)
        values = self.tcp_stop()
        print(values)
        # Get value required for measurement
        bytes = values[values_line]
        # Get value in Bits and convert to Mbps
        bits = (int(bytes.split(": ", 1)[1])) * 8
        mpbs = round((bits / 1000000) / self.runtime_secs, 2)
        return mpbs
# ~class


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
########################## Test Code ################################

##Main will perform 4 throughput tests on SSID provided by input and return a list with the values

def main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, upstream_port):
    ######## Establish Client Connection #########################
    singleClient = SingleClient("10.10.10.201", 8080, debug_=False)
    singleClient.sta_mode = 0
    singleClient.upstream_resource = 1
    singleClient.upstream_port = upstream_port
    singleClient.radio = radio
    singleClient.resource = 1
    singleClient.dut_ssid = ssid_name
    singleClient.dut_passwd = ssid_psk
    singleClient.dut_security = security
    singleClient.station_names = station
    singleClient.runtime_secs = runtime
    singleClient.cleanup_on_exit = True

    #Create List for Throughput Data
    tput_data = []

    ####### Setup UDP Profile and Run Traffic Downstream (AP to STA)  #######################
    singleClient.setup()
    side_a_min_bps = 56000
    side_b_min_bps = 500000000
    side_a_min_pdu = 1200
    side_b_min_pdu = 1500
    direction = "Downstream"
    values_line = 1        # 1 = Station Rx
    try:
        udp_ds = singleClient.udp_unidirectional(side_a_min_bps, side_b_min_bps, side_a_min_pdu, side_b_min_pdu, direction, values_line)
        print("UDP Downstream:", udp_ds, "Mbps")
        tput_data.append("UDP Downstream: " + str(udp_ds))
    except:
        udp_ds = "error"
        print("UDP Downstream Test Error")
        tput_data.append("UDP Downstream: Error")


    ####### Setup UDP Profile and Run Traffic Upstream (STA to AP)  #######################
    #singleClient.setup()
    side_a_min_bps = 500000000
    side_b_min_bps = 0
    side_a_min_pdu = 1200
    side_b_min_pdu = 1500
    direction = "Upstream"
    values_line = 3        # 3 = AP Rx
    try:
        udp_us = singleClient.udp_unidirectional(side_a_min_bps, side_b_min_bps, side_a_min_pdu, side_b_min_pdu, direction, values_line)
        print("UDP Upstream:",udp_us,"Mbps")
        tput_data.append("UDP Upstream: " + str(udp_us))
    except:
        udp_us = "error"
        print("UDP Upstream Test Error")
        tput_data.append("UDP Upstream: Error")
    #Cleanup UDP Endpoints
    #singleClient.cleanup_udp()


    ####### Setup TCP Profile and Run Traffic Downstream (AP to STA)  #######################
    #singleClient.setup()
    side_a_min_bps = 0
    side_b_min_bps = 500000000
    direction = "Downstream"
    values_line = 1        # 1 = Station Rx
    try:
        tcp_ds = singleClient.tcp_unidirectional(side_a_min_bps, side_b_min_bps, direction, values_line)
        print("TCP Downstream:",tcp_ds,"Mbps")
        tput_data.append("TCP Downstream: " + str(tcp_ds))
    except:
        tcp_ds = "error"
        print("TCP Downstream Test Error")
        tput_data.append("TCP Downstream: Error")

    ####### Setup TCP Profile and Run Traffic Upstream (STA to AP)  #######################
    #singleClient.setup()
    side_a_min_bps = 500000000
    side_b_min_bps = 0
    direction = "Upstream"
    values_line = 3        # 3 = AP Rx
    try:
        tcp_us = singleClient.tcp_unidirectional(side_a_min_bps, side_b_min_bps, direction, values_line)
        print("TCP Upstream:",tcp_us,"Mbps")
        tput_data.append("TCP Upstream: " + str(tcp_us))
    except:
        tcp_us = "error"
        print("TCP Upstream Test Error")
        tput_data.append("TCP Uptream: Error")

    #Cleanup TCP Endpoints
    #singleClient.cleanup_tcp()

    #Cleanup Endpoints
    singleClient.cleanup()

    return(tput_data)

def eap_tput(sta_list, ssid_name, radio, security, eap_type, identity, ttls_password, upstream_port):
    eap_connect = SingleClientEAP("10.10.10.201", 8080, _debug_on=False)
    eap_connect.upstream_resource = 1
    eap_connect.upstream_port = upstream_port
    eap_connect.security = security
    eap_connect.sta_list = sta_list
    eap_connect.station_names = sta_list
    eap_connect.ssid = ssid_name
    eap_connect.radio = radio
    eap_connect.eap = eap_type
    eap_connect.identity = identity
    eap_connect.ttls_passwd = ttls_password
    eap_connect.runtime_secs = 10

    #Create List for Throughput Data
    tput_data = []

    ####### Setup UDP Profile and Run Traffic Downstream (AP to STA)  #######################
    eap_connect.setup()
    side_a_min_bps = 56000
    side_b_min_bps = 500000000
    side_a_min_pdu = 1200
    side_b_min_pdu = 1500
    direction = "Downstream"
    values_line = 1        # 1 = Station Rx
    try:
        udp_ds = eap_connect.udp_unidirectional(side_a_min_bps, side_b_min_bps, side_a_min_pdu, side_b_min_pdu, direction, values_line)
        print("UDP Downstream:", udp_ds, "Mbps")
        tput_data.append("UDP Downstream: " + str(udp_ds))
    except:
        udp_ds = "error"
        print("UDP Downstream Test Error")
        tput_data.append("UDP Downstream: Error")


    ####### Setup UDP Profile and Run Traffic Upstream (STA to AP)  #######################
    #singleClient.setup()
    side_a_min_bps = 500000000
    side_b_min_bps = 0
    side_a_min_pdu = 1200
    side_b_min_pdu = 1500
    direction = "Upstream"
    values_line = 3        # 3 = AP Rx
    try:
        udp_us = eap_connect.udp_unidirectional(side_a_min_bps, side_b_min_bps, side_a_min_pdu, side_b_min_pdu, direction, values_line)
        print("UDP Upstream:",udp_us,"Mbps")
        tput_data.append("UDP Upstream: " + str(udp_us))
    except:
        udp_us = "error"
        print("UDP Upstream Test Error")
        tput_data.append("UDP Upstream: Error")
    #Cleanup UDP Endpoints
    #singleClient.cleanup_udp()


    ####### Setup TCP Profile and Run Traffic Downstream (AP to STA)  #######################
    #singleClient.setup()
    side_a_min_bps = 0
    side_b_min_bps = 500000000
    direction = "Downstream"
    values_line = 1        # 1 = Station Rx
    try:
        tcp_ds = eap_connect.tcp_unidirectional(side_a_min_bps, side_b_min_bps, direction, values_line)
        print("TCP Downstream:",tcp_ds,"Mbps")
        tput_data.append("TCP Downstream: " + str(tcp_ds))
    except:
        tcp_ds = "error"
        print("TCP Downstream Test Error")
        tput_data.append("TCP Downstream: Error")

    ####### Setup TCP Profile and Run Traffic Upstream (STA to AP)  #######################
    #singleClient.setup()
    side_a_min_bps = 500000000
    side_b_min_bps = 0
    direction = "Upstream"
    values_line = 3        # 3 = AP Rx
    try:
        tcp_us = eap_connect.tcp_unidirectional(side_a_min_bps, side_b_min_bps, direction, values_line)
        print("TCP Upstream:",tcp_us,"Mbps")
        tput_data.append("TCP Upstream: " + str(tcp_us))
    except:
        tcp_us = "error"
        print("TCP Upstream Test Error")
        tput_data.append("TCP Uptream: Error")

    #Cleanup TCP Endpoints
    #singleClient.cleanup_tcp()

    #Cleanup Endpoints
    eap_connect.cleanup()

    return(tput_data)
