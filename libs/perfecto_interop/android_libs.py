import os
import re
import time
import warnings

import allure
import pytest
import urllib3
from appium.webdriver import webdriver
from perfecto.model.model import Job, Project
from perfecto import (PerfectoExecutionContext, PerfectoReportiumClient, TestContext, TestResultFactory)
from perfecto_interop import perfecto_interop
from appium import webdriver
class android_libs(perfecto_interop):
    global driver, perfecto_execution_context

    def __init__(self, perfecto_data=None, dut_data=None):
        super().__init__(perfecto_data=perfecto_data, dut_data=dut_data)
        self.perfecto_data = perfecto_data
        self.dut_data = dut_data
        pass

    def check_if_no_internet_popup(self, driver):
        time.sleep(1)
        driver.implicitly_wait(1)
        try:

            popup = driver.find_element_by_xpath("//*[@resource-id='android:id/alertTitle']")
            popup_text = popup.text

            try:
                if popup_text == "Internet may not be available":
                    print("**alert** popup **alert**")

                    try:
                        driver.implicitly_wait(2)
                        time.sleep(2)
                        kill_popup = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/keep_btn']")
                        kill_popup.click()
                        print("popup killed")
                    except:
                        print("Couldnt kill popup")
                        return False
                else:
                    print("Popup Text is: ", popup_text)
                    print("popup element is: ", popup)
                    return False
            except:
                print("Popup Text is: ", popup_text)
                print("popup element is: ", popup)
                return False
        except:
            pass

    def get_all_available_ssids(self, driver, deviceModelName):
        active_ssid_list = []
        print("Selected Device Model: " + deviceModelName)
        if deviceModelName != ("Pixel 4"):
            try:
                time.sleep(8)
                driver.implicitly_wait(10)
                elements = driver.find_elements_by_xpath("//*[@resource-id='com.android.settings:id/title']")
                # print("elements: ", elements)
                print(len(elements))
                for i in range(len(elements)):
                    # print("elements[i]", elements[i])
                    # print("elements[i].text", elements[i].text)
                    active_ssid_list.append(elements[i].text)
            except:
                print("No SSIDS available")
        else:
            try:
                time.sleep(8)
                driver.implicitly_wait(10)
                elements = driver.find_elements_by_xpath("//*[@resource-id='android:id/title']")
                # print("elements: ", elements)
                print(len(elements))
                for i in range(len(elements)):
                    # print("elements[i]", elements[i])
                    # print("elements[i].text", elements[i].text)
                    try:
                        active_ssid_list.append(elements[i].text)
                    except:
                        print("Encountered a cache SSID which is no longer in the DOM.Moving to next SSID.")
            except:
                print("No SSIDS available")
        return active_ssid_list
    def openApp(self, appName, setup_perfectoMobile):
        print("Refreshing App: " + appName)
        setup_perfectoMobile[1].step_start("Opening App: " + appName)
        params = {'identifier': appName}
        # Open/Close/Open Action is performed to ensure the app is back to its Original Settings
        setup_perfectoMobile[0].execute_script('mobile:application:open', params)
        setup_perfectoMobile[0].execute_script('mobile:application:close', params)
        setup_perfectoMobile[0].execute_script('mobile:application:open', params)

    def closeApp(self, appName, setup_perfectoMobile):
        print("Closing App.." + appName)
        setup_perfectoMobile[1].step_start("Closing App: " + appName)
        params = {'identifier': appName}
        setup_perfectoMobile[0].execute_script('mobile:application:close', params)
        print("Closed App")

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

    def scroll_down_pixel(self, setup_perfectoMobile):
        print("Scroll Down")
        setup_perfectoMobile[1].step_start("Scroll Down")
        params2 = {}
        params2["start"] = "50%,50%"
        params2["end"] = "50%,20%"
        params2["duration"] = "4"
        time.sleep(2)
        setup_perfectoMobile[0].execute_script('mobile:touch:swipe', params2)
        time.sleep(1)

    def scroll_up(self, setup_perfectoMobile):
        print("Scroll up")
        setup_perfectoMobile[1].step_start("Scroll up")
        params2 = {}
        params2["start"] = "50%,20%"
        params2["end"] = "50%,80%"
        params2["duration"] = "2"
        time.sleep(1)
        setup_perfectoMobile[0].execute_script('mobile:touch:swipe', params2)
        time.sleep(1)

    def getDeviceID(self, setup_perfectoMobile):
        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]

        report.step_start("Get DeviceID")
        params = {'property': 'deviceId'}
        deviceID = driver.execute_script('mobile:handset:info', params)
        print("DeviceID: " + deviceID)
        return deviceID

    def getDeviceModelName(self, setup_perfectoMobile):
        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]

        report.step_start("Device Model Name")
        params = {'property': 'model'}
        deviceModel = driver.execute_script('mobile:handset:info', params)
        print("ModelName: " + deviceModel)
        return deviceModel

    def get_phone_information(self, setup_perfectoMobile, search_this):
        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]

        report.step_start("Get DeviceID")
        params = {'property': search_this}
        device_information = driver.execute_script('mobile:handset:info', params)
        print("device information for " + search_this + " is: ", device_information)
        return device_information
    def setup_perfectoMobile_android(self):
        global perfecto_execution_context, driver
        driver = None
        reporting_client = None
        get_device_configuration = self.get_device_configuration()
        print("Device CONFIG:", get_device_configuration)
        warnings.simplefilter("ignore", ResourceWarning)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        capabilities = {
            'platformName': get_device_configuration["platformName-android"],
            'model': get_device_configuration["model-android"],
            'browserName': 'mobileOS',
            # 'automationName' : 'Appium',
            'securityToken': self.perfecto_data["securityToken"],
            'useAppiumForWeb': 'false',
            'useAppiumForHybrid': 'false',
            # 'bundleId' : request.config.getini("appPackage-android"),
        }

        if not perfecto_interop.is_device_Available_timeout(self, capabilities['model']):
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
        testCaseName = "TestCaseName_Hari_check"
        print("-----------------------------------------------")
        print(projectname, projectversion, jobnumber, jobname, tags)
        print("-----------------------------------------------")
        # print("\nSetting Perfecto ReportClient....")
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
        global driver, perfecto_execution_context
        reporting_client = PerfectoReportiumClient(perfecto_execution_context)
        try:
            print("\n---------- Tear Down ----------")
            try:
                params = {'property': 'model'}
                deviceModel = driver.execute_script('mobile:handset:info', params)
                allure.dynamic.link(
                    str(reporting_client.report_url()),
                    name=str(deviceModel))
            except:
                print("fail to attach video link")

            print('Report-Url: ' + reporting_client.report_url())

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

