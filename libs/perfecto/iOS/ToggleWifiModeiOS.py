import time
import unittest
import warnings

#from perfecto import TestResultFactory
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import argparse
from BaseClassiOS import TestConf


class ReportingTests(TestConf):

    def test_navigation(self):
        warnings.simplefilter("ignore", ResourceWarning)
        try:
           # assert 'Perfecto' in self.driver.title
            print("-------------------------------------------")
             #REPORTIUM TEST START
            #self.reporting_client.step_start("BasicConnectionTest") 
            #DefaultGateWayAccessPoint = self.driver.find_element_by_xpath("//*[@label='Default Gateway IP']/parent::*/XCUIElementTypeButton").text
           # print("Device-DefaultGateWay-AP: " + "'"+ DefaultGateWayAccessPoint + "'")    
            #self.assertNotEqual(DefaultGateWayAccessPoint, "N/A", "Check Wifi Access Point")
            print("Verify Internet Connection..")
            self.reporting_client.step_start("Verify Internet Connection")     
            networkAccessPoint = self.driver.find_element_by_xpath("//*[@label='Network Connected']/parent::*/XCUIElementTypeButton").text
            print("Network-AccessPoint-Connected: " + "'"+ networkAccessPoint + "'")

            #Open Setting Application - Resets to Home
            print("Opening Settings App..")
            self.reporting_client.step_start("Opening Settings App")     
            params = {'identifier': 'com.apple.Preferences'}
            self.driver.execute_script('mobile:application:open', params)
            self.driver.execute_script('mobile:application:close', params)
            self.driver.execute_script('mobile:application:open', params)

            print("Verify Wifi Connection Name..")
            self.reporting_client.step_start("Verify Wifi Connection Name.")     
            element = self.driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
            Wifi_AP_Name = element.text
            print("Wifi_AP_ConnName: " + "'"+ Wifi_AP_Name + "'")

            #Verify if Ap is connected with Wifi
            self.reporting_client.step_start("Click Wifi Connection.")     
            print("Click Wifi Connection..")
            element.click()

            #Verifies if AP is connected to Wifi status
            print("Verify Wifi Connection Status..")
            self.reporting_client.step_start("Verify Wifi Connection Status")     
            WifiXpath = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ Wifi_AP_Name + "']"
            elementWifName = self.driver.find_element_by_xpath(WifiXpath)
            
            #Check AP Internet Error Msg 
            self.reporting_client.step_start("Checking Internet Connection Error")     
            print("Checking Internet Connection Error..")
           # self.driver.implicitly_wait(5)
            try:
                WifiInternetErrMsg = self.driver.find_element_by_xpath("//*[@label='No Internet Connection']").text
            except NoSuchElementException:
                print("Connected-Wifi-AP..Connection Successfull")
            
            #Close/Open App resets the settings app back to home page
            #self.driver.execute_script('mobile:application:close', params)
            #self.driver.execute_script('mobile:application:open', params)

            #Toggle Wifi Mode
            self.reporting_client.step_start("Toggle Wifi Mode")    
            print("Toggle Wifi Mode..")
            try:
                WifiMode = self.driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='1']")
                #Toggle Wifi Mode
                WifiMode.click()
                #Verify Radio Button Mode
                try:
                    WifiDissconnected = self.driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='0']")
                    #self.assertEqual(WifiDissconnected.text, "Airplane Mode", "Airplane Mode Not Triggerd")
                    print("Wifi Radio Button Disconnected Successfully")
                except NoSuchElementException:
                    print("Wifi Radio Button Not Disabled...") 
                
                #Set Airplane Mode Back
                WifiDissconnected.click()         
            except NoSuchElementException:
                print("Airplane Wifi Button not loaded...")

            #Verifies if AP is connected to Wifi status
            self.reporting_client.step_start("Verify Wifi Connection Status")    
            print("Verify Wifi Connection Status..")
            WifiXpath = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ Wifi_AP_Name + "']"
            elementWifName = self.driver.find_element_by_xpath(WifiXpath)
            
            #Check AP Internet Error Msg 
            print("Checking Internet Connection Error..")
            self.reporting_client.step_start("Checking Internet Connection Error")  
           # self.driver.implicitly_wait(5)
            try:
                WifiInternetErrMsg = self.driver.find_element_by_xpath("//*[@label='No Internet Connection']").text
            except NoSuchElementException:
                print("Connected-Wifi-AP..Connection Successfull")

            #Close Settings App
            self.reporting_client.step_start("Close Settings App")  
            print("Close Settings App")
            self.driver.execute_script('mobile:application:close', params)

        except NoSuchElementException as ex:
            self.currentResult = False
            #self.reporting_client.test_stop(TestResultFactory.create_failure("NoSuchElementException", ex))
            print (ex.message)
            self.currentResult = True
        #self.reporting_client.test_stop(Tes

if __name__ == '__main__':
   # parser = argparse.ArgumentParser(description="Perfecto Arguments")
        
    #parser.add_argument(
    #    "-c",
    #    "--cloud_name",
    #    metavar="cloud_name",
   #     help="Perfecto cloud name. (E.g. demo)",
    #)
   # parser.add_argument(
       #     "-s",
      #      "--security_token",
      #      metavar="security_token",
      #      help="Perfecto cloud name. (E.g. demo)",
      #  )

    #args = vars(parser.parse_args())

    #if not args["cloud_name"]:
       #     parser.print_help()
       #     parser.error(
        #       "cloud_name parameter is empty. Pass the argument -c followed by cloud_name"
        #    )
       #     exit

    #print(str(args["cloud_name"]))     

    unittest.main()
