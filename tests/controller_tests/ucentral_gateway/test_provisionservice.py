"""

    Provision Services Rest API Tests

"""

import string
import random

import pytest
import json
import allure


@pytest.mark.uc_sanity
@allure.feature("SDK PROV REST API")
class TestUcentralProvisionService(object):

    @pytest.mark.sdk_restapi
    @pytest.mark.prov_api
    def test_provservice_inventorylist(self, setup_controller):
        """
            Test the list devices endpoint
            WIFI-3452
        """
        resp = setup_controller.request("prov", "inventory", "GET", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="prov inventory list", body=body)
        if resp.status_code != 200:
            assert False
        inven = json.loads(resp.text)
        print(inven)