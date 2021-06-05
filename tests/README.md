## Test Case Execution Suite

```commandline
pytest -m sanity -s -vvv --testbed=basic-01 -o build=<firmware URL>
pytest -m sanity_55 -s -vvv --testbed=basic-01 -o build=<firmware URL>
pytest -m performance -s -vvv --testbed=basic-01 -o build=<firmware URL>
pytest -m firmware -s -vvv --testbed=basic-01 -o build=<firmware URL>
```
## You can customize the markets with and/or/not logical options





## wlan-testing framework Information

**_pytest  uses setup > test > tear_down_** <br>
**_Fixtures : Code that needs to be part of more than 1 test cases, Setup and teardown is Implemented in Fixtures_**


### Test cases are structured across different directories
```
├── wlan-testing                 
    ├── tests       /* Root directory for tests  */                
```


We have 3 main resource types:
1. Controller
2. Access Points
3. Traffic Generator



Controller is meant to Provision the Access-Point


```
├── tests                       /* Pytest cases Directory */
    ├── controller_tests    /* controller has the REST API*/
        ├── conftest.py     /* Fixtures to be used by controller tests */        
        ├── test_api_login.py
        ├── test_api_customer.py
        ├── test_api_location.py
        ├── test_api_equipment.py
        ├── test_api_equipment_gateway.py
        ├── test_api_profile.py
        ├── test_api_firmware_management.py 
               
```

Access-Point is meant to be connected to controller, as well as should be able to provide wired and wireless connectivity to Both real and virtual Clients
```
├── tests                       /* Pytest cases Directory */
    ├── access_point_tests            
        ├── conftest.py     /* Fixtures to be used by access point tests */
        ├── test_connectivity.py
        ├── test_radio.py
        ├── test_featureA.py    To be added 
        ├── test_featureB.py
```
e2e (End to End) test cases are further structured into test case physical environment

Each Environment differs in testbed setup

```
            Controller      AP      Traffic Generator   PDU     Attenuator
basic  :        1           1           1 LANforge       1       0 Atten
advanced :      1           1           1 LANforge       1       1 Atten
interOp :       1           -           8 Perfecto       0       1 Atten
MDU  :          1           -           - LANforge       0
Scale  :        1           -           - LANforge       0
```




```
├── tests              /* Pytest cases Directory */
    ├── conftest.py    /* Global Fixtures for tests */        
```



```
├── tests            - /* Pytest cases Directory */
      ├── e2e
          ├── advanced
            ├── conftest.py     /* Fixtures specific to advanced LAB Environment */
          ├── basic
            ├── conftest.py     /* Fixtures specific to basic LAB Environment */     
          ├── interOp
            ├── conftest.py     /* Fixtures specific to interOp LAB Environment */
          ├── mdu
            ├── conftest.py     /* Fixtures specific to mdu LAB Environment */
          |── mesh
            ├── conftest.py     /* Fixtures specific to mesh LAB Environment */
          |── scale
            ├── conftest.py     /* Fixtures specific to scale LAB Environment */

Read the README.md in each e2e directory to get sample test case.
```


**_For any Clarifications, regarding Framework,_** <br> 
**_Email : shivam.thakur@candelatech.com_**



