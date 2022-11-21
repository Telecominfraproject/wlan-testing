#!/usr/bin/env python3
"""
NAME: lf_add_profile.py

PURPOSE:    Add LANforge device profile. This can give a high level description of how the LANforge system should act. 
            The profile can then be selected in higher-level test cases to auto-generate lower level configuration. 

EXAMPLE:

lf_add_profile.py  , the --name refers to the profile name

    vscode sample:
            "args":[
            "--mgr","192.168.0.104",
            "--mgr_port","8080",
            "--lf_user","lanforge",
            "--lf_passwd","lanforge",
            "--antenna","4",
            "--instance_count","1",
            // see http://www.candelatech.com/lfcli_ug.php#add_profile for the profile flags
            //"--profile_flags","DHCP_SERVER,SKIP_DHCP_ROAM,NAT,ENABLE_POWERSAVE",
            "--profile_flags","4105",
            "--name","Routed-AP-QA13",  
            "--profile_type","routed_ap",
            "--ssid","vap",
            "--passwd","hello123",
            "--dut","Routed-AP-13",
            "--text","Making a Routed-AP-13",
            "--log_level","debug",
            "--debug"]

    Command line:
    see see http://www.candelatech.com/lfcli_ug.php#add_profile for the profile flags
    ./lf_add_profile.py --mgr 192.168.0.104 --mgr_port 8080 --lf_user lanforge --lf_passwd lanforge --antenna 4
        --instance_count 1 --profile_flags 4105 --name Routed-AP-QA13 --profile_type routed_ap 
        --ssid vap --passwd hello123 --dut Routed-AP-13 --text 'Making a Routed-AP-13 profile' 
        --log_level debug --debug

    Once the profile is created a chamberview need to be created based off that profile
    ./create_chamberview.py --lfmgr 192.168.0.104 --port 8080 --create_scenario QA13-2 
    --raw_line 'profile_link 1.1 Routed-AP-QA13 1 NA NA wiphy1,AUTO -1 NA' --raw_line 'resource 1.1.0 0'

    The --raw_line are determined applying the profile above 


NOTES:


TO DO NOTES:

"""
import sys

if sys.version_info[0] != 3:
    print("This script requires Python3")
    exit()

import importlib
import argparse
from pprint import pformat
import os
import logging

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
lanforge_api = importlib.import_module("lanforge_client.lanforge_api")
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
from lanforge_client.lanforge_api import LFJsonQuery
from lanforge_client.lanforge_api import LFJsonCommand
from lanforge_client.lanforge_api import LFSession


lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

logger = logging.getLogger(__name__)

# add_wanpath
# http://www.candelatech.com/lfcli_ug.php#add_wanpath


