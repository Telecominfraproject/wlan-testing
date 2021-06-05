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

@pytest.fixture(scope="function")
def setup_perfectoMobile_android(request):
    from appium import webdriver
    driver = None
    reporting_client = None
    
    warnings.simplefilter("ignore", ResourceWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
   
    capabilities = {
            'platformName': request.config.getini("platformName-android"),
            'model': request.config.getini("model-android"),
            'browserName': 'mobileOS',
            #'automationName' : 'Appium',
            'securityToken' : request.config.getini("securityToken"),  
            'useAppiumForWeb' : 'false',
            'useAppiumForHybrid' : 'false',
            #'bundleId' : request.config.getini("appPackage-android"),
    }

    driver = webdriver.Remote('https://'+request.config.getini("perfectoURL")+'.perfectomobile.com/nexperience/perfectomobile/wd/hub', capabilities)
    driver.implicitly_wait(35)
   
    TestCaseFullName = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
    nCurrentTestMethodNameSplit = re.sub(r'\[.*?\]\ *', "", TestCaseFullName)
    try:
        TestCaseName = nCurrentTestMethodNameSplit.removeprefix('test_')
        print ("\nTestCaseName: " + TestCaseName)
    except Exception as e:
        TestCaseName = nCurrentTestMethodNameSplit
        print("\nUpgrade Python to 3.9 to avoid test_ string in your test case name, see below URL")
        print("https://www.andreagrandi.it/2020/10/11/python39-introduces-removeprefix-removesuffix/")
        
    projectname = request.config.getini("projectName")
    projectversion = request.config.getini("projectVersion")
    jobname = request.config.getini("jobName")
    jobnumber = request.config.getini("jobNumber")
    tags = request.config.getini("reportTags")
    testCaseName = TestCaseName

    print("\nSetting Perfecto ReportClient....")
    perfecto_execution_context = PerfectoExecutionContext(driver, tags, Job(jobname, jobnumber),Project(projectname, projectversion))
    reporting_client = PerfectoReportiumClient(perfecto_execution_context)
    reporting_client.test_start(testCaseName, TestContext([], "Perforce"))

    def teardown():
        try:
            print("\n\n---------- Tear Down ----------")
            testFailed = request.session.testsfailed
            if testFailed>0:
                print ("Test Case Failure, please check report link: " + testCaseName)
                exceptionFailure = request.config.cache.get("SelectingWifiFailed", None)
                reporting_client.test_stop(TestResultFactory.create_failure(exceptionFailure))
                #seen = {None}
                #session = request.node
                #print(session)
            elif testFailed<=0:
                reporting_client.test_stop(TestResultFactory.create_success())
                
            #amount = len(request.session.items)
            #print("Test Session Items: ")
            #print(amount)

            #tests_count = request.session.testscollected
            #print("Test Collected: ")
            #print(tests_count)

            print('Report-Url: ' + reporting_client.report_url())
            print("----------------------------------------------------------")
            driver.close()
        except Exception as e:
            print(" -- Exception While Tear Down --")    
            reporting_client.test_stop(TestResultFactory.create_failure(e))
            print('Report-Url-Failure: ' + reporting_client.report_url() + '\n')
            driver.close()
            print (e)
        finally:
            try:
                driver.quit()
            except Exception as e:
                print(" -- Exception Not Able To Quit --")    
                print (e)

    request.addfinalizer(teardown)

    if driver is None:
        yield -1
    else:
        yield driver,reporting_client 

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
                WifiInternetErrMsg = WebDriverWait(driver, 35).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")))
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
                WifiForget= driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")     
                print("Wifi Not disconnected, check xpath for: " + WifiName)
            except NoSuchElementException:
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
                WifiForget= driver.find_element_by_xpath("//*[@resource-id='com.android.settings:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + WifiName + "']")     
                print("Wifi Not disconnected, check xpath for: " + WifiName)
              
            except NoSuchElementException:
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
        except NoSuchElementException:
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
    except NoSuchElementException:
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
        print("Launching Safari")
        report.step_start("Google Home Page") 
        driver.get(connData["webURL"]) 
        print("Enter Search Text")
        elementFindTxt = driver.find_element_by_xpath(connData["lblSearch"])
        elementFindTxt.send_keys("Internet Speed Test")
    except Exception as e:
        print("Launching Safari Failed")
        print (e)

    try:
        print("Click Search Button")
        report.step_start("Click Search Button") 
        elelSearch = driver.find_element_by_xpath("//*[@class='aajZCb']/li[1]/div[1]")  
        elelSearch.click()
    except NoSuchElementException:
        print("Search Drop Down not active...")

    print("Click Run Speed Test Button...")
    report.step_start("Click Run Speed Test Button")  
    driver.find_element_by_xpath(connData["BtnRunSpeedTest"]).click()

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
        
        print("Access Point Verification Completed Successfully")
        currentResult = True
    except NoSuchElementException:
        print("Access Point Verification NOT Completed, checking Connection....")

    return currentResult
 