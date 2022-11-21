#!/usr/bin/env python3
"""
NAME: lf_snp_test.py  snp == Scaling and Performance

PURPOSE:

This program is to test an AP connected to a controller.
    The AP name is configurable.
    The controler with with a specific ap mode, wifi mode (2.4 Ghz or 5 Ghz),
     Bandwidth (20,40,80,160) and TX power.
    This currently only works with certain models of Cisco controllers.

The controller will configure the AP.
The Lanforge radios are configured for a specific client density, Packet type (TCP, UDP), Direction (download, upload) and Packet-size.
The transmission rate will be recorded and compared against the expected rate to determine pass or fail.
The results will be recorded in CSV file with the following data
AP, Band, wifi_mode, Bandwidth, encryption, ap mode, number of clients, packet type, direction, packet size, measured rx bytes, upload bits per second,
download bits per second.
unique test id, pass / fail, epoch time, and time.

TECHNICAL UNDERSTANDING:
    LANForge Monitored Values Per Polling Interval
        'rx bytes' - bytes transmitted
        'rx rate'  - bits per second

    in DL direction:    -B tx -> -A rx, (side_b_tx_min_bps) LANforge Eth endpoint transmits bytes (AP/DUT),
                        station endpoint (Wifi) LANForge receives them.  station-end-rx-bps (bits per second) is download rx-bps (bits per second)

    in UL direction:    -A tx -> -B rx, (side_a_tx_min_bps) LANforge Eth endpoint receives bytes (AP/DUT),
                        station endpoint (Wifi) LANForge transmits them.  ethernet-end-rx-bps (bits per second) is upload load rx-bps (bits per second)

    configured bps (side_a_tx_min_bps and side_b_tx_min_bps) if lists not same lenght shorter list padded out with 256000 if upload and download selected.

NOTES:
    1.  The controller_client_densities are indpendent of the number of stations on a radio
    2.  The --side_a_tx_min_bps (download) and --side_b_tx_min_bps (upload) is used to set the rate
        a. default 256000

The script is devided into parts:
1. Controller Class : CreateCtlr controller interface.
    Configurable by script:
        a. Band : a (5ghz) b (2.4ghz)
        b. wifi_mode : supported modes based on radio
        c. chan_5ghz and chan_24ghz
        d. BW: Band width 20 40 80 160,  160 only supports (2x2) spatial streams
        d. encryption : enable / disable, * encryption not supported
        e. ap_mode : local / flex connect, * ap mode not supported
        f. clients : number of clients set by controller_client_densities , radios much create associated number of stations Note: LANforge configuration
        g. packet_type: lf_udp  lf_tcp
        h. traffic direction: upload / download
        i. pdu: --side_a_min_pdu, --side_b_min_pdu Note: LANforge configuration

2. Traffic Generation Class : L3VariableTime
        a. Creates and brings up stations/clients on radios
        b. Measures connections
        c. reports results

3. Scaling And Performance Main
    a. Command parcing
    b. Fixed Configuration Coded Into The Script
    c. Script Controller Configurations
    d. Script LANforge Configurations
    e. Parameters Used For Testing
    f. report generation

OUTPUT:
    In /home/lanforge/report-data/<date>_Scaling_and_Performance or if not present in script directory under <date>_Scaling_and_Performance
    html results , default .html
    pdf results , default .pdf
    csv results_snp_<date>.csv  , results reflected in html and pdf files
    csv details_snp_<date>.csv raw data
    * radios and con

EXAMPLE:

Use --print_test_config at end of command to see test configuration

Test configurations take presidence to command line parameters

Using Coded Test Configuration --controller_test_1
    ./lf_snp_test.py --controller_ip 10.195.197.234 --controller_user admin --controller_passwd Milpitas@123
    --controller_aps 'Vanc-e' --controller_series "9800" --endp_types 'lf_udp' --upstream_port eth2 --controller_prompt "Can-SnP-9120" --controller_test_1
    --print_test_config

Using Coded Test Configuration --controller_test_1
    ./lf_snp_test.py --controller_ip 10.195.197.234 --controller_user admin --controller_passwd Milpitas@123
    --controller_aps 'Vanc-e' --controller_series "9800" --endp_types 'lf_udp' --upstream_port eth2 --controller_prompt "Can-SnP-9120" --controller_test_1
    --print_test_config

Using Coded Test Configuration:
    ./lf_snp_test.py -cc 192.168.100.112 -cu admin -cpw Cisco123 -cca APA453.0E7B.CF9C -cs "3504" --endp_types 'lf_udp' --upstream_port eth2 --controller_test_3
    --controller_prompt "(Cisco Controller)"
    --print_test_config

Using Commandline with defaults:
    ./lf_snp_test.py --controller_ip 192.168.100.112 --controller_user admin --controller_passwd Cisco123 --controller_aps APA453.0E7B.CF9C --controller_series "3504"
    --controller_prompt "(Cisco Controller)" --radio "radio==1.wiphy0 stations==1  ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto"
    --print_test_config

Using Commandline:
    ./lf_snp_test.py --controller_ip 192.168.100.112 --controller_user admin --controller_passwd Cisco123 --controller_aps APA453.0E7B.CF9C
    --controller_series "3504" --upstream_port eth2  --controller_prompt "(Cisco Controller)" --controller_wifimode "a" --controller_chan_5ghz "36"
    --radio "radio==1.wiphy0 stations==10  ssid==test_candela ssid_pw==[BLANK] security==open wifimode==ac" --controller_client_densities "10"
    --print_test_config

Using Commandline: Setting --test_duration "20s" --polling_interval to 5s -ccd "2" (--controller_client_densities)
    ./lf_snp_test.py --controller_ip 192.168.100.112 --controller_user admin --controller_passwd Cisco123 --controller_aps APA453.0E7B.CF9C
    --controller_series "3504" --upstream_port eth2  --controller_prompt "(Cisco Controller)" --controller_wifimode "auto"  --controller_chan_5ghz "36"
    --radio "radio==1.wiphy0 stations==2  ssid==test_candela ssid_pw==[BLANK] security==open wifimode==an" --controller_client_densities "2"
    --print_test_config

SAMPLE TEST CONFIG: --controller_test_1  output from --print_test_config option

2021-04-21 05:43:25,040 __main__ INFO: USING: controller_test_1
2021-04-21 05:43:25,040 __main__ INFO: TEST CONFIG:
2021-04-21 05:43:25,040 __main__ INFO: controller_aps ('-cca' ,'--controller_aps'): ['vanc-e']
2021-04-21 05:43:25,040 __main__ INFO: controller_bands ('-ccf' ,'--controller_bands'): ['a', 'b']
2021-04-21 05:43:25,040 __main__ INFO: controller_wifimodes ('-cwm' ,'--controller_wifimodes'): ['an', 'anAX', 'anAC', 'abgn', 'bg']
2021-04-21 05:43:25,040 __main__ INFO: controller_chan_5ghzs ('-cc5','--controller_chan_5ghzs'): ['36']
2021-04-21 05:43:25,040 __main__ INFO: controller_chan_24ghzs ('-cc2','--controller_chan_24ghzs'): ['1']
2021-04-21 05:43:25,040 __main__ INFO: controller_chan_widths ('-ccw','--controller_chan_widths'): ['20', '40', '80']
2021-04-21 05:43:25,040 __main__ INFO: controller_tx_powers ('-ctp','--controller_tx_powers'): ['3']
2021-04-21 05:43:25,041 __main__ INFO: controller_ap_modes ('-cam','--controller_ap_modes'): ['local']
2021-04-21 05:43:25,041 __main__ INFO: controller_client_densities ('-ccd','--controller_client_densities'): ['1', '10', '50', '200']
2021-04-21 05:43:25,041 __main__ INFO: controller_packet_types ('-t', '--endp_types'): ['lf_udp', 'lf_tcp']
2021-04-21 05:43:25,041 __main__ INFO: controller_pdus ('-cps','--controller_pdus'): ['88', '512', '1370', '1518']
2021-04-21 05:43:25,041 __main__ INFO: controller_directions ('-cd', '--controller_directions'): ['upload', 'download']
2021-04-21 05:43:25,041 __main__ INFO: controller_data_encryptions ('-cde','--controller_data_encryptions') ['disable']
2021-04-21 05:43:25,041 __main__ INFO: controller_side_a_tx_min_bps ('-amr','--side_a_tx_min_bps'): 256000
2021-04-21 05:43:25,041 __main__ INFO: controller_side_b_tx_min_bps ('-bmr','--side_b_tx_min_bps'): 256000
2021-04-21 05:43:25,041 __main__ INFO: test duration ('-d','--test_duration'): 20s
2021-04-21 05:43:25,041 __main__ INFO: polling_interval ('-pi','--polling_interval'): 5s
2021-04-21 05:43:25,041 __main__ INFO: radios from coded config used

INCLUDE_IN_README

COPYRIGHT:
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

"""
import sys
import os
import importlib
import itertools
from pprint import pprint
import argparse
import time
import datetime
import subprocess
import csv
import random
import logging

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

from lf_report import lf_report

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
# lf_graph = importlib.import_module("py-scripts.lf_graph")
# lf_bar_graph = lf_graph.lf_bar_graph

FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'


# see https://stackoverflow.com/a/13306095/11014343


class FileAdapter(object):
    def __init__(self, logger):
        self.logger = logger

    def write(self, data):
        # NOTE: data can be a partial line, multiple lines
        data = data.strip()  # ignore leading/trailing whitespace
        if data:  # non-blank
            self.logger.info(data)

    def flush(self):
        pass  # leave it to logging to flush properly


