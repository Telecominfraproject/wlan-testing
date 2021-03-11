#!/usr/bin/python3

import base64
import urllib.request
from bs4 import BeautifulSoup
import ssl
import subprocess, os
from artifactory import ArtifactoryPath
import tarfile
import paramiko
from paramiko import SSHClient
from scp import SCPClient
import os
import pexpect
from pexpect import pxssh
import sys
import paramiko
from scp import SCPClient
import pprint
from pprint import pprint
from os import listdir
import re
import requests
import json
import testrail
import logging
import datetime
import time
from datetime import date
from shutil import copyfile
import argparse
import importlib

# For finding files
# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
import glob

# external_results_dir=/var/tmp/lanforge

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)
for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../../lanforge/lanforge-scripts/{folder}')


#sys.path.append(f'../../libs/testrails')
#sys.path.append(f'../../libs/apnos')
#sys.path.append(f'../../libs/cloudsdk')
sys.path.append(f'../../libs')
#sys.path.append(f'../test_utility/')
sys.path.append(f'../../libs/lanforge')
sys.path.append(f'../')
sys.path.append('test_bed_info')

from LANforge.LFUtils import *

# if you lack __init__.py in this directory you will not find sta_connect module#

if 'py-json' not in sys.path:
    sys.path.append('../../py-scripts')

import sta_connect2
from sta_connect2 import StaConnect2
import testrail
import eap_connect
from eap_connect import EAPConnect
import cloud_connect
from cloud_connect import CloudSDK
import ap_connect
from ap_connect import ssh_cli_active_fw
from ap_connect import iwinfo_status

###Class for jfrog Interaction
class GetBuild:
    def __init__(self):
        self.user = jfrog_user
        self.password = jfrog_pwd
        ssl._create_default_https_context = ssl._create_unverified_context

    def get_latest_image(self, url, build):
        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()
        headers = {'Authorization': 'Basic ' + auth}

        ''' FIND THE LATEST FILE NAME'''
        # print(url)
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html, features="html.parser")
        ##find the last pending link on dev
        last_link = soup.find_all('a', href=re.compile(build))[-1]
        latest_file = last_link['href']
        latest_fw = latest_file.replace('.tar.gz', '')
        return latest_fw


###Class for Tests
class RunTest:
    def Single_Client_Connectivity(self, port, radio, prefix, ssid_name, ssid_psk, security, station, test_case, rid):
        '''SINGLE CLIENT CONNECTIVITY using test_connect2.py'''
        staConnect = StaConnect2(lanforge_ip, 8080, debug_=False)
        staConnect.sta_mode = 0
        staConnect.upstream_resource = 1
        staConnect.upstream_port = port
        staConnect.radio = radio
        staConnect.resource = 1
        staConnect.dut_ssid = ssid_name
        staConnect.dut_passwd = ssid_psk
        staConnect.dut_security = security
        staConnect.station_names = station
        staConnect.sta_prefix = prefix
        staConnect.runtime_secs = 10
        staConnect.bringup_time_sec = 60
        staConnect.cleanup_on_exit = True
        # staConnect.cleanup()
        staConnect.setup()
        staConnect.start()
        print("napping %f sec" % staConnect.runtime_secs)
        time.sleep(staConnect.runtime_secs)
        staConnect.stop()
        staConnect.cleanup()
        run_results = staConnect.get_result_list()
        for result in run_results:
            print("test result: " + result)
        # result = 'pass'
        print("Single Client Connectivity :", staConnect.passes)
        if staConnect.passes() == True:
            print("Single client connection to", ssid_name, "successful. Test Passed")
            client.update_testrail(case_id=test_case, run_id=rid, status_id=1, msg='Client connectivity passed')
            logger.info("Client connectivity to " + ssid_name + " Passed")
            return ("passed")
        else:
            client.update_testrail(case_id=test_case, run_id=rid, status_id=5, msg='Client connectivity failed')
            print("Single client connection to", ssid_name, "unsuccessful. Test Failed")
            logger.warning("Client connectivity to " + ssid_name + " FAILED")
            return ("failed")

    def Single_Client_EAP(port, sta_list, ssid_name, radio, sta_prefix, security, eap_type, identity, ttls_password, test_case,
                          rid):
        eap_connect = EAPConnect(lanforge_ip, 8080, _debug_on=False)
        eap_connect.upstream_resource = 1
        eap_connect.upstream_port = port
        eap_connect.security = security
        eap_connect.sta_list = sta_list
        eap_connect.station_names = sta_list
        eap_connect.sta_prefix = sta_prefix
        eap_connect.ssid = ssid_name
        eap_connect.radio = radio
        eap_connect.eap = eap_type
        eap_connect.identity = identity
        eap_connect.ttls_passwd = ttls_password
        eap_connect.runtime_secs = 10
        eap_connect.setup()
        eap_connect.start()
        print("napping %f sec" % eap_connect.runtime_secs)
        time.sleep(eap_connect.runtime_secs)
        eap_connect.stop()
        eap_connect.cleanup()
        run_results = eap_connect.get_result_list()
        for result in run_results:
            print("test result: " + result)
        # result = 'pass'
        print("Single Client Connectivity :", eap_connect.passes)
        if eap_connect.passes() == True:
            print("Single client connection to", ssid_name, "successful. Test Passed")
            client.update_testrail(case_id=test_case, run_id=rid, status_id=1, msg='Client connectivity passed')
            logger.info("Client connectivity to " + ssid_name + " Passed")
            return ("passed")
        else:
            client.update_testrail(case_id=test_case, run_id=rid, status_id=5, msg='Client connectivity failed')
            print("Single client connection to", ssid_name, "unsuccessful. Test Failed")
            logger.warning("Client connectivity to " + ssid_name + " FAILED")
            return ("failed")

    def testrail_retest(self, test_case, rid, ssid_name):
        client.update_testrail(case_id=test_case, run_id=rid, status_id=4,
                               msg='Error in Client Connectivity Test. Needs to be Re-run')
        print("Error in test for single client connection to", ssid_name)
        logger.warning("ERROR testing Client connectivity to " + ssid_name)


# Command Line Args
parser = argparse.ArgumentParser(description="Sanity Testing on Firmware Build")
parser.add_argument("-b", "--build", type=str, default="pending",
                    help="FW commit ID (latest pending build on dev is default)")
parser.add_argument("-i", "--ignore", type=str, default='no', choices=['yes', 'no'],
                    help="Set to 'no' to ignore current running version on AP and run sanity including upgrade")
# parser.add_argument("-r", "--report", type=str, default=report_path, help="Report directory path other than default - directory must already exist!")
parser.add_argument("-m", "--model", type=str, choices=['ea8300', 'ecw5410', 'ecw5211', 'ec420', "wf188n", "wf194c", "ex227", "ex447", "eap101", "eap102"],
                    help="AP model to be run")
parser.add_argument("-f", "--file", type=str, help="Test Info file name", default="test_info")
# parser.add_argument("--tr_prefix", type=str, default=testRunPrefix, help="Testrail test run prefix override (default is Env variable)")
parser.add_argument("--skip_upgrade", dest="skip_upgrade", action='store_true', help="Skip Upgrade testing")
parser.set_defaults(skip_eap=False)
parser.add_argument("--skip_eap", dest="skip_eap", action='store_true', help="Skip EAP testing")
parser.set_defaults(skip_eap=False)
parser.add_argument("--skip_bridge", dest="skip_bridge", action='store_true', help="Skip Bridge testing")
parser.set_defaults(skip_bridge=False)
parser.add_argument("--skip_nat", dest="skip_nat", action='store_true', help="Skip NAT testing")
parser.set_defaults(skip_nat=False)
parser.add_argument("--skip_vlan", dest="skip_vlan", action='store_true', help="Skip VLAN testing")
parser.set_defaults(skip_vlan=False)
args = parser.parse_args()

build = args.build
ignore = args.ignore
# report_path = args.report
test_file = args.file

# Import info for lab setup and APs under test
file = os.path.splitext(test_file)[0]
if '/' in test_file:
    path, file = os.path.split(file)
    sys.path.append(path)
    test_info = importlib.import_module(file)
else:
    test_info = importlib.import_module(file)

# AP Upgrade
jfrog_user = test_info.jfrog_user
jfrog_pwd = test_info.jfrog_pass
ap_username = test_info.ap_user

# Testrail info
testrail_url = test_info.tr_url
tr_user = test_info.tr_user
tr_pw = test_info.tr_pass
milestoneId = test_info.milestone
testRunPrefix = test_info.tr_prefix
projectId = test_info.tr_project_id
client = testrail.APIClient(testrail_url, tr_user, tr_pw, projectId)

# Directory Paths
local_dir = test_info.sanity_log_dir
report_path = test_info.sanity_report_dir
report_template = test_info.report_template

# Equipment info
equipment_id_dict = test_info.equipment_id_dict
equipment_ids = equipment_id_dict
profile_info_dict = test_info.profile_info_dict
cloud_sdk_models = test_info.cloud_sdk_models
equipment_ip_dict = test_info.equipment_ip_dict
equipment_credentials_dict = test_info.equipment_credentials_dict
ap_models = test_info.ap_models
customer_id = test_info.customer_id
cloud_type = test_info.cloud_type
test_cases = test_info.test_cases

# CloudSDK info
cloudSDK_url = test_info.cloudSDK_url
cloud_user = test_info.cloud_user
cloud_password = test_info.cloud_password

# RADIUS info and EAP credentials
radius_info = test_info.radius_info
identity = test_info.radius_info["eap_identity"]
ttls_password = test_info.radius_info["eap_pwd"]

if args.model is not None:
    model_id = args.model
    equipment_ids = {
        model_id: equipment_id_dict[model_id]
    }
    print("User requested test on equipment ID:",equipment_ids)

