from logging import exception
import unittest
import warnings
from perfecto.test import TestResultFactory
import pytest
import sys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException

import sys
import allure

if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.android, pytest.mark.interop_and, pytest.mark.Reboot]

from android_lib import set_APconnMobileDevice_android, rebootPhone

@allure.feature("Android DeviceMaint Reboot")

class TestAndroidRebootDevices(object):

    def test_Reboot_deviceMaint(self, request, get_APToMobileDevice_data, setup_perfectoMobile_android):

    
        report = setup_perfectoMobile_android[1]
        driver = setup_perfectoMobile_android[0]
        connData = get_APToMobileDevice_data

        get_APToMobileDevice_data

        rebootPhone(setup_perfectoMobile_android, get_APToMobileDevice_data)

  