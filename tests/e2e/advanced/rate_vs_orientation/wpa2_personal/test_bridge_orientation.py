import os
import time
import pytest
import allure
import os.path

pytestmark = [pytest.mark.advance, pytest.mark.ratevsorientation, pytest.mark.bridge]


setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}
@allure.feature("BRIDGE MODE RATE VS ORIENTATION")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestRatevsOrientationBridge(object):


    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5431", name="WIFI-5431")
    def test_client_wpa2_personal_5g_11ac(self, lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration, lf_tools):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        print("station", station)
        ser_no = lf_test.attenuator_serial()
        print(ser_no)
        val = [['modes: 802.11an-AC'], ['pkts: MTU'], ['directions: DUT Transmit'], ['traffic_types:TCP'],
               ['bandw_options: 80'], ['spatial_streams: 2'], ['attenuator: ' + str(ser_no[0])],
               ['attenuator2: ' + str(ser_no[1])],
               ['attenuations: 0..+50..800'], ['attenuations2: 0..+50..800'],['chamber: DUT-Chamber'], ['tt_deg: 0..+30..359']]

        if station:
            time.sleep(3)
            rvr_o = lf_test.ratevsrange(station_name=station_names_fiveg, mode=mode,
                                        instance_name="ORIENTATION_RVR_BRIDGE_11_AC",
                                        vlan_id=vlan, dut_name=dut_name, raw_lines=val)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

