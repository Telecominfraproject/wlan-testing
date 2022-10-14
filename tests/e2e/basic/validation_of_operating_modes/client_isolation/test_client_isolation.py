"""
    Test Client Isolation: Bridge Mode
    pytest -m client_isolation
"""

import time
import allure
import pytest

pytestmark = [pytest.mark.client_isolation, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {
                "ssid_name": "ci_enabled_wpa2_ssid1_2g",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            },
            {
                "ssid_name": "ci_enabled_wpa2_ssid2_2g",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            },
            {
                "ssid_name": "ci_enabled_wpa2_ssid1_5g",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            },
            {
                "ssid_name": "ci_enabled_wpa2_ssid2_5g",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            }
        ]
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestClientIsolationEnabled(object):
    """
        Test Config with Enabling Client Isolation in SSIDs
        pytest -m "client_isolation and ci_enabled and bridge"
    """
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.ci_enabled_in_5g_ssid
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10610", name="WIFI-10610")
    def test_client_isolation_enabled_ssid_5g(self, lf_test, lf_tools, update_report, test_cases,
                                               station_names_fiveg, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][2]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][3]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name = lf_test.fiveg_radios[0]
        sta = []
        for i in range(2):
            sta.append(station_list + str(i))
        print("station-list :", sta)

        allure.attach(name="testcase-details", body="Verify the connectivity of 2 clients connected to the different "
                                                    "SSID by enabling the client isolation in both the SSID's.(5Ghz)")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general["ssid_modes"]["wpa2_personal"][2]))
        allure.attach(name="station2_ssid-info", body=str(setup_params_general["ssid_modes"]["wpa2_personal"][3]))
        station_result1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name1, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name, station_name=[sta[0]])
        station_result2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name2, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name, station_name=[sta[1]])
        print("station results 1  :", station_result1)
        print("station results 2  :", station_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta,side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="rx drop % endp-a", body=str(rx_data["Unsetsta10000-0"]["rx drop % a"]))
        allure.attach(name="rx drop % endp-b", body=str(rx_data["Unsetsta10000-0"]["rx drop % b"]))
        if not station_result1 and station_result2:
            print("Test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta10000-0"]["rx drop % a"] and rx_data["Unsetsta10000-0"]["rx drop % b"] == 100:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
                else:
                    print("Test pass, traffic ran between two stations when isolation enabled in both 5g ssids.")
                    assert True
            else:
                print("Layer3 not ran properly.")

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.ci_enabled_in_2g_ssid
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10620", name="WIFI-10620")
    def test_client_isolation_enabled_with_2g(self, lf_test, lf_tools, update_report, test_cases,
                                              station_names_twog, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_twog[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name = lf_test.twog_radios[0]

        allure.attach(name="testcase-details", body="Run traffic between eth2 port (AP) and station "
                                                    "(with client isolation enabled) -2.4GHz")
        allure.attach(name="station_ssid-info", body=str(setup_params_general["ssid_modes"]["wpa2_personal"][0]))
        station_result = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=security_key,
                                                             security=security, mode=mode, radio=radio_name,
                                                             station_name=[station_list])
        print(station_result)

        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=[station_list], side_b="")
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="rx drop % endp-a", body=str(rx_data["Unsetsta0000-0"]["rx drop % a"]))
        allure.attach(name="rx drop % endp-b", body=str(rx_data["Unsetsta0000-0"]["rx drop % b"]))
        if not station_result:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta0000-0"]["rx drop % a"] and rx_data["Unsetsta0000-0"]["rx drop % b"] == 100:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
                else:
                    print("Test pass, traffic ran between eth2 and station when isolation enabled in one 2g ssid.")
                    assert True
            else:
                print("Layer3 not ran properly.")



    # clients_connected to different ssid, enabling isolation in both(2.4GH)
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.ci_ebabled_in_2g
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10602",name="WIFI-10602")
    def test_client_isolation_enabled_ssids_2g(self,lf_test, lf_tools, update_report, test_cases,
                                                 station_names_twog,get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_twog[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name = lf_test.twog_radios[0]
        sta = []
        for i in range(2):
            sta.append(station_list + str(i))
        print("station-list :", sta)

        allure.attach(name="testcase-details", body="Verify the connectivity of 2 clients connected to the different "
                                                    "SSID by enabling the client isolation in both the SSID's.(2.4Ghz)")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general["ssid_modes"]["wpa2_personal"][0]))
        allure.attach(name="station2_ssid-info", body=str(setup_params_general["ssid_modes"]["wpa2_personal"][1]))
        station_result1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name1, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name, station_name=[sta[0]])
        station_result2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name2, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name, station_name=[sta[1]])
        print("station results 1  :", station_result1)
        print("station results 2  :", station_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta, side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="rx drop % endp-a", body=str(rx_data["Unsetsta00000-0"]["rx drop % a"]))
        allure.attach(name="rx drop % endp-b", body=str(rx_data["Unsetsta00000-0"]["rx drop % b"]))
        if not station_result1 and station_result2:
            print("Test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta00000-0"]["rx drop % a"] and rx_data["Unsetsta00000-0"]["rx drop % b"] == 100:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
                else:
                    print("Test pass, traffic ran between two stations when isolation enabled in both 2g ssids.")
                    assert True
            else:
                print("Layer3 not ran properly.")


    # Running traffic between eth2 to station with client-isolation enabled in (5GH) ssid
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.eth_to_5g_station_true
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10621", name="WIFI-10621")
    def test_client_isolation_enabled_with_5g(self, lf_test, lf_tools, update_report, test_cases,
                                              station_names_fiveg, get_configuration):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][2]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name = lf_test.fiveg_radios[0]

        allure.attach(name="testcase-details", body="Run traffic between eth2 port (AP) and station "
                                                    "(with client isolation enabled) -5GHz")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general["ssid_modes"]["wpa2_personal"][2]))
        station_result = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=security_key,
                                                             security=security, mode=mode, radio=radio_name,
                                                             station_name=[station_list])
        print(station_result)

        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=[station_list], side_b="")
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="rx drop % endp-a", body=str(rx_data["Unsetsta1000-0"]["rx drop % a"]))
        allure.attach(name="rx drop % endp-b", body=str(rx_data["Unsetsta1000-0"]["rx drop % b"]))
        if not station_result:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta1000-0"]["rx drop % a"] and rx_data["Unsetsta1000-0"]["rx drop % b"] == 100:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
                else:
                    print("Test pass, traffic ran between eth2 and station when isolation enabled in one 5g ssid.")
                    assert True
            else:
                print("Layer3 not ran properly.")


setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {
                "ssid_name": "ci_disabled_wpa2_ssid1_2g",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            },
            {
                "ssid_name": "ci_disabled_wpa2_ssid2_2g",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            },
            {
                "ssid_name": "ci_disabled_wpa2_ssid1_5g",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            },
            {
                "ssid_name": "ci_disabled_wpa2_ssid2_5g",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            }
        ]
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestClientIsolationDisabled(object):
    """
        Test Config with Enabling Client Isolation in SSIDs
        pytest -m "client_isolation and ci_disabled and bridge"
    """
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.ci_disabled_in_2g_ssid
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10603", name="WIFI-10603")
    def test_client_isolation_disabled_ssids_2g(self, lf_test, lf_tools, update_report, test_cases,
                                               station_names_twog, get_configuration):

        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][0]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][1]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_twog[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name = lf_test.twog_radios[0]
        sta = []
        for i in range(2):
            sta.append(station_list + str(i))
        print("station-list :", sta)

        allure.attach(name="testcase-details", body="Verify the connectivity of 2 clients connected to the different "
                                                    "SSID disabling the client isolation(2.4Ghz)")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general1["ssid_modes"]["wpa2_personal"][0]))
        allure.attach(name="station2_ssid-info", body=str(setup_params_general1["ssid_modes"]["wpa2_personal"][1]))
        station_result1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name1, passkey=security_key,
                                                             security=security, mode=mode, radio=radio_name,
                                                             station_name=[sta[0]])
        station_result2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name2, passkey=security_key,
                                                             security=security, mode=mode, radio=radio_name,
                                                             station_name=[sta[1]])
        print("station results 1  :", station_result1)
        print("station results 2  :", station_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta, side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="rx drop % endp-a", body=str(rx_data["Unsetsta00000-0"]["rx drop % a"]))
        allure.attach(name="rx drop % endp-b", body=str(rx_data["Unsetsta00000-0"]["rx drop % b"]))
        if not station_result1 and station_result2:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta00000-0"]["rx drop % a"] and rx_data["Unsetsta00000-0"]["rx drop % b"] == 100:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
                else:
                    print("Test pass, traffic ran between two stations when isolation disabled in both 2g ssids.")
                    assert True
            else:
                print("Layer3 not ran properly.")

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.eth_to_2g_station_false
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10624", name="WIFI-10624")
    def test_client_isolation_disabled_with_2g(self, lf_test, lf_tools, update_report, test_cases,
                                         station_names_twog, get_configuration):

        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_twog[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name = lf_test.twog_radios[0]

        allure.attach(name="testcase-details", body="Run traffic between eth2 port (AP) and station "
                                                    "(with client isolation disabled) -2.4GHz")
        allure.attach(name="station_ssid-info", body=str(setup_params_general1["ssid_modes"]["wpa2_personal"][0]))
        station_result = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=security_key,
                                                            security=security, mode=mode, radio=radio_name,
                                                            station_name=[station_list])
        print(station_result)

        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=[station_list], side_b="")
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="rx drop % endp-a", body=str(rx_data["Unsetsta0000-0"]["rx drop % a"]))
        allure.attach(name="rx drop % endp-b", body=str(rx_data["Unsetsta0000-0"]["rx drop % b"]))
        if not station_result:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta0000-0"]["rx drop % a"] and rx_data["Unsetsta0000-0"]["rx drop % b"] == 100:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
                else:
                    print("Test pass, traffic ran between eth2 and station when isolation disabled in one 2g ssid.")
                    assert True
            else:
                print("Layer3 not ran properly.")

    # clients_connected to different ssid, disabling isolation in both(5GH)
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.ci_disabled_in_5g_ssid
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10611",name="WIFI-10611")
    def test_client_isolation_disabled_ssid_5g(self,lf_test, lf_tools, update_report, test_cases,
                                                 station_names_fiveg,get_configuration):

        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][2]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][3]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name = lf_test.fiveg_radios[0]
        sta = []
        for i in range(2):
            sta.append(station_list + str(i))
        print("station-list :", sta)

        allure.attach(name="testcase-details", body="Verify the connectivity of 2 clients connected to the different "
                                                    "SSID disabling the client isolation(5Ghz)")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general1["ssid_modes"]["wpa2_personal"][2]))
        allure.attach(name="station2_ssid-info", body=str(setup_params_general1["ssid_modes"]["wpa2_personal"][3]))
        station_result1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name1, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name, station_name=[sta[0]])
        station_result2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name2, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name, station_name=[sta[1]])
        print("station results 1  :", station_result1)
        print("station results 2  :", station_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta, side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="rx drop % endp-a", body=str(rx_data["Unsetsta10000-0"]["rx drop % a"]))
        allure.attach(name="rx drop % endp-b", body=str(rx_data["Unsetsta10000-0"]["rx drop % b"]))
        if not station_result1 and station_result2:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta10000-0"]["rx drop % a"] and rx_data["Unsetsta10000-0"]["rx drop % b"] == 100:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
                else:
                    print("Test pass, traffic ran between two stations when isolation disabled in both 5g ssids.")
                    assert True
            else:
                print("Layer3 not ran properly.")

    # Running traffic between eth2 to station with client-isolation disabled in (5GH) ssid
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.eth_to_5g_station_false
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10623", name="WIFI-10623")
    def test_client_isolation_disabled_with_5g(self, lf_test, lf_tools, update_report, test_cases,
                                         station_names_fiveg, get_configuration):

        profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][2]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name = lf_test.fiveg_radios[0]

        allure.attach(name="testcase-details", body="Run traffic between eth2 port (AP) and station "
                                                    "(with client isolation disabled) -5GHz")
        allure.attach(name="station_ssid-info", body=str(setup_params_general1["ssid_modes"]["wpa2_personal"][2]))
        station_result = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=security_key,
                                                             security=security, mode=mode, radio=radio_name,
                                                             station_name=[station_list])
        print(station_result)

        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=[station_list], side_b="")
        print("layer3 results:", layer3_restult)

        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="rx drop % endp-a", body=str(rx_data["Unsetsta1000-0"]["rx drop % a"]))
        allure.attach(name="rx drop % endp-b", body=str(rx_data["Unsetsta1000-0"]["rx drop % b"]))
        if not station_result:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta1000-0"]["rx drop % a"] and rx_data["Unsetsta1000-0"]["rx drop % b"] == 100:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
                else:
                    print("Test pass, traffic ran between eth2 and stations when isolation disabled in one 5g ssid.")
                    assert True
            else:
                print("Layer3 not ran properly.")


setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {
                "ssid_name": "ci_enabled_wpa2_ssid",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            },
            {
                "ssid_name": "ci_disabled_wpa2_ssid",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            },
            {
                "ssid_name": "ci_enabled_wpa2_ssid",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            },
            {
                "ssid_name": "ci_disabled_wpa2_ssid",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            },
        ]
    },
    "rf": {},
    "radius": False
}
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestClientIsolationSameSSID(object):
    """
        Test Config with Enabling Client Isolation in SSIDs
        pytest -m "client_isolation and ci_disabled and bridge"
    """
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.same_ssid_enabling_isolation_2g
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10601", name="WIFI-10601")
    def test_cleint_isolation_enabled_same_ssid_2g(self, lf_test, lf_tools, update_report,
                                               station_names_twog, get_configuration):

        profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_twog[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name = lf_test.twog_radios[0]
        sta = []
        for i in range(2):
            sta.append(station_list + str(i))
        print("station-list :", sta)

        allure.attach(name="testcase-details", body="Verify the connectivity of 2 clients connected to the same "
                                                    "SSID without enabling the client isolation.(2.4Ghz)")
        allure.attach(name="station_ssid-info", body=str(setup_params_general2["ssid_modes"]["wpa2_personal"][0]))
        station_result = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=security_key,
                                                            security=security, mode=mode, radio=radio_name,
                                                            station_name=sta)
        print("station results :", station_result)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta, side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("Waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="rx drop % endp-a", body=str(rx_data["Unsetsta00000-0"]["rx drop % a"]))
        allure.attach(name="rx drop % endp-b", body=str(rx_data["Unsetsta00000-0"]["rx drop % b"]))
        if not station_result:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta00000-0"]["rx drop % a"] and rx_data["Unsetsta00000-0"]["rx drop % b"] == 100:
                    print("Test paseed,Packet drop has 100%")
                    assert True
                else:
                    print("Test fail, traffic ran between two stations when isolation enabled in both 2g same-ssid.")
                    assert False
            else:
                print("Layer3 not ran properly.")

    # clients_connected to same ssid, disabled isolation(2.4GH)
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.same_ssid_disabling_isolation_2g
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 2.4 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10604",name="WIFI-10604")
    def test_cleint_isolation_disabled_same_ssid_2g(self,lf_test, lf_tools, update_report,
                                             station_names_twog, get_configuration):

        profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_twog[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name = lf_test.twog_radios[0]
        sta = []
        for i in range(2):
            sta.append(station_list + str(i))
        print("station-list :", sta)

        allure.attach(name="testcase-details", body="Verify the connectivity of 2 clients connected to the same "
                                                    "SSID without enabling the client isolation.(2.4Ghz)")
        allure.attach(name="station_ssid-info", body=str(setup_params_general2["ssid_modes"]["wpa2_personal"][1]))
        station_result = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=security_key,
                                                            security=security, mode=mode, radio=radio_name,
                                                            station_name=sta)
        print("station results :", station_result)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta, side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="rx drop % endp-a", body=str(rx_data["Unsetsta00000-0"]["rx drop % a"]))
        allure.attach(name="rx drop % endp-b", body=str(rx_data["Unsetsta00000-0"]["rx drop % b"]))
        if not station_result:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta00000-0"]["rx drop % a"] and rx_data["Unsetsta00000-0"]["rx drop % b"] == 100:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
                else:
                    print("Test pass, traffic ran between two stations when isolation disabled in both 2g same-ssid.")
                    assert True
            else:
                print("Layer3 not ran properly.")

    # clients_connected to same ssid, enabled isolation(5GHZ)
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.same_ssid_enabling_isolation_5g
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10606", name="WIFI-10606")
    def test_cleint_isolation_enabled_same_ssid_5g(self, lf_test, lf_tools, update_report, test_cases,
                                              station_names_fiveg, get_configuration):

        profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][2]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name = lf_test.fiveg_radios[0]
        sta = []
        for i in range(2):
            sta.append(station_list + str(i))
        print("station-list :", sta)

        allure.attach(name="testcase-details", body="Verify the connectivity of 2 clients connected to the same "
                                                    "SSID by enabling client isolation.(5Ghz)")
        allure.attach(name="station_ssid-info", body=str(setup_params_general2["ssid_modes"]["wpa2_personal"][2]))
        station_result = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=security_key,
                                                            security=security, mode=mode, radio=radio_name,
                                                            station_name=sta)
        print("station results :", station_result)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta, side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="rx drop % endp-a", body=str(rx_data["Unsetsta10000-0"]["rx drop % a"]))
        allure.attach(name="rx drop % endp-b", body=str(rx_data["Unsetsta10000-0"]["rx drop % b"]))
        if not station_result:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta10000-0"]["rx drop % a"] and rx_data["Unsetsta10000-0"]["rx drop % b"] == 100:
                    print("Test paseed,Packet drop has 100%")
                    assert True
                else:
                    print("Test fail, traffic ran between two stations when isolation enabled in both 5g same-ssid.")
                    assert False
            else:
                print("Layer3 not ran properly.")

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.same_ssid_disabling_isolation_5g
    @allure.title("BRIDGE Mode Client Isolation with wpa2_personal encription 5 GHz Band")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10612", name="WIFI-10612")
    def test_cleint_isolation_disabled_same_ssid_5g(self, lf_test, lf_tools, update_report, test_cases,
                                              station_names_fiveg, get_configuration):

        profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][3]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name = lf_test.fiveg_radios[0]
        sta = []
        for i in range(2):
            sta.append(station_list + str(i))
        print("station-list :", sta)

        allure.attach(name="testcase-details", body="Verify the connectivity of 2 clients connected to the same "
                                                    "SSID disabling the client isolation.(5Ghz)")
        allure.attach(name="station_ssid-info", body=str(setup_params_general2["ssid_modes"]["wpa2_personal"][3]))
        station_result = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=security_key,
                                                            security=security, mode=mode, radio=radio_name,
                                                            station_name=sta)
        print("station results :", station_result)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta, side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="rx drop % endp-a", body=str(rx_data["Unsetsta10000-0"]["rx drop % a"]))
        allure.attach(name="rx drop % endp-b", body=str(rx_data["Unsetsta10000-0"]["rx drop % b"]))
        if not station_result:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta10000-0"]["rx drop % a"] and rx_data["Unsetsta10000-0"]["rx drop % b"] == 100:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
                else:
                    print("Test pass, traffic ran between two stations when isolation disabled in both 5g same-ssid.")
                    assert True
            else:
                print("Layer3 not ran properly.")


