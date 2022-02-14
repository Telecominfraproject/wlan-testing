#!/usr/bin/env python3
import sys
import os
import importlib
import argparse
import time

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class TestGroup(Realm):
    def __init__(self, host, port,
                 group_name=None,
                 add_cx_list=None,
                 rm_cx_list=None,
                 tg_action=None,
                 cx_action=None,
                 list_groups=None,
                 show_group=None):
        super().__init__(lfclient_host=host, lfclient_port=port)

        if add_cx_list is None:
            add_cx_list = []
        if rm_cx_list is None:
            rm_cx_list = []
        self.tg_profile = self.new_test_group_profile()
        if group_name is None and list_groups is None and (tg_action is not None or cx_action is not None or
                                                           add_cx_list is not None or rm_cx_list is not None or show_group is not None):
            raise ValueError(
                "Group name must be set if manipulating test groups")
        else:
            self.tg_profile.group_name = group_name

        self.tg_action = tg_action
        self.cx_action = cx_action
        self.list_groups = list_groups
        self.show_group = show_group
        if add_cx_list:
            if len(add_cx_list) == 1 and ',' in add_cx_list[0]:
                self.add_cx_list = add_cx_list[0].split(',')
        else:
            self.add_cx_list = add_cx_list

        if rm_cx_list:
            if len(rm_cx_list) == 1 and ',' in rm_cx_list[0]:
                self.rm_cx_list = rm_cx_list[0].split(',')
        else:
            self.rm_cx_list = rm_cx_list

    def do_cx_action(self):
        if self.cx_action == 'start':
            print("Starting %s" % self.tg_profile.group_name)
            self.tg_profile.start_group()
        elif self.cx_action == 'stop':
            print("Stopping %s" % self.tg_profile.group_name)
            self.tg_profile.stop_group()
        elif self.cx_action == 'quiesce':
            print("Quiescing %s" % self.tg_profile.group_name)
            self.tg_profile.quiesce_group()

    def do_tg_action(self):
        if self.tg_action == 'add':
            print("Creating %s" % self.tg_profile.group_name)
            self.tg_profile.create_group()
        if self.tg_action == 'del':
            print("Removing %s" % self.tg_profile.group_name)
            if self.tg_profile.check_group_exists():
                self.tg_profile.rm_group()
            else:
                print("%s not found, no action taken" %
                      self.tg_profile.group_name)

    def show_info(self):
        time.sleep(.5)
        if self.list_groups:
            tg_list = self.tg_profile.list_groups()
            if len(tg_list) > 0:
                print("Current Test Groups: ")
                for group in tg_list:
                    print(group)
            else:
                print("No test groups found")
        if self.show_group:
            cx_list = self.tg_profile.list_cxs()
            if len(cx_list) > 0:
                print("Showing cxs in %s" % self.tg_profile.group_name)
                for cx in cx_list:
                    print(cx)
            else:
                print("No cxs found in %s" % self.tg_profile.group_name)

    def update_cxs(self):
        if len(self.add_cx_list) > 0:
            print("Adding cxs %s to %s" %
                  (', '.join(self.add_cx_list), self.tg_profile.group_name))
            for cx in self.add_cx_list:
                self.tg_profile.add_cx(cx)
                self.tg_profile.cx_list.append(cx)
        if len(self.rm_cx_list) > 0:
            print("Removing cxs %s from %s" %
                  (', '.join(self.rm_cx_list), self.tg_profile.group_name))
            for cx in self.rm_cx_list:
                self.tg_profile.rm_cx(cx)
                if cx in self.tg_profile.cx_list:
                    self.tg_profile.cx_list.remove(cx)


def main():
    parser = Realm.create_bare_argparse(
        prog='testgroup.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''Control and query test groups\n''',
        description='''testgroup.py
    --------------------
    Generic command example:
    ./testgroup.py --group_name group1 --add_group --add_cx l3_test1,l3_test2 --remove_cx l3_test3 --list_groups
    ./testgroup.py --group_name group1 --add_group --list_groups
    ''')

    parser.add_argument(
        '--group_name', help='specify the name of the test group to use', default=None)
    parser.add_argument('--list_groups', help='list all existing test groups',
                        action='store_true', default=False)

    tg_group = parser.add_mutually_exclusive_group()
    tg_group.add_argument(
        '--add_group', help='add new test group', action='store_true', default=False)
    tg_group.add_argument(
        '--del_group', help='delete test group', action='store_true', default=False)
    parser.add_argument('--show_group', help='show connections in current test group',
                        action='store_true', default=False)

    cx_group = parser.add_mutually_exclusive_group()
    cx_group.add_argument(
        '--start_group', help='start all cxs in chosen test group', default=None)
    cx_group.add_argument(
        '--stop_group', help='stop all cxs in chosen test group', default=None)
    cx_group.add_argument(
        '--quiesce_group', help='quiesce all cxs in chosen test groups', default=None)

    parser.add_argument(
        '--add_cx', help='add cx to chosen test group', nargs='*',  default=[])
    parser.add_argument(
        '--remove_cx', help='remove cx from chosen test group', nargs='*', default=[])

    args = parser.parse_args()

    tg_action = None
    cx_action = None

    if args.add_group:
        tg_action = 'add'
    elif args.del_group:
        tg_action = 'del'

    if args.start_group:
        cx_action = 'start'
    elif args.stop_group:
        cx_action = 'stop'
    elif args.quiesce_group:
        cx_action = 'quiesce'

    tg = TestGroup(host=args.mgr, port=args.mgr_port,
                   group_name=args.group_name,
                   add_cx_list=args.add_cx, rm_cx_list=args.remove_cx, cx_action=cx_action,
                   tg_action=tg_action, list_groups=args.list_groups, show_group=args.show_group)

    tg.do_tg_action()
    tg.update_cxs()
    tg.do_cx_action()
    time.sleep(5)
    tg.show_info()


if __name__ == "__main__":
    main()