class lf_add_profile():
    def __init__(self,
                 lf_mgr=None,
                 lf_port=None,
                 lf_user=None,
                 lf_passwd=None,
                 debug=False,
                 ):
        self.lf_mgr = lf_mgr
        self.lf_port = lf_port
        self.lf_user = lf_user
        self.lf_passwd = lf_passwd
        self.debug = debug

        self.session = LFSession(lfclient_url="http://%s:8080" % self.lf_mgr,
                                 debug=debug,
                                 connection_timeout_sec=4.0,
                                 stream_errors=True,
                                 stream_warnings=True,
                                 require_session=True,
                                 exit_on_error=True)
        # type hinting
        self.command: LFJsonCommand
        self.command = self.session.get_command()
        self.query: LFJsonQuery
        self.query = self.session.get_query()

    # http://www.candelatech.com/lfcli_ug.php#add_profile
    # add_profile Routed-AP-QA Routed-AP 0 4 0 0 vap hello123 4105
    def add_profile(self,
                    _alias_prefix: str = None,                 # Port alias prefix, aka hostname prefix.
                    _antenna: str = None,                      # Antenna count for this profile.
                    _bandwidth: str = None,                    # 0 (auto), 20, 40, 80 or 160
                    _eap_id: str = None,                       # EAP Identifier
                    _flags_mask: str = None,                   # Specify what flags to set.
                    _freq: str = None,                         # WiFi frequency to be used, 0 means default.
                    _instance_count: str = None,               # Number of devices (stations, vdevs, etc)
                    _mac_pattern: str = None,                  # Optional MAC-Address pattern, for instance: xx:xx:xx:*:*:xx
                    _name: str = None,                         # Profile Name. [R]
                    _passwd: str = None,                       # WiFi Password to be used (AP Mode), [BLANK] means no password.
                    _profile_flags: str = None,                # Flags for this profile, see above.
                    _profile_flags_list: list = [],            # Flags for the profile passed as list
                    _profile_type: str = None,                 # Profile type: See above. [W]
                    _ssid: str = None,                         # WiFi SSID to be used, [BLANK] means any.
                    _vid: str = None,                          # Vlan-ID (only valid for vlan profiles).
                    _wifi_mode: str = None,                    # WiFi Mode for this profile.
                    _response_json_list: list = None,
                    _errors_warnings: list = None,
                    _suppress_related_commands: bool = False):

        flag_val =  0
        if _profile_flags is not None:
            if '0x' in _profile_flags:
                _profile_flags = str(int(_profile_flags.replace('0x',''), 16))

            flag_val = _profile_flags
            logger.debug("profile_flags used flag_val = {flag_val}".format(flag_val=flag_val))
        elif len(_profile_flags_list) != 0:
            flag_val = self.command.set_flags(self.command.AddProfileProfileFlags,0, flag_names=_profile_flags_list)
            logger.debug("profile_flags_list used flag_val = {flag_val}".format(flag_val=flag_val))
        else:
            logger.error("_profile_flags is None and _profile_flags_list is empty")

        # flag_val = self.command.set_flags(self.command.AddProfileProfileFlags,0, flag_names=_profile_flags)            

        self.command.post_add_profile(
            alias_prefix=_alias_prefix,             # Port alias prefix, aka hostname prefix.
            antenna=_antenna,                       # Antenna count for this profile.
            bandwidth=_bandwidth,                   # 0 (auto), 20, 40, 80 or 160
            eap_id=_eap_id,                         # EAP Identifier
            flags_mask=flag_val,                    # Specify what flags to set.
            freq=_freq,                             # WiFi frequency to be used, 0 means default.
            instance_count=_instance_count,         # Number of devices (stations, vdevs, etc)
            mac_pattern=_mac_pattern,               # Optional MAC-Address pattern, for instance:   xx:xx:xx:*:*:xx
            name=_name,                             # Profile Name. [R]
            passwd=_passwd,                         # WiFi Password to be used (AP Mode), [BLANK] means no password.
            profile_flags=flag_val,                 # Flags for this profile, see above.
            profile_type=_profile_type,             # Profile type: See lanforge_api [W]
            ssid=_ssid,                             # WiFi SSID to be used, [BLANK] means any.
            vid=_vid,                               # Vlan-ID (only valid for vlan profiles).
            wifi_mode=_wifi_mode,                   # WiFi Mode for this profile.
            response_json_list=_response_json_list,
            debug=self.debug,
            errors_warnings=_errors_warnings,
            suppress_related_commands=_suppress_related_commands)

    # This text will be added to the end of the notes field for Profiles. 
    # The text must be entered one line at a time, primarily due to CLI parsing limitations. 

    # http://www.candelatech.com/lfcli_ug.php#add_profile_notes
    def add_profile_notes(self,
        _dut: str = None,                          # Profile Name. [R]
        _text: str = None,                         # [BLANK] will erase all, any other text will be appended to existing text. 
        _response_json_list: list = None,
        _errors_warnings: list = None,
        _suppress_related_commands: bool = False):

        self.command.post_add_profile_notes(
                               dut=_dut,                          # Profile Name. [R]
                               text=_text,                        # [BLANK] will erase all, any other text will be appended to existing text. 
                               response_json_list=_response_json_list,
                               debug=self.debug,
                               errors_warnings=_errors_warnings,
                               suppress_related_commands=_suppress_related_commands)



# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #


