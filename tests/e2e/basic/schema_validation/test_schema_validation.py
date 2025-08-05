import pytest
import allure
import logging
import json
import requests
import re
import os
import time
from tabulate import tabulate
from datetime import datetime

pytestmark = [pytest.mark.schema_validation]


# Get the directory of the current test config file
test_file_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path relative to the config file directory
file_path = os.path.join(test_file_dir, 'master-config-1.json')
with open(file_path, 'r') as file:
    json_string = file.read()
    config_data_1 = json.loads(json_string)

file_path2 = os.path.join(test_file_dir, 'master-config-2.json')
with open(file_path2, 'r') as file:
    json_string = file.read()
    config_data_2 = json.loads(json_string)

file_path3 = os.path.join(test_file_dir, 'master-config-3.json')
with open(file_path3, 'r') as file:
    json_string = file.read()
    config_data_3 = json.loads(json_string)


def make_raw_url(url):
    return url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")


def get_github_file(url, path=None, commit_id=None):
    if commit_id:
        url = url.replace("main", commit_id)
    if path:
        url = url + path
    url = make_raw_url(url)
    logging.info(f"Fetching {url}")
    response = requests.get(url)
    if response.status_code != 200:
        logging.info(f"Failed to fetch {url}. Status code: {response.status_code}")
        pytest.skip("Failed to fetch the schema file from GitHub. Make sure the commit-id is one from "
                    "wlan-ucentral-schema repo.")
    return response.text

