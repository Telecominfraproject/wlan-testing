import logging
import time
import warnings

import allure
import pytest
import urllib3
from appium import webdriver
from appium.webdriver import webdriver
from appium.webdriver.common.mobileby import MobileBy
from perfecto import (PerfectoExecutionContext, PerfectoReportiumClient, TestContext)
from perfecto.model.model import Job, Project
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



class ios_libs:
    global driver, perfecto_execution_context, deviceModel
    def __init__(self, perfecto_data=None, dut_data=None):
        self.perfecto_data = perfecto_data
        self.dut_data = dut_data
        pass

    def openApp(self, appName, setup_perfectoMobile):
        setup_perfectoMobile[1].step_start("Opening App: " + appName)
        params = {'identifier': appName}
        # Open/Close/Open Action is performed to ensure the app is back to its Original Settings
        setup_perfectoMobile[0].execute_script('mobile:application:open', params)
        setup_perfectoMobile[0].execute_script('mobile:application:close', params)
        setup_perfectoMobile[0].execute_script('mobile:application:open', params)

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

    def closeApp(self, appName, setup_perfectoMobile):
        # print("Closing App.." + appName)
        setup_perfectoMobile[1].step_start("Closing App: " + appName)
        params = {'identifier': appName}
        setup_perfectoMobile[0].execute_script('mobile:application:close', params)
    def setup_perfectoMobile_iOS(self):
        global perfecto_execution_context, driver, deviceModel
        driver = None
        reporting_client = None
        get_device_configuration = self.get_device_configuration()
        warnings.simplefilter("ignore", ResourceWarning)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        capabilities = {
            'platformName': get_device_configuration["platformName-iOS"],
            'model': get_device_configuration["model-iOS"],
            'browserName': 'safari',
            # 'automationName' : 'Appium',
            'securityToken': self.perfecto_data["securityToken"],
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
        testCaseName = "TestCaseName_hari_ios_check"

        print("\nSetting Perfecto ReportClient....")
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

    def ssid_Visible(self, driver, WifiName):
        wifiSelectionElement = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@label='" + WifiName + "']")))
        isVisible = wifiSelectionElement.get_attribute("visible")
        print(f"Is ssid visible: {isVisible}")
        if (isVisible == 'false'):
            return False
        else:
            return True

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
    def wifi_connect(self, ssid, passkey, setup_perfectoMobile, connData):
        print("\n-------------------------------------")
        print("Select Wifi/Get IP Address IOS Connection")
        print("-------------------------------------")
        is_internet = False
        wifi_name = ssid
        wifi_pass = passkey

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
                            return is_internet
                    else:
                        print("Switch is Still OFF")
                        logging.error("Wifi Switch is OFF")
                        self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
                        return is_internet
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
            return is_internet

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
                            return is_internet

                except:
                    print("couldn't connect to " + wifi_name)
                    logging.error("Couldn't Find ssid")
                    # request.config.cache.set(key="SelectingWifiFailed", value=str(e))
                    self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
                    return is_internet
                    pass

            if not ssid_found:
                print("could not found " + wifi_name + " in device")
                logging.error("Couldn't Find ssid in device")
                self.closeApp(self.connData["bundleId-iOS-Settings"], setup_perfectoMobile)
                return is_internet
        except:
            pass
        # ---------------------To get all available SSID and select it-------------------------------
        # ---------------------Set Password-------------------------------
        try:
            driver.implicitly_wait(5)
            print("Entering Password")
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
        return is_internet, setup_perfectoMobile

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