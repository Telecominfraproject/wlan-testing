#!/usr/bin/env python3

"""
Note: To Run this script gui should be opened with

    path: cd LANforgeGUI_5.4.3 (5.4.3 can be changed with GUI version)
          pwd (Output : /home/lanforge/LANforgeGUI_5.4.3)
          ./lfclient.bash -cli-socket 3990

This script is used to automate running AP-Auto tests.  You
may need to view an AP Auto test configured through the GUI to understand
the options and how best to input data.
    
    ./lf_ap_auto_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \
      --instance_name ap-auto-instance --config_name test_con --upstream 1.1.eth2 \
      --dut5_0 'linksys-8450 Default-SSID-5gl c4:41:1e:f5:3f:25 (2)' \
      --dut2_0 'linksys-8450 Default-SSID-2g c4:41:1e:f5:3f:24 (1)' \
      --max_stations_2 100 --max_stations_5 100 --max_stations_dual 200 \
      --radio2 1.1.wiphy0 --radio2 1.1.wiphy2 \
      --radio5 1.1.wiphy1 --radio5 1.1.wiphy3 --radio5 1.1.wiphy4 \
      --radio5 1.1.wiphy5 --radio5 1.1.wiphy6 --radio5 1.1.wiphy7 \
      --set 'Basic Client Connectivity' 1 --set 'Multi Band Performance' 1 \
      --set 'Skip 2.4Ghz Tests' 1 --set 'Skip 5Ghz Tests' 1 \
      --set 'Throughput vs Pkt Size' 0 --set 'Capacity' 0 --set 'Stability' 0 --set 'Band-Steering' 0 \
      --set 'Multi-Station Throughput vs Pkt Size' 0 --set 'Long-Term' 0 \
      --pull_report \
      --influx_host c7-graphana --influx_port 8086 --influx_org Candela \
      --influx_token=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ== \
      --influx_bucket ben \
      --influx_tag testbed Ferndale-01

Note:
    --enable [option] will attempt to select any checkbox of that name to true.
    --disable [option] will attempt to un-select any checkbox of that name to true.
    --raw_line 'line contents' will add any setting to the test config.  This is
        useful way to support any options not specifically enabled by the
        command options.
    --set modifications will be applied after the other config has happened,
        so it can be used to override any other config.

Example of raw text config for ap-auto, to show other possible options:

sel_port-0: 1.1.sta00500
show_events: 1
show_log: 0
port_sorting: 0
kpi_id: AP Auto
bg: 0xE0ECF8
show_scan: 1
auto_helper: 1
skip_2: 1
skip_5: 1
skip_5b: 1
skip_dual: 0
skip_tri: 1
dut5b-0: NA
dut5-0: linksys-8450 Default-SSID-5gl c4:41:1e:f5:3f:25 (2)
dut2-0: linksys-8450 Default-SSID-2g c4:41:1e:f5:3f:24 (1)
dut5b-1: NA
dut5-1: NA
dut2-1: NA
dut5b-2: NA
dut5-2: NA
dut2-2: NA
spatial_streams: AUTO
bandw_options: AUTO
modes: Auto
upstream_port: 1.1.2 eth2
operator: 
mconn: 1
tos: 0
vid_buf: 1000000
vid_speed: 700000
reset_stall_thresh_udp_dl: 9600
cx_prcnt: 950000
cx_open_thresh: 35
cx_psk_thresh: 75
cx_1x_thresh: 130
reset_stall_thresh_udp_ul: 9600
reset_stall_thresh_tcp_dl: 9600
reset_stall_thresh_tcp_ul: 9600
reset_stall_thresh_l4: 100000
reset_stall_thresh_voip: 20000
stab_mcast_dl_min: 100000
stab_mcast_dl_max: 0
stab_udp_dl_min: 56000
stab_udp_dl_max: 0
stab_udp_ul_min: 56000
stab_udp_ul_max: 0
stab_tcp_dl_min: 500000
stab_tcp_dl_max: 0
stab_tcp_ul_min: 500000
stab_tcp_ul_max: 0
dl_speed: 85%
ul_speed: 85%
max_stations_2: 100
max_stations_5: 100
max_stations_5b: 64
max_stations_dual: 200
max_stations_tri: 64
lt_sta: 2
voip_calls: 0
lt_dur: 3600
reset_dur: 600
lt_gi: 30
dur20: 20
hunt_retries: 1
hunt_iter: 15
bind_bssid: 1
set_txpower_default: 0
cap_dl: 1
cap_ul: 0
cap_use_pkt_sizes: 0
stability_reset_radios: 0
stability_use_pkt_sizes: 0
pkt_loss_thresh: 10000
frame_sizes: 200, 512, 1024, MTU
capacities: 1, 2, 5, 10, 20, 40, 64, 128, 256, 512, 1024, MAX
pf_text0: 2.4 DL 200 70Mbps
pf_text1: 2.4 DL 512 110Mbps
pf_text2: 2.4 DL 1024 115Mbps
pf_text3: 2.4 DL MTU 120Mbps
pf_text4: 
pf_text5: 2.4 UL 200 88Mbps
pf_text6: 2.4 UL 512 106Mbps
pf_text7: 2.4 UL 1024 115Mbps
pf_text8: 2.4 UL MTU 120Mbps
pf_text9: 
pf_text10: 5 DL 200 72Mbps
pf_text11: 5 DL 512 185Mbps
pf_text12: 5 DL 1024 370Mbps
pf_text13: 5 DL MTU 525Mbps
pf_text14: 
pf_text15: 5 UL 200 90Mbps
pf_text16: 5 UL 512 230Mbps
pf_text17: 5 UL 1024 450Mbps
pf_text18: 5 UL MTU 630Mbps
radio2-0: 1.1.4 wiphy0
radio2-1: 1.1.6 wiphy2
radio5-0: 1.1.5 wiphy1
radio5-1: 1.1.7 wiphy3
radio5-2: 1.1.8 wiphy4
radio5-3: 1.1.9 wiphy5
radio5-4: 1.1.10 wiphy6
radio5-5: 1.1.11 wiphy7
basic_cx: 0
tput: 0
tput_multi: 0
tput_multi_tcp: 1
tput_multi_udp: 1
tput_multi_dl: 1
tput_multi_ul: 1
dual_band_tput: 1
capacity: 0
band_steering: 0
longterm: 0
mix_stability: 0
loop_iter: 1
reset_batch_size: 1
reset_duration_min: 10000
reset_duration_max: 60000
bandsteer_always_5g: 0

"""
import sys
import os
import importlib
import argparse
import time
import logging

