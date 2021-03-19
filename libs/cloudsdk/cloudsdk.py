# !/usr/local/lib64/python3.8
"""
    Library for setting up the configuration for cloud connectivity
        1. testbed/ sdk_base_url
        2. login credentials
"""
import base64
import datetime
import json
import re
import ssl
import time
import urllib

import requests
import swagger_client
from swagger_client import FirmwareManagementApi
from swagger_client import EquipmentGatewayApi
from bs4 import BeautifulSoup

from testbed_info import SDK_BASE_URLS
from testbed_info import LOGIN_CREDENTIALS


class ConfigureCloudSDK:

    def __init__(self):
        self.configuration = swagger_client.Configuration()

    def set_credentials(self, user_id=None, password=None):
        if user_id is None or password is None:
            self.configuration.username = LOGIN_CREDENTIALS['userId']
            self.configuration.password = LOGIN_CREDENTIALS['password']
            print("Login Credentials set to default: \n user_id: %s\n password: %s\n" % (LOGIN_CREDENTIALS['userId'],
                                                                                         LOGIN_CREDENTIALS['password']))
            return False
        else:
            LOGIN_CREDENTIALS['user_id'] = user_id
            self.configuration.username = user_id
            LOGIN_CREDENTIALS['password'] = password
            self.configuration.password = password
            print("Login Credentials set to custom: \n user_id: %s\n password: %s\n" % (LOGIN_CREDENTIALS['userId'],
                                                                                        LOGIN_CREDENTIALS['password']))
            return True

    def select_testbed(self, testbed=None):
        if testbed is None:
            print("No Testbed Selected")
            exit()
        self.sdk_base_url = "https://wlan-portal-svc-" + testbed + ".cicd.lab.wlan.tip.build"
        self.configuration.host = self.sdk_base_url
        print("Testbed Selected: %s\n SDK_BASE_URL: %s\n" % (testbed, self.sdk_base_url))
        return True

    def set_sdk_base_url(self, sdk_base_url=None):
        if sdk_base_url is None:
            print("URL is None")
            exit()
        self.configuration.host = sdk_base_url
        return True


"""
    Library for cloudsdk_tests generic usages, it instantiate the bearer and credentials.
    It provides the connectivity to the cloud.
"""


class CloudSDK(ConfigureCloudSDK):
    """
    constructor for cloudsdk_tests library : can be used from pytest framework
    """

    def __init__(self, testbed=None, customer_id=None):
        super().__init__()
        if customer_id is None:
            print("Invalid Customer Id")
            exit()
        self.customer_id = customer_id
        # Setting the CloudSDK Client Configuration
        self.select_testbed(testbed=testbed)
        self.set_credentials()
        # self.configuration.refresh_api_key_hook = self.get_bearer_token

        # Connecting to CloudSDK
        self.api_client = swagger_client.ApiClient(self.configuration)
        self.login_client = swagger_client.LoginApi(api_client=self.api_client)
        self.bearer = self.get_bearer_token()

        self.api_client.default_headers['Authorization'] = "Bearer " + self.bearer._access_token
        self.equipment_client = swagger_client.EquipmentApi(self.api_client)
        self.profile_client = swagger_client.ProfileApi(self.api_client)
        self.api_client.configuration.api_key_prefix = {
            "Authorization": "Bearer " + self.bearer._access_token
        }
        self.api_client.configuration.refresh_api_key_hook = self.get_bearer_token()
        self.ping_response = self.portal_ping()
        self.default_profiles = {}
        # print(self.bearer)
        if self.ping_response._application_name != 'PortalServer':
            print("Server not Reachable")
            exit()
        print("Connected to CloudSDK Server")

    """
    Login Utilities
    """

    def get_bearer_token(self):
        return self.login_client.get_access_token(LOGIN_CREDENTIALS)

    def portal_ping(self):
        return self.login_client.portal_ping()

    def disconnect_cloudsdk(self):
        self.api_client.__del__()

    """
    Equipment Utilities
    """

    # Returns a List of All the Equipments that are available
    def get_equipment_by_customer_id(self, max_items=10):
        pagination_context = """{
                "model_type": "PaginationContext",
                "maxItemsPerPage": """ + str(max_items) + """
        }"""

        equipment_data = self.equipment_client.get_equipment_by_customer_id(customer_id=self.customer_id,
                                                                            pagination_context=pagination_context)
        return equipment_data._items

    def validate_equipment_availability(self, equipment_id=None):
        data = self.get_equipment_by_customer_id()
        for i in data:
            if i._id == equipment_id:
                return i._id
        return -1

    def request_ap_reboot(self):
        pass

    def request_firmware_update(self):
        pass

    def get_model_name(self, equipment_id=None):
        if equipment_id is None:
            return None
        data = self.equipment_client.get_equipment_by_id(equipment_id=equipment_id)
        return str(data._details._equipment_model)

    """
    Profile Utilities
    """

    def get_profile_by_id(self, profile_id=None):
        # print(self.profile_client.get_profile_by_id(profile_id=profile_id))
        pass

    """ 
    default templates are as follows : 
        profile_name=   TipWlan-rf/
                        Radius-Profile/
                        TipWlan-2-Radios/
                        TipWlan-3-Radios/
                        TipWlan-Cloud-Wifi/
                        Captive-Portal
    """


