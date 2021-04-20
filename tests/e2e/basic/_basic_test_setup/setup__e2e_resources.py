"""
    Test Case Module:  setup test cases for basic test cases
    Details:    Firmware Upgrade

"""
import pytest


@pytest.mark.sanity
@pytest.mark.bridge
@pytest.mark.nat
@pytest.mark.vlan
@pytest.mark.firmware
class TestFirmware(object):

    @pytest.mark.firmware_create
    def test_firmware_create(self, upload_firmware, instantiate_testrail, instantiate_project, test_cases):
        if upload_firmware != 0:
            instantiate_testrail.update_testrail(case_id=test_cases["create_fw"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='Create new FW version by API successful')
            PASS = True
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["create_fw"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='Error creating new FW version by API')
            PASS = False
        assert PASS

    @pytest.mark.firmware_upgrade
    def test_firmware_upgrade_request(self, upgrade_firmware, instantiate_testrail, instantiate_project, test_cases):
        print()
        if not upgrade_firmware:
            instantiate_testrail.update_testrail(case_id=test_cases["upgrade_api"], run_id=instantiate_project,
                                                 status_id=0,
                                                 msg='Error requesting upgrade via API')
            PASS = False
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["upgrade_api"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='Upgrade request using API successful')
            PASS = True
        assert PASS

    @pytest.mark.check_active_firmware_cloud
    def test_active_version_cloud(self, get_latest_firmware, check_ap_firmware_cloud, instantiate_testrail,
                                  instantiate_project, test_cases):
        if get_latest_firmware != check_ap_firmware_cloud:
            instantiate_testrail.update_testrail(case_id=test_cases["cloud_fw"], run_id=instantiate_project,
                                                 status_id=5,
                                                 msg='CLOUDSDK reporting incorrect firmware version.')
        else:
            instantiate_testrail.update_testrail(case_id=test_cases["cloud_fw"], run_id=instantiate_project,
                                                 status_id=1,
                                                 msg='CLOUDSDK reporting correct firmware version.')

        assert get_latest_firmware == check_ap_firmware_cloud


@pytest.mark.sanity
@pytest.mark.bridge
@pytest.mark.nat
@pytest.mark.vlan
@pytest.mark.check_active_firmware_ap
def test_ap_firmware(check_ap_firmware_ssh, get_latest_firmware, instantiate_testrail, instantiate_project,
                     test_cases):
    if check_ap_firmware_ssh == get_latest_firmware:
        instantiate_testrail.update_testrail(case_id=test_cases["ap_upgrade"], run_id=instantiate_project,
                                             status_id=1,
                                             msg='Upgrade to ' + get_latest_firmware + ' successful')
    else:
        instantiate_testrail.update_testrail(case_id=test_cases["ap_upgrade"], run_id=instantiate_project,
                                             status_id=4,
                                             msg='Cannot reach AP after upgrade to check CLI - re-test required')

    assert check_ap_firmware_ssh == get_latest_firmware
