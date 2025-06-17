import allure
import pytest

pytestmark = [pytest.mark.client_connectivity_tests, pytest.mark.ow_sanity_lf,
              pytest.mark.bridge, pytest.mark.enterprise, pytest.mark.tls, pytest.mark.uc_sanity]

setup_params_enterprise = {
    "mode": "BRIDGE",
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
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="EAP TLS Client Connectivity : Suite-A")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.uc_sanity
@pytest.mark.usefixtures("setup_configuration")
class TestBridgeModeEnterpriseTLSSuiteA(object):
    """ SuiteA Enterprise Test Cases
            pytest -m "client_connectivity_tests and bridge and enterprise and tls"
        """

    @pytest.mark.wpa_enterprise
    @pytest.mark.twog
    @allure.title("Bridge Mode Client Connectivity Test with WPA-Enterprise-TLS in 2.4GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3742", name="WIFI-3742")
    def test_tls_wpa_enterprise_2g(self, get_test_library, get_dut_logs_per_test_case,
                                   get_test_device_logs,
                                   get_target_object,
                                   num_stations, setup_configuration, check_connectivity, radius_info):
        """
         To verify that a client created on 2G radio connects to AP in Bridge mode with WPA enterprise TLS security
         Unique Marker: pytest -m "client_connectivity_tests and enterprise and wpa_enterprise and ow_sanity_lf and tls and bridge and twog"
                """

        profile_data = {"ssid_name": "tls_ssid_wpa_eap_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
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
    @allure.title("Bridge Mode Client Connectivity Test with WPA-Enterprise-TLS in 5GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3743", name="WIFI-3743")
    def test_tls_wpa_enterprise_5g(self, get_test_library, get_dut_logs_per_test_case,
                                   get_test_device_logs,
                                   get_target_object,
                                   num_stations, setup_configuration, check_connectivity, radius_info):
        """
        To verify that a client created on 5G radio connects to AP in Bridge mode with WPA enterprise TLS security
        Unique Marker: pytest -m "client_connectivity_tests and enterprise and wpa_enterprise and ow_sanity_lf and tls and bridge and fiveg"
                """

        profile_data = {"ssid_name": "tls_ssid_wpa_eap_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
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
    @allure.title("Bridge Mode Client Connectivity Test with WPA2-Enterprise-TLS in 2.4GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3739", name="WIFI-3739")
    def test_tls_wpa2_enterprise_2g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """
        To verify that a client created on 2G radio connects to AP in Bridge mode with WPA2 enterprise TLS security
        Unique Marker: pytest -m "client_connectivity_tests and enterprise and wpa2_enterprise and ow_sanity_lf and tls and bridge and twog"
                """

        profile_data = {"ssid_name": "tls_ssid_wpa2_eap_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "BRIDGE"
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
    @allure.title("Bridge Mode Client Connectivity Test with WPA2-Enterprise-TLS in 5GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3713", name="WIFI-3713")
    def test_tls_wpa2_enterprise_5g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """
        To verify that a client created on 5G radio connects to AP in Bridge mode with WPA2 enterprise TLS security
        Unique Marker: pytest -m "client_connectivity_tests and enterprise and wpa2_enterprise and ow_sanity_lf and tls and bridge and fiveg"
                """

        profile_data = {"ssid_name": "tls_ssid_wpa2_eap_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "BRIDGE"
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
    @allure.title("Bridge Mode Client Connectivity Test with WPA3-Enterprise-TLS in 2.4GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3736", name="WIFI-3736")
    def test_tls_wpa3_enterprise_2g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """
        To verify that a client created on 2G radio connects to AP in Bridge mode with WPA3 enterprise TLS security
                 Unique Marker: pytest -m "To verify that a client created on 2G radio connects to AP in Bridge mode with WPA3 enterprise TLS security"
                """

        profile_data = {"ssid_name": "tls_ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "BRIDGE"
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
    @allure.title("Bridge Mode Client Connectivity Test with WPA3-Enterprise-TLS in 5GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3734", name="WIFI-3734")
    def test_tls_wpa3_enterprise_5g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """
        To verify that a client created on 5G radio connects to AP in Bridge mode with WPA3 enterprise TLS security
        Unique Marker: pytest -m "client_connectivity_tests and enterprise and wpa3_enterprise and ow_sanity_lf and tls and bridge and fiveg"
                """

        profile_data = {"ssid_name": "tls_ssid_wpa3_eap_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "BRIDGE"
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
    "mode": "BRIDGE",
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
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="EAP TLS Client Connectivity : Suite-B")
@pytest.mark.suiteB
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_enterprise_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestBridgeModeEnterpriseTLSSuiteTwo(object):
    """ SuiteA Enterprise Test Cases
        pytest -m "client_connectivity_tests and bridge and enterprise and ttls and suiteB"
    """

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.twog
    @allure.title("Bridge Mode Client Connectivity Test with WPA-WPA2-Enterprise-TLS in 2.4GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10589", name="WIFI-10589")
    def test_wpa_wpa2_enterprise_2g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """
        To verify that a client created on 2G radio connects to AP in Bridge mode with WPA-WPA2-Enterprise  TLS security
          Unique Marker:  pytest -m "client_connectivity_tests and wpa_wpa2_enterprise_mixed and enterprise and ow_sanity_lf and tls and bridge and twog"
        """
        profile_data = {"ssid_name": "tls_ssid_wpa_wpa2_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
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
    @allure.title("Bridge Mode Client Connectivity Test with WPA-WPA2-Enterprise-TLS in 5GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10590", name="WIFI-10590")
    def test_wpa_wpa2_enterprise_5g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """
               To verify that a client created on 5G radio connects to AP in Bridge mode with WPA-WPA2-Enterprise  TLS security
                 Unique Marker:  pytest -m "client_connectivity_tests and wpa_wpa2_enterprise_mixed and enterprise and ow_sanity_lf and tls and bridge and fiveg"
               """
        profile_data = {"ssid_name": "tls_ssid_wpa_wpa2_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
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
    @allure.title("Bridge Mode Client Connectivity Test with WPA3-Enterprise-Mixed-TLS in 2.4GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10591", name="WIFI-10591")
    def test_wpa3_enterprise_mixed_2g(self, get_test_library, get_dut_logs_per_test_case,
                                      get_test_device_logs,
                                      get_target_object,
                                      num_stations, setup_configuration, check_connectivity, radius_info):
        """
                       To verify that a client created on 2G radio connects to AP in Bridge mode with WPA3-Enterprise-Mixed  TLS security
                         Unique Marker: pytest -m "client_connectivity_tests and wpa3_enterprise_mixed and enterprise and ow_sanity_lf and tls and bridge and twog"
                       """
        profile_data = {"ssid_name": "tls_ssid_wpa3_mixed_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "BRIDGE"
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
    @allure.title("Bridge Mode Client Connectivity Test with WPA3-Enterprise-Mixed-TLS in 5GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10592", name="WIFI-10592")
    def test_wpa3_enterprise_mixed_5g(self, get_test_library, get_dut_logs_per_test_case,
                                      get_test_device_logs,
                                      get_target_object,
                                      num_stations, setup_configuration, check_connectivity, radius_info):
        """
         To verify that a client created on 5G radio connects to AP in Bridge mode with WPA3-Enterprise-Mixed  TLS security
         Unique Marker: pytest -m "client_connectivity_tests and wpa3_enterprise_mixed and enterprise and ow_sanity_lf and tls and bridge and fiveg"
                              """
        profile_data = {"ssid_name": "tls_ssid_wpa3_mixed_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "BRIDGE"
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



setup_params_enterprise_6G = {
        "mode": "BRIDGE",
        "ssid_modes": {
            "wpa3_enterprise": [
                {"ssid_name": "tls_ssid_wpa3_eap_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "tls_ssid_wpa3_eap_6g", "appliedRadios": ["6G"], "security_key": "something"}
            ]
        },
        "rf": {
            "6G": {
            "band": "6G",
            "channel-mode": "EHT",
            "channel-width": 80,
                }
        },
        "radius": True
}
@allure.parent_suite("Client Connectivity Tests")
@allure.feature("Client Connectivity")
@allure.suite(suite_name="BRIDGE Mode")
@allure.sub_suite(sub_suite_name="EAP TLS Client Connectivity : Suite-B")
@pytest.mark.parametrize(
        'setup_configuration',
        [setup_params_enterprise_6G],
        indirect=True,
        scope="class"
)
@pytest.mark.uc_sanity
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.wpa3_enterprise
@pytest.mark.twog
class TestBridgeModeEnterpriseTLSSuiteC(object):
    """ SuiteB Enterprise Test Cases
            pytest -m "client_connectivity_tests and bridge and enterprise and tls"
    """

    @pytest.mark.wpa3_enterprise
    @pytest.mark.sixg
    @allure.title("Bridge Mode Client Connectivity Test with WPA3-Enterprise-TLS in 6GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14369", name="WIFI-14369")
    def test_tls_wpa3_enterprise_6g(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs,
                                    get_target_object,
                                    num_stations, setup_configuration, check_connectivity, radius_info):
        """
        To verify that a client created on 6G radio connects to AP in Bridge mode with WPA3 enterprise TLS security
        Unique Marker: pytest -m "client_connectivity_tests and enterprise and wpa3_enterprise and ow_sanity_lf and tls and bridge and sixg"
                """

        profile_data = {"ssid_name": "tls_ssid_wpa3_eap_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "sixg"
        tls_passwd = radius_info["password"]
        eap = "TLS"
        key_mgmt = "WPA-EAP-SHA256"
        identity = radius_info['user']
        pk_passwd = radius_info['pk_password']
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=tls_passwd,
                                                                              identity=identity, num_sta=num_stations,
                                                                              key_mgmt=key_mgmt, pk_passwd=pk_passwd,
                                                                              dut_data=setup_configuration)

        assert passes == "PASS", result
