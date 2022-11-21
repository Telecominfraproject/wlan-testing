#!/usr/bin/env python3
"""
This file is intended to expose concurrency
problems in the /events/ URL handler by inserting events rapidly.
Please concurrently use with event_breaker.py.
"""
import sys
import os
import importlib
from datetime import datetime
from time import sleep
import pprint

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class EventFlood(Realm):
    def __init__(self, host, port,
                 duration=None,
                 pause_ms=None,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, port)
        self.counter = 0
        self.test_duration = duration
        self.pause_ms = pause_ms
        if self.test_duration is None:
            raise ValueError("run wants numeric run_duration_sec")

    def create(self):
        pass

    def run(self):
        last_second_ms = 0
        start_time = datetime.now()
        end_time = self.parse_time(self.test_duration) + start_time
        client_time_ms = 0
        loop_time_ms = 0

        while datetime.now() < end_time:
            sleep(self.pause_ms / 1000)
            start_loop_time_ms = int(self.get_milliseconds(datetime.now()))
            print('\r♦ ', end='')
            response_list = []
            self.json_post("/cli-json/add_event",
                           {
                               "event_id": "new",
                               "details": "event_flood %d" % start_loop_time_ms,
                               "priority": "INFO",
                               "name": "custom"
                           },
                           response_json_list_=response_list)
            if self.debug:
                pprint.pprint(response_list)
            prev_client_time_ms = client_time_ms
            prev_loop_time_ms = loop_time_ms
            now = int(self.get_milliseconds(datetime.now()))
            loop_time_ms = now - start_loop_time_ms

            client_time_ms = response_list[0]["LAST"]["duration"]
            if client_time_ms != prev_client_time_ms:
                print(" client %d ms %d" % (client_time_ms,
                                            (prev_client_time_ms - client_time_ms)),
                      end='')
            if loop_time_ms != prev_loop_time_ms:
                print(" loop %d ms %d                            " % (loop_time_ms,
                                                                      (prev_loop_time_ms - loop_time_ms)),
                      end='')
            if (last_second_ms + 1000) < now:
                last_second_ms = now
                print("")

    def cleanup(self):
        pass


def main():
    parser = LFCliBase.create_bare_argparse(
        prog='event_breaker.py',
        description="""event flood is meant  to be used in conjunction with event breaker
    Please use the event_break_flood.py script""")

    parser.add_argument("--test_duration", help='test duration', default="30s")
    parser.add_argument("--pause_ms", help='interval between submitting events', default="30")
    args = parser.parse_args()

    event_breaker = EventFlood(host=args.mgr,
                               port=args.mgr_port,
                               duration=args.test_duration,
                               pause_ms=int(args.pause_ms),
                               _debug_on=True,
                               _exit_on_error=True,
                               _exit_on_fail=True)
    event_breaker.create()
    event_breaker.run()
    event_breaker.cleanup()


if __name__ == "__main__":
    main()
