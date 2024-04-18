"""
    Multiple number of SSIDs Test: Bridge Mode
    pytest -m multi_ssid
"""
import logging
import time
import allure
import pytest
import tabulate

pytestmark = [pytest.mark.multi_ssid, pytest.mark.bridge, pytest.mark.twog, pytest.mark.fiveg]


def get_radio_availabilities(num_stations_2g, num_stations_5g, test_lib):
    """
        Get how many 2G/5G stations to be created on which radios.

        Note: Same radio can not be used to create 2G and 5G stations at the same time.
    """

    message = None
    requested_num_stations_2g = num_stations_2g
    requested_num_stations_5g = num_stations_5g

    radio_dict_2g = {}
    radio_dict_5g = {}
    dict_all_radios_2g = {
        "wave2_2g_radios": test_lib.wave2_2g_radios,
        "wave1_radios": test_lib.wave1_radios,
        "mtk_radios": test_lib.mtk_radios,
        "ax200_radios": test_lib.ax200_radios,
        "ax210_radios": test_lib.ax210_radios
    }
    dict_all_radios_5g = {
        "wave2_5g_radios": test_lib.wave2_5g_radios,
        "wave1_radios": test_lib.wave1_radios,
        "mtk_radios": test_lib.mtk_radios,
        "ax200_radios": test_lib.ax200_radios,
        "ax210_radios": test_lib.ax210_radios
    }
    max_station_per_radio = {
        "wave2_2g_radios": 64,
        "wave2_5g_radios": 64,
        "wave1_radios": 64,
        "mtk_radios": 19,
        "ax200_radios": 1,
        "ax210_radios": 1
    }

    for i in range(2):
        if num_stations_2g > num_stations_5g:
            for keys in dict_all_radios_2g:
                if num_stations_2g == 0:
                    break
                max_station = max_station_per_radio[keys]
                if len(dict_all_radios_2g[keys]) > 0:
                    diff = max_station - num_stations_2g
                    for port_name in dict_all_radios_2g[keys]:
                        if port_name in radio_dict_5g:
                            continue
                        if diff >= 0:
                            radio_dict_2g[port_name] = num_stations_2g
                            num_stations_2g = 0
                            break
                        else:
                            radio_dict_2g[port_name] = max_station
                            num_stations_2g -= max_station
                            diff = max_station - num_stations_2g
            if num_stations_2g != 0:
                if i == 0:
                    message = f"Not enough radios available for connecting {requested_num_stations_2g} 2g clients!"
                break
        else:
            for keys in dict_all_radios_5g:
                if num_stations_5g == 0:
                    break
                max_station = max_station_per_radio[keys]
                if len(dict_all_radios_5g[keys]) > 0:
                    diff = max_station - num_stations_5g
                    for port_name in dict_all_radios_5g[keys]:
                        if port_name in radio_dict_2g:
                            continue
                        if diff >= 0:
                            radio_dict_5g[port_name] = num_stations_5g
                            num_stations_5g = 0
                            break
                        else:
                            radio_dict_5g[port_name] = max_station
                            num_stations_5g -= max_station
                            diff = max_station - num_stations_5g
            if num_stations_5g != 0:
                if i == 0:
                    message = f"Not enough radios available for connecting {requested_num_stations_5g} 5g clients!"
                break


    if num_stations_2g != 0 or num_stations_5g != 0:
        logging.info(f"Radio-2G-Stations dict : {num_stations_2g}")
        logging.info(f"Radio-5G-Stations dict : {num_stations_5g}")
        if message is None:
            message = (f"Not enough radios available for connecting {requested_num_stations_2g} 2g clients and "
                       f"{requested_num_stations_5g} 5g clients simultaneously!")
        logging.info(message)
        pytest.skip(message)

    return radio_dict_2g, radio_dict_5g


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
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for 1 SSID")
class TestMultiSsidDataPath1(object):
    """
        Multiple number of SSIDs Test: Bridge Mode

        Unique Marker:
        multi_ssid and bridge and one_ssid
    """

    @allure.title("1-SSID")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12227")
    @pytest.mark.wpa2_personal
    @pytest.mark.one_ssid
    def test_one_ssid(self, get_test_library, get_dut_logs_per_test_case, get_test_device_logs, setup_configuration,
                      check_connectivity):
        """
            Multi-SSID Bridge Mode

            Unique Marker:
            multi_ssid and bridge and one_ssid
        """
        mode = "BRIDGE"
        security_key = "something"
        security = "wpa2"
        stations_list = ["sta_2g_1", "sta_2g_2", "sta_5g_1", "sta_5g_2"]
        sta_names_2g = {stations_list[0], stations_list[1]}
        sta_names_5g = {stations_list[2], stations_list[3]}

        radio_dict_2g, radio_dict_5g = get_radio_availabilities(num_stations_2g=len(sta_names_2g),
                                                                num_stations_5g=len(sta_names_5g),
                                                                test_lib=get_test_library)
        logging.info(f"Radio-2G-Stations dict : {radio_dict_2g}")
        logging.info(f"Radio-5G-Stations dict : {radio_dict_5g}")

        sta_got_ip = []
        allure.attach(name="ssid info", body=str(setup_params_general1["ssid_modes"]["wpa2_personal"]))

        get_test_library.pre_cleanup()

        for i in range(len(setup_params_general1["ssid_modes"]["wpa2_personal"])):
            profile_data = setup_params_general1["ssid_modes"]["wpa2_personal"][i]
            ssid_name = profile_data["ssid_name"]
            if str(profile_data["appliedRadios"][0]) == "2G":
                while len(sta_names_2g) > 0:
                    radio = num_stations = None
                    for _radio in radio_dict_2g:
                        radio = _radio
                        num_stations = radio_dict_2g[_radio]
                        del radio_dict_2g[_radio]
                        break
                    station_name_list = []
                    for _ in range(num_stations):
                        station_name_list.append(sta_names_2g.pop())
                    sta_got_ip.append(get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                                  passkey=security_key, mode=mode,
                                                                                  radio=radio,
                                                                                  station_name=station_name_list,
                                                                                  attach_station_data=False))
            elif str(profile_data["appliedRadios"][0]) == "5G":
                while len(sta_names_5g) > 0:
                    radio = num_stations = None
                    for _radio in radio_dict_5g:
                        radio = _radio
                        num_stations = radio_dict_5g[_radio]
                        del radio_dict_5g[_radio]
                        break
                    station_name_list = []
                    for _ in range(num_stations):
                        station_name_list.append(sta_names_5g.pop())
                    sta_got_ip.append(get_test_library.client_connect_using_radio(ssid=ssid_name, security=security,
                                                                                  passkey=security_key, mode=mode,
                                                                                  radio=radio,
                                                                                  station_name=station_name_list,
                                                                                  attach_station_data=False,
                                                                                  attach_port_info=False))

        port_data = get_test_library.json_get(_req_url="port?fields=ip")
        port_info = {key: value for d in port_data["interfaces"] for key, value in d.items()}
        get_test_library.allure_report_table_format(dict_data=port_info, key="Port Names", value="ip",
                                                    name="Port info after creating all stations")

        dict_table_2g = {}
        dict_table_5g = {}
        for sta in stations_list:
            result = get_test_library.json_get(_req_url="port/1/1/%s" % sta)
            if "Key" not in dict_table_2g:
                dict_table_2g["Key"] = list(result["interface"].keys())
                dict_table_5g["Key"] = list(result["interface"].keys())
            if '_2g_' in sta:
                dict_table_2g[f"Value ({sta})"] = list(result["interface"].values())
            else:
                dict_table_5g[f"Value ({sta})"] = list(result["interface"].values())

        data_table_2g = tabulate.tabulate(dict_table_2g, headers='keys', tablefmt='fancy_grid')
        data_table_5g = tabulate.tabulate(dict_table_5g, headers='keys', tablefmt='fancy_grid')
        logging.info(f"2G Stations Data: \n{data_table_2g}\n")
        logging.info(f"5G Stations Data: \n{data_table_5g}\n")
        allure.attach(name="2G Stations Data", body=str(data_table_2g))
        allure.attach(name="5G Stations Data", body=str(data_table_5g))

        if False in sta_got_ip:
            logging.info("Some/All Stations didn't get IP address")
            pytest.fail("Some/All Stations didn't get IP address")

        # create Layer 3 and check data path
        for i in range(3):
            get_test_library.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                                           side_b_min_rate=6291456, side_b_max_rate=0,
                                           traffic_type="lf_tcp", sta_list=[stations_list[i]],
                                           side_b=stations_list[i + 1], start_cx=True,
                                           prefix="cx-{}{}-".format(i, i + 1))
            time.sleep(5)
            logging.info(f"CX created between endpoint-a= {stations_list[i]} and endpoint-b= {stations_list[i + 1]}")

        logging.info("Run Layer 3 traffic for 60 sec ...")
        time.sleep(60)

        cx_list = get_test_library.get_cx_list()
        dict_table_cx = {}
        pass_fail_data = []
        for i in range(len(cx_list)):
            cx_data = get_test_library.json_get(_req_url=f"cx/{cx_list[i]}")
            if "L3 CX Column" not in dict_table_cx:
                dict_table_cx["L3 CX Column"] = list(cx_data[f"{cx_list[i]}"].keys())
            dict_table_cx[f"L3 CX values ({cx_list[i]})"] = list(cx_data[f"{cx_list[i]}"].values())

            if cx_data[cx_list[i]]['bps rx a'] != 0 and cx_data[cx_list[i]]['bps rx a'] != 0:
                res = True
            else:
                res = False
            pass_fail_data.append(
                [f"{cx_data[cx_list[i]]['endpoints'][0]}<->{cx_data[cx_list[i]]['endpoints'][1]}",
                 f"{cx_data[cx_list[i]]['bps rx a']}",
                 f"{cx_data[cx_list[i]]['bps rx b']}", res])

        # attach l3 cx data to allure
        data_table_cx = tabulate.tabulate(dict_table_cx, headers='keys', tablefmt='fancy_grid')
        logging.info(f"L3 cross-connects Data: \n{data_table_cx}\n")
        allure.attach(name="L3 cross-connects Data", body=str(data_table_cx))

        # attach pass fail data to allure
        result_table = tabulate.tabulate(pass_fail_data,
                                         headers=["Data Path", "Tx Rate (bps)", "Rx Rate (bps)", "Pass/Fail"],
                                         tablefmt='fancy_grid')
        logging.info(f"Test Result Table: \n{result_table}\n")
        allure.attach(name="Test Result Table", body=str(result_table))

        # cleanup Layer3 data
        get_test_library.client_disconnect(station_name=stations_list, clean_l3_traffic=True, clear_all_sta=True)

        test_result = True
        for pf in pass_fail_data:
            if pf[3] is False:
                test_result = False

        if not test_result:
            pytest.fail("DataPath check failed, Traffic didn't reported on some endpoints")


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
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for 2 SSID's")
class TestMultiSsidDataPath2(object):
    """
        Multiple number of SSIDs Test: Bridge Mode
        pytest -m multi_ssid and two_ssid
    """

    @allure.title("2-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12228")
    @pytest.mark.wpa2_personal
    @pytest.mark.two_ssid
    def test_two_ssids(self, get_test_library, get_dut_logs_per_test_case,
                       get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multiple number of SSIDs Test: Bridge Mode

            Unique Marker:
            multi_ssid and bridge and two_ssid
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
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for 3 SSID's")
class TestMultiSsidDataPath3(object):

    @allure.title("3-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.three_ssid
    def test_three_ssids(self, get_test_library, get_dut_logs_per_test_case,
                         get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multiple number of SSIDs Test: Bridge Mode

            Unique Marker:
            multi_ssid and bridge and three_ssid
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
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for 4 SSID's")
class TestMultiSsidDataPath4(object):

    @allure.title("4-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.four_ssid
    def test_four_ssids(self, get_test_library, get_dut_logs_per_test_case,
                        get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multiple number of SSIDs Test: Bridge Mode

            Unique Marker:
            multi_ssid and bridge and four_ssid
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
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for 5 SSID's")
class TestMultiSsidDataPath5(object):

    @allure.title("5-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.five_ssid
    def test_five_ssids(self, get_test_library, get_dut_logs_per_test_case,
                        get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multiple number of SSIDs Test: Bridge Mode

            Unique Marker:
            multi_ssid and bridge and five_ssid
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
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for 6 SSID's")
class TestMultiSsidDataPath6(object):

    @allure.title("6-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.six_ssid
    def test_six_ssids(self, get_test_library, get_dut_logs_per_test_case,
                       get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multiple number of SSIDs Test: Bridge Mode

            Unique Marker:
            multi_ssid and bridge and six_ssid
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
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for 7 SSID's")
class TestMultiSsidDataPath7(object):

    @allure.title("7-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.seven_ssid
    def test_seven_ssids(self, get_test_library, get_dut_logs_per_test_case,
                         get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multiple number of SSIDs Test: Bridge Mode

            Unique Marker:
            multi_ssid and bridge and seven_ssid
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
@allure.feature("Multi-SSID")
@allure.parent_suite("Multi-SSID Tests")
@allure.suite(suite_name="Bridge")
@allure.sub_suite(sub_suite_name="Test Data Path for 8 SSID's")
class TestMultiSsidDataPath8(object):

    @allure.title("8-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-12227", name="WIFI-12229")
    @pytest.mark.wpa2_personal
    @pytest.mark.eight_ssid
    def test_eight_ssids(self, get_test_library, get_dut_logs_per_test_case,
                         get_test_device_logs, num_stations, setup_configuration, check_connectivity):
        """
            Multiple number of SSIDs Test: Bridge Mode

            Unique Marker:
            multi_ssid and bridge and eight_ssid
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
