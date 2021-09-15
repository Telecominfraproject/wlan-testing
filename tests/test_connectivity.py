"""
    Test Case Module:  Testing Basic Connectivity with Resources
"""

import allure
import pytest
import requests

pytestmark = [pytest.mark.test_resources, pytest.mark.sanity,
              pytest.mark.sanity_55]


@pytest.mark.fw
def test_firmware(firmware_upgrade):

    assert True


@allure.testcase(name="Test Resources", url="")
class TestResources(object):
    """Test Case Class: Test cases to cover resource Connectivity"""

    @pytest.mark.test_cloud_controller
    @pytest.mark.uc_sanity
    @allure.testcase(name="test_controller_connectivity", url="")
    def test_controller_connectivity(self, setup_controller):
        """Test case to verify cloud Controller Connectivity"""
        login_response_json = setup_controller.login_resp.json()
        response_code = setup_controller.login_resp.status_code
        allure.attach(name="Login Response Code", body=str(response_code))
        allure.attach(name="Login Response JSON", body=str(login_response_json))
        # if setup_controller.bearer:
        #     allure.attach(name="Controller Connectivity Success", body="")
        # else:
        #     allure.attach(name="Controller Connectivity Failed", body="")
        #     pytest.exit("Controller Not Available")
        # assert setup_controller.bearer
        assert response_code == 200

    @pytest.mark.test_access_points_connectivity
    @allure.testcase(name="test_access_points_connectivity", url="")
    def test_access_points_connectivity(self, test_access_point):
        """Test case to verify Access Points Connectivity"""
        flag = True
        for i in test_access_point:
            if "ACTIVE" not in i:
                flag = False
        if flag is False:
            allure.attach(name="Access Point Connectivity Success", body=str(test_access_point))
            pytest.exit("Access Point Manager state is not Active")
        else:
            allure.attach(name="Access Point Connectivity Failed", body=str(test_access_point))

        assert flag

    @pytest.mark.traffic_generator_connectivity
    @allure.testcase(name="test_traffic_generator_connectivity", url="")
    def test_traffic_generator_connectivity(self, traffic_generator_connectivity, update_report, test_cases):
        """Test case to verify Traffic Generator Connectivity"""
        if traffic_generator_connectivity == "5.4.4":
            allure.attach(name="LANforge-", body=str(traffic_generator_connectivity))

        else:
            pytest.exit("LANforgeGUI-5.4.3 is not available")

        assert traffic_generator_connectivity
