"""

    Multi Association and Disassociation: NAT Mode
    pytest -m "multi_assoc_disassoc_tests and wpa2_personal and nat"

"""

import pytest
import allure

pytestmark = [pytest.mark.advance, pytest.mark.multi_assoc_disassoc_tests, pytest.mark.nat, pytest.mark.wpa2_personal]

setup_params_general = {
    "mode": "NAT",
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
@allure.sub_suite("Nat Mode")
@allure.feature("UDP upload")
@pytest.mark.usefixtures("setup_configuration")
class TestMultiAssoDisassoNat(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5848", name="WIFI-5848")
    @pytest.mark.twog
    @pytest.mark.udp_upload_2g
    @allure.title("Test for Multi Association and Disassociation for UDP upload 2.4G")
    def test_multi_asso_disasso_NAT_udp_upload_nss2_2g(self, get_test_library, setup_configuration, check_connectivity):
        """
                pytest -m "multi_assoc_disassoc_tests and wpa2_personal and nat and twog and udp_upload_2g"
        """
        mode = "NAT"
        vlan = 1
        result, discription = get_test_library.multi_asso_disasso(band="2G", num_stations=16, dut_data=setup_configuration,
                                                            mode = mode, vlan=vlan, instance_name="udp_upload_2g",
                                                            traffic_direction="upload", traffic_rate="4Mbps")
        if result:
            assert True
        else:
            assert False, discription

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5870", name="WIFI-5870")
    @pytest.mark.twog
    @pytest.mark.udp_download_2g
    @allure.title("Test for Multi Association and Disassociation for UDP download 2.4G")
    def test_multi_asso_disasso_NAT_udp_download_nss2_2g(self, get_test_library, setup_configuration):
        """
                pytest -m "multi_assoc_disassoc_tests and wpa2_personal and nat and twog and udp_download_2g"
        """
        mode = "NAT"
        vlan = 1
        result, discription = get_test_library.multi_asso_disasso(band="2G", num_stations=16,
                                                                  dut_data=setup_configuration,
                                                                  mode=mode, vlan=vlan, instance_name="udp_download_2g",
                                                                  traffic_direction="download", traffic_rate="4Mbps")
        if result:
            assert True
        else:
            assert False, discription

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5871", name="WIFI-5871")
    @pytest.mark.fiveg
    @pytest.mark.udp_upload_5g
    @allure.title("Test for Multi Association and Disassociation for UDP upload 5G")
    def test_multi_asso_disasso_NAT_udp_upload_nss2_5g(self, get_test_library, setup_configuration):
        """
                pytest -m "multi_assoc_disassoc_tests and wpa2_personal and nat and fiveg and udp_upload_5g"
        """
        mode = "NAT"
        vlan = 1
        result, discription = get_test_library.multi_asso_disasso(band="5G", num_stations=16,
                                                                  dut_data=setup_configuration,
                                                                  mode=mode, vlan=vlan, instance_name="udp_upload_5g",
                                                                  traffic_direction="upload", traffic_rate="8Mbps")
        if result:
            assert True
        else:
            assert False, discription

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5872", name="WIFI-5872")
    @pytest.mark.fiveg
    @pytest.mark.udp_download_5g
    @allure.title("Test for Multi Association and Disassociation for UDP download 5G")
    def test_multi_asso_disasso_NAT_udp_download_nss2_5g(self, get_test_library, setup_configuration):
        """
                pytest -m "multi_assoc_disassoc_tests and wpa2_personal and nat and fiveg and udp_download_5g"
        """
        mode = "NAT"
        vlan = 1
        result, discription = get_test_library.multi_asso_disasso(band="5G", num_stations=16,
                                                                  dut_data=setup_configuration,
                                                                  mode=mode, vlan=vlan, instance_name="udp_download_5g",
                                                                  traffic_direction="download", traffic_rate="8Mbps")
        if result:
            assert True
        else:
            assert False, discription


