import os
import sys
import unittest
import warnings
import urllib3
import argparse
#from perfecto import (PerfectoExecutionContext, PerfectoReportiumClient,
  #                    TestContext, TestResultFactory)
#from appium import webdriver
from selenium import webdriver

class TestConf(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        #Suppress InsecureRequestWarning: Unverified HTTPS request is being made 
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        #Perfecto
        self.securityToken = 'eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIyODhhNDIyNS1jOTE1LTQwZDctOTc2YS04MDhiMWE3YTFmODYifQ.eyJqdGkiOiJkMmMwNzU5YS0yNWIyLTQ4ZmItYmViNC0wNzAxMWI4MDVmODMiLCJleHAiOjAsIm5iZiI6MCwiaWF0IjoxNjE0MjI5MTUxLCJpc3MiOiJodHRwczovL2F1dGgucGVyZmVjdG9tb2JpbGUuY29tL2F1dGgvcmVhbG1zL3BzLXBlcmZlY3RvbW9iaWxlLWNvbSIsImF1ZCI6Imh0dHBzOi8vYXV0aC5wZXJmZWN0b21vYmlsZS5jb20vYXV0aC9yZWFsbXMvcHMtcGVyZmVjdG9tb2JpbGUtY29tIiwic3ViIjoiMzkzYjMxYTQtNDJiZS00NmIxLTg5MGUtYmRlNzY3ZWEzYjQ2IiwidHlwIjoiT2ZmbGluZSIsImF6cCI6Im9mZmxpbmUtdG9rZW4tZ2VuZXJhdG9yIiwibm9uY2UiOiJmOTQ4MjI2Yi04YWQwLTQ1YTAtYmMzNC04NzQ5MzZjNDQ0NDgiLCJhdXRoX3RpbWUiOjAsInNlc3Npb25fc3RhdGUiOiIzMzVhNGM2My01ODE4LTQ0NmMtOTA2NC1iZWZiY2JkZWQ2N2MiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZXBvcnRpdW0iOnsicm9sZXMiOlsiYWRtaW5pc3RyYXRvciIsInJlcG9ydF9hZG1pbiJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgb2ZmbGluZV9hY2Nlc3MifQ.BKnSYDAczir7suvt_5T44pJ5IaZLzsT_JwVAziR4pKg'
        self.host = 'ps.perfectomobile.com'

        #self.securityToken = 'eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJqdGkiOiJjYjRjYjQzYi05Y2FiLTQxNzQtOTYxYi04MDEwNTZkNDM2MzgiLCJleHAiOjAsIm5iZiI6MCwiaWF0IjoxNjExNTk0NzcxLCJpc3MiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRoMi5wZXJmZWN0b21vYmlsZS5jb20vYXV0aC9yZWFsbXMvdGlwLXBlcmZlY3RvbW9iaWxlLWNvbSIsInN1YiI6IjdiNTMwYWUwLTg4MTgtNDdiOS04M2YzLTdmYTBmYjBkZGI0ZSIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJvZmZsaW5lLXRva2VuLWdlbmVyYXRvciIsIm5vbmNlIjoiZTRmOTY4NjYtZTE3NS00YzM2LWEyODMtZTQwMmI3M2U5NzhlIiwiYXV0aF90aW1lIjowLCJzZXNzaW9uX3N0YXRlIjoiYWNkNTQ3MTctNzJhZC00MGU3LWI0ZDctZjlkMTAyNDRkNWZlIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZXBvcnRpdW0iOnsicm9sZXMiOlsiYWRtaW5pc3RyYXRvciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.SOL-wlZiQ4BoLLfaeIW8QoxJ6xzrgxBjwSiSzkLBPYw'
        #self.host = 'tip.perfectomobile.com'
       
        self.driver = None
     #   self.reporting_client = None
  
        super(TestConf, self).__init__(*args, **kwargs)
        
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        capabilities = {
            'platformName': 'iOS',
            #'manufacturer': 'Apple',
            'browserName': 'safari',
            'securityToken' : 'eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIyODhhNDIyNS1jOTE1LTQwZDctOTc2YS04MDhiMWE3YTFmODYifQ.eyJqdGkiOiJkMmMwNzU5YS0yNWIyLTQ4ZmItYmViNC0wNzAxMWI4MDVmODMiLCJleHAiOjAsIm5iZiI6MCwiaWF0IjoxNjE0MjI5MTUxLCJpc3MiOiJodHRwczovL2F1dGgucGVyZmVjdG9tb2JpbGUuY29tL2F1dGgvcmVhbG1zL3BzLXBlcmZlY3RvbW9iaWxlLWNvbSIsImF1ZCI6Imh0dHBzOi8vYXV0aC5wZXJmZWN0b21vYmlsZS5jb20vYXV0aC9yZWFsbXMvcHMtcGVyZmVjdG9tb2JpbGUtY29tIiwic3ViIjoiMzkzYjMxYTQtNDJiZS00NmIxLTg5MGUtYmRlNzY3ZWEzYjQ2IiwidHlwIjoiT2ZmbGluZSIsImF6cCI6Im9mZmxpbmUtdG9rZW4tZ2VuZXJhdG9yIiwibm9uY2UiOiJmOTQ4MjI2Yi04YWQwLTQ1YTAtYmMzNC04NzQ5MzZjNDQ0NDgiLCJhdXRoX3RpbWUiOjAsInNlc3Npb25fc3RhdGUiOiIzMzVhNGM2My01ODE4LTQ0NmMtOTA2NC1iZWZiY2JkZWQ2N2MiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZXBvcnRpdW0iOnsicm9sZXMiOlsiYWRtaW5pc3RyYXRvciIsInJlcG9ydF9hZG1pbiJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgb2ZmbGluZV9hY2Nlc3MifQ.BKnSYDAczir7suvt_5T44pJ5IaZLzsT_JwVAziR4pKg',
            #'bundleId': 'com.apple.mobilesafari',
            #'enableAppiumBehavior': True, # Enable new architecture of Appium
          #  'autoLaunch': True, # To work with hybrid applications, install the iOS/Android application as instrumented.
            'model': 'iPhone.*'
        }
        
        #self.driver = webdriver.Remote('https://tip.perfectomobile.com/nexperience/perfectomobile/wd/hub', capabilities)
        
        self.driver = webdriver.Remote('https://ps.perfectomobile.com/nexperience/perfectomobile/wd/hub', capabilities)
        self.driver.implicitly_wait(20)
      #  self.create_reporting_client()
    #    self.reporting_client.test_start(self.id(), TestContext('Python', 'unittest'))
        
    def run(self, result=None):
        self.currentResult = result  # remember result for use in tearDown
        unittest.TestCase.run(self, result)  # call superclass run method

    def tearDown(self):
        warnings.simplefilter("ignore", ResourceWarning)
        try:
            print("-------------------------------------------")
            print(" -- Tear Down --")       

            #if self.currentResult.wasSuccessful():
           #     self.reporting_client.test_stop(TestResultFactory.create_success())
           # else:
                # self.reporting_client.test_stop(TestResultFactory.create_failure('failure 4096' * 1000))
                
            #    self.reporting_client.test_stop(TestResultFactory.create_failure(self.currentResult.errors,
                         #                                                        self.currentResult.failures))
            # Print report's url
        #print('Report-Url: ' + self.reporting_client.report_url() + '\n')
        except Exception as e:
            print (e.message)

        try:
            self.driver.close()
        except Exception as e:
            print(" -- Exception Not Able To close --")    
            print (e.message)
        finally:
            try:
                self.driver.quit()
            except Exception as e:
                print(" -- Exception Not Able To Quit --")    
                print (e.message)

        

  #  def create_reporting_client(self):
  #      perfecto_execution_context = PerfectoExecutionContext(self.driver, ['execution tag1', 'execution tag2'])
  #      self.reporting_client = PerfectoReportiumClient(perfecto_execution_context)
