#!/usr/bin/env python3
"""
this file is used in tip for getting serial number of attenuators
"""
import sys
import os
import importlib
import time
import argparse

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFRequest = importlib.import_module("py-json.LANforge.LFRequest")
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")


class AttenuatorSerial(LFCliBase):
    def __init__(self, lfclient_host, lfclient_port, debug_=False):
        super().__init__(lfclient_host, lfclient_port, debug_)
        self.lfclient_host = lfclient_host
        self.COMMANDS = ["show_attenuators", "set_attenuator"]
        self.atten_serno = ""
        self.atten_idx = ""
        self.atten_val = ""
        self.atten_data = {
            "shelf": 1,
            "resource": 1,
            "serno": None,
            "atten_idx": None,
            "val": None,
            "mode": None,
            "pulse_width_us5": None,
            "pulse_interval_ms": None,
            "pulse_count": None,
            "pulse_time_ms": None
        }

    def show(self, debug=False):
        ser_no_list = []
        print("Show Attenuators.........")
        response = self.json_get("/attenuators/")
        time.sleep(0.01)
        if response is None:
            print(response)
            raise ValueError("Cannot find any endpoints")
        else:
            attenuator_resp = response["attenuators"]
            for i in attenuator_resp:
                for key in i:
                    if key == "entity id":
                        print("entity id")
                    # print("%s " % (key))
                    ser_no_list.append(key)

        return ser_no_list


def main():
    parser = argparse.ArgumentParser(
        prog='attenuator_serial.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
 Useful Information:
 this file is used in tip for getting serial number of attenuators,
            ''',

        description='''
attenuator_serial.py.py:
    this file is used in tip for getting serial number of attenuators,
        ''')

    # used for showing help 
    parser.parse_args()

    obj = AttenuatorSerial(lfclient_host="localhost", lfclient_port=8802)
    x = obj.show()
    print("out", x)


if __name__ == '__main__':
    main()