################################################################################
#
# Controller Class : CreateCtlr  controller interface
#
################################################################################
class CreateCtlr:
    def __init__(self,
                 _scheme,
                 _port,
                 _series,
                 _ctlr,
                 _prompt,
                 _user,
                 _passwd,
                 _ap,
                 _band,
                 _chan_5ghz,
                 _chan_24ghz,
                 _chan_width,
                 _ap_mode,
                 _tx_power,
                 _wlan,
                 _cap_ctl_out):

        self.scheme = _scheme
        self.port = _port
        self.series = _series
        self.ctlr = _ctlr
        self.prompt = _prompt
        self.user = _user
        self.passwd = _passwd
        self.ap = _ap
        self.band = _band
        self.chan_5ghz = _chan_5ghz
        self.chan_24ghz = _chan_24ghz
        self.chan_width = _chan_width
        self.ap_mode = _ap_mode
        self.tx_power = _tx_power
        self.wlan = _wlan
        self.cap_ctl_out = _cap_ctl_out
        self.client_density = 0

    # show summary (to get AP) (3400/9800)
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 --action summary --series 9800 --log stdout
    def controller_show_summary(self):
        pss = ""
        try:
            logg.info("\
                    scheme: {} \
                    ctlr: {} \
                    port: {} \
                    prompt: {} \
                    user: {}  \
                    passwd: {} \
                    AP: {} \
                    series: {} \
                    band: {} \
                    action: {}".format(
                self.scheme,
                self.ctlr,
                self.port,
                self.prompt,
                self.user,
                self.passwd,
                self.ap,
                self.series,
                self.band,
                "summary"))

            ctl_output = subprocess.run(["../wifi_ctl_9800_3504.py",
                                         "--scheme", self.scheme,
                                         "--prompt", self.prompt,
                                         "--port", self.port,
                                         "-d", self.ctlr,
                                         "-u", self.user,
                                         "-p", self.passwd,
                                         "-a", self.ap,
                                         "--series", self.series,
                                         "--band", self.band,
                                         "--action", "summary"],
                                        capture_output=self.cap_ctl_out,
                                        check=True)
            if self.cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)

        except subprocess.CalledProcessError as process_error:
            logg.info(
                "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                    process_error.returncode, process_error.output))
            time.sleep(1)
            exit(1)

        return pss

    # show ap dot11 5ghz summary (band defaults to 5ghz) --band a
    # show ap dot11 24ghz summary use --band b for 2.4 ghz
    # action advanced  (3400/9800)
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 --action advanced --series 9800 --log stdout
    def controller_show_ap_summary(self):
        pss = ""
        try:
            logg.info("\
                scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {}".format(
                self.scheme,
                self.ctlr, self.port, self.prompt, self.user,
                self.passwd, self.ap, self.series, self.band, "advanced"))

            ctl_output = subprocess.run(
                ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                 "-d", self.ctlr, "-u",
                 self.user, "-p", self.passwd,
                 "-a", self.ap, "--series", self.series, "--band", self.band, "--action", "advanced"],
                capture_output=True, check=True)

            pss = ctl_output.stdout.decode('utf-8', 'ignore')
            logg.info(pss)

        except subprocess.CalledProcessError as process_error:
            logg.info(
                "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                    process_error.returncode, process_error.output))
            time.sleep(1)
            exit(1)
        return pss

    # show wlan summary
    def controller_show_wlan_summary(self):
        try:
            logg.info(
                "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {}".format(
                    self.scheme,
                    self.ctlr, self.port, self.prompt, self.user,
                    self.passwd, self.ap, self.series, self.band, "show wlan summary"))

            ctl_output = subprocess.run(
                ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                 "-d", self.ctlr, "-u",
                 self.user, "-p", self.passwd,
                 "-a", self.ap, "--series", self.series, "--band", self.band, "--action", "show_wlan_summary"],
                capture_output=self.cap_ctl_out, check=True)

            if self.cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)

        except subprocess.CalledProcessError as process_error:
            logg.info(
                "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                    process_error.returncode, process_error.output))
            time.sleep(1)
            exit(1)

    # disable AP
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action disable --series 9800
    def controller_disable_ap(self):
        try:
            logg.info(
                "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {}".format(
                    self.scheme,
                    self.ctlr, self.port, self.prompt, self.user,
                    self.passwd, self.ap, self.series, self.band, "disable"))

            ctl_output = subprocess.run(
                ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                 "-d",
                 self.ctlr, "-u", self.user, "-p", self.passwd,
                 "-a", self.ap, "--series", self.series, "--band", self.band, "--action", "disable"],
                capture_output=self.cap_ctl_out, check=True)

            if self.cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)

        except subprocess.CalledProcessError as process_error:
            logg.info(
                "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                    process_error.returncode, process_error.output))
            time.sleep(1)
            exit(1)

    # disable wlan
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action disable_wlan --series 9800
    def controller_disable_wlan(self):
        try:
            logg.info(
                "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} wlan: {} action: {}".format(
                    self.scheme,
                    self.ctlr, self.port, self.prompt, self.user,
                    self.passwd, self.ap, self.series, self.band, self.wlan, "disable_wlan"))

            ctl_output = subprocess.run(
                ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                 "-d", self.ctlr, "-u",
                 self.user, "-p", self.passwd,
                 "-a", self.ap, "--series", self.series, "--band", self.band, "--wlan", self.wlan, "--action",
                 "disable_wlan"],
                capture_output=self.cap_ctl_out, check=True)

            if self.cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)

        except subprocess.CalledProcessError as process_error:
            logg.info(
                "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                    process_error.returncode, process_error.output))
            time.sleep(1)
            exit(1)

    # disable network 5ghz
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action disable_network_5ghz --series 9800
    def controller_disable_network_5ghz(self):
        if self.series == "9800":
            try:
                logg.info(
                    "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {}".format(
                        self.scheme,
                        self.ctlr, self.port, self.prompt, self.user,
                        self.passwd, self.ap, self.series, self.band, "disable_network_5ghz"))

                ctl_output = subprocess.run(
                    ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                     "-d", self.ctlr, "-u",
                     self.user, "-p", self.passwd,
                     "-a", self.ap, "--series", self.series, "--band", self.band, "--action", "disable_network_5ghz"],
                    capture_output=self.cap_ctl_out, check=True)

                if self.cap_ctl_out:
                    pss = ctl_output.stdout.decode('utf-8', 'ignore')
                    logg.info(pss)

            except subprocess.CalledProcessError as process_error:
                logg.info(
                    "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                        process_error.returncode, process_error.output))
                time.sleep(1)
                exit(1)
        else:
            try:
                logg.info(
                    "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {} value: {}".format(
                        self.scheme,
                        self.ctlr, self.port, self.prompt, self.user, self.passwd, self.ap, self.series,
                        self.band, "cmd", "config 802.11a disable network"))

                ctl_output = subprocess.run(
                    ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                     "-d", self.ctlr, "-u",
                     self.user, "-p", self.passwd,
                     "-a", self.ap, "--series", self.series, "--band", self.band, "--action", "cmd", "--value",
                     "config 802.11a disable network"],
                    capture_output=self.cap_ctl_out, check=True)

                if self.cap_ctl_out:
                    pss = ctl_output.stdout.decode('utf-8', 'ignore')
                    logg.info(pss)

            except subprocess.CalledProcessError as process_error:
                logg.info(
                    "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                        process_error.returncode, process_error.output))
                time.sleep(1)
                exit(1)

    # disable network 24ghz
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action disable_network_24ghz --series 9800
    def controller_disable_network_24ghz(self):
        if self.series == "9800":
            try:
                logg.info(
                    "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {}".format(
                        self.scheme,
                        self.ctlr, self.port, self.prompt, self.user,
                        self.passwd, self.ap, self.series, self.band, "disable_network_24ghz"))

                ctl_output = subprocess.run(
                    ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                     "-d", self.ctlr, "-u",
                     self.user, "-p", self.passwd,
                     "-a", self.ap, "--series", self.series, "--band", self.band, "--action", "disable_network_24ghz"],
                    capture_output=self.cap_ctl_out, check=True)

                if self.cap_ctl_out:
                    pss = ctl_output.stdout.decode('utf-8', 'ignore')
                    logg.info(pss)

            except subprocess.CalledProcessError as process_error:
                logg.info(
                    "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                        process_error.returncode, process_error.output))
                time.sleep(1)
                exit(1)
        else:
            try:
                logg.info(
                    "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {} value: {}".format(
                        self.scheme,
                        self.ctlr, self.port, self.prompt, self.user, self.passwd, self.ap, self.series,
                        self.band, "cmd", "config 802.11b disable network"))

                ctl_output = subprocess.run(
                    ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                     "-d", self.ctlr, "-u",
                     self.user, "-p", self.passwd,
                     "-a", self.ap, "--series", self.series, "--band", self.band, "--action", "cmd", "--value",
                     "config 802.11b disable network"],
                    capture_output=self.cap_ctl_out, check=True)

                if self.cap_ctl_out:
                    pss = ctl_output.stdout.decode('utf-8', 'ignore')
                    logg.info(pss)

            except subprocess.CalledProcessError as process_error:
                logg.info(
                    "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                        process_error.returncode, process_error.output))
                time.sleep(1)
                exit(1)

    # set manual mode - Series 9800 must be set to manual mode
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action manual --series 9800
    # ap name <AP NAME> dot11 5ghz radio role manual client-serving
    def controller_role_manual(self):
        if self.series == "9800":
            try:
                logg.info(
                    "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {}".format(
                        self.scheme,
                        self.ctlr, self.port, self.prompt, self.user,
                        self.passwd, self.ap, self.series, self.band, "manual"))

                ctl_output = subprocess.run(
                    ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                     "-d", self.ctlr, "-u",
                     self.user, "-p", self.passwd,
                     "-a", self.ap, "--series", self.series, "--band", self.band, "--action", "manual"],
                    capture_output=self.cap_ctl_out, check=True)

                if self.cap_ctl_out:
                    pss = ctl_output.stdout.decode('utf-8', 'ignore')
                    logg.info(pss)

            except subprocess.CalledProcessError as process_error:
                logg.info(
                    "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                        process_error.returncode, process_error.output))
                time.sleep(1)
                exit(1)
        else:
            logg.info(
                "Check the controller scheme used attemping 9800 series on 3504 controller: {}".format(self.scheme))

    # set manual mode - Series 9800 must be set to auto mode
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action auto --series 9800
    # ap name <AP NAME> dot11 5ghz radio role manual client-serving
    def controller_role_auto(self):
        if self.series == "9800":
            try:
                logg.info(
                    "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {}".format(
                        self.scheme,
                        self.ctlr, self.port, self.prompt, self.user,
                        self.passwd, self.ap, self.series, self.band, "auto"))

                ctl_output = subprocess.run(
                    ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                     "-d", self.ctlr, "-u",
                     self.user, "-p", self.passwd,
                     "-a", self.ap, "--series", self.series, "--band", self.band, "--action", "auto"],
                    capture_output=self.cap_ctl_out, check=True)

                if self.cap_ctl_out:
                    pss = ctl_output.stdout.decode('utf-8', 'ignore')
                    logg.info(pss)

            except subprocess.CalledProcessError as process_error:
                logg.info(
                    "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                        process_error.returncode, process_error.output))
                time.sleep(1)
                exit(1)
        else:
            logg.info(
                "Check the controller scheme used attemping 9800 series on 3504 controller: {}".format(self.scheme))

    # test parameters summary (txPower 1-8)
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action txPower  --value 5 --series 9800
    def controller_set_tx_power(self):
        try:
            logg.info(
                "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {} value {}".format(
                    self.scheme,
                    self.ctlr, self.port, self.prompt, self.user, self.passwd, self.ap, self.series,
                    self.band, "txPower", self.tx_power))  # TODO fix txPower to tx_power in wifi_ctl_9800_3504.py
            ctl_output = subprocess.run(
                ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                 "-d", self.ctlr, "-u",
                 self.user, "-p", self.passwd,
                 "-a", self.ap, "--series", self.series, "--band", self.band,
                 "--action", "txPower", "--value", self.tx_power],
                capture_output=self.cap_ctl_out, check=True)

            if self.cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)

        except subprocess.CalledProcessError as process_error:
            logg.info(
                "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                    process_error.returncode, process_error.output))
            time.sleep(1)
            exit(1)

    # set channel [36, 64, 100]
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action channel  --value 36 --series 9800
    # 9800 : ap name <AP> dot11 [5ghz | 24ghz] channel <channel>
    # 3504 : (controller Controller) >config 802.11a channel ap APA453.0E7B.CF9C  52
    def controller_set_channel(self):
        try:
            if self.band == "a":
                controller_channel = self.chan_5ghz
            else:
                controller_channel = self.chan_24ghz

            logg.info(
                "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {} value {}".format(
                    self.scheme,
                    self.ctlr, self.port, self.prompt, self.user, self.passwd, self.ap, self.series,
                    self.band, "channel", controller_channel))
            ctl_output = subprocess.run(
                ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                 "-d", self.ctlr, "-u",
                 self.user, "-p", self.passwd,
                 "-a", self.ap, "--series", self.series, "--band", self.band,
                 "--action", "channel", "--value", controller_channel],
                capture_output=self.cap_ctl_out, check=True)

            if self.cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)

        except subprocess.CalledProcessError as process_error:
            logg.info(
                "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                    process_error.returncode, process_error.output))
            time.sleep(1)
            exit(1)

    # set bandwidth [20 40 80 160]
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action bandwidth  --value 40 --series 9800
    def controller_set_bandwidth(self):
        try:
            logg.info(
                "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {} value {}".format(
                    self.scheme,
                    self.ctlr, self.port, self.prompt, self.user, self.passwd, self.ap, self.series,
                    self.band, "channel", self.chan_width))
            ctl_output = subprocess.run(
                ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                 "-d", self.ctlr, "-u",
                 self.user, "-p", self.passwd,
                 "-a", self.ap, "--series", self.series, "--band", self.band,
                 "--action", "channel", "--value", self.chan_width],
                capture_output=self.cap_ctl_out, check=True)

            if self.cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)

        except subprocess.CalledProcessError as process_error:
            logg.info(
                "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                    process_error.returncode, process_error.output))
            time.sleep(1)
            exit(1)

    # create wlan
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action create_wlan  --wlan "open-wlan"  --wlanID 1 --series 9800
    def controller_create_wlan(self):
        if self.series == "9800":
            try:
                logg.info(
                    "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {} wlan {} wlanID {} wlanSSID {}".format(
                        self.scheme,
                        self.ctlr, self.port, self.prompt, self.user, self.passwd, self.ap, self.series,
                        self.band, "create_wlan", self.wlan, self.wlanID, self.wlanSSID))
                ctl_output = subprocess.run(
                    ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                     "-d", self.ctlr, "-u",
                     self.user, "-p", self.passwd,
                     "-a", self.ap, "--series", self.series, "--band", self.band,
                     "--action", "create_wlan", "--wlan", self.wlan, "--wlanID", self.wlanID, "--wlanSSID",
                     self.wlanSSID],
                    capture_output=self.cap_ctl_out, check=True)

                if self.cap_ctl_out:
                    pss = ctl_output.stdout.decode('utf-8', 'ignore')
                    logg.info(pss)

            except subprocess.CalledProcessError as process_error:
                logg.info(
                    "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                        process_error.returncode, process_error.output))
                time.sleep(1)
                exit(1)
        else:
            logg.info(
                "Check the controller_scheme used attemping 9800 series on 3504 controller: {}".format(self.scheme))

    # create wireless tag policy  --9800 series needs to have wireless tag policy set
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action wireless_tag_policy --series 9800
    def controller_set_wireless_tag_policy(self):
        if self.series == "9800":
            try:
                logg.info(
                    "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {}".format(
                        self.scheme,
                        self.ctlr, self.port, self.prompt, self.user, self.passwd, self.ap, self.series,
                        self.band, "wireless_tag_policy"))
                ctl_output = subprocess.run(
                    ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                     "-d", self.ctlr, "-u",
                     self.user, "-p", self.passwd,
                     "-a", self.ap, "--series", self.series, "--band", self.band,
                     "--action", "wireless_tag_policy"],
                    capture_output=self.cap_ctl_out, check=True)

                if self.cap_ctl_out:
                    pss = ctl_output.stdout.decode('utf-8', 'ignore')
                    logg.info(pss)

            except subprocess.CalledProcessError as process_error:
                logg.info(
                    "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                        process_error.returncode, process_error.output))
                time.sleep(1)
                exit(1)
        else:
            logg.info(
                "Check the controller_scheme used attemping 9800 series on 3504 controller: {}".format(self.scheme))

    # enable wlan
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action enable_wlan --series 9800
    def controller_enable_wlan(self):
        try:
            logg.info(
                "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} wlan: {} action: {}".format(
                    self.scheme,
                    self.ctlr, self.port, self.prompt, self.user, self.passwd, self.ap, self.series,
                    self.band, self.wlan, "enable_wlan"))
            ctl_output = subprocess.run(
                ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                 "-d", self.ctlr, "-u",
                 self.user, "-p", self.passwd,
                 "-a", self.ap, "--series", self.series, "--band", self.band, "--wlan", self.wlan,
                 "--action", "enable_wlan"],
                capture_output=self.cap_ctl_out, check=True)

            if self.cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)

        except subprocess.CalledProcessError as process_error:
            logg.info(
                "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                    process_error.returncode, process_error.output))
            time.sleep(1)
            exit(1)

    # enable 5ghz
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action enable_network_5ghz --series 9800
    def controller_enable_network_5ghz(self):
        if self.series == "9800":
            try:
                logg.info(
                    "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {}".format(
                        self.scheme,
                        self.ctlr, self.port, self.prompt, self.user, self.passwd, self.ap, self.series,
                        self.band, "enable_network_5ghz"))
                ctl_output = subprocess.run(
                    ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                     "-d", self.ctlr, "-u",
                     self.user, "-p", self.passwd,
                     "-a", self.ap, "--series", self.series, "--band", self.band,
                     "--action", "enable_network_5ghz"],
                    capture_output=self.cap_ctl_out, check=True)

                if self.cap_ctl_out:
                    pss = ctl_output.stdout.decode('utf-8', 'ignore')
                    logg.info(pss)

            except subprocess.CalledProcessError as process_error:
                logg.info(
                    "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                        process_error.returncode, process_error.output))
                time.sleep(1)
                exit(1)
        else:
            try:
                logg.info(
                    "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {} value: {}".format(
                        self.scheme,
                        self.ctlr, self.port, self.prompt, self.user, self.passwd, self.ap, self.series,
                        self.band, "cmd", "config 802.11a enable network"))

                ctl_output = subprocess.run(
                    ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                     "-d", self.ctlr, "-u",
                     self.user, "-p", self.passwd,
                     "-a", self.ap, "--series", self.series, "--band", self.band, "--action", "cmd", "--value",
                     "config 802.11a enable network"],
                    capture_output=self.cap_ctl_out, check=True)

                if self.cap_ctl_out:
                    pss = ctl_output.stdout.decode('utf-8', 'ignore')
                    logg.info(pss)

            except subprocess.CalledProcessError as process_error:
                logg.info(
                    "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                        process_error.returncode, process_error.output))
                time.sleep(1)
                exit(1)

    # enable 24ghz
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action enable_network_24ghz --series 9800
    def controller_enable_network_24ghz(self):
        if self.series == "9800":
            try:
                logg.info(
                    "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {}".format(
                        self.scheme,
                        self.ctlr, self.port, self.prompt, self.user, self.passwd, self.ap, self.series,
                        self.band, "enable_network_24ghz"))
                ctl_output = subprocess.run(
                    ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                     "-d", self.ctlr, "-u",
                     self.user, "-p", self.passwd,
                     "-a", self.ap, "--series", self.series, "--band", self.band,
                     "--action", "enable_network_24ghz"],
                    capture_output=self.cap_ctl_out, check=True)

                if self.cap_ctl_out:
                    pss = ctl_output.stdout.decode('utf-8', 'ignore')
                    logg.info(pss)

            except subprocess.CalledProcessError as process_error:
                logg.info(
                    "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                        process_error.returncode, process_error.output))
                time.sleep(1)
                exit(1)
        else:
            try:
                logg.info(
                    "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {} value: {}".format(
                        self.scheme,
                        self.ctlr, self.port, self.prompt, self.user, self.passwd, self.ap, self.series,
                        self.band, "cmd", "config 802.11b enable network"))

                ctl_output = subprocess.run(
                    ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                     "-d", self.ctlr, "-u",
                     self.user, "-p", self.passwd,
                     "-a", self.ap, "--series", self.series, "--band", self.band, "--action", "cmd", "--value",
                     "config 802.11b enable network"],
                    capture_output=self.cap_ctl_out, check=True)

                if self.cap_ctl_out:
                    pss = ctl_output.stdout.decode('utf-8', 'ignore')
                    logg.info(pss)

            except subprocess.CalledProcessError as process_error:
                logg.info(
                    "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                        process_error.returncode, process_error.output))
                time.sleep(1)
                exit(1)

    # enable (band a)
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action enable --series 9800
    def controller_enable_ap(self):
        try:
            logg.info(
                "scheme: {} ctlr: {} port: {} prompt: {} user: {}  passwd: {} AP: {} series: {} band: {} action: {}".format(
                    self.scheme,
                    self.ctlr, self.port, self.prompt, self.user, self.passwd, self.ap, self.series,
                    self.band, "enable"))
            ctl_output = subprocess.run(
                ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port,
                 "-d", self.ctlr, "-u",
                 self.user, "-p", self.passwd,
                 "-a", self.ap, "--series", self.series, "--band", self.band,
                 "--action", "enable"],
                capture_output=self.cap_ctl_out, check=True)

            if self.cap_ctl_out:
                pss = ctl_output.stdout.decode('utf-8', 'ignore')
                logg.info(pss)

        except subprocess.CalledProcessError as process_error:
            logg.info(
                "Command Error, Controller unable to communicate to AP or unable to communicate to controller error code: {} output {}".format(
                    process_error.returncode, process_error.output))
            time.sleep(1)
            exit(1)

    # advanced (showes summary)
    # ./wifi_ctl_9800_3504.py --scheme ssh -d 172.19.36.168 -p <controller_pw> --port 23 -a "9120-Chamber-1" --band a --action advanced --series 9800
    def controller_show_ap_channel(self):
        advanced = subprocess.run(
            ["../wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--prompt", self.prompt, "--port", self.port, "-d",
             self.ctlr, "-u",
             self.user, "-p", self.passwd,
             "-a", self.ap, "--series", self.series, "--action", "ap_channel"], capture_output=True)

        pss = advanced.stdout.decode('utf-8', 'ignore')
        logg.info(pss)

        if self.series == "9800":
            if self.band == "a":
                controller_channel = self.chan_5ghz
            else:
                controller_channel = self.chan_24ghz

            for line in pss.splitlines():
                search_str = self.ap
                logg.info("line {}".format(line))
                element_list = line.lstrip().split()
                logg.info("element_list {}".format(element_list))
                if line.lstrip().startswith(search_str):
                    logg.info("line {}".format(line))
                    element_list = line.lstrip().split()
                    logg.info("element_list {}".format(element_list))
                    # AP Name (0) mac (1) slot (2) Admin State [enable/disable] (3) Oper State [Up/Down] (4) Width (5) Txpwr (6,7) channel (8) mode (9)
                    logg.info("ap: {} slof {} channel {}  chan_width {}".format(element_list[0], element_list[2],
                                                                                element_list[8], element_list[5]))
                    if (str(controller_channel) in str(element_list[8])) and (
                            str(self.chan_width) in str(element_list[5])):
                        logg.info(
                            "ap {} configuration successful: channel {} in expected {}  chan_width {} in expected {}".format(
                                element_list[0],
                                controller_channel,
                                element_list[8],
                                self.chan_width,
                                element_list[5]))
                    else:
                        logg.info("WARNING ap {} configuration: channel {} in expected {}  chan_width {} in expected {}"
                                  .format(element_list[0], controller_channel, element_list[8], self.chan_width,
                                          element_list[5]))
                    break
        else:
            logg.info("checking for 802.11{}".format(self.band))
            if self.band == "a":
                controller_channel = self.chan_5ghz
            else:
                controller_channel = self.chan_24ghz

            for line in pss.splitlines():
                # logg.info("line {}".format(line))
                search_str = "802.11{}".format(self.band)
                if line.lstrip().startswith(search_str):
                    logg.info("line {}".format(line))
                    element_list = line.lstrip().split()
                    logg.info("element_list {}".format(element_list))
                    logg.info("ap: {} channel {}  chan_width {}".format(self.ap, element_list[4], element_list[5]))
                    if (str(controller_channel) in str(element_list[4])) and (
                            str(self.chan_width) in str(element_list[5])):
                        logg.info("ap configuration successful: channel {} in expected {}  chan_width {} in expected {}"
                                  .format(controller_channel, element_list[4], self.chan_width, element_list[5]))
                    else:
                        logg.info("AP WARNING: channel {} expected {}  chan_width {} expected {}"
                                  .format(element_list[4], controller_channel, element_list[5], self.chan_width))
                    break

        logg.info("configure ap {} channel {} chan_width {}".format(self.ap, self.channel, self.chan_width))
        # Verify channel and channel width. 


