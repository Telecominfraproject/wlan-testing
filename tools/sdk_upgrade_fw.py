#!/usr/bin/python3 -u

# Example to upgrade firmware on NOLA-12 testbed:
"""
./sdk_upgrade_fw.py --testrail-user-id NONE --model wf188n --ap-jumphost-address localhost --ap-jumphost-port 8823 \
  --ap-jumphost-password pumpkin77 --ap-jumphost-tty /dev/ttyAP1 --testbed \"NOLA-12\" \
  --sdk-base-url https://wlan-portal-svc-ben-testbed.cicd.lab.wlan.tip.build --force-upgrade true

  # Use specified firmware image, not just the latest.
  ./sdk_upgrade_fw.py --testrail-user-id NONE --model wf188n --ap-jumphost-address localhost --ap-jumphost-port 8823 \
  --ap-jumphost-password pumpkin77 --ap-jumphost-tty /dev/ttyAP1 --testbed \"NOLA-12\" \
  --sdk-base-url https://wlan-portal-svc-ben-testbed.cicd.lab.wlan.tip.build --ap-image wf188n-2021-02-01-pending-686c4df --verbose

# Example to upgrade fw on NOLA-01 testbed
./sdk_upgrade_fw.py --testrail-user-id NONE --model ecw5410 --ap-jumphost-address localhost --ap-jumphost-port 8803 \
  --ap-jumphost-password pumpkin77 --ap-jumphost-tty /dev/ttyAP1 --testbed \"NOLA-01\" \
  --sdk-base-url https://wlan-portal-svc.cicd.lab.wlan.tip.build --verbose

"""

import sys

sys.path.append(f'../tests')

from UnitTestBase import *
from JfrogHelper import *
from cloudsdk import CreateAPProfiles

parser = argparse.ArgumentParser(description="SDK Upgrade Firmware", add_help=False)
parser.add_argument("--ap-image", type=str,
                    help="Specify an AP image to install.  Will use latest found on jfrog if this is not specified.",
                    default=None)
base = UnitTestBase("sdk-upgrade-fw", parser)

command_line_args = base.command_line_args


# cmd line takes precedence over env-vars.
cloudSDK_url = command_line_args.sdk_base_url       # was os.getenv('CLOUD_SDK_URL')
local_dir = command_line_args.local_dir             # was os.getenv('SANITY_LOG_DIR')
report_path = command_line_args.report_path         # was os.getenv('SANITY_REPORT_DIR')
report_template = command_line_args.report_template  # was os.getenv('REPORT_TEMPLATE')

## TestRail Information
tr_user = command_line_args.testrail_user_id        # was os.getenv('TR_USER')
tr_pw = command_line_args.testrail_user_password    # was os.getenv('TR_PWD')
milestoneId = command_line_args.milestone           # was os.getenv('MILESTONE')
projectId = command_line_args.testrail_project      # was os.getenv('PROJECT_ID')
testRunPrefix = command_line_args.testrail_run_prefix # os.getenv('TEST_RUN_PREFIX')

##Jfrog credentials
jfrog_user = command_line_args.jfrog_user_id        # was os.getenv('JFROG_USER')
jfrog_pwd = command_line_args.jfrog_user_password   # was os.getenv('JFROG_PWD')

##EAP Credentials
identity = command_line_args.eap_id                 # was os.getenv('EAP_IDENTITY')
ttls_password = command_line_args.ttls_password     # was os.getenv('EAP_PWD')

## AP Credentials
ap_username = command_line_args.ap_username         # was os.getenv('AP_USER')

##LANForge Information
lanforge_ip = command_line_args.lanforge_ip_address
lanforge_port = command_line_args.lanforge_port_number
lanforge_prefix = command_line_args.lanforge_prefix

build = command_line_args.build_id

logger = base.logger
hdlr = base.hdlr

client: TestRail_Client = TestRail_Client(command_line_args)
rid = 0 # testrails run-id, not actually supported at the moment.

