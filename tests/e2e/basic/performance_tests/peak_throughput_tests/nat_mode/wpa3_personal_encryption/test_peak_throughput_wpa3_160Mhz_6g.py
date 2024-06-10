"""

    Performance Test: Single client Wifi capacity with Channel and Channel-width Test: nat Mode
    pytest -m "peak_throughput_tests and nat"

"""

import allure
import pytest

pytestmark = [pytest.mark.peak_throughput_tests, pytest.mark.nat, pytest.mark.sixg, pytest.mark.channel_width_160,
              pytest.mark.wpa3_personal]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
            ]},
    "rf": {
        "6G": {
            'band': '6G',
            'channel-width': 160}
    },
    "radius": False
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("Throughput Benchmark Test")
@allure.suite("6 GHz Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.wpa3_personal
@pytest.mark.twog
@pytest.mark.performance
@pytest.mark.usefixtures("setup_configuration")
class Test160Mhz6GChannelautoPeakThroughput(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12400", name="WIFI-12400")
    @pytest.mark.tcp_download
    @pytest.mark.sixg
    @allure.title("Single client TCP Download wifi capacity 160Mhz Bw")
    def test_client_wpa3_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration):
        """ Single client Wifi Capacity Test nat mode
            pytest -m "peak_throughput_tests and sixg and tcp_download and nat and channel_width_160"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_nat_tcp_download", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="56Kbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1}, pass_fail_criteria=True)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12401", name="WIFI-12401")
    @pytest.mark.udp_download
    @pytest.mark.sixg
    @allure.title("Single client UDP Download wifi capacity 160Mhz Bw")
    def test_client_wpa3_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration):
        """ Single client Wifi Capacity Test nat mode
            pytest -m "peak_throughput_tests and sixg and udp_download and nat and channel_width_160"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_nat_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="56Kbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1}, pass_fail_criteria=True)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12403", name="WIFI-12403")
    @pytest.mark.tcp_bidirectional
    @pytest.mark.sixg
    @allure.title("Single client TCP Bidirectional wifi capacity 160Mhz Bw")
    def test_client_wpa3_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration):
        """ Single client Wifi Capacity Test nat mode
            pytest -m "peak_throughput_tests and sixg and udp_download and nat and channel_width_160"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1}, pass_fail_criteria=True)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12402", name="WIFI-12402")
    @pytest.mark.udp_bidirectional
    @pytest.mark.sixg
    @allure.title("Single client UDP Bidirectional wifi capacity 160Mhz Bw")
    def test_client_wpa3_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration):
        """ Single client Wifi Capacity Test nat mode
            pytest -m "peak_throughput_tests and sixg and udp_bidirectional and nat and channel_width_160"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1}, pass_fail_criteria=True)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12399", name="WIFI-12399")
    @pytest.mark.tcp_upload
    @pytest.mark.sixg
    @allure.title("Single client TCP Upload wifi capacity 160Mhz Bw")
    def test_client_wpa3_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration):
        """ Single client Wifi Capacity Test nat mode
            pytest -m "peak_throughput_tests and sixg and tcp_upload and nat and channel_width_160"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_nat_tcp_ul", mode=mode,
                                       download_rate="56Kbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1}, pass_fail_criteria=True)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12398", name="WIFI-12398")
    @pytest.mark.udp_upload
    @pytest.mark.sixg
    @allure.title("Single client UDP Upload wifi capacity 160Mhz Bw")
    def test_client_wpa3_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration):
        """ Single client Wifi Capacity Test nat mode
            pytest -m "peak_throughput_tests and sixg and udp_upload and nat and channel_width_160"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g_channel_auto", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_nat_udp_ul", mode=mode,
                                       download_rate="56Kbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": 1}, pass_fail_criteria=True)
        assert True