logger = logging.getLogger('Nightly_Sanity')
hdlr = logging.FileHandler(local_dir + "/Nightly_Sanity.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# if args.tr_prefix is not None:
#     testRunPrefix = args.tr_prefix

##LANForge Information
lanforge_ip = test_info.lanforge_ip
#lanforge_prefix = test_info.lanforge_prefix

print("Start of Sanity Testing...")
print("Test file used will be: "+test_file)
print("TestRail Test Run Prefix is: "+testRunPrefix)
print("Skipping Upgrade Tests? " + str(args.skip_upgrade))
print("Skipping EAP Tests? " + str(args.skip_eap))
print("Skipping Bridge Tests? " + str(args.skip_bridge))
print("Skipping NAT Tests? " + str(args.skip_nat))
print("Skipping VLAN Tests? " + str(args.skip_vlan))
print("Testing Latest Build with Tag: " + build)

if ignore == 'yes':
    print("Will ignore if AP is already running build under test and run sanity regardless...")
else:
    print("Checking for APs requiring upgrade to latest build...")

######Testrail Project and Run ID Information ##############################

Test: RunTest = RunTest()

projId = client.get_project_id(project_name=projectId)
print("TIP WLAN Project ID is:", projId)

logger.info('Start of Nightly Sanity')

###Dictionaries
ap_latest_dict = {
    "ec420": "Unknown",
    "ea8300": "Unknown",
    "ecw5211": "unknown",
    "ecw5410": "unknown"
}

# import json file used by throughput test
sanity_status = json.load(open("sanity_status.json"))

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

# Copy report template to folder. If template doesn't exist, continue anyway with log
try:
    copyfile(report_template, report_path + today + '/report.php')

except:
    print("No report template created. Report data will still be saved. Continuing with tests...")

##Create report_data dictionary
tc_results = dict.fromkeys(test_cases.values(), "not run")

report_data = dict()
report_data["cloud_sdk"] = dict.fromkeys(ap_models, "")
for key in report_data["cloud_sdk"]:
    report_data["cloud_sdk"][key] = {
        "date": "N/A",
        "commitId": "N/A",
        "projectVersion": "N/A"
    }
report_data["fw_available"] = dict.fromkeys(ap_models, "Unknown")
report_data["fw_under_test"] = dict.fromkeys(ap_models, "N/A")
report_data['pass_percent'] = dict.fromkeys(ap_models, "")

report_data['tests'] = dict.fromkeys(ap_models, "")
for key in ap_models:
    report_data['tests'][key] = dict.fromkeys(test_cases.values(), "not run")
print(report_data)

# write to report_data contents to json file so it has something in case of unexpected fail
with open(report_path + today + '/report_data.json', 'w') as report_json_file:
    json.dump(report_data, report_json_file)

###Get Cloud Bearer Token
bearer = CloudSDK.get_bearer(cloudSDK_url, cloud_type, cloud_user, cloud_password)

############################################################################
#################### Jfrog Firmware Check ##################################
############################################################################

for model in ap_models:
    apModel = model
    cloudModel = cloud_sdk_models[apModel]
    # print(cloudModel)
    ###Check Latest FW on jFrog
    jfrog_url = 'https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/'
    url = jfrog_url + apModel + "/dev/"
    Build: GetBuild = GetBuild()
    latest_image = Build.get_latest_image(url, build)
    print(model, "Latest FW on jFrog:", latest_image)
    ap_latest_dict[model] = latest_image

print(ap_latest_dict)
####################################################################################
############ Update FW and Run Test Cases on Each AP Variant #######################
####################################################################################
####################################################################################

for key in equipment_ids:
    ##Get Bearer Token to make sure its valid (long tests can require re-auth)
    bearer = CloudSDK.get_bearer(cloudSDK_url, cloud_type, cloud_user, cloud_password)

    ###Get Current AP Firmware and upgrade
    equipment_id = equipment_id_dict[key]
    ap_ip = equipment_ip_dict[key]
    ap_username = "root"
    ap_password = equipment_credentials_dict[key]
    print("AP MODEL UNDER TEST IS", key)
    try:
        ap_cli_info = ssh_cli_active_fw(ap_ip, ap_username, ap_password)
        ap_cli_fw = ap_cli_info['active_fw']
    except:
        ap_cli_info = "ERROR"
        print("Cannot Reach AP CLI, will not test this variant")
        report_data["pass_percent"][key] = "AP offline"
        continue

    fw_model = ap_cli_fw.partition("-")[0]
    print('Current Active AP FW from CLI:', ap_cli_fw)

    if ap_cli_info['state'] != "active":
        print('Manager Status not Active. Skipping AP Model!')
        report_data["pass_percent"][key] = "AP offline"
        continue

    else:
       print('Manager Status Active. Proceed with tests...')
    ###Find Latest FW for Current AP Model and Get FW ID
    ##Compare Latest and Current AP FW and Upgrade
    latest_ap_image = ap_latest_dict[fw_model]

    if ap_cli_fw == latest_ap_image and ignore == 'no' and args.skip_upgrade != True:
        print('FW does not require updating')
        report_data['fw_available'][key] = "No"
        logger.info(fw_model + " does not require upgrade. Not performing sanity tests for this AP variant")
        cloudsdk_cluster_info = {
            "date": "N/A",
            "commitId": "N/A",
            "projectVersion": "N/A"
        }
        report_data['cloud_sdk'][key] = cloudsdk_cluster_info

    else:
        if ap_cli_fw == latest_ap_image and ignore == "yes":
            print('AP is already running FW version under test. Ignored based on ignore flag')
            report_data['fw_available'][key] = "Yes"
        elif args.skip_upgrade == True:
            print("User requested to skip upgrade, will use existing version and not upgrade AP")
            report_data['fw_available'][key] = "N/A"
            report_data['fw_under_test'][key] = ap_cli_fw
            latest_ap_image = ap_cli_fw
        else:
            print('FW needs updating')
        report_data['fw_available'][key] = "Yes"
        report_data['fw_under_test'][key] = latest_ap_image

        ###Create Test Run
        today = str(date.today())
        now = datetime.datetime.now()
        case_ids = list(test_cases.values())

        ##Remove unused test cases based on command line arguments

        # Skip upgrade argument
        if args.skip_upgrade == True:
            case_ids.remove(test_cases["upgrade_api"])
        else:
            pass

        # Skip Bridge argument
        if args.skip_bridge == True:
            for x in test_cases:
                if "bridge" in x:
                    case_ids.remove(test_cases[x])
        else:
            pass

        # Skip NAT argument
        if args.skip_nat == True:
            for x in test_cases:
                if "nat" in x:
                    case_ids.remove(test_cases[x])
        else:
            pass

        # Skip VLAN argument
        if args.skip_vlan == True:
            for x in test_cases:
                if "vlan" in x:
                    case_ids.remove(test_cases[x])
        else:
            pass

        # Skip EAP argument
        if args.skip_eap == True:
            case_ids.remove(test_cases["radius_profile"])
            for x in test_cases:
                if "eap" in x and test_cases[x] in case_ids:
                    case_ids.remove(test_cases[x])
        else:
            pass

        test_run_name = testRunPrefix + fw_model + "_" + today + "_" + latest_ap_image
        client.create_testrun(name=test_run_name, case_ids=case_ids, project_id=projId, milestone_id=milestoneId,
                              description="Automated Nightly Sanity test run for new firmware build")
        rid = client.get_run_id(test_run_name=testRunPrefix + fw_model + "_" + today + "_" + latest_ap_image)
        print("TIP run ID is:", rid)

        ###GetCloudSDK Version
        print("Getting CloudSDK version information...")
        try:
            cluster_ver = CloudSDK.get_cloudsdk_version(cloudSDK_url, bearer)
            print("CloudSDK Version Information:")
            print("-------------------------------------------")
            print(cluster_ver)
            print("-------------------------------------------")

            cloudsdk_cluster_info = {}
            cloudsdk_cluster_info['date'] = cluster_ver['commitDate']
            cloudsdk_cluster_info['commitId'] = cluster_ver['commitID']
            cloudsdk_cluster_info['projectVersion'] = cluster_ver['projectVersion']
            report_data['cloud_sdk'][key] = cloudsdk_cluster_info
            client.update_testrail(case_id=test_cases["cloud_ver"], run_id=rid, status_id=1,
                                   msg='Read CloudSDK version from API successfully')
            report_data['tests'][key][test_cases["cloud_ver"]] = "passed"

        except:
            cluster_ver = 'error'
            print("ERROR: CloudSDK Version Unavailable")
            logger.info('CloudSDK version Unavailable')
            cloudsdk_cluster_info = {
                "date": "unknown",
                "commitId": "unknown",
                "projectVersion": "unknown"
            }
            client.update_testrail(case_id=test_cases["cloud_ver"], run_id=rid, status_id=5,
                                   msg='Could not read CloudSDK version from API')
            report_data['cloud_sdk'][key] = cloudsdk_cluster_info
            report_data['tests'][key][test_cases["cloud_ver"]] = "failed"

        with open(report_path + today + '/report_data.json', 'w') as report_json_file:
            json.dump(report_data, report_json_file)

        # Update TR Testrun with CloudSDK info for use in QA portal
        sdk_description = cloudsdk_cluster_info["date"]+" (Commit ID: "+cloudsdk_cluster_info["commitId"]+")"
        update_test = client.update_testrun(rid,sdk_description)
        print(update_test)

        # Test Create Firmware Version
        test_id_fw = test_cases["create_fw"]
        latest_image = ap_latest_dict[key]
        cloudModel = cloud_sdk_models[key]
        print(cloudModel)
        firmware_list_by_model = CloudSDK.CloudSDK_images(cloudModel, cloudSDK_url, bearer)
        print("Available", cloudModel, "Firmware on CloudSDK:", firmware_list_by_model)

        if latest_image in firmware_list_by_model:
            print("Latest Firmware", latest_image, "is already on CloudSDK, need to delete to test create FW API")
            old_fw_id = CloudSDK.get_firmware_id(latest_image, cloudSDK_url, bearer)
            delete_fw = CloudSDK.delete_firmware(str(old_fw_id), cloudSDK_url, bearer)
            fw_url = "https://" + jfrog_user + ":" + jfrog_pwd + "@tip.jfrog.io/artifactory/tip-wlan-ap-firmware/" + key + "/dev/" + latest_image + ".tar.gz"
            commit = latest_image.split("-")[-1]
            try:
                fw_upload_status = CloudSDK.firwmare_upload(commit, cloudModel, latest_image, fw_url, cloudSDK_url,
                                                            bearer)
                fw_id = fw_upload_status['id']
                print("Upload Complete.", latest_image, "FW ID is", fw_id)
                client.update_testrail(case_id=test_id_fw, run_id=rid, status_id=1,
                                       msg='Create new FW version by API successful')
                report_data['tests'][key][test_id_fw] = "passed"
            except:
                fw_upload_status = 'error'
                print("Unable to upload new FW version. Skipping Sanity on AP Model")
                client.update_testrail(case_id=test_id_fw, run_id=rid, status_id=5,
                                       msg='Error creating new FW version by API')
                report_data['tests'][key][test_id_fw] = "failed"
                continue
        else:
            print("Latest Firmware is not on CloudSDK! Uploading...")
            fw_url = "https://" + jfrog_user + ":" + jfrog_pwd + "@tip.jfrog.io/artifactory/tip-wlan-ap-firmware/" + key + "/dev/" + latest_image + ".tar.gz"
            commit = latest_image.split("-")[-1]
            try:
                fw_upload_status = CloudSDK.firwmare_upload(commit, cloudModel, latest_image, fw_url, cloudSDK_url,
                                                            bearer)
                fw_id = fw_upload_status['id']
                print("Upload Complete.", latest_image, "FW ID is", fw_id)
                client.update_testrail(case_id=test_id_fw, run_id=rid, status_id=1,
                                       msg='Create new FW version by API successful')
                report_data['tests'][key][test_id_fw] = "passed"
            except:
                fw_upload_status = 'error'
                print("Unable to upload new FW version. Skipping Sanity on AP Model")
                client.update_testrail(case_id=test_id_fw, run_id=rid, status_id=5,
                                       msg='Error creating new FW version by API')
                report_data['tests'][key][test_id_fw] = "failed"
                continue

        # Upgrade AP firmware
        if args.skip_upgrade == True:
            print("User Requested to Not Performing Upgrade, skipping to Connectivity Tests")
        else:
            print("Upgrading...firmware ID is: ", fw_id)
            upgrade_fw = CloudSDK.update_firmware(equipment_id, str(fw_id), cloudSDK_url, bearer)
            logger.info("Lab " + fw_model + " Requires FW update")
            print(upgrade_fw)

            if "success" in upgrade_fw:
                if upgrade_fw["success"] == True:
                    print("CloudSDK Upgrade Request Success")
                    report_data['tests'][key][test_cases["upgrade_api"]] = "passed"
                    client.update_testrail(case_id=test_cases["upgrade_api"], run_id=rid, status_id=1,
                                           msg='Upgrade request using API successful')
                    logger.info('Firmware upgrade API successfully sent')
                else:
                    print("Cloud SDK Upgrade Request Error!")
                    # mark upgrade test case as failed with CloudSDK error
                    client.update_testrail(case_id=test_cases["upgrade_api"], run_id=rid, status_id=5,
                                           msg='Error requesting upgrade via API')
                    report_data['tests'][key][test_cases["upgrade_api"]] = "failed"
                    logger.warning('Firmware upgrade API failed to send')
                    continue
            else:
                print("Cloud SDK Upgrade Request Error!")
                # mark upgrade test case as failed with CloudSDK error
                client.update_testrail(case_id=test_cases["upgrade_api"], run_id=rid, status_id=5,
                                       msg='Error requesting upgrade via API')
                report_data['tests'][key][test_cases["upgrade_api"]] = "failed"
                logger.warning('Firmware upgrade API failed to send')
                continue

            time.sleep(300)

        # Check if upgrade success is displayed on CloudSDK
        test_id_cloud = test_cases["cloud_fw"]
        cloud_ap_fw = CloudSDK.ap_firmware(customer_id, equipment_id, cloudSDK_url, bearer)
        print('Current AP Firmware from CloudSDK:', cloud_ap_fw)
        logger.info('AP Firmware from CloudSDK: ' + cloud_ap_fw)
        if cloud_ap_fw == "ERROR":
            print("AP FW Could not be read from CloudSDK")

        elif cloud_ap_fw == latest_ap_image:
            print("CloudSDK status shows upgrade successful!")

        else:
            print("AP FW from CloudSDK status is not latest build. Will check AP CLI.")

        # Check if upgrade successful on AP CLI
        test_id_cli = test_cases["ap_upgrade"]
        try:
            ap_cli_info = ssh_cli_active_fw(ap_ip, ap_username, ap_password)
            ap_cli_fw = ap_cli_info['active_fw']
            print("CLI reporting AP Active FW as:", ap_cli_fw)
            logger.info('Firmware from CLI: ' + ap_cli_fw)
        except:
            ap_cli_info = "ERROR"
            print("Cannot Reach AP CLI to confirm upgrade!")
            logger.warning('Cannot Reach AP CLI to confirm upgrade!')
            client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=4,
                                   msg='Cannot reach AP after upgrade to check CLI - re-test required')
            continue

        if cloud_ap_fw == latest_ap_image and ap_cli_fw == latest_ap_image:
            print("CloudSDK and AP CLI both show upgrade success, passing upgrade test case")
            client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=1,
                                   msg='Upgrade to ' + latest_ap_image + ' successful')
            client.update_testrail(case_id=test_id_cloud, run_id=rid, status_id=1,
                                   msg='CLOUDSDK reporting correct firmware version.')
            report_data['tests'][key][test_id_cli] = "passed"
            report_data['tests'][key][test_id_cloud] = "passed"
            print(report_data['tests'][key])

        elif cloud_ap_fw != latest_ap_image and ap_cli_fw == latest_ap_image:
            print("AP CLI shows upgrade success - CloudSDK reporting error!")
            ##Raise CloudSDK error but continue testing
            client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=1,
                                   msg='Upgrade to ' + latest_ap_image + ' successful.')
            client.update_testrail(case_id=test_id_cloud, run_id=rid, status_id=5,
                                   msg='CLOUDSDK reporting incorrect firmware version.')
            report_data['tests'][key][test_id_cli] = "passed"
            report_data['tests'][key][test_id_cloud] = "failed"
            print(report_data['tests'][key])

        elif cloud_ap_fw == latest_ap_image and ap_cli_fw != latest_ap_image:
            print("AP CLI shows upgrade failed - CloudSDK reporting error!")
            # Testrail TC fail
            client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=5,
                                   msg='AP failed to download or apply new FW. Upgrade to ' + latest_ap_image + ' Failed')
            client.update_testrail(case_id=test_id_cloud, run_id=rid, status_id=5,
                                   msg='CLOUDSDK reporting incorrect firmware version.')
            report_data['tests'][key][test_id_cli] = "failed"
            report_data['tests'][key][test_id_cloud] = "failed"
            print(report_data['tests'][key])
            continue

        elif cloud_ap_fw != latest_ap_image and ap_cli_fw != latest_ap_image:
            print("Upgrade Failed! Confirmed on CloudSDK and AP CLI. Upgrade test case failed.")
            ##fail TR testcase and exit
            client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=5,
                                   msg='AP failed to download or apply new FW. Upgrade to ' + latest_ap_image + ' Failed')
            report_data['tests'][key][test_id_cli] = "failed"
            print(report_data['tests'][key])
            continue

        else:
            print("Unable to determine upgrade status. Skipping AP variant")
            # update TR testcase as error
            client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=4,
                                   msg='Cannot determine upgrade status - re-test required')
            report_data['tests'][key][test_id_cli] = "error"
            print(report_data['tests'][key])
            continue

        print(report_data)

        ###Check AP Manager Status
        manager_status = ap_cli_info['state']

        if manager_status != "active":
            print("Manager status is " + manager_status + "! Not connected to the cloud.")
            print("Waiting 30 seconds and re-checking status")
            time.sleep(30)
            ap_cli_info = ssh_cli_active_fw(ap_ip, ap_username, ap_password)
            manager_status = ap_cli_info['state']
            if manager_status != "active":
                print("Manager status is", manager_status, "! Not connected to the cloud.")
                print("Manager status fails multiple checks - failing test case.")
                ##fail cloud connectivity testcase
                client.update_testrail(case_id=test_cases["cloud_connection"], run_id=rid, status_id=5,
                                       msg='CloudSDK connectivity failed')
                report_data['tests'][key][test_cases["cloud_connection"]] = "failed"
                continue
            else:
                print("Manager status is Active. Proceeding to connectivity testing!")
                # TC522 pass in Testrail
                client.update_testrail(case_id=test_cases["cloud_connection"], run_id=rid, status_id=1,
                                       msg='Manager status is Active')
                report_data['tests'][key][test_cases["cloud_connection"]] = "passed"
        else:
            print("Manager status is Active. Proceeding to connectivity testing!")
            # TC5222 pass in testrail
            client.update_testrail(case_id=test_cases["cloud_connection"], run_id=rid, status_id=1,
                                   msg='Manager status is Active')
            report_data['tests'][key][test_cases["cloud_connection"]] = "passed"
            # Pass cloud connectivity test case

        # Update report json
        with open(report_path + today + '/report_data.json', 'w') as report_json_file:
            json.dump(report_data, report_json_file)

        # Create List of Created Profiles to Delete After Test
        delete_list = []

        print("Switching AP's to default profile")
        for id in equipment_id_dict.values():
            ap_profile = CloudSDK.set_ap_profile(id, 6, cloudSDK_url, bearer)
        print('Profile change successful. Deleting profiles that cause potential conflicts...')

        # PROFILE CLEANUP BY NAME
        profile_delete_list = CloudSDK.get_profile_by_name(cloudSDK_url, bearer, customer_id, fw_model + '_5G_EAP_') + \
                              CloudSDK.get_profile_by_name(cloudSDK_url, bearer, customer_id, fw_model + '_5G_WPA_') + \
                              CloudSDK.get_profile_by_name(cloudSDK_url, bearer, customer_id, fw_model + '_2G_EAP_') + \
                              CloudSDK.get_profile_by_name(cloudSDK_url, bearer, customer_id, fw_model + '_2G_WPA_') + \
                              CloudSDK.get_profile_by_name(cloudSDK_url, bearer, customer_id, 'Automation_RADIUS_') + \
                              CloudSDK.get_profile_by_name(cloudSDK_url, bearer, customer_id, "Nightly_Sanity_"
                                                           + fw_model + "_")

        for x in profile_delete_list:
            delete_profile = CloudSDK.delete_profile(cloudSDK_url, bearer, str(x))
            if delete_profile == "SUCCESS":
                print("profile", x, "delete successful")
            else:
                print("Error deleting profile")

        # Create RADIUS profile - used for all EAP SSIDs
        if args.skip_eap != True:
            radius_template = "templates/radius_profile_template.json"
            radius_name = "Automation_RADIUS_"+today
            server_ip = radius_info['server_ip']
            secret = radius_info['secret']
            auth_port = radius_info['auth_port']
            try:
                radius_profile = CloudSDK.create_radius_profile(cloudSDK_url, bearer, radius_template, radius_name, customer_id,
                                                                server_ip, secret,
                                                                auth_port)
                print("radius profile Id is", radius_profile)
                client.update_testrail(case_id=test_cases["radius_profile"], run_id=rid, status_id=1,
                                       msg='RADIUS profile created successfully')
                report_data['tests'][key][test_cases["radius_profile"]] = "passed"
                # Add created RADIUS profile to list for deletion at end of test
                delete_list.append(radius_profile)
            except:
                radius_profile = 'error'
                print("RADIUS Profile Create Error, will use existing profile for tests")
                # Set backup profile ID so test can continue
                radius_profile = test_info.radius_profile
                server_name = "Lab-RADIUS"
                client.update_testrail(case_id=test_cases["radius_profile"], run_id=rid, status_id=5,
                                       msg='Failed to create RADIUS profile')
                report_data['tests'][key][test_cases["radius_profile"]] = "failed"
        else:
            print("Skipped creating RADIUS profile based on skip_eap argument")

        # Set RF Profile Id depending on AP capability
        if test_info.ap_spec[key] == "wifi5":
            rfProfileId = test_info.rf_profile_wifi5
            print("using Wi-Fi5 profile Id")
        elif test_info.ap_spec[key] == "wifi6":
            rfProfileId = test_info.rf_profile_wifi6
            print("using Wi-Fi6 profile Id")
        else:
            rfProfileId = 10
            print("Unknown AP radio spec, using default RF profile")


        ###########################################################################
        ############## Bridge Mode Client Connectivity ############################
        ###########################################################################
        if args.skip_bridge != True:
            ### Create SSID Profiles
            ssid_template = "templates/ssid_profile_template.json"
            child_profiles = [rfProfileId]

            # 5G SSIDs
            if args.skip_eap != True:
                try:
                    fiveG_eap = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                             fw_model + '_5G_EAP_' + today, customer_id, profile_info_dict[fw_model]["fiveG_WPA2-EAP_SSID"], None,
                                                             radius_profile,
                                                             "wpa2OnlyRadius", "BRIDGE", 1,
                                                             ["is5GHzU", "is5GHz", "is5GHzL"])
                    print("5G EAP SSID created successfully - bridge mode")
                    client.update_testrail(case_id=test_cases["ssid_5g_eap_bridge"], run_id=rid, status_id=1,
                                           msg='5G EAP SSID created successfully - bridge mode')
                    report_data['tests'][key][test_cases["ssid_5g_eap_bridge"]] = "passed"
                    # Add create profile to list for AP profile
                    child_profiles.append(fiveG_eap)
                    # Add created profile to list for deletion at end of test
                    delete_list.append(fiveG_eap)
                except:
                    fiveG_eap = "error"
                    print("5G EAP SSID create failed - bridge mode")
                    client.update_testrail(case_id=test_cases["ssid_5g_eap_bridge"], run_id=rid, status_id=5,
                                           msg='5G EAP SSID create failed - bridge mode')
                    report_data['tests'][key][test_cases["ssid_5g_eap_bridge"]] = "failed"

            else:
                pass

            try:
                fiveG_wpa2 = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                          fw_model + '_5G_WPA2_' + today, customer_id,
                                                          profile_info_dict[fw_model]["fiveG_WPA2_SSID"],
                                                          profile_info_dict[fw_model]["fiveG_WPA2_PSK"],
                                                          0, "wpa2OnlyPSK", "BRIDGE", 1,
                                                          ["is5GHzU", "is5GHz", "is5GHzL"])
                print("5G WPA2 SSID created successfully - bridge mode")
                client.update_testrail(case_id=test_cases["ssid_5g_wpa2_bridge"], run_id=rid, status_id=1,
                                       msg='5G WPA2 SSID created successfully - bridge mode')
                report_data['tests'][key][test_cases["ssid_5g_wpa2_bridge"]] = "passed"
                # Add created profile to list for AP profile
                child_profiles.append(fiveG_wpa2)
                # Add created profile to list for deletion at end of test
                delete_list.append(fiveG_wpa2)
            except:
                fiveG_wpa2 = "error"
                print("5G WPA2 SSID create failed - bridge mode")
                client.update_testrail(case_id=test_cases["ssid_5g_wpa2_bridge"], run_id=rid, status_id=5,
                                       msg='5G WPA2 SSID create failed - bridge mode')
                report_data['tests'][key][test_cases["ssid_5g_wpa2_bridge"]] = "failed"

            try:
                fiveG_wpa = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                         fw_model + '_5G_WPA_' + today, customer_id,
                                                         profile_info_dict[fw_model]["fiveG_WPA_SSID"],
                                                         profile_info_dict[fw_model]["fiveG_WPA_PSK"],
                                                         0, "wpaPSK", "BRIDGE", 1,
                                                         ["is5GHzU", "is5GHz", "is5GHzL"])
                print("5G WPA SSID created successfully - bridge mode")
                client.update_testrail(case_id=test_cases["ssid_5g_wpa_bridge"], run_id=rid, status_id=1,
                                       msg='5G WPA SSID created successfully - bridge mode')
                report_data['tests'][key][test_cases["ssid_5g_wpa_bridge"]] = "passed"
                # Add created profile to list for AP profile
                child_profiles.append(fiveG_wpa)
                # Add created profile to list for deletion at end of test
                delete_list.append(fiveG_wpa)
            except:
                fiveG_wpa = "error"
                print("5G WPA SSID create failed - bridge mode")
                client.update_testrail(case_id=test_cases["ssid_5g_wpa_bridge"], run_id=rid, status_id=5,
                                       msg='5G WPA SSID create failed - bridge mode')
                report_data['tests'][key][test_cases["ssid_5g_wpa_bridge"]] = "failed"

            # 2.4G SSIDs
            if args.skip_eap != True:
                try:
                    twoFourG_eap = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                                fw_model + '_2G_EAP_' + today, customer_id,
                                                                profile_info_dict[fw_model]["twoFourG_WPA2-EAP_SSID"],
                                                                None,
                                                                radius_profile, "wpa2OnlyRadius", "BRIDGE", 1,
                                                                ["is2dot4GHz"])
                    print("2.4G EAP SSID created successfully - bridge mode")
                    client.update_testrail(case_id=test_cases["ssid_2g_eap_bridge"], run_id=rid, status_id=1,
                                           msg='2.4G EAP SSID created successfully - bridge mode')
                    report_data['tests'][key][test_cases["ssid_2g_eap_bridge"]] = "passed"
                    # Add created profile to list for AP profile
                    child_profiles.append(twoFourG_eap)
                    # Add created profile to list for deletion at end of test
                    delete_list.append(twoFourG_eap)
                except:
                    twoFourG_eap = "error"
                    print("2.4G EAP SSID create failed - bridge mode")
                    client.update_testrail(case_id=test_cases["ssid_2g_eap_bridge"], run_id=rid, status_id=5,
                                           msg='2.4G EAP SSID create failed - bridge mode')
                    report_data['tests'][key][test_cases["ssid_2g_eap_bridge"]] = "failed"
            else:
                pass

            try:
                twoFourG_wpa2 = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                             fw_model + '_2G_WPA2_' + today, customer_id,
                                                             profile_info_dict[fw_model]["twoFourG_WPA2_SSID"],
                                                             profile_info_dict[fw_model]["twoFourG_WPA2_PSK"],
                                                             0, "wpa2OnlyPSK", "BRIDGE", 1,
                                                             ["is2dot4GHz"])
                print("2.4G WPA2 SSID created successfully - bridge mode")
                client.update_testrail(case_id=test_cases["ssid_2g_wpa2_bridge"], run_id=rid, status_id=1,
                                       msg='2.4G WPA2 SSID created successfully - bridge mode')
                report_data['tests'][key][test_cases["ssid_2g_wpa2_bridge"]] = "passed"
                # Add created profile to list for AP profile
                child_profiles.append(twoFourG_wpa2)
                # Add created profile to list for deletion at end of test
                delete_list.append(twoFourG_wpa2)
            except:
                twoFourG_wpa2 = "error"
                print("2.4G WPA2 SSID create failed - bridge mode")
                client.update_testrail(case_id=test_cases["ssid_2g_wpa2_bridge"], run_id=rid, status_id=5,
                                       msg='2.4G WPA2 SSID create failed - bridge mode')
                report_data['tests'][key][test_cases["ssid_2g_wpa2_bridge"]] = "failed"

            try:
                twoFourG_wpa = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                            fw_model + '_2G_WPA_' + today, customer_id,
                                                            profile_info_dict[fw_model]["twoFourG_WPA_SSID"],
                                                            profile_info_dict[fw_model]["twoFourG_WPA_PSK"],
                                                            0, "wpaPSK", "BRIDGE", 1,
                                                            ["is2dot4GHz"])
                print("2.4G WPA SSID created successfully - bridge mode")
                client.update_testrail(case_id=test_cases["ssid_2g_wpa_bridge"], run_id=rid, status_id=1,
                                       msg='2.4G WPA SSID created successfully - bridge mode')
                report_data['tests'][key][test_cases["ssid_2g_wpa_bridge"]] = "passed"
                # Add created profile to list for AP profile
                child_profiles.append(twoFourG_wpa)
                # Add created profile to list for deletion at end of test
                delete_list.append(twoFourG_wpa)
            except:
                twoFourG_wpa = "error"
                print("2.4G WPA SSID create failed - bridge mode")
                client.update_testrail(case_id=test_cases["ssid_2g_wpa_bridge"], run_id=rid, status_id=5,
                                       msg='2.4G WPA SSID create failed - bridge mode')
                report_data['tests'][key][test_cases["ssid_2g_wpa_bridge"]] = "failed"

            ### Create AP Bridge Profile
            print(child_profiles)

            ap_template = "templates/ap_profile_template.json"
            name = "Nightly_Sanity_" + fw_model + "_" + today + "_bridge"

            try:
                create_ap_profile = CloudSDK.create_ap_profile(cloudSDK_url, bearer, ap_template, name, customer_id, child_profiles)
                test_profile_id = create_ap_profile
                print("Test Profile ID for Test is:", test_profile_id)
                client.update_testrail(case_id=test_cases["ap_bridge"], run_id=rid, status_id=1,
                                       msg='AP profile for bridge tests created successfully')
                report_data['tests'][key][test_cases["ap_bridge"]] = "passed"
                # Add created profile to list for deletion at end of test
                delete_list.append(test_profile_id)
            except:
                create_ap_profile = "error"
                #test_profile_id = profile_info_dict[fw_model]["profile_id"]
                print("Error creating AP profile for bridge tests. Will use existing AP profile")
                client.update_testrail(case_id=test_cases["ap_bridge"], run_id=rid, status_id=5,
                                       msg='AP profile for bridge tests could not be created using API')
                report_data['tests'][key][test_cases["ap_bridge"]] = "failed"

            ### Set Proper AP Profile for Bridge SSID Tests
            ap_profile = CloudSDK.set_ap_profile(equipment_id, test_profile_id, cloudSDK_url, bearer)

            ### Wait for Profile Push
            time.sleep(180)

            ### Check if VIF Config and VIF State reflect AP Profile from CloudSDK
            ## VIF Config
            if args.skip_eap != True:
                ssid_config = profile_info_dict[key]["ssid_list"]
            else:
                ssid_config = [x for x in profile_info_dict[key]["ssid_list"] if "-EAP" not in x]
            try:
                print("SSIDs in AP Profile:", ssid_config)

                ssid_list = ap_connect.get_vif_config(ap_ip, ap_username, ap_password)
                print("SSIDs in AP VIF Config:", ssid_list)

                if set(ssid_list) == set(ssid_config):
                    print("SSIDs in Wifi_VIF_Config Match AP Profile Config")
                    client.update_testrail(case_id=test_cases["bridge_vifc"], run_id=rid, status_id=1,
                                           msg='SSIDs in VIF Config matches AP Profile Config')
                    report_data['tests'][key][test_cases["bridge_vifc"]] = "passed"
                else:
                    print("SSIDs in Wifi_VIF_Config do not match desired AP Profile Config")
                    client.update_testrail(case_id=test_cases["bridge_vifc"], run_id=rid, status_id=5,
                                           msg='SSIDs in VIF Config do not match AP Profile Config')
                    report_data['tests'][key][test_cases["bridge_vifc"]] = "failed"

                    print('Writing logs...')
                    os.system('mkdir -p AP_Logs/' + now.strftime('%B') + '/' + now.strftime('%d') + '/' + file)
                    logread_output, dmesg_output = ap_connect.copy_logread_dmesg(ap_ip, ap_username, ap_password)

                    with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime(
                            '%d') + '/' + file + '/' + key + '_logread_' + now.strftime('%X').replace(':', '-'),
                              'w') as log_file:
                        log_file.write(logread_output)

                    with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime(
                            '%d') + '/' + file + '/' + key + '_dmesg_' + now.strftime('%X').replace(':', '-'),
                              'w') as dmesg_file:
                        dmesg_file.write(dmesg_output)
            except:
                ssid_list = "ERROR"
                print("Error accessing VIF Config from AP CLI")
                client.update_testrail(case_id=test_cases["bridge_vifc"], run_id=rid, status_id=4,
                                       msg='Cannot determine VIF Config - re-test required')
                report_data['tests'][key][test_cases["bridge_vifc"]] = "error"

            # VIF State
            try:
                ssid_state = ap_connect.get_vif_state(ap_ip, ap_username, ap_password)
                print("SSIDs in AP VIF State:", ssid_state)

                if set(ssid_state) == set(ssid_config):
                    print("SSIDs properly applied on AP")
                    client.update_testrail(case_id=test_cases["bridge_vifs"], run_id=rid, status_id=1,
                                           msg='SSIDs in VIF Config applied to VIF State')
                    report_data['tests'][key][test_cases["bridge_vifs"]] = "passed"
                else:
                    print("SSIDs not applied on AP")
                    client.update_testrail(case_id=test_cases["bridge_vifs"], run_id=rid, status_id=5,
                                           msg='SSIDs in VIF Config not applied to VIF State')
                    report_data['tests'][key][test_cases["bridge_vifs"]] = "failed"

                    print('Writing logs...')
                    os.system('mkdir -p AP_Logs/' + now.strftime('%B') + '/' + now.strftime('%d') + '/' + file)
                    logread_output, dmesg_output = ap_connect.copy_logread_dmesg(ap_ip, ap_username, ap_password)

                    with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime(
                            '%d') + '/' + file + '/' + key + '_logread_' + now.strftime('%X').replace(':', '-'),
                              'w') as log_file:
                        log_file.write(logread_output)

                    with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime(
                            '%d') + '/' + file + '/' + key + '_dmesg_' + now.strftime('%X').replace(':', '-'),
                              'w') as dmesg_file:
                        dmesg_file.write(dmesg_output)

            except:
                ssid_list = "ERROR"
                print("Error accessing VIF State from AP CLI")
                print("Error accessing VIF Config from AP CLI")
                client.update_testrail(case_id=test_cases["bridge_vifs"], run_id=rid, status_id=4,
                                       msg='Cannot determine VIF State - re-test required')
                report_data['tests'][key][test_cases["bridge_vifs"]] = "error"

            # Set LANForge port for tests
            port = test_info.lanforge_bridge_port

            # print iwinfo for information
            iwinfo = iwinfo_status(ap_ip, ap_username, ap_password)
            print(iwinfo)

            ###Run Client Single Connectivity Test Cases for Bridge SSIDs
            # TC5214 - 2.4 GHz WPA2-Enterprise
            if args.skip_eap != True:
                test_case = test_cases["2g_eap_bridge"]
                radio = test_info.lanforge_2dot4g
                #sta_list = [lanforge_prefix + "5214"]
                sta_list = [test_info.lanforge_2dot4g_station]
                prefix = test_info.lanforge_2dot4g_prefix
                ssid_name = profile_info_dict[fw_model]["twoFourG_WPA2-EAP_SSID"]
                security = "wpa2"
                eap_type = "TTLS"
                try:
                    test_result = RunTest.Single_Client_EAP(port, sta_list, ssid_name, radio, prefix, security, eap_type,
                                                            identity,
                                                            ttls_password, test_case, rid)
                except:
                    test_result = "error"
                    Test.testrail_retest(test_case, rid, ssid_name)
                    pass
                report_data['tests'][key][int(test_case)] = test_result
                time.sleep(10)
            else:
                pass

            ###Run Client Single Connectivity Test Cases for Bridge SSIDs
            # TC - 2.4 GHz WPA2
            test_case = test_cases["2g_wpa2_bridge"]
            radio = test_info.lanforge_2dot4g
            #station = [lanforge_prefix + "2237"]
            station = [test_info.lanforge_2dot4g_station]
            prefix = test_info.lanforge_2dot4g_prefix
            ssid_name = profile_info_dict[fw_model]["twoFourG_WPA2_SSID"]
            ssid_psk = profile_info_dict[fw_model]["twoFourG_WPA2_PSK"]
            security = "wpa2"
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, ssid_name, ssid_psk, security, station,
                                                              test_case,
                                                              rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, ssid_name)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(10)

            # TC - 2.4 GHz WPA
            test_case = test_cases["2g_wpa_bridge"]
            radio = test_info.lanforge_2dot4g
            #station = [lanforge_prefix + "2420"]
            station = [test_info.lanforge_2dot4g_station]
            prefix = test_info.lanforge_2dot4g_prefix
            ssid_name = profile_info_dict[fw_model]["twoFourG_WPA_SSID"]
            ssid_psk = profile_info_dict[fw_model]["twoFourG_WPA_PSK"]
            security = "wpa"
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, ssid_name, ssid_psk, security, station,
                                                              test_case,
                                                              rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, ssid_name)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(10)

            # TC - 5 GHz WPA2-Enterprise
            if args.skip_eap != True:
                test_case = test_cases["5g_eap_bridge"]
                radio = test_info.lanforge_5g
                #sta_list = [lanforge_prefix + "5215"]
                sta_list = [test_info.lanforge_5g_station]
                prefix = test_info.lanforge_5g_prefix
                ssid_name = profile_info_dict[fw_model]["fiveG_WPA2-EAP_SSID"]
                security = "wpa2"
                eap_type = "TTLS"
                try:
                    test_result = RunTest.Single_Client_EAP(port, sta_list, ssid_name, radio, prefix, security, eap_type,
                                                            identity,
                                                            ttls_password, test_case, rid)
                except:
                    test_result = "error"
                    Test.testrail_retest(test_case, rid, ssid_name)
                    pass
                report_data['tests'][key][int(test_case)] = test_result
                time.sleep(10)
            else:
                pass

            # TC 5 GHz WPA2
            test_case = test_cases["5g_wpa2_bridge"]
            radio = test_info.lanforge_5g
            #station = [lanforge_prefix + "2236"]
            station = [test_info.lanforge_5g_station]
            prefix = test_info.lanforge_5g_prefix
            ssid_name = profile_info_dict[fw_model]["fiveG_WPA2_SSID"]
            ssid_psk = profile_info_dict[fw_model]["fiveG_WPA2_PSK"]
            security = "wpa2"
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, ssid_name, ssid_psk, security, station,
                                                              test_case,
                                                              rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, ssid_name)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(10)

            # TC - 5 GHz WPA
            test_case = test_cases["5g_wpa_bridge"]
            radio = test_info.lanforge_5g
            #station = [lanforge_prefix + "2419"]
            station = [test_info.lanforge_5g_station]
            prefix = test_info.lanforge_5g_prefix
            ssid_name = profile_info_dict[fw_model]["fiveG_WPA_SSID"]
            ssid_psk = profile_info_dict[fw_model]["fiveG_WPA_PSK"]
            security = "wpa"
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, ssid_name, ssid_psk, security, station,
                                                              test_case,
                                                              rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, ssid_name)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(10)

            # Update SSID Profile
            update_profile_id = str(fiveG_wpa)
            update_ssid = key+"_Updated_SSID"
            update_auth = "wpa2OnlyPSK"
            update_security = "wpa2"
            update_psk = "12345678"
            update_profile = CloudSDK.update_ssid_profile(cloudSDK_url, bearer, update_profile_id, update_ssid, update_auth, update_psk)
            print(update_profile)
            time.sleep(90)

            # TC - Update Bridge SSID profile
            test_case = test_cases["bridge_ssid_update"]
            radio = test_info.lanforge_5g
            station = [test_info.lanforge_5g_station]
            prefix = test_info.lanforge_5g_prefix
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, update_ssid, update_psk,
                                                              update_security, station,
                                                              test_case,
                                                              rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, update_ssid)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(5)

            print(report_data['tests'][key])
            logger.info("Testing for " + fw_model + "Bridge Mode SSIDs Complete")
            with open(report_path + today + '/report_data.json', 'w') as report_json_file:
                json.dump(report_data, report_json_file)
        else:
            print("Skipping Bridge tests at user request...")
            pass

        ###########################################################################
        ################# NAT Mode Client Connectivity ############################
        ###########################################################################
        if args.skip_nat != True:
            child_profiles = [rfProfileId]
            ### Create SSID Profiles
            ssid_template = "templates/ssid_profile_template.json"

            # 5G SSIDs
            if args.skip_eap != True:
                try:
                    fiveG_eap = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                             fw_model + '_5G_EAP_NAT_' + today, customer_id,
                                                             profile_info_dict[fw_model + '_nat'][
                                                                 "fiveG_WPA2-EAP_SSID"], None,
                                                             radius_profile,
                                                             "wpa2OnlyRadius", "NAT", 1,
                                                             ["is5GHzU", "is5GHz", "is5GHzL"])
                    print("5G EAP SSID created successfully - NAT mode")
                    client.update_testrail(case_id=test_cases["ssid_5g_eap_nat"], run_id=rid, status_id=1,
                                           msg='5G EAP SSID created successfully - NAT mode')
                    report_data['tests'][key][test_cases["ssid_5g_eap_nat"]] = "passed"
                    # Add created profile to list for AP profile
                    child_profiles.append(fiveG_eap)
                    # Add created profile to list for deletion at end of test
                    delete_list.append(fiveG_eap)

                except:
                    fiveG_eap = "error"
                    print("5G EAP SSID create failed - NAT mode")
                    client.update_testrail(case_id=test_cases["ssid_5g_eap_nat"], run_id=rid, status_id=5,
                                           msg='5G EAP SSID create failed - NAT mode')
                    report_data['tests'][key][test_cases["ssid_5g_eap_nat"]] = "failed"
            else:
                pass

            try:
                fiveG_wpa2 = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                          fw_model + '_5G_WPA2_NAT_' + today, customer_id,
                                                          profile_info_dict[fw_model + '_nat']["fiveG_WPA2_SSID"],
                                                          profile_info_dict[fw_model + '_nat']["fiveG_WPA2_PSK"],
                                                          0, "wpa2OnlyPSK", "NAT", 1,
                                                          ["is5GHzU", "is5GHz", "is5GHzL"])
                print("5G WPA2 SSID created successfully - NAT mode")
                client.update_testrail(case_id=test_cases["ssid_5g_wpa2_nat"], run_id=rid, status_id=1,
                                       msg='5G WPA2 SSID created successfully - NAT mode')
                report_data['tests'][key][test_cases["ssid_5g_wpa2_nat"]] = "passed"
                # Add created profile to list for AP profile
                child_profiles.append(fiveG_wpa2)
                # Add created profile to list for deletion at end of test
                delete_list.append(fiveG_wpa2)
            except:
                fiveG_wpa2 = "error"
                print("5G WPA2 SSID create failed - NAT mode")
                client.update_testrail(case_id=test_cases["ssid_5g_wpa2_nat"], run_id=rid, status_id=5,
                                       msg='5G WPA2 SSID create failed - NAT mode')
                report_data['tests'][key][test_cases["ssid_5g_wpa2_nat"]] = "failed"

            try:
                fiveG_wpa = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                         fw_model + '_5G_WPA_NAT_' + today, customer_id,
                                                         profile_info_dict[fw_model + '_nat']["fiveG_WPA_SSID"],
                                                         profile_info_dict[fw_model + '_nat']["fiveG_WPA_PSK"],
                                                         0, "wpaPSK", "NAT", 1,
                                                         ["is5GHzU", "is5GHz", "is5GHzL"])
                print("5G WPA SSID created successfully - NAT mode")
                client.update_testrail(case_id=test_cases["ssid_5g_wpa_nat"], run_id=rid, status_id=1,
                                       msg='5G WPA SSID created successfully - NAT mode')
                report_data['tests'][key][test_cases["ssid_5g_wpa_nat"]] = "passed"
                # Add created profile to list for AP profile
                child_profiles.append(fiveG_wpa)
                # Add created profile to list for deletion at end of test
                delete_list.append(fiveG_wpa)
            except:
                fiveG_wpa = "error"
                print("5G WPA SSID create failed - NAT mode")
                client.update_testrail(case_id=test_cases["ssid_5g_wpa_nat"], run_id=rid, status_id=5,
                                       msg='5G WPA SSID create failed - NAT mode')
                report_data['tests'][key][test_cases["ssid_5g_wpa_nat"]] = "failed"

                # 2.4G SSIDs
            if args.skip_eap != True:
                try:
                    twoFourG_eap = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                                fw_model + '_2G_EAP_NAT_' + today, customer_id,
                                                                profile_info_dict[fw_model + '_nat'][
                                                                    "twoFourG_WPA2-EAP_SSID"],
                                                                None,
                                                                radius_profile, "wpa2OnlyRadius", "NAT", 1, ["is2dot4GHz"])
                    print("2.4G EAP SSID created successfully - NAT mode")
                    client.update_testrail(case_id=test_cases["ssid_2g_eap_nat"], run_id=rid, status_id=1,
                                           msg='2.4G EAP SSID created successfully - NAT mode')
                    report_data['tests'][key][test_cases["ssid_2g_eap_nat"]] = "passed"
                    # Add created profile to list for AP profile
                    child_profiles.append(twoFourG_eap)
                    # Add created profile to list for deletion at end of test
                    delete_list.append(twoFourG_eap)
                except:
                    twoFourG_eap = "error"
                    print("2.4G EAP SSID create failed - NAT mode")
                    client.update_testrail(case_id=test_cases["ssid_2g_eap_nat"], run_id=rid, status_id=5,
                                           msg='2.4G EAP SSID create failed - NAT mode')
                    report_data['tests'][key][test_cases["ssid_2g_eap_nat"]] = "failed"
            else:
                pass

            try:
                twoFourG_wpa2 = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                             fw_model + '_2G_WPA2_NAT_' + today, customer_id,
                                                             profile_info_dict[fw_model + '_nat']["twoFourG_WPA2_SSID"],
                                                             profile_info_dict[fw_model + '_nat']["twoFourG_WPA2_PSK"],
                                                             0, "wpa2OnlyPSK", "NAT", 1,
                                                             ["is2dot4GHz"])
                print("2.4G WPA2 SSID created successfully - NAT mode")
                client.update_testrail(case_id=test_cases["ssid_2g_wpa2_nat"], run_id=rid, status_id=1,
                                       msg='2.4G WPA2 SSID created successfully - NAT mode')
                report_data['tests'][key][test_cases["ssid_2g_wpa2_nat"]] = "passed"
                # Add created profile to list for AP profile
                child_profiles.append(twoFourG_wpa2)
                # Add created profile to list for deletion at end of test
                delete_list.append(twoFourG_wpa2)
            except:
                twoFourG_wpa2 = "error"
                print("2.4G WPA2 SSID create failed - NAT mode")
                client.update_testrail(case_id=test_cases["ssid_2g_wpa2_nat"], run_id=rid, status_id=5,
                                       msg='2.4G WPA2 SSID create failed - NAT mode')
                report_data['tests'][key][test_cases["ssid_2g_wpa2_nat"]] = "failed"
            try:
                twoFourG_wpa = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                            fw_model + '_2G_WPA_NAT_' + today, customer_id,
                                                            profile_info_dict[fw_model + '_nat']["twoFourG_WPA_SSID"],
                                                            profile_info_dict[fw_model + '_nat']["twoFourG_WPA_PSK"],
                                                            0, "wpaPSK", "NAT", 1,
                                                            ["is2dot4GHz"])
                print("2.4G WPA SSID created successfully - NAT mode")
                client.update_testrail(case_id=test_cases["ssid_2g_wpa_nat"], run_id=rid, status_id=1,
                                       msg='2.4G WPA SSID created successfully - NAT mode')
                report_data['tests'][key][test_cases["ssid_2g_wpa_nat"]] = "passed"
                # Add created profile to list for AP profile
                child_profiles.append(twoFourG_wpa)
                # Add created profile to list for deletion at end of test
                delete_list.append(twoFourG_wpa)
            except:
                twoFourG_wpa = "error"
                print("2.4G WPA SSID create failed - NAT mode")
                client.update_testrail(case_id=test_cases["ssid_2g_wpa_nat"], run_id=rid, status_id=5,
                                       msg='2.4G WPA SSID create failed - NAT mode')
                report_data['tests'][key][test_cases["ssid_2g_wpa_nat"]] = "failed"

            ### Create AP NAT Profile
            print(child_profiles)
            ap_template = "templates/ap_profile_template.json"
            name = "Nightly_Sanity_" + fw_model + "_" + today + "_nat"

            try:
                create_ap_profile = CloudSDK.create_ap_profile(cloudSDK_url, bearer, ap_template, name, customer_id, child_profiles)
                test_profile_id = create_ap_profile
                print("Test Profile ID for Test is:", test_profile_id)
                client.update_testrail(case_id=test_cases["ap_nat"], run_id=rid, status_id=1,
                                       msg='AP profile for NAT tests created successfully')
                report_data['tests'][key][test_cases["ap_nat"]] = "passed"
                # Add created profile to list for AP profile
                # Add created profile to list for deletion at end of test
                delete_list.append(test_profile_id)
            except:
                create_ap_profile = "error"
                #test_profile_id = profile_info_dict[fw_model + '_nat']["profile_id"]
                print("Error creating AP profile for NAT tests. Will use existing AP profile")
                client.update_testrail(case_id=test_cases["ap_nat"], run_id=rid, status_id=5,
                                       msg='AP profile for NAT tests could not be created using API')
                report_data['tests'][key][test_cases["ap_nat"]] = "failed"

            ###Set Proper AP Profile for NAT SSID Tests
            ap_profile = CloudSDK.set_ap_profile(equipment_id, test_profile_id, cloudSDK_url, bearer)

            ### Wait for Profile Push
            time.sleep(180)

            ###Check if VIF Config and VIF State reflect AP Profile from CloudSDK
            ## VIF Config
            if args.skip_eap != True:
                ssid_config = profile_info_dict[fw_model + '_nat']["ssid_list"]
            else:
                ssid_config = [x for x in profile_info_dict[fw_model + '_nat']["ssid_list"] if "-EAP" not in x]
            try:
                print("SSIDs in AP Profile:", ssid_config)

                ssid_list = ap_connect.get_vif_config(ap_ip, ap_username, ap_password)
                print("SSIDs in AP VIF Config:", ssid_list)

                if set(ssid_list) == set(ssid_config):
                    print("SSIDs in Wifi_VIF_Config Match AP Profile Config")
                    client.update_testrail(case_id=test_cases["nat_vifc"], run_id=rid, status_id=1,
                                           msg='SSIDs in VIF Config matches AP Profile Config')
                    report_data['tests'][key][test_cases["nat_vifc"]] = "passed"
                else:
                    print("SSIDs in Wifi_VIF_Config do not match desired AP Profile Config")
                    client.update_testrail(case_id=test_cases["nat_vifc"], run_id=rid, status_id=5,
                                           msg='SSIDs in VIF Config do not match AP Profile Config')
                    report_data['tests'][key][test_cases["nat_vifc"]] = "failed"

                    print('Writing logs...')
                    os.system('mkdir -p AP_Logs/' + now.strftime('%B') + '/' + now.strftime('%d') + '/' + file)
                    logread_output, dmesg_output = ap_connect.copy_logread_dmesg(ap_ip, ap_username, ap_password)

                    with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime(
                            '%d') + '/' + file + '/' + key + '_logread_' + now.strftime('%X').replace(':', '-'),
                              'w') as log_file:
                        log_file.write(logread_output)

                    with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime(
                            '%d') + '/' + file + '/' + key + '_dmesg_' + now.strftime('%X').replace(':', '-'),
                              'w') as dmesg_file:
                        dmesg_file.write(dmesg_output)
            except:
                ssid_list = "ERROR"
                print("Error accessing VIF Config from AP CLI")
                client.update_testrail(case_id=test_cases["nat_vifc"], run_id=rid, status_id=4,
                                       msg='Cannot determine VIF Config - re-test required')
                report_data['tests'][key][test_cases["nat_vifc"]] = "error"

            # VIF State
            try:
                ssid_state = ap_connect.get_vif_state(ap_ip, ap_username, ap_password)
                print("SSIDs in AP VIF State:", ssid_state)

                if set(ssid_state) == set(ssid_config):
                    print("SSIDs properly applied on AP")
                    client.update_testrail(case_id=test_cases["nat_vifs"], run_id=rid, status_id=1,
                                           msg='SSIDs in VIF Config applied to VIF State')
                    report_data['tests'][key][test_cases["nat_vifs"]] = "passed"
                else:
                    print("SSIDs not applied on AP")
                    client.update_testrail(case_id=test_cases["nat_vifs"], run_id=rid, status_id=5,
                                           msg='SSIDs in VIF Config not applied to VIF State')
                    report_data['tests'][key][test_cases["nat_vifs"]] = "failed"

                    print('Writing logs...')
                    os.system('mkdir -p AP_Logs/' + now.strftime('%B') + '/' + now.strftime('%d') + '/' + file)
                    logread_output, dmesg_output = ap_connect.copy_logread_dmesg(ap_ip, ap_username, ap_password)

                    with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime(
                            '%d') + '/' + file + '/' + key + '_logread_' + now.strftime('%X').replace(':', '-'),
                              'w') as log_file:
                        log_file.write(logread_output)

                    with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime(
                            '%d') + '/' + file + '/' + key + '_dmesg_' + now.strftime('%X').replace(':', '-'),
                              'w') as dmesg_file:
                        dmesg_file.write(dmesg_output)
            except:
                ssid_list = "ERROR"
                print("Error accessing VIF State from AP CLI")
                print("Error accessing VIF Config from AP CLI")
                client.update_testrail(case_id=test_cases["nat_vifs"], run_id=rid, status_id=4,
                                       msg='Cannot determine VIF State - re-test required')
                report_data['tests'][key][test_cases["nat_vifs"]] = "error"

            ### Set LANForge port for tests
            port = test_info.lanforge_bridge_port

            # Print iwinfo for logs
            iwinfo = iwinfo_status(ap_ip, ap_username, ap_password)
            print(iwinfo)

            ###Run Client Single Connectivity Test Cases for NAT SSIDs
            # TC - 2.4 GHz WPA2-Enterprise NAT
            if args.skip_eap != True:
                test_case = test_cases["2g_eap_nat"]
                radio = test_info.lanforge_2dot4g
                #sta_list = [lanforge_prefix + "5216"]
                sta_list = [test_info.lanforge_2dot4g_station]
                prefix = test_info.lanforge_2dot4g_prefix
                ssid_name = profile_info_dict[fw_model + '_nat']["twoFourG_WPA2-EAP_SSID"]
                security = "wpa2"
                eap_type = "TTLS"
                try:
                    test_result = RunTest.Single_Client_EAP(port, sta_list, ssid_name, radio, prefix, security, eap_type,
                                                            identity,
                                                            ttls_password, test_case, rid)
                except:
                    test_result = "error"
                    Test.testrail_retest(test_case, rid, ssid_name)
                    pass
                report_data['tests'][key][int(test_case)] = test_result
                time.sleep(10)
            else:
                pass

            # TC - 2.4 GHz WPA2 NAT
            test_case = test_cases["2g_wpa2_nat"]
            radio = test_info.lanforge_2dot4g
            #station = [lanforge_prefix + "4325"]
            station = [test_info.lanforge_2dot4g_station]
            prefix = test_info.lanforge_2dot4g_prefix
            ssid_name = profile_info_dict[fw_model + '_nat']["twoFourG_WPA2_SSID"]
            ssid_psk = profile_info_dict[fw_model + '_nat']["twoFourG_WPA2_PSK"]
            security = "wpa2"
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, ssid_name, ssid_psk, security, station,
                                                              test_case,
                                                              rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, ssid_name)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(10)

            # TC - 2.4 GHz WPA NAT
            test_case = test_cases["2g_wpa_nat"]
            radio = test_info.lanforge_2dot4g
            #station = [lanforge_prefix + "4323"]
            station = [test_info.lanforge_2dot4g_station]
            prefix = test_info.lanforge_2dot4g_prefix
            ssid_name = profile_info_dict[fw_model + '_nat']["twoFourG_WPA_SSID"]
            ssid_psk = profile_info_dict[fw_model + '_nat']["twoFourG_WPA_PSK"]
            security = "wpa"
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, ssid_name, ssid_psk, security, station,
                                                              test_case, rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, ssid_name)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(10)

            # TC - 5 GHz WPA2-Enterprise NAT
            if args.skip_eap != True:
                test_case = test_cases["5g_eap_nat"]
                radio = test_info.lanforge_5g
                #sta_list = [lanforge_prefix + "5217"]
                sta_list = [test_info.lanforge_5g_station]
                prefix = test_info.lanforge_5g_prefix
                ssid_name = profile_info_dict[fw_model + '_nat']["fiveG_WPA2-EAP_SSID"]
                security = "wpa2"
                eap_type = "TTLS"
                try:
                    test_result = RunTest.Single_Client_EAP(port, sta_list, ssid_name, radio, prefix, security, eap_type,
                                                            identity,
                                                            ttls_password, test_case, rid)
                except:
                    test_result = "error"
                    Test.testrail_retest(test_case, rid, ssid_name)
                    pass
                report_data['tests'][key][int(test_case)] = test_result
                time.sleep(10)

            # TC - 5 GHz WPA2 NAT
            test_case = test_cases["5g_wpa2_nat"]
            radio = test_info.lanforge_5g
            #station = [lanforge_prefix + "4326"]
            station = [test_info.lanforge_5g_station]
            prefix = test_info.lanforge_5g_prefix
            ssid_name = profile_info_dict[fw_model + '_nat']["fiveG_WPA2_SSID"]
            ssid_psk = profile_info_dict[fw_model]["fiveG_WPA2_PSK"]
            security = "wpa2"
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, ssid_name, ssid_psk, security, station,
                                                              test_case,
                                                              rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, ssid_name)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(10)

            # TC - 5 GHz WPA NAT
            test_case = test_cases["5g_wpa_nat"]
            radio = test_info.lanforge_5g
            #station = [lanforge_prefix + "4324"]
            station = [test_info.lanforge_5g_station]
            prefix = test_info.lanforge_5g_prefix
            ssid_name = profile_info_dict[fw_model + '_nat']["fiveG_WPA_SSID"]
            ssid_psk = profile_info_dict[fw_model]["fiveG_WPA_PSK"]
            security = "wpa"
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, ssid_name, ssid_psk, security, station,
                                                              test_case,
                                                              rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, ssid_name)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(10)

            # Update SSID Profile
            update_profile_id = str(fiveG_wpa2)
            update_ssid = key + "_Updated_SSID_NAT"
            update_auth = "wpaPSK"
            update_security = "wpa"
            update_psk = "12345678"
            update_profile = CloudSDK.update_ssid_profile(cloudSDK_url, bearer, update_profile_id, update_ssid,
                                                          update_auth, update_psk)
            print(update_profile)
            time.sleep(90)

            # TC - Update NAT SSID profile
            test_case = test_cases["nat_ssid_update"]
            radio = test_info.lanforge_5g
            station = [test_info.lanforge_5g_station]
            prefix = test_info.lanforge_5g_prefix
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, update_ssid, update_psk,
                                                              update_security, station,
                                                              test_case,
                                                              rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, update_ssid)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(5)

            print(report_data['tests'][key])
            logger.info("Testing for " + fw_model + "NAT Mode SSIDs Complete")
            with open(report_path + today + '/report_data.json', 'w') as report_json_file:
                json.dump(report_data, report_json_file)
        else:
            print("Skipping NAT tests at user request...")
            pass

        ###########################################################################
        ################# Customer VLAN Client Connectivity #######################
        ###########################################################################
        if args.skip_vlan != True:
            child_profiles = [rfProfileId]
            ### Create SSID Profiles
            ssid_template = "templates/ssid_profile_template.json"

            # 5G SSIDs
            if args.skip_eap != True:
                try:
                    fiveG_eap = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                             fw_model + '_5G_EAP_VLAN' + today, customer_id,
                                                             profile_info_dict[fw_model + '_vlan'][
                                                                 "fiveG_WPA2-EAP_SSID"], None,
                                                             radius_profile,
                                                             "wpa2OnlyRadius", "BRIDGE", test_info.vlan,
                                                             ["is5GHzU", "is5GHz", "is5GHzL"])
                    print("5G EAP SSID created successfully - custom VLAN mode")
                    client.update_testrail(case_id=test_cases["ssid_5g_eap_vlan"], run_id=rid, status_id=1,
                                           msg='5G EAP SSID created successfully - Custom VLAN mode')
                    report_data['tests'][key][test_cases["ssid_5g_eap_vlan"]] = "passed"
                    # Add created profile to list for AP profile
                    child_profiles.append(fiveG_eap)
                    # Add created profile to list for deletion at end of test
                    delete_list.append(fiveG_eap)

                except:
                    fiveG_eap = "error"
                    print("5G EAP SSID create failed - custom VLAN mode")
                    client.update_testrail(case_id=test_cases["ssid_5g_eap_vlan"], run_id=rid, status_id=5,
                                           msg='5G EAP SSID create failed - custom VLAN mode')
                    report_data['tests'][key][test_cases["ssid_5g_eap_vlan"]] = "failed"
            else:
                pass

            try:
                fiveG_wpa2 = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                          fw_model + '_5G_WPA2_VLAN' + today, customer_id,
                                                          profile_info_dict[fw_model + '_vlan']["fiveG_WPA2_SSID"],
                                                          profile_info_dict[fw_model + '_vlan']["fiveG_WPA2_PSK"],
                                                          0, "wpa2OnlyPSK", "BRIDGE", test_info.vlan,
                                                          ["is5GHzU", "is5GHz", "is5GHzL"])
                print("5G WPA2 SSID created successfully - custom VLAN mode")
                client.update_testrail(case_id=test_cases["ssid_5g_wpa2_vlan"], run_id=rid, status_id=1,
                                       msg='5G WPA2 SSID created successfully - custom VLAN mode')
                report_data['tests'][key][test_cases["ssid_5g_wpa2_vlan"]] = "passed"
                # Add created profile to list for AP profile
                child_profiles.append(fiveG_wpa2)
                # Add created profile to list for deletion at end of test
                delete_list.append(fiveG_wpa2)
            except:
                fiveG_wpa2 = "error"
                print("5G WPA2 SSID create failed - custom VLAN mode")
                client.update_testrail(case_id=test_cases["ssid_5g_wpa2_vlan"], run_id=rid, status_id=5,
                                       msg='5G WPA2 SSID create failed - custom VLAN mode')
                report_data['tests'][key][test_cases["ssid_5g_wpa2_vlan"]] = "failed"

            try:
                fiveG_wpa = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                         fw_model + '_5G_WPA_VLAN_' + today, customer_id,
                                                         profile_info_dict[fw_model + '_vlan']["fiveG_WPA_SSID"],
                                                         profile_info_dict[fw_model + '_vlan']["fiveG_WPA_PSK"],
                                                         0, "wpaPSK", "BRIDGE", test_info.vlan,
                                                         ["is5GHzU", "is5GHz", "is5GHzL"])
                print("5G WPA SSID created successfully - custom VLAN mode")
                client.update_testrail(case_id=test_cases["ssid_5g_wpa_vlan"], run_id=rid, status_id=1,
                                       msg='5G WPA SSID created successfully - custom VLAN mode')
                report_data['tests'][key][test_cases["ssid_5g_wpa_vlan"]] = "passed"
                # Add created profile to list for AP profile
                child_profiles.append(fiveG_wpa)
                # Add created profile to list for deletion at end of test
                delete_list.append(fiveG_wpa)
            except:
                fiveG_wpa = "error"
                print("5G WPA SSID create failed - custom VLAN mode")
                client.update_testrail(case_id=test_cases["ssid_5g_wpa_vlan"], run_id=rid, status_id=5,
                                       msg='5G WPA SSID create failed - custom VLAN mode')
                report_data['tests'][key][test_cases["ssid_5g_wpa_vlan"]] = "failed"

            # 2.4G SSIDs
            if args.skip_eap != True:
                try:
                    twoFourG_eap = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                                fw_model + '_2G_EAP_VLAN_' + today, customer_id,
                                                                profile_info_dict[fw_model + '_vlan'][
                                                                    "twoFourG_WPA2-EAP_SSID"],
                                                                None,
                                                                radius_profile, "wpa2OnlyRadius", "BRIDGE", test_info.vlan,
                                                                ["is2dot4GHz"])
                    print("2.4G EAP SSID created successfully - custom VLAN mode")
                    client.update_testrail(case_id=test_cases["ssid_2g_eap_vlan"], run_id=rid, status_id=1,
                                           msg='2.4G EAP SSID created successfully - custom VLAN mode')
                    report_data['tests'][key][test_cases["ssid_2g_eap_vlan"]] = "passed"
                    # Add created profile to list for AP profile
                    child_profiles.append(twoFourG_eap)
                    # Add created profile to list for deletion at end of test
                    delete_list.append(twoFourG_eap)
                except:
                    twoFourG_eap = "error"
                    print("2.4G EAP SSID create failed - custom VLAN mode")
                    client.update_testrail(case_id=test_cases["ssid_2g_eap_vlan"], run_id=rid, status_id=5,
                                           msg='2.4G EAP SSID create failed - custom VLAN mode')
                    report_data['tests'][key][test_cases["ssid_2g_eap_vlan"]] = "failed"
            else:
                pass

            try:
                twoFourG_wpa2 = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                             fw_model + '_2G_WPA2_VLAN_' + today, customer_id,
                                                             profile_info_dict[fw_model + '_vlan'][
                                                                 "twoFourG_WPA2_SSID"],
                                                             profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2_PSK"],
                                                             0, "wpa2OnlyPSK", "BRIDGE", test_info.vlan,
                                                             ["is2dot4GHz"])
                print("2.4G WPA2 SSID created successfully - custom VLAN mode")
                client.update_testrail(case_id=test_cases["ssid_2g_wpa2_vlan"], run_id=rid, status_id=1,
                                       msg='2.4G WPA2 SSID created successfully - custom VLAN mode')
                report_data['tests'][key][test_cases["ssid_2g_wpa2_vlan"]] = "passed"
                # Add created profile to list for AP profile
                child_profiles.append(twoFourG_wpa2)
                # Add created profile to list for deletion at end of test
                delete_list.append(twoFourG_wpa2)
            except:
                twoFourG_wpa2 = "error"
                print("2.4G WPA2 SSID create failed - custom VLAN mode")
                client.update_testrail(case_id=test_cases["ssid_2g_wpa2_vlan"], run_id=rid, status_id=5,
                                       msg='2.4G WPA2 SSID create failed - custom VLAN mode')
                report_data['tests'][key][test_cases["ssid_2g_wpa2_vlan"]] = "failed"

            try:
                twoFourG_wpa = CloudSDK.create_ssid_profile(cloudSDK_url, bearer, ssid_template,
                                                            fw_model + '_2G_WPA_VLAN_' + today, customer_id,
                                                            profile_info_dict[fw_model + '_vlan']["twoFourG_WPA_SSID"],
                                                            profile_info_dict[fw_model + '_vlan']["twoFourG_WPA_PSK"],
                                                            0, "wpaPSK", "BRIDGE", test_info.vlan,
                                                            ["is2dot4GHz"])
                print("2.4G WPA SSID created successfully - custom VLAN mode")
                client.update_testrail(case_id=test_cases["ssid_2g_wpa_vlan"], run_id=rid, status_id=1,
                                       msg='2.4G WPA SSID created successfully - custom VLAN mode')
                report_data['tests'][key][test_cases["ssid_2g_wpa_vlan"]] = "passed"
                # Add created profile to list for AP profile
                child_profiles.append(twoFourG_wpa)
                # Add created profile to list for deletion at end of test
                delete_list.append(twoFourG_wpa)
            except:
                twoFourG_wpa = "error"
                print("2.4G WPA SSID create failed - custom VLAN mode")
                client.update_testrail(case_id=test_cases["ssid_2g_wpa_vlan"], run_id=rid, status_id=5,
                                       msg='2.4G WPA SSID create failed - custom VLAN mode')
                report_data['tests'][key][test_cases["ssid_2g_wpa_vlan"]] = "failed"

            ### Create AP VLAN Profile
            print(child_profiles)
            ap_template = "templates/ap_profile_template.json"
            name = "Nightly_Sanity_" + fw_model + "_" + today + "_vlan"

            try:
                create_ap_profile = CloudSDK.create_ap_profile(cloudSDK_url, bearer, ap_template, name, customer_id, child_profiles)
                test_profile_id = create_ap_profile
                print("Test Profile ID for Test is:", test_profile_id)
                client.update_testrail(case_id=test_cases["ap_vlan"], run_id=rid, status_id=1,
                                       msg='AP profile for VLAN tests created successfully')
                report_data['tests'][key][test_cases["ap_vlan"]] = "passed"
                # Add created profile to list for deletion at end of test
                delete_list.append(test_profile_id)
            except:
                create_ap_profile = "error"
                #test_profile_id = profile_info_dict[fw_model + '_vlan']["profile_id"]
                print("Error creating AP profile for bridge tests. Will use existing AP profile")
                client.update_testrail(case_id=test_cases["ap_vlan"], run_id=rid, status_id=5,
                                       msg='AP profile for VLAN tests could not be created using API')
                report_data['tests'][key][test_cases["ap_vlan"]] = "failed"

            ### Set Proper AP Profile for VLAN SSID Tests
            ap_profile = CloudSDK.set_ap_profile(equipment_id, test_profile_id, cloudSDK_url, bearer)

            ### Wait for Profile Push
            time.sleep(180)

            ###Check if VIF Config and VIF State reflect AP Profile from CloudSDK
            ## VIF Config
            if args.skip_eap != True:
                ssid_config = profile_info_dict[fw_model + '_vlan']["ssid_list"]
            else:
                ssid_config = [x for x in profile_info_dict[fw_model + '_vlan']["ssid_list"] if "-EAP" not in x]

            try:
                print("SSIDs in AP Profile:", ssid_config)

                ssid_list = ap_connect.get_vif_config(ap_ip, ap_username, ap_password)
                print("SSIDs in AP VIF Config:", ssid_list)

                if set(ssid_list) == set(ssid_config):
                    print("SSIDs in Wifi_VIF_Config Match AP Profile Config")
                    client.update_testrail(case_id=test_cases["vlan_vifc"], run_id=rid, status_id=1,
                                           msg='SSIDs in VIF Config matches AP Profile Config')
                    report_data['tests'][key][test_cases["vlan_vifc"]] = "passed"
                else:
                    print("SSIDs in Wifi_VIF_Config do not match desired AP Profile Config")
                    client.update_testrail(case_id=test_cases["vlan_vifc"], run_id=rid, status_id=5,
                                           msg='SSIDs in VIF Config do not match AP Profile Config')
                    report_data['tests'][key][test_cases["vlan_vifc"]] = "failed"

                    print('Writing logs...')
                    os.system('mkdir -p AP_Logs/' + now.strftime('%B') + '/' + now.strftime('%d') + '/' + file)
                    logread_output, dmesg_output = ap_connect.copy_logread_dmesg(ap_ip, ap_username, ap_password)

                    with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime(
                            '%d') + '/' + file + '/' + key + '_logread_' + now.strftime('%X').replace(':', '-'),
                              'w') as log_file:
                        log_file.write(logread_output)

                    with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime(
                            '%d') + '/' + file + '/' + key + '_dmesg_' + now.strftime('%X').replace(':', '-'),
                              'w') as dmesg_file:
                        dmesg_file.write(dmesg_output)
            except:
                ssid_list = "ERROR"
                print("Error accessing VIF Config from AP CLI")
                client.update_testrail(case_id=test_cases["vlan_vifc"], run_id=rid, status_id=4,
                                       msg='Cannot determine VIF Config - re-test required')
                report_data['tests'][key][test_cases["vlan_vifc"]] = "error"

            # VIF State
            try:
                ssid_state = ap_connect.get_vif_state(ap_ip, ap_username, ap_password)
                print("SSIDs in AP VIF State:", ssid_state)

                if set(ssid_state) == set(ssid_config):
                    print("SSIDs properly applied on AP")
                    client.update_testrail(case_id=test_cases["vlan_vifs"], run_id=rid, status_id=1,
                                           msg='SSIDs in VIF Config applied to VIF State')
                    report_data['tests'][key][test_cases["vlan_vifs"]] = "passed"
                else:
                    print("SSIDs not applied on AP")
                    client.update_testrail(case_id=test_cases["vlan_vifs"], run_id=rid, status_id=5,
                                           msg='SSIDs in VIF Config not applied to VIF State')
                    report_data['tests'][key][test_cases["vlan_vifs"]] = "failed"

                    print('Writing logs...')
                    os.system('mkdir -p AP_Logs/' + now.strftime('%B') + '/' + now.strftime('%d') + '/' + file)
                    logread_output, dmesg_output = ap_connect.copy_logread_dmesg(ap_ip, ap_username, ap_password)

                    with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime(
                            '%d') + '/' + file + '/' + key + '_logread_' + now.strftime('%X').replace(':', '-'),
                              'w') as log_file:
                        log_file.write(logread_output)

                    with open('AP_Logs/' + now.strftime('%B') + '/' + now.strftime(
                            '%d') + '/' + file + '/' + key + '_dmesg_' + now.strftime('%X').replace(':', '-'),
                              'w') as dmesg_file:
                        dmesg_file.write(dmesg_output)
            except:
                ssid_list = "ERROR"
                print("Error accessing VIF State from AP CLI")
                print("Error accessing VIF Config from AP CLI")
                client.update_testrail(case_id=test_cases["vlan_vifs"], run_id=rid, status_id=4,
                                       msg='Cannot determine VIF State - re-test required')
                report_data['tests'][key][test_cases["vlan_vifs"]] = "error"

            ### Set port for LANForge
            port = test_info.lanforge_vlan_port

            # Print iwinfo for logs
            iwinfo = iwinfo_status(ap_ip, ap_username, ap_password)
            print(iwinfo)

            ###Run Client Single Connectivity Test Cases for VLAN SSIDs
            # TC- 2.4 GHz WPA2-Enterprise VLAN
            if args.skip_eap != True:
                test_case = test_cases["2g_eap_vlan"]
                radio = test_info.lanforge_2dot4g
                #sta_list = [lanforge_prefix + "5253"]
                sta_list = [test_info.lanforge_2dot4g_station]
                prefix = test_info.lanforge_2dot4g_prefix
                ssid_name = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2-EAP_SSID"]
                security = "wpa2"
                eap_type = "TTLS"
                try:
                    test_result = RunTest.Single_Client_EAP(port, sta_list, ssid_name, radio, prefix, security, eap_type,
                                                            identity,
                                                            ttls_password, test_case, rid)
                except:
                    test_result = "error"
                    Test.testrail_retest(test_case, rid, ssid_name)
                    pass
                report_data['tests'][key][int(test_case)] = test_result
                time.sleep(10)
            else:
                pass
            # TC - 2.4 GHz WPA2 VLAN
            test_case = test_cases["2g_wpa2_vlan"]
            radio = test_info.lanforge_2dot4g
            #station = [lanforge_prefix + "5251"]
            station = [test_info.lanforge_2dot4g_station]
            prefix = test_info.lanforge_2dot4g_prefix
            ssid_name = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2_SSID"]
            ssid_psk = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2_PSK"]
            security = "wpa2"
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, ssid_name, ssid_psk, security, station,
                                                              test_case,
                                                              rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, ssid_name)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(10)

            # TC 4323 - 2.4 GHz WPA VLAN
            test_case = test_cases["2g_wpa_vlan"]
            radio = test_info.lanforge_2dot4g
            #station = [lanforge_prefix + "5252"]
            station = [test_info.lanforge_2dot4g_station]
            prefix = test_info.lanforge_2dot4g_prefix
            ssid_name = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA_SSID"]
            ssid_psk = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA_PSK"]
            security = "wpa"
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, ssid_name, ssid_psk, security, station,
                                                              test_case, rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, ssid_name)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(10)

            # TC - 5 GHz WPA2-Enterprise VLAN
            if args.skip_eap != True:
                test_case = test_cases["5g_eap_vlan"]
                radio = test_info.lanforge_5g
                #sta_list = [lanforge_prefix + "5250"]
                sta_list = [test_info.lanforge_5g_station]
                prefix = test_info.lanforge_5g_prefix
                ssid_name = profile_info_dict[fw_model + '_vlan']["fiveG_WPA2-EAP_SSID"]
                security = "wpa2"
                eap_type = "TTLS"
                try:
                    test_result = RunTest.Single_Client_EAP(port, sta_list, ssid_name, radio, prefix, security, eap_type,
                                                            identity,
                                                            ttls_password, test_case, rid)
                except:
                    test_result = "error"
                    Test.testrail_retest(test_case, rid, ssid_name)
                    pass
                report_data['tests'][key][int(test_case)] = test_result
                time.sleep(10)
            else:
                pass

            # TC - 5 GHz WPA2 VLAN
            test_case = test_cases["5g_wpa2_vlan"]
            radio = test_info.lanforge_5g
            #station = [lanforge_prefix + "5248"]
            station = [test_info.lanforge_5g_station]
            prefix = test_info.lanforge_5g_prefix
            ssid_name = profile_info_dict[fw_model + '_vlan']["fiveG_WPA2_SSID"]
            ssid_psk = profile_info_dict[fw_model]["fiveG_WPA2_PSK"]
            security = "wpa2"
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, ssid_name, ssid_psk, security, station,
                                                              test_case,
                                                              rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, ssid_name)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(10)

            # TC 4324 - 5 GHz WPA VLAN
            test_case = test_cases["5g_wpa_vlan"]
            radio = test_info.lanforge_5g
            #station = [lanforge_prefix + "5249"]
            station = [test_info.lanforge_5g_station]
            prefix = test_info.lanforge_5g_prefix
            ssid_name = profile_info_dict[fw_model + '_vlan']["fiveG_WPA_SSID"]
            ssid_psk = profile_info_dict[fw_model]["fiveG_WPA_PSK"]
            security = "wpa"
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, ssid_name, ssid_psk, security, station,
                                                              test_case,
                                                              rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, ssid_name)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(10)

            # Update SSID Profile
            update_profile_id = str(fiveG_wpa)
            update_ssid = key + "_Updated_SSID_NAT"
            update_auth = "open"
            update_security = "open"
            update_psk = ""
            update_profile = CloudSDK.update_ssid_profile(cloudSDK_url, bearer, update_profile_id, update_ssid,
                                                          update_auth, update_psk)
            print(update_profile)
            time.sleep(90)

            # TC - Updated VLAN SSID profile
            test_case = test_cases["vlan_ssid_update"]
            radio = test_info.lanforge_5g
            station = [test_info.lanforge_5g_station]
            prefix = test_info.lanforge_5g_prefix
            try:
                test_result = Test.Single_Client_Connectivity(port, radio, prefix, update_ssid, update_psk,
                                                              update_security, station,
                                                              test_case,
                                                              rid)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, update_ssid)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            time.sleep(5)

            print(report_data['tests'][key])
            logger.info("Testing for " + fw_model + "Custom VLAN SSIDs Complete")
        else:
            print("Skipping VLAN tests at user request...")
            pass

        logger.info("Testing for " + fw_model + "Complete")

        # Add indication of complete TC pass/fail to sanity_status for pass to external json used by Throughput Test
        x = all(status == "passed" for status in report_data["tests"][key].values())
        print(x)

        if x == True:
            sanity_status['sanity_status'][key] = "passed"

        else:
            sanity_status['sanity_status'][key] = "failed"

        ##Update sanity_status.json to indicate there has been a test on at least one AP model tonight
        sanity_status['sanity_run']['new_data'] = "yes"

        print(sanity_status)

        # write to json file
        with open('sanity_status.json', 'w') as json_file:
            json.dump(sanity_status, json_file)

        # write to report_data contents to json file so it has something in case of unexpected fail
        print(report_data)
        with open(report_path + today + '/report_data.json', 'w') as report_json_file:
            json.dump(report_data, report_json_file)

        ###########################################################################
        ################# Post-test Prfofile Cleanup ##############################
        ###########################################################################

        # Set AP to use permanently available profile to allow for deletion of RADIUS, SSID, and AP profiles
        print("Cleaning up! Deleting created test profiles")
        print("Set AP to profile not created in test")
        ap_profile = CloudSDK.set_ap_profile(equipment_id, 6, cloudSDK_url, bearer)
        time.sleep(5)

        # Delete profiles in delete_list
        for x in delete_list:
            delete_profile = CloudSDK.delete_profile(cloudSDK_url, bearer, str(x))
            if delete_profile == "SUCCESS":
                print("profile", x, "delete successful")
            else:
                print("Error deleting profile")


