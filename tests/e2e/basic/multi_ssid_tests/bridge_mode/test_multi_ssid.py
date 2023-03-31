"""
    Multiple number of SSIDs Test: Bridge Mode
    pytest -m multi_ssid
"""
import logging
import time
import allure
import pytest
import tabulate

pytestmark = [pytest.mark.multi_ssid, pytest.mark.bridge]

setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {

        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],

    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi SSID Test")
@allure.parent_suite("MULTI SSID")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="Test Data Path for 1 SSID")
class TestMultiSsidDataPath1(object):
    """
        Multiple number of SSIDs Test: Bridge Mode
        pytest -m multi_ssid and one_ssid
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12227")
    @pytest.mark.wpa2_personal
    @pytest.mark.one_ssid
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.multi_ssid
    def test_one_ssid(self, get_test_library, get_dut_logs_per_test_case,
                      get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multi-SSID Bridge Mode
            pytest -m "multi_ssid and single_ssid"
        """
        mode = "BRIDGE"
        security_key = "something"
        security = "wpa2"
        sta_list1 = ["sta0001", "sta0002"]
        sta_list2 = ["sta0003", "sta0004"]
        stations_list = sta_list1 + sta_list2
        pass_fail, l3_data = [], {}
        pass_fail_data = []
        allure.attach(name="ssid info", body=str(setup_params_general1["ssid_modes"]["wpa2_personal"]))
        for i in range(len(setup_params_general1["ssid_modes"]["wpa2_personal"])):
            profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][i]
            ssid_name = profile_data["ssid_name"]
            if str(profile_data["appliedRadios"][0]) == "2G":
                passes1 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_2g_radios[0],
                                                                      station_name=sta_list1)
                pass_fail.append(passes1)
            elif str(profile_data["appliedRadios"][0]) == "5G":
                passes2 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_5g_radios[0],
                                                                      station_name=sta_list2)
                pass_fail.append(passes2)

        for sta in stations_list:
            result = get_test_library.json_get(_req_url="port/1/1/%s" % sta)
            get_test_library.allure_report_table_format(dict_data=result["interface"], key="Station Data",
                                                        value="Value", name="%s info" % sta)
        if False in pass_fail:
            assert False, "Test Failed, Station's didn't get IP address"

        # create Layer 3 and check data path
        for i in range(len(stations_list)):
            for j in range(i + 1, len(stations_list)):
                get_test_library.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_tcp", sta_list=[stations_list[i]],
                                               side_b=stations_list[j], start_cx=True,
                                               prefix="cx-{}{}-".format(i, j))
                time.sleep(5)
                logging.info(
                    "cx created between endpint a {} and endpoint b {}".format(stations_list[i], stations_list[j]))

        # start layer3
        logging.info("Run Layer 3 traffic for 30 sec ...")
        time.sleep(30)
        cx_list = get_test_library.get_cx_list()
        for i in range(len(cx_list)):
            cx_data = get_test_library.json_get(_req_url=f"cx/{cx_list[i]}")
            get_test_library.allure_report_table_format(dict_data=cx_data[f"{cx_list[i]}"], key="L3 CX Column",
                                                        value="L3 CX values", name=f"cx {cx_list[i]} info")
            l3_data.update({f"{cx_list[i]}": cx_data[f"{cx_list[i]}"]})
            if cx_data[cx_list[i]]['bps rx a'] != 0 and cx_data[cx_list[i]]['bps rx a'] != 0:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     f"{cx_data[cx_list[i]]['bps rx a']}",
                     f"{cx_data[cx_list[i]]['bps rx b']}", True])
            else:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     cx_data[cx_list[i]]['bps rx a'],
                     f"{cx_data[cx_list[i]]['bps rx b']}", False])

        print("L3 Data \n", l3_data)
        print("Pass Fail Data: \n", pass_fail_data)

        # attach pass fail data to allure
        result_table = tabulate.tabulate(pass_fail_data,
                                         headers=["Data Path", "Tx Rate (bps)", "Rx Rate (bps)", "Pass/Fail"],
                                         tablefmt='fancy_grid')
        allure.attach(name="Test Result Table", body=str(result_table))
        # cleanup Layer3 data
        get_test_library.client_disconnect(station_name=stations_list, clean_l3_traffic=True, clear_all_sta=True)
        test_result = True
        for pf in pass_fail_data:
            if pf[3] is False:
                test_result = False

        if test_result:
            assert True
        else:
            assert False, "DataPath check failed, Traffic didn't reported on some endpoints"


setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi SSID Test")
@allure.parent_suite("MULTI SSID")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="Test Data Path for 2 SSID's")
class TestMultiSsidDataPath2(object):
    """
        Multiple number of SSIDs Test: Bridge Mode
        pytest -m multi_ssid and two_ssid
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12228")
    @pytest.mark.wpa2_personal
    @pytest.mark.two_ssid
    @pytest.mark.fiveg
    def test_two_ssids(self, get_test_library, get_dut_logs_per_test_case,
                       get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multi-SSID Bridge Mode
            pytest -m "multi_ssid and two_ssid"
        """
        mode = "BRIDGE"
        security_key = "something"
        security = "wpa2"
        sta_list1 = ["sta0001", "sta0002"]
        sta_list2 = ["sta0003", "sta0004"]
        stations_list = sta_list1 + sta_list2
        pass_fail, l3_data = [], {}
        pass_fail_data = []
        allure.attach(name="ssid info", body=str(setup_params_general2["ssid_modes"]["wpa2_personal"]))
        for i in range(len(setup_params_general2["ssid_modes"]["wpa2_personal"])):
            profile_data = setup_params_general2["ssid_modes"]["wpa2_personal"][i]
            ssid_name = profile_data["ssid_name"]
            if str(profile_data["appliedRadios"][0]) == "2G":
                passes1 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_2g_radios[0],
                                                                      station_name=sta_list1)
                pass_fail.append(passes1)
            elif str(profile_data["appliedRadios"][0]) == "5G":
                passes2 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_5g_radios[0],
                                                                      station_name=sta_list2)
                pass_fail.append(passes2)

        for sta in stations_list:
            result = get_test_library.json_get(_req_url="port/1/1/%s" % sta)
            get_test_library.allure_report_table_format(dict_data=result["interface"], key="Station Data",
                                                        value="Value", name="%s info" % sta)
        if False in pass_fail:
            assert False, "Test Failed, Station's didn't get IP address"

        # create Layer 3 and check data path
        for i in range(len(stations_list)):
            for j in range(i + 1, len(stations_list)):
                get_test_library.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_tcp", sta_list=[stations_list[i]],
                                               side_b=stations_list[j], start_cx=True,
                                               prefix="cx-{}{}-".format(i, j))
                time.sleep(5)
                logging.info(
                    "cx created between endpint a {} and endpoint b {}".format(stations_list[i], stations_list[j]))

        # start layer3
        logging.info("Run Layer 3 traffic for 30 sec ...")
        time.sleep(30)
        cx_list = get_test_library.get_cx_list()
        for i in range(len(cx_list)):
            cx_data = get_test_library.json_get(_req_url=f"cx/{cx_list[i]}")
            get_test_library.allure_report_table_format(dict_data=cx_data[f"{cx_list[i]}"], key="L3 CX Column",
                                                        value="L3 CX values", name=f"cx {cx_list[i]} info")
            l3_data.update({f"{cx_list[i]}": cx_data[f"{cx_list[i]}"]})
            if cx_data[cx_list[i]]['bps rx a'] != 0 and cx_data[cx_list[i]]['bps rx a'] != 0:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     f"{cx_data[cx_list[i]]['bps rx a']}",
                     f"{cx_data[cx_list[i]]['bps rx b']}", True])
            else:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     cx_data[cx_list[i]]['bps rx a'],
                     f"{cx_data[cx_list[i]]['bps rx b']}", False])

        print("L3 Data \n", l3_data)
        print("Pass Fail Data: \n", pass_fail_data)

        # attach pass fail data to allure
        result_table = tabulate.tabulate(pass_fail_data,
                                         headers=["Data Path", "Tx Rate (bps)", "Rx Rate (bps)", "Pass/Fail"],
                                         tablefmt='fancy_grid')
        allure.attach(name="Test Result Table", body=str(result_table))
        # cleanup Layer3 data
        get_test_library.client_disconnect(station_name=stations_list, clean_l3_traffic=True, clear_all_sta=True)
        test_result = True
        for pf in pass_fail_data:
            if pf[3] is False:
                test_result = False

        if test_result:
            assert True
        else:
            assert False, "DataPath check failed, Traffic didn't reported on some endpoints"


