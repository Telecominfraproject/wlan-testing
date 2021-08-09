import os
import pprint
import time
from typing import Sequence
from typing import Optional
import argparse

try:
    import dlipower
except:
    print('Please wait we are installing DLI Power')
    os.system('pip install dlipower')
power_switch = dlipower.PowerSwitch(hostname='192.168.200.49', userid='admin', password='Lanforge12345!')


class switch_on:
    def __init__(self, num=None):
        self.num = num
        if self.num != None:
            power_switch[int(self.num)-1].state = "ON"
        else:
            for outlet in power_switch:
                outlet.state = 'ON'


class switch_off:
    def __init__(self, num=None):
        self.num = num
        if self.num != None:
            power_switch[int(self.num)-1].state = "OFF"
        else:
            for outlet in power_switch:
                outlet.state = 'OFF'

def main(argv:Optional[Sequence[str]]=None):
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument('--ON_ALL', help='Switches all Outlets in ON Mode')
    parser.add_argument('--OFF_ALL', help='Switches all Outlets in OFF Mode')
    parser.add_argument('--ON', help='Switches the target Outlets in ON Mode eg: --ON 4')
    parser.add_argument('--OFF', help='Switches the target Outlets in OFF Mode --OFF 6')
    parser.add_argument('--CYCLE_ALL', help='Cycle all Outlets in OFF Mode and then ON Mode eg: --CYCLE_ALL True')
    parser.add_argument('--CYCLE', help='Cycle selected target Outlets in OFF Mode and then ON Mode eg: --CYCLE 6')
    args = parser.parse_args(argv)
    dic = vars(args)
    # print(dic)
    if dic['ON_ALL'] == 'True':
        on = switch_on()
    elif dic['OFF_ALL'] == 'True':
        off = switch_off()
    elif dic['CYCLE_ALL'] is not None:
        off = switch_off()
        on = switch_on()
    elif dic['CYCLE'] is not None:
        on = switch_off(dic['CYCLE'])
        off = switch_on(dic['CYCLE'])
    elif dic['ON'] is not None:
        on = switch_on(dic['ON'])
    elif dic['OFF'] is not None:
        on = switch_off(dic['OFF'])


if __name__ == '__main__':
    main()
