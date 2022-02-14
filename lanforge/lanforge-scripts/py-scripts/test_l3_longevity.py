#!/usr/bin/env python3
"""
NAME: test_l3_longevity.py

PURPOSE:

 Supports creating user-specified amount stations on multiple radios
 Supports configuring upload and download requested rates and PDU sizes.
 Supports generating KPI data for storing in influxdb (used by Graphana)
 Supports generating connections with different ToS values.
 Supports generating tcp and/or UDP traffic types.
 Supports iterating over different PDU sizes
 Supports iterating over different requested tx rates
    (configurable as total or per-connection value)
 Supports iterating over attenuation values.
 Supports testing connection between two ethernet connection - L3 dataplane

EXAMPLE:

 10 stations on wiphy0, 1 station on wiphy2.  open-auth to ASUS_70 SSID
 Configured to submit KPI info to influxdb-version2.
 The configuration of the radio==shelf.resource.radio , 1.2.wiphy0 will be on resource 2
./test_l3_longevity.py --mgr localhost --endp_type 'lf_udp lf_tcp' --upstream_port 1.1.eth1 \
  --radio "radio==1.1.wiphy0 stations==10 ssid==ASUS_70 ssid_pw==[BLANK] security==open" \
  --radio "radio==1.1.wiphy2 stations==1 ssid==ASUS_70 ssid_pw==[BLANK] security==open" \
  --test_duration 5s --influx_host c7-graphana --influx_port 8086 --influx_org Candela \
  --influx_token=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ== \
  --influx_bucket ben --rates_are_totals --side_a_min_bps=20000 --side_b_min_bps=300000000 \
  --influx_tag testbed ath11k --influx_tag DUT ROG -o longevity.csv

Example command using attenuator
./test_l3_longevity.py --test_duration 5m --polling_interval 1s --upstream_port 1.1.eth2 \
    --radio 'radio==1.1.wiphy1,stations==1,ssid==TCH-XB7,ssid_pw==comcast123,security==wpa2' \
    --radio 'radio==1.1.wiphy2,stations==1,ssid==TCH-XB7,ssid_pw==comcast123,security==wpa2' \
    --radio 'radio==1.1.wiphy3,stations==1,ssid==TCH-XB7,ssid_pw==comcast123,security==wpa2' \
    --radio 'radio==1.1.wiphy4,stations==1,ssid==TCH-XB7,ssid_pw==comcast123,security==wpa2' \
    --endp_type lf_udp --ap_read --ap_scheduler_stats --ap_ofdma_stats --side_a_min_bps=20000 --side_b_min_bps=400000000 \
    --attenuators 1.1.<serial number>.1 \
    --atten_vals 20,21,40,41

Example using upsteam eth1 downstream eth2
    ./test_l3_longevity.py --test_duration 20s --polling_interval 1s --upstream_port 1.1.eth1 --downstream_port 1.1.eth2
    --endp_type lf --rates_are_totals --side_a_min_bps=10000000,0 --side_a_min_pdu=1000 --side_b_min_bps=0,300000000 --side_b_min_pdu=1000

Example using wifi_settings
    ./test_l3_longevity.py  --lfmgr 192.168.100.116 --local_lf_report_dir
     /home/lanforge/html-reports/ --test_duration 15s --polling_interval 5s
     --upstream_port 1.1.eth2
     --radio "radio==1.1.wiphy1 stations==4 ssid==asus11ax-5 ssid_pw==hello123 security==wpa2
     wifi_mode==0 wifi_settings==wifi_settings
     enable_flags==('ht160_enable'|'wpa2_enable'|'80211u_enable'|'create_admin_down')"
     --endp_type lf_udp --rates_are_totals --side_a_min_bps=20000 --side_b_min_bps=300000000
     --test_rig CT-US-001 --test_tag 'l3_longevity'

COPYRIGHT:
Copyright 2021 Candela Technologies Inc

INCLUDE_IN_README
"""
import argparse
import csv
import datetime
import importlib
import os
import random
import sys
import time
from pprint import pprint

import pexpect
import serial
from pexpect_serial import SerialSpawn

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lf_report = importlib.import_module("py-scripts.lf_report")
lf_kpi_csv = importlib.import_module("py-scripts.lf_kpi_csv")
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
csv_to_influx = importlib.import_module("py-scripts.csv_to_influx")
InfluxRequest = importlib.import_module("py-dashboard.InfluxRequest")
influx_add_parser_args = InfluxRequest.influx_add_parser_args
RecordInflux = InfluxRequest.RecordInflux


