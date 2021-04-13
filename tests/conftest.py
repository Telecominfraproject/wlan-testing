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

if 'cloudsdk' not in sys.path:
    sys.path.append(f'../libs/cloudsdk')
if 'apnos' not in sys.path:
    sys.path.append(f'../libs/apnos')
if 'testrails' not in sys.path:
    sys.path.append(f'../libs/testrails')

from apnos import APNOS
from cloudsdk import CloudSDK
from cloudsdk import ProfileUtility
from cloudsdk import FirmwareUtility
import pytest
import logging
from configuration import APNOS_CREDENTIAL_DATA
from configuration import RADIUS_SERVER_DATA
from configuration import TEST_CASES
from configuration import Controller
from configuration import NOLA
from testrail_api import APIClient
from reporting import Reporting


def pytest_addoption(parser):
    parser.addini("force-upload", "firmware-upload option")

    parser.addini("jfrog-base-url", "jfrog base url")
    parser.addini("jfrog-user-id", "jfrog username")
    parser.addini("jfrog-user-password", "jfrog password")

    parser.addini("testbed-name", "cloud sdk base url")
    parser.addini("equipment-model", "Equipment Model")

    parser.addini("sdk-user-id", "cloud sdk username")
    parser.addini("sdk-user-password", "cloud sdk user password")

    parser.addini("sdk-customer-id", "cloud sdk customer id for the access points")
    parser.addini("sdk-equipment-id", "cloud sdk customer id for the access points")

    parser.addini("testrail-base-url", "testrail base url")
    parser.addini("testrail-project", "testrail project name to use to generate test reports")
    parser.addini("testrail-user-id", "testrail username")
    parser.addini("testrail-user-password", "testrail user password")

    parser.addini("lanforge-ip-address", "LANforge ip address to connect to")
    parser.addini("lanforge-port-number", "LANforge port number to connect to")
    parser.addini("lanforge-bridge-port", "LANforge port for bridge mode testing")
    parser.addini("lanforge-2dot4g-prefix", "LANforge 2.4g prefix")
    parser.addini("lanforge-5g-prefix", "LANforge 5g prefix")
    parser.addini("lanforge-2dot4g-station", "LANforge station name for 2.4g")
    parser.addini("lanforge-5g-station", "LANforge station name for 5g")
    parser.addini("lanforge-2dot4g-radio", "LANforge radio for 2.4g")
    parser.addini("lanforge-5g-radio", "LANforge radio for 5g")

    parser.addini("jumphost_ip", "APNOS Jumphost IP Address")
    parser.addini("jumphost_username", "APNOS Jumphost Username")
    parser.addini("jumphost_password", "APNOS Jumphost password")
    parser.addini("jumphost_port", "APNOS Jumphost ssh Port")

    parser.addini("skip-open", "skip open ssid mode")
    parser.addini("skip-wpa", "skip wpa ssid mode")
    parser.addini("skip-wpa2", "skip wpa2 ssid mode")
    parser.addini("skip-eap", "skip eap ssid mode")

    parser.addini("radius_server_ip", "Radius server IP")
    parser.addini("radius_port", "Radius Port")
    parser.addini("radius_secret", "Radius shared Secret")

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
        "--skip-testrail",
        action="store_true",
        default=False,
        help="Stop using Testrails"
    )


"""
Test session base fixture
"""


@pytest.fixture(scope="session")
def testrun_session(request):
    var = request.config.getoption("model")
    yield var


"""
Instantiate Objects for Test session
"""


@pytest.fixture(scope="session")
def instantiate_cloudsdk(request, testrun_session):
    try:
        sdk_client = CloudSDK(testbed=Controller["url"],
                              customer_id=2)

        def teardown_session():
            print("\nTest session Completed")
            sdk_client.disconnect_cloudsdk()

        request.addfinalizer(teardown_session)
    except Exception as e:
        print(e)
        sdk_client = False
    yield sdk_client


@pytest.fixture(scope="class")
def instantiate_profile(instantiate_cloudsdk):
    try:
        profile_object = ProfileUtility(sdk_client=instantiate_cloudsdk)
    except:
        profile_object = False
    yield profile_object


@pytest.fixture(scope="session")
def instantiate_testrail(request):
    if request.config.getoption("--skip-testrail"):
        tr_client = Reporting()
    else:
        tr_client = APIClient(request.config.getini("tr_url"), request.config.getini("tr_user"),
                              request.config.getini("tr_pass"), request.config.getini("tr_project_id"))
    yield tr_client


