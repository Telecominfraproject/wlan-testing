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

local_dir="logs/"
#print("Local Directory where all files will be copied and logged", local_dir)
tr_user="syama.devi@connectus.ai"
tr_pw="Connectus123$"
#print ("Testrail password =", tr_pw)
aws_host='3.96.56.0'
aws_user='ubuntu'

logger = logging.getLogger('Nightly_Sanity')
hdlr = logging.FileHandler(local_dir+"/Nightly_Sanity.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
logger.info('Start Nightly Sanity run')

# For finding files
# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
import glob
#external_results_dir=/var/tmp/lanforge


if sys.version_info[0] != 3:
       print("This script requires Python 3")
       exit(1)
if 'py-json' not in sys.path:
       sys.path.append('../py-json')

from LANforge.LFUtils import *
# if you lack __init__.py in this directory you will not find sta_connect module#
import sta_connect
import sta_connect2
import testrail_api
from sta_connect import StaConnect
from sta_connect2 import StaConnect2
from testrail_api import APIClient
from datetime import date
client: APIClient = APIClient('https://telecominfraproject.testrail.com')
client.user = tr_user
client.password = tr_pw


###Class for jfrog Interaction
class GetBuild:
    def __init__(self):
        self.user = 'cicd_user'
        self.password = 'fepv6nj9guCPeEHC'
        ssl._create_default_https_context = ssl._create_unverified_context

    def get_latest_image(self,url):

        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()
        headers = {'Authorization': 'Basic ' + auth}

        ''' FIND THE LATEST FILE NAME'''
        #print(url)
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html, features="html.parser")
        ##find the last pending link on dev
        last_link = soup.find_all('a', href=re.compile("pending"))[-1]
        latest_file=last_link['href']
        latest_fw = latest_file.replace('.tar.gz','')
        return latest_fw

###Class for CloudSDK Interaction via RestAPI
class CloudSDK:
    def __init__(self):
        self.user = 'support@example.com'

    def get_bearer():
        cloud_login_url = "https://wlan-portal-svc.demo.lab.wlan.tip.build/management/v1/oauth2/token"
        payload = "{\n    \"userId\": \"support@example.com\",\n    \"password\": \"support\"\n}"
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            token_response = requests.request("POST", cloud_login_url, headers=headers, data=payload)
        except requests.exceptions.RequestException as e:
            raise SystemExit("Exiting Script! Cloud not get bearer token for reason:",e)
        token_data = token_response.json()
        bearer_token = token_data['access_token']
        return(bearer_token)

    def ap_firmware(customer_id,equipment_id):
        equip_fw_url = "https://wlan-portal-svc.demo.lab.wlan.tip.build/portal/status/forEquipment?customerId="+customer_id+"&equipmentId="+equipment_id
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        status_response = requests.request("GET", equip_fw_url, headers=headers, data=payload)
        status_data = status_response.json()
        current_ap_fw = status_data[2]['details']['reportedSwVersion']
        return current_ap_fw

    def CloudSDK_images(apModel):
        getFW_url = "https://wlan-portal-svc.demo.lab.wlan.tip.build/portal/firmware/version/byEquipmentType?equipmentType=AP&modelId=" + apModel
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("GET", getFW_url, headers=headers, data=payload)
        ap_fw_details = response.json()
        ###return ap_fw_details
        fwlist = []
        for version in ap_fw_details:
           fwlist.append(version.get('versionName'))
        return(fwlist)
        #fw_versionNames = ap_fw_details[0]['versionName']
        #return fw_versionNames

    def firwmare_upload(commit, apModel,latest_image,fw_url):
        fw_upload_url = "https://wlan-portal-svc.demo.lab.wlan.tip.build/portal/firmware/version"
        payload = "{\n  \"model_type\": \"FirmwareVersion\",\n  \"id\": 0,\n  \"equipmentType\": \"AP\",\n  \"modelId\": \""+apModel+"\",\n  \"versionName\": \""+latest_image+"\",\n  \"description\": \"\",\n  \"filename\": \""+fw_url+"\",\n  \"commit\": \""+commit+"\",\n  \"validationMethod\": \"MD5_CHECKSUM\",\n  \"validationCode\": \"19494befa87eb6bb90a64fd515634263\",\n  \"releaseDate\": 1596192028877,\n  \"createdTimestamp\": 0,\n  \"lastModifiedTimestamp\": 0\n}\n\n"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", fw_upload_url, headers=headers, data=payload)
        #print(response)
        upload_result = response.json()
        return(upload_result)

    def get_firmware_id(latest_ap_image):
        #print(latest_ap_image)
        fw_id_url = "https://wlan-portal-svc.demo.lab.wlan.tip.build/portal/firmware/version/byName?firmwareVersionName="+latest_ap_image

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("GET", fw_id_url, headers=headers, data=payload)
        fw_data = response.json()
        latest_fw_id = fw_data['id']
        return latest_fw_id

    def update_firmware(equioment_id, latest_firmware_id):
        url = "https://wlan-portal-svc.demo.lab.wlan.tip.build/portal/equipmentGateway/requestFirmwareUpdate?equipmentId="+equipment_id+"&firmwareVersionId="+latest_firmware_id

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

    def set_ap_profile(equipment_id,test_profile_id):
        ###Get AP Info
        url = "https://wlan-portal-svc.demo.lab.wlan.tip.build/portal/equipment?equipmentId="+equipment_id
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        print(response)

        ###Add Lab Profile ID to Equipment
        equipment_info = response.json()
        #print(equipment_info)
        equipment_info["profileId"] = test_profile_id
        #print(equipment_info)

        ###Update AP Info with Required Profile ID
        url = "https://wlan-portal-svc.demo.lab.wlan.tip.build/portal/equipment"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("PUT", url, headers=headers, data=json.dumps(equipment_info))
        #print(response)

