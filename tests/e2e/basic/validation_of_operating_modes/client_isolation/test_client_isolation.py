"""
Testplan:
Client Isolation is feature that isolates clients only with in the same SSID, Thereby
adding level of security to the users connected to the same SSID. However, we are able
to ping the Stations from other SSID’s

Any user knowing the Password to the SSID can connect to network and gain the privileges
with in the network. If the user is a malicious user it is a threat to other users in
the same network. Client isolation feature isolates every client connected to the SSID
adding a level of security against attacks and threats to others users in the same SSID.

In this Test plan we have covered various scenarios and test working of the feature.

Mode: Bridge

Marker: pytest -m "wpa2_personal and bridge and client_isolation"
"""

import allure
import pytest

pytestmark = [pytest.mark.ow_regression_lf, pytest.mark.wpa2_personal, pytest.mark.client_isolation, pytest.mark.bridge]

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
@allure.feature("Bridge Mode Client Isolation")
@allure.parent_suite("Client Isolation")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Client Isolation-Enabled SSIDs")
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.ci_enabled
class TestClientIsolationEnabled(object):
    """
        Test Config with Enabling Client Isolation in SSIDs
        pytest -m "wpa2_personal and bridge and client_isolation and ci_enabled"
    """
    @pytest.mark.one_of_each
    @pytest.mark.fiveg
    @pytest.mark.ci_different_ssid
    @allure.title("2 Clients connected to different SSIDs, CI is Enabled on both 5G SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10610", name="WIFI-10610")
    def test_client_isolation_enabled_ssids_5g(self, setup_configuration, get_test_library, num_stations,
                                              get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the different SSIDs
        (with client isolation enabled on both) are not isolated when
        both the clients are on 5GHz band.

        Markers: client_isolation and wpa2_personal and bridge and ci_enabled and fiveg and ci_different_ssid
        """

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid1_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid2_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode,
                                                                band_5g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as the stations were "
                            "connected to different SSIDs.")
            assert True

    @pytest.mark.twog
    @pytest.mark.between_eth_client
    @allure.title("Traffic run between WAN port (AP) and station, CI is Enabled on 2G")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10620", name="WIFI-10620")
    def test_client_isolation_enabled_with_2g(self, setup_configuration, get_test_library, num_stations,
                                              get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the endpoints (a station and a wan port)
        (with client isolation enabled) are not isolated when
        the station is on 2.4GHz band.

        Markers: client_isolation and wpa2_personal and bridge and ci_enabled and twog and between_eth_client
        """

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid1_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name, ssid2=None,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=True,
                                                                dut_data=setup_configuration, num_sta=1,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It is expected that the traffic would run between the WAN port and any station.")
            assert True

    @pytest.mark.twog
    @pytest.mark.ci_different_ssid
    @allure.title("2 Clients connected to different SSIDs, CI is Enabled on both 2G SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10602", name="WIFI-10602")
    def test_client_isolation_enabled_ssids_2g(self, setup_configuration, get_test_library, num_stations,
                                               get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the different SSIDs
        (with client isolation enabled on both) are not isolated when
        both the clients are on 2.4GHz band.

        Markers: client_isolation and wpa2_personal and bridge and ci_enabled and twog and ci_different_ssid
        """

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid1_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid2_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as the stations were "
                            "connected to different SSIDs.")
            assert True

    @pytest.mark.fiveg
    @pytest.mark.between_eth_client
    @allure.title("Traffic run between WAN port (AP) and station, CI is Enabled on 5G")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10621", name="WIFI-10621")
    def test_client_isolation_enabled_with_5g(self, setup_configuration, get_test_library, num_stations,
                                              get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the endpoints (a station and a wan port)
        (with client isolation enabled) are not isolated when
        the station is on 5GHz band.

        Markers: client_isolation and wpa2_personal and bridge and ci_enabled and fiveg and between_eth_client
        """

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid1_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name, ssid2=None,
                                                                passkey=security_key,
                                                                security=security, mode=mode,
                                                                band_5g=True,
                                                                dut_data=setup_configuration, num_sta=1,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It is expected that the traffic would run between the WAN port and any station.")
            assert True


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
@allure.feature("Bridge Mode Client Isolation")
@allure.parent_suite("Client Isolation")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Client Isolation-Disabled SSIDs")
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.ci_disabled
class TestClientIsolationDisabled(object):
    """
        Test Config with Disabling Client Isolation in SSIDs
        pytest -m "wpa2_personal and bridge and client_isolation and ci_disabled"
    """
    @pytest.mark.twog
    @pytest.mark.ci_different_ssid
    @allure.title("2 Clients connected to different SSIDs, CI is Disabled on both 2G SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10603", name="WIFI-10603")
    def test_client_isolation_disabled_ssids_2g(self, setup_configuration, get_test_library, num_stations,
                                                get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the different SSIDs
        (with client isolation disabled on both) are not isolated when
        both the clients are on 2.4GHz band.

        Markers: client_isolation and wpa2_personal and bridge and ci_disabled and twog and ci_different_ssid
        """

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid1_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid2_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as the stations were "
                            "connected to different SSIDs.")
            assert True

    @pytest.mark.one_of_each
    @pytest.mark.twog
    @pytest.mark.between_eth_client
    @allure.title("Traffic run between WAN port (AP) and station, CI is Disabled on 2G")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10624", name="WIFI-10624")
    def test_client_isolation_disabled_with_2g(self, setup_configuration, get_test_library, num_stations,
                                               get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the endpoints (a station and a wan port)
        (with client isolation disabled) are not isolated when
        the station is on 2.4GHz band.

        Markers: client_isolation and wpa2_personal and bridge and ci_disabled and twog and between_eth_client
        """

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid1_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name, ssid2=None,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=True,
                                                                dut_data=setup_configuration, num_sta=1,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It is expected that the traffic would run between the WAN port and any station.")
            assert True

    @pytest.mark.fiveg
    @pytest.mark.ci_different_ssid
    @allure.title("2 Clients connected to different SSIDs, CI is Disabled on both 5G SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10611", name="WIFI-10611")
    def test_client_isolation_disabled_ssids_5g(self, setup_configuration, get_test_library, num_stations,
                                               get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the different SSIDs
        (with client isolation disabled on both) are not isolated when
        both the clients are on 5GHz band.

        Markers: client_isolation and wpa2_personal and bridge and ci_disabled and fiveg and ci_different_ssid
        """

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid1_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid2_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode,
                                                                band_5g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as the stations were "
                            "connected to different SSIDs.")
            assert True

    @pytest.mark.fiveg
    @pytest.mark.between_eth_client
    @allure.title("Traffic run between WAN port (AP) and station, CI is Disabled on 5G")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10623", name="WIFI-10623")
    def test_client_isolation_disabled_with_5g(self, setup_configuration, get_test_library, num_stations,
                                               get_test_device_logs, get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the endpoints (a station and a wan port)
        (with client isolation disabled) are not isolated when
        the station is on 5GHz band.

        Markers: client_isolation and wpa2_personal and bridge and ci_disabled and fiveg and between_eth_client
        """

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid1_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name, ssid2=None,
                                                                passkey=security_key,
                                                                security=security, mode=mode,
                                                                band_5g=True,
                                                                dut_data=setup_configuration, num_sta=1,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It is expected that the traffic would run between the WAN port and any station.")
            assert True


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
@allure.feature("Bridge Mode Client Isolation")
@allure.parent_suite("Client Isolation")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Client Isolation Same-SSID")
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.ci_same_ssid
class TestClientIsolationSameSSID(object):
    """
        Test Config with Enabling/Disabling Client Isolation on same SSID
        pytest -m "wpa2_personal and bridge and client_isolation and ci_same_ssid"
    """

    @pytest.mark.twog
    @pytest.mark.ci_enabled
    @allure.title("2 Clients connected to same SSID, CI is Enabled on 2G")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10601", name="WIFI-10601")
    def test_client_isolation_enabled_same_ssid_2g(self, setup_configuration, get_test_library, num_stations,
                                                   get_test_device_logs, get_dut_logs_per_test_case,
                                                   check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the same SSID
        (with client isolation enabled) are isolated when
        both the clients are on 2.4GHz band.

        Markers: client_isolation and wpa2_personal and bridge and ci_same_ssid and twog and ci_enabled
        """

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name, ssid2=ssid_name,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] != 100 or information["drop_b"] != 100:
                pytest.fail("It was expected that the traffic would not run between the endpoints as the stations were"
                            " connected to the same SSID and Client Isolation was enabled.")
            assert True

    @pytest.mark.twog
    @pytest.mark.ci_disabled
    @allure.title("2 Clients connected to same SSID, CI is Disabled on 2G")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10604", name="WIFI-10604")
    def test_client_isolation_disabled_same_ssid_2g(self, setup_configuration, get_test_library, num_stations,
                                                    get_test_device_logs, get_dut_logs_per_test_case,
                                                    check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the same SSID
        (with client isolation disabled) are not isolated when
        both the clients are on 2.4GHz band.

        Markers: client_isolation and wpa2_personal and bridge and ci_same_ssid and twog and ci_disabled
        """

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name, ssid2=ssid_name,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as Client Isolation"
                            " was Disabled.")
            assert True

    @pytest.mark.one_of_each
    @pytest.mark.fiveg
    @pytest.mark.ci_enabled
    @allure.title("2 Clients connected to same SSID, CI is Enabled on 5G")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10606", name="WIFI-10606")
    def test_client_isolation_enabled_same_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                                   get_test_device_logs, get_dut_logs_per_test_case,
                                                   check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the same SSID
        (with client isolation enabled) are isolated when
        both the clients are on 5GHz band.

        Markers: client_isolation and wpa2_personal and bridge and ci_same_ssid and fiveg and ci_enabled
        """

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name, ssid2=ssid_name,
                                                                passkey=security_key,
                                                                security=security, mode=mode,
                                                                band_5g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] != 100 or information["drop_b"] != 100:
                pytest.fail("It was expected that the traffic would not run between the endpoints as the stations were"
                            " connected to the same SSID and Client Isolation was enabled.")
            assert True

    @pytest.mark.fiveg
    @pytest.mark.ci_disabled
    @allure.title("2 Clients connected to same SSID, CI is Disabled on 5G")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10612", name="WIFI-10612")
    def test_client_isolation_disabled_same_ssid_5g(self, setup_configuration, get_test_library, num_stations,
                                                    get_test_device_logs, get_dut_logs_per_test_case,
                                                    check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the same SSID
        (with client isolation disabled) are not isolated when
        both the clients are on 5GHz band.

        Markers: client_isolation and wpa2_personal and bridge and ci_same_ssid and fiveg and ci_disabled
        """

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name, ssid2=ssid_name,
                                                                passkey=security_key,
                                                                security=security, mode=mode,
                                                                band_5g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as Client Isolation"
                            " was Disabled.")
            assert True


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
@allure.feature("Bridge Mode Client Isolation")
@allure.parent_suite("Client Isolation")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Client Isolation Enabled/Disabled on 2 Different SSIDs")
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.ci_different_ssid
class TestClientIsolationDifferentSSID(object):
    """
        Test Config with Enabling/Disabling Client Isolation in different SSIDs
        pytest -m "wpa2_personal and bridge and client_isolation and ci_different_ssid"
    """
    @pytest.mark.twog
    @pytest.mark.ci_enabled_and_disabled
    @pytest.mark.bi_directional
    @allure.title("CI is enabled on one 2G and disabled on other 2G ssid")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10605", name="WIFI-10605")
    def test_client_isolation_enabled_ssid_2g_disabled_ssid_2g(self, setup_configuration, get_test_library,
                                                               num_stations, get_test_device_logs,
                                                               get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the different SSIDs
        (with client isolation enabled on A and disabled on B) are not isolated when
        both the clients are on 2.4GHz band.

        Markers: client_isolation and wpa2_personal and bridge and ci_different_ssid and twog and
                 ci_enabled_and_disabled and bi_directional
        """

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as the stations were "
                            "connected to different SSIDs.")
            assert True

    @pytest.mark.fiveg
    @pytest.mark.ci_enabled_and_disabled
    @pytest.mark.bi_directional
    @allure.title("CI is enabled on one 5G and disabled on other 5G ssid")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10613", name="WIFI-10613")
    def test_client_isolation_enabled_ssid_5g_disabled_ssid_5g(self, setup_configuration, get_test_library,
                                                               num_stations, get_test_device_logs,
                                                               get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the different SSIDs
        (with client isolation enabled on A and disabled on B) are not isolated when
        both the clients are on 5GHz band.

        Markers: client_isolation and wpa2_personal and bridge and ci_different_ssid and fiveg and
                 ci_enabled_and_disabled and bi_directional
        """

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode,
                                                                band_5g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as the stations were "
                            "connected to different SSIDs.")
            assert True

    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_enabled_and_enabled
    @pytest.mark.from_2g_to_5g
    @allure.title("CI is enabled on both, 2G and 5G (run traffic from 2G client to 5G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10616", name="WIFI-10616")
    def test_client_isolation_enabled_ssid_2g_and_ssid_5g_a_to_b(self, setup_configuration, get_test_library,
                                                                num_stations, get_test_device_logs,
                                                                get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the different SSIDs
        (with client isolation enabled on both, 2.4GHz and 5GHz) are not isolated when
        traffic is run from 2.4GHz client to 5GHz client.

        Markers: client_isolation and wpa2_personal and bridge and ci_different_ssid and twog and fiveg and
                 ci_enabled_and_enabled and from_2g_to_5g
        """

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key, security=security,
                                                                mode=mode, band_2g=True, band_5g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=0, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as the stations were "
                            "connected to different SSIDs.")
            assert True

    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_disabled_and_disabled
    @pytest.mark.from_2g_to_5g
    @allure.title("CI is disabled on both, 2G and 5G (run traffic from 2G client to 5G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10618", name="WIFI-10618")
    def test_client_isolation_disabled_ssid2g_and_ssid_5g_a_to_b(self, setup_configuration, get_test_library,
                                                                 num_stations, get_test_device_logs,
                                                                 get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the different SSIDs
        (with client isolation disabled on both, 2.4GHz and 5GHz) are not isolated when
        traffic is run from 2.4GHz client to 5GHz client.

        Markers: client_isolation and wpa2_personal and bridge and ci_different_ssid and twog and fiveg and
                 ci_disabled_and_disabled and from_2g_to_5g
        """

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=True,
                                                                band_5g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=0, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as the stations were "
                            "connected to different SSIDs.")
            assert True

    @pytest.mark.one_of_each
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_enabled_and_enabled
    @pytest.mark.from_5g_to_2g
    @allure.title("CI is enabled on both, 2G and 5G (run traffic from 5G client to 2G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10617", name="WIFI-10617")
    def test_client_isolation_enabled_ssid_2g_and_ssid_5g_b_to_a(self, setup_configuration, get_test_library,
                                                                 num_stations, get_test_device_logs,
                                                                 get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the different SSIDs
        (with client isolation enabled on both, 2.4GHz and 5GHz) are not isolated when
        traffic is run from 5GHz client to 2.4GHz client.

        Markers: client_isolation and wpa2_personal and bridge and ci_different_ssid and twog and fiveg and
                 ci_enabled_and_enabled and from_5g_to_2g
        """

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=True,
                                                                band_5g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=0, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as the stations were "
                            "connected to different SSIDs.")
            assert True

    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_disabled_and_disabled
    @pytest.mark.from_5g_to_2g
    @allure.title("CI is disabled on both, 2G and 5G (run traffic from 5G client to 2G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10619", name="WIFI-10619")
    def test_client_isolation_disabled_ssid_2g_and_ssid_5g_b_to_a(self, setup_configuration, get_test_library,
                                                                  num_stations,get_test_device_logs,
                                                                  get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the different SSIDs
        (with client isolation disabled on both, 2.4GHz and 5GHz) are not isolated when
        traffic is run from 5GHz client to 2.4GHz client.

        Markers: client_isolation and wpa2_personal and bridge and ci_different_ssid and twog and fiveg and
                 ci_disabled_and_disabled and from_5g_to_2g
        """

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=True,
                                                                band_5g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=0, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as the stations were "
                            "connected to different SSIDs.")
            assert True

    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_enabled_and_disabled
    @pytest.mark.from_2g_to_5g
    @allure.title("CI is enabled on 2G and disabled on 5G (run traffic from 2G client to 5G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10614", name="WIFI-10614")
    def test_client_isolation_enabled_ssid_2g_disabled_ssid_5g_a_to_b(self, setup_configuration, get_test_library,
                                                                       num_stations, get_test_device_logs,
                                                                       get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the different SSIDs
        (with client isolation enabled on 2.4GHz and disabled on 5GHz) are not isolated when
        traffic is run from 2.4GHz client to 5GHz client.

        Markers: client_isolation and wpa2_personal and bridge and ci_different_ssid and twog and fiveg and
                 ci_enabled_and_disabled and from_2g_to_5g
        """
        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=True,
                                                                band_5g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=0, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as the stations were "
                            "connected to different SSIDs.")
            assert True

    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_disabled_and_enabled
    @pytest.mark.from_5g_to_2g
    @allure.title("CI is disabled on 2G and enabled on 5G (run traffic from 5G client to 2G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10625", name="WIFI-10625")
    def test_client_isolation_disabled_ssid_2g_enabled_ssid_5g_b_to_a(self, setup_configuration, get_test_library,
                                                                      num_stations, get_test_device_logs,
                                                                      get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the different SSIDs
        (with client isolation disabled on 2.4GHz and enabled on 5GHz) are not isolated when
        traffic is run from 5GHz client to 2.4GHz client.

        Markers: client_isolation and wpa2_personal and bridge and ci_different_ssid and twog and fiveg and
                 ci_disabled_and_enabled and from_5g_to_2g
        """

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=True,
                                                                band_5g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=0, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as the stations were "
                            "connected to different SSIDs.")
            assert True

    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_enabled_and_disabled
    @pytest.mark.from_5g_to_2g
    @allure.title("CI is enabled on 2G and disabled on 5G (run traffic from 5G client to 2G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10615", name="WIFI-10615")
    def test_client_isolation_enabled_ssid_2g_disabled_ssid_5g_b_to_a(self, setup_configuration, get_test_library,
                                                                       num_stations, get_test_device_logs,
                                                                       get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the different SSIDs
        (with client isolation enabled on 2.4GHz and disabled on 5GHz) are not isolated when
        traffic is run from 5GHz client to 2.4GHz client.

        Markers: client_isolation and wpa2_personal and bridge and ci_different_ssid and twog and fiveg and
                 ci_enabled_and_disabled and from_5g_to_2g
        """

        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key, security=security, mode=mode,
                                                                band_2g=True, band_5g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=0, side_a_max_rate=0,
                                                                side_b_min_rate=6291456, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as the stations were "
                            "connected to different SSIDs.")
            assert True

    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_disabled_and_enabled
    @pytest.mark.from_2g_to_5g
    @allure.title("CI is disabled on 2G and enabled on 5G (run traffic from 2G client to 5G client)")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10626", name="WIFI-10626")
    def test_client_isolation_disabled_ssid_2g_enabled_ssid_5g_a_to_b(self, setup_configuration, get_test_library,
                                                                      num_stations, get_test_device_logs,
                                                                      get_dut_logs_per_test_case, check_connectivity):
        """
        Description:
        Client Isolation is feature that isolates clients only within the same SSID,
        Thereby adding level of security to the users connected to the same SSID.
        However, we are able to ping the Stations from other SSIDs.

        This testcase is to verify that the clients connected to the different SSIDs
        (with client isolation disabled on 2.4GHz and enabled on 5GHz) are not isolated when
        traffic is run from 2.4GHz client to 5GHz client.

        Markers: client_isolation and wpa2_personal and bridge and ci_different_ssid and twog and fiveg and
                 ci_disabled_and_enabled and from_2g_to_5g
        """

        profile_data = {"ssid_name": "ci_disabled_wpa2_ssid_2g", "appliedRadios": ["2G"], "security_key": "OpenWifi"}
        ssid_name1 = profile_data["ssid_name"]
        profile_data = {"ssid_name": "ci_enabled_wpa2_ssid_5g", "appliedRadios": ["5G"], "security_key": "OpenWifi"}
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"

        result, information = get_test_library.client_isolation(ssid1=ssid_name1, ssid2=ssid_name2,
                                                                passkey=security_key,
                                                                security=security, mode=mode, band_2g=True,
                                                                band_5g=True,
                                                                dut_data=setup_configuration, num_sta=2,
                                                                side_a_min_rate=6291456, side_a_max_rate=0,
                                                                side_b_min_rate=0, side_b_max_rate=0)
        if result is False:
            pytest.fail(information)
        else:
            if information["drop_a"] == 100 or information["drop_b"] == 100:
                pytest.fail("It was expected that the traffic would run between the endpoints as the stations were "
                            "connected to different SSIDs.")
            assert True
