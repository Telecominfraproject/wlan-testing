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

@pytest.fixture(scope="class")
def setup_open_roaming_configuration(request, get_markers, get_target_object, run_lf):
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
        data = get_target_object.setup_basic_configuration(configuration=configuration, requested_combination=
                                                           requested_combination, open_roaming=True)
    logging.info("dut_data after config applied: " + str(data))
    yield data
