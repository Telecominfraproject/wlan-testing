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
from configuration_data import PROFILE_DATA


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


@pytest.fixture(scope="function")
def setup_bridge_mode(request, instantiate_cloudsdk, setup_profile_data, create_bridge_profile):
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
    profile_data = create_bridge_profile
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

    def delete_profile(profile_data, sdk_client):
        print(f"Cloud SDK cleanup for {request.node.originalname}, {profile_data}")
        delete_profiles(profile_names=profile_data, sdk_client=sdk_client)
    request.addfinalizer(delete_profile(profile_data, instantiate_cloudsdk))
    yield [profile_data, vif_config, vif_state]

@pytest.fixture(scope="function")
def setup_profile_data(request):
    # logic to setup bridge mode ssid and parameters
    yield True


@pytest.fixture(scope="function")
def create_bridge_profile(request, instantiate_cloudsdk, get_testbed_name):
    # SSID and AP name shall be used as testbed_name and mode
    profile_object = ProfileUtility(sdk_client=instantiate_cloudsdk)
    profile_object.get_default_profiles()
    profile_object.set_rf_profile()
    ssid_list = []
    if request.config.getini("skip-open") == 'False':
        profile_data = {
            "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '2G_O_BR'),
            "ssid_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '2G_O_BR'),
            "mode": "BRIDGE"
        }
        profile_object.create_open_ssid_profile(profile_data=profile_data, fiveg=False)
        ssid_list.append(profile_data["profile_name"])
        profile_data = {
            "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '5G_O_BR'),
            "ssid_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '5G_O_BR'),
            "mode": "BRIDGE"
        }
        profile_object.create_open_ssid_profile(profile_data=profile_data, two4g=False)
        ssid_list.append(profile_data["profile_name"])
        # Create an open ssid profile
    if request.config.getini("skip-wpa") == 'False':
        profile_data = {
            "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '2G_WPA_BR'),
            "ssid_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '2G_WPA_BR'),
            "mode": "BRIDGE",
            "security_key": "%s-%s" % ("ecw5410", "2G_WPA_BR")
        }
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, fiveg=False)
        ssid_list.append(profile_data["profile_name"])
        profile_data = {
            "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '5G_WPA_BR'),
            "ssid_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '5G_WPA_BR'),
            "mode": "BRIDGE",
            "security_key": "%s-%s" % ("ecw5410", "5G_WPA_BR")
        }
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, two4g=False)
        ssid_list.append(profile_data["profile_name"])
        # Create a wpa profile
        pass
    if request.config.getini("skip-wpa2") == 'False':
        profile_data = {
            "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '5G_WPA2_BR'),
            "ssid_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '5G_WPA2_BR'),
            "mode": "BRIDGE",
            "security_key": "%s-%s" % ("ecw5410", "5G_WPA2_BR")
        }
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, fiveg=False)
        ssid_list.append(profile_data["profile_name"])
        profile_data = {
            "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '2G_WPA2_BR'),
            "ssid_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '2G_WPA2_BR'),
            "mode": "BRIDGE",
            "security_key": "%s-%s" % ("ecw5410", "2G_WPA2_BR")
        }
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, two4g=False)
        ssid_list.append(profile_data["profile_name"])
        # Create a wpa2 profile
        pass
    if request.config.getini("skip-eap") == 'False':
        radius_info = {
            "name": request.config.getini("testbed-name") + "-RADIUS-Nightly",
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

    # create an equipment ap profile
    yield ssid_list


@pytest.fixture(scope="function")
def setup_nat_profile(request, instantiate_cloudsdk, get_testbed_name):
    # SSID and AP name shall be used as testbed_name and mode
    profile_object = ProfileUtility(sdk_client=instantiate_cloudsdk)
    profile_object.get_default_profiles()
    profile_object.set_rf_profile()
    if request.config.getini("skip-open") == 'False':
        profile_data = {
            "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '2G_O_NAT'),
            "ssid_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '2G_O_NAT'),
            "mode": "NAT"
        }
        profile_object.create_open_ssid_profile(profile_data=profile_data, fiveg=False)
        profile_data = {
            "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '5G_O_NAT'),
            "ssid_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '5G_O_NAT'),
            "mode": "NAT"
        }
        profile_object.create_open_ssid_profile(profile_data=profile_data, two4g=False)
        # Create an open ssid profile
    if request.config.getini("skip-wpa") == 'False':
        profile_data = {
            "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '2G_WPA_NAT'),
            "ssid_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '2G_WPA_NAT'),
            "mode": "NAT",
            "security_key": "%s-%s" % ("ecw5410", "2G_WPA_NAT")
        }
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, fiveg=False)
        profile_data = {
            "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '5G_WPA_NAT'),
            "ssid_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '5G_WPA_NAT'),
            "mode": "NAT",
            "security_key": "%s-%s" % ("ecw5410", "5G_WPA_NAT")
        }
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, two4g=False)
        # Create a wpa profile
        pass
    if request.config.getini("skip-wpa2") == 'False':
        profile_data = {
            "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '5G_WPA2_NAT'),
            "ssid_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '5G_WPA2_NAT'),
            "mode": "NAT",
            "security_key": "%s-%s" % ("ecw5410", "5G_WPA2_NAT")
        }
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, fiveg=False)
        profile_data = {
            "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '2G_WPA2_NAT'),
            "ssid_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", '2G_WPA2_NAT'),
            "mode": "NAT",
            "security_key": "%s-%s" % ("ecw5410", "2G_WPA2_NAT")
        }
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, two4g=False)
        # Create a wpa2 profile
        pass
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
        "profile_name": "%s-%s-%s" % (get_testbed_name, "ecw5410", 'NAT'),
    }
    profile_object.set_ap_profile(profile_data=profile_data)
    profile_object.push_profile_old_method(equipment_id='13')
    # create an equipment ap profile
    yield profile_object


@pytest.fixture(scope="function")
def setup_vlan_profile(request, instantiate_cloudsdk):
    # SSID and AP name shall be used as testbed_name and mode
    profile_object = ProfileUtility(sdk_client=instantiate_cloudsdk)
    # profile_object.select_rf_profile(profile_data=None)
    if request.config.getini("skip-open") is False:
        # Create an open ssid profile
        pass
    if request.config.getini("skip-wpa") is False:
        # Create a wpa profile
        pass
    if request.config.getini("skip-wpa2") is False:
        # Create a wpa2 profile
        pass
    if request.config.getini("skip-eap") is False:
        # create a radius profile
        # create a eap profile
        pass
    # create an equipment ap profile
    yield profile_object


@pytest.fixture(scope="function")
def apply_default_profile(instantiate_cloudsdk):
    profile_object = ProfileUtility(sdk_client=instantiate_cloudsdk)
    profile_object.get_default_profiles()
    profile_object.profile_creation_ids['ap'] = profile_object.default_profiles['equipment_ap_3_radios']
    profile_object.push_profile_old_method(equipment_id='13')


def delete_profiles(profile_names, sdk_client=None):
    profile_object = ProfileUtility(sdk_client=sdk_client)
    profile_object.get_default_profiles()
    profile_object.profile_creation_ids['ap'] = profile_object.default_profiles['equipment_ap_3_radios']
    profile_object.push_profile_old_method()
