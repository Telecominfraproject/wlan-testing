"""
    Pytest fixtures: High level Resource Management and base setup fixtures
"""
import datetime
import sys
import os
import time

import allure
import re
import logging

from _pytest.fixtures import SubRequest
from pyparsing import Optional

ALLURE_ENVIRONMENT_PROPERTIES_FILE = 'environment.properties'
ALLUREDIR_OPTION = '--alluredir'

# if "logs" not in os.listdir():
#     os.mkdir("logs/")
# logging.basicConfig(level=logging.INFO, filename="logs/" + '{:%Y-%m-%d-%H-%M-%S}.log'.format(datetime.datetime.now()))
sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)
if "libs" not in sys.path:
    sys.path.append(f'../libs')
for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../lanforge/lanforge-scripts/{folder}')

sys.path.append(f"../lanforge/lanforge-scripts/py-scripts/tip-cicd-sanity")

sys.path.append(f'../libs')
sys.path.append(f'../libs/lanforge/')

from LANforge.LFUtils import *

if 'py-json' not in sys.path:
    sys.path.append('../py-scripts')
from apnos.apnos import APNOS
from controller.controller import Controller
from controller.ucentral_ctlr import UController
from controller.controller import FirmwareUtility
import pytest
from cv_test_manager import cv_test
from configuration import CONFIGURATION
from configuration import RADIUS_SERVER_DATA
from configuration import RADIUS_ACCOUNTING_DATA
from configuration import TEST_CASES
from testrails.testrail_api import APIClient
from testrails.reporting import Reporting
from lf_tools import ChamberView
from sta_connect2 import StaConnect2
from os import path
from typing import Any, Callable, Optional

from _pytest.fixtures import SubRequest
from pytest import fixture


def pytest_addoption(parser):
    """pytest addoption function: contains ini objects and options"""
    parser.addini("tr_url", "Test Rail URL")
    parser.addini("tr_prefix", "Test Rail Prefix (Generally Testbed_name_)")
    parser.addini("tr_user", "Testrail Username")
    parser.addini("tr_pass", "Testrail Password")
    parser.addini("tr_project_id", "Testrail Project ID")
    parser.addini("milestone", "milestone Id")

    parser.addini("influx_host", "Influx Host", default="influx.cicd.lab.wlan.tip.build")
    parser.addini("influx_port", "Influx Port", default=80)
    parser.addini("influx_token", "Influx Token", default="TCkdATXAbHmNbn4QyNaj43WpGBYxFrzV")
    parser.addini("influx_bucket", "influx bucket", default="tip-cicd")
    parser.addini("influx_org", "influx organization", default="tip")
    parser.addini("build", "AP Firmware build URL", default="0")
    parser.addini("cloud_ctlr", "AP Firmware build URL", default="0")

    parser.addini("num_stations", "Number of Stations/Clients for testing")

    # change behaviour
    parser.addoption(
        "--skip-upgrade",
        action="store_true",
        default=False,
        help="skip updating firmware on the AP (useful for local testing)"
    )

    # change behaviour
    parser.addoption(
        "--exit-on-fail",
        action="store_true",
        default=False,
        help="skip updating firmware on the AP (useful for local testing)"
    )

    # change to Ucentral Ctlr
    parser.addoption(
        "--1.x",
        action="store_true",
        default=False,
        help="Option to run Test Cases on 1.x SDK"
    )

    # change behaviour
    parser.addoption(
        "--force-upgrade",
        action="store_true",
        default=False,
        help="force Upgrading Firmware even if it is already latest version"
    )
    parser.addoption(
        "--force-upload",
        action="store_true",
        default=False,
        help="force Uploading Firmware even if it is already latest version"
    )
    # this has to be the last argument
    # example: --access-points ECW5410 EA8300-EU
    parser.addoption(
        "--testbed",
        # nargs="+",
        default="basic-01",
        help="AP Model which is needed to test"
    )
    parser.addoption(
        "--skip-testrail",
        action="store_true",
        default=False,
        help="Stop using Testrails"
    )

    # Perfecto Parameters
    parser.addini("perfectoURL", "Cloud URL")
    parser.addini("securityToken", "Security Token")
    parser.addini("platformName-iOS", "iOS Platform")
    parser.addini("platformName-android", "Android Platform")
    parser.addini("model-iOS", "iOS Devices")
    parser.addini("model-android", "Android Devices")
    parser.addini("bundleId-iOS", "iOS Devices")
    parser.addini("bundleId-iOS-Settings", "iOS Settings App")
    parser.addini("appPackage-android", "Android Devices")
    parser.addini("bundleId-iOS-Safari", "Safari BundleID")
    parser.addini("wifi-SSID-2g-Pwd", "Wifi 2g Password")
    parser.addini("Default-SSID-5gl-perfecto-b", "Wifi 5g AP Name")
    parser.addini("Default-SSID-2g-perfecto-b", "Wifi 2g AP Name")
    parser.addini("Default-SSID-perfecto-b", "Wifi AP Name")
    parser.addini("bundleId-iOS-Ping", "Ping Bundle ID")
    parser.addini("browserType-iOS", "Mobile Browser Name")
    parser.addini("projectName", "Project Name")
    parser.addini("projectVersion", "Project Version")
    parser.addini("jobName", "CI Job Name")
    parser.addini("jobNumber", "CI Job Number")
    parser.addini("reportTags", "Report Tags")
    parser.addoption(
        "--access-points-perfecto",
        # nargs="+",
        default=["Perfecto"],
        help="list of access points to test"
    )


