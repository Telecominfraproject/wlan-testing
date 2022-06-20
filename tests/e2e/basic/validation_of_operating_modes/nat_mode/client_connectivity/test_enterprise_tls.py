import allure
import pytest

pytestmark = [pytest.mark.ow_client_connectivity_lf,
              pytest.mark.nat, pytest.mark.enterprise, pytest.mark.tls, pytest.mark.uc_sanity]

setup_params_enterprise = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa_enterprise": [
            {"ssid_name": "tls_ssid_wpa_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "tls_ssid_wpa_eap_5g", "appliedRadios": ["5G"]}],
        "wpa2_enterprise": [
            {"ssid_name": "tls_ssid_wpa2_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "tls_ssid_wpa2_eap_5g", "appliedRadios": ["5G"]}],
        "wpa3_enterprise": [
            {"ssid_name": "tls_ssid_wpa3_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "tls_ssid_wpa3_eap_5g", "appliedRadios": ["5G"]}]},

    "rf": {},
    "radius": True
}


@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.uc_sanity
@pytest.mark.usefixtures("setup_profiles")
class TestNATModeEnterpriseTLSSuiteOne(object):

    @pytest.mark.wpa_enterprise
    @pytest.mark.twog
    def test_tls_wpa_enterprise_2g(self, get_ap_logs, get_lf_logs,
                                    station_names_twog, setup_profiles,  lf_test, update_report,
                                    test_cases, radius_info, exit_on_fail, get_ap_channel):
        """ wpa enterprise 2g
                    pytest -m "client_connectivity and bridge and enterprise and tts and twog"
                """

        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "NAT"
        band = "twog"
        channel = get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan = 1
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        # pk_passwd = radcius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                     mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                     identity=identity, station_name=station_names_twog,
                                     key_mgmt=key_mgmt, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.wpa_enterprise
    @pytest.mark.fiveg
    def test_tls_wpa_enterprise_5g(self, get_ap_logs, get_lf_logs,
                                    station_names_fiveg, setup_profiles,  lf_test,
                                    update_report, test_cases, radius_info, exit_on_fail, get_ap_channel):
        """ wpa enterprise 2g
                    pytest -m "client_connectivity and bridge and enterprise and tts and twog"
                """

        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "NAT"
        band = "fiveg"
        channel = get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)
        vlan = 1
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        # pk_passwd = radcius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                     mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                     identity=identity, station_name=station_names_fiveg,
                                     key_mgmt=key_mgmt, vlan_id=vlan, ssid_channel=channel)

        # if passes:
        #     update_report.update_testrail(case_id=test_cases["2g_wpa_NAT"],
        #                                   status_id=1,
        #                                   msg='2G WPA Client Connectivity Passed successfully - NAT mode' + str(
        #                                       passes))
        # else:
        #     update_report.update_testrail(case_id=test_cases["2g_wpa_NAT"],
        #                                   status_id=5,
        #                                   msg='2G WPA Client Connectivity Failed - NAT mode' + str(
        #                                       passes))

        assert passes == "PASS", result



    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    def test_tls_wpa2_enterprise_2g(self, get_ap_logs, get_lf_logs,
                                    station_names_twog, setup_profiles,  lf_test, update_report,
                                    test_cases, radius_info, exit_on_fail, get_ap_channel):
        """ wpa enterprise 2g
                    pytest -m "client_connectivity and bridge and enterprise and tts and twog"
                """

        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "NAT"
        band = "twog"
        channel = get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan = 1
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        # pk_passwd = radcius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                     identity=identity, station_name=station_names_twog,
                                     key_mgmt=key_mgmt, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    def test_tls_wpa2_enterprise_5g(self, get_ap_logs, get_lf_logs,
                                    station_names_fiveg, setup_profiles,  lf_test,
                                    update_report, test_cases, radius_info, exit_on_fail, get_ap_channel):
        """ wpa enterprise 2g
                    pytest -m "client_connectivity and bridge and enterprise and tts and twog"
                """

        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        channel = get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)
        vlan = 1
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        # pk_passwd = radcius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                     identity=identity, station_name=station_names_fiveg,
                                     key_mgmt=key_mgmt, vlan_id=vlan, ssid_channel=channel)

        # if passes:
        #     update_report.update_testrail(case_id=test_cases["2g_wpa_NAT"],
        #                                   status_id=1,
        #                                   msg='2G WPA Client Connectivity Passed successfully - NAT mode' + str(
        #                                       passes))
        # else:
        #     update_report.update_testrail(case_id=test_cases["2g_wpa_NAT"],
        #                                   status_id=5,
        #                                   msg='2G WPA Client Connectivity Failed - NAT mode' + str(
        #                                       passes))

        assert passes == "PASS", result



    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    def test_tls_wpa3_enterprise_2g(self, get_ap_logs, get_lf_logs,
                                    station_names_twog, setup_profiles,  lf_test, update_report,
                                    test_cases, radius_info, exit_on_fail, get_ap_channel):
        """ wpa enterprise 2g
                    pytest -m "client_connectivity and bridge and enterprise and tts and twog"
                """

        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "NAT"
        band = "twog"
        channel = get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan = 1
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP-SHA256"
        identity = radius_info['user']
        # pk_passwd = radcius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                     identity=identity, station_name=station_names_twog,
                                     key_mgmt=key_mgmt, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    def test_tls_wpa3_enterprise_5g(self, get_ap_logs, get_lf_logs,
                                    station_names_fiveg, setup_profiles,  lf_test,
                                    update_report, test_cases, radius_info, exit_on_fail, get_ap_channel):
        """ wpa3 enterprise 5g
                    pytest -m "client_connectivity and bridge and enterprise and tts and twog"
                """

        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "NAT"
        band = "fiveg"
        channel = get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)
        vlan = 1
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP-SHA256"
        identity = radius_info['user']
        # pk_passwd = radcius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band, eap=eap, ttls_passwd=tls_passwd,
                                     identity=identity, station_name=station_names_fiveg,
                                     key_mgmt=key_mgmt, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

