#!/usr/bin/python3
import sys
import urllib

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

import time
from time import sleep
from urllib import error
import pprint
import LANforge
from LANforge import LFRequest
from LANforge import LFUtils
from LANforge.LFUtils import NA


j_printer = pprint.PrettyPrinter(indent=2)
# typically you're using resource 1 in stand alone realm
resource_id = 1

def main():
    base_url = "http://localhost:8080"
    json_post = ""
    json_response = ""

    # see if there are old wanlinks to remove
    json_post = LFRequest.LFRequest(base_url+"/layer4/list")
    try:
        json_response = json_post.getAsJson()
        LFUtils.debug_printer.pprint(json_response)

    except urllib.error.HTTPError as error:
        j_printer.pprint(error)

    add_l4_endp_url = base_url + "/cli-json/add_l4_endp";
    json_post = LFRequest.LFRequest(add_l4_endp_url)
    json_post.addPostData({
            "shelf":1,
            "resource":1,
            "port":"sta00500",
            "type":"l4_generic",
            "timeout":2000,
            "url_rate":600,
            # this produces an error that should be listed in headers
            "URL":"dl http://10.40.0.1/ /dev/null"
    })
    json_response = json_post.jsonPost(True);
    j_printer.pprint(json_response)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    main()

###
###