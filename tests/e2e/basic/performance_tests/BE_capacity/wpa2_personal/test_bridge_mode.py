"""
    Performance Test: BE Capacity Test : BRIDGE Mode
    pytest -m "be_capacity_tests and wpa2_personal and bridge"
"""
import pytest
import allure

pytestmark = [pytest.mark.bridge, pytest.mark.be_capacity_tests, pytest.mark.wpa2_personal]
setup_params_general_5G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {
        "5G": {
            "band": "5G",
            "channel-width": 80,
            "channel-mode": "EHT",
            "channel": 36
        }
    },
    "radius": False
}


@allure.feature("Performance Test")
@allure.parent_suite("BE Capacity Test")
@allure.suite("5 GHz Band")
@allure.sub_suite("BRIDGE Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_5G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.fiveg
class TestWifiCapacityBRIDGEModeBE5G(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.tcp_download
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @allure.title("Single BE client TCP Download wifi capacity")
    def test_client_wpa2_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting BE clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz TCP Download traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        be_capacity_tests and wpa2_personal and bridge and fiveg and tcp_download

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.be_capacity_test(instance_name="test_client_wpa2_bridge_tcp_dl", dut_data=setup_configuration,
                                          dut_mode=dut_mode, protocol="TCP", upload_rate="56Kbps",
                                          download_rate="10Gbps", num_stations={"5G": 1}, mode="BRIDGE")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.udp_download
    @pytest.mark.performance
    @allure.title("Single BE client UDP Download wifi capacity")
    def test_client_wpa2_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting BE clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz UDP Download traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        be_capacity_tests and wpa2_personal and bridge and fiveg and udp_download

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.be_capacity_test(instance_name="test_client_wpa2_bridge_udp_dl", dut_data=setup_configuration,
                                          dut_mode=dut_mode, protocol="UDP", upload_rate="56Kbps",
                                          download_rate="10Gbps", num_stations={"5G": 1}, mode="BRIDGE")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.tcp_upload
    @pytest.mark.performance
    @allure.title("Single BE client TCP Upload wifi capacity")
    def test_client_wpa2_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting BE clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz TCP Upload traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        be_capacity_tests and wpa2_personal and bridge and fiveg and tcp_upload

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.be_capacity_test(instance_name="test_client_wpa2_bridge_tcp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"5G": 1}, mode="BRIDGE")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.udp_upload
    @pytest.mark.performance
    @allure.title("Single BE client UDP Upload wifi capacity")
    def test_client_wpa2_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting BE clients in Bridge mode.
        The test case examines the maximum performance of a DUT supporting BE clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 5Ghz UDP Upload traffic.
        The 5Ghz station is configured for 80Mhz bandwidth and two spatial streams.

        Markers:
        be_capacity_tests and wpa2_personal and bridge and fiveg and udp_upload

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.be_capacity_test(instance_name="test_client_wpa2_bridge_udp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"5G": 1}, mode="BRIDGE")
        assert True


setup_params_general_2G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ]
    },
    "rf": {
        "2G": {
            "band": "2G",
            "channel-width": 20,
            "channel-mode": "EHT",
            "channel": 6
        }
    },
    "radius": False
}


@allure.feature("Performance Test")
@allure.parent_suite("BE Capacity Test")
@allure.suite("2.4 GHz Band")
@allure.sub_suite("BRIDGE Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general_2G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@pytest.mark.twog
class TestWifiCapacityBRIDGEModeBE2G(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.tcp_download
    @pytest.mark.performance
    @pytest.mark.ow_sanity_lf
    @allure.title("Single BE client TCP Download wifi capacity")
    def test_client_wpa2_bridge_tcp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting BE clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4Ghz TCP Download traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        be_capacity_tests and wpa2_personal and bridge and twog and tcp_download

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.be_capacity_test(instance_name="test_client_wpa2_bridge_tcp_dl",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="BRIDGE")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.udp_download
    @pytest.mark.performance
    @allure.title("Single BE client UDP Download wifi capacity")
    def test_client_wpa2_bridge_udp_dl(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting BE clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4Ghz UDP Download traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        be_capacity_tests and wpa2_personal and bridge and twog and udp_download

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.be_capacity_test(instance_name="test_client_wpa2_bridge_udp_dl",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="56Kbps", download_rate="10Gbps",
                                          num_stations={"2G": 1}, mode="BRIDGE")
        assert True


    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.tcp_upload
    @pytest.mark.performance
    @allure.title("Single BE client TCP Upload wifi capacity")
    def test_client_wpa2_bridge_tcp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a DUT supporting BE clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4Ghz TCP Upload traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        be_capacity_tests and wpa2_personal and bridge and twog and tcp_upload

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.be_capacity_test(instance_name="test_client_wpa2_bridge_tcp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="TCP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"2G": 1}, mode="BRIDGE")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14446", name="WIFI-14446")
    @pytest.mark.udp_upload
    @pytest.mark.performance
    @allure.title("Single BE client UDP Upload wifi capacity")
    def test_client_wpa2_bridge_udp_ul(self, get_test_library, get_dut_logs_per_test_case,
                                       get_test_device_logs, num_stations, setup_configuration,
                                       get_lab_info, selected_testbed, check_connectivity):
        """
        Description:
        The test case examines the maximum performance of a 2G-enabled DUT supporting BE clients in Bridge mode.
        This test focuses on stressing the DUT's capacity under the influence of 2.4Ghz UDP Upload traffic.
        The 2.4Ghz station is configured for 20Mhz bandwidth and two spatial streams.

        Markers:
        be_capacity_tests and wpa2_personal and bridge and twog and udp_upload

        Note:
        Please refer to the PDF report for detailed observations and analysis of the test results.
        """
        dut_mode = get_lab_info.CONFIGURATION[selected_testbed]["device_under_tests"][0]["mode"]

        get_test_library.be_capacity_test(instance_name="test_client_wpa2_bridge_udp_ul",
                                          dut_data=setup_configuration, dut_mode=dut_mode,
                                          protocol="UDP", upload_rate="10Gbps", download_rate="56Kbps",
                                          num_stations={"2G": 1}, mode="BRIDGE")
        assert True
