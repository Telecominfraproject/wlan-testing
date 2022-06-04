"""

    Client Connectivity and tcp-udp Traffic Test: vlan Mode
    pytest -m "client_connectivity and vlan and general"

"""

import allure
import pytest

pytestmark = [pytest.mark.ow_sanity_lf,
              pytest.mark.ow_client_connectivity_lf,
              pytest.mark.vlan,
              pytest.mark.general,
              pytest.mark.sanity]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
                 {"ssid_name": "ssid_open_5g_vlan", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}],
        "wpa": [{"ssid_name": "ssid_wpa_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
                {"ssid_name": "ssid_wpa_5g_vlan", "appliedRadios": ["5G"],
                 "security_key": "something", "vlan": 100}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g_vlan", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa2_5g_vlan", "appliedRadios": ["5G"],
             "security_key": "something", "vlan": 100}]},
    "rf": {},
    "radius": False
}


@pytest.mark.uc_sanity
@pytest.mark.suiteA
@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestvlanModeConnectivitySuiteA(object):
    """ Client Connectivity SuiteA
        pytest -m "client_connectivity and vlan and general and suiteA"
    """

    @pytest.mark.open
    @pytest.mark.twog
    @allure.story('open 2.4 GHZ Band')
    def test_open_ssid_2g(self, get_ap_logs, get_lf_logs,
                          lf_test, update_report,
                          station_names_twog,
                          test_cases, get_ap_channel):
        """Client Connectivity open ssid 2.4G
           pytest -m "client_connectivity and vlan and general and open and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        channel = get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan = 100
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan, ssid_channel=channel)
        assert passes == "PASS", result

    @pytest.mark.open
    @pytest.mark.fiveg
    @allure.story('open 5 GHZ Band')
    def test_open_ssid_5g(self, get_ap_logs, get_lf_logs,
                          lf_test, test_cases, station_names_fiveg,
                          update_report, get_ap_channel):
        """Client Connectivity open ssid 5G
           pytest -m "client_connectivity and vlan and general and open and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        channel = get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)
        vlan = 100
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.sanity_light
    @pytest.mark.wpa
    @pytest.mark.twog
    @allure.story('wpa 2.4 GHZ Band')
    def test_wpa_ssid_2g(self, get_ap_logs,
                         update_report, get_lf_logs,
                         lf_test, test_cases, station_names_twog, get_ap_channel):
        """Client Connectivity wpa ssid 2.4G
           pytest -m "client_connectivity and vlan and general and wpa and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "VLAN"
        band = "twog"
        channel = get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan = 100
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.sanity_light
    @pytest.mark.wpa
    @pytest.mark.fiveg
    @allure.story('wpa 5 GHZ Band')
    def test_wpa_ssid_5g(self, get_ap_logs, get_lf_logs,
                         lf_test, update_report, test_cases, station_names_fiveg, get_ap_channel):
        """Client Connectivity wpa ssid 5G
           pytest -m "client_connectivity and vlan and general and wpa and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "VLAN"
        band = "fiveg"
        channel = get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)
        vlan = 100
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.sanity_light
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    def test_wpa2_personal_ssid_2g(self, get_ap_logs, get_lf_logs,
                                   lf_test, update_report, test_cases,
                                   station_names_twog, get_ap_channel):
        """Client Connectivity wpa2_personal ssid 2.4G
           pytest -m "client_connectivity and vlan and general and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        channel = get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan = 100
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.sanity_light
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    def test_wpa2_personal_ssid_5g(self, get_ap_logs, get_lf_logs,
                                   update_report, test_cases,
                                   station_names_fiveg,
                                   lf_test, get_ap_channel):
        """Client Connectivity wpa2_personal ssid 5G
           pytest -m "client_connectivity and vlan and general and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        channel = get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)
        vlan = 100
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result


setup_params_general_two = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa3_p_5g", "appliedRadios": ["5G"],
             "security_key": "something", "vlan": 100}],
        "wpa3_personal_mixed": [
            {"ssid_name": "ssid_wpa3_p_m_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa3_p_m_5g", "appliedRadios": ["5G"],
             "security_key": "something", "vlan": 100}],
        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g", "appliedRadios": ["5G"],
             "security_key": "something", "vlan": 100}]
    },
    "rf": {},
    "radius": False
}