setup_params_general3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general3],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi SSID Test")
@allure.parent_suite("MULTI SSID")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="Test Data Path for 3 SSID's")
class TestMultiSsidDataPath3(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.three_ssid
    def test_three_ssids(self, get_test_library, get_dut_logs_per_test_case,
                         get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multi-SSID Bridge Mode
            pytest -m "multi_ssid and three_ssid"
        """
        mode = "BRIDGE"
        security_key = "something"
        security = "wpa2"
        sta_list1 = ["sta0001", "sta0002"]
        sta_list2 = ["sta0003", "sta0004"]
        stations_list = sta_list1 + sta_list2
        pass_fail, l3_data = [], {}
        pass_fail_data = []
        allure.attach(name="ssid info", body=str(setup_params_general3["ssid_modes"]["wpa2_personal"]))
        for i in range(len(setup_params_general3["ssid_modes"]["wpa2_personal"])):
            profile_data = setup_params_general3["ssid_modes"]["wpa2_personal"][i]
            ssid_name = profile_data["ssid_name"]
            if str(profile_data["appliedRadios"][0]) == "2G":
                passes1 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_2g_radios[0],
                                                                      station_name=sta_list1)
                pass_fail.append(passes1)
            elif str(profile_data["appliedRadios"][0]) == "5G":
                passes2 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_5g_radios[0],
                                                                      station_name=sta_list2)
                pass_fail.append(passes2)

        for sta in stations_list:
            result = get_test_library.json_get(_req_url="port/1/1/%s" % sta)
            get_test_library.allure_report_table_format(dict_data=result["interface"], key="Station Data",
                                                        value="Value", name="%s info" % sta)
        if False in pass_fail:
            assert False, "Test Failed, Station's didn't get IP address"

        # create Layer 3 and check data path
        for i in range(len(stations_list)):
            for j in range(i + 1, len(stations_list)):
                get_test_library.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_tcp", sta_list=[stations_list[i]],
                                               side_b=stations_list[j], start_cx=True,
                                               prefix="cx-{}{}-".format(i, j))
                time.sleep(5)
                logging.info(
                    "cx created between endpint a {} and endpoint b {}".format(stations_list[i], stations_list[j]))

        # start layer3
        logging.info("Run Layer 3 traffic for 30 sec ...")
        time.sleep(30)
        cx_list = get_test_library.get_cx_list()
        for i in range(len(cx_list)):
            cx_data = get_test_library.json_get(_req_url=f"cx/{cx_list[i]}")
            get_test_library.allure_report_table_format(dict_data=cx_data[f"{cx_list[i]}"], key="L3 CX Column",
                                                        value="L3 CX values", name=f"cx {cx_list[i]} info")
            l3_data.update({f"{cx_list[i]}": cx_data[f"{cx_list[i]}"]})
            if cx_data[cx_list[i]]['bps rx a'] != 0 and cx_data[cx_list[i]]['bps rx a'] != 0:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     f"{cx_data[cx_list[i]]['bps rx a']}",
                     f"{cx_data[cx_list[i]]['bps rx b']}", True])
            else:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     cx_data[cx_list[i]]['bps rx a'],
                     f"{cx_data[cx_list[i]]['bps rx b']}", False])

        print("L3 Data \n", l3_data)
        print("Pass Fail Data: \n", pass_fail_data)

        # attach pass fail data to allure
        result_table = tabulate.tabulate(pass_fail_data,
                                         headers=["Data Path", "Tx Rate (bps)", "Rx Rate (bps)", "Pass/Fail"],
                                         tablefmt='fancy_grid')
        allure.attach(name="Test Result Table", body=str(result_table))
        # cleanup Layer3 data
        get_test_library.client_disconnect(station_name=stations_list, clean_l3_traffic=True, clear_all_sta=True)
        test_result = True
        for pf in pass_fail_data:
            if pf[3] is False:
                test_result = False

        if test_result:
            assert True
        else:
            assert False, "DataPath check failed, Traffic didn't reported on some endpoints"


setup_params_general4 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general4],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi SSID Test")
@allure.parent_suite("MULTI SSID")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="Test Data Path for 4 SSID's")
class TestMultiSsidDataPath4(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.four_ssid
    def test_four_ssids(self, get_test_library, get_dut_logs_per_test_case,
                        get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multi-SSID Bridge Mode
            pytest -m "multi_ssid and four_ssid"
        """
        mode = "BRIDGE"
        security_key = "something"
        security = "wpa2"
        sta_list1 = ["sta0001", "sta0002"]
        sta_list2 = ["sta0003", "sta0004"]
        stations_list = sta_list1 + sta_list2
        pass_fail, l3_data = [], {}
        pass_fail_data = []
        allure.attach(name="ssid info", body=str(setup_params_general4["ssid_modes"]["wpa2_personal"]))
        for i in range(len(setup_params_general4["ssid_modes"]["wpa2_personal"])):
            profile_data = setup_params_general4["ssid_modes"]["wpa2_personal"][i]
            ssid_name = profile_data["ssid_name"]
            if str(profile_data["appliedRadios"][0]) == "2G":
                passes1 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_2g_radios[0],
                                                                      station_name=sta_list1)
                pass_fail.append(passes1)
            elif str(profile_data["appliedRadios"][0]) == "5G":
                passes2 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_5g_radios[0],
                                                                      station_name=sta_list2)
                pass_fail.append(passes2)

        for sta in stations_list:
            result = get_test_library.json_get(_req_url="port/1/1/%s" % sta)
            get_test_library.allure_report_table_format(dict_data=result["interface"], key="Station Data",
                                                        value="Value", name="%s info" % sta)
        if False in pass_fail:
            assert False, "Test Failed, Station's didn't get IP address"

        # create Layer 3 and check data path
        for i in range(len(stations_list)):
            for j in range(i + 1, len(stations_list)):
                get_test_library.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_tcp", sta_list=[stations_list[i]],
                                               side_b=stations_list[j], start_cx=True,
                                               prefix="cx-{}{}-".format(i, j))
                time.sleep(5)
                logging.info(
                    "cx created between endpint a {} and endpoint b {}".format(stations_list[i], stations_list[j]))

        # start layer3
        logging.info("Run Layer 3 traffic for 30 sec ...")
        time.sleep(30)
        cx_list = get_test_library.get_cx_list()
        for i in range(len(cx_list)):
            cx_data = get_test_library.json_get(_req_url=f"cx/{cx_list[i]}")
            get_test_library.allure_report_table_format(dict_data=cx_data[f"{cx_list[i]}"], key="L3 CX Column",
                                                        value="L3 CX values", name=f"cx {cx_list[i]} info")
            l3_data.update({f"{cx_list[i]}": cx_data[f"{cx_list[i]}"]})
            if cx_data[cx_list[i]]['bps rx a'] != 0 and cx_data[cx_list[i]]['bps rx a'] != 0:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     f"{cx_data[cx_list[i]]['bps rx a']}",
                     f"{cx_data[cx_list[i]]['bps rx b']}", True])
            else:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     cx_data[cx_list[i]]['bps rx a'],
                     f"{cx_data[cx_list[i]]['bps rx b']}", False])

        print("L3 Data \n", l3_data)
        print("Pass Fail Data: \n", pass_fail_data)

        # attach pass fail data to allure
        result_table = tabulate.tabulate(pass_fail_data,
                                         headers=["Data Path", "Tx Rate (bps)", "Rx Rate (bps)", "Pass/Fail"],
                                         tablefmt='fancy_grid')
        allure.attach(name="Test Result Table", body=str(result_table))
        # cleanup Layer3 data
        get_test_library.client_disconnect(station_name=stations_list, clean_l3_traffic=True, clear_all_sta=True)
        test_result = True
        for pf in pass_fail_data:
            if pf[3] is False:
                test_result = False

        if test_result:
            assert True
        else:
            assert False, "DataPath check failed, Traffic didn't reported on some endpoints"


