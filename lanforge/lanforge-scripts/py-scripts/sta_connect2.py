#!/usr/bin/env python3
'''
This will create a station, create TCP and UDP traffic, run it a short amount of time, and verify whether traffic
 was sent and received.  It also verifies the station connected to the requested BSSID if bssid is specified
 as an argument. The script will clean up the station and connections at the end of the test.

cli example:
./sta_connect2.py --dest localhost --dut_ssid <ssid> --dut_passwd <passwd> --dut_security wpa2
--upstream_port eth1 --radio wiphy1

Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
'''

import sys
import os
import importlib
import argparse
from pprint import pformat
import time
import logging
import pandas as pd

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
removeCX = LFUtils.removeCX
removeEndps = LFUtils.removeEndps
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
influx = importlib.import_module("py-scripts.influx_utils")
RecordInflux = influx.RecordInflux
lf_report = importlib.import_module("py-scripts.lf_report")
lf_graph = importlib.import_module("py-scripts.lf_graph")
lf_kpi_csv = importlib.import_module("py-scripts.lf_kpi_csv")
logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

OPEN = "open"
WEP = "wep"
WPA = "wpa"
WPA2 = "wpa2"
WPA3 = "wpa3"
MODE_AUTO = 0


class StaConnect2(Realm):
    def __init__(self, host, port, _dut_ssid="jedway-open-1", _dut_passwd="NA", _dut_bssid="",
                 _user="", _passwd="", _sta_mode="0", _radio="wiphy0",
                 _influx_host=None, _influx_db=None, _influx_user=None,
                 _influx_passwd=None,
                 _resource=1, _upstream_resource=1, _upstream_port="eth1",
                 _sta_name=None, _sta_prefix='sta', _bringup_time_sec=300,
                 debug_=False, _dut_security=OPEN, _exit_on_error=False,
                 _cleanup_on_exit=True, _clean_all_sta=False, _runtime_sec=60, _exit_on_fail=False):
        # do not use `super(LFCLiBase,self).__init__(self, host, port, _debugOn)
        # that is py2 era syntax and will force self into the host variable, making you
        # very confused.
        super().__init__(host, port, debug_=debug_, _exit_on_fail=_exit_on_fail)
        self.host = host
        self.port = port
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
        self.clean_all_sta = _clean_all_sta
        self.sta_url_map = None  # defer construction
        self.upstream_url = None  # defer construction
        self.station_names = []
        if _sta_name:
            self.station_names = [_sta_name]
        self.sta_prefix = _sta_prefix
        self.bringup_time_sec = _bringup_time_sec
        self.resulting_stations = {}
        self.resulting_endpoints = {}
        self.station_profile = None
        self.l3_udp_profile = None
        self.l3_tcp_profile = None
        self.influx_host = _influx_host
        self.influx_db = _influx_db
        self.influx_user = _influx_user
        self.influx_passwd = _influx_passwd
        self.name_prefix = "tcp"
        self.use_existing_sta = False

        self.cx_profile = self.new_l3_cx_profile()
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = self.name_prefix


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
        self.station_results = self.find_ports_like("%s*" % self.sta_prefix, fields, debug_=False)
        if (self.station_results is None) or (len(self.station_results) < 1):
            self.get_failed_result_list()
        for eid, record in self.station_results.items():
            # logger.info("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- ")
            logger.debug(pformat(eid))
            # logger.debug(pformat(record))
            if record["ap"] == bssid:
                counter += 1
            # logger.info("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- ")
        return counter

    def clear_test_results(self):
        self.resulting_stations = {}
        self.resulting_endpoints = {}
        super().clear_test_results()
        # super(StaConnect, self).clear_test_results().test_results.clear()

    def setup(self, extra_securities=None):
        if extra_securities is None:
            extra_securities = []
        self.clear_test_results()
        self.check_connect()
        upstream_json = self.json_get("%s?fields=alias,phantom,down,port,ip" % self.get_upstream_url(), debug_=False)

        if upstream_json is None:
            self._fail(message="Unable to query %s, bye" % self.upstream_port, print_=True)
            return False

        if upstream_json['interface']['ip'] == "0.0.0.0":
            if self.debug:
                logger.debug(pformat(upstream_json))
            self._fail("Warning: %s lacks ip address" % self.get_upstream_url(), print_=True)
            return False

        self.pre_cleanup()

        # Create stations and turn dhcp on
        self.station_profile = self.new_station_profile()
        self.station_profile.sta_prefix = self.sta_prefix

        if self.dut_security == WPA2:
            self.station_profile.use_security(security_type="wpa2", ssid=self.dut_ssid, passwd=self.dut_passwd)
        elif self.dut_security == OPEN:
            self.station_profile.use_security(security_type="open", ssid=self.dut_ssid, passwd="[BLANK]")
        elif self.dut_security == WPA:
            self.station_profile.use_security(security_type="wpa", ssid=self.dut_ssid, passwd=self.dut_passwd)
        elif self.dut_security == WEP:
            self.station_profile.use_security(security_type="wep", ssid=self.dut_ssid, passwd=self.dut_passwd)
        elif self.dut_security == WPA3:
            self.station_profile.use_security(security_type="wpa3", ssid=self.dut_ssid, passwd=self.dut_passwd)
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        for security in extra_securities:
            self.station_profile.add_security_extra(security=security)
        # print("Adding new stations ", end="")
        logger.info("Adding new stations ")
        self.station_profile.create(radio=self.radio, sta_names_=self.station_names, up_=False, debug=self.debug,
                                    suppress_related_commands_=True)
        LFUtils.wait_until_ports_appear(self.lfclient_url, self.station_names, debug=self.debug)

        # Create UDP endpoints
        self.l3_udp_profile = self.new_l3_cx_profile()
        self.l3_udp_profile.side_a_min_bps = 128000
        self.l3_udp_profile.side_b_min_bps = 128000
        self.l3_udp_profile.side_a_min_pdu = 1200
        self.l3_udp_profile.side_b_min_pdu = 1500
        self.l3_udp_profile.report_timer = 1000
        self.l3_udp_profile.name_prefix = "udp"
        port_list = list(self.find_ports_like("%s+" % self.sta_prefix))
        if (port_list is None) or (len(port_list) < 1):
            raise ValueError("Unable to find ports named '%s'+" % self.sta_prefix)
        self.l3_udp_profile.create(endp_type="lf_udp",
                                   side_a=port_list,
                                   side_b="%d.%s" % (self.resource, self.upstream_port),
                                   suppress_related_commands=True)

        # Create TCP endpoints
        self.l3_tcp_profile = self.new_l3_cx_profile()
        self.l3_tcp_profile.side_a_min_bps = 128000
        self.l3_tcp_profile.side_b_min_bps = 56000
        self.l3_tcp_profile.name_prefix = self.name_prefix
        self.l3_tcp_profile.report_timer = 1000
        self.l3_tcp_profile.create(endp_type="lf_tcp",
                                   side_a=list(self.find_ports_like("%s+" % self.sta_prefix)),
                                   side_b="%d.%s" % (self.resource, self.upstream_port),
                                   suppress_related_commands=True)

    def start(self):
        if self.station_profile is None:
            self._fail("Incorrect setup")
        logger.debug(pformat(self.station_profile))
        if self.station_profile.up is None:
            self._fail("Incorrect station profile, missing profile.up")
        if not self.station_profile.up:
            logger.info("Bringing ports up...")
            # logger.info("start() - self.lf_client_url: %s", self.lfclient_url)
            data = {"shelf": 1,
                    "resource": self.resource,
                    "port": "ALL",
                    "probe_flags": 1}
            self.json_post("/cli-json/nc_show_ports", data)
            self.station_profile.admin_up()
            LFUtils.waitUntilPortsAdminUp(self.resource, self.lfclient_url, self.station_names)

        if self.influx_db:
            grapher = RecordInflux(_influx_host=self.influx_host,
                                   _influx_db=self.influx_db,
                                   _influx_user=self.influx_user,
                                   _influx_passwd=self.influx_passwd,
                                   _longevity=1,
                                   _devices=self.station_names,
                                   _monitor_interval=1,
                                   _target_kpi=['bps rx'])

        # station_info = self.jsonGet(self.mgr_url, "%s?fields=port,ip,ap" % (self.getStaUrl()))
        duration = 0
        maxTime = self.bringup_time_sec
        ip = "0.0.0.0"
        ap = ""
        # print("Waiting for %s stations to associate to AP: " % len(self.station_names), end="")
        logger.info("Waiting for %s stations to associate to AP: ", len(self.station_names))
        connected_stations = {}
        while (len(connected_stations.keys()) < len(self.station_names)) and (duration < maxTime):
            duration += 3
            time.sleep(3)
            print(".", end="")
            for sta_name in self.station_names:
                sta_url = self.get_station_url(sta_name)
                station_info = self.json_get(sta_url + "?fields=port,ip,ap")

                # LFUtils.debug_printer.pprint(station_info)
                if (station_info) and ("interface" in station_info):
                    if "ip" in station_info["interface"]:
                        ip = station_info["interface"]["ip"]
                    if "ap" in station_info["interface"]:
                        ap = station_info["interface"]["ap"]

                if (ap == "Not-Associated") or (ap == ""):
                    if self.debug:
                        # print(" -%s," % sta_name, end="")
                        logger.info(" -%s,", sta_name)
                else:
                    if ip == "0.0.0.0":
                        if self.debug:
                            # print(" %s (0.0.0.0)" % sta_name, end="")
                            logger.info(" %s (0.0.0.0)", sta_name)
                    else:
                        connected_stations[sta_name] = sta_url
            data = {
                "shelf": 1,
                "resource": self.resource,
                "port": "ALL",
                "probe_flags": 1
            }
            self.json_post("/cli-json/nc_show_ports", data)
            if self.influx_db:
                grapher.getdata()
        # LFUtils.wait_until_ports_appear(port_list=self.station_names, debug=self.debug)
        LFUtils.wait_until_ports_appear(self.lfclient_url, port_list=self.station_names, debug=self.debug)

        for sta_name in self.station_names:
            sta_url = self.get_station_url(sta_name)
            station_info = self.json_get(sta_url)  # + "?fields=port,ip,ap")
            if station_info is None:
                logger.info("unable to query %s", sta_url)
            self.resulting_stations[sta_url] = station_info
            try:
                ap = station_info["interface"]["ap"]
            except Exception as e:
                logger.info(e)
                ap = "NULL"
            ip = station_info["interface"]["ip"]
            if (ap != "") and (ap != "Not-Associated"):
                print(" %s +AP %s, " % (sta_name, ap), end="")
                if self.dut_bssid != "":
                    if self.dut_bssid.lower() == ap.lower():
                        self._pass(sta_name + " connected to BSSID: " + ap)
                        # self.test_results.append("PASSED: )
                        logger.info("PASSED: Connected to BSSID: %s", ap)
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
                logger.info("Cleaning up...")
                self.remove_stations()
            return False

        # start cx traffic
        logger.info("Starting CX Traffic")
        self.l3_udp_profile.start_cx()
        self.l3_tcp_profile.start_cx()
        time.sleep(1)
        # Refresh stats
        self.l3_udp_profile.refresh_cx()
        self.l3_tcp_profile.refresh_cx()

    def collect_endp_stats(self, endp_map):
        logger.info("Collecting Data")
        fields = "/all"
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

                self.compare_vals(endps[0], ptest_a_tx)
                self.compare_vals(endps[0], ptest_a_rx)

                self.compare_vals(endps[1], ptest_b_tx)
                self.compare_vals(endps[1], ptest_b_rx)

            except Exception as e:
                self.error(e)

    def stop(self):
        # stop cx traffic
        logger.info("Stopping CX Traffic")
        self.l3_udp_profile.stop_cx()
        self.l3_tcp_profile.stop_cx()

        # Refresh stats
        logger.info("Refresh CX stats")
        self.l3_udp_profile.refresh_cx()
        self.l3_tcp_profile.refresh_cx()

        logger.info("Sleeping for 5 seconds")
        time.sleep(5)

        # get data for endpoints JSON
        self.collect_endp_stats(self.l3_udp_profile.created_cx)
        self.collect_endp_stats(self.l3_tcp_profile.created_cx)

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
            removeEndps(self.lfclient_url, curr_endp_names, debug=self.debug)

    def pre_cleanup(self):
        self.cx_profile.cleanup_prefix()
        # do not clean up station if existed prior to test
        if not self.use_existing_sta:
            for sta in self.station_names:
                self.rm_port(sta, check_exists=True, debug_=self.debug)