logger = logging.getLogger(__name__)

if sys.version_info[0] != 3:
    logger.critical("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

cv_test_manager = importlib.import_module("py-json.cv_test_manager")
cvtest = cv_test_manager.cv_test
cv_add_base_parser = cv_test_manager.cv_add_base_parser
cv_base_adjust_parser = cv_test_manager.cv_base_adjust_parser
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

class ApAutoTest(cvtest):
    def __init__(self,
                 lf_host="localhost",
                 lf_port=8080,
                 lf_user="lanforge",
                 lf_password="lanforge",
                 ssh_port=22,
                 local_lf_report_dir=None,
                 lf_report_dir=None,
                 instance_name="ap_auto_instance",
                 config_name="ap_auto_config",
                 upstream=None,
                 pull_report=False,
                 dut5_0="NA",
                 dut2_0="NA",
                 load_old_cfg=False,
                 max_stations_2=100,
                 max_stations_5=100,
                 max_stations_dual=200,
                 radio2=None,
                 radio5=None,
                 enables=None,
                 disables=None,
                 raw_lines=None,
                 raw_lines_file="",
                 sets=None,
                 graph_groups=None,
                 debug=False,
                 test_tag=""
                 ):
        super().__init__(lfclient_host=lf_host, lfclient_port=lf_port, debug_=debug)

        if radio2 is None:
            radio2 = []
        if radio5 is None:
            radio5 = []
        if enables is None:
            enables = []
        if disables is None:
            disables = []
        if raw_lines is None:
            raw_lines = []
        if sets is None:
            sets = []
        self.lf_host = lf_host
        self.lf_port = lf_port
        self.lf_user = lf_user
        self.lf_password = lf_password
        self.instance_name = instance_name
        self.config_name = config_name
        self.upstream = upstream
        self.pull_report = pull_report
        self.load_old_cfg = load_old_cfg
        self.test_name = "AP-Auto"
        self.dut5_0 = dut5_0
        self.dut2_0 = dut2_0
        self.max_stations_2 = max_stations_2
        self.max_stations_5 = max_stations_5
        self.max_stations_dual = max_stations_dual
        self.radio2 = radio2
        self.radio5 = radio5
        self.enables = enables
        self.disables = disables
        self.raw_lines = raw_lines
        self.raw_lines_file = raw_lines_file
        self.sets = sets
        self.ssh_port = ssh_port
        self.graph_groups = graph_groups
        self.lf_report_dir = lf_report_dir
        self.local_lf_report_dir = local_lf_report_dir
        self.test_tag = test_tag

    def setup(self):
        # Nothing to do at this time.
        return

    def run(self):
        self.sync_cv()
        time.sleep(2)
        self.sync_cv()

        blob_test = "%s-" % self.test_name

        self.rm_text_blob(self.config_name, blob_test)  # To delete old config with same name
        self.show_text_blob(None, None, False)

        # Test related settings
        cfg_options = []

        ridx = 0
        for r in self.radio2:
            cfg_options.append("radio2-%i: %s" % (ridx, r[0]))
            ridx += 1

        ridx = 0
        for r in self.radio5:
            cfg_options.append("radio5-%i: %s" % (ridx, r[0]))
            ridx += 1

        self.apply_cfg_options(cfg_options, self.enables, self.disables, self.raw_lines, self.raw_lines_file)

        # Command line args take precedence.
        if self.upstream:
            cfg_options.append("upstream_port: %s" % self.upstream)
        if self.dut5_0 != "":
            cfg_options.append("dut5-0: " + self.dut5_0)
        if self.dut2_0 != "":
            cfg_options.append("dut2-0: " + self.dut2_0)
        if self.max_stations_2 != -1:
            cfg_options.append("max_stations_2: " + str(self.max_stations_2))
        if self.max_stations_5 != -1:
            cfg_options.append("max_stations_5: " + str(self.max_stations_5))
        if self.max_stations_dual != -1:
            cfg_options.append("max_stations_dual: " + str(self.max_stations_dual))
        if self.test_tag != "":
            cfg_options.append("test_tag: " + self.test_tag)

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
        prog="lf_ap_auto_test.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
    Open this file in an editor and read the top notes for more details.
    
    Example:
    ./lf_ap_auto_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \\
      --instance_name ap-auto-instance --config_name test_con --upstream 1.1.eth2 \\
      --dut5_0 'linksys-8450 Default-SSID-5gl c4:41:1e:f5:3f:25 (2)' \\
      --dut2_0 'linksys-8450 Default-SSID-2g c4:41:1e:f5:3f:24 (1)' \\
      --max_stations_2 100 --max_stations_5 100 --max_stations_dual 200 \\
      --radio2 1.1.wiphy0 --radio2 1.1.wiphy2 \\
      --radio5 1.1.wiphy1 --radio5 1.1.wiphy3 --radio5 1.1.wiphy4 \\
      --radio5 1.1.wiphy5 --radio5 1.1.wiphy6 --radio5 1.1.wiphy7 \\
      --set 'Basic Client Connectivity' 1 --set 'Multi Band Performance' 1 \\
      --set 'Skip 2.4Ghz Tests' 1 --set 'Skip 5Ghz Tests' 1 \\
      --set 'Throughput vs Pkt Size' 0 --set 'Capacity' 0 --set 'Stability' 0 --set 'Band-Steering' 0 \\
      --set 'Multi-Station Throughput vs Pkt Size' 0 --set 'Long-Term' 0 \\
      --test_rig Testbed-01 --test_tag ATH10K --pull_report \\
      --influx_host c7-graphana --influx_port 8086 --influx_org Candela \\
      --influx_token=-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ== \\
      --influx_bucket ben \\
      --influx_tag testbed Ferndale-01
      """
    )
    cv_add_base_parser(parser)  # see cv_test_manager.py

    parser.add_argument("-u", "--upstream", type=str, default=None,
                        help="Upstream port for wifi capacity test ex. 1.1.eth1")

    parser.add_argument("--max_stations_2", type=int, default=-1,
                        help="Specify maximum 2.4Ghz stations")
    parser.add_argument("--max_stations_5", type=int, default=-1,
                        help="Specify maximum 5Ghz stations")
    parser.add_argument("--max_stations_dual", type=int, default=-1,
                        help="Specify maximum stations for dual-band tests")
    parser.add_argument("--dut5_0", type=str, default="",
                        help="Specify 5Ghz DUT entry.  Syntax is somewhat tricky:  DUT-name SSID BSID (bssid-idx), example: linksys-8450 Default-SSID-5gl c4:41:1e:f5:3f:25 (2)")
    parser.add_argument("--dut2_0", type=str, default="",
                        help="Specify 5Ghz DUT entry.  Syntax is somewhat tricky:  DUT-name SSID BSID (bssid-idx), example: linksys-8450 Default-SSID-2g c4:41:1e:f5:3f:24 (1)")

    parser.add_argument("--radio2", action='append', nargs=1, default=[],
                        help="Specify 2.4Ghz radio.  May be specified multiple times.")
    parser.add_argument("--radio5", action='append', nargs=1, default=[],
                        help="Specify 5Ghz radio.  May be specified multiple times.")
    parser.add_argument("--local_lf_report_dir",
                        help="--local_lf_report_dir <where to pull reports to>  default '' put where dataplane script run from",
                        default="")
    parser.add_argument("--lf_report_dir",
                        help="--lf_report_dir <where to pull reports from>  default '' put where dataplane script run from",
                        default="")

    # TODO:  Use lfcli_base for common arguments.
    parser.add_argument('--debug', help='Enable debugging', default=False, action="store_true")
    parser.add_argument('--log_level',
                        default=None,
                        help='Set logging level: debug | info | warning | error | critical')
    parser.add_argument('--lf_logger_config_json',
                        help="--lf_logger_config_json <json file> , json configuration of logger")

    args = parser.parse_args()

    logger_config = lf_logger_config.lf_logger_config()
    # set the logger level to requested value
    logger_config.set_level(level=args.log_level)
    logger_config.set_json(json_file=args.lf_logger_config_json)


    cv_base_adjust_parser(args)

    CV_Test = ApAutoTest(lf_host=args.mgr,
                         lf_port=args.port,
                         lf_user=args.lf_user,
                         lf_password=args.lf_password,
                         instance_name=args.instance_name,
                         config_name=args.config_name,
                         upstream=args.upstream,
                         pull_report=args.pull_report,
                         local_lf_report_dir=args.local_lf_report_dir,
                         lf_report_dir=args.lf_report_dir,
                         dut5_0=args.dut5_0,
                         dut2_0=args.dut2_0,
                         load_old_cfg=args.load_old_cfg,
                         max_stations_2=args.max_stations_2,
                         max_stations_5=args.max_stations_5,
                         max_stations_dual=args.max_stations_dual,
                         radio2=args.radio2,
                         radio5=args.radio5,
                         enables=args.enable,
                         disables=args.disable,
                         raw_lines=args.raw_line,
                         raw_lines_file=args.raw_lines_file,
                         sets=args.set,
                         debug=args.debug
                         )
    CV_Test.setup()
    CV_Test.run()

    CV_Test.check_influx_kpi(args)

    if CV_Test.passes():
        CV_Test.exit_success()
    else:
        CV_Test.exit_fail()

if __name__ == "__main__":
    main()
