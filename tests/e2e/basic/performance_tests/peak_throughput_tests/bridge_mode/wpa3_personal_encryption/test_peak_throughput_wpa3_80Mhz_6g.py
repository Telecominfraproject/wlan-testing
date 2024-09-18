"""

    Performance Test: Single client Wifi capacity with Channel and Channel-width Test: Bridge Mode
    pytest -m "peak_throughput_tests and bridge"

"""

import allure
import pytest

pytestmark = [pytest.mark.peak_throughput_tests, pytest.mark.bridge, pytest.mark.sixg, pytest.mark.channel_width_80,
              pytest.mark.wpa3_personal]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [{"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
                          ]},
    "rf": {
        "6G": {
            'band': '6G',
            'channel-width': 80}
    },
    "radius": False
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("Throughput Benchmark Test")
@allure.suite("6 GHz Band")
@allure.sub_suite("BRIDGE Mode")

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.wpa3_personal
@pytest.mark.sixg
@pytest.mark.sixg_band
# @pytest.mark.performance
@pytest.mark.usefixtures("setup_configuration")
class Test80Mhz6GChannelautoPeakThroughput(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10500", name="WIFI-10500")
    @pytest.mark.tcp_download
    @pytest.mark.jkkk
    @allure.title("Single client TCP Download wifi capacity 80Mhz Bw")
    def test_client_wpa3_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Single client Wifi Capacity Test BRIDGE mode
            pytest -m "peak_throughput_tests and sixg and tcp_download and bridge and channel_width_80"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_bridge_tcp_download", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="56Kbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10509", name="WIFI-10509")
    @pytest.mark.udp_download
    @allure.title("Single client UDP Download wifi capacity 80Mhz Bw")
    def test_client_wpa3_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Single client Wifi Capacity Test BRIDGE mode
            pytest -m "peak_throughput_tests and sixg and udp_download and bridge and channel_width_80"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_bridge_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="56Kbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12385", name="WIFI-12385")
    @pytest.mark.tcp_bidirectional
    @allure.title("Single client TCP Bidirectional wifi capacity 80Mhz Bw")
    def test_client_wpa3_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Single client Wifi Capacity Test BRIDGE mode
            pytest -m "peak_throughput_tests and sixg and udp_download and bridge and channel_width_80"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_bridge_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12384", name="WIFI-12384")
    @pytest.mark.udp_bidirectional
    @allure.title("Single client UDP Bidirectional wifi capacity 80Mhz Bw")
    def test_client_wpa3_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Single client Wifi Capacity Test BRIDGE mode
            pytest -m "peak_throughput_tests and sixg and udp_bidirectional and bridge and channel_width_80"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_bridge_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10499", name="WIFI-10499")
    @pytest.mark.tcp_upload
    @allure.title("Single client TCP Upload wifi capacity 80Mhz Bw")
    def test_client_wpa3_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Single client Wifi Capacity Test BRIDGE mode
            pytest -m "peak_throughput_tests and sixg and tcp_upload and bridge and channel_width_80"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_bridge_tcp_ul", mode=mode,
                                       download_rate="56Kbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7942", name="WIFI-7942")
    @pytest.mark.udp_upload
    @allure.title("Single client UDP Upload wifi capacity 80Mhz Bw")
    def test_client_wpa3_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Single client Wifi Capacity Test BRIDGE mode
            pytest -m "peak_throughput_tests and sixg and udp_upload and bridge and channel_width_80"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_bridge_udp_ul", mode=mode,
                                       download_rate="56Kbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1})
        assert True
