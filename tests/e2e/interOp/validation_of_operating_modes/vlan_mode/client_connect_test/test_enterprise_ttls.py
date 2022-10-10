"""

    Client Connect : VLAN Mode
    pytest -m "client_connect_tests and nat and enterprise"

"""
import logging
import random
import string
import time

import allure
import pytest

pytestmark = [pytest.mark.client_connect_tests, pytest.mark.vlan, pytest.mark.enterprise]

setup_params_enterprise = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa_enterprise": [
            {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa_eap_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "vlan": 100}]},

    "rf": {},
    "radius": True
}
for sec_modes in setup_params_enterprise['ssid_modes'].keys():
    for i in range(len(setup_params_enterprise['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                              string.digits, k=N))) + str(int(time.time_ns()) % 10000)
        setup_params_enterprise['ssid_modes'][sec_modes][i]['ssid_name'] = \
            setup_params_enterprise['ssid_modes'][sec_modes][i]['ssid_name'] + "_" + rand_string

@allure.feature("VLAN MODE CLIENT CONNECT")
@allure.parent_suite("Client Connect Tests")
@allure.suite(suite_name="VLAN Mode")
@allure.sub_suite(sub_suite_name="Enterprise security mode Client Connect")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestVlanModeConnectSuiteA(object):
    """
        Vlan Client Connect (open. wpa. wpa2_personal) (twog, fiveg)
        pytest -m "client_connect_tests and vlan and enterprise"
    """

    @pytest.mark.wpa_enterprise
    @pytest.mark.twog
    @allure.title("VLAN Mode Client Connect Test for wpa enterprise 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4565", name="JIRA LINK")
    def test_vlan_wpa_eap_2g_client_connect(self, get_dut_logs_per_test_case, get_test_device_logs,
                                           num_stations, setup_configuration, get_test_library, radius_info):
        """
            VLAN Mode Client Connect Test with open encryption 2.4 GHz Band
            pytest -m "client_connect_tests and vlan and enterprise and open and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connect(ssid=ssid_name, identity=identity, ttls_passwd=ttls_passwd)

        assert passes == "PASS", result

    @pytest.mark.wpa_enterprise
    @pytest.mark.fiveg
    @allure.title("VLAN Mode Client Connect Test for wpa enterprise 5 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4566", name="JIRA LINK")
    def test_vlan_wpa_eap_5g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                                get_test_device_logs, num_stations, setup_configuration, radius_info):
        """
            VLAN Mode Client Connect Test with open encryption 5 GHz Band
            pytest -m "client_connect_tests and vlan and enterprise and open and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connect(ssid=ssid_name, identity=identity,
                                                                    ttls_passwd=ttls_passwd)

        assert passes == "PASS", result

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.title("VLAN Mode Client Connect Test for wpa2 enterprise 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4567", name="JIRA LINK")
    def test_vlan_wpa2_eap_2g_client_connect(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs,
                                               num_stations, setup_configuration, radius_info):
        """
            VLAN Mode Client Connect Test with wpa encryption 2.4 GHz Band
            pytest -m "client_connectivity_tests and vlan and enterprise and wpa and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "VLAN"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connect(ssid=ssid_name, identity=identity,
                                                                    ttls_passwd=ttls_passwd)

        assert passes == "PASS", result

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("VLAN Mode Client Connect Test Test for wpa2 enterprise 5 GHzd")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4568", name="JIRA LINK")
    def test_vlan_wpa2_eap_5g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration, radius_info):
        """
            VLAN Mode Client Connect Test with wpa encryption 5 GHz Band
            pytest -m "client_connect_tests and vlan and enterprise and wpa and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "VLAN"
        band = "fiveg"
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connect(ssid=ssid_name, identity=identity,
                                                                    ttls_passwd=ttls_passwd)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    @allure.title("VLAN Mode Client Connect Test for wpa3 enterprise 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4569", name="JIRA LINK")
    def test_vlan_wpa3_eap_2g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration, radius_info):
        """
            VLAN Mode Client Connect Test with wpa2_personal encryption 2.4 GHz Band
            pytest -m "client_connect_tests and vlan and enterprise and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connect(ssid=ssid_name, identity=identity,
                                                                    ttls_passwd=ttls_passwd)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    @allure.title("VLAN Mode Client Connect Test for wpa3 enterprise 5 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4570", name="JIRA LINK")
    def test_vlan_wpa3_eap_5g_client_connect(self, get_test_device_logs, get_dut_logs_per_test_case,
                                                    num_stations, setup_configuration, get_test_library, radius_info):
        """
            VLAN Mode Client Connect Test with wpa2_personal encryption 5 GHz Band
            pytest -m "client_connect_tests and vlan and enterprise and wpa2_personal and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connect(ssid=ssid_name, identity=identity,
                                                                    ttls_passwd=ttls_passwd)
        assert passes == "PASS", result


