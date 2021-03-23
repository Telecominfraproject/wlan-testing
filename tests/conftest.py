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
from cloudsdk import FirmwareUtility
import pytest
import logging


def pytest_addoption(parser):
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
    # change behaviour
    parser.addoption(
        "--skip-update-firmware",
        action="store_true",
        default=True,
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
    jfrog_cred = {
        "user": request.config.getini("jfrog-user-id"),
        "password": request.config.getini("jfrog-user-password")
    }
    yield jfrog_cred


"""
Fixtures for Getting Essentials from ini
"""


@pytest.fixture(scope="session")
def get_testbed_name(request):
    yield request.config.getini("testbed-name")


@pytest.fixture(scope="session")
def get_customer_id(request):
    yield request.config.getini("sdk-customer-id")


@pytest.fixture(scope="session")
def get_equipment_id(request):
    yield request.config.getini("sdk-equipment-id")


"""
Fixtures for CloudSDK Utilities
"""


@pytest.fixture(scope="session")
def get_equipment_model(request, instantiate_cloudsdk, get_equipment_id):
    yield request.config.getini("equipment-model")


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
def upgrade_firmware(request, instantiate_jFrog, instantiate_cloudsdk, get_equipment_id):
    if request.config.getoption("--skip-update-firmware"):
        obj = FirmwareUtility(jfrog_credentials=instantiate_jFrog, sdk_client=instantiate_cloudsdk)
        status = obj.upgrade_fw(equipment_id=get_equipment_id, force_upload=False, force_upgrade=False)
    else:
        status = "skip-upgrade"
    yield status


# @pytest.fixture(scope="session")
# def retrieve_latest_image(request, access_points):
#     if request.config.getoption("--skip-update-firmware"):
#         yield True
#     yield True


@pytest.fixture(scope="session")
def get_latest_firmware(request, instantiate_cloudsdk, get_equipment_model):
    yield request.config.getini("testbed-name")


@pytest.fixture(scope="function")
def disconnect_cloudsdk(instantiate_cloudsdk):
    instantiate_cloudsdk.disconnect_cloudsdk()


"""
Fixtures to Create Profiles and Push to vif config and delete after the test completion
"""


@pytest.fixture(scope="class")
def setup_bridge_mode(request, instantiate_cloudsdk, create_bridge_profile, get_equipment_id):
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
        for j in create_bridge_profile[i]:
            if create_bridge_profile[i][j] != {}:
                profile_data.append(create_bridge_profile[i][j]['ssid_name'])
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

    yield [profile_data, vif_config, vif_state, create_bridge_profile]
    delete_profiles(instantiate_cloudsdk, get_equipment_id)


@pytest.fixture(scope="class")
def create_bridge_profile(request, instantiate_cloudsdk, setup_bridge_profile_data, get_testbed_name, get_equipment_id,
                          get_equipment_model,
                          get_bridge_testcases):
    print(setup_bridge_profile_data)
    # SSID and AP name shall be used as testbed_name and mode
    profile_object = ProfileUtility(sdk_client=instantiate_cloudsdk)
    profile_object.get_default_profiles()
    profile_object.set_rf_profile()
    profile_list = {"open": {"2g": {}, "5g": {}}, "wpa": {"2g": {}, "5g": {}}, "wpa2_personal": {"2g": {}, "5g": {}},
                    "wpa2_enterprise": {"2g": {}, "5g": {}}}

    if get_bridge_testcases["open_2g"]:

        profile_data = setup_bridge_profile_data['OPEN']['2G']
        profile_list["open"]["2g"] = profile_data
        profile_object.create_open_ssid_profile(profile_data=profile_data, fiveg=False)
    if get_bridge_testcases["open_5g"]:

        profile_data = setup_bridge_profile_data['OPEN']['5G']
        profile_list["open"]["5g"] = profile_data
        profile_object.create_open_ssid_profile(profile_data=profile_data, two4g=False)

    if get_bridge_testcases["wpa_2g"]:

        profile_data = setup_bridge_profile_data['WPA']['2G']
        profile_list["wpa"]["2g"] = profile_data
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, fiveg=False)

    if get_bridge_testcases["wpa_5g"]:

        profile_data = setup_bridge_profile_data['WPA']['5G']
        profile_list["wpa"]["5g"] = profile_data
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, two4g=False)

    if get_bridge_testcases["wpa2_personal_2g"]:

        profile_data = setup_bridge_profile_data['WPA2']['2G']
        profile_list["wpa2_personal"]["2g"] = profile_data
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, fiveg=False)

    if get_bridge_testcases["wpa2_personal_5g"]:

        profile_data = setup_bridge_profile_data['WPA2']['5G']
        profile_list["wpa2_personal"]["5g"] = profile_data
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, two4g=False)

    if get_bridge_testcases["wpa2_enterprise_2g"] or get_bridge_testcases["wpa2_enterprise_5g"]:
        radius_info = {
            "name": get_testbed_name + "-RADIUS-Sanity",
            "ip": request.config.getini("radius_server_ip"),
            "port": request.config.getini("radius_port"),
            "secret": request.config.getini("radius_secret")
        }
        profile_object.create_radius_profile(radius_info=radius_info)

    if get_bridge_testcases["wpa2_enterprise_2g"]:

        profile_data = setup_bridge_profile_data['EAP']['2G']
        profile_list["wpa2_enterprise"]["2g"] = profile_data
        profile_object.create_wpa2_enterprise_ssid_profile(profile_data=profile_data, fiveg=False)

    if get_bridge_testcases["wpa2_enterprise_5g"]:

        profile_data = setup_bridge_profile_data['EAP']['5G']
        profile_list["wpa2_enterprise"]["5g"] = profile_data
        profile_object.create_wpa2_enterprise_ssid_profile(profile_data=profile_data, two4g=False)

    profile_data = {
        "profile_name": "%s-%s-%s" % (get_testbed_name, get_equipment_model, 'BRIDGE'),
    }
    profile_object.set_ap_profile(profile_data=profile_data)
    profile_object.push_profile_old_method(equipment_id=get_equipment_id)
    yield profile_list


