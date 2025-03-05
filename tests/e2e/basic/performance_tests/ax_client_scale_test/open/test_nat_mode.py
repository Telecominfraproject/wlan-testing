"""

    Performance Test: AX Client Scale Test : NAT Mode
    pytest -m "ax_client_scale_tests and nat"

"""
import logging
import allure
import pytest

pytestmark = [pytest.mark.nat, pytest.mark.ax_client_scale_tests]

setup_params_general_2G = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("AX Client Scale Tests")
@allure.parent_suite("AX Client Scale Tests")
@allure.suite(suite_name="Open Security")
@allure.sub_suite(sub_suite_name="NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_2G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.open
@pytest.mark.twog
@pytest.mark.twog_band
class TestWifiCapacityNATMode2G(object):
    """ AX Client Scale Test NAT mode
        pytest -m "ax_client_scale_tests and nat and open and twog"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3648", name="WIFI-3648")
    @pytest.mark.open
    @pytest.mark.tcp_download
    @allure.title("Test for TCP Download 2.4 GHz")
    def test_client_open_NAT_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and open and twog and tcp_download"
        """
        profile_data = {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3654", name="WIFI-3654")
    @pytest.mark.open
    @pytest.mark.udp_download
    @allure.title("Test for UDP Download 2.4 GHz")
    def test_client_open_NAT_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and open and twog and udp_download"
        """
        profile_data = {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_NAT_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3670", name="WIFI-3670")
    @pytest.mark.open
    @pytest.mark.tcp_bidirectional
    @allure.title("Test for TCP Bidirectional 2.4 GHz")
    def test_client_open_NAT_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration,
                                               max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and open and twog and tcp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_NAT_tcp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3664", name="WIFI-3664")
    @pytest.mark.open
    @pytest.mark.udp_bidirectional
    @allure.title("Test for UDP Bidirectional 2.4 GHz")
    def test_client_open_NAT_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration,
                                               max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and open and twog and udp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_NAT_udp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @pytest.mark.open
    @pytest.mark.tcp_upload
    @allure.title("Test for TCP Upload 2.4 GHz")
    def test_client_open_NAT_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and open and twog and tcp_upload"
        """
        profile_data = {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_NAT_tcp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @pytest.mark.open
    @pytest.mark.udp_upload
    @allure.title("Test for UDP Upload 2.4 GHz")
    def test_client_open_NAT_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and open and twog and udp_upload"
        """
        profile_data = {"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_NAT_udp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True


setup_params_general_5G = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("AX Client Scale Tests")
@allure.parent_suite("AX Client Scale Tests")
@allure.suite(suite_name="Open Security")
@allure.sub_suite(sub_suite_name="NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_5G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.open_personal
@pytest.mark.fiveg
@pytest.mark.fiveg_band
class TestWifiCapacityNATMode5G(object):
    """ AX Client Scale Test NAT mode
        pytest -m "ax_client_scale_tests and nat and open and fiveg"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3649", name="WIFI-3649")
    @pytest.mark.open
    @pytest.mark.tcp_download
    @allure.title("Test for TCP Download 5 GHz")
    def test_client_open_NAT_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and open and fiveg and tcp_download"
        """
        profile_data = {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})

        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3655", name="WIFI-3655")
    @pytest.mark.open
    @pytest.mark.udp_download
    @allure.title("Test for UDP Download 5 GHz")
    def test_client_open_NAT_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and open and fiveg and udp_download"
        """
        profile_data = {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_NAT_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3671", name="WIFI-3671")
    @pytest.mark.open
    @pytest.mark.tcp_bidirectional
    @allure.title("Test for TCP Bidirectional 5 GHz")
    def test_client_open_NAT_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration,
                                               max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and open and fiveg and tcp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_NAT_tcp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3665", name="WIFI-3665")
    @pytest.mark.open
    @pytest.mark.udp_bidirectional
    @allure.title("Test for UDP Bidirectional 5 GHz")
    def test_client_open_NAT_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration,
                                               max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and open and fiveg and udp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_NAT_udp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True

    @pytest.mark.udp_upload
    @pytest.mark.open
    @allure.title("Test for UDP Upload 5 GHz")
    def test_client_open_NAT_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and open and fiveg and udp_upload"
        """
        profile_data = {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_NAT_udp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True

    @pytest.mark.tcp_upload
    @pytest.mark.open
    @allure.title("Test for TCP Upload 5 GHz")
    def test_client_open_NAT_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and open and fiveg and tcp_upload"
        """
        profile_data = {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_open_NAT_tcp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True