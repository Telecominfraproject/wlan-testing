"""
    Performance Test:  Client Scale Test : BRIDGE Mode
    pytest -m "wifi_capacity_client_scale_tests and wpa2_enterprise and bridge"
"""
import pytest
import allure

pytestmark = [pytest.mark.performance, pytest.mark.bridge, pytest.mark.client_scale_tests]
setup_params_general_2G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_2g_eap", "appliedRadios": ["2G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": True
}

@allure.feature("Performance Test")
@allure.parent_suite("Client Scale Test")
@allure.suite("2.4 GHz Band")
@allure.sub_suite("BRIDGE Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_2G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.twog
@pytest.mark.wpa2_enterprise
class TestWifiCapacityEnterpriseBRIDGEMode2G(object):
    @pytest.mark.wpa2_enterprise
    @pytest.mark.tcp_download
    @pytest.mark.twog
    @allure.title("Test for TCP Download 2.4 GHz")
    def test_client_wpa2_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in BRIDGE mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with TCP download traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**: performance, client_scale_tests, bridge, wap2_enterprise, twog,tcp_download
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
        num_sta=max_stations,
        dut_data=setup_configuration,
        cleanup=False,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl_eap", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations},add_stations=False)
        assert True
    
    @pytest.mark.wpa2_enterprise
    @pytest.mark.udp_download
    @pytest.mark.twog
    @allure.title("Test for UDP Download 2.4 GHz")
    def test_client_wpa2_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in BRIDGE mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with UDP download traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**:performance,client_scale_tests, bridge, wpa2_enterprise, twog,udp_download,
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
        num_sta=max_stations,
        dut_data=setup_configuration,
        cleanup=False,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_dl_eap", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations},add_stations=False)
            assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.tcp_bidirectional
    @pytest.mark.twog
    @allure.title("Test for TCP Bidirectional 2.4 GHz")
    def test_client_wpa2_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in BRIDGE mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with TCP download and upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**:performance, client_scale_tests, bridge, wpa2_enterprise, twog, tcp_bidirectional
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
        num_sta=max_stations,
        dut_data=setup_configuration,
        cleanup=False,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_bidirectional_eap", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations},add_stations=False)
            assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.udp_bidirectional
    @pytest.mark.twog
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14329", name="WIFI-14329")
    @allure.title("Test for UDP Bidirectional 2.4 GHz")
    def test_client_wpa2_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in BRIDGE mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with UDP download and upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**:performance, client_scale_tests, bridge, wpa2_enterprise, twog, udp_bidirectional
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
        num_sta=max_stations,
        dut_data=setup_configuration,
        cleanup=False,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_bidirectional_eap", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations},add_stations=False)
            assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.tcp_upload
    @pytest.mark.twog
    @allure.title("Test for TCP Upload 2.4 GHz")
    def test_client_wpa2_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in BRIDGE mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with TCP upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**:performance, client_scale_tests, bridge, wpa2_enterprise, twog, tcp_upload
        """

        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()
        profile_data = {"ssid_name": "ssid_wpa2_2g_eap","security_key": "something","appliedRadios": ["2G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "twog"
        eap = "TTLS"

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=max_stations,
        dut_data=setup_configuration,
        cleanup=False,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_ul_eap", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations},add_stations=False)
            assert True
    
    @pytest.mark.wpa2_enterprise
    @pytest.mark.udp_upload
    @pytest.mark.twog
    @allure.title("Test for UDP Upload 2.4 GHz")
    def test_client_wpa2_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in BRIDGE mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with UDP upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**:performance, client_scale_tests, bridge, wpa2_enterprise, twog, udp_upload
        """

        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()
        profile_data = {"ssid_name": "ssid_wpa2_2g_eap","security_key": "something","appliedRadios": ["2G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "twog"
        eap = "TTLS"

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=max_stations,
        dut_data=setup_configuration,
        cleanup=False,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_ul_eap", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations},add_stations=False)
            assert True



setup_params_general_5G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_5g_eap", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": True
}


@allure.feature("Performance Test")
@allure.parent_suite("Client Scale Test")
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
class TestWifiCapacityEnterpriseBRIDGEMode5G(object):
    @pytest.mark.wpa2_enterprise
    @pytest.mark.tcp_download
    @pytest.mark.fiveg
    @allure.title("Test for TCP Download 5 GHz")
    def test_client_wpa2_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in BRIDGE mode using WPA2 Enterprise security. 
        It focuses on the 5GHz band with TCP download traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**:performance, client_scale_tests, bridge, wpa2_enterprise, fiveg, tcp_download
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
        num_sta=max_stations,
        dut_data=setup_configuration,
        cleanup=False,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl_eap", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations},add_stations=False)
            assert True
    
    @pytest.mark.wpa2_enterprise
    @pytest.mark.udp_download
    @pytest.mark.fiveg
    @allure.title("Test for UDP Download 5 GHz")
    def test_client_wpa2_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in BRIDGE mode using WPA2 Enterprise security. 
        It focuses on the 5GHz band with UDP download traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**:performance, client_scale_tests, bridge, wpa2_enterprise, fiveg, udp_download
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
        num_sta=max_stations,
        dut_data=setup_configuration,
        cleanup=False,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_dl_eap", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations},add_stations=False)
            assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.tcp_bidirectional
    @pytest.mark.fiveg
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14330", name="WIFI-14330")
    @allure.title("Test for TCP Bidirectional 5 GHz")
    def test_client_wpa2_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in BRIDGE mode using WPA2 Enterprise security. 
        It focuses on the 5GHz band with TCP download and upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**:performance, client_scale_tests, bridge, wpa2_enterprise, fiveg, tcp_bidirectional
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
        num_sta=max_stations,
        dut_data=setup_configuration,
        cleanup=False,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_bidirectional;_eap", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations},add_stations=False)
            assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.udp_bidirectional
    @pytest.mark.fiveg
    @allure.title("Test for UDP Bidirectional 5 GHz")
    def test_client_wpa2_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in BRIDGE mode using WPA2 Enterprise security. 
        It focuses on the 5GHz band with UDP download and upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**:performance, client_scale_tests, bridge, wpa2_enterprise, fiveg, udp_bidirectional
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
        num_sta=max_stations,
        dut_data=setup_configuration,
        cleanup=False,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_bidirectional_eap", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations},add_stations=False)
            assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.tcp_upload
    @pytest.mark.fiveg
    @allure.title("Test for TCP Upload 5 GHz")
    def test_client_wpa2_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in BRIDGE mode using WPA2 Enterprise security. 
        It focuses on the 5GHz band with TCP upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**:performance, client_scale_tests, bridge, wpa2_enterprise, fiveg, tcp_upload
        """

        # Pre-test cleanup to ensure a clean state
        profile_data = {"ssid_name": "ssid_wpa2_5g_eap","security_key": "something","appliedRadios": ["5G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=max_stations,
        dut_data=setup_configuration,
        cleanup=False,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_ul_eap", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations},add_stations=False)
            assert True
    
    @pytest.mark.wpa2_enterprise
    @pytest.mark.udp_upload
    @pytest.mark.fiveg
    @allure.title("Test for UDP Upload 2.4 GHz")
    def test_client_wpa2_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in BRIDGE mode using WPA2 Enterprise security. 
        It focuses on the 5GHz band with UDP upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**:performance, client_scale_tests, bridge, wpa2_enterprise, fiveg, tcp_download
        """

        # Pre-test cleanup to ensure a clean state
        get_test_library.pre_cleanup()
        profile_data = {"ssid_name": "ssid_wpa2_5g_eap","security_key": "something","appliedRadios": ["5G"],}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"

        passes, result = get_test_library.enterprise_client_connectivity_test(
        ssid=ssid_name,
        security=security,
        mode=mode,
        band=band,
        eap=eap,
        ttls_passwd="password",
        identity="testing",
        num_sta=max_stations,
        dut_data=setup_configuration,
        cleanup=False,
        )
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_ul_eap", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations},add_stations=False)
            assert True