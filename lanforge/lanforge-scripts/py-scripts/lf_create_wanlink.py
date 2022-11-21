#!/usr/bin/env python3
"""
NAME: lf_create_wanlink.py

PURPOSE: create a wanlink using the lanforge api

EXAMPLE:
Both port_A and port_B have the same configuraiton
$ ./lf_create_wanlink.py --mgr 192.168.0.104 --mgr_port 8080 --port_A eth1 --port_B eth2\
    --speed 1024000 --wl_name wanlink --latency 24 --max_jitter 50 --jitter_freq 6 --drop_freq 12\
    --log_level debug --debug 

Mixed configuration for port_A and port_B
$ ./lf_create_wanlink.py --mgr 192.168.0.104 --mgr_port 8080 --port_A eth1 --port_B eth2\
    --speed_A 1024000 --speed_B 2048000 --wl_name wanlink --latency_A 24 --latency_B 32 --max_jitter 50 --jitter_freq 6 --drop_freq 12\
    --log_level debug --debug 



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


class lf_create_wanlink():
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

    # The order to creating an wanlink between two ethernet ports
    # add_wl_endp
    # add_cx
    # set_wanlink_info side A
    # set_endp_flag side A
    # set_wanlink_info side B
    # set_endp_flag side B

    # verify set_wl_corruption side A - commented out
    # verify set_wl_corruption side B - commented out

    # nc_show_endpoints
    # nc_show_endpoints

    # query.get_wl
    # query.get_wl_endp


    def add_wl_endp(self,
                    _alias: str = None,                        # Name of endpoint. [R]
                    _cpu_id: str = None,                       # The CPU/thread that this process should run on
                    # (kernel-mode only).
                    _description: str = None,                  # Description for this endpoint, put in single quotes if
                    # it contains spaces.
                    _latency: str = None,                      # The latency (ms) that will be added to each packet
                    # entering this WanLink.
                    _max_rate: str = None,                     # Maximum transmit rate (bps) for this WanLink.
                    _port: str = None,                         # Port number. [W]
                    _resource: int = None,                     # Resource number. [W]
                    _shelf: int = 1,                           # Shelf name/id. [R][D:1]
                    _wle_flags: str = None,                    # WanLink Endpoint specific flags, see above.
                    _debug: bool = False,
                    _suppress_related_commands: bool = False):

        if _alias is None:
            logger.error("alias in None alias must be set to end point A or end point B. Exiting")
            exit(1)

        self.command.post_add_wl_endp(
            alias=_alias,                        # Name of endpoint. [R]
            cpu_id=_cpu_id,                       # The CPU/thread that this process should run on
            # (kernel-mode only).
            description=_description,                  # Description for this endpoint, put in single quotes if
            # it contains spaces.
            latency=_latency,                      # The latency (ms) that will be added to each packet
            # entering this WanLink.
            max_rate=_max_rate,                     # Maximum transmit rate (bps) for this WanLink.
            port=_port,                         # Port number. [W]
            resource=_resource,                     # Resource number. [W]
            shelf=_shelf,                           # Shelf name/id. [R][D:1]
            wle_flags=_wle_flags,                    # WanLink Endpoint specific flags, see above.
            debug=self.debug,
            suppress_related_commands=_suppress_related_commands)

    def set_wanlink_info(self,
                         _drop_freq: str = None,                    # How often, out of 1,000,000 packets, should we
                         # purposefully drop a packet.
                         _dup_freq: str = None,                     # How often, out of 1,000,000 packets, should we
                         # purposefully duplicate a packet.
                         _extra_buffer: str = None,                 # The extra amount of bytes to buffer before
                         # dropping pkts, in units of 1024. Use -1 for AUTO.
                         _jitter_freq: str = None,                  # How often, out of 1,000,000 packets, should we
                         # apply jitter.
                         _latency: str = None,                      # The base latency added to all packets, in
                         # milliseconds (or add 'us' suffix for microseconds
                         _max_drop_amt: str = None,                 # Maximum amount of packets to drop in a row.
                         # Default is 1.
                         _max_jitter: str = None,                   # The maximum jitter, in milliseconds (or ad 'us'
                         # suffix for microseconds)
                         _max_lateness: str = None,                 # Maximum amount of un-intentional delay before pkt
                         # is dropped. Default is AUTO
                         _max_reorder_amt: str = None,              # Maximum amount of packets by which to reorder,
                         # Default is 10.
                         _min_drop_amt: str = None,                 # Minimum amount of packets to drop in a row.
                         # Default is 1.
                         _min_reorder_amt: str = None,              # Minimum amount of packets by which to reorder,
                         # Default is 1.
                         _name: str = None,                         # The name of the endpoint we are configuring. [R]
                         _playback_capture_file: str = None,        # Name of the WAN capture file to play back.
                         _reorder_freq: str = None,                 # How often, out of 1,000,000 packets, should we
                         # make a packet out of order.
                         _speed: str = None,                        # The maximum speed of traffic this endpoint will
                         # accept (bps).
                         _debug: bool = False,
                         _suppress_related_commands: bool = False):

        # the LANforge api will handle the None values
        self.command.post_set_wanlink_info(
            drop_freq=_drop_freq,                    # How often, out of 1,000,000 packets, should we
            # purposefully drop a packet.
            dup_freq=_dup_freq,                     # How often, out of 1,000,000 packets, should we
            # purposefully duplicate a packet.
            extra_buffer=_extra_buffer,                 # The extra amount of bytes to buffer before
            # dropping pkts, in units of 1024. Use -1 for AUTO.
            jitter_freq=_jitter_freq,                  # How often, out of 1,000,000 packets, should we
            # apply jitter.
            latency=_latency,                      # The base latency added to all packets, in
            # milliseconds (or add 'us' suffix for microseconds
            max_drop_amt=_max_drop_amt,                 # Maximum amount of packets to drop in a row.
            # Default is 1.
            max_jitter=_max_jitter,                   # The maximum jitter, in milliseconds (or ad 'us'
            # suffix for microseconds)
            max_lateness=_max_lateness,                 # Maximum amount of un-intentional delay before pkt
            # is dropped. Default is AUTO
            max_reorder_amt=_max_reorder_amt,              # Maximum amount of packets by which to reorder,
            # Default is 10.
            min_drop_amt=_min_drop_amt,                 # Minimum amount of packets to drop in a row.
            # Default is 1.
            min_reorder_amt=_min_reorder_amt,              # Minimum amount of packets by which to reorder,
            # Default is 1.
            name=_name,                         # The name of the endpoint we are configuring. [R]
            playback_capture_file=_playback_capture_file,        # Name of the WAN capture file to play back.
            reorder_freq=_reorder_freq,                 # How often, out of 1,000,000 packets, should we
            # make a packet out of order.
            speed=_speed,                        # The maximum speed of traffic this endpoint will
            # accept (bps).
            debug=self.debug,
            suppress_related_commands=_suppress_related_commands)

    # set_endp_flag 
    def set_endp_flag(self,
                    _flag: str = None,                         # The name of the flag. [R]
                    _name: str = None,                         # The name of the endpoint we are configuring. [R]
                    _val: str = None,                          # Either 1 (for on), or 0 (for off). [R,0-1]
                    _suppress_related_commands: bool = False):

        self.command.post_set_endp_flag(flag=_flag,             # The name of the flag. [R]
                                        name=_name,             # The name of the endpoint we are configuring. [R]
                                        val=_val,               # Either 1 (for on), or 0 (for off). [R,0-1]
                                        debug=self.debug,
                                        suppress_related_commands=_suppress_related_commands)

    def add_cx(self,
               _alias=None,
               _rx_endp=None,  # endp_A
               _tx_endp=None,  # endp_B
               _test_mgr="default_tm"):

        self.command.post_add_cx(alias=_alias,
                                 rx_endp=_rx_endp,
                                 tx_endp=_tx_endp,
                                 test_mgr=_test_mgr)


    def get_wl(self,
               _eid_list: list = None,
               _requested_col_names: list = None,
               _wait_sec: float = 0.01,
               _timeout_sec: float = 5.0,
               _errors_warnings: list = None):

        ewarn_list = []
        result = self.query.get_wl(eid_list=_eid_list,
                                   requested_col_names=_requested_col_names, 
                                   wait_sec=_wait_sec,
                                   timeout_sec=_timeout_sec,
                                   errors_warnings=ewarn_list,
                                   debug=self.debug)
        logger.debug(pformat(result))
        return result


    def get_wl_endp(self,
                    _eid_list: list = None,
                    _requested_col_names: list = None,
                    _wait_sec: float = 0.01,
                    _timeout_sec: float = 5.0,
                    _errors_warnings: list = None):

        result = self.query.get_wl_endp(eid_list=_eid_list,
                    requested_col_names=_requested_col_names,
                    wait_sec=_wait_sec,
                    timeout_sec=_timeout_sec,
                    errors_warnings=_errors_warnings,
                    debug=self.debug)

        logger.debug(pformat(result))
        return result

        


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #


def main():
    parser = argparse.ArgumentParser(
        prog=__file__,
        formatter_class=argparse.RawTextHelpFormatter,
        description='''\
            tests creating wanlink

Both port_A and port_B have the same configuraiton
$ ./lf_create_wanlink.py --mgr 192.168.0.104 --mgr_port 8080 --port_A eth1 --port_B eth2\
    --speed 1024000 --wl_name wanlink --latency 24 --max_jitter 50 --jitter_freq 6 --drop_freq 12\
    --log_level debug --debug 

Mixed configuration for port_A and port_B
$ ./lf_create_wanlink.py --mgr 192.168.0.104 --mgr_port 8080 --port_A eth1 --port_B eth2\
    --speed_A 1024000 --speed_B 2048000 --wl_name wanlink --latency_A 24 --latency_B 32 --max_jitter 50 --jitter_freq 6 --drop_freq 12\
    --log_level debug --debug 


            ''')
    # http://www.candelatech.com/lfcli_ug.php#add_wl_endp
    parser.add_argument("--host", "--mgr", dest='mgr', help='specify the GUI to connect to')
    parser.add_argument("--mgr_port", help="specify the GUI to connect to, default 8080", default="8080")
    parser.add_argument("--lf_user", help="lanforge user name default lanforge", default="lanforge")
    parser.add_argument("--lf_passwd", help="lanforge password defualt lanforge ", default="lanforge")
    parser.add_argument('--wl_name', '--alias', dest='wl_name', help='(add wl endp) The name of the endpoint we are configuring. [R] ', required=True)
    parser.add_argument('--cpu_id', help="(add wl endp) The CPU/thread that this process should run on (kernel-mode only). Default = 'NA'", default='NA')
    parser.add_argument('--description', help="(add wl endp) Description for this endpoint, put in single quotes if it contains spaces Default = 'NA'", default='NA')
    parser.add_argument("--latency", help="(add wl endp) The latency (ms) that will be added to each packet entering this WanLink. Default = 'NA' both ports", default='NA')
    parser.add_argument("--latency_A", help="(add wl endp) The latency (ms) that will be added to each packet entering this WanLink. Default = None port a", default=None)
    parser.add_argument("--latency_B", help="(add wl endp) The latency (ms) that will be added to each packet entering this WanLink. Default = None port b", default=None)
    parser.add_argument("--max_rate", help="(add wl endp) Maximum transmit rate (bps) for this WanLink. Default = 1024000 ", default='1024000')
    parser.add_argument("--max_rate_A", help="(add wl endp) Maximum transmit rate (bps) for this WanLink. Default = None ", default=None)
    parser.add_argument("--max_rate_B", help="(add wl endp) Maximum transmit rate (bps) for this WanLink. Default = None ", default=None)
    parser.add_argument('--port_A', help='(add wl endp) Endpoint A', default="eth1")
    parser.add_argument('--port_B', help='(add wl endp) Endpoint B', default="eth2")
    parser.add_argument("--resource", help='(add wl endp) LANforge resource Default', default=1)
    parser.add_argument("--shelf", help='(add wl endp) LANforge Shelf name/id', default=1)
    parser.add_argument("--wle_flags", help='(add wl endp) WanLink Endpoint specific flags, Default = 1, SHOW_WP = 1 .Show WanPaths in wanlink endpoint table in GUI', default=1)

    # http://www.candelatech.com/lfcli_ug.php#set_wanlink_info
    parser.add_argument('--drop_freq', help='(set wanlink info) How often, out of 1,000,000 packets, should we purposefully drop a packet. Default = 0 Both ports (%%)', default="0")
    parser.add_argument('--drop_freq_A', help='(set wanlink info) How often, out of 1,000,000 packets, should we purposefully drop a packet. Default = None port A (%%)', default=None)
    parser.add_argument('--drop_freq_B', help='(set wanlink info) How often, out of 1,000,000 packets, should we purposefully drop a packet. Default = None port B (%%)', default=None)
    parser.add_argument('--dup_freq', help='(set wanlink info) How often, out of 1,000,000 packets, should we purposefully duplicate a packet. Default = 0 Both ports (%%)', default="0")
    parser.add_argument('--dup_freq_A', help='(set wanlink info) How often, out of 1,000,000 packets, should we purposefully duplicate a packet. Default = None port A (%%)', default=None)
    parser.add_argument('--dup_freq_B', help='(set wanlink info) How often, out of 1,000,000 packets, should we purposefully duplicate a packet. Default = None port B (%%)', default=None)
    parser.add_argument('--extra_buffer', help='(set wanlink info) The extra amount of bytes to buffer before dropping pkts, in units of 1024. Use -1 for AUTO. Default = -1 Both ports (%%)', default="-1")
    parser.add_argument('--extra_buffer_A', help='(set wanlink info) The extra amount of bytes to buffer before dropping pkts, in units of 1024. Use -1 for AUTO. Default = None port A (%%)', default=None)
    parser.add_argument('--extra_buffer_B', help='(set wanlink info) The extra amount of bytes to buffer before dropping pkts, in units of 1024. Use -1 for AUTO. Default = None port B (%%)', default=None)
    parser.add_argument('--jitter_freq', help='(set wanlink info) How often, out of 1,000,000 packets, should we apply jitter. Default = 0 both ports (%%)', default="0")
    parser.add_argument('--jitter_freq_A', help='(set wanlink info) How often, out of 1,000,000 packets, should we apply jitter. Default = None port A (%%)', default=None)
    parser.add_argument('--jitter_freq_B', help='(set wanlink info) How often, out of 1,000,000 packets, should we apply jitter. Default = None port B (%%)', default=None)
    parser.add_argument('--latency_packet', help="(set wanlink info) The base latency added to all packets, in milliseconds (or add 'us' suffix for microseconds. Default = 20 both ports", default="20")
    parser.add_argument('--latency_packet_A', help="(set wanlink info) The base latency added to all packets, in milliseconds (or add 'us' suffix for microseconds. Default = None port A", default=None)
    parser.add_argument('--latency_packet_B', help="(set wanlink info) The base latency added to all packets, in milliseconds (or add 'us' suffix for microseconds. Default = None port B", default=None)
    parser.add_argument('--max_drop_amt', help='(set wanlink info) Maximum amount of packets to drop in a row. Default is 1. both ports', default="1")
    parser.add_argument('--max_drop_amt_A', help='(set wanlink info) Maximum amount of packets to drop in a row. Default is None. port A', default=None)
    parser.add_argument('--max_drop_amt_B', help='(set wanlink info) Maximum amount of packets to drop in a row. Default is None. port B', default=None)
    parser.add_argument('--max_jitter', help="(set wanlink info) The maximum jitter, in milliseconds (or ad 'us' suffix for microseconds) Default = 10 both ports (ms)", default="10")
    parser.add_argument('--max_jitter_A', help="(set wanlink info) The maximum jitter, in milliseconds (or ad 'us' suffix for microseconds) port A (ms)", default=None)
    parser.add_argument('--max_jitter_B', help="(set wanlink info) The maximum jitter, in milliseconds (or ad 'us' suffix for microseconds) port B (ms)", default=None)
    parser.add_argument('--max_lateness', help='(set wanlink info) Maximum amount of un-intentional delay before pkt both ports (ms) is dropped. Default is AUTO both ports', default="AUTO")
    parser.add_argument('--max_lateness_A', help='(set wanlink info) Maximum amount of un-intentional delay before pkt both ports (ms) is dropped. Default is AUTO port A', default=None)
    parser.add_argument('--max_lateness_B', help='(set wanlink info) Maximum amount of un-intentional delay before pkt both ports (ms) is dropped. Default is AUTO port B', default=None)
    parser.add_argument('--max_reorder_amt', help='(set wanlink info) Maximum amount of packets by which to reorder, Default is 10. both ports (ms)', default="10")
    parser.add_argument('--max_reorder_amt_A', help='(set wanlink info) Maximum amount of packets by which to reorder, Default is 10. both ports (ms) port A (ms)', default=None)
    parser.add_argument('--max_reorder_amt_B', help='(set wanlink info) Maximum amount of packets by which to reorder, Default is 10. both ports (ms) port B (ms)', default=None)
    parser.add_argument('--min_drop_amt', help='(set wanlink info) Minimum amount of packets to drop in a row. Default is 1. both ports (ms)', default="1")
    parser.add_argument('--min_drop_amt_A', help='(set wanlink info) Minimum amount of packets to drop in a row. Default is 1. both ports (ms) port A (ms)', default=None)
    parser.add_argument('--min_drop_amt_B', help='(set wanlink info) Minimum amount of packets to drop in a row. Default is 1. both ports (ms) port B (ms)', default=None)
    parser.add_argument('--min_reorder_amt', help='(set wanlink info) Minimum amount of packets by which to reorder, Default is 1. both ports ', default="1")
    parser.add_argument('--min_reorder_amt_A', help='(set wanlink info) Minimum amount of packets by which to reorder, Default is 1. port A', default=None)
    parser.add_argument('--min_reorder_amt_B', help='(set wanlink info) Minimum amount of packets by which to reorder, Default is 1. port B', default=None)
    parser.add_argument('--playback_capture_file', help='(set wanlink info) Name of the WAN capture file to play back. Default = None', default=None)
    parser.add_argument('--reorder_freq', help='(set wanlink info) How often, out of 1,000,000 packets, should we make a packet out of order. both ports Default = None', default=None)
    parser.add_argument('--reorder_freq_A', help='(set wanlink info) How often, out of 1,000,000 packets, should we make a packet out of order. port A Default = None', default=None)
    parser.add_argument('--reorder_freq_B', help='(set wanlink info) How often, out of 1,000,000 packets, should we make a packet out of order. port B Default = None', default=None)
    parser.add_argument('--speed', help='(set wanlink info) The maximum speed of traffic this endpoint will accept (bps). both ports', default=1000000)
    parser.add_argument('--speed_A', help='(set wanlink info) The maximum speed of traffic this endpoint will accept (bps). port A', default=None)
    parser.add_argument('--speed_B', help='(set wanlink info) The maximum speed of traffic this endpoint will accept (bps). port B', default=None)
    parser.add_argument('--suppress_related_commands', help='(set wanlink info) Used by lanforge_api Default False if set store true', action='store_true')

    # Set Endp Flags enable KernelMode 
    parser.add_argument('--kernel_mode', help='(set endp flag) Select  kernel-mode Wanlinks , must be the same for both endpoint sets both ports, Default = False', action='store_true')
    parser.add_argument('--pass_through_mode', help='''
        (set endp flag) pass-through means disable all impairments and slow-downs, without having to manually zero out all of the impairments.  Good way to turn it on/off without stopping traffic., 
        Default = False', action='store_true'
        ''', action='store_true')

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

    if not args.wl_name:
        logger.error("No wanlink name provided")
        exit(1)

    # The order to creating an wanlink between two ethernet ports
    # add_wl_endp
    # add_cx
    # set_wanlink_info side A
    # set_endp_flag side A
    # set_wanlink_info side B
    # set_endp_flag side B

    wanlink = lf_create_wanlink(lf_mgr=args.mgr,
                                lf_port=8080,
                                lf_user=args.lf_user,
                                lf_passwd=args.lf_passwd,
                                debug=True)

    # parameters for add_wl_endp
    # alias
    endp_A = args.wl_name + "-A"
    endp_B = args.wl_name + "-B"

    latency_A = args.latency_A if args.latency_A is not None else args.latency
    latency_B = args.latency_B if args.latency_B is not None else args.latency

    max_rate_A = args.max_rate_A if args.max_rate_A is not None else args.max_rate
    max_rate_B = args.max_rate_B if args.max_rate_B is not None else args.max_rate

    # parameters for set_wanlink_info
    drop_freq_A = args.drop_freq_A if args.drop_freq_A is not None else args.drop_freq
    drop_freq_B = args.drop_freq_B if args.drop_freq_B is not None else args.drop_freq

    dup_freq_A = args.dup_freq_A if args.dup_freq_A is not None else args.dup_freq
    dup_freq_B = args.dup_freq_B if args.dup_freq_B is not None else args.dup_freq

    extra_buffer_A = args.extra_buffer_A if args.extra_buffer_A is not None else args.extra_buffer
    extra_buffer_B = args.extra_buffer_B if args.extra_buffer_B is not None else args.extra_buffer

    jitter_freq_A = args.jitter_freq_A if args.jitter_freq_A is not None else args.jitter_freq
    jitter_freq_B = args.jitter_freq_B if args.jitter_freq_B is not None else args.jitter_freq

    latency_packet_A = args.latency_packet_A if args.latency_packet_A is not None else args.latency_packet
    latency_packet_B = args.latency_packet_B if args.latency_packet_B is not None else args.latency_packet

    max_drop_amt_A = args.max_drop_amt_A if args.max_drop_amt_A is not None else args.max_drop_amt
    max_drop_amt_B = args.max_drop_amt_B if args.max_drop_amt_B is not None else args.max_drop_amt

    max_jitter_A = args.max_jitter_A if args.max_jitter_A is not None else args.max_jitter
    max_jitter_B = args.max_jitter_B if args.max_jitter_B is not None else args.max_jitter

    max_lateness_A = args.max_lateness_A if args.max_lateness_A is not None else args.max_lateness
    max_lateness_B = args.max_lateness_B if args.max_lateness_B is not None else args.max_lateness

    max_reorder_amt_A = args.max_reorder_amt_A if args.max_reorder_amt_A is not None else args.max_reorder_amt
    max_reorder_amt_B = args.max_reorder_amt_B if args.max_reorder_amt_B is not None else args.max_reorder_amt

    min_drop_amt_A = args.min_drop_amt_A if args.min_drop_amt_A is not None else args.min_drop_amt
    min_drop_amt_B = args.min_drop_amt_B if args.min_drop_amt_B is not None else args.min_drop_amt

    min_reorder_amt_A = args.min_reorder_amt_A if args.min_reorder_amt_A is not None else args.min_reorder_amt
    min_reorder_amt_B = args.min_reorder_amt_B if args.min_reorder_amt_B is not None else args.min_reorder_amt

    reorder_freq_A = args.reorder_freq_A if args.reorder_freq_A is not None else args.reorder_freq
    reorder_freq_B = args.reorder_freq_B if args.reorder_freq_B is not None else args.reorder_freq

    speed_A = args.speed_A if args.speed_A is not None else args.speed
    speed_B = args.speed_B if args.speed_B is not None else args.speed

    # Comment out some parameters like 'max_jitter', 'drop_freq' and 'wanlink'
    # in order to view the X-Errors headers

    # create side A
    wanlink.add_wl_endp(_alias=endp_A,                        # Name of endpoint. [R]
                        _cpu_id=args.cpu_id,                  # The CPU/thread that this process should run on (kernel-mode only).
                        _description=args.description,        # Description for this endpoint, put in single quotes if it contains spaces.
                        _latency=latency_A,                   # The latency (ms) that will be added to each packet entering this WanLink.
                        _max_rate=max_rate_A,                 # Maximum transmit rate (bps) for this WanLink.
                        _port=args.port_A,                    # Port number. [W]
                        _resource=args.resource,              # Resource number. [W]
                        _shelf=args.shelf,                    # Shelf name/id. [R][D:1]
                        _wle_flags=args.wle_flags,            # WanLink Endpoint specific flags, see above.
                        _suppress_related_commands=args.suppress_related_commands)

    # endp B
    wanlink.add_wl_endp(_alias=endp_B,                        # Name of endpoint. [R]
                        _cpu_id=args.cpu_id,                  # The CPU/thread that this process should run on (kernel-mode only).
                        _description=args.description,        # Description for this endpoint, put in single quotes if it contains spaces.
                        _latency=latency_B,                   # The latency (ms) that will be added to each packet entering this WanLink.
                        _max_rate=max_rate_B,                 # Maximum transmit rate (bps) for this WanLink.
                        _port=args.port_B,                    # Port number. [W]
                        _resource=args.resource,              # Resource number. [W]
                        _shelf=args.shelf,                    # Shelf name/id. [R][D:1]
                        _wle_flags=args.wle_flags,            # WanLink Endpoint specific flags, see above.
                        _suppress_related_commands=args.suppress_related_commands)

    result = wanlink.add_cx(_alias=args.wl_name,
                            _rx_endp=endp_A,
                            _tx_endp=endp_B,
                            _test_mgr="default_tm")

    logger.debug(pformat(result))

    # set_wanlink_info A
    wanlink.set_wanlink_info(_drop_freq=drop_freq_A,                    # How often, out of 1,000,000 packets, should we
                             # purposefully drop a packet.
                             _dup_freq=dup_freq_A,                     # How often, out of 1,000,000 packets, should we
                             # purposefully duplicate a packet.
                             _extra_buffer=extra_buffer_A,                 # The extra amount of bytes to buffer before
                             # dropping pkts, in units of 1024. Use -1 for AUTO.
                             _jitter_freq=jitter_freq_A,                  # How often, out of 1,000,000 packets, should we
                             # apply jitter.
                             _latency=latency_packet_A,                      # The base latency added to all packets, in
                             # milliseconds (or add 'us' suffix for microseconds
                             _max_drop_amt=max_drop_amt_A,                 # Maximum amount of packets to drop in a row.
                             # Default is 1.
                             _max_jitter=max_jitter_A,                   # The maximum jitter, in milliseconds (or ad 'us'
                             # suffix for microseconds)
                             _max_lateness=max_lateness_A,                 # Maximum amount of un-intentional delay before pkt
                             # is dropped. Default is AUTO
                             _max_reorder_amt=max_reorder_amt_A,              # Maximum amount of packets by which to reorder,
                             # Default is 10.
                             _min_drop_amt=min_drop_amt_A,                 # Minimum amount of packets to drop in a row.
                             # Default is 1.
                             _min_reorder_amt=min_reorder_amt_A,              # Minimum amount of packets by which to reorder,
                             # Default is 1.
                             _name=endp_A,                         # The name of the endpoint we are configuring. [R]
                             _playback_capture_file=args.playback_capture_file,        # Name of the WAN capture file to play back.
                             _reorder_freq=reorder_freq_A,                 # How often, out of 1,000,000 packets, should we
                             # make a packet out of order.
                             _speed=speed_A,                        # The maximum speed of traffic this endpoint will
                             # accept (bps).
                             _debug=args.debug,
                             _suppress_related_commands=args.suppress_related_commands)

    if args.kernel_mode:
        wanlink.set_endp_flag(_name=endp_A,
                            _flag=wanlink.command.SetEndpFlagFlag.KernelMode.value,
                            _val=1,
                            _suppress_related_commands=args.suppress_related_commands)

    else:                                
        wanlink.set_endp_flag(_name=endp_A,
                            _flag=wanlink.command.SetEndpFlagFlag.KernelMode.value,
                            _val=0,
                            _suppress_related_commands=args.suppress_related_commands)

    if args.pass_through_mode:
        wanlink.set_endp_flag(_name=endp_A,
                            _flag='PassthroughMode',
                            _val=1,
                            _suppress_related_commands=args.suppress_related_commands)

    else:                                
        wanlink.set_endp_flag(_name=endp_A,
                            _flag='PassthroughMode',
                            _val=0,
                            _suppress_related_commands=args.suppress_related_commands)


    # set_wanlink_info B
    wanlink.set_wanlink_info(_drop_freq=drop_freq_B,                    # How often, out of 1,000,000 packets, should we
                             # purposefully drop a packet.
                             _dup_freq=dup_freq_B,                     # How often, out of 1,000,000 packets, should we
                             # purposefully duplicate a packet.
                             _extra_buffer=extra_buffer_B,                 # The extra amount of bytes to buffer before
                             # dropping pkts, in units of 1024. Use -1 for AUTO.
                             _jitter_freq=jitter_freq_B,                  # How often, out of 1,000,000 packets, should we
                             # apply jitter.
                             _latency=latency_packet_B,                      # The base latency added to all packets, in
                             # milliseconds (or add 'us' suffix for microseconds
                             _max_drop_amt=max_drop_amt_B,                 # Maximum amount of packets to drop in a row.
                             # Default is 1.
                             _max_jitter=max_jitter_B,                   # The maximum jitter, in milliseconds (or ad 'us'
                             # suffix for microseconds)
                             _max_lateness=max_lateness_B,                 # Maximum amount of un-intentional delay before pkt
                             # is dropped. Default is AUTO
                             _max_reorder_amt=max_reorder_amt_B,              # Maximum amount of packets by which to reorder,
                             # Default is 10.
                             _min_drop_amt=min_drop_amt_B,                 # Minimum amount of packets to drop in a row.
                             # Default is 1.
                             _min_reorder_amt=min_reorder_amt_B,              # Minimum amount of packets by which to reorder,
                             # Default is 1.
                             _name=endp_B,                         # The name of the endpoint we are configuring. [R]
                             _playback_capture_file=args.playback_capture_file,        # Name of the WAN capture file to play back.
                             _reorder_freq=reorder_freq_B,                 # How often, out of 1,000,000 packets, should we
                             # make a packet out of order.
                             _speed=speed_B,                        # The maximum speed of traffic this endpoint will
                             # accept (bps).
                             _debug=args.debug,
                             _suppress_related_commands=args.suppress_related_commands)

    if args.kernel_mode:
        wanlink.set_endp_flag(_name=endp_B,
                            _flag=wanlink.command.SetEndpFlagFlag.KernelMode.value,
                            _val=1,
                            _suppress_related_commands=args.suppress_related_commands)

    else:                                
        wanlink.set_endp_flag(_name=endp_B,
                            _flag=wanlink.command.SetEndpFlagFlag.KernelMode.value,
                            _val=0,
                            _suppress_related_commands=args.suppress_related_commands)
    if args.pass_through_mode:
        wanlink.set_endp_flag(_name=endp_B,
                            _flag='PassthroughMode',
                            _val=1,
                            _suppress_related_commands=args.suppress_related_commands)

    else:                                
        wanlink.set_endp_flag(_name=endp_B,
                            _flag='PassthroughMode',
                            _val=0,
                            _suppress_related_commands=args.suppress_related_commands)


    eid_list = [args.wl_name]
    ewarn_list = []
    result = wanlink.get_wl(_eid_list=eid_list,
                            _wait_sec=0.2,
                            _timeout_sec=2.0,
                            _errors_warnings=ewarn_list)
    logger.debug(pformat(result))

    eid_list = [endp_A, endp_B]
    result = wanlink.get_wl_endp(_eid_list=eid_list,
                            _wait_sec=0.2,
                            _timeout_sec=2.0,
                            _errors_warnings=ewarn_list)
    logger.debug(pformat(result))



if __name__ == "__main__":
    main()