###Class for Tests
class RunTest:
    def Single_Client_Connectivity(self, radio, ssid_name, ssid_psk, security, station, test_case, rid):
        '''SINGLE CLIENT CONNECTIVITY using sta_connect2.py'''
        staConnect = StaConnect2("10.10.10.201", 8080, debug_= False)
        staConnect.sta_mode = 0
        staConnect.upstream_resource = 1
        staConnect.upstream_port = "eth2"
        staConnect.radio = radio
        staConnect.resource = 1
        staConnect.dut_ssid = ssid_name
        staConnect.dut_passwd = ssid_psk
        staConnect.dut_security = security
        staConnect.station_names = station
        staConnect.runtime_secs = 30
        staConnect.cleanup_on_exit = True
        staConnect.setup()
        staConnect.start()
        print("napping %f sec" % staConnect.runtime_secs)
        time.sleep(staConnect.runtime_secs)
        staConnect.stop()
        staConnect.cleanup()
        run_results = staConnect.get_result_list()
        for result in run_results:
            print("test result: " + result)
        #result = 'pass'
        print("Single Client Connectivity :",staConnect.passes)
        if staConnect.passes() == True:
            print("Single client connection to", ssid_name, "successful. Test Passed")
            client.update_testrail(case_id=test_case, run_id=rid, status_id=1, msg='Client connectivity passed')
        else:
            client.update_testrail(case_id=test_case, run_id=rid, status_id=5, msg='Client connectivity failed')
            print("Single client connection to", ssid_name, "unsuccessful. Test Failed")

    def Client_Count(customer_id, equipment_id):
        url = "https://wlan-portal-svc.demo.lab.wlan.tip.build/portal/status/forEquipment?customerId=" + customer_id + "&equipmentId=" + equipment_id
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text.encode('utf8'))


    def TestCase_941(self, rid):
        #MULTI CLIENT CONNECTIVITY
        staConnect = StaConnect2("10.10.10.201", 8080, debug_= True)
        staConnect.sta_mode = 0
        staConnect.upstream_resource = 1
        staConnect.upstream_port = "eth2"
        staConnect.radio = "wiphy0"
        staConnect.resource = 1
        staConnect.dut_ssid = "LAB_2dot4G_WPA2"
        # staConnect.dut_passwd = "4C0nnectUS!"
        staConnect.dut_passwd = "Connectus123$"
        staConnect.dut_security = "wpa2"
        staConnect.station_names = ["sta0020", 'sta0021', 'sta0022', 'sta0023']
        staConnect.runtime_secs = 20
        staConnect.cleanup_on_exit = True
        staConnect.run()
        run_results = staConnect.get_result_list()
        for result in run_results:
            print("test result: " + result)
        if staConnect.passes() == True:
            client.update_testrail(case_id=941, run_id=rid, status_id=1,
                                   msg='client Connectivity to SSID Passed ')
        else:
            client.update_testrail(case_id=941, run_id=rid, status_id=5,
                                   msg='client connectivity to SSID Failed')

######Testrail Project and Run ID Information ##############################

Test: RunTest = RunTest()

projId = client.get_project_id(project_name= 'WLAN')
print("TIP WLAN Project ID is:", projId)

logger.info('Start of Nightly Sanity')



###Dictionaries
ap_latest_dict = {
  "ea8300": "Unknown",
  "ecw5410": "unknown"
}

ap_updated_dict = {
  "ea8300": "",
  "ecw5410": ""
}

##Equipment IDs for Lab APs under test
equipment_id_dict = {
    "ea8300": "3",
    "ecw5410": "6"
}

