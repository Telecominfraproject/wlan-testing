import os
import sys

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
import allure


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

    # This loop will check the VIF Config with cloud profile
    vif_config = []
    test_cases['vifc'] = False
    for i in range(0, 18):
        vif_config = list(ap_ssh.get_vif_config_ssids())
        vif_config.sort()
        print(vif_config)
        print(ssid_names)
        if ssid_names == vif_config:
            test_cases['vifc'] = True
            break
        time.sleep(10)
    allure.attach(body=str("VIF Config: " + str(vif_config) + "\n" + "SSID Pushed from Controller: " + str(ssid_names)),
                  name="SSID Profiles in VIF Config and Controller: ")
    ap_ssh = get_apnos(get_configuration['access_point'][0], pwd="../libs/apnos/")

    # This loop will check the VIF Config with VIF State
    test_cases['vifs'] = False
    for i in range(0, 18):
        vif_state = list(ap_ssh.get_vif_state_ssids())
        vif_state.sort()
        vif_config = list(ap_ssh.get_vif_config_ssids())
        vif_config.sort()
        print(vif_config)
        print(vif_state)
        if vif_state == vif_config:
            test_cases['vifs'] = True
            break
        time.sleep(10)
    allure.attach(body=str("VIF Config: " + str(vif_config) + "\n" + "VIF State: " + str(vif_state)),
                  name="SSID Profiles in VIF Config and VIF State: ")
    print(test_cases)

    def teardown_session():
        print("\nRemoving Profiles")
        instantiate_profile.delete_profile_by_name(profile_name=profile_data['equipment_ap']['profile_name'])
        instantiate_profile.delete_profile(instantiate_profile.profile_creation_ids["ssid"])
        instantiate_profile.delete_profile(instantiate_profile.profile_creation_ids["radius"])
        instantiate_profile.delete_profile(instantiate_profile.profile_creation_ids["rf"])
        allure.attach(body=str(profile_data['equipment_ap']['profile_name'] + "\n"),
                      name="Tear Down in Profiles ")
        time.sleep(20)

    request.addfinalizer(teardown_session)
    yield test_cases


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
