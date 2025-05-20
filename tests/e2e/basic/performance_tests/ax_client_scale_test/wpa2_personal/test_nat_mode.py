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
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ]
    },
    "rf": {
        "2G": {
            "band": "2G",
            "channel-width": 20,
            "channel-mode": "HE",
            "channel": 6
        },
        "5G": {
            "band": "5G",
            "channel-width": 80,
            "channel-mode": "HE",
            "channel": 36
        },
        "6G": {
            "band": "6G",
            "channel-width": 160,
            "channel-mode": "HE",
            "channel": 33
        }
    },
    "radius": False
}


@allure.feature("AX Client Scale Tests")
@allure.parent_suite("AX Client Scale Tests")
@allure.suite(suite_name="WPA2 Personal Security")
@allure.sub_suite(sub_suite_name="NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_2G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.wpa2_personal
@pytest.mark.twog
@pytest.mark.twog_band
class TestWifiCapacityNATMode2G(object):
    """ AX Client Scale Test NAT mode
        pytest -m "ax_client_scale_tests and nat and wpa2_personal and twog"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3928", name="WIFI-3928")
    @pytest.mark.wpa2_personal
    @pytest.mark.tcp_download
    @pytest.mark.performance
    @allure.title("Test for TCP Download 2.4 GHz")
    def test_client_wpa2_NAT_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and twog and tcp_download"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="56Kbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3930", name="WIFI-3930")
    @pytest.mark.wpa2_personal
    @pytest.mark.udp_download
    @pytest.mark.performance
    @allure.title("Test for UDP Download 2.4 GHz")
    def test_client_wpa2_NAT_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and twog and udp_download"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="56Kbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3934", name="WIFI-3934")
    @pytest.mark.wpa2_personal
    @pytest.mark.tcp_bidirectional
    @allure.title("Test for TCP Bidirectional 2.4 GHz")
    def test_client_wpa2_NAT_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration,
                                               max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and twog and tcp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_tcp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3935", name="WIFI-3935")
    @pytest.mark.wpa2_personal
    @pytest.mark.udp_bidirectional
    @allure.title("Test for UDP Bidirectional 2.4 GHz")
    def test_client_wpa2_NAT_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration,
                                               max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and twog and udp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_udp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7127", name="WIFI-7127")
    @pytest.mark.wpa2_personal
    @pytest.mark.tcp_upload
    @pytest.mark.performance
    @allure.title("Test for TCP Upload 2.4 GHz")
    def test_client_wpa2_NAT_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and twog and tcp_upload"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_tcp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7128", name="WIFI-7128")
    @pytest.mark.wpa2_personal
    @pytest.mark.udp_upload
    @pytest.mark.performance
    @allure.title("Test for UDP Upload 2.4 GHz")
    def test_client_wpa2_NAT_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and twog and udp_upload"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_udp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True


setup_params_general_5G = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "2G": {
            "band": "2G",
            "channel-width": 20,
            "channel-mode": "HE",
            "channel": 6
        },
        "5G": {
            "band": "5G",
            "channel-width": 80,
            "channel-mode": "HE",
            "channel": 36
        },
        "6G": {
            "band": "6G",
            "channel-width": 160,
            "channel-mode": "HE",
            "channel": 33
        }
    },
    "radius": False
}


@allure.feature("AX Client Scale Tests")
@allure.parent_suite("AX Client Scale Tests")
@allure.suite(suite_name="WPA2 Personal Security")
@allure.sub_suite(sub_suite_name="NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_5G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.wpa2_personal
@pytest.mark.fiveg
@pytest.mark.fiveg_band
class TestWifiCapacityNATMode5G(object):
    """ AX Client Scale Test NAT mode
        pytest -m "ax_client_scale_tests and nat and wpa2_personal and fiveg"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3929", name="WIFI-3929")
    @pytest.mark.wpa2_personal
    @pytest.mark.tcp_download
    @pytest.mark.performance
    @allure.title("Test for TCP Download 5 GHz")
    def test_client_wpa2_NAT_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and fiveg and tcp_download"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="56Kbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})

        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3931", name="WIFI-3931")
    @pytest.mark.wpa2_personal
    @pytest.mark.udp_download
    @pytest.mark.performance
    @allure.title("Test for UDP Download 5 GHz")
    def test_client_wpa2_NAT_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and fiveg and udp_download"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="56Kbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3936", name="WIFI-3936")
    @pytest.mark.wpa2_personal
    @pytest.mark.tcp_bidirectional
    @allure.title("Test for TCP Bidirectional 5 GHz")
    def test_client_wpa2_NAT_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration,
                                               max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and fiveg and tcp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_tcp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3937", name="WIFI-3937")
    @pytest.mark.wpa2_personal
    @pytest.mark.udp_bidirectional
    @allure.title("Test for UDP Bidirectional 5 GHz")
    def test_client_wpa2_NAT_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration,
                                               max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and fiveg and udp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_udp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True

    @pytest.mark.udp_upload
    @pytest.mark.wpa2_personal
    @pytest.mark.performance
    @allure.title("Test for UDP Upload 5 GHz")
    def test_client_wpa2_NAT_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and fiveg and udp_upload"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_udp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True

    @pytest.mark.tcp_upload
    @pytest.mark.wpa2_personal
    @pytest.mark.performance
    @allure.title("Test for TCP Upload 5 GHz")
    def test_client_wpa2_NAT_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and fiveg and tcp_upload"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_tcp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True