def validate_schema_through_github(commit_id, path):
    def get_commit_id(owner, repo, path="", headers=None):
        if headers is None:
            headers = {"Accept": "application/vnd.github.v3+json"}
        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        params = {"sha": "main", "path": path}
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            commit_id = data[0]['sha']
            return commit_id
        else:
            logging.info(f"Failed to fetch commit-id. Status code: {response.status_code}")

    def compare_dicts(dict1, dict2, path="", added_keys=None, removed_keys=None, changed_items=None):
        if dict1 == dict2:
            return added_keys, removed_keys, changed_items

        if changed_items is None:
            changed_items = []
        if removed_keys is None:
            removed_keys = set()
        if added_keys is None:
            added_keys = set()

        for key in set(dict1.keys()) | set(dict2.keys()):
            new_path = f"{path} > {key}" if path else key

            if key not in dict1:
                added_keys.add((new_path, f"{dict2[key]}"))
            elif key not in dict2:
                removed_keys.add(new_path)
            elif dict1[key] != dict2[key]:
                if type(dict1[key]) == type(dict2[key]):
                    if isinstance(dict1[key], dict):
                        added_keys, removed_keys, changed_items = compare_dicts(dict1[key], dict2[key], path=new_path,
                                                                                added_keys=added_keys,
                                                                                removed_keys=removed_keys,
                                                                                changed_items=changed_items)
                    elif isinstance(dict1[key], list):
                        if len(dict1[key]) != len(dict2[key]):
                            changed_items.append((f"length of array at {new_path}", f"{len(dict1[key])}",
                                                  f"{len(dict2[key])}"))
                            changed_items.append((new_path, f"{dict1[key]}", f"{dict2[key]}"))
                        else:
                            for index, (val1, val2) in enumerate(zip(dict1[key], dict2[key])):
                                added_keys, removed_keys, changed_items = compare_dicts(val1, val2,
                                                                                        path=f"{new_path} > [item {index}]",
                                                                                        added_keys=added_keys,
                                                                                        removed_keys=removed_keys,
                                                                                        changed_items=changed_items)
                    elif isinstance(dict1[key], str) or isinstance(dict1[key], int) or isinstance(dict1[key], float):
                        changed_items.append((new_path, f"{dict1[key]}", f"{dict2[key]}"))
                else:
                    changed_items.append((new_path, f"{dict1[key]}", f"{dict2[key]}"))

        return added_keys, removed_keys, changed_items

    def generate_diff(wlan_ucentral_schema_url, latest_version_id, previous_version_id, path):
        previous_schema_pretty_json = get_github_file(wlan_ucentral_schema_url, path, previous_version_id)
        updated_schema_pretty_json = get_github_file(wlan_ucentral_schema_url, path, latest_version_id)
        allure.attach(previous_schema_pretty_json, name=f"OLD {path}:")
        allure.attach(updated_schema_pretty_json, name=f"NEW {path}:")

        if updated_schema_pretty_json == previous_schema_pretty_json:
            logging.info(f"No changes were found at {path}. Exiting.")
            allure.attach(name=f"No changes found at {path}", body=f"No changes were found at {path}. Exiting the test.")
            return None, None, None
        else:
            logging.info(f"Changes found at {path}. Proceeding with the comparison.")
            added_keys, removed_keys, changed_items = compare_dicts(json.loads(previous_schema_pretty_json),
                                                                    json.loads(updated_schema_pretty_json))
            return added_keys, removed_keys, changed_items

    def convert_changed_items_to_vertical_table(changed_items):
        formatted_rows = []
        for path, old, new in changed_items:
            formatted_rows.append(["Key Path", path])
            formatted_rows.append(["Old Value", old])
            formatted_rows.append(["New Value", new])
            formatted_rows.append(["", ""])  # Add blank line between entries
        return tabulate(formatted_rows, headers=["Field", "Content"], tablefmt="fancy_grid")

    if commit_id is None:
        logging.info("Use --commit-id to the pass an old commit-id of tip/wlan-ucentral-schema repo. Skipping the test.")
        pytest.skip("Use --commit-id to the pass an old commit-id of tip/wlan-ucentral-schema repo. Skipping the test.")

    latest_version_id = get_commit_id(owner="Telecominfraproject", repo="wlan-ucentral-schema")
    logging.info(f"Latest Commit-ID of wlan-ucentral-schema = {latest_version_id}")
    allure.attach(latest_version_id, name="Latest commit-id of wlan-ucentral-schema:")

    previous_version_id = commit_id
    logging.info(f"Passed Commit-ID of wlan-ucentral-schema: {previous_version_id}")
    allure.attach(previous_version_id, name=f"Passed Commit-ID of wlan-ucentral-schema:")

    if latest_version_id == previous_version_id:
        logging.info("No new commit-id found in wlan-ucentral-schema. Exiting.")
        return
    logging.info("New commit found. Proceeding with the schema validation.")

    wlan_ucentral_schema_url = "https://github.com/Telecominfraproject/wlan-ucentral-schema/blob/main"
    added_keys, removed_keys, changed_items = (
        generate_diff(wlan_ucentral_schema_url, latest_version_id, previous_version_id, path=path))

    if added_keys or removed_keys or changed_items:
        logging.info(f"Differences found in the schema:")
        if added_keys:
            added_keys = [list(key) for key in added_keys]
            added_keys = sorted(added_keys)
            message = ("Note: These keys were not present in old schema and have been added in the new schema.\n\n"
                       + tabulate(added_keys, headers=['Key Paths', 'Values'], tablefmt='fancy_grid'))
            logging.info("\nAdded keys:\n" + message + "\n")
            allure.attach(message, name="Added keys:")
        if removed_keys:
            removed_keys = [[key] for key in removed_keys]
            removed_keys = sorted(removed_keys)
            message = ("Note: These keys were present in the old schema but have been removed in the new schema.\n\n"
                       + tabulate(removed_keys, headers=['Key Paths'], tablefmt='fancy_grid'))
            logging.info("\nRemoved keys:\n" + message + "\n")
            allure.attach(message, name="Removed keys:")
        if changed_items:
            changed_items = [list(key) for key in changed_items]
            changed_items = sorted(changed_items)
            message = (
                    "Note: The following key paths have modified values:\n\n"
                    + convert_changed_items_to_vertical_table(changed_items)
            )
            logging.info("\nChanged Items:\n" + message + "\n")
            allure.attach(message, name="Changed items:")
        pytest.fail(f"Differences found in the schema, check Test Body for Added/Removed/Changed items")
    return


