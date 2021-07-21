"""

    Performance Test: Wifi Capacity Test : VLAN Mode
    pytest -m "wifi_capacity_test and VLAN"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.performance, pytest.mark.wifi_capacity_test, pytest.mark.vlan]
# """pytest.mark.usefixtures("setup_test_run")"""]

setup_params_general_dual_band = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz", "is5GHz"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_dual_band],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa2_personal
@pytest.mark.twog
@pytest.mark.fiveg
@pytest.mark.dual_band
class TestWifiCapacityVLANModeDualBand(object):
    """ Wifi Capacity Test VLAN mode
           pytest -m "wifi_capacity_test and VLAN"
    """

    @pytest.mark.tcp_download
    def test_client_wpa2_VLAN_tcp_dl(self, get_vif_state, lf_tools,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and VLAN and wpa2_personal and twog"
        """
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "VLAN"
        security_key = profile_data["security_key"]
        band = "twog"
        vlan = 1
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        wct_obj = lf_test.wifi_capacity(stations="1.1.%s" % station_names_twog[0],
                                        instance_name="test_wct_wpa2_VLAN_2g", mode=mode, vlan_id=vlan)
        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        entries = os.listdir("../reports/" + report_name + '/')
        pdf = False
        for i in entries:
            if ".pdf" in i:
                pdf = i
        if pdf:
            allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                               name=get_configuration["access_point"][0]["model"] + "_wifi_capacity_test")
            allure.attach.file(source="../reports/" + report_name + "/chart-0.png",
                               name=get_configuration["access_point"][0]["model"] + "Realtime bps",
                               attachment_type="image/png", extension=None)
            allure.attach.file(source="../reports/" + report_name + "/chart-2.png",
                               name=get_configuration["access_point"][0]["model"] + \
                                    "Total PDU Received vs NUmber of Stations Active",
                               attachment_type="image/png", extension=None)
            allure.attach.file(source="../reports/" + report_name + "/chart-3.png",
                               name=get_configuration["access_point"][0]["model"] + "Port Reset Totals",
                               attachment_type="image/png", extension=None)
            allure.attach.file(source="../reports/" + report_name + "/chart-4.png",
                               name=get_configuration["access_point"][0]["model"] + "Station Connect Time",
                               attachment_type="image/png", extension=None)
            allure.attach.file(source="../reports/" + report_name + "/chart-5.png",
                               name=get_configuration["access_point"][0]["model"] + \
                                    "Combined bps - 60 Second Running Average",
                               attachment_type="image/png", extension=None)
            allure.attach.file(source="../reports/" + report_name + "/chart-6.png",
                               name=get_configuration["access_point"][0]["model"] + \
                                    "Combined Received Bytes",
                               attachment_type="image/png", extension=None)
            allure.attach.file(source="../reports/" + report_name + "/chart-7.png",
                               name=get_configuration["access_point"][0]["model"] + \
                                    "Station Maximums",
                               attachment_type="image/png", extension=None)
            allure.attach.file(source="../reports/" + report_name + "/chart-8.png",
                               name=get_configuration["access_point"][0]["model"] + \
                                    "RF Stats for Station",
                               attachment_type="image/png", extension=None)
            allure.attach.file(source="../reports/" + report_name + "/chart-9.png",
                               name=get_configuration["access_point"][0]["model"] + \
                                    "Link Rate for Stations",
                               attachment_type="image/png", extension=None)
        print("Test Completed... Cleaning up Stations")
        lf_test.Client_disconnect(station_name=station_names_twog)
        assert True

    @pytest.mark.udp_download
    def test_client_wpa2_VLAN_udp_dl(self, get_vif_state, lf_tools,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and VLAN and wpa2_personal and twog"
        """
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa2_personal"][0]
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
                                            instance_name="test_wct_wpa2_VLAN_2g", mode=mode, vlan_id=vlan)
            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_wifi_capacity_test")
                allure.attach.file(source="../reports/" + report_name + "/chart-0.png",
                                   name=get_configuration["access_point"][0]["model"] + "Realtime bps",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-2.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Total PDU Received vs NUmber of Stations Active",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-3.png",
                                   name=get_configuration["access_point"][0]["model"] + "Port Reset Totals",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-4.png",
                                   name=get_configuration["access_point"][0]["model"] + "Station Connect Time",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-5.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined bps - 60 Second Running Average",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-6.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined Received Bytes",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-7.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Station Maximums",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-8.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "RF Stats for Station",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-9.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Link Rate for Stations",
                                   attachment_type="image/png", extension=None)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_VLAN_tcp_bidirectional(self, get_vif_state, lf_tools,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and VLAN and wpa2_personal and twog"
        """
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa2_personal"][0]
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
                                            instance_name="test_wct_wpa2_VLAN_2g", mode=mode, vlan_id=vlan)
            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_wifi_capacity_test")
                allure.attach.file(source="../reports/" + report_name + "/chart-0.png",
                                   name=get_configuration["access_point"][0]["model"] + "Realtime bps",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-2.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Total PDU Received vs NUmber of Stations Active",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-3.png",
                                   name=get_configuration["access_point"][0]["model"] + "Port Reset Totals",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-4.png",
                                   name=get_configuration["access_point"][0]["model"] + "Station Connect Time",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-5.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined bps - 60 Second Running Average",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-6.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined Received Bytes",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-7.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Station Maximums",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-8.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "RF Stats for Station",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-9.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Link Rate for Stations",
                                   attachment_type="image/png", extension=None)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.udp_bidirectional
    def test_client_wpa2_VLAN_udp_bidirectional(self, get_vif_state, lf_tools,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and VLAN and wpa2_personal and twog"
        """
        profile_data = setup_params_general_dual_band["ssid_modes"]["wpa2_personal"][0]
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
                                            instance_name="test_wct_wpa2_VLAN_2g", mode=mode, vlan_id=vlan)
            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_wifi_capacity_test")
                allure.attach.file(source="../reports/" + report_name + "/chart-0.png",
                                   name=get_configuration["access_point"][0]["model"] + "Realtime bps",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-2.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Total PDU Received vs NUmber of Stations Active",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-3.png",
                                   name=get_configuration["access_point"][0]["model"] + "Port Reset Totals",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-4.png",
                                   name=get_configuration["access_point"][0]["model"] + "Station Connect Time",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-5.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined bps - 60 Second Running Average",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-6.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined Received Bytes",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-7.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Station Maximums",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-8.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "RF Stats for Station",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-9.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Link Rate for Stations",
                                   attachment_type="image/png", extension=None)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False


setup_params_general_2G = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz", "is5GHz"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_2G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa2_personal
@pytest.mark.twog
@pytest.mark.fiveg
@pytest.mark.fiveg_band
class TestWifiCapacityVLANMode2G(object):
    """ Wifi Capacity Test VLAN mode
           pytest -m "wifi_capacity_test and VLAN"
    """

    @pytest.mark.tcp_download
    def test_client_wpa2_VLAN_tcp_dl(self, get_vif_state,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and VLAN and wpa2_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa2_personal"][0]
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
                                            instance_name="test_wct_wpa2_VLAN_2g", mode=mode, vlan_id=vlan)
            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_wifi_capacity_test")
                allure.attach.file(source="../reports/" + report_name + "/chart-0.png",
                                   name=get_configuration["access_point"][0]["model"] + "Realtime bps",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-2.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Total PDU Received vs NUmber of Stations Active",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-3.png",
                                   name=get_configuration["access_point"][0]["model"] + "Port Reset Totals",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-4.png",
                                   name=get_configuration["access_point"][0]["model"] + "Station Connect Time",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-5.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined bps - 60 Second Running Average",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-6.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined Received Bytes",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-7.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Station Maximums",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-8.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "RF Stats for Station",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-9.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Link Rate for Stations",
                                   attachment_type="image/png", extension=None)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.udp_download
    def test_client_wpa2_VLAN_udp_dl(self, get_vif_state,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and VLAN and wpa2_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa2_personal"][0]
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
                                            instance_name="test_wct_wpa2_VLAN_2g", mode=mode, vlan_id=vlan)
            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_wifi_capacity_test")
                allure.attach.file(source="../reports/" + report_name + "/chart-0.png",
                                   name=get_configuration["access_point"][0]["model"] + "Realtime bps",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-2.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Total PDU Received vs NUmber of Stations Active",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-3.png",
                                   name=get_configuration["access_point"][0]["model"] + "Port Reset Totals",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-4.png",
                                   name=get_configuration["access_point"][0]["model"] + "Station Connect Time",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-5.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined bps - 60 Second Running Average",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-6.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined Received Bytes",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-7.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Station Maximums",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-8.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "RF Stats for Station",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-9.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Link Rate for Stations",
                                   attachment_type="image/png", extension=None)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_VLAN_tcp_bidirectional(self, get_vif_state,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and VLAN and wpa2_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa2_personal"][0]
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
                                            instance_name="test_wct_wpa2_VLAN_2g", mode=mode, vlan_id=vlan)
            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_wifi_capacity_test")
                allure.attach.file(source="../reports/" + report_name + "/chart-0.png",
                                   name=get_configuration["access_point"][0]["model"] + "Realtime bps",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-2.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Total PDU Received vs NUmber of Stations Active",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-3.png",
                                   name=get_configuration["access_point"][0]["model"] + "Port Reset Totals",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-4.png",
                                   name=get_configuration["access_point"][0]["model"] + "Station Connect Time",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-5.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined bps - 60 Second Running Average",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-6.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined Received Bytes",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-7.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Station Maximums",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-8.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "RF Stats for Station",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-9.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Link Rate for Stations",
                                   attachment_type="image/png", extension=None)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.udp_bidirectional
    def test_client_wpa2_VLAN_udp_bidirectional(self, get_vif_state,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and VLAN and wpa2_personal and twog"
        """
        profile_data = setup_params_general_2G["ssid_modes"]["wpa2_personal"][0]
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
                                            instance_name="test_wct_wpa2_VLAN_2g", mode=mode, vlan_id=vlan)
            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_wifi_capacity_test")
                allure.attach.file(source="../reports/" + report_name + "/chart-0.png",
                                   name=get_configuration["access_point"][0]["model"] + "Realtime bps",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-2.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Total PDU Received vs NUmber of Stations Active",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-3.png",
                                   name=get_configuration["access_point"][0]["model"] + "Port Reset Totals",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-4.png",
                                   name=get_configuration["access_point"][0]["model"] + "Station Connect Time",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-5.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined bps - 60 Second Running Average",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-6.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined Received Bytes",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-7.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Station Maximums",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-8.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "RF Stats for Station",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-9.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Link Rate for Stations",
                                   attachment_type="image/png", extension=None)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False


