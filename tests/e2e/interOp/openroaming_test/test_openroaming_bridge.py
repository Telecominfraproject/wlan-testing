"""

    Client Connect : BRIDGE Mode
    pytest -m "client_connect_tests and nat and enterprise"

"""
import logging
import random
import string
import time

import allure
import pytest

pytestmark = [pytest.mark.client_connect_tests, pytest.mark.bridge, pytest.mark.enterprise, pytest.mark.ow_sanity_interop]

setup_params_enterprise_two_br = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "pass_point", "appliedRadios": ["5G"]}],
        "wpa_wpa2_enterprise_mixed": [
            {"ssid_name": "wpa_wpa2_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "Meta_secure", "appliedRadios": ["5G"]}],
        "wpa3_enterprise_mixed": [
            {"ssid_name": "wpa3_m_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "wpa3_m_eap_5g", "appliedRadios": ["5G"]}]
    },
    "rf": {},
    "radius": True
}
@allure.feature("BRIDGE MODE CLIENT CONNECT")
@allure.parent_suite("Client Connect Tests")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="Enterprise security mode Client Connect")
@pytest.mark.parametrize(
    'setup_open_roaming_configuration',
    [setup_params_enterprise_two_br],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_open_roaming_configuration")
class TestBridgeModeConnectSuiteTwo(object):
    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.fiveg
    @allure.story('wpa_wpa2_enterprise_mixed 5 GHZ Band')
    @pytest.mark.usefixtures("setup_open_roaming_configuration")
    @allure.title("BRIDGE Mode Client Connect Test with wpa_wpa2_enterprise_mixed encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4572", name="JIRA LINK")
    def test_bridge_wpa_wpa2_eap_mixed_5g_client_connect(self,
                                                         num_stations, setup_open_roaming_configuration):
        print("1.Config:", setup_open_roaming_configuration)
        assert True