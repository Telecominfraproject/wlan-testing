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
import testrail_api
import logging
import datetime
import time
from datetime import date
from shutil import copyfile
import argparse
from unittest.mock import Mock

# For finding files
# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
import glob

# external_results_dir=/var/tmp/lanforge

# To run this from your home system to NOLA-01 testbed, use this command.
# This assumes you have set up an ssh tunnel logged to the cicd jumphost that can
# reach the lab.
# In separate console to set up the ssh tunnel:
#ssh -C -L 7220:lab-ctlr:22 ubuntu@3.130.51.163
# On local machine:
#./query_ssids.py --testrail-user-id NONE --model ecw5410 --ap-jumphost-address localhost --ap-jumphost-port 7220 --ap-jumphost-password secret --ap-jumphost-tty /dev/ttyAP1 --equipment_id 3

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

import sys
for folder in 'py-json','py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../lanforge/lanforge-scripts/{folder}')

from LANforge.LFUtils import *

# if you lack __init__.py in this directory you will not find sta_connect module#

import sta_connect2
from sta_connect2 import StaConnect2
import testrail_api
from testrail_api import TestRail_Client
import eap_connect
from eap_connect import EAPConnect
import cloudsdk
from cloudsdk import CloudSDK
import ap_ssh
from ap_ssh import ssh_cli_active_fw
from ap_ssh import iwinfo_status

##Import info for lab setup and APs under test
import lab_ap_info
from lab_ap_info import profile_info_dict
from lab_ap_info import cloud_sdk_models
from lab_ap_info import ap_models
from lab_ap_info import customer_id
from lab_ap_info import cloud_type
from lab_ap_info import test_cases
from lab_ap_info import radius_info

parser = argparse.ArgumentParser(description="Sanity Testing on Firmware Build")
parser.add_argument("-b", "--build-id", type=str, help="FW commit ID (latest pending build on dev is default)",
                    default = "pending")
parser.add_argument("--skip-upgrade", type=bool, help="Skip upgrading firmware",
                    default = False)
parser.add_argument("--force-upgrade", type=bool, help="Force upgrading firmware even if it is already current version",
                    default = False)
parser.add_argument("-m", "--model", type=str, choices=['ea8300', 'ecw5410', 'ecw5211', 'ec420'],
                    help="AP model to be run", required=True)
parser.add_argument("--equipment_id", type=str,
                    help="AP model ID, as exists in the cloud-sdk", required=True)

parser.add_argument("--sdk-base-url", type=str, help="cloudsdk base url",
                    default="https://wlan-portal-svc.cicd.lab.wlan.tip.build")
parser.add_argument("--sdk-user-id", type=str, help="cloudsdk user id",
                    default="support@example.com")
parser.add_argument("--sdk-user-password", type=str, help="cloudsdk user password",
                    default="support")

parser.add_argument("--jfrog-base-url", type=str, help="jfrog base url",
                    default="tip.jFrog.io/artifactory/tip-wlan-ap-firmware")
parser.add_argument("--jfrog-user-id", type=str, help="jfrog user id",
                    default="tip-read")
parser.add_argument("--jfrog-user-password", type=str, help="jfrog user password",
                    default="tip-read")

parser.add_argument("--testrail-base-url", type=str, help="testrail base url",   # was os.getenv('TESTRAIL_URL')
                    default="https://telecominfraproject.testrail.com")
parser.add_argument("--testrail-project", type=str, help="testrail project name",
                    default="opsfleet-wlan")
parser.add_argument("--testrail-user-id", type=str, help="testrail user id.  Use 'NONE' to disable use of testrails.",
                    default="gleb@opsfleet.com")
parser.add_argument("--testrail-user-password", type=str, help="testrail user password",
                    default="password")
parser.add_argument("--testrail-run-prefix", type=str, help="testrail run prefix",
                    default="prefix-1")
parser.add_argument("--milestone", type=str, help="testrail milestone ID",
                    default="milestone-1")

parser.add_argument("--lanforge-ip-address", type=str, help="ip address of the lanforge gui",
                    default="127.0.0.1")
parser.add_argument("--lanforge-port-number", type=str, help="port of the lanforge gui",
                    default="8080")
parser.add_argument("--lanforge-prefix", type=str, help="LANforge api prefix string",
                    default="sdk")

parser.add_argument("--local_dir", type=str, help="Sanity logging directory",
                    default="logs")
parser.add_argument("--report-path", type=str, help="Sanity report directory",
                    default="reports")
parser.add_argument("--report-template", type=str, help="Sanity report template",
                    default="reports/report_template.php")

parser.add_argument("--eap-id", type=str, help="EAP indentity",
                    default="lanforge")
parser.add_argument("--ttls-password", type=str, help="TTLS password",
                    default="lanforge")

parser.add_argument("--ap-ip", type=str, help="AP IP Address, for direct ssh access if not using jumphost",
                    default="127.0.0.1")
parser.add_argument("--ap-username", type=str, help="AP username",
                    default="root")
parser.add_argument("--ap-password", type=str, help="AP password",
                    default="root")
parser.add_argument("--ap-jumphost-address", type=str, help="IP of system that we can ssh in to get serial console access to AP",
                    default=None)
parser.add_argument("--ap-jumphost-port", type=str, help="SSH port to use in case we are using ssh tunneling or other non-standard ports",
                    default="22")
parser.add_argument("--ap-jumphost-username", type=str, help="User-ID for system that we can ssh in to get serial console access to AP",
                    default="lanforge")
parser.add_argument("--ap-jumphost-password", type=str, help="Passwort for system that we can ssh in to get serial console access to AP",
                    default="lanforge")
parser.add_argument("--ap-jumphost-wlan-testing", type=str, help="wlan-testing repo dir on the jumphost",
                    default="git/wlan-testing")
parser.add_argument("--ap-jumphost-tty", type=str, help="Serial port for the AP we wish to talk to",
                    default="UNCONFIGURED-JUMPHOST-TTY")

parser.add_argument('--skip-update-firmware', dest='update_firmware', action='store_false')
parser.set_defaults(update_firmware=True)
command_line_args = parser.parse_args()

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
lanforge_prefix = command_line_args.lanforge_prefix

build = command_line_args.build_id

logger = logging.getLogger('Nightly_Sanity')
hdlr = logging.FileHandler(local_dir + "/Nightly_Sanity.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

client: TestRail_Client = TestRail_Client(command_line_args)

####Use variables other than defaults for running tests on custom FW etc

model_id = command_line_args.model
equipment_id = command_line_args.equipment_id

logger.info('Start of SSID tests')

###Get Cloud Bearer Token
cloud: CloudSDK = CloudSDK(command_line_args)
bearer = cloud.get_bearer(cloudSDK_url, cloud_type)

customer_id = "2"

# 5G SSIDs
try:
    ssids = cloud.get_customer_profiles(cloudSDK_url, bearer, customer_id)
    print("Profiles for customer %s:"%(customer_id))
    #jobj = json.load(ssids)
    print(json.dumps(ssids, indent=4, sort_keys=True))
except Exception as ex:
    print(ex)
    logging.error(logging.traceback.format_exc())
    print("Failed to read customer profiles")
