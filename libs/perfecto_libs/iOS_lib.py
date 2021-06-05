# !/usr/local/lib64/python3.8
"""
    Controller Library
        1. controller_data/sdk_base_url
        2. login credentials
"""
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

def openApp(appName, setup_perfectoMobile):
    #print("Refreshing App: " + appName)
    setup_perfectoMobile[1].step_start("Opening App: " + appName)  
    params = {'identifier': appName}
    #Open/Close/Open Action is performed to ensure the app is back to its Original Settings
    setup_perfectoMobile[0].execute_script('mobile:application:open', params)
    setup_perfectoMobile[0].execute_script('mobile:application:close', params)
    setup_perfectoMobile[0].execute_script('mobile:application:open', params)

def scrollDown(setup_perfectoMobile):
    #print("Refreshing App: " + appName)
    setup_perfectoMobile[1].step_start("Scroll Down")  
    params = {'start': "40%,90%"}
    params = {'end': "40%,20%"}
    params = {'duration': "2"}
    #Open/Close/Open Action is performed to ensure the app is back to its Original Settings
    setup_perfectoMobile[0].execute_script('mobile:application:swipe', params)
  

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

def set_APconnMobileDevice_iOS(request, WifiName, WifiPass, setup_perfectoMobile, connData):
    consoleOutput = ""

    print("\n-------------------------------------")
    print("Select Wifi/AccessPoint Connection")
    print("-------------------------------------")
   
    reportFlag = True
   
    print("Verifying Wifi/AP Connection Details....") 
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]

    report.step_start("Switching Driver Context")  
    print("Switching Context to Native")
    contexts = driver.contexts
    #print(contexts)

    driver.switch_to.context(contexts[0])

    report.step_start("Set Wifi Network to " + WifiName)  
    #Open Settings Application
    openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

    try:
        print("Verifying Connected Wifi Connection")
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
        try:
            report.step_start("Verify Wifi Connected Status")
            WifiXpath = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ Wifi_AP_Name + "']"
            elementWifName = driver.find_element_by_xpath(WifiXpath)
        except NoSuchElementException:
            reportFlag = False
            assert reportFlag

        #Check AP Internet Error Msg 
        print("Checking Internet Connection Error..")
        report.step_start("Checking Internet Connection Error..")

        try:
            WifiInternetErrMsg = driver.find_element_by_xpath("//*[@label='No Internet Connection']").text
        except NoSuchElementException:
            print("No Error with Wifi-AP Connection: " + Wifi_AP_Name)

    else:
        print("Selecting Wifi: " + WifiName)   
        #consoleOutput+=str(WifiName)+ "\n"
        report.step_start("Selecting Wifi...: " + WifiName)
        element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
        element.click()
        try:
            wifiXpath2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='"+ WifiName + "']")))
            wifiXpath2.click()
        except Exception as e:
            print("Exception on Selecting Wifi Network.  Please check wifi Name or signal")
            request.config.cache.set(key="SelectingWifiFailed", value=str(e))
            #allure.attach(name="Raj", body="hello world")
            assert False
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
            reportFlag = False
        except NoSuchElementException:
            reportFlag = True
            print("No Wifi-AP Error Internet Error: " + WifiName)
    return reportFlag

def Toggle_AirplaneMode_iOS(request, setup_perfectoMobile, connData):
    print("\n-----------------------")
    print("Toggle Airplane Mode")
    print("-----------------------")
    
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]
    currentResult = True

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
            currentResult = False
            print("Cellular Mode Not in Airplane Mode: ERROR") 

        #Set Airplane Mode Back
        AirplaneMode.click()         
    except NoSuchElementException:
        currentResult = False
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

    return  currentResult

def verify_APconnMobileDevice_iOS(request, WifiName, setup_perfectoMobile, connData):
    print("\n-----------------------")
    print("Verify Connected Wifi Mode")
    print("-----------------------")
    
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]

    report.step_start("Verifying WifiName: " + WifiName)  

    #Refresh Settings Application
    openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

    #Verifies if AP is connected to Wifi status
    try:
       # print("Verifying Connected Wifi Connection")
        wifiXpath2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='"+ WifiName + "']")))
        wifiXpath2.click()
        
        report.step_start("Verifying Connected Wifi Connection")  
        element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
        Wifi_AP_Name = element.text
       
    except Exception as e:
        print("Exception on Selecting Wifi Network.  Please check wifi Name or signal")
        request.config.cache.set(key="SelectingWifiFailed", value=str(e))
        #allure.attach(name="Raj", body="hello world")
        assert False

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

def ForgetWifiConnection(request, setup_perfectoMobile, wifiName, connData):
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

