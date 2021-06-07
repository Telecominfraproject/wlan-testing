# wlan-testing framework Information

## pytest  uses setup > test > tear_down
#### Fixtures : Code that needs to be part of more than 1 test cases, Setup and teardown is Implemented in Fixtures

Requried Module Installation:
pip3 install selenium
pip3 install perfecto-py37
pip3 install Appium-Python-Client   

Avaiable WPA2 & WPA Protocal for 5G or 2G Options
1) wpa2_personal :>
    a) setup_profile_data["NAT"]["WPA2_P"]["5G"]  
    b) setup_profile_data["NAT"]["WPA2_P"]["2G"] 
2) wpa :>
    a) setup_profile_data["NAT"]["WPA"]["5G"]  
    b) setup_profile_data["NAT"]["WPA"]["2G"]  

Sample Execution of Test Cases for a maximum of 4 devices in parallel only. 

Required Parameters:
1) securityToken=<Please-Enter-your-securityToken>
2) jobName=<Your-CI-JOB-NAME>
3) jobNumber=<Your-CI-JOB-NUMBER>
4) model-iOS=iPhone.*  < Picks any random iphone or use any device below.
    a) iPhone-11.*   (Picks any random iphone 11)
    b) iPhone-12.*   (Picks any random iphone 12)
    c) iPhone-7.*   (Picks any random iphone 7)
    d) iPhone-XR.*   (Picks any random iphone XR)
    Note:Only 1 device of each are avaible on the cloud.  You can only assign 1 test case to to a phone @ a time. 

Sample Execution of Tests from CI:

Execute AccessPassPointConnectivety Test Case with wpa2_personal & fiveg
#pytest -m "AccessPassPointConnectivety and wpa2_personal and fiveg" -s -vvv --testbed=interop -o 'model-iOS=iPhone.*' -o 'jobName=TestRajMay' -o 'jobNumber=2' -o 'securityToken=<YOUR-SECURITY-TOKEN>'

pytest -m "ToggleAirplaneMode and wpa2_personal and fiveg" -s -vvv --testbed=interop -o 'model-iOS=iPhone.*' -o 'jobName=TestRajMay' -o 'jobNumber=2' -o 'securityToken=<YOUR-SECURITY-TOKEN>'

pytest -m "ClientConnectivity and wpa2_personal and fiveg" -s -vvv --testbed=interop -o 'model-iOS=iPhone.*' -o 'jobName=TestRajMay' -o 'jobNumber=2' -o 'securityToken=<YOUR-SECURITY-TOKEN>'

pytest -m "PassPointConnection and wpa2_personal and fiveg" -s -vvv --testbed=interop -o 'model-iOS=iPhone.*' -o 'jobName=TestRajMay' -o 'jobNumber=2' -o 'securityToken=<YOUR-SECURITY-TOKEN>'

pytest -m "ToggleWifiMode and wpa2_personal and fiveg" -s -vvv --testbed=interop -o 'model-iOS=iPhone.*' -o 'jobName=TestRajMay' -o 'jobNumber=2' -o 'securityToken=<YOUR-SECURITY-TOKEN>'

#### For any Clarifications, regarding Framework, 
#### Email : shivam.thakur@candelatech.com <Shivam>
#### Email : rpasupathy@perforce.com <Raj>