@pytest.fixture(scope="class")
def setup_nat_mode(request, instantiate_cloudsdk, create_nat_profile, get_equipment_id):
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
        for j in create_nat_profile[i]:
            if create_nat_profile[i][j] != {}:
                profile_data.append(create_nat_profile[i][j]['ssid_name'])
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

    yield [profile_data, vif_config, vif_state, create_nat_profile]
    delete_profiles(instantiate_cloudsdk, get_equipment_id)


@pytest.fixture(scope="class")
def create_nat_profile(request, instantiate_cloudsdk, setup_nat_profile_data, get_testbed_name, get_equipment_id,
                       get_nat_testcases, get_equipment_model):
    print(setup_nat_profile_data)
    # SSID and AP name shall be used as testbed_name and mode
    profile_object = ProfileUtility(sdk_client=instantiate_cloudsdk)
    profile_object.get_default_profiles()
    profile_object.set_rf_profile()
    profile_list = {"open": {"2g": {}, "5g": {}}, "wpa": {"2g": {}, "5g": {}}, "wpa2_personal": {"2g": {}, "5g": {}},
                    "wpa2_enterprise": {"2g": {}, "5g": {}}}

    if get_nat_testcases["open_2g"]:
        profile_data = setup_nat_profile_data['OPEN']['2G']
        profile_list["open"]["2g"] = profile_data
        profile_object.create_open_ssid_profile(profile_data=profile_data, fiveg=False)
    if get_nat_testcases["open_5g"]:
        profile_data = setup_nat_profile_data['OPEN']['5G']
        profile_list["open"]["5g"] = profile_data
        profile_object.create_open_ssid_profile(profile_data=profile_data, two4g=False)

    if get_nat_testcases["wpa_2g"]:
        profile_data = setup_nat_profile_data['WPA']['2G']
        profile_list["wpa"]["2g"] = profile_data
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, fiveg=False)

    if get_nat_testcases["wpa_5g"]:
        profile_data = setup_nat_profile_data['WPA']['5G']
        profile_list["wpa"]["5g"] = profile_data
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, two4g=False)

    if get_nat_testcases["wpa2_personal_2g"]:
        profile_data = setup_nat_profile_data['WPA2']['2G']
        profile_list["wpa2_personal"]["2g"] = profile_data
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, fiveg=False)

    if get_nat_testcases["wpa2_personal_5g"]:
        profile_data = setup_nat_profile_data['WPA2']['5G']
        profile_list["wpa2_personal"]["5g"] = profile_data
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, two4g=False)

    if get_nat_testcases["wpa2_enterprise_2g"] or get_nat_testcases["wpa2_enterprise_5g"]:
        radius_info = {
            "name": get_testbed_name + "-RADIUS-Sanity",
            "ip": request.config.getini("radius_server_ip"),
            "port": request.config.getini("radius_port"),
            "secret": request.config.getini("radius_secret")
        }
        profile_object.create_radius_profile(radius_info=radius_info)

    if get_nat_testcases["wpa2_enterprise_2g"]:
        profile_data = setup_nat_profile_data['EAP']['2G']
        profile_list["wpa2_enterprise"]["2g"] = profile_data
        profile_object.create_wpa2_enterprise_ssid_profile(profile_data=profile_data, fiveg=False)

    if get_nat_testcases["wpa2_enterprise_5g"]:
        profile_data = setup_nat_profile_data['EAP']['5G']
        profile_list["wpa2_enterprise"]["5g"] = profile_data
        profile_object.create_wpa2_enterprise_ssid_profile(profile_data=profile_data, two4g=False)

    profile_data = {
        "profile_name": "%s-%s-%s" % (get_testbed_name, get_equipment_model, 'NAT'),
    }
    profile_object.set_ap_profile(profile_data=profile_data)
    profile_object.push_profile_old_method(equipment_id=get_equipment_id)
    yield profile_list


