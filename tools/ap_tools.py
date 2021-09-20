#!/usr/bin/python3.9
"""

    ap_tools : Tools for Access Point
                reboot, run_cmd, etc
    ./ap_tools --host 10.28.3.8 --jumphost True --port 22 --username root --password openwifi --action reboot
    ./ap_tools --host 10.28.3.8 --jumphost True --port 22 --username root --password openwifi --action run_cmd --cmd ls

"""
import sys
import time
if "libs" not in sys.path:
    sys.path.append("../libs/apnos/")

import argparse
from apnos import APNOS


class APTools:

    def __init__(self, host="", port=22, username="root", jumphost=True,
                 password="openwifi", tty="/dev/ttyAP1", serial=""):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.credentials = {
            'jumphost': jumphost,
            'ip': host,
            'serial': serial,
            'username': username,
            'password': password,
            'port': port,
            'jumphost_tty': tty,

        }
        self.apnos = APNOS(credentials=self.credentials)

    def run_action(self, action, cmd, url):
        if action == "reboot":
            output, error = self.apnos.reboot()
            print(output, error)
        elif action == "run_cmd":
            output = self.apnos.run_generic_command(cmd=cmd)
            print(output)
        elif action == "verify":
            [input, output, error] = self.apnos.run_generic_command("cat /tmp/sysinfo/model;"
                                                                    "cat /etc/banner")
            print(output)
            #print(error)
        elif action == "upgrade":
            [input, output, error] = self.apnos.run_generic_command(f"cd /tmp ; curl -L {url} --output upgrade ; "
                                                                    "sysupgrade -n upgrade")
            print(input, output, error)
            time.sleep(300)
        elif action == "get_redirector":
            redirector = self.apnos.get_redirector()
            print(redirector)
        elif action == "set_redirector":
            [input, output, error] = self.apnos.run_generic_command(cmd=cmd)
            print(input, output, error)


def main():
    parser = argparse.ArgumentParser(prog="ap_tools",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     allow_abbrev=True,
                                     epilog="About ap_tools.py",
                                     description="Tools for Access Point System")
    parser.add_argument('--host', type=str, help=' --host : IP Address f LAB Controller / '
                                                 'Access Point System', default="localhost")
    parser.add_argument('--jumphost', type=bool, help=' --jumphost : True/False ', default=True)
    parser.add_argument('--tty', type=str, help=' --tty : /dev/ttyAP1', default="/dev/ttyAP1")
    parser.add_argument('--port', type=int, help='--port key of LAB Controller/AP ', default=22)
    parser.add_argument('--username', type=str, help='--username to use on Access Point/LAB Controller', default="root")
    parser.add_argument('--password', type=str, help='--password to the given username', default="openwifi")
    parser.add_argument('--sdk', type=str, help='--sdk - [1.x/2.x], default-2.x', default="2.x")
    parser.add_argument('--serial', type=str, help='--serial - lowercase serial number', default="serial") 
    parser.add_argument('--action', type=str, help='--action to perform:-'
                                                   '"reboot": For rebooting the ap | '
                                                   '"run_cmd": For running commands on AP'
                                                   ' | "verify": For verifying AP model and firmware version'
                                                   ' | "upgrade": Used for upgrading AP firmware version'
                        , default="run_cmd")
    parser.add_argument('--cmd', type=str, help='--cmd : used when action is "run_cmd"', default="pwd")
    parser.add_argument('--url', type=str, help='--url : Url of the jfrog image file; used when action is "upgrade"',
                        default="")
    args = parser.parse_args()
    print(args.tty)
    lf_tools = APTools(host=args.host, port=args.port, tty=args.tty,
                       username=args.username, jumphost=args.jumphost, password=args.password)
    lf_tools.run_action(args.action, args.cmd, args.url)


if __name__ == '__main__':
    main()
