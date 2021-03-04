# !/usr/local/lib64/python3.8
"""
    Library for setting up the configuration for cloud connectivity
        1. testbed/ sdk_base_url
        2. login credentials
"""

import datetime
import time
import swagger_client
from testbed_info import SDK_BASE_URLS
from testbed_info import LOGIN_CREDENTIALS


class ConfigureCloudSDK:

    def __init__(self):
        self.configuration = swagger_client.Configuration()

    def set_credentials(self, user_id=None, password=None):
        if user_id is None or password is None:
            self.configuration.username = LOGIN_CREDENTIALS['user_id']
            self.configuration.password = LOGIN_CREDENTIALS['password']
            print("Login Credentials set to default: \n user_id: %s\n password: %s\n" % (LOGIN_CREDENTIALS['user_id'],
                                                                                        LOGIN_CREDENTIALS['password']))
            return False
        else:
            LOGIN_CREDENTIALS['user_id'] = user_id
            self.configuration.username = user_id
            LOGIN_CREDENTIALS['password'] = password
            self.configuration.password = password
            print("Login Credentials set to custom: \n user_id: %s\n password: %s\n" % (LOGIN_CREDENTIALS['user_id'],
                                                                                       LOGIN_CREDENTIALS['password']))
            return True

    def select_testbed(self, testbed=None):
        if testbed is None:
            print("No Testbed Selected")
            exit()
        self.configuration.host = SDK_BASE_URLS[testbed]
        print("Testbed Selected: %s\n SDK_BASE_URL: %s\n" % (testbed, SDK_BASE_URLS[testbed]))
        return True

    def set_sdk_base_url(self, sdk_base_url=None):
        if sdk_base_url is None:
            print("URL is None")
            exit()
        self.configuration.host = sdk_base_url
        return True


"""
    Library for cloudSDK generic usages, it instantiate the bearer and credentials.
    It provides the connectivity to the cloud.
"""


class CloudSDK(ConfigureCloudSDK):
    """
    constructor for cloudsdk library : can be used from pytest framework
    """

    def __init__(self, testbed=None):
        super().__init__()

        # Setting the CloudSDK Client Configuration
        self.select_testbed(testbed=testbed)
        self.set_credentials()
        self.configuration.refresh_api_key_hook = self.get_bearer_token

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

    def get_equipment_by_customer_id(self, customer_id=None):
        pagination_context = """{
                "model_type": "PaginationContext",
                "maxItemsPerPage": 10
        }"""

        print(self.equipment_client.get_equipment_by_customer_id(customer_id=customer_id,
                                                                 pagination_context=pagination_context))

    def request_ap_reboot(self):
        pass

    def request_firmware_update(self):
        pass

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

    def get_profile_template(self, customer_id=None, profile_name=None):
        pagination_context = """{
                        "model_type": "PaginationContext",
                        "maxItemsPerPage": 100
                }"""
        profiles = self.profile_client.get_profiles_by_customer_id(customer_id=customer_id,
                                                                   pagination_context=pagination_context)._items
        for i in profiles:
            if i._name == profile_name:
                return i
        return None

    def get_profiles_by_customer_id(self, customer_id=None):
        pagination_context = """{
                "model_type": "PaginationContext",
                "maxItemsPerPage": 100
        }"""
        self.default_profiles = {}
        print(len((self.profile_client.get_profiles_by_customer_id(customer_id=customer_id,
                                                                   pagination_context=pagination_context))._items))
        for i in self.profile_client.get_profiles_by_customer_id(customer_id=customer_id,
                                                                 pagination_context=pagination_context)._items:
            print(i._name, i._id)
            if i._name == "TipWlan-Cloud-Wifi":
                self.default_profiles['ssid'] = i
            if i._name == "TipWlan-Cloud-Wifi":
                self.default_profiles['ssid'] = i
            if i._name == "TipWlan-Cloud-Wifi":
                self.default_profiles['ssid'] = i

    def create_profile(self, profile_type=None, customer_id=None, profile_name=None):
        if profile_type is None or customer_id is None or profile_name is None:
            return "Invalid profile_type/customer_id/profile_name"

        profile_data = {
            "profileType": profile_type,  # eg. ("equipment_ap", "ssid", "rf", "radius", "captive_portal")
            "customerId": customer_id,
            "name": profile_name
        }
        return "Profile Created Successfully!"


