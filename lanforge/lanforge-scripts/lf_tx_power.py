#!/usr/bin/python3
'''
NAME: lf_tx_power

CLASSIFICATION: lanforge test

PURPOSE:
Perform tx power testing

SETUP:
You might need to install perl
Fedora : dnf install perl-Net-Telnet
Ubunto : sudo apt install libnet-telnet-perl

NOTE: To convert the per spatial stream dBm to combined dBm
convert dBm to watts (power) for each spatial stream,  add the power values then convert back to dBm
https://www.rapidtables.com/convert/power/dBm_to_Watt.html
https://www.rapidtables.com/convert/power/Watt_to_dBm.html

Discussion
https://www.thepacketologist.com/2021/10/power-conversion-in-python/

EXAMPLE:
TODO : add sample command

RESULTS:  csv xlsx

COPYRIGHT:
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

INCLUDE_IN_README
'''


import math
import xlsxwriter
import subprocess
import argparse
from time import sleep
import time
import logging
import re
import sys
import datetime
import importlib
import os
import traceback
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../")))

# TODO change the name from logg to logger
# to match consistency with other files.
logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")
lf_report = importlib.import_module("py-scripts.lf_report")
lf_kpi_csv = importlib.import_module("py-scripts.lf_kpi_csv")


EPILOG = '''\

#############################################################################################
# RSSI adjust

be root
sudo -s

manually disable it run-time by echo-ing a zero to the debugfs file, like:
echo 0 > /debug/ieee80211/wiphy0/ath10k/ofdm_peak_power_rssi

manually enable
echo 1 > /debug/ieee80211/wiphy0/ath10k/ofdm_peak_power_rssi

/* QCA seems to report a max-power average over the bandwidth, where mtk and intel radios
 * report a ofdm peak power.  The ofdm peak power corresponds more closely to tx-power minus
 * pathloss, so I think that is preferred output.  After some extensive measurements in
 * a fully cabled environment, it looks like these adjustments are appropriate to make
 * QCA be similar to MTK7915 and ax210:
 * 2.4Ghz:
 *  1x1 +8            (+13 to match txpower - pathloss.  Less confident on anything above 1x1 for this column)
 *  2x2 +4             +11
 *  3x3 +3             +10
 *  4x4 +3             +10
 * 5Ghz
 *  1x1 +12            +18
 *  2x2 +12            +18
 *  3x3 +10            +18
 *  4x4 +10            +18
 */

/* OFDM RSSI adjustments, for nss 1-4 */
const int adjust_24[4] = {8, 4, 3, 3};
const int adjust_5[4] = {12, 12, 10, 10};
const int adjust_zero[4] = {0, 0, 0, 0};

note the second collumn, that is what we calculate from actual received peak OFDM power,
but I was not sure we'd want to go that far, so intead I tried to make it match ax210 and mtk7915

##############################################################################################
# Support History
##############################################################################################
2/25/2022 - adding 6E support
formula:
5GHz channel = (freq_mhz - 5180) / 5 + 36
6GHz channel = (freq_mhz - 5955) / 5 + 1

6E has the concept of slot
WLC1#ap name APCCC9C.3EF4.DDE0 dot11 6ghz ?
  cleanair  Enable 802.11 6Ghz cleanair management
  slot      Set slot number

WLC1#ap name APCCC9C.3EF4.DDE0 dot11 6ghz slot ?
  <2-3>  Enter Slot Id

WLC1#ap name APCCC9C.3EF4.DDE0 dot11 6ghz slot 3 ?
  antenna   Configures the 802.11 6Ghz antenna
  channel   Configure advanced 802.11 6Ghz channel assignment parameters for Cisco AP
  dot11ax   Configure 802.11ax-6GHz parameters
  radio     Configures the 802.11 6Ghz radio
  rrm       Radio resource management
  shutdown  Disable 802.11 Ghz radio on Cisco AP
  txpower   Configures the 802.11 6Ghz Tx Power Level


# 6G example : use existing station
./lf_ts_power.py
[controller configuration ]
--scheme ssh
--dest localhost
--port 8887
--user admin
--passwd Cisco123
--prompt WLC1
--series 9800
--band 6g
--module cc_module_9800_3504
--timeout 3

[AP Configuration]
--ap AP687D.B45C.25EC
--ap_band_slot_6g 3

[wlan configuration]
--wlan 6G-wpa3-AP3
--wlan_id 15
--wlan_ssid 6G-wpa3-AP3
--tag_policy RM204-TB1-AP4
--policy_profile default-policy-profile

[tx power configuration]
--pathloss 59
--antenna_gain 6

[traffic generation configuration (LANforge)]
--lfmgr 192.168.100.139
--upstream_port eth2
--lfresource 1
--radio wiphy0
--station wlan0
--ssid 6G-wpa3-AP3
--ssidpw hello123
--security wpa3
--bssid DEFAULT or aa:bb:cc:00:11:22
--no_cleanup_station

[test configuration]
--channel 1
--bandwidth 160
--vht160
--nss 2
--txpower 3
--duration 25
--outfile tx_power_AP4_AX210_2x2_6E
--no_cleanup
--test_rig Cisco-WLC1-AP4

# Command on one line

./lf_tx_power.py --scheme ssh --dest localhost --port 8887 --user admin --passwd Cisco123 --prompt 'WLC1' --series 9800 --band 6g --module cc_module_9800_3504 --timeout 3 --ap AP687D.B45C.25EC  --ap_band_slot_6g 3 --wlan '6G-wpa3-AP3' --wlan_id 15 --wlan_ssid '6G-wpa3-AP3' --tag_policy 'RM204-TB1-AP4' --policy_profile 'default-policy-profile' --pathloss 69 --antenna_gain 6 --lfmgr '192.168.100.139' --upstream_port eth2 --lfresource 1 --radio wiphy0 --station 'wlan0' --ssid '6G-wpa3-AP3' --ssidpw 'hello123' --security wpa3 --no_cleanup_station --channel 1 --bandwidth 160 --vht160 --nss 2 --txpower 3 --duration 25 --outfile 'tx_power_AP4_AX210_2x2_6E' --no_cleanup  2>&1 |tee tx_output_AP4_AX210_2x2_6E.txt

# Verified 3/1/2022
./lf_tx_power.py -d localhost -u admin -p Cisco123 --port 8887 --scheme ssh --ap AP687D.B45C.25EC  --bandwidth "160" --vht160  --channel "1" --nss 2 --txpower "2" --pathloss 59 --antenna_gain 6 --band 6g --upstream_port eth2 --series 9800 --radio wiphy0 --ap_band_slot_6g 3 --ssid 6G-wpa3-AP3 --prompt "WLC1"  --station 'wlan0' --lfmgr '192.168.100.139' --ssidpw hello123 --security wpa3   --wlan 6G-wpa3-AP3 --wlanID 15 --wlanSSID 6G-wpa3-AP3 --lfresource 1  --tag_policy "RM204-TB1-AP4" --policy_profile "default-policy-profile" --testbed_id 'Cisco-WLC1-AP4' --module 'cc_module_9800_3504' --no_cleanup --outfile 'tx_power_AP4_AX210_2x2_6E' --duration 25  2>&1 |tee tx_output_AP4_AX210_2x2_6E.txt

##############################################################################################
##############################################################################################

make sure pexpect is installed:
$ sudo yum install python3-pexpect
$ sudo yum install python3-xlsxwriter

You might need to install pexpect-serial using pip:
$ pip3 install pexpect-serial
$ pip3 install XlsxWriter

You might need to install perl
Fedora : dnf install perl-Net-Telnet
Ubunto : sudo apt install libnet-telnet-perl

This script will automatically create and start a layer-3 UDP connection between the
configured upstream port and station.

The user also has the option of setting up the station oustide of this script, however.

# Examples:
# See cisco_power_results.txt when complete.
# See cisco_power_results.xlsx when complete.
NOTE:  Telnet port 23 unless specified ,  ssh  port 22 unless specified,  scheme defaults to ssh


# TODO update , OLD EXAMPLE - Connecting to AP
##############################################################################################
# read AP for powercfg values using : show controllers dot11Radio 1 powercfg | g T1'
##############################################################################################
./lf_tx_power.py -d 172.19.27.55 -u admin -p Wnbulab@123 --port 2013 --scheme telnet \
    --ap 9120_Candela --bandwidth "20" --channel "149" --nss 4 --txpower "1" \
    --pathloss 56 --band a --upstream_port eth2 --series 9800 --radio wiphy5 --slot 1 --ssid open-wlan \
    --prompt "katar_candela" --create_station --station sta0001 --ssidpw [BLANK] --security open  \
    --antenna_gain "6" --wlanID 1 --wlan open-wlan --wlanSSID open-wlan\
    --ap_info "ap_scheme==telnet ap_prompt==9120_Candela ap_ip==172.19.27.55 ap_port==2008 ap_user==admin ap_pw==Wnbulab@123"

# TODO update OLD EXAMPLE replaced by BATCH mode
##############################################################################################
# Long duration test -- need to create the ---wlanID 1 --wlan open-wlan --wlanSSID open-wlan
##############################################################################################

./lf_tx_power.py -d 172.19.36.168 -u admin -p Wnbulab@123 --port 23 --scheme telnet --ap "APA453.0E7B.CF60" \
    --bandwidth "20 40 80" --channel "36 40 44 48 52 56 60 64 100 104 108 112 116 120 124 128 132 136 140 144 149 153 157 161 165" \
    --nss 4 --txpower "1 2 3 4 5 6 7 8" --pathloss 54 --antenna_gain 6 --band a --upstream_port eth2 --series 9800  \
    --wlanID 1 --wlan open-wlan --wlanSSID open-wlan --create_station --station sta0001 --radio wiphy1 --ssid  open-wlan --ssidpw [BLANK] --security open \
    --outfile cisco_power_results_60_chan_ALL  --cleanup --slot 1


##############################################################################################
# Per-channel path-loss example station present
##############################################################################################

./lf_tx_power.py -d 192.168.100.112 -u admin -p Cisco123 -s ssh --port 22 -a VC --lfmgr 192.168.100.178 \
  --station sta00000 --bandwidth "20 40 80 160" --channel "36:64 149:60" --antenna_gain 5 --nss 4 --txpower "1 2 3 4 5 6 7 8" --pathloss 64 \
  --band a --upstream_port eth2 --lfresource2 2

##############################################################################################
# To create a station run test against station create open-wlan
##############################################################################################

./lf_tx_power.py -d <router IP> -u admin -p Cisco123 -port 23 --scheme telnet --ap AP6C71.0DE6.45D0 \
--station sta2222 --bandwidth "20" --channel "36" --nss 4 --txpower "1 2 3 4 5 6 7 8" --pathloss 54 --antenna_gain 6 --band a \
--upstream_port eth2 --series 9800 --wlanID 1 --wlan open-wlan --wlanSSID open-wlan --create_station --station sta2222 --radio wiphy1 --ssid open-wlan \
--ssidpw [BLANK] --security open

##############################################################################################
# station already present
##############################################################################################

./lf_tx_power.py -d <router IP> -u admin -p Cisco123 -port 23 --scheme telnet --ap AP6C71.0DE6.45D0 \
--station sta0000 --bandwidth "20" --channel "36" --nss 4 --txpower "1 2 3 4 5 6 7 8" --pathloss 64 --antenna_gain 5 --band a \
--upstream_port eth2 --series 9800 --wlanID 1 --wlan open-wlan --wlanSSID open-wlan


##############################################################################################
# to create a station
##############################################################################################

./lf_associate_ap.pl --mgr 192.168.100.178 --radio wiphy2 --ssid 6G-wpa3-AP3 --passphrase hello123 ssecurity wpa3 --bssid DEFAULT --upstream 1.1.eth2 --first_ip DHCP --first_sta sta0000 --duration 25 --cxtype udp --bps_min 1000000000--ieee80211w 2 --wifi_mode abgnAX --action add

Changing regulatory domain should happen outside of this script.


##############################################################################################
# OUTPUT in XLSX file - Spread sheet how values determined
##############################################################################################

Tx Power                             : Input from command line (1-8)
Allowed Per Path                     : Read from the Controller
Cabling Pathloss                     : Input from command line, best if verified prior to testing
Antenna Gain                         : Input from command line, if AP cannot detect antenna connection
Beacon RSSI (beacon_sig)             : From Lanforge probe, command ./lf_portmod.pl with cli parameter probe_port 1 (~line 1183, ~line 1209)
Combined RSSI User (sig)             : From Lanforge probe, command ./lf_portmod.pl with cli parameter probe_port 1 (~line 1183, ~line 1193)
RSSI 1, RSSI 2, RSSI 3, RSSI 4       : (~line 1160)
    ants[q] (antX) read from Lanforge probe, command ./lf_portmod.pl with cli parameter probe_port 1

Ant 1, Ant 2, Ant 3, Ant 4 : ()
    Starting Value for antX read from lanforge probe, using command ./lf_portmod.pl with cli parameter porbe_port 1

    _noise_bear (_noise_i) = from Lanforge returning NOISE from command (!line 1070) lf_portmod.pl reading --show_port
    "AP, IP, Mode, NSS, Bandwith, Channel, Signal, NOISE, Status, RX-Rate

    rssi_adj (only used if --adjust_nf and _noise_bare != None) (~line 1263)  _noise_i(_noise_bear) - nf_at_calibration (fixed value of -105)

    Thus calc_antX =  int(antX read from Lanforge) + pi (path loss from command line) + rssi_adj + ag (antenna gain from command line)

    calc_antX is put on the spread sheet under Ant X

Offset 1, Offset 2, Offset 3, Offset 4: which in the code is diff_aX = calc_antX - allowed_per_path (adjusted based on number of streams)

Pass/Fail : (~line 1286) If the diff / offset is greater than the pfrange determins the pass or fail

Show the tx_power for a specific station:
 iw dev <station> station dump
 iw dev sta0000 station dump

#####################################################################
5g dual band restrictions
#####################################################################

when both 5g (slot 1) is enabled and dual-band 5g (slot 2) is enabled .
5g slot 1 will used the 5g channels to 64,  the 5g dual-band will use channels 100 -> 165.
When 5g (slot 1) and dual-band 6g (slot 2) is enabled then 5g (slot 1) has all ba

Path lost
24g 5g : 50dB inline attenuation + cables and splitters, so I think last time we estimated the path loss should be about 56dB
that is to the 5ghz radio

6g : wiphy2 has only 30dB inline attenuation to the 6ghz radio on the 9136

'''

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()


NL = "\n"
CR = "\r\n"
Q = '"'
A = "'"
FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'

lfmgr = "127.0.0.1"
lfstation = "sta00000"
lfresource = "1"
lfresource2 = "1"
outfile = "cisco_power_results.txt"
full_outfile = "cisco_power_results_full.txt"
outfile_xlsx = "cisco_power_results.xlsx"
upstream_port = "eth1"
pf_dbm = 3

# kpi notes
# Maybe subtest pass/failed is interesting,
# and for KPI, could do min/max/avg of the beacon power offset
# from expected, and same for data power offset from expected?

# Channel notes
# setting channel' typically means setting the bandwidth range,
# and also setting the control channel.
# So, running on ctrl channel 36 at HT40 and ch 40 at HT40 uses same total bandwdith range,
# but in second case, the beacons and control frames should be on ch 40.
# At least that is normally how things are implemented.

# Allow one chain to have a lower signal, since customer's DUT has
# lower tx-power on one chain when doing high MCS at 4x4.
pf_ignore_offset = 0

# Threshold for allowing a pass
failed_low_threshold = 0

# This below is only used when --adjust_nf is used.
# Noise floor on ch 36 where we calibrated -54 path loss (based on hard-coded -95 noise-floor in driver)
nf_at_calibration = -105
# older ath10k driver hard-codes noise-floor to -95 when calculating RSSI
# RSSI = NF + reported_power
# Shift RSSI by difference in actual vs calibrated noise-floor since driver hard-codes
# the noise floor.

# rssi_adjust = (current_nf - nf_at_calibration)


def usage():
    print("Incorrect inputs:  ./lf_tx_power.py --help to show usage ")
#
# see https://stackoverflow.com/a/13306095/11014343

# TODO use common logger library


class FileAdapter(object):
    def __init__(self, logger):
        self.logger = logger

    def write(self, data):
        # NOTE: data can be a partial line, multiple lines
        data = data.strip()  # ignore leading/trailing whitespace
        if data:  # non-blank
            self.logger.debug(data)

    def flush(self):
        pass  # leave it to logging to flush properly


def close_workbook(workbook):
    workbook.close()
    sleep(0.5)


