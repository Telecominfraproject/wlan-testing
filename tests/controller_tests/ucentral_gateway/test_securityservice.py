"""

    UCentral Security Services Rest API Tests: Test Login, Logout API's

"""
import pytest
import json
import allure

@allure.feature("SDK REST API")

class TestUcentralSecService(object):
    """
        pytest -m "uci_login or uci_logout"
    """
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
            pytest -m "uci_logout"
        """
        resp = setup_controller.logout()
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="oauth revoke", body=body)
        assert resp.status_code == 204
        setup_controller.login()

    @pytest.mark.sdk_restapi
    def test_secservice_system_endpoints(self, setup_controller):
        """
            pytest -m "uci_endpoints"
            look for ucentralgw and ucentralfms services for 2.1 release
        """
        resp = setup_controller.request("sec", "systemEndpoints", "GET", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="security systemEndpoints", body=body)

        if resp.status_code != 200:
            assert False
        services = json.loads(resp.text)
        print (services)

        if 'endpoints' not in services:
            assert False

        num_services = 0
        uri_present = 0
        authtype_present = 0
        for item in services['endpoints']:
            if item['type'] == 'ucentralgw':
                num_services += 1
                if item['uri'] is not None:
                    uri_present += 1
                if item['authenticationType'] is not None:
                    authtype_present += 1
            elif item['type'] == 'ucentralfms':
                num_services += 1
                if item['uri'] is not None:
                    uri_present += 1
                if item['authenticationType'] is not None:
                    authtype_present += 1

        assert (num_services == 2) and (uri_present == 2) and (authtype_present == 2)

    @pytest.mark.sdk_restapi
    def test_secservice_get_version(self, setup_controller):
        """
            pytest -m "uci_endpoints"
            look for ucentralgw and ucentralfms services for 2.1 release
        """

        params = {'command': 'version'}
        resp = setup_controller.request("sec", "system", "GET", params, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="security get version result", body=body)

        if resp.status_code != 200:
            assert False
        system = json.loads(resp.text)
        print (system)
        if 'tag' not in system:
            assert False
        if system['tag'] != 'version':
            assert False
        if not system['value']:
            assert False

    @pytest.mark.sdk_restapi
    def test_secservice_get_uptime(self, setup_controller):
        """
            look for ucentralgw and ucentralfms services for 2.1 release
        """

        params = {'command': 'times'}
        resp = setup_controller.request("sec", "system", "GET", params, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="security get uptime", body=body)
        if resp.status_code != 200:
            assert False
        system = json.loads(resp.text)
        print (system)
        if 'times' not in system:
            assert False

        valid_entities = 0
        for item in system['times']:
            if item['tag'] == 'uptime':
                valid_entities += 1
            if item['tag'] == 'start':
                valid_entities += 1
            if item['value'] is not None:
                valid_entities += 1

        assert (valid_entities == 4)



