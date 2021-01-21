#!/usr/bin/python3

from UnitTestBase import *

parser = argparse.ArgumentParser(description="Query SDK Objects", add_help=False)
parser.add_argument("--type", type=str, help="Type of thing to query",
                    choices=['profile', 'customer', 'location', 'equipment', 'portalUser',
                             'status', 'client-sessions', 'client-info', 'alarm', 'service-metric',
                             'event', 'all'],
                    default = "all")
parser.add_argument("--cmd", type=str, help="Operation to do, default is 'get'",
                    choices=['get', 'delete', 'child_of'],
                    default = "get")
parser.add_argument("--brief", type=str, help="Show output in brief mode?",
                    choices=["true", "false"],
                    default = "false")

base = UnitTestBase("query-sdk", parser)

qtype = base.command_line_args.type
cmd = base.command_line_args.cmd
brief = False
if base.command_line_args.brief == "true":
    brief = True

def get_profile(url, bearer, cust_id, object_id):
    if (object_id == None or object_id.isdigit()):
        return base.cloud.get_customer_profiles(url, bearer, cust_id, object_id)
    else:
        return [base.cloud.get_customer_profile_by_name(url, bearer, cust_id, object_id)]
    
if qtype == 'all' or qtype == 'profile':
    # Get customer profiles
    try:
        if cmd == "get":
            rv = get_profile(base.cloudSDK_url, base.bearer, base.customer_id, base.command_line_args.object_id)
            print("Profiles for customer %s  (%i pages):"%(base.customer_id, len(rv)))
            #jobj = json.load(ssids)
            for r in rv:
                if brief:
                    for p in r['items']:
                        print("Profile id: %s name: %s  type: %s"%(p['id'], p['name'], p['profileType']))
                else:
                    print(json.dumps(r, indent=4, sort_keys=True))

        if cmd == "delete":
            delid = base.command_line_args.object_id;
            if delid.isdigit():
                rv = base.cloud.delete_profile(base.cloudSDK_url, base.bearer, base.command_line_args.object_id)
                print("Delete profile for customer %s, id: %s results:"%(base.customer_id, base.command_line_args.object_id))
                print(rv.json())
            else:
                # Query object by name to find its ID
                targets = get_profile(base.cloudSDK_url, base.bearer, base.customer_id, base.command_line_args.object_id)
                for me in targets:
                    rv = base.cloud.delete_profile(base.cloudSDK_url, base.bearer, str(me['id']))
                    print("Delete profile for customer %s, id: %s results:"%(base.customer_id, base.command_line_args.object_id))
                    print(rv.json())

        if cmd == "child_of":
            targets = get_profile(base.cloudSDK_url, base.bearer, base.customer_id, base.command_line_args.object_id)
            for me in targets:
                meid = me['id']
                print("Profiles using profile: %s %s"%(meid, me['name']))

                # Get all profiles and search
                rv = get_profile(base.cloudSDK_url, base.bearer, base.customer_id, None)
                #jobj = json.load(ssids)
                for r in rv:
                    for p in r['items']:
                        #print("profile: %s %s, checking children..."%(p['id'], p['name']))
                        if 'childProfileIds' in p:
                            for child in p['childProfileIds']:
                                #print("profile: %s %s, checking child: %s  my-id: %s"%(p['id'], p['name'], child, meid))
                                if child == meid:
                                    print("Used-By: %s %s"%(p['id'], p['name']))

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
        if cmd == "get":
            rv = base.cloud.get_customer_equipment(base.cloudSDK_url, base.bearer, base.customer_id)
            print("Equipment for customer %s:"%(base.customer_id))
            #jobj = json.load(ssids)
            for e in rv:
                if brief:
                    for eq in e['items']:
                        print("Equipment id: %s inventoryId: %s profileId: %s type: %s"%(eq['id'], eq['inventoryId'], eq['profileId'], eq['equipmentType']))
                else:
                    print(json.dumps(e, indent=4, sort_keys=True))
        if cmd == "delete":
            delid = base.command_line_args.object_id;
            rv = base.cloud.delete_equipment(base.cloudSDK_url, base.bearer, base.command_line_args.object_id)
            print("Delete Equipment, id: %s results:"%(base.command_line_args.object_id))
            print(rv.json())


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
