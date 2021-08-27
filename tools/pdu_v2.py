#!/usr/bin/env python3
"""
Date: 12-08-2021
By: Amrit Raj @ Candela Technologies Pvt. ltd.
Note: Please ensure that PDU is powered on.
    Command line to be used as
    python pdu_automation.py --host 192.168.200.90 --user admin --password 1234 --action on/off/cycle --port all/specific_port_name
    Eg 1: python pdu_automation.py --host 192.168.200.90 --user admin --password 1234 --action off --port 'Outlet 1'
    Eg 2: python pdu_automation.py --host 192.168.200.90 --user admin --password 1234 --action cycle --port all
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
            self.i = 0
            for i in self.power_switch:
                # print(i.description)
                if i.description == self.port:
                    self.power_switch[self.i].state = "ON"
                self.i += 1
        else:
            for outlet in self.power_switch:
                outlet.state = 'ON'


class switch_off(setup):
    def __init__(self, hostname, user, password, port=None):
        super().__init__(hostname, user, password)
        self.port = port
        if self.port != 'all':
            self.i = 0
            for i in self.power_switch:
                # print(i.description)
                if i.description == self.port:
                    self.power_switch[self.i].state = "OFF"
                self.i += 1
            # self.power_switch[int(self.port)-1].state = "OFF"
        else:
            for outlet in self.power_switch:
                outlet.state = 'OFF'


class print_status(setup):
    def __init__(self, hostname, user, password):
        super().__init__(hostname, user, password)
        print(self.power_switch)


def main(argv: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', help='Input the pdu name eg: basic-01 or basic-02\n')
    parser.add_argument('--action', help='Switches all Outlets in ON Mode eg: on or off\n')
    parser.add_argument('--port', help='Please provide port name eg: --port lanforge')
    args = parser.parse_args(argv)
    argument1 = vars(args)
    testbed = argument1['testbed']
    f = open('pdu.json')
    y = json.load(f)
    argument2 = y[testbed]
    dic = {**argument1, **argument2}  # Dictionay Merging
    # print(dic)
    if dic['action'] == 'on':
        set = setup(dic['host'], dic['username'], dic['password'])
        on = switch_on(dic['host'], dic['username'], dic['password'], dic['port'])
    elif dic['action'] == 'off':
        set = setup(dic['host'], dic['username'], dic['password'])
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
