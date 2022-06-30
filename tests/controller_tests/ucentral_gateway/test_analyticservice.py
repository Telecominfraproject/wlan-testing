"""

    Analytics Service Rest API Tests

"""

import datetime
import random

import pytest
import json
import allure


@pytest.mark.ow_sanity_lf
@pytest.mark.uc_sanity
@pytest.mark.ow_sdk_tests
@pytest.mark.ow_sdk_load_tests
@pytest.mark.owa_api_tests
@allure.parent_suite("OpenWifi SDK Tests")
@allure.suite("OpenWIfi Analytics Service Tests")
class TestUcentralAnalyticsService(object):

    @pytest.mark.owa_get_boards
    @allure.title("GET List of Boards")
    def test_analytics_service_boards(self, setup_owan_controller):
        """
            Test List of Boards Retrieved from Analytic Service
        """
        resp=setup_owan_controller.get_boards()
        assert resp.status_code == 200

    @pytest.mark.owa_boards_crud
    @allure.title("CRUD Board")
    def test_ananlytics_service_create_edit_delete_board(self, setup_owan_controller, testbed):
        """
            Test the create board in Analytics Service
        """
        payload={
            "name": "Test-Board",
            "description": "Check Create Board API using Automation Test",
            "notes": [
                {
                    "note": "Test-Note"
                }
            ],
            "tags": [],
            "venueList": [
                {
                    "id": "4db9d9af-287d-438c-bef4-c3889a54296c",
                    "name": "check-create-board-sub-venue",
                    "description": "test-create-board-API",
                    "retention": 604800,
                    "interval": 60,
                    "monitorSubVenues": True
                }
            ]
        }
        # print(json.dumps(payload))
        resp=setup_owan_controller.add_board(payload)
        # body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        if resp.status_code != 200:
            assert False
        board=json.loads(resp.text)
        print(board)
        board_id=board['id']

        # Retrieve a Created Board
        resp=setup_owan_controller.get_board_by_id(board_id)
        # body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        if resp.status_code != 200:
            assert False

        # Edit  board
        update_payload={
            "name": "Test-Board",
            "description": "Check Edit Board API using Automation Test",
            "notes": [
                {
                    "note": "This is a Board Edit Test "
                }
            ],
            "tags": [],
            "venueList": [
                {
                    "id": "4db9d9af-287d-438c-bef4-c3889a54296c",
                    "name": "check-create-board-sub-venue",
                    "description": "test-create-board-API",
                    "retention": 609600,
                    "interval": 120,
                    "monitorSubVenues": True
                }
            ]
        }
        print(json.dumps(update_payload))
        resp=setup_owan_controller.edit_board(board_id, update_payload)
        # body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        if resp.status_code != 200:
            assert False
        board=json.loads(resp.text)
        print(board)
        board_id=board['id']

        # Retrieve an Updated Board
        resp=setup_owan_controller.get_board_by_id(board_id)
        # body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        if resp.status_code != 200:
            assert False

        # Delete a Board
        resp=setup_owan_controller.delete_board(board_id)
        # body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        if resp.status_code != 200:
            assert False

    @pytest.mark.owa_get_board_devices
    @allure.title("GET Board Devices")
    def test_analytics_service_get_board_devices(self, setup_owan_controller):
        """
            Test Retrieved Devices from the Board
        """
        response=setup_owan_controller.get_boards()
        if response.status_code == 200:
            res_dict=json.loads(response.text)
            if len(res_dict["boards"]) > 0:
                boards=res_dict["boards"]
                board_id=boards[random.randint(0, len(boards))]["id"]
                resp=setup_owan_controller.get_board_devices(board_id)
            assert response.status_code == 200
        else:
            assert response.status_code == 200, str(response.text)

    @pytest.mark.owa_get_board_data_bytime
    @allure.title("GET Board Data by time")
    def test_analytics_service_get_board_data_bytime(self, setup_owan_controller):
        """
            Test Retrieving of a Board Data from timestamp
        """
        fd=str(datetime.datetime.now().replace(microsecond=0).timestamp())
        from_date=fd.split(".")[0]
        td=str((datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=1)).timestamp())
        to_date=td.split(".")[0]
        response = setup_owan_controller.get_boards()
        if response.status_code == 200:
            res_dict = json.loads(response.text)
            if len(res_dict["boards"]) > 0:
                boards = res_dict["boards"]
                board_id = boards[random.randint(0, len(boards))]["id"]
                response = setup_owan_controller.get_board_data_bytime(board_id=board_id, from_date=from_date, to_date=to_date)
            # print(response.json())
            assert response.status_code == 200
        else:
            assert False, str(response.text)

    @pytest.mark.owa_delete_board_data_bytime
    @allure.title("DELETE Board Data by time")
    def test_analytics_service_delete_board_data_bytime(self, setup_owan_controller):
        """
            Test Deleting a Board Data for given time period
        """
        fd = str(datetime.datetime.now().replace(microsecond=0).timestamp())
        from_date = fd.split(".")[0]
        td = str((datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=1)).timestamp())
        to_date = td.split(".")[0]
        response = setup_owan_controller.get_boards()
        if response.status_code == 200:
            res_dict = json.loads(response.text)
            if len(res_dict["boards"]) > 0:
                boards = res_dict["boards"]
                board_id = boards[random.randint(0, len(boards))]["id"]
                response = setup_owan_controller.delete_board_data_bytime(board_id=board_id, from_date=from_date, to_date=to_date)
                # print(response.json())
            assert response.status_code == 200
        else:
            assert False, str(response.text)

    @pytest.mark.owa_get_wificlients_history
    @allure.title("GET WifiClients From a Venue")
    def test_analytics_service_get_wificlients_history(self, setup_owan_controller):
        """
            Test Retrieving of Wifi Clients from a Venue
        """
        resp=setup_owan_controller.get_wificlients_history(venue_id="38b2492e-23e0-4ac7-873f-7a09ca9d9de6")
        # print(resp.json())
        assert resp.status_code == 200

    @pytest.mark.owa_get_wifi_client_history
    @allure.title("GET WifiClient History")
    def test_analytics_service_get_wifi_client_history(self, setup_owan_controller):
        """
            Test Retrieveing a Wifi Client from a Venue
        """
        resp=setup_owan_controller.get_wifi_client_history(client_mac="04f02126128d", venue_id="38b2492e-23e0-4ac7-873f-7a09ca9d9de6")
        # print(resp.json())
        assert resp.status_code == 200

    @pytest.mark.owa_delete_wifi_client_history
    @allure.title("DELETE WifiClient History")
    def test_analytics_service_delete_wifi_client_history(self, setup_owan_controller):
        """
            Test Removing of a Wifi Client from a Venue
        """
        resp=setup_owan_controller.delete_wifi_client_history(client_mac="04f02126128d", venue_id="38b2492e-23e0-4ac7-873f-7a09ca9d9de6")
        # print(resp.json())
        assert resp.status_code == 200

    @pytest.mark.owa_get_system_info
    @allure.title("GET System Info - OW Analytics Service")
    def test_analytics_service_get_system_info(self, setup_owan_controller):
        """
            Test System Command
        """
        system_info=setup_owan_controller.get_system_info(command="info")
        # print(system_info.json())
        assert system_info.status_code == 200

    @pytest.mark.owa_post_system_info
    @allure.title("POST System Command - Analytics Service")
    def test_analytics_service_post_system_info(self, setup_owan_controller):
        """
            Test System command
        """
        system_info=setup_owan_controller.post_system_info(command="getsubsystemnames")
        # print(system_info.json())
        assert system_info.status_code == 200
