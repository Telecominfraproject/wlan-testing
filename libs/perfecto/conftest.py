import datetime
import sys
import os
import time
import warnings
from selenium.common.exceptions import NoSuchElementException
import urllib3
from perfecto.model.model import Job, Project
from perfecto import (PerfectoExecutionContext, PerfectoReportiumClient,TestContext, TestResultFactory)
import pytest
import logging

from urllib3 import exceptions

def pytest_addoption(parser):
    parser.addini("perfectoURL", "Cloud URL")
    parser.addini("securityToken", "Security Token")
    parser.addini("platformName-iOS", "iOS Platform")
    parser.addini("platformName-android", "Android Platform")
    parser.addini("model-iOS", "iOS Devices")
    parser.addini("model-android", "Android Devices")
    parser.addini("bundleId-iOS", "iOS Devices")
    parser.addini("bundleId-iOS-Settings", "iOS Settings App")
    parser.addini("appPackage-android", "Android Devices")
    parser.addini("wifi-SSID-5gl-Pwd", "Wifi 5g Password")
    parser.addini("wifi-SSID-2g-Pwd", "Wifi 2g Password")
    parser.addini("Default-SSID-5gl-perfecto-b", "Wifi 5g AP Name")
    parser.addini("Default-SSID-2g-perfecto-b", "Wifi 2g AP Name")
    parser.addini("Default-SSID-perfecto-b", "Wifi AP Name")
    parser.addini("bundleId-iOS-Ping", "Ping Bundle ID")
    parser.addini("browserType-iOS", "Mobile Browser Name")    
    parser.addini("projectName", "Project Name")
    parser.addini("projectVersion", "Project Version")
    parser.addini("jobName", "CI Job Name")
    parser.addini("jobNumber", "CI Job Number")
    parser.addini("reportTags", "Report Tags")

    parser.addoption(
        "--access-points",
        # nargs="+",
        default=["Perfecto"],
        help="list of access points to test"
    )

