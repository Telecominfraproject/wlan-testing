"""
    Controller Library
        1. controller_data/sdk_base_url
        2. login credentials
"""
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

import allure

sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)
if "tests" not in sys.path:
    sys.path.append(f'../../tests')

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

def openApp(appName, setup_perfectoMobile):
    print("Refreshing App: " + appName)
    setup_perfectoMobile[1].step_start("Opening App: " + appName)
    params = {'identifier': appName}
    #Open/Close/Open Action is performed to ensure the app is back to its Original Settings
    setup_perfectoMobile[0].execute_script('mobile:application:open', params)
    setup_perfectoMobile[0].execute_script('mobile:application:close', params)
    setup_perfectoMobile[0].execute_script('mobile:application:open', params)

def closeApp(appName, setup_perfectoMobile):
    print("Closing App.." + appName)
    setup_perfectoMobile[1].step_start("Closing App: " + appName)
    params = {'identifier': appName}
    setup_perfectoMobile[0].execute_script('mobile:application:close', params)

def scrollDown(setup_perfectoMobile):
    print("Scroll Down")
    setup_perfectoMobile[1].step_start("Scroll Down")
    params2 = {}
    params2["start"] = "50%,90%"
    params2["end"] = "50%,20%"
    params2["duration"] = "4"
    time.sleep(5)
    setup_perfectoMobile[0].execute_script('mobile:touch:swipe', params2)
    time.sleep(5)


def getDeviceID(setup_perfectoMobile):
    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    report.step_start("Get DeviceID")
    params = {'property': 'deviceId'}
    deviceID = driver.execute_script('mobile:handset:info', params)
    print("DeviceID: " + deviceID)
    return deviceID

def getDeviceModelName(setup_perfectoMobile):
    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    report.step_start("Device Model Name")
    params = {'property': 'model'}
    deviceModel = driver.execute_script('mobile:handset:info', params)
    print("ModelName: " + deviceModel)
    return deviceModel

def set_APconnMobileDevice_android(request, WifiName, WifiPass, setup_perfectoMobile, connData):
    print("\n-------------------------------------")
    print("Select Wifi/AccessPoint Connection")
    print("-------------------------------------")
    print("Verifying Wifi/AP Connection Details....")
    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    report.step_start("Switching Driver Context")
    print("Switching Context to Native")
    contexts = driver.contexts
    driver.switch_to.context(contexts[0])

    #Open Settings Application
    openApp(connData["appPackage-android"], setup_perfectoMobile)

    deviceModelName = getDeviceModelName(setup_perfectoMobile)
    print ("Selected Device Model: " + deviceModelName)

    if deviceModelName!=("Pixel 4"):

        report.step_start("Set Wifi Network to " + WifiName)
        try:
            print("Verifying Connected Wifi Connection")
            report.step_start("Click Connections")
            connElement = driver.find_element_by_xpath("//*[@text='Connections']")
            connElement.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")

        try:
            print("Get Connected Wifi Name if any")
            report.step_start("Get Connected Wifi Name if any")
            try:
                driver.implicitly_wait(20)
                WifiNameElement = driver.find_element_by_xpath("//*[@resource-id='android:id/summary']")
                Wifi_AP_Name = WifiNameElement.text
                print("Current Wifi Status Name: " + Wifi_AP_Name)
            except NoSuchElementException:
                report.step_start("Checking Wifi Radio Button Status")
                try:
                    driver.implicitly_wait(5)
                    WifiRadioBtnConnections = driver.find_element_by_xpath("//*[@resource-id='android:id/switch_widget' and @content-desc='Wi-Fi' and @text='Off']")
                    report.step_start("Wifi Radio Button Disabled, Enabling Radio Button..")
                    print("Wifi Radio Button Disabled, Enabling Radio Button..")
                    WifiRadioBtnConnections.click()
                except NoSuchElementException:
                    Wifi_AP_Name="Null"
                    driver.implicitly_wait(25)
                    report.step_start("Wifi Radio Button Already Enabled")
                    print("Wifi Radio Button Already Enabled")

        except NoSuchElementException:
            Wifi_AP_Name="Null"
            print("Device not connected to any Wifi")

        report.step_start("Clicking Wi-Fi")
        wifiElement = driver.find_element_by_xpath("//*[@text='Wi-Fi']")
        wifiElement.click()

        if Wifi_AP_Name.__eq__(WifiName):
            print("Wifi Name Matches - Already Connected To: " + Wifi_AP_Name)

            try:
                report.step_start("Verify if Wifi is Connected")
                WifiInternetErrMsg = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")
                print("Wifi Successfully Connected")

            except NoSuchElementException:
                print("Wifi Connection Error: " + WifiName)

        else:

            #print("Set Wifi Radio Button to enabled")
            #try:
            #    report.step_start("Set Wifi Radio Button to enabled")
            #    wifiRadioBtn = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/switch_widget' and @text='Wi-Fi, Off']")
            #    wifiRadioBtn.click()
           # except NoSuchElementException:
           #     report.step_start("Set Wifi Radio Button Already enabled")
             #   print("Radio button Already Enabled")

            print("Selecting Wifi: " + WifiName)
            try:
                report.step_start("Selecting Wifi: " + WifiName)
                wifiSelectionElement = WebDriverWait(driver, 35).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='"+ WifiName + "']")))
                wifiSelectionElement.click()
            except Exception as e:
                print("Exception on Selecting Wifi Network.  Please check wifi Name or signal")
                request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                assert False

            #Set password if Needed
            try:
                report.step_start("Set Wifi Password")
                wifiPasswordElement = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/edittext']")
                wifiPasswordElement.send_keys(WifiPass)
            except NoSuchElementException:
                print("Password Page Not Loaded, password May be cached in the System")

            try:
                report.step_start("Click Connect Button")
                joinBTNElement = driver.find_element_by_xpath("//*[@text='Connect']")
                joinBTNElement.click()
            except NoSuchElementException:
                print("Connect Button Not Enabled...Verify if Password is set properly  ")

            try:
                report.step_start("Verify if Wifi is Connected")
                WifiInternetErrMsg = WebDriverWait(driver, 60).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                print("Wifi Successfully Connected")

            except NoSuchElementException:
                print("Wifi Connection Error: " + WifiName)

    else:

        report.step_start("Set Wifi Network to Pixel" + WifiName)
        try:
            print("Click Network & Internet")
            report.step_start("Click Network & Internet")
            connElement = driver.find_element_by_xpath("//*[@text='Network & internet']")
            connElement.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")

        try:
            print("Get Connected Wifi Name if any")
            report.step_start("Get Connected Wifi Name if any")
            WifiNameElement = WebDriverWait(driver, 35).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='android:id/title' and @text='Wi‑Fi']/parent::*/android.widget.TextView[@resource-id='android:id/summary']")))
            Wifi_AP_Name = WifiNameElement.text
            print("Current Wifi Status Name: " + Wifi_AP_Name)
            WifiNameElement.click()
        except NoSuchElementException:
            Wifi_AP_Name="Null"
            print("Device not connected to any Wifi")

        if Wifi_AP_Name.__eq__(WifiName):
            print("Wifi Name Matches - Already Connected To: " + Wifi_AP_Name)

            try:
                report.step_start("Verify if Wifi is Connected")
                WifiInternetErrMsg = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")
                print("Wifi Successfully Connected")

            except NoSuchElementException:
                print("Wifi Connection Error: " + WifiName)

        else:

            print("Set Wifi Radio Button to enabled")
            try:
                report.step_start("Set Wifi Radio Button to enabled")
                wifiRadioBtn = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/switch_widget' and @text='OFF']")
                wifiRadioBtn.click()
            except NoSuchElementException:
                report.step_start("Set Wifi Radio Button Already enabled")
                print("Radio button Already Enabled")

            print("Selecting Wifi: " + WifiName)
            try:
                report.step_start("Selecting Wifi: " + WifiName)
                wifiSelectionElement = WebDriverWait(driver, 35).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='"+ WifiName + "']")))
                wifiSelectionElement.click()
            except NoSuchElementException:
                print("Exception on Selecting Wifi Network.  Please check wifi Name or signal")

            #Set password if Needed
            try:
                report.step_start("Set Wifi Password")
                wifiPasswordElement = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/password']")
                wifiPasswordElement.send_keys(WifiPass)
            except NoSuchElementException:
                print("Password Page Not Loaded, password May be cached in the System")

            try:
                report.step_start("Click Connect Button")
                joinBTNElement = driver.find_element_by_xpath("//*[@resource-id='android:id/button1' and @text='Connect']")
                joinBTNElement.click()
            except NoSuchElementException:
                print("Connect Button Not Enabled...Verify if Password is set properly  ")

            try:
                report.step_start("Verify if Wifi is Connected")
                WifiInternetErrMsg = WebDriverWait(driver, 35).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='android:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                print("Wifi Successfully Connected")

            except NoSuchElementException:
                print("Wifi Connection Error: " + WifiName)

    closeApp(connData["appPackage-android"], setup_perfectoMobile)

def ForgetWifiConnection(request, setup_perfectoMobile, WifiName, connData):
    print("\n-----------------------------")
    print("Forget Wifi/AP Connection")
    print("-----------------------------")
    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    report.step_start("Switching Driver Context")
    print("Switching Context to Native")
    driver.switch_to.context('NATIVE_APP')
    contexts = driver.contexts
    #print(contexts)

    #Open Settings Application
    openApp(connData["appPackage-android"], setup_perfectoMobile)

    deviceModelName = getDeviceModelName(setup_perfectoMobile)
    print ("Selected Device Model: " + deviceModelName)

    if deviceModelName!=("Pixel 4"):

        report.step_start("Forget Existing Wifi" + WifiName)
        try:
            print("Verifying Connected Wifi Connection")
            report.step_start("Click Connections")
            connElement = driver.find_element_by_xpath("//*[@text='Connections']")
            connElement.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")

        try:
            print("Connected Wifi Name if any")
            report.step_start("Get Connected Wifi Name if any")
            WifiNameElement = driver.find_element_by_xpath("//*[@resource-id='android:id/summary']")
            Wifi_AP_Name = WifiNameElement.text
            print("Connected to Wifi: " + Wifi_AP_Name)
        except NoSuchElementException:
            Wifi_AP_Name="Null"
            print("Device not connected to any Wifi")

        report.step_start("Clicking Wi-Fi")
        wifiElement = driver.find_element_by_xpath("//*[@text='Wi-Fi']")
        wifiElement.click()

        if Wifi_AP_Name.__eq__(WifiName):
            report.step_start("Wifi Name Matches - Already Connected To: " + Wifi_AP_Name)
            print("Wifi Name Matches - Already Connected To: " + Wifi_AP_Name)

            print("Load Wifi Details Page")
            try:
                report.step_start("Load Wifi Details Page")
                WifiInternetDetails = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/wifi_details']")
                WifiInternetDetails.click()
            except NoSuchElementException:
                print("Wifi Connection Error: " + WifiName)

            print("Forget Wifi Network")
            try:
                report.step_start("Forget Wifi Network")
                WifiForget= driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/smallLabel' and @text='Forget']")
                WifiForget.click()
            except NoSuchElementException:
                print("Wifi Connection Error: " + WifiName)

            print("Verify if wifi is disconnected from: " + WifiName)
            try:
                report.step_start("Verify if wifi is disconnected from: " + WifiName)
                WifiDisconnect = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")
                print("Wifi Not disconnected, check xpath for: " + WifiName)
                assert False
            except Exception as e:
                assert True
                print("Wifi Disconnected Successfully: " + WifiName)

        else:
            print("Wifi Does not Match with Wifi: " + WifiName)
            report.step_start("Wifi Does not Match with Wifi: " + WifiName)
            report.step_start("Probably wifi auto connected to another network")
            try:
                report.step_start("Wifi Details Page")
                WifiInternetDetails = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/wifi_details']")
                WifiInternetDetails.click()
            except NoSuchElementException:
                print("Wifi Connection Error: " + WifiName)

            try:
                report.step_start("Forget Wifi Network")
                WifiForget= driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/smallLabel' and @text='Forget']")
                WifiForget.click()
            except NoSuchElementException:
                print("Wifi Connection Error: " + WifiName)

            print("Verify if wifi is disconnected from: " + WifiName)
            try:
                report.step_start("Verify if wifi is disconnected from: " + WifiName)
                #WifiForget= driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")
                print("Wifi Not disconnected, check xpath for: " + WifiName)
                WifiForget = WebDriverWait(driver, 20).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
            except Exception as e:
                assert True
                print("Wifi Disconnected Successfully: " + WifiName)

    else:
        #print("Pixel Custom Code")
        report.step_start("Forget Wifi Network on Pixel" + WifiName)
        try:
            print("Click Network & Internet")
            report.step_start("Click Network & Internet")
            connElement = driver.find_element_by_xpath("//*[@text='Network & internet']")
            connElement.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")

        try:
            print("Get Connected Wifi Name if any")
            report.step_start("Get Connected Wifi Name if any")
            WifiNameElement = WebDriverWait(driver, 35).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='android:id/title' and @text='Wi‑Fi']/parent::*/android.widget.TextView[@resource-id='android:id/summary']")))
            Wifi_AP_Name = WifiNameElement.text
            print("Current Wifi Status Name: " + Wifi_AP_Name)
            WifiNameElement.click()
        except NoSuchElementException:
            Wifi_AP_Name="Null"
            print("Device not connected to any Wifi")


        #print("Wifi Name Matches - Already Connected To: " + Wifi_AP_Name)
        try:
            report.step_start("Wifi More information")
            WifiInternetMoreSettings = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/settings_button_no_background']")
            WifiInternetMoreSettings.click()
        except NoSuchElementException:
            print("Wifi Not Connected to any Wifi Error: " + WifiName)

        try:
            report.step_start("Forget Wifi Network")
            WifiInternetMoreSettings = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/button1' and @text='Forget']")
            WifiInternetMoreSettings.click()
        except NoSuchElementException:
            print("Wifi Connection Error: " + WifiName)


        try:
            report.step_start("Verify if Wifi is Connected")
            WifiInternetErrMsg = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")
            print("Forgot Wifi Error, check xpath")
        except Exception as e:
            print("Wifi Disconnected Successfully: " + WifiName)

    closeApp(connData["appPackage-android"], setup_perfectoMobile)

def Toggle_AirplaneMode_android(request, setup_perfectoMobile, connData):
    print("\n-----------------------")
    print("Toggle Airplane Mode")
    print("-----------------------")
    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    report.step_start("Switching Driver Context")
    print("Switching Context to Native")
    driver.switch_to.context('NATIVE_APP')
    contexts = driver.contexts
    #print(contexts)

    #Open Settings Application
    openApp(connData["appPackage-android"], setup_perfectoMobile)

    deviceModelName = getDeviceModelName(setup_perfectoMobile)
    print ("Selected Device Model: " + deviceModelName)

    airplaneFlag = False

    report.step_start("Click Connections")
    try:
        print("Verifying Connected Wifi Connection")
        report.step_start("Click Connections")
        connElement = driver.find_element_by_xpath("//*[@text='Connections']")
        connElement.click()
    except NoSuchElementException:
        print("Exception: Verify Xpath - Update/check Xpath for Click Connections")

    try:
        report.step_start("Toggle Airplane Mode to On")
        print("Toggle Airplane Mode to On")
        ToggleAirplanEle = driver.find_element_by_xpath("//*[@content-desc='Airplane mode' and @text='Off']")
        ToggleAirplanEle.click()
        airplaneFlag = True

        print("Toggle Airplane Mode to Off")
        ToggleAirplanEle2 = driver.find_element_by_xpath("//*[@content-desc='Airplane mode' and @text='On']")
        ToggleAirplanEle2.click()
    except NoSuchElementException:
        print("Toggle Airplane Exception, Airplane mode may be on Already.")

        try:
            print("Checking to see if Airplane is already enabled")
            report.step_start("Checking to see if Airplane is already enabled")
            connElement = driver.find_element_by_xpath("//*[@content-desc='Airplane mode' and @text='On']")
            airplaneFlag = True
            report.step_start("Disable Airplane Mode")
            connElement.click()

        except NoSuchElementException:
            print("Airplane Mode is On & Off status elements Error, please check xpath or if the Page Loaded")

    return airplaneFlag

