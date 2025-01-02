"""
    Performance Test: AX Capacity Test : BRIDGE Mode
    pytest -m "wifi_capacity_ax_tests and wpa2_enterprise and bridge"
"""
import pytest
import allure

pytestmark = [pytest.mark.bridge, pytest.mark.wifi_capacity_ax_tests, pytest.mark.wpa2_enterprise]
setup_params_general_2G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_2g_eap", "appliedRadios": ["2G"], "security_key": "something"}
        ]
    },
    "rf": {
        "2G": {
            "band": "2G",
            "channel-width": 20,
            "channel": 6
        }
    },
    "radius": True
}


@allure.feature("Performance Test")
@allure.parent_suite("AX Capacity Test")
@allure.suite("2.4 GHz Band")
@allure.sub_suite("BRIDGE Mode")
@pytest.mark.channel_6
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_2G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.twog
class TestWifiCapacityBRIDGEModeEnterpriseAX2G(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14240", name="WIFI-14240")
    @pytest.mark.tcp_download
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.title("Single Enterprise AX client TCP Download wifi capacity")
    def test_client_wpa2_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4GHz TCP Download traffic.
        The 2.4GHz station is configured for 20MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and bridge and twog and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_eap","security_key": "something","appliedRadios": ["2G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=1,
        dut_data=setup_configuration,
        cleanup=False,
        ax_enabled=True,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_eap_bridge_tcp_dl_eap",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="BRIDGE")
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14243", name="WIFI-14243")
    @pytest.mark.udp_download
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.title("Single Enterprise AX client UDP Download wifi capacity")
    def test_client_wpa2_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                            get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4GHz UDP Download traffic.
        The 2.4GHz station is configured for 20MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and bridge and twog and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_eap","security_key": "something","appliedRadios": ["2G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=1,
        dut_data=setup_configuration,
        cleanup=False,
        ax_enabled=True,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_bridge_udp_dl",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="BRIDGE")
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6940", name="WIFI-6940")
    @pytest.mark.tcp_bidirectional
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.title("Single Enterprise AX client TCP Bidirectional wifi capacity")
    def test_client_wpa2_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,
                                                  get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4GHz TCP Download and Upload traffic.
        The 2.4GHz station is configured for 20MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and bridge and twog and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_eap","security_key": "something","appliedRadios": ["2G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "twog"
        eap = "TTLS"

        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=1,
        dut_data=setup_configuration,
        cleanup=False,
        ax_enabled=True,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_bridge_tcp_bidirectional",
                                          dut_data=setup_configuration,
                                          dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="BRIDGE")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6940", name="WIFI-6940")
    @pytest.mark.udp_bidirectional
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.title("Single Enterprise AX client UDP Bidirectional wifi capacity")
    def test_client_wpa2_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,
                                                  get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4GHz UDP Download and Upload traffic.
        The 2.4GHz station is configured for 20MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and bridge and twog and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_eap","security_key": "something","appliedRadios": ["2G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "twog"
        eap = "TTLS"

        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=1,
        dut_data=setup_configuration,
        cleanup=False,
        ax_enabled=True,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_bridge_udp_bidirectional",
                                          dut_data=setup_configuration,
                                          dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="BRIDGE")
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14241", name="WIFI-14241")
    @pytest.mark.tcp_upload
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.title("Single Enterprise AX client TCP Upload wifi capacity")
    def test_client_wpa2_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4GHz TCP Upload traffic.
        The 2.4GHz station is configured for 20MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and bridge and twog and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_eap","security_key": "something","appliedRadios": ["2G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=1,
        dut_data=setup_configuration,
        cleanup=False,
        ax_enabled=True,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_bridge_tcp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"2G": 1}, mode="BRIDGE")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14242", name="WIFI-14242")
    @pytest.mark.udp_upload
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.title("Single Enterprise AX client UDP Upload wifi capacity")
    def test_client_wpa2_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4GHz UDP Upload traffic.
        The 2.4GHz station is configured for 20MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and bridge and twog and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g_eap","security_key": "something","appliedRadios": ["2G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=1,
        dut_data=setup_configuration,
        cleanup=False,
        ax_enabled=True,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_bridge_udp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"2G": 1}, mode="BRIDGE")
            assert True

