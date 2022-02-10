"""

    Performance Test: AX Capacity Test : BRIDGE Mode
    pytest -m "wifi_capacity_test and BRIDGE"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.performance, pytest.mark.bridge]
setup_params_general_5G = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("BRIDGE MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_5G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa2_personal
@pytest.mark.fiveg
@pytest.mark.fiveg_band
@pytest.mark.ax
class TestWifiCapacityBRIDGEModeAX5G(object):
    """ Wifi Capacity Test BRIDGE mode
           pytest -m "wifi_capacity_test and BRIDGE"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3929", name="WIFI-3929")
    @pytest.mark.tcp_download
    def test_client_wpa2_BRIDGE_tcp_dl(self, lf_tools, setup_profiles,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3931", name="WIFI-3931")
    @pytest.mark.udp_download
    def test_client_wpa2_BRIDGE_udp_dl(self, lf_tools,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3936", name="WIFI-3936")
    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_BRIDGE_tcp_bidirectional(self, lf_tools,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3937", name="WIFI-3937")
    @pytest.mark.udp_bidirectional
    def test_client_wpa2_BRIDGE_udp_bidirectional(self, lf_tools,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_bi", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4000", name="WIFI-4000")
    @pytest.mark.tcp_upload
    def test_client_wpa2_BRIDGE_tcp_ul(self, lf_tools, setup_profiles,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_ul", mode=mode, vlan_id=vlan,
                                        download_rate="0",
                                        upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-40001", name="WIFI-4001")
    @pytest.mark.udp_upload
    def test_client_wpa2_BRIDGE_udp_ul(self, lf_tools,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test BRIDGE mode
            pytest -m "wifi_capacity_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_udp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="0",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True