################################################################################
#
# End of Controller Class : controller interface
#
################################################################################

################################################################################
#
# Traffic Generation Class : L3VariableTime
#
################################################################################
class L3VariableTime(Realm):
    def __init__(self,
                 args,
                 _scheme,
                 _port,
                 _series,
                 _ctlr,
                 _prompt,
                 _user,
                 _passwd,
                 _ap,
                 _ap_slot,
                 _band,
                 _chan_5ghz,
                 _chan_24ghz,
                 _chan_width,
                 _ap_mode,
                 _tx_power,
                 _client_density,
                 _cap_ctl_out,
                 _ap_dict,
                 endp_type,
                 tos,
                 side_b,
                 radio_name_list,
                 number_of_stations_per_radio_list,
                 ssid_list,
                 ssid_password_list,
                 ssid_security_list,
                 wifimode_list,
                 station_lists,
                 name_prefix,
                 debug_on,
                 outfile,
                 results,
                 test_keys,
                 test_config,
                 reset_port_enable_list,
                 reset_port_time_min_list,
                 reset_port_time_max_list,
                 csv_started=False,
                 side_a_tx_min_bps=560000,
                 side_a_tx_max_bps=0,  # setting to 0 will match min
                 side_a_min_pdu=1518,
                 side_a_max_pdu=0,
                 side_b_tx_min_bps=560000,
                 side_b_tx_max_bps=0,  # setting to 0 will match min
                 side_b_min_pdu=1518,
                 side_b_max_pdu=0,
                 number_template="00",
                 test_duration="256s",
                 polling_interval="60s",
                 lfclient_host="localhost",
                 lfclient_port=8080,
                 debug=False,
                 wait_timeout=120,
                 _exit_on_error=False,
                 _exit_on_fail=False,
                 _proxy_str=None,
                 _capture_signal_list=None):
        super().__init__(lfclient_host=lfclient_host,
                         lfclient_port=lfclient_port,
                         debug_=debug,
                         _exit_on_error=_exit_on_error,
                         _exit_on_fail=_exit_on_fail,
                         _proxy_str=_proxy_str,
                         _capture_signal_list=_capture_signal_list)
        if _capture_signal_list is None:
            _capture_signal_list = []
        self.scheme = _scheme
        self.port = _port
        self.series = _series
        self.ctlr = _ctlr
        self.prompt = _prompt
        self.user = _user
        self.passwd = _passwd
        self.ap = _ap
        self.ap_slot = _ap_slot
        self.band = _band
        self.chan_5ghz = _chan_5ghz
        self.chan_24ghz = _chan_24ghz
        self.chan_width = _chan_width
        self.ap_mode = _ap_mode
        self.tx_power = _tx_power
        self.cap_ctl_out = _cap_ctl_out
        self.ap_dict = _ap_dict
        self.client_density = _client_density
        self.tos = tos.split()
        self.endp_type = endp_type
        self.side_b = side_b
        self.ssid_list = ssid_list
        self.ssid_password_list = ssid_password_list
        self.station_lists = station_lists
        self.ssid_security_list = ssid_security_list
        self.wifimode_list = wifimode_list
        self.reset_port_enable_list = reset_port_enable_list
        self.reset_port_time_min_list = reset_port_time_min_list
        self.reset_port_time_max_list = reset_port_time_max_list
        self.number_template = number_template
        self.name_prefix = name_prefix
        self.test_duration = test_duration
        self.radio_name_list = radio_name_list
        self.number_of_stations_per_radio_list = number_of_stations_per_radio_list
        # self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port, debug_=debug_on)
        self.polling_interval_seconds = self.duration_time_to_seconds(polling_interval)
        self.cx_profile = self.new_l3_cx_profile()
        self.multicast_profile = self.new_multicast_profile()
        self.multicast_profile.name_prefix = "MLT-"
        self.station_profiles = []
        self.args = args
        self.outfile = outfile
        self.results = results
        self.csv_started = csv_started

        self.side_a_tx_min_bps = side_a_tx_min_bps
        self.side_a_tx_max_bps = side_a_tx_max_bps
        self.side_a_min_pdu = side_a_min_pdu
        self.side_a_max_pdu = side_a_max_pdu

        self.side_b_tx_min_bps = side_b_tx_min_bps
        self.side_b_tx_max_bps = side_b_tx_max_bps
        self.side_b_min_pdu = side_b_min_pdu
        self.side_b_max_pdu = side_b_max_pdu

        self.epoch_time = int(time.time())
        self.debug = debug_on
        self.wait_timeout = wait_timeout
        self.test_keys = test_keys
        self.test_config = test_config

        self.test_config_dict = dict(map(lambda x: x.split('=='),
                                         str(self.test_config).replace('[', '').replace(']', '').replace("'",
                                                                                                         "").split()))

        # Full spread-sheet data
        if self.outfile is not None:
            self.csv_file_details = open(self.outfile, "a+")
            self.csv_writer = csv.writer(self.csv_file_details, delimiter=",")

        if self.results is not None:
            self.csv_results = open(self.results, "a+")
            self.csv_results_writer = csv.writer(self.csv_results, delimiter=",")

        for (radio_, ssid_, ssid_password_, ssid_security_, wifimode_,
             reset_port_enable_, reset_port_time_min_, reset_port_time_max_) \
                in zip(radio_name_list, ssid_list, ssid_password_list, ssid_security_list, wifimode_list,
                       reset_port_enable_list, reset_port_time_min_list, reset_port_time_max_list):
            self.station_profile = self.new_station_profile()
            self.station_profile.lfclient_url = self.lfclient_url
            self.station_profile.ssid = ssid_
            self.station_profile.ssid_pass = ssid_password_
            self.station_profile.security = ssid_security_
            self.station_profile.mode = wifimode_
            self.station_profile.number_template = self.number_template
            self.station_profile.mode = wifimode_
            self.station_profile.set_reset_extra(reset_port_enable=reset_port_enable_,
                                                 test_duration=self.duration_time_to_seconds(self.test_duration),
                                                 reset_port_min_time=self.duration_time_to_seconds(
                                                     reset_port_time_min_),
                                                 reset_port_max_time=self.duration_time_to_seconds(
                                                     reset_port_time_max_))
            self.station_profiles.append(self.station_profile)

        self.multicast_profile.host = self.lfclient_host
        self.cx_profile.host = self.lfclient_host
        self.cx_profile.port = self.lfclient_port
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = self.side_a_tx_min_bps  # Note: side_a_tx_min_bps is side_a_min_bps in py-json profiles
        self.cx_profile.side_a_max_bps = self.side_a_tx_min_bps
        self.cx_profile.side_a_min_pdu = self.side_a_min_pdu
        self.cx_profile.side_a_max_pdu = self.side_a_max_pdu
        self.cx_profile.side_b_min_bps = self.side_b_tx_min_bps  # Note: side_b_tx_min_bps is side_b_min_bps in py-json profiles
        self.cx_profile.side_b_max_bps = self.side_b_tx_min_bps
        self.cx_profile.side_b_min_pdu = self.side_b_min_pdu
        self.cx_profile.side_b_max_pdu = self.side_b_max_pdu

    def __get_rx_values(self):
        endp_list = self.json_get("endp?fields=name,eid,delay,jitter,rx+rate,rx+bytes,rx+drop+%25", debug_=False)
        endp_rx_drop_map = {}
        endp_rx_map = {}
        our_endps = {}

        endps = []
        # total upload in bits per second across all stations
        total_ul = 0
        total_dl = 0

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
                            if value_name == 'rx drop %':
                                endp_rx_drop_map[item] = value
                            if value_name == 'rx rate':
                                # This hack breaks for mcast or if someone names endpoints weirdly.
                                # print("item: ", item, " rx-bps: ", value_rx_bps)
                                if item.endswith("-A"):
                                    total_dl += int(value)
                                else:
                                    total_ul += int(value)

        # print("total-dl: ", total_dl, " total-ul: ", total_ul, "\n")
        return endp_rx_map, endp_rx_drop_map, endps, total_dl, total_ul

    def time_stamp(self):
        return time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(self.epoch_time))

    def __compare_vals(self, old_list, new_list, total_dl_bps, total_ul_bps):
        passes = 0
        expected_passes = 0
        csv_rx_headers = []
        csv_rx_row_data = []
        csv_result_row_data = []
        csv_rx_delta_row_data = []
        csv_rx_delta_dict = {}
        test_id = ""

        for key in [key for key in old_list if "mtx" in key]:
            del old_list[key]
        for key in [key for key in new_list if "mtx" in key]:
            del new_list[key]

        filtered_values = [v for _, v in new_list.items() if v != 0]
        # Evaluate upload or download
        new_evaluate_list = new_list.copy()
        print("new_evaluate_list before", new_evaluate_list)
        # look at ul and dl
        old_evaluate_list = old_list.copy()

        if len(old_evaluate_list) == len(new_evaluate_list):
            for item, value in old_evaluate_list.items():
                # check only upload or download - expected passes corresponds to traffic only in observed direction
                if "upload" in self.test_config_dict.values() and item.endswith("-B") \
                        or "download" in self.test_config_dict.values() and item.endswith("-A"):
                    expected_passes += 1
                print("ITEM: {} VALUE: {}".format(item, value))
                if new_evaluate_list[item] > old_evaluate_list[item]:
                    passes += 1
                    # if self.debug: logg.info(item, new_evaluate_list[item], old_evaluate_list[item], " Difference: ", new_evaluate_list[item] - old_evaluate_list[item])
                    print(item, new_evaluate_list[item], old_evaluate_list[item], " Difference: ",
                          new_evaluate_list[item] - old_evaluate_list[item])
                else:
                    if "upload" in self.test_config_dict.values() and item.endswith("-B") \
                            or "download" in self.test_config_dict.values() and item.endswith("-A"):
                        # only a failure if expecting traffic in that direction
                        print("Failed to increase rx bytes: ", item, new_evaluate_list[item], old_evaluate_list[item])
                if not self.csv_started:
                    # stations that end in -A are dl (download, download), stations that end in -B are ul (upload, upload)
                    if item.endswith("-A"):
                        csv_rx_headers.append(item + '-dl-rx-bytes')
                    else:
                        csv_rx_headers.append(item + '-ul-rx-bytes')
                csv_rx_delta_dict.update({item: (new_evaluate_list[item] - old_evaluate_list[item])})

            if not self.csv_started:
                csv_header = self.csv_generate_column_details_headers()
                csv_header += csv_rx_headers
                logg.info(csv_header)
                self.csv_add_column_headers(csv_header)
                csv_results = self.csv_generate_column_results_headers()
                # csv_results += csv_rx_headers
                self.csv_add_column_headers_results(csv_results)
                self.csv_started = True

            # need to generate list of all the values
            filtered_values = [v for _, v in csv_rx_delta_dict.items() if v != 0]
            # if need the average use average_rx_delta
            # average_rx_delta= sum(filtered_values) / len(filtered_values) if len(filtered_values) != 0 else 0

            # write out the configuraiton for the test
            for key in self.test_keys:
                csv_rx_row_data.append(self.test_config_dict[key])
                csv_result_row_data.append(self.test_config_dict[key])
                csv_rx_delta_row_data.append(self.test_config_dict[key])

            csv_rx_row_data.extend([self.epoch_time, self.time_stamp()])
            csv_result_row_data.extend([self.epoch_time, self.time_stamp()])

            # Generate TestID
            for key in self.test_keys:
                test_id = test_id + "_" + self.test_config_dict[key]

            print("test_id: {}".format(test_id))
            csv_rx_row_data.append(test_id)
            csv_result_row_data.append(test_id)

            csv_rx_row_data.append(self.test_duration)
            csv_rx_row_data.append(self.polling_interval_seconds)

            csv_rx_row_data.append(self.side_a_tx_min_bps)
            csv_rx_row_data.append(self.side_b_tx_min_bps)

            # Recorde the Total Transmit rate for all stations
            rx_bytes = sum(filtered_values)  # total
            csv_rx_row_data.append(rx_bytes)

            # The total_dl_bps and total_up_bps is for the interval
            csv_rx_row_data.append(total_dl_bps)
            csv_rx_row_data.append(total_ul_bps)
            # csv_result_row_data.append(rx_bytes)

            print("csv_rx_row_data {}".format(csv_rx_row_data))
            # TODO:  may want to pass in the information that needs to be in the csv file into the class

            for item, value in old_evaluate_list.items():
                expected_passes += 1
                if new_evaluate_list[item] > old_evaluate_list[item]:
                    passes += 1
                    print(item, new_evaluate_list[item], old_evaluate_list[item], " Difference: ",
                          new_evaluate_list[item] - old_evaluate_list[item])
                else:
                    print("Failed to increase rx data: ", item, new_evaluate_list[item], old_evaluate_list[item])
                if not self.csv_started:
                    csv_rx_headers.append(item)
                # append the rate for each station
                csv_rx_row_data.append(new_list[item] - old_list[item])

            # data from each station for each iteration
            self.csv_add_row(csv_rx_row_data, self.csv_writer, self.csv_file_details)

            if passes == expected_passes:
                return True, rx_bytes, csv_result_row_data
            else:
                return False, rx_bytes, csv_result_row_data
        else:
            print("Old-list length: %i  new: %i does not match in compare-vals." % (len(old_list), len(new_list)))
            print("old-list:", old_list)
            print("new-list:", new_list)
            return False, None, None

    def reset_port_check(self):
        for station_profile in self.station_profiles:
            if station_profile.reset_port_extra_data['reset_port_enable']:
                if not station_profile.reset_port_extra_data['reset_port_timer_started']:
                    logg.info(
                        "reset_port_time_min: {}".format(station_profile.reset_port_extra_data['reset_port_time_min']))
                    logg.info(
                        "reset_port_time_max: {}".format(station_profile.reset_port_extra_data['reset_port_time_max']))
                    station_profile.reset_port_extra_data['seconds_till_reset'] = \
                        random.randint(station_profile.reset_port_extra_data['reset_port_time_min'],
                                       station_profile.reset_port_extra_data['reset_port_time_max'])
                    station_profile.reset_port_extra_data['reset_port_timer_started'] = True
                    logg.info("on radio {} seconds_till_reset {}".format(station_profile.add_sta_data['radio'],
                                                                         station_profile.reset_port_extra_data[
                                                                             'seconds_till_reset']))
                else:
                    station_profile.reset_port_extra_data['seconds_till_reset'] = station_profile.reset_port_extra_data[
                                                                                      'seconds_till_reset'] - 1
                    if self.debug:
                        logg.info(
                            "radio: {} countdown seconds_till_reset {}".format(station_profile.add_sta_data['radio'],
                                                                               station_profile.reset_port_extra_data[
                                                                                   'seconds_till_reset']))
                    if station_profile.reset_port_extra_data['seconds_till_reset'] <= 0:
                        station_profile.reset_port_extra_data['reset_port_timer_started'] = False
                        port_to_reset = random.randint(0, len(station_profile.station_names) - 1)
                        logg.info("reset on radio {} station: {}".format(station_profile.add_sta_data['radio'],
                                                                         station_profile.station_names[port_to_reset]))
                        self.reset_port(station_profile.station_names[port_to_reset])

    def pre_cleanup(self):
        self.cx_profile.cleanup_prefix()
        self.multicast_profile.cleanup_prefix()
        self.total_stas = 0
        for station_list in self.station_lists:
            for sta in station_list:
                self.rm_port(sta, check_exists=True)
                self.total_stas += 1

        # Verify Stations are Gone
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

    def build(self):
        index = 0
        for station_profile in self.station_profiles:
            station_profile.use_security(station_profile.security, station_profile.ssid, station_profile.ssid_pass)
            station_profile.set_number_template(station_profile.number_template)
            logg.info("Creating stations")

            station_profile.create(radio=self.radio_name_list[index], sta_names_=self.station_lists[index],
                                   debug=self.debug, sleep_time=0)
            index += 1

            for _tos in self.tos:
                logg.info(
                    "Creating connections for endpoint type: {} TOS: {} stations_names {}".format(self.endp_type, _tos,
                                                                                                  station_profile.station_names))
                self.cx_profile.create(endp_type=self.endp_type, side_a=station_profile.station_names,
                                       side_b=self.side_b, sleep_time=0, tos=_tos)
        self._pass("PASS: Stations build finished")

    def start(self, print_pass=False, print_fail=False):
        best_rx_bytes = 0
        rx_bytes = 0
        csv_rx_row_data = " "
        Result = False
        logg.info("Bringing up stations")
        self.admin_up(self.side_b)
        for station_profile in self.station_profiles:
            for sta in station_profile.station_names:
                logg.info("Bringing up station %s" % sta)
                self.admin_up(sta)

        temp_stations_list = []
        temp_stations_list.append(self.side_b)
        for station_profile in self.station_profiles:
            temp_stations_list.extend(station_profile.station_names.copy())
        if self.wait_for_ip(temp_stations_list, timeout_sec=self.wait_timeout, debug=self.debug):
            logg.info("ip's acquired")
        else:
            logg.info("Stations Failed to get IP's , consider increasing -wto','--wait_timeout' from the command line ")
            exit(1)  # Exit if cannot receive IP's
        time.sleep(30)
        logg.info("Starting layer-3 traffic (if any configured)")
        self.cx_profile.start_cx()
        self.cx_profile.refresh_cx()

        cur_time = datetime.datetime.now()
        logg.info("Getting initial values.")
        # the total_dl_bps and total_up_bps is for all stations 
        old_rx_values, rx_drop_percent, endps, total_dl_bps, total_ul_bps = self.__get_rx_values()

        end_time = self.parse_time(self.test_duration) + cur_time

        logg.info("Monitoring throughput for duration: %s" % self.test_duration)

        passes = 0
        expected_passes = 0
        logg.info("polling_interval_seconds {}".format(self.polling_interval_seconds))

        while cur_time < end_time:
            interval_time = cur_time + datetime.timedelta(seconds=self.polling_interval_seconds)
            while cur_time < interval_time:
                cur_time = datetime.datetime.now()
                self.reset_port_check()
                time.sleep(1)

            self.epoch_time = int(time.time())
            # the total_dl_bps and total_up_bps is for all stations 
            new_rx_values, rx_drop_percent, endps, total_dl_bps, total_ul_bps = self.__get_rx_values()

            print("main loop, total-dl: ", total_dl_bps, " total-ul: ", total_ul_bps)

            expected_passes += 1

            # __compare_vals - does the calculations
            Result, rx_bytes, csv_rx_row_data = self.__compare_vals(old_rx_values, new_rx_values, total_dl_bps,
                                                                    total_ul_bps)
            # save the best rate for the interval 
            if rx_bytes > best_rx_bytes:
                best_rx_bytes = rx_bytes

            if Result:
                passes += 1
            else:
                fail_msg = "FAIL: TIME: {} EPOCH: {} Not all stations increased traffic".format(cur_time,
                                                                                                self.epoch_time)
                self._fail(fail_msg, print_fail)
            old_rx_values = new_rx_values

            cur_time = datetime.datetime.now()
        csv_rx_row_data.append(self.test_duration)
        csv_rx_row_data.append(self.polling_interval_seconds)
        csv_rx_row_data.append(self.side_a_tx_min_bps)
        csv_rx_row_data.append(self.side_b_tx_min_bps)
        csv_rx_row_data.append(best_rx_bytes)
        csv_rx_row_data.append(total_dl_bps)
        csv_rx_row_data.append(total_ul_bps)
        self.csv_add_row(csv_rx_row_data, self.csv_results_writer, self.csv_results)
        if passes == expected_passes:
            self._pass("PASS: All tests passed", print_pass)

    def stop(self):
        self.cx_profile.stop_cx()
        self.multicast_profile.stop_mc()
        for station_list in self.station_lists:
            for station_name in station_list:
                self.admin_down(station_name)

    def cleanup(self):
        self.cx_profile.cleanup()
        self.multicast_profile.cleanup()
        for station_profile in self.station_profiles:
            station_profile.cleanup()

    # for details csv file                                    
    def csv_generate_column_details_headers(self):
        # test_keys used to generate the test_id
        csv_rx_headers = self.test_keys.copy()
        # test_keys are the controller configuration
        csv_rx_headers.extend(
            ['epoch_time', 'time', 'test_id', 'test_duration', 'intv_sec', 'A_to_B_tx_bps_ul', 'B_to_A_tx_bps_dl',
             'rx_bytes_intv_best', 'all_sta_dl_bps', 'all_sta_ul_bps'])
        return csv_rx_headers

    def csv_generate_column_results_headers(self):
        # test_keys used to generate test_id
        csv_rx_headers = self.test_keys.copy()
        # test_keys are the controller configuration
        csv_rx_headers.extend(
            ['epoch_time', 'time', 'test_id', 'test_duration', 'intv_sec', 'A_to_B_tx_bps_ul', 'B_to_A_tx_bps_dl',
             'rx_bytes_intv_best', 'all_sta_dl_bps', 'all_sta_ul_bps'])
        return csv_rx_headers

    def csv_add_column_headers(self, headers):
        if self.csv_file_details is not None:
            self.csv_writer.writerow(headers)
            self.csv_file_details.flush()

    def csv_add_column_headers_results(self, headers):
        if self.csv_results is not None:
            self.csv_results_writer.writerow(headers)
            self.csv_results.flush()

    @staticmethod
    def csv_validate_list(csv_list, length):
        if len(csv_list) < length:
            csv_list = csv_list + [('no data', 'no data')] * (length - len(csv_list))
        return csv_list

    @staticmethod
    def csv_add_row(row, writer, csv_file_details):  # can make two calls eventually
        if csv_file_details is not None:
            writer.writerow(row)
            csv_file_details.flush()