"""
    Library for Profile Utility, Creating Profiles and Pushing and Deleting them
"""


class ProfileUtility:
    """
       constructor for Access Point Utility library : can be used from pytest framework
                                                      to control Access Points
    """

    def __init__(self, sdk_client=None, testbed=None, customer_id=None):
        if sdk_client is None:
            sdk_client = CloudSDK(testbed=testbed, customer_id=customer_id)
        self.sdk_client = sdk_client
        self.profile_client = swagger_client.ProfileApi(api_client=self.sdk_client.api_client)
        self.profile_creation_ids = {
            "ssid": [],
            "ap": [],
            "radius": [],
            "rf": []
        }
        self.default_profiles = {}
        self.profile_ids = []

    def get_profile_by_name(self, profile_name=None):
        pagination_context = """{
                        "model_type": "PaginationContext",
                        "maxItemsPerPage": 1000
                }"""
        profiles = self.profile_client.get_profiles_by_customer_id(customer_id=self.sdk_client.customer_id,
                                                                   pagination_context=pagination_context)

        for i in profiles._items:
            if i._name == profile_name:
                return i
        return None

    def get_profile_by_id(self, profile_id=None):
        profiles = self.profile_client.get_profile_by_id(profile_id=profile_id)
        print(profiles)

    def get_default_profiles(self):
        pagination_context = """{
                "model_type": "PaginationContext",
                "maxItemsPerPage": 100
        }"""
        items = self.profile_client.get_profiles_by_customer_id(customer_id=self.sdk_client.customer_id,
                                                                pagination_context=pagination_context)

        for i in items._items:
            # print(i._name, i._id)
            if i._name == "TipWlan-Cloud-Wifi":
                self.default_profiles['ssid'] = i
            if i._name == "TipWlan-3-Radios":
                self.default_profiles['equipment_ap_3_radios'] = i
            if i._name == "TipWlan-2-Radios":
                self.default_profiles['equipment_ap_2_radios'] = i
            if i._name == "Captive-Portal":
                self.default_profiles['captive_portal'] = i
            if i._name == "Radius-Profile":
                self.default_profiles['radius'] = i
            if i._name == "TipWlan-rf":
                self.default_profiles['rf'] = i

    def delete_current_profile(self, equipment_id=None):
        equipment_data = self.sdk_client.equipment_client.get_equipment_by_id(equipment_id=equipment_id)

        data = self.profile_client.get_profile_with_children(profile_id=equipment_data._profile_id)
        delete_ids = []
        for i in data:
            if i._name == "TipWlan-rf":
                continue
            else:
                delete_ids.append(i._id)
        print(delete_ids)
        self.get_default_profiles()
        self.profile_creation_ids['ap'] = self.default_profiles['equipment_ap_3_radios']._id
        print(self.profile_creation_ids)
        self.push_profile_old_method(equipment_id=equipment_id)
        self.delete_profile(profile_id=delete_ids)

    """
        method call: used to create the rf profile and push set the parameters accordingly and update
    """

    def set_rf_profile(self, profile_data=None):
        default_profile = self.default_profiles['rf']
        # default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-rf")
        if profile_data is None:
            self.profile_creation_ids['rf'].append(default_profile._id)
        # Need to add functionality to add similar Profile and modify accordingly

    """
        method call: used to create a ssid profile with the given parameters
    """

    def create_open_ssid_profile(self, two4g=True, fiveg=True, profile_data=None):
        if profile_data is None:
            return False
        default_profile = self.default_profiles['ssid']
        # default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-Cloud-Wifi")
        default_profile._details['appliedRadios'] = []
        if two4g is True:
            default_profile._details['appliedRadios'].append("is2dot4GHz")
        if fiveg is True:
            default_profile._details['appliedRadios'].append("is5GHzU")
            default_profile._details['appliedRadios'].append("is5GHz")
            default_profile._details['appliedRadios'].append("is5GHzL")
        default_profile._name = profile_data['profile_name']
        default_profile._details['vlanId'] = profile_data['vlan']
        default_profile._details['ssid'] = profile_data['ssid_name']
        default_profile._details['forwardMode'] = profile_data['mode']
        default_profile._details['secureMode'] = 'open'
        profile_id = self.profile_client.create_profile(body=default_profile)._id
        self.profile_creation_ids['ssid'].append(profile_id)
        self.profile_ids.append(profile_id)
        return True

    def create_wpa_ssid_profile(self, two4g=True, fiveg=True, profile_data=None):
        if profile_data is None:
            return False
        default_profile = self.default_profiles['ssid']
        # default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-Cloud-Wifi")
        default_profile._details['appliedRadios'] = []
        if two4g is True:
            default_profile._details['appliedRadios'].append("is2dot4GHz")
        if fiveg is True:
            default_profile._details['appliedRadios'].append("is5GHzU")
            default_profile._details['appliedRadios'].append("is5GHz")
            default_profile._details['appliedRadios'].append("is5GHzL")
        default_profile._name = profile_data['profile_name']
        default_profile._details['vlanId'] = profile_data['vlan']
        default_profile._details['ssid'] = profile_data['ssid_name']
        default_profile._details['keyStr'] = profile_data['security_key']
        default_profile._details['forwardMode'] = profile_data['mode']
        default_profile._details['secureMode'] = 'wpaPSK'
        print(default_profile)
        profile_id = self.profile_client.create_profile(body=default_profile)._id
        self.profile_creation_ids['ssid'].append(profile_id)
        self.profile_ids.append(profile_id)
        return True

    def create_wpa2_personal_ssid_profile(self, two4g=True, fiveg=True, profile_data=None):
        if profile_data is None:
            return False
        default_profile = self.default_profiles['ssid']
        # default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-Cloud-Wifi")
        default_profile._details['appliedRadios'] = []
        if two4g is True:
            default_profile._details['appliedRadios'].append("is2dot4GHz")
        if fiveg is True:
            default_profile._details['appliedRadios'].append("is5GHzU")
            default_profile._details['appliedRadios'].append("is5GHz")
            default_profile._details['appliedRadios'].append("is5GHzL")
        default_profile._name = profile_data['profile_name']
        default_profile._details['vlanId'] = profile_data['vlan']
        default_profile._details['ssid'] = profile_data['ssid_name']
        default_profile._details['keyStr'] = profile_data['security_key']
        default_profile._details['forwardMode'] = profile_data['mode']
        default_profile._details['secureMode'] = 'wpa2OnlyPSK'
        profile_id = self.profile_client.create_profile(body=default_profile)._id
        self.profile_creation_ids['ssid'].append(profile_id)
        self.profile_ids.append(profile_id)
        # print(default_profile)
        return True

    def create_wpa3_personal_ssid_profile(self, two4g=True, fiveg=True, profile_data=None):
        if profile_data is None:
            return False
        default_profile = self.default_profiles['ssid']
        # default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-Cloud-Wifi")
        default_profile._details['appliedRadios'] = []
        if two4g is True:
            default_profile._details['appliedRadios'].append("is2dot4GHz")
        if fiveg is True:
            default_profile._details['appliedRadios'].append("is5GHzU")
            default_profile._details['appliedRadios'].append("is5GHz")
            default_profile._details['appliedRadios'].append("is5GHzL")
        default_profile._name = profile_data['profile_name']
        default_profile._details['vlanId'] = profile_data['vlan']
        default_profile._details['ssid'] = profile_data['ssid_name']
        default_profile._details['keyStr'] = profile_data['security_key']
        default_profile._details['forwardMode'] = profile_data['mode']
        default_profile._details['secureMode'] = 'wpa3OnlyPSK'
        profile_id = self.profile_client.create_profile(body=default_profile)._id
        self.profile_creation_ids['ssid'].append(profile_id)
        self.profile_ids.append(profile_id)
        return True

    def create_wpa2_enterprise_ssid_profile(self, two4g=True, fiveg=True, profile_data=None):
        if profile_data is None:
            return False
        default_profile = self.default_profiles['ssid']
        # default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-Cloud-Wifi")
        default_profile._details['appliedRadios'] = []
        if two4g is True:
            default_profile._details['appliedRadios'].append("is2dot4GHz")
        if fiveg is True:
            default_profile._details['appliedRadios'].append("is5GHzU")
            default_profile._details['appliedRadios'].append("is5GHz")
            default_profile._details['appliedRadios'].append("is5GHzL")
        default_profile._name = profile_data['profile_name']
        default_profile._details['vlanId'] = profile_data['vlan']
        default_profile._details['ssid'] = profile_data['ssid_name']
        default_profile._details['forwardMode'] = profile_data['mode']
        default_profile._details['secureMode'] = 'wpa2OnlyRadius'
        profile_id = self.profile_client.create_profile(body=default_profile)._id
        self.profile_creation_ids['ssid'].append(profile_id)
        self.profile_ids.append(profile_id)
        return True

    def create_wpa3_enterprise_ssid_profile(self, two4g=True, fiveg=True, profile_data=None):
        if profile_data is None:
            return False
        default_profile = self.default_profiles['ssid']
        # default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-Cloud-Wifi")
        default_profile._details['appliedRadios'] = []
        if two4g is True:
            default_profile._details['appliedRadios'].append("is2dot4GHz")
        if fiveg is True:
            default_profile._details['appliedRadios'].append("is5GHzU")
            default_profile._details['appliedRadios'].append("is5GHz")
            default_profile._details['appliedRadios'].append("is5GHzL")
        default_profile._name = profile_data['profile_name']
        default_profile._details['vlanId'] = profile_data['vlan']
        default_profile._details['ssid'] = profile_data['ssid_name']
        default_profile._details['keyStr'] = profile_data['security_key']
        default_profile._details['forwardMode'] = profile_data['mode']
        default_profile._details['secureMode'] = 'wpa3OnlyRadius'
        profile_id = self.profile_client.create_profile(body=default_profile)._id
        self.profile_creation_ids['ssid'].append(profile_id)
        self.profile_ids.append(profile_id)
        return True

    """
        method call: used to create a ap profile that contains the given ssid profiles
    """

    def set_ap_profile(self, profile_data=None):
        if profile_data is None:
            return False
        default_profile = self.default_profiles['equipment_ap_2_radios']
        # default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-2-Radios")
        default_profile._child_profile_ids = []
        for i in self.profile_creation_ids:
            for j in self.profile_creation_ids[i]:
                default_profile._child_profile_ids.append(j)
        # default_profile._details['radiusServiceId'] = self.profile_creation_ids['radius']
        default_profile._name = profile_data['profile_name']
        print(default_profile)
        default_profile = self.profile_client.create_profile(body=default_profile)
        self.profile_creation_ids['ap'] = default_profile._id
        self.profile_ids.append(default_profile._id)
        # print(default_profile)

    """
        method call: used to create a radius profile with the settings given
    """

    def set_radius_profile(self, radius_info=None):
        default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="Radius-Profile")
        default_profile._name = radius_info['name']
        default_profile._details['primaryRadiusAuthServer']['ipAddress'] = radius_info['ip']
        default_profile._details['primaryRadiusAuthServer']['port'] = radius_info['port']
        default_profile._details['primaryRadiusAuthServer']['secret'] = radius_info['secret']
        default_profile = self.profile_client.create_profile(body=default_profile)
        self.profile_creation_ids['radius'].append(default_profile._id)
        self.profile_ids.append(default_profile._id)

    """
        method call: used to create the ssid and psk data that can be used in creation of ssid profile
    """

    def set_ssid_psk_data(self):
        pass

    """
        method to push the profile to the given equipment 
    """

    # Under a Bug, depreciated until resolved, should be used primarily
    def push_profile(self, equipment_id=None):
        pagination_context = """{
                                "model_type": "PaginationContext",
                                "maxItemsPerPage": 100
                        }"""
        default_equipment_data = self.sdk_client.equipment_client.get_equipment_by_id(equipment_id=11, async_req=False)
        # default_equipment_data._details[] = self.profile_creation_ids['ap']
        print(default_equipment_data)
        # print(self.sdk_client.equipment_client.update_equipment(body=default_equipment_data, async_req=True))

    """
        method to verify if the expected ssid's are loaded in the ap vif config
    """

    def monitor_vif_conf(self):
        pass

    """
        method to delete a profile by its id
    """

    def delete_profile(self, profile_id=None):
        for i in profile_id:
            self.profile_client.delete_profile(profile_id=i)

    # Need to be depreciated by using push_profile method
    def push_profile_old_method(self, equipment_id=None):
        if equipment_id is None:
            return 0
        url = self.sdk_client.configuration.host + "/portal/equipment?equipmentId=" + str(equipment_id)
        payload = {}
        headers = self.sdk_client.configuration.api_key_prefix
        response = requests.request("GET", url, headers=headers, data=payload)
        equipment_info = response.json()
        equipment_info['profileId'] = self.profile_creation_ids['ap']
        url = self.sdk_client.configuration.host + "/portal/equipment"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.sdk_client.configuration.api_key_prefix['Authorization']
        }

        response = requests.request("PUT", url, headers=headers, data=json.dumps(equipment_info))


