#!/usr/bin/env python3
"""
Date: 15-09-2021
By: Amrit Raj @ Candela Technologies Pvt. ltd.
Note: Please ensure that PDU is powered on
    Command line to be used as
    python pdu_automation.py --host 192.168.200.49 --user admin --password pass1234 --action on/off/cycle --port all/specific_port_number
    Eg 1: python pdu_v3.py --host 192.168.200.49 --user admin --password pass1234 --action off --port 1
    Eg 2: python pdu_v3.py --host 192.168.200.49 --user admin --password pass1234 --action off --port 1,2,3,4
    Eg 3: python pdu_v3.py --host 192.168.200.49 --user admin --password pass1234 --action cycle --port all
"""
import os
import json
import time
import argparse
from typing import Sequence
from typing import Optional

try:
    import dlipower
except:
    print('Please wait we are installing DLI Power')
    os.system('pip install dlipower')


class setup:
    try:
        def __init__(self, hostname, user, password):
            self.hostname = hostname
            self.user = user
            self.password = password
            self.power_switch = dlipower.PowerSwitch(hostname=self.hostname, userid=self.user, password=self.password)
    except:
        print('PDU device is Off')


class switch_on(setup):
    def __init__(self, hostname, user, password, port=None):
        super().__init__(hostname, user, password)
        self.port = port
        if self.port != 'all':
            try:
                port = str(self.port).split(",")
                for i in port:
                    self.power_switch[int(i)-1].state  = "ON"
            except:
                self.power_switch[int(self.port)-1].state  = "ON"
        else:
            for outlet in self.power_switch:
                outlet.state = 'ON'


class switch_off(setup):
    def __init__(self, hostname, user, password, port=None):
        super().__init__(hostname, user, password)
        self.port = port
        if self.port != 'all':
            try:
                port = str(self.port).split(",")
                for i in port:
                    self.power_switch[int(i) - 1].state = "OFF"
            except:
                self.power_switch[int(self.port) - 1].state = "OFF"
        else:
            for outlet in self.power_switch:
                outlet.state = 'ON'


class print_status(setup):
    def __init__(self, hostname, user, password):
        super().__init__(hostname, user, password)
        print(self.power_switch)


def main(argv: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Please provide host name eg: 192.168.200.65')
    parser.add_argument('--username', help='Please provide username eg: admin')
    parser.add_argument('--password', help='Please provide password eg: 1234')
    parser.add_argument('--action', help='Switches all Outlets in ON Mode eg: --on or --off\n')
    parser.add_argument('--port', help='Please provide port name eg: --port lanforge')
    args = parser.parse_args(argv)
    dic = vars(args)
    # if user enter ports as  1,6,7
    # port = [1,6,7]
    # print(dic)
    if dic['action'] == 'on':
        set = setup(dic['host'], dic['username'], dic['password'])
        on = switch_on(dic['host'], dic['username'], dic['password'], dic['port'])
    elif dic['action'] == 'off':
        set = setup(dic['host'], dic['username'], dic['password'])
        # for single in port
        off = switch_off(dic['host'], dic['username'], dic['password'], dic['port'])
        # off = switch_on(dic['action'])
    elif dic['action'] == 'cycle':
        set = setup(dic['host'], dic['username'], dic['password'])
        on = switch_off(dic['host'], dic['username'], dic['password'], dic['port'])
        off = switch_on(dic['host'], dic['username'], dic['password'], dic['port'])
    else:
        print('Command not found')


if __name__ == '__main__':
    main()