###Testing AP Profile Information
profile_info_dict = {
    "ecw5410": {
        "profile_id": "7",
        "fiveG_WPA2_SSID": "ECW5410_5G_WPA2",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "ECW5410_5G_WPA",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "ECW5410_5G_OPEN",
        "twoFourG_OPEN_SSID": "ECW5410_2dot4G_OPEN",
        "twoFourG_WPA2_SSID": "ECW5410_2dot4G_WPA2",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID":"ECW5410_2dot4G_WPA",
        "twoFourG_WPA_PSK": "Connectus123$"
        },

    "ea8300": {
        "profile_id": "24",
        "fiveG_WPA2_SSID": "EA8300_5G_WPA2",
        "fiveG_WPA2_PSK": "Connectus123$",
        "fiveG_WPA_SSID": "EA8300_5G_WPA",
        "fiveG_WPA_PSK": "Connectus123$",
        "fiveG_OPEN_SSID": "EA8300_5G_OPEN",
        "twoFourG_OPEN_SSID": "EA8300_2dot4G_OPEN",
        "twoFourG_WPA2_SSID": "EA8300_2dot4G_WPA2",
        "twoFourG_WPA2_PSK": "Connectus123$",
        "twoFourG_WPA_SSID":"EA8300_2dot4G_WPA",
        "twoFourG_WPA_PSK": "Connectus123$"
        }

}

##Test Cases to be included in Test Runs
test_cases = [
       2233,
       2234,
       2235,
       2236,
       2237,
       2419,
       2420
]

##AP models
ap_models = ["ea8300","ecw5410"]
#ap_models = ["ecw5410"]

###Get Cloud Bearer Token
bearer = CloudSDK.get_bearer()



#############################################################################
##################### CloudSDK Firmware Check ###############################
### 1) Get Token for CloudSDK ###############################################
### 2) Find Latest FW on jfrog for each AP Model ############################
### 3) Find Available FW on CloudSDK --> if Latest FW not present, upload ###
#############################################################################

###Check Latest FW Version on jfrog and CloudSDK for each model
for model in ap_models:
    apModel = model
    ###Check Latest FW on jFrog
    jfrog_url = 'https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/'
    url = jfrog_url + apModel + "/dev/"
    Build: GetBuild = GetBuild()
    latest_image = Build.get_latest_image(url)
    print(model,"Latest FW on jFrog:",latest_image)
    ###Check images already on CloudSDK
    firmware_list_by_model = CloudSDK.CloudSDK_images(apModel)
    print("Available",apModel,"Firmware on CloudSDK:",firmware_list_by_model)

    if latest_image in firmware_list_by_model:
        print("Latest Firmware",latest_image,"is on CloudSDK!")
        ap_latest_dict[model] = latest_image
        ap_updated_dict[model] = "Up to Date"

    else:
        print("Latest Firmware is not on CloudSDK! Uploading...")
        fw_url = "https://cicd_user:fepv6nj9guCPeEHC@tip.jfrog.io/artifactory/tip-wlan-ap-firmware/" + apModel + "/dev/" + latest_image + ".tar.gz"
        #print(fw_url)
        commit = latest_image.split("-")[-1]
        fw_upload_status = CloudSDK.firwmare_upload(commit, apModel,latest_image,fw_url)
        #print(fw_upload_status)
        fw_id = fw_upload_status['id']
        print("Upload Complete.",latest_image,"FW ID is",fw_id)
        ap_latest_dict[model] = latest_image
        ap_updated_dict[model] = "Outdated"


sleep(1)
#print(ap_updated_dict)
if (ap_updated_dict["ea8300"] == "Up to Date") and (ap_updated_dict["ecw5410"] == "Up to Date"):
    print("All AP FW loads up to date on CloudSDK")
    logger.info("Newest builds on jfrog already loaded to CloudSDK")
else:
    print("All new FW loads created on CloudSDK")
    logger.info("New loads have been created on CloudSDK")
#print("Latest FW List:",ap_latest_dict)

####################################################################################
####################################################################################
############ Update FW and Run Test Cases on Each AP Variant #######################
####################################################################################
####################################################################################