def valid_endp_types(_endp_type):
    etypes = _endp_type.split()
    for endp_type in etypes:
        valid_endp_type = ['lf_udp', 'lf_udp6', 'lf_tcp', 'lf_tcp6', 'mc_udp', 'mc_udp6']
        if not (str(endp_type) in valid_endp_type):
            print('invalid endp_type: %s. Valid types lf_udp, lf_udp6, lf_tcp, lf_tcp6, mc_udp, mc_udp6' % endp_type)
            exit(1)
    return _endp_type


################################################################################
#
# End of Traffic Generation Class
#
################################################################################

############################################################
#
#  Scaling And Performance MAIN
#
############################################################
def main():
    global logg
    lfjson_port = 8080
    debug_on = False

    parser = argparse.ArgumentParser(
        prog='lf_controller_snp.py',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            Scaling and Performance
            ''',

        description='''\
lf_controller_snp.py:
--------------------

##################################################################################
Task Description:  Ultimate Aim
##################################################################################
-----------------
Candela Scaling and Performance Test (SNP) 

The Test supports configuraiton of a Controller which configures
An AP and the Configuration of LANforge or Multiple LANforges
configured into a "Realm". 

#########################################
# Examples
# #######################################            
EXAMPLE: 

Use --print_test_config at end of command to see test configuration

Test configurations take presidence to command line parameters

Using Coded Test Configuration --controller_test_1
    ./lf_snp_test.py --controller_ip 10.195.197.234 --controller_user admin --controller_passwd Milpitas@123  
    --controller_aps 'Vanc-e' --controller_series "9800" --endp_types 'lf_udp' --upstream_port eth2 --controller_prompt "Can-SnP-9120" --controller_test_1
    --print_test_config

Using Coded Test Configuration --controller_test_1
    ./lf_snp_test.py --controller_ip 10.195.197.234 --controller_user admin --controller_passwd Milpitas@123  
    --controller_aps 'Vanc-e' --controller_series "9800" --endp_types 'lf_udp' --upstream_port eth2 --controller_prompt "Can-SnP-9120" --controller_test_1
    --print_test_config

Using Coded Test Configuration:
    ./lf_snp_test.py -cc 192.168.100.112 -cu admin -cpw Cisco123 -cca APA453.0E7B.CF9C -cs "3504" --endp_types 'lf_udp' --upstream_port eth2 --controller_test_3 
    --controller_prompt "(Cisco Controller)" 
    --print_test_config

Using Commandline with defaults:
    ./lf_snp_test.py --controller_ip 192.168.100.112 --controller_user admin --controller_passwd Cisco123 --controller_aps APA453.0E7B.CF9C --controller_series "3504" 
    --controller_prompt "(Cisco Controller)" --radio "radio==1.wiphy0 stations==1  ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto" 
    --print_test_config

Using Commandline:
    ./lf_snp_test.py --controller_ip 192.168.100.112 --controller_user admin --controller_passwd Cisco123 --controller_aps APA453.0E7B.CF9C 
    --controller_series "3504" --upstream_port eth2  --controller_prompt "(Cisco Controller)" --controller_wifimode "a" --controller_chan_5ghz "36" 
    --radio "radio==1.wiphy0 stations==10  ssid==test_candela ssid_pw==[BLANK] security==open wifimode==ac" --controller_client_densities "10"  
    --print_test_config

Using Commandline: Setting --test_duration "20s" --polling_interval to 5s -ccd "2" (--controller_client_densities)
    ./lf_snp_test.py --controller_ip 192.168.100.112 --controller_user admin --controller_passwd Cisco123 --controller_aps APA453.0E7B.CF9C 
    --controller_series "3504" --upstream_port eth2  --controller_prompt "(Cisco Controller)" --controller_wifimode "auto"  --controller_chan_5ghz "36" 
    --radio "radio==1.wiphy0 stations==2  ssid==test_candela ssid_pw==[BLANK] security==open wifimode==an" --controller_client_densities "2"  
    --print_test_config

#############################################
#############################################
LANforge Information and General Information
#############################################
#############################################

#############################################
Radios Description
#############################################

Radio descriptions:
ax200: so if AP is /n, then ax200 will connect at /n.  But if AP is /AX, we have no way to force ax200 to act like /n
ax200: is dual band, supporting at least /b/g/n/AX on 2.4Ghz, and /a/n/ac/AX on 5Ghz.  2.4Ghz doesn't officially support /AC, but often chips will do /AC there anyway

ath10K: if they want /AC or /n or /abg stations, then our ath10k radios can support that need (and ath9k if they have any, can do /n and /abg)
ath10K(998x)  - wave -1 , dual band card it can be ac, n , a/b/g modes, up to 3x3 spacial streams
ath10K(9884) - wave-2 supports 4x4  802.11an-AC  5ghz  (can act as ac , an)

Note: wave-2 radios can act as ac, an, (802.11an-AC) or legacy a/b/g (802.11bgn-AC)

#############################################
Wifi Modes 
#############################################
11ax (2.4 ghz or 5 ghz), 11ac (5 ghz only), 11n (2.4ghz or 5 ghz), 11bg (2.4 ghz)  (controller)

#############################################
5 Ghz Radios and Wifi Modes
#############################################
Wifi mode: 11ax  - 5ghz
Radios   :  ax200  :        802.11 /a/n/ac/AX

Wifi mode: 11ac - 5ghz
Radios   :  ath10K(9984)    802.11an-AC (9984 are single band)

Wifi mode: 11n - 5ghz
Radios   :  ath10K(9984)    802.11an-AC (9984 are single band)

#############################################
24 Ghz Radios and Wifi Modes
#############################################
Wifi mode: 11ax - 24ghz
Radios   :  ax200 -         802.11 /b/g/n/AX     

Wifi mode: 11ac - 24ghz
Radios   :  ax200           802.11 /b/g/n/AX (2.4Ghz doesn't officially support /AC, but often chips will do /AC there anyway) (invalid)

Wifi mode: 11n - 24ghz 
Radios   :  ax200           802.11 /b/g/n/AX

Wifi mode: 11bg - 24ghz
Radios   :  ax200           802.11 /b/g/n/AX

############################################
Radio Mode Configuration
############################################
controller_wifimode == "anAX" or controller_wifimode == "abgn" or controller_wifimode == "bg":
        radios = radio_AX200_abgn_ax_dict[controller_client_density]
                                                
controller_wifimode == "an" or controller_wifimode == "anAC":
        radios = radio_ath10K_9984_an_AC_dict[controller_client_density]

############################################
LANforge Realm Configuration
############################################

1.wiphy0  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
1.wiphy1  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
1.wiphy2  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
1.wiphy3  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
1.wiphy4  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
1.wiphy5  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
1.wiphy6  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
1.wiphy7  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
1.wiphy8  802.11an-AC    ath10k(9984)    523 - 64 stations - 5ghz 
1.wiphy9  802.11an-AC    ath10k(9984)    523 - 64 stations - 5ghz

2.wiphy0  802.11abgn-ax  iwlwifi(AX200)  521 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
2.wiphy1  802.11abgn-ax  iwlwifi(AX200)  521 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn 

3.wiphy0  802.11abgn-ax  iwlwifi(AX200)  521 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
3.wiphy1  802.11abgn-ax  iwlwifi(AX200)  521 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn

4.wiphy0  802.11abgn-ax  iwlwifi(AX200)  521 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
4.wiphy1  802.11abgn-ax  iwlwifi(AX200)  521 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn

5.wiphy0  802.11abgn-ax  iwlwifi(AX200)  521 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
5.wiphy1  802.11abgn-ax  iwlwifi(AX200)  521 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn

6.wiphy0  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
6.wiphy1  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
6.wiphy2  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
6.wiphy3  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
6.wiphy4  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
6.wiphy5  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
6.wiphy6  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
6.wiphy7  802.11abgn-ax  iwlwifi(AX200)  523 - 1  stations - 5ghz/24ghz use only for 802.11ax - 24gz abgn
6.wiphy8  802.11an-AC    ath10k(9984)    523 - 64 stations - 5ghz
6.wiphy9  802.11an-AC    ath10k(9984)    523 - 64 stations - 5ghz

########################################################################################################
TECHNICAL UNDERSTANDING: LANForge
########################################################################################################
    LANForge Monitored Values Per Polling Interval
        'rx bytes' - bytes transmitted
        'rx rate'  - bits per second 

    in DL direction: -B tx -> -A rx, (side_b_tx_min_bps) LANforge Eth endpoint transmits bytes (AP/DUT), station endpoint (Wifi) LANForge receives them.  station-end-rx-bps (bits per second) is download rx-bps (bits per second)
    in UL direction: -A tx -> -B rx, (side_a_tx_min_bps) LANforge Eth endpoint receives bytes (AP/DUT), station endpoint (Wifi) LANForge transmits them.  ethernet-end-rx-bps (bits per second) is upload load rx-bps (bits per second)

#########################################################################################################
LANforge GUI what is displayed in the Column and how to access the value with cli or json
#########################################################################################################
# NOTE: see how rx rate is used in script and can monitor any values in similiar manner 

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
        ''')
    #############################################
    # Fixed Configurations Coded Into Script
    #############################################
    parser.add_argument('-ct1', '--controller_test_1', help='--controller_test_1 LANforge static radio configuration',
                        action="store_true")
    parser.add_argument('-ct2', '--controller_test_2', help='--controller_test_2 LANforge static radio configuration',
                        action="store_true")
    parser.add_argument('-ct3', '--controller_test_3', help='--controller_test_3 LANforge static radio configuration',
                        action="store_true")

    #############################################
    # Script Controller Configurations
    #############################################
    parser.add_argument('-cca', '--controller_aps',
                        help='--controller_aps List of APs to test  default: APA453.0E7B.CF9C',
                        default="APA453.0E7B.CF9C")
    parser.add_argument('-ccf', '--controller_bands', help='--controller_bands <a | b | abgn> default: a', default="a")
    parser.add_argument('-cwm', '--controller_wifimodes', help='List of of wifi mode to test default: auto',
                        default="auto")

    parser.add_argument('-cc5', '--controller_chan_5ghzs', help='--controller_chan_5ghzs <36 40 ...> default 36',
                        default="36")
    parser.add_argument('-cc2', '--controller_chan_24ghzs', help='--controller_chan_24ghzs <1 2 ...> default 1',
                        default="1")
    parser.add_argument('-ccw', '--controller_chan_widths',
                        help='--controller_chan_widths <20 40 80 160> default: \"20\"', default="20")
    parser.add_argument('-cam', '--controller_ap_modes', help='--controller_ap_modes <local flexconnect> default local',
                        default="local")
    parser.add_argument('-pdu', '--controller_pdus',
                        help='--controller_pdus List of packet sizes \"88 512 1370 1518\" default 1580', default="1518")

    parser.add_argument('-cde', '--controller_data_encryptions',
                        help='--controller_data_encryptions \"enable disable\"', default="disable")
    parser.add_argument('-cs', '--controller_series', help='--controller_series <9800 | 3504>', default="9800",
                        choices=["9800", "3504"])
    parser.add_argument('-ccp', '--controller_prompt', type=str, help="controller prompt default WLC", default="WLC")
    parser.add_argument('-cas', '--controller_ap_slot', type=str, help="AP slot, default 1", default="1")
    parser.add_argument('-cwl', '--controller_wlan', type=str, help="--controller_wlan <wlan>, default wlan",
                        default="wlan")

    parser.add_argument('-cc', '--controller_ip',
                        help='--controller_ip <IP of controller Controller> default 192.168.100.178',
                        default="192.168.100.178")
    parser.add_argument('-cp', '--controller_port',
                        help='--controller_port <port of controller Controller> ssh default 22', default="22")
    parser.add_argument('-cu', '--controller_user', help='--controller_user <User-name for controller Controller>',
                        default="admin")
    parser.add_argument('-cpw', '--controller_passwd', help='--controller_passwd <Password for controller Controller>',
                        default="controller123")
    parser.add_argument('-ccs', '--controller_scheme',
                        help='--controller_scheme (serial|telnet|ssh): connect via serial, ssh or telnet',
                        default="ssh", choices=["serial", "telnet", "ssh"])
    parser.add_argument('-ccd', '--controller_client_densities',
                        help='--controller_client_densities List of client densities defaults 1', default="1")

    parser.add_argument('-ctp', '--controller_tx_powers',
                        help='--controller_tx_powers <1 | 2 | 3 | 4 | 5 | 6 | 7 | 8>  1 is highest power default 3',
                        default="3", choices=["1", "2", "3", "4", "5", "6", "7", "8"])
    parser.add_argument('-cco', '--cap_ctl_out',
                        help='--cap_ctl_out , switch the controller controller output will be captured',
                        action='store_true')

    #################################################################
    # Script AP parameters for reading AP, - not used in this script
    #################################################################
    parser.add_argument('-api', '--ap_info', action='append', nargs=1, type=str,
                        help='(enter 0 if does not apply) --ap_info \"ap_scheme==<telnet,ssh or serial> ap_prompt==<ap_prompt> ap_ip==<ap ip> ap_port==<ap port number> ap_user==<ap user> ap_pw==<ap password> ap_tty==<tty serial device>\" ')
    # --ap_info "ap_scheme==serial ap_prompt==APA53.0E7B.CF9C ap_ip==0 ap_port==0 ap_user==admin ap_pw==Admin123 ap_tty==/dev/ttyUSB2"

    #############################################
    # Script LANforge Configurations
    #############################################
    parser.add_argument('-lm', '--mgr', help='--mgr <hostname for where LANforge GUI is running>', default='localhost')
    parser.add_argument('-d', '--test_duration',
                        help='--test_duration <how long to run>  example --time 5d (5 days) default: 2m options: number followed by d, h, m or s',
                        default='20s')
    parser.add_argument('-pi', '--polling_interval', help="--polling_interval <seconds>", default='5s')
    parser.add_argument('--tos', help='--tos:  Support different ToS settings: BK | BE | VI | VO | numeric',
                        default="BE")
    parser.add_argument('-db', '--debug', help='--debug:  Enable debugging', action='store_true')
    parser.add_argument('-t', '--endp_types',
                        help='--endp_types <types of traffic> example --endp_types \"lf_udp lf_tcp\"  Default: lf_udp lf_tcp, options: lf_udp, lf_udp6, lf_tcp, lf_tcp6, mc_udp, mc_udp6',
                        default='lf_udp lf_tcp', type=valid_endp_types)
    parser.add_argument('-cd', '--controller_directions',
                        help='--controller_directions <upload download> example --controller_directions \"upload download\"  Default: upload download',
                        default='upload download')
    parser.add_argument('-u', '--upstream_port',
                        help='--upstream_port <cross connect upstream_port> example: --upstream_port eth1',
                        default='eth1')
    parser.add_argument('-o', '--csv_outfile', help="--csv_outfile <Output file for csv data>", default='snp')
    parser.add_argument("-l", "--log", action='store_true', help="create logfile for messages, default stdout")
    parser.add_argument('-c', '--csv_output', help="Generate csv output", default=True)

    parser.add_argument('-r', '--radio', action='append', nargs=1, help='--radio  \
                        \"radio==<number_of_wiphy stations=<=number of stations> ssid==<ssid> ssid_pw==<ssid password> security==<security> wifimode==<wifimode>\" ',
                        required=False)
    parser.add_argument('-ul_bps', '--side_a_tx_min_bps',
                        help='--side_a_tx_min_bps , upload (A side tx) min tx rate bps  default 256000 500000000',
                        default="256000 1000000000")
    parser.add_argument('-dl_bps', '--side_b_tx_min_bps',
                        help='--side_b_tx_min_bps , download(B side tx) min tx rate bps  default 1000000000',
                        default="1000000000")

    ##############################################
    # Parameters Used For Testing
    ##############################################
    parser.add_argument('-noc', '--no_controller', help='-noc / --no_controller no configuration of the controller',
                        action='store_true')
    parser.add_argument('-nos', '--no_stations', help='-nos / --no_stations , no stations', action='store_true')
    parser.add_argument('-wto', '--wait_timeout', type=int,
                        help='-wto / --wait_timeout , time to wait for stations to get IP ',
                        default="360")
    parser.add_argument('-ptc', '--print_test_config',
                        help='-ptc / --print_test_config , print out the test configuration and exit',
                        action='store_true')

    ##############################################################
    #
    #  Scaling and Performance Args Parser
    #
    ##############################################################
    args = parser.parse_args()
    controller_args = args  # use args.
    # logg.info("args: {}".format(args))
    debug_on = args.debug

    ###############################################################
    # Gather Test Data
    ###############################################################

    if args.controller_scheme:
        __scheme = args.controller_scheme

    if args.controller_port:
        __port = args.controller_port

    if args.controller_ip:
        __ctlr = args.controller_ip

    if args.controller_prompt:
        __prompt = args.controller_prompt

    if args.controller_series:
        __series = args.controller_series

    if args.controller_user:
        __user = args.controller_user

    if args.controller_passwd:
        __passwd = args.controller_passwd

    if args.cap_ctl_out:
        __cap_ctl_out = args.cap_ctl_out
    else:
        __cap_ctl_out = False

    if args.controller_ap_slot:
        __ap_slot = args.controller_ap_slot

    if args.controller_wlan:
        __wlan = args.controller_wlan

    ap_dict = []
    if args.ap_info:
        ap_info = args.ap_info
        for _ap_info in ap_info:
            print("ap_info {}".format(_ap_info))
            ap_keys = ['ap_scheme', 'ap_prompt', 'ap_ip', 'ap_port', 'ap_user', 'ap_pw', 'ap_tty', 'ap_baud']
            ap_dict = dict(
                map(lambda x: x.split('=='), str(_ap_info).replace('[', '').replace(']', '').replace("'", "").split()))
            for key in ap_keys:
                if key not in ap_dict:
                    print("missing ap config, for the {}, all these need to be set {} ".format(key, ap_keys))
                    exit(1)
            print("ap_dict: {}".format(ap_dict))

    ###############################################
    #
    # Create a report instanciate a reporting class
    #
    ###############################################
    report = lf_report(_results_dir_name="Scaling_and_Performance", _output_html="snp.html", _output_pdf="snp.pdf")

    if args.csv_outfile:
        current_time = time.strftime("%m_%d_%Y_%H_%M_%S", time.localtime())
        csv_outfile = "details_{}_{}.csv".format(args.csv_outfile, current_time)
        csv_outfile = report.file_add_path(csv_outfile)

        csv_results = "results_{}_{}.csv".format(args.csv_outfile, current_time)
        csv_results = report.file_add_path(csv_results)
        print("csv output file : {}".format(csv_outfile))
        print("csv results file : {}".format(csv_results))

    if args.log:
        outfile_log = "{}_{}_output_log.log".format(args.outfile, current_time)
        outfile_log = report.file_add_path(outfile_log)
        print("output file log: {}".format(outfile_log))
    else:
        outfile_log = "stdout"
        print("output file log: {}".format(outfile_log))

        # Set up the log file
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(FORMAT)
    logg = logging.getLogger(__name__)
    logg.setLevel(logging.DEBUG)
    file_handler = None
    if args.log:
        file_handler = logging.FileHandler(outfile_log, "w")

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logg.addHandler(file_handler)
        logg.addHandler(logging.StreamHandler(sys.stdout))  # allows to logging to file and stderr
        # if loggin.basicConfig is called this will result in duplicating log entries
        # logging.basicConfig(format=FORMAT, handlers=[file_handler])
    else:
        # stdout logging
        logging.basicConfig(format=FORMAT, handlers=[console_handler])

    #############################################################
    #
    #   Radio Eictionary for LANforge 1 in LANforge Realm
    #   Configuration used by command switch --controller_test_1
    #
    #############################################################
    radio_AX200_abgn_ax_list_001_one = [
        ['radio==1.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]

    radio_AX200_abgn_ax_list_008_one = [
        ['radio==1.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy2 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy3 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy4 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy5 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy6 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy7 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]

    radio_AX200_abgn_ax_dict_one = {'1': radio_AX200_abgn_ax_list_001_one,
                                    '8': radio_AX200_abgn_ax_list_008_one}

    radio_ath10K_9984_an_AC_list_001_one = [
        ['radio==1.wiphy8 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath10K_9984_an_AC_list_010_one = [
        ['radio==1.wiphy8 stations==10 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath10K_9984_an_AC_list_020_one = [
        ['radio==1.wiphy8 stations==20 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath10K_9984_an_AC_list_050_one = [
        ['radio==1.wiphy8 stations==50 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath10K_9984_an_AC_list_050_one = [
        ['radio==1.wiphy8 stations==64 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]

    radio_ath10K_9984_an_AC_dict_one = {'1': radio_ath10K_9984_an_AC_list_001_one,
                                        '10': radio_ath10K_9984_an_AC_list_010_one,
                                        '20': radio_ath10K_9984_an_AC_list_020_one,
                                        '50': radio_ath10K_9984_an_AC_list_020_one,
                                        '65': radio_ath10K_9984_an_AC_list_020_one}

    ####################################################################
    #
    # End of Configuration used by command switch --controller_test_1
    #
    ####################################################################

    ############################################################
    #
    #  Radio Dictionary for multiple LANforge in  Realm 
    #  Configuration used by command switch --controller_test_2
    #
    ############################################################
    radio_AX200_abgn_ax_list_001 = [
        ['radio==1.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]

    radio_AX200_abgn_ax_list_010 = [
        ['radio==1.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy2 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy3 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy4 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy5 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy6 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy7 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==2.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==2.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]

    radio_AX200_abgn_ax_list_020 = [
        ['radio==1.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy2 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy3 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy4 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy5 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy6 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy7 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==2.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==2.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==3.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==3.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==4.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==4.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==5.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==5.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==6.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==6.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==6.wiphy2 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==6.wiphy3 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
    ]

    radio_AX200_abgn_ax_list_024 = [
        ['radio==1.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy2 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy3 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy4 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy5 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy6 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy7 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==2.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==2.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==3.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==3.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==4.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==4.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==5.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==5.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==6.wiphy0 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==6.wiphy1 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==6.wiphy2 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==6.wiphy3 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==6.wiphy4 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==6.wiphy5 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==6.wiphy6 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==6.wiphy7 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
    ]

    radio_AX200_abgn_ax_dict = {'1': radio_AX200_abgn_ax_list_001,
                                '10': radio_AX200_abgn_ax_list_010,
                                '24': radio_AX200_abgn_ax_list_024}

    radio_ath10K_9984_an_AC_list_001 = [
        ['radio==1.wiphy8 stations==1 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath10K_9984_an_AC_list_010 = [
        ['radio==1.wiphy8 stations==10 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath10K_9984_an_AC_list_020 = [
        ['radio==1.wiphy8 stations==20 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath10K_9984_an_AC_list_050 = [
        ['radio==1.wiphy8 stations==50 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath10K_9984_an_AC_list_100 = [
        ['radio==1.wiphy8 stations==50 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy9 stations==50 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath10K_9984_an_AC_list_200 = [
        ['radio==1.wiphy8 stations==50 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy9 stations==50 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==6.wiphy8 stations==50 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==6.wiphy9 stations==50 ssid==test-can ssid_pw==[BLANK] security==open wifimode==auto']]

    radio_ath10K_9984_an_AC_dict = {'1': radio_ath10K_9984_an_AC_list_001,
                                    '50': radio_ath10K_9984_an_AC_list_050,
                                    '200': radio_ath10K_9984_an_AC_list_200}

    ####################################################################
    #
    # End of Configuration used by command switch --controller_test_2
    #
    ####################################################################

    #############################################################
    #
    #  Static dictionary for radios on 191.168.100.178  
    #  Static Configuration Candela Tech Realm ()
    #  Configuration used by command switch --controller_test_3
    #
    #############################################################
    # iwlwifi(AX200) 521
    radio_AX200_abgn_ax_list_001_wiphy2 = [
        ['radio==1.wiphy2 stations==1 ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto']]

    radio_AX200_abgn_ax_list_001 = [
        ['radio==1.wiphy2 stations==1 ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_AX200_abgn_ax_list_004 = [
        ['radio==1.wiphy2 stations==1 ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy3 stations==1 ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy4 stations==1 ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto'],
        ['radio==1.wiphy5 stations==1 ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto']]

    radio_AX200_abgn_ax_dict_test = {'1': radio_AX200_abgn_ax_list_001,
                                     '4': radio_AX200_abgn_ax_list_004}

    radio_AX200_abgn_ax_dict_test_wiphy2 = {'1': radio_AX200_abgn_ax_list_001_wiphy2}

    radio_ath10K_9984_an_AC_list_001 = [
        ['radio==1.wiphy0 stations==1   ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath10K_9984_an_AC_list_010 = [
        ['radio==1.wiphy0 stations==10  ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath10K_9984_an_AC_list_020 = [
        ['radio==1.wiphy0 stations==20  ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath10K_9984_an_AC_list_050 = [
        ['radio==1.wiphy0 stations==50  ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto']]

    radio_ath10K_9984_an_AC_list_001_wiphy0 = [
        ['radio==1.wiphy0 stations==1    ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath10K_9984_an_AC_list_010_wiphy0 = [
        ['radio==1.wiphy0 stations==10   ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto']]

    radio_ath10K_9984_an_AC_dict_test_wiphy0 = {'1': radio_ath10K_9984_an_AC_list_001_wiphy0,
                                                '10': radio_ath10K_9984_an_AC_list_010_wiphy0}

    radio_ath10K_9984_an_AC_dict_test = {'1': radio_ath10K_9984_an_AC_list_001,
                                         '10': radio_ath10K_9984_an_AC_list_010,
                                         '50': radio_ath10K_9984_an_AC_list_050}

    ####################################################################
    # Test to use ath9K
    ####################################################################

    radio_ath9K_9984_abgn_list_001 = [
        ['radio==1.wiphy1 stations==1 ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath9K_9984_abgn_list_010 = [
        ['radio==1.wiphy1 stations==10 ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath9K_9984_abgn_list_020 = [
        ['radio==1.wiphy1 stations==20 ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath9K_9984_abgn_list_050 = [
        ['radio==1.wiphy1 stations==50 ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto']]
    radio_ath9K_9984_abgn_list_200 = [
        ['radio==1.wiphy1 stations==200 ssid==test_candela ssid_pw==[BLANK] security==open wifimode==auto']]

    radio_ath9K_9984_abgn_dict_test = {'1': radio_ath9K_9984_abgn_list_001,
                                       '10': radio_ath9K_9984_abgn_list_010,
                                       '20': radio_ath9K_9984_abgn_list_020,
                                       '50': radio_ath9K_9984_abgn_list_050,
                                       '200': radio_ath9K_9984_abgn_list_200}
    ####################################################################
    # Test to only use teh ath9K
    ####################################################################
    #
    # End of Configuration used by command switch --controller_test_3
    #
    ####################################################################
    MAX_NUMBER_OF_STATIONS = 200

    radio_name_list = []
    number_of_stations_per_radio_list = []
    ssid_list = []
    ssid_password_list = []
    ssid_security_list = []
    wifimode_list = []

    # optional radio configuration
    reset_port_enable_list = []
    reset_port_time_min_list = []
    reset_port_time_max_list = []

    wifi_mode_dict = {
        "auto": "0",
        "a": "1",
        "b": "2",
        "g": "3",
        "abg": "4",
        "abgn": "5",
        "bgn": "6",
        "bg": "7",
        "abgnAC": "8",
        "anAC": "9",
        "an": "10",
        "bgnAC": "11",
        "abgnAX": "12",
        "bgnAX": "13",
        "anAX": "14"
    }

    ###########################################################################################
    #  Test Configurations:  Take presidence over command line arguments
    #     GOAL: help with command line configurations
    ###########################################################################################

    ###########################################################################################
    #
    # controller_test_1
    #
    ###########################################################################################
    # Test configuration that may be read in , in conjunction with command line arguments
    if args.controller_test_1:
        logg.info("USING: controller_test_1")
        controller_aps = "vanc-e".split()
        controller_bands = "a b".split()
        controller_wifimodes = "an anAX anAC abgn bg".split()
        controller_tx_powers = "3".split()
        controller_chan_5ghzs = "36".split()
        controller_chan_24ghzs = "1".split()
        controller_chan_widths = "20 40 80".split()
        controller_ap_modes = "local".split()
        controller_data_encryptions = "disable".split()
        controller_packet_types = "lf_udp lf_tcp".split()
        controller_directions = "upload download".split()
        controller_pdus = "88 512 1370 1518".split()
        controller_client_densities = "1 10 50 200".split()
        controller_side_a_tx_min_bps = "256000".split()
        controller_side_b_tx_min_bps = "256000".split()
        radio_AX200_abgn_ax_dict = radio_AX200_abgn_ax_dict_one
        radio_ath10K_9984_an_AC_dict = radio_ath10K_9984_an_AC_dict_one

    ###########################################################################################
    #
    # controller_test_2
    #
    ###########################################################################################
    elif args.controller_test_2:
        logg.info("USING: controller_test_2")
        # Note the local system only supports 802.11-abgn , 802.11a
        controller_aps = "APA453.0E7B.CF9C".split()
        controller_bands = "a".split()
        # controller_wifimodes       = "an anAX anAC abgn bg".split()
        controller_wifimodes = "an".split()
        controller_tx_powers = "3".split()
        controller_chan_5ghzs = "36".split()
        controller_chan_24ghzs = "1".split()
        controller_chan_widths = "20".split()
        controller_ap_modes = "local".split()
        controller_data_encryptions = "disable".split()
        # controller_packet_types    = "lf_udp lf_tcp".split()
        controller_packet_types = "lf_udp".split()
        # controller_directions      = "upload download".split()
        controller_directions = "upload download".split()
        # controller_pdus            = "88 512 1370 1518".split()
        controller_pdus = "1518".split()
        controller_client_densities = "10".split()
        controller_data_encryptions = "disable".split()
        controller_side_a_tx_min_bps = "256000".split()
        controller_side_b_tx_min_bps = "256000".split()
        radio_AX200_abgn_ax_dict = radio_AX200_abgn_ax_dict_test
        radio_ath10K_9984_an_AC_dict = radio_ath10K_9984_an_AC_dict_test

    ###########################################################################################
    #
    # controller_test_3
    #
    ###########################################################################################
    elif args.controller_test_3:  # CMR_test_3
        logg.info("USING: controller_test_3")
        # Note the local system only supports 802.11-abgn , 802.11a
        controller_aps = "APA453.0E7B.CF9C".split()
        controller_bands = "a".split()
        # controller_wifimodes       = "an anAX anAC abgn bg".split()
        controller_wifimodes = "an".split()
        controller_tx_powers = "3".split()
        controller_chan_5ghzs = "36".split()
        controller_chan_24ghzs = "1".split()
        controller_chan_widths = "20".split()
        controller_ap_modes = "local".split()
        controller_data_encryptions = "disable".split()
        # controller_packet_types    = "lf_udp lf_tcp".split()
        controller_packet_types = "lf_udp".split()
        # controller_directions      = "upload download".split()
        controller_directions = "upload download".split()
        # controller_pdus            = "88 512 1370 1518".split()
        controller_pdus = "1518".split()
        controller_client_densities = "1".split()
        controller_data_encryptions = "disable".split()
        controller_side_a_tx_min_bps = "256000".split()
        controller_side_b_tx_min_bps = "256000".split()
        radio_AX200_abgn_ax_dict = radio_AX200_abgn_ax_dict_test_wiphy2
        radio_ath10K_9984_an_AC_dict = radio_ath10K_9984_an_AC_dict_test
        # radio_ath10K_9984_an_AC_dict = radio_ath9K_9984_abgn_dict_test

    ###########################################################################################
    #  Use Command line arguments
    ###########################################################################################
    else:

        controller_aps = args.controller_aps.split()
        controller_bands = args.controller_bands.split()
        controller_wifimodes = args.controller_wifimodes.split()
        for mode in controller_wifimodes:
            if mode in wifi_mode_dict.keys():
                pass
            else:
                logg.info(
                    "wifimode [{}] not recognised. Please use: auto, a, b, g, abg, abgn, bgn, bg, abgnAC, anAC, an, bgnAC, abgnAX, bgnAX, anAX".format(
                        mode))
                exit(1)
        controller_tx_powers = args.controller_tx_powers.split()
        controller_chan_5ghzs = args.controller_chan_5ghzs.split()
        controller_chan_24ghzs = args.controller_chan_24ghzs.split()
        controller_chan_widths = args.controller_chan_widths.split()
        controller_ap_modes = args.controller_ap_modes.split()
        controller_client_densities = args.controller_client_densities.split()
        controller_packet_types = args.endp_types.split()
        controller_pdus = args.controller_pdus.split()
        controller_directions = args.controller_directions.split()
        controller_data_encryptions = args.controller_data_encryptions.split()

        controller_side_a_tx_min_bps = args.side_a_tx_min_bps.split()
        controller_side_b_tx_min_bps = args.side_b_tx_min_bps.split()
    logg.info("TEST CONFIG: ")
    logg.info("controller_aps ('-cca' ,'--controller_aps'): {}".format(controller_aps))
    logg.info("controller_bands ('-ccf' ,'--controller_bands'): {}".format(controller_bands))
    logg.info("controller_wifimodes ('-cwm' ,'--controller_wifimodes'): {}".format(controller_wifimodes))
    logg.info("controller_chan_5ghzs ('-cc5','--controller_chan_5ghzs'): {}".format(controller_chan_5ghzs))
    logg.info("controller_chan_24ghzs ('-cc2','--controller_chan_24ghzs'): {}".format(controller_chan_24ghzs))
    logg.info("controller_chan_widths ('-ccw','--controller_chan_widths'): {}".format(controller_chan_widths))
    logg.info("controller_tx_powers ('-ctp','--controller_tx_powers'): {}".format(controller_tx_powers))
    logg.info("controller_ap_modes ('-cam','--controller_ap_modes'): {}".format(controller_ap_modes))
    logg.info(
        "controller_client_densities ('-ccd','--controller_client_densities'): {}".format(controller_client_densities))
    logg.info("controller_packet_types ('-t', '--endp_types'): {}".format(controller_packet_types))
    logg.info("controller_pdus ('-cps','--controller_pdus'): {}".format(controller_pdus))
    logg.info("controller_directions ('-cd', '--controller_directions'): {}".format(controller_directions))
    logg.info(
        "controller_data_encryptions ('-cde','--controller_data_encryptions') {}".format(controller_data_encryptions))
    logg.info("controller_side_a_tx_min_bps ('-amr','--side_a_tx_min_bps'): {}".format(controller_side_a_tx_min_bps))
    logg.info("controller_side_b_tx_min_bps ('-bmr','--side_b_tx_min_bps'): {}".format(controller_side_b_tx_min_bps))
    logg.info("test duration ('-d','--test_duration'): {}".format(args.test_duration))
    logg.info("polling_interval ('-pi','--polling_interval'): {}".format(args.polling_interval))

    if args.radio:
        logg.info("radios from command line used")
        logg.info(args.radio)
    elif args.controller_test_1 or args.controller_test_2 or args.controller_test_3:
        logg.info("radios from coded config used")
        logg.info("##### AX200 RADIOS #####")
        logg.info(radio_AX200_abgn_ax_dict)
        logg.info('##### ATH10K_9984 RADIOS ####')
        logg.info(radio_ath10K_9984_an_AC_dict)
    else:
        logg.info(
            "No radios endered EXITING,  use --radio or --controller_test_1, --controller_test_2 or --controller_test_3")
        exit(1)

    if args.print_test_config:
        logg.info("PRINT TEST CONFIG ONLY - exiting remove --print_test_config to run test")
        try:
            report_path = report.get_report_path()
            logg.info("Reports Directory Created: {}".format(report_path))
        except:
            logg.info("Reports Directory Created")
        exit(1)

    __ap_set = None
    __band_set = None
    __chan_width_set = None
    __ap_mode_set = None
    __tx_power_set = None
    __chan_5ghz_set = None
    __chan_24ghz_set = None
    __csv_started = False

    for controller_ap in controller_aps:
        for controller_band in controller_bands:  # frequency
            for controller_wifimode in controller_wifimodes:
                # check for valid frequency and wifi_mode combination put here to simplify logic since all radios do not support all modes
                # "an anAX anAC abgn bg"
                if ((controller_band == "a" and controller_wifimode == "bg") or (
                        controller_band == "b" and controller_wifimode == "anAC")):
                    logg.info("#######################################################################")
                    logg.info("# Skipping combination controller_band {} controller_wifimode {}".format(controller_band,
                                                                                                        controller_wifimode))
                    logg.info("#######################################################################")
                    pass  # invalid combination continue
                else:
                    for controller_tx_power in controller_tx_powers:
                        for controller_chan_5ghz in controller_chan_5ghzs:
                            for controller_chan_24ghz in controller_chan_24ghzs:
                                for controller_chan_width in controller_chan_widths:  # bandwidth
                                    for controller_data_encryption in controller_data_encryptions:
                                        for controller_ap_mode in controller_ap_modes:
                                            for controller_client_density in controller_client_densities:
                                                radios = ""
                                                ########################################################
                                                # Validate radio configuration 
                                                # If controller_client_density is NOT supported continue
                                                ########################################################

                                                ########################################################
                                                # USE command line to configure LANforge radios
                                                ###############################################
                                                if args.radio:
                                                    radios = args.radio
                                                    logg.info(
                                                        "########################################################")
                                                    logg.info("# radios configured from command line {}".format(radios))
                                                    logg.info("# controller_band: {}".format(controller_band))
                                                    logg.info("# controller_wifimode: {}".format(controller_wifimode))
                                                    logg.info(
                                                        "########################################################")

                                                #################################################################
                                                # USE radio dictionaies in this file to configure LANforge radios
                                                #################################################################
                                                elif controller_band == "a":
                                                    if controller_wifimode == "anAX" or controller_wifimode == "abgn":
                                                        # AX200 dual band
                                                        try:
                                                            radios = radio_AX200_abgn_ax_dict[controller_client_density]
                                                            logg.info("controller_client_density:{} radios: {}".format(
                                                                controller_client_density, radios))
                                                        except:
                                                            logg.info(
                                                                "CONTROLLER DENSITY INVALID FOR RADIO DICTIONARY: controller_client_density: {} not supported for configuration".format(
                                                                    controller_client_density))
                                                            logg.info(
                                                                "CONTROLLER DENSITY INVALID FOR RADIO DICTIONARY: current dictionary radio_AX200_abgn_ax_dict {}".format(
                                                                    radio_AX200_abgn_ax_dict))
                                                            logg.info(
                                                                "CONTROLLER DENSITY INVALID FOR RADIO DICTIONARY: MOVE TO NEXT DENSITY CONTINUING TESTING")
                                                            continue
                                                    elif controller_wifimode == "an" or controller_wifimode == "anAC" or controller_wifimode == "auto":
                                                        # ath10K only supports 5Ghz
                                                        try:
                                                            radios = radio_ath10K_9984_an_AC_dict[
                                                                controller_client_density]
                                                            logg.info("radios: {}".format(radios))
                                                        except:
                                                            logg.info(
                                                                "CONTROLLER DENSITY INVALID FOR RADIO DICTIONARY: controller_client_density: {} not supported for configuration".format(
                                                                    controller_client_density))
                                                            logg.info(
                                                                "CONTROLLER DENSITY INVALID FOR RADIO DICTIONARY: current dictionary radio_AX200_abgn_ax_dict {}".format(
                                                                    radio_ath10K_9984_an_AC_dict))
                                                            logg.info(
                                                                "CONTROLLER DENSITY INVALID FOR RADIO DICTIONARY: MOVE TO NEXT DENSITY CONTINUING TESTING")
                                                            continue
                                                    else:
                                                        logg.info("##################################")
                                                        logg.info("# INVALID COMBINATION 5ghz")
                                                        # logg.info("# controller run settings: {}".format(test_config))
                                                        logg.info("##################################")
                                                        exit(1)
                                                else:  # controller_band == "b"
                                                    if controller_wifimode == "an" or controller_wifimode == "anAX" or controller_wifimode == "abgn" or controller_wifimode == "bg" or controller_wifimode == "auto":
                                                        # AX200 dual band
                                                        try:
                                                            radios = radio_AX200_abgn_ax_dict[controller_client_density]
                                                            logg.info("radios: {}".format(radios))
                                                        except:
                                                            logg.info(
                                                                "CONTROLLER DENSITY INVALID FOR RADIO DICTIONARY: controller_client_density: {} not supported for configuration".format(
                                                                    controller_client_density))
                                                            logg.info(
                                                                "CONTROLLER DENSITY INVALID FOR RADIO DICTIONARY: current dictionary radio_AX200_abgn_ax_dict {}".format(
                                                                    radio_AX200_abgn_ax_dict))
                                                            logg.info(
                                                                "CONTROLLER DENSITY INVALID FOR RADIO DICTIONARY: MOVE TO NEXT DENSITY CONTINUING TESTING")
                                                            continue
                                                    else:
                                                        logg.info("##################################")
                                                        logg.info("# INVALID COMBINATION 24 ghz")
                                                        # logg.info("# controller run settings: {}".format(test_config))
                                                        logg.info("##################################")
                                                        exit(1)

                                                for controller_packet_type in controller_packet_types:
                                                    for controller_direction in controller_directions:
                                                        # looping though both A and B together,  upload direction will select A, download direction will select B
                                                        for side_a_tx_min_bps_ul, side_b_tx_min_bps_dl in itertools.zip_longest(
                                                                controller_side_a_tx_min_bps,
                                                                controller_side_b_tx_min_bps, fillvalue=256000):
                                                            for controller_pdu in controller_pdus:
                                                                logg.info(
                                                                    "###################################################################")
                                                                logg.info(
                                                                    "# TEST RUNNING direction:{} ul: {} ,  TEST RUNNING dl: {}".format(
                                                                        controller_direction,
                                                                        side_a_tx_min_bps_ul,
                                                                        side_b_tx_min_bps_dl))
                                                                logg.info(
                                                                    "####################################################################")
                                                                test_config = "AP=={} Band=={} chan_5ghz=={} chan_24ghz=={} wifi_mode=={} BW=={} encryption=={} ap_mode=={} clients=={} packet_type=={} direction=={} pdu=={}".format(
                                                                    controller_ap, controller_band,
                                                                    controller_chan_5ghz, controller_chan_24ghz,
                                                                    controller_wifimode, controller_chan_width,
                                                                    controller_data_encryption, controller_ap_mode,
                                                                    controller_client_density,
                                                                    controller_packet_type, controller_direction,
                                                                    controller_pdu)
                                                                test_keys = ['AP', 'Band', 'wifi_mode', 'chan_5ghz',
                                                                             'chan_24ghz', 'BW', 'encryption',
                                                                             'ap_mode', 'clients', 'packet_type',
                                                                             'direction', 'pdu']
                                                                logg.info(
                                                                    "# controller run settings: {}".format(test_config))
                                                                if args.no_controller:
                                                                    logg.info(
                                                                        "################################################")
                                                                    logg.info(
                                                                        "# TEST MODE : NO CONTROLLER SET : TEST MODE")
                                                                    logg.info(
                                                                        "################################################")
                                                                    if (controller_ap != __ap_set or
                                                                            controller_band != __band_set or
                                                                            controller_chan_width != __chan_width_set or
                                                                            controller_ap_mode != __ap_mode_set or
                                                                            controller_tx_power != __tx_power_set or
                                                                            controller_chan_5ghz != __chan_5ghz_set or
                                                                            controller_chan_24ghz != __chan_24ghz_set):
                                                                        logg.info(
                                                                            "###############################################")
                                                                        logg.info(
                                                                            "# TEST MODE : NEW CONTROLLER CONFIG : TEST MODE")
                                                                        logg.info(
                                                                            "###############################################")
                                                                        __ap_set = controller_ap
                                                                        __band_set = controller_band
                                                                        __chan_width_set = controller_chan_width
                                                                        __ap_mode_set = controller_ap_mode
                                                                        __tx_power_set = controller_tx_power
                                                                        __chan_5ghz_set = controller_chan_5ghz
                                                                        __chan_24ghz_set = controller_chan_24ghz
                                                                        __client_density = controller_client_density
                                                                else:
                                                                    logg.info(
                                                                        "################################################")
                                                                    logg.info(
                                                                        "# SETUP MODE : SETUP CONTROLLER : SETUP MODE")
                                                                    logg.info(
                                                                        "################################################")

                                                                    if (controller_ap != __ap_set or
                                                                            controller_band != __band_set or
                                                                            controller_chan_width != __chan_width_set or
                                                                            controller_ap_mode != __ap_mode_set or
                                                                            controller_tx_power != __tx_power_set or
                                                                            controller_chan_5ghz != __chan_5ghz_set or
                                                                            controller_chan_24ghz != __chan_24ghz_set):
                                                                        logg.info(
                                                                            "###############################################")
                                                                        logg.info(
                                                                            "# SETUP MODE : NEW CONTROLLER CONFIG")
                                                                        logg.info(
                                                                            "###############################################")
                                                                        __ap_set = controller_ap
                                                                        __band_set = controller_band
                                                                        __chan_width_set = controller_chan_width
                                                                        __ap_mode_set = controller_ap_mode
                                                                        __tx_power_set = controller_tx_power
                                                                        __chan_5ghz_set = controller_chan_5ghz
                                                                        __chan_24ghz_set = controller_chan_24ghz
                                                                        __client_density = controller_client_density
                                                                        controller = CreateCtlr(
                                                                            _scheme=__scheme,
                                                                            _port=__port,
                                                                            _series=__series,
                                                                            _ctlr=__ctlr,
                                                                            _prompt=__prompt,
                                                                            _user=__user,
                                                                            _passwd=__passwd,
                                                                            _ap=__ap_set,
                                                                            _band=__band_set,
                                                                            _chan_5ghz=__chan_5ghz_set,
                                                                            _chan_24ghz=__chan_24ghz_set,
                                                                            _chan_width=__chan_width_set,
                                                                            _ap_mode=__ap_mode_set,
                                                                            _tx_power=__tx_power_set,
                                                                            _wlan=__wlan,
                                                                            _cap_ctl_out=__cap_ctl_out
                                                                        )
                                                                        # Disable AP
                                                                        #
                                                                        # Controller Configuration
                                                                        #
                                                                        # if controller_args.controller_series == "9800":
                                                                        #    controller_controller_no_loggin_console()
                                                                        pss = controller.controller_show_ap_summary()
                                                                        logg.info("pss {}".format(pss))
                                                                        controller.controller_disable_ap()
                                                                        if controller_args.controller_series == "9800":
                                                                            # CISCO 4/27/2021 controller.controller_disable_wlan()
                                                                            controller.controller_disable_network_5ghz()
                                                                            controller.controller_disable_network_24ghz()
                                                                            # CISCO 4/27/2021 controller.controller_role_manual()
                                                                        else:
                                                                            controller.controller_disable_network_5ghz()
                                                                            controller.controller_disable_network_24ghz()
                                                                        controller.controller_set_tx_power()
                                                                        controller.controller_set_channel()
                                                                        controller.controller_set_bandwidth()
                                                                        # if controller_args.controller_series == "9800":
                                                                        # CANDELA TODO, not needed controller.controller_create_wlan()
                                                                        # CANDELA TODO set the policy tag, controller.controller_set_wireless_tag_policy()
                                                                        # CANDELA controller.controller_enable_wlan()
                                                                        if controller_band == "a":
                                                                            controller.controller_enable_network_5ghz()
                                                                        else:
                                                                            controller.controller_enable_network_24ghz()
                                                                        controller.controller_enable_ap()
                                                                        # need to actually check the CAC timer
                                                                        time.sleep(30)
                                                                        ####################################
                                                                        # end of controller controller code
                                                                        ####################################
                                                                    else:
                                                                        logg.info(
                                                                            "###############################################")
                                                                        logg.info(
                                                                            "# SETUP MODE : NO CHANGE TO CONTROLLER CONFIG")
                                                                        logg.info(
                                                                            "###############################################")
                                                                        logg.info(
                                                                            "controller_ap: {} controller_band: {} controller_chan_width: {} controller_ap_mode: {} controller_tx_power: {} controller_chan_5ghz: {} controller_chan_24ghz: {}".format(
                                                                                controller_ap, controller_band,
                                                                                controller_chan_width,
                                                                                controller_ap_mode,
                                                                                controller_tx_power,
                                                                                controller_chan_5ghz,
                                                                                controller_chan_24ghz))
                                                                        logg.info(
                                                                            "__ap_set: {} __band_set: {} __chan_width_set: {} __ap_mode_set: {} __tx_power_set: {} __chan_5ghz_set: {} __chan_24ghz_set: {}".format(
                                                                                __ap_set, __band_set,
                                                                                __chan_width_set, __ap_mode_set,
                                                                                __tx_power_set, __chan_5ghz_set,
                                                                                __chan_24ghz_set))
                                                                    logg.info("controller_wifi_mode {}".format(
                                                                        controller_wifimode))
                                                                    logg.info("radios {}".format(radios))
                                                                    for radio_ in radios:
                                                                        radio_keys = ['radio', 'stations', 'ssid',
                                                                                      'ssid_pw', 'security', 'wifimode']
                                                                        radio_info_dict = dict(
                                                                            map(lambda x: x.split('=='),
                                                                                str(radio_).replace('[', '').replace(
                                                                                    ']', '').replace("'", "").split()))
                                                                        logg.info(
                                                                            "radio_dict {}".format(radio_info_dict))
                                                                        for key in radio_keys:
                                                                            if key not in radio_info_dict:
                                                                                logg.info(
                                                                                    "missing config, for the {}, all of the following need to be present {} ".format(
                                                                                        key, radio_keys))
                                                                                exit(1)
                                                                        radio_name_list.append(radio_info_dict['radio'])
                                                                        ssid_list.append(radio_info_dict['ssid'])
                                                                        ssid_password_list.append(
                                                                            radio_info_dict['ssid_pw'])
                                                                        ssid_security_list.append(
                                                                            radio_info_dict['security'])
                                                                        if args.radio:
                                                                            number_of_stations_per_radio_list.append(
                                                                                radio_info_dict['stations'])
                                                                            wifimode_list.append(int(wifi_mode_dict[
                                                                                                         radio_info_dict[
                                                                                                             'wifimode']]))
                                                                        else:
                                                                            number_of_stations_per_radio_list.append(
                                                                                radio_info_dict['stations'])
                                                                            wifimode_list.append(int(wifi_mode_dict[
                                                                                                         radio_info_dict[
                                                                                                             'wifimode']]))
                                                                        optional_radio_reset_keys = [
                                                                            'reset_port_enable']
                                                                        radio_reset_found = True
                                                                        for key in optional_radio_reset_keys:
                                                                            if key not in radio_info_dict:
                                                                                # logg.info("port reset test not enabled")
                                                                                radio_reset_found = False
                                                                                break

                                                                        if radio_reset_found:
                                                                            reset_port_enable_list.append(True)
                                                                            reset_port_time_min_list.append(
                                                                                radio_info_dict['reset_port_time_min'])
                                                                            reset_port_time_max_list.append(
                                                                                radio_info_dict['reset_port_time_max'])
                                                                        else:
                                                                            reset_port_enable_list.append(False)
                                                                            reset_port_time_min_list.append('0s')
                                                                            reset_port_time_max_list.append('0s')
                                                                # no stations for testing reconfiguration of the controller - 
                                                                if args.no_stations:
                                                                    logg.info(
                                                                        "#################################################")
                                                                    logg.info("# TEST MODE : NO STATIONS TEST MODE")
                                                                    logg.info(
                                                                        "##################################################")
                                                                else:
                                                                    logg.info(
                                                                        "#################################################")
                                                                    logg.info(
                                                                        "# SETUP MODE : CREATING STATIONS SETUP MODE")
                                                                    logg.info(
                                                                        "##################################################")

                                                                    index = 0
                                                                    station_lists = []
                                                                    for (
                                                                            radio_name_,
                                                                            number_of_stations_per_radio_) in zip(radio_name_list, number_of_stations_per_radio_list):
                                                                        number_of_stations = int(
                                                                            number_of_stations_per_radio_)
                                                                        if number_of_stations > MAX_NUMBER_OF_STATIONS:
                                                                            logg.info(
                                                                                "number of stations per radio exceeded max of : {}".format(
                                                                                    MAX_NUMBER_OF_STATIONS))
                                                                            quit(1)
                                                                        station_list = LFUtils.portNameSeries(
                                                                            prefix_="sta", start_id_=1 + index * 1000,
                                                                            end_id_=number_of_stations + index * 1000,
                                                                            padding_number_=10000, radio=radio_name_)
                                                                        station_lists.append(station_list)
                                                                        index += 1
                                                                    # Run Traffic upload (STA to AP)
                                                                    if controller_direction == "upload":
                                                                        side_a_tx_min_bps = side_a_tx_min_bps_ul
                                                                        side_b_tx_min_bps = 0
                                                                        # Run Traffic download (AP to STA)
                                                                    else:
                                                                        side_a_tx_min_bps = 0
                                                                        side_b_tx_min_bps = side_b_tx_min_bps_dl
                                                                        # current default is to have a values
                                                                    ip_var_test = L3VariableTime(
                                                                        args=args,
                                                                        _scheme=__scheme,
                                                                        _port=__port,
                                                                        _series=__series,
                                                                        _ctlr=__ctlr,
                                                                        _prompt=__prompt,
                                                                        _user=__user,
                                                                        _passwd=__passwd,
                                                                        _ap=__ap_set,
                                                                        _ap_slot=__ap_slot,
                                                                        _band=__band_set,
                                                                        _chan_5ghz=__chan_5ghz_set,
                                                                        _chan_24ghz=__chan_24ghz_set,
                                                                        _chan_width=__chan_width_set,
                                                                        _ap_mode=__ap_mode_set,
                                                                        _tx_power=__tx_power_set,
                                                                        _client_density=__client_density,
                                                                        _cap_ctl_out=__cap_ctl_out,
                                                                        _ap_dict=ap_dict,
                                                                        endp_type=controller_packet_type,
                                                                        tos=args.tos,
                                                                        side_b=args.upstream_port,
                                                                        radio_name_list=radio_name_list,
                                                                        number_of_stations_per_radio_list=number_of_stations_per_radio_list,
                                                                        ssid_list=ssid_list,
                                                                        ssid_password_list=ssid_password_list,
                                                                        ssid_security_list=ssid_security_list,
                                                                        wifimode_list=wifimode_list,
                                                                        station_lists=station_lists,
                                                                        name_prefix="LT-",
                                                                        debug_on=debug_on,
                                                                        wait_timeout=args.wait_timeout,
                                                                        outfile=csv_outfile,
                                                                        results=csv_results,
                                                                        test_keys=test_keys,
                                                                        test_config=test_config,
                                                                        reset_port_enable_list=reset_port_enable_list,
                                                                        reset_port_time_min_list=reset_port_time_min_list,
                                                                        reset_port_time_max_list=reset_port_time_max_list,
                                                                        csv_started=__csv_started,
                                                                        side_a_tx_min_bps=side_a_tx_min_bps,
                                                                        side_a_tx_max_bps=0,
                                                                        side_a_min_pdu=controller_pdu,
                                                                        side_a_max_pdu=0,
                                                                        side_b_tx_min_bps=side_b_tx_min_bps,
                                                                        side_b_tx_max_bps=0,
                                                                        side_b_min_pdu=controller_pdu,
                                                                        side_b_max_pdu=0,
                                                                        number_template="00",
                                                                        test_duration=args.test_duration,
                                                                        polling_interval=args.polling_interval,
                                                                        lfclient_host=args.mgr,
                                                                        lfclient_port=lfjson_port)
                                                                    __csv_started = True
                                                                    ip_var_test.pre_cleanup()
                                                                    ip_var_test.build()
                                                                    if not ip_var_test.passes():
                                                                        logg.info("build step failed.")
                                                                        logg.info(ip_var_test.get_fail_message())
                                                                        exit(1)
                                                                    ip_var_test.start(False, False)
                                                                    ip_var_test.stop()
                                                                    if not ip_var_test.passes():
                                                                        logg.info("stop test failed")
                                                                        logg.info(ip_var_test.get_fail_message())
                                                                    # clean up 
                                                                    radio_name_list = []
                                                                    number_of_stations_per_radio_list = []
                                                                    ssid_list = []
                                                                    ssid_password_list = []
                                                                    ssid_security_list = []
                                                                    wifimode_list = []
                                                                    ip_var_test.cleanup()
                                                                    if args.no_stations:
                                                                        pass
                                                                    else:
                                                                        ip_var_test.passes()
                                                                        logg.info(
                                                                            "Full test passed, all connections increased rx rate")
    ##########################################  
    #
    # Build Results
    #
    ##########################################
    if args.csv_outfile:
        logg.info("Report CSV Details: {}".format(csv_outfile))
        logg.info("Report CSV Results: {}".format(csv_results))
        report.set_title("Scaling And Performance")
        report.build_banner()
        report.set_table_title("Scaling And Performance Throughput")
        report.build_table_title()
        report.set_table_dataframe_from_csv(csv_results)
        report.build_table()
        report.write_html()
        report.write_pdf(_page_size='A3', _orientation='Landscape')

    if args.log:
        logg.info("output_log: {}".format(outfile_log))

    # TODO:  Check pass/fail and do exit code accordingly.

if __name__ == "__main__":
    main()
