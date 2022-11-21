#!/usr/bin/env python3
"""

Author:
    Amrit Raj <amrit.raj@candelatech.com>
Status:
    In Progress
Created:
    22-Aug-2022

NAME: lf_setup_radius_server.py
PURPOSE:
    lf_setup_radius_server.py will add user to users in Radius server for TTLS.
EXAMPLE:
    lf_setup_radius_server.py --mrg <lanforge ip> --secret sec_ret --input_text "Config text"

COPYRIGHT:
Copyright 2022 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""

import argparse
import sys
import paramiko
import logging


logger = logging.getLogger(__name__)
if sys.version_info[0] != 3:
    logger.critical("This script requires Python 3")
    exit(1)
logger = logging.getLogger(__name__)

class SetupRadiusServer:
    def __init__(self, ipaddress, secret, input_text):
        self.host = ipaddress
        self.secret = secret
        self.input_text = input_text

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.host, port=22, username='root', password='lanforge', timeout=10)
        logger.info("[ESTABLISHMENT] Connection is being established.\n\n")
    def add_user(self):
        # adding the args in the users file
        logger.info("[NEW USER] Trying to add new user.\n\n")
        users_data = ''
        sftp_client = self.ssh.open_sftp()
        remote_file = sftp_client.open('/etc/raddb/users')
        try:
            for line in remote_file:
                users_data += line
            remote_file.close()
            if self.input_text in users_data:
                logger.error("[DUPLICATE] Configuration for this user already available.\n\n")
                return 0
        finally:
            remote_file.close()

        temp_file_data = users_data.split('\n')
        line_number = 0

        for i in range(len(temp_file_data)):
            if temp_file_data[i] == '# EAP-TTLS user (name + password login)':
                line_number = i
                logger.info("[FINDING] User Not found in the users config file.\n\n")
                break

        # client_conf = """
        # client localhost {
        #    ipaddr = 10.28.2.0/24
        #    proto = *
        #    secret = testing123
        #    require_message_authenticator = no
        #    shortname = localhost
        #    nas_type    = other   # localhost isn't usually a NAS...
        #    limit {
        #       max_connections = 16
        #       lifetime = 0
        #       idle_timeout = 30
        #    }
        # }
        # client localhost_ipv6 {
        #         ipv6addr = ::1
        #         secret = testing123
        # }
        # """

        temp_file_data.insert(line_number+1, self.input_text)
        remote_file = sftp_client.open('/etc/raddb/users', 'w')
        text = ''
        for i in temp_file_data:
            text += i + "\n"
        remote_file.write(text)
        logger.info("[SUCCESS] configuration applied successfully\n")
        remote_file.flush()

    def get_logs(self):
        # Getting Log
        logger.info("[LOG] Accessing logs...\n\n")
        stdin, stdout, stderr = self.ssh.exec_command('tail /var/log/radius/radius.log')
        output = stdout.readlines()
        for i in output:
            logger.info(i)



    def copy_certs(self):
        # Before Copying certificates Checking availablity
        stdin, stdout, stderr = self.ssh.exec_command('ls /etc/raddb/certs/')
        logger.info("[UPDATING CERTS] Copying the certificates.\n\n")
        output = str(stdout.read())
        try:
            if "client.p12" not in output or "ca.pem" not  in output:
                logger.error("Error: Sorry your certificates does not exit. Please create one before copying.")
                return 0
        except:
            logger.error("[ERROR]: Sorry your certificates does not exit. Please create one before copying.\n\n")

        # # Copying certificates
        stdin, stdout, stderr = self.ssh.exec_command('cp /etc/raddb/certs/client.p12 /home/lanforge && '
                                                 'cp /etc/raddb/certs/ca.pem /home/lanforge')



parser = argparse.ArgumentParser(prog='lf_setup_radius_server.py', description='''lf_setup_radius_server.py: Summary 
                                        :This script will be able to add a configuration provided by the user to the
                                         Radius server's users configuration. ''')

parser.add_argument('--mgr', help="ipaddr of connections", type=str, default='localhost')
parser.add_argument('--secret', help="secrets for each user", type=str, default='NA')

parser.add_argument('--input_text', help="""
    client localhost {
       ipaddr = 10.28.2.0/24
       proto = *
       secret = testing123
       require_message_authenticator = no
       shortname = localhost
       nas_type    = other
       limit {
          max_connections = 16
          lifetime = 0
          idle_timeout = 30
       }
    }
    client localhost_ipv6 {
            ipv6addr = ::1
            secret = testing123
    }
    """, type=str, default=None)


args = parser.parse_args()

if args.input_text is None or args.input_text == "":
    print("[INPUT ERROR] Input text can not be Empty")
    exit(0)

def main():
    setupRadius = SetupRadiusServer(ipaddress = args.mgr,
                                    secret = args.secret,
                                    input_text = args.input_text)
    setupRadius.add_user()
    setupRadius.copy_certs()
    setupRadius.get_logs()


if __name__ == "__main__":
    main()