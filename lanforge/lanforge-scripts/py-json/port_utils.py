#!/usr/bin/env python3

class PortUtils():
    def __init__(self, local_realm):
        self.local_realm = local_realm

    def set_ftp(self, port_name="", resource=1, on=False):
        if port_name != "":
            data = {
                "shelf": 1,
                "resource": resource,
                "port": port_name,
                "current_flags": 0,
                "interest": 0
            }

            if on:
                data["current_flags"] = 0x400000000000
                data["interest"] = 0x10000000
            else:
                data["interest"] = 0x10000000

            self.local_realm.json_post("cli-json/set_port", data)
        else:
            raise ValueError("Port name required")

    def set_http(self, port_name="", resource=1, on=False):
        if port_name != "":
            data = {
                "shelf": 1,
                "resource": resource,
                "port": port_name,
                "current_flags": 0,
                "interest": 0
            }

            if on:
                data["current_flags"] = 0x200000000000
                data["interest"] = 0x8000000
            else:
                data["interest"] = 0x8000000

            self.local_realm.json_post("cli-json/set_port", data)
        else:
            raise ValueError("Port name required")
