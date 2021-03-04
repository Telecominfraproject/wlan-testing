import argparse
from cloud_connect import CloudSDK
import importlib
import os
import sys
import json

sys.path.append('test_bed_info')

parser = argparse.ArgumentParser(description="Sanity Testing on Firmware Build")
parser.add_argument("-f", "--file", type=str, help="Test Info file name", default="test_info")
args = parser.parse_args()
test_file = args.file

test_file = os.path.splitext(test_file)[0]
if '/' in test_file:
    path, file = os.path.split(test_file)
    sys.path.append(path)
    test_info = importlib.import_module(file)
else:
    test_info = importlib.import_module(test_file)

cloudSDK_url = test_info.cloudSDK_url
cloud_type = test_info.cloud_type
deletion_file = test_info.deletion_file
cloud_user = test_info.cloud_user
cloud_password = test_info.cloud_password
equipment_id_dict = test_info.equipment_id_dict


bearer = CloudSDK.get_bearer(cloudSDK_url, cloud_type, cloud_user, cloud_password)


with open(deletion_file) as infile:
    data = json.load(infile)

delete_list = data[cloudSDK_url]

if len(delete_list) > 0:
    print("Switching AP's to default profile")
    for id in equipment_id_dict.values():
        ap_profile = CloudSDK.set_ap_profile(id, 6, cloudSDK_url, bearer)
    print('Profile change successful')

    for x in delete_list:
        delete_profile = CloudSDK.delete_profile(cloudSDK_url, bearer, str(x))
        if delete_profile == "SUCCESS":
            print("profile", x, "delete successful")
        else:
            print("Error deleting profile")

    data[cloudSDK_url] = []

    with open(deletion_file, 'w') as outfile:
        json.dump(data, outfile)