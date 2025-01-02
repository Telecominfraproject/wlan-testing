"""

    Client Scale Test TTLS
    pytest -m "client_scale_test and nat and enterprise and ttls"

"""
import allure
import pytest

pytestmark = [pytest.mark.performance, pytest.mark.nat, pytest.mark.client_scale_tests]


setup_params_general_2G = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_enterprise":[
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"]}
        ],
        },

    "rf": {},
    "radius": True
}


@allure.feature("Performance Test")
@allure.parent_suite("Client Scale Test")
@allure.suite("2.4 GHz Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_2G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.twog
@pytest.mark.wpa2_enterprise
class TestWifiCapacityEnterpriseNATMode2G(object):
    @pytest.mark.wpa2_enterprise
    @pytest.mark.tcp_download
    @pytest.mark.twog
    @allure.title("Test for TCP Download 2.4 GHz")
    def test_client_wpa2_eap_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in NAT mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with TCP download traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**: performance, client_scale_tests, nat, wpa2_enterprise, twog, tcp_download
        """                  
        get_test_library.pre_cleanup()  
        profile_data = {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "twog"
        ttls_passwd = "password"
        eap = "TTLS"
        identity = "testing" 
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=num_stations,
                                                                              dut_data=setup_configuration,cleanup=False,)
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
    def test_client_wpa2_eap_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in NAT mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with UDP download traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.
      
        **Markers**: performance, client_scale_tests, nat, wpa2_enterprise, twog, udp_download
        """                  
        get_test_library.pre_cleanup()  
        profile_data = {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "twog"
        ttls_passwd = "password"
        eap = "TTLS"
        identity = "testing" 
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=max_stations,
                                                                              dut_data=setup_configuration,cleanup=False,)
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
    def test_client_wpa2_eap_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in NAT mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with TCP download and upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**: performance, client_scale_tests, nat, wpa2_enterprise, twog, tcp_bidirectional
        """                  
        get_test_library.pre_cleanup()  
        profile_data = {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "twog"
        ttls_passwd = "password"
        eap = "TTLS"
        identity = "testing" 
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=max_stations,
                                                                              dut_data=setup_configuration,cleanup=False,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations},add_stations=False)
            assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.udp_bidirectional
    @pytest.mark.twog
    @allure.title("Test for UDP Bidirectional 2.4 GHz")
    def test_client_wpa2_eap_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in NAT mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with UDP download and upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**: performance, client_scale_tests, nat, wpa2_enterprise, twog, udp_bidirectional
        """                  
        get_test_library.pre_cleanup()  
        profile_data = {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "twog"
        ttls_passwd = "password"
        eap = "TTLS"
        identity = "testing" 
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=max_stations,
                                                                              dut_data=setup_configuration,cleanup=False,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations},add_stations=False)
            assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.tcp_upload
    @pytest.mark.twog
    @allure.title("Test for TCP Upload 2.4 GHz")
    def test_client_wpa2_eap_nat_tcp_upload(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in NAT mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with TCP upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**: performance, client_scale_tests, nat, wpa2_enterprise, twog, tcp_upload
        """                  
        get_test_library.pre_cleanup()  
        profile_data = {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "twog"
        ttls_passwd = "password"
        eap = "TTLS"
        identity = "testing" 
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=max_stations,
                                                                              dut_data=setup_configuration,cleanup=False,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_upload", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations},add_stations=False)
            assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.udp_upload
    @pytest.mark.twog
    @allure.title("Test for UDP Upload 2.4 GHz")
    def test_client_wpa2_eap_nat_udp_upload(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in NAT mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with UDP upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**: performance, client_scale_tests, nat, wpa2_enterprise, twog, udp_upload
        """                  
        get_test_library.pre_cleanup()  
        profile_data = {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "twog"
        ttls_passwd = "password"
        eap = "TTLS"
        identity = "testing" 
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=max_stations,
                                                                              dut_data=setup_configuration,cleanup=False,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_upload", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations},add_stations=False)
            assert True

setup_params_general_5G = {
    "mode": "NAT",
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
@allure.sub_suite("NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_5G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.fiveg
@pytest.mark.wpa2_enterprise
class TestWifiCapacityEnterpriseNATMode5G(object):
    @pytest.mark.wpa2_enterprise
    @pytest.mark.tcp_download
    @pytest.mark.twog
    @allure.title("Test for TCP Download 5 GHz")
    def test_client_wpa2_eap_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in NAT mode using WPA2 Enterprise security. 
        It focuses on the 5GHz band with TCP download traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**: performance, client_scale_tests, nat, wpa2_enterprise, twog, tcp_download
        """                  
        get_test_library.pre_cleanup()  
        profile_data = {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "fiveg"
        ttls_passwd = "password"
        eap = "TTLS"
        identity = "testing" 
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=num_stations,
                                                                              dut_data=setup_configuration,cleanup=False,)
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
    @pytest.mark.twog
    @allure.title("Test for UDP Download 5 GHz")
    def test_client_wpa2_eap_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in NAT mode using WPA2 Enterprise security. 
        It focuses on the 5GHz band with UDP download traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**: performance, client_scale_tests, nat, wpa2_enterprise, twog, udp_download
        """                  
        get_test_library.pre_cleanup()  
        profile_data = {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "fiveg"
        ttls_passwd = "password"
        eap = "TTLS"
        identity = "testing" 
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=max_stations,
                                                                              dut_data=setup_configuration,cleanup=False,)
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
    @pytest.mark.twog
    @allure.title("Test for TCP Bidirectional 5 GHz")
    def test_client_wpa2_eap_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in NAT mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with TCP download and upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**: performance, client_scale_tests, nat, wpa2_enterprise, twog, tcp_bidirectional
        """                  
        get_test_library.pre_cleanup()  
        profile_data = {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "fiveg"
        ttls_passwd = "password"
        eap = "TTLS"
        identity = "testing" 
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=max_stations,
                                                                              dut_data=setup_configuration,cleanup=False,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations},add_stations=False)
            assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.udp_bidirectional
    @pytest.mark.twog
    @allure.title("Test for UDP Bidirectional 5 GHz")
    def test_client_wpa2_eap_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in NAT mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with UDP download and upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**: performance, client_scale_tests, nat, wpa2_enterprise, twog, udp_bidirectional
        """                  
        get_test_library.pre_cleanup()  
        profile_data = {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "twog"
        ttls_passwd = "password"
        eap = "TTLS"
        identity = "testing" 
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=max_stations,
                                                                              dut_data=setup_configuration,cleanup=False,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations},add_stations=False)
            assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.tcp_upload
    @pytest.mark.twog
    @allure.title("Test for TCP Upload 5 GHz")
    def test_client_wpa2_eap_nat_tcp_upload(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in NAT mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with TCP upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**: performance, client_scale_tests, nat, wpa2_enterprise, twog, tcp_upload
        """                  
        get_test_library.pre_cleanup()  
        profile_data = {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "fiveg"
        ttls_passwd = "password"
        eap = "TTLS"
        identity = "testing" 
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=max_stations,
                                                                              dut_data=setup_configuration,cleanup=False,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_upload", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations},add_stations=False)
            assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.udp_upload
    @pytest.mark.twog
    @allure.title("Test for UDP Upload 5 GHz")
    def test_client_wpa2_eap_nat_udp_upload(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info,max_stations):
        """
        Client Scale Test - BRIDGE mode with WPA2 Enterprise Security

        This test evaluates the scalability and performance of a network in NAT mode using WPA2 Enterprise security. 
        It focuses on the 2.4GHz band with UDP upload traffic, validating client connectivity, throughput, and stability 
        as the number of clients increases.

        **Markers**: performance, client_scale_tests, nat, wpa2_enterprise, twog, udp_upload
        """                  
        get_test_library.pre_cleanup()  
        profile_data = {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "fiveg"
        ttls_passwd = "password"
        eap = "TTLS"
        identity = "testing" 
        passes, result = get_test_library.enterprise_client_connectivity_test(ssid=ssid_name, security=security,
                                                                              mode=mode, band=band, eap=eap,
                                                                              ttls_passwd=ttls_passwd,
                                                                              identity=identity, num_sta=max_stations,
                                                                              dut_data=setup_configuration,cleanup=False,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_upload", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations},add_stations=False)
            assert True