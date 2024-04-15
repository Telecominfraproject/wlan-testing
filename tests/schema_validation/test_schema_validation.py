import pytest
import allure
import logging
import json
import requests
import re
from tabulate import tabulate

pytestmark = [pytest.mark.schema_validation]


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
        logging.info(f"Failed to fetch {path}. Status code: {response.status_code}")
    return response.text


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


def extract_pkg_src_version_from_makefile(commit_id=None):
    wlan_ap_url = make_raw_url("https://github.com/Telecominfraproject/wlan-ap/blob/main/feeds/ucentral/ucentral-schema"
                               "/Makefile")
    if commit_id:
        wlan_ap_url = wlan_ap_url.replace("main", commit_id)
    response = requests.get(wlan_ap_url)
    if response.status_code == 200:
        lines = response.text.split('\n')
        for line in lines:
            if line.startswith("PKG_SOURCE_VERSION:="):
                return line.split(":=")[1].strip()
        logging.info("Line containing PKG_SOURCE_VERSION not found in Makefile.")
        pytest.fail("Line containing PKG_SOURCE_VERSION not found in Makefile.")
    else:
        logging.info(f"Failed to fetch file content. Status code: {response.status_code}")


def compare_dicts(dict1, dict2, path="", added_keys=None, removed_keys=None, changed_items=None):
    if changed_items is None:
        changed_items = []
    if removed_keys is None:
        removed_keys = set()
    if added_keys is None:
        added_keys = set()

    for key in set(dict1.keys()) | set(dict2.keys()):
        new_path = f"{path} > {key}" if path else key

        if key not in dict1:
            added_keys.add(new_path + f" : {dict2[key]}")
        elif key not in dict2:
            removed_keys.add(new_path)
        elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            added_keys, removed_keys, changed_items = compare_dicts(dict1[key], dict2[key], path=new_path,
                                                                    added_keys=added_keys, removed_keys=removed_keys,
                                                                    changed_items=changed_items)
        elif dict1[key] != dict2[key]:
            changed_items.append((new_path, dict1[key], dict2[key]))

    return added_keys, removed_keys, changed_items


