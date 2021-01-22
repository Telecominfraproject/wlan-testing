# TIP CICD Sanity Scripts
This directory contains scripts and modules designed for wlan sanity testing. 

# Libraries needed to run this code successfully
sudo pip3 install artifactory
sudo pip3 install xlsxwriter
sudo pip3 install pandas
sudo pip3 install paramiko
sudo pip3 install scp
sudo pip3 install pexpect

# Find the cloud-sdk API document here:
https://github.com/Telecominfraproject/wlan-cloud-services/tree/master/portal-services/src/main/resources/

# Examples in this code often assume you are using ssh port redirects to log into the testbeds,
# for instance:
ssh -C -L 8800:lf1:4002 -L 8801:lf1:5901 -L 8802:lf1:8080 ubuntu@orch

Then, you would use port 8802 for connecting to the LANforge-GUI for the python LANforge test logic,
and port 8803 to access the lab jumphost.

./Nightly_Sanity.py --testrail-user-id NONE --model ecw5410 --ap-jumphost-address localhost --ap-jumphost-port 8803 \
  --ap-jumphost-password pumpkin77 --ap-jumphost-tty /dev/ttyAP1 --skip-upgrade True --testbed "NOLA-01h" \
  --lanforge-ip-address localhost --lanforge-port-number 8802 --default_ap_profile TipWlan-2-Radios --skip_radius --skip_profiles


## Nightly Sanity
This script is used to look for and test new firmware available for the APs. AP equipment IDs and SSID information used in test is stored in the lab_ap_info file

1. Check current CloudSDK version
2. Find latest dev firmware on TIP jfrog and create instances on CloudSDK (if necessary)
3. Create report_data.json file with information about versions and test case pass/fail
4. For each AP model:
    1. Check current AP firmware *(If AP already running newest firmware, test will skip)*
    2. Create Testrail test run with required test cases included 
    3. Upgrade AP via CloudSDK API
    4. Check if AP upgrade and CloudSDK connection successful
    5. For each SSID mode (bridge, NAT and VLAN), marking TestRail and report_data.json with pass/fail:
        1. Create SSID Profiles for various security modes and radio types
        2. Create AP Profile for SSID mode
        3. Apply AP profile to AP
        5. Check that SSID have been applied properly on AP
        4. Perform client connectivity tests
    6. Update sanity_status.json with **overall** pass/fail
 
## Throughput Test
This script is used to test UDP and TCP throughput on different modes of SSIDs, on multiple AP models. It is designed to run on APs that have successfully passed through Nightly_Sanity test.

For each AP model:
1) Read sanity_status.json to see if throughput should be run, if yes:
    1) Run throughput tests on SSIDs modes
    2) Record results to CSV file
2) Update sanity_status.json that throughput tests have been run

## Environment Variables
Environment variables required to run scripts and modules in this directory
#### Nightly_Sanity.py		
CLOUD_SDK_URL: CloudSDK URL for API calls  
SANITY_LOG_DIR: Logger file directory  
SANITY_REPORT_DIR: Report file directory 
REPORT_TEMPLATE: Report template path  
TR_USER: TestRail Username  
TR_PWD: TestRail Password  
MILESTONE: TestRail Milestone ID  
PROJECT_ID: TestRail Project ID  
EAP_IDENTITY: EAP identity for testing  
EAP_PWD: EAP password for testing  
AP_USER: Username for AP  
JFROG_USER: Jfrog username  
JFROG_PWD: Jfrog password  
		
#### cloudsdk.py		
CLOUDSDK_USER: CloudSDK username  
CLOUDSDK_PWD: CloudSDK password  
		
#### cluster_version.py		
AWS_USER: CloudSDK username  
AWS_PWD: CloudSDK password  
		
#### testrail_api.py		
TR_USER	tr_user	TestRail Username  
TR_PWD	tr_pw	TestRail Password  
		
#### Throughput_Test.py		
CLOUD_SDK_URL: CloudSDK URL for API calls  
CSV_PATH: Path for CSV file  
EAP_IDENTITY: EAP identity for testing  
EAP_PWD: EAP password for testing  
TPUT_LOG_DIR: Logger file directory  
