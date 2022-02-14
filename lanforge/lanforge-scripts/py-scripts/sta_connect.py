#!/usr/bin/env python3
#  This will create a station, create TCP and UDP traffic, run it a short amount of time,
#  and verify whether traffic was sent and received.  It also verifies the station connected
#  to the requested BSSID if bssid is specified as an argument.
#  The script will clean up the station and connections at the end of the test.
import sys
import os
import importlib
import argparse
import time

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
removeCX = LFUtils.removeCX
removeEndps = LFUtils.removeEndps
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
set_port = importlib.import_module("py-json.LANforge.set_port")
add_sta = importlib.import_module("py-json.LANforge.add_sta")
LFRequest = importlib.import_module("py-json.LANforge.LFRequest")
OPEN = "open"
WEP = "wep"
WPA = "wpa"
WPA2 = "wpa2"
MODE_AUTO = 0


class StaConnect(Realm):
    def __init__(self, host, port, _dut_ssid="MyAP", _dut_passwd="NA", _dut_bssid="",
                 _user="lanforge", _passwd="lanforge", _sta_mode="0", _radio="wiphy0",
                 _resource=1, _upstream_resource=None, _upstream_port="eth2",
                 _sta_name=None, _debugOn=False, _dut_security=OPEN, _exit_on_error=False,
                 _cleanup_on_exit=True, _runtime_sec=60, _exit_on_fail=False):
        # do not use `super(LFCLiBase,self).__init__(self, host, port, _debugOn)
        # that is py2 era syntax and will force self into the host variable, making you
        # very confused.
        super().__init__(lfclient_host=host, lfclient_port=port, debug_=_debugOn, _exit_on_fail=_exit_on_fail)
        fields = "_links,port,alias,ip,ap,port+type"
        self.station_results = self.find_ports_like("sta*", fields, debug_=False)
        self.host = host
        self.port = port
        self.debugOn = _debugOn
        self.dut_security = ""
        self.dut_ssid = _dut_ssid
        self.dut_passwd = _dut_passwd
        self.dut_bssid = _dut_bssid
        self.user = _user
        self.passwd = _passwd
        self.sta_mode = _sta_mode  # See add_sta LANforge CLI users guide entry
        self.radio = _radio
        self.resource = _resource
        _upstream_port = LFUtils.name_to_eid(_upstream_port)
        if _upstream_resource:
            self.upstream_resource = _upstream_resource
        else:
            self.upstream_resource = _upstream_port[1]
        self.upstream_port = _upstream_port[2]
        self.runtime_secs = _runtime_sec
        self.cleanup_on_exit = _cleanup_on_exit
        self.sta_url_map = None  # defer construction
        self.upstream_url = None  # defer construction
        self.station_names = _sta_name
        self.cx_names = {}
        self.resulting_stations = {}
        self.resulting_endpoints = {}

        self.cx_profile = self.new_l3_cx_profile()
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        print(self.upstream_port)

        self.desired_set_port_current_flags = ["if_down", "use_dhcp"]
        self.desired_set_port_interest_flags = ["current_flags", "ifdown", "dhcp"]

        self.desired_add_sta_flags = ["wpa2_enable", "80211u_enable", "create_admin_down"]
        self.desired_add_sta_flags_mask = ["wpa2_enable", "80211u_enable", "create_admin_down"]

    def get_station_url(self, sta_name_=None):
        if not sta_name_:
            raise ValueError("get_station_url wants a station name")
        if not self.sta_url_map:
            self.sta_url_map = {}
            for sta_name in self.station_names:
                self.sta_url_map[sta_name] = "port/1/%s/%s" % (self.resource, sta_name)
        return self.sta_url_map[sta_name_]

    def get_upstream_url(self):
        if not self.upstream_url:
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
        # TODO:  Add wait-until-removed call to LFUtils, check return code.

    def num_associated(self, bssid):
        counter = 0
        # print("there are %d results" % len(self.station_results))
        if not self.station_results or (len(self.station_results) < 1):
            self.get_failed_result_list()
        for eid, record in self.station_results.items():
            # print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- ")
            # pprint(eid)
            # pprint(record)
            if record["ap"] == bssid:
                counter += 1
            # print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- ")
        return counter

    def clear_test_results(self):
        self.resulting_stations = {}
        self.resulting_endpoints = {}
        super().clear_test_results()
        # super(StaConnect, self).clear_test_results().test_results.clear()

    def run(self):
        if not self.setup():
            return False
        if not self.start():
            return False
        time.sleep(self.runtime_secs)
        if not self.stop():
            return False
        if not self.finish():
            return False

        # remove all endpoints and cxs
        if self.cleanup_on_exit:
            if not self.cleanup():
                return False
        return True

    @staticmethod
    def add_named_flags(desired_list, command_ref):
        if not desired_list:
            raise ValueError("addNamedFlags wants a list of desired flag names")
        if len(desired_list) < 1:
            raise ValueError("addNamedFlags: empty desired list")
        if not command_ref or (len(command_ref) < 1):
            raise ValueError("addNamedFlags wants a maps of flag values")

        result = 0
        for name in desired_list:
            if not name:
                continue
            if name not in command_ref:
                raise ValueError("flag %s not in map" % name)
            result += command_ref[name]

        return result

    def setup(self):
        self.clear_test_results()
        self.check_connect()
        eth1IP = self.json_get(self.get_upstream_url())
        if not eth1IP:
            self._fail("Unable to query %s, bye" % self.upstream_port, True)
            return False
        if eth1IP['interface']['ip'] == "0.0.0.0":
            self._fail("Warning: %s lacks ip address" % self.get_upstream_url())
            return False

        for sta_name in self.station_names:
            self.rm_port(sta_name, check_exists=True, debug_=self.debug)
        # TODO:  Check return code.
        self.wait_until_ports_disappear(self.station_names, debug_=self.debug)

        # Create stations and turn dhcp on

        radio = LFUtils.name_to_eid(self.radio)

        add_sta_data = {
            "shelf": radio[0],
            "resource": radio[1],
            "radio": radio[2],
            "ssid": self.dut_ssid,
            "key": self.dut_passwd,
            "mode": self.sta_mode,
            "mac": "xx:xx:xx:xx:*:xx",
            "flags": self.add_named_flags(self.desired_add_sta_flags, add_sta.add_sta_flags),  # verbose, wpa2
            "flags_mask": self.add_named_flags(self.desired_add_sta_flags_mask, add_sta.add_sta_flags)
        }
        print("Adding new stations ", end="")
        for sta_name in self.station_names:
            add_sta_data["sta_name"] = sta_name
            print(" %s," % sta_name, end="")
            self.json_post("/cli-json/add_sta", add_sta_data, suppress_related_commands_=True)
            time.sleep(0.01)

        set_port_data = {"shelf": 1, "resource": self.resource,
                         "current_flags": self.add_named_flags(self.desired_set_port_current_flags,
                                                               set_port.set_port_current_flags),
                         "interest": self.add_named_flags(self.desired_set_port_interest_flags,
                                                          set_port.set_port_interest_flags),
                         'report_timer': 1500, 'suppress_preexec_cli': 'yes',
                         'suppress_preexec_method': 1}

        print("\nConfiguring ")
        for sta_name in self.station_names:
            set_port_data["port"] = sta_name
            print(" %s," % sta_name, end="")
            set_port_r = LFRequest.LFRequest(self.lfclient_url + "/cli-json/set_port")
            set_port_r.addPostData(set_port_data)
            set_port_r.jsonPost()
            # TODO:  Remove sleep
            time.sleep(0.01)

        print("\nBringing ports up...")
        for port in self.station_names:
            self.admin_up(port)
        # TODO:  Check return code.
        LFUtils.waitUntilPortsAdminUp(self.resource, self.lfclient_url, self.station_names)

        # station_info = self.jsonGet(self.mgr_url, "%s?fields=port,ip,ap" % (self.getStaUrl()))
        duration = 0
        maxTime = 300
        ip = "0.0.0.0"
        ap = ""

        # TODO:  Move this logic to LFUtils, ensure it does proper return code.
        print("Waiting for %s stations to associate to AP: " % len(self.station_names), end="")
        connected_stations = {}
        while (len(connected_stations.keys()) < len(self.station_names)) and (duration < maxTime):
            duration += 3
            time.sleep(3)
            print(".", end="")
            for sta_name in self.station_names:
                sta_url = self.get_station_url(sta_name)
                station_info = self.json_get(sta_url + "?fields=port,ip,ap", debug_=False)

                # LFUtils.debug_printer.pprint(station_info)
                if station_info and "interface" in station_info:
                    if "ip" in station_info["interface"]:
                        ip = station_info["interface"]["ip"]
                    if "ap" in station_info["interface"]:
                        ap = station_info["interface"]["ap"]

                if (ap == "Not-Associated") or (ap == ""):
                    if self.debugOn:
                        print(" -%s," % sta_name, end="")
                else:
                    if ip == "0.0.0.0":
                        if self.debugOn:
                            print(" %s (0.0.0.0)" % sta_name, end="")
                    else:
                        connected_stations[sta_name] = sta_url
            data = {
                "shelf": 1,
                "resource": self.resource,
                "port": "ALL",
                "probe_flags": 1
            }
            self.json_post("/cli-json/nc_show_ports", data, suppress_related_commands_=True)

        # make a copy of the connected stations for test records
        for sta_name in self.station_names:
            sta_url = self.get_station_url(sta_name)
            station_info = self.json_get(sta_url)  # + "?fields=port,ip,ap")
            self.resulting_stations[sta_url] = station_info
            ap = station_info["interface"]["ap"]
            ip = station_info["interface"]["ip"]
            if (ap != "") and (ap != "Not-Associated"):
                print(" %s +AP %s, " % (sta_name, ap), end="")
                if self.dut_bssid != "":
                    if self.dut_bssid.lower() == ap.lower():
                        self._pass(sta_name + " connected to BSSID: " + ap)
                        # self.test_results.append("PASSED: )
                        # print("PASSED: Connected to BSSID: "+ap)
                    else:
                        self._fail(
                            "%s connected to wrong BSSID, requested: %s  Actual: %s" % (sta_name, self.dut_bssid, ap))
            else:
                self._fail(sta_name + " did not connect to AP")
                return False

            if ip == "0.0.0.0":
                self._fail("%s did not get an ip. Ending test" % sta_name)
            else:
                self._pass("%s connected to AP: %s  With IP: %s" % (sta_name, ap, ip))

        if not self.passes():
            if self.cleanup_on_exit:
                print("Cleaning up...")
                self.remove_stations()
            return False

        # create endpoints and cxs
        # Create UDP endpoints

        for sta_name in self.station_names:
            self.cx_names["testUDP-" + sta_name] = {"a": "testUDP-%s-A" % sta_name,
                                                    "b": "testUDP-%s-B" % sta_name}
            data = {
                "alias": "testUDP-%s-A" % sta_name,
                "shelf": 1,
                "resource": self.resource,
                "port": sta_name,
                "type": "lf_udp",
                "ip_port": "-1",
                "min_rate": 1000000
            }
            self.json_post("/cli-json/add_endp", data, suppress_related_commands_=True)

            data = {
                "name": "testUDP-%s-A" % sta_name,
                "flag": "UseAutoNAT",
                "val": 1
            }
            self.json_post("/cli-json/set_endp_flag", data, suppress_related_commands_=True)

            data = {
                "alias": "testUDP-%s-B" % sta_name,
                "shelf": 1,
                "resource": self.upstream_resource,
                "port": self.upstream_port,
                "type": "lf_udp",
                "ip_port": "-1",
                "min_rate": 1000000
            }
            self.json_post("/cli-json/add_endp", data, suppress_related_commands_=True)

            data = {
                "name": "testUDP-%s-B" % sta_name,
                "flag": "UseAutoNAT",
                "val": 1
            }
            self.json_post("/cli-json/set_endp_flag", data, suppress_related_commands_=True)

            # Create CX
            data = {
                "alias": "testUDP-%s" % sta_name,
                "test_mgr": "default_tm",
                "tx_endp": "testUDP-%s-A" % sta_name,
                "rx_endp": "testUDP-%s-B" % sta_name,
            }
            self.json_post("/cli-json/add_cx", data, suppress_related_commands_=True)

            data = {
                "test_mgr": "default_tm",
                "cx_name": "testUDP-%s" % sta_name,
                "milliseconds": 1000
            }
            self.json_post("/cli-json/set_cx_report_timer", data, suppress_related_commands_=True)

            # Create TCP endpoints
            self.cx_names["testTCP-" + sta_name] = {"a": "testTCP-%s-A" % sta_name,
                                                    "b": "testTCP-%s-B" % sta_name}
            data = {
                "alias": "testTCP-%s-A" % sta_name,
                "shelf": 1,
                "resource": self.resource,
                "port": sta_name,
                "type": "lf_tcp",
                "ip_port": "0",
                "min_rate": 1000000
            }
            self.json_post("/cli-json/add_endp", data, suppress_related_commands_=True)

            data = {
                "alias": "testTCP-%s-B" % sta_name,
                "shelf": 1,
                "resource": self.upstream_resource,
                "port": self.upstream_port,
                "type": "lf_tcp",
                "ip_port": "-1",
                "min_rate": 1000000
            }
            self.json_post("/cli-json/add_endp", data, suppress_related_commands_=True)

            # Create CX
            data = {
                "alias": "testTCP-%s" % sta_name,
                "test_mgr": "default_tm",
                "tx_endp": "testTCP-%s-A" % sta_name,
                "rx_endp": "testTCP-%s-B" % sta_name,
            }
            self.json_post("/cli-json/add_cx", data)

            data = {
                "test_mgr": "default_tm",
                "cx_name": "testTCP-%s" % sta_name,
                "milliseconds": 1000
            }
            self.json_post("/cli-json/set_cx_report_timer", data, suppress_related_commands_=True)

        # TODO:  Check return code and do pass/fail, unless base class does that?  If so, add comment about it.
        self.wait_until_cxs_appear(self.cx_names, debug=self.debug)
        return True

    def start(self):
        # start cx traffic
        print("\nStarting CX Traffic")
        for cx_name in self.cx_names.keys():
            data = {
                "test_mgr": "ALL",
                "cx_name": cx_name,
                "cx_state": "RUNNING"
            }
            self.json_post("/cli-json/set_cx_state", data)

        # Refresh stats

        print("Refresh CX stats")
        for cx_name in self.cx_names.keys():
            data = {
                "test_mgr": "ALL",
                "cross_connect": cx_name
            }
            self.json_post("/cli-json/show_cxe", data)
        return True

    def stop(self):
        self.cx_profile.stop_cx()

    def finish(self):
        # Refresh stats
        print("\nRefresh CX stats")
        for cx_name in self.cx_names.keys():
            data = {
                "test_mgr": "ALL",
                "cross_connect": cx_name
            }
            self.json_post("/cli-json/show_cxe", data)

        # print("Sleeping for 5 seconds")
        time.sleep(5)

        # get data for endpoints JSON
        print("Collecting Data")
        for cx_name in self.cx_names.keys():

            try:
                # ?fields=tx+bytes,rx+bytes
                endp_url = "/endp/%s" % self.cx_names[cx_name]["a"]
                ptest = self.json_get(endp_url)
                self.resulting_endpoints[endp_url] = ptest

                ptest_a_tx = ptest['endpoint']['tx bytes']
                ptest_a_rx = ptest['endpoint']['rx bytes']

                # ptest = self.json_get("/endp/%s?fields=tx+bytes,rx+bytes" % self.cx_names[cx_name]["b"])
                endp_url = "/endp/%s" % self.cx_names[cx_name]["b"]
                ptest = self.json_get(endp_url)
                self.resulting_endpoints[endp_url] = ptest

                ptest_b_tx = ptest['endpoint']['tx bytes']
                ptest_b_rx = ptest['endpoint']['rx bytes']

                self.compare_vals("testTCP-A TX", ptest_a_tx)
                self.compare_vals("testTCP-A RX", ptest_a_rx)

                self.compare_vals("testTCP-B TX", ptest_b_tx)
                self.compare_vals("testTCP-B RX", ptest_b_rx)

            except Exception as e:
                self.error(e)

        # Examples of what happens when you add test results that do not begin with PASS
        # self.test_results.append("Neutral message will fail")
        # self.test_results.append("FAILED message will fail")
        # print("\n")

    def cleanup(self):
        for sta_name in self.station_names:
            self.rm_port(sta_name)
        endp_names = []
        for cx in self.cx_names.keys():
            self.rm_cx(cx)
        for cx_name in self.cx_names:
            endp_names.append(self.cx_names[cx_name]["a"])
            endp_names.append(self.cx_names[cx_name]["b"])
        if self.debug:
            print("Removing endpoints %s" % self.cx_names.values())
        removeEndps(self.lfclient_url, endp_names, debug=False)


