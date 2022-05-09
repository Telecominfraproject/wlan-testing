"""
    Config AP with maximum no.of SSIDs Test: Bridge Mode
    pytest -m max_ssid
"""

import time
import allure
import pytest
from configuration import DYNAMIC_VLAN_RADIUS_SERVER_DATA
from configuration import DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]}],

        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"],
             "radius_auth_data": DYNAMIC_VLAN_RADIUS_SERVER_DATA,
             "radius_acc_data": DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA,
             }],

        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"],
             "radius_auth_data": DYNAMIC_VLAN_RADIUS_SERVER_DATA,
             "radius_acc_data": DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA,
             }],

        "wpa_enterprise": [
            {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["2G"],
             "radius_auth_data": DYNAMIC_VLAN_RADIUS_SERVER_DATA,
             "radius_acc_data": DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA,
             }],
    },
    "rf": {},
    "radius": False
}

pytestmark = [pytest.mark.max_ssid, pytest.mark.bridge]


@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMaxSsidBridge2G(object):
    """Config AP with maximum no.of SSIDs Test Bridge mode
       pytest -m "max_ssid and bridge"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.open
    @pytest.mark.twog
    def test_client_bridge_open_2g(self, lf_test, station_names_twog, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security = "open"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if passes == "PASS":
            if lf_test.station_ip != '0.0.0.0':
                print(f"{station_names_twog}---{lf_test.station_ip}\nstation got IP. Test passed")
                assert True
            else:
                assert False
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa
    @pytest.mark.twog
    def test_client_bridge_wpa_2g(self, lf_test, station_names_twog, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if passes == "PASS":
            if lf_test.station_ip != '0.0.0.0':
                print(f"{station_names_twog}---{lf_test.station_ip}\nstation got IP. Test passed")
                assert True
            else:
                assert False
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_client_bridge_wpa2_2g(self, lf_test, station_names_twog, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if passes == "PASS":
            if lf_test.station_ip != '0.0.0.0':
                print(f"{station_names_twog}---{lf_test.station_ip}\nstation got IP. Test passed")
                assert True
            else:
                assert False
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.twog
    def test_client_bridge_wpa_wpa2_2g(self, lf_test, station_names_twog, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,extra_securities=extra_secu,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if passes == "PASS":
            if lf_test.station_ip != '0.0.0.0':
                print(f"{station_names_twog}---{lf_test.station_ip}\nstation got IP. Test passed")
                assert True
            else:
                assert False
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    def test_client_bridge_wpa3_2g(self, lf_test, station_names_twog, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if passes == "PASS":
            if lf_test.station_ip != '0.0.0.0':
                print(f"{station_names_twog}---{lf_test.station_ip}\nstation got IP. Test passed")
                assert True
            else:
                assert False
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    def test_client_bridge_wpa2_eap_2g(self, get_ap_logs, get_lf_logs, station_names_twog, setup_profiles,  lf_test,
                                      update_report, exit_on_fail, test_cases, radius_info):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 100
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                             mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                             identity=identity, station_name=station_names_twog,
                                             key_mgmt=key_mgmt, vlan_id=vlan)

        if passes == "PASS":
            if lf_test.station_ip != '0.0.0.0':
                print(f"{station_names_twog}---{lf_test.station_ip}\nstation got IP. Test passed")
                assert True
            else:
                assert False
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    def test_client_bridge_wpa3_eap_2g(self, get_ap_logs, get_lf_logs, station_names_twog, setup_profiles,  lf_test,
                                      update_report, exit_on_fail, test_cases, radius_info):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 100
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                             mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                             identity=identity, station_name=station_names_twog,
                                             key_mgmt=key_mgmt, vlan_id=vlan)

        if passes == "PASS":
            if lf_test.station_ip != '0.0.0.0':
                print(f"{station_names_twog}---{lf_test.station_ip}\nstation got IP. Test passed")
                assert True
            else:
                assert False
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa_enterprise
    @pytest.mark.twog
    def test_client_bridge_wpa_eap_2g(self, get_ap_logs, get_lf_logs, station_names_twog, setup_profiles,  lf_test,
                                      update_report, exit_on_fail, test_cases, radius_info):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 100
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                             mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                             identity=identity, station_name=station_names_twog,
                                             key_mgmt=key_mgmt, vlan_id=vlan)

        if passes == "PASS":
            if lf_test.station_ip != '0.0.0.0':
                print(f"{station_names_twog}---{lf_test.station_ip}\nstation got IP. Test passed")
                assert True
            else:
                assert False
        else:
            assert False


setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]}],

        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"],
             "radius_auth_data": DYNAMIC_VLAN_RADIUS_SERVER_DATA,
             "radius_acc_data": DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA,
             }],

        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"],
             "radius_auth_data": DYNAMIC_VLAN_RADIUS_SERVER_DATA,
             "radius_acc_data": DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA,
             }],

        "wpa_enterprise": [
            {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["2G"],
             "radius_auth_data": DYNAMIC_VLAN_RADIUS_SERVER_DATA,
             "radius_acc_data": DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA,
             }],

        "wpa_wpa2_enterprise_mixed": [
            {"ssid_name": "max_ssid_wpa_wpa2_eap_2g", "appliedRadios": ["2G"],
             "radius_auth_data": DYNAMIC_VLAN_RADIUS_SERVER_DATA,
             "radius_acc_data": DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA,
             }],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestAdditionalSsidBridge2G(object):
    """Config AP with maximum no.of SSIDs Test Bridge mode
       pytest -m "max_ssid and bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.add_ssid
    def test_client_bridge_open_2g(self, lf_test, station_names_twog, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general1["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security = "open"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if passes == "FAIL":
            assert True
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.add_ssid
    def test_client_bridge_wpa_2g(self, lf_test, station_names_twog, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general1["ssid_modes"]["wpa"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if passes == "FAIL":
            assert True
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.add_ssid
    def test_client_bridge_wpa2_2g(self, lf_test, station_names_twog, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if passes == "FAIL":
            assert True
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.twog
    @pytest.mark.add_ssid
    def test_client_bridge_wpa_wpa2_2g(self, lf_test, station_names_twog, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general1["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if passes == "FAIL":
            assert True
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @pytest.mark.add_ssid
    def test_client_bridge_wpa3_2g(self, lf_test, station_names_twog, get_configuration):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general1["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if passes == "FAIL":
            assert True
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.add_ssid
    def test_client_bridge_wpa2_eap_2g(self, get_ap_logs, get_lf_logs, station_names_twog, setup_profiles, lf_test,
                                       update_report, exit_on_fail, test_cases, radius_info):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general1["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 100
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                             mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                             identity=identity, station_name=station_names_twog,
                                             key_mgmt=key_mgmt, vlan_id=vlan)

        if passes == "FAIL":
            assert True
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    @pytest.mark.add_ssid
    def test_client_bridge_wpa3_eap_2g(self, get_ap_logs, get_lf_logs, station_names_twog, setup_profiles, lf_test,
                                       update_report, exit_on_fail, test_cases, radius_info):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general1["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 100
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                             mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                             identity=identity, station_name=station_names_twog,
                                             key_mgmt=key_mgmt, vlan_id=vlan)

        if passes == "FAIL":
            assert True
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa_enterprise
    @pytest.mark.twog
    @pytest.mark.add_ssid
    def test_client_bridge_wpa_eap_2g(self, get_ap_logs, get_lf_logs, station_names_twog, setup_profiles, lf_test,
                                      update_report, exit_on_fail, test_cases, radius_info):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general1["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 100
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                             mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                             identity=identity, station_name=station_names_twog,
                                             key_mgmt=key_mgmt, vlan_id=vlan)  # , ssid_channel=channel)

        if passes == "FAIL":
            assert True
        else:
            assert False


    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.twog
    @pytest.mark.add_ssid
    def test_client_bridge_wpa_wpa2_eap_2g(self, get_ap_logs, get_lf_logs, station_names_twog, setup_profiles,  lf_test,
                                      update_report, exit_on_fail, test_cases, radius_info):
        """Max-SSID Bridge Mode
           pytest -m "max_ssid and twog"
        """
        profile_data = setup_params_general1["ssid_modes"]["wpa_wpa2_enterprise_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
        band = "twog"
        vlan = 100
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        lf_test.station_ip = '0.0.0.0'

        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                             mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                             identity=identity, station_name=station_names_twog,
                                             key_mgmt=key_mgmt, vlan_id=vlan)

        if passes == "FAIL":
            assert True
        else:
            assert False

