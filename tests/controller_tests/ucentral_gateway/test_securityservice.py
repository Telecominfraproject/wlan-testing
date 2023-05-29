"""

    2.x Security Services Rest API Tests: Test Login, Logout API's

"""
import logging
import time
import pytest
import json
import allure


@pytest.mark.uc_sanity
@pytest.mark.ow_sanity_lf
@pytest.mark.ow_sdk_tests
@pytest.mark.ow_sdk_load_tests
@pytest.mark.owsec_api_tests
@allure.parent_suite("SDK Tests")
@allure.suite("Security Service Tests")
class TestUcentralSecService(object):

    @allure.title("Get System Endpoints")
    @allure.testcase(name="WIFI-3450",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3450")
    @pytest.mark.system_endpoints
    def test_secservice_system_endpoints(self, get_target_object):
        """
            Test the system endpoints to verify list of services that are present
            Unique marker:pytest -m "system endpoints"
        """
        resp = get_target_object.controller_library_object.request("sec", "systemEndpoints", "GET", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        # allure.attach(name="security systemEndpoints", body=body)

        if resp.status_code != 200:
            assert False
        services = json.loads(resp.text)
        # print(services)

        if 'endpoints' not in services:
            assert False

        num_services = 0
        uri_present = 0
        authtype_present = 0
        for item in services['endpoints']:
            if item['type'] == 'owgw':
                num_services += 1
                if item['uri'] is not None:
                    uri_present += 1
                if item['authenticationType'] is not None:
                    authtype_present += 1
            elif item['type'] == 'owfms':
                num_services += 1
                if item['uri'] is not None:
                    uri_present += 1
                if item['authenticationType'] is not None:
                    authtype_present += 1

        assert (num_services == 2) and (uri_present == 2) and (authtype_present == 2)

    @allure.title("Get Security Version")
    @allure.testcase(name="WIFI-3451",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-3451")
    @pytest.mark.security_versions
    def test_secservice_get_version(self, get_target_object):
        """
            Test the system endpoint to verify the version of the service
            Unique marker:pytest -m "security_version"
        """

        params = {'command': 'info'}
        resp = get_target_object.controller_library_object.request("sec", "system", "GET", params, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        # allure.attach(name="security get version result", body=body)

        if resp.status_code != 200:
            assert False
        system = json.loads(resp.text)
        # print(system)
        if 'version' not in system:
            assert False
        if system['version'] == '':
            assert False

    @allure.title("Get Security Service Uptime")
    def test_secservice_get_uptime(self, get_target_object):
        """
            Test the system endpoint to verify the uptime of the service
            WIFI-3451
        """

        params = {'command': 'info'}
        resp = get_target_object.controller_library_object.request("sec", "system", "GET", params, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        # allure.attach(name="security get uptime", body=body)
        if resp.status_code != 200:
            assert False
        system = json.loads(resp.text)
        # print(system)
        if 'uptime' not in system:
            assert False

        if 'start' not in system:
            assert False

        if system['uptime'] == '':
            assert False

        if system['start'] == '':
            assert False

    @allure.title("Allows any microservice to validate a token and get security policy for a specific user")
    @allure.testcase(name="WIFI-12608",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12608")
    @pytest.mark.validatetoken
    def test_validatetoken(self, get_target_object):
        """
            Allows any microservice to validate a token and get security policy for a specific user
            Unique marker:pytest -m "validatetoken"
        """
        print("Token: ", get_target_object.controller_library_object.access_token)
        params = {'token': get_target_object.controller_library_object.access_token}
        resp = get_target_object.controller_library_object.request("sec", "validateToken", "GET", params, None)

        if resp.status_code != 200:
            assert False

    @allure.title("Get system configuration items")
    @allure.testcase(name="WIFI-12609",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12609")
    @pytest.mark.system_configuration_items
    def test_system_configuration_items(self, get_target_object):
        """
            Get system configuration items
            Unique marker:pytest -m "system_configuration_items"
        """
        params = {'entries': "element1"}
        resp = get_target_object.controller_library_object.request("sec", "systemConfiguration", "GET", params, None)

        if resp.status_code != 200:
            assert False

    @allure.title("Get List of existing users(User Management)")
    @allure.testcase(name="WIFI-12605",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12605")
    @pytest.mark.list_of_existing_users_user_management
    def test_list_of_existing_users_user_management(self, get_target_object):
        """
            Retrieve a list of existing users as well as some information about them
            Unique marker:pytest -m "list_of_existing_users_user_management"
        """
        resp = get_target_object.controller_library_object.request("sec", "users", "GET", None, None)

        if resp.status_code != 200:
            assert False

    @allure.title("CRUD User")
    @allure.testcase(name="WIFI-12632",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12632")
    @pytest.mark.crud_user
    def test_crud_user(self, get_target_object):
        """
            CRUD User
            Unique marker:pytest -m "crud_user"
        """
        payload = {
            "id": "0",
            "name": "Default User",
            "description": "Testing through Automation",
            "email": "testautomation@telecominfraproject.com",
            "validated": True,
            "validationEmail": "testautomation@telecominfraproject.com",
            "changePassword": True,
            "currentPassword": "OpenWifi%123",
            "userRole": "root"
        }
        # Delete if user already exist
        resp = get_target_object.controller_library_object.request("sec", "users", "GET", None, None)
        resp = resp.json()
        all_users = resp["users"]
        for i in all_users:
            if i["email"] == payload["email"]:
                logging.info("User already exist")
                resp = get_target_object.controller_library_object.request("sec", "user/" + str(i["id"]), "DELETE",
                                                                           None, None)
                time.sleep(2)
                if resp.status_code != 200:
                    assert False

        # Create a single user
        payload = json.dumps(payload)
        resp = get_target_object.controller_library_object.request("sec", "user/0", "POST", None, payload)
        if resp.status_code != 200:
            assert False
        time.sleep(2)
        resp = resp.json()
        user_id = resp['id']
        # Retrieve the information for a single user
        resp = get_target_object.controller_library_object.request("sec", "user/" + str(user_id), "GET", None, None)
        if resp.status_code != 200:
            assert False
        # Modify a single user
        edited_payload = {
            "name": "Modified name"
        }
        edited_payload = json.dumps(edited_payload)
        resp = get_target_object.controller_library_object.request("sec", "user/" + str(user_id), "PUT", None,
                                                                   edited_payload)
        if resp.status_code != 200:
            assert False

        # Delete a single user
        resp = get_target_object.controller_library_object.request("sec", "user/" + str(user_id), "DELETE", None,
                                                                   None)
        if resp.status_code != 200:
            assert False

    @allure.title("Get the Authenticator QR Code")
    @allure.testcase(name="WIFI-12633",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12633")
    @pytest.mark.authenticator_qr_code
    def test_authenticator_qr_code(self, get_target_object):
        """
            Get the Authenticator QR Code
            Unique marker:pytest -m "authenticator_qr_code"
        """
        params = {'reset': False}
        resp = get_target_object.controller_library_object.request("sec", "totp", "GET", params, None)

        if resp.status_code != 200:
            assert False

    @allure.title("Get List of existing users(Subscribers)")
    @allure.testcase(name="WIFI-12606",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12606")
    @pytest.mark.list_of_existing_users_subscribers
    def test_list_of_existing_users_subscribers(self, get_target_object):
        """
            Retrieve a list of existing users as well as some information about them
            Unique marker:pytest -m "list_of_existing_users_subscribers"
        """
        resp = get_target_object.controller_library_object.request("sec", "subusers", "GET", None, None)

        if resp.status_code != 200:
            assert False

    @allure.title("CRUD subuser")
    @allure.testcase(name="WIFI-12643",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12643")
    @pytest.mark.crud_subuser
    def test_crud_subuser(self, get_target_object):
        """
            CRUD subuser
            Unique marker:pytest -m "crud_subuser"
        """
        payload = {
            "id": "0",
            "name": "Default User",
            "description": "Testing through Automation",
            "email": "testautomation@telecominfraproject.com",
            "validated": True,
            "validationEmail": "testautomation@telecominfraproject.com",
            "changePassword": False,
            "currentPassword": "OpenWifi%123",
            "userRole": "subscriber"
        }
        # Delete if user already exist
        resp = get_target_object.controller_library_object.request("sec", "subusers", "GET", None, None)
        resp = resp.json()
        all_users = resp["users"]
        for i in all_users:
            if i["email"] == payload["email"]:
                logging.info("User already exist")
                resp = get_target_object.controller_library_object.request("sec", "subuser/" + str(i["id"]), "DELETE",
                                                                           None, None)
                time.sleep(2)
                if resp.status_code != 200:
                    assert False
        # Create a single user
        payload = json.dumps(payload)
        resp = get_target_object.controller_library_object.request("sec", "subuser/0", "POST", None, payload)
        if resp.status_code != 200:
            assert False
        time.sleep(2)
        resp = resp.json()
        user_id = resp['id']
        # Retrieve the information for a single user
        resp = get_target_object.controller_library_object.request("sec", "subuser/" + str(user_id), "GET", None, None)
        if resp.status_code != 200:
            assert False
        # Modify a single user
        edited_payload = {
            "name": "Modified name"
        }
        edited_payload = json.dumps(edited_payload)
        resp = get_target_object.controller_library_object.request("sec", "subuser/" + str(user_id), "PUT", None,
                                                                   edited_payload)
        if resp.status_code != 200:
            assert False

        # Delete a single user
        resp = get_target_object.controller_library_object.request("sec", "subuser/" + str(user_id), "DELETE", None,
                                                                   None)
        if resp.status_code != 200:
            assert False
