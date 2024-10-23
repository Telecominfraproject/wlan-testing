"""

    Performance Test: Country code along with Channel and Channel-width Test: Bridge Mode
    pytest -m "country_code and Bridge"

"""

import allure
import pytest

pytestmark = [pytest.mark.peak_throughput_tests, pytest.mark.bridge, pytest.mark.twog, pytest.mark.channel_width_40,
              pytest.mark.wpa3_enterprise]

setup_params_general_1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_enterprise_2g_1", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 40,
            "channel": 1
        }
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_1
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz2GChannel1PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa3_enterprise_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_1", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_station=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_enterprise_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_1", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_enterprise_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_1", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_enterprise_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput uisng in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP bidirectional traffic. It confirms the client's ability to connect via RADIUS, authenticate 
        using TTLS, and measures throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_1", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_enterprise_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_1", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_enterprise_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_1", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True


setup_params_general_2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_enterprise_2g_2", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 40,
            "channel": 2
        }
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_2
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz2GChannel2PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa3_enterprise_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak throughput uisng in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_2", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_enterprise_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_2", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_enterprise_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_2", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_enterprise_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP bidirectional traffic. It confirms the client's ability to connect via RADIUS, authenticate 
        using TTLS, and measures throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_2", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_enterprise_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_2", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_enterprise_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_2", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True


setup_params_general_3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_enterprise_2g_3", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 40,
            "channel": 3
        }
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_3
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_3],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz2GChannel3PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa3_enterprise_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_3", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_enterprise_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_3", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_enterprise_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_3", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_enterprise_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP bidirectional traffic. It confirms the client's ability to connect via RADIUS, authenticate 
        using TTLS, and measures throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_3", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_enterprise_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_3", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_enterprise_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_3", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True


setup_params_general_4 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_enterprise_2g_4", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 40,
            "channel": 4
        }
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_3
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_4],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz2GChannel4PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa3_enterprise_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_4", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_enterprise_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_4", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_enterprise_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_4", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_enterprise_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP bidirectional traffic. It confirms the client's ability to connect via RADIUS, authenticate 
        using TTLS, and measures throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_4", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_enterprise_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_4", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_enterprise_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_4", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True


setup_params_general_5 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_enterprise_2g_5", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 40,
            "channel": 4
        }
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_3
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz2GChannel5PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa3_enterprise_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak throughput uisng in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_5", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_enterprise_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_5", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_enterprise_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_5", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_enterprise_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP bidirectional traffic. It confirms the client's ability to connect via RADIUS, authenticate 
        using TTLS, and measures throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_5", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_enterprise_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_5", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_enterprise_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_5", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True


setup_params_general_6 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_enterprise_2g_6", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 40,
            "channel": 6
        }
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_6
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz2GChannel6PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa3_enterprise_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_6", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_enterprise_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_6", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_enterprise_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_6", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_enterprise_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput uisng in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP bidirectional traffic. It confirms the client's ability to connect via RADIUS, authenticate 
        using TTLS, and measures throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_6", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_enterprise_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_6", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_enterprise_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_6", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True


setup_params_general_7 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_enterprise_2g_7", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',

            'channel-width': 40,
            "channel": 7}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_7
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_7],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz2GChannel7PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @pytest.mark.aaa
    def test_client_wpa3_enterprise_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_7", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_enterprise_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_7", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_enterprise_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_7", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_enterprise_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP bidirectional traffic. It confirms the client's ability to connect via RADIUS, authenticate 
        using TTLS, and measures throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_7", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_enterprise_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_7", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_enterprise_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_7", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True


setup_params_general_8 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_enterprise_2g_8", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 40,
            "channel": 8}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_8
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_8],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz2GChannel8PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa3_enterprise_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_8", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_enterprise_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_8", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_enterprise_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_8", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_enterprise_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP bidirectional traffic. It confirms the client's ability to connect via RADIUS, authenticate 
        using TTLS, and measures throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_8", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_enterprise_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_8", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_enterprise_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_8", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True


setup_params_general_9 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_enterprise_2g_9", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',

            'channel-width': 40,
            "channel": 9}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_9
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_9],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz2GChannel9PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @pytest.mark.aaa
    def test_client_wpa3_enterprise_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_9", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_enterprise_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_9", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_enterprise_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_9", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_enterprise_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP bidirectional traffic. It confirms the client's ability to connect via RADIUS, authenticate 
        using TTLS, and measures throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_9", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_enterprise_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_9", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_enterprise_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_9", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True


setup_params_general_10 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_enterprise_2g_10", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 40,
            "channel": 10}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_10
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_10],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz2GChannel10PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa3_enterprise_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_enterprise_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_enterprise_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_enterprise_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP bidirectional traffic. It confirms the client's ability to connect via RADIUS, authenticate 
        using TTLS, and measures throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_enterprise_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_enterprise_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True


setup_params_general_11 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_enterprise": [{"ssid_name": "ssid_wpa3_enterprise_2g_11", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 40,
            "channel": 11}
    },
    "radius": True
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_11
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_11],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz2GChannel11PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa3_enterprise_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks the Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP download traffic. It ensures that the client can connect to the AP via RADIUS, authenticate with 
        TTLS, and measures the throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa3_enterprise_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP download traffic. The client connects via RADIUS, authenticates using TTLS, and measures the 
        throughput with 1Gbps download and 0Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_download
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE" 
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa3_enterprise_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test assesses Peak throughput uisng Wi-Fi capacity  in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP bidirectional traffic. It verifies that the client can connect via RADIUS and authenticate 
        using TTLS, measuring throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa3_enterprise_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP bidirectional traffic. It confirms the client's ability to connect via RADIUS, authenticate 
        using TTLS, and measures throughput with 1Gbps download and upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_bidirectional
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa3_enterprise_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test checks Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and TCP upload traffic. It ensures that the client connects via RADIUS, authenticates with TTLS, and 
        measures the upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and tcp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa3_enterprise_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,radius_info):
        """
        Test Description:
        This test evaluates Peak throughput in BRIDGE mode using WPA3 Enterprise security with a 2.4 GHz band 
        and UDP upload traffic. It confirms that the client connects via RADIUS, authenticates with TTLS, and 
        measures upload throughput with 0Gbps download and 1Gbps upload.

        Unique Marker:
        wifi_capacity_test and BRIDGE and wpa3_enterprise and twog and udp_upload
        """
        profile_data = {"ssid_name": "ssid_wpa3_enterprise_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        band="twog"           
        eap = "TTLS"
        security = "wpa3"
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
            get_test_library.wifi_capacity(instance_name="test_client_wpa3_enterprise_bridge_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1},add_stations=False)
        assert True
