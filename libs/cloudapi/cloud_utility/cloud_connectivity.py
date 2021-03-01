"""
cloud_connectivity.py :

ConnectCloud : <class> has methods to invoke the connections to the cloud constructor
                default constructor of ConnectCloud class (args: testbed-name)
get_bearer() :  It is called by default from the constructor itself. bearer gets expired in 3000 seconds
refresh_bearer() : It is used to refresh the Connectivity. It can be used for Long test runs

"""

import sys

if "cloudsdk" not in sys.path:
    sys.path.append("../cloudsdk")

from swagger_client.api.login_api import LoginApi
from swagger_client.api.equipment_api import EquipmentApi
from swagger_client.api_client import ApiClient

# Testbed name and its respective urls, Modify and add accordingly
cloud_sdk_base_urls = {
    "nola-01": "https://wlan-portal-svc-nola-01.cicd.lab.wlan.tip.build",
    "nola-02": "https://wlan-portal-svc-nola-02.cicd.lab.wlan.tip.build",
    "nola-03": "https://wlan-portal-svc-nola-03.cicd.lab.wlan.tip.build",
    "nola-04": "https://wlan-portal-svc-nola-04.cicd.lab.wlan.tip.build",
    "nola-05": "https://wlan-portal-svc-nola-05.cicd.lab.wlan.tip.build",
    "nola-06": "https://wlan-portal-svc-nola-06.cicd.lab.wlan.tip.build",
    "nola-07": "https://wlan-portal-svc-nola-07.cicd.lab.wlan.tip.build",
    "nola-08": "https://wlan-portal-svc-nola-08.cicd.lab.wlan.tip.build",
    "nola-09": "https://wlan-portal-svc-nola-09.cicd.lab.wlan.tip.build",
    "nola-10": "https://wlan-portal-svc-nola-10.cicd.lab.wlan.tip.build",
    "nola-11": "https://wlan-portal-svc-nola-11.cicd.lab.wlan.tip.build"
}
login_credentials = {
    "userId": "support@example.com",
    "password": "support"
}


class cloudsdk:

    def __init__(self, testbed="nola-01"):
        self.testbed = testbed
        self.sdk_base_url = cloud_sdk_base_urls[self.testbed]
        self.login_credentials = login_credentials
        self.api_client = ApiClient(sdk_base_url=self.sdk_base_url)
        self.login_api = LoginApi(api_client=self.api_client)
        self.equipment_api = EquipmentApi(api_client=self.api_client)
        self.get_or_refresh_bearer()

    def get_or_refresh_bearer(self):
        bearer = self.login_api.get_access_token(self.login_credentials)
        # print(bearer)
        return bearer

    def get_equipment_by_id(self, customer_id=None):
        pagination_context = {
          "model_type": "PaginationContext",
          "maxItemsPerPage": 10
        }
        return self.equipment_api.get_equipment_by_customer_id(customer_id=customer_id, pagination_context=pagination_context)


def main():
    cloudsdk()




if __name__ == "__main__":
    main()

