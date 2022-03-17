import allure
import pytest

pytestmark = [pytest.mark.client_connectivity,
              pytest.mark.vlan, pytest.mark.enterprise, pytest.mark.tls, pytest.mark.uc_sanity]

setup_params_enterprise = {
    "mode": "VLAN",

    "ssid_modes": {
        "wpa_enterprise": [
            {"ssid_name": "tls_ssid_wpa_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "tls_ssid_wpa_eap_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa2_enterprise": [
            {"ssid_name": "tls_ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "tls_ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa3_enterprise": [
            {"ssid_name": "tls_ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "tls_ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "vlan": 100}]},

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
class TestVLANModeEnterpriseTLSSuiteOne(object):

    @pytest.mark.wpa_enterprise
    @pytest.mark.twog
    @pytest.mark.amrit
    def test_wpa_enterprise_2g(self, get_ap_logs, get_lf_logs,
                               station_names_twog, lf_test,
                               update_report,
                               test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "twog"
        vlan = 100
        ttls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, vlan_id=vlan)

        assert passes

    @pytest.mark.wpa_enterprise
    @pytest.mark.fiveg
    def test_wpa_enterprise_5g(self, get_ap_logs, get_lf_logs,
                               station_names_fiveg, lf_test,
                               update_report,
                               test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        ttls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, vlan_id=vlan)

        assert passes

    @pytest.mark.sanity_light
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    def test_wpa2_enterprise_2g(self, get_ap_logs, get_lf_logs,
                                station_names_twog, lf_test,
                                update_report,
                                test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = 100
        ttls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, vlan_id=vlan)

        assert passes

    @pytest.mark.sanity_light
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    def test_wpa2_enterprise_5g(self, get_ap_logs, get_lf_logs,
                                station_names_fiveg, lf_test,
                                update_report,
                                test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        ttls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, vlan_id=vlan)

        assert passes

    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    def test_wpa3_enterprise_2g(self, get_ap_logs, get_lf_logs,
                                station_names_twog, lf_test,
                                update_report,
                                test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "VLAN"
        band = "twog"
        vlan = 100
        ttls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band, ieee80211w=2, key_mgmt="WPA-EAP-SHA256",
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, vlan_id=vlan)

        assert passes

    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    def test_wpa3_enterprise_5g(self, get_ap_logs, get_lf_logs,
                                station_names_fiveg, lf_test,
                                update_report,
                                test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        ttls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band, ieee80211w=2, key_mgmt="WPA-EAP-SHA256",
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, vlan_id=vlan)

        assert passes


setup_params_enterprise_two = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa_wpa2_enterprise_mixed": [
            {"ssid_name": "tls_ssid_wpa_wpa2_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "tls_ssid_wpa_wpa2_eap_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa3_enterprise_mixed": [
            {"ssid_name": "tls_ssid_wpa3_mixed_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "tls_ssid_wpa3_mixed_eap_5g", "appliedRadios": ["5G"], "vlan": 100}]
    },
    "rf": {},
    "radius": True
}


@pytest.mark.enterprise
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestVLANModeEnterpriseTTLSSuiteTwo(object):

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.twog
    @pytest.mark.amrit
    def test_wpa_wpa2_enterprise_2g(self, get_ap_logs, get_lf_logs,
                                    station_names_twog,  lf_test,
                                    update_report,
                                    test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa_wpa2_enterprise_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "twog"
        vlan = 100
        ttls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, vlan_id=vlan)

        assert passes

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.fiveg
    @pytest.mark.amrit
    def test_wpa_wpa2_enterprise_5g(self,  get_ap_logs,
                                    station_names_fiveg,
                                    lf_test, get_lf_logs,
                                    update_report, test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa_wpa2_enterprise_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        ttls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, vlan_id=vlan)

        assert passes

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.twog
    @pytest.mark.amrit
    def test_wpa3_enterprise_mixed_2g(self,  get_ap_logs, get_lf_logs,
                                      station_names_twog,
                                      lf_test,
                                      update_report, test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa3_enterprise_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "VLAN"
        band = "twog"
        vlan = 100
        ttls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, vlan_id=vlan)

        assert passes

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.fiveg
    @pytest.mark.amrit
    def test_wpa3_enterprise_mixed_5g(self,  get_ap_logs, get_lf_logs,
                                      station_names_fiveg,
                                      lf_test,
                                      update_report, exit_on_fail,
                                      test_cases, radius_info):
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa3_enterprise_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        ttls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, vlan_id=vlan)

        assert passes
