"""

    UCentral FMS Services Rest API Tests

"""

import allure
import pytest


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
