import datetime
import sys
import os
import time
import warnings
from selenium.common.exceptions import NoSuchElementException
import urllib3
from perfecto.model.model import Job, Project
from perfecto import (PerfectoExecutionContext, PerfectoReportiumClient, TestContext, TestResultFactory)
import pytest
import logging
import re
import allure
import requests
from xml.etree import ElementTree as ET
from time import gmtime, strftime

sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)
if "libs" not in sys.path:
    sys.path.append(f'../libs')
import allure
from apnos.apnos import APNOS
from controller.controller_1x.controller import Controller
from controller.controller_1x.controller import ProfileUtility
from controller.controller_2x.controller import UProfileUtility
from controller.controller_1x.controller import FirmwareUtility
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
from configuration import PERFECTO_DETAILS

from urllib3 import exceptions

reporting_client = None
testCaseNameList = []
testCaseStatusList = []
testCaseErrorMsg = []
testCaseReportURL = []


@pytest.fixture(scope="function")
def get_PassPointConniOS_data(request, get_device_configuration):
    passPoint_data = {
        "netAnalyzer-inter-Con-Xpath": "//*[@label='Network Connected']/parent::*/XCUIElementTypeButton",
        "bundleId-iOS-Settings": get_device_configuration["bundleId-iOS-Settings"],
        "bundleId-iOS-Ping": get_device_configuration["bundleId-iOS-Ping"]
    }
    yield passPoint_data


@pytest.fixture(scope="function")
def get_APToMobileDevice_data(request, get_device_configuration):
    passPoint_data = {
        "webURL": "https://www.google.com",
        "lblSearch": "//*[@class='gLFyf']",
        "elelSearch": "(//*[@class='sbic sb43'])[1]",
        "BtnRunSpeedTest": "//*[text()='RUN SPEED TEST']",
        "bundleId-iOS-Settings": get_device_configuration["bundleId-iOS-Settings"],
        "bundleId-iOS-Safari": get_device_configuration["bundleId-iOS-Safari"],
        "downloadMbps": "//*[@id='knowledge-verticals-internetspeedtest__download']/P[@class='spiqle']",
        "UploadMbps": "//*[@id='knowledge-verticals-internetspeedtest__upload']/P[@class='spiqle']",
        # Android
        "platformName-android": get_device_configuration["platformName-android"],
        "appPackage-android": get_device_configuration["appPackage-android"]
    }
    yield passPoint_data


@pytest.fixture(scope="function")
def get_AccessPointConn_data(request, get_device_configuration):
    passPoint_data = {
        "bundleId-iOS-Settings": get_device_configuration["bundleId-iOS-Settings"],
        "bundleId-iOS-Ping": get_device_configuration["bundleId-iOS-Ping"]
    }
    yield passPoint_data


@pytest.fixture(scope="function")
def get_ToggleAirplaneMode_data(request, get_device_configuration):
    passPoint_data = {
        "webURL": "https://www.google.com",
        "lblSearch": "//*[@class='gLFyf']",
        "elelSearch": "(//*[@class='sbic sb43'])[1]",
        "BtnRunSpeedTest": "//*[text()='RUN SPEED TEST']",
        "bundleId-iOS-Settings": get_device_configuration["bundleId-iOS-Settings"],
        "bundleId-iOS-Safari": get_device_configuration["bundleId-iOS-Safari"],
        "downloadMbps": "//*[@id='knowledge-verticals-internetspeedtest__download']/P[@class='spiqle']",
        "UploadMbps": "//*[@id='knowledge-verticals-internetspeedtest__upload']/P[@class='spiqle']",
        # Android
        "platformName-android": get_device_configuration["platformName-android"],
        "appPackage-android": get_device_configuration["appPackage-android"]
    }
    yield passPoint_data


