"""
    Test Case Module:  Testing Basic Cloud

"""
import pytest
from configuration import CONFIGURATION


@pytest.mark.sanity
@pytest.mark.sanity_55
@pytest.mark.sdk_version_check
def test_cloud_sdk_version(setup_controller, testbed, test_cases, update_report):
    try:
        response = setup_controller.portal_ping()
        if CONFIGURATION[testbed]['controller']['version'] == response._project_version:
            PASS = True
        else:
            PASS = False
    except Exception as e:
        print(e)
        PASS = False
    assert PASS
