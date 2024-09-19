"""

    Performance Test: Country code along with Channel and Channel-width Test: Bridge Mode
    pytest -m "country_code and Bridge"

"""

import allure
import pytest

pytestmark = [pytest.mark.peak_throughput_tests, pytest.mark.nat, pytest.mark.twog, pytest.mark.channel_width_20,
              pytest.mark.wpa2_personal]

setup_params_general_1 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_personal_2g_1", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 20,
            "channel": 1
        }
    },
    "radius": False
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
class Test20Mhz2GChannel1PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_personal_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_1", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_personal_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_1", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_personal_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_1", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_personal_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_1", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_personal_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_1", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_personal_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_1", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True


setup_params_general_2 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_personal_2g_2", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 20,
            "channel": 2
        }
    },
    "radius": False
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
class Test20Mhz2GChannel2PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_personal_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_2", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_personal_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_2", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_personal_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_2", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_personal_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_2", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_personal_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_2", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_personal_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_2", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True


setup_params_general_3 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_personal_2g_3", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 20,
            "channel": 3
        }
    },
    "radius": False
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
class Test20Mhz2GChannel3PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_personal_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_3", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_personal_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_3", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_personal_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_3", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_personal_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_3", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_personal_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_3", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_personal_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_3", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True


setup_params_general_4 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_personal_2g_4", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 20,
            "channel": 4
        }
    },
    "radius": False
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
class Test20Mhz2GChannel4PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_personal_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_4", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_personal_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_4", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_personal_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_4", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_personal_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_4", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_personal_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_4", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_personal_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_4", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True


setup_params_general_5 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_personal_2g_5", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 20,
            "channel": 4
        }
    },
    "radius": False
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
class Test20Mhz2GChannel5PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_personal_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_5", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_personal_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_5", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_personal_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_5", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_personal_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_5", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_personal_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_5", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_personal_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_5", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True


setup_params_general_6 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_personal_2g_6", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 20,
            "channel": 6
        }
    },
    "radius": False
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
class Test20Mhz2GChannel6PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_personal_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_6", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_personal_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_6", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_personal_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_6", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_personal_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_6", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_personal_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_6", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_personal_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_6", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True


setup_params_general_7 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_personal_2g_7", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',

            'channel-width': 20,
            "channel": 7}
    },
    "radius": False
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
class Test20Mhz2GChannel7PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @pytest.mark.aaa
    def test_client_wpa2_personal_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_7", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_personal_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_7", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_personal_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_7", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_personal_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_7", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_personal_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_7", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_personal_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_7", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True


setup_params_general_8 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_personal_2g_8", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 20,
            "channel": 8}
    },
    "radius": False
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
class Test20Mhz2GChannel8PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @pytest.mark.aaa
    def test_client_wpa2_personal_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_8", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_personal_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_8", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_personal_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_8", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_personal_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_8", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_personal_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_8", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_personal_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_8", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True


setup_params_general_9 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_personal_2g_9", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',

            'channel-width': 20,
            "channel": 9}
    },
    "radius": False
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
class Test20Mhz2GChannel9PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @pytest.mark.aaa
    def test_client_wpa2_personal_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_9", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_personal_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_9", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_personal_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_9", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_personal_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_9", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_personal_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_9", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_personal_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_9", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True


setup_params_general_10 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_personal_2g_10", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 20,
            "channel": 10}
    },
    "radius": False
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
class Test20Mhz2GChannel10PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @pytest.mark.aaa
    def test_client_wpa2_personal_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_personal_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_personal_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_personal_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_personal_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_personal_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_10", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True


setup_params_general_11 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_personal_2g_11", "appliedRadios": ["2G"], "security_key": "something"}]},
    "rf": {
        "2G": {
            'band': '2G',
            'channel-width': 20,
            "channel": 11}
    },
    "radius": False
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
class Test20Mhz2GChannel11PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @pytest.mark.aaa
    def test_client_wpa2_personal_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_personal_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_personal_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_personal_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_personal_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_personal_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_personal_2g_11", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_personal_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": 1})
        assert True
