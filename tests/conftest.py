"""
    Pytest fixtures: High level Resource Management and base setup fixtures
"""
import datetime
import os
import random
import string
import sys
import re

import allure

ALLURE_ENVIRONMENT_PROPERTIES_FILE = 'environment.properties'
ALLUREDIR_OPTION = '--alluredir'

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
from controller.controller_1x.controller import FirmwareUtility
import pytest
from lanforge.lf_tests import RunTest
from cv_test_manager import cv_test
from configuration import CONFIGURATION
from configuration import PERFECTO_DETAILS
from configuration import open_flow
from configuration import RADIUS_SERVER_DATA
from configuration import RADIUS_ACCOUNTING_DATA
from configuration import RATE_LIMITING_RADIUS_SERVER_DATA
from configuration import RATE_LIMITING_RADIUS_ACCOUNTING_DATA
from lanforge.scp_util import SCP_File
from testrails.testrail_api import APIClient
from testrails.reporting import Reporting
from lf_tools import ChamberView
from os import path
from typing import Any, Callable, Optional

from _pytest.fixtures import SubRequest
from pytest import fixture

from fixtures_1x import Fixtures_1x
from fixtures_2x import Fixtures_2x

ALLURE_ENVIRONMENT_PROPERTIES_FILE = 'environment.properties'
ALLUREDIR_OPTION = '--alluredir'
import logging

