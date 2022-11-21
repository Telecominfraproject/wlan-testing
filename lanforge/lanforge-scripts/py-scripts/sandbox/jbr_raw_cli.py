#!/usr/bin/env python3
"""
NAME: jbr_raw_cli.py

PURPOSE: test the functionality of passing raw commands thru JSON API

EXAMPLE:
$ ./jbr_raw_cli.py --mgr localhost --debug --cmd "reset_port 1 1 sta00500"
$ echo watch that station reset

$ ./jbr_raw_cli.py --host ct521a-jana --cmd "add_text_blob category type it takes a village to raise a child"
$ Krl /text/spicy.takes
$ echo that created a text blob

NOTES:
This method of executing CLI commands does NOT report errors presently.

TO DO NOTES:

"""
import os
import sys
import time

if sys.version_info[0] != 3:
    print("This script requires Python3")
    exit()

import importlib
import argparse
import pprint
sys.path.insert(1, "../../")

if "SHELL" in os.environ.keys():
    lanforge_api = importlib.import_module("lanforge_client.lanforge_api")
    from lanforge_client.lanforge_api import LFSession
    from lanforge_client.lanforge_api import LFJsonCommand
    from lanforge_client.lanforge_api import LFJsonQuery
else:
    import lanforge_api
    from lanforge_api import LFJsonCommand
    from lanforge_api import LFJsonQuery

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
#   M A I N
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
def main():
    parser = argparse.ArgumentParser(
        prog=__file__,
        formatter_class=argparse.RawTextHelpFormatter,
        description='tests creating raw command')
    parser.add_argument("--host", "--mgr", help='specify the GUI to connect to, assumes port 8080')
    parser.add_argument("--cmd", help='raw cli command to test')
    parser.add_argument("--debug", help='turn on debugging', action="store_true")

    args = parser.parse_args()

    if not args.cmd:
        print("No CLI command provided")
        exit(1)

    session = lanforge_api.LFSession(lfclient_url="http://%s:8080" % args.host,
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

    session.logger.enable(reserved_tag="json_get")
    session.logger.enable(reserved_tag="json_post")

    txt_cmd = args.cmd
    if (not args.cmd) or (args.cmd == "saved01"):
        txt_cmd = "takes a village to ruin \"a\" ''stuffy''"

    # Is it possible that the post_add_text_blob can detect any kind of \r \n combo and
    # split it up into lines, multiplying the command?

    # command.post_rm_adb(shelf=1, resource=1, adb_id=args.id, debug=args.debug, suppress_related_commands=True)
    data={
        "cmd": txt_cmd
    };
    command.json_post(url="/cli-json/raw", post_data=data, debug=args.debug, suppress_related_commands=True)

    print("Next, using command.json_post_raw")

    command.json_post_raw(post_data=data, debug=args.debug, suppress_related_commands=True)

    #localrealm =

if __name__ == "__main__":
    main()
