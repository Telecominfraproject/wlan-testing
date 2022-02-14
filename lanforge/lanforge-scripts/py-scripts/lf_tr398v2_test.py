#!/usr/bin/env python3
"""
Note: To Run this script gui should be opened with

    path: cd LANforgeGUI_5.4.4 (5.4.4 can be changed with GUI version)
          pwd (Output : /home/lanforge/LANforgeGUI_5.4.4)
          ./lfclient.bash -cli-socket 3990

This script is used to automate running TR398v2 tests.  You
may need to view a TR398v2 test configured through the GUI to understand
the options and how best to input data.

    ./lf_tr398v2_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \
      --instance_name tr398-instance --config_name test_con \
      --upstream 1.2.eth2 \
      --test_rig Testbed-01 --pull_report \
      --local_lf_report_dir=/tmp/my_report \
      --dut5 'TR398-DUT ruckus750-5 4c:b1:cd:18:e8:ec (1)' \
      --dut2 'TR398-DUT ruckus750-2 4c:b1:cd:18:e8:e8 (2)' \
      --raw_lines_file example-configs/tr398v2-ferndale-ac-cfg.txt \
      --set 'Calibrate 802.11AX Attenuators' 0 \
      --set 'Calibrate 802.11AC Attenuators' 0 \
      --set '6.1.1 Receiver Sensitivity' 0 \
      --set '6.2.1 Maximum Connection' 0 \
      --set '6.2.2 Maximum Throughput' 1 \
      --set '6.2.3 Airtime Fairness' 0 \
      --set '6.2.3 Airtime Fairness' 0 \
      --set '6.2.4 Dual-Band Throughput' 0 \
      --set '6.2.5 Bi-Directional Throughput' 0 \
      --set '6.3.1 Range Versus Rate' 0 \
      --set '6.3.2 Spatial Consistency' 0 \
      --set '6.3.3 AX Peak Performance' 0 \
      --set '6.4.1 Multiple STAs Performance' 0 \
      --set '6.4.2 Multiple Assoc Stability' 0 \
      --set '6.4.3 Downlink MU-MIMO' 0 \
      --set '6.5.2 AP Coexistence' 0 \
      --set '6.5.1 Long Term Stability' 0

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
    example-configs/tr398v2-ferndale-ac-cfg.txt in this example.
    Contents of that file is a list of raw lines, for instance:

rssi_0_2-0: -26
rssi_0_2-1: -26
rssi_0_2-2: -26
....

Example of raw text config for TR-398v2, to show other possible options.  You
can configure the TR398v2 test in the LANforge GUI and use the 'Show Config' option
on the 'Advanced Configuration' tab to show this config info:

show_events: 1
show_log: 1
port_sorting: 2
kpi_id: TR_398v2
bg: 0xE0ECF8
dut_info_override: Anonymous Enterprise AX AP
test_rig:
test_tag:
show_scan: 1
auto_helper: 1
skip_ac: 0
skip_ax: 0
skip_2: 0
skip_5: 0
skip_5b: 1
skip_dual: 0
skip_tri: 1
selected_dut5: TR398-DUT-r750 ruckus-r750-5g 4c:b1:cd:18:e8:ec (1)
selected_dut2: TR398-DUT-r750 ruckus-r750-2g 4c:b1:cd:18:e8:e8 (2)
upstream_port: 1.2.2 eth2
operator:
mconn: 5
txpower: 20
band2_freq: 2437
band5_freq: 5180
tos: 0
speed: 65%
ospeed: 20000
max_cx_random: 0
speed_max_cx_adjust: 1000000
speed_max_cx_2: 2000000
speed_max_cx_ax_2: 3000000
speed_max_cx_5: 8000000
speed_max_cx_ax_5: 10000000
max_tput_speed_2: 100000000
max_tput_speed_5: 560000000
max_tput_speed_ax_2: 200000000
max_tput_speed_ax_5: 720000000
max_peak_tput_speed_ax_2: 300000000
max_peak_tput_speed_ax_5: 1100000000
max_peak_tput_speed_ax_5_4: 1100000000
atf_max_nss: 2
atf_extra_2m_atten: 0
rxsens_deg_rot: 180
rxsens_pre_steps: 4
stability_udp_dur: 900
stability_iter: 16
calibrate_mode: 4
calibrate_nss: 1
dur120: 30
dur180: 180
i_5g_80: 195000000
i_5g_40: 90000000
i_2g_20: 32000000
i_5g_80_ax: 195000000
i_5g_40_ax: 90000000
i_2g_20_ax: 32000000
spatial_deg_rot: 30
spatial_retry: 0
reset_pp: 99
bidir_dp_prcnt: 0.05
rxsens_stop_at_pass: 0
spatial_pause_on_zero_tput: 0
auto_coex: 0
use_virtual_ax_sta: 0
rvr_adj: 0
rssi_2m_2: -26
rssi_2m_5: -30
extra_dl_path_loss: 0
dur60: 20
turn_table: TR-398
radio-0: 1.1.2 wiphy0
radio-1: 1.1.3 wiphy1
radio-2: 1.1.4 wiphy2
radio-3: 1.1.5 wiphy3
radio-4: 1.1.6 wiphy4
radio-5: 1.1.7 wiphy5
ax_radio-0: 1.2.wiphy0
ax_radio-1: 1.2.wiphy1
ax_radio-2: 1.2.wiphy2
ax_radio-3: 1.2.wiphy3
ax_radio-4: 1.2.wiphy4
ax_radio-5: 1.2.wiphy5
ax_radio-6: 1.2.wiphy6
ax_radio-7: 1.2.wiphy7
ax_radio-8: 1.2.wiphy8
ax_radio-9: 1.2.wiphy9
ax_radio-10: 1.2.wiphy10
ax_radio-11: 1.2.wiphy11
ax_radio-12: 1.3.wiphy0
ax_radio-13: 1.3.wiphy5
ax_radio-14: 1.3.wiphy10
ax_radio-15: 1.3.wiphy15
ax_radio-16: 1.3.wiphy1
ax_radio-17: 1.3.wiphy6
ax_radio-18: 1.3.wiphy11
ax_radio-19: 1.3.wiphy16
ax_radio-20: 1.3.wiphy2
ax_radio-21: 1.3.wiphy7
ax_radio-22: 1.3.wiphy12
ax_radio-23: 1.3.wiphy17
ax_radio-24: 1.3.wiphy3
ax_radio-25: 1.3.wiphy8
ax_radio-26: 1.3.wiphy13
ax_radio-27: 1.3.wiphy18
ax_radio-28: 1.3.wiphy4
ax_radio-29: 1.3.wiphy9
ax_radio-30: 1.3.wiphy14
ax_radio-31: 1.3.wiphy19
rssi_0_2-0: -28
rssi_0_2-1: -28
rssi_0_2-2: -28
rssi_0_2-3: -28
rssi_0_2-4: -22
rssi_0_2-5: -22
rssi_0_2-6: -22
rssi_0_2-7: -22
rssi_0_2-8: -25
rssi_0_2-9: -25
rssi_0_2-10: -25
rssi_0_2-11: -25
ax_rssi_0_2-0: -29
ax_rssi_0_2-1: -29
ax_rssi_0_2-2: -29
ax_rssi_0_2-3: -29
ax_rssi_0_2-4: -23
ax_rssi_0_2-5: -23
ax_rssi_0_2-6: -23
ax_rssi_0_2-7: -23
ax_rssi_0_2-8: -26
ax_rssi_0_2-9: -26
ax_rssi_0_2-10: -26
ax_rssi_0_2-11: -26
rssi_0_5-0: -35
rssi_0_5-1: -35
rssi_0_5-2: -35
rssi_0_5-3: -35
rssi_0_5-4: -33
rssi_0_5-5: -33
rssi_0_5-6: -33
rssi_0_5-7: -33
rssi_0_5-8: -39
rssi_0_5-9: -39
rssi_0_5-10: -39
rssi_0_5-11: -39
ax_rssi_0_5-0: -35
ax_rssi_0_5-1: -35
ax_rssi_0_5-2: -35
ax_rssi_0_5-3: -35
ax_rssi_0_5-4: -32
ax_rssi_0_5-5: -32
ax_rssi_0_5-6: -32
ax_rssi_0_5-7: -32
ax_rssi_0_5-8: -39
ax_rssi_0_5-9: -39
ax_rssi_0_5-10: -39
ax_rssi_0_5-11: -39
atten-0: 1.1.3094.0
atten-1: 1.1.3094.1
atten-2: 1.1.3094.2
atten-3: 1.1.3094.3
atten-4: 1.1.3102.0
atten-5: 1.1.3102.1
atten-6: 1.1.3099.0
atten-7: 1.1.3099.1
atten-8: 1.1.3102.2
atten-9: 1.1.3102.3
ax_atten-0: 1.1.3100.3
ax_atten-1: 1.1.3100.2
ax_atten-2: NA
ax_atten-3: NA
ax_atten-4: 1.1.3100.1
ax_atten-5: 1.1.3100.0
ax_atten-8: 1.1.3099.3
ax_atten-9: 1.1.3099.2
atten_cal_ac: 0
atten_cal_ax: 0
rxsens: 0
max_cx: 0
max_tput: 1
peak_perf: 0
max_tput_bi: 0
dual_band_tput: 0
atf: 0
atf3: 0
qos3: 0
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


class TR398v2Test(cvtest):
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
                 enables=None,
                 disables=None,
                 raw_lines=None,
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
        self.dut5 = dut5
        self.dut2 = dut2
        self.raw_lines_file = raw_lines_file
        self.upstream = upstream
        self.pull_report = pull_report
        self.load_old_cfg = load_old_cfg
        self.test_name = "TR-398 Issue 2"
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

        blob_test = "TR398v2-"

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
    parser = argparse.ArgumentParser("""
    Open this file in an editor and read the top notes for more details.

    Example:

  ./lf_tr398v2_test.py --mgr localhost --port 8080 --lf_user lanforge --lf_password lanforge \\
      --instance_name tr398-instance --config_name test_con \\
      --upstream 1.2.eth2 \\
      --test_rig Testbed-01 --pull_report \\
      --local_lf_report_dir /tmp/my-report \\
      --dut5 'TR398-DUT-r750 ruckus-r750-5g 4c:b1:cd:18:e8:ec (1)' \\
      --dut2 'TR398-DUT-r750 ruckus-r750-2g 4c:b1:cd:18:e8:e8 (2)' \\
      --raw_lines_file example-configs/tr398v2-ferndale-ac-cfg.txt \\
      --set 'Calibrate 802.11AX Attenuators' 0 \\
      --set 'Calibrate 802.11AC Attenuators' 0 \\
      --set '6.1.1 Receiver Sensitivity' 0 \\
      --set '6.2.1 Maximum Connection' 0 \\
      --set '6.2.2 Maximum Throughput' 1 \\
      --set '6.2.3 Airtime Fairness' 0 \\
      --set '6.2.3 Airtime Fairness' 0 \\
      --set '6.2.4 Dual-Band Throughput' 0 \\
      --set '6.2.5 Bi-Directional Throughput' 0 \\
      --set '6.3.1 Range Versus Rate' 0 \\
      --set '6.3.2 Spatial Consistency' 0 \\
      --set '6.3.3 AX Peak Performance' 0 \\
      --set '6.4.1 Multiple STAs Performance' 0 \\
      --set '6.4.2 Multiple Assoc Stability' 0 \\
      --set '6.4.3 Downlink MU-MIMO' 0 \\
      --set '6.5.2 AP Coexistence' 0 \\
      --set '6.5.1 Long Term Stability' 0

   The contents of the 'raw_lines_file' argument can be obtained by manually configuring the
   TR398 issue 2 test in the LANforge GUI, then select 'Show Config' on the Advanced configuration tab,
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

    CV_Test = TR398v2Test(lf_host=args.mgr,
                          lf_port=args.port,
                          lf_user=args.lf_user,
                          lf_password=args.lf_password,
                          instance_name=args.instance_name,
                          config_name=args.config_name,
                          upstream=args.upstream,
                          pull_report=args.pull_report,
                          local_lf_report_dir=args.local_lf_report_dir,
                          load_old_cfg=args.load_old_cfg,
                          dut2=args.dut2,
                          dut5=args.dut5,
                          raw_lines_file=args.raw_lines_file,
                          enables=args.enable,
                          disables=args.disable,
                          raw_lines=args.raw_line,
                          sets=args.set,
                          test_rig=args.test_rig
                          )
    CV_Test.setup()
    CV_Test.run()


if __name__ == "__main__":
    main()
