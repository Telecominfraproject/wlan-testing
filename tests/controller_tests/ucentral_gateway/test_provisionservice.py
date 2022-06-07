"""

    Provision Services Rest API Tests

"""

import string
import random

import pytest
import json
import allure


@pytest.mark.ow_sanity_lf
@pytest.mark.uc_sanity
@pytest.mark.owprov_api_tests
@pytest.mark.owprov_api_inventory
@allure.feature("SDK PROV REST API")
class TestProvAPIInventory(object):


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
    def test_prov_service_create_edit_delete_inventory_device(self, setup_prov_controller, testbed):
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
        allure.attach(name="Prov edited device", body=body)
        if resp.status_code != 200:
            assert False
        devices = json.loads(resp.text)
        print(devices)

        resp = setup_prov_controller.get_inventory_by_device(device_name)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov edited device-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_prov_controller.delete_device_from_inventory(device_name)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created device-delete", body=body)
        if resp.status_code != 200:
            assert False

@pytest.mark.ow_sanity_lf
@pytest.mark.uc_sanity
@pytest.mark.owprov_api_tests
@pytest.mark.owprov_api_system_commands
@allure.feature("SDK PROV REST API")
class TestProvAPISystemCommands(object):

    @pytest.mark.system_info_prov
    def test_system_info_prov(self, setup_prov_controller):
        system_info = setup_prov_controller.get_system_prov()
        print(system_info.json())
        allure.attach(name="system info", body=str(system_info.json()), attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200

@pytest.mark.ow_sanity_lf
@pytest.mark.uc_sanity
@pytest.mark.owprov_api_tests
@pytest.mark.owprov_api_entity
@allure.feature("SDK PROV REST API")
class TestProvAPIEntity(object):

    @pytest.mark.prov_api_entity
    def test_get_entities(self, setup_prov_controller):
        resp = setup_prov_controller.get_entity()
        print(resp.json())
        allure.attach(name="Entities", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.prov_api_entity_test
    def test_prov_service_create_edit_delete_entity(self, setup_prov_controller, testbed):
        """
            Test the create Entity in provision Service
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
        allure.attach(name="Prov edited entity", body=body)
        if resp.status_code != 200:
            assert False
        entitiy = json.loads(resp.text)
        print(entitiy)

        resp = setup_prov_controller.get_entity_by_id(entity_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov edited device-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_prov_controller.delete_entity(entity_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created device-delete", body=body)
        if resp.status_code != 200:
            assert False

@pytest.mark.ow_sanity_lf
@pytest.mark.uc_sanity
@pytest.mark.owprov_api_tests
@pytest.mark.owprov_api_contact
@allure.feature("SDK PROV REST API")
class TestProvAPIContact(object):

    # Contact related Test cases
    @pytest.mark.prov_api_contact
    def test_get_contacts(self, setup_prov_controller):
        resp = setup_prov_controller.get_contact()
        print(resp.json())
        allure.attach(name="Contacts", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.prov_api_contact_test
    def test_prov_service_create_edit_delete_contact(self, setup_prov_controller, testbed):
        """
            Test the create Contact in provision Service
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

        # This to edit Contact
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
        allure.attach(name="Prov edited contact", body=body)
        if resp.status_code != 200:
            assert False
        entitiy = json.loads(resp.text)
        print(entitiy)

        resp = setup_prov_controller.get_contact_by_id(contact_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov edited contact-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_prov_controller.delete_contact(contact_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created contact-delete", body=body)
        if resp.status_code != 200:
            assert False

@pytest.mark.ow_sanity_lf
@pytest.mark.uc_sanity
@pytest.mark.owprov_api_tests
@pytest.mark.owprov_api_location
@allure.feature("SDK PROV REST API")
class TestProvAPILocation(object):

    # Location related Test cases
    @pytest.mark.prov_api_location
    def test_get_locations(self, setup_prov_controller):
        resp = setup_prov_controller.get_location()
        print(resp.json())
        allure.attach(name="location", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.prov_api_location_test
    def test_prov_service_create_edit_delete_location(self, setup_prov_controller, testbed):
        """
            Test the create location in provision Service
        """
        payload = {
                    "name": "TIP",
                    "type": "AUTO",
                    "buildingName": "",
                    "addressLines": ["Pedda Rushikonda"],
                    "city": "Visakhapatnam",
                    "state": "Andhra pradesh",
                    "postal": "530045",
                    "country": "IN",
                    "phones": [],
                    "mobiles": [],
                    "geoCode": "",
                    "description": "For Testing through Automation",
                    "initialNote": "Testing purposes through Automation",
                    "entity": "0000-0000-0000",
                    "notes": [{"note": "Testing purposes"}]
                }
        print(json.dumps(payload))
        resp = setup_prov_controller.add_location(payload)
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

        # This to edit Location
        editing_payload = {
                          "addressLines": [
                            "Madhurawada",
                            ""
                          ],
                          "buildingName": "",
                          "city": "Visakhapatnam",
                          "country": "IN",
                          "description": "Candela Testing",
                          "entity": "0000-0000-0000",
                          "geoCode": "",
                          "mobiles": [],
                          "name": "Candela IND",
                          "notes": [],
                          "phones": [],
                          "postal": "530048",
                          "state": "Andhra Pradesh",
                          "type": "SERVICE"
                        }
        print(json.dumps(editing_payload))
        resp = setup_prov_controller.edit_location(editing_payload, location_id)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov edited location", body=body)
        if resp.status_code != 200:
            assert False
        entitiy = json.loads(resp.text)
        print(entitiy)

        resp = setup_prov_controller.get_location_by_id(location_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov edited location-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_prov_controller.delete_location(location_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created location-delete", body=body)
        if resp.status_code != 200:
            assert False

@pytest.mark.ow_sanity_lf
@pytest.mark.uc_sanity
@pytest.mark.owprov_api_tests
@pytest.mark.owprov_api_venue
@allure.feature("SDK PROV REST API")
class TestProvAPIVenue(object):

    # Venue related Test cases
    @pytest.mark.prov_api_venue
    def test_get_venue(self, setup_prov_controller):
        resp = setup_prov_controller.get_venue()
        print(resp.json())
        allure.attach(name="venue", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.prov_api_venue_test
    def test_prov_service_create_edit_delete_venue(self, setup_prov_controller, testbed):
        """
            Test the create venue in provision Service
        """
        payload = {
                      "description": "For testing Purposes",
                      "entity": "6a657863-9940-4303-ac68-4cc10d3078ec",
                      "location": "",
                      "name": "Testing Prov",
                      "notes": [
                        {
                          "note": "For testing Purposes"
                        }
                      ],
                      "parent": "",
                      "rrm": "inherit"
                    }
        print(json.dumps(payload))
        resp = setup_prov_controller.add_venue(payload)
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

        # This to edit venue
        editing_payload = {
                          "description": "For testing Purposes through Automation",
                          "location": "",
                          "name": "Testing Prov",
                          "notes": [],
                          "rrm": "inherit",
                          "sourceIP": []
                        }
        print(json.dumps(editing_payload))
        resp = setup_prov_controller.edit_venue(editing_payload, venue_id)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov edited venue", body=body)
        if resp.status_code != 200:
            assert False
        entitiy = json.loads(resp.text)
        print(entitiy)

        resp = setup_prov_controller.get_venue_by_id(venue_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov edited venue-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_prov_controller.delete_venue(venue_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created venue-delete", body=body)
        if resp.status_code != 200:
            assert False

@pytest.mark.ow_sanity_lf
@pytest.mark.uc_sanity
@pytest.mark.owprov_api_tests
@pytest.mark.owprov_api_maps
@allure.feature("SDK PROV REST API")
class TestProvAPIMaps(object):

    # Maps related Test cases
    @pytest.mark.prov_api_maps
    def test_get_map(self, setup_prov_controller):
        resp = setup_prov_controller.get_map()
        print(resp.json())
        allure.attach(name="Maps", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.prov_api_maps
    def test_prov_service_maps_create_edit_delete(self, setup_prov_controller, testbed):
        """
                    Test the create Map in provision Service
                """
        payload = {
                  "access": {
                    "list": []
                  },
                  "created": 1654266780,
                  "creator": "11111111-0000-0000-6666-999999999999",
                  "data": "{\"elements\":[{\"id\":\"entity/0000-0000-0000\",\"position\":{\"x\":788.0001984205973,\"y\":-228}},"
                          "{\"id\":\"entity/0d3b713c-579f-4449-b005-980fc45266f7\",\"position\":{\"x\":125.00091086366538,\"y\":110}},"
                          "{\"id\":\"entity/25e3781c-ff89-4060-98de-72f2f469ece7\",\"position\":{\"x\":0.00013680958416162147,\"y\":220}},"
                          "{\"id\":\"venue/d25b862d-7211-4f5d-8980-eb796cf90259\",\"position\":{\"x\":0.0009741442442360648,\"y\":330}},"
                          "{\"id\":\"entity/3bf7563a-3d9d-11ec-bc4b-6ed02b842da1\",\"position\":{\"x\":375.0004521666363,\"y\":110}},"
                          "{\"id\":\"entity/6a657863-9940-4303-ac68-4cc10d3078ec\",\"position\":{\"x\":633.0000704105611,\"y\":310}},"
                          "{\"id\":\"entity/7ef6dd8e-5ad3-47d6-951f-681adcf2171c\",\"position\":{\"x\":857.0000877260527,\"y\":184}},"
                          "{\"id\":\"entity/da165a23-2562-4a1a-b0c5-8f6e955a2e01\",\"position\":{\"x\":1125.000287727392,\"y\":110}},"
                          "{\"id\":\"venue/b7c1825b-2f25-41b7-8a39-b51b07a5bc64\",\"position\":{\"x\":1339.0000824838032,\"y\":220}},"
                          "{\"id\":\"entity/e6223c6a-c150-43ea-8286-f2d6395e6d65\",\"position\":{\"x\":1625.000942559204,\"y\":110}},"
                          "{\"id\":\"entity/4002042d-b2a7-4a74-bde3-10229ab889a3\",\"position\":{\"x\":1093.0008368135925,\"y\":592}},"
                          "{\"id\":\"entity/c3993947-f5af-4530-9f6e-72edb767abfe\",\"position\":{\"x\":1501.0009763642392,\"y\":462}},"
                          "{\"id\":\"entity/ee468f28-465d-47bc-8ffe-b02678450fd8\",\"position\":{\"x\":1875.0002469570716,\"y\":220}},"
                          "{\"id\":\"device/903cb3bb24df\",\"position\":{\"x\":354.0006993336034,\"y\":264}},"
                          "{\"id\":\"device/68215f9d076a\",\"position\":{\"x\":887.0006396562085,\"y\":352}}],\"zoom\":0.5,\"position\":[-100.25009594166397,168],\"rootNode\":\"entity/0000-0000-0000\"}",
                  "description": "",
                  "entity": "",
                  "id": "d24b07e9-9925-47d7-b7e6-4cc28fb11603",
                  "managementPolicy": "",
                  "modified": 1654266955,
                  "name": "Maps from API Automation",
                  "notes": [],
                  "tags": [],
                  "venue": "",
                  "visibility": "public"
                }
        print(json.dumps(payload))
        resp = setup_prov_controller.add_map(payload)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create Map", body=body)
        if resp.status_code != 200:
            assert False
        map = json.loads(resp.text)
        print(map)
        map_id = map['id']

        resp = setup_prov_controller.get_map_by_id(map_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create Map-verify", body=body)
        if resp.status_code != 200:
            assert False

        # This to edit Map
        editing_payload = {
                          "access": {
                            "list": []
                          },
                          "created": 1654267598,
                          "creator": "11111111-0000-0000-6666-999999999999",
                          "data": "{\"elements\":[{\"id\":\"entity/0000-0000-0000\",\"position\":{\"x\":742.0002986856452,\"y\":-258}},"
                                  "{\"id\":\"entity/0d3b713c-579f-4449-b005-980fc45266f7\",\"position\":{\"x\":125.0000746112698,\"y\":110}},"
                                  "{\"id\":\"entity/25e3781c-ff89-4060-98de-72f2f469ece7\",\"position\":{\"x\":0.000987247185699772,\"y\":220}},"
                                  "{\"id\":\"venue/d25b862d-7211-4f5d-8980-eb796cf90259\",\"position\":{\"x\":0.00015366265594566887,\"y\":330}},"
                                  "{\"id\":\"entity/3bf7563a-3d9d-11ec-bc4b-6ed02b842da1\",\"position\":{\"x\":375.00078943444134,\"y\":110}},"
                                  "{\"id\":\"entity/6a657863-9940-4303-ac68-4cc10d3078ec\",\"position\":{\"x\":625.0001373023756,\"y\":110}},"
                                  "{\"id\":\"entity/7ef6dd8e-5ad3-47d6-951f-681adcf2171c\",\"position\":{\"x\":995.0002519718007,\"y\":390}},"
                                  "{\"id\":\"entity/da165a23-2562-4a1a-b0c5-8f6e955a2e01\",\"position\":{\"x\":1125.0005714344913,\"y\":110}},"
                                  "{\"id\":\"venue/b7c1825b-2f25-41b7-8a39-b51b07a5bc64\",\"position\":{\"x\":1125.0000846706366,\"y\":220}},"
                                  "{\"id\":\"entity/e6223c6a-c150-43ea-8286-f2d6395e6d65\",\"position\":{\"x\":1625.0007765709465,\"y\":110}},"
                                  "{\"id\":\"entity/4002042d-b2a7-4a74-bde3-10229ab889a3\",\"position\":{\"x\":1455.000216347443,\"y\":426}},"
                                  "{\"id\":\"entity/c3993947-f5af-4530-9f6e-72edb767abfe\",\"position\":{\"x\":1625.0006288181921,\"y\":220}},"
                                  "{\"id\":\"entity/ee468f28-465d-47bc-8ffe-b02678450fd8\",\"position\":{\"x\":1875.0006116378358,\"y\":220}},"
                                  "{\"id\":\"device/903cb3bb24df\",\"position\":{\"x\":790.000930605748,\"y\":328}},"
                                  "{\"id\":\"device/68215f9d076a\",\"position\":{\"x\":1125.0006631675788,\"y\":330}}],\"zoom\":0.5,\"position\":[-236.25019132512296,168],\"rootNode\":\"entity/0000-0000-0000\"}",
                          "description": "",
                          "entity": "",
                          "id": "34cfd185-da33-4885-85c7-1fef21900570",
                          "managementPolicy": "",
                          "modified": 1654267727,
                          "name": "Maps from API Automation after Edit",
                          "notes": [],
                          "tags": [],
                          "venue": "",
                          "visibility": "public"
                        }
        print(json.dumps(editing_payload))
        resp = setup_prov_controller.edit_map(editing_payload, map_id)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov edited venue", body=body)
        if resp.status_code != 200:
            assert False
        map = json.loads(resp.text)
        print(map)

        resp = setup_prov_controller.get_map_by_id(map_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov edited Map-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_prov_controller.delete_map(map_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created Map-delete", body=body)
        if resp.status_code != 200:
            assert False

@pytest.mark.ow_sanity_lf
@pytest.mark.uc_sanity
@pytest.mark.owprov_api_tests
@pytest.mark.owprov_api_operators
@allure.feature("SDK PROV REST API")
class TestProvAPIOperator(object):

    @pytest.mark.prov_api_operator_test
    def test_get_operator(self, setup_prov_controller):
        resp = setup_prov_controller.get_operator()
        print(resp.json())
        allure.attach(name="Operators", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.prov_api_operator_test
    def test_prov_service_create_edit_delete_operator(self, setup_prov_controller, testbed):
        """
            Test the create Operator in provision Service
        """
        payload = {
                  "name": "Testing API through Automation",
                  "deviceRules": {
                    "rrm": "inherit",
                    "rcOnly": "inherit",
                    "firmwareUpgrade": "inherit"
                  },
                  "sourceIP": [],
                  "registrationId": "12345",
                  "description": "Testing API through Automation",
                  "firmwareRCOnly": False,
                  "notes": [
                    {
                      "note": "Testing purposes"
                    }
                  ]
                }
        print(json.dumps(payload))
        resp = setup_prov_controller.add_operator(payload)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create operator", body=body)
        if resp.status_code != 200:
            assert False
        operator = json.loads(resp.text)
        print(operator)
        operator_id = operator['id']

        resp = setup_prov_controller.get_operator_by_id(operator_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create operator-verify", body=body)
        if resp.status_code != 200:
            assert False

        # This to edit operator
        editing_payload = {
                          "name": "Testing API through Automation after edit",
                          "description": "Testing API through Automation after edit",
                          "deviceRules": {
                            "firmwareUpgrade": "inherit",
                            "rcOnly": "inherit",
                            "rrm": "inherit"
                          },
                          "sourceIP": [],
                          "registrationId": "12345",
                          "notes": []
                        }
        print(json.dumps(editing_payload))
        resp = setup_prov_controller.edit_operator(editing_payload, operator_id)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov edited operator", body=body)
        if resp.status_code != 200:
            assert False
        operator = json.loads(resp.text)
        print(operator)

        resp = setup_prov_controller.get_operator_by_id(operator_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov edited operator-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_prov_controller.delete_operator(operator_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created operator-delete", body=body)
        if resp.status_code != 200:
            assert False

@pytest.mark.ow_sanity_lf
@pytest.mark.uc_sanity
@pytest.mark.owprov_api_tests
@pytest.mark.owprov_api_service_class
@allure.feature("SDK PROV REST API")
class TestProvAPIEntity(object):

    @pytest.mark.prov_api_service_class_test
    def test_prov_service_create_edit_delete_service_class(self, setup_prov_controller, testbed):
        """
            Test the create Service class in provision Service (USE CASE)
        """
        payload = {
                  "name": "Testing API through Automation",
                  "deviceRules": {
                    "rrm": "inherit",
                    "rcOnly": "inherit",
                    "firmwareUpgrade": "inherit"
                  },
                  "sourceIP": [],
                  "registrationId": "12345",
                  "description": "Testing API through Automation",
                  "firmwareRCOnly": False,
                  "notes": [
                    {
                      "note": "Testing purposes"
                    }
                  ]
                }
        print(json.dumps(payload))
        resp = setup_prov_controller.add_operator(payload)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create operator", body=body)
        if resp.status_code != 200:
            assert False
        operator = json.loads(resp.text)
        print(operator)
        operator_id = operator['id']

        resp = setup_prov_controller.get_operator_by_id(operator_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create operator-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_prov_controller.get_service_class_by_operator_id(operator_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov Service Class-verify", body=body)
        if resp.status_code != 200:
            assert False

        payload = {
                  "name": "Testing Purposes through API Automation",
                  "billingCode": "12345",
                  "description": "Testing Purposes through API Automation",
                  "period": "monthly",
                  "cost": 0,
                  "currency": "USD",
                  "notes": [
                    {
                      "note": "Testing Purposes through API Automation"
                    }
                  ],
                  "operatorId": operator_id
                }
        print(json.dumps(payload))
        resp = setup_prov_controller.add_service_class(payload)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov create Service Class", body=body)
        if resp.status_code != 200:
            assert False
        service_class = json.loads(resp.text)
        print(service_class)
        service_class_id = service_class['id']

        resp = setup_prov_controller.get_service_class_by_id(service_class_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov  created Service Class-verify", body=body)
        if resp.status_code != 200:
            assert False

        # This to edit operator
        editing_payload = {
                          "name": "Testing Purposes through API Automation",
                          "billingCode": "12345",
                          "description": "Testing Purposes through API Automation after editing",
                          "period": "monthly",
                          "cost": 0,
                          "currency": "USD",
                          "notes": []
                        }
        print(json.dumps(editing_payload))
        resp = setup_prov_controller.edit_service_class(editing_payload, service_class_id)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov edited service_class", body=body)
        if resp.status_code != 200:
            assert False
        service_class = json.loads(resp.text)
        print(service_class)

        resp = setup_prov_controller.get_service_class_by_id(service_class_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov edited service_class-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_prov_controller.delete_service_class(service_class_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created service_class-delete", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_prov_controller.delete_operator(operator_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Prov created operator-delete", body=body)
        if resp.status_code != 200:
            assert False

@pytest.mark.ow_sanity_lf
@pytest.mark.uc_sanity
@pytest.mark.owprov_api_tests
@pytest.mark.owprov_api_usecase
@allure.feature("SDK PROV REST API")
class TestProvAPIUseCase(object):

    @pytest.mark.prov_api_usecase_test
    def test_prov_service_use_case(self, setup_prov_controller, testbed):
        """
            Test to create use case in provision Service
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