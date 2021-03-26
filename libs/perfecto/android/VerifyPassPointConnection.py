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
            #DefaultGateWayAccessPoint = self.driver.find_element_by_xpath("//*[@label='Default Gateway IP']/parent::*/XCUIElementTypeButton").text
           # print("Device-DefaultGateWay-AP: " + "'"+ DefaultGateWayAccessPoint + "'")    
            #self.assertNotEqual(DefaultGateWayAccessPoint, "N/A", "Check Wifi Access Point")
           # print("Verify Internet Connection..")
         #   networkAccessPoint = self.driver.find_element_by_xpath("//*[@label='Network Connected']/parent::*/XCUIElementTypeButton").text
       #     print("Network-AccessPoint-Connected: " + "'"+ networkAccessPoint + "'")

            #Open Setting Application 
          #  print("Opening Settings App..")
          #  params = {'identifier': 'com.android.settings'}
            #self.driver.execute_script('mobile:application:open', params)
          #  self.driver.execute_script('mobile:application:close', params)
          #  self.driver.execute_script('mobile:application:open', params)
            
           # params = {'property': 'All'}
           # deviceProperty = self.driver.execute_script('mobile:handset:info', params)
           # print("ModelName: " + deviceProperty)  
            self.reporting_client.step_start("Pass Point Verification")
            params = {'property': 'deviceId'}
            deviceID = self.driver.execute_script('mobile:handset:info', params)
            params = {'property': 'model'}
            deviceModel = self.driver.execute_script('mobile:handset:info', params)
            print("ModelName: " + deviceModel + "  DeviceId: " + deviceID)  

            #modelName = self.driver.desired_capabilities['model'] 
            #deviceID = self.driver.desired_capabilities['deviceId'] 
            #  
           # print("DeviceID: " + deviceID)    

            #Close Settings App
           # print("Close Settings App")
            #self.driver.execute_script('mobile:application:close', params)

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
