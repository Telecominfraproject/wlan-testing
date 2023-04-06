"""
    Test Case Module:  Testing Basic Connectivity with Resources
"""
import time

import allure
import pytest
import logging
import requests
import json

pytestmark = [pytest.mark.test_resources,
              pytest.mark.sanity,
              pytest.mark.ow_sanity_lf,
              pytest.mark.ow_sanity_interop,
              pytest.mark.uc_sanity,
              pytest.mark.sanity_55,
              pytest.mark.interop_uc_sanity,
              pytest.mark.android,
              pytest.mark.ios,
              pytest.mark.client_connect]

state = True
sdk_expected = True


@allure.feature("Test Connectivity")
@allure.parent_suite("Test Connectivity")
# @allure.suite("Test Resources")
class TestResources(object):
    """Test Case Class: Test cases to cover resource Connectivity"""

    @pytest.mark.test_cloud_controller
    @allure.testcase(name="Test Cloud Controller", url="")
    @allure.title("Cloud Controller Connectivity")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-11615", name="11615")
    def test_controller_connectivity(self, get_target_object, get_testbed_details):
        """Test case to verify cloud Controller Connectivity
           Unique marker: pytest -m "test_cloud_controller"
        """

        login_response_json = get_target_object.controller_library_object.login_resp.json()
        response_code = get_target_object.controller_library_object.login_resp.status_code
        request_url = get_target_object.controller_library_object.login_resp.request.url
        print("Login_Request_URL: ", str(request_url))
        allure.attach(name="Login_Request_URL: ", body=str(request_url))
        print("response_code: ", response_code)
        allure.attach(name="Login Response Code: ", body=str(response_code))
        print("login_response_json: ", login_response_json)
        allure.attach(name="Login Response JSON: ",
                      body=str(get_target_object.controller_library_object.login_resp.json()))
        if response_code != 200:
            pytest.exit(
                "exiting from pytest, login response is no 200: " + str(
                    get_target_object.controller_library_object.login_resp.status_code))

        gw_system_info = get_target_object.controller_library_object.get_system_gw()
        request_url = gw_system_info.request.url
        allure.attach(name="get_system_gw_request: ", body=str(request_url))
        gw_system_status = gw_system_info.status_code
        gw_system_status_json = gw_system_info.json()
        print("gw_status_check response from gateway: ", gw_system_status)
        allure.attach(name="gw_status_check response from gateway: ", body=str(gw_system_status) +
                                                                           str(gw_system_status_json))
        if gw_system_status != 200:
            allure.attach(name="Login_Request_URL: ", body=str(request_url))
            pytest.exit("gw_status_check response from gateway: " + str(gw_system_status))

        fms_system_info = get_target_object.controller_library_object.get_system_fms()
        request_url = fms_system_info.request.url
        allure.attach(name="get_system_fms_request: ", body=str(request_url))
        fms_system_status = fms_system_info.status_code
        fms_system_status_json = fms_system_info.json()
        print("fms_status_check response from fms: ", fms_system_status)
        allure.attach(name="fms_status_check response from fms:", body=str(fms_system_status) +
                                                                       str(fms_system_status_json))
        if fms_system_status != 200:
            pytest.exit("fms_status_check response from fms: " + str(fms_system_status))

        # Provisioning system info
        prov_system_info = get_target_object.controller_library_object.get_system_prov()
        request_url = prov_system_info.request.url
        allure.attach(name="get_system_prov_request: ", body=str(request_url))
        prov_system_status = prov_system_info.status_code
        prov_system_status_json = prov_system_info.json()
        print("prov_status_check response from fms: ", prov_system_status)
        allure.attach(name="prov_status_check response from Prov:", body=str(prov_system_status) +
                                                                         str(prov_system_status_json))
        if prov_system_status != 200:
            pytest.exit("Prov_status_check response from Prov: " + str(prov_system_status))

        # if gw_status_check != 200:
        #     for i in range(10):
        #         if get_target_object.get_system_gw().status_code != 200 and i < 9:
        #             print("sleeping for 30 sec, gw service is down with response not equals to 200")
        #             time.sleep(30)
        #         elif get_target_object.get_system_gw().status_code != 200 and i == 9:
        #             pytest.exit("GW service is not up yet, exiting from pytest")
        #         else:
        #             break
        #
        # if fms_status_check != 200:
        #     for i in range(10):
        #         if get_target_object.get_system_fms().status_code != 200 and i < 9:
        #             print("sleeping for 30 sec, fms service is down with response not equals to 200")
        #             time.sleep(30)
        #         elif get_target_object.get_system_fms().status_code != 200 and i == 9:
        #             pytest.exit("fms service is not up yet, exiting from pytest")
        #         else:
        #             break
        #
        # available_device_list = []
        # devices = get_target_object.get_devices()
        # number_devices = len(devices["devices"])
        # for i in range(number_devices):
        #     available_device_list.append(devices["devices"][i]["serialNumber"])
        # print("available_device_list: ", available_device_list)
        #
        # if get_configuration["access_point"][0]["serial"] not in available_device_list:
        #     for i in range(10):
        #         available_device_list = []
        #         devices = get_target_object.get_devices()
        #         number_devices = len(devices["devices"])
        #         for i in range(number_devices):
        #             available_device_list.append(devices["devices"][i]["serialNumber"])
        #         print(available_device_list)
        #
        #         if get_configuration["access_point"][0]["serial"] not in available_device_list and i < 9:
        #             print("unable to find device on UI, Sleeping for 30 sec")
        #             time.sleep(30)
        #         elif get_configuration["access_point"][0]["serial"] not in available_device_list and i == 9:
        #             pytest.exit("Device" + get_configuration["access_point"][0]["serial"] + "not found on UI")
        #         else:
        #             break
        #
        # for ap in get_configuration['access_point']:
        #
        #     ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
        #     uci_show_ucentral = ap_ssh.run_generic_command("uci show ucentral")
        #     print(uci_show_ucentral)
        #     print("AP is pointing to: ", ap_ssh.get_ap_uci_show_ucentral())
        #     expected_sdk = str(get_configuration["controller"]['url'].replace("https://sec", "\'gw").replace(":16001","\'"))
        #     if ap_ssh.get_ap_uci_show_ucentral() != expected_sdk:
        #         for i in range(10):
        #             ucentral_show = str(ap_ssh.get_ap_uci_show_ucentral().strip())
        #             print("AP pointing to: ", ucentral_show)
        #             print("AP should point to: ", expected_sdk)
        #
        #             if ucentral_show != expected_sdk and i < 9:
        #                 print("AP is not pointing to right SDK, retry after 30 sec")
        #                 time.sleep(30)
        #             elif ucentral_show != expected_sdk and i == 9:
        #                 assert False
        #                 pytest.exit("AP is not pointing to right SDK")
        #             else:
        #                 break

        assert True

    @pytest.mark.test_access_points_connectivity
    @allure.testcase(name="Test Access Point Connectivity", url="")
    @allure.title("Cloud Access Point Connectivity")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-11615", name="11615")
    def test_access_points_connectivity(self, get_target_object, get_testbed_details):
        """Test case to verify Access Points Connectivity
        Unique marker: pytest -m "test_access_points_connectivity"
        """

        # Logic to Get ubus call ucentral status from AP
        connected = True
        ubus_data = []
        for i in range(0, len(get_target_object.device_under_tests_info)):
            ret_val = get_target_object.get_dut_library_object().ubus_call_ucentral_status(idx=i)
            ubus_data.append(ret_val)
            if not ret_val["connected"]:
                connected = False
                get_target_object.get_dut_library_object().verify_certificates(idx=i, print_log=True,
                                                                               attach_allure=True)
                get_target_object.get_dut_library_object().check_connectivity(idx=i, print_log=True, attach_allure=True)

        # Logic to get uci show ucentral and check the target sdk
        uci_data = []
        for i in range(0, len(get_target_object.device_under_tests_info)):
            ret_val = get_target_object.get_dut_library_object().get_uci_show(idx=i, param="ucentral.config.server")
            ret_val = str(ret_val).split("=")[1]
            uci_data.append(ret_val)
        gw_host = get_target_object.controller_library_object.gw_host.hostname
        expected_host = True
        for j in uci_data:
            if gw_host not in j:
                expected_host = False

        # If Connected but not with expected host
        if connected:
            if expected_host:
                logging.info(("Connected With Expected HOST" + "\n Current GW HOST: " + str(uci_data[0]) +
                              "\n EXPECTED GW HOST: " + str(gw_host)))
                assert True, "Connected With Expected HOST"
            else:
                logging.error("Connected With Unexpected HOST" + "\n Current GW HOST: " + str(uci_data[0]) +
                              "\n EXPECTED GW HOST: " + str(gw_host))
                pytest.exit("Connected With Unexpected HOST" + "\n Current GW HOST: " + str(uci_data[0]) +
                            "\n EXPECTED GW HOST: " + str(gw_host))
        else:
            ap_logs = get_target_object.get_dut_library_object().get_dut_logs(idx=i, print_log=False, attach_allure=False)
            allure.attach(body=ap_logs, name="Disconnected ap logs")
            logging.error("AP is in disconnected state from Ucentral gateway!!!")
            pytest.fail("AP is in disconnected state from Ucentral gateway!!!")

    # @pytest.mark.traffic_generator_connectivity
    # @allure.testcase(name="test_traffic_generator_connectivity", url="")
    # @allure.title("Traffic Generator  Connectivity")
    # def test_traffic_generator_connectivity(self, get_test_library):
    #     """Test case to verify Traffic Generator Connectivity"""
    #     port_data = get_test_library.json_get(_req_url="/port?fields=alias,port+type,ip")['interfaces']
    #     logging.info("Port data: " + str(port_data))
    #     eth_table_data = {}
    #     port = []
    #     ip = []
    #     for i in port_data:
    #         for item in i:
    #             if i[item]['port type'] == 'Ethernet':
    #                 port.append(item)
    #                 ip.append(i[item]['ip'])
    #     # creating dict for eth table
    #     eth_table_data["Port"] = port
    #     eth_table_data["ip"] = ip
    #     # Attaching eth table to allure
    #     get_test_library.attach_table_allure(data=eth_table_data, allure_name="Ethernet Table")
    #     max_num_sta_table_data = {}
    #     col = ["max possible stations", "max 2g stations", "max 5g stations", "max 6g stations", "max ax stations",
    #            "max ac stations"]
    #     max_num_sta = [get_test_library.max_possible_stations, get_test_library.max_2g_stations,
    #                    get_test_library.max_5g_stations, get_test_library.max_6g_stations,
    #                    get_test_library.max_ax_stations, get_test_library.max_ac_stations]
    #     max_num_sta_table_data[""] = col
    #     max_num_sta_table_data["Max number of stations"] = max_num_sta
    #     get_test_library.attach_table_allure(data=max_num_sta_table_data, allure_name="Max number of stations Table")
    #
    #     assert True

    # def test_ap_conn_state(self):
    #     global state
    #     if state == False:
    #         pytest.exit("AP is in DISCONNECTED State")
    #     global sdk_expected
    #     if sdk_expected == False:
    #         pytest.exit("AP has invalid Redirector")
    #     assert True

    @pytest.mark.test_ap_restrictions
    @allure.testcase(name="Check AP is restricted", url="")
    @allure.title("Check AP is restricted")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12318", name="12318")
    def test_check_restrictions(self, get_target_object, get_testbed_details):
        device_name = get_testbed_details['device_under_tests'][0]['identifier']
        resp = resp = get_target_object.controller_library_object.check_restrictions(device_name)
        if not resp:
            logging.info("AP is not restricted")
            assert True, "AP is not in restricted mode we can continue testing"
        else:
            logging.info("AP is restricted, Removing Restrictions")
            output = get_target_object.get_dut_library_object().remove_restrictions()
            resp = resp = get_target_object.controller_library_object.check_restrictions(device_name)
            if not resp:
                logging.info("Removed Restrictions")
                assert True, "Remove restrictions, Can continue testing"
            else:
                logging.error("Unable to remove restrictions")
                assert False, "Unable to remove restrictions"


