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

from apnos import APNOS
from cloudsdk import CloudSDK
from cloudsdk import ProfileUtility
import pytest
import logging



def pytest_addoption(parser):
    parser.addini("jfrog-base-url", "jfrog base url")
    parser.addini("jfrog-user-id", "jfrog username")
    parser.addini("jfrog-user-password", "jfrog password")

    parser.addini("testbed-name", "cloud sdk base url")

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
    parser.addini("lanforge-radio", "LANforge radio to use")
    parser.addini("lanforge-ethernet-port", "LANforge ethernet adapter to use")

    parser.addini("jumphost_ip", "APNOS Jumphost IP Address")
    parser.addini("jumphost_username", "APNOS Jumphost Username")
    parser.addini("jumphost_password", "APNOS Jumphost password")
    parser.addini("jumphost_port", "APNOS Jumphost ssh Port")

    parser.addini("skip-open", "skip open ssid mode")
    parser.addini("skip-wpa", "skip wpa ssid mode")
    parser.addini("skip-wpa2", "skip wpa2 ssid mode")
    parser.addini("skip-eap", "skip eap ssid mode")
    # change behaviour
    parser.addoption(
        "--skip-update-firmware",
        action="store_true",
        default=False,
        help="skip updating firmware on the AP (useful for local testing)"
    )
    # this has to be the last argument
    # example: --access-points ECW5410 EA8300-EU
    parser.addoption(
        "--access-points",
        # nargs="+",
        default=["ECW5410"],
        help="list of access points to test"
    )


"""
Fixtures for Instantiate the Objects
"""


@pytest.fixture(scope="session")
def instantiate_cloudsdk(request):
    sdk_client = CloudSDK(testbed=request.config.getini("testbed-name"),
                          customer_id=request.config.getini("sdk-customer-id"))
    yield sdk_client


@pytest.fixture(scope="session")
def instantiate_jFrog(request):
    yield "instantiate_jFrog"


"""
Fixtures for Getting Essentials from ini
"""


@pytest.fixture(scope="session")
def get_testbed_name(request):
    yield request.config.getini("testbed-name")


@pytest.fixture(scope="session")
def get_customer_id(request):
    yield request.config.getini("sdk-customer-id")


"""
Fixtures for CloudSDK Utilities
"""


@pytest.fixture(scope="session")
def get_equipment_model(request, instantiate_cloudsdk, get_equipment_id):
    yield request.config.getini("testbed-name")


@pytest.fixture(scope="session")
def get_current_firmware(request, instantiate_cloudsdk, get_equipment_model):
    yield request.config.getini("testbed-name")


def pytest_generate_tests(metafunc):
    if 'access_points' in metafunc.fixturenames:
        metafunc.parametrize("access_points", metafunc.config.getoption('--access-points'), scope="session")


# run something after all tests are done regardless of the outcome
def pytest_unconfigure(config):
    # cleanup or reporting
    print("Tests cleanup done")


"""
Basic CloudSDK inatance Objects
"""


@pytest.fixture(scope="function")
def setup_cloudsdk(request, instantiate_cloudsdk):
    equipment_id = instantiate_cloudsdk.validate_equipment_availability(
        equipment_id=int(request.config.getini("sdk-equipment-id")))
    if equipment_id == -1:
        yield -1
    else:
        yield equipment_id


@pytest.fixture(scope="session")
def update_firmware(request, instantiate_jFrog, instantiate_cloudsdk, retrieve_latest_image, access_points):
    if request.config.getoption("--skip-update-firmware"):
        return
    yield "update_firmware"


@pytest.fixture(scope="session")
def retrieve_latest_image(request, access_points):
    if request.config.getoption("--skip-update-firmware"):
        return
    yield "retrieve_latest_image"


@pytest.fixture(scope="session")
def get_latest_firmware(request, instantiate_cloudsdk, get_equipment_model):
    yield request.config.getini("testbed-name")


@pytest.fixture(scope="function")
def disconnect_cloudsdk(instantiate_cloudsdk):
    instantiate_cloudsdk.disconnect_cloudsdk()