def main():
    global lfmgr
    global lfstation
    global lfresource
    global lfresource2
    global outfile
    global outfile_xlsx
    global full_outfile
    global upstream_port
    global pf_dbm
    global pf_ignore_offset
    global failed_low_threshold

    parser = argparse.ArgumentParser(description="Cisco TX Power report Script", epilog=EPILOG,
                                     formatter_class=argparse.RawTextHelpFormatter)

    # controller configuration
    parser.add_argument("-s", "--scheme", type=str, choices=["serial", "ssh", "telnet"], help="[controller configuration] Connect via serial, ssh or telnet --scheme ssh", required=True)
    parser.add_argument("-d", "--controller_ip", "--dest", dest="dest", type=str, help="[controller configuration] address of the controller --dest localhost", required=True)
    parser.add_argument("-o", "--port", type=str, help="[controller configuration] controller port on the controller --port 8887", required=True)
    parser.add_argument("-u", "--user", type=str, help="[controller configuration] controller login/username --user admin", required=True)
    parser.add_argument("-p", "--passwd", type=str, help="[controller configuration] credential password --passwd Cisco123", required=True)
    parser.add_argument('-ccp', '--prompt', type=str, help="[controller configuration] controller prompt --prompt WLC1", required=True)
    parser.add_argument("--series", type=str, help="[controller configuration] controller series --series 9800", required=True)
    parser.add_argument("--band", type=str, help="band testing --band 6g", choices=["5g", "24g", "6g", "dual_band_5g", "dual_band_6g"])
    parser.add_argument("--module", type=str, help="[controller configuration] series module (cc_module_9800_3504.py)  --module cc_module_9800_3504 ", required=True)
    parser.add_argument("--timeout", type=str, help="[controller configuration] controller command timeout --timeout 3 ", default=3)

    # AP configuration
    parser.add_argument("-a", "--ap", type=str, help="[AP configuration] select AP  ", required=True)
    parser.add_argument("--ap_dual_band_slot_6g", type=str, help="[AP configuration] --ap_dual_band_slot_6g 2 , 9800 AP dual-band slot , for 6g dual-band use show ap dot11 dual-band summary", default='2')
    parser.add_argument("--ap_dual_band_slot_5g", type=str, help="[AP configuration] --ap_dual_band_slot_5g 2 , 9800 AP dual-band slot , for 5g dual-band use show ap dot11 dual-band summary", default='2')
    parser.add_argument("--ap_band_slot_6g", type=str, help="[AP configuration] --ap_band_slot_6g 2 , 9800 AP band slot , use show ap dot11 6ghz summary", default='2')
    parser.add_argument("--ap_band_slot_5g", type=str, help="[AP configuration] --ap_band_slot_5g 1 , 9800 AP band slot , use show ap dot11 5ghz summary", default='1')
    parser.add_argument("--ap_band_slot_24g", type=str, help="[AP configuration] --ap_band_slot_24g 0 , 9800 AP band slot , use show ap dot11 24ghz summary", default='0')

    # wlan configuration
    parser.add_argument("--create_wlan", help="[wlan configuration] --create_wlan", action='store_true')
    parser.add_argument("--wlan", type=str, help="[wlan configuration] controller wlan name --wlan 6G-wpa3-AP3 ", required=True)
    parser.add_argument("--wlan_id", "--wlanID", dest="wlanID", type=str, help="[wlan configuration] controller wlan id  --wlan_id 15", required=True)
    parser.add_argument("--wlan_ssid", "--wlanSSID", dest="wlanSSID", type=str, help="[wlan configuration] controller wlan ssid --wlan_ssid 6G-wpa3-AP3, wlan ssid must match station ssid", required=True)
    parser.add_argument("--tag_policy", type=str, help="[wlan configuration] controller tag policy --tag_policy RM204-TB1-AP4")
    parser.add_argument("--policy_profile", type=str, help="[wlan configuration] --policy_profile default-policy-profile")

    # ap interface configuration
    parser.add_argument('-api', '--ap_info', action='append', nargs=1, type=str, help="[ap configuration] --ap_info ap_scheme==<telnet,ssh or serial> ap_prompt==<ap_prompt> ap_ip==<ap ip> ap_port==<ap port number> ap_user==<ap user> ap_pw==<ap password>")

    # if args.ap_admin_down_up_6g:  - work around for 6G
    parser.add_argument("--ap_admin_down_up_6g", help="[ap admin down up] --6g_ap_admin_down_up  will admin down and up the AP", action='store_true')

    # tx power pathloss configuration
    parser.add_argument("--pathloss", type=str, help="[tx power configuration] Calculated pathloss between LANforge Station and AP --pathloss 59", required=True)
    parser.add_argument("--antenna_gain", type=str, help="[tx power configuration] Antenna gain,  take into account the gain due to the antenna --antenna_gain 6", required=True)
    parser.add_argument("--pf_ignore_offset", type=str, help="[tx power configuration] Allow a chain to have lower tx-power and still pass. default 0 so disabled", default="0")
    parser.add_argument("--adjust_nf", action='store_true', help="[tx power configuration] Adjust RSSI based on noise-floor.  ath10k without the use-real-noise-floor fix needs this option")
    parser.add_argument('--beacon_dbm_diff', type=str, help="[tx power configuration] --beacon_dbm_diff <value>  is the delta that is allowed between the controller tx and the beacon measured", default="7")

    # pass / fail criteria
    parser.add_argument("--pf_dbm", type=str, help="[tx power pass / fail criteria] Pass/Fail threshold per Spetial Stream.  Default is 3", default="3")

    # traffic generation configuration (LANforge)
    parser.add_argument("--lfmgr", type=str, help="[traffic generation configuration (LANforge)] LANforge Manager IP address --lfmgr 192.168.100.178", required=True)
    parser.add_argument("--upstream_port", type=str, help="[traffic generation configuration (LANforge)] LANforge upsteram-port to use (eth1, etc)  --upstream_port eth2", required=True)
    parser.add_argument("--lfresource", type=str, help="[traffic generation configuration (LANforge)] LANforge resource ID for the station --lfresource 1")
    parser.add_argument("--lfresource2", type=str, help="[traffic generation configuration (LANforge)] LANforge resource ID for the upstream port system ")

    # LANforge station configuration
    parser.add_argument("--radio", type=str, help="[LANforge station configuration] LANforge radio station created on --radio wiphy0")
    parser.add_argument("--create_station", help="[LANforge station configuration] create LANforge station at the beginning of the test", action='store_true')
    parser.add_argument("--station", type=str, help="[LANforge station configuration] Use already created LANforge station, use --no_cleanup also --station wlan0", required=True)
    parser.add_argument("--ssid", type=str, help="[station configuration] station ssid, ssid of station must match the wlan created --ssid 6G-wpa3-AP3", required=True)
    parser.add_argument("--ssidpw", "--security_key", dest='ssidpw', type=str, help="[station configuration]  station security key --ssidpw hello123", required=True)
    parser.add_argument("--bssid", "--ap_bssid", dest='bssid', type=str, help="[station configuration]  station AP bssid ", required=True)
    parser.add_argument("--security", type=str, help="[station configuration] security type open wpa wpa2 wpa3", required=True)
    parser.add_argument("--wifi_mode", type=str, help="[station configuration] --wifi_mode auto  types auto|a|abg|abgn|abgnAC|abgnAX|an|anAC|anAX|b|bg|bgn|bgnAC|bgnAX|g ", default='auto')
    parser.add_argument("--vht160", action='store_true', help="[station configuration] --vht160 , Enable VHT160 in lanforge ")
    parser.add_argument("--ieee80211w", type=str, help="[station configuration] --ieee80211w 0 (Disabled) 1 (Optional) 2 (Required) (Required needs to be set to Required for 6g and wpa3 default Optional ", default='1')
    parser.add_argument("--wave2", help="[station configuration] --wave2 , wave2 (9984) has restrictions : 160Mhz is 2x2", action='store_true')
    parser.add_argument("--no_cleanup_station", action='store_true', help="[station configuration] --no_cleanup_station , do not clean up station after test completes ")

    # test configuration
    parser.add_argument("-c", "--channel", type=str, help="[test configuration] --channel '1 33' List of channels to test, with optional path-loss, 36:64 149:60. NA means no change")
    parser.add_argument("-b", "--bandwidth", type=str, help="[test configuration] --bandwidth '20 40 80 160' List of bandwidths to test. NA means no change")
    parser.add_argument("-n", "--nss", type=str, help="[test configuration] --nss '2' List of spatial streams to test.  NA means no change")

    parser.add_argument("--tx_pw_cmp_to_prev", help='''
    [test configuration] --tx_pw_cmp_to_prev  validated that there was 3 dBm difference for each power step between runs
                            tx pwr 1 (20 dBm) to tx_pwr 2 (17 dBm) the pwr difference is 3 dBm
                            tx_power of 1 has no comparison", action='store_true'
                            ''')

    parser.add_argument("--nss_4x4_override", help="[test configuration] --nss_4x4_override  controller nss is 4 client nss is 2, set expected power to 1/4", action='store_true')
    parser.add_argument("--nss_4x4_ap_adjust", help="[test configuration] --nss_4x4_ap_adjust read ap to know number of spatial stream to take into account", action='store_true')
    parser.add_argument("--set_nss", help="[test configuration] --set_nss  configure controller to spatial streams to test", action='store_true')
    parser.add_argument("-T", "--txpower", type=str, help="[test configuration] List of txpowers to test.  NA means no change")
    parser.add_argument('-D', '--duration', type=str, help='[test configuration] --traffic <how long to run in seconds>  example -D 30 (seconds) default: 30 ', default='30')
    parser.add_argument('--wait_time', type=str, help='[test configuration] --wait_time <how long to wait for station to connect seconds>  example --wait_time 180 (seconds) default: 180 ', default='180')
    parser.add_argument("--outfile", help="[test configuration] Output file for csv data --outfile 'tx_power_AX210_2x2_6E")
    parser.add_argument("-k", "--keep_state", "--no_cleanup", dest="keep_state", action="store_true", help="[test configuration] --no_cleanup, keep the state, no configuration change at the end of the test")
    # TODO may want to remove enable_all_bands , all bands need to be enabled for 6E testing for 6E to know the domain
    parser.add_argument("-enb", "--enable_all_bands", dest="enable_all_bands", action="store_true", help="[test configuration] --enable_all_bands, enable 6g, 5g, 24b bands at end of test")
    parser.add_argument('--tx_power_adjust_6E', action="store_true", help="[test configuration] --power_adjust_6E  stores true, 6E: 20 Mhz pw 1-6, 40 Mhz pw 1-7 ")
    # parser.add_argument('--per_ss', action="store_true", help="[test configuration] --per_ss  stores true, per spatial stream used in pass fail criteria")

    # test configuration
    parser.add_argument("--testbed_id", "--test_rig", dest='test_rig', type=str, help="[testbed configuration] --test_rig", default="")
    parser.add_argument("--testbed_location", dest='testbed_location', type=str, help="[testbed configuration] --testbed_location <from show ap summary Location>", default="default location")

    # kpi_csv arguments:
    parser.add_argument("--test_tag", default="", help="[kpi configuration] test tag for kpi.csv,  test specific information to differenciate the test")
    parser.add_argument("--dut_hw_version", default="", help="[kpi configuration] dut hw version for kpi.csv, hardware version of the device under test")
    parser.add_argument("--dut_sw_version", default="", help="[kpi configuration] dut sw version for kpi.csv, software version of the device under test")
    parser.add_argument("--dut_model_num", default="", help="[kpi configuration] dut model for kpi.csv,  model number / name of the device under test")
    parser.add_argument("--dut_serial_num", default="", help="[kpi configuration] dut serial for kpi.csv, serial number / serial number of the device under test")
    parser.add_argument("--test_priority", default="", help="[kpi configuration] dut model for kpi.csv,  test-priority is arbitrary number")
    parser.add_argument("--test_id", default="TX power", help="[kpi configuration] test-id for kpi.csv,  script or test name")

    parser.add_argument("--html_report", help="[html configuration] --html_report store True , will create html and pdf reports", action='store_true')

    parser.add_argument('--local_lf_report_dir', help='--local_lf_report_dir override the report path, primary use when running test in test suite', default="")

    # TODO ADD KP configuration

    # debug configuration
    parser.add_argument("--wait_forever", action='store_true', help="[debug configuration] Wait forever for station to associate, may aid debugging if STA cannot associate properly")
    parser.add_argument('--show_lf_portmod', action='store_true', help="[debug configuration] --show_lf_portmod,  show the output of lf_portmod after traffic to verify RSSI values measured by lanforge")
    parser.add_argument("--exit_on_fail", action='store_true', help="[debug configuration] --exit_on_fail,  exit on test failure")
    parser.add_argument("--exit_on_error", action='store_true', help="[debug configuration] --exit_on_error, exit on test error, test mechanics failed")

    # logg information
    parser.add_argument("--lf_logger_config_json", help="[log configuration] --lf_logger_config_json <json file> , json configuration of logger")
    parser.add_argument("--log_level", help="[log configuration] --log_level  debug info warning error critical")

    # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "{:.3f}".format(time.time() - (math.floor(time.time())))[1:]
    # print(current_time)
    # usage()
    args = None

    # Parcing the input parameters and assignment
    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    if args.log_level:
        logger_config.set_level(level=args.log_level)

    if args.lf_logger_config_json:
        # logger_config.lf_logger_config_json = "lf_logger_config.json"
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()

    # TODO refactor to be logger for consistency
    logg = logging.getLogger(__name__)
    # logg.setLevel(logging.DEBUG)

    # for kpi.csv generation

    local_lf_report_dir = args.local_lf_report_dir
    test_rig = args.test_rig
    test_tag = args.test_tag
    dut_hw_version = args.dut_hw_version
    dut_sw_version = args.dut_sw_version
    dut_model_num = args.dut_model_num
    dut_serial_num = args.dut_serial_num
    # test_priority = args.test_priority  # this may need to be set per test
    test_id = args.test_id

    lfstation = args.station
    upstream_port = args.upstream_port
    lfmgr = args.lfmgr
    # TODO
    if (args.lfresource is not None):
        lfresource = args.lfresource
    if (args.lfresource2 is not None):
        lfresource2 = args.lfresource2

    if (args.pf_dbm is not None):
        pf_dbm = int(args.pf_dbm)
    if (args.pf_ignore_offset is not None):
        pf_ignore_offset = int(args.pf_ignore_offset)
    if (args.wlanSSID != args.ssid):
        print("####### ERROR ################################")
        print("wlanSSID: {} must equal the station ssid: {}".format(args.wlanSSID, args.ssid))
        print("####### ERROR ################################")
        exit(1)
    if (args.create_wlan):
        if(args.tag_policy is None or args.policy_profile is None):
            print("####### ERROR ######################################################")
            print(" For create_wlan both tag_policy and policy_profile must be entered")
            print("####### ERROR #######################################################")
            exit(1)

    ap_dict = []
    if args.ap_info:
        ap_info = args.ap_info
        for _ap_info in ap_info:
            print("ap_info {}".format(_ap_info))
            ap_keys = ['ap_scheme', 'ap_prompt', 'ap_ip', 'ap_port', 'ap_user', 'ap_pw']
            ap_dict = dict(map(lambda x: x.split('=='), str(_ap_info).replace('[', '').replace(']', '').replace("'", "").split()))
            for key in ap_keys:
                if key not in ap_dict:
                    print("missing ap config, for the {}, all these need to be set {} ".format(key, ap_keys))
                    exit(1)
            print("ap_dict: {}".format(ap_dict))

    # except Exception as e:
    #    logging.exception(e)
    #    usage()
    #    exit(2)

    # dynamic import of the controller module
    series = importlib.import_module(args.module)

    # create the controller , cs is controller scheme
    cs = series.create_controller_series_object(
        scheme=args.scheme,
        dest=args.dest,
        user=args.user,
        passwd=args.passwd,
        prompt=args.prompt,
        series=args.series,
        ap=args.ap,
        ap_band_slot_6g=args.ap_band_slot_6g,
        port=args.port,
        band=args.band,
        timeout=args.timeout)
    cs.wlan = args.wlan
    cs.wlanID = args.wlanID
    cs.wlanSSID = args.wlanSSID
    # TODO change to use args.security_key
    cs.security_key = args.ssidpw
    cs.series = args.series

    # Need to get regulatory domain for title
    # Read the country code and regulatory domain
    #
    cs.console_setup()

    cs.read_country_code_and_regulatory_domain()

    myrd = cs.regulatory_domain
    mycc = cs.country_code

    # setup Logging and Paths

    # end setup logging and paths
    # put in test information in title name
    # this only works for single test passed in.
    if args.tx_power_adjust_6E and args.band == '6g':
        txpowers = args.txpower.split()
        if args.bandwidth == '20':
            if '8' in txpowers:
                txpowers.remove('8')
            if '7' in txpowers:
                txpowers.remove('7')
        elif args.bandwidth == '40':
            if '8' in txpowers:
                txpowers.remove('8')
        txpowers_str = '_'.join(txpowers)

        results_dir_name = ("tx_power"
                            + '_cc_' + mycc
                            + '_rd_' + myrd
                            + '_band_' + args.band
                            + '_ch_' + args.channel.replace(' ', '_')
                            + '_nss_' + args.nss.replace(' ', '_')
                            + '_bw_' + args.bandwidth.replace(' ', '_')
                            + '_txpw_' + txpowers_str)

    else:
        results_dir_name = ("tx_power"
                            + '_cc_' + mycc
                            + '_rd_' + myrd
                            + '_band_' + args.band
                            + '_ch_' + args.channel.replace(' ', '_')
                            + '_nss_' + args.nss.replace(' ', '_')
                            + '_bw_' + args.bandwidth.replace(' ', '_')
                            + '_txpw_' + args.txpower.replace(' ', '_'))

    if local_lf_report_dir != "":
        report = lf_report.lf_report(
            _path=local_lf_report_dir,
            _results_dir_name=results_dir_name,
            _output_html="{results_dir}.html".format(results_dir=results_dir_name),
            _output_pdf="{results_dir}.pdf".format(results_dir=results_dir_name))
    else:
        report = lf_report.lf_report(
            _results_dir_name=results_dir_name,
            _output_html="{results_dir}.html".format(results_dir=results_dir_name),
            _output_pdf="{results_dir}.pdf".format(results_dir=results_dir_name))

    kpi_path = report.get_report_path()
    # kpi_filename = "kpi.csv"
    logg.info("kpi_path :{kpi_path}".format(kpi_path=kpi_path))

    # create kpi_csv object and record the common data
    # TX power is not a class so access kpi directly in function
    kpi_csv = lf_kpi_csv.lf_kpi_csv(
        _kpi_path=kpi_path,
        _kpi_test_rig=test_rig,
        _kpi_test_tag=test_tag,
        _kpi_dut_hw_version=dut_hw_version,
        _kpi_dut_sw_version=dut_sw_version,
        _kpi_dut_model_num=dut_model_num,
        _kpi_dut_serial_num=dut_serial_num,
        _kpi_test_id=test_id)

    outfile_path = report.get_report_path()
    current_time = time.strftime("%m_%d_%Y_%H_%M_%S", time.localtime())
    if (args.outfile):
        test_name = ('Tx Power:' + args.outfile + ', AP: ' + args.ap + ', CC: ' + mycc + ', RD ' + myrd
                     + ', Band: ' + args.band + ', Channel: ' + args.channel
                     + ', NSS: ' + args.nss
                     + ', BW: ' + args.bandwidth
                     + ', Tx Power: ' + args.txpower)

        outfile_tmp = (outfile_path + '/' + current_time + '_' + args.outfile
                       + '_AP_' + args.ap
                       + '_CC_' + mycc
                       + '_RD_' + myrd
                       + '_band_' + args.band
                       + '_ch_' + args.channel.replace(' ', '_')
                       + '_nss_' + args.nss.replace(' ', '_')
                       + '_bw_' + args.bandwidth.replace(' ', '_')
                       + '_tx_pw_' + args.txpower.replace(' ', '_'))
    else:
        test_name = ('Tx Power:' + 'AP: ' + args.ap + ', CC: ' + mycc + ', RD ' + myrd
                     + ', Band: ' + args.band + ', Channel: ' + args.channel
                     + ', NSS: ' + args.nss
                     + ', BW: ' + args.bandwidth
                     + ', Tx Power: ' + args.txpower)

        outfile_tmp = (outfile_path + '/' + current_time + '_' + 'tx_power'
                       + '_AP_' + args.ap
                       + '_CC_' + mycc
                       + '_RD_' + myrd
                       + '_band_' + args.band
                       + '_ch_' + args.channel.replace(' ', '_')
                       + '_nss_' + args.nss.replace(' ', '_')
                       + '_bw_' + args.bandwidth.replace(' ', '_')
                       + '_tx_pw_' + args.txpower.replace(' ', '_'))
    print("outfile_tmp {outfile_tmp}".format(outfile_tmp=outfile_tmp))

    # note: there would always be an args.outfile due to the default
    full_outfile = "{}_full.txt".format(outfile_tmp)
    outfile_xlsx = "{}.xlsx".format(outfile_tmp)
    outfile = "{}.txt".format(outfile_tmp)
    print("output file: {}".format(outfile))
    print("output file full: {}".format(full_outfile))
    print("output file xlsx: {}".format(outfile_xlsx))

    if args.create_wlan:
        cs.tag_policy = args.tag_policy
        cs.policy_profile = args.policy_profile

    if bool(ap_dict):
        logg.info("ap_dict {}".format(ap_dict))

    if args.outfile is not None:
        logg.info("output file: {}".format(outfile))
        logg.info("output file full: {}".format(full_outfile))
        logg.info("output file xlsx: {}".format(outfile_xlsx))

    if (args.bandwidth is None):
        usage()
        logg.info("ERROR:  Must specify bandwidths")
        exit(1)

    if (args.channel is None):
        usage()
        logg.info("ERROR:  Must specify channels")
        exit(1)

    if (args.nss is None):
        usage()
        logg.info("ERROR:  Must specify NSS")
        exit(1)

    if (args.txpower is None):
        usage()
        logg.info("ERROR:  Must specify txpower")
        exit(1)

    if (args.pathloss is None):
        logg.info("ERROR:  Pathloss must be specified.")
        exit(1)

    if (args.antenna_gain is None):
        usage()
        logg.info("ERROR: Antenna gain must be specified.")
        exit(1)

    # Full spread-sheet data
    csv = open(full_outfile, "w")
    csv.write("Regulatory Domain\tCabling Pathloss\tAntenna Gain\tCfg-Channel\tCfg-NSS\tCfg-AP-BW\tTx Power\tBeacon-Signal\tCombined-Signal\tRSSI 1\tRSSI 2\tRSSI 3\tRSSI 4\tAP-BSSID\tRpt-BW\tRpt-Channel\tRpt-Mode\tRpt-NSS\tRpt-Noise\tRpt-Rxrate\tCtrl-AP-MAC\tCtrl-Channel\tCtrl-Power\tCtrl-dBm\tCalc-dBm-Combined\tDiff-dBm-Combined\tAnt-1\tAnt-2\tAnt-3\tAnt-4\tOffset-1\tOffset-2\tOffset-3\tOffset-4\tPASS/FAIL(+-%sdB)\tTimeStamp\tWarnings-and-Errors" % (pf_dbm))
    csv.write("\n")
    csv.flush()

    # Summary spread-sheet data
    csvs = open(outfile, "w")
    csvs.write("Regulatory Domain\tCabling Pathloss\tAntenna Gain\tAP Channel\tNSS\tAP BW\tTx Power\tAllowed Per-Path\tRSSI 1\tRSSI 2\tRSSI 3\tRSSI 4\tAnt-1\tAnt-2\tAnt-3\tAnt-4\tOffset-1\tOffset-2\tOffset-3\tOffset-4\tPASS/FAIL(+-%sdB)\tTimeStamp\tWarnings-and-Errors" % (pf_dbm))
    csvs.write("\n")
    csvs.flush()

    # XLSX file
    workbook = xlsxwriter.Workbook(outfile_xlsx)
    worksheet = workbook.add_worksheet()

    # bold = workbook.add_format({'bold': True, 'align': 'center'})
    dblue_bold = workbook.add_format({'bold': True, 'align': 'center'})
    dblue_bold.set_bg_color("#b8cbe4")
    # dblue_bold.set_bg_color("#00FFFF")
    dblue_bold.set_border(1)
    dtan_bold = workbook.add_format({'bold': True, 'align': 'center'})
    dtan_bold.set_bg_color("#dcd8c3")
    dtan_bold.set_border(1)
    dpeach_bold = workbook.add_format({'bold': True, 'align': 'center'})
    dpeach_bold.set_bg_color("#ffd8bb")
    dpeach_bold.set_border(1)
    dpink_bold = workbook.add_format({'bold': True, 'align': 'center'})
    dpink_bold.set_bg_color("#fcc8ca")
    dpink_bold.set_border(1)
    dyel_bold = workbook.add_format({'bold': True, 'align': 'center'})
    dyel_bold.set_bg_color("#ffe699")
    dyel_bold.set_border(1)
    dgreen_bold = workbook.add_format({'bold': True, 'align': 'center'})
    dgreen_bold.set_bg_color("#c6e0b4")
    dgreen_bold.set_border(1)
    dgreen_bold_left = workbook.add_format({'bold': True, 'align': 'left'})
    dgreen_bold_left.set_bg_color("#c6e0b4")
    dgreen_bold_left.set_border(1)
    # center = workbook.add_format({'align': 'center'})
    center_blue = workbook.add_format({'align': 'center'})
    center_blue.set_bg_color("#dbe5f1")
    center_blue.set_border(1)
    center_tan = workbook.add_format({'align': 'center'})
    center_tan.set_bg_color("#edede1")
    center_tan.set_border(1)
    center_peach = workbook.add_format({'align': 'center'})
    center_peach.set_bg_color("#fce4d6")
    center_peach.set_border(1)
    center_yel = workbook.add_format({'align': 'center'})
    center_yel.set_bg_color("#fdf2cc")
    center_yel.set_border(1)
    center_yel_red = workbook.add_format({'align': 'center', 'color': 'red'})
    center_yel_red.set_bg_color("#fdf2cc")
    center_yel_red.set_border(1)
    center_pink = workbook.add_format({'align': 'center'})
    center_pink.set_bg_color("ffd2d3")
    center_pink.set_border(1)
    center_red = workbook.add_format({'align': 'center'})
    center_red.set_bg_color("fc5555")
    center_red.set_border(1)
    red = workbook.add_format({'color': 'red', 'align': 'center'})
    red.set_bg_color("#e0efda")
    red.set_border(1)
    red_left = workbook.add_format({'color': 'red', 'align': 'left'})
    red_left.set_bg_color("#e0efda")
    red_left.set_border(1)
    green = workbook.add_format({'color': 'green', 'align': 'center'})
    green.set_bg_color("#e0efda")
    green.set_border(1)
    green_left = workbook.add_format({'color': 'green', 'align': 'left'})
    green_left.set_bg_color("#e0efda")
    green_left.set_border(1)
    orange_left = workbook.add_format({'color': 'orange', 'align': 'left'})
    orange_left.set_bg_color("#e0efda")
    orange_left.set_border(1)
    # Set up some formats to use.
    dark_green = workbook.add_format({'color': '#006400', 'bold': True})
    black = workbook.add_format({'color': 'black', 'bold': True})
    black_not_bold = workbook.add_format({'color': 'black', 'bold': False})
    # #e68b15
    title_format = workbook.add_format({
        'bold': 1,
        'border': 10,
        'align': 'left',
        'valign': 'vcenter',
        'fg_color': "#FFD700"})

    row = 0
    col = 0
    worksheet.set_row(0, 40)
    worksheet.set_column(0, 0, 10)
    # Create a format to use in the merged range.
    # https://xlsxwriter.readthedocs.io/worksheet.html
    # parameters  merge_range(first_row, first_col, last_row, last_col, data[, cell_format])

    # Can only write simple types to merged ranges so write a blank string
    test_notes = '                          Pass / Fail criteria based on Offset per spatial stream being greater then {pf_dbm} dBm'.format(pf_dbm=pf_dbm)
    worksheet.merge_range(0, 0, 0, 38, ' ', title_format)
    worksheet.write_rich_string(0, 0, dark_green, '      Candela Technologies : ', black, '{test_name} '.format(test_name=test_name), black_not_bold, '\n{test_notes}'.format(test_notes=test_notes), title_format)

    worksheet.set_row(1, 75)  # Set height
    worksheet.set_column(0, 0, 10)  # Set width

    row = 1
    col = 0
    worksheet.write(row, col, 'Country\nCode', dblue_bold)
    col += 1
    worksheet.write(row, col, 'Regulatory\nDomain', dblue_bold)
    col += 1
    worksheet.set_column(col, col, 16)  # Set width
    worksheet.write(row, col, 'Controller\nTest Rig:\n{test_rig}\nLocation\n{location}'.format(test_rig=args.test_rig, location=args.testbed_location), dblue_bold)
    col += 1
    worksheet.set_column(col, col, 25)  # Set width
    worksheet.write(row, col, 'Controller\nChannel', dblue_bold)
    col += 1
    worksheet.set_column(col, col, 20)  # Set width
    worksheet.write(row, col, '{ap}\nClient Reported\nChannel'.format(ap=args.ap), dblue_bold)
    col += 1
    worksheet.write(row, col, 'Client\nNSS', dblue_bold)
    col += 1
    worksheet.set_column(col, col, 10)  # Set width
    worksheet.write(row, col, 'Controller\nBW', dblue_bold)
    col += 1
    worksheet.set_column(col, col, 10)  # Set width
    worksheet.write(row, col, 'Station\nReported\nBW', dblue_bold)
    col += 1
    worksheet.write(row, col, 'Tx\nPower\nSetting', dtan_bold)
    col += 1
    worksheet.write(row, col, 'AP Tx\nPower\nSetting', dtan_bold)
    col += 1
    worksheet.set_column(col, col, 20)  # Set width
    worksheet.write(row, col, 'Controller Reported\nTotal\nTx Power dBm\nFrom AP Summary', dtan_bold)
    col += 1
    worksheet.set_column(col, col, 20)  # Set width
    worksheet.write(row, col, 'AP Reported\nTotal\nTx Power dBm\n', dtan_bold)
    if (bool(ap_dict)):
        col += 1
        worksheet.set_column(col, col, 20)  # Set width
        worksheet.write(row, col, 'AP Reported\nTotal \nTx Power dBm', dtan_bold)
    col += 1
    worksheet.set_column(col, col, 20)  # Set width
    worksheet.write(row, col, 'Allowed dBm\nPer Spatial Stream\n cc_dbm', dtan_bold)
    if (bool(ap_dict)):
        col += 1
        worksheet.set_column(col, col, 20)  # Set width
        worksheet.write(row, col, 'AP reported\nAllowed dBm\nPer Spatial Steam\n ap_dbm', dtan_bold)

    col += 1
    worksheet.write(row, col, 'Cabling\nPathloss', dtan_bold)
    col += 1
    worksheet.write(row, col, 'Antenna\nGain', dtan_bold)
    col += 1
    worksheet.set_column(col, col, 10)  # Set width
    worksheet.write(row, col, 'Client\n Reported\n Noise', dpeach_bold)
    col += 1
    worksheet.set_column(col, col, 15)  # Set width
    worksheet.write(row, col, 'rssi_adj:\nnoise bare\n - noise floor', dpeach_bold)
    col += 1
    if (args.adjust_nf):
        worksheet.write(row, col, 'Noise Floor\nAdjust\n(vs -105)', dpeach_bold)
        col += 1

    worksheet.set_column(col, col, 15)  # Set width
    worksheet.write(row, col, 'Client Reported\nRx Rate', dpeach_bold)
    col += 1
    worksheet.set_column(col, col, 20)  # Set width
    worksheet.write(row, col, 'Client Reported\nBeacon Signal dBm\nRSSI', dpeach_bold)
    col += 1
    worksheet.set_column(col, col, 20)  # Set width
    worksheet.write(row, col, 'Client Reported\nCombined Signal dBm\nRSSI\n(Signal ave)', dpeach_bold)
    col += 1
    worksheet.set_column(col, col, 15)  # Set width
    worksheet.write(row, col, 'Client Reported\nAntenna\nSignal\ndBm\n SS 1', dpeach_bold)
    col += 1
    worksheet.set_column(col, col, 15)  # Set width
    worksheet.write(row, col, 'Client Reported\nAntenna\nSignal\ndBm\n SS 2', dpeach_bold)
    col += 1
    worksheet.set_column(col, col, 15)  # Set width
    worksheet.write(row, col, 'Client Reported\nAntenna\nSignal\ndBm\n SS 3', dpeach_bold)
    col += 1
    worksheet.set_column(col, col, 15)  # Set width
    worksheet.write(row, col, 'Client Reported\nAntenna\nSignal\ndBm\n SS 4', dpeach_bold)
    col += 1
    worksheet.set_column(col, col, 25)  # Set width
    worksheet.write(row, col, 'Calculated Antenna 1 =\n Antenna Sig dBm\n + pathloss\n + rssi_adj\n + ant gain', dpink_bold)
    col += 1
    worksheet.set_column(col, col, 25)  # Set width
    worksheet.write(row, col, 'Calculated Antenna 2 =\n Antenna Sig dBm\n + pathloss\n + rssi_adj\n + ant gain', dpink_bold)
    col += 1
    worksheet.set_column(col, col, 25)  # Set width
    worksheet.write(row, col, 'Calculated Antenna 3 =\n Antenna Sig dBm\n + pathloss\n + rssi_adj\n + ant gain', dpink_bold)
    col += 1
    worksheet.set_column(col, col, 25)  # Set width
    worksheet.write(row, col, 'Calculated Antenna 4 =\n Antenna Sig dBm\n + pathloss\n + rssi_adj\n + ant gain', dpink_bold)
    col += 1
    worksheet.set_column(col, col, 20)  # Set width
    worksheet.write(row, col, 'Offset 1 = \nCalculated Antenna 1\n - cc_dbm(per SS)', dyel_bold)
    col += 1
    worksheet.set_column(col, col, 20)  # Set width
    worksheet.write(row, col, 'Offset 2 = \nCalculated Antenna 2\n - cc_dbm(per SS)', dyel_bold)
    col += 1
    worksheet.set_column(col, col, 20)  # Set width
    worksheet.write(row, col, 'Offset 3 = \nCalculated Antenna 3\n - cc_dbm(per SS)', dyel_bold)
    col += 1
    worksheet.set_column(col, col, 20)  # Set width
    worksheet.write(row, col, 'Offset 4 = \nCalculated Antenna 4\n - cc_dbm(per SS)', dyel_bold)
    col += 1
    worksheet.set_column(col, col, 15)  # Set width
    worksheet.write(row, col, 'Controller\nReported\ndBm', dblue_bold)
    col += 1
    worksheet.set_column(col, col, 25)  # Set width
    worksheet.write(row, col, 'Client Calc Beacon dBm\n beacon + pathloss\n + rssi_adj - antenna gain', dblue_bold)
    col += 1
    worksheet.set_column(col, col, 25)  # Set width
    worksheet.write(row, col, 'Difference Between\n Controller dBm\n & Client Calc Beacon dBm \n (+/- {diff} dBm)'.format(diff=args.beacon_dbm_diff), dblue_bold)
    col += 1
    worksheet.set_column(col, col, 25)  # Set width
    worksheet.write(row, col, 'Client Calc\n Combined Signal dBm\n total signal dBm + pathloss\n + rssi_adj - antenna gain', dblue_bold)
    col += 1
    worksheet.set_column(col, col, 25)  # Set width
    worksheet.write(row, col, 'Difference Between\n Controller dBm\n& Client Calc Combined\n Signal dBm', dblue_bold)
    col += 1
    worksheet.set_column(col, col, 12)  # Set width
    worksheet.write(row, col, "PASS /\nFAIL\n( += %s dBm)" % (pf_dbm), dgreen_bold)
    col += 1
    worksheet.set_column(col, col, 24)  # Set width
    worksheet.write(row, col, 'Time Stamp\n', dgreen_bold)
    col += 1
    worksheet.set_column(col, col, 24)  # Set width
    worksheet.write(row, col, 'Run Time Single Test\n', dgreen_bold)
    col += 1
    worksheet.set_column(col, col, 24)  # Set width
    worksheet.write(row, col, 'Total Run Time\n', dgreen_bold)
    col += 1
    worksheet.set_column(col, col, 100)  # Set width
    worksheet.write(row, col, 'Information, Warnings, Errors', dgreen_bold_left)
    col += 1
    row += 1

    bandwidths = args.bandwidth.split()
    channels = args.channel.split()
    nss = args.nss.split()
    # args.tx_power.split() will be read later since 6E 20 Mhz does not do tx power 7 8, 40 Mhz does not do power 8
    txpowers = args.txpower.split()

    # The script has the ability to create a station if one does not exist
    if (args.create_station):
        if (args.radio is None):
            logg.info("WARNING --create needs a radio")
            close_workbook(workbook)
            exit(1)
        if (args.band == '6g' or args.band == 'dual_band_6g'):
            if (args.vht160):
                logg.info("creating station with VHT160 set: {} on radio {}".format(args.station, args.radio))
                logg.info("cwd lf_associate_ap.pl: {dir}".format(dir=os.getcwd()))
                subprocess.run(["./lf_associate_ap.pl", "--mgr", lfmgr, "--radio", args.radio, "--ssid", args.ssid, "--passphrase", args.ssidpw, "--bssid", args.bssid,
                                "--security", args.security, "--upstream", args.upstream_port, "--first_ip", "DHCP",
                                "--first_sta", args.station, "--ieee80211w", args.ieee80211w, "--wifi_mode", args.wifi_mode, "--action", "add", "--xsec", "ht160_enable"], timeout=20, capture_output=True)
                sleep(3)
            else:
                logg.info("creating station: {} on radio {}".format(args.station, args.radio))
                subprocess.run(["./lf_associate_ap.pl", "--mgr", lfmgr, "--radio", args.radio, "--ssid", args.ssid, "--passphrase", args.ssidpw, "--bssid", args.bssid,
                                "--security", args.security, "--upstream", args.upstream_port, "--first_ip", "DHCP",
                                "--first_sta", args.station, "--ieee80211w", args.ieee80211w, "--wifi_mode", args.wifi_mode, "--action", "add"], timeout=20, capture_output=True)

        else:
            if (args.vht160):
                logg.info("creating station with VHT160 set: {} on radio {}".format(args.station, args.radio))
                print()
                subprocess.run(["./lf_associate_ap.pl", "--mgr", lfmgr, "--radio", args.radio, "--ssid", args.ssid, "--passphrase", args.ssidpw, "--bssid", args.bssid,
                                "--security", args.security, "--upstream", args.upstream_port, "--first_ip", "DHCP",
                                "--first_sta", args.station, "--ieee80211w", args.ieee80211w, "--wifi_mode", args.wifi_mode, "--action", "add", "--xsec", "ht160_enable"], timeout=20, capture_output=False)
                sleep(3)
            else:
                logg.info("creating station: {} on radio {}".format(args.station, args.radio))
                subprocess.run(["./lf_associate_ap.pl", "--mgr", lfmgr, "--radio", args.radio, "--ssid", args.ssid, "--passphrase", args.ssidpw, "--bssid", args.bssid,
                                "--security", args.security, "--upstream", args.upstream_port, "--first_ip", "DHCP",
                                "--first_sta", args.station, "--ieee80211w", args.ieee80211w, "--wifi_mode", args.wifi_mode, "--action", "add"], timeout=20, capture_output=False)
        sleep(3)

    # Find LANforge station parent radio
    parent = None
    logg.info("portmod command: ./lf_portmod.pl --manager {lfmgr} --card {lfresource} --port_name {lfstation} --show_port Parent/Peer".format(
        lfmgr=lfmgr, lfresource=lfresource, lfstation=lfstation))
    port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card", lfresource, "--port_name", lfstation,
                                 "--show_port", "Parent/Peer"], capture_output=True)
    pss = port_stats.stdout.decode('utf-8', 'ignore')
    for line in pss.splitlines():
        m = re.search('Parent/Peer:\\s+(.*)', line)
        if (m is not None):
            parent = m.group(1)

    # Create downstream connection
    # First, delete any old one
    subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "do_cmd",
                    "--cmd", "rm_cx all c-udp-power"], capture_output=False)

    subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "do_cmd",
                    "--cmd", "rm_endp c-udp-power-A"], capture_output=False)

    subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource2, "--action", "do_cmd",
                    "--cmd", "rm_endp c-udp-power-B"], capture_output=False)
    # Now, create the new connection
    # higher is better because it means more frames at the signal level to be measured vs leaked frames at low signal lev

    subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "create_endp", "--port_name", lfstation,
                    "--endp_type", "lf_udp", "--endp_name", "c-udp-power-A", "--speed", "0", "--report_timer", "1000"], capture_output=False)
    subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource2, "--action", "create_endp", "--port_name", upstream_port,
                    "--endp_type", "lf_udp", "--endp_name", "c-udp-power-B", "--speed", "100000000", "--report_timer", "1000"], capture_output=False)
    subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "create_cx", "--cx_name", "c-udp-power",
                    "--cx_endps", "c-udp-power-A,c-udp-power-B", "--report_timer", "1000"], capture_output=False)
    command = ["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "create_endp", "--port_name", lfstation,
               "--endp_type", "lf_udp", "--endp_name", "c-udp-power-A", "--speed", "9600", "--report_timer", "1000"]
    logg.info("command: {command}".format(command=command))
    summary_output = ''
    summary = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(summary.stdout.readline, ''):
        logger.debug(line)
        summary_output += line
    summary.wait()
    logger.info(summary_output)

    command = ["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource2, "--action", "create_endp", "--port_name", upstream_port,
               "--endp_type", "lf_udp", "--endp_name", "c-udp-power-B", "--speed", "100000000", "--report_timer", "1000"]
    logg.info("command: {command}".format(command=command))
    summary_output = ''
    summary = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(summary.stdout.readline, ''):
        logger.debug(line)
        summary_output += line
    summary.wait()
    logger.info(summary_output)
    # ./lf_firemod.pl --manager 192.168.100.178 --resource 1 --action create_cx --cx_name c-udp-power --cx_endps c-udp-power-A,c-udp-power-B --report_timer 1000 --endp_type lf_udp --port_name sta0003 --use_speeds 0,1000000
    command = ["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "create_cx", "--cx_name", "c-udp-power",
               "--cx_endps", "c-udp-power-A,c-udp-power-B", "--report_timer", "1000", "--endp_type", "lf_udp", "--port_name", lfstation,
               "--use_speeds", "9600,100000000"]
    logg.info("command: {command}".format(command=command))
    summary_output = ''
    summary = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(summary.stdout.readline, ''):
        logger.debug(line)
        summary_output += line
    summary.wait()
    logger.info(summary_output)

    # Notes:
    # These need to be verified with test_ip_variable_time.py - which calculates the speeds
    #  1 antenna 80 Mhz 433 Mbps
    #  2 antenna 80 Mhz 867 Mbps
    #  3 antenna 80 Mhz 1,300 Mbps
    #  4 antenna 80 Mhz 1,733 Mbps

    #  1 antenna 160 Mhz 867 Mbps
    #  2 antenna 160 Mhz 1,733 Mbps
    #  3 antenna 160 Mhz 2,600 Mbps
    #  4 antenna 160 Mhz 3,466 Mbps

    # ./lf_firemod.pl --manager 192.168.100.178 --resource 1 --action create_cx --cx_name c-udp-power --cx_endps c-udp-power-A,c-udp-power-B --report_timer 1000 --endp_type udp --port_name sta0000 --speed 1000000

    # 5ghz speeds

    # myrd = "NA"
    # mycc = ""
    # The script supports both the 9800 series controller and the 3504 series controller ,  the controllers have different interfaces
    # if args.series == "9800":
    #
    #   cs.no_logging_console()
    #   cs.line_console_0()

    cs.series = "9800"
    cs.testbed_location = args.testbed_location
    cs.console_setup()

    cs.read_country_code_and_regulatory_domain()

    myrd = cs.regulatory_domain
    mycc = cs.country_code

    cs.read_ap_config_radio_role()

    # this reads if the radio role is 'Manual' or 'Auto'
    # A Manual role has the channel, channel width and tx_power
    # stay on the settings that are set in the AP or controller
    ap_config_radio_role = cs.ap_config_radio_role

    # these are set to configure the number of spatial streams and MCS values
    # 5g has 8 spatial streams , MCS is 7, 9, 11
    # ap dot11 6ghz dot11ax mcs tx index 7 spatial-stream 1 << - turn on
    # no ap dot11 6ghz dot11ax mcs tx index 7 www.you-stream 2 <<-- turn off

    # Loop through all iterations and run txpower tests.
    # The is the main loop of loops:   Channels, spatial streams (nss), bandwidth (bw), txpowers (tx)
    # Note: supports 9800 and 3504 controllers
    # create blank time stamp
    total_run_duration = datetime.timedelta(0)
    run_start_time = datetime.datetime.now()
    run_start_time_str = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")).replace(':', '-')
    logger.info("run_start_time : {run_start_time}".format(run_start_time=run_start_time_str))
    for ch in channels:
        pathloss = args.pathloss
        antenna_gain = args.antenna_gain
        ch_colon = ch.count(":")
        if (ch_colon == 1):
            cha = ch.split(":")
            pathloss = cha[1]
            ch = cha[0]
        for n in nss:
            if (n != "NA" and args.set_nss):
                # Disable the wlan to set the spatial streams
                # Disable wlan, apply settings, Enable wlan
                if args.band == "dual_band_6g":
                    cs.ap_dot11_dual_band_6ghz_shutdown()
                    cs.ap_dot11_6ghz_shutdown()
                elif args.band == "dual_band_5g":
                    cs.ap_dot11_dual_band_5ghz_shutdown()
                    cs.ap_dot11_5ghz_shutdown()
                elif args.band == "6g":
                    cs.ap_dot11_6ghz_shutdown()
                elif args.band == "5g":
                    cs.ap_dot11_5ghz_shutdown()
                elif args.band == "24g":
                    cs.ap_dot11_24ghz_shutdown()

                # the band will be set
                num_spatial_streams = int(n)
                # set the spatial streams for   - need to disable the wlan and re-enable
                # ap dot11 dot11ax mcs tx index 7 spatial-stream 1 << - turn on
                # no ap dot11 dot11ax mcs tx index 7 spatial-stream 2 <<-- turn off

                # Cannot disable MCS lower data rates when higher data rates are enabled
                # enabling MCS  from lower MCS to higher MCS
                # disabling MCS from higher MCS to lower MCS
                if num_spatial_streams == 1 or num_spatial_streams == 2 or num_spatial_streams == 3 or num_spatial_streams == 4:
                    cs.spatial_stream = 1
                    cs.mcs_tx_index = 7
                    cs.ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 9
                    cs.ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 11
                    cs.ap_dot11_dot11ax_mcs_tx_index_spatial_stream()

                if num_spatial_streams == 2 or num_spatial_streams == 3 or num_spatial_streams == 4:
                    cs.spatial_stream = 2
                    cs.mcs_tx_index = 7
                    cs.ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 9
                    cs.ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 11
                    cs.ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                else:
                    cs.spatial_stream = 2
                    cs.mcs_tx_index = 11
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 9
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 7
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()

                if num_spatial_streams == 3 or num_spatial_streams == 4:
                    cs.spatial_stream = 3
                    cs.mcs_tx_index = 7
                    cs.ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 9
                    cs.ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 11
                    cs.ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                else:
                    cs.spatial_stream = 3
                    cs.mcs_tx_index = 11
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 9
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 7
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()

                if num_spatial_streams == 4:
                    cs.spatial_stream = 3
                    cs.mcs_tx_index = 7
                    cs.ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 9
                    cs.ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 11
                    cs.ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                else:
                    cs.spatial_stream = 4
                    cs.mcs_tx_index = 11
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 9
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 7
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()

                if args.band == '5g' or args.band == 'dual_band_5g':
                    # turn off spatial streams 5 - 8
                    # disable spatial stream 5
                    cs.spatial_stream = 5
                    cs.mcs_tx_index = 11
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 9
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 7
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()

                    # disable spatial stream 6
                    cs.spatial_stream = 6
                    cs.mcs_tx_index = 11
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 9
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 7
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()

                    # disable spatial stream 7
                    cs.spatial_stream = 7
                    cs.mcs_tx_index = 11
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 9
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 7
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()

                    # disable spatial stream 8
                    cs.spatial_stream = 8
                    cs.mcs_tx_index = 11
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 9
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()
                    cs.mcs_tx_index = 7
                    cs.no_ap_dot11_dot11ax_mcs_tx_index_spatial_stream()

            for bw in bandwidths:
                if (n != "NA"):
                    ni = int(n)
                    if (parent is None):
                        logg.info("ERROR:  Skipping setting the spatial streams because cannot find Parent radio for station: %s." % (lfstation))
                    else:
                        # Set nss on LANforge Station, not sure it can be done on AP
                        # for ax210, it can do any bandwidth at up to 2 NSS
                        # for 9984 (wave-2), it does have restrictions
                        # 9984 can do 4x4 at 80Mhz, and 2x2 at 160Mhz
                        if (bw == "160"):
                            if(args.vht160):
                                # for 9984 (wave-2) for 160 Mhz set for 160 set ni = 2
                                if(args.wave2):
                                    ni = int(2)
                                    logg.info("NOTE: wave2 (9984) has restrictions : 160Mhz is 2x2 --vht160 set and will set ni : {}".format(ni))
                            else:
                                logg.info("NOTE: Skipping NSS %s for 160Mhz, LANforge needs 160Mhz enabled." % (n))
                                logg.info("NOTE: use --vht160 to force 160Mhz")
                                continue
                    antset = 0  # all available
                    if (ni == 1):
                        antset = 1
                    if (ni == 2):
                        antset = 4
                    if (ni == 3):
                        antset = 7
                    if (ni == 4):
                        antset = 8
                    set_cmd = "set_wifi_radio 1 %s %s NA NA NA NA NA NA NA NA NA %s" % (lfresource, parent, antset)
                    logg.info("Setting LANforge radio to %s NSS with command: %s" % (ni, set_cmd))
                    subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card", lfresource, "--port_name", parent,
                                    "--cli_cmd", set_cmd], capture_output=True)
                # tx power 1 is the highest power ,  2 power is 1/2 of 1 power etc till power 8 the lowest.
                # 6E 20Mhz tx power 1 - 6
                # 6E 40Mhz tx power 1 - 7
                # TODO make txpower file into object ,
                if args.tx_power_adjust_6E:
                    txpowers = args.txpower.split()
                    if args.band == '6g' or args.band == 'dual_band_6g':
                        if bw == '20':
                            if '8' in txpowers:
                                txpowers.remove('8')
                            if '7' in txpowers:
                                txpowers.remove('7')
                        elif bw == '40':
                            if '8' in txpowers:
                                txpowers.remove('8')

                for tx in txpowers:
                    # e_tot is the errors, w_tot is the warning, i_tot is information
                    e_tot = ""
                    w_tot = ""
                    i_tot = ""

                    # Stop traffic , if traffic was running ,  this is on the lanforge side.  Commands that start with lf_ are directed
                    # towards the lanforge
                    subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "do_cmd",
                                    "--cmd", "set_cx_state all c-udp-power STOPPED"], capture_output=True)
                    command = ["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "do_cmd",
                               "--cmd", "set_cx_state all c-udp-power STOPPED"]
                    summary_output = ''
                    summary = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    for line in iter(summary.stdout.readline, ''):
                        logger.debug(line)
                        summary_output += line
                    summary.wait()
                    logger.info(summary_output)

                    # Down station
                    # CMR TODO this looks to be an issue  7/15/2022
                    command = ["./lf_portmod.pl", "--manager", lfmgr, "--card", lfresource, "--port_name", lfstation,
                                                  "--set_ifstate", "down"]
                    summary_output = ''
                    summary = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    for line in iter(summary.stdout.readline, ''):
                        logger.debug(line)
                        summary_output += line
                    summary.wait()
                    logger.info(summary_output)
                    cs.show_ap_summary()

                    
                    # Begin setting client Serving mode , Dual band and creating dual-band
                    # when both 5g (slot 1) is enabled and dual-band 5g (slot 2) is enabled .
                    # 5g slot 1 will used the 5g channels to 64,  the 5g dual-band will use channels 100 -> 165.
                    # When 5g (slot 1) and dual-band 6g (slot 2) is enabled then 5g (slot 1) has all bands.

                    # if dual band : disable dual-band mode, config mode, enable dual-band mode
                    # disable dual-band mode
                    # for other bands just disable the radio
                    if args.band == "dual_band_6g":
                        logg.info("ap_dot11_dual_band_mode_shutdown_6ghz")
                        cs.ap_dot11_dual_band_mode_shutdown_6ghz()
                    elif args.band == "dual_band_5g":
                        logg.info("ap_dot11_dual_band_mode_shutdown_5ghz")
                        cs.ap_dot11_dual_band_mode_shutdown_5ghz()
                    elif args.band == "6g":
                        logg.info("ap_dot11_shutdown_6ghz")
                        cs.show_ap_dot11_6gz_shutdown()
                    elif args.band == "5g":
                        logg.info("ap_dot11_shutdown_5ghz")
                        cs.show_ap_dot11_5gz_shutdown()
                    elif args.band == "24g":
                        logg.info("ap_dot11_shutdown_24ghz")
                        cs.show_ap_dot11_24gz_shutdown()


                    # if dual band : disable dual-band mode, config mode, enable dual-band mode
                    # disable dual-band mode


                    # set the radio role selection if not set
                    if ap_config_radio_role != 'Manual':
                        if args.band == 'dual_band_6g':
                            logg.info("ap_dot11_dual_band_6ghz_radio_role_manual_client_serving")
                            cs.ap_dot11_dual_band_6ghz_radio_role_manual_client_serving()
                        elif args.band == 'dual_band_5g':
                            logg.info("ap_dot11_dual_band_5ghz_radio_role_manual_client_serving")
                            cs.ap_dot11_dual_band_5ghz_radio_role_manual_client_serving()
                        elif args.band == '6g':
                            cs.ap_dot11_6ghz_radio_role_manual_client_serving()
                            logg.info("ap_dot11_6ghz_radio_role_manual_client_serving")
                        elif args.band == '5g':
                            cs.ap_dot11_5ghz_radio_role_manual_client_serving()
                            logg.info("ap_dot11_5ghz_radio_role_manual_client_serving")
                        elif args.band == '24g':
                            cs.ap_dot11_24ghz_radio_role_manual_client_serving()
                            logg.info("ap_dot11_24ghz_radio_role_manual_client_serving")

                    # config dual-band mode
                    if args.band == "dual_band_6g":
                        cs.config_ap_dot11_dual_band_to_6ghz()
                    elif args.band == "dual_band_5g":
                        cs.config_ap_dot11_dual_band_to_5ghz()

                    # enable  dual-band mode
                    if args.band == "dual_band_6g":
                        cs.ap_dot11_dual_band_no_mode_shutdown_6ghz()
                    elif args.band == "dual_band_5g":
                        cs.ap_dot11_dual_band_no_mode_shutdown_5ghz()

                    # Disable AP, apply settings, enable AP
                    if args.band == "dual_band_6g":
                        cs.ap_dot11_dual_band_6ghz_shutdown()
                    elif args.band == "dual_band_5g":
                        cs.ap_dot11_dual_band_5ghz_shutdown()
                    elif args.band == "6g":
                        cs.ap_dot11_6ghz_shutdown()
                    elif args.band == "5g":
                        cs.ap_dot11_5ghz_shutdown()
                    elif args.band == "24g":
                        cs.ap_dot11_24ghz_shutdown()

                    if args.series == "9800":
                        # 9800 series need to  "Configure radio for manual channel assignment"
                        logg.info("9800 Configure radio for manual channel assignment")
                        cs.wlan_shutdown()
                        if args.band == 'dual_band_6g':
                            cs.ap_dot11_dual_band_6ghz_shutdown()
                        elif args.band == 'dual_band_5g':
                            cs.ap_dot11_dual_band_5ghz_shutdown()
                        elif args.band == '6g':
                            cs.ap_dot11_6ghz_shutdown()
                        elif args.band == '5g':
                            cs.ap_dot11_5ghz_shutdown()
                        elif args.band == '24g':
                            cs.ap_dot11_24ghz_shutdown()


                    else:
                        cs.ap_dot11_5ghz_shutdown()
                        cs.ap_dot11_24ghz_shutdown()

                    logg.info("9800/3504 test_parameters_summary: set : tx: {tx_power} ch: {channel} bw: {bandwidth}".format(
                        tx_power=tx, channel=ch, bandwidth=bw))
                    if (tx != "NA"):
                        logg.info("9800/3504 test_parameters: set txPower: {tx_power}".format(tx_power=tx))
                        cs.tx_power = tx

                        if args.band == 'dual_band_6g':
                            cs.config_dot11_dual_band_6ghz_tx_power()
                        elif args.band == 'dual_band_5g':
                            cs.config_dot11_dual_band_5ghz_tx_power()
                        elif args.band == '6g':
                            cs.config_dot11_6ghz_tx_power()
                        elif args.band == '5g':
                            cs.config_dot11_5ghz_tx_power()
                        elif args.band == '24g':
                            cs.config_dot11_24ghz_tx_power()

                    # NSS is set on the station earlier...
                    if (ch != "NA"):
                        logg.info("9800/3504 test_parameters set channel: {}".format(ch))
                        cs.channel = ch
                        if args.band == 'dual_band_6g':
                            cs.config_dot11_dual_band_6ghz_channel()
                        elif args.band == 'dual_band_5g':
                            cs.config_dot11_dual_band_5ghz_channel()
                        elif args.band == '6g':
                            cs.config_dot11_6ghz_channel()
                        elif args.band == '5g':
                            cs.config_dot11_5ghz_channel()
                        elif args.band == '24g':
                            cs.config_dot11_24ghz_channel()

                    if (bw != "NA"):
                        logg.info("9800/3504 test_parameters bandwidth: set : {}".format(bw))
                        cs.bandwidth = bw
                        if args.band == 'dual_band_6g':
                            cs.config_dot11_dual_band_6ghz_channel_width()
                        elif args.band == 'dual_band_5g':
                            cs.config_dot11_dual_band_5ghz_channel_width()
                        elif args.band == '6g':
                            cs.config_dot11_6ghz_channel_width()
                        elif args.band == '5g':
                            cs.config_dot11_5ghz_channel_width()
                        elif args.band == '24g':
                            # 24g can only be 20 Mhz
                            pass

                    # only create the wlan the first time
                    if args.series == "9800":
                        if args.create_wlan is False:
                            wlan_created = True
                        if wlan_created:
                            pss = cs.show_wlan_summary()
                            logg.info(pss)
                            logg.info(
                                "wlan already present, no need to create wlanID {} wlan {} wlanSSID {} port {}".format(
                                    args.wlanID, args.wlan, args.wlanSSID, args.port))

                            if args.band == 'dual_band_6g':
                                pss = cs.show_ap_dot11_dual_band_6gz_summary()
                                logg.info(pss)
                                pss = cs.show_ap_bssid_dual_band_6ghz()
                                logg.info(pss)
                            elif args.band == 'dual_band_5g':
                                pss = cs.show_ap_dot11_dual_band_5gz_summary()
                                logg.info(pss)
                                pss = cs.show_ap_bssid_dual_band_5ghz()
                                logg.info(pss)
                            elif args.band == '6g':
                                pss = cs.show_ap_dot11_6gz_summary()
                                logg.info(pss)
                                pss = cs.show_ap_bssid_6ghz()
                                logg.info(pss)
                            elif args.band == '5g':
                                pss = cs.show_ap_dot11_5gz_summary()
                                logg.info(pss)
                                pss = cs.show_ap_bssid_5ghz()
                                logg.info(pss)
                            elif args.band == '24g':
                                pss = cs.show_ap_dot11_24gz_summary()
                                logg.info(pss)
                                pss = cs.show_ap_bssid_24ghz()
                                logg.info(pss)
                        else:
                            # Verify that a wlan does not exist on wlanID
                            # delete the wlan if already exists
                            pss = cs.show_wlan_summary()
                            logg.info(pss)
                            if args.band == 'dual_band_6g':
                                cs.show_ap_dot11_dual_band_6gz_summary()
                            elif args.band == 'dual_band_5g':
                                cs.show_ap_dot11_dual_band_5gz_summary()
                            elif args.band == '6g':
                                cs.show_ap_dot11_6gz_summary()
                            elif args.band == '5g':
                                cs.show_ap_dot11_5gz_summary()
                            elif args.band == '24g':
                                cs.show_ap_dot11_24gz_summary()

                            #  "number of WLANs:\\s+(\\S+)"
                            # https://regex101.com/
                            search_wlan = False
                            for line in pss.splitlines():
                                logg.info(line)
                                if (line.startswith("---------")):
                                    search_wlan = True
                                    continue
                                if (search_wlan):
                                    pat = "{}\\s+(\\S+)\\s+(\\S+)".format(args.wlanID)
                                    m = re.search(pat, line)
                                    if (m is not None):
                                        cc_wlan = m.group(1)
                                        cc_wlan_ssid = m.group(2)
                                        # wlanID is in use
                                        logg.info("###############################################################################")
                                        logg.info("Need to remove wlanID: {} cc_wlan: {} cc_wlan_ssid: {}".format(args.wlanID, cc_wlan, cc_wlan_ssid))
                                        logg.info("###############################################################################")
                                        cs.config_no_wlan()

                            # Create wlan
                            wlan_created = True
                            logg.info("create wlan {} wlanID {} port {}".format(args.wlan, args.wlanID, args.port))
                            # TODO be able to do for WPA2 , WPA3
                            # TODO check for failure to close cookbook
                            # this needs to be configurable
                            if args.security == 'open':
                                cs.config_wlan_open()
                            elif args.security == 'wpa2':
                                cs.config_wlan_wpa2()
                            elif args.security == 'wpa3':
                                cs.config_wlan_wpa3()

                            cs.config_wireless_tag_policy_and_policy_profile()

                        # enable_wlan
                        cs.config_enable_wlan_send_no_shutdown()


                    # enable transmission for the entier 802.11z network
                    # the wlan may not care about dual_band
                    # enable_network_6ghz or enable_network_5ghz or enable_network_24ghz
                    if args.band == 'dual_band_6g':
                        # enable 6g wlan
                        pss = cs.config_no_ap_dot11_dual_band_6ghz_shutdown()
                        logg.info(pss)
                        # enable 6g operation status
                        pss = cs.config_ap_no_dot11_dual_band_6ghz_shutdown()
                        logg.info(pss)

                        # enable 6g wlan
                        pss = cs.config_no_ap_dot11_6ghz_shutdown()
                        logg.info(pss)
                        # enable 6g operation status
                        pss = cs.config_ap_no_dot11_6ghz_shutdown()
                        logg.info(pss)

                        # enable 5g wlan to show scans
                        pss = cs.config_no_ap_dot11_5ghz_shutdown()
                        logger.info(pss)
                        # enable 5g operation status
                        pss = cs.config_ap_no_dot11_5ghz_shutdown()
                        logger.info(pss)

                    elif args.band == 'dual_band_5g':
                        # enable 5g wlan - dual band
                        pss = cs.config_no_ap_dot11_dual_band_5ghz_shutdown()
                        logg.info(pss)
                        # enable 5g operation status
                        pss = cs.config_ap_no_dot11_dual_band_5ghz_shutdown()
                        logg.info(pss)
                        # enable 5g wlan
                        pss = cs.config_no_ap_dot11_5ghz_shutdown()
                        logger.info(pss)
                        # enable 5g operation status
                        pss = cs.config_ap_no_dot11_5ghz_shutdown()
                        logger.info(pss)

                    elif args.band == '6g':
                        # enable 6g wlan
                        pss = cs.config_no_ap_dot11_6ghz_shutdown()
                        logg.info(pss)
                        # enable 6g operation status
                        pss = cs.config_ap_no_dot11_6ghz_shutdown()
                        logg.info(pss)
                        # 6g needs to see the 5g bands
                        # enable 5g wlan
                        pss = cs.config_no_ap_dot11_5ghz_shutdown()
                        logger.info(pss)
                        # enable 5g operation status
                        pss = cs.config_ap_no_dot11_5ghz_shutdown()
                        logger.info(pss)

                    elif args.band == '5g':
                        # enable 5g wlan
                        pss = cs.config_no_ap_dot11_5ghz_shutdown()
                        logg.info(pss)
                        # enable 5g operation status
                        pss = cs.config_ap_no_dot11_5ghz_shutdown()
                        logg.info(pss)
                    elif args.band == '24g':
                        # enable wlan 24ghz
                        pss = cs.config_no_ap_dot11_24ghz_shutdown()
                        logg.info(pss)
                        # enable 24ghz operation status
                        cs.config_ap_no_dot11_24ghz_shutdown()
                        logg.info(pss)

                    # Wait a bit for AP to come back up
                    time.sleep(3)
                    loop_count = 0
                    cc_dbm_rcv = False
                    if args.series == "9800":
                        while cc_dbm_rcv is False and loop_count <= 3:
                            logg.info("9800 read controller dBm")
                            loop_count += 1
                            time.sleep(1)

                            if args.band == 'dual_band_6g':
                                pss = cs.show_ap_dot11_dual_band_6gz_summary()
                                logg.info("show ap dot11 dual-band (6ghz) summary")
                                logg.info("ap: {ap} ap_band_slot_6g: {slot} ".format(ap=args.ap, slot=args.ap_band_slot_6g))
                                logg.info(pss)
                            elif args.band == 'dual_band_5g':
                                pss = cs.show_ap_dot11_dual_band_5gz_summary()
                                logg.info("show ap dot11 dual-band (5ghz) summary")
                                logg.info("ap: {ap} ap_band_slot_5g: {slot} ".format(ap=args.ap, slot=args.ap_band_slot_5g))
                                logg.info(pss)
                            elif args.band == '6g':
                                pss = cs.show_ap_dot11_6gz_summary()
                                logg.info("show ap dot11 6ghz summary")
                                logg.info("ap: {ap} ap_band_slot_6g: {slot} ".format(ap=args.ap, slot=args.ap_band_slot_6g))
                                logg.info(pss)
                            elif args.band == '5g':
                                logg.info("show ap dot11 5ghz summary")
                                logg.info("ap: {ap} ap_band_slot_5g: {slot} ".format(ap=args.ap, slot=args.ap_band_slot_5g))
                                pss = cs.show_ap_dot11_5gz_summary()
                                logg.info(pss)
                            else:
                                logg.info("show ap dot11 24ghz summary")
                                logg.info("ap: {ap} ap_band_slot_24g: {slot} ".format(ap=args.ap, slot=args.ap_band_slot_24g))
                                pss = cs.show_ap_dot11_24gz_summary()
                                logg.info(pss)

                            searchap = False
                            cc_mac = ""
                            cc_ch = ""
                            cc_bw = ""
                            cc_power = ""
                            cc_dbm = ""
                            for line in pss.splitlines():
                                if (line.startswith("---------")):
                                    searchap = True
                                    continue
                                # if the pattern changes save the output of the advanced command and re parse https://regex101.com
                                if (searchap):
                                    logg.info("##### line #####")
                                    logg.info(line)
                                    if args.band == 'dual_band_6g':
                                        logg.info("ap : {ap} ap_dual_band_slot_6g: {slot}".format(ap=args.ap, slot=args.ap_dual_band_slot_6g))
                                    elif args.band == 'dual_band_5g':
                                        logg.info("ap : {ap} ap_dual_band_slot_5g: {slot}".format(ap=args.ap, slot=args.ap_dual_band_slot_5g))
                                    elif args.band == '6g':
                                        logg.info("ap : {ap} ap_band_slot_6g: {slot}".format(ap=args.ap, slot=args.ap_band_slot_6g))
                                    elif args.band == '5g':
                                        logg.info("ap : {ap} ap_band_slot_5g: {slot}".format(ap=args.ap, slot=args.ap_band_slot_5g))
                                    elif args.band == '24g':
                                        logg.info("ap : {ap} ap_band_slot_24g: {slot}".format(ap=args.ap, slot=args.ap_band_slot_24g))

                                    if args.band == 'dual_band_6g' or args.band == 'dual_band_5g':
                                        pat = "%s\\s+(\\S+)\\s+(\\S+)\\s+\\S+\\s+\\S+\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+dBm\\)+\\s+\\S+\\s+\\S+\\s+(\\S+)" % (args.ap)
                                    else:
                                        pat = "%s\\s+(\\S+)\\s+(\\S+)\\s+\\S+\\s+\\S+\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+dBm\\)+\\s+(\\S+)+\\s" % (args.ap)
                                    logg.info(pat)
                                    m = re.search(pat, line)
                                    logg.info(m)
                                    ap_band_slot = None
                                    if (m is not None):
                                        if args.band == 'dual_band_6g':
                                            logg.info("checking of dual-band slot for 6g {band_slot} present in the show ap dot11 dual-band summary".format(band_slot=args.ap_dual_band_slot_6g))
                                            ap_band_slot = args.ap_dual_band_slot_6g
                                        elif args.band == 'dual_band_5g':
                                            logg.info("checking of dual-band slot for 5g {band_slot} present in the show ap dot11 dual-band summary".format(band_slot=args.ap_dual_band_slot_5g))
                                            ap_band_slot = args.ap_dual_band_slot_5g
                                        elif args.band == '6g':
                                            logg.info("checking of band slot 6g {band_slot} present in the show ap dot11 6ghz summary".format(band_slot=args.ap_band_slot_6g))
                                            ap_band_slot = args.ap_band_slot_6g
                                        elif args.band == '5g':
                                            logg.info("checking of band slot 5g {band_slot} present in the show ap dot11 5ghz summary".format(band_slot=args.ap_band_slot_5g))
                                            ap_band_slot = args.ap_band_slot_5g
                                        elif args.band == '24g':
                                            logg.info("checking of band slot 24g {band_slot} present in the show ap dot11 24ghz summary".format(band_slot=args.ap_band_slot_24g))
                                            ap_band_slot = args.ap_band_slot_24g
                                        else:
                                            logg.warning("band_slot not set, results will be incomplete setting ap_band_slot to 1")
                                            ap_band_slot = '1'

                                        if(m.group(2) == ap_band_slot):
                                            cc_ap = args.ap
                                            cc_mac = m.group(1)
                                            cc_slot = m.group(2)
                                            cc_ch = m.group(6)  # (132,136,140,144)
                                            cc_power = m.group(4)
                                            cc_power = cc_power.replace("/", " of ")  # spread-sheets turn 1/8 into a date
                                            cc_dbm = m.group(5)
                                            cc_dbm = cc_dbm.replace("(", "")

                                            logg.info("ap slot {cc_slot} present in the show ap dot11 {band}hz summary".format(cc_slot=cc_slot, band=args.band))

                                            cc_ch_count = cc_ch.count(",") + 1
                                            cc_bw = m.group(3)
                                            logg.info("show ap summary : {summary}".format(summary=m.group(0)))
                                            logg.info(
                                                ("(ap): {ap}, group 1 (cc_mac): {mac}, group 2(ap band slot): {slot}, group 3 (bw): {admin} "
                                                 "group 4 (cc_Txpwr): {Txpwr}, group 5 (cc_dbm): {dbm}, group 6 (cc_ch): {chan}".format(
                                                     ap=args.ap, mac=m.group(1), slot=m.group(2), admin=m.group(3), Txpwr=m.group(4),
                                                     dbm=m.group(5), chan=m.group(6))))
                                            logg.info("9800 test_parameters_summary:  read: tx: {} ch: {} bw: {}".format(tx, ch, bw))

                                            logg.info("9800  cc_ap:    read : {}".format(cc_ap))
                                            logg.info("9800 from ap summary cc_mac:   read : {}".format(cc_mac))
                                            logg.info("9800 from ap summary cc_slot:  read : {}".format(cc_slot))
                                            logg.info("9800 from ap summary cc_count: read : {}".format(cc_ch_count))
                                            logg.info("9800 from ap summary cc_bw:    read : {}".format(cc_bw))
                                            logg.info("9800 from ap summary cc_power: read : {}".format(cc_power))
                                            logg.info("9800 from ap summary cc_dbm:   read : {}".format(cc_dbm))
                                            logg.info("9800 from ap summary cc_ch:    read : {}".format(cc_ch))
                                            break

                            if (cc_dbm == ""):
                                if loop_count >= 3:
                                    # Could not talk to controller? Not this may not be a reason to exit
                                    # Some of the tests run for 32 plus hours ,  do not kill the whole test unless trying to
                                    # debug an issue with the test.  Sometimes the controller is taking time to configure.
                                    err = "ERROR: cc_dmp not found from query of controller:  is the AP --slot set correctly?"
                                    logg.info(err)
                                    logg.info("run show ap dot11 6/5/24gghz summary ")
                                    e_tot += err
                                    e_tot += "  "
                                else:
                                    logg.info("9800 read controller dBm loop_count {} try again".format(loop_count))
                            else:
                                cc_dbm_rcv = True
                        cs.show_wlan_summary()
                    else:
                        pss = cs.show_ap_dot11_5gz_summary()
                        logg.info(pss)
                        pss = cs.show_ap_dot11_24gz_summary()
                        logg.info(pss)
                        pss = cs.show_wlan_summary()
                        logg.info(pss)

                        searchap = False
                        cc_mac = ""
                        cc_ch = ""
                        cc_bw = ""
                        cc_power = ""
                        cc_dbm = ""
                        ch_count = ""
                        for line in pss.splitlines():
                            if (line.startswith("---------")):
                                searchap = True
                                continue

                            if (searchap):
                                pat = "%s\\s+(\\S+)\\s+\\S+\\s+\\S+\\s+\\S+\\s+(\\S+)\\s+(\\S+)\\s+\\(\\s*(\\S+)\\s+dBm" % (args.ap)
                                m = re.search(pat, line)
                                if (m is not None):
                                    cc_mac = m.group(1)
                                    cc_ch = m.group(2)  # (132,136,140,144)
                                    cc_power = m.group(3)
                                    cc_power = cc_power.replace("/", " of ", 1)  # spread-sheets turn 1/8 into a date
                                    cc_dbm = m.group(4)

                                    ch_count = cc_ch.count(",")
                                    cc_bw = 20 * (ch_count + 1)

                                    break

                        if (cc_dbm == ""):
                            # Could not talk to controller?
                            err = "Warning : Could not query dBm from controller"
                            logg.info(err)
                            e_tot += err
                            e_tot += "  "

                        logg.info("3504 test_parameters cc_mac: read : {}".format(cc_mac))
                        logg.info("3504 test_parameters cc_count: read : {}".format(ch_count))
                        logg.info("3504 test_parameters cc_bw: read : {}".format(cc_bw))
                        logg.info("3504 test_parameters cc_power: read : {}".format(cc_power))
                        logg.info("3504 test_parameters cc_dbm: read : {}".format(cc_dbm))
                        logg.info("3504 test_parameters cc_ch: read : {}".format(cc_ch))

                    # read the AP Tx Power
                    cs.get_ap_tx_power_config()
                    ap_dbm = cs.ap_tx_power_dbm
                    ap_power = "{pw} of {pw_levels}".format(pw=cs.ap_current_tx_power_level, pw_levels=cs.ap_num_power_levels)

                    # Up station
                    subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card", lfresource, "--port_name", lfstation,
                                    "--set_ifstate", "up"])
                    # subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card", lfresource, "--port_name", lfstation,
                    #             "--cmd", "reset","--amt_resets","2","--min_sleep","10","--max_sleep","10"])
                    # sleep(12)

                    i = 0
                    wait_ip_print = False
                    wait_assoc_print = False

                    # Temporary Work around
                    # disable the AP for 6g and enable
                    # if args.ap_admin_down_up_6g is True and (args.band == '6g' or args.band == 'dual_band_6g'):
                    # TODO this is needed after an upgrade
                    cs.ap_name_shutdown()
                    sleep(5)
                    cs.ap_name_no_shutdown()

                    # Wait untill LANforge station connects
                    while True:
                        port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card", lfresource, "--port_name", lfstation,
                                                     "--show_port", "AP,IP,Mode,NSS,Bandwidth,Channel,Signal,Noise,Status,RX-Rate"], capture_output=True, check=True)
                        pss = port_stats.stdout.decode('utf-8', 'ignore')

                        _status = None
                        _ip = None

                        for line in pss.splitlines():
                            m = re.search('Status:\\s+(.*)', line)
                            if (m is not None):
                                _status = m.group(1)
                            m = re.search('IP:\\s+(.*)', line)
                            if (m is not None):
                                _ip = m.group(1)

                        if (i % 3) == 0:
                            logg.info("IP %s  Status %s" % (_ip, _status))

                        if (_status == "Authorized"):
                            if ((_ip is not None) and (_ip != "0.0.0.0")):
                                logg.info("Station is associated with IP address.")
                                break
                            else:
                                if (not wait_ip_print):
                                    logg.info("Waiting for station to get IP Address.")
                                    wait_ip_print = True
                        else:
                            if (not wait_assoc_print):
                                logg.info("Waiting up to 180s for station to associate.")
                                wait_assoc_print = True

                        i += 1
                        # We wait a fairly long time since AP will take a long time to start on a CAC channel.
                        if (i > int(args.wait_time)):
                            err = "ERROR:  Station did not connect within 180 seconds."
                            logg.info(err)
                            e_tot += err
                            e_tot += "  "

                            if (args.wait_forever):
                                logg.info("Will continue waiting, you may wish to debug the system...")
                                i = 0
                            else:
                                break

                        time.sleep(1)

                    if args.series == "9800":
                        # being explicite as
                        if args.band == 'dual_band_6g':
                            pss = cs.show_ap_dot11_dual_band_6gz_summary()
                            logg.info(pss)
                            pss = cs.show_ap_bssid_dual_band_6ghz()
                            logg.info(pss)
                        elif args.band == 'dual_band_5g':
                            pss = cs.show_ap_dot11_dual_band_5gz_summary()
                            logg.info(pss)
                            pss = cs.show_ap_bssid_dual_band_5ghz()
                            logg.info(pss)
                        elif args.band == '6g':
                            pss = cs.show_ap_dot11_6gz_summary()
                            logg.info(pss)
                            pss = cs.show_ap_bssid_6ghz()
                            logg.info(pss)
                        elif args.band == '5g':
                            pss = cs.show_ap_dot11_5gz_summary()
                            logg.info(pss)
                            pss = cs.show_ap_bssid_5ghz()
                            logg.info(pss)
                        elif args.band == '24g':
                            pss = cs.show_ap_dot11_24gz_summary()
                            logg.info(pss)
                            pss = cs.show_ap_bssid_24ghz()
                            logg.info(pss)

                    # Start traffic
                    # subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "do_cmd",
                    #                 "--cmd", "set_cx_state all c-udp-power RUNNING"], capture_output=True, check=False)
                    #
                    logg.info("Start Running traffic cx")

                    command = ["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "do_cmd",
                               "--cmd", "set_cx_state all c-udp-power RUNNING"]

                    logg.info("command: {command}".format(command=command))

                    summary_output = ''
                    summary = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    for line in iter(summary.stdout.readline, ''):
                        logger.debug(line)
                        summary_output += line
                    summary.wait()
                    logger.info(summary_output)

                    # Wait configured number of seconds more seconds
                    logg.info("Waiting {} seconds to let traffic run for a bit, Channel {} NSS {} BW {} TX-Power {}".format(args.duration, ch, n, bw, tx))
                    time.sleep(int(args.duration))

                    # gather information from ap
                    if(bool(ap_dict)):
                        logg.info("ap_dict {}".format(ap_dict))
                        logg.info("Read AP ap_scheme: {} ap_ip: {} ap_port: {} ap_user: {} ap_pw: {}".format(ap_dict['ap_scheme'], ap_dict['ap_ip'], ap_dict["ap_port"],
                                                                                                             ap_dict['ap_user'], ap_dict['ap_pw']))
                        logg.info("####################################################################################################")
                        logg.info("# READ AP POWERREG")
                        logg.info("####################################################################################################")
                        summary_output = ''
                        try:
                            logg.info("ap_ctl.py: read AP power information")
                            # TODO use ap module
                            command = ["./ap_ctl.py", "--scheme", ap_dict['ap_scheme'], "--prompt", ap_dict['ap_prompt'], "--dest", ap_dict['ap_ip'], "--port", ap_dict["ap_port"],
                                                      "--user", ap_dict['ap_user'], "--passwd", ap_dict['ap_pw'], "--action", "powerreg"]
                            summary = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                            for line in iter(summary.stdout.readline, ''):
                                logger.info(line)
                                if len(line) > 4:
                                    summary_output += line
                            summary.wait()
                            logger.info(summary_output)  # .decode('utf-8', 'ignore'))

                        except subprocess.CalledProcessError as process_error:
                            logg.info("####################################################################################################")
                            logg.info("# CHECK IF AP HAS TELNET CONNECTION ALREADY ACTIVE")
                            logg.info("####################################################################################################")
                            logg.info("####################################################################################################")
                            logg.info(
                                "# Unable to commicate to AP error code: {} output {}".format(
                                    process_error.returncode, process_error.output))
                            logg.info("####################################################################################################")
                            summary = "empty_process_error"
                            summary_output = summary

                        ap_ant_gain = ''
                        ap_legal_ant_gain = ''
                        ap_total_power = ''
                        ap_total_power_found = False
                        ap_per_path_power = ''
                        ap_per_path_power_found = False
                        summary_output_split = summary_output.splitlines()
                        print(summary_output_split)
                        for line in summary_output.splitlines():
                            if 'Configured Antenna Gain(dBi):' in line:
                                pat = "Configured Antenna Gain\\(dBi\\)\\:\\s+(\\d+)"
                                match = re.search(pat, line)
                                if match is not None:
                                    ap_ant_gain = match.group(1)
                                    logger.info("AP antenna gain: {gain}".format(gain=ap_ant_gain))
                            if 'Legal Antenna Gain in use(dBi):' in line:
                                pat = "Legal Antenna Gain in use\\(dBi\\):\\s+(\\S+)"
                                match = re.search(pat, line)
                                if match is not None:
                                    ap_legal_ant_gain = match.group(1)
                                    logger.info("AP Legal antenna gain: {gain}".format(gain=ap_legal_ant_gain))
                            # /Allowed total powers\S+\Sn(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)
                            if "INFO" not in line and "Allowed total powers(dBm):" in line:
                                ap_total_power_found = True
                                continue
                            if ap_total_power_found is True:
                                ap_total_power_found = False
                                if args.band == '6g' or args.band == 'dual_band_6g':
                                    if bw == '20':
                                        pat = "(\\d+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)"
                                    elif bw == '40':
                                        pat = "(\\d+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)"
                                    else:
                                        pat = "(\\d+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)"
                                else:
                                    pat = "(\\d+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)"

                                match = re.search(pat, line)
                                if match is not None:
                                    ap_total_power = match.group(int(tx))

                            # /Allowed per-path powers\S+\Sn(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)/gm
                            if "INFO" not in line and "Allowed per-path powers(dBm):" in line:
                                ap_per_path_power_found = True
                                continue
                            if ap_per_path_power_found is True:
                                ap_per_path_power_found = False
                                if args.band == '6g' or args.band == 'dual_band_6g':
                                    if bw == '20':
                                        # pat = "Allowed per-path powers\\S+\\Sn(\\d+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)"
                                        pat = "(\\d+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)"
                                    elif bw == '40':
                                        # pat = "Allowed per-path powers\\S+\\Sn(\\d+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)"
                                        pat = "(\\d+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)"
                                    else:
                                        # pat = "Allowed per-path powers\\S+\\Sn(\\d+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)"
                                        pat = "(\\d+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)"
                                else:
                                    pat = "(\\d+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)"

                                match = re.search(pat, line)
                                if match is not None:
                                    ap_per_path_power = match.group(int(tx))

                        logg.info("ap_ant_gain: {ap_ant_gain}".format(ap_ant_gain=ap_ant_gain))
                        logg.info("ap_legal_ant_gain: {ap_legal_ant_gain}".format(ap_legal_ant_gain=ap_legal_ant_gain))
                        logg.info("ap_total_power: {ap_total_power}".format(ap_total_power=ap_total_power))
                        logg.info("ap_per_path_power: {ap_per_path_power}".format(ap_per_path_power=ap_per_path_power))

                    # Gather probe results and record data, verify NSS, BW, Channel
                    # note the probe will get the information from this command
                    # iw dev sta0000 station dump
                    i = 0
                    beacon_sig = None
                    sig = None
                    pf = 1
                    ants = []
                    while True:
                        time.sleep(1)
                        port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card", lfresource, "--port_name", lfstation,
                                                     "--cli_cmd", "probe_port 1 %s %s" % (lfresource, lfstation)], capture_output=True, check=True)
                        pss = port_stats.stdout.decode('utf-8', 'ignore')
                        # for debug: print the output of lf_portmod.pl and the command used
                        logg.debug("######## lf_portmod ######### ")
                        logg.debug(pss)
                        logg.debug("######## lf_portmod  END ######### ")

                        if (args.show_lf_portmod):
                            logg.info("./lf_portmod.pl --manager {} --card {} --port_name {} --cli_cmd probe_port 1 {} {}".format(lfmgr,
                                                                                                                                  lfresource, lfstation, lfresource, lfstation))
                            logg.info(pss)

                        foundit = False
                        for line in pss.splitlines():
                            # logg.info("probe-line: %s"%(line))
                            # TODO switch to signal avg
                            m = re.search('signal avg:\\s+(\\S+)\\s+\\[(.*)\\]\\s+dBm', line)
                            # m = re.search('signal:\\s+(\\S+)\\s+\\[(.*)\\]\\s+dBm', line)
                            # print("m singal avg : {}".format(m))
                            # AX210 needs to look at signal
                            if (m is None):
                                m = re.search('signal:\\s+(\\S+)\\s+\\[(.*)\\]\\s+dBm', line)
                                # print("m signal: {}".format(m))
                            if (m is not None):
                                logg.info("search: signal: resulted in m = {}".format(m))
                                sig = m.group(1)
                                ants = m.group(2).split()
                                q = 0
                                for a in ants:
                                    ants[q] = ants[q].replace(",", "", 1)
                                    q += 1

                                logg.info("sig: %s  ants: %s ants-len: %s n: %s" % (sig, m.group(2), len(ants), n))

                                if (len(ants) == int(n)):
                                    foundit = True
                                else:
                                    logg.info("Looking for %s spatial streams, signal avg reported fewer: %s" % (n, m.group(1)))
                            m = re.search('beacon signal avg:\\s+(\\S+)\\s+dBm', line)
                            if (m is not None):
                                logg.info("search: beacon signal avg: resulted in m = {}".format(m))
                                beacon_sig = m.group(1)
                                logg.info("beacon_sig: %s " % (beacon_sig))

                        if (foundit):
                            break

                        i += 1
                        if (i > 10):
                            err = "Tried and failed 10 times to find all probe values, continuing."
                            logg.info(err)
                            e_tot += err
                            e_tot += "  "
                            while (len(ants) < int(n)):
                                ants.append("")
                            break

                    endp_stats = subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--endp_vals", "rx_bps",
                                                 "--cx_name", "c-udp-power"], capture_output=True, check=True)

                    pss = endp_stats.stdout.decode('utf-8', 'ignore')
                    logg.info(pss)

                    for line in pss.splitlines():
                        # logg.info("probe-line: %s"%(line))From Lanforge probe, command
                        # ./lf_portmod.pl with cli parameter probe_port 1 (about line 1150)
                        m = re.search('Rx Bytes:\\s+(\\d+)', line)
                        if (m is not None):
                            logg.info("Rx Bytes: result {}".format(m))
                            rx_bytes = int(m.group(1))
                            if (rx_bytes == 0):
                                err = "ERROR:  No bytes received by data connection, test results may not be valid."
                                e_tot += err
                                e_tot += "  "

                    # Stop traffic
                    # subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "do_cmd",
                    #                "--cmd", "set_cx_state all c-udp-power STOPPED"], capture_output=True, check=True)

                    command = ["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "do_cmd",
                               "--cmd", "set_cx_state all c-udp-power STOPPED"]

                    logg.info("command: {command}".format(command=command))

                    summary_output = ''
                    summary = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    for line in iter(summary.stdout.readline, ''):
                        logger.debug(line)
                        summary_output += line
                    summary.wait()
                    logger.info(summary_output)

                    antstr = ""
                    for x in range(4):
                        if (x < int(n)):
                            logg.info("x: %s n: %s  len(ants): %s" % (x, n, len(ants)))
                            antstr += ants[x]
                        else:
                            antstr += " "
                        antstr += "\t"

                    logg.info("antenna dBm {antstr}".format(antstr=antstr))
                    port_stats = subprocess.run(["./lf_portmod.pl", "--manager", lfmgr, "--card", lfresource, "--port_name", lfstation,
                                                 "--show_port", "AP,IP,Mode,NSS,Bandwidth,Channel,Signal,Noise,Status,RX-Rate"], capture_output=True, check=True)
                    pss = port_stats.stdout.decode('utf-8', 'ignore')
                    logg.info(pss)

                    _ap = None
                    _bw = None
                    _ch = None
                    _mode = None
                    _nss = None
                    _noise = None
                    _rxrate = None
                    _noise_bare = None

                    for line in pss.splitlines():
                        m = re.search('AP:\\s+(.*)', line)
                        if (m is not None):
                            _ap = m.group(1)
                            logg.info("AP: {}".format(m))
                        m = re.search('Bandwidth:\\s+(.*)Mhz', line)
                        if (m is not None):
                            _bw = m.group(1)
                            logg.info("Bandwidth: {}".format(m))
                        m = re.search('Channel:\\s+(.*)', line)
                        if (m is not None):
                            _ch = m.group(1)
                            logg.info("Channel: {}".format(m))
                        m = re.search('Mode:\\s+(.*)', line)
                        if (m is not None):
                            _mode = m.group(1)
                            logg.info("Mode: {}".format(m))
                        m = re.search('NSS:\\s+(.*)', line)
                        if (m is not None):
                            _nss = m.group(1)
                            logg.info("NSS: {}".format(m))
                        m = re.search('Noise:\\s+(.*)', line)
                        if (m is not None):
                            _noise = m.group(1)
                            logg.info("Noise: {}".format(m))
                        m = re.search('Noise:\\s+(.*)dBm', line)
                        if (m is not None):
                            _noise_bare = m.group(1)
                            logg.info("Noise Bare: {}".format(m))
                        m = re.search('RX-Rate:\\s+(.*)', line)
                        if (m is not None):
                            _rxrate = m.group(1)
                            logg.info("RX-Rate: {}".format(m))

                    # ath10k radios now take noise-floor into account, so adjust_nf
                    # should remain set to false when using those radios.  Possibly other
                    # radios would need this, so leave code in place.
                    rssi_adj = 0
                    if (args.adjust_nf and _noise_bare is not None):
                        _noise_i = int(_noise_bare)
                        if (_noise_i == 0):
                            # Guess we could not detect noise properly?
                            e_tot += "WARNING:  Invalid noise-floor, calculations may be inaccurate.  "
                            pf = 0
                        else:
                            rssi_adj = (_noise_i - nf_at_calibration)

                    if (sig is None):
                        e_tot += "ERROR:  Could not detect signal level.  "
                        sig = -100
                        pf = 0

                    if (beacon_sig is None):
                        e_tot += "ERROR:  Could not detect beacon signal level.  "
                        beacon_sig = -100
                        pf = 0

                    pi = int(pathloss)
                    ag = int(antenna_gain)
                    calc_dbm_beacon = int(beacon_sig) + pi + rssi_adj + ag
                    logg.info("calc_dbm_beacon {}".format(calc_dbm_beacon))

                    logg.info("sig: %s" % sig)
                    calc_dbm = int(sig) + pi + rssi_adj + ag
                    logg.info("calc_dbm %s" % (calc_dbm))

                    # Calculated per-antenna power is what we calculate the AP transmitted
                    # at (rssi + pathloss + antenna_gain ). Spatial stream rssi is -36 , with pathloss of 44 ,
                    # with antenna gain of 6
                    #  -36 + 44 - 6
                    # then we calculate AP transmitted at +2
                    calc_ant1 = 0
                    if (ants[0] != ""):
                        calc_ant1 = int(ants[0]) + pi + rssi_adj + ag
                        logg.info("calc_ant1: {} = ants[0]: {} + pi: {} + rssi_adj: {} + ag: {}".format(calc_ant1, ants[0], pi, rssi_adj, ag))
                    calc_ant2 = 0
                    calc_ant3 = 0
                    calc_ant4 = 0
                    if (len(ants) > 1 and ants[1] != ""):
                        calc_ant2 = int(ants[1]) + pi + rssi_adj + ag
                        logg.info("calc_ant2: {} = ants[1]: {} + pi: {} + rssi_adj: {} + ag: {}".format(calc_ant2, ants[1], pi, rssi_adj, ag))

                    if (len(ants) > 2 and ants[2] != ""):
                        calc_ant3 = int(ants[2]) + pi + rssi_adj + ag
                        logg.info("calc_ant3: {} = ants[2]: {} + pi: {} + rssi_adj: {} + ag: {}".format(calc_ant3, ants[2], pi, rssi_adj, ag))

                    if (len(ants) > 3 and ants[3] != ""):
                        calc_ant4 = int(ants[3]) + pi + rssi_adj + ag
                        logg.info("calc_ant4: {} = ants[3]: {} + pi: {} + rssi_adj: {} + ag: {}".format(calc_ant4, ants[3], pi, rssi_adj, ag))

                    diff_a1 = ""
                    diff_a2 = ""
                    diff_a3 = ""
                    diff_a4 = ""

                    pfs = "PASS"
                    pfrange = pf_dbm

                    if (cc_dbm == ""):
                        cc_dbmi = 0
                    else:
                        cc_dbmi = int(cc_dbm)
                    diff_dbm = calc_dbm - cc_dbmi
                    if(int(abs(diff_dbm)) > pfrange):
                        w_tot = "Info: Controller dBm and Calculated dBm power different by greater than +/- {} dBm".format(
                            args.pf_dbm)  # pass / fail dbm

                    logg.info("diff_dbm {} calc_dbm {} - cc_dbmi {}".format(diff_dbm, calc_dbm, cc_dbmi))
                    diff_dbm_beacon = calc_dbm_beacon - cc_dbmi
                    logg.info("diff_dbm_beacon {} calc_dbm_beacon {} - cc_dbmi {}".format(diff_dbm_beacon, calc_dbm_beacon, cc_dbmi))

                    if(int(abs(diff_dbm_beacon)) > int(args.beacon_dbm_diff)):
                        w_tot = "INFO: Controller dBm and Calculated dBm Beacon power different by greater than +/- {} dBm".format(
                            args.beacon_dbm_diff)

                    # Allowed per path is what we expect the AP should be transmitting at.
                    # calc_ant1 is what we calculated it actually transmitted at based on rssi
                    # pathloss and antenna gain.  Allowed per-path is modified taking into account that multi
                    # NSS tranmission will mean that each chain should be decreased so that sum total
                    # of all chains is equal to the maximum allowed txpower.
                    allowed_per_path = cc_dbmi
                    logg.info("combined_power read from Controller: {}  = cc_dbmi: {}".format(allowed_per_path, cc_dbmi))
                    if (int(_nss) == 1):

                        if args.nss_4x4_override:
                            allowed_per_path = cc_dbmi - 6
                            logg.info("allowed_per_path: {}  = cc_dbmi: {} - 6 nss_4x4_override True".format(allowed_per_path, cc_dbmi))
                            logg.info("(Offset 1) diff_a1 (): {} = calc_ant1: {} - allowed_per_path: {} nss_4x4_override True".format(diff_a1, calc_ant1, allowed_per_path))
                        diff_a1 = calc_ant1 - cc_dbmi
                        logg.info("(Offset 1) diff_a1 (): {} = calc_ant1: {} - allowed_per_path: {}".format(diff_a1, calc_ant1, allowed_per_path))

                        # if args.per_ss:
                        if (abs(diff_a1) > pfrange):
                            pf = 0
                    if (int(_nss) == 2):
                        # NSS of 2 means each chain should transmit at 1/2 total power, thus the '- 3'
                        if args.nss_4x4_override:
                            allowed_per_path = cc_dbmi - 6
                            logg.info("allowed_per_path: {}  = cc_dbmi: {} - 6 nss_4x4_override True".format(allowed_per_path, cc_dbmi))
                        else:
                            allowed_per_path = cc_dbmi - 3
                            logg.info("allowed_per_path: {}  = cc_dbmi: {} - 3".format(allowed_per_path, cc_dbmi))

                        diff_a1 = calc_ant1 - allowed_per_path
                        logg.info("(Offset 1) diff_a1: {} = calc_ant1: {} - allowed_per_path: {}".format(diff_a1, calc_ant1, allowed_per_path))

                        diff_a2 = calc_ant2 - allowed_per_path
                        logg.info("(Offset 2) diff_a2: {} = calc_ant2: {} - allowed_per_path: {}".format(diff_a2, calc_ant2, allowed_per_path))
                        # if args.per_ss:
                        if ((abs(diff_a1) > pfrange) or (abs(diff_a2) > pfrange)):
                            pf = 0
                    if (int(_nss) == 3):
                        # NSS of 3 means each chain should transmit at 1/3 total power, thus the '- 5'
                        allowed_per_path = cc_dbmi - 5
                        logg.info("allowed_per_path: {}  = cc_dbmi: {} - 5".format(allowed_per_path, cc_dbmi))

                        diff_a1 = calc_ant1 - allowed_per_path
                        logg.info("(Offset 1) diff_a1: {} = calc_ant1: {} - allowed_per_path: {}".format(diff_a1, calc_ant1, allowed_per_path))

                        diff_a2 = calc_ant2 - allowed_per_path
                        logg.info("(Offset 2) diff_a2: {} = calc_ant2: {} - allowed_per_path: {}".format(diff_a2, calc_ant2, allowed_per_path))

                        diff_a3 = calc_ant3 - allowed_per_path
                        logg.info("(Offset 3) diff_a3: {} = calc_ant3: {} - allowed_per_path: {}".format(diff_a3, calc_ant3, allowed_per_path))

                        # if args.per_ss:
                        if ((abs(diff_a1) > pfrange) or
                            (abs(diff_a2) > pfrange) or
                                (abs(diff_a3) > pfrange)):
                            pf = 0
                    if (int(_nss) == 4):
                        # NSS of 4 means each chain should transmit at 1/4 total power, thus the '- 6'
                        allowed_per_path = cc_dbmi - 6
                        logg.info("allowed_per_path: {}  = cc_dbmi: {} - 6".format(allowed_per_path, cc_dbmi))

                        diff_a1 = calc_ant1 - allowed_per_path
                        logg.info("(Offset 1) diff_a1: {} = calc_ant1: {} - allowed_per_path: {}".format(diff_a1, calc_ant1, allowed_per_path))

                        diff_a2 = calc_ant2 - allowed_per_path
                        logg.info("(Offset 2) diff_a2: {} = calc_ant2: {} - allowed_per_path: {}".format(diff_a2, calc_ant2, allowed_per_path))

                        diff_a3 = calc_ant3 - allowed_per_path
                        logg.info("(Offset 3) diff_a3: {} = calc_ant3: {} - allowed_per_path: {}".format(diff_a3, calc_ant3, allowed_per_path))

                        diff_a4 = calc_ant4 - allowed_per_path
                        logg.info("(Offset 4) diff_a4: {} = calc_ant4: {} - allowed_per_path: {}".format(diff_a4, calc_ant4, allowed_per_path))

                        # Read AP to determine if there are less chains or spatial steams then expected
                        # Thus provide a passing result
                        failed_low = 0
                        # least = 0
                        if (abs(diff_a1) > pfrange):
                            failed_low += 1
                            # least = diff_a1 #leave in code if want to move to least
                        if (abs(diff_a2) > pfrange):
                            failed_low += 1
                            # least = min(least, diff_a2)
                        if (abs(diff_a3) > pfrange):
                            failed_low += 1
                            # least = min(least, diff_a3)
                        if (abs(diff_a4) > pfrange):
                            failed_low += 1
                            # least = min(least, diff_a4)

                        failed_low_threshold = 0
                        #
                        #
                        # If the ap dictionary is set the read the AP to see the number
                        # of spatial streams used.  For tx power 1 the AP may determine to use
                        # fewer spatial streams
                        #
                        #
                        P1 = None
                        T1 = None
                        P2 = None
                        T2 = None
                        P3 = None
                        T3 = None
                        P4 = None
                        T4 = None
                        N_ANT = None
                        DAA_Pwr = None
                        DAA_N_TX = None
                        DAA_Total_pwr = None
                        if(bool(ap_dict) and args.nss_4x4_ap_adjust):
                            logg.info("ap_dict {}".format(ap_dict))
                            logg.info("Read AP ap_scheme: {} ap_ip: {} ap_port: {} ap_user: {} ap_pw: {}".format(ap_dict['ap_scheme'], ap_dict['ap_ip'], ap_dict["ap_port"],
                                                                                                                 ap_dict['ap_user'], ap_dict['ap_pw']))
                            logg.info("####################################################################################################")
                            logg.info("# READ AP POWERCFG")
                            logg.info("####################################################################################################")

                            try:
                                logg.info("ap_ctl.py: read AP power information")
                                # TODO use ap module
                                summary_output = ''
                                command = ["./ap_ctl.py", "--scheme", ap_dict['ap_scheme'], "--prompt", ap_dict['ap_prompt'], "--dest", ap_dict['ap_ip'], "--port", ap_dict["ap_port"],
                                                          "--user", ap_dict['ap_user'], "--passwd", ap_dict['ap_pw'], "--action", "powercfg"]
                                summary = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                                for line in iter(summary.stdout.readline, ''):
                                    logger.debug(line)
                                    if line:
                                        summary_output += line
                                    # sys.stdout.flush() # please see comments regarding the necessity of this line
                                summary.wait()
                                logger.info(summary_output)  # .decode('utf-8', 'ignore'))
