"""

    UCentral Analytics Service OPEN API Tests

"""

import allure
import pytest


@pytest.mark.uc_sanity
@pytest.mark.ow_sdk_load_tests
@allure.parent_suite("OpenWifi SDK Tests")
@allure.suite("OpenWifi Analytics Service Tests")
class TestUcentralAnalyticService(object):

    @pytest.mark.system_info_analytics
    @allure.title("Get System Info Analytics")
    def test_analytics_system_info(self, get_target_object):
        system_info = get_target_object.controller_library_object.get_system_ow_analytics()
        print(system_info.json())
        allure.attach(name="GET - Analytics system info:\n", body=str(system_info.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200

    @pytest.mark.get_boards
    @allure.title("GET Boards")
    def test_analytics_get_boards(self, get_target_object):
        response = get_target_object.controller_library_object.get_boards()
        print(response.json())
        allure.attach(name="GET - List of Boards :\n", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.add_board
    @allure.title("Create a Board")
    def test_analytics_create_board(self, get_target_object):
        response = get_target_object.controller_library_object.create_board()
        print(response.json())
        allure.attach(name="POST - Create a Board:\n", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.retireve_board
    @allure.title("Retrieve a Board")
    def test_analytics_get_board(self, get_target_object):
        response = get_target_object.controller_library_object.get_board()
        print(response.json())
        allure.attach(name="PUT - Update a Board:\n", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.edit_board
    @allure.title("Update a Board")
    def test_analytics_update_board(self, get_target_object):
        response = get_target_object.controller_library_object.edit_board()
        print(response.json())
        allure.attach(name="PUT - Update a Board:\n", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.remove_board
    @allure.title("Remove a Board")
    def test_analytics_delete_board(self, get_target_object):
        response = get_target_object.controller_library_object.remove_board()
        print(response.json())
        allure.attach(name="DEL - Update a Board:\n", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.get_board_devices
    @allure.title("GET Board Devices")
    def test_analytics_create_board(self, get_target_object):
        response = get_target_object.controller_library_object.get_board_devices()
        print(response.json())
        allure.attach(name="GET - Devices in a Board:\n", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.get_wificlients_history
    @allure.title("GET Wifi Clients History")
    def test_analytics_get_wificlients_history(self, get_target_object):
        response = get_target_object.controller_library_object.get_wificlients_history()
        print(response.json())
        allure.attach(name="GET - Wifi Clients History :\n", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.get_wificlient_history
    @allure.title("GET Wifi Client History")
    def test_analytics_get_wificlient_history(self, get_target_object):
        response = get_target_object.controller_library_object.get_wificlient_history()
        print(response.json())
        allure.attach(name="GET - A Wifi Client History :\n", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.remove_wificlient_history
    @allure.title("DELETE Wifi Client History")
    def test_analytics_remove_wificlient_history(self, get_target_object):
        response = get_target_object.controller_library_object.remove_wificlient_history()
        print(response.json())
        allure.attach(name="DEL - A Wifi Client History :\n", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.retireve_board_timepoints
    @allure.title("Retrieve a Board within a time period")
    def test_analytics_get_board_timepoints(self, get_target_object):
        response = get_target_object.controller_library_object.retireve_board_timepoints()
        print(response.json())
        allure.attach(name="GET - Retrieve a Board Data within a specific period:\n", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.remove_board_timepoints
    @allure.title("Retrieve a Board within a time period")
    def test_analytics_remove_board_timepoints(self, get_target_object):
        response = get_target_object.controller_library_object.remove_board_timepoints()
        print(response.json())
        allure.attach(name="DEL - Retrieve a Board Data within a specific period:\n", body=str(response.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200

    @pytest.mark.post_system_commands
    @allure.title("Perform some system wide commands")
    def test_analytics_post_system_commands(self, get_target_object):
        system_info = get_target_object.controller_library_object.post_system_commands()
        print(system_info.json())
        allure.attach(name="POST - Analytics system info:\n", body=str(system_info.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200

    @pytest.mark.get_system_commands
    @allure.title("Retrieve different values from the running service")
    def test_analytics_get_system_commands(self, get_target_object):
        system_info = get_target_object.controller_library_object.get_system_commands()
        print(system_info.json())
        allure.attach(name="GET - Analytics system info:\n", body=str(system_info.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200