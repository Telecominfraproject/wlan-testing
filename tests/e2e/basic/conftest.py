import os
import sys

for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../lanforge/lanforge-scripts/{folder}')

sys.path.append(f"../lanforge/lanforge-scripts/py-scripts/tip-cicd-sanity")

sys.path.append(f'../libs')
sys.path.append(f'../libs/lanforge/')

from LANforge.LFUtils import *

if 'py-json' not in sys.path:
    sys.path.append('../py-scripts')

sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)
if "libs" not in sys.path:
    sys.path.append(f'../libs')

from controller.controller import ProfileUtility
import time
from lanforge.lf_tests import RunTest
import pytest

import logging
from configuration import RADIUS_SERVER_DATA
from configuration import TEST_CASES
from configuration import CONFIGURATION
from configuration import FIRMWARE
from testrails.testrail_api import APIClient
from testrails.reporting import Reporting
import allure
from cv_test_manager import cv_test
from create_chamberview import CreateChamberview
from create_chamberview_dut import DUT

"""
Basic Setup Collector
"""


@pytest.fixture(scope="session")
def get_lanforge_data(testbed):
    lanforge_data = {}
    if CONFIGURATION[testbed]['traffic_generator']['name'] == 'lanforge':
        lanforge_data = {
            "lanforge_ip": CONFIGURATION[testbed]['traffic_generator']['details']['ip'],
            "lanforge-port-number": CONFIGURATION[testbed]['traffic_generator']['details']['port'],
            "lanforge_2dot4g": CONFIGURATION[testbed]['traffic_generator']['details']['2.4G-Radio'][0],
            "lanforge_5g": CONFIGURATION[testbed]['traffic_generator']['details']['5G-Radio'][0],
            "lanforge_2dot4g_prefix": CONFIGURATION[testbed]['traffic_generator']['details']['2.4G-Station-Name'],
            "lanforge_5g_prefix": CONFIGURATION[testbed]['traffic_generator']['details']['5G-Station-Name'],
            "lanforge_2dot4g_station": CONFIGURATION[testbed]['traffic_generator']['details']['2.4G-Station-Name'],
            "lanforge_5g_station": CONFIGURATION[testbed]['traffic_generator']['details']['5G-Station-Name'],
            "lanforge_bridge_port": CONFIGURATION[testbed]['traffic_generator']['details']['upstream'],
            "lanforge_vlan_port": CONFIGURATION[testbed]['traffic_generator']['details']['upstream'] + ".100",
            "vlan": 100
        }
    yield lanforge_data


@pytest.fixture(scope="module")
def instantiate_profile(se):
    try:
        profile_object = ProfileUtility(sdk_client=instantiate_controller)
    except Exception as e:
        profile_object = False
    yield profile_object


@pytest.fixture(scope="session")
def instantiate_profile():
    yield ProfileUtility


@pytest.fixture(scope="session")
def setup_vlan():
    vlan_id = [100]
    allure.attach(body=str(vlan_id), name="VLAN Created: ")
    yield vlan_id[0]


