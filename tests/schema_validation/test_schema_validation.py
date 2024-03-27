import pytest
import allure
import logging
import json
import requests

pytestmark = [pytest.mark.schema_validation]


def make_raw_url(url):
    return url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")


def get_github_file(url, path, commit_id=None):
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
        logging.info(f"Commit-ID of {url}{path} is {commit_id}")
        return commit_id
    else:
        logging.info(f"Failed to fetch commit-id. Status code: {response.status_code}")


def get_version_id_from_wlan_ap_repo(commit_id=None):
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
        logging.info("Line containing PKG_SOURCE_VERSION not found.")
    else:
        logging.info(f"Failed to fetch file content. Status code: {response.status_code}")


def compare_dicts(dict1, dict2, path="", added_keys=set(), removed_keys=set(), changed_items=[]):
    for key in set(dict1.keys()) | set(dict2.keys()):
        new_path = f"{path}.{key}" if path else key

        if key not in dict1:
            added_keys.add(new_path)
        elif key not in dict2:
            removed_keys.add(new_path)
        elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            added_keys, removed_keys, changed_items = compare_dicts(dict1[key], dict2[key], path=new_path,
                                                                    added_keys=added_keys, removed_keys=removed_keys,
                                                                    changed_items=changed_items)
        elif dict1[key] != dict2[key]:
            changed_items.append((new_path, dict1[key], dict2[key]))

    return added_keys, removed_keys, changed_items


def get_differences(added_keys, removed_keys, changed_items, filename="result.txt"):
    differences = ""
    if added_keys:
        differences += "Added keys:\n"
        differences += "\n".join(added_keys)
    if removed_keys:
        differences += "\n\nRemoved keys:\n"
        differences += "\n".join(removed_keys)
    if changed_items:
        differences += "\n\nChanged items:\n"
        for path, old_value, new_value in changed_items:
            differences += f"{path}: {old_value} -> {new_value}\n"
    return differences


def generate_diff(wlan_ucentral_schema_url, latest_version_id, previous_version_id, path, filename):
    previous_schema_pretty_json = get_github_file(wlan_ucentral_schema_url, path, previous_version_id)
    updated_schema_pretty_json = get_github_file(wlan_ucentral_schema_url, path, latest_version_id)
    allure.attach(previous_schema_pretty_json, name=f"OLD {path}:")
    allure.attach(updated_schema_pretty_json, name=f"NEW {path}:")

    if updated_schema_pretty_json == previous_schema_pretty_json:
        logging.info(f"No changes found at {path}. Exiting.")
        return None
    else:
        logging.info(f"Changes found at {path}. Proceeding with the comparison.")
        added_keys, removed_keys, changed_items = compare_dicts(json.loads(previous_schema_pretty_json),
                                                                json.loads(updated_schema_pretty_json))
        return get_differences(added_keys, removed_keys, changed_items, filename=filename)


@allure.feature("Schema Validation")
@allure.parent_suite("Schema Validation")
@allure.suite("Through GitHub")
class TestSchemaValidation(object):
    @pytest.mark.parametrize("path, filename",
                             [("/ucentral.state.pretty.json", "diff_ucentral_state_pretty.txt"),
                              ("/ucentral.schema.pretty.json", "diff_ucentral_schema_pretty.txt"),
                              ("/ucentral.schema.json", "diff_ucentral_schema.txt"),
                              ("/ucentral.schema.full.json", "diff_ucentral_schema_full.txt")])
    @allure.title("Checking {path}")
    def test_schema(self, path, filename):
        allure.dynamic.sub_suite("State JSON" if "state" in path else "Schema JSON")

        latest_makefile_commit_id = get_commit_id(owner="Telecominfraproject", repo="wlan-ap",
                                                  path="/feeds/ucentral/ucentral-schema/Makefile")
        with open("schema_validation/base.txt", "r") as file:
            previous_makefile_commit_id = file.read().strip()
            logging.info(f"Previously checked Commit-ID = {previous_makefile_commit_id}")

        if latest_makefile_commit_id == previous_makefile_commit_id:
            logging.info("No new commits in the Makefile (wlan-ap). Exiting.")
            return
        logging.info("New commits found in the Makefile (wlan-ap). Proceeding with the schema validation.")

        latest_version_id = get_version_id_from_wlan_ap_repo()
        logging.info(f"Latest Commit-ID of wlan-ucentral-schema according to latest Makefile = {latest_version_id}")

        previous_version_id = get_version_id_from_wlan_ap_repo(previous_makefile_commit_id)
        logging.info(
            f"Previous Commit-ID of wlan-ucentral-schema according to previous Makefile = {previous_version_id}")

        if latest_version_id == previous_version_id:
            logging.info("No new Schema-ID found. Exiting.")
            return
        logging.info("New Schema-ID found. Proceeding with the schema validation.")

        wlan_ucentral_schema_url = "https://github.com/Telecominfraproject/wlan-ucentral-schema/blob/main"
        differences = generate_diff(wlan_ucentral_schema_url, latest_version_id, previous_version_id,
                                    path=path, filename=filename)

        if differences is not None:
            logging.info(f"Differences: \n{differences}\n")
            pytest.fail(f"Differences found in the schema: \n{differences}")
        return

    @classmethod
    def teardown_class(cls):
        latest_makefile_commit_id = get_commit_id(owner="Telecominfraproject", repo="wlan-ap",
                                                  path="/feeds/ucentral/ucentral-schema/Makefile")
        with open("schema_validation/base.txt", "r") as file:
            previous_makefile_commit_id = file.read().strip()
        with open("schema_validation/base.txt", "w") as file:
            file.write(str(latest_makefile_commit_id))
            logging.info(f"Updated schema_validation/base.txt with the latest Makefile commit-id: "
                         f"{latest_makefile_commit_id}, replacing: {previous_makefile_commit_id}.")