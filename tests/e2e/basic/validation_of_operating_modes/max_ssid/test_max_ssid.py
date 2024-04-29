"""
    Config AP with maximum no.of SSIDs Test: Bridge Mode
    pytest -m max_ssid
"""
import logging
import time
import allure
import pytest
import tabulate

pytestmark = [pytest.mark.max_ssid, pytest.mark.bridge, pytest.mark.open, pytest.mark.wpa, pytest.mark.wpa2_personal,
              pytest.mark.wpa3_personal]


def get_radio_availabilities(num_stations_2g: int = 0, num_stations_5g: int = 0, test_lib=None) -> tuple:
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


def max_ssid(setup_params_general: dict, test_lib=None) -> None:
    test_lib.pre_cleanup()

    ssid_2g_list = []
    ssid_5g_list = []
    for mode, ssids in setup_params_general["ssid_modes"].items():
        for ssid in ssids:
            ssid_dict = {
                'ssid_name': ssid["ssid_name"],
                'mode': mode.split("_")[0],
                'password': ssid.get("security_key", "[BLANK]"),
            }
            if "2G" in ssid["appliedRadios"]:
                ssid_2g_list.append(ssid_dict)
            elif "5G" in ssid["appliedRadios"]:
                ssid_5g_list.append(ssid_dict)

    no_of_sta_2g = len(ssid_2g_list)
    no_of_sta_5g = len(ssid_5g_list)
    sta_names_2g = [f"sta_2g_{i + 1}" for i in range(no_of_sta_2g)]
    sta_names_5g = [f"sta_5g_{i + 1}" for i in range(no_of_sta_5g)]

    radio_dict_2g, radio_dict_5g = get_radio_availabilities(num_stations_2g=no_of_sta_2g,
                                                            num_stations_5g=no_of_sta_5g,
                                                            test_lib=test_lib)
    if len(radio_dict_2g) > 0:
        logging.info(f"Radio-Stations dict : {radio_dict_2g}")
    if len(radio_dict_5g) > 0:
        logging.info(f"Radio-Stations dict : {radio_dict_5g}")

    if no_of_sta_2g > 0:
        logging.info(f"A total of {no_of_sta_2g} 2G stations will be created for {no_of_sta_2g} SSIDs, "
                     f"i.e., one 2G stations on each SSID.")
    if no_of_sta_5g > 0:
        logging.info(f"A total of {no_of_sta_5g} 5G stations will be created for {no_of_sta_5g} SSIDs, "
                     f"i.e., one 5G stations on each SSID.")

    sta_got_ip = []
    radio = None
    timeout_sec = 100 if no_of_sta_2g <= 8 and no_of_sta_5g <= 8 else 15
    for i in range(no_of_sta_2g):
        logging.info(f"Creating a 2G station on {ssid_2g_list[i]['ssid_name']} ssid...")
        for _radio in radio_dict_2g:
            radio = _radio
            if radio_dict_2g[radio] == 1:
                del radio_dict_2g[radio]
            else:
                radio_dict_2g[radio] -= 1
            break
        sta_got_ip.append(test_lib.client_connect_using_radio(ssid=ssid_2g_list[i]['ssid_name'],
                                                              security=ssid_2g_list[i]['mode'],
                                                              passkey=ssid_2g_list[i]['password'],
                                                              mode="BRIDGE",
                                                              radio=radio,
                                                              station_name=[sta_names_2g[i]],
                                                              attach_station_data=False,
                                                              attach_port_info=False,
                                                              timeout_sec=timeout_sec))
    for i in range(no_of_sta_5g):
        logging.info(f"Creating a 5G station on {ssid_5g_list[i]['ssid_name']} ssid...")
        for _radio in radio_dict_5g:
            radio = _radio
            if radio_dict_5g[radio] == 1:
                del radio_dict_5g[radio]
            else:
                radio_dict_5g[radio] -= 1
            break
        sta_got_ip.append(test_lib.client_connect_using_radio(ssid=ssid_5g_list[i]['ssid_name'],
                                                              security=ssid_5g_list[i]['mode'],
                                                              passkey=ssid_5g_list[i]['password'],
                                                              mode="BRIDGE",
                                                              radio=radio,
                                                              station_name=[sta_names_5g[i]],
                                                              attach_station_data=False,
                                                              attach_port_info=False,
                                                              timeout_sec=timeout_sec))

    logging.info("Fetching port info after all stations created")
    port_data = test_lib.json_get(_req_url="port?fields=ip")
    port_info = {key: value for d in port_data["interfaces"] for key, value in d.items()}
    test_lib.allure_report_table_format(dict_data=port_info, key="Port Names", value="ip",
                                        name="Port info after creating all stations")

    logging.info("Adding Station Data to the report")
    dict_table_sta = {}
    start_sta, end_sta = 1, 0
    for index, sta in enumerate(sta_names_2g):
        end_sta += 1
        result = test_lib.json_get(_req_url="port/1/1/%s" % sta)
        if "Key" not in dict_table_sta:
            dict_table_sta["Key"] = list(result["interface"].keys())
        dict_table_sta[f"Value ({sta})"] = list(result["interface"].values())

        if end_sta - start_sta == 3 or index == len(sta_names_2g) - 1:
            data_table_sta = tabulate.tabulate(dict_table_sta, headers='keys', tablefmt='fancy_grid')
            logging.info(f"2G-Stations Data ({start_sta}-{end_sta}): \n{data_table_sta}\n")
            allure.attach(name=f"2G-Stations Data ({start_sta}-{end_sta})", body=str(data_table_sta))
            start_sta = end_sta + 1
            dict_table_sta.clear()

    start_sta, end_sta = 1, 0
    for index, sta in enumerate(sta_names_5g):
        end_sta += 1
        result = test_lib.json_get(_req_url="port/1/1/%s" % sta)
        if "Key" not in dict_table_sta:
            dict_table_sta["Key"] = list(result["interface"].keys())
        dict_table_sta[f"Value ({sta})"] = list(result["interface"].values())

        if end_sta - start_sta == 3 or index == len(sta_names_5g) - 1:
            data_table_sta = tabulate.tabulate(dict_table_sta, headers='keys', tablefmt='fancy_grid')
            logging.info(f"5G-Stations Data ({start_sta}-{end_sta}): \n{data_table_sta}\n")
            allure.attach(name=f"5G-Stations Data ({start_sta}-{end_sta})", body=str(data_table_sta))
            start_sta = end_sta + 1
            dict_table_sta.clear()

    if no_of_sta_2g > 8 or no_of_sta_5g > 8:
        if True in sta_got_ip:
            logging.info("Some/All stations got the IP when more than 8 SSIDs were configured on a single band!")
            pytest.fail("Some/All stations got the IP when more than 8 SSIDs were configured on a single band!")
        else:
            logging.info("As expected, None of the stations got the IP when more than 8 SSIDs were configured "
                         "on a single band!")
            test_lib.pre_cleanup()
            return

    if False in sta_got_ip:
        logging.info("Some/All Stations didn't get IP address")
        pytest.fail("Some/All Stations didn't get IP address")
    logging.info("All Stations got IP address")

    logging.info("Creating Layer3 traffic on stations...")
    for sta in sta_names_2g + sta_names_5g:
        test_lib.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                               side_b_min_rate=6291456, side_b_max_rate=0,
                               traffic_type="lf_tcp", sta_list=[sta], side_b="",
                               start_cx=True, prefix=f"t-")
        logging.info(f"CX with TCP traffic created between endpoint-a = {sta} and endpoint-b = upstream port.")
        time.sleep(2)
        test_lib.create_layer3(side_a_min_rate=6291456, side_a_max_rate=0,
                               side_b_min_rate=6291456, side_b_max_rate=0,
                               traffic_type="lf_udp", sta_list=[sta], side_b="",
                               start_cx=True, prefix=f"u-")
        logging.info(f"CX with UDP traffic created between endpoint-a = {sta} and endpoint-b = upstream port.")
        time.sleep(2)

    logging.info("Running Layer3 traffic for 40 sec ...")
    time.sleep(40)

    logging.info("Fetching CX data and adding it to the report...")
    cx_list = test_lib.get_cx_list()
    dict_table_cx_tcp = {}
    dict_table_cx_udp = {}
    pass_fail_data = []
    overall_test = True
    start_tcp, start_udp = 1, 1
    end_tcp, end_udp = 0, 0
    for i in range(len(cx_list)):
        cx_data = test_lib.json_get(_req_url=f"cx/{cx_list[i]}")
        cx_name = f"{cx_list[i].split('-')[1]}"

        if "L3 CX Column" not in dict_table_cx_tcp:
            dict_table_cx_tcp["L3 CX Column"] = list(cx_data[f"{cx_list[i]}"].keys())
        if "L3 CX Column" not in dict_table_cx_udp:
            dict_table_cx_udp["L3 CX Column"] = list(cx_data[f"{cx_list[i]}"].keys())
        if "TCP" in cx_data[f"{cx_list[i]}"]['type']:
            end_tcp += 1
            dict_table_cx_tcp[f"values ({cx_name})"] = list(cx_data[f"{cx_list[i]}"].values())
        else:
            end_udp += 1
            dict_table_cx_udp[f"values ({cx_name})"] = list(cx_data[f"{cx_list[i]}"].values())

        if cx_data[cx_list[i]]['bps rx a'] != 0 and cx_data[cx_list[i]]['bps rx a'] != 0:
            res = True
        else:
            overall_test = False
            res = False
        pass_fail_data.append(
            [f"{cx_list[i][:-2]}", f"{cx_data[cx_list[i]]['bps rx a']}", f"{cx_data[cx_list[i]]['bps rx b']}", res])

        # attach l3 cx data to allure
        if end_tcp - start_tcp == 3 or (i == len(cx_list) - 1 and start_tcp <= end_tcp):
            data_table_cx_tcp = tabulate.tabulate(dict_table_cx_tcp, headers='keys', tablefmt='fancy_grid')
            logging.info(f"L3 cross-connects Data (TCP) ({start_tcp} - {end_tcp}): \n{data_table_cx_tcp}\n")
            allure.attach(name=f"L3 cross-connects Data (TCP) ({start_tcp} - {end_tcp})", body=str(data_table_cx_tcp))
            start_tcp = end_tcp + 1
            dict_table_cx_tcp.clear()
        if end_udp - start_udp == 3 or (i == len(cx_list) - 1 and start_udp <= end_udp):
            data_table_cx_udp = tabulate.tabulate(dict_table_cx_udp, headers='keys', tablefmt='fancy_grid')
            logging.info(f"L3 cross-connects Data (UDP) ({start_udp} - {end_udp}): \n{data_table_cx_udp}\n")
            allure.attach(name=f"L3 cross-connects Data (UDP) ({start_udp} - {end_udp})", body=str(data_table_cx_udp))
            start_udp = end_udp + 1
            dict_table_cx_udp.clear()

    logging.info("Attaching pass/fail data to the report...")
    result_table = tabulate.tabulate(pass_fail_data,
                                     headers=["Data Path", "Tx Rate (bps)", "Rx Rate (bps)", "Pass/Fail"],
                                     tablefmt='fancy_grid')
    logging.info(f"Test Result Table: \n{result_table}\n")
    allure.attach(name="Test Result Table", body=str(result_table))

    test_lib.pre_cleanup()

    if overall_test is False:
        pytest.fail("DataPath check failed, Traffic didn't reported on some endpoints")
    logging.info("All Traffic reported on all endpoints, test successful!")


