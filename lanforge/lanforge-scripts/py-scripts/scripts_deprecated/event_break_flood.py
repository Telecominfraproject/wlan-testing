#!/usr/bin/python3

import threading
from event_flood import EventFlood
from event_breaker import EventBreaker
import importlib
import sys
import os

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase


def event_break(args):
    event_breaker = EventBreaker(host=args.mgr,
                                 port=args.mgr_port,
                                 duration='30s')
    event_breaker.create()
    event_breaker.run()
    event_breaker.cleanup()


def event_flooding(args):
    event_flood = EventFlood(host=args.mgr,
                             port=args.mgr_port,
                             duration='30s',
                             pause_ms=30)
    event_flood.create()
    event_flood.run()
    event_flood.cleanup()


def main():
    parser = LFCliBase.create_bare_argparse()
    args = parser.parse_args()
    flood = threading.Thread(target=event_flooding(args))
    breaker = threading.Thread(target=event_break(args))

    flood.start()
    breaker.start()


if __name__ == "__main__":
    main()
