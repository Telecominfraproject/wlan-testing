"""

    Performance Test: Receiver Sensitivity Test: bridge Mode
    pytest -m "rx_sensitivity_tests and wpa2_personal and bridge"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.rx_sensitivity_tests, pytest.mark.bridge, pytest.mark.wpa2_personal]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}]},
        "rf": {
            "2G": {"channel-width": 20},
            "5G": {"channel-width": 80},
        },
    "radius": False,
}


@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@allure.parent_suite("Receiver Sensitivity Tests")
@allure.suite("WPA2 Personal Security")
@allure.sub_suite("Bridge Mode")
@allure.feature("TR-398 Issue 2")
@pytest.mark.usefixtures("setup_configuration")
class TestRxSensitivityBRIDGE2G(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2446", name="WIFI-2446")
    @pytest.mark.twog
    @allure.title("Test for Receiver Sensitivity for 2.4G band")
    def test_client_wpa2_personal_bridge_2g(self, get_test_library, setup_configuration, check_connectivity):
        """Receiver Sensitivity Bridge Mode
           pytest -m "rx_sensitivity_tests and bridge and wpa2_personal and twog"
        """
        profile_data = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        dut_name = list(setup_configuration.keys())[0]
        dut_5g, dut_2g = "", ""
        radios_2g, radios_5g, radios_ax = [], [], []
        data = get_test_library.json_get(_req_url="/port?fields=alias,port,mode")
        data = data['interfaces']
        port, port_data = "", []
        for i in data:
            for j in i:
                if i[j]['mode'] != '':
                    port_data.append(i)

        for item in range(len(port_data)):
            for p in port_data[item]:
                temp = port_data[item][p]['port'].split('.')
                temp = list(map(int, temp))
                temp = list(map(str, temp))
                port = ".".join(temp)
                if port_data[item][p]['mode'] == '802.11bgn-AC':
                    radios_2g.append(port + " " + port_data[item][p]['alias'])
                if port_data[item][p]['mode'] == '802.11an-AC':
                    radios_5g.append(port + " " + port_data[item][p]['alias'])
                if port_data[item][p]['mode'] == '802.11abgn-AX':
                    radios_ax.append(port + " " + port_data[item][p]['alias'])
        for i in setup_configuration[dut_name]['ssid_data']:
            get_test_library.dut_idx_mapping[str(i)] = list(setup_configuration[dut_name]['ssid_data'][i].values())
            dut_5g = dut_name + ' ' + get_test_library.dut_idx_mapping[str(i)][0] + ' ' \
                    '' + get_test_library.dut_idx_mapping[str(i)][4] + f' ({i+1})' \
                    f'' if get_test_library.dut_idx_mapping[str(i)][3] == "5G" else "NA"

            dut_2g = dut_name + ' ' + get_test_library.dut_idx_mapping[str(i)][0] + ' ' \
                   '' + get_test_library.dut_idx_mapping[str(i)][4] + f' ({i+1})' \
                    f'' if get_test_library.dut_idx_mapping[str(i)][3] == "2G" else "NA"

        instance_name = "rx_sens_TR398"
        result, description = get_test_library.tr398(radios_2g=radios_2g, radios_5g=radios_5g, radios_ax=radios_ax,dut_name=dut_name,
                                           dut_5g=dut_5g, dut_2g=dut_2g, mode=mode, vlan_id=vlan, skip_2g=False,
                                           skip_5g=True, instance_name=instance_name, test="rxsens", ssid_name=ssid_name,
                                           security_key=security_key, security=security,
                                           move_to_influx=False, dut_data=setup_configuration)

        if result:
            assert True
        else:
            assert False, description

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2446", name="WIFI-2446")
    @pytest.mark.fiveg
    @allure.title("Test for Receiver Sensitivity for 5G band")
    def test_client_wpa2_personal_bridge_5g(self, get_test_library, setup_configuration, check_connectivity):
        """Receiver Sensitivity Bridge Mode
           pytest -m "rx_sensitivity_tests and bridge and wpa2_personal and fiveg"
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = list(setup_configuration.keys())[0]
        dut_5g, dut_2g = "", ""
        radios_2g, radios_5g, radios_ax = [], [], []
        data = get_test_library.json_get(_req_url="/port?fields=alias,port,mode")
        data = data['interfaces']
        port, port_data = "", []
        for i in data:
            for j in i:
                if i[j]['mode'] != '':
                    port_data.append(i)

        for item in range(len(port_data)):
            for p in port_data[item]:
                temp = port_data[item][p]['port'].split('.')
                temp = list(map(int, temp))
                temp = list(map(str, temp))
                port = ".".join(temp)
                if port_data[item][p]['mode'] == '802.11bgn-AC':
                    radios_2g.append(port + " " + port_data[item][p]['alias'])
                if port_data[item][p]['mode'] == '802.11an-AC':
                    radios_5g.append(port + " " + port_data[item][p]['alias'])
                if port_data[item][p]['mode'] == '802.11abgn-AX':
                    radios_ax.append(port + " " + port_data[item][p]['alias'])
        for i in setup_configuration[dut_name]['ssid_data']:
            get_test_library.dut_idx_mapping[str(i)] = list(setup_configuration[dut_name]['ssid_data'][i].values())
            dut_5g = dut_name + ' ' + get_test_library.dut_idx_mapping[str(i)][0] + ' ' \
                                                                                    '' + \
                     get_test_library.dut_idx_mapping[str(i)][4] + f' ({i + 1})' \
                                                                   f'' if get_test_library.dut_idx_mapping[str(i)][
                                                                              3] == "5G" else "NA"

            dut_2g = dut_name + ' ' + get_test_library.dut_idx_mapping[str(i)][0] + ' ' \
                                                                                    '' + \
                     get_test_library.dut_idx_mapping[str(i)][4] + f' ({i + 1})' \
                                                                   f'' if get_test_library.dut_idx_mapping[str(i)][
                                                                              3] == "2G" else "NA"

        instance_name = "rx_sens_TR398"
        result, description = get_test_library.tr398(radios_2g=radios_2g, radios_5g=radios_5g, radios_ax=radios_ax,
                                                     dut_name=dut_name, dut_5g=dut_5g, dut_2g=dut_2g, mode=mode,
                                                     vlan_id=vlan, skip_2g=True, skip_5g=False, instance_name=instance_name,
                                                     test="rxsens", ssid_name=ssid_name, security_key=security_key,
                                                     security=security, move_to_influx=False, dut_data=setup_configuration)

        if result:
            assert True
        else:
            assert False, description