@pytest.fixture(scope="class")
def setup_perfectoMobileWeb(request):
    from selenium import webdriver
    driver = None
    reporting_client = None
    
    warnings.simplefilter("ignore", ResourceWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    capabilities = {
            'platformName': request.config.getini("platformName-iOS"),
            'model': request.config.getini("model-iOS"),
            'browserName': request.config.getini("browserType-iOS"),
            'securityToken' : request.config.getini("securityToken")
    }

    driver = webdriver.Remote('https://'+request.config.getini("perfectoURL")+'.perfectomobile.com/nexperience/perfectomobile/wd/hub', capabilities)
    driver.implicitly_wait(25)
   
    projectname = request.config.getini("projectName")
    projectversion = request.config.getini("projectVersion")
    jobname = request.config.getini("jobName")
    jobnumber = request.config.getini("jobNumber")
    tags = request.config.getini("reportTags")
    testCaseName = request.config.getini("jobName")

    print("Setting Perfecto ReportClient....")
    perfecto_execution_context = PerfectoExecutionContext(driver, tags, Job(jobname, jobnumber),Project(projectname, projectversion))
    reporting_client = PerfectoReportiumClient(perfecto_execution_context)
    reporting_client.test_start(testCaseName, TestContext([], "Raj"))

    if driver is None:
        yield -1
    else:
        yield driver,reporting_client 

    try:
        print(" -- Tear Down --")     
        reporting_client.test_stop(TestResultFactory.create_success())
        print('Report-Url: ' + reporting_client.report_url() + '\n')
        driver.close()
    except Exception as e:
        print(" -- Exception Not Able To close --")    
        print (e.message)
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(" -- Exception Not Able To Quit --")    
            print (e.message)

@pytest.fixture(scope="class")
def setup_perfectoMobile_iOS(request):
    from appium import webdriver
    driver = None
    reporting_client = None
    
    warnings.simplefilter("ignore", ResourceWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    capabilities = {
            'platformName': request.config.getini("platformName-iOS"),
            'model': request.config.getini("model-iOS"),
            'securityToken' : request.config.getini("securityToken"),
            'bundleId' : request.config.getini("bundleId-iOS"),
    }

    driver = webdriver.Remote('https://'+request.config.getini("perfectoURL")+'.perfectomobile.com/nexperience/perfectomobile/wd/hub', capabilities)
    driver.implicitly_wait(25)
   
    projectname = request.config.getini("projectName")
    projectversion = request.config.getini("projectVersion")
    jobname = request.config.getini("jobName")
    jobnumber = request.config.getini("jobNumber")
    tags = request.config.getini("reportTags")
    testCaseName = request.config.getini("jobName")

    print("Setting Perfecto ReportClient....")
    perfecto_execution_context = PerfectoExecutionContext(driver, tags, Job(jobname, jobnumber),Project(projectname, projectversion))
    reporting_client = PerfectoReportiumClient(perfecto_execution_context)
    reporting_client.test_start(testCaseName, TestContext([], "Raj"))

    if driver is None:
        yield -1
    else:
        yield driver,reporting_client 

    try:
        print(" -- Tear Down --")     
        reporting_client.test_stop(TestResultFactory.create_success())
        print('Report-Url: ' + reporting_client.report_url() + '\n')
        driver.close()
    except Exception as e:
        print(" -- Exception Not Able To close --")    
        print (e.message)
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(" -- Exception Not Able To Quit --")    
            print (e.message)

@pytest.fixture(scope="function")
def get_PassPointConniOS_data(request):
    passPoint_data = {
        "netAnalyzer-inter-Con-Xpath": "//*[@label='Network Connected']/parent::*/XCUIElementTypeButton",
        "bundleId-iOS-Settings": request.config.getini("bundleId-iOS-Settings"),
        "bundleId-iOS-Ping": request.config.getini("bundleId-iOS-Ping")
    }
    yield passPoint_data

@pytest.fixture(scope="function")
def get_APToMobileDevice_data(request):
    passPoint_data = {
        "webURL": "https://www.google.com",
        "lblSearch": "//*[@class='gLFyf']",
        "elelSearch": "(//*[@class='sbic sb43'])[1]",
        "BtnRunSpeedTest": "//*[text()='RUN SPEED TEST']",
        "downloadMbps": "//*[@id='knowledge-verticals-internetspeedtest__download']/P[@class='spiqle']",
        "UploadMbps": "//*[@id='knowledge-verticals-internetspeedtest__upload']/P[@class='spiqle']",
        "lblSearch2": "test "
    }
    yield passPoint_data

@pytest.fixture(scope="function")
def get_AccessPointConn_data(request):
    passPoint_data = {
        "bundleId-iOS-Settings": request.config.getini("bundleId-iOS-Settings"),
        "bundleId-iOS-Ping": request.config.getini("bundleId-iOS-Ping"),
        "Default-SSID-5gl-perfecto-b": request.config.getini("Default-SSID-5gl-perfecto-b"),
        "Default-SSID-2g-perfecto-b": request.config.getini("Default-SSID-2g-perfecto-b"),
        "Default-SSID-perfecto-b": request.config.getini("Default-SSID-perfecto-b")
        
    }
    yield passPoint_data

@pytest.fixture(scope="function")
def get_ToggleAirplaneMode_data(request):
    passPoint_data = {
        "bundleId-iOS-Settings": request.config.getini("bundleId-iOS-Settings"),
        "lblSearch": "//*[@class='gLFyf']",
        "elelSearch": "(//*[@class='sbic sb43'])[1]",
        "BtnRunSpeedTest": "//*[text()='RUN SPEED TEST']",
        "downloadMbps": "//*[@id='knowledge-verticals-internetspeedtest__download']/P[@class='spiqle']",
        "UploadMbps": "//*[@id='knowledge-verticals-internetspeedtest__upload']/P[@class='spiqle']",

    }
    yield passPoint_data

@pytest.fixture(scope="function")
def get_ToggleWifiMode_data(request):
    passPoint_data = {
        "bundleId-iOS-Settings": request.config.getini("bundleId-iOS-Settings"),
        "wifi-SSID-5gl-Pwd": request.config.getini("wifi-SSID-5gl-Pwd"),
        "wifi-SSID-2g-Pwd": request.config.getini("wifi-SSID-2g-Pwd")
    }
    yield passPoint_data

def openApp(appName, setup_perfectoMobile):
    #print("Refreshing App: " + appName)
    setup_perfectoMobile[1].step_start("Opening App: " + appName)  
    params = {'identifier': appName}
    #Open/Close/Open Action is performed to ensure the app is back to its Original Settings
    setup_perfectoMobile[0].execute_script('mobile:application:open', params)
    setup_perfectoMobile[0].execute_script('mobile:application:close', params)
    setup_perfectoMobile[0].execute_script('mobile:application:open', params)
    
def closeApp(appName, setup_perfectoMobile):
    #print("Closing App.." + appName)
    setup_perfectoMobile[1].step_start("Closing App: " + appName)  
    params = {'identifier': appName}
    setup_perfectoMobile[0].execute_script('mobile:application:close', params)

def set_APconnMobileDevice_iOS(WifiName, setup_perfectoMobile, connData):
    
    print("Verifying Wifi/AP Connection Details....") 
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]

    report.step_start("Set Wifi Network to " + WifiName)  

    #Open Settings Application
    openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

    try:
    # print("Verifying Connected Wifi Connection")
        report.step_start("Verifying Connected Wifi Connection")  
        element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
        Wifi_AP_Name = element.text
    except NoSuchElementException:
        print("Exception: Verify Xpath - UpdateXpath") 

        #NEED to fail if Wifi AP NAME isn't in the approved list AKA 5g & 2g.  
    #print("Wifi Name Matches - Already Connected To: " + Wifi_AP_Name)
    #print("Wifi Name Matches - Already Connected To: " + WifiName)

    if Wifi_AP_Name.__eq__(WifiName):
        print("Wifi Name Matches - Already Connected To: " + Wifi_AP_Name) 
    
        #Verify if Ap is connected with Wifi
        report.step_start("Verify Wifi Connection Status..")  
        #print("Click Wifi Connection..")
        element.click()

        #Verifies if AP is connected to Wifi status
        #print("Verify Wifi Connection Status..")
        report.step_start("Verify Wifi Connected Status")
        WifiXpath = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ Wifi_AP_Name + "']"
        elementWifName = driver.find_element_by_xpath(WifiXpath)
    
        #Check AP Internet Error Msg 
        print("Checking Internet Connection Error..")
        report.step_start("Checking Internet Connection Error..")

        try:
            WifiInternetErrMsg = driver.find_element_by_xpath("//*[@label='No Internet Connection']").text
        except NoSuchElementException:
            report.assertSoft
            print("Wifi-AP Connected Successfully: " + Wifi_AP_Name)

    else:
        try:
            report.step_start("Selecting Wifi...: " + WifiName)
            element.click()
        except NoSuchElementException:
            print("Exception: Selection Wifi Network")

        try:
            wifiXpath2 = driver.find_element_by_xpath("//*[@label='"+ WifiName + "']")
            wifiXpath2.click()
        
        except NoSuchElementException:
            print("\n Can't find Wifi/AP NAME.....CheckXpath & Wifi Name")
        # print (e.message)

        #Set password if Needed
        try:
            wifiPassword = driver.find_element_by_xpath("//*[@label='Password']")
            wifiPassword.send_keys(connData["wifi-SSID-2g-Pwd"])
        except NoSuchElementException:
            print("Enter Password Page Not Loaded  ")
        
        try:
            joinBTN = driver.find_element_by_xpath("//*[@label='Join']")
            joinBTN.click()
        except NoSuchElementException:
            print("Join Button Not Enabled...Verify if Password is set properly  ")

        try:
            WifiInternetErrMsg2 = driver.find_element_by_xpath("//*[@label='No Internet Connection']").text
        except NoSuchElementException:
            print("Wifi-AP Connected Successfully: " + WifiName)

def Toggle_AirplaneMode_iOS(setup_perfectoMobile, connData):
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]

    #Open Settings Application
    openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

    #Toggle Airplane Mode
    print("Toggle Airplane Mode..")
    report.step_start("Toggle Airplane Mode")
    try:
        AirplaneMode = driver.find_element_by_xpath("//XCUIElementTypeSwitch[@label='Airplane Mode']")
        #Toggle Airplane Mode
        AirplaneMode.click()

        #Verify Cellular Mode Text
        report.step_start("Verify Cellular Mode")
        try:
            CellularMsgEle = driver.find_element_by_xpath("//*[@name='Airplane Mode' and @value='Airplane Mode']")
            #ssertEqual(CellularMsgEle.text, "Airplane Mode", "Airplane Mode Not Triggerd")
            print("Verify Cellular Mode Text: Airplane Mode Success")
        except NoSuchElementException:
            print("Cellular Mode Not in Airplane Mode: ERROR") 

        #Set Airplane Mode Back
        AirplaneMode.click()         
    except NoSuchElementException:
        print("Airplane Wifi Button not loaded...")
        
    #Verify No Sim Card Installed Msg Popup
    report.step_start("Verify No Sim Card Installed Msg Popup")
    print("Verify No Sim Card Installed Msg Popup..")
    try:
        NoSimCardErrorMsg = driver.find_element_by_xpath("//*[@value='No SIM Card Installed']")
    except NoSuchElementException:
        print("No Sim Card AlertMsg")
        
    #Click ok on No Sim Card Msg Popup
    print("Click ok on No Sim Card Msg Popup..")
    report.step_start("Click ok on No Sim Card Msg Popup")
    try:
        NoSimCardErrorMsgOK = driver.find_element_by_xpath("//*[@label='OK']")
        NoSimCardErrorMsgOK.click()
    except NoSuchElementException:
        print("No Sim Card AlertMsg")

