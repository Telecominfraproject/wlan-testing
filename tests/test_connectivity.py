"""
    Test Case Module:  Testing Basic Connectivity with Resources
"""

import allure
import pytest
import requests

pytestmark = [pytest.mark.test_resources, pytest.mark.sanity, pytest.mark.uc_sanity,
              pytest.mark.sanity_55]


@allure.testcase(name="Test Resources", url="")
class TestResources(object):
    """Test Case Class: Test cases to cover resource Connectivity"""

    @pytest.mark.test_cloud_controller
    @pytest.mark.uc_sanity
    @allure.testcase(name="test_controller_connectivity", url="")
    def test_controller_connectivity(self, setup_controller):
        """Test case to verify cloud Controller Connectivity"""
        login_response_json = setup_controller.login_resp.json()
        response_code = setup_controller.login_resp.status_code
        allure.attach(name="Login Response Code", body=str(response_code))
        allure.attach(name="Login Response JSON",
                      body=str(login_response_json),
                      attachment_type=allure.attachment_type.JSON)
        version = setup_controller.get_sdk_version()
        print(version)
        assert response_code == 200

    @pytest.mark.test_access_points_connectivity
    @allure.testcase(name="test_access_points_connectivity", url="")
    def test_access_points_connectivity(self, test_access_point, fixtures_ver):
        """Test case to verify Access Points Connectivity"""
        data = []
        for status in test_access_point:
            data.append(status[0])
        allure.attach(name="AP - Cloud connectivity info", body=str(fixtures_ver.ubus_connection))
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
    def test_fms_version_list(self, fixtures_ver, get_configuration):
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
    def test_firmware_upgrade_request(self, firmware_upgrade):
        for update in firmware_upgrade:
            allure.attach(name='serial: ' + update[0], body="")
        assert True

    @pytest.mark.test_firmware_ap
    def test_firmware_upgrade_status_AP(self, firmware_upgrade):
        allure.attach(name="firmware Upgrade Status:", body="")
        assert True

    @pytest.mark.test_firmware_gw
    def test_firmware_upgrade_status_gateway(self, get_apnos, get_configuration, setup_controller):
        status = []
        for ap in get_configuration['access_point']:
            ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
            ap_version = ap_ssh.get_ap_version_ucentral()
            current_version_ap = str(ap_version).split()
            data = setup_controller.get_device_by_serial_number(serial_number=ap['serial'])
            allure.attach(name=str(data['firmware']) + str(current_version_ap), body="")
            status.append(current_version_ap == data['firmware'].split())
        assert False not in status
