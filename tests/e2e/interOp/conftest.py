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
import re

sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)
if "libs" not in sys.path:
    sys.path.append(f'../libs')
import allure
from apnos.apnos import APNOS
from controller.controller import Controller
from controller.controller import ProfileUtility
from controller.controller import FirmwareUtility
import pytest
import logging
from configuration import RADIUS_SERVER_DATA

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
    rdriver = None
    reporting_client = None
    
    warnings.simplefilter("ignore", ResourceWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    capabilities = {
            'platformName': request.config.getini("platformName-iOS"),
            'model': request.config.getini("model-iOS"),
            'browserName': request.config.getini("browserType-iOS"),
            'securityToken' : request.config.getini("securityToken"),
    }

    rdriver = webdriver.Remote('https://'+request.config.getini("perfectoURL")+'.perfectomobile.com/nexperience/perfectomobile/wd/hub', capabilities)
    rdriver.implicitly_wait(35)

    projectname = request.config.getini("projectName")
    projectversion = request.config.getini("projectVersion")
    jobname = request.config.getini("jobName")
    jobnumber = request.config.getini("jobNumber")
    tags = request.config.getini("reportTags")
    testCaseName = request.config.getini("jobName")

    print("Setting Perfecto ReportClient....")
    perfecto_execution_context = PerfectoExecutionContext(rdriver, tags, Job(jobname, jobnumber),Project(projectname, projectversion))
    reporting_client = PerfectoReportiumClient(perfecto_execution_context)
    reporting_client.test_start(testCaseName, TestContext([], "Perforce"))

    def teardown():
        try:
            print(" -- Tear Down --")     
            reporting_client.test_stop(TestResultFactory.create_success())
            print('Report-Url: ' + reporting_client.report_url() + '\n')
            rdriver.close()
        except Exception as e:
            print(" -- Exception Not Able To close --")    
            print (e.message)
        finally:
            try:
                rdriver.quit()
            except Exception as e:
                print(" -- Exception Not Able To Quit --")    
                print (e.message)

    request.addfinalizer(teardown)

    if rdriver is None:
        yield -1
    else:
        yield rdriver,reporting_client 


@pytest.fixture(scope="function")
def setup_perfectoMobile_iOS(request):
    from appium import webdriver
    driver = None
    reporting_client = None
    
    warnings.simplefilter("ignore", ResourceWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
   
    capabilities = {
            'platformName': request.config.getini("platformName-iOS"),
            'model': request.config.getini("model-iOS"),
            'browserName': 'safari',
            #'automationName' : 'Appium',
            'securityToken' : request.config.getini("securityToken"),  
            'useAppiumForWeb' : 'false', 
            'autoAcceptAlerts' : 'true',
            #'bundleId' : request.config.getini("bundleId-iOS"),
            'useAppiumForHybrid' : 'false',
    }

    driver = webdriver.Remote('https://'+request.config.getini("perfectoURL")+'.perfectomobile.com/nexperience/perfectomobile/wd/hub', capabilities)
    driver.implicitly_wait(35)
   
    TestCaseFullName = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
    nCurrentTestMethodNameSplit = re.sub(r'\[.*?\]\ *', "", TestCaseFullName)
    try:
        TestCaseName = nCurrentTestMethodNameSplit.removeprefix('test_')
        print ("\nTestCaseName: " + TestCaseName)
    except Exception as e:
        TestCaseName = nCurrentTestMethodNameSplit
        print("\nUpgrade Python to 3.9 to avoid test_ string in your test case name, see below URL")
        print("https://www.andreagrandi.it/2020/10/11/python39-introduces-removeprefix-removesuffix/")
        
    projectname = request.config.getini("projectName")
    projectversion = request.config.getini("projectVersion")
    jobname = request.config.getini("jobName")
    jobnumber = request.config.getini("jobNumber")
    tags = request.config.getini("reportTags")
    testCaseName = TestCaseName

    print("\nSetting Perfecto ReportClient....")
    perfecto_execution_context = PerfectoExecutionContext(driver, tags, Job(jobname, jobnumber),Project(projectname, projectversion))
    reporting_client = PerfectoReportiumClient(perfecto_execution_context)
    reporting_client.test_start(testCaseName, TestContext([], "Perforce"))

    def teardown():
        try:
            print("\n\n---------- Tear Down ----------")

            testFailed = request.session.testsfailed
            if testFailed>0:
                print ("Test Case Failure, please check report link: " + testCaseName)
                reporting_client.test_stop(TestResultFactory.create_failure(request.config.cache.get("SelectingWifiFailed", None)))
                request.config.cache.set(key="SelectingWifiFailed", value="Cache Cleared!!")
                #seen = {None}
                #session = request.node
                #print(session)
            elif testFailed<=0:
                reporting_client.test_stop(TestResultFactory.create_success())
                
            #amount = len(request.session.items)
            #print("Test Session Items: ")
            #print(amount)

            #tests_count = request.session.testscollected
            #print("Test Collected: ")
            #print(tests_count)

            print('Report-Url: ' + reporting_client.report_url())
            print("----------------------------------------------------------")
            driver.close()
        except Exception as e:
            print(" -- Exception While Tear Down --")    
            reporting_client.test_stop(TestResultFactory.create_failure("Exception"))
            print('Report-Url-Failure: ' + reporting_client.report_url() + '\n')
            
            driver.close()
           
            print (e)
        finally:
            try:
                driver.quit()
            except Exception as e:
                print(" -- Exception Not Able To Quit --")    
                print (e)
    

    request.addfinalizer(teardown)

    if driver is None:
        yield -1
    else:
        yield driver,reporting_client 


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
        "bundleId-iOS-Settings": request.config.getini("bundleId-iOS-Settings"),
        "bundleId-iOS-Safari": request.config.getini("bundleId-iOS-Safari"),
        "downloadMbps": "//*[@id='knowledge-verticals-internetspeedtest__download']/P[@class='spiqle']",
        "UploadMbps": "//*[@id='knowledge-verticals-internetspeedtest__upload']/P[@class='spiqle']",
        "openRoaming-iOS-URL": request.config.getini("openRoaming-iOS-URL"),
        #Android
        "platformName-android": request.config.getini("platformName-android"),
        "openRoaming-and-URL": request.config.getini("openRoaming-and-URL"),
        "appPackage-android": request.config.getini("appPackage-android")      
    }
    yield passPoint_data

@pytest.fixture(scope="function")
def get_AccessPointConn_data(request):
    passPoint_data = {
        "bundleId-iOS-Settings": request.config.getini("bundleId-iOS-Settings"),
        "bundleId-iOS-Ping": request.config.getini("bundleId-iOS-Ping")
    }
    yield passPoint_data

@pytest.fixture(scope="function")
def get_ToggleAirplaneMode_data(request):
    passPoint_data = {
        "webURL": "https://www.google.com",
        "lblSearch": "//*[@class='gLFyf']",
        "elelSearch": "(//*[@class='sbic sb43'])[1]",
        "BtnRunSpeedTest": "//*[text()='RUN SPEED TEST']",
        "bundleId-iOS-Settings": request.config.getini("bundleId-iOS-Settings"),
        "bundleId-iOS-Safari": request.config.getini("bundleId-iOS-Safari"),
        "downloadMbps": "//*[@id='knowledge-verticals-internetspeedtest__download']/P[@class='spiqle']",
        "UploadMbps": "//*[@id='knowledge-verticals-internetspeedtest__upload']/P[@class='spiqle']",
        #Android
        "platformName-android": request.config.getini("platformName-android"),
        "appPackage-android": request.config.getini("appPackage-android")      
    }
    yield passPoint_data

@pytest.fixture(scope="function")
def get_ToggleWifiMode_data(request):
    passPoint_data = {
        #iOS
        "bundleId-iOS-Settings": request.config.getini("bundleId-iOS-Settings"),
         #Android
        "platformName-android": request.config.getini("platformName-android"),
        "appPackage-android": request.config.getini("appPackage-android")      
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


@pytest.fixture(scope="session")
def instantiate_profile():
    yield ProfileUtility

@pytest.fixture(scope="session")
def get_equipment_id(setup_controller, testbed, get_configuration):
    equipment_id_list = []
    for i in get_configuration['access_point']:
        equipment_id_list.append(setup_controller.get_equipment_id(
            serial_number=i['serial']))
    yield equipment_id_list

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
def check_ap_firmware_cloud(setup_controller, get_equipment_id):
    yield setup_controller.get_ap_firmware_old_method(equipment_id=get_equipment_id)


"""

Profiles Related Fixtures

"""


@pytest.fixture(scope="module")
def get_current_profile_cloud(instantiate_profile):
    ssid_names = []
    for i in instantiate_profile.profile_creation_ids["ssid"]:
        ssid_names.append(instantiate_profile.get_ssid_name_by_profile_id(profile_id=i))
    yield ssid_names


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


#@pytest.fixture(scope="module", autouse=True)
def failure_tracking_fixture(request):
    tests_failed_before_module = request.session.testsfailed
    print("\n\ntests_failed_before_module: ")
    print(tests_failed_before_module)
    tests_failed_during_module = request.session.testsfailed - tests_failed_before_module
    print("tests_failed_during_module: ")
    print(tests_failed_during_module)
    yield tests_failed_during_module
    