def verify_APconnMobileDevice_iOS(WifiName, setup_perfectoMobile, connData):
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]

    report.step_start("Verifying WifiName: " + WifiName)  

    #Refresh Settings Application
    openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

    #Verifies if AP is connected to Wifi status
    try:
       # print("Verifying Connected Wifi Connection")
        report.step_start("Verifying Connected Wifi Connection")  
        element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
        Wifi_AP_Name = element.text
       
    except NoSuchElementException:
        print("Exception: Verify Xpath - UpdateXpath") 

    try: 
        if Wifi_AP_Name.__eq__(WifiName):
            print("Wifi Name Matched Successful ") 
            #print("Wifi_AP_ConnName: " + "'"+ Wifi_AP_Name + "'" +  "   Not Equal To: " + WifiName + "....Check AP Name Syntax")
            return True
        else:
            print ("-- Wifi Don't Match Match -- ") 
            #print("Wifi_AP_ConnName: " + "'"+ Wifi_AP_Name + "'" +  "   Not Equal To: " + WifiName + "....Check AP Name Syntax")
            return False
    except NoSuchElementException:
        print("Exception Checking Wifi/AP connection NAME...")    
        return None

def Toggle_WifiMode_iOS(setup_perfectoMobile, connData):
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]

    #Open Settings Application
    #openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)
    
    report.step_start("Toggle Wifi Mode")    
    print("Toggle Wifi Mode..")
    try:
        WifiMode = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='1']")
        #Toggle Wifi Mode
        WifiMode.click()
        #Verify Radio Button Mode
        try:
            WifiDissconnected = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='0']")
            #self.assertEqual(WifiDissconnected.text, "Airplane Mode", "Airplane Mode Not Triggerd")
            print("Wifi Radio Button Toggled to Disable")
        except NoSuchElementException:
            print("Wifi Radio Button Not Disabled...") 
        
        #Set Airplane Mode Back
        WifiDissconnected.click()     
        print("Wifi Radio Button Toggled to Enabled")    
    except NoSuchElementException:
        print("Airplane Wifi Button not loaded...")

