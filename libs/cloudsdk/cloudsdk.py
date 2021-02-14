#!/usr/bin/python3

##################################################################################
# Module contains functions to interact with CloudSDK using APIs
# Start by calling get_bearer to obtain bearer token, then other APIs can be used
#
# Used by Nightly_Sanity and Throughput_Test #####################################
##################################################################################

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
from ap_ssh import ssh_cli_active_fw
import lab_ap_info
import ap_ssh


###Class for CloudSDK Interaction via RestAPI
class CloudSDK:
    def __init__(self, command_line_args):
        self.user = command_line_args.sdk_user_id
        self.password = command_line_args.sdk_user_password
        self.assert_bad_response = False
        self.verbose = command_line_args.verbose
        self.base_url = command_line_args.sdk_base_url
        self.cloud_type = "v1"
        self.refresh_bearer()

    def refresh_bearer(self):
        self.bearer = self.get_bearer(self.base_url, self.cloud_type)

    def get_bearer(self, cloudSDK_url, cloud_type):
        cloud_login_url = cloudSDK_url + "/management/" + cloud_type + "/oauth2/token"
        payload = '''
        {
        "userId": "''' + self.user + '''",
        "password": "''' + self.password + '''"
        }   
        '''
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            token_response = requests.request("POST", cloud_login_url, headers=headers, data=payload)
            self.check_response("POST", token_response, headers, payload, cloud_login_url)
        except requests.exceptions.RequestException as e:
            raise SystemExit("Exiting Script! Cloud not get bearer token for reason:", e)
        token_data = token_response.json()
        bearer_token = token_data['access_token']
        bearer = bearer_token
        return (bearer_token)

    def check_response(self, cmd, response, headers, data_str, url):
        if response.status_code >= 500 or self.verbose:
            if response.status_code >= 500:
                print("check-response: ERROR, url: ", url)
            else:
                print("check-response: url: ", url)
            print("Command: ", cmd)
            print("response-status: ", response.status_code)
            print("response-headers: ", response.headers)
            print("response-content: ", response.content)
            print("headers: ", headers)
            print("data-str: ", data_str)

        if response.status_code >= 500:
            if self.assert_bad_response:
                raise NameError("Invalid response code.")
            return False
        return True

    def should_upgrade_ap_fw(self, force_upgrade, skip_upgrade, report_data, latest_ap_image, fw_model, ap_cli_fw,
                             logger):
        do_upgrade = False
        if ap_cli_fw == latest_ap_image and force_upgrade != True:
            print('FW does not require updating')
            if report_data:
                report_data['fw_available'][key] = "No"
            if logger:
                logger.info(fw_model + " does not require upgrade.")
            cloudsdk_cluster_info = {
                "date": "N/A",
                "commitId": "N/A",
                "projectVersion": "N/A"
            }
            if report_data:
                report_data['cloud_sdk'][key] = cloudsdk_cluster_info

        if ap_cli_fw != latest_ap_image and skip_upgrade == True:
            print('FW needs updating, but skip_upgrade is True, so skipping upgrade')
            if report_data:
                report_data['fw_available'][key] = "No"
            if logger:
                logger.info(fw_model + " firmware upgrade skipped, running with " + ap_cli_fw)
            cloudsdk_cluster_info = {
                "date": "N/A",
                "commitId": "N/A",
                "projectVersion": "N/A"
            }
            if report_data:
                report_data['cloud_sdk'][key] = cloudsdk_cluster_info

        if (ap_cli_fw != latest_ap_image or force_upgrade == True) and not skip_upgrade:
            print('Updating firmware, old: %s  new: %s' % (ap_cli_fw, latest_ap_image))
            do_upgrade = True
            if report_data:
                report_data['fw_available'][key] = "Yes"
                report_data['fw_under_test'][key] = latest_ap_image

        return do_upgrade

    # client is testrail client
    def do_upgrade_ap_fw(self, command_line_args, report_data, test_cases, testrail_client, ap_image, cloudModel, model,
                         jfrog_user, jfrog_pwd, testrails_rid, customer_id, equipment_id, logger):
        ###Test Create Firmware Version
        key = model
        rid = testrails_rid
        cloudSDK_url = self.base_url
        bearer = self.bearer
        if test_cases:
            test_id_fw = test_cases["create_fw"]
        print(cloudModel)
        firmware_list_by_model = self.CloudSDK_images(cloudModel, cloudSDK_url, bearer)
        print("Available", cloudModel, "Firmware on CloudSDK:", firmware_list_by_model)

        if ap_image in firmware_list_by_model:
            print("Latest Firmware", ap_image, "is already on CloudSDK, need to delete to test create FW API")
            old_fw_id = self.get_firmware_id(ap_image, cloudSDK_url, bearer)
            delete_fw = self.delete_firmware(str(old_fw_id), cloudSDK_url, bearer)
            fw_url = "https://" + jfrog_user + ":" + jfrog_pwd + "@tip.jfrog.io/artifactory/tip-wlan-ap-firmware/" + key + "/dev/" + ap_image + ".tar.gz"
            commit = ap_image.split("-")[-1]
            try:
                fw_upload_status = self.firwmare_upload(commit, cloudModel, ap_image, fw_url, cloudSDK_url,
                                                        bearer)
                fw_id = fw_upload_status['id']
                print("Upload Complete.", ap_image, "FW ID is", fw_id)
                if testrail_client:
                    testrail_client.update_testrail(case_id=test_id_fw, run_id=rid, status_id=1,
                                                    msg='Create new FW version by API successful')
                if report_data:
                    report_data['tests'][key][test_id_fw] = "passed"
            except:
                fw_upload_status = 'error'
                print("Unable to upload new FW version. Skipping Sanity on AP Model")
                if testrail_client:
                    testrail_client.update_testrail(case_id=test_id_fw, run_id=rid, status_id=5,
                                                    msg='Error creating new FW version by API')
                if report_data:
                    report_data['tests'][key][test_id_fw] = "failed"
                return False
        else:
            print("Latest Firmware is not on CloudSDK! Uploading...")
            fw_url = "https://" + jfrog_user + ":" + jfrog_pwd + "@tip.jfrog.io/artifactory/tip-wlan-ap-firmware/" + key + "/dev/" + ap_image + ".tar.gz"
            commit = ap_image.split("-")[-1]
            try:
                fw_upload_status = self.firwmare_upload(commit, cloudModel, ap_image, fw_url, cloudSDK_url,
                                                        bearer)
                fw_id = fw_upload_status['id']
                print("Upload Complete.", ap_image, "FW ID is", fw_id)
                if testrail_client:
                    testrail_client.update_testrail(case_id=test_id_fw, run_id=rid, status_id=1,
                                                    msg='Create new FW version by API successful')
                if report_data:
                    report_data['tests'][key][test_id_fw] = "passed"
            except:
                fw_upload_status = 'error'
                print("Unable to upload new FW version. Skipping Sanity on AP Model")
                if testrail_client:
                    testrail_client.update_testrail(case_id=test_id_fw, run_id=rid, status_id=5,
                                                    msg='Error creating new FW version by API')
                if report_data:
                    report_data['tests'][key][test_id_fw] = "failed"
                return False

        # Upgrade AP firmware
        print("Upgrading...firmware ID is: ", fw_id)
        upgrade_fw = self.update_firmware(equipment_id, str(fw_id), cloudSDK_url, bearer)
        if logger:
            logger.info("Lab " + model + " Requires FW update")
        print(upgrade_fw)

        if "success" in upgrade_fw:
            if upgrade_fw["success"] == True:
                print("CloudSDK Upgrade Request Success")
                if report_data and test_cases:
                    report_data['tests'][key][test_cases["upgrade_api"]] = "passed"
                if testrail_client:
                    testrail_client.update_testrail(case_id=test_cases["upgrade_api"], run_id=rid, status_id=1,
                                                    msg='Upgrade request using API successful')
                if logger:
                    logger.info('Firmware upgrade API successfully sent')
            else:
                print("Cloud SDK Upgrade Request Error!")
                # mark upgrade test case as failed with CloudSDK error
                if test_cases:
                    if testrail_client:
                        testrail_client.update_testrail(case_id=test_cases["upgrade_api"], run_id=rid, status_id=5,
                                                        msg='Error requesting upgrade via API')
                    if report_data:
                        report_data['tests'][key][test_cases["upgrade_api"]] = "failed"
                if logger:
                    logger.warning('Firmware upgrade API failed to send')
                return False
        else:
            print("Cloud SDK Upgrade Request Error!")
            # mark upgrade test case as failed with CloudSDK error
            if test_cases:
                if testrail_client:
                    testrail_client.update_testrail(case_id=test_cases["upgrade_api"], run_id=rid, status_id=5,
                                                    msg='Error requesting upgrade via API')
                if report_data:
                    report_data['tests'][key][test_cases["upgrade_api"]] = "failed"
            if logger:
                logger.warning('Firmware upgrade API failed to send')
            return False

        sdk_ok = False
        for i in range(10):
            time.sleep(30)
            # Check if upgrade success is displayed on CloudSDK
            if test_cases:
                test_id_cloud = test_cases["cloud_fw"]
            cloud_ap_fw = self.ap_firmware(customer_id, equipment_id, cloudSDK_url, bearer)
            print('Current AP Firmware from CloudSDK: %s  requested-image: %s' % (cloud_ap_fw, ap_image))
            if logger:
                logger.info('AP Firmware from CloudSDK: ' + cloud_ap_fw)
            if cloud_ap_fw == "ERROR":
                print("AP FW Could not be read from CloudSDK")

            elif cloud_ap_fw == ap_image:
                print("CloudSDK status shows upgrade successful!")
                sdk_ok = True
                break

            else:
                print("AP FW from CloudSDK status is not latest build. Will try again in 30 seconds.")

        cli_ok = False
        if sdk_ok:
            for i in range(10):
                # Check if upgrade successful on AP CLI
                if test_cases:
                    test_id_cli = test_cases["ap_upgrade"]
                try:
                    ap_cli_info = ssh_cli_active_fw(command_line_args)
                    ap_cli_fw = ap_cli_info['active_fw']
                    print("CLI reporting AP Active FW as:", ap_cli_fw)
                    if logger:
                        logger.info('Firmware from CLI: ' + ap_cli_fw)
                    if ap_cli_fw == ap_image:
                        cli_ok = True
                        break
                    else:
                        print("probed api-cli-fw: %s  !=  requested-image: %s" % (ap_cli_fw, ap_image))
                        continue
                except Exception as ex:
                    ap_cli_info = "ERROR"
                    print(ex)
                    logging.error(logging.traceback.format_exc())
                    print("Cannot Reach AP CLI to confirm upgrade!")
                    if logger:
                        logger.warning('Cannot Reach AP CLI to confirm upgrade!')
                    if test_cases:
                        if testrail_client:
                            testrail_client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=4,
                                                            msg='Cannot reach AP after upgrade to check CLI - re-test required')
                    continue

            time.sleep(30)
        else:
            print("ERROR:  Cloud did not report firmware upgrade within expiration time.")

        if not (sdk_ok and cli_ok):
            return False  # Cannot talk to AP/Cloud, cannot make intelligent decision on pass/fail

        # Check status
        if cloud_ap_fw == ap_image and ap_cli_fw == ap_image:
            print("CloudSDK and AP CLI both show upgrade success, passing upgrade test case")
            if test_cases:
                if testrail_client:
                    testrail_client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=1,
                                                    msg='Upgrade to ' + ap_image + ' successful')
                    testrail_client.update_testrail(case_id=test_id_cloud, run_id=rid, status_id=1,
                                                    msg='CLOUDSDK reporting correct firmware version.')
                if report_data:
                    report_data['tests'][key][test_id_cli] = "passed"
                    report_data['tests'][key][test_id_cloud] = "passed"
                    print(report_data['tests'][key])
            return True

        elif cloud_ap_fw != ap_image and ap_cli_fw == ap_image:
            print("AP CLI shows upgrade success - CloudSDK reporting error!")
            ##Raise CloudSDK error but continue testing
            if test_cases:
                if testrail_client:
                    testrail_client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=1,
                                                    msg='Upgrade to ' + ap_image + ' successful.')
                    testrail_client.update_testrail(case_id=test_id_cloud, run_id=rid, status_id=5,
                                                    msg='CLOUDSDK reporting incorrect firmware version.')
                if report_data:
                    report_data['tests'][key][test_id_cli] = "passed"
                    report_data['tests'][key][test_id_cloud] = "failed"
                    print(report_data['tests'][key])
            return True

        elif cloud_ap_fw == ap_image and ap_cli_fw != ap_image:
            print("AP CLI shows upgrade failed - CloudSDK reporting error!")
            # Testrail TC fail
            if test_cases:
                if testrail_client:
                    testrail_client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=5,
                                                    msg='AP failed to download or apply new FW. Upgrade to ' + ap_image + ' Failed')
                    testrail_client.update_testrail(case_id=test_id_cloud, run_id=rid, status_id=5,
                                                    msg='CLOUDSDK reporting incorrect firmware version.')
                if report_data:
                    report_data['tests'][key][test_id_cli] = "failed"
                    report_data['tests'][key][test_id_cloud] = "failed"
                    print(report_data['tests'][key])
            return False

        elif cloud_ap_fw != ap_image and ap_cli_fw != ap_image:
            print("Upgrade Failed! Confirmed on CloudSDK and AP CLI. Upgrade test case failed.")
            ##fail TR testcase and exit
            if test_cases:
                if testrail_client:
                    testrail_client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=5,
                                                    msg='AP failed to download or apply new FW. Upgrade to ' + ap_image + ' Failed')
                if report_data:
                    report_data['tests'][key][test_id_cli] = "failed"
                    print(report_data['tests'][key])
            return False

        else:
            print("Unable to determine upgrade status. Skipping AP variant")
            # update TR testcase as error
            if test_cases:
                if testrail_client:
                    testrail_client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=4,
                                                    msg='Cannot determine upgrade status - re-test required')
                if report_data:
                    report_data['tests'][key][test_id_cli] = "error"
                    print(report_data['tests'][key])
            return False

    def ap_firmware(self, customer_id, equipment_id, cloudSDK_url, bearer):
        equip_fw_url = cloudSDK_url + "/portal/status/forEquipment?customerId=" + customer_id + "&equipmentId=" + equipment_id
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        status_response = requests.request("GET", equip_fw_url, headers=headers, data=payload)
        self.check_response("GET", status_response, headers, payload, equip_fw_url)
        status_code = status_response.status_code
        if status_code == 200:
            status_data = status_response.json()
            # print(status_data)
            current_ap_fw = status_data[2]['details']['reportedSwVersion']
            return current_ap_fw
        else:
            return ("ERROR")

    def CloudSDK_images(self, apModel, cloudSDK_url, bearer):
        if apModel and apModel != "None":
            getFW_url = cloudSDK_url + "/portal/firmware/version/byEquipmentType?equipmentType=AP&modelId=" + apModel
        else:
            getFW_url = cloudSDK_url + "/portal/firmware/version/byEquipmentType?equipmentType=AP"
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("GET", getFW_url, headers=headers, data=payload)
        self.check_response("GET", response, headers, payload, getFW_url)
        ap_fw_details = response.json()
        ###return ap_fw_details
        fwlist = []
        for version in ap_fw_details:
            fwlist.append(version.get('versionName'))
        return (fwlist)
        # fw_versionNames = ap_fw_details[0]['versionName']
        # return fw_versionNames

    def firwmare_upload(self, commit, apModel, latest_image, fw_url, cloudSDK_url, bearer):
        fw_upload_url = cloudSDK_url + "/portal/firmware/version"
        payload = "{\n  \"model_type\": \"FirmwareVersion\",\n  \"id\": 0,\n  \"equipmentType\": \"AP\",\n  \"modelId\": \"" + apModel + "\",\n  \"versionName\": \"" + latest_image + "\",\n  \"description\": \"\",\n  \"filename\": \"" + fw_url + "\",\n  \"commit\": \"" + commit + "\",\n  \"validationMethod\": \"MD5_CHECKSUM\",\n  \"validationCode\": \"19494befa87eb6bb90a64fd515634263\",\n  \"releaseDate\": 1596192028877,\n  \"createdTimestamp\": 0,\n  \"lastModifiedTimestamp\": 0\n}\n\n"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", fw_upload_url, headers=headers, data=payload)
        self.check_response("POST", response, headers, payload, fw_upload_url)
        # print(response)
        upload_result = response.json()
        return (upload_result)

    def get_firmware_id(self, latest_ap_image, cloudSDK_url, bearer):
        # print(latest_ap_image)
        fw_id_url = cloudSDK_url + "/portal/firmware/version/byName?firmwareVersionName=" + latest_ap_image

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("GET", fw_id_url, headers=headers, data=payload)
        self.check_response("GET", response, headers, payload, fw_id_url)
        fw_data = response.json()
        latest_fw_id = fw_data['id']
        return latest_fw_id

    def get_paged_url(self, bearer, url_base):
        url = url_base

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        rv = []
        req = 0
        while True:
            print("Request %i: in get-paged-url, url: %s" % (req, url))
            response = requests.request("GET", url, headers=headers, data=payload)
            self.check_response("GET", response, headers, payload, url)
            rjson = response.json()
            rv.append(rjson)
            if not 'context' in rjson:
                print(json.dumps(rjson, indent=4, sort_keys=True))
                break
            if rjson['context']['lastPage']:
                break
            context_str = json.dumps(rjson['context'])
            # print("context-str: %s"%(context_str))
            url = url_base + "&paginationContext=" + urllib.parse.quote(context_str)
            req = req + 1
            # print("Profile, reading another page, context:")
            # print(rjson['context'])
            # print("url: %s"%(fw_id_url))

        return rv

    def get_url(self, bearer, url):
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        print("Get-url, url: %s" % (url))
        response = requests.request("GET", url, headers=headers, data=payload)
        self.check_response("GET", response, headers, payload, url)
        return response.json()

    def get_customer_profiles(self, cloudSDK_url, bearer, customer_id, object_id):
        if object_id != None:
            url_base = cloudSDK_url + "/portal/profile" + "?profileId=" + object_id
            return [self.get_url(bearer, url_base)]
        else:
            url_base = cloudSDK_url + "/portal/profile/forCustomer" + "?customerId=" + customer_id
            return self.get_paged_url(bearer, url_base)

    def ping(self, cloudSDK_url, bearer):
        url_base = cloudSDK_url + "/ping"
        return [self.get_url(bearer, url_base)]

    # This is querys all and filters locally. Maybe there is better way to get cloud to
    # do the filtering?
    def get_customer_profile_by_name(self, cloudSDK_url, bearer, customer_id, name):
        rv = self.get_customer_profiles(cloudSDK_url, bearer, customer_id, None)
        for page in rv:
            for e in page['items']:
                prof_id = str(e['id'])
                prof_model_type = e['model_type']
                prof_type = e['profileType']
                prof_name = e['name']
                print("looking for profile: %s  checking prof-id: %s  model-type: %s  type: %s  name: %s" % (
                name, prof_id, prof_model_type, prof_type, prof_name))
                if name == prof_name:
                    return e
        return None

    def delete_customer_profile(self, cloudSDK_url, bearer, profile_id):
        url = cloudSDK_url + '/portal/profile/?profileId=' + profile_id
        print("Deleting customer profile with url: " + url)
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("DELETE", url, headers=headers, data=payload)
        self.check_response("DELETE", response, headers, payload, url)
        return (response)

    def delete_equipment(self, cloudSDK_url, bearer, eq_id):
        url = cloudSDK_url + '/portal/equipment/?equipmentId=' + eq_id
        print("Deleting equipment with url: " + url)
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("DELETE", url, headers=headers, data=payload)
        self.check_response("DELETE", response, headers, payload, url)
        return (response)

    def get_customer_locations(self, cloudSDK_url, bearer, customer_id):
        url_base = cloudSDK_url + "/portal/location/forCustomer" + "?customerId=" + customer_id
        return self.get_paged_url(bearer, url_base)

    def get_customer_equipment(self, customer_id):
        url = self.base_url + "/portal/equipment/forCustomer" + "?customerId=" + customer_id
        return self.get_paged_url(self.bearer, url)

    def get_customer_portal_users(self, cloudSDK_url, bearer, customer_id):
        url_base = cloudSDK_url + "/portal/portalUser/forCustomer" + "?customerId=" + customer_id
        return self.get_paged_url(bearer, url_base)

    def get_customer_status(self, cloudSDK_url, bearer, customer_id):
        url_base = cloudSDK_url + "/portal/status/forCustomer" + "?customerId=" + customer_id
        return self.get_paged_url(bearer, url_base)

    def get_customer_client_sessions(self, cloudSDK_url, bearer, customer_id):
        url_base = cloudSDK_url + "/portal/client/session/forCustomer" + "?customerId=" + customer_id
        return self.get_paged_url(bearer, url_base)

    def get_customer_clients(self, cloudSDK_url, bearer, customer_id):
        url_base = cloudSDK_url + "/portal/client/forCustomer" + "?customerId=" + customer_id
        return self.get_paged_url(bearer, url_base)

    def get_customer_alarms(self, cloudSDK_url, bearer, customer_id):
        url_base = cloudSDK_url + "/portal/alarm/forCustomer" + "?customerId=" + customer_id
        return self.get_paged_url(bearer, url_base)

    def get_customer_service_metrics(self, cloudSDK_url, bearer, customer_id, fromTime, toTime):
        url_base = cloudSDK_url + "/portal/serviceMetric/forCustomer" + "?customerId=" + customer_id + "&fromTime=" + fromTime + "&toTime=" + toTime
        return self.get_paged_url(bearer, url_base)

    def get_customer_system_events(self, cloudSDK_url, bearer, customer_id, fromTime, toTime):
        url_base = cloudSDK_url + "/portal/systemEvent/forCustomer" + "?customerId=" + customer_id + "&fromTime=" + fromTime + "&toTime=" + toTime
        return self.get_paged_url(bearer, url_base)

    def get_customer(self, cloudSDK_url, bearer, customer_id):
        fw_id_url = cloudSDK_url + "/portal/customer" + "?customerId=" + customer_id

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("GET", fw_id_url, headers=headers, data=payload)
        self.check_response("GET", response, headers, payload, fw_id_url)
        return response.json()

    def delete_firmware(self, fw_id, cloudSDK_url, bearer):
        url = cloudSDK_url + '/portal/firmware/version?firmwareVersionId=' + fw_id
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("DELETE", url, headers=headers, data=payload)
        self.check_response("DELETE", response, headers, payload, url)
        return (response)

    def update_firmware(self, equipment_id, latest_firmware_id, cloudSDK_url, bearer):
        url = cloudSDK_url + "/portal/equipmentGateway/requestFirmwareUpdate?equipmentId=" + equipment_id + "&firmwareVersionId=" + latest_firmware_id

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.check_response("POST", response, headers, payload, url)
        # print(response.text)
        return response.json()

    # This one is not yet tested, coded from spec, could have bugs.
    def ap_reboot(self, equipment_id, cloudSDK_url, bearer):
        url = cloudSDK_url + "/portal/equipmentGateway/requestApReboot?equipmentId=" + equipment_id

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.check_response("POST", response, headers, payload, url)
        # print(response.text)
        return response.json()

    # This one is not yet tested, coded from spec, could have bugs.
    def ap_switch_sw_bank(self, equipment_id, cloudSDK_url, bearer):
        url = cloudSDK_url + "/portal/equipmentGateway/requestApSwitchSoftwareBank?equipmentId=" + equipment_id

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.check_response("POST", response, headers, payload, url)
        # print(response.text)
        return response.json()

    # This one is not yet tested, coded from spec, could have bugs.
    def ap_factory_reset(self, equipment_id, cloudSDK_url, bearer):
        url = cloudSDK_url + "/portal/equipmentGateway/requestApFactoryReset?equipmentId=" + equipment_id

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.check_response("POST", response, headers, payload, url)
        # print(response.text)
        return response.json()

    # This one is not yet tested, coded from spec, could have bugs.
    def ap_channel_change(self, equipment_id, cloudSDK_url, bearer):
        url = cloudSDK_url + "/portal/equipmentGateway/requestChannelChange?equipmentId=" + equipment_id

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.check_response("POST", response, headers, payload, url)
        # print(response.text)
        return response.json()

    def set_ap_profile(self, equipment_id, test_profile_id):
        ###Get AP Info
        url = self.base_url + "/portal/equipment?equipmentId=" + equipment_id
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + self.bearer
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        self.check_response("GET", response, headers, payload, url)
        print(response)

        ###Add Lab Profile ID to Equipment
        equipment_info = response.json()
        # print(equipment_info)
        equipment_info["profileId"] = test_profile_id
        print(equipment_info)

        ###Update AP Info with Required Profile ID
        url = self.base_url + "/portal/equipment"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.bearer
        }

        response = requests.request("PUT", url, headers=headers, data=json.dumps(equipment_info))
        self.check_response("PUT", response, headers, payload, url)
        print(response)

    def get_cloudsdk_version(self, cloudSDK_url, bearer):
        # print(latest_ap_image)
        url = cloudSDK_url + "/ping"

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        self.check_response("GET", response, headers, payload, url)
        cloud_sdk_version = response.json()
        return cloud_sdk_version

    def create_ap_profile(self, cloudSDK_url, bearer, customer_id, template, name, child_profiles):
        # TODO:  specify default ap profile.
        profile = self.get_customer_profile_by_name(cloudSDK_url, bearer, customer_id, template)

        profile["name"] = name
        profile["childProfileIds"] = child_profiles

        url = cloudSDK_url + "/portal/profile"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }

        data_str = json.dumps(profile)
        print("Creating new ap-profile, data: %s" % (data_str))
        response = requests.request("POST", url, headers=headers, data=data_str)
        self.check_response("POST", response, headers, data_str, url)
        ap_profile = response.json()
        print("New AP profile: ", ap_profile)
        ap_profile_id = ap_profile['id']
        return ap_profile_id

    def create_or_update_ap_profile(self, cloudSDK_url, bearer, customer_id, template, name, child_profiles):
        profile = self.get_customer_profile_by_name(cloudSDK_url, bearer, customer_id, name)
        if profile == None:
            return self.create_ap_profile(cloudSDK_url, bearer, customer_id, template, name, child_profiles)

        if self.verbose:
            print("AP Profile before modification:")
            print(json.dumps(profile, indent=4, sort_keys=True))

        profile["name"] = name
        profile["childProfileIds"] = child_profiles

        url = cloudSDK_url + "/portal/profile"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }

        data_str = json.dumps(profile)
        print("Updating ap-profile, data: %s" % (data_str))
        response = requests.request("PUT", url, headers=headers, data=data_str)
        self.check_response("PUT", response, headers, data_str, url)
        print(response)

        if self.verbose:
            p2 = self.get_customer_profile_by_name(cloudSDK_url, bearer, customer_id, name)
            print("AP Profile: %s after update:" % (name))
            print(json.dumps(p2, indent=4, sort_keys=True))

        return profile['id']

    def create_ssid_profile(self, cloudSDK_url, bearer, customer_id, template, name, ssid, passkey, radius, security,
                            mode, vlan, radios):
        print("create-ssid-profile, template: %s" % (template))
        profile = self.get_customer_profile_by_name(cloudSDK_url, bearer, customer_id, template)

        profile['name'] = name
        profile['details']['ssid'] = ssid
        profile['details']['keyStr'] = passkey
        profile['details']['radiusServiceName'] = radius
        profile['details']['secureMode'] = security
        profile['details']['forwardMode'] = mode
        profile['details']['vlanId'] = vlan
        profile['details']['appliedRadios'] = radios

        url = cloudSDK_url + "/portal/profile"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }
        data_str = json.dumps(profile)
        response = requests.request("POST", url, headers=headers, data=data_str)
        self.check_response("POST", response, headers, data_str, url)
        ssid_profile = response.json()
        return ssid_profile['id']

    def create_or_update_ssid_profile(self, cloudSDK_url, bearer, customer_id, template, name,
                                      ssid, passkey, radius, security, mode, vlan, radios):
        # First, see if profile of this name already exists.
        profile = self.get_customer_profile_by_name(cloudSDK_url, bearer, customer_id, name)
        if profile == None:
            # create one then
            return self.create_ssid_profile(cloudSDK_url, bearer, customer_id, template, name,
                                            ssid, passkey, radius, security, mode, vlan, radios)

        # Update then.
        print("Update existing ssid profile, name: %s" % (name))
        profile['name'] = name
        profile['details']['ssid'] = ssid
        profile['details']['keyStr'] = passkey
        profile['details']['radiusServiceName'] = radius
        profile['details']['secureMode'] = security
        profile['details']['forwardMode'] = mode
        profile['details']['vlanId'] = vlan
        profile['details']['appliedRadios'] = radios

        url = cloudSDK_url + "/portal/profile"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }
        data_str = json.dumps(profile)
        response = requests.request("PUT", url, headers=headers, data=data_str)
        self.check_response("PUT", response, headers, data_str, url)
        return profile['id']

    # General usage:  get the default profile, modify it accordingly, pass it back to here
    # Not tested yet.
    def create_rf_profile(self, cloudSDK_url, bearer, customer_id, template, name, new_prof):
        print("create-rf-profile, template: %s" % (template))

        url = cloudSDK_url + "/portal/profile"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }
        data_str = json.dumps(profile)
        response = requests.request("POST", url, headers=headers, data=data_str)
        self.check_response("POST", response, headers, data_str, url)
        ssid_profile = response.json()
        return ssid_profile['id']

    # Not tested yet.
    def create_or_update_rf_profile(self, cloudSDK_url, bearer, customer_id, template, name,
                                    new_prof):
        # First, see if profile of this name already exists.
        profile = self.get_customer_profile_by_name(cloudSDK_url, bearer, customer_id, name)
        if profile == None:
            # create one then
            return self.create_rf_profile(cloudSDK_url, bearer, customer_id, template, name, new_prof)

        # Update then.
        print("Update existing ssid profile, name: %s" % (name))

        url = cloudSDK_url + "/portal/profile"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }
        data_str = json.dumps(new_profile)
        response = requests.request("PUT", url, headers=headers, data=data_str)
        self.check_response("PUT", response, headers, data_str, url)
        return profile['id']

    def create_radius_profile(self, cloudSDK_url, bearer, customer_id, template, name, subnet_name, subnet, subnet_mask,
                              region, server_name, server_ip, secret, auth_port):
        print("Create-radius-profile called, template: %s" % (template))
        profile = self.get_customer_profile_by_name(cloudSDK_url, bearer, customer_id, template)

        profile['name'] = name

        subnet_config = profile['details']['subnetConfiguration']
        old_subnet_name = list(subnet_config.keys())[0]
        subnet_config[subnet_name] = subnet_config.pop(old_subnet_name)
        profile['details']['subnetConfiguration'][subnet_name]['subnetAddress'] = subnet
        profile['details']['subnetConfiguration'][subnet_name]['subnetCidrPrefix'] = subnet_mask
        profile['details']['subnetConfiguration'][subnet_name]['subnetName'] = subnet_name

        region_map = profile['details']['serviceRegionMap']
        old_region = list(region_map.keys())[0]
        region_map[region] = region_map.pop(old_region)
        profile['details']['serviceRegionName'] = region
        profile['details']['subnetConfiguration'][subnet_name]['serviceRegionName'] = region
        profile['details']['serviceRegionMap'][region]['regionName'] = region

        server_map = profile['details']['serviceRegionMap'][region]['serverMap']
        old_server_name = list(server_map.keys())[0]
        server_map[server_name] = server_map.pop(old_server_name)
        profile['details']['serviceRegionMap'][region]['serverMap'][server_name][0]['ipAddress'] = server_ip
        profile['details']['serviceRegionMap'][region]['serverMap'][server_name][0]['secret'] = secret
        profile['details']['serviceRegionMap'][region]['serverMap'][server_name][0]['authPort'] = auth_port

        url = cloudSDK_url + "/portal/profile"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }

        data_str = json.dumps(profile)
        print("Sending json to create radius: %s" % (data_str))
        response = requests.request("POST", url, headers=headers, data=data_str)
        self.check_response("POST", response, headers, data_str, url)
        radius_profile = response.json()
        print(radius_profile)
        radius_profile_id = radius_profile['id']
        return radius_profile_id

    def create_or_update_radius_profile(self, cloudSDK_url, bearer, customer_id, template, name, subnet_name, subnet,
                                        subnet_mask,
                                        region, server_name, server_ip, secret, auth_port):
        null = None
        profile = {"model_type": "Profile", "id": 129, "customerId": "2", "profileType": "radius", "name": "Automation_Radius_Nightly-1553", "details": {"model_type": "RadiusProfile", "primaryRadiusAuthServer": {"model_type": "RadiusServer", "ipAddress": "18.189.25.141", "secret": "testing123", "port": 1812, "timeout": 5}, "secondaryRadiusAuthServer": null, "primaryRadiusAccountingServer": null, "secondaryRadiusAccountingServer": null, "profileType": "radius"}, "createdTimestamp": 1602263176599, "lastModifiedTimestamp": 1611708334061, "childProfileIds": []}
        profile['name'] = name
        profile['customerId'] = customer_id
        profile['details']["primaryRadiusAuthServer"]['ipAddress'] = server_ip
        profile['details']["primaryRadiusAuthServer"]['secret'] = secret
        profile['details']["primaryRadiusAuthServer"]['port'] = auth_port

        url = cloudSDK_url + "/portal/profile"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }

        json_profile_data = json.dumps(profile).encode("utf-8")
        response = requests.request("POST", url, headers=headers, data=json_profile_data)
        radius_profile = response.json()
        radius_profile_id = radius_profile['id']
        return radius_profile_id


