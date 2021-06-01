## Docker based environment

### Building a docker image

From the root directory of this repository (wlan-testing) run the following command:
```bash
docker build -f ./docker/Dockerfile -t wlantest .
```
This will produce a docker image, which you can verify by running docker images command.

### Running a docker image

From the root directory of this repository (wlan-testing) run the following command. This command executes  
connectivity tests on a specific lab. **NOTE:** Use appropriate marker for your pytest execution, 
configuration.py and replace ${YOUR_ALLURE_RESULTS_DIR} with your allure result dir.

```bash
docker run -i -t -v $(YOUR_ALLURE_RESULT_DIR):/allure-results -v $(pwd)/configuration.py:/wlan-testing/configuration.py wlantest /bin/bash -c "cd tests; pytest -s -vvv --testbed=basic-02 -m client_connectivity_test --skip-testrail --alluredir=/allure-result"
```