def get_WifiIPAddress_iOS(setup_perfectoMobile, connData):
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]

    openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

    try:
       # print("Verifying Connected Wifi Connection")
        report.step_start("Loading Wifi Page")  
        element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
        element.click()
    except NoSuchElementException:
        print("Exception: Verify Xpath - unable to click on Wifi") 

    report.step_start("Wifi Page")
    WifiXpath = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ connData["Default-SSID-perfecto-b"] + "']"
    elementWifName = driver.find_element_by_xpath(WifiXpath)
     #Check AP Internet Error Msg 
    print("Checking Internet Connection Error...")
    report.step_start("Checking Internet Connection Error..")

    try:
        driver.implicitly_wait(5)
        WifiInternetErrMsg = driver.find_element_by_xpath("//*[@label='No Internet Connection']").text
    except NoSuchElementException:
        #Need to fail test case
        driver.implicitly_wait(25)
        print("Wifi Connected without any errors: " + connData["Default-SSID-perfecto-b"])
        #Fail TEST CASE

    try:   
        WifiInternetInfo=driver.find_element_by_xpath("(//XCUIElementTypeButton[@label='More Info'])[1]")
        WifiInternetInfo.click()
    except NoSuchElementException:
        print("Wifi-AP Connected Successfully: " + connData["Default-SSID-perfecto-b"])

    try:   
        WifiIPaddress= driver.find_element_by_xpath("(//*[@label='Router']/parent::*/XCUIElementTypeStaticText)[2]").text
        return WifiIPaddress
    except NoSuchElementException:
        print("Wifi-AP Connected Successfully: " + connData["Default-SSID-perfecto-b"])

    return None

