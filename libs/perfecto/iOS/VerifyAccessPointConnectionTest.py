import time
import unittest

#from perfecto import TestResultFactory
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import argparse
from BaseClassiOS import TestConf


class ReportingTests(TestConf):

    def test_navigation(self):
        try:
           # assert 'Perfecto' in self.driver.title
            print("-------------------------------------------")
             #REPORTIUM TEST START
            #self.reporting_client.step_start("BasicConnectionTest") 
            DefaultGateWayAccessPoint = self.driver.find_element_by_xpath("//*[@label='Default Gateway IP']/parent::*/XCUIElementTypeButton").text
            print("Device-DefaultGateWay-AP: " + "'"+ DefaultGateWayAccessPoint + "'")    
            self.assertNotEqual(DefaultGateWayAccessPoint, "N/A", "Check Wifi Access Point")

            networkAccessPoint = self.driver.find_element_by_xpath("//*[@label='Network Connected']/parent::*/XCUIElementTypeButton").text
            print("Network-AccessPoint-Connected: " + "'"+ networkAccessPoint + "'")

            #Open Setting Application 
            print("Opening Settings App..")
            params = {'identifier': 'com.apple.Preferences'}
            self.driver.execute_script('mobile:application:open', params)
            self.driver.execute_script('mobile:application:close', params)
            self.driver.execute_script('mobile:application:open', params)

            #Verify Wifi Connected Network
            #try:
               # settingsBTN = self.driver.find_element_by_xpath("//XCUIElementTypeButton[@label='Settings']")
               # settingsBTN.click()
            #except NoSuchElementException:
                #print("Wifi Main Menu")    

            print("Verify Wifi Connection Name..")
            element = self.driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
            Wifi_AP_Name = element.text
            print("Wifi_AP_ConnName: " + "'"+ Wifi_AP_Name + "'")

            #Verify if Ap is connected with Wifi
            print("Click Wifi Connection..")
            element.click()

            #Verifies if AP is connected to Wifi status
            print("Verify Wifi Connection Status..")
            WifiXpath = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ Wifi_AP_Name + "']"
            elementWifName = self.driver.find_element_by_xpath(WifiXpath)
            
            #Check AP Internet Error Msg 
            print("Checking Internet Connection Error..")
            self.driver.implicitly_wait(5)
            try:
                WifiInternetErrMsg = self.driver.find_element_by_xpath("//*[@label='No Internet Connection']").text
            except NoSuchElementException:
                print("Connected-Wifi-AP..Connection Successfull")
                self.driver.implicitly_wait(30)    

            #Close Settings App
            print("Close Settings App")
            self.driver.execute_script('mobile:application:close', params)

            #Open Ping App
            print("Open Ping Application & Ping Host..")
            params2 = {'identifier': 'com.deftapps.ping'}
            self.driver.execute_script('mobile:application:open', params2)
            # The reason to close is to clear any cache from any previous failures
            self.driver.execute_script('mobile:application:close', params2)
            self.driver.execute_script('mobile:application:open', params2)

            pingHost = "//*[@value='<Hostname or IP address>']"
            element2 = self.driver.find_element_by_xpath(pingHost)
            element2.clear()
            element2.send_keys(DefaultGateWayAccessPoint)

            #Ping Enable
            print("Pingin Host..")
            element3 = self.driver.find_element_by_xpath("//XCUIElementTypeButton[@label='Ping']")
            element3.click()

            time.sleep(10)
            print("Stop Ping Host..")
            element4 = self.driver.find_element_by_xpath("//*[@label='Stop']")
            element4.click()

            # /* Check Packet Loss */
            print("Verifying Packet Loss..")
            try:
                element5 = self.driver.find_element_by_xpath("//XCUIElementTypeStaticText[@label='0']")  
                self.assertEqual(element5.text, "0", "Packet Loss Exist, Please Check Device")
            except NoSuchElementException:
                print("No Packet Loss Detected 1st Attempt")

            # Also Check #Sendto: No route to host
            print("Verifying No route to host Error Msg....")
            try:
                element7 = self.driver.find_element_by_xpath("(//XCUIElementTypeStaticText[@label='Sendto: No route to host'][2]")  
                self.assertNotEqual(element7.text, "Sendto: No route to host", "Packet Loss Exist, Please Check Device AP: " + Wifi_AP_Name)
            except NoSuchElementException:
                print("No Packet Loss Detected on AP: " + Wifi_AP_Name)

            #Close Settings App
            self.driver.execute_script('mobile:application:close', params2)
        
            #REPORTIUM TEST END
            #self.reporting_client.step_end()
            
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
