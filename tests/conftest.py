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
from configuration_data import APNOS_CREDENTIAL_DATA
from configuration_data import RADIUS_SERVER_DATA
from configuration_data import TEST_CASES
from configuration_data import NOLA
from testrail_api import APIClient


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
        help="Stop Upgrading Firmware if already latest"
    )
    # this has to be the last argument
    # example: --access-points ECW5410 EA8300-EU
    parser.addoption(
        "--model",
        # nargs="+",
        default="ecw5410",
        help="AP Model which is needed to test"
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
def instantiate_cloudsdk(testrun_session):
    try:
        sdk_client = CloudSDK(testbed=NOLA[testrun_session]["cloudsdk_url"],
                              customer_id=NOLA[testrun_session]["customer_id"])
    except:
        sdk_client = False
    yield sdk_client


@pytest.fixture(scope="session")
def instantiate_jFrog(request):
    jfrog_cred = {
        "user": request.config.getini("jfrog-user-id"),
        "password": request.config.getini("jfrog-user-password")
    }
    yield jfrog_cred


@pytest.fixture(scope="session")
def instantiate_firmware(instantiate_cloudsdk, instantiate_jFrog):
    try:
        firmware_client = FirmwareUtility(jfrog_credentials=instantiate_jFrog, sdk_client=instantiate_cloudsdk)
    except:
        firmware_client = False
    yield firmware_client


@pytest.fixture(scope="session")
def instantiate_profile(instantiate_cloudsdk):
    try:
        profile_object = ProfileUtility(sdk_client=instantiate_cloudsdk)
    except:
        profile_object = False
    yield profile_object


@pytest.fixture(scope="session")
def instantiate_testrail(request):
    tr_client = APIClient(request.config.getini("tr_url"), request.config.getini("tr_user"),
                          request.config.getini("tr_pass"), request.config.getini("tr_project_id"))
    yield tr_client


@pytest.fixture(scope="session")
def instantiate_project(request, instantiate_testrail, get_equipment_model, get_latest_firmware):
    #(instantiate_testrail)

    projId = instantiate_testrail.get_project_id(project_name=request.config.getini("tr_project_id"))
    test_run_name = request.config.getini("tr_prefix") + get_equipment_model + "_" + str(
        datetime.date.today()) + "_" + get_latest_firmware
    instantiate_testrail.create_testrun(name=test_run_name, case_ids=list(TEST_CASES.values()), project_id=projId,
                                        milestone_id=request.config.getini("milestone"),
                                        description="Automated Nightly Sanity test run for new firmware build")
    rid = instantiate_testrail.get_run_id(
        test_run_name=request.config.getini("tr_prefix") + get_equipment_model + "_" + str(
            datetime.date.today()) + "_" + get_latest_firmware)
    yield rid


"""
Utility Fixtures
"""


@pytest.fixture(scope="session")
def get_equipment_id(testrun_session):
    yield NOLA[testrun_session]["equipment_id"]


@pytest.fixture(scope="session")
def get_latest_firmware(testrun_session, instantiate_firmware):
    try:
        latest_firmware = instantiate_firmware.get_latest_fw_version(testrun_session)
    except:
        latest_firmware = False
    yield latest_firmware


@pytest.fixture(scope="session")
def check_ap_firmware_ssh(request, testrun_session):
    try:
        ap_ssh = APNOS(APNOS_CREDENTIAL_DATA)
        active_fw = ap_ssh.get_active_firmware()
    except Exception as e:
        active_fw = False
    #(active_fw)
    yield active_fw


@pytest.fixture(scope="session")
def check_ap_firmware_cloud(instantiate_cloudsdk, get_equipment_id):
    yield instantiate_cloudsdk.get_ap_firmware_old_method(equipment_id=get_equipment_id)


@pytest.fixture(scope="function")
def get_ap_manager_status():
    ap_ssh = APNOS(APNOS_CREDENTIAL_DATA)
    status = ap_ssh.get_manager_state()
    if "ACTIVE" not in status:
        time.sleep(30)
        ap_ssh = APNOS(APNOS_CREDENTIAL_DATA)
        status = ap_ssh.get_manager_state()
    yield status


@pytest.fixture(scope="session")
def should_upload_firmware(request):
    yield request.config.getini("force-upload")


@pytest.fixture(scope="session")
def should_upgrade_firmware(request):
    yield request.config.getoption("--force-upgrade")


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
def setup_profile_data(testrun_session):
    profile_data = {}
    for mode in "BRIDGE", "NAT", "VLAN":
        profile_data[mode] = {}
        for security in "OPEN", "WPA", "WPA2_P", "WPA2_E":
            profile_data[mode][security] = {}
            for radio in "2G", "5G":
                profile_data[mode][security][radio] = {}
                name_string = "%s-%s-%s_%s_%s" % ("Sanity", testrun_session, radio, security, mode)
                passkey_string = "%s-%s_%s" % (radio, security, mode)
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


"""
Profile Utility
"""


@pytest.fixture(scope="class")
def reset_profile(instantiate_profile):
    instantiate_profile.profile_creation_ids["ssid"] = []
    yield True


@pytest.fixture(scope="function")
def cleanup_cloud_profiles(instantiate_cloudsdk):
    profile_object = ProfileUtility(sdk_client=instantiate_cloudsdk)
    yield profile_object.cleanup_profiles()


@pytest.fixture(scope="session")
def create_radius_profile(instantiate_profile, testrun_session):
    radius_info = {
        "name": testrun_session + "-RADIUS-Sanity",
        "ip": RADIUS_SERVER_DATA["ip"],
        "port": RADIUS_SERVER_DATA["port"],
        "secret": RADIUS_SERVER_DATA["secret"]
    }
    instantiate_profile.delete_profile_by_name(radius_info["name"])
    instantiate_profile.get_default_profiles()
    profile_info = instantiate_profile.create_radius_profile(radius_info=radius_info)
    yield profile_info


@pytest.fixture(scope="session")
def set_rf_profile(instantiate_profile):
    try:
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.set_rf_profile()
    except:
        profile = False
    yield profile

"""
BRIDGE MOde
"""


@pytest.fixture(scope="session")
def create_wpa_ssid_2g_profile_bridge(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["BRIDGE"]['WPA']['2G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa_ssid_profile(profile_data=profile_data, fiveg=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa_ssid_5g_profile_bridge(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["BRIDGE"]['WPA']['5G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa_ssid_profile(profile_data=profile_data, two4g=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa2_p_ssid_2g_profile_bridge(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["BRIDGE"]['WPA2_P']['2G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa2_personal_ssid_profile(profile_data=profile_data, fiveg=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa2_p_ssid_5g_profile_bridge(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["BRIDGE"]['WPA2_P']['5G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa2_personal_ssid_profile(profile_data=profile_data, two4g=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa2_e_ssid_2g_profile_bridge(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["BRIDGE"]['WPA2_E']['2G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa2_enterprise_ssid_profile(profile_data=profile_data, fiveg=False)
    except Exception as e:
        #(e)
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa2_e_ssid_5g_profile_bridge(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["BRIDGE"]['WPA2_E']['5G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa2_enterprise_ssid_profile(profile_data=profile_data, two4g=False)
    except Exception as e:
        #(e)
        profile = False
    yield profile


"""
NAT MOde
"""


@pytest.fixture(scope="session")
def create_wpa_ssid_2g_profile_nat(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["NAT"]['WPA']['2G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa_ssid_profile(profile_data=profile_data, fiveg=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa_ssid_5g_profile_nat(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["NAT"]['WPA']['5G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa_ssid_profile(profile_data=profile_data, two4g=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa2_p_ssid_2g_profile_nat(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["NAT"]['WPA2_P']['2G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa2_personal_ssid_profile(profile_data=profile_data, fiveg=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa2_p_ssid_5g_profile_nat(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["NAT"]['WPA2_P']['5G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa2_personal_ssid_profile(profile_data=profile_data, two4g=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa2_e_ssid_2g_profile_nat(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["NAT"]['WPA2_E']['2G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa2_enterprise_ssid_profile(profile_data=profile_data, fiveg=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa2_e_ssid_5g_profile_nat(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["NAT"]['WPA2_E']['5G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa2_enterprise_ssid_profile(profile_data=profile_data, two4g=False)
    except:
        profile = False
    yield profile


"""
VLAN MOde
"""


@pytest.fixture(scope="session")
def create_wpa_ssid_2g_profile_vlan(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["VLAN"]['WPA']['2G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa_ssid_profile(profile_data=profile_data, fiveg=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa_ssid_5g_profile_vlan(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["VLAN"]['WPA']['5G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa_ssid_profile(profile_data=profile_data, two4g=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa2_p_ssid_2g_profile_vlan(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["VLAN"]['WPA2_P']['2G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa_ssid_profile(profile_data=profile_data, fiveg=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa2_p_ssid_5g_profile_vlan(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["VLAN"]['WPA2_P']['5G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa_ssid_profile(profile_data=profile_data, two4g=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa2_e_ssid_2g_profile_vlan(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["VLAN"]['WPA2_E']['2G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa_ssid_profile(profile_data=profile_data, fiveg=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_wpa2_e_ssid_5g_profile_vlan(instantiate_profile, setup_profile_data):
    try:
        profile_data = setup_profile_data["VLAN"]['WPA2_E']['5G']
        instantiate_profile.get_default_profiles()
        profile = instantiate_profile.create_wpa_ssid_profile(profile_data=profile_data, two4g=False)
    except:
        profile = False
    yield profile


@pytest.fixture(scope="session")
def create_ap_profile_bridge(instantiate_profile, testrun_session):
    profile_data = {
        "profile_name": "%s-%s-%s" % ("Sanity", testrun_session, 'BRIDGE'),
    }
    profile_obj = instantiate_profile.set_ap_profile(profile_data=profile_data)
    yield profile_obj


@pytest.fixture(scope="session")
def create_ap_profile_nat(instantiate_profile, testrun_session):
    profile_data = {
        "profile_name": "%s-%s-%s" % ("Sanity", testrun_session, 'NAT'),
    }
    profile_obj = instantiate_profile.set_ap_profile(profile_data=profile_data)
    yield profile_obj


@pytest.fixture(scope="session")
def create_ap_profile_vlan(instantiate_profile, testrun_session):
    profile_data = {
        "profile_name": "%s-%s-%s" % ("Sanity", testrun_session, 'VLAN'),
    }
    profile_obj = instantiate_profile.set_ap_profile(profile_data=profile_data)
    yield profile_obj


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
