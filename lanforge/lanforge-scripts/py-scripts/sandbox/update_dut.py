#!/usr/bin/env python3
"""
This script updates a Device Under Test (DUT) entry in the LANforge test scenario.
A common reason to use this would be to update MAC addresses in a DUT when you switch
between different items of the same make/model of a DUT.
"""
import sys

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append('../py-json')

import argparse
import pprint
from pprint import *
from LANforge.lfcli_base import LFCliBase
from LANforge.LFUtils import *
from LANforge import add_dut
from LANforge import LFUtils
import argparse
import realm
import time
import datetime


class UpdateDUT(LFCliBase):
    def __init__(self, host, port,
                _debug_on=False,
                _exit_on_error=False,
                _exit_on_fail=False):

        super().__init__(host, port,
                         _debug=_debug_on,
                         _exit_on_fail=_exit_on_fail,
                         _local_realm=realm.Realm(lfclient_host=host, lfclient_port=port, debug_=_debug_on))
        self.host       = host
        self.port       = port
        self.notes      = []
        self.append     = []
        self.params     = {}
        self.flags      = 0x0
        self.flags_mask = 0x0
        self.data       = {}
        self.url        = "/cli-json/add_dut"

    def build(self):
        self.dut_profile = self.local_realm.new_dut_profile()
        self.dut_profile.name = self.name
        for param in self.params:
            if (self.debug):
                print("param: %s: %s"%(param, self.params[param]))
            self.dut_profile.set_param(param, self.params[param])

        if (self.debug):
            print("flags: %s"%self.flags)
        self.dut_profile.flags = self.flags
        self.dut_profile.flags_mask = self.flags_mask
        if len(self.notes) > 0:
            if (self.debug):
                pprint.pprint(self.notes)
            self.dut_profile.notes = self.notes
        if len(self.append) > 0:
            if (self.debug):
                pprint.pprint(self.append)
            self.dut_profile.append = self.append

    def start(self, print_pass=False, print_fail=False):
        self.dut_profile.create()
        self._pass("DUT updated")
        pass

    def stop(self):
        pass

    def cleanup(self, sta_list):
        pass

def main():
    lfjson_host = "localhost"
    lfjson_port = 8080

    param_string = " "
    for param in add_dut.dut_params:
        param_string += "%s, "%param.name

    flags_string = " "
    for flag in add_dut.dut_flags:
        flags_string += "%s, "%flag.name

    parser = LFCliBase.create_bare_argparse( prog='update_dut.py',
        formatter_class=argparse.RawTextHelpFormatter,
        description='''{file}
--------------------
Generic command layout:
python   {file} --dut [DUT name]     # update existing DUT record
                --entry [key,value]     # update/add entry by specifying key and value
                --flag [flag,0|1]       # toggle a flag on 1 or off 0
                --notes "all lines of text"
                --notes "are replaced if any"
                --notes "line of text is submitted with --notes"
                --append "this appends a line of text"
DUT Parameters:
    {params}
DUT Flags:
    {flags}
    
Command Line Example: 
python3 {file} --mgr 192.168.100.24 --update Pathfinder \
    --entry MAC1,"00:00:ae:f0:b1:b9" \
    --notes "build 2901" \
    --flag STA_MODE,0
    --flag AP_MODE,1

'''.format(file=__file__, params=param_string, flags=flags_string),
         epilog="See",
    )
    parser.add_argument("--dut",      type=str, help="name of DUT record")
    parser.add_argument("-p", "--param",    type=str, action="append", help="name,value pair to set parameter")
    parser.add_argument("-f", "--flag",     type=str, action="append", help="name,1/0/True/False pair to turn parameter on or off")
    parser.add_argument("-n", "--notes",    type=str, action="append", help="replace lines of notes in the record")
    parser.add_argument("-a", "--append",   type=str, action="append", help="append lines of text to the record")
    args = parser.parse_args()

    if args.dut is None:
        raise ValueError("need a name for the dut: --dut something")

    update_dut = UpdateDUT(args.mgr, lfjson_port, _debug_on=args.debug)
    update_dut.name = args.dut

    if (args.param is not None):
        for param in args.param:
            if "," not in param:
                raise ValueError("Invalid format for param: %s, please use key,value"%param)
            (name,value) = param.split(",")
            if (args.debug):
                print("name %s = %s"%(name, value))
            if add_dut.dut_params.has(name):
                update_dut.params[name] = value
            else:
                raise ValueError("parameter %s not in dut_params"%name)

    flags_sum = 0
    flags_mask_sum = 0

    if (args.flag is not None):
        for flag in args.flag:
            if "," not in flag:
                raise ValueError("Invalid format for flag: %s, please use flag,(0/1)"%param)
            (name,val_str) = flag.split(",")
            if (args.debug):
                print("name %s = %s"%(name, val_str))
            if not add_dut.dut_flags.has(name):
                raise ValueError("flag %s not in add_dut.dut_flags"%name)
            on_off = (0,1)[val_str=="1"]
            if (args.debug):
                print("name %s = %s"%(name, on_off))
            flags_sum |= (0,add_dut.dut_flags.to_flag(name).value)[on_off]
            flags_mask_sum |= add_dut.dut_flags.to_flag(name).value

    if args.debug:
        print("params %s; flags %s; mask %s"%(",".join(update_dut.params),
                                            hex(flags_sum),
                                            hex(flags_mask_sum)))
    if (args.notes is not None) and (len(args.notes) > 0):
        update_dut.notes = args.notes.copy()
    if (args.append is not None) and (len(args.append) > 0):
        update_dut.append = args.append.copy()

    update_dut.flags = flags_sum
    update_dut.flags_mask = flags_mask_sum

    update_dut.build()
    update_dut.start()


if __name__ == "__main__":
    main()
