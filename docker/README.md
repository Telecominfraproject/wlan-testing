## Docker based environment

### Building a docker image

From the root directory of this repository (wlan-testing) run the following command:

```bash
docker build -f ./docker/Dockerfile -t wlantest .
```

This will produce a docker image, which you can verify by running docker images command.

By default image will run [setup_env.bash](../setup_env.bash) that will install all required dependencies for tests against all supported devices and version 2 of Cloud SDK (see https://github.com/Telecominfraproject/wlan-cloud-ucentral-deploy/ for details).

If you want to modify this logic, you may pass different build arguments to the build. Supported arguments:

- CLOUDSDK_LIBRARY - Cloud SDK library that should be used for tests (by default `tip_2x` will be used);
- TEST_DEVICE_NAME - device type that should be installed as a depencency (by default `all` will be used).

Check [setup_env.bash](../setup_env.bash) for more details on supported parameters.

Example on how to pass build arguments:

```bash
docker build -f ./docker/Dockerfile -t wlantest --build-arg TEST_DEVICE_NAME=lanforge .
```

### Running a docker image

From the root directory of this repository (wlan-testing) run the following command. This command executes  
connectivity tests on a specific lab. **NOTE:** Use appropriate marker for your pytest execution, 
configuration.py and replace ${YOUR_ALLURE_RESULTS_DIR} with your allure result dir.

```bash
docker run -i -t -v $(YOUR_ALLURE_RESULT_DIR):/allure-results -v $(pwd)/configuration.py:/wlan-testing/configuration.py wlantest /bin/bash -c "cd tests; pytest -s -vvv --testbed=basic-02 -m client_connectivity_test --skip-testrail --alluredir=/allure-result"
```
