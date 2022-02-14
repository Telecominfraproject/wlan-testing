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

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class LoadScenario(Realm):
    def __init__(self,
                 mgr='localhost',
                 mgr_port=8080,
                 scenario=None,
                 action='overwrite',
                 clean_dut=True,
                 clean_chambers=True,
                 start=None,
                 stop=None,
                 quiesce=None,
                 timeout=120,
                 debug=False):
        super().__init__(lfclient_host=mgr,
                         lfclient_port=mgr_port,
                         debug_=debug)
        self.mgr = mgr
        self.scenario = scenario
        self.action = action
        self.clean_dut = clean_dut
        self.clean_chambers = clean_chambers
        self.start = start
        self.stop = stop
        self.quiesce = quiesce
        self.timeout = timeout
        self.BuildVersion = self.json_get('/')['VersionInfo']['BuildVersion']
        self.starting_events = 1
        self.add_event("Starting Scenario.py")

    def are_any_ports_phantom(self):
        ports = self.json_get('/ports')['interfaces']
        for port in ports:
            port = list(port.values())[0]
            if port['phantom']:
                return True
        return False

    def is_port_phantom(self, port_eid):
        if not port_eid:
            return False
        port = self.name_to_eid(port_eid)
        port_data = self.json_get('/ports/%s/%s/%s' % (port[0], port[1], port[2]))
        if 'interface' in port_data.keys():
            if port_data['interface']['phantom']:
                print('%s is phantom' % port_eid)
                return True
        else:
            for port in port_data['interfaces']:
                if 'phantom' in port.keys():
                    if port['phantom']:
                        print('%s is phantom' % port)
                        return True

        return False

    def start_test(self):
        self.starting_events = self.json_get('/events/last/1')['event']['id']

    def load_scenario(self):
        if self.scenario is not None:
            data = {
                "name": self.scenario,
                "action": self.action,
                "clean_dut": "no",
                "clean_chambers": "no"
            }
            if self.clean_dut:
                data['clean_dut'] = "yes"
            if self.clean_chambers:
                data['clean_chambers'] = "yes"
            print("Loading database %s" % self.scenario)
            self.json_post("/cli-json/load", data)
        elif self.start is not None:
            print("Starting test group %s..." % self.start)
            self.json_post("/cli-json/start_group", {"name": self.start})
        elif self.stop is not None:
            print("Stopping test group %s..." % self.stop)
            self.json_post("/cli-json/stop_group", {"name": self.stop})
        elif self.quiesce is not None:
            print("Quiescing test group %s..." % self.quiesce)
            self.json_post("/cli-json/quiesce_group", {"name": self.quiesce})

    def check_if_complete(self):
        completed = False
        timer = 0
        while not completed:
            new_events = self.find_new_events(self.starting_events)
            target_events = [event for event in self.get_events(new_events, 'event description') if
                             event.startswith('LOAD COMPLETED')]
            if 'LOAD-DB:  Load attempt has been completed.' in self.get_events(new_events, 'event description'):
                completed = True
                print('Scenario %s fully loaded after %s seconds' % (self.scenario, timer))
            elif len(target_events) > 0:
                completed = True
                print('Scenario %s fully loaded after %s seconds' % (self.scenario, timer))
            else:
                timer += 1
                time.sleep(1)
                if timer > self.timeout:
                    completed = True
                    print('Scenario failed to load after %s seconds' % self.timeout)
                else:
                    print('Waiting %s out of %s seconds to load scenario %s' % (timer, self.timeout, self.scenario))
        if self.debug:
            print(self.json_get('/port'))


def main():
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
    parser.add_argument('--timeout', help='Stop trying to load scenario after this many seconds', default=120)
    parser.add_argument('--quit_on_phantom', help='do not load the database if a phantom port is present', action='store_true')
    parser.add_argument('--check_phantom', help='check if these ports are phantom', default=None, nargs="+")
    args = parser.parse_args()

    scenario = LoadScenario(mgr=args.mgr,
                            scenario=args.load,
                            action=args.action,
                            clean_dut=args.clean_dut,
                            clean_chambers=args.clean_chambers,
                            start=args.start,
                            stop=args.stop,
                            quiesce=args.quiesce,
                            timeout=args.timeout,
                            debug=args.debug)
    if args.check_phantom:
        for port in args.check_phantom:
            if scenario.is_port_phantom(port):
                print('%s is phantom' % port)

    if args.quit_on_phantom:
        if scenario.are_any_ports_phantom():
            raise EnvironmentError("There are phantom ports on your LANforge")

    build_version = [int(n) for n in scenario.BuildVersion.split('.')]

    if build_version >= [5, 4, 4]:
        scenario.start_test()

    scenario.load_scenario()

    if build_version < [5, 4, 4]:
        print('sleeping 30 seconds, please upgrade your LANforge for a better experience, more information at https://www.candelatech.com/downloads.php#releases')
        time.sleep(30)

    if build_version >= [5, 4, 4]:
        scenario.check_if_complete()

    # scenario_loader.load_scenario()


if __name__ == '__main__':
    main()