@pytest.fixture(scope="class")
def setup_vlan_mode(request, instantiate_cloudsdk, create_vlan_profile, get_equipment_id):
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
        for j in create_vlan_profile[i]:
            if create_vlan_profile[i][j] != {}:
                profile_data.append(create_vlan_profile[i][j]['ssid_name'])
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
    yield [profile_data, vif_config, vif_state, create_vlan_profile]
    delete_profiles(instantiate_cloudsdk, get_equipment_id)


@pytest.fixture(scope="class")
def create_vlan_profile(request, instantiate_cloudsdk, setup_vlan_profile_data, get_testbed_name, get_equipment_id,
                        get_vlan_testcases, get_equipment_model):
    print(setup_vlan_profile_data)
    # SSID and AP name shall be used as testbed_name and mode
    profile_object = ProfileUtility(sdk_client=instantiate_cloudsdk)
    profile_object.get_default_profiles()
    profile_object.set_rf_profile()
    profile_list = {"open": {"2g": {}, "5g": {}}, "wpa": {"2g": {}, "5g": {}}, "wpa2_personal": {"2g": {}, "5g": {}},
                    "wpa2_enterprise": {"2g": {}, "5g": {}}}

    if get_vlan_testcases["open_2g"]:
        profile_data = setup_vlan_profile_data['OPEN']['2G']
        profile_list["open"]["2g"] = profile_data
        profile_object.create_open_ssid_profile(profile_data=profile_data, fiveg=False)
    if get_vlan_testcases["open_5g"]:
        profile_data = setup_vlan_profile_data['OPEN']['5G']
        profile_list["open"]["5g"] = profile_data
        profile_object.create_open_ssid_profile(profile_data=profile_data, two4g=False)

    if get_vlan_testcases["wpa_2g"]:
        profile_data = setup_vlan_profile_data['WPA']['2G']
        profile_list["wpa"]["2g"] = profile_data
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, fiveg=False)

    if get_vlan_testcases["wpa_5g"]:
        profile_data = setup_vlan_profile_data['WPA']['5G']
        profile_list["wpa"]["5g"] = profile_data
        profile_object.create_wpa_ssid_profile(profile_data=profile_data, two4g=False)

    if get_vlan_testcases["wpa2_personal_2g"]:
        profile_data = setup_vlan_profile_data['WPA2']['2G']
        profile_list["wpa2_personal"]["2g"] = profile_data
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, fiveg=False)

    if get_vlan_testcases["wpa2_personal_5g"]:
        profile_data = setup_vlan_profile_data['WPA2']['5G']
        profile_list["wpa2_personal"]["5g"] = profile_data
        profile_object.create_wpa2_personal_ssid_profile(profile_data=profile_data, two4g=False)

    if get_vlan_testcases["wpa2_enterprise_2g"] or get_vlan_testcases["wpa2_enterprise_5g"]:
        radius_info = {
            "name": get_testbed_name + "-RADIUS-Sanity",
            "ip": request.config.getini("radius_server_ip"),
            "port": request.config.getini("radius_port"),
            "secret": request.config.getini("radius_secret")
        }
        profile_object.create_radius_profile(radius_info=radius_info)

    if get_vlan_testcases["wpa2_enterprise_2g"]:
        profile_data = setup_vlan_profile_data['EAP']['2G']
        profile_list["wpa2_enterprise"]["2g"] = profile_data
        profile_object.create_wpa2_enterprise_ssid_profile(profile_data=profile_data, fiveg=False)

    if get_vlan_testcases["wpa2_enterprise_5g"]:
        profile_data = setup_vlan_profile_data['EAP']['5G']
        profile_list["wpa2_enterprise"]["5g"] = profile_data
        profile_object.create_wpa2_enterprise_ssid_profile(profile_data=profile_data, two4g=False)

    profile_data = {
        "profile_name": "%s-%s-%s" % (get_testbed_name, get_equipment_model, 'VLAN'),
    }
    profile_object.set_ap_profile(profile_data=profile_data)
    profile_object.push_profile_old_method(equipment_id=get_equipment_id)
    yield profile_list