for key in equipment_id_dict:
    ###Get Current AP Firmware and upgrade
    customer_id = "2"
    equipment_id = equipment_id_dict[key]
    ap_fw = CloudSDK.ap_firmware(customer_id,equipment_id)
    fw_model = ap_fw.partition("-")[0]
    print("AP MODEL UNDER TEST IS", fw_model)
    print ('Current AP Firmware:', ap_fw)
    ###Find Latest FW for Current AP Model and Get FW ID

    latest_ap_image = ap_latest_dict[fw_model]
    model_firmware_id = CloudSDK.get_firmware_id(latest_ap_image)
    latest_firmware_id = str(model_firmware_id)
    print("Latest FW ID is:",latest_firmware_id)

    ##Compare Latest and Current AP FW and Upgrade
    if ap_fw == latest_ap_image:
        print('FW does not require updating')
        logger.info(fw_model + " does not require upgrade. Not performing sanity tests for this AP variant")
        #raise SystemExit("No new FW loads available. Exiting Test...")

    else:
        print('FW needs updating')
        #Upgrade AP firmware
        upgrade_fw = CloudSDK.update_firmware(equipment_id, latest_firmware_id)
        logger.info("Lab "+fw_model+" Requires FW update")
        time.sleep(300)

        ###Create Test Run
        today = str(date.today())
        test_run_name = "Daily_Sanity_"+fw_model+"_"+today
        client.create_testrun(name=test_run_name, case_ids=test_cases, project_id=projId)
        rid = client.get_run_id(test_run_name="Daily_Sanity_"+fw_model+"_"+today)

        print("TIP run ID is:", rid)

        #Check if upgrade worked
        ap_fw = CloudSDK.ap_firmware(customer_id, equipment_id)
        print('Current AP Firmware:', ap_fw)
        if ap_fw == latest_ap_image:
            print("Upgrade Successful!")
            client.update_testrail(case_id="2233", run_id=rid, status_id=1,msg='Upgrade successful')
            logger.info("Lab "+fw_model+" upgrade SUCCESS. Proceeding with sanity testing for this AP variant")
        else:
            client.update_testrail(case_id="2233", run_id=rid, status_id=5, msg='Upgrade Failed')
            logger.warning("Lab "+fw_model+" upgrade FAILED")
            print("AP FW Upgrade Failed. Updating TestRail and skipping sanity testing for this AP variant...")
            continue


        ###Set Proper AP Profile
        test_profile_id = profile_info_dict[fw_model]["profile_id"]
        print(test_profile_id)
        ap_profile = CloudSDK.set_ap_profile(equipment_id,test_profile_id)

        ###Run Client Single Connectivity Test Cases
        #TC 2237 - 2.4 GHz WPA2
        test_case = "2237"
        radio = "wiphy0"
        station = ["sta2237"]
        ssid_name = profile_info_dict[fw_model]["twoFourG_WPA2_SSID"]
        ssid_psk = profile_info_dict[fw_model]["twoFourG_WPA2_PSK"]
        security = "wpa2"
        Test.Single_Client_Connectivity(radio, ssid_name, ssid_psk, security, station, test_case, rid)

        time.sleep(10)

        #TC 2420 - 2.4 GHz WPA
        test_case = "2420"
        radio = "wiphy0"
        station = ["sta2420"]
        ssid_name = profile_info_dict[fw_model]["twoFourG_WPA_SSID"]
        ssid_psk = profile_info_dict[fw_model]["twoFourG_WPA_PSK"]
        security = "wpa"
        Test.Single_Client_Connectivity(radio, ssid_name, ssid_psk, security, station, test_case, rid)

        time.sleep(10)

        #TC 2234 - 2.4 GHz Open
        test_case = "2234"
        radio = "wiphy0"
        station = ["sta2234"]
        ssid_name = profile_info_dict[fw_model]["twoFourG_OPEN_SSID"]
        ssid_psk = "BLANK"
        security = "open"
        Test.Single_Client_Connectivity(radio, ssid_name, ssid_psk, security, station, test_case, rid)

        time.sleep(10)

        #TC 2236 - 5 GHz WPA2
        test_case = "2236"
        radio = "wiphy3"
        station = ["sta2236"]
        ssid_name = profile_info_dict[fw_model]["fiveG_WPA2_SSID"]
        ssid_psk = profile_info_dict[fw_model]["fiveG_WPA2_PSK"]
        security = "wpa2"
        Test.Single_Client_Connectivity(radio, ssid_name, ssid_psk, security, station, test_case, rid)

        time.sleep(10)

        #TC 2419 - 5 GHz WPA
        test_case = "2419"
        radio = "wiphy3"
        station = ["sta2419"]
        ssid_name = profile_info_dict[fw_model]["fiveG_WPA_SSID"]
        ssid_psk = profile_info_dict[fw_model]["fiveG_WPA_PSK"]
        security = "wpa"
        Test.Single_Client_Connectivity(radio, ssid_name, ssid_psk, security, station, test_case, rid)

        time.sleep(10)

        #TC 2235 - 5 GHz Open
        test_case = "2235"
        radio = "wiphy3"
        station = ["sta2235"]
        ssid_name = profile_info_dict[fw_model]["fiveG_OPEN_SSID"]
        ssid_psk = "BLANK"
        security = "open"
        Test.Single_Client_Connectivity(radio, ssid_name, ssid_psk, security, station, test_case, rid)

print(".....End of Sanity Test.....")
logger.info("End of Sanity Test run")