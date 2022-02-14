#!/usr/bin/env python3
"""
NAME: attenuator_mon.py

PURPOSE: example of a monitoring loop that notices when attenator values change

EXAMPLE:

NOTES:


"""
import sys

if sys.version_info[0] != 3:
    print("This script requires Python3")
    exit()

sys.path.insert(1, "../../py-json")
import argparse
import importlib
import os
from os.path import exists
import pprint
from time import sleep


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../../")))
lfcli_base = importlib.import_module('py-json.LANforge.lfcli_base')
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module('py-json.LANforge.LFUtils')
realm = importlib.import_module('py-json.realm')
Realm = realm.Realm

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase


class AttenuatorMonitor(Realm):
    def __init__(self,
                 host=None,
                 port=None,
                 action=None,
                 action_every_channel=False,
                 attenuator=None,
                 interval_sec: float = 1.0,
                 stop_file=None,
                 _deep_clean=False,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host,
                         port,
                         debug_=_debug_on,
                         _exit_on_fail=_exit_on_fail)
        self.action = action
        self.action_every_channel = action_every_channel
        self.attenuator = attenuator
        self.interval_sec = interval_sec
        self.stop_file = stop_file

        self.prev_values = {
            "module 1": 0.0,
            "module 2": 0.0,
            "module 3": 0.0,
            "module 4": 0.0,
            "module 5": 0.0,
            "module 6": 0.0,
            "module 7": 0.0,
            "module 8": 0.0,
        }
        # check for attenuator

        response = self.json_get("/atten/list")
        if "attenuator" not in response:
            if "attenuators" not in response:
                print("Unable to retrieve list of attenuators. Is a LANforge GUI at %s:%s ?"
                      % (host, port))
                exit(1)

        found = False
        if "attenuator" in response:
            if response["attenuator"]["entity id"] != self.attenuator:
                print("Unable to find attenuator %s" % self.attenuator)
                pprint.pprint(("reponse", response))
                exit(1)
            else:
                found = True
        elif "attenuators" in response:
            atten_list = response["attenuators"]
            for atten_o in atten_list:
                for key_1 in atten_o.keys():
                    if atten_o[key_1]["entity id"] == self.attenuator:
                        found = True
        else:
            print("No attenators on system.")
            exit(1)
        if not found:
            print("No matching attenuators found.")
            exit(1)

        self.attenuator_url = "/atten/" + self.attenuator

    def run(self):
        if self.stop_file is not None:
            if exists(self.stop_file):
                print("Stop File [%s] already exists. Remove file before starting script." % self.stop_file)
                exit(0)
        else:
            print("No stop file provided. Stop this script with ctrl-c or kill")

        counter = 0;
        while(True):
            sleep(self.interval_sec)
            if exists(self.stop_file):
                return
            num_changes = 0
            changes = {}
            attenuator_values = self.json_get(self.attenuator_url)
            z_old: float
            z_new: float

            for key in self.prev_values.keys():

                if key not in attenuator_values["attenuator"]:
                    pprint.pprint(attenuator_values["attenuator"])
                    raise ValueError("Unexpected lack of keys for attenuator record:")
                if self.debug:
                    print("I see: %s -> %s" % (self.prev_values[key], attenuator_values["attenuator"][key]))

                if "" == attenuator_values["attenuator"][key]:
                    continue

                z_old = float(self.prev_values[key])
                z_new = float(attenuator_values["attenuator"][key])

                changes[key] = 0
                if z_old != z_new:
                    if (counter > 0) and self.action_every_channel:
                        self.do_cmd(channel=key, value=z_new)
                    else:
                        changes[key] = str(z_new)
                        num_changes += 1
                    self.prev_values[key] = z_new

            if (counter > 0) and (num_changes > 0) and (not self.action_every_channel):
                self.do_cmd(channel="all",
                            value=",".join(changes.values()))
            if exists(self.stop_file):
                return
            counter += 1

    def do_cmd(self,
               channel=None,
               value=None):
        if not channel:
            raise ValueError("do_cmd not given channel")
        if not value:
            raise ValueError("do_cmd not given value")
        if not self.action:
            raise ValueError("do_cmd lost self.action")

        pprint.pprint([("channel", channel),
                       ("values", value)])
        os.system(self.action)

def main():
    parser = LFCliBase.create_bare_argparse(
        prog=__file__,
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
""")
    parser.add_argument('--action', help="command to execute when attenuator changes levels")
    parser.add_argument('--action_every_channel', help="When True, do an action for every channel that changes")
    parser.add_argument('--attenuator', help="attenuator entity id to watch; E.G.: 1.1.323")
    parser.add_argument('--interval_sec', type=float, help="wait between checking")
    parser.add_argument('--stop_file', help="when this file appears, exit; E.G.: /tmp/stop-monitoring")

    args = parser.parse_args()

    if (not args.action) or ("" == args.action):
        print("--action is required; how about 'echo hi' ?")
        exit(1)
    attenuator_mon = AttenuatorMonitor(args.mgr,
                                       args.mgr_port,
                                       attenuator=args.attenuator,
                                       action=args.action,
                                       action_every_channel=args.action_every_channel,
                                       interval_sec=args.interval_sec,
                                       stop_file=args.stop_file,
                                       _debug_on=False,
                                       _exit_on_error=False,
                                       _exit_on_fail=False)
    attenuator_mon.run()


if __name__ == "__main__":
    main()
