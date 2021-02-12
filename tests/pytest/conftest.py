import pytest
from time import sleep, gmtime, strftime

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

sys.path.append(f'..')

for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../../lanforge/lanforge-scripts/{folder}')

sys.path.append(f'../../libs/lanforge/')
sys.path.append(f'../../libs/cloudsdk/')
sys.path.append(f'../../libs/apnos/')
sys.path.append(f'../../libs/testrails/')
sys.path.append(f'../../libs/')

sys.path.append(f'../test_utility/')

from utils import *
from UnitTestBase import *
from JfrogHelper import *
from cloudsdk import *
from testrail_api import TestRail_Client


def pytest_addoption(parser):
    parser.addini("jfrog-base-url", "jfrog base url")
    parser.addini("jfrog-user-id", "jfrog username")
    parser.addini("jfrog-user-password", "jfrog password")

    parser.addini("sdk-base-url", "cloud sdk base url")
    parser.addini("sdk-user-id", "cloud sdk username")
    parser.addini("sdk-user-password", "cloud sdk user password")
    parser.addini("customer-id", "cloud sdk customer id for the access points")
    parser.addini("equipment-id", "cloud sdk equipment id for the access point")
    parser.addini("default-ap-profile", "cloud sdk default AP profile name")

    parser.addini("verbose", "Enable verbose logs?")

    parser.addini("ap-ip", "AP IP address (or can use serial)")
    parser.addini("ap-username", "AP username")
    parser.addini("ap-password", "AP password")
    parser.addini("ap-jumphost-address", "AP jumphost IP address")
    parser.addini("ap-jumphost-username", "AP jumphost username")
    parser.addini("ap-jumphost-password", "AP jumphost password")
    parser.addini("ap-jumphost-port", "AP jumphost port")
    parser.addini("ap-jumphost-wlan-testing", "AP jumphost wlan-testing code directory")
    parser.addini("ap-jumphost-tty", "AP jumphost TTY")

    parser.addini("build-id", "What build flavor to use, ie 'pending'")
    parser.addini("testbed", "Testbed name")
    parser.addini("mode", "AP Mode, bridge/vlan/nat")
    parser.addini("skip-wpa", "Should we skip setting up WPA?")
    parser.addini("skip-wpa2", "Should we skip setting up WPA2?")
    parser.addini("skip-radius", "Should we skip setting up EAP/Radius?")
    parser.addini("skip-profiles", "Should we skip setting up profiles")

    parser.addini("ssid-2g-wpa", "Configure ssid-2g-wpa")
    parser.addini("psk-2g-wpa", "Configure psk-2g-wpa")
    parser.addini("ssid-5g-wpa", "Configure ssid-5g-wpa")
    parser.addini("psk-5g-wpa", "Configure psk-5g-wpa")
    parser.addini("ssid-2g-wpa2", "Configure ssid-2g-wpa2")
    parser.addini("psk-2g-wpa2", "Configure psk-2g-wpa2")
    parser.addini("ssid-5g-wpa2", "Configure ssid-5g-wpa2")
    parser.addini("psk-5g-wpa2", "Configure psk-5g-wpa2")

    parser.addini("testrail-base-url", "testrail base url")
    parser.addini("testrail-project", "testrail project name to use to generate test reports")
    parser.addini("testrail-user-id", "testrail username")
    parser.addini("testrail-user-password", "testrail user password")
    parser.addini("lanforge-ip-address", "LANforge ip address to connect to")
    parser.addini("lanforge-port-number", "LANforge port number to connect to")
    parser.addini("lanforge-radio", "LANforge radio to use")
    parser.addini("lanforge-ethernet-port", "LANforge ethernet adapter to use")

    add_base_parse_args_pytest(parser)

    # this has to be the last argument
    # example: --access-points ECW5410 EA8300-EU
    parser.addoption(
        "--access-points",
        nargs="+",
        default=[ "ECW5410" ],
        help="list of access points to test"
    )

def pytest_generate_tests(metafunc):
    metafunc.parametrize("access_points", metafunc.config.getoption('--access-points'), scope="session")

# run something after all tests are done regardless of the outcome
def pytest_unconfigure(config):
    print("Tests cleanup done")

@pytest.fixture(scope="session")
def setup_testrails(request, instantiate_testrail, access_points):
    if request.config.getoption("--testrail-user-id") == "NONE":
        yield -1
        return # needed to stop fixture execution

    if request.config.getoption("--skip-update-firmware"):
        firmware_update_case = []
    else:
        firmware_update_case = [ 2831 ]
    seen = {None}
    test_data = []
    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        if cls not in seen:
            if hasattr(cls.obj, "get_test_data"):
                test_data.append(cls.obj.get_test_data())
            seen.add(cls)
    testrail_project_id = instantiate_testrail.get_project_id(request.config.getini("testrail-project"))
    runId = instantiate_testrail.create_testrun(
        name=f'Nightly_model_{access_points}_{strftime("%Y-%m-%d", gmtime())}',
        case_ids=( [*test_data] + firmware_update_case ),
        project_id=testrail_project_id
    )
    yield runId

