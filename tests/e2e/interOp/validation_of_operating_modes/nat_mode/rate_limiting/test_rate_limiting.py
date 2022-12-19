"""
    Rate Limiting : NAT Mode
    pytest -m "rate_limiting_tests and nat and general"

"""
import logging
import random
import string
import time

import allure
import pytest

pytestmark = [pytest.mark.nat, pytest.mark.general]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g_RL",
             "appliedRadios": ["2G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 60,
                 "egress-rate": 10
             }
             },
            {"ssid_name": "ssid_wpa2_5g_RL",
             "appliedRadios": ["5G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 60,
                 "egress-rate": 10
             }
             }
        ],
        "wpa": [
            {"ssid_name": "ssid_wpa_2g_RL",
             "appliedRadios": ["2G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 60,
                 "egress-rate": 10
             }
             },
            {"ssid_name": "ssid_wpa_5g_RL",
             "appliedRadios": ["5G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 60,
                 "egress-rate": 10
             }
             }
        ],
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_2g_RL",
             "appliedRadios": ["2G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 60,
                 "egress-rate": 10
             }
             },
            {"ssid_name": "ssid_wpa3_5g_RL",
             "appliedRadios": ["5G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 60,
                 "egress-rate": 10
             }
             }
        ]
    },
    "rf": {},
    "radius": False
}
for sec_modes in setup_params_general['ssid_modes'].keys():
    for i in range(len(setup_params_general['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string
@allure.feature("NAT MODE RATE LIMITING")
@allure.parent_suite("Rate Limiting Tests")
@allure.suite(suite_name="NAT Mode")
@allure.sub_suite(sub_suite_name="General security mode Rate Limiting")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestRateLimitingNat(object):
    """
        NAT MODE Rate Limiting (wpa. wpa2. wpa3) (twog, fiveg)
        pytest -m "rate_limiting_tests and nat and general"
    """

    @pytest.mark.wpa
    @pytest.mark.twog
    @allure.story('wpa 2.4 GHZ Band')
    @allure.title("NAT Mode Rate Limiting Test with wpa encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7012", name="JIRA LINK")
    def test_rate_limiting_wpa_2g(self, get_dut_logs_per_test_case, get_test_device_logs,
                                          num_stations, setup_configuration, get_test_library):
        """
            NAT Mode Rate Limiting Test with wpa encryption 2.4 GHz Band
            pytest -m "rate_limiting_tests and nat and general and wpa and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        up_rate = profile_data["rate-limit"]["ingress-rate"]
        down_rate = profile_data["rate-limit"]["egress-rate"]
        security = "wpa"
        mode = "NAT"
        band = "twog"

        passes, result = get_test_library.rate_limiting_test(ssid_name=ssid_name, passkey=security_key, up_rate=up_rate,
                                                             down_rate=down_rate)
        assert passes == "PASS", result

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @allure.story('wpa 5 GHZ Band')
    @allure.title("NAT Mode Rate Limiting Test with wpa encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7013",name="JIRA LINK")
    def test_rate_limiting_wpa_5g(self, get_dut_logs_per_test_case, get_test_device_logs,
                                          num_stations, setup_configuration, get_test_library):
        """
           NAT Mode Rate Limiting Test with wpa encryption 5 GHz Band
           pytest -m "rate_limiting_tests and nat and general and wpa and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        up_rate = profile_data["rate-limit"]["ingress-rate"]
        down_rate = profile_data["rate-limit"]["egress-rate"]
        security = "wpa"
        mode = "NAT"
        band = "fiveg"

        passes, result = get_test_library.rate_limiting_test(ssid_name=ssid_name, passkey=security_key, up_rate=up_rate,
                                                             down_rate=down_rate)
        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.ow_sanity_interop
    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.title("NAT Mode Rate Limiting Test with wpa2_personal encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7012", name="JIRA LINK")
    def test_rate_limiting_wpa2_2g(self, get_dut_logs_per_test_case, get_test_device_logs,
                                          num_stations, setup_configuration, get_test_library):
        """
            NAT Mode Rate Limiting Test with wpa2_personal encryption 2.4 GHz Band
            pytest -m "rate_limiting_tests and nat and general and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        up_rate = profile_data["rate-limit"]["ingress-rate"]
        down_rate = profile_data["rate-limit"]["egress-rate"]
        security = "wpa2"
        mode = "NAT"
        band = "twog"

        passes, result = get_test_library.rate_limiting_test(ssid_name=ssid_name, passkey=security_key, up_rate=up_rate,
                                                             down_rate=down_rate)
        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.ow_sanity_interop
    @allure.story('wpa2_personal 5 GHZ Band')
    @allure.title("NAT Mode Rate Limiting Test with wpa2_personal encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7013", name="JIRA LINK")
    def test_rate_limiting_wpa2_5g(self, get_dut_logs_per_test_case, get_test_device_logs,
                                          num_stations, setup_configuration, get_test_library):
        """
           NAT Mode Rate Limiting Test with wpa2_personal encryption 5 GHz Band
           pytest -m "rate_limiting_tests and nat and general and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        up_rate = profile_data["rate-limit"]["ingress-rate"]
        down_rate = profile_data["rate-limit"]["egress-rate"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"

        passes, result = get_test_library.rate_limiting_test(ssid_name=ssid_name, passkey=security_key, up_rate=up_rate,
                                                             down_rate=down_rate)
        assert passes == "PASS", result

    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @allure.story('wpa3_personal 2.4 GHZ Band')
    @allure.title("NAT Mode Rate Limiting Test with wpa3_personal encryption 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7012", name="JIRA LINK")
    def test_rate_limiting_wpa3_2g(self, get_dut_logs_per_test_case, get_test_device_logs,
                                          num_stations, setup_configuration, get_test_library):
        """
            NAT Mode Rate Limiting Test with wpa3_personal encryption 2.4 GHz Band
            pytest -m "rate_limiting_tests and nat and general and wpa3_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        up_rate = profile_data["rate-limit"]["ingress-rate"]
        down_rate = profile_data["rate-limit"]["egress-rate"]
        security = "wpa3"
        mode = "NAT"
        band = "twog"

        passes, result = get_test_library.rate_limiting_test(ssid_name=ssid_name, passkey=security_key, up_rate=up_rate,
                                                             down_rate=down_rate)
        assert passes == "PASS", result

    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @allure.story('wpa3_personal 5 GHZ Band')
    @allure.title("NAT Mode Rate Limiting Test with wpa3_personal encryption 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7013", name="JIRA LINK")
    def test_rate_limiting_wpa3_5g(self, get_dut_logs_per_test_case, get_test_device_logs,
                                          num_stations, setup_configuration, get_test_library):
        """
           NAT Mode Rate Limiting Test with wpa3_personal encryption 5 GHz Band
           pytest -m "rate_limiting_tests and nat and general and wpa3_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        up_rate = profile_data["rate-limit"]["ingress-rate"]
        down_rate = profile_data["rate-limit"]["egress-rate"]
        security = "wpa3"
        mode = "NAT"
        band = "fiveg"

        passes, result = get_test_library.rate_limiting_test(ssid_name=ssid_name, passkey=security_key, up_rate=up_rate,
                                                             down_rate=down_rate)
        assert passes == "PASS", result


