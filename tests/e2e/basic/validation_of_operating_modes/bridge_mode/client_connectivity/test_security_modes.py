import allure
import pytest

pytestmark = [pytest.mark.client_connectivity, pytest.mark.bridge, pytest.mark.sanity]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["is2dot4GHz"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
                 "security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@pytest.mark.basic
@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectivitySuiteOne(object):

    @pytest.mark.open
    @pytest.mark.twog
    @allure.story('open 2.4 GHZ Band')
    def test_open_ssid_2g(self, setup_profiles, get_lanforge_data, lf_test, update_report, station_names_twog,
                          test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)

        # if result:
        #     update_report.update_testrail(case_id=test_cases["2g_wpa_bridge"],
        #                                   status_id=1,
        #                                   msg='2G WPA Client Connectivity Passed successfully - bridge mode' + str(
        #                                       passes))
        # else:
        #     update_report.update_testrail(case_id=test_cases["2g_wpa_bridge"],
        #                                   status_id=5,
        #                                   msg='2G WPA Client Connectivity Failed - bridge mode' + str(
        #                                       passes))
        assert result

    @pytest.mark.open
    @pytest.mark.fiveg
    @allure.story('open 5 GHZ Band')
    def test_open_ssid_5g(self, get_lanforge_data, lf_test, test_cases, station_names_fiveg, update_report):
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)

        # if result:
        #     update_report.update_testrail(case_id=test_cases["2g_wpa_bridge"],
        #                                   status_id=1,
        #                                   msg='2G WPA Client Connectivity Passed successfully - bridge mode' + str(
        #                                       passes))
        # else:
        #     update_report.update_testrail(case_id=test_cases["2g_wpa_bridge"],
        #                                   status_id=5,
        #                                   msg='2G WPA Client Connectivity Failed - bridge mode' + str(
        #                                       passes))
        assert result

    @pytest.mark.wpa
    @pytest.mark.twog
    @allure.story('wpa 2.4 GHZ Band')
    def test_wpa_ssid_2g(self, request, get_lanforge_data, update_report,
                         lf_test, test_cases, station_names_twog):
        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)

        if result:
            update_report.update_testrail(case_id=test_cases["2g_wpa_bridge"],
                                          status_id=1,
                                          msg='2G WPA Client Connectivity Passed successfully - bridge mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["2g_wpa_bridge"],
                                          status_id=5,
                                          msg='2G WPA Client Connectivity Failed - bridge mode' + str(
                                              passes))
        assert result

    @pytest.mark.wpa
    @pytest.mark.fiveg
    @allure.story('wpa 5 GHZ Band')
    def test_wpa_ssid_5g(self, lf_test, update_report, test_cases, station_names_fiveg, get_lanforge_data):
        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)

        if result:
            update_report.update_testrail(case_id=test_cases["5g_wpa_bridge"],
                                          status_id=1,
                                          msg='5G WPA Client Connectivity Passed successfully - bridge mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["5g_wpa_bridge"],
                                          status_id=5,
                                          msg='5G WPA Client Connectivity Failed - bridge mode' + str(
                                              passes))
        assert result

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    def test_wpa2_personal_ssid_2g(self, get_lanforge_data, lf_test, update_report, test_cases,
                                   station_names_twog):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)

        if result:
            update_report.update_testrail(case_id=test_cases["2g_wpa2_bridge"],
                                          status_id=1,
                                          msg='2G WPA2 Client Connectivity Passed successfully - bridge mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["2g_wpa2_bridge"],
                                          status_id=5,
                                          msg='2G WPA2 Client Connectivity Failed - bridge mode' + str(
                                              passes))
        assert result

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    def test_wpa2_personal_ssid_5g(self, get_lanforge_data, update_report, test_cases, station_names_fiveg,
                                   lf_test):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)

        if result:
            update_report.update_testrail(case_id=test_cases["5g_wpa2_bridge"],
                                          status_id=1,
                                          msg='5G WPA2 Client Connectivity Passed successfully - bridge mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["5g_wpa2_bridge"],
                                          status_id=5,
                                          msg='5G WPA2 Client Connectivity Failed - bridge mode' + str(
                                              passes))
        assert result


