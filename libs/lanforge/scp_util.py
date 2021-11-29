#!/usr/bin/env python3
import argparse

import paramiko
from scp import SCPClient


class SCP_File:
    def __init__(self, ip="localhost", port=22, username="lanforge", password="lanforge", remote_path="/home/lanforge/",
                 local_path="."):
        self.ip = ip
        self.port = port
        self.remote_path = remote_path
        self.local_path = local_path
        self.username = username
        self.password = password

    def pull_file(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip, username=self.username, password=self.password, port=self.port, allow_agent=False,
                    look_for_keys=False)
        # ssh.close()

        with SCPClient(ssh.get_transport()) as scp:
            scp.get(remote_path=self.remote_path, local_path=self.local_path, recursive=True)
            scp.close()


def main():
    parser = argparse.ArgumentParser(prog="lf_utils",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     allow_abbrev=True,
                                     epilog="About lf_tools.py",
                                     description="Tools for LANforge System")
    parser.add_argument('--host', type=str, help=' --host : IP Address f LANforge System', default="localhost")
    parser.add_argument('--port', type=int, help='--passwd of dut', default=22)
    parser.add_argument('--username', type=str, help='--username to use on LANforge', default="lanforge")
    parser.add_argument('--password', type=str, help='--password to use on LANforge', default="lanforge")
    parser.add_argument('--remote_path', type=str, help='--password to the given username',
                        default="/home/lanforge/lf_kinstall.pl")
    parser.add_argument('--local_path', type=str, help='--action to perform'
                                                       'reboot | run_cmd', default=".")
    args = parser.parse_args()
    lf_tools = SCP_File(ip=args.host, port=args.port,
                        username=args.username, password=args.password,
                        remote_path=args.remote_path, local_path=args.local_path)
    lf_tools.pull_file()




if __name__ == '__main__':
    main()
