#!/usr/local/bin/python3

import re
import requests
import json
import logging
import argparse
from time import sleep, gmtime, strftime
from unittest.mock import Mock

# the below hack is only needed for local dev
# This should be replaced with a module and added to dockerfile
import sys
for folder in 'py-json','py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../lanforge/lanforge/{folder}')

from LANforge.LFUtils import *
from sta_connect2 import StaConnect2

# Run from remote dev machine on ssh tunnel through to LANforge in TIP Lab, without testrails being used.
# SSH tunnel created with login to orchestrator with option: -L 10080:lf1:8080
# python3 ./nightly.py --skip-update-firmware --no-testrails --lanforge-ip-address localhost --lanforge-port-number 10080

parser = argparse.ArgumentParser()
parser.add_argument("--sdk-base-url", type=str, help="cloudsdk base url",
                    default="https://wlan-portal-svc.cicd.lab.wlan.tip.build")
parser.add_argument("--sdk-user-id", type=str, help="cloudsdk user id",
                    default="support@example.com")
parser.add_argument("--sdk-user-password", type=str, help="cloudsdk user password",
                    default="support")
parser.add_argument("--jfrog-base-url", type=str, help="jfrog base url",
                    default="tip.jFrog.io/artifactory/tip-wlan-ap-firmware")
parser.add_argument("--jfrog-user-id", type=str, help="jfrog user id",
                    default="tip-read")
parser.add_argument("--jfrog-user-password", type=str, help="jfrog user password",
                    default="tip-read")
parser.add_argument("--testrail-base-url", type=str, help="testrail base url",
                    default="https://telecominfraproject.testrail.com")
parser.add_argument("--testrail-project", type=str, help="testrail project name",
                    default="opsfleet-wlan")
parser.add_argument("--testrail-user-id", type=str, help="testrail user id",
                    default="gleb@opsfleet.com")
parser.add_argument("--testrail-user-password", type=str, help="testrail user password",
                    default="password")
parser.add_argument("--lanforge-ip-address", type=str, help="ip address of the lanforge gui",
                    default="10.28.3.6")
parser.add_argument("--lanforge-port-number", type=str, help="port of the lanforge gui",
                    default="8080")
parser.add_argument('--skip-update-firmware', dest='update_firmware', action='store_false')
parser.add_argument('--no-testrails', dest='use_testrails', action='store_false')
parser.set_defaults(update_firmware=True)
parser.set_defaults(use_testrails=True)
command_line_args = parser.parse_args()

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
logging.info("------------------------")
logging.info("nightly sanity run start")

# Initialize constants
with open("nightly_test_config.json") as json_file:
    TEST_DATA = json.load(json_file)
TESTRAIL = {
    True: {
        "statusCode": 1, # status_id is 1 for Passed, 2 For Blocked, 4 for Retest, 5 for Failed
        "message": "success"
    },
    False: {
        "statusCode": 5,
        "message": "failure"
    }
}

# Class to interact with Testrail; better to replace this with pytest\nunit
class TestRail_Client:
    def __new__(cls, *args, **kwargs):
        if command_line_args.use_testrails:
            return super().__new__(cls, *args, **kwargs)
        else:
            mock = Mock()
            mock.get_project_id.return_value = -1
            mock.create_testrun.return_value = -1
            return mock

    def __init__(self):
        self.user = command_line_args.testrail_user_id
        self.password = command_line_args.testrail_user_password
        self.__url = f"{command_line_args.testrail_base_url}/index.php?/api/v2/"

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
            if uri[:14] == "add_attachment": # add_attachment API method
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

    def update_testrail(self, case_id, run_id, status_id, msg):
        logging.info(f"Update TestRail; result status: {status_id}; case id: {case_id}; run id: {run_id}")
        if run_id is not None:
            try:
                result = testrail.send_post(
                    f"add_result_for_case/{run_id}/{case_id}",
                    { "status_id": status_id, "comment": msg }
                )
                logging.info(f"Updating TestRail result: {result}")
            except Exception as e:
                logging.info(f"Exception in update_testrail(): {e}")
            else:
                logging.info(f"Updated test result for case: {case_id} in test run: {run_id} with msg: {msg}")

    def create_testrun(self, name, case_ids, project_id):
        result = testrail.send_post(
            f"add_run/{project_id}",
            {"name": name, "case_ids": case_ids, "include_all": False}
        )
        logging.debug(result)
        return result["id"]

