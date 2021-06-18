#!/usr/bin/python3.9
"""

    lf_tools : Tools for Access Point
                reboot, run_cmd, etc
    ./lf_tools --host 10.28.3.8 --jumphost True --port 22 --username root --password openwifi --action reboot
    ./lf_tools --host 10.28.3.8 --jumphost True --port 22 --username root --password openwifi --action run_cmd --cmd ls

"""
import sys

if "libs" not in sys.path:
    sys.path.append("../libs/apnos/")

import argparse
import paramiko
from apnos import APNOS


class APTools:

    def __init__(self, host="", port=22, username="root", jumphost=True,
                 password="openwifi", tty="/dev/ttyAP1"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.credentials = {
            'jumphost': jumphost,
            'ip': host,
            'username': username,
            'password': password,
            'port': port,
            'jumphost_tty': tty,

        }
        self.apnos = APNOS(credentials=self.credentials)

    def run_action(self, action, cmd):
        if action == "reboot":
            output, error = self.apnos.reboot()
            print(output, error)
        elif action == "run_cmd":
            [input, output, error] = self.apnos.run_generic_command(cmd=cmd)
            print(input, output, error)
        elif action == "get_redirector":
            redirector = self.apnos.get_redirector()
            print(redirector)
        elif action == "set_redirector":
            [input, output, error] = self.apnos.run_generic_command(cmd=cmd)
            print(input, output, error)


def main():
    parser = argparse.ArgumentParser(prog="lf_utils",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     allow_abbrev=True,
                                     epilog="About lf_tools.py",
                                     description="Tools for Access Point System")
    parser.add_argument('--host', type=str, help=' --host : IP Address f LAB Controller / '
                                                 'Access Point System', default="localhost")
    parser.add_argument('--jumphost', type=bool, help=' --host : IP Address f Access Point System', default=True)
    parser.add_argument('--tty', type=bool, help=' --tty : /dev/ttyAP1', default="/dev/ttyAP1")
    parser.add_argument('--port', type=int, help='--passwd of dut', default=22)
    parser.add_argument('--username', type=str, help='--username to use on Access Point', default="root")
    parser.add_argument('--password', type=str, help='--password to the given username', default="openwifi")
    parser.add_argument('--action', type=str, help='--action to perform'
                                                   'reboot | run_cmd', default="run_cmd")
    parser.add_argument('--cmd', type=str, help='--cmd : used when action is "run_cmd"', default="pwd")
    args = parser.parse_args()
    lf_tools = APTools(host=args.host, port=args.port, tty=args.tty,
                       username=args.username, jumphost=args.jumphost, password=args.password)
    lf_tools.run_action(args.action, args.cmd)


if __name__ == '__main__':
    main()
