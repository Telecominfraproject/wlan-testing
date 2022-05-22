"""

    UCentral FMS Services Rest API Tests

"""

import string
import random

import pytest
import json
import allure


@pytest.mark.uc_sanity
@allure.feature("SDK REST API")
class TestUcentralFMSService(object):

    @pytest.mark.system_info_fms
    def test_system_info_fms(self, setup_controller):
        system_info = setup_controller.get_system_fms()
        print(system_info.json())
        allure.attach(name="system info", body=str(system_info.json()), attachment_type=allure.attachment_type.JSON)
        assert system_info.status_code == 200