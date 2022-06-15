import time
import pytest
import sys
import allure
import string
import random


if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

pytestmark = [pytest.mark.regression, pytest.mark.interop, pytest.mark.android, pytest.mark.interop_and, pytest.mark.ToggleWifiMode,
              pytest.mark.client_reconnect,pytest.mark.ToggleAirplaneMode]
from android_lib import closeApp, openApp, set_APconnMobileDevice_android, Toggle_AirplaneMode_android, Toggle_WifiMode_android, ForgetWifiConnection, openApp, get_ip_address_maverick_and, gets_ip_add_for_checking_and_forgets_ssid

@allure.feature("Maverick")
class TestMaverick(object):
    @pytest.mark.nolme
    def test_ap_maverick(self,request, lf_tools, setup_controller, get_vif_state, get_configuration, get_ToggleAirplaneMode_data, get_ToggleWifiMode_data, setup_perfectoMobile_android, get_APToMobileDevice_data, get_ap_logs, get_apnos):
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
            # print("reboot:")
            # print(reboot)

            iwinfo = ap_ssh.get_iwinfo()
            print("iwinfo:")
            print(iwinfo)
            # for i in iwinfo:
            #     print(i)
            #     print(iwinfo)
            #     # print(i[0])
            #     print('The result is:',i)
            #     # print(i.wlan0[0])
            for key, value in iwinfo.items():
                print(key, ' : ', value[0])
                ssidName = "Maverick-6AE4A3"
                ssidPassword = "[BLANK]"
                print("SSID_NAME: " + ssidName)
                print("SSID_PASS: " + ssidPassword)
                get_vif_state.append(ssidName)


            report = setup_perfectoMobile_android[1]
            driver = setup_perfectoMobile_android[0]
            connData = get_ToggleAirplaneMode_data

            ip, is_internet = get_ip_address_maverick_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            if ip:
                if is_internet:
                    text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
                else:
                    text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
                print(text_body)
                allure.attach(name="Connection Status: ", body=str(text_body))
                assert True
            else:
                allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
                assert False
            verifyUploadDownloadSpeed_mav_android(request, setup_perfectoMobile_android, get_APToMobileDevice_data)
            print("Succesfully displayed mav page!")
            assert True