"""
Test session base fixture
"""


# To be depreciated as testrails will go
@pytest.fixture(scope="session")
def test_cases():
    """Yields the test cases from configuration.py: will be depreciated"""
    yield []


@pytest.fixture(scope="session")
def testbed(request):
    """yields the testbed option selection"""
    var = request.config.getoption("--testbed")
    allure.attach(body=str(var),
                  name="Testbed Selected : ")
    yield var


@pytest.fixture(scope="session")
def should_upload_firmware(request):
    """yields the --force-upload option for firmware upload selection"""
    yield request.config.getoption("--force-upload")


@pytest.fixture(scope="session")
def should_upgrade_firmware(request):
    """yields the --force-upgrade option  for firmware upgrade selection"""
    yield request.config.getoption("--force-upgrade")


@pytest.fixture(scope="session")
def exit_on_fail(request):
    """yields the --exit-on-fail option for exiting the test case if it fails without teardown"""
    yield request.config.getoption("--exit-on-fail")


@pytest.fixture(scope="session")
def radius_info():
    """yields the radius server information from lab info file"""
    allure.attach(body=str(RADIUS_SERVER_DATA), name="Radius server Info: ")
    yield RADIUS_SERVER_DATA


@pytest.fixture(scope="session")
def radius_accounting_info():
    """yields the radius accounting information from lab info file"""
    allure.attach(body=str(RADIUS_ACCOUNTING_DATA), name="Radius server Info: ")
    yield RADIUS_ACCOUNTING_DATA


@pytest.fixture(scope="session")
def get_configuration(testbed, request):
    """yields the selected testbed information from lab info file (configuration.py)"""
    allure.attach(body=str(testbed), name="Testbed Selected: ")
    if request.config.getini("cloud_ctlr") != "0":
        CONFIGURATION[testbed]["controller"]["url"] = request.config.getini("cloud_ctlr")
    yield CONFIGURATION[testbed]


@pytest.fixture(scope="session")
def get_apnos():
    """yields the LIBRARY for APNOS, Reduces the use of imports across files"""
    yield APNOS


@pytest.fixture(scope="session")
def get_equipment_id(request, setup_controller, testbed, get_configuration):
    """"""
    if request.config.getoption("1.x"):
        equipment_id_list = []
        for i in get_configuration['access_point']:
            equipment_id_list.append(setup_controller.get_equipment_id(
                serial_number=i['serial']))
    else:
        equipment_id_list = []
        for i in get_configuration['access_point']:
            equipment_id_list.append(i['serial'])
    yield equipment_id_list