LOGGER = logging.getLogger(__name__)


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
    parser.addini(name="firmware", type='string', help="AP Firmware build URL", default="0")
    parser.addini("cloud_ctlr", "AP Firmware build URL", default="0")

    parser.addini("num_stations", "Number of Stations/Clients for testing")

    # change behaviour
    parser.addoption(
        "--skip-upgrade",
        action="store_true",
        default=False,
        help="skip updating firmware on the AP (useful for local testing)"
    )

    parser.addoption(
        "--skip-lanforge",
        action="store_true",
        default=False,
        help="skip to do any interactions on lanforge (to be used in case of interop)"
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
        "--use-testrail",
        action="store_false",
        default=True,
        help="Stop using Testrails"
    )
    parser.addoption(
        "--run-lf",
        action="store_true",
        default=False,
        help="skip cloud controller and AP, run only lanforge tests on a ssid preconfigured"
    )
    parser.addoption(
        "--skip-pcap",
        action="store_true",
        default=False,
        help="skip packet capture for sanity"
    )
    parser.addoption(
        "--device",
        default="iPhone-11",
        help="Device Model which is needed to test"
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
    yield var

@pytest.fixture(scope="session")
def device(request):
    """yields the device option selection"""
    var = request.config.getoption("--device")
    yield var

@pytest.fixture(scope="session")
def should_upload_firmware(request):
    """yields the --force-upload option for firmware upload selection"""
    yield request.config.getoption("--force-upload")


@pytest.fixture(scope="session")
def run_lf(request):
    """yields the --run-lf option for skipping configuration on AP and using Cloud controller"""
    var = request.config.getoption("--run-lf")
    yield var

@pytest.fixture(scope="session")
def skip_pcap(request):
    """yields the --skip-pcap option for skipping the packet capture for sanity"""
    var = request.config.getoption("--skip-pcap")
    yield var

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
    yield RADIUS_SERVER_DATA


@pytest.fixture(scope="session")
def radius_accounting_info():
    """yields the radius accounting information from lab info file"""
    yield RADIUS_ACCOUNTING_DATA


@pytest.fixture(scope="session")
def rate_radius_info():
    """yields the radius server information from lab info file"""
    yield RATE_LIMITING_RADIUS_SERVER_DATA


@pytest.fixture(scope="session")
def rate_radius_accounting_info():
    """yields the radius accounting information from lab info file"""
    yield RATE_LIMITING_RADIUS_ACCOUNTING_DATA


@pytest.fixture(scope="session")
def get_configuration(testbed, request):
    """yields the selected testbed information from lab info file (configuration.py)"""
    if request.config.getini("cloud_ctlr") != "0":
        CONFIGURATION[testbed]["controller"]["url"] = request.config.getini("cloud_ctlr")
    if request.config.getini("firmware") != "0":
        version = request.config.getini("firmware")
        version_list = version.split(",")
        for i in range(len(CONFIGURATION[testbed]["access_point"])):
            CONFIGURATION[testbed]["access_point"][i]["version"] = version_list[0]
    LOGGER.info("Selected the lab Info data: " + str((CONFIGURATION[testbed])))
    yield CONFIGURATION[testbed]

@pytest.fixture(scope="session")
def get_device_configuration(device, request):
    """yields the selected device information from lab info file (configuration.py)"""

    LOGGER.info("Selected the lab Info data: " + str((PERFECTO_DETAILS[device])))
    print(PERFECTO_DETAILS[device])
    yield PERFECTO_DETAILS[device]


@pytest.fixture(scope="session")
def get_apnos():
    """yields the LIBRARY for APNOS, Reduces the use of imports across files"""
    yield APNOS


@pytest.fixture(scope="session")
def get_equipment_ref(request, setup_controller, testbed, get_configuration):
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
def get_sdk_version(fixtures_ver, run_lf):
    version = ""
    if not run_lf:
        version = fixtures_ver.get_sdk_version()
    yield version


@pytest.fixture(scope="session")
def get_uci_show(fixtures_ver, get_apnos, get_configuration):
    uci_show = fixtures_ver.get_uci_show(get_apnos, get_configuration)
    yield uci_show

@pytest.fixture(scope="session")
def get_ap_version(fixtures_ver, get_apnos, get_configuration):
    ap_version = fixtures_ver.get_ap_version(get_apnos, get_configuration)
    yield ap_version

@pytest.fixture(scope="session")
def skip_lf(request):
    yield request.config.getoption("--skip-lanforge")


@pytest.fixture(scope="session")
def get_openflow():
    yield open_flow


# Controller Fixture
@pytest.fixture(scope="session")
def setup_controller(request, get_configuration, add_env_properties, fixtures_ver):
    """sets up the controller connection and yields the sdk_client object"""
    sdk_client = fixtures_ver.controller_obj
    request.addfinalizer(fixtures_ver.disconnect)
    yield sdk_client

# Prov Controller Fixture
@pytest.fixture(scope="session")
def setup_prov_controller(request, get_configuration, add_env_properties, fixtures_ver):
    """sets up the prov controller connection and yields the sdk_client object"""
    sdk_client = fixtures_ver.prov_controller_obj
    request.addfinalizer(fixtures_ver.disconnect)
    yield sdk_client


@pytest.fixture(scope="session")
def setup_firmware(setup_controller):
    """ Fixture to Setup Firmware with the selected sdk """
    setup_controller.instantiate_firmware()
    yield True


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
def upgrade_firmware(request, instantiate_firmware, get_equipment_ref, check_ap_firmware_cloud, get_latest_firmware,
                     should_upgrade_firmware, should_upload_firmware, get_apnos, get_configuration):
    """yields the status of upgrade of firmware. waits for 300 sec after each upgrade request"""
    print(should_upgrade_firmware, should_upload_firmware)
    if request.config.getoption("--1.x"):
        status_list = []
        active_fw_list = []
        try:
            for access_point in get_configuration['access_point']:
                ap_ssh = get_apnos(access_point, sdk="1.x")
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
                    status = instantiate_firmware[i].upgrade_fw(equipment_id=get_equipment_ref[i], force_upload=True,
                                                                force_upgrade=should_upgrade_firmware)
                    status_list.append(status)
        else:
            if should_upgrade_firmware:
                for i in range(0, len(instantiate_firmware)):
                    status = instantiate_firmware[i].upgrade_fw(equipment_id=get_equipment_ref[i],
                                                                force_upload=should_upload_firmware,
                                                                force_upgrade=should_upgrade_firmware)
                    status_list.append(status)
            else:
                status = "skip-upgrade Version Already Available"
                status_list.append(status)
        yield status_list
    else:
        # 2.x release
        pass


@pytest.fixture(scope="session")
def check_ap_firmware_cloud(request, setup_controller, get_equipment_ref):
    """yields the active version of firmware on cloud"""
    if request.config.getoption("--1.x"):
        ap_fw_list = []
        for i in get_equipment_ref:
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
                   get_equipment_ref, get_latest_firmware,
                   get_apnos):
    """used to upgrade the firmware on AP and should be called on each test case on a module level"""
    if request.config.getoption("--1.x"):
        active_fw_list = []
        try:
            for access_point in get_configuration['access_point']:
                ap_ssh = get_apnos(access_point, sdk="1.x")
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
    if request.config.getoption("--use-testrail"):
        tr_client = Reporting()
    else:
        tr_client = APIClient(request.config.getini("tr_url"), request.config.getini("tr_user"),
                              request.config.getini("tr_pass"), request.config.getini("tr_project_id"))
    if request.config.getoption("--use-testrail"):
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
    for i in security:
        if set(markers).__contains__(i):
            security_dict[i] = True
        else:
            security_dict[i] = False

    yield security_dict


