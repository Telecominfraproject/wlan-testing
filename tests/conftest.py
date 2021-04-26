# import files in the current directory
import datetime
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
        "--model",
        # nargs="+",
        default="ecw5410",
        help="AP Model which is needed to test"
    )
    parser.addoption(
        "--testbed",
        # nargs="+",
        default="lab-info",
        help="AP Model which is needed to test"
    )
    parser.addoption(
        "--skip-testrail",
        action="store_true",
        default=False,
        help="Stop using Testrails"
    )


"""
Test session base fixture
"""


@pytest.fixture(scope="session")
def testbed(request):
    var = request.config.getoption("--testbed")
    yield var


@pytest.fixture(scope="session")
def should_upload_firmware(request):
    yield request.config.getoption("--force-upload")


@pytest.fixture(scope="session")
def should_upgrade_firmware(request):
    yield request.config.getoption("--force-upgrade")


"""
Instantiate Objects for Test session
"""


@pytest.fixture(scope="session")
def instantiate_controller(request, testbed):
    try:
        sdk_client = Controller(controller_data=CONFIGURATION[testbed]["controller"])

        def teardown_session():
            print("\nTest session Completed")
            sdk_client.disconnect_Controller()

        request.addfinalizer(teardown_session)
    except Exception as e:
        print(e)
        sdk_client = False
    yield sdk_client


@pytest.fixture(scope="session")
def instantiate_testrail(request):
    if request.config.getoption("--skip-testrail"):
        tr_client = Reporting()
    else:
        tr_client = APIClient(request.config.getini("tr_url"), request.config.getini("tr_user"),
                              request.config.getini("tr_pass"), request.config.getini("tr_project_id"))
    yield tr_client


@pytest.fixture(scope="session")
def instantiate_firmware(instantiate_controller, instantiate_jFrog, testbed):
    firmware_client = FirmwareUtility(jfrog_credentials=instantiate_jFrog, sdk_client=instantiate_controller,
                                      model=CONFIGURATION[testbed]["access_point"][0]["model"],
                                      version=CONFIGURATION[testbed]["access_point"][0]["version"])
    yield firmware_client


@pytest.fixture(scope="session")
def instantiate_jFrog():
    yield FIRMWARE["JFROG"]


@pytest.fixture(scope="session")
def instantiate_project(request, instantiate_testrail, testbed, get_latest_firmware):
    if request.config.getoption("--skip-testrail"):
        rid = "skip testrails"
    else:
        projId = instantiate_testrail.get_project_id(project_name=request.config.getini("tr_project_id"))
        test_run_name = request.config.getini("tr_prefix") + testbed + "_" + str(
            datetime.date.today()) + "_" + get_latest_firmware
        instantiate_testrail.create_testrun(name=test_run_name, case_ids=list(TEST_CASES.values()), project_id=projId,
                                            milestone_id=request.config.getini("milestone"),
                                            description="Automated Nightly Sanity test run for new firmware build")
        rid = instantiate_testrail.get_run_id(test_run_name=test_run_name)
    yield rid


@pytest.fixture(scope="session")
def setup_lanforge():
    yield True


@pytest.fixture(scope="session")
def setup_perfecto_devices(request):
    yield True


@pytest.fixture(scope="session")
def test_cases():
    yield TEST_CASES


@pytest.fixture(scope="session")
def instantiate_access_point(testbed):
    APNOS(CONFIGURATION[testbed]['access_point'][0], pwd="../libs/apnos/")
    yield True


@pytest.fixture(scope="function")
def test_access_point(testbed, instantiate_access_point):
    ap_ssh = APNOS(CONFIGURATION[testbed]['access_point'][0])
    status = ap_ssh.get_manager_state()
    if "ACTIVE" not in status:
        time.sleep(30)
        ap_ssh = APNOS(CONFIGURATION[testbed]['access_point'][0])
        status = ap_ssh.get_manager_state()
    yield status


@pytest.fixture(scope="session")
def setup_profile_data(testbed):
    model = CONFIGURATION[testbed]["access_point"][0]["model"]
    profile_data = {}
    for mode in "BRIDGE", "NAT", "VLAN":
        profile_data[mode] = {}
        for security in "OPEN", "WPA", "WPA2_P", "WPA2_E", "WEP":
            profile_data[mode][security] = {}
            for radio in "2G", "5G":
                profile_data[mode][security][radio] = {}
                name_string = f"{'Sanity'}-{model}-{radio}_{security}_{mode}"
                passkey_string = f"{radio}-{security}_{mode}"
                profile_data[mode][security][radio]["profile_name"] = name_string
                profile_data[mode][security][radio]["ssid_name"] = name_string
                if mode == "VLAN":
                    profile_data[mode][security][radio]["vlan"] = 100
                else:
                    profile_data[mode][security][radio]["vlan"] = 1
                if mode != "NAT":
                    profile_data[mode][security][radio]["mode"] = "BRIDGE"
                else:
                    profile_data[mode][security][radio]["mode"] = "NAT"
                if security != "OPEN":
                    profile_data[mode][security][radio]["security_key"] = passkey_string
                else:
                    profile_data[mode][security][radio]["security_key"] = "[BLANK]"
    yield profile_data


@pytest.fixture(scope="session")
def get_security_flags():
    security = ["open", "wpa", "wpa2_personal", "wpa2_enterprise", "twog", "fiveg", "radius"]
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
    yield security_dict


@pytest.fixture(scope="session")
def get_latest_firmware(instantiate_firmware):
    # try:
    latest_firmware = instantiate_firmware.get_fw_version()
    # except:
    #     latest_firmware = False
    yield latest_firmware


@pytest.fixture(scope="function")
def check_ap_firmware_ssh(testbed):
    try:
        ap_ssh = APNOS(CONFIGURATION[testbed]['access_point'][0])
        active_fw = ap_ssh.get_active_firmware()
        print(active_fw)
    except Exception as e:
        print(e)
        active_fw = False
    yield active_fw


@pytest.fixture(scope="session")
def radius_info():
    yield RADIUS_SERVER_DATA
