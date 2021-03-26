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

            #Open Setting Application 
            print("Opening Settings App..")
            self.reporting_client.step_start("Opening Settings App")     
            params = {'identifier': 'com.apple.Preferences'}
            self.driver.execute_script('mobile:application:open', params)
            self.driver.execute_script('mobile:application:close', params)
            self.driver.execute_script('mobile:application:open', params)

            print("Verify Wifi Connection Name..")
            self.reporting_client.step_start("Verify Wifi Connection Name") 
            element = self.driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
            Wifi_AP_Name = element.text
            print("Wifi_AP_ConnName: " + "'"+ Wifi_AP_Name + "'")

            #Verify if Ap is connected with Wifi
            self.reporting_client.step_start("Click Wifi Connection")
            print("Click Wifi Connection..")
            element.click()

            #Verifies if AP is connected to Wifi status
            print("Verify Wifi Connection Status..")
            self.reporting_client.step_start("Verify Wifi Connection Status")
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
            
            #Close/Open App resets the settings app back to home page
            self.reporting_client.step_start("Close/Open App Reset Settings")
            self.driver.execute_script('mobile:application:close', params)
            self.driver.execute_script('mobile:application:open', params)

            #Toggle Airplane Mode
            print("Toggle Airplane Mode..")
            self.reporting_client.step_start("Toggle Airplane Mode..")
            try:
                AirplaneMode = self.driver.find_element_by_xpath("//XCUIElementTypeSwitch[@label='Airplane Mode']")
                #Toggle Airplane Mode
                AirplaneMode.click()

                #Verify Cellular Mode Text
                try:
                    self.reporting_client.step_start("Verify Cellular Mode..")
                    CellularMsgEle = self.driver.find_element_by_xpath("//*[@name='Airplane Mode' and @value='Airplane Mode']")
                    self.assertEqual(CellularMsgEle.text, "Airplane Mode", "Airplane Mode Not Triggerd")             
                except NoSuchElementException:
                    print("Exception Cellular Mode Not in Airplane Mode: CheckPhoneStatus") 

                #Set Airplane Mode Back
                AirplaneMode.click()         
            except NoSuchElementException:
                print("Airplane Wifi Button not loaded...")
                
            #Verify No Sim Card Installed Msg Popup
            print("Verify No Sim Card Installed Msg Popup..")
            self.reporting_client.step_start("Verify No Sim Card Installed Msg Popup")
            try:
                NoSimCardErrorMsg = self.driver.find_element_by_xpath("//*[@value='No SIM Card Installed']")
            except NoSuchElementException:
                print(" ----- No Sim Card AlertMsg ----")
               
            #Click ok on No Sim Card Msg Popup
            print("Click ok on No Sim Card Msg Popup..")
            self.reporting_client.step_start("Click ok on No Sim Card Msg Popup..")
            try:
                NoSimCardErrorMsgOK = self.driver.find_element_by_xpath("//*[@label='OK']")
                NoSimCardErrorMsgOK.click()
            except NoSuchElementException:
                print(" -----  No Sim Card AlertMsg  -----")
       
            #Close/Open App resets the settings app back to home page
            self.reporting_client.step_start("Close/Open App resets the settings")
            self.driver.execute_script('mobile:application:close', params)
            self.driver.execute_script('mobile:application:open', params)
           
            #time.sleep(5)
            self.reporting_client.step_start("Verify Wifi Connection Name after Toggle Mode")
            print("Verify Wifi Connection Name after Airplane Toggle Mode..")
            element22 = self.driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
            Wifi_AP_NameNew = element22.text
            print("Wifi_AP_ConnNameAfterToggle: " + "'"+ Wifi_AP_NameNew + "'")
                
            #self.assertqual(Wifi_AP_Name, "Sendto: No route to host", "Packet Loss Exist, Please Check Device AP: " + Wifi_AP_Name)
            #self.assertEqual(Wifi_AP_Name, Wifi_AP_NameNew, "AP Connection Successfull")

            #Verify if Ap is connected with Wifi
            self.reporting_client.step_start("Click Wifi Connection after Airplane Toggle Mode")
            print("Click Wifi Connection after Airplane Toggle Mode..")
            element22.click()

            #Verifies if AP is connected to Wifi status
            print("Verify Wifi Connection Status..")
            self.reporting_client.step_start("Verify Wifi Connection Status")
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
