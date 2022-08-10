import os
import re
from ast import Str
from logging import exception
import unittest
import warnings

import urllib3
from _pytest.outcomes import fail
from appium.webdriver import webdriver
from perfecto.model.model import Job, Project
from perfecto import (PerfectoExecutionContext, PerfectoReportiumClient, TestContext, TestResultFactory)
import pytest
import sys
import time
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support import expected_conditions as EC
import allure
from perfecto_interop import perfecto_interop
class ios_libs(perfecto_interop):
    global driver, perfecto_execution_context, deviceModel
    def __init__(self, perfecto_data=None, dut_data=None):
        super().__init__(perfecto_data=perfecto_data, dut_data=dut_data)
        self.perfecto_data = perfecto_data
        self.dut_data = dut_data
        pass

    def openApp(self, appName, setup_perfectoMobile):
        setup_perfectoMobile[1].step_start("Opening App: " + appName)
        params = {'identifier': appName}
        # Open/Close/Open Action is performed to ensure the app is back to its Original Settings
        setup_perfectoMobile[0].execute_script('mobile:application:open', params)
        setup_perfectoMobile[0].execute_script('mobile:application:close', params)
        setup_perfectoMobile[0].execute_script('mobile:application:open', params)

    def scrollDown(self, setup_perfectoMobile):
        print("Scroll Down")
        setup_perfectoMobile[1].step_start("Scroll Down")
        params2 = {}
        params2["start"] = "50%,90%"
        params2["end"] = "50%,20%"
        params2["duration"] = "4"
        # time.sleep(2)
        setup_perfectoMobile[0].execute_script('mobile:touch:swipe', params2)
        time.sleep(3)

    def closeApp(self, appName, setup_perfectoMobile):
        # print("Closing App.." + appName)
        setup_perfectoMobile[1].step_start("Closing App: " + appName)
        params = {'identifier': appName}
        setup_perfectoMobile[0].execute_script('mobile:application:close', params)
    def setup_perfectoMobile_iOS(self):
        global perfecto_execution_context, driver, deviceModel
        driver = None
        reporting_client = None
        get_device_configuration = self.get_device_configuration()
        warnings.simplefilter("ignore", ResourceWarning)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        capabilities = {
            'platformName': get_device_configuration["platformName-iOS"],
            'model': get_device_configuration["model-iOS"],
            'browserName': 'safari',
            # 'automationName' : 'Appium',
            'securityToken': self.perfecto_data["securityToken"],
            'useAppiumForWeb': 'false',
            'autoAcceptAlerts': 'true',
            # 'bundleId' : request.config.getini("bundleId-iOS"),
            'useAppiumForHybrid': 'false',
        }

        # Check if the device is available
        if not self.is_device_Available_timeout(capabilities['model']):
            print("Unable to get device.")
            pytest.exit("Exiting Pytest")

        driver = webdriver.Remote(
            'https://' + self.perfecto_data["perfectoURL"] + '.perfectomobile.com/nexperience/perfectomobile/wd/hub',
            capabilities)
        driver.implicitly_wait(2)

        # TestCaseFullName = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
        # nCurrentTestMethodNameSplit = re.sub(r'\[.*?\]\ *', "", TestCaseFullName)
        # try:
        #     # TestCaseName = nCurrentTestMethodNameSplit.removeprefix('test_')
        #     TestCaseName = nCurrentTestMethodNameSplit.replace('test_', '')
        #     print("\n\nExecuting TestCase: " + TestCaseName)
        # except Exception as e:
        #     TestCaseName = nCurrentTestMethodNameSplit
        #     print("\nUpgrade Python to 3.9 to avoid test_ string in your test case name, see below URL")
        #     # print("https://www.andreagrandi.it/2020/10/11/python39-introduces-removeprefix-removesuffix/")

        projectname = self.perfecto_data["projectName"]
        projectversion = self.perfecto_data["projectVersion"]
        jobname = get_device_configuration["jobName"]
        jobnumber = get_device_configuration["jobNumber"]
        tags = self.perfecto_data["reportTags"]
        testCaseName = "TestCaseName_hari_ios_check"

        print("\nSetting Perfecto ReportClient....")
        perfecto_execution_context = PerfectoExecutionContext(driver, tags, Job(jobname, jobnumber),
                                                              Project(projectname, projectversion))
        reporting_client = PerfectoReportiumClient(perfecto_execution_context)
        reporting_client.test_start(testCaseName, TestContext([], "Perforce"))
        self.report_client(reporting_client)
        try:
            params = {'property': 'model'}
            deviceModel = driver.execute_script('mobile:handset:info', params)
        except:
            pass

        # request.addfinalizer(teardown)

        if driver is None:
            yield -1
        else:
            yield driver, reporting_client

    def teardown(self):
        global driver, perfecto_execution_context, deviceModel
        reporting_client = PerfectoReportiumClient(perfecto_execution_context)
        try:
            print("\n---------- Tear Down ----------")
            print('Report-Url: ' + reporting_client.report_url())
            try:
                allure.dynamic.link(
                    str(reporting_client.report_url()),
                    name=str(deviceModel))
            except:
                print("fail to attach video link")
            print("----------------------------------------------------------\n\n\n\n")
            driver.close()
        except Exception as e:
            print(" -- Exception While Tear Down --")
            driver.close()
            print(e)
        finally:
            try:
                driver.quit()
            except Exception as e:
                print(" -- Exception Not Able To Quit --")
                print(e)

    def get_all_available_ssids(self, driver):
        print("\n----------------------------")
        print("Get All Available SSID")
        print("------------------------------")

        active_ssid_list = []
        try:
            time.sleep(2)
            driver.implicitly_wait(2)
            elements = driver.find_elements_by_xpath("(//*[@label='More Info']/parent::*/XCUIElementTypeStaticText)")
            print(len(elements))
            for i in range(len(elements)):
                active_ssid_list.append(elements[i].text)
            print("active_ssid_list: ", active_ssid_list)
        except:
            print("No SSIDS available")

        return active_ssid_list

    def ssid_Visible(self, driver, WifiName):
        wifiSelectionElement = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='" + WifiName + "']")))
        isVisible = wifiSelectionElement.get_attribute("visible")
        print(f"Is ssid visible: {isVisible}")
        if (isVisible == 'false'):
            return False
        else:
            return True

    def scrollDown(self, setup_perfectoMobile):
        print("Scroll Down")
        setup_perfectoMobile[1].step_start("Scroll Down")
        params2 = {}
        params2["start"] = "50%,90%"
        params2["end"] = "50%,20%"
        params2["duration"] = "4"
        # time.sleep(2)
        setup_perfectoMobile[0].execute_script('mobile:touch:swipe', params2)
        time.sleep(3)