setup_params_general_dual = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_dual_band", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "2G": {
            "band": "2G",
            "channel-width": 20,
            "channel-mode": "HE",
            "channel": 6
        },
        "5G": {
            "band": "5G",
            "channel-width": 80,
            "channel-mode": "HE",
            "channel": 36
        },
        "6G": {
            "band": "6G",
            "channel-width": 160,
            "channel-mode": "HE",
            "channel": 33
        }
    },
    "radius": False
}


@allure.feature("AX Client Scale Tests")
@allure.parent_suite("AX Client Scale Tests")
@allure.suite(suite_name="WPA2 Personal Security")
@allure.sub_suite(sub_suite_name="NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_dual],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.wpa2_personal
@pytest.mark.twog
@pytest.mark.fiveg
@pytest.mark.dual_band
@pytest.mark.twog_band
class TestWifiCapacityNATModeDual(object):
    """ AX Client Scale Test NAT mode
        pytest -m "ax_client_scale_tests and nat and wpa2_personal and dual_band"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3926", name="WIFI-3926")
    @pytest.mark.wpa2_personal
    @pytest.mark.tcp_download
    @pytest.mark.performance
    @allure.title("Test for TCP Download 2.4 GHz and 5 GHz")
    def test_client_wpa2_NAT_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and dual_band and tcp_download"
        """
        profile_data = {"ssid_name": "ssid_wpa2_dual_band", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="56Kbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations, "5G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3927", name="WIFI-3927")
    @pytest.mark.wpa2_personal
    @pytest.mark.udp_download
    @pytest.mark.performance
    @allure.title("Test for UDP Download 2.4 GHz and 5 GHz")
    def test_client_wpa2_NAT_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and dual_band and udp_download"
        """
        profile_data = {"ssid_name": "ssid_wpa2_dual_band", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="56Kbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations, "5G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3932", name="WIFI-3932")
    @pytest.mark.wpa2_personal
    @pytest.mark.tcp_bidirectional
    @allure.title("Test for TCP Bidirectional 2.4 GHz and 5 GHz")
    def test_client_wpa2_NAT_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration,
                                               max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and dual_band and tcp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_wpa2_dual_band", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_tcp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations, "5G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3933", name="WIFI-3933")
    @pytest.mark.wpa2_personal
    @pytest.mark.udp_bidirectional
    @allure.title("Test for UDP Bidirectional 2.4 GHz and 5 GHz")
    def test_client_wpa2_NAT_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration,
                                               max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and dual_band and udp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_wpa2_dual_band", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_udp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations, "5G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7127", name="WIFI-7127")
    @pytest.mark.wpa2_personal
    @pytest.mark.tcp_upload
    @pytest.mark.performance
    @allure.title("Test for TCP Upload 2.4 GHz and 5 GHz")
    def test_client_wpa2_NAT_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and dual_band and tcp_upload"
        """
        profile_data = {"ssid_name": "ssid_wpa2_dual_band", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_tcp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations, "5G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7128", name="WIFI-7128")
    @pytest.mark.wpa2_personal
    @pytest.mark.udp_upload
    @pytest.mark.performance
    @allure.title("Test for UDP Upload 2.4 GHz and 5 GHz")
    def test_client_wpa2_NAT_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    max_stations):
        """ AX Client Scale Test NAT mode
            pytest -m "ax_client_scale_tests and nat and wpa2_personal and dual_band and udp_upload"
        """
        profile_data = {"ssid_name": "ssid_wpa2_dual_band", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "NAT-WAN"
        get_test_library.wifi_capacity(instance_name="test_client_wpa2_NAT_udp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations, "5G": max_stations})
        assert True