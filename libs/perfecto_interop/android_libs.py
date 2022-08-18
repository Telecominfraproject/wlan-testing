import logging
import os
import re
import time
import warnings

import allure
import pytest
import urllib3
from appium.webdriver import webdriver
from perfecto.model.model import Job, Project
from perfecto import (PerfectoExecutionContext, PerfectoReportiumClient, TestContext, TestResultFactory)
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
from perfecto_interop import perfecto_interop
from appium import webdriver


class android_libs(perfecto_interop):
    global driver, perfecto_execution_context

    def __init__(self, perfecto_data=None, dut_data=None):
        super().__init__(perfecto_data=perfecto_data, dut_data=dut_data)
        self.perfecto_data = perfecto_data
        self.dut_data = dut_data
        self.connData = self.get_ToggleAirplaneMode_data(self.android_devices["Galaxy S10.*"])
        print("connData------", self.connData)
        pass

    def check_if_no_internet_popup(self, driver):
        time.sleep(1)
        driver.implicitly_wait(1)
        try:

            popup = driver.find_element_by_xpath("//*[@resource-id='android:id/alertTitle']")
            popup_text = popup.text

            try:
                if popup_text == "Internet may not be available":
                    print("**alert** popup **alert**")

                    try:
                        driver.implicitly_wait(2)
                        time.sleep(2)
                        kill_popup = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/keep_btn']")
                        kill_popup.click()
                        print("popup killed")
                    except:
                        print("Couldnt kill popup")
                        logging.warning("Couldn't kill popup")
                        return False
                else:
                    print("Popup Text is: ", popup_text)
                    print("popup element is: ", popup)
                    return False
            except:
                print("Popup Text is: ", popup_text)
                print("popup element is: ", popup)
                return False
        except:
            pass

    def get_all_available_ssids(self, driver, deviceModelName):
        active_ssid_list = []
        print("Selected Device Model: " + deviceModelName)
        if deviceModelName != ("Pixel 4"):
            try:
                time.sleep(8)
                driver.implicitly_wait(10)
                elements = driver.find_elements_by_xpath("//*[@resource-id='com.android.settings:id/title']")
                # print("elements: ", elements)
                print(len(elements))
                for i in range(len(elements)):
                    # print("elements[i]", elements[i])
                    # print("elements[i].text", elements[i].text)
                    active_ssid_list.append(elements[i].text)
            except:
                print("No SSIDS available")
        else:
            try:
                time.sleep(8)
                driver.implicitly_wait(10)
                elements = driver.find_elements_by_xpath("//*[@resource-id='android:id/title']")
                # print("elements: ", elements)
                print(len(elements))
                for i in range(len(elements)):
                    # print("elements[i]", elements[i])
                    # print("elements[i].text", elements[i].text)
                    try:
                        active_ssid_list.append(elements[i].text)
                    except:
                        print("Encountered a cache SSID which is no longer in the DOM.Moving to next SSID.")
                        logging.warning("Encountered a cache SSID which is no longer in the DOM.Moving to next SSID")
            except:
                print("No SSIDS available")
                logging.error("No SSIDS available")
        return active_ssid_list

    def openApp(self, appName, setup_perfectoMobile):
        print("Refreshing App: " + appName)
        setup_perfectoMobile[1].step_start("Opening App: " + appName)
        params = {'identifier': appName}
        # Open/Close/Open Action is performed to ensure the app is back to its Original Settings
        setup_perfectoMobile[0].execute_script('mobile:application:open', params)
        setup_perfectoMobile[0].execute_script('mobile:application:close', params)
        setup_perfectoMobile[0].execute_script('mobile:application:open', params)

    def closeApp(self, appName, setup_perfectoMobile):
        print("Closing App.." + appName)
        setup_perfectoMobile[1].step_start("Closing App: " + appName)
        params = {'identifier': appName}
        setup_perfectoMobile[0].execute_script('mobile:application:close', params)
        print("Closed App")

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

    def scroll_down_pixel(self, setup_perfectoMobile):
        print("Scroll Down")
        setup_perfectoMobile[1].step_start("Scroll Down")
        params2 = {}
        params2["start"] = "50%,50%"
        params2["end"] = "50%,20%"
        params2["duration"] = "4"
        time.sleep(2)
        setup_perfectoMobile[0].execute_script('mobile:touch:swipe', params2)
        time.sleep(1)

    def scroll_up(self, setup_perfectoMobile):
        print("Scroll up")
        setup_perfectoMobile[1].step_start("Scroll up")
        params2 = {}
        params2["start"] = "50%,20%"
        params2["end"] = "50%,80%"
        params2["duration"] = "2"
        time.sleep(1)
        setup_perfectoMobile[0].execute_script('mobile:touch:swipe', params2)
        time.sleep(1)

    def getDeviceID(self, setup_perfectoMobile):
        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]

        report.step_start("Get DeviceID")
        params = {'property': 'deviceId'}
        deviceID = driver.execute_script('mobile:handset:info', params)
        print("DeviceID: " + deviceID)
        return deviceID

    def getDeviceModelName(self, setup_perfectoMobile):
        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]

        report.step_start("Device Model Name")
        params = {'property': 'model'}
        deviceModel = driver.execute_script('mobile:handset:info', params)
        print("ModelName: " + deviceModel)
        return deviceModel

    def get_phone_information(self, setup_perfectoMobile, search_this):
        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]

        report.step_start("Get DeviceID")
        params = {'property': search_this}
        device_information = driver.execute_script('mobile:handset:info', params)
        print("device information for " + search_this + " is: ", device_information)
        return device_information

    def setup_perfectoMobile_android(self):
        global perfecto_execution_context, driver
        driver = None
        reporting_client = None
        get_device_configuration = self.get_device_configuration()
        print("Device CONFIG:", get_device_configuration)
        warnings.simplefilter("ignore", ResourceWarning)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        capabilities = {
            'platformName': get_device_configuration["platformName-android"],
            'model': get_device_configuration["model-android"],
            'browserName': 'mobileOS',
            # 'automationName' : 'Appium',
            'securityToken': self.perfecto_data["securityToken"],
            'useAppiumForWeb': 'false',
            'useAppiumForHybrid': 'false',
            # 'bundleId' : request.config.getini("appPackage-android"),
        }

        if not self.is_device_Available_timeout(capabilities['model']):
            print("Unable to get device.")
            pytest.exit("Exiting Pytest")
        driver = webdriver.Remote(
            'https://' + self.perfecto_data["perfectoURL"] + '.perfectomobile.com/nexperience/perfectomobile/wd/hub',
            capabilities)
        driver.implicitly_wait(2)

        # TestCaseFullName = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
        # nCurrentTestMethodNameSplit = re.sub(r'\[.*?\]\ *', "", TestCaseFullName)
        # try:
        #     # TestCaseName = nCurrentTestMethodNameSplit.removeprefix('test_')
        #     TestCaseName = nCurrentTestMethodNameSplit.replace('test_', '')
        #     print("\n\nExecuting TestCase: " + TestCaseName)
        # except Exception as e:
        #     TestCaseName = nCurrentTestMethodNameSplit
        #     print("\nUpgrade Python to 3.9 to avoid test_ string in your test case name, see below URL")
        #     # print("https://www.andreagrandi.it/2020/10/11/python39-introduces-removeprefix-removesuffix/")

        projectname = self.perfecto_data["projectName"]
        projectversion = self.perfecto_data["projectVersion"]
        jobname = get_device_configuration["jobName"]
        jobnumber = get_device_configuration["jobNumber"]
        tags = self.perfecto_data["reportTags"]
        testCaseName = "TestCaseName_Hari_check"
        print("-----------------------------------------------")
        print(projectname, projectversion, jobnumber, jobname, tags)
        print("-----------------------------------------------")
        # print("\nSetting Perfecto ReportClient....")
        perfecto_execution_context = PerfectoExecutionContext(driver, tags, Job(jobname, jobnumber),
                                                              Project(projectname, projectversion))
        reporting_client = PerfectoReportiumClient(perfecto_execution_context)
        reporting_client.test_start(testCaseName, TestContext([], "Perforce"))
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

    def teardown(self):
        global driver, perfecto_execution_context
        reporting_client = PerfectoReportiumClient(perfecto_execution_context)
        try:
            print("\n---------- Tear Down ----------")
            try:
                params = {'property': 'model'}
                deviceModel = driver.execute_script('mobile:handset:info', params)
                allure.dynamic.link(
                    str(reporting_client.report_url()),
                    name=str(deviceModel))
            except:
                print("fail to attach video link")

            print('Report-Url: ' + reporting_client.report_url())

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

    # ------------------Functions related to perfecto Android libs such as Wifi connect, Get IP address, Forget Wifi----
    def wifi_connect(self, ssid, passkey, setup_perfectoMobile, connData):
        print("\n-------------------------------------")
        print("Select Wifi/AccessPoint Connection")
        print("-------------------------------------")
        print("Verifying Wifi Connection Details....")
        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]

        # ip_address_element_text = False
        ssid_with_internet = False
        wifi_name = ssid

        report.step_start("Switching Driver Context")
        print("Switching Context to Native")
        contexts = driver.contexts
        driver.switch_to.context(contexts[0])

        # Open Settings Application
        self.openApp(connData["appPackage-android"], setup_perfectoMobile)
        device_model_name = self.getDeviceModelName(setup_perfectoMobile)
        print("Selected Device Model: " + device_model_name)

        if device_model_name != "Pixel 4":
            logging.info("Selected Model is not Pixel 4")
            report.step_start("Set Wifi Network to " + wifi_name)

            # -----------------To Open Connections page-----------------------
            try:
                print("Verifying Connected Wifi Connection")
                logging.info("Verifying Connected Wifi Connection")
                report.step_start("Click Connections")
                conn_element = driver.find_element_by_xpath("//*[@text='Connections']")
                conn_element.click()

                # ---------------------Open WIFI page-------------------------------
                try:
                    report.step_start("Clicking Wi-Fi")
                    print("Clicking WIFI")
                    logging.info("Clicking WIFI")
                    time.sleep(3)
                    wifi_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='Wi-Fi']")))
                    wifi_element.click()

                    # --------------------To Turn on WIFi Switch if already OFF--------------------------------
                    try:
                        driver.implicitly_wait(1)
                        get_switch_text_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/switch_text']")
                        get_switch_text = get_switch_text_element.text
                        print("get_switch_text: ", get_switch_text)
                        print("Find wifi switch")
                        logging.info("Find wifi switch")
                        try:  # To Turn on Wi-Fi Switch
                            if get_switch_text == "Off":
                                # driver.implicitly_wait(3)
                                get_switch_element = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/switch_widget']")
                                driver.implicitly_wait(1)
                                get_switch_element.click()
                                driver.implicitly_wait(1)
                                i = 0
                                for i in range(5):
                                    if get_switch_text == "On":
                                        print("WIFI Switch is ON")
                                        break
                                    else:
                                        try:
                                            get_switch_text_element = driver.find_element_by_xpath(
                                                "//*[@resource-id='com.android.settings:id/switch_text']")
                                            get_switch_text = get_switch_text_element.text
                                        except:
                                            pass
                                        print("Sleeping for: ", i)
                                        time.sleep(i)
                                        pass
                                if get_switch_text == "Off":
                                    print("Switch is Still OFF")
                                    self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                    return ssid_with_internet, setup_perfectoMobile
                            else:
                                print("Switch is already On")
                                logging.info("Switch is already On")
                                # self.check_if_no_internet_popup(driver)
                        except:
                            print("Couldn't turn on WIFI switch")
                            logging.error("Couldn't turn on WIFI switch")
                            self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            return ssid_with_internet, setup_perfectoMobile
                    except:
                        print("No Switch element found")
                        logging.error("No Switch element found")
                    # ---------------------This is to Forget current connected SSID-------------------------------
                    if self.get_phone_information(setup_perfectoMobile,
                                                  search_this="osVersion") != "12":
                        print("Trying to forget already connected ssid in Device OS-version=!12")
                        try:  # To deal with already connected SSID
                            self.check_if_no_internet_popup(driver)
                            network_category = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/connected_network_category']")
                            try:  # To forget existing ssid
                                print("To forget ssid")
                                logging.info("To forget ssid")
                                self.check_if_no_internet_popup(driver)
                                additional_details_element = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/layout_details']")
                                additional_details_element.click()
                                try:
                                    self.check_if_no_internet_popup(driver)
                                    forget_ssid = driver.find_element_by_xpath(
                                        "//*[@resource-id='com.android.settings:id/forget_button']//"
                                        "*[@resource-id='com.android.settings:id/icon']")
                                    forget_ssid.click()
                                    print("Forget old ssid")
                                    logging.info("Forget old ssid")
                                except:
                                    print("Couldn't forget ssid")
                                    logging.error("Couldn't forget ssid")
                                    self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                    return ssid_with_internet, setup_perfectoMobile
                            except:
                                print("Couldn't get into additional details")
                                logging.error("Couldn't get into additional details")
                        except:
                            print("No Connected SSIDS")
                            logging.warning("No Connected SSIDS")
                    else:
                        print("Trying to forget already connected ssid in Device OS-version=12")
                        try:  # To deal with already connected SSID
                            self.check_if_no_internet_popup(driver)
                            network_category = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/connected_list']/android.widget."
                                "LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]"
                                "/android.widget.RelativeLayout[2]")
                            try:  # To forget existing ssid
                                print("To forget ssid in OS-Version 12")
                                logging.info("To forget ssid in OS-Version 12")
                                self.check_if_no_internet_popup(driver)
                                additional_details_element = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/wifi_details']")
                                additional_details_element.click()
                                try:
                                    print("To forget ssid in OS-Version 12")
                                    self.check_if_no_internet_popup(driver)
                                    forget_ssid = driver.find_element_by_xpath(
                                        "//*[@resource-id='com.android.settings:id/forget_button']//"
                                        "*[@resource-id='com.android.settings:id/navigation_bar_item_icon_view']")
                                    forget_ssid.click()
                                    print("Forgot old ssid")
                                    logging.info("Forgot old ssid")
                                except:
                                    print("Couldn't forget ssid")
                                    logging.error("Couldn't forget ssid")
                                    self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                    return ssid_with_internet, setup_perfectoMobile
                            except:
                                print("Couldn't get into additional details")
                                logging.error("Couldn't get into additional details")
                        except:
                            print("No Connected SSIDS")
                            logging.warning("No Connected SSIDS")
                    # ----------------------This is to Forget current connected SSID--------------------------------

                    # time.sleep(2)
                    print("Selecting Wifi: " + wifi_name)
                    logging.info("Selecting SSID")
                    # allure.attach(name= body=str("Selecting Wifi: " + wifi_name))
                    ssid_found = False
                    available_ssids = False
                    # This is To get all available ssids
                    # ------------------------------------------------------
                    try:
                        for k in range(9):
                            available_ssids = self.get_all_available_ssids(driver, device_model_name)
                            print("active_ssid_list: ", available_ssids)
                            logging.info("Available Ssids:", available_ssids)
                            allure.attach(name="Available SSIDs in device: ", body=str(available_ssids))
                            try:
                                if wifi_name not in available_ssids:
                                    self.scrollDown(driver)
                                    time.sleep(2)
                                else:
                                    ssid_found = True
                                    print(wifi_name + " : Found in Device")
                                    # allure.attach(name= body=str(wifi_name+" : Found in Device"))
                                    break
                            except:
                                print("couldn't find wifi in available ssid")
                                logging.error("couldn't find wifi in available ssid")
                        if not ssid_found:
                            print("could not found " + wifi_name + " in device")
                            logging.error("Couldn't find the SSID")
                            # allure.attach(name= body=str("could not found" + wifi_name + " in device"))
                            self.closeApp(connData["appPackage-android"], setup_perfectoMobile)

                            return ssid_with_internet, setup_perfectoMobile
                    except:
                        self.closeApp(connData["appPackage-android"], setup_perfectoMobile)

                        return ssid_with_internet, setup_perfectoMobile
                    # -------------------------------------------------------

                    # Selecting WIFI
                    # -------------------------------------------------------
                    try:
                        report.step_start("Selecting Wifi: " + wifi_name)
                        print("Clicking WIFI")
                        logging.info("Clicking SSID")
                        wifi_selection_element = WebDriverWait(driver, 35).until(
                            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='" + wifi_name + "']")))
                        wifi_selection_element.click()
                        self.check_if_no_internet_popup(driver)
                    except Exception as e:
                        print("Exception on Selecting Wifi Network.  Please check wifi Name or signal")
                        logging.error("Exception on Selecting Wifi Network.  Please check wifi Name or signal")
                        # request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                        self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        return ssid_with_internet, setup_perfectoMobile
                    # -------------------------------------------------------

                    # Set password if Needed
                    # -------------------------------------------------------
                    try:
                        self.check_if_no_internet_popup(driver)
                        time.sleep(3)
                        report.step_start("Set Wifi Password")
                        print("Set Wifi password")
                        logging.info("Set Wifi password")
                        passkeywordElement = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/edittext']")
                        passkeywordElement.send_keys(passkey)
                    except NoSuchElementException:
                        print("Password Page Not Loaded, password May be cached in the System")
                        logging.error("Password Page Not Loaded, password May be cached in the System")
                    self.check_if_no_internet_popup(driver)
                    # -------------------------------------------------------

                    # Click on connect button
                    # -------------------------------------------------------
                    try:
                        time.sleep(5)
                        report.step_start("Click Connect Button")
                        print("Click Connect")
                        logging.info("Click Connect")
                        joinBTNElement = driver.find_element_by_xpath("//*[@text='Connect']")
                        joinBTNElement.click()
                    except NoSuchElementException:
                        print("Connect Button Not Enabled...Verify if Password is set properly")
                        logging.error("Connect Button Not Enabled...Verify if Password is set properly")
                    self.check_if_no_internet_popup(driver)
                    # -------------------------------------------------------

                    # Verify if WiFi is connected
                    # -------------------------------------------------------
                    if self.get_phone_information(setup_perfectoMobile,
                                                  search_this="osVersion") != "12":
                        try:
                            report.step_start("Verify if Wifi is Connected")
                            logging.info("Verify if Wifi is Connected")
                            WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH,
                                                                "//*[@resource-id='android:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + wifi_name + "']")))
                            ssid_with_internet = True
                            print("Wifi Successfully Connected")
                            logging.info("Wifi Successfully Connected")
                            # time.sleep(5)
                            self.check_if_no_internet_popup(driver)
                        except:
                            try:
                                self.check_if_no_internet_popup(driver)
                                WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                                    EC.presence_of_element_located((MobileBy.XPATH,
                                                                    "//*[@resource-id='com.android.settings:id"
                                                                    "/summary' and @text='Connected without internet']"
                                                                    "/parent::*/android.widget.TextView[@text='"
                                                                    + wifi_name + "']")))
                                print("Wifi Successfully Connected without internet")
                                logging.info("Wifi Successfully Connected without internet")
                                self.check_if_no_internet_popup(driver)
                            except:
                                try:
                                    report.step_start("Verify if Wifi is Connected - 2")
                                    WifiInternetErrMsg = WebDriverWait(driver, 60).until(
                                        EC.presence_of_element_located((
                                            MobileBy.XPATH,
                                            "//*[@resource-id='com.android.settings:id/summary' and "
                                            "@text='Connected']/parent::*/android.widget.TextView[@text='" + wifi_name + "']")))
                                    ssid_with_internet = True
                                    print("Wifi Successfully Connected")
                                    logging.info("Wifi Successfully Connected")
                                except NoSuchElementException:
                                    print("Wifi Connection Error: " + wifi_name)
                                    logging.error("Wifi Connection Error")
                                    self.closeApp(connData["appPackage-android"], setup_perfectoMobile)

                                    return ssid_with_internet, setup_perfectoMobile
                    else:
                        try:
                            report.step_start(
                                "Verifying wifi connection status connected/connected without internet")
                            self.check_if_no_internet_popup(driver)
                            self.check_if_no_internet_popup(driver)

                            wifi_connection_name = WebDriverWait(driver, 50).until(
                                EC.presence_of_element_located((MobileBy.XPATH,
                                                                "//*[@resource-id='com.android.settings"
                                                                ":id/connected_list']/android.widget.LinearLayout[1]"
                                                                "/android.widget.LinearLayout[1]/android.widget."
                                                                "LinearLayout[1]/android.widget.RelativeLayout[2]/"
                                                                "android.widget.TextView[1]"
                                                                )))
                            if wifi_connection_name.text == wifi_name:
                                wifi_connection_status = WebDriverWait(driver, 50).until(
                                    EC.presence_of_element_located((MobileBy.XPATH,
                                                                    "//*[@resource-id='com.android.settings:id/summary']"
                                                                    )))
                                if wifi_connection_status.text == "Connected":
                                    ssid_with_internet = True
                                    print("Connected with internet")
                                    logging.info("Connected with internet")

                                else:
                                    ssid_with_internet = False
                                    print("Wifi Successfully Connected without internet")
                                    logging.info("Wifi Successfully Connected without internet")
                                    self.check_if_no_internet_popup(driver)
                                # Go into additional details here
                            else:
                                # Connected to some other wifi, makes sense to close app and fail this testcase
                                logging.error("Connected to some other wifi")
                                self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                return ssid_with_internet, setup_perfectoMobile
                        except:
                            self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            return ssid_with_internet, setup_perfectoMobile

                    # ---------------------To Turn on WIFi Switch if already OFF-------------------------------

                except:
                    print("Couldn't find wifi Button")
                    logging.error("Couldn't find wifi Button")
                # ------------------Open WIFI page----------------------------------

            except:
                print("Exception: Verify Xpath - Update/check Xpath for Click Connections")
                logging.error("Exception: Verify Xpath - Update/check Xpath for Click Connections")
            # -----------------To Open Connections page---------------------------
        # --------------------Pixel 4 code---------------------------
        else:
            report.step_start("Set Wifi Network to " + wifi_name)

            # -----------------To Open Connections page-----------------------
            try:
                print("Verifying Connected Wifi Connection")
                report.step_start("Click Network & internet in pixel4")
                conn_element = driver.find_element_by_xpath("//*[@text='Network & internet']")
                conn_element.click()
                # ---------------------Open WIFI page-------------------------------
                try:
                    report.step_start("Clicking Wi-Fi")
                    print("Clicking WIFI")
                    time.sleep(3)
                    wifi_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='Wi‑Fi']")))
                    wifi_element.click()

                    # --------------------To Turn on WIFi Switch if already OFF--------------------------------
                    try:
                        driver.implicitly_wait(1)
                        get_switch_text_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/switch_widget']")
                        get_switch_text = get_switch_text_element.text
                        # if get_switch_text is not None:
                        #     switch_text = "OFF"
                        # else:
                        #     switch_text = "ON"
                        switch_text = get_switch_text
                        print("get_switch_text: ", switch_text)
                        print("Find wifi switch")
                        try:  # To Turn on Wi-Fi Switch
                            if switch_text == "OFF":
                                # driver.implicitly_wait(3)
                                get_switch_element = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/switch_widget']")
                                driver.implicitly_wait(1)
                                get_switch_element.click()
                                driver.implicitly_wait(1)
                                i = 0
                                for i in range(5):
                                    if switch_text == "ON":
                                        print("WIFI Switch is ON")
                                        break
                                    else:
                                        try:
                                            get_switch_text_element = driver.find_element_by_xpath(
                                                "//*[@text='Add network']")
                                            get_switch_text = get_switch_text_element.text
                                            if get_switch_text == "Add network":
                                                switch_text = "ON"
                                            else:
                                                switch_text = "OFF"
                                        except NoSuchElementException:
                                            print("Exception: Verify Xpath")
                                        # Scroll Down
                                        self.scrollDown(driver)
                                        print("Sleeping for: ", i)
                                        time.sleep(i)
                                        pass
                                if switch_text == "OFF":
                                    print("Switch is Still OFF")
                                    self.closeApp(connData["appPackage-android"], setup_perfectoMobile)

                                    return ssid_with_internet, setup_perfectoMobile
                            else:
                                print("Switch is already On")
                                self.check_if_no_internet_popup(driver)
                        except:
                            print("Couldn't turn on WIFI switch")
                            self.closeApp(connData["appPackage-android"], setup_perfectoMobile)

                            return ssid_with_internet, setup_perfectoMobile

                        # ---------------------This is to Forget current connected SSID-------------------------------
                        try:  # To deal with already connected SSID
                            self.check_if_no_internet_popup(driver)
                            network_category = driver.find_element_by_xpath("//*[@text='Connected']")
                            try:  # To forget existing ssid
                                print("To forget ssid")
                                self.check_if_no_internet_popup(driver)
                                additional_details_element = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/settings_button_no_background']")
                                additional_details_element.click()
                            except:
                                print("Couldn't get into additional details")
                            try:
                                self.check_if_no_internet_popup(driver)
                                forget_ssid = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/button1']")
                                forget_ssid.click()
                                print("Forget old ssid")
                            except:
                                print("Couldn't forget ssid")
                                self.closeApp(connData["appPackage-android"], setup_perfectoMobile)

                                return ssid_with_internet, setup_perfectoMobile
                        except:
                            print("No Connected SSIDS")
                        # ----------------------This is to Forget current connected SSID--------------------------------

                        time.sleep(2)
                        print("Selecting Wifi: " + wifi_name)
                        # allure.attach(name= body=str("Selecting Wifi: " + wifi_name))
                        ssid_found = False
                        available_ssids = False
                        # This is To get all available ssids
                        # ------------------------------------------------------
                        try:
                            for k in range(5):
                                available_ssids = self.get_all_available_ssids(driver, device_model_name)
                                print("active_ssid_list: ", available_ssids)
                                allure.attach(name="Available SSIDs in device: ", body=str(available_ssids))
                                try:
                                    if wifi_name not in available_ssids:
                                        self.scrollDown(driver)
                                        time.sleep(2)
                                    else:
                                        ssid_found = True
                                        print(wifi_name + " : Found in Device")
                                        # allure.attach(name= body=str(wifi_name+" : Found in Device"))
                                        break
                                except:
                                    print("couldn't find wifi in available ssid")
                            if not ssid_found:
                                ssid_not_found = False
                                for k in range(5):
                                    available_ssids = self.get_all_available_ssids(driver, device_model_name)
                                    print("active_ssid_list: ", available_ssids)
                                    allure.attach(name="Available SSIDs in device: ", body=str(available_ssids))
                                    try:
                                        if wifi_name not in available_ssids:
                                            self.scroll_up(driver)
                                            time.sleep(2)
                                        else:
                                            ssid_not_found = True
                                            print(wifi_name + " : Found in Device")
                                            # allure.attach(name= body=str(wifi_name+" : Found in Device"))
                                            break
                                    except:
                                        print("couldn't find wifi in available ssid")
                                if not ssid_not_found:
                                    print("could not found " + wifi_name + " in device")
                                    # allure.attach(name= body=str("could not found" + wifi_name + " in device"))
                                    self.closeApp(connData["appPackage-android"], setup_perfectoMobile)

                                    return ssid_with_internet, setup_perfectoMobile
                        except:
                            self.closeApp(connData["appPackage-android"], setup_perfectoMobile)

                            return ssid_with_internet, setup_perfectoMobile
                        # -------------------------------------------------------

                        # Selecting WIFI
                        # -------------------------------------------------------
                        try:
                            report.step_start("Selecting Wifi: " + wifi_name)
                            wifi_selection_element = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='" + wifi_name + "']")))
                            wifi_selection_element.click()
                            self.check_if_no_internet_popup(driver)
                        except Exception as e:
                            print("Exception on Selecting Wifi Network.  Please check wifi Name or signal")
                            # request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                            self.closeApp(connData["appPackage-android"], setup_perfectoMobile)

                            return ssid_with_internet, setup_perfectoMobile
                        # -------------------------------------------------------

                        # Set password if Needed
                        # -------------------------------------------------------
                        try:
                            time.sleep(3)
                            self.check_if_no_internet_popup(driver)
                            report.step_start("Set Wifi Password")
                            print("Entering password")
                            passkeywordElement = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/password']")
                            passkeywordElement.send_keys(passkey)
                        except NoSuchElementException:
                            print("Password Page Not Loaded, password May be cached in the System")
                        self.check_if_no_internet_popup(driver)
                        # -------------------------------------------------------

                        # Click on connect button
                        # -------------------------------------------------------
                        try:
                            report.step_start("Click Connect Button")
                            time.sleep(5)
                            joinBTNElement = driver.find_element_by_xpath("//*[@text='Connect']")
                            joinBTNElement.click()
                        except NoSuchElementException:
                            print("Connect Button Not Enabled...Verify if Password is set properly  ")
                        self.check_if_no_internet_popup(driver)
                        # -------------------------------------------------------

                        # Verify if WiFi is connected
                        # -------------------------------------------------------
                        try:
                            report.step_start("Verify if Wifi is Connected")
                            WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                                EC.presence_of_element_located((MobileBy.XPATH,
                                                                "//*[@resource-id='android:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + wifi_name + "']")))
                            ssid_with_internet = True
                            print("Wifi Successfully Connected")
                            # time.sleep(5)
                            self.check_if_no_internet_popup(driver)
                        except:
                            try:
                                print("Not able to verify the connected WiFi. Scrolling up.")
                                self.scroll_up(driver)
                                self.scroll_up(driver)
                                # self.check_if_no_internet_popup(driver)
                                WifiInternetErrMsg = WebDriverWait(driver, 35).until(
                                    EC.presence_of_element_located((MobileBy.XPATH,
                                                                    "//*[@resource-id='com.android.settings:id/summary' and @text='Connected without internet']/parent::*/android.widget.TextView[@text='" + wifi_name + "']")))
                                print("Wifi Successfully Connected without internet")
                                self.check_if_no_internet_popup(driver)
                            except:
                                try:
                                    report.step_start("Verify if Wifi is Connected")
                                    print("Verifying after scrolling")
                                    self.scroll_up(driver)
                                    WifiInternetErrMsg = WebDriverWait(driver, 60).until(
                                        EC.presence_of_element_located((
                                            MobileBy.XPATH,
                                            "//*[@resource-id='android:id/summary' and @text='Connected']/parent::*/android.widget.TextView[@text='" + wifi_name + "']")))
                                    ssid_with_internet = True
                                    print("Wifi Successfully Connected")
                                except NoSuchElementException:
                                    print("Wifi Connection Error: " + wifi_name)
                                    self.closeApp(connData["appPackage-android"], setup_perfectoMobile)

                                    return ssid_with_internet, setup_perfectoMobile
                        # -------------------------------------------------------
                    except:
                        print("No Switch element found")
                    # ---------------------To Turn on WIFi Switch if already OFF-------------------------------

                except:
                    print("Couldn't find wifi Button")
                # ------------------Open WIFI page----------------------------------

            except:
                print("Exception: Verify Xpath - Update/check Xpath for Click Connections")
            # -----------------To Open Connections page---------------------------

        # self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
        return ssid_with_internet, setup_perfectoMobile

    def get_ip_address(self, ssid, setup_perfectoMobile, connData):
        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]
        device_model_name = self.getDeviceModelName(setup_perfectoMobile)
        print("Selected Device Model: " + device_model_name)

        if device_model_name != "Pixel 4":
            logging.info("Selected Model is not Pixel 4")
            report.step_start("Getting IP address")
        # Get into Additional Details
        # To Get an IP Address
        # -------------------------------------------------------
            if self.get_phone_information(setup_perfectoMobile,
                                          search_this="osVersion") != "12":
                try:
                    print("Into additional details")
                    logging.info("Into additional details")
                    time.sleep(2)
                    additional_details_element = driver.find_element_by_xpath(
                        "//*[@resource-id='com.android.settings:id/layout_details']")
                    additional_details_element.click()
                    try:
                        time.sleep(2)
                        ip_address_element = driver.find_element_by_xpath(
                            "//*[@text='IP address']/parent::*/android.widget."
                            "TextView[@resource-id='com.android.settings:id/summary']")
                        ip_address_element_text = ip_address_element.text
                        print("Device IP address is :", ip_address_element_text)
                    except:
                        try:
                            time.sleep(2)
                            ip_address_element = driver.find_element_by_xpath(
                                "//*[@text='IP address']/parent::*/android.widget."
                                "TextView[@resource-id='android:id/summary']")
                            ip_address_element_text = ip_address_element.text
                            print("Device IP address is :", ip_address_element_text)
                        except:
                            print("IP address element not found")
                            logging.error("IP address element not found")
                            self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            assert False
                    # --------------------Added for ssid security check--------------------------
                    try:
                        time.sleep(2)
                        security_name_element = driver.find_element_by_xpath(
                            "//*[@text='Security']/parent::*/android.widget."
                            "TextView[@resource-id='com.android.settings:id/summary']")
                        security_name_element_text = security_name_element.text
                        print("Ssid security is :", security_name_element_text)
                        allure.attach(name="Ssid Security:", body=str(security_name_element_text))
                    except:
                        print("Security is not available")
                        logging.error("Security is not available")
                    # --------------------Added for ssid Name check--------------------------
                    try:
                        time.sleep(2)
                        ssid_name_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/entity_header_title']")
                        ssid_name_element_text = ssid_name_element.text
                        print("Ssid Name is :", ssid_name_element_text)
                        allure.attach(name="Ssid connected:", body=str(ssid_name_element_text))
                    except:
                        print("Ssid name not available")
                        logging.error("Ssid name not available")
                        self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        assert False
                    if ssid_name_element_text == ssid:
                        print("Wifi is connected to the expected ssid")
                        logging.info("Wifi is connected to the expected ssid")
                    else:
                        print("Wifi is not connected to the expected ssid")
                        logging.error("Wifi is not connected to the expected ssid")
                        self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                        assert False
                    try:
                        self.check_if_no_internet_popup(driver)
                        driver.implicitly_wait(3)
                        time.sleep(2)
                        auto_reconnect_off = driver.find("//*[@resource-id='android:id/switch_widget']")
                        auto_reconnect_off_text = auto_reconnect_off.text
                        if auto_reconnect_off_text != "Off":
                            auto_reconnect_off.click()
                            print("Auto reconnect turning off")
                            logging.info("Auto reconnect turning off")
                        else:
                            print("Auto reconnect is already off")
                            logging.info("Auto reconnect is already off")
                    except:
                        print("Couldn't find auto reconnect element")
                        logging.error("Couldn't find auto reconnect element")

                    # ------------------------------- Forget SSID ----------------
                    try:
                        self.check_if_no_internet_popup(driver)
                        forget_ssid = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/forget_button']//"
                            "*[@resource-id='com.android.settings:id/icon']")
                        forget_ssid.click()
                        print("Forgetting ssid")
                        logging.info("Forgetting ssid")
                    except:
                        print("Couldn't forget ssid")
                        logging.error("Couldn't forget ssid")
                except:
                    print("Couldn't get into Additional settings")
                    logging.error("Couldn't get into Additional settings")
                # -------------------------------------------------------
            else:
                try:
                    print("Into additional details")
                    logging.info("Into additional details")
                    time.sleep(2)
                    additional_details_element = driver.find_element_by_xpath(
                        "//*[@resource-id='com.android.settings:id/wifi_details']")
                    additional_details_element.click()

                    try:
                        print("click on view more")
                        logging.info("click on view more")
                        additional_details_element = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='View more']")))
                        additional_details_element.click()
                    except:
                        pass

                    try:
                        time.sleep(2)
                        ssid_name_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/entity_header_title']")
                        ssid_name_element_text = ssid_name_element.text
                        print("Ssid Name is :", ssid_name_element_text)
                        allure.attach(name="Ssid connected:", body=str(ssid_name_element_text))
                    except:
                        print("Ssid name not available")
                        logging.error("Ssid name not available")
                        pass

                    if (ssid_name_element_text == ssid):
                        print("Wifi is connected to the expected ssid")
                        logging.info("Wifi is connected to the expected ssid")
                        ip_address_element_text = "SSID Match, S20 Does Not support scrolling"
                        ssid_with_internet = "SSID Match, S20 Does Not support scrolling"
                        # return ssid_with_internet
                    else:
                        print("Wifi is not connected to the expected ssid")
                        self.closeApp(connData["appPackage-android"], setup_perfectoMobile)

                    report.step_start("Scrolling for ip address - 1")
                    # if device_model_name == "Galaxy S20":
                    #     print("Scrolling for S20")
                    driver.swipe(470, 1400, 470, 1000, 400)
                    # else:
                    #     self.scrollDown(driver)

                    report.step_start("Scrolling for ip address - 2")
                    # if device_model_name == "Galaxy S20":
                    #     print("Scrolling for S20")
                    driver.swipe(470, 1400, 470, 1000, 400)
                    # else:
                    #     self.scrollDown(driver)

                    report.step_start("Scrolling for ip address - 3")
                    # if device_model_name == "Galaxy S20":
                    #     print("Scrolling for S20")
                    driver.swipe(470, 1400, 470, 1000, 400)
                    # else:
                    #     self.scrollDown(driver)
                    report.step_start("looking for ip address")

                    try:
                        ip_address_element_text = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/recycler_view']/"
                            "android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]/"
                            "android.widget.TextView[2]")
                        ip_address_element_text = ip_address_element_text.text

                    except:
                        print("Unable to get IP address")
                        logging.error("Unable to get IP address")
                except:
                    print("Couldn't get into Additional settings")
                    logging.error("Couldn't get into Additional settings")
                # -------------------------------------------------------
        # ----------------Pixel 4 code------------
        else:
            # -------------------------------------------------------

            # Get into Additional Details
            # To Get an IP Address
            # -------------------------------------------------------
            try:
                print("Into additional details")
                time.sleep(5)
                report.step_start("Going for ip address")
                additional_details_element = driver.find_element_by_xpath(
                    "//*[@resource-id='com.android.settings:id/settings_button_no_background']")
                additional_details_element.click()
                print("Entered ssid")
                try:
                    time.sleep(10)
                    print("clicking Advanced")
                    report.step_start("clicking Advanced")
                    advanced_element = driver.find_element_by_xpath("//*[@text='Advanced']")
                    advanced_element.click()
                    print("clicked Advanced")
                    # print("Device IP address is :", ip_address_element_text)
                except:
                    try:
                        time.sleep(5)
                        print("clicking Advanced2")
                        advanced_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/recycler_view']/android.widget."
                            "FrameLayout[2]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]")
                        advanced_element.click()
                        # print("Device IP address is :", ip_address_element_text)
                    except:
                        try:
                            time.sleep(5)
                            print("clicking Advanced2")
                            advanced_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/recycler_view']/android.widget."
                                "LinearLayout[5]/android.widget.LinearLayout[1]/android.widget.ImageView[1]")
                            advanced_element.click()
                        except:
                            print("No advanced options")
                # Scroll Down
                self.scrollDown(driver)
                try:
                    time.sleep(2)
                    ip_address_element = driver.find_element_by_xpath(
                        "//*[@text='IP address']/parent::*/android.widget.TextView[@resource-id='android:id/summary']")
                    ip_address_element_text = ip_address_element.text
                    print("Device IP address is :", ip_address_element_text)
                except:
                    print("IP address element not found")
                # ------------------------------- Forget SSID ----------------
                # try:
                #     self.check_if_no_internet_popup(driver)
                #     forget_ssid = driver.find_element_by_xpath(
                #         "//*[@resource-id='com.android.settings:id/settings_button_no_background']")
                #     forget_ssid.click()
                #     print("Forgetting ssid")
                #
                #     # ------------------------------- Wifi Switch ----------------
                #     try:
                #         print("clicking on wifi switch")
                #         get_switch_element = driver.find_element_by_xpath(
                #             "//*[@resource-id='com.android.settings:id/switch_widget']")
                #         driver.implicitly_wait(2)
                #         get_switch_element.click()
                #     except:
                #         print("couldn't click on wifi switch")
                #     # allure.attach(name= body=str("couldn't click on wifi switch"))
                # except:
                #     print("Couldn't forget ssid")
                #     self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                #     return ssid_with_internet
            except:
                print("Couldn't get into Additional settings")
        return ip_address_element_text

    def wifi_disconnect(self, ssid, setup_perfectoMobile, connData):
        print("\n-------------------------------------")
        print("WIFI Disconnect")
        print("-------------------------------------")
        # allure.attach(name= body=str("------------------- WIFI Disconnect ------------------"))

        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]

        report.step_start("Switching Driver Context")
        print("Switching Context to Native")
        contexts = driver.contexts
        driver.switch_to.context(contexts[0])

        # Open Settings Application
        self.openApp(connData["appPackage-android"], setup_perfectoMobile)
        device_model_name = self.getDeviceModelName(setup_perfectoMobile)
        print("Selected Device Model: " + device_model_name)

        if device_model_name != "Pixel 4":
            report.step_start("Set Wifi Network to " + ssid)

            # -----------------To Open Connections page-----------------------
            try:
                print("Verifying Connected Wifi Connection")
                report.step_start("Click Connections")
                conn_element = driver.find_element_by_xpath("//*[@text='Connections']")
                conn_element.click()

                # ---------------------Open WIFI page-------------------------------
                try:
                    report.step_start("Clicking Wi-Fi")
                    print("Clicking WIFI")
                    wifi_element = driver.find_element_by_xpath("//*[@text='Wi-Fi']")
                    wifi_element.click()

                    # --------------------To Turn on WIFi Switch if already OFF--------------------------------
                    try:
                        driver.implicitly_wait(1)
                        get_switch_text_element = driver.find_element_by_xpath(
                            "//*[@resource-id='com.android.settings:id/switch_text']")
                        get_switch_text = get_switch_text_element.text
                        print("get_switch_text: ", get_switch_text)
                        print("Find wifi switch")
                        try:  # To Turn on Wi-Fi Switch
                            if get_switch_text == "Off":
                                # driver.implicitly_wait(3)
                                get_switch_element = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/switch_widget']")
                                driver.implicitly_wait(1)
                                get_switch_element.click()
                                driver.implicitly_wait(1)
                                i = 0
                                for i in range(5):
                                    if get_switch_text == "On":
                                        print("WIFI Switch is ON")
                                        break
                                    else:
                                        try:
                                            get_switch_text_element = driver.find_element_by_xpath(
                                                "//*[@resource-id='com.android.settings:id/switch_text']")
                                            get_switch_text = get_switch_text_element.text
                                        except:
                                            pass
                                        print("Sleeping for: ", i)
                                        time.sleep(i)
                                        pass
                                if get_switch_text == "Off":
                                    print("Switch is Still OFF")
                                    self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            else:
                                print("Switch is already On")
                                self.check_if_no_internet_popup(driver)
                        except:
                            print("Couldn't turn on WIFI switch")
                            self.closeApp(connData["appPackage-android"], setup_perfectoMobile)

                        # ---------------------This is to Forget current connected SSID-------------------------------
                        if self.get_phone_information(setup_perfectoMobile,
                                                      search_this="osVersion") != "12":
                            try:  # To deal with already connected SSID
                                self.check_if_no_internet_popup(driver)
                                network_category = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/connected_network_category']")
                                try:  # To forget exhisting ssid
                                    print("To forget ssid")
                                    self.check_if_no_internet_popup(driver)
                                    additional_details_element = driver.find_element_by_xpath(
                                        "//*[@resource-id='com.android.settings:id/layout_details']")
                                    additional_details_element.click()
                                    try:
                                        self.check_if_no_internet_popup(driver)
                                        forget_ssid = driver.find_element_by_xpath(
                                            "//*[@resource-id='com.android.settings:id/forget_button']//*[@resource-id='com.android.settings:id/icon']")
                                        forget_ssid.click()
                                        print("Forget old ssid")
                                    # allure.attach(name=body=str("Forget old ssid"))
                                    except:
                                        print("Couldn't forget ssid")
                                        # allure.attach(name=body=str("Couldn't forget ssid"))
                                        self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                except:
                                    # allure.attach(name=body=str("Couldn't get into additional details"))
                                    print("Couldn't get into additional details")
                            except:
                                # allure.attach(name=body=str("No Connected SSIDS"))
                                print("No Connected SSIDS")
                        else:
                            try:
                                self.check_if_no_internet_popup(driver)
                                forget_ssid = driver.find_element_by_xpath(
                                    "//*[@text='Forget']")
                                forget_ssid.click()
                                print("Forgetting ssid")
                            except:
                                print("Couldn't Forget Ssid or No connected Ssid")
                                logging.warning("Couldn't Forget Ssid or No connected Ssid")
                        # ----------------------This is to Forget current connected SSID--------------------------------

                        try:
                            print("clicking on wifi switch")
                            get_switch_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/switch_widget']")
                            driver.implicitly_wait(2)
                            get_switch_element.click()
                        except:
                            print("couldn't click on wifi switch")


                    except NoSuchElementException:
                        print("No Switch element found")
                    # ---------------------To Turn on WIFi Switch if already OFF-------------------------------

                except NoSuchElementException:
                    print("Couldn't find wifi Button")
                # ------------------Open WIFI page----------------------------------

            except NoSuchElementException:
                print("Exception: Verify Xpath - Update/check Xpath for Click Connections")
            # -----------------To Open Connections page---------------------------
        else:  # -----------------------Pixel4 code-------------------------
            report.step_start("Set Wifi Network to " + ssid)

            # -----------------To Open Connections page-----------------------
            try:
                print("Verifying Connected Wifi Connection")
                report.step_start("Click Network & internet")
                conn_element = driver.find_element_by_xpath("//*[@text='Network & internet']")
                conn_element.click()

                # ---------------------Open WIFI page-------------------------------
                try:
                    report.step_start("Clicking Wi-Fi")
                    print("Clicking WIFI")
                    time.sleep(3)
                    wifi_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='Wi‑Fi']")))
                    wifi_element.click()

                    # --------------------To Turn on WIFi Switch if already OFF--------------------------------
                    try:
                        driver.implicitly_wait(1)
                        get_switch_text_element = driver.find_element_by_xpath(
                            "//*[@resource-id='android:id/icon']")
                        get_switch_text = get_switch_text_element.click()
                        if get_switch_text is not None:
                            switch_text = "Off"
                        else:
                            switch_text = "On"

                        print("get_switch_text: ", switch_text)
                        print("Find wifi switch")
                        try:  # To Turn on Wi-Fi Switch
                            if switch_text == "Off":
                                # driver.implicitly_wait(3)
                                get_switch_element = driver.find_element_by_xpath(
                                    "//*[@resource-id='com.android.settings:id/switch_widget']")
                                driver.implicitly_wait(1)
                                get_switch_element.click()
                                driver.implicitly_wait(1)
                                i = 0
                                for i in range(5):
                                    if switch_text == "On":
                                        print("WIFI Switch is ON")
                                        break
                                    else:
                                        try:
                                            get_switch_text_element = driver.find_element_by_xpath(
                                                "//*[@text='Add network']")
                                            get_switch_text = get_switch_text_element.text
                                            if get_switch_text == "Add network":
                                                switch_text = "On"
                                            else:
                                                switch_text = "Off"
                                        except NoSuchElementException:
                                            print("Exception: Verify Xpath")
                                        # Scroll Down
                                        self.scrollDown(setup_perfectoMobile)
                                        print("Sleeping for: ", i)
                                        time.sleep(i)
                                        pass
                                if switch_text == "Off":
                                    print("Switch is Still OFF")
                                    self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            else:
                                print("Switch is already On")
                                self.check_if_no_internet_popup(driver)
                        except:
                            print("Couldn't turn on WIFI switch")
                            self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                            # ---------------------This is to Forget current connected SSID-------------------------------
                            try:  # To deal with already connected SSID
                                self.check_if_no_internet_popup(driver)
                                network_category = driver.find_element_by_xpath("//*[@text='Connected']")
                                try:  # To forget existing ssid
                                    print("To forget ssid")
                                    self.check_if_no_internet_popup(driver)
                                    additional_details_element = driver.find_element_by_xpath(
                                        "//*[@resource-id='com.android.settings:id/settings_button_no_background']")
                                    additional_details_element.click()
                                    try:
                                        self.check_if_no_internet_popup(driver)
                                        forget_ssid = driver.find_element_by_xpath(
                                            "//*[@resource-id='com.android.settings:id/button1']")
                                        forget_ssid.click()
                                        print("Forget old ssid")
                                    except:
                                        print("Couldn't forget ssid")
                                        self.closeApp(connData["appPackage-android"], setup_perfectoMobile)
                                except:
                                    # allure.attach(name=body=str("Couldn't get into additional details"))
                                    print("Couldn't get into additional details")
                            except:
                                # allure.attach(name=body=str("No Connected SSIDS"))
                                print("No Connected SSIDS")
                        # ----------------------This is to Forget current connected SSID--------------------------------

                        try:
                            print("clicking on wifi switch")
                            get_switch_element = driver.find_element_by_xpath(
                                "//*[@resource-id='com.android.settings:id/switch_widget']")
                            driver.implicitly_wait(2)
                            get_switch_element.click()
                        except:
                            print("couldn't click on wifi switch")


                    except NoSuchElementException:
                        print("No Switch element found")
                    # ---------------------To Turn on WIFi Switch if already OFF-------------------------------

                except NoSuchElementException:
                    print("Couldn't find wifi Button")
                # ------------------Open WIFI page----------------------------------

            except NoSuchElementException:
                print("Exception: Verify Xpath - Update/check Xpath for Click Connections")

        self.closeApp(connData["appPackage-android"], setup_perfectoMobile)

    def run_speed_test(self, setup_perfectoMobile, connData):
        print("\n-------------------------------------")
        print("Verify Upload & Download Speed")
        print("-------------------------------------")

        report = setup_perfectoMobile[1]
        driver = setup_perfectoMobile[0]
        connData = connData

        currentResult = False

        driver.switch_to.context('WEBVIEW_1')

        try:
            print("Launching Chrome")
            report.step_start("Google Home Page")
            logging.info("Launching Chrome")
            driver.get(connData["webURL"])
            print("Enter Search Text")
            logging.info("Entering Internet speed test search")
            elementFindTxt = driver.find_element_by_xpath(connData["lblSearch"])
            elementFindTxt.send_keys("Internet Speed Test")
            try:
                print("Click Search Button")
                report.step_start("Click Search Button")
                time.sleep(2)
                driver.implicitly_wait(2)
                elelSearch = driver.find_element_by_xpath("//*[@class='aajZCb']//*[@class='nz2CCf']/li[1]/div[2]")
                elelSearch.click()
                print("Keyboard enter")
                driver.press_keycode(66)
            except:
                try:
                    time.sleep(2)
                    driver.implicitly_wait(2)
                    elelSearch = driver.find_element_by_xpath("//*[@class='aajZCb']//*[@class='nz2CCf']/li[1]/div[2]")
                    elelSearch.click()
                except:
                    print("Search Drop Down not active...")
                    return False

            try:
                print("Click Run Speed Test Button...")
                report.step_start("Click Run Speed Test Button")
                driver.find_element_by_xpath(connData["BtnRunSpeedTest"]).click()
            except NoSuchElementException:
                print("Error in speed test element ", NoSuchElementException)
                return False

            # Get upload/Download Speed
            try:
                print("Get Download Speed")
                report.step_start("Get upload/Download Speed")
                time.sleep(60)
                downloadMbps = driver.find_element_by_xpath(connData["downloadMbps"])
                downloadSpeed = downloadMbps.text
                print("Download: " + downloadSpeed + " Mbps")

                print("Get Upload Speed")
                report.step_start("Get Upload Speed")
                UploadMbps = driver.find_element_by_xpath(connData["UploadMbps"])
                uploadSpeed = UploadMbps.text
                print("Upload: " + uploadSpeed + " Mbps")
                allure.attach(name="Speed Test logs: ",
                              body=str("Upload: " + uploadSpeed + " Mbps" + "  Download: " + downloadSpeed + " Mbps"))
                print("Access Point Verification Completed Successfully")
                currentResult = True
            except NoSuchElementException:
                print("Access Point Verification NOT Completed, checking Connection....")
        except Exception as e:
            print("Launching Chrome Failed")
            logging.error("Launching Chrome Failed")
            print(e)
            # allure.attach(name="Speed Test logs: ", body=str("Launching Safari Failed"))
            # allure.attach(name="Speed Test logs: ", body=str("Error log: " + e))
        return currentResult