setup_params_general_5G = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz", "is5GHz"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_5G],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa2_personal
@pytest.mark.twog
@pytest.mark.fiveg
@pytest.mark.twog_band
class TestWifiCapacityVLANMode5G(object):
    """ Wifi Capacity Test VLAN mode
           pytest -m "wifi_capacity_test and VLAN"
    """

    @pytest.mark.tcp_download
    def test_client_wpa2_VLAN_tcp_dl(self, get_vif_state,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and VLAN and wpa2_personal and twog"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa2_personal"][0]
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
                                            instance_name="test_wct_wpa2_VLAN_2g", mode=mode, vlan_id=vlan)
            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_wifi_capacity_test")
                allure.attach.file(source="../reports/" + report_name + "/chart-0.png",
                                   name=get_configuration["access_point"][0]["model"] + "Realtime bps",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-2.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Total PDU Received vs NUmber of Stations Active",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-3.png",
                                   name=get_configuration["access_point"][0]["model"] + "Port Reset Totals",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-4.png",
                                   name=get_configuration["access_point"][0]["model"] + "Station Connect Time",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-5.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined bps - 60 Second Running Average",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-6.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined Received Bytes",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-7.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Station Maximums",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-8.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "RF Stats for Station",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-9.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Link Rate for Stations",
                                   attachment_type="image/png", extension=None)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.udp_download
    def test_client_wpa2_VLAN_udp_dl(self, get_vif_state,
                                       lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                       get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and VLAN and wpa2_personal and twog"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa2_personal"][0]
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
                                            instance_name="test_wct_wpa2_VLAN_2g", mode=mode, vlan_id=vlan)
            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_wifi_capacity_test")
                allure.attach.file(source="../reports/" + report_name + "/chart-0.png",
                                   name=get_configuration["access_point"][0]["model"] + "Realtime bps",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-2.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Total PDU Received vs NUmber of Stations Active",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-3.png",
                                   name=get_configuration["access_point"][0]["model"] + "Port Reset Totals",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-4.png",
                                   name=get_configuration["access_point"][0]["model"] + "Station Connect Time",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-5.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined bps - 60 Second Running Average",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-6.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined Received Bytes",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-7.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Station Maximums",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-8.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "RF Stats for Station",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-9.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Link Rate for Stations",
                                   attachment_type="image/png", extension=None)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.tcp_bidirectional
    def test_client_wpa2_VLAN_tcp_bidirectional(self, get_vif_state,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and VLAN and wpa2_personal and twog"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa2_personal"][0]
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
                                            instance_name="test_wct_wpa2_VLAN_2g", mode=mode, vlan_id=vlan)
            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_wifi_capacity_test")
                allure.attach.file(source="../reports/" + report_name + "/chart-0.png",
                                   name=get_configuration["access_point"][0]["model"] + "Realtime bps",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-2.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Total PDU Received vs NUmber of Stations Active",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-3.png",
                                   name=get_configuration["access_point"][0]["model"] + "Port Reset Totals",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-4.png",
                                   name=get_configuration["access_point"][0]["model"] + "Station Connect Time",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-5.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined bps - 60 Second Running Average",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-6.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined Received Bytes",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-7.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Station Maximums",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-8.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "RF Stats for Station",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-9.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Link Rate for Stations",
                                   attachment_type="image/png", extension=None)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @pytest.mark.udp_bidirectional
    def test_client_wpa2_VLAN_udp_bidirectional(self, get_vif_state,
                                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                                  get_configuration):
        """ Wifi Capacity Test VLAN mode
            pytest -m "wifi_capacity_test and VLAN and wpa2_personal and twog"
        """
        profile_data = setup_params_general_5G["ssid_modes"]["wpa2_personal"][0]
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
                                            instance_name="test_wct_wpa2_VLAN_2g", mode=mode, vlan_id=vlan)
            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_wifi_capacity_test")
                allure.attach.file(source="../reports/" + report_name + "/chart-0.png",
                                   name=get_configuration["access_point"][0]["model"] + "Realtime bps",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-2.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Total PDU Received vs NUmber of Stations Active",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-3.png",
                                   name=get_configuration["access_point"][0]["model"] + "Port Reset Totals",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-4.png",
                                   name=get_configuration["access_point"][0]["model"] + "Station Connect Time",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-5.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined bps - 60 Second Running Average",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-6.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Combined Received Bytes",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-7.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Station Maximums",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-8.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "RF Stats for Station",
                                   attachment_type="image/png", extension=None)
                allure.attach.file(source="../reports/" + report_name + "/chart-9.png",
                                   name=get_configuration["access_point"][0]["model"] + \
                                        "Link Rate for Stations",
                                   attachment_type="image/png", extension=None)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False
