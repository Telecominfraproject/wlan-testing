"""
This file contains the functions that are required for Perfecto iOS devices
"""
import logging
import os
import re
import time
import warnings
from time import gmtime, strftime
import allure
import pytest
import requests
import urllib3
from appium import webdriver
from appium.webdriver import webdriver
from appium.webdriver.common.mobileby import MobileBy
from perfecto import (PerfectoExecutionContext, PerfectoReportiumClient, TestContext)
from perfecto.model.model import Job, Project
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from xml.etree import ElementTree as ET


class ios_libs:
    global driver, perfecto_execution_context, deviceModel
    def __init__(self, perfecto_data=None, dut_data=None, testcase=None):
        logging_level = logging.INFO
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging_level)
        self.perfecto_data = perfecto_data
        self.dut_data = dut_data
        self.testcase_name = testcase
        pass

    # Opens an APP on the device based on the argument given
    def openApp(self, appName, setup_perfectoMobile):
        setup_perfectoMobile[1].step_start("Opening App: " + appName)
        params = {'identifier': appName}
        # Open/Close/Open Action is performed to ensure the app is back to its Original Settings
        setup_perfectoMobile[0].execute_script('mobile:application:open', params)
        setup_perfectoMobile[0].execute_script('mobile:application:close', params)
        setup_perfectoMobile[0].execute_script('mobile:application:open', params)

    # Tries to swipe the screen on the device based on the Params given
    def scrollDown(self, setup_perfectoMobile):
        print("Scroll Down")
        setup_perfectoMobile[1].step_start("Scroll Down")
        params2 = {}
        params2["start"] = "50%,90%"
        params2["end"] = "50%,20%"
        params2["duration"] = "4"
        # time.sleep(2)
        setup_perfectoMobile[0].execute_script('mobile:touch:swipe', params2)
        time.sleep(3)

    # Closes an APP on the device based on the argument given
    def closeApp(self, appName, setup_perfectoMobile):
        # print("Closing App.." + appName)
        setup_perfectoMobile[1].step_start("Closing App: " + appName)
        params = {'identifier': appName}
        setup_perfectoMobile[0].execute_script('mobile:application:close', params)

    # Returns the Data needed for the Device
    def get_ToggleAirplaneMode_data(self, get_device_configuration):

        passPoint_data = {
            "webURL": "https://www.google.com",
            "lblSearch": "//*[@class='gLFyf']",
            "elelSearch": "(//*[@class='sbic sb43'])[1]",
            "BtnRunSpeedTest": "//*[text()='RUN SPEED TEST']",
            "bundleId-iOS-Settings": get_device_configuration["bundleId-iOS-Settings"],
            "bundleId-iOS-Safari": get_device_configuration["bundleId-iOS-Safari"],
            "downloadMbps": "//*[@id='knowledge-verticals-internetspeedtest__download']/P[@class='spiqle']",
            "UploadMbps": "//*[@id='knowledge-verticals-internetspeedtest__upload']/P[@class='spiqle']",
            # Android
            "platformName-android": get_device_configuration["platformName-android"],
            "appPackage-android": get_device_configuration["appPackage-android"]
        }
        return passPoint_data

    def report_client(self, value):
        global reporting_client  # declare a to be a global
        reporting_client = value  # this sets the global value of a

    def reportPerfecto(testCaseName, testCaseStatus, testErrorMsg, reportURL):
        global testCaseNameList  # declare a to be a global
        global testCaseStatusList
        global testCaseErrorMsg
        global testCaseReportURL

        testCaseNameList.append(testCaseName)
        testCaseStatusList.append(testCaseStatus)
        testCaseErrorMsg.append(str(testErrorMsg))
        testCaseReportURL.append(reportURL)

    # Gets the Device response from Perfecto
    def response_device(self, model):
        securityToken = self.perfecto_data["securityToken"]
        perfectoURL = self.perfecto_data["perfectoURL"]
        url = f"https://{perfectoURL}.perfectomobile.com/services/handsets?operation=list&securityToken={securityToken}&model={model}"
        resp = requests.get(url=url)
        return ET.fromstring(resp.content)

    def get_attribute_device(self, responseXml, attribute):
        try:
            return responseXml.find('handset').find(attribute).text
        except:
            print(f"Unable to get value of {attribute} from response")
            return ""

    # Checks to see if a particular handset is available
    def is_device_available(self, model):
        try:
            response_xml = self.response_device(model)
        except:
            print("Unable to get response.")
            raise Exception("Unable to get response.")
        device_available = self.get_attribute_device(response_xml, 'available')
        print("Result:" + device_available)
        if device_available == 'true':
            return True
        else:
            allocated_to = self.get_attribute_device(response_xml, 'allocatedTo')
            print("The device is currently allocated to:" + allocated_to)
            return False

    # Checks whether the device is available or not.If the device is not available rechecks depending upon the
    # 'timerValue' and 'timerThreshold' values.With the current parameters it will check after:10,20,40,80 mins.
    def is_device_Available_timeout(self, model):
        device_available = self.is_device_available(model)
        timer_value = 5
        timer_threshold = 80
        if not device_available:
            while timer_value <= timer_threshold:
                print("Last checked at:" + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                print(f"Waiting for: {timer_value} min(s)")
                time.sleep(timer_value * 60)
                print("Checking now at:" + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                device_available = self.is_device_available(model)
                if device_available:
                    return True
                else:
                    timer_value = timer_value + 5

            if timer_value > timer_threshold:
                return False
            else:
                return True
        else:
            return True

    def get_device_attribuites(self, model, attribute):
        try:
            response_xml = self.response_device(model)
        except:
            print("Unable to get response.")
            raise Exception("Unable to get response.")
        try:
            attribute_value = self.get_attribute_device(response_xml, str(attribute))
        except:
            attribute_value = False
        return attribute_value

    # Used to get the iOS Device driver obj for further utility,Base function for iOS Tests
    def setup_perfectoMobile_iOS(self, get_device_configuration, perfecto_data):
        global perfecto_execution_context, driver, deviceModel
        from appium import webdriver
        driver = None
        reporting_client = None
        warnings.simplefilter("ignore", ResourceWarning)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        capabilities = {
            'platformName': get_device_configuration["platformName-iOS"],
            'model': get_device_configuration["model-iOS"],
            'browserName': 'safari',
            # 'automationName' : 'Appium',
            'securityToken': perfecto_data["securityToken"],
            'useAppiumForWeb': 'false',
            'autoAcceptAlerts': 'true',
            # 'bundleId' : request.config.getini("bundleId-iOS"),
            'useAppiumForHybrid': 'false',
        }

        # Check if the device is available
        if not self.is_device_Available_timeout(capabilities['model']):
            print("Unable to get device.")
            pytest.exit("Exiting Pytest")

        driver = webdriver.Remote(
            'https://' + perfecto_data["perfectoURL"] + '.perfectomobile.com/nexperience/perfectomobile/wd/hub',
            capabilities)
        driver.implicitly_wait(2)
        if os.environ.get('PYTEST_CURRENT_TEST') is not None:
            TestCaseFullName = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
            nCurrentTestMethodNameSplit = re.sub(r'\[.*?\]\ *', "", TestCaseFullName)
        else:
            nCurrentTestMethodNameSplit = self.testcase_name
        try:
            # TestCaseName = nCurrentTestMethodNameSplit.removeprefix('test_')
            testcase = nCurrentTestMethodNameSplit.replace('test_', '')
            print("\n\nExecuting TestCase: " + testcase)
        except Exception as e:
            TestCaseName = nCurrentTestMethodNameSplit
            print("\nUpgrade Python to 3.9 to avoid test_ string in your test case name, see below URL")
            # print("https://www.andreagrandi.it/2020/10/11/python39-introduces-removeprefix-removesuffix/")

        projectname = perfecto_data["projectName"]
        projectversion = perfecto_data["projectVersion"]
        jobname = get_device_configuration["jobName"]
        jobnumber = get_device_configuration["jobNumber"]
        tags = perfecto_data["reportTags"]
        test_case_name = testcase

        print("\nSetting Perfecto ReportClient....")
        perfecto_execution_context = PerfectoExecutionContext(driver, tags, Job(jobname, jobnumber),
                                                              Project(projectname, projectversion))
        reporting_client = PerfectoReportiumClient(perfecto_execution_context)
        reporting_client.test_start(test_case_name, TestContext([], "Perforce"))
        self.report_client(reporting_client)
        try:
            params = {'property': 'model'}
            deviceModel = driver.execute_script('mobile:handset:info', params)
        except:
            pass

        # request.addfinalizer(teardown)

        if driver is None:
            yield -1
        else:
            yield driver, reporting_client

    # Teardown function used to release all the data that presently hold from Perfecto
    def teardown(self):
        global driver, perfecto_execution_context, deviceModel
        reporting_client = PerfectoReportiumClient(perfecto_execution_context)
        try:
            print("\n---------- Tear Down ----------")
            print('Report-Url: ' + reporting_client.report_url())
            try:
                allure.dynamic.link(
                    str(reporting_client.report_url()),
                    name=str(deviceModel))
            except:
                print("fail to attach video link")
            print("----------------------------------------------------------\n\n\n\n")
            driver.close()
        except Exception as e:
            print(" -- Exception While Tear Down --")
            driver.close()
            print(e)
        finally:
            try:
                driver.quit()
            except Exception as e:
                print(" -- Exception Not Able To Quit --")
                print(e)

    # Checks the Available SSIDS on device and return them in the form of List
    def get_all_available_ssids(self, driver):
        print("\n----------------------------")
        print("Get All Available SSID")
        print("------------------------------")

        active_ssid_list = []
        try:
            time.sleep(2)
            driver.implicitly_wait(2)
            elements = driver.find_elements_by_xpath("(//*[@label='More Info']/parent::*/XCUIElementTypeStaticText)")
            print(len(elements))
            for i in range(len(elements)):
                active_ssid_list.append(elements[i].text)
            print("active_ssid_list: ", active_ssid_list)
        except:
            print("No SSIDS available")

        return active_ssid_list

    # checks if SSID is visible or not on the Phone screen
    def ssid_Visible(self, driver, WifiName):
        wifiSelectionElement = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='" + WifiName + "']")))
        isVisible = wifiSelectionElement.get_attribute("visible")
        print(f"Is ssid visible: {isVisible}")
        if (isVisible == 'false'):
            return False
        else:
            return True

    # Tries to swipe the screen on the device based on the Params given
    def scrollDown(self, setup_perfectoMobile):
        print("Scroll Down")
        setup_perfectoMobile[1].step_start("Scroll Down")
        params2 = {}
        params2["start"] = "50%,90%"
        params2["end"] = "50%,20%"
        params2["duration"] = "4"
        # time.sleep(2)
        setup_perfectoMobile[0].execute_script('mobile:touch:swipe', params2)
        time.sleep(3)

    # Runs Speed test on OOKla Speed test App on Android devices, OOKLA app should be present on the Device
    def speed_test(self, setup_perfectoMobile):
        driver = setup_perfectoMobile[0]
        driver.switch_to.context('NATIVE_APP')
        self.openApp('com.ookla.speedtest', setup_perfectoMobile)
        driver.find_element_by_xpath("//*[@label='GO']").click()
        # Wait untill 2 minutes for the test to complete
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@value='Test Again']")))
        result = driver.find_element_by_xpath("//XCUIElementTypeOther[contains(@label,'Download Speed')]").text
        print(result)
        download_speed = result.split('Download Speed, ')[1].split('. ')[0]
        upload_speed = result.split('Upload speed, ')[1].split('. ')[0]
        download_speed = str(download_speed)[0:4]
        upload_speed = str(upload_speed)[0:4]
        print(f"Download speed: {download_speed}")
        print(f"Upload speed: {upload_speed}")
        return download_speed, upload_speed

    # Function used to connect to a particular SSID
    def wifi_connect(self, ssid, passkey, setup_perfectoMobile, connData):
        print("\n-------------------------------------")
        print("Select Wifi/Get IP Address IOS Connection")
        print("-------------------------------------")
        is_internet = False
        wifi_name = ssid
        wifi_pass = passkey
        ssid_found = False
        print("Verifying Wifi/AP Connection Details....")
        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]

        report.step_start("Switching Driver Context")
        print("Switching Context to Native")
        driver.switch_to.context('NATIVE_APP')
        # driver.switch_to.context(contexts[0])

        report.step_start("Set Wifi Network to " + wifi_name)
        # Open Settings Application
        logging.info("Opening IOS setting APP")
        self.openApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)

        try:
            time.sleep(2)
            driver.implicitly_wait(2)
            try:
                print("Verifying Connected Wifi Connection")
                report.step_start("Loading Wifi Page")
                element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']")
                element.click()
            except NoSuchElementException:
                print("Exception: Verify Xpath - unable to click on Wifi")
                logging.error("Exception: Verify Xpath - unable to click on Wifi")

            time.sleep(2)
            driver.implicitly_wait(4)
            # --------------------To Turn on WIFi Switch if already OFF--------------------------------
            try:
                get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='0']")
                get_wifi_switch_element_text = get_wifi_switch_element.text
                try:
                    if get_wifi_switch_element_text == "0" or get_wifi_switch_element_text == 0:
                        get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='0']")
                        driver.implicitly_wait(1)
                        get_wifi_switch_element.click()
                        driver.implicitly_wait(1)
                        i = 0
                        for i in range(5):
                            try:
                                get_wifi_switch_element = driver.find_element_by_xpath(
                                    "//*[@label='Wi-Fi' and @value='1']")
                                get_wifi_switch_element_text = get_wifi_switch_element.text
                            except:
                                print("Switch is OFF")
                                logging.info("Wifi Switch is OFF")

                            if get_wifi_switch_element_text == "1" or get_wifi_switch_element_text == 1:
                                print("WIFI Switch is ON")
                                logging.info("Wifi Switch is ON")
                                break
                            else:
                                try:
                                    get_wifi_switch_element = driver.find_element_by_xpath(
                                        "//*[@label='Wi-Fi' and @value='0']")
                                    get_wifi_switch_element_text = get_wifi_switch_element.text
                                except:
                                    print("WIFi switch is ON")
                                    logging.info("Wifi Switch is ON")
                        if (get_wifi_switch_element_text == "0" or get_wifi_switch_element_text == 0):
                            print("switch is still OFF")
                            logging.error("Wifi Switch is OFF")
                            self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
                            return is_internet, setup_perfectoMobile, ssid_found
                    else:
                        print("Switch is Still OFF")
                        logging.error("Wifi Switch is OFF")
                        self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
                        return is_internet, setup_perfectoMobile, ssid_found
                except:
                    print("No switch element found")
                    logging.error("No switch element found")
            except:
                print("get_wifi_switch_element is ON")
                logging.warning("get_wifi_switch_element is ON")
            # --------------------To Turn on WIFi Switch if already OFF--------------------------------

        except:
            print("Cannot find WIFI element")
            logging.error("Cannot find WIFI element")
            self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
            return is_internet, setup_perfectoMobile, ssid_found

        # ---------------------This is to Forget current connected SSID-------------------------------
        # ---------------------This to Avoid any popup page from captive portal--------------------#

        try:
            time.sleep(4)
            print("getting in to Additional details")
            report.step_start("Clicking More Info")
            logging.info("getting in to Additional details")
            additional_details_element = driver.find_element_by_xpath(
                "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeButton[@label='More Info']")
            additional_details_element.click()
            try:
                time.sleep(2)
                print("Forget Connected Network")
                logging.info("Forget Connected Network")
                forget_ssid = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Forget This Network']")))
                forget_ssid.click()
                print("Forget old ssid")
                logging.info("Forget old ssid")
                try:
                    time.sleep(2)
                    report.step_start("Forget SSID popup1")
                    forget_ssid_popup = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Forget']")))
                    forget_ssid_popup.click()

                    print("**alert** Forget SSID popup killed **alert**")
                except:
                    print("Forget SSID popup not found")
            except:
                print("couldn't find forget ssid element")
                logging.warning("couldn't find forget ssid element")
        except:
            print("No connected SSID")
            logging.info("No connected SSID")
            try:
                report.step_start("Unexpected Captive Popup")
                print("Unexpeceted Captive Poped Up")
                captive_portal_cancel_element = driver.find_element_by_xpath("//*[@label='Cancel']")
                captive_portal_cancel_element.click()
                time.sleep(2)
                use_other_network_element = driver.find_element_by_xpath("//*[@label='Use Other Network']")
                use_other_network_element.click()
                time.sleep(2)
            except:
                print("No Captive Portal Popup Found")
                try:
                    time.sleep(4)
                    print("getting in to Additional details")
                    report.step_start("Clicking More Info")
                    additional_details_element = driver.find_element_by_xpath(
                        "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeButton[@label='More Info']")
                    additional_details_element.click()
                    try:
                        time.sleep(2)
                        print("Forget Connected Network")
                        forget_ssid = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Forget This Network']")))
                        forget_ssid.click()
                        print("Forget old ssid")
                        try:
                            time.sleep(2)
                            report.step_start("Forget SSID popup1")
                            forget_ssid_popup = WebDriverWait(driver, 30).until(
                                EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Forget']")))
                            forget_ssid_popup.click()

                            print("**alert** Forget SSID popup killed **alert**")
                        except:
                            print("Forget SSID popup not found")
                    except:
                        print("couldn't find forget ssid element")
                except:
                    print("No connected SSID")

        # ---------------------This is to Forget current connected SSID-------------------------------

        # ---------------------To get all available SSID and select it-------------------------------
        print("Searching for Wifi: " + wifi_name)
        # allure.attach(name= body=str("Searching for Wifi: " + wifi_name))
        time.sleep(2)
        report.step_start("Searching SSID")
        print("Selecting Wifi: " + wifi_name)
        available_ssids = False

        try:
            for check_for_all_ssids in range(12):
                available_ssids = self.get_all_available_ssids(driver)
                allure.attach(name="Available SSIDs in device: ", body=str(available_ssids))
                try:
                    if (not self.ssid_Visible(driver, wifi_name)) or (wifi_name not in available_ssids):
                        self.scrollDown(setup_perfectoMobile)
                        time.sleep(2)
                    else:
                        try:
                            driver.implicitly_wait(8)
                            report.step_start("Selecting SSID To Connect")
                            ssid_found = True
                            print(wifi_name + " : Found in Device")
                            wifiSelElement = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='" + wifi_name + "']")))
                            print(wifiSelElement)
                            wifiSelElement.click()
                            print("Selecting SSID")
                            break
                        except:
                            print("SSID unable to select")
                            logging.error("Unable to select SSID")
                            report.step_start("Selecting Unable SSID To Connect")
                            self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
                            return is_internet, setup_perfectoMobile, ssid_found

                except:
                    print("couldn't connect to " + wifi_name)
                    logging.error("Couldn't Find ssid")
                    # request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                    self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
                    return is_internet, setup_perfectoMobile, ssid_found
                    pass

            if not ssid_found:
                print("could not found " + wifi_name + " in device")
                logging.error("Couldn't Find ssid in device")
                self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
                return is_internet, setup_perfectoMobile, ssid_found
        except:
            pass
        # ---------------------To get all available SSID and select it-------------------------------
        # ---------------------Set Password-------------------------------
        try:
            driver.implicitly_wait(5)
            print("Entering Password")
            logging.info("Entering Password")
            report.step_start("Entering Password")
            wifiPassword = driver.find_element_by_xpath("//*[@label='Password']")
            wifiPassword.send_keys(wifi_pass)
        except NoSuchElementException:
            print("Enter Password Page Not Loaded")
            logging.warning("Enter Password Page Not Loaded")
        # ---------------------Set Password-------------------------------

        # ---------------------Click on join-------------------------------
        try:
            driver.implicitly_wait(4)
            print("Selecting join")
            report.step_start("Clicking JOIN")
            joinBTN = driver.find_element_by_xpath("//*[@label='Join']")
            joinBTN.click()
        except Exception as e:
            print("Join Button Not Enabled...Password may not be needed")
            logging.warning("Join Button Not Enabled...Password may not be needed")
        # ---------------------Click on join-------------------------------

        # ---------------------check if internet-------------------------------
        try:
            driver.implicitly_wait(5)
            WifiInternetErrMsg2 = driver.find_element_by_xpath("//*[@label='No Internet Connection']")
            # = driver.find_element_by_xpath("//*[@label='No Internet Connection']").text
        except Exception as e:
            is_internet = True
            print("No Wifi-AP Error Internet Error: " + wifi_name)
            # Need to add Wait for Selected Wifi Xpath
            # time.sleep(3)
        # ---------------------check if internet-------------------------------
        return is_internet, setup_perfectoMobile, ssid_found

    # Gets the IP Address of the connected SSID from Phone
    def get_ip_address(self, ssid, setup_perfectoMobile, connData):
        wifi_name = ssid
        driver = setup_perfectoMobile[0]
        report = setup_perfectoMobile[1]
        # ---------------------Additional INFO-------------------------------
        try:
            driver.implicitly_wait(5)
            print("Selecting SSID: ", wifi_name)
            report.step_start("Additional details of SSID")
            additional_details_element = WebDriverWait(driver, 35).until(
                EC.presence_of_element_located((MobileBy.XPATH,
                                                "//*[@label='" + wifi_name + "']")))
            # //*[@label='selected']/parent::*/parent::*/XCUIElementTypeButton[@label='More Info']
            additional_details_element.click()

            try:
                driver.implicitly_wait(2)
                report.step_start("Checking SSID Name as Expected")
                print("Checking SSID Name")
                ssidname_text = driver.find_element_by_xpath("//*[@label='" + wifi_name + "']").text
                print(ssidname_text)
                if (ssidname_text == wifi_name):
                    print("SSID Matched")
                    logging.info("SSID Matched")
                    allure.attach(name="SSID Matched ", body=str(wifi_name))
                else:
                    print("SSID Not Matched")
                    logging.info("SSID Not Matched")
                    allure.attach(name="SSID Not Matched ", body=str(wifi_name))
                    reportFlag = False
                    assert reportFlag
            except:
                print("SSID is not Checked in more Info")
                logging.warning("SSID is not Checked in more Info")
            try:
                report.step_start("Checking WiFi Address")
                print("Checking WIFI address")
                # (//*[@label="IP Address"]/parent::*/XCUIElementTypeStaticText)[2]
                wifi_address_element_text = driver.find_element_by_xpath(
                    "(//*[@label='Wi-Fi Address']/parent::*/XCUIElementTypeStaticText)[2]").text
                print("wifi_address_element_text: ", wifi_address_element_text)
                allure.attach(name="Connected SSID WiFi-Address: ", body=str(wifi_address_element_text))
            except Exception as e:
                print("WiFi-Address not Found")
                logging.warning("WiFi-Address not Found")
            try:
                time.sleep(4)
                report.step_start("Checking IP Address")
                print("Checking IP address")
                logging.info("Checking IP address")
                # (//*[@label="IP Address"]/parent::*/XCUIElementTypeStaticText)[2]
                ip_address_element_text = driver.find_element_by_xpath(
                    "(//*[@label='IP Address']/parent::*/XCUIElementTypeStaticText)[2]").text
                print("ip_address_element_text: ", ip_address_element_text)
            except Exception as e:
                try:
                    time.sleep(4)
                    print("Scrolling for checking ip address")
                    self.scrollDown(setup_perfectoMobile)
                    ip_address_element_text = driver.find_element_by_xpath(
                        "(//*[@label='IP Address']/parent::*/XCUIElementTypeStaticText)[2]").text
                    print("ip_address_element_text: ", ip_address_element_text)
                except:
                    print("IP Address not Found")
                    logging.info("IP Address not Found")
        except Exception as e:
            print("Select Additional Info failed")
            logging.warning("Select Additional Info failed")
        # ---------------------Additional INFO-------------------------------
        return ip_address_element_text

    def run_speed_test(self, setup_perfectoMobile, connData):
        print("\n-------------------------------------")
        print("Verify Upload & Download Speed")
        print("-------------------------------------")

        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]
        current_result = True

        contexts = driver.contexts
        # print("Printing Context")
        # print(contexts)

        driver.switch_to.context('WEBVIEW_1')
        time.sleep(5)
        try:
            print("Launching Safari")
            report.step_start("Google Home Page")
            time.sleep(4)
            driver.get(connData["webURL"])
            print("Enter Search Text")
            time.sleep(4)
            driver.find_element_by_xpath("//*[@class='gLFyf']").send_keys("Internet speed test")
            time.sleep(4)
            driver.find_element_by_xpath("//*[@class='aajZCb']//*[@class='nz2CCf']/li[1]/div[1]/div[1]").click()
        except:
            try:
                print("Finding search option")
                report.step_start("Input For Search")
                driver.implicitly_wait(4)
                driver.get(connData["webURL"])
                print("Enter Search Text")
                driver.implicitly_wait(4)
                element_find_txt = driver.find_element_by_xpath(connData["lblSearch"])
                element_find_txt.send_keys("Internet Speed Test")
            except Exception as e:
                print("Launching Safari Failed")
                print(e)

        try:
            print("Click Run Speed Test Button...")
            report.step_start("Click Run Speed Test Button")
            driver.implicitly_wait(4)
            driver.find_element_by_xpath(connData["BtnRunSpeedTest"]).click()
        except NoSuchElementException:
            current_result = False
            print("Run Speed Test Button element not found", NoSuchElementException)
            return current_result

        # Get upload/Download Speed
        try:
            report.step_start("Get upload/Download Speed")
            time.sleep(60)
            download_mbps = driver.find_element_by_xpath(connData["downloadMbps"])
            download_speed = download_mbps.text
            print("Download: " + download_speed + " Mbps")

            time.sleep(30)
            upload_mbps = driver.find_element_by_xpath(connData["UploadMbps"])
            upload_speed = upload_mbps.text
            print("Upload: " + upload_speed + " Mbps")
            allure.attach(name="Speed Test logs: ",
                          body=str("Upload: " + upload_speed + " Mbps" + "  Download: " + download_speed + " Mbps"))
            print("Access Point Verification Completed Successfully")

        except NoSuchElementException:
            print("Access Point Verification NOT Completed, checking Connection....")
            current_result = False
        return current_result
    #----------Wifi connect for Enterprise Security---------------
    def wifi_connect_eap(self, ssid, user, ttls_passwd, setup_perfectoMobile, connData):
        print("\n-------------------------------------")
        print("Select Wifi/Get IP Address IOS Connection")
        print("-------------------------------------")
        is_internet = False
        wifi_name = ssid
        ssid_found = False
        print("Verifying Wifi/AP Connection Details....")
        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]

        report.step_start("Switching Driver Context")
        print("Switching Context to Native")
        driver.switch_to.context('NATIVE_APP')
        # driver.switch_to.context(contexts[0])

        report.step_start("Set Wifi Network to " + wifi_name)
        # Open Settings Application
        logging.info("Opening IOS setting APP")
        self.openApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)

        try:
            time.sleep(2)
            driver.implicitly_wait(2)
            try:
                print("Verifying Connected Wifi Connection")
                report.step_start("Loading Wifi Page")
                element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']")
                element.click()
            except NoSuchElementException:
                print("Exception: Verify Xpath - unable to click on Wifi")
                logging.error("Exception: Verify Xpath - unable to click on Wifi")

            time.sleep(2)
            driver.implicitly_wait(4)
            # --------------------To Turn on WIFi Switch if already OFF--------------------------------
            try:
                get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='0']")
                get_wifi_switch_element_text = get_wifi_switch_element.text
                try:
                    if get_wifi_switch_element_text == "0" or get_wifi_switch_element_text == 0:
                        get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='0']")
                        driver.implicitly_wait(1)
                        get_wifi_switch_element.click()
                        driver.implicitly_wait(1)
                        i = 0
                        for i in range(5):
                            try:
                                get_wifi_switch_element = driver.find_element_by_xpath(
                                    "//*[@label='Wi-Fi' and @value='1']")
                                get_wifi_switch_element_text = get_wifi_switch_element.text
                            except:
                                print("Switch is OFF")
                                logging.info("Wifi Switch is OFF")

                            if get_wifi_switch_element_text == "1" or get_wifi_switch_element_text == 1:
                                print("WIFI Switch is ON")
                                logging.info("Wifi Switch is ON")
                                break
                            else:
                                try:
                                    get_wifi_switch_element = driver.find_element_by_xpath(
                                        "//*[@label='Wi-Fi' and @value='0']")
                                    get_wifi_switch_element_text = get_wifi_switch_element.text
                                except:
                                    print("WIFi switch is ON")
                                    logging.info("Wifi Switch is ON")
                        if (get_wifi_switch_element_text == "0" or get_wifi_switch_element_text == 0):
                            print("switch is still OFF")
                            logging.error("Wifi Switch is OFF")
                            self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
                            return is_internet, setup_perfectoMobile, ssid_found
                    else:
                        print("Switch is Still OFF")
                        logging.error("Wifi Switch is OFF")
                        self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
                        return is_internet, setup_perfectoMobile, ssid_found
                except:
                    print("No switch element found")
                    logging.error("No switch element found")
            except:
                print("get_wifi_switch_element is ON")
                logging.warning("get_wifi_switch_element is ON")
            # --------------------To Turn on WIFi Switch if already OFF--------------------------------

        except:
            print("Cannot find WIFI element")
            logging.error("Cannot find WIFI element")
            self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
            return is_internet, setup_perfectoMobile, ssid_found

        # ---------------------This is to Forget current connected SSID-------------------------------
        # ---------------------This to Avoid any popup page from captive portal--------------------#

        try:
            time.sleep(4)
            print("getting in to Additional details")
            report.step_start("Clicking More Info")
            logging.info("getting in to Additional details")
            additional_details_element = driver.find_element_by_xpath(
                "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeButton[@label='More Info']")
            additional_details_element.click()
            try:
                time.sleep(2)
                print("Forget Connected Network")
                logging.info("Forget Connected Network")
                forget_ssid = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Forget This Network']")))
                forget_ssid.click()
                print("Forget old ssid")
                logging.info("Forget old ssid")
                try:
                    time.sleep(2)
                    report.step_start("Forget SSID popup1")
                    forget_ssid_popup = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Forget']")))
                    forget_ssid_popup.click()

                    print("**alert** Forget SSID popup killed **alert**")
                except:
                    print("Forget SSID popup not found")
            except:
                print("couldn't find forget ssid element")
                logging.warning("couldn't find forget ssid element")
        except:
            print("No connected SSID")
            logging.info("No connected SSID")
            try:
                report.step_start("Unexpected Captive Popup")
                print("Unexpeceted Captive Poped Up")
                captive_portal_cancel_element = driver.find_element_by_xpath("//*[@label='Cancel']")
                captive_portal_cancel_element.click()
                time.sleep(2)
                use_other_network_element = driver.find_element_by_xpath("//*[@label='Use Other Network']")
                use_other_network_element.click()
                time.sleep(2)
            except:
                print("No Captive Portal Popup Found")
                try:
                    time.sleep(4)
                    print("getting in to Additional details")
                    report.step_start("Clicking More Info")
                    additional_details_element = driver.find_element_by_xpath(
                        "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeButton[@label='More Info']")
                    additional_details_element.click()
                    try:
                        time.sleep(2)
                        print("Forget Connected Network")
                        forget_ssid = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Forget This Network']")))
                        forget_ssid.click()
                        print("Forget old ssid")
                        try:
                            time.sleep(2)
                            report.step_start("Forget SSID popup1")
                            forget_ssid_popup = WebDriverWait(driver, 30).until(
                                EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Forget']")))
                            forget_ssid_popup.click()

                            print("**alert** Forget SSID popup killed **alert**")
                        except:
                            print("Forget SSID popup not found")
                    except:
                        print("couldn't find forget ssid element")
                except:
                    print("No connected SSID")

        # ---------------------This is to Forget current connected SSID-------------------------------

        # ---------------------To get all available SSID and select it-------------------------------
        print("Searching for Wifi: " + wifi_name)
        # allure.attach(name= body=str("Searching for Wifi: " + wifi_name))
        time.sleep(2)
        report.step_start("Searching SSID")
        print("Selecting Wifi: " + wifi_name)
        ssid_found = False
        available_ssids = False

        try:
            for check_for_all_ssids in range(12):
                available_ssids = self.get_all_available_ssids(driver)
                allure.attach(name="Available SSIDs in device: ", body=str(available_ssids))
                try:
                    if (not self.ssid_Visible(driver, wifi_name)) or (wifi_name not in available_ssids):
                        self.scrollDown(setup_perfectoMobile)
                        time.sleep(2)
                    else:
                        try:
                            driver.implicitly_wait(8)
                            report.step_start("Selecting SSID To Connect")
                            ssid_found = True
                            print(wifi_name + " : Found in Device")
                            wifi_sel_element = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='" + wifi_name + "']")))
                            print(wifi_sel_element)
                            wifi_sel_element.click()
                            print("Selecting SSID")
                            break
                        except:
                            print("SSID unable to select")
                            logging.error("Unable to select SSID")
                            report.step_start("Selecting Unable SSID To Connect")
                            self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
                            return is_internet, setup_perfectoMobile, ssid_found

                except:
                    print("couldn't connect to " + wifi_name)
                    logging.error("Couldn't Find ssid")
                    # request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                    self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
                    return is_internet, setup_perfectoMobile, ssid_found
                    pass

            if not ssid_found:
                print("could not found " + wifi_name + " in device")
                logging.error("Couldn't Find ssid in device")
                self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
                return is_internet, setup_perfectoMobile, ssid_found
        except:
            pass
        # ---------------------To get all available SSID and select it-------------------------------
        # Set username
        # -------------------------------------------------------
        try:
            driver.implicitly_wait(4)
            report.step_start("Entering User")
            print("Entering User name")
            logging.info("Entering User name")
            wifi_user_element = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Username']")))
            wifi_user_element.send_keys(user)
        except NoSuchElementException:
            print("Password Page Not Loaded, password May be cached in the System")
            logging.error("Password Page Not Loaded, password May be cached in the System")
        # -------------------------------------------------------

        # ---------------------Set Password-------------------------------
        try:
            driver.implicitly_wait(4)
            report.step_start("Entering Password")
            print("Entering password")
            wifi_password = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Password']")))
            wifi_password.send_keys(ttls_passwd)
        except NoSuchElementException:
            print("Enter Password Page Not Loaded")
            logging.error("Enter Password Page Not Loaded")
        # ---------------------Set Password-------------------------------
        # -------------------------------------------------------

        # ---------------------Click on join-------------------------------
        try:
            driver.implicitly_wait(4)
            report.step_start("Clicking Join")
            print("Clicking Join")
            join_btn = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Join']")))
            join_btn.click()
        except Exception as e:
            print("Join Button Not Enabled...Password may not be needed")
            logging.error("Join Button Not Enabled...Password may not be needed")
        # ---------------------Click on join-------------------------------
        # Selecting certificate
        # -------------------------------------------------------
        try:
            driver.implicitly_wait(4)
            report.step_start("Clicking Trust CA Cert")
            print("Clicking Trust CA Cert")
            cert_element = WebDriverWait(driver, 45).until(
                EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='Trust']")))
            cert_element.click()
        except NoSuchElementException:
            print("Password Page Not Loaded, password May be cached in the System")
            logging.error("Password Page Not Loaded, password May be cached in the System")

        # ---------------------check if internet-------------------------------
        try:
            driver.implicitly_wait(5)
            wifi_internet_err_msg = driver.find_element_by_xpath("//*[@label='No Internet Connection']")
            # = driver.find_element_by_xpath("//*[@label='No Internet Connection']").text
        except Exception as e:
            is_internet = True
            print("No Wifi-AP Error Internet Error: " + wifi_name)
            logging.error("No Wifi-AP Error Internet Error: " + wifi_name)
            # Need to add Wait for Selected Wifi Xpath
            # time.sleep(3)
        # ---------------------check if internet-------------------------------
        return is_internet, setup_perfectoMobile, ssid_found

    def wifi_disconnect(self, ssid, setup_perfectoMobile, connData):
        print("\n-------------------------------------")
        print("Wifi Disconnect and Forget Connection")
        print("-------------------------------------")
        print("Verifying Wifi/AP Connection Details....")
        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]

        report.step_start("Switching Driver Context")
        print("Switching Context to Native")
        driver.switch_to.context('NATIVE_APP')
        # driver.switch_to.context(contexts[0])

        report.step_start("Set Wifi Network to " + ssid)
        # Open Settings Application
        self.openApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

        try:
            time.sleep(2)
            driver.implicitly_wait(2)
            try:
                print("Verifying Connected Wifi Connection")
                report.step_start("Loading Wifi Page")
                element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']")
                element.click()
            except NoSuchElementException:
                print("Exception: Verify Xpath - unable to click on Wifi")

            time.sleep(2)
            driver.implicitly_wait(2)
            # --------------------To Turn on WIFi Switch if already OFF--------------------------------
            try:
                get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='0']")
                get_wifi_switch_element_text = get_wifi_switch_element.text
                if get_wifi_switch_element_text == "0" or get_wifi_switch_element_text == 0:
                    get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='0']")
                    driver.implicitly_wait(1)
                    get_wifi_switch_element.click()
                    driver.implicitly_wait(1)
                    i = 0
                    for i in range(5):
                        try:
                            get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='1']")
                            get_wifi_switch_element_text = get_wifi_switch_element.text
                        except:
                            print("switch is OFF")

                        if get_wifi_switch_element_text == "1" or get_wifi_switch_element_text == 1:
                            print("WIFI Switch is ON")
                            break
                        else:
                            try:
                                get_wifi_switch_element = driver.find_element_by_xpath(
                                    "//*[@label='Wi-Fi' and @value='0']")
                                get_wifi_switch_element_text = get_wifi_switch_element.text
                            except:
                                print("WIFi switch is ON")
                    if (get_wifi_switch_element_text == "0" or get_wifi_switch_element_text == 0):
                        print("switch is still OFF")
                        self.closeApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)
                else:
                    print("Switch is Still OFF")
                    self.closeApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)
            except:
                print("get_wifi_switch_element is ON")
            # --------------------To Turn on WIFi Switch if already OFF--------------------------------

        except:
            print("Cannot find WIFI element")
            self.closeApp(connData["bundleId-iOS-Settings"], setup_perfectoMobile)

        # ---------------------This is to Forget current connected SSID-------------------------------

        try:
            print("getting in to Additional details")
            additional_details_element = driver.find_element_by_xpath(
                "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeButton[@label='More Info']")
            additional_details_element.click()
            try:
                print("Forget Connected Network")
                forget_ssid = driver.find_element_by_xpath("//*[@label='Forget This Network']")
                forget_ssid.click()
                print("Forget old ssid")
                try:
                    report.step_start("Forget SSID popup1")
                    forget_ssid_popup = driver.find_element_by_xpath("//*[@label='Forget']")
                    forget_ssid_popup.click()

                    print("**alert** Forget SSID popup killed **alert**")
                except:
                    print("Forget SSID popup not found")
            except:
                print("couldn't find forget ssid element")
        except:
            print("No connected SSID")

        # ---------------------This is to Forget current connected SSID-------------------------------
        # --------------------To Turn on WIFi Switch if already OFF--------------------------------
        try:
            get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='1']")
            get_wifi_switch_element_text = get_wifi_switch_element.text
            print("switch state is : ", get_wifi_switch_element_text)
            try:
                if get_wifi_switch_element_text == "1" or get_wifi_switch_element_text == 1:
                    get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='1']")
                    driver.implicitly_wait(1)
                    get_wifi_switch_element.click()
                    driver.implicitly_wait(1)
                    i = 0
                    for i in range(5):
                        try:
                            get_wifi_switch_element = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='0']")
                            get_wifi_switch_element_text = get_wifi_switch_element.text
                        except:
                            print("switch is ON")

                        if get_wifi_switch_element_text == "0" or get_wifi_switch_element_text == 0:
                            print("WIFI Switch is OFF")
                            break
                        else:
                            try:
                                get_wifi_switch_element = driver.find_element_by_xpath(
                                    "//*[@label='Wi-Fi' and @value='1']")
                                get_wifi_switch_element.click()
                                get_wifi_switch_element_text = get_wifi_switch_element.text
                            except:
                                print("WIFi switch is OFF")

                else:
                    print("Switch is Still OFF")
            except:
                pass
        except:
            print("get_wifi_switch_element is ON")
        # --------------------To Turn on WIFi Switch if already OFF--------------------------------


    def toggle_wifi_mode(self,ssid, setup_perfectoMobile, connData):
        print("\n-----------------------")
        print("Toggle Wifi Mode")
        print("-----------------------")

        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]

        # report.step_start("Switching Driver Context")
        # print("Switching Context to Native")
        # driver.switch_to.context('NATIVE_APP')
        # # driver.switch_to.context(contexts[0])

        try:    # Disabling wifi-toggle button
            time.sleep(2)
            driver.implicitly_wait(2)
            print("Disable Wifi Radio Btn")
            report.step_start("Disable Wifi Radio Btn")
            wifiRadioBTN_On = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='1']")
            driver.implicitly_wait(1)
            wifiRadioBTN_On.click()
            driver.implicitly_wait(1)
            time.sleep(5)
        except NoSuchElementException:
            print("Wifi Radio Button Not Disabled...")

        try:    # Enabling wifi-toggle button
            time.sleep(2)
            driver.implicitly_wait(2)
            print("Enable Wifi Radio Btn")
            report.step_start("Enable Wifi Radio Btn")
            wifiRadioBTN_Off = driver.find_element_by_xpath("//*[@label='Wi-Fi' and @value='0']")
            driver.implicitly_wait(1)
            wifiRadioBTN_Off.click()
            driver.implicitly_wait(1)
            time.sleep(5)
        except NoSuchElementException:
            print("Wifi Radio Button Not Enabled...")

        try:    # Checking whether connected to same ssid, after toggling wifi-button
            print("Get Connected Wifi Name if any after Wifi Radio is Enabled")
            report.step_start("Get Connected Wifi Name if any after Wifi Radio is disabled")
            driver.implicitly_wait(2)
            WifiNameElement = WebDriverWait(driver, 35).until(
                EC.presence_of_element_located((MobileBy.XPATH, "//AppiumAUT/XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[2]/XCUIElementTypeStaticText[1]")))
            Wifi_SSID_Name = WifiNameElement.text
            print("Current Wifi Status Name: " + Wifi_SSID_Name)
        except NoSuchElementException:
            Wifi_SSID_Name = "Null"
            print("Device did not connect back to Wifi: " + ssid)

        if Wifi_SSID_Name.__eq__(ssid):
            WifiFlag = True
        else:
            WifiFlag = False

        return WifiFlag