setup_params_general3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {
                "ssid_name": "ci_enabled_wpa2_ssid1_2g",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            },
            {
                "ssid_name": "ci_disabled_wpa2_ssid2_2g",
                "appliedRadios": ["2G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            },
            {
                "ssid_name": "ci_enabled_wpa2_ssid1_5g",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": True
            },
            {
                "ssid_name": "ci_disabled_wpa2_ssid2_5g",
                "appliedRadios": ["5G"],
                "security": "psk2",
                "security_key": "OpenWifi",
                "isolate-clients": False
            }
        ]
    },
    "rf": {},
    "radius": False
}
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general3],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestClientIsolationDifferentSSID(object):
    """
        Test Config with Enabling Client Isolation in SSIDs
        pytest -m "client_isolation and ci_disabled and bridge"
    """

    # clients_connected to different ssid,enabling isolation in ssid (2GH)& isolation disabled in ssid (2GHZ)
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.ci_enable_and_disable_2g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10605", name="WIFI-10605")
    def test_client_isoaltion_enabled_ssid_2g_disabled_ssid_2g(self, lf_test, lf_tools, update_report, test_cases,
                                                               station_names_twog, get_configuration):

        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][0]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][1]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_twog[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name = lf_test.twog_radios[0]
        sta = []
        for i in range(2):
            sta.append(station_list + str(i))
        print("station-list : ----->", sta)

        allure.attach(name="testcase-details", body="Verify the connectivity of 2 clients connected to different "
                                                    "SSID's where Client isolation is enabled in one and disabled "
                                                    "in other.(2.4Ghz)")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][0]))
        allure.attach(name="station2_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][1]))
        station_result1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name1, passkey=security_key,
                                                             security=security, mode=mode, radio=radio_name,
                                                             station_name=[sta[0]])
        station_result2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name2, passkey=security_key,
                                                             security=security, mode=mode, radio=radio_name,
                                                             station_name=[sta[1]])
        print("station results 1  :", station_result1)
        print("station results 2  :", station_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta, side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="rx drop % endp-a", body=str(rx_data["Unsetsta00000-0"]["rx drop % a"]))
        allure.attach(name="rx drop % endp-b", body=str(rx_data["Unsetsta00000-0"]["rx drop % b"]))
        if not station_result1 and station_result2:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta00000-0"]["rx drop % a"] and rx_data["Unsetsta00000-0"]["rx drop % b"] == 100:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
                else:
                    print("Test pass, traffic ran between two stations when isolation enabled in one 2g ssid disabled in another.")
                    assert True
            else:
                print("Layer3 not ran properly.")


    # clients_connected to different ssid,enabling isolation in ssid (5GH)& isolation disabled in ssid (5GHZ)
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.ci_enable_and_disable_5g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10613", name="WIFI-10613")
    def test_client_isoaltion_enabled_ssid_5g_disabled_ssid_5g(self, lf_test, lf_tools, update_report, test_cases,
                                                                station_names_fiveg, get_configuration):

        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][2]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][3]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name = lf_test.fiveg_radios[0]
        sta = []
        for i in range(2):
            sta.append(station_list + str(i))
        print("station-list : ----->", sta)

        allure.attach(name="testcase-details", body="Verify the connectivity of 2 clients connected to different "
                                                    "SSID's where Client isolation is enabled in one and disabled "
                                                    "in other.(5Ghz)")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][2]))
        allure.attach(name="station2_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][3]))
        station_result1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name1, passkey=security_key,
                                                             security=security, mode=mode, radio=radio_name,
                                                             station_name=[sta[0]])
        station_result2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name2, passkey=security_key,
                                                             security=security, mode=mode, radio=radio_name,
                                                             station_name=[sta[1]])
        print("station results 1  :", station_result1)
        print("station results 2  :", station_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta, side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="rx drop % endp-a", body=str(rx_data["Unsetsta10000-0"]["rx drop % a"]))
        allure.attach(name="rx drop % endp-b", body=str(rx_data["Unsetsta10000-0"]["rx drop % b"]))
        if not station_result1 and station_result2:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta10000-0"]["rx drop % a"] and rx_data["Unsetsta10000-0"]["rx drop % b"] == 100:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
                else:
                    print("Test pass, traffic ran between two stations when isolation enabled in one 5g and disabled in another.")
                    assert True
            else:
                print("Layer3 not ran properly.")

    # run traffic from 2g to 5g
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.twog
    @pytest.mark.ci_enabled_2g_and_5g_traffic_2g_to_5g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10616", name="WIFI-10616")
    def test_client_isolation_enabled_ssid2g_and_ssid5g(self, lf_test, lf_tools, update_report, test_cases,
                                                          station_names_twog, station_names_fiveg, get_configuration):

        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][0]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][2]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog[0]
        station_list2 = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name1 = lf_test.twog_radios[0]
        radio_name2 = lf_test.fiveg_radios[0]
        sta = []
        for i in range(1):
            sta.append(station_list1 + str(i))
            sta.append(station_list2 + str(i))
        print("station-list : ----->", sta)

        allure.attach(name="testcase-details", body=" Verify the connectivity of 2 clients connected to different "
                                                    "SSID's where Client isolation is enabled in 2G SSID and 5G SSID"
                                                    "(run traffic from 2G client to 5G client)")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][0]))
        allure.attach(name="station2_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][2]))
        station_result1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name1, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name1, station_name=[sta[0]])
        station_result2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name2, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name2, station_name=[sta[1]])
        print("station results 1  :", station_result1)
        print("station results 2  :", station_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta,side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="bps rx endp-a", body=str(rx_data["Unsetsta00000-0"]["bps rx a"]))
        allure.attach(name="bps rx endp-b", body=str(rx_data["Unsetsta00000-0"]["bps rx b"]))
        if not station_result1 and station_result2:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta00000-0"]["bps rx a"] == 0 and rx_data["Unsetsta00000-0"]["bps rx b"] != 0:
                    print("Test pass, traffic ran between 2g to 5g stations when isolation enabled in 2g and 5g ssid.")
                    assert True
                else:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
            else:
                print("Layer3 not ran properly.")

    # run traffic from 2g to 5g
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.twog
    @pytest.mark.ci_disable_2g_and_5g_traffic_2g_to_5g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10618",name="WIFI-10618")
    def test_client_isolation_disabled_ssid2g_and_ssid5g(self, lf_test, lf_tools, update_report, test_cases,
                                                 station_names_twog, station_names_fiveg, get_configuration):

        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][1]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][3]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog[0]
        station_list2 = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name1 = lf_test.twog_radios[0]
        radio_name2 = lf_test.fiveg_radios[0]
        sta = []
        for i in range(1):
            sta.append(station_list1 + str(i))
            sta.append(station_list2 + str(i))
        print("station-list : ----->", sta)

        allure.attach(name="testcase-details", body=" Verify the connectivity of 2 clients connected to different "
                                                    "SSID's where Client isolation is disabled in 2G SSID and 5G SSID "
                                                    "(run traffic from 2G client to 5G client)")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][1]))
        allure.attach(name="station2_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][3]))
        station_result1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name1, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name1, station_name=[sta[0]])
        station_result2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name2, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name2, station_name=[sta[1]])
        print("station results 1  :", station_result1)
        print("station results 2  :", station_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta,side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="bps rx endp-a", body=str(rx_data["Unsetsta00000-0"]["bps rx a"]))
        allure.attach(name="bps rx endp-b", body=str(rx_data["Unsetsta00000-0"]["bps rx b"]))
        if not station_result1 and station_result2:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta00000-0"]["bps rx a"] == 0 and rx_data["Unsetsta00000-0"]["bps rx b"] != 0:
                    print("Test pass, traffic ran between 2g to 5g stations when isolation disabled in 2g and 5g ssid.")
                    assert True
                else:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
            else:
                print("Layer3 not ran properly.")

    # clients_connected to different ssid, enabling isolation in both (2GHz) & (5GHz) ssid
    # run traffic from 5g to 2g
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.twog
    @pytest.mark.ci_enabled_2g_and_5g_traffic_5g_to_2g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10617", name="WIFI-10617")
    def test_client_isolation_enabled_ssid_2gandssid_5g(self, lf_test, lf_tools, update_report, test_cases,
                                                          station_names_twog, station_names_fiveg, get_configuration):

        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][0]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][2]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog[0]
        station_list2 = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name1 = lf_test.twog_radios[0]
        radio_name2 = lf_test.fiveg_radios[0]
        sta = []
        for i in range(1):
            sta.append(station_list1 + str(i))
            sta.append(station_list2 + str(i))
        print("station-list : ----->", sta)

        allure.attach(name="testcase-details", body=" Verify the connectivity of 2 clients connected to different "
                                                    "SSID's where Client isolation is enabled in 2G SSID and 5G SSID "
                                                    "(run traffic from 5G client to 2G client)")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][0]))
        allure.attach(name="station2_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][2]))
        station_result1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name1, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name1, station_name=[sta[0]])
        station_result2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name2, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name2, station_name=[sta[1]])
        print("station results 1  :", station_result1)
        print("station results 2  :", station_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=0, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta,side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="bps rx endp-a", body=str(rx_data["Unsetsta00000-0"]["bps rx a"]))
        allure.attach(name="bps rx endp-b", body=str(rx_data["Unsetsta00000-0"]["bps rx b"]))
        if not station_result1 and station_result2:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta00000-0"]["bps rx a"] != 0 and rx_data["Unsetsta00000-0"]["bps rx b"] == 0:
                    print("Test pass, traffic ran between 5g to 2g stations when isolation enabled in 2g and 5g ssid.")
                    assert True
                else:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
            else:
                print("Layer3 not ran properly.")

    # clients_connected to different ssid, disabled isolation in both (2GHz) & (5GHz) ssid
    # run traffic from 5g to 2g
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.twog
    @pytest.mark.ci_disable_2g_and_5g_traffic_5g_to_2g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10619",name="WIFI-10619")
    def test_client_isolation_disabled_ssid_2gandssid_5g(self, lf_test, lf_tools, update_report, test_cases,
                                                 station_names_twog,station_names_fiveg,get_configuration):

        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][1]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][3]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog[0]
        station_list2 = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name1 = lf_test.twog_radios[0]
        radio_name2 = lf_test.fiveg_radios[0]
        sta = []
        for i in range(1):
            sta.append(station_list1 + str(i))
            sta.append(station_list2 + str(i))
        print("station-list : ----->", sta)

        allure.attach(name="testcase-details", body="Verify the connectivity of 2 clients connected to different "
                                                    "SSID's where Client isolation is disabled in 2G SSID and 5G SSID"
                                                    "(run traffic from 5G client to 2G client)")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][1]))
        allure.attach(name="station2_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][3]))
        station_result1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name1, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name1, station_name=[sta[0]])
        station_result2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name2, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name2, station_name=[sta[1]])
        print("station results 1  :", station_result1)
        print("station results 2  :", station_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=0, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta,side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="bps rx endp-a", body=str(rx_data["Unsetsta00000-0"]["bps rx a"]))
        allure.attach(name="bps rx endp-b", body=str(rx_data["Unsetsta00000-0"]["bps rx b"]))
        if not station_result1 and station_result2:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta00000-0"]["bps rx a"] != 0 and rx_data["Unsetsta00000-0"]["bps rx b"] == 0:
                    print("Test pass, traffic ran between 5g to 2g stations when isolation disabled in 2g and 5g ssid.")
                    assert True
                else:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
            else:
                print("Layer3 not ran properly.")

    # run traffic from 2g to 5g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_enabled_2g_disabled_5g_traffic_2g_to_5g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10614", name="WIFI-10614")
    def test_client_isolation_enabled_ssids_2gdisabled_ssid_5g(self, lf_test, lf_tools,update_report, test_cases,
                                                               station_names_twog, station_names_fiveg, get_ap_channel):
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][0]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][3]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog[0]
        station_list2 = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name1 = lf_test.twog_radios[0]
        radio_name2 = lf_test.fiveg_radios[0]
        sta = []
        for i in range(1):
            sta.append(station_list1 + str(i))
            sta.append(station_list2 + str(i))
        print("station-list : ----->", sta)

        allure.attach(name="testcase-details", body=" Verify the connectivity of 2 clients connected to different "
                                                    "SSID's where Client isolation is enabled in 2G SSID and disabled"
                                                    " in 5G SSID (run traffic from 2G client to 5G client)")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][0]))
        allure.attach(name="station2_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][3]))
        station_result1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name1, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name1, station_name=[sta[0]])
        station_result2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name2, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name2, station_name=[sta[1]])
        print("station results 1  :", station_result1)
        print("station results 2  :", station_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta,side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="bps rx endp-a", body=str(rx_data["Unsetsta00000-0"]["bps rx a"]))
        allure.attach(name="bps rx endp-b", body=str(rx_data["Unsetsta00000-0"]["bps rx b"]))
        if not station_result1 and station_result2:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta00000-0"]["bps rx a"] == 0 and rx_data["Unsetsta00000-0"]["bps rx b"] != 0:
                    print("Test pass, traffic ran between 2g to 5g stations when isolation enabled in 2g and disabled 5g ssid.")
                    assert True
                else:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
            else:
                print("Layer3 not ran properly.")

    # run traffic from 5g to 2g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_disabled_2g_enabled_5g_traffic_5g_to_2g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10625", name="WIFI-10625")
    def test_client_isolation_disabled_ssid_2genabled_ssid_5g(self, lf_test, lf_tools, update_report,test_cases,
                                                      station_names_twog,station_names_fiveg, get_configuration):

        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][1]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][2]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog[0]
        station_list2 = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name1 = lf_test.twog_radios[0]
        radio_name2 = lf_test.fiveg_radios[0]
        sta = []
        for i in range(1):
            sta.append(station_list1 + str(i))
            sta.append(station_list2 + str(i))
        print("station-list : ----->", sta)

        allure.attach(name="testcase-details", body=" Verify the connectivity of 2 clients connected to different "
                                                    "SSID's where Client isolation is disabled in 2G SSID and enabled"
                                                    " in 5G SSID (run traffic from 5G client to 2G client)")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][1]))
        allure.attach(name="station2_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][2]))
        station_result1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name1, passkey=security_key,
                                                             security=security, mode=mode, radio=radio_name1,
                                                             station_name=[sta[0]])
        station_result2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name2, passkey=security_key,
                                                             security=security, mode=mode, radio=radio_name2,
                                                             station_name=[sta[1]])
        print("station results 1  :", station_result1)
        print("station results 2  :", station_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=0, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta, side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="bps rx endp-a", body=str(rx_data["Unsetsta00000-0"]["bps rx a"]))
        allure.attach(name="bps rx endp-b", body=str(rx_data["Unsetsta00000-0"]["bps rx b"]))
        if not station_result1 and station_result2:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta00000-0"]["bps rx a"] != 0 and rx_data["Unsetsta00000-0"]["bps rx b"] == 0:
                    print("Test pass, traffic ran between 5g to 2g stations when isolation disabled in 2g and enabled 5g ssid.")
                    assert True
                else:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
            else:
                print("Layer3 not ran properly.")


    # clients_connected to different ssid,enabled isolation in (2GHz)ssid & isolation disabled in (5GH)ssid
    # run traffic from 5g to 2g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_enabled_2g_disabled_5g_traffic_5g_to_2g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10615",name="WIFI-10615")
    def test_client_isolation_enabled_ssids_2g_disabled_ssid_5g(self, lf_test, lf_tools, update_report,test_cases,
                                                                station_names_twog,station_names_fiveg,get_ap_channel):

        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][0]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][3]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog[0]
        station_list2 = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name1 = lf_test.twog_radios[0]
        radio_name2 = lf_test.fiveg_radios[0]
        sta = []
        for i in range(1):
            sta.append(station_list1 + str(i))
            sta.append(station_list2 + str(i))
        print("station-list : ----->", sta)

        allure.attach(name="testcase-details", body="Verify the connectivity of 2 clients connected to "
                                                    "different SSID's where Client isolation is enabled in 2G SSID "
                                                    "and disabled in 5G SSID (run traffic from 5G client to 2G client)")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][0]))
        allure.attach(name="station2_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][3]))
        station_result1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name1, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name1, station_name=[sta[0]])
        station_result2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name2, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name2, station_name=[sta[1]])
        print("station results 1  :", station_result1)
        print("station results 2  :", station_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=0, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta,side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="bps rx endp-a", body=str(rx_data["Unsetsta00000-0"]["bps rx a"]))
        allure.attach(name="bps rx endp-b", body=str(rx_data["Unsetsta00000-0"]["bps rx b"]))
        if not station_result1 and station_result2:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta00000-0"]["bps rx a"] != 0 and rx_data["Unsetsta00000-0"]["bps rx b"] == 0:
                    print("Test pass, traffic ran between 5g to 2g stations when isolation disabled in 2g and enabled 5g ssid.")
                    assert True
                else:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
            else:
                print("Layer3 not ran properly.")

    # clients_connected to different ssid,disabled isolation in ssid (2GHz)& isolation enabled in ssid(5GH)
    # run traffic from 2g to 5g
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.ci_disabled_2g_enabled_5g_traffic_2g_to_5g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-10626", name="WIFI-10626")
    def test_client_isolation_disabled_ssid_2g_enabled_ssid_5g(self, lf_test, lf_tools, update_report,test_cases,
                                                      station_names_twog,station_names_fiveg, get_configuration):

        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][1]
        ssid_name1 = profile_data["ssid_name"]
        profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][2]
        ssid_name2 = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        station_list1 = station_names_twog[0]
        station_list2 = station_names_fiveg[0]
        security = "wpa2"
        mode = "BRIDGE"
        radio_name1 = lf_test.twog_radios[0]
        radio_name2 = lf_test.fiveg_radios[0]
        sta = []
        for i in range(1):
            sta.append(station_list1 + str(i))
            sta.append(station_list2 + str(i))
        print("station-list : ----->", sta)

        allure.attach(name="testcase-details", body="Verify the connectivity of 2 clients connected to different "
                                                    "SSID's where Client isolation is disabled in 2G SSID and enabled"
                                                    " in 5G SSID (run traffic from 2G client to 5G client)")
        allure.attach(name="station1_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][1]))
        allure.attach(name="station2_ssid-info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"][2]))
        station_result1 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name1, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name1, station_name=[sta[0]])
        station_result2 = lf_test.Client_Connect_Using_Radio(ssid=ssid_name2, passkey=security_key,
                                             security=security, mode=mode, radio=radio_name2, station_name=[sta[1]])
        print("station results 1  :", station_result1)
        print("station results 2  :", station_result2)
        layer3_restult = lf_test.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=0, side_b_max_rate=0,
                                               traffic_type="lf_udp", sta_list=sta,side_b=sta[1])
        print("layer3 results:", layer3_restult)
        print("waiting for 30 sec...")
        time.sleep(30)

        cx_list = lf_test.get_cx_list()
        rx_data = lf_tools.json_get(_req_url=f"cx/{cx_list[0]}")
        print("Rx data : ", rx_data)

        l3_cleanup = lf_test.l3_cleanup()
        print("layer3 cleaning result :", l3_cleanup)

        allure.attach(name="bps rx endp-a", body=str(rx_data["Unsetsta00000-0"]["bps rx a"]))
        allure.attach(name="bps rx endp-b", body=str(rx_data["Unsetsta00000-0"]["bps rx b"]))
        if not station_result1 and station_result2:
            print("test failed due to station has no ip")
            assert False
        else:
            print("Station creation passed. Successful.")
            if layer3_restult is None:
                print("Layer3 traffic ran.")
                if rx_data["Unsetsta00000-0"]["bps rx a"] == 0 and rx_data["Unsetsta00000-0"]["bps rx b"] != 0:
                    print("Test pass, traffic ran between 2g to 5g stations when isolation disabled in 2g and enabled 5g ssid.")
                    assert True
                else:
                    print("Test failed,Packet drop should not be 100%")
                    assert False
            else:
                print("Layer3 not ran properly.")
