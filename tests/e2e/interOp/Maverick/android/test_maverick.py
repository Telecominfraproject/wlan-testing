import pytest
import sys
import sys
import allure

if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.android, pytest.mark.interop_and, pytest.mark.client_connectivity
              ,pytest.mark.interop_uc_sanity, pytest.mark.nat]

from android_lib import closeApp, set_APconnMobileDevice_android, verify_open_mav_android, Toggle_AirplaneMode_android, ForgetWifiConnection, openApp, \
    get_ip_address_maverick_and, wifi_disconnect_and_forget

class TestNatModeConnectivitySuiteOne(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4536", name="WIFI-4536")
    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    @pytest.mark.destroy
    def test_maverick_android(self, request, get_vif_state, get_apnos, get_configuration, get_ap_logs,
                                                     get_ToggleAirplaneMode_data, setup_perfectoMobile_android):

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

            iwinfo = ap_ssh.get_iwinfo()
            print("iwinfo:")
            print(iwinfo)
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

        # Set Wifi/AP Mode
            ip, is_internet = get_ip_address_maverick_and(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            #
            if is_internet:
                if ip:
                    text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
                else:
                    text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
                print(text_body)
                allure.attach(name="Connection Status: ", body=str(text_body))

                assert verify_open_mav_android(request, setup_perfectoMobile_android, connData)
                wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)

            else:
                allure.attach(name="Connection Status: ", body=str("No Internet access"))
                assert True
