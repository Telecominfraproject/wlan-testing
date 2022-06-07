"""

    2.x Security Services Rest API Tests: Test Login, Logout API's

"""
import pytest
import json
import allure


@pytest.mark.uc_sanity
@pytest.mark.ow_sanity_lf
@pytest.mark.owsec_api_tests
@allure.feature("SDK REST API")
class TestUcentralSecService(object):
    """
        Test the oauth endpoint
        WIFI-3447
    """
    '''
    @pytest.mark.sdk_restapi
    def test_secservice_oauth(self, setup_controller):
        """
            pytest -m "uci_login"
        """
        resp = setup_controller.login_resp
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="login", body=body)
        assert setup_controller.login_resp.status_code == 200

    @pytest.mark.sdk_restapi
    def test_secservice_oauth_revoke(self, setup_controller):
        """
            Test the oauth revoke endpoint
            WIFI-3448
        """
        resp = setup_controller.logout()
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="oauth revoke", body=body)
        assert resp.status_code == 204
        setup_controller.login()
    '''

    @pytest.mark.sdk_restapi
    def test_secservice_system_endpoints(self, setup_controller):
        """
            Test the system endpoints to verify list of services present
            WIFI-3449
        """
        resp = setup_controller.request("sec", "systemEndpoints", "GET", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="security systemEndpoints", body=body)

        if resp.status_code != 200:
            assert False
        services = json.loads(resp.text)
        print(services)

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

    @pytest.mark.sdk_restapi
    def test_secservice_get_version(self, setup_controller):
        """
            Test the system endpoint to verify the version of the service
            WIFI-3450
        """

        params = {'command': 'info'}
        resp = setup_controller.request("sec", "system", "GET", params, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="security get version result", body=body)

        if resp.status_code != 200:
            assert False
        system = json.loads(resp.text)
        print(system)
        if 'version' not in system:
            assert False
        if system['version'] == '':
            assert False

    @pytest.mark.sdk_restapi
    def test_secservice_get_uptime(self, setup_controller):
        """
            Test the system endpoint to verify the uptime of the service
            WIFI-3451
        """

        params = {'command': 'info'}
        resp = setup_controller.request("sec", "system", "GET", params, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="security get uptime", body=body)
        if resp.status_code != 200:
            assert False
        system = json.loads(resp.text)
        print(system)
        if 'uptime' not in system:
            assert False

        if 'start' not in system:
            assert False

        if system['uptime'] == '':
            assert False

        if system['start'] == '':
            assert False
