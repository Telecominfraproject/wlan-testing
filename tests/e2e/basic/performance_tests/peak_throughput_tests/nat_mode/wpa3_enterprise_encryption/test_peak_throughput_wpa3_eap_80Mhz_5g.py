"""

    Performance Test: Country code along with Channel and Channel-width Test: Bridge Mode
    pytest -m "country_code and Bridge"

"""

import allure
import pytest


pytestmark = [pytest.mark.peak_throughput_tests, pytest.mark.nat, pytest.mark.fiveg, pytest.mark.channel_width_80,
              pytest.mark.wpa3_enterprise]

setup_params_general1 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_36", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 40,
            "channel": 36
        }
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_36
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test80Mhz5GChannel36PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @pytest.mark.aaa
    def test_client_wpa3_eap_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_eap_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_eap_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_eap_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_eap_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_eap_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general5 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_52", "appliedRadios": ["5G"], "security_key": "something"}]
    },
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 40,
            "channel": 52}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_52
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test80Mhz5GChannel52PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa3_eap_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_eap_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_eap_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_eap_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_eap_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_eap_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general9 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 40,
            "channel": 100}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_100
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general9],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test80Mhz5GChannel100PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa3_eap_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_eap_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_eap_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_eap_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_eap_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_eap_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general14 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 40,
            "channel": 132}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_132
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general14],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test80Mhz5GChannel132PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa3_eap_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_eap_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_eap_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_eap_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_eap_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_eap_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="BRIDGE",
            band=band,
            eap=eap,
            ttls_passwd=ttls_passwd,
            identity=identity,
            num_sta=1,
            dut_data=setup_configuration,
            cleanup=False,
            key_mgmt="WPA-EAP-SHA256"
        )

        if passes != "PASS":
            assert passes == "PASS", result
        if passes == "PASS":
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True
