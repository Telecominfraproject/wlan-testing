#!/usr/bin/python3.9
"""

    interop_tools : Tools for Interop
                reboot
    ./interop_tools --device "{\"Galaxy S9\":\"Android\"}" --project_name "" --job_name "" --job_number 1 --test_tag "" --test_case_name ""
    ./interop_tools --device "{\"Galaxy S9\":\"Android\"}" --job_number 1
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
from perfecto import (PerfectoExecutionContext, PerfectoReportiumClient,TestContext, TestResultFactory)
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
# device = iPhone-12, iPhone-11, iPhone-7 ,platform_name=iOS
# device =  Galaxy S20, Galaxy S10.*, Galaxy S9, Pixel 4, platform_name = Android

class perfecto_tools:

    def __init__(self, project_name="TIP-test-Execution", job_name="reboot-devices", job_number=1,
                 test_tag="TIP-PyTest-Execution", test_case_name="reboot", device="iPhone-12",
                 platform_name="iOS", browser_name="mobileOS"):
        warnings.simplefilter("ignore", ResourceWarning)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.driver = None
        self.reporting_client = None
        self.projectname = project_name
        self.projectversion = 1.0
        self.jobname = job_name
        self.jobnumber = job_number
        self.tags = test_tag
        self.device = device  # iPhone-11
        self.testCaseName = test_case_name
        self.platform_name = platform_name  # iOS
        self.browser_name = browser_name
        self.capabilities = {
            'platformName': self.platform_name,
            'model': self.device,
            'browserName': self.browser_name,
            'securityToken': 'eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJpYXQiOjE2MzI4Mzc2NDEsImp0aSI6IjAwZGRiYWY5LWQwYjMtNDRjNS1hYjVlLTkyNzFlNzc5ZGUzNiIsImlzcyI6Imh0dHBzOi8vYXV0aDIucGVyZmVjdG9tb2JpbGUuY29tL2F1dGgvcmVhbG1zL3RpcC1wZXJmZWN0b21vYmlsZS1jb20iLCJhdWQiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwic3ViIjoiODNkNjUxMWQtNTBmZS00ZWM5LThkNzAtYTA0ZjBkNTdiZDUyIiwidHlwIjoiT2ZmbGluZSIsImF6cCI6Im9mZmxpbmUtdG9rZW4tZ2VuZXJhdG9yIiwibm9uY2UiOiI2ZjE1YzYxNy01YTU5LTQyOWEtODc2Yi1jOTQxMTQ1ZDFkZTIiLCJzZXNzaW9uX3N0YXRlIjoiYmRjZTFmYTMtMjlkYi00MmFmLWI5YWMtYjZjZmJkMDEyOTFhIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.5R85_1R38ZFXv_wIjjCIsj8NJm1p66dCsLJI5DBEmks',
            'useAppiumForWeb': 'false',
            'useAppiumForHybrid': 'false',
        }
        self.app_data = {
            "webURL": "https://www.google.com",
            "lblSearch": "//*[@class='gLFyf']",
            "elelSearch": "(//*[@class='sbic sb43'])[1]",
            "BtnRunSpeedTest": "//*[text()='RUN SPEED TEST']",
            "bundleId-iOS-Settings": 'com.apple.Preferences',
            "bundleId-iOS-Safari": 'com.apple.mobilesafari',
            "downloadMbps": "//*[@id='knowledge-verticals-internetspeedtest__download']/P[@class='spiqle']",
            "UploadMbps": "//*[@id='knowledge-verticals-internetspeedtest__upload']/P[@class='spiqle']",
            # Android
            "platformName-android": 'Android',
            "appPackage-android": 'com.android.settings'
        }

        self.driver = webdriver.Remote(
            "https://tip.perfectomobile.com/nexperience/perfectomobile/wd/hub",
            self.capabilities
        )
        self.device_model_name = self.driver.execute_script('mobile:handset:info', {'property': 'model'})
        self.perfecto_execution_context = PerfectoExecutionContext(self.driver, self.tags, Job(self.jobname, self.jobnumber),
                                                              Project(self.projectname, self.projectversion))
        self.reporting_client = PerfectoReportiumClient(self.perfecto_execution_context)
        self.reporting_client.test_start(test_case_name, TestContext([], "Perforce"))

    def driver_wait(self, time):
        self.driver.implicitly_wait(time)

    def reboot(self):
        params = {}
        print("rebooting..",self.device_model_name)
        self.driver.execute_script('mobile:handset:reboot', params)
        print("rebooting complete !!")


def main():
    parser = argparse.ArgumentParser(prog="interop_tools",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     allow_abbrev=True,
                                     epilog="About interop_tools.py",
                                     description="Tools for Interop")

    parser.add_argument('--device', type=str, help=' --device : device you want to reboot',
                        default="{\"Galaxy S20\": 'Android', \"Galaxy S10.*\": 'Android', \"Galaxy S9\": 'Android', \"Pixel 4\": 'Android',\"iPhone-12\": 'iOS', \"iPhone-11\": 'iOS', \"iPhone-7\" : 'iOS'}")

    parser.add_argument('--project_name', type=str, help='', default="TIP-test-Execution")
    parser.add_argument('--job_name', type=str, help='', default="reboot-devices")
    parser.add_argument('--job_number', type=int, help='', default=1)
    parser.add_argument('--test_tag', type=str, help='', default="TIP-PyTest-Execution")
    parser.add_argument('--test_case_name', type=str, help='', default="reboot")

    args = parser.parse_args()
    devices = args.device
    print(devices)
    device = ast.literal_eval(devices)
    job_name = args.job_name
    job_number = args.job_number
    test_tag = args.test_tag
    test_case_name = args.test_case_name


    for device_name,platform in device.items():
        try:
            perfecto_tool = perfecto_tools(device=device_name,
                                           platform_name=platform,
                                           job_name=job_name,
                                           job_number=job_number,
                                           test_tag=test_tag,
                                           test_case_name=str(test_case_name+"-"+device_name))
            try:
                perfecto_tool.reboot()
                perfecto_tool.reporting_client.test_stop(TestResultFactory.create_success())
            except:
                print("Reboot Failed !")
                perfecto_tool.reporting_client.test_stop(TestResultFactory.create_failure("Failed!"))
            finally:
                try:
                    perfecto_tool.driver.close()
                except:
                    print("not able to close the driver")
                try:
                    perfecto_tool.driver.quit()
                except:
                    print("not able to quit the driver")
        except:
            print("Failed to get Driver")


if __name__ == '__main__':
    main()