def Toggle_WifiMode_android(request, setup_perfectoMobile, WifiName, connData):
    print("\n-----------------------")
    print("Toggle Wifi Mode")
    print("-----------------------")
    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    report.step_start("Switching Driver Context")
    print("Switching Context to Native")
    driver.switch_to.context('NATIVE_APP')
    contexts = driver.contexts
    #print(contexts)

    #Open Settings Application
    openApp(connData["appPackage-android"], setup_perfectoMobile)

    deviceModelName = getDeviceModelName(setup_perfectoMobile)
    print ("Selected Device Model: " + deviceModelName)

    WifiFlag = False

    try:
        report.step_start("Click Connections")
        print("Click Connections")
        connElement = driver.find_element_by_xpath("//*[@text='Connections']")
        connElement.click()
    except NoSuchElementException:
        print("Exception: Verify Xpath - Update/check Xpath for Click Connections")

    try:
        print("Get Connected Wifi Name if any")
        report.step_start("Get Connected Wifi Name if any")
        WifiNameElement = driver.find_element_by_xpath("//*[@resource-id='android:id/summary']")
        Wifi_AP_Name = WifiNameElement.text
        print("Current Wifi Status Name: " + Wifi_AP_Name)
    except NoSuchElementException:
        Wifi_AP_Name="Null"
        print("Device not connected to any Wifi")

    print("Current Selected Wifi: " + Wifi_AP_Name)
    report.step_start("Current Selected Wifi: " + Wifi_AP_Name)

    try:
        report.step_start("Disable Wifi Radio Button")
        print("Disable Wifi Radio Button")
        connElement = driver.find_element_by_xpath("//*[@content-desc='Wi-Fi' and @text='On']")
        connElement.click()
    except NoSuchElementException:
        print("Exception: Verify Xpath - Update/check Xpath for Wifi Radio Button")

    try:
        print("Get Connected Wifi Name if any after Wifi Radio is disabled")
        report.step_start("Get Connected Wifi Name if any after Wifi Radio is disabled")
        WifiNameElement = driver.find_element_by_xpath("//*[@resource-id='android:id/summary']")
        Wifi_AP_Name2 = WifiNameElement.text
        print("Device Connected to Wifi: " + Wifi_AP_Name2)
    except NoSuchElementException:
        Wifi_AP_Name2="Null"
        print("Device connected to Wifi: " + Wifi_AP_Name2)

    try:
        report.step_start("Enable Wifi Radio Button")
        print("Enable Wifi Radio Button")
        wifiRadioBTN_Off = driver.find_element_by_xpath("//*[@content-desc='Wi-Fi' and @text='Off']")
        wifiRadioBTN_Off.click()
    except NoSuchElementException:
        print("Exception: Verify Xpath - Update/check Xpath for Wifi Radio Button")

    try:
        print("Get Connected Wifi Name if any after Wifi Radio is Enabled")
        report.step_start("Get Connected Wifi Name if any after Wifi Radio is disabled")
        WifiNameElement3 = WebDriverWait(driver, 35).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='android:id/summary']")))
        Wifi_AP_Name3 = WifiNameElement3.text
        print("Current Wifi Status Name: " + Wifi_AP_Name3)
    except NoSuchElementException and TimeoutException:
        Wifi_AP_Name3="Null"
        print("Device did not connect back to Wifi: " + WifiName)

    if Wifi_AP_Name3.__eq__(WifiName):
        WifiFlag = True
    else:
        WifiFlag = False

    return WifiFlag

def verifyUploadDownloadSpeed_android(request, setup_perfectoMobile, get_APToMobileDevice_data):
    print("\n-------------------------------------")
    print("Verify Upload & Download Speed")
    print("-------------------------------------")

    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]
    connData = get_APToMobileDevice_data

    currentResult=False

    driver.switch_to.context('WEBVIEW_1')

    try:
        print("Launching Chrome")
        report.step_start("Google Home Page")
        driver.get(connData["webURL"])
        print("Enter Search Text")
        elementFindTxt = driver.find_element_by_xpath(connData["lblSearch"])
        elementFindTxt.send_keys("Internet Speed Test")
    except Exception as e:
        print("Launching Chrome Failed")
        print (e)
        # allure.attach(name="Speed Test logs: ", body=str("Launching Safari Failed"))
        # allure.attach(name="Speed Test logs: ", body=str("Error log: " + e))

    try:
        print("Click Search Button")
        report.step_start("Click Search Button")
        time.sleep(2)
        driver.implicitly_wait(2)
        elelSearch = driver.find_element_by_xpath("//*[@class='aajZCb']//*[@class='nz2CCf']/li[1]/div[2]")
        elelSearch.click()
    except:
        try:
            time.sleep(2)
            driver.implicitly_wait(2)
            elelSearch = driver.find_element_by_xpath("//*[@class='aajZCb']//*[@class='nz2CCf']/li[1]/div[2]")
            elelSearch.click()
        except:
            print("Search Drop Down not active...")
            return False

    try:
        print("Click Run Speed Test Button...")
        report.step_start("Click Run Speed Test Button")
        driver.find_element_by_xpath(connData["BtnRunSpeedTest"]).click()
    except NoSuchElementException:
        print("Error in speed test element ", NoSuchElementException)
        # allure.attach(name="Speed Test logs: ", body=str("Search Run Speed Test not active..." + NoSuchElementException))
        return False

    #Get upload/Download Speed
    try:
        print("Get Download Speed")
        report.step_start("Get upload/Download Speed")
        time.sleep(60)
        downloadMbps = driver.find_element_by_xpath(connData["downloadMbps"])
        downloadSpeed = downloadMbps.text
        print("Download: " + downloadSpeed + " Mbps")

        print("Get Upload Speed")
        report.step_start("Get Upload Speed")
        UploadMbps = driver.find_element_by_xpath(connData["UploadMbps"])
        uploadSpeed = UploadMbps.text
        print("Upload: " + uploadSpeed + " Mbps")
        allure.attach(name="Speed Test logs: ", body=str("Upload: " + uploadSpeed + " Mbps" + "  Download: " + downloadSpeed + " Mbps"))
        print("Access Point Verification Completed Successfully")
        currentResult = True
    except NoSuchElementException:
        print("Access Point Verification NOT Completed, checking Connection....")

    return currentResult

def downloadInstallOpenRoamingProfile(request, profileDownloadURL, setup_perfectoMobile, connData):
    print("\n-------------------------------------")
    print("Installing Android Profile ")
    print("-------------------------------------")

    OpenRoamingWifiName = ""

    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    driver.switch_to.context('WEBVIEW_1')

    print("Launching Chrome with OpenRoaming Profile")
    report.step_start("Open Roaming Download Page")
    driver.get(profileDownloadURL)

    try:
        print("Accept Popup")
        report.step_start("Accept Popup")
        driver.switch_to.context('NATIVE_APP')
        WebDriverWait(driver, 40).until(EC.alert_is_present(), 'Time out confirmation popup to appear')
        alert = driver.switch_to.alert
        alert.accept()
        print("Alert Accepted")
    except TimeoutException:
        print("no alert")
        #//*[@resource-id="android:id/button1"]
    #Open Settings Application
    #openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

def deleteOpenRoamingInstalledProfile(request, profileName, setup_perfectoMobile, connData):
    print("\n-----------------------------")
    print("Delete Open Roaming Profile")
    print("-----------------------------")

    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    report.step_start("Switching Driver Context")
    print("Switching Context to Native")
    driver.switch_to.context('NATIVE_APP')
    contexts = driver.contexts

    #Open Settings Application
    openApp(connData["appPackage-android"], setup_perfectoMobile)

    deviceModelName = getDeviceModelName(setup_perfectoMobile)

    if deviceModelName!=("Pixel 4"):
        #Not a pixel Device
        print ("Selected Device Model: " + deviceModelName)
        report.step_start("Forget Profile: " + profileName)

        # three dotss
        #//*[@resource-id='com.android.settings:id/round_corner']
        try:
            print("Click Connections")
            report.step_start("Click Connections")
            connElement = driver.find_element_by_xpath("//*[@text='Connections']")
            connElement.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")

        try:
            report.step_start("Clicking Wi-Fi")
            wifiElement = driver.find_element_by_xpath("//*[@text='Wi-Fi']")
            wifiElement.click()
        except NoSuchElementException:
            print("Exception: Clicking Wi-Fi - Update/check Xpath for Click Wifi Connection ")

        try:
            print ("Click Advanced Menu 3 Dot")
            report.step_start("Click Advanced Menu 3 Dot")
            ThreeDotMenuBtn = driver.find_element_by_xpath("//*[@content-desc='More options']")
            ThreeDotMenuBtn.click()
        except NoSuchElementException:
            print("Exception: Click Advanced Menu Not Loaded")

        # Click Advanced
        # //*[@text='Advanced']
        try:
            print ("Click Advanced")
            report.step_start("Click Advanced")
            AdvBtn = driver.find_element_by_xpath("//*[@text='Advanced']")
            AdvBtn.click()
        except NoSuchElementException:
            print("Exception: Click Advanced")

        #Scroll Down
        scrollDown(setup_perfectoMobile)

        #Click HotSpot
        #//*[@text="Hotspot 2.0"]
        try:
            print ("Click HotSpot")
            report.step_start("Click HotSpot")
            HotSpotBtn = driver.find_element_by_xpath("//*[@text='Hotspot 2.0']")
            HotSpotBtn.click()
        except NoSuchElementException:
            print("Exception: Click HotSpot")

        #Click Ameriband
        #//*[@text="Ameriband"]
        try:
            print ("Click Ameriband")
            report.step_start("Click Ameriband")
            AmeribandXpath = "//*[@text='Ameriband']"
            AmeribandBtn = WebDriverWait(driver, 25).until(EC.presence_of_element_located((MobileBy.XPATH, AmeribandXpath)))
            AmeribandBtn.click()

        except NoSuchElementException and TimeoutException and Exception:
            report.step_start("Exception: Profile Don't Exist")
            print("Exception: Profile Don't Exist")

        #Click Forget
        #//*[@resource-id="com.android.settings:id/icon"]
        try:
            print ("Click Forget")
            report.step_start("Click Forget")
            ForgetBTN = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/icon']")
            ForgetBTN.click()
        except NoSuchElementException:
            print("Exception: Click Forget")

        #Click Forget Confirm
        #//*[@resource-id="android:id/button1"]
        try:
            print ("Click Forget Confirm")
            report.step_start("Click Forget Confirm")
            ForgetConfirm = driver.find_element_by_xpath("//*[@resource-id='android:id/button1']")
            ForgetConfirm.click()
        except NoSuchElementException:
            print("Exception: Click Forget Confirm")

    else:
        #Pixel Device
        print ("Pixel Device Not supported: " + deviceModelName)
        report.step_start("Pixel Device Not supported: ")
        assert False

    closeApp(connData["appPackage-android"], setup_perfectoMobile)

def verify_APconnMobileDevice_Android(request, profileNameSSID, setup_perfectoMobile, connData):
    print("\n-----------------------------")
    print("Verify Connected Network ")
    print("-----------------------------")

    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    report.step_start("Switching Driver Context")
    print("Switching Context to Native")
    driver.switch_to.context('NATIVE_APP')
    contexts = driver.contexts

    #Open Settings Application
    openApp(connData["appPackage-android"], setup_perfectoMobile)

    deviceModelName = getDeviceModelName(setup_perfectoMobile)

    if deviceModelName!=("Pixel 4"):
        #Not a pixel Device
        print ("Selected Device Model: " + deviceModelName)

        report.step_start("Click Connections")
        try:
            print("Click Connections")
            report.step_start("Click Connections")
            connElement = driver.find_element_by_xpath("//*[@text='Connections']")
            connElement.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")

        print("Clicking Wi-Fi")
        report.step_start("Clicking Wi-Fi")
        wifiElement = driver.find_element_by_xpath("//*[@text='Wi-Fi']")
        wifiElement.click()

        try:
            print("Verify if Wifi is Connected to: " + profileNameSSID)
            report.step_start("Verify if Wifi is Connected: " + profileNameSSID)
            #WifiInternetErrMsg = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + profileNameSSID + "']")
            WifiInternetErrMsg = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='Ameriband']")
            print("Wifi Successfully Connected")

        except NoSuchElementException:
            print("Wifi Connection Error: " + profileNameSSID)
            report.step_start("Wifi Connection Error: " + profileNameSSID)
            assert False

    else:
        #Pixel Device
        print ("Pixel Device Not supported: " + deviceModelName)
        report.step_start("Pixel Device Not supported: ")
        assert False

    closeApp(connData["appPackage-android"], setup_perfectoMobile)

    # Cache_clear Function

def cache_clear_android(request, setup_perfectoMobile, connData):
    print("\n-------------------------------------")
    print("Select Cache Clear")
    print("-------------------------------------")
    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    report.step_start("Switching Driver Context")
    print("Switching Context to Native")
    contexts = driver.contexts
    driver.switch_to.context(contexts[0])

    # Open Settings Application
    openApp(connData["appPackage-android"], setup_perfectoMobile)

    deviceModelName = getDeviceModelName(setup_perfectoMobile)
    print("Selected Device Model: " + deviceModelName)

    if deviceModelName != ("Pixel 4" and "Galaxy S9"):
        try:
            print("Clicking Search button")
            report.step_start("Click Search")
            conn_ele = driver.find_element_by_xpath("//*[@content-desc='Search']")
            conn_ele.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Search")

        try:
            driver.implicitly_wait(30)
            print("Entering Chrome in Search")
            report.step_start("Entering text Chrome")
            search_ele = driver.find_element_by_xpath("//*[@resource-id='com.android.settings.intelligence:id/search_src_text']")
            search_ele.send_keys("chrome")
        except Exception as e:
            print("Exception: Entering chrome failed")
            print(e)

        try:
            driver.implicitly_wait(40)
            print("Clicking Chrome App Info")
            report.step_start("Click Chrome App Info")
            chrome_ele = driver.find_element_by_xpath("//*[@text='Chrome']")
            chrome_ele.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Chrome")

        # Scroll Down
        scrollDown(setup_perfectoMobile)

        try:
            driver.implicitly_wait(30)
            print("Clicking Storage")
            report.step_start("Click Storage")
            store_ele = driver.find_element_by_xpath("//*[@text='Storage']")
            store_ele.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Storage")

        try:
            driver.implicitly_wait(30)
            print("Clicking Clear Cache")
            report.step_start("Click Clear Cache")
            clear_ele = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/button2']")
            clear_ele.click()
            print("Cleared Cache")
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Clearcache")

        try:
            driver.implicitly_wait(30)
            print("Checking if cache cleared or not with 0B")
            report.step_start("Checking if cache cleared or not with 0B")
            check_ele = driver.find_element_by_xpath("//*[@text='0 B']")
            if check_ele is not None:
                return True
            else:
                return False
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Checking cache clear")

    elif deviceModelName == ("Pixel 4"):
        # Pixel cache clear code
        try:
            print("Clicking Search button")
            report.step_start("Click Search")
            conn_ele = driver.find_element_by_xpath("//*[@class='android.widget.ImageButton']")
            conn_ele.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Search")

        try:
            driver.implicitly_wait(30)
            print("Entering Chrome in Search")
            report.step_start("Entering text Chrome")
            search_ele = driver.find_element_by_xpath("//*[@resource-id='android:id/search_src_text']")
            search_ele.send_keys("chrome")
        except Exception as e:
            print("Exception: Entering chrome failed")
            print(e)

        try:
            driver.implicitly_wait(35)
            print("Clicking Chrome App Info")
            report.step_start("Click Chrome App Info")
            chrom_ele = driver.find_element_by_xpath("//*[@text='Chrome']")
            chrom_ele.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Chrome")

        try:
            driver.implicitly_wait(30)
            print("Clicking Storage & cache")
            report.step_start("Click Storage & cache")
            store_ele = driver.find_element_by_xpath("//*[@text='Storage & cache']")
            store_ele.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Storage & cache")

        try:
            driver.implicitly_wait(30)
            print("Clicking Clear Cache")
            report.step_start("Click Clear Cache")
            clear_ele = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/button2']")
            clear_ele.click()
            print("Cleared cache")
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Clearcache")

        try:
            driver.implicitly_wait(30)
            print("Checking if cache cleared or not with 0B")
            report.step_start("Checking if cache cleared or not with 0B")
            store_ele = driver.find_element_by_xpath("//*[@text='0 B']")
            if store_ele is not None:
                return True
            else:
                return False
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Checking cache clear")

    else:
        try:
            print("Clicking Search button")
            report.step_start("Click Search")
            conn_ele = driver.find_element_by_xpath("//*[@content-desc='Search settings']")
            conn_ele.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Search")

        try:
            driver.implicitly_wait(30)
            print("Entering Chrome in Search")
            report.step_start("Entering text Chrome")
            search_ele = driver.find_element_by_xpath(
                "//*[@resource-id='com.android.settings.intelligence:id/search_src_text']")
            search_ele.send_keys("chrome")
        except Exception as e:
            print("Exception: Entering chrome failed")
            print(e)

        try:
            driver.implicitly_wait(40)
            print("Clicking Chrome App Info")
            report.step_start("Click Chrome App Info")
            chrome_ele = driver.find_element_by_xpath("//*[@text='Chrome']")
            chrome_ele.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Chrome")

        # Scroll Down
        scrollDown(setup_perfectoMobile)

        try:
            driver.implicitly_wait(30)
            print("Clicking Storage")
            report.step_start("Click Storage")
            store_ele = driver.find_element_by_xpath("//*[@text='Storage']")
            store_ele.click()
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Storage")

        try:
            driver.implicitly_wait(30)
            print("Clicking Clear Cache")
            report.step_start("Click Clear Cache")
            clear_ele = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/button2']")
            clear_ele.click()
            print("Cleared Cache")
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Clearcache")

        try:
            driver.implicitly_wait(30)
            print("Checking if cache cleared or not with 0B")
            report.step_start("Checking if cache cleared or not with 0B")
            check_ele = driver.find_element_by_xpath("//*[@text='0 B']")
            if check_ele is not None:
                return True
            else:
                return False
        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Checking cache clear")


    closeApp(connData["appPackage-android"], setup_perfectoMobile)

