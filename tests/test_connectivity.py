"""
    Test Case Module:  Testing Basic Connectivity with Resources
"""
import time

import allure
import pytest
import requests
import json

pytestmark = [pytest.mark.test_resources, pytest.mark.sanity, pytest.mark.uc_sanity,
              pytest.mark.sanity_55, pytest.mark.interop_uc_sanity, pytest.mark.android, pytest.mark.ios,
              pytest.mark.client_connect]

state = True
sdk_expected = True


@allure.testcase(name="Test Resources", url="")
class TestResources(object):
    """Test Case Class: Test cases to cover resource Connectivity"""

    @pytest.mark.test_cloud_controller
    @pytest.mark.uc_sanity
    @pytest.mark.interop_uc_sanity
    @allure.testcase(name="test_controller_connectivity", url="")
    def test_controller_connectivity(self, setup_controller, get_configuration):
        """Test case to verify cloud Controller Connectivity"""

        login_response_json = setup_controller.login_resp.json()
        response_code = setup_controller.login_resp.status_code
        request_url = setup_controller.login_resp.request.url
        print("Login_Request_URL: ", str(request_url))
        allure.attach(name="Login_Request_URL: ", body=str(request_url))
        print("response_code: ", response_code)
        allure.attach(name="Login Response Code: ", body=str(response_code))
        print("login_response_json: ", login_response_json)
        allure.attach(name="Login Response JSON: ", body=str(setup_controller.login_resp.json()))
        if response_code != 200:
            pytest.exit(
                "exiting from pytest, login response is no 200: " + str(setup_controller.login_resp.status_code))

        gw_system_info = setup_controller.get_system_gw()
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

        fms_system_info = setup_controller.get_system_fms()
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
        prov_system_info = setup_controller.get_system_prov()
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
        #         if setup_controller.get_system_gw().status_code != 200 and i < 9:
        #             print("sleeping for 30 sec, gw service is down with response not equals to 200")
        #             time.sleep(30)
        #         elif setup_controller.get_system_gw().status_code != 200 and i == 9:
        #             pytest.exit("GW service is not up yet, exiting from pytest")
        #         else:
        #             break
        #
        # if fms_status_check != 200:
        #     for i in range(10):
        #         if setup_controller.get_system_fms().status_code != 200 and i < 9:
        #             print("sleeping for 30 sec, fms service is down with response not equals to 200")
        #             time.sleep(30)
        #         elif setup_controller.get_system_fms().status_code != 200 and i == 9:
        #             pytest.exit("fms service is not up yet, exiting from pytest")
        #         else:
        #             break
        #
        # available_device_list = []
        # devices = setup_controller.get_devices()
        # number_devices = len(devices["devices"])
        # for i in range(number_devices):
        #     available_device_list.append(devices["devices"][i]["serialNumber"])
        # print("available_device_list: ", available_device_list)
        #
        # if get_configuration["access_point"][0]["serial"] not in available_device_list:
        #     for i in range(10):
        #         available_device_list = []
        #         devices = setup_controller.get_devices()
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
    @allure.testcase(name="test_access_points_connectivity", url="")
    def test_access_points_connectivity(self, setup_controller, get_uci_show, test_access_point, get_configuration,
                                        test_ap_connection_status, fixtures_ver, get_apnos_logs):
        """Test case to verify Access Points Connectivity"""
        # print(test_ap_connection_status)
        # pytest.exit("")
        data = []
        for status in test_access_point:
            data.append(status[0])
        connection, redirector = test_ap_connection_status
        allure.attach(name="AP - Cloud connectivity info", body=str(fixtures_ver.ubus_connection))
        print("test_ap_connection_status: ", connection, redirector)
        expected_sdk = str(
            get_configuration["controller"]['url'].replace("https://sec", "\'gw").replace(":16001", "\'"))
        print("Expected SDK: ", expected_sdk)
        allure.attach(name="Exoected SDK: ", body=str(expected_sdk))
        print("SDK On AP: ", str(get_uci_show.split("=")[1]))
        allure.attach(name="SDK Pointed by AP: ", body=str(get_uci_show.split("=")[1]))
        for ap in get_configuration["access_point"]:
            out = setup_controller.get_device_by_serial_number(serial_number=ap["serial"])
            if "ErrorCode" in out.keys():
                print(out)
                allure.attach(name="Error Device not found in Gateway: ", body=str(out))
                pytest.exit("Error Device not found in Gateway:")
            else:
                print(out)
                allure.attach(name="Device is available in Gateway: ", body=str(out))
        for log in get_apnos_logs:
            allure.attach(name="AP Logs: ", body=log)
        if expected_sdk not in get_uci_show:
            global sdk_expected
            sdk_expected = False
            pytest.fail("AP has invalid Redirector")
            pytest.exit("AP has invalid Redirector")
        if test_ap_connection_status[0] == 0:
            global state
            state = False
            pytest.fail("AP in Disconnected State")
            pytest.exit("AP in Disconnected State")
        assert False not in data

    @pytest.mark.traffic_generator_connectivity
    @allure.testcase(name="test_traffic_generator_connectivity", url="")
    def test_traffic_generator_connectivity(self, traffic_generator_connectivity):
        """Test case to verify Traffic Generator Connectivity"""
        allure.attach(name="LANforge version", body=str(traffic_generator_connectivity))
        assert traffic_generator_connectivity

    def test_ap_conn_state(self):
        global state
        if state == False:
            pytest.exit("AP is in DISCONNECTED State")
        global sdk_expected
        if sdk_expected == False:
            pytest.exit("AP has invalid Redirector")
        assert True


