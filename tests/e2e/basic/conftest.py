import allure
import pytest
import logging

@pytest.fixture(scope="class")
def setup_configuration(request, get_markers, get_target_object, run_lf):
    # Predefined selected markers and selected configuration

    conf = dict(request.param)
    configuration = conf.copy()
    requested_combination = []
    for key in get_markers:
        if get_markers[key]:
            requested_combination.append(get_markers[key])

    # Method to setup the basic configuration
    data = {}
    if not run_lf:
        data = get_target_object.setup_basic_configuration(configuration=configuration,
                                                           requested_combination=requested_combination)
    logging.info("dut_data after config applied: " + str(data))
    yield data


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