@pytest.fixture(scope="session")
def instantiate_access_point(testbed, get_apnos, get_configuration):
    """setup the access point connectivity"""
    for access_point_info in get_configuration['access_point']:
        if access_point_info["jumphost"]:
            allure.attach(name="added openwrtctl.py to :",
                          body=access_point_info['ip'] + ":" + str(access_point_info["port"]))
            get_apnos(access_point_info, pwd="../libs/apnos/")
        else:
            allure.attach(name="Direct AP SSH : ",
                          body=access_point_info['ip'] + ":" + str(access_point_info["port"]))
        # Write a code to verify Access Point Connectivity
    yield True


# Controller Fixture
@pytest.fixture(scope="session")
def setup_controller(request, get_configuration, test_access_point, add_env_properties):
    """sets up the controller connection and yields the sdk_client object"""
    try:
        if request.config.getoption("1.x"):
            sdk_client = Controller(controller_data=get_configuration["controller"])
            allure.attach(body=str(get_configuration["controller"]), name="Controller Instantiated: ")

            def teardown_controller():
                print("\nTest session Completed")
                allure.attach(body=str(get_configuration["controller"]), name="Controller Teardown: ")
                sdk_client.disconnect_Controller()

            request.addfinalizer(teardown_controller)

        else:
            sdk_client = UController(controller_data=get_configuration["controller"])
            allure.attach(body=str(get_configuration["controller"]), name="Ucentral Controller Instantiated: ")

            def teardown_ucontroller():
                print("\nTest session Completed")
                sdk_client.logout()
                allure.attach(body=str(get_configuration["controller"]), name="Controller Teardown: ")
                try:
                    sdk_client.logout()
                except Exception as e:
                    print(e)

            request.addfinalizer(teardown_ucontroller)

    except Exception as e:
        print(e)
        allure.attach(body=str(e), name="Controller Instantiation Failed: ")
        sdk_client = False
        pytest.exit("unable to communicate to Controller" + str(e))
    yield sdk_client


@pytest.fixture(scope="session")
def instantiate_firmware(request, setup_controller, get_configuration):
    """sets up firmware utility and yields the object for firmware upgrade"""
    if request.config.getoption("--1.x"):
        firmware_client_obj = []

        for access_point_info in get_configuration['access_point']:
            version = access_point_info["version"]
            if request.config.getini("build").__contains__("https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/"):
                version = request.config.getini("build")
            firmware_client = FirmwareUtility(sdk_client=setup_controller,
                                              model=access_point_info["model"],
                                              version_url=version)
            firmware_client_obj.append(firmware_client)
        yield firmware_client_obj
    else:
        # 2.x
        pass


@pytest.fixture(scope="session")
def get_latest_firmware(request, instantiate_firmware):
    """yields the list of firmware version"""
    if request.config.getoption("--1.x"):
        fw_version_list = []
        try:

            for fw_obj in instantiate_firmware:
                latest_firmware = fw_obj.get_fw_version()
                latest_firmware = latest_firmware.replace(".tar.gz", "")
                fw_version_list.append(latest_firmware)
        except Exception as e:
            print(e)
            fw_version_list = []

        yield fw_version_list
    else:
        # 2.x
        pass


@pytest.fixture(scope="session")
def upload_firmware(request, should_upload_firmware, instantiate_firmware):
    """yields the firmware_id that is uploaded to cloud"""
    if request.config.getoption("--1.x"):
        firmware_id_list = []
        for i in range(0, len(instantiate_firmware)):
            firmware_id = instantiate_firmware[i].upload_fw_on_cloud(force_upload=should_upload_firmware)
            firmware_id_list.append(firmware_id)
        yield firmware_id_list
    else:
        # 2.x release
        yield True