def validate_state_message_through_ap(test_object, target_object, config_data, ssid=None):
    def get_type_of_message(message):
        type_of_message = "unknown"
        if isinstance(message, dict):
            type_of_message = "object"
        elif isinstance(message, list):
            type_of_message = "array"
        elif isinstance(message, int):
            type_of_message = "integer"
        elif isinstance(message, float):
            type_of_message = "number"
        elif isinstance(message, str):
            type_of_message = "string"
        return type_of_message

    def verify_type_of_value(message, schema, path):
        if '$ref' in schema:
            return verify_type_of_value(message,
                                        full_schema[schema['$ref'].split('/')[1]][schema['$ref'].split('/')[2]],
                                        path)

        nonlocal missing_keys, type_mismatch, enum_mismatch, pattern_mismatch, other_discrepancies
        if 'enum' in schema:
            if message not in schema['enum']:
                enum_mismatch.add(f"{path} = '{message}' is not in the schema enum: {schema['enum']}.")

        if 'type' not in schema:
            discrepancy = f"Type not defined in schema for '{path}'. "
            if 'properties' in schema:
                discrepancy += f"Assumed type as 'object' for this path to continue."
                schema['type'] = 'object'
            elif 'items' in schema:
                discrepancy += f"Assumed type as 'array' for this path to continue."
                schema['type'] = 'array'
            else:
                discrepancy += "Could not validate this path any further."
                other_discrepancies.add(discrepancy)
                return
            other_discrepancies.add(discrepancy)

        if schema['type'] == 'integer':
            if not isinstance(message, int):
                type_mismatch.add((path, get_type_of_message(message), 'integer'))
        elif schema['type'] == 'number':
            if not isinstance(message, int) and not isinstance(message, float):
                type_mismatch.add((path, get_type_of_message(message), 'number'))
        elif schema['type'] == 'string':
            if not isinstance(message, str):
                type_mismatch.add((path, get_type_of_message(message), 'string'))
        elif schema['type'] == 'array':
            if not isinstance(message, list):
                type_mismatch.add((path, get_type_of_message(message), 'array'))
                return
            if 'properties' in schema:
                other_discrepancies.add(f"An array can't have properties, at '{path}'.")
            if 'items' not in schema:
                other_discrepancies.add(f"Items not defined in schema for array at '{path}'.")
                return
            for i in range(len(message)):
                verify_type_of_value(message[i], schema['items'], f"{path} > [item]")
        elif schema['type'] == 'object':
            if not isinstance(message, dict):
                type_mismatch.add((path, get_type_of_message(message), 'object'))
                return
            if 'items' in schema:
                other_discrepancies.add(f"An object can't have items, at '{path}'.")
            if 'properties' not in schema and 'patternProperties' not in schema and '$ref' not in schema:
                other_discrepancies.add(f"Properties not defined in schema for object at '{path}'.")
                return
            for key in message:
                if 'patternProperties' in schema:
                    pattern = ""
                    for key_name in schema['patternProperties']:
                        pattern = key_name
                    if not re.match(pattern, key, re.IGNORECASE):
                        pattern_mismatch.add(f"Key name '{path} > \"{key}\"' does not match the pattern '{pattern}'"
                                             f" in schema.")
                    return verify_type_of_value(message[key], schema['patternProperties'][pattern],
                                                f"{path} > {key}")
                if key == '$ref':
                    if 'ref' not in schema['properties']:
                        missing_keys.add(f'{path}.ref')
                        continue
                    else:
                        return verify_type_of_value(message['$ref'], schema['properties']['ref'],
                                                    f"{path}.'$ref'")
                elif 'properties' in schema and key not in schema['properties']:
                    missing_keys.add(f'{path} > {key}')
                    continue
                verify_type_of_value(message[key], schema['properties'][key], f"{path} > {key}")

    for ap in range(len(target_object.device_under_tests_info)):
        serial_number = target_object.device_under_tests_info[ap]['identifier']
        logging.info(f"Configuration : {config_data}")
        payload = {"configuration": json.dumps(config_data), "serialNumber": serial_number, "UUID": 1}
        uri = target_object.firmware_library_object.sdk_client.build_uri(
            "device/" + serial_number + "/configure")
        logging.info("Sending Command: " + "\n" + str(uri) + "\n" +
                     "TimeStamp: " + str(datetime.utcnow()) + "\n" +
                     "Data: " + str(json.dumps(payload, indent=2)) + "\n" +
                     "Headers: " + str(target_object.firmware_library_object.sdk_client.make_headers()))
        allure.attach(name="Push Config:", body="Sending Command: " + "\n" + str(uri) + "\n" +
                                                "TimeStamp: " + str(datetime.utcnow()) + "\n" +
                                                "Data: " + str(payload) + "\n" +
                                                "Headers: " + str(
            target_object.firmware_library_object.sdk_client.make_headers()))
        resp = requests.post(uri, data=json.dumps(payload),
                             headers=target_object.firmware_library_object.sdk_client.make_headers(),
                             verify=False, timeout=120)
        logging.info(resp.json())
        allure.attach(name=f"Response - {resp.status_code}{resp.reason}", body=str(resp.json()))
        if int(resp.status_code) == 200:
            time.sleep(120)
        else:
            pytest.fail("Configuration Push Failed")

        # check RX message from AP after config push
        target_object.dut_library_object.get_dut_logs()

        # get pushed config from ap
        target_object.dut_library_object.run_generic_command(cmd="cat /etc/ucentral/ucentral.active",
                                                                 attach_allure=True)
        # check ssid info in iwinfo
        iw_info = target_object.dut_library_object.get_iwinfo()
        if iw_info is not None:
            matches = re.findall(r'(\S+)\s+ESSID:\s+"(.*?)"', iw_info)
            if matches and len(matches) != 0:
                data = {interface: essid for interface, essid in matches}
                logging.info(f"All available interfaces and ssid:\n{data}")
            else:
                pytest.fail("Some or ALL Configured SSID's are not present in iwinfo")

        radio_5g = None
        dict_all_radios_5g = {"wave2_5g_radios": test_object.wave2_5g_radios,
                              "wave1_radios": test_object.wave1_radios,
                              "mtk_radios": test_object.mtk_radios,
                              "ax200_radios": test_object.ax200_radios,
                              "be200_radios": test_object.be200_radios,
                              "ax210_radios": test_object.ax210_radios}
        for radio in dict_all_radios_5g:
            if len(dict_all_radios_5g[radio]) > 0:
                radio_5g = dict_all_radios_5g[radio][0]
                break

        logging.info(f"ssid:{ssid}")
        test_object.pre_cleanup()
        fiveg_sta_got_ip = test_object.client_connect_using_radio(ssid=ssid,
                                                                       passkey="OpenWifi",
                                                                       security="wpa2", radio=radio_5g,
                                                                       station_name=["station-5G"],
                                                                       attach_port_info=False,
                                                                       attach_station_data=False)
        if not fiveg_sta_got_ip:
            logging.info("Station did not get IP address")
            pytest.fail("Station did not get IP address")

        logging.info("Waiting for 30 seconds before fetching state message...")
        time.sleep(30)

        # Fetching the schema from GitHub
        full_schema = get_github_file("https://github.com/Telecominfraproject/wlan-ucentral-schema/blob/main"
                                      "/ucentral.state.pretty.json")
        logging.info(f"State Schema: \n{full_schema}")
        allure.attach(full_schema, name=f"Schema:")
        full_schema = json.loads(full_schema)

        # Fetching the state message from AP
        full_message = target_object.get_dut_library_object().run_generic_command(cmd="cat /tmp/ucentral.state",
                                                                                      idx=ap, print_log=True)
        try:
            full_message = json.dumps(json.loads(full_message), indent=4)
        except json.JSONDecodeError:
            logging.info("Extra characters appeared as part of the state message from AP!")
            allure.attach(full_message, name="Response with extra characters as received from AP:")
            logging.info("Trying to remove extra characters.")
            full_message = '{' + re.split(r"{", full_message, maxsplit=1)[1].strip()
            try:
                full_message = json.dumps(json.loads(full_message), indent=4)
            except json.JSONDecodeError:
                logging.info("Failed to remove the extra unwanted characters.")
                logging.info(f"State Message after trial: \n{full_message}")
                pytest.fail("Extra characters appeared as part of the state message from AP!")
        logging.info(f"State Message: \n{full_message}")
        allure.attach(full_message, name=f"State Message:")
        full_message = json.loads(full_message)

        for key in full_message["state"]:
            full_message[key] = full_message["state"][key]
        del full_message["state"]

        missing_keys = set()
        type_mismatch = set()
        enum_mismatch = set()
        pattern_mismatch = set()
        other_discrepancies = set()

        if full_schema['type'] == 'object':
            if not isinstance(full_message, dict):
                type_mismatch.add(("State Message", 'unknown', 'object'))
            else:
                for key in full_message:
                    if (key == '$ref' and 'ref' not in full_schema['properties']) or (
                            key not in full_schema['properties']):
                        missing_keys.add(key)
                        continue
                    verify_type_of_value(full_message[key], full_schema['properties'][key], key)
        else:
            logging.info(
                f"Did not expect type of state message in the schema to be {full_schema['type']} and not 'object'.")
            pytest.skip(
                f"Did not expect type of state message in the schema to be {full_schema['type']} and not 'object'.")

        if missing_keys or type_mismatch or enum_mismatch or pattern_mismatch or other_discrepancies:
            logging.info("Detected Discrepancies:\n")
            if missing_keys:
                missing_keys = [[key] for key in missing_keys]
                missing_keys = sorted(missing_keys)
                message = ("Note: These keys are present in the state message received from AP but missing in the "
                           "state schema.\n\n" + tabulate(missing_keys, headers=['Key Paths'], tablefmt='fancy_grid'))
                logging.info("\nMissing Keys:\n" + message + "\n")
                allure.attach(message, name="Missing keys:")
            if type_mismatch:
                type_mismatch = [list(key) for key in type_mismatch]
                type_mismatch = sorted(type_mismatch)
                message = ("Note: The type of values present in the state message received from AP is different "
                           "from the one described in the state schema.\n\n"
                           + tabulate(type_mismatch, headers=['Key Path', 'Type in State Message'
                            , 'Type according to State Schema'], tablefmt='fancy_grid'))
                logging.info("\nType Mismatches:\n" + message + "\n")
                allure.attach(message, name="Type Mismatches:")
            if enum_mismatch:
                enum_mismatch = [[key] for key in enum_mismatch]
                enum_mismatch = sorted(enum_mismatch)
                message = ("Note: Enums are predefined possible values of a key in the schema, the value present at "
                           "the following keys are not part of the enum in state schema.\n\n"
                           + tabulate(enum_mismatch, tablefmt='fancy_grid'))
                logging.info("\nEnum Mismatches:\n" + message + "\n")
                allure.attach(message, name="Enum Mismatches:")
            if pattern_mismatch:
                pattern_mismatch = [[key] for key in pattern_mismatch]
                pattern_mismatch = sorted(pattern_mismatch)
                message = ("Note: Patterns are defined for some of the keys in the schema, the key name present "
                           "inside the state message does not match the specified pattern in the state "
                           "schema.\n\n" + tabulate(pattern_mismatch, tablefmt='fancy_grid'))
                logging.info("\nPattern Mismatches:\n" + message + "\n")
                allure.attach(message, name="Pattern Mismatches:")
            if other_discrepancies:
                other_discrepancies = [[key] for key in other_discrepancies]
                other_discrepancies = sorted(other_discrepancies)
                message = ("Note: These are possible problems with the schema itself.\n\n" +
                           tabulate(other_discrepancies, tablefmt='fancy_grid'))
                logging.info("\nOther Discrepancies:\n" + message + "\n")
                allure.attach(message, name="Other Discrepancies:")

            pytest.fail("Detected Discrepancies: Check Test Body for Missing Keys or Type/Pattern/Enum Mismatches")
        else:
            logging.info("No discrepancies found.")