# This class handles running the test and generating reports.
class L3VariableTime(Realm):
    def __init__(self,
                 endp_types,
                 args,
                 tos,
                 side_b,
                 side_a,
                 radio_name_list,
                 number_of_stations_per_radio_list,
                 ssid_list,
                 ssid_password_list,
                 ssid_security_list,
                 wifi_mode_list,
                 enable_flags_list,
                 station_lists,
                 name_prefix,
                 outfile,
                 reset_port_enable_list,
                 reset_port_time_min_list,
                 reset_port_time_max_list,
                 side_a_min_rate=None,
                 side_a_max_rate=None,
                 side_b_min_rate=None,
                 side_b_max_rate=None,
                 side_a_min_pdu=None,
                 side_a_max_pdu=None,
                 side_b_min_pdu=None,
                 side_b_max_pdu=None,
                 user_tags=None,
                 rates_are_totals=False,
                 mconn=1,
                 attenuators=None,
                 atten_vals=None,
                 number_template="00",
                 test_duration="256s",
                 polling_interval="60s",
                 lfclient_host="localhost",
                 lfclient_port=8080,
                 debug=False,
                 influxdb=None,
                 # kpi_csv object to set kpi values during the test
                 kpi_csv=None,
                 ap_scheduler_stats=False,
                 ap_ofdma_stats=False,
                 ap_read=False,
                 ap_port='/dev/ttyUSB0',
                 ap_baud='115200',
                 ap_cmd_6g='wl -i wl2 bs_data',
                 ap_cmd_5g='wl -i wl1 bs_data',
                 ap_cmd_2g='wl -i wl0 bs_data',
                 ap_cmd_ul_6g='wl -i wl2 rx_report',
                 ap_cmd_ul_5g='wl -i wl1 rx_report',
                 ap_cmd_ul_2g='wl -i wl0 rx_report',
                 ap_chanim_cmd_6g='wl -i wl2 chanim_stats',
                 ap_chanim_cmd_5g='wl -i wl1 chanim_stats',
                 ap_chanim_cmd_2g='wl -i wl0 chanim_stats',
                 ap_test_mode=False,
                 _exit_on_error=False,
                 _exit_on_fail=False,
                 _proxy_str=None,
                 _capture_signal_list=None):

        self.eth_endps = []
        self.total_stas = 0
        if side_a_min_rate is None:
            side_a_min_rate = [56000]
        if side_a_max_rate is None:
            side_a_max_rate = [0]
        if side_b_min_rate is None:
            side_b_min_rate = [56000]
        if side_b_max_rate is None:
            side_b_max_rate = [0]
        if side_a_min_pdu is None:
            side_a_min_pdu = ["MTU"]
        if side_a_max_pdu is None:
            side_a_max_pdu = [0]
        if side_b_min_pdu is None:
            side_b_min_pdu = ["MTU"]
        if side_b_max_pdu is None:
            side_b_max_pdu = [0]
        if user_tags is None:
            user_tags = []
        if attenuators is None:
            attenuators = []
        if atten_vals is None:
            atten_vals = []
        if _capture_signal_list is None:
            _capture_signal_list = []
        super().__init__(lfclient_host=lfclient_host,
                         lfclient_port=lfclient_port,
                         debug_=debug,
                         _exit_on_error=_exit_on_error,
                         _exit_on_fail=_exit_on_fail,
                         _proxy_str=_proxy_str,
                         _capture_signal_list=_capture_signal_list)
        self.influxdb = influxdb
        # kpi_csv object to set kpi.csv values
        self.kpi_csv = kpi_csv
        self.tos = tos.split(",")
        self.endp_types = endp_types.split(",")
        self.side_b = side_b
        self.side_a = side_a
        # if it is a dataplane test the side_a is not none and an ethernet port
        if self.side_a is not None:
            self.dataplane = True
        else:
            self.dataplane = False
        self.ssid_list = ssid_list
        self.ssid_password_list = ssid_password_list
        self.wifi_mode_list = wifi_mode_list
        self.enable_flags_list = enable_flags_list
        self.station_lists = station_lists
        self.ssid_security_list = ssid_security_list
        self.reset_port_enable_list = reset_port_enable_list
        self.reset_port_time_min_list = reset_port_time_min_list
        self.reset_port_time_max_list = reset_port_time_max_list
        self.number_template = number_template
        self.name_prefix = name_prefix
        self.test_duration = test_duration
        self.radio_name_list = radio_name_list
        self.number_of_stations_per_radio_list = number_of_stations_per_radio_list
        # self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port, debug_=debug_on)
        self.polling_interval_seconds = self.duration_time_to_seconds(
            polling_interval)
        self.cx_profile = self.new_l3_cx_profile()
        self.multicast_profile = self.new_multicast_profile()
        self.multicast_profile.name_prefix = "MLT-"
        self.station_profiles = []
        self.args = args
        self.outfile = outfile
        self.csv_started = False
        self.epoch_time = int(time.time())
        self.debug = debug
        self.mconn = mconn
        self.user_tags = user_tags

        self.side_a_min_rate = side_a_min_rate
        self.side_a_max_rate = side_a_max_rate
        self.side_b_min_rate = side_b_min_rate
        self.side_b_max_rate = side_b_max_rate

        self.side_a_min_pdu = side_a_min_pdu
        self.side_a_max_pdu = side_a_max_pdu
        self.side_b_min_pdu = side_b_min_pdu
        self.side_b_max_pdu = side_b_max_pdu

        self.rates_are_totals = rates_are_totals
        self.cx_count = 0
        self.station_count = 0

        self.attenuators = attenuators
        self.atten_vals = atten_vals
        if ((len(self.atten_vals) > 0) and (
                self.atten_vals[0] != -1) and (len(self.attenuators) == 0)):
            raise ValueError(
                "ERROR:  Attenuation values configured, but no Attenuator EIDs specified.\n")

        self.cx_profile.mconn = mconn
        self.cx_profile.side_a_min_bps = side_a_min_rate[0]
        self.cx_profile.side_a_max_bps = side_a_max_rate[0]
        self.cx_profile.side_b_min_bps = side_b_min_rate[0]
        self.cx_profile.side_b_max_bps = side_b_max_rate[0]

        self.ap_scheduler_stats = ap_scheduler_stats
        self.ap_ofdma_stats = ap_ofdma_stats
        self.ap_read = ap_read
        self.ap_port = ap_port
        self.ap_baud = ap_baud
        self.ap_cmd_6g = ap_cmd_6g
        self.ap_cmd_5g = ap_cmd_5g
        self.ap_cmd_2g = ap_cmd_2g
        self.ap_cmd_ul_6g = ap_cmd_ul_6g
        self.ap_cmd_ul_5g = ap_cmd_ul_5g
        self.ap_cmd_ul_2g = ap_cmd_ul_2g
        self.ap_chanim_cmd_6g = ap_chanim_cmd_6g
        self.ap_chanim_cmd_5g = ap_chanim_cmd_5g
        self.ap_chanim_cmd_2g = ap_chanim_cmd_2g
        self.ap_test_mode = ap_test_mode
        self.ap_6g_umsched = ""
        self.ap_6g_msched = ""
        self.ap_5g_umsched = ""
        self.ap_5g_msched = ""
        self.ap_24g_umsched = ""
        self.ap_24g_msched = ""
        self.ap_ofdma_6g = ""
        self.ap_ofdma_5g = ""
        self.ap_ofdma_24g = ""

        # Lookup key is port-eid name
        self.port_csv_files = {}
        self.port_csv_writers = {}

        self.ul_port_csv_files = {}
        self.ul_port_csv_writers = {}

        # TODO:  cmd-line arg to enable/disable these stats.
        self.ap_stats_col_titles = [
            "Station Address",
            "Dl-PHY-Mbps",
            "Dl-Data-Mbps",
            "Dl-Air-Use",
            "Dl-Data-Use",
            "Dl-Retries",
            "Dl-BW",
            "Dl-MCS",
            "Dl-NSS",
            "Dl-OFDMA",
            "Dl-MU-MIMO",
            "Dl-Channel-Utilization"]

        self.ap_stats_ul_col_titles = [
            "UL Station Address",
            "Ul-rssi",
            "Ul-tid",
            "Ul-ampdu",
            "Ul-mpdu",
            "Ul-Data-Mbps",
            "Ul-PHY-Mbps",
            "UL-BW",
            "Ul-MCS",
            "Ul-NSS",
            "Ul-OOW",
            "Ul-HOLES",
            "Ul-DUP",
            "Ul-Retries",
            "Ul-OFDMA",
            "Ul-Tones",
            "Ul-AIR"]

        dur = self.duration_time_to_seconds(self.test_duration)

        if self.polling_interval_seconds > dur + 1:
            self.polling_interval_seconds = dur - 1

        # Full spread-sheet data
        if self.outfile is not None:
            results = self.outfile[:-4]
            results = results + "-results.csv"
            self.csv_results_file = open(results, "w")
            self.csv_results_writer = csv.writer(self.csv_results_file, delimiter=",")

        # if it is a dataplane test the side_a is not None and an ethernet port
        # if side_a is None then side_a is radios
        if not self.dataplane:
            for (
                    radio_,
                    ssid_,
                    ssid_password_,
                    ssid_security_,
                    mode_,
                    enable_flags_,
                    reset_port_enable_,
                    reset_port_time_min_,
                    reset_port_time_max_) in zip(
                    radio_name_list,
                    ssid_list,
                    ssid_password_list,
                    ssid_security_list,
                    wifi_mode_list,
                    enable_flags_list,
                    reset_port_enable_list,
                    reset_port_time_min_list,
                    reset_port_time_max_list):
                self.station_profile = self.new_station_profile()
                self.station_profile.lfclient_url = self.lfclient_url
                self.station_profile.ssid = ssid_
                self.station_profile.ssid_pass = ssid_password_
                self.station_profile.security = ssid_security_
                self.station_profile.number_template = self.number_template
                self.station_profile.mode = mode_
                self.station_profile.desired_add_sta_flags = enable_flags_.copy()
                self.station_profile.desired_add_sta_flags_mask = enable_flags_.copy()

                # place the enable and disable flags
                # self.station_profile.desired_add_sta_flags = self.enable_flags
                # self.station_profile.desired_add_sta_flags_mask = self.enable_flags
                self.station_profile.set_reset_extra(
                    reset_port_enable=reset_port_enable_,
                    test_duration=self.duration_time_to_seconds(
                        self.test_duration),
                    reset_port_min_time=self.duration_time_to_seconds(reset_port_time_min_),
                    reset_port_max_time=self.duration_time_to_seconds(reset_port_time_max_))
                self.station_profiles.append(self.station_profile)
        else:
            pass

        self.multicast_profile.host = self.lfclient_host
        self.cx_profile.host = self.lfclient_host
        self.cx_profile.port = self.lfclient_port
        self.cx_profile.name_prefix = self.name_prefix

        self.lf_endps = None
        self.udp_endps = None
        self.tcp_endps = None

    def get_ap_6g_umsched(self):
        return self.ap_6g_umsched

    def get_ap_6g_msched(self):
        return self.ap_6g_msched

    def get_ap_5g_umsched(self):
        return self.ap_5g_umsched

    def get_ap_5g_msched(self):
        return self.ap_5g_msched

    def get_ap_24g_umsched(self):
        return self.ap_5g_umsched

    def get_ap_24g_msched(self):
        return self.ap_5g_msched

    def get_ap_ofdma_6g(self):
        return self.ap_ofdma_6g

    def get_ap_ofdma_5g(self):
        return self.ap_ofdma_5g

    def get_ap_ofdma_24g(self):
        return self.ap_ofdma_24g

    def get_results_csv(self):
        # print("self.csv_results_file {}".format(self.csv_results_file.name))
        return self.csv_results_file.name

    # Find avg latency, jitter for connections using specified port.
    def get_endp_stats_for_port(self, eid_name, endps):
        lat = 0
        jit = 0
        total_dl_rate = 0
        total_dl_rate_ll = 0
        total_dl_pkts_ll = 0
        total_ul_rate = 0
        total_ul_rate_ll = 0
        total_ul_pkts_ll = 0
        count = 0
        sta_name = 'no_station'

        # print("endp-stats-for-port, port-eid: {}".format(eid_name))
        eid = self.name_to_eid(eid_name)
        print(
            "eid_name: {eid_name} eid: {eid}".format(
                eid_name=eid_name,
                eid=eid))

        # Convert all eid elements to strings
        eid[0] = str(eid[0])
        eid[1] = str(eid[1])
        eid[2] = str(eid[2])

        for endp in endps:
            pprint(endp)
            eid_endp = endp["eid"].split(".")
            print(
                "Comparing eid:{eid} to endp-id {eid_endp}".format(eid=eid, eid_endp=eid_endp))
            # Look through all the endpoints (endps), to find the port the eid_name is using.
            # The eid_name that has the same Shelf, Resource, and Port as the eid_endp (looking at all the endps)
            # Then read the eid_endp to get the delay, jitter and rx rate
            # Note: the endp eid is shelf.resource.port.endp-id, the eid can be treated somewhat as
            # child class of port-eid , and look up the port the eid is using.
            if eid[0] == eid_endp[0] and eid[1] == eid_endp[1] and eid[2] == eid_endp[2]:
                lat += int(endp["delay"])
                jit += int(endp["jitter"])
                name = endp["name"]
                print("endp name {name}".format(name=name))
                sta_name = name.replace('-A', '')
                # only the -A endpoint will be found so need to look

                count += 1
                print(
                    "Matched: name: {name} eid:{eid} to endp-id {eid_endp}".format(
                        name=name, eid=eid, eid_endp=eid_endp))
            else:
                name = endp["name"]
                print(
                    "No Match: name: {name} eid:{eid} to endp-id {eid_endp}".format(
                        name=name, eid=eid, eid_endp=eid_endp))

        if count > 1:
            lat = int(lat / count)
            jit = int(jit / count)

        # need to loop though again to find the upload and download per station
        # if the name matched
        for endp in endps:
            if sta_name in endp["name"]:
                name = endp["name"]
                if name.endswith("-A"):
                    print("name has -A")
                    total_dl_rate += int(endp["rx rate"])
                    total_dl_rate_ll += int(endp["rx rate ll"])
                    total_dl_pkts_ll += int(endp["rx pkts ll"])
                # -B upload side
                else:
                    total_ul_rate += int(endp["rx rate"])
                    total_ul_rate_ll += int(endp["rx rate ll"])
                    total_ul_pkts_ll += int(endp["rx pkts ll"])

        return lat, jit, total_dl_rate, total_dl_rate_ll, total_dl_pkts_ll, total_ul_rate, total_ul_rate_ll, total_ul_pkts_ll

    # Query all endpoints to generate rx and other stats, returned
    # as an array of objects.
    def __get_rx_values(self):
        endp_list = self.json_get(
            "endp?fields=name,eid,delay,jitter,rx+rate,rx+rate+ll,rx+bytes,rx+drop+%25,rx+pkts+ll",
            debug_=False)
        endp_rx_drop_map = {}
        endp_rx_map = {}
        our_endps = {}
        endps = []

        total_ul = 0
        total_ul_ll = 0
        total_dl = 0
        total_dl_ll = 0

        for e in self.multicast_profile.get_mc_names():
            our_endps[e] = e
        for e in self.cx_profile.created_endp.keys():
            our_endps[e] = e
        for endp_name in endp_list['endpoint']:
            if endp_name != 'uri' and endp_name != 'handler':
                for item, endp_value in endp_name.items():
                    if item in our_endps:
                        endps.append(endp_value)
                        print("endpoint: ", item, " value:\n")
                        pprint(endp_value)

                        for value_name, value in endp_value.items():
                            if value_name == 'rx bytes':
                                endp_rx_map[item] = value
                            if value_name == 'rx rate':
                                endp_rx_map[item] = value
                            if value_name == 'rx rate ll':
                                endp_rx_map[item] = value
                            if value_name == 'rx pkts ll':
                                endp_rx_map[item] = value
                            if value_name == 'rx drop %':
                                endp_rx_drop_map[item] = value
                            if value_name == 'rx rate':
                                # This hack breaks for mcast or if someone names endpoints weirdly.
                                # print("item: ", item, " rx-bps: ", value_rx_bps)
                                if item.endswith("-A"):
                                    total_dl += int(value)
                                else:
                                    total_ul += int(value)
                            if value_name == 'rx rate ll':
                                # This hack breaks for mcast or if someone
                                # names endpoints weirdly.
                                if item.endswith("-A"):
                                    total_dl_ll += int(value)
                                else:
                                    total_ul_ll += int(value)

        # print("total-dl: ", total_dl, " total-ul: ", total_ul, "\n")
        return endp_rx_map, endp_rx_drop_map, endps, total_dl, total_ul, total_dl_ll, total_ul_ll
    # This script supports resetting ports, allowing one to test AP/controller under data load
    # while bouncing wifi stations.  Check here to see if we should reset
    # ports.

    def reset_port_check(self):
        for station_profile in self.station_profiles:
            if station_profile.reset_port_extra_data['reset_port_enable']:
                if not station_profile.reset_port_extra_data['reset_port_timer_started']:
                    print(
                        "reset_port_timer_started {}".format(
                            station_profile.reset_port_extra_data['reset_port_timer_started']))
                    print(
                        "reset_port_time_min: {}".format(
                            station_profile.reset_port_extra_data['reset_port_time_min']))
                    print(
                        "reset_port_time_max: {}".format(
                            station_profile.reset_port_extra_data['reset_port_time_max']))
                    station_profile.reset_port_extra_data['seconds_till_reset'] = random.randint(
                        station_profile.reset_port_extra_data['reset_port_time_min'],
                        station_profile.reset_port_extra_data['reset_port_time_max'])
                    station_profile.reset_port_extra_data['reset_port_timer_started'] = True
                    print(
                        "on radio {} seconds_till_reset {}".format(
                            station_profile.add_sta_data['radio'],
                            station_profile.reset_port_extra_data['seconds_till_reset']))
                else:
                    station_profile.reset_port_extra_data[
                        'seconds_till_reset'] = station_profile.reset_port_extra_data['seconds_till_reset'] - 1
                    print(
                        "radio: {} countdown seconds_till_reset {}".format(
                            station_profile.add_sta_data['radio'],
                            station_profile.reset_port_extra_data['seconds_till_reset']))
                    if ((
                            station_profile.reset_port_extra_data['seconds_till_reset'] <= 0)):
                        station_profile.reset_port_extra_data['reset_port_timer_started'] = False
                        port_to_reset = random.randint(
                            0, len(station_profile.station_names) - 1)
                        print(
                            "reset on radio {} station: {}".format(
                                station_profile.add_sta_data['radio'],
                                station_profile.station_names[port_to_reset]))
                        self.reset_port(
                            station_profile.station_names[port_to_reset])

    # Common code to generate timestamp for CSV files.
    def time_stamp(self):
        return time.strftime('%m_%d_%Y_%H_%M_%S',
                             time.localtime(self.epoch_time))

    # Cleanup any older config that a previous run of this test may have
    # created.
    def pre_cleanup(self):
        self.cx_profile.cleanup_prefix()
        self.multicast_profile.cleanup_prefix()
        self.total_stas = 0
        for station_list in self.station_lists:
            for sta in station_list:
                self.rm_port(sta, check_exists=True)
                self.total_stas += 1

        # Make sure they are gone
        count = 0
        while count < 10:
            more = False
            for station_list in self.station_lists:
                for sta in station_list:
                    rv = self.rm_port(sta, check_exists=True)
                    if rv:
                        more = True
            if not more:
                break
            count += 1
            time.sleep(5)

    def gather_port_eids(self):
        rv = [self.side_b]

        for station_profile in self.station_profiles:
            rv = rv + station_profile.station_names

        return rv

    # Create stations and connections/endpoints.  If rebuild is true, then
    # only update connections/endpoints.
    def build(self, rebuild=False):
        index = 0
        self.station_count = 0
        self.udp_endps = []
        self.tcp_endps = []
        self.eth_endps = []

        if rebuild:
            # if we are just re-applying new cx values, then no need to rebuild
            # stations, so allow skipping it.
            # Do clean cx lists so that when we re-apply them we get same endp name
            # as we had previously
            # print("rebuild: Clearing cx profile lists.\n")
            self.cx_profile.clean_cx_lists()
            self.multicast_profile.clean_mc_lists()

        if self.dataplane:
            for etype in self.endp_types:
                for _tos in self.tos:
                    print(
                        "Creating connections for endpoint type: %s TOS: %s  cx-count: %s" %
                        (etype, _tos, self.cx_profile.get_cx_count()))
                    # use brackes on [self.side_a] to make it a list
                    these_cx, these_endp = self.cx_profile.create(
                        endp_type=etype, side_a=[
                            self.side_a], side_b=self.side_b, sleep_time=0, tos=_tos)
                    if etype == "lf_udp" or etype == "lf_udp6":
                        self.udp_endps = self.udp_endps + these_endp
                    elif etype == "lf":
                        self.lf_endps = self.eth_endps + these_endp
                    else:
                        self.tcp_endps = self.tcp_endps + these_endp

        else:
            for station_profile in self.station_profiles:
                if not rebuild:
                    station_profile.use_security(
                        station_profile.security,
                        station_profile.ssid,
                        station_profile.ssid_pass)
                    station_profile.set_number_template(
                        station_profile.number_template)
                    print(
                        "Creating stations on radio %s" %
                        (self.radio_name_list[index]))

                    station_profile.create(
                        radio=self.radio_name_list[index],
                        sta_names_=self.station_lists[index],
                        debug=self.debug,
                        sleep_time=0)
                    index += 1

                self.station_count += len(station_profile.station_names)

                # Build/update connection types
                for etype in self.endp_types:
                    if etype == "mc_udp" or etype == "mc_udp6":
                        print(
                            "Creating Multicast connections for endpoint type: %s" %
                            etype)
                        self.multicast_profile.create_mc_tx(
                            etype, self.side_b, etype)
                        self.multicast_profile.create_mc_rx(
                            etype, side_rx=station_profile.station_names)
                    else:
                        for _tos in self.tos:
                            print(
                                "Creating connections for endpoint type: %s TOS: %s  cx-count: %s" %
                                (etype, _tos, self.cx_profile.get_cx_count()))
                            these_cx, these_endp = self.cx_profile.create(
                                endp_type=etype, side_a=station_profile.station_names, side_b=self.side_b, sleep_time=0, tos=_tos)
                            if etype == "lf_udp" or etype == "lf_udp6":
                                self.udp_endps = self.udp_endps + these_endp
                            else:
                                self.tcp_endps = self.tcp_endps + these_endp

        self.cx_count = self.cx_profile.get_cx_count()

        if self.dataplane:
            self._pass(
                "PASS: CX build finished: created/updated:  %s connections." %
                self.cx_count)
        else:
            self._pass(
                "PASS: Stations & CX build finished: created/updated: %s stations and %s connections." %
                (self.station_count, self.cx_count))

    def ap_custom_cmd(self, ap_custom_cmd):
        ap_results = ""
        try:
            # configure the serial interface
            ser = serial.Serial(self.ap_port, int(self.ap_baud), timeout=5)
            ss = SerialSpawn(ser)
            ss.sendline(str(ap_custom_cmd))
            # do not detete line, waits for output
            ss.expect([pexpect.TIMEOUT], timeout=1)
            ap_results = ss.before.decode('utf-8', 'ignore')
            print(
                "ap_custom_cmd: {} ap_results {}".format(
                    ap_custom_cmd, ap_results))
        except BaseException:
            print(
                "ap_custom_cmd: {} WARNING unable to read AP ".format(ap_custom_cmd))

        return ap_results

    def read_ap_stats_6g(self):
        #  6ghz:  wl -i wl2 bs_data
        ap_stats_6g = ""
        try:
            # configure the serial interface
            ser = serial.Serial(self.ap_port, int(self.ap_baud), timeout=5)
            ss = SerialSpawn(ser)
            ss.sendline(str(self.ap_cmd_6g))
            # do not detete line, waits for output
            ss.expect([pexpect.TIMEOUT], timeout=1)
            ap_stats_6g = ss.before.decode('utf-8', 'ignore')
            print("ap_stats_6g from AP: {}".format(ap_stats_6g))

        except BaseException:
            print("WARNING: ap_stats_6g unable to read AP")

        return ap_stats_6g

    def read_ap_stats_5g(self):
        #  5ghz:  wl -i wl1 bs_data
        ap_stats_5g = ""
        try:
            # configure the serial interface
            ser = serial.Serial(self.ap_port, int(self.ap_baud), timeout=5)
            ss = SerialSpawn(ser)
            ss.sendline(str(self.ap_cmd_5g))
            # do not detete line, waits for output
            ss.expect([pexpect.TIMEOUT], timeout=1)
            ap_stats_5g = ss.before.decode('utf-8', 'ignore')
            print("ap_stats_5g from AP: {}".format(ap_stats_5g))

        except BaseException:
            print("WARNING: ap_stats_5g unable to read AP")

        return ap_stats_5g

    def read_ap_stats_2g(self):
        #  2.4ghz# wl -i wl0 bs_data
        ap_stats_2g = ""
        try:
            # configure the serial interface
            ser = serial.Serial(self.ap_port, int(self.ap_baud), timeout=5)
            ss = SerialSpawn(ser)
            ss.sendline(str(self.ap_cmd_2g))
            # do not detete line, waits for output
            ss.expect([pexpect.TIMEOUT], timeout=1)
            ap_stats_2g = ss.before.decode('utf-8', 'ignore')
            print("ap_stats_2g from AP: {}".format(ap_stats_2g))

        except BaseException:
            print("WARNING: ap_stats_2g unable to read AP")

        return ap_stats_2g

    def read_ap_chanim_stats_6g(self):
        #  5ghz:  wl -i wl1 chanim_stats
        ap_chanim_stats_6g = ""
        try:
            # configure the serial interface
            ser = serial.Serial(self.ap_port, int(self.ap_baud), timeout=5)
            ss = SerialSpawn(ser)
            ss.sendline(str(self.ap_chanim_cmd_6g))
            # do not detete line, waits for output
            ss.expect([pexpect.TIMEOUT], timeout=1)
            ap_chanim_stats_6g = ss.before.decode('utf-8', 'ignore')
            print("read_ap_chanim_stats_6g {}".format(ap_chanim_stats_6g))

        except BaseException:
            print("WARNING: read_ap_chanim_stats_6g unable to read AP")

        return ap_chanim_stats_6g

    def read_ap_chanim_stats_5g(self):
        #  5ghz:  wl -i wl1 chanim_stats
        ap_chanim_stats_5g = ""
        try:
            # configure the serial interface
            ser = serial.Serial(self.ap_port, int(self.ap_baud), timeout=5)
            ss = SerialSpawn(ser)
            ss.sendline(str(self.ap_chanim_cmd_5g))
            # do not detete line, waits for output
            ss.expect([pexpect.TIMEOUT], timeout=1)
            ap_chanim_stats_5g = ss.before.decode('utf-8', 'ignore')
            print("read_ap_chanim_stats_5g {}".format(ap_chanim_stats_5g))

        except BaseException:
            print("WARNING: read_ap_chanim_stats_5g unable to read AP")

        return ap_chanim_stats_5g

    def read_ap_chanim_stats_2g(self):
        #  2.4ghz# wl -i wl0 chanim_stats
        ap_chanim_stats_2g = ""
        try:
            # configure the serial interface
            ser = serial.Serial(self.ap_port, int(self.ap_baud), timeout=5)
            ss = SerialSpawn(ser)
            ss.sendline(str(self.ap_chanim_cmd_2g))
            # do not detete line, waits for output
            ss.expect([pexpect.TIMEOUT], timeout=1)
            ap_chanim_stats_2g = ss.before.decode('utf-8', 'ignore')
            print("read_ap_chanim_stats_2g {}".format(ap_chanim_stats_2g))

        except BaseException:
            print("WARNING: read_ap_chanim_stats_2g unable to read AP")

        return ap_chanim_stats_2g

    def read_ap_stats_ul_6g(self):
        #  6ghz:  wl -i wl2 rx_report
        ap_stats_ul_6g = ""
        try:
            # configure the serial interface
            ser = serial.Serial(self.ap_port, int(self.ap_baud), timeout=5)
            ss = SerialSpawn(ser)
            ss.sendline(str(self.ap_cmd_ul_6g))
            # do not detete line, waits for output
            ss.expect([pexpect.TIMEOUT], timeout=1)
            ap_stats_ul_6g = ss.before.decode('utf-8', 'ignore')
            print("ap_stats_ul_6g from AP: {}".format(ap_stats_ul_6g))

        except BaseException:
            print("WARNING: ap_stats_ul_6g unable to read AP")

        return ap_stats_ul_6g

    def read_ap_stats_ul_5g(self):
        #  6ghz:  wl -i wl1 rx_report
        ap_stats_ul_5g = ""
        try:
            # configure the serial interface
            ser = serial.Serial(self.ap_port, int(self.ap_baud), timeout=5)
            ss = SerialSpawn(ser)
            ss.sendline(str(self.ap_cmd_ul_5g))
            # do not detete line, waits for output
            ss.expect([pexpect.TIMEOUT], timeout=1)
            ap_stats_ul_5g = ss.before.decode('utf-8', 'ignore')
            print("ap_stats_ul_5g from AP: {}".format(ap_stats_ul_5g))

        except BaseException:
            print("WARNING: ap_stats_ul_5g unable to read AP")

        return ap_stats_ul_5g

    def read_ap_stats_ul_2g(self):
        #  6ghz:  wl -i wl0 rx_report
        ap_stats_ul_2g = ""
        try:
            # configure the serial interface
            ser = serial.Serial(self.ap_port, int(self.ap_baud), timeout=5)
            ss = SerialSpawn(ser)
            ss.sendline(str(self.ap_cmd_ul_2g))
            # do not detete line, waits for output
            ss.expect([pexpect.TIMEOUT], timeout=1)
            ap_stats_ul_2g = ss.before.decode('utf-8', 'ignore')
            print("ap_stats_ul_2g from AP: {}".format(ap_stats_ul_2g))

        except BaseException:
            print("WARNING: ap_stats_ul_6g unable to read AP")

        return ap_stats_ul_2g

    # provide fake bs_data for testing without AP wl2 is the 6E interface, wl1
    # 5G, wl0 2G

    @staticmethod
    def read_ap_rx_report_test_mode():
        ap_rx_report_fake = "{}{}{}{}{}".format(
            "root@Docsis-Gateway:~#  wl -i wl1 rx_report\n",
            "Station Address (rssi)  tid   ampdu     mpdu  Data Mbps   PHY Mbps    bw   mcs   Nss   oow holes   dup rtries  ofdma  tones    air\n",
            "50:E0:85:87:5B:F4 (-43dBm)   0    2062   127078       32.5      571.9    80  11.0     2     0     0    64     0%   100%  483.3     6%\n",
            "50:E0:85:84:7A:E7 (-44dBm)   0    2334   144373       36.9      343.1    80  10.9     2     0     0    63     0%   100%  291.4    11%\n",
            "50:E0:85:88:F4:5F (-45dBm)   0    2296   142463       36.4      346.3    80  10.9     2     0     0    64     0%   100%  294.1    11%\n")
        # Keep commented for testing "(overall)   -    6692   413914      105.8
        # -     -     -     -     -     -     -      -     -      -       -
        # -\n"
        return ap_rx_report_fake

    @staticmethod
    def read_ap_bs_data_test_mode():
        ap_stats_fake = "{}{}{}{}{}{}".format(
            "root@Docsis-Gateway:~# wl -i wl2 bs_data\n",
            "Station Address   PHY Mbps  Data Mbps    Air Use   Data Use    Retries   bw   mcs   Nss   ofdma mu-mimo\n",
            "04:f0:21:82:2f:d6     1016.6       48.9       6.5%      24.4%      16.6%   80   9.7     2    0.0%    0.0%\n",
            "50:E0:85:84:7A:E7      880.9       52.2       7.7%      26.1%      20.0%   80   8.5     2    0.0%    0.0%\n",
            "50:E0:85:89:5D:00      840.0       47.6       6.4%      23.8%       2.3%   80   8.0     2    0.0%    0.0%\n",
            "50:E0:85:87:5B:F4      960.7       51.5       5.9%      25.7%       0.0%   80     9     2    0.0%    0.0%\n")
        # Keep commented for testing "- note the MAC will match ap_stats.append((overall)          -      200.2      26.5%         -         - \n")
        # print("ap_stats_fake {}".format(ap_stats_fake))
        return ap_stats_fake

    @staticmethod
    def read_ap_chanim_stats_test_mode():
        # Create the test data as a continuous string
        ap_chanim_stats_fake = "{}{}{}{}".format("root@Docsis-Gateway:~# wl -i wl2 chanim_stats\n",
                                                 "version: 3\n",
                                                 "chanspec tx   inbss   obss   nocat   nopkt   doze     txop     goodtx  badtx   glitch   badplcp  knoise  idle  timestamp\n",
                                                 # `"0xe06a  61      15      0       17      0       0       6       53      2       0       0       -91     65      343370578\n")
                                                 '0xe06a\t41.82\t20.22\t0.00\t13.56\t0.02\t0.00\t17.58\t29.54\t1.94\t3\t0\t-90\t58\t146903490\n')
        # "0xe06a  1.67  15.00   0.00   17.00   0.00    0.00     97.33    53.00   2.00    0         0       -91     65      343370578\n")
        return ap_chanim_stats_fake

    # Run the main body of the test logic.
    def start(self, print_pass=False):
        print("Bringing up stations")
        self.admin_up(self.side_b)
        for station_profile in self.station_profiles:
            for sta in station_profile.station_names:
                print("Bringing up station %s" % sta)
                self.admin_up(sta)

        temp_stations_list = []
        # temp_stations_list.append(self.side_b)
        for station_profile in self.station_profiles:
            temp_stations_list.extend(station_profile.station_names.copy())

        temp_stations_list_with_side_b = temp_stations_list.copy()
        # wait for b side to get IP
        temp_stations_list_with_side_b.append(self.side_b)
        print("temp_stations_list {temp_stations_list}".format(
            temp_stations_list=temp_stations_list))
        print("temp_stations_list_with_side_b {temp_stations_list_with_side_b}".format(
            temp_stations_list_with_side_b=temp_stations_list_with_side_b))

        if self.wait_for_ip(temp_stations_list_with_side_b, timeout_sec=120):
            print("ip's acquired")
        else:
            # No reason to continue
            raise ValueError("ERROR: print failed to get IP's Check station configuration SSID, Security, Is DHCP enabled exiting")

        csv_header = self.csv_generate_column_headers()
        # print(csv_header)
        self.csv_add_column_headers()

        # dl - ports
        port_eids = self.gather_port_eids()
        for eid_name in port_eids:
            self.csv_add_port_column_headers(
                eid_name, self.csv_generate_port_column_headers())

        port_eids = self.gather_port_eids()
        for eid_name in port_eids:
            self.csv_add_ul_port_column_headers(
                eid_name, self.csv_generate_ul_port_column_headers())

        # For each rate
        rate_idx = 0
        for ul in self.side_a_min_rate:
            dl = self.side_b_min_rate[rate_idx]
            rate_idx += 1

            # For each pdu size
            pdu_idx = 0
            for ul_pdu in self.side_a_min_pdu:
                dl_pdu = self.side_b_min_pdu[pdu_idx]
                pdu_idx += 1

                # Adjust rate to take into account the number of connections we
                # have.
                if self.cx_count > 1 and self.rates_are_totals:
                    # Convert from string to int to do math, then back to string
                    # as that is what the cx_profile wants.
                    ul = str(int(int(ul) / self.cx_count))
                    dl = str(int(int(dl) / self.cx_count))

                dl_pdu_str = dl_pdu
                ul_pdu_str = ul_pdu

                if ul_pdu == "AUTO" or ul_pdu == "MTU":
                    ul_pdu = "-1"

                if dl_pdu == "AUTO" or dl_pdu == "MTU":
                    dl_pdu = "-1"

                print(
                    "ul: %s  dl: %s  cx-count: %s  rates-are-totals: %s\n" %
                    (ul, dl, self.cx_count, self.rates_are_totals))

                # Set rate and pdu size config
                self.cx_profile.side_a_min_bps = ul
                self.cx_profile.side_a_max_bps = ul
                self.cx_profile.side_b_min_bps = dl
                self.cx_profile.side_b_max_bps = dl

                self.cx_profile.side_a_min_pdu = ul_pdu
                self.cx_profile.side_a_max_pdu = ul_pdu
                self.cx_profile.side_b_min_pdu = dl_pdu
                self.cx_profile.side_b_max_pdu = dl_pdu

                # Update connections with the new rate and pdu size config.
                self.build(rebuild=True)

                if self.ap_scheduler_stats or self.ap_ofdma_stats:
                    self.ap_custom_cmd('wl -i wl2 dump_clear')
                    self.ap_custom_cmd('wl -i wl1 dump_clear')
                    self.ap_custom_cmd('wl -i wl0 dump_clear')

                for atten_val in self.atten_vals:
                    if atten_val != -1:
                        for atten_idx in self.attenuators:
                            self.set_atten(atten_idx, atten_val)

                    print("Starting multicast traffic (if any configured)")
                    self.multicast_profile.start_mc(debug_=self.debug)
                    self.multicast_profile.refresh_mc(debug_=self.debug)
                    print("Starting layer-3 traffic (if any configured)")
                    self.cx_profile.start_cx()
                    self.cx_profile.refresh_cx()

                    cur_time = datetime.datetime.now()
                    print("Getting initial values.")
                    self.__get_rx_values()

                    end_time = self.parse_time(self.test_duration) + cur_time

                    print(
                        "Monitoring throughput for duration: %s" %
                        self.test_duration)

                    # Monitor test for the interval duration.
                    passes = 0
                    expected_passes = 0
                    total_dl_bps = 0
                    total_ul_bps = 0
                    total_dl_ll_bps = 0
                    total_ul_ll_bps = 0
                    ap_row = []
                    mac_found_ul_6g = False
                    mac_found_ul_5g = False
                    mac_found_ul_2g = False
                    mac_found_6g = False
                    mac_found_5g = False
                    mac_found_2g = False
                    reset_timer = 0

                    while cur_time < end_time:
                        # interval_time = cur_time + datetime.timedelta(seconds=5)
                        interval_time = cur_time + \
                            datetime.timedelta(
                                seconds=self.polling_interval_seconds)
                        # print("polling_interval_seconds {}".format(self.polling_interval_seconds))

                        while cur_time < interval_time:
                            cur_time = datetime.datetime.now()
                            time.sleep(.2)
                            reset_timer += 1
                            if reset_timer % 5 == 0:
                                self.reset_port_check()

                        self.epoch_time = int(time.time())
                        new_rx_values, rx_drop_percent, endps, total_dl_bps, total_ul_bps, total_dl_ll_bps, total_ul_ll_bps = self.__get_rx_values()

                        print(
                            "main loop, total-dl: ",
                            total_dl_bps,
                            " total-ul: ",
                            total_ul_bps,
                            " total-dl-ll: ",
                            total_dl_ll_bps,
                            " total-ul-ll: ",
                            total_ul_ll_bps)

                        # AP OUTPUT
                        # rx_report command gives OFDMA and airtime fro the Uplink
                        # bs_data command shows the OFDMA and MU-MIMO on the
                        # downlink
                        if self.ap_read:
                            # 6G test mode
                            if self.ap_test_mode:
                                ap_stats_6g = self.read_ap_bs_data_test_mode()
                                ap_chanim_stats_6g = self.read_ap_chanim_stats_test_mode()
                                ap_stats_ul_6g = self.read_ap_rx_report_test_mode()
                            else:
                                # read from the AP 6g
                                ap_stats_6g = self.read_ap_stats_6g()
                                ap_chanim_stats_6g = self.read_ap_chanim_stats_6g()
                                ap_stats_ul_6g = self.read_ap_stats_ul_6g()

                            ap_stats_6g_rows = ap_stats_6g.splitlines()
                            print(
                                "From AP stats: ap_stats_6g_rows {}".format(ap_stats_6g_rows))

                            ap_chanim_stats_rows_6g = ap_chanim_stats_6g.splitlines()
                            print(
                                "From AP chanim: ap_chanim_stats_rows_6g {}".format(ap_chanim_stats_rows_6g))

                            ap_stats_ul_6g_rows = ap_stats_ul_6g.splitlines()
                            print(
                                "From AP stats ul: ap_stats_ul_6g_rows {}".format(ap_stats_ul_6g_rows))

                            channel_utilization = 0

                            # Query all of our ports
                            # Note: the endp eid is the
                            # shelf.resource.port.endp-id
                            port_eids = self.gather_port_eids()
                            # read find the bs_data
                            for eid_name in port_eids:
                                eid = self.name_to_eid(eid_name)
                                url = "/port/%s/%s/%s" % (eid[0],
                                                          eid[1], eid[2])
                                # read LANforge to get the mac
                                response = self.json_get(url)
                                if (response is None) or (
                                        "interface" not in response):
                                    print(
                                        "6g query-port: %s: incomplete response:" %
                                        url)
                                    pprint(response)
                                else:
                                    # print("response".format(response))
                                    pprint(response)
                                    port_data = response['interface']
                                    print(
                                        "#### 6g From LANforge: port_data, response['insterface']:{}".format(port_data))
                                    mac = port_data['mac']
                                    # print("#### From LANforge: port_data['mac']:
                                    # {mac}".format(mac=mac))

                                    # Parse the ap stats to find the matching
                                    # mac then use that row for reporting
                                    for row in ap_stats_6g_rows:
                                        split_row = row.split()
                                        # print("split_row {}".format(split_row))
                                        # print("split_row[0] {}  mac {}".format(split_row[0].lower(),mac.lower()))
                                        if self.ap_test_mode:
                                            if split_row[0].lower(
                                            ) != mac.lower():
                                                ap_row = split_row
                                                mac_found_6g = True
                                        else:
                                            try:
                                                # split_row[0].lower() , mac from AP
                                                # mac.lower() , mac from
                                                # LANforge
                                                if split_row[0].lower(
                                                ) == mac.lower():
                                                    ap_row = split_row
                                                    mac_found_6g = True
                                            except BaseException:
                                                print(
                                                    "6g 'No stations are currently associated.'? from AP")
                                                print(
                                                    " since possibly no stations: excption on compare split_row[0].lower() ")
                                    if mac_found_6g:
                                        mac_found_6g = False
                                        print(
                                            "6g selected ap_row (from split_row): {}".format(ap_row))

                                        # Find latency, jitter for connections
                                        # using this port.
                                        self.get_endp_stats_for_port(port_data["port"], endps)

                                        # now report the ap_chanim_stats along
                                        # side of the ap_stats_6g
                                        xtop_reported = False
                                        for row in ap_chanim_stats_rows_6g:
                                            split_row = row.split()
                                            if xtop_reported:
                                                print(
                                                    "6g xtop_reported row: {row}".format(
                                                        row=row))
                                                print(
                                                    "6g xtop_reported split_row: {split_row}".format(
                                                        split_row=split_row))
                                                try:
                                                    xtop = split_row[7]
                                                    print(
                                                        "6g xtop {xtop}".format(xtop=xtop))
                                                    channel_utilization = float(
                                                        100) - float(xtop)
                                                    print("6g channel_utilization {utilization}".format(utilization=channel_utilization))
                                                except BaseException:
                                                    print(
                                                        "6g detected chanspec with reading chanim_stats, exception reading xtop")

                                                # should be only one channel
                                                # utilization
                                                break
                                            else:
                                                try:
                                                    if split_row[0].lower(
                                                    ) == 'chanspec':
                                                        print(
                                                            "6g chanspec found xtop_reported = True")
                                                        xtop_reported = True
                                                except BaseException:
                                                    print(
                                                        "6g Error reading xtop")
                                        # ap information is passed with ap_row
                                        # so all information needs to be
                                        # contained in ap_row
                                        ap_row.append(str(channel_utilization))

                            # work though the ul rx_data 6G
                            for eid_name in port_eids:
                                eid = self.name_to_eid(eid_name)
                                url = "/port/%s/%s/%s" % (eid[0],
                                                          eid[1], eid[2])
                                # read LANforge to get the mac
                                response = self.json_get(url)
                                if (response is None) or (
                                        "interface" not in response):
                                    print(
                                        "6g query-port: %s: incomplete response:" %
                                        url)
                                    pprint(response)
                                else:
                                    # print("response".format(response))
                                    pprint(response)
                                    port_data = response['interface']
                                    print(
                                        "#### 6g From LANforge: port_data, response['insterface']:{}".format(port_data))
                                    mac = port_data['mac']
                                    # print("#### From LANforge: port_data['mac']:
                                    # {mac}".format(mac=mac))

                                    # Parse the ap stats to find the matching
                                    # mac then use that row for reporting
                                    for row in ap_stats_ul_6g_rows:
                                        split_ul_row = row.split()
                                        # print("split_row {}".format(split_row))
                                        # print("split_row[0] {}  mac {}".format(split_row[0].lower(),mac.lower()))
                                        if self.ap_test_mode:
                                            if split_ul_row[0].lower(
                                            ) != mac.lower():
                                                ap_ul_row = split_ul_row
                                                mac_found_ul_6g = True
                                        else:
                                            try:
                                                # split_ul_row[0].lower() , mac from AP
                                                # mac.lower() , mac from
                                                # LANforge
                                                if split_ul_row[0].lower(
                                                ) == mac.lower():
                                                    ap_ul_row = split_ul_row
                                                    mac_found_ul_6g = True
                                            except BaseException:
                                                print(
                                                    "6g ul 'No stations are currently associated.'? from AP")
                                                print(
                                                    " ul since possibly no stations: excption on compare split_row[0].lower() ")
                                    if mac_found_ul_6g:
                                        mac_found_ul_6g = False
                                        print(
                                            "6g ul selected ap_ul_row (from split_ul_row): {}".format(ap_ul_row))

                                        # Find latency, jitter for connections
                                        # using this port.
                                        latency, jitter, total_ul_rate, total_ul_rate_ll, total_ul_pkts_ll, total_dl_rate, total_dl_rate_ll, total_dl_pkts_ll = self.get_endp_stats_for_port(
                                            port_data["port"], endps)

                                        print(
                                            "6g ap_ul_row {ap_ul_row}".format(
                                                ap_ul_row=ap_ul_row))

                                        self.write_port_csv(
                                            len(temp_stations_list),
                                            ul,
                                            dl,
                                            ul_pdu_str,
                                            dl_pdu_str,
                                            atten_val,
                                            eid_name,
                                            port_data,
                                            latency,
                                            jitter,
                                            total_ul_rate,
                                            total_ul_rate_ll,
                                            total_ul_pkts_ll,
                                            total_dl_rate,
                                            total_dl_rate_ll,
                                            total_dl_pkts_ll,
                                            ap_row)
                                #####
                            # 5G test mode
                            if self.ap_test_mode:
                                ap_stats_5g = self.read_ap_bs_data_test_mode()
                                print("ap_stats 5g {}".format(ap_stats_5g))
                                ap_chanim_stats_5g = self.read_ap_chanim_stats_test_mode()
                                ap_stats_ul_5g = self.read_ap_rx_report_test_mode()
                            else:
                                # read from the AP
                                ap_stats_5g = self.read_ap_stats_5g()
                                ap_chanim_stats_5g = self.read_ap_chanim_stats_5g()
                                ap_stats_ul_5g = self.read_ap_stats_ul_5g()

                            ap_stats_5g_rows = ap_stats_5g.splitlines()
                            print(
                                "From AP stats: ap_stats_5g_rows {}".format(ap_stats_5g_rows))

                            ap_chanim_stats_rows_5g = ap_chanim_stats_5g.splitlines()
                            print(
                                "From AP chanim: ap_chanim_stats_rows_5g {}".format(ap_chanim_stats_rows_5g))

                            ap_stats_ul_5g_rows = ap_stats_ul_5g.splitlines()
                            print(
                                "From AP stats ul: ap_stats_ul_5g_rows {}".format(ap_stats_ul_5g_rows))

                            channel_utilization = 0

                            # Query all of our ports
                            # Note: the endp eid is the shelf.resource.port.endp-id
                            # reading the data for bs_data
                            port_eids = self.gather_port_eids()
                            for eid_name in port_eids:
                                eid = self.name_to_eid(eid_name)
                                url = "/port/%s/%s/%s" % (eid[0],
                                                          eid[1], eid[2])
                                # read LANforge to get the mac
                                response = self.json_get(url)
                                if (response is None) or (
                                        "interface" not in response):
                                    print(
                                        "query-port 5g: %s: incomplete response:" %
                                        url)
                                    pprint(response)
                                else:
                                    # print("response".format(response))
                                    pprint(response)
                                    port_data = response['interface']
                                    print(
                                        "#### From LANforge: port_data, response['insterface']:{}".format(port_data))
                                    mac = port_data['mac']
                                    # print("#### From LANforge: port_data['mac']:
                                    # {mac}".format(mac=mac))

                                    # Parse the ap stats to find the matching
                                    # mac then use that row for reporting
                                    for row in ap_stats_5g_rows:
                                        split_row = row.split()
                                        # print("split_row {}".format(split_row))
                                        # print("split_row[0] {}  mac {}".format(split_row[0].lower(),mac.lower()))
                                        if self.ap_test_mode:
                                            if split_row[0].lower(
                                            ) != mac.lower():
                                                ap_row = split_row
                                                mac_found_5g = True
                                        else:
                                            try:
                                                # split_row[0].lower() , mac from AP
                                                # mac.lower() , mac from
                                                # LANforge
                                                if split_row[0].lower(
                                                ) == mac.lower():
                                                    ap_row = split_row
                                                    mac_found_5g = True
                                            except BaseException:
                                                print(
                                                    "5g 'No stations are currently associated.'? from AP")
                                                print(
                                                    "5g since possibly no stations: excption on compare split_row[0].lower() ")
                                    if mac_found_5g:
                                        mac_found_5g = False
                                        print(
                                            "5g selected ap_row (from split_row): {}".format(ap_row))

                                        # Find latency, jitter for connections
                                        # using this port.
                                        latency, jitter, total_ul_rate, total_ul_rate_ll, total_ul_pkts_ll, total_dl_rate, total_dl_rate_ll, total_dl_pkts_ll = self.get_endp_stats_for_port(
                                            port_data["port"], endps)

                                        # now report the ap_chanim_stats along
                                        # side of the ap_stats_5g
                                        xtop_reported = False
                                        for row in ap_chanim_stats_rows_5g:
                                            split_row = row.split()
                                            if xtop_reported:
                                                print(
                                                    "xtop_reported 5g row: {row}".format(
                                                        row=row))
                                                print(
                                                    "xtop_reported 5g split_row: {split_row}".format(
                                                        split_row=split_row))
                                                try:
                                                    xtop = split_row[7]
                                                    print(
                                                        "5g xtop {xtop}".format(xtop=xtop))
                                                except BaseException:
                                                    print(
                                                        "5g detected chanspec with reading chanim_stats, exception reading xtop")

                                                try:
                                                    channel_utilization = float(
                                                        100) - float(xtop)
                                                    print(
                                                        "5g channel_utilization {utilization}".format(
                                                            utilization=channel_utilization))
                                                except BaseException:
                                                    print(
                                                        "5g detected chanspec with reading chanim_stats, failed calcluating channel_utilization from xtop")
                                                # should be only one channel
                                                # utilization
                                                break
                                            else:
                                                try:
                                                    if split_row[0].lower(
                                                    ) == 'chanspec':
                                                        print(
                                                            "5g chanspec found xtop_reported = True")
                                                        xtop_reported = True
                                                except BaseException:
                                                    print(
                                                        "5g Error reading xtop")
                                        # ap information is passed with ap_row
                                        # so all information needs to be
                                        # contained in ap_row
                                        ap_row.append(str(channel_utilization))
                                        print(
                                            "5g channel_utilization {channel_utilization}".format(
                                                channel_utilization=channel_utilization))
                                        print(
                                            "5g ap_row {ap_row}".format(
                                                ap_row=ap_row))

                                        self.write_port_csv(
                                            len(temp_stations_list),
                                            ul,
                                            dl,
                                            ul_pdu_str,
                                            dl_pdu_str,
                                            atten_val,
                                            eid_name,
                                            port_data,
                                            latency,
                                            jitter,
                                            total_ul_rate,
                                            total_ul_rate_ll,
                                            total_ul_pkts_ll,
                                            total_dl_rate,
                                            total_dl_rate_ll,
                                            total_dl_pkts_ll,
                                            ap_row)

                            # work though the ul rx_data 5G
                            for eid_name in port_eids:
                                eid = self.name_to_eid(eid_name)
                                url = "/port/%s/%s/%s" % (eid[0],
                                                          eid[1], eid[2])
                                # read LANforge to get the mac
                                response = self.json_get(url)
                                if (response is None) or (
                                        "interface" not in response):
                                    print(
                                        "5g query-port: %s: incomplete response:" %
                                        url)
                                    pprint(response)
                                else:
                                    # print("response".format(response))
                                    pprint(response)
                                    port_data = response['interface']
                                    print(
                                        "#### 5g From LANforge: port_data, response['insterface']:{}".format(port_data))
                                    mac = port_data['mac']
                                    # print("#### From LANforge: port_data['mac']:
                                    # {mac}".format(mac=mac))

                                    # Parse the ap stats to find the matching
                                    # mac then use that row for reporting
                                    for row in ap_stats_ul_5g_rows:
                                        split_ul_row = row.split()
                                        # print("split_row {}".format(split_row))
                                        # print("split_row[0] {}  mac {}".format(split_row[0].lower(),mac.lower()))
                                        if self.ap_test_mode:
                                            if split_ul_row[0].lower(
                                            ) != mac.lower():
                                                ap_ul_row = split_ul_row
                                                mac_found_ul_5g = True
                                        else:
                                            try:
                                                # split_ul_row[0].lower() , mac from AP
                                                # mac.lower() , mac from
                                                # LANforge
                                                if split_ul_row[0].lower(
                                                ) == mac.lower():
                                                    ap_ul_row = split_ul_row
                                                    mac_found_ul_5g = True
                                            except BaseException:
                                                print(
                                                    "5g ul 'No stations are currently associated.'? from AP")
                                                print(
                                                    "5g ul since possibly no stations: excption on compare split_row[0].lower() ")
                                    if mac_found_ul_5g:
                                        mac_found_ul_5g = False
                                        print(
                                            "5g ul selected ap_ul_row (from split_ul_row): {}".format(ap_ul_row))

                                        # Find latency, jitter for connections
                                        # using this port.
                                        latency, jitter, total_ul_rate, total_ul_rate_ll, total_ul_pkts_ll, total_dl_rate, total_dl_rate_ll, total_dl_pkts_ll = self.get_endp_stats_for_port(
                                            port_data["port"], endps)

                                        print(
                                            "5g ap_ul_row {ap_ul_row}".format(
                                                ap_ul_row=ap_ul_row))
                                        self.write_ul_port_csv(
                                            len(temp_stations_list),
                                            ul,
                                            dl,
                                            ul_pdu_str,
                                            dl_pdu_str,
                                            atten_val,
                                            eid_name,
                                            port_data,
                                            latency,
                                            jitter,
                                            total_ul_rate,
                                            total_ul_rate_ll,
                                            total_ul_pkts_ll,
                                            total_dl_rate,
                                            total_dl_rate_ll,
                                            total_dl_pkts_ll,
                                            ap_ul_row)

                            # 2g test mode
                            if self.ap_test_mode:
                                ap_stats_2g = self.read_ap_bs_data_test_mode()
                                print("ap_stats 2g {}".format(ap_stats_2g))
                                ap_chanim_stats_2g = self.read_ap_chanim_stats_test_mode()
                                ap_stats_ul_2g = self.read_ap_rx_report_test_mode()
                            else:
                                # read from the AP
                                ap_stats_2g = self.read_ap_stats_2g()
                                ap_chanim_stats_2g = self.read_ap_chanim_stats_2g()
                                ap_stats_ul_2g = self.read_ap_stats_ul_2g()

                            ap_stats_2g_rows = ap_stats_2g.splitlines()
                            print(
                                "From AP stats: ap_stats_2g_rows {}".format(ap_stats_2g_rows))

                            ap_chanim_stats_rows_2g = ap_chanim_stats_2g.splitlines()
                            print(
                                "From AP chanim: ap_chanim_stats_rows_2g {}".format(ap_chanim_stats_rows_2g))

                            ap_stats_ul_2g_rows = ap_stats_ul_2g.splitlines()
                            print(
                                "From AP stats ul: ap_stats_ul_2g_rows {}".format(ap_stats_ul_2g_rows))

                            channel_utilization = 0

                            # Query all of our ports
                            # Note: the endp eid is the
                            # shelf.resource.port.endp-id
                            port_eids = self.gather_port_eids()
                            for eid_name in port_eids:
                                eid = self.name_to_eid(eid_name)
                                url = "/port/%s/%s/%s" % (eid[0],
                                                          eid[1], eid[2])
                                # read LANforge to get the mac
                                response = self.json_get(url)
                                if (response is None) or (
                                        "interface" not in response):
                                    print(
                                        "2g query-port: %s: incomplete response:" %
                                        url)
                                    pprint(response)
                                else:
                                    # print("response".format(response))
                                    pprint(response)
                                    port_data = response['interface']
                                    # print("#### From LANforge: port_data,
                                    # response['insterface']:{}".format(p))
                                    mac = port_data['mac']
                                    # print("#### From LANforge: port_data['mac']:
                                    # {mac}".format(mac=mac))

                                    # Parse the ap stats to find the matching
                                    # mac then use that row for reporting
                                    for row in ap_stats_2g_rows:
                                        split_row = row.split()
                                        # print("split_row {}".format(split_row))
                                        # print("split_row[0] {}  mac {}".format(split_row[0].lower(),mac.lower()))
                                        if self.ap_test_mode:
                                            if split_row[0].lower(
                                            ) != mac.lower():
                                                ap_row = split_row
                                                mac_found_2g = True
                                        else:
                                            try:
                                                # split_row[0].lower() , mac from AP
                                                # mac.lower() , mac from
                                                # LANforge
                                                if split_row[0].lower(
                                                ) == mac.lower():
                                                    ap_row = split_row
                                                    mac_found_2g = True
                                            except BaseException:
                                                print(
                                                    "2g 'No stations are currently associated.'? from AP")
                                                print(
                                                    "2g since possibly no stations: excption on compare split_row[0].lower() ")
                                    if mac_found_2g:
                                        mac_found_2g = False
                                        print(
                                            "2g selected ap_row (from split_row): {}".format(ap_row))

                                        # Find latency, jitter for connections
                                        # using this port.
                                        latency, jitter, total_ul_rate, total_ul_rate_ll, total_ul_pkts_ll, total_dl_rate, total_dl_rate_ll, total_dl_pkts_ll = self.get_endp_stats_for_port(
                                            port_data["port"], endps)

                                        # now report the ap_chanim_stats along
                                        # side of the ap_stats_2g
                                        xtop_reported = False
                                        for row in ap_chanim_stats_rows_2g:
                                            split_row = row.split()
                                            if xtop_reported:
                                                print(
                                                    "2g xtop_reported row: {row}".format(
                                                        row=row))
                                                print(
                                                    "2g xtop_reported split_row: {split_row}".format(
                                                        split_row=split_row))
                                                try:
                                                    xtop = split_row[7]
                                                    print(
                                                        "2g xtop {xtop}".format(xtop=xtop))
                                                except BaseException:
                                                    print(
                                                        "2g detected chanspec with reading chanim_stats, exception reading xtop")

                                                try:
                                                    channel_utilization = float(
                                                        100) - float(xtop)
                                                    print(
                                                        "2g channel_utilization {utilization}".format(
                                                            utilization=channel_utilization))
                                                except BaseException:
                                                    print(
                                                        "2g detected chanspec with reading chanim_stats, failed calcluating channel_utilization from xtop")
                                                # should be only one channel
                                                # utilization
                                                break
                                            else:
                                                try:
                                                    if split_row[0].lower(
                                                    ) == 'chanspec':
                                                        print(
                                                            "2g chanspec found xtop_reported = True")
                                                        xtop_reported = True
                                                except BaseException:
                                                    print(
                                                        "2g Error reading xtop")
                                        # ap information is passed with ap_row
                                        # so all information needs to be
                                        # contained in ap_row
                                        ap_row.append(str(channel_utilization))
                                        print(
                                            "2g channel_utilization {channel_utilization}".format(
                                                channel_utilization=channel_utilization))
                                        print(
                                            "2g ap_row {ap_row}".format(
                                                ap_row=ap_row))

                                        self.write_port_csv(
                                            len(temp_stations_list),
                                            ul,
                                            dl,
                                            ul_pdu_str,
                                            dl_pdu_str,
                                            atten_val,
                                            eid_name,
                                            port_data,
                                            latency,
                                            jitter,
                                            total_ul_rate,
                                            total_ul_rate_ll,
                                            total_ul_pkts_ll,
                                            total_dl_rate,
                                            total_dl_rate_ll,
                                            total_dl_pkts_ll,
                                            ap_row)
                            # work though the ul rx_data 5G
                            for eid_name in port_eids:
                                eid = self.name_to_eid(eid_name)
                                url = "/port/%s/%s/%s" % (eid[0],
                                                          eid[1], eid[2])
                                # read LANforge to get the mac
                                response = self.json_get(url)
                                if (response is None) or (
                                        "interface" not in response):
                                    print(
                                        "5g query-port: %s: incomplete response:" %
                                        url)
                                    pprint(response)
                                else:
                                    # print("response".format(response))
                                    pprint(response)
                                    port_data = response['interface']
                                    print(
                                        "#### 2g From LANforge: port_data, response['insterface']:{}".format(port_data))
                                    mac = port_data['mac']
                                    # print("#### From LANforge: port_data['mac']:
                                    # {mac}".format(mac=mac))

                                    # Parse the ap stats to find the matching
                                    # mac then use that row for reporting
                                    for row in ap_stats_ul_2g_rows:
                                        split_ul_row = row.split()
                                        # print("split_row {}".format(split_row))
                                        # print("split_row[0] {}  mac {}".format(split_row[0].lower(),mac.lower()))
                                        if self.ap_test_mode:
                                            if split_ul_row[0].lower(
                                            ) != mac.lower():
                                                ap_ul_row = split_ul_row
                                                mac_found_ul_2g = True
                                        else:
                                            try:
                                                # split_ul_row[0].lower() , mac from AP
                                                # mac.lower() , mac from
                                                # LANforge
                                                if split_ul_row[0].lower(
                                                ) == mac.lower():
                                                    ap_ul_row = split_ul_row
                                                    mac_found_ul_2g = True
                                            except BaseException:
                                                print(
                                                    "2g ul 'No stations are currently associated.'? from AP")
                                                print(
                                                    "2g ul since possibly no stations: excption on compare split_row[0].lower() ")
                                    if mac_found_ul_2g:
                                        mac_found_ul_2g = False
                                        print(
                                            "2g ul selected ap_ul_row (from split_ul_row): {}".format(ap_ul_row))

                                        # Find latency, jitter for connections
                                        # using this port.
                                        latency, jitter, total_ul_rate, total_ul_rate_ll, total_ul_pkts_ll, total_dl_rate, total_dl_rate_ll, total_dl_pkts_ll = self.get_endp_stats_for_port(
                                            port_data["port"], endps)

                                        print(
                                            "2g ap_ul_row {ap_ul_row}".format(
                                                ap_ul_row=ap_ul_row))
                                        self.write_ul_port_csv(
                                            len(temp_stations_list),
                                            ul,
                                            dl,
                                            ul_pdu_str,
                                            dl_pdu_str,
                                            atten_val,
                                            eid_name,
                                            port_data,
                                            latency,
                                            jitter,
                                            total_ul_rate,
                                            total_ul_rate_ll,
                                            total_ul_pkts_ll,
                                            total_dl_rate,
                                            total_dl_rate_ll,
                                            total_dl_pkts_ll,
                                            ap_ul_row)
                        else:

                            # Query all of our ports
                            # Note: the endp eid is the
                            # shelf.resource.port.endp-id
                            port_eids = self.gather_port_eids()
                            for eid_name in port_eids:
                                eid = self.name_to_eid(eid_name)
                                url = "/port/%s/%s/%s" % (eid[0],
                                                          eid[1], eid[2])
                                response = self.json_get(url)
                                if (response is None) or (
                                        "interface" not in response):
                                    print(
                                        "query-port: %s: incomplete response:" % url)
                                    pprint(response)
                                else:
                                    port_data = response['interface']
                                    latency, jitter, total_ul_rate, total_ul_rate_ll, total_ul_pkts_ll, total_dl_rate, total_dl_rate_ll, total_dl_pkts_ll = self.get_endp_stats_for_port(
                                        port_data["port"], endps)

                                    self.write_port_csv(
                                        len(temp_stations_list),
                                        ul,
                                        dl,
                                        ul_pdu_str,
                                        dl_pdu_str,
                                        atten_val,
                                        eid_name,
                                        port_data,
                                        latency,
                                        jitter,
                                        total_ul_rate,
                                        total_ul_rate_ll,
                                        total_ul_pkts_ll,
                                        total_dl_rate,
                                        total_dl_rate_ll,
                                        total_dl_pkts_ll,
                                        ap_row)

                    # At end of test step, record KPI into kpi.csv
                    self.record_kpi_csv(
                        len(temp_stations_list),
                        ul,
                        dl,
                        ul_pdu_str,
                        dl_pdu_str,
                        atten_val,
                        total_dl_bps,
                        total_ul_bps,
                        total_dl_ll_bps,
                        total_ul_ll_bps)

                    # At end of test step, record results information. This is
                    self.record_results(
                        len(temp_stations_list),
                        ul,
                        dl,
                        ul_pdu_str,
                        dl_pdu_str,
                        atten_val,
                        total_dl_bps,
                        total_ul_bps,
                        total_dl_ll_bps,
                        total_ul_ll_bps)

                    # At end of test if requested store upload and download
                    # stats
                    if self.ap_scheduler_stats:
                        # get the (UL) Upload 6g scheduler statistics
                        self.ap_6g_umsched += self.ap_custom_cmd(
                            'wl -i wl2 dump umsched')
                        # get the (DL) Download 6g schduler staticstics
                        self.ap_6g_msched += self.ap_custom_cmd(
                            'wl -i wl2 dump msched')

                        # get the (UL) Upload 5g scheduler statistics
                        self.ap_5g_umsched += self.ap_custom_cmd(
                            'wl -i wl1 dump umsched')
                        # get the (DL) Download 5g schduler staticstics
                        self.ap_5g_msched += self.ap_custom_cmd(
                            'wl -i wl1 dump msched')

                        # get the (UL) Upload 24g scheduler statistics
                        self.ap_24g_umsched += self.ap_custom_cmd(
                            'wl -i wl0 dump umsched')
                        # get the (DL) Download 24g schduler staticstics
                        self.ap_24g_msched += self.ap_custom_cmd(
                            'wl -i wl0 dump msched')

                    if self.ap_ofdma_stats:
                        # provide OFDMA stats 6GHz
                        self.ap_ofdma_6g += self.ap_custom_cmd(
                            'wl -i wl2 muinfo -v')

                        # provide OFDMA stats 5GHz
                        self.ap_ofdma_5g += self.ap_custom_cmd(
                            'wl -i wl1 muinfo -v')

                        # provide OFDMA stats 2.4GHz
                        self.ap_ofdma_24g += self.ap_custom_cmd(
                            'wl -i wl0 muinfo -v')

                    # Stop connections.
                    self.cx_profile.stop_cx()
                    self.multicast_profile.stop_mc()

                    if passes == expected_passes:
                        self._pass(
                            "PASS: Requested-Rate: %s <-> %s  PDU: %s <-> %s   All tests passed" %
                            (ul, dl, ul_pdu, dl_pdu), print_pass)

    def write_port_csv(
            self,
            sta_count,
            ul,
            dl,
            ul_pdu,
            dl_pdu,
            atten,
            eid_name,
            port_data,
            latency,
            jitter,
            total_ul_rate,
            total_ul_rate_ll,
            total_ul_pkts_ll,
            total_dl_rate,
            total_dl_rate_ll,
            total_dl_pkts_ll,
            ap_row):
        row = [self.epoch_time, self.time_stamp(), sta_count,
               ul, ul, dl, dl, dl_pdu, dl_pdu, ul_pdu, ul_pdu,
               atten, eid_name
               ]

        row = row + [port_data['bps rx'],
                     port_data['bps tx'],
                     port_data['rx-rate'],
                     port_data['tx-rate'],
                     port_data['signal'],
                     port_data['ap'],
                     port_data['mode'],
                     latency,
                     jitter,
                     total_ul_rate,
                     total_ul_rate_ll,
                     total_ul_pkts_ll,
                     total_dl_rate,
                     total_dl_rate_ll,
                     total_dl_pkts_ll]

        # Add in info queried from AP.
        # print("ap_row length {} col_titles length {}".format(len(ap_row),len(self.ap_stats_col_titles)))
        # print("self.ap_stats_col_titles {} ap_stats_col_titles {}".format(self.ap_stats_col_titles,ap_stats_col_titles))
        if len(ap_row) == len(self.ap_stats_col_titles):
            # print("ap_row {}".format(ap_row))
            for col in ap_row:
                # print("col {}".format(col))
                row.append(col)

        writer = self.port_csv_writers[eid_name]
        writer.writerow(row)
        self.port_csv_files[eid_name].flush()

    def write_ul_port_csv(
            self,
            sta_count,
            ul,
            dl,
            ul_pdu,
            dl_pdu,
            atten,
            eid_name,
            port_data,
            latency,
            jitter,
            total_ul_rate,
            total_ul_rate_ll,
            total_ul_pkts_ll,
            total_dl_rate,
            total_dl_rate_ll,
            total_dl_pkts_ll,
            ap_ul_row):
        row = [self.epoch_time, self.time_stamp(), sta_count,
               ul, ul, dl, dl, dl_pdu, dl_pdu, ul_pdu, ul_pdu,
               atten, eid_name
               ]

        row = row + [port_data['bps rx'],
                     port_data['bps tx'],
                     port_data['rx-rate'],
                     port_data['tx-rate'],
                     port_data['signal'],
                     port_data['ap'],
                     port_data['mode'],
                     latency,
                     jitter,
                     total_ul_rate,
                     total_ul_rate_ll,
                     total_ul_pkts_ll,
                     total_dl_rate,
                     total_dl_rate_ll,
                     total_dl_pkts_ll]

        # Add in info queried from AP.
        # print("ap_row length {} col_titles length {}".format(len(ap_row),len(self.ap_stats_col_titles)))
        # print("self.ap_stats_col_titles {} ap_stats_col_titles {}".format(self.ap_stats_col_titles,ap_stats_col_titles))

        print("ap_ul_row len {} ap_stats_ul_col_titles len {} ap_ul_row {}".format(
            len(ap_ul_row), len(self.ap_stats_ul_col_titles), ap_ul_row))
        if len(ap_ul_row) == len(self.ap_stats_ul_col_titles):
            print("ap_ul_row {}".format(ap_ul_row))
            for col in ap_ul_row:
                print("col {}".format(col))
                row.append(col)

        writer = self.ul_port_csv_writers[eid_name]
        writer.writerow(row)
        self.ul_port_csv_files[eid_name].flush()

    def record_kpi_csv(
            self,
            sta_count,
            ul,
            dl,
            ul_pdu,
            dl_pdu,
            atten,
            total_dl_bps,
            total_ul_bps,
            total_dl_ll_bps,
            total_ul_ll_bps):

        print("NOTE:  Adding kpi to kpi.csv, sta_count {sta_count}  total-download-bps:{total_dl_bps}  upload: {total_ul_bps}  bi-directional: {total}\n".format(
              sta_count=sta_count, total_dl_bps=total_dl_bps, total_ul_bps=total_ul_bps, total=(total_ul_bps + total_dl_bps)))

        print("NOTE:  Adding kpi to kpi.csv, sta_count {sta_count}  total-download-bps:{total_dl_ll_bps}  upload: {total_ul_ll_bps}  bi-directional: {total_ll}\n".format(
              sta_count=sta_count, total_dl_ll_bps=total_dl_ll_bps, total_ul_ll_bps=total_ul_ll_bps, total_ll=(total_ul_ll_bps + total_dl_ll_bps)))

        # the short description will all for more data to show up in one
        # test-tag graph
        # Look at lf_kpi_csv.py library for the kpi columns
        results_dict = self.kpi_csv.kpi_csv_get_dict_update_time()
        results_dict['Graph-Group'] = "Per Stations Rate DL"
        results_dict['short-description'] = "DL {dl} bps  pdu {dl_pdu}  {sta_count} STA".format(
            dl=dl, dl_pdu=dl_pdu, sta_count=sta_count)
        results_dict['numeric-score'] = "{}".format(total_dl_bps)
        results_dict['Units'] = "bps"
        self.kpi_csv.kpi_csv_write_dict(results_dict)

        results_dict['Graph-Group'] = "Per Stations Rate UL"
        results_dict['short-description'] = "UL {ul} bps pdu {ul_pdu} {sta_count} STA".format(
            ul=ul, ul_pdu=ul_pdu, sta_count=sta_count)
        results_dict['numeric-score'] = "{}".format(total_ul_bps)
        results_dict['Units'] = "bps"
        self.kpi_csv.kpi_csv_write_dict(results_dict)

        results_dict['Graph-Group'] = "Per Stations Rate UL+DL"
        results_dict['short-description'] = "UL {ul} bps pdu {ul_pdu} + DL {dl} bps pud {dl_pdu}- {sta_count} STA".format(
            ul=ul, ul_pdu=ul_pdu, dl=dl, dl_pdu=dl_pdu, sta_count=sta_count)
        results_dict['numeric-score'] = "{}".format(
            (total_ul_bps + total_dl_bps))
        results_dict['Units'] = "bps"
        self.kpi_csv.kpi_csv_write_dict(results_dict)

        results_dict['Graph-Group'] = "Per Stations Rate DL"
        results_dict['short-description'] = "DL LL {dl} bps  pdu {dl_pdu}  {sta_count} STA".format(
            dl=dl, dl_pdu=dl_pdu, sta_count=sta_count)
        results_dict['numeric-score'] = "{}".format(total_dl_ll_bps)
        results_dict['Units'] = "bps"
        self.kpi_csv.kpi_csv_write_dict(results_dict)

        results_dict['Graph-Group'] = "Per Stations Rate UL"
        results_dict['short-description'] = "UL LL {ul} bps pdu {ul_pdu} {sta_count} STA".format(
            ul=ul, ul_pdu=ul_pdu, sta_count=sta_count)
        results_dict['numeric-score'] = "{}".format(total_ul_ll_bps)
        results_dict['Units'] = "bps"
        self.kpi_csv.kpi_csv_write_dict(results_dict)

        results_dict['Graph-Group'] = "Per Stations Rate UL+DL"
        results_dict['short-description'] = "UL LL {ul} bps pdu {ul_pdu} + DL LL {dl} bps pud {dl_pdu}- {sta_count} STA".format(
            ul=ul, ul_pdu=ul_pdu, dl=dl, dl_pdu=dl_pdu, sta_count=sta_count)
        results_dict['numeric-score'] = "{}".format(
            (total_ul_ll_bps + total_dl_ll_bps))
        results_dict['Units'] = "bps"
        self.kpi_csv.kpi_csv_write_dict(results_dict)

    # Results csv
    def record_results(
            self,
            sta_count,
            ul,
            dl,
            ul_pdu,
            dl_pdu,
            atten,
            total_dl_bps,
            total_ul_bps,
            total_dl_ll_bps,
            total_ul_ll_bps):

        tags = dict()
        tags['requested-ul-bps'] = ul
        tags['requested-dl-bps'] = dl
        tags['ul-pdu-size'] = ul_pdu
        tags['dl-pdu-size'] = dl_pdu
        tags['station-count'] = sta_count
        tags['attenuation'] = atten
        tags["script"] = 'test_l3_longevity'

        # Add user specified tags
        for k in self.user_tags:
            tags[k[0]] = k[1]

        now = str(datetime.datetime.utcnow().isoformat())

        print(
            "NOTE:  Adding results to influx, total-download-bps: %s  upload: %s  bi-directional: %s\n" %
            (total_dl_bps, total_ul_bps, (total_ul_bps + total_dl_bps)))

        if self.influxdb is not None:
            self.influxdb.post_to_influx(
                "total-download-bps", total_dl_bps, tags, now)
            self.influxdb.post_to_influx(
                "total-upload-bps", total_ul_bps, tags, now)
            self.influxdb.post_to_influx(
                "total-bi-directional-bps",
                total_ul_bps +
                total_dl_bps,
                tags,
                now)

        if self.csv_results_file:
            row = [self.epoch_time, self.time_stamp(), sta_count,
                   ul, ul, dl, dl, dl_pdu, dl_pdu, ul_pdu, ul_pdu,
                   atten,
                   total_dl_bps, total_ul_bps, (total_ul_bps + total_dl_bps),
                   total_dl_ll_bps, total_ul_ll_bps, (
                       total_ul_ll_bps + total_dl_ll_bps)
                   ]
            # Add values for any user specified tags
            for k in self.user_tags:
                row.append(k[1])

            self.csv_results_writer.writerow(row)
            self.csv_results_file.flush()

    # Stop traffic and admin down stations.
    def stop(self):
        self.cx_profile.stop_cx()
        self.multicast_profile.stop_mc()
        for station_list in self.station_lists:
            for station_name in station_list:
                self.admin_down(station_name)

    # Remove traffic connections and stations.
    def cleanup(self):
        self.cx_profile.cleanup()
        self.multicast_profile.cleanup()
        for station_profile in self.station_profiles:
            station_profile.cleanup()

    @staticmethod
    def csv_generate_column_headers():
        csv_rx_headers = ['Time epoch', 'Time', 'Monitor', 'UL-Min-Requested', 'UL-Max-Requested', 'DL-Min-Requested',
                          'DL-Max-Requested', 'UL-Min-PDU', 'UL-Max-PDU', 'DL-Min-PDU', 'DL-Max-PDU',
                          "average_rx_data_bytes"]
        return csv_rx_headers

    def csv_generate_port_column_headers(self):
        csv_rx_headers = [
            'Time epoch',
            'Time',
            'Station-Count',
            'UL-Min-Requested',
            'UL-Max-Requested',
            'DL-Min-Requested',
            'DL-Max-Requested',
            'UL-Min-PDU',
            'UL-Max-PDU',
            'DL-Min-PDU',
            'DL-Max-PDU',
            'Attenuation',
            'Name',
            'Rx-Bps',
            'Tx-Bps',
            'Rx-Link-Rate',
            'Tx-Link-Rate',
            'RSSI',
            'AP',
            'Mode',
            'Rx-Latency',
            'Rx-Jitter',
            'Ul-Rx-Goodput-bps',
            'Ul-Rx-Rate-ll',
            'Ul-Rx-Pkts-ll',
            'Dl-Rx-Goodput-bps',
            'Dl-Rx-Rate-ll',
            'Dl-Rx-Pkts-ll']
        # Add in columns we are going to query from the AP
        for col in self.ap_stats_col_titles:
            csv_rx_headers.append(col)

        return csv_rx_headers

    def csv_generate_ul_port_column_headers(self):
        csv_ul_rx_headers = [
            'Time epoch',
            'Time',
            'Station-Count',
            'UL-Min-Requested',
            'UL-Max-Requested',
            'DL-Min-Requested',
            'DL-Max-Requested',
            'UL-Min-PDU',
            'UL-Max-PDU',
            'DL-Min-PDU',
            'DL-Max-PDU',
            'Attenuation',
            'Name',
            'Rx-Bps',
            'Tx-Bps',
            'Rx-Link-Rate',
            'Tx-Link-Rate',
            'RSSI',
            'AP',
            'Mode',
            'Rx-Latency',
            'Rx-Jitter',
            'Ul-Rx-Goodput-bps',
            'Ul-Rx-Rate-ll',
            'Ul-Rx-Pkts-ll',
            'Dl-Rx-Goodput-bps',
            'Dl-Rx-Rate-ll',
            'Dl-Rx-Pkts-ll']
        # Add in columns we are going to query from the AP
        for col in self.ap_stats_ul_col_titles:
            csv_ul_rx_headers.append(col)

        return csv_ul_rx_headers

    def csv_generate_results_column_headers(self):
        csv_rx_headers = [
            'Time epoch',
            'Time',
            'Station-Count',
            'UL-Min-Requested',
            'UL-Max-Requested',
            'DL-Min-Requested',
            'DL-Max-Requested',
            'UL-Min-PDU',
            'UL-Max-PDU',
            'DL-Min-PDU',
            'DL-Max-PDU',
            'Attenuation',
            'Total-Download-Bps',
            'Total-Upload-Bps',
            'Total-UL/DL-Bps',
            'Total-Download-LL-Bps',
            'Total-Upload-LL-Bps',
            'Total-UL/DL-LL-Bps']
        for k in self.user_tags:
            csv_rx_headers.append(k[0])

        return csv_rx_headers

    # Write initial headers to csv file.
    def csv_add_column_headers(self):
        if self.csv_results_file is not None:
            self.csv_results_writer.writerow(
                self.csv_generate_results_column_headers())
            self.csv_results_file.flush()

    # Write initial headers to port csv file.
    def csv_add_port_column_headers(self, eid_name, headers):
        # if self.csv_file is not None:
        fname = self.outfile[:-4]  # Strip '.csv' from file name
        fname = fname + "-dl-" + eid_name + ".csv"
        pfile = open(fname, "w")
        port_csv_writer = csv.writer(pfile, delimiter=",")
        self.port_csv_files[eid_name] = pfile
        self.port_csv_writers[eid_name] = port_csv_writer

        port_csv_writer.writerow(headers)
        pfile.flush()

    def csv_add_ul_port_column_headers(self, eid_name, headers):
        # if self.csv_file is not None:
        fname = self.outfile[:-4]  # Strip '.csv' from file name
        fname = fname + "-ul-" + eid_name + ".csv"
        pfile = open(fname, "w")
        ul_port_csv_writer = csv.writer(pfile, delimiter=",")
        self.ul_port_csv_files[eid_name] = pfile
        self.ul_port_csv_writers[eid_name] = ul_port_csv_writer

        ul_port_csv_writer.writerow(headers)
        pfile.flush()

    @staticmethod
    def csv_validate_list(csv_list, length):
        if len(csv_list) < length:
            csv_list = csv_list + [('no data', 'no data')] * \
                (length - len(csv_list))
        return csv_list

    @staticmethod
    def csv_add_row(row, writer, csv_file):
        if csv_file is not None:
            writer.writerow(row)
            csv_file.flush()

    # End of the main class.

