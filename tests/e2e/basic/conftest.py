"""
conftest.py : Contains fixtures that are specific to basic testbed environment

Basic Test Scenario : 1 AP, 1 LANforge, 1 Controller Instance

Includes:

    Setup:
        setup_profiles
        create_profiles

    Utilities:
        update_ssid

Information:
    Setup Fixtures: Every Test case Needs to use setup fixtures
                    Setup Fixtures can be customised for all different levels of execution:
                        session level
                        package level
                        module level
                        class level
                        function level

"""

import sys
import os
import time

sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)
if "libs" not in sys.path:
    sys.path.append(f'../libs')

from apnos.apnos import APNOS
from controller.controller import Controller
from controller.controller import ProfileUtility
from controller.controller import FirmwareUtility
import pytest
import logging
from configuration import RADIUS_SERVER_DATA
from configuration import TEST_CASES
from configuration import CONFIGURATION
from configuration import FIRMWARE
from testrails.testrail_api import APIClient
from testrails.reporting import Reporting

"""
Basic Setup Collector
"""


@pytest.fixture(scope="function")
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
def instantiate_profile(instantiate_controller):
    try:
        profile_object = ProfileUtility(sdk_client=instantiate_controller)
    except Exception as e:
        profile_object = False
    yield profile_object


@pytest.fixture(scope="session")
def get_equipment_id(instantiate_controller, testbed):
    equipment_id = 0
    if len(CONFIGURATION[testbed]['access_point']) == 1:
        equipment_id = instantiate_controller.get_equipment_id(
            serial_number=CONFIGURATION[testbed]['access_point'][0]['serial'])
    print(equipment_id)
    yield equipment_id


@pytest.fixture(scope="session")
def upload_firmware(should_upload_firmware, instantiate_firmware, get_latest_firmware):
    firmware_id = instantiate_firmware.upload_fw_on_cloud(fw_version=get_latest_firmware,
                                                          force_upload=should_upload_firmware)
    yield firmware_id


@pytest.fixture(scope="function")
def upgrade_firmware(request, instantiate_firmware, get_equipment_id, check_ap_firmware_cloud, get_latest_firmware,
                     should_upgrade_firmware):
    if get_latest_firmware != check_ap_firmware_cloud:
        if request.config.getoption("--skip-upgrade"):
            status = "skip-upgrade"
        else:
            status = instantiate_firmware.upgrade_fw(equipment_id=get_equipment_id, force_upload=False,
                                                     force_upgrade=should_upgrade_firmware)
    else:
        if should_upgrade_firmware:
            status = instantiate_firmware.upgrade_fw(equipment_id=get_equipment_id, force_upload=False,
                                                     force_upgrade=should_upgrade_firmware)
        else:
            status = "skip-upgrade"
    yield status


@pytest.fixture(scope="function")
def check_ap_firmware_cloud(instantiate_controller, get_equipment_id):
    yield instantiate_controller.get_ap_firmware_old_method(equipment_id=get_equipment_id)


"""

Profiles Related Fixtures

"""


@pytest.fixture(scope="module")
def get_current_profile_cloud(instantiate_profile):
    ssid_names = []
    for i in instantiate_profile.profile_creation_ids["ssid"]:
        ssid_names.append(instantiate_profile.get_ssid_name_by_profile_id(profile_id=i))
    yield ssid_names


@pytest.fixture(scope="module")
def setup_profiles(request, create_profiles, instantiate_profile, get_equipment_id, get_current_profile_cloud, testbed):
    test_cases = {}
    mode = str(request.param[0]).lower()
    try:
        instantiate_profile.push_profile_old_method(equipment_id=get_equipment_id)
    except Exception as e:
        print(e)
        print("failed to Push Profile")
    ap_ssh = APNOS(CONFIGURATION[testbed]['access_point'][0], pwd="../libs/apnos/")
    get_current_profile_cloud.sort()
    # This loop will check the VIF Config with cloud profile
    for i in range(0, 18):
        vif_config = list(ap_ssh.get_vif_config_ssids())
        vif_config.sort()
        print(vif_config)
        print(get_current_profile_cloud)
        if get_current_profile_cloud == vif_config:
            test_cases[mode + '_vifc'] = True
            break
        time.sleep(10)
    ap_ssh = APNOS(CONFIGURATION[testbed]['access_point'][0], pwd="../libs/apnos/")
    # This loop will check the VIF Config with VIF State
    for i in range(0, 18):
        vif_state = list(ap_ssh.get_vif_state_ssids())
        vif_state.sort()
        vif_config = list(ap_ssh.get_vif_config_ssids())
        vif_config.sort()
        print(vif_config)
        print(vif_state)
        if vif_state == vif_config:
            test_cases[mode + '_vifs'] = True
            break
        time.sleep(10)
        #
    yield test_cases