@allure.testcase(name="Firmware Management", url="")
@pytest.mark.uc_firmware
class TestFMS(object):

    @pytest.mark.get_firmware_list
    def test_fms_version_list(self, fixtures_ver, get_configuration, get_ap_logs):
        PASS = []
        for ap in get_configuration['access_point']:
            # get the latest branch
            firmware_list = fixtures_ver.fw_client.get_firmwares(model=ap['model'],
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
                response = requests.get(ap['version'])
                print("URL is valid and exists on the internet")
                allure.attach(name="firmware url: ", body=str(ap['version']))
                target_revision_commit = ap['version'].split("-")[-2]
                target_revision_branch = ap['version'].split("-")[-3]
                flag = True
                for i in release_list_data:
                    if target_revision_commit == i.split('-')[-1] and target_revision_branch == i.split('-')[-2]:
                        print('target firmware : ' + ap['version'] + " is available in FMS : " + i)
                        allure.attach(name='target firmware : ' + ap['version'] + " is available in FMS : " + i,
                                      body="")
                        PASS.append(True)
                        flag = False

                if flag:
                    print('target firmware : ' + ap['version'] + " is not available in FMS : ")
                    allure.attach(name='target firmware : ' + ap['version'] + " is not available in FMS : ",
                                  body="")
                    PASS.append(False)
                break
            except Exception as e:
                pass

            if ap['version'].split('-')[1] == "latest":

                for firmware in firmware_list:
                    if ap['version'].split('-')[0] == 'release':
                        version = firmware['revision'].split("/")[1].replace(" ", "").split('-')[1]
                        if firmware['revision'].split("/")[1].replace(" ", "").split('-')[1].__contains__('v2.'):
                            print("Target Firmware: \n", firmware)
                            allure.attach(name="Target firmware : ", body=str(firmware['release']))
                            break

                    if firmware['release'].split("-")[-2] == ap['version'].split('-')[0]:
                        print("Target Firmware: \n", firmware)
                        allure.attach(name="Target firmware : ", body=str(firmware['release']))
                        break
            else:
                flag = True
                for firmware in firmware_list:
                    if ap['version'].split('-')[0] == 'release':
                        branch = firmware['revision'].split("/")[1].replace(" ", "").split('-')[1]
                        commit = ap['version'].split('-')[1]
                        if branch.__contains__('v2.') and commit == firmware['release'].split('-')[-1]:
                            print("Target Firmware: \n", firmware)
                            allure.attach(name="Target firmware : ", body=str(firmware['release']))
                            PASS.append(True)
                            flag = False
                            break
                    if ap['version'].split('-')[1] == firmware['release'].split('-')[-1] and ap['version'].split('-')[
                        0] == \
                            firmware['release'].split('-')[-2]:
                        print('target firmware : ' + ap['version'] + " is available in FMS : " + firmware['release'])
                        allure.attach(
                            name='target firmware : ' + ap['version'] + " is available in FMS : " + firmware['release']
                            , body="")
                        PASS.append(True)
                        flag = False

                if flag:
                    print('target firmware : ' + ap['version'] + " is not available in FMS : ")
                    allure.attach(name='target firmware : ' + ap['version'] + " is not available in FMS : ",
                                  body="")
                    PASS.append(False)
        assert False not in PASS

    @pytest.mark.firmware_upgrade
    def test_firmware_upgrade_request(self, firmware_upgrade, get_ap_logs, test_ap_connection_status):
        for update in firmware_upgrade:
            allure.attach(name='serial: ' + update[0], body="")
        if test_ap_connection_status[0] == 0:
            assert False
            pytest.exit("AP in Disconnected State")
        assert True

    @pytest.mark.test_firmware_ap
    def test_firmware_upgrade_status_AP(self, firmware_upgrade, get_ap_logs):
        allure.attach(name="firmware Upgrade Status:", body="")
        assert True

    @pytest.mark.test_firmware_gw
    def test_firmware_upgrade_status_gateway(self, get_apnos, get_configuration, setup_controller, get_ap_logs,
                                             add_firmware_property_after_upgrade):
        status = []
        for ap in get_configuration['access_point']:
            ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
            ap_version = ap_ssh.get_ap_version_ucentral()
            current_version_ap = str(ap_version).split()
            data = setup_controller.get_device_by_serial_number(serial_number=ap['serial'])
            allure.attach(name=str(data['firmware']) + str(current_version_ap), body="")
            status.append(current_version_ap == data['firmware'].split())
        assert False not in status
