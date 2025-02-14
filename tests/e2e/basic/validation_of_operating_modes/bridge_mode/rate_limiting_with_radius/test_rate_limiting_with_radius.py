"""
Rate LImiting with radius Bridge Mode Scenario
"""
import time

import allure
import pytest
import importlib

lf_library = importlib.import_module("configuration")
RATE_LIMITING_RADIUS_SERVER_DATA = {
    "ip": "10.28.3.21",
    "port": 1812,
    "secret": "testing123",
    "user": "bandwidth10m",
    "password": "password",
    "pk_password": "whatever"
}
RATE_LIMITING_RADIUS_ACCOUNTING_DATA = {
    "ip": "10.28.3.21",
    "port": 1813,
    "secret": "testing123",
    "user": "bandwidth10m",
    "password": "password",
    "pk_password": "whatever"
}

pytestmark = [pytest.mark.rate_limiting_with_radius_tests,
              pytest.mark.bridge, pytest.mark.ow_regression_lf]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_2g_br",
             "appliedRadios": ["2G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 20,
                 "egress-rate": 20
             },
             "radius_auth_data": RATE_LIMITING_RADIUS_SERVER_DATA,
             "radius_acc_data": RATE_LIMITING_RADIUS_ACCOUNTING_DATA

             },
            {"ssid_name": "ssid_wpa2_5g_br",
             "appliedRadios": ["5G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 20,
                 "egress-rate": 20
             },
             "radius_auth_data": RATE_LIMITING_RADIUS_SERVER_DATA,
             "radius_acc_data": RATE_LIMITING_RADIUS_ACCOUNTING_DATA
             }
        ]
    },
    "rf": {},
    "radius": True
}


