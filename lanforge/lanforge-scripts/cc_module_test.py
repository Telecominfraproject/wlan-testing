#!/usr/bin/env python3

"""
NAME: cc_module_test.py

CLASSIFICATION:
module unit test

PURPOSE:
to test the dynamic import of a controller module

SETUP:
None

EXAMPLE:
    There is a unit test included to try sample command scenarios
      ./cc_module_test.py --scheme ssh --dest localhost --port 8887 --user admin --passwd Cisco123 --ap AP687D.B45C.2B24 --series 9800 --prompt "WLC1" --timeout 10 --band '6g' --module 'cc_module_9800_3504' 2>&1 | tee cc_tx_output_6g.txt

COPYRIGHT:
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

INCLUDE_IN_README

RELEASE STATUS:  in development

RELEASE NOTES:
"""

import sys
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

import argparse
import logging
import importlib
import os
from time import sleep


sys.path.append(os.path.join(os.path.abspath(__file__ + "././")))

logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")


class create_module_test_object:
    def __init__(self,
                 cs=None):
        if cs is None:
            raise ValueError('Controller series must be passed in ')
        else:
            self.cs = cs

# please do not delete
# modifying existing tests.

    # This sample runs thought dumping status
    def sample_test_dump_status(self):
        self.cs.show_ap_config_slots()
        self.cs.show_ap_summary()
        self.cs.no_logging_console()
        self.cs.line_console_0()
        self.cs.show_wlan_summary()
        # cs.show_ap_dot11_5gz_summary()
        # cs.show_ap_dot11_24gz_summary()
        self.cs.show_ap_bssid_5ghz()

    # sample setting dtim dot11 5ghz : delivery traffic indication message
    def sample_test_setting_dtim(self):
        logger.info("sample_test_setting_dtim")
        # This needs to be here to disable and delete
        self.cs.dtim = '2'

        self.cs.wlan = '6G-wpa3-AP3'
        self.cs.wlanID = '7'
        self.cs.wlanSSID = '6g-wpa3-AP3'
        self.cs.tx_power = '1'
        self.cs.security_key = 'hello123'

        self.cs.tag_policy = 'RM204-TB1-AP5'
        self.cs.policy_profile = 'default-policy-profile'
        # summary
        self.cs.show_ap_summary()

        # disable
        self.cs.show_ap_dot11_6gz_shutdown()
        self.cs.show_ap_dot11_5gz_shutdown()
        self.cs.show_ap_dot11_24gz_shutdown()

        # disable_wlan
        self.cs.wlan_shutdown()
        # disable_network_6ghz
        self.cs.ap_dot11_6ghz_shutdown()
        # disable_network_5ghz
        self.cs.ap_dot11_5ghz_shutdown()
        # disable_network_24ghz
        self.cs.ap_dot11_24ghz_shutdown()
        # manual
        self.cs.ap_dot11_6ghz_radio_role_manual_client_serving()
        self.cs.ap_dot11_5ghz_radio_role_manual_client_serving()
        self.cs.ap_dot11_24ghz_radio_role_manual_client_serving()

        # Configuration for 5g

        # txPower
        self.cs.config_dot11_6ghz_tx_power()
        self.cs.config_dot11_5ghz_tx_power()
        # self.cs.bandwidth = '20'
        # bandwidth (to set to 20 if channel change does not support)
        # self.cs.config_dot11_5ghz_channel_width()
        self.cs.channel = '33'

        # channel
        self.cs.config_dot11_6ghz_channel()
        # self.cs.config_dot11_5ghz_channel()
        self.cs.bandwidth = '40'
        # bandwidth
        self.cs.config_dot11_6ghz_channel_width()
        # show_wlan_summary
        self.cs.show_wlan_summary()

        # delete wlan
        # self.cs.config_no_wlan()

        # create_wlan_wpa3
        self.cs.config_wlan_wpa3()

        # wireless_tag_policy
        self.cs.config_wireless_tag_policy_and_policy_profile()

        # show_wlan_summary
        self.cs.show_wlan_summary()

        # somehow during the configure the WLAN gets enabled
        # disable_wlan
        self.cs.wlan_shutdown()

        # show_wlan_summary
        self.cs.show_wlan_summary()

        # % WLAN needs to be disabled before performing this operation.
        self.cs.config_dtim_dot11_6ghz()

        # enable_wlan
        self.cs.config_enable_wlan_send_no_shutdown()
        # enable_network_6ghz
        self.cs.config_no_ap_dot11_6ghz_shutdown()
        # enable_network_24ghz
        # self.cs.config_no_ap_dot11_5ghz_shutdown()
        # enable
        self.cs.config_ap_no_dot11_6ghz_shutdown()
        # config_ap_no_dot11_24ghz_shutdown
        # advanced
        self.cs.show_ap_dot11_6gz_summary()
        # self.cs.show_ap_dot11_24gz_summary()
        # show_wlan_summary
        self.cs.show_wlan_summary()

    # This sample runs though the sequence of commands used
    # by tx_power script

    # TODO unit test for 6g wlan, 5g wlan, 2g wlan, and all three

    def sample_test_tx_power_sequence(self):

        # series of commands to create a wlan , similiar to how tx_power works.
        # pass in the ap and band from the command line
        # self.cs.ap = 'APA453.0E7B.CF9C'
        # self.cs.band = '5g'

        logger.info("sample_test_tx_power_sequence")
        # This needs to be here to disable and delete
        self.cs.wlan = 'wpa2_wlan_3'
        self.cs.wlanID = '3'
        self.cs.wlanSSID = 'wpa2_wlan_3'
        self.cs.tx_power = '1'
        self.cs.security_key = 'wpa2_wlan_3'

        self.cs.tag_policy = 'RM204-TB1'
        self.cs.policy_profile = 'default-policy-profile'

        # no_logging_console
        self.cs.no_logging_console()
        # line_console_0
        self.cs.line_console_0()
        # summary
        self.cs.show_ap_summary()

        # disable
        self.cs.show_ap_dot11_5gz_shutdown()
        self.cs.show_ap_dot11_24gz_shutdown()

        # disable_wlan
        self.cs.wlan_shutdown()
        # disable_network_5ghz
        self.cs.ap_dot11_5ghz_shutdown()
        # disable_network_24ghz
        self.cs.ap_dot11_24ghz_shutdown()
        # manual
        self.cs.ap_dot11_5ghz_radio_role_manual_client_serving()
        self.cs.ap_dot11_24ghz_radio_role_manual_client_serving()

        # Configuration for 5g

        # txPower
        self.cs.config_dot11_5ghz_tx_power()
        self.cs.bandwidth = '20'
        # bandwidth (to set to 20 if channel change does not support)
        self.cs.config_dot11_5ghz_channel_width()
        self.cs.channel = '100'
        # channel
        self.cs.config_dot11_5ghz_channel()
        self.cs.bandwidth = '40'
        # bandwidth
        self.cs.config_dot11_5ghz_channel_width()
        # show_wlan_summary
        self.cs.show_wlan_summary()

        # Configuration for 6g
        # txPower
        # self.cs.config_dot11_6ghz_tx_power()
        # self.cs.bandwidth = '20'
        # # bandwidth (to set to 20 if channel change does not support)
        # self.cs.config_dot11_6ghz_channel_width()
        # self.cs.channel = '36'
        # # channel
        # self.cs.config_dot11_6ghz_channel()
        # self.cs.bandwidth = '40'
        # # bandwidth
        # self.cs.config_dot11_6ghz_channel_width()
        # # show_wlan_summary
        # self.cs.show_wlan_summary()

        # delete_wlan
        # TODO (there were two in tx_power the logs)
        # need to check if wlan present
        # delete wlan
        self.cs.config_no_wlan()

        # Create open
        # self.cs.wlan = 'open-wlan_3'
        # self.cs.wlanID = '3'
        # self.cs.wlanSSID = 'open-wlan_3'

        # create_wlan  open
        # self.cs.wlan = 'open-wlan'
        # self.cs.wlanID = '1'
        # self.cs.wlanSSID = 'open-wlan'
        # self.cs.config_wlan_open()

        # create_wlan_wpa2
        self.cs.config_wlan_wpa2()

        # create_wlan_wpa3
        # self.cs.wlan = 'wpa3_wlan_4'
        # self.cs.wlanID = '4'
        # self.cs.wlanSSID = 'wpa3_wlan_4'
        # self.cs.security_key = 'hello123'
        # self.cs.config_wlan_wpa3()

        # wireless_tag_policy
        self.cs.config_wireless_tag_policy_and_policy_profile()
        # enable_wlan
        self.cs.config_enable_wlan_send_no_shutdown()
        # enable_network_5ghz
        self.cs.config_no_ap_dot11_5ghz_shutdown()
        # enable_network_24ghz
        # self.cs.config_no_ap_dot11_5ghz_shutdown()
        # enable
        self.cs.config_ap_no_dot11_5ghz_shutdown()
        # config_ap_no_dot11_24ghz_shutdown
        # advanced
        self.cs.show_ap_dot11_5gz_summary()
        # self.cs.show_ap_dot11_24gz_summary()
        # show_wlan_summary
        self.cs.show_wlan_summary()
    
    # Test dual-band 6g
    def test_config_tx_power_dual_band_6g_wpa3(self):
        # TODO : leave for now for reference
        # WLC1#show ap summary
        # Number of APs: 3
        #
        # WLC1 show ap summary
        # Number of APs: 5
        # 
        # AP Name                            Slots    AP Model              Ethernet MAC    Radio MAC       Location                          Country     IP Address                                 State         
        # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # APCC9C.3EF4.E0B0                     3      CW9166I-B             cc9c.3ef4.e0b0  10f9.20fd.e7a0  RM204-TB1-9166                    US          172.16.223.41                              Registered    
        # APCC9C.3EF1.0AE0                     3      CW9164I-B             cc9c.3ef1.0ae0  10f9.20fd.eda0  RM204-TB1-9164                    US          172.16.223.40                              Registered    
        # AP687D.B45C.25EC                     4      C9136I-B              687d.b45c.25ec  687d.b45f.c5f0  RM204-TB1-AP4                     US          172.16.222.199                             Registered    
        # AP687D.B45C.2B24                     4      C9136I-B              687d.b45c.2b24  687d.b460.04b0  RM204-TB1-AP5                     US          172.16.222.201                             Registered    
        # APA453.0E7B.CF9C                     2      C9120AXE-B            a453.0e7b.cf9c  d4ad.bda2.2ce0  RM204-TB1-AP2                     US          172.16.222.176                             Registered    

        # helper commands 
        # WLC# ap slots  , shows the ap slots shows slot dual band
        # show ap dot11 5ghz summary # slot 2 enabled 
        #   show ap slots check 
        # show ap dot11 dual-band summary # will show if in 5g or 6g
        # show ap name <ap name> dot11 
        # config file / Cisco - yaml file 
        # 
        # Flow of script -for roaming - skeleton. 
        # show ap summary 
        # configure wlan - (config file  - security combo)
        # configure band (config file , 2g/5g/6g) 
        # config channel / channel width 
        # AP min state up 
        # check admin state of AP
        # Bring down unused band ( if 2g, bring down 5g)
        # show ap dot11 5ghz summary : verify the configuration
        # Siffer capture
        # 
        # Client side connections
        # Sniffer verification - 11r configuration (if 11r)
        # check in controller/AP -> client connected -> also check 11r (sh wireless client details)
        # Ping traffic or dup traffie - insure smotth
        # Siffer capture
        # Roam
        # Siffer verification 
        # Keep the iteration for above steps from the ping traffice 
        # Common clean up 
        # Table display
        # Isaac : there needs to be a 5g ssid present for 6E to 6E roaming

        # Nikita - multi client , pass fail criteria
        # Sythia (Cisco) - 10 20 50 , table per client , number of iterations
        # Nikita - show transitions using bssi , roam time
        # Sythia would like data per client,  
        # pytest / Allure has limitations to show the proper data in Allure
        # Sythia would prefer data as compared to pass / fail

        # Nikia - how to push voice traffic when attempting to roam
        # Sythia - VO platinum, VI ,  the clients need to choose traffic (do rdp traffic)
        # ingress / egress configured by wifi controller.
        # 




        logger.info("test_config_tx_power_dual_6g_wpa3")
        # This needs to be here to disable and delete
        self.cs.wlan = '6G-wpa3'
        self.cs.wlanID = '1'
        self.cs.wlanSSID = '6G-wpa3'
        self.cs.tx_power = '1'
        self.cs.security_key = 'hello123'

        self.cs.tag_policy = 'RM204-TB1-9166'
        self.cs.policy_profile = 'default-policy-profile'

        # no_logging_console
        self.cs.no_logging_console()
        # line_console_0
        self.cs.line_console_0()
        # summary
        self.cs.show_ap_summary()
        

        # set the dual-band slot
        self.cs.ap_dual_band_slot_6g = '2'
        # configure dual-band to be 6G
        # disable dual-band mode
        if self.cs.band == "dual_band_6g":
            logger.info("ap_dot11_dual_band_mode_shutdown_6ghz")
            self.cs.ap_dot11_dual_band_mode_shutdown_6ghz()
        elif self.cs.band == "dual_band_5g":
            logger.info("ap_dot11_dual_band_mode_shutdown_6ghz")
            self.cs.ap_dot11_dual_band_mode_shutdown_5ghz()

        # ap name APCC9C.3EF4.E0B0 dot11 dual-band slot 2 band 6ghz
        # % Error: AP APCC9C.3EF4.E0B0 Slot 2 - Failed to change band, Radio role selection is not Manual
        # set the radio role selection 
        if self.cs.band == 'dual_band_6g':
            logger.info("ap_dot11_dual_band_6ghz_radio_role_manual_client_serving")
            self.cs.ap_dot11_dual_band_6ghz_radio_role_manual_client_serving()
        elif self.cs.band == 'dual_band_5g':
            logger.info("ap_dot11_dual_band_5ghz_radio_role_manual_client_serving")
            self.cs.ap_dot11_dual_band_5ghz_radio_role_manual_client_serving()
        # elif self.cs.band == '6g':
        #    self.cs.ap_dot11_6ghz_radio_role_manual_client_serving()
        # self.cs.ap_dot11_5ghz_radio_role_manual_client_serving()
        # self.cs.ap_dot11_24ghz_radio_role_manual_client_serving()


        # config dual-band mode
        if self.cs.band == "dual_band_6g":
            logger.info("config_ap_dot11_dual_band_to_6ghz")
            self.cs.config_ap_dot11_dual_band_to_6ghz()
        elif self.cs.band == "dual_band_5g":
            logger.info("config_ap_dot11_dual_band_to_5ghz")
            self.cs.config_ap_dot11_dual_band_to_5ghz

        # enable  dual-band mode
        if self.cs.band == "dual_band_6g":
            logger.info("ap_dot11_dual_band_no_mode_shutdown_6ghz")
            self.cs.ap_dot11_dual_band_no_mode_shutdown_6ghz()
        elif self.cs.band == "dual_band_5g":
            logger.info("ap_dot11_dual_band_no_mode_shutdown_5ghz")
            self.cs.ap_dot11_dual_band_no_mode_shutdown_5ghz()

        # Configuration for 6g
        # txPower
        # TODO is this still needed
        logger.info("config_dot11_dual_band_6ghz_tx_power")
        self.cs.config_dot11_dual_band_6ghz_tx_power()
        # channel
        # self.cs.channel = '1'
        # self.cs.channel = '33'
        self.cs.channel = '65'
        logger.info("config_dot11_dual_band_6ghz_channel")
        self.cs.config_dot11_dual_band_6ghz_channel()
        # bandwidth
        self.cs.bandwidth = '40'
        # self.cs.bandwidth = '20'
        self.cs.config_dot11_dual_band_6ghz_channel_width()

        # show_wlan_summary
        self.cs.show_wlan_summary()

        # enable_wlan
        self.cs.config_enable_wlan_send_no_shutdown()

        # enable_network_6ghz or enable_network_5ghz or enable_network_24ghz
        if self.cs.band == 'dual_band_6g':
            # enable 6g wlan
            logger.info("config_no_ap_dot11_dual_band_6ghz_shutdown")
            pss = self.cs.config_no_ap_dot11_dual_band_6ghz_shutdown()
            logger.info(pss)
            # enable 6g operation status
            pss = self.cs.config_ap_no_dot11_dual_band_6ghz_shutdown()
            logger.info(pss)

            # enable 5g wlan to show scans
            pss = self.cs.config_no_ap_dot11_5ghz_shutdown()
            logger.info(pss)
            # enable 5g operation status
            pss = self.cs.config_ap_no_dot11_5ghz_shutdown()
            logger.info(pss)

        elif self.cs.band == 'dual_band_5g':
            # enable 5g wlan
            pss = self.cs.config_no_ap_dot11_dual_band_5ghz_shutdown()
            logger.info(pss)
            # enable 5g operation status
            pss = self.cs.config_ap_no_dot11_dual_band_5ghz_shutdown()
            logger.info(pss)
        elif self.cs.band == '6g':
            # enable 6g wlan
            pss = self.cs.config_no_ap_dot11_6ghz_shutdown()
            logger.info(pss)
            # enable 6g operation status
            pss = self.cs.config_ap_no_dot11_6ghz_shutdown()
            logger.info(pss)
            # enable 5g wlan
            pss = self.cs.config_no_ap_dot11_5ghz_shutdown()
            logger.info(pss)
            # enable 5g operation status
            pss = self.cs.config_ap_no_dot11_5ghz_shutdown()
            logger.info(pss)

        # 6g needs to see the 5g bands
        elif self.cs.band == '5g':
            # enable 5g wlan
            pss = self.cs.config_no_ap_dot11_5ghz_shutdown()
            logger.info(pss)
            # enable 5g operation status
            pss = self.cs.config_ap_no_dot11_5ghz_shutdown()
            logger.info(pss)
        elif self.cs.band == '24g':
            # enable wlan 24ghz
            pss = self.cs.config_no_ap_dot11_24ghz_shutdown()
            logger.info(pss)
            # enable 24ghz operation status
            self.cs.config_ap_no_dot11_24ghz_shutdown()
            logger.info(pss)
        

        if self.cs.band == 'dual_band_6g':
            pss = self.cs.show_ap_dot11_dual_band_6gz_summary()
            logger.info("show ap dot11 dual-band (6ghz) summary")
            logger.info("ap: {ap} ap_band_slot_6g: {slot} ".format(ap=self.cs.ap, slot=self.cs.ap_band_slot))
            logger.info(pss)
        elif self.cs.band == 'dual_band_5g':
            pss = self.cs.show_ap_dot11_dual_band_5gz_summary()
            logger.info("show ap dot11 dual-band (5ghz) summary")
            logger.info("ap: {ap} ap_band_slot_5g: {slot} ".format(ap=self.cs.ap, slot=self.cs.ap_band_slot_5g))
            logger.info(pss)
        elif self.cs.band == '6g':
            pss = self.cs.show_ap_dot11_6gz_summary()
            logger.info("show ap dot11 6ghz summary")
            logger.info("ap: {ap} ap_band_slot_6g: {slot} ".format(ap=self.cs.ap, slot=self.cs.ap_band_slot_6g))
            logger.info(pss)
        elif self.cs.band == '5g':
            logger.info("show ap dot11 5ghz summary")
            logger.info("ap: {ap} ap_band_slot_5g: {slot} ".format(ap=self.cs.ap, slot=self.cs.ap_band_slot_5g))
            pss = self.cs.show_ap_dot11_5gz_summary()
            logger.info(pss)
        else:
            logger.info("show ap dot11 24ghz summary")
            logger.info("ap: {ap} ap_band_slot_24g: {slot} ".format(ap=self.cs.ap, slot=self.cs.ap_band_slot_24g))
            pss = self.cs.show_ap_dot11_24gz_summary()
            logger.info(pss)

        # Temporary Work around
        # disable the AP for 6g and enable
        if self.cs.band == '6g':
            self.cs.ap_name_shutdown()
            sleep(5)
            self.cs.ap_name_no_shutdown()

        
        # show_wlan_summary
        self.cs.show_wlan_summary()

    
    def test_config_tx_power_6g_wpa3(self):
        # TODO : leave for now for reference
        # WLC1#show ap summary
        # Number of APs: 3
        #
        # AP Name                            Slots    AP Model              Ethernet MAC    Radio MAC       Location
        # -------------------------------------------------------------------------------------------------------------------------
        # APCC9C.3EF4.DDE0                     3      CW9166I-B             cc9c.3ef4.dde0  10f9.20fd.e200  default location
        # APCC9C.3EF1.1140                     3      CW9164I-B             cc9c.3ef1.1140  10f9.20fd.fa60  default location
        # APA453.0E7B.CF9C                     2      C9120AXE-B            a453.0e7b.cf9c  d4ad.bda2.2ce0  default location

        # series of commands to create a wlan , similiar to how tx_power works.
        # pass in the ap and band from the command line
        # self.cs.ap = 'APA453.0E7B.CF9C'
        # self.cs.band = '5g'

        logger.info("test_config_tx_power_6g_wpa3")
        # This needs to be here to disable and delete
        self.cs.wlan = '6G-wpa3-AP3'
        self.cs.wlanID = '15'
        self.cs.wlanSSID = '6G-wpa3-AP3'
        self.cs.tx_power = '1'
        # self.cs.security_key = 'wpa3_wlan_4_6g'
        self.cs.security_key = 'hello123'

        self.cs.tag_policy = 'RM204-TB1-AP3'
        self.cs.policy_profile = 'default-policy-profile'

        # no_logging_console
        self.cs.no_logging_console()
        # line_console_0
        self.cs.line_console_0()
        # summary
        self.cs.show_ap_summary()

        # disable
        self.cs.show_ap_dot11_6gz_shutdown()
        self.cs.show_ap_dot11_5gz_shutdown()
        self.cs.show_ap_dot11_24gz_shutdown()

        # disable_wlan
        self.cs.wlan_shutdown()
        # disable_network_6ghz
        self.cs.ap_dot11_6ghz_shutdown()
        # disable_network_5ghz
        self.cs.ap_dot11_5ghz_shutdown()
        # disable_network_24ghz
        self.cs.ap_dot11_24ghz_shutdown()
        # manual
        self.cs.ap_dot11_6ghz_radio_role_manual_client_serving()
        self.cs.ap_dot11_5ghz_radio_role_manual_client_serving()
        self.cs.ap_dot11_24ghz_radio_role_manual_client_serving()

        # Configuration for 6g

        # Configuration for 6g
        # txPower
        # TODO is this still needed
        self.cs.config_dot11_6ghz_tx_power()
        self.cs.bandwidth = '20'
        # bandwidth (to set to 20 if channel change does not support)
        self.cs.config_dot11_6ghz_channel_width()
        self.cs.channel = '1'
        # channel
        self.cs.config_dot11_6ghz_channel()
        self.cs.bandwidth = '40'
        # bandwidth
        self.cs.config_dot11_6ghz_channel_width()
        # show_wlan_summary
        self.cs.show_wlan_summary()

        # delete_wlan
        # TODO (there were two in tx_power the logs)
        # need to check if wlan present
        # delete wlan
        self.cs.config_no_wlan()

        # create_wlan_wpa3
        self.cs.config_wlan_wpa3()

        # wireless_tag_policy
        self.cs.config_wireless_tag_policy_and_policy_profile()
        # enable_wlan
        self.cs.config_enable_wlan_send_no_shutdown()
        # enable_network_5ghz
        self.cs.config_no_ap_dot11_6ghz_shutdown()
        # enable_network_24ghz
        # self.cs.config_no_ap_dot11_5ghz_shutdown()
        # enable
        self.cs.config_ap_no_dot11_6ghz_shutdown()
        # config_ap_no_dot11_24ghz_shutdown
        # advanced
        self.cs.show_ap_dot11_6gz_summary()
        # show_wlan_summary
        self.cs.show_wlan_summary()

    def test_config_tx_power_6g_wpa3_attempt2(self):
        # TODO : leave for now for reference
        # WLC1#show ap summary
        # Number of APs: 3
        #
        # AP Name                            Slots    AP Model              Ethernet MAC    Radio MAC       Location
        # -------------------------------------------------------------------------------------------------------------------------
        # OTA
        # APCC9C.3EF4.DDE0                     3      CW9166I-B             cc9c.3ef4.dde0  10f9.20fd.e200  default location

        # Cabled together
        # APCC9C.3EF1.1140                     3      CW9164I-B             cc9c.3ef1.1140  10f9.20fd.fa60  default location
        # APA453.0E7B.CF9C                     2      C9120AXE-B            a453.0e7b.cf9c  d4ad.bda2.2ce0  default location

        # series of commands to create a wlan , similiar to how tx_power works.
        # pass in the ap and band from the command line
        # self.cs.ap = 'APA453.0E7B.CF9C'
        # self.cs.band = '5g'

        logger.info("test_config_tx_power_6g_wpa3")
        # This needs to be here to disable and delete
        self.cs.wlan = '6G-wpa3-AP3'
        self.cs.wlanID = '15'
        self.cs.wlanSSID = '6G-wpa3-AP3'
        self.cs.tx_power = '1'
        # self.cs.security_key = 'wpa3_wlan_4_6g'
        self.cs.security_key = 'hello123'

        self.cs.tag_policy = 'RM204-TB1-AP3'
        self.cs.policy_profile = 'default-policy-profile'

        # no_logging_console
        self.cs.no_logging_console()
        # line_console_0
        self.cs.line_console_0()
        # summary
        self.cs.show_ap_summary()

        # disable
        self.cs.show_ap_dot11_6gz_shutdown()
        self.cs.show_ap_dot11_5gz_shutdown()
        self.cs.show_ap_dot11_24gz_shutdown()

        # disable_wlan
        self.cs.wlan_shutdown()
        # disable_network_6ghz
        self.cs.ap_dot11_6ghz_shutdown()
        # disable_network_5ghz
        self.cs.ap_dot11_5ghz_shutdown()
        # disable_network_24ghz
        self.cs.ap_dot11_24ghz_shutdown()
        # manual
        self.cs.ap_dot11_6ghz_radio_role_manual_client_serving()
        self.cs.ap_dot11_5ghz_radio_role_manual_client_serving()
        self.cs.ap_dot11_24ghz_radio_role_manual_client_serving()

        # Configuration for 6g

        # Configuration for 6g
        # txPower
        # TODO is this still needed
        self.cs.config_dot11_6ghz_tx_power()
        self.cs.bandwidth = '20'
        # bandwidth (to set to 20 if channel change does not support)
        self.cs.config_dot11_6ghz_channel_width()
        self.cs.channel = '59'
        # channel
        self.cs.config_dot11_6ghz_channel()
        self.cs.bandwidth = '20'
        # bandwidth
        self.cs.config_dot11_6ghz_channel_width()
        # show_wlan_summary
        self.cs.show_wlan_summary()

        # delete_wlan
        # TODO (there were two in tx_power the logs)
        # need to check if wlan present
        # delete wlan
        self.cs.config_no_wlan()

        # create_wlan_wpa3
        self.cs.config_wlan_wpa3()

        # wireless_tag_policy
        self.cs.config_wireless_tag_policy_and_policy_profile()
        # enable_wlan
        self.cs.config_enable_wlan_send_no_shutdown()
        # enable_network_5ghz
        self.cs.config_no_ap_dot11_6ghz_shutdown()
        # enable_network_24ghz
        # self.cs.config_no_ap_dot11_5ghz_shutdown()
        # enable
        self.cs.config_ap_no_dot11_6ghz_shutdown()
        # config_ap_no_dot11_24ghz_shutdown
        # advanced
        self.cs.show_ap_dot11_6gz_summary()
        # show_wlan_summary
        self.cs.show_wlan_summary()

    def test_config_tx_power_5g_open(self):

        logger.info("test_config_tx_power_open")
        # configure once at the top
        self.cs.wlan = 'open-wlan-14'
        self.cs.wlanID = '14'
        self.cs.wlanSSID = 'open-wlan-14'
        self.cs.config_wlan_open()

        # wireless_tag_policy
        self.cs.tag_policy = 'RM204-TB1-AP2'
        self.cs.policy_profile = 'default-policy-profile'
        self.cs.config_wireless_tag_policy_and_policy_profile()

        self.cs.tx_power = '1'
        self.cs.channel = '149'
        self.cs.bandwidth = '40'

        # no_logging_console
        self.cs.no_logging_console()
        # line_console_0
        self.cs.line_console_0()
        # summary
        self.cs.show_ap_summary()

        # disable
        self.cs.show_ap_dot11_5gz_shutdown()
        self.cs.show_ap_dot11_24gz_shutdown()

        # disable_wlan only need wlan
        self.cs.wlan_shutdown()
        # disable_network_5ghz
        self.cs.ap_dot11_5ghz_shutdown()
        # disable_network_24ghz
        self.cs.ap_dot11_24ghz_shutdown()
        # manual
        self.cs.ap_dot11_5ghz_radio_role_manual_client_serving()
        self.cs.ap_dot11_24ghz_radio_role_manual_client_serving()

        # Configuration for 5g

        # txPower
        self.cs.config_dot11_5ghz_tx_power()
        # bandwidth (to set to 20 if channel change does not support)
        self.cs.bandwidth = '20'
        self.cs.config_dot11_5ghz_channel_width()
        # channel
        self.cs.channel = '100'
        self.cs.config_dot11_5ghz_channel()
        self.cs.channel = '5'
        self.cs.config_dot11_24ghz_channel()
        # bandwidth
        self.cs.bandwidth = '40'
        self.cs.config_dot11_5ghz_channel_width()
        # show_wlan_summary
        self.cs.show_wlan_summary()

        # delete_wlan
        # TODO (there were two in tx_power the logs)
        # need to check if wlan present
        # delete wlan
        # self.cs.config_no_wlan()

        # create_wlan  open

        # enable_wlan
        self.cs.config_enable_wlan_send_no_shutdown()
        # enable_network_5ghz
        self.cs.config_no_ap_dot11_5ghz_shutdown()
        # enable_network_24ghz
        self.cs.config_no_ap_dot11_24ghz_shutdown()
        # enable
        self.cs.config_ap_no_dot11_5ghz_shutdown()
        self.cs.config_ap_no_dot11_24ghz_shutdown()
        # config_ap_no_dot11_24ghz_shutdown
        # advanced
        self.cs.show_ap_dot11_5gz_summary()
        self.cs.show_ap_dot11_24gz_summary()
        # show_wlan_summary
        self.cs.show_wlan_summary()

        self.cs.show_ap_dot11_5gz_summary()
        self.cs.show_ap_bssid_5ghz()

    # 2g test

    def test_config_tx_power_2g_open(self):

        logger.info("test_config_tx_power_open_2g")
        # configure once at the top
        self.cs.wlan = 'open-wlan-2-2g'
        self.cs.wlanID = '2'
        self.cs.wlanSSID = 'open-wlan-2-2g'
        self.cs.config_wlan_open()

        # wireless_tag_policy
        self.cs.tag_policy = 'RM204-TB1-AP2'
        self.cs.policy_profile = 'default-policy-profile'
        self.cs.config_wireless_tag_policy_and_policy_profile()

        self.cs.tx_power = '5'
        self.cs.channel = '2'
        self.cs.bandwidth = '20'

        # no_logging_console
        self.cs.no_logging_console()
        # line_console_0
        self.cs.line_console_0()
        # summary
        self.cs.show_ap_summary()

        # disable
        self.cs.show_ap_dot11_5gz_shutdown()
        self.cs.show_ap_dot11_24gz_shutdown()

        # disable_wlan only need wlan
        self.cs.wlan_shutdown()
        # disable_network_5ghz
        self.cs.ap_dot11_5ghz_shutdown()
        # disable_network_24ghz
        self.cs.ap_dot11_24ghz_shutdown()
        # manual
        self.cs.ap_dot11_5ghz_radio_role_manual_client_serving()
        # self.cs.ap_dot11_24ghz_radio_role_manual_client_serving()

        # Configuration for 5g

        # txPower
        self.cs.config_dot11_24ghz_tx_power()
        # bandwidth (to set to 20 if channel change does not support)
        self.cs.bandwidth = '20'
        # self.cs.config_dot11_24ghz_channel_width()
        # channel
        self.cs.config_dot11_24ghz_channel()
        # bandwidth
        self.cs.bandwidth = '20'
        # self.cs.config_dot11_24ghz_channel_width()
        # show_wlan_summary
        self.cs.show_wlan_summary()

        # delete_wlan
        # TODO (there were two in tx_power the logs)
        # need to check if wlan present
        # delete wlan
        self.cs.config_no_wlan()

        # create_wlan  open

        # enable_wlan
        self.cs.config_enable_wlan_send_no_shutdown()
        # enable_network_5ghz
        # self.cs.config_no_ap_dot11_5ghz_shutdown()
        # enable_network_24ghz
        self.cs.config_no_ap_dot11_24ghz_shutdown()
        # enable
        # self.cs.config_ap_no_dot11_5ghz_shutdown()
        self.cs.config_ap_no_dot11_24ghz_shutdown()
        # config_ap_no_dot11_24ghz_shutdown
        # advanced
        # self.cs.show_ap_dot11_5gz_summary()
        self.cs.show_ap_dot11_24gz_summary()
        # show_wlan_summary
        self.cs.show_wlan_summary()

        self.cs.show_ap_dot11_24gz_summary()
        self.cs.show_ap_bssid_24ghz()

    # tb2

    def test_config_tx_power_5g_open_tb2_AP3(self):

        logger.info("test_config_tx_power_open")
        # configure once at the top
        self.cs.wlan = 'open-wlan-13'
        self.cs.wlanID = '13'
        self.cs.wlanSSID = 'open-wlan-13'
        self.cs.config_wlan_open()

        # wireless_tag_policy
        self.cs.tag_policy = 'RM204-TB2-AP1'
        self.cs.policy_profile = 'default-policy-profile'
        self.cs.config_wireless_tag_policy_and_policy_profile()

        self.cs.tx_power = '1'
        self.cs.channel = '100'
        self.cs.bandwidth = '40'

        # no_logging_console
        self.cs.no_logging_console()
        # line_console_0
        self.cs.line_console_0()
        # summary
        self.cs.show_ap_summary()

        # disable
        self.cs.show_ap_dot11_5gz_shutdown()
        self.cs.show_ap_dot11_24gz_shutdown()

        # disable_wlan only need wlan
        self.cs.wlan_shutdown()
        # disable_network_5ghz
        self.cs.ap_dot11_5ghz_shutdown()
        # disable_network_24ghz
        self.cs.ap_dot11_24ghz_shutdown()
        # manual
        self.cs.ap_dot11_5ghz_radio_role_manual_client_serving()
        self.cs.ap_dot11_24ghz_radio_role_manual_client_serving()

        # Configuration for 5g

        # txPower
        self.cs.config_dot11_5ghz_tx_power()
        # bandwidth (to set to 20 if channel change does not support)
        self.cs.bandwidth = '20'
        self.cs.config_dot11_5ghz_channel_width()
        # channel
        self.cs.config_dot11_5ghz_channel()
        # bandwidth
        self.cs.bandwidth = '40'
        self.cs.config_dot11_5ghz_channel_width()
        # show_wlan_summary
        self.cs.show_wlan_summary()

        # delete_wlan
        # TODO (there were two in tx_power the logs)
        # need to check if wlan present
        # delete wlan
        # self.cs.config_no_wlan()

        # create_wlan  open

        # enable_wlan
        self.cs.config_enable_wlan_send_no_shutdown()
        # enable_network_5ghz
        self.cs.config_no_ap_dot11_5ghz_shutdown()
        # enable_network_24ghz
        self.cs.config_no_ap_dot11_24ghz_shutdown()
        # enable
        self.cs.config_ap_no_dot11_5ghz_shutdown()
        self.cs.config_ap_no_dot11_24ghz_shutdown()
        # config_ap_no_dot11_24ghz_shutdown
        # advanced
        self.cs.show_ap_dot11_5gz_summary()
        self.cs.show_ap_dot11_24gz_summary()
        # show_wlan_summary
        self.cs.show_wlan_summary()

    def test_config_tx_power_5g_wpa2_AP3(self):

        logger.info("sample_test_tx_power_sequence on AP")

        # no_logging_console
        self.cs.no_logging_console()
        # line_console_0
        self.cs.line_console_0()
        # summary
        self.cs.show_ap_summary()

        # disable
        self.cs.show_ap_dot11_5gz_shutdown()
        self.cs.show_ap_dot11_24gz_shutdown()
        # This needs to be here to disable and delete
        self.cs.wlan = 'wpa2_wlan_3'

        # disable_wlan
        self.cs.wlan_shutdown()
        # disable_network_5ghz
        self.cs.ap_dot11_5ghz_shutdown()
        # disable_network_24ghz
        self.cs.ap_dot11_24ghz_shutdown()
        # manual
        self.cs.ap_dot11_5ghz_radio_role_manual_client_serving()
        # self.cs.ap_dot11_24ghz_radio_role_manual_client_serving()
        self.cs.tx_power = '1'

        # Configuration for 5g

        # txPower
        self.cs.config_dot11_5ghz_tx_power()
        self.cs.bandwidth = '20'
        # bandwidth (to set to 20 if channel change does not support)
        self.cs.config_dot11_5ghz_channel_width()
        self.cs.channel = '100'
        # channel
        self.cs.config_dot11_5ghz_channel()
        self.cs.bandwidth = '40'
        # bandwidth
        self.cs.config_dot11_5ghz_channel_width()
        # show_wlan_summary
        self.cs.show_wlan_summary()

        # delete_wlan
        # TODO (there were two in tx_power the logs)
        # need to check if wlan present
        self.cs.wlan = 'wpa2_wlan_3'

        # delete wlan
        self.cs.config_no_wlan()

        # create_wlan_wpa2
        self.cs.wlan = 'wpa2_wlan_3'
        self.cs.wlanID = '3'
        self.cs.wlanSSID = 'wpa2_wlan_3'
        self.cs.security_key = 'hello123'
        self.cs.config_wlan_wpa2()

        # wireless_tag_policy
        self.cs.tag_policy = 'RM204-TB1-AP3'
        self.cs.policy_profile = 'default-policy-profile'
        self.cs.config_wireless_tag_policy_and_policy_profile()
        # enable_wlan
        self.cs.config_enable_wlan_send_no_shutdown()
        # enable_network_5ghz
        self.cs.config_no_ap_dot11_5ghz_shutdown()
        # enable_network_24ghz
        # self.cs.config_no_ap_dot11_24ghz_shutdown()
        # enable
        self.cs.config_ap_no_dot11_5ghz_shutdown()
        # config_ap_no_dot11_24ghz_shutdown
        # advanced
        self.cs.show_ap_dot11_5gz_summary()
        # self.cs.show_ap_dot11_24gz_summary()
        # show_wlan_summary
        self.cs.show_wlan_summary()

    def test_config_tx_power_6g_wpa3_AP4(self):

        logger.info("sample_test_tx_power_sequence for 6G AP3 on AP")

        # no_logging_console
        self.cs.no_logging_console()
        # line_console_0
        self.cs.line_console_0()
        # summary
        self.cs.show_ap_summary()

        # disable
        self.cs.show_ap_dot11_6gz_shutdown()
        self.cs.show_ap_dot11_5gz_shutdown()
        self.cs.show_ap_dot11_24gz_shutdown()
        # This needs to be here to disable and delete
        self.cs.wlan = '6G-wpa3-AP4-2'

        # disable_wlan
        self.cs.wlan_shutdown()
        # disable_network_6ghz
        self.cs.ap_dot11_6ghz_shutdown()

        # disable_network_5ghz
        self.cs.ap_dot11_5ghz_shutdown()
        # disable_network_24ghz
        self.cs.ap_dot11_24ghz_shutdown()
        # manual
        self.cs.ap_dot11_6ghz_radio_role_manual_client_serving()
        # self.cs.ap_dot11_24ghz_radio_role_manual_client_serving()

        self.cs.ap_dot11_5ghz_radio_role_manual_client_serving()
        # self.cs.ap_dot11_24ghz_radio_role_manual_client_serving()
        self.cs.tx_power = '1'

        # Configuration for 6g

        # txPower
        self.cs.config_dot11_6ghz_tx_power()
        self.cs.bandwidth = '20'
        # bandwidth (to set to 20 if channel change does not support)
        self.cs.config_dot11_6ghz_channel_width()
        self.cs.channel = '191'
        # channel
        self.cs.config_dot11_6ghz_channel()
        self.cs.bandwidth = '20'
        # bandwidth
        self.cs.config_dot11_5ghz_channel_width()
        # show_wlan_summary
        self.cs.show_wlan_summary()

        # delete_wlan
        # TODO (there were two in tx_power the logs)
        # need to check if wlan present
        self.cs.wlan = '6G-wpa3-AP4-2'

        # delete wlan
        self.cs.config_no_wlan()

        # create_wlan_wpa2
        self.cs.wlan = '6G-wpa3-AP4-2'
        self.cs.wlanID = '1'
        self.cs.wlanSSID = '6G-wpa3-AP4-2'
        self.cs.security_key = 'hello123'
        self.cs.config_wlan_wpa2()

        # wireless_tag_policy
        self.cs.tag_policy = 'RM204-TB1-AP4'
        self.cs.policy_profile = 'default-policy-profile'
        self.cs.config_wireless_tag_policy_and_policy_profile()
        # enable_wlan
        self.cs.config_enable_wlan_send_no_shutdown()
        # enable_network_6ghz
        self.cs.config_no_ap_dot11_6ghz_shutdown()
        # enable_network_24ghz
        # self.cs.config_no_ap_dot11_24ghz_shutdown()
        # enable
        self.cs.config_ap_no_dot11_6ghz_shutdown()
        # config_ap_no_dot11_24ghz_shutdown
        # advanced
        self.cs.show_ap_dot11_6gz_summary()
        # self.cs.show_ap_dot11_24gz_summary()
        # show_wlan_summary
        self.cs.show_wlan_summary()

    # Used before testbed change

    def test_config_tx_power_wpa2_IDIC(self):

        logger.info("sample_test_tx_power_sequence")

        # no_logging_console
        self.cs.no_logging_console()
        # line_console_0
        self.cs.line_console_0()
        # summary
        self.cs.show_ap_summary()

        # disable
        self.cs.show_ap_dot11_5gz_shutdown()
        self.cs.show_ap_dot11_24gz_shutdown()
        # This needs to be here to disable and delete
        self.cs.wlan = 'wpa2_wlan_3_CF9C'

        # disable_wlan
        self.cs.wlan_shutdown()
        # disable_network_5ghz
        self.cs.ap_dot11_5ghz_shutdown()
        # disable_network_24ghz
        self.cs.ap_dot11_24ghz_shutdown()
        # manual
        self.cs.ap_dot11_5ghz_radio_role_manual_client_serving()
        # self.cs.ap_dot11_24ghz_radio_role_manual_client_serving()
        self.cs.tx_power = '1'

        # Configuration for 5g

        # txPower
        self.cs.config_dot11_5ghz_tx_power()
        self.cs.bandwidth = '20'
        # bandwidth (to set to 20 if channel change does not support)
        self.cs.config_dot11_5ghz_channel_width()
        self.cs.channel = '100'
        # channel
        self.cs.config_dot11_5ghz_channel()
        self.cs.bandwidth = '40'
        # bandwidth
        self.cs.config_dot11_5ghz_channel_width()
        # show_wlan_summary
        self.cs.show_wlan_summary()

        # delete_wlan
        # TODO (there were two in tx_power the logs)
        # need to check if wlan present
        self.cs.wlan = 'wpa2_wlan_3'

        # delete wlan
        self.cs.config_no_wlan()

        # create_wlan_wpa2
        self.cs.wlan = 'wpa2_wlan_3_CF9C'
        self.cs.wlanID = '3'
        self.cs.wlanSSID = 'wpa2_wlan_3_CF9C'
        self.cs.security_key = 'hello123'
        self.cs.config_wlan_wpa2()

        # wireless_tag_policy
        self.cs.tag_policy = 'RM204-TB1'
        self.cs.policy_profile = 'default-policy-profile'
        self.cs.config_wireless_tag_policy_and_policy_profile()
        # enable_wlan
        self.cs.config_enable_wlan_send_no_shutdown()
        # enable_network_5ghz
        self.cs.config_no_ap_dot11_5ghz_shutdown()
        # enable_network_24ghz
        # self.cs.config_no_ap_dot11_24ghz_shutdown()
        # enable
        self.cs.config_ap_no_dot11_5ghz_shutdown()
        # config_ap_no_dot11_24ghz_shutdown
        # advanced
        self.cs.show_ap_dot11_5gz_summary()
        # self.cs.show_ap_dot11_24gz_summary()
        # show_wlan_summary
        self.cs.show_wlan_summary()

        summary = self.cs.show_ap_wlan_summary()
        logger.info(summary)


