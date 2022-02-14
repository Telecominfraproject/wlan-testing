#!/usr/bin/env python3
"""
This example is to demonstrate ws_generic_monitor to monitor events triggered by scripts,
This script when running, will monitor the events triggered by test_ipv4_connection.py

"""
import sys
import os
import importlib

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

ws_generic_monitor = importlib.import_module("py-json.ws_generic_monitor")
WS_Listener = ws_generic_monitor.WS_Listener
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm

reference = "test_ipv4_connection.py"


class GenericMonitorTest(Realm):
    def __init__(self,
                 ssid=None,
                 security=None,
                 password=None,
                 radio=None):
        self.ssid=ssid
        self.security=security
        self.password=password
        self.radio=radio

    def start(self):
        pass

    def stop(self):
        pass

    def monitor(self):
        pass

def main():
    WS_Listener(lfclient_host="localhost", _scriptname=reference)#, _callback=TestRun)


if __name__ == "__main__":
    main()

