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
            update_report.update_testrail(case_id=test_cases["cloud_ver"],
                                                 status_id=1, msg='Read CloudSDK version from API successfully')
            PASS = True
        else:
            update_report.update_testrail(case_id=test_cases["cloud_ver"],
                                                 status_id=0, msg='Could not read CloudSDK version from API -  '
                                                                  'version missmatch')
            PASS = False
    except Exception as e:
        print(e)
        update_report.update_testrail(case_id=test_cases["cloud_ver"],
                                             status_id=0, msg='Could not read CloudSDK version from API - Exception '
                                                              'occured')
        PASS = False
    assert PASS
