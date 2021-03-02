# !/usr/local/lib64/python3.8
import swagger_client

login_credentials = {
    "userId": "support@example.com",
    "password": "support"
}
sdk_base_urls = {
    "nola-01": "https://wlan-portal-svc-nola-01.cicd.lab.wlan.tip.build",
    "nola-02": "https://wlan-portal-svc-nola-02.cicd.lab.wlan.tip.build",
    "nola-04": "https://wlan-portal-svc-nola-04.cicd.lab.wlan.tip.build",
}

class CloudSdk:
    """
    constructor for cloudsdk library : can be used from pytest framework
    """

    def __init__(self, testbed="nola-01"):
        self.configuration = swagger_client.Configuration()
        self.configuration.host = sdk_base_urls[testbed]
        self.configuration.refresh_api_key_hook = self.get_bearer_token
        self.configuration.username = login_credentials['userId']
        self.configuration.password = login_credentials['password']

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
        print(self.bearer)
        # print(self.ping_response)

    """
    Login Utilities
    """

    def get_bearer_token(self):
        return self.login_client.get_access_token(body=login_credentials)

    def portal_ping(self):
        return self.login_client.portal_ping()

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

if __name__ == "__main__":
    obj = CloudSdk(testbed="nola-01")
    obj.portal_ping()
    obj.get_equipment_by_customer_id(customer_id=2)
    obj.get_profiles_by_customer_id(customer_id=2)
    print(obj.default_profiles)
    obj.api_client.__del__()
