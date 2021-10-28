import sys
import os
import importlib
import csv
import sys
import time
import datetime
from datetime import date
import json
import os
import logging

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../../")))

import single_client_throughput
single_client_throughput = importlib.import_module("py-scripts.tip-cicd-sanity.single_client_throughput")
import cloudsdk
cloudsdk = importlib.import_module("py-scripts.tip-cicd-sanity.cloudsdk")
from cloudsdk import CloudSDK
CloudSDK = cloudsdk.CloudSDK
import lab_ap_info
lab_ap_info = importlib.import_module("py-scripts.tip-cicd-sanity.lab_ap_info")
import throughput_profiles
throughput_profiles = importlib.import_module("py-scripts.tip-cicd-sanity.throughput_profiles")

cloudSDK_url=os.getenv('CLOUD_SDK_URL')
station = ["tput5000"]
runtime = 10
csv_path=os.getenv('CSV_PATH')
bridge_upstream_port = "eth2"
nat_upstream_port = "eth2"
vlan_upstream_port = "vlan100"

#EAP Credentials
identity=os.getenv('EAP_IDENTITY')
ttls_password=os.getenv('EAP_PWD')

local_dir=os.getenv('TPUT_LOG_DIR')
logger = logging.getLogger('Throughput_Test')
hdlr = logging.FileHandler(local_dir+"/Throughput_Testing.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append('../../py-json')

def throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput):
    #parse client_tput list returned from single_client_throughput
    udp_ds = client_tput[0].partition(": ")[2]
    udp_us = client_tput[1].partition(": ")[2]
    tcp_ds = client_tput[2].partition(": ")[2]
    tcp_us = client_tput[3].partition(": ")[2]
    # Find band for CSV ---> This code is not great, it SHOULD get that info from LANForge!
    if "5G" in ssid_name:
        frequency = "5 GHz"
    elif "2dot4G" in ssid_name:
        frequency = "2.4 GHz"
    else:
        frequency = "Unknown"
    # Append row to top of CSV file
    row = [ap_model, firmware, frequency, mimo, security, mode, udp_ds, udp_us, tcp_ds, tcp_us]
    with open(csv_file, 'r') as readFile:
        reader = csv.reader(readFile)
        lines = list(reader)
        lines.insert(1, row)
    with open(csv_file, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    readFile.close()
    writeFile.close()

#Import dictionaries for AP Info
from lab_ap_info import equipment_id_dict
from lab_ap_info import profile_info_dict
from lab_ap_info import ap_models
from lab_ap_info import mimo_2dot4g
from lab_ap_info import mimo_5g
from lab_ap_info import customer_id
from lab_ap_info import cloud_type
#import json file to determine if throughput should be run for specific AP model
sanity_status = json.load(open("sanity_status.json"))

#create CSV file for test run
today = str(date.today())
csv_file = csv_path+"throughput_test_"+today+".csv"
headers = ['AP Type', 'Firmware','Radio', 'MIMO', 'Security', 'Mode', 'UDP Downstream (Mbps)', 'UDP Upstream (Mbps)', 'TCP Downstream (Mbps)', 'TCP Upstream (Mbps)']
with open(csv_file, "w") as file:
    create = csv.writer(file)
    create.writerow(headers)
    file.close()

ap_firmware_dict = {
    "ea8300": '',
    "ecw5211": '',
    "ecw5410": '',
    "ec420": ''
}

logger.info('Start of Throughput Test')

for key in equipment_id_dict:
    if sanity_status['sanity_status'][key] == "passed":
        logger.info("Running throughput test on " + key)
        ##Get Bearer Token to make sure its valid (long tests can require re-auth)
        bearer = CloudSDK.get_bearer(cloudSDK_url, cloud_type)
        ###Get Current AP Firmware
        equipment_id = equipment_id_dict[key]
        ap_fw = CloudSDK.ap_firmware(customer_id, equipment_id, cloudSDK_url, bearer)
        fw_model = ap_fw.partition("-")[0]
        print("AP MODEL UNDER TEST IS", fw_model)
        print('Current AP Firmware:', ap_fw)
        ##add current FW to dictionary
        ap_firmware_dict[fw_model] = ap_fw

        # Create Profiles for Testing
        profiles = throughput_profiles.main(fw_model, cloudSDK_url, cloud_type, customer_id)
        print("AP Profile List: ",profiles[1])

        ###########################################################################
        ############## Bridge Throughput Testing #################################
        ###########################################################################
        print("Testing for Bridge SSIDs")
        logger.info("Starting Bridge SSID tput tests on " + key)
        ###Set Proper AP Profile for Bridge SSID Tests
        test_profile_id = profiles[1]['bridge_profile']
        #print(test_profile_id)
        ap_profile = CloudSDK.set_ap_profile(equipment_id, test_profile_id, cloudSDK_url, bearer)
        ### Wait for Profile Push
        print('-----------------PROFILE PUSH -------------------')
        time.sleep(180)

        ##Set port for LANForge
        port = bridge_upstream_port

        # 5G WPA2 Enterprise UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        sta_list = station
        radio = lab_ap_info.lanforge_5g
        ssid_name = profile_info_dict[fw_model]["fiveG_WPA2-EAP_SSID"]
        security = "wpa2"
        eap_type = "TTLS"
        mode = "Bridge"
        mimo = mimo_5g[fw_model]
        client_tput = single_client_throughput.eap_tput(sta_list, ssid_name, radio, security, eap_type, identity, ttls_password, port)
        print(fw_model, "5 GHz WPA2-EAP throughput:\n", client_tput)
        security = "wpa2-eap"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        #5G WPA2 UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        radio = lab_ap_info.lanforge_5g
        ssid_name = profile_info_dict[fw_model]["fiveG_WPA2_SSID"]
        ssid_psk = profile_info_dict[fw_model]["fiveG_WPA2_PSK"]
        security = "wpa2"
        mode = "Bridge"
        mimo = mimo_5g[fw_model]
        client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        print(fw_model, "5 GHz WPA2 throughput:\n",client_tput)
        security = "wpa2-psk"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 5G WPA UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        radio = lab_ap_info.lanforge_5g
        ssid_name = profile_info_dict[fw_model]["fiveG_WPA_SSID"]
        ssid_psk = profile_info_dict[fw_model]["fiveG_WPA_PSK"]
        security = "wpa"
        mode = "Bridge"
        mimo = mimo_5g[fw_model]
        client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        print(fw_model, "5 GHz WPA throughput:\n",client_tput)
        security = "wpa-psk"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 5G Open UDP DS/US and TCP DS/US
        # ap_model = fw_model
        # firmware = ap_fw
        # radio = lab_ap_info.lanforge_5g
        # ssid_name = profile_info_dict[fw_model]["fiveG_OPEN_SSID"]
        # ssid_psk = "BLANK"
        # security = "open"
        #mode = "Bridge"
        #mimo = mimo_5g[fw_model]
        # client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        #print(fw_model, "5 GHz Open throughput:\n",client_tput)
        #throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 2.4G WPA2 Enterprise UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        sta_list = station
        radio = lab_ap_info.lanforge_2dot4g
        ssid_name = profile_info_dict[fw_model]["twoFourG_WPA2-EAP_SSID"]
        security = "wpa2"
        eap_type = "TTLS"
        mode = "Bridge"
        mimo = mimo_2dot4g[fw_model]
        client_tput = single_client_throughput.eap_tput(sta_list, ssid_name, radio, security, eap_type, identity,
                                                        ttls_password, port)
        print(fw_model, "2.4 GHz WPA2-EAP throughput:\n", client_tput)
        security = "wpa2-eap"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 2.4G WPA2 UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        radio = lab_ap_info.lanforge_2dot4g
        ssid_name = profile_info_dict[fw_model]["twoFourG_WPA2_SSID"]
        ssid_psk = profile_info_dict[fw_model]["twoFourG_WPA2_PSK"]
        security = "wpa2"
        mode = "Bridge"
        mimo = mimo_2dot4g[fw_model]
        client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        print(fw_model, "2.4 GHz WPA2 throughput:\n",client_tput)
        security = "wpa2-psk"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 2.4G WPA UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        radio = lab_ap_info.lanforge_2dot4g
        ssid_name = profile_info_dict[fw_model]["twoFourG_WPA_SSID"]
        ssid_psk = profile_info_dict[fw_model]["twoFourG_WPA_PSK"]
        security = "wpa"
        mode = "Bridge"
        mimo = mimo_2dot4g[fw_model]
        client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        print(fw_model, "2.4 GHz WPA throughput:\n",client_tput)
        security = "wpa-psk"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 2.4G Open UDP DS/US and TCP DS/US
        #ap_model = fw_model
        #firmware = ap_fw
        # radio = lab_ap_info.lanforge_5g
        # ssid_name = profile_info_dict[fw_model]["twoFourG_OPEN_SSID"]
        # ssid_psk = "BLANK"
        # security = "open"
        #mode = "Bridge"
        #mimo = mimo_2dot4g[fw_model]
        #client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        #print(fw_model, "2.4 GHz Open throughput:\n",client_tput)
        #throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        ###########################################################################
        ################# NAT Mode Throughput Testing ############################
        ###########################################################################
        print('Testing for NAT SSIDs')
        logger.info("Starting NAT SSID tput tests on " + key)
        ###Set Proper AP Profile for NAT SSID Tests
        test_profile_id = profiles[1]['nat_profile']
        print(test_profile_id)
        bearer = CloudSDK.get_bearer(cloudSDK_url, cloud_type)
        ap_profile = CloudSDK.set_ap_profile(equipment_id, test_profile_id, cloudSDK_url, bearer)

        ### Wait for Profile Push
        print('-----------------PROFILE PUSH -------------------')
        time.sleep(180)

        ##Set port for LANForge
        port = nat_upstream_port

        # 5G WPA2 Enterprise UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        sta_list = station
        radio = lab_ap_info.lanforge_5g
        ssid_name = profile_info_dict[fw_model+'_nat']["fiveG_WPA2-EAP_SSID"]
        security = "wpa2"
        eap_type = "TTLS"
        mode = "NAT"
        mimo = mimo_5g[fw_model]
        client_tput = single_client_throughput.eap_tput(sta_list, ssid_name, radio, security, eap_type, identity,
                                                        ttls_password, port)
        print(fw_model, "5 GHz WPA2-EAP NAT throughput:\n", client_tput)
        security = "wpa2-eap"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 5G WPA2 NAT UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        radio = lab_ap_info.lanforge_5g
        ssid_name = profile_info_dict[fw_model+'_nat']["fiveG_WPA2_SSID"]
        ssid_psk = profile_info_dict[fw_model+'_nat']["fiveG_WPA2_PSK"]
        security = "wpa2"
        mode = "NAT"
        mimo = mimo_5g[fw_model]
        client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        print(fw_model, "5 GHz WPA2 NAT throughput:\n", client_tput)
        security = "wpa2-psk"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 5G WPA UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        radio = lab_ap_info.lanforge_5g
        ssid_name = profile_info_dict[fw_model+'_nat']["fiveG_WPA_SSID"]
        ssid_psk = profile_info_dict[fw_model+'_nat']["fiveG_WPA_PSK"]
        security = "wpa"
        mode = "NAT"
        mimo = mimo_5g[fw_model]
        client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        print(fw_model, "5 GHz WPA NAT throughput:\n", client_tput)
        security = "wpa-psk"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 5G Open UDP DS/US and TCP DS/US
        # ap_model = fw_model
        # firmware = ap_fw
        # radio = lab_ap_info.lanforge_5g
        # ssid_name = profile_info_dict[fw_model+'_nat']["fiveG_OPEN_SSID"]
        # ssid_psk = "BLANK"
        # security = "open"
        # mode = "NAT"
        #mimo = mimo_5g[fw_model]
        # client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        # print(fw_model, "5 GHz Open NAT throughput:\n",client_tput)
        # throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 2.4G WPA2 Enterprise UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        sta_list = station
        radio = lab_ap_info.lanforge_2dot4g
        ssid_name = profile_info_dict[fw_model+'_nat']["twoFourG_WPA2-EAP_SSID"]
        security = "wpa2"
        eap_type = "TTLS"
        mode = "NAT"
        mimo = mimo_2dot4g[fw_model]
        client_tput = single_client_throughput.eap_tput(sta_list, ssid_name, radio, security, eap_type, identity, ttls_password, port)
        print(fw_model, "2.4 GHz WPA2-EAP NAT throughput:\n", client_tput)
        security = "wpa2-eap"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 2.4G WPA2 UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        radio = lab_ap_info.lanforge_2dot4g
        ssid_name = profile_info_dict[fw_model+'_nat']["twoFourG_WPA2_SSID"]
        ssid_psk = profile_info_dict[fw_model+'_nat']["twoFourG_WPA2_PSK"]
        security = "wpa2"
        mode = "NAT"
        mimo = mimo_2dot4g[fw_model]
        client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        print(fw_model, "2.4 GHz WPA2 NAT throughput:\n", client_tput)
        security = "wpa2-psk"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 2.4G WPA UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        radio = lab_ap_info.lanforge_2dot4g
        ssid_name = profile_info_dict[fw_model+'_nat']["twoFourG_WPA_SSID"]
        ssid_psk = profile_info_dict[fw_model+'_nat']["twoFourG_WPA_PSK"]
        security = "wpa"
        mode = "NAT"
        mimo = mimo_2dot4g[fw_model]
        client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        print(fw_model, "2.4 GHz WPA NAT throughput:\n", client_tput)
        security = "wpa-psk"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 2.4G Open NAT UDP DS/US and TCP DS/US
        # ap_model = fw_model
        # firmware = ap_fw
        # radio = lab_ap_info.lanforge_5g
        # ssid_name = profile_info_dict[fw_model+'_nat']["twoFourG_OPEN_SSID"]
        # ssid_psk = "BLANK"
        # security = "open"
        # mode = "NAT"
        #mimo = mimo_2dot4g[fw_model]
        # client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        # print(fw_model, "2.4 GHz Open NAT throughput:\n",client_tput)
        # throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        ###########################################################################
        ################# Custom VLAN Mode Throughput Testing #####################
        ###########################################################################
        print('Testing for Custom VLAN SSIDs')
        logger.info("Starting Custom VLAN SSID tput tests on " + key)
        ###Set Proper AP Profile for VLAN SSID Tests
        test_profile_id = profiles[1]['vlan_profile']
        print(test_profile_id)
        bearer = CloudSDK.get_bearer(cloudSDK_url, cloud_type)
        ap_profile = CloudSDK.set_ap_profile(equipment_id, test_profile_id, cloudSDK_url, bearer)

        ### Wait for Profile Push
        print('-----------------PROFILE PUSH -------------------')
        time.sleep(180)

        ##Set port for LANForge
        port = vlan_upstream_port
        # 5G WPA2 Enterprise UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        sta_list = station
        radio = lab_ap_info.lanforge_5g
        ssid_name = profile_info_dict[fw_model + '_vlan']["fiveG_WPA2-EAP_SSID"]
        security = "wpa2"
        eap_type = "TTLS"
        mode = "VLAN"
        mimo = mimo_5g[fw_model]
        client_tput = single_client_throughput.eap_tput(sta_list, ssid_name, radio, security, eap_type, identity, ttls_password, port)
        print(fw_model, "5 GHz WPA2-EAP VLAN throughput:\n", client_tput)
        security = "wpa2-eap"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 5G WPA2 VLAN UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        radio = lab_ap_info.lanforge_5g
        ssid_name = profile_info_dict[fw_model + '_vlan']["fiveG_WPA2_SSID"]
        ssid_psk = profile_info_dict[fw_model + '_vlan']["fiveG_WPA2_PSK"]
        security = "wpa2"
        mode = "VLAN"
        mimo = mimo_5g[fw_model]
        client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        print(fw_model, "5 GHz WPA2 VLAN throughput:\n", client_tput)
        security = "wpa2-psk"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 5G WPA UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        radio = lab_ap_info.lanforge_5g
        ssid_name = profile_info_dict[fw_model + '_vlan']["fiveG_WPA_SSID"]
        ssid_psk = profile_info_dict[fw_model + '_vlan']["fiveG_WPA_PSK"]
        security = "wpa"
        mode = "VLAN"
        mimo = mimo_5g[fw_model]
        client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        print(fw_model, "5 GHz WPA VLAN throughput:\n", client_tput)
        security = "wpa-psk"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 5G Open UDP DS/US and TCP DS/US
        # ap_model = fw_model
        # firmware = ap_fw
        # radio = lab_ap_info.lanforge_5g
        # ssid_name = profile_info_dict[fw_model+'_vlan']["fiveG_OPEN_SSID"]
        # ssid_psk = "BLANK"
        # security = "open"
        # mode = "VLAN"
        # mimo = mimo_5g[fw_model]
        # client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        # print(fw_model, "5 GHz Open VLAN throughput:\n",client_tput)
        # throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 2.4G WPA2 Enterprise UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        sta_list = station
        radio = lab_ap_info.lanforge_2dot4g
        ssid_name = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2-EAP_SSID"]
        security = "wpa2"
        eap_type = "TTLS"
        mode = "VLAN"
        mimo = mimo_2dot4g[fw_model]
        client_tput = single_client_throughput.eap_tput(sta_list, ssid_name, radio, security, eap_type, identity, ttls_password, port)
        print(fw_model, "2.4 GHz WPA2-EAP VLAN throughput:\n", client_tput)
        security = "wpa2-eap"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 2.4G WPA2 UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        radio = lab_ap_info.lanforge_2dot4g
        ssid_name = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2_SSID"]
        ssid_psk = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2_PSK"]
        security = "wpa2"
        mode = "VLAN"
        mimo = mimo_2dot4g[fw_model]
        client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        print(fw_model, "2.4 GHz WPA2 VLAN throughput:\n", client_tput)
        security = "wpa2-psk"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 2.4G WPA UDP DS/US and TCP DS/US
        ap_model = fw_model
        firmware = ap_fw
        radio = lab_ap_info.lanforge_2dot4g
        ssid_name = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA_SSID"]
        ssid_psk = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA_PSK"]
        security = "wpa"
        mode = "VLAN"
        mimo = mimo_2dot4g[fw_model]
        client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        print(fw_model, "2.4 GHz WPA VLAN throughput:\n", client_tput)
        security = "wpa-psk"
        throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)

        # 2.4G Open VLAN UDP DS/US and TCP DS/US
        # ap_model = fw_model
        # firmware = ap_fw
        # radio = lab_ap_info.lanforge_5g
        # ssid_name = profile_info_dict[fw_model+'_vlan']["twoFourG_OPEN_SSID"]
        # ssid_psk = "BLANK"
        # security = "open"
        # mode = "VLAN"
        # mimo = mimo_2dot4g[fw_model]
        # client_tput = single_client_throughput.main(ap_model, firmware, radio, ssid_name, ssid_psk, security, station, runtime, port)
        # print(fw_model, "2.4 GHz Open VLAN throughput:\n",client_tput)
        # throughput_csv(csv_file, ssid_name, ap_model, mimo, firmware, security, mode, client_tput)


        #Indicates throughput has been run for AP model
        sanity_status['sanity_status'][key] = "tput run"
        with open('sanity_status.json', 'w') as json_file:
            json.dump(sanity_status, json_file)

        logger.info("Throughput tests complete on " + key)
        # Move AP off profile in use
        ap_profile = CloudSDK.set_ap_profile(equipment_id, profile_info_dict[fw_model]["profile_id"], cloudSDK_url,
                                             bearer)
        time.sleep(5)

        # Delete profiles created for test
        for x in profiles[0]:
            delete_profile = CloudSDK.delete_profile(cloudSDK_url, bearer, str(x))
            if delete_profile == "SUCCESS":
                print("profile", x, "delete successful")
            else:
                print("Error deleting profile")

    elif sanity_status['sanity_status'][key] == "tput run":
        print("Throughput test already run on", key)
        logger.info("Throughput test already run on "+ key +" for latest AP FW")

    else:
        print(key,"did not pass Nightly Sanity. Skipping throughput test on this AP Model")
        logger.info(key+" did not pass Nightly Sanity. Skipping throughput test.")

#Indicate which AP model has had tput test to external json file
with open('sanity_status.json', 'w') as json_file:
  json.dump(sanity_status, json_file)

with open(csv_file, 'r') as readFile:
    reader = csv.reader(readFile)
    lines = list(reader)
    row_count = len(lines)
    #print(row_count)

if row_count <= 1:
    os.remove(csv_file)
    file.close()

else:
    print("Saving File")
    file.close()

print(" -- Throughput Testing Complete -- ")
