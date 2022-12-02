"""

    Multi Association and Disassociation: BRIDGE Mode
    pytest -m "multi_assoc_disassoc_tests and wpa2_personal and bridge"

"""

import pytest
import allure

pytestmark = [pytest.mark.advance, pytest.mark.multi_assoc_disassoc_tests, pytest.mark.bridge, pytest.mark.wpa2_personal]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@allure.parent_suite("Multi Association and Disassociation Tests")
@allure.suite("WPA2 Personal Security")
@allure.sub_suite("Bridge Mode")
@allure.feature("UDP upload")
@pytest.mark.usefixtures("setup_configuration")
class TestMultiAssoDisassoBridge(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5691", name="WIFI-5691")
    @pytest.mark.twog
    @pytest.mark.udp_upload_2g
    @pytest.mark.karthika
    @allure.title("Test for Multi Association and Disassociation for UDP upload 2.4G")
    def test_multi_asso_disasso_udp_upload_nss2_2g(self, get_test_library, setup_configuration, check_connectivity):
        """
                pytest -m "multi_assoc_disassoc_tests and wpa2_personal and bridge and twog and udp_upload_2g"
        """
        mode = "BRIDGE"
        vlan = 1
        result, discription = get_test_library.multi_asso_disasso(band="2G", num_stations=16, dut_data=setup_configuration,
                                                            mode = mode, vlan=vlan, instance_name="udp_upload_2g",
                                                            traffic_direction="upload", traffic_rate="4Mbps")
        if result:
            assert True
        else:
            assert False, discription

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5692", name="WIFI-5692")
    @pytest.mark.twog
    @pytest.mark.udp_download_2g
    @allure.title("Test for Multi Association and Disassociation for UDP download 2.4G")
    def test_multi_asso_disasso_udp_download_nss2_2g(self, get_test_library, setup_configuration, check_connectivity):
        """
                pytest -m "multi_assoc_disassoc_tests and wpa2_personal and bridge and twog and udp_download_2g"
        """
        mode = "BRIDGE"
        vlan = 1
        result, discription = get_test_library.multi_asso_disasso(band="2G", num_stations=16,
                                                                  dut_data=setup_configuration,
                                                                  mode=mode, vlan=vlan, instance_name="udp_download_2g",
                                                                  traffic_direction="download", traffic_rate="4Mbps")
        if result:
            assert True
        else:
            assert False, discription

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5693", name="WIFI-5693")
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_5g
    @allure.title("Test for Multi Association and Disassociation for UDP upload 5G")
    def test_multi_asso_disasso_udp_upload_nss2_5g(self, get_test_library, setup_configuration, check_connectivity):
        """
                pytest -m "multi_assoc_disassoc_tests and wpa2_personal and bridge and fiveg and udp_upload_5g"
        """
        mode = "BRIDGE"
        vlan = 1
        result, discription = get_test_library.multi_asso_disasso(band="5G", num_stations=16,
                                                                  dut_data=setup_configuration,
                                                                  mode=mode, vlan=vlan, instance_name="udp_upload_5g",
                                                                  traffic_direction="upload", traffic_rate="8Mbps")
        if result:
            assert True
        else:
            assert False, discription

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5694", name="WIFI-5694")
    @pytest.mark.fiveg
    @pytest.mark.udp_download_5g
    @allure.title("Test for Multi Association and Disassociation for UDP download 5G")
    def test_multi_asso_disasso_udp_download_nss2_5g(self, get_test_library, setup_configuration,check_connectivity):
        """
                pytest -m "multi_assoc_disassoc_tests and wpa2_personal and bridge and fiveg and udp_download_5g"
        """
        mode = "BRIDGE"
        vlan = 1
        result, discription = get_test_library.multi_asso_disasso(band="5G", num_stations=16,
                                                                  dut_data=setup_configuration,
                                                                  mode=mode, vlan=vlan, instance_name="udp_download_5g",
                                                                  traffic_direction="download", traffic_rate="8Mbps")
        if result:
            assert True
        else:
            assert False, discription


