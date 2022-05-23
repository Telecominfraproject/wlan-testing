import time
import pytest
import sys
import allure
import random
import string

if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

pytestmark = [pytest.mark.regression, pytest.mark.interop, pytest.mark.android, pytest.mark.interop_and, pytest.mark.ToggleWifiMode,
              pytest.mark.client_reconnect, pytest.mark.enterprise]
from android_lib import closeApp, set_APconnMobileDevice_android, Toggle_WifiMode_android, ForgetWifiConnection, openApp,\
    gets_ip_add_for_checking_and_forgets_ssid, verifyUploadDownloadSpeed_android, wifi_connect, wifi_disconnect_and_forget, gets_ip_add_eap_and_does_not_forget_ssid

setup_params_enterprise = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa_enterprise": [
            {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_wpa_eap_5g", "appliedRadios": ["5G"]}],
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"]}],
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"]}]},

    "rf": {},
    "radius": True
}
for sec_modes in setup_params_enterprise['ssid_modes'].keys():
    for i in range(len(setup_params_enterprise['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_enterprise['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_enterprise['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string

@allure.suite(suite_name="interop regression")
@allure.sub_suite(sub_suite_name="Bridge Mode EAP Client ReConnect : Suite-A")
@pytest.mark.suiteA
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")


@allure.feature("Maverick")
@pytest.mark.maverick
class TestMaverick(object):
    @pytest.mark.nolme
    def test_ap_maverick(self,request, lf_tools, setup_controller, get_vif_state, get_configuration, get_ap_logs, get_apnos):
        for ap in get_configuration['access_point']:
            cmd = "uci show ucentral"
            print(get_configuration['access_point'])
            ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
            gw = ap_ssh.run_generic_command(cmd)
            print("Status:")
            print(gw)
            connected, latest, active = ap_ssh.get_ucentral_status()
            print("Connected:")
            print(connected)
            iwinfo = ap_ssh.get_iwinfo()
            print("iwinfo:")
            print(iwinfo)
            maverick = ap_ssh.set_maverick()
            print("maverick:")
            print(maverick)
            # reboot = ap_ssh.reboot()
            # print("rebooted")
            # print(reboot)

    # def test_maverick_Bridge(self, request, get_vif_state, get_ToggleAirplaneMode_data
    #                                                   , setup_perfectoMobile_android, radius_info, get_ap_logs):
    #
    #     profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][1]
    #     ssidName = profile_data["ssid_name"]
    #     # ssidPassword = profile_data["security_key"]
    #     print("SSID_NAME: " + ssidName)
    #     # print ("SSID_PASS: " + ssidPassword)
    #     ttls_passwd = radius_info["password"]
    #     identity = radius_info['user']
    #     get_vif_state.append(ssidName)
    #     if ssidName not in get_vif_state:
    #         allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
    #         pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
    #
    #     report = setup_perfectoMobile_android[1]
    #     driver = setup_perfectoMobile_android[0]
    #     connData = get_ToggleAirplaneMode_data
    #
    #     # Set Wifi/AP Mode
    #     ip, is_internet = gets_ip_add_eap_and_does_not_forget_ssid(request, ssidName, identity, ttls_passwd,
    #                                                                setup_perfectoMobile_android, connData)
    #     #
    #     if is_internet:
    #         if ip:
    #             text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
    #         else:
    #             text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
    #         print(text_body)
    #         allure.attach(name="Connection Status: ", body=str(text_body))
    #
    #         # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
    #         Toggle_WifiMode_android(request, setup_perfectoMobile_android, ssidName, connData)
    #         ip_check, is_internet_check = gets_ip_add_for_checking_and_forgets_ssid(request, ssidName, identity,
    #                                                                                 ttls_passwd,
    #                                                                                 setup_perfectoMobile_android,
    #                                                                                 connData)
    #         if (ip_check == ip):
    #             assert True
    #         else:
    #             assert False
    #     else:
    #         allure.attach(name="Connection Status: ", body=str("No Internet access"))
    #         assert False
    #
    #
    #
    #

