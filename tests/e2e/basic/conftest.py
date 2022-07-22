import pytest


@pytest.fixture(scope="class")
def setup_configuration(request, get_markers):
    param = dict(request.param)
    available_keys = []
    for key in get_markers:
        if get_markers[key] == True:
            available_keys.append(key)
    print(available_keys)
    yield "return_var"
