from ast import Str
from logging import exception
import unittest
import warnings
from _pytest.outcomes import fail
from perfecto.test import TestResultFactory
import pytest
import sys
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support import expected_conditions as EC
import allure
from ios_libs import ios_libs

class ios_tests(ios_libs):

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
                    }
    }
    def __init__(self, perfecto_data=None, dut_data=None):
        super().__init__(perfecto_data=perfecto_data, dut_data=dut_data)
        self.perfecto_data = perfecto_data
        self.dut_data = dut_data
        self.setup_perfectoMobile = list(self.setup_perfectoMobile_iOS())
        self.connData = self.get_ToggleAirplaneMode_data(self.ios_devices["iPhone-11"])

    def client_connect_iOS(self, ssid, passkey):
        print("\n-------------------------------------")
        print("Select Wifi/Get IP Address IOS Connection")
        print("-------------------------------------")

        reportFlag = True
        is_internet = False
        ip_address_element_text = False
        WifiName = ssid
        WifiPass = passkey

        print("Verifying Wifi/AP Connection Details....")
        report = self.setup_perfectoMobile[0][1]
        driver = self.setup_perfectoMobile[0][0]

        report.step_start("Switching Driver Context")
        print("Switching Context to Native")
        driver.switch_to.context('NATIVE_APP')
        # driver.switch_to.context(contexts[0])

        report.step_start("Set Wifi Network to " + WifiName)
        # Open Settings Application
        self.openApp(self.connData["bundleId-iOS-Settings"], self.setup_perfectoMobile[0])

        try:
            time.sleep(2)
            driver.implicitly_wait(2)
            try:
                print("Verifying Connected Wifi Connection")
                report.step_start("Loading Wifi Page")
                element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']")
                element.click()
            except NoSuchElementException:
                print("Exception: Verify Xpath - unable to click on Wifi")

            time.sleep(2)
            driver.implicitly_wait(4)
            # --------------------To Turn on WIFi Switch if already OFF--------------------------------
            try:
                get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='0']")
                get_wifi_switch_element_text = get_wifi_switch_element.text
                try:
                    if get_wifi_switch_element_text == "0" or get_wifi_switch_element_text == 0:
                        get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='0']")
                        driver.implicitly_wait(1)
                        get_wifi_switch_element.click()
                        driver.implicitly_wait(1)
                        i = 0
                        for i in range(5):
                            try:
                                get_wifi_switch_element = driver.find_element_by_xpath(
                                    "//*[@label='Wi-Fi' and @value='1']")
                                get_wifi_switch_element_text = get_wifi_switch_element.text
                            except:
                                print("Switch is OFF")

                            if get_wifi_switch_element_text == "1" or get_wifi_switch_element_text == 1:
                                print("WIFI Switch is ON")
                                break
                            else:
                                try:
                                    get_wifi_switch_element = driver.find_element_by_xpath(
                                        "//*[@label='Wi-Fi' and @value='0']")
                                    get_wifi_switch_element_text = get_wifi_switch_element.text
                                except:
                                    print("WIFi switch is ON")
                        if (get_wifi_switch_element_text == "0" or get_wifi_switch_element_text == 0):
                            print("switch is still OFF")
                            self.closeApp(self.connData["bundleId-iOS-Settings"], self.setup_perfectoMobile[0])
                            self.teardown()
                            return ip_address_element_text, is_internet
                    else:
                        print("Switch is Still OFF")
                        self.closeApp(self.connData["bundleId-iOS-Settings"], self.setup_perfectoMobile[0])
                        self.teardown()
                        return ip_address_element_text, is_internet
                except:
                    print("No switch element found")
            except:
                print("get_wifi_switch_element is ON")
            # --------------------To Turn on WIFi Switch if already OFF--------------------------------

        except:
            print("Cannot find WIFI element")
            self.closeApp(self.connData["bundleId-iOS-Settings"], self.setup_perfectoMobile[0])
            self.teardown()
            return ip_address_element_text, is_internet

        # ---------------------This is to Forget current connected SSID-------------------------------
        # ---------------------This to Avoid any popup page from captive portal--------------------#

        try:
            time.sleep(4)
            print("getting in to Additional details")
            report.step_start("Clicking More Info")
            additional_details_element = driver.find_element_by_xpath(
                "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeButton[@label='More Info']")
            additional_details_element.click()
            try:
                time.sleep(2)
                print("Forget Connected Network")
                forget_ssid = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Forget This Network']")))
                forget_ssid.click()
                print("Forget old ssid")
                try:
                    time.sleep(2)
                    report.step_start("Forget SSID popup1")
                    forget_ssid_popup = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Forget']")))
                    forget_ssid_popup.click()

                    print("**alert** Forget SSID popup killed **alert**")
                except:
                    print("Forget SSID popup not found")
            except:
                print("couldn't find forget ssid element")
        except:
            print("No connected SSID")
            try:
                report.step_start("Unexpected Captive Popup")
                print("Unexpeceted Captive Poped Up")
                captive_portal_cancel_element = driver.find_element_by_xpath("//*[@label='Cancel']")
                captive_portal_cancel_element.click()
                time.sleep(2)
                use_other_network_element = driver.find_element_by_xpath("//*[@label='Use Other Network']")
                use_other_network_element.click()
                time.sleep(2)
            except:
                print("No Captive Portal Popup Found")
                try:
                    time.sleep(4)
                    print("getting in to Additional details")
                    report.step_start("Clicking More Info")
                    additional_details_element = driver.find_element_by_xpath(
                        "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeButton[@label='More Info']")
                    additional_details_element.click()
                    try:
                        time.sleep(2)
                        print("Forget Connected Network")
                        forget_ssid = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Forget This Network']")))
                        forget_ssid.click()
                        print("Forget old ssid")
                        try:
                            time.sleep(2)
                            report.step_start("Forget SSID popup1")
                            forget_ssid_popup = WebDriverWait(driver, 30).until(
                                EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Forget']")))
                            forget_ssid_popup.click()

                            print("**alert** Forget SSID popup killed **alert**")
                        except:
                            print("Forget SSID popup not found")
                    except:
                        print("couldn't find forget ssid element")
                except:
                    print("No connected SSID")

        # ---------------------This is to Forget current connected SSID-------------------------------

        # ---------------------To get all available SSID-------------------------------
        print("Searching for Wifi: " + WifiName)
        # allure.attach(name= body=str("Searching for Wifi: " + WifiName))
        time.sleep(2)
        report.step_start("Searching SSID")
        print("Selecting Wifi: " + WifiName)
        ssid_found = False
        available_ssids = False

        try:
            for check_for_all_ssids in range(12):
                available_ssids = self.get_all_available_ssids(driver)
                allure.attach(name="Available SSIDs in device: ", body=str(available_ssids))
                try:
                    if (not self.ssid_Visible(driver, WifiName)) or (WifiName not in available_ssids):
                        self.scrollDown(self.setup_perfectoMobile[0])
                        time.sleep(2)
                    else:
                        try:
                            driver.implicitly_wait(8)
                            report.step_start("Selecting SSID To Connect")
                            ssid_found = True
                            print(WifiName + " : Found in Device")
                            wifiSelElement = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='" + WifiName + "']")))
                            print(wifiSelElement)
                            wifiSelElement.click()
                            print("Selecting SSID")
                            break
                        except:
                            print("SSID unable to select")
                            report.step_start("Selecting Unable SSID To Connect")
                            self.closeApp(self.connData["bundleId-iOS-Settings"], self.setup_perfectoMobile[0])
                            self.teardown()
                            return ip_address_element_text, is_internet

                except:
                    print("couldn't connect to " + WifiName)
                    # request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                    self.closeApp(self.connData["bundleId-iOS-Settings"], self.setup_perfectoMobile[0])
                    self.teardown()
                    return ip_address_element_text, is_internet
                    pass

            if not ssid_found:
                print("could not found " + WifiName + " in device")
                self.closeApp(self.connData["bundleId-iOS-Settings"], self.setup_perfectoMobile[0])
                self.teardown()
                return ip_address_element_text, is_internet
        except:
            pass
        # ---------------------To get all available SSID-------------------------------

        # ---------------------This is to Select SSID-------------------------------

        # ---------------------This is to Select SSID-------------------------------
        # ---------------------Set Password-------------------------------
        try:
            driver.implicitly_wait(5)
            print("Entering Password")
            report.step_start("Entering Password")
            wifiPassword = driver.find_element_by_xpath("//*[@label='Password']")
            wifiPassword.send_keys(WifiPass)
        except NoSuchElementException:
            print("Enter Password Page Not Loaded")
        # ---------------------Set Password-------------------------------

        # ---------------------Click on join-------------------------------
        try:
            driver.implicitly_wait(4)
            print("Selecting join")
            report.step_start("Clicking JOIN")
            joinBTN = driver.find_element_by_xpath("//*[@label='Join']")
            joinBTN.click()
        except Exception as e:
            print("Join Button Not Enabled...Password may not be needed")
        # ---------------------Click on join-------------------------------

        # ---------------------check if internet-------------------------------
        try:
            driver.implicitly_wait(5)
            WifiInternetErrMsg2 = driver.find_element_by_xpath("//*[@label='No Internet Connection']")
            # = driver.find_element_by_xpath("//*[@label='No Internet Connection']").text
        except Exception as e:
            is_internet = True
            print("No Wifi-AP Error Internet Error: " + WifiName)
            # Need to add Wait for Selected Wifi Xpath
            # time.sleep(3)
        # ---------------------check if internet-------------------------------

        # ---------------------Additional INFO-------------------------------
        try:
            driver.implicitly_wait(5)
            print("Selecting SSID: ", WifiName)
            report.step_start("Additional details of SSID")
            additional_details_element = WebDriverWait(driver, 35).until(
                EC.presence_of_element_located((MobileBy.XPATH,
                                                "//*[@label='" + WifiName + "']")))
            # //*[@label='selected']/parent::*/parent::*/XCUIElementTypeButton[@label='More Info']
            additional_details_element.click()

            try:
                driver.implicitly_wait(2)
                report.step_start("Checking SSID Name as Expected")
                print("Checking SSID Name")
                ssidname_text = driver.find_element_by_xpath("//*[@label='" + WifiName + "']").text
                print(ssidname_text)
                if (ssidname_text == WifiName):
                    print("SSID Matched")
                    allure.attach(name="SSID Matched ", body=str(WifiName))
                else:
                    print("SSID Not Matched")
                    allure.attach(name="SSID Not Matched ", body=str(WifiName))
                    reportFlag = False
                    assert reportFlag
            except:
                print("SSID is not Checked in more Info")

            try:
                report.step_start("Checking WiFi Address")
                print("Checking WIFI address")
                # (//*[@label="IP Address"]/parent::*/XCUIElementTypeStaticText)[2]
                wifi_address_element_text = driver.find_element_by_xpath(
                    "(//*[@label='Wi-Fi Address']/parent::*/XCUIElementTypeStaticText)[2]").text
                print("wifi_address_element_text: ", wifi_address_element_text)
                allure.attach(name="Connected SSID WiFi-Address: ", body=str(wifi_address_element_text))
            except Exception as e:
                print("WiFi-Address not Found")
            try:
                time.sleep(4)
                report.step_start("Checking IP Address")
                print("Checking IP address")
                # (//*[@label="IP Address"]/parent::*/XCUIElementTypeStaticText)[2]
                ip_address_element_text = driver.find_element_by_xpath(
                    "(//*[@label='IP Address']/parent::*/XCUIElementTypeStaticText)[2]").text
                print("ip_address_element_text: ", ip_address_element_text)
            except Exception as e:
                try:
                    time.sleep(4)
                    print("Scrolling for checking ip address")
                    self.scrollDown(self.setup_perfectoMobile[0])
                    ip_address_element_text = driver.find_element_by_xpath(
                        "(//*[@label='IP Address']/parent::*/XCUIElementTypeStaticText)[2]").text
                    print("ip_address_element_text: ", ip_address_element_text)
                except:
                    print("IP Address not Found")

            try:
                report.step_start("Forget Network")
                forget_ssid = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Forget This Network']")))
                forget_ssid.click()
                print("Forget old ssid")
                # time.sleep(2)
                # driver.implicitly_wait(3)
                try:
                    report.step_start("Forget Network popup")
                    forget_ssid_popup = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Forget']")))
                    forget_ssid_popup.click()
                except:
                    print("in popup exception")

            except:
                print("error on ssid element")

                # --------------------To Turn on WIFi Switch if already OFF--------------------------------
            # try:
            #     get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='1']")
            #     get_wifi_switch_element_text = get_wifi_switch_element.text
            #     print("switch state is : ", get_wifi_switch_element_text)
            #     try:
            #         if get_wifi_switch_element_text == "1" or get_wifi_switch_element_text == 1:
            #             get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='1']")
            #             driver.implicitly_wait(1)
            #             get_wifi_switch_element.click()
            #             driver.implicitly_wait(1)
            #             i = 0
            #             for i in range(5):
            #                 try:
            #                     get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='0']")
            #                     get_wifi_switch_element_text = get_wifi_switch_element.text
            #                 except:
            #                     print("switch is ON")
            #
            #                 if get_wifi_switch_element_text == "0" or get_wifi_switch_element_text == 0:
            #                     print("WIFI Switch is OFF")
            #                     break
            #                 else:
            #                     try:
            #                         get_wifi_switch_element = driver.find_element_by_xpath(
            #                             "//*[@label='Wi-Fi' and @value='1']")
            #                         get_wifi_switch_element.click()
            #                         get_wifi_switch_element_text = get_wifi_switch_element.text
            #                     except:
            #                         print("WIFi switch is OFF")
            #
            #         else:
            #             print("Switch is Still OFF")
            #     except:
            #         pass
            # except:
            #     print("get_wifi_switch_element is ON")
            # --------------------To Turn on WIFi Switch if already OFF--------------------------------

        except Exception as e:
            print("Select Additional Info failed")
        # ---------------------Additional INFO-------------------------------

        # --------------------- close app-------------------------------
        self.closeApp(self.connData["bundleId-iOS-Settings"], self.setup_perfectoMobile[0])
        self.teardown()
        return ip_address_element_text, is_internet
        # ---------------------close app-------------------------------

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
    obj = ios_tests(perfecto_data=perfecto_data, dut_data=access_point)
    print(obj.client_connect_iOS("stress_open_2g", "something"))