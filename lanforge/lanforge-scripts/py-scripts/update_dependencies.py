#!/usr/bin/env python3

import subprocess
import argparse
import os


def main():
    parser = argparse.ArgumentParser(
        prog="update_dependencies.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description='''
        NAME: update_dependencies.py
        
        PURPOSE:  Installs python3 script package dependencies
        
        OUTPUT: List of successful and unsuccessful installs
        
        NOTES: Install as root
        '''
    )
    parser.add_argument('--pyjwt', help='Install PyJWT which is necessary for GhostRequest', action="store_true")

    args = parser.parse_args()

    print("Installing Script Python3 Dependencies")
    packages = ['pandas', 'plotly', 'numpy', 'cryptography', 'paramiko', 'pyarrow', 'websocket-client',
                'xlsxwriter', 'pyshark', 'influxdb', 'influxdb-client', 'matplotlib', 'pdfkit', 'pip-search', 'pyserial',
                'pexpect-serial', 'scp', 'dash']
    if args.pyjwt:
        packages.append('pyjwt')
    else:
        print('Not installing PyJWT')
    packages_installed = []
    packages_failed = []
    subprocess.call("pip3 uninstall jwt", shell=True)
    subprocess.call('pip3 install --upgrade pip', shell=True)
    for package in packages:
        if os.name == 'nt':
            command = "pip3 install {} ".format(package)
        else:
            command = "pip3 install {} >/tmp/pip3-stdout 2>/tmp/pip3-stderr".format(package)
        res = subprocess.call(command, shell=True)
        if res == 0:
            print("Package {} install SUCCESS Returned Value: {} ".format(package, res))
            packages_installed.append(package)
        else:
            print("Package {} install FAILED Returned Value: {} ".format(package, res))
            print("To see errors try: pip3 install {}".format(package))
            packages_failed.append(package)

    print("Install Complete")
    print("Packages Installed Success: {}\n".format(packages_installed))
    if not packages_failed:
        return
    print("Packages Failed (Some scripts may not need these packages): {}".format(packages_failed))


if __name__ == "__main__":
    main()
