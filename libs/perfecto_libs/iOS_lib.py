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
    print("Scroll Down")
    setup_perfectoMobile[1].step_start("Scroll Down")  
    params2 = {}
    params2["start"] = "50%,90%"
    params2["end"] = "50%,20%"
    params2["duration"] = "4"
    time.sleep(5)
    setup_perfectoMobile[0].execute_script('mobile:touch:swipe', params2)
    time.sleep(5)
  
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

def set_APconnMobileDevice_iOS(request, WifiNameSSID, WifiPass, setup_perfectoMobile, connData):
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
    #contexts = driver.contexts
    #print(contexts)
    driver.switch_to.context('NATIVE_APP')
    #driver.switch_to.context(contexts[0])

    print(WifiNameSSID)
    report.step_start("Set Wifi Network to " + WifiNameSSID)  
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

    if Wifi_AP_Name.__eq__(WifiNameSSID):
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
        print("Selecting Wifi: " + WifiNameSSID)   
        #consoleOutput+=str(WifiName)+ "\n"
        report.step_start("Selecting Wifi...: " + WifiNameSSID)
        element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
        element.click()
        try:
            wifiXpath2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='"+ WifiNameSSID + "']")))
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
            print("Enter Password Page Not Loaded")
        
        try:
            joinBTN = driver.find_element_by_xpath("//*[@label='Join']")
            joinBTN.click()
        except Exception as e:
            print("Join Button Not Enabled...Password may not be needed")

        try:
            WifiInternetErrMsg2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='No Internet Connection']")))
             #= driver.find_element_by_xpath("//*[@label='No Internet Connection']").text
            reportFlag = False
        except Exception as e:
            reportFlag = True
            print("No Wifi-AP Error Internet Error: " + WifiNameSSID)
            #Need to add Wait for Selected Wifi Xpath
            time.sleep(3)
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
        print("Get Connected Wifi Name")
        report.step_start("Get Connected Wifi Name")  
        element = WebDriverWait(driver, 45).until(EC.presence_of_element_located((MobileBy.XPATH, "//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")))
        #element = driver.find_element_by_xpath("")
        element.click()
        
    except Exception as e:
        print("SSID Not Connected Within allocated Time: " + WifiName)
        report.step_start("SSID Not Connected: " + WifiName)  
        request.config.cache.set(key="SelectingWifiFailed", value=str(e))
        reportFlag = False
        assert reportFlag  

        #print("Verifying if SSID Wifi Shows up")
        #report.step_start("Verifying if SSID Wifi Shows up")  
        #wifiXpath2 = WebDriverWait(driver, 45).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='"+ WifiName + "']")))
        #print("SSID is Present: " + WifiName)
        #report.step_start("SSID is Present: " + WifiName)  

    try: 
        print("Waiting for Auto Connection to: " + WifiName)
        report.step_start("Waiting for Auto Connection to: " + WifiName)   
        selectedWifiNetwork = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ WifiName + "']/parent::*/XCUIElementTypeButton[@label='More Info']"
        passPointWifi = WebDriverWait(driver, 30).until(EC.presence_of_element_located((MobileBy.XPATH, selectedWifiNetwork)))
    except Exception as e:
        #Toggle Wifi Mode
        Toggle_WifiMode_iOS(request, setup_perfectoMobile, connData)  
        time.sleep(15)

        try:
            print("Waiting for Auto Connection After Toggling Wifi: " + WifiName)
            selectedWifiNetwork2 = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ WifiName + "']/parent::*/XCUIElementTypeButton[@label='More Info']"
            passPointWifi = WebDriverWait(driver, 30).until(EC.presence_of_element_located((MobileBy.XPATH, selectedWifiNetwork2)))
        except Exception as e:
            print("SSID Not Connected Within allocated Time: " + WifiName)
            report.step_start("SSID Not Connected: " + WifiName)  
            request.config.cache.set(key="SelectingWifiFailed", value=str(e))
            reportFlag = False
            assert reportFlag

    return True

