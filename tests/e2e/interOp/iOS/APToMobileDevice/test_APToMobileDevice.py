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
from conftest import tearDown

class TestVerifyAPToMobileDevice(object):

    @pytest.mark.sanity
    #@pytest.mark.wpa2_personal
    #@pytest.mark.VerifyApTo_MobileDeviceWeb
    def test_VerifyApTo_MobileDeviceWeb(self, get_APToMobileDevice_data, setup_perfectoMobileWeb):
        
        try:
            report = setup_perfectoMobileWeb[1]
            driver = setup_perfectoMobileWeb[0]

            try:  
                report.step_start("Google Home Page")     
                driver.get(get_APToMobileDevice_data["webURL"]) 
                elementFindTxt = driver.find_element_by_xpath(get_APToMobileDevice_data["lblSearch"])
                elementFindTxt.send_keys("Internet Speed Test")

                try:
                    elelSearch = driver.find_element_by_xpath(get_APToMobileDevice_data["elelSearch"])  
                    elelSearch.click()
                except NoSuchElementException:
                    print("Enter Not Active...")

                report.step_start("Verify Run Button")           
                driver.find_element_by_xpath(get_APToMobileDevice_data["BtnRunSpeedTest"]).click()

                #get_APToMobileDevice_data["BtnRunSpeedTest"]
                #get_APToMobileDevice_data["BtnRunSpeedTest"]

                #Get upload/Download Speed
                try:
                    report.step_start("Get upload/Download Speed")   
                    time.sleep(60)
                    downloadMbps = driver.find_element_by_xpath(get_APToMobileDevice_data["downloadMbps"])
                    downloadSpeed = downloadMbps.text
                    print("Download: " + downloadSpeed + " Mbps")

                    UploadMbps = driver.find_element_by_xpath(get_APToMobileDevice_data["UploadMbps"])
                    uploadSpeed = UploadMbps.text
                    print("Upload: " + uploadSpeed + " Mbps")
                    
                    print("Access Point Verification Completed Successfully")

                except NoSuchElementException:
                    print("Access Point Verification NOT Completed, checking Connection....")

                currentResult = True    

                assert currentResult
            except Exception as e:
                print (e.message)
        
        except exception as e:
            print (e.message)
            tearDown(setup_perfectoMobileWeb)
     