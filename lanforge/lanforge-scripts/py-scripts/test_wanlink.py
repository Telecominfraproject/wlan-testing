#!/usr/bin/env python3
# Create and modify WAN Links from the command line.
# Written by Candela Technologies Inc.
# Updated by: Erin Grimes
"""
sample command:
./test_wanlink.py --name my_wanlink4 --latency_A 20 --latency_B 69 --rate 1000 --jitter_A 53 --jitter_B 73 --jitter_freq 6 --drop_A 12 --drop_B 11
"""
import sys
import os
import importlib
import argparse

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
create_wanlink = importlib.import_module("py-json.create_wanlink")


class LANtoWAN(Realm):
    def __init__(self, args):
        super().__init__(args['host'], args['port'])
        self.args = args
        self._debug_on = False
        self._exit_on_error = False
        self._exit_on_fail = False

    def create_wanlinks(self):
        print("Creating wanlinks")
        create_wanlink.main(self.args)

    def cleanup(self): pass


def main():
    parser = LFCliBase.create_basic_argparse(
        prog='test_wanlink.py',
        formatter_class=argparse.RawTextHelpFormatter)

    optional_args = None
    for group in parser._action_groups:
        if group.title == "optional arguments":
            optional_args = group
            break
    if optional_args is not None:
        optional_args.add_argument('--name', help='The name of the wanlink', default="wl_eg1")
        optional_args.add_argument('--port_A', help='Endpoint A', default="eth1")
        optional_args.add_argument('--port_B', help='Endpoint B', default="eth2")
        optional_args.add_argument('--rate', help='The maximum rate of transfer at both endpoints (bits/s)', default=1000000)
        optional_args.add_argument('--rate_A', help='The max rate of transfer at endpoint A (bits/s)', default=None)
        optional_args.add_argument('--rate_B', help='The maximum rate of transfer (bits/s)', default=None)
        optional_args.add_argument('--latency', help='The delay of both ports', default=20)
        optional_args.add_argument('--latency_A', help='The delay of port A', default=None)
        optional_args.add_argument('--latency_B', help='The delay of port B', default=None)
        optional_args.add_argument('--jitter', help='The max jitter of both ports (ms)', default=None)
        optional_args.add_argument('--jitter_A', help='The max jitter of port A (ms)', default=None)
        optional_args.add_argument('--jitter_B', help='The max jitter of port B (ms)', default=None)
        optional_args.add_argument('--jitter_freq', help='The jitter frequency of both ports (%%)', default=None)
        optional_args.add_argument('--jitter_freq_A', help='The jitter frequency of port A (%%)', default=None)
        optional_args.add_argument('--jitter_freq_B', help='The jitter frequency of port B (%%)', default=None)
        optional_args.add_argument('--drop', help='The drop frequency of both ports (%%)', default=None)
        optional_args.add_argument('--drop_A', help='The drop frequency of port A (%%)', default=None)
        optional_args.add_argument('--drop_B', help='The drop frequency of port B (%%)', default=None)
        # todo: packet loss A and B
        # todo: jitter A and B
    parseargs = parser.parse_args()
    args = {
        "host": parseargs.mgr,
        "port": parseargs.mgr_port,
        "name": parseargs.name,
        "port_A": parseargs.port_A,
        "port_B": parseargs.port_B,
        "latency": parseargs.latency,
        "latency_A": (parseargs.latency_A if parseargs.latency_A is not None else parseargs.latency),
        "latency_B": (parseargs.latency_B if parseargs.latency_B is not None else parseargs.latency),
        "rate": parseargs.rate,
        "rate_A": (parseargs.rate_A if parseargs.rate_A is not None else parseargs.rate),
        "rate_B": (parseargs.rate_B if parseargs.rate_B is not None else parseargs.rate),
        "jitter": parseargs.jitter,
        "jitter_A": (parseargs.jitter_A if parseargs.jitter_A is not None else parseargs.jitter),
        "jitter_B": (parseargs.jitter_B if parseargs.jitter_B is not None else parseargs.jitter),
        "jitter_freq": parseargs.jitter,
        "jitter_freq_A": (parseargs.jitter_freq_A if parseargs.jitter_freq_A is not None else parseargs.jitter_freq),
        "jitter_freq_B": (parseargs.jitter_freq_B if parseargs.jitter_freq_B is not None else parseargs.jitter_freq),
        "drop": parseargs.drop,
        "drop_A": (parseargs.drop_A if parseargs.drop_A is not None else parseargs.drop),
        "drop_B": (parseargs.drop_B if parseargs.drop_B is not None else parseargs.drop),
    }
    ltw = LANtoWAN(args)
    ltw.create_wanlinks()
    ltw.cleanup()


if __name__ == "__main__":
    main()
