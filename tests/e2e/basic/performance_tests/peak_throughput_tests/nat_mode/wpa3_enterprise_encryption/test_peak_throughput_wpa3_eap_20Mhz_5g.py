"""

    Performance Test: Country code along with Channel and Channel-width Test: Bridge Mode
    pytest -m "country_code and Bridge"

"""

import allure
import pytest

pytestmark = [pytest.mark.peak_throughput_tests, pytest.mark.nat, pytest.mark.fiveg, pytest.mark.channel_width_20,
              pytest.mark.wpa3_enterprise]

setup_params_general1 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_36", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 20,
            "channel": 36
        }
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHz Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_36
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test20Mhz5GChannel36PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
    def test_client_wpa3_eap_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak Throughput in NAT mode using wpa3 Enterprise security with a 
        5 GHz band 
        and UDP bidirectional traffic. It confirms the client's ability to connect via RADIUS, authenticate 
        using TTLS, and measures throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and NAT and wpa3_enterprise and fiveg and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general2 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_40", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 20,
            "channel": 40}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_40
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test20Mhz5GChannel40PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_40", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_40", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_40", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_40", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_40", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_40", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general3 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_44", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 20,
            "channel": 44}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_44
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general3],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test20Mhz5GChannel44PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_44", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_44", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_44", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_44", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_44", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_44", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general4 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_48", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 20,
            "channel": 48}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_48
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general4],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz5GChannel48PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_48", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_48", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_48", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_48", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_48", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_48", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
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
            'channel-width': 20,
            "channel": 52}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_52
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz5GChannel52PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general6 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_56", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 20,
            "channel": 56}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_56
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general6],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz5GChannel56PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_56", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_56", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_56", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_56", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_56", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_56", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general7 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_60", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 20,
            "channel": 60}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_60
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general7],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz5GChannel60PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
    def test_client_wpa3_eap_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 5 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and fiveg and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
    def test_client_wpa3_eap_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and fiveg and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
    def test_client_wpa3_eap_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP bidirectional traffic. It confirms the client's ability to connect via RADIUS, authenticate 
        using TTLS, and measures throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and fiveg and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
    def test_client_wpa3_eap_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and fiveg and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
    def test_client_wpa3_eap_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and fiveg and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general8 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_2g_64", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 20,
            "channel": 64}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_64
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general8],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz5GChannel64PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_64", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_64", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_64", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_64", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_64", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_64", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
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

            'channel-width': 20,
            "channel": 100}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_100
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general9],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz5GChannel100PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general10 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_104", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 20,
            "channel": 104}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_104
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general10],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz5GChannel104PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_104", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_104", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_104", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_104", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_104", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_104", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general11 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_108", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 20,
            "channel": 108
        }
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_108
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general11],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz5GChannel108PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_108", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_108", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_108", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_108", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_108", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_108", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general12 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_112", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 20,
            "channel": 112}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_112
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general12],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz5GChannel112PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_112", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_112", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_112", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_112", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_112", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_112", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general13 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_116", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 20,
            "channel": 116}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_116
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general13],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz5GChannel116PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_116", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_116", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_116", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_116", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_116", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_116", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
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

            'channel-width': 20,
            "channel": 132}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_114
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general14],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz5GChannel132PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general15 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_136", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 20,
            "channel": 136}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_136
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general15],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz5GChannel136PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_136", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_136", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_136", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_136", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_136", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_136", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general16 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_140", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 20,
            "channel": 140}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general16],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz5GChannel140PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_140", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_140", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_140", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_140", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_140", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_140", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True


setup_params_general17 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_eap_5g_144", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 20,
            "channel": 144}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("peak throughput test")
@allure.suite("5 GHZ Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.channel_144
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general17],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestCountryCA20Mhz5GChannel144PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @allure.title("peak thoughput client TCP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_144", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    @allure.title("peak thoughput enterprise client UDP Download wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_144", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_eap_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    @allure.title("peak thoughput enterprise client TCP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_144", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    @allure.title("peak thoughput enterprise client UDP Bidirectional wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_144", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    @allure.title("peak thoughput enterprise client TCP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_144", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    @allure.title("peak thoughput enterprise client UDP Upload wifi capacity")
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
        profile_data = {"ssid_name": "ssid_wpa3_eap_5g_144", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        security = "wpa3"
        band = "fiveg"
        eap = "TTLS"
        ttls_passwd = radius_info["password"]
        identity=radius_info["user"]
        get_test_library.pre_cleanup()
        passes, result = get_test_library.enterprise_client_connectivity_test(
            ssid=ssid_name,
            security=security,
            mode="NAT-WAN",
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
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1},add_stations=False)
        assert True