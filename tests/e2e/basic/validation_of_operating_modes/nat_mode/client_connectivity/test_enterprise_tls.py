import allure
import pytest

pytestmark = [pytest.mark.client_connectivity_tests,
              pytest.mark.nat, pytest.mark.enterprise, pytest.mark.tls, pytest.mark.uc_sanity]

setup_params_enterprise = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa_enterprise": [
            {"ssid_name": "tls_ssid_wpa_eap_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "tls_ssid_wpa_eap_5g", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa2_enterprise": [
            {"ssid_name": "tls_ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "tls_ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "security_key": "something"}],
        "wpa3_enterprise": [
            {"ssid_name": "tls_ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "tls_ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "security_key": "something"}]},

    "rf": {},
    "radius": True
}


@allure.parent_suite("Client Connectivity Tests")
@allure.feature("Client Connectivity")
@allure.suite(suite_name="NAT Mode")
@allure.sub_suite(sub_suite_name="EAP TLS Client Connectivity : Suite-A")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.uc_sanity
@pytest.mark.usefixtures("setup_configuration")
class TestNATModeEnterpriseTLSSuiteA(object):
    """ SuiteA Enterprise Test Cases
            pytest -m "client_connectivity_tests and nat and enterprise and tls"
        """

    @pytest.mark.wpa_enterprise
    @pytest.mark.twog
    @allure.title("Test for wpa enterprise 2.4 GHz")
    def test_tls_wpa_enterprise_2g(self, get_test_library, get_dut_logs_per_test_case,
                                   get_test_device_logs, execution_number,
                                   get_target_object,
                                   num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
                    pytest -m "client_connectivity_tests and nat and enterprise and tts and twog"
                """

        profile_data = {"ssid_name": "tls_ssid_wpa_eap_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        if execution_number == 0:
            mode = "NAT-WAN"
        if execution_number == 1:
            mode = "NAT-LAN"
        band = "twog"
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        pk_passwd = radius_info['pk_password']
        # pk_passwd = radcius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              extra_securities=extra_secu,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=tls_passwd,
                                                                              identity=identity, num_sta=num_stations,
                                                                              key_mgmt=key_mgmt, pk_passwd=pk_passwd,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result

    @pytest.mark.wpa_enterprise
    @pytest.mark.fiveg
    @allure.title("Test for wpa enterprise 5 GHz")
    def test_tls_wpa_enterprise_5g(self, get_test_library, get_dut_logs_per_test_case,
                                   get_test_device_logs, execution_number,
                                   get_target_object,
                                   num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
                    pytest -m "client_connectivity_tests and nat and enterprise and tts and twog"
                """

        profile_data = {"ssid_name": "tls_ssid_wpa_eap_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        if execution_number == 0:
            mode = "NAT-WAN"
        if execution_number == 1:
            mode = "NAT-LAN"
        band = "fiveg"
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        pk_passwd = radius_info['pk_password']
        # pk_passwd = radcius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              extra_securities=extra_secu,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=tls_passwd,
                                                                              identity=identity, num_sta=num_stations,
                                                                              key_mgmt=key_mgmt, pk_passwd=pk_passwd,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.title("Test for wpa2 enterprise 2.4 GHz")
    def test_tls_wpa2_enterprise_2g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, execution_number,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
                    pytest -m "client_connectivity_tests and nat and enterprise and tls and twog"
                """

        profile_data = {"ssid_name": "tls_ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        if execution_number == 0:
            mode = "NAT-WAN"
        if execution_number == 1:
            mode = "NAT-LAN"
        band = "twog"
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        pk_passwd = radius_info['pk_password']
        # pk_passwd = radius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=tls_passwd,
                                                                              identity=identity, num_sta=num_stations,
                                                                              key_mgmt=key_mgmt, pk_passwd=pk_passwd,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("Test for wpa2 enterprise 5 GHz")
    def test_tls_wpa2_enterprise_5g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, execution_number,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
                    pytest -m "client_connectivity_tests and nat and enterprise and tts and twog"
                """

        profile_data = {"ssid_name": "tls_ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        if execution_number == 0:
            mode = "NAT-WAN"
        if execution_number == 1:
            mode = "NAT-LAN"
        band = "fiveg"
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP"
        identity = radius_info['user']
        pk_passwd = radius_info['pk_password']
        # pk_passwd = radius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=tls_passwd,
                                                                              identity=identity, num_sta=num_stations,
                                                                              key_mgmt=key_mgmt, pk_passwd=pk_passwd,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    @allure.title("Test for wpa3 enterprise 2.4 GHz")
    def test_tls_wpa3_enterprise_2g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, execution_number,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
                    pytest -m "client_connectivity_tests and nat and enterprise and tts and twog"
                """

        profile_data = {"ssid_name": "tls_ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        if execution_number == 0:
            mode = "NAT-WAN"
        if execution_number == 1:
            mode = "NAT-LAN"
        band = "twog"
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP-SHA256"
        identity = radius_info['user']
        pk_passwd = radius_info['pk_password']
        # pk_passwd = radius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=tls_passwd,
                                                                              identity=identity, num_sta=num_stations,
                                                                              key_mgmt=key_mgmt, pk_passwd=pk_passwd,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    @allure.title("Test for wpa3 enterprise 5 GHz")
    def test_tls_wpa3_enterprise_5g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, execution_number,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 5g
                    pytest -m "client_connectivity_tests and nat and enterprise and tts and twog"
                """

        profile_data = {"ssid_name": "tls_ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        if execution_number == 0:
            mode = "NAT-WAN"
        if execution_number == 1:
            mode = "NAT-LAN"
        band = "fiveg"
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP-SHA256"
        identity = radius_info['user']
        pk_passwd = radius_info['pk_password']
        # pk_passwd = radius_info['pk_password']
        # lf_tools.add_vlan(vlan)
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=tls_passwd,
                                                                              identity=identity, num_sta=num_stations,
                                                                              key_mgmt=key_mgmt, pk_passwd=pk_passwd,
                                                                              dut_data=setup_configuration)

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


@allure.parent_suite("Client Connectivity Tests")
@allure.feature("Client Connectivity")
@allure.suite(suite_name="NAT Mode")
@allure.sub_suite(sub_suite_name="EAP TLS Client Connectivity : Suite-B")
@pytest.mark.suiteB
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_enterprise_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestNATModeEnterpriseTLSSuiteTwo(object):
    """ SuiteA Enterprise Test Cases
        pytest -m "client_connectivity_tests and nat and enterprise and ttls and suiteB"
    """

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.twog
    @allure.title("Test for wpa wpa2 enterprise 2.4 GHz")
    def test_wpa_wpa2_enterprise_2g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, execution_number,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
            pytest -m "client_connectivity_tests and NAT and enterprise and ttls and wpa_wpa2_enterprise_mixed and twog"
        """
        profile_data = {"ssid_name": "tls_ssid_wpa_wpa2_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        if execution_number == 0:
            mode = "NAT-WAN"
        if execution_number == 1:
            mode = "NAT-LAN"
        band = "twog"
        tls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        pk_passwd = radius_info['pk_password']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              extra_securities=extra_secu,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=tls_passwd, pk_passwd=pk_passwd,
                                                                              identity=identity, num_sta=num_stations,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.fiveg
    @allure.title("Test for wpa wpa2 enterprise 5 GHz")
    def test_wpa_wpa2_enterprise_5g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, execution_number,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
            pytest -m "client_connectivity_tests and nat and enterprise and ttls and wpa_wpa2_enterprise_mixed and fiveg"
        """
        profile_data = {"ssid_name": "tls_ssid_wpa_wpa2_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        if execution_number == 0:
            mode = "NAT-WAN"
        if execution_number == 1:
            mode = "NAT-LAN"
        band = "fiveg"
        tls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        pk_passwd = radius_info['pk_password']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              extra_securities=extra_secu,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=tls_passwd, pk_passwd=pk_passwd,
                                                                              identity=identity, num_sta=num_stations,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.twog
    @allure.title("Test for wpa3 enterprise mixed 2.4 GHz")
    def test_wpa3_enterprise_mixed_2g(self, get_test_library, get_dut_logs_per_test_case,
                                      get_test_device_logs, execution_number,
                                      get_target_object,
                                      num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
            pytest -m "client_connectivity_tests and nat and enterprise and ttls and wpa3_enterprise_mixed and twog"
        """
        profile_data = {"ssid_name": "tls_ssid_wpa3_mixed_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        if execution_number == 0:
            mode = "NAT-WAN"
        if execution_number == 1:
            mode = "NAT-LAN"
        band = "twog"
        tls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        pk_passwd = radius_info['pk_password']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=tls_passwd, pk_passwd=pk_passwd,
                                                                              identity=identity, num_sta=num_stations,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.fiveg
    @allure.title("Test for wpa3 enterprise mixed 5 GHz")
    def test_wpa3_enterprise_mixed_5g(self, get_test_library, get_dut_logs_per_test_case,
                                      get_test_device_logs, execution_number,
                                      get_target_object,
                                      num_stations, setup_configuration, check_connectivity, radius_info):
        """ wpa enterprise 2g
            pytest -m "client_connectivity_tests and nat and enterprise and ttls and wpa3_enterprise_mixed and fiveg"
        """
        profile_data = {"ssid_name": "tls_ssid_wpa3_mixed_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        if execution_number == 0:
            mode = "NAT-WAN"
        if execution_number == 1:
            mode = "NAT-LAN"
        band = "fiveg"
        tls_passwd = radius_info["password"]
        eap = "TLS"
        identity = radius_info['user']
        pk_passwd = radius_info['pk_password']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=tls_passwd, pk_passwd=pk_passwd,
                                                                              identity=identity, num_sta=num_stations,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result