@pytest.fixture(scope="session")
def test_access_point(fixtures_ver, request, get_configuration, get_apnos):
    """used to check the manager status of AP, should be used as a setup to verify if ap can reach cloud"""
    status = fixtures_ver.get_ap_cloud_connectivity_status(get_configuration, get_apnos)

    def teardown_session():
        data = []
        data.append(False)
        for s in status:
            data.append(s[0])
        print(data)
        if False not in data:
            pytest.exit("AP is Not connected to ucentral gw")
        allure.attach(name=str(status), body="")

    request.addfinalizer(teardown_session)
    yield status


@pytest.fixture(scope="session")
def test_ap_connection_status(fixtures_ver, request, get_configuration, get_apnos):
    """used to check the manager status of AP, should be used as a setup to verify if ap can reach cloud"""
    connection, redirector_value = fixtures_ver.get_ap_status_logs(get_configuration, get_apnos)
    yield connection, redirector_value


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
def create_lanforge_chamberview_dut(lf_tools, skip_lf, run_lf):
    dut_name = ""
    if (not run_lf) and (not skip_lf):
        dut_object, dut_name = lf_tools.Create_Dut()
    return dut_name


@pytest.fixture(scope="session")
def lf_tools(get_configuration, testbed, skip_lf, run_lf, get_ap_version):
    """ Create a DUT on LANforge"""
    if not skip_lf:
        obj = ChamberView(lanforge_data=get_configuration["traffic_generator"]["details"],
                          testbed=testbed, run_lf=run_lf,
                          access_point_data=get_configuration["access_point"], ap_version=get_ap_version)
    else:
        obj = False
    yield obj


@pytest.fixture(scope="session")
def lf_test(get_configuration, setup_influx, request, skip_lf, run_lf, skip_pcap):
    if not skip_lf:
        if request.config.getoption("--exit-on-fail"):
            obj = RunTest(configuration_data=get_configuration, influx_params=setup_influx,
                          debug=True, run_lf=run_lf, skip_pcap=skip_pcap)
        if request.config.getoption("--exit-on-fail") is False:
            obj = RunTest(configuration_data=get_configuration, influx_params=setup_influx,
                          debug=False, run_lf=run_lf, skip_pcap=skip_pcap)
    yield obj


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
def add_env_properties(get_configuration, get_sdk_version, get_apnos, fixtures_ver,
                       add_allure_environment_property: Callable) -> None:
    add_allure_environment_property('Access-Point-Model', get_configuration["access_point"][0]["model"])
    add_allure_environment_property('SDK-Version', get_sdk_version)
    try:
        add_allure_environment_property('Access-Point-Firmware-Version',
                                        fixtures_ver.get_ap_version(get_apnos, get_configuration)[0].split("\n")[1])
    except Exception as e:
        print(e)
        pass
    add_allure_environment_property('Cloud-Controller-SDK-URL', get_configuration["controller"]["url"])
    add_allure_environment_property('AP-Serial-Number', get_configuration["access_point"][0]["serial"] + "\n")


@fixture(scope="session")
def add_firmware_property_after_upgrade(add_allure_environment_property, fixtures_ver, get_apnos,
                                        get_configuration):
    # try:
    add_allure_environment_property('Access-Point-Firmware-Version',
                                    fixtures_ver.get_ap_version(get_apnos, get_configuration)[0].split("\n")[1])
    # except Exception as e:
    #     print(e)
    #     pass


@pytest.fixture(scope="session")
def fixtures_ver(request, get_configuration, run_lf):
    if request.config.getoption("1.x") is False:
        print("2.x")
        obj = Fixtures_2x(configuration=get_configuration, run_lf=run_lf)
    if request.config.getoption("1.x"):
        print("1.x")
        obj = Fixtures_1x(configuration=get_configuration)
    yield obj


