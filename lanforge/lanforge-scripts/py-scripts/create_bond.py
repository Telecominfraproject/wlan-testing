#!/usr/bin/env python3

"""create_bond.py Script to create a bond

This script can be used to create a bond, only one can be created at a time. Network devices must be specified
as a list of comma-separated items with no spaces.

Use './create_bond.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""
import sys
import os
import importlib
import argparse
import time
import logging
from time import sleep

logger = logging.getLogger(__name__)

if sys.version_info[0] != 3:
    logger.critical("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")


class CreateBond(Realm):
    def __init__(self, _network_dev_list=None,
                 _host=None,
                 _port=None,
                 _eid=None,
                 _debug_on=False):
        super().__init__(_host, _port)
        self.host = _host
        self.timeout = 120
        self.debug = _debug_on
        self.network_dev_list = _network_dev_list

        eid = self.name_to_eid(_eid)
        self.shelf = eid[0]
        self.resource = eid[1]
        self.bond_name = eid[2]

    def build(self):
        eid = "%s.%s.%s" % (self.shelf, self.resource, self.bond_name)
        nd = False
        for td in self.network_dev_list.split(","):
            e2 = self.name_to_eid(td)
            if not nd:
                nd = e2[2]
            else:
                nd += ","
                nd += e2[2]

        data = {
            'shelf': self.shelf,
            'resource': self.resource,
            'port': self.bond_name,
            'network_devs': nd
        }
        self.json_post("cli-json/add_bond", data)
        #time.sleep(3)
        bond_set_port = {
            "shelf": self.shelf,
            "resource": self.resource,
            "port": self.bond_name,
            "current_flags": 0x80000000,
            # (0x2 + 0x4000 + 0x800000)  # current, dhcp, down
            "interest": 0x4000
        }
        self.json_post("cli-json/set_port", bond_set_port)

        if LFUtils.wait_until_ports_admin_up(base_url=self.lfclient_url,
                                             port_list=[eid],
                                             debug_=self.debug):
            self._pass("Bond interface went admin up.")
        else:
            self._fail("Bond interface did NOT go admin up.")

    def cleanup(self):
        eid = "%s.%s.%s" % (self.shelf, self.resource, self.bond_name)
        self.rm_port(eid, check_exists=False, debug_=self.debug)
        if LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=[eid], debug=self.debug):
            self._pass("Ports successfully cleaned up.")
        else:
            self._fail("Ports NOT successfully cleaned up.")

def main():
    parser = LFCliBase.create_basic_argparse(
        prog='create_bond.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
         Create bonds
            ''',

        description='''\
        create_bond.py
--------------------
Command example:
./create_bond.py
    --bond_name bond0
    --network_dev_list eth0,eth1
    --noclean
    --debug
            ''')

    required = parser.add_argument_group('required arguments')

    required.add_argument('--bond_name', help='Name of the bridge to create', required=True)
    required.add_argument('--network_dev_list', help='list of network devices in the bond, must be comma separated '
                          'with no spaces', required=True)

    args = parser.parse_args()

    logger_config = lf_logger_config.lf_logger_config()
    # set the logger level to requested value
    logger_config.set_level(level=args.log_level)
    logger_config.set_json(json_file=args.lf_logger_config_json)

    create_bond = CreateBond(_host=args.mgr,
                             _port=args.mgr_port,
                             _eid = args.bond_name,
                             _network_dev_list=args.network_dev_list,
                             _debug_on=args.debug
                             )
    create_bond.build()

    if not args.noclean:
        sleep(5)

        create_bond.cleanup()

    if create_bond.passes():
        create_bond.exit_success()
    else:
        create_bond.exit_fail()

if __name__ == "__main__":
    main()
