#!/usr/bin/python3
import requests


class CloudAPI:

    def __init__(self,
                 cloud_credentials,
                 testbed_urls,
                 target_testbed,
                 equipment_ids=None,
                 target_model="ecw5410"):
        self.user = cloud_credentials["user"]
        self.password = cloud_credentials["password"]
        self.cloudSDK_url = testbed_urls[target_testbed]["url"]
        self.cloud_type = "v1"
        self.bearer = self.get_bearer_token(cloud_type=self.cloud_type)
        pass

    def get_bearer_token(self, cloud_type="v1"):
        cloud_login_url = self.cloudSDK_url + "/management/" + cloud_type + "/oauth2/token"
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
        return bearer_token

    def refresh_bearer_token(self):
        self.bearer = self.get_bearer_token(cloud_type=self.cloud_type)

    def check_response(self, cmd, response, headers, data_str, url):
        if response.status_code >= 500:
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

    def get_equipment(self, equipment_id):

        request_data = {
            "equipmentType": "AP",
            "customerId": 2,
            "profileId": 1,
            "locationId": 2,
            "inventoryId": "example_ap",
            "serial": "example_serial",
            "name": "example AP"
        }
        equipment_data = {
          "equipmentType": "AP",
          "customerId": 2,
          "profileId": 1,
          "locationId": 2,
          "inventoryId": "example_ap",
          "serial": "example_serial",
          "name": "example AP"
        }
        url = self.cloudSDK_url + "/portal/equipment/forCustomer" + "?customerId=" + customer_id
        return self.get_paged_url(self.bearer, url)
        pass
