#!/usr/bin/python3

from UnitTestBase import *

parser = argparse.ArgumentParser(description="Query SDK Objects", add_help=False)
parser.add_argument("--type", type=str, help="Type of thing to query",
                    choices=['profile', 'customer', 'location', 'equipment', 'portalUser',
                             'status', 'client-sessions', 'client-info', 'alarm', 'service-metric',
                             'event', 'all'],
                    default = "all")

base = UnitTestBase("query-sdk", parser)

qtype = base.command_line_args.type

if qtype == 'all' or qtype == 'profile':
    # Get customer profiles
    try:
        rv = base.cloud.get_customer_profiles(base.cloudSDK_url, base.bearer, base.customer_id)
        print("Profiles for customer %s  (%i pages):"%(base.customer_id, len(rv)))
        #jobj = json.load(ssids)
        for r in rv:
            print(json.dumps(r, indent=4, sort_keys=True))
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        print("Failed to read customer profiles")

if qtype == 'all' or qtype == 'customer':
    try:
        rv = base.cloud.get_customer(base.cloudSDK_url, base.bearer, base.customer_id)
        print("Customer %s:"%(base.customer_id))
        #jobj = json.load(ssids)
        print(json.dumps(rv, indent=4, sort_keys=True))
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        print("Failed to read Customer %i"%(customer_id))

if qtype == 'all' or qtype == 'location':
    # Get location info
    try:
        # NOTE:  Could also use base.customer_id to get single one that user may have specified.
        rv = base.cloud.get_customer_locations(base.cloudSDK_url, base.bearer, base.customer_id)
        print("Locations for customer %s:"%(base.customer_id))
        #jobj = json.load(ssids)
        print(json.dumps(rv, indent=4, sort_keys=True))
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        print("Failed to read Customer %s locations"%(base.customer_id))

if qtype == 'all' or qtype == 'equipment':
    # Get equipment info
    try:
        rv = base.cloud.get_customer_equipment(base.cloudSDK_url, base.bearer, base.customer_id)
        print("Equipment for customer %s:"%(base.customer_id))
        #jobj = json.load(ssids)
        for e in rv:
            print(json.dumps(e, indent=4, sort_keys=True))
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        print("Failed to read Customer %s equipment"%(base.customer_id))

if qtype == 'all' or qtype == 'portalUser':
    # Get portalUser info
    try:
        rv = base.cloud.get_customer_portal_users(base.cloudSDK_url, base.bearer, base.customer_id)
        print("PortalUsers for customer %s:"%(base.customer_id))
        #jobj = json.load(ssids)
        for e in rv:
            print(json.dumps(e, indent=4, sort_keys=True))
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        print("Failed to read Customer %s portalUsers"%(base.customer_id))

if qtype == 'all' or qtype == 'status':
    # Get status info
    try:
        rv = base.cloud.get_customer_status(base.cloudSDK_url, base.bearer, base.customer_id)
        print("Status for customer %s:"%(base.customer_id))
        #jobj = json.load(ssids)
        for e in rv:
            print(json.dumps(e, indent=4, sort_keys=True))
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        print("Failed to read Customer %s status"%(base.customer_id))

if qtype == 'all' or qtype == 'client-sessions':
    # Get client sessions info
    try:
        rv = base.cloud.get_customer_client_sessions(base.cloudSDK_url, base.bearer, base.customer_id)
        print("Sessions for customer %s:"%(base.customer_id))
        #jobj = json.load(ssids)
        for e in rv:
            print(json.dumps(e, indent=4, sort_keys=True))
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        print("Failed to read Customer %s sessions"%(base.customer_id))

if qtype == 'all' or qtype == 'client-info':
    # Get clients info
    try:
        rv = base.cloud.get_customer_clients(base.cloudSDK_url, base.bearer, base.customer_id)
        print("Clients for customer %s:"%(base.customer_id))
        #jobj = json.load(ssids)
        for e in rv:
            print(json.dumps(e, indent=4, sort_keys=True))
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        print("Failed to read Customer %s clients"%(base.customer_id))

if qtype == 'all' or qtype == 'alarm':
    # Get alarms info
    try:
        rv = base.cloud.get_customer_alarms(base.cloudSDK_url, base.bearer, base.customer_id)
        print("Alarms for customer %s:"%(base.customer_id))
        #jobj = json.load(ssids)
        for e in rv:
            print(json.dumps(e, indent=4, sort_keys=True))
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        print("Failed to read Customer %s alarms"%(base.customer_id))

if qtype == 'all' or qtype == 'service-metric':
    # Get service metrics
    try:
        fromTime = "0"
        toTime = "%i"%(0xFFFFFFFFFFFF)  # something past now, units are msec
        rv = base.cloud.get_customer_service_metrics(base.cloudSDK_url, base.bearer, base.customer_id, fromTime, toTime)
        print("Service Metrics for customer %s:"%(base.customer_id))
        for e in rv:
            #jobj = json.load(ssids)
            print(json.dumps(e, indent=4, sort_keys=True))
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        print("Failed to read Customer %s service metrics"%(base.customer_id))

if qtype == 'all' or qtype == 'event':
    # Get system events
    try:
        fromTime = "0"
        toTime = "%i"%(0xFFFFFFFFFFFF)  # something past now, units are msec
        rv = base.cloud.get_customer_system_events(base.cloudSDK_url, base.bearer, base.customer_id, fromTime, toTime)
        #print("System Events for customer %s:"%(base.customer_id))
        #jobj = json.load(ssids)
        for e in rv:
            print(json.dumps(e, indent=4, sort_keys=True))
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        print("Failed to read Customer %s system events"%(base.customer_id))
