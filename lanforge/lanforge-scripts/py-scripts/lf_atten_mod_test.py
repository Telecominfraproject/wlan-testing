#!/usr/bin/env python3
"""
NAME: lf_atten_mod_test.py

PURPOSE:
This program is used to modify the LANforge attenuator (through the LANforge manager/server processes) by using create() method.
You can check the attenuator details and serial number by using show() method.

EXAMPLE:
Run with all serial number and module: python3 lf_atten_mod_test.py -hst 192.168.200.12 -port 8080 -atten_serno all --atten_idx all --atten_val 220
Run with particular serial number(2222) and module(2): python3 lf_atten_mod_test.py -hst 192.168.200.12 -port 8080 -atten_serno 2222 --atten_idx 3 --atten_val 220

"atten_serno" = serial number
"atten_idx" = module name


Use './lf_atten_mod_test.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
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


class CreateAttenuator(LFCliBase):
    def __init__(self, host, port, serno, idx, val,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, port, _local_realm=realm.Realm(host, port), _debug=_debug_on, _exit_on_fail=_exit_on_fail)
        self.host = host
        self.port = port
        self.serno = serno
        self.idx = idx
        self.val = val
        self.attenuator_profile = self.local_realm.new_attenuator_profile()
        self.attenuator_profile.atten_idx = self.idx
        self.attenuator_profile.atten_val = self.val
        self.attenuator_profile.atten_serno = self.serno

    def build(self):
        self.attenuator_profile.create()
        self.attenuator_profile.show()

def main():
    parser = LFCliBase.create_basic_argparse(
        prog='lf_atten_mod_test.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=None,
        description='''\
            lf_atten_mod_test.py
            --------------------
        set and show Attenuator:
        python3 lf_atten_mod_test.py -hst 192.168.200.12 -port 8080 -atten_serno all --atten_idx all --atten_val 220
                ''')

    parser.add_argument('-hst', '--host', help='host name', default='192.168.200.12')
    parser.add_argument('-port', '--port', help='port name', default=8080)
    parser.add_argument('-atten_serno', '--atten_serno', help='Serial number for requested Attenuator, or \'all\'', default=2222)
    parser.add_argument('-atten_idx', '--atten_idx', help='Attenuator index eg. For module 1 = 0,module 2 = 1', default='all')
    parser.add_argument('-atten_val', '--atten_val', help='Requested attenution in 1/10ths of dB (ddB).', default=550)
    args = parser.parse_args()

    atten_mod_test = CreateAttenuator(host=args.host, port=args.port, serno=args.atten_serno, idx=args.atten_idx, val=args.atten_val)
    atten_mod_test.build()


if __name__ == "__main__":
    main()
