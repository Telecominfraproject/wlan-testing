# !/usr/local/lib64/python3.8
"""
    Controller Library
        1. controller_data/sdk_base_url
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
import threading


class ConfigureController:

    def __init__(self):
        self.configuration = swagger_client.Configuration()

    def set_credentials(self, controller_data=None):
        if dict(controller_data).keys().__contains__("username") and dict(controller_data).keys().__contains__(
                "password"):
            self.configuration.username = controller_data["username"]
            self.configuration.password = controller_data["password"]
            print("Login Credentials set to custom: \n user_id: %s\n password: %s\n" % (controller_data["username"],
                                                                                        controller_data["password"]))
            return True
        else:
            self.configuration.username = "support@example.com"
            self.configuration.password = "support"
            print("Login Credentials set to default: \n user_id: %s\n password: %s\n" % ("support@example.com",
                                                                                         "support"))
            return False

    def select_controller_data(self, controller_data=None):
        if dict(controller_data).keys().__contains__("url") is None:
            print("No controller_data Selected")
            exit()
        self.sdk_base_url = controller_data["url"]
        self.configuration.host = self.sdk_base_url
        print("controller_data Selected: %s\n SDK_BASE_URL: %s\n" % (controller_data["url"], self.sdk_base_url))
        return True

    def set_sdk_base_url(self, sdk_base_url=None):
        if sdk_base_url is None:
            print("URL is None")
            exit()
        self.configuration.host = sdk_base_url
        return True


"""
    Library for cloud_controller_tests generic usages, it instantiate the bearer and credentials.
    It provides the connectivity to the cloud.
    Instantiate the Object by providing the controller_data=controller_url, customer_id=2
