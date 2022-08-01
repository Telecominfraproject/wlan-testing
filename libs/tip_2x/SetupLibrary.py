import logging

import paramiko
from scp import SCPClient

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class SetupLibrary:

    def __init__(self, remote_ip="",
                 remote_ssh_port=22,
                 remote_ssh_username="lanforge",
                 remote_ssh_password="lanforge",
                 pwd="",
                 ):
        self.pwd = pwd
        self.remote_ip = remote_ip
        self.remote_ssh_username = remote_ssh_username
        self.remote_ssh_password = remote_ssh_password
        self.remote_ssh_port = remote_ssh_port

    def setup_serial_environment(self):
        client = self.ssh_cli_connect()
        cmd = '[ -f ~/cicd-git/ ] && echo "True" || echo "False"'
        stdin, stdout, stderr = client.exec_command(cmd)
        output = str(stdout.read())
        if output.__contains__("False"):
            cmd = 'mkdir ~/cicd-git/'
            client.exec_command(cmd)
        cmd = '[ -f ~/cicd-git/openwrt_ctl.py ] && echo "True" || echo "False"'
        stdin, stdout, stderr = client.exec_command(cmd)
        output = str(stdout.read())
        if output.__contains__("False"):
            print("Copying openwrt_ctl serial control Script...")
            with SCPClient(client.get_transport()) as scp:
                scp.put(self.pwd + 'openwrt_ctl.py', '~/cicd-git/openwrt_ctl.py')  # Copy my_file.txt to the server
        cmd = '[ -f ~/cicd-git/openwrt_ctl.py ] && echo "True" || echo "False"'
        stdin, stdout, stderr = client.exec_command(cmd)
        var = str(stdout.read())
        client.close()

    def ssh_cli_connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logging.info("Trying SSH Connection to: " + str(self.remote_ip) +
                     " on port: " + str(self.remote_ssh_port) +
                     " with username: " + str(self.remote_ssh_username) +
                     " and password: " + str(self.remote_ssh_password))
        client.connect(self.remote_ip, username=self.remote_ssh_username, password=self.remote_ssh_password,
                       port=self.remote_ssh_port, timeout=10, allow_agent=False, banner_timeout=200)
        return client

    def check_serial_connection(self, tty="/dev/ttyUSB0"):
        client = self.ssh_cli_connect()
        cmd = 'ls /dev/tty*'
        stdin, stdout, stderr = client.exec_command(cmd)
        output = str(stdout.read().decode('utf-8'))
        client.close()
        available_tty_ports = output.split("\n")
        if tty in available_tty_ports:
            logging.info("Expected Serial Console Port, " + tty + " is available on " + self.remote_ip)
        else:
            logging.error("Expected Serial Console Port, " + tty + " is not available on " + self.remote_ip)
        return tty in available_tty_ports

    def kill_all_minicom_process(self, tty="/dev/ttyUSB0"):
        client = self.ssh_cli_connect()
        stdin, stdout, stderr = client.exec_command("fuser -k " + tty)
        # print(stdout.read())
        client.close()


if __name__ == '__main__':
    obj = SetupLibrary(remote_ip="192.168.52.89",
                       remote_ssh_port=22,
                       pwd="")

    obj.setup_serial_environment()
    obj.check_serial_connection(tty="/dev/ttyUSB0")
    obj.kill_all_minicom_process(tty="/dev/ttyUSB0")
