import pytest
from configuration import CLOUDSDK_VERSION


@pytest.mark.sdk_version_check
def test_cloud_sdk_version(instantiate_cloudsdk):
    try:
        response = instantiate_cloudsdk.portal_ping()
        if CLOUDSDK_VERSION['project_version'] == response._project_version and \
                CLOUDSDK_VERSION['commit_id'] == response._commit_id:
            PASS = True
        else:
            PASS = False
    except Exception as e:
        print(e)
        PASS = False
    assert PASS


