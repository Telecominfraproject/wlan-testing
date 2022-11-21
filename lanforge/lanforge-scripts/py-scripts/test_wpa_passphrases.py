#!/usr/bin/env python3
''' test_wpa_passphrases will test challenging wpa psk passphrases

Use './test_wpa_passphrases.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
 '''
import sys
import os
import importlib

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class WPAPassphrases(Realm):
    def __init__(self,
                 ssid=None,
                 security=None,
                 password=None):
        self.ssid = ssid
        self.security = security
        self.password = password


def main():
    pass

if __name__ == "__main__":
    main()
