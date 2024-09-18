"""
    Performance Test: AX Capacity Test : VLAN Mode
    pytest -m "wifi_capacity_ax_tests and wpa2_personal and vlan"
"""
import pytest
import allure

pytestmark = [pytest.mark.vlan, pytest.mark.wifi_capacity_ax_tests, pytest.mark.wpa2_personal]
setup_params_general_5G = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "channel-width": 80,
            "channel": 36
        }
    },
    "radius": False
}


@allure.feature("Performance Test")
@allure.parent_suite("AX Capacity Test")
@allure.suite("5 GHz Band")
@allure.sub_suite("VLAN Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_5G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.fiveg
class TestWifiCapacityVLANModeAX5G(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6953", name="WIFI-6953")
    @pytest.mark.tcp_download
    @allure.title("Single AX client TCP Download wifi capacity")
    def test_client_wpa2_vlan_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                     get_test_device_logs, num_stations, setup_configuration,
                                     get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in VLAN mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz TCP Download traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and vlan and fiveg and tcp_download

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        vid = [100]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_vlan_tcp_dl",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="VLAN", vlan_id=vid)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6956", name="WIFI-6956")
    @pytest.mark.udp_download
    @allure.title("Single AX client UDP Download wifi capacity")
    def test_client_wpa2_vlan_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                     get_test_device_logs, num_stations, setup_configuration,
                                     get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in VLAN mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz UDP Download traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and vlan and fiveg and udp_download

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        vid = [100]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_vlan_udp_dl",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="VLAN", vlan_id=vid)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6955", name="WIFI-6955")
    @pytest.mark.tcp_bidirectional
    @allure.title("Single AX client TCP Bidirectional wifi capacity")
    def test_client_wpa2_vlan_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                get_test_device_logs, num_stations, setup_configuration,
                                                get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in VLAN mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz TCP Bidirectional traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and vlan and fiveg and tcp_bidirectional

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        vid = [100]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_vlan_tcp_bidirectional",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="VLAN", vlan_id=vid)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6958", name="WIFI-6958")
    @pytest.mark.udp_bidirectional
    @allure.title("Single AX client UDP Bidirectional wifi capacity")
    def test_client_wpa2_vlan_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                get_test_device_logs, num_stations, setup_configuration,
                                                get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in VLAN mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz UDP Bidirectional traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and vlan and fiveg and udp_bidirectional

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        vid = [100]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_vlan_udp_bidirectional",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"5G": 1}, mode="VLAN", vlan_id=vid)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6954", name="WIFI-6954")
    @pytest.mark.tcp_upload
    @allure.title("Single AX client TCP Upload wifi capacity")
    def test_client_wpa2_vlan_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                     get_test_device_logs, num_stations, setup_configuration,
                                     get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in VLAN mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz TCP Upload traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and vlan and fiveg and tcp_upload

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        vid = [100]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_vlan_tcp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"5G": 1}, mode="VLAN", vlan_id=vid)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6960", name="WIFI-6960")
    @pytest.mark.udp_upload
    @allure.title("Single AX client UDP Upload wifi capacity")
    def test_client_wpa2_vlan_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                     get_test_device_logs, num_stations, setup_configuration,
                                     get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in VLAN mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz UDP Upload traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and vlan and fiveg and udp_upload

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        vid = [100]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_vlan_udp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"5G": 1}, mode="VLAN", vlan_id=vid)
        assert True


setup_params_general_2G = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ]
    },
    "rf": {
        "2G": {
            "band": "2G",
            "channel-width": 20,
            "channel": 6
        }
    },
    "radius": False
}


@allure.feature("Performance Test")
@allure.parent_suite("AX Capacity Test")
@allure.suite("2.4 GHz Band")
@allure.sub_suite("VLAN Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_2G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.twog
class TestWifiCapacityVLANModeAX2G(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13296", name="WIFI-13296")
    @pytest.mark.tcp_download
    @allure.title("Single AX client TCP Download wifi capacity")
    def test_client_wpa2_vlan_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                     get_test_device_logs, num_stations, setup_configuration,
                                     get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in VLAN mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz TCP Download traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and vlan and twog and tcp_download

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        vid = [100]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_vlan_tcp_dl",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="VLAN", vlan_id=vid)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13299", name="WIFI-13299")
    @pytest.mark.udp_download
    @allure.title("Single AX client UDP Download wifi capacity")
    def test_client_wpa2_vlan_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                     get_test_device_logs, num_stations, setup_configuration,
                                     get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in VLAN mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz UDP Download traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and vlan and twog and udp_download

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        vid = [100]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_vlan_udp_dl",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="VLAN", vlan_id=vid)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13298", name="WIFI-13298")
    @pytest.mark.tcp_bidirectional
    @allure.title("Single AX client TCP Bidirectional wifi capacity")
    def test_client_wpa2_vlan_tcp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                get_test_device_logs, num_stations, setup_configuration,
                                                get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in VLAN mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz TCP Bidirectional traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and vlan and twog and tcp_bidirectional

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        vid = [100]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_vlan_tcp_bidirectional",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="VLAN", vlan_id=vid)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13300", name="WIFI-13300")
    @pytest.mark.udp_bidirectional
    @allure.title("Single AX client UDP Bidirectional wifi capacity")
    def test_client_wpa2_vlan_udp_bidirectional(self, get_test_library, get_dut_logs_per_test_case,
                                                get_test_device_logs, num_stations, setup_configuration,
                                                get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in VLAN mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz UDP Bidirectional traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and vlan and twog and udp_bidirectional

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        vid = [100]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_vlan_udp_bidirectional",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="VLAN", vlan_id=vid)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13297", name="WIFI-13297")
    @pytest.mark.tcp_upload
    @allure.title("Single AX client TCP Upload wifi capacity")
    def test_client_wpa2_vlan_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                     get_test_device_logs, num_stations, setup_configuration,
                                     get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in VLAN mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz TCP Upload traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and vlan and twog and tcp_upload

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        vid = [100]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_vlan_tcp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"2G": 1}, mode="VLAN", vlan_id=vid)
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13301", name="WIFI-13301")
    @pytest.mark.udp_upload
    @allure.title("Single AX client UDP Upload wifi capacity")
    def test_client_wpa2_vlan_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                     get_test_device_logs, num_stations, setup_configuration,
                                     get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting 802.11ax clients in VLAN mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz UDP Upload traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        wifi_capacity_ax_tests and wpa2_personal and vlan and twog and udp_upload

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]
        vid = [100]

        get_test_library.ax_capacity_test(instance_name="test_client_wpa2_vlan_udp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"2G": 1}, mode="VLAN", vlan_id=vid)
        assert True