class APUtils:
    """
       constructor for Access Point Utility library : can be used from pytest framework
                                                      to control Access Points
    """

    def __init__(self, sdk_client=None, testbed=None):
        if sdk_client is None:
            sdk_client = CloudSDK(testbed=testbed)
        self.sdk_client = sdk_client
        self.profile_client = swagger_client.ProfileApi(api_client=self.sdk_client.api_client)
        self.profile_creation_ids = {
            "ssid": [],
            "ap": [],
            "radius": [],
            "rf": []
        }
        self.profile_ids = []

    """
        method call: used to create the rf profile and push set the parameters accordingly and update
    """

    def select_rf_profile(self, profile_data=None):
        default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-rf")
        if profile_data is None:
            self.profile_creation_ids['rf'].append(default_profile._id)
        # Need to add functionality to add similar Profile and modify accordingly

    """
        method call: used to create a ssid profile with the given parameters
    """

    def create_open_ssid_profile(self, two4g=True, fiveg=True, profile_data=None):
        if profile_data is None:
            return False
        default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-Cloud-Wifi")
        default_profile._details['appliedRadios'] = []
        if two4g is True:
            default_profile._details['appliedRadios'].append("is2dot4GHz")
        if fiveg is True:
            default_profile._details['appliedRadios'].append("is5GHzU")
            default_profile._details['appliedRadios'].append("is5GHz")
            default_profile._details['appliedRadios'].append("is5GHzL")
        default_profile._name = profile_data['profile_name']
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
        default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-Cloud-Wifi")
        default_profile._details['appliedRadios'] = []
        if two4g is True:
            default_profile._details['appliedRadios'].append("is2dot4GHz")
        if fiveg is True:
            default_profile._details['appliedRadios'].append("is5GHzU")
            default_profile._details['appliedRadios'].append("is5GHz")
            default_profile._details['appliedRadios'].append("is5GHzL")
        default_profile._name = profile_data['profile_name']
        default_profile._details['ssid'] = profile_data['ssid_name']
        default_profile._details['keyStr'] = profile_data['security_key']
        default_profile._details['forwardMode'] = profile_data['mode']
        default_profile._details['secureMode'] = 'wpaPSK'
        profile_id = self.profile_client.create_profile(body=default_profile)._id
        self.profile_creation_ids['ssid'].append(profile_id)
        self.profile_ids.append(profile_id)
        return True

    def create_wpa2_personal_ssid_profile(self, two4g=True, fiveg=True, profile_data=None):
        if profile_data is None:
            return False
        default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-Cloud-Wifi")
        default_profile._details['appliedRadios'] = []
        if two4g is True:
            default_profile._details['appliedRadios'].append("is2dot4GHz")
        if fiveg is True:
            default_profile._details['appliedRadios'].append("is5GHzU")
            default_profile._details['appliedRadios'].append("is5GHz")
            default_profile._details['appliedRadios'].append("is5GHzL")
        default_profile._name = profile_data['profile_name']
        default_profile._details['ssid'] = profile_data['ssid_name']
        default_profile._details['keyStr'] = profile_data['security_key']
        default_profile._details['forwardMode'] = profile_data['mode']
        default_profile._details['secureMode'] = 'wpa2OnlyPSK'
        profile_id = self.profile_client.create_profile(body=default_profile)._id
        self.profile_creation_ids['ssid'].append(profile_id)
        self.profile_ids.append(profile_id)
        return True

    def create_wpa3_personal_ssid_profile(self, two4g=True, fiveg=True, profile_data=None):
        if profile_data is None:
            return False
        default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-Cloud-Wifi")
        default_profile._details['appliedRadios'] = []
        if two4g is True:
            default_profile._details['appliedRadios'].append("is2dot4GHz")
        if fiveg is True:
            default_profile._details['appliedRadios'].append("is5GHzU")
            default_profile._details['appliedRadios'].append("is5GHz")
            default_profile._details['appliedRadios'].append("is5GHzL")
        default_profile._name = profile_data['profile_name']
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
        default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-Cloud-Wifi")
        default_profile._details['appliedRadios'] = []
        if two4g is True:
            default_profile._details['appliedRadios'].append("is2dot4GHz")
        if fiveg is True:
            default_profile._details['appliedRadios'].append("is5GHzU")
            default_profile._details['appliedRadios'].append("is5GHz")
            default_profile._details['appliedRadios'].append("is5GHzL")
        default_profile._name = profile_data['profile_name']
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
        default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-Cloud-Wifi")
        default_profile._details['appliedRadios'] = []
        if two4g is True:
            default_profile._details['appliedRadios'].append("is2dot4GHz")
        if fiveg is True:
            default_profile._details['appliedRadios'].append("is5GHzU")
            default_profile._details['appliedRadios'].append("is5GHz")
            default_profile._details['appliedRadios'].append("is5GHzL")
        default_profile._name = profile_data['profile_name']
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
        default_profile = self.sdk_client.get_profile_template(customer_id=2, profile_name="TipWlan-2-Radios")
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
        pass

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

    def push_profile(self, equipment_id=None):
        default_equipment_data =self.sdk_client.equipment_client.get_equipment_by_id(equipment_id=equipment_id)
        default_equipment_data._profile_id = self.profile_creation_ids['ap']
        print(default_equipment_data)
        self.sdk_client.equipment_client.update_equipment(body=default_equipment_data)


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
        pass


