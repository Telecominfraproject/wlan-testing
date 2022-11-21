#!/usr/bin/env python3
"""
NAME: jbr_adb.py

PURPOSE: test the functionality of the adb command, both using Realm and using lanforge_api

EXAMPLE:
$ ./jbr_adb.py --host ct521a-jana --id asdf --cmd "free form command to test unescaped value"

NOTES:


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
    import lanforge_api.LFJsonCommand
    import lanforge_api.LFJsonQuery


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
#   M A I N
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
def main():
    parser = argparse.ArgumentParser(
        prog=__file__,
        formatter_class=argparse.RawTextHelpFormatter,
        description='tests creating wanlink')
    parser.add_argument("--host", "--mgr", help='specify the GUI to connect to, assumes port 8080')
    parser.add_argument("--id", help='adb_id of device')
    parser.add_argument("--cmd", help='adb_cmd to give device')
    parser.add_argument("--debug", help='turn on debugging', action="store_true")

    args = parser.parse_args()
    if not args.id:
        print("No adb_id provided")
        exit(1)
    if not args.cmd:
        print("No adb_cmd provided")
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
        txt_cmd = "shell dumpsys wifi"

    # Is it possible that the post_add_text_blob can detect any kind of \r \n combo and
    # split it up into lines, multiplying the command?

    # command.post_rm_adb(shelf=1, resource=1, adb_id=args.id, debug=args.debug, suppress_related_commands=True)
    command.post_show_adb(shelf=1, resource=1, serno='ALL')
    adb_key = session.get_session_based_key()
    session.logger.error("adb_key: " + adb_key)
    errors_warnings = []
    response_list = []
    command.post_adb(shelf=1,
                     resource=1,
                     key=adb_key,
                     adb_id=args.id,
                     adb_cmd=txt_cmd,
                     response_json_list=response_list,
                     debug=True,
                     errors_warnings=errors_warnings,
                     suppress_related_commands=True)
    pprint.pprint(["Response", response_list])

    command.post_show_adb(shelf=1, resource=1, serno='ALL')
    eid_url = "%s.%s.%s" % (1, 1, args.id)
    time.sleep(0.05)
    print("List of adbs:")
    diagnostics = []
    result = query.get_adb(eid_list=eid_url, debug=True, errors_warnings=diagnostics)
    pprint.pprint(diagnostics)
    pprint.pprint(result)

    # localrealm =


if __name__ == "__main__":
    main()
