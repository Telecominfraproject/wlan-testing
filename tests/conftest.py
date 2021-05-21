# import files in the current directory
import datetime
import sys
import os
import time
import allure

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
<<<<<<< HEAD
from cv_test_manager import cv_test
=======
import sta_connect2
from sta_connect2 import StaConnect2

>>>>>>> staging-wifi-1960

def pytest_addoption(parser):
    parser.addini("tr_url", "Test Rail URL")
    parser.addini("tr_prefix", "Test Rail Prefix (Generally Testbed_name_)")
    parser.addini("tr_user", "Testrail Username")
    parser.addini("tr_pass", "Testrail Password")
    parser.addini("tr_project_id", "Testrail Project ID")
    parser.addini("milestone", "milestone Id")

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
    parser.addoption(
        "--exit-on-fail",
        action="store_true",
        default=False,
        help="use to stop execution if failure"
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
    parser.addini("wifi-SSID-5gl-Pwd", "Wifi 5g Password")
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
    yield TEST_CASES


@pytest.fixture(scope="session")
def instantiate_jFrog():
    yield FIRMWARE["JFROG"]


@pytest.fixture(scope="session")
def testbed(request):
    var = request.config.getoption("--testbed")
    allure.attach(body=str(var),
                  name="Testbed Selected : ")
    yield var


@pytest.fixture(scope="session")
def should_upload_firmware(request):
    yield request.config.getoption("--force-upload")


@pytest.fixture(scope="session")
def should_upgrade_firmware(request):
    yield request.config.getoption("--force-upgrade")


@pytest.fixture(scope="session")
def radius_info():
    allure.attach(body=str(RADIUS_SERVER_DATA), name="Radius server Info: ")
    yield RADIUS_SERVER_DATA


# Get Configuration data f
@pytest.fixture(scope="session")
def get_configuration(testbed):
    allure.attach(body=str(testbed), name="Testbed Selected: ")
    yield CONFIGURATION[testbed]


# APNOS Library
@pytest.fixture(scope="session")
def get_apnos():
    yield APNOS


@pytest.fixture(scope="session")
def get_equipment_id(setup_controller, testbed, get_configuration):
    equipment_id_list = []
    for i in get_configuration['access_point']:
        equipment_id_list.append(setup_controller.get_equipment_id(
            serial_number=i['serial']))
    yield equipment_id_list


# APNOS SETUP
@pytest.fixture(scope="session")
def instantiate_access_point(testbed, get_apnos, get_configuration):
    # Used to add openwrtctl.py in case of serial console mode
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
def setup_controller(request, get_configuration, instantiate_access_point):
    try:
        sdk_client = Controller(controller_data=get_configuration["controller"])
        allure.attach(body=str(get_configuration["controller"]), name="Controller Instantiated: ")

        def teardown_controller():
            print("\nTest session Completed")
            allure.attach(body=str(get_configuration["controller"]), name="Controller Teardown: ")
            sdk_client.disconnect_Controller()

        request.addfinalizer(teardown_controller)
    except Exception as e:
        print(e)
        allure.attach(body=str(e), name="Controller Instantiation Failed: ")
        sdk_client = False
    yield sdk_client


@pytest.fixture(scope="class")
def instantiate_firmware(setup_controller, instantiate_jFrog, get_configuration):
    firmware_client_obj = []
    for access_point_info in get_configuration['access_point']:
        firmware_client = FirmwareUtility(jfrog_credentials=instantiate_jFrog, sdk_client=setup_controller,
                                          model=access_point_info["model"],
                                          version=access_point_info["version"])
        firmware_client_obj.append(firmware_client)
    yield firmware_client_obj


@pytest.fixture(scope="class")
def get_latest_firmware(instantiate_firmware):
    fw_version_list = []
    try:

        for fw_obj in instantiate_firmware:
            latest_firmware = fw_obj.get_fw_version()
            fw_version_list.append(latest_firmware)
    except Exception as e:
        print(e)
        fw_version_list = []

    yield fw_version_list


@pytest.fixture(scope="class")
def upload_firmware(should_upload_firmware, instantiate_firmware, get_latest_firmware):
    firmware_id_list = []
    for i in range(0, len(instantiate_firmware)):
        firmware_id = instantiate_firmware[i].upload_fw_on_cloud(fw_version=get_latest_firmware[i],
                                                                 force_upload=should_upload_firmware)
        firmware_id_list.append(firmware_id)
    yield firmware_id_list


@pytest.fixture(scope="class")
def upgrade_firmware(request, instantiate_firmware, get_equipment_id, check_ap_firmware_cloud, get_latest_firmware,
                     should_upgrade_firmware):
    status_list = []
    if get_latest_firmware != check_ap_firmware_cloud:
        if request.config.getoption("--skip-upgrade"):
            status = "skip-upgrade"
            status_list.append(status)
        else:

            for i in range(0, len(instantiate_firmware)):
                status = instantiate_firmware[i].upgrade_fw(equipment_id=get_equipment_id, force_upload=False,
                                                            force_upgrade=should_upgrade_firmware)
                status_list.append(status)
    else:
        if should_upgrade_firmware:
            for i in range(0, len(instantiate_firmware)):
                status = instantiate_firmware[i].upgrade_fw(equipment_id=get_equipment_id, force_upload=False,
                                                            force_upgrade=should_upgrade_firmware)
                status_list.append(status)
        else:
            status = "skip-upgrade Version Already Available"
            status_list.append(status)
    yield status_list


@pytest.fixture(scope="class")
def check_ap_firmware_cloud(setup_controller, get_equipment_id):
    ap_fw_list = []
    for i in get_equipment_id:
        ap_fw_list.append(setup_controller.get_ap_firmware_old_method(equipment_id=i))
    yield ap_fw_list


@pytest.fixture(scope="class")
def check_ap_firmware_ssh(get_configuration):
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


"""
Instantiate Reporting
"""


@pytest.fixture(scope="session")
def update_report(request, testbed, get_configuration):
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
<<<<<<< HEAD
            datetime.date.today()) + "_" + get_latest_firmware
        instantiate_testrail.create_testrun(name=test_run_name, case_ids=list(TEST_CASES.values()), project_id=projId,
                                            milestone_id=request.config.getini("milestone"),
                                            description="Automated Nightly Sanity test run for new firmware build")
        rid = instantiate_testrail.get_run_id(test_run_name=test_run_name)
    yield rid


