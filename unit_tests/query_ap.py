#!/usr/bin/python3

# Example command line:
#./query_ap.py --testrail-user-id NONE --model ecw5410 --ap-jumphost-address localhost --ap-jumphost-port 7220 --ap-jumphost-password pumpkin77 --ap-jumphost-tty /dev/ttyAP1 --cmd "ifconfig -a"

from UnitTestBase import *

parser = argparse.ArgumentParser(description="Query AP", add_help=False)
parser.add_argument("--cmd", type=str, help="Command-line to run on AP",
                    default = "ifconfig -a")
parser.add_argument("--ap_ssh", type=str, help="ap_ssh method to execute.",
                    default = None, choices=["get_vif_config", "get_vif_state"])

base = UnitTestBase("query-ap", parser)

cmd = base.command_line_args.cmd

try:

    if base.command_line_args.ap_ssh != None:
        ap_cmd = base.command_line_args.ap_ssh
        if ap_cmd == "get_vif_config":
            print(get_vif_config(base.command_line_args))
            sys.exit(0)
        if ap_cmd == "get_vif_state":
            print(get_vif_state(base.command_line_args))
            sys.exit(0)

        print("Un-known ap-ssh method: %s"%(ap_cmd))
        sys.exit(1)
        
    print("Command: %s"%(cmd))
    rv = ap_ssh_cmd(base.command_line_args, cmd)
    print("Command Output:\n%s"%(rv))

except Exception as ex:
    print(ex)
    logging.error(logging.traceback.format_exc())
    print("Failed to execute command on AP")