@pytest.fixture(scope="module")
def create_profiles(request, testbed, get_security_flags, get_markers, instantiate_profile, setup_profile_data):
    profile_id = {"ssid": [], "rf": None, "radius": None, "equipment_ap": None}
    mode = str(request.param[0])
    test_cases = {}
    if mode not in ["BRIDGE", "NAT", "VLAN"]:
        print("Invalid Mode: ", mode)
        yield False
    instantiate_profile.delete_profile_by_name(profile_name=testbed + "-Equipment-AP-" + mode)
    for i in setup_profile_data[mode]:
        for j in setup_profile_data[mode][i]:
            instantiate_profile.delete_profile_by_name(
                profile_name=setup_profile_data[mode][i][j]['profile_name'])
    instantiate_profile.delete_profile_by_name(profile_name=testbed + "-Automation-Radius-Profile-" + mode)
    instantiate_profile.get_default_profiles()
    profile_data = {
        "name": "RF-Profile-" + CONFIGURATION[testbed]['access_point'][0]['mode'] +
                CONFIGURATION[testbed]['access_point'][0]['model'] + "_" + mode + "_" + testbed
    }
    instantiate_profile.delete_profile_by_name(profile_name=profile_data['name'])
    instantiate_profile.set_rf_profile(profile_data=profile_data,
                                       mode=CONFIGURATION[testbed]['access_point'][0]['mode'])
    # Create RF Profile Here
    if get_markers["radius"]:
        radius_info = RADIUS_SERVER_DATA
        radius_info["name"] = testbed + "-Automation-Radius-Profile-" + mode
        try:
            instantiate_profile.create_radius_profile(radius_info=radius_info)
            test_cases['radius_profile'] = True
        except Exception as e:
            test_cases['radius_profile'] = False
    for i in get_security_flags:
        if get_markers[i] and i == "open":
            if get_markers["twog"]:
                profile_data = setup_profile_data[mode]["OPEN"]["2G"]
                try:
                    id = instantiate_profile.create_open_ssid_profile(two4g=True, fiveg=False,
                                                                      profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_2g_open_' + mode.lower()] = True
                except Exception as e:
                    test_cases['ssid_2g_open_' + mode.lower()] = False
            if get_markers["fiveg"]:
                profile_data = setup_profile_data[mode]["OPEN"]["5G"]
                try:
                    id = instantiate_profile.create_open_ssid_profile(two4g=False, fiveg=True,
                                                                      profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_5g_open_' + mode.lower()] = True
                except Exception as e:
                    test_cases['ssid_5g_open_' + mode.lower()] = False
        if get_markers[i] and i == "wpa":
            if get_markers["twog"]:
                profile_data = setup_profile_data[mode]["WPA"]["2G"]
                try:
                    id = instantiate_profile.create_wpa_ssid_profile(two4g=True, fiveg=False, profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_2g_wpa_' + mode.lower()] = True
                except Exception as e:
                    test_cases['ssid_5g_wpa_' + mode.lower()] = False
            if get_markers["fiveg"]:
                profile_data = setup_profile_data[mode]["WPA"]["5G"]
                try:
                    id = instantiate_profile.create_wpa_ssid_profile(two4g=False, fiveg=True, profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_5g_wpa_' + mode.lower()] = True
                except Exception as e:
                    test_cases['ssid_5g_wpa_' + mode.lower()] = False
        if get_markers[i] and i == "wpa2_personal":
            if get_markers["twog"]:
                profile_data = setup_profile_data[mode]["WPA2_P"]["2G"]
                try:
                    id = instantiate_profile.create_wpa2_personal_ssid_profile(two4g=True, fiveg=False,
                                                                               profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_2g_wpa2_' + mode.lower()] = True
                except Exception as e:
                    test_cases['ssid_2g_wpa2_' + mode.lower()] = False
            if get_markers["fiveg"]:
                profile_data = setup_profile_data[mode]["WPA2_P"]["5G"]
                try:
                    id = instantiate_profile.create_wpa2_personal_ssid_profile(two4g=False, fiveg=True,
                                                                               profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_5g_wpa2_' + mode.lower()] = True
                except Exception as e:
                    test_cases['ssid_5g_wpa2_' + mode.lower()] = False
        if get_markers[i] and i == "wpa2_enterprise":
            if get_markers["twog"]:
                profile_data = setup_profile_data[mode]["WPA2_E"]["2G"]
                try:
                    id = instantiate_profile.create_wpa2_enterprise_ssid_profile(two4g=True, fiveg=False,
                                                                                 profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_2g_eap_' + mode.lower()] = True
                except Exception as e:
                    test_cases['ssid_2g_eap_' + mode.lower()] = False
            if get_markers["fiveg"]:
                profile_data = setup_profile_data[mode]["WPA2_E"]["5G"]
                try:
                    id = instantiate_profile.create_wpa2_enterprise_ssid_profile(two4g=False, fiveg=True,
                                                                                 profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_5g_eap_' + mode.lower()] = True
                except Exception as e:
                    test_cases['ssid_5g_eap_' + mode.lower()] = False

    # Create Equipment AP Profile Here
    profile_data = {
        "profile_name": testbed + "-Equipment-AP-" + mode
    }
    try:
        instantiate_profile.set_ap_profile(profile_data=profile_data)
        test_cases['ap_' + mode.lower()] = True
    except Exception as e:
        print(e)
        test_cases['ap_' + mode.lower()] = False

    def teardown_profiles():
        print("\nRemoving Profiles")
        instantiate_profile.delete_profile_by_name(profile_name=profile_data['profile_name'])
        time.sleep(20)

    request.addfinalizer(teardown_profiles)
    yield test_cases


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

