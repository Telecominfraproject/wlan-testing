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
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10610", name="WIFI-10610")
    def test_client_isolation_disabled_ssid_5g(self, lf_test, update_report, test_cases,
                                               station_names_fiveg, get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][2]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][3]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg
        scan_ssid = True
        band = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name1, passkey=security_key, security=security, mode=mode,
                                             band=band, vlan_id=vlan, station_name=[station_list], scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name2, passkey=security_key, security=security, mode=mode,
                                             band=band, vlan_id=vlan, station_name=[station_list], scan_ssid=scan_ssid)
        print(sta_result2)
        sta_list = station_list
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta_list)
        print(layer3_restult)

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.eth_to_2g_station_true
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10620", name="WIFI-10620")
    def test_client_isolation_enabled_with_2g(self, lf_test, update_report, test_cases,
                                              station_names_fiveg, get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and ethernet_to_2g_station_true and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg
        band = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result = lf_test.Client_Connect(ssid=ssid_name, passkey=security_key, security=security, mode=mode,
                                            band=band, vlan_id=vlan, station_name=[station_list],
                                            scan_ssid=True)
        print(sta_result)
        sta_list = station_list
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta_list)
        print(layer3_restult)

        assert True


    # clients_connected to different ssid, enabling isolation in both(2.4GH)
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10602",name="WIFI-10602")
    def test_client_isolation_enabled_ssids_2g(self,lf_test, update_report, test_cases,
                                                 station_names_twog,get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_twog
        scan_ssid = True
        band = "twog"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name1, passkey=security_key, security=security, mode=mode,
                                            band=band, vlan_id=vlan, station_name=[station_list], scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name2, passkey=security_key, security=security, mode=mode,
                                        band=band, vlan_id=vlan, station_name=[station_list], scan_ssid=scan_ssid)
        print(sta_result2)
        sta_list = station_list
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                           side_b_min_rate=0, side_b_max_rate=0,
                                           traffic_type="lf_udp", sta_list=sta_list)
        print(layer3_restult)

        assert True

    # Running traffic between eth2 to station with client-isolation enabled in (5GH) ssid
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.eth_to_5g_station_true
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10621", name="WIFI-10621")
    def test_client_isolation_enabled_with_5g(self, lf_test, update_report, test_cases,
                                              station_names_fiveg, get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and ethernet_to_5g_station_true and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][2]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg
        band = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result = lf_test.Client_Connect(ssid=ssid_name, passkey=security_key, security=security, mode=mode,
                                            band=band, vlan_id=vlan, station_name=[station_list],
                                            scan_ssid=True)
        print(sta_result)
        sta_list = station_list
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta_list)
        print(layer3_restult)

        assert True


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
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10603", name="WIFI-10603")
    def test_client_isolation_enabled_ssids_2g(self, lf_test, update_report, test_cases,
                                               station_names_twog, get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_twog
        scan_ssid = True
        band = "twog"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name1, passkey=security_key, security=security, mode=mode,
                                             band=band, vlan_id=vlan, station_name=[station_list], scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name2, passkey=security_key, security=security, mode=mode,
                                             band=band, vlan_id=vlan, station_name=[station_list], scan_ssid=scan_ssid)
        print(sta_result2)
        sta_list = station_list
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta_list)
        print(layer3_restult)

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.eth_to_2g_station_false
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10624", name="WIFI-10624")
    def test_client_iso_in_same_ssids_2g(self, lf_test, update_report, test_cases,
                                         station_names_fiveg, get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and eth_to_2g_station_false and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg
        band = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result = lf_test.Client_Connect(ssid=ssid_name, passkey=security_key, security=security, mode=mode,
                                            band=band, vlan_id=vlan, station_name=[station_list],
                                            scan_ssid=True)
        print(sta_result)
        sta_list = station_list
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta_list)
        print(layer3_restult)

        assert True



    # clients_connected to different ssid, disabling isolation in both(5GH)
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10611",name="WIFI-10611")
    def test_client_isolation_disabled_ssid_5g(self,lf_test, update_report, test_cases,
                                                 station_names_fiveg,get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][2]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][3]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg
        scan_ssid = True
        band = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name1, passkey=security_key, security=security, mode=mode,
                                            band=band, vlan_id=vlan, station_name=[station_list], scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name2, passkey=security_key, security=security, mode=mode,
                                            band=band, vlan_id=vlan, station_name=[station_list], scan_ssid=scan_ssid)
        print(sta_result2)
        sta_list = station_list
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta_list)
        print(layer3_restult)

        assert True

    # Running traffic between eth2 to station with client-isolation disabled in (5GH) ssid
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.eth_to_5g_station_false
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10623", name="WIFI-10623")
    def test_client_iso_in_same_ssids_5g(self, lf_test, update_report, test_cases,
                                         station_names_fiveg, get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and ethernet_to_5g_station_false and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][3]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg
        band = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result = lf_test.Client_Connect(ssid=ssid_name, passkey=security_key, security=security, mode=mode,
                                            band=band, vlan_id=vlan, station_name=[station_list],
                                            scan_ssid=True)
        print(sta_result)
        sta_list = station_list
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta_list)
        print(layer3_restult)

        assert True


