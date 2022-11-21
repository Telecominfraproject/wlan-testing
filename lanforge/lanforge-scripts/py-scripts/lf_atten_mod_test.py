#!/usr/bin/env python3
"""
NAME: lf_atten_mod_test.py

PURPOSE:
This program is used to modify the LANforge attenuator (through the LANforge manager/server processes) by using create() method.
You can check the attenuator details and serial number by using show() method.

EXAMPLE:
Run with all serial number and module: python3 lf_atten_mod_test.py -hst 192.168.200.12  -atten_serno all --atten_idx all --atten_val 220
Run with particular serial number(2222) and module(2): python3 lf_atten_mod_test.py -hst 192.168.200.12  -atten_serno 2222 --atten_idx 3 --atten_val 220

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
import logging


if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

realm = importlib.import_module("py-json.realm")
Realm = realm.Realm

logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")



class CreateAttenuator(Realm):
    def __init__(self, host, port, serno, idx, val,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, port, debug_=_debug_on, _exit_on_fail=_exit_on_fail)
        self.host = host
        self.serno = serno
        self.idx = idx
        self.val = val
        self.attenuator_profile = self.new_attenuator_profile()
        self.attenuator_profile.atten_idx = self.idx
        self.attenuator_profile.atten_val = self.val
        self.attenuator_profile.atten_serno = self.serno

    def build(self):
        self.attenuator_profile.create()
        self.attenuator_profile.show()


def main():
    # create_basic_argparse defined in lanforge-scripts/py-json/LANforge/lfcli_base.py
    parser = Realm.create_basic_argparse(
        prog='lf_atten_mod_test.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=None,
        description='''\
            lf_atten_mod_test.py
            --------------------
        set and show Attenuator:
        python3 lf_atten_mod_test.py --hst 192.168.200.12  --atten_serno all --atten_idx 7 --atten_val 220
                ''')

    parser.add_argument('-hst', '--host', help='host name', default='192.168.200.12')
    # basic_argparser contains --port option
    # Realm requires a port to be passed in 
    parser.add_argument('-atten_serno', '--atten_serno', help='Serial number for requested Attenuator, or \'all\'', default=2222)
    parser.add_argument('-atten_idx', '--atten_idx', help='Attenuator index eg. For module 1 = 0,module 2 = 1', default=7)
    parser.add_argument('-atten_val', '--atten_val', help='Requested attenuation in 1/10ths of dB (ddB).', default=550)
    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()
    # set the logger level to requested value
    logger_config.set_level(level=args.log_level)
    logger_config.set_json(json_file=args.lf_logger_config_json)


    # TODO the attenuator does not need port need to clean up. 5/5/22
    args.port = 8080
    atten_mod_test = CreateAttenuator(host=args.host, port=args.port, serno=args.atten_serno, idx=args.atten_idx, val=args.atten_val, _debug_on=args.debug)
    atten_mod_test.build()


if __name__ == "__main__":
    main()
