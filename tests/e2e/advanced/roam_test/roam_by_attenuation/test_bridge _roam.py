import time

import pytest
import allure
from configuration import CONFIGURATION

pytestmark = [pytest.mark.roam_test, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {},
    "radius": False
}

class TestRateLimitingWithRadiusBridge(object):

    @pytest.mark.roam_2g
    def test_basic_roam_2g(self, get_configuration, lf_test,station_names_twog, lf_tools, run_lf, add_env_properties):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        c1_2g_bssid = ""
        c2_2g_bssid = ""
        if run_lf:
            c1_2g_bssid = get_configuration["access_point"][0]["ssid"]["2g-bssid"]
            allure.attach(name="bssid of ap1", body=c1_2g_bssid)
            c2_2g_bssid = get_configuration["access_point"][1]["ssid"]["2g-bssid"]
            allure.attach(name="bssid of ap2", body=c2_2g_bssid)

        ser_no = lf_test.attenuator_serial()
        print(ser_no[0])
        ser_1 = ser_no[0].split(".")[2]
        ser_2 = ser_no[1].split(".")[2]
        # put attenuation to zero in all attenuator's
        # for i in range(4):
        #     lf_test.attenuator_modify(ser_1, i, 0)
        #     lf_test.attenuator_modify(ser_2, i, 0)

        # # create station
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        if station :
            lf_test.attach_stationdata_to_allure(name="staion info before roam", station_name=station_names_twog)
            bssid = lf_tools.station_data_query(station_name=str(station_names_twog[0]), query="ap")
            formated_bssid = bssid.lower()
            if formated_bssid == c1_2g_bssid:
                print("station connected to chamber1 ap")
            elif formated_bssid == c2_2g_bssid:
                print("station connected to chamber 2 ap")

            # logic to decrease c1 attenuation and increase c2 attenuation
            for atten_val1, atten_val2 in zip([0, 100, 300, 500, 750, 950],[950, 750, 500,300, 100, 0]):
                print(atten_val1)
                print(atten_val2)
                for i in range(4):
                    lf_test.attenuator_modify(int(ser_1), i, atten_val1)
                    lf_test.attenuator_modify(int(ser_2), i, atten_val2)
                time.sleep(10)
                lf_tools.admin_up_down(sta_list=station_names_twog, option="down")
                time.sleep(15)
                lf_tools.admin_up_down(sta_list=station_names_twog,option="up")
                time.sleep(15)
                bssid = lf_tools.station_data_query(station_name=str(station_names_twog[0]), query="ap")
                formated_bssid = bssid.lower()
                if formated_bssid == c1_2g_bssid:
                    print("station connected to chamber1 ap")
                    lf_test.attach_stationdata_to_allure(name="staion info after roam",
                                                         station_name=station_names_twog)
                    allure.attach(name="PASS",  body="client performed roam from chamber 2 ap to chamber 1 ap")
                    break
                elif formated_bssid == c2_2g_bssid:
                    print("station connected to chamber 2 ap")
                    continue
            lf_test.Client_disconnect(station_name=station_names_twog)

        else:
            allure.attach(name="FAIL", body="station failed to get ip")
            assert False







