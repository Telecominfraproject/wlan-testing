#!/usr/bin/env python3

"""
    Script for creating a variable number of bridges.
"""
import sys
import os
import importlib
import pprint
import argparse
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

class CreateBridge(Realm):
    def __init__(self, target_device,
                 _host=None,
                 _port=None,
                 _bridge_list=None,
                 _debug_on=False):
        super().__init__(_host,
                         _port)
        self.host = _host
        self.port = _port
        self.bridge_list = _bridge_list
        self.debug = _debug_on
        self.target_device = target_device

        eid = self.name_to_eid(self.bridge_list[0])
        self.shelf = eid[0]
        self.resource = eid[1]
        self.bridge_name = eid[2]

    def build(self):
        # Build bridges
        eid_str = "%s.%s.%s" % (1, self.resource, self.bridge_name)
        nd = False
        for td in self.target_device.split(","):
            eid = self.name_to_eid(td)
            if not nd:
                nd = eid[2]
            else:
                nd += ","
                nd += eid[2]

        data = {
            "shelf": self.shelf,
            "resource": self.resource,
            "port": self.bridge_name,
            "network_devs": nd # eth1,eth2
        }
        self.json_post("cli-json/add_br", data)

        bridge_set_port = {
            "shelf": self.shelf,
            "resource": self.resource,
            "port": self.bridge_name,
            "current_flags": 0x80000000,
            # (0x2 + 0x4000 + 0x800000)  # current, dhcp, down
            "interest": 0x4000
        }
        self.json_post("cli-json/set_port", bridge_set_port)


        if LFUtils.wait_until_ports_admin_up(base_url=self.lfclient_url,
                                             port_list=[eid_str],
                                             debug_=self.debug):
            self._pass("Bond interface went admin up.")
        else:
            self._fail("Bond interface did NOT go admin up.")

    def cleanup(self):
        eid = "%s.%s.%s" % (self.shelf, self.resource, self.bridge_name)
        self.rm_port(eid, check_exists=False, debug_=self.debug)
        if LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=[eid], debug=self.debug):
            self._pass("Ports successfully cleaned up.")
        else:
            self._fail("Ports NOT successfully cleaned up.")

def main():
    parser = LFCliBase.create_basic_argparse(
        prog='create_bridge.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
         Create bridges
            ''',

        description='''\
        create_bridge.py
--------------------
Command example:
./create_bridge.py
    --bridge_name br0
    --target_device eth1,eth2
    --debug
            ''')
    required = parser.add_argument_group('required arguments')

    required.add_argument('--bridge_name', help='Name of the bridge to create', required=True)
    required.add_argument('--target_device', help='The interfaces the bridge should contain', required=True)

    args = parser.parse_args()
    # if args.debug:
    #    pprint.pprint(args)
    #    time.sleep(5)

    logger_config = lf_logger_config.lf_logger_config()
    # set the logger level to requested value
    logger_config.set_level(level=args.log_level)
    logger_config.set_json(json_file=args.lf_logger_config_json)

    # This code supports creating only single bridge at a time
    bridge_list = [args.bridge_name]

    create_bridge = CreateBridge(_host=args.mgr,
                                 _port=args.mgr_port,
                                 _bridge_list=bridge_list,
                                 _debug_on=args.debug,
                                 target_device=args.target_device)

    create_bridge.build()
    logger.info('Created bridge: %s' % bridge_list[0])

    if not args.noclean:
        sleep(5)

        create_bridge.cleanup()

    if create_bridge.passes():
        create_bridge.exit_success()
    else:
        create_bridge.exit_fail()

if __name__ == "__main__":
    main()
