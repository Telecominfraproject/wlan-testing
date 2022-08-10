import logging
import os
import re
import warnings
from perfecto.model.model import Job, Project
from perfecto import (PerfectoExecutionContext, PerfectoReportiumClient, TestContext, TestResultFactory)
import allure
import pytest
import requests
import urllib3
from time import gmtime, strftime
import time
from xml.etree import ElementTree as ET
from appium import webdriver
class perfecto_interop:
    dut_data = list()
    security_token = None
    perfecto_data = dict()
    android_devices = {
        "Galaxy S20": {
            "platformName-android": "Android",
            "model-android": "Galaxy S20",
            "appPackage-android": "com.android.settings",
            "bundleId-iOS-Settings": "com.apple.Preferences",
            "bundleId-iOS-Safari": "com.apple.mobilesafari",
            "jobName": "Interop-Galaxy-S20",
            "jobNumber": 38
        },
        "Galaxy S10.*": {
            "platformName-android": "Android",
            "model-android": "Galaxy S10.*",
            "appPackage-android": "com.android.settings",
            "bundleId-iOS-Settings": "com.apple.Preferences",
            "bundleId-iOS-Safari": "com.apple.mobilesafari",
            "jobName": "Interop-Galaxy-S10",
            "jobNumber": 38
        },
        "Galaxy S9": {
            "platformName-android": "Android",
            "model-android": "Galaxy S9",
            "appPackage-android": "com.android.settings",
            "bundleId-iOS-Settings": "com.apple.Preferences",
            "bundleId-iOS-Safari": "com.apple.mobilesafari",
            "jobName": "Interop-Galaxy-S9",
            "jobNumber": 38
        },
        "Pixel 4": {
            "platformName-android": "Android",
            "model-android": "Pixel 4",
            "appPackage-android": "com.android.settings",
            "bundleId-iOS-Settings": "com.apple.Preferences",
            "bundleId-iOS-Safari": "com.apple.mobilesafari",
            "jobName": "Interop-pixel-4",
            "jobNumber": 38
        }
    }
    ios_devices = {
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
    },
        "iPhone-12": {
        "model-iOS": "iPhone-12",
        "bundleId-iOS": "com.apple.Preferences",
        "platformName-iOS": "iOS",
        "bundleId-iOS-Settings": "com.apple.Preferences",
        "bundleId-iOS-Ping": "com.deftapps.ping",
        "browserType-iOS": "Safari",
        "bundleId-iOS-Safari": "com.apple.mobilesafari",
        "platformName-android": "Android",
        "appPackage-android": "com.android.settings",
        "jobName": "Interop-iphone-12",
        "jobNumber": 38
    },
        "iPhone-7": {
        "model-iOS": "iPhone-7",
        "bundleId-iOS": "com.apple.Preferences",
        "platformName-iOS": "iOS",
        "bundleId-iOS-Settings": "com.apple.Preferences",
        "bundleId-iOS-Ping": "com.deftapps.ping",
        "browserType-iOS": "Safari",
        "bundleId-iOS-Safari": "com.apple.mobilesafari",
        "platformName-android": "Android",
        "appPackage-android": "com.android.settings",
        "jobName": "Interop-iphone-7",
        "jobNumber": 38
    },
        "iPhone-XR": {
        "model-iOS": "iPhone-XR",
        "bundleId-iOS": "com.apple.Preferences",
        "platformName-iOS": "iOS",
        "bundleId-iOS-Settings": "com.apple.Preferences",
        "bundleId-iOS-Ping": "com.deftapps.ping",
        "browserType-iOS": "Safari",
        "bundleId-iOS-Safari": "com.apple.mobilesafari",
        "platformName-android": "Android",
        "appPackage-android": "com.android.settings",
        "jobName": "Interop-iphone-XR",
        "jobNumber": 38
    }
    }
    def __init__(self, perfecto_data=None, dut_data=None):
        if perfecto_data is None:
            logging.error("Perfecto data is not provided")
            pytest.exit("Perfecto data is not provided")
        if dut_data is None:
            logging.error("Device Under Test data is not provided")
            pytest.exit("Device Under Test data is not provided")
        self.perfecto_data = perfecto_data
        self.dut_data = dut_data


    def setup_metadata(self):
        pass
    def get_device_configuration(self):
        return self.perfecto_data["iPhone-11"]
    # def get_PassPointConniOS_data(self, get_device_configuration):
    #     passPoint_data = {
    #         "netAnalyzer-inter-Con-Xpath": "//*[@label='Network Connected']/parent::*/XCUIElementTypeButton",
    #         "bundleId-iOS-Settings": get_device_configuration["bundleId-iOS-Settings"],
    #         "bundleId-iOS-Ping": get_device_configuration["bundleId-iOS-Ping"]
    #     }
    #     yield passPoint_data

    # def get_APToMobileDevice_data(get_device_configuration):
    #     passPoint_data = {
    #         "webURL": "https://www.google.com",
    #         "lblSearch": "//*[@class='gLFyf']",
    #         "elelSearch": "(//*[@class='sbic sb43'])[1]",
    #         "BtnRunSpeedTest": "//*[text()='RUN SPEED TEST']",
    #         "bundleId-iOS-Settings": get_device_configuration["bundleId-iOS-Settings"],
    #         "bundleId-iOS-Safari": get_device_configuration["bundleId-iOS-Safari"],
    #         "downloadMbps": "//*[@id='knowledge-verticals-internetspeedtest__download']/P[@class='spiqle']",
    #         "UploadMbps": "//*[@id='knowledge-verticals-internetspeedtest__upload']/P[@class='spiqle']",
    #         # Android
    #         "platformName-android": get_device_configuration["platformName-android"],
    #         "appPackage-android": get_device_configuration["appPackage-android"]
    #     }
    #     yield passPoint_data

    # def get_AccessPointConn_data(get_device_configuration):
    #     passPoint_data = {
    #         "bundleId-iOS-Settings": get_device_configuration["bundleId-iOS-Settings"],
    #         "bundleId-iOS-Ping": get_device_configuration["bundleId-iOS-Ping"]
    #     }
    #     yield passPoint_data

    def get_ToggleAirplaneMode_data(self, get_device_configuration):
        passPoint_data = {
            "webURL": "https://www.google.com",
            "lblSearch": "//*[@class='gLFyf']",
            "elelSearch": "(//*[@class='sbic sb43'])[1]",
            "BtnRunSpeedTest": "//*[text()='RUN SPEED TEST']",
            "bundleId-iOS-Settings": get_device_configuration["bundleId-iOS-Settings"],
            "bundleId-iOS-Safari": get_device_configuration["bundleId-iOS-Safari"],
            "downloadMbps": "//*[@id='knowledge-verticals-internetspeedtest__download']/P[@class='spiqle']",
            "UploadMbps": "//*[@id='knowledge-verticals-internetspeedtest__upload']/P[@class='spiqle']",
            # Android
            "platformName-android": get_device_configuration["platformName-android"],
            "appPackage-android": get_device_configuration["appPackage-android"]
        }
        return passPoint_data

    # def get_ToggleWifiMode_data(get_device_configuration):
    #     passPoint_data = {
    #         # iOS
    #         "bundleId-iOS-Settings": get_device_configuration["bundleId-iOS-Settings"],
    #         # Android
    #         "platformName-android": get_device_configuration["platformName-android"],
    #         "appPackage-android": get_device_configuration["appPackage-android"]
    #     }
    #     yield passPoint_data


    def report_client(self, value):
        global reporting_client  # declare a to be a global
        reporting_client = value  # this sets the global value of a

    def reportPerfecto(testCaseName, testCaseStatus, testErrorMsg, reportURL):
        global testCaseNameList  # declare a to be a global
        global testCaseStatusList
        global testCaseErrorMsg
        global testCaseReportURL

        testCaseNameList.append(testCaseName)
        testCaseStatusList.append(testCaseStatus)
        testCaseErrorMsg.append(str(testErrorMsg))
        testCaseReportURL.append(reportURL)

    def setup_perfectoMobileWeb(self, get_device_configuration):
        from selenium import webdriver
        rdriver = None
        reporting_client = None

        warnings.simplefilter("ignore", ResourceWarning)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        capabilities = {
            'platformName': get_device_configuration["platformName-iOS"],
            'model': get_device_configuration["model-iOS"],
            'browserName': get_device_configuration["browserType-iOS"],
            'securityToken': get_device_configuration["securityToken"],
        }

        if not self.is_device_available_timeout(capabilities['model']):
            print("Unable to get device.")
            pytest.exit("Exiting Pytest")

        rdriver = webdriver.Remote(
            'https://' + self.perfecto_data["perfectoURL"] + '.perfectomobile.com/nexperience/perfectomobile/wd/hub',
            capabilities)
        rdriver.implicitly_wait(2)

        projectname = self.perfecto_data["projectName"]
        projectversion = self.perfecto_data["projectVersion"]
        jobname = get_device_configuration["jobName"]
        jobnumber = get_device_configuration["jobNumber"]
        tags = self.perfecto_data["reportTags"]
        testCaseName = get_device_configuration["jobName"]

        print("Setting Perfecto ReportClient....")
        perfecto_execution_context = PerfectoExecutionContext(rdriver, tags, Job(jobname, jobnumber),
                                                              Project(projectname, projectversion))
        reporting_client = PerfectoReportiumClient(perfecto_execution_context)
        reporting_client.test_start(testCaseName, TestContext([], "Perforce"))

        def teardown():
            try:
                print(" -- Tear Down --")
                reporting_client.test_stop(TestResultFactory.create_success())
                print('Report-Url: ' + reporting_client.report_url() + '\n')
                rdriver.close()
            except Exception as e:
                print(" -- Exception Not Able To close --")
                print(e.message)
            finally:
                try:
                    rdriver.quit()
                except Exception as e:
                    print(" -- Exception Not Able To Quit --")
                    print(e.message)

        # request.addfinalizer(teardown)

        if rdriver is None:
            yield -1
        else:
            yield rdriver, reporting_client

    # Does HTTP GET request to Perfecto cloud and gets response and information related to a headset
    def response_device(self, model):
        securityToken = self.perfecto_data["securityToken"]
        perfectoURL = self.perfecto_data["perfectoURL"]
        url = f"https://{perfectoURL}.perfectomobile.com/services/handsets?operation=list&securityToken={securityToken}&model={model}"
        resp = requests.get(url=url)
        return ET.fromstring(resp.content)

    # Get an attribute value from the handset response
    def get_attribute_device(self, responseXml, attribute):
        try:
            return responseXml.find('handset').find(attribute).text
        except:
            print(f"Unable to get value of {attribute} from response")
            return ""
    
    # Checks to see if a particular handset is available
    def is_device_available(self, model):
        try:
            responseXml = self.response_device(model)
        except:
            print("Unable to get response.")
            raise Exception("Unable to get response.")
        device_available = self.get_attribute_device(responseXml, 'available')
        print("Result:" + device_available)
        if device_available == 'true':
            return True
        else:
            allocated_to = self.get_attribute_device(responseXml, 'allocatedTo')
            print("The device is currently allocated to:" + allocated_to)
            return False

    # Checks whether the device is available or not.If the device is not available rechecks depending upon the

    # Checks whether the device is available or not.If the device is not available rechecks depending upon the
    # 'timerValue' and 'timerThreshold' values.With the current parameters it will check after:10,20,40,80 mins.
    def is_device_Available_timeout(self, model):
        device_available = self.is_device_available(model)
        timerValue = 5
        timerThreshold = 80
        if not device_available:
            while (timerValue <= timerThreshold):
                print("Last checked at:" + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                print(f"Waiting for: {timerValue} min(s)")
                time.sleep(timerValue * 60)
                print("Checking now at:" + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                device_available = self.is_device_available(model)
                if (device_available):
                    return True
                else:
                    timerValue = timerValue + 5

            if (timerValue > timerThreshold):
                return False
            else:
                return True
        else:
            return True

    def get_device_attribuites(self, model, attribute):
        try:
            responseXml = self.response_device(model)
        except:
            print("Unable to get response.")
            raise Exception("Unable to get response.")
        try:
            attribute_value = self.get_attribute_device(responseXml, str(attribute))
        except:
            attribute_value = False
        return attribute_value

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

    obj = perfecto_interop(perfecto_data=perfecto_data, dut_data=access_point)
    x = obj.get_device_configuration()
    obj.setup_perfectoMobile_android()