def generate_diff(wlan_ucentral_schema_url, latest_version_id, previous_version_id, path):
    previous_schema_pretty_json = get_github_file(wlan_ucentral_schema_url, path, previous_version_id)
    updated_schema_pretty_json = get_github_file(wlan_ucentral_schema_url, path, latest_version_id)
    allure.attach(previous_schema_pretty_json, name=f"OLD {path}:")
    allure.attach(updated_schema_pretty_json, name=f"NEW {path}:")

    if updated_schema_pretty_json == previous_schema_pretty_json:
        logging.info(f"No changes found at {path}. Exiting.")
        return None, None, None
    else:
        logging.info(f"Changes found at {path}. Proceeding with the comparison.")
        added_keys, removed_keys, changed_items = compare_dicts(json.loads(previous_schema_pretty_json),
                                                                json.loads(updated_schema_pretty_json))
        return added_keys, removed_keys, changed_items


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

        Objective is to identify any modifications, additions, or removals in the schema.

        Unique Marker:
        schema_validation and through_github and schema_json
        """

        if commit_id is None:
            logging.info("Use --commit-id to the pass an old commit-id of tip/wlan-ap repo. Skipping the test.")
            pytest.skip("Use --commit-id to the pass an old commit-id of tip/wlan-ap repo. Skipping the test.")

        latest_makefile_commit_id = get_commit_id(owner="Telecominfraproject", repo="wlan-ap")
        previous_makefile_commit_id = commit_id

        allure.attach(latest_makefile_commit_id, name="Latest commit-id of wlan-ap:")
        allure.attach(previous_makefile_commit_id, name="Passed commit-id to CLI:")

        logging.info(f"Latest Commit-ID of wlan-ap/feeds/ucentral/ucentral-schema/'Makefile' is {commit_id}")
        logging.info(f"Passed Commit-ID through CLI = {previous_makefile_commit_id}")

        if latest_makefile_commit_id == previous_makefile_commit_id:
            logging.info("No new commits in the Makefile (wlan-ap). Exiting.")
            return
        logging.info("New commits found in the Makefile (wlan-ap). Proceeding with the schema validation.")

        latest_version_id = extract_pkg_src_version_from_makefile()
        logging.info(f"Latest Commit-ID of wlan-ucentral-schema according to latest Makefile = {latest_version_id}")
        allure.attach(latest_version_id, name="PKG_SOURCE_VERSION (a/c to latest):")

        previous_version_id = extract_pkg_src_version_from_makefile(previous_makefile_commit_id)
        if previous_version_id is None:
            logging.info(f"Invalid Commit-ID passed through CLI. Commit-ID must be one from "
                        f"telecominfraproject/wlan-ap repo. Skipping the test.")
            pytest.skip(f"Invalid Commit-ID passed through CLI. Commit-ID must be one from "
                        f"telecominfraproject/wlan-ap repo. Skipping the test.")
        logging.info(f"Commit-ID of wlan-ucentral-schema according to the passed Commit-ID = {previous_version_id}")
        allure.attach(previous_version_id, name=f"PKG_SOURCE_VERSION (a/c to passed commit-id):")

        if latest_version_id == previous_version_id:
            logging.info("No new Schema-ID found. Exiting.")
            return
        logging.info("New Schema-ID found. Proceeding with the schema validation.")

        wlan_ucentral_schema_url = "https://github.com/Telecominfraproject/wlan-ucentral-schema/blob/main"
        added_keys, removed_keys, changed_items = (
            generate_diff(wlan_ucentral_schema_url, latest_version_id, previous_version_id,
                          path="/ucentral.schema.json"))

        if added_keys or removed_keys or changed_items:
            logging.info(f"Differences found in the schema:")
            if added_keys:
                logging.info("\n\nAdded keys:" + "\n" + "\n".join(added_keys))
                allure.attach("\n".join(added_keys), name="Added keys:")
            if removed_keys:
                logging.info("\n\nRemoved keys:" + "\n" + "\n".join(removed_keys))
                allure.attach("\n".join(removed_keys), name="Removed keys:")
            if changed_items:
                message = ""
                for path, old_value, new_value in changed_items:
                    message += f"{path}: {old_value} --> {new_value}\n"
                logging.info("\n\nChanged items:" + "\n" + message)
                allure.attach(message, name="Changed items:")
            pytest.fail(f"Differences found in the schema, check Test Body for Added/Removed/Changed items")
        return

    @allure.sub_suite("Schema JSON")
    @pytest.mark.schema_full_json
    @allure.title("Checking ucentral.schema.full.json")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13443", name="WIFI-13443")
    def test_schema_full_through_github(self, commit_id):
        """
        Validating the ucentral schema to ensure consistency and integrity in the system. The validation process
        involves detecting any changes in the schema YML files and comparing them periodically after any new commits
        int the wlan-ucentral-schema repo.

        Objective is to identify any modifications, additions, or removals in the schema.

        Unique Marker:
        schema_validation and through_github and schema_full_json
        """

        if commit_id is None:
            logging.info("Use --commit-id to the pass an old commit-id of tip/wlan-ap repo. Skipping the test.")
            pytest.skip("Use --commit-id to the pass an old commit-id of tip/wlan-ap repo. Skipping the test.")

        latest_makefile_commit_id = get_commit_id(owner="Telecominfraproject", repo="wlan-ap")
        previous_makefile_commit_id = commit_id

        allure.attach(latest_makefile_commit_id, name="Latest commit-id of wlan-ap:")
        allure.attach(previous_makefile_commit_id, name="Passed commit-id to CLI:")

        logging.info(f"Latest Commit-ID of wlan-ap/feeds/ucentral/ucentral-schema/'Makefile' is {commit_id}")
        logging.info(f"Passed Commit-ID through CLI = {previous_makefile_commit_id}")

        if latest_makefile_commit_id == previous_makefile_commit_id:
            logging.info("No new commits in the Makefile (wlan-ap). Exiting.")
            return
        logging.info("New commits found in the Makefile (wlan-ap). Proceeding with the schema validation.")

        latest_version_id = extract_pkg_src_version_from_makefile()
        logging.info(f"Latest Commit-ID of wlan-ucentral-schema according to latest Makefile = {latest_version_id}")
        allure.attach(latest_version_id, name="PKG_SOURCE_VERSION (a/c to latest):")

        previous_version_id = extract_pkg_src_version_from_makefile(previous_makefile_commit_id)
        if previous_version_id is None:
            logging.info(f"Invalid Commit-ID passed through CLI. Commit-ID must be one from "
                         f"telecominfraproject/wlan-ap repo. Skipping the test.")
            pytest.skip(f"Invalid Commit-ID passed through CLI. Commit-ID must be one from "
                        f"telecominfraproject/wlan-ap repo. Skipping the test.")
        logging.info(f"Commit-ID of wlan-ucentral-schema according to the passed Commit-ID = {previous_version_id}")
        allure.attach(previous_version_id, name=f"PKG_SOURCE_VERSION (a/c to passed commit-id):")

        if latest_version_id == previous_version_id:
            logging.info("No new Schema-ID found. Exiting.")
            return
        logging.info("New Schema-ID found. Proceeding with the schema validation.")

        wlan_ucentral_schema_url = "https://github.com/Telecominfraproject/wlan-ucentral-schema/blob/main"
        added_keys, removed_keys, changed_items = (
            generate_diff(wlan_ucentral_schema_url, latest_version_id, previous_version_id,
                          path="/ucentral.schema.full.json"))

        if added_keys or removed_keys or changed_items:
            logging.info(f"Differences found in the schema:")
            if added_keys:
                logging.info("\n\nAdded keys:" + "\n" + "\n".join(added_keys))
                allure.attach("\n".join(added_keys), name="Added keys:")
            if removed_keys:
                logging.info("\n\nRemoved keys:" + "\n" + "\n".join(removed_keys))
                allure.attach("\n".join(removed_keys), name="Removed keys:")
            if changed_items:
                message = ""
                for path, old_value, new_value in changed_items:
                    message += f"{path}: {old_value} --> {new_value}\n"
                logging.info("\n\nChanged items:" + "\n" + message)
                allure.attach(message, name="Changed items:")
            pytest.fail(f"Differences found in the schema, check Test Body for Added/Removed/Changed items")
        return

    @allure.sub_suite("Schema JSON")
    @pytest.mark.schema_pretty_json
    @allure.title("Checking ucentral.schema.pretty.json")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13443", name="WIFI-13443")
    def test_schema_pretty_through_github(self, commit_id):
        """
        Validating the ucentral schema to ensure consistency and integrity in the system. The validation process
        involves detecting any changes in the schema YML files and comparing them periodically after any new commits
        int the wlan-ucentral-schema repo.

        Objective is to identify any modifications, additions, or removals in the schema.

        Unique Marker:
        schema_validation and through_github and schema_pretty_json
        """

        if commit_id is None:
            logging.info("Use --commit-id to the pass an old commit-id of tip/wlan-ap repo. Skipping the test.")
            pytest.skip("Use --commit-id to the pass an old commit-id of tip/wlan-ap repo. Skipping the test.")

        latest_makefile_commit_id = get_commit_id(owner="Telecominfraproject", repo="wlan-ap")
        previous_makefile_commit_id = commit_id

        allure.attach(latest_makefile_commit_id, name="Latest commit-id of wlan-ap:")
        allure.attach(previous_makefile_commit_id, name="Passed commit-id to CLI:")

        logging.info(f"Latest Commit-ID of wlan-ap/feeds/ucentral/ucentral-schema/'Makefile' is {commit_id}")
        logging.info(f"Passed Commit-ID through CLI = {previous_makefile_commit_id}")

        if latest_makefile_commit_id == previous_makefile_commit_id:
            logging.info("No new commits in the Makefile (wlan-ap). Exiting.")
            return
        logging.info("New commits found in the Makefile (wlan-ap). Proceeding with the schema validation.")

        latest_version_id = extract_pkg_src_version_from_makefile()
        logging.info(f"Latest Commit-ID of wlan-ucentral-schema according to latest Makefile = {latest_version_id}")
        allure.attach(latest_version_id, name="PKG_SOURCE_VERSION (a/c to latest):")

        previous_version_id = extract_pkg_src_version_from_makefile(previous_makefile_commit_id)
        if previous_version_id is None:
            logging.info(f"Invalid Commit-ID passed through CLI. Commit-ID must be one from "
                         f"telecominfraproject/wlan-ap repo. Skipping the test.")
            pytest.skip(f"Invalid Commit-ID passed through CLI. Commit-ID must be one from "
                        f"telecominfraproject/wlan-ap repo. Skipping the test.")
        logging.info(f"Commit-ID of wlan-ucentral-schema according to the passed Commit-ID = {previous_version_id}")
        allure.attach(previous_version_id, name=f"PKG_SOURCE_VERSION (a/c to passed commit-id):")

        if latest_version_id == previous_version_id:
            logging.info("No new Schema-ID found. Exiting.")
            return
        logging.info("New Schema-ID found. Proceeding with the schema validation.")

        wlan_ucentral_schema_url = "https://github.com/Telecominfraproject/wlan-ucentral-schema/blob/main"
        added_keys, removed_keys, changed_items = (
            generate_diff(wlan_ucentral_schema_url, latest_version_id, previous_version_id,
                          path="/ucentral.schema.pretty.json"))

        if added_keys or removed_keys or changed_items:
            logging.info(f"Differences found in the schema:")
            if added_keys:
                logging.info("\n\nAdded keys:" + "\n" + "\n".join(added_keys))
                allure.attach("\n".join(added_keys), name="Added keys:")
            if removed_keys:
                logging.info("\n\nRemoved keys:" + "\n" + "\n".join(removed_keys))
                allure.attach("\n".join(removed_keys), name="Removed keys:")
            if changed_items:
                message = ""
                for path, old_value, new_value in changed_items:
                    message += f"{path}: {old_value} --> {new_value}\n"
                logging.info("\n\nChanged items:" + "\n" + message)
                allure.attach(message, name="Changed items:")
            pytest.fail(f"Differences found in the schema, check Test Body for Added/Removed/Changed items")
        return

    @allure.sub_suite("State JSON")
    @pytest.mark.state_pretty_json
    @allure.title("Checking ucentral.state.pretty.json")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13443", name="WIFI-13443")
    def test_state_pretty_through_github(self, commit_id):
        """
        Validating the ucentral schema to ensure consistency and integrity in the system. The validation process
        involves detecting any changes in the schema YML files and comparing them periodically after any new commits
        int the wlan-ucentral-schema repo.

        Objective is to identify any modifications, additions, or removals in the schema.

        Unique Marker:
        schema_validation and through_github and state_pretty_json
        """

        if commit_id is None:
            logging.info("Use --commit-id to the pass an old commit-id of tip/wlan-ap repo. Skipping the test.")
            pytest.skip("Use --commit-id to the pass an old commit-id of tip/wlan-ap repo. Skipping the test.")

        latest_makefile_commit_id = get_commit_id(owner="Telecominfraproject", repo="wlan-ap")
        previous_makefile_commit_id = commit_id

        allure.attach(latest_makefile_commit_id, name="Latest commit-id of wlan-ap:")
        allure.attach(previous_makefile_commit_id, name="Passed commit-id to CLI:")

        logging.info(f"Latest Commit-ID of wlan-ap/feeds/ucentral/ucentral-schema/'Makefile' is {commit_id}")
        logging.info(f"Passed Commit-ID through CLI = {previous_makefile_commit_id}")

        if latest_makefile_commit_id == previous_makefile_commit_id:
            logging.info("No new commits in the Makefile (wlan-ap). Exiting.")
            return
        logging.info("New commits found in the Makefile (wlan-ap). Proceeding with the schema validation.")

        latest_version_id = extract_pkg_src_version_from_makefile()
        logging.info(f"Latest Commit-ID of wlan-ucentral-schema according to latest Makefile = {latest_version_id}")
        allure.attach(latest_version_id, name="PKG_SOURCE_VERSION (a/c to latest):")

        previous_version_id = extract_pkg_src_version_from_makefile(previous_makefile_commit_id)
        if previous_version_id is None:
            logging.info(f"Invalid Commit-ID passed through CLI. Commit-ID must be one from "
                         f"telecominfraproject/wlan-ap repo. Skipping the test.")
            pytest.skip(f"Invalid Commit-ID passed through CLI. Commit-ID must be one from "
                        f"telecominfraproject/wlan-ap repo. Skipping the test.")
        logging.info(f"Commit-ID of wlan-ucentral-schema according to the passed Commit-ID = {previous_version_id}")
        allure.attach(previous_version_id, name=f"PKG_SOURCE_VERSION (a/c to passed commit-id):")

        if latest_version_id == previous_version_id:
            logging.info("No new Schema-ID found. Exiting.")
            return
        logging.info("New Schema-ID found. Proceeding with the schema validation.")

        wlan_ucentral_schema_url = "https://github.com/Telecominfraproject/wlan-ucentral-schema/blob/main"
        added_keys, removed_keys, changed_items = (
            generate_diff(wlan_ucentral_schema_url, latest_version_id, previous_version_id,
                          path="/ucentral.state.pretty.json"))

        if added_keys or removed_keys or changed_items:
            logging.info(f"Differences found in the schema:")
            if added_keys:
                logging.info("\n\nAdded keys:" + "\n" + "\n".join(added_keys))
                allure.attach("\n".join(added_keys), name="Added keys:")
            if removed_keys:
                logging.info("\n\nRemoved keys:" + "\n" + "\n".join(removed_keys))
                allure.attach("\n".join(removed_keys), name="Removed keys:")
            if changed_items:
                message = ""
                for path, old_value, new_value in changed_items:
                    message += f"{path}: {old_value} --> {new_value}\n"
                logging.info("\n\nChanged items:" + "\n" + message)
                allure.attach(message, name="Changed items:")
            pytest.fail(f"Differences found in the schema, check Test Body for Added/Removed/Changed items")
        return


@allure.feature("Schema Validation")
@allure.parent_suite("Schema Validation")
@allure.suite("Through AP")
@allure.sub_suite("Schema Validation through State Messages")
@pytest.mark.through_ap_terminal
class TestSchemaValidationThroughAPTerminal(object):
    @allure.title("Schema Validation through AP State Messages")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13567", name="WIFI-13567")
    def test_state_message_schema_through_ap_terminal(self, get_target_object, get_dut_logs_per_test_case,
                                                      get_test_device_logs, check_connectivity):
        """
        Validating the ucentral schema to ensure consistency and integrity in the system. The validation 
        process involves detecting any changes in the schema YML files and comparing them between the 
        live current state received from the AP and out ucentral state json output file.

        Objective is to detect discrepancies in data types (e.g., string to integer) and object structures.

        Unique Marker:
        schema_validation and through_ap_terminal
        """

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
                for i in range(len(message)):
                    verify_type_of_value(message[i], schema['items'], f"{path} > [item]")
            elif schema['type'] == 'object':
                if not isinstance(message, dict):
                    type_mismatch.add((path, get_type_of_message(message), 'object'))
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
                    elif key not in schema['properties']:
                        missing_keys.add(f'{path} > {key}')
                        continue
                    verify_type_of_value(message[key], schema['properties'][key], f"{path} > {key}")

        # Fetching the schema from GitHub
        full_schema = get_github_file("https://github.com/Telecominfraproject/wlan-ucentral-schema/blob/main"
                                      "/ucentral.state.pretty.json")
        logging.info(f"State Schema: \n{full_schema}")
        allure.attach(full_schema, name=f"Schema:")
        full_schema = json.loads(full_schema)

        # Fetching the state message from AP
        full_message = get_target_object.get_dut_library_object().run_generic_command(cmd="cat /tmp/ucentral.state",
                                                                                      idx=0, print_log=True)
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
                message = tabulate(other_discrepancies, tablefmt='fancy_grid')
                logging.info("\nOther Discrepancies:\n" + message + "\n")
                allure.attach(message, name="Other Discrepancies:")

            pytest.fail("Detected Discrepancies: Check Test Body for Missing Keys or Type/Pattern/Enum Mismatches")
        else:
            logging.info("No discrepancies found.")