if __name__ == "__main__":
    sdk_client = CloudSDK(testbed="nola-ext-03")
    # sdk_client.get_equipment_by_customer_id(customer_id=2)
    ap_utils = APUtils(sdk_client=sdk_client)
    ap_utils.select_rf_profile(profile_data=None)
    # radius_info = {
    #     "name": "Radius-Profile-" + str(datetime.datetime.now()),
    #     "ip": "192.168.200.75",
    #     "port": 1812,
    #     "secret": "testing123"
    # }
    #
    # ap_utils.set_radius_profile(radius_info=radius_info)
    profile_data = {
        "profile_name": "test-ssid-open",
        "ssid_name": "test_open",
        "mode": "BRIDGE"
    }

    ap_utils.create_open_ssid_profile(profile_data=profile_data)
    profile_data = {
        "profile_name": "test-ssid-wpa",
        "ssid_name": "test_wpa",
        "mode": "BRIDGE",
        "security_key": "testing12345"
    }

    ap_utils.create_wpa_ssid_profile(profile_data=profile_data)
    profile_data = {
        "profile_name": "test-ssid-wpa2",
        "ssid_name": "test_wpa2",
        "mode": "BRIDGE",
        "security_key": "testing12345"
    }

    ap_utils.create_wpa2_personal_ssid_profile(profile_data=profile_data)
    #
    # obj.portal_ping()
    # obj.get_equipment_by_customer_id(customer_id=2)
    # obj.get_profiles_by_customer_id(customer_id=2)
    # print(obj.default_profiles)
    profile_data = {
        "profile_name": "test-ap-library",
    }
    ap_utils.set_ap_profile(profile_data=profile_data)
    ap_utils.push_profile(equipment_id=1)
    sdk_client.disconnect_cloudsdk()
    # ap_utils.delete_profile(profile_id=ap_utils.profile_ids)