setup_params_enterprise_two = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa_wpa2_enterprise_mixed": [
            {"ssid_name": "tls_ssid_wpa_wpa2_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "tls_ssid_wpa_wpa2_eap_5g", "appliedRadios": ["5G"]}],
        "wpa3_enterprise_mixed": [
            {"ssid_name": "tls_ssid_wpa3_mixed_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "tls_ssid_wpa3_mixed_eap_5g", "appliedRadios": ["5G"]}]
    },
    "rf": {},
    "radius": True
}


@allure.suite(suite_name="sanity")
@allure.sub_suite(sub_suite_name="Bridge Mode EAP Client Connectivity : Suite-B")
@pytest.mark.suiteB
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestNATModeEnterpriseTLSSuiteTwo(object):
    """ SuiteA Enterprise Test Cases
        pytest -m "client_connectivity and bridge and enterprise and ttls and suiteB"
    """

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.twog
    def test_wpa_wpa2_enterprise_2g(self, get_ap_logs, get_lf_logs,
                                    station_names_twog, setup_profiles,  lf_test, update_report,
                                    test_cases, radius_info, exit_on_fail, get_ap_channel):
        """ wpa enterprise 2g
            pytest -m "client_connectivity and bridge and enterprise and ttls and wpa_wpa2_enterprise_mixed and twog"
        """
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa_wpa2_enterprise_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "NAT"
        band = "twog"
        channel = get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)
        vlan = 1
        tls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=tls_passwd, identity=identity,
                                     station_name=station_names_twog, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result
    
    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.fiveg
    def test_wpa_wpa2_enterprise_5g(self, get_ap_logs, get_lf_logs,
                                    station_names_fiveg, setup_profiles,  lf_test,
                                    update_report, test_cases, radius_info, exit_on_fail, get_ap_channel):
        """ wpa enterprise 2g
            pytest -m "client_connectivity and bridge and enterprise and ttls and wpa_wpa2_enterprise_mixed and fiveg"
        """
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa_wpa2_enterprise_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "NAT"
        band = "fiveg"
        channel = get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)
        vlan = 1
        tls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=tls_passwd, identity=identity,
                                     station_name=station_names_fiveg, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.twog
    def test_wpa3_enterprise_mixed_2g(self, get_ap_logs, get_lf_logs,
                                      station_names_twog, setup_profiles,  lf_test,
                                      update_report, test_cases, radius_info, exit_on_fail, get_ap_channel):
        """ wpa enterprise 2g
            pytest -m "client_connectivity and bridge and enterprise and ttls and wpa3_enterprise_mixed and twog"
        """
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa3_enterprise_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "NAT"
        band = "twog"
        channel = get_ap_channel[0]["2G"]
        print("ssid channel:- ", channel)

        vlan = 1
        tls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=tls_passwd, identity=identity,
                                     station_name=station_names_twog, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.fiveg
    def test_wpa3_enterprise_mixed_5g(self, get_ap_logs, get_lf_logs,
                                      station_names_fiveg, setup_profiles,  lf_test,
                                      update_report, exit_on_fail,
                                      test_cases, radius_info, get_ap_channel):
        """ wpa enterprise 2g
            pytest -m "client_connectivity and bridge and enterprise and ttls and wpa3_enterprise_mixed and fiveg"
        """
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa3_enterprise_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "NAT"
        band = "fiveg"
        channel = get_ap_channel[0]["5G"]
        print("ssid channel:- ", channel)

        vlan = 1
        tls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        passes, result = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=tls_passwd, identity=identity,
                                     station_name=station_names_fiveg, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result


