import time

import unittest
import warnings
from selenium.webdriver.common.keys import Keys
#from perfecto import TestResultFactory
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import argparse

from urllib3.exceptions import HeaderParsingError
from BaseClassWebiOS import TestConf


class ReportingTests(TestConf):

    def test_navigation(self):
        try:
            print("-----------------AP TO MOBILE DEVICE--------------------------")
             #REPORTIUM TEST START
            #self.reporting_client.step_start("BasicConnectionTest") 

            #Search
            try:  
                self.reporting_client.step_start("Google Home Page")     
                self.driver.get('https://www.google.com') 
                lblSearch = "//*[@class='gLFyf']"
                elementFindTxt = self.driver.find_element_by_xpath(lblSearch)
                elementFindTxt.send_keys("Internet Speed Test")

                try:
                    elelSearch = self.driver.find_element_by_xpath("(//*[@class='sbic sb43'])[1]")  
                    elelSearch.click()
                except NoSuchElementException:
                    print("Enter Not Active...")

                self.reporting_client.step_start("Verify Run Button")           
                BtnRunSpeedTest = "//*[text()='RUN SPEED TEST']"
                self.driver.find_element_by_xpath(BtnRunSpeedTest).click()

                #Get upload/Download Speed
                try:
                    self.reporting_client.step_start("Get upload/Download Speed")   
                    time.sleep(60)
                    downloadMbps = self.driver.find_element_by_xpath("//*[@id='knowledge-verticals-internetspeedtest__download']/P[@class='spiqle']")
                    downloadSpeed = downloadMbps.text
                    print("Download: " + downloadSpeed + " Mbps")

                    UploadMbps = self.driver.find_element_by_xpath("//*[@id='knowledge-verticals-internetspeedtest__upload']/P[@class='spiqle']")
                    uploadSpeed = UploadMbps.text
                    print("Upload: " + uploadSpeed + " Mbps")
                    
                    print("Access Point Verification Completed Successfully")

                except NoSuchElementException:
                    print("Access Point Verification NOT Completed, checking Connection....")
                    
            except Exception as e:
                print (e.message)
            
            #refresh page  //*[@label="reload"]
            #TestAgain: //*[text()="TEST AGAIN"]

         

           # time.sleep(20)      


            #Close Settings App
           # self.driver.execute_script('mobile:application:close', params2)
        
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

    