# Class for jFrog Interaction
class jFrog_Client:
    def __init__(self):
        self.user = command_line_args.jfrog_user_id
        self.password = command_line_args.jfrog_user_password
        self.baseUrl = command_line_args.jfrog_base_url

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
        self.baseUrl = command_line_args.sdk_base_url
        cloud_login_url = f"{self.baseUrl}/management/v1/oauth2/token"
        payload = {
            "userId": command_line_args.sdk_user_id,
            "password": command_line_args.sdk_user_password
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
        return (status_response.json())[2]["details"]["reportedSwVersion"]

    def get_images(self, apModel):
        getFW_url = f"{self.baseUrl}/portal/firmware/version/byEquipmentType?equipmentType=AP&modelId={apModel}"
        status_response = requests.get(getFW_url, headers=self.headers)
        logging.debug(status_response.json())
        return([ version.get("versionName") for version in status_response.json()])

    def firwmare_upload(self, apModel, latest_image, fw_url):
        fw_upload_url = f"{self.baseUrl}/portal/firmware/version"
        payload = {
            "model_type": "FirmwareVersion",
            "id": 0,
            "equipmentType": "AP",
            "modelId": apModel,
            "versionName": latest_image,
            "description": "",
            "filename": fw_url,
            "commit": latest_image.split("-")[-1],
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

    def get_firmware_id(self, image):
        logging.debug(image)
        fw_id_url = f"{self.baseUrl}/portal/firmware/version/byName?firmwareVersionName={image}"
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
        logging.debug(response.json())

        # Add Lab Profile ID to Equipment
        equipment_info = response.json()
        logging.debug(equipment_info)
        equipment_info["profileId"] = test_profile_id

        # Update AP Info with Required Profile ID
        url = f"{self.baseUrl}/portal/equipment"
        self.headers["Content-Type"] = "application/json"
        response = requests.put(url, headers=self.headers, data=json.dumps(equipment_info))
        self.headers.pop("Content-Type", None)
        logging.debug(response.text)

# Instantiate clients and configuration
sdk: CloudSDK_Client = CloudSDK_Client()
testrail: TestRail_Client = TestRail_Client()
jFrog: jFrog_Client = jFrog_Client()

# 1. Find Latest firmware on jFrog for each AP Model
# 2. Find Available firmware on CloudSDK
# 3. If Latest firmware not present, upload
# 4. Update Firmware on each AP Model
# 5. Run tests
for model in TEST_DATA["ap_models"].keys():
    # Get latest firmware on jFrog and Cloud SDK
    latest_image = jFrog.get_latest_image(model)
    firmware_list_by_model = sdk.get_images(model)
    TEST_DATA["ap_models"][model]["firmware"] = latest_image
    logging.info(f"Model: {model}; Latest firmware on jFrog: {latest_image}; Firmware on Cloud SDK: {firmware_list_by_model}")

    if latest_image in firmware_list_by_model:
        model_firmware_id = sdk.get_firmware_id(latest_image)
        logging.info(f"Latest firmware {latest_image} present on CloudSDK!")
    else:
        logging.info(f"Uploading {latest_image} firmware to CloudSDK")
        fw_url = jFrog.get_latest_image_url(model, latest_image)
        fw_upload_status = sdk.firwmare_upload(model, latest_image, fw_url)
        model_firmware_id = fw_upload_status['id']
        logging.info(f"Upload Complete. {latest_image}; firmware ID is {model_firmware_id}")

    # Get Current AP Firmware and upgrade\run tests if needed
    ap_fw = sdk.ap_firmware(TEST_DATA["customer_id"], TEST_DATA["ap_models"][model]["id"])
    logging.info(f"Firmware: {ap_fw}; latest firmware is: {latest_image} with ID: {model_firmware_id}")

    if ap_fw == latest_image and command_line_args.update_firmware:
        logging.info("Model does not require firmware upgrade, skipping sanity tests")
    else:
        if command_line_args.update_firmware:
            firmware_update_case = [2831]
            logging.info("Model requires firmware update, will update and sleep")
            sdk.update_firmware(TEST_DATA["ap_models"][model]["id"], model_firmware_id)
            sleep(300) # need to have a proper wait\retry here
        else:
            firmware_update_case = []

        test_cases_data = {
            2832: { # 2.4 GHz Open
                "radio": "wiphy4",
                "station": ["sta2234"],
                "ssid_name": TEST_DATA["ap_models"][model]["info"]["twoFourG_OPEN_SSID"],
                "ssid_psk": "BLANK",
                "security": "open"
            },
            2835: { # 2.4 GHz WPA2
                "radio": "wiphy4",
                "station": ["sta2237"],
                "ssid_name": TEST_DATA["ap_models"][model]["info"]["twoFourG_WPA2_SSID"],
                "ssid_psk": TEST_DATA["ap_models"][model]["info"]["twoFourG_WPA2_PSK"],
                "security": "wpa2"
            },
            2833: { # 5 GHz Open
                "radio": "wiphy3",
                "station": ["sta2235"],
                "ssid_name": TEST_DATA["ap_models"][model]["info"]["fiveG_OPEN_SSID"],
                "ssid_psk": "BLANK",
                "security": "open"
            },
            2834: { # 5 GHz WPA2
                "radio": "wiphy3",
                "station": ["sta2236"],
                "ssid_name": TEST_DATA["ap_models"][model]["info"]["fiveG_WPA2_SSID"],
                "ssid_psk": TEST_DATA["ap_models"][model]["info"]["fiveG_WPA2_PSK"],
                "security": "wpa2"
            },
            2836: { # 5 GHz WPA
                "radio": "wiphy3",
                "station": ["sta2419"],
                "ssid_name": TEST_DATA["ap_models"][model]["info"]["fiveG_WPA_SSID"],
                "ssid_psk": TEST_DATA["ap_models"][model]["info"]["fiveG_WPA_PSK"],
                "security": "wpa"
            },
            2837: { # 2.4 GHz WPA
                "radio": "wiphy0",
                "station": ["sta2420"],
                "ssid_name": TEST_DATA["ap_models"][model]["info"]["twoFourG_WPA_SSID"],
                "ssid_psk": TEST_DATA["ap_models"][model]["info"]["twoFourG_WPA_PSK"],
                "security": "wpa"
            }
        }

        # Create Test Run
        testrail_project_id = testrail.get_project_id(project_name=command_line_args.testrail_project)
        runId = testrail.create_testrun(
            name=f'Nightly_model_{model}_firmware_{ap_fw}_{strftime("%Y-%m-%d", gmtime())}',
            case_ids=( [*test_cases_data] + firmware_update_case ),
            project_id=testrail_project_id
        )
        logging.info(f"Testrail project id: {testrail_project_id}; run ID is: {runId}")

        # Check if upgrade worked
        if command_line_args.update_firmware:
            results = TESTRAIL[(sdk.ap_firmware(TEST_DATA["customer_id"], TEST_DATA["ap_models"][model]["id"]) == latest_image)]
            testrail.update_testrail(case_id="2831", run_id=runId, status_id=results["statusCode"], msg=f"Upgrade {results['message']}")
            logging.info(f"Upgrade {results['statusCode']}")
            if results["message"] == "failure": # might want to fail all the other tests in testrails
                continue

        # Set Proper AP Profile
        test_profile_id = TEST_DATA["ap_models"][model]["info"]["profile_id"]
        sdk.set_ap_profile(TEST_DATA["ap_models"][model]["id"], test_profile_id)
        logging.info(f"Test profile id: {test_profile_id}")

        # Run Client Single Connectivity Test Cases
        for testcase in test_cases_data.keys():
            if test_cases_data[testcase]["ssid_name"] != "skip": # to be refactored with pytest, good enough for now
                logging.info(f"Test parameters are:\n  radio = {test_cases_data[testcase]['radio']}\n  ssid_name = {test_cases_data[testcase]['ssid_name']}\n  ssid_psk = {test_cases_data[testcase]['ssid_psk']}\n  security = {test_cases_data[testcase]['security']}\n  station = {test_cases_data[testcase]['station']}\n  testcase = {testcase}")
                staConnect = StaConnect2(command_line_args.lanforge_ip_address, command_line_args.lanforge_port_number, debug_ = False)
                staConnect.sta_mode = 0
                staConnect.upstream_resource = 1
                staConnect.upstream_port = "eth2"
                staConnect.radio = test_cases_data[testcase]["radio"]
                staConnect.resource = 1
                staConnect.dut_ssid = test_cases_data[testcase]["ssid_name"]
                staConnect.dut_passwd = test_cases_data[testcase]["ssid_psk"]
                staConnect.dut_security = test_cases_data[testcase]["security"]
                staConnect.station_names = test_cases_data[testcase]["station"]
                staConnect.runtime_secs = 30
                staConnect.clean_all_sta = True
                staConnect.cleanup_on_exit = True
                staConnect.setup()
                staConnect.start()
                logging.info(f"sleeping {staConnect.runtime_secs} seconds")
                sleep(staConnect.runtime_secs)
                staConnect.stop()
                staConnect.cleanup()
                for result in staConnect.get_result_list():
                    logging.info(f"test result: {result}")
                results = TESTRAIL[staConnect.passes()]
                logging.info(f"Single client connection to {test_cases_data[testcase]['ssid_name']} successful. Test {results['message']}")
                testrail.update_testrail(case_id=testcase, run_id=runId, status_id=results["statusCode"], msg=f"Test {results['message']}")

logging.info("----------------------")
logging.info("End of Sanity Test run")
logging.info("----------------------")
