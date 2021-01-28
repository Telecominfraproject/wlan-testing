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

    def get_bearer(self, cloudSDK_url, cloud_type):
        cloud_login_url = cloudSDK_url+"/management/"+cloud_type+"/oauth2/token"
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
        except requests.exceptions.RequestException as e:
            raise SystemExit("Exiting Script! Cloud not get bearer token for reason:",e)
        token_data = token_response.json()
        bearer_token = token_data['access_token']
        return(bearer_token)

    def ap_firmware(self, customer_id, equipment_id, cloudSDK_url, bearer):
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
            current_ap_fw = status_data[2]['details']['reportedSwVersion']
            return current_ap_fw
        else:
            return("ERROR")

    def CloudSDK_images(self, apModel, cloudSDK_url, bearer):
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

    def firwmare_upload(self, commit, apModel,latest_image,fw_url,cloudSDK_url,bearer):
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

    def get_firmware_id(self, latest_ap_image, cloudSDK_url, bearer):
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

    def get_paged_url(self, bearer, url_base):
        url = url_base

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        rv = []
        req = 0
        while True:
            print("Request %i: in get-paged-url, url: %s"%(req, url))
            response = requests.request("GET", url, headers=headers, data=payload)
            rjson = response.json()
            rv.append(rjson)
            if not 'context' in rjson:
                print(json.dumps(rjson, indent=4, sort_keys=True))
                break
            if rjson['context']['lastPage']:
                break
            context_str = json.dumps(rjson['context'])
            #print("context-str: %s"%(context_str))
            url = url_base + "&paginationContext=" + urllib.parse.quote(context_str)
            req = req + 1
            #print("Profile, reading another page, context:")
            #print(rjson['context'])
            #print("url: %s"%(fw_id_url))

        return rv

    def get_url(self, bearer, url):
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        print("Get-url, url: %s"%(url))
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def get_customer_profiles(self, cloudSDK_url, bearer, customer_id, object_id):
        if object_id != None:
            url_base = cloudSDK_url + "/portal/profile" + "?profileId=" + object_id
            return [self.get_url(bearer, url_base)]
        else:
            url_base = cloudSDK_url + "/portal/profile/forCustomer" + "?customerId=" + customer_id
            return self.get_paged_url(bearer, url_base)

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
                print("looking for profile: %s  checking prof-id: %s  model-type: %s  type: %s  name: %s"%(name, prof_id, prof_model_type, prof_type, prof_name))
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
        return(response)

    def delete_equipment(self, cloudSDK_url, bearer, eq_id):
        url = cloudSDK_url + '/portal/equipment/?equipmentId=' + eq_id
        print("Deleting equipment with url: " + url)
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("DELETE", url, headers=headers, data=payload)
        return(response)

    def get_customer_locations(self, cloudSDK_url, bearer, customer_id):
        url_base = cloudSDK_url + "/portal/location/forCustomer" + "?customerId=" + customer_id
        return self.get_paged_url(bearer, url_base)

    def get_customer_equipment(self, cloudSDK_url, bearer, customer_id):
        url_base = cloudSDK_url + "/portal/equipment/forCustomer" + "?customerId=" + customer_id
        return self.get_paged_url(bearer, url_base)

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
        return response.json()

    def delete_firmware(self, fw_id, cloudSDK_url, bearer):
        url = cloudSDK_url + '/portal/firmware/version?firmwareVersionId=' + fw_id
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("DELETE", url, headers=headers, data=payload)
        return(response)

    def update_firmware(self, equipment_id, latest_firmware_id, cloudSDK_url, bearer):
        url = cloudSDK_url+"/portal/equipmentGateway/requestFirmwareUpdate?equipmentId="+equipment_id+"&firmwareVersionId="+latest_firmware_id

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        #print(response.text)
        return response.json()

    # This one is not yet tested, coded from spec, could have bugs.
    def ap_reboot(self, equipment_id, cloudSDK_url, bearer):
        url = cloudSDK_url+"/portal/equipmentGateway/requestApReboot?equipmentId="+equipment_id

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        #print(response.text)
        return response.json()

    # This one is not yet tested, coded from spec, could have bugs.
    def ap_switch_sw_bank(self, equipment_id, cloudSDK_url, bearer):
        url = cloudSDK_url+"/portal/equipmentGateway/requestApSwitchSoftwareBank?equipmentId="+equipment_id

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        #print(response.text)
        return response.json()

    # This one is not yet tested, coded from spec, could have bugs.
    def ap_factory_reset(self, equipment_id, cloudSDK_url, bearer):
        url = cloudSDK_url+"/portal/equipmentGateway/requestApFactoryReset?equipmentId="+equipment_id

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        #print(response.text)
        return response.json()

    # This one is not yet tested, coded from spec, could have bugs.
    def ap_channel_change(self, equipment_id, cloudSDK_url, bearer):
        url = cloudSDK_url+"/portal/equipmentGateway/requestChannelChange?equipmentId="+equipment_id

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        #print(response.text)
        return response.json()

    def set_ap_profile(self, equipment_id, test_profile_id, cloudSDK_url, bearer):
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
        print(equipment_info)

        ###Update AP Info with Required Profile ID
        url = cloudSDK_url+"/portal/equipment"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }

        response = requests.request("PUT", url, headers=headers, data=json.dumps(equipment_info))
        print(response)

    def get_cloudsdk_version(self, cloudSDK_url, bearer):
        #print(latest_ap_image)
        url = cloudSDK_url+"/ping"

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + bearer
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        cloud_sdk_version = response.json()
        return cloud_sdk_version

    def create_ap_profile(self, cloudSDK_url, bearer, customer_id, template, name, child_profiles):
        # TODO:  specify default ap profile.
        profile = self.get_customer_profile_by_name(cloudSDK_url, bearer, customer_id, template)

        profile["name"] = name
        profile["childProfileIds"] = child_profiles

        url = cloudSDK_url+"/portal/profile"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }

        data_str = json.dumps(profile)
        print("Creating new ap-profile, data: %s"%(data_str))
        response = requests.request("POST", url, headers=headers, data=data_str)
        ap_profile = response.json()
        print("New AP profile: ", ap_profile)
        ap_profile_id = ap_profile['id']
        return ap_profile_id

    def create_or_update_ap_profile(self, cloudSDK_url, bearer, customer_id, template, name, child_profiles):
        profile = self.get_customer_profile_by_name(cloudSDK_url, bearer, customer_id, name)
        if profile == None:
            return self.create_ap_profile(cloudSDK_url, bearer, customer_id, template, name, child_profiles)

        profile["name"] = name
        profile["childProfileIds"] = child_profiles

        url = cloudSDK_url+"/portal/profile"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }

        data_str = json.dumps(profile)
        print("Updating ap-profile, data: %s"%(data_str))
        response = requests.request("PUT", url, headers=headers, data=data_str)
        print(response)
        return profile['id']

    def create_ssid_profile(self, cloudSDK_url, bearer, customer_id, template, name, ssid, passkey, radius, security, mode, vlan, radios):
        print("create-ssid-profile, template: %s"%(template))
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
        response = requests.request("POST", url, headers=headers, data=json.dumps(profile))
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
        print("Update existing ssid profile, name: %s"%(name))
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
        response = requests.request("PUT", url, headers=headers, data=json.dumps(profile))
        print(response)
        return profile['id']

    def create_radius_profile(self, cloudSDK_url, bearer, customer_id, template, name, subnet_name, subnet, subnet_mask,
                              region, server_name, server_ip, secret, auth_port):
        print("Create-radius-profile called, template: %s"%(template))
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
        print("Sending json to create radius: %s"%(data_str))
        response = requests.request("POST", url, headers=headers, data=data_str)
        radius_profile = response.json()
        print(radius_profile)
        radius_profile_id = radius_profile['id']
        return radius_profile_id

    def create_or_update_radius_profile(self, cloudSDK_url, bearer, customer_id, template, name, subnet_name, subnet, subnet_mask,
                                        region, server_name, server_ip, secret, auth_port):
        profile = self.get_customer_profile_by_name(cloudSDK_url, bearer, customer_id, name)
        if profile == None:
            # create one then
            return self.create_radius_profile(cloudSDK_url, bearer, customer_id, template, name, subnet_name, subnet, subnet_mask,
                                              region, server_name, server_ip, secret, auth_port)
        
        print("Found existing radius profile, will update, name: %s"%(name))

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
        response = requests.request("PUT", url, headers=headers, data=json.dumps(profile))
        # TODO:  Code below is wrong, obviously in hindsight.  But, need to parse response
        # and throw exception or something if it is an error code.
        #response = requests.request("PUT", url, headers=headers, data=profile)
        print(response)
        return profile['id']



