#!/usr/bin/python3

from UnitTestBase import *

base = UnitTestBase("query-sdk")

# 5G SSIDs
try:
    ssids = base.cloud.get_customer_profiles(base.cloudSDK_url, base.bearer, base.customer_id)
    print("Profiles for customer %s:"%(base.customer_id))
    #jobj = json.load(ssids)
    print(json.dumps(ssids, indent=4, sort_keys=True))
except Exception as ex:
    print(ex)
    logging.error(logging.traceback.format_exc())
    print("Failed to read customer profiles")
