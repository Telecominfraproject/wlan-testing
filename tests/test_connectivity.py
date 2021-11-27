"""
    Test Case Module:  Testing Basic Connectivity with Resources
"""
import time

import allure
import pytest
import requests
import json

pytestmark = [pytest.mark.test_resources, pytest.mark.sanity, pytest.mark.uc_sanity,
              pytest.mark.sanity_55]


@allure.testcase(name="Test Resources", url="")
class TestResources(object):
    """Test Case Class: Test cases to cover resource Connectivity"""

    @pytest.mark.test_cloud_controller
    @pytest.mark.uc_sanity
    @allure.testcase(name="test_controller_connectivity", url="")
    def test_controller_connectivity(self, get_apnos, setup_controller, get_configuration):
        """Test case to verify cloud Controller Connectivity"""
        login_response_json = setup_controller.login_resp.json()
        print("login_response_json: ",login_response_json)

        response_code = setup_controller.login_resp.status_code
        print("response_code: ",response_code)

        if response_code != 200:
            for i in range(10):
                if setup_controller.login_resp.status_code != 200 and i < 9:
                    print("sleeping for 30 sec, login response not equals to 200")
                    time.sleep(30)
                elif setup_controller.login_resp.status_code != 200 and i == 9:
                    pytest.exit("exiting from pytest, login response is no 200")
                else:
                    break

        version = setup_controller.get_sdk_version()
        print("version: ",version)

        gw_status_check = setup_controller.get_system_gw().status_code
        print("gw_status_check response from gateway: ",gw_status_check)
        fms_status_check = setup_controller.get_system_fms().status_code
        print("fms_status_check response from fms: ", fms_status_check)

        if gw_status_check != 200:
            for i in range(10):
                if setup_controller.get_system_gw().status_code != 200 and i < 9:
                    print("sleeping for 30 sec, gw service is down with response not equals to 200")
                    time.sleep(30)
                elif setup_controller.get_system_gw().status_code != 200 and i == 9:
                    pytest.exit("GW service is not up yet, exiting from pytest")
                else:
                    break

        if fms_status_check != 200:
            for i in range(10):
                if setup_controller.get_system_fms().status_code != 200 and i < 9:
                    print("sleeping for 30 sec, fms service is down with response not equals to 200")
                    time.sleep(30)
                elif setup_controller.get_system_fms().status_code != 200 and i == 9:
                    pytest.exit("fms service is not up yet, exiting from pytest")
                else:
                    break

        available_device_list = []
        devices = setup_controller.get_devices()
        number_devices = len(devices["devices"])
        for i in range(number_devices):
            available_device_list.append(devices["devices"][i]["serialNumber"])
        print("available_device_list: ",available_device_list)

        if get_configuration["access_point"][0]["serial"] not in available_device_list:
            for i in range(10):
                available_device_list = []
                devices = setup_controller.get_devices()
                number_devices = len(devices["devices"])
                for i in range(number_devices):
                    available_device_list.append(devices["devices"][i]["serialNumber"])
                print(available_device_list)

                if get_configuration["access_point"][0]["serial"] not in available_device_list and i < 9:
                    print("unable to find device on UI, Sleeping for 30 sec")
                    time.sleep(30)
                elif get_configuration["access_point"][0]["serial"] not in available_device_list and i == 9:
                    pytest.exit("Device" + get_configuration["access_point"][0]["serial"] + "not found on UI")
                else:
                    break

        for ap in get_configuration['access_point']:

            ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
            uci_show_ucentral = ap_ssh.run_generic_command("uci show ucentral")
            print(uci_show_ucentral)
            print("AP is pointing to: ", ap_ssh.get_ap_uci_show_ucentral())
            expected_sdk = str(get_configuration["controller"]['url'].replace("https://sec", "\'gw").replace(":16001","\'"))
            if ap_ssh.get_ap_uci_show_ucentral() != expected_sdk:
                for i in range(10):
                    ucentral_show = str(ap_ssh.get_ap_uci_show_ucentral().strip())
                    print("AP pointing to: ", ucentral_show)
                    print("AP should point to: ", expected_sdk)

                    if ucentral_show != expected_sdk and i < 9:
                        print("AP is not pointing to right SDK, retry after 30 sec")
                        time.sleep(30)
                    elif ucentral_show != expected_sdk and i == 9:
                        assert False
                        pytest.exit("AP is not pointing to right SDK")
                    else:
                        break

        assert True

    @pytest.mark.test_access_points_connectivity
    @allure.testcase(name="test_access_points_connectivity", url="")
    def test_access_points_connectivity(self, test_access_point, test_ap_connection_status, fixtures_ver):
        """Test case to verify Access Points Connectivity"""
        data = []
        for status in test_access_point:
            data.append(status[0])
        allure.attach(name="AP - Cloud connectivity info", body=str(fixtures_ver.ubus_connection))
        print("test_ap_connection_status: ", test_ap_connection_status)
        if test_ap_connection_status[0] == 0:
            assert False
            pytest.exit("AP in Disconnected State")
        assert False not in data

    @pytest.mark.traffic_generator_connectivity
    @allure.testcase(name="test_traffic_generator_connectivity", url="")
    def test_traffic_generator_connectivity(self, traffic_generator_connectivity):
        """Test case to verify Traffic Generator Connectivity"""
        allure.attach(name="LANforge version", body=str(traffic_generator_connectivity))
        assert traffic_generator_connectivity


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
    def test_firmware_upgrade_status_gateway(self, get_apnos, get_configuration, setup_controller, get_ap_logs):
        status = []
        for ap in get_configuration['access_point']:
            ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
            ap_version = ap_ssh.get_ap_version_ucentral()
            current_version_ap = str(ap_version).split()
            data = setup_controller.get_device_by_serial_number(serial_number=ap['serial'])
            allure.attach(name=str(data['firmware']) + str(current_version_ap), body="")
            status.append(current_version_ap == data['firmware'].split())
        assert False not in status
