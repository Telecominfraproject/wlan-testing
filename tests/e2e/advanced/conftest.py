import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)
if "libs" not in sys.path:
    sys.path.append(f'../libs')

from controller.controller_1x.controller import ProfileUtility
from controller.controller_2x.controller import UProfileUtility
import time
from lanforge.lf_tests import RunTest
from lanforge.lf_tools import ChamberView
import pytest
import allure


@pytest.fixture(scope="session")
def instantiate_profile(request):
    if request.config.getoption("1.x"):
        yield ProfileUtility
    else:
        yield UProfileUtility





@pytest.fixture(scope="session")
def create_lanforge_chamberview(lf_tools):
    scenario_object, scenario_name = lf_tools.Chamber_View()
    return scenario_name


@pytest.fixture(scope="session")
def setup_vlan():
    vlan_id = [100]
    allure.attach(body=str(vlan_id), name="VLAN Created: ")
    yield vlan_id[0]



@pytest.fixture(scope="class")
def setup_profiles(request, setup_controller, testbed, get_equipment_ref, fixtures_ver,
                   instantiate_profile, get_markers, create_lanforge_chamberview_dut, lf_tools,
                   get_security_flags, get_configuration, radius_info, get_apnos, radius_accounting_info, run_lf):
    lf_tools.reset_scenario()
    param = dict(request.param)

    # VLAN Setup
    if request.param["mode"] == "VLAN":

        vlan_list = list()
        refactored_vlan_list = list()
        ssid_modes = request.param["ssid_modes"].keys()
        for mode in ssid_modes:
            for ssid in range(len(request.param["ssid_modes"][mode])):
                if "vlan" in request.param["ssid_modes"][mode][ssid]:
                    vlan_list.append(request.param["ssid_modes"][mode][ssid]["vlan"])
                else:
                    pass
        if vlan_list:
            [refactored_vlan_list.append(x) for x in vlan_list if x not in refactored_vlan_list]
            vlan_list = refactored_vlan_list
            for i in range(len(vlan_list)):
                if vlan_list[i] > 4095 or vlan_list[i] < 1:
                    vlan_list.pop(i)
    if request.param["mode"] == "VLAN":
        lf_tools.add_vlan(vlan_ids=vlan_list)

    # call this, if 1.x
    return_var = fixtures_ver.setup_profiles(request, param, setup_controller, testbed, get_equipment_ref,
                                             instantiate_profile,
                                             get_markers, create_lanforge_chamberview_dut, lf_tools,
                                             get_security_flags, get_configuration, radius_info, get_apnos,
                                             radius_accounting_info, run_lf=run_lf)

    yield return_var


@pytest.fixture(scope="session")
def station_names_twog(request, get_configuration):
    station_names = []
    for i in range(0, int(request.config.getini("num_stations"))):
        station_names.append(get_configuration["traffic_generator"]["details"]["2.4G-Station-Name"] + "0" + str(i))
    yield station_names


@pytest.fixture(scope="session")
def station_names_fiveg(request, get_configuration):
    station_names = []
    for i in range(0, int(request.config.getini("num_stations"))):
        station_names.append(get_configuration["traffic_generator"]["details"]["5G-Station-Name"] + "0" + str(i))
    yield station_names


@pytest.fixture(scope="session")
def num_stations(request):
    num_sta = int(request.config.getini("num_stations"))
    yield num_sta


@pytest.fixture(scope="class")
def get_vif_state(get_apnos, get_configuration):
    ap_ssh = get_apnos(get_configuration['access_point'][0], pwd="../libs/apnos/")
    vif_config = list(ap_ssh.get_vif_config_ssids())
    vif_state = list(ap_ssh.get_vif_state_ssids())
    vif_state.sort()
    vif_config.sort()
    allure.attach(name="vif_state", body=str(vif_state))
    yield vif_state

@pytest.fixture(scope="class")
def get_vlan_list(get_apnos, get_configuration):
    ap_ssh = get_apnos(get_configuration['access_point'][0], pwd="../libs/apnos/")
    vlan_list = list(ap_ssh.get_vlan())
    vlan_list.sort()
    allure.attach(name="vlan_list", body=str(vlan_list))
    yield vlan_list