@allure.feature("Rate Limiting With Radius Test")
@allure.parent_suite("Rate Limiting With Radius Test")
@allure.suite("BRIDGE Mode")
@allure.sub_suite("WPA2 Enterprise Security")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestRateLimitingWithRadiusBridge(object):

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.twog_upload_per_ssid
    @allure.title("Test for Upload per SSID 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5849", name="WIFI-5849")
    def test_radius_server_2g_upload_per_ssid(self, get_test_library, get_dut_logs_per_test_case,
                                              get_test_device_logs,
                                              get_target_object,
                                              num_stations, setup_configuration, rate_radius_info,
                                              rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "bandwidth10m"
        configured = profile_data["rate-limit"]["ingress-rate"]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            obj = get_test_library.wifi_capacity(instance_name="Test_Radius_2g_up_per_ssid", mode=mode,
                                                 download_rate="0Gbps", batch_size="1",
                                                 upload_rate="1Gbps", protocol="TCP", duration="60000",
                                                 move_to_influx=False, dut_data=setup_configuration,
                                                 ssid_name=ssid_name,
                                                 add_stations=False, raw_lines=raw_lines)
            report_name = obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1] + "/"
            kpi_data = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
            achieved = float("{:.2f}".format(kpi_data[1][0]))
            if achieved <= configured:
                assert True
            else:
                assert False, f"Expected Throughput should be less than {configured} Mbps"

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.twog_download_perssid_persta
    @pytest.mark.ow_sanity_lf
    @allure.title("Test for TCP Download per SSID per Station 2.4GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5850", name="WIFI-5850")
    def test_radius_server_2g_download_perssid_persta(self, get_test_library, get_dut_logs_per_test_case,
                                                      get_test_device_logs,
                                                      get_target_object,
                                                      num_stations, setup_configuration, rate_radius_info,
                                                      rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "bandwidth10m"
        configured = profile_data["rate-limit"]["egress-rate"]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel:  Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            obj = get_test_library.wifi_capacity(instance_name="Test_Radius_2g_down_perssid_persta", mode=mode,
                                                 download_rate="1Gbps", batch_size="1",
                                                 upload_rate="0Gbps", protocol="TCP", duration="60000",
                                                 move_to_influx=False, dut_data=setup_configuration,
                                                 ssid_name=ssid_name,
                                                 add_stations=False, raw_lines=raw_lines)
            report_name = obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1] + "/"
            kpi_data = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
            achieved = float("{:.2f}".format(kpi_data[0][0]))
            if achieved <= configured:
                assert True
            else:
                assert False, f"Expected Throughput should be less than {configured} Mbps"

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.twog_upload_persta_perclient
    @allure.title("Test for Upload per station per client 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5851", name="WIFI-5851")
    @allure.title("Test for Upload per station per client 2.4GHz")
    def test_radius_server_2g_upload_persta_perclient_rate(self, get_test_library, get_dut_logs_per_test_case,
                                                           get_test_device_logs,
                                                           get_target_object,
                                                           num_stations, setup_configuration, rate_radius_info,
                                                           rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "bandwidth10m"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel:  Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Test_Radius_2g_up_perssid_persta", mode=mode,
                                           download_rate="0Gbps", batch_size="1",
                                           upload_rate="2.488Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.twog_upload_download_persta_perclient
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5852", name="WIFI-5852")
    @allure.title("Test for Upload Download per station per client 2.4GHz")
    def test_radius_server_2g_upload_download_persta_perclient_rate(self, get_test_library, get_dut_logs_per_test_case,
                                                                    get_test_device_logs,
                                                                    get_target_object,
                                                                    num_stations, setup_configuration, rate_radius_info,
                                                                    rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "bandwidth10m"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel:  Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Test_Radius_2g_up_down_per_per_client", mode=mode,
                                           download_rate="1Gbps", batch_size="1",
                                           upload_rate="1Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.fiveg_download_per_ssid
    @allure.title("Test for Download per SSID 5 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5853", name="WIFI-5853")
    def test_radius_server_fiveg_per_ssid_download(self, get_test_library, get_dut_logs_per_test_case,
                                                   get_test_device_logs,
                                                   get_target_object,
                                                   num_stations, setup_configuration, rate_radius_info,
                                                   rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "bandwidth10m"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Test_Radius_5g_down_per_ssid", mode=mode,
                                           download_rate="1Gbps", batch_size="1",
                                           upload_rate="0Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.fiveg_upload_per_ssid
    @pytest.mark.ow_sanity_lf
    @allure.title("Test for UDP Upload per SSID 5 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5854", name="WIFI-5854")
    def test_radius_server_fiveg_per_ssid_upload(self, get_test_library, get_dut_logs_per_test_case,
                                                 get_test_device_logs,
                                                 get_target_object,
                                                 num_stations, setup_configuration, rate_radius_info,
                                                 rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "user"
        configured = 5
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            obj = get_test_library.wifi_capacity(instance_name="Test_Radius_5g_up_per_ssid", mode=mode,
                                           download_rate="0Gbps", batch_size="1",
                                           upload_rate="1Gbps", protocol="UDP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)
            report_name = obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1] + "/"
            kpi_data = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
            achieved = float("{:.2f}".format(kpi_data[1][0]))
            if achieved <= configured:
                assert True
            else:
                assert False, f"Expected Throughput should be less than {configured} Mbps"


    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.fiveg_download_per_ssid_per_client
    @allure.title("Test for Download per SSID per client 5 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5855", name="WIFI-5855")
    def test_radius_server_fiveg_per_ssid_perclient_download(self, get_test_library, get_dut_logs_per_test_case,
                                                             get_test_device_logs,
                                                             get_target_object,
                                                             num_stations, setup_configuration, rate_radius_info,
                                                             rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "bandwidth10m"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel:  Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Test_Radius_5g_down_per_ssid_perclient", mode=mode,
                                           download_rate="1Gbps", batch_size="1",
                                           upload_rate="0Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.fiveg_upstream_per_ssid_per_client
    @allure.title("Test for Upload per SSID per client 5 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5856", name="WIFI-5856")
    def test_radius_server_fiveg_per_ssid_perclient_upstream(self, get_test_library, get_dut_logs_per_test_case,
                                                             get_test_device_logs,
                                                             get_target_object,
                                                             num_stations, setup_configuration, rate_radius_info,
                                                             rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "bandwidth10m"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel:  Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Test_Radius_5g_upstream_per_ssid_perclient", mode=mode,
                                           download_rate="0Gbps", batch_size="1",
                                           upload_rate="1Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.fiveg_upstream__downstream_per_ssid_per_client
    @allure.title("Test for Upload Download per SSID per client 5 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5857", name="WIFI-5857")
    def test_radius_server_fiveg_per_ssid_perclient_upstream_downstream(self, get_test_library,
                                                                        get_dut_logs_per_test_case,
                                                                        get_test_device_logs,
                                                                        get_target_object,
                                                                        num_stations, setup_configuration,
                                                                        rate_radius_info,
                                                                        rate_radius_accounting_info,
                                                                        check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "bandwidth10m"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel:  Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Test_Radius_5g_upstream_downstream_per_ssid_perclient",
                                           mode=mode,
                                           download_rate="1Gbps", batch_size="1",
                                           upload_rate="1Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.twog_per_ssid
    @allure.title("Test for per SSID 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5858", name="WIFI-5858")
    def test_radius_server_2g_per_ssid(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs,
                                       get_target_object,
                                       num_stations, setup_configuration, rate_radius_info,
                                       rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "bandwidth10m"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Total Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Test_Radius_2g_per_ssid",
                                           mode=mode,
                                           download_rate="0Gbps", batch_size="1",
                                           upload_rate="1Gbps", protocol="TCP and UDP IPv4", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.fiveg_per_ssid
    @allure.title("Test for per SSID 5 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5860", name="WIFI-5860")
    def test_radius_server_fiveg_per_ssid(self, get_test_library, get_dut_logs_per_test_case,
                                          get_test_device_logs,
                                          get_target_object,
                                          num_stations, setup_configuration, rate_radius_info,
                                          rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "bandwidth10m"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel:  Per-Station Upload Rate:"]]
            get_test_library.wifi_capacity(instance_name="Test_Radius_5g_per_ssid",
                                           mode=mode,
                                           download_rate="1Gbps", batch_size="1",
                                           upload_rate="0Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.twog_per_ssid_per_client
    @allure.title("Test for per SSID per client 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5862", name="WIFI-5862")
    def test_radius_server_2g_per_ssid_per_client(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs,
                                                  get_target_object,
                                                  num_stations, setup_configuration, rate_radius_info,
                                                  rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "bandwidth10m"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Per-Station Download Rate:"], ["ul_rate_sel: Per-Station Upload Rate:"]]
            get_test_library.wifi_capacity(instance_name="Test_Radius_2g_per_ssid_per_client",
                                           mode=mode,
                                           download_rate="1Gbps", batch_size="1",
                                           upload_rate="1Gbps", protocol="TCP and UDP IPv4", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.fiveg_per_ssid_per_client
    @allure.title("Test for per SSID per client 5 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5864", name="WIFI-5864")
    def test_radius_server_fiveg_per_ssid_per_client(self, get_test_library, get_dut_logs_per_test_case,
                                                     get_test_device_logs,
                                                     get_target_object,
                                                     num_stations, setup_configuration, rate_radius_info,
                                                     rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_5g_br",
                        "appliedRadios": ["5G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "bandwidth10m"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Upload Rate:"]]
            get_test_library.wifi_capacity(instance_name="Test_Radius_5g_per_ssid_per_client",
                                           mode=mode,
                                           download_rate="1Gbps", batch_size="1",
                                           upload_rate="0Gbps", protocol="TCP and UDP IPv4", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.twog_per_ssid_down
    @allure.title("Test for Download per SSID 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5868", name="WIFI-5868")
    def test_radius_server_2g_per_ssid_downstream(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs,
                                                  get_target_object,
                                                  num_stations, setup_configuration, rate_radius_info,
                                                  rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "bandwidth10m"
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Total Upload Rate:"]]
            get_test_library.wifi_capacity(instance_name="Test_Radius_2g",
                                           mode=mode,
                                           download_rate="1Gbps", batch_size="1",
                                           upload_rate="0Gbps", protocol="TCP and UDP IPv4", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        assert True

    @pytest.mark.twog
    @pytest.mark.max_upload_user1
    @pytest.mark.wpa2_enterprise
    @allure.title("Test for max upload group user1 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7618", name="WIFI-7618")
    def test_radius_server_ratelimit_maxupload_groupuser1_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                             get_test_device_logs,
                                                             get_target_object,
                                                             num_stations, setup_configuration, rate_radius_info,
                                                             rate_radius_accounting_info, check_connectivity):
        """
            Test: check max-upload ratelimit of group - user1
            pytest -m "wpa2_enterprise and twog and max_upload_user1"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = 'password'
        identity = 'user1'
        configured = 10
        allure.attach(name="Max-Upload-User1", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Ratelimit_Radius_group_user1",
                                           mode=mode,
                                           download_rate="0Gbps", batch_size="1",
                                           upload_rate="1Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        #     kpi_data = lf_tools.read_kpi_file(column_name=["short-description", "numeric-score"], dir_name=report_name)
        #     print(kpi_data)
        #     achieved = float("{:.2f}".format(kpi_data[1][1]))
        #     allure.attach(name="Check PASS/FAIL information", body=f"Configured WISPr Bandwidth for Max Upload for "
        #                                                            f"user1: {configured} Mbps \nAchieved throughput "
        #                                                            f"via Test: {achieved} Mbps")
        #     lf_tools.attach_report_graphs(report_name=report_name)
        #     print("Test Completed... Cleaning up Stations")
        #     if float(achieved) != float(0) and (achieved <= configured):
        #         assert True
        #     else:
        #         assert False, f"Expected Throughput should be less than {configured} Mbps"
        # else:
        #     assert False, "EAP Connect Failed"

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.max_download_user1
    @allure.title("Test for max download group user1 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7619", name="WIFI-7619")
    def test_radius_server_ratelimit_maxdownload_groupuser1_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                               get_test_device_logs,
                                                               get_target_object,
                                                               num_stations, setup_configuration, rate_radius_info,
                                                               rate_radius_accounting_info, check_connectivity):
        """
            Test: check max-download ratelimit of group - user1
            pytest -m "wpa2_enterprise and twog and max_download_user1"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 20,
                            "egress-rate": 30
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = 'password'
        identity = 'user1'
        configured = 10
        allure.attach(name="Max-Download-User1", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Ratelimit_Radius_group_user1",
                                           mode=mode,
                                           download_rate="1Gbps", batch_size="1",
                                           upload_rate="0Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        #     kpi_data = lf_tools.read_kpi_file(column_name=["short-description", "numeric-score"], dir_name=report_name)
        #     print(kpi_data)
        #     achieved = float("{:.2f}".format(kpi_data[0][1]))
        #     allure.attach(name="Check PASS/FAIL information", body=f"Configured WISPr Bandwidth for Max Download for "
        #                                                            f"user1: {configured} Mbps \nAchieved throughput "
        #                                                            f"via Test: {achieved} Mbps")
        #     lf_tools.attach_report_graphs(report_name=report_name)
        #     print("Test Completed... Cleaning up Stations")
        #     if float(achieved) != float(0) and (achieved <= configured):
        #         assert True
        #     else:
        #         assert False, f"Expected Throughput should be less than {configured} Mbps"
        # else:
        #     assert False, "EAP Connect Failed"

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.max_upload_user2
    @allure.title("Test for max upload group user2 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7620", name="WIFI-7620")
    def test_radius_server_ratelimit_maxupload_groupuser2_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                             get_test_device_logs,
                                                             get_target_object,
                                                             num_stations, setup_configuration, rate_radius_info,
                                                             rate_radius_accounting_info, check_connectivity):
        """
            Test: check max-upload ratelimit of group - user2
            pytest -m "wpa2_enterprise and twog and max_upload_user2"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 60,
                            "egress-rate": 50
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = 'password'
        identity = 'user2'
        configured = 20
        allure.attach(name="Max-Upload-User2", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Ratelimit_Radius_group_user2",
                                           mode=mode,
                                           download_rate="0Gbps", batch_size="1",
                                           upload_rate="1Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        #     kpi_data = lf_tools.read_kpi_file(column_name=["short-description", "numeric-score"], dir_name=report_name)
        #     print(kpi_data)
        #     achieved = float("{:.2f}".format(kpi_data[1][1]))
        #     allure.attach(name="Check PASS/FAIL information", body=f"Configured WISPr Bandwidth for Max Upload for "
        #                                                            f"user2: {configured} Mbps \nAchieved throughput "
        #                                                            f"via Test: {achieved} Mbps")
        #     lf_tools.attach_report_graphs(report_name=report_name)
        #     print("Test Completed... Cleaning up Stations")
        #     if float(achieved) != float(0) and (achieved <= configured):
        #         assert True
        #     else:
        #         assert False, f"Expected Throughput should be less than {configured} Mbps"
        # else:
        #     assert False, "EAP Connect Failed"

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.max_download_user2
    @allure.title("Test for max download group user2 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7621", name="WIFI-7621")
    def test_radius_server_ratelimit_maxdownload_groupuser2_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                               get_test_device_logs,
                                                               get_target_object,
                                                               num_stations, setup_configuration, rate_radius_info,
                                                               rate_radius_accounting_info, check_connectivity):
        """
                    Test: check max-download ratelimit of group - user2
                    pytest -m "wpa2_enterprise and twog and max_download_user2"
                """
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 60,
                            "egress-rate": 50
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = 'password'
        identity = 'user2'
        configured = 20
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        allure.attach(name="Max-Download-User2", body=str(profile_data["rate-limit"]))
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Ratelimit_Radius_group_user2",
                                           mode=mode,
                                           download_rate="1Gbps", batch_size="1",
                                           upload_rate="0Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        #     kpi_data = lf_tools.read_kpi_file(column_name=["short-description", "numeric-score"], dir_name=report_name)
        #     print(kpi_data)
        #     achieved = float("{:.2f}".format(kpi_data[0][1]))
        #     allure.attach(name="Check PASS/FAIL information", body=f"Configured WISPr Bandwidth for Max Upload for "
        #                                                            f"user2: {configured} Mbps \nAchieved throughput "
        #                                                            f"via Test: {achieved} Mbps")
        #     lf_tools.attach_report_graphs(report_name=report_name)
        #     print("Test Completed... Cleaning up Stations")
        #     if float(achieved) != float(0) and (achieved <= configured):
        #         assert True
        #     else:
        #         assert False, f"Expected Throughput should be less than {configured} Mbps"
        # else:
        #     assert False, "EAP Connect Failed"

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.max_upload_user3
    @allure.title("Test for max upload group user3 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7622", name="WIFI-7622")
    def test_radius_server_ratelimit_maxupload_groupuser3_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                             get_test_device_logs,
                                                             get_target_object,
                                                             num_stations, setup_configuration, rate_radius_info,
                                                             rate_radius_accounting_info, check_connectivity):
        """
            Test: check max-download ratelimit of group - user3
            pytest -m "wpa2_enterprise and twog and max_upload_user3"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 50,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = 'password'
        identity = 'user3'
        configured = 10
        allure.attach(name="Max-Upload-User3", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Ratelimit_Radius_group_user2",
                                           mode=mode,
                                           download_rate="0Gbps", batch_size="1",
                                           upload_rate="1Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)
        #     kpi_data = lf_tools.read_kpi_file(column_name=["short-description", "numeric-score"], dir_name=report_name)
        #     print(kpi_data)
        #     achieved = float("{:.2f}".format(kpi_data[1][1]))
        #     allure.attach(name="Check PASS/FAIL information", body=f"Configured WISPr Bandwidth for Max Upload for "
        #                                                            f"user3: {configured} Mbps \nAchieved throughput "
        #                                                            f"via Test: {achieved} Mbps")
        #     lf_tools.attach_report_graphs(report_name=report_name)
        #     print("Test Completed... Cleaning up Stations")
        #     if float(achieved) != float(0) and (achieved <= configured):
        #         assert True
        #     else:
        #         assert False, f"Expected Throughput should be less than {configured} Mbps"
        # else:
        #     assert False, "EAP Connect Failed"

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.max_download_user3
    @allure.title("Test for max download group user3 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7623", name="WIFI-7623")
    def test_radius_server_ratelimit_maxdownload_groupuser3_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                               get_test_device_logs,
                                                               get_target_object,
                                                               num_stations, setup_configuration, rate_radius_info,
                                                               rate_radius_accounting_info, check_connectivity):
        """
            Test: check max-download ratelimit of group - user3
            pytest -m "wpa2_enterprise and twog and max_download_user3"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 50,
                            "egress-rate": 10
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = 'password'
        identity = 'user3'
        configured = 50
        allure.attach(name="Max-Download-User3", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Ratelimit_Radius_group_user3",
                                           mode=mode,
                                           download_rate="1Gbps", batch_size="1",
                                           upload_rate="0Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        #     kpi_data = lf_tools.read_kpi_file(column_name=["short-description", "numeric-score"], dir_name=report_name)
        #     print(kpi_data)
        #     achieved = float("{:.2f}".format(kpi_data[0][1]))
        #     allure.attach(name="Check PASS/FAIL information", body=f"Configured WISPr Bandwidth for Max Download for "
        #                                                            f"user1: {configured} Mbps \nAchieved throughput "
        #                                                            f"via Test: {achieved} Mbps")
        #     lf_tools.attach_report_graphs(report_name=report_name)
        #     print("Test Completed... Cleaning up Stations")
        #     if float(achieved) != float(0) and (achieved <= configured):
        #         assert True
        #     else:
        #         assert False, f"Expected Throughput should be less than {configured} Mbps"
        # else:
        #     assert False, "EAP Connect Failed"

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.max_upload_user4
    @allure.title("Test for max upload group user4 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7624", name="WIFI-7624")
    def test_radius_server_ratelimit_maxupload_groupuser4_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                             get_test_device_logs,
                                                             get_target_object,
                                                             num_stations, setup_configuration, rate_radius_info,
                                                             rate_radius_accounting_info, check_connectivity):
        """
            Test: check max-upload ratelimit of group - user4
            pytest -m "wpa2_enterprise and twog and max_upload_user4"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 50
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = 'password'
        identity = 'user4'
        configured = 50
        allure.attach(name="Max-Upload-User4", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Ratelimit_Radius_group_user4",
                                           mode=mode,
                                           download_rate="0Gbps", batch_size="1",
                                           upload_rate="1Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        #     kpi_data = lf_tools.read_kpi_file(column_name=["short-description", "numeric-score"], dir_name=report_name)
        #     print(kpi_data)
        #     achieved = float("{:.2f}".format(kpi_data[1][1]))
        #     allure.attach(name="Check PASS/FAIL information", body=f"Configured WISPr Bandwidth for Max Upload for "
        #                                                            f"user4: {configured} Mbps \nAchieved throughput "
        #                                                            f"via Test: {achieved} Mbps")
        #     lf_tools.attach_report_graphs(report_name=report_name)
        #     print("Test Completed... Cleaning up Stations")
        #     if float(achieved) != float(0) and (achieved <= configured):
        #         assert True
        #     else:
        #         assert False, f"Expected Throughput should be less than {configured} Mbps"
        # else:
        #     assert False, "EAP Connect Failed"

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.max_download_user4
    @allure.title("Test for max download group user4 2.4 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7625", name="WIFI-7625")
    def test_radius_server_ratelimit_maxdownload_groupuser4_2g(self, get_test_library, get_dut_logs_per_test_case,
                                                               get_test_device_logs,
                                                               get_target_object,
                                                               num_stations, setup_configuration, rate_radius_info,
                                                               rate_radius_accounting_info, check_connectivity):
        """
            Test: check max-download ratelimit of group - user4
            pytest -m "wpa2_enterprise and twog and max_download_user4"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_br",
                        "appliedRadios": ["2G"],
                        "security_key": "something",
                        "rate-limit": {
                            "ingress-rate": 10,
                            "egress-rate": 50
                        }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = 'password'
        identity = 'user4'
        configured = 10
        allure.attach(name="Max-Download-User4", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            get_test_library.wifi_capacity(instance_name="Ratelimit_Radius_group_user4",
                                           mode=mode,
                                           download_rate="1Gbps", batch_size="1",
                                           upload_rate="0Gbps", protocol="TCP", duration="60000",
                                           move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                           add_stations=False, raw_lines=raw_lines)

        #     kpi_data = lf_tools.read_kpi_file(column_name=["short-description", "numeric-score"], dir_name=report_name)
        #     print(kpi_data)
        #     achieved = float("{:.2f}".format(kpi_data[0][1]))
        #     allure.attach(name="Check PASS/FAIL information", body=f"Configured WISPr Bandwidth for Max Download for "
        #                                                            f"user4: {configured} Mbps \nAchieved throughput "
        #                                                            f"via Test: {achieved} Mbps")
        #     lf_tools.attach_report_graphs(report_name=report_name)
        #     print("Test Completed... Cleaning up Stations")
        #     if float(achieved) != float(0) and (achieved <= configured):
        #         assert True
        #     else:
        #         assert False, f"Expected Throughput should be less than {configured} Mbps"
        # else:
        #     assert False, "EAP Connect Failed"

setup_params_general_sixg = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa2_2g_br",
             "appliedRadios": ["2G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 10,
                 "egress-rate": 10
             },
             "radius_auth_data": RATE_LIMITING_RADIUS_SERVER_DATA,
             "radius_acc_data": RATE_LIMITING_RADIUS_ACCOUNTING_DATA

             },
            {"ssid_name": "ssid_wpa2_6g_br",
             "appliedRadios": ["6G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 5,
                 "egress-rate": 5
             },
             "radius_auth_data": RATE_LIMITING_RADIUS_SERVER_DATA,
             "radius_acc_data": RATE_LIMITING_RADIUS_ACCOUNTING_DATA
             }
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

@allure.feature("Rate Limiting With Radius Test")
@allure.parent_suite("Rate Limiting With Radius Test")
@allure.suite("BRIDGE Mode")
@allure.sub_suite("WPA3 Enterprise Security")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_sixg],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.wpa3_enterprise
@pytest.mark.twog
class TestRateLimitingWithRadiusBridgeSixg(object):

    @pytest.mark.wpa3_enterprise
    @pytest.mark.sixg
    @pytest.mark.sixg_upload_per_ssid
    @pytest.mark.ow_sanity_lf
    @allure.title("Test for UDP Upload per SSID 6 GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14366", name="WIFI-14366")
    def test_radius_server_6g_upload_per_ssid(self, get_test_library, get_dut_logs_per_test_case,
                                              get_test_device_logs,
                                              get_target_object,
                                              num_stations, setup_configuration, rate_radius_info,
                                              rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_6g_br",
             "appliedRadios": ["6G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 5,
                 "egress-rate": 5
             }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa3"
        band = "sixg"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "user"
        configured = profile_data["rate-limit"]["ingress-rate"]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False, key_mgmt="WPA-EAP-SHA256")

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            obj = get_test_library.wifi_capacity(instance_name="Test_Radius_2g_up_per_ssid", mode=mode,
                                                 download_rate="0Gbps", batch_size="1",
                                                 upload_rate="1Gbps", protocol="UDP", duration="60000",
                                                 move_to_influx=False, dut_data=setup_configuration,
                                                 ssid_name=ssid_name,
                                                 add_stations=False, raw_lines=raw_lines)
            report_name = obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1] + "/"
            kpi_data = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
            achieved = float("{:.2f}".format(kpi_data[1][0]))
            if achieved <= configured:
                assert True
            else:
                assert False, f"Expected Throughput should be less than {configured} Mbps"

    @pytest.mark.wpa3_enterprise
    @pytest.mark.sixg
    @pytest.mark.sixg_download_perssid_persta
    @pytest.mark.ow_sanity_lf
    @allure.title("Test for TCP Download per Station 6GHz")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14365", name="WIFI-14365")
    def test_radius_server_6g_download_persta(self, get_test_library, get_dut_logs_per_test_case,
                                                      get_test_device_logs,
                                                      get_target_object,
                                                      num_stations, setup_configuration, rate_radius_info,
                                                      rate_radius_accounting_info, check_connectivity):
        profile_data = {"ssid_name": "ssid_wpa2_6g_br",
             "appliedRadios": ["6G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 5,
                 "egress-rate": 5
             }}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        security = "wpa3"
        band = "sixg"
        eap = "TTLS"
        ttls_passwd = "password"
        identity = "user"
        configured = profile_data["rate-limit"]["egress-rate"]
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd, ieee80211w=0,
                                                                              identity=identity, num_sta=1,
                                                                              dut_data=setup_configuration,
                                                                              cleanup=False, key_mgmt="WPA-EAP-SHA256")
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            raw_lines = [["dl_rate_sel:  Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            obj = get_test_library.wifi_capacity(instance_name="Test_Radius_2g_down_perssid_persta", mode=mode,
                                                 download_rate="1Gbps", batch_size="1",
                                                 upload_rate="0Gbps", protocol="TCP", duration="60000",
                                                 move_to_influx=False, dut_data=setup_configuration,
                                                 ssid_name=ssid_name,
                                                 add_stations=False, raw_lines=raw_lines)
            report_name = obj[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1] + "/"
            kpi_data = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
            achieved = float("{:.2f}".format(kpi_data[0][0]))
            if achieved <= configured:
                assert True
            else:
                assert False, f"Expected Throughput should be less than {configured} Mbps"