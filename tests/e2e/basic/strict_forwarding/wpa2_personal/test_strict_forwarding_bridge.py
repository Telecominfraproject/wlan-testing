"""
    Test Strict Forwarding: Bridge Mode
    pytest -m strict_forwarding_tests
"""

import allure
import pytest

pytestmark = [pytest.mark.ow_regression_lf, pytest.mark.strict_forwarding_tests, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
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
@allure.parent_suite("Strict Forwarding Tests")
@allure.suite(suite_name="Bridge Mode")
@allure.sub_suite(sub_suite_name="Clients connected to same SSID")
@pytest.mark.usefixtures("setup_configuration")
class TestStrictForwardingSameSSID(object):
    """
        Strict Forwarding Test: BRIDGE Mode
        pytest -m "strict_forwarding_tests and bridge"
    """

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.clients_connected_same_ssid_sf_enabled
    @allure.title("Verify the clients connected to same SSID cannot ping each other when strict_forwarding is enabled")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12923", name="WIFI-12923")
    def test_sf_enabled_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        """
        The Strict Forwarding feature is designed to enhance network security by isolating individual wireless devices
        (clients) from each other. When enabled on a specific SSID, it prevents wireless clients from communicating
        directly with each other, even if they are connected to the same access point or different access points.

        With Strict Forwarding enabled, all peer-to-peer communication between wireless clients within the network
        is disabled. The only traffic allowed is from clients to the gateway or configured servers. Any other traffic
        not destined for the gateway or configured servers will not be forwarded by the Instant AP.

        This testcase evaluates Strict Forwarding feature in Bridge Mode scenario where 2 clients are connected to the
        same SSID where strict forwarding is enabled. The clients shouldn't be able to ping each other in such case.

        Unique Marker:
        strict_forwarding_tests and bridge and wpa2_personal and fiveg and clients_connected_same_ssid_sf_enabled
        """

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
        mode = "BRIDGE"
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
    "mode": "BRIDGE",
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
@allure.parent_suite("Strict Forwarding Tests")
@allure.suite(suite_name="Bridge Mode")
@allure.sub_suite(sub_suite_name="Clients connected to two different SSID (sf is enabled on both SSIDs)")
@pytest.mark.usefixtures("setup_configuration")
class TestStrictForwardingEnabledTwoSSID(object):
    """
        Strict Forwarding Test: BRIDGE Mode
        pytest -m "strict_forwarding_tests and bridge"
    """

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.clients_connected_different_ssid_sf_enabled
    @allure.title("Verify whether clients connected to different SSIDs cannot ping each other when strict_forwarding"
                  " is enabled on both SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12924", name="WIFI-12924")
    def test_sf_enabled_two_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                    get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        """
        The Strict Forwarding feature is designed to enhance network security by isolating individual wireless devices
        (clients) from each other. When enabled on a specific SSID, it prevents wireless clients from communicating
        directly with each other, even if they are connected to the same access point or different access points.

        With Strict Forwarding enabled, all peer-to-peer communication between wireless clients within the network
        is disabled. The only traffic allowed is from clients to the gateway or configured servers. Any other traffic
        not destined for the gateway or configured servers will not be forwarded by the Instant AP.

        This testcase evaluates Strict Forwarding feature in Bridge Mode scenario where 2 clients are connected to the
        different SSIDs where strict forwarding is enabled on both the SSIDs. The clients shouldn't be able to ping
        each other in such case.

        Unique Marker:
        strict_forwarding_tests and bridge and wpa2_personal and fiveg and clients_connected_different_ssid_sf_enabled
        """

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
        mode = "BRIDGE"
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
    "mode": "BRIDGE",
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
@allure.parent_suite("Strict Forwarding Tests")
@allure.suite(suite_name="Bridge Mode")
@allure.sub_suite(sub_suite_name="Clients connected to two different SSID (SSID with sf enabled and another "
                                 "SSID where sf is disabled")
@pytest.mark.usefixtures("setup_configuration")
class TestStrictForwardingEnabledSSIDDisableSSID(object):
    """
        Strict Forwarding Test: BRIDGE Mode
        pytest -m "strict_forwarding_tests and bridge"
    """

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.clients_connected_ssid_sf_enabled_ssid_sf_disable
    @allure.title("Verify that clients connected to an SSID with strict_forwarding enabled cannot ping clients "
                  "connected to another SSID where strict_forwarding is disabled")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12925", name="WIFI-12925")
    def test_sf_enabled_two_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                    get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        """
        The Strict Forwarding feature is designed to enhance network security by isolating individual wireless devices
        (clients) from each other. When enabled on a specific SSID, it prevents wireless clients from communicating
        directly with each other, even if they are connected to the same access point or different access points.

        With Strict Forwarding enabled, all peer-to-peer communication between wireless clients within the network
        is disabled. The only traffic allowed is from clients to the gateway or configured servers. Any other traffic
        not destined for the gateway or configured servers will not be forwarded by the Instant AP.

        This testcase evaluates Strict Forwarding feature in Bridge Mode scenario where 2 clients are connected to the
        different SSIDs where strict forwarding is enabled on one and disabled on another. The clients shouldn't be
        able to ping each other in such case.

        Unique Marker:
        strict_forwarding_tests and bridge and wpa2_personal and fiveg and
        clients_connected_ssid_sf_enabled_ssid_sf_disable
        """

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
        mode = "BRIDGE"
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
