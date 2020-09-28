#!/usr/local/bin/python3
import re
import requests
import json
import logging
import configparser
from time import sleep, gmtime, strftime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--sdk-base-url', type=str, help='cloudsdk base url',
                    default="https://wlan-portal-svc.cicd.lab.wlan.tip.build")
parser.add_argument('--sdk-user-id', type=str, help='cloudsdk user id',
                    default="support@example.com")
parser.add_argument('--sdk-user-password', type=str, help='cloudsdk user password',
                    default="support")
parser.add_argument('--jfrog-base-url', type=str, help='jfrog base url',
                    default="tip.jFrog.io/artifactory/tip-wlan-ap-firmware")
parser.add_argument('--jfrog-user-id', type=str, help='jfrog user id',
                    default="cicd_user")
parser.add_argument('--jfrog-user-password', type=str, help='jfrog user password',
                    default="fakepassword")
parser.add_argument('--testrail-base-url', type=str, help='testrail base url',
                    default="https://telecominfraproject.testrail.com")
parser.add_argument('--testrail-project', type=str, help='testrail project name',
                    default="opsfleet-wlan")
parser.add_argument('--testrail-user-id', type=str, help='testrail user id',
                    default="gleb@opsfleet.com")
parser.add_argument('--testrail-user-password', type=str, help='testrail user password',
                    default="fakepassword")
args = parser.parse_args()

# if you lack __init__.py in this directory you will not find sta_connect module
from LANforge.LFUtils import *
from sta_connect2 import StaConnect2

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)-8s %(message)s file:%(pathname)s line:%(lineno)d",
                    datefmt="%m-%d %H:%M",
                    filename="nightly_cicd_sanity.log",
                    filemode="a")
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logging.getLogger().addHandler(console)
logging.info("")
logging.info("nightly sanity run start")