def Toggle_WifiMode_iOS(request, setup_perfectoMobile, connData):
    print("\n-----------------------")
    print("Toggle Wifi Mode")
    print("-----------------------")
    
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

def get_WifiIPAddress_iOS(request, setup_perfectoMobile, connData, wifiName):
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
        WifiInternetErrMsg = driver.find_element_by_xpath("//*[@label='No Internet Connection']").text
    except NoSuchElementException:
        print("Wifi Connected without any errors: " + wifiName)

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
        print (e)
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(" -- Exception Not Able To Quit --")    
            print (e)

def verifyUploadDownloadSpeediOS(request, setup_perfectoMobile, get_APToMobileDevice_data):
    print("\n-------------------------------------")
    print("Verify Upload & Download Speed")
    print("-------------------------------------")
    
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]
    connData = get_APToMobileDevice_data
    currentResult = True

    contexts = driver.contexts
    #print("Printing Context")
    #print(contexts)

    driver.switch_to.context('WEBVIEW_1')
    
 
    print("Launching Safari")
    report.step_start("Google Home Page") 
    driver.get(connData["webURL"]) 
    print("Enter Search Text")
    elementFindTxt = driver.find_element_by_xpath(connData["lblSearch"])
    elementFindTxt.send_keys("Internet Speed Test")

    try:
        print("Click Search Button")
        elelSearch = driver.find_element_by_xpath("//*[@class='aajZCb']/li[1]/div[1]")  
        elelSearch.click()
    except NoSuchElementException:
        currentResult = False
        print("Search Drop Down not active...")

    print("Click Run Speed Test Button...")
    report.step_start("Click Run Speed Test Button")  
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
        currentResult = False
        
    return currentResult

def downloadInstallOpenRoamingProfile(request, setup_perfectoMobile, get_APToMobileDevice_data):
    print("\n-------------------------------------")
    print("Download Open Roaming Profile")
    print("-------------------------------------")
    
    OpenRoamingWifiName = ""

    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]
    connData = get_APToMobileDevice_data
    currentResult = True
    contexts = driver.contexts
    #print("Printing Context")
    #print(contexts)

    driver.switch_to.context('WEBVIEW_1')
    
    print("Launching Safari with OpenRoaming Profile")
    report.step_start("Open Roaming Download Page") 
    driver.get(connData["openRoaming-iOS-URL"]) 
  
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
  
    #Open Settings Application
    openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

    try:
        print("Click on downloaded Profile")
        report.step_start("Click on downloaded Profile") 
        downloadprofile = driver.find_element_by_xpath("//XCUIElementTypeStaticText[@label='Profile Downloaded']")  
        downloadprofile.click()
    except NoSuchElementException:
        print("Exception: Click Download Profile Button not showing up in settings")

    try:
        print("Install 1st Confirmation")
        report.step_start("Install 1st Confirmation") 
        install1stConf = driver.find_element_by_xpath("//XCUIElementTypeButton[@label='Install']")  
        install1stConf.click()
    except NoSuchElementException:
        print("Exception: Install 1st Confirmation")
  
    # //*[@label="The profile is not signed."]
    try:
        print("Install 2nd Confirmation")
        report.step_start("Install 2nd Confirmation") 
        install2ndConf = driver.find_element_by_xpath("//XCUIElementTypeButton[@label='Install'] ")  
        install2ndConf.click()
    except NoSuchElementException:
        print("Exception: Install 2nd Confirmation")

    try:
        print("Install 3rd Confirmation")
        report.step_start("Install 3rd Confirmation") 
        install3rdConf = driver.find_element_by_xpath("//XCUIElementTypeButton[@label='Install']")  
        install3rdConf.click()
    except NoSuchElementException:
        print("Exception: Install 3rd Confirmation")

    try:
        print("Verify Profile Installed")
        report.step_start("Verify Profile Installed") 
        elelSearch2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Profile Installed']")))
        elelSearch2.click()
    except Exception as e:
        print("Profile Installed Message Error")
        request.config.cache.set(key="SelectingWifiFailed", value=str(e))
        assert False

    try:
        print("Click Done Button")
        report.step_start("Click Done Button") 
        elelSearch = driver.find_element_by_xpath("//XCUIElementTypeButton[@label='Done']")  
        elelSearch.click()
    except NoSuchElementException:
        print("Exception: Clicking on Done Button")

    closeApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

    #Open Settings Application
    openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

    try:
        print("Verifying OpenRoaming Connected Wifi")
        time.sleep(20)
        report.step_start("Verifying Connected Wifi Name")  
        element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
        OpenRoamingWifiName = element.text
        element.click()
     
    except Exception as e:
        OpenRoamingWifiName = "None"
        print("Wifi Not Connected to OpenRoaming Profile: ") 
        request.config.cache.set(key="SelectingWifiFailed", value=str(e))
        assert False

    #try:
      #  report.step_start("Verify Wifi Connected Status")
     #   WifiXpath = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ OpenRoamingWifiName + "']"
     #   elementWifName = driver.find_element_by_xpath(WifiXpath)
    #    OpenRoamingWifiName = elementWifName.text
    #    print ("Connected to: " + OpenRoamingWifiName)
   #except NoSuchElementException:
      #  OpenRoamingWifiName = "None"
      #  reportFlag = False
      #  assert reportFlag


    #return OpenRoamingWifiName

