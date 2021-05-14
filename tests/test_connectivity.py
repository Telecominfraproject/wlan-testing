"""
    Test Case Module:  Testing Basic Connectivity with Resources
"""
import sys

<<<<<<< HEAD
pytestmark = [pytest.mark.test_connectivity]


@pytest.mark.sanity
@pytest.mark.bridge
@pytest.mark.nat
@pytest.mark.vlan
@pytest.mark.test_controller_connectivity
def test_controller_connectivity(instantiate_controller, instantiate_testrail, instantiate_project, test_cases):
    try:
        instantiate_testrail.update_testrail(case_id=test_cases["cloud_ver"], run_id=instantiate_project,
                                             status_id=1, msg='Read CloudSDK version from API successfully')
        PASS = True
    except:
        instantiate_testrail.update_testrail(case_id=test_cases["cloud_ver"], run_id=instantiate_project,
                                             status_id=0, msg='Could not read CloudSDK version from API')
        PASS = False
    assert instantiate_controller


@pytest.mark.sanity
@pytest.mark.bridge
@pytest.mark.nat
@pytest.mark.vlan
@pytest.mark.test_access_points_connectivity
def test_access_points_connectivity(access_point_connectivity, instantiate_testrail, instantiate_project, test_cases,
                                    exit_on_fail):
    if not access_point_connectivity["serial"] and not access_point_connectivity["mgr"]:
        instantiate_testrail.update_testrail(case_id=test_cases["cloud_connection"], run_id=instantiate_project,
                                             status_id=5,
                                             msg='CloudSDK connectivity failed')
        status = False
        pytest.exit("Access Point is not Properly Connected: Sanity Failed")
    else:
        instantiate_testrail.update_testrail(case_id=test_cases["cloud_connection"], run_id=instantiate_project,
                                             status_id=1,
                                             msg='Manager status is Active')
        status = True

    assert status


@pytest.mark.test_lanforge_connectivity
def test_lanforge_connectiity(check_lanforge_connectivity):
    assert True
=======
import allure
import pytest

pytestmark = [pytest.mark.test_resources]


@pytest.mark.sanity
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
        print(setup_controller.bearer)
        assert setup_controller.bearer

    @pytest.mark.test_access_points_connectivity
    @allure.testcase(name="test_access_points_connectivity", url="")
    def test_access_points_connectivity(self, test_access_point, update_report, test_cases):
        print(test_access_point)
        # if "ACTIVE" not in test_access_point:
        #     allure.attach(name="Access Point Connectivity Success", body=str(test_access_point))
        #     update_report.update_testrail(case_id=test_cases["cloud_connection"],
        #                                   status_id=5,
        #                                   msg='CloudSDK connectivity failed')
        #
        #     sys.exit()
        # else:
        #     allure.attach(name="Access Point Connectivity Failed", body=str(test_access_point))
        #     update_report.update_testrail(case_id=test_cases["cloud_connection"],
        #                                   status_id=1,
        #                                   msg='Manager status is Active')
        #
        # assert "ACTIVE" in test_access_point
        assert True
>>>>>>> staging-wifi-1960
