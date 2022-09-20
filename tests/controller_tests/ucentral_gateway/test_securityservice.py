"""

    2.x Security Services Rest API Tests: Test Login, Logout API's

"""
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
        #allure.attach(name="security systemEndpoints", body=body)

        if resp.status_code != 200:
            assert False
        services = json.loads(resp.text)
        #print(services)

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
        #allure.attach(name="security get version result", body=body)

        if resp.status_code != 200:
            assert False
        system = json.loads(resp.text)
        #print(system)
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
        #allure.attach(name="security get uptime", body=body)
        if resp.status_code != 200:
            assert False
        system = json.loads(resp.text)
        #print(system)
        if 'uptime' not in system:
            assert False

        if 'start' not in system:
            assert False

        if system['uptime'] == '':
            assert False

        if system['start'] == '':
            assert False