@pytest.fixture(scope="function")
def get_ToggleWifiMode_data(request,get_device_configuration):
    passPoint_data = {
        # iOS
        "bundleId-iOS-Settings": get_device_configuration["bundleId-iOS-Settings"],
        # Android
        "platformName-android": get_device_configuration["platformName-android"],
        "appPackage-android": get_device_configuration["appPackage-android"]
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
def instantiate_profile(request):
    if request.config.getoption("1.x"):
        yield ProfileUtility
    else:
        yield UProfileUtility



@pytest.fixture(scope="session")
def upload_firmware(should_upload_firmware, instantiate_firmware, get_latest_firmware):
    firmware_id = instantiate_firmware.upload_fw_on_cloud(fw_version=get_latest_firmware,
                                                          force_upload=should_upload_firmware)
    yield firmware_id


@pytest.fixture(scope="session")
def upgrade_firmware(request, instantiate_firmware, get_equipment_ref, check_ap_firmware_cloud, get_latest_firmware,
                     should_upgrade_firmware):
    if get_latest_firmware != check_ap_firmware_cloud:
        if request.config.getoption("--skip-upgrade"):
            status = "skip-upgrade"
        else:
            status = instantiate_firmware.upgrade_fw(equipment_id=get_equipment_ref, force_upload=False,
                                                     force_upgrade=should_upgrade_firmware)
    else:
        if should_upgrade_firmware:
            status = instantiate_firmware.upgrade_fw(equipment_id=get_equipment_ref, force_upload=False,
                                                     force_upgrade=should_upgrade_firmware)
        else:
            status = "skip-upgrade"
    yield status


@pytest.fixture(scope="session")
def check_ap_firmware_cloud(setup_controller, get_equipment_ref):
    yield setup_controller.get_ap_firmware_old_method(equipment_id=get_equipment_ref)


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
    yield vlan_id[0]


@pytest.fixture(scope="class")
def setup_profiles(request, setup_controller, testbed, get_equipment_ref, fixtures_ver, skip_lf, get_openflow, run_lf,
                   instantiate_profile, get_markers, create_lanforge_chamberview_dut, lf_tools,
                   get_security_flags, get_configuration, radius_info, get_apnos, radius_accounting_info):

    param = dict(request.param)
    if not skip_lf:
        lf_tools.reset_scenario()
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
                                             radius_accounting_info, skip_lf=skip_lf, open_flow=get_openflow, run_lf=run_lf)
    print("sleeping for 120 sec.")
    time.sleep(180)
    print("Done sleeping")
    yield return_var


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


# @pytest.fixture(scope="module", autouse=True)
def failure_tracking_fixture(request):
    tests_failed_before_module = request.session.testsfailed
    print("\n\ntests_failed_before_module: ")
    print(tests_failed_before_module)
    tests_failed_during_module = request.session.testsfailed - tests_failed_before_module
    print("tests_failed_during_module: ")
    print(tests_failed_during_module)
    yield tests_failed_during_module



empty_get_vif_state_list = []

