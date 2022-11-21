#!/usr/bin/env python3
"""
Note: To Run this script gui should be opened with

    path: cd LANforgeGUI_5.4.3 (5.4.3 can be changed with GUI version)
          pwd (Output : /home/lanforge/LANforgeGUI_5.4.3)
          ./lfclient.bash -cli-socket 3990

This script is used to automate running Rate-vs-Range tests.  You
may need to view a Rate-vs-Range test configured through the GUI to understand
the options and how best to input data.

    ./lf_rvr_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \
      --instance_name rvr-instance --config_name test_con --upstream 1.1.eth1 \
      --dut RootAP --duration 15s --station 1.1.wlan0 \
      --download_speed 85% --upload_speed 56Kbps \
      --raw_line 'pkts: MTU' \
      --raw_line 'directions: DUT Transmit' \
      --raw_line 'traffic_types: TCP' \
      --test_rig Ferndale-Mesh-01 --pull_report \
      --raw_line 'attenuator: 1.1.1040' \
      --raw_line 'attenuations: 0..+50..950' \
      --raw_line 'attenuator_mod: 3' \
      --influx_host c7-graphana --influx_port 8086 --influx_org Candela \
      --influx_token=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ== \
      --influx_bucket ben \
      --influx_tag testbed Ferndale-Mesh

Note:
    attenuator_mod: selects the attenuator modules, bit-field.
       This example uses 3, which is first two attenuator modules on Attenuator ID 1040.

    --raw_line 'line contents' will add any setting to the test config.  This is
        useful way to support any options not specifically enabled by the
        command options.
    --set modifications will be applied after the other config has happened,
        so it can be used to override any other config.

Example of raw text config for Rate-vsRange, to show other possible options:

sel_port-0: 1.1.wlan0
show_events: 1
show_log: 0
port_sorting: 0
kpi_id: Rate vs Range
bg: 0xE0ECF8
test_rig:
show_scan: 1
auto_helper: 0
skip_2: 0
skip_5: 0
skip_5b: 1
skip_dual: 0
skip_tri: 1
selected_dut: RootAP
duration: 15000
traffic_port: 1.1.6 wlan0
upstream_port: 1.1.1 eth1
path_loss: 10
speed: 85%
speed2: 56Kbps
min_rssi_bound: -150
max_rssi_bound: 0
channels: AUTO
modes: Auto
pkts: MTU
spatial_streams: AUTO
security_options: AUTO
bandw_options: AUTO
traffic_types: TCP
directions: DUT Transmit
txo_preamble: OFDM
txo_mcs: 0 CCK, OFDM, HT, VHT
txo_retries: No Retry
txo_sgi: OFF
txo_txpower: 15
attenuator: 1.1.1040
attenuator2: 0
attenuator_mod: 243
attenuator_mod2: 255
attenuations: 0..+50..950
attenuations2: 0..+50..950
chamber: 0
tt_deg: 0..+45..359
cust_pkt_sz:
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
import importlib
import argparse
import time
import json
import logging
import subprocess
from time import sleep
from os import path


if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

cv_test_manager = importlib.import_module("py-json.cv_test_manager")
cvtest = cv_test_manager.cv_test
cv_add_base_parser = cv_test_manager.cv_add_base_parser
cv_base_adjust_parser = cv_test_manager.cv_base_adjust_parser

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")

logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

class RvrTest(cvtest):
    def __init__(self,
                 lf_host="localhost",
                 lf_port=8080,
                 ssh_port=22,
                 local_lf_report_dir="",
                 graph_groups=None,
                 lf_user="lanforge",
                 lf_password="lanforge",
                 instance_name="rvr_instance",
                 config_name="rvr_config",
                 upstream="1.1.eth1",
                 pull_report=False,
                 load_old_cfg=False,
                 upload_speed="0",
                 download_speed="85%",
                 duration="15s",
                 station="1.1.wlan0",
                 dut="NA",
                 enables=[],
                 disables=[],
                 raw_lines=[],
                 raw_lines_file="",
                 sets=[],
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
        self.test_name = "Rate vs Range"
        self.upload_speed = upload_speed
        self.download_speed = download_speed
        self.enables = enables
        self.disables = disables
        self.raw_lines = raw_lines
        self.raw_lines_file = raw_lines_file
        self.sets = sets
        self.ssh_port = ssh_port
        self.graph_groups = graph_groups
        self.local_lf_report_dir = local_lf_report_dir

    def setup(self):
        # Nothing to do at this time.
        return

    def run(self):
        self.sync_cv()
        time.sleep(2)
        self.sync_cv()

        blob_test = "rvr-test-latest-"

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
                                 cv_cmds, ssh_port=self.ssh_port, local_lf_report_dir=self.local_lf_report_dir,
                                 graph_groups_file=self.graph_groups)
        self.rm_text_blob(self.config_name, blob_test)  # To delete old config with same name


def main():
    parser = argparse.ArgumentParser(
        prog="lf_rvr_test.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
    Open this file in an editor and read the top notes for more details.

    Example:

    ./lf_rvr_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \\
      --instance_name rvr-instance --config_name test_con --upstream 1.1.eth1 \\
      --dut RootAP --duration 15s --station 1.1.wlan0 \\
      --download_speed 85% --upload_speed 56Kbps \\
      --raw_line 'pkts: MTU' \\
      --raw_line 'directions: DUT Transmit' \\
      --raw_line 'traffic_types: TCP' \\
      --test_rig Ferndale-Mesh-01 --pull_report \\
      --raw_line 'attenuator: 1.1.1040' \\
      --raw_line 'attenuations: 0..+50..950' \\
      --raw_line 'attenuator_mod: 3' \\
      --influx_host c7-graphana --influx_port 8086 --influx_org Candela \\
      --influx_token=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ== \\
      --influx_bucket ben \\
      --influx_tag testbed Ferndale-Mesh

    ./lf_rvr_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \\
      --instance_name rvr-instance --config_name test_con --upstream 1.1.eth1 \\
      --dut RootAP --duration 15s --station 1.1.wlan0 \\
      --download_speed 85% --upload_speed 56Kbps \\
      --raw_line 'pkts: MTU' \\
      --raw_line 'directions: DUT Transmit' \\
      --raw_line 'traffic_types: TCP' \\
      --test_rig Ferndale-Mesh-01 --pull_report \\
      --raw_line 'attenuator: 1.1.1040' \\
      --raw_line 'attenuations: 0..+50..950' \\
      --raw_line 'attenuator_mod: 3' \\
      --pull_report \\
      --local_lf_report_dir /tmp/rvr-report \\
      --raw_line 'notes0: my rvr notes' \\
      --raw_line 'notes1: are here.' \\
      --raw_line 'rvr_bringup_wait: 30000' \\
      --raw_line 'first_byte_wait: 30000'

    To create a station 
        --create_station
        --band 5g
        --radio wiphy1
        --ssid asus_5g
        --ssidpw lf_asus_5g
        --bssid f0:2f:74:c7:a2:04
        --security wpa2

      """
                                     )
    # more command line args in py-json/cv_test_manager.py 
    cv_add_base_parser(parser)  # see cv_test_manager.py

    parser.add_argument("-u", "--upstream", type=str, default="",
                        help="Upstream port for wifi capacity test ex. 1.1.eth2")
    parser.add_argument("--station", type=str, default="", help="Station to be used in this test, example: 1.1.sta01500")

    # LANforge station configuration 
    parser.add_argument("--band", type=str, help="band testing --band 6g", choices=["5g", "24g", "6g", "dual_band_5g", "dual_band_6g"], default='5g')
    parser.add_argument("--radio", type=str, help="[LANforge station configuration] LANforge radio station created on --radio wiphy0")
    parser.add_argument("--create_station", help="[LANforge station configuration] create LANforge station at the beginning of the test", action='store_true')
    parser.add_argument("--ssid", type=str, help="[station configuration] station ssid, ssid of station must match the wlan created --ssid 6G-wpa3-AP3", required=True)
    parser.add_argument("--ssidpw", "--security_key", dest='ssidpw', type=str, help="[station configuration]  station security key --ssidpw hello123", required=True)
    parser.add_argument("--bssid", "--ap_bssid", dest='bssid', type=str, help="[station configuration]  station AP bssid ", required=True)
    parser.add_argument("--security", type=str, help="[station configuration] security type open wpa wpa2 wpa3", required=True)
    parser.add_argument("--wifi_mode", type=str, help="[station configuration] --wifi_mode auto  types auto|a|abg|abgn|abgnAC|abgnAX|an|anAC|anAX|b|bg|bgn|bgnAC|bgnAX|g ", default='auto')
    parser.add_argument("--vht160", action='store_true', help="[station configuration] --vht160 , Enable VHT160 in lanforge ")
    parser.add_argument("--ieee80211w", type=str, help="[station configuration] --ieee80211w 0 (Disabled) 1 (Optional) 2 (Required) (Required needs to be set to Required for 6g and wpa3 default Optional ", default='1')

    parser.add_argument("--dut", default="",
                        help="Specify DUT used by this test, example: linksys-8450")
    parser.add_argument("--download_speed", default="",
                        help="Specify requested download speed.  Percentage of theoretical is also supported.  Default: 85")
    parser.add_argument("--upload_speed", default="",
                        help="Specify requested upload speed.  Percentage of theoretical is also supported.  Default: 0")
    parser.add_argument("--duration", default="",
                        help="Specify duration of each traffic run")
    parser.add_argument("--graph_groups", help="File to save graph_groups to", default=None)
    parser.add_argument("--report_dir", default="")
    parser.add_argument("--local_lf_report_dir", help="--local_lf_report_dir <where to pull reports to>  default '' put where dataplane script run from",default="")
    parser.add_argument('--log_level', default=None, help='Set logging level: debug | info | warning | error | critical')
    # logging configuration
    parser.add_argument("--lf_logger_config_json", help="--lf_logger_config_json <json file> , json configuration of logger")

    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    if args.log_level:
        logger_config.set_level(level=args.log_level)

    # lf_logger_config_json will take presidence to changing debug levels
    if args.lf_logger_config_json:
        # logger_config.lf_logger_config_json = "lf_logger_config.json"
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()

    cv_base_adjust_parser(args)
    

    # The script has the ability to create a station if one does not exist
    if (args.create_station):
    # go up one directory to run perl 
    # TODO use lanforge_api
        shelf, resource, station_name, *nil = LFUtils.name_to_eid(args.station)

        cwd = os.getcwd()
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)

        if (args.radio is None):
            logger.info("WARNING --create needs a radio")
            close_workbook(workbook)
            exit(1)
        if (args.band == '6g' or args.band == 'dual_band_6g'):
            if (args.vht160):
                logger.info("creating station with VHT160 set: {} on radio {}".format(station_name, args.radio))
                logger.info("cwd lf_associate_ap.pl: {dir}".format(dir=os.getcwd()))
                subprocess.run(["./lf_associate_ap.pl", "--mgr", args.mgr, "--radio", args.radio, "--ssid", args.ssid, "--passphrase", args.ssidpw, "--bssid", args.bssid,
                                "--security", args.security, "--upstream", args.upstream, "--first_ip", "DHCP",
                                "--first_sta", station_name, "--ieee80211w", args.ieee80211w, "--wifi_mode", args.wifi_mode, "--action", "add", "--xsec", "ht160_enable"], timeout=20, capture_output=True)
                sleep(3)
            else:
                logger.info("creating station: {} on radio {}".format(station_name, args.radio))
                subprocess.run(["./lf_associate_ap.pl", "--mgr", args.mgr, "--radio", args.radio, "--ssid", args.ssid, "--passphrase", args.ssidpw, "--bssid", args.bssid,
                                "--security", args.security, "--upstream", args.upstream, "--first_ip", "DHCP",
                                "--first_sta", station_name, "--ieee80211w", args.ieee80211w, "--wifi_mode", args.wifi_mode, "--action", "add"], timeout=20, capture_output=True)

        else:
            if (args.vht160):
                logger.info("creating station with VHT160 set: {} on radio {}".format(station_name, args.radio))
                subprocess.run(["./lf_associate_ap.pl", "--mgr", args.mgr, "--radio", args.radio, "--ssid", args.ssid, "--passphrase", args.ssidpw, "--bssid", args.bssid,
                                "--security", args.security, "--upstream", args.upstream, "--first_ip", "DHCP",
                                "--first_sta", station_name, "--ieee80211w", args.ieee80211w, "--wifi_mode", args.wifi_mode, "--action", "add", "--xsec", "ht160_enable"], timeout=20, capture_output=False)
                sleep(3)
            else:
                logger.info("creating station: {} on radio {}".format(station_name, args.radio))
                subprocess.run(["./lf_associate_ap.pl", "--mgr", args.mgr, "--radio", args.radio, "--ssid", args.ssid, "--passphrase", args.ssidpw, "--bssid", args.bssid,
                                "--security", args.security, "--upstream", args.upstream, "--first_ip", "DHCP",
                                "--first_sta", station_name, "--ieee80211w", args.ieee80211w, "--wifi_mode", args.wifi_mode, "--action", "add"], timeout=20, capture_output=False)
        sleep(3)
        # change back to the currentl workin directory
        os.chdir(cwd)



    CV_Test = RvrTest(lf_host=args.mgr,
                      lf_port=args.port,
                      lf_user=args.lf_user,
                      lf_password=args.lf_password,
                      instance_name=args.instance_name,
                      config_name=args.config_name,
                      upstream=args.upstream,
                      pull_report=args.pull_report,
                      local_lf_report_dir = args.local_lf_report_dir,
                      load_old_cfg=args.load_old_cfg,
                      download_speed=args.download_speed,
                      upload_speed=args.upload_speed,
                      duration=args.duration,
                      dut=args.dut,
                      station=args.station,
                      enables=args.enable,
                      disables=args.disable,
                      raw_lines=args.raw_line,
                      raw_lines_file=args.raw_lines_file,
                      sets=args.set,
                      graph_groups=args.graph_groups
                      )
    CV_Test.setup()
    CV_Test.run()

    CV_Test.check_influx_kpi(args)


if __name__ == "__main__":
    main()

