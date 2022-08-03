import logging

import pytest


class perfecto_interop:
    dut_data = list()
    security_token = None
    perfecto_data = dict()

    def __init__(self, perfecto_data=None, dut_data=None):
        if perfecto_data is None:
            logging.error("Perfecto data is not provided")
            pytest.exit("Perfecto data is not provided")
        if dut_data is None:
            logging.error("Device Under Test data is not provided")
            pytest.exit("Device Under Test data is not provided")
        self.perfecto_data = perfecto_data

    def setup_metadata(self):
        pass
