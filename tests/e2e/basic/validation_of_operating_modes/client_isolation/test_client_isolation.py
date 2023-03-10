"""
    Test Client Isolation: Bridge Mode
    pytest -m client_isolation
"""

import allure
import pytest

pytestmark = [pytest.mark.ow_regression_lf, pytest.mark.client_isolation, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {
                "ssid_name": "ci_enabled_wpa2_ssid1_2g",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            },
            {
                "ssid_name": "ci_enabled_wpa2_ssid2_2g",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            },
            {
                "ssid_name": "ci_enabled_wpa2_ssid1_5g",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            },
            {
                "ssid_name": "ci_enabled_wpa2_ssid2_5g",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
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
@allure.feature("BRIDGE MODE CLIENT ISOLATION")
@allure.parent_suite("CLIENT ISOLATION")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="Test Client Isolation Enabled SSIDs")
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.ci_enabled
class TestClientIsolationEnabled(object):
    """
        Test Config with Enabling Client Isolation in SSIDs
        pytest -m "client_isolation and ci_enabled and bridge"
    """
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.ci_enabled_in_5g_ssid
    @allure.title("Verify the connectivity of 2 clients connected to the different SSID by enabling the client "
                                                "isolation in both the SSID's.(5Ghz)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10610", name="WIFI-10610")
    def test_client_isolation_enabled_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid1_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid2_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=None,
                                                                band_5g=band,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456,side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.ci_enabled_in_2g_ssid
    @allure.title("Run traffic between eth2 port (AP) and station (with client isolation enabled) -2.4GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10620", name="WIFI-10620")
    def test_client_isolation_enabled_with_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid1_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"

        result, description = get_test_library.client_isolation(ssid1=ssid_name, ssid2=None,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=band,
                                                                band_5g=None,
                                                                dut_data=setup_configuration, num_sta=1,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description


    # clients_connected to different ssid, enabling isolation in both(2.4GH)
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.ci_ebabled_in_2g
    @allure.title("Verify the connectivity of 2 clients connected to the different SSID by enabling the client "
                  "isolation in both the SSID's.(2.4Ghz)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10602",name="WIFI-10602")
    def test_client_isolation_enabled_ssids_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid1_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid2_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"

        result, description = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=band,
                                                                band_5g=None,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description


    # Running traffic between eth2 to station with client-isolation enabled in (5GH) ssid
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.eth_to_5g_station_true
    @allure.title("Run traffic between eth2 port (AP) and station (with client isolation enabled) -5GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10621", name="WIFI-10621")
    def test_client_isolation_enabled_with_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid1_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band ="fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name, ssid2=None,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=None,
                                                                band_5g=band,
                                                                dut_data=setup_configuration, num_sta=1,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description


setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {
                "ssid_name": "ci_disabled_wpa2_ssid1_2g",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            },
            {
                "ssid_name": "ci_disabled_wpa2_ssid2_2g",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            },
            {
                "ssid_name": "ci_disabled_wpa2_ssid1_5g",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            },
            {
                "ssid_name": "ci_disabled_wpa2_ssid2_5g",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
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
@allure.feature("BRIDGE MODE CLIENT ISOLATION")
@allure.parent_suite("CLIENT ISOLATION")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="Test Client Isolation Disabled SSIDs")
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.ci_disabled
class TestClientIsolationDisabled(object):
    """
        Test Config with Enabling Client Isolation in SSIDs
        pytest -m "client_isolation and ci_disabled and bridge"
    """
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.ci_disabled_in_2g_ssid
    @allure.title("Verify the connectivity of 2 clients connected to the different SSID disabling the client "
                  "isolation(2.4Ghz)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10603", name="WIFI-10603")
    def test_client_isolation_disabled_ssids_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid1_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid2_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"

        result, description = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=band,
                                                                band_5g=None,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.eth_to_2g_station_false
    @allure.title("Run traffic between eth2 port (AP) and station (with client isolation disabled) -2.4GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10624", name="WIFI-10624")
    def test_client_isolation_disabled_with_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid1_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"

        result, description = get_test_library.client_isolation(ssid1=ssid_name, ssid2=None,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=band,
                                                                band_5g=None,
                                                                dut_data=setup_configuration, num_sta=1,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description

    # clients_connected to different ssid, disabling isolation in both(5GH)
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.ci_disabled_in_5g_ssid
    @allure.title("Verify the connectivity of 2 clients connected to the different SSID disabling the client "
                  "isolation(5Ghz)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10611",name="WIFI-10611")
    def test_client_isolation_disabled_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid1_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid2_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=None,
                                                                band_5g=band,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description

    # Running traffic between eth2 to station with client-isolation disabled in (5GH) ssid
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.eth_to_5g_station_false
    @allure.title("Run traffic between eth2 port (AP) and station (with client isolation disabled) -5GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10623", name="WIFI-10623")
    def test_client_isolation_disabled_with_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid1_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name, ssid2=None,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=None,
                                                                band_5g=band,
                                                                dut_data=setup_configuration, num_sta=1,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description


setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {
                "ssid_name": "ci_enabled_wpa2_ssid",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            },
            {
                "ssid_name": "ci_disabled_wpa2_ssid",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            },
            {
                "ssid_name": "ci_enabled_wpa2_ssid",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            },
            {
                "ssid_name": "ci_disabled_wpa2_ssid",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            },
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
@allure.feature("BRIDGE MODE CLIENT ISOLATION")
@allure.parent_suite("CLIENT ISOLATION")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="Test Client Isolation Same SSIDs")
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.ci_same_ssid
class TestClientIsolationSameSSID(object):
    """
        Test Config with Enabling Client Isolation in SSIDs
        pytest -m "client_isolation and ci_same_ssid and bridge"
    """
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.same_ssid_enabling_isolation_2g
    @allure.title("Verify the connectivity of 2 clients connected to the same SSID enabling the client "
                  "isolation.(2.4Ghz)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10601", name="WIFI-10601")
    def test_cleint_isolation_enabled_same_ssid_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"

        result, description = get_test_library.client_isolation(ssid1=ssid_name, ssid2=ssid_name,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=band,
                                                                band_5g=None,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description

    # clients_connected to same ssid, disabled isolation(2.4GH)
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.same_ssid_disabling_isolation_2g
    @allure.title("Verify the connectivity of 2 clients connected to the same SSID without enabling the client "
                  "isolation.(2.4Ghz)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10604",name="WIFI-10604")
    def test_cleint_isolation_disabled_same_ssid_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"

        result, description = get_test_library.client_isolation(ssid1=ssid_name, ssid2=ssid_name,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=band,
                                                                band_5g=None,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description

    # clients_connected to same ssid, enabled isolation(5GHZ)
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.same_ssid_enabling_isolation_5g
    @allure.title("Verify the connectivity of 2 clients connected to the same SSID by enabling client isolation.(5Ghz)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10606", name="WIFI-10606")
    def test_cleint_isolation_enabled_same_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name, ssid2=ssid_name,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=None,
                                                                band_5g=band,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.same_ssid_disabling_isolation_5g
    @allure.title("Verify the connectivity of 2 clients connected to the same SSID disabling the client isolation.(5Ghz)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10612", name="WIFI-10612")
    def test_cleint_isolation_disabled_same_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name, ssid2=ssid_name,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=None,
                                                                band_5g=band,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description


setup_params_general3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {
                "ssid_name": "ci_enabled_wpa2_ssid_2g",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            },
            {
                "ssid_name": "ci_disabled_wpa2_ssid_2g",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            },
            {
                "ssid_name": "ci_enabled_wpa2_ssid_5g",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            },
            {
                "ssid_name": "ci_disabled_wpa2_ssid_5g",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            }
        ]
    },
    "rf": {},
    "radius": False
}
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general3],
    indirect=True,
    scope="class"
)
@allure.feature("BRIDGE MODE CLIENT ISOLATION")
@allure.parent_suite("CLIENT ISOLATION")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="Test Client Isolation Enable and Disabled with Different SSIDs")
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.ci_different_ssid
class TestClientIsolationDifferentSSID(object):
    """
        Test Config with Enabling Client Isolation in SSIDs
        pytest -m "client_isolation and ci_different_ssid and bridge"
    """

    # clients_connected to different ssid,enabling isolation in ssid (2GH)& isolation disabled in ssid (2GHZ)
    @pytest.mark.wpa2_personal
    @pytest.mark.ci
    @pytest.mark.twog
    @pytest.mark.ci_enable_and_disable_2g
    @allure.title("Verify the connectivity of 2 clients connected to different SSID's where Client isolation is enabled"
                  " in one and disabled in other.(2.4Ghz)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10605", name="WIFI-10605")
    def test_client_isoaltion_enabled_ssid_2g_disabled_ssid_2g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"

        result, description = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=band,
                                                                band_5g=None,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description


    # clients_connected to different ssid,enabling isolation in ssid (5GH)& isolation disabled in ssid (5GHZ)
    @pytest.mark.wpa2_personal
    @pytest.mark.ci
    @pytest.mark.fiveg
    @pytest.mark.ci_enable_and_disable_5g
    @allure.title("Verify the connectivity of 2 clients connected to different SSID's where Client isolation is enabled"
                  " in one and disabled in other.(5Ghz)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10613", name="WIFI-10613")
    def test_client_isoaltion_enabled_ssid_5g_disabled_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=None,
                                                                band_5g=band,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description

    # run traffic from 2g to 5g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_enabled_2g_and_5g_traffic_2g_to_5g
    @allure.title("Verify the connectivity of 2 clients connected to different SSID's where Client isolation is enabled"
                  " in 2G SSID and 5G SSID (run traffic from 2G client to 5G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10616", name="WIFI-10616")
    def test_client_isolation_enabled_ssid2g_and_ssid5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band_2g = "twog"
        band_5g = "fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2, passkey=security_key,
                                                                security=security, mode=mode, band_2g=band_2g, band_5g=band_5g,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=0, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description

    # run traffic from 2g to 5g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_disable_2g_and_5g_traffic_2g_to_5g
    @allure.title("Verify the connectivity of 2 clients connected to different SSID's where Client isolation is disabled"
                  " in 2G SSID and 5G SSID (run traffic from 2G client to 5G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10618",name="WIFI-10618")
    def test_client_isolation_disabled_ssid2g_and_ssid5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band_2g = "twog"
        band_5g = "fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=band_2g,
                                                                band_5g=band_5g,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=0, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description

    # clients_connected to different ssid, enabling isolation in both (2GHz) & (5GHz) ssid
    # run traffic from 5g to 2g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_enabled_2g_and_5g_traffic_5g_to_2g
    @allure.title("Verify the connectivity of 2 clients connected to different SSID's where Client isolation is enabled"
                  " in 2G SSID and 5G SSID (run traffic from 5G client to 2G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10617", name="WIFI-10617")
    def test_client_isolation_enabled_ssid_2gandssid_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band_2g = "twog"
        band_5g = "fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=band_2g,
                                                                band_5g=band_5g,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=0, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0, sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description

    # clients_connected to different ssid, disabled isolation in both (2GHz) & (5GHz) ssid
    # run traffic from 5g to 2g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_disable_2g_and_5g_traffic_5g_to_2g
    @allure.title("Verify the connectivity of 2 clients connected to different SSID's where Client isolation is disabled"
                  " in 2G SSID and 5G SSID (run traffic from 5G client to 2G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10619",name="WIFI-10619")
    def test_client_isolation_disabled_ssid_2gandssid_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band_2g = "twog"
        band_5g = "fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=band_2g,
                                                                band_5g=band_5g,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=0, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description

    # run traffic from 2g to 5g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_enabled_2g_disabled_5g_traffic_2g_to_5g
    @allure.title("Verify the connectivity of 2 clients connected to different SSID's where Client isolation is enabled"
                  " in 2G SSID and disabled in 5G SSID (run traffic from 2G client to 5G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10614", name="WIFI-10614")
    def test_client_isolation_enabled_ssids_2gdisabled_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data ={"ssid_name": "ci_disabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band_2g = "twog"
        band_5g = "fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=band_2g,
                                                                band_5g=band_5g,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=0, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description

    # run traffic from 5g to 2g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_disabled_2g_enabled_5g_traffic_5g_to_2g
    @allure.title("Verify the connectivity of 2 clients connected to different SSID's where Client isolation is disabled"
                  " in 2G SSID and enabled in 5G SSID (run traffic from 5G client to 2G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10625", name="WIFI-10625")
    def test_client_isolation_disabled_ssid_2genabled_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band_2g = "twog"
        band_5g = "fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=band_2g,
                                                                band_5g=band_5g,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=0, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description


    # clients_connected to different ssid,enabled isolation in (2GHz)ssid & isolation disabled in (5GH)ssid
    # run traffic from 5g to 2g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_enabled_2g_disabled_5g_traffic_5g_to_2g
    @allure.title("Verify the connectivity of 2 clients connected to different SSID's where Client isolation is enabled"
                  " in 2G SSID and disabled in 5G SSID (run traffic from 5G client to 2G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10615",name="WIFI-10615")
    def test_client_isolation_enabled_ssids_2g_disabled_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band_2g = "twog"
        band_5g = "fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                               passkey=security_key,
                                                               security=security, mode=mode, band_2g=band_2g,
                                                               band_5g=band_5g,
                                                               dut_data=setup_configuration, num_sta=2,
                                                               side_a_min_rate=0, side_a_max_rate=0,
                                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                                               sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description

    # clients_connected to different ssid,disabled isolation in ssid (2GHz)& isolation enabled in ssid(5GH)
    # run traffic from 2g to 5g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_disabled_2g_enabled_5g_traffic_2g_to_5g
    @allure.title("Verify the connectivity of 2 clients connected to different SSID's where Client isolation is disabled"
                  " in 2G SSID and enabled in 5G SSID (run traffic from 2G client to 5G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10626", name="WIFI-10626")
    def test_client_isolation_disabled_ssid_2g_enabled_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                            get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band_2g = "twog"
        band_5g = "fiveg"

        result, description = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=band_2g,
                                                                band_5g=band_5g,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=0, side_b_max_rate=0,
                                                                sniff_radio=True)
        if not result:
            assert False, description
        else:
            assert True, description
