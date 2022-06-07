"""

    Provision Services Rest API Use Case Tests

"""

import string
import random

import pytest
import json
import allure


@pytest.mark.ow_sanity_lf
@pytest.mark.uc_sanity
@pytest.mark.owprov_api_tests
@pytest.mark.owprov_api_usecase
@allure.feature("SDK PROV REST API")
class TestProvAPIUseCase(object):

    @pytest.mark.prov_api_usecase_test
    def test_prov_service_use_case(self, setup_prov_controller, testbed):
        """
            Test to create Entity and then creates child entity under it,
            then location, venue with the before created location, contact, Inventory device under this child Entity and
             deletes them at last
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

        child_payload = {
                          "name": "Child Entity testing_prov",
                          "deviceRules": {
                            "rrm": "inherit",
                            "rcOnly": "inherit",
                            "firmwareUpgrade": "inherit"
                          },
                          "description": "Child Entity testing",
                          "notes": [
                            {
                              "note": "Child Entity testing"
                            }
                          ],
                          "parent": entity_id
                        }
        print(json.dumps(child_payload))
        resp = setup_prov_controller.add_entity(child_payload)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create Child entity", body=body)
        if resp.status_code != 200:
            assert False
        child_entity = json.loads(resp.text)
        print(child_entity)
        child_entity_id = child_entity['id']

        resp = setup_prov_controller.get_entity_by_id(child_entity_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create child Entity-verify", body=body)
        if resp.status_code != 200:
            assert False

        location_payload = {
                              "name": "Testing usecase through Automation",
                              "description": "Testing usecase through Automation",
                              "type": "SERVICE",
                              "addressLines": [
                                "Pedda Rushikonda",
                                ""
                              ],
                              "city": "Visakhapatnam",
                              "state": "Andhra Prdaesh",
                              "postal": "530045",
                              "country": "IN",
                              "buildingName": "Candela Technologies",
                              "mobiles": [],
                              "phones": [],
                              "geoCode": "",
                              "entity": child_entity_id
                            }
        print(json.dumps(location_payload))
        resp = setup_prov_controller.add_location(location_payload)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create location", body=body)
        if resp.status_code != 200:
            assert False
        location = json.loads(resp.text)
        print(location)
        location_id = location['id']

        resp = setup_prov_controller.get_location_by_id(location_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create location-verify", body=body)
        if resp.status_code != 200:
            assert False

        venue_payload = {
                          "name": "Venue under child entity through Automation",
                          "deviceRules": {
                            "rrm": "inherit",
                            "rcOnly": "inherit",
                            "firmwareUpgrade": "inherit"
                          },
                          "description": "Venue under child entity through Automation",
                          "parent": "",
                          "entity": child_entity_id,
                          "location": location_id
                        }
        print(json.dumps(venue_payload))
        resp = setup_prov_controller.add_venue(venue_payload)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create venue", body=body)
        if resp.status_code != 200:
            assert False
        venue = json.loads(resp.text)
        print(venue)
        venue_id = venue['id']

        resp = setup_prov_controller.get_venue_by_id(venue_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create venue-verify", body=body)
        if resp.status_code != 200:
            assert False

        device_mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                                  random.randint(0, 255),
                                                  random.randint(0, 255))
        device_name = device_mac.replace(":", "")
        inventory_payload = {
                              "serialNumber": device_name,
                              "name": "Device under child entity",
                              "deviceRules": {
                                "rrm": "inherit",
                                "rcOnly": "inherit",
                                "firmwareUpgrade": "inherit"
                              },
                              "deviceType": "cig_wf194c4",
                              "devClass": "entity",
                              "description": "Device under child entity",
                              "entity": child_entity_id,
                              "venue": "",
                              "subscriber": ""
                            }
        print(json.dumps(inventory_payload))
        resp = setup_prov_controller.add_device_to_inventory(device_name, inventory_payload)
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

        contact_payload = {
                          "name": "Tip automation",
                          "type": "MANAGER",
                          "salutation": "",
                          "title": "",
                          "firstname": "Tip",
                          "lastname": "Automation",
                          "initials": "",
                          "primaryEmail": "tip@candelatech.com",
                          "secondaryEmail": "",
                          "mobiles": [],
                          "phones": [],
                          "description": "Creating contact through Automation testing",
                          "accessPIN": "",
                          "entity": child_entity_id
                        }
        print(json.dumps(contact_payload))
        resp = setup_prov_controller.add_contact(contact_payload)
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

        # Deleting Contact
        resp = setup_prov_controller.delete_contact(contact_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created contact-delete", body=body)
        if resp.status_code != 200:
            assert False

        # Deleting Device from Inventory
        resp = setup_prov_controller.delete_device_from_inventory(device_name)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created device-delete", body=body)
        if resp.status_code != 200:
            assert False

        # Deleting Venue
        resp = setup_prov_controller.delete_venue(venue_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created venue-delete", body=body)
        if resp.status_code != 200:
            assert False

        # Deleting Location
        resp = setup_prov_controller.delete_location(location_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created location-delete", body=body)
        if resp.status_code != 200:
            assert False

        # Deleting Child Entity
        resp = setup_prov_controller.delete_entity(child_entity_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created Child Entity-delete", body=body)
        if resp.status_code != 200:
            assert False

        # Deleting Entity
        resp = setup_prov_controller.delete_entity(entity_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created Entity-delete", body=body)
        if resp.status_code != 200:
            assert False