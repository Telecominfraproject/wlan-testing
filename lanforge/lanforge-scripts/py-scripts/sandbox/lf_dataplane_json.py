#!/usr/bin/env python3

"""
Note: To Run this script gui should be opened with

    path: cd LANforgeGUI_5.4.3 (5.4.3 can be changed with GUI version)
          pwd (Output : /home/lanforge/LANforgeGUI_5.4.3)
          ./lfclient.bash -cli-socket 3990

This script is used to automate running Dataplane tests.  You
may need to view a Dataplane test configured through the GUI to understand
the options and how best to input data.
    
    ./lf_dataplane_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \
      --instance_name dataplane-instance --config_name test_con --upstream 1.1.eth2 \
      --dut linksys-8450 --duration 15s --station 1.1.sta01500 \
      --download_speed 85% --upload_speed 0 \
      --raw_line 'pkts: Custom;60;142;256;512;1024;MTU' \
      --raw_line 'cust_pkt_sz: 88 1200' \
      --raw_line 'directions: DUT Transmit;DUT Receive' \
      --raw_line 'traffic_types: UDP;TCP' \
      --test_rig Testbed-01 --pull_report \
      --influx_host c7-graphana --influx_port 8086 --influx_org Candela \
      --influx_token=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ== \
      --influx_bucket ben \
      --influx_tag testbed Ferndale-01

Note:
    --raw_line 'line contents' will add any setting to the test config.  This is
        useful way to support any options not specifically enabled by the
        command options.
    --set modifications will be applied after the other config has happened,
        so it can be used to override any other config.

Example of raw text config for Dataplane, to show other possible options:

show_events: 1
show_log: 0
port_sorting: 0
kpi_id: Dataplane Pkt-Size
notes0: ec5211 in bridge mode, wpa2 auth.
bg: 0xE0ECF8
test_rig: 
show_scan: 1
auto_helper: 0
skip_2: 0
skip_5: 0
skip_5b: 1
skip_dual: 0
skip_tri: 1
selected_dut: ea8300
duration: 15000
traffic_port: 1.1.157 sta01500
upstream_port: 1.1.2 eth2
path_loss: 10
speed: 85%
speed2: 0Kbps
min_rssi_bound: -150
max_rssi_bound: 0
channels: AUTO
modes: Auto
pkts: Custom;60;142;256;512;1024;MTU
spatial_streams: AUTO
security_options: AUTO
bandw_options: AUTO
traffic_types: UDP;TCP
directions: DUT Transmit;DUT Receive
txo_preamble: OFDM
txo_mcs: 0 CCK, OFDM, HT, VHT
txo_retries: No Retry
txo_sgi: OFF
txo_txpower: 15
attenuator: 0
attenuator2: 0
attenuator_mod: 255
attenuator_mod2: 255
attenuations: 0..+50..950
attenuations2: 0..+50..950
chamber: 0
tt_deg: 0..+45..359
cust_pkt_sz: 88 1200
show_bar_labels: 1
show_prcnt_tput: 0
show_3s: 0
show_ll_graphs: 0
show_gp_graphs: 1
show_1m: 1
pause_iter: 0
outer_loop_atten: 0
show_realtime: 1
operator: 
mconn: 1
mpkt: 1000
tos: 0
loop_iterations: 1

"""

import sys
import os
import argparse
import time
import json
from os import path

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append(os.path.join(os.path.abspath('..'), 'py-json'))

from cv_test_manager import cv_test
from cv_test_manager import *


class DataplaneTest(cv_test):
    def __init__(self,
                 lf_host="localhost",
                 lf_port=8080,
                 lf_user="lanforge",
                 lf_password="lanforge",
                 ssh_port=22,
                 local_path="",
                 instance_name="dpt_instance",
                 config_name="dpt_config",
                 upstream="1.1.eth2",
                 pull_report=False,
                 load_old_cfg=False,
                 upload_speed="0",
                 download_speed="85%",
                 duration="15s",
                 station="1.1.sta01500",
                 dut="NA",
                 enables=[],
                 disables=[],
                 raw_lines=[],
                 raw_lines_file="",
                 sets=[],
                 graph_groups=None,
                 report_dir=""
                 ):
        super().__init__(lfclient_host=lf_host, lfclient_port=lf_port)

        self.lf_host = lf_host
        self.lf_port = lf_port
        self.lf_user = lf_user
        self.lf_password = lf_password
        self.instance_name = instance_name
        self.config_name = config_name
        self.dut = dut
        self.duration = duration
        self.upstream = upstream
        self.station = station
        self.pull_report = pull_report
        self.load_old_cfg = load_old_cfg
        self.test_name = "Dataplane"
        self.upload_speed = upload_speed
        self.download_speed = download_speed
        self.enables = enables
        self.disables = disables
        self.raw_lines = raw_lines
        self.raw_lines_file = raw_lines_file
        self.sets = sets
        self.graph_groups = graph_groups
        self.report_dir = report_dir
        self.ssh_port = ssh_port
        self.local_path = local_path

    def setup(self):
        # Nothing to do at this time.
        return

    def run(self):
        self.sync_cv()
        time.sleep(2)
        self.sync_cv()

        blob_test = "dataplane-test-latest-"

        self.rm_text_blob(self.config_name, blob_test)  # To delete old config with same name
        self.show_text_blob(None, None, False)

        # Test related settings
        cfg_options = []

        ### HERE###
        self.apply_cfg_options(cfg_options, self.enables, self.disables, self.raw_lines, self.raw_lines_file)

        # cmd line args take precedence and so come last in the cfg array.
        if self.upstream != "":
            cfg_options.append("upstream_port: " + self.upstream)
        if self.station != "":
            cfg_options.append("traffic_port: " + self.station)
        if self.download_speed != "":
            cfg_options.append("speed: " + self.download_speed)
        if self.upload_speed != "":
            cfg_options.append("speed2: " + self.upload_speed)
        if self.duration != "":
            cfg_options.append("duration: " + self.duration)
        if self.dut != "":
            cfg_options.append("selected_dut: " + self.dut)

        # We deleted the scenario earlier, now re-build new one line at a time.

        self.build_cfg(self.config_name, blob_test, cfg_options)

        cv_cmds = []
        self.create_and_run_test(self.load_old_cfg, self.test_name, self.instance_name,
                                 self.config_name, self.sets,
                                 self.pull_report, self.lf_host, self.lf_user, self.lf_password,
                                 cv_cmds, ssh_port=self.ssh_port, local_path=self.local_path,
                                 graph_groups_file=self.graph_groups)
        self.rm_text_blob(self.config_name, blob_test)  # To delete old config with same name