@pytest.fixture(scope="session")
def firmware_upgrade(fixtures_ver, get_apnos, get_configuration):
    upgrade_status = fixtures_ver.setup_firmware(get_apnos, get_configuration)
    yield upgrade_status


"""
Logs related Fixtures
"""


@pytest.fixture(scope="function")
def get_ap_logs(request, get_apnos, get_configuration, run_lf):
    if not run_lf:
        S = 9
        instance_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
        for ap in get_configuration['access_point']:
            ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
            ap_ssh.run_generic_command(cmd="logger start testcase: " + instance_name)

        # Adding memory Profile code before every test start
        output = ap_ssh.run_generic_command(cmd="ucode /usr/share/ucentral/sysinfo.uc")
        allure.attach(name="ucode /usr/share/ucentral/sysinfo.uc ", body=str(output))

        def collect_logs():
            for ap in get_configuration['access_point']:
                ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
                ap_ssh.run_generic_command(cmd="logger stop testcase: " + instance_name)
                ap_logs = ap_ssh.get_logread(start_ref="start testcase: " + instance_name,
                                             stop_ref="stop testcase: " + instance_name)
                allure.attach(name='logread', body=str(ap_logs))

            # Adding memory Profile code after every test completion
            output = ap_ssh.run_generic_command(cmd="ucode /usr/share/ucentral/sysinfo.uc")
            allure.attach(name="ucode /usr/share/ucentral/sysinfo.uc ", body=str(output))

        request.addfinalizer(collect_logs)


@pytest.fixture(scope="function")
def get_lf_logs(request, get_apnos, get_configuration):
    ip = get_configuration["traffic_generator"]["details"]["ip"]
    port = get_configuration["traffic_generator"]["details"]["ssh_port"]

    def collect_logs_lf():
        log_0 = "/home/lanforge/lanforge_log_0.txt"
        log_1 = "/home/lanforge/lanforge_log_1.txt"
        obj = SCP_File(ip=ip, port=port, username="root", password="lanforge", remote_path=log_0,
                       local_path=".")
        obj.pull_file()
        allure.attach.file(source="lanforge_log_0.txt",
                           name="lanforge_log_0")
        obj = SCP_File(ip=ip, port=port, username="root", password="lanforge", remote_path=log_1,
                       local_path=".")
        obj.pull_file()
        allure.attach.file(source="lanforge_log_1.txt",
                           name="lanforge_log_1")

    request.addfinalizer(collect_logs_lf)


@pytest.fixture(scope="function")
def get_apnos_logs(get_apnos, get_configuration):
    all_logs = []
    for ap in get_configuration['access_point']:
        ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
        logs = ap_ssh.logread()
        all_logs.append(logs)
    yield all_logs


@pytest.fixture(scope="session")
def get_apnos_max_clients(get_apnos, get_configuration):
    all_logs = []
    for ap in get_configuration['access_point']:
        ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
        ap_ssh.run_generic_command(cmd="chmod +x /usr/share/ucentral/wifi_max_user.uc")
        a = ap_ssh.run_generic_command(cmd="/usr/share/ucentral/wifi_max_user.uc")
        try:
            all_logs.append(a[1])
        except Exception as e:
            pass
    yield all_logs

@pytest.fixture(scope="function")
def get_ap_channel(get_apnos, get_configuration):
    all_data = []
    dict_band_channel = {}
    for ap in get_configuration['access_point']:
        ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
        a = ap_ssh.run_generic_command(cmd="iw dev | grep channel")
        print("ap command output:- ", a)
        try:
            a = a[1:]
            for i in a:
                if i == '':
                    continue
                j = int(re.findall('\d+', i)[0])
                print(j)
                if j >= 36:
                    dict_band_channel["5G"] = j
                    continue
                elif j < 36:
                    dict_band_channel["2G"] = j
                    continue
            if not "2G" in dict_band_channel:
                dict_band_channel["2G"] = "AUTO"
            if not "5G" in dict_band_channel:
                dict_band_channel["5G"] = "AUTO"
            all_data.append(dict_band_channel)
        except Exception as e:
            print(e)
            pass
    print(all_data)
    yield all_data