@pytest.fixture(scope="class")
def get_vif_state(get_apnos, get_configuration, request, lf_tools, skip_lf):
    if not skip_lf:
        if request.config.getoption("1.x"):
            ap_ssh = get_apnos(get_configuration['access_point'][0], pwd="../libs/apnos/", sdk="1.x")
            vif_state = list(ap_ssh.get_vif_state_ssids())
            vif_state.sort()
            yield vif_state
        else:
            yield lf_tools.ssid_list
    else:
        yield empty_get_vif_state_list

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    # testCaseStatusValue = ""
    testCasePassedStatusValue = ""
    testCaseFailedStatusValue = ""
    testCaseNameList = []
    testCaseStatusList = []
    testCaseErrorMsg = []
    testCaseReportURL = []

    if os.environ.get('PYTEST_CURRENT_TEST') is not None:
        if (str(os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]).strip()).startswith("test_unique"):
            return 0

    # if os.environ.get('PYTEST_CURRENT_TEST') is not None and ((os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]).strip()).startswith("test_unique_ssid"):
    #     return 0;

    if result.when == 'call':
        item.session.results[item] = result

        # Gets the Current Test Case Name
        TestCaseFullName = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
        nCurrentTestMethodNameSplit = re.sub(r'\[.*?\]\ *', "", TestCaseFullName)
        # print("TestCasefullNameTEST: " + TestCaseFullName)
        try:
            # TestCaseName = nCurrentTestMethodNameSplit.removeprefix('test_')
            TestCaseName = nCurrentTestMethodNameSplit.replace('test_', '')
            # print ("\nTestCaseName: " + TestCaseName)
        except Exception as e:
            TestCaseName = nCurrentTestMethodNameSplit
            print("\nUpgrade Python to 3.9 to avoid test_ string in your test case name, see below URL")
            # print("https://www.andreagrandi.it/2020/10/11/python39-introduces-removeprefix-removesuffix/")

        # exception = call.excinfo.value
        # exception_class = call.excinfo.type
        # exception_class_name = call.excinfo.typename

        # exception_traceback = call.excinfo.traceback

        if result.outcome == "failed":
            exception_type_and_message_formatted = call.excinfo.exconly()
            testCaseFailedStatusValue = "FAILED"
            reporting_client.test_stop(TestResultFactory.create_failure(str(testCaseErrorMsg)))
            testCaseNameList.append(TestCaseName)
            testCaseStatusList.append(testCaseFailedStatusValue)
            testCaseErrorMsg.append(exception_type_and_message_formatted)
            testCaseReportURL.append(reporting_client.report_url())

            print("\n     TestStatus: " + testCaseFailedStatusValue)
            print("     FailureMsg: " + str(testCaseErrorMsg))
            reportPerfecto(TestCaseName, testCaseFailedStatusValue, testCaseErrorMsg,
                           str(reporting_client.report_url()))

        if result.outcome == "passed":
            testCasePassedStatusValue = "PASSED"
            reporting_client.test_stop(TestResultFactory.create_success())
            testCaseNameList.append(TestCaseName)
            testCaseStatusList.append(testCasePassedStatusValue)
            testCaseReportURL.append(reporting_client.report_url())
            print("\n     TestStatus:  " + testCasePassedStatusValue)
            reportPerfecto(TestCaseName, testCasePassedStatusValue, "N/A", str(reporting_client.report_url()))

        if result.outcome == "skipped":
            testCaseSkippedStatusValue = "SKIPPED"
            exception_type_Skipped_message_formatted = call.excinfo.exconly()
            reporting_client.test_stop(TestResultFactory.create_failure(str(exception_type_Skipped_message_formatted)))
            testCaseNameList.append(TestCaseName)
            testCaseStatusList.append("SKIPPED")
            testCaseErrorMsg.append(str(exception_type_Skipped_message_formatted))
            testCaseReportURL.append(reporting_client.report_url())
            print("\n     TestStatus: " + testCaseSkippedStatusValue)
            print("     FailureMsg: " + str(testCaseErrorMsg))
            reportPerfecto(TestCaseName, testCaseSkippedStatusValue, testCaseErrorMsg,
                           str(reporting_client.report_url()))


def pytest_sessionfinish(session, exitstatus):

    try:
        if reporting_client is not None:
            print()
            skipped_amount = 0
            # print('Perfecto TestCase Execution Status:', exitstatus)
            passed_amount = sum(1 for result in session.results.values() if result.passed)
            failed_amount = sum(1 for result in session.results.values() if result.failed)
            skipped_amount = sum(1 for result in session.results.values() if result.skipped)
            #  print(f'There are {passed_amount} passed and {failed_amount} failed tests')
            TotalExecutedCount = failed_amount + passed_amount + skipped_amount

            print('\n------------------------------------')
            print('TestCase Execution Summary')
            print('------------------------------------')
            print('Total TestCase Executed: ' + str(TotalExecutedCount))
            print('Total Passed: ' + str(passed_amount))
            print('Total Failed: ' + str(failed_amount))
            print('Total Skipped: ' + str(skipped_amount) + "\n")
            try:
                for index in range(len(testCaseNameList)):
                    print(str(index + 1) + ") " + str(testCaseNameList[index]) + " : " + str(testCaseStatusList[index]))
                    print("     ReportURL: " + str(testCaseReportURL[index]))
                    print("     FailureMsg: " + str(testCaseErrorMsg[index]) + "\n")
            except Exception as e:
                print('No Interop Test Cases Executed')
        else:
            pass

    except Exception as e:
        pass
    print('\n------------------------------------------------------------------\n\n\n\n')


