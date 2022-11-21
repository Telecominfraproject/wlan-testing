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

user=os.getenv('CLOUDSDK_USER')
password=os.getenv('CLOUDSDK_PWD')

###Class for CloudSDK Interaction via RestAPI
class CloudSDK:
    def __init__(self):
        self.user = user

    def get_bearer(cloudSDK_url, cloud_type):
        cloud_login_url = cloudSDK_url+"/management/"+cloud_type+"/oauth2/token"
        payload = '''
        {
        "userId": "'''+user+'''",
        "password": "'''+password+'''"
        }   
        '''
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

    def ap_firmware(customer_id,equipment_id, cloudSDK_url, bearer):
        equip_fw_url = cloudSDK_url+"/portal/status/forEquipment?customerId="+customer_id+"&equipmentId="+equipment_id
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        status_response = requests.request("GET", equip_fw_url, headers=headers, data=payload)
        status_code = status_response.status_code
        if status_code == 200:
            status_data = status_response.json()
            #print(status_data)
            try:
                current_ap_fw = status_data[2]['details']['reportedSwVersion']
                return current_ap_fw
            except:
                current_ap_fw = "error"
                return "ERROR"

        else:
            return "ERROR"

    def CloudSDK_images(apModel, cloudSDK_url, bearer):
        getFW_url = cloudSDK_url+"/portal/firmware/version/byEquipmentType?equipmentType=AP&modelId=" + apModel
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

    def firwmare_upload(commit, apModel,latest_image,fw_url,cloudSDK_url,bearer):
        fw_upload_url = cloudSDK_url+"/portal/firmware/version"
        payload = "{\n  \"model_type\": \"FirmwareVersion\",\n  \"id\": 0,\n  \"equipmentType\": \"AP\",\n  \"modelId\": \""+apModel+"\",\n  \"versionName\": \""+latest_image+"\",\n  \"description\": \"\",\n  \"filename\": \""+fw_url+"\",\n  \"commit\": \""+commit+"\",\n  \"validationMethod\": \"MD5_CHECKSUM\",\n  \"validationCode\": \"19494befa87eb6bb90a64fd515634263\",\n  \"releaseDate\": 1596192028877,\n  \"createdTimestamp\": 0,\n  \"lastModifiedTimestamp\": 0\n}\n\n"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", fw_upload_url, headers=headers, data=payload)
        #print(response)
        upload_result = response.json()
        return(upload_result)

    def get_firmware_id(latest_ap_image, cloudSDK_url, bearer):
        #print(latest_ap_image)
        fw_id_url = cloudSDK_url+"/portal/firmware/version/byName?firmwareVersionName="+latest_ap_image

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("GET", fw_id_url, headers=headers, data=payload)
        fw_data = response.json()
        latest_fw_id = fw_data['id']
        return latest_fw_id

    def delete_firmware(fw_id, cloudSDK_url, bearer):
        url = cloudSDK_url + '/portal/firmware/version?firmwareVersionId=' + fw_id
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("DELETE", url, headers=headers, data=payload)
        return(response)

    def update_firmware(equipment_id, latest_firmware_id, cloudSDK_url, bearer):
        url = cloudSDK_url+"/portal/equipmentGateway/requestFirmwareUpdate?equipmentId="+equipment_id+"&firmwareVersionId="+latest_firmware_id

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        #print(response.text)
        return response.json()

    def set_ap_profile(equipment_id, test_profile_id, cloudSDK_url, bearer):
        ###Get AP Info
        url = cloudSDK_url+"/portal/equipment?equipmentId="+equipment_id
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
        url = cloudSDK_url+"/portal/equipment"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("PUT", url, headers=headers, data=json.dumps(equipment_info))
        #print(response)

    def get_cloudsdk_version(cloudSDK_url, bearer):
        #print(latest_ap_image)
        url = cloudSDK_url+"/ping"

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        cloud_sdk_version = response.json()
        return cloud_sdk_version

    def create_ap_profile(cloudSDK_url, bearer, template, name, customer_id, child_profiles):
        with open(template, 'r+') as ap_profile:
            profile = json.load(ap_profile)
            profile["name"] = name
            profile['customerId'] = customer_id
            profile["childProfileIds"] = child_profiles

        with open(template, 'w') as ap_profile:
            json.dump(profile, ap_profile)

        url = cloudSDK_url+"/portal/profile"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("POST", url, headers=headers, data=open(template, 'rb'))
        ap_profile = response.json()
        print(ap_profile)
        ap_profile_id = ap_profile['id']
        return ap_profile_id

    def create_ssid_profile(cloudSDK_url, bearer, template, name, customer_id, ssid, passkey, radius, security, mode, vlan, radios):
        with open(template, 'r+') as ssid_profile:
            profile = json.load(ssid_profile)
            profile['name'] = name
            profile['customerId'] = customer_id
            profile['details']['ssid'] = ssid
            profile['details']['keyStr'] = passkey
            profile['details']['radiusServiceId'] = radius
            profile['details']['secureMode'] = security
            profile['details']['forwardMode'] = mode
            profile['details']['vlanId'] = vlan
            profile['details']['appliedRadios'] = radios
            if radius != 0:
                profile["childProfileIds"] = [radius]
            else:
                profile["childProfileIds"] = []
        with open(template, 'w') as ssid_profile:
            json.dump(profile, ssid_profile)

        url = cloudSDK_url + "/portal/profile"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("POST", url, headers=headers, data=open(template, 'rb'))
        ssid_profile = response.json()
        #print(ssid_profile)
        ssid_profile_id = ssid_profile['id']
        return ssid_profile_id

    def create_radius_profile(cloudSDK_url, bearer, template, name, customer_id, server_ip, secret, auth_port):
        with open(template, 'r+') as radius_profile:
            profile = json.load(radius_profile)

            profile['name'] = name
            profile['customerId'] = customer_id
            profile['details']["primaryRadiusAuthServer"]['ipAddress'] = server_ip
            profile['details']["primaryRadiusAuthServer"]['secret'] = secret
            profile['details']["primaryRadiusAuthServer"]['port'] = auth_port

        with open(template, 'w') as radius_profile:
            json.dump(profile, radius_profile)

        url = cloudSDK_url + "/portal/profile"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("POST", url, headers=headers, data=open(template, 'rb'))
        radius_profile = response.json()
        radius_profile_id = radius_profile['id']
        return radius_profile_id

    def delete_profile(cloudSDK_url, bearer, profile_id):
        url = cloudSDK_url + "/portal/profile?profileId="+profile_id
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        del_profile = requests.request("DELETE", url, headers=headers, data=payload)
        status_code = del_profile.status_code
        if status_code == 200:
            return("SUCCESS")
        else:
            return ("ERROR")

    def update_ssid_profile(cloudSDK_url, bearer, profile_id, new_ssid, new_secure_mode, new_psk):
        get_profile_url = cloudSDK_url + "/portal/profile?profileId="+profile_id

        payload = {}
        headers = headers = {
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("GET", get_profile_url, headers=headers, data=payload)
        original_profile = response.json()
        print(original_profile)

        original_profile['details']['ssid'] = new_ssid
        original_profile['details']['secureMode'] = new_secure_mode
        original_profile['details']['keyStr'] = new_psk

        put_profile_url = cloudSDK_url + "/portal/profile"
        payload = original_profile
        headers = headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("PUT", put_profile_url, headers=headers, json=payload)
        print(response)
        updated_profile = response.json()
        return updated_profile