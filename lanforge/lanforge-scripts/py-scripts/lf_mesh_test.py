#!/usr/bin/env python3

"""
Note: To Run this script gui should be opened with

    path: cd LANforgeGUI_5.4.3 (5.4.3 can be changed with GUI version)
          pwd (Output : /home/lanforge/LANforgeGUI_5.4.3)
          ./lfclient.bash -cli-socket 3990

This script is used to automate running Mesh tests.  You
may need to view a Mesh test configured through the GUI to understand
the options and how best to input data.

    ./lf_mesh_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \
      --instance_name mesh-instance --config_name test_con --upstream 1.1.eth1 \
      --raw_line 'selected_dut2: RootAP wactest 08:36:c9:19:47:40 (1)' \
      --raw_line 'selected_dut5: RootAP wactest 08:36:c9:19:47:50 (2)' \
      --duration 15s \
      --download_speed 85% --upload_speed 56Kbps \
      --raw_line 'velocity: 100' \
      --raw_lines_file example-configs/mesh-ferndale-cfg.txt \
      --test_rig Ferndale-Mesh-01 --pull_report

Note:
    --raw_line 'line contents' will add any setting to the test config.  This is
        useful way to support any options not specifically enabled by the
        command options.
    --set modifications will be applied after the other config has happened,
        so it can be used to override any other config.

Example of raw text config for Mesh, to show other possible options:

show_events: 1
show_log: 0
port_sorting: 0
kpi_id: Mesh
bg: 0xE0ECF8
test_rig:
show_scan: 1
auto_helper: 1
skip_2: 0
skip_5: 0
skip_5b: 1
skip_dual: 0
skip_tri: 1
selected_dut5: RootAP wactest 08:36:c9:19:47:50 (2)
selected_dut2: RootAP wactest 08:36:c9:19:47:40 (1)
upstream_port: 1.1.1 eth1
operator:
mconn: 5
tos: 0
dur: 60
speed: 100%
speed2: 56Kbps
velocity: 100
path_loops: 1
bgscan_mod: simple
bgscan_short: 30
bgscan_long: 300
bgscan_rssi: -60
skip_2: 0
skip_5: 0
skip_dhcp: 0
show_tx_mcs: 1
show_rx_mcs: 1
chamber-0: RootAP
chamber-1: Node1
chamber-2: Node2
chamber-3:
chamber-4: MobileStations
sta_amount-0: 1
sta_amount-1: 1
sta_amount-2: 1
sta_amount-3: 1
sta_amount-4: 1
radios-0-0: 1.2.2 wiphy0
radios-0-1:
radios-0-2:
radios-0-3: 1.2.3 wiphy1
radios-0-4:
radios-0-5:
radios-1-0: 1.3.2 wiphy0
radios-1-1:
radios-1-2:
radios-1-3: 1.3.3 wiphy1
radios-1-4:
radios-1-5:
radios-2-0: 1.4.2 wiphy0
radios-2-1:
radios-2-2:
radios-2-3: 1.4.3 wiphy1
radios-2-4:
radios-2-5:
radios-3-0:
radios-3-1:
radios-3-2:
radios-3-3:
radios-3-4:
radios-3-5:
radios-4-0: 1.1.2 wiphy0
radios-4-1:
radios-4-2:
radios-4-3: 1.1.3 wiphy1
radios-4-4:
radios-4-5:
ap_arrangements: Current Position
tests: Roam
traf_combo: STA
sta_position: Current Position
traffic_types: UDP
direction: Download
path: Orbit Current
traf_use_sta: 0

"""
import sys
import os
import importlib
import argparse
import time

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

cv_test_manager = importlib.import_module("py-json.cv_test_manager")
cvtest = cv_test_manager.cv_test
cv_add_base_parser = cv_test_manager.cv_add_base_parser
cv_base_adjust_parser = cv_test_manager.cv_base_adjust_parser