@allure.feature("Schema Validation")
@allure.parent_suite("Schema Validation")
@allure.suite("Through GitHub")
@pytest.mark.through_github
class TestSchemaValidationThroughGitHub(object):
    @allure.sub_suite("Schema JSON")
    @pytest.mark.schema_json
    @allure.title("Checking ucentral.schema.json")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13443", name="WIFI-13443")
    def test_schema_through_github(self, commit_id):
        """
        Validating the ucentral schema to ensure consistency and integrity in the system. The validation process
        involves detecting any changes in the schema YML files and comparing them periodically after any new commits
        int the wlan-ucentral-schema repo.

        Objective is to identify any modifications, additions, or removals in the file: ucentral.schema.json.

        Unique Marker:
        schema_validation and through_github and schema_json
        """
        validate_schema_through_github(commit_id, "/ucentral.schema.json")


    @allure.sub_suite("Schema JSON")
    @pytest.mark.schema_full_json
    @allure.title("Checking ucentral.schema.full.json")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13443", name="WIFI-13443")
    def test_schema_full_through_github(self, commit_id):
        """
        Validating the ucentral schema to ensure consistency and integrity in the system. The validation process
        involves detecting any changes in the schema YML files and comparing them periodically after any new commits
        int the wlan-ucentral-schema repo.

        Objective is to identify any modifications, additions, or removals in the file: ucentral.schema.full.json.

        Unique Marker:
        schema_validation and through_github and schema_full_json
        """
        validate_schema_through_github(commit_id, "/ucentral.schema.full.json")

    @allure.sub_suite("Schema JSON")
    @pytest.mark.schema_pretty_json
    @allure.title("Checking ucentral.schema.pretty.json")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13443", name="WIFI-13443")
    def test_schema_pretty_through_github(self, commit_id):
        """
        Validating the ucentral schema to ensure consistency and integrity in the system. The validation process
        involves detecting any changes in the schema YML files and comparing them periodically after any new commits
        int the wlan-ucentral-schema repo.

        Objective is to identify any modifications, additions, or removals in the file: ucentral.schema.pretty.json.

        Unique Marker:
        schema_validation and through_github and schema_pretty_json
        """
        validate_schema_through_github(commit_id, "/ucentral.schema.pretty.json")

    @allure.sub_suite("State JSON")
    @pytest.mark.state_pretty_json
    @allure.title("Checking ucentral.state.pretty.json")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13443", name="WIFI-13443")
    def test_state_pretty_through_github(self, commit_id):
        """
        Validating the ucentral schema to ensure consistency and integrity in the system. The validation process
        involves detecting any changes in the schema YML files and comparing them periodically after any new commits
        int the wlan-ucentral-schema repo.

        Objective is to identify any modifications, additions, or removals in the file: ucentral.state.pretty.json.

        Unique Marker:
        schema_validation and through_github and state_pretty_json
        """
        validate_schema_through_github(commit_id, "/ucentral.state.pretty.json")


