#!/usr/bin/python3

from UnitTestBase import *

parser = argparse.ArgumentParser(description="Query AP", add_help=False)
parser.add_argument("--cmd", type=str, help="Command-line to run on AP",
                    default = "ifconfig -a")

base = UnitTestBase("query-ap", parser)

cmd = base.command_line_args.cmd

try:
    print("Command: %s"%(cmd))
    rv = ap_ssh_cmd(base.command_line_args, cmd)
    print("Command Output:\n%s"%(rv))

except Exception as ex:
    print(ex)
    logging.error(logging.traceback.format_exc())
    print("Failed to execute command on AP")
