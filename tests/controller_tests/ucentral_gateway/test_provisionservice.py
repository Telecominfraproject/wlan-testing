"""

    Provision Services Rest API Tests

"""

import string
import random

import pytest
import json
import allure


@pytest.mark.uc_sanity
@pytest.mark.prov_all_api
@allure.feature("SDK PROV REST API")
class TestUcentralProvisionService(object):


    @pytest.mark.sdk_restapi
    @pytest.mark.prov_api
    def test_provservice_inventorylist(self, setup_prov_controller, get_configuration):
        """
            Test the device present in Provisioning UI
        """
        device_name = get_configuration['access_point'][0]['serial']
        resp = setup_prov_controller.get_inventory_by_device(device_name)
        print(resp.json())
        allure.attach(name="Inventory", body=str(resp.json()),attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.prov_api_test
    def test_prov_service_create_inventory_device(self, setup_prov_controller, testbed):
        """
            Test the create device in provision Inventory
        """
        device_mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                     random.randint(0, 255),
                                     random.randint(0, 255))
        device_name = device_mac.replace(":", "")
        # device_name = "deadbeef0011" + testbed.replace("-","")
        payload = {"serialNumber": device_name,
                   "name": "Testing_to_add_device_through_automation",
                   "rrm": "inherit",
                   "deviceType": "edgecore_eap101",
                   "devClass": "any",
                   "description": "For testing API through automation",
                   "entity": "",
                   "venue": "",
                   "subscriber": "",
                   "__newConfig":
                       {"rrm": "inherit",
                        "firmwareUpgrade": "no",
                        "configuration": [],
                        "name": "Device added through automation",
                        "description": "Created from the Edit Tag menu",
                        "deviceTypes": ["edgecore_eap101"]
                        }
                   }
        print(json.dumps(payload))
        resp = setup_prov_controller.add_device_to_inventory(device_name, payload)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create device", body=body)
        if resp.status_code != 200:
            assert False
        devices = json.loads(resp.text)
        print(devices)

        resp = setup_prov_controller.get_inventory_by_device(device_name)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create device-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_prov_controller.request("prov", "inventory/" + device_name, "DELETE", None, None)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created device-delete", body=body)
        if resp.status_code != 200:
            assert False

    @pytest.mark.system_info_prov
    def test_system_info_prov(self, setup_prov_controller):
        system_info = setup_prov_controller.get_system_prov()
        print(system_info.json())
        allure.attach(name="system info", body=str(system_info.json()), attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200
