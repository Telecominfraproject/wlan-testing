#!/usr/bin/env python3

"""
NAME: cc_module_9800_3504.py

CLASSIFICATION: module

PURPOSE:
controller module for communicating to a cisco 9800 or 3504 controller
This module can be dynamically imported

SETUP:
None

EXAMPLE:
    There is a unit test included to try sample command scenarios
    ./cc_module_9800_3504.py --scheme ssh --dest localhost --port 8887 --user admin --passwd Cisco123 --ap APA453.0E7B.CF9C --series 9800 --prompt "WLC1" --timeout 10 --band '5g'
    ./cc_module_9800_3504.py --scheme ssh --dest localhost --port 8887 --user admin --passwd Cisco123 --ap APA453.0E7B.CF9C --series 9800 --prompt "WLC1" --timeout 10 --band '24g'

    ./cc_module_9800_3504.py --scheme ssh --dest localhost --port 8887 --user admin --passwd Cisco123 --ap APCC9C.3EF1.1140 --series 9800 --prompt "WLC1" --timeout 10 --band '5g'

SUPPORT HISTORY:

2/25/2022 - adding 6E support
formula:
5GHz channel = (freq_mhz - 5180) / 5 + 36
6GHz channel = (freq_mhz - 5955) / 5 + 1


COPYRIGHT:
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

INCLUDE_IN_README
"""

import sys
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

import argparse
import logging
import importlib
import os
import re
import subprocess
from pprint import pformat

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../")))


logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")


class create_controller_series_object:
    def __init__(self,
                 scheme=None,
                 dest=None,
                 user=None,
                 passwd=None,
                 prompt=None,
                 series=None,
                 band=None,
                 ap=None,
                 ap_band_slot_24g=None,
                 ap_band_slot_5g=None,
                 ap_band_slot_6g=None,
                 ap_dual_band_slot_5g=None,
                 ap_dual_band_slot_6g=None,
                 port=None,
                 timeout=None,
                 pwd=None
                 ):
        if scheme is None:
            raise ValueError('Controller scheme must be set: serial, ssh or telnet')
        else:
            self.scheme = scheme
        if dest is None:
            raise ValueError('Controller dest must be set: and IP or localhost')
        else:
            self.dest = dest
        if user is None:
            raise ValueError('Controller user must be set')
        else:
            self.user = user
        if passwd is None:
            raise ValueError('Controller passwd must be set')
        else:
            self.passwd = passwd
        if prompt is None:
            raise ValueError('Controller prompt must be set: WLC1')
        else:
            self.prompt = prompt
        if series is None:
            raise ValueError('Controller series must be set: 9800 or 3504')
        else:
            self.series = series

        if ap is None:
            raise ValueError('Controller AP  must be set')
        else:
            self.ap = ap

        # for backward compatiblity if the ap_band_clot is not passed in set to common defaults
        # Also some APs do not support all bands
        # TODO put in a check if the slots are not found.
        if ap_band_slot_24g is None:
            logger.warning("ap_band_slot_24g not configured using value of '0'")
            self.ap_band_slot_24g = '0'
        else:
            self.ap_band_slot_24g = ap_band_slot_24g

        if ap_band_slot_5g is None:
            logger.warning("ap_band_slot_5g not configured using value of '1'")
            self.ap_band_slot_5g = '1'
        else:
            self.ap_band_slot_5g = ap_band_slot_5g

        if ap_band_slot_6g is None:
            logger.warning("ap_band_slot_6g not configured using value of '2'")
            self.ap_band_slot_6g = '2'
        else:
            self.ap_band_slot_6g = ap_band_slot_6g

        if ap_dual_band_slot_5g is None:
            logger.warning("ap_dual_band_slot_5g not configured using value of '2'")
            self.ap_dual_band_slot_5g = '2'
        else:
            self.ap_dual_band_slot_5g = ap_dual_band_slot_5g

        if ap_dual_band_slot_6g is None:
            logger.warning("ap_dual_band_slot_6g not configured using value of '2'")
            self.ap_dual_band_slot_6g = '2'
        else:
            self.ap_dual_band_slot_6g = ap_dual_band_slot_6g

        if band is None:
            raise ValueError('Controller band  must be set')
        else:
            self.band = band
        if port is None:
            raise ValueError('Controller port  must be set')
        else:
            self.port = port

        if timeout is None:
            logger.info("timeout not set default to 3 sec")
            self.timeout = '3'
        else:
            self.timeout = timeout

        self.bandwidth = None
        self.wlan = None
        self.wlanID = None
        self.wlanSSID = None
        self.security_key = None
        self.wlanpw = None
        self.tag_policy = None
        self.policy_profile = None
        self.ap_band_slot = None
        self.tx_power = None
        self.ap_num_power_levels = 'NA'
        self.ap_current_tx_power_level = 'NA'
        self.ap_tx_power_dbm = 'NA'
        self.channel = None
        self.bandwidth = None
        self.action = None
        self.value = None
        self.command = []
        self.command_extend = []
        self.info = "Cisco 9800 Controller Series"
        self.pwd = pwd
        self.dtim = None
        self.spatial_stream = None  # default cannot be NONE for send command
        self.mcs_tx_index = None    # default cannot be NONE for send command
        self.regulatory_domain = 'NA'
        self.country_code = 'NA'
        # self.series = 'NA'
        self.testbed_location = 'NA'
        self.ap_config_radio_role = 'NA'


    # TODO update the wifi_ctl_9800_3504 to use 24g, 5g, 6g

    def convert_band(self):
        if self.band == '24g':
            self.band = '24g'
        elif self.band == '5g':
            self.band = '5g'
        elif self.band == '6g':
            self.band = '6g'
        elif self.band == 'dual_band_5g':
            self.band = 'dual_band_5g'
        elif self.band == 'dual_band_6g':
            self.band = 'dual_band_6g'
        else:
            logger.critical("band needs to be set 24g 5g 6g dual_band_5g, dual_band_6g")
            raise ValueError("band needs to be set 24g 5g 6g dual_band_5g or dual_band_6g")

    # TODO need to configure the slot
    def set_ap_band_slot(self):
        if self.band == '24g':
            self.ap_band_slot = self.ap_band_slot_24g
        elif self.band == '5g':
            self.ap_band_slot = self.ap_band_slot_5g
        # TODO need to support configuration
        elif self.band == '6g':
            self.ap_band_slot = self.ap_band_slot_6g
        elif self.band == 'dual_band_5g':
            self.ap_band_slot = self.ap_dual_band_slot_5g
        elif self.band == 'dual_band_6g':
            self.ap_band_slot = self.ap_dual_band_slot_6g

            # if self.ap_band_slot is None:
            #    logger.critical("ap_band_slot_6g needs to be set to 2 or 3")
            #    raise ValueError("ap_band_slot_6g needs to be set to 2 or 3")