def main():
    parser = argparse.ArgumentParser(
        prog=__file__,
        formatter_class=argparse.RawTextHelpFormatter,
        description='''\
            adds a chamberview profile

            add_profile Routed-AP-QA Routed-AP 0 4 1 0 vap hello123 4105

            profile flags   
            4105 = 0x1009          

            DHCP_SERVER = 0x1           # This should provide DHCP server.
            WPA2        = 0x8
            ENABLE_POWERSAVE = 0x1000   # Enable power-save when creating stations.

            pass in --profile_flags 'DHCP_SERVER,WPA2,ENABLE_POWERSAVE'

    Example:
        Command line:
        see see http://www.candelatech.com/lfcli_ug.php#add_profile for the profile flags
        ./lf_add_profile.py --mgr 192.168.0.104 --mgr_port 8080 --lf_user lanforge --lf_passwd lanforge --antenna 4\
            --instance_count 1 --profile_flags 4105 --name Routed-AP-QA13 --profile_type routed_ap\
            --ssid vap --passwd hello123 --dut Routed-AP-13 --text 'Making a Routed-AP-13 profile'\
            --log_level debug --debug

        Once the profile is created a chamberview need to be created based off that profile
        ./create_chamberview.py --lfmgr 192.168.0.104 --port 8080 --delete_scenario --create_scenario QA13-2\
        --raw_line 'profile_link 1.1 Routed-AP-QA13 1 NA NA wiphy1,AUTO -1 NA' --raw_line 'resource 1.1.0 0'\

        The --raw_line are determined applying the profile above 

            ''')
    # http://www.candelatech.com/lfcli_ug.php#add_profile
    parser.add_argument("--host", "--mgr", dest='mgr', help='specify the GUI to connect to')
    parser.add_argument("--mgr_port", help="specify the GUI to connect to, default 8080", default="8080")
    parser.add_argument("--lf_user", help="lanforge user name", default="lanforge")
    parser.add_argument("--lf_passwd", help="lanforge password", default="lanforge")

    # http://www.candelatech.com/lfcli_ug.php#add_profile
    parser.add_argument('--alias_prefix', help='(add profile) alias_prefix Port alias prefix, aka hostname prefix. ')
    parser.add_argument('--antenna', help="(add profile) Antenna count for this profile.")
    parser.add_argument('--bandwidth', help="(add profile) 0 (auto), 20, 40, 80 or 160")
    parser.add_argument("--eap_id", help="(add profile) EAP Identifier")
    parser.add_argument("--flags_mask", help="(add profile) Specify what flags to set.")
    parser.add_argument("--freq", help="(add profile)WiFi frequency to be used, 0 means default.")
    parser.add_argument("--instance_count", help="(add profile) Number of devices (stations, vdevs, etc)")
    parser.add_argument("--mac_pattern", help="(add profile) Optional MAC-Address pattern, for instance:  xx:xx:xx:*:*:xx")
    parser.add_argument("--name", help="(add profile) Profile Name. [R] ", required=True)
    parser.add_argument('--passwd', help='(add profile) WiFi SSID to be used, [BLANK] means any.')
    parser.add_argument('--profile_flags', help='pass in flags as a decimal value takes presidence over hex and --pf []')
    parser.add_argument('--profile_flags_hex', help='pass in flags as a hex value')
    parser.add_argument('--pf', 
            # nargs='+', # trying to pass in a list
            action='append',
            help=''' 
    (add profile) 
    Profile flags entered as a list
    Flags for this profilelanforge_api AddProfileProfileFlags'
    enter the flags as a list 0x1009 is:
        DHCP_SERVER = 0x1           # This should provide DHCP server.
        SKIP_DHCP_ROAM = 0x10       # Ask station to not re-do DHCP on roam.
        NAT = 0x100                 # Enable NAT if this object is in a virtual router
        ENABLE_POWERSAVE = 0x1000   # Enable power-save when creating stations.

        pass in --profile_flags 'DHCP_SERVER,SKIP_DHCP_ROAM,NAT,ENABLE_POWERSAVE'

    flags:
            p_11r = 0x40                   # Use 802.11r roaming setup.
            ALLOW_11W = 0x800              # Set 11w (MFP/PMF) to optional.
            BSS_TRANS = 0x400              # Enable BSS Transition logic
            DHCP_SERVER = 0x1              # This should provide DHCP server.
            EAP_PEAP = 0x200               # Enable EAP-PEAP
            EAP_TTLS = 0x80                # Use 802.1x EAP-TTLS
            ENABLE_POWERSAVE = 0x1000      # Enable power-save when creating stations.
            NAT = 0x100                    # Enable NAT if this object is in a virtual router
            SKIP_DHCP_ROAM = 0x10          # Ask station to not re-do DHCP on roam.
            WEP = 0x2                      # Use WEP encryption
            WPA = 0x4                      # Use WPA encryption
            WPA2 = 0x8                     # Use WPA2 encryption
            WPA3 = 0x20                    # Use WPA3 encryption
    ''')
    parser.add_argument("--profile_type", help='''
        (add profile) 
        Profile type: [W]
        Bridged_AP: briged-AP
        Monitor: monitor
        Peer: peer
        RDD: rdd
        Routed_AP: routed-AP
        STA: STA-AC
        STA: STA-AUTO
        STA: STA-AX
        STA: STA-abg
        STA: STA-n
        Uplink: uplink-nat
        Upstream: upstrream
        Upstream: upstream-dhcp
        as_is: as-is
        NA
        ''')
    parser.add_argument("--ssid", help='(add profile) WiFi SSID to be used, [BLANK] means any.')
    parser.add_argument("--vid", help='(add profile) Vlan-ID (only valid for vlan profiles).')
    parser.add_argument("--wifi_mode", help='''(add profile) WiFi Mode for this profile.
        p_802_11a = "802.11a"        # 802.11a
        AUTO = "AUTO"                # 802.11g
        aAX = "aAX"                  # 802.11a-AX (6E disables /n and /ac)
        abg = "abg"                  # 802.11abg
        abgn = "abgn"                # 802.11abgn
        abgnAC = "abgnAC"            # 802.11abgn-AC
        abgnAX = "abgnAX"            # 802.11abgn-AX
        an = "an"                    # 802.11an
        anAC = "anAC"                # 802.11an-AC
        anAX = "anAX"                # 802.11an-AX
        as_is = "as_is"              # Make no changes to current configuration
        b = "b"                      # 802.11b
        bg = "bg"                    # 802.11bg
        bgn = "bgn"                  # 802.11bgn
        bgnAC = "bgnAC"              # 802.11bgn-AC
        bgnAX = "bgnAX"              # 802.11bgn-AX
        bond = "bond"                # Bonded pair of Ethernet ports.
        bridged_ap = "bridged_ap"    # AP device in bridged mode. The EIDs may specify radio and bridged port.
        client = "client"            # Client-side non-WiFi device (Ethernet port, for instance).
        g = "g"                      # 802.11g
        mobile_sta = "mobile_sta"    # Mobile station device. Expects to connect to DUT AP(s) and upstream LANforge.
        monitor = "monitor"          # Monitor device/sniffer. The EIDs may specify which radios to use.
        peer = "peer"                # Edge device, client or server (Ethernet port, for instance).
        rdd = "rdd"                  # Pair of redirect devices, typically associated with VR to act as traffic endpoint
        routed_ap = "routed_ap"      # AP in routed mode. The EIDs may specify radio and upstream port.
        sta = "sta"                  # Station device, most likely non mobile. The EIDs may specify radio(s) to use
        uplink = "uplink"            # Uplink towards rest of network (can go in virtual router and do NAT)
        upstream = "upstream"        # Upstream server device. The EIDs may specify which ports to use.
        vlan = "vlan"                # 802.1q VLAN. Specify VID with the 'freq' option.
        ''')

    # http://www.candelatech.com/lfcli_ug.php#add_profile_notes
    parser.add_argument('--dut', help='(add profile notes) Profile Name. [R]', required=True)
    parser.add_argument('--text', action='append',
                        nargs=1,
                        help='''(add profile notes) list of lines of text  
                                            [BLANK] will erase all, 
                                            any other text will be appended to existing text. 
                                            must be entered line by line
                                        ''')

    # Logging Configuration
    parser.add_argument('--log_level', default=None, help='Set logging level: debug | info | warning | error | critical')
    parser.add_argument("--lf_logger_config_json", help="--lf_logger_config_json <json file> , json configuration of logger")
    parser.add_argument('--debug', help='Legacy debug flag', action='store_true')

    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    # set the logger level to debug
    if args.log_level:
        logger_config.set_level(level=args.log_level)

    # lf_logger_config_json will take presidence to changing debug levels
    if args.lf_logger_config_json:
        # logger_config.lf_logger_config_json = "lf_logger_config.json"
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()


    profile = lf_add_profile(lf_mgr=args.mgr,
                            lf_port=args.mgr_port,
                            lf_user=args.lf_user,
                            lf_passwd=args.lf_passwd,
                            debug=args.debug)

    logger.debug("profile_flags_list {pf}".format(pf=args.pf))
    if args.pf:
        profile_flags_list = args.pf.copy()
    else:
        profile_flags_list = []


    # parameters for add_profile
    # alias
    # create side A
    print("args.alias_prefix {}".format(args.alias_prefix))
    profile.add_profile(
                    _alias_prefix=args.alias_prefix,                    # Port alias prefix, aka hostname prefix.
                    _antenna=args.antenna,                              # Antenna count for this profile.
                    _bandwidth=args.bandwidth,                          # 0 (auto), 20, 40, 80 or 160
                    _eap_id=args.eap_id,                                # EAP Identifier
                    _flags_mask=args.flags_mask,                        # Specify what flags to set.
                    _freq=args.freq,                                    # WiFi frequency to be used, 0 means default.
                    _instance_count=args.instance_count,                # Number of devices (stations, vdevs, etc)
                    _mac_pattern=args.mac_pattern,                      # Optional MAC-Address pattern, for instance: xx:xx:xx:*:*:xx
                    _name=args.name,                                    # Profile Name. [R]
                    _passwd=args.passwd,                                # WiFi Password to be used (AP Mode), [BLANK] means no password.
                    _profile_flags_list=profile_flags_list,             # Flags for the profile passed as list
                    _profile_flags=args.profile_flags,                  # Flags for this profile, see above.
                    _profile_type=args.profile_type,                    # Profile type: See above. [W]
                    _ssid=args.ssid,                                    # WiFi SSID to be used, [BLANK] means any.
                    _vid=args.vid,                                      # Vlan-ID (only valid for vlan profiles).
                    _wifi_mode=args.wifi_mode                          # WiFi Mode for this profile.
                    )

    if args.text is not None:
        for text in args.text:
            profile.add_profile_notes(_dut=args.name,
                                    _text=text)


if __name__ == "__main__":
    main()