# Class to interact with Testrail
# I suspect it is probably better to replace this
# with pytest and nunit xml report
class TestRail_Client:
    def __init__(self):
        self.user = args.testrail_user_id
        self.password = args.testrail_user_password
        self.__url = f"{args.testrail_base_url}/index.php?/api/v2/"

    def send_get(self, uri, filepath=None):
        """Issue a GET request (read) against the API.

        Args:
            uri: The API method to call including parameters, e.g. get_case/1.
            filepath: The path and file name for attachment download; used only
                for "get_attachment/:attachment_id".

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request("GET", uri, filepath)

    def send_post(self, uri, data):
        """Issue a POST request (write) against the API.

        Args:
            uri: The API method to call, including parameters, e.g. add_case/1.
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded. If adding an attachment, must be the
                path to the file.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request("POST", uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri
        headers = {
            "Content-Type": "application/json"
        }
        logging.debug(f"Method: {method}; Url: {url}; Data: {data}")

        if method == "POST":
            if uri[:14] == "add_attachment":  # add_attachment API method
                files = { "attachment": open(data, "rb") }
                response = requests.post(url, headers=headers, files=files, auth=(self.user, self.password))
                files["attachment"].close()
            else:
                payload = bytes(json.dumps(data), "utf-8")
                response = requests.post(url, headers=headers, data=payload, auth=(self.user, self.password))
        else:
            response = requests.get(url, headers=headers, auth=(self.user, self.password))
            logging.debug(f"headers: {headers}; response: {response.text}; response code: {response.status_code}")

        if response.status_code > 201:
            try:
                error = response.json()
            except: # response.content not formatted as JSON
                error = str(response.content)
            logging.info(f"TestRail API returned HTTP status code {response.status_code} with the following: ({error})")
            return
        else:
            logging.debug(uri[:15])
            if uri[:15] == "get_attachments": # Expecting file, not JSON
                try:
                    logging.info (str(response.content))
                    open(data, "wb").write(response.content)
                    return (data)
                except:
                    return ("Error saving attachment.")
            else:
                try:
                    return response.json()
                except: # Nothing to return
                    return {}

    def get_project_id(self, project_name):
        "Get the project ID using project name"
        projects = testrail.send_get("get_projects")
        logging.debug(projects)
        for project in projects:
            if project["name"] == project_name:
                return project["id"]

    # def get_run_id(self, test_run_name, project_id):
    #     try:
    #         test_runs = testrail.send_get(f"get_runs/{project_id}")
    #     except Exception as e:
    #         logging.error(f"Exception in get_run_id(): {e}")
    #         return None
    #     else:
    #         for test_run in test_runs:
    #             if test_run["name"] == test_run_name:
    #                 logging.info(test_run)
    #                 run_id = test_run["id"]
    #                 logging.info(f"runId in Test Runs: {run_id}")
    #                 return run_id

    def update_testrail(self, case_id, run_id, status_id, msg):
        logging.info(f"Update TestRail; result status: {status_id}; case id: {case_id}; run id: {run_id}")
        if run_id is not None:
            try:
                result = testrail.send_post(
                    f"add_result_for_case/{run_id}/{case_id}",
                    { "status_id": status_id, "comment": msg } # status_id is 1 for Passed, 2 For Blocked, 4 for Retest and 5 for Failed
                )
                logging.info(f"Updating TestRail result: {result}")
            except Exception as e:
                logging.info(f"Exception in update_testrail(): {e}")
            else:
                logging.info(f"Updated test result for case: {case_id} in test run: {run_id} with msg: {msg}")

    def create_testrun(self, name, case_ids, project_id):
        result = testrail.send_post(
            f'add_run/{project_id}',
            {'name': name, 'case_ids': case_ids, 'include_all': False}
        )
        logging.info(result)
        return result["id"]

# Class for jFrog Interaction
class jFrog_Client:
    def __init__(self):
        self.user = args.jfrog_user_id
        self.password = args.jfrog_user_password
        self.baseUrl = args.jfrog_base_url

    def get_latest_image(self, model):
        # todo handle auth errors
        logging.debug(f"searching for the latest firmware on url: {model}")
        response = requests.get(f"https://{self.baseUrl}/{model}/dev/", auth=(self.user, self.password))
        return re.findall('href="(.+pending.+).tar.gz"', response.text)[-1]

    def get_latest_image_url(self, model, latest_image):
        return f"https://{self.user}:{self.password}@{self.baseUrl}/{model}/dev/{latest_image}.tar.gz"

# Class for CloudSDK Interaction via RestAPI
class CloudSDK_Client:
    def __init__(self):
        self.baseUrl = args.sdk_base_url
        cloud_login_url = f"{self.baseUrl}/management/v1/oauth2/token"
        payload = {
            "userId": args.sdk_user_id,
            "password": args.sdk_user_password
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            token_response = requests.post(cloud_login_url, headers=headers, data=json.dumps(payload))
        except requests.exceptions.RequestException as e:
            raise SystemExit(f"Exiting Script! Cloud not get bearer token for reason: {e}")
        token_data = token_response.json()
        self.headers = {
            "Authorization": f"Bearer {token_data['access_token']}"
        }

    def ap_firmware(self, customer_id, equipment_id):
        equip_fw_url = f"{self.baseUrl}/portal/status/forEquipment?customerId={customer_id}&equipmentId={equipment_id}&statusDataTypes="
        status_response = requests.get(equip_fw_url, headers=self.headers)
        logging.debug(status_response.json())
        return "ea8300-2020-09-09-pending-a6348d3" # (status_response.json())[2]["details"]["reportedSwVersion"]

    def get_images(self, apModel):
        getFW_url = f"{self.baseUrl}/portal/firmware/version/byEquipmentType?equipmentType=AP&modelId={apModel}"
        status_response = requests.get(getFW_url, headers=self.headers)
        logging.debug(status_response.json())
        return([ version.get("versionName") for version in status_response.json()])

    def firwmare_upload(self, apModel, latest_image, fw_url):
        commit = latest_image.split("-")[-1]
        fw_upload_url = f"{self.baseUrl}/portal/firmware/version"
        payload = {
            "model_type": "FirmwareVersion",
            "id": 0,
            "equipmentType": "AP",
            "modelId": apModel,
            "versionName": latest_image,
            "description": "",
            "filename": fw_url,
            "commit": commit,
            "validationMethod": "MD5_CHECKSUM",
            "validationCode": "19494befa87eb6bb90a64fd515634263",
            "releaseDate": 1596192028877,
            "createdTimestamp": 0,
            "lastModifiedTimestamp": 0
        }
        self.headers["Content-Type"] = "application/json"
        response = requests.post(fw_upload_url, headers=self.headers, data=json.dumps(payload))
        self.headers.pop("Content-Type", None)
        logging.debug(response)
        return(response.json())

    def get_firmware_id(self, latest_ap_image):
        logging.debug(latest_ap_image)
        fw_id_url = f"{self.baseUrl}/portal/firmware/version/byName?firmwareVersionName={latest_ap_image}"
        response = requests.get(fw_id_url, headers=self.headers)
        fw_data = response.json()
        return fw_data["id"]

    def update_firmware(self, equipment_id, latest_firmware_id):
        url = f"{self.baseUrl}/portal/equipmentGateway/requestFirmwareUpdate?equipmentId={equipment_id}&firmwareVersionId={latest_firmware_id}"
        response = requests.post(url, headers=self.headers)
        logging.info(response.text)

    def set_ap_profile(self, equipment_id, test_profile_id):
        url = f"{self.baseUrl}/portal/equipment?equipmentId={equipment_id}"
        response = requests.get(url, headers=self.headers)
        logging.info(response)

        # Add Lab Profile ID to Equipment
        equipment_info = response.json()
        logging.debug(equipment_info)
        equipment_info["profileId"] = test_profile_id
        logging.debug(equipment_info)

        # Update AP Info with Required Profile ID
        url = f"{self.baseUrl}/portal/equipment"
        self.headers["Content-Type"] = "application/json"
        response = requests.put(url, headers=self.headers, data=json.dumps(equipment_info))
        self.headers.pop("Content-Type", None)
        logging.debug(response.text)

# Class for tests (temp)
class RunTest:
    def Single_Client_Connectivity(self, radio, ssid_name, ssid_psk, security, station, test_case, runId):
        """SINGLE CLIENT CONNECTIVITY using sta_connect2.py"""
        staConnect = StaConnect2("10.10.10.201", 8080, debug_= False)
        staConnect.sta_mode = 0
        staConnect.upstream_resource = 1
        staConnect.upstream_port = "eth2"
        staConnect.radio = radio
        staConnect.resource = 1
        staConnect.dut_ssid = ssid_name
        staConnect.dut_passwd = ssid_psk
        staConnect.dut_security = security
        staConnect.station_names = station
        staConnect.runtime_secs = 30
        staConnect.cleanup_on_exit = True
        staConnect.setup()
        staConnect.start()
        logging.info(f"sleeping {staConnect.runtime_secs} seconds")
        sleep(staConnect.runtime_secs)
        staConnect.stop()
        staConnect.cleanup()
        run_results = staConnect.get_result_list()
        for result in run_results:
            logging.info("test result: " + result)
        if staConnect.passes() == True:
            logging.info(f"Single client connection to {ssid_name} successful. Test Passed")
            testrail.update_testrail(case_id=test_case, run_id=runId, status_id=1, msg="Client connectivity passed")
        else:
            logging.info(f"Single client connection to {ssid_name} unsuccessful. Test Failed")
            testrail.update_testrail(case_id=test_case, run_id=runId, status_id=5, msg="Client connectivity failed")

# instantiate clients and configuration
sdk: CloudSDK_Client = CloudSDK_Client()
testrail: TestRail_Client = TestRail_Client()
jFrog: jFrog_Client = jFrog_Client()
Test: RunTest = RunTest()

# models under test and their data
customer_id = "2"
ap_models = {
    "ea8300": {
        "id": "3",
        "firmware": "unknown",
        "info": {
            "profile_id": "24",
            "fiveG_WPA2_SSID": "EA8300_5G_WPA2",
            "fiveG_WPA2_PSK": "Connectus123$",
            "fiveG_WPA_SSID": "EA8300_5G_WPA",
            "fiveG_WPA_PSK": "Connectus123$",
            "fiveG_OPEN_SSID": "EA8300_5G_OPEN",
            "twoFourG_OPEN_SSID": "EA8300_2dot4G_OPEN",
            "twoFourG_WPA2_SSID": "EA8300_2dot4G_WPA2",
            "twoFourG_WPA2_PSK": "Connectus123$",
            "twoFourG_WPA_SSID":"EA8300_2dot4G_WPA",
            "twoFourG_WPA_PSK": "Connectus123$"
        }
    },
    # "ecw5410": {
    #     "id": "6",
    #     "firmware": "unknown",
    #     "info": {
    #         "profile_id": "7",
    #         "fiveG_WPA2_SSID": "ECW5410_5G_WPA2",
    #         "fiveG_WPA2_PSK": "Connectus123$",
    #         "fiveG_WPA_SSID": "ECW5410_5G_WPA",
    #         "fiveG_WPA_PSK": "Connectus123$",
    #         "fiveG_OPEN_SSID": "ECW5410_5G_OPEN",
    #         "twoFourG_OPEN_SSID": "ECW5410_2dot4G_OPEN",
    #         "twoFourG_WPA2_SSID": "ECW5410_2dot4G_WPA2",
    #         "twoFourG_WPA2_PSK": "Connectus123$",
    #         "twoFourG_WPA_SSID":"ECW5410_2dot4G_WPA",
    #         "twoFourG_WPA_PSK": "Connectus123$"
    #     }
    # }
}

# 1. Find Latest firmware on jFrog for each AP Model
# 2. Find Available firmware on CloudSDK
# 3. If Latest firmware not present, upload
# 4. Update Firmware on each AP Model
# 5. Run tests
for model in ap_models.keys():
    # Get latest firmware on jFrog
    logging.info(f"Model: {model}")
    latest_image = jFrog.get_latest_image(model)
    logging.info(f"Latest firmware on jFrog: {latest_image}")
    # Get latest firmware on Cloud SDK
    firmware_list_by_model = sdk.get_images(model)
    logging.info(f"Latest firmware on Cloud SDK: {firmware_list_by_model}")

    if latest_image in firmware_list_by_model:
        logging.info(f"Latest firmware {latest_image} present on CloudSDK!")
        ap_models[model]["firmware"] = latest_image
    else:
        logging.info(f"Uploading {latest_image} firmware to CloudSDK")
        fw_url = jFrog.get_latest_image_url(model, latest_image)
        fw_upload_status = sdk.firwmare_upload(model, latest_image, fw_url)
        logging.debug(fw_upload_status)
        logging.info(f"Upload Complete. {latest_image}; firmware ID is {fw_upload_status['id']}")
        ap_models[model]["firmware"] = latest_image

    # Get Current AP Firmware and upgrade
    equipment_id = ap_models[model]["id"]
    ap_fw = sdk.ap_firmware(customer_id, equipment_id)
    fw_model = ap_fw.partition("-")[0]
    logging.info(f"Testing AP model: {fw_model}; firmware: {ap_fw}")
    # Find Latest firmware for Current AP Model and Get FW ID
    latest_ap_image = ap_models[fw_model]["firmware"]
    model_firmware_id = sdk.get_firmware_id(latest_ap_image)
    logging.info(f"Latest firmware ID is: {model_firmware_id}")

    if ap_fw != latest_ap_image:
        logging.info("Model does not require firmware upgrade, skipping sanity tests")
    else:
        logging.info("Model requires firmware update, will update and sleep for 5 minutes")
        sdk.update_firmware(equipment_id, model_firmware_id)
        # sleep(300) # probably waits for the AP to upgrade ??? this is really fragile, need to loop and check

        test_cases_data = {
            2832: { # 2.4 GHz Open
                "radio": "wiphy0",
                "station": ["sta2234"],
                "ssid_name": ap_models[fw_model]["info"]["twoFourG_OPEN_SSID"],
                "ssid_psk": "BLANK",
                "security": "open"
            },
            2833: { # 5 GHz Open
                "radio": "wiphy3",
                "station": ["sta2235"],
                "ssid_name": ap_models[fw_model]["info"]["fiveG_OPEN_SSID"],
                "ssid_psk": "BLANK",
                "security": "open"
            },
            2834: { # 5 GHz WPA2
                "radio": "wiphy3",
                "station": ["sta2236"],
                "ssid_name": ap_models[fw_model]["info"]["fiveG_WPA2_SSID"],
                "ssid_psk": ap_models[fw_model]["info"]["fiveG_WPA2_PSK"],
                "security": "wpa2"
            },
            2835: { # 2.4 GHz WPA2
                "radio": "wiphy0",
                "station": ["sta2237"],
                "ssid_name": ap_models[fw_model]["info"]["twoFourG_WPA2_SSID"],
                "ssid_psk": ap_models[fw_model]["info"]["twoFourG_WPA2_PSK"],
                "security": "wpa2"
            },
            2836: { # 5 GHz WPA
                "radio": "wiphy3",
                "station": ["sta2419"],
                "ssid_name": ap_models[fw_model]["info"]["fiveG_WPA_SSID"],
                "ssid_psk": ap_models[fw_model]["info"]["fiveG_WPA_PSK"],
                "security": "wpa"
            },
            2837: { # 2.4 GHz WPA
                "radio": "wiphy0",
                "station": ["sta2420"],
                "ssid_name": ap_models[fw_model]["info"]["twoFourG_WPA_SSID"],
                "ssid_psk": ap_models[fw_model]["info"]["twoFourG_WPA_PSK"],
                "security": "wpa"
            }
        }

        # Create Test Run
        test_run_name = f'Daily_Sanity_{fw_model}_{strftime("%Y-%m-%d", gmtime())}_{ap_fw}_opsfleet'
        testrail_project_id = testrail.get_project_id(project_name=args.testrail_project)
        runId = testrail.create_testrun(name=test_run_name, case_ids=(list(test_cases_data) + [2831]), project_id=testrail_project_id)
        logging.debug(f"Testrail project id: {testrail_project_id}")
        logging.debug(f"TIP run ID is: {runId}")

        # Check if upgrade worked
        ap_fw = sdk.ap_firmware(customer_id, equipment_id)
        logging.info(f"Current AP Firmware: {ap_fw}")
        if ap_fw == latest_ap_image:
            testrail.update_testrail(case_id="2831", run_id=runId, status_id=1, msg="Upgrade successful")
            logging.info("Upgrade SUCCESS. Proceeding with sanity testing for this AP variant")
        else:
            testrail.update_testrail(case_id="2831", run_id=runId, status_id=5, msg="Upgrade Failed")
            logging.error("Upgrade FAILED. Updating TestRail and skipping sanity tests for this AP variant.")
            continue

        # Set Proper AP Profile
        test_profile_id = ap_models[fw_model]["info"]["profile_id"]
        logging.info(test_profile_id)
        sdk.set_ap_profile(equipment_id, test_profile_id)

        # Run Client Single Connectivity Test Cases
        for testcase in test_cases_data.keys():
            logging.info(f"radio: {test_cases_data[testcase]['radio']}; ssid_name: {test_cases_data[testcase]['ssid_name']}; ssid_psk: {test_cases_data[testcase]['ssid_psk']}; security: {test_cases_data[testcase]['security']}; station: {test_cases_data[testcase]['station']}; testcase: {testcase}; runId: {runId}")
            Test.Single_Client_Connectivity(test_cases_data[testcase]["radio"], test_cases_data[testcase]["ssid_name"], test_cases_data[testcase]["ssid_psk"],
                                            test_cases_data[testcase]["security"], test_cases_data[testcase]["station"], testcase, runId)

logging.info("End of Sanity Test run")
