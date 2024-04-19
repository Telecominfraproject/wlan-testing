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


def multi_ssid_test(test_lib, setup_params_general, no_of_2g_and_5g_stations=2):
    sta_names_2g, sta_names_5g = [], []
    for i in range(no_of_2g_and_5g_stations):
        sta_names_2g.append(f"sta_2g_{i + 1}")
        sta_names_5g.append(f"sta_5g_{i + 1}")

    mode = "BRIDGE"
    security_key = "something"
    security = "wpa2"
    cx_sta_list = [sta_names_2g[-2], sta_names_2g[-1], sta_names_5g[-2], sta_names_5g[-1]]

    radio_dict_2g, radio_dict_5g = get_radio_availabilities(num_stations_2g=len(sta_names_2g),
                                                            num_stations_5g=len(sta_names_5g),
                                                            test_lib=test_lib)
    logging.info(f"Radio-2G-Stations dict : {radio_dict_2g}")
    logging.info(f"Radio-5G-Stations dict : {radio_dict_5g}")

    sta_got_ip = []
    allure.attach(name="ssid info", body=str(setup_params_general["ssid_modes"]["wpa2_personal"]))

    test_lib.pre_cleanup()
    no_of_ssids = len(setup_params_general["ssid_modes"]["wpa2_personal"])
    logging.info(f"A total of {no_of_2g_and_5g_stations} 2G and {no_of_2g_and_5g_stations} 5G stations will be "
                 f"created for {no_of_ssids} SSIDs, i.e., a 2G and a 5G stations on each SSID.")

    for i in range(no_of_2g_and_5g_stations):
        ssid_name = setup_params_general["ssid_modes"]["wpa2_personal"][i % no_of_ssids]["ssid_name"]
        logging.info(f"Creating a 2G station on {ssid_name} ssid...")
        radio = None
        for _radio in radio_dict_2g:
            radio = _radio
            if radio_dict_2g[radio] == 1:
                del radio_dict_2g[radio]
            else:
                radio_dict_2g[radio] -= 1
            break
        sta_got_ip.append(test_lib.client_connect_using_radio(ssid=ssid_name, security=security,
                                                              passkey=security_key, mode=mode,
                                                              radio=radio,
                                                              station_name=[sta_names_2g[i]],
                                                              attach_station_data=False,
                                                              attach_port_info=False))
        logging.info(f"Creating a 5G station on {ssid_name} ssid...")
        for _radio in radio_dict_5g:
            radio = _radio
            if radio_dict_5g[radio] == 1:
                del radio_dict_5g[radio]
            else:
                radio_dict_5g[radio] -= 1
            break
        sta_got_ip.append(test_lib.client_connect_using_radio(ssid=ssid_name, security=security,
                                                              passkey=security_key, mode=mode,
                                                              radio=radio,
                                                              station_name=[sta_names_5g[i]],
                                                              attach_station_data=False,
                                                              attach_port_info=False))

    port_data = test_lib.json_get(_req_url="port?fields=ip")
    port_info = {key: value for d in port_data["interfaces"] for key, value in d.items()}
    test_lib.allure_report_table_format(dict_data=port_info, key="Port Names", value="ip",
                                                name="Port info after creating all stations")

    dict_table_2g_1st = {}
    dict_table_2g_2nd = {}
    dict_table_5g_1st = {}
    dict_table_5g_2nd = {}
    for sta in sta_names_2g + sta_names_5g:
        result = test_lib.json_get(_req_url="port/1/1/%s" % sta)
        if "Key" not in dict_table_2g_1st:
            dict_table_2g_1st["Key"] = list(result["interface"].keys())
            dict_table_2g_2nd["Key"] = list(result["interface"].keys())
            dict_table_5g_1st["Key"] = list(result["interface"].keys())
            dict_table_5g_2nd["Key"] = list(result["interface"].keys())
        if '_2g_' in sta:
            if len(dict_table_2g_1st) < 5:
                dict_table_2g_1st[f"Value ({sta})"] = list(result["interface"].values())
            else:
                dict_table_2g_2nd[f"Value ({sta})"] = list(result["interface"].values())
        else:
            if len(dict_table_5g_1st) < 5:
                dict_table_5g_1st[f"Value ({sta})"] = list(result["interface"].values())
            else:
                dict_table_5g_2nd[f"Value ({sta})"] = list(result["interface"].values())

    data_table_2g_1st = tabulate.tabulate(dict_table_2g_1st, headers='keys', tablefmt='fancy_grid')
    data_table_2g_2nd = tabulate.tabulate(dict_table_2g_2nd, headers='keys', tablefmt='fancy_grid')
    data_table_5g_1st = tabulate.tabulate(dict_table_5g_1st, headers='keys', tablefmt='fancy_grid')
    data_table_5g_2nd = tabulate.tabulate(dict_table_5g_2nd, headers='keys', tablefmt='fancy_grid')

    logging.info(f"2G Stations Data (1-{min(4, no_of_2g_and_5g_stations)}): \n{data_table_2g_1st}\n")
    allure.attach(name=f"2G Stations Data (1-{min(4, no_of_2g_and_5g_stations)})", body=str(data_table_2g_1st))
    if no_of_2g_and_5g_stations > 4:
        logging.info(f"2G Stations Data (5-{no_of_2g_and_5g_stations}): \n{data_table_2g_2nd}\n")
        allure.attach(name=f"2G Stations Data (5-{no_of_2g_and_5g_stations})", body=str(data_table_2g_2nd))

    logging.info(f"5G Stations Data (1-{min(4, no_of_2g_and_5g_stations)}): \n{data_table_5g_1st}\n")
    allure.attach(name=f"5G Stations Data (1-{min(4, no_of_2g_and_5g_stations)})", body=str(data_table_5g_1st))
    if no_of_2g_and_5g_stations > 4:
        logging.info(f"5G Stations Data (5-{no_of_2g_and_5g_stations}): \n{data_table_5g_2nd}\n")
        allure.attach(name=f"5G Stations Data (5-{no_of_2g_and_5g_stations})", body=str(data_table_5g_2nd))

    if False in sta_got_ip:
        logging.info("Some/All Stations didn't get IP address")
        pytest.fail("Some/All Stations didn't get IP address")
    logging.info("All 2G/5G Stations got IP address")

    # create Layer 3 and check data path
    for i in range(3):
        test_lib.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                               side_b_min_rate=6291456, side_b_max_rate=0,
                               traffic_type="lf_tcp", sta_list=[cx_sta_list[i]],
                               side_b=cx_sta_list[i + 1], start_cx=True,
                               prefix=f"{cx_sta_list[i][4:]}-{cx_sta_list[i + 1][4:]}:t")
        logging.info(f"CX with TCP traffic created between "
                     f"endpoint-a = {cx_sta_list[i]} and endpoint-b = {cx_sta_list[i + 1]}.")
        time.sleep(2)
        test_lib.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                               side_b_min_rate=6291456, side_b_max_rate=0,
                               traffic_type="lf_udp", sta_list=[cx_sta_list[i]],
                               side_b=cx_sta_list[i + 1], start_cx=True,
                               prefix=f"{cx_sta_list[i][4:]}-{cx_sta_list[i + 1][4:]}:u")
        logging.info(f"CX with UDP traffic created between "
                     f"endpoint-a = {cx_sta_list[i]} and endpoint-b = {cx_sta_list[i + 1]}.")
        time.sleep(2)

    logging.info("Running Layer3 traffic for 40 sec ...")
    time.sleep(40)

    cx_list = test_lib.get_cx_list()
    dict_table_cx_tcp = {}
    dict_table_cx_udp = {}
    pass_fail_data = []
    for i in range(len(cx_list)):
        cx_data = test_lib.json_get(_req_url=f"cx/{cx_list[i]}")
        cx_name = f"sta_{cx_list[i].split(':')[0].split('-')[0]} <==> sta_{cx_list[i].split(':')[0].split('-')[1]}"

        if "L3 CX Column" not in dict_table_cx_tcp:
            dict_table_cx_tcp["L3 CX Column"] = list(cx_data[f"{cx_list[i]}"].keys())
            dict_table_cx_udp["L3 CX Column"] = list(cx_data[f"{cx_list[i]}"].keys())
        if "TCP" in cx_data[f"{cx_list[i]}"]['type']:
            dict_table_cx_tcp[f"values ({cx_name})"] = list(cx_data[f"{cx_list[i]}"].values())
        else:
            dict_table_cx_udp[f"values ({cx_name})"] = list(cx_data[f"{cx_list[i]}"].values())

        if cx_data[cx_list[i]]['bps rx a'] != 0 and cx_data[cx_list[i]]['bps rx a'] != 0:
            res = True
        else:
            res = False
        pass_fail_data.append(
            [f"{cx_list[i]}", f"{cx_data[cx_list[i]]['bps rx a']}", f"{cx_data[cx_list[i]]['bps rx b']}", res])

    # attach l3 cx data to allure
    data_table_cx_tcp = tabulate.tabulate(dict_table_cx_tcp, headers='keys', tablefmt='fancy_grid')
    data_table_cx_udp = tabulate.tabulate(dict_table_cx_udp, headers='keys', tablefmt='fancy_grid')
    logging.info(f"L3 cross-connects Data (TCP): \n{data_table_cx_tcp}\n")
    logging.info(f"L3 cross-connects Data (UDP): \n{data_table_cx_udp}\n")
    allure.attach(name="L3 cross-connects Data (TCP)", body=str(data_table_cx_tcp))
    allure.attach(name="L3 cross-connects Data (UDP)", body=str(data_table_cx_udp))

    # attach pass fail data to allure
    result_table = tabulate.tabulate(pass_fail_data,
                                     headers=["Data Path", "Tx Rate (bps)", "Rx Rate (bps)", "Pass/Fail"],
                                     tablefmt='fancy_grid')
    logging.info(f"Test Result Table: \n{result_table}\n")
    allure.attach(name="Test Result Table", body=str(result_table))

    # cleanup Layer3 data
    test_lib.client_disconnect(station_name=sta_names_2g + sta_names_5g, clean_l3_traffic=True,
                                       clear_all_sta=True)

    test_result = True
    for pf in pass_fail_data:
        if pf[3] is False:
            test_result = False

    if not test_result:
        pytest.fail("DataPath check failed, Traffic didn't reported on some endpoints")


setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
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
        multi_ssid_test(test_lib=get_test_library, setup_params_general=setup_params_general1,
                        no_of_2g_and_5g_stations=2)


setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
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
        multi_ssid_test(test_lib=get_test_library, setup_params_general=setup_params_general2,
                        no_of_2g_and_5g_stations=2)


setup_params_general3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
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
        multi_ssid_test(test_lib=get_test_library, setup_params_general=setup_params_general3,
                        no_of_2g_and_5g_stations=3)


setup_params_general4 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid4_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
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
        multi_ssid_test(test_lib=get_test_library, setup_params_general=setup_params_general4,
                        no_of_2g_and_5g_stations=4)


setup_params_general5 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid4_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid5_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
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

        multi_ssid_test(test_lib=get_test_library, setup_params_general=setup_params_general5,
                        no_of_2g_and_5g_stations=5)


setup_params_general6 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid4_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid5_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid6_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
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
        multi_ssid_test(test_lib=get_test_library, setup_params_general=setup_params_general6,
                        no_of_2g_and_5g_stations=6)


setup_params_general7 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid4_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid5_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid6_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid7_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
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
        multi_ssid_test(test_lib=get_test_library, setup_params_general=setup_params_general7,
                        no_of_2g_and_5g_stations=7)


setup_params_general8 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "multi_ssid1_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid2_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid3_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid4_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid5_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid6_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid7_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"},
            {"ssid_name": "multi_ssid8_wpa2", "appliedRadios": ["2G", "5G"], "security_key": "something"}
        ],
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
        multi_ssid_test(test_lib=get_test_library, setup_params_general=setup_params_general8,
                        no_of_2g_and_5g_stations=8)