@allure.feature("CLIENT CONNECTIVITY SETUP")
@pytest.fixture(scope="class")
def setup_profiles(request, setup_controller, testbed, setup_vlan, get_equipment_id,
                   instantiate_profile, get_markers,
                   get_security_flags, get_configuration, radius_info, get_apnos):
    instantiate_profile = instantiate_profile(sdk_client=setup_controller)
    vlan_id, mode = 0, 0
    instantiate_profile.cleanup_objects()
    parameter = dict(request.param)
    print(parameter)
    test_cases = {}
    profile_data = {}
    if parameter['mode'] not in ["BRIDGE", "NAT", "VLAN"]:
        print("Invalid Mode: ", parameter['mode'])
        allure.attach(body=parameter['mode'], name="Invalid Mode: ")
        yield test_cases

    if parameter['mode'] == "NAT":
        mode = "NAT"
        vlan_id = 1
    if parameter['mode'] == "BRIDGE":
        mode = "BRIDGE"
        vlan_id = 1
    if parameter['mode'] == "VLAN":
        mode = "BRIDGE"
        vlan_id = setup_vlan

    instantiate_profile.delete_profile_by_name(profile_name=testbed + "-Equipment-AP-" + parameter['mode'])

    profile_data["equipment_ap"] = {"profile_name": testbed + "-Equipment-AP-" + parameter['mode']}
    profile_data["ssid"] = {}
    for i in parameter["ssid_modes"]:
        profile_data["ssid"][i] = []
        for j in range(len(parameter["ssid_modes"][i])):
            profile_name = testbed + "-SSID-" + i + "-" + str(j) + "-" + parameter['mode']
            data = parameter["ssid_modes"][i][j]
            data["profile_name"] = profile_name
            if "mode" not in dict(data).keys():
                data["mode"] = mode
            if "vlan" not in dict(data).keys():
                data["vlan"] = vlan_id
            instantiate_profile.delete_profile_by_name(profile_name=profile_name)
            profile_data["ssid"][i].append(data)
    #         print(profile_name)
    # print(profile_data)

    instantiate_profile.delete_profile_by_name(profile_name=testbed + "-Automation-Radius-Profile-" + mode)
    time.sleep(10)
    """
      Setting up rf profile
    """
    rf_profile_data = {
        "name": "RF-Profile-" + testbed + "-" + parameter['mode'] + "-" +
                get_configuration['access_point'][0]['mode']
    }

    for i in parameter["rf"]:
        rf_profile_data[i] = parameter['rf'][i]
    # print(rf_profile_data)

    try:
        instantiate_profile.delete_profile_by_name(profile_name=rf_profile_data['name'])
        instantiate_profile.set_rf_profile(profile_data=rf_profile_data,
                                           mode=get_configuration['access_point'][0]['mode'])
        allure.attach(body=str(rf_profile_data),
                      name="RF Profile Created : " + get_configuration['access_point'][0]['mode'])
    except Exception as e:
        print(e)
        allure.attach(body=str(e), name="Exception ")

    # Radius Profile Creation
    if parameter["radius"]:
        radius_info = radius_info
        radius_info["name"] = testbed + "-Automation-Radius-Profile-" + testbed
        instantiate_profile.delete_profile_by_name(profile_name=testbed + "-Automation-Radius-Profile-" + testbed)
        try:
            # pass
            instantiate_profile.create_radius_profile(radius_info=radius_info)
            allure.attach(body=str(radius_info),
                          name="Radius Profile Created")
            test_cases['radius_profile'] = True
        except Exception as e:
            print(e)
            test_cases['radius_profile'] = False

    # SSID Profile Creation
    print(get_markers)
    for mode in profile_data['ssid']:
        if mode == "open":
            for j in profile_data["ssid"][mode]:
                # print(j)
                if mode in get_markers.keys() and get_markers[mode]:
                    try:
                        if "twog" in get_markers.keys() and get_markers["twog"] and "is2dot4GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_open_ssid_profile(profile_data=j)
                            test_cases["open_2g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["open_2g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")

                    try:
                        if "fiveg" in get_markers.keys() and get_markers["fiveg"] and "is5GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_open_ssid_profile(profile_data=j)
                            test_cases["open_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["open_5g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")

        if mode == "wpa":
            for j in profile_data["ssid"][mode]:
                # print(j)
                if mode in get_markers.keys() and get_markers[mode]:
                    try:
                        if "twog" in get_markers.keys() and get_markers["twog"] and "is2dot4GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa_ssid_profile(profile_data=j)
                            test_cases["wpa_2g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["wpa_2g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")
                    try:
                        if "fiveg" in get_markers.keys() and get_markers["fiveg"] and "is5GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa_ssid_profile(profile_data=j)
                            test_cases["wpa_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["wpa_5g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")
        if mode == "wpa2_personal":
            for j in profile_data["ssid"][mode]:
                # print(j)
                if mode in get_markers.keys() and get_markers[mode]:
                    try:
                        if "twog" in get_markers.keys() and get_markers["twog"] and "is2dot4GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa2_personal_ssid_profile(profile_data=j)
                            test_cases["wpa2_personal_2g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["wpa2_personal_2g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")
                    try:
                        if "fiveg" in get_markers.keys() and get_markers["fiveg"] and "is5GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa2_personal_ssid_profile(profile_data=j)
                            test_cases["wpa2_personal_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["wpa2_personal_5g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")

        if mode == "wpa_wpa2_personal_mixed":
            for j in profile_data["ssid"][mode]:
                # print(j)
                if mode in get_markers.keys() and get_markers[mode]:
                    try:
                        if "twog" in get_markers.keys() and get_markers["twog"] and "is2dot4GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa_wpa2_personal_mixed_ssid_profile(profile_data=j)
                            test_cases["wpa_wpa2_personal_mixed_2g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["wpa_wpa2_personal_mixed_2g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")
                    try:
                        if "fiveg" in get_markers.keys() and get_markers["fiveg"] and "is5GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa_wpa2_personal_mixed_ssid_profile(profile_data=j)
                            test_cases["wpa_wpa2_personal_mixed_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["wpa_wpa2_personal_mixed_5g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")
        if mode == "wpa3_personal":
            for j in profile_data["ssid"][mode]:
                print(j)
                if mode in get_markers.keys() and get_markers[mode]:
                    try:
                        if "twog" in get_markers.keys() and get_markers["twog"] and "is2dot4GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa3_personal_ssid_profile(profile_data=j)
                            test_cases["wpa3_personal_2g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["wpa3_personal_2g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")
                    try:
                        if "fiveg" in get_markers.keys() and get_markers["fiveg"] and "is5GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa3_personal_ssid_profile(profile_data=j)
                            test_cases["wpa3_personal_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["wpa3_personal_5g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")
        if mode == "wpa3_personal_mixed":
            for j in profile_data["ssid"][mode]:
                print(j)
                if mode in get_markers.keys() and get_markers[mode]:
                    try:
                        if "twog" in get_markers.keys() and get_markers["twog"] and "is2dot4GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa3_personal_mixed_ssid_profile(
                                profile_data=j)
                            test_cases["wpa3_personal_mixed_2g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["wpa3_personal_2g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")
                    try:
                        if "fiveg" in get_markers.keys() and get_markers["fiveg"] and "is5GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa3_personal_mixed_ssid_profile(
                                profile_data=j)
                            test_cases["wpa3_personal_mixed_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["wpa3_personal_5g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")

        if mode == "wpa2_enterprise":
            for j in profile_data["ssid"][mode]:
                # print(j)
                if mode in get_markers.keys() and get_markers[mode]:
                    try:
                        if "twog" in get_markers.keys() and get_markers["twog"] and "is2dot4GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa2_enterprise_ssid_profile(profile_data=j)
                            test_cases["wpa2_enterprise_2g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["wpa2_enterprise_2g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")
                    try:
                        if "fiveg" in get_markers.keys() and get_markers["fiveg"] and "is5GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa2_enterprise_ssid_profile(profile_data=j)
                            test_cases["wpa2_enterprise_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["wpa2_enterprise_5g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")

        if mode == "wpa3_enterprise":
            for j in profile_data["ssid"][mode]:
                # print(j)
                if mode in get_markers.keys() and get_markers[mode]:
                    try:
                        if "twog" in get_markers.keys() and get_markers["twog"] and "is2dot4GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa3_enterprise_ssid_profile(profile_data=j)
                            test_cases["wpa3_enterprise_2g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["wpa3_enterprise_2g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")
                    try:
                        if "fiveg" in get_markers.keys() and get_markers["fiveg"] and "is5GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa3_enterprise_ssid_profile(profile_data=j)
                            test_cases["wpa3_enterprise_5g"] = True
                            allure.attach(body=str(creates_profile),
                                          name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases["wpa3_enterprise_5g"] = False
                        allure.attach(body=str(e),
                                      name="SSID Profile Creation Failed")

    # Equipment AP Profile Creation
    try:
        instantiate_profile.set_ap_profile(profile_data=profile_data['equipment_ap'])
        test_cases["equipment_ap"] = True
        allure.attach(body=str(profile_data['equipment_ap']),
                      name="Equipment AP Profile Created")
    except Exception as e:
        print(e)
        test_cases["equipment_ap"] = False
        allure.attach(body=str(e),
                      name="Equipment AP Profile Creation Failed")

    # Push the Equipment AP Profile to AP
    try:
        for i in get_equipment_id:
            instantiate_profile.push_profile_old_method(equipment_id=i)
    except Exception as e:
        print(e)
        print("failed to create AP Profile")

    ap_ssh = get_apnos(get_configuration['access_point'][0], pwd="../libs/apnos/")
    ssid_names = []
    for i in instantiate_profile.profile_creation_ids["ssid"]:
        ssid_names.append(instantiate_profile.get_ssid_name_by_profile_id(profile_id=i))
    ssid_names.sort()


@pytest.fixture(scope="function")
def update_ssid(request, instantiate_profile, setup_profile_data):
    requested_profile = str(request.param).replace(" ", "").split(",")
    profile = setup_profile_data[requested_profile[0]][requested_profile[1]][requested_profile[2]]
    status = instantiate_profile.update_ssid_name(profile_name=profile["profile_name"],
                                                  new_profile_name=requested_profile[3])
    setup_profile_data[requested_profile[0]][requested_profile[1]][requested_profile[2]]["profile_name"] = \
        requested_profile[3]
    setup_profile_data[requested_profile[0]][requested_profile[1]][requested_profile[2]]["ssid_name"] = \
        requested_profile[3]
    time.sleep(90)
    yield status


@pytest.fixture(scope="package")
def create_lanforge_chamberview(create_lanforge_chamberview_dut, get_configuration, testbed):
    lanforge_data = get_configuration['traffic_generator']['details']
    ip = lanforge_data["ip"]
    port = lanforge_data["port"]
    upstream_port = lanforge_data["upstream"]  # eth1
    uplink_port = lanforge_data["uplink"]  # eth2
    upstream_subnet = lanforge_data["upstream_subnet"]
    scenario_name = "TIP-" + testbed
    upstream_res = upstream_port.split(".")[0] + "." + upstream_port.split(".")[1]
    uplink_res = uplink_port.split(".")[0] + "." + uplink_port.split(".")[1]
    print(ip)
    print(upstream_port, upstream_res, upstream_port.split(".")[2])
    # "profile_link 1.1 upstream-dhcp 1 NA NA eth2,AUTO -1 NA"
    # "profile_link 1.1 uplink-nat 1 'DUT: upstream LAN 10.28.2.1/24' NA eth1,eth2 -1 NA"
    raw_line = [
        ["profile_link " + upstream_res + " upstream-dhcp 1 NA NA " + upstream_port.split(".")[2] + ",AUTO -1 NA"]
        , ["profile_link " + uplink_res + " uplink-nat 1 'DUT: upstream LAN "
           + upstream_subnet + "' NA " + uplink_port.split(".")[2] + " -1 NA"]
    ]
    print(raw_line)
    Create_Chamberview = CreateChamberview(ip, port)
    Create_Chamberview.clean_cv_scenario()
    Create_Chamberview.clean_cv_scenario(type="Network-Connectivity", scenario_name=scenario_name)

    Create_Chamberview.setup(create_scenario=scenario_name,
                             raw_line=raw_line)

    Create_Chamberview.build(scenario_name)
    Create_Chamberview.show_text_blob(None, None, True)  # Show changes on GUI
    yield Create_Chamberview


@pytest.fixture(scope="package")
def create_lanforge_chamberview_dut(get_configuration, testbed):
    ap_model = get_configuration["access_point"][0]["model"]
    version = get_configuration["access_point"][0]["version"]
    serial = get_configuration["access_point"][0]["serial"]
    # ap_model = get_configuration["access_point"][0]["model"]
    lanforge_data = get_configuration['traffic_generator']['details']
    ip = lanforge_data["ip"]
    port = lanforge_data["port"]
    dut = DUT(lfmgr=ip,
              port=port,
              dut_name=testbed,
              sw_version=version,
              model_num=ap_model,
              serial_num=serial
              )
    dut.setup()
    yield dut


@pytest.fixture(scope="session")
def lf_test(get_configuration):
    obj = RunTest(lanforge_data=get_configuration['traffic_generator']['details'])
    yield obj


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