def check_if_no_internet_popup(driver):#To check and kill if any popups related to no internet
    time.sleep(1)
    driver.implicitly_wait(1)
    try:

        popup = driver.find_element_by_xpath("//*[@resource-id='android:id/alertTitle']")
        popup_text = popup.text

        try:
            if popup_text == "Internet may not be available":
                print("**alert** popup **alert**")

                try:
                    driver.implicitly_wait(3)
                    time.sleep(2)
                    kill_popup = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/keep_btn']")
                    kill_popup.click()
                    print("popup killed")
                except:
                    print("Couldnt kill popup")
                    return False
            else:
                print("Popup Text is: ", popup_text)
                print("popup element is: ",popup)
                return False
        except:
            print("Popup Text is: ", popup_text)
            print("popup element is: ", popup)
            return False
    except:
        pass

#To get an IP address
def get_ip_address_and(request, WifiName, WifiPass, setup_perfectoMobile, connData):
    print("\n-------------------------------------")
    print("Select Wifi/AccessPoint Connection")
    print("-------------------------------------")
    print("Verifying Wifi Connection Details....")
    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    ip_address_element_text = False
    ssid_with_internet = False

    report.step_start("Switching Driver Context")
    print("Switching Context to Native")
    contexts = driver.contexts
    driver.switch_to.context(contexts[0])

    # Open Settings Application
    openApp(connData["appPackage-android"], setup_perfectoMobile)
    deviceModelName = getDeviceModelName(setup_perfectoMobile)
    print("Selected Device Model: " + deviceModelName)

    if deviceModelName != ("Pixel 4"):
        report.step_start("Set Wifi Network to " + WifiName)


        # -----------------To Open Connections page-----------------------
        try:
            print("Verifying Connected Wifi Connection")
            report.step_start("Click Connections")
            connElement = driver.find_element_by_xpath("//*[@text='Connections']")
            connElement.click()


            # ---------------------Open WIFI page-------------------------------
            try:
                report.step_start("Clicking Wi-Fi")
                print("Clicking WIFI")
                time.sleep(3)
                wifiElement = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((MobileBy.XPATH,"//*[@text='Wi-Fi']")))
                wifiElement.click()


                # --------------------To Turn on WIFi Switch if already OFF--------------------------------
                try:
                    driver.implicitly_wait(1)
                    get_switch_text_element = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/switch_text']")
                    get_switch_text = get_switch_text_element.text
                    print("get_switch_text: ",get_switch_text)
                    print("Find wifi switch")
                    try: #To Turn on Wi-Fi Switch
                        if get_switch_text == "Off":
                            # driver.implicitly_wait(3)
                            get_switch_element = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/switch_widget']")
                            driver.implicitly_wait(1)
                            get_switch_element.click()
                            driver.implicitly_wait(1)
                            i = 0
                            for i in range(5):
                                if get_switch_text == "On":
                                    print("WIFI Switch is ON")
                                    break
                                else:
                                    try:
                                        get_switch_text_element = driver.find_element_by_xpath(
                                            "//*[@resource-id='com.android.settings:id/switch_text']")
                                        get_switch_text = get_switch_text_element.text
                                    except:
                                        pass
                                    print("Sleeping for: ", i)
                                    time.sleep(i)
                                    pass
                            if get_switch_text == "Off":
                                print("Switch is Still OFF")
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ip_address_element_text, ssid_with_internet
                        else:
                            print("Switch is already On")
                            check_if_no_internet_popup(driver)
                    except:
                        print("Couldn't turn on WIFI switch")
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ip_address_element_text, ssid_with_internet

                    #---------------------This is to Forget current connected SSID-------------------------------
                    try: #To deal with already connected SSID
                        check_if_no_internet_popup(driver)
                        network_category = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/connected_network_category']")
                        try: #To forget exhisting ssid
                            print("To forget ssid")
                            check_if_no_internet_popup(driver)
                            additional_details_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/layout_details']")
                            additional_details_element.click()
                            try:
                                check_if_no_internet_popup(driver)
                                forget_ssid = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/forget_button']//*[@resource-id='com.android.settings:id/icon']")
                                forget_ssid.click()
                                print("Forget old ssid")
                            except:
                                print("Couldn't forget ssid")
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ip_address_element_text, ssid_with_internet
                        except:
                            print("Couldn't get into additional details")
                    except:
                        print("No Connected SSIDS")
                    #----------------------This is to Forget current connected SSID--------------------------------

                    time.sleep(2)
                    print("Selecting Wifi: " + WifiName)
                   #allure.attach(name= body=str("Selecting Wifi: " + WifiName))
                    ssid_found = False
                    available_ssids = False
                    #This is To get all available ssids
                    #------------------------------------------------------
                    try:
                        for k in range(3):
                            available_ssids = get_all_available_ssids(driver, deviceModelName)
                            print("active_ssid_list: ", available_ssids)
                            allure.attach(name="Available SSIDs in device: ", body=str(available_ssids))
                            try:
                                if WifiName not in available_ssids:
                                    scrollDown(setup_perfectoMobile)
                                    time.sleep(2)
                                else:
                                    ssid_found = True
                                    print(WifiName+" : Found in Device")
                                   #allure.attach(name= body=str(WifiName+" : Found in Device"))
                                    break
                            except:
                                print("couldn't find wifi in available ssid")
                        if not ssid_found:
                            print("could not found " + WifiName + " in device")
                           #allure.attach(name= body=str("could not found" + WifiName + " in device"))
                            closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            return ip_address_element_text, ssid_with_internet
                    except:
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ip_address_element_text, ssid_with_internet
                    #-------------------------------------------------------



                    #Selecting WIFI
                    # -------------------------------------------------------
                    try:
                        report.step_start("Selecting Wifi: " + WifiName)
                        wifiSelectionElement = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='" + WifiName + "']")))
                        wifiSelectionElement.click()
                        check_if_no_internet_popup(driver)
                    except Exception as e:
                        print("Exception on Selecting Wifi Network.  Please check wifi Name or signal")
                        request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ip_address_element_text, ssid_with_internet
                    # -------------------------------------------------------


                    #Set password if Needed
                    # -------------------------------------------------------
                    try:
                        check_if_no_internet_popup(driver)
                        report.step_start("Set Wifi Password")
                        wifiPasswordElement = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/edittext']")
                        wifiPasswordElement.send_keys(WifiPass)
                    except NoSuchElementException:
                        print("Password Page Not Loaded, password May be cached in the System")
                    check_if_no_internet_popup(driver)
                    # -------------------------------------------------------

                    #Click on connect button
                    # -------------------------------------------------------
                    try:
                        report.step_start("Click Connect Button")
                        joinBTNElement = driver.find_element_by_xpath("//*[@text='Connect']")
                        joinBTNElement.click()
                    except NoSuchElementException:
                        print("Connect Button Not Enabled...Verify if Password is set properly  ")
                    check_if_no_internet_popup(driver)
                    # -------------------------------------------------------

                    #Verify if WiFi is connected
                    # -------------------------------------------------------
                    try:
                        report.step_start("Verify if Wifi is Connected")
                        WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH,
                            "//*[@resource-id='android:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                        ssid_with_internet = True
                        print("Wifi Successfully Connected")
                        # time.sleep(5)
                        check_if_no_internet_popup(driver)
                    except:
                        try:
                            check_if_no_internet_popup(driver)
                            WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH,
                                "//*[@resource-id='com.android.settings:id/summary' and @text='Connected without internet']/parent::*/android.widget.TextView[@text='"
                                                                + WifiName + "']")))
                            print("Wifi Successfully Connected without internet")
                            check_if_no_internet_popup(driver)
                        except:
                            try:
                                report.step_start("Verify if Wifi is Connected")
                                WifiInternetErrMsg = WebDriverWait(driver, 60).until(EC.presence_of_element_located((
                                    MobileBy.XPATH,
                                    "//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                                ssid_with_internet = True
                                print("Wifi Successfully Connected")
                            except NoSuchElementException:
                                print("Wifi Connection Error: " + WifiName)
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ip_address_element_text, ssid_with_internet
                    # -------------------------------------------------------

                    #Get into Additional Details
                    #To Get an IP Address
                    #To Forget connection
                    #To turn off auto. connect
                    # -------------------------------------------------------
                    try:
                        print("Into additional details")
                        time.sleep(2)
                        additional_details_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/layout_details']")
                        additional_details_element.click()
                        try:
                            time.sleep(2)
                            ip_address_element = driver.find_element_by_xpath(
                                                                "//*[@text='IP address']/parent::*/android.widget.TextView[@resource-id='com.android.settings:id/summary']")
                            ip_address_element_text = ip_address_element.text
                            print("Device IP address is :", ip_address_element_text)
                        except:
                            try:
                                time.sleep(2)
                                ip_address_element = driver.find_element_by_xpath(
                                    "//*[@text='IP address']/parent::*/android.widget.TextView[@resource-id='android:id/summary']")
                                ip_address_element_text = ip_address_element.text
                                print("Device IP address is :", ip_address_element_text)
                            except:
                                print("IP address element not found")
                               #allure.attach(name= body=str("IP address element not found"))

                            # closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            # return ip_address_element_text, ssid_with_internet

                        try:
                            check_if_no_internet_popup(driver)
                            driver.implicitly_wait(3)
                            time.sleep(2)
                            auto_reconnect_off = driver.find("//*[@resource-id='android:id/switch_widget']")
                            auto_reconnect_off_text = auto_reconnect_off.text
                            if auto_reconnect_off_text != "Off":
                                auto_reconnect_off.click()
                                print("Auto reconnect turning off")
                            else:
                                print("Auto reconnect is already off")
                        except:
                            print("Couldn't find auto reconnect element")

                        # ------------------------------- Forget SSID ----------------
                        try:
                            check_if_no_internet_popup(driver)
                            forget_ssid = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/forget_button']//*[@resource-id='com.android.settings:id/icon']")
                            forget_ssid.click()
                            print("Forgetting ssid")

                            #------------------------------- Wifi Switch ----------------
                            try:
                                print("clicking on wifi switch")
                                get_switch_element = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/switch_widget']")
                                driver.implicitly_wait(2)
                                get_switch_element.click()
                            except:
                                print("couldn't click on wifi switch")
                               #allure.attach(name= body=str("couldn't click on wifi switch"))
                        except:
                            print("Couldn't forget ssid")
                            # closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            # return ip_address_element_text, ssid_with_internet
                    except:
                        print("Couldn't get into Additional settings")
                    # -------------------------------------------------------
                except:
                    print("No Switch element found")
                # ---------------------To Turn on WIFi Switch if already OFF-------------------------------

            except:
                print("Couldn't find wifi Button")
            # ------------------Open WIFI page----------------------------------

        except:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")
        # -----------------To Open Connections page---------------------------
    #--------------------Pixel 4 code---------------------------
    else:
        report.step_start("Set Wifi Network to " + WifiName)

        # -----------------To Open Connections page-----------------------
        try:
            print("Verifying Connected Wifi Connection")
            report.step_start("Click Network & internet in pixel4")
            connElement = driver.find_element_by_xpath("//*[@text='Network & internet']")
            connElement.click()

            # ---------------------Open WIFI page-------------------------------
            try:
                report.step_start("Clicking Wi-Fi")
                print("Clicking WIFI")
                time.sleep(3)
                wifiElement = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='Wi‑Fi']")))
                wifiElement.click()

                # --------------------To Turn on WIFi Switch if already OFF--------------------------------
                try:
                    driver.implicitly_wait(1)
                    get_switch_text_element = driver.find_element_by_xpath(
                        "//*[@resource-id='android:id/icon']")
                    get_switch_text = get_switch_text_element.click()
                    if get_switch_text is not None:
                        switch_text = "Off"
                    else:
                        switch_text = "On"

                    print("get_switch_text: ", switch_text)
                    print("Find wifi switch")
                    try:  # To Turn on Wi-Fi Switch
                        if switch_text == "Off":
                            # driver.implicitly_wait(3)
                            get_switch_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/switch_widget']")
                            driver.implicitly_wait(1)
                            get_switch_element.click()
                            driver.implicitly_wait(1)
                            i = 0
                            for i in range(5):
                                if switch_text == "On":
                                    print("WIFI Switch is ON")
                                    break
                                else:
                                    try:
                                        get_switch_text_element = driver.find_element_by_xpath(
                                            "//*[@text='Add network']")
                                        get_switch_text = get_switch_text_element.text
                                        if get_switch_text == "Add network":
                                            switch_text = "On"
                                        else:
                                            switch_text = "Off"
                                    except NoSuchElementException:
                                        print("Exception: Verify Xpath")
                                    # Scroll Down
                                    scrollDown(setup_perfectoMobile)
                                    print("Sleeping for: ", i)
                                    time.sleep(i)
                                    pass
                            if switch_text == "Off":
                                print("Switch is Still OFF")
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ip_address_element_text, ssid_with_internet
                        else:
                            print("Switch is already On")
                            check_if_no_internet_popup(driver)
                    except:
                        print("Couldn't turn on WIFI switch")
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ip_address_element_text, ssid_with_internet

                    # ---------------------This is to Forget current connected SSID-------------------------------
                    try:  # To deal with already connected SSID
                        check_if_no_internet_popup(driver)
                        network_category = driver.find_element_by_xpath("//*[@text='Connected']")
                        try:  # To forget existing ssid
                            print("To forget ssid")
                            check_if_no_internet_popup(driver)
                            additional_details_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/settings_button_no_background']")
                            additional_details_element.click()
                        except:
                            print("Couldn't get into additional details")
                        try:
                            check_if_no_internet_popup(driver)
                            forget_ssid = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/button1']")
                            forget_ssid.click()
                            print("Forget old ssid")
                        except:
                            print("Couldn't forget ssid")
                            closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            return ip_address_element_text, ssid_with_internet
                    except:
                        print("No Connected SSIDS")
                    # ----------------------This is to Forget current connected SSID--------------------------------

                    time.sleep(2)
                    print("Selecting Wifi: " + WifiName)
                    # allure.attach(name= body=str("Selecting Wifi: " + WifiName))
                    ssid_found = False
                    available_ssids = False
                    # This is To get all available ssids
                    # ------------------------------------------------------
                    try:
                        for k in range(3):
                            available_ssids = get_all_available_ssids(driver, deviceModelName)
                            print("active_ssid_list: ", available_ssids)
                            allure.attach(name="Available SSIDs in device: ", body=str(available_ssids))
                            try:
                                if WifiName not in available_ssids:
                                    scrollDown(setup_perfectoMobile)
                                    time.sleep(2)
                                else:
                                    ssid_found = True
                                    print(WifiName + " : Found in Device")
                                    # allure.attach(name= body=str(WifiName+" : Found in Device"))
                                    break
                            except:
                                print("couldn't find wifi in available ssid")
                        if not ssid_found:
                            print("could not found " + WifiName + " in device")
                            # allure.attach(name= body=str("could not found" + WifiName + " in device"))
                            closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            return ip_address_element_text, ssid_with_internet
                    except:
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ip_address_element_text, ssid_with_internet
                    # -------------------------------------------------------

                    # Selecting WIFI
                    # -------------------------------------------------------
                    try:
                        report.step_start("Selecting Wifi: " + WifiName)
                        wifiSelectionElement = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='" + WifiName + "']")))
                        wifiSelectionElement.click()
                        check_if_no_internet_popup(driver)
                    except Exception as e:
                        print("Exception on Selecting Wifi Network.  Please check wifi Name or signal")
                        request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ip_address_element_text, ssid_with_internet
                    # -------------------------------------------------------

                    # Set password if Needed
                    # -------------------------------------------------------
                    try:
                        check_if_no_internet_popup(driver)
                        report.step_start("Set Wifi Password")
                        print("Entering password")
                        wifiPasswordElement = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/password']")
                        wifiPasswordElement.send_keys(WifiPass)
                    except NoSuchElementException:
                        print("Password Page Not Loaded, password May be cached in the System")
                    check_if_no_internet_popup(driver)
                    # -------------------------------------------------------

                    # Click on connect button
                    # -------------------------------------------------------
                    try:
                        report.step_start("Click Connect Button")
                        joinBTNElement = driver.find_element_by_xpath("//*[@text='Connect']")
                        joinBTNElement.click()
                    except NoSuchElementException:
                        print("Connect Button Not Enabled...Verify if Password is set properly  ")
                    check_if_no_internet_popup(driver)
                    # -------------------------------------------------------

                    # Verify if WiFi is connected
                    # -------------------------------------------------------
                    try:
                        report.step_start("Verify if Wifi is Connected")
                        WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH,
                                                            "//*[@resource-id='android:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                        ssid_with_internet = True
                        print("Wifi Successfully Connected")
                        # time.sleep(5)
                        check_if_no_internet_popup(driver)
                    except:
                        try:
                            check_if_no_internet_popup(driver)
                            WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH,
                                                                "//*[@resource-id='com.android.settings:id/summary' and @text='Connected without internet']/parent::*/android.widget.TextView[@text='"+ WifiName + "']")))
                            print("Wifi Successfully Connected without internet")
                            check_if_no_internet_popup(driver)
                        except:
                            try:
                                report.step_start("Verify if Wifi is Connected")
                                WifiInternetErrMsg = WebDriverWait(driver, 60).until(EC.presence_of_element_located((
                                    MobileBy.XPATH,
                                    "//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                                ssid_with_internet = True
                                print("Wifi Successfully Connected")
                            except NoSuchElementException:
                                print("Wifi Connection Error: " + WifiName)
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ip_address_element_text, ssid_with_internet
                    # -------------------------------------------------------

                    # Get into Additional Details
                    # To Get an IP Address
                    # To Forget connection
                    # To turn off auto. connect
                    # -------------------------------------------------------
                    try:
                        print("Into additional details")
                        time.sleep(5)
                        report.step_start("Going for ip address")
                        additional_details_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/settings_button_no_background']")
                        additional_details_element.click()
                        print("Entered ssid")
                        try:
                            time.sleep(10)
                            print("clicking Advanced")
                            report.step_start("clicking Advanced")
                            advanced_element = driver.find_element_by_xpath("//*[@text='Advanced']")
                            advanced_element.click()
                            print("clicked Advanced")
                            #print("Device IP address is :", ip_address_element_text)
                        except:
                            try:
                                time.sleep(5)
                                print("clicking Advanced2")
                                advanced_element = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/recycler_view']/android.widget.FrameLayout[2]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]")
                                advanced_element.click()
                                #print("Device IP address is :", ip_address_element_text)
                            except:
                                try:
                                    time.sleep(5)
                                    print("clicking Advanced2")
                                    advanced_element = driver.find_element_by_xpath(
                                        "//*[@resource-id='com.android.settings:id/recycler_view']/android.widget.LinearLayout[5]/android.widget.LinearLayout[1]/android.widget.ImageView[1]")
                                    advanced_element.click()
                                except:
                                    print("No advanced options")
                            # allure.attach(name= body=str("IP address element not found"))

                            # closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            # return ip_address_element_text, ssid_with_internet
                        # Scroll Down
                        scrollDown(setup_perfectoMobile)
                        try:
                            time.sleep(2)
                            ip_address_element = driver.find_element_by_xpath(
                                "//*[@text='IP address']/parent::*/android.widget.TextView[@resource-id='android:id/summary']")
                            ip_address_element_text = ip_address_element.text
                            print("Device IP address is :", ip_address_element_text)
                        except:
                            print("IP address element not found")
                        #------------------------------- Forget SSID ----------------
                        try:
                            check_if_no_internet_popup(driver)
                            forget_ssid = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/settings_button_no_background']")
                            forget_ssid.click()
                            print("Forgetting ssid")

                            # ------------------------------- Wifi Switch ----------------
                            try:
                                print("clicking on wifi switch")
                                get_switch_element = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/switch_widget']")
                                driver.implicitly_wait(2)
                                get_switch_element.click()
                            except:
                                print("couldn't click on wifi switch")
                            # allure.attach(name= body=str("couldn't click on wifi switch"))
                        except:
                            print("Couldn't forget ssid")
                            # closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            # return ip_address_element_text, ssid_with_internet
                    except:
                        print("Couldn't get into Additional settings")
                    # -------------------------------------------------------
                except:
                    print("No Switch element found")
                # ---------------------To Turn on WIFi Switch if already OFF-------------------------------

            except:
                print("Couldn't find wifi Button")
            # ------------------Open WIFI page----------------------------------

        except:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")
        # -----------------To Open Connections page---------------------------

    closeApp(connData["appPackage-android"], setup_perfectoMobile)
    return ip_address_element_text, ssid_with_internet

#only to connect to wifi
def wifi_connect(request, WifiName, WifiPass, setup_perfectoMobile, connData):
    print("\n-------------------------------------")
    print("Select Wifi/AccessPoint Connection")
    print("-------------------------------------")
    print("Verifying Wifi Connection Details....")
   #allure.attach(name= body=str("\n-------------------------------------"))
    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    ssid_with_internet = False

    report.step_start("Switching Driver Context")
    print("Switching Context to Native")
    contexts = driver.contexts
    driver.switch_to.context(contexts[0])

    # Open Settings Application
    openApp(connData["appPackage-android"], setup_perfectoMobile)
    deviceModelName = getDeviceModelName(setup_perfectoMobile)
    print("Selected Device Model: " + deviceModelName)
   #allure.attach(name= body=str("\Selected Device Model: " + deviceModelName))
    if deviceModelName != ("Pixel 4"):
        report.step_start("Set Wifi Network to " + WifiName)


        # -----------------To Open Connections page-----------------------
        try:
            print("Verifying Connected Wifi Connection")
            report.step_start("Click Connections")
            connElement = driver.find_element_by_xpath("//*[@text='Connections']")
            connElement.click()


            # ---------------------Open WIFI page-------------------------------
            try:
                report.step_start("Clicking Wi-Fi")
                print("Clicking WIFI")
                wifiElement = driver.find_element_by_xpath("//*[@text='Wi-Fi']")
                wifiElement.click()


                # --------------------To Turn on WIFi Switch if already OFF--------------------------------
                try:
                    driver.implicitly_wait(1)
                    get_switch_text_element = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/switch_text']")
                    get_switch_text = get_switch_text_element.text
                    print("get_switch_text: ",get_switch_text)
                    print("Find wifi switch")
                    try: #To Turn on Wi-Fi Switch
                        if get_switch_text == "Off":
                            # driver.implicitly_wait(3)
                            get_switch_element = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/switch_widget']")
                            driver.implicitly_wait(1)
                            get_switch_element.click()
                            driver.implicitly_wait(1)
                            i = 0
                            for i in range(5):
                                if get_switch_text == "On":
                                    print("WIFI Switch is ON")
                                    break
                                else:
                                    try:
                                        get_switch_text_element = driver.find_element_by_xpath(
                                            "//*[@resource-id='com.android.settings:id/switch_text']")
                                        get_switch_text = get_switch_text_element.text
                                    except:
                                        pass
                                    print("Sleeping for: ", i)
                                    time.sleep(i)
                                    pass
                            if get_switch_text == "Off":
                                print("Switch is Still OFF")
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ssid_with_internet
                        else:
                            print("Switch is already On")
                            check_if_no_internet_popup(driver)
                    except:
                        print("Couldn't turn on WIFI switch")
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ssid_with_internet

                    #---------------------This is to Forget current connected SSID-------------------------------
                    try: #To deal with already connected SSID
                        check_if_no_internet_popup(driver)
                        network_category = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/connected_network_category']")
                        try: #To forget exhisting ssid
                            print("To forget ssid")
                            check_if_no_internet_popup(driver)
                            additional_details_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/layout_details']")
                            additional_details_element.click()
                            try:
                                check_if_no_internet_popup(driver)
                                forget_ssid = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/forget_button']//*[@resource-id='com.android.settings:id/icon']")
                                forget_ssid.click()
                                print("Forget old ssid")
                            except:
                                print("Couldn't forget ssid")
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ssid_with_internet
                        except:
                            print("Couldn't get into additional details")
                    except:
                        print("No Connected SSIDS")
                    #----------------------This is to Forget current connected SSID--------------------------------


                    print("Searching for Wifi: " + WifiName)
                   #allure.attach(name= body=str("Searching for Wifi: " + WifiName))
                    time.sleep(2)
                    print("Selecting Wifi: " + WifiName)
                    ssid_found = False
                    available_ssids = False
                    # This is To get all available ssids
                    # ------------------------------------------------------
                    try:
                        for check_for_all_ssids in range(2):
                            available_ssids = get_all_available_ssids(driver, deviceModelName)
                            try:
                                if WifiName not in available_ssids:
                                    scrollDown(setup_perfectoMobile)
                                    time.sleep(2)
                                else:
                                    ssid_found = True
                                    print(WifiName + " : Found in Device")
                                   #allure.attach(name= body=str(WifiName + " : Found in Device"))
                                    break
                            except:
                                print("1538")
                                pass
                        if not ssid_found:
                            print("could not found" + WifiName + " in device")
                           #allure.attach(name= body=str("could not found" + WifiName + " in device"))
                            closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            return ssid_with_internet
                    except:
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ssid_with_internet
                    # -------------------------------------------------------



                    #Selecting WIFI
                    # -------------------------------------------------------
                    try:
                        report.step_start("Selecting Wifi: " + WifiName)
                        wifiSelectionElement = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='" + WifiName + "']")))
                        wifiSelectionElement.click()
                        check_if_no_internet_popup(driver)
                       #allure.attach(name= body=str("Selecting Wifi: " + WifiName))
                    except Exception as e:
                        print("Exception on Selecting Wifi Network.  Please check wifi Name or signal")
                       #allure.attach(name= body=str("Exception on Selecting Wifi Network.  Please check wifi Name or signal"))
                        request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ssid_with_internet
                    # -------------------------------------------------------


                    #Set password if Needed
                    # -------------------------------------------------------
                    try:
                        check_if_no_internet_popup(driver)
                        report.step_start("Set Wifi Password")
                        wifiPasswordElement = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/edittext']")
                        wifiPasswordElement.send_keys(WifiPass)
                    except NoSuchElementException:
                        print("Password Page Not Loaded, password May be cached in the System")
                    check_if_no_internet_popup(driver)
                    # -------------------------------------------------------

                    #Click on connect button
                    # -------------------------------------------------------
                    try:
                        report.step_start("Click Connect Button")
                        joinBTNElement = driver.find_element_by_xpath("//*[@text='Connect']")
                        joinBTNElement.click()
                    except NoSuchElementException:
                        print("Connect Button Not Enabled...Verify if Password is set properly  ")
                    check_if_no_internet_popup(driver)
                    # -------------------------------------------------------

                    #Verify if WiFi is connected
                    # -------------------------------------------------------
                    try:
                        report.step_start("Verify if Wifi is Connected")
                        WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH,
                            "//*[@resource-id='android:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                        ssid_with_internet = True
                        print("Wifi Successfully Connected")
                       #allure.attach(name= body=str("Wifi Successfully Connected"))
                        # time.sleep(5)
                        check_if_no_internet_popup(driver)
                    except:
                        try:
                            check_if_no_internet_popup(driver)
                            WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH,
                                "//*[@resource-id='com.android.settings:id/summary' and @text='Connected without internet']/parent::*/android.widget.TextView[@text='"
                                                                + WifiName + "']")))
                            print("Wifi Successfully Connected without internet")
                           #allure.attach(name= body=str("Wifi Successfully Connected without internet"))
                            check_if_no_internet_popup(driver)
                        except:
                            try:
                                report.step_start("Verify if Wifi is Connected")
                                WifiInternetErrMsg = WebDriverWait(driver, 60).until(EC.presence_of_element_located((
                                    MobileBy.XPATH,
                                    "//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                                ssid_with_internet = True
                                print("Wifi Successfully Connected")
                               #allure.attach(name=body=str("Wifi Successfully Connected"))
                            except NoSuchElementException:
                                print("Wifi Connection Error: " + WifiName)
                               #allure.attach(name=body=str("Wifi Connection Error: " + WifiName))
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ssid_with_internet


                except NoSuchElementException:
                    print("No Switch element found")
                   #allure.attach(name= body=str("No Switch element found"))
                # ---------------------To Turn on WIFi Switch if already OFF-------------------------------

            except NoSuchElementException:
                print("Couldn't find wifi Button")
                #allure.attach(name= body=str("Couldn't find wifi Button"))
            # ------------------Open WIFI page----------------------------------

        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")
           #allure.attach(name= body=str("Exception: Verify Xpath - Update/check Xpath for Click Connections"))
        # -----------------To Open Connections page---------------------------
    else: #--------------Pixel 4 code--------------------------
        report.step_start("Set Wifi Network to " + WifiName)

        # -----------------To Open Connections page-----------------------
        try:
            print("Verifying Connected Wifi Connection")
            report.step_start("Click Network & internet in pixel4")
            connElement = driver.find_element_by_xpath("//*[@text='Network & internet']")
            connElement.click()

            # ---------------------Open WIFI page-------------------------------
            try:
                report.step_start("Clicking Wi-Fi")
                print("Clicking WIFI")
                time.sleep(3)
                wifiElement = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='Wi‑Fi']")))
                wifiElement.click()

                # --------------------To Turn on WIFi Switch if already OFF--------------------------------
                try:
                    driver.implicitly_wait(1)
                    get_switch_text_element = driver.find_element_by_xpath(
                        "//*[@resource-id='android:id/icon']")
                    get_switch_text = get_switch_text_element.click()
                    if get_switch_text is not None:
                        switch_text = "Off"
                    else:
                        switch_text = "On"

                    print("get_switch_text: ", switch_text)
                    print("Find wifi switch")
                    try:  # To Turn on Wi-Fi Switch
                        if switch_text == "Off":
                            # driver.implicitly_wait(3)
                            get_switch_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/switch_widget']")
                            driver.implicitly_wait(1)
                            get_switch_element.click()
                            driver.implicitly_wait(1)
                            i = 0
                            for i in range(5):
                                if switch_text == "On":
                                    print("WIFI Switch is ON")
                                    break
                                else:
                                    try:
                                        get_switch_text_element = driver.find_element_by_xpath(
                                            "//*[@text='Add network']")
                                        get_switch_text = get_switch_text_element.text
                                        if get_switch_text == "Add network":
                                            switch_text = "On"
                                        else:
                                            switch_text = "Off"
                                    except NoSuchElementException:
                                        print("Exception: Verify Xpath")
                                    # Scroll Down
                                    scrollDown(setup_perfectoMobile)
                                    print("Sleeping for: ", i)
                                    time.sleep(i)
                                    pass
                            if switch_text == "Off":
                                print("Switch is Still OFF")
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ssid_with_internet
                        else:
                            print("Switch is already On")
                            check_if_no_internet_popup(driver)
                    except:
                        print("Couldn't turn on WIFI switch")
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ssid_with_internet

                    # ---------------------This is to Forget current connected SSID-------------------------------
                    try:  # To deal with already connected SSID
                        check_if_no_internet_popup(driver)
                        network_category = driver.find_element_by_xpath("//*[@text='Connected']")
                        try:  # To forget existing ssid
                            print("To forget ssid")
                            check_if_no_internet_popup(driver)
                            additional_details_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/settings_button_no_background']")
                            additional_details_element.click()
                        except:
                            print("Couldn't get into additional details")
                        try:
                            check_if_no_internet_popup(driver)
                            forget_ssid = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/button1']")
                            forget_ssid.click()
                            print("Forget old ssid")
                        except:
                            print("Couldn't forget ssid")
                            closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            return ssid_with_internet
                    except:
                        print("No Connected SSIDS")
                    # ----------------------This is to Forget current connected SSID--------------------------------

                    time.sleep(2)
                    print("Selecting Wifi: " + WifiName)
                    # allure.attach(name= body=str("Selecting Wifi: " + WifiName))
                    ssid_found = False
                    available_ssids = False
                    # This is To get all available ssids
                    # ------------------------------------------------------
                    try:
                        for k in range(3):
                            available_ssids = get_all_available_ssids(driver, deviceModelName)
                            print("active_ssid_list: ", available_ssids)
                            #allure.attach(name="Available SSIDs in device: ", body=str(available_ssids))
                            try:
                                if WifiName not in available_ssids:
                                    scrollDown(setup_perfectoMobile)
                                    time.sleep(2)
                                else:
                                    ssid_found = True
                                    print(WifiName + " : Found in Device")
                                    # allure.attach(name= body=str(WifiName+" : Found in Device"))
                                    break
                            except:
                                print("couldn't find wifi in available ssid")
                        if not ssid_found:
                            print("could not found " + WifiName + " in device")
                            # allure.attach(name= body=str("could not found" + WifiName + " in device"))
                            closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            return ssid_with_internet
                    except:
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ssid_with_internet
                    # -------------------------------------------------------

                    # Selecting WIFI
                    # -------------------------------------------------------
                    try:
                        report.step_start("Selecting Wifi: " + WifiName)
                        wifiSelectionElement = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='" + WifiName + "']")))
                        wifiSelectionElement.click()
                        check_if_no_internet_popup(driver)
                    except Exception as e:
                        print("Exception on Selecting Wifi Network.  Please check wifi Name or signal")
                        request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ssid_with_internet
                    # -------------------------------------------------------

                    # Set password if Needed
                    # -------------------------------------------------------
                    try:
                        check_if_no_internet_popup(driver)
                        report.step_start("Set Wifi Password")
                        wifiPasswordElement = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/password']")
                        wifiPasswordElement.send_keys(WifiPass)
                    except NoSuchElementException:
                        print("Password Page Not Loaded, password May be cached in the System")
                    check_if_no_internet_popup(driver)
                    # -------------------------------------------------------

                    # Click on connect button
                    # -------------------------------------------------------
                    try:
                        report.step_start("Click Connect Button")
                        joinBTNElement = driver.find_element_by_xpath("//*[@text='Connect']")
                        joinBTNElement.click()
                    except NoSuchElementException:
                        print("Connect Button Not Enabled...Verify if Password is set properly  ")
                    check_if_no_internet_popup(driver)
                    # -------------------------------------------------------

                    # Verify if WiFi is connected
                    # -------------------------------------------------------
                    try:
                        report.step_start("Verify if Wifi is Connected")
                        WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH,
                                                            "//*[@resource-id='android:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                        ssid_with_internet = True
                        print("Wifi Successfully Connected")
                        # time.sleep(5)
                        check_if_no_internet_popup(driver)
                    except:
                        try:
                            check_if_no_internet_popup(driver)
                            WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH,
                                                                "//*[@resource-id='com.android.settings:id/summary' and @text='Connected without internet']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                            print("Wifi Successfully Connected without internet")
                            check_if_no_internet_popup(driver)
                        except:
                            try:
                                report.step_start("Verify if Wifi is Connected")
                                WifiInternetErrMsg = WebDriverWait(driver, 60).until(EC.presence_of_element_located((
                                    MobileBy.XPATH,
                                    "//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                                ssid_with_internet = True
                                print("Wifi Successfully Connected")
                            except NoSuchElementException:
                                print("Wifi Connection Error: " + WifiName)
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ssid_with_internet


                except NoSuchElementException:
                    print("No Switch element found")
                # allure.attach(name= body=str("No Switch element found"))
                # ---------------------To Turn on WIFi Switch if already OFF-------------------------------

            except NoSuchElementException:
                print("Couldn't find wifi Button")
                # allure.attach(name= body=str("Couldn't find wifi Button"))
            # ------------------Open WIFI page----------------------------------

        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")
        # allure.attach(name= body=str("Exception: Verify Xpath - Update/check Xpath for Click Connections"))
        # -----------------To Open Connections page---------------------------

    closeApp(connData["appPackage-android"], setup_perfectoMobile)
    return ssid_with_internet

#To disconnect and forget network
def wifi_disconnect_and_forget(request, WifiName, WifiPass, setup_perfectoMobile, connData):
    print("\n-------------------------------------")
    print("WIFI Disconnect")
    print("-------------------------------------")
   #allure.attach(name= body=str("------------------- WIFI Disconnect ------------------"))

    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    report.step_start("Switching Driver Context")
    print("Switching Context to Native")
    contexts = driver.contexts
    driver.switch_to.context(contexts[0])

    # Open Settings Application
    openApp(connData["appPackage-android"], setup_perfectoMobile)
    deviceModelName = getDeviceModelName(setup_perfectoMobile)
    print("Selected Device Model: " + deviceModelName)

    if deviceModelName != ("Pixel 4"):
        report.step_start("Set Wifi Network to " + WifiName)


        # -----------------To Open Connections page-----------------------
        try:
            print("Verifying Connected Wifi Connection")
            report.step_start("Click Connections")
            connElement = driver.find_element_by_xpath("//*[@text='Connections']")
            connElement.click()


            # ---------------------Open WIFI page-------------------------------
            try:
                report.step_start("Clicking Wi-Fi")
                print("Clicking WIFI")
                wifiElement = driver.find_element_by_xpath("//*[@text='Wi-Fi']")
                wifiElement.click()


                # --------------------To Turn on WIFi Switch if already OFF--------------------------------
                try:
                    driver.implicitly_wait(1)
                    get_switch_text_element = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/switch_text']")
                    get_switch_text = get_switch_text_element.text
                    print("get_switch_text: ",get_switch_text)
                    print("Find wifi switch")
                    try: #To Turn on Wi-Fi Switch
                        if get_switch_text == "Off":
                            # driver.implicitly_wait(3)
                            get_switch_element = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/switch_widget']")
                            driver.implicitly_wait(1)
                            get_switch_element.click()
                            driver.implicitly_wait(1)
                            i = 0
                            for i in range(5):
                                if get_switch_text == "On":
                                    print("WIFI Switch is ON")
                                    break
                                else:
                                    try:
                                        get_switch_text_element = driver.find_element_by_xpath(
                                            "//*[@resource-id='com.android.settings:id/switch_text']")
                                        get_switch_text = get_switch_text_element.text
                                    except:
                                        pass
                                    print("Sleeping for: ", i)
                                    time.sleep(i)
                                    pass
                            if get_switch_text == "Off":
                                print("Switch is Still OFF")
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        else:
                            print("Switch is already On")
                            check_if_no_internet_popup(driver)
                    except:
                        print("Couldn't turn on WIFI switch")
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)

                    #---------------------This is to Forget current connected SSID-------------------------------
                    try: #To deal with already connected SSID
                        check_if_no_internet_popup(driver)
                        network_category = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/connected_network_category']")
                        try: #To forget exhisting ssid
                            print("To forget ssid")
                            check_if_no_internet_popup(driver)
                            additional_details_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/layout_details']")
                            additional_details_element.click()
                            try:
                                check_if_no_internet_popup(driver)
                                forget_ssid = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/forget_button']//*[@resource-id='com.android.settings:id/icon']")
                                forget_ssid.click()
                                print("Forget old ssid")
                               #allure.attach(name=body=str("Forget old ssid"))
                            except:
                                print("Couldn't forget ssid")
                               #allure.attach(name=body=str("Couldn't forget ssid"))
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        except:
                           #allure.attach(name=body=str("Couldn't get into additional details"))
                            print("Couldn't get into additional details")
                    except:
                       #allure.attach(name=body=str("No Connected SSIDS"))
                        print("No Connected SSIDS")
                    #----------------------This is to Forget current connected SSID--------------------------------

                    try:
                        print("clicking on wifi switch")
                        get_switch_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/switch_widget']")
                        driver.implicitly_wait(2)
                        get_switch_element.click()
                    except:
                        print("couldn't click on wifi switch")


                except NoSuchElementException:
                    print("No Switch element found")
                # ---------------------To Turn on WIFi Switch if already OFF-------------------------------

            except NoSuchElementException:
                print("Couldn't find wifi Button")
            # ------------------Open WIFI page----------------------------------

        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")
        # -----------------To Open Connections page---------------------------
    else:#-----------------------Pixel4 code-------------------------
        report.step_start("Set Wifi Network to " + WifiName)

        # -----------------To Open Connections page-----------------------
        try:
            print("Verifying Connected Wifi Connection")
            report.step_start("Click Network & internet")
            connElement = driver.find_element_by_xpath("//*[@text='Network & internet']")
            connElement.click()

            # ---------------------Open WIFI page-------------------------------
            try:
                report.step_start("Clicking Wi-Fi")
                print("Clicking WIFI")
                time.sleep(3)
                wifiElement = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='Wi‑Fi']")))
                wifiElement.click()

                # --------------------To Turn on WIFi Switch if already OFF--------------------------------
                try:
                    driver.implicitly_wait(1)
                    get_switch_text_element = driver.find_element_by_xpath(
                        "//*[@resource-id='android:id/icon']")
                    get_switch_text = get_switch_text_element.click()
                    if get_switch_text is not None:
                        switch_text = "Off"
                    else:
                        switch_text = "On"

                    print("get_switch_text: ", switch_text)
                    print("Find wifi switch")
                    try:  # To Turn on Wi-Fi Switch
                        if switch_text == "Off":
                            # driver.implicitly_wait(3)
                            get_switch_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/switch_widget']")
                            driver.implicitly_wait(1)
                            get_switch_element.click()
                            driver.implicitly_wait(1)
                            i = 0
                            for i in range(5):
                                if switch_text == "On":
                                    print("WIFI Switch is ON")
                                    break
                                else:
                                    try:
                                        get_switch_text_element = driver.find_element_by_xpath(
                                            "//*[@text='Add network']")
                                        get_switch_text = get_switch_text_element.text
                                        if get_switch_text == "Add network":
                                            switch_text = "On"
                                        else:
                                            switch_text = "Off"
                                    except NoSuchElementException:
                                        print("Exception: Verify Xpath")
                                    # Scroll Down
                                    scrollDown(setup_perfectoMobile)
                                    print("Sleeping for: ", i)
                                    time.sleep(i)
                                    pass
                            if switch_text == "Off":
                                print("Switch is Still OFF")
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        else:
                            print("Switch is already On")
                            check_if_no_internet_popup(driver)
                    except:
                        print("Couldn't turn on WIFI switch")
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        # ---------------------This is to Forget current connected SSID-------------------------------
                        try:  # To deal with already connected SSID
                            check_if_no_internet_popup(driver)
                            network_category = driver.find_element_by_xpath("//*[@text='Connected']")
                            try:  # To forget existing ssid
                                print("To forget ssid")
                                check_if_no_internet_popup(driver)
                                additional_details_element = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/settings_button_no_background']")
                                additional_details_element.click()
                                try:
                                    check_if_no_internet_popup(driver)
                                    forget_ssid = driver.find_element_by_xpath(
                                        "//*[@resource-id='com.android.settings:id/button1']")
                                    forget_ssid.click()
                                    print("Forget old ssid")
                                except:
                                    print("Couldn't forget ssid")
                                    closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            except:
                                #allure.attach(name=body=str("Couldn't get into additional details"))
                                print("Couldn't get into additional details")
                        except:
                            #allure.attach(name=body=str("No Connected SSIDS"))
                            print("No Connected SSIDS")
                    #----------------------This is to Forget current connected SSID--------------------------------

                    try:
                        print("clicking on wifi switch")
                        get_switch_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/switch_widget']")
                        driver.implicitly_wait(2)
                        get_switch_element.click()
                    except:
                        print("couldn't click on wifi switch")


                except NoSuchElementException:
                    print("No Switch element found")
                # ---------------------To Turn on WIFi Switch if already OFF-------------------------------

            except NoSuchElementException:
                print("Couldn't find wifi Button")
            # ------------------Open WIFI page----------------------------------

        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")

    closeApp(connData["appPackage-android"], setup_perfectoMobile)



#  try:
#         elements = driver.find_elements_by_xpath("//*[@resource-id='com.android.settings:id/title']")
#         print("elements: ", elements)
#         print(len(elements))
#         for i in range(len(elements)):
#             print("elements[i]", elements[i])
#             print("elements[i].text", elements[i].text)
#     except:
#         print("No SSIDS available")
def get_all_available_ssids(driver, deviceModelName):
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
                active_ssid_list.append(elements[i].text)
        except:
            print("No SSIDS available")

    #allure.attach(name= body=str("SSIDs visible in device: " + available_ssid))
    return active_ssid_list

def reportClient(value):
    global reporting_client  # declare a to be a global
    reporting_client = value  # this sets the global value of a

# This is a functon to get all of the ssid details
# This function needs to be called from a standalone script and not throuh testcase
# def get_all_available_ssids():
#     from appium import webdriver
#     driver = None
#     reporting_client = None
#
#     warnings.simplefilter("ignore", ResourceWarning)
#     urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#
#     capabilities = {
#         'platformName': 'Android',
#         'model': 'Galaxy S9',
#         'browserName': 'mobileOS',
#         # 'automationName' : 'Appium',
#         'securityToken': 'eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJpYXQiOjE2MjE4NjgyOTksImp0aSI6IjIzNGFiOTM1LWIxYjQtNGZiOC1hZmJiLTM0OTQwNzU5MjIwMyIsImlzcyI6Imh0dHBzOi8vYXV0aDIucGVyZmVjdG9tb2JpbGUuY29tL2F1dGgvcmVhbG1zL3RpcC1wZXJmZWN0b21vYmlsZS1jb20iLCJhdWQiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwic3ViIjoiN2I1MzBhZTAtODgxOC00N2I5LTgzZjMtN2ZhMGZiMGRkYjRlIiwidHlwIjoiT2ZmbGluZSIsImF6cCI6Im9mZmxpbmUtdG9rZW4tZ2VuZXJhdG9yIiwibm9uY2UiOiI1MzI2NDQxNS0xYTQwLTQ1ZTctOGVkMi1hOTNiYWZmZWNjYjIiLCJzZXNzaW9uX3N0YXRlIjoiY2YzY2JlOGMtY2Y5OC00NzRlLWJmODctYTIxNzU0NzVhM2EzIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.4a4v6AKxmY95Zb-l84K_Od49WPikwOHP7ryctfmnn-w',
#         'useAppiumForWeb': 'false',
#         'useAppiumForHybrid': 'false',
#         # 'bundleId' : request.config.getini("appPackage-android"),
#     }
#
#     app_data = {
#         "webURL": "https://www.google.com",
#         "lblSearch": "//*[@class='gLFyf']",
#         "elelSearch": "(//*[@class='sbic sb43'])[1]",
#         "BtnRunSpeedTest": "//*[text()='RUN SPEED TEST']",
#         "bundleId-iOS-Settings": 'com.apple.Preferences',
#         "bundleId-iOS-Safari": 'com.apple.mobilesafari',
#         "downloadMbps": "//*[@id='knowledge-verticals-internetspeedtest__download']/P[@class='spiqle']",
#         "UploadMbps": "//*[@id='knowledge-verticals-internetspeedtest__upload']/P[@class='spiqle']",
#         # Android
#         "platformName-android": 'Android',
#         "appPackage-android": 'com.android.settings'
#     }
#
#     driver = webdriver.Remote(
#         "https://tip.perfectomobile.com/nexperience/perfectomobile/wd/hub",
#         capabilities
#     )
#
#     try:
#         print(driver)
#         driver.implicitly_wait(35)
#         #Driver Ends here
#
#         projectname = "TIP-PyTest-Execution"
#         projectversion = 1.0
#         jobname = "tip-sushant-android"
#         jobnumber = 2
#         tags = "TestTag"
#         testCaseName = "getting_ssids"
#
#         # print("\nSetting Perfecto ReportClient....")
#         perfecto_execution_context = PerfectoExecutionContext(driver, tags, Job(jobname, jobnumber),
#                                                               Project(projectname, projectversion))
#         reporting_client = PerfectoReportiumClient(perfecto_execution_context)
#         reporting_client.test_start(testCaseName, TestContext([], "Perforce"))
#         reportClient(reporting_client)
#
#
#         setup_perfectoMobile = (driver, reporting_client)
#         print("setup_perfectoMobile_android: ", setup_perfectoMobile)
#         print(type(setup_perfectoMobile))
#
#         print("\n-------------------------------------")
#         print("Select Wifi/AccessPoint Connection")
#         print("-------------------------------------")
#         print("Verifying Wifi Connection Details....")
#         report = setup_perfectoMobile[1]
#         driver = setup_perfectoMobile[0]
#
#
#
#         ip_address_element_text = False
#         ssid_with_internet = False
#         ssid_list = []
#
#         report.step_start("Switching Driver Context")
#         print("Switching Context to Native")
#         contexts = driver.contexts
#         print("contexts", contexts)
#         driver.switch_to.context(contexts[0])
#         print("1508")
#
#         # Open Settings Application
#         openApp(app_data["appPackage-android"], setup_perfectoMobile)
#
#         deviceModelName = driver.execute_script('mobile:handset:info', {'property': 'model'})
#
#         # deviceModelName = getDeviceModelName(setup_perfectoMobile)
#         print("Selected Device Model: " + deviceModelName)
#
#         if deviceModelName != ("Pixel 4"):
#             # -----------------To Open Connections page-----------------------
#             try:
#                 print("Verifying Connected Wifi Connection")
#                 report.step_start("Click Connections")
#                 connElement = driver.find_element_by_xpath("//*[@text='Connections']")
#                 connElement.click()
#
#                 # ---------------------Open WIFI page-------------------------------
#                 try:
#                     report.step_start("Clicking Wi-Fi")
#                     print("Clicking WIFI")
#                     wifiElement = driver.find_element_by_xpath("//*[@text='Wi-Fi']")
#                     wifiElement.click()
#
#                     # --------------------To Turn on WIFi Switch if already OFF--------------------------------
#                     try:
#                         driver.implicitly_wait(1)
#                         get_switch_text_element = driver.find_element_by_xpath(
#                             "//*[@resource-id='com.android.settings:id/switch_text']")
#                         get_switch_text = get_switch_text_element.text
#                         print("get_switch_text: ", get_switch_text)
#                         # print("Find wifi switch")
#                         try:  # To Turn on Wi-Fi Switch
#                             if get_switch_text == "Off":
#                                 # driver.implicitly_wait(3)
#                                 get_switch_element = driver.find_element_by_xpath(
#                                     "//*[@resource-id='com.android.settings:id/switch_widget']")
#                                 # driver.implicitly_wait(1)
#                                 get_switch_element.click()
#                                 driver.implicitly_wait(1)
#                                 i = 0
#                                 for i in range(5):
#                                     if get_switch_text == "On":
#                                         print("WIFI Switch is ON")
#                                         break
#                                     else:
#                                         try:
#                                             get_switch_text_element = driver.find_element_by_xpath(
#                                                 "//*[@resource-id='com.android.settings:id/switch_text']")
#                                             get_switch_text = get_switch_text_element.text
#                                         except:
#                                             pass
#                                         print("Sleeping for: ", i)
#                                         time.sleep(i)
#                                         pass
#                                 if get_switch_text == "Off":
#                                     print("Switch is Still OFF")
#                                     closeApp(app_data["appPackage-android"], setup_perfectoMobile)
#                                     close_driver(driver)
#                                     return ip_address_element_text
#                             else:
#                                 print("Switch is already On")
#                                 check_if_no_internet_popup(driver)
#                         except:
#                             print("Couldn't turn on WIFI sewitch")
#                             closeApp(app_data["appPackage-android"], setup_perfectoMobile)
#                             close_driver(driver)
#                             return ip_address_element_text
#
#                         # ---------------------This is to Forget current connected SSID-------------------------------
#                         try:  # To deal with already connected SSID
#                             check_if_no_internet_popup(driver)
#                             network_category = driver.find_element_by_xpath(
#                                 "//*[@resource-id='com.android.settings:id/connected_network_category']")
#                             try:  # To forget exhisting ssid
#                                 print("To forget exhisting ssid")
#                                 check_if_no_internet_popup(driver)
#                                 additional_details_element = driver.find_element_by_xpath(
#                                     "//*[@resource-id='com.android.settings:id/layout_details']")
#                                 additional_details_element.click()
#                                 try:
#                                     check_if_no_internet_popup(driver)
#                                     forget_ssid = driver.find_element_by_xpath(
#                                         "//*[@resource-id='com.android.settings:id/forget_button']//*[@resource-id='com.android.settings:id/icon']")
#                                     forget_ssid.click()
#                                     print("Forget old ssid")
#                                 except:
#                                     print("Couldn't forget ssid")
#                                     closeApp(app_data["appPackage-android"], setup_perfectoMobile)
#                                     close_driver(driver)
#                                     return ip_address_element_text
#                             except:
#                                 print("Couldn't get into additional details")
#                         except:
#                             print("No Connected SSIDS")
#                         # ----------------------This is to Forget current connected SSID--------------------------------
#                         scroll_if_not_end_of_page = True
#
#                         try:
#                             for i in range(10):
#                                 try:
#                                     driver.implicitly_wait(5)
#                                     window_size = driver.get_window_size()
#                                     # print(window_size)
#                                     # print(type(window_size))
#                                     window_width = window_size['width']
#                                     # print(window_width)
#                                     window_height = window_size['height']
#                                     # print(window_height)
#                                     try:
#                                         try:
#                                             elements = driver.find_elements_by_xpath(
#                                                 "//*[@resource-id='com.android.settings:id/title']")
#                                             print("elements: ", elements)
#                                             print(len(elements))
#                                             curent_ssid_list = []
#                                             for j in range(len(elements)):
#                                                 # print("elements[i].text", elements[j].text)
#                                                 # print(j)
#                                                 if i != 0:
#                                                     curent_ssid_list.append(elements[j].text)
#                                                     # print("curent_ssid_list: ", curent_ssid_list)
#                                                 ssid_list.append(elements[j].text)
#                                             print("ssid_list",ssid_list)
#                                             print("curent_ssid_list: ", curent_ssid_list)
#                                         except:
#                                             print("No SSIDS available")
#
#                                         try:
#                                             print("in check")
#                                             check = all(item in curent_ssid_list for item in ssid_list)
#                                             print("check: ", check)
#                                             if check:
#                                                 scroll_if_not_end_of_page = False
#                                                 break
#                                             else:
#                                                 new_window_height = window_height + 100
#                                                 # driver.scroll(0, new_window_height)
#                                                 driver.execute_script("mobile: scroll", {"direction": "down"})
#                                                 continue
#                                         except:
#                                             print("Error in page end")
#                                     except:
#                                         pass
#                                 except:
#                                     pass
#                         except:
#                             pass
#                     except NoSuchElementException:
#                         print("No Switch element found")
#                     # ---------------------To Turn on WIFi Switch if already OFF-------------------------------
#
#                 except NoSuchElementException:
#                     print("Couldn't find wifi Button")
#                 # ------------------Open WIFI page----------------------------------
#
#             except NoSuchElementException:
#                 print("Exception: Verify Xpath - Update/check Xpath for Click Connections")
#             # -----------------To Open Connections page---------------------------
#
#     except:
#         try:
#             closeApp(app_data["appPackage-android"], setup_perfectoMobile)
#         except:
#             pass
#         try:
#             reporting_client.test_stop(TestResultFactory.create_success())
#             print('Report-Url: ' + reporting_client.report_url() + '\n')
#         except:
#             pass
#         try:
#             close_driver(driver)
#         except:
#             pass
#     finally:
#         try:
#             reporting_client.test_stop(TestResultFactory.create_success())
#             print('Report-Url: ' + reporting_client.report_url() + '\n')
#         except:
#             pass
#         try:
#             close_driver(driver)
#         except:
#             pass
#         return ssid_list
   #------------Enterprise Mode code----------------------------
def get_ip_address_eap_and(request, WifiName, User, ttls_passwd, setup_perfectoMobile, connData):
    print("\n-------------------------------------")
    print("Select Wifi/AccessPoint Connection")
    print("-------------------------------------")
    print("Verifying Wifi Connection Details....")
    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    ip_address_element_text = False
    ssid_with_internet = False

    report.step_start("Switching Driver Context")
    print("Switching Context to Native")
    contexts = driver.contexts
    driver.switch_to.context(contexts[0])

    # Open Settings Application
    openApp(connData["appPackage-android"], setup_perfectoMobile)
    deviceModelName = getDeviceModelName(setup_perfectoMobile)
    print("Selected Device Model: " + deviceModelName)

    if deviceModelName != ("Pixel 4"):
        report.step_start("Set Wifi Network to " + WifiName)


        # -----------------To Open Connections page-----------------------
        try:
            print("Verifying Connected Wifi Connection")
            report.step_start("Click Connections")
            connElement = driver.find_element_by_xpath("//*[@text='Connections']")
            connElement.click()


            # ---------------------Open WIFI page-------------------------------
            try:
                report.step_start("Clicking Wi-Fi")
                print("Clicking WIFI")
                time.sleep(3)
                wifiElement = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((MobileBy.XPATH,"//*[@text='Wi-Fi']")))
                wifiElement.click()


                # --------------------To Turn on WIFi Switch if already OFF--------------------------------
                try:
                    driver.implicitly_wait(1)
                    get_switch_text_element = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/switch_text']")
                    get_switch_text = get_switch_text_element.text
                    print("get_switch_text: ",get_switch_text)
                    print("Find wifi switch")
                    try: #To Turn on Wi-Fi Switch
                        if get_switch_text == "Off":
                            # driver.implicitly_wait(3)
                            get_switch_element = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/switch_widget']")
                            driver.implicitly_wait(1)
                            get_switch_element.click()
                            driver.implicitly_wait(1)
                            i = 0
                            for i in range(5):
                                if get_switch_text == "On":
                                    print("WIFI Switch is ON")
                                    break
                                else:
                                    try:
                                        get_switch_text_element = driver.find_element_by_xpath(
                                            "//*[@resource-id='com.android.settings:id/switch_text']")
                                        get_switch_text = get_switch_text_element.text
                                    except:
                                        pass
                                    print("Sleeping for: ", i)
                                    time.sleep(i)
                                    pass
                            if get_switch_text == "Off":
                                print("Switch is Still OFF")
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ip_address_element_text, ssid_with_internet
                        else:
                            print("Switch is already On")
                            check_if_no_internet_popup(driver)
                    except:
                        print("Couldn't turn on WIFI switch")
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ip_address_element_text, ssid_with_internet

                    #---------------------This is to Forget current connected SSID-------------------------------
                    try: #To deal with already connected SSID
                        check_if_no_internet_popup(driver)
                        network_category = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/connected_network_category']")
                        try: #To forget exhisting ssid
                            print("To forget ssid")
                            check_if_no_internet_popup(driver)
                            additional_details_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/layout_details']")
                            additional_details_element.click()
                            try:
                                check_if_no_internet_popup(driver)
                                forget_ssid = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/forget_button']//*[@resource-id='com.android.settings:id/icon']")
                                forget_ssid.click()
                                print("Forget old ssid")
                            except:
                                print("Couldn't forget ssid")
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ip_address_element_text, ssid_with_internet
                        except:
                            print("Couldn't get into additional details")
                    except:
                        print("No Connected SSIDS")
                    #----------------------This is to Forget current connected SSID--------------------------------

                    time.sleep(2)
                    print("Selecting Wifi: " + WifiName)
                   #allure.attach(name= body=str("Selecting Wifi: " + WifiName))
                    ssid_found = False
                    available_ssids = False
                    #This is To get all available ssids
                    #------------------------------------------------------
                    try:
                        for k in range(3):
                            available_ssids = get_all_available_ssids(driver, deviceModelName)
                            print("active_ssid_list: ", available_ssids)
                            allure.attach(name="Available SSIDs in device: ", body=str(available_ssids))
                            try:
                                if WifiName not in available_ssids:
                                    scrollDown(setup_perfectoMobile)
                                    time.sleep(2)
                                else:
                                    ssid_found = True
                                    print(WifiName+" : Found in Device")
                                   #allure.attach(name= body=str(WifiName+" : Found in Device"))
                                    break
                            except:
                                print("couldn't find wifi in available ssid")
                        if not ssid_found:
                            print("could not found " + WifiName + " in device")
                           #allure.attach(name= body=str("could not found" + WifiName + " in device"))
                            closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            return ip_address_element_text, ssid_with_internet
                    except:
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ip_address_element_text, ssid_with_internet
                    #-------------------------------------------------------

                    # Selecting WIFI
                    # -------------------------------------------------------
                    try:
                        report.step_start("Selecting Wifi: " + WifiName)
                        print("Selecting Wifi")
                        wifiSelectionElement = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='" + WifiName + "']")))
                        wifiSelectionElement.click()
                        check_if_no_internet_popup(driver)
                    except Exception as e:
                        print("Exception on Selecting Wifi Network.  Please check wifi Name or signal")
                        request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ip_address_element_text, ssid_with_internet
                    # -------------------------------------------------------

                    # Set username
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Set User name")
                        print("Set User name")
                        wifiUserElement = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/edittext' and @password='false']")
                        wifiUserElement.send_keys(User)
                    except NoSuchElementException:
                        print("User name not Loaded")
                    # -------------------------------------------------------

                    # Set Password
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(6)
                        report.step_start("Set Password")
                        print("Set Password")
                        wifiPasswordElement = driver.find_element_by_xpath(
                            "//*[@text='Enter password']")
                        wifiPasswordElement.send_keys(ttls_passwd)
                        print("Entered Password")
                    except NoSuchElementException:
                        print("Password Page Not Loaded, password May be cached in the System")
                    # -------------------------------------------------------
                    # Selecting certificate
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Selecting CA Cert")
                        certElement = driver.find_element_by_xpath(
                            "//*[@text='Select certificate']")
                        certElement.click()
                    except NoSuchElementException:
                        print("Selecting certificate failed")
                    # -------------------------------------------------------
                    # Validating certificate
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Validting CA Cert")
                        certElement = driver.find_element_by_xpath(
                            "//*[@text=\"Don't validate\"]")
                        certElement.click()
                    except NoSuchElementException:
                        print("validation failed")
                    # -------------------------------------------------------

                    # Click on connect button
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Click Connect Button")
                        joinBTNElement = driver.find_element_by_xpath("//*[@text='Connect']")
                        joinBTNElement.click()
                    except NoSuchElementException:
                        print("Connect Button Not Enabled...Verify if Password is set properly  ")
                    check_if_no_internet_popup(driver)
                    # -------------------------------------------------------

                    #Verify if WiFi is connected
                    # -------------------------------------------------------
                    try:
                        report.step_start("Verify if Wifi is Connected")
                        WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH,
                            "//*[@resource-id='android:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                        ssid_with_internet = True
                        print("Wifi Successfully Connected")
                        # time.sleep(5)
                        check_if_no_internet_popup(driver)
                    except:
                        try:
                            check_if_no_internet_popup(driver)
                            WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH,
                                "//*[@resource-id='com.android.settings:id/summary' and @text='Connected without internet']/parent::*/android.widget.TextView[@text='"
                                                                + WifiName + "']")))
                            print("Wifi Successfully Connected without internet")
                            check_if_no_internet_popup(driver)
                        except:
                            try:
                                report.step_start("Verify if Wifi is Connected")
                                WifiInternetErrMsg = WebDriverWait(driver, 60).until(EC.presence_of_element_located((
                                    MobileBy.XPATH,
                                    "//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                                ssid_with_internet = True
                                print("Wifi Successfully Connected")
                            except NoSuchElementException:
                                print("Wifi Connection Error: " + WifiName)
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ip_address_element_text, ssid_with_internet
                    # -------------------------------------------------------

                    #Get into Additional Details
                    #To Get an IP Address
                    #To Forget connection
                    #To turn off auto. connect
                    # -------------------------------------------------------
                    try:
                        print("Into additional details")
                        time.sleep(2)
                        additional_details_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/layout_details']")
                        additional_details_element.click()
                        try:
                            time.sleep(2)
                            ip_address_element = driver.find_element_by_xpath(
                                                                "//*[@text='IP address']/parent::*/android.widget.TextView[@resource-id='com.android.settings:id/summary']")
                            ip_address_element_text = ip_address_element.text
                            print("Device IP address is :", ip_address_element_text)
                        except:
                            try:
                                time.sleep(2)
                                ip_address_element = driver.find_element_by_xpath(
                                    "//*[@text='IP address']/parent::*/android.widget.TextView[@resource-id='android:id/summary']")
                                ip_address_element_text = ip_address_element.text
                                print("Device IP address is :", ip_address_element_text)
                            except:
                                print("IP address element not found")
                               #allure.attach(name= body=str("IP address element not found"))

                            # closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            # return ip_address_element_text, ssid_with_internet

                        try:
                            check_if_no_internet_popup(driver)
                            driver.implicitly_wait(3)
                            time.sleep(2)
                            auto_reconnect_off = driver.find("//*[@resource-id='android:id/switch_widget']")
                            auto_reconnect_off_text = auto_reconnect_off.text
                            if auto_reconnect_off_text != "Off":
                                auto_reconnect_off.click()
                                print("Auto reconnect turning off")
                            else:
                                print("Auto reconnect is already off")
                        except:
                            print("Couldn't find auto reconnect element")

                        # ------------------------------- Forget SSID ----------------
                        try:
                            check_if_no_internet_popup(driver)
                            forget_ssid = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/forget_button']//*[@resource-id='com.android.settings:id/icon']")
                            forget_ssid.click()
                            print("Forgetting ssid")

                            #------------------------------- Wifi Switch ----------------
                            try:
                                print("clicking on wifi switch")
                                get_switch_element = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/switch_widget']")
                                driver.implicitly_wait(2)
                                get_switch_element.click()
                            except:
                                print("couldn't click on wifi switch")
                               #allure.attach(name= body=str("couldn't click on wifi switch"))
                        except:
                            print("Couldn't forget ssid")
                            # closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            # return ip_address_element_text, ssid_with_internet
                    except:
                        print("Couldn't get into Additional settings")
                    # -------------------------------------------------------
                except:
                    print("No Switch element found")
                # ---------------------To Turn on WIFi Switch if already OFF-------------------------------

            except:
                print("Couldn't find wifi Button")
            # ------------------Open WIFI page----------------------------------

        except:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")
        # -----------------To Open Connections page---------------------------
    else: #--------------------Pixel code-----------------------------------
        report.step_start("Set Wifi Network to " + WifiName)

        # -----------------To Open Connections page-----------------------
        try:
            print("Verifying Connected Wifi Connection in Pixel")
            report.step_start("Click Network & internet in pixel4")
            conn_element = driver.find_element_by_xpath("//*[@text='Network & internet']")
            conn_element.click()

            # ---------------------Open WIFI page-------------------------------
            try:
                report.step_start("Clicking Wi-Fi")
                print("Clicking WIFI")
                time.sleep(3)
                wifi_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='Wi‑Fi']")))
                wifi_element.click()

                # --------------------To Turn on WIFi Switch if already OFF--------------------------------
                try:
                    driver.implicitly_wait(1)
                    get_switch_text_element = driver.find_element_by_xpath(
                        "//*[@resource-id='android:id/icon']")
                    get_switch_text = get_switch_text_element.click()
                    if get_switch_text is not None:
                        switch_text = "Off"
                    else:
                        switch_text = "On"

                    print("get_switch_text: ", switch_text)
                    print("Find wifi switch")
                    try:  # To Turn on Wi-Fi Switch
                        if switch_text == "Off":
                            # driver.implicitly_wait(3)
                            get_switch_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/switch_widget']")
                            driver.implicitly_wait(1)
                            get_switch_element.click()
                            driver.implicitly_wait(1)
                            i = 0
                            for i in range(5):
                                if switch_text == "On":
                                    print("WIFI Switch is ON")
                                    break
                                else:
                                    try:
                                        get_switch_text_element = driver.find_element_by_xpath(
                                            "//*[@text='Add network']")
                                        get_switch_text = get_switch_text_element.text
                                        if get_switch_text == "Add network":
                                            switch_text = "On"
                                        else:
                                            switch_text = "Off"
                                    except NoSuchElementException:
                                        print("Exception: Verify Xpath")
                                    # Scroll Down
                                    scrollDown(setup_perfectoMobile)
                                    print("Sleeping for: ", i)
                                    time.sleep(i)
                                    pass
                            if switch_text == "Off":
                                print("Switch is Still OFF")
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ip_address_element_text, ssid_with_internet
                        else:
                            print("Switch is already On")
                            check_if_no_internet_popup(driver)
                    except:
                        print("Couldn't turn on WIFI switch")
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ip_address_element_text, ssid_with_internet

                    # ---------------------This is to Forget current connected SSID-------------------------------
                    try:  # To deal with already connected SSID
                        check_if_no_internet_popup(driver)
                        network_category = driver.find_element_by_xpath("//*[@text='Connected']")
                        try:  # To forget existing ssid
                            print("To forget ssid")
                            check_if_no_internet_popup(driver)
                            additional_details_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/settings_button_no_background']")
                            additional_details_element.click()
                        except:
                            print("Couldn't get into additional details")
                        try:
                            check_if_no_internet_popup(driver)
                            forget_ssid = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/button1']")
                            forget_ssid.click()
                            print("Forget old ssid")
                        except:
                            print("Couldn't forget ssid")
                            closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            return ip_address_element_text, ssid_with_internet
                    except:
                        print("No Connected SSIDS")
                    # ----------------------This is to Forget current connected SSID--------------------------------

                    time.sleep(2)
                    print("Selecting Wifi: " + WifiName)
                    # allure.attach(name= body=str("Selecting Wifi: " + WifiName))
                    ssid_found = False
                    available_ssids = False
                    # This is To get all available ssids
                    # ------------------------------------------------------
                    try:
                        for k in range(3):

                            # available_ssids = get_all_available_ssids(driver, deviceModelName)
                            # print("active_ssid_list: ", available_ssids)
                            # allure.attach(name="Available SSIDs in device: ", body=str(available_ssids))
                            available_ssids = []
                            try:
                                elements = WebDriverWait(driver, 20).until(
                                    EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='" + WifiName + "']")))
                                available_ssids.append(elements.text)
                            except:
                                pass

                            try:
                                if WifiName not in available_ssids:
                                    scrollDown(setup_perfectoMobile)
                                    time.sleep(2)
                                else:
                                    ssid_found = True
                                    print(WifiName + " : Found in Device")
                                    # allure.attach(name= body=str(WifiName+" : Found in Device"))
                                    break
                            except:
                                print("couldn't find wifi in available ssid")
                        if not ssid_found:
                            print("could not found " + WifiName + " in device")
                            # allure.attach(name= body=str("could not found" + WifiName + " in device"))
                            closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            return ip_address_element_text, ssid_with_internet
                    except:
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ip_address_element_text, ssid_with_internet
                    # -------------------------------------------------------

                    # Selecting WIFI
                    # -------------------------------------------------------
                    try:
                        report.step_start("Selecting Wifi: " + WifiName)
                        wifi_selection_element = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='" + WifiName + "']")))
                        wifi_selection_element.click()
                        check_if_no_internet_popup(driver)
                    except Exception as e:
                        print("Exception on Selecting Wifi Network.  Please check wifi Name or signal")
                        request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ip_address_element_text, ssid_with_internet
                    # -------------------------------------------------------
                    # -------------------------------------------------------
                    # Selecting certificate
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Selecting CA Cert")
                        print("Selecting certificate")
                        cert_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/ca_cert']")
                        cert_element.click()
                    except NoSuchElementException:
                        print("Selecting certificate failed")
                    # -------------------------------------------------------
                    # Validating certificate
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Validting CA Cert")
                        print("validation")
                        cert_element = driver.find_element_by_xpath(
                            "//*[@text='Do not validate']")
                        cert_element.click()
                    except NoSuchElementException:
                        print("validation failed")
                    # Set username
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Set User name")
                        print("Set User name")
                        wifi_user_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/identity']")
                        wifi_user_element.send_keys(User)
                    except NoSuchElementException:
                        print("User name not Loaded")
                    # -------------------------------------------------------
                    # Scroll Down
                    scrollDown(setup_perfectoMobile)
                    time.sleep(2)
                    # Set Password
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(6)
                        report.step_start("Set Password")
                        print("Set Password")
                        time.sleep(5)
                        wifi_password_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/password']")
                        print("Entered Password1")
                        wifi_password_element.send_keys(ttls_passwd)
                        print("Entered Password")
                    except NoSuchElementException:
                        print("Password Page Not Loaded, password May be cached in the System")

                    # -------------------------------------------------------

                    # Click on connect button
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Click Connect Button")
                        join_element = driver.find_element_by_xpath("//*[@text='Connect']")
                        join_element.click()
                    except NoSuchElementException:
                        print("Connect Button Not Enabled...Verify if Password is set properly  ")
                    check_if_no_internet_popup(driver)
                    # -------------------------------------------------------

                    # Verify if WiFi is connected
                    # -------------------------------------------------------
                    try:
                        report.step_start("Verify if Wifi is Connected")
                        WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH,
                                                            "//*[@resource-id='android:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                        ssid_with_internet = True
                        print("Wifi Successfully Connected")
                        # time.sleep(5)
                        check_if_no_internet_popup(driver)
                    except:
                        try:
                            check_if_no_internet_popup(driver)
                            WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH,
                                                                "//*[@resource-id='com.android.settings:id/summary' and @text='Connected without internet']/parent::*/android.widget.TextView[@text='"+ WifiName + "']")))
                            print("Wifi Successfully Connected without internet")
                            check_if_no_internet_popup(driver)
                        except:
                            try:
                                report.step_start("Verify if Wifi is Connected")
                                WifiInternetErrMsg = WebDriverWait(driver, 60).until(EC.presence_of_element_located((
                                    MobileBy.XPATH,
                                    "//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                                ssid_with_internet = True
                                print("Wifi Successfully Connected")
                            except NoSuchElementException:
                                print("Wifi Connection Error: " + WifiName)
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ip_address_element_text, ssid_with_internet
                    # -------------------------------------------------------

                    # Get into Additional Details
                    # To Get an IP Address
                    # To Forget connection
                    # To turn off auto. connect
                    # -------------------------------------------------------
                    try:
                        print("Into additional details")
                        time.sleep(5)
                        report.step_start("Going for ip address")
                        additional_details_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/settings_button_no_background']")
                        additional_details_element.click()
                        print("Entered ssid")
                        try:
                            time.sleep(10)
                            print("clicking Advanced")
                            report.step_start("clicking Advanced")
                            advanced_element = driver.find_element_by_xpath("//*[@text='Advanced']")
                            advanced_element.click()
                            print("clicked Advanced")
                            #print("Device IP address is :", ip_address_element_text)
                        except:
                            try:
                                time.sleep(5)
                                print("clicking Advanced2")
                                advanced_element = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/recycler_view']/android.widget.FrameLayout[2]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]")
                                advanced_element.click()
                                #print("Device IP address is :", ip_address_element_text)
                            except:
                                try:
                                    time.sleep(5)
                                    print("clicking Advanced2")
                                    advanced_element = driver.find_element_by_xpath(
                                        "//*[@resource-id='com.android.settings:id/recycler_view']/android.widget.LinearLayout[5]/android.widget.LinearLayout[1]/android.widget.ImageView[1]")
                                    advanced_element.click()
                                except:
                                    print("No advanced options")
                            # allure.attach(name= body=str("IP address element not found"))

                            # closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            # return ip_address_element_text, ssid_with_internet
                        # Scroll Down
                        scrollDown(setup_perfectoMobile)
                        try:
                            time.sleep(2)
                            ip_address_element = driver.find_element_by_xpath(
                                "//*[@text='IP address']/parent::*/android.widget.TextView[@resource-id='android:id/summary']")
                            ip_address_element_text = ip_address_element.text
                            print("Device IP address is :", ip_address_element_text)
                        except:
                            print("IP address element not found")
                        #------------------------------- Forget SSID ----------------
                        try:
                            check_if_no_internet_popup(driver)
                            forget_ssid = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/settings_button_no_background']")
                            forget_ssid.click()
                            print("Forgetting ssid")

                            # ------------------------------- Wifi Switch ----------------
                            try:
                                print("clicking on wifi switch")
                                get_switch_element = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/switch_widget']")
                                driver.implicitly_wait(2)
                                get_switch_element.click()
                            except:
                                print("couldn't click on wifi switch")
                            # allure.attach(name= body=str("couldn't click on wifi switch"))
                        except:
                            print("Couldn't forget ssid")
                            # closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            # return ip_address_element_text, ssid_with_internet
                    except:
                        print("Couldn't get into Additional settings")
                    # -------------------------------------------------------
                except:
                    print("No Switch element found")
                # ---------------------To Turn on WIFi Switch if already OFF-------------------------------

            except:
                print("Couldn't find wifi Button")
            # ------------------Open WIFI page----------------------------------

        except:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")
        # -----------------To Open Connections page---------------------------
    closeApp(connData["appPackage-android"], setup_perfectoMobile)
    return ip_address_element_text, ssid_with_internet
#only to connect to wifi
def wifi_connect_eap(request, WifiName, User, ttls_passwd, setup_perfectoMobile, connData):
    print("\n-------------------------------------")
    print("Select Wifi/AccessPoint Connection")
    print("-------------------------------------")
    print("Verifying Wifi Connection Details....")
   #allure.attach(name= body=str("\n-------------------------------------"))
    report = setup_perfectoMobile[1]
    driver = setup_perfectoMobile[0]

    ssid_with_internet = False

    report.step_start("Switching Driver Context")
    print("Switching Context to Native")
    contexts = driver.contexts
    driver.switch_to.context(contexts[0])

    # Open Settings Application
    openApp(connData["appPackage-android"], setup_perfectoMobile)
    deviceModelName = getDeviceModelName(setup_perfectoMobile)
    print("Selected Device Model: " + deviceModelName)
   #allure.attach(name= body=str("\Selected Device Model: " + deviceModelName))
    if deviceModelName != ("Pixel 4"):
        report.step_start("Set Wifi Network to " + WifiName)


        # -----------------To Open Connections page-----------------------
        try:
            print("Verifying Connected Wifi Connection")
            report.step_start("Click Connections")
            connElement = driver.find_element_by_xpath("//*[@text='Connections']")
            connElement.click()


            # ---------------------Open WIFI page-------------------------------
            try:
                report.step_start("Clicking Wi-Fi")
                print("Clicking WIFI")
                wifiElement = driver.find_element_by_xpath("//*[@text='Wi-Fi']")
                wifiElement.click()


                # --------------------To Turn on WIFi Switch if already OFF--------------------------------
                try:
                    driver.implicitly_wait(1)
                    get_switch_text_element = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/switch_text']")
                    get_switch_text = get_switch_text_element.text
                    print("get_switch_text: ",get_switch_text)
                    print("Find wifi switch")
                    try: #To Turn on Wi-Fi Switch
                        if get_switch_text == "Off":
                            # driver.implicitly_wait(3)
                            get_switch_element = driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/switch_widget']")
                            driver.implicitly_wait(1)
                            get_switch_element.click()
                            driver.implicitly_wait(1)
                            i = 0
                            for i in range(5):
                                if get_switch_text == "On":
                                    print("WIFI Switch is ON")
                                    break
                                else:
                                    try:
                                        get_switch_text_element = driver.find_element_by_xpath(
                                            "//*[@resource-id='com.android.settings:id/switch_text']")
                                        get_switch_text = get_switch_text_element.text
                                    except:
                                        pass
                                    print("Sleeping for: ", i)
                                    time.sleep(i)
                                    pass
                            if get_switch_text == "Off":
                                print("Switch is Still OFF")
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ssid_with_internet
                        else:
                            print("Switch is already On")
                            check_if_no_internet_popup(driver)
                    except:
                        print("Couldn't turn on WIFI switch")
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ssid_with_internet

                    #---------------------This is to Forget current connected SSID-------------------------------
                    try: #To deal with already connected SSID
                        check_if_no_internet_popup(driver)
                        network_category = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/connected_network_category']")
                        try: #To forget exhisting ssid
                            print("To forget ssid")
                            check_if_no_internet_popup(driver)
                            additional_details_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/layout_details']")
                            additional_details_element.click()
                            try:
                                check_if_no_internet_popup(driver)
                                forget_ssid = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/forget_button']//*[@resource-id='com.android.settings:id/icon']")
                                forget_ssid.click()
                                print("Forget old ssid")
                            except:
                                print("Couldn't forget ssid")
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ssid_with_internet
                        except:
                            print("Couldn't get into additional details")
                    except:
                        print("No Connected SSIDS")
                    #----------------------This is to Forget current connected SSID--------------------------------


                    print("Searching for Wifi: " + WifiName)
                   #allure.attach(name= body=str("Searching for Wifi: " + WifiName))
                    time.sleep(2)
                    print("Selecting Wifi: " + WifiName)
                    ssid_found = False
                    available_ssids = False
                    # This is To get all available ssids
                    # ------------------------------------------------------
                    try:
                        for check_for_all_ssids in range(2):
                            available_ssids = get_all_available_ssids(driver, deviceModelName)
                            try:
                                if WifiName not in available_ssids:
                                    scrollDown(setup_perfectoMobile)
                                    time.sleep(2)
                                else:
                                    ssid_found = True
                                    print(WifiName + " : Found in Device")
                                   #allure.attach(name= body=str(WifiName + " : Found in Device"))
                                    break
                            except:
                                print("1538")
                                pass
                        if not ssid_found:
                            print("could not found" + WifiName + " in device")
                           #allure.attach(name= body=str("could not found" + WifiName + " in device"))
                            closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            return ssid_with_internet
                    except:
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ssid_with_internet
                    # -------------------------------------------------------

                    # Selecting WIFI
                    # -------------------------------------------------------
                    try:
                        report.step_start("Selecting Wifi: " + WifiName)
                        print("Selecting Wifi")
                        wifiSelectionElement = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='" + WifiName + "']")))
                        wifiSelectionElement.click()
                        check_if_no_internet_popup(driver)
                    except Exception as e:
                        print("Exception on Selecting Wifi Network.  Please check wifi Name or signal")
                        request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ssid_with_internet
                    # -------------------------------------------------------

                    # Set username
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Set User name")
                        print("Set User name")
                        wifiUserElement = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/edittext' and @password='false']")
                        wifiUserElement.send_keys(User)
                    except NoSuchElementException:
                        print("User name not Loaded")
                    # -------------------------------------------------------

                    # Set Password
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(6)
                        report.step_start("Set Password")
                        print("Set Password")
                        wifiPasswordElement = driver.find_element_by_xpath(
                            "//*[@text='Enter password']")
                        wifiPasswordElement.send_keys(ttls_passwd)
                        print("Entered Password")
                    except NoSuchElementException:
                        print("Password Page Not Loaded, password May be cached in the System")
                    # -------------------------------------------------------
                    # Selecting certificate
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Selecting CA Cert")
                        certElement = driver.find_element_by_xpath(
                            "//*[@text='Select certificate']")
                        certElement.click()
                    except NoSuchElementException:
                        print("Selecting certificate failed")
                    # -------------------------------------------------------
                    # Validating certificate
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Validting CA Cert")
                        certElement = driver.find_element_by_xpath(
                            "//*[@text=\"Don't validate\"]")
                        certElement.click()
                    except NoSuchElementException:
                        print("validation failed")
                    # -------------------------------------------------------

                    # Click on connect button
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Click Connect Button")
                        joinBTNElement = driver.find_element_by_xpath("//*[@text='Connect']")
                        joinBTNElement.click()
                    except NoSuchElementException:
                        print("Connect Button Not Enabled...Verify if Password is set properly  ")
                    check_if_no_internet_popup(driver)
                    # -------------------------------------------------------

                    #Verify if WiFi is connected
                    # -------------------------------------------------------
                    try:
                        report.step_start("Verify if Wifi is Connected")
                        WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH,
                            "//*[@resource-id='android:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                        ssid_with_internet = True
                        print("Wifi Successfully Connected")
                       #allure.attach(name= body=str("Wifi Successfully Connected"))
                        # time.sleep(5)
                        check_if_no_internet_popup(driver)
                    except:
                        try:
                            check_if_no_internet_popup(driver)
                            WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH,
                                "//*[@resource-id='com.android.settings:id/summary' and @text='Connected without internet']/parent::*/android.widget.TextView[@text='"
                                                                + WifiName + "']")))
                            print("Wifi Successfully Connected without internet")
                           #allure.attach(name= body=str("Wifi Successfully Connected without internet"))
                            check_if_no_internet_popup(driver)
                        except:
                            try:
                                report.step_start("Verify if Wifi is Connected")
                                WifiInternetErrMsg = WebDriverWait(driver, 60).until(EC.presence_of_element_located((
                                    MobileBy.XPATH,
                                    "//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                                ssid_with_internet = True
                                print("Wifi Successfully Connected")
                               #allure.attach(name=body=str("Wifi Successfully Connected"))
                            except NoSuchElementException:
                                print("Wifi Connection Error: " + WifiName)
                               #allure.attach(name=body=str("Wifi Connection Error: " + WifiName))
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ssid_with_internet


                except NoSuchElementException:
                    print("No Switch element found")
                   #allure.attach(name= body=str("No Switch element found"))
                # ---------------------To Turn on WIFi Switch if already OFF-------------------------------

            except NoSuchElementException:
                print("Couldn't find wifi Button")
                #allure.attach(name= body=str("Couldn't find wifi Button"))
            # ------------------Open WIFI page----------------------------------

        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")
           #allure.attach(name= body=str("Exception: Verify Xpath - Update/check Xpath for Click Connections"))
        # -----------------To Open Connections page---------------------------
    else: #--------------Pixel 4 code--------------------------
        report.step_start("Set Wifi Network to " + WifiName)

        # -----------------To Open Connections page-----------------------
        try:
            print("Verifying Connected Wifi Connection")
            report.step_start("Click Network & internet in pixel4")
            conn_element = driver.find_element_by_xpath("//*[@text='Network & internet']")
            conn_element.click()

            # ---------------------Open WIFI page-------------------------------
            try:
                report.step_start("Clicking Wi-Fi")
                print("Clicking WIFI")
                time.sleep(3)
                wifi_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='Wi‑Fi']")))
                wifi_element.click()

                # --------------------To Turn on WIFi Switch if already OFF--------------------------------
                try:
                    driver.implicitly_wait(1)
                    get_switch_text_element = driver.find_element_by_xpath(
                        "//*[@resource-id='android:id/icon']")
                    get_switch_text = get_switch_text_element.click()
                    if get_switch_text is not None:
                        switch_text = "Off"
                    else:
                        switch_text = "On"

                    print("get_switch_text: ", switch_text)
                    print("Find wifi switch")
                    try:  # To Turn on Wi-Fi Switch
                        if switch_text == "Off":
                            # driver.implicitly_wait(3)
                            get_switch_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/switch_widget']")
                            driver.implicitly_wait(1)
                            get_switch_element.click()
                            driver.implicitly_wait(1)
                            i = 0
                            for i in range(5):
                                if switch_text == "On":
                                    print("WIFI Switch is ON")
                                    break
                                else:
                                    try:
                                        get_switch_text_element = driver.find_element_by_xpath(
                                            "//*[@text='Add network']")
                                        get_switch_text = get_switch_text_element.text
                                        if get_switch_text == "Add network":
                                            switch_text = "On"
                                        else:
                                            switch_text = "Off"
                                    except NoSuchElementException:
                                        print("Exception: Verify Xpath")
                                    # Scroll Down
                                    scrollDown(setup_perfectoMobile)
                                    print("Sleeping for: ", i)
                                    time.sleep(i)
                                    pass
                            if switch_text == "Off":
                                print("Switch is Still OFF")
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ssid_with_internet
                        else:
                            print("Switch is already On")
                            check_if_no_internet_popup(driver)
                    except:
                        print("Couldn't turn on WIFI switch")
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ssid_with_internet

                    # ---------------------This is to Forget current connected SSID-------------------------------
                    try:  # To deal with already connected SSID
                        check_if_no_internet_popup(driver)
                        network_category = driver.find_element_by_xpath("//*[@text='Connected']")
                        try:  # To forget existing ssid
                            print("To forget ssid")
                            check_if_no_internet_popup(driver)
                            additional_details_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/settings_button_no_background']")
                            additional_details_element.click()
                        except:
                            print("Couldn't get into additional details")
                        try:
                            check_if_no_internet_popup(driver)
                            forget_ssid = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/button1']")
                            forget_ssid.click()
                            print("Forget old ssid")
                        except:
                            print("Couldn't forget ssid")
                            closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            return ssid_with_internet
                    except:
                        print("No Connected SSIDS")
                    # ----------------------This is to Forget current connected SSID--------------------------------

                    time.sleep(2)
                    print("Selecting Wifi: " + WifiName)
                    # allure.attach(name= body=str("Selecting Wifi: " + WifiName))
                    ssid_found = False
                    available_ssids = False
                    # This is To get all available ssids
                    # ------------------------------------------------------
                    try:
                        for k in range(3):
                            # available_ssids = get_all_available_ssids(driver, deviceModelName)
                            # print("active_ssid_list: ", available_ssids)
                            available_ssids = []
                            try:
                                elements = WebDriverWait(driver, 20).until(
                                    EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='" + WifiName + "']")))
                                available_ssids.append(elements.text)
                            except:
                                pass
                            #allure.attach(name="Available SSIDs in device: ", body=str(available_ssids))
                            try:
                                if WifiName not in available_ssids:
                                    scrollDown(setup_perfectoMobile)
                                    time.sleep(2)
                                else:
                                    ssid_found = True
                                    print(WifiName + " : Found in Device")
                                    # allure.attach(name= body=str(WifiName+" : Found in Device"))
                                    break
                            except:
                                print("couldn't find wifi in available ssid")
                        if not ssid_found:
                            print("could not found " + WifiName + " in device")
                            # allure.attach(name= body=str("could not found" + WifiName + " in device"))
                            closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            return ssid_with_internet
                    except:
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ssid_with_internet
                    # -------------------------------------------------------

                    # Selecting WIFI
                    # -------------------------------------------------------
                    try:
                        report.step_start("Selecting Wifi: " + WifiName)
                        wifi_selection_element = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='" + WifiName + "']")))
                        wifi_selection_element.click()
                        check_if_no_internet_popup(driver)
                    except Exception as e:
                        print("Exception on Selecting Wifi Network.  Please check wifi Name or signal")
                        request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                        closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ssid_with_internet
                    # -------------------------------------------------------
                    # Selecting certificate
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Selecting CA Cert")
                        cert_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/ca_cert']")
                        cert_element.click()
                    except NoSuchElementException:
                        print("Selecting certificate failed")
                    # -------------------------------------------------------
                    # Validating certificate
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Validting CA Cert")
                        cert_element = driver.find_element_by_xpath(
                            "//*[@text='Do not validate']")
                        cert_element.click()
                    except NoSuchElementException:
                        print("validation failed")
                    # Set username
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Set User name")
                        print("Set User name")
                        wifi_user_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/identity']")
                        wifi_user_element.send_keys(User)
                    except NoSuchElementException:
                        print("User name not Loaded")
                    # -------------------------------------------------------
                    # Scroll Down
                    scrollDown(setup_perfectoMobile)
                    time.sleep(2)
                    # Set Password
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(6)
                        report.step_start("Set Password")
                        print("Set Password")
                        wifi_password_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/password']")
                        wifi_password_element.send_keys(ttls_passwd)
                        print("Entered Password")
                    except NoSuchElementException:
                        print("Password Page Not Loaded, password May be cached in the System")

                    # -------------------------------------------------------

                    # Click on connect button
                    # -------------------------------------------------------
                    try:
                        driver.implicitly_wait(3)
                        report.step_start("Click Connect Button")
                        join_element = driver.find_element_by_xpath("//*[@text='Connect']")
                        join_element.click()
                    except NoSuchElementException:
                        print("Connect Button Not Enabled...Verify if Password is set properly  ")
                    check_if_no_internet_popup(driver)
                    # -------------------------------------------------------

                    # Verify if WiFi is connected
                    # -------------------------------------------------------
                    try:
                        report.step_start("Verify if Wifi is Connected")
                        WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH,
                                                            "//*[@resource-id='android:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                        ssid_with_internet = True
                        print("Wifi Successfully Connected")
                        # time.sleep(5)
                        check_if_no_internet_popup(driver)
                    except:
                        try:
                            check_if_no_internet_popup(driver)
                            WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH,
                                                                "//*[@resource-id='com.android.settings:id/summary' and @text='Connected without internet']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                            print("Wifi Successfully Connected without internet")
                            check_if_no_internet_popup(driver)
                        except:
                            try:
                                report.step_start("Verify if Wifi is Connected")
                                WifiInternetErrMsg = WebDriverWait(driver, 60).until(EC.presence_of_element_located((
                                    MobileBy.XPATH,
                                    "//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
                                ssid_with_internet = True
                                print("Wifi Successfully Connected")
                            except NoSuchElementException:
                                print("Wifi Connection Error: " + WifiName)
                                closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ssid_with_internet


                except NoSuchElementException:
                    print("No Switch element found")
                # allure.attach(name= body=str("No Switch element found"))
                # ---------------------To Turn on WIFi Switch if already OFF-------------------------------

            except NoSuchElementException:
                print("Couldn't find wifi Button")
                # allure.attach(name= body=str("Couldn't find wifi Button"))
            # ------------------Open WIFI page----------------------------------

        except NoSuchElementException:
            print("Exception: Verify Xpath - Update/check Xpath for Click Connections")
        # allure.attach(name= body=str("Exception: Verify Xpath - Update/check Xpath for Click Connections"))
        # -----------------To Open Connections page---------------------------

    closeApp(connData["appPackage-android"], setup_perfectoMobile)
    return ssid_with_internet

def close_driver(driver):
    driver.close()
    driver.quit()

# def capture_start_har(setup_perfectoMobile):
#     setup_perfectoMobile[1].step_start("Start HAR capture on Phone...")
#     # params = {'generateHarFile', 'true'}
#     params = {'generateHarFile' : 'true'}
#     setup_perfectoMobile[0].execute_script('mobile:vnetwork:start', params)
#
# def capture_stop_har(setup_perfectoMobile):
#     setup_perfectoMobile[1].step_start("Stop HAR capture on Phone...")
#     params = {'generateHarFile' : 'true'}
#     setup_perfectoMobile[0].execute_script('mobile:vnetwork:stop', params)