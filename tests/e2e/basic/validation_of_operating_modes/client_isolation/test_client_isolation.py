"""
    Test Client Isolation: Bridge Mode
    pytest -m client_isolation
"""

import time
import allure
import pytest

pytestmark = [pytest.mark.client_isolation, pytest.mark.bridge]

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
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestClientIsolationEnabled(object):
    """
        Test Config with Enabling Client Isolation in SSIDs
        pytest -m "client_isolation and ci_enabled and bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10620", name="WIFI-10620")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.ci_enabled
    def test_client_isolation_enabled_ssid_2g(self, lf_test, station_names_twog, get_configuration):
        """
            Client-Isolation Bridge Mode
            pytest -m "client_isolation and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        scan_ssid = True
        mode = "BRIDGE"
        band = "twog"
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        security_key = profile_data["security_key"]
        vlan = 1
        station_names = station_names_twog
        passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                        band=band, station_name=[station_names_twog], vlan_id=vlan, scan_ssid=scan_ssid)
        sta_list = []
        sta_list = station_names
        lf_test.create_layer3(side_a_min_rate="6M", side_a_max_rate=0, side_b_min_rate="6M", side_b_max_rate=0,
                      traffic_type="lf_udp", sta_list=sta_list)


setup_params_general = {
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
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestClientIsolationDisabled(object):
    """
        Test Config with Enabling Client Isolation in SSIDs
        pytest -m "client_isolation and ci_disabled and bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10620", name="WIFI-10620")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.ci_disabled
    def test_client_isolation_disabled_ssid_2g(self, lf_test, station_names_twog, get_configuration):
        """
            Client-Isolation Bridge Mode
            pytest -m "client_isolation and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        scan_ssid = True
        mode = "BRIDGE"
        band = "twog"
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        security_key = profile_data["security_key"]
        vlan = 1
        station_names = station_names_twog
        passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                        band=band, station_name=[station_names_twog], vlan_id=vlan, scan_ssid=scan_ssid)
        sta_list = []
        sta_list = station_names
        lf_test.create_layer3(side_a_min_rate="6M", side_a_max_rate=0, side_b_min_rate="6M", side_b_max_rate=0,
                              traffic_type="lf_udp", sta_list=sta_list)


setup_params_general = {
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
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestClientIsolationSameSSID(object):
    """
        Test Config with Enabling Client Isolation in SSIDs
        pytest -m "client_isolation and ci_disabled and bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10620", name="WIFI-10620")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.ci_disabled
    def test_client_isolation_disabled_ssid_2g(self, lf_test, station_names_twog, get_configuration):
        """
            Client-Isolation Bridge Mode
            pytest -m "client_isolation and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        scan_ssid = True
        mode = "BRIDGE"
        band = "twog"
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        security_key = profile_data["security_key"]
        vlan = 1
        station_names = station_names_twog
        passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                        band=band, station_name=[station_names_twog], vlan_id=vlan, scan_ssid=scan_ssid)
        sta_list = []
        sta_list = station_names
        lf_test.create_layer3(side_a_min_rate="6M", side_a_max_rate=0, side_b_min_rate="6M", side_b_max_rate=0,
                              traffic_type="lf_udp", sta_list=sta_list)

setup_params_general = {
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
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestClientIsolationDifferentSSID(object):
    """
        Test Config with Enabling Client Isolation in SSIDs
        pytest -m "client_isolation and ci_disabled and bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10620", name="WIFI-10620")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.ci_disabled
    def test_client_isolation_disabled_ssid_2g(self, lf_test, station_names_twog, get_configuration):
        """
            Client-Isolation Bridge Mode
            pytest -m "client_isolation and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        scan_ssid = True
        mode = "BRIDGE"
        band = "twog"
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        security_key = profile_data["security_key"]
        vlan = 1
        station_names = station_names_twog
        passes = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key, mode=mode,
                                        band=band, station_name=[station_names_twog], vlan_id=vlan, scan_ssid=scan_ssid)
        sta_list = []
        sta_list = station_names
        lf_test.create_layer3(side_a_min_rate="6M", side_a_max_rate=0, side_b_min_rate="6M", side_b_max_rate=0,
                              traffic_type="lf_udp", sta_list=sta_list)
