"""
    Test Case Module:  Testing Basic Connectivity with Resources
"""
import sys

import allure
import pytest

pytestmark = [pytest.mark.usefixtures("setup_test_run"), pytest.mark.test_resources, pytest.mark.sanity]


@allure.testcase(name="Test Resources", url="")
class TestResources(object):

    @pytest.mark.test_cloud_controller
    @allure.testcase(name="test_controller_connectivity", url="")
    def test_controller_connectivity(self, setup_controller, update_report, test_cases):
        if setup_controller.bearer:
            allure.attach(name="Controller Connectivity Success", body="")
            update_report.update_testrail(case_id=test_cases["cloud_ver"],
                                          status_id=1, msg='Read CloudSDK version from API successfully')
        else:
            allure.attach(name="Controller Connectivity Failed", body="")
            update_report.update_testrail(case_id=test_cases["cloud_ver"],
                                          status_id=0, msg='Could not read CloudSDK version from API')
            pytest.exit("Resource Not Available")
        # print(setup_controller.bearer)
        assert setup_controller.bearer

    @pytest.mark.test_access_points_connectivity
    @allure.testcase(name="test_access_points_connectivity", url="")
    def test_access_points_connectivity(self, test_access_point, update_report, test_cases):
        flag = True
        print(test_access_point)
        for i in test_access_point:
            if "ACTIVE" not in i:
                flag = False

        if flag is False:
            allure.attach(name="Access Point Connectivity Success", body=str(test_access_point))
            update_report.update_testrail(case_id=test_cases["cloud_connection"],
                                          status_id=5,
                                          msg='CloudSDK connectivity failed')

            pytest.exit("Access Point Manafer state is not ACtive")
        else:
            allure.attach(name="Access Point Connectivity Failed", body=str(test_access_point))
            update_report.update_testrail(case_id=test_cases["cloud_connection"],
                                          status_id=1,
                                          msg='Manager status is Active')

        assert flag
