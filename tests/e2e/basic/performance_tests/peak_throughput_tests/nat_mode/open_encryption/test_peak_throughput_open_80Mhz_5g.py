"""

    Performance Test: Country code along with Channel and Channel-width Test: NAT Mode
    pytest -m "country_code and NAT"

"""

import allure
import pytest


pytestmark = [pytest.mark.peak_throughput_tests, pytest.mark.nat, pytest.mark.fiveg, pytest.mark.channel_width_80,
              pytest.mark.open]

setup_params_general1 = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_5g_36", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 80,
            "channel": 36
        }
    },
    "radius": False
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("Peak Throughput Tests: NAT Mode w/ Open Security")
@allure.suite("80Mhz Bandwidth in 5GHz Band")
@allure.sub_suite("Channel-36")
@pytest.mark.channel_36
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test80Mhz5GChannel36PeakThroughput(object):
    """Country code along with Channel and Channel-width Test NAT mode
       pytest -m "country_code and NAT"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_open_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_open_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="56Kbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_open_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_open_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_open_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_open_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True


setup_params_general5 = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_5g_52", "appliedRadios": ["5G"], "security_key": "something"}]
    },
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 80,
            "channel": 52}
    },
    "radius": False
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("Peak Throughput Tests: NAT Mode w/ Open Security")
@allure.suite("80Mhz Bandwidth in 5GHz Band")
@allure.sub_suite("Channel-52")
@pytest.mark.channel_52
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test80Mhz5GChannel52PeakThroughput(object):
    """Country code along with Channel and Channel-width Test NAT mode
       pytest -m "country_code and NAT"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_open_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_open_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_open_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_open_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_open_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_open_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True


setup_params_general9 = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 80,
            "channel": 100}
    },
    "radius": False
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("Peak Throughput Tests: NAT Mode w/ Open Security")
@allure.suite("80Mhz Bandwidth in 5GHz Band")
@allure.sub_suite("Channel-100")
@pytest.mark.channel_100
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general9],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test80Mhz5GChannel100PeakThroughput(object):
    """Country code along with Channel and Channel-width Test NAT mode
       pytest -m "country_code and NAT"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_open_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_open_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_open_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_open_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_open_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_open_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True


setup_params_general14 = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 80,
            "channel": 132}
    },
    "radius": False
}


@allure.feature("PEAK THROUGHPUT TESTS")
@allure.parent_suite("Peak Throughput Tests: NAT Mode w/ Open Security")
@allure.suite("80Mhz Bandwidth in 5GHz Band")
@allure.sub_suite("Channel-132")
@pytest.mark.channel_132
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general14],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test80Mhz5GChannel132PeakThroughput(object):
    """Country code along with Channel and Channel-width Test NAT mode
       pytest -m "country_code and NAT"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_open_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_open_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_open_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_open_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_open_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_open_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "peak_throughput_tests and NAT and open and twog"
        """
        profile_data = {"ssid_name": "ssid_open_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True