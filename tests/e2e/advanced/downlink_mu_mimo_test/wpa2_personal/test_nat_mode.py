"""

    Performance Test: Downlink MU-MIMO Test: NAT Mode
    pytest -m "downlink_mu_mimo and nat and wpa2_personal"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.mu_mimo_performance_tests, pytest.mark.nat, pytest.mark.wpa2_personal]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"}
        ]
    },
    "rf": [],
    "radius": False
}

@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@allure.parent_suite("Downlink MU_MIMO Tests")
@allure.suite("WPA2 Personal Security")
@allure.sub_suite("NAT Mode")
@allure.feature("TR-398 Issue 2")
@pytest.mark.usefixtures("setup_configuration")
class TestMuMimoNat(object):
    """
    Downlink MU-MIMO Test: nat Mode
    pytest -m downlink_mu_mimo and nat
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6849",
                     name="WIFI-6849")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_mu_mimo_wpa2_personal_nat_5g(self, get_test_library, setup_configuration, check_connectivity):
        """
            Downlink MU-MIMO Test: Nat Mode
            pytest -m downlink_mu_mimo and nat and wpa2_personal and fiveg
        """
        profile_data = {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT-WAN"
        band = "fiveg"
        mode = "BRIDGE"
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
            if get_test_library.dut_idx_mapping[str(i)][3] == "5G":
                dut_5g = dut_name + ' ' + get_test_library.dut_idx_mapping[str(i)][0] + ' ' \
                                                                                        '' + \
                         get_test_library.dut_idx_mapping[str(i)][4] + f' (1)'
        result, description = get_test_library.tr398(radios_2g=radios_2g, radios_5g=radios_5g, radios_ax=radios_ax,
                                                     dut_name=dut_name, dut_5g=dut_5g, dut_2g=dut_2g,  mode=mode,
                                                     vlan_id=vlan,  skip_2g=True, skip_5g=False, test="mu_mimo",
                                                     ssid_name=ssid_name, security_key=security_key, security=security,
                                                     move_to_influx=False, dut_data=setup_configuration, sniff_packets=False,
                                                     tr398=True)
        if result:
            assert True
        else:
            assert False, description
