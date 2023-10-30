"""

    UCentral FMS Services Rest API Tests

"""

import allure
import pytest
import importlib
import time
logging = importlib.import_module("logging")


@pytest.mark.uc_sanity
@pytest.mark.ow_sdk_load_tests
@pytest.mark.owfms_api_tests
@allure.parent_suite("SDK Tests")
@allure.suite("FMS Service Tests")
class TestUcentralFMSService(object):

    @pytest.mark.fms_list_of_firmwares
    @allure.title("Get list of firmwares")
    @allure.testcase(name="WIFI-12559",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12559")
    def test_fms_list_of_firmwares(self, get_target_object):
        """
                    Get list of firmwares
                    Unique marker: pytest -m "fms_list_of_firmwares"
        """
        system_info = get_target_object.controller_library_object.get_list_of_firmwares()
        assert system_info.status_code == 200

    @pytest.mark.fms_different_values_from_the_running_service
    @allure.title("Get different values from the running service")
    @allure.testcase(name="WIFI-12560",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12560")
    def test_fms_different_values_from_the_running_service(self, get_target_object):
        """
                    Get different values from the running service
                    Unique marker: pytest -m "fms_different_values_from_the_running_service"
        """
        system_info = get_target_object.controller_library_object.get_different_values_from_the_running_service()
        assert system_info.status_code == 200

    @pytest.mark.fms_system_wide_commands
    @allure.title("Perform some system wide commands")
    @allure.testcase(name="WIFI-12647",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12647")
    def test_fms_system_wide_commands(self, get_target_object):
        """
                    Perform some system wide commands
                    Unique marker: pytest -m "fms_system_wide_commands"
        """
        payload = {
            "command": "setloglevel",
            "subsystems": [
                {
                    "tag": "",
                    "value": ""
                }
            ]
        }
        system_info = get_target_object.controller_library_object.perform_system_wide_commands(payload)
        assert system_info.status_code == 200

    @pytest.mark.fms_list_all_the_defined_device_revision_history
    @allure.title("Get list all the defined device revision history")
    @allure.testcase(name="WIFI-12561",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12561")
    def test_fms_list_all_the_defined_device_revision_history(self, get_target_object, get_testbed_details):
        """
                    Get list all the defined device revision history
                    Unique marker: pytest -m "fms_list_all_the_defined_device_revision_history"
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        system_info = get_target_object.controller_library_object.get_list_all_the_defined_device_revision_history(
            device_name)
        assert system_info.status_code == 200

    @pytest.mark.fms_list_of_connected_devices_and_some_values
    @allure.title("Get list of connected devices and some values")
    @allure.testcase(name="WIFI-12562",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12562")
    def test_fms_list_of_connected_devices_and_some_values(self, get_target_object, get_testbed_details):
        """
                    Get list of connected devices and some values
                    Unique marker: pytest -m "fms_list_of_connected_devices_and_some_values"
        """
        system_info = get_target_object.controller_library_object.get_list_of_connected_devices_and_some_values()
        assert system_info.status_code == 200

    @pytest.mark.fms_status_of_connected_device
    @allure.title("Get status of a connected device")
    @allure.testcase(name="WIFI-12563",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12563")
    def test_fms_status_of_connected_device(self, get_target_object, get_testbed_details):
        """
                    Get status of a connected device
                    Unique marker: pytest -m "fms_status_of_connected_device"
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        system_info = get_target_object.controller_library_object.get_status_of_connected_device(
            device_name)
        assert system_info.status_code == 200

    @pytest.mark.fms_analysis_of_the_existing_devices_we_know_about
    @allure.title("Get an analysis of the existing devices we know about")
    @allure.testcase(name="WIFI-12564",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12564")
    def test_fms_analysis_of_the_existing_devices_we_know_about(self, get_target_object, get_testbed_details):
        """
                    Get an analysis of the existing devices we know about
                    Unique marker: pytest -m "fms_analysis_of_the_existing_devices_we_know_about"
        """
        system_info = get_target_object.controller_library_object.get_analysis_of_the_existing_devices_we_know_about()
        assert system_info.status_code == 200

    @pytest.mark.fms_receive_a_report_on_single_decide
    @allure.title("Get a report on a single decide")
    @allure.testcase(name="WIFI-12565",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12565")
    def test_fms_receive_a_report_on_single_decide(self, get_target_object, get_testbed_details):
        """
                    Get a report on a single decide
                    Unique marker: pytest -m "fms_receive_a_report_on_single_decide"
        """
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        system_info = get_target_object.controller_library_object.get_receive_a_report_on_single_decide(
            device_name)
        assert system_info.status_code == 200

    @pytest.mark.fms_system_configuration_items
    @allure.title("Get system configuration items")
    @allure.testcase(name="WIFI-12566",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-12566")
    def test_fms_system_configuration_items(self, get_target_object, get_testbed_details):
        """
                    Get system configuration items
                    Unique marker: pytest -m "fms_system_configuration_items"
        """
        entries = "info"
        system_info = get_target_object.controller_library_object.get_system_configuration_items(entries)
        assert system_info.status_code == 200


"""Test cases for Firmware Upgrade/Downgrade"""


@pytest.mark.firmware_upgrade_downgrade
@allure.parent_suite("Firmware Tests")
@allure.suite("Firmware Upgrade/Downgrade Tests")
class TestFirmwareUpgradeDowngrade(object):

    @pytest.mark.downgrade_f1_to_f2
    @allure.title("Downgrade Firmware to one lower release image from (F1) to firmware (F2)")
    @allure.testcase(name="WIFI-13007",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-13007")
    def test_downgrade_f1_to_f2(self, get_target_object, get_testbed_details):
        """
                    Downgrade Firmware to one lower release image from (F1) to firmware (F2)
                    Unique marker: pytest -m "downgrade_f1_to_f2"
                    F1 - Latest release image
                    F2 - One lower release image
        """
        for ap in range(len(get_target_object.device_under_tests_info)):
            firmware_list = get_target_object.firmware_library_object.get_firmwares(
                model=get_target_object.device_under_tests_info[ap]['model'],
                branch="",
                commit_id='',
                limit='',
                offset='3000')
            latest_4_release_images = get_target_object.firmware_library_object.get_latest_four_release_images(
                firmware_list=firmware_list)
            if len(latest_4_release_images) < 4:
                pytest.fail("Latest 4 release images are not available on GW")
            # check the current AP Revision before upgrade

            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

            # print and report the firmware versions before upgrade
            allure.attach(name="Current Firmware Image: ",
                          body=str(current_version))
            logging.info("Current Firmware Image: " + str(current_version))
            allure.attach(name="F1 Firmware Image: ",
                          body=str(latest_4_release_images[0]))
            logging.info("F1 Firmware Image: " + str(latest_4_release_images[0]))
            allure.attach(name="F2 Firmware Image: ",
                          body=str(latest_4_release_images[1]))
            logging.info("F2 Firmware Image: " + str(latest_4_release_images[1]))
            # Check the current AP’s firmware, it should be on latest release image (F1)
            f1_version = latest_4_release_images[0]['revision'].split("/")[1].replace(" ", "")
            logging.info("f1_version: " + str(f1_version))
            logging.info("current_version: " + str(current_version))
            # If current version and F1 version are same then skip upgrade to F1
            if current_version == f1_version:
                logging.info("Skipping Upgrade! AP is already in F1 version")
                allure.attach(name="AP is already in the F1 Version",
                              body="")
            else:
                get_target_object.firmware_library_object.upgrade_firmware(
                    serial=get_target_object.device_under_tests_info[ap]['identifier'],
                    url=str(latest_4_release_images[0]['uri']))
                # wait for 300 seconds after firmware upgrade
                logging.info("Waiting for 300 Sec for Firmware Upgrade")
                time.sleep(300)

                # check the current AP Revision again
                ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
                current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                # print and report the Firmware versions after upgrade
                allure.attach(name="After Firmware Upgrade Request to F1: ",
                              body="Current revision: " + current_version + "\nF1 revision: " + f1_version)
                logging.info("current revision: " + str(current_version) +
                             "\nF1 revision: " + str(f1_version))

                if current_version == f1_version:
                    logging.info("firmware upgrade successfully to F1: " + f1_version)
                else:
                    logging.info("firmware upgrade failed to F1: " + f1_version)
                    pytest.fail("firmware upgrade failed to F1: " + f1_version)

            # Downgrade to one lower Release image (F2)
            f2_version = latest_4_release_images[1]['revision'].split("/")[1].replace(" ", "")
            logging.info("f2_version: " + str(f2_version))
            get_target_object.firmware_library_object.upgrade_firmware(
                serial=get_target_object.device_under_tests_info[ap]['identifier'],
                url=str(latest_4_release_images[1]['uri']))
            # wait for 300 seconds after firmware upgrade
            logging.info("waiting for 300 Sec for Firmware Downgrade")
            time.sleep(300)
            # check the current AP Revision again
            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
            # print and report the Firmware versions after upgrade
            allure.attach(name="After Firmware downgrade Request to F2: ",
                          body="Current revision: " + current_version + "\nF2 revision: " + f2_version)
            logging.info("current revision: " + str(current_version) +
                         "\nF2 revision: " + str(f2_version))

            if current_version == f2_version:
                logging.info("firmware downgraded successfully to F2: " + f2_version)
            else:
                logging.info("firmware downgrade failed to F2: " + f2_version)
                pytest.fail("firmware downgrade failed to F2: " + f2_version)

    @pytest.mark.upgrade_f2_to_f1
    @allure.title("Upgrade Firmware to one upper release image from (F2) to firmware image (F1)")
    @allure.testcase(name="WIFI-13008",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-13008")
    def test_upgrade_f2_to_f1(self, get_target_object, get_testbed_details):
        """
                    Upgrade Firmware to one upper release image from (F2) to firmware image (F1)
                    Unique marker: pytest -m "upgrade_f2_to_f1"
                    F1 - Latest release image
                    F2 - One lower release image
        """
        for ap in range(len(get_target_object.device_under_tests_info)):
            firmware_list = get_target_object.firmware_library_object.get_firmwares(
                model=get_target_object.device_under_tests_info[ap]['model'],
                branch="",
                commit_id='',
                limit='',
                offset='3000')
            latest_4_release_images = get_target_object.firmware_library_object.get_latest_four_release_images(
                firmware_list=firmware_list)
            if len(latest_4_release_images) < 4:
                pytest.fail("Latest 4 release images are not available on GW")
            # check the current AP Revision before upgrade

            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

            # print and report the firmware versions before upgrade
            allure.attach(name="Current Firmware Image: ",
                          body=str(current_version))
            logging.info("Current Firmware Image: " + str(current_version))
            allure.attach(name="F1 Firmware Image: ",
                          body=str(latest_4_release_images[0]))
            logging.info("F1 Firmware Image: " + str(latest_4_release_images[0]))
            allure.attach(name="F2 Firmware Image: ",
                          body=str(latest_4_release_images[1]))
            logging.info("F2 Firmware Image: " + str(latest_4_release_images[1]))
            # Check the current AP’s firmware, it should be on One lower release image (F2)
            f2_version = latest_4_release_images[1]['revision'].split("/")[1].replace(" ", "")
            logging.info("f2_version: " + str(f2_version))
            logging.info("current_version: " + str(current_version))
            # If current version and F2 version are same then skip upgrade to F2
            if current_version == f2_version:
                logging.info("Skipping Upgrade! AP is already in F2 version")
                allure.attach(name="AP is already in the F2 Version",
                              body="")
            else:
                get_target_object.firmware_library_object.upgrade_firmware(
                    serial=get_target_object.device_under_tests_info[ap]['identifier'],
                    url=str(latest_4_release_images[1]['uri']))
                # wait for 300 seconds after firmware upgrade
                logging.info("Waiting for 300 Sec for Firmware Upgrade")
                time.sleep(300)

                # check the current AP Revision again
                ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
                current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                # print and report the Firmware versions after upgrade
                allure.attach(name="After Firmware Upgrade Request to F2: ",
                              body="Current revision: " + current_version + "\nF2 revision: " + f2_version)
                logging.info("current revision: " + str(current_version) +
                             "\nF2 revision: " + str(f2_version))

                if current_version == f2_version:
                    logging.info("firmware upgrade successfully to F2: " + f2_version)
                else:
                    logging.info("firmware upgrade failed to F2: " + f2_version)
                    pytest.fail("firmware upgrade failed to F2: " + f2_version)

            # Upgrade to one upper Release image (F1)
            f1_version = latest_4_release_images[0]['revision'].split("/")[1].replace(" ", "")
            logging.info("f1_version: " + str(f1_version))
            get_target_object.firmware_library_object.upgrade_firmware(
                serial=get_target_object.device_under_tests_info[ap]['identifier'],
                url=str(latest_4_release_images[0]['uri']))
            # wait for 300 seconds after firmware upgrade
            logging.info("waiting for 300 Sec for Firmware Upgrade")
            time.sleep(300)
            # check the current AP Revision again
            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
            # print and report the Firmware versions after upgrade
            allure.attach(name="After Firmware upgrade Request to F1: ",
                          body="Current revision: " + current_version + "\nF1 revision: " + f1_version)
            logging.info("current revision: " + str(current_version) +
                         "\nF1 revision: " + str(f1_version))

            if current_version == f1_version:
                logging.info("firmware upgrade successfully to F1: " + f1_version)
            else:
                logging.info("firmware upgrade failed to F1: " + f1_version)
                pytest.fail("firmware upgrade failed to F1: " + f1_version)

    @pytest.mark.downgrade_f1_to_f3
    @allure.title("Downgrade Firmware to two lower release image from (F1) to firmware (F3)")
    @allure.testcase(name="WIFI-13009",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-13009")
    def test_downgrade_f1_to_f3(self, get_target_object, get_testbed_details):
        """
                    Downgrade Firmware to two lower release image from (F1) to firmware (F3)
                    Unique marker: pytest -m "downgrade_f1_to_f3"
                    F1 - Latest release image
                    F3 - Two lower release image
        """
        for ap in range(len(get_target_object.device_under_tests_info)):
            firmware_list = get_target_object.firmware_library_object.get_firmwares(
                model=get_target_object.device_under_tests_info[ap]['model'],
                branch="",
                commit_id='',
                limit='',
                offset='3000')
            latest_4_release_images = get_target_object.firmware_library_object.get_latest_four_release_images(
                firmware_list=firmware_list)
            if len(latest_4_release_images) < 4:
                pytest.fail("Latest 4 release images are not available on GW")
            # check the current AP Revision before upgrade

            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

            # print and report the firmware versions before upgrade
            allure.attach(name="Current Firmware Image: ",
                          body=str(current_version))
            logging.info("Current Firmware Image: " + str(current_version))
            allure.attach(name="F1 Firmware Image: ",
                          body=str(latest_4_release_images[0]))
            logging.info("F1 Firmware Image: " + str(latest_4_release_images[0]))
            allure.attach(name="F3 Firmware Image: ",
                          body=str(latest_4_release_images[2]))
            logging.info("F3 Firmware Image: " + str(latest_4_release_images[2]))
            # Check the current AP’s firmware, it should be on latest release image (F1)
            f1_version = latest_4_release_images[0]['revision'].split("/")[1].replace(" ", "")
            logging.info("f1_version: " + str(f1_version))
            logging.info("current_version: " + str(current_version))
            # If current version and F1 version are same then skip upgrade to F1
            if current_version == f1_version:
                logging.info("Skipping Upgrade! AP is already in F1 version")
                allure.attach(name="AP is already in the F1 Version",
                              body="")
            else:
                get_target_object.firmware_library_object.upgrade_firmware(
                    serial=get_target_object.device_under_tests_info[ap]['identifier'],
                    url=str(latest_4_release_images[0]['uri']))
                # wait for 300 seconds after firmware upgrade
                logging.info("Waiting for 300 Sec for Firmware Upgrade")
                time.sleep(300)

                # check the current AP Revision again
                ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
                current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                # print and report the Firmware versions after upgrade
                allure.attach(name="After Firmware Upgrade Request to F1: ",
                              body="Current revision: " + current_version + "\nF1 revision: " + f1_version)
                logging.info("current revision: " + str(current_version) +
                             "\nF1 revision: " + str(f1_version))

                if current_version == f1_version:
                    logging.info("firmware upgrade successfully to F1: " + f1_version)
                else:
                    logging.info("firmware upgrade failed to F1: " + f1_version)
                    pytest.fail("firmware upgrade failed to F1: " + f1_version)

            # Downgrade to two lower Release image (F3)
            f3_version = latest_4_release_images[2]['revision'].split("/")[1].replace(" ", "")
            logging.info("f3_version: " + str(f3_version))
            get_target_object.firmware_library_object.upgrade_firmware(
                serial=get_target_object.device_under_tests_info[ap]['identifier'],
                url=str(latest_4_release_images[2]['uri']))
            # wait for 300 seconds after firmware upgrade
            logging.info("waiting for 300 Sec for Firmware Downgrade")
            time.sleep(300)
            # check the current AP Revision again
            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
            # print and report the Firmware versions after upgrade
            allure.attach(name="After Firmware downgrade Request to F3: ",
                          body="Current revision: " + current_version + "\nF3 revision: " + f3_version)
            logging.info("current revision: " + str(current_version) +
                         "\nF3 revision: " + str(f3_version))

            if current_version == f3_version:
                logging.info("firmware downgraded successfully to F3: " + f3_version)
            else:
                logging.info("firmware downgrade failed to F3: " + f3_version)
                pytest.fail("firmware downgrade failed to F3: " + f3_version)

    @pytest.mark.upgrade_f3_to_f1
    @allure.title("Upgrade Firmware to two upper release image from (F3) to firmware (F1)")
    @allure.testcase(name="WIFI-13010",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-13010")
    def test_upgrade_f3_to_f1(self, get_target_object, get_testbed_details):
        """
                    Upgrade Firmware to two upper release image from (F3) to firmware (F1)
                    Unique marker: pytest -m "upgrade_f3_to_f1"
                    F1 - Latest release image
                    F3 - Two lower release image
        """
        for ap in range(len(get_target_object.device_under_tests_info)):
            firmware_list = get_target_object.firmware_library_object.get_firmwares(
                model=get_target_object.device_under_tests_info[ap]['model'],
                branch="",
                commit_id='',
                limit='',
                offset='3000')
            latest_4_release_images = get_target_object.firmware_library_object.get_latest_four_release_images(
                firmware_list=firmware_list)
            if len(latest_4_release_images) < 4:
                pytest.fail("Latest 4 release images are not available on GW")
            # check the current AP Revision before upgrade

            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

            # print and report the firmware versions before upgrade
            allure.attach(name="Current Firmware Image: ",
                          body=str(current_version))
            logging.info("Current Firmware Image: " + str(current_version))
            allure.attach(name="F1 Firmware Image: ",
                          body=str(latest_4_release_images[0]))
            logging.info("F1 Firmware Image: " + str(latest_4_release_images[0]))
            allure.attach(name="F3 Firmware Image: ",
                          body=str(latest_4_release_images[2]))
            logging.info("F3 Firmware Image: " + str(latest_4_release_images[2]))
            # Check the current AP’s firmware, it should be on One lower release image (F2)
            f3_version = latest_4_release_images[2]['revision'].split("/")[1].replace(" ", "")
            logging.info("f3_version: " + str(f3_version))
            logging.info("current_version: " + str(current_version))
            # If current version and F3 version are same then skip upgrade to F3
            if current_version == f3_version:
                logging.info("Skipping Upgrade! AP is already in F3 version")
                allure.attach(name="AP is already in the F3 Version",
                              body="")
            else:
                get_target_object.firmware_library_object.upgrade_firmware(
                    serial=get_target_object.device_under_tests_info[ap]['identifier'],
                    url=str(latest_4_release_images[2]['uri']))
                # wait for 300 seconds after firmware upgrade
                logging.info("Waiting for 300 Sec for Firmware Upgrade")
                time.sleep(300)

                # check the current AP Revision again
                ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
                current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                # print and report the Firmware versions after upgrade
                allure.attach(name="After Firmware Upgrade Request to F3: ",
                              body="Current revision: " + current_version + "\nF3 revision: " + f3_version)
                logging.info("current revision: " + str(current_version) +
                             "\nF3 revision: " + str(f3_version))

                if current_version == f3_version:
                    logging.info("firmware upgrade successfully to F3: " + f3_version)
                else:
                    logging.info("firmware upgrade failed to F3: " + f3_version)
                    pytest.fail("firmware upgrade failed to F3: " + f3_version)

            # Upgrade to two upper Release image (F1)
            f1_version = latest_4_release_images[0]['revision'].split("/")[1].replace(" ", "")
            logging.info("f1_version: " + str(f1_version))
            get_target_object.firmware_library_object.upgrade_firmware(
                serial=get_target_object.device_under_tests_info[ap]['identifier'],
                url=str(latest_4_release_images[0]['uri']))
            # wait for 300 seconds after firmware upgrade
            logging.info("waiting for 300 Sec for Firmware Upgrade")
            time.sleep(300)
            # check the current AP Revision again
            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
            # print and report the Firmware versions after upgrade
            allure.attach(name="After Firmware upgrade Request to F1: ",
                          body="Current revision: " + current_version + "\nF1 revision: " + f1_version)
            logging.info("current revision: " + str(current_version) +
                         "\nF1 revision: " + str(f1_version))

            if current_version == f1_version:
                logging.info("firmware upgrade successfully to F1: " + f1_version)
            else:
                logging.info("firmware upgrade failed to F1: " + f1_version)
                pytest.fail("firmware upgrade failed to F1: " + f1_version)

    @pytest.mark.downgrade_f1_to_f4
    @allure.title("Downgrade Firmware to three lower release image from (F1) to firmware image (F4)")
    @allure.testcase(name="WIFI-13011",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-13011")
    def test_downgrade_f1_to_f4(self, get_target_object, get_testbed_details):
        """
                    Downgrade Firmware to three lower release image from (F1) to firmware image (F4)
                    Unique marker: pytest -m "downgrade_f1_to_f4"
                    F1 - Latest release image
                    F4 - Three lower release image
        """
        for ap in range(len(get_target_object.device_under_tests_info)):
            firmware_list = get_target_object.firmware_library_object.get_firmwares(
                model=get_target_object.device_under_tests_info[ap]['model'],
                branch="",
                commit_id='',
                limit='',
                offset='3000')
            latest_4_release_images = get_target_object.firmware_library_object.get_latest_four_release_images(
                firmware_list=firmware_list)
            if len(latest_4_release_images) < 4:
                pytest.fail("Latest 4 release images are not available on GW")
            # check the current AP Revision before upgrade

            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

            # print and report the firmware versions before upgrade
            allure.attach(name="Current Firmware Image: ",
                          body=str(current_version))
            logging.info("Current Firmware Image: " + str(current_version))
            allure.attach(name="F1 Firmware Image: ",
                          body=str(latest_4_release_images[0]))
            logging.info("F1 Firmware Image: " + str(latest_4_release_images[0]))
            allure.attach(name="F4 Firmware Image: ",
                          body=str(latest_4_release_images[3]))
            logging.info("F4 Firmware Image: " + str(latest_4_release_images[3]))
            # Check the current AP’s firmware, it should be on latest release image (F1)
            f1_version = latest_4_release_images[0]['revision'].split("/")[1].replace(" ", "")
            logging.info("f1_version: " + str(f1_version))
            logging.info("current_version: " + str(current_version))
            # If current version and F1 version are same then skip upgrade to F1
            if current_version == f1_version:
                logging.info("Skipping Upgrade! AP is already in F1 version")
                allure.attach(name="AP is already in the F1 Version",
                              body="")
            else:
                get_target_object.firmware_library_object.upgrade_firmware(
                    serial=get_target_object.device_under_tests_info[ap]['identifier'],
                    url=str(latest_4_release_images[0]['uri']))
                # wait for 300 seconds after firmware upgrade
                logging.info("Waiting for 300 Sec for Firmware Upgrade")
                time.sleep(300)

                # check the current AP Revision again
                ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
                current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                # print and report the Firmware versions after upgrade
                allure.attach(name="After Firmware Upgrade Request to F1: ",
                              body="Current revision: " + current_version + "\nF1 revision: " + f1_version)
                logging.info("current revision: " + str(current_version) +
                             "\nF1 revision: " + str(f1_version))

                if current_version == f1_version:
                    logging.info("firmware upgrade successfully to F1: " + f1_version)
                else:
                    logging.info("firmware upgrade failed to F1: " + f1_version)
                    pytest.fail("firmware upgrade failed to F1: " + f1_version)

            # Downgrade to three lower Release image (F4)
            f4_version = latest_4_release_images[3]['revision'].split("/")[1].replace(" ", "")
            logging.info("f4_version: " + str(f4_version))
            get_target_object.firmware_library_object.upgrade_firmware(
                serial=get_target_object.device_under_tests_info[ap]['identifier'],
                url=str(latest_4_release_images[3]['uri']))
            # wait for 300 seconds after firmware upgrade
            logging.info("waiting for 300 Sec for Firmware Downgrade")
            time.sleep(300)
            # check the current AP Revision again
            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
            # print and report the Firmware versions after upgrade
            allure.attach(name="After Firmware downgrade Request to F4: ",
                          body="Current revision: " + current_version + "\nF4 revision: " + f4_version)
            logging.info("current revision: " + str(current_version) +
                         "\nF4 revision: " + str(f4_version))

            if current_version == f4_version:
                logging.info("firmware downgraded successfully to F4: " + f4_version)
            else:
                logging.info("firmware downgrade failed to F4: " + f4_version)
                pytest.fail("firmware downgrade failed to F4: " + f4_version)

    @pytest.mark.upgrade_f4_to_f1
    @allure.title("Upgrade Firmware to three upper release image from (F4) to firmware (F1)")
    @allure.testcase(name="WIFI-13012",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-13012")
    def test_upgrade_f4_to_f1(self, get_target_object, get_testbed_details):
        """
                    Upgrade Firmware to one upper release image from (F2) to firmware image (F1)
                    Unique marker: pytest -m "upgrade_f4_to_f1"
                    F1 - Latest release image
                    F4 - Three lower release image
        """
        for ap in range(len(get_target_object.device_under_tests_info)):
            firmware_list = get_target_object.firmware_library_object.get_firmwares(
                model=get_target_object.device_under_tests_info[ap]['model'],
                branch="",
                commit_id='',
                limit='',
                offset='3000')
            latest_4_release_images = get_target_object.firmware_library_object.get_latest_four_release_images(
                firmware_list=firmware_list)
            if len(latest_4_release_images) < 4:
                pytest.fail("Latest 4 release images are not available on GW")
            # check the current AP Revision before upgrade

            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]

            # print and report the firmware versions before upgrade
            allure.attach(name="Current Firmware Image: ",
                          body=str(current_version))
            logging.info("Current Firmware Image: " + str(current_version))
            allure.attach(name="F1 Firmware Image: ",
                          body=str(latest_4_release_images[0]))
            logging.info("F1 Firmware Image: " + str(latest_4_release_images[0]))
            allure.attach(name="F4 Firmware Image: ",
                          body=str(latest_4_release_images[3]))
            logging.info("F4 Firmware Image: " + str(latest_4_release_images[3]))
            # Check the current AP’s firmware, it should be on One lower release image (F2)
            f4_version = latest_4_release_images[3]['revision'].split("/")[1].replace(" ", "")
            logging.info("f4_version: " + str(f4_version))
            logging.info("current_version: " + str(current_version))
            # If current version and F4 version are same then skip upgrade to F4
            if current_version == f4_version:
                logging.info("Skipping Upgrade! AP is already in F4 version")
                allure.attach(name="AP is already in the F4 Version",
                              body="")
            else:
                get_target_object.firmware_library_object.upgrade_firmware(
                    serial=get_target_object.device_under_tests_info[ap]['identifier'],
                    url=str(latest_4_release_images[3]['uri']))
                # wait for 300 seconds after firmware upgrade
                logging.info("Waiting for 300 Sec for Firmware Upgrade")
                time.sleep(300)

                # check the current AP Revision again
                ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
                current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
                # print and report the Firmware versions after upgrade
                allure.attach(name="After Firmware Upgrade Request to F4: ",
                              body="Current revision: " + current_version + "\nF4 revision: " + f4_version)
                logging.info("current revision: " + str(current_version) +
                             "\nF4 revision: " + str(f4_version))

                if current_version == f4_version:
                    logging.info("firmware upgrade successfully to F4: " + f4_version)
                else:
                    logging.info("firmware upgrade failed to F4: " + f4_version)
                    pytest.fail("firmware upgrade failed to F4: " + f4_version)

            # Upgrade to three upper Release image (F1)
            f1_version = latest_4_release_images[0]['revision'].split("/")[1].replace(" ", "")
            logging.info("f1_version: " + str(f1_version))
            get_target_object.firmware_library_object.upgrade_firmware(
                serial=get_target_object.device_under_tests_info[ap]['identifier'],
                url=str(latest_4_release_images[0]['uri']))
            # wait for 300 seconds after firmware upgrade
            logging.info("waiting for 300 Sec for Firmware Upgrade")
            time.sleep(300)
            # check the current AP Revision again
            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
            # print and report the Firmware versions after upgrade
            allure.attach(name="After Firmware upgrade Request to F1: ",
                          body="Current revision: " + current_version + "\nF1 revision: " + f1_version)
            logging.info("current revision: " + str(current_version) +
                         "\nF1 revision: " + str(f1_version))

            if current_version == f1_version:
                logging.info("firmware upgrade successfully to F1: " + f1_version)
            else:
                logging.info("firmware upgrade failed to F1: " + f1_version)
                pytest.fail("firmware upgrade failed to F1: " + f1_version)





