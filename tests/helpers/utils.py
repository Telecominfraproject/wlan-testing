import re
import requests
import json
import argparse

# Map firmware directory name to cloud's model name.
cloud_sdk_models = {
    "ec420": "EC420-G1",
    "ea8300": "EA8300-CA",
    "ecw5211": "ECW5211",
    "ecw5410": "ECW5410",
    "wf188n": "WF188N"
    }

# To better interoperate with libs that want to take a cmd-line-args thing vs
# the pytest request config.
def create_command_line_args(request):
    parser = argparse.ArgumentParser(description="Fake")
    command_line_args, unknown = parser.parse_known_args()

    # And then overwrite it with whatever pytest is using (which is likely same in many cases)
    command_line_args.equipment_id = request.config.getoption("--equipment-id")
    command_line_args.customer_id = request.config.getoption("--customer-id")
    command_line_args.sdk_base_url = request.config.getoption("--sdk-base-url")
    command_line_args.sdk_user_id = request.config.getoption("--sdk-user-id")
    command_line_args.sdk_user_password = request.config.getoption("--sdk-user-password")
    command_line_args.default_ap_profile = request.config.getoption("--default-ap-profile")

    command_line_args.verbose = request.config.getoption("--verbose")
    
    command_line_args.ap_ip = request.config.getoption("--ap-ip")
    command_line_args.ap_username = request.config.getoption("--ap-username")
    command_line_args.ap_password = request.config.getoption("--ap-password")
    command_line_args.ap_jumphost_address = request.config.getoption("--ap-jumphost-address")
    command_line_args.ap_jumphost_username = request.config.getoption("--ap-jumphost-username")
    command_line_args.ap_jumphost_password = request.config.getoption("--ap-jumphost-password")
    command_line_args.ap_jumphost_port = request.config.getoption("--ap-jumphost-port")
    command_line_args.ap_jumphost_wlan_testing = request.config.getoption("--ap-jumphost-wlan-testing")  # directory
    command_line_args.ap_jumphost_tty = request.config.getoption("--ap-jumphost-tty")

    command_line_args.build_id = request.config.getoption("--build-id")
    command_line_args.testbed = request.config.getoption("--testbed")
    command_line_args.mode = request.config.getoption("--mode")
    command_line_args.skip_wpa = request.config.getoption("--skip-wpa")
    command_line_args.skip_wpa2 = request.config.getoption("--skip-wpa2")
    command_line_args.skip_radius = request.config.getoption("--skip-radius")
    command_line_args.skip_profiles = request.config.getoption("--skip-profiles")
    command_line_args.ssid_2g_wpa = request.config.getoption("--ssid-2g-wpa")
    command_line_args.ssid_5g_wpa = request.config.getoption("--ssid-5g-wpa")
    command_line_args.psk_2g_wpa = request.config.getoption("--psk-2g-wpa")
    command_line_args.psk_5g_wpa = request.config.getoption("--psk-5g-wpa")
    command_line_args.ssid_2g_wpa2 = request.config.getoption("--ssid-2g-wpa2")
    command_line_args.ssid_5g_wpa2 = request.config.getoption("--ssid-5g-wpa2")
    command_line_args.psk_2g_wpa2 = request.config.getoption("--psk-2g-wpa2")
    command_line_args.psk_5g_wpa2 = request.config.getoption("--psk-5g-wpa2")

    command_line_args.testrail_base_url = request.config.getoption("--testrail-base-url")
    command_line_args.testrail_project = request.config.getoption("--testrail-project")
    command_line_args.testrail_user_id = request.config.getoption("--testrail-user-id")
    command_line_args.testrail_user_password = request.config.getoption("--testrail-user-password")
    command_line_args.testrail_run_prefix = request.config.getoption("--testrail-run-prefix")
    command_line_args.testrail_milestone = request.config.getoption("--testrail-milestone")
    
    return command_line_args
