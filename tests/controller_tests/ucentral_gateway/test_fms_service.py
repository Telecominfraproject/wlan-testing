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
@pytest.mark.ow_regression_lf
@allure.parent_suite("Firmware Tests")
@allure.suite("Firmware Upgrade/Downgrade Tests")
class TestFirmwareUpgradeDowngrade(object):
    @pytest.mark.upgrade_downgrade_test
    @allure.title("Firmware Downgrade and Upgrade test")
    @allure.testcase(name="WIFI-13007",
                     url="https://telecominfraproject.atlassian.net/browse/WIFI-13012")
    def test_upgrade_downgrade_tests(self, get_target_object, get_testbed_details):
        """
                    To validate the reliability and correctness of the firmware downgrade and upgrade process
                    on Access Points (APs) for three consecutive releases, ensuring no functionality issues.
                    Unique marker: pytest -m "upgrade_downgrade_test"
                    F1 - Current AP firmware
                    F2 - One lower release image
                    F3 - Two lower release image
                    F4 - Three lower release image
                    Flow:
                    AP is on F1 (If F1 is current AP image)
                    AP downgrade to F2
                    AP upgrade from F2 to F1
                    AP downgrade from F1 to F3
                    AP upgrade from F3 to F1
                    AP downgrade from F1 to F4
                    AP upgrade from F4 to F1
        """
        for ap in range(len(get_target_object.device_under_tests_info)):
            firmware_list = get_target_object.firmware_library_object.get_firmwares(
                model=get_target_object.device_under_tests_info[ap]['model'],
                branch="",
                commit_id='',
                limit='',
                offset='3000')
            # check the current AP Revision (F1)
            ap_version_f1 = get_target_object.dut_library_object.get_ap_version(idx=ap)

            current_version = str(ap_version_f1).split("/")[1].replace(" ", "").splitlines()[0]
            f1_version = current_version
            # Finding uri for current image
            for i in firmware_list:
                if f1_version in i["revision"]:
                    ap_version_f1 = i
                    break
            latest_3_release_images = get_target_object.firmware_library_object.get_least_three_release_images_from_current_image(
                firmware_list=firmware_list, current_image=current_version)
            if len(latest_3_release_images) < 3:
                pytest.fail("Least 3 release images from current image are not available on GW")
            allure.attach(name="Current Firmware Image(F1): ",
                          body=str(ap_version_f1))
            logging.info("Current Firmware Image(F1): " + str(ap_version_f1))
            allure.attach(name="F2 Firmware Image: ",
                          body=str(latest_3_release_images[0]))
            logging.info("F2 Firmware Image: " + str(latest_3_release_images[0]))
            allure.attach(name="F3 Firmware Image: ",
                          body=str(latest_3_release_images[1]))
            logging.info("F3 Firmware Image: " + str(latest_3_release_images[1]))
            allure.attach(name="F4 Firmware Image: ",
                          body=str(latest_3_release_images[2]))
            logging.info("F4 Firmware Image: " + str(latest_3_release_images[2]))
            f1_version = current_version
            f2_version = latest_3_release_images[0]['revision'].split("/")[1].replace(" ", "")
            f3_version = latest_3_release_images[1]['revision'].split("/")[1].replace(" ", "")
            f4_version = latest_3_release_images[2]['revision'].split("/")[1].replace(" ", "")
            # Downgrade F1 to F2
            logging.info("---------- Downgrading F1 to F2----------")
            get_target_object.firmware_library_object.upgrade_firmware(
                serial=get_target_object.device_under_tests_info[ap]['identifier'],
                url=str(latest_3_release_images[0]['uri']))
            # wait for 300 seconds after firmware upgrade
            logging.info("Waiting for 300 Sec for Firmware Downgrade")
            time.sleep(300)
            # check the current AP Revision again
            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
            # print and report the Firmware versions after upgrade
            allure.attach(name="After Firmware Downgrade Request to F2 from F1: ",
                          body="Current revision: " + current_version + "\nF2 revision: " + f2_version)
            logging.info("current revision: " + str(current_version) +
                         "\nF2 revision: " + str(f2_version))

            if current_version == f2_version:
                logging.info("firmware Downgrade successfully to F2: " + f2_version)
            else:
                logging.info("firmware Downgrade failed to F2: " + f2_version)
                pytest.fail("firmware Downgrade failed to F2: " + f2_version)

            # Upgrade F2 to F1
            logging.info("---------- Upgrading F2 to F1----------")
            get_target_object.firmware_library_object.upgrade_firmware(
                serial=get_target_object.device_under_tests_info[ap]['identifier'],
                url=str(ap_version_f1['uri']))
            # wait for 300 seconds after firmware upgrade
            logging.info("Waiting for 300 Sec for Firmware Downgrade")
            time.sleep(300)

            # check the current AP Revision again
            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
            # print and report the Firmware versions after upgrade
            allure.attach(name="After Firmware Upgrade Request to F1 from F2: ",
                          body="Current revision: " + current_version + "\nF1 revision: " + f1_version)
            logging.info("current revision: " + str(current_version) +
                         "\nF1 revision: " + str(f1_version))

            if current_version == f1_version:
                logging.info("firmware Upgrade successfully to F1: " + f1_version)
            else:
                logging.info("firmware Upgrade failed to F1: " + f1_version)
                pytest.fail("firmware Upgrade failed to F1: " + f1_version)

            # Downgrade F1 to F3
            logging.info("---------- Downgrading F1 to F3----------")
            get_target_object.firmware_library_object.upgrade_firmware(
                serial=get_target_object.device_under_tests_info[ap]['identifier'],
                url=str(latest_3_release_images[1]['uri']))
            # wait for 300 seconds after firmware upgrade
            logging.info("Waiting for 300 Sec for Firmware Downgrade")
            time.sleep(300)
            # check the current AP Revision again
            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
            # print and report the Firmware versions after upgrade
            allure.attach(name="After Firmware Downgrade Request to F3 from F1: ",
                          body="Current revision: " + current_version + "\nF3 revision: " + f3_version)
            logging.info("current revision: " + str(current_version) +
                         "\nF3 revision: " + str(f3_version))

            if current_version == f3_version:
                logging.info("firmware Downgrade successfully to F3: " + f3_version)
            else:
                logging.info("firmware Downgrade failed to F3: " + f3_version)
                pytest.fail("firmware Downgrade failed to F3: " + f3_version)

            # Upgrade F3 to F1
            logging.info("---------- Upgrading F3 to F1----------")
            get_target_object.firmware_library_object.upgrade_firmware(
                serial=get_target_object.device_under_tests_info[ap]['identifier'],
                url=str(ap_version_f1['uri']))
            # wait for 300 seconds after firmware upgrade
            logging.info("Waiting for 300 Sec for Firmware Downgrade")
            time.sleep(300)

            # check the current AP Revision again
            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
            # print and report the Firmware versions after upgrade
            allure.attach(name="After Firmware Upgrade Request to F1 from F3: ",
                          body="Current revision: " + current_version + "\nF1 revision: " + f1_version)
            logging.info("current revision: " + str(current_version) +
                         "\nF1 revision: " + str(f1_version))

            if current_version == f1_version:
                logging.info("firmware Upgrade successfully to F1: " + f1_version)
            else:
                logging.info("firmware Upgrade failed to F1: " + f1_version)
                pytest.fail("firmware Upgrade failed to F1: " + f1_version)

            # Downgrade F1 to F4
            logging.info("---------- Downgrading F1 to F4----------")
            get_target_object.firmware_library_object.upgrade_firmware(
                serial=get_target_object.device_under_tests_info[ap]['identifier'],
                url=str(latest_3_release_images[2]['uri']))
            # wait for 300 seconds after firmware upgrade
            logging.info("Waiting for 300 Sec for Firmware Downgrade")
            time.sleep(300)
            # check the current AP Revision again
            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
            # print and report the Firmware versions after upgrade
            allure.attach(name="After Firmware Downgrade Request to F4 from F1: ",
                          body="Current revision: " + current_version + "\nF4 revision: " + f4_version)
            logging.info("current revision: " + str(current_version) +
                         "\nF4 revision: " + str(f4_version))

            if current_version == f4_version:
                logging.info("firmware Downgrade successfully to F4: " + f4_version)
            else:
                logging.info("firmware Downgrade failed to F4: " + f4_version)
                pytest.fail("firmware Downgrade failed to F4: " + f4_version)

            # Upgrade F4 to F1
            logging.info("---------- Upgrading F4 to F1----------")
            get_target_object.firmware_library_object.upgrade_firmware(
                serial=get_target_object.device_under_tests_info[ap]['identifier'],
                url=str(ap_version_f1['uri']))
            # wait for 300 seconds after firmware upgrade
            logging.info("Waiting for 300 Sec for Firmware Downgrade")
            time.sleep(300)

            # check the current AP Revision again
            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version = str(ap_version).split("/")[1].replace(" ", "").splitlines()[0]
            # print and report the Firmware versions after upgrade
            allure.attach(name="After Firmware Upgrade Request to F1 from F4: ",
                          body="Current revision: " + current_version + "\nF1 revision: " + f1_version)
            logging.info("current revision: " + str(current_version) +
                         "\nF1 revision: " + str(f1_version))

            if current_version == f1_version:
                logging.info("firmware Upgrade successfully to F1: " + f1_version)
            else:
                logging.info("firmware Upgrade failed to F1: " + f1_version)
                pytest.fail("firmware Upgrade failed to F1: " + f1_version)






