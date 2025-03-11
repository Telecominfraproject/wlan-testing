"""
    Performance Test: AX Capacity Test : NAT Mode
    pytest -m "wifi_capacity_ax_tests and wpa2_personal and nat"
"""
import pytest
import allure

pytestmark = [pytest.mark.nat, pytest.mark.wifi_capacity_ax_tests, pytest.mark.wpa2_personal]
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


@allure.feature("Performance Test")
@allure.parent_suite("AX Capacity Test")
@allure.suite("5 GHz Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_5G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.fiveg
class TestWifiCapacityNATModeAX5G(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6947", name="WIFI-6947")
    @pytest.mark.tcp_download
    @pytest.mark.performance
    @allure.title("Single AX client TCP Download wifi capacity")
    def test_client_wpa2_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz TCP Download traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and nat and fiveg and tcp_download

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_nat_tcp_dl",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="NAT-WAN")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6950", name="WIFI-6950")
    @pytest.mark.udp_download
    @pytest.mark.performance
    @allure.title("Single AX client UDP Download wifi capacity")
    def test_client_wpa2_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz UDP Download traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and nat and fiveg and udp_download

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_nat_tcp_dl",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="NAT-WAN")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6949", name="WIFI-6949")
    @pytest.mark.tcp_bidirectional
    @allure.title("Single AX client TCP Bidirectional wifi capacity")
    def test_client_wpa2_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration,
                                               get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz TCP Bidirectional traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and nat and fiveg and tcp_bidirectional

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_nat_tcp_bidirectional",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="NAT-WAN")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6952", name="WIFI-6952")
    @pytest.mark.udp_bidirectional
    @allure.title("Single AX client UDP Bidirectional wifi capacity")
    def test_client_wpa2_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration,
                                               get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz UDP Bidirectional traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and nat and fiveg and udp_bidirectional

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_nat_udp_bidirectional",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="NAT-WAN")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6948", name="WIFI-6948")
    @pytest.mark.tcp_upload
    @pytest.mark.performance
    @allure.title("Single AX client TCP Upload wifi capacity")
    def test_client_wpa2_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz TCP Upload traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and nat and fiveg and tcp_upload

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_nat_tcp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"5G": 1}, mode="NAT-WAN")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6951", name="WIFI-6951")
    @pytest.mark.udp_upload
    @pytest.mark.performance
    @allure.title("Single AX client UDP Upload wifi capacity")
    def test_client_wpa2_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz UDP Upload traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and nat and fiveg and udp_upload

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_nat_udp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"5G": 1}, mode="NAT-WAN")
        assert True


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


@allure.feature("Performance Test")
@allure.parent_suite("AX Capacity Test")
@allure.suite("2.4 GHz Band")
@allure.sub_suite("NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_2G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.twog
class TestWifiCapacityNATModeAX2G(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13290", name="WIFI-13290")
    @pytest.mark.tcp_download
    @pytest.mark.performance
    @allure.title("Single AX client TCP Download wifi capacity")
    def test_client_wpa2_nat_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4Ghz TCP Download traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and nat and twog and tcp_download

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_nat_tcp_dl",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="NAT-WAN")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13293", name="WIFI-13293")
    @pytest.mark.udp_download
    @pytest.mark.performance
    @allure.title("Single AX client UDP Download wifi capacity")
    def test_client_wpa2_nat_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4Ghz UDP Download traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and nat and twog and udp_download

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_nat_udp_dl",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="NAT-WAN")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13292", name="WIFI-13292")
    @pytest.mark.tcp_bidirectional
    @allure.title("Single AX client TCP Bidirectional wifi capacity")
    def test_client_wpa2_nat_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration,
                                               get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4Ghz TCP Bidirectional traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and nat and twog and tcp_bidirectional

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_nat_tcp_bidirectional",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="NAT-WAN")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13295", name="WIFI-13295")
    @pytest.mark.udp_bidirectional
    @allure.title("Single AX client UDP Bidirectional wifi capacity")
    def test_client_wpa2_nat_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                               get_test_device_logs, num_stations, setup_configuration,
                                               get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4Ghz UDP Bidirectional traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and nat and twog and udp_bidirectional

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_nat_udp_bidirectional",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="NAT-WAN")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13291", name="WIFI-13291")
    @pytest.mark.tcp_upload
    @pytest.mark.performance
    @allure.title("Single AX client TCP Upload wifi capacity")
    def test_client_wpa2_nat_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4Ghz TCP Upload traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and nat and twog and tcp_upload

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_nat_tcp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"2G": 1}, mode="NAT-WAN")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13294", name="WIFI-13294")
    @pytest.mark.udp_upload
    @pytest.mark.performance
    @allure.title("Single AX client UDP Upload wifi capacity")
    def test_client_wpa2_nat_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                    get_test_device_logs, num_stations, setup_configuration,
                                    get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in NAT mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4Ghz UDP Upload traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and nat and twog and udp_upload

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_nat_udp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"2G": 1}, mode="NAT-WAN")
        assert True
