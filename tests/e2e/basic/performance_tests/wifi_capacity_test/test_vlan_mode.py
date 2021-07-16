"""

    Performance Test: Wifi Capacity Test : VLAN Mode
    pytest -m "wifi_capacity_test and VLAN"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.wifi_capacity_test, pytest.mark.vlan,
              pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestWifiCapacityVLANMode(object):
    """ Wifi Capacity Test vlan mode
           pytest -m "wifi_capacity_test and vlan"
    """

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_client_wpa2_VLAN_2g(self, get_vif_state,
                                   lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                   get_configuration):
        """ Wifi Capacity Test vlan mode
            pytest -m "wifi_capacity_test and vlan and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "VLAN"
        security_key = profile_data["security_key"]
        band = "twog"
        vlan = 1
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        if station:
            wct_obj = lf_test.wifi_capacity(stations="1.1.%s" % station_names_twog[0],
                                            instance_name="test_wct_wpa2_vlan", mode=mode, vlan_id=vlan)
            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_wifi_capacity_test")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_client_wpa2_vlan_5gg(self, get_vif_state,
                                   lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                   get_configuration):
        """ Wifi Capacity Test vlan mode
            pytest -m "wifi_capacity_test and vlan and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "VLAN"
        security_key = profile_data["security_key"]
        band = "fiveg"
        vlan = 1
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        if station:
            wct_obj = lf_test.wifi_capacity(stations="1.1.%s" % station_names_fiveg[0],
                                            instance_name="test_wct_wpa2_vlan", mode=mode, vlan_id=vlan)
            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_wifi_capacity_test")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False
