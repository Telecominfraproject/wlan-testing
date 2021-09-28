"""

    Performance Test: Dataplane Throughput Test: BRIDGE Mode
    pytest -m "dataplane_throughput_test open security and bridge"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.dataplane_throughput_test,
              pytest.mark.bridge]  # , pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "open", "appliedRadios": ["2G"]},
            {"ssid_name": "open", "appliedRadios": ["5G"]}]},
    "rf": {},
    "radius": False
}

@allure.suite("performance")
@allure.feature("BRIDGE MODE open security and Dataplane Throughput Test")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestDataplaneThroughputBRIDGE(object):
    """Dataplane THroughput BRIDGE Mode
       pytest -m "dataplane_throughput_test and open and BRIDGE"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3673",name="WIFI-3673")
    @pytest.mark.open
    @pytest.mark.twog
    def test_tcp_upd_open_bridge_2g_band(self, get_vif_state, lf_tools,
                             lf_test, station_names_twog, create_lanforge_chamberview_dut,
                             get_configuration):
        """Dataplane THroughput BRIDGE Mode.
           pytest -m "dataplane_throughput_test and BRIDGE and open and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security = "open"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        # if ssid_name not in get_vif_state:
        #     allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        #     pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_DPT_DPT_OPEN_2G_BRIDGE",
                                       vlan_id=vlan, dut_name=dut_name)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Dataplane Throughput Test - TCP-UDP 2.4G")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3674", name="WIFI-3674")
    @pytest.mark.open
    @pytest.mark.fiveg
    def test_tcp_upd_open_bridge_5g_band(self, get_vif_state, lf_tools,
                             lf_test, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Dataplane THroughput BRIDGE Mode
           pytest -m "dataplane_throughput_test and BRIDGE and open and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security = "open"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_DPT_DPT_OPEN_5G_BRIDGE",
                                       vlan_id=vlan, dut_name=dut_name)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Dataplane Throughput Test - TCP-UDP 5G")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False