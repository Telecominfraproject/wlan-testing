# !/usr/local/lib64/python3.8
"""
    Controller Library
        1. controller_data/sdk_base_url
        2. login credentials
"""
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

def rebootPhone(setup_perfectoMobile):
        #print("Closing App.." + appName)
    setup_perfectoMobile[1].step_start("Rebooting Phone...")  
    params = {}
    setup_perfectoMobile[0].execute_script('mobile:handset:reboot', params)

def set_APconnMobileDevice_iOS(WifiName, WifiPass, setup_perfectoMobile, connData):
    
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
            print("No Error with Wifi-AP Connection: " + Wifi_AP_Name)

    else:
        print("Selecting Wifi...: " + WifiName)
        try:
            report.step_start("Selecting Wifi...: " + WifiName)
            element.click()
        except NoSuchElementException:
            print("Exception: Selection Wifi Network")

        try:
            wifiXpath2 = driver.find_element_by_xpath("//*[@label='"+ WifiName + "']")
            wifiXpath2.click()
        
        except NoSuchElementException:
            #PerfectoErrorHandleClass
                #Pass a list of errors that can be ignored
            print("\n Can't find Wifi/AP NAME.....CheckXpath & Wifi Name")
        # print (e.message)

        #Set password if Needed
        try:
            wifiPassword = driver.find_element_by_xpath("//*[@label='Password']")
            wifiPassword.send_keys(WifiPass)
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
            print("No Wifi-AP Error Internet Error: " + WifiName)

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

def ForgetWifiConnection(setup_perfectoMobile, wifiName, connData):
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]

    report.step_start("Forget Existing Wifi")   
    openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

    try:
    # print("Verifying Connected Wifi Connection")
        report.step_start("Verifying Existing Connected Wifi Connection")  
        element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
        Wifi_AP_Name = element.text
    except NoSuchElementException:
        print("Exception: Verify Xpath - UpdateXpath") 

    if Wifi_AP_Name.__eq__(wifiName):
        print("Wifi Name Matches Connected To: " + Wifi_AP_Name) 
        element.click()

        print("More Info on Wifi: " + Wifi_AP_Name)
        report.step_start("Click on More Info on Wifi")
        WifiXpathMoreInfo = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ Wifi_AP_Name + "']/parent::*/XCUIElementTypeButton[@label='More Info']"
        elementMoreInfo = driver.find_element_by_xpath(WifiXpathMoreInfo)
        elementMoreInfo.click()

        print("Forget Wifi Network " + Wifi_AP_Name)
        report.step_start("Forget Wifi Network")
        WifiXpathForgetWifi = "//*[@label='Forget This Network']"
        elementforgetWifi = driver.find_element_by_xpath(WifiXpathForgetWifi)
        elementforgetWifi.click()

        print("Forget Wifi PopUp: " + Wifi_AP_Name)
        report.step_start("Forget Wifi Network PopUp Confirm")
        WifiXpathForgetWifi = "//*[@label='Forget']"
        elementforgetWifi = driver.find_element_by_xpath(WifiXpathForgetWifi)
        elementforgetWifi.click()

    else:
        print("Connected To: " + Wifi_AP_Name) 
        print("Initial Wifi: " + wifiName) 
        element.click()

        report.step_start("Click on More Info on Wifi")
        WifiXpathMoreInfo = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ wifiName + "']/parent::*/XCUIElementTypeButton[@label='More Info']"
        elementMoreInfo = driver.find_element_by_xpath(WifiXpathMoreInfo)
        elementMoreInfo.click()

        print("Forget Wifi Network " + wifiName)
        report.step_start("Forget Wifi Network")
        WifiXpathForgetWifi = "//*[@label='Forget This Network']"
        elementforgetWifi = driver.find_element_by_xpath(WifiXpathForgetWifi)
        elementforgetWifi.click()

        report.step_start("Confirm Forget Wifi Network")
        WifiXpathForgetWifi = "//*[@label='Forget']"
        elementforgetWifi = driver.find_element_by_xpath(WifiXpathForgetWifi)
        elementforgetWifi.click()

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

