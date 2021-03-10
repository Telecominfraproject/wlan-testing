# import files in the current directory
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.realpath( __file__ )
    )
)

import pytest
from configuration_data import PROFILE_DATA

def pytest_addoption(parser):
    parser.addini("jfrog-base-url", "jfrog base url")
    parser.addini("jfrog-user-id", "jfrog username")
    parser.addini("jfrog-user-password", "jfrog password")
    parser.addini("testbed-name", "cloud sdk base url")
    parser.addini("sdk-user-id", "cloud sdk username")
    parser.addini("sdk-user-password", "cloud sdk user password")
    parser.addini("sdk-customer-id", "cloud sdk customer id for the access points")
    parser.addini("testrail-base-url", "testrail base url")
    parser.addini("testrail-project", "testrail project name to use to generate test reports")
    parser.addini("testrail-user-id", "testrail username")
    parser.addini("testrail-user-password", "testrail user password")
    parser.addini("lanforge-ip-address", "LANforge ip address to connect to")
    parser.addini("lanforge-port-number", "LANforge port number to connect to")
    parser.addini("lanforge-radio", "LANforge radio to use")
    parser.addini("lanforge-ethernet-port", "LANforge ethernet adapter to use")

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
        default=[ "ECW5410" ],
        help="list of access points to test"
    )

def pytest_generate_tests(metafunc):
    if 'access_points' in metafunc.fixturenames:
        metafunc.parametrize("access_points", metafunc.config.getoption('--access-points'), scope="session")

# run something after all tests are done regardless of the outcome
def pytest_unconfigure(config):
    print("Tests cleanup done")

@pytest.fixture(scope="function")
def setup_cloudsdk(request, instantiate_cloudsdk):
    def fin():
        print(f"Cloud SDK cleanup for {request.node.originalname}")
    request.addfinalizer(fin)
    yield PROFILE_DATA[request.node.originalname]

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
def instantiate_cloudsdk(request):
    yield "instantiate_cloudsdk"

@pytest.fixture(scope="session")
def instantiate_jFrog(request):
    yield "instantiate_jFrog"

@pytest.fixture(scope="session")
def get_customer_id(request):
    yield request.config.getini("sdk-customer-id")

@pytest.fixture(scope="session")
def get_testbed_name(request):
    yield request.config.getini("testbed-name")