setup_params_general0 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"]}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@allure.parent_suite("Max-SSID Tests")
@allure.suite("Bridge Mode")
@allure.sub_suite("Only 2.4GHz Band")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general0],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMaxEightSsid2G(object):
    @allure.title("8-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.twog
    @pytest.mark.eight_ssid_2g
    def test_max_eight_ssid_2g(self, get_test_library, get_dut_logs_per_test_case, setup_configuration,
                               get_test_device_logs, check_connectivity):
        """
        Unique Marker: max_ssid and bridge and eight_ssid_2g
        """

        max_ssid(setup_params_general=setup_params_general0, test_lib=get_test_library)


setup_params_general1 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"]},
            {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"]}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@allure.parent_suite("Max-SSID Tests")
@allure.suite("Bridge Mode")
@allure.sub_suite("Only 5GHz Band")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general1],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMaxEightSsid5G(object):
    @allure.title("8-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.fiveg
    @pytest.mark.eight_ssid_5g
    def test_max_eight_ssid_5g(self, get_test_library, get_dut_logs_per_test_case, setup_configuration,
                               get_test_device_logs, check_connectivity):
        """
        Unique Marker: max_ssid and bridge and eight_ssid_5g
        """

        max_ssid(setup_params_general=setup_params_general1, test_lib=get_test_library)


setup_params_general2 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"]}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid3_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@allure.parent_suite("Max-SSID Tests")
@allure.suite("Bridge Mode")
@allure.sub_suite("Only 2.4GHz Band")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general2],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMoreThanEightSsid2G(object):
    @allure.title("Trying more than 8-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.twog
    @pytest.mark.more_than_eight_ssid_2g
    def test_more_than_eight_ssid_2g(self, get_test_library, get_dut_logs_per_test_case, setup_configuration,
                                     get_test_device_logs, check_connectivity):
        """
        Unique Marker: max_ssid and bridge and more_than_eight_ssid_2g
        """

        max_ssid(setup_params_general=setup_params_general2, test_lib=get_test_library)


setup_params_general3 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"]},
            {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"]}],

        "wpa": [
            {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid3_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}],
    },
    "rf": {},
    "radius": False
}


@allure.parent_suite("Max-SSID Tests")
@allure.suite("Bridge Mode")
@allure.sub_suite("Only 5GHz Band")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general3],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMoreThanEightSsid5G(object):
    @allure.title("Trying more than 8-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.fiveg
    @pytest.mark.more_than_eight_ssid_5g
    def test_more_than_eight_ssid_5g(self, get_test_library, get_dut_logs_per_test_case, setup_configuration,
                                     get_test_device_logs, check_connectivity):
        """
        Unique Marker: max_ssid and bridge and more_than_eight_ssid_5g
        """

        max_ssid(setup_params_general=setup_params_general3, test_lib=get_test_library)


setup_params_general4 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"]},
                 {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"]}],

        "wpa": [{"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"},
                {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}],
        },
    "rf": {},
    "radius": False
}