@pytest.fixture(scope="class")
def setup_bridge_profile_data(request, get_testbed_name, get_equipment_model):
    profile_data = {}
    equipment_model = get_equipment_model
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
            else:
                profile_data[security][radio]["security_key"] = "[BLANK]"
    yield profile_data


@pytest.fixture(scope="class")
def setup_nat_profile_data(request, get_testbed_name, get_equipment_model):
    profile_data = {}
    equipment_model = get_equipment_model
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
            else:
                profile_data[security][radio]["security_key"] = "[BLANK]"
    yield profile_data


@pytest.fixture(scope="class")
def setup_vlan_profile_data(request, get_testbed_name, get_equipment_model):
    profile_data = {}
    equipment_model = get_equipment_model
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
            else:
                profile_data[security][radio]["security_key"] = "[BLANK]"
    yield profile_data


def delete_profiles(sdk_client=None, equipment_id=None):
    profile_object = ProfileUtility(sdk_client=sdk_client)
    profile_object.delete_current_profile(equipment_id=equipment_id)


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


# @pytest.fixture(scope="session")
# def get_testcase(request):
#     import pdb
#     pdb.set_trace()
#
#     # mode = request.config.getoption("-m")
#     # markers = []
#     # for i in request.node.iter_markers():
#     #     markers.append(i.name)
#     # a = set(mode.split(" "))
#     # b = set(markers)
#     # markers = a.intersection(b)
#     # yield list(markers)


