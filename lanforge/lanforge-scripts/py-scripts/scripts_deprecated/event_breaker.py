#!/usr/bin/env python3
"""
This file is intended to expose concurrency
problems in the /events/ URL handler by querying events rapidly.
Please use concurrently with event_flood.py.
"""
import sys
import os
import importlib
from datetime import datetime
import pprint

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class EventBreaker(Realm):
    def __init__(self, host, port,
                 duration=None,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, port)
        self.counter = 0
        self.test_duration = duration
        if self.test_duration is None:
            raise ValueError("run wants numeric run_duration_sec")

    def create(self):
        pass

    def run(self):

        now = datetime.now()
        end_time = self.parse_time(self.test_duration) + now
        client_time_ms = 0
        loop_time_ms = 0
        num_events = 0
        while datetime.now() < end_time:
            bad_events = []
            start_loop_time_ms = int(self.get_milliseconds(datetime.now()))
            print('\r♦ ', end='')
            prev_client_time_ms = client_time_ms
            response = self.json_get("/events/all")
            if self.debug:
                pprint.pprint(response)

            if "events" not in response:
                pprint.pprint(response)
                raise AssertionError("no events in response")
            events = response["events"]
            prev_num_events = num_events
            num_events = len(events)
            if num_events != prev_num_events:
                print("%s events Δ%s" % (num_events, (num_events - prev_num_events)))
            if "candela.lanforge.HttpEvents" in response:
                client_time_ms = float(response["candela.lanforge.HttpEvents"]["duration"])
                if self.debug:
                    print(" client_time %d" % client_time_ms)

            if abs(prev_client_time_ms - client_time_ms) > 30:
                print(" client time %d ms Δ%d" % (client_time_ms, (prev_client_time_ms - client_time_ms)),
                      end='')
            event_index = 0
            for record in events:

                for k in record.keys():
                    if record[k] is None:
                        print(' ☠no %s☠' % k, end='')
                        continue
                    if self.debug:
                        pprint.pprint(record[k])
                    if "NA" == record[k]["event"] \
                            or "NA" == record[k]["name"] \
                            or "NA" == record[k]["type"] \
                            or "NA" == record[k]["priority"]:
                        bad_events.append(int(k))
                        pprint.pprint(record[k])
                        if self.debug:
                            print(" ☠id[%s]☠" % k, end='')
            if len(bad_events) > 0:
                pprint.pprint(events[event_index])
                print(" ☠id[%s]☠" % bad_events, end='')
                exit(1)
            event_index += 1
            prev_loop_time_ms = loop_time_ms
            now_ms = int(self.get_milliseconds(datetime.now()))
            loop_time_ms = now_ms - start_loop_time_ms
            if (prev_loop_time_ms - loop_time_ms) > 15:
                print(" loop time %d ms Δ%d                                   "
                      % (loop_time_ms, (prev_loop_time_ms - loop_time_ms)),
                      end='')
            if (prev_loop_time_ms - loop_time_ms) > 30:
                print("")

    def cleanup(self):
        pass


def main():
    parser = LFCliBase.create_bare_argparse(
        prog='event_breaker.py',
        description="""event breaker is meant  to be used in conjunction with event flood
    Please use the event_break_flood.py script""")

    parser.add_argument("--test_duration", help='test duration', default="30s")
    args = parser.parse_args()

    event_breaker = EventBreaker(host=args.mgr,
                                 port=args.mgr_port,
                                 duration=args.test_duration,
                                 _debug_on=True,
                                 _exit_on_error=True,
                                 _exit_on_fail=True)
    event_breaker.create()
    event_breaker.run()
    event_breaker.cleanup()


if __name__ == "__main__":
    main()