@pytest.fixture(scope="session")
def upgrade_firmware(request, instantiate_firmware, get_equipment_id, check_ap_firmware_cloud, get_latest_firmware,
                     should_upgrade_firmware, should_upload_firmware, get_apnos, get_configuration):
    """yields the status of upgrade of firmware. waits for 300 sec after each upgrade request"""
    print(should_upgrade_firmware, should_upload_firmware)
    if request.config.getoption("--1.x"):
        status_list = []
        active_fw_list = []
        try:
            for access_point in get_configuration['access_point']:
                ap_ssh = get_apnos(access_point)
                active_fw = ap_ssh.get_active_firmware()
                active_fw_list.append(active_fw)
        except Exception as e:
            print(e)
            active_fw_list = []
        print(active_fw_list, get_latest_firmware)
        if get_latest_firmware != active_fw_list:
            if request.config.getoption("--skip-upgrade"):
                status = "skip-upgrade"
                status_list.append(status)
            else:

                for i in range(0, len(instantiate_firmware)):
                    status = instantiate_firmware[i].upgrade_fw(equipment_id=get_equipment_id[i], force_upload=True,
                                                                force_upgrade=should_upgrade_firmware)
                    allure.attach(name="Firmware Upgrade Request", body=str(status))
                    status_list.append(status)
        else:
            if should_upgrade_firmware:
                for i in range(0, len(instantiate_firmware)):
                    status = instantiate_firmware[i].upgrade_fw(equipment_id=get_equipment_id[i],
                                                                force_upload=should_upload_firmware,
                                                                force_upgrade=should_upgrade_firmware)
                    allure.attach(name="Firmware Upgrade Request", body=str(status))
                    status_list.append(status)
            else:
                status = "skip-upgrade Version Already Available"
                status_list.append(status)
        yield status_list
    else:
        # 2.x release
        pass


@pytest.fixture(scope="session")
def check_ap_firmware_cloud(request, setup_controller, get_equipment_id):
    """yields the active version of firmware on cloud"""
    if request.config.getoption("--1.x"):
        ap_fw_list = []
        for i in get_equipment_id:
            ap_fw_list.append(setup_controller.get_ap_firmware_old_method(equipment_id=i))
        yield ap_fw_list
    else:
        # 2.x
        pass


@pytest.fixture(scope="session")
def check_ap_firmware_ssh(get_configuration, request):
    """yields the active version of firmware on ap"""
    if request.config.getoption("--1.x"):
        active_fw_list = []
        try:
            for access_point in get_configuration['access_point']:
                ap_ssh = APNOS(access_point)
                active_fw = ap_ssh.get_active_firmware()
                active_fw_list.append(active_fw)
        except Exception as e:
            print(e)
            active_fw_list = []
        yield active_fw_list
    else:
        # 2.x
        pass


@pytest.fixture(scope="session")
def setup_test_run(setup_controller, request, upgrade_firmware, get_configuration,
                   get_equipment_id, get_latest_firmware,
                   get_apnos):
    """used to upgrade the firmware on AP and should be called on each test case on a module level"""
    if request.config.getoption("--1.x"):
        active_fw_list = []
        try:
            for access_point in get_configuration['access_point']:
                ap_ssh = get_apnos(access_point)
                active_fw = ap_ssh.get_active_firmware()
                active_fw_list.append(active_fw)
        except Exception as e:
            print(e)
            active_fw_list = []
        print(active_fw_list, get_latest_firmware)
        if active_fw_list == get_latest_firmware:
            yield True
        else:
            pytest.exit("AP is not Upgraded tp Target Firmware versions")
    else:
        # 2.x
        pass


"""
Instantiate Reporting
"""


@pytest.fixture(scope="session")
def update_report(request, testbed, get_configuration):
    """used to update the test report on testrail/allure"""
    if request.config.getoption("--skip-testrail"):
        tr_client = Reporting()
    else:
        tr_client = APIClient(request.config.getini("tr_url"), request.config.getini("tr_user"),
                              request.config.getini("tr_pass"), request.config.getini("tr_project_id"))
    if request.config.getoption("--skip-testrail"):
        tr_client.rid = "skip testrails"
    else:
        projId = tr_client.get_project_id(project_name=request.config.getini("tr_project_id"))
        test_run_name = request.config.getini("tr_prefix") + testbed + "_" + str(
            datetime.date.today()) + "_" + get_configuration['access_point'][0]['version']
        tr_client.create_testrun(name=test_run_name, case_ids=list(TEST_CASES.values()), project_id=projId,
                                 milestone_id=request.config.getini("milestone"),
                                 description="Automated Nightly Sanity test run for new firmware build")
        rid = tr_client.get_run_id(test_run_name=test_run_name)
        tr_client.rid = rid
    yield tr_client


