#!/usr/bin/env python3

import sys
import os
import importlib
from pprint import pprint #, pformat


path_hunks = os.path.abspath(__file__).split('/')
while( path_hunks[-1] != 'lanforge-scripts'):
    path_hunks.pop()
sys.path.append(os.path.join("/".join(path_hunks)))
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm

class eggsample(Realm):
    def __init__(self):
        super().__init__("ct521a-lion", 8080);

    def run(self):
        layer3_result = self.cx_list() # this is realm::cx_list()
        pprint(("layer3 result records:", layer3_result))
        layer3_names = [ item["name"] for item in layer3_result.values() if "_links" in item]
        pprint(("layer3 names:", layer3_names))
        #LFUtils.remove_cx(self.url, layer3_names)


def main():
    egg = eggsample()
    egg.run()


if __name__ == "__main__":
    main()
#