# Check some input values.


def valid_endp_types(_endp_type):
    etypes = _endp_type.split(',')
    for endp_type in etypes:
        valid_endp_type = [
            'lf',
            'lf_udp',
            'lf_udp6',
            'lf_tcp',
            'lf_tcp6',
            'mc_udp',
            'mc_udp6']
        if not (str(endp_type) in valid_endp_type):
            print(
                'invalid endp_type: %s. Valid types lf, lf_udp, lf_udp6, lf_tcp, lf_tcp6, mc_udp, mc_udp6' %
                endp_type)
            exit(1)
    return _endp_type


# Starting point for running this from cmd line.
def main():
    lfjson_host = "localhost"
    lfjson_port = 8080
    endp_types = "lf_udp"

    parser = argparse.ArgumentParser(
        prog='test_l3_longevity.py',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        Useful Information:
            1. Polling interval for checking traffic is fixed at 1 minute
            2. The test will generate csv file
            3. The tx/rx rates are fixed at 256000 bits per second
            4. Maximum stations per radio based on radio
            ''',

        description='''\
test_l3_longevity.py:
--------------------

Summary :
----------
create stations, create traffic between upstream port and stations,  run traffic.
The traffic on the stations will be checked once per minute to verify that traffic is transmitted
and received.

Generic command layout:
-----------------------
./test_l3_longevity.py --mgr <ip_address> --test_duration <duration> --endp_type <traffic types>
--upstream_port <shelf>.<resource>.<port>
--radio "radio==<shelf>.<resource>.<radio> stations==<number stations> ssid==<ssid> ssid_pw==<ssid password>
security==<security type: wpa2, open, wpa3>" --debug

Multiple radios may be entered with individual --radio switches

# UDP bi-directional test, no use of controller.
./test_l3_longevity.py --mgr localhost --endp_type 'lf_udp lf_tcp' --upstream_port 1.1.eth1
--radio "radio==1.1.wiphy0 stations==10 ssid==ASUS_70 ssid_pw==[BLANK] security==open"
--radio "radio==1.1.wiphy2 stations==1 ssid==ASUS_70 ssid_pw==[BLANK] security==open" --test_duration 30s

# Port resets, chooses random value between min and max
./test_l3_longevity.py --lfmgr LF_MGR_IP --test_duration 90s --polling_interval 10s --upstream_port 1.1.eth2
--radio 'radio==1.1.wiphy1,stations==4,ssid==SSID_USED,ssid_pw==SSID_PW_USED,security==SECURITY_USED,
reset_port_enable==TRUE,reset_port_time_min==10s,reset_port_time_max==20s'
--endp_type lf_udp --rates_are_totals --side_a_min_bps=20000 --side_b_min_bps=300000000"


<duration>: number followed by one of the following
d - days
h - hours
m - minutes
s - seconds

<traffic type>:
lf_udp  : IPv4 UDP traffic
lf_tcp  : IPv4 TCP traffic
lf_udp6 : IPv6 UDP traffic
lf_tcp6 : IPv6 TCP traffic
mc_udp  : IPv4 multi cast UDP traffic
mc_udp6 : IPv6 multi cast UDP traffic

<tos>:
BK, BE, VI, VO:  Optional wifi related Tos Settings.  Or, use your preferred numeric values.

#################################
#Command switches
#################################

--mgr <hostname for where LANforge GUI is running>',default='localhost'
-d  / --test_duration <how long to run>  example --time 5d (5 days) default: 3m options: number followed by d, h, m or s',default='3m'
--tos:  Support different ToS settings: BK | BE | VI | VO | numeric',default="BE"
--debug:  Enable debugging',default=False
-t  / --endp_type <types of traffic> example --endp_type \"lf_udp lf_tcp mc_udp\"  Default: lf_udp , options: lf_udp, lf_udp6, lf_tcp, lf_tcp6, mc_udp, mc_udp6',
                        default='lf_udp', type=valid_endp_types
-u / --upstream_port <cross connect upstream_port> example: --upstream_port eth1',default='eth1')
-o / --outfile <Output file for csv data>", default='longevity_results'

#########################################
# Examples
# #######################################
Example #1  running traffic with two radios
1. Test duration 4 minutes
2. Traffic IPv4 TCP
3. Upstream-port eth1
4. Shelf 1 Resource 1 Radio wiphy0 has 32 stations, ssid = candelaTech-wpa2-x2048-4-1, ssid password = candelaTech-wpa2-x2048-4-1
5. Shelf 1 Resource 2 Radio wiphy1 has 64 stations, ssid = candelaTech-wpa2-x2048-5-3, ssid password = candelaTech-wpa2-x2048-5-3
6. Create connections with TOS of BK and VI

Command:
./test_l3_longevity.py --test_duration 4m --endp_type \"lf_tcp lf_udp mc_udp\" --tos \"BK VI\" --upstream_port 1.1.eth1
--radio "radio==1.1.wiphy0 stations==32 ssid==candelaTech-wpa2-x2048-4-1 ssid_pw==candelaTech-wpa2-x2048-4-1 security==wpa2"
--radio "radio==1.2.wiphy1 stations==64 ssid==candelaTech-wpa2-x2048-5-3 ssid_pw==candelaTech-wpa2-x2048-5-3 security==wpa2"

Setting wifi_settings per radio
./test_l3_longevity.py  --lfmgr 192.168.100.116 --local_lf_report_dir /home/lanforge/html-reports/ --test_duration 15s
--polling_interval 5s --upstream_port 1.1.eth2
--radio "radio==1.1.wiphy1 stations==4 ssid==asus11ax-5 ssid_pw==hello123 security==wpa2  mode==0 wifi_settings==wifi_settings
    enable_flags==('ht160_enable'|'wpa2_enable'|'80211u_enable'|'create_admin_down'|'ht160_enable') "
--endp_type lf_udp --rates_are_totals --side_a_min_bps=20000 --side_b_min_bps=300000000 --test_rig CT-US-001 --test_tag 'l3_longevity'

        wifi_mode
        Input       : Enum Val  : Shown by nc_show_ports

        AUTO        |  0        #  802.11g
        802.11a     |  1        #  802.11a
        b           |  2        #  802.11b
        g           |  3        #  802.11g
        abg         |  4        #  802.11abg
        abgn        |  5        #  802.11abgn
        bgn         |  6        #  802.11bgn
        bg          |  7        #  802.11bg
        abgnAC      |  8        #  802.11abgn-AC
        anAC        |  9        #  802.11an-AC
        an          | 10        #  802.11an
        bgnAC       | 11        #  802.11bgn-AC
        abgnAX      | 12        #  802.11abgn-AX
                                #     a/b/g/n/AC/AX (dual-band AX) support
        bgnAX       | 13        #  802.11bgn-AX
        anAX        | 14        #  802.11an-AX
        aAX         | 15        #  802.11a-AX (6E disables /n and /ac)


        wifi_settings flags are currently defined as:
        wpa_enable           | 0x10         # Enable WPA
        custom_conf          | 0x20         # Use Custom wpa_supplicant config file.
        wep_enable           | 0x200        # Use wpa_supplicant configured for WEP encryption.
        wpa2_enable          | 0x400        # Use wpa_supplicant configured for WPA2 encryption.
        ht40_disable         | 0x800        # Disable HT-40 even if hardware and AP support it.
        scan_ssid            | 0x1000       # Enable SCAN-SSID flag in wpa_supplicant.
        passive_scan         | 0x2000       # Use passive scanning (don't send probe requests).
        disable_sgi          | 0x4000       # Disable SGI (Short Guard Interval).
        lf_sta_migrate       | 0x8000       # OK-To-Migrate (Allow station migration between LANforge radios)
        verbose              | 0x10000      # Verbose-Debug:  Increase debug info in wpa-supplicant and hostapd logs.
        80211u_enable        | 0x20000      # Enable 802.11u (Interworking) feature.
        80211u_auto          | 0x40000      # Enable 802.11u (Interworking) Auto-internetworking feature.  Always enabled currently.
        80211u_gw            | 0x80000      # AP Provides access to internet (802.11u Interworking)
        80211u_additional    | 0x100000     # AP requires additional step for access (802.11u Interworking)
        80211u_e911          | 0x200000     # AP claims emergency services reachable (802.11u Interworking)
        80211u_e911_unauth   | 0x400000     # AP provides Unauthenticated emergency services (802.11u Interworking)
        hs20_enable          | 0x800000     # Enable Hotspot 2.0 (HS20) feature.  Requires WPA-2.
        disable_gdaf         | 0x1000000    # AP:  Disable DGAF (used by HotSpot 2.0).
        8021x_radius         | 0x2000000    # Use 802.1x (RADIUS for AP).
        80211r_pmska_cache   | 0x4000000    # Enable oportunistic PMSKA caching for WPA2 (Related to 802.11r).
        disable_ht80         | 0x8000000    # Disable HT80 (for AC chipset NICs only)
        ibss_mode            | 0x20000000   # Station should be in IBSS mode.
        osen_enable          | 0x40000000   # Enable OSEN protocol (OSU Server-only Authentication)
        disable_roam         | 0x80000000   # Disable automatic station roaming based on scan results.
        ht160_enable         | 0x100000000  # Enable HT160 mode.
        disable_fast_reauth  | 0x200000000  # Disable fast_reauth option for virtual stations.
        mesh_mode            | 0x400000000  # Station should be in MESH mode.
        power_save_enable    | 0x800000000  # Station should enable power-save.  May not work in all drivers/configurations.
        create_admin_down    | 0x1000000000 # Station should be created admin-down.
        wds-mode             | 0x2000000000 # WDS station (sort of like a lame mesh), not supported on ath10k
        no-supp-op-class-ie  | 0x4000000000 # Do not include supported-oper-class-IE in assoc requests.  May work around AP bugs.
        txo-enable           | 0x8000000000 # Enable/disable tx-offloads, typically managed by set_wifi_txo command
        use-wpa3             | 0x10000000000 # Enable WPA-3 (SAE Personal) mode.
        use-bss-transition   | 0x80000000000 # Enable BSS transition.
        disable-twt          | 0x100000000000 # Disable TWT mode

===============================================================================
 ** FURTHER INFORMATION **
    Using the layer3_cols flag:

    Currently the output function does not support inputting the columns in layer3_cols the way they are displayed in the GUI. This quirk is under construction. To output
    certain columns in the GUI in your final report, please match the according GUI column display to it's counterpart to have the columns correctly displayed in
    your report.

    GUI Column Display       Layer3_cols argument to type in (to print in report)

    Name                |  'name'
    EID                 |  'eid'
    Run                 |  'run'
    Mng                 |  'mng'
    Script              |  'script'
    Tx Rate             |  'tx rate'
    Tx Rate (1 min)     |  'tx rate (1&nbsp;min)'
    Tx Rate (last)      |  'tx rate (last)'
    Tx Rate LL          |  'tx rate ll'
    Rx Rate             |  'rx rate'
    Rx Rate (1 min)     |  'rx rate (1&nbsp;min)'
    Rx Rate (last)      |  'rx rate (last)'
    Rx Rate LL          |  'rx rate ll'
    Rx Drop %           |  'rx drop %'
    Tx PDUs             |  'tx pdus'
    Tx Pkts LL          |  'tx pkts ll'
    PDU/s TX            |  'pdu/s tx'
    Pps TX LL           |  'pps tx ll'
    Rx PDUs             |  'rx pdus'
    Rx Pkts LL          |  'pps rx ll'
    PDU/s RX            |  'pdu/s tx'
    Pps RX LL           |  'pps rx ll'
    Delay               |  'delay'
    Dropped             |  'dropped'
    Jitter              |  'jitter'
    Tx Bytes            |  'tx bytes'
    Rx Bytes            |  'rx bytes'
    Replays             |  'replays'
    TCP Rtx             |  'tcp rtx'
    Dup Pkts            |  'dup pkts'
    Rx Dup %            |  'rx dup %'
    OOO Pkts            |  'ooo pkts'
    Rx OOO %            |  'rx ooo %'
    RX Wrong Dev        |  'rx wrong dev'
    CRC Fail            |  'crc fail'
    RX BER              |  'rx ber'
    CX Active           |  'cx active'
    CX Estab/s          |  'cx estab/s'
    1st RX              |  '1st rx'
    CX TO               |  'cx to'
    Pattern             |  'pattern'
    Min PDU             |  'min pdu'
    Max PDU             |  'max pdu'
    Min Rate            |  'min rate'
    Max Rate            |  'max rate'
    Send Buf            |  'send buf'
    Rcv Buf             |  'rcv buf'
    CWND                |  'cwnd'
    TCP MSS             |  'tcp mss'
    Bursty              |  'bursty'
    A/B                 |  'a/b'
    Elapsed             |  'elapsed'
    Destination Addr    |  'destination addr'
    Source Addr         |  'source addr'

    Using the port_mgr_cols flag:
         '4way time (us)'
         'activity'
         'alias'
         'anqp time (us)'
         'ap'
         'beacon'
         'bps rx'
         'bps rx ll'
         'bps tx'
         'bps tx ll'
         'bytes rx ll'
         'bytes tx ll'
         'channel'
         'collisions'
         'connections'
         'crypt'
         'cx ago'
         'cx time (us)'
         'device'
         'dhcp (ms)'
         'down'
         'entity id'
         'gateway ip'
         'ip'
         'ipv6 address'
         'ipv6 gateway'
         'key/phrase'
         'login-fail'
         'login-ok'
         'logout-fail'
         'logout-ok'
         'mac'
         'mask'
         'misc'
         'mode'
         'mtu'
         'no cx (us)'
         'noise'
         'parent dev'
         'phantom'
         'port'
         'port type'
         'pps rx'
         'pps tx'
         'qlen'
         'reset'
         'retry failed'
         'rx bytes'
         'rx crc'
         'rx drop'
         'rx errors'
         'rx fifo'
         'rx frame'
         'rx length'
         'rx miss'
         'rx over'
         'rx pkts'
         'rx-rate'
         'sec'
         'signal'
         'ssid'
         'status'
         'time-stamp'
         'tx abort'
         'tx bytes'
         'tx crr'
         'tx errors'
         'tx fifo'
         'tx hb'
         'tx pkts'
         'tx wind'
         'tx-failed %'
         'tx-rate'
         'wifi retries'

    Can't decide what columns to use? You can just use 'all' to select all available columns from both tables.


        ''')

    parser.add_argument(
        '--local_lf_report_dir',
        help='--local_lf_report_dir override the report path, primary use when running test in test suite',
        default="")
    parser.add_argument(
        "--test_rig",
        default="",
        help="test rig for kpi.csv, testbed that the tests are run on")
    parser.add_argument(
        "--test_tag",
        default="",
        help="test tag for kpi.csv,  test specific information to differenciate the test")
    parser.add_argument(
        "--dut_hw_version",
        default="",
        help="dut hw version for kpi.csv, hardware version of the device under test")
    parser.add_argument(
        "--dut_sw_version",
        default="",
        help="dut sw version for kpi.csv, software version of the device under test")
    parser.add_argument(
        "--dut_model_num",
        default="",
        help="dut model for kpi.csv,  model number / name of the device under test")
    parser.add_argument(
        "--dut_serial_num",
        default="",
        help="dut serial for kpi.csv, serial number / serial number of the device under test")
    parser.add_argument(
        "--test_priority",
        default="",
        help="dut model for kpi.csv,  test-priority is arbitrary number")
    parser.add_argument(
        "--test_id",
        default="l3 Longevity",
        help="test-id for kpi.csv,  script or test name")
    '''
    Other values that are included in the kpi.csv row.
    short-description : short description of the test
    pass/fail : set blank for performance tests
    numeric-score : this is the value for the y-axis (x-axis is a timestamp),  numeric value of what was measured
    test details : what was measured in the numeric-score,  e.g. bits per second, bytes per second, upload speed, minimum cx time (ms)
    Units : units used for the numeric-scort
    Graph-Group - For the lf_qa.py dashboard

    '''
    parser.add_argument(
        '-o',
        '--csv_outfile',
        help="--csv_outfile <Output file for csv data>",
        default="")

    parser.add_argument(
        '--tty',
        help='--tty \"/dev/ttyUSB2\" the serial interface to the AP',
        default="")
    parser.add_argument(
        '--baud',
        help='--baud \"9600\"  AP baud rate for the serial interface',
        default="9600")
    parser.add_argument(
        '--mgr',
        '--lfmgr',
        dest='lfmgr',
        help='--lfmgr <hostname for where LANforge GUI is running>',
        default='localhost')
    parser.add_argument(
        '--test_duration',
        help='--test_duration <how long to run>  example --time 5d (5 days) default: 3m options: number followed by d, h, m or s',
        default='3m')
    parser.add_argument(
        '--tos',
        help='--tos:  Support different ToS settings: BK | BE | VI | VO | numeric',
        default="BE")
    parser.add_argument(
        '--debug',
        help='--debug flag present debug on  enable debugging',
        action='store_true')
    parser.add_argument(
        '-t',
        '--endp_type',
        help=(
            '--endp_type <types of traffic> example --endp_type \"lf_udp lf_tcp mc_udp\" '
            ' Default: lf_udp , options: lf_udp, lf_udp6, lf_tcp, lf_tcp6, mc_udp, mc_udp6'),
        default='lf_udp',
        type=valid_endp_types)
    parser.add_argument(
        '-u',
        '--upstream_port',
        help='--upstream_port <cross connect upstream_port> example: --upstream_port eth1',
        default='eth1')
    parser.add_argument(
        '--downstream_port',
        help='--downstream_port <cross connect downstream_port> example: --downstream_port eth2', default=None)
    parser.add_argument(
        '--polling_interval',
        help="--polling_interval <seconds>",
        default='60s')

    parser.add_argument(
        '-r', '--radio',
        action='append',
        nargs=1,
        help=(' --radio'
              ' "radio==<number_of_wiphy stations=<=number of stations>'
              ' ssid==<ssid> ssid_pw==<ssid password> security==<security> '
              ' wifi_settings==True wifi_mode==<wifi_mode>'
              ' enable_flags==<enable_flags> '
              ' reset_port_enable==True reset_port_time_min==<min>s'
              ' reset_port_time_max==<max>s" ')
    )
    parser.add_argument(
        '--ap_read',
        help='--ap_read  flag present enable reading ap',
        action='store_true')
    parser.add_argument(
        '--ap_port',
        help='--ap_port \'/dev/ttyUSB0\'',
        default='/dev/ttyUSB0')
    parser.add_argument(
        '--ap_baud',
        help='--ap_baud \'115200\'',
        default='115200')
    # note wl2 is the 6G interface , check the MAC ifconfig -a of the
    # interface to the AP BSSID connection (default may be eth8)
    parser.add_argument(
        '--ap_cmd_6g',
        help='ap_cmd_6g \'wl -i wl2 bs_data\'',
        default="wl -i wl2 bs_data")
    # note wl1 is the 5G interface , check the MAC ifconfig -a of the
    # interface to the AP BSSID connection (default may be eth7)
    parser.add_argument(
        '--ap_cmd_5g',
        help='ap_cmd_5g \'wl -i wl1 bs_data\'',
        default="wl -i wl1 bs_data")
    # note wl1 is the 2.4G interface , check the MAC ifconfig -a of the
    # interface to the AP BSSID connection (default may be eth6)
    parser.add_argument(
        '--ap_cmd_2g',
        help='ap_cmd_2g \'wl -i wl0 bs_data\'',
        default="wl -i wl0 bs_data")
    # note wl2 is the 6G interface , check the MAC ifconfig -a of the
    # interface to the AP BSSID connection (default may be eth8)
    parser.add_argument(
        '--ap_cmd_ul_6g',
        help='ap_cmd_ul_6g \'wl -i wl2 rx_report\'',
        default="wl -i wl2 rx_report")
    # note wl1 is the 5G interface , check the MAC ifconfig -a of the
    # interface to the AP BSSID connection (default may be eth7)
    parser.add_argument(
        '--ap_cmd_ul_5g',
        help='ap_cmd_ul_5g \'wl -i wl1 rx_report\'',
        default="wl -i wl1 rx_report")
    # note wl1 is the 2.4G interface , check the MAC ifconfig -a of the
    # interface to the AP BSSID connection (default may be eth6)
    parser.add_argument(
        '--ap_cmd_ul_2g',
        help='ap_cmd_ul_2g \'wl -i wl0 rx_report\'',
        default="wl -i wl0 rx_report")
    parser.add_argument(
        '--ap_chanim_cmd_6g',
        help='ap_chanim_cmd_6g \'wl -i wl2 chanim_stats\'',
        default="wl -i wl2 chanim_stats")
    parser.add_argument(
        '--ap_chanim_cmd_5g',
        help='ap_chanim_cmd_5g \'wl -i wl1 chanim_stats\'',
        default="wl -i wl1 chanim_stats")
    parser.add_argument(
        '--ap_chanim_cmd_2g',
        help='ap_chanim_cmd_2g \'w1 -i wl0 chanim_stats\'',
        default="wl -i wl0 chanim_stats")
    parser.add_argument(
        '--ap_scheduler_stats',
        help='--ap_scheduler_stats flag to clear stats run test then dump ul and dl stats to file',
        action='store_true')
    parser.add_argument(
        '--ap_ofdma_stats',
        help='--ap_ofdma_stats flag to clear stats run test then dumps wl -i wl1 muinfo -v and wl 0i wl0 muinof -v to file',
        action='store_true')

    parser.add_argument(
        '--ap_test_mode',
        help='ap_test_mode flag present use ap canned data',
        action='store_true')

    parser.add_argument(
        '-amr',
        '--side_a_min_bps',
        help='--side_a_min_bps, requested downstream min tx rate, comma separated list for multiple iterations.  Default 256k',
        default="256000")
    parser.add_argument(
        '-amp',
        '--side_a_min_pdu',
        help='--side_a_min_pdu, downstream pdu size, comma separated list for multiple iterations.  Default MTU',
        default="MTU")
    parser.add_argument(
        '-bmr',
        '--side_b_min_bps',
        help='--side_b_min_bps, requested upstream min tx rate, comma separated list for multiple iterations.  Default 256000',
        default="256000")
    parser.add_argument(
        '-bmp',
        '--side_b_min_pdu',
        help='--side_b_min_pdu, upstream pdu size, comma separated list for multiple iterations. Default MTU',
        default="MTU")
    parser.add_argument(
        "--rates_are_totals",
        default=False,
        help="Treat configured rates as totals instead of using the un-modified rate for every connection.",
        action='store_true')
    parser.add_argument(
        "--multiconn",
        default=1,
        help="Configure multi-conn setting for endpoints.  Default is 1 (auto-helper is enabled by default as well).")

    parser.add_argument(
        '--attenuators',
        help='--attenuators,  comma separated list of attenuator module eids:  shelf.resource.atten-serno.atten-idx',
        default="")
    parser.add_argument(
        '--atten_vals',
        help='--atten_vals,  comma separated list of attenuator settings in ddb units (1/10 of db)',
        default="")

    influx_add_parser_args(parser)

    parser.add_argument(
        "--cap_ctl_out",
        help="--cap_ctl_out, switch the controller output will be captured",
        action='store_true')
    parser.add_argument(
        "--wait",
        help="--wait <time> , time to wait at the end of the test",
        default='0')

    args = parser.parse_args()

    # print("args: {}".format(args))

    # for kpi.csv generation
    local_lf_report_dir = args.local_lf_report_dir
    test_rig = args.test_rig
    test_tag = args.test_tag
    dut_hw_version = args.dut_hw_version
    dut_sw_version = args.dut_sw_version
    dut_model_num = args.dut_model_num
    dut_serial_num = args.dut_serial_num
    # test_priority = args.test_priority  # this may need to be set per test
    test_id = args.test_id

    if args.ap_read:
        ap_read = args.ap_read
    else:
        ap_read = False

    if args.ap_scheduler_stats:
        ap_scheduler_stats = args.ap_scheduler_stats
    else:
        ap_scheduler_stats = False

    if args.ap_ofdma_stats:
        ap_ofdma_stats = args.ap_ofdma_stats
    else:
        ap_ofdma_stats = False

    if args.ap_test_mode:
        ap_test_mode = args.ap_test_mode
    else:
        ap_test_mode = False

    if args.ap_port:
        ap_port = args.ap_port

    if args.ap_baud:
        ap_baud = args.ap_baud

    if args.ap_cmd_6g:
        ap_cmd_6g = args.ap_cmd_6g

    if args.ap_cmd_5g:
        ap_cmd_5g = args.ap_cmd_5g

    if args.ap_cmd_2g:
        ap_cmd_2g = args.ap_cmd_2g

    if args.ap_cmd_ul_6g:
        ap_cmd_ul_6g = args.ap_cmd_ul_6g

    if args.ap_cmd_ul_5g:
        ap_cmd_ul_5g = args.ap_cmd_ul_5g

    if args.ap_cmd_ul_2g:
        ap_cmd_ul_2g = args.ap_cmd_ul_2g

    if args.ap_chanim_cmd_6g:
        ap_chanim_cmd_6g = args.ap_chanim_cmd_6g

    if args.ap_chanim_cmd_5g:
        ap_chanim_cmd_5g = args.ap_chanim_cmd_5g

    if args.ap_chanim_cmd_2g:
        ap_chanim_cmd_2g = args.ap_chanim_cmd_2g

    if args.test_duration:
        test_duration = args.test_duration

    if args.polling_interval:
        polling_interval = args.polling_interval

    if args.endp_type:
        endp_types = args.endp_type

    if args.lfmgr:
        lfjson_host = args.lfmgr

    if args.upstream_port:
        side_b = args.upstream_port

    if args.downstream_port:
        side_a = args.downstream_port
    else:
        side_a = None

    if args.radio:
        radios = args.radio
    else:
        radios = None

    # Create report, when running with the test framework (lf_check.py)
    # results need to be in the same directory
    if local_lf_report_dir != "":
        report = lf_report.lf_report(
            _path=local_lf_report_dir,
            _results_dir_name="test_l3_longevity",
            _output_html="test_l3_longevity.html",
            _output_pdf="test_l3_longevity.pdf")
    else:
        report = lf_report.lf_report(
            _results_dir_name="test_l3_longevity",
            _output_html="test_l3_longevity.html",
            _output_pdf="test_l3_longevity.pdf")

    # Get the report path to create the kpi.csv path
    kpi_path = report.get_report_path()
    print("kpi_path :{kpi_path}".format(kpi_path=kpi_path))

    kpi_csv = lf_kpi_csv.lf_kpi_csv(
        _kpi_path=kpi_path,
        _kpi_test_rig=test_rig,
        _kpi_test_tag=test_tag,
        _kpi_dut_hw_version=dut_hw_version,
        _kpi_dut_sw_version=dut_sw_version,
        _kpi_dut_model_num=dut_model_num,
        _kpi_dut_serial_num=dut_serial_num,
        _kpi_test_id=test_id)

    if args.csv_outfile is not None:
        current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        csv_outfile = "{}_{}-test_l3_longevity.csv".format(
            args.csv_outfile, current_time)
        csv_outfile = report.file_add_path(csv_outfile)
        print("csv output file : {}".format(csv_outfile))

    influxdb = None
    if args.influx_bucket is not None:
        influxdb = RecordInflux(_influx_host=args.influx_host,
                                _influx_port=args.influx_port,
                                _influx_org=args.influx_org,
                                _influx_token=args.influx_token,
                                _influx_bucket=args.influx_bucket)

    MAX_NUMBER_OF_STATIONS = 1000

    radio_name_list = []
    number_of_stations_per_radio_list = []
    ssid_list = []
    ssid_password_list = []
    ssid_security_list = []
    station_lists = []

    # wifi settings configuration
    wifi_mode_list = []
    wifi_enable_flags_list = []

    # optional radio configuration
    reset_port_enable_list = []
    reset_port_time_min_list = []
    reset_port_time_max_list = []

    if radios is not None:
        print("radios {}".format(radios))
        for radio_ in radios:
            radio_keys = ['radio', 'stations', 'ssid', 'ssid_pw', 'security']
            print("radio_dict before format {}".format(radio_))
            radio_info_dict = dict(
                map(
                    lambda x: x.split('=='),
                    str(radio_).replace(
                        '"',
                        '').replace(
                        '[',
                        '').replace(
                        ']',
                        '').replace(
                        "'",
                        "").replace(
                            ",",
                        " ").split()))
            # radio_info_dict = dict(map(lambda x: x.split('=='), str(radio_).replace('"', '').split()))

            print("radio_dict {}".format(radio_info_dict))

            for key in radio_keys:
                if key not in radio_info_dict:
                    print(
                        "missing config, for the {}, all of the following need to be present {} ".format(
                            key, radio_keys))
                    exit(1)

            radio_name_list.append(radio_info_dict['radio'])
            number_of_stations_per_radio_list.append(
                radio_info_dict['stations'])
            ssid_list.append(radio_info_dict['ssid'])
            ssid_password_list.append(radio_info_dict['ssid_pw'])
            ssid_security_list.append(radio_info_dict['security'])

            # check for wifi_settings
            wifi_settings_keys = ['wifi_settings']
            wifi_settings_found = True
            for key in wifi_settings_keys:
                if key not in radio_info_dict:
                    print("wifi_settings_keys not enabled")
                    wifi_settings_found = False
                    break

            if wifi_settings_found:
                # Check for additional flags
                if {'wifi_mode', 'enable_flags'}.issubset(
                        radio_info_dict.keys()):
                    print("wifi_settings flags set")
                else:
                    print(
                        "wifi_settings is present wifi_mode, enable_flags need to be set")
                    print(
                        "or remove the wifi_settings or set wifi_settings==False flag on the radio for defaults")
                    exit(1)
                wifi_mode_list.append(radio_info_dict['wifi_mode'])
                enable_flags_str = radio_info_dict['enable_flags'].replace(
                    '(', '').replace(')', '').replace('|', ',')
                enable_flags_list = list(enable_flags_str.split(","))
                wifi_enable_flags_list.append(enable_flags_list)
            else:
                wifi_mode_list.append(0)
                wifi_enable_flags_list.append(
                    ["wpa2_enable", "80211u_enable", "create_admin_down"])

            # check for optional radio key , currently only reset is enabled
            # update for checking for reset_port_time_min, reset_port_time_max
            optional_radio_reset_keys = ['reset_port_enable']
            radio_reset_found = True
            for key in optional_radio_reset_keys:
                if key not in radio_info_dict:
                    # print("port reset test not enabled")
                    radio_reset_found = False
                    break

            if radio_reset_found:
                reset_port_enable_list.append(
                    radio_info_dict['reset_port_enable'])
                reset_port_time_min_list.append(
                    radio_info_dict['reset_port_time_min'])
                reset_port_time_max_list.append(
                    radio_info_dict['reset_port_time_max'])
            else:
                reset_port_enable_list.append(False)
                reset_port_time_min_list.append('0s')
                reset_port_time_max_list.append('0s')

        index = 0
        for (radio_name_, number_of_stations_per_radio_) in zip(
                radio_name_list, number_of_stations_per_radio_list):
            number_of_stations = int(number_of_stations_per_radio_)
            if number_of_stations > MAX_NUMBER_OF_STATIONS:
                print("number of stations per radio exceeded max of : {}".format(
                    MAX_NUMBER_OF_STATIONS))
                quit(1)
            station_list = LFUtils.portNameSeries(
                prefix_="sta",
                start_id_=1 + index * 1000,
                end_id_=number_of_stations + index * 1000,
                padding_number_=10000,
                radio=radio_name_)
            station_lists.append(station_list)
            index += 1

    # print("endp-types: %s"%(endp_types))

    ul_rates = args.side_a_min_bps.split(",")
    dl_rates = args.side_b_min_bps.split(",")
    ul_pdus = args.side_a_min_pdu.split(",")
    dl_pdus = args.side_b_min_pdu.split(",")
    if args.attenuators == "":
        attenuators = []
    else:
        attenuators = args.attenuators.split(",")
    if args.atten_vals == "":
        atten_vals = [-1]
    else:
        atten_vals = args.atten_vals.split(",")

    if len(ul_rates) != len(dl_rates):
        raise ValueError(
            "ERROR:  ul_rates %s and dl_rates %s arrays must be same length\n" %
            (len(ul_rates), len(dl_rates)))
    if len(ul_pdus) != len(dl_pdus):
        raise ValueError(
            "ERROR:  ul_pdus %s and dl_pdus %s arrays must be same length\n" %
            (len(ul_rates), len(dl_rates)))

    ip_var_test = L3VariableTime(
        endp_types=endp_types,
        args=args,
        tos=args.tos,
        side_b=side_b,
        side_a=side_a,
        radio_name_list=radio_name_list,
        number_of_stations_per_radio_list=number_of_stations_per_radio_list,
        ssid_list=ssid_list,
        ssid_password_list=ssid_password_list,
        ssid_security_list=ssid_security_list,
        wifi_mode_list=wifi_mode_list,
        enable_flags_list=wifi_enable_flags_list,
        station_lists=station_lists,
        name_prefix="LT-",
        outfile=csv_outfile,
        reset_port_enable_list=reset_port_enable_list,
        reset_port_time_min_list=reset_port_time_min_list,
        reset_port_time_max_list=reset_port_time_max_list,
        side_a_min_rate=ul_rates,
        side_b_min_rate=dl_rates,
        side_a_min_pdu=ul_pdus,
        side_b_min_pdu=dl_pdus,
        user_tags=args.influx_tag,
        rates_are_totals=args.rates_are_totals,
        mconn=args.multiconn,
        attenuators=attenuators,
        atten_vals=atten_vals,
        number_template="00",
        test_duration=test_duration,
        polling_interval=polling_interval,
        lfclient_host=lfjson_host,
        lfclient_port=lfjson_port,
        debug=args.debug,
        influxdb=influxdb,
        kpi_csv=kpi_csv,  # kpi.csv object
        ap_scheduler_stats=ap_scheduler_stats,
        ap_ofdma_stats=ap_ofdma_stats,
        ap_read=ap_read,
        ap_port=ap_port,
        ap_baud=ap_baud,
        ap_cmd_6g=ap_cmd_6g,
        ap_cmd_5g=ap_cmd_5g,
        ap_cmd_2g=ap_cmd_2g,
        ap_cmd_ul_6g=ap_cmd_ul_6g,
        ap_cmd_ul_5g=ap_cmd_ul_5g,
        ap_cmd_ul_2g=ap_cmd_ul_2g,
        ap_chanim_cmd_6g=ap_chanim_cmd_6g,
        ap_chanim_cmd_5g=ap_chanim_cmd_5g,
        ap_chanim_cmd_2g=ap_chanim_cmd_2g,
        ap_test_mode=ap_test_mode)

    ip_var_test.pre_cleanup()

    ip_var_test.build()
    if not ip_var_test.passes():
        print("build step failed.")
        print(ip_var_test.get_fail_message())
        exit(1)
    ip_var_test.start(False)
    ip_var_test.stop()
    if not ip_var_test.passes():
        print("Test Ended: There were Failures")
        print(ip_var_test.get_fail_message())

    print(
        "Pausing {} seconds for manual inspection before clean up.".format(
            args.wait))
    time.sleep(int(args.wait))
    ip_var_test.cleanup()
    if ip_var_test.passes():
        print("Full test passed, all connections increased rx bytes")

    # Results
    csv_results_file = ip_var_test.get_results_csv()
    report.set_title("L3 Longevity")
    report.build_banner()
    report.set_table_title("L3 Longevity Key Performance Indexes")
    report.build_table_title()
    report.set_table_dataframe_from_csv(csv_results_file)
    report.build_table()
    report.write_html_with_timestamp()
    report.write_index_html()
    # report.write_pdf(_page_size = 'A3', _orientation='Landscape')
    # report.write_pdf_with_timestamp(_page_size='A4', _orientation='Portrait')
    report.write_pdf_with_timestamp(_page_size='A4', _orientation='Landscape')

    # ap scheduler results and write to a file
    if ap_scheduler_stats:
        print("getting umsched and msched ap data and writing to a file")
        file_date = report.get_date()

        ap_6g_umsched_data = ip_var_test.get_ap_6g_umsched()
        ap_6g_umsched = "{}-{}".format(file_date, "ap_6g_umsched.txt")
        ap_6g_umsched = report.file_add_path(ap_6g_umsched)
        ap_6g_umsched_file = open(ap_6g_umsched, "w")
        ap_6g_umsched_file.write(str(ap_6g_umsched_data))
        ap_6g_umsched_file.close()

        ap_6g_msched_data = ip_var_test.get_ap_6g_msched()
        ap_6g_msched = "{}-{}".format(file_date, "ap_6g_msched.txt")
        ap_6g_msched = report.file_add_path(ap_6g_msched)
        ap_6g_msched_file = open(ap_6g_msched, "w")
        ap_6g_msched_file.write(str(ap_6g_msched_data))
        ap_6g_msched_file.close()

        ap_5g_umsched_data = ip_var_test.get_ap_5g_umsched()
        ap_5g_umsched = "{}-{}".format(file_date, "ap_5g_umsched.txt")
        ap_5g_umsched = report.file_add_path(ap_5g_umsched)
        ap_5g_umsched_file = open(ap_5g_umsched, "w")
        ap_5g_umsched_file.write(str(ap_5g_umsched_data))
        ap_5g_umsched_file.close()

        ap_5g_msched_data = ip_var_test.get_ap_5g_msched()
        ap_5g_msched = "{}-{}".format(file_date, "ap_5g_msched.txt")
        ap_5g_msched = report.file_add_path(ap_5g_msched)
        ap_5g_msched_file = open(ap_5g_msched, "w")
        ap_5g_msched_file.write(str(ap_5g_msched_data))
        ap_5g_msched_file.close()

        ap_24g_umsched_data = ip_var_test.get_ap_24g_umsched()
        ap_24g_umsched = "{}-{}".format(file_date, "ap_24g_umsched.txt")
        ap_24g_umsched = report.file_add_path(ap_24g_umsched)
        ap_24g_umsched_file = open(ap_24g_umsched, "w")
        ap_24g_umsched_file.write(str(ap_24g_umsched_data))
        ap_24g_umsched_file.close()

        ap_24g_msched_data = ip_var_test.get_ap_24g_msched()
        ap_24g_msched = "{}-{}".format(file_date, "ap_24g_msched.txt")
        ap_24g_msched = report.file_add_path(ap_24g_msched)
        ap_24g_msched_file = open(ap_24g_msched, "w")
        ap_24g_msched_file.write(str(ap_24g_msched_data))
        ap_24g_msched_file.close()

    # ap scheduler results and write to a file
    if ap_ofdma_stats:
        print("getting ofdma ap data and writing to a file")
        file_date = report.get_date()

        ip_var_test.get_ap_ofdma_6g()
        ap_ofdma_6g = "{}-{}".format(file_date, "ap_ofdma_6g_data.txt")
        ap_ofdma_6g = report.file_add_path(ap_ofdma_6g)
        ap_ofdma_6g_data = open(ap_ofdma_6g, "w")
        ap_ofdma_6g_data.write(str(ap_ofdma_6g_data))
        ap_ofdma_6g_data.close()

        ip_var_test.get_ap_ofdma_5g()
        ap_ofdma_5g = "{}-{}".format(file_date, "ap_ofdma_5g_data.txt")
        ap_ofdma_5g = report.file_add_path(ap_ofdma_5g)
        ap_ofdma_5g_data = open(ap_ofdma_5g, "w")
        ap_ofdma_5g_data.write(str(ap_ofdma_5g_data))
        ap_ofdma_5g_data.close()

        ip_var_test.get_ap_ofdma_24g()
        ap_ofdma_24g = "{}-{}".format(file_date, "ap_ofdma_24g_data.txt")
        ap_ofdma_24g = report.file_add_path(ap_ofdma_24g)
        ap_ofdma_24g_data = open(ap_ofdma_24g, "w")
        ap_ofdma_24g_data.write(str(ap_ofdma_24g_data))
        ap_ofdma_24g_data.close()

    # for csv_file in csv_list:
    #    print("Ouptput reports CSV list value: {}".format(str(csv_file)))


if __name__ == "__main__":
    main()