"""
Fixtures to Create Profiles and Push to vif config and delete after the test completion
"""


@pytest.fixture(scope="function")
def setup_bridge_mode(request, instantiate_cloudsdk, create_bridge_profile):
    # vif config and vif state logic here
    logging.basicConfig(level=logging.DEBUG)
    APNOS_CREDENTIAL_DATA = {
        'jumphost_ip': request.config.getini("jumphost_ip"),
        'jumphost_username': request.config.getini("jumphost_username"),
        'jumphost_password': request.config.getini("jumphost_password"),
        'jumphost_port': request.config.getini("jumphost_port")
    }
    obj = APNOS(APNOS_CREDENTIAL_DATA)
    profile_data = []
    for i in create_bridge_profile:
        profile_data.append(i['ssid_name'])
    log = logging.getLogger('test_1')
    vif_config = list(obj.get_vif_config_ssids())
    vif_config.sort()
    vif_state = list(obj.get_vif_state_ssids())
    vif_state.sort()
    profile_data = list(profile_data)
    profile_data.sort()
    for i in range(18):
        print("profiles pushed: ", profile_data)
        print("vif config data: ", vif_config)
        print("vif state data: ", vif_state)
        if profile_data == vif_config:
            print("matched")
            if vif_config == vif_state:
                status = True
                print("matched 1")
                break
            else:
                print("matched 2")
                status = False
        else:
            status = False
        time.sleep(10)
        vif_config = list(obj.get_vif_config_ssids())
        vif_config.sort()
        vif_state = list(obj.get_vif_state_ssids())
        vif_state.sort()
        profile_data = list(profile_data)
        profile_data.sort()

    # request.addfinalizer(delete_profiles(profile_data, instantiate_cloudsdk))
    yield [profile_data, vif_config, vif_state]
    delete_profiles(instantiate_cloudsdk)


@pytest.fixture(scope="function")
def create_bridge_profile(request, instantiate_cloudsdk, setup_profile_data, get_testbed_name):
    print(setup_profile_data)
    # SSID and AP name shall be used as testbed_name and mode
    profile_object = ProfileUtility(sdk_client=instantiate_cloudsdk)
    profile_object.get_default_profiles()
    profile_object.set_rf_profile()
    profile_list = []
    if request.config.getini("skip-open") == 'False':
        profile_data = setup_profile_data['OPEN']['2G']
        profile_object.create_open_ssid_profile(profile_data=profile_data, fiveg=False)
        profile_list.append(profile_data)
        profile_data = setup_profile_data['OPEN']['5G']
        profile_object.create_open_ssid_profile(profile_data=profile_data, two4g=False)
        profile_list.append(profile_data)
    if request.config.getini("skip-wpa") == 'False':
        profile_data = setup_profile_data['WPA']['2G']
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, fiveg=False)
        profile_list.append(profile_data)
        profile_data = setup_profile_data['WPA']['5G']
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, two4g=False)
        profile_list.append(profile_data)
    if request.config.getini("skip-wpa2") == 'False':
        profile_data = setup_profile_data['WPA2']['2G']
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, fiveg=False)
        profile_list.append(profile_data)
        profile_data = setup_profile_data['WPA2']['5G']
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, two4g=False)
        profile_list.append(profile_data)
    if request.config.getini("skip-eap") == 'False':
        radius_info = {
            "name": get_testbed_name + "-RADIUS-Nightly",
            "ip": "192.168.200.75",
            "port": 1812,
            "secret": "testing123"
        }
        # create a eap profile
        pass
    profile_data = {
        "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", 'BRIDGE'),
    }
    profile_object.set_ap_profile(profile_data=profile_data)
    profile_object.push_profile_old_method(equipment_id='13')
    yield profile_list