# ~class


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def main():
    lfjson_host = "localhost"
    lfjson_port = 8080
    parser = argparse.ArgumentParser(
        prog="sta_connect2.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
---------------------------
LANforge Unit Test:  Connect Station to AP - sta_connect2.py
---------------------------
Summary:
This will create a station, create TCP and UDP traffic, run it a short amount of time, and verify whether traffic 
 was sent and received.  It also verifies the station connected to the requested BSSID if bssid is specified
 as an argument. The script will clean up the station and connections at the end of the test.
---------------------------
CLI Example: 
./sta_connect2.py --dest localhost --dut_ssid <ssid> --dut_passwd <passwd> --dut_security wpa2 
--upstream_port eth1 --radio wiphy1
--------------------------- 
""")
    parser.add_argument("-d", "--dest", type=str, help="address of the LANforge GUI machine (localhost is default)", default='localhost')
    parser.add_argument("-o", "--port", type=int, help="IP Port the LANforge GUI is listening on (8080 is default)", default=8080)
    parser.add_argument("-u", "--user", type=str, help="TBD: credential login/username")
    parser.add_argument("-p", "--passwd", type=str, help="TBD: credential password")
    parser.add_argument("--resource", type=str, help="LANforge Station resource ID to use, default is 1", default=1)
    parser.add_argument("--upstream_resource", type=str, help="LANforge Ethernet port resource ID to use, default is 1", default=None)
    parser.add_argument("--upstream_port", type=str, help="LANforge Ethernet port name, default is eth2", default='1.1.eth2')
    parser.add_argument("--radio", type=str, help="LANforge radio to use, default is wiphy0", default='wiphy0')
    parser.add_argument("--sta_mode", type=str,
                        help="LANforge station-mode setting (see add_sta LANforge CLI documentation, default is 0 (auto))", default=0)
    parser.add_argument("--dut_ssid", type=str, help="DUT SSID")
    parser.add_argument("--dut_security", type=str, help="DUT security: openLF, wpa, wpa2, wpa3")
    parser.add_argument("--dut_passwd", type=str, help="DUT PSK password.  Do not set for OPEN auth")
    parser.add_argument("--dut_bssid", type=str, help="DUT BSSID to which we expect to connect.")
    parser.add_argument("--debug", help="enable debugging", action="store_true")
    parser.add_argument("--prefix", type=str, help="Station prefix. Default: 'sta'", default='sta')
    parser.add_argument("--bringup_time", type=int,
                        help="Seconds to wait for stations to associate and aquire IP. Default: 300", default=300)
    parser.add_argument('--influx_user', help='Username for your Influx database', default=None)
    parser.add_argument('--influx_passwd', help='Password for your Influx database', default=None)
    parser.add_argument('--influx_db', help='Name of your Influx database', default=None)
    parser.add_argument('--influx_host',
                        help='Host of your influx database if different from the system you are running on',
                        default='localhost')
    parser.add_argument('--monitor_interval', help='How frequently you want to append to your database', default='5s')
    # logging configuration
    parser.add_argument(
        "--lf_logger_config_json",
        help="--lf_logger_config_json <json file> , json configuration of logger")

    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()
    if args.lf_logger_config_json:
        # logger_config.lf_logger_config_json = "lf_logger_config.json"
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()

    upstream_port = LFUtils.name_to_eid(args.upstream_port)
    if args.upstream_resource:
        upstream_resource = args.upstream_resource
    else:
        upstream_resource = upstream_port[1]

    staConnect = StaConnect2(args.dest, args.port,
                             _resource=args.resource,
                             _upstream_resource=upstream_resource,
                             _upstream_port=upstream_port[2],
                             _radio=args.radio,
                             _sta_mode=args.sta_mode,
                             debug_=args.debug,
                             _influx_db=args.influx_db,
                             _influx_passwd=args.influx_passwd,
                             _influx_user=args.influx_user,
                             _influx_host=args.influx_host,
                             _exit_on_fail=True,
                             _exit_on_error=False)

    if args.user:
        staConnect.user = args.user
    if args.passwd:
        staConnect.passwd = args.passwd
    if args.dut_ssid:
        staConnect.dut_ssid = args.dut_ssid
    if args.dut_passwd:
        staConnect.dut_passwd = args.dut_passwd
    if args.dut_bssid:
        staConnect.dut_bssid = args.dut_bssid
    if args.dut_security:
        staConnect.dut_security = args.dut_security
    if args.prefix or (args.prefix != "sta"):
        staConnect.sta_prefix = args.prefix
    staConnect.station_names = ["%s0000" % args.prefix]
    staConnect.bringup_time_sec = args.bringup_time

    staConnect.setup()
    staConnect.start()
    logger.info("napping %f sec", staConnect.runtime_secs)

    time.sleep(staConnect.runtime_secs)
    staConnect.stop()
    staConnect.get_result_list()
    is_passing = staConnect.passes()

    # TODO clean up pass fail  to use realm
    if not is_passing:
        logger.info("FAIL:  Some tests failed")
    else:
        logger.info("PASS:  All tests pass")
    logger.info(staConnect.get_all_message())

    staConnect.pre_cleanup()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


if __name__ == "__main__":
    main()