setup_params_general5 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi SSID Test")
@allure.parent_suite("MULTI SSID")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="Test Data Path for 5 SSID's")
class TestMultiSsidDataPath5(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.five_ssid
    def test_five_ssids(self, get_test_library, get_dut_logs_per_test_case,
                        get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multi-SSID Bridge Mode
            pytest -m "multi_ssid and five_ssid"
        """
        mode = "BRIDGE"
        security_key = "something"
        security = "wpa2"
        sta_list1 = ["sta0001", "sta0002"]
        sta_list2 = ["sta0003", "sta0004"]
        stations_list = sta_list1 + sta_list2
        pass_fail, l3_data = [], {}
        pass_fail_data = []
        allure.attach(name="ssid info", body=str(setup_params_general5["ssid_modes"]["wpa2_personal"]))
        for i in range(len(setup_params_general5["ssid_modes"]["wpa2_personal"])):
            profile_data = setup_params_general5["ssid_modes"]["wpa2_personal"][i]
            ssid_name = profile_data["ssid_name"]
            if str(profile_data["appliedRadios"][0]) == "2G":
                passes1 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_2g_radios[0],
                                                                      station_name=sta_list1)
                pass_fail.append(passes1)
            elif str(profile_data["appliedRadios"][0]) == "5G":
                passes2 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_5g_radios[0],
                                                                      station_name=sta_list2)
                pass_fail.append(passes2)

        for sta in stations_list:
            result = get_test_library.json_get(_req_url="port/1/1/%s" % sta)
            get_test_library.allure_report_table_format(dict_data=result["interface"], key="Station Data",
                                                        value="Value", name="%s info" % sta)
        if False in pass_fail:
            assert False, "Test Failed, Station's didn't get IP address"

        # create Layer 3 and check data path
        for i in range(len(stations_list)):
            for j in range(i + 1, len(stations_list)):
                get_test_library.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_tcp", sta_list=[stations_list[i]],
                                               side_b=stations_list[j], start_cx=True,
                                               prefix="cx-{}{}-".format(i, j))
                time.sleep(5)
                logging.info(
                    "cx created between endpint a {} and endpoint b {}".format(stations_list[i], stations_list[j]))

        # start layer3
        logging.info("Run Layer 3 traffic for 30 sec ...")
        time.sleep(30)
        cx_list = get_test_library.get_cx_list()
        for i in range(len(cx_list)):
            cx_data = get_test_library.json_get(_req_url=f"cx/{cx_list[i]}")
            get_test_library.allure_report_table_format(dict_data=cx_data[f"{cx_list[i]}"], key="L3 CX Column",
                                                        value="L3 CX values", name=f"cx {cx_list[i]} info")
            l3_data.update({f"{cx_list[i]}": cx_data[f"{cx_list[i]}"]})
            if cx_data[cx_list[i]]['bps rx a'] != 0 and cx_data[cx_list[i]]['bps rx a'] != 0:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     f"{cx_data[cx_list[i]]['bps rx a']}",
                     f"{cx_data[cx_list[i]]['bps rx b']}", True])
            else:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     cx_data[cx_list[i]]['bps rx a'],
                     f"{cx_data[cx_list[i]]['bps rx b']}", False])

        print("L3 Data \n", l3_data)
        print("Pass Fail Data: \n", pass_fail_data)

        # attach pass fail data to allure
        result_table = tabulate.tabulate(pass_fail_data,
                                         headers=["Data Path", "Tx Rate (bps)", "Rx Rate (bps)", "Pass/Fail"],
                                         tablefmt='fancy_grid')
        allure.attach(name="Test Result Table", body=str(result_table))
        # cleanup Layer3 data
        get_test_library.client_disconnect(station_name=stations_list, clean_l3_traffic=True, clear_all_sta=True)
        test_result = True
        for pf in pass_fail_data:
            if pf[3] is False:
                test_result = False

        if test_result:
            assert True
        else:
            assert False, "DataPath check failed, Traffic didn't reported on some endpoints"


setup_params_general6 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general6],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi SSID Test")
@allure.parent_suite("MULTI SSID")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="Test Data Path for 6 SSID's")
class TestMultiSsidDataPath6(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.six_ssid
    def test_six_ssids(self, get_test_library, get_dut_logs_per_test_case,
                       get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multi-SSID Bridge Mode
            pytest -m "multi_ssid and six_ssid"
        """
        mode = "BRIDGE"
        security_key = "something"
        security = "wpa2"
        sta_list1 = ["sta0001", "sta0002"]
        sta_list2 = ["sta0003", "sta0004"]
        stations_list = sta_list1 + sta_list2
        pass_fail, l3_data = [], {}
        pass_fail_data = []
        allure.attach(name="ssid info", body=str(setup_params_general6["ssid_modes"]["wpa2_personal"]))
        for i in range(len(setup_params_general6["ssid_modes"]["wpa2_personal"])):
            profile_data = setup_params_general6["ssid_modes"]["wpa2_personal"][i]
            ssid_name = profile_data["ssid_name"]
            if str(profile_data["appliedRadios"][0]) == "2G":
                passes1 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_2g_radios[0],
                                                                      station_name=sta_list1)
                pass_fail.append(passes1)
            elif str(profile_data["appliedRadios"][0]) == "5G":
                passes2 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_5g_radios[0],
                                                                      station_name=sta_list2)
                pass_fail.append(passes2)

        for sta in stations_list:
            result = get_test_library.json_get(_req_url="port/1/1/%s" % sta)
            get_test_library.allure_report_table_format(dict_data=result["interface"], key="Station Data",
                                                        value="Value", name="%s info" % sta)
        if False in pass_fail:
            assert False, "Test Failed, Station's didn't get IP address"

        # create Layer 3 and check data path
        for i in range(len(stations_list)):
            for j in range(i + 1, len(stations_list)):
                get_test_library.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_tcp", sta_list=[stations_list[i]],
                                               side_b=stations_list[j], start_cx=True,
                                               prefix="cx-{}{}-".format(i, j))
                time.sleep(5)
                logging.info(
                    "cx created between endpint a {} and endpoint b {}".format(stations_list[i], stations_list[j]))

        # start layer3
        logging.info("Run Layer 3 traffic for 30 sec ...")
        time.sleep(30)
        cx_list = get_test_library.get_cx_list()
        for i in range(len(cx_list)):
            cx_data = get_test_library.json_get(_req_url=f"cx/{cx_list[i]}")
            get_test_library.allure_report_table_format(dict_data=cx_data[f"{cx_list[i]}"], key="L3 CX Column",
                                                        value="L3 CX values", name=f"cx {cx_list[i]} info")
            l3_data.update({f"{cx_list[i]}": cx_data[f"{cx_list[i]}"]})
            if cx_data[cx_list[i]]['bps rx a'] != 0 and cx_data[cx_list[i]]['bps rx a'] != 0:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     f"{cx_data[cx_list[i]]['bps rx a']}",
                     f"{cx_data[cx_list[i]]['bps rx b']}", True])
            else:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     cx_data[cx_list[i]]['bps rx a'],
                     f"{cx_data[cx_list[i]]['bps rx b']}", False])

        print("L3 Data \n", l3_data)
        print("Pass Fail Data: \n", pass_fail_data)

        # attach pass fail data to allure
        result_table = tabulate.tabulate(pass_fail_data,
                                         headers=["Data Path", "Tx Rate (bps)", "Rx Rate (bps)", "Pass/Fail"],
                                         tablefmt='fancy_grid')
        allure.attach(name="Test Result Table", body=str(result_table))
        # cleanup Layer3 data
        get_test_library.client_disconnect(station_name=stations_list, clean_l3_traffic=True, clear_all_sta=True)
        test_result = True
        for pf in pass_fail_data:
            if pf[3] is False:
                test_result = False

        if test_result:
            assert True
        else:
            assert False, "DataPath check failed, Traffic didn't reported on some endpoints"