@pytest.fixture(scope="function")
def setup_nat_mode(request, instantiate_cloudsdk, create_nat_profile):
    # vif config and vif state logic here
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test_1')
    APNOS_CREDENTIAL_DATA = {
        'jumphost_ip': request.config.getini("jumphost_ip"),
        'jumphost_username': request.config.getini("jumphost_username"),
        'jumphost_password': request.config.getini("jumphost_password"),
        'jumphost_port': request.config.getini("jumphost_port")
    }
    obj = APNOS(APNOS_CREDENTIAL_DATA)
    profile_data = []
    for i in create_nat_profile:
        profile_data.append(i['ssid_name'])
    vif_config = list(obj.get_vif_config_ssids())
    vif_config.sort()
    vif_state = list(obj.get_vif_state_ssids())
    vif_state.sort()
    profile_data = list(profile_data)
    profile_data.sort()
    for i in range(18):
        print("profiles pushed: ", profile_data)
        print("vif config data: ", vif_config)
        print("vif state data: ", vif_state)
        if profile_data == vif_config:
            print("matched")
            if vif_config == vif_state:
                status = True
                print("matched 1")
                break
            else:
                print("matched 2")
                status = False
        else:
            status = False
        time.sleep(10)
        vif_config = list(obj.get_vif_config_ssids())
        vif_config.sort()
        vif_state = list(obj.get_vif_state_ssids())
        vif_state.sort()
        profile_data = list(profile_data)
        profile_data.sort()

    # request.addfinalizer(delete_profiles(profile_data, instantiate_cloudsdk))
    yield [profile_data, vif_config, vif_state]
    delete_profiles(instantiate_cloudsdk)


@pytest.fixture(scope="function")
def create_nat_profile(request, instantiate_cloudsdk, setup_profile_data, get_testbed_name):
    print(setup_profile_data)
    # SSID and AP name shall be used as testbed_name and mode
    profile_object = ProfileUtility(sdk_client=instantiate_cloudsdk)
    profile_object.get_default_profiles()
    profile_object.set_rf_profile()
    profile_list = []
    if request.config.getini("skip-open") == 'False':
        profile_data = setup_profile_data['OPEN']['2G']
        profile_object.create_open_ssid_profile(profile_data=profile_data, fiveg=False)
        profile_list.append(profile_data)
        profile_data = setup_profile_data['OPEN']['5G']
        profile_object.create_open_ssid_profile(profile_data=profile_data, two4g=False)
        profile_list.append(profile_data)
    if request.config.getini("skip-wpa") == 'False':
        profile_data = setup_profile_data['WPA']['2G']
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, fiveg=False)
        profile_list.append(profile_data)
        profile_data = setup_profile_data['WPA']['5G']
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, two4g=False)
        profile_list.append(profile_data)
    if request.config.getini("skip-wpa2") == 'False':
        profile_data = setup_profile_data['WPA2']['2G']
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, fiveg=False)
        profile_list.append(profile_data)
        profile_data = setup_profile_data['WPA2']['5G']
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, two4g=False)
        profile_list.append(profile_data)
    if request.config.getini("skip-eap") == 'False':
        radius_info = {
            "name": get_testbed_name + "-RADIUS-Nightly",
            "ip": "192.168.200.75",
            "port": 1812,
            "secret": "testing123"
        }
        # create a eap profile
    profile_data = {
        "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", "NAT")
    }
    profile_object.set_ap_profile(profile_data=profile_data)
    profile_object.push_profile_old_method(equipment_id='13')

    yield profile_list


@pytest.fixture(scope="function")
def setup_vlan_mode(request, instantiate_cloudsdk, create_vlan_profile):
    # vif config and vif state logic here
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test_1')
    APNOS_CREDENTIAL_DATA = {
        'jumphost_ip': request.config.getini("jumphost_ip"),
        'jumphost_username': request.config.getini("jumphost_username"),
        'jumphost_password': request.config.getini("jumphost_password"),
        'jumphost_port': request.config.getini("jumphost_port")
    }
    obj = APNOS(APNOS_CREDENTIAL_DATA)
    profile_data = []
    for i in create_vlan_profile:
        profile_data.append(i['ssid_name'])
    log = logging.getLogger('test_1')
    vif_config = list(obj.get_vif_config_ssids())
    vif_config.sort()
    vif_state = list(obj.get_vif_state_ssids())
    vif_state.sort()
    profile_data = list(profile_data)
    profile_data.sort()
    for i in range(18):
        print("profiles pushed: ", profile_data)
        print("vif config data: ", vif_config)
        print("vif state data: ", vif_state)
        if profile_data == vif_config:
            print("matched")
            if vif_config == vif_state:
                status = True
                print("matched 1")
                break
            else:
                print("matched 2")
                status = False
        else:
            status = False
        time.sleep(10)
        vif_config = list(obj.get_vif_config_ssids())
        vif_config.sort()
        vif_state = list(obj.get_vif_state_ssids())
        vif_state.sort()
        profile_data = list(profile_data)
        profile_data.sort()

    # request.addfinalizer(delete_profiles(profile_data, instantiate_cloudsdk))
    yield [profile_data, vif_config, vif_state]
    delete_profiles(instantiate_cloudsdk)