@allure.testcase(name="Firmware Management", url="")
@pytest.mark.firmware
@allure.feature("Test Connectivity")
@allure.parent_suite("Test Connectivity")
class TestFirmwareUpgrade(object):

    @pytest.mark.get_firmware_list
    def test_get_firmware_version_list(self, get_testbed_details, get_target_object):
        PASS = []
        for ap in range(len(get_target_object.device_under_tests_info)):
            # get the latest branch
            firmware_list = get_target_object.firmware_library_object.get_firmwares(
                model=get_target_object.device_under_tests_info[ap]['model'],
                branch="",
                commit_id='',
                limit='10000',
                offset='3000')
            firmware_list.reverse()
            release_list_data = []
            for i in firmware_list:
                release_list_data.append(str(i['release']))
            allure.attach(name="firmware_list", body=str("\n".join(release_list_data)),
                          attachment_type=allure.attachment_type.JSON)
            try:
                response = requests.get(get_target_object.device_under_tests_info[ap]['firmware_version'])
                print("URL is valid and exists on the internet")
                allure.attach(name="firmware url: ",
                              body=str(get_target_object.device_under_tests_info[ap]['firmware_version']))
                target_revision_commit = get_target_object.device_under_tests_info[ap]['firmware_version'].split("-")[
                    -2]
                target_revision_branch = get_target_object.device_under_tests_info[ap]['firmware_version'].split("-")[
                    -3]
                flag = True
                for i in release_list_data:
                    if target_revision_commit == i.split('-')[-1] and target_revision_branch == i.split('-')[-2]:
                        print('target firmware : ' + get_target_object.device_under_tests_info[ap][
                            'version'] + " is available in FMS : " + i)
                        allure.attach(
                            name='target firmware : ' + get_target_object.device_under_tests_info[ap][
                                'firmware_version'] + " is available in FMS : " + i,
                            body="")
                        PASS.append(True)
                        flag = False

                if flag:
                    print('target firmware : ' + get_target_object.device_under_tests_info[ap][
                        'firmware_version'] + " is not available in FMS : ")
                    allure.attach(name='target firmware : ' + get_target_object.device_under_tests_info[ap][
                        'firmware_version'] + " is not available in FMS : ",
                                  body="")
                    PASS.append(False)
                break
            except Exception as e:
                pass

            if get_target_object.device_under_tests_info[ap]['firmware_version'].split('-')[1] == "latest":

                for firmware in firmware_list:
                    if get_target_object.device_under_tests_info[ap]['firmware_version'].split('-')[0] == 'release':
                        version = firmware['revision'].split("/")[1].replace(" ", "").split('-')[1]
                        if firmware['revision'].split("/")[1].replace(" ", "").split('-')[1].__contains__('v2.'):
                            print("Target Firmware: \n", firmware)
                            allure.attach(name="Target firmware : ", body=str(firmware['release']))
                            break

                    if firmware['release'].split("-")[-2] == \
                            get_target_object.device_under_tests_info[ap]['firmware_version'].split('-')[0]:
                        print("Target Firmware: \n", firmware)
                        allure.attach(name="Target firmware : ", body=str(firmware['release']))
                        break
            else:
                flag = True
                for firmware in firmware_list:
                    if get_target_object.device_under_tests_info[ap]['firmware_version'].split('-')[0] == 'release':
                        branch = firmware['revision'].split("/")[1].replace(" ", "").split('-')[1]
                        commit = get_target_object.device_under_tests_info[ap]['firmware_version'].split('-')[1]
                        if branch.__contains__('v2.') and commit == firmware['release'].split('-')[-1]:
                            print("Target Firmware: \n", firmware)
                            allure.attach(name="Target firmware : ", body=str(firmware['release']))
                            PASS.append(True)
                            flag = False
                            break
                    if get_target_object.device_under_tests_info[ap]['firmware_version'].split('-')[1] == \
                            firmware['release'].split('-')[-1] and \
                            get_target_object.device_under_tests_info[ap]['firmware_version'].split('-')[
                                0] == \
                            firmware['release'].split('-')[-2]:
                        print('target firmware : ' + get_target_object.device_under_tests_info[ap][
                            'firmware_version'] + " is available in FMS : " + firmware[
                                  'release'])
                        allure.attach(
                            name='target firmware : ' + get_target_object.device_under_tests_info[ap][
                                'firmware_version'] + " is available in FMS : " + firmware[
                                     'release']
                            , body="")
                        PASS.append(True)
                        flag = False

                if flag:
                    print('target firmware : ' + get_target_object.device_under_tests_info[ap][
                        'firmware_version'] + " is not available in FMS : ")
                    allure.attach(name='target firmware : ' + get_target_object.device_under_tests_info[ap][
                        'firmware_version'] + " is not available in FMS : ",
                                  body="")
                    PASS.append(False)
            assert False not in PASS

    @pytest.mark.firmware_upgrade
    def test_firmware_upgrade_request(self, get_target_object, get_dut_logs_per_test_case, check_connectivity):
        for update in get_target_object.setup_firmware():
            allure.attach(name='serial: ' + update[0], body="")
        assert True

    @pytest.mark.test_firmware_ap
    def test_firmware_upgrade_status_AP(self):
        allure.attach(name="firmware Upgrade Status:", body="")
        assert True

    @pytest.mark.test_firmware_gw
    def test_firmware_upgrade_status_gateway(self, get_testbed_details, get_target_object,
                                             add_firmware_property_after_upgrade):
        status = []
        for ap in range(len(get_target_object.device_under_tests_info)):
            ap_version = get_target_object.dut_library_object.get_ap_version(idx=ap)
            current_version_ap = str(ap_version).split()
            data = get_target_object.controller_library_object.get_device_by_serial_number(
                serial_number=get_target_object.device_under_tests_info[ap]['identifier'])
            data = data.json()
            allure.attach(name=str(data['firmware']) + str(current_version_ap), body="")
            status.append(current_version_ap == data['firmware'].split())
        assert False not in status