@pytest.fixture(scope="session")
def check_lanforge_connectivity(testbed):
    lanforge_ip = CONFIGURATION[testbed]['traffic_generator']['details']['ip']
    lanforge_port = CONFIGURATION[testbed]['traffic_generator']['details']['port']

    try:
        cv = cv_test(lanforge_ip,lanforge_port)
        url_data = cv.get_ports("/")
        lanforge_GUI_version = url_data["VersionInfo"]["BuildVersion"]
        lanforge_gui_git_version = url_data["VersionInfo"]["GitVersion"]
        lanforge_gui_build_date = url_data["VersionInfo"]["BuildDate"]
        print(lanforge_GUI_version,lanforge_gui_build_date,lanforge_gui_git_version)
        if not (lanforge_GUI_version or lanforge_gui_build_date or lanforge_gui_git_version):
            yield False
        else:
            yield True
    except:
        yield False


@pytest.fixture(scope="session")
def exit_on_fail(request):
    yield request.config.getoption("--exit-on-fail")


@pytest.fixture(scope="session")
def setup_perfecto_devices(request):
    yield True


@pytest.fixture(scope="session")
def test_cases():
    yield TEST_CASES


@pytest.fixture(scope="session")
def apnos_obj(get_configuration, testbed):
    yield APNOS(get_configuration[testbed]['access_point'][0])


@pytest.fixture(scope="session")
def instantiate_access_point(testbed):
    APNOS(CONFIGURATION[testbed]['access_point'][0], pwd="../libs/apnos/")
    yield True


@pytest.fixture(scope="function")
def access_point_connectivity(apnos_obj, get_configuration, testbed):
    ap_conn = {}
    config_serial = get_configuration[testbed]['access_point'][0]['serial']
    ap_serial = apnos_obj.get_serial_number()
    ap_conn["serial"] = True
    if ap_serial != config_serial:
        ap_conn["serial"] = False

    ap_conn["redir"] = False
    ap_redir = apnos_obj.get_redirector()

    # Compare with something ...

    ap_conn["mgr"] = False
    status = apnos_obj.get_manager_state()
    if "ACTIVE" not in status:
        apnos_obj.run_generic_command(cmd="service opensync restart")
        time.sleep(30)
        status = apnos_obj.get_manager_state()
        if "ACTIVE" in status:
            ap_conn["mgr"] = True
    else:
        ap_conn["mgr"] = True
    yield ap_conn
=======
            datetime.date.today()) + "_" + get_configuration['access_point'][0]['version']
        tr_client.create_testrun(name=test_run_name, case_ids=list(TEST_CASES.values()), project_id=projId,
                                 milestone_id=request.config.getini("milestone"),
                                 description="Automated Nightly Sanity test run for new firmware build")
        rid = tr_client.get_run_id(test_run_name=test_run_name)
        tr_client.rid = rid
    yield tr_client

>>>>>>> staging-wifi-1960

"""
FRAMEWORK MARKER LOGIC

"""


@pytest.fixture(scope="session")
def get_security_flags():
    # Add more classifications as we go
    security = ["open", "wpa", "wpa2_personal", "wpa3_personal", "wpa3_personal_mixed",
                "wpa2_enterprise", "wpa3_enterprise", "twog", "fiveg", "radius"]
    yield security


@pytest.fixture(scope="session")
def get_markers(request, get_security_flags):
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
@pytest.fixture(scope="function")
def test_access_point(testbed, get_apnos, get_configuration):
    mgr_status = []
    for access_point_info in get_configuration['access_point']:
        ap_ssh = get_apnos(access_point_info)
        ap_ssh.reboot()
        time.sleep(100)
        status = ap_ssh.get_manager_state()
        if "ACTIVE" not in status:
            time.sleep(30)
            ap_ssh = APNOS(access_point_info)
            status = ap_ssh.get_manager_state()
        mgr_status.append(status)
    yield mgr_status


@pytest.fixture(scope="session")
def client_connectivity():
    yield StaConnect2


@pytest.fixture(scope="session")
<<<<<<< HEAD
def radius_info():
    yield RADIUS_SERVER_DATA


@pytest.fixture(scope="session")
def get_configuration(testbed):
    yield CONFIGURATION[testbed]
=======
def get_lanforge_data(get_configuration):
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
>>>>>>> staging-wifi-1960
