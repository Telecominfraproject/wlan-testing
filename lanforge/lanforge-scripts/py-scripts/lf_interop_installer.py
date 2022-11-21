#!/usr/bin/env python3

"""
NAME: lf_interop_installer.py


PURPOSE:
    This program is used updating the Lanforge InterOp android app in phones that are connected to Lanforge using usb.

EXAMPLE: ./python3 lf_interop_installer.py  --mgr 192.168.200.220 --mgr_port 8080 --app_loc
/home/lanforge/LANforgeGUI_5.4.5/lanforge_interop_app.apk --device all(or serial number with comma seperated
8PSSJNDUHY8DSCUG,52009ecbeafc253b) --lf_user lanforge --lf_password lanforge

Note: To Run this script
    The phone should be Connected to lanforge using usb cable and developer option of the phone must be enabled
    If Lanforge InterOp android app is not previously installed then it will install the app on the devices

LICENSE:
    Free to distribute and modify. LANforge systems must be licensed.
    Copyright 2021 Candela Technologies Inc
"""
import sys
import paramiko
import argparse
import socket

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)


class AppInstaller:
    def __init__(self,
                 app_loc='/home/lanforge/interop-5.4.5.apk',
                 device=None,
                 lf_user='lanforge',
                 lf_password='lanforge',
                 host="localhost",
                 _exit_on_fail=False):

        self.host = host
        self.app_loc = app_loc
        self.device = device
        self.lf_user = lf_user
        self.lf_password = lf_password
        if self.host == "localhost":
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            self.host = ip
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.lf_user, password=self.lf_password)

    def Get_Device_List(self):
        stdin, stdout, stderr = self.client.exec_command('adb devices')
        ls = []
        for i in stdout:
            if any(map(str.isdigit, i)):
                ls.append(i.split('\t')[0])
        return ls

    def install_apk(self):
        phone_list = []
        if self.device[0] == "all":
            phone_list = self.Get_Device_List()
        else:
            for i in self.device:
                phone_list.append(i)
        # print("List of Phones ", phone_list)
        for i in phone_list:
            self.clean_phone(i)
            stdin, stdout, stderr = self.client.exec_command("adb -s " + i + " install -t " + self.app_loc)
            output = stdout.readline().strip()
            print("[INSTALLATION] ", output)
            print("[SUCCESS] Installation Success\n")
        self.client.close()

    def clean_phone(self, device_name):
        stdin, stdout, stderr = self.client.exec_command("adb -s " + device_name + " shell pm list packages "
                                                                                   "| grep com.candela.wecan")
        output = (stdout.readline()).strip()
        # print(output)
        if output == "package:com.candela.wecan":
            print("[CLEANING] Old installed app from device " + device_name)
            stdin, stdout, stderr = self.client.exec_command("adb -s " + device_name + " shell pm uninstall "
                                                                                       "com.candela.wecan")
            print("[CLEANING] ", stdout.readlines()[0].strip())


def main():
    parser = argparse.ArgumentParser(description="Lanforge Interop App Installer (Please enable developers mode for "
                                                 "all the phones before using this script)")
    parser.add_argument('--mgr', help='Lanforge IP address on which all the phones are connected', required=True,
                        default='localhost')
    parser.add_argument('--app_loc', help='Location where latest app is kept on lanforge '
                                          'Eg. /home/lanforge/LANforgeGUI_5.4.5/lanforge_interop_app.apk ',
                        default="/home/lanforge/LANforgeGUI_5.4.5/lanforge_interop_app.apk ", required=True)
    parser.add_argument('--device', help='On which device you want to install Eg. RZ8R21T5RWH, or all for all device',
                        nargs='+', default='all')
    parser.add_argument('--lf_user', help='Lanforge username Eg. lanforge', default='lanforge')
    parser.add_argument('--lf_pass', help='Password of Lanforge Eg. lanforge', default='lanforge')

    args = parser.parse_args()
    app_installer = AppInstaller(host=args.mgr,
                                 lf_user=args.lf_user,
                                 lf_password=args.lf_pass,
                                 app_loc=args.app_loc,
                                 device=args.device)
    app_installer.install_apk()


if __name__ == "__main__":
    main()