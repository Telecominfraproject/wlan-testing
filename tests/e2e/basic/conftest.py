import allure
import pytest
import logging


def separate_band_and_encryption(markers: list, target_object) -> list:
    """
    examples:
    1> if markers = ['2G', 'wpa2_personal']
          return -> [['2G', 'wpa2_personal']]
    2> if markers = ['2G', 'wpa3_personal', 'wpa2_personal', 'wpa', 'open']
          return -> [['2G', 'open'], ['2G', 'wpa'], ['2G', 'wpa2_personal'], ['2G', 'wpa3_personal']]
    3> if markers = ['5G', 'wpa3_personal', 'wpa2_personal', 'wpa', 'open']
          return -> [['5G', 'open'], ['5G', 'wpa'], ['5G', 'wpa2_personal'], ['5G', 'wpa3_personal']]
    4> if markers = ['5G', 'wpa3_personal', 'wpa2_personal', '2G', 'wpa', 'open']
          return -> [['2G', 'open'], ['2G', 'wpa'], ['2G', 'wpa2_personal'], ['2G', 'wpa3_personal'],
                     ['5G', 'open'], ['5G', 'wpa'], ['5G', 'wpa2_personal'], ['5G', 'wpa3_personal']]
    """

    bands = []
    encryption = []
    for marker in markers:
        if marker in target_object.supported_bands:
            bands.append(marker)
        elif marker in target_object.supported_encryption:
            encryption.append(marker)

    combinations = []
    for band in bands:
        for enc in encryption:
            combinations.append([band, enc])

    return combinations


@pytest.fixture(scope="class")
def setup_configuration(request, get_markers, get_target_object, run_lf):
    # Predefined selected markers and selected configuration

    conf = dict(request.param)
    configuration = conf.copy()
    requested_combination = []
    for key in get_markers:
        if get_markers[key]:
            combinations = separate_band_and_encryption(markers=get_markers[key], target_object=get_target_object)
            for comb in combinations:
                requested_combination.append(comb)

    # Method to setup the basic configuration
    data = {}
    if not run_lf:
        data = get_target_object.setup_basic_configuration(configuration=configuration,
                                                           requested_combination=requested_combination)
    logging.info("dut_data after config applied: " + str(data))
    yield data