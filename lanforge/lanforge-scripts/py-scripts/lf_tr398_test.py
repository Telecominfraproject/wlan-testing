#!/usr/bin/env python3
"""
Note: To Run this script gui should be opened with

    path: cd LANforgeGUI_5.4.3 (5.4.3 can be changed with GUI version)
          pwd (Output : /home/lanforge/LANforgeGUI_5.4.3)
          ./lfclient.bash -cli-socket 3990

This script is used to automate running TR398 tests.  You
may need to view a TR398 test configured through the GUI to understand
the options and how best to input data.
    
    ./lf_tr398_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \
      --instance_name tr398-instance --config_name test_con \
      --upstream 1.2.eth2 \
      --test_rig Testbed-01 --pull_report \
      --local_lf_report_dir=/tmp/my_report \
      --dut5 'TR398-DUT ruckus750-5 4c:b1:cd:18:e8:ec (1)' \
      --dut2 'TR398-DUT ruckus750-2 4c:b1:cd:18:e8:e8 (2)' \
      --raw_lines_file example-configs/tr398-ferndale-ac-cfg.txt \
      --set 'Calibrate Attenuators' 0 \
      --set 'Receiver Sensitivity' 0 \
      --set 'Maximum Connection' 1 \
      --set 'Maximum Throughput' 1 \
      --set 'Airtime Fairness' 0 \
      --set 'Range Versus Rate' 0 \
      --set 'Spatial Consistency' 0 \
      --set 'Multiple STAs Performance' 0 \
      --set 'Multiple Assoc Stability' 0 \
      --set 'Downlink MU-MIMO' 0 \
      --set 'AP Coexistence' 0 \
      --set 'Long Term Stability' 0

Note:
    --raw_line 'line contents' will add any setting to the test config.  This is
        useful way to support any options not specifically enabled by the
        command options.
    --set modifications will be applied after the other config has happened,
        so it can be used to override any other config.  Above, we are disabling many
        of the subtests, and enablign just Maximum Connection and Maximum Throughput
        tests.

    The RSSI values are calibrated, so you will need to run the calibration step and
    call with appropriate values for your particular testbed.  This is loaded from
    example-configs/tr398-ferndale-ac-cfg.txt in this example.
    Contents of that file is a list of raw lines, for instance:

rssi_0_2-0: -26
rssi_0_2-1: -26
rssi_0_2-2: -26
....

Example of raw text config for TR-398, to show other possible options:

show_events: 1
show_log: 0
port_sorting: 0
kpi_id: TR_398
notes0: Standard LANforge TR-398 automation setup, DUT is in large chamber CT840a, LANforge test system is in
notes1: smaller CT810a chamber.  CT704b and CT714 4-module attenuators are used.  Directional antennas
notes2: mounted on the sides of the DUT chamber are used to communicate to the DUT.   DUT is facing forward at
notes3: the zero-rotation angle.
bg: 0xE0ECF8
show_scan: 1
auto_helper: 1
skip_2: 0
skip_5: 0
skip_5b: 1
skip_dual: 0
skip_tri: 1
selected_dut5: TR398-DUT ruckus750-5 4c:b1:cd:18:e8:ec (1)
selected_dut2: TR398-DUT ruckus750-2 4c:b1:cd:18:e8:e8 (2)
upstream_port: 1.2.2 eth2
operator: 
mconn: 5
band2_freq: 2437
band5_freq: 5180
tos: 0
speed: 65%
speed_max_cx_2: 2000000
speed_max_cx_5: 8000000
max_tput_speed_2: 100000000
max_tput_speed_5: 560000000
rxsens_deg_rot: 45
rxsens_pre_steps: 8
stability_udp_dur: 3600
stability_iter: 288
calibrate_mode: 4
calibrate_nss: 1
dur120: 120
dur180: 180
i_5g_80: 195000000
i_5g_40: 90000000
i_2g_20: 32000000
spatial_deg_rot: 30
spatial_retry: 0
reset_pp: 99
rxsens_stop_at_pass: 0
auto_coex: 1
rvr_adj: 0
rssi_2m_2: -20
rssi_2m_5: -32
extra_dl_path_loss: 3
dur60: 60
turn_table: TR-398
radio-0: 1.1.2 wiphy0
radio-1: 1.1.3 wiphy1
radio-2: 1.1.4 wiphy2
radio-3: 1.1.5 wiphy3
radio-4: 1.1.6 wiphy4
radio-5: 1.1.7 wiphy5
rssi_0_2-0: -26
rssi_0_2-1: -26
rssi_0_2-2: -26
rssi_0_2-3: -26
rssi_0_2-4: -27
rssi_0_2-5: -27
rssi_0_2-6: -27
rssi_0_2-7: -27
rssi_0_2-8: -25
rssi_0_2-9: -25
rssi_0_2-10: -25
rssi_0_2-11: -25
rssi_0_5-0: -38
rssi_0_5-1: -38
rssi_0_5-2: -38
rssi_0_5-3: -38
rssi_0_5-4: -38
rssi_0_5-5: -38
rssi_0_5-6: -38
rssi_0_5-7: -38
rssi_0_5-8: -47
rssi_0_5-9: -47
rssi_0_5-10: -47
rssi_0_5-11: -47
atten-0: 1.1.85.0
atten-1: 1.1.85.1
atten-2: 1.1.85.2
atten-3: 1.1.85.3
atten-4: 1.1.1002.0
atten-5: 1.1.1002.1
atten-8: 1.1.1002.2
atten-9: 1.1.1002.3
atten_cal: 1
rxsens: 0
max_cx: 0
max_tput: 0
atf: 0
rvr: 0
spatial: 0
multi_sta: 0
reset: 0
mu_mimo: 0
stability: 0
ap_coex: 0
"""
import sys
import os
import importlib
import argparse
import time
import json
from os import path

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