if __name__ == '__main__':
    perfecto_data = {
        "securityToken": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJpYXQiOjE2MzI4Mzc2NDEsImp0aSI6IjAwZGRiYWY5LWQwYjMtNDRjNS1hYjVlLTkyNzFlNzc5ZGUzNiIsImlzcyI6Imh0dHBzOi8vYXV0aDIucGVyZmVjdG9tb2JpbGUuY29tL2F1dGgvcmVhbG1zL3RpcC1wZXJmZWN0b21vYmlsZS1jb20iLCJhdWQiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwic3ViIjoiODNkNjUxMWQtNTBmZS00ZWM5LThkNzAtYTA0ZjBkNTdiZDUyIiwidHlwIjoiT2ZmbGluZSIsImF6cCI6Im9mZmxpbmUtdG9rZW4tZ2VuZXJhdG9yIiwibm9uY2UiOiI2ZjE1YzYxNy01YTU5LTQyOWEtODc2Yi1jOTQxMTQ1ZDFkZTIiLCJzZXNzaW9uX3N0YXRlIjoiYmRjZTFmYTMtMjlkYi00MmFmLWI5YWMtYjZjZmJkMDEyOTFhIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.5R85_1R38ZFXv_wIjjCIsj8NJm1p66dCsLJI5DBEmks",
        "projectName": "TIP-PyTest-Execution",
        "projectVersion": "1.0",
        "reportTags": "TestTag",
        "perfectoURL": "tip",
        "Galaxy S20": {
            "platformName-android": "Android",
            "model-android": "Galaxy S20",
            "appPackage-android": "com.android.settings",
            "bundleId-iOS-Settings": "com.apple.Preferences",
            "bundleId-iOS-Safari": "com.apple.mobilesafari",
            "jobName": "Interop-Galaxy-S20",
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
    obj = android_libs()