@pytest.fixture(scope="function")
def create_vlan_profile(request, instantiate_cloudsdk, setup_profile_data, get_testbed_name):
    print(setup_profile_data)
    # SSID and AP name shall be used as testbed_name and mode
    profile_object = ProfileUtility(sdk_client=instantiate_cloudsdk)
    profile_object.get_default_profiles()
    profile_object.set_rf_profile()
    profile_list = []
    if request.config.getini("skip-open") == 'False':
        profile_data = setup_profile_data['OPEN']['2G']
        profile_object.create_open_ssid_profile(profile_data=profile_data, fiveg=False)
        profile_list.append(profile_data)
        profile_data = setup_profile_data['OPEN']['5G']
        profile_object.create_open_ssid_profile(profile_data=profile_data, two4g=False)
        profile_list.append(profile_data)
    if request.config.getini("skip-wpa") == 'False':
        profile_data = setup_profile_data['WPA']['2G']
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, fiveg=False)
        profile_list.append(profile_data)
        profile_data = setup_profile_data['WPA']['5G']
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, two4g=False)
        profile_list.append(profile_data)
    if request.config.getini("skip-wpa2") == 'False':
        profile_data = setup_profile_data['WPA2']['2G']
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, fiveg=False)
        profile_list.append(profile_data)
        profile_data = setup_profile_data['WPA2']['5G']
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, two4g=False)
        profile_list.append(profile_data)
    if request.config.getini("skip-eap") == 'False':
        radius_info = {
            "name": get_testbed_name + "-RADIUS-Nightly",
            "ip": "192.168.200.75",
            "port": 1812,
            "secret": "testing123"
        }
        # create a eap profile
        pass
    profile_data = {
        "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", 'VLAN')
    }
    profile_object.set_ap_profile(profile_data=profile_data)
    profile_object.push_profile_old_method(equipment_id='13')
    yield profile_list


@pytest.fixture(scope="function")
def setup_profile_data(request, get_testbed_name):
    profile_data = {}
    equipment_model = "ecw5410"
    mode = str(request._parent_request.fixturename).split("_")[1].upper()
    if mode == "BRIDGE":
        mode_str = "BR"
        vlan_id = 1
    elif mode == "VLAN":
        mode_str = "VLAN"
        mode = "BRIDGE"
        vlan_id = 100
    else:
        mode_str = mode
        vlan_id = 1
    for security in "OPEN", "WPA", "WPA2", "EAP":
        profile_data[security] = {}
        for radio in "2G", "5G":
            name_string = "%s-%s-%s_%s_%s" % (get_testbed_name, equipment_model, radio, security, mode_str)
            passkey_string = "%s-%s_%s" % (radio, security, mode)
            profile_data[security][radio] = {}
            profile_data[security][radio]["profile_name"] = name_string
            profile_data[security][radio]["ssid_name"] = name_string
            profile_data[security][radio]["mode"] = mode
            profile_data[security][radio]["vlan"] = vlan_id
            if security != "OPEN":
                profile_data[security][radio]["security_key"] = passkey_string
    yield profile_data


def delete_profiles(sdk_client=None):
    profile_object = ProfileUtility(sdk_client=sdk_client)
    profile_object.delete_current_profile(equipment_id=13)