cv_test_manager = importlib.import_module("py-json.cv_test_manager")
cvtest = cv_test_manager.cv_test
cv_add_base_parser = cv_test_manager.cv_add_base_parser
cv_base_adjust_parser = cv_test_manager.cv_base_adjust_parser


class TR398Test(cvtest):
    def __init__(self,
                 lf_host="localhost",
                 lf_port=8080,
                 lf_user="lanforge",
                 lf_password="lanforge",
                 instance_name="tr398_instance",
                 config_name="tr398_config",
                 upstream="1.2.eth2",
                 test_rig="",
                 local_lf_report_dir="",
                 pull_report=False,
                 load_old_cfg=False,
                 raw_lines_file="",
                 dut5="",
                 dut2="",
                 enables=[],
                 disables=[],
                 raw_lines=[],
                 sets=[],
                 ):
        super().__init__(lfclient_host=lf_host, lfclient_port=lf_port)

        self.lf_host = lf_host
        self.lf_port = lf_port
        self.lf_user = lf_user
        self.lf_password =lf_password
        self.instance_name = instance_name
        self.config_name = config_name
        self.dut5 = dut5
        self.dut2 = dut2
        self.raw_lines_file = raw_lines_file
        self.upstream = upstream
        self.pull_report = pull_report
        self.load_old_cfg = load_old_cfg
        self.test_name = "TR-398"
        self.enables = enables
        self.disables = disables
        self.raw_lines = raw_lines
        self.sets = sets
        self.local_lf_report_dir = local_lf_report_dir
        self.test_rig = test_rig

    def setup(self):
        # Nothing to do at this time.
        return


    def run(self):
        self.sync_cv()
        time.sleep(2)
        self.sync_cv()

        blob_test = "%s-"%(self.test_name)

        self.rm_text_blob(self.config_name, blob_test)  # To delete old config with same name
        self.show_text_blob(None, None, False)

        # Test related settings
        cfg_options = []

        self.apply_cfg_options(cfg_options, self.enables, self.disables, self.raw_lines, self.raw_lines_file)

        # cmd line args take precedence
        if self.upstream != "":
            cfg_options.append("upstream_port: " + self.upstream)
        if self.dut5 != "":
            cfg_options.append("selected_dut5: " + self.dut5)
        if self.dut2 != "":
            cfg_options.append("selected_dut2: " + self.dut2)
        if self.test_rig != "":
            cfg_options.append("test_rig: " + self.test_rig)

        # We deleted the scenario earlier, now re-build new one line at a time.

        self.build_cfg(self.config_name, blob_test, cfg_options)

        cv_cmds = []
        self.create_and_run_test(self.load_old_cfg, self.test_name, self.instance_name,
                                 self.config_name, self.sets,
                                 self.pull_report, self.lf_host, self.lf_user, self.lf_password,
                                 cv_cmds, local_lf_report_dir=self.local_lf_report_dir)

        self.rm_text_blob(self.config_name, blob_test)  # To delete old config with same name