"""


class Controller(ConfigureController):
    """
    constructor for cloud_controller_tests library
    """

    def __init__(self, controller_data=None, customer_id=None):
        super().__init__()
        self.controller_data = controller_data
        self.customer_id = customer_id
        if customer_id is None:
            self.customer_id = 2
            print("Setting to default Customer ID 2")
        #
        # Setting the Controller Client Configuration
        self.select_controller_data(controller_data=controller_data)
        self.set_credentials(controller_data=controller_data)
        self.configuration.refresh_api_key_hook = self.get_bearer_token

        # Connecting to Controller
        self.api_client = swagger_client.ApiClient(self.configuration)
        self.login_client = swagger_client.LoginApi(api_client=self.api_client)
        self.bearer = False
        self.disconnect = False
        # Token expiry in seconds
        self.token_expiry = 1000
        self.token_timestamp = time.time()
        try:

            self.bearer = self.get_bearer_token()
            # t1 = threading.Thread(target=self.refresh_instance)
            # t1.start()
            self.api_client.default_headers['Authorization'] = "Bearer " + self.bearer._access_token
            self.status_client = swagger_client.StatusApi(api_client=self.api_client)
            self.equipment_client = swagger_client.EquipmentApi(self.api_client)
            self.profile_client = swagger_client.ProfileApi(self.api_client)
            self.api_client.configuration.api_key_prefix = {
                "Authorization": "Bearer " + self.bearer._access_token
            }
            self.api_client.configuration.refresh_api_key_hook = self.refresh_instance
            self.ping_response = self.portal_ping()
            print("Portal details :: \n", self.ping_response)
        except Exception as e:
            self.bearer = False
            print(e)

        print("Connected to Controller Server")

    def get_bearer_token(self):
        request_body = {
            "userId": self.configuration.username,
            "password": self.configuration.password
        }
        return self.login_client.get_access_token(request_body)

    def refresh_instance(self):
        # Refresh token 10 seconds before it's expiry
        if time.time() - self.token_timestamp > self.token_expiry - 10:
            self.token_timestamp = time.time()
            print("Refreshing the controller API token")
            self.disconnect_Controller()
            self.api_client = swagger_client.ApiClient(self.configuration)
            self.login_client = swagger_client.LoginApi(api_client=self.api_client)
            self.bearer = self.get_bearer_token()
            self.api_client.default_headers['Authorization'] = "Bearer " + self.bearer._access_token
            self.status_client = swagger_client.StatusApi(api_client=self.api_client)
            self.equipment_client = swagger_client.EquipmentApi(self.api_client)
            self.profile_client = swagger_client.ProfileApi(self.api_client)
            self.api_client.configuration.api_key_prefix = {
                "Authorization": "Bearer " + self.bearer._access_token
            }
            self.api_client.configuration.refresh_api_key_hook = self.refresh_instance
            self.ping_response = self.portal_ping()
            print("Portal details :: \n", self.ping_response)
            if self.ping_response._application_name != 'PortalServer':
                print("Server not Reachable")
                exit()
            print("Connected to Controller Server")

    def portal_ping(self):
        self.refresh_instance()
        return self.login_client.portal_ping()

    def disconnect_Controller(self):
        self.refresh_instance()
        self.disconnect = True
        self.api_client.__del__()

    # Returns a List of All the Equipments that are available in the cloud instances
    def get_equipment_by_customer_id(self, max_items=10):
        self.refresh_instance()
        pagination_context = """{
                "model_type": "PaginationContext",
                "maxItemsPerPage": """ + str(max_items) + """
        }"""
        self.refresh_instance()
        equipment_data = self.equipment_client.get_equipment_by_customer_id(customer_id=self.customer_id,
                                                                            pagination_context=pagination_context)
        return equipment_data._items

    # check if equipment with the given equipment_id is available in cloud instance or not
    def validate_equipment_availability(self, equipment_id=None):
        self.refresh_instance()
        data = self.get_equipment_by_customer_id()
        for i in data:
            if i._id == equipment_id:
                return i._id
        return -1

    # Need to be added in future
    def request_ap_reboot(self):
        self.refresh_instance()
        pass

    # Get the equipment id, of a equipment with a serial number
    def get_equipment_id(self, serial_number=None):
        self.refresh_instance()
        equipment_data = self.get_equipment_by_customer_id(max_items=100)
        # print(len(equipment_data))
        for equipment in equipment_data:
            if equipment._serial == serial_number:
                return equipment._id

    # Get the equipment model name of a given equipment_id
    def get_model_name(self, equipment_id=None):
        self.refresh_instance()
        if equipment_id is None:
            return None
        self.refresh_instance()
        data = self.equipment_client.get_equipment_by_id(equipment_id=equipment_id)
        print(str(data._details._equipment_model))
        return str(data._details._equipment_model)

    # Needs Bug fix from swagger code generation side
    def get_ap_firmware_new_method(self, equipment_id=None):
        self.refresh_instance()
        response = self.status_client.get_status_by_customer_equipment(customer_id=self.customer_id,
                                                                       equipment_id=equipment_id)
        print(response[2])

    # Old Method, will be depreciated in future
    def get_ap_firmware_old_method(self, equipment_id=None):
        self.refresh_instance()
        url = self.configuration.host + "/portal/status/forEquipment?customerId=" + str(
            self.customer_id) + "&equipmentId=" + str(equipment_id)
        payload = {}
        headers = self.configuration.api_key_prefix
        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            status_data = response.json()
            # print(status_data)
            try:
                current_ap_fw = status_data[2]['details']['reportedSwVersion']
                # print(current_ap_fw)
                return current_ap_fw
            except Exception as e:
                print(e)
                current_ap_fw = "error"
                return e

        else:
            return False

    """
    Profile Utilities
    """

    def get_current_profile_on_equipment(self, equipment_id=None):
        self.refresh_instance()
        default_equipment_data = self.equipment_client.get_equipment_by_id(equipment_id=equipment_id, async_req=False)
        return default_equipment_data._profile_id

    # Get the ssid's that are used by the equipment
    def get_ssids_on_equipment(self, equipment_id=None):
        self.refresh_instance()
        profile_id = self.get_current_profile_on_equipment(equipment_id=equipment_id)
        all_profiles = self.profile_client.get_profile_with_children(profile_id=profile_id)
        ssid_name_list = []
        for i in all_profiles:
            if i._profile_type == "ssid":
                ssid_name_list.append(i._details['ssid'])
        return all_profiles

    # Get the child ssid profiles that are used by equipment ap profile of given profile id
    def get_ssid_profiles_from_equipment_profile(self, profile_id=None):
        self.refresh_instance()
        equipment_ap_profile = self.profile_client.get_profile_by_id(profile_id=profile_id)
        ssid_name_list = []
        child_profile_ids = equipment_ap_profile.child_profile_ids
        for i in child_profile_ids:
            profile = self.profile_client.get_profile_by_id(profile_id=i)
            if profile._profile_type == "ssid":
                ssid_name_list.append(profile._details['ssid'])
        return ssid_name_list


"""
    Library for Profile Utility, Creating Profiles and Pushing and Deleting them
    Steps to create a Profile on Controller:
        create a RF Profile
        create a Radius Profile
        create ssid profiles, and add the radius profile in them, if needed (only used by eap ssid's)

        create equipment_ap profile, and add the rf profile and ssid profiles
    Now using push profile method, equipment_ap profile will be pushed to an AP of given equipment_id

"""


class ProfileUtility:
    """
       constructor for Access Point Utility library
    """

    def __init__(self, sdk_client=None, controller_data=None, customer_id=None):
        if sdk_client is None:
            sdk_client = Controller(controller_data=controller_data, customer_id=customer_id)
        self.sdk_client = sdk_client
        self.sdk_client.refresh_instance()
        self.profile_client = swagger_client.ProfileApi(api_client=self.sdk_client.api_client)
        self.profile_creation_ids = {
            "ssid": [],
            "ap": [],
            "radius": [],
            "rf": [],
            "passpoint_osu_id_provider": [],
            "passpoint_operator": [],
            "passpoint_venue": [],
            "passpoint": []
        }
        self.profile_name_with_id = {}
        self.default_profiles = {}
        self.profile_ids = []

    def cleanup_objects(self):
        self.sdk_client.refresh_instance()
        self.profile_creation_ids = {
            "ssid": [],
            "ap": [],
            "radius": [],
            "rf": [],
            "passpoint_osu_id_provider": [],
            "passpoint_operator": [],
            "passpoint_venue": [],
            "passpoint": []
        }
        self.profile_name_with_id = {}
        self.default_profiles = {}
        self.profile_ids = []

    def get_profile_by_name(self, profile_name=None):
        self.sdk_client.refresh_instance()
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

    def get_ssid_name_by_profile_id(self, profile_id=None):
        self.sdk_client.refresh_instance()
        profiles = self.profile_client.get_profile_by_id(profile_id=profile_id)
        return profiles._details["ssid"]

    """ 
    default templates are as follows : 
        profile_name=   TipWlan-rf/
                        Radius-Profile/
                        TipWlan-2-Radios/
                        TipWlan-3-Radios/
                        TipWlan-Cloud-Wifi/
                        Captive-Portal
    """

    def get_default_profiles(self):
        pagination_context = """{
                "model_type": "PaginationContext",
                "maxItemsPerPage": 100
        }"""
        self.sdk_client.refresh_instance()
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
                # print(i)

    # This will delete the Profiles associated with an equipment of givwn equipment_id, and associate it to default
    # equipment_ap profile
    def delete_current_profile(self, equipment_id=None):
        self.sdk_client.refresh_instance()
        equipment_data = self.sdk_client.equipment_client.get_equipment_by_id(equipment_id=equipment_id)

        data = self.profile_client.get_profile_with_children(profile_id=equipment_data._profile_id)
        delete_ids = []
        for i in data:
            if i._name == "TipWlan-rf":
                continue
            else:
                delete_ids.append(i._id)
        # print(delete_ids)
        self.get_default_profiles()
        self.profile_creation_ids['ap'] = self.default_profiles['equipment_ap_3_radios']._id
        # print(self.profile_creation_ids)
        self.push_profile_old_method(equipment_id=equipment_id)
        self.delete_profile(profile_id=delete_ids)

    # This will delete all the profiles on an controller instance, except the default profiles
    def cleanup_profiles(self):
        self.sdk_client.refresh_instance()
        try:
            self.get_default_profiles()
            pagination_context = """{
                            "model_type": "PaginationContext",
                            "maxItemsPerPage": 10000
                    }"""
            skip_delete_id = []
            for i in self.default_profiles:
                skip_delete_id.append(self.default_profiles[i]._id)

            all_profiles = self.profile_client.get_profiles_by_customer_id(customer_id=self.sdk_client.customer_id,
                                                                           pagination_context=pagination_context)

            delete_ids = []
            for i in all_profiles._items:
                delete_ids.append(i._id)
            skip_delete_id = []
            for i in self.default_profiles:
                skip_delete_id.append(self.default_profiles[i]._id)
            delete_ids = list(set(delete_ids) - set(delete_ids).intersection(set(skip_delete_id)))
            print(delete_ids)
            for i in delete_ids:
                self.set_equipment_to_profile(profile_id=i)
            self.delete_profile(profile_id=delete_ids)
            status = True
        except Exception as e:
            print(e)
            status = False
        return status

    # Delete any profile with the given name
    def delete_profile_by_name(self, profile_name=None):
        self.sdk_client.refresh_instance()
        pagination_context = """{
                                                "model_type": "PaginationContext",
                                                "maxItemsPerPage": 5000
                                        }"""
        all_profiles = self.profile_client.get_profiles_by_customer_id(customer_id=self.sdk_client.customer_id,
                                                                       pagination_context=pagination_context)
        for i in all_profiles._items:
            if i._name == profile_name:
                counts = self.profile_client.get_counts_of_equipment_that_use_profiles([i._id])[0]
                if counts._value2:
                    self.set_equipment_to_profile(profile_id=i._id)
                    self.delete_profile(profile_id=[i._id])
                else:
                    self.delete_profile(profile_id=[i._id])

    # This method will set all the equipments to default equipment_ap profile, those having the profile_id passed in
    # argument
    def set_equipment_to_profile(self, profile_id=None):
        self.sdk_client.refresh_instance()
        pagination_context = """{
                                                "model_type": "PaginationContext",
                                                "maxItemsPerPage": 5000
                                        }"""
        equipment_data = self.sdk_client.equipment_client. \
            get_equipment_by_customer_id(customer_id=2,
                                         pagination_context=pagination_context)
        self.get_default_profiles()
        for i in equipment_data._items:
            if i._profile_id == profile_id:
                self.profile_creation_ids['ap'] = self.default_profiles['equipment_ap_2_radios']._id
                self.push_profile_old_method(equipment_id=i._id)
                time.sleep(2)

    """ 
        method call: used to create the rf profile and push set the parameters accordingly and update
        Library method to create a new rf profile: Now using default profile
    """

    def set_rf_profile(self, profile_data=None, mode=None):
        self.sdk_client.refresh_instance()
        self.get_default_profiles()
        if mode == "wifi5":
            default_profile = self.default_profiles['rf']
            default_profile._name = profile_data["name"]

            default_profile._details["rfConfigMap"]["is2dot4GHz"]["rf"] = profile_data["name"]
            default_profile._details["rfConfigMap"]["is5GHz"]["rf"] = profile_data["name"]
            default_profile._details["rfConfigMap"]["is5GHzL"]["rf"] = profile_data["name"]
            default_profile._details["rfConfigMap"]["is5GHzU"]["rf"] = profile_data["name"]
            for i in default_profile._details["rfConfigMap"]:
                for j in profile_data:
                    if i == j:
                        for k in default_profile._details["rfConfigMap"][i]:
                            for l in profile_data[j]:
                                if l == k:
                                    default_profile._details["rfConfigMap"][i][l] = profile_data[j][l]
            profile = self.profile_client.create_profile(body=default_profile)
            self.profile_creation_ids['rf'].append(profile._id)
            return profile
        if mode == "wifi6":
            default_profile = self.default_profiles['rf']
            default_profile._name = profile_data["name"]
            default_profile._details["rfConfigMap"]["is2dot4GHz"]["activeScanSettings"]["enabled"] = False
            default_profile._details["rfConfigMap"]["is2dot4GHz"]["radioMode"] = 'modeAX'
            default_profile._details["rfConfigMap"]["is5GHz"]["radioMode"] = 'modeAX'
            default_profile._details["rfConfigMap"]["is5GHzL"]["radioMode"] = 'modeAX'
            default_profile._details["rfConfigMap"]["is5GHzU"]["radioMode"] = 'modeAX'
            default_profile._details["rfConfigMap"]["is2dot4GHz"]["rf"] = profile_data["name"]
            default_profile._details["rfConfigMap"]["is5GHz"]["rf"] = profile_data["name"]
            default_profile._details["rfConfigMap"]["is5GHzL"]["rf"] = profile_data["name"]
            default_profile._details["rfConfigMap"]["is5GHzU"]["rf"] = profile_data["name"]
            default_profile._name = profile_data["name"]
            for i in default_profile._details["rfConfigMap"]:
                for j in profile_data:
                    if i == j:
                        for k in default_profile._details["rfConfigMap"][i]:
                            for l in profile_data[j]:
                                if l == k:
                                    default_profile._details["rfConfigMap"][i][l] = profile_data[j][l]
            profile = self.profile_client.create_profile(body=default_profile)
            self.profile_creation_ids['rf'].append(profile._id)
            return profile

    """
        method call: used to create a ssid profile with the given parameters
    """

    # Open
    def create_open_ssid_profile(self, profile_data=None):
        self.sdk_client.refresh_instance()
        try:
            if profile_data is None:
                return False
            default_profile = self.default_profiles['ssid']
            default_profile._details['appliedRadios'] = profile_data["appliedRadios"]

            default_profile._name = profile_data['profile_name']
            default_profile._details['ssid'] = profile_data['ssid_name']
            default_profile._details['vlanId'] = profile_data['vlan']
            default_profile._details['forwardMode'] = profile_data['mode']
            default_profile._details['secureMode'] = 'open'
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids['ssid'].append(profile_id)
            self.profile_ids.append(profile_id)
            self.profile_name_with_id[profile_data["ssid_name"]] = profile_id
        except Exception as e:
            print(e)
            profile = "error"

        return profile

    # wpa personal
    def create_wpa_ssid_profile(self, profile_data=None):
        self.sdk_client.refresh_instance()
        self.get_default_profiles()
        try:
            if profile_data is None:
                return False
            default_profile = self.default_profiles['ssid']
            default_profile._details['appliedRadios'] = profile_data["appliedRadios"]
            default_profile._name = profile_data['profile_name']
            default_profile._details['vlanId'] = profile_data['vlan']
            default_profile._details['ssid'] = profile_data['ssid_name']
            default_profile._details['keyStr'] = profile_data['security_key']
            default_profile._details['forwardMode'] = profile_data['mode']
            default_profile._details['secureMode'] = 'wpaPSK'
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids['ssid'].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            print(e)
            profile = False
        return profile

    # wpa2 personal
    def create_wpa2_personal_ssid_profile(self, profile_data=None):
        self.sdk_client.refresh_instance()
        try:
            if profile_data is None:
                return False
            default_profile = self.default_profiles['ssid']
            default_profile._details['appliedRadios'] = profile_data["appliedRadios"]

            default_profile._name = profile_data['profile_name']
            default_profile._details['vlanId'] = profile_data['vlan']
            default_profile._details['ssid'] = profile_data['ssid_name']
            default_profile._details['keyStr'] = profile_data['security_key']
            default_profile._details['forwardMode'] = profile_data['mode']
            default_profile._details['secureMode'] = 'wpa2OnlyPSK'
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids['ssid'].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            print(e)
            profile = False
        return profile

    # wpa3 personal
    def create_wpa3_personal_ssid_profile(self, profile_data=None):
        self.sdk_client.refresh_instance()
        try:
            if profile_data is None:
                return False
            default_profile = self.default_profiles['ssid']
            default_profile._details['appliedRadios'] = profile_data["appliedRadios"]

            default_profile._name = profile_data['profile_name']
            default_profile._details['vlanId'] = profile_data['vlan']
            default_profile._details['ssid'] = profile_data['ssid_name']
            default_profile._details['keyStr'] = profile_data['security_key']
            default_profile._details['forwardMode'] = profile_data['mode']
            default_profile._details['secureMode'] = 'wpa3OnlySAE'
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids['ssid'].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            print(e)
            profile = False
        return profile

    # wpa3 personal mixed mode
    def create_wpa3_personal_mixed_ssid_profile(self, profile_data=None):
        self.sdk_client.refresh_instance()
        try:
            if profile_data is None:
                return False
            default_profile = self.default_profiles['ssid']
            default_profile._details['appliedRadios'] = profile_data["appliedRadios"]

            default_profile._name = profile_data['profile_name']
            default_profile._details['vlanId'] = profile_data['vlan']
            default_profile._details['ssid'] = profile_data['ssid_name']
            default_profile._details['keyStr'] = profile_data['security_key']
            default_profile._details['forwardMode'] = profile_data['mode']
            default_profile._details['secureMode'] = 'wpa3MixedSAE'
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids['ssid'].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            print(e)
            profile = False
        return profile

    # wpa wpa2 personal mixed mode
    def create_wpa_wpa2_personal_mixed_ssid_profile(self, profile_data=None):
        self.sdk_client.refresh_instance()
        try:
            if profile_data is None:
                return False
            default_profile = self.default_profiles['ssid']
            default_profile._details['appliedRadios'] = profile_data["appliedRadios"]

            default_profile._name = profile_data['profile_name']
            default_profile._details['vlanId'] = profile_data['vlan']
            default_profile._details['ssid'] = profile_data['ssid_name']
            default_profile._details['keyStr'] = profile_data['security_key']
            default_profile._details['forwardMode'] = profile_data['mode']
            default_profile._details['secureMode'] = 'wpa2PSK'
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids['ssid'].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            print(e)
            profile = False
        return profile

    # wpa enterprise    done
    def create_wpa_enterprise_ssid_profile(self, profile_data=None):
        self.sdk_client.refresh_instance()
        try:
            if profile_data is None:
                return False
            default_profile = self.default_profiles['ssid']
            default_profile._details['appliedRadios'] = profile_data["appliedRadios"]
            default_profile._name = profile_data['profile_name']
            default_profile._details['vlanId'] = profile_data['vlan']
            default_profile._details['ssid'] = profile_data['ssid_name']
            default_profile._details['forwardMode'] = profile_data['mode']
            default_profile._details["radiusServiceId"] = self.profile_creation_ids["radius"][0]
            default_profile._child_profile_ids = self.profile_creation_ids["radius"]
            default_profile._details['secureMode'] = 'wpaRadius'
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids['ssid'].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            print(e)
            profile = False
        return profile

    # wpa wpa2 enterprise mixed mode done
    def create_wpa_wpa2_enterprise_mixed_ssid_profile(self, profile_data=None):
        self.sdk_client.refresh_instance()
        try:
            if profile_data is None:
                return False
            default_profile = self.default_profiles['ssid']
            default_profile._details['appliedRadios'] = profile_data["appliedRadios"]

            default_profile._name = profile_data['profile_name']
            default_profile._details['vlanId'] = profile_data['vlan']
            default_profile._details['ssid'] = profile_data['ssid_name']
            default_profile._details['forwardMode'] = profile_data['mode']
            default_profile._details["radiusServiceId"] = self.profile_creation_ids["radius"][0]
            default_profile._child_profile_ids = self.profile_creation_ids["radius"]
            default_profile._details['secureMode'] = 'wpa2Radius'
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids['ssid'].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            print(e)
            profile = False
        return profile

    # wpa2 enterprise mode ssid profile
    def create_wpa2_enterprise_ssid_profile(self, profile_data=None):
        self.sdk_client.refresh_instance()
        try:
            if profile_data is None:
                return False
            default_profile = self.default_profiles['ssid']
            default_profile._details['appliedRadios'] = profile_data["appliedRadios"]

            default_profile._name = profile_data['profile_name']
            default_profile._details['vlanId'] = profile_data['vlan']
            default_profile._details['ssid'] = profile_data['ssid_name']
            default_profile._details['forwardMode'] = profile_data['mode']
            default_profile._details["radiusServiceId"] = self.profile_creation_ids["radius"][0]
            default_profile._child_profile_ids = self.profile_creation_ids["radius"]
            default_profile._details['secureMode'] = 'wpa2OnlyRadius'
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids['ssid'].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            print(e)
            profile = False
        return profile

    # wpa3 enterprise mode
    def create_wpa3_enterprise_ssid_profile(self, profile_data=None):
        self.sdk_client.refresh_instance()
        try:
            if profile_data is None:
                return False
            default_profile = self.default_profiles['ssid']
            default_profile._details['appliedRadios'] = profile_data["appliedRadios"]
            default_profile._name = profile_data['profile_name']
            default_profile._details['vlanId'] = profile_data['vlan']
            default_profile._details['ssid'] = profile_data['ssid_name']
            default_profile._details['forwardMode'] = profile_data['mode']
            default_profile._details["radiusServiceId"] = self.profile_creation_ids["radius"][0]
            default_profile._child_profile_ids = self.profile_creation_ids["radius"]
            default_profile._details['secureMode'] = 'wpa3OnlyEAP'
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids['ssid'].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            print(e)
            profile = False
        return profile

    # wpa3 enterprise mixed mode done
    def create_wpa3_enterprise_mixed_ssid_profile(self, profile_data=None):
        self.sdk_client.refresh_instance()
        try:
            if profile_data is None:
                return False
            default_profile = self.default_profiles['ssid']
            default_profile._details['appliedRadios'] = profile_data["appliedRadios"]
            default_profile._name = profile_data['profile_name']
            default_profile._details['vlanId'] = profile_data['vlan']
            default_profile._details['ssid'] = profile_data['ssid_name']
            default_profile._details['forwardMode'] = profile_data['mode']
            default_profile._details["radiusServiceId"] = self.profile_creation_ids["radius"][0]
            default_profile._child_profile_ids = self.profile_creation_ids["radius"]
            default_profile._details['secureMode'] = 'wpa3MixedEAP'
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids['ssid'].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            print(e)
            profile = False
        return profile

    # wpa3 enterprise mixed mode done
    def create_wep_ssid_profile(self, profile_data=None):
        self.sdk_client.refresh_instance()
        try:
            if profile_data is None:
                return False
            default_profile = self.default_profiles['ssid']
            default_profile._details['appliedRadios'] = profile_data["appliedRadios"]
            default_profile._name = profile_data['profile_name']
            default_profile._details['vlanId'] = profile_data['vlan']
            default_profile._details['ssid'] = profile_data['ssid_name']
            default_profile._details['forwardMode'] = profile_data['mode']
            default_profile._details['secureMode'] = 'wep'
            default_profile._details['wepConfig'] = {}
            default_profile._details['wepConfig']["model_type"] = "WepConfiguration"
            default_profile._details['wepConfig']["wepAuthType"] = "open"
            default_profile._details['wepConfig']["primaryTxKeyId"] = profile_data["default_key_id"]
            default_profile._details['wepConfig']["wepKeys"] = [{'model_type': 'WepKey',
                                                                 'txKey': profile_data["wep_key"],
                                                                 'txKeyConverted': None,
                                                                 'txKeyType': 'wep64'},
                                                                {'model_type': 'WepKey',
                                                                 'txKey': profile_data["wep_key"],
                                                                 'txKeyConverted': None,
                                                                 'txKeyType': 'wep64'},
                                                                {'model_type': 'WepKey',
                                                                 'txKey': profile_data["wep_key"],
                                                                 'txKeyConverted': None,
                                                                 'txKeyType': 'wep64'},
                                                                {'model_type': 'WepKey',
                                                                 'txKey': profile_data["wep_key"],
                                                                 'txKeyConverted': None,
                                                                 'txKeyType': 'wep64'}]
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids['ssid'].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            print(e)
            profile = False
        return profile

    def __get_boolean(self, flag):
        return 'true' if flag in ["Enabled", "True"] else 'false'

    # wpa eap general method
    def __create_wpa_eap_passpoint_ssid_profiles(self, profile_data=None, secure_mode=None):
        try:
            if profile_data is None or secure_mode is None:
                return False
            default_profile = self.default_profiles["ssid"]
            default_profile._details["appliedRadios"] = profile_data["appliedRadios"]
            default_profile._name = profile_data["profile_name"]
            default_profile._details["vlanId"] = profile_data["vlan"]
            default_profile._details["ssid"] = profile_data["ssid_name"]
            default_profile._details["forwardMode"] = profile_data["mode"]
            default_profile._details["radiusServiceId"] = self.profile_creation_ids["radius"][0]
            default_profile._child_profile_ids = self.profile_creation_ids["radius"]
            default_profile._details["secureMode"] = secure_mode
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids["ssid"].append(profile_id)
            self.profile_ids.append(profile_id)
            self.profile_name_with_id[profile_data["ssid_name"]] = profile_id
        except Exception as e:
            print(e)
            profile = False
        return profile

    # wpa eap passpoint
    def create_wpa_eap_passpoint_ssid_profile(self, profile_data=None):
        if profile_data is None:
            return False
        return self.__create_wpa_eap_passpoint_ssid_profiles(profile_data, "wpaEAP")

    # wpa2 eap passpoint
    def create_wpa2_eap_passpoint_ssid_profile(self, profile_data=None):
        if profile_data is None:
            return False
        return self.__create_wpa_eap_passpoint_ssid_profiles(profile_data, "wpa2EAP")

    # wpa2only eap passpoint
    def create_wpa2_only_eap_passpoint_ssid_profile(self, profile_data=None):
        if profile_data is None:
            return False
        return self.__create_wpa_eap_passpoint_ssid_profiles(profile_data, "wpa2OnlyEAP")

    # passpoint osu id provider profile
    def create_passpoint_osu_id_provider_profile(self, profile_data=None):
        try:
            if profile_data is None:
                return False
            default_profile = dict()
            default_profile["model_type"] = "Profile"
            default_profile["customerId"] = self.sdk_client.customer_id
            default_profile["profileType"] = "passpoint_osu_id_provider"
            default_profile["name"] = profile_data["profile_name"]
            details = dict()
            details["model_type"] = "PasspointOsuProviderProfile"
            mcc_mnc = dict()
            if (profile_data["mcc"] and profile_data["mnc"]) is not None:
                mcc_mnc = {"mcc": profile_data["mcc"], "mnc": profile_data["mnc"]}
            if profile_data["network"] is not None:
                mcc_mnc["network"] = profile_data["network"]
            if mcc_mnc:
                details["mccMncList"] = [mcc_mnc]
            if (profile_data["mcc"] and profile_data["mnc"]) is not None:
                details["mccMncList"] = [{"mcc": profile_data["mcc"], "mnc": profile_data["mnc"]}]
            if profile_data["osu_nai_standalone"] is not None:
                details["osuNaiStandalone"] = profile_data["osu_nai_standalone"]
            if profile_data["osu_nai_shared"] is not None:
                details["osuNaiShared"] = profile_data["osu_nai_shared"]
            if profile_data["nai_realms"] is not None:
                details["naiRealmList"] = [{"naiRealms": [profile_data["nai_realms"]["domain"]],
                                            "encoding": profile_data["nai_realms"]["encoding"],
                                            "eapMap": profile_data["nai_realms"]["eap_map"]
                                            }]
            details["roamingOi"] = profile_data["roaming_oi"]
            default_profile['details'] = details
            default_profile['childProfileIds'] = []
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids["passpoint_osu_id_provider"].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            print(e)
            profile = False
        return profile

    # passpoint operator profile
    def create_passpoint_operator_profile(self, profile_data=None):
        try:
            if profile_data is None:
                return False
            default_profile = dict()
            default_profile["model_type"] = "Profile"
            default_profile["customerId"] = self.sdk_client.customer_id
            default_profile["profileType"] = "passpoint_operator"
            default_profile["name"] = profile_data["profile_name"]

            default_profile["details"] = dict()
            default_profile["details"]["model_type"] = "PasspointOperatorProfile"
            default_profile["details"]["serverOnlyAuthenticatedL2EncryptionNetwork"] = \
                self.__get_boolean(profile_data["osen"])
            operator_names = []
            operators = profile_data["operator_names"]
            for operator in profile_data["operator_names"]:
                operator_temp = dict()
                for key in operator.keys():
                    if key == "name":
                        operator_temp["dupleName"] = operator["name"]
                    else:
                        operator_temp[key] = operator[key]
                operator_names.append(operator_temp)
            default_profile["details"]["operatorFriendlyName"] = operator_names
            default_profile["details"]["domainNameList"] = profile_data["domain_name_list"]
            default_profile["childProfileIds"] = []
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids["passpoint_operator"].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            profile = False
        return profile

    # passpoint venue profile
    def create_passpoint_venue_profile(self, profile_data=None):
        try:
            if profile_data is None:
                return False
            default_profile = dict()
            default_profile["model_type"] = "Profile"
            default_profile["customerId"] = self.sdk_client.customer_id
            default_profile["profileType"] = "passpoint_venue"
            default_profile["name"] = profile_data["profile_name"]
            default_profile["details"] = dict()
            default_profile["details"]["model_type"] = "PasspointVenueProfile"
            venue_names = []
            for venue in profile_data["venue_names"]:
                venue_temp = dict()
                for key in venue.keys():
                    if key == "name":
                        venue_temp["dupleName"] = venue["name"]
                    if key == "url":
                        venue_temp["venueUrl"] = venue["url"]
                venue_names.append(venue_temp)
            default_profile["details"]["venueNameSet"] = venue_names
            allowed_venue_groups = {"Unspecified": 0, "Assembly": 1, "Business": 2, "Educational": 3,
                                    "Factory and Industrial": 4, "Institutional": 5, "Mercantile": 6, "Residential": 7}
            allowed_venue_types = {"Unspecified Assembly": 0, "Areana": 1, "Stadium": 2, "Passenger Terminal": 3,
                                   "Amphitheatre": 4, "Amusement Park": 5, "Place of Worship": 6,
                                   "Convention Center": 7,
                                   "Library": 8, "Museum": 9, "Restaurant": 10, "Theatre": 11, "Bar": 12,
                                   "Coffee Shop": 13,
                                   "Zoo or Aquarium": 14, "Emergency Coordination Center": 15,
                                   "Unspecified Business": 0, "Doctor or Dentist office": 1, "Bank": 2,
                                   "Fire Station": 3,
                                   "Police Station": 4, "Post Office": 5, "Professional Office": 6,
                                   "Research and Development Facility": 7, "Attorney Office": 8,
                                   "Unspecified Educational": 0, "School, Primary": 1, "School, Secondary": 2,
                                   "University or College": 3, "Unspecified Factory and Industrial": 0, "Factory": 1,
                                   "Unspecified Institutional": 0, "Hospital": 1, "Long-Term Care Facility": 2,
                                   "Alcohol and Drug Re-habilitation Center": 3, "Group Home": 4, "Prison or Jail": 5,
                                   "Unspecified Mercantile": 0, "Retail Store": 1, "Grocery Market": 2,
                                   "Automotive Service Station": 3, "Shopping Mall": 4, "Gas Station": 5,
                                   "Unspecified Residential": 0, "Pivate Residence": 1, "Hotel or Model": 2,
                                   "Dormitory": 3, "Boarding House": 4}
            default_profile["details"]["venueTypeAssignment"] = {"venueGroupId":
                                                                     allowed_venue_groups[
                                                                         profile_data["venue_type"]["group"]],
                                                                 "venueTypeId":
                                                                     allowed_venue_types[
                                                                         profile_data["venue_type"]["type"]]}
            default_profile["childProfileIds"] = []
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids["passpoint_venue"].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            print(e)
            profile = False
        return profile

    # passpoint profile
    def create_passpoint_profile(self, profile_data=None):
        try:
            if profile_data is None:
                return False
            default_profile = dict()
            default_profile["model_type"] = "Profile"
            default_profile["customerId"] = self.sdk_client.customer_id
            default_profile["profileType"] = "passpoint"
            default_profile["name"] = profile_data["profile_name"]

            default_profile["details"] = dict()
            default_profile["details"]["model_type"] = "PasspointProfile"
            default_profile["details"]["enableInterworkingAndHs20"] = self.__get_boolean(
                profile_data["interworking_hs2dot0"])
            if profile_data["hessid"] is not None:
                default_profile["details"]["hessid"] = dict()
                default_profile["details"]["hessid"]["addressAsString"] = profile_data["hessid"]
            default_profile["details"]["passpointAccessNetworkType"] = \
                profile_data["access_network"]["Access Network Type"].replace(' ', '_').lower()
            default_profile["details"]["passpointNetworkAuthenticationType"] = \
                profile_data["access_network"]["Authentication Type"].replace('&', 'and').replace(' ', '_').lower()
            default_profile["details"]["emergencyServicesReachable"] = self.__get_boolean(
                profile_data["access_network"][
                    "Emergency Services Reachable"])
            default_profile["details"]["unauthenticatedEmergencyServiceAccessible"] = self.__get_boolean(
                profile_data["access_network"][
                    "Unauthenticated Emergency Service"])
            default_profile["details"]["internetConnectivity"] = self.__get_boolean(profile_data["ip_connectivity"][
                                                                                        "Internet Connectivity"])
            capability_set = []
            for cap in profile_data["ip_connectivity"]["Connection Capability"]:
                capability_info = dict()
                capability_info["connectionCapabilitiesPortNumber"] = cap["port"]
                capability_info["connectionCapabilitiesIpProtocol"] = cap["protocol"]
                capability_info["connectionCapabilitiesStatus"] = cap["status"]
                capability_set.append(capability_info)
            default_profile["details"]["connectionCapabilitySet"] = capability_set
            default_profile["details"]["ipAddressTypeAvailability"] = profile_data["ip_connectivity"]["IP Address Type"]
            allowed_gas_address_behavior = {"P2P Spec Workaround From Request": "p2pSpecWorkaroundFromRequest",
                                            "forceNonCompliantBehaviourFromRequest": "forceNonCompliantBehaviourFromRequest",
                                            "IEEE 80211 Standard Compliant Only": "ieee80211StandardCompliantOnly"}
            default_profile["details"]["gasAddr3Behaviour"] = allowed_gas_address_behavior[
                profile_data["ip_connectivity"]
                ["GAS Address 3 Behaviour"]]
            default_profile["details"]["anqpDomainId"] = profile_data["ip_connectivity"]["ANQP Domain ID"]
            default_profile["details"]["disableDownstreamGroupAddressedForwarding"] = self.__get_boolean(
                profile_data["ip_connectivity"][
                    "Disable DGAF"])
            default_profile["details"]["associatedAccessSsidProfileIds"] = profile_data["allowed_ssids"]
            default_profile["details"]["passpointOperatorProfileId"] = self.profile_creation_ids["passpoint_operator"][0]
            default_profile["details"]["passpointVenueProfileId"] = self.profile_creation_ids["passpoint_venue"][0]
            default_profile["details"]["passpointOsuProviderProfileIds"] = self.profile_creation_ids[
                "passpoint_osu_id_provider"]
            default_profile["details"]["accessNetworkType"] = \
                profile_data["access_network"]["Access Network Type"].replace(' ', '_').lower()
            # osuSsidProfileId is needed for R2
            default_profile["details"]["networkAuthenticationType"] = \
                profile_data["access_network"]["Authentication Type"].replace('&', 'and').replace(' ', '_').lower()
            default_profile["childProfileIds"] = self.profile_creation_ids["passpoint_venue"] + \
                                                 self.profile_creation_ids["passpoint_operator"] + \
                                                 self.profile_creation_ids["passpoint_osu_id_provider"]
            profile = self.profile_client.create_profile(body=default_profile)
            profile_id = profile._id
            self.profile_creation_ids["passpoint"].append(profile_id)
            self.profile_ids.append(profile_id)
        except Exception as e:
            print(e)
            profile = False
        return profile

    """
        method call: used to create a ap profile that contains the given ssid profiles
    """

    def set_ap_profile(self, profile_data=None):
        self.sdk_client.refresh_instance()
        if profile_data is None:
            return False
        default_profile = self.default_profiles['equipment_ap_2_radios']
        default_profile._child_profile_ids = []
        for i in self.profile_creation_ids:
            if i not in ["ap", "passpoint_osu_id_provider", "passpoint_operator", "passpoint_venue", "passpoint",
                         "radius"]:
                for j in self.profile_creation_ids[i]:
                    default_profile._child_profile_ids.append(j)

        default_profile._name = profile_data['profile_name']
        # print(default_profile)
        default_profile = self.profile_client.create_profile(body=default_profile)
        self.profile_creation_ids['ap'] = default_profile._id
        self.profile_ids.append(default_profile._id)
        return default_profile

    """
        method call: used to create a ap profile that contains the given ssid profiles
    """

    def set_ap_profile_custom(self, profile_data=None):
        self.sdk_client.refresh_instance()
        if profile_data is None:
            return False
        default_profile = self.default_profiles['equipment_ap_2_radios']
        default_profile._child_profile_ids = []
        for i in self.profile_creation_ids:
            if i not in ["ap", "passpoint_osu_id_provider", "passpoint_operator", "passpoint_venue", "passpoint",
                         "radius", "ssid"]:
                for j in self.profile_creation_ids[i]:
                    default_profile._child_profile_ids.append(j)
        for ssid in profile_data["ssid_names"]:
            default_profile._child_profile_ids.append(self.profile_name_with_id[ssid])
        default_profile._name = profile_data['profile_name']
        default_profile = self.profile_client.create_profile(body=default_profile)
        self.profile_creation_ids['ap'] = default_profile._id
        self.profile_ids.append(default_profile._id)
        return default_profile

    """
        method call: used to create a ap profile that contains the specific ssid profiles
    """

    def update_ap_profile(self, profile_data=None):
        self.sdk_client.refresh_instance()
        if profile_data is None:
            print("profile info is None, Please specify the profile info that you want to update")
            return False

        child_profiles_to_apply = []
        try:
            for ssid in profile_data["ssid_names"]:
                child_profiles_to_apply.append(self.profile_name_with_id[ssid])
            default_profile = self.get_profile_by_name(profile_name=profile_data["profile_name"])
            for i in self.profile_creation_ids:
                if i not in ["ap", "passpoint_osu_id_provider", "passpoint_operator", "passpoint_venue", "passpoint",
                             "radius", "ssid"]:
                    for j in self.profile_creation_ids[i]:
                        child_profiles_to_apply.append(j)
            default_profile._child_profile_ids = child_profiles_to_apply
            default_profile = self.profile_client.update_profile(default_profile)
            return True
        except Exception as e:
            print(e)
            return False

    """
        method call: used to create a radius profile with the settings given
    """

    def create_radius_profile(self, radius_info=None, radius_accounting_info=None):
        self.sdk_client.refresh_instance()
        default_profile = self.default_profiles['radius']
        default_profile._name = radius_info['name']
        default_profile._details['primaryRadiusAuthServer'] = {}
        default_profile._details['primaryRadiusAuthServer']['ipAddress'] = radius_info['ip']
        default_profile._details['primaryRadiusAuthServer']['port'] = radius_info['port']
        default_profile._details['primaryRadiusAuthServer']['secret'] = radius_info['secret']
        if radius_accounting_info is not None:
            default_profile._details["primaryRadiusAccountingServer"] = {}
            default_profile._details["primaryRadiusAccountingServer"]["ipAddress"] = radius_accounting_info["ip"]
            default_profile._details["primaryRadiusAccountingServer"]["port"] = radius_accounting_info["port"]
            default_profile._details["primaryRadiusAccountingServer"]["secret"] = radius_accounting_info["secret"]
        default_profile = self.profile_client.create_profile(body=default_profile)
        self.profile_creation_ids['radius'] = [default_profile._id]
        self.profile_ids.append(default_profile._id)
        return default_profile

    """
        method to push the profile to the given equipment 
    """

    # Under a Bug, depreciated until resolved, should be used primarily
    def push_profile(self, equipment_id=None):
        self.sdk_client.refresh_instance()
        pagination_context = """{
                                "model_type": "PaginationContext",
                                "maxItemsPerPage": 100
                        }"""
        default_equipment_data = self.sdk_client.equipment_client.get_equipment_by_id(equipment_id=11, async_req=False)
        # default_equipment_data._details[] = self.profile_creation_ids['ap']
        # print(default_equipment_data)
        # print(self.sdk_client.equipment_client.update_equipment(body=default_equipment_data, async_req=True))

    """
        method to verify if the expected ssid's are loaded in the ap vif config
    """

    def update_ssid_name(self, profile_name=None, new_profile_name=None):
        self.sdk_client.refresh_instance()
        if profile_name is None:
            print("profile name is None, Please specify the ssid profile name that you want to modify")
            return False
        if new_profile_name is None:
            print("Please specify the new name for ssid profile that you want to make to")
            return False

        try:
            profile = self.get_profile_by_name(profile_name=profile_name)
            profile._details['ssid'] = new_profile_name
            self.profile_client.update_profile(profile)
            return True
        except Exception as e:
            return False

    def update_ssid_profile(self, profile_info=None):
        self.sdk_client.refresh_instance()
        if profile_info is None:
            print("profile info is None, Please specify the profile info that you want to update")
            return False

        try:
            profile = self.get_profile_by_name(profile_name=profile_info["ssid_profile_name"])
            profile._details["radiusServiceId"] = self.profile_creation_ids["radius"][0]
            profile._child_profile_ids = self.profile_creation_ids["radius"] + self.profile_creation_ids["passpoint"]
            if "radius_configuration" in profile_info.keys():
                if "radius_acounting_service_interval" in profile_info["radius_configuration"].keys():
                    profile._details["radiusAcountingServiceInterval"] = profile_info["radius_configuration"]["radius_acounting_service_interval"]
                if "user_defined_nas_id" in profile_info["radius_configuration"].keys():
                    profile._details["radiusClientConfiguration"]["userDefinedNasId"] = profile_info["radius_configuration"]["user_defined_nas_id"]
                if "operator_id" in profile_info["radius_configuration"].keys():
                    profile._details["radiusClientConfiguration"]["operatorId"] = profile_info["radius_configuration"]["operator_id"]
            self.profile_client.update_profile(profile)
            return True
        except Exception as e:
            print(e)
            return False

    def clear_ssid_profile(self, profile_name=None):
        if profile_name is None:
            print("profile name is None, Please specify the ssid profile name that you want to update")
            return False

        try:
            profile = self.get_profile_by_name(profile_name=profile_name)
            profile._details["radiusServiceId"] = None
            profile._child_profile_ids = []
            self.profile_client.update_profile(profile)
            return True
        except Exception as e:
            print(e)
            return False

    """
        method to delete a profile by its id
    """

    def delete_profile(self, profile_id=None):
        self.sdk_client.refresh_instance()
        for i in profile_id:
            self.profile_client.delete_profile(profile_id=i)

    # Need to be depreciated by using push_profile method
    def push_profile_old_method(self, equipment_id=None):
        self.sdk_client.refresh_instance()
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
        return response


"""

    FirmwareUtility class
        uses JfrogUtility base class
        sdk_client  [ controller_tests instance ]
        controller_data     [ sdk_base_url ]    needed only if sdk_instance is not passed
        customer_id     [ 2 ]           needed only if sdk_instance is not passed
"""


class FirmwareUtility:

    def __init__(self,
                 sdk_client=None,
                 jfrog_credentials=None,
                 controller_data=None,
                 customer_id=2,
                 model=None,
                 version_url=None):
        # super().__init__(credentials=jfrog_credentials)
        if sdk_client is None:
            sdk_client = Controller(controller_data=controller_data, customer_id=customer_id)
        self.sdk_client = sdk_client
        self.sdk_client.refresh_instance()
        self.firmware_client = FirmwareManagementApi(api_client=sdk_client.api_client)
        # self.jfrog_client = JFrogUtility(credentials=jfrog_credentials)
        self.equipment_gateway_client = EquipmentGatewayApi(api_client=sdk_client.api_client)
        self.model = model
        self.fw_version = version_url

    def get_fw_version(self):
        fw_version = self.fw_version.split("/")[-1]
        return fw_version

    def upload_fw_on_cloud(self, force_upload=False):
        self.sdk_client.refresh_instance()
        fw_version = self.fw_version.split("/")[-1]
        print("Upload fw version :", self.fw_version)
        fw_id = self.is_fw_available(fw_version=fw_version)
        if fw_id and not force_upload:
            print("Skipping upload, Firmware Already Available", "Force Upload :", force_upload)
            # Don't Upload the fw
            return fw_id
        else:
            if fw_id and force_upload:
                print("Firmware Version Already Available, Deleting and Uploading Again",
                      " Force Upload :", force_upload)
                self.firmware_client.delete_firmware_version(firmware_version_id=fw_id)
                print("Deleted Firmware Image from cloud, uploading again")
                time.sleep(2)
                # if force_upload is true and latest image available, then delete the image
            firmware_data = {
                "id": 0,
                "equipmentType": "AP",
                "modelId": str(self.model).upper(),
                "versionName": fw_version,
                "description": fw_version + "  FW VERSION",
                "filename": self.fw_version,
            }
            firmware_id = self.firmware_client.create_firmware_version(body=firmware_data)
            print("Uploaded the Image: ", fw_version)
            return firmware_id._id

    def upgrade_fw(self, equipment_id=None, force_upgrade=False, force_upload=False):
        self.sdk_client.refresh_instance()
        if equipment_id is None:
            print("No Equipment Id Given")
            exit()
        if (force_upgrade is True) or (self.should_upgrade_ap_fw(equipment_id=equipment_id)):
            firmware_id = self.upload_fw_on_cloud(force_upload=force_upload)
            time.sleep(5)
            try:
                obj = self.equipment_gateway_client.request_firmware_update(equipment_id=equipment_id,
                                                                            firmware_version_id=firmware_id)
                print("Request firmware upgrade Success! waiting for 300 sec")
                time.sleep(400)
            except Exception as e:
                print(e)
                obj = False
            return obj
            # Write the upgrade fw logic here

    def should_upgrade_ap_fw(self, equipment_id=None):
        self.sdk_client.refresh_instance()
        current_fw = self.sdk_client.get_ap_firmware_old_method(equipment_id=equipment_id)
        latest_fw = self.get_fw_version()
        print(self.model, current_fw, latest_fw)
        if current_fw == latest_fw:
            return False
        else:
            return True

    def is_fw_available(self, fw_version=None):
        self.sdk_client.refresh_instance()
        if fw_version is None:
            exit()
        try:
            firmware_version = self.firmware_client.get_firmware_version_by_name(
                firmware_version_name=fw_version)
            firmware_version = firmware_version._id
            print("Firmware ID: ", firmware_version)
        except Exception as e:
            print(e)
            firmware_version = False
            print("firmware not available: ", firmware_version)
        return firmware_version


# This is for Unit tests on Controller Library
if __name__ == '__main__':
    controller = {
        'url': "https://wlan-portal-svc-nola-ext-04.cicd.lab.wlan.tip.build",  # API base url for the controller
        'username': 'support@example.com',
        'password': 'support',
        'version': "1.1.0-SNAPSHOT",
        'commit_date': "2021-04-27"
    }
    api = Controller(controller_data=controller)
    profile = ProfileUtility(sdk_client=api)
    profile_data = {
        "name": "test-rf-wifi-6",
        "is2dot4GHz": {},
        "is5GHz": {"channelBandwidth": "is20MHz"},
        "is5GHzL": {"channelBandwidth": "is20MHz"},
        "is5GHzU": {"channelBandwidth": "is20MHz"}
    }
    profile.set_rf_profile(profile_data=profile_data, mode="wifi6")
    print(profile.default_profiles["rf"])
    # profile.cleanup_profiles()

    # profile.get_default_profiles()
    # profile_data = {
    #     "profile_name": "ssid_wep_2g",
    #     "ssid_name": "ssid_wep_2g",
    #     "appliedRadios": ["is2dot4GHz"],
    #     "default_key_id" : 1,
    #     "wep_key" : 1234567890,
    #     "vlan": 1,
    #     "mode": "BRIDGE"
    # }
    # profile.create_wep_ssid_profile(profile_data=profile_data)
    # print(profile.get_profile_by_name(profile_name="wpa_wpa2_eap"))
    # profile.get_default_profiles()
    api.disconnect_Controller()
