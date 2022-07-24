"""
       RSN Capability Test : BRIDGE Mode
       pytest -m "rsn and open and bridge"
"""

import os
import allure
import pytest

pytestmark=[pytest.mark.rsn, pytest.mark.bridge]

setup_params_general={
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "rsn_ssid_open_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "rsn_ssid_open_5g", "appliedRadios": ["5G"]}
        ],
        "wpa": [
            {"ssid_name": "rsn_ssid_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "rsn_ssid_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ],
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ],
        "wpa3_personal_mixed": [
            {"ssid_name": "ssid_wpa3_p_m_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_m_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ],
        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ],
        "wpa2_enterprise": [
            {"ssid_name": "tls_ssid_wpa2_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "tls_ssid_wpa2_eap_5g", "appliedRadios": ["5G"]}
        ],
        "wpa3_enterprise": [
            {"ssid_name": "tls_ssid_wpa3_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "tls_ssid_wpa3_eap_5g", "appliedRadios": ["5G"]}
        ]
    },
    "rf": {
        "5G": {
            "band": '5G',
            "channel": 36,
            "channel-width": 80
        },
        "2G": {
            "band": '2G',
            "channel": 6,
            "channel-width": 20
        }
    },
    "radius": True
}


@pytest.mark.rsn
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestRSNCapabilitities(object):
    """
        RSN capabilities Test Cases
        pytest -m "rsn and bridge"
    """

    @pytest.mark.open
    @pytest.mark.twog
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-9539", name="WIFI-9539")
    def test_rsn_open_2g(self, radius_info, lf_test, station_names_twog, get_ap_channel):
        """
            rsn open 2.4g
            pytest -m "rsn and bridge and open and twog"
        """
        profile_data=setup_params_general["ssid_modes"]["open"][0]
        ssid_2g=profile_data["ssid_name"]
        security="open"
        extra_sec=[]
        mode="BRIDGE"
        band="twog"
        channel=6
        vlan=1
        print("ssid channel:- ", channel)
        passes=lf_test.rsn_test(ssid=ssid_2g, security=security, extra_securities=extra_sec, passkey="[BLANK]",
                                mode=mode, band=band, station_name=station_names_twog, vlan_id=vlan,
                                ssid_channel=channel, sniff_radio='wiphy0', sniff_channel=channel)

        assert passes

    @pytest.mark.open
    @pytest.mark.fiveg
    def test_rsn_open_5g(self, radius_info, lf_test, station_names_fiveg, get_ap_channel):
        """
            rsn open 5g
            pytest -m "rsn and bridge and wpa and fiveg"
        """
        profile_data=setup_params_general["ssid_modes"]["open"][1]
        ssid_5g=profile_data["ssid_name"]
        security="open"
        extra_sec = []
        mode="BRIDGE"
        band="twog"
        channel=36
        vlan=1
        print("ssid channel:- ", channel)
        passes, result=lf_test.rsn_test(ssid=ssid_5g, security=security, extra_securities=extra_sec, passkey="[BLANK]",
                                mode=mode, band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                ssid_channel=channel, sniff_radio='wiphy0', sniff_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.wpa
    @pytest.mark.twog
    @allure.story('wpa 2.4 GHZ Band')
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-9539", name="WIFI-9539")
    def test_rsn_wpa_2g(self, radius_info, lf_test, station_names_twog, get_ap_channel):
        """
            rsn wpa 2.4G
           pytest -m "rsn and bridge and wpa and twog"
        """
        profile_data=setup_params_general["ssid_modes"]["wpa"][0]
        ssid_2g=profile_data["ssid_name"]
        passkey=profile_data["security_key"]
        security="wpa"
        extra_sec=[]
        mode="BRIDGE"
        band="twog"
        channel=6
        print("ssid channel:- ", channel)
        vlan=1
        passes, result=lf_test.rsn_test(ssid=ssid_2g, security=security, extra_securities=extra_sec, passkey="[BLANK]",
                                        mode=mode, band=band, station_name=station_names_twog, vlan_id=vlan,
                                        ssid_channel=channel, sniff_radio='wiphy0', sniff_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @allure.story('wpa 5 GHZ Band')
    def test_rsn_wpa_5g(self, radius_info, lf_test, station_names_fiveg, get_ap_channel):
        """
            rsn wpa 5G
           pytest -m "rsn and bridge and wpa and fiveg"
        """
        profile_data=setup_params_general["ssid_modes"]["wpa"][1]
        ssid_5g=profile_data["ssid_name"]
        passkey=profile_data["security_key"]
        security="wpa"
        extra_sec = []
        mode="BRIDGE"
        band="fiveg"
        channel=36
        print("ssid channel:- ", channel)
        vlan=1
        passes, result=lf_test.rsn_test(ssid=ssid_5g, security=security, extra_securities=extra_sec, passkey=passkey,
                                mode=mode, band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                ssid_channel=channel, sniff_radio='wiphy0', sniff_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-9539", name="WIFI-9539")
    def test_rsn_wpa2_personal_2g(self, radius_info, lf_test, station_names_twog, get_ap_channel):
        """
            rsn wpa 2.4G
           pytest -m "rsn and bridge and wpa2_personal and twog"
        """
        profile_data=setup_params_general["ssid_modes"]["wpa"][0]
        ssid_2g=profile_data["ssid_name"]
        passkey=profile_data["security_key"]
        security="wpa2"
        extra_sec=[]
        mode="BRIDGE"
        band="twog"
        channel=6
        print("ssid channel:- ", channel)
        vlan=1
        passes, result=lf_test.rsn_test(ssid=ssid_2g, security=security, extra_securities=extra_sec, passkey="[BLANK]",
                                        mode=mode, band=band, station_name=station_names_twog, vlan_id=vlan,
                                        ssid_channel=channel, sniff_radio='wiphy0', sniff_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    def test_rsn_wpa2_personal_5g(self, radius_info, lf_test, station_names_fiveg, get_ap_channel):
        """
            rsn wpa2_personal 5G
           pytest -m "rsn and bridge and wpa2_personal and fiveg"
        """
        profile_data=setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_5g=profile_data["ssid_name"]
        passkey=profile_data["security_key"]
        security="wpa2"
        extra_sec = []
        mode="BRIDGE"
        band="fiveg"
        channel=36
        print("ssid channel:- ", channel)
        vlan=1
        passes, result=lf_test.rsn_test(ssid=ssid_5g, security=security, extra_securities=extra_sec, passkey=passkey,
                                mode=mode, band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                ssid_channel=channel, sniff_radio='wiphy0', sniff_channel=channel)
        assert passes == "PASS", result

    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @allure.story('open 2.4 GHZ Band')
    def test_wpa3_personal_ssid_2g(self, station_names_twog, lf_test, get_ap_channel):
        """RSN open ssid 2.4G
           pytest -m "rsn and bridge and general and wpa3_personal and twog"
        """
        profile_data=setup_params_general["ssid_modes"]["wpa3_personal"][0]
        ssid_2g=profile_data["ssid_name"]
        security_key=profile_data["security_key"]
        security="wpa3"
        extra_sec = []
        mode="BRIDGE"
        band="twog"
        channel=get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan=1
        passes, result=lf_test.rsn_test(ssid=ssid_2g, security=security, extra_securities=extra_sec, passkey=security_key,
                                mode=mode, band=band, station_name=station_names_twog, vlan_id=vlan,
                                ssid_channel=channel, sniff_radio='wiphy0', sniff_channel=channel)
        assert passes == "PASS", result

    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @allure.story('wpa3 5 GHZ Band')
    def test_wpa3_personal_ssid_5g(self, station_names_fiveg, lf_test, get_ap_channel):
        """RSN wpa3 Personal ssid 5G
           pytest -m "rsn and bridge and wpa3_personal and fiveg"
        """
        profile_data=setup_params_general["ssid_modes"]["wpa3_personal"][1]
        ssid_5g=profile_data["ssid_name"]
        security_key=profile_data["security_key"]
        security="wpa3"
        extra_sec = []
        mode="BRIDGE"
        band="fiveg"
        channel=get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)
        vlan=1
        passes, result=lf_test.rsn_test(ssid=ssid_5g, security=security, extra_securities=extra_sec, passkey=passkey,
                                mode=mode, band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                ssid_channel=channel, sniff_radio='wiphy0', sniff_channel=channel)
        assert passes == "PASS", result

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa3 Mixed GHZ Band')
    def test_wpa3_personal_mixed_ssid_2g(self, station_names_twog, lf_test, get_ap_channel):
        """RSN wpa3 personal ssid 2.4G
           pytest -m "rsn and bridge and general and wpa3_personal_mixed and twog"
        """
        profile_data=setup_params_general["ssid_modes"]["wpa3_personal_mixed"][0]
        ssid_2g=profile_data["ssid_name"]
        security_key=profile_data["security_key"]
        security="wpa3"
        extra_sec = []
        mode="BRIDGE"
        band="twog"
        channel=get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan=1
        passes, result=lf_test.rsn_test(ssid=ssid_2g, security=security_key, extra_securities=extra_sec, passkey="[BLANK]",
                                mode=mode, band=band, station_name=station_names_twog, vlan_id=vlan,
                                ssid_channel=channel, sniff_radio='wiphy0', sniff_channel=channel)
        assert passes == "PASS", result

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.fiveg
    @allure.story('open 5 GHZ Band')
    def test_wpa3_personal_mixed_ssid_5g(self, station_names_fiveg, lf_test, get_ap_channel):
        """RSN open ssid 2.4G
           pytest -m "rsn and bridge and general and wpa3_personal_mixed and fiveg"
        """
        profile_data=setup_params_general["ssid_modes"]["wpa3_personal_mixed"][1]
        ssid_5g=profile_data["ssid_name"]
        security_key=profile_data["security_key"]
        security="wpa3"
        extra_sec = []
        mode="BRIDGE"
        band="fiveg"
        channel=get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)
        vlan=1
        passes, result=lf_test.rsn_test(ssid=ssid_5g, security=security, extra_securities=extra_sec, passkey=security_key,
                                mode=mode, band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                ssid_channel=channel, sniff_radio='wiphy0', sniff_channel=channel)
        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa wpa2 personal mixed 2.4 GHZ Band')
    def test_wpa_wpa2_personal_ssid_2g(self, station_names_twog, lf_test, get_ap_channel):
        """RSN wpa-wpa2 mixed ssid 2.4G
           pytest -m "rsn and bridge and general and wpa_wpa2_personal_mixed and twog"
        """
        profile_data=setup_params_general["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
        ssid_2g=profile_data["ssid_name"]
        security_key=profile_data["security_key"]
        security="wpa"
        extra_sec=["wpa2"]
        mode="BRIDGE"
        band="twog"
        channel=get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan=1
        passes, result=lf_test.rsn_test(ssid=ssid_2g, security=security, extra_securities=extra_sec, passkey=security_key,
                                mode=mode, band=band, station_name=station_names_twog, vlan_id=vlan,
                                ssid_channel=channel, sniff_radio='wiphy0', sniff_channel=channel)
        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.fiveg
    @allure.story('wpa wpa2 personal mixed 5 GHZ Band')
    def test_wpa_wpa2_personal_ssid_5g(self, station_names_fiveg, lf_test, get_ap_channel):
        """RSN wpa-wpa2 mixed ssid 5G
           pytest -m "rsn and bridge and general and wpa_wpa2_personal_mixed and fiveg"
        """
        profile_data=setup_params_general["ssid_modes"]["wpa_wpa2_personal_mixed"][1]
        ssid_5g=profile_data["ssid_name"]
        security_key=profile_data["security_key"]
        security="wpa"
        extra_sec=["wpa2"]
        mode="BRIDGE"
        band="fiveg"
        channel=get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)
        vlan=1
        passes, result=lf_test.rsn_test(ssid=ssid_5g, security=security, extra_securities=extra_sec, passkey=security_key,
                                mode=mode, band=band, station_name=station_names_fiveg, vlan_id=vlan,
                                ssid_channel=channel, sniff_radio='wiphy0', sniff_channel=channel)
        assert passes == "PASS", result

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    def test_tls_wpa2_enterprise_2g(self, get_ap_logs, get_lf_logs,
                                    station_names_twog, setup_profiles, lf_test, update_report,
                                    test_cases, radius_info, exit_on_fail, get_ap_channel):
        """ wpa enterprise 2g
                    pytest -m "rsn and bridge and enterprise and tts and twog"
        """

        profile_data=setup_params_general["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name=profile_data["ssid_name"]
        security="wpa2"
        mode="BRIDGE"
        band="twog"
        channel=get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan=100
        tls_passwd=radius_info["password"]
        eap="TLS"
        key_mgmt="WPA-EAP"
        identity=radius_info['user']
        # pk_passwd = radius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result=lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                           mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                           identity=identity, station_name=station_names_twog,
                                           key_mgmt=key_mgmt, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    def test_tls_wpa2_enterprise_5g(self, get_ap_logs, get_lf_logs,
                                    station_names_fiveg, setup_profiles, lf_test,
                                    update_report, exit_on_fail,
                                    test_cases, radius_info, get_ap_channel):
        """ wpa enterprise 2g
                    pytest -m "rsn and bridge and enterprise and tts and twog"
                """

        profile_data=setup_params_general["ssid_modes"]["wpa2_enterprise"][1]
        ssid_name=profile_data["ssid_name"]
        security="wpa2"
        mode="BRIDGE"
        band="fiveg"
        print("output of get_ap_channel ", get_ap_channel)
        channel=get_ap_channel[0]["5G"]
        vlan=100
        tls_passwd=radius_info["password"]
        eap="TLS"
        key_mgmt="WPA-EAP"
        identity=radius_info['user']
        # pk_passwd = radius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result=lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                           mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                           identity=identity, station_name=station_names_fiveg,
                                           key_mgmt=key_mgmt, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    def test_tls_wpa3_enterprise_2g(self, get_ap_logs, get_lf_logs,
                                    station_names_twog, setup_profiles, lf_test, update_report,
                                    test_cases, radius_info, exit_on_fail, get_ap_channel):
        """ wpa enterprise 2g
                    pytest -m "rsn and bridge and enterprise and tts and twog"
                """

        profile_data=setup_params_general["ssid_modes"]["wpa3_enterprise"][0]
        ssid_name=profile_data["ssid_name"]
        security="wpa3"
        mode="BRIDGE"
        band="twog"
        channel=get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan=100
        tls_passwd=radius_info["password"]
        eap="TLS"
        key_mgmt="WPA-EAP-SHA256"
        identity=radius_info['user']
        # pk_passwd = radius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result=lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                           mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                           identity=identity, station_name=station_names_twog,
                                           key_mgmt=key_mgmt, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    def test_tls_wpa3_enterprise_5g(self, get_ap_logs, get_lf_logs,
                                    station_names_fiveg, setup_profiles, lf_test,
                                    update_report, exit_on_fail,
                                    test_cases, radius_info, get_ap_channel):
        """ wpa enterprise 5g
                    pytest -m "rsn and bridge and wpa3_enterprise and twog"
                """

        profile_data=setup_params_general["ssid_modes"]["wpa3_enterprise"][1]
        ssid_name=profile_data["ssid_name"]
        security="wpa3"
        mode="BRIDGE"
        band="fiveg"
        channel=get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)
        vlan=100
        tls_passwd=radius_info["password"]
        eap="TLS"
        key_mgmt="WPA-EAP-SHA256"
        identity=radius_info['user']
        passes, result=lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                           mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                           identity=identity, station_name=station_names_fiveg,
                                           key_mgmt=key_mgmt, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result
