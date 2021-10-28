#!/usr/bin/env python3
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


parser = LFCliBase.create_bare_argparse(
    prog='scenario.py',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog='''Load a database file and control test groups\n''',
    description='''scenario.py
--------------------
Generic command example:
scenario.py --load db1 --action overwrite --clean_dut --clean_chambers

scenario.py --start test_group1

scenario.py --quiesce test_group1

scenario.py --stop test_group1
''')

group = parser.add_mutually_exclusive_group()

parser.add_argument('--load', help='name of database to load', default=None)

parser.add_argument('--action', help='action to take with database {overwrite | append}', default="overwrite")

parser.add_argument('--clean_dut',
                    help='use to cleanup DUT will be when overwrite is selected, otherwise they will be kept',
                    action="store_true")

parser.add_argument('--clean_chambers',
                    help='use to cleanup Chambers will be when overwrite is selected, otherwise they will be kept',
                    action="store_true")

group.add_argument('--start', help='name of test group to start', default=None)
group.add_argument('--quiesce', help='name of test group to quiesce', default=None)
group.add_argument('--stop', help='name of test group to stop', default=None)
args = parser.parse_args()

local_realm = realm.Realm(lfclient_host=args.mgr, lfclient_port=args.mgr_port, debug_=args.debug)

if args.load is not None:
    data = {
        "name": args.load,
        "action": args.action,
        "clean_dut": "no",
        "clean_chambers": "no"
    }
    if args.clean_dut:
        data['clean_dut'] = "yes"
    if args.clean_chambers:
        data['clean_chambers'] = "yes"
    print("Loading database %s" % args.load)
    local_realm.json_post("/cli-json/load", data)

elif args.start is not None:
    print("Starting test group %s..." % args.start)
    local_realm.json_post("/cli-json/start_group", {"name": args.start})
elif args.stop is not None:
    print("Stopping test group %s..." % args.stop)
    local_realm.json_post("/cli-json/stop_group", {"name": args.stop})
elif args.quiesce is not None:
    print("Quiescing test group %s..." % args.quiesce)
    local_realm.json_post("/cli-json/quiesce_group", {"name": args.quiesce})
