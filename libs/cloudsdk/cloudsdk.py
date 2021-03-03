# !/usr/local/lib64/python3.8
import swagger_client
from testbed_info import SDK_BASE_URLS
from testbed_info import LOGIN_CREDENTIALS

"""
    Library for setting up the configuration for cloud connectivity
        1. testbed/ sdk_base_url
        2. login credentials
"""


class ConfigureCloudSDK:

    def __init__(self):
        self.configuration = swagger_client.Configuration()

    def set_credentials(self, userId=None, password=None):
        if userId is None or password is None:
            self.configuration.username = LOGIN_CREDENTIALS['userId']
            self.configuration.password = LOGIN_CREDENTIALS['password']
            print("Login Credentials set to default: \n userID: %s\n password: %s\n" % (LOGIN_CREDENTIALS['userId'],
                                                                                        LOGIN_CREDENTIALS['password']))
            return False
        else:
            LOGIN_CREDENTIALS['userId'] = userId
            self.configuration.username = userId
            LOGIN_CREDENTIALS['password'] = password
            self.configuration.password = password
            print("Login Credentials set to custom: \n userID: %s\n password: %s\n" % (LOGIN_CREDENTIALS['userId'],
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

        # print(self.equipment_client.get_equipment_by_customer_id(customer_id=customer_id,
        #                                                          pagination_context=pagination_context))

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

    def __init__(self):
        pass

    """
        method call: used to create the rf profile and push set the parameters accordingly and update
    """

    def set_rf_profile(self):
        pass

    """
        method call: used to create a ssid profile with the given parameters
    """

    def set_ssid_profile(self):
        pass

    """
        method call: used to create a ap profile that contains the given ssid profiles
    """

    def set_ap_profile(self):
        pass

    """
        method call: used to create a radius profile with the settings given
    """

    def set_radius_profile(self):
        pass

    """
        method call: used to create the ssid and psk data that can be used in creation of ssid profile
    """

    def set_ssid_psk_data(self):
        pass

    """
        method to push the profile to the given equipment 
    """

    def push_profile(self):
        pass

    """
        method to verify if the expected ssid's are loaded in the ap vif config
    """

    def monitor_vif_conf(self):
        pass


if __name__ == "__main__":
    obj = CloudSDK(testbed="nola-01")
    # obj.portal_ping()
    # obj.get_equipment_by_customer_id(customer_id=2)
    # obj.get_profiles_by_customer_id(customer_id=2)
    # print(obj.default_profiles)
    obj.disconnect_cloudsdk()
