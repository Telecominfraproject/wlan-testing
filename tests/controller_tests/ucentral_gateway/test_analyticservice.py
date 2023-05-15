"""

    UCentral Analytics Service OPEN API Tests

"""
import datetime
import json
import random
import string
import time

import allure
import pytest
import logging


@pytest.mark.uc_sanity
@pytest.mark.ow_sdk_tests
@pytest.mark.ow_analytics_api_tests
@allure.parent_suite("OpenWifi SDK Tests")
@allure.suite("OpenWifi Analytics Service Tests")
class TestUcentralAnalyticService(object):
    boards, clients = [], []
    board_id, entity_id = "", "aefb7254-571f-42c3-be51-39a2b1441234"

    @pytest.mark.system_info_analytics
    @allure.title("Get System Info Analytics")
    def test_analytics_system_info(self, get_target_object):
        response = get_target_object.controller_library_object.get_system_ow_analytics()
        logging.info(response.json())
        allure.attach(name=f"Response: {response.status_code} - {response.reason}", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.get_boards
    @allure.title("Retrieve list of available boards")
    def test_analytics_get_boards(self, get_target_object):
        response = get_target_object.analytics_library_object.get_boards()
        logging.info(response.json())
        if response.status_code == 200:
            body = response.json()
            self.boards = body["boards"]
        allure.attach(name=f"Response: {response.status_code} - {response.reason}", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.get_board_devices
    @allure.title("GET Board Devices")
    def test_analytics_get_board_devices(self, get_target_object):
        response = get_target_object.analytics_library_object.get_boards()
        logging.info(response.json())
        if response.status_code == 200:
            body = response.json()
            self.boards = body["boards"]
        else:
            assert response.status_code == 200, "Failed in getting boards data"
        if len(self.boards) > 0:
            response = get_target_object.analytics_library_object.get_board_devices(
                board_id=self.boards[random.randint(0, len(self.boards)-1)]['id'])
            logging.info(response.json())
            allure.attach(name=f"Response: {response.status_code} - {response.reason}", body=str(response.json()),
                          attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 200, "Failed in getting devices in a board"
        else:
            assert False, "No Boards Available"

    @pytest.mark.create_board
    @allure.title("Create a Board")
    def test_analytics_create_board(self, get_target_object):
        resp, venue_list = {}, []
        temp_response = get_target_object.prov_library_object.get_entity_by_id(TestUcentralAnalyticService.entity_id)
        if temp_response.status_code == 200:
            resp = temp_response.json()
            venue_list = resp['venues']
        else:
            assert temp_response.status_code == 200, "Failed in getting Venues"
        data = {
            "name": "Test-Create-Board-" + "".join(random.choices(string.ascii_letters, k=6)),
            "description": "Create Board API using Automation Test",
            "notes": [
                {
                    "note": "Test-Note"
                }
            ],
            "tags": [],
            "venueList": [
                {
                    "id": venue_list[random.randint(0, len(venue_list) - 1)],
                    "name": "Test-create-board-in-a-sub-venue",
                    "description": "test-create-board-API",
                    "retention": 604800,
                    "interval": 60,
                    "monitorSubVenues": True
                }
            ]
        }
        response = get_target_object.analytics_library_object.create_board(data)
        logging.info(response.json())
        allure.attach(name=f"Response: {response.status_code} - {response.reason}", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        if response.status_code == 200:
            TestUcentralAnalyticService.board_id = response.json()['id']
        assert response.status_code == 200, "Failed in creating a board"

    @pytest.mark.get_board
    @allure.title("Retrieve a Board")
    def test_analytics_get_board(self, get_target_object):
        resp = get_target_object.analytics_library_object.get_boards()
        if resp.status_code == 200:
            body = resp.json()
            self.boards = body["boards"]
        else:
            assert resp.status_code == 200, "Failed in getting boards data"
        if TestUcentralAnalyticService.board_id == "" and len(self.boards) > 0:
            response = get_target_object.analytics_library_object.get_board(self.boards[random.randint(0, len(self.boards)-1)])
        else:
            response = get_target_object.analytics_library_object.get_board(TestUcentralAnalyticService.board_id)
        logging.info(response.json())
        allure.attach(name=f"Response: {response.status_code} - {response.reason}", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.update_board
    @allure.title("Update a Board")
    def test_analytics_update_board(self, get_target_object):
        response = get_target_object.analytics_library_object.get_boards()
        if response.status_code == 200:
            body = response.json()
            self.boards = body["boards"]
        else:
            assert response.status_code == 200, "Failed in getting boards data"
        data = {
            "name": "Test-update-board-check-sub-venue",
            "description": "This is a test to check Update board API"
        }
        if TestUcentralAnalyticService.board_id == "" and len(self.boards) > 0:
            response = get_target_object.analytics_library_object.edit_board(board_id=self.boards[random.randint(0, len(self.boards)-1)], payload=data)
        else:
            response = get_target_object.analytics_library_object.edit_board(board_id=TestUcentralAnalyticService.board_id, payload=data)
        logging.info(response.json())
        allure.attach(name=f"Response: {response.status_code} - {response.reason}", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        if response.status_code == 200:
            response1 = get_target_object.analytics_library_object.get_board(response.json()['id'])
            if response1.status_code == 200:
                allure.attach(name=f"Response: {response1.status_code} - {response1.reason}", body=str(response1.json()),
                              attachment_type=allure.attachment_type.JSON)
        else:
            assert response.status_code == 200, "Failed in updating a board"
        assert response.status_code == response1.status_code

    @pytest.mark.remove_board
    @allure.title("Remove a Board")
    def test_analytics_delete_board(self, get_target_object):
        response = get_target_object.analytics_library_object.get_boards()
        if response.status_code == 200:
            body = response.json()
            self.boards = body["boards"]
        else:
            assert response.status_code == 200, "Failed in getting boards data"
        if TestUcentralAnalyticService.board_id == "" and len(self.boards) > 0:
            response = get_target_object.analytics_library_object.delete_board(self.boards[random.randint(0, len(self.boards)-1)]['id'])
        else:
            response = get_target_object.analytics_library_object.delete_board(TestUcentralAnalyticService.board_id)
        if len(response.content) == 0:
            logging.info('Response content is empty')
        allure.attach(name=f"Response: {response.status_code} - {response.reason}", body=response.text,
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.get_wifi_clients_history
    @allure.title("Retrieve WiFi clients history")
    def test_analytics_get_wificlients_history(self, get_target_object):
        resp, venue_list = {}, []
        temp_response = get_target_object.prov_library_object.get_entity_by_id(TestUcentralAnalyticService.entity_id)
        if temp_response.status_code == 200:
            resp = temp_response.json()
            venue_list = resp['venues']
        else:
            assert temp_response.status_code == 200, "Failed in getting Venues"
        if len(venue_list) > 0:
            venue = venue_list[random.randint(0, len(venue_list)-1)]
        else:
            assert False, "No Venues found in selected Entity"
        response = get_target_object.analytics_library_object.get_wifi_clients_history(venue=venue)
        logging.info(response.json())
        if response.status_code == 200:
            TestUcentralAnalyticService.clients = response.json()['entries']
        allure.attach(name="Response:GET - Wifi Clients History ", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.get_wifi_client_history
    @allure.title("Retrieve a Wifi Client History")
    def test_analytics_get_wifi_client_history(self, get_target_object):
        resp, venue_list = {}, []
        if len(TestUcentralAnalyticService.clients) > 0:
            client = TestUcentralAnalyticService.clients[random.randint(0, len(TestUcentralAnalyticService.clients)-1)]
        else:
            client = '04f021d405cc'
        temp_response = get_target_object.prov_library_object.get_entity_by_id(TestUcentralAnalyticService.entity_id)
        if temp_response.status_code == 200:
            resp = temp_response.json()
            venue_list = resp['venues']
        else:
            assert temp_response.status_code == 200, "Failed in getting Venues"
        if len(venue_list) > 0:
            venue = venue_list[random.randint(0, len(venue_list) - 1)]
        else:
            venue = 'eb5c5165-b168-4748-8609-fcabd564b5e3'
        response = get_target_object.analytics_library_object.get_wifi_client_history(client=client, venue=venue)
        logging.info(response.json())
        allure.attach(name=f"Response: {response.status_code} - {response.reason}", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.delete_wifi_client_history
    @allure.title("Delete specific Wifi Client History")
    def test_analytics_remove_wificlient_history(self, get_target_object):
        resp, venue_list = {}, []
        if len(TestUcentralAnalyticService.clients) > 0:
            client = TestUcentralAnalyticService.clients[random.randint(0, len(TestUcentralAnalyticService.clients)-1)]
        else:
            client = '04f021d405cc'
        temp_response = get_target_object.prov_library_object.get_entity_by_id(TestUcentralAnalyticService.entity_id)
        if temp_response.status_code == 200:
            resp = temp_response.json()
            venue_list = resp['venues']
        else:
            assert temp_response.status_code == 200, "Failed in getting Venues"
        if len(venue_list) > 0:
            venue = venue_list[random.randint(0, len(venue_list)-1)]
        else:
            venue = 'eb5c5165-b168-4748-8609-fcabd564b5e3'
        response = get_target_object.analytics_library_object.delete_wifi_client_history(client=client, venue=venue)
        logging.info(response.json())
        allure.attach(name="Response:DEL - A Wifi Client History ", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.retireve_board_timepoints
    @allure.title("Retrieve a Board within a time period")
    def test_analytics_get_board_data(self, get_target_object):
        response = get_target_object.analytics_library_object.get_boards()
        if response.status_code == 200:
            body = response.json()
            self.boards = body["boards"]
        else:
            assert response.status_code == 200, "Failed in getting boards data"
        if TestUcentralAnalyticService.board_id == "":
            response = get_target_object.analytics_library_object.get_board_data(self.boards[random.randint(0, len(self.boards)-1)])
        else:
            response = get_target_object.analytics_library_object.get_board_data(TestUcentralAnalyticService.board_id)
        logging.info(response.json())
        allure.attach(name=f"Response: {response.status_code} - {response.reason}", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.remove_board_timepoints
    @allure.title("Remove a Board within a time period")
    def test_analytics_remove_board_data(self, get_target_object):
        response = get_target_object.analytics_library_object.get_boards()
        if response.status_code == 200:
            body = response.json()
            self.boards = body["boards"]
        else:
            assert response.status_code == 200, "Failed in getting boards data"
        if TestUcentralAnalyticService.board_id == "":
            response = get_target_object.analytics_library_object.delete_board_data(self.boards[random.randint(0, len(self.boards)-1)])
        else:
            response = get_target_object.analytics_library_object.delete_board_data(TestUcentralAnalyticService.board_id)
        logging.info(response.json())
        allure.attach(name=f"Response: {response.status_code} - {response.reason}", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.post_system_commands
    @allure.title("Perform some system wide commands")
    def test_analytics_post_system_commands(self, get_target_object):
        payload = {
            "command": "getsubsystemnames"
        }
        response = get_target_object.analytics_library_object.post_system_commands(payload)
        logging.info(response.json())
        allure.attach(name=f"Response: {response.status_code} - {response.reason}", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.get_system_commands
    @allure.title("Retrieve different values from the running service")
    def test_analytics_get_system_commands(self, get_target_object):
        command = 'info'
        response = get_target_object.analytics_library_object.get_system_commands(command)
        logging.info(response.json())
        allure.attach(name=f"Response: {response.status_code} - {response.reason}", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200
