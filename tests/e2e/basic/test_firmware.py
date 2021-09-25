"""
    Test Case Module:  setup test cases for basic test cases
    Details:    Firmware Upgrade

"""
import allure
import pytest

pytestmark = [pytest.mark.firmware, pytest.mark.sanity, pytest.mark.sanity_light,
              pytest.mark.usefixtures("setup_test_run")]


@allure.testcase("firmware upgrade from Cloud")
@pytest.mark.firmware_cloud
class TestFirmware(object):

    @pytest.mark.firmware_create
    def test_firmware_create(self, upload_firmware, update_report, test_cases):
        if upload_firmware != 0:
            PASS = True
        else:
            PASS = False
        assert PASS

    @pytest.mark.firmware_upgrade
    def test_firmware_upgrade_request(self, upgrade_firmware, update_report, test_cases):
        print(upgrade_firmware)
        if not upgrade_firmware:
            PASS = False
        else:
            PASS = True
        assert PASS

    @pytest.mark.check_active_firmware_cloud
    def test_active_version_cloud(self, get_latest_firmware, get_equipment_ref, setup_controller,
                                  update_report, test_cases):
        ap_fw_list = []
        for i in get_equipment_ref:
            ap_fw_list.append(setup_controller.get_ap_firmware_old_method(equipment_id=i))

        assert get_latest_firmware == ap_fw_list


@pytest.mark.firmware_ap
def test_ap_firmware(get_configuration, get_apnos, get_latest_firmware, update_report,
                     test_cases):
    """yields the active version of firmware on ap"""
    active_fw_list = []
    try:
        for access_point in get_configuration['access_point']:
            ap_ssh = get_apnos(access_point, sdk="1.x")
            active_fw = ap_ssh.get_active_firmware()
            active_fw_list.append(active_fw)
    except Exception as e:
        print(e)
        active_fw_list = []
    assert active_fw_list == get_latest_firmware
