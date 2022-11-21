#!/usr/bin/env python3
"""
NAME: lf_modify_radio.py

PURPOSE: Set the spatial streams and channel of a radio

EXAMPLE:
$ ./lf_modify_radio.py --host 192.168.100.205 --radio "1.1.wiphy0" --channel 36 --antenna 7 --debug

NOTES:


TO DO NOTES:

"""
import os
import sys
import importlib
import argparse
import pprint

if sys.version_info[0] != 3:
    print("This script requires Python3")
    exit()

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
lanforge_api = importlib.import_module("lanforge_client.lanforge_api")
from lanforge_client.lanforge_api import LFSession
from lanforge_client.lanforge_api import LFJsonCommand
from lanforge_client.lanforge_api import LFJsonQuery
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
def main():
    parser = argparse.ArgumentParser(
        prog=__file__,
        formatter_class=argparse.RawTextHelpFormatter,
        description='modifies radio antenna')
    parser.add_argument("--debug", help='turn on debugging', action="store_true")
    parser.add_argument("--host", "--mgr", help='specify the GUI to connect to, assumes port 8080')
    parser.add_argument("--radio", help='name of the radio to modify: e.g. 1.1.wiphy0')
    parser.add_argument("--antenna", help='number of spatial streams: 0 Diversity (All), 1 Fixed-A (1x1), 4 AB (2x2), 7 ABC (3x3), 8 ABCD (4x4), 9 (8x8)')
    parser.add_argument("--channel", help='channel of the radio: e.g. 6 (2.4G) or 36 (5G)')

    args = parser.parse_args()
    if not args.radio:
        print("No radio name provided")
        exit(1)

    session = LFSession(lfclient_url="http://%s:8080" % args.host,
                        debug=args.debug,
                        connection_timeout_sec=2.0,
                        stream_errors=True,
                        stream_warnings=True,
                        require_session=True,
                        exit_on_error=True)
    command: LFJsonCommand
    command = session.get_command()
    query: LFJsonQuery
    query = session.get_query()

    shelf, resource, radio, *nil = LFUtils.name_to_eid(args.radio)
    
    command.post_set_wifi_radio(resource=resource,
                                radio=radio,
                                shelf=shelf,
                                antenna=args.antenna,
                                channel=args.channel,
                                debug=args.debug)

if __name__ == "__main__":
    main()
#
