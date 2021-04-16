import pytest
from configuration import CONFIGURATION


@pytest.mark.sanity
@pytest.mark.sdk_version_check
def test_cloud_sdk_version(instantiate_cloudsdk, testbed, test_cases, instantiate_testrail, instantiate_project):
    try:
        response = instantiate_cloudsdk.portal_ping()
        if CONFIGURATION[testbed]['controller']['version'] == response._project_version:
            PASS = True
            instantiate_testrail.update_testrail(case_id=test_cases["cloud_ver"], run_id=instantiate_project,
                                                 status_id=1, msg='Read CloudSDK version from API successfully')
            PASS = True
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["cloud_ver"], run_id=instantiate_project,
                                                 status_id=0, msg='Could not read CloudSDK version from API -  version missmatch')
            PASS = False
    except Exception as e:
        print(e)
        instantiate_testrail.update_testrail(case_id=test_cases["cloud_ver"], run_id=instantiate_project,
                                             status_id=0, msg='Could not read CloudSDK version from API - Exception occured')
        PASS = False
    assert PASS
