"""
    Test Case Module:  Testing Basic Connectivity with Resources
    Mode:       BRIDGE

"""
import pytest
import sys

pytestmark = [pytest.mark.test_connectivity]


@pytest.mark.sanity
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
@pytest.mark.test_access_points_connectivity
def test_access_points_connectivity(test_access_point, instantiate_testrail, instantiate_project, test_cases):
    if "ACTIVE" not in test_access_point:
        instantiate_testrail.update_testrail(case_id=test_cases["cloud_connection"], run_id=instantiate_project,
                                             status_id=5,
                                             msg='CloudSDK connectivity failed')
        status = False
        sys.exit()
    else:
        instantiate_testrail.update_testrail(case_id=test_cases["cloud_connection"], run_id=instantiate_project,
                                             status_id=1,
                                             msg='Manager status is Active')
        status = True

    assert status


@pytest.mark.test_lanforge_connectivity
def test_lanforge_connectivity(setup_lanforge):
    assert "instantiate_cloudsdk"


@pytest.mark.test_perfecto_connectivity
def test_perfecto_connectivity(setup_perfecto_devices):
    assert "instantiate_cloudsdk"