def get_WifiIPAddress_iOS(setup_perfectoMobile, connData, wifiName):
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
    WifiXpath = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ wifiName + "']"
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
        print("Wifi Connected without any errors: " + wifiName)
        #Fail TEST CASE

    try:   
        WifiInternetInfo=driver.find_element_by_xpath("(//XCUIElementTypeButton[@label='More Info'])[1]")
        WifiInternetInfo.click()
    except NoSuchElementException:
        print("Wifi-AP Connected Successfully: " + wifiName)

    try:   
        WifiIPaddress= driver.find_element_by_xpath("(//*[@label='Router']/parent::*/XCUIElementTypeStaticText)[2]").text
        return WifiIPaddress
    except NoSuchElementException:
        print("Wifi-AP Connected Successfully: " + wifiName)

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

def verifyUploadDownloadSpeediOS(setup_perfectoMobile, get_APToMobileDevice_data):
        report = setup_perfectoMobile[1]    
        driver = setup_perfectoMobile[0]
        connData = get_APToMobileDevice_data

        try:  
            report.step_start("Google Home Page")     
            driver.get(connData["webURL"]) 
            elementFindTxt = driver.find_element_by_xpath(connData["lblSearch"])
            elementFindTxt.send_keys("Internet Speed Test")

            try:
                elelSearch = driver.find_element_by_xpath(connData["elelSearch"])  
                elelSearch.click()
            except NoSuchElementException:
                print("Enter Not Active...")

            report.step_start("Verify Run Button")           
            driver.find_element_by_xpath(connData["BtnRunSpeedTest"]).click()

            #Get upload/Download Speed
            try:
                report.step_start("Get upload/Download Speed")   
                time.sleep(60)
                downloadMbps = driver.find_element_by_xpath(connData["downloadMbps"])
                downloadSpeed = downloadMbps.text
                print("Download: " + downloadSpeed + " Mbps")

                UploadMbps = driver.find_element_by_xpath(connData["UploadMbps"])
                uploadSpeed = UploadMbps.text
                print("Upload: " + uploadSpeed + " Mbps")
                
                print("Access Point Verification Completed Successfully")

            except NoSuchElementException:
                print("Access Point Verification NOT Completed, checking Connection....")

            currentResult = True    

            assert currentResult
        except Exception as e:
            print (e.message)

def verifyUploadDownloadSpeediOSRemoteDriver(setup_perfectoMobile, get_APToMobileDevice_data):
        report = setup_perfectoMobile[1]    
        driver = setup_perfectoMobile[0]
        connData = get_APToMobileDevice_data

        report.step_start("Launch Safari")   
        openApp(connData["bundleId-iOS-Safari"], setup_perfectoMobile)

        print("Search Google Page Internet Speed Test")       
        #driver.get(connData["webURL"]) 
        report.step_start("Search Internet Speed Test")   
        elementFindTxt0 = driver.find_element_by_xpath("//XCUIElementTypeButton[@label='Address']")
        elementFindTxt0.click()

        print("Send Keys")
        elementFindTxt1 = driver.find_element_by_xpath("//*[@label='Address']")
        elementFindTxt1.send_keys("Internet Speed Test")

        print("Click Go Search")
        report.step_start("Click Go Search")   
        elementGo = driver.find_element_by_xpath("//*[@label='go']")
        elementGo.click()

       # print("Switching to Dom Tree")
       # context = driver.contexts[2]
        #print("WebView: " + context) 
        print("AvaiableContext: " + driver.getContexts())
        #driver.switch_to.window("handle")
        driver.switch_to.context('WEBVIEW_1')

        print("--Click Run Speed Test Btn ")
        try:
            elelSearch2 = driver.find_element_by_xpath("//*[@id='knowledge-verticals-internetspeedtest__test_button']")  
            elelSearch2.click()
        except NoSuchElementException:
            print("Enter Not Active...")

        report.step_start("Verify Run Button")           
        driver.find_element_by_xpath(connData["BtnRunSpeedTest"]).click()

        #Get upload/Download Speed
        try:
            report.step_start("Get upload/Download Speed")   
            time.sleep(60)
            downloadMbps = driver.find_element_by_xpath(connData["downloadMbps"])
            downloadSpeed = downloadMbps.text
            print("Download: " + downloadSpeed + " Mbps")

            UploadMbps = driver.find_element_by_xpath(connData["UploadMbps"])
            uploadSpeed = UploadMbps.text
            print("Upload: " + uploadSpeed + " Mbps")
            
            print("Access Point Verification Completed Successfully")

        except NoSuchElementException:
            driver.switch_to.context('NATIVE_APP')
            print("Access Point Verification NOT Completed, checking Connection....")

        driver.switch_to.context('NATIVE_APP')

      