def main():
    parser = Realm.create_basic_argparse(
        prog="sta_connect.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""LANforge Unit Test:  Connect Station to AP
Example:
./sta_connect.py --mgr 192.168.100.209 --dut_ssid OpenWrt-2 --dut_bssid 24:F5:A2:08:21:6C
""")
    parser.add_argument("-o", "--port", type=int, help="IP Port the LANforge GUI is listening on (8080 is default)", default=8080)
    parser.add_argument("--resource", type=str, help="LANforge Station resource ID to use, default is 1", default=1)
    parser.add_argument("--upstream_resource", type=str, help="LANforge Ethernet port resource ID to use, default is 1", default=1)
    parser.add_argument("--sta_mode", type=str,
                        help="LANforge station-mode setting (see add_sta LANforge CLI documentation, default is 0 (auto))", default=0)
    parser.add_argument("--dut_bssid", type=str, help="DUT BSSID to which we expect to connect.", default="MyAP")
    parser.add_argument('--test_duration', help='--test_duration sets the duration of the test', default="2m")

    args = parser.parse_args()
    monitor_interval = Realm.parse_time(args.test_duration).total_seconds()

    staConnect = StaConnect(args.mgr, args.port, _upstream_port=args.upstream_port, _runtime_sec=monitor_interval,
                            _sta_mode=args.sta_mode, _upstream_resource=args.upstream_resource,
                            _radio=args.radio, _resource=args.resource, _passwd=args.passwd, _dut_passwd=args.passwd,
                            _dut_bssid=args.dut_bssid, _dut_ssid=args.ssid, _dut_security=args.security,
                            _sta_name=["sta0000"])

    staConnect.run()

    staConnect.get_result_list()

    if not staConnect.passes():
        print("FAIL:  Some tests failed")
    else:
        print("PASS:  All tests pass")

    print(staConnect.get_all_message())

    if not staConnect.passes():
        print("FAIL:  Some tests failed")
    else:
        print("PASS:  All tests pass")

    print(staConnect.get_all_message())

    # TODO:  Do proper exit codes.

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


if __name__ == "__main__":
    main()