@allure.parent_suite("Max-SSID Tests")
@allure.suite("Bridge Mode")
@allure.sub_suite("Both 2.4GHz and 5GHz Band")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general4],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMaxSixteenSsid(object):
    @allure.title("16-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.sixteen_ssid_2g_5g
    def test_max_sixteen_2g_5g(self, get_test_library, get_dut_logs_per_test_case, setup_configuration,
                                     get_test_device_logs, check_connectivity):
        """
        Unique Marker: max_ssid and bridge and sixteen_ssid_2g_5g
        """

        max_ssid(setup_params_general=setup_params_general4, test_lib=get_test_library)


setup_params_general5 = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid1_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid2_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid1_open_5g", "appliedRadios": ["5G"]},
                 {"ssid_name": "ssid2_open_5g", "appliedRadios": ["5G"]}],

        "wpa": [{"ssid_name": "ssid1_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid2_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid1_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"},
                {"ssid_name": "ssid2_wpa_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa2_personal": [
            {"ssid_name": "ssid1_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid1_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}],

        "wpa3_personal": [
            {"ssid_name": "ssid1_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid3_wpa3_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid1_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid2_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid3_wpa3_5g", "appliedRadios": ["5G"], "security_key": "something"}],
        },
    "rf": {},
    "radius": False
}


@allure.parent_suite("Max-SSID Tests")
@allure.suite("Bridge Mode")
@allure.sub_suite("Both 2.4GHz and 5GHz Band")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general5],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestMoreThanSixteenSsid(object):
    @allure.title("Trying more than 16-SSIDs")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7678", name="WIFI-7678")
    @pytest.mark.twog
    @pytest.mark.fiveg
    @pytest.mark.more_than_sixteen_ssid_2g_5g
    def test_more_than_sixteen_2g_5g(self, get_test_library, get_dut_logs_per_test_case, setup_configuration,
                                     get_test_device_logs, check_connectivity):
        """
        Unique Marker: max_ssid and bridge and more_than_sixteen_ssid_2g_5g
        """

        max_ssid(setup_params_general=setup_params_general5, test_lib=get_test_library)