def main():

    parser = argparse.ArgumentParser(
        prog="lf_tr398_test.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
    Open this file in an editor and read the top notes for more details.

    Example:

  ./lf_tr398_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \\
      --instance_name tr398-instance --config_name test_con \\
      --upstream 1.2.eth2 \\
      --test_rig Testbed-01 --pull_report \\
      --local_lf_report_dir /tmp/my-report \\
      --dut5 'TR398-DUT-r750 ruckus-r750-5g 4c:b1:cd:18:e8:ec (1)' \\
      --dut2 'TR398-DUT-r750 ruckus-r750-2g 4c:b1:cd:18:e8:e8 (2)' \\
      --raw_lines_file example-configs/tr398-ferndale-ac-cfg.txt \\
      --set 'Calibrate Attenuators' 0 \\
      --set 'Receiver Sensitivity' 0 \\
      --set 'Maximum Connection' 1 \\
      --set 'Maximum Throughput' 1 \\
      --set 'Airtime Fairness' 0 \\
      --set 'Range Versus Rate' 0 \\
      --set 'Spatial Consistency' 0 \\
      --set 'Multiple STAs Performance' 0 \\
      --set 'Multiple Assoc Stability' 0 \\
      --set 'Downlink MU-MIMO' 0 \\
      --set 'AP Coexistence' 0 \\
      --set 'Long Term Stability' 0

   The contents of the 'raw_lines_file' argument can be obtained by manually configuring the
   TR398 test in the LANforge GUI, then select 'Show Config' on the Advanced configuration tab,
   select that config text, and paste it into a file.  That file is the argument to the
   --raw_lines_file argument.

      """
                                     )

    cv_add_base_parser(parser)  # see cv_test_manager.py

    parser.add_argument("-u", "--upstream", type=str, default="",
                        help="Upstream port for wifi capacity test ex. 1.1.eth2")

    parser.add_argument("--dut2", default="",
                        help="Specify 2Ghz DUT used by this test, example: 'TR398-DUT-r750 ruckus-r750-2g 4c:b1:cd:18:e8:e8 (2)'")
    parser.add_argument("--dut5", default="",
                        help="Specify 5Ghz DUT used by this test, example: 'TR398-DUT-r750 ruckus-r750-5g 4c:b1:cd:18:e8:ec (1)'")
    parser.add_argument("--local_lf_report_dir",
                        help="--local_lf_report_dir <where to pull reports to>  default '' means put in current working directory",
                        default="")

    args = parser.parse_args()

    cv_base_adjust_parser(args)

    CV_Test = TR398Test(lf_host = args.mgr,
                        lf_port = args.port,
                        lf_user = args.lf_user,
                        lf_password = args.lf_password,
                        instance_name = args.instance_name,
                        config_name = args.config_name,
                        upstream = args.upstream,
                        pull_report = args.pull_report,
                        local_lf_report_dir = args.local_lf_report_dir,
                        load_old_cfg = args.load_old_cfg,
                        dut2 = args.dut2,
                        dut5 = args.dut5,
                        raw_lines_file = args.raw_lines_file,
                        enables = args.enable,
                        disables = args.disable,
                        raw_lines = args.raw_line,
                        sets = args.set,
                        test_rig=args.test_rig
                        )
    CV_Test.setup()
    CV_Test.run()


if __name__ == "__main__":
    main()
