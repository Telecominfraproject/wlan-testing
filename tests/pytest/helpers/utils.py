import re
import requests
import json

# Class to interact with Testrail
class TestRail_Client:
    def __init__(self, url, user, password):
        self.user = user
        self.password = password
        self.__url = f"https://{url}/index.php?/api/v2/"

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

        if response.status_code > 201:
            try:
                error = response.json()
            except: # response.content not formatted as JSON
                error = str(response.content)
            return
        else:
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
        projects = self.send_get("get_projects")
        for project in projects:
            if project["name"] == project_name:
                return project["id"]

    def update_testrail(self, case_id, run_id, status_id, msg):
        result = self.send_post(
            f"add_result_for_case/{run_id}/{case_id}",
            { "status_id": status_id, "comment": msg }
        )

    def create_testrun(self, name, case_ids, project_id):
        result = self.send_post(
            f"add_run/{project_id}",
            {"name": name, "case_ids": case_ids, "include_all": False}
        )
        return result["id"]

# Class for jFrog Interaction
class jFrog_Client:
    def __init__(self, url, user, password):
        self.user = user
        self.password = password
        self.baseUrl = f"https://{url}"

    def get_latest_image(self, model):
        # todo handle auth errors
        response = requests.get(f"{self.baseUrl}/{model}/dev/", auth=(self.user, self.password))
        return re.findall('href="(.+pending.+).tar.gz"', response.text)[-1]

    def get_latest_image_url(self, model, latest_image):
        return f"https://{self.user}:{self.password}@{self.baseUrl}/{model}/dev/{latest_image}.tar.gz"

# Class for CloudSDK Interaction via RestAPI
class CloudSDK_Client:
    def __init__(self, url, user, password):
        self.baseUrl = f"https://{url}"
        cloud_login_url = f"{self.baseUrl}/management/v1/oauth2/token"
        payload = {
            "userId": user,
            "password": password
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
        return (status_response.json())[2]["details"]["reportedSwVersion"]

    def get_images(self, apModel):
        getFW_url = f"{self.baseUrl}/portal/firmware/version/byEquipmentType?equipmentType=AP&modelId={apModel}"
        status_response = requests.get(getFW_url, headers=self.headers)
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
        return(response.json())

    def get_firmware_id(self, image):
        fw_id_url = f"{self.baseUrl}/portal/firmware/version/byName?firmwareVersionName={image}"
        response = requests.get(fw_id_url, headers=self.headers)
        fw_data = response.json()
        return fw_data["id"]

    def update_firmware(self, equipment_id, latest_firmware_id):
        url = f"{self.baseUrl}/portal/equipmentGateway/requestFirmwareUpdate?equipmentId={equipment_id}&firmwareVersionId={latest_firmware_id}"
        response = requests.post(url, headers=self.headers)

    def set_ap_profile(self, equipment_id, test_profile_id):
        url = f"{self.baseUrl}/portal/equipment?equipmentId={equipment_id}"
        response = requests.get(url, headers=self.headers)

        # Add Lab Profile ID to Equipment
        equipment_info = response.json()
        equipment_info["profileId"] = test_profile_id

        # Update AP Info with Required Profile ID
        url = f"{self.baseUrl}/portal/equipment"
        self.headers["Content-Type"] = "application/json"
        response = requests.put(url, headers=self.headers, data=json.dumps(equipment_info))
        self.headers.pop("Content-Type", None)