def ForgetAllWifiConnection(request, setup_perfectoMobile, connData):
    print("\n-----------------------------")
    print("Forget All Wifi/AP Connection")
    print("-----------------------------")
    
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]

    report.step_start("Switching Driver Context")  
    print("Switching Context to Native")
    driver.switch_to.context('NATIVE_APP')
    contexts = driver.contexts
    #print(contexts)

    report.step_start("Forget Existing Wifi")   
    openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

    try:
        print("Verifying Connected Wifi Connection")
        report.step_start("Verifying Existing Connected Wifi Connection")  
        element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
        Wifi_AP_Name = element.text
        element.click()
        print ("Connected to: " + Wifi_AP_Name)
    except NoSuchElementException:
        Wifi_AP_Name = "None"
        print("Wifi Not Connected to anything") 

    if Wifi_AP_Name.__eq__("Not Connected"):
        print("Not Connected to any wifi") 

    else:
        report.step_start("Click on More Info on Wifi")
        WifiXpathMoreInfo = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ Wifi_AP_Name + "']/parent::*/XCUIElementTypeButton[@label='More Info']"
        elementMoreInfo = driver.find_element_by_xpath(WifiXpathMoreInfo)
        elementMoreInfo.click()

        print("Forget Wifi Network " + Wifi_AP_Name)
        report.step_start("Forget Wifi Network")
        WifiXpathForgetWifi = "//*[@label='Forget This Network']"
        elementforgetWifi = driver.find_element_by_xpath(WifiXpathForgetWifi)
        elementforgetWifi.click()

        report.step_start("Confirm Forget Wifi Network")
        WifiXpathForgetWifi = "//*[@label='Forget']"
        elementforgetWifi = driver.find_element_by_xpath(WifiXpathForgetWifi)
        elementforgetWifi.click()

def deleteOpenRoamingInstalledProfile(request, setup_perfectoMobile, connData):
    print("\n-----------------------------")
    print("Delete Open Roaming Profile")
    print("-----------------------------")
    
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]

    report.step_start("Switching Driver Context")  
    print("Switching Context to Native")
    driver.switch_to.context('NATIVE_APP')
    contexts = driver.contexts
    #print(contexts)

    report.step_start("Forget Existing Wifi")   
    openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

    try:
        print("Click General")
        report.step_start("Click General")  
        element = driver.find_element_by_xpath("//*[@value='General']")
        element.click()
    except NoSuchElementException:
        print("Exception General Menu Not found")
        assert False

    scrollDown(setup_perfectoMobile)

    try:
        print("Select Profile ")
        report.step_start("Select Profile")  
        element = driver.find_element_by_xpath("//*[@name='ManagedConfigurationList' and @label='Profile']")
        element.click()
    except NoSuchElementException:
        print("Exception Select Profile Button")
        assert False

    try:
        print("Click Configuration Profile ")
        report.step_start("Click Configuration Profile ")  
        element = driver.find_element_by_xpath("//XCUIElementTypeStaticText[@label='AmeriBand']")
        element.click()
    except NoSuchElementException:
        print("Exception Click Configuration Button")
        assert False

    try:
        print("Remove Profile")
        report.step_start("Remove Profile ")  
        element = driver.find_element_by_xpath("//*[@label='Remove Profile']")
        element.click()
    except NoSuchElementException:
        print("Exception Remove")
        assert False
      
    try:
        print("Click Remove Button")
        report.step_start("Click Remove Button")  
        element = driver.find_element_by_xpath("//*[@label='Remove']")
        element.click()
    except NoSuchElementException:
        print("Exception Remove Button")
        assert False

    try:
        print("Verify No Profile Installed Msg")
        report.step_start("Verify No Profile Installed Msg")  
        element = driver.find_element_by_xpath("//*[@label='No profiles are currently installed.']")
    except NoSuchElementException:
        print("Exception Verify No Profile Installed Msg")
        assert False