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

        # This is for Edititng the information fo device in Inventory
        editing_payload = {
                          "description": "For testing API through automation after editing",
                          "devClass": "any",
                          "deviceType": "edgecore_eap101",
                          "entity": "",
                          "name": "Testing_to_add_device_through_automation",
                          "notes": [],
                          "rrm": "inherit",
                          "venue": ""
                        }
        print(json.dumps(editing_payload))
        resp = setup_prov_controller.edit_device_from_inventory(device_name, editing_payload)
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

        resp = setup_prov_controller.delete_device_from_inventory(device_name)
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

    @pytest.mark.prov_api_entity_test
    def test_prov_service_create_entity(self, setup_prov_controller, testbed):
        """
            Test the create Entity in provision Inventory
        """
        payload = {"name": "Testing_prov",
                    "rrm": "inherit",
                    "description": "For testing Purposes through Automation",
                    "notes": [{"note": "For testing Purposes through Automation"}],
                    "parent": "0000-0000-0000"
                   }
        print(json.dumps(payload))
        resp = setup_prov_controller.add_entity(payload)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create entity", body=body)
        if resp.status_code != 200:
            assert False
        entitiy = json.loads(resp.text)
        print(entitiy)
        entity_id = entitiy['id']

        resp = setup_prov_controller.get_entity_by_id(entity_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create device-verify", body=body)
        if resp.status_code != 200:
            assert False

        # This to edit Entity
        editing_payload = {
                          "description": "For testing Purposes through Automation after edit",
                          "deviceConfiguration": [],
                          "name": "Testing_prov",
                          "notes": [],
                          "rrm": "inherit",
                          "sourceIP": [],
                          "uuid": entity_id
                        }
        print(json.dumps(editing_payload))
        resp = setup_prov_controller.edit_entity(editing_payload, entity_id)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create entity", body=body)
        if resp.status_code != 200:
            assert False
        entitiy = json.loads(resp.text)
        print(entitiy)

        resp = setup_prov_controller.get_entity_by_id(entity_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create device-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_prov_controller.delete_entity(entity_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created device-delete", body=body)
        if resp.status_code != 200:
            assert False

    @pytest.mark.prov_api_entity
    def test_get_entities(self, setup_prov_controller):
        resp = setup_prov_controller.get_entity()
        print(resp.json())
        allure.attach(name="Entities", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    # Contact related Test cases
    @pytest.mark.prov_api_contact
    def test_get_contacts(self, setup_prov_controller):
        resp = setup_prov_controller.get_contact()
        print(resp.json())
        allure.attach(name="Contacts", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.prov_api_contact_test
    def test_prov_service_create_contact(self, setup_prov_controller, testbed):
        """
            Test the create Contact in provision Inventory
        """
        payload = {
                    "name": "Prov-Testing-through-Automation",
                    "type": "USER",
                    "title": "Testing_contact",
                    "salutation": "",
                    "firstname": "ProvTesting",
                    "lastname": "Through Automation",
                    "initials": "",
                    "visual": "",
                    "phones": [],
                    "mobiles": [],
                    "primaryEmail": "tip@ucentral.com",
                    "secondaryEmail": "",
                    "accessPIN": "",
                    "description": "",
                    "initialNote": "",
                    "entity": "0000-0000-0000",
                    "notes": [{"note": ""}]
                }
        print(json.dumps(payload))
        resp = setup_prov_controller.add_contact(payload)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create contact", body=body)
        if resp.status_code != 200:
            assert False
        contact = json.loads(resp.text)
        print(contact)
        contact_id = contact['id']

        resp = setup_prov_controller.get_contact_by_id(contact_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create contact-verify", body=body)
        if resp.status_code != 200:
            assert False

        # This to edit Entity
        editing_payload = {
                          "accessPIN": "",
                          "description": "",
                          "entity": "0000-0000-0000",
                          "firstname": "ProvTesting",
                          "initials": "",
                          "lastname": "Through Automation",
                          "mobiles": [],
                          "name": "Prov-Testing-Automation API's",
                          "notes": [],
                          "phones": [],
                          "primaryEmail": "tip@ucentral.com",
                          "salutation": "",
                          "secondaryEmail": "",
                          "title": "Testing_contact",
                          "type": "USER"
                        }
        print(json.dumps(editing_payload))
        resp = setup_prov_controller.edit_contact(editing_payload, contact_id)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create contact", body=body)
        if resp.status_code != 200:
            assert False
        entitiy = json.loads(resp.text)
        print(entitiy)

        resp = setup_prov_controller.get_contact_by_id(contact_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create contact-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_prov_controller.delete_contact(contact_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created contact-delete", body=body)
        if resp.status_code != 200:
            assert False

