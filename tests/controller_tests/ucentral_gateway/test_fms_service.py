"""

    UCentral FMS Services Rest API Tests

"""

import allure
import pytest
import importlib
import time
logging = importlib.import_module("logging")


@allure.parent_suite("SDK Tests")
@allure.suite("FMS Service Tests")
class TestUcentralFMSService(object):

    @pytest.mark.fms_list_of_firmwares
    @allure.title("Get list of firmwares")
    @allure.testcase(name="WIFI-12559",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12559")
    def test_fms_list_of_firmwares(self, get_target_object):
        """
                    Get list of firmwares
                    Unique marker: pytest -m "fms_list_of_firmwares"
        """
        system_info = get_target_object.controller_library_object.get_list_of_firmwares()
        assert system_info.status_code == 200






