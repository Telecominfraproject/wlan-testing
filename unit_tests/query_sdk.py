#!/usr/bin/python3

from UnitTestBase import *

base = UnitTestBase("query-sdk")

# Get customer profiles
try:
    ssids = base.cloud.get_customer_profiles(base.cloudSDK_url, base.bearer, base.customer_id)
    print("Profiles for customer %s:"%(base.customer_id))
    #jobj = json.load(ssids)
    print(json.dumps(ssids, indent=4, sort_keys=True))
except Exception as ex:
    print(ex)
    logging.error(logging.traceback.format_exc())
    print("Failed to read customer profiles")

# Get customer info.  I don't see any way to query for all customer IDs, so just look at first 3 for now.
for customer_id in range(4):
    try:
        # NOTE:  Could also use base.customer_id to get single one that user may have specified.
        ssids = base.cloud.get_customer(base.cloudSDK_url, base.bearer, "%i"%(customer_id))
        print("Customer %i:"%(customer_id))
        #jobj = json.load(ssids)
        print(json.dumps(ssids, indent=4, sort_keys=True))
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        print("Failed to read Customer %i"%(customer_id))
