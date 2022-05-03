"""

    Performance Test: Ofdma Test : bridge Mode
    pytest -m "ofdma and bridge"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.wpa2_personal, pytest.mark.ofdma, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ofdma-2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ofdma-5g", "appliedRadios": ["5G"], "security_key": "something"},

        ]
    },
    "rf": [],
    "radius": False
}


@allure.suite("performance")
@allure.feature("bridge MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa2_personal
class TestOfdmabridgeMode(object):
    """
        OFDMA Test bridge mode
        pytest -m "ofdma_test and bridge"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7112", name="WIFI-7112")
    @pytest.mark.twog
    def test_ofdma_he_capability_wpa2_bridge_twog(self, lf_tools, lf_test, station_names_ax):
        """ ofdma Test bridge mode
            pytest -m "ofdma_test and bridge and wpa2_personal and twog"
        """
        ssid_2g = setup_params_general["ssid_modes"]["wpa2_personal"][0]['ssid_name']
        passkey = setup_params_general["ssid_modes"]["wpa2_personal"][0]['security_key']
        mode = "BRIDGE"
        vlan = 100
        if len(lf_test.ax_radios) >= 1:
            radios_ax = lf_test.ax_radios
            for i in range(len(radios_ax)):
                if '1.1.' in radios_ax[i]:
                    radios_ax[i] = str(radios_ax[i]).replace('1.1.', '')
            sta_mode, sta = 13, 'sta000'
            sta_list = []
            sta_names = ''
            for j in range(len(radios_ax) - 1):
                sta_list.append(sta + str(j))
                lf_test.Client_Connect_Using_Radio(ssid=ssid_2g, passkey=passkey, security="wpa2", mode="BRIDGE",
                                                   vlan_id=100, radio=radios_ax[j], sta_mode=sta_mode,
                                                   station_name=[sta + str(j)])
            print(sta_list)
            sniffer_channel = int(lf_tools.station_data_query(station_name=sta_list[0]))
            sniffer_radio = radios_ax[-1]
            influx_tags = ["ofdma", "download", "2.4G"]
            print("ax station names: ", station_names_ax)
            res_data = lf_tools.json_get(_req_url='port?fields=port+type')['interfaces']
            temp_sta =[]
            for i in res_data:
                for item in i:
                    if i[item]['port type'] == 'WIFI-STA':
                            sta_names += item + ","
            if sta_names.endswith(','):
                sta_names.removesuffix(',')
            ofdma_obj = lf_test.ofdma(mode=mode, vlan_id=vlan, inst_name="ofdma", batch_size='1', rawlines=None,
                                      sniffer_channel=sniffer_channel, sniffer_radio=sniffer_radio, wct_stations=sta_names)
            report_name = ofdma_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            assert True
        else:
            print("This Feature needs AX radios to test")
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7112", name="WIFI-7112")
    @pytest.mark.fiveg
    def test_ofdma_he_capability_wpa2_bridge_fiveg(self, lf_tools, lf_test, station_names_ax):
        """ ofdma Test bridge mode
            pytest -m "ofdma_test and bridge and wpa2_personal and fiveg"
        """
        ssid_5g = setup_params_general["ssid_modes"]["wpa2_personal"][1]['ssid_name']
        passkey = setup_params_general["ssid_modes"]["wpa2_personal"][1]['security_key']
        mode = "BRIDGE"
        vlan = 100
        if len(lf_test.ax_radios) >= 1:
            radios_ax = lf_test.ax_radios
            for i in range(len(radios_ax)):
                if '1.1.' in radios_ax[i]:
                    radios_ax[i] = str(radios_ax[i]).replace('1.1.', '')
            sta_mode, sta = 13, 'sta000'
            sta_list = []
            sta_names = ''
            for j in range(len(radios_ax) - 1):
                sta_list.append(sta + str(j))
                lf_test.Client_Connect_Using_Radio(ssid=ssid_5g, passkey=passkey, security="wpa2", mode="BRIDGE",
                                                   vlan_id=100, radio=radios_ax[j], sta_mode=sta_mode,
                                                   station_name=[sta + str(j)])
            print(sta_list)
            sniffer_channel = int(lf_tools.station_data_query(station_name=sta_list[0]))
            sniffer_radio = radios_ax[-1]
            influx_tags = ["ofdma", "download", "5G"]
            print("ax station names: ", station_names_ax)
            res_data = lf_tools.json_get(_req_url='port?fields=port+type')['interfaces']
            temp_sta =[]
            for i in res_data:
                for item in i:
                    if i[item]['port type'] == 'WIFI-STA':
                            sta_names += item + ","
            if sta_names.endswith(','):
                sta_names.removesuffix(',')
            ofdma_obj = lf_test.ofdma(mode=mode, vlan_id=vlan, inst_name="ofdma", batch_size='1', rawlines=None,
                                      sniffer_channel=sniffer_channel, sniffer_radio=sniffer_radio, wct_stations=sta_names)
            report_name = ofdma_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            assert True
        else:
            print("This Feature needs AX radios to test")
            assert False