"""

    Analytics Service Rest API Tests

"""

import string
import random

import pytest
import json
import allure


# @pytest.mark.ow_sanity_lf
# @pytest.mark.uc_sanity
# @pytest.mark.owa_api_tests
# @allure.feature("SDK ANALYTICS REST API")
class TestUcentralAnalyticsisionService(object):

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
        allure.attach(name="Analytics edited board-verify", body=body)
        if resp.status_code != 200:
            assert False

        resp = setup_owan_controller.delete_board(board_id)
        body = resp.url + "," + str(resp.status_code) + ',' + resp.text
        allure.attach(name="Analytics created board-delete", body=body)
        if resp.status_code != 200:
            assert False