setup_params_general7 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid4_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general7],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi SSID Test")
@allure.parent_suite("MULTI SSID")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="Test Data Path for 7 SSID's")
class TestMultiSsidDataPath7(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.seven_ssid
    def test_seven_ssids(self, get_test_library, get_dut_logs_per_test_case,
                         get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multi-SSID Bridge Mode
            pytest -m "multi_ssid and seven_ssid"
        """
        mode = "BRIDGE"
        security_key = "something"
        security = "wpa2"
        sta_list1 = ["sta0001", "sta0002"]
        sta_list2 = ["sta0003", "sta0004"]
        stations_list = sta_list1 + sta_list2
        pass_fail, l3_data = [], {}
        pass_fail_data = []
        allure.attach(name="ssid info", body=str(setup_params_general7["ssid_modes"]["wpa2_personal"]))
        for i in range(len(setup_params_general7["ssid_modes"]["wpa2_personal"])):
            profile_data = setup_params_general7["ssid_modes"]["wpa2_personal"][i]
            ssid_name = profile_data["ssid_name"]
            if str(profile_data["appliedRadios"][0]) == "2G":
                passes1 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_2g_radios[0],
                                                                      station_name=sta_list1)
                pass_fail.append(passes1)
            elif str(profile_data["appliedRadios"][0]) == "5G":
                passes2 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_5g_radios[0],
                                                                      station_name=sta_list2)
                pass_fail.append(passes2)

        for sta in stations_list:
            result = get_test_library.json_get(_req_url="port/1/1/%s" % sta)
            get_test_library.allure_report_table_format(dict_data=result["interface"], key="Station Data",
                                                        value="Value", name="%s info" % sta)
        if False in pass_fail:
            assert False, "Test Failed, Station's didn't get IP address"

        # create Layer 3 and check data path
        for i in range(len(stations_list)):
            for j in range(i + 1, len(stations_list)):
                get_test_library.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_tcp", sta_list=[stations_list[i]],
                                               side_b=stations_list[j], start_cx=True,
                                               prefix="cx-{}{}-".format(i, j))
                time.sleep(5)
                logging.info(
                    "cx created between endpint a {} and endpoint b {}".format(stations_list[i], stations_list[j]))

        # start layer3
        logging.info("Run Layer 3 traffic for 30 sec ...")
        time.sleep(30)
        cx_list = get_test_library.get_cx_list()
        for i in range(len(cx_list)):
            cx_data = get_test_library.json_get(_req_url=f"cx/{cx_list[i]}")
            get_test_library.allure_report_table_format(dict_data=cx_data[f"{cx_list[i]}"], key="L3 CX Column",
                                                        value="L3 CX values", name=f"cx {cx_list[i]} info")
            l3_data.update({f"{cx_list[i]}": cx_data[f"{cx_list[i]}"]})
            if cx_data[cx_list[i]]['bps rx a'] != 0 and cx_data[cx_list[i]]['bps rx a'] != 0:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     f"{cx_data[cx_list[i]]['bps rx a']}",
                     f"{cx_data[cx_list[i]]['bps rx b']}", True])
            else:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     cx_data[cx_list[i]]['bps rx a'],
                     f"{cx_data[cx_list[i]]['bps rx b']}", False])

        print("L3 Data \n", l3_data)
        print("Pass Fail Data: \n", pass_fail_data)

        # attach pass fail data to allure
        result_table = tabulate.tabulate(pass_fail_data,
                                         headers=["Data Path", "Tx Rate (bps)", "Rx Rate (bps)", "Pass/Fail"],
                                         tablefmt='fancy_grid')
        allure.attach(name="Test Result Table", body=str(result_table))
        # cleanup Layer3 data
        get_test_library.client_disconnect(station_name=stations_list, clean_l3_traffic=True, clear_all_sta=True)
        test_result = True
        for pf in pass_fail_data:
            if pf[3] is False:
                test_result = False

        if test_result:
            assert True
        else:
            assert False, "DataPath check failed, Traffic didn't reported on some endpoints"


setup_params_general8 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid4_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "multi_ssid4_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general8],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
@allure.feature("Multi SSID Test")
@allure.parent_suite("MULTI SSID")
@allure.suite(suite_name="BRIDGE MODE")
@allure.sub_suite(sub_suite_name="Test Data Path for 8 SSID's")
class TestMultiSsidDataPath8(object):
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.eight_ssid
    def test_eight_ssids(self, get_test_library, get_dut_logs_per_test_case,
                         get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multi-SSID Bridge Mode
            pytest -m "multi_ssid and eight_ssid"
        """
        mode = "BRIDGE"
        security_key = "something"
        security = "wpa2"
        sta_list1 = ["sta0001", "sta0002"]
        sta_list2 = ["sta0003", "sta0004"]
        stations_list = sta_list1 + sta_list2
        pass_fail, l3_data = [], {}
        pass_fail_data = []
        allure.attach(name="ssid info", body=str(setup_params_general8["ssid_modes"]["wpa2_personal"]))
        for i in range(len(setup_params_general8["ssid_modes"]["wpa2_personal"])):
            profile_data = setup_params_general8["ssid_modes"]["wpa2_personal"][i]
            ssid_name = profile_data["ssid_name"]
            if str(profile_data["appliedRadios"][0]) == "2G":
                passes1 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_2g_radios[0],
                                                                      station_name=sta_list1)
                pass_fail.append(passes1)
            elif str(profile_data["appliedRadios"][0]) == "5G":
                passes2 = get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                      passkey=security_key,
                                                                      mode=mode,
                                                                      radio=get_test_library.wave2_5g_radios[0],
                                                                      station_name=sta_list2)
                pass_fail.append(passes2)

        for sta in stations_list:
            result = get_test_library.json_get(_req_url="port/1/1/%s" % sta)
            get_test_library.allure_report_table_format(dict_data=result["interface"], key="Station Data",
                                                        value="Value", name="%s info" % sta)
        if False in pass_fail:
            assert False, "Test Failed, Station's didn't get IP address"

        # create Layer 3 and check data path
        for i in range(len(stations_list)):
            for j in range(i + 1, len(stations_list)):
                get_test_library.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                               side_b_min_rate=6291456, side_b_max_rate=0,
                                               traffic_type="lf_tcp", sta_list=[stations_list[i]],
                                               side_b=stations_list[j], start_cx=True,
                                               prefix="cx-{}{}-".format(i, j))
                time.sleep(5)
                logging.info(
                    "cx created between endpint a {} and endpoint b {}".format(stations_list[i], stations_list[j]))

        # start layer3
        logging.info("Run Layer 3 traffic for 30 sec ...")
        time.sleep(30)
        cx_list = get_test_library.get_cx_list()
        for i in range(len(cx_list)):
            cx_data = get_test_library.json_get(_req_url=f"cx/{cx_list[i]}")
            get_test_library.allure_report_table_format(dict_data=cx_data[f"{cx_list[i]}"], key="L3 CX Column",
                                                        value="L3 CX values", name=f"cx {cx_list[i]} info")
            l3_data.update({f"{cx_list[i]}": cx_data[f"{cx_list[i]}"]})
            if cx_data[cx_list[i]]['bps rx a'] != 0 and cx_data[cx_list[i]]['bps rx a'] != 0:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     f"{cx_data[cx_list[i]]['bps rx a']}",
                     f"{cx_data[cx_list[i]]['bps rx b']}", True])
            else:
                pass_fail_data.append(
                    ["{}<->{}".format(cx_data[cx_list[i]]['endpoints'][0], cx_data[cx_list[i]]['endpoints'][1]),
                     cx_data[cx_list[i]]['bps rx a'],
                     f"{cx_data[cx_list[i]]['bps rx b']}", False])

        print("L3 Data \n", l3_data)
        print("Pass Fail Data: \n", pass_fail_data)

        # attach pass fail data to allure
        result_table = tabulate.tabulate(pass_fail_data,
                                         headers=["Data Path", "Tx Rate (bps)", "Rx Rate (bps)", "Pass/Fail"],
                                         tablefmt='fancy_grid')
        allure.attach(name="Test Result Table", body=str(result_table))
        # cleanup Layer3 data
        get_test_library.client_disconnect(station_name=stations_list, clean_l3_traffic=True, clear_all_sta=True)
        test_result = True
        for pf in pass_fail_data:
            if pf[3] is False:
                test_result = False

        if test_result:
            assert True
        else:
            assert False, "DataPath check failed, Traffic didn't reported on some endpoints"
