"""

    Performance Test: Country code along with Channel and Channel-width Test: Bridge Mode
    pytest -m "country_code and Bridge"

"""

import allure
import pytest


pytestmark = [pytest.mark.peak_throughput_tests, pytest.mark.nat, pytest.mark.fiveg, pytest.mark.channel_width_40,
              pytest.mark.wpa2_personal]

setup_params_general1 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g_36", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 40,
            "channel": 36
        }
    },
    "radius": False
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
class Test40Mhz5GChannel36PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_36", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True


setup_params_general2 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g_44", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 40,
            "channel": 44}
    },
    "radius": False
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_44
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz5GChannel44PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_44", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_44", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_44", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_44", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_44", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"

        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_44", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"

        assert True


setup_params_general5 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g_52", "appliedRadios": ["5G"], "security_key": "something"}]
    },
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 40,
            "channel": 52}
    },
    "radius": False
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
class Test40Mhz5GChannel52PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_52", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True


setup_params_general7 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g_60", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 40,
            "channel": 60}
    },
    "radius": False
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_60
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general7],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz5GChannel60PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True


setup_params_general9 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g_100", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 40,
            "channel": 100}
    },
    "radius": False
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
class Test40Mhz5GChannel100PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_60", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True


setup_params_general11 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g_108", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 40,
            "channel": 108
        }
    },
    "radius": False
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_108
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general11],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz5GChannel108PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_108", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_108", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_108", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_108", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_108", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_108", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True


setup_params_general14 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {
        "5G": {
            'band': '5G',

            'channel-width': 40,
            "channel": 132}
    },
    "radius": False
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
class Test40Mhz5GChannel132PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    @pytest.mark.aaa
    def test_client_wpa2_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_132", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True


setup_params_general15 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g_136", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 40,
            "channel": 136}
    },
    "radius": False
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_136
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general15],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz5GChannel136PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_136", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_136", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_136", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_136", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_136", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_136", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True


setup_params_general16 = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_5g_140", "appliedRadios": ["5G"], "security_key": "something"}
                          ]},
    "rf": {
        "5G": {
            'band': '5G',
            'channel-width': 40,
            "channel": 140}
    },
    "radius": False
}


@allure.feature("PEAK THROUGHPUT TESTS")
@pytest.mark.channel_140
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general16],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class Test40Mhz5GChannel140PeakThroughput(object):
    """Country code along with Channel and Channel-width Test Bridge mode
       pytest -m "country_code and Bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6934", name="WIFI-6934")
    @pytest.mark.tcp_download
    def test_client_wpa2_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_140", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6944", name="WIFI-6944")
    @pytest.mark.udp_download
    def test_client_wpa2_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_140", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6943", name="WIFI-6943")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_140", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6946", name="WIFI-6946")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_140", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_bidirectional", mode=mode,
                                       download_rate="1Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6942", name="WIFI-6942")
    @pytest.mark.tcp_upload
    def test_client_wpa2_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_140", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_tcp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6945", name="WIFI-6945")
    @pytest.mark.udp_upload
    def test_client_wpa2_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration):
        """ Wifi Capacity Test NAT mode
            pytest -m "wifi_capacity_test and NAT and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g_140", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_nat_udp_ul", mode=mode,
                                       download_rate="0Gbps", batch_size="1",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": 1})
        assert True
