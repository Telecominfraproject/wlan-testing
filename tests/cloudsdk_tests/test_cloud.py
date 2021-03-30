"""
About: It contains some Functional Unit Tests for CloudSDK and to run and test them on per unit level
"""

import pytest
import sys

if 'cloudsdk_tests' not in sys.path:
    sys.path.append(f'../../libs/cloudsdk')
from cloudsdk import CloudSDK
from configuration_data import TEST_CASES


@pytest.mark.sanity
@pytest.mark.bridge
@pytest.mark.nat
@pytest.mark.vlan
@pytest.mark.cloud_connect
class TestCloudSDK(object):

    @pytest.mark.sdk_version_check
    def test_cloud_sdk_version(self, instantiate_cloudsdk):
        print("1")
        cloudsdk_cluster_info = {}  # Needed in Test Result
        try:
            response = instantiate_cloudsdk.portal_ping()

            cloudsdk_cluster_info['date'] = response._commit_date
            cloudsdk_cluster_info['commitId'] = response._commit_id
            cloudsdk_cluster_info['projectVersion'] = response._project_version
            # instantiate_testrail.update_testrail(case_id=TEST_CASES["cloud_ver"], run_id=instantiate_project,
            #                                      status_id=1, msg='Read CloudSDK version from API successfully')
            PASS = True
        except:
            cloudsdk_cluster_info = {'date': "unknown", 'commitId': "unknown", 'projectVersion': "unknown"}
            # instantiate_testrail.update_testrail(case_id=TEST_CASES["cloud_ver"], run_id=instantiate_project,
            #                                      status_id=0, msg='Could not read CloudSDK version from API')
            PASS = False

        assert PASS, cloudsdk_cluster_info


@pytest.mark.sanity(depends=['TestCloudSDK'])
@pytest.mark.bridge
@pytest.mark.nat
@pytest.mark.vlan
@pytest.mark.firmware
class TestFirmware(object):

    @pytest.mark.firmware_create
    def test_firmware_create(self, upload_firmware):
        print("2")
        if upload_firmware != 0:
            # instantiate_testrail.update_testrail(case_id=TEST_CASES["create_fw"], run_id=instantiate_project,
            #                                      status_id=1,
            #                                      msg='Create new FW version by API successful')
            PASS = True
        else:
            # instantiate_testrail.update_testrail(case_id=TEST_CASES["create_fw"], run_id=instantiate_project,
            #                                      status_id=5,
            #                                      msg='Error creating new FW version by API')
            PASS = False
        assert PASS

    @pytest.mark.firmware_upgrade
    def test_firmware_upgrade_request(self, upgrade_firmware):
        print("2")
        if not upgrade_firmware:
            # instantiate_testrail.update_testrail(case_id=TEST_CASES["upgrade_api"], run_id=instantiate_project,
            #                                      status_id=0,
            #                                      msg='Error requesting upgrade via API')
            PASS = False
        else:
            # instantiate_testrail.update_testrail(case_id=TEST_CASES["upgrade_api"], run_id=instantiate_project,
            #                                      status_id=1,
            #                                      msg='Upgrade request using API successful')
            PASS = True
        assert PASS

    @pytest.mark.check_active_firmware_cloud
    def test_active_version_cloud(self, check_ap_firmware_cloud):
        print("3")
        if not check_ap_firmware_cloud:
            # instantiate_testrail.update_testrail(case_id=TEST_CASES["cloud_fw"], run_id=instantiate_project,
            #                                      status_id=5,
            #                                      msg='CLOUDSDK reporting incorrect firmware version.')
            PASS = False
        else:
            PASS = True
            # instantiate_testrail.update_testrail(case_id=TEST_CASES["cloud_fw"], run_id=instantiate_project,
            #                                      status_id=1,
            #                                      msg='CLOUDSDK reporting correct firmware version.')

        assert PASS


@pytest.mark.shivamy(before='test_something_2')
def test_something_1():
    assert True
