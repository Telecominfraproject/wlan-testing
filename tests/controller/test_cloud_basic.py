import pytest
from configuration import CONFIGURATION


@pytest.mark.sdk_version_check
def test_cloud_sdk_version(instantiate_cloudsdk, testbed):
    try:
        response = instantiate_cloudsdk.portal_ping()
        if CONFIGURATION[testbed]['controller']['version'] == response._project_version:
            PASS = True
        else:
            PASS = False
    except Exception as e:
        print(e)
        PASS = False
    assert PASS


