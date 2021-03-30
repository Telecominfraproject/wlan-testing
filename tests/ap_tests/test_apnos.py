import pytest

from configuration_data import TEST_CASES


@pytest.mark.shivamy(after='test_something_1')
def test_something_2():
    assert True


@pytest.mark.sanity(depends=['TestFirmware'])
@pytest.mark.bridge(order=3)
@pytest.mark.nat(order=3)
@pytest.mark.vlan(order=3)
@pytest.mark.ap_firmware
class TestFirmwareAPNOS(object):

    @pytest.mark.check_active_firmware_ap
    def test_ap_firmware(self, check_ap_firmware_ssh, get_latest_firmware):
        print("5")
        if check_ap_firmware_ssh == get_latest_firmware:
            status = True
            # instantiate_testrail.update_testrail(case_id=TEST_CASES["ap_upgrade"], run_id=instantiate_project,
            #                                      status_id=1,
            #                                      msg='Upgrade to ' + get_latest_firmware + ' successful')
        else:
            status = False
            # instantiate_testrail.update_testrail(case_id=TEST_CASES["ap_upgrade"], run_id=instantiate_project,
            #                                      status_id=4,
            #                                      msg='Cannot reach AP after upgrade to check CLI - re-test required')

        assert status


@pytest.mark.basic
@pytest.mark.bridge(order=4)
@pytest.mark.nat(order=4)
@pytest.mark.vlan(order=4)
@pytest.mark.ap_connection
class TestConnection(object):

    @pytest.mark.ap_manager_state
    @pytest.mark.sanity(depends=['TestFirmwareAPNOS'])
    def test_ap_manager_state(self, get_ap_manager_status):
        print("4")
        if "ACTIVE" not in get_ap_manager_status:
            # instantiate_testrail.update_testrail(case_id=TEST_CASES["cloud_connection"], run_id=instantiate_project,
            #                                      status_id=5,
            #                                      msg='CloudSDK connectivity failed')
            status = False
        else:
            # instantiate_testrail.update_testrail(case_id=TEST_CASES["cloud_connection"], run_id=instantiate_project,
            #                                      status_id=1,
            #                                      msg='Manager status is Active')
            status = True
        assert status
        # break test session if test case is false


@pytest.mark.shivamy(after='test_something_2')
def test_something_3():
    assert True
