"""

    Client Connectivity Enterprise TTLS
    pytest -m "client_connectivity and nat and enterprise and ttls"

"""
import allure
import pytest

pytestmark = [pytest.mark.nat, pytest.mark.wifi_capacity_ax_tests, pytest.mark.wpa2_enterprise]

setup_params_enterprise_2G = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"]},
        ],
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
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_6
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_enterprise_2G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.twog
class TestWifiCapacityNATModeAX2G(object):
    """ SuiteA Enterprise Test Cases
        pytest -m "client_connectivity_tests and nat and enterprise and ttls and suiteA"
    """
    @pytest.mark.tcp_download
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.title("Single Enterprise AX client TCP Download wifi capacity")
    def test_client_wpa2_eap_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4GHz TCP Download traffic.
        The 2.4GHz station is configured for 20MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and NAT and twog and tcp_download
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
                                                                              dut_data=setup_configuration,cleanup=False,ax_enabled=True,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_nat_tcp_dl_eap",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="NAT-WAN")
            assert True

    @pytest.mark.udp_download
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.decf
    @allure.title("Single Enterprise AX client UDP Download wifi capacity")
    def test_client_wpa2_eap_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4GHz UDP Download traffic.
        The 2.4GHz station is configured for 20MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and NAT and twog and udp_download
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
                                                                              dut_data=setup_configuration,cleanup=False,ax_enabled=True,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_nat_udp_dl_eap",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="NAT-WAN")
            assert True
    
    @pytest.mark.tcp_bidirectional
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.title("Single Enterprise AX client TCP Bidirectional wifi capacity")
    def test_client_wpa2_eap_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4GHz TCP Download and Upload traffic.
        The 2.4GHz station is configured for 20MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and NAT and twog and tcp_bidirectional
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
                                                                              dut_data=setup_configuration,cleanup=False,ax_enabled=True,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_eap_nat_tcp_bidirectional",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="NAT-WAN")
            assert True
    
    @pytest.mark.udp_bidirectional
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.title("Single Enterprise AX client UDP Bidirectional wifi capacity")
    def test_client_wpa2_eap_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4GHz UDP Download and Upload traffic.
        The 2.4GHz station is configured for 20MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and NAT and twog and udp_bidirectional
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
                                                                              dut_data=setup_configuration,cleanup=False,ax_enabled=True,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_eap_nat_udp_bidirectional",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="NAT-WAN")
            assert True
    
    @pytest.mark.udp_upload
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.bcdfiw
    @allure.title("Single Enterprise AX client UDP Upload wifi capacity")
    def test_client_wpa2_eap_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4GHz UDP Upload traffic.
        The 2.4GHz station is configured for 20MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and NAT and twog and udp_upload
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
                                                                              dut_data=setup_configuration,cleanup=False,ax_enabled=True,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_eap_nat_udp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"2G": 1}, mode="NAT-WAN")
            assert True

    @pytest.mark.tcp_upload
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.title("Single Enterprise AX client TCP Upload wifi capacity")
    def test_client_wpa2_eap_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4GHz TCP Upload traffic.
        The 2.4GHz station is configured for 20MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and NAT and twog and tcp_upload
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
                                                                              dut_data=setup_configuration,cleanup=False,ax_enabled=True,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_eap_nat_tcp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"2G": 1}, mode="NAT-WAN")
            assert True
    
setup_params_enterprise_5G = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"]},
        ],
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
@allure.sub_suite("NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_enterprise_5G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.fiveg
class TestWifiCapacityNATModeAX5G(object):
    """ SuiteA Enterprise Test Cases
        pytest -m "client_connectivity_tests and nat and enterprise and ttls and suiteA"
    """
    @pytest.mark.tcp_download
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("Single Enterprise AX client TCP Download wifi capacity")
    def test_client_wpa2_eap_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 5GHz TCP Download traffic.
        The 5GHz station is configured for 80MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and NAT and fiveg and tcp_download
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
                                                                              dut_data=setup_configuration,cleanup=False,ax_enabled=True,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_eap_nat_tcp_dl",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="NAT-WAN")
            assert True

    @pytest.mark.udp_download
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("Single Enterprise AX client UDP Download wifi capacity")
    def test_client_wpa2_eap_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 5GHz UDP Download traffic.
        The 5GHz station is configured for 80MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and NAT and fiveg and udp_download
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
                                                                              dut_data=setup_configuration,cleanup=False,ax_enabled=True,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_eap_nat_udp_dl",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="NAT-WAN")
            assert True
    
    @pytest.mark.tcp_bidirectional
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("Single Enterprise AX client TCP Bidirectional wifi capacity")
    def test_client_wpa2_eap_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 5GHz TCP Download and Upload traffic.
        The 5GHz station is configured for 80MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and NAT and fiveg and tcp_bidirectional
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
                                                                              dut_data=setup_configuration,cleanup=False,ax_enabled=True,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_eap_nat_tcp_bidirectional",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="NAT-WAN")
            assert True
    
    @pytest.mark.udp_bidirectional
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("Single Enterprise AX client UDP Bidirectional wifi capacity")
    def test_client_wpa2_eap_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 5GHz UDP Download and Upload traffic.
        The 5GHz station is configured for 80MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and NAT and fiveg and udp_bidirectional
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
                                                                              dut_data=setup_configuration,cleanup=False,ax_enabled=True,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_eap_nat_udp_bidirectional",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="NAT-WAN")
            assert True
    
    @pytest.mark.udp_upload
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("Single Enterprise AX client UDP Upload wifi capacity")
    def test_client_wpa2_eap_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 5GHz UDP Upload traffic.
        The 5GHz station is configured for 80MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and NAT and fiveg and udp_upload
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
                                                                              dut_data=setup_configuration,cleanup=False,ax_enabled=True,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_eap_nat_udp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"5G": 1}, mode="NAT-WAN")
            assert True
    @pytest.mark.tcp_upload
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.title("Single Enterprise AX client TCP Upload wifi capacity")
    def test_client_wpa2_eap_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity,radius_info):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 5GHz TCP Download traffic.
        The 5GHz station is configured for 80MHz bandwidth, two spatial streams, and WPA2 Enterprise security using TTLS authentication.

        Markers:
        wifi_capacity_ax_tests and wpa2_enterprise and NAT and fiveg and tcp_upload
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
                                                                              dut_data=setup_configuration,cleanup=False,ax_enabled=True,)
        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
            get_test_library.ax_eap_capacity_test(instance_name="test_client_wpa2_eap_nat_tcp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"5G": 1}, mode="NAT-WAN")
            assert True