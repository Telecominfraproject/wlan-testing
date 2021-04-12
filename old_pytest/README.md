# Pytest Framework
## Perform Unit Tests in TIP Community Testbeds

### Fixtures : 
#### conftest.py
### Unit Tests : 
#### Structured around multiple Directories
### Markers : 
#### Categorized the Test across different Markers


### Note: Run all the tests from "tests" directory

Modify pytest.ini based on the config for your setup
You can modify the ini options by using switch -o 

## Examples:
Following are the examples for Running Client Connectivity Test with different Combinations:

    # Run the sanity test in all modes across wpa, wpa2 and eap)
    pytest -m run -s

    # Run the sanity test in all modes except wpa2_enterprise)
    pytest -m "run and not wpa2_enterprise" -s

    # Run the bridge test in all modes across wpa, wpa2 and eap)
    pytest -m "run and bridge" -s

    # Run the bridge test in all modes except wpa2_enterprise)
    pytest -m "run and bridge and not wpa2_enterprise" -s

    # Run the nat test in all modes across wpa, wpa2 and eap)
    pytest -m "run and nat" -s

    # Run the nat test in all modes except wpa2_enterprise)
    pytest -m "run and nat and not wpa2_enterprise" -s

    # Run the vlan test in all modes across wpa, wpa2 and eap)
    pytest -m "run and vlan" -s

    # Run the vlan test in all modes except wpa2_enterprise)
    pytest -m "run and vlan and not wpa2_enterprise" -s


Following are the examples for cloudSDK standalone tests
    
    # Run cloud test to check sdk version
    pytest -m sdk_version_check -s
    
    # Run cloud test to create firmware on cloudsdk instance (currently using pending)
    pytest -m firmware_create -s 
    
    # Run cloud test to upgrade the latest firmware on AP (currently using pending)
    pytest -m firmware_upgrade -s
    
    All test cases can be executed individually as well as part of sanity work flow also

Following are the examples for apnos standalone tests
    
    # Run ap test to see the manager state on AP using SSH
    pytest -m ap_manager_state -s

    # Run ap test to see if the AP is in latest firmware
    pytest -m check_active_firmware_ap -s

Following are the examples for apnos+cloudsdk mixed tests
    
    # Run apnos and cloudsdk test to verify if profiles that are pushed from cloud are same on vif_config
    pytest -m vif_config_test -s

    # Run apnos and cloudsdk test to verify if profiles that are pushed from cloud are same on vif_config
    pytest -m vif_state_test -s


##General Notes:

Please enter your testrail userid and password inside pytest.ini to run the sanity with testrails 
    
    # Modify the below fields in tests/pytest.ini
    tr_user=shivam.thakur@candelatech.com
    tr_pass=Something

you can always skip the use of testrails by adding an option "--skip-testrail"
    
    # Run test cases without testrails
    pytest -m ap_manager_state -s --skip-testrail


you can always control the number of clients for test cases by just adding a command line option
    
    # Run test cases with multiclient
    pytest -m "run and bridge" -s --skip-testrail -o num_stations=5


Modify the tests/configuration_data.py, according to the requirement
#### AP SSH info is wrapped up in APNOS Library in libs/apnos/apnos.py
the configuration_data.py has the data structure in the below format,

    APNOS_CREDENTIAL_DATA = {
        'ip': "192.168.200.80",
        'username': "lanforge",
        'password': "lanforge",
        'port': 22,
        'mode': 1
    }
    # There are two modes, (mode:0, AP direct ssh mode, mode:1, Jumphost mode)