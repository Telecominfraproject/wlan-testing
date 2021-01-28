# TIP CICD Sanity Scripts
This directory contains scripts and modules designed for automated full-system testing. 

# Libraries needed to run this code successfully
sudo pip3 install artifactory
sudo pip3 install xlsxwriter
sudo pip3 install pandas
sudo pip3 install paramiko
sudo pip3 install scp
sudo pip3 install pexpect

# Clone these repositories to get started:
git@github.com:Telecominfraproject/wlan-testing.git   # This repo

# LANforge scripts repo.  This *MUST* be located or linked at wlan-testing/lanforge/lanforge-scripts
git@github.com:Telecominfraproject/wlan-lanforge-scripts.git

# Cloud-services, so that you can find the API document
git@github.com:Telecominfraproject/wlan-cloud-services

# Find the cloud-sdk API document here:
https://github.com/Telecominfraproject/wlan-cloud-services/tree/master/portal-services/src/main/resources/

# You need access to the 'ubuntu' jumphost.  Send your public ssh key to greearb@candelatech.com
# and he will add this to the jumphost.
# For ease of use, add this to your /etc/hosts file:  3.130.51.163 orch

# Examples in this code often assume you are using ssh port redirects to log into the testbeds,
# for instance, this is for working on the NOLA-01 testbed.  The 3.130.51.163 (aka orch)
# system has its /etc/hosts file updated, so that 'lf1' means LANforg system in testbed NOLA-01
# You can find other testbed info in TIP Confluence
#  https://telecominfraproject.atlassian.net/wiki/spaces/WIFI/pages/307888428/TIP+Testbeds
#  Please communicate with Ben Greear or Jaspreet Sachdev before accessing a testbed
#  at leat until we have a reservation system in place.

# NOLA-01 testbed
ssh -C -L 8800:lf1:4002 -L 8801:lf1:5901 -L 8802:lf1:8080 -L 8803:lab-ctlr:22 ubuntu@orch
#  Example of accessing AP over serial console through jumphost
./query_ap.py --ap-jumphost-address localhost --ap-jumphost-port 8803 --ap-jumphost-password pumpkin77 --ap-jumphost-tty /dev/ttyAP1 -m ecw5410 --cmd "cat /etc/banner"
# Example of accessing NOLA-01's cloud controller (https://wlan-portal-svc.cicd.lab.wlan.tip.build)
./query_sdk.py --testrail-user-id NONE --model ecw5410 --sdk-base-url https://wlan-portal-svc.cicd.lab.wlan.tip.build --sdk-user-id \
   support@example.com --sdk-user-password support --equipment_id 3 --type profile --cmd get --brief true

# NOLA-04 testbed
#  testbed ssh tunnel
ssh -C -L 8810:lf4:4002 -L 8811:lf4:5901 -L 8812:lf4:8080 -L 8813:lab-ctlr:22 ubuntu@orch
#  Example of accessing AP over serial console through jumphost
./query_ap.py --ap-jumphost-address localhost --ap-jumphost-port 8813 --ap-jumphost-password pumpkin77 --ap-jumphost-tty /dev/ttyAP4 -m ecw5410 --cmd "cat /etc/banner"


# NOLA-12 testbed
#  testbed ssh tunnel
ssh -C -L 8820:lf12:4002 -L 8821:lf12:5901 -L 8822:lf12:8080 -L 8823:lab-ctlr4:22 ubuntu@orch
# Create profiles.
./sdk_set_profile.py --testrail-user-id NONE --model ecw5410 --ap-jumphost-address localhost --ap-jumphost-port 8823 --ap-jumphost-password pumpkin77 --ap-jumphost-tty /dev/ttyAP1 --testbed "NOLA-12" --lanforge-ip-address localhost --lanforge-port-number 8822 --default_ap_profile TipWlan-2-Radios --sdk-base-url https://wlan-portal-svc-ben-testbed.cicd.lab.wlan.tip.build --skip_radius


Then, you would use port 8802 for connecting to the LANforge-GUI for the python LANforge test logic,
and port 8803 to access the lab jumphost.  Port 8800 could connect a locally running LANforge GUI to the
testbed for monitoring the test, and port 8801 will connect VNC to the LANforge machine.

# This automated test logic is found in the wlan-testing/unit_tests directory.  These notes
# assume you are in that directory unless otherwise specified.

# Interesting files in this repo

* ap_ssh.py:  Library methods to access the AP over direct ssh connection or serial console.  For NOLA
  testbeds, currently serial console is the only viable way to connect.

* cloudsdk.py: Library methods to access the cloud controller API using REST/JSON.  This is how you configure
  the AP.

* lab_ap_info.py:  Holds some variables related to lab config.  I prefer to use this as little as possible.
  Instead, use command line arguments, possibly specifying a particular config file on the cmd line if
  needed.

* UnitTestBase.py:  Base class for all test cases.  Handles bulk of command-line-argument processing and importing
  of various modules needed for testing.  Test cases should normally inherit from this.

* Nightly_Sanity.py:  All-in-one script that updates firmware, creates cloud controller profiles, and runs LANforge
  tests.  This is only partially functional for now.  Much of the logic in it needs to be moved to library files
  so that other test cases can take advantage of the logic.

* query_ap.py:  Calls into ap_ssh.py to do some actions on APs, including running arbitrary commands.  This would
  be a good example to use as starting point for writing new test cases that need to access the AP.
  Try: ./query_ap.py --help  for example of how to use.

* query_sdk.py:  Calls into cloudsdk.py to do some actions on cloud controller.  This would
  be a good example to use as starting point for writing new test cases that need to access the cloud controller.
  Try: ./query_sdk.py --help  for example of how to use.



# This is how the nightly sanity script is launched for the NOLA-01 testbed.

./Nightly_Sanity.py --testrail-user-id NONE --model ecw5410 --ap-jumphost-address localhost --ap-jumphost-port 8803 \
  --ap-jumphost-password pumpkin77 --ap-jumphost-tty /dev/ttyAP1 --skip-upgrade True --testbed "NOLA-01h" \
  --lanforge-ip-address localhost --lanforge-port-number 8802 --default_ap_profile TipWlan-2-Radios --skip_radius --skip_profiles \
  --lanforge-2g-radio 1.1.wiphy4 --lanforge-5g-radio 1.1.wiphy5



## Nightly Sanity details:
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

