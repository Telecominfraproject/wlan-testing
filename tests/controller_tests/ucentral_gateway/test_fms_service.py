"""

    UCentral FMS Services Rest API Tests

"""

import allure
import pytest


@pytest.mark.uc_sanity
@pytest.mark.ow_sdk_load_tests
@allure.parent_suite("OpenWifi SDK Tests")
@allure.parent_suite("OpenWifi FMS Service Tests")
class TestUcentralFMSService(object):

    @pytest.mark.system_info_fms
    def test_system_info_fms(self, setup_controller):
        system_info = setup_controller.get_system_fms()
        print(system_info.json())
        allure.attach(name="system info", body=str(system_info.json()), attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200