class MeshTest(cvtest):
    def __init__(self,
                 lf_host="localhost",
                 lf_port=8080,
                 ssh_port=22,
                 local_lf_report_dir="",
                 graph_groups=None,
                 lf_user="lanforge",
                 lf_password="lanforge",
                 instance_name="dpt_instance",
                 config_name="dpt_config",
                 upstream="1.1.eth1",
                 pull_report=False,
                 load_old_cfg=False,
                 upload_speed="56Kbps",
                 download_speed="85%",
                 duration="60s",
                 enables=None,
                 disables=None,
                 raw_lines=None,
                 raw_lines_file="",
                 sets=None,
                 ):
        super().__init__(lfclient_host=lf_host, lfclient_port=lf_port)

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
        self.duration = duration
        self.upstream = upstream
        self.pull_report = pull_report
        self.load_old_cfg = load_old_cfg
        self.test_name = "Mesh"
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

        blob_test = "Mesh-"

        self.rm_text_blob(self.config_name, blob_test)  # To delete old config with same name
        self.show_text_blob(None, None, False)

        # Test related settings
        cfg_options = []

        ### HERE###
        self.apply_cfg_options(cfg_options, self.enables, self.disables, self.raw_lines, self.raw_lines_file)

        # cmd line args take precedence and so come last in the cfg array.
        if self.upstream != "":
            cfg_options.append("upstream_port: " + self.upstream)
        if self.download_speed != "":
            cfg_options.append("speed: " + self.download_speed)
        if self.upload_speed != "":
            cfg_options.append("speed2: " + self.upload_speed)
        if self.duration != "":
            cfg_options.append("duration: " + self.duration)

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
        prog="lf_mesh_test.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
    Open this file in an editor and read the top notes for more details.

    Example:
    ./lf_mesh_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \\
      --instance_name mesh-instance --config_name test_con --upstream 1.1.eth1 \\
      --raw_line 'selected_dut2: RootAP wactest 08:36:c9:19:47:40 (1)' \\
      --raw_line 'selected_dut5: RootAP wactest 08:36:c9:19:47:50 (2)' \\
      --duration 15s \\
      --download_speed 85% --upload_speed 56Kbps \\
      --raw_line 'velocity: 100' \\
      --raw_lines_file example-configs/mesh-ferndale-cfg.txt \\
      --test_rig Ferndale-Mesh-01 --pull_report

      NOTE:  There is quite a lot of config needed, see example-configs/mesh-ferndale-cfg.txt
         Suggestion is to configure the test through the GUI, make sure it works, then view
         the config and paste it into your own cfg.txt file.

      """
    )

    cv_add_base_parser(parser)  # see cv_test_manager.py

    parser.add_argument("-u", "--upstream", type=str, default="",
                        help="Upstream port for wifi capacity test ex. 1.1.eth2")
    # argparse uses the % formatting so use %%
    parser.add_argument("--download_speed", default="",
                        help="Specify requested download speed.  Percentage of theoretical is also supported.  Default: 85%%")
    parser.add_argument("--upload_speed", default="",
                        help="Specify requested upload speed.  Percentage of theoretical is also supported.  Default: 0")
    parser.add_argument("--duration", default="",
                        help="Specify duration of each traffic run")
    parser.add_argument("--graph_groups", help="File to save graph_groups to", default=None)
    parser.add_argument("--report_dir", default="")
    parser.add_argument("--local_lf_report_dir",
                        help="--local_lf_report_dir <where to pull reports to>  default '' put where dataplane script run from",
                        default="")

    args = parser.parse_args()

    cv_base_adjust_parser(args)

    CV_Test = MeshTest(lf_host=args.mgr,
                       lf_port=args.port,
                       lf_user=args.lf_user,
                       lf_password=args.lf_password,
                       instance_name=args.instance_name,
                       config_name=args.config_name,
                       upstream=args.upstream,
                       pull_report=args.pull_report,
                       load_old_cfg=args.load_old_cfg,
                       download_speed=args.download_speed,
                       upload_speed=args.upload_speed,
                       duration=args.duration,
                       enables=args.enable,
                       disables=args.disable,
                       raw_lines=args.raw_line,
                       raw_lines_file=args.raw_lines_file,
                       sets=args.set
                       )
    CV_Test.setup()
    CV_Test.run()

    # Mesh does not do KPI currently.
    # CV_Test.check_influx_kpi(args)


if __name__ == "__main__":
    main()