"""
FRAMEWORK MARKER LOGIC
"""


@pytest.fixture(scope="session")
def get_security_flags():
    """used to get the essential markers on security and band"""
    # Add more classifications as we go
    security = ["open", "wpa", "wep", "wpa2_personal", "wpa3_personal", "wpa3_personal_mixed",
                "wpa_wpa2_enterprise_mixed", "wpa2_eap", "wpa2_only_eap",
                "wpa_wpa2_personal_mixed", "wpa_enterprise", "wpa2_enterprise", "wpa3_enterprise_mixed",
                "wpa3_enterprise", "twog", "fiveg", "radius"]
    yield security


@pytest.fixture(scope="session")
def get_markers(request, get_security_flags):
    """used to get the markers on the selected test case class, used in setup_profiles"""
    session = request.node
    markers = list()
    security = get_security_flags
    security_dict = dict().fromkeys(security)
    for item in session.items:
        for j in item.iter_markers():
            markers.append(j.name)
    # print(set(markers))
    for i in security:
        if set(markers).__contains__(i):
            security_dict[i] = True
        else:
            security_dict[i] = False
    # print(security_dict)
    allure.attach(body=str(security_dict), name="Test Cases Requires: ")
    yield security_dict


# Will be availabe as a test case
@pytest.fixture(scope="session")
def test_access_point(request, testbed, get_apnos, get_configuration):
    """used to check the manager status of AP, should be used as a setup to verify if ap can reach cloud"""
    mgr_status = []
    if request.config.getoption("1.x"):
        for access_point_info in get_configuration['access_point']:
            ap_ssh = get_apnos(access_point_info)
            status = ap_ssh.get_manager_state()
            if "ACTIVE" not in status:
                time.sleep(30)
                ap_ssh = APNOS(access_point_info)
                status = ap_ssh.get_manager_state()
            mgr_status.append(status)
    else:
        # for access_point_info in get_configuration['access_point']:
        #     ap_ssh = get_apnos(access_point_info)
        #     status = ap_ssh.get_manager_state()
        #     if "ACTIVE" not in status:
        #         time.sleep(30)
        #         ap_ssh = APNOS(access_point_info)
        #         status = ap_ssh.get_manager_state()
        #     mgr_status.append(status)
        pass
    yield mgr_status


# Not used anymore, needs to depreciate it
@pytest.fixture(scope="session")
def get_lanforge_data(get_configuration):
    """depreciate it"""
    lanforge_data = {}
    if get_configuration['traffic_generator']['name'] == 'lanforge':
        lanforge_data = {
            "lanforge_ip": get_configuration['traffic_generator']['details']['ip'],
            "lanforge-port-number": get_configuration['traffic_generator']['details']['port'],
            "lanforge_2dot4g": get_configuration['traffic_generator']['details']['2.4G-Radio'][0],
            "lanforge_5g": get_configuration['traffic_generator']['details']['5G-Radio'][0],
            "lanforge_2dot4g_prefix": get_configuration['traffic_generator']['details']['2.4G-Station-Name'],
            "lanforge_5g_prefix": get_configuration['traffic_generator']['details']['5G-Station-Name'],
            "lanforge_2dot4g_station": get_configuration['traffic_generator']['details']['2.4G-Station-Name'],
            "lanforge_5g_station": get_configuration['traffic_generator']['details']['5G-Station-Name'],
            "lanforge_bridge_port": get_configuration['traffic_generator']['details']['upstream'],
            "lanforge_vlan_port": get_configuration['traffic_generator']['details']['upstream'] + ".100",
            "vlan": 100
        }
    yield lanforge_data


