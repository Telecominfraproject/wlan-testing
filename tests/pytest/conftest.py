import pytest
from time import sleep, gmtime, strftime

import sys
import os
#sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

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
    parser.addini("sdk-customer-id", "cloud sdk customer id for the access points")
    parser.addini("sdk-equipment-id", "cloud sdk equipment id for the access point")
    parser.addini("testrail-base-url", "testrail base url")
    parser.addini("testrail-project", "testrail project name to use to generate test reports")
    parser.addini("testrail-user-id", "testrail username")
    parser.addini("testrail-user-password", "testrail user password")
    parser.addini("lanforge-ip-address", "LANforge ip address to connect to")
    parser.addini("lanforge-port-number", "LANforge port number to connect to")
    parser.addini("lanforge-radio", "LANforge radio to use")
    parser.addini("lanforge-ethernet-port", "LANforge ethernet adapter to use")

    parser.addoption(
        "--testrail-user-password",
        action="store",
        default="password",
        help="testrail user password",
        type=str
    )

    parser.addoption(
        "--sdk-equipment-id",
        action="store",
        default="-1",
        help="SDK equipment ID for AP",
        type=str
    )

    # # Cloud SDK
    # parser.addoption(
    #     "--sdk-base-url",
    #     action="store",
    #     default="wlan-portal-svc.cicd.lab.wlan.tip.build",
    #     help="cloudsdk base url",
    #     type=str
    # )
    # parser.addoption(
    #     "--sdk-user-id",
    #     action="store",
    #     default="support@example.com",
    #     help="cloudsdk user id",
    #     type=str
    # )
    # parser.addoption(
    #     "--sdk-user-password",
    #     action="store",
    #     default="support",
    #     help="cloudsdk user password",
    #     type=str
    # )

    # # jFrog
    # parser.addoption(
    #     "--jfrog-base-url",
    #     action="store",
    #     default="tip.jFrog.io/artifactory/tip-wlan-ap-firmware",
    #     help="jfrog base url",
    #     type=str
    # )
    # parser.addoption(
    #     "--jfrog-user-id",
    #     action="store",
    #     default="tip-read",
    #     help="jfrog user id",
    #     type=str
    # )
    # parser.addoption(
    #     "--jfrog-user-password",
    #     action="store",
    #     default="tip-read",
    #     help="jfrog user password",
    #     type=str
    # )

    # # testrail
    # parser.addoption(
    #     "--testrail-base-url",
    #     action="store",
    #     default="telecominfraproject.testrail.com",
    #     help="testrail base url",
    #     type=str
    # )
    # parser.addoption(
    #     "--testrail-project",
    #     action="store",
    #     default="opsfleet-wlan",
    #     help="testrail project name",
    #     type=str
    # )
    # parser.addoption(
    #     "--testrail-user-id",
    #     action="store",
    #     default="gleb@opsfleet.com",
    #     help="testrail user id",
    #     type=str
    # )
    # parser.addoption(
    #     "--testrail-user-password",
    #     action="store",
    #     default="password",
    #     help="testrail user password",
    #     type=str
    # )

    # # lanforge
    # parser.addoption(
    #     "--lanforge-ip-address",
    #     action="store",
    #     default="10.28.3.6",
    #     help="ip address of the lanforge gui",
    #     type=str
    # )
    # parser.addoption(
    #     "--lanforge-port-number",
    #     action="store",
    #     default="8080",
    #     help="port of the lanforge gui",
    #     type=str
    # )

    # change behaviour
    parser.addoption(
        "--skip-update-firmware",
        action="store_true",
        default=False,
        help="skip updating firmware on the AP (useful for local testing)"
    )
    parser.addoption(
        "--no-testrails",
        action="store_true",
        default=False,
        help="do not generate testrails tests"
    )
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
    if request.config.getoption("--no-testrails"):
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
def setup_cloudsdk(request, instantiate_cloudsdk):
    # snippet to do cleanup after all the tests are done
    def fin():
        print("Cloud SDK cleanup done")
    request.addfinalizer(fin)

    # This is broken, see sdk_set_profile for correct way to do this.
    #instantiate_cloudsdk.set_ap_profile(3, 6)
    #yield {
    #    "LANforge": {
    #        "host": request.config.getini("lanforge-ip-address"),
    #        "port": request.config.getini("lanforge-port-number"),
    #        "radio": request.config.getini("lanforge-radio"),
    #        "eth_port": request.config.getini("lanforge-ethernet-port"),
    #        "runtime_duration": 15
    #    },
    #    "24ghz": {
    #        "ssid": "TipWlan-cloud-wifi",
    #        "password": "w1r3l3ss-fr33d0m",
    #        "station_names": [ "sta2237" ]
    #    }
    #}

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
        customer_id = request.config.getini("sdk-customer-id")
        equipment_id = request.config.getoption("--sdk-equipment-id")
        if equipment_id == "-1":
            print("EQ ID invalid: ", equipment_id)
            sys.exit(1)
        pf = instantiate_cloudsdk.do_upgrade_ap_fw(request.config, report_data, test_cases, testrail_client,
                                                   latest_image, cloudModel, ap, jfrog_user, jfrog_pwd, testrail_rid,
                                                   customer_id, equipment_id, logger)

        return pf

@pytest.fixture(scope="session")
def instantiate_cloudsdk(request):
    yield CloudSDK(
        request.config.getini("sdk-user-id"),
        request.config.getini("sdk-user-password"),
        request.config.getini("sdk-base-url"),
        False  # verbose  TODO:  Make this configurable
    )

@pytest.fixture(scope="session")
def instantiate_testrail(request):
    yield TestRail_Client(
        request.config.getini("testrail-base-url"),
        request.config.getini("testrail-user-id"),
        request.config.getoption("--testrail-user-password")
    )

@pytest.fixture(scope="session")
def instantiate_jFrog(request):
    yield GetBuild(
        request.config.getini("jfrog-user-id"),
        request.config.getini("jfrog-user-password"),
        "pending",  # TODO make this optional
        url=request.config.getini("jfrog-base-url")
    )
