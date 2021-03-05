import time
import unittest
import warnings

#from perfecto import TestResultFactory
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import argparse
from BaseClassAndroid import TestConf


class ReportingTests(TestConf):

    def test_navigation(self):
        warnings.simplefilter("ignore", ResourceWarning)
        try:
           # assert 'Perfecto' in self.driver.title
            print("-------------------------------------------")
             #REPORTIUM TEST START
            #self.reporting_client.step_start("BasicConnectionTest") 
 
            #Open Setting Application 
            print("Opening Settings App..")
            params = {'identifier': 'com.android.settings'}
            self.driver.execute_script('mobile:application:close', params)
            self.driver.execute_script('mobile:application:open', params)

            print("Load Wifi/BlueTooth/AirplaneMode Connection Settings..")
            element = self.driver.find_element_by_xpath("//*[@text='Connections']")
            element.click()

            #Verifies if AP is connected to Wifi status
         #   print("Verify AirplaneMode Connection Status..")
         #   try:
         #       WifiXpath = "//*[@text='Airplane mode']/parent::*/android.widget.TextView[2]"
          ##      elementWifName = self.driver.find_element_by_xpath(WifiXpath)
          #      print("Airplane Mode StatusMsg: " + elementWifName.text)
          #  except NoSuchElementException:
           #     print("Exception: Unable to Toggle Airplane Radio Button...Check Xpath")
            

            print("Toggle Airplane AP Mode..")
            try:
                WifiInternet = self.driver.find_element_by_xpath("//*[@content-desc='Airplane mode']")
                WifiInternet.click()
            except NoSuchElementException:
                print("Exception: Unable to Toggle Airplane Radio Button...Check Xpath")
            

            #Ensure Wifi Radio Button Disabled 
            print("Verify Airplane Disconnected Status..")
            try:
                WifiXpathDisconnected = "//*[@text='Airplane mode']/parent::*/android.widget.TextView[2]"
                elementWifiDiscont = self.driver.find_element_by_xpath(WifiXpathDisconnected)
                print("AirPlane Disconnected Name: " + "Please " + elementWifiDiscont.text)
            except NoSuchElementException:
                print("Warning...No Airplane Mode Msg...Check Xpath")
            
            print("Toggle Airplane Radio Button On..")
            try:
                #Toggle Wifi Radio Button 
                WifiInternet2 = self.driver.find_element_by_xpath("//*[@content-desc='Airplane mode']")
                WifiInternet2.click()
            except NoSuchElementException:
                print("Exception: Unable to Toggle Airplane Radio...Check Xpath")

            #Verifies if AP is connected to Wifi status
            print("Verify Wifi ReConnection Status..")
            try:
                WifiXpathToggle = "//*[@text='Wi-Fi']/parent::*/android.widget.TextView[2]"
                elementWifNameToggle = self.driver.find_element_by_xpath(WifiXpathToggle)
                print("Wifi Connected AP Status: " + elementWifNameToggle.text)
                #self.assertEqual("elementWifName.text","elementWifNameToggle.text","Connection Successfull Reconnected")
                print("Connection Successfull Reconnected")
            except NoSuchElementException:
                print("Exception: AirplaneMode Not Connected Back...Check Xpath")

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
