import pytest
import allure
import sys



if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.android, pytest.mark.interop_and,
              pytest.mark.client_connectivity
    , pytest.mark.interop_uc_sanity, pytest.mark.nat]

from android_lib import closeApp, return_open_maverickpage_android, set_APconnMobileDevice_android, \
    Toggle_AirplaneMode_android, ForgetWifiConnection, openApp, \
    get_ip_address_maverick_and, wifi_disconnect_and_forget


class TestMaverickAndroid(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-4536", name="WIFI-4536")
    @pytest.mark.maverickAnd
    def test_maverick_android(self, request, get_vif_state, get_ap_logs, currentmav,
                              get_ToggleAirplaneMode_data,get_configuration, setup_perfectoMobile_android):
        ssidName = currentmav
        ssidPassword = "[BLANK]"
        print("SSID_NAME: " + ssidName)
        print("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_ToggleAirplaneMode_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_maverick_and(request, ssidName, ssidPassword, setup_perfectoMobile_android,
                                                      connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            return_open_maverickpage_android(request, setup_perfectoMobile_android, connData)
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert True

    # @pytest.mark.Mavtra
    # def test_maverick_trail(self, request, get_vif_state, get_apnos, get_configuration, get_ap_logs,
    #                         get_ToggleAirplaneMode_data, setup_perfectoMobile_android):
    #     report = setup_perfectoMobile_android[1]
    #     driver = setup_perfectoMobile_android[0]
    #     connData = get_ToggleAirplaneMode_data
    #
    #     return_open_maverickpage_android(request, setup_perfectoMobile_android, connData)
    #     assert True