if __name__ == '__main__':
    perfecto_data = {
        "securityToken": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJpYXQiOjE2MzI4Mzc2NDEsImp0aSI6IjAwZGRiYWY5LWQwYjMtNDRjNS1hYjVlLTkyNzFlNzc5ZGUzNiIsImlzcyI6Imh0dHBzOi8vYXV0aDIucGVyZmVjdG9tb2JpbGUuY29tL2F1dGgvcmVhbG1zL3RpcC1wZXJmZWN0b21vYmlsZS1jb20iLCJhdWQiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwic3ViIjoiODNkNjUxMWQtNTBmZS00ZWM5LThkNzAtYTA0ZjBkNTdiZDUyIiwidHlwIjoiT2ZmbGluZSIsImF6cCI6Im9mZmxpbmUtdG9rZW4tZ2VuZXJhdG9yIiwibm9uY2UiOiI2ZjE1YzYxNy01YTU5LTQyOWEtODc2Yi1jOTQxMTQ1ZDFkZTIiLCJzZXNzaW9uX3N0YXRlIjoiYmRjZTFmYTMtMjlkYi00MmFmLWI5YWMtYjZjZmJkMDEyOTFhIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.5R85_1R38ZFXv_wIjjCIsj8NJm1p66dCsLJI5DBEmks",
        "projectName": "TIP-PyTest-Execution",
        "projectVersion": "1.0",
        "reportTags": "TestTag",
        "perfectoURL": "tip",
        "iPhone-11": {
                        "model-iOS": "iPhone-11",
                        "bundleId-iOS": "com.apple.Preferences",
                        "platformName-iOS": "iOS",
                        "bundleId-iOS-Settings": "com.apple.Preferences",
                        "bundleId-iOS-Ping": "com.deftapps.ping",
                        "browserType-iOS": "Safari",
                        "bundleId-iOS-Safari": "com.apple.mobilesafari",
                        "platformName-android": "Android",
                        "appPackage-android": "com.android.settings",
                        "jobName": "Interop-iphone-11",
                        "jobNumber": 38
                    }
    }
    access_point = [{
            "model": "edgecore_eap101",
            "supported_bands": ["2G", "5G"],
            "upstream_port": "1.1.eth1",
            "supported_modes": ["BRIDGE", "NAT", "VLAN"],
            "ssid": {
                "2g-ssid": "OpenWifi",
                "5g-ssid": "OpenWifi",
                "6g-ssid": "candela6ghz",
                "2g-password": "OpenWifi",
                "5g-password": "OpenWifi",
                "6g-password": "hello123",
                "2g-encryption": "WPA2",
                "5g-encryption": "open",
                "6g-encryption": "WPA3",
                "2g-bssid": "68:7d:b4:5f:5c:31 ",
                "5g-bssid": "68:7d:b4:5f:5c:3c",
                "6g-bssid": "68:7d:b4:5f:5c:38"
            },
            "mode": "wifi6",
            "identifier": "903cb36ae255",
            "serial_port": True,
            "host_ip": "10.28.3.102",
            "host_username": "lanforge",
            "host_password": "pumpkin77",
            "host_ssh_port": 22,
            "serial_tty": "/dev/ttyAP5",
            "firmware_version": "next-latest"
        }]
    obj = ios_libs()