@pytest.fixture(scope="session")
def instantiate_firmware(instantiate_cloudsdk, instantiate_jFrog):
    try:
        firmware_client = FirmwareUtility(jfrog_credentials=instantiate_jFrog, sdk_client=instantiate_cloudsdk)
    except:
        firmware_client = False
    yield firmware_client


@pytest.fixture(scope="session")
def instantiate_jFrog(request):
    jfrog_cred = {
        "user": request.config.getini("jfrog-user-id"),
        "password": request.config.getini("jfrog-user-password")
    }
    yield jfrog_cred


@pytest.fixture(scope="session")
def instantiate_project(request, instantiate_testrail, testrun_session, get_latest_firmware):
    if request.config.getoption("--skip-testrail"):
        rid = "skip testrails"
    else:
        projId = instantiate_testrail.get_project_id(project_name=request.config.getini("tr_project_id"))
        test_run_name = request.config.getini("tr_prefix") + testrun_session + "_" + str(
            datetime.date.today()) + "_" + get_latest_firmware
        instantiate_testrail.create_testrun(name=test_run_name, case_ids=list(TEST_CASES.values()), project_id=projId,
                                            milestone_id=request.config.getini("milestone"),
                                            description="Automated Nightly Sanity test run for new firmware build")
        rid = instantiate_testrail.get_run_id(
            test_run_name=request.config.getini("tr_prefix") + testrun_session + "_" + str(
                datetime.date.today()) + "_" + get_latest_firmware)
    yield rid


@pytest.fixture(scope="session")
def setup_lanforge(request):
    yield True


@pytest.fixture(scope="session")
def setup_perfecto_devices(request):
    yield True


@pytest.fixture(scope="session")
def setup_profile_data(testrun_session):
    profile_data = {}
    for mode in "BRIDGE", "NAT", "VLAN":
        profile_data[mode] = {}
        for security in "OPEN", "WPA", "WPA2_P", "WPA2_E", "WEP":
            profile_data[mode][security] = {}
            for radio in "2G", "5G":
                profile_data[mode][security][radio] = {}
                name_string = f"{'Sanity'}-{testrun_session}-{radio}_{security}_{mode}"
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
    print(set(markers))
    for i in security:
        if set(markers).__contains__(i):
            security_dict[i] = True
        else:
            security_dict[i] = False
    print(security_dict)
    yield security_dict


@pytest.fixture(scope="session")
def get_equipment_id(testrun_session):
    yield NOLA[testrun_session]["equipment_id"]


@pytest.fixture(scope="class")
def get_current_profile_cloud(instantiate_profile):
    ssid_names = []
    print(instantiate_profile.profile_creation_ids["ssid"])
    for i in instantiate_profile.profile_creation_ids["ssid"]:
        ssid_names.append(instantiate_profile.get_ssid_name_by_profile_id(profile_id=i))
    yield ssid_names


@pytest.fixture(scope="class")
def setup_profiles(create_profiles, instantiate_profile, get_equipment_id, get_current_profile_cloud):
    instantiate_profile.push_profile_old_method(equipment_id=get_equipment_id)
    print(create_profiles)
    ap_ssh = APNOS(APNOS_CREDENTIAL_DATA)
    get_current_profile_cloud.sort()
    for i in range(0, 18):
        vif_config = list(ap_ssh.get_vif_config_ssids())
        vif_config.sort()
        print(vif_config)
        print(get_current_profile_cloud)
        if get_current_profile_cloud == vif_config:
            break
        time.sleep(10)
    ap_ssh = APNOS(APNOS_CREDENTIAL_DATA)
    for i in range(0, 18):
        vif_state = list(ap_ssh.get_vif_state_ssids())
        vif_state.sort()
        vif_config = list(ap_ssh.get_vif_config_ssids())
        vif_config.sort()
        print(vif_config)
        print(vif_state)
        if vif_state == vif_config:
            break
        time.sleep(10)
    yield "set(markers)"


