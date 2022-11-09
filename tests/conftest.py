import json
import logging
import os
import re
import string
import sys
import random

import allure
import pytest
from _pytest.fixtures import SubRequest
from typing import Any, Callable, Optional

ALLURE_ENVIRONMENT_PROPERTIES_FILE = 'environment.properties'
ALLUREDIR_OPTION = '--alluredir'

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
log_filename = "logs/pytest_logs.log"
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
file_handler = logging.FileHandler(log_filename, mode="w", encoding=None, delay=False)

try:
    import importlib

    # sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
    sys.path.append("../tests")

    imports = importlib.import_module("imports")
    target = imports.target
    lf_libs = imports.lf_libs
    lf_tests = imports.lf_tests
    scp_file = imports.scp_file
    perfecto_interop = imports.perfecto_interop
    android_tests = imports.android_tests
    ios_tests = imports.ios_tests
    configuration = importlib.import_module("configuration")
    CONFIGURATION = configuration.CONFIGURATION
    PERFECTO_DETAILS = configuration.PERFECTO_DETAILS
    # cv_test_manager = importlib.import_module("py-json.cv_test_manager")
    # cv_test = cv_test_manager.cv_test
except ImportError as e:
    print(e)
    sys.exit("Python Import Error: " + str(e))


def pytest_addoption(parser):
    """pytest addoption function: contains ini objects and options"""
    parser.addini("controller_url", type='string', help="controller_url_parameter_override", default="0")
    parser.addini(name="firmware", type='string', help="AP Firmware build URL", default="0")

    parser.addoption(
        "--testbed",
        # nargs="+",
        default="basic-01",
        help="AP Model which is needed to test"
    )
    parser.addoption(
        "--num_stations",
        default=1,
        help="Number of Stations"
    )
    parser.addoption(
        "--device",
        # nargs="+",
        default="lanforge",
        help="Test Traffic Generator which can be used,  lanforge | perfecto"
    )
    parser.addoption(
        "--run-lf",
        action="store_true",
        default=False,
        help="Test Traffic Generator which can be used,  lanforge | perfecto"
    )
    parser.addoption(
        "--skip-lf",
        action="store_true",
        default=False,
        help="Skips the Lanforge Usage"
    )
    parser.addoption(
        "--skip-all",
        action="store_true",
        default=False,
        help="Skips the Lanforge Usage"
    )

    parser.addoption(
        "--skip-env",
        action="store_true",
        default=False,
        help="skip adding to env data"
    )
    parser.addoption(
        "--client-type",
        default="ac",
        help="Select the client type for test ac | ax"
    )

    parser.addoption(
        "--use-perfecto-android",
        action="store_true",
        default=False,
        help="Use Interop Android Test Package for tests"
    )

    parser.addoption(
        "--use-perfecto-ios",
        action="store_true",
        default=False,
        help="Use Interop IoS Test Package for tests"
    )

    parser.addoption(
        "--port",
        default=False,
        help="Select the port for AP Up Down tests"
    )


@pytest.fixture(scope="session")
def get_lab_info():
    yield configuration


@pytest.fixture(scope="session")
def run_lf(request):
    """yields the testbed option selection"""
    run_lf = request.config.getoption("--run-lf")
    yield run_lf


@pytest.fixture(scope="session")
def skip_lf(request):
    """yields the testbed option selection"""
    skip_lf = request.config.getoption("--skip-lf")
    yield skip_lf


@pytest.fixture(scope="session")
def selected_testbed(request):
    """yields the testbed option selection"""
    current_testbed = request.config.getoption("--testbed")
    yield current_testbed


@pytest.fixture(scope="session")
def selected_port(request):
    """yields the port option selection"""
    current_port = request.config.getoption("--port")
    yield current_port


@pytest.fixture(scope="session")
def num_stations(request):
    """yields the testbed option selection"""
    num_stations = request.config.getoption("--num_stations")
    yield int(num_stations)


@pytest.fixture(scope="session")
def device(request):
    """yields the device option selection"""
    var = request.config.getoption("--device")
    yield var


@pytest.fixture(scope="session")
def get_device_configuration(device, request):
    """yields the selected device information from lab info file (configuration.py)"""
    if device != "lanforge":
        logging.info("Selected the lab Info data: " + str((PERFECTO_DETAILS[device])))
        print(PERFECTO_DETAILS[device])
        yield PERFECTO_DETAILS[device]
    else:
        yield ""


@pytest.fixture(scope="session")
def client_type(request):
    """yields the testbed option selection"""
    client_type = request.config.getoption("--client-type")
    yield client_type


@pytest.fixture(scope="session")
def get_security_flags():
    """used to get the essential markers on security and band"""
    # Add more classifications as we go
    security = ["open", "wpa", "wep", "wpa2_personal", "wpa3_personal", "wpa3_personal_mixed",
                "wpa_wpa2_enterprise_mixed", "wpa2_eap", "wpa2_only_eap",
                "wpa_wpa2_personal_mixed", "wpa_enterprise", "wpa2_enterprise", "wpa3_enterprise_mixed",
                "wpa3_enterprise", "twog", "fiveg", "sixg", "fiveg_lower", "fiveg_upper", "radius"]
    yield security