@allure.feature("Schema Validation")
@allure.parent_suite("Schema Validation")
@allure.suite("Through AP")
@allure.sub_suite("Schema Validation through State Messages")
@pytest.mark.through_ap_terminal
class TestSchemaValidationThroughAPTerminal(object):
    @pytest.mark.master_config_1
    @allure.title("Pushing master config-1")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13567", name="WIFI-13567")
    def test_state_message_schema_master_config_1(self, get_test_library, get_target_object, get_dut_logs_per_test_case,
                                                  get_test_device_logs, check_connectivity):
        """
        Validating the ucentral schema to ensure consistency and integrity in the system. The validation 
        process involves detecting any changes in the schema YML files and comparing them between the 
        live current state received from the AP and out ucentral state json output file.

        Objective is to detect discrepancies in data types (e.g., string to integer) and object structures.

        Unique Marker:
        schema_validation and through_ap_terminal and master_config_1
        """
        ssid = "captive-credential-4"
        validate_state_message_through_ap(get_test_library, get_target_object, config_data=config_data_1, ssid=ssid)

    @pytest.mark.master_config_2
    @allure.title("Pushing master config-2")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13567", name="WIFI-13567")
    def test_state_message_schema_master_config_2(self, get_test_library, get_target_object, get_dut_logs_per_test_case,
                                                  get_test_device_logs, check_connectivity):
        """
        Validating the ucentral schema to ensure consistency and integrity in the system. The validation
        process involves detecting any changes in the schema YML files and comparing them between the
        live current state received from the AP and out ucentral state json output file.

        Objective is to detect discrepancies in data types (e.g., string to integer) and object structures.

        Unique Marker:
        schema_validation and through_ap_terminal and master_config_2
        """
        ssid = "captive-uam-8"
        validate_state_message_through_ap(get_test_library, get_target_object, config_data=config_data_2, ssid=ssid)

    @pytest.mark.master_config_3
    @allure.title("Pushing master config-3")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13567", name="WIFI-13567")
    def test_state_message_schema_master_config_3(self, get_test_library, get_target_object, get_dut_logs_per_test_case,
                                                  get_test_device_logs, check_connectivity):
        """
        Validating the ucentral schema to ensure consistency and integrity in the system. The validation
        process involves detecting any changes in the schema YML files and comparing them between the
        live current state received from the AP and out ucentral state json output file.

        Objective is to detect discrepancies in data types (e.g., string to integer) and object structures.

        Unique Marker:
        schema_validation and through_ap_terminal and master_config_3
        """
        ssid = "Uchannel-ds-4"
        validate_state_message_through_ap(get_test_library, get_target_object, config_data=config_data_3, ssid=ssid)