if __name__ == '__main__':
    perfecto_data = {
        "securityToken": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJpYXQiOjE2MzI4Mzc2NDEsImp0aSI6IjAwZGRiYWY5LWQwYjMtNDRjNS1hYjVlLTkyNzFlNzc5ZGUzNiIsImlzcyI6Imh0dHBzOi8vYXV0aDIucGVyZmVjdG9tb2JpbGUuY29tL2F1dGgvcmVhbG1zL3RpcC1wZXJmZWN0b21vYmlsZS1jb20iLCJhdWQiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwic3ViIjoiODNkNjUxMWQtNTBmZS00ZWM5LThkNzAtYTA0ZjBkNTdiZDUyIiwidHlwIjoiT2ZmbGluZSIsImF6cCI6Im9mZmxpbmUtdG9rZW4tZ2VuZXJhdG9yIiwibm9uY2UiOiI2ZjE1YzYxNy01YTU5LTQyOWEtODc2Yi1jOTQxMTQ1ZDFkZTIiLCJzZXNzaW9uX3N0YXRlIjoiYmRjZTFmYTMtMjlkYi00MmFmLWI5YWMtYjZjZmJkMDEyOTFhIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.5R85_1R38ZFXv_wIjjCIsj8NJm1p66dCsLJI5DBEmks",
        "projectName": "TIP-PyTest-Execution",
        "projectVersion": "1.0",
        "reportTags": "TestTag",
        "perfectoURL": "tip",
        "iPhone-11": {
                        "model-iOS": "iPhone-11",
                        "bundleId-iOS": "com.apple.Preferences",
                        "platformName-iOS": "iOS",
                        "bundleId-iOS-Settings": "com.apple.Preferences",
                        "bundleId-iOS-Ping": "com.deftapps.ping",
                        "browserType-iOS": "Safari",
                        "bundleId-iOS-Safari": "com.apple.mobilesafari",
                        "platformName-android": "Android",
                        "appPackage-android": "com.android.settings",
                        "jobName": "Interop-iphone-11",
                        "jobNumber": 38
                    }
    }
    access_point = [{
            "model": "edgecore_eap101",
            "supported_bands": ["2G", "5G"],
            "upstream_port": "1.1.eth1",
            "supported_modes": ["BRIDGE", "NAT", "VLAN"],
            "ssid": {
                "2g-ssid": "OpenWifi",
                "5g-ssid": "OpenWifi",
                "6g-ssid": "candela6ghz",
                "2g-password": "OpenWifi",
                "5g-password": "OpenWifi",
                "6g-password": "hello123",
                "2g-encryption": "WPA2",
                "5g-encryption": "open",
                "6g-encryption": "WPA3",
                "2g-bssid": "68:7d:b4:5f:5c:31 ",
                "5g-bssid": "68:7d:b4:5f:5c:3c",
                "6g-bssid": "68:7d:b4:5f:5c:38"
            },
            "mode": "wifi6",
            "identifier": "903cb36ae255",
            "serial_port": True,
            "host_ip": "10.28.3.102",
            "host_username": "lanforge",
            "host_password": "pumpkin77",
            "host_ssh_port": 22,
            "serial_tty": "/dev/ttyAP5",
            "firmware_version": "next-latest"
        }]
    obj = ios_libs()