@pytest.fixture(scope="function")
def setup_perfectoMobile_android(request, get_device_configuration):
    from appium import webdriver
    driver = None
    reporting_client = None

    warnings.simplefilter("ignore", ResourceWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    capabilities = {
        'platformName': get_device_configuration["platformName-android"],
        'model': get_device_configuration["model-android"],
        'browserName': 'mobileOS',
        # 'automationName' : 'Appium',
        'securityToken': PERFECTO_DETAILS["securityToken"],
        'useAppiumForWeb': 'false',
        'useAppiumForHybrid': 'false',
        # 'bundleId' : request.config.getini("appPackage-android"),
    }

    if not is_device_Available_timeout(request, capabilities['model']):
        print("Unable to get device.")
        pytest.exit("Exiting Pytest")

    driver = webdriver.Remote(
        'https://' + PERFECTO_DETAILS["perfectoURL"] + '.perfectomobile.com/nexperience/perfectomobile/wd/hub',
        capabilities)
    driver.implicitly_wait(2)

    TestCaseFullName = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
    nCurrentTestMethodNameSplit = re.sub(r'\[.*?\]\ *', "", TestCaseFullName)
    try:
        # TestCaseName = nCurrentTestMethodNameSplit.removeprefix('test_')
        TestCaseName = nCurrentTestMethodNameSplit.replace('test_', '')
        print("\n\nExecuting TestCase: " + TestCaseName)
    except Exception as e:
        TestCaseName = nCurrentTestMethodNameSplit
        print("\nUpgrade Python to 3.9 to avoid test_ string in your test case name, see below URL")
        # print("https://www.andreagrandi.it/2020/10/11/python39-introduces-removeprefix-removesuffix/")

    projectname = PERFECTO_DETAILS["projectName"]
    projectversion = PERFECTO_DETAILS["projectVersion"]
    jobname = get_device_configuration["jobName"]
    jobnumber = get_device_configuration["jobNumber"]
    tags = PERFECTO_DETAILS["reportTags"]
    testCaseName = TestCaseName

    # print("\nSetting Perfecto ReportClient....")
    perfecto_execution_context = PerfectoExecutionContext(driver, tags, Job(jobname, jobnumber),
                                                          Project(projectname, projectversion))
    reporting_client = PerfectoReportiumClient(perfecto_execution_context)
    reporting_client.test_start(testCaseName, TestContext([], "Perforce"))
    reportClient(reporting_client)

    try:
        params = {'property': 'model'}
        deviceModel = driver.execute_script('mobile:handset:info', params)
    except:
        pass

    def teardown():
        try:
            print("\n---------- Tear Down ----------")
            try:
                params = {'property': 'model'}
                deviceModel = driver.execute_script('mobile:handset:info', params)
                allure.dynamic.link(
                    str(reporting_client.report_url()),
                    name=str(deviceModel))
            except:
                print("fail to attach video link")

            print('Report-Url: ' + reporting_client.report_url())

            print("----------------------------------------------------------\n\n\n\n")
            driver.close()
        except Exception as e:
            print(" -- Exception While Tear Down --")
            driver.close()
            print(e)
        finally:
            try:
                driver.quit()
            except Exception as e:
                print(" -- Exception Not Able To Quit --")
                print(e)

    request.addfinalizer(teardown)

    if driver is None:
        yield -1
    else:
        yield driver, reporting_client


def reportClient(value):
    global reporting_client  # declare a to be a global
    reporting_client = value  # this sets the global value of a


def reportPerfecto(testCaseName, testCaseStatus, testErrorMsg, reportURL):
    global testCaseNameList  # declare a to be a global
    global testCaseStatusList
    global testCaseErrorMsg
    global testCaseReportURL

    testCaseNameList.append(testCaseName)
    testCaseStatusList.append(testCaseStatus)
    testCaseErrorMsg.append(str(testErrorMsg))
    testCaseReportURL.append(reportURL)


@pytest.fixture(scope="class")
def setup_perfectoMobileWeb(request, get_device_configuration):
    from selenium import webdriver
    rdriver = None
    reporting_client = None

    warnings.simplefilter("ignore", ResourceWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    capabilities = {
        'platformName': get_device_configuration["platformName-iOS"],
        'model': get_device_configuration["model-iOS"],
        'browserName': get_device_configuration["browserType-iOS"],
        'securityToken': get_device_configuration["securityToken"],
    }

    if not is_device_Available_timeout(request, capabilities['model']):
        print("Unable to get device.")
        pytest.exit("Exiting Pytest")

    rdriver = webdriver.Remote(
        'https://' + PERFECTO_DETAILS["perfectoURL"] + '.perfectomobile.com/nexperience/perfectomobile/wd/hub',
        capabilities)
    rdriver.implicitly_wait(2)

    projectname = PERFECTO_DETAILS["projectName"]
    projectversion = PERFECTO_DETAILS["projectVersion"]
    jobname = get_device_configuration["jobName"]
    jobnumber = get_device_configuration["jobNumber"]
    tags = PERFECTO_DETAILS["reportTags"]
    testCaseName = get_device_configuration["jobName"]

    print("Setting Perfecto ReportClient....")
    perfecto_execution_context = PerfectoExecutionContext(rdriver, tags, Job(jobname, jobnumber),
                                                          Project(projectname, projectversion))
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
            print(e.message)
        finally:
            try:
                rdriver.quit()
            except Exception as e:
                print(" -- Exception Not Able To Quit --")
                print(e.message)

    request.addfinalizer(teardown)

    if rdriver is None:
        yield -1
    else:
        yield rdriver, reporting_client


@pytest.fixture(scope="function")
def setup_perfectoMobile_iOS(request, get_device_configuration):
    from appium import webdriver
    driver = None
    reporting_client = None

    warnings.simplefilter("ignore", ResourceWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    capabilities = {
        'platformName': get_device_configuration["platformName-iOS"],
        'model': get_device_configuration["model-iOS"],
        'browserName': 'safari',
        # 'automationName' : 'Appium',
        'securityToken': PERFECTO_DETAILS["securityToken"],
        'useAppiumForWeb': 'false',
        'autoAcceptAlerts': 'true',
        # 'bundleId' : request.config.getini("bundleId-iOS"),
        'useAppiumForHybrid': 'false',
    }

    # Check if the device is available
    if not is_device_Available_timeout(request, capabilities['model']):
        print("Unable to get device.")
        pytest.exit("Exiting Pytest")

    driver = webdriver.Remote(
        'https://' + PERFECTO_DETAILS["perfectoURL"] + '.perfectomobile.com/nexperience/perfectomobile/wd/hub',
        capabilities)
    driver.implicitly_wait(2)

    TestCaseFullName = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
    nCurrentTestMethodNameSplit = re.sub(r'\[.*?\]\ *', "", TestCaseFullName)
    try:
        # TestCaseName = nCurrentTestMethodNameSplit.removeprefix('test_')
        TestCaseName = nCurrentTestMethodNameSplit.replace('test_', '')
        print("\n\nExecuting TestCase: " + TestCaseName)
    except Exception as e:
        TestCaseName = nCurrentTestMethodNameSplit
        print("\nUpgrade Python to 3.9 to avoid test_ string in your test case name, see below URL")
        # print("https://www.andreagrandi.it/2020/10/11/python39-introduces-removeprefix-removesuffix/")

    projectname = PERFECTO_DETAILS["projectName"]
    projectversion = PERFECTO_DETAILS["projectVersion"]
    jobname = get_device_configuration["jobName"]
    jobnumber = get_device_configuration["jobNumber"]
    tags = PERFECTO_DETAILS["reportTags"]
    testCaseName = TestCaseName

    print("\nSetting Perfecto ReportClient....")
    perfecto_execution_context = PerfectoExecutionContext(driver, tags, Job(jobname, jobnumber),
                                                          Project(projectname, projectversion))
    reporting_client = PerfectoReportiumClient(perfecto_execution_context)
    reporting_client.test_start(testCaseName, TestContext([], "Perforce"))
    reportClient(reporting_client)
    try:
        params = {'property': 'model'}
        deviceModel = driver.execute_script('mobile:handset:info', params)
    except:
        pass

    def teardown():
        try:
            print("\n---------- Tear Down ----------")
            print('Report-Url: ' + reporting_client.report_url())
            try:
                allure.dynamic.link(
                    str(reporting_client.report_url()),
                    name=str(deviceModel))
            except:
                print("fail to attach video link")
            print("----------------------------------------------------------\n\n\n\n")
            driver.close()
        except Exception as e:
            print(" -- Exception While Tear Down --")
            driver.close()
            print(e)
        finally:
            try:
                driver.quit()
            except Exception as e:
                print(" -- Exception Not Able To Quit --")
                print(e)

    request.addfinalizer(teardown)

    if driver is None:
        yield -1
    else:
        yield driver, reporting_client
# Does a HTTP GET request to Perfecto cloud and gets response and information related to a headset
def response_device(request, model):
    securityToken = PERFECTO_DETAILS["securityToken"]
    perfectoURL = PERFECTO_DETAILS["perfectoURL"]
    url = f"https://{perfectoURL}.perfectomobile.com/services/handsets?operation=list&securityToken={securityToken}&model={model}"
    resp = requests.get(url=url)
    return ET.fromstring(resp.content)

# Get an attribute value from the handset response
def get_attribute_device(responseXml, attribute):
    try:
        return responseXml.find('handset').find(attribute).text
    except:
        print(f"Unable to get value of {attribute} from response")
        return ""

# Checks to see if a particular handset is available
def is_device_available(request, model):
    try:
        responseXml = response_device(request, model)
    except:
        print("Unable to get response.")
        raise Exception("Unable to get response.")
    device_available = get_attribute_device(responseXml, 'available')
    print("Result:" + device_available)
    if device_available == 'true':
        return True
    else:
        allocated_to = get_attribute_device(responseXml, 'allocatedTo')
        print("The device is currently allocated to:" + allocated_to)
        return False

# Checks whether the device is available or not.If the device is not available rechecks depending upon the

# Checks whether the device is available or not.If the device is not available rechecks depending upon the
# 'timerValue' and 'timerThreshold' values.With the current parameters it will check after:10,20,40,80 mins.
def is_device_Available_timeout(request, model):
    device_available = is_device_available(request, model)
    timerValue = 5
    timerThreshold = 80
    if not device_available:
        while(timerValue <= timerThreshold):
            print("Last checked at:" + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            print(f"Waiting for: {timerValue} min(s)")
            time.sleep(timerValue*60)
            print("Checking now at:" + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            device_available = is_device_available(request, model)
            if(device_available):
                return True
            else:
                timerValue = timerValue + 5

        if(timerValue > timerThreshold):
            return False
        else:
            return True
    else:
        return True

def get_device_attribuites(request, model, attribute):
    try:
        responseXml = response_device(request, model)
    except:
        print("Unable to get response.")
        raise Exception("Unable to get response.")
    try:
        attribute_value = get_attribute_device(responseXml, str(attribute))
    except:
        attribute_value = False
    return attribute_value