@pytest.fixture(scope="session")
def get_bridge_testcases(request):
    # import pdb
    # pdb.set_trace()
    print("callattr_ahead_of_alltests called")
    security = {"open_2g": False,
                "open_5g": False,
                "wpa_5g": False,
                "wpa_2g": False,
                "wpa2_personal_5g": False,
                "wpa2_personal_2g": False,
                "wpa2_enterprise_5g": False,
                "wpa2_enterprise_2g": False
                }
    session = request.node
    for item in session.items:
        for i in item.iter_markers():
            if str(i.name).__eq__("wpa_2g"):
                print(i)
                security["wpa_2g"] = True

            if str(i.name).__eq__("wpa_5g"):
                print(i)
                security["wpa_5g"] = True

            if str(i.name).__eq__("wpa2_personal_5g"):
                print(i)
                security["wpa2_personal_5g"] = True

            if str(i.name).__eq__("wpa2_personal_2g"):
                print(i)
                security["wpa2_personal_2g"] = True

            if str(i.name).__eq__("wpa2_enterprise_2g"):
                print(i)
                security["wpa2_enterprise_2g"] = True

            if str(i.name).__eq__("wpa2_enterprise_5g"):
                print(i)
                security["wpa2_enterprise_5g"] = True

    yield security


"""
open_2g
open_5g
wpa2_personal_5g
wpa2_personal_2g
wpa_5g
wpa_2g
wpa2_enterprise_5g
wpa2_enterprise_2g
"""


@pytest.fixture(scope="session")
def get_nat_testcases(request):
    print("callattr_ahead_of_alltests called")
    security = {"open_2g": False,
                "open_5g": False,
                "wpa_5g": False,
                "wpa_2g": False,
                "wpa2_personal_5g": False,
                "wpa2_personal_2g": False,
                "wpa2_enterprise_5g": False,
                "wpa2_enterprise_2g": False
                }
    session = request.node
    for item in session.items:
        for i in item.iter_markers():
            if str(i.name).__eq__("wpa_2g"):
                print(i)
                security["wpa_2g"] = True

            if str(i.name).__eq__("wpa_5g"):
                print(i)
                security["wpa_5g"] = True

            if str(i.name).__eq__("wpa2_personal_5g"):
                print(i)
                security["wpa2_personal_5g"] = True

            if str(i.name).__eq__("wpa2_personal_2g"):
                print(i)
                security["wpa2_personal_2g"] = True

            if str(i.name).__eq__("wpa2_enterprise_2g"):
                print(i)
                security["wpa2_enterprise_2g"] = True

            if str(i.name).__eq__("wpa2_enterprise_5g"):
                print(i)
                security["wpa2_enterprise_5g"] = True

    yield security


@pytest.fixture(scope="session")
def get_vlan_testcases(request):
    print("callattr_ahead_of_alltests called")
    security = {"open_2g": False,
                "open_5g": False,
                "wpa_5g": False,
                "wpa_2g": False,
                "wpa2_personal_5g": False,
                "wpa2_personal_2g": False,
                "wpa2_enterprise_5g": False,
                "wpa2_enterprise_2g": False
                }
    session = request.node
    for item in session.items:
        for i in item.iter_markers():
            if str(i.name).__eq__("wpa_2g"):
                print(i)
                security["wpa_2g"] = True

            if str(i.name).__eq__("wpa_5g"):
                print(i)
                security["wpa_5g"] = True

            if str(i.name).__eq__("wpa2_personal_5g"):
                print(i)
                security["wpa2_personal_5g"] = True

            if str(i.name).__eq__("wpa2_personal_2g"):
                print(i)
                security["wpa2_personal_2g"] = True

            if str(i.name).__eq__("wpa2_enterprise_2g"):
                print(i)
                security["wpa2_enterprise_2g"] = True

            if str(i.name).__eq__("wpa2_enterprise_5g"):
                print(i)
                security["wpa2_enterprise_5g"] = True

    yield security