"""
    Jfrog Utility for Artifactory Management
"""


class JFrogUtility:

    def __init__(self, credentials=None):
        if credentials is None:
            exit()
        self.user = credentials["user"]
        self.password = credentials["password"]
        self.jfrog_url = "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/"
        self.build = "pending"
        ssl._create_default_https_context = ssl._create_unverified_context

    def get_latest_build(self, model=None):
        jfrog_url = self.jfrog_url + model + "/dev/"
        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()
        headers = {'Authorization': 'Basic ' + auth}

        ''' FIND THE LATEST FILE NAME'''
        # print(url)
        req = urllib.request.Request(jfrog_url, headers=headers)
        response = urllib.request.urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html, features="html.parser")
        ##find the last pending link on dev
        last_link = soup.find_all('a', href=re.compile(self.build))[-1]
        latest_file = last_link['href']
        latest_fw = latest_file.replace('.tar.gz', '')
        return latest_fw

    def get_revisions(self, model=None):
        pass


class FirmwareUtility(JFrogUtility):

    def __init__(self, sdk_client=None, jfrog_credentials=None, testbed=None, customer_id=None):
        super().__init__(credentials=jfrog_credentials)
        if sdk_client is None:
            sdk_client = CloudSDK(testbed=testbed, customer_id=customer_id)
        self.sdk_client = sdk_client
        self.firmware_client = FirmwareManagementApi(api_client=sdk_client.api_client)
        self.jfrog_client = JFrogUtility(credentials=jfrog_credentials)
        self.equipment_gateway_client = EquipmentGatewayApi(api_client=sdk_client.api_client)
    def get_current_fw_version(self, equipment_id=None):
        # Write a logic to get the currently loaded firmware on the equipment
        self.current_fw = "something"
        return self.current_fw

    def get_latest_fw_version(self, model="ecw5410"):
        # Get The equipment model

        self.latest_fw = self.get_latest_build(model=model)
        return self.latest_fw

    def upload_fw_on_cloud(self, fw_version=None, force_upload=False):
        # if fw_latest available and force upload is False -- Don't upload
        # if fw_latest available and force upload is True -- Upload
        # if fw_latest is not available -- Upload
        fw_id = self.is_fw_available(fw_version=fw_version)
        if fw_id and (force_upload is False):
            print("Force Upload :", force_upload, "  Skipping upload")
            # Don't Upload the fw
            pass
        else:
            if fw_id and (force_upload is True):
                self.firmware_client.delete_firmware_version(firmware_version_id=fw_id)
                print("Force Upload :", force_upload, "  Deleted current Image")
                time.sleep(2)
                # if force_upload is true and latest image available, then delete the image
            firmware_data = {
                "id": 0,
                "equipmentType": "AP",
                "modelId": fw_version.split("-")[0],
                "versionName": fw_version + ".tar.gz",
                "description": "ECW5410 FW VERSION TEST",
                "filename": "https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/" + fw_version.split("-")[
                    0] + "/dev/" + fw_version + ".tar.gz",
                "commit": fw_version.split("-")[5]
            }
            firmware_id = self.firmware_client.create_firmware_version(body=firmware_data)
            print("Force Upload :", force_upload, "  Uploaded Image")
            return firmware_id._id

    def upgrade_fw(self, equipment_id=None, force_upgrade=False, force_upload=False):
        if equipment_id is None:
            print("No Equipment Id Given")
            exit()
        if (force_upgrade is True) or (self.should_upgrade_ap_fw(equipment_id=equipment_id)):
            model = self.sdk_client.get_model_name(equipment_id=equipment_id).lower()
            latest_fw = self.get_latest_fw_version(model=model)
            firmware_id = self.upload_fw_on_cloud(fw_version=latest_fw, force_upload=force_upload)
            time.sleep(5)
            try:
                obj = self.equipment_gateway_client.request_firmware_update(equipment_id=equipment_id, firmware_version_id=firmware_id)
            except Exception as e:
                obj = False
            return obj
            # Write the upgrade fw logic here

    def should_upgrade_ap_fw(self, equipment_id=None):
        current_fw = self.get_current_fw_version(equipment_id=equipment_id)
        model = self.sdk_client.get_model_name(equipment_id=equipment_id).lower()
        latest_fw = self.get_latest_fw_version(model=model)
        if current_fw == latest_fw:
            return False
        else:
            return True

    def is_fw_available(self, fw_version=None):
        if fw_version is None:
            exit()
        try:
            firmware_version = self.firmware_client.get_firmware_version_by_name(
                firmware_version_name=fw_version + ".tar.gz")
            firmware_version = firmware_version._id
            print("Firmware already Available: ", firmware_version)
        except Exception as e:
            firmware_version = False
            print("firmware not available: ", firmware_version)
        return firmware_version


# from testbed_info import JFROG_CREDENTIALS
#
# sdk_client = CloudSDK(testbed="nola-ext-05", customer_id=2)
# obj = FirmwareUtility(jfrog_credentials=JFROG_CREDENTIALS, sdk_client=sdk_client)
# obj.upgrade_fw(equipment_id=7, force_upload=False, force_upgrade=False)

"""
Check the ap model
Check latest revision of a model
Check the firmware version on AP
Check if latest version is available on cloud
    if not:
        Upload to cloud
    if yes:
        continue
Upgrade the Firmware on AP
"""
