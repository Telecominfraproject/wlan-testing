import pytest
import sys
import sys
import allure

if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.iOS, pytest.mark.interop_iOS, pytest.mark.client_connectivity
              ,pytest.mark.interop_uc_sanity, pytest.mark.nat]

from iOS_lib import closeApp, set_APconnMobileDevice_iOS, Toggle_AirplaneMode_iOS, ForgetWifiConnection, openApp, \
    get_ip_address_maverick_iOS,return_open_maverickpage_iOS, wifi_disconnect_and_forget

class TestMaverickIOS(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4536", name="WIFI-4536")
    @pytest.mark.maverickIOS
    @pytest.mark.destroyios
    def test_maverick_ios(self, request, get_vif_state, get_ap_logs,currentmav,
                                                     get_ToggleAirplaneMode_data, get_configuration, setup_perfectoMobile_iOS):

        ssidName = currentmav
        ssidPassword = "[BLANK]"
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_maverick_iOS(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            return_open_maverickpage_iOS(request, setup_perfectoMobile_iOS, connData)

        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert True
# @pytest.mark.Mavtraios
# def test_maverick_trail(self, request, get_vif_state, get_apnos, get_configuration, get_ap_logs,
#                                                  get_ToggleAirplaneMode_data, setup_perfectoMobile_iOS):
#     report = setup_perfectoMobile_iOS[1]
#     driver = setup_perfectoMobile_iOS[0]
#     connData = get_ToggleAirplaneMode_data
#
#     return_open_maverick_iOS(request, setup_perfectoMobile_iOS, connData)
#     assert True