@pytest.fixture(scope="session")
def traffic_generator_connectivity(testbed, get_configuration):
    """Verify if traffic generator is reachable"""
    if get_configuration['traffic_generator']['name'] == "lanforge":
        lanforge_ip = get_configuration['traffic_generator']['details']['ip']
        lanforge_port = get_configuration['traffic_generator']['details']['port']
        # Condition :
        #   if gui connection is not available
        #   yield False
        # Condition :
        # If Gui Connection is available
        # yield the gui version
        try:
            cv = cv_test(lanforge_ip, lanforge_port)
            url_data = cv.get_ports("/")
            lanforge_GUI_version = url_data["VersionInfo"]["BuildVersion"]
            lanforge_gui_git_version = url_data["VersionInfo"]["GitVersion"]
            lanforge_gui_build_date = url_data["VersionInfo"]["BuildDate"]
            print(lanforge_GUI_version, lanforge_gui_build_date, lanforge_gui_git_version)
            if not (lanforge_GUI_version or lanforge_gui_build_date or lanforge_gui_git_version):
                yield False
            else:
                yield lanforge_GUI_version
        except:
            yield False
    else:
        yield True


@pytest.fixture(scope="session")
def create_lanforge_chamberview_dut(get_configuration, testbed):
    """ Create a DUT on LANforge"""
    ChamberView(lanforge_data=get_configuration["traffic_generator"]["details"],
                testbed=testbed, access_point_data=get_configuration["access_point"])
    yield True


@pytest.fixture(scope="session")
def lf_tools(get_configuration, testbed):
    """ Create a DUT on LANforge"""
    obj = ChamberView(lanforge_data=get_configuration["traffic_generator"]["details"],
                      testbed=testbed, access_point_data=get_configuration["access_point"])

    yield obj


@pytest.fixture(scope="session")
def lf_tools(get_configuration, testbed):
    """ Create a DUT on LANforge"""
    obj = ChamberView(lanforge_data=get_configuration["traffic_generator"]["details"],
                      testbed=testbed, access_point_data=get_configuration["access_point"])
    yield obj


# @pytest.fixture(scope="class")
# def create_vlan(request, testbed, get_configuration, lf_tools):
#     """Create a vlan on lanforge"""
#


@pytest.fixture(scope="session")
def setup_influx(request, testbed, get_configuration):
    """ Setup Influx Parameters: Used in CV Automation"""
    influx_params = {
        "influx_host": request.config.getini("influx_host"),
        "influx_port": request.config.getini("influx_port"),
        "influx_token": request.config.getini("influx_token"),
        "influx_bucket": request.config.getini("influx_bucket"),
        "influx_org": request.config.getini("influx_org"),
        "influx_tag": [testbed, get_configuration["access_point"][0]["model"]],
    }
    yield influx_params


# Need for Perforce Mobile Device Execution
def pytest_sessionstart(session):
    session.results = dict()


ALLURE_ENVIRONMENT_PROPERTIES_FILE = 'environment.properties'
ALLUREDIR_OPTION = '--alluredir'


@fixture(scope='session', autouse=True)
def add_allure_environment_property(request: SubRequest) -> Optional[Callable]:
    environment_properties = dict()

    def maker(key: str, value: Any):
        environment_properties.update({key: value})

    yield maker

    alluredir = request.config.getoption(ALLUREDIR_OPTION)

    if not alluredir or not os.path.isdir(alluredir) or not environment_properties:
        return

    allure_env_path = path.join(alluredir, ALLURE_ENVIRONMENT_PROPERTIES_FILE)

    with open(allure_env_path, 'w') as _f:
        data = '\n'.join([f'{variable}={value}' for variable, value in environment_properties.items()])
        _f.write(data)


@fixture(scope='session')
def get_uc_ap_version(get_apnos, get_configuration):
    version_list = []
    for access_point_info in get_configuration['access_point']:
        ap_ssh = get_apnos(access_point_info)
        version = ap_ssh.get_ap_version_ucentral()
        version_list.append(version)
    yield version_list


@fixture(scope='session')
def add_env_properties(get_configuration, get_uc_ap_version, add_allure_environment_property: Callable) -> None:
    add_allure_environment_property('Access-Point-Model', get_configuration["access_point"][0]["model"])
    add_allure_environment_property('Access-Point-Firmware-Version', "\n".join(get_uc_ap_version))
    add_allure_environment_property('Cloud-Controller-SDK-URL', get_configuration["controller"]["url"])
