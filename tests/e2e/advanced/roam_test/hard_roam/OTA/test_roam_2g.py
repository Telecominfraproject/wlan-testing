import pytest
import allure
import time

pytestmark = [pytest.mark.roam_test, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "roam": True,
    "ft+psk": True,
    "ft-otd": False,
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "RoamAP2g", "appliedRadios": ["2G"], "security_key": "something"},
                          {"ssid_name": "RoamAP5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [{"ssid_name": "RoamAP6g", "appliedRadios": ["6G"], "security_key": "something"}]
    },
    "rf": {},
    "radius": False
}
@allure.suite("Hard Roam 2g")
@allure.feature("Roam Test")
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")


class TestRoamOTATwog(object):

    @pytest.mark.hard_roam_2g_ota
    @pytest.mark.wpa2_personal
    def test_multi_hard_roam_2g_to_2g(self, get_configuration, lf_test, lf_reports, lf_tools,
                                      run_lf, add_env_properties,
                                      instantiate_profile, get_controller_logs, get_ap_config_slots, get_lf_logs,
                                      roaming_delay, iteration, client):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        # check channel

        lf_test.create_n_clients(sta_prefix="wlan1", num_sta=1, dut_ssid=ssid_name,
                                 dut_security=security, dut_passwd=security_key, band="twog",
                                 lf_tools=lf_tools, type="11r")
        sta_list = lf_tools.get_station_list()
        print(sta_list)
        val = lf_test.wait_for_ip(station=sta_list)
        ch = ""
        if val:
            for sta_name in sta_list:
                sta = sta_name.split(".")[2]
                time.sleep(5)
                ch = lf_tools.station_data_query(station_name=str(sta), query="channel")
            print(ch)
            lf_test.Client_disconnect(station_name=sta_list)

        else:
            pytest.exit("station failed to get ip")
            assert False

        lf_test.multi_hard_roam(run_lf=run_lf, get_configuration=get_configuration, lf_tools=lf_tools,
                                lf_reports=lf_reports,
                                instantiate_profile=instantiate_profile,
                                ssid_name=ssid_name, security=security, security_key=security_key,
                                band=band, test="2g",
                                iteration=int(iteration), num_sta=int(client), roaming_delay=roaming_delay,
                                option="ota", channel=ch)