# Library for creating AP Profiles
class CreateAPProfiles:

    def __init__(self,
                 command_line_args,
                 cloud = None,
                 cloud_type= "v1",
                 customer_id = "2",
                 client = None
                 ):

        self.command_line_args = command_line_args
        self.radius_profile = None
        self.radius_name = None
        self.cloud = cloud
        self.client= client
        self.cloud_type = cloud_type
        self.customer_id = customer_id
        self.ap_cli_info = ssh_cli_active_fw(self.command_line_args)
        if self.cloud == None:
            print("cloud cannot be None")
            exit()
        self.ap_cli_fw = self.ap_cli_info['active_fw']
        self.bearer = self.cloud.get_bearer(self.command_line_args.sdk_base_url  , self.cloud_type)
        self.radius_info = {

            "name": "Lab-RADIUS",
            "subnet_name": "Lab",
            "subnet": "10.10.0.0",
            "subnet_mask": 16,
            "region": "Toronto",
            "server_name": "Lab-RADIUS",
            "server_ip": "10.10.10.203",
            "secret": "testing123",
            "auth_port": 1812
        }
        self.ap_models = ["ec420", "ea8300", "ecw5211", "ecw5410"]
        self.report_data = {}
        self.report_data['tests'] = dict.fromkeys(self.ap_models, "")
        self.test_cases = {
            "radius_profile" : None,
            "ssid_5g_eap_bridge" : None,
            "ssid_5g_wpa2_bridge" :  None,
            "ssid_5g_wpa_bridge" : None,
            "ssid_2g_eap_bridge" : None,
            "ssid_2g_wpa2_bridge" : None,
            "ssid_2g_wpa_bridge" : None,
            "ap_bridge" : None,
            "bridge_vifc" : None,
            "bridge_vifs" : None
        }



    def create_radius_profile(self, radius_name, rid, key):

        ### Create RADIUS profile - used for all EAP SSIDs
        self.radius_name = radius_name
        self.radius_template = "Radius-Profile"  # Default radius profile found in cloud-sdk
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
                self.radius_profile = self.cloud.create_or_update_radius_profile(self.command_line_args.sdk_base_url, self.bearer, self.customer_id,
                                                                       self.radius_template, self.radius_name, self.subnet_name,
                                                                       self.subnet,
                                                                       self.subnet_mask, self.region, self.server_name, self.server_ip,
                                                                       self.secret, self.auth_port)
                print("radius profile Id is", self.radius_profile)
                client.update_testrail(case_id=self.test_cases["radius_profile"], run_id=self.rid, status_id=1,
                                       msg='RADIUS profile created successfully')
                self.test_cases["radius_profile"] = "passed"
            except:
                print(ex)
                logging.error(logging.traceback.format_exc())
                radius_profile = 'error'
                print("RADIUS Profile Create Error, will skip radius profile.")
                # Set backup profile ID so test can continue
                radius_profile = None
                radius_name = None
                server_name = "Lab-RADIUS"
                self.client.update_testrail(case_id=self.test_cases["radius_profile"], run_id=self.rid, status_id=5,
                                       msg='Failed to create RADIUS profile')
                self.test_cases["radius_profile"] = "failed"

    def create_ssid_profile(self, ssid_profile_data= None):
        self.ssid_profile_data = ssid_profile_data
        self.ssid_template = ssid_profile_data["ssid_template"]

        # 5G SSID's

        # 5G eap
        try:
            self.fiveG_eap = self.cloud.create_or_update_ssid_profile(self.command_line_args.sdk_base_url, self.bearer, self.customer_id, self.ssid_template,
                                                            ssid_profile_data['5G']['eap']['info'][1],
                                                            ssid_profile_data['5G']['eap']['info'][0], None,
                                                            self.radius_name,
                                                            "wpa2OnlyRadius", "BRIDGE", 1, ["is5GHzU", "is5GHz", "is5GHzL"])
            print("5G EAP SSID created successfully - bridge mode")
            self.client.update_testrail(case_id=self.test_cases["ssid_5g_eap_bridge"], run_id=self.rid, status_id=1,
                                   msg='5G EAP SSID created successfully - bridge mode')
            self.test_cases["ssid_5g_eap_bridge"] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            fiveG_eap = "error"
            print("5G EAP SSID create failed - bridge mode")
            self.client.update_testrail(case_id=self.test_cases["ssid_5g_eap_bridge"], run_id=self.rid, status_id=5,
                                   msg='5G EAP SSID create failed - bridge mode')
            self.test_cases["ssid_5g_eap_bridge"] = "failed"

        # 5g wpa2
        try:
            self.fiveG_wpa2 = self.cloud.create_or_update_ssid_profile(self.command_line_args.sdk_base_url, self.bearer, self.customer_id, self.ssid_template,
                                                             ssid_profile_data['5G']['wpa2']['info'][1],
                                                             ssid_profile_data['5G']['wpa2']['info'][0], ssid_profile_data['5G']['wpa2']['psk'][0],
                                                             "Radius-Accounting-Profile", "wpa2OnlyPSK", "BRIDGE", 1,
                                                             ["is5GHzU", "is5GHz", "is5GHzL"])
            print("5G WPA2 SSID created successfully - bridge mode")
            self.client.update_testrail(case_id=self.test_cases["ssid_5g_wpa2_bridge"], run_id=self.rid, status_id=1,
                                   msg='5G WPA2 SSID created successfully - bridge mode')
            self.test_cases["ssid_5g_wpa2_bridge"] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            fiveG_wpa2 = "error"
            print("5G WPA2 SSID create failed - bridge mode")
            self.client.update_testrail(case_id=test_cases["ssid_5g_wpa2_bridge"], run_id=self.rid, status_id=5,
                                   msg='5G WPA2 SSID create failed - bridge mode')
            self.test_cases["ssid_5g_wpa2_bridge"] = "failed"

        # 5g wpa


        try:
            self.fiveG_wpa = self.cloud.create_or_update_ssid_profile(self.command_line_args.sdk_base_url, self.bearer, self.customer_id, self.ssid_template,
                                                            ssid_profile_data['5G']['wpa']['info'][1],
                                                            ssid_profile_data['5G']['wpa']['info'][0], ssid_profile_data['5G']['wpa']['psk'][0],
                                                            "Radius-Accounting-Profile", "wpaPSK", "BRIDGE", 1,
                                                            ["is5GHzU", "is5GHz", "is5GHzL"])
            print("5G WPA SSID created successfully - bridge mode")
            self.client.update_testrail(case_id=self.test_cases["ssid_5g_wpa_bridge"], run_id=self.rid, status_id=1,
                                   msg='5G WPA SSID created successfully - bridge mode')
            self.test_cases["ssid_5g_wpa_bridge"] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            fiveG_wpa = "error"
            print("5G WPA SSID create failed - bridge mode")
            self.client.update_testrail(case_id=test_cases["ssid_5g_wpa_bridge"], run_id=self.rid, status_id=5,
                                   msg='5G WPA SSID create failed - bridge mode')
            self.test_cases["ssid_5g_wpa_bridge"] = "failed"

        # 2.4G SSIDs

        # 2.4G eap
        try:
            self.twoFourG_eap = self.cloud.create_or_update_ssid_profile(self.command_line_args.sdk_base_url, self.bearer, self.customer_id, self.ssid_template,
                                                               ssid_profile_data['2G']['eap']['info'][1],
                                                               ssid_profile_data['2G']['eap']['info'][0], None,
                                                               self.radius_name, "wpa2OnlyRadius", "BRIDGE", 1,
                                                               ["is2dot4GHz"])
            print("2.4G EAP SSID created successfully - bridge mode")
            self.client.update_testrail(case_id=self.test_cases["ssid_2g_eap_bridge"], run_id=self.rid, status_id=1,
                                   msg='2.4G EAP SSID created successfully - bridge mode')
            self.test_cases["ssid_2g_eap_bridge"] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            twoFourG_eap = "error"
            print("2.4G EAP SSID create failed - bridge mode")
            self.client.update_testrail(case_id=self.test_cases["ssid_2g_eap_bridge"], run_id=self.rid, status_id=5,
                                   msg='2.4G EAP SSID create failed - bridge mode')
            self.test_cases["ssid_2g_eap_bridge"] = "failed"

        # 2.4G wpa2
        try:
            self.twoFourG_wpa2 = self.cloud.create_or_update_ssid_profile(self.command_line_args.sdk_base_url, self.bearer, self.customer_id, self.ssid_template,
                                                                ssid_profile_data['2G']['wpa2']['info'][1],
                                                                ssid_profile_data['2G']['wpa2']['info'][0], ssid_profile_data['2G']['wpa2']['psk'][0],
                                                                "Radius-Accounting-Profile", "wpa2OnlyPSK", "BRIDGE", 1,
                                                                ["is2dot4GHz"])
            print("2.4G WPA2 SSID created successfully - bridge mode")
            self.client.update_testrail(case_id=self.test_cases["ssid_2g_wpa2_bridge"], run_id=self.rid, status_id=1,
                                   msg='2.4G WPA2 SSID created successfully - bridge mode')
            self.test_cases["ssid_2g_wpa2_bridge"] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            twoFourG_wpa2 = "error"
            print("2.4G WPA2 SSID create failed - bridge mode")
            self.client.update_testrail(case_id=test_cases["ssid_2g_wpa2_bridge"], run_id=self.rid, status_id=5,
                                   msg='2.4G WPA2 SSID create failed - bridge mode')
            self.test_cases["ssid_2g_wpa2_bridge"] = "failed"

        # 2.4G wpa
        try:
            self.twoFourG_wpa = self.cloud.create_or_update_ssid_profile(self.command_line_args.sdk_base_url, self.bearer, self.customer_id, self.ssid_template,
                                                               ssid_profile_data['2G']['wpa']['info'][1],
                                                               ssid_profile_data['2G']['wpa']['info'][0], ssid_profile_data['2G']['wpa']['psk'][0],
                                                               "Radius-Accounting-Profile", "wpaPSK", "BRIDGE", 1,
                                                               ["is2dot4GHz"])
            print("2.4G WPA SSID created successfully - bridge mode")
            self.client.update_testrail(case_id=self.test_cases["ssid_2g_wpa_bridge"], run_id=self.rid, status_id=1,
                                   msg='2.4G WPA SSID created successfully - bridge mode')
            self.test_cases["ssid_2g_wpa_bridge"] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            twoFourG_wpa = "error"
            print("2.4G WPA SSID create failed - bridge mode")
            self.client.update_testrail(case_id=self.test_cases["ssid_2g_wpa_bridge"], run_id=self.rid, status_id=5,
                                   msg='2.4G WPA SSID create failed - bridge mode')
            self.test_cases["ssid_2g_wpa_bridge"] = "failed"



    def create_ap_bridge_profile(self,fw_model=None):
        self.fw_model = fw_model
        self.rfProfileId = lab_ap_info.rf_profile
        self.child_profiles = [self.fiveG_wpa2, self.fiveG_wpa, self.twoFourG_wpa2, self.twoFourG_wpa, self.rfProfileId]

        self.ssid_prof_config = [self.ssid_profile_data['5G']['wpa2']['info'][1],
                                 self.ssid_profile_data['5G']['wpa']['info'][1],
                                 self.ssid_profile_data['2G']['wpa2']['info'][1],
                                 self.ssid_profile_data['2G']['wpa']['info'][1]]
        self.ssid_config = [self.ssid_profile_data['5G']['wpa2']['info'][0],
                                 self.ssid_profile_data['5G']['wpa']['info'][0],
                                 self.ssid_profile_data['2G']['wpa2']['info'][0],
                                 self.ssid_profile_data['2G']['wpa']['info'][0]]

        if self.radius_profile is not None:
            child_profiles.append(radius_profile)
            child_profiles.append(fiveG_eap)
            child_profiles.append(twoFourG_eap)
            ssid_prof_config.append(prof_5g_wpa2_name)
            ssid_prof_config.append(prof_2g_wpa2_name)
            ssid_config.append(ssid_5g_wpa2)
            ssid_config.append(ssid_2g_wpa2)

        name = self.command_line_args.testbed + "-" + self.fw_model + "_bridge"

        try:
            self.create_ap_profile = self.cloud.create_or_update_ap_profile(self.command_line_args.sdk_base_url, self.bearer, self.customer_id,
                                                                  self.command_line_args.default_ap_profile, name,
                                                                  self.child_profiles)
            self.test_profile_id = self.create_ap_profile
            print("Test Profile ID for Test is:", self.test_profile_id)
            self.client.update_testrail(case_id=self.test_cases["ap_bridge"], run_id=self.rid, status_id=1,
                                   msg='AP profile for bridge tests created successfully')
            self.test_cases["ap_bridge"] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            create_ap_profile = "error"
            print("Error creating AP profile for bridge tests. Will use existing AP profile")
            self.client.update_testrail(case_id=self.test_cases["ap_bridge"], run_id=self.rid, status_id=5,
                                   msg='AP profile for bridge tests could not be created using API')
            self.test_cases["ap_bridge"] = "failed"
        self.ap_profile = self.cloud.set_ap_profile(self.command_line_args.equipment_id, self.test_profile_id, self.command_line_args.sdk_base_url, self.bearer)



    def cleanup_profile(self):
        pass

    def validate_changes(self):

        ssid_list_ok = False
        vif_state_ok = False
        for i in range(18):
            ### Check if VIF Config and VIF State reflect AP Profile from CloudSDK
            ## VIF Config

            if (ssid_list_ok and vif_state_ok):
                print("SSID and VIF state is OK, continuing.")
                break

            print("Check: %i  Wait 10 seconds for profile push.\n" % (i))
            time.sleep(10)
            try:
                print("SSIDs in AP Profile:", self.ssid_config)
                print("SSID Profiles in AP Profile:", self.ssid_prof_config)

                ssid_list = ap_ssh.get_vif_state(self.command_line_args)
                print("SSIDs in AP VIF Config:", ssid_list)

                if set(ssid_list) == set(self.ssid_config):
                    print("SSIDs in Wifi_VIF_Config Match AP Profile Config")
                    self.client.update_testrail(case_id=self.test_cases["bridge_vifc"], run_id=self.rid, status_id=1,
                                           msg='SSIDs in VIF Config matches AP Profile Config')
                    self.test_cases["bridge_vifc"] = "passed"
                    ssid_list_ok = True
                else:
                    print("SSIDs in Wifi_VIF_Config do not match desired AP Profile Config")
                    self.client.update_testrail(case_id=self.test_cases["bridge_vifc"], run_id=self.rid, status_id=5,
                                           msg='SSIDs in VIF Config do not match AP Profile Config')
                    self.test_cases["bridge_vifc"] = "failed"
            except Exception as ex:
                print(ex)
                logging.error(logging.traceback.format_exc())
                ssid_list = "ERROR"
                print("Error accessing VIF Config from AP CLI")
                self.client.update_testrail(case_id=self.test_cases["bridge_vifc"], run_id=self.rid, status_id=4,
                                       msg='Cannot determine VIF Config - re-test required')
                self.test_cases["bridge_vifc"] = "error"

            # VIF State
            try:
                ssid_state = ap_ssh.get_vif_state(self.command_line_args)
                print("SSIDs in AP VIF State:", ssid_state)

                if set(ssid_state) == set(self.ssid_config):
                    print("SSIDs properly applied on AP")
                    self.client.update_testrail(case_id=self.test_cases["bridge_vifs"], run_id=self.rid, status_id=1,
                                           msg='SSIDs in VIF Config applied to VIF State')
                    self.test_cases["bridge_vifs"] = "passed"
                    vif_state_ok = True
                else:
                    print("SSIDs not applied on AP")
                    self.client.update_testrail(case_id=self.test_cases["bridge_vifs"], run_id=self.rid, status_id=5,
                                           msg='SSIDs in VIF Config not applied to VIF State')
                    self.test_cases["bridge_vifs"] = "failed"
            except Exception as ex:
                print(ex)
                logging.error(logging.traceback.format_exc())
                ssid_list = "ERROR"
                print("Error accessing VIF State from AP CLI")
                self.client.update_testrail(case_id=self.test_cases["bridge_vifs"], run_id=self.rid, status_id=4,
                                       msg='Cannot determine VIF State - re-test required')
                self.test_cases["bridge_vifs"] = "error"

        print("Profiles Created")