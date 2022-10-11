"""

    Client Connectivity Enterprise TTLS
    pytest -m "client_connectivity and vlan and enterprise and ttls"

"""
import allure
import pytest

pytestmark = [pytest.mark.ow_client_connectivity_lf, pytest.mark.vlan, pytest.mark.enterprise, pytest.mark.ttls,
              pytest.mark.ucentral, pytest.mark.sanity, pytest.mark.uc_sanity]

setup_params_enterprise = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa_enterprise": [
            {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa_eap_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "vlan": 100}]},

    "rf": {},
    "radius": True
}


@allure.parent_suite("OpenWifi Client Connectivity")
@allure.suite(suite_name="VLAN Mode")
@allure.sub_suite(sub_suite_name="EAP TTLS Client Connectivity : Suite-A")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestVLANModeEnterpriseTTLSSuiteA(object):
    """ SuiteA Enterprise Test Cases
        pytest -m "ow_client_connectivity_lf and vlan and enterprise and ttls and suiteA"
    """

    @pytest.mark.wpa_enterprise
    @pytest.mark.twog
    @allure.title("Test for wpa enterprise 2.4 GHz")
    def test_wpa_enterprise_2g(self, get_test_library, get_dut_logs_per_test_case,
                               get_test_device_logs,
                               get_target_object,
                               num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
            pytest -m "client_conow_client_connectivity_lfnectivity and vlan and enterprise and ttls and wpa_enterprise and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["2G"], "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              extra_securities=extra_secu,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=1,
                                                                              vlan_id=vlan,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result

    @pytest.mark.wpa_enterprise
    @pytest.mark.fiveg
    @allure.title("Test for wpa enterprise 5 GHz")
    def test_wpa_enterprise_5g(self, get_test_library, get_dut_logs_per_test_case,
                               get_test_device_logs,
                               get_target_object,
                               num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 5g
            pytest -m "ow_client_connectivity_lf and vlan and enterprise and ttls and wpa_enterprise and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa_eap_5g", "appliedRadios": ["5G"], "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              extra_securities=extra_secu,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=1,
                                                                              vlan_id=vlan,
                                                                              dut_data=setup_configuration)
        assert passes == "PASS", result

    @pytest.mark.sanity_light
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.title("Test for wpa2 enterprise 2.4 GHz")
    def test_wpa2_enterprise_2g(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs,
                                get_target_object,
                                num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
            pytest -m "ow_client_connectivity_lf and vlan and enterprise and ttls and wpa2_enterprise and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=1,
                                                                              vlan_id=vlan,
                                                                              dut_data=setup_configuration)
        assert passes == "PASS", result

    @pytest.mark.sanity_light
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("Test for wpa2 enterprise 5 GHz")
    def test_wpa2_enterprise_5g(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs,
                                get_target_object,
                                num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
            pytest -m "ow_client_connectivity_lf and vlan and enterprise and ttls and wpa2_enterprise and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=1,
                                                                              vlan_id=vlan,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    @allure.title("Test for wpa3 enterprise 2.4 GHz")
    def test_wpa3_enterprise_2g(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs,
                                get_target_object,
                                num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
            pytest -m "ow_client_connectivity_lf and vlan and enterprise and ttls and wpa3_enterprise and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=1,
                                                                              vlan_id=vlan,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    @allure.title("Test for wpa3 enterprise 5 GHz")
    def test_wpa3_enterprise_5g(self, get_test_library, get_dut_logs_per_test_case,
                                get_test_device_logs,
                                get_target_object,
                                num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
            pytest -m "ow_client_connectivity_lf and vlan and enterprise and ttls and wpa3_enterprise and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=1,
                                                                              vlan_id=vlan,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result


setup_params_enterprise_two = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa_wpa2_enterprise_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa_wpa2_eap_5g", "appliedRadios": ["5G"], "vlan": 100}],
        "wpa3_enterprise_mixed": [
            {"ssid_name": "ssid_wpa3_mixed_eap_2g", "appliedRadios": ["2G"], "vlan": 100},
            {"ssid_name": "ssid_wpa3_mixed_eap_5g", "appliedRadios": ["5G"], "vlan": 100}]
    },
    "rf": {},
    "radius": True
}


@allure.parent_suite("OpenWifi Client Connectivity")
@allure.suite(suite_name="VLAN Mode")
@allure.sub_suite(sub_suite_name="EAP TTLS Client Connectivity : Suite-B")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_enterprise_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestVLANModeEnterpriseTTLSSuiteTwo(object):
    """ SuiteA Enterprise Test Cases
        pytest -m "ow_client_connectivity_lf and vlan and enterprise and ttls and suiteB"
    """

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.twog
    @allure.title("Test for wpa wpa2 enterprise 2.4 GHz")
    def test_wpa_wpa2_enterprise_2g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
            pytest -m "ow_client_connectivity_lf and vlan and enterprise and ttls and wpa_wpa2_enterprise_mixed and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa_wpa2_eap_2g", "appliedRadios": ["2G"], "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              extra_securities=extra_secu,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=1,
                                                                              vlan_id=vlan,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.fiveg
    @allure.title("Test for wpa wpa2 enterprise 5 GHz")
    def test_wpa_wpa2_enterprise_5g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
            pytest -m "client_connow_client_connectivity_lfectivity and vlan and enterprise and ttls and wpa_wpa2_enterprise_mixed and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa_wpa2_eap_5g", "appliedRadios": ["5G"], "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              extra_securities=extra_secu,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=1,
                                                                              vlan_id=vlan,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.twog
    @allure.title("Test for wpa3 enterprise mixed 2.4 GHz")
    def test_wpa3_enterprise_mixed_2g(self, get_test_library, get_dut_logs_per_test_case,
                                      get_test_device_logs,
                                      get_target_object,
                                      num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
            pytest -m "ow_client_connectivity_lf and vlan and enterprise and ttls and wpa3_enterprise_mixed and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa3_mixed_eap_2g", "appliedRadios": ["2G"], "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "VLAN"
        band = "twog"
        vlan = [100]
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=1,
                                                                              vlan_id=vlan,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.fiveg
    @allure.title("Test for wpa3 enterprise mixed 5 GHz")
    def test_wpa3_enterprise_mixed_5g(self, get_test_library, get_dut_logs_per_test_case,
                                      get_test_device_logs,
                                      get_target_object,
                                      num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
            pytest -m "ow_client_connectivity_lf and vlan and enterprise and ttls and wpa3_enterprise_mixed and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa3_mixed_eap_5g", "appliedRadios": ["5G"], "vlan": 100}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "VLAN"
        band = "fiveg"
        vlan = [100]
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=1,
                                                                              vlan_id=vlan,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result