# Library for creating AP Profiles
class CreateAPProfiles:

    def __init__(self,
                 command_line_args,
                 cloud=None,
                 cloud_type="v1",
                 client=None,
                 fw_model=None
                 ):

        self.rid = None
        self.fiveG_wpa2 = None
        self.fiveG_wpa = None
        self.fiveG_eap = None
        self.twoFourG_wpa2 = None
        self.twoFourG_wpa = None
        self.twoFourG_eap = None
        self.command_line_args = command_line_args
        self.radius_profile = None
        self.radius_name = None
        self.cloud = cloud
        self.client = client
        self.cloud_type = cloud_type
        self.customer_id = command_line_args.customer_id
        self.ap_cli_info = ssh_cli_active_fw(self.command_line_args)
        if self.cloud == None:
            print("cloud cannot be None")
            exit()
        self.ap_cli_fw = self.ap_cli_info['active_fw']
        self.bearer = self.cloud.get_bearer(self.command_line_args.sdk_base_url, self.cloud_type)
        self.radius_info = {

            "name": "Lab-RADIUS",
            "subnet_name": "Lab",
            "subnet": "8.189.25.141",
            "subnet_mask": 16,
            "region": "Toronto",
            "server_name": "Lab-RADIUS",
            "server_ip": "18.189.25.141",
            "secret": "testing123",
            "auth_port": 1812
        }
        self.ap_models = ["ec420", "ea8300", "ecw5211", "ecw5410"]
        self.fw_model = fw_model
        self.report_data = {}
        self.report_data['tests'] = dict.fromkeys(self.ap_models, "")
        self.test_cases = {
            "radius_profile": None,

            "ssid_5g_eap_bridge": None,
            "ssid_5g_wpa2_bridge": None,
            "ssid_5g_wpa_bridge": None,
            "ssid_2g_eap_bridge": None,
            "ssid_2g_wpa2_bridge": None,
            "ssid_2g_wpa_bridge": None,

            "ssid_5g_eap_nat": None,
            "ssid_5g_wpa2_nat": None,
            "ssid_5g_wpa_nat": None,
            "ssid_2g_eap_nat": None,
            "ssid_2g_wpa2_nat": None,
            "ssid_2g_wpa_nat": None,

            "ap_bridge": None,
            "ap_nat": None,
            "ap_vlan": None,

            "bridge_vifc": None,
            "bridge_vifs": None,

            "nat_vifc": None,
            "nat_vifs": None,

            "vlan_vifc": None,
            "vlan_vifs": None
        }
        self.profile_data, self.prof_names, self.prof_names_eap = self.create_profile_data(self.command_line_args,
                                                                                           self.fw_model)
        self.ssid_data, self.psk_data = self.create_ssid_data(self.command_line_args, self.fw_model)

    def create_profile_data(self, args, fw_model):
        profile_data = {
            "5g": {"eap":
                {
                    "bridge": "%s-%s-%s" % (args.testbed, fw_model, "5G_EAP"),
                    "nat": "%s-%s-%s" % (args.testbed, fw_model, "5G_EAP_NAT"),
                    "vlan": "%s-%s-%s" % (args.testbed, fw_model, "5G_EAP_VLAN")
                },
                "wpa":
                    {
                        "bridge": "%s-%s-%s" % (args.testbed, fw_model, "5G_WPA"),
                        "nat": "%s-%s-%s" % (args.testbed, fw_model, "5G_WPA_NAT"),
                        "vlan": "%s-%s-%s" % (args.testbed, fw_model, "5G_WPA_VLAN")
                    },
                "wpa2":
                    {
                        "bridge": "%s-%s-%s" % (args.testbed, fw_model, "5G_WPA2"),
                        "nat": "%s-%s-%s" % (args.testbed, fw_model, "5G_WPA2_NAT"),
                        "vlan": "%s-%s-%s" % (args.testbed, fw_model, "5G_WPA2_VLAN")
                    }
            },
            "2g": {"eap":
                {
                    "bridge": "%s-%s-%s" % (args.testbed, fw_model, "2G_EAP"),
                    "nat": "%s-%s-%s" % (args.testbed, fw_model, "2G_EAP_NAT"),
                    "vlan": "%s-%s-%s" % (args.testbed, fw_model, "2G_EAP_VLAN")
                },
                "wpa":
                    {
                        "bridge": "%s-%s-%s" % (args.testbed, fw_model, "2G_WPA"),
                        "nat": "%s-%s-%s" % (args.testbed, fw_model, "2G_WPA_NAT"),
                        "vlan": "%s-%s-%s" % (args.testbed, fw_model, "2G_WPA_VLAN")
                    },
                "wpa2":
                    {
                        "bridge": "%s-%s-%s" % (args.testbed, fw_model, "2G_WPA2"),
                        "nat": "%s-%s-%s" % (args.testbed, fw_model, "2G_WPA2_NAT"),
                        "vlan": "%s-%s-%s" % (args.testbed, fw_model, "2G_WPA2_VLAN")
                    }
            }
        }
        prof_names = [profile_data["5g"]["wpa2"]["bridge"], profile_data["5g"]["wpa"]["bridge"],
                      profile_data["2g"]["wpa2"]["bridge"], profile_data["2g"]["wpa"]["bridge"],
                      profile_data["5g"]["wpa2"]["nat"], profile_data["5g"]["wpa"]["nat"],
                      profile_data["2g"]["wpa2"]["nat"], profile_data["2g"]["wpa"]["nat"],
                      profile_data["5g"]["wpa2"]["vlan"], profile_data["5g"]["wpa"]["vlan"],
                      profile_data["2g"]["wpa2"]["vlan"], profile_data["2g"]["wpa"]["vlan"]]

        prof_names_eap = [profile_data["5g"]["eap"]["bridge"], profile_data["2g"]["eap"]["bridge"],
                          profile_data["5g"]["eap"]["nat"], profile_data["2g"]["eap"]["nat"],
                          profile_data["5g"]["eap"]["vlan"], profile_data["2g"]["eap"]["vlan"]]

        return profile_data, prof_names, prof_names_eap

    def create_ssid_data(self, args, fw_model):
        ssid_data = self.profile_data.copy()

        psk_data = {
            "5g":
                {
                    "wpa":
                        {
                            "bridge": "%s-%s" % (fw_model, "5G_WPA"),
                            "nat": "%s-%s" % (fw_model, "5G_WPA_NAT"),
                            "vlan": "%s-%s" % (fw_model, "5G_WPA_VLAN")
                        },
                    "wpa2":
                        {
                            "bridge": "%s-%s" % (fw_model, "5G_WPA2"),
                            "nat": "%s-%s" % (fw_model, "5G_WPA2_NAT"),
                            "vlan": "%s-%s" % (fw_model, "5G_WPA2_VLAN")
                        }
                },
            "2g":
                {
                    "wpa":
                        {
                            "bridge": "%s-%s" % (fw_model, "2G_WPA"),
                            "nat": "%s-%s" % (fw_model, "2G_WPA_NAT"),
                            "vlan": "%s-%s" % (fw_model, "2G_WPA_VLAN")
                        },
                    "wpa2":
                        {
                            "bridge": "%s-%s" % (fw_model, "2G_WPA2"),
                            "nat": "%s-%s" % (fw_model, "2G_WPA2_NAT"),
                            "vlan": "%s-%s" % (fw_model, "2G_WPA2_VLAN")
                        }
                }

        }

        return ssid_data, psk_data

    def set_ssid_psk_data(self,
                          ssid_2g_wpa=None,
                          ssid_5g_wpa=None,
                          psk_2g_wpa=None,
                          psk_5g_wpa=None,
                          ssid_2g_wpa2=None,
                          ssid_5g_wpa2=None,
                          psk_2g_wpa2=None,
                          psk_5g_wpa2=None):
        if psk_5g_wpa2 is not None:
            self.psk_data["5g"]["wpa2"]["bridge"] = psk_5g_wpa2
            self.psk_data["5g"]["wpa2"]["nat"] = psk_5g_wpa2
            self.psk_data["5g"]["wpa2"]["vlan"] = psk_5g_wpa2
        if psk_5g_wpa is not None:
            self.psk_data["5g"]["wpa"]["bridge"] = psk_5g_wpa
            self.psk_data["5g"]["wpa"]["nat"] = psk_5g_wpa
            self.psk_data["5g"]["wpa"]["vlan"] = psk_5g_wpa
        if psk_2g_wpa2 is not None:
            self.psk_data["2g"]["wpa2"]["bridge"] = psk_2g_wpa2
            self.psk_data["2g"]["wpa2"]["nat"] = psk_2g_wpa2
            self.psk_data["2g"]["wpa2"]["vlan"] = psk_2g_wpa2
        if psk_2g_wpa is not None:
            self.psk_data["2g"]["wpa"]["bridge"] = psk_2g_wpa
            self.psk_data["2g"]["wpa"]["nat"] = psk_2g_wpa
            self.psk_data["2g"]["wpa"]["nat"] = psk_2g_wpa
        if ssid_5g_wpa2 is not None:
            self.ssid_data["5g"]["wpa2"]["bridge"] = ssid_5g_wpa2
            self.ssid_data["5g"]["wpa2"]["nat"] = ssid_5g_wpa2
            self.ssid_data["5g"]["wpa2"]["vlan"] = ssid_5g_wpa2
        if ssid_5g_wpa is not None:
            self.ssid_data["5g"]["wpa"]["bridge"] = ssid_5g_wpa
            self.ssid_data["5g"]["wpa"]["nat"] = ssid_5g_wpa
            self.ssid_data["5g"]["wpa"]["vlan"] = ssid_5g_wpa
        if ssid_2g_wpa2 is not None:
            self.ssid_data["2g"]["wpa2"]["bridge"] = ssid_2g_wpa2
            self.ssid_data["2g"]["wpa2"]["nat"] = ssid_2g_wpa2
            self.ssid_data["2g"]["wpa2"]["vlan"] = ssid_2g_wpa2
        if ssid_2g_wpa is not None:
            self.ssid_data["2g"]["wpa"]["bridge"] = ssid_2g_wpa
            self.ssid_data["2g"]["wpa"]["nat"] = ssid_2g_wpa
            self.ssid_data["2g"]["wpa"]["vlan"] = ssid_2g_wpa

    def create_radius_profile(self, radius_name=None, radius_template=None, rid=None, key=None):

        ### Create RADIUS profile - used for all EAP SSIDs
        self.radius_name = radius_name
        self.radius_template = radius_template  # Default radius profile found in cloud-sdk
        self.subnet_name = self.radius_info['subnet_name']
        self.subnet = self.radius_info['subnet']
        self.subnet_mask = self.radius_info['subnet_mask']
        self.region = self.radius_info['region']
        self.server_name = self.radius_info['server_name']
        self.server_ip = self.radius_info['server_ip']
        self.secret = self.radius_info['secret']
        self.auth_port = self.radius_info['auth_port']
        self.rid = rid
        self.key = key
        if self.command_line_args.skip_radius == False:
            try:
                print("Into")
                self.radius_profile = self.cloud.create_or_update_radius_profile(self.command_line_args.sdk_base_url,
                                                                                 self.bearer, self.customer_id,
                                                                                 self.radius_template, self.radius_name,
                                                                                 self.subnet_name,
                                                                                 self.subnet,
                                                                                 self.subnet_mask, self.region,
                                                                                 self.server_name, self.server_ip,
                                                                                 self.secret, self.auth_port)
                print("radius profile Id is", self.radius_profile)
                self.client.update_testrail(case_id=self.test_cases["radius_profile"], run_id=self.rid, status_id=1,
                                            msg='RADIUS profile created successfully')
                self.test_cases["radius_profile"] = "passed"
            except Exception as ex:
                print(ex)
                logging.error(logging.traceback.format_exc())
                print("RADIUS Profile Create Error, will skip radius profile.")
                # Set backup profile ID so test can continue
                self.radius_profile = None
                self.radius_name = None
                self.server_name = "Lab-RADIUS"
                self.client.update_testrail(case_id=self.test_cases["radius_profile"], run_id=self.rid, status_id=5,
                                            msg='Failed to create RADIUS profile')
                self.test_cases["radius_profile"] = "failed"

    def create_ssid_profiles(self, ssid_template=None, skip_wpa2=False, skip_wpa=False, skip_eap=False, mode="bridge"):

        self.ssid_template = ssid_template
        self.mode = mode
        self.fiveG_eap = None
        self.twoFourG_eap = None
        self.fiveG_wpa2 = None
        self.twoFourG_wpa2 = None
        self.fiveG_wpa = None
        self.twoFourG_wpa = None

        # 5G SSID's
        print("CreateAPProfile::create_ssid_profile, skip-wpa: ", skip_wpa, " skip-wpa2: ", skip_wpa2, " skip-eap: ",
              skip_eap)

        if not skip_eap:
            # 5G eap
            try:
                self.fiveG_eap = self.cloud.create_or_update_ssid_profile(self.command_line_args.sdk_base_url,
                                                                          self.bearer, self.customer_id,
                                                                          self.ssid_template,
                                                                          self.profile_data['5g']['eap'][self.mode],
                                                                          self.ssid_data['5g']['eap'][self.mode],
                                                                          None,
                                                                          self.radius_name,
                                                                          "wpa2OnlyRadius", mode.upper(), 1,
                                                                          ["is5GHzU", "is5GHz", "is5GHzL"])
                print("5G EAP SSID created successfully - " + mode + " mode")
                self.client.update_testrail(case_id=self.test_cases["ssid_5g_eap_" + mode],
                                            run_id=self.rid,
                                            status_id=1,
                                            msg='5G EAP SSID created successfully - ' + mode + ' mode')
                self.test_cases["ssid_5g_eap_" + mode] = "passed"
            except Exception as ex:
                print(ex)
                logging.error(logging.traceback.format_exc())
                self.fiveG_eap = None
                print("5G EAP SSID create failed - " + mode + " mode")
                self.client.update_testrail(case_id=self.test_cases["ssid_5g_eap_" + mode], run_id=self.rid,
                                            status_id=5,
                                            msg='5G EAP SSID create failed - ' + mode + ' mode')
                self.test_cases["ssid_5g_eap_" + mode] = "failed"

            # 2.4G eap
            try:
                self.twoFourG_eap = self.cloud.create_or_update_ssid_profile(self.command_line_args.sdk_base_url,
                                                                             self.bearer, self.customer_id,
                                                                             self.ssid_template,
                                                                             self.profile_data['2g']['eap'][self.mode],
                                                                             self.ssid_data['2g']['eap'][self.mode],
                                                                             None,
                                                                             self.radius_name, "wpa2OnlyRadius",
                                                                             mode.upper(), 1,
                                                                             ["is2dot4GHz"])
                print("2.4G EAP SSID created successfully - " + mode + " mode")
                self.client.update_testrail(case_id=self.test_cases["ssid_5g_eap_" + mode], run_id=self.rid,
                                            status_id=1,
                                            msg='2.4G EAP SSID created successfully - ' + mode + ' mode')
                self.test_cases["ssid_5g_eap_" + mode] = "passed"
            except Exception as ex:
                print(ex)
                logging.error(logging.traceback.format_exc())
                self.twoFourG_eap = None
                print("2.4G EAP SSID create failed - bridge mode")
                self.client.update_testrail(case_id=self.test_cases["ssid_5g_eap_" + mode], run_id=self.rid,
                                            status_id=5,
                                            msg='2.4G EAP SSID create failed - bridge mode')
                self.test_cases["ssid_5g_eap_" + mode] = "failed"

        if not skip_wpa2:
            # 5g wpa2
            try:
                self.fiveG_wpa2 = self.cloud.create_or_update_ssid_profile(self.command_line_args.sdk_base_url,
                                                                           self.bearer, self.customer_id,
                                                                           self.ssid_template,
                                                                           self.profile_data['5g']['wpa2'][self.mode],
                                                                           self.ssid_data['5g']['wpa2'][self.mode],
                                                                           self.psk_data['5g']['wpa2'][self.mode],
                                                                           "Radius-Accounting-Profile", "wpa2OnlyPSK",
                                                                           mode.upper(), 1,
                                                                           ["is5GHzU", "is5GHz", "is5GHzL"])
                print("5G WPA2 SSID created successfully - " + mode + " mode")
                self.client.update_testrail(case_id=self.test_cases["ssid_5g_wpa2_" + mode], run_id=self.rid,
                                            status_id=1,
                                            msg='5G WPA2 SSID created successfully - ' + mode + ' mode')
                self.test_cases["ssid_5g_wpa2_" + mode] = "passed"
            except Exception as ex:
                print(ex)
                logging.error(logging.traceback.format_exc())
                self.fiveG_wpa2 = None
                print("5G WPA2 SSID create failed - " + mode + " mode")
                self.client.update_testrail(case_id=self.test_cases["ssid_5g_wpa2_" + mode], run_id=self.rid,
                                            status_id=5,
                                            msg='5G WPA2 SSID create failed - ' + mode + ' mode')
                self.test_cases["ssid_5g_wpa2_" + mode] = "failed"

            # 2.4G wpa2
            try:
                self.twoFourG_wpa2 = self.cloud.create_or_update_ssid_profile(self.command_line_args.sdk_base_url,
                                                                              self.bearer, self.customer_id,
                                                                              self.ssid_template,
                                                                              self.profile_data['2g']['wpa2'][
                                                                                  self.mode],
                                                                              self.ssid_data['2g']['wpa2'][self.mode],
                                                                              self.psk_data['2g']['wpa2'][self.mode],
                                                                              "Radius-Accounting-Profile",
                                                                              "wpa2OnlyPSK", self.mode.upper(), 1,
                                                                              ["is2dot4GHz"])
                print("2.4G WPA2 SSID created successfully - " + mode + " mode")
                self.client.update_testrail(case_id=self.test_cases["ssid_2g_wpa2_" + mode], run_id=self.rid,
                                            status_id=1,
                                            msg='2.4G WPA2 SSID created successfully - ' + mode + ' mode')
                self.test_cases["ssid_2g_wpa2_" + mode] = "passed"
            except Exception as ex:
                print(ex)
                logging.error(logging.traceback.format_exc())
                self.twoFourG_wpa2 = None
                print("2.4G WPA2 SSID create failed - " + mode + " mode")
                self.client.update_testrail(case_id=self.test_cases["ssid_2g_wpa2_" + mode], run_id=self.rid,
                                            status_id=5,
                                            msg='2.4G WPA2 SSID create failed - ' + mode + ' mode')
                self.test_cases["ssid_2g_wpa2_" + mode] = "failed"

        if not skip_wpa:
            # 5g wpa
            try:
                self.fiveG_wpa = self.cloud.create_or_update_ssid_profile(self.command_line_args.sdk_base_url,
                                                                          self.bearer, self.customer_id,
                                                                          self.ssid_template,
                                                                          self.profile_data['5g']['wpa'][self.mode],
                                                                          self.ssid_data['5g']['wpa'][self.mode],
                                                                          self.psk_data['5g']['wpa'][self.mode],
                                                                          "Radius-Accounting-Profile", "wpaPSK",
                                                                          mode.upper(), 1,
                                                                          ["is5GHzU", "is5GHz", "is5GHzL"])
                print("5G WPA SSID created successfully - " + mode + " mode")
                self.client.update_testrail(case_id=self.test_cases["ssid_5g_wpa_" + mode],
                                            run_id=self.rid,
                                            status_id=1,
                                            msg='5G WPA SSID created successfully - ' + mode + ' mode')
                self.test_cases["ssid_5g_wpa_" + mode] = "passed"
            except Exception as ex:
                print(ex)
                logging.error(logging.traceback.format_exc())
                self.fiveG_wpa = None
                print("5G WPA SSID create failed - " + mode + " mode")
                self.client.update_testrail(case_id=self.test_cases["ssid_5g_wpa_" + mode], run_id=self.rid,
                                            status_id=5,
                                            msg='5G WPA SSID create failed - ' + mode + ' mode')
                self.test_cases["ssid_5g_wpa_" + mode] = "failed"

            # 2.4G wpa
            try:
                self.twoFourG_wpa = self.cloud.create_or_update_ssid_profile(self.command_line_args.sdk_base_url,
                                                                             self.bearer, self.customer_id,
                                                                             self.ssid_template,
                                                                             self.profile_data['2g']['wpa'][self.mode],
                                                                             self.ssid_data['2g']['wpa'][self.mode],
                                                                             self.psk_data['2g']['wpa'][self.mode],
                                                                             "Radius-Accounting-Profile", "wpaPSK",
                                                                             mode.upper(), 1,
                                                                             ["is2dot4GHz"])
                print("2.4G WPA SSID created successfully - " + mode + " mode")
                self.client.update_testrail(case_id=self.test_cases["ssid_2g_wpa_" + mode], run_id=self.rid,
                                            status_id=1,
                                            msg='2.4G WPA SSID created successfully - ' + mode + ' mode')
                self.test_cases["ssid_2g_wpa_" + mode] = "passed"
            except Exception as ex:
                print(ex)
                logging.error(logging.traceback.format_exc())
                self.twoFourG_wpa = None
                print("2.4G WPA SSID create failed - " + mode + " mode")
                self.client.update_testrail(case_id=self.test_cases["ssid_2g_wpa_" + mode], run_id=self.rid,
                                            status_id=5,
                                            msg='2.4G WPA SSID create failed - ' + mode + ' mode')
                self.test_cases["ssid_2g_wpa_" + mode] = "failed"

    def create_ap_profile(self, eq_id=None, fw_model=None, mode="bridge"):
        self.ssid_prof_config = []
        self.ssid_config = []
        self.fw_model = fw_model
        self.rfProfileId = lab_ap_info.rf_profile
        self.child_profiles = [self.rfProfileId]
        self.mode = mode

        print("create-ap-bridge-profile:  5G-wpa2: ", self.fiveG_wpa2, " 2g-wpa2: ", self.twoFourG_wpa2)

        if self.fiveG_wpa2:
            self.child_profiles.append(self.fiveG_wpa2)
            self.ssid_prof_config.append(self.profile_data['5g']['wpa2'][self.mode])
            self.ssid_config.append(self.ssid_data['5g']['wpa2'][self.mode])

        if self.twoFourG_wpa2:
            self.child_profiles.append(self.twoFourG_wpa2)
            self.ssid_prof_config.append(self.profile_data['2g']['wpa2'][self.mode])
            self.ssid_config.append(self.ssid_data['2g']['wpa2'][self.mode])

        if self.fiveG_eap:
            self.child_profiles.append(self.fiveG_eap)
            self.ssid_prof_config.append(self.profile_data['5g']['eap'][self.mode])
            self.ssid_config.append(self.ssid_data['5g']['eap'][self.mode])

        if self.twoFourG_eap:
            self.child_profiles.append(self.twoFourG_eap)
            self.ssid_prof_config.append(self.profile_data['2g']['eap'][self.mode])
            self.ssid_config.append(self.ssid_data['2g']['eap'][self.mode])

        if self.fiveG_wpa:
            self.child_profiles.append(self.fiveG_wpa)
            self.ssid_prof_config.append(self.profile_data['5g']['wpa'][self.mode])
            self.ssid_config.append(self.ssid_data['5g']['wpa'][self.mode])

        if self.twoFourG_wpa:
            self.child_profiles.append(self.twoFourG_wpa)
            self.ssid_prof_config.append(self.profile_data['2g']['wpa'][self.mode])
            self.ssid_config.append(self.ssid_data['2g']['wpa'][self.mode])

        if self.radius_profile is not None:
            self.child_profiles.append(self.radius_profile)
            # EAP ssid profiles would have been added above if they existed.

        name = self.command_line_args.testbed + "-" + self.fw_model + "_" + self.mode

        print("child profiles: ", self.child_profiles)

        try:
            self.create_ap_profile = self.cloud.create_or_update_ap_profile(self.command_line_args.sdk_base_url,
                                                                            self.bearer, self.customer_id,
                                                                            self.command_line_args.default_ap_profile,
                                                                            name,
                                                                            self.child_profiles)
            self.test_profile_id = self.create_ap_profile
            print("Test Profile ID for Test is:", self.test_profile_id)
            self.client.update_testrail(case_id=self.test_cases["ap_" + self.mode], run_id=self.rid, status_id=1,
                                        msg='AP profile for ' + mode + ' tests created successfully')
            self.test_cases["ap_" + self.mode] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            create_ap_profile = "error"
            print("Error creating AP profile for bridge tests. Will use existing AP profile")
            self.client.update_testrail(case_id=self.test_cases["ap_" + self.mode], run_id=self.rid, status_id=5,
                                        msg='AP profile for ' + mode + ' tests could not be created using API')
            self.test_cases["ap_" + self.mode] = "failed"

        self.ap_profile = self.cloud.set_ap_profile(eq_id, self.test_profile_id)

    def cleanup_profile(self):
        pass

    def validate_changes(self, mode="bridge"):

        ssid_list_ok = False
        vif_state_ok = False
        for i in range(18):
            ### Check if VIF Config and VIF State reflect AP Profile from CloudSDK
            ## VIF Config

            if (ssid_list_ok and vif_state_ok):
                print("SSID and VIF state is OK, continuing.")
                break

            print("Check: %i/18  Wait 10 seconds for profile push.\n" % (i))
            time.sleep(10)
            try:
                print("SSIDs in AP Profile:", self.ssid_config)
                print("SSID Profiles in AP Profile:", self.ssid_prof_config)

                ssid_list = ap_ssh.get_vif_state(self.command_line_args)
                print("SSIDs in AP VIF Config:", ssid_list)

                if set(ssid_list) == set(self.ssid_config):
                    print("SSIDs in Wifi_VIF_Config Match AP Profile Config")
                    self.client.update_testrail(case_id=self.test_cases[mode + "_vifc"], run_id=self.rid, status_id=1,
                                                msg='SSIDs in VIF Config matches AP Profile Config')
                    self.test_cases[mode + "_vifc"] = "passed"
                    ssid_list_ok = True
                else:
                    print("SSIDs in Wifi_VIF_Config do not match desired AP Profile Config")
                    self.client.update_testrail(case_id=self.test_cases[mode + "_vifc"], run_id=self.rid, status_id=5,
                                                msg='SSIDs in VIF Config do not match AP Profile Config')
                    self.test_cases[mode + "_vifc"] = "failed"
            except Exception as ex:
                print(ex)
                logging.error(logging.traceback.format_exc())
                ssid_list = "ERROR"
                print("Error accessing VIF Config from AP CLI")
                self.client.update_testrail(case_id=self.test_cases[mode + "_vifc"], run_id=self.rid, status_id=4,
                                            msg='Cannot determine VIF Config - re-test required')
                self.test_cases[mode + "_vifc"] = "error"

            # VIF State
            try:
                ssid_state = ap_ssh.get_vif_state(self.command_line_args)
                print("SSIDs in AP VIF State:", ssid_state)

                if set(ssid_state) == set(self.ssid_config):
                    print("SSIDs properly applied on AP")
                    self.client.update_testrail(case_id=self.test_cases[mode + "_vifs"], run_id=self.rid, status_id=1,
                                                msg='SSIDs in VIF Config applied to VIF State')
                    self.test_cases[mode + "_vifs"] = "passed"
                    vif_state_ok = True
                else:
                    print("SSIDs not applied on AP")
                    self.client.update_testrail(case_id=self.test_cases[mode + "_vifs"], run_id=self.rid, status_id=5,
                                                msg='SSIDs in VIF Config not applied to VIF State')
                    self.test_cases[mode + "_vifs"] = "failed"
            except Exception as ex:
                print(ex)
                logging.error(logging.traceback.format_exc())
                ssid_list = "ERROR"
                print("Error accessing VIF State from AP CLI")
                self.client.update_testrail(case_id=self.test_cases[mode + "_vifs"], run_id=self.rid, status_id=4,
                                            msg='Cannot determine VIF State - re-test required')
                self.test_cases[mode + "_vifs"] = "error"

        print("Profiles Created")
