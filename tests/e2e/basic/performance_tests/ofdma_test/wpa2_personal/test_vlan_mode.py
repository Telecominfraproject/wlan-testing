"""

    Performance Test: Ofdma Test : vlan Mode
    pytest -m "ofdma and vlan"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.wpa2_personal, pytest.mark.ofdma, pytest.mark.vlan]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ofdma-5g", "appliedRadios": ["5G"], "security_key": "something", "vlan": 100},
            {"ssid_name": "ofdma-2g", "appliedRadios": ["2G"], "security_key": "something", "vlan": 100}
        ]
    },
    "rf": [],
    "radius": False
}


@allure.suite("performance")
@allure.feature("vlan MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa2_personal
@pytest.mark.twog
class TestOfdmabridgeMode(object):
    """
        OFDMA Test vlan mode
        pytest -m "ofdma_test and vlan"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7112", name="WIFI-7112")
    @pytest.mark.tcp_download
    def test_ofdma_he_capability_wpa2_bridge_twog(self, lf_tools, setup_profiles,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test vlan mode
            pytest -m "ofdma_test and vlan and wpa2_personal and twog"
        """
        ssid_2g = setup_params_general["ssid_modes"]["wpa2_personal"]['ssid_name'][1]
        mode = "vlan"
        vlan = 1
        lf_tools.add_stations(band="2G", num_stations="4", dut=lf_tools.dut_name, ssid_name=ssid_2g)
        lf_tools.Chamber_View()
        influx_tags = ["ofdma", "download", "2G"]
        wct_obj = lf_test.wifi_capacity(instance_name="ofdma_wpa2_bridge", mode=mode, vlan_id=vlan,
                                        download_rate="300Mbps", batch_size='4',
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7112", name="WIFI-7112")
    @pytest.mark.fiveg
    def test_ofdma_he_capability_wpa2_bridge_fiveg(self, lf_tools,
                                                   lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                   get_configuration):
        """ ofdma Test vlan mode
            pytest -m "ofdma_test and vlan and wpa2_personal and twog"
        """
        ssid_5g = setup_params_general["ssid_modes"]["wpa2_personal"]['ssid_name'][1]
        mode = "vlan"
        vlan = 1
        lf_tools.add_stations(band="5G", num_stations="4", dut=lf_tools.dut_name, ssid_name=ssid_5g)
        lf_tools.Chamber_View()
        influx_tags = ["ofdma", "download", "5G"]
        wct_obj = lf_test.wifi_capacity(instance_name="ofdma_wpa2_bridge", mode=mode, vlan_id=vlan,
                                        download_rate="300Mbps", batch_size='4',
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True