# Dump all sanity test results to external json file again just to be sure
with open('sanity_status.json', 'w') as json_file:
    json.dump(sanity_status, json_file)

# Calculate percent of tests passed for report
for key in ap_models:
    if report_data['fw_available'][key] == "No":
        report_data["pass_percent"][key] = "Not Run"
    else:
        # no_of_tests = len(report_data["tests"][key])
        passed_tests = sum(x == "passed" for x in report_data["tests"][key].values())
        failed_tests = sum(y == "failed" for y in report_data["tests"][key].values())
        error_tests = sum(z == "error" for z in report_data["tests"][key].values())
        no_of_tests = len(case_ids)
        if no_of_tests == 0:
            print("No tests run for", key)
        else:
            print("--- Test Data for", key, "---")
            print(key, "tests passed:", passed_tests)
            print(key, "tests failed:", failed_tests)
            print(key, "tests with error:", error_tests)
            print(key, "total tests:", no_of_tests)
            percent = float(passed_tests / no_of_tests) * 100
            percent_pass = round(percent, 2)
            print(key, "pass rate is", str(percent_pass) + "%")
            print("---------------------------")
            report_data["pass_percent"][key] = str(percent_pass) + '%'

# write to report_data contents to json file
print(report_data)
with open(report_path + today + '/report_data.json', 'w') as report_json_file:
    json.dump(report_data, report_json_file)

print(".....End of Sanity Test.....")
logger.info("End of Sanity Test run")
