import datetime
import sys
import os
import time
import warnings
from selenium.common.exceptions import NoSuchElementException
import urllib3
from perfecto.model.model import Job, Project
from perfecto import (PerfectoExecutionContext, PerfectoReportiumClient,TestContext, TestResultFactory)
import pytest
import logging


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

sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)
if "tests" not in sys.path:
    sys.path.append(f'../tests')

from configuration import CONFIGURATION

from urllib3 import exceptions



@pytest.fixture(scope="class")
def setup_perfectoMobileWeb(request):
    from selenium import webdriver
    driver = None
    reporting_client = None
    
    warnings.simplefilter("ignore", ResourceWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    capabilities = {
            'platformName': request.config.getini("platformName-iOS"),
            'model': request.config.getini("model-iOS"),
            'browserName': request.config.getini("browserType-iOS"),
            'securityToken' : request.config.getini("securityToken")
    }

    driver = webdriver.Remote('https://'+request.config.getini("perfectoURL")+'.perfectomobile.com/nexperience/perfectomobile/wd/hub', capabilities)
    driver.implicitly_wait(25)
   
    projectname = request.config.getini("projectName")
    projectversion = request.config.getini("projectVersion")
    jobname = request.config.getini("jobName")
    jobnumber = request.config.getini("jobNumber")
    tags = request.config.getini("reportTags")
    testCaseName = request.config.getini("jobName")

    print("Setting Perfecto ReportClient....")
    perfecto_execution_context = PerfectoExecutionContext(driver, tags, Job(jobname, jobnumber),Project(projectname, projectversion))
    reporting_client = PerfectoReportiumClient(perfecto_execution_context)
    reporting_client.test_start(testCaseName, TestContext([], "Raj"))

    if driver is None:
        yield -1
    else:
        yield driver,reporting_client 

    try:
        print(" -- Tear Down --")     
        reporting_client.test_stop(TestResultFactory.create_success())
        print('Report-Url: ' + reporting_client.report_url() + '\n')
        driver.close()
    except Exception as e:
        print(" -- Exception Not Able To close --")    
        print (e.message)
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(" -- Exception Not Able To Quit --")    
            print (e.message)

@pytest.fixture(scope="class")
def setup_perfectoMobile_iOS(request):
    from appium import webdriver
    driver = None
    reporting_client = None
    
    warnings.simplefilter("ignore", ResourceWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    capabilities = {
            'platformName': request.config.getini("platformName-iOS"),
            'model': request.config.getini("model-iOS"),
            'securityToken' : request.config.getini("securityToken"),
            'bundleId' : request.config.getini("bundleId-iOS"),
    }

    driver = webdriver.Remote('https://'+request.config.getini("perfectoURL")+'.perfectomobile.com/nexperience/perfectomobile/wd/hub', capabilities)
    driver.implicitly_wait(25)
   
    projectname = request.config.getini("projectName")
    projectversion = request.config.getini("projectVersion")
    jobname = request.config.getini("jobName")
    jobnumber = request.config.getini("jobNumber")
    tags = request.config.getini("reportTags")
    testCaseName = request.config.getini("jobName")

    print("Setting Perfecto ReportClient....")
    perfecto_execution_context = PerfectoExecutionContext(driver, tags, Job(jobname, jobnumber),Project(projectname, projectversion))
    reporting_client = PerfectoReportiumClient(perfecto_execution_context)
    reporting_client.test_start(testCaseName, TestContext([], "Raj"))

    if driver is None:
        yield -1
    else:
        yield driver,reporting_client 

    try:
        print(" -- Tear Down --")     
        reporting_client.test_stop(TestResultFactory.create_success())
        print('Report-Url: ' + reporting_client.report_url() + '\n')
        driver.close()
    except Exception as e:
        print(" -- Exception Not Able To close --")    
        print (e.message)
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(" -- Exception Not Able To Quit --")    
            print (e.message)

@pytest.fixture(scope="function")
def get_PassPointConniOS_data(request):
    passPoint_data = {
        "netAnalyzer-inter-Con-Xpath": "//*[@label='Network Connected']/parent::*/XCUIElementTypeButton",
        "bundleId-iOS-Settings": request.config.getini("bundleId-iOS-Settings"),
        "bundleId-iOS-Ping": request.config.getini("bundleId-iOS-Ping")
    }
    yield passPoint_data

@pytest.fixture(scope="function")
def get_APToMobileDevice_data(request):
    passPoint_data = {
        "webURL": "https://www.google.com",
        "lblSearch": "//*[@class='gLFyf']",
        "elelSearch": "(//*[@class='sbic sb43'])[1]",
        "BtnRunSpeedTest": "//*[text()='RUN SPEED TEST']",
        "downloadMbps": "//*[@id='knowledge-verticals-internetspeedtest__download']/P[@class='spiqle']",
        "UploadMbps": "//*[@id='knowledge-verticals-internetspeedtest__upload']/P[@class='spiqle']",
        "lblSearch2": "test "
    }
    yield passPoint_data

@pytest.fixture(scope="function")
def get_AccessPointConn_data(request):
    passPoint_data = {
        "bundleId-iOS-Settings": request.config.getini("bundleId-iOS-Settings"),
        "bundleId-iOS-Ping": request.config.getini("bundleId-iOS-Ping"),
        "Default-SSID-5gl-perfecto-b": request.config.getini("Default-SSID-5gl-perfecto-b"),
        "Default-SSID-2g-perfecto-b": request.config.getini("Default-SSID-2g-perfecto-b"),
        "Default-SSID-perfecto-b": request.config.getini("Default-SSID-perfecto-b")
        
    }
    yield passPoint_data

@pytest.fixture(scope="function")
def get_ToggleAirplaneMode_data(request):
    passPoint_data = {
        "bundleId-iOS-Settings": request.config.getini("bundleId-iOS-Settings"),
        "lblSearch": "//*[@class='gLFyf']",
        "elelSearch": "(//*[@class='sbic sb43'])[1]",
        "BtnRunSpeedTest": "//*[text()='RUN SPEED TEST']",
        "downloadMbps": "//*[@id='knowledge-verticals-internetspeedtest__download']/P[@class='spiqle']",
        "UploadMbps": "//*[@id='knowledge-verticals-internetspeedtest__upload']/P[@class='spiqle']",

    }
    yield passPoint_data

@pytest.fixture(scope="function")
def get_ToggleWifiMode_data(request):
    passPoint_data = {
        "bundleId-iOS-Settings": request.config.getini("bundleId-iOS-Settings"),
        "wifi-SSID-5gl-Pwd": request.config.getini("wifi-SSID-5gl-Pwd"),
        "wifi-SSID-2g-Pwd": request.config.getini("wifi-SSID-2g-Pwd")
    }
    yield passPoint_data




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
    #try:
    profile_object = ProfileUtility(sdk_client=instantiate_controller)
    #except:
    #profile_object = False
    yield profile_object


@pytest.fixture(scope="session")
def get_equipment_id(instantiate_controller, testbed):
    equipment_id = 0
    if len(CONFIGURATION[testbed]['access_point']) == 1:
        equipment_id = instantiate_controller.get_equipment_id(
            serial_number=CONFIGURATION[testbed]['access_point'][0]['serial'])
    yield equipment_id


@pytest.fixture(scope="session")
def upload_firmware(should_upload_firmware, instantiate_firmware, get_latest_firmware):
    firmware_id = instantiate_firmware.upload_fw_on_cloud(fw_version=get_latest_firmware,
                                                          force_upload=should_upload_firmware)
    yield firmware_id


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
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
    except:
        print("failed to create AP Profile")
    ap_ssh = APNOS(CONFIGURATION[testbed]['access_point'][0])
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
    ap_ssh = APNOS(CONFIGURATION[testbed]['access_point'][0])
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
    yield test_cases


@pytest.fixture(scope="module")
def create_profiles(request, get_security_flags, get_markers, instantiate_profile, setup_profile_data):
    profile_id = {"ssid": [], "rf": None, "radius": None, "equipment_ap": None}
    mode = str(request.param[0])
    test_cases = {}
    if mode not in ["BRIDGE", "NAT", "VLAN"]:
        print("Invalid Mode: ", mode)
        yield False
    instantiate_profile.delete_profile_by_name(profile_name="Equipment-AP-" + mode)
    for i in setup_profile_data[mode]:
        for j in setup_profile_data[mode][i]:
            instantiate_profile.delete_profile_by_name(
                profile_name=setup_profile_data[mode][i][j]['profile_name'])
    instantiate_profile.delete_profile_by_name(profile_name="Automation-Radius-Profile-" + mode)
    instantiate_profile.get_default_profiles()
    # if get_markers["wifi5"]:
    #     # Create RF Profile
    #     pass
    # if get_markers["wifi6"]:
    #     # Create RF Profile
    #     pass

    # Create RF Profile Here
    instantiate_profile.set_rf_profile()
    if get_markers["radius"]:
        radius_info = RADIUS_SERVER_DATA
        radius_info["name"] = "Automation-Radius-Profile-" + mode
        try:
            instantiate_profile.create_radius_profile(radius_info=radius_info)
            test_cases['radius_profile'] = True
        except:
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
                except:
                    test_cases['ssid_2g_open_' + mode.lower()] = False
            if get_markers["fiveg"]:
                profile_data = setup_profile_data[mode]["OPEN"]["5G"]
                try:
                    id = instantiate_profile.create_open_ssid_profile(two4g=False, fiveg=True,
                                                                      profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_5g_open_' + mode.lower()] = True
                except:
                    test_cases['ssid_5g_open_' + mode.lower()] = False
        if get_markers[i] and i == "wpa":
            if get_markers["twog"]:
                profile_data = setup_profile_data[mode]["WPA"]["2G"]
                try:
                    id = instantiate_profile.create_wpa_ssid_profile(two4g=True, fiveg=False, profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_2g_wpa_' + mode.lower()] = True
                except:
                    test_cases['ssid_5g_wpa_' + mode.lower()] = False
            if get_markers["fiveg"]:
                profile_data = setup_profile_data[mode]["WPA"]["5G"]
                try:
                    id = instantiate_profile.create_wpa_ssid_profile(two4g=False, fiveg=True, profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_5g_wpa_' + mode.lower()] = True
                except:
                    test_cases['ssid_5g_wpa_' + mode.lower()] = False
        if get_markers[i] and i == "wpa2_personal":
            if get_markers["twog"]:
                profile_data = setup_profile_data[mode]["WPA2_P"]["2G"]
                try:
                    id = instantiate_profile.create_wpa2_personal_ssid_profile(two4g=True, fiveg=False,
                                                                               profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_2g_wpa2_' + mode.lower()] = True
                except:
                    test_cases['ssid_2g_wpa2_' + mode.lower()] = False
            if get_markers["fiveg"]:
                profile_data = setup_profile_data[mode]["WPA2_P"]["5G"]
                try:
                    id = instantiate_profile.create_wpa2_personal_ssid_profile(two4g=False, fiveg=True,
                                                                               profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_5g_wpa2_' + mode.lower()] = True
                except:
                    test_cases['ssid_5g_wpa2_' + mode.lower()] = False
        if get_markers[i] and i == "wpa2_enterprise":
            if get_markers["twog"]:
                profile_data = setup_profile_data[mode]["WPA2_E"]["2G"]
                try:
                    id = instantiate_profile.create_wpa2_enterprise_ssid_profile(two4g=True, fiveg=False,
                                                                                 profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_2g_eap_' + mode.lower()] = True
                except:
                    test_cases['ssid_2g_eap_' + mode.lower()] = False
            if get_markers["fiveg"]:
                profile_data = setup_profile_data[mode]["WPA2_E"]["5G"]
                try:
                    id = instantiate_profile.create_wpa2_enterprise_ssid_profile(two4g=False, fiveg=True,
                                                                                 profile_data=profile_data)
                    profile_id["ssid"].append(profile_data['ssid_name'])
                    test_cases['ssid_5g_eap_' + mode.lower()] = True
                except:
                    test_cases['ssid_5g_eap_' + mode.lower()] = False

    # Create Equipment AP Profile Here
    profile_data = {
        "profile_name": "Equipment-AP-" + mode
    }
    try:
        instantiate_profile.set_ap_profile(profile_data=profile_data)
        test_cases['ap_' + mode.lower()] = True
    except:
        test_cases['ap_' + mode.lower()] = False
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