@pytest.fixture(scope="session")
def get_markers(request, get_security_flags):
    """used to get the markers on the selected test case class, used in setup_configuration"""
    session = request.node
    markers = list()
    security = get_security_flags
    data = dict()
    for item in session.items:
        data[item] = []
        for j in item.iter_markers():
            for i in security:
                if j.name == i:
                    if j.name == "twog":
                        data[item].append("2G")
                        continue
                    if j.name == "fiveg":
                        data[item].append("5G")
                        continue
                    if j.name == "sixg":
                        data[item].append("6G")
                        continue
                    if j.name == "fiveg_lower":
                        data[item].append("5G-lower")
                        continue
                    if j.name == "fiveg_upper":
                        data[item].append("5G-upper")
                        continue
                    data[item].append(j.name)
            print(j.name)
            markers.append(j.name)
    print(data)
    yield data


@pytest.fixture(scope="session")
def get_target_object(request, run_lf, get_testbed_details, add_allure_environment_property: Callable) -> None:
    """yields the testbed option selection"""
    if request.config.getoption("--skip-all"):
        pytest.skip("Skipping all")
    t_object = None
    if not run_lf:
        try:
            t_object = target(controller_data=get_testbed_details["controller"], target=get_testbed_details["target"],
                              configuration=configuration,
                              device_under_tests_info=get_testbed_details["device_under_tests"])
            if not request.config.getoption("--skip-env"):
                if get_testbed_details["target"] == "tip_2x":
                    t_object.setup_environment_properties(add_allure_environment_property=
                                                          add_allure_environment_property)

        except Exception as e:
            t_object = None
            logging.error(
                "Exception is setting up Target Library Object: " + str(
                    e) + " Check the lab_info.json for the Data and ")
            pytest.exit("Exception is setting up Target Library Object: " + str(e))

        def teardown_target():
            if t_object is not None:
                t_object.teardown_objects()

        request.addfinalizer(teardown_target)
    yield t_object


@pytest.fixture(scope="session")
def get_testbed_details(selected_testbed, request):
    """yields the selected testbed information from lab info file (configuration.py)"""
    try:
        TESTBED = CONFIGURATION[selected_testbed]
    except Exception as e:
        logging.error("Error in Fetching Testbed: " + str(e))
        pytest.exit("Exception in getting Testbed Details. Testbed Details are not available : " + selected_testbed)
    if request.config.getini("controller_url") != "0":
        TESTBED["controller"]["url"] = request.config.getini("controller_url")
    if request.config.getini("firmware") != "0":
        version = request.config.getini("firmware")
        version_list = version.split(",")
        for i in range(len(TESTBED["device_under_tests"])):
            TESTBED["device_under_tests"][i]["version"] = version_list[0]
    allure.attach(name="Testbed Details", body=str(json.dumps(TESTBED, indent=2)),
                  attachment_type=allure.attachment_type.JSON)
    yield TESTBED


@pytest.fixture(scope="session")
def get_controller_version(fixtures_ver, run_lf, cc_1):
    version = ""
    if not run_lf and not cc_1:
        version = fixtures_ver.get_sdk_version()
        print(version)
    yield version


@pytest.fixture(scope="session")
def get_dut_versions(fixtures_ver, run_lf, cc_1):
    version = ""
    if not run_lf and not cc_1:
        version = fixtures_ver.get_sdk_version()
        print(version)
    yield version


@pytest.fixture(scope="session")
def is_test_library_perfecto_android(request):
    interop = request.config.getoption("--use-perfecto-android")
    yield interop


@pytest.fixture(scope="session")
def is_test_library_perfecto_ios(request):
    interop = request.config.getoption("--use-perfecto-ios")
    yield interop


@pytest.fixture(scope="session")
def get_test_library(get_testbed_details, is_test_library_perfecto_android, is_test_library_perfecto_ios, request,
                     get_device_configuration, device, run_lf):
    if request.config.getoption("--skip-all"):
        pytest.skip("Skipping all")
    if is_test_library_perfecto_android:
        obj = android_tests.AndroidTests(perfecto_data=PERFECTO_DETAILS,
                                         dut_data=get_testbed_details["device_under_tests"], device=device)

    elif is_test_library_perfecto_ios:
        obj = ios_tests.ios_tests(perfecto_data=PERFECTO_DETAILS, dut_data=get_testbed_details["device_under_tests"],
                                  device=device)
    else:
        obj = lf_tests(lf_data=get_testbed_details["traffic_generator"],
                       dut_data=get_testbed_details["device_under_tests"],
                       log_level=logging.DEBUG,
                       run_lf=run_lf,
                       influx_params=None)
        pwd = os.getcwd()
        isExist = os.path.exists(str(pwd) + "/../reports")
        if not isExist:
            os.mkdir(str(pwd) + "/../reports")

    def teardown_test():
        if is_test_library_perfecto_android:
            try:
                obj.teardown()
            except Exception as e:
                print(e)
                logging.error("Exception in teardown")
        elif is_test_library_perfecto_ios:
            try:
                obj.teardown()
            except Exception as e:
                print(e)
                logging.error("Exception in teardown")
        else:
            pass

    request.addfinalizer(teardown_test)
    yield obj