setup_params_enterprise_two_vlan = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa_wpa2_enterprise_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa_wpa2_eap_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa3_enterprise_mixed": [
            {"ssid_name": "ssid_wpa3_mixed_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa3_mixed_eap_5g", "appliedRadios": ["5G"], "vlan": 100}]
    },
    "rf": {},
    "radius": True
}
for sec_modes in setup_params_enterprise_two_vlan['ssid_modes'].keys():
    for i in range(len(setup_params_enterprise_two_vlan['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                              string.digits, k=N))) + str(int(time.time_ns()) % 10000)
        setup_params_enterprise_two_vlan['ssid_modes'][sec_modes][i]['ssid_name'] = \
            setup_params_enterprise_two_vlan['ssid_modes'][sec_modes][i]['ssid_name'] + "_" + rand_string


@allure.feature("VLAN MODE CLIENT CONNECT")
@allure.parent_suite("Client Connect Tests")
@allure.suite(suite_name="VLAN Mode")
@allure.sub_suite(sub_suite_name="Enterprise security mode Client Connect")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_enterprise_two_vlan],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestVlanModeConnectSuiteTwo(object):
    """ Client Connect SuiteA
        pytest -m "client_connect_tests and vlan and suiteB"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7410", name="JIRA LINK")
    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.twog
    @allure.story('wpa3_personal 2.4 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with wpa3_personal encryption 2.4 GHz Band")
    def test_vlan_wpa_wpa2_eap_mixed_2g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration, radius_info):
        """
            VLAN Mode Client Connect Test with wpa3_personal encryption 2.4 GHz Band
            pytest -m "client_connect_tests and vlan and enterprise and wpa3_personal and twog"
        """
        profile_data = {"ssid_name": "wpa_wpa2_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connect(ssid=ssid_name, identity=identity,
                                                                    ttls_passwd=ttls_passwd)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.fiveg
    @allure.story('wpa3_personal 5 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with wpa3_personal encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4572", name="JIRA LINK")
    def test_vlan_wpa_wpa2_eap_mixed_5g_client_connect(self, get_test_library, get_dut_logs_per_test_case,
                                                         get_test_device_logs, num_stations, setup_configuration, radius_info):
        """
            VLAN Mode Client Connect Test with wpa3_personal encryption 5 GHz Band
            pytest -m "client_connect_tests and vlan and enterprise and wpa3_personal and fiveg"
        """
        profile_data = {"ssid_name": "wpa_wpa2_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "fiveg"
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connect(ssid=ssid_name, identity=identity,
                                                                    ttls_passwd=ttls_passwd)

        assert passes == "PASS", result


    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.twog
    @allure.story('wpa3_personal_mixed 2.4 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with wpa3_personal_mixed encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4573", name="JIRA LINK")
    def test_vlan_wpa3_eap_mixed_2g_client_connect(self, get_test_library,
                                                               get_dut_logs_per_test_case, get_test_device_logs,
                                                               num_stations, setup_configuration, radius_info):
        """
            VLAN Mode Client Connect Test with wpa3_personal_mixed encryption 2.4 GHz Band
            pytest -m "client_connect_tests and vlan and enterprise and wpa3_personal_mixed and twog"
        """
        profile_data = {"ssid_name": "wpa3_m_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "twog"
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connect(ssid=ssid_name, identity=identity,
                                                                    ttls_passwd=ttls_passwd)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.fiveg
    @allure.story('wpa3_personal_mixed 5 GHZ Band')
    @allure.title("VLAN Mode Client Connect Test with wpa3_personal_mixed encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4574", name="JIRA LINK")
    def test_vlan_wpa3_eap_mixed_5g_client_connect(self, get_test_library,
                                                               get_dut_logs_per_test_case, get_test_device_logs,
                                                               num_stations, setup_configuration, radius_info):
        """
            VLAN Mode Client Connect Test with wpa3_personal_mixed encryption 5 GHz Band
            pytest -m "client_connect_tests and vlan and enterprise and wpa3_personal_mixed and fiveg"
        """
        profile_data = {"ssid_name": "wpa3_m_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "fiveg"
        ttls_passwd = radius_info["password"]
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connect(ssid=ssid_name, identity=identity,
                                                                    ttls_passwd=ttls_passwd)

        assert passes == "PASS", result