# TODO:  Should not be session wide I think, you will want to run different
# configurations (bridge, nat, vlan, wpa/wpa2/eap, etc
@pytest.fixture(scope="session")
def setup_cloudsdk(request, instantiate_cloudsdk, instantiate_testrail):
    # snippet to do cleanup after all the tests are done
    def fin():
        print("Cloud SDK cleanup done")
    request.addfinalizer(fin)

    # Set up bridged setup by default.

    command_line_args = create_command_line_args(request)

    cloud = instantiate_cloudsdk

    cloud.assert_bad_response = True

    equipment_id = instantiate_cloudsdk.equipment_id

    print("equipment-id: %s" % (equipment_id))
    if equipment_id == "-1":
        print("ERROR:  Could not find equipment-id.")
        sys.exit(1)

    ###Get Current AP info
    try:
        ap_cli_info = ssh_cli_active_fw(command_line_args)
        ap_cli_fw = ap_cli_info['active_fw']
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        ap_cli_info = "ERROR"
        print("FAILED:  Cannot Reach AP CLI.");
        sys.exit(1)

    fw_model = ap_cli_fw.partition("-")[0]

    print('Current Active AP FW from CLI:', ap_cli_fw)

    radius_name = "%s-%s-%s" % (command_line_args.testbed, fw_model, "Radius")

    print("Create profiles")
    ap_object = CreateAPProfiles(command_line_args, cloud=cloud, client=instantiate_testrail, fw_model=fw_model)

    # Logic to create AP Profiles (Bridge Mode)

    ap_object.set_ssid_psk_data(ssid_2g_wpa=command_line_args.ssid_2g_wpa,
                                ssid_5g_wpa=command_line_args.ssid_5g_wpa,
                                psk_2g_wpa=command_line_args.psk_2g_wpa,
                                psk_5g_wpa=command_line_args.psk_5g_wpa,
                                ssid_2g_wpa2=command_line_args.ssid_2g_wpa2,
                                ssid_5g_wpa2=command_line_args.ssid_5g_wpa2,
                                psk_2g_wpa2=command_line_args.psk_2g_wpa2,
                                psk_5g_wpa2=command_line_args.psk_5g_wpa2)

    print(ap_object)

    print("creating Profiles")
    ssid_template = "TipWlan-Cloud-Wifi"

    if not command_line_args.skip_profiles:
        if not command_line_args.skip_radius:
            # Radius Profile needs to be set here
            # obj.create_radius_profile(radius_name, rid, key)
            pass
        ap_object.create_ssid_profiles(ssid_template=ssid_template, skip_eap=True, skip_wpa=command_line_args.skip_wpa,
                                       skip_wpa2=command_line_args.skip_wpa2, mode=command_line_args.mode)

        print("Create AP with equipment-id: ", equipment_id)
        ap_object.create_ap_profile(eq_id=equipment_id, fw_model=fw_model, mode=command_line_args.mode)
        ap_object.validate_changes(mode=command_line_args.mode)

    print("Profiles Created")

    yield ap_object

@pytest.fixture(scope="session")
def update_firmware(request, setup_testrails, instantiate_jFrog, instantiate_cloudsdk, access_points):
    if request.config.getoption("--skip-update-firmware"):
        return True

    #access_points is really a single AP.
    ap = access_points

    if True:
        latest_image = instantiate_jFrog.get_latest_image(ap)
        if latest_image is None:
            print("AP Model: %s doesn't match the available Models"%(ap))
            sys.exit(1)  # TODO:  How to return error properly here?

        cloudModel = cloud_sdk_models[ap]
        logger = None
        report_data = None
        test_cases = None
        testrail_client = None
        jfrog_user = instantiate_jFrog.get_user()
        jfrog_pwd = instantiate_jFrog.get_passwd()
        testrail_rid = 0
        customer_id = request.config.getoption("--customer-id")
        equipment_id = instantiate_cloudsdk.equipment_id
        pf = instantiate_cloudsdk.do_upgrade_ap_fw(request.config, report_data, test_cases, testrail_client,
                                                   latest_image, cloudModel, ap, jfrog_user, jfrog_pwd, testrail_rid,
                                                   customer_id, equipment_id, logger)

        return pf

@pytest.fixture(scope="session")
def instantiate_cloudsdk(request):
    command_line_args = create_command_line_args(request)
    rv = CloudSDK(command_line_args)

    equipment_id = request.config.getoption("--equipment-id")
    if equipment_id == "-1":
        eq_id = ap_ssh_ovsh_nodec(command_line_args, 'id')
        print("EQ Id: %s" % (eq_id))

        # Now, query equipment to find something that matches.
        eq = rv.get_customer_equipment(customer_id)
        for item in eq:
            for e in item['items']:
                print(e['id'], "  ", e['inventoryId'])
                if e['inventoryId'].endswith("_%s" % (eq_id)):
                    print("Found equipment ID: %s  inventoryId: %s" % (e['id'], e['inventoryId']))
                    equipment_id = str(e['id'])

    rv.equipment_id = equipment_id

    if equipment_id == "-1":
        print("EQ ID invalid: ", equipment_id)
        sys.exit(1)

    yield rv

@pytest.fixture(scope="session")
def instantiate_testrail(request):    
    yield TestRail_Client(create_command_line_args(request))

@pytest.fixture(scope="session")
def instantiate_jFrog(request):
    yield GetBuild(
        request.config.getini("jfrog-user-id"),
        request.config.getini("jfrog-user-password"),
        "pending",  # TODO make this optional
        url=request.config.getini("jfrog-base-url")
    )
