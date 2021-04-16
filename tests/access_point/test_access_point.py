import pytest


@pytest.mark.sanity
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
