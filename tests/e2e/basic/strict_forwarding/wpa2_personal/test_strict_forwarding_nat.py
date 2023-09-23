"""
    Test Strict Forwarding: NAT Mode
    pytest -m strict_forwarding_tests
"""

import allure
import pytest

pytestmark = [pytest.mark.ow_regression_lf, pytest.mark.strict_forwarding_tests, pytest.mark.nat]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {
                "ssid_name": "strict_forwarding_wpa2_br",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "something",
                "strict-forwarding": True
            }
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
@allure.feature("Strict Forwarding")
@allure.parent_suite("Strict Forwarding")
@allure.suite(suite_name="NAT Mode")
@allure.sub_suite(sub_suite_name="Clients connected to same SSID")
@pytest.mark.usefixtures("setup_configuration")
class TestStrictForwardingSameSSID(object):
    """
        Strict Forwarding Test: NAT Mode
        pytest -m "strict_forwarding_tests and nat"
    """

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.clients_connected_same_ssid_sf_enabled
    @allure.title("Verify the clients connected to same SSID cannot ping eachother when strict_forwarding is enabled")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12926", name="WIFI-12926")
    def test_sf_enabled_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {
            "ssid_name": "strict_forwarding_wpa2_br",
            "appliedRadios": ["5G"],
            "security": "psk2",
            "security_key": "something",
            "strict-forwarding": True
        }
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "fiveg"

        result, description = get_test_library.strict_forwarding(ssids=[ssid_name],
                                                                 passkey=security_key,
                                                                 security=security, mode=mode,
                                                                 dut_data=setup_configuration, num_stations_per_ssid=2,
                                                                 side_a_min_rate=6291456, side_a_max_rate=0,
                                                                 side_b_min_rate=6291456, side_b_max_rate=0, band=band)
        if not result:
            assert False, description
        else:
            assert True, description


setup_params_general1 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {
                "ssid_name": "sf_enabled_ssid1_wpa2_br",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "something",
                "strict-forwarding": True
            },
            {
                "ssid_name": "sf_enabled_ssid2_wpa2_br",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "something",
                "strict-forwarding": True
            }
        ]
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@allure.feature("Strict Forwarding")
@allure.parent_suite("Strict Forwarding")
@allure.suite(suite_name="NAT Mode")
@allure.sub_suite(sub_suite_name="Clients connected to two different SSID (sf is enabled on both SSIDs)")
@pytest.mark.usefixtures("setup_configuration")
class TestStrictForwardingEnabledTwoSSID(object):
    """
        Strict Forwarding Test: NAT Mode
        pytest -m "strict_forwarding_tests and nat"
    """

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.clients_connected_different_ssid_sf_enabled
    @allure.title("Verify whether clients connected to different SSIDs cannot ping each other when strict_forwarding"
                  " is enabled on both SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12927", name="WIFI-12927")
    def test_sf_enabled_two_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                    get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {
            "ssid_name": "sf_enabled_ssid1_wpa2_br",
            "appliedRadios": ["5G"],
            "security": "psk2",
            "security_key": "something",
            "strict-forwarding": True
        }
        ssid_name_1 = profile_data["ssid_name"]
        profile_data = {
            "ssid_name": "sf_enabled_ssid2_wpa2_br",
            "appliedRadios": ["5G"],
            "security": "psk2",
            "security_key": "something",
            "strict-forwarding": True
        }
        ssid_name_2 = profile_data["ssid_name"]
        ssids = [ssid_name_1, ssid_name_2]
        print("SSIDS", ssids)
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "fiveg"
        result, description = get_test_library.strict_forwarding(ssids=ssids,
                                                                 passkey=security_key,
                                                                 security=security, mode=mode,
                                                                 dut_data=setup_configuration, num_stations_per_ssid=1,
                                                                 side_a_min_rate=6291456, side_a_max_rate=0,
                                                                 side_b_min_rate=6291456, side_b_max_rate=0, band=band)
        if not result:
            assert False, description
        else:
            assert True, description


setup_params_general2 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {
                "ssid_name": "sf_enabled_ssid1_wpa2_br",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "something",
                "strict-forwarding": True
            },
            {
                "ssid_name": "sf_disabled_ssid2_wpa2_br",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "something",
                "strict-forwarding": False
            }
        ]
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@allure.feature("Strict Forwarding")
@allure.parent_suite("Strict Forwarding")
@allure.suite(suite_name="NAT Mode")
@allure.sub_suite(sub_suite_name="Clients connected to two different SSID (SSID with sf enabled and another "
                                 "SSID where sf is disabled")
@pytest.mark.usefixtures("setup_configuration")
class TestStrictForwardingEnabledSSIDDisableSSID(object):
    """
        Strict Forwarding Test: NAT Mode
        pytest -m "strict_forwarding_tests and nat"
    """

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.clients_connected_ssid_sf_enabled_ssid_sf_disable
    @allure.title("Verify that clients connected to an SSID with strict_forwarding enabled cannot ping clients "
                  "connected to another SSID where strict_forwarding is disabled")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12928", name="WIFI-12928")
    def test_sf_enabled_two_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                    get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {
                "ssid_name": "sf_enabled_ssid1_wpa2_br",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "something",
                "strict-forwarding": True
            }
        ssid_name_1 = profile_data["ssid_name"]
        profile_data = {
                "ssid_name": "sf_disabled_ssid2_wpa2_br",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "something",
                "strict-forwarding": False
            }
        ssid_name_2 = profile_data["ssid_name"]
        ssids = [ssid_name_1, ssid_name_2]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "fiveg"
        print("SSIDS", ssids)
        result, description = get_test_library.strict_forwarding(ssids=ssids,
                                                                 passkey=security_key,
                                                                 security=security, mode=mode,
                                                                 dut_data=setup_configuration, num_stations_per_ssid=1,
                                                                 side_a_min_rate=6291456, side_a_max_rate=0,
                                                                 side_b_min_rate=6291456, side_b_max_rate=0, band=band)
        if not result:
            assert False, description
        else:
            assert True, description