#
                                # ap_info = subprocess.run(["./ap_ctl.py", "--scheme", ap_dict['ap_scheme'], "--prompt", ap_dict['ap_prompt'], "--dest", ap_dict['ap_ip'], "--port", ap_dict["ap_port"],
                                #                          "--user", ap_dict['ap_user'], "--passwd", ap_dict['ap_pw'], "--action", "powercfg"], stdout=subprocess.PIPE)
                                # try:
                                #     pss = ap_info.stdout.decode('utf-8', 'ignore')
                                #     logg.info(pss)
                                # except BaseException:
                                #     logg.info("ap_info was of type NoneType will set pss empty")
                                #     pss = "empty"

                            # TODO print out the call stack
                            except subprocess.CalledProcessError as process_error:
                                logg.info("####################################################################################################")
                                logg.info("# CHECK IF AP HAS TELNET CONNECTION ALREADY ACTIVE")
                                logg.info("####################################################################################################")

                                logg.info("####################################################################################################")
                                logg.info(
                                    "# Unable to commicate to AP error code: {} output {}".format(
                                        process_error.returncode, process_error.output))
                                logg.info("####################################################################################################")
                                summary = "empty_process_error"

                            logg.info(summary_output)
                            for line in summary_output.splitlines():
                                logg.info("ap {}".format(line))
                                pat = '^\\s+1\\s+6\\s+\\S+\\s+\\S+\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)'
                                m = re.search(pat, line)
                                if (m is not None):
                                    P1 = m.group(1)
                                    T1 = m.group(2)
                                    P2 = m.group(3)
                                    T2 = m.group(4)
                                    P3 = m.group(5)
                                    T3 = m.group(6)
                                    P4 = m.group(7)
                                    T4 = m.group(8)
                                    N_ANT = m.group(9)
                                    DAA_Pwr = m.group(10)
                                    DAA_N_TX = m.group(11)  # number of spatial streams
                                    DAA_Total_pwr = m.group(12)
                                    # adjust the fail criterial based on the number of spatial streams
                                    if DAA_N_TX == "4":
                                        failed_low_threshold = 0
                                        logg.info("4 failed_low_threshold {}".format(failed_low_threshold))
                                    if DAA_N_TX == "3":
                                        failed_low_threshold = 1
                                        logg.info("3 failed_low_threshold {}".format(failed_low_threshold))
                                    if DAA_N_TX == "2":
                                        failed_low_threshold = 2
                                        logg.info("2 failed_low_threshold {}".format(failed_low_threshold))
                                    if DAA_N_TX == "1":
                                        failed_low_threshold = 3
                                        logg.info("1 failed_low_threshold {}".format(failed_low_threshold))

                                    i_tot = "P1: {} T1: {} P2: {} T2: {} P3: {} T3: {} P4: {} T4: {} N_ANT: {} DAA_Pwr: {} DAA_N_TX: {} DAA_Total_pwr: {}  ".format(
                                        P1, T1, P2, T2, P3, T3, P4, T4, N_ANT, DAA_Pwr, DAA_N_TX, DAA_Total_pwr)
                                    print(i_tot)
                                    logg.info(i_tot)
                                else:
                                    logg.info("AP Check using regular expressions")

                        #
                        #  The controller may adjust the number of spatial streams to allow for the
                        #  best power values
                        #
                        # for 4 spatial streams if the AP is read and the failed threshold is met then there is a failure
                        # the failure will be caugh below if the range is not correct.
                        # range check and reading the data from the AP may be used in conjunction thus it is coded to be non-exclusive
                        logg.info("failed_low: {} failed_low_threshold: {}".format(failed_low, failed_low_threshold))
                        if bool(ap_dict) and failed_low > failed_low_threshold:
                            logg.info("failed_low: {} > failed_low_threshold: {}".format(failed_low, failed_low_threshold))
                            pf = 0

                        # this allows for a larger offset for specific spatial streams
                        if(pf_ignore_offset != 0):
                            logg.info(
                                "diff_a1: {} diff_a2: {} diff_a3: {} diff_a4: {} pfrange: {} pf_ignore_offset: {}".format(
                                    diff_a1, diff_a2, diff_a3, diff_a4, pfrange, pf_ignore_offset))
                            if (abs(diff_a1) > pfrange):
                                if(abs(diff_a1) < (pfrange + pf_ignore_offset)):
                                    logg.info("abs(diff_a1): {} > (pfrange: {} + pf_ignore_offset: {})".format(abs(diff_a1), pfrange, pf_ignore_offset))
                                    i_tot += "PASSED abs(diff_a1)({}) > pfrange({}) + pf_ignore_offset({})  ".format(abs(diff_a1), pfrange, pf_ignore_offset)
                                    logg.info("i_tot {}".format(i_tot))
                                else:
                                    logg.info("abs(diff_a1): {} failure".format(abs(diff_a1)))
                                    pf = 0
                            if (abs(diff_a2) > pfrange):
                                if(abs(diff_a2) < (pfrange + pf_ignore_offset)):
                                    logg.info("abs(diff_a2): {} > pfrange: {} + pf_ignore_offset: {}".format(abs(diff_a2), pfrange, pf_ignore_offset))
                                    i_tot += "PASSED abs(diff_a2)({}) > pfrange({}) + pf_ignore_offset({})  ".format(abs(diff_a2), pfrange, pf_ignore_offset)
                                    logg.info("i_tot {}".format(i_tot))
                                else:
                                    logg.info("abs(diff_a2): {} failure".format(abs(diff_a2)))
                                    pf = 0
                            if (abs(diff_a3) > pfrange):
                                if(abs(diff_a3) < (pfrange + pf_ignore_offset)):
                                    logg.info("abs(diff_a3): {} > pfrange: {} + pf_ignore_offset: {}".format(abs(diff_a3), pfrange, pf_ignore_offset))
                                    i_tot += "PASSED abs(diff_a3)({}) > pfrange({}) + pf_ignore_offset({})  ".format(abs(diff_a3), pfrange, pf_ignore_offset)
                                    logg.info("i_tot {}".format(i_tot))
                                else:
                                    logg.info("abs(diff_a3): {} failure".format(abs(diff_a3)))
                                    pf = 0
                            if (abs(diff_a4) > pfrange):
                                if(abs(diff_a4) < (pfrange + pf_ignore_offset)):
                                    logg.info("abs(diff_a4): {} > pfrange: {} + pf_ignore_offset: {}".format(abs(diff_a4), pfrange, pf_ignore_offset))
                                    i_tot += "PASSED abs(diff_a4)({}) > pfrange({}) + pf_ignore_offset({})  ".format(abs(diff_a4), pfrange, pf_ignore_offset)
                                    logg.info("i_tot {}".format(i_tot))
                                else:
                                    logg.info("abs(diff_a4): {} failure".format(abs(diff_a4)))
                                    pf = 0
                        # Did not read AP , did not have a adjusted offset
                        # use straight absolute value greater then the expected threshold
                        if failed_low_threshold == 0:
                            if (abs(diff_a1) > pfrange):
                                logg.info("abs(diff_a1): {} > (pfrange: {})".format(abs(diff_a1), pfrange))
                                pf = 0
                            if (abs(diff_a2) > pfrange):
                                logg.info("abs(diff_a2): {} > (pfrange: {})".format(abs(diff_a2), pfrange))
                                pf = 0
                            if (abs(diff_a3) > pfrange):
                                logg.info("abs(diff_a3): {} > (pfrange: {})".format(abs(diff_a3), pfrange))
                                pf = 0
                            if (abs(diff_a4) > pfrange):
                                logg.info("abs(diff_a4): {} > (pfrange: {})".format(abs(diff_a4), pfrange))
                                pf = 0

                    logg.info("_nss {}  allowed_per_path (AP should be transmitting at) {}".format(_nss, allowed_per_path))

                    if (pf == 0 or e_tot != ""):
                        pfs = "FAIL"
                    run_end_time = datetime.datetime.now()
                    run_end_time_str = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")).replace(':', '-')
                    logger.info("run_end_time : {run_end_time}".format(run_end_time=run_end_time_str))

                    run_time_delta = run_end_time - run_start_time
                    minutes, seconds = divmod(run_time_delta.seconds, 60)
                    hours, minutes = divmod(minutes, 60)
                    run_duration = "{day}d {hours}h {minutes}m {seconds}s {msec} ms".format(
                        day=run_time_delta.days, hours=hours, minutes=minutes, seconds=seconds, msec=run_time_delta.microseconds)
                    logger.info("Run Duration:  {run_duration}".format(run_duration=run_duration))

                    total_run_duration += run_time_delta
                    minutes, seconds = divmod(total_run_duration.seconds, 60)
                    hours, minutes = divmod(minutes, 60)
                    total_run_duration_str = "{day}d {hours}h {minutes}m {seconds}s {msec} ms".format(
                        day=total_run_duration.days, hours=hours, minutes=minutes, seconds=seconds, msec=total_run_duration.microseconds)
                    logger.info("Total Run Duration:  {total_run_duration}".format(total_run_duration=total_run_duration))

                    run_start_time = run_end_time

                    time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "{:.3f}".format(time.time() - (math.floor(time.time())))[1:]

                    # This line writes the data to the CSV
                    ln = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
                        mycc, myrd, pathloss, antenna_gain, ch, n, bw, tx, beacon_sig, sig,
                        antstr, _ap, _bw, _ch, _mode, _nss, _noise, _rxrate,
                        cc_mac, cc_ch, cc_power, cc_dbm,
                        calc_dbm, diff_dbm, calc_ant1, calc_ant2, calc_ant3, calc_ant4,
                        diff_a1, diff_a2, diff_a3, diff_a4, pfs, time_stamp, run_duration, total_run_duration_str
                    )

                    # logg.info("RESULT: %s"%(ln))
                    csv.write(ln)
                    csv.write("\t")

                    # TODO recorde the kpi.csv
                    # Controller dBm
                    # worksheet.write(row, col, cc_dbmi, center_blue)
                    results_dict = kpi_csv.kpi_csv_get_dict_update_time()
                    results_dict['Graph-Group'] = "Tx Power {ap} {band} {channel}".format(ap=args.ap, band=args.band, channel=cc_ch)
                    results_dict['pass/fail'] = pfs
                    # TODO kpi pass fail
                    # results_dict['Subtest-Pass'] = None
                    # results_dict['Subtest-Fail'] = None
                    results_dict['short-description'] = "CC dBm {ap} {band} {channel} {nss} {bw} {mode} {txpower}".format(
                        ap=args.ap, band=args.band, channel=_ch, nss=_nss, bw=_bw, mode=_mode, txpower=cc_power)
                    results_dict['numeric-score'] = "{cc_dbmi}".format(cc_dbmi=cc_dbmi)
                    results_dict['Units'] = "dBm"
                    kpi_csv.kpi_csv_write_dict(results_dict)

                    # Calculated beacon dBm
                    # worksheet.write(row, col, calc_dbm_beacon, center_blue)
                    results_dict = kpi_csv.kpi_csv_get_dict_update_time()
                    results_dict['Graph-Group'] = "Tx Power {ap} {band} {channel}".format(ap=args.ap, band=args.band, channel=cc_ch)
                    results_dict['pass/fail'] = pfs
                    # TODO kpi pass fail
                    # results_dict['Subtest-Pass'] = None
                    # results_dict['Subtest-Fail'] = None
                    results_dict['short-description'] = "Calc dBm Beacon {ap} {band} ch:{channel} nss:{nss} bw:{bw} {mode} tx:{txpower}".format(
                        ap=args.ap, band=args.band, channel=_ch, nss=_nss, bw=_bw, mode=_mode, txpower=cc_power)
                    results_dict['numeric-score'] = "{calc_dbm_beacon}".format(calc_dbm_beacon=calc_dbm_beacon)
                    results_dict['Units'] = "dBm"
                    kpi_csv.kpi_csv_write_dict(results_dict)

                    # Diff Controller dBm & Beacon dBM (+/- 7 dBm)
                    # worksheet.write(row, col, diff_dbm_beacon, center_blue)
                    results_dict = kpi_csv.kpi_csv_get_dict_update_time()
                    results_dict['Graph-Group'] = "Tx Power {ap} {band} {channel}".format(ap=args.ap, band=args.band, channel=cc_ch)
                    results_dict['pass/fail'] = pfs
                    # TODO kpi pass fail
                    # results_dict['Subtest-Pass'] = None
                    # results_dict['Subtest-Fail'] = None
                    results_dict['short-description'] = "Diff CC & Beacon dBm {ap} {band} ch:{channel} nss:{nss} bw:{bw} {mode} tx:{txpower}".format(
                        ap=args.ap, band=args.band, channel=_ch, nss=_nss, bw=_bw, mode=_mode, txpower=cc_power)
                    results_dict['numeric-score'] = "{diff_dbm_beacon}".format(diff_dbm_beacon=diff_dbm_beacon)
                    results_dict['Units'] = "dBm"
                    kpi_csv.kpi_csv_write_dict(results_dict)

                    # Calculated dBm Combined
                    # worksheet.write(row, col, calc_dbm, center_blue)
                    results_dict = kpi_csv.kpi_csv_get_dict_update_time()
                    results_dict['Graph-Group'] = "Tx Power {ap} {band} {channel}".format(ap=args.ap, band=args.band, channel=cc_ch)
                    results_dict['pass/fail'] = pfs
                    # TODO kpi pass fail
                    # results_dict['Subtest-Pass'] = None
                    # results_dict['Subtest-Fail'] = None
                    results_dict['short-description'] = "Calc dBm Combined {ap} {band} ch:{channel} nss:{nss} bw:{bw} {mode} tx:{txpower}".format(
                        ap=args.ap, band=args.band, channel=_ch, nss=_nss, bw=_bw, mode=_mode, txpower=cc_power)
                    results_dict['numeric-score'] = "{calc_dbm}".format(calc_dbm=calc_dbm)
                    results_dict['Units'] = "dBm"
                    kpi_csv.kpi_csv_write_dict(results_dict)

                    # Diff Controller dBm and Combined
                    # worksheet.write(row, col, diff_dbm, center_blue)
                    results_dict = kpi_csv.kpi_csv_get_dict_update_time()
                    results_dict['Graph-Group'] = "Tx Power {ap} {band} {channel}".format(ap=args.ap, band=args.band, channel=cc_ch)
                    results_dict['pass/fail'] = pfs
                    # TODO kpi pass fail
                    # results_dict['Subtest-Pass'] = None
                    # results_dict['Subtest-Fail'] = None
                    results_dict['short-description'] = "Diff CC dBm & Combined {ap} {band} ch:{channel} nss:{nss} bw:{bw} {mode} tx:{txpower}".format(
                        ap=args.ap, band=args.band, channel=_ch, nss=_nss, bw=_bw, mode=_mode, txpower=cc_power)
                    results_dict['numeric-score'] = "{diff_dbm}".format(diff_dbm=diff_dbm)
                    results_dict['Units'] = "dBm"
                    kpi_csv.kpi_csv_write_dict(results_dict)

                    # Start xlsx reporting - report as reported from ap summary
                    ln = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
                        mycc, myrd, pathloss, antenna_gain, _ch, _nss, _bw, cc_power, cc_dbm, allowed_per_path,
                        antstr,
                        calc_ant1, calc_ant2, calc_ant3, calc_ant4,
                        diff_a1, diff_a2, diff_a3, diff_a4, pfs, time_stamp, run_duration, total_run_duration_str
                    )
                    csvs.write(ln)
                    csvs.write("\t")

                    # Save the configurations
                    center_blue_tmp = center_blue
                    center_tan_tmp = center_tan
                    center_peach_tmp = center_peach
                    center_pink_tmp = center_pink
                    center_yel_red_tmp = center_yel_red
                    center_yel_tmp = center_yel

                    # TODO refactor this is a quick fix to allow the fail's to be better indicated
                    if (pfs == "FAIL") or (_bw != bw) or (_nss != n) or (e_tot != "") or (int(cc_dbm) != int(ap_dbm)) or (cc_power != ap_power):
                        center_blue = center_red
                        center_tan = center_red
                        center_peach = center_red
                        center_pink = center_red
                        center_yel_red = center_red
                        center_yel = center_red

                    # Start report line
                    col = 0
                    worksheet.write(row, col, mycc, center_blue)
                    col += 1
                    worksheet.write(row, col, myrd, center_blue)
                    col += 1

                    worksheet.write(row, col, args.series, center_blue)
                    col += 1
                    worksheet.write(row, col, cc_ch, center_blue)
                    col += 1
                    worksheet.write(row, col, _ch, center_blue)
                    col += 1
                    worksheet.write(row, col, _nss, center_blue)
                    col += 1
                    worksheet.write(row, col, cc_bw, center_blue)
                    col += 1
                    worksheet.write(row, col, _bw, center_blue)
                    col += 1
                    worksheet.write(row, col, cc_power, center_tan)
                    col += 1
                    worksheet.write(row, col, ap_power, center_tan)
                    col += 1
                    worksheet.write(row, col, cc_dbm, center_tan)
                    col += 1
                    worksheet.write(row, col, ap_dbm, center_tan)
                    if(bool(ap_dict)):
                        col += 1
                        worksheet.write(row, col, ap_total_power, center_tan)
                    col += 1
                    worksheet.write(row, col, allowed_per_path, center_tan)
                    if(bool(ap_dict)):
                        col += 1
                        worksheet.write(row, col, ap_per_path_power, center_tan)
                    col += 1
                    worksheet.write(row, col, pathloss, center_tan)
                    col += 1
                    worksheet.write(row, col, antenna_gain, center_tan)
                    col += 1
                    worksheet.write(row, col, _noise, center_peach)
                    col += 1
                    worksheet.write(row, col, rssi_adj, center_peach)
                    col += 1
                    if (args.adjust_nf):
                        worksheet.write(row, col, rssi_adj, center_peach)
                        col += 1
                    worksheet.write(row, col, _rxrate, center_peach)
                    col += 1
                    worksheet.write(row, col, beacon_sig, center_peach)
                    col += 1
                    worksheet.write(row, col, sig, center_peach)
                    col += 1
                    for x in range(4):
                        if (x < int(n)):
                            worksheet.write(row, col, ants[x], center_peach)
                            col += 1
                        else:
                            worksheet.write(row, col, " ", center_peach)
                            col += 1
                    worksheet.write(row, col, calc_ant1, center_pink)
                    col += 1
                    worksheet.write(row, col, calc_ant2, center_pink)
                    col += 1
                    worksheet.write(row, col, calc_ant3, center_pink)
                    col += 1
                    worksheet.write(row, col, calc_ant4, center_pink)
                    col += 1
                    if (diff_a1 != "" and abs(diff_a1) > pfrange):
                        worksheet.write(row, col, diff_a1, center_yel_red)
                        col += 1
                    else:
                        worksheet.write(row, col, diff_a1, center_yel)
                        col += 1
                    if (diff_a2 != "" and abs(diff_a2) > pfrange):
                        worksheet.write(row, col, diff_a2, center_yel_red)
                        col += 1
                    else:
                        worksheet.write(row, col, diff_a2, center_yel)
                        col += 1
                    if (diff_a3 != "" and abs(diff_a3) > pfrange):
                        worksheet.write(row, col, diff_a3, center_yel_red)
                        col += 1
                    else:
                        worksheet.write(row, col, diff_a3, center_yel)
                        col += 1
                    if (diff_a4 != "" and abs(diff_a4) > pfrange):
                        worksheet.write(row, col, diff_a4, center_yel_red)
                        col += 1
                    else:
                        worksheet.write(row, col, diff_a4, center_yel)
                        col += 1
                    worksheet.write(row, col, cc_dbmi, center_blue)
                    col += 1
                    worksheet.write(row, col, calc_dbm_beacon, center_blue)
                    col += 1
                    worksheet.write(row, col, diff_dbm_beacon, center_blue)
                    col += 1
                    worksheet.write(row, col, calc_dbm, center_blue)
                    col += 1
                    worksheet.write(row, col, diff_dbm, center_blue)
                    col += 1
                    if (pfs == "FAIL"):
                        worksheet.write(row, col, pfs, red)
                        col += 1
                    else:
                        worksheet.write(row, col, pfs, green)
                        col += 1
                    worksheet.write(row, col, time_stamp, green)
                    col += 1
                    worksheet.write(row, col, run_duration, green)
                    col += 1
                    worksheet.write(row, col, total_run_duration_str, green)
                    col += 1
                    if (int(cc_dbm) != int(ap_dbm)):
                        err = "ERROR:  Controller dBm : %s != AP dBm: %s.  " % (cc_dbm, ap_dbm)
                        logg.info(err)
                        csv.write(err)
                        csvs.write(err)
                        e_tot += err
                    if (cc_power != ap_power):
                        err = "ERROR:  Controller Power : %s != AP Power: %s.  " % (cc_power, ap_power)
                        logg.info(err)
                        csv.write(err)
                        csvs.write(err)
                        e_tot += err

                    if (_bw != bw):
                        err = "WARNING: Known Issue with AX210 Requested bandwidth: %s != station's reported bandwidth: %s.  " % (bw, _bw)
                        e_tot += err
                        logg.info(err)
                        csv.write(err)
                        csvs.write(err)
                    if (_nss != n):
                        err = "ERROR:  Station NSS: %s != configured: %s.  " % (_nss, n)
                        logg.info(err)
                        csv.write(err)
                        csvs.write(err)
                        e_tot += err
                    if (e_tot == ""):
                        e_w_tot = e_tot + w_tot + i_tot
                        if(w_tot == ""):
                            worksheet.write(row, col, e_w_tot, green_left)
                            col += 1
                        else:
                            worksheet.write(row, col, e_w_tot, orange_left)
                            col += 1
                    else:
                        e_w_tot = e_tot + w_tot + i_tot
                        worksheet.write(row, col, e_w_tot, red_left)
                        col += 1
                    row += 1

                    # reset colors in case of failure
                    center_blue = center_blue_tmp
                    center_tan = center_tan_tmp
                    center_peach = center_peach_tmp
                    center_pink = center_pink_tmp
                    center_yel_red = center_yel_red_tmp
                    center_yel = center_yel_tmp

                    csv.write("\n")
                    csv.flush()

                    csvs.write("\n")
                    csvs.flush()

                    # write out the data and exit on error : error takes presidence over failure
                    if (e_tot != ""):
                        if(args.exit_on_error):
                            logg.info("EXITING ON ERROR, exit_on_error err: {} ".format(e_tot))
                            close_workbook(workbook)
                            exit(1)

                    # write out the data and exit on failure
                    if (pf == 0):
                        if(args.exit_on_fail):
                            if(e_tot != ""):
                                logg.info("EXITING ON FAILURE as a result of  err {}".format(e_tot))
                            else:
                                logg.info("EXITING ON FAILURE, exit_on_fail set there was no err ")
                            close_workbook(workbook)
                            exit(1)

    workbook.close()

    # check if keeping the existing state
    # TODO add --no_cleanup
    # Set things back to defaults
    # if no_cleanup_station is False then clean up station
    # TODO Have the station clean up be with
    if(args.no_cleanup_station is False):
        # Remove LANforge traffic connection
        logg.info("Remove LANforge traffic connections")
        subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "do_cmd",
                        "--cmd", "set_cx_state all c-udp-power DELETED"], capture_output=False)
        subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "do_cmd",
                        "--cmd", "rm_endp c-udp-power-A"], capture_output=False)
        subprocess.run(["./lf_firemod.pl", "--manager", lfmgr, "--resource", lfresource, "--action", "do_cmd",
                        "--cmd", "rm_endp c-udp-power-B"], capture_output=False)

        logg.info("--no_cleanup_station set False,  Deleting all stations on radio {}".format(args.radio))
        subprocess.run(["./lf_associate_ap.pl", "--mgr", lfmgr, "--action", "del_all_phy", "--port_del", args.radio], timeout=20, capture_output=False)

    # keep the state of the controller
    if(args.keep_state):
        # TODO may have to check the AP type or AP series
        logg.info("9800/3504 flag --keep_state True thus leaving controller is last test configuration")
        if args.band == 'dual_band_6g':
            pss = cs.show_ap_dot11_dual_band_6gz_summary()
            logg.info(pss)
            pss = cs.show_ap_bssid_dual_band_6ghz()
            logg.info(pss)
        elif args.band == 'dual_band_5g':
            pss = cs.show_ap_dot11_dual_band_5gz_summary()
            logg.info(pss)
            pss = cs.show_ap_bssid_dual_band_5ghz()
            logg.info(pss)
        elif args.band == '6g':
            pss = cs.show_ap_dot11_6gz_summary()
            logg.info(pss)
            pss = cs.show_ap_bssid_6ghz()
            logg.info(pss)
        pss = cs.show_ap_dot11_5gz_summary()
        logg.info(pss)
        pss = cs.show_ap_dot11_24gz_summary()
        logg.info(pss)
        pss = cs.show_ap_summary()
        logg.info(pss)

    else:
        logg.info("9800/3504 flag --keep_state False thus setting controller to known state ")
        # TODO what is the known state

        # Disable AP, retrun AP to known settings , enable AP
        # TODO Choose fault settings
        if args.series == "9800":
            pss = cs.config_no_wlan()
            logg.info(pss)

        # Disable wlan networks to try to restore to original configuration
        if args.band == 'dual_band_6g':
            pss = cs.ap_dot11_dual_band_6ghz_shutdown()
            logg.info(pss)
        elif args.band == 'dual_band_5g':
            pss = cs.ap_dot11_dual_band_5ghz_shutdown()
            logg.info(pss)
        else:
            pss = cs.ap_dot11_6ghz_shutdown()
            logg.info(pss)
        pss = cs.ap_dot11_5ghz_shutdown()
        logg.info(pss)
        pss = cs.ap_dot11_24ghz_shutdown()
        logg.info(pss)

        if args.band == 'dual_band_6g':
            pss = cs.config_dot11_dual_band_6ghz_tx_power()
            logg.info(pss)
        elif args.band == 'dual_band_5g':
            pss = cs.config_dot11_dual_band_5ghz_tx_power()
            logg.info(pss)
        elif args.band == '6g':
            pss = cs.config_dot11_6ghz_tx_power()
            logg.info(pss)
        elif args.band == '5g':
            pss = cs.config_dot11_5ghz_tx_power()
            logg.info(pss)

        # NSS is set on the station earlier...
        if (ch != "NA"):
            if args.band == 'dual_band_6g':
                pss = cs.config_dot11_dual_band_6ghz_channel()
            elif args.band == 'dual_band_5g':
                pss = cs.config_dot11_dual_band_5ghz_channel()
            elif args.band == '6g':
                pss = cs.config_dot11_6ghz_channel()
            elif args.band == '5g':
                pss = cs.config_dot11_5ghz_channel()
            elif args.band == '24g':
                pss = cs.config_dot11_24ghz_channel()
            logg.info(pss)

        if (bw != "NA"):
            if args.band == 'dual_band_6g':
                pss = cs.config_dot11_dual_band_6ghz_channel_width()
            elif args.band == 'dual_band_5g':
                pss = cs.config_dot11_dual_band_5ghz_channel_width()
            elif args.band == '6g':
                pss = cs.config_dot11_6ghz_channel_width()
            elif args.band == '5g':
                pss = cs.config_dot11_5ghz_channel_width()
            logg.info(pss)

        if args.series == "9800":
            if args.band == 'dual_band_6g':
                pss = cs.config_no_ap_dot11_dual_band_6ghz_shutdown()
                logg.info(pss)
            elif args.band == 'dual_band_5g':
                pss = cs.config_no_ap_dot11_dual_band_5ghz_shutdown()
                logg.info(pss)
            elif args.band == '6g':
                pss = cs.config_no_ap_dot11_6ghz_shutdown()
                logg.info(pss)
            pss = cs.config_no_ap_dot11_5ghz_shutdown()
            logg.info(pss)
            pss = cs.config_no_ap_dot11_24ghz_shutdown()
            logg.info(pss)

            if args.band == 'dual_band_6g':
                pss = cs.ap_dot11_dual_band_6ghz_radio_role_auto()
                logg.info(pss)
            elif args.band == 'dual_band_5g':
                pss = cs.ap_dot11_dual_band_5ghz_radio_role_auto()
                logg.info(pss)
            elif args.band == '6g':
                pss = cs.ap_dot11_6ghz_radio_role_auto()
                logg.info(pss)
            pss = cs.ap_dot11_5ghz_radio_role_auto()
            logg.info(pss)

        else:
            pss = cs.config_no_ap_dot11_5ghz_shutdown()
            logg.info(pss)
            pss = cs.config_no_ap_dot11_24ghz_shutdown()
            logg.info(pss)

        if args.band == 'dual_band_6g':
            pss = cs.config_no_ap_dot11_dual_band_6ghz_shutdown()  # enable_network dual_band 6ghz
            logg.info(pss)
        if args.band == 'dual_band_5g':
            pss = cs.config_no_ap_dot11_dual_band_5ghz_shutdown()  # enable_network dual_band 6ghz
            logg.info(pss)
        if args.band == '6g':
            pss = cs.config_no_ap_dot11_6ghz_shutdown()  # enable_network 6ghz
            logg.info(pss)
        if args.band == '5g':
            pss = cs.config_no_ap_dot11_5ghz_shutdown()  # enable_network 5ghz
            logg.info(pss)
        if args.band == '24g':
            pss = cs.config_no_ap_dot11_24ghz_shutdown()  # enable_network 24ghz
            logg.info(pss)

        # try enabling all bands
        if args.enable_all_bands:
            if args.band == 'dual_band_6g':
                pss = cs.config_no_ap_dot11_dual_band_6ghz_shutdown()  # enable_network dual_band 6ghz
                logg.info(pss)
            if args.band == 'dual_band_5g':
                pss = cs.config_no_ap_dot11_dual_band_5ghz_shutdown()  # enable_network dual_band 6ghz
                logg.info(pss)
            if args.band == '6g':
                pss = cs.config_no_ap_dot11_6ghz_shutdown()  # enable_network 6ghz
                logg.info(pss)

            pss = cs.config_no_ap_dot11_5ghz_shutdown()  # enable_network 5ghz
            logg.info(pss)
            pss = cs.config_no_ap_dot11_24ghz_shutdown()  # enable_network 5ghz
            logg.info(pss)

    # Show controller status
    # Note
    if args.band == 'dual_band_6g':
        pss = cs.show_ap_dot11_dual_band_6gz_summary()
        logg.info(pss)
        pss = cs.show_ap_bssid_dual_band_6ghz()
        logg.info(pss)
    elif args.band == 'dual_band_5g':
        pss = cs.show_ap_dot11_dual_band_5gz_summary()
        logg.info(pss)
        pss = cs.show_ap_bssid_dual_band_5ghz()
        logg.info(pss)
    elif args.band == '6g':
        pss = cs.show_ap_dot11_6gz_summary()
        logg.info(pss)
        pss = cs.show_ap_bssid_6ghz()
        logg.info(pss)

    pss = cs.show_ap_dot11_5gz_summary()
    logg.info(pss)
    pss = cs.show_ap_dot11_24gz_summary()
    logg.info(pss)
    # Generate Report
    report.set_title("Tx Power")
    report.build_banner()
    report.set_table_title("Tx Power")

    # close the workbook
    close_workbook(workbook)

    if args.html_report:
        # TODO fix csv output
        report.set_table_dataframe_from_csv_sep_tab(full_outfile)
        report.build_table()
        # TODO the table looks off
        try:
            report.set_table_dataframe_from_xlsx(outfile_xlsx)
            report.build_table()
            report.build_footer()
            report.write_html_with_timestamp()
            report.write_index_html()

            report.write_pdf(_page_size='A3', _orientation='Landscape')
            # report.write_pdf_with_timestamp(_page_size='A4', _orientation='Portrait')
            # report.write_pdf_with_timestamp(_page_size='A4', _orientation='Landscape')
        except BaseException:
            traceback.print_exc()


# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
if __name__ == '__main__':
    main()
    print("Summary results stored in %s, full results in %s, xlsx file in %s" % (outfile, full_outfile, outfile_xlsx))

####
####
####
