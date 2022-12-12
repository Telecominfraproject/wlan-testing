"""

    UCentral FMS Services Rest API Tests

"""

import allure
import pytest


@pytest.mark.uc_sanity
@pytest.mark.ow_sdk_load_tests
@allure.parent_suite("OpenWifi SDK Tests")
@allure.suite("OpenWifi FMS Service Tests")
class TestUcentralFMSService(object):

    @pytest.mark.system_info_fms
    @pytest.mark.jk
    @allure.title("Get System Info FMS")
    def test_system_info_fms(self, get_target_object):
        system_info = get_target_object.controller_library_object.get_system_fms()
        print(system_info.json())
        allure.attach(name="system info", body=str(system_info.json()), attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200