#
    # TODO consolidate the command formats

    def send_command(self):
        # self.convert_band()
        self.set_ap_band_slot()

        logger.info("action {action}".format(action=self.action))

        # set the ap_band_slot 24g = ap_band_slot 0 , 5g ap_band_slot = 1 / 2, 6g - ap_band_slot 2 / 3 so needs to be passed in

        # Command base
        if self.pwd is None:
            self.command = ["./wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--dest", self.dest,
                            "--user", self.user, "--passwd", self.passwd, "--prompt", self.prompt,
                            "--series", self.series, "--ap", self.ap, "--ap_band_slot", self.ap_band_slot, "--band", self.band, "--port", self.port,
                            "--timeout", self.timeout,
                            ]
        else:
            self.command = [str(str(self.pwd) + "/wifi_ctl_9800_3504.py"), "--scheme", self.scheme, "--dest", self.dest,
                            "--user", self.user, "--passwd", self.passwd, "--prompt", self.prompt,
                            "--series", self.series, "--ap", self.ap, "--ap_band_slot", self.ap_band_slot, "--band", self.band, "--port", self.port,
                            "--timeout", self.timeout,
                            ]

        # Generate command
        if self.action in ['cmd', 'txPower', 'channel', 'bandwidth']:

            self.command_extend = ["--action", self.action, "--value", self.value]
            self.command.extend(self.command_extend)

        elif self.action in ["create_wlan", "create_wlan_wpa2", "create_wlan_wpa3", "dtim", "enable_ft_akm_ftpsk",
                             "enable_ftotd_akm_ftpsk", "enable_ft_akm_ftsae", "enable_ft_wpa3_dot1x",
                             "enable_ft_wpa3_dot1x_sha256", "show_client_macadd_detail",  'debug_wieless_mac',
                             'no_debug_wieless_mac', 'get_data_ra_trace_files', 'del_ra_trace_file']:

            if self.action in ["create_wlan"]:
                self.command_extend = ["--action", self.action, "--wlan", self.wlan,
                                       "--wlanID", self.wlanID, "--wlanSSID", self.wlanSSID]
            elif self.action in ["create_wlan_wpa2", "create_wlan_wpa3"]:
                self.command_extend = ["--action", self.action, "--wlan", self.wlan,
                                       "--wlanID", self.wlanID, "--wlanSSID", self.wlanSSID, "--security_key", self.security_key]
            elif self.action in ["dtim"]:
                self.command_extend = ["--action", self.action, "--wlan", self.wlan, "--value", self.value]
            elif self.action in ["enable_ft_akm_ftpsk"]:
                self.command_extend = ["--action", self.action, "--wlan", self.wlan, "--security_key", self.security_key]
            elif self.action in ["enable_ft_akm_ftsae"]:
                self.command_extend = ["--action", self.action, "--wlan", self.wlan, "--security_key",
                                       self.security_key]
            elif self.action in ["enable_ft_wpa3_dot1x"]:
                self.command_extend = ["--action", self.action, "--wlan", self.wlan, "--security_key",
                                       self.security_key]
            elif self.action in ["enable_ft_wpa3_dot1x_sha256"]:
                self.command_extend = ["--action", self.action, "--wlan", self.wlan, "--security_key",
                                       self.security_key, "--value", self.value]
            elif self.action in ["enable_ftotd_akm_ftpsk"]:
                self.command_extend = ["--action", self.action, "--wlan", self.wlan, "--security_key",
                                       self.security_key]
            elif self.action in ["show_client_macadd_detail"]:
                self.command_extend = ["--action", self.action, "--value", self.value]
            elif self.action in ['debug_wieless_mac']:
                self.command_extend = ["--action", self.action, "--value", self.value]
            elif self.action in ['no_debug_wieless_mac']:
                self.command_extend = ["--action", self.action, "--value", self.value]
            elif self.action in ['get_data_ra_trace_files']:
                self.command_extend = ["--action", self.action, "--value", self.value]
            elif self.action in ['del_ra_trace_file']:
                self.command_extend = ["--action", self.action, "--value", self.value]

            self.command.extend(self.command_extend)

        elif self.action in ["enable_wlan", "disable_wlan", "delete_wlan"]:

            self.command_extend = ["--action", self.action, "--wlan", self.wlan]
            self.command.extend(self.command_extend)

        elif self.action in ["wireless_tag_policy"]:

            self.command_extend = [
                "--action",
                self.action,
                "--wlan",
                self.wlan,
                "--tag_policy",
                self.tag_policy,
                "--policy_profile",
                self.policy_profile]
            self.command.extend(self.command_extend)

        elif self.action in ["ap_dot11_dot11ax_mcs_tx_index_spatial_stream", "no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream"]:
            self.command_extend = [
                "--action", self.action, 
                "--spatial_stream", str(self.spatial_stream), 
                "--mcs_tx_index", str(self.mcs_tx_index)
            ]
            self.command.extend(self.command_extend)

        # possible need to look for exact command
        elif self.action in ["summary", "show_radio", "no_logging_console", "line_console_0", "show_ap_wlan_summary", "show_wlan_summary", "show_wlan_id",
                             "show_ap_name_config_role",
                             "advanced", "disable_operation_status",
                             "disable_network_dual_band_6ghz", "disable_network_dual_band_5ghz", "disable_network_6ghz", "disable_network_5ghz", "disable_network_24ghz",
                             "show_ap_bssid_dual_band_6g", "show_ap_bssid_dual_band_5g", "show_ap_bssid_6g", "show_ap_bssid_5g", "show_ap_bssid_24g",
                             "manual", "auto",
                             "enable_network_dual_band_6ghz", "enable_network_dual_band_5ghz", "enable_network_6ghz", "enable_network_5ghz", "enable_network_24ghz",
                             "enable_operation_status", "11r_logs", "enable_ft_akm_ftpsk", "enable_ftotd_akm_ftpsk",
                             "config_dual_band_mode", "dual_band_no_mode_shutdown", "dual_band_mode_shutdown",
                             "enable_ft_akm_ftsae", "enable_ft_wpa3_dot1x", "enable_ft_wpa3_dot1x_sha256",
                             "show_wireless_client_sumry", "show_client_macadd_detail", 'debug_wieless_mac',
                             'no_debug_wieless_mac', 'get_ra_trace_files','get_data_ra_trace_files','del_ra_trace_file',
                             "show_ap_status","show_ap_tx_power_config"
                             ]:

            self.command_extend = ["--action", self.action]
            self.command.extend(self.command_extend)

        else:
            logger.critical("action {action} not supported".format(action=self.action))
            raise ValueError("action {action} not supported".format(action=self.action))

        # logger.info(pformat(self.command))
        logger.info(self.command)
        # TODO change the subprocess.run to pOpen
        summary_output = ''
        print(self.command)
        summary = subprocess.Popen(self.command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(summary.stdout.readline, ''):
            logger.debug(line)
            summary_output += line
            # sys.stdout.flush() # please see comments regarding the necessity of this line
        summary.wait()
        logger.info(summary_output)  # .decode('utf-8', 'ignore'))
        # logger.info(advanced.stderr.decode('utf-8', 'ignore'))
        return summary_output

    # use to get the BSSID for wlan
    def show_ap_config_slots(self):
        logger.info("show ap config slots")
        self.action = "cmd"
        self.value = "show ap config slots"
        summary = self.send_command()
        return summary

    # show wlan id <wlan ID>
    def show_wlan_id(self):
        logger.info("show ap config slots")
        self.action = "cmd"
        self.value = "show wlan id {wlanID}".format(wlanID=self.wlanID)
        summary = self.send_command()
        return summary

    def config_dtim_dot11_dual_band_6ghz(self):
        logger.info("dtim dot11 dual band 6ghz")
        self.band = 'dual_band_6g'
        self.action = "dtim"
        self.value = self.dtim
        summary = self.send_command()
        return summary

    def config_dtim_dot11_dual_band_5ghz(self):
        logger.info("dtim dot11 dual band 5ghz")
        self.band = 'dual_band_5g'
        self.action = "dtim"
        self.value = self.dtim
        summary = self.send_command()
        return summary

    def config_dtim_dot11_6ghz(self):
        logger.info("dtim dot11 6ghz")
        self.band = '6g'
        self.action = "dtim"
        self.value = self.dtim
        summary = self.send_command()
        return summary

    # DTIM Delivery Traffic Indication Message
    def config_dtim_dot11_5ghz(self):
        logger.info("dtim dot11 5ghz")
        self.band = '5g'
        self.action = "dtim"
        self.value = self.dtim
        summary = self.send_command()
        return summary

    # DTIM Delivery Traffic Indication Message
    def config_dtim_dot11_24ghz(self):
        logger.info("dtim dot11 24ghz")
        self.band = '24g'
        self.action = "dtim"
        self.value = self.dtim
        summary = self.send_command()
        return summary

    # NOTE: need to do _no_logging_console and line_console_0 at the beginning of every session
    # to avoid unexpected log messages showing up

    # this command will disable debug logging to the terminal which causes issues with pexpect
    def no_logging_console(self):
        logger.info("no_logging_console")
        self.action = "no_logging_console"
        summary = self.send_command()
        return summary

    # Note: needed to be set for tx power script
    def line_console_0(self):
        logger.info("line_console_0")
        self.action = "line_console_0"
        summary = self.send_command()
        return summary

    def show_controllers_dot11Radio_0(self):
        logger.info("show radio")
        self.action = "show_radio"
        summary = self.send_command()
        return summary

    def show_ap_summary(self):
        logger.info("show ap summary")
        self.action = "summary"
        summary = self.send_command()
        return summary

    def show_ap_status(self):
        logger.info("show ap status")
        self.action = "show_ap_status"
        summary = self.send_command()
        return summary

    def show_ap_name_config_role(self):
        logger.info("show ap name config role")
        self.action = "show_ap_name_config_role"
        summary = self.send_command()
        return summary       

    def show_ap_bssid_dual_band_6ghz(self):
        logger.info("show ap name  wlan dot11 dual-band")
        self.band = 'dual_band_6g'
        self.action = "show_ap_bssid_dual_band_6g"
        summary = self.send_command()
        return summary

    def show_ap_bssid_dual_band_5ghz(self):
        logger.info("show ap name  wlan dot11 dual-band")
        self.band = 'dual_band_5g'
        self.action = "show_ap_bssid_dual_band_5g"
        summary = self.send_command()
        return summary

    def show_ap_bssid_6ghz(self):
        logger.info("show ap name <AP NAME> wlan dot11 6ghz")
        self.band = '6g'
        self.action = "show_ap_bssid_6g"
        summary = self.send_command()
        return summary

    def show_ap_bssid_5ghz(self):
        logger.info("show ap name  wlan dot11 5ghz")
        self.band = '5g'
        self.action = "show_ap_bssid_5g"
        summary = self.send_command()
        return summary

    def show_ap_bssid_24ghz(self):
        logger.info("show ap name  wlan dot11 24ghz")
        self.band = '24g'
        self.action = "show_ap_bssid_24g"
        summary = self.send_command()
        return summary

    def show_ap_wlan_dual_band_summary(self):
        logger.info("show ap wlan summary")
        self.action = "show_ap_wlan_summary"
        summary = self.send_command()
        return summary

    def show_ap_wlan_summary(self):
        logger.info("show ap wlan summary")
        self.action = "show_ap_wlan_summary"
        summary = self.send_command()
        return summary

    def show_wlan_summary(self):
        logger.info("show_wlan_summary")
        self.action = "show_wlan_summary"
        summary = self.send_command()
        return summary

    # TODO clean up action advanced to ap_dot11_summary
    def show_ap_dot11_dual_band_6gz_summary(self):
        logger.info("show ap dot11 dual-band 6gz summary")
        self.band = 'dual_band_6g'
        self.action = "advanced"
        summary = self.send_command()
        return summary

    def show_ap_dot11_dual_band_5gz_summary(self):
        logger.info("show ap dot11 dual-band 5gz summary")
        self.band = 'dual_band_5g'
        self.action = "advanced"
        summary = self.send_command()
        return summary

    def show_ap_dot11_6gz_summary(self):
        logger.info("show ap dot11 6gz summary")
        self.band = '6g'
        self.action = "advanced"
        summary = self.send_command()
        return summary

    def show_ap_dot11_5gz_summary(self):
        logger.info("show ap dot11 5gz summary")
        self.band = '5g'
        self.action = "advanced"
        summary = self.send_command()
        return summary

    def show_ap_dot11_24gz_summary(self):
        logger.info("show ap dot11 24gz summary")
        self.band = '24g'
        self.action = "advanced"
        summary = self.send_command()
        return summary

    def show_ap_dot11_dual_band_6gz_shutdown(self):
        logger.info("ap name {name} dot11 dual-band 6ghz shutdown")
        self.band = 'dual_band_6g'
        self.action = "disable_operation_status"
        summary = self.send_command()
        return summary

    def show_ap_dot11_dual_band_5gz_shutdown(self):
        logger.info("ap name {name} dot11 dual-band 5ghz shutdown")
        self.band = 'dual_band_5g'
        self.action = "disable_operation_status"
        summary = self.send_command()
        return summary

    def show_ap_dot11_6gz_shutdown(self):
        logger.info("ap name {name} dot11 6ghz shutdown")
        self.band = '6g'
        self.action = "disable_operation_status"
        summary = self.send_command()
        return summary

    def show_ap_dot11_5gz_shutdown(self):
        logger.info("ap name {name} dot11 5ghz shutdown")
        self.band = '5g'
        self.action = "disable_operation_status"
        summary = self.send_command()
        return summary

    def show_ap_dot11_24gz_shutdown(self):
        logger.info("ap name {name} dot11 24ghz shutdown")
        self.band = '24g'
        self.action = "disable_operation_status"
        summary = self.send_command()
        return summary

    def wlan_shutdown(self):
        logger.info("wlan {wlan} shutdown wlanID {wlanID} wlanSSID {wlanSSID}".format(wlan=self.wlan, wlanID=self.wlanID, wlanSSID=self.wlanSSID))
        self.action = "disable_wlan"
        summary = self.send_command()
        return summary

    # TODO May need to check if 6g supported on AP ,
    # or just send command and let controller show not supported.
    def ap_dot11_dual_band_6ghz_shutdown(self):
        logger.info("ap dot11 dual-band 6ghz shutdown")
        self.band = 'dual_band_6g'
        self.action = "disable_network_dual_band_6ghz"
        summary = self.send_command()
        return summary

    def ap_dot11_dual_band_5ghz_shutdown(self):
        logger.info("ap dot11 dual-band 5ghz shutdown")
        self.band = 'dual_band_5g'
        self.action = "disable_network_dual_band_5ghz"
        summary = self.send_command()
        return summary

    def ap_dot11_6ghz_shutdown(self):
        logger.info("ap dot11 6ghz shutdown")
        self.band = '6g'
        self.action = "disable_network_6ghz"
        summary = self.send_command()
        return summary

    def ap_dot11_5ghz_shutdown(self):
        logger.info("ap dot11 5ghz shutdown")
        self.band = '5g'
        self.action = "disable_network_5ghz"
        summary = self.send_command()
        return summary

    def ap_dot11_24ghz_shutdown(self):
        logger.info("wlan {wlan} shutdown".format(wlan=self.wlan))
        self.band = '24g'
        self.action = "disable_network_24ghz"
        summary = self.send_command()
        return summary

    def ap_dot11_dual_band_6ghz_radio_role_manual_client_serving(self):
        logger.info("ap name {ap_name} dot11 dual band 6ghz radio role manual client-serving".format(ap_name=self.ap))
        self.band = 'dual_band_6g'
        self.action = "manual"
        summary = self.send_command()
        return summary

    def ap_dot11_dual_band_5ghz_radio_role_manual_client_serving(self):
        logger.info("ap name {ap_name} dot11 dual band 5ghz radio role manual client-serving".format(ap_name=self.ap))
        self.band = 'dual_band_5g'
        self.action = "manual"
        summary = self.send_command()
        return summary

    def ap_dot11_6ghz_radio_role_manual_client_serving(self):
        logger.info("ap name {ap_name} dot11 6ghz radio role manual client-serving".format(ap_name=self.ap))
        self.band = '6g'
        self.action = "manual"
        summary = self.send_command()
        return summary

    def ap_dot11_5ghz_radio_role_manual_client_serving(self):
        logger.info("ap name {ap_name} dot11 5ghz radio role manual client-serving".format(ap_name=self.ap))
        self.band = '5g'
        self.action = "manual"
        summary = self.send_command()
        return summary

    def ap_dot11_24ghz_radio_role_manual_client_serving(self):
        logger.info("ap name {ap_name} dot11 24ghz radio role manual client-serving".format(ap_name=self.ap))
        self.band = '24g'
        self.action = "manual"
        summary = self.send_command()
        return summary

    def ap_dot11_dual_band_6ghz_radio_role_auto(self):
        logger.info("ap name {ap_name} dot11 dual band 6ghz radio role auto".format(ap_name=self.ap))
        self.band = 'dual_band_6g'
        self.action = "auto"
        summary = self.send_command()
        return summary

    def ap_dot11_dual_band_5ghz_radio_role_auto(self):
        logger.info("ap name {ap_name} dot11 dual band 5ghz radio role auto".format(ap_name=self.ap))
        self.band = 'dual_band_5g'
        self.action = "auto"
        summary = self.send_command()
        return summary

    def ap_dot11_6ghz_radio_role_auto(self):
        logger.info("ap name {ap_name} dot11 6ghz radio role auto".format(ap_name=self.ap))
        self.band = '6g'
        self.action = "auto"
        summary = self.send_command()
        return summary

    def ap_dot11_5ghz_radio_role_auto(self):
        logger.info("ap name {ap_name} dot11 5ghz radio role auto".format(ap_name=self.ap))
        self.band = '5g'
        self.action = "auto"
        summary = self.send_command()
        return summary

    def ap_dot11_24ghz_radio_role_auto(self):
        logger.info("ap name {ap_name} dot11 5ghz radio role auto".format(ap_name=self.ap))
        self.band = '24g'
        self.action = "auto"
        summary = self.send_command()
        return summary

    # TODO check if this command is used
    def config_dot11_5ghz_disable_network(self):
        logger.info("config_dot11_5ghz_disable_network")
        self.action = "cmd"
        self.value = "config 802.11a disable network"
        summary = self.send_command()
        return summary

    # TODO check if this command is used
    def config_dot11_24ghz_disable_network(self):
        logger.info("config_dot11_24ghz_disable_network")
        self.action = "cmd"
        self.value = "config 802.11b disable network"
        summary = self.send_command()
        return summary

    # txPower
    def config_dot11_dual_band_6ghz_tx_power(self):
        logger.info("config_dot11_dual_band_6ghz_tx_power")
        self.band = 'dual_band_6g'
        self.action = "txPower"
        self.value = "{tx_power}".format(tx_power=self.tx_power)
        summary = self.send_command()
        return summary

    def config_dot11_dual_band_5ghz_tx_power(self):
        logger.info("config_dot11_dual_band_5ghz_tx_power")
        self.band = 'dual_band_5g'
        self.action = "txPower"
        self.value = "{tx_power}".format(tx_power=self.tx_power)
        summary = self.send_command()
        return summary

    def config_dot11_6ghz_tx_power(self):
        logger.info("config_dot11_6ghz_tx_power")
        self.band = '6g'
        self.action = "txPower"
        self.value = "{tx_power}".format(tx_power=self.tx_power)
        summary = self.send_command()
        return summary

    def config_dot11_5ghz_tx_power(self):
        logger.info("config_dot11_5ghz_tx_power")
        self.band = '5g'
        self.action = "txPower"
        self.value = "{tx_power}".format(tx_power=self.tx_power)
        summary = self.send_command()
        return summary

    def config_dot11_24ghz_tx_power(self):
        logger.info("config_dot11_24ghz_tx_power")
        self.band = '24g'
        self.action = "txPower"
        self.value = "{tx_power}".format(tx_power=self.tx_power)
        summary = self.send_command()
        return summary

    # set channel
    def config_dot11_dual_band_6ghz_channel(self):
        logger.info("config_dot11_dual_band_6ghz_channel {channel}".format(channel=self.channel))
        self.band = 'dual_band_6g'
        self.action = "channel"
        self.value = "{channel}".format(channel=self.channel)
        summary = self.send_command()
        return summary

    def config_dot11_dual_band_5ghz_channel(self):
        logger.info("config_dot11_dual_band_5ghz_channel {channel}".format(channel=self.channel))
        self.band = 'dual_band_5g'
        self.action = "channel"
        self.value = "{channel}".format(channel=self.channel)
        summary = self.send_command()
        return summary

    def config_dot11_6ghz_channel(self):
        logger.info("config_dot11_6ghz_channel {channel}".format(channel=self.channel))
        self.band = '6g'
        self.action = "channel"
        self.value = "{channel}".format(channel=self.channel)
        summary = self.send_command()
        return summary

    def config_dot11_5ghz_channel(self):
        logger.info("config_dot11_5ghz_channel {channel}".format(channel=self.channel))
        self.band = '5g'
        self.action = "channel"
        self.value = "{channel}".format(channel=self.channel)
        summary = self.send_command()
        return summary

    def config_dot11_24ghz_channel(self):
        logger.info("config_dot11_24ghz_channel {channel}".format(channel=self.channel))
        self.band = '24g'
        self.action = "channel"
        self.value = "{channel}".format(channel=self.channel)
        summary = self.send_command()
        return summary

    # set bandwidth
    def config_dot11_dual_band_6ghz_channel_width(self):
        logger.info("config_dot11_dual_band_6ghz_channel width {bandwidth}".format(bandwidth=self.bandwidth))
        self.band = 'dual_band_6g'
        self.action = "bandwidth"
        self.value = "{bandwidth}".format(bandwidth=self.bandwidth)
        summary = self.send_command()
        return summary

    def config_dot11_dual_band_5ghz_channel_width(self):
        logger.info("config_dot11_dual_band_5ghz_channel width {bandwidth}".format(bandwidth=self.bandwidth))
        self.band = 'dual_band_5g'
        self.action = "bandwidth"
        self.value = "{bandwidth}".format(bandwidth=self.bandwidth)
        summary = self.send_command()
        return summary

    def config_dot11_6ghz_channel_width(self):
        logger.info("config_dot11_6ghz_channel width {bandwidth}".format(bandwidth=self.bandwidth))
        self.band = '6g'
        self.action = "bandwidth"
        self.value = "{bandwidth}".format(bandwidth=self.bandwidth)
        summary = self.send_command()
        return summary

    def config_dot11_5ghz_channel_width(self):
        logger.info("config_dot11_5ghz_channel width {bandwidth}".format(bandwidth=self.bandwidth))
        self.band = '5g'
        self.action = "bandwidth"
        self.value = "{bandwidth}".format(bandwidth=self.bandwidth)
        summary = self.send_command()
        return summary

    # TODO 24ghz is always 20 Mhz
    def config_dot11_24ghz_channel_width(self):
        logger.info("config_dot11_24ghz_channel width {bandwidth}".format(bandwidth=self.bandwidth))
        self.band = '24g'
        self.action = "bandwidth"
        self.value = "{bandwidth}".format(bandwidth=self.bandwidth)
        summary = self.send_command()
        return summary

    def ap_name_shutdown(self):
        logger.info("ap name {ap} shutdown".format(ap=self.ap))
        self.action = 'cmd'
        self.value = "ap name {ap} shutdown".format(ap=self.ap)
        summary = self.send_command()
        return summary

    def ap_name_no_shutdown(self):
        logger.info("ap name {ap} no shutdown".format(ap=self.ap))
        self.action = 'cmd'
        self.value = "ap name {ap} no shutdown".format(ap=self.ap)
        summary = self.send_command()
        return summary

    # delete_wlan (may need to get the wlan from the summary)

    def config_no_wlan(self):
        logger.info("config_no_wlan {wlan}".format(wlan=self.wlan))
        self.action = "delete_wlan"
        summary = self.send_command()
        return summary

    # configure open wlan , commands sent
    #    for command in [
    #        "no security ft",
    #        "no security ft adaptive",
    #        "no security wpa",
    #        "no security wpa wpa2",
    #        "no security wpa wpa1",
    #        "no security wpa wpa2 ciphers aes"
    #        "no security dot1x authentication-list",
    #        "no security wpa akm dot1x",
    #        "no shutdown"]:

    def config_wlan_open(self):
        logger.info("config_wlan wlan: Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID}".format(
            wlan=self.wlan, wlanID=self.wlanID, wlanSSID=self.wlanSSID))
        self.action = "create_wlan"
        summary = self.send_command()
        return summary

    # TODO ability to pass in psk
    # configuration for wpa2, commands
    #    for command in [
    #        "assisted-roaming dual-list",
    #        "bss-transition dual-list",
    #        "radio policy dot11 24ghz",
    #        "radio policy dot11 5ghz",
    #        "security wpa psk set-key ascii 0 hello123",
    #        "no security wpa akm dot1x",
    #        "security wpa akm psk"
    #        "no shutdown"]:
    # configure wpa2
    def config_wlan_wpa2(self):
        logger.info("config_wlan_wpa2 wlan: Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID} security_key {security_key}".format(
            wlan=self.wlan, wlanID=self.wlanID, wlanSSID=self.wlanSSID, security_key=self.security_key))
        self.action = "create_wlan_wpa2"
        summary = self.send_command()
        return summary

    # configuration for wpa3, commands
    #    for command in [
    #        "assisted-roaming dual-list"
    #        "radio policy dot11 6ghz"
    #        "no security ft adaptive"
    #        "no security wpa wpa2"
    #        "security wpa psk set-key ascii 0 hello123"
    #        "no security wpa akm dot1x"
    #        "security wpa akm sae"
    #        "security wpa akm sae pwe h2e"
    #        "security wpa wpa3"
    #        "security pmf mandatory"
    #        "no shutdown"]:

    # configure wpa3
    # TODO pass in

    def config_wlan_wpa3(self):
        logger.info("config_wlan_wpa3 wlan: Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID}".format(
            wlan=self.wlan, wlanID=self.wlanID, wlanSSID=self.wlanSSID))
        self.action = "create_wlan_wpa3"
        summary = self.send_command()
        return summary

    # config wireless tag policy and policy_profile
    # this may need to be split up
    # WCL1 : RM204-TB1 , WLC2 : RM204-TB2
    # policy_profile = 'default-policy-profile'
    # TODO remove hardcoded 'default-policy-profile' make configurable

    def config_wireless_tag_policy_and_policy_profile(self):
        logger.info("config_wireless_tag_policy: Profile name {wlan} tag policy {tag_policy} ".format(wlan=self.wlan, tag_policy=self.tag_policy))
        self.action = "wireless_tag_policy"
        summary = self.send_command()
        return summary

    # enable_wlan
    def config_enable_wlan_send_no_shutdown(self):
        logger.info(
            "config_enable_wlan_send_no_shutdown: Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID}".format(
                wlan=self.wlan,
                wlanID=self.wlanID,
                wlanSSID=self.wlanSSID))
        self.action = "enable_wlan"
        summary = self.send_command()
        return summary

    # enable_network_dual_band_6ghz
    def config_no_ap_dot11_dual_band_6ghz_shutdown(self):
        logger.info(
            "config_no_ap_dot11_dual_band_6ghz_shutdown (enable network dual band 6ghz): Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID}".format(
                wlan=self.wlan,
                wlanID=self.wlanID,
                wlanSSID=self.wlanSSID))
        self.action = "enable_network_dual_band_6ghz"
        summary = self.send_command()
        return summary

    # enable_dual_band_network_5ghz
    def config_no_ap_dot11_dual_band_5ghz_shutdown(self):
        logger.info(
            "config_no_ap_dot11_dual_band_5ghz_shutdown (enable network dual band 5ghz): Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID}".format(
                wlan=self.wlan,
                wlanID=self.wlanID,
                wlanSSID=self.wlanSSID))
        self.action = "enable_network_dual_band_5ghz"
        summary = self.send_command()
        return summary

    # enable_network_6ghz
    def config_no_ap_dot11_6ghz_shutdown(self):
        logger.info(
            "config_no_ap_dot11_6ghz_shutdown (enable network 6ghz): Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID}".format(
                wlan=self.wlan,
                wlanID=self.wlanID,
                wlanSSID=self.wlanSSID))
        self.action = "enable_network_6ghz"
        summary = self.send_command()
        return summary

    # enable_network_5ghz
    def config_no_ap_dot11_5ghz_shutdown(self):
        logger.info(
            "config_no_ap_dot11_5ghz_shutdown (enable network 5ghz): Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID}".format(
                wlan=self.wlan,
                wlanID=self.wlanID,
                wlanSSID=self.wlanSSID))
        self.action = "enable_network_5ghz"
        summary = self.send_command()
        return summary

    # enable_network_24ghz
    def config_no_ap_dot11_24ghz_shutdown(self):
        logger.info(
            "config_no_ap_dot11_24ghz_shutdown (enable network 24ghz): Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID}".format(
                wlan=self.wlan,
                wlanID=self.wlanID,
                wlanSSID=self.wlanSSID))
        self.action = "enable_network_24ghz"
        summary = self.send_command()
        return summary

    # dual-band mode shut down 6ghz
    def ap_dot11_dual_band_mode_shutdown_6ghz(self):
        self.band = 'dual_band_6g'
        self.action = 'dual_band_mode_shutdown'
        summary = self.send_command()
        logger.info("ap name {ap} dot11 dual-band shutdown slot {slot} band 6ghz {band}".format(ap=self.ap, band=self.band, slot=self.ap_band_slot))
        return summary

    # dual-band mode shut down 5ghz
    def ap_dot11_dual_band_mode_shutdown_5ghz(self):
        self.band = 'dual_band_5g'
        self.action = 'dual_band_mode_shutdown'
        summary = self.send_command()
        logger.info("ap name {ap} dot11 dual-band shutdown slot {slot} band 5ghz {band}".format(ap=self.ap, band=self.band, slot=self.ap_band_slot))
        return summary

    # dual-band mode shut down 6ghz
    def ap_dot11_dual_band_no_mode_shutdown_6ghz(self):
        self.band = 'dual_band_6g'
        self.action = 'dual_band_no_mode_shutdown'
        summary = self.send_command()
        logger.info("ap name {ap} dot11 dual-band no mode shutdown slot {slot} band 6ghz {band}".format(ap=self.ap, band=self.band, slot=self.ap_band_slot))
        return summary

    # dual-band mode shut down 5ghz
    def ap_dot11_dual_band_no_mode_shutdown_5ghz(self):
        self.band = 'dual_band_5g'
        self.action = 'dual_band_no_mode_shutdown'
        summary = self.send_command()
        logger.info("ap name {ap} dot11 dual-band no mode shutdown slot {slot} band 5ghz {band}".format(ap=self.ap, band=self.band, slot=self.ap_band_slot))
        return summary

    # dual-band change radio roll 6ghz
    def config_ap_dot11_dual_band_to_6ghz(self):
        self.band = 'dual_band_6g'
        self.action = 'config_dual_band_mode'
        summary = self.send_command()
        logger.info("ap name {ap} dot11 dual-band slot {slot} band 6ghz {band}".format(ap=self.ap, band=self.band, slot=self.ap_band_slot))
        return summary

    # dual-band change radio roll 5ghz
    def config_ap_dot11_dual_band_to_5ghz(self):
        self.band = 'dual_band_5g'
        self.action = 'config_dual_band_mode'
        summary = self.send_command()
        logger.info("ap name {ap} dot11 dual-band slot {slot} band 5ghz {band}".format(ap=self.ap, band=self.band, slot=self.ap_band_slot))
        return summary

    # enable ap dual band 6ghz
    def config_ap_no_dot11_dual_band_6ghz_shutdown(self):
        self.band = 'dual_band_6g'
        self.action = "enable_operation_status"
        summary = self.send_command()
        logger.info("ap name {ap} dot11 {band} shutdown {slot}  (enable ap)".format(ap=self.ap, band=self.band, slot=self.ap_band_slot))
        return summary

    # enable ap dual band 5ghz
    def config_ap_no_dot11_dual_band_5ghz_shutdown(self):
        self.band = 'dual_band_5g'
        self.action = "enable_operation_status"
        summary = self.send_command()
        logger.info("ap name {ap} dot11 {band} shutdown {slot}  (enable ap)".format(ap=self.ap, band=self.band, slot=self.ap_band_slot))
        return summary

    # enable ap 6ghz
    def config_ap_no_dot11_6ghz_shutdown(self):
        self.band = '6g'
        self.action = "enable_operation_status"
        summary = self.send_command()
        logger.info("ap name {ap} dot11 {band}hz shutdown {slot}  (enable ap)".format(ap=self.ap, band=self.band, slot=self.ap_band_slot))
        return summary

    # enable ap 5ghz
    def config_ap_no_dot11_5ghz_shutdown(self):
        self.band = '5g'
        self.action = "enable_operation_status"
        summary = self.send_command()
        logger.info("ap name {ap} dot11 {band}hz shutdown {slot}  (enable ap)".format(ap=self.ap, band=self.band, slot=self.ap_band_slot))
        return summary

    # enable ap 24ghz
    def config_ap_no_dot11_24ghz_shutdown(self):
        self.band = '24g'
        self.action = "enable_operation_status"
        summary = self.send_command()
        logger.info("ap name {ap} dot11 {band}hz shutdown {slot}  (enable ap)".format(ap=self.ap, band=self.band, slot=self.ap_band_slot))
        return summary

    def show_11r_logs(self):
        logger.info("sh wi stats client detail | inc 11r ")
        self.action = "11r_logs"
        summary = self.send_command()
        return summary

    def enable_ft_psk_cc(self):
        logger.info("enable ft and akm ft+psk ")
        self.action = "enable_ft_akm_ftpsk"
        summary = self.send_command()
        return summary

    def enable_ft_sae_cc(self):
        logger.info("enable ft and akm ft+sae ")
        self.action = "enable_ft_akm_ftsae"
        summary = self.send_command()
        return summary

    def enable_ftotd_psk_cc(self):
        logger.info("enable ft , ft over the ds  and akm ft+psk ")
        self.action = "enable_ftotd_akm_ftpsk"
        summary = self.send_command()
        print(summary)
        return summary

    def enable_ft_dot1x_wpa3_cc(self):
        logger.info("enable ft dot1x ")
        self.action = "enable_ft_wpa3_dot1x"
        summary = self.send_command()
        print(summary)
        return summary

    def enable_ft_dot1x_sha256_wpa3_cc(self, radius):
        logger.info("enable ft dot1x and sha256")
        self.value = radius
        self.action = "enable_ft_wpa3_dot1x_sha256"
        summary = self.send_command()
        print(summary)
        return summary

    # Adjusting the number of spatial streams in the controller
    def ap_dot11_dot11ax_mcs_tx_index_spatial_stream(self):
        logger.info("ap_dot11_dot11ax_mcs_tx_index_spatial_stream")
        self.action = "ap_dot11_dot11ax_mcs_tx_index_spatial_stream"
        summary = self.send_command()
        logger.info(summary)
        return summary


    # disablespatial streams
    def no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream(self):
        logger.info("no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream")
        self.action = "no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream"
        summary = self.send_command()
        logger.info(summary)
        return summary

    def show_wireless_client_sum_cc(self):
        logger.info("show wireless client sumarry")
        self.action = "show_wireless_client_sumry"
        summary = self.send_command()
        return summary

    def show_wireless_client_mac_details(self, mac):
        logger.info("show wireless client mac-address details")
        self.action = "show_client_macadd_detail"
        self.value = mac
        summary = self.send_command()
        return summary

    def debug_wireless_mac_cc(self, mac):
        logger.info("debug wireless mac <mac> to enable ra_tracing")
        self.action = 'debug_wieless_mac'
        self.value = mac
        summary = self.send_command()
        return summary

    def no_debug_wireless_mac_cc(self, mac):
        logger.info("no debug wireless mac <mac> to disable ra_tracing")
        self.action = 'no_debug_wieless_mac'
        self.value = mac
        summary = self.send_command()
        return summary

    def get_ra_trace_files__cc(self):
        logger.info("get ra trace files")
        self.action = 'get_ra_trace_files'
        summary = self.send_command()
        return summary

    def get_data_ra_trace_file_cc(self, file):
        logger.info("get data of ra trace file")
        self.action = 'get_data_ra_trace_files'
        self.value = file
        summary = self.send_command()
        return summary

    def get_mc_address(self):
        wlan_sumry = self.show_wireless_client_sum_cc()
        print(wlan_sumry)
        ele_list = [y for y in (x.strip() for x in wlan_sumry.splitlines()) if y]
        print(ele_list)
        indices = [i for i, s in enumerate(ele_list) if 'MAC Address' in s]
        data = indices[1]
        data2 = data + 1
        data3 = data + 2
        data4 = data + 3
        # ele_list[data]
        y = ele_list[data3]
        print(y)
        list_ = []
        list_.append(y)
        z = list_[0].split(" ")
        print(z[0])
        return z[0]

    def del_ra_trace_file_cc(self, file):
        logger.info("delete ra trace file")
        self.action = 'del_ra_trace_file'
        self.value = file
        summary = self.send_command()
        return summary

    # todo have the series passed in 
    # if args.series == "9800":
    def console_setup(self):
        self.no_logging_console()
        self.line_console_0()

    def read_ap_config_radio_role(self):
        logger.info("read the AP if in Manual ") 
        pss = self.show_ap_name_config_role()

        for line in pss.splitlines():
            if 'Radio Role Op' in line: 
                if 'Manual' in line:
                    self.ap_config_radio_role = 'Manual'

                elif 'Auto' in line:
                    self.ap_config_radio_role = 'Auto'
        logger.info("ap config radio role: {role}".format(role=self.ap_config_radio_role))

    # read AP txpower values
    def show_ap_tx_power_config(self):
        logger.info("show ap tx power levels, show ap name <ap> config dot 11 <band>")
        self.action = "show_ap_tx_power_config"
        summary = self.send_command()
        return summary

    def get_ap_tx_power_config(self):
        summary = self.show_ap_tx_power_config()
        self.ap_current_tx_power_level = 'NA'
        self.ap_tx_power_dbm = 'NA'
        self.ap_num_power_levels = 'NA'
        for line in summary.splitlines():
            pat = "Number of Supported Power Levels\\s+\\S+\\s+(\\S+)"
            m = re.search(pat, line)
            if (m is not None):
                self.ap_num_power_levels = m.group(1)
        for line in summary.splitlines():
            pat = "Current Tx Power Level\\s+\\S+\\s+(\\S)"
            m = re.search(pat, line)
            if (m is not None):
                self.ap_current_tx_power_level = m.group(1)
                break
        if self.ap_current_tx_power_level is not None:
            for line in summary.splitlines():
                pat = 'Tx Power Level %s\\s+\\S+\\s+(\\S+)' % (self.ap_current_tx_power_level)
                m = re.search(pat, line)
                if (m is not None):
                    self.ap_tx_power_dbm = m.group(1)
                    break

        logger.info("Total Power Levels: {levels} Current Power Level: {level} Current Tx Power: {tx_power}".
            format(levels=self.ap_num_power_levels,level=self.ap_current_tx_power_level,tx_power=self.ap_tx_power_dbm))

    def read_country_code_and_regulatory_domain(self):
        logger.info("read_conutry_code_and_regulatory_domain")

        self.regulatory_domain = "NA"
        self.country_code = "NA"
        
        pss = self.show_ap_summary()
        logger.info(pss)

        # Find our current regulatory domain so we can report it properly
        searchap = False
        for line in pss.splitlines():
            if (line.startswith("---------")):
                searchap = True
                continue
            # the summaries are different between the 9800 series controller and the 3504 series
            # if the output changes then the following pattern/regular expression parcing needs to be changed
            # this site may help: https://regex101.com/
            # when using https://regex101.com/ for tool beginning of string begins with ^
            if (searchap):
                if self.series == "9800":
                    pat = "%s\\s+\\S+\\s+\\S+\\s+\\S+\\s+\\S+\\s+%s\\s+(\\S+)" % (self.ap, self.testbed_location)
                else:
                    pat = "%s\\s+\\S+\\s+\\S+\\s+\\S+\\s+\\S+.*  (\\S+)\\s+\\S+\\s*\\S+\\s+\\[" % (self.ap)
                m = re.search(pat, line)
                if (m is not None):
                    self.regulatory_domain = m.group(1)
                    logger.info("Regulatory Domain in AP Summary : {domain}".format(domain=myrd))
                    break
        #Try for new formatting  
        searchap = False              
        if self.regulatory_domain == "NA":
            for line in pss.splitlines():
                if (line.startswith("---------")):
                    searchap = True
                    continue
                if (searchap):
                    pat = "%s\\s+\\S+\\s+\\S+\\s+\\S+\\s+\\S+\\s+(\\S+)\s+(\\S+)" % (self.ap)
                    m = re.search(pat, line)
                    if (m is not None):
                        self.country_code = m.group(1)
                        self.regulatory_domain = m.group(2)
                        logger.info("Regulatory Domain in show AP Summary : Regulatory {domain} Country Code {cc}".format(domain=self.regulatory_domain, cc=self.country_code))
                        break

        if self.regulatory_domain == "NA":
            logger.error("Regulatory domain is blank: --testbed_location <show ap summary Location> : location entered {location}".format(location=args.testbed_location))



# This next section is to allow for tests to be created without

# This sample runs thought dumping status
def sample_test_dump_status(cs):
    # This dumps a lot of information cs.show_ap_config_slots()
    cs.show_ap_summary()
    # cs.no_logging_console()
    # cs.line_console_0()
    if cs.band in ['24g', 'b']:
        cs.show_ap_bssid_24ghz()
        cs.show_ap_dot11_24gz_summary()
    elif cs.band in ['5g', 'a']:
        cs.show_ap_bssid_5ghz()
        cs.show_ap_dot11_5gz_summary()
    elif cs.band in ['6g']:
        cs.show_ap_bssid_6ghz_dual_band()
        cs.show_ap_dot11_6gz_summary()
    elif cs.band in ['dual_band_5g']:
        cs.show_ap_bssid_dual_band_5ghz_dual_band()
        cs.show_ap_dot11_dual_band_5gz_summary()
    elif cs.band in ['dual_band_6g']:
        cs.show_ap_bssid_dual_band_6ghz_dual_band()
        cs.show_ap_dot11_dual_band_6gz_summary()


# unit test for 9800 3504 controller
def main():
    # arguments
    parser = argparse.ArgumentParser(
        prog='cc_9800_3504.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            cc_9800_3504.py: wrapper for interface to a controller library
            ''',
        description='''\
NAME: cc_module_9800_3504.py

PURPOSE:
controller module for communicating to a cisco 9800 or 3504 controller
This module can be dynamically imported

SETUP:
None

EXAMPLE:
./cc_module_9800_3504.py --scheme ssh --dest localhost --port 8887 --user admin --passwd Cisco123 --ap APA453.0E7B.CF9C --series 9800 --prompt "WLC1" --timeout 10 --band '5g'

# APCC9C.3EF4.DDE0
./cc_module_9800_3504.py --scheme ssh --dest localhost --port 8887 --user admin --passwd Cisco123 --ap APCC9C.3EF4.DDE0 --series 9800 --prompt "WLC1" --timeout 10 --band '5g'

COPYWRITE
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

INCLUDE_IN_README
---------
            ''')

# sample command
# ./cc_module_9800_3504.py --scheme ssh --dest localhost --port 8887 --user admin --passwd Cisco123 --ap APA453.0E7B.CF9C --series 9800 --prompt "WLC1" --timeout 10 --band '5g'
    parser.add_argument("--dest", type=str, help="address of the cisco controller", required=True)
    parser.add_argument("--port", type=str, help="control port on the controller", required=True)
    parser.add_argument("--user", type=str, help="credential login/username", required=True)
    parser.add_argument("--passwd", type=str, help="credential password", required=True)
    parser.add_argument("--ap", type=str, help="ap name APA453.0E7B.CF9C", required=True)
    parser.add_argument("--ap_band_slot_24g", type=str, help="ap_band_slot_24g", default='0')
    parser.add_argument("--ap_band_slot_5g", type=str, help="ap_band_slot_5g", default='1')
    parser.add_argument("--ap_band_slot_6g", type=str, help="ap_band_slot_6g", default='2')
    parser.add_argument("--ap_dual_band_slot_5g", type=str, help="ap_dual_band_slot_5g", default='2')
    parser.add_argument("--ap_dual_band_slot_6g", type=str, help="ap_dual_band_slot_6g", default='2')
    parser.add_argument("--prompt", type=str, help="controller prompt", required=True)
    parser.add_argument("--band", type=str, help="band to test 24g, 5g, 6g, dual_band_5g, dual_band_6g", required=True)
    parser.add_argument("--series", type=str, help="controller series", choices=["9800", "3504"], required=True)
    parser.add_argument("--scheme", type=str, choices=["serial", "ssh", "telnet"], help="Connect via serial, ssh or telnet")
    parser.add_argument("--timeout", type=str, help="timeout value", default=3)
    parser.add_argument("--lf_logger_config_json", help="[debug configuration] --lf_logger_config_json <json file> , json configuration of logger")
    parser.add_argument("--debug", help='--debug flag present debug on  enable debugging', action='store_true')
    parser.add_argument('--log_level', default=None, help='--log_level <level>', choices=['debug', 'info', 'warning', 'error', 'critical'])

    args = parser.parse_args()

    # set up logger , do not delete
    logger_config = lf_logger_config.lf_logger_config()

    # set the logger level to debug
    if args.debug:
        logger_config.set_level('debug')

    if args.log_level:
        logger_config.set_level(args.log_level)

    # lf_logger_config_json will take presidence to changing debug levels
    if args.lf_logger_config_json:
        # logger_config.lf_logger_config_json = "lf_logger_config.json"
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()

    cs = create_controller_series_object(
        scheme=args.scheme,
        dest=args.dest,
        user=args.user,
        passwd=args.passwd,
        prompt=args.prompt,
        series=args.series,
        ap=args.ap,
        port=args.port,
        band=args.band,
        timeout=args.timeout)
    # TODO add ability to select tests
    # cs.show_ap_summary()
    # summary = cs.show_ap_bssid_5ghz()
    # logger.info(summary)

    # sample to dump status
    # sample_test_dump_status(cs=cs)
    cs.show_wireless_client_sum_cc()


if __name__ == "__main__":
    main()