def ForgetWifiConnection(request, setup_perfectoMobile, wifiName, connData):
    print("\n-----------------------------")
    print("Forget Wifi/AP Connection")
    print("-----------------------------")
    
    report = setup_perfectoMobile[1]    
    driver = setup_perfectoMobile[0]

    report.step_start("Switching Driver Context")  
    print("Switching Context to Native")
    driver.switch_to.context('NATIVE_APP')
    #contexts = driver.contexts
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

    report.step_start("Toggle Wifi Mode")    
    print("Toggle Wifi Mode..")
    try:
        print("Disable Wifi Radio Btn")
        report.step_start("Disable Wifi Radio Btn")    
        WifiMode = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='1']")
        #Toggle Wifi Mode
        WifiMode.click()
        time.sleep(5)
        #Verify Radio Button Mode
        try:
            print("Enable Wifi Radio Btn")
            report.step_start("Enable Wifi Radio Btn")  
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

def downloadInstallOpenRoamingProfile(request, profileDownloadURL, setup_perfectoMobile, get_APToMobileDevice_data):
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

    print("Switching Context to Webview")
    driver.switch_to.context('WEBVIEW_1')
    print("Launching Google to Reset Browser")
    report.step_start("Launching Google to Reset Browser") 
    driver.get("https://www.google.com") 

    print("Switching Context to Native")
    report.step_start("Switching Driver Context Native")  
    driver.switch_to.context('NATIVE_APP')

    closeApp(connData["bundleId-iOS-Safari"], setup_perfectoMobile)

    #Open Settings Application
    #openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

     

   # try:
   #     print("Verifying OpenRoaming Connected Wifi")
   #     time.sleep(3)
    #    report.step_start("Verifying Connected Wifi Name")  
   #     element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
  #      OpenRoamingWifiName = element.text
  #      element.click()
     
 #   except Exception as e:
  #      OpenRoamingWifiName = "None"
   #     print("Wifi Not Connected to OpenRoaming Profile: ") 
   #     request.config.cache.set(key="SelectingWifiFailed", value=str(e))
    #    assert False



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

def ForgetProfileWifiConnection(request, setup_perfectoMobile, installedProfileSSID, connData):
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
        #Also have to check with Connected Status xpath
        print("Verifying Connected Wifi Connection")
        report.step_start("Verifying Existing Connected Wifi Connection")  
        element22 = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
        element22.click()

        #WifiXpath2= "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[2]"
        WifiXpath2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[2]")))
        elementMoreInfo = driver.find_element_by_xpath(WifiXpath2)
        Wifi_AP_Name = elementMoreInfo.text
        print ("Connected to: " + Wifi_AP_Name)

    except NoSuchElementException and TimeoutException:
        Wifi_AP_Name = "None"
        print("Wifi Not Connected to anything") 

    if Wifi_AP_Name.__eq__("Not Connected"):
        print("Not Connected to any wifi") 
        #deleteOpenRoamingInstalledProfile(request, installedProfileSSID, setup_perfectoMobile, connData)
    elif Wifi_AP_Name.__eq__("None"):
        #deleteOpenRoamingInstalledProfile(request, installedProfileSSID, setup_perfectoMobile, connData)
        print("Not Connected to any wifi Network/None") 
    elif Wifi_AP_Name.__eq__(installedProfileSSID):
       deleteOpenRoamingInstalledProfile(request, installedProfileSSID, setup_perfectoMobile, connData)
    else:
        try:
            #element22.click()
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

        except NoSuchElementException:
            
            print("Exception General Menu Not found")
            assert False

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
        print("Verify if any Profile Installed ")
        try:
            print("Select Profile ")
            report.step_start("Select Profile")  
            elementProfile = driver.find_element_by_xpath("//*[@name='ManagedConfigurationList' and @label='Profile']")
            elementProfile.click()
        except NoSuchElementException:
            #Verify Multi Profiles
            print("Multiple Profiles Maybe Installed, Checking Profiles")
            try:
                elementProfiles = driver.find_element_by_xpath("//*[@name='ManagedConfigurationList' and @label='Profiles']")
                elementProfiles.click()
                
                print("Exception Select Profile Button")
            except NoSuchElementException:
                print("No Profile Installed")

        try:
            print("Click Configuration Profile ")
            report.step_start("Click Configuration Profile ")  
            element = driver.find_element_by_xpath("//XCUIElementTypeStaticText[@label='" + profileName + "']")
            element.click()
        except NoSuchElementException:
            print("Exception Click AmeriBand Profile Btn")
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
        except Exception as e:
            print("Exception Remove Button")
            assert False

    except Exception:
        print("Exception There may be No Profiles Installed")
        report.step_start("Exception There may be No Profiles Installed")  

    closeApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)