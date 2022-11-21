#!/usr/bin/env python3
"""
This script is out-dated, please see py-scripts/test_ipv4_variable_time.py
"""
import sys
import pprint
from pprint import pprint

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

from LANforge.lfcli_base import LFCliBase

class GenericCx(LFCliBase):
    def __init__(self, lfclient_host, lfclient_port, debug_=False):
        super().__init__(lfclient_host, lfclient_port, _debug=debug_)

    def createGenEndp(self, alias=None, shelf=1, resource=1, port=None, type="gen_generic"):
        """
        @deprecated

        :param alias:
        :param shelf:
        :param resource:
        :param port:
        :param type:
        :return:
        """
        return self.create_gen_endp(alias=alias, shelf=shelf, resource=resource, port=port, type=type)

    def create_gen_endp(self, alias=None, shelf=1, resource=1, port=None, type="gen_generic"):
        """
        :param alias: name of connection
        :param shelf: shelf
        :param resource: resource id
        :param port: port
        :param type: gen_generic is what firemod reports, just use this
        :return:
        """
        if port is None:
            raise ValueError("createGenEndp: port required")
        if type is None:
            raise ValueError("createGenEndp: type required")

        data = {
            "alias": alias,
            "shelf": shelf,
            "resource": resource,
            "port": port,
            "type": type
        }
        if self.debug:
            pprint(data)

        self.json_post("cli-json/add_gen_endp", data, debug_=self.debug)

    def setFlags(self, endpName, flagName, val):
        return self.set_flags(endpName, flagName, val)

    def set_flags(self, endpName, flagName, val):
        data = {
            "name": endpName,
            "flag": flagName,
            "val": val
        }
        self.json_post("cli-json/set_endp_flag", data, debug_=self.debug)

    def setCmd(self, endpName, cmd):
        return self.set_cmd(endpName, cmd)

    def set_cmd(self, endpName, cmd):
        data = {
            "name": endpName,
            "command": cmd
        }
        self.json_post("cli-json/set_gen_cmd", data, debug_=self.debug)
