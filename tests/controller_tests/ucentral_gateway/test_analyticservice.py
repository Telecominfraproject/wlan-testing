"""

    Analytics Service Rest API Tests

"""

import string
import random

import pytest
import json
import allure


@pytest.mark.ow_sanity_lf
@pytest.mark.uc_sanity
@pytest.mark.owa_api_tests
@allure.feature("SDK ANALYTICS REST API")
class TestUcentralAnalyticsService(object):

    @pytest.mark.owa_get_boards
    def test_analytics_service_boards(self, setup_owan_controller):
        """
            Test List of Boards Retrieved from Analytic Service
        """
        resp = setup_owan_controller.get_boards()
        print(resp.json())
        allure.attach(name="Retrieved List of Boards", body=str(resp.json()), attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.owa_boards_crud
    def test_ananlytics_service_create_edit_delete_board(self, setup_owan_controller, testbed):
        """
            Test the create board in Analytics Service
        """
        payload = {
            "allOf": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "string",
                "description": "string",
                "notes": [
                    {
                        "created": 0,
                        "createdBy": "string",
                        "note": "string"
                    }
                ],
                "created": 0,
                "modified": 0,
                "tags": [
                    0
                ]
            },
            "venueList": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "string",
                    "description": "string",
                    "retention": 0,
                    "interval": 0,
                    "monitorSubVenues": true
                }
            ]
        }
        print(json.dumps(payload))
        resp = setup_owan_controller.add_board(payload)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="create board in analytics", body=body)
        if resp.status_code != 200:
            assert False
        board = json.loads(resp.text)
        print(board)
        board_id = board['id']

        resp = setup_owan_controller.get_board_by_id(board_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Analytics create venue-verify", body=body)
        if resp.status_code != 200:
            assert False

        # This to edit board
        editing_payload = {
            "allOf": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "string",
                "description": "string",
                "notes": [
                    {
                        "created": 0,
                        "createdBy": "string",
                        "note": "string"
                    }
                ],
                "created": 0,
                "modified": 0,
                "tags": [
                    0
                ]
            },
            "venueList": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "string",
                    "description": "string",
                    "retention": 0,
                    "interval": 0,
                    "monitorSubVenues": true
                }
            ]
        }
        print(json.dumps(editing_payload))
        resp = setup_owan_controller.edit_board(editing_payload, board_id)
        allure.attach(name="response: ", body=str(resp.json()))
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Analytics edited board", body=body)
        if resp.status_code != 200:
            assert False
        entitiy = json.loads(resp.text)
        print(entitiy)

        resp = setup_owan_controller.get_board_by_id(board_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Verify GET Board", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_owan_controller.delete_board(board_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Verify DELETE board", body=body)
        if resp.status_code != 200:
            assert False

    @pytest.mark.owa_get_board_devices
    def test_analytics_service_get_board_devices(self, setup_owan_controller):
        """
            Test Retrieved Devices from the Board
        """
        resp=setup_owan_controller.get_board_devices()
        print(resp.json())
        allure.attach(name="Verify Devices Retrieved from the Board", body=str(resp.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.owa_get_board_data_bytime
    def test_analytics_service_get_board_data_bytime(self, setup_owan_controller):
        """
            Test Retrieving of Board Data from timestamp
        """
        resp=setup_owan_controller.get_board_data_bytime(board_id='', from_date=1656433571, to_date=1656437971)
        print(resp.json())
        allure.attach(name="Verify GET Board Data Retrieved as per time period ", body=str(resp.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.owa_delete_board_data_bytime
    def test_analytics_service_get_board_data_bytime(self, setup_owan_controller):
        """
            Test Retrieving of Board Data from timestamp
        """
        resp=setup_owan_controller.delete_board_data_bytime(board_id='', from_date=1656433571, to_date=1656437971)
        print(resp.json())
        allure.attach(name="Verify DELETE Board Data as per time period ", body=str(resp.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.owa_get_wificlients_history
    def test_analytics_service_get_wificlients_history(self, setup_owan_controller):
        """
            Test Retrieving of Wifi Clients from a Venue
        """
        resp=setup_owan_controller.get_wificlients_history(venue_id="")
        print(resp.json())
        allure.attach(name="Verify GET Wifi clients from the Venue ", body=str(resp.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.owa_get_wifi_client_history
    def test_analytics_service_get_wifi_client_history(self, setup_owan_controller):
        """
            Test Retrieveing a Wifi Client from a Venue
        """
        resp=setup_owan_controller.get_wifi_client_history(client_mac="")
        print(resp.json())
        allure.attach(name="Verify GET Wifi clients from the Venue ", body=str(resp.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.owa_delete_wifi_client_history
    def test_analytics_service_delete_wifi_client_history(self, setup_owan_controller):
        """
            Test Removing of a Wifi Client from a Venue
        """
        resp=setup_owan_controller.delete_wifi_client_history(client_mac="")
        print(resp.json())
        allure.attach(name="Verify DELETE a Wifi client from the Venue ", body=str(resp.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert resp.status_code == 200

    @pytest.mark.owa_get_system_info
    def test_analytics_service_get_system_info(self, setup_owan_controller):
        """
            Test System Command
        """
        system_info=setup_owan_controller.get_system_info(command="info")
        print(system_info.json())
        allure.attach(name="system info", body=str(system_info.json()), attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200

    @pytest.mark.owa_post_system_info
    def test_analytics_service_post_system_info(self, setup_owan_controller):
        """
            Test System command
        """
        system_info=setup_owan_controller.post_system_info(command="getsubsystemnames")
        print(system_info.json())
        allure.attach(name="Verify a system command: getsubsystemnames", body=str(system_info.json()), attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200
