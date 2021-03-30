import pytest
import sys

if 'cloudsdk_tests' not in sys.path:
    sys.path.append(f'../../libs/cloudsdk')
from cloudsdk import CloudSDK
from configuration_data import TEST_CASES


class TestCloudAPNOS(object):

    def test_apnos_cloud(self):
        pass