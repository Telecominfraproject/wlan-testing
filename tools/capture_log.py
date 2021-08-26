#!/usr/bin/python3.9
"""

    lf_tools : Tools for LANforge
                reboot, run_cmd, etc
    ./lf_tools --host 10.28.3.8 --port 22 --username root --password lanforge --action reboot
    ./lf_tools --host 10.28.3.8 --port 22 --username root --password lanforge --action run_cmd --cmd ls

"""
import argparse
import paramiko
import os
import datetime
import re


class LFTools:

    def __init__(self, host="", port=22, username="root", password="lanforge"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def ssh_cli_connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("Connecting to LANforge: %s@%s:%s" % (
            self.username, self.host, self.port))
        client.connect(self.host, username=self.username, password=self.password,
                       port=self.port, timeout=10, allow_agent=False, banner_timeout=200)

        return client

    def run_cmd(self, cmd):
        client = self.ssh_cli_connect()
        stdin, stdout, stderr = client.exec_command(cmd)
        output = "Output: " + str(stdout.read())
        error = "Error: " + str(stderr.read())
        client.close()
        return output, error

    def run_action(self, action, cmd):
        if action == "reboot":
            output, error = self.run_cmd("reboot")
            print(output, error)
        elif action == "run_cmd":
            output, error = self.run_cmd(cmd)
            print(output, error)
        elif action == "capture_log":
            output, error = self.run_cmd('sudo cat -n /home/lanforge/wifi/wpa_supplicant_log_wiphy0.txt')
            # print('log is being fetched......')
            out1 = output[10:].replace('\\n', '\n').replace('\\t', '.').replace('"', '')
            list_of_output = out1.split('\n')
            # print("".join(list_of_output))
            temp_data = []
            for i in list_of_output:
                line = re.split('\s', i.strip())
                # print(lst)
                try:
                    date1 = line[0].split('.')
                    date = date1[1:]
                    date.pop()
                    date.append(":")
                    datetime_format = datetime.datetime.fromtimestamp(int(date[0]))
                    date[0] = str(datetime_format)
                    line[0] = str(".".join(date))
                    temp_data.append(" ".join(line))
                except:
                    pass
            data_text = "\n".join(temp_data)
            with open("capture_log_text.txt", "w") as file:
                file.write(data_text)
        else:
            print("Invalid Action")


def main():
    parser = argparse.ArgumentParser(prog="lf_utils",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     allow_abbrev=True,
                                     epilog="About lf_tools.py",
                                     description="Tools for LANforge System")
    parser.add_argument('--host', type=str, help=' --host : IP Address f LANforge System', default="192.168.200.15")
    parser.add_argument('--port', type=int, help='--passwd of dut', default=22)
    parser.add_argument('--username', type=str, help='--username to use on LANforge', default="root")
    parser.add_argument('--password', type=str, help='--password to the given username', default="lanforge")
    parser.add_argument('--action', type=str, help='--action to perform'
                                                   'reboot | run_cmd', default="run_cmd")
    parser.add_argument('--cmd', type=str, help='--cmd : used when action is "run_cmd"', default="ls")
    args = parser.parse_args()
    lf_tools = LFTools(host=args.host, port=args.port, username=args.username, password=args.password)
    lf_tools.run_action(args.action, args.cmd)


if __name__ == '__main__':
    main()

# python capture_log.py --host 192.168.200.15 --password lanforge --action capture_log