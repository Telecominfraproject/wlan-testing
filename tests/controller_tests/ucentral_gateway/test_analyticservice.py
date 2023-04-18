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

    @pytest.mark.analytics_add_board
    @allure.title("Create a Board")
    def test_analytics_create_board(self, get_target_object):
        system_info = get_target_object.controller_library_object.get_system_ow_analytics()
        print(system_info.json())
        allure.attach(name="GET - Analytics system info:\n", body=str(system_info.json()),
                      attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200