@pytest.fixture(scope="class")
def create_profiles(request, get_security_flags, get_markers, instantiate_profile, setup_profile_data):
    profile_id = {"ssid": [], "rf": None, "radius": None, "equipment_ap": None}
    mode = str(request._parent_request.param)
    instantiate_profile.delete_profile_by_name(profile_name="Equipment-AP-" + mode)
    for i in setup_profile_data[mode]:
        for j in setup_profile_data[mode][i]:
            instantiate_profile.delete_profile_by_name(
                profile_name=setup_profile_data[mode][i][j]['profile_name'])
    instantiate_profile.delete_profile_by_name(profile_name="Automation-Radius-Profile-" + mode)
    instantiate_profile.get_default_profiles()
    # if get_markers["wifi5"]:
    #     # Create Radius Profile
    #     pass
    # if get_markers["wifi6"]:
    #     # Create Radius Profile
    #     pass

    # Create RF Profile Here
    instantiate_profile.set_rf_profile()
    if get_markers["radius"]:
        radius_info = RADIUS_SERVER_DATA
        radius_info["name"] = "Automation-Radius-Profile-" + mode
        instantiate_profile.create_radius_profile(radius_info=radius_info)
    for i in get_security_flags:
        if get_markers[i] and i == "open":
            if get_markers["twog"]:
                profile_data = setup_profile_data[mode]["OPEN"]["2G"]
                id = instantiate_profile.create_open_ssid_profile(two4g=True, fiveg=False, profile_data=profile_data)
                profile_id["ssid"].append(profile_data['ssid_name'])
            if get_markers["fiveg"]:
                profile_data = setup_profile_data[mode]["OPEN"]["5G"]
                id = instantiate_profile.create_open_ssid_profile(two4g=False, fiveg=True, profile_data=profile_data)
                profile_id["ssid"].append(profile_data['ssid_name'])
        if get_markers[i] and i == "wpa":
            if get_markers["twog"]:
                profile_data = setup_profile_data[mode]["WPA"]["2G"]
                id = instantiate_profile.create_wpa_ssid_profile(two4g=True, fiveg=False, profile_data=profile_data)
                profile_id["ssid"].append(profile_data['ssid_name'])
            if get_markers["fiveg"]:
                profile_data = setup_profile_data[mode]["WPA"]["5G"]
                id = instantiate_profile.create_wpa_ssid_profile(two4g=False, fiveg=True, profile_data=profile_data)
                profile_id["ssid"].append(profile_data['ssid_name'])
        if get_markers[i] and i == "wpa2_personal":
            if get_markers["twog"]:
                profile_data = setup_profile_data[mode]["WPA2_P"]["2G"]
                id = instantiate_profile.create_wpa2_personal_ssid_profile(two4g=True, fiveg=False,
                                                                           profile_data=profile_data)
                profile_id["ssid"].append(profile_data['ssid_name'])
            if get_markers["fiveg"]:
                profile_data = setup_profile_data[mode]["WPA2_P"]["5G"]
                id = instantiate_profile.create_wpa2_personal_ssid_profile(two4g=False, fiveg=True,
                                                                           profile_data=profile_data)
                profile_id["ssid"].append(profile_data['ssid_name'])
        if get_markers[i] and i == "wpa2_enterprise":
            if get_markers["twog"]:
                profile_data = setup_profile_data[mode]["WPA2_E"]["2G"]
                id = instantiate_profile.create_wpa2_enterprise_ssid_profile(two4g=True, fiveg=False,
                                                                             profile_data=profile_data)
                profile_id["ssid"].append(profile_data['ssid_name'])
            if get_markers["fiveg"]:
                profile_data = setup_profile_data[mode]["WPA2_E"]["5G"]
                id = instantiate_profile.create_wpa2_enterprise_ssid_profile(two4g=False, fiveg=True,
                                                                             profile_data=profile_data)
                profile_id["ssid"].append(profile_data['ssid_name'])

    # Create Equipment AP Profile Here
    profile_data = {
        "profile_name": "Equipment-AP-" + mode
    }
    instantiate_profile.set_ap_profile(profile_data=profile_data)
    yield profile_id


@pytest.fixture(scope="function")
def get_lanforge_data(request):
    lanforge_data = {
        "lanforge_ip": request.config.getini("lanforge-ip-address"),
        "lanforge-port-number": request.config.getini("lanforge-port-number"),
        "lanforge_2dot4g": request.config.getini("lanforge-2dot4g-radio"),
        "lanforge_5g": request.config.getini("lanforge-5g-radio"),
        "lanforge_2dot4g_prefix": request.config.getini("lanforge-2dot4g-prefix"),
        "lanforge_5g_prefix": request.config.getini("lanforge-5g-prefix"),
        "lanforge_2dot4g_station": request.config.getini("lanforge-2dot4g-station"),
        "lanforge_5g_station": request.config.getini("lanforge-5g-station"),
        "lanforge_bridge_port": request.config.getini("lanforge-bridge-port"),
        "lanforge_vlan_port": "eth1.100",
        "vlan": 100
    }
    yield lanforge_data


@pytest.fixture(scope="session")
def get_latest_firmware(testrun_session, instantiate_firmware):
    try:
        latest_firmware = instantiate_firmware.get_latest_fw_version(testrun_session)
    except:
        latest_firmware = False
    yield latest_firmware


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