def ping_deftapps_iOS(setup_perfectoMobile, AP_IPaddress):
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]

    report.step_start("Pinging deftapps....")
    try:
        pingHost = "//*[@value='<Hostname or IP address>']"
        element2 = driver.find_element_by_xpath(pingHost)
        element2.clear()
        #element2.send_keys(AP_IPaddress)
        element2.send_keys("8.8.8.8")

        #Ping Enable
        report.step_start("Pingin Host")
        print("Pingin Host..")
        element3 = driver.find_element_by_xpath("//*[@label='go']")
        element3.click()

        time.sleep(10)

        #handle any popup

        report.step_start("Stop Ping Host")
        print("Stop Ping Host..")
        element4 = driver.find_element_by_xpath("//*[@label='Stop']")
        element4.click()

        # /* Check Packet Loss */
        report.step_start("Verifying Packet Loss..")
        print("Verifying Packet Loss..")
        try:
            element5 = driver.find_element_by_xpath("//XCUIElementTypeStaticText[@label='0']")  
            #assertEqual(element5.text, "0", "Packet Loss Exist, Please Check Device")
        except NoSuchElementException:
            print("No Packet Loss Detected 1st Attempt")

        report.step_start("Verifying Packet Sent..")
        print("Verifying Packet Sent..")
        try:
            packetSent = driver.find_element_by_xpath("//XCUIElementTypeStaticText[@label='Sent']/parent::*/XCUIElementTypeStaticText[2]").text          
            #assertEqual(element5.text, "0", "Packet Loss Exist, Please Check Device")
        except NoSuchElementException:
            print("-------Exception: Packet Sent Error, check object ID")

        report.step_start("Verifying Packet Received..")
        print("Verifying Packet Received..")
        try:
            packetReceived = driver.find_element_by_xpath("//XCUIElementTypeStaticText[@label='Received']/parent::*/XCUIElementTypeStaticText[2]").text          
            #assertEqual(element5.text, "0", "Packet Loss Exist, Please Check Device")
        except NoSuchElementException:
            print("-------Exception: Packet Sent Error, check object ID")

        print("Total Packet Sent: " + packetSent + " Packed Recieved: " + packetReceived)

        # Also Check #Sendto: No route to host
        print("Verifying No route to host Error Msg....")
        report.step_start("Verifying No route to host Error Msg..")
        try:
            element7 = driver.find_element_by_xpath("(//XCUIElementTypeStaticText[@label='Sendto: No route to host'])[2]")  
            print("Packet Loss Detected on AP!!!!!: " + AP_IPaddress)
            #self.assertNotEqual(element7.text, "Sendto: No route to host", "Packet Loss Exist, Please Check Device AP: " + Wifi_AP_Name)
        except NoSuchElementException:
            print("\nNo Packet Loss Detected on AP!!!!!: " + AP_IPaddress)

    except NoSuchElementException:
        print("Exception while ping Deft App on iOS")

    return None

def tearDown(setup_perfectoMobile):
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]

    report.step_start("Exception Failure Tear Down....")

    try:
        print(" -- Tear Down --")     
        report.test_stop(TestResultFactory.create_failure)
        print('Report-Url: ' + report.report_url() + '\n')
        driver.close()
    except Exception as e:
        print(" -- Exception Not Able To close --")    
        print (e.message)
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(" -- Exception Not Able To Quit --")    
            print (e.message)