# unit test for controller wrapper
def main():
    # arguments
    parser = argparse.ArgumentParser(
        prog='cc_module_test.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            cc_module_test.py: wrapper for interface to a series of controllers
            ''',
        description='''\
NAME: cc_module_test.py

PURPOSE:
to test the dynamic import of a controller module

SETUP:
None

EXAMPLE:
    There is a unit test included to try sample command scenarios


COPYWRITE
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

INCLUDE_IN_README
---------
            ''')

# ./cc_module_test.py --scheme ssh --dest localhost --port 8887 --user admin --passwd Cisco123 --ap APA453.0E7B.CF9C --series 9800 --prompt "WLC1" --timeout 10 --band '5g' --module "cc_module_9800_3504"

    # These commands are just needed to interact it can be done in class methods.abs(
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
    parser.add_argument("--module", type=str, help="series module", required=True)

    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    logger_config.set_level('debug')

    # dynamic import of the controller module
    # 'cc_module_9800_3504'
    series = importlib.import_module(args.module)

    # create the controller
    cc = series.create_controller_series_object(
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

    # cc.show_ap_config_slots()

    mt = create_module_test_object(cs=cc)

    # mt.sample_test_dump_status()

    # mt.test_config_tx_power_6g_wpa3()

    # mt.test_config_tx_power_5g_wpa2_AP3()

    # mt.test_config_tx_power_6g_wpa3_AP4()

    mt.test_config_tx_power_dual_band_6g_wpa3()

    # mt.test_config_tx_power_6g_wpa3_attempt2()

    # cc.show_ap_summary()
    # cc.no_logging_console()
    # cc.line_console_0()
    # cc.show_wlan_summary()
    # cc.show_ap_dot11_5gz_summary()


if __name__ == "__main__":
    main()
