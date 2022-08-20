import pytest


@pytest.fixture(scope="class")
def setup_configuration(request, get_markers, get_target_object):
    # Predefined selected markers and selected configuration
    configuration = dict(request.param).copy()
    requested_combination = []
    for key in get_markers:
        if get_markers[key]:
            requested_combination.append(get_markers[key])

    # Method to setup the basic configuration
    data = get_target_object.setup_basic_configuration(configuration=configuration,
                                                       requested_combination=requested_combination)
    yield data
