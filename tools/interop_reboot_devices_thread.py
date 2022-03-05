#!/usr/bin/python3.9
"""
Note: Run this file as it is to reboot all devices at same time from interop lab
    interop_tools : To reboot
   ./interop_tools --all_devices "{\"Galaxy S9\":\"Android\",\"Galaxy S20\":\"Android\"}"
"""

import sys

if "libs" not in sys.path:
    sys.path.append("../libs/perfecto_libs/")

import argparse
import paramiko

import datetime
import sys
import os
import time
import warnings
from _pytest.outcomes import xfail
import urllib3
from perfecto.model.model import Job, Project
from perfecto import (PerfectoExecutionContext, PerfectoReportiumClient, TestContext, TestResultFactory)
import pytest
import logging
import re
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver

from android_lib import *
from iOS_lib import *
import json
import ast
import threading

# device = iPhone-12, iPhone-11, iPhone-7 ,platform_name=iOS
# device =  Galaxy S20, Galaxy S10.*, Galaxy S9, Pixel 4, platform_name = Android

class perfecto_tools:

    def __init__(self):
        warnings.simplefilter("ignore", ResourceWarning)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_capabilities(self, platform_name, device, browser_name):
        self.capabilities = {
            'platformName': platform_name,
            'model': device,
            'browserName': browser_name,
            'securityToken': 'eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJpYXQiOjE2MzI4Mzc2NDEsImp0aSI6IjAwZGRiYWY5LWQwYjMtNDRjNS1hYjVlLTkyNzFlNzc5ZGUzNiIsImlzcyI6Imh0dHBzOi8vYXV0aDIucGVyZmVjdG9tb2JpbGUuY29tL2F1dGgvcmVhbG1zL3RpcC1wZXJmZWN0b21vYmlsZS1jb20iLCJhdWQiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwic3ViIjoiODNkNjUxMWQtNTBmZS00ZWM5LThkNzAtYTA0ZjBkNTdiZDUyIiwidHlwIjoiT2ZmbGluZSIsImF6cCI6Im9mZmxpbmUtdG9rZW4tZ2VuZXJhdG9yIiwibm9uY2UiOiI2ZjE1YzYxNy01YTU5LTQyOWEtODc2Yi1jOTQxMTQ1ZDFkZTIiLCJzZXNzaW9uX3N0YXRlIjoiYmRjZTFmYTMtMjlkYi00MmFmLWI5YWMtYjZjZmJkMDEyOTFhIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.5R85_1R38ZFXv_wIjjCIsj8NJm1p66dCsLJI5DBEmks',
            'useAppiumForWeb': 'false',
            'useAppiumForHybrid': 'false',
        }
        return self.capabilities

    def get_driver(self, capabilities):
        try:
            self.driver = webdriver.Remote(
                "https://tip.perfectomobile.com/nexperience/perfectomobile/wd/hub",
                capabilities
            )
        except:
            exit("Unable to get driver")

        return self.driver

    def driver_wait(self, time):
        self.driver.implicitly_wait(time)

    def reboot(self, driver, device_model_name):
        params = {}
        print("rebooting..", device_model_name)
        driver.execute_script('mobile:handset:reboot', params)
        print("rebooting complete for ",device_model_name)

    def close_driver(self, driver, device_model_name):
        try:
            driver.close()
            print("Driver Closed for ",device_model_name)
        except:
            print("Unable to close driver")
        finally:
            driver.quit()


def main():
    parser = argparse.ArgumentParser(prog="interop_tools",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     allow_abbrev=True,
                                     epilog="About interop_tools.py",
                                     description="Tools for Interop")

    parser.add_argument('--all_devices', type=str,
                        help=' --all_devices : device you want to reboot '
                             'ex. --all_devices "{\"Galaxy S9\":\"Android\",\"Galaxy S20\":\"Android\"}"',
                        default="{\"Galaxy S20\": 'Android', \"Galaxy S10.*\": 'Android', \"Galaxy S9\": 'Android', \"Pixel 4\": 'Android',\"iPhone-12\": 'iOS', \"iPhone-11\": 'iOS', \"iPhone-7\" : 'iOS', \"iPhone-XR\" : 'iOS'}")

    args = parser.parse_args()
    all_devices = args.all_devices
    all_devices = ast.literal_eval(all_devices)

    perfecto_tool = perfecto_tools()

    def rebool_all(platform, device_name):
        try:
            capabilities = perfecto_tool.get_capabilities(platform_name=platform, device=device_name,
                                                          browser_name="mobileOS")
            driver = perfecto_tool.get_driver(capabilities=capabilities)
            perfecto_tool.reboot(driver=driver, device_model_name=device_name)
        except:
            print("Reboot Failed !")
        finally:
            print("Closing driver for: ", device_name)
            perfecto_tool.close_driver(driver=driver,device_model_name=device_name)

    for device_name, platform in all_devices.items():
        device_name = threading.Thread(target=rebool_all, args=(platform,device_name))
        print(device_name)
        device_name.start()

if __name__ == '__main__':
    main()
