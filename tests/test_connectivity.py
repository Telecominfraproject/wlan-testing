"""
    Test Case Module:  Testing Basic Connectivity with Resources
    Mode:       BRIDGE

"""
import pytest
import sys

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
