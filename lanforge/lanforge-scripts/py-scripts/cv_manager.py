#!/usr/bin/env python3
import sys
import os
import importlib
import argparse

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

cv_test_manager = importlib.import_module("py-json.cv_test_manager")
cv_test = cv_test_manager.cv_test


class CVManager(cv_test):
    def __init__(self,
                 scenario=None,
                 debug=False,
                 lfclient_host='localhost'):
        self.scenario = scenario
        self.debug = debug
        self.exit_on_error = False
        self.lfclient_host = lfclient_host

    def apply_and_build_scenario(self):
        self.apply_cv_scenario(self.scenario)
        self.build_cv_scenario()


def main():
    parser = argparse.ArgumentParser(
        prog='cv_manager.py',
        formatter_class=argparse.RawTextHelpFormatter,
        description='''This is a simple driver script to load a CV Scenario''')
    parser.add_argument('--scenario', help='Scenario you wish to build')
    parser.add_argument('--debug', help='Enable debugging', default=False, action="store_true")
    parser.add_argument('--mgr', default='localhost')

    args = parser.parse_args()

    manager = CVManager(scenario=args.scenario,
                        debug=args.debug,
                        lfclient_host=args.mgr)
    manager.apply_and_build_scenario()


if __name__ == "__main__":
    main()
