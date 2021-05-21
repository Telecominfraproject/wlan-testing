
"""
    Test Case Module:  setup test cases for basic test cases
    Details:    Firmware Upgrade

"""
import pytest
import time

@pytest.mark.configure_lanforge
def test_configure_lanforge(configure_lanforge):

    assert True


@pytest.mark.lanforge_scenario_setup_dut
def test_lanforge_scenario_setup_dut(create_lanforge_chamberview_dut):
    print(create_lanforge_chamberview_dut)
    ssid = [
        ['ssid_idx=0 ssid=Default-SSID-2g password=12345678 bssid=90:3c:b3:94:48:58'],
        ['ssid_idx=1 ssid=Default-SSID-5gl password=12345678 bssid=90:3c:b3:94:48:59']
            ]

    create_lanforge_chamberview_dut.ssid = ssid
    create_lanforge_chamberview_dut.setup()
    create_lanforge_chamberview_dut.add_ssids()
    create_lanforge_chamberview_dut.cv_test.show_text_blob(None, None, True)  # Show changes on GUI
    create_lanforge_chamberview_dut.cv_test.sync_cv()
    time.sleep(2)
    create_lanforge_chamberview_dut.cv_test.show_text_blob(None, None, True)  # Show changes on GUI
    create_lanforge_chamberview_dut.cv_test.sync_cv()

    assert True

@pytest.mark.lanforge_scenario_setup
def test_lanforge_scenario_setup(create_lanforge_chamberview):
    # raw_line = [
    #     ["profile_link 1.1 vlan-100 1 NA NA eth2,AUTO -1 100"]
    # ]
    # print(create_lanforge_chamberview.setup_scenario(create_scenario="TIP-test",raw_line=raw_line))
    # create_lanforge_chamberview.build_scenario("TIP-test")
    assert True

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


# """
#     Test Case Module:  setup test cases for basic test cases
#     Details:    Firmware Upgrade
#
# """
# import pytest
#
# @pytest.mark.configure_lanforge
# def test_configure_lanforge(configure_lanforge):
#
#     assert True
#
#
# @pytest.mark.sanity
# @pytest.mark.bridge
# @pytest.mark.nat
# @pytest.mark.vlan
# @pytest.mark.firmware
# class TestFirmware(object):
#
#     @pytest.mark.firmware_create
#     def test_firmware_create(self, upload_firmware, instantiate_testrail, instantiate_project, test_cases):
#         if upload_firmware != 0:
#             instantiate_testrail.update_testrail(case_id=test_cases["create_fw"], run_id=instantiate_project,
#                                                  status_id=1,
#                                                  msg='Create new FW version by API successful')
#             PASS = True
#         else:
#             instantiate_testrail.update_testrail(case_id=test_cases["create_fw"], run_id=instantiate_project,
#                                                  status_id=5,
#                                                  msg='Error creating new FW version by API')
#             PASS = False
#         assert PASS
#
#     @pytest.mark.firmware_upgrade
#     def test_firmware_upgrade_request(self, upgrade_firmware, instantiate_testrail, instantiate_project, test_cases):
#         print()
#         if not upgrade_firmware:
#             instantiate_testrail.update_testrail(case_id=test_cases["upgrade_api"], run_id=instantiate_project,
#                                                  status_id=0,
#                                                  msg='Error requesting upgrade via API')
#             PASS = False
#         else:
#             instantiate_testrail.update_testrail(case_id=test_cases["upgrade_api"], run_id=instantiate_project,
#                                                  status_id=1,
#                                                  msg='Upgrade request using API successful')
#             PASS = True
#         assert PASS
#
#     @pytest.mark.check_active_firmware_cloud
#     def test_active_version_cloud(self, get_latest_firmware, check_ap_firmware_cloud, instantiate_testrail,
#                                   instantiate_project, test_cases):
#         if get_latest_firmware != check_ap_firmware_cloud:
#             instantiate_testrail.update_testrail(case_id=test_cases["cloud_fw"], run_id=instantiate_project,
#                                                  status_id=5,
#                                                  msg='CLOUDSDK reporting incorrect firmware version.')
#         else:
#             instantiate_testrail.update_testrail(case_id=test_cases["cloud_fw"], run_id=instantiate_project,
#                                                  status_id=1,
#                                                  msg='CLOUDSDK reporting correct firmware version.')
#
#         assert get_latest_firmware == check_ap_firmware_cloud
#
#
# @pytest.mark.sanity
# @pytest.mark.bridge
# @pytest.mark.nat
# @pytest.mark.vlan
# @pytest.mark.check_active_firmware_ap
# def test_ap_firmware(check_ap_firmware_ssh, get_latest_firmware, instantiate_testrail, instantiate_project,
#                      test_cases):
#     if check_ap_firmware_ssh == get_latest_firmware:
#         instantiate_testrail.update_testrail(case_id=test_cases["ap_upgrade"], run_id=instantiate_project,
#                                              status_id=1,
#                                              msg='Upgrade to ' + get_latest_firmware + ' successful')
#     else:
#         instantiate_testrail.update_testrail(case_id=test_cases["ap_upgrade"], run_id=instantiate_project,
#                                              status_id=4,
#                                              msg='Cannot reach AP after upgrade to check CLI - re-test required')
#
#     assert check_ap_firmware_ssh == get_latest_firmware

