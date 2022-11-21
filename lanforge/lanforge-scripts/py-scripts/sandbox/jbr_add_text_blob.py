#!/usr/bin/env python3
"""
NAME: jbr_add_text_blob.py

PURPOSE: create a text blob to verify the functionality of unescaped arguments

EXAMPLE:
$ ./jbr_add_text_blob.py --host ct521a-jana --type 'hot take' --name 'spicy jab' --text stuff .....

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
    from lanforge_api import LFJsonCommand
    from lanforge_api import LFJsonQuery

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
#   M A I N
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
def main():
    parser = argparse.ArgumentParser(
        prog=__file__,
        formatter_class=argparse.RawTextHelpFormatter,
        description='tests creating wanlink')
    parser.add_argument("--host", "--mgr", help='specify the GUI to connect to, assumes port 8080')
    parser.add_argument("--type", help='text-blob type')
    parser.add_argument("--name", help='text-blob name')
    parser.add_argument("--text", help='text-blob body')
    parser.add_argument("--debug", help='turn on debugging', action="store_true")

    args = parser.parse_args()
    if not args.name:
        print("No blob name provided")
        exit(1)
    if not args.type:
        print("No blob type provided")
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

    txt_blob = args.text
    if (not args.text) or (args.text == "saved01"):
        txt_blob = """      }
    }
EOF
  )"
  qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "$SCRIPT" 2> /dev/null
fi

# TODO: handle other desktop environments

exec /snap/bin/firefox "$@"
"""

    # Is it possible that the post_add_text_blob can detect any kind of \r \n combo and
    # split it up into lines, multiplying the command?

    command.post_rm_text_blob(p_type=args.type, name=args.name,
                              debug=args.debug, suppress_related_commands=True)
    command.post_show_text_blob(name='ALL', p_type='ALL', brief='yes')
    command.post_add_text_blob(p_type=args.type, name=args.name, text=txt_blob,
                               debug=True, suppress_related_commands=True)
    command.post_show_text_blob(name='ALL', p_type='ALL', brief='no')
    eid_url="%s.%s" % (args.type, args.name)
    time.sleep(0.05)
    print ("List of text blobs:")
    diagnostics=[]
    result = query.get_text(eid_list=eid_url, debug=True, errors_warnings=diagnostics)
    pprint.pprint(diagnostics)
    pprint.pprint(result)

if __name__ == "__main__":
    main()