setup_params_general = {
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
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
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
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10601", name="WIFI-10601")
    def test_cleint_isolation_disabled_ssid_2g(self, lf_test, update_report,
                                               station_names_twog, get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_twog
        scan_ssid = True
        band = "twog"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1
        sta_result1 = lf_test.Client_Connect(ssid=ssid_name, passkey=security_key, security=security, mode=mode,
                                             band=band, vlan_id=vlan, station_name=[station_list],
                                             scan_ssid=scan_ssid)
        print("First Station resulet:", sta_result1)

        sta_result2 = lf_test.Client_Connect(ssid=ssid_name, passkey=security_key, security=security, mode=mode,
                                             band=band, vlan_id=vlan, station_name=[station_list],
                                             scan_ssid=scan_ssid)
        print("Second Station result:", sta_result2)
        sta_list = station_list
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta_list)
        print(layer3_restult)

        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10612", name="WIFI-10612")
    def test_cleint_isolation_disabled_ssid_5g(self, lf_test, update_report, test_cases,
                                              station_names_fiveg, get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg
        scan_ssid = True
        band = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name, passkey=security_key, security=security, mode=mode,
                                             band=band, vlan_id=vlan, station_name=[station_list],
                                             scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name, passkey=security_key, security=security, mode=mode,
                                             band=band, vlan_id=vlan, station_name=[station_list],
                                             scan_ssid=scan_ssid)
        print(sta_result2)
        sta_list = station_list
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta_list)
        print(layer3_restult)

        assert True


    # clients_connected to same ssid, disabled isolation(2.4GH)
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10604",name="WIFI-10604")
    def test_cleint_isolation_enabled_ssid_2g(self,lf_test, update_report,
                                             station_names_twog,get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][2]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_twog
        scan_ssid = True
        band = "twog"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1
        sta_result1 = lf_test.Client_Connect(ssid=ssid_name,passkey=security_key, security=security, mode=mode,
                                        band=band,vlan_id=vlan,station_name=[station_list], scan_ssid=scan_ssid)
        print("First Station resulet:",sta_result1)

        sta_result2 = lf_test.Client_Connect(ssid=ssid_name,passkey=security_key, security=security, mode=mode,
                                            band=band,vlan_id=vlan,station_name=[station_list], scan_ssid=scan_ssid)
        print("Second Station result:",sta_result2)
        sta_list = station_list
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta_list)
        print(layer3_restult)

        assert True

    # clients_connected to same ssid, enabled isolation(5GHZ)
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10606", name="WIFI-10606")
    def test_cleint_isolation_enabled_ssid_5g(self, lf_test, update_report, test_cases,
                                              station_names_fiveg, get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][3]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg
        scan_ssid = True
        band = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name, passkey=security_key, security=security, mode=mode,
                                             band=band, vlan_id=vlan, station_name=[station_list],
                                             scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name, passkey=security_key, security=security, mode=mode,
                                             band=band, vlan_id=vlan, station_name=[station_list],
                                             scan_ssid=scan_ssid)
        print(sta_result2)
        sta_list = station_list
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta_list)
        print(layer3_restult)

        assert True


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
                "ssid_name": "ci_disabled_wpa2_ssid2_2g",
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

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.twog
    @pytest.mark.ci_enable_and_disable_2g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10605", name="WIFI-10605")
    def test_client_isoaltion_enabled_ssid_2g_disabled_ssid_2g(self, lf_test, update_report, test_cases,
                                                               station_names_twog, station_names_fiveg,
                                                               get_ap_channel):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and ci_enable_and_disable_2g and twog and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog
        station_list2 = station_names_fiveg
        scan_ssid = True
        band1 = "twog"
        band2 = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name1, passkey=security_key, security=security, mode=mode,
                                             band=band1, vlan_id=vlan, station_name=[station_list1],
                                             scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name2, passkey=security_key, security=security, mode=mode,
                                             band=band2, vlan_id=vlan, station_name=[station_list2],
                                             scan_ssid=scan_ssid)
        print(sta_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=station_list1,
                                               side_b_list=station_list2)
        print(layer3_restult)

        assert True

    # run traffic from 2g to 5g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.bridge
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10614",name="WIFI-10614")
    def test_client_isolation_enabled_ssids_2gdisabled_ssid_5g(self, lf_test, update_report,test_cases,
                                                                station_names_twog,station_names_fiveg,get_ap_channel):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][3]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog
        station_list2 = station_names_fiveg
        scan_ssid = True
        band1 = "twog"
        band2 = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name1, passkey=security_key, security=security, mode=mode,
                                       band=band1, vlan_id=vlan, station_name=[station_list1], scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name2, passkey=security_key, security=security, mode=mode,
                                       band=band2, vlan_id=vlan, station_name=[station_list2], scan_ssid=scan_ssid)
        print(sta_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=station_list1,side_b_list=station_list2)
        print(layer3_restult)

        assert True

    # run traffic from 2g to 5g
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.twog
    @pytest.mark.ci_enabled_2g_and_5g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10616", name="WIFI-10616")
    def test_client_isolation_enabled_ssid2g_and_ssid5g(self, lf_test, update_report, test_cases,
                                                          station_names_twog, station_names_fiveg, get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and ci_enabled_2g_and_5g and twog and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][2]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog
        station_list2 = station_names_fiveg
        scan_ssid = True
        band1 = "twog"
        band2 = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name1, passkey=security_key, security=security, mode=mode,
                                             band=band1, vlan_id=vlan, station_name=[station_list1],
                                             scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name2, passkey=security_key, security=security, mode=mode,
                                             band=band2, vlan_id=vlan, station_name=[station_list2],
                                             scan_ssid=scan_ssid)
        print(sta_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=station_list1,side_b_list=station_list2)
        print(layer3_restult)

        assert True

    # run traffic from 2g to 5g
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.twog
    @pytest.mark.ci_disable_2g_and_5g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10618",name="WIFI-10618")
    def test_client_isolation_disabled_ssid2g_and_ssid5g(self, lf_test, update_report, test_cases,
                                                 station_names_twog,station_names_fiveg,get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and ci_disable_2g_and_5g and twog and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][3]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog
        station_list2 = station_names_fiveg
        scan_ssid = True
        band1 = "twog"
        band2 = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name1, passkey=security_key, security=security, mode=mode,
                                        band=band1, vlan_id=vlan, station_name=[station_list1], scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name2, passkey=security_key, security=security, mode=mode,
                                        band=band2, vlan_id=vlan, station_name=[station_list2], scan_ssid=scan_ssid)
        print(sta_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=station_list1,side_b_list=station_list2)
        print(layer3_restult)

        assert True

    # run traffic from 5g to 2g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.bridge
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10625", name="WIFI-10625")
    def test_client_isolation_disabled_ssid_2genabled_ssid_5g(self, lf_test, update_report,test_cases,
                                                      station_names_twog,station_names_fiveg, get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and bridge and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][2]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog
        station_list2 = station_names_fiveg
        scan_ssid = True
        band1 = "twog"
        band2 = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name1, passkey=security_key, security=security, mode=mode,
                                      band=band1, vlan_id=vlan, station_name=[station_list1], scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name2, passkey=security_key, security=security, mode=mode,
                                      band=band2, vlan_id=vlan, station_name=[station_list2], scan_ssid=scan_ssid)
        print(sta_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=station_list2,side_b_list=station_list1)
        print(layer3_restult)

        assert True


    # clients_connected to different ssid,enabled isolation in (2GHz)ssid & isolation disabled in (5GH)ssid
    # run traffic from 5g to 2g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.bridge
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10615",name="WIFI-10615")
    def test_client_isolation_enabled_ssids_2g_disabled_ssid_5g(self, lf_test, update_report,test_cases,
                                                                station_names_twog,station_names_fiveg,get_ap_channel):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][3]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog
        station_list2 = station_names_fiveg
        scan_ssid = True
        band1 = "twog"
        band2 = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name1, passkey=security_key, security=security, mode=mode,
                                       band=band1, vlan_id=vlan, station_name=[station_list1], scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name2, passkey=security_key, security=security, mode=mode,
                                       band=band2, vlan_id=vlan, station_name=[station_list2], scan_ssid=scan_ssid)
        print(sta_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=station_list2,side_b_list=station_list1)
        print(layer3_restult)

        assert True

    # clients_connected to different ssid,disabled isolation in ssid (2GHz)& isolation enabled in ssid(5GH)
    # run traffic from 2g to 5g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.bridge
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10626", name="WIFI-10626")
    def test_client_isolation_disabled_ssid_2g_enabled_ssid_5g(self, lf_test, update_report,test_cases,
                                                      station_names_twog,station_names_fiveg, get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and bridge and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][2]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog
        station_list2 = station_names_fiveg
        scan_ssid = True
        band1 = "twog"
        band2 = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name1, passkey=security_key, security=security, mode=mode,
                                      band=band1, vlan_id=vlan, station_name=[station_list1], scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name2, passkey=security_key, security=security, mode=mode,
                                      band=band2, vlan_id=vlan, station_name=[station_list2], scan_ssid=scan_ssid)
        print(sta_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=station_list1,side_b_list=station_list2)
        print(layer3_restult)

        assert True

    # clients_connected to different ssid, enabling isolation in both (2GHz) & (5GHz) ssid
    # run traffic from 5g to 2g
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.twog
    @pytest.mark.ci_enabled_2g_and_5g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10617", name="WIFI-10617")
    def test_client_isolation_enabled_ssid_2g_and_ssid_5g(self, lf_test, update_report, test_cases,
                                                          station_names_twog, station_names_fiveg, get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and ci_enabled_2g_and_5g and twog and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][2]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog
        station_list2 = station_names_fiveg
        scan_ssid = True
        band1 = "twog"
        band2 = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name1, passkey=security_key, security=security, mode=mode,
                                             band=band1, vlan_id=vlan, station_name=[station_list1],
                                             scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name2, passkey=security_key, security=security, mode=mode,
                                             band=band2, vlan_id=vlan, station_name=[station_list2],
                                             scan_ssid=scan_ssid)
        print(sta_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=station_list2,side_b_list=station_list1)
        print(layer3_restult)

        assert True

    # clients_connected to different ssid, disabled isolation in both (2GHz) & (5GHz) ssid
    # run traffic from 5g to 2g
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.twog
    @pytest.mark.ci_disable_2g_and_5g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10619",name="WIFI-10619")
    def test_client_isolation_disabled_ssid_2g_and_ssid_5g(self, lf_test, update_report, test_cases,
                                                 station_names_twog,station_names_fiveg,get_configuration):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and ci_disable_2g_and_5g and twog and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][3]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog
        station_list2 = station_names_fiveg
        scan_ssid = True
        band1 = "twog"
        band2 = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name1, passkey=security_key, security=security, mode=mode,
                                        band=band1, vlan_id=vlan, station_name=[station_list1], scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name2, passkey=security_key, security=security, mode=mode,
                                        band=band2, vlan_id=vlan, station_name=[station_list2], scan_ssid=scan_ssid)
        print(sta_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=station_list2,side_b_list=station_list1)
        print(layer3_restult)

        assert True

    # clients_connected to different ssid,enabling isolation in ssid (5GH)& isolation disabled in ssid (5GHZ)
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.twog
    @pytest.mark.ci_enable_and_disable_5g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10613", name="WIFI-10613")
    def test_client_isoaltion_enabled_ssid_5g_disabled_ssid_5g(self, lf_test, update_report, test_cases,
                                                               station_names_twog, station_names_fiveg,
                                                               get_ap_channel):
        """Client-Isolation Bridge Mode
           pytest -m "client_isolation and ci_enable_and_disable_5g and twog and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][2]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][3]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog
        station_list2 = station_names_fiveg
        scan_ssid = True
        band1 = "twog"
        band2 = "fiveg"
        security = "wpa2"
        mode = "BRIDGE"
        vlan = 1

        sta_result1 = lf_test.Client_Connect(ssid=ssid_name1, passkey=security_key, security=security, mode=mode,
                                             band=band1, vlan_id=vlan, station_name=[station_list1],
                                             scan_ssid=scan_ssid)
        print(sta_result1)
        sta_result2 = lf_test.Client_Connect(ssid=ssid_name2, passkey=security_key, security=security, mode=mode,
                                             band=band2, vlan_id=vlan, station_name=[station_list2],
                                             scan_ssid=scan_ssid)
        print(sta_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate="10M", side_a_max_rate="10M",
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=station_list1,
                                               side_b_list=station_list2)
        print(layer3_restult)

        assert True
