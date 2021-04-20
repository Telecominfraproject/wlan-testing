import os
import sys
import unittest
from unittest.loader import getTestCaseNames
import warnings
from perfecto.model.model import Job, Project
import urllib3
import argparse
from perfecto import (PerfectoExecutionContext, PerfectoReportiumClient,TestContext, TestResultFactory)
from appium import webdriver
#rom selenium import webdriver
import pytest

class TestConf(unittest.TestCase):
    projectname = 'TIP Project'
    projectversion = '1.0'
    jobname = 'Tip-CI-Regression'
    jobnumber = 1
    tags = 'TestTag'
    
    #testCaseName = 'ToggleWifiModeAndroid'

    def __init__(self, *args, **kwargs):
        warnings.simplefilter("ignore", ResourceWarning)
        #Suppress InsecureRequestWarning: Unverified HTTPS request is being made 
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        self.securityToken = 'eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJqdGkiOiJjYjRjYjQzYi05Y2FiLTQxNzQtOTYxYi04MDEwNTZkNDM2MzgiLCJleHAiOjAsIm5iZiI6MCwiaWF0IjoxNjExNTk0NzcxLCJpc3MiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRoMi5wZXJmZWN0b21vYmlsZS5jb20vYXV0aC9yZWFsbXMvdGlwLXBlcmZlY3RvbW9iaWxlLWNvbSIsInN1YiI6IjdiNTMwYWUwLTg4MTgtNDdiOS04M2YzLTdmYTBmYjBkZGI0ZSIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJvZmZsaW5lLXRva2VuLWdlbmVyYXRvciIsIm5vbmNlIjoiZTRmOTY4NjYtZTE3NS00YzM2LWEyODMtZTQwMmI3M2U5NzhlIiwiYXV0aF90aW1lIjowLCJzZXNzaW9uX3N0YXRlIjoiYWNkNTQ3MTctNzJhZC00MGU3LWI0ZDctZjlkMTAyNDRkNWZlIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZXBvcnRpdW0iOnsicm9sZXMiOlsiYWRtaW5pc3RyYXRvciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.SOL-wlZiQ4BoLLfaeIW8QoxJ6xzrgxBjwSiSzkLBPYw'
        self.host = 'tip.perfectomobile.com'
        self.driver = None
        self.reporting_client = None
        self.running = False
        self.suitesetup = False
        self.setupclient = None
        self.tags = ''
        self.testCaseName = 'ToggleWifiModeAndroid'
        super(TestConf, self).__init__(*args, **kwargs)


    def init_listener(self, projectname=None, projectversion=None, jobname=None, jobnumber=None):
        """
        This key word helps to initialize the listener with proper project info
        :param projectname: current project name
        :param projectversion: current project version
        :param jobname: the CI job name
        :param jobnumber: the CI job number
        :return:
        """
        if projectname != None:
            self.projectname = projectname
        if projectversion != None:
            self.projectversion = projectversion
        if jobname != None:
            self.jobname = jobname
        if jobnumber != None:
            self.jobnumber = int(float(jobnumber))

   # def suitesetup_result(self):
       # if self.suitesetup:
       #     if self.bi.get_variable_value('${TEST STATUS}') == 'FAIL':
        #        self.setupclient.test_stop(
       ##             TestResultFactory.create_failure(self.bi.get_variable_value('${TEST MESSAGE}')))
        #    else:
        #        self.setupclient.test_stop(TestResultFactory.create_success())
       #     self.suitesetup = False

    def setUp(self):

        warnings.simplefilter("ignore", ResourceWarning)
        capabilities = {
            'platformName': 'Android',
            'appPackage': 'com.android.settings',
            'securityToken' : "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJqdGkiOiJjYjRjYjQzYi05Y2FiLTQxNzQtOTYxYi04MDEwNTZkNDM2MzgiLCJleHAiOjAsIm5iZiI6MCwiaWF0IjoxNjExNTk0NzcxLCJpc3MiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRoMi5wZXJmZWN0b21vYmlsZS5jb20vYXV0aC9yZWFsbXMvdGlwLXBlcmZlY3RvbW9iaWxlLWNvbSIsInN1YiI6IjdiNTMwYWUwLTg4MTgtNDdiOS04M2YzLTdmYTBmYjBkZGI0ZSIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJvZmZsaW5lLXRva2VuLWdlbmVyYXRvciIsIm5vbmNlIjoiZTRmOTY4NjYtZTE3NS00YzM2LWEyODMtZTQwMmI3M2U5NzhlIiwiYXV0aF90aW1lIjowLCJzZXNzaW9uX3N0YXRlIjoiYWNkNTQ3MTctNzJhZC00MGU3LWI0ZDctZjlkMTAyNDRkNWZlIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZXBvcnRpdW0iOnsicm9sZXMiOlsiYWRtaW5pc3RyYXRvciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.SOL-wlZiQ4BoLLfaeIW8QoxJ6xzrgxBjwSiSzkLBPYw",
        }
        
        self.driver = webdriver.Remote('https://tip.perfectomobile.com/nexperience/perfectomobile/wd/hub', capabilities)
        self.driver.implicitly_wait(20)
        self.create_reporting_client()
        #self.suitesetup_result()
        self.reporting_client.test_start(self.testCaseName, TestContext([], 'TipCustomTag'))
        
    def run(self, result=None):
        self.currentResult = True  # remember result for use in tearDown
        #print('Before' + self.currentResult)
        unittest.TestCase.run(self, result)  # call superclass run method
        #print('Result' + result)

    def tearDown(self):
        warnings.simplefilter("ignore", ResourceWarning)
        try:
            print("-------------------------------------------")
            print(" -- Tear Down --")       
            
            self.reporting_client.test_stop(TestResultFactory.create_success())
            #print('Report-Url: ' + self.reporting_client.report_url() + '\n')

           # if self.currentResult.wasSuccessful():
             #   print(" -- Test Successful --")       
                #self.reporting_client.test_stop(TestResultFactory.create_success())
          #  else:
            #    print(" -- Test Not Successful --")   
                #self.reporting_client.test_stop(TestResultFactory.create_failure('failure 4096' * 1000))
                
            #      self.reporting_client.test_stop(TestResultFactory.create_failure(self.currentResult.errors,self.currentResult.failures))
             #Print report's url
            print('Report-Url: ' + self.reporting_client.report_url() + '\n')
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

    def create_reporting_client(self):
        perfecto_execution_context = PerfectoExecutionContext(self.driver, self.tags, Job(self.jobname, self.jobnumber),
                                                       Project(self.projectname, self.projectversion))
        #perfecto_execution_context = PerfectoExecutionContext(self.driver, ['execution tag1', 'execution tag2'])
        self.reporting_client = PerfectoReportiumClient(perfecto_execution_context)

    
      