if __name__ == '__main__':
    perfecto_data = {
        "securityToken": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJpYXQiOjE2MzI4Mzc2NDEsImp0aSI6IjAwZGRiYWY5LWQwYjMtNDRjNS1hYjVlLTkyNzFlNzc5ZGUzNiIsImlzcyI6Imh0dHBzOi8vYXV0aDIucGVyZmVjdG9tb2JpbGUuY29tL2F1dGgvcmVhbG1zL3RpcC1wZXJmZWN0b21vYmlsZS1jb20iLCJhdWQiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwic3ViIjoiODNkNjUxMWQtNTBmZS00ZWM5LThkNzAtYTA0ZjBkNTdiZDUyIiwidHlwIjoiT2ZmbGluZSIsImF6cCI6Im9mZmxpbmUtdG9rZW4tZ2VuZXJhdG9yIiwibm9uY2UiOiI2ZjE1YzYxNy01YTU5LTQyOWEtODc2Yi1jOTQxMTQ1ZDFkZTIiLCJzZXNzaW9uX3N0YXRlIjoiYmRjZTFmYTMtMjlkYi00MmFmLWI5YWMtYjZjZmJkMDEyOTFhIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.5R85_1R38ZFXv_wIjjCIsj8NJm1p66dCsLJI5DBEmks",
        "projectName": "TIP-PyTest-Execution",
        "projectVersion": "1.0",
        "reportTags": "TestTag",
        "perfectoURL": "tip",
        "Galaxy S20": {
            "platformName-android": "Android",
            "model-android": "Galaxy S20",
            "appPackage-android": "com.android.settings",
            "bundleId-iOS-Settings": "com.apple.Preferences",
            "bundleId-iOS-Safari": "com.apple.mobilesafari",
            "jobName": "Interop-Galaxy-S20",
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
    obj = android_libs()
