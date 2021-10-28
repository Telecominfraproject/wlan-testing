#!/usr/bin/env python3
"""
This file is intended to expose concurrency
problems in the /events/ URL handler by inserting events rapidly.
Please concurrently use with event_breaker.py.
"""
import sys
import os
import importlib
import argparse
from datetime import datetime
from time import sleep

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class EventBreaker(Realm):
    def __init__(self,  host, port,
                 duration=None,
                 pause_ms=None,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, port)
        self.counter = 0
        self.test_duration = duration
        self.pause_ms = pause_ms
        if (self.test_duration is None):
            raise ValueError("run wants numeric run_duration_sec")

    def create(self):
        pass

    def run(self):
        last_second_ms = 0
        start_time = datetime.now()
        now_ms = 0
        end_time = self.parse_time(self.test_duration) + start_time
        client_time_ms = 0
        prev_client_time_ms = 0
        start_loop_time_ms = 0
        loop_time_ms = 0
        prev_loop_time_ms = 0
        num_events = 0
        prev_num_events = 0

        while datetime.now() < end_time:
            sleep( self.pause_ms / 1000 )
            start_loop_time_ms = int(self.get_milliseconds(datetime.now()))
            print ('\r♦ ', end='')
            #prev_loop_time_ms = loop_time_ms
            # loop_time_ms = self.get_milliseconds(datetime.now())
            prev_client_time_ms = client_time_ms
            response_list = []
            response = self.json_post("/cli-json/add_event",
                                      {
                                          "event_id": "new",
                                          "details": "event_flood %d"%start_loop_time_ms,
                                          "priority": "INFO",
                                          "name": "custom"
                                      },
                                      response_json_list_=response_list)
            # pprint.pprint(response_list)
            prev_client_time_ms = client_time_ms
            prev_loop_time_ms = loop_time_ms
            now = int(self.get_milliseconds(datetime.now()))
            loop_time_ms = now - start_loop_time_ms

            client_time_ms = response_list[0]["LAST"]["duration"]
            if (client_time_ms != prev_client_time_ms):
                print(" client %d ms %d"%(client_time_ms,
                                          (prev_client_time_ms - client_time_ms)),
                      end='')
            if (loop_time_ms != prev_loop_time_ms):
                print(" loop %d ms %d                            "%(loop_time_ms,
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
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--test_duration", help='test duration', default="30s" )
    parser.add_argument("--pause_ms", help='interval between submitting events', default="30" )
    # if optional_args is not None:
    args = parser.parse_args()

    event_breaker = EventBreaker(host=args.mgr,
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
