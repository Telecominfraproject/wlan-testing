#!/usr/bin/env python3

"""
NAME: cc_module_9800_3504.py

PURPOSE:
controller module for communicating to a cisco 9800 or 3504 controller
This module can be dynamically imported

SETUP:
None

EXAMPLE:
    There is a unit test included to try sample command scenarios


COPYWRITE
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
        if band is None:
            raise ValueError('Controller band  must be set')
        else:
            self.band = band
        if port is None:
            raise ValueError('Controller port  must be set')
        else:
            self.port = port

        if timeout is None:
            logger.info("timeout not set default to 10 sec")
            self.timeout = '10'
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
        self.tx_power = None
        self.channel = None
        self.bandwidth = None
        self.action = None
        self.value = None
        self.command = []
        self.command_extend = []
        self.info = "Cisco 9800 Controller Series"
        self.pwd = pwd

    # TODO update the wifi_ctl_9800_3504 to use 24g, 5g, 6g

    def convert_band(self):
        if self.band == '24g':
            self.band = 'b'
        elif self.band == '5g':
            self.band = 'a'
        elif self.band == '6g':
            self.band = '6g'
        elif self.band == 'a' or self.band == 'b':
            pass
        else:
            logger.critical("band needs to be set 24g 5g or 6g")
            raise ValueError("band needs to be set 24g 5g or 6g")

    # TODO consolidate the command formats
    def send_command(self):
        # for backward compatibility wifi_ctl_9800_3504 expects 'a' for 5g and 'b' for 24b
        self.convert_band()
        logger.info("action {action}".format(action=self.action))

        # Command base
        if self.pwd is None:
            self.command = ["./wifi_ctl_9800_3504.py", "--scheme", self.scheme, "--dest", self.dest,
                            "--user", self.user, "--passwd", self.passwd, "--prompt", self.prompt,
                            "--series", self.series, "--ap", self.ap, "--band", self.band, "--port", self.port]
        else:
            self.command = [str(str(self.pwd) + "/wifi_ctl_9800_3504.py"), "--scheme", self.scheme, "--dest", self.dest,
                            "--user", self.user, "--passwd", self.passwd, "--prompt", self.prompt,
                            "--series", self.series, "--ap", self.ap, "--band", self.band, "--port", self.port]
        # Generate command
        if self.action in ['cmd', 'txPower', 'channel', 'bandwidth']:

            self.command_extend = ["--action", self.action, "--value", self.value]
            self.command.extend(self.command_extend)

        elif self.action in ["create_wlan", "create_wlan_wpa2", "create_wlan_wpa3"]:

            if self.action in ["create_wlan"]:
                self.command_extend = ["--action", self.action, "--wlan", self.wlan,
                                       "--wlanID", self.wlanID, "--wlanSSID", self.wlanSSID]
            else:
                self.command_extend = ["--action", self.action, "--wlan", self.wlan,
                                       "--wlanID", self.wlanID, "--wlanSSID", self.wlanSSID, "--security_key", self.security_key]
            self.command.extend(self.command_extend)

        elif self.action in ["enable_wlan", "disable_wlan", "delete_wlan"]:

            self.command_extend = ["--action", self.action, "--wlan", self.wlan]
            self.command.extend(self.command_extend)

        elif self.action in ["wireless_tag_policy"]:

            self.command_extend = ["--action", self.action, "--wlan", self.wlan, "--tag_policy", self.tag_policy, "--policy_profile", self.policy_profile]
            self.command.extend(self.command_extend)

        # possible need to look for exact command
        elif self.action in ["summary", "show_radio", "no_logging_console", "line_console_0", "show_ap_wlan_summary", "show_wlan_summary",
                             "advanced", "disable", "disable_network_5ghz", "disable_network_24ghz",
                             "manual", "auto", "enable_network_5ghz", "enable_network_24ghz", "enable"]:

            self.command_extend = ["--action", self.action]
            self.command.extend(self.command_extend)

        else:
            logger.critical("action {action} not supported".format(action=self.action))
            raise ValueError("action {action} not supported".format(action=self.action))

        # logger.info(pformat(self.command))
        logger.info(self.command)
        # TODO change the subprocess.run to pOpen
        summary_output = ''
        summary = subprocess.Popen(self.command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(summary.stdout.readline, ''):
            logger.debug(line)
            summary_output += line
            # sys.stdout.flush() # please see comments regarding the necessity of this line
        summary.wait()
        logger.info(summary_output)  # .decode('utf-8', 'ignore'))
        # logger.info(advanced.stderr.decode('utf-8', 'ignore'))
        return summary_output

    def show_ap_config_slots(self):
        logger.info("show ap config slots")
        self.action = "cmd"
        self.value = "show ap config slots"
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

    def show_ap_dot11_5gz_summary(self):
        logger.info("show_ap_dot11_5gz_summary")
        self.band = '5g'
        self.action = "advanced"
        summary = self.send_command()
        return summary

    def show_ap_dot11_24gz_summary(self):
        logger.info("show_ap_dot11_24gz_summary")
        self.band = '24g'
        self.action = "advanced"
        summary = self.send_command()
        return summary

    def show_ap_dot11_5gz_shutdown(self):
        logger.info("ap name {name} dot11 5ghz shutdown")
        self.band = '5g'
        self.action = "disable"
        summary = self.send_command()
        return summary

    def show_ap_dot11_24gz_shutdown(self):
        logger.info("ap name {name} dot11 24ghz shutdown")
        self.band = '24g'
        self.action = "disable"
        summary = self.send_command()
        return summary

    def wlan_shutdown(self):
        logger.info("wlan {wlan} shutdown wlanID {wlanID} wlanSSID {wlanSSID}".format(wlan=self.wlan, wlanID=self.wlanID, wlanSSID=self.wlanSSID))
        self.action = "disable_wlan"
        summary = self.send_command()
        return summary

    def ap_dot11_5ghz_shutdown(self):
        logger.info("ap dot11 5ghz shutdown")
        self.action = "disable_network_5ghz"
        summary = self.send_command()
        return summary

    def ap_dot11_24ghz_shutdown(self):
        logger.info("wlan {wlan} shutdown".format(wlan=self.wlan))
        self.action = "disable_network_24ghz"
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

    def config_dot11_5ghz_disable_network(self):
        logger.info("config_dot11_5ghz_disable_network")
        self.action = "cmd"
        self.value = "config 802.11a disable network"
        summary = self.send_command()
        return summary

    def config_dot11_24ghz_disable_network(self):
        logger.info("config_dot11_24ghz_disable_network")
        self.action = "cmd"
        self.value = "config 802.11b disable network"
        summary = self.send_command()
        return summary

    # txPower
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
    def config_dot11_6ghz_channel(self):
        logger.info("config_dot11_5ghz_channel {channel}".format(channel=self.channel))
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
        self.action = "channel"
        self.value = "{channel}".format(channel=self.channel)
        summary = self.send_command()
        return summary

    # set bandwidth
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
        logger.info("config_wlan wlan: Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID}".format(wlan=self.wlan, wlanID=self.wlanID, wlanSSID=self.wlanSSID))
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
        logger.info("config_wlan_wpa2 wlan: Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID} security_key {security_key}".format(wlan=self.wlan, wlanID=self.wlanID, wlanSSID=self.wlanSSID, security_key=self.security_key))
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
        logger.info("config_wlan_wpa3 wlan: Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID}".format(wlan=self.wlan, wlanID=self.wlanID, wlanSSID=self.wlanSSID))
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
        logger.info("config_enable_wlan_send_no_shutdown: Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID}".format(wlan=self.wlan, wlanID=self.wlanID, wlanSSID=self.wlanSSID))
        self.action = "enable_wlan"
        summary = self.send_command()
        return summary

    # enable_network_5ghz
    def config_no_ap_dot11_5ghz_shutdown(self):
        logger.info("config_no_ap_dot11_5ghz_shutdown (enable network 5ghz): Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID}".format(wlan=self.wlan, wlanID=self.wlanID, wlanSSID=self.wlanSSID))
        self.action = "enable_network_5ghz"
        summary = self.send_command()
        return summary

    # enable_network_24ghz
    def config_no_ap_dot11_24ghz_shutdown(self):
        logger.info("config_no_ap_dot11_24ghz_shutdown (enable network 24ghz): Profile name {wlan} wlanID {wlanID} wlanSSID {wlanSSID}".format(wlan=self.wlan, wlanID=self.wlanID, wlanSSID=self.wlanSSID))
        self.action = "enable_network_24ghz"
        summary = self.send_command()
        return summary

    # enable ap 5ghz
    def config_ap_no_dot11_5ghz_shutdown(self):
        logger.info("ap name %s dot11 5ghz shutdown {ap}  (enable ap)".format(ap=self.ap))
        self.band = '5g'
        self.action = "enable"
        summary = self.send_command()
        return summary

    # enable ap 24ghz
    def config_ap_no_dot11_24ghz_shutdown(self):
        logger.info("ap name %s dot11 24ghz shutdown {ap} (enable ap)".format(ap=self.ap))
        self.band = '24g'
        self.action = "enable"
        summary = self.send_command()
        return summary


# This next section is to allow for tests to be created without
# please do not delete
# modifying existing tests.

# This sample runs thought dumping status
def sample_test_dump_status(cs):
    cs.show_ap_config_slots()
    cs.show_ap_summary()
    cs.no_logging_console()
    cs.line_console_0()
    cs.show_wlan_summary()
    cs.show_ap_dot11_5gz_summary()


# This sample runs though the sequence of commands used
# by tx_power script

# TODO unit test for 6g wlan, 5g wlan, 2g wlan, and all three
def sample_test_tx_power_sequence(cs):

    # series of commands to create a wlan , similiar to how tx_power works.
    # pass in the ap and band from the command line
    # cs.ap = 'APA453.0E7B.CF9C'
    # cs.band = '5g'

    logger.info("sample_test_tx_power_sequence")
    # This needs to be here to disable and delete
    cs.wlan = 'wpa2_wlan_3'
    cs.wlanID = '3'
    cs.wlanSSID = 'wpa2_wlan_3'
    cs.tx_power = '1'

    cs.tag_policy = 'RM204-TB1'
    cs.policy_profile = 'default-policy-profile'

    # no_logging_console
    cs.no_logging_console()
    # line_console_0
    cs.line_console_0()
    # summary
    cs.show_ap_summary()

    # disable
    cs.show_ap_dot11_5gz_shutdown()
    cs.show_ap_dot11_24gz_shutdown()

    # disable_wlan
    cs.wlan_shutdown()
    # disable_network_5ghz
    cs.ap_dot11_5ghz_shutdown()
    # disable_network_24ghz
    cs.ap_dot11_24ghz_shutdown()
    # manual
    cs.ap_dot11_5ghz_radio_role_manual_client_serving()
    cs.ap_dot11_24ghz_radio_role_manual_client_serving()

    # Configuration for 5g

    # txPower
    cs.config_dot11_5ghz_tx_power()
    cs.bandwidth = '20'
    # bandwidth (to set to 20 if channel change does not support)
    cs.config_dot11_5ghz_channel_width()
    cs.channel = '100'
    # channel
    cs.config_dot11_5ghz_channel()
    cs.bandwidth = '40'
    # bandwidth
    cs.config_dot11_5ghz_channel_width()
    # show_wlan_summary
    cs.show_wlan_summary()

    # Configuration for 6g
    # txPower
    # cs.config_dot11_6ghz_tx_power()
    # cs.bandwidth = '20'
    # # bandwidth (to set to 20 if channel change does not support)
    # cs.config_dot11_6ghz_channel_width()
    # cs.channel = '36'
    # # channel
    # cs.config_dot11_6ghz_channel()
    # cs.bandwidth = '40'
    # # bandwidth
    # cs.config_dot11_6ghz_channel_width()
    # # show_wlan_summary
    # cs.show_wlan_summary()

    # delete_wlan
    # TODO (there were two in tx_power the logs)
    # need to check if wlan present
    # delete wlan
    cs.config_no_wlan()

    # Create open
    # cs.wlan = 'open-wlan_3'
    # cs.wlanID = '3'
    # cs.wlanSSID = 'open-wlan_3'

    # create_wlan  open
    # cs.wlan = 'open-wlan'
    # cs.wlanID = '1'
    # cs.wlanSSID = 'open-wlan'
    # cs.config_wlan_open()

    # create_wlan_wpa2
    cs.config_wlan_wpa2()

    # create_wlan_wpa3
    # cs.wlan = 'wpa3_wlan_4'
    # cs.wlanID = '4'
    # cs.wlanSSID = 'wpa3_wlan_4'
    # cs.security_key = 'hello123'
    # cs.config_wlan_wpa3()

    # wireless_tag_policy
    cs.config_wireless_tag_policy_and_policy_profile()
    # enable_wlan
    cs.config_enable_wlan_send_no_shutdown()
    # enable_network_5ghz
    cs.config_no_ap_dot11_5ghz_shutdown()
    # enable_network_24ghz
    # cs.config_no_ap_dot11_5ghz_shutdown()
    # enable
    cs.config_ap_no_dot11_5ghz_shutdown()
    # config_ap_no_dot11_24ghz_shutdown
    # advanced
    cs.show_ap_dot11_5gz_summary()
    # cs.show_ap_dot11_24gz_summary()
    # show_wlan_summary
    cs.show_wlan_summary()


def test_config_tx_power_5g_open(cs):

    logger.info("test_config_tx_power_open")
    # configure once at the top
    cs.wlan = 'open-wlan-15'
    cs.wlanID = '15'
    cs.wlanSSID = 'open-wlan-15'
    cs.config_wlan_open()

    # wireless_tag_policy
    cs.tag_policy = 'RM204-TB1'
    cs.policy_profile = 'default-policy-profile'
    cs.config_wireless_tag_policy_and_policy_profile()

    cs.tx_power = '1'
    cs.channel = '100'
    cs.bandwidth = '40'

    # no_logging_console
    cs.no_logging_console()
    # line_console_0
    cs.line_console_0()
    # summary
    cs.show_ap_summary()

    # disable
    cs.show_ap_dot11_5gz_shutdown()
    cs.show_ap_dot11_24gz_shutdown()

    # disable_wlan only need wlan
    cs.wlan_shutdown()
    # disable_network_5ghz
    cs.ap_dot11_5ghz_shutdown()
    # disable_network_24ghz
    cs.ap_dot11_24ghz_shutdown()
    # manual
    cs.ap_dot11_5ghz_radio_role_manual_client_serving()
    cs.ap_dot11_24ghz_radio_role_manual_client_serving()

    # Configuration for 5g

    # txPower
    cs.config_dot11_5ghz_tx_power()
    # bandwidth (to set to 20 if channel change does not support)
    cs.bandwidth = '20'
    cs.config_dot11_5ghz_channel_width()
    # channel
    cs.config_dot11_5ghz_channel()
    # bandwidth
    cs.bandwidth = '40'
    cs.config_dot11_5ghz_channel_width()
    # show_wlan_summary
    cs.show_wlan_summary()

    # delete_wlan
    # TODO (there were two in tx_power the logs)
    # need to check if wlan present
    # delete wlan
    # cs.config_no_wlan()

    # create_wlan  open

    # enable_wlan
    cs.config_enable_wlan_send_no_shutdown()
    # enable_network_5ghz
    cs.config_no_ap_dot11_5ghz_shutdown()
    # enable_network_24ghz
    cs.config_no_ap_dot11_24ghz_shutdown()
    # enable
    cs.config_ap_no_dot11_5ghz_shutdown()
    cs.config_ap_no_dot11_24ghz_shutdown()
    # config_ap_no_dot11_24ghz_shutdown
    # advanced
    cs.show_ap_dot11_5gz_summary()
    cs.show_ap_dot11_24gz_summary()
    # show_wlan_summary
    cs.show_wlan_summary()


def test_config_tx_power_wpa2(cs):

    logger.info("sample_test_tx_power_sequence")

    # no_logging_console
    cs.no_logging_console()
    # line_console_0
    cs.line_console_0()
    # summary
    cs.show_ap_summary()

    # disable
    cs.show_ap_dot11_5gz_shutdown()
    cs.show_ap_dot11_24gz_shutdown()
    # This needs to be here to disable and delete
    cs.wlan = 'wpa2_wlan_3'

    # disable_wlan
    cs.wlan_shutdown()
    # disable_network_5ghz
    cs.ap_dot11_5ghz_shutdown()
    # disable_network_24ghz
    cs.ap_dot11_24ghz_shutdown()
    # manual
    cs.ap_dot11_5ghz_radio_role_manual_client_serving()
    # cs.ap_dot11_24ghz_radio_role_manual_client_serving()
    cs.tx_power = '1'

    # Configuration for 5g

    # txPower
    cs.config_dot11_5ghz_tx_power()
    cs.bandwidth = '20'
    # bandwidth (to set to 20 if channel change does not support)
    cs.config_dot11_5ghz_channel_width()
    cs.channel = '100'
    # channel
    cs.config_dot11_5ghz_channel()
    cs.bandwidth = '40'
    # bandwidth
    cs.config_dot11_5ghz_channel_width()
    # show_wlan_summary
    cs.show_wlan_summary()

    # delete_wlan
    # TODO (there were two in tx_power the logs)
    # need to check if wlan present
    cs.wlan = 'wpa2_wlan_3'

    # delete wlan
    cs.config_no_wlan()

    # create_wlan_wpa2
    cs.wlan = 'wpa2_wlan_3'
    cs.wlanID = '3'
    cs.wlanSSID = 'wpa2_wlan_3'
    cs.security_key = 'hello123'
    cs.config_wlan_wpa2()

    # wireless_tag_policy
    cs.tag_policy = 'RM204-TB1'
    cs.policy_profile = 'default-policy-profile'
    cs.config_wireless_tag_policy_and_policy_profile()
    # enable_wlan
    cs.config_enable_wlan_send_no_shutdown()
    # enable_network_5ghz
    cs.config_no_ap_dot11_5ghz_shutdown()
    # enable_network_24ghz
    # cs.config_no_ap_dot11_24ghz_shutdown()
    # enable
    cs.config_ap_no_dot11_5ghz_shutdown()
    # config_ap_no_dot11_24ghz_shutdown
    # advanced
    cs.show_ap_dot11_5gz_summary()
    # cs.show_ap_dot11_24gz_summary()
    # show_wlan_summary
    cs.show_wlan_summary()


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
    parser.add_argument("--prompt", type=str, help="controller prompt", required=True)
    parser.add_argument("--band", type=str, help="band to test 24g, 5g, 6g", required=True)
    parser.add_argument("--series", type=str, help="controller series", choices=["9800", "3504"], required=True)
    parser.add_argument("--scheme", type=str, choices=["serial", "ssh", "telnet"], help="Connect via serial, ssh or telnet")
    parser.add_argument("--timeout", type=str, help="timeout value", default=3)

    args = parser.parse_args()

    # set up logger , do not delete
    logger_config = lf_logger_config.lf_logger_config()

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
    summary = cs.show_ap_wlan_summary()
    logger.info(summary)

    # sample to dump status
    # sample_test_dump_status(cs=cs)

    # test sequences used by tx_power
    # sample_test_tx_power_sequence(cs=cs)

    # test_config_tx_power_5g_open(cs=cs)

    # test_config_tx_power_wpa2(cs=cs)


if __name__ == "__main__":
    main()