setup_params_general_two = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}],
        "wpa3_personal_mixed": [
            {"ssid_name": "ssid_wpa3_p_m_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_m_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}]
    },
    "rf": {},
    "radius": False
}


@pytest.mark.shivam
@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectivitySuiteTwo(object):

    @pytest.mark.wpa3_personal
    @pytest.mark.twog
    @allure.story('open 2.4 GHZ Band')
    def test_wpa3_personal_ssid_2g(self, station_names_twog, setup_profiles, get_lanforge_data, lf_test, update_report,
                                   test_cases):
        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = ["wpa3"]
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)

        if result:
            update_report.update_testrail(case_id=test_cases["2g_wpa_bridge"],
                                          status_id=1,
                                          msg='2G WPA Client Connectivity Passed successfully - bridge mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["2g_wpa_bridge"],
                                          status_id=5,
                                          msg='2G WPA Client Connectivity Failed - bridge mode' + str(
                                              passes))
        assert result

    @pytest.mark.wpa3_personal
    @pytest.mark.fiveg
    @allure.story('open 5 GHZ Band')
    def test_wpa3_personal_ssid_5g(self, station_names_fiveg, get_lanforge_data, lf_test, test_cases, update_report):
        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = ["wpa3"]
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)

        if result:
            update_report.update_testrail(case_id=test_cases["2g_wpa_bridge"],
                                          status_id=1,
                                          msg='2G WPA Client Connectivity Passed successfully - bridge mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["2g_wpa_bridge"],
                                          status_id=5,
                                          msg='2G WPA Client Connectivity Failed - bridge mode' + str(
                                              passes))
        assert result

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.twog
    @allure.story('open 2.4 GHZ Band')
    def test_wpa3_personal_mixed_ssid_2g(self, station_names_twog, setup_profiles, get_lanforge_data, lf_test, update_report,
                                         test_cases):
        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)

        if result:
            update_report.update_testrail(case_id=test_cases["2g_wpa_bridge"],
                                          status_id=1,
                                          msg='2G WPA Client Connectivity Passed successfully - bridge mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["2g_wpa_bridge"],
                                          status_id=5,
                                          msg='2G WPA Client Connectivity Failed - bridge mode' + str(
                                              passes))
        assert result

    @pytest.mark.wpa3_personal_mixed
    @pytest.mark.fiveg
    @allure.story('open 5 GHZ Band')
    def test_wpa3_personal_mixed_ssid_5g(self, station_names_fiveg, get_lanforge_data, lf_test, test_cases, update_report):
        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)

        if result:
            update_report.update_testrail(case_id=test_cases["2g_wpa_bridge"],
                                          status_id=1,
                                          msg='2G WPA Client Connectivity Passed successfully - bridge mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["2g_wpa_bridge"],
                                          status_id=5,
                                          msg='2G WPA Client Connectivity Failed - bridge mode' + str(
                                              passes))
        assert result

# setup_params_enterprise = {
#     "mode": "BRIDGE",
#     "ssid_modes": {
#         "wpa2_enterprise": [
#             {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
#             {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
#              "security_key": "something"}],
#         "wpa3_enterprise": [
#             {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["is2dot4GHz"]},
#             {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}]},
#
#     "rf": {},
#     "radius": True
# }
#
#
# @pytest.mark.enterprise
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_enterprise],
#     indirect=True,
#     scope="package"
# )
# @pytest.mark.usefixtures("setup_profiles")
# class TestBridgeModeEnterprise(object):
#
#     @pytest.mark.wpa2_enterprise
#     @pytest.mark.twog
#     def test_wpa2_enterprise_2g(self):
#         # print(setup_client_connectivity)
#         assert "setup_client_connectivity"
#
#     @pytest.mark.wpa2_enterprise
#     @pytest.mark.fiveg
#     def test_wpa2_enterprise_5g(self):
#         assert "setup_client_connectivity"
#
#     @pytest.mark.wpa3_enterprise
#     @pytest.mark.twog
#     def test_wpa3_enterprise_2g(self):
#         # print(setup_client_connectivity)
#         assert "setup_client_connectivity"
#
#     @pytest.mark.wpa3_enterprise
#     @pytest.mark.fiveg
#     def test_wpa3_enterprise_5g(self):
#         assert "setup_client_connectivity"