@pytest.fixture(scope="session")
def execution_number(request):
    number = int(request.param)
    print(number)
    mode = "NAT-WAN"
    if number == 0:
        mode = "NAT-WAN"
    if number == 1:
        mode = "NAT-LAN"
    yield mode


@pytest.fixture(scope="session")
def radius_info():
    """yields the radius server information from lab info file"""
    yield configuration.RADIUS_SERVER_DATA


@pytest.fixture(scope="session")
def rate_radius_info():
    """yields the radius server information from lab info file"""
    yield configuration.RATE_LIMITING_RADIUS_SERVER_DATA


@pytest.fixture(scope="session")
def rate_radius_accounting_info():
    """yields the radius accounting information from lab info file"""
    yield configuration.RATE_LIMITING_RADIUS_ACCOUNTING_DATA


@pytest.fixture(scope='session', autouse=True)
def add_allure_environment_property(request: SubRequest) -> Optional[Callable]:
    environment_properties = dict()

    def maker(key: str, value: Any):
        environment_properties.update({key: value})

    yield maker

    alluredir = request.config.getoption(ALLUREDIR_OPTION)

    if not alluredir or not os.path.isdir(alluredir) or not environment_properties:
        return

    allure_env_path = os.path.join(alluredir, ALLURE_ENVIRONMENT_PROPERTIES_FILE)

    with open(allure_env_path, 'w') as _f:
        data = '\n'.join([f'{variable}={value}' for variable, value in environment_properties.items()])
        _f.write(data)


@pytest.fixture(scope="function")
def get_dut_logs_per_test_case(request, run_lf, get_testbed_details, get_target_object):
    if not run_lf:
        S = 9
        instance_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
        for i in range(len(get_testbed_details["device_under_tests"])):
            get_target_object.get_dut_library_object().run_generic_command(
                cmd="logger start testcase: " + instance_name,
                idx=i)

        def collect_logs():
            for i in range(len(get_testbed_details["device_under_tests"])):
                get_target_object.get_dut_library_object().run_generic_command(
                    cmd="logger stop testcase: " + instance_name,
                    idx=i)
                ap_logs = get_target_object.get_dut_library_object().get_logread(
                    start_ref="start testcase: " + instance_name,
                    stop_ref="stop testcase: " + instance_name)
                allure.attach(name='Logs - ' + get_testbed_details["device_under_tests"][i]["identifier"],
                              body=str(ap_logs))

        request.addfinalizer(collect_logs)


@pytest.fixture(scope="function")
def get_test_device_logs(request, get_testbed_details, get_target_object, skip_lf):
    if not skip_lf:
        ip = get_testbed_details["traffic_generator"]["details"]["manager_ip"]
        port = get_testbed_details["traffic_generator"]["details"]["ssh_port"]

        def collect_logs_tg():
            log_0 = "/home/lanforge/lanforge_log_0.txt"
            log_1 = "/home/lanforge/lanforge_log_1.txt"
            obj = scp_file(ip=ip, port=port, username="root", password="lanforge", remote_path=log_0,
                           local_path=".")
            obj.pull_file()
            allure.attach.file(source="lanforge_log_0.txt",
                               name="lanforge_log_0")
            obj = scp_file(ip=ip, port=port, username="root", password="lanforge", remote_path=log_1,
                           local_path=".")
            obj.pull_file()
            allure.attach.file(source="lanforge_log_1.txt",
                               name="lanforge_log_1")

        request.addfinalizer(collect_logs_tg)


@pytest.fixture(scope="function")
def check_connectivity(request, get_testbed_details, get_target_object, run_lf):
    def collect_logs():
        for i in range(len(get_testbed_details["device_under_tests"])):
            ret_val = get_target_object.get_dut_library_object().ubus_call_ucentral_status(idx=i, attach_allure=True,
                                                                                           retry=10)
            if not ret_val["connected"] or ret_val["connected"] is None:
                ap_logs = get_target_object.get_dut_library_object().get_dut_logs()
                allure.attach(name='Logs - ' + get_testbed_details["device_under_tests"][i]["identifier"],
                              body=str(ap_logs))

            allure.attach(name='Device : ' + get_testbed_details["device_under_tests"][i]["identifier"] +
                               " is connected after Test", body="")

    if not run_lf:
        request.addfinalizer(collect_logs)
