"""

    Performance Test: Client Scale Test : BRIDGE Mode
    pytest -m "client_scale_tests and bridge"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.bridge, pytest.mark.client_scale_tests]

setup_params_general_2G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("Client Scale Tests")
@allure.parent_suite("Client Scale Tests")
@allure.suite(suite_name="WPA3 Personal Security")
@allure.sub_suite(sub_suite_name="BRIDGE Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_2G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.wpa3_personal
@pytest.mark.twog
@pytest.mark.twog_band
class TestWifiCapacityBRIDGEMode2G(object):
    """ Client Scale Test BRIDGE mode
        pytest -m "client_scale_tests and bridge and wpa3_personal and twog"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3651", name="WIFI-3651")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_download
    @allure.title("Test for TCP Download 2.4 GHz")
    def test_client_wpa3_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and twog and tcp_download"
        """
        profile_data = {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_upload
    @allure.title("Test for TCP Upload 2.4 GHz")
    def test_client_wpa3_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and twog and tcp_upload"
        """
        profile_data = {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @pytest.mark.wpa3_personal
    @pytest.mark.udp_upload
    @allure.title("Test for UDP Upload 2.4 GHz")
    def test_client_wpa3_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and twog and udp_upload"
        """
        profile_data = {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3658", name="WIFI-3658")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_download
    @allure.title("Test for UDP Download 2.4 GHz")
    def test_client_wpa3_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ Client Scale Test BRIDGE mode
                    pytest -m "client_scale_tests and bridge and wpa3_personal and twog and udp_download"
                """
        profile_data = {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3668", name="WIFI-3668")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_bidirectional
    @allure.title("Test for TCP Bidirectional 2.4 GHz")
    def test_client_wpa3_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,
                                                  max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and twog and tcp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3662", name="WIFI-3662")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_bidirectional
    @allure.title("Test for UDP Bidirectional 2.4 GHz")
    def test_client_wpa3_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,
                                                  max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and twog and udp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"2G": max_stations})
        assert True


setup_params_general_5G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("Client Scale Tests")
@allure.parent_suite("Client Scale Tests")
@allure.suite(suite_name="WPA3 Personal Security")
@allure.sub_suite(sub_suite_name="BRIDGE Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_5G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.wpa3_personal
@pytest.mark.fiveg
@pytest.mark.fiveg_band
class TestWifiCapacityBRIDGEMode5G(object):
    """ Client Scale Test BRIDGE mode
           client_scale_tests and bridge and wpa3_personal and fiveg"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3653", name="WIFI-3653")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_download
    @allure.title("Test for TCP Download 5 GHz")
    def test_client_wpa3_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and fiveg and tcp_download"
        """
        profile_data = {"ssid_name": "ssid_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3659", name="WIFI-3659")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_download
    @allure.title("Test for UDP Download 5 GHz")
    def test_client_wpa3_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and fiveg and udp_download"
        """
        profile_data = {"ssid_name": "ssid_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3669", name="WIFI-3669")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_bidirectional
    @allure.title("Test for TCP Bidirectional 5 GHz")
    def test_client_wpa3_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,
                                                  max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and fiveg and tcp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3663", name="WIFI-3663")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_bidirectional
    @allure.title("Test for UDP Bidirectional 5 GHz")
    def test_client_wpa3_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,
                                                  max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and fiveg and udp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True

    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_upload
    @allure.title("Test for TCP Upload 5 GHz")
    def test_client_wpa3_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and fiveg and tcp_upload"
        """
        profile_data = {"ssid_name": "ssid_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True

    @pytest.mark.wpa3_personal
    @pytest.mark.udp_upload
    @allure.title("Test for UDP Upload 5 GHz")
    def test_client_wpa3_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and fiveg and udp_upload"
        """
        profile_data = {"ssid_name": "ssid_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"5G": max_stations})
        assert True


setup_params_general_6G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("Client Scale Tests")
@allure.parent_suite("Client Scale Tests")
@allure.suite(suite_name="WPA3 Personal Security")
@allure.sub_suite(sub_suite_name="BRIDGE Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_6G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.wpa3_personal
@pytest.mark.sixg
@pytest.mark.sixg_band
@pytest.mark.performance
class TestWifiCapacityBRIDGEMode6G(object):
    """ Client Scale Test BRIDGE mode
           client_scale_tests and bridge and wpa3_personal and sixg"
    """

    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_download
    @allure.title("Test for TCP Download 6 GHz")
    def test_client_wpa3_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and sixg and tcp_download"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": max_stations})
        assert True

    # @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3659", name="WIFI-3659")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_download
    @allure.title("Test for UDP Download 6 GHz")
    def test_client_wpa3_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and sixg and udp_download"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_dl", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": max_stations})
        assert True

    # @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3669", name="WIFI-3669")
    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_bidirectional
    @allure.title("Test for TCP Bidirectional 6 GHz")
    def test_client_wpa3_bridge_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,
                                                  max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and sixg and tcp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": max_stations})
        assert True

    # @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3663", name="WIFI-3663")
    @pytest.mark.wpa3_personal
    @pytest.mark.udp_bidirectional
    @allure.title("Test for UDP Bidirectional 6 GHz")
    def test_client_wpa3_bridge_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                  get_test_device_logs, num_stations, setup_configuration,
                                                  max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and sixg and udp_bidirectional"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_bi", mode=mode,
                                       download_rate="1Gbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": max_stations})
        assert True

    @pytest.mark.wpa3_personal
    @pytest.mark.tcp_upload
    @allure.title("Test for TCP Upload 6 GHz")
    def test_client_wpa3_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and sixg and tcp_upload"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_tcp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": max_stations})
        assert True

    @pytest.mark.wpa3_personal
    @pytest.mark.udp_upload
    @allure.title("Test for UDP Upload 6 GHz")
    def test_client_wpa3_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration, max_stations):
        """ Client Scale Test BRIDGE mode
            pytest -m "client_scale_tests and bridge and wpa3_personal and sixg and udp_upload"
        """
        profile_data = {"ssid_name": "ssid_wpa3_6g", "appliedRadios": ["6G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        get_test_library.wifi_capacity(instance_name="test_client_wpa3_BRIDGE_udp_ul", mode=mode,
                                       download_rate="100Kbps", batch_size="1,5,10,20,40,64,128,256",
                                       upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000",
                                       move_to_influx=False, dut_data=setup_configuration, ssid_name=ssid_name,
                                       num_stations={"6G": max_stations})
        assert True