def main():
    parser = argparse.ArgumentParser("""
    Open this file in an editor and read the top notes for more details.

    Example:

    ./lf_dataplane_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \
      --instance_name dataplane-instance --config_name test_con --upstream 1.1.eth2 \
      --dut linksys-8450 --duration 15s --station 1.1.sta01500 \
      --download_speed 85% --upload_speed 0 \
      --raw_line 'pkts: Custom;60;142;256;512;1024;MTU' \
      --raw_line 'cust_pkt_sz: 88 1200' \
      --raw_line 'directions: DUT Transmit;DUT Receive' \
      --raw_line 'traffic_types: UDP;TCP' \
      --test_rig Testbed-01 --pull_report \
      --influx_host c7-graphana --influx_port 8086 --influx_org Candela \
      --influx_token=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ== \
      --influx_bucket ben \
      --influx_tag testbed Ferndale-01
    
      """
                                     )

    cv_add_base_parser(parser)  # see cv_test_manager.py

    parser.add_argument('--json', help="--json <config.json> json input file", default="")
    parser.add_argument("-u", "--upstream", type=str, default="",
                        help="Upstream port for wifi capacity test ex. 1.1.eth2")
    parser.add_argument("--station", type=str, default="",
                        help="Station to be used in this test, example: 1.1.sta01500")

    parser.add_argument("--dut", default="",
                        help="Specify DUT used by this test, example: linksys-8450")
    parser.add_argument("--download_speed", default="",
                        help="Specify requested download speed.  Percentage of theoretical is also supported.  Default: 85%")
    parser.add_argument("--upload_speed", default="",
                        help="Specify requested upload speed.  Percentage of theoretical is also supported.  Default: 0")
    parser.add_argument("--duration", default="",
                        help="Specify duration of each traffic run")
    parser.add_argument("--graph_groups", help="File to save graph_groups to", default=None)
    parser.add_argument("--report_dir", default="")

    args = parser.parse_args()

    # TODO
    if args.json != "":
        try:
            with open(args.json, 'r') as json_config:
                json_data = json.load(json_config)
        except:
            print("Error reading {}".format(args.json))
        # json configuation takes presidence to command line 
        # TODO see if there is easier way to search presence, look at parser args
        if "mgr" in json_data:
            args.mgr = json_data["mgr"]
        if "port" in json_data:
            args.port = json_data["port"]
        if "lf_user" in json_data:
            args.lf_user = json_data["lf_user"]
        if "lf_password" in json_data:
            args.lf_password = json_data["lf_password"]
        if "instance_name" in json_data:
            args.instance_name = json_data["instance_name"]
        if "config_name" in json_data:
            args.config_name = json_data["config_name"]
        if "upstream" in json_data:
            args.upstream = json_data["upstream"]
        if "dut" in json_data:
            args.dut = json_data["dut"]
        if "duration" in json_data:
            args.duration = json_data["duration"]
        if "station" in json_data:
            args.station = json_data["station"]
        if "download_speed" in json_data:
            args.download_speed = json_data["download_speed"]
        if "upload_speed" in json_data:
            args.upload_speed = json_data["upload_speed"]
        if "raw_line" in json_data:
            # the json_data is a list , need to make into a list of lists, to match command line raw_line paramaters
            # https://www.tutorialspoint.com/convert-list-into-list-of-lists-in-python
            json_data_tmp = [[x] for x in json_data["raw_line"]]
            args.raw_line = json_data_tmp

    cv_base_adjust_parser(args)
    print(args)
    #exit(1)

    # if json present use json config will override

    CV_Test = DataplaneTest(lf_host = args.mgr,
                            lf_port = args.port,
                            lf_user = args.lf_user,
                            lf_password = args.lf_password,
                            instance_name = args.instance_name,
                            config_name = args.config_name,
                            upstream = args.upstream,
                            pull_report = args.pull_report,
                            load_old_cfg = args.load_old_cfg,
                            download_speed = args.download_speed,
                            upload_speed = args.upload_speed,
                            duration = args.duration,
                            dut = args.dut,
                            station = args.station,
                            enables = args.enable,
                            disables = args.disable,
                            raw_lines = args.raw_line,  # this is interesting.
                            raw_lines_file = args.raw_lines_file,
                            sets = args.set,
                            graph_groups = args.graph_groups
                            )
    CV_Test.setup()
    CV_Test.run()

    CV_Test.check_influx_kpi(args)


if __name__ == "__main__":
    main()