###Get Cloud Bearer Token
cloud: CloudSDK = CloudSDK(command_line_args)
bearer = cloud.get_bearer(cloudSDK_url, cloud_type)

cloud.assert_bad_response = True

model_id = command_line_args.model
equipment_id = command_line_args.equipment_id

print("equipment-id: %s"%(equipment_id))

if equipment_id == "-1":
    eq_id = ap_ssh_ovsh_nodec(command_line_args, 'id')
    print("EQ Id: %s"%(eq_id))

    # Now, query equipment to find something that matches.
    eq = cloud.get_customer_equipment(cloudSDK_url, bearer, customer_id)
    for item in eq:
        for e in item['items']:
            print(e['id'], "  ", e['inventoryId'])
            if e['inventoryId'].endswith("_%s"%(eq_id)):
                print("Found equipment ID: %s  inventoryId: %s"%(e['id'], e['inventoryId']))
                equipment_id = str(e['id'])

if equipment_id == -1:
    print("ERROR:  Could not find equipment-id.")
    sys.exit(1)

###Get Current AP Firmware and upgrade
try:
    ap_cli_info = ssh_cli_active_fw(command_line_args)
    ap_cli_fw = ap_cli_info['active_fw']
except Exception as ex:
    print(ex)
    logging.error(logging.traceback.format_exc())
    ap_cli_info = "ERROR"
    print("FAILED:  Cannot Reach AP CLI.");
    sys.exit(1)

fw_model = ap_cli_fw.partition("-")[0]
print('Current Active AP FW from CLI:', ap_cli_fw)

############################################################################
#################### Create Report #########################################
############################################################################

# Create Report Folder for Today
today = str(date.today())
try:
    os.mkdir(report_path + today)
except OSError:
    print("Creation of the directory %s failed" % report_path)
else:
    print("Successfully created the directory %s " % report_path)

logger.info('Report data can be found here: ' + report_path + today)

###Dictionaries
ap_image = command_line_args.ap_image

############################################################################
#################### Jfrog Firmware Check ##################################
############################################################################

apModel = model_id
cloudModel = cloud_sdk_models[apModel]
if not ap_image:
    # then get latest from jfrog
    # print(cloudModel)
    jfrog_url = 'https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/'
    url = jfrog_url + apModel + "/dev/"
    Build: GetBuild = GetBuild(jfrog_user, jfrog_pwd)
    latest_image = Build.get_latest_image(url, build)
    print(apModel, "Latest FW on jFrog:", latest_image)
    ap_image = latest_image

##Get Bearer Token to make sure its valid (long tests can require re-auth)
bearer = cloud.get_bearer(cloudSDK_url, cloud_type)

print("AP MODEL UNDER TEST IS", model_id)
try:
    ap_cli_info = ssh_cli_active_fw(command_line_args)
    ap_cli_fw = ap_cli_info['active_fw']
except Exception as ex:
    print(ex)
    logging.error(logging.traceback.format_exc())
    ap_cli_info = "ERROR"
    print("Cannot Reach AP CLI, will not test this variant");
    sys.exit(1)

fw_model = ap_cli_fw.partition("-")[0]
print('Current Active AP FW from CLI:', ap_cli_fw)
###Find Latest FW for Current AP Model and Get FW ID

##Compare Latest and Current AP FW and Upgrade
report_data = None

do_upgrade = cloud.should_upgrade_ap_fw(bearer, command_line_args, report_data, ap_image, fw_model, ap_cli_fw,
                                        logger)

cloudModel = cloud_sdk_models[model_id]
pf = cloud.do_upgrade_ap_fw(bearer, command_line_args, report_data, test_cases, client,
                            ap_image, cloudModel, model_id, jfrog_user, jfrog_pwd, rid,
                            customer_id, equipment_id, logger)

if pf:
    sys.exit(0)

sys.exit(1)