setup_params_general_5G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_5g_eap", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "channel-width": 80,
            "channel": 36
        }
    },
    "radius": True
}


@allure.feature("Performance Test")
@allure.parent_suite("AX Capacity Test")
@allure.suite("5 GHz Band")
@allure.sub_suite("BRIDGE Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_5G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.fiveg
class TestWifiCapacityBRIDGEModeAX5G(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14236", name="WIFI-14236")
    @pytest.mark.tcp_download
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("Single Enterprise AX client TCP Download wifi capacity")
    def test_client_wpa2_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 5GHz TCP Download traffic.
        The 5GHz station is configured for 80MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and bridge and fiveg and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_eap","security_key": "something","appliedRadios": ["5G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=1,
        dut_data=setup_configuration,
        cleanup=False,
        ax_enabled=True,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_eap_bridge_tcp_dl_eap",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="BRIDGE")
        assert True

    @allure.testcase(url="  https://telecominfraproject.atlassian.net/browse/WIFI-14237", name="WIFI-14237")
    @pytest.mark.udp_download
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("Single Enterprise AX client UDP Download wifi capacity")
    def test_client_wpa2_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 5GHz UDP Download traffic.
        The 5GHz station is configured for 80MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and bridge and fiveg and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_eap","security_key": "something","appliedRadios": ["5G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=1,
        dut_data=setup_configuration,
        cleanup=False,
        ax_enabled=True,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_bridge_udp_dl",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="BRIDGE")
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6940", name="WIFI-6940")
    @pytest.mark.tcp_bidirectional
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("Single Enterprise AX client TCP Bidirectional wifi capacity")
    def test_client_wpa2_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,
                                                  get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 5GHz TCP Download and Upload traffic.
        The 5GHz station is configured for 80MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and bridge and fiveg and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_eap","security_key": "something","appliedRadios": ["5G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"

        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=1,
        dut_data=setup_configuration,
        cleanup=False,
        ax_enabled=True,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_bridge_tcp_bidirectional",
                                          dut_data=setup_configuration,
                                          dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="BRIDGE")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6940", name="WIFI-6940")
    @pytest.mark.udp_bidirectional
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("Single Enterprise AX client UDP Bidirectional wifi capacity")
    def test_client_wpa2_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,
                                                  get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 5GHz UDP Download and Upload traffic.
        The 5GHz station is configured for 80MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and bridge and fiveg and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_eap","security_key": "something","appliedRadios": ["5G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"

        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=1,
        dut_data=setup_configuration,
        cleanup=False,
        ax_enabled=True,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_bridge_udp_bidirectional",
                                          dut_data=setup_configuration,
                                          dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="BRIDGE")
            assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14238", name="WIFI-14238")
    @pytest.mark.tcp_upload
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("Single Enterprise AX client TCP Upload wifi capacity")
    def test_client_wpa2_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 5GHz TCP Upload traffic.
        The 5GHz station is configured for 80MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and bridge and fiveg and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_eap","security_key": "something","appliedRadios": ["5G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=1,
        dut_data=setup_configuration,
        cleanup=False,
        ax_enabled=True,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_bridge_tcp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"5G": 1}, mode="BRIDGE")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14239", name="WIFI-14239")
    @pytest.mark.udp_upload
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("Single Enterprise AX client UDP Upload wifi capacity")
    def test_client_wpa2_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 5GHz UDP Upload traffic.
        The 5GHz station is configured for 80MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and bridge and fiveg and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_eap","security_key": "something","appliedRadios": ["5G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=1,
        dut_data=setup_configuration,
        cleanup=False,
        ax_enabled=True,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_bridge_udp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"5G": 1}, mode="BRIDGE")
            assert True