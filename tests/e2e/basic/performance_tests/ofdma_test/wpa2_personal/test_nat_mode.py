"""

    Performance Test: Ofdma Test : nat Mode
    pytest -m "ofdma and nat"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.wpa2_personal, pytest.mark.ofdma, pytest.mark.nat]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ofdma-5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ofdma-2g", "appliedRadios": ["2G"], "security_key": "something"}
        ]
    },
    "rf": [],
    "radius": False
}


@allure.suite("performance")
@allure.feature("nat MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa2_personal
@pytest.mark.twog
@pytest.mark.twog_band
class TestOfdmabridgeMode(object):
    """
        OFDMA Test nat mode
        pytest -m "ofdma_test and nat"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7112", name="WIFI-7112")
    @pytest.mark.tcp_download
    def test_ofdma_he_capability_wpa2_bridge_twog(self, lf_tools, setup_profiles,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test nat mode
            pytest -m "ofdma_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]
        ssid_2g = profile_data['ssid_name'][0]
        ssid_5g = profile_data['ssid_name'][1]
        mode = "nat"
        vlan = 1
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_2g)
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_5g)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="ofdma_wpa2_bridge", mode=mode, vlan_id=vlan,
                                        download_rate="300Mbps",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7112", name="WIFI-7112")
    @pytest.mark.udp_download
    def test_ofdma_he_capability_wpa2_bridge_fiveg(self, lf_tools,
                                                   lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                   get_configuration):
        """ Wifi Capacity Test nat mode
            pytest -m "ofdma_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "nat"
        vlan = 1
        lf_tools.add_stations(band="2G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.add_stations(band="5G", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_bridge_udp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps",
                                        upload_rate="0", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True