@pytest.mark.suiteB
@allure.feature("vlan MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestvlanModeConnectivitySuiteTwo(object):
    """ Client Connectivity SuiteA
        pytest -m "client_connectivity and vlan and suiteB"
    """

    @pytest.mark.uc_sanity
    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @allure.story('open 2.4 GHZ Band')
    def test_wpa3_personal_ssid_2g(self, get_ap_logs, get_lf_logs,
                                   station_names_twog, lf_test,
                                   update_report,
                                   test_cases, get_ap_channel):
        """Client Connectivity open ssid 2.4G
           pytest -m "client_connectivity and vlan and general and wpa3_personal and twog"
        """
        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "twog"
        channel = get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan = 100
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.uc_sanity
    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @allure.story('open 5 GHZ Band')
    def test_wpa3_personal_ssid_5g(self, get_ap_logs, get_lf_logs,
                                   station_names_fiveg, lf_test, test_cases,
                                   update_report, get_ap_channel):
        """Client Connectivity open ssid 2.4G
           pytest -m "client_connectivity and vlan and general and wpa3_personal and fiveg"
        """
        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "fiveg"
        channel = get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)
        vlan = 100
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan, ssid_channel=channel)
        assert passes == "PASS", result

    @pytest.mark.uc_sanity
    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.twog
    @allure.story('open 2.4 GHZ Band')
    def test_wpa3_personal_mixed_ssid_2g(self, get_ap_logs,
                                         station_names_twog,
                                         lf_test, get_lf_logs,
                                         update_report,
                                         test_cases, get_ap_channel):
        """Client Connectivity open ssid 2.4G
           pytest -m "client_connectivity and vlan and general and wpa3_personal_mixed and twog"
        """
        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "twog"
        channel = get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan = 100
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan, ssid_channel=channel)
        assert passes == "PASS", result

    @pytest.mark.uc_sanity
    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.fiveg
    @allure.story('open 5 GHZ Band')
    def test_wpa3_personal_mixed_ssid_5g(self, get_ap_logs,
                                         station_names_fiveg, lf_test,
                                         test_cases, get_lf_logs,
                                         update_report, get_ap_channel):
        """Client Connectivity open ssid 2.4G
           pytest -m "client_connectivity and vlan and general and wpa3_personal_mixed and fiveg"
        """
        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "VLAN"
        band = "fiveg"
        channel = get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)
        vlan = 100
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan, ssid_channel=channel)
        assert passes == "PASS", result

    @pytest.mark.uc_sanity
    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.twog
    @allure.story('wpa wpa2 personal mixed 2.4 GHZ Band')
    def test_wpa_wpa2_personal_ssid_2g(self, get_ap_logs,
                                       station_names_twog,
                                       lf_test, get_lf_logs,
                                       update_report,
                                       test_cases, get_ap_channel):
        """Client Connectivity open ssid 2.4G
           pytest -m "client_connectivity and vlan and general and wpa_wpa2_personal_mixed and twog"
        """
        profile_data = setup_params_general_two["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "twog"
        channel = get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan = 100
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan, ssid_channel=channel)
        assert passes == "PASS", result

    @pytest.mark.uc_sanity
    @pytest.mark.wpa_wpa2_personal_mixed
    @pytest.mark.fiveg
    @allure.story('wpa wpa2 personal mixed 5 GHZ Band')
    def test_wpa_wpa2_personal_ssid_5g(self, get_ap_logs, get_lf_logs,
                                       station_names_fiveg, lf_test, test_cases,
                                       update_report, get_ap_channel):
        """Client Connectivity open ssid 2.4G
           pytest -m "client_connectivity and vlan and general and wpa_wpa2_personal_mixed and fiveg"
        """
        profile_data = setup_params_general_two["ssid_modes"]["wpa_wpa2_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "fiveg"
        channel = get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)
        vlan = 100
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

# WEP Security Feature not available
# setup_params_wep = {
#     "mode": "VLAN",
#     "ssid_modes": {
#         "wep": [ {"ssid_name": "ssid_wep_2g", "appliedRadios": ["2G"], "default_key_id": 1,
#                   "wep_key": 1234567890},
#                 {"ssid_name": "ssid_wep_5g", "appliedRadios": ["5G"],
#                  "default_key_id": 1, "wep_key": 1234567890}]
#     },
#     "rf": {},
#     "radius": True
# }
#
#
# @pytest.mark.enterprise
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_wep],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")
# class TestvlanModeWEP(object):
#
#     @pytest.mark.wep
#     @pytest.mark.twog
#     def test_wep_2g(self, get_vif_state,station_names_twog, setup_profiles,  lf_test, update_report,
#                                test_cases, radius_info):
#         profile_data = setup_params_wep["ssid_modes"]["wep"][0]
#         ssid_name = profile_data["ssid_name"]
#         wep_key = "[BLANK]"
#         security = "open"
#         extra_secu = []
#         mode = "VLAN"
#         band = "twog"
#         vlan = 100
#         passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
#                                                      passkey=wep_key, mode=mode, band=band,
#                                                      station_name=station_names_twog, vlan_id=vlan)
#
#         if passes:
#             update_report.update_testrail(case_id=test_cases["2g_wpa_vlan"],
#                                           status_id=1,
#                                           msg='2G WPA Client Connectivity Passed successfully - vlan mode' + str(
#                                               passes))
#         else:
#             update_report.update_testrail(case_id=test_cases["2g_wpa_vlan"],
#                                           status_id=5,
#                                           msg='2G WPA Client Connectivity Failed - vlan mode' + str(
#                                               passes))
#         assert passes
#
#     @pytest.mark.wep
#     @pytest.mark.fiveg
#     def test_wep_5g(self, get_vif_state,station_names_fiveg, setup_profiles,  lf_test, update_report,
#                                test_cases, radius_info):
#         profile_data = setup_params_wep["ssid_modes"]["wep"][1]
#         ssid_name = profile_data["ssid_name"]
#         wep_key = "[BLANK]"
#         security = "open"
#         extra_secu = []
#         mode = "VLAN"
#         band = "twog"
#         vlan = 100
#         passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
#                                                      passkey=wep_key, mode=mode, band=band,
#                                                      station_name=station_names_fiveg, vlan_id=vlan)
#
#         if passes:
#             update_report.update_testrail(case_id=test_cases["2g_wpa_vlan"],
#                                           status_id=1,
#                                           msg='2G WPA Client Connectivity Passed successfully - vlan mode' + str(
#                                               passes))
#         else:
#             update_report.update_testrail(case_id=test_cases["2g_wpa_vlan"],
#                                           status_id=5,
#                                           msg='2G WPA Client Connectivity Failed - vlan mode' + str(
#                                               passes))
#         assert passes
