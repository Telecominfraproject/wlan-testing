#!/usr/local/bin/python3

import argparse
import paramiko
from datetime import datetime

today = datetime.today().strftime("%Y-%m-%d")
time_now = datetime.today().strftime("%H-%M-%S")
parser = argparse.ArgumentParser()
parser.add_argument("--nola-number", type=str, help="nola testbed number")
parser.add_argument("--jumpbox-address", type=str, help="jumpbox ip address")
parser.add_argument("--jumpbox-username", type=str, help="jumpbox password", default="lanforge")
parser.add_argument("--jumpbox-password", type=str, help="jumpbox password")
command_line_args = parser.parse_args()

commands_to_execute = (
    "cd /home/lanforge/nola-nightly-sanity/wlan-testing/tests/cicd_sanity",
    "git pull",
    f"mkdir -p logs/{today}",
    f"./cicd_sanity.py -f nola{command_line_args.nola_number}_test_info.py --skip_vlan -i yes --tr_prefix NOLA{command_line_args.nola_number}_Sanity_ > logs/{today}/{time_now}.log 2>&1",
    f"cat logs/{today}/{time_now}.log"
)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() ) # accept all keys
ssh.connect(
    command_line_args.jumpbox_address,
    port = 22,
    username = command_line_args.jumpbox_username,
    password = command_line_args.jumpbox_password,
    banner_timeout = 600
)

stdin, stdout, stderr = ssh.exec_command( '\n'.join( commands_to_execute ) )
exit_status = stdout.channel.recv_exit_status()
for channel in stdout, stderr:
    for line in channel:
        print( line )
ssh.close()
