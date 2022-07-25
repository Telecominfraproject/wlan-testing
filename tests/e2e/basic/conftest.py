import pytest


@pytest.fixture(scope="class")
def setup_configuration(request, get_markers, get_target_object):
    configuration = dict(request.param)
    requested_combination = []
    for key in get_markers:
        if get_markers[key]:
            requested_combination.append(get_markers[key])
    print(requested_combination)
    status = get_target_object.setup_basic_configuration(configuration=configuration,
                                                         requested_combination=requested_combination)
    yield status
