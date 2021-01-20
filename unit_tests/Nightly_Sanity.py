#!/usr/bin/python3

from UnitTestBase import *

parser = argparse.ArgumentParser(description="Nightly Combined Tests", add_help=False)
parser.add_argument("--default_ap_profile", type=str,
                    help="Default AP profile to use as basis for creating new ones, typically: TipWlan-2-Radios or TipWlan-3-Radios",
                    required=True)

base = UnitTestBase("query-sdk", parser)

command_line_args = base.command_line_args

# cmd line takes precedence over env-vars.
cloudSDK_url = command_line_args.sdk_base_url       # was os.getenv('CLOUD_SDK_URL')
local_dir = command_line_args.local_dir             # was os.getenv('SANITY_LOG_DIR')
report_path = command_line_args.report_path         # was os.getenv('SANITY_REPORT_DIR')
report_template = command_line_args.report_template  # was os.getenv('REPORT_TEMPLATE')

## TestRail Information
tr_user = command_line_args.testrail_user_id        # was os.getenv('TR_USER')
tr_pw = command_line_args.testrail_user_password    # was os.getenv('TR_PWD')
milestoneId = command_line_args.milestone           # was os.getenv('MILESTONE')
projectId = command_line_args.testrail_project      # was os.getenv('PROJECT_ID')
testRunPrefix = command_line_args.testrail_run_prefix # os.getenv('TEST_RUN_PREFIX')

##Jfrog credentials
jfrog_user = command_line_args.jfrog_user_id        # was os.getenv('JFROG_USER')
jfrog_pwd = command_line_args.jfrog_user_password   # was os.getenv('JFROG_PWD')

##EAP Credentials
identity = command_line_args.eap_id                 # was os.getenv('EAP_IDENTITY')
ttls_password = command_line_args.ttls_password     # was os.getenv('EAP_PWD')

## AP Credentials
ap_username = command_line_args.ap_username         # was os.getenv('AP_USER')

##LANForge Information
lanforge_ip = command_line_args.lanforge_ip_address
lanforge_prefix = command_line_args.lanforge_prefix

build = command_line_args.build_id

logger = base.logger
hdlr = base.hdlr

if command_line_args.testbed == None:
    print("ERROR:  Must specify --testbed argument for this test.")
    sys.exit(1)

client: TestRail_Client = TestRail_Client(command_line_args)

###Class for jfrog Interaction
class GetBuild:
    def __init__(self):
        self.user = jfrog_user
        self.password = jfrog_pwd
        ssl._create_default_https_context = ssl._create_unverified_context

    def get_latest_image(self, url, build):
        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()
        headers = {'Authorization': 'Basic ' + auth}

        ''' FIND THE LATEST FILE NAME'''
        # print(url)
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html, features="html.parser")
        ##find the last pending link on dev
        last_link = soup.find_all('a', href=re.compile(build))[-1]
        latest_file = last_link['href']
        latest_fw = latest_file.replace('.tar.gz', '')
        return latest_fw


###Class for Tests
class RunTest:
    def Single_Client_Connectivity(self, port, radio, ssid_name, ssid_psk, security, station, test_case, rid):
        '''SINGLE CLIENT CONNECTIVITY using test_connect2.py'''
        staConnect = StaConnect2(lanforge_ip, 8080, debug_=False)
        staConnect.sta_mode = 0
        staConnect.upstream_resource = 1
        staConnect.upstream_port = port
        staConnect.radio = radio
        staConnect.resource = 1
        staConnect.dut_ssid = ssid_name
        staConnect.dut_passwd = ssid_psk
        staConnect.dut_security = security
        staConnect.station_names = station
        staConnect.sta_prefix = lanforge_prefix
        staConnect.runtime_secs = 10
        staConnect.bringup_time_sec = 60
        staConnect.cleanup_on_exit = True
        # staConnect.cleanup()
        staConnect.setup()
        staConnect.start()
        print("napping %f sec" % staConnect.runtime_secs)
        time.sleep(staConnect.runtime_secs)
        staConnect.stop()
        staConnect.cleanup()
        run_results = staConnect.get_result_list()
        for result in run_results:
            print("test result: " + result)
        # result = 'pass'
        print("Single Client Connectivity :", staConnect.passes)
        if staConnect.passes() == True:
            print("Single client connection to", ssid_name, "successful. Test Passed")
            client.update_testrail(case_id=test_case, run_id=rid, status_id=1, msg='Client connectivity passed')
            logger.info("Client connectivity to " + ssid_name + " Passed")
            return ("passed")
        else:
            client.update_testrail(case_id=test_case, run_id=rid, status_id=5, msg='Client connectivity failed')
            print("Single client connection to", ssid_name, "unsuccessful. Test Failed")
            logger.warning("Client connectivity to " + ssid_name + " FAILED")
            return ("failed")

    def Single_Client_EAP(port, sta_list, ssid_name, radio, security, eap_type, identity, ttls_password, test_case,
                          rid):
        eap_connect = EAPConnect(lanforge_ip, 8080, _debug_on=False)
        eap_connect.upstream_resource = 1
        eap_connect.upstream_port = port
        eap_connect.security = security
        eap_connect.sta_list = sta_list
        eap_connect.station_names = sta_list
        eap_connect.sta_prefix = lanforge_prefix
        eap_connect.ssid = ssid_name
        eap_connect.radio = radio
        eap_connect.eap = eap_type
        eap_connect.identity = identity
        eap_connect.ttls_passwd = ttls_password
        eap_connect.runtime_secs = 10
        eap_connect.setup()
        eap_connect.start()
        print("napping %f sec" % eap_connect.runtime_secs)
        time.sleep(eap_connect.runtime_secs)
        eap_connect.stop()
        eap_connect.cleanup()
        run_results = eap_connect.get_result_list()
        for result in run_results:
            print("test result: " + result)
        # result = 'pass'
        print("Single Client Connectivity :", eap_connect.passes)
        if eap_connect.passes() == True:
            print("Single client connection to", ssid_name, "successful. Test Passed")
            client.update_testrail(case_id=test_case, run_id=rid, status_id=1, msg='Client connectivity passed')
            logger.info("Client connectivity to " + ssid_name + " Passed")
            return ("passed")
        else:
            client.update_testrail(case_id=test_case, run_id=rid, status_id=5, msg='Client connectivity failed')
            print("Single client connection to", ssid_name, "unsuccessful. Test Failed")
            logger.warning("Client connectivity to " + ssid_name + " FAILED")
            return ("failed")

    def testrail_retest(self, test_case, rid, ssid_name):
        client.update_testrail(case_id=test_case, run_id=rid, status_id=4,
                               msg='Error in Client Connectivity Test. Needs to be Re-run')
        print("Error in test for single client connection to", ssid_name)
        logger.warning("ERROR testing Client connectivity to " + ssid_name)

####Use variables other than defaults for running tests on custom FW etc

###Get Cloud Bearer Token
cloud: CloudSDK = CloudSDK(command_line_args)
bearer = cloud.get_bearer(cloudSDK_url, cloud_type)

model_id = command_line_args.model
equipment_id = command_line_args.equipment_id

print("equipment-id: %s"%(equipment_id))

if equipment_id == "-1":
    eq_id = ap_ssh_ovsh_nodec(command_line_args, 'id')
    print("EQ Id: %s"%(eq_id))

    # Now, query equipment to find something that matches.
    eq = cloud.get_customer_equipment(cloudSDK_url, bearer, customer_id)
    for item in eq:
        for e in item['items']:
            print(e['id'], "  ", e['inventoryId'])
            if e['inventoryId'].endswith("_%s"%(eq_id)):
                print("Found equipment ID: %s  inventoryId: %s",
                      e['id'], e['inventoryId'])
                equipment_id = str(e['id'])

print("Start of Sanity Testing...")
print("Testing Latest Build with Tag: "+build)
if command_line_args.skip_upgrade == True:
    print("Will skip upgrading AP firmware...")

######Testrail Project and Run ID Information ##############################

Test: RunTest = RunTest()

projId = client.get_project_id(project_name=projectId)
print("TIP WLAN Project ID is:", projId)

logger.info('Start of Nightly Sanity')

###Dictionaries
ap_latest_dict = {
    "ec420": "Unknown",
    "ea8300": "Unknown",
    "ecw5211": "unknown",
    "ecw5410": "unknown"
}

# import json file used by throughput test
sanity_status = json.load(open("sanity_status.json"))


############################################################################
#################### Create Report #########################################
############################################################################

# Create Report Folder for Today
today = str(date.today())
try:
    os.mkdir(report_path + today)
except OSError:
    print("Creation of the directory %s failed" % report_path)
else:
    print("Successfully created the directory %s " % report_path)

logger.info('Report data can be found here: ' + report_path + today)

# Copy report template to folder. If template doesn't exist, continue anyway with log
try:
    copyfile(report_template, report_path + today + '/report.php')

except:
    print("No report template created. Report data will still be saved. Continuing with tests...")

##Create report_data dictionary
tc_results = dict.fromkeys(test_cases.values(), "not run")

report_data = dict()
report_data["cloud_sdk"] = dict.fromkeys(ap_models, "")
for key in report_data["cloud_sdk"]:
    report_data["cloud_sdk"][key] = {
        "date": "N/A",
        "commitId": "N/A",
        "projectVersion": "N/A"
    }
report_data["fw_available"] = dict.fromkeys(ap_models, "Unknown")
report_data["fw_under_test"] = dict.fromkeys(ap_models, "N/A")
report_data['pass_percent'] = dict.fromkeys(ap_models, "")

report_data['tests'] = dict.fromkeys(ap_models, "")
for key in ap_models:
    report_data['tests'][key] = dict.fromkeys(test_cases.values(), "not run")

print(report_data)

# write to report_data contents to json file so it has something in case of unexpected fail
with open(report_path + today + '/report_data.json', 'w') as report_json_file:
    json.dump(report_data, report_json_file)


############################################################################
#################### Jfrog Firmware Check ##################################
############################################################################

for model in ap_models:
    apModel = model
    cloudModel = cloud_sdk_models[apModel]
    # print(cloudModel)
    ###Check Latest FW on jFrog
    jfrog_url = 'https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/'
    url = jfrog_url + apModel + "/dev/"
    Build: GetBuild = GetBuild()
    latest_image = Build.get_latest_image(url, build)
    print(model, "Latest FW on jFrog:", latest_image)
    ap_latest_dict[model] = latest_image

####################################################################################
############ Update FW and Run Test Cases on Each AP Variant #######################
####################################################################################
####################################################################################

# Dummy up a single list item.
equipment_ids = {
    model: equipment_id
}
print(equipment_ids)


for key in equipment_ids:
    ##Get Bearer Token to make sure its valid (long tests can require re-auth)
    bearer = cloud.get_bearer(cloudSDK_url, cloud_type)

    ###Get Current AP Firmware and upgrade
    print("AP MODEL UNDER TEST IS", key)
    try:
        ap_cli_info = ssh_cli_active_fw(command_line_args)
        ap_cli_fw = ap_cli_info['active_fw']
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        ap_cli_info = "ERROR"
        print("Cannot Reach AP CLI, will not test this variant");
        continue

    fw_model = ap_cli_fw.partition("-")[0]
    print('Current Active AP FW from CLI:', ap_cli_fw)
    ###Find Latest FW for Current AP Model and Get FW ID

    ##Compare Latest and Current AP FW and Upgrade
    latest_ap_image = ap_latest_dict[fw_model]
    do_upgrade = False
    if ap_cli_fw == latest_ap_image and command_line_args.force_upgrade != True:
        print('FW does not require updating')
        report_data['fw_available'][key] = "No"
        logger.info(fw_model + " does not require upgrade.")
        cloudsdk_cluster_info = {
            "date": "N/A",
            "commitId": "N/A",
            "projectVersion": "N/A"
        }
        report_data['cloud_sdk'][key] = cloudsdk_cluster_info

    if ap_cli_fw != latest_ap_image and command_line_args.skip_upgrade == True:
        print('FW needs updating, but skip_upgrade is True, so skipping upgrade')
        report_data['fw_available'][key] = "No"
        logger.info(fw_model + " firmware upgrade skipped, running with " + ap_cli_fw)
        cloudsdk_cluster_info = {
            "date": "N/A",
            "commitId": "N/A",
            "projectVersion": "N/A"
        }
        report_data['cloud_sdk'][key] = cloudsdk_cluster_info

    if (ap_cli_fw != latest_ap_image or command_line_args.force_upgrade == True) and not command_line_args.skip_upgrade:
        print('Updating firmware, old: %s  new: %s'%(ap_cli_fw, latest_ap_image))
        do_upgrade = True
        report_data['fw_available'][key] = "Yes"
        report_data['fw_under_test'][key] = latest_ap_image

    ###Create Test Run
    today = str(date.today())
    case_ids = list(test_cases.values())
    test_run_name = testRunPrefix + fw_model + "_" + today + "_" + latest_ap_image
    client.create_testrun(name=test_run_name, case_ids=case_ids, project_id=projId, milestone_id=milestoneId,
                          description="Automated Nightly Sanity test run for new firmware build")
    rid = client.get_run_id(test_run_name= testRunPrefix + fw_model + "_" + today + "_" + latest_ap_image)
    print("TIP run ID is:", rid)

    ###GetCloudSDK Version
    print("Getting CloudSDK version information...")
    try:
        cluster_ver = cloud.get_cloudsdk_version(cloudSDK_url, bearer)
        print("CloudSDK Version Information:")
        print("-------------------------------------------")
        print(cluster_ver)
        print("-------------------------------------------")

        cloudsdk_cluster_info = {}
        cloudsdk_cluster_info['date'] = cluster_ver['commitDate']
        cloudsdk_cluster_info['commitId'] = cluster_ver['commitID']
        cloudsdk_cluster_info['projectVersion'] = cluster_ver['projectVersion']
        report_data['cloud_sdk'][key] = cloudsdk_cluster_info
        client.update_testrail(case_id=test_cases["cloud_ver"], run_id=rid, status_id=1,
                               msg='Read CloudSDK version from API successfully')
        report_data['tests'][key][test_cases["cloud_ver"]] = "passed"

    except:
        cluster_ver = 'error'
        print("ERROR: CloudSDK Version Unavailable")
        logger.info('CloudSDK version Unavailable')
        cloudsdk_cluster_info = {
            "date": "unknown",
            "commitId": "unknown",
            "projectVersion": "unknown"
        }
        client.update_testrail(case_id=test_cases["cloud_ver"], run_id=rid, status_id=5,
                               msg='Could not read CloudSDK version from API')
        report_data['cloud_sdk'][key] = cloudsdk_cluster_info
        report_data['tests'][key][test_cases["cloud_ver"]] = "failed"

    with open(report_path + today + '/report_data.json', 'w') as report_json_file:
            json.dump(report_data, report_json_file)

    if do_upgrade:
        ###Test Create Firmware Version
        test_id_fw = test_cases["create_fw"]
        latest_image = ap_latest_dict[key]
        cloudModel = cloud_sdk_models[key]
        print(cloudModel)
        firmware_list_by_model = cloud.CloudSDK_images(cloudModel, cloudSDK_url, bearer)
        print("Available", cloudModel, "Firmware on CloudSDK:", firmware_list_by_model)

        if latest_image in firmware_list_by_model:
            print("Latest Firmware", latest_image, "is already on CloudSDK, need to delete to test create FW API")
            old_fw_id = cloud.get_firmware_id(latest_image, cloudSDK_url, bearer)
            delete_fw = cloud.delete_firmware(str(old_fw_id), cloudSDK_url, bearer)
            fw_url = "https://" + jfrog_user + ":" + jfrog_pwd + "@tip.jfrog.io/artifactory/tip-wlan-ap-firmware/" + key + "/dev/" + latest_image + ".tar.gz"
            commit = latest_image.split("-")[-1]
            try:
                fw_upload_status = cloud.firwmare_upload(commit, cloudModel, latest_image, fw_url, cloudSDK_url,
                                                            bearer)
                fw_id = fw_upload_status['id']
                print("Upload Complete.", latest_image, "FW ID is", fw_id)
                client.update_testrail(case_id=test_id_fw, run_id=rid, status_id=1,
                                       msg='Create new FW version by API successful')
                report_data['tests'][key][test_id_fw] = "passed"
            except:
                fw_upload_status = 'error'
                print("Unable to upload new FW version. Skipping Sanity on AP Model")
                client.update_testrail(case_id=test_id_fw, run_id=rid, status_id=5,
                                       msg='Error creating new FW version by API')
                report_data['tests'][key][test_id_fw] = "failed"
                continue
        else:
            print("Latest Firmware is not on CloudSDK! Uploading...")
            fw_url = "https://" + jfrog_user + ":" + jfrog_pwd + "@tip.jfrog.io/artifactory/tip-wlan-ap-firmware/" + key + "/dev/" + latest_image + ".tar.gz"
            commit = latest_image.split("-")[-1]
            try:
                fw_upload_status = cloud.firwmare_upload(commit, cloudModel, latest_image, fw_url, cloudSDK_url,
                                                            bearer)
                fw_id = fw_upload_status['id']
                print("Upload Complete.", latest_image, "FW ID is", fw_id)
                client.update_testrail(case_id=test_id_fw, run_id=rid, status_id=1,
                                       msg='Create new FW version by API successful')
                report_data['tests'][key][test_id_fw] = "passed"
            except:
                fw_upload_status = 'error'
                print("Unable to upload new FW version. Skipping Sanity on AP Model")
                client.update_testrail(case_id=test_id_fw, run_id=rid, status_id=5,
                                       msg='Error creating new FW version by API')
                report_data['tests'][key][test_id_fw] = "failed"
                continue

        # Upgrade AP firmware
        print("Upgrading...firmware ID is: ", fw_id)
        upgrade_fw = cloud.update_firmware(equipment_id, str(fw_id), cloudSDK_url, bearer)
        logger.info("Lab " + fw_model + " Requires FW update")
        print(upgrade_fw)

        if "success" in upgrade_fw:
            if upgrade_fw["success"] == True:
                print("CloudSDK Upgrade Request Success")
                report_data['tests'][key][test_cases["upgrade_api"]] = "passed"
                client.update_testrail(case_id=test_cases["upgrade_api"], run_id=rid, status_id=1, msg='Upgrade request using API successful')
                logger.info('Firmware upgrade API successfully sent')
            else:
                print("Cloud SDK Upgrade Request Error!")
                # mark upgrade test case as failed with CloudSDK error
                client.update_testrail(case_id=test_cases["upgrade_api"], run_id=rid, status_id=5, msg='Error requesting upgrade via API')
                report_data['tests'][key][test_cases["upgrade_api"]] = "failed"
                logger.warning('Firmware upgrade API failed to send')
                continue
        else:
            print("Cloud SDK Upgrade Request Error!")
            # mark upgrade test case as failed with CloudSDK error
            client.update_testrail(case_id=test_cases["upgrade_api"], run_id=rid, status_id=5,msg='Error requesting upgrade via API')
            report_data['tests'][key][test_cases["upgrade_api"]] = "failed"
            logger.warning('Firmware upgrade API failed to send')
            continue

        sdk_ok = False
        for i in range(10):
            time.sleep(30)
            # Check if upgrade success is displayed on CloudSDK
            test_id_cloud = test_cases["cloud_fw"]
            cloud_ap_fw = cloud.ap_firmware(customer_id, equipment_id, cloudSDK_url, bearer)
            print('Current AP Firmware from CloudSDK: %s  latest-image: %s'%(cloud_ap_fw, latest_ap_image))
            logger.info('AP Firmware from CloudSDK: ' + cloud_ap_fw)
            if cloud_ap_fw == "ERROR":
                print("AP FW Could not be read from CloudSDK")
                
            elif cloud_ap_fw == latest_ap_image:
                print("CloudSDK status shows upgrade successful!")
                sdk_ok = True
                break
                
            else:
                print("AP FW from CloudSDK status is not latest build. Will try again in 30 seconds.")

        cli_ok = False
        if sdk_ok:
            for i in range(10):
                # Check if upgrade successful on AP CLI
                test_id_cli = test_cases["ap_upgrade"]
                try:
                    ap_cli_info = ssh_cli_active_fw(command_line_args)
                    ap_cli_fw = ap_cli_info['active_fw']
                    print("CLI reporting AP Active FW as:", ap_cli_fw)
                    logger.info('Firmware from CLI: ' + ap_cli_fw)
                    if ap_cli_fw == latest_image:
                        cli_ok = True
                        break
                    else:
                        print("probed api-cli-fw: %s  !=  latest-image: %s"%(ap_cli_fw, latest_image))
                        continue
                except Exception as ex:
                    ap_cli_info = "ERROR"
                    print(ex)
                    logging.error(logging.traceback.format_exc())
                    print("Cannot Reach AP CLI to confirm upgrade!")
                    logger.warning('Cannot Reach AP CLI to confirm upgrade!')
                    client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=4,
                                           msg='Cannot reach AP after upgrade to check CLI - re-test required')
                    continue

            time.sleep(30)
        else:
            print("ERROR:  Cloud did not report firmware upgrade within expiration time.")

        if not sdk_ok and cli_ok:
            continue

        if cloud_ap_fw == latest_ap_image and ap_cli_fw == latest_ap_image:
            print("CloudSDK and AP CLI both show upgrade success, passing upgrade test case")
            client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=1,
                                   msg='Upgrade to ' + latest_ap_image + ' successful')
            client.update_testrail(case_id=test_id_cloud, run_id=rid, status_id=1,
                                   msg='CLOUDSDK reporting correct firmware version.')
            report_data['tests'][key][test_id_cli] = "passed"
            report_data['tests'][key][test_id_cloud] = "passed"
            print(report_data['tests'][key])

        elif cloud_ap_fw != latest_ap_image and ap_cli_fw == latest_ap_image:
            print("AP CLI shows upgrade success - CloudSDK reporting error!")
            ##Raise CloudSDK error but continue testing
            client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=1,
                                   msg='Upgrade to ' + latest_ap_image + ' successful.')
            client.update_testrail(case_id=test_id_cloud, run_id=rid, status_id=5,
                                   msg='CLOUDSDK reporting incorrect firmware version.')
            report_data['tests'][key][test_id_cli] = "passed"
            report_data['tests'][key][test_id_cloud] = "failed"
            print(report_data['tests'][key])

        elif cloud_ap_fw == latest_ap_image and ap_cli_fw != latest_ap_image:
            print("AP CLI shows upgrade failed - CloudSDK reporting error!")
            # Testrail TC fail
            client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=5,
                                   msg='AP failed to download or apply new FW. Upgrade to ' + latest_ap_image + ' Failed')
            client.update_testrail(case_id=test_id_cloud, run_id=rid, status_id=5,
                                   msg='CLOUDSDK reporting incorrect firmware version.')
            report_data['tests'][key][test_id_cli] = "failed"
            report_data['tests'][key][test_id_cloud] = "failed"
            print(report_data['tests'][key])
            continue

        elif cloud_ap_fw != latest_ap_image and ap_cli_fw != latest_ap_image:
            print("Upgrade Failed! Confirmed on CloudSDK and AP CLI. Upgrade test case failed.")
            ##fail TR testcase and exit
            client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=5,
                                   msg='AP failed to download or apply new FW. Upgrade to ' + latest_ap_image + ' Failed')
            report_data['tests'][key][test_id_cli] = "failed"
            print(report_data['tests'][key])
            continue

        else:
            print("Unable to determine upgrade status. Skipping AP variant")
            # update TR testcase as error
            client.update_testrail(case_id=test_id_cli, run_id=rid, status_id=4,
                                   msg='Cannot determine upgrade status - re-test required')
            report_data['tests'][key][test_id_cli] = "error"
            print(report_data['tests'][key])
            continue

        print(report_data)

    # TODO:  Fix indentation, break all this up into small test cases anyway.
    if True:
        ###Check AP Manager Status
        manager_status = ap_cli_info['state']

        if manager_status != "active":
            print("Manager status is " + manager_status + "! Not connected to the cloud.")
            print("Waiting 30 seconds and re-checking status")
            time.sleep(30)
            ap_cli_info = ssh_cli_active_fw(command_line_args)
            manager_status = ap_cli_info['state']
            if manager_status != "active":
                print("Manager status is", manager_status, "! Not connected to the cloud.")
                print("Manager status fails multiple checks - failing test case.")
                ##fail cloud connectivity testcase
                client.update_testrail(case_id=test_cases["cloud_connection"], run_id=rid, status_id=5, msg='CloudSDK connectivity failed')
                report_data['tests'][key][test_cases["cloud_connection"]] = "failed"
                print(report_data['tests'][key])
                continue
            else:
                print("Manager status is Active. Proceeding to connectivity testing!")
                # TC522 pass in Testrail
                client.update_testrail(case_id=test_cases["cloud_connection"], run_id=rid, status_id=1, msg='Manager status is Active')
                report_data['tests'][key][test_cases["cloud_connection"]] = "passed"
                print(report_data['tests'][key])
        else:
            print("Manager status is Active. Proceeding to connectivity testing!")
            # TC5222 pass in testrail
            client.update_testrail(case_id=test_cases["cloud_connection"], run_id=rid, status_id=1, msg='Manager status is Active')
            report_data['tests'][key][test_cases["cloud_connection"]] = "passed"
            print(report_data['tests'][key])
            # Pass cloud connectivity test case

        ###Update report json
        with open(report_path + today + '/report_data.json', 'w') as report_json_file:
            json.dump(report_data, report_json_file)

        radius_name = "%s-%s-%s"%(command_line_args.testbed, fw_model, "Radius")

        prof_5g_eap_name = "%s-%s-%s"%(command_line_args.testbed, fw_model, "5G_EAP")
        prof_5g_wpa2_name = "%s-%s-%s"%(command_line_args.testbed, fw_model, "5G_WPA2")
        prof_5g_wpa_name = "%s-%s-%s"%(command_line_args.testbed, fw_model, "5G_WPA")
        prof_2g_eap_name = "%s-%s-%s"%(command_line_args.testbed, fw_model, "2G_EAP")
        prof_2g_wpa2_name = "%s-%s-%s"%(command_line_args.testbed, fw_model, "2G_WPA2")
        prof_2g_wpa_name = "%s-%s-%s"%(command_line_args.testbed, fw_model, "2G_WPA")

        prof_5g_eap_name_nat = "%s-%s-%s"%(command_line_args.testbed, fw_model, "5G_EAP_NAT")
        prof_5g_wpa2_name_nat = "%s-%s-%s"%(command_line_args.testbed, fw_model, "5G_WPA2_NAT")
        prof_5g_wpa_name_nat = "%s-%s-%s"%(command_line_args.testbed, fw_model, "5G_WPA_NAT")
        prof_2g_eap_name_nat = "%s-%s-%s"%(command_line_args.testbed, fw_model, "2G_EAP_NAT")
        prof_2g_wpa2_name_nat = "%s-%s-%s"%(command_line_args.testbed, fw_model, "2G_WPA2_NAT")
        prof_2g_wpa_name_nat = "%s-%s-%s"%(command_line_args.testbed, fw_model, "2G_WPA_NAT")

        prof_5g_eap_name_vlan = "%s-%s-%s"%(command_line_args.testbed, fw_model, "5G_EAP_VLAN")
        prof_5g_wpa2_name_vlan = "%s-%s-%s"%(command_line_args.testbed, fw_model, "5G_WPA2_VLAN")
        prof_5g_wpa_name_vlan = "%s-%s-%s"%(command_line_args.testbed, fw_model, "5G_WPA_VLAN")
        prof_2g_eap_name_vlan = "%s-%s-%s"%(command_line_args.testbed, fw_model, "2G_EAP_VLAN")
        prof_2g_wpa2_name_vlan = "%s-%s-%s"%(command_line_args.testbed, fw_model, "2G_WPA2_VLAN")
        prof_2g_wpa_name_vlan = "%s-%s-%s"%(command_line_args.testbed, fw_model, "2G_WPA_VLAN")

        prof_names = [prof_5g_eap_name, prof_5g_wpa2_name, prof_5g_wpa_name, prof_2g_eap_name, prof_2g_wpa2_name, prof_2g_wpa_name,
                      prof_5g_eap_name_nat, prof_5g_wpa2_name_nat, prof_5g_wpa_name_nat, prof_2g_eap_name_nat, prof_2g_wpa2_name_nat, prof_2g_wpa_name_nat,
                      prof_5g_eap_name_vlan, prof_5g_wpa2_name_vlan, prof_5g_wpa_name_vlan, prof_2g_eap_name_vlan, prof_2g_wpa2_name_vlan, prof_2g_wpa_name_vlan]

        # First, remove any existing profiles
        # Paginated reads means we get an array of json objects back, one object per 'page'
        # NOTE:  Cloud gives error when I try to remove these.  Not sure removal works?
        #profs = cloud.get_customer_profiles(cloudSDK_url, bearer, customer_id)
        #for p in profs:
        #    for e in p['items']:
        #        prof_id = str(e['id'])
        #        prof_model_type = e['model_type']
        #        #print(" prof-id: %s  model-type: %s"%(prof_id, prof_model_type))
        #        prof_type = e['profileType']
        #        prof_name = e['name']
        #        print("Profile: ", prof_id, " Model-Type: ", prof_model_type, " Profile-Type: ", prof_type, " Name: ", prof_name)
        #        for pn in prof_names:
        #            if pn == prof_name:
        #                print("Deleting existing profile name: ", pn)
        #                cloud.delete_customer_profile(cloudSDK_url, bearer, customer_id, prof_id)

        ### Create RADIUS profile - used for all EAP SSIDs
        radius_template = "Radius-Profile"  # Default radius profile found in cloud-sdk
        subnet_name = radius_info['subnet_name']
        subnet = radius_info['subnet']
        subnet_mask = radius_info['subnet_mask']
        region = radius_info['region']
        server_name = radius_info['server_name']
        server_ip = radius_info['server_ip']
        secret = radius_info['secret']
        auth_port = radius_info['auth_port']
        try:
            radius_profile = cloud.create_or_update_radius_profile(cloudSDK_url, bearer, customer_id, radius_template, radius_name, subnet_name, subnet,
                                                                   subnet_mask, region, server_name, server_ip, secret, auth_port)
            print("radius profile Id is", radius_profile)
            client.update_testrail(case_id=test_cases["radius_profile"], run_id=rid, status_id=1,
                                   msg='RADIUS profile created successfully')
            report_data['tests'][key][test_cases["radius_profile"]] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            radius_profile = 'error'
            print("RADIUS Profile Create Error, will skip radius profile.")
            #Set backup profile ID so test can continue
            radius_profile = None
            server_name = "Lab-RADIUS"
            client.update_testrail(case_id=test_cases["radius_profile"], run_id=rid, status_id=5,
                                   msg='Failed to create RADIUS profile')
            report_data['tests'][key][test_cases["radius_profile"]] = "failed"

        ###########################################################################
        ############## Bridge Mode Client Connectivity ############################
        ###########################################################################

        ### Create SSID Profiles
        ssid_template = "templates/ssid_profile_template.json"

        # 5G SSIDs
        try:
            fiveG_eap = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template, prof_5g_eap_name,
                                                            profile_info_dict[fw_model]["fiveG_WPA2-EAP_SSID"], None,
                                                            radius_name,
                                                            "wpa2OnlyRadius", "BRIDGE", 1, ["is5GHzU", "is5GHz", "is5GHzL"])
            print("5G EAP SSID created successfully - bridge mode")
            client.update_testrail(case_id=test_cases["ssid_5g_eap_bridge"], run_id=rid, status_id=1, msg='5G EAP SSID created successfully - bridge mode')
            report_data['tests'][key][test_cases["ssid_5g_eap_bridge"]] = "passed"

        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            fiveG_eap = "error"
            print("5G EAP SSID create failed - bridge mode")
            client.update_testrail(case_id=test_cases["ssid_5g_eap_bridge"], run_id=rid, status_id=5,
                                   msg='5G EAP SSID create failed - bridge mode')
            report_data['tests'][key][test_cases["ssid_5g_eap_bridge"]] = "failed"
            fiveG_eap = profile_info_dict[fw_model]["fiveG_WPA2-EAP_profile"]

        try:
            fiveG_wpa2 = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template, prof_5g_wpa2_name,
                                                             profile_info_dict[fw_model]["fiveG_WPA2_SSID"],
                                                             profile_info_dict[fw_model]["fiveG_WPA2_PSK"],
                                                             "Radius-Accounting-Profile", "wpa2OnlyPSK", "BRIDGE", 1,
                                                             ["is5GHzU", "is5GHz", "is5GHzL"])
            print("5G WPA2 SSID created successfully - bridge mode")
            client.update_testrail(case_id=test_cases["ssid_5g_wpa2_bridge"], run_id=rid, status_id=1, msg='5G WPA2 SSID created successfully - bridge mode')
            report_data['tests'][key][test_cases["ssid_5g_wpa2_bridge"]] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            fiveG_wpa2 = "error"
            print("5G WPA2 SSID create failed - bridge mode")
            client.update_testrail(case_id=test_cases["ssid_5g_wpa2_bridge"], run_id=rid, status_id=5,
                                   msg='5G WPA2 SSID create failed - bridge mode')
            report_data['tests'][key][test_cases["ssid_5g_wpa2_bridge"]] = "failed"
            fiveG_wpa2 = profile_info_dict[fw_model]["fiveG_WPA2_profile"]

        try:
            fiveG_wpa = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template, prof_5g_wpa_name,
                                                            profile_info_dict[fw_model]["fiveG_WPA_SSID"],
                                                            profile_info_dict[fw_model]["fiveG_WPA_PSK"],
                                                            "Radius-Accounting-Profile", "wpaPSK", "BRIDGE", 1,
                                                            ["is5GHzU", "is5GHz", "is5GHzL"])
            print("5G WPA SSID created successfully - bridge mode")
            client.update_testrail(case_id=test_cases["ssid_5g_wpa_bridge"], run_id=rid, status_id=1,
                                   msg='5G WPA SSID created successfully - bridge mode')
            report_data['tests'][key][test_cases["ssid_5g_wpa_bridge"]] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            fiveG_wpa = "error"
            print("5G WPA SSID create failed - bridge mode")
            client.update_testrail(case_id=test_cases["ssid_5g_wpa_bridge"], run_id=rid, status_id=5,
                                   msg='5G WPA SSID create failed - bridge mode')
            report_data['tests'][key][test_cases["ssid_5g_wpa_bridge"]] = "failed"
            fiveG_wpa = profile_info_dict[fw_model]["fiveG_WPA_profile"]

        # 2.4G SSIDs
        try:
            twoFourG_eap = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                               prof_2g_eap_name,
                                                               profile_info_dict[fw_model]["twoFourG_WPA2-EAP_SSID"], None,
                                                               radius_name, "wpa2OnlyRadius", "BRIDGE", 1, ["is2dot4GHz"])
            print("2.4G EAP SSID created successfully - bridge mode")
            client.update_testrail(case_id=test_cases["ssid_2g_eap_bridge"], run_id=rid, status_id=1,
                                   msg='2.4G EAP SSID created successfully - bridge mode')
            report_data['tests'][key][test_cases["ssid_2g_eap_bridge"]] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            twoFourG_eap = "error"
            print("2.4G EAP SSID create failed - bridge mode")
            client.update_testrail(case_id=test_cases["ssid_2g_eap_bridge"], run_id=rid, status_id=5,
                                   msg='2.4G EAP SSID create failed - bridge mode')
            report_data['tests'][key][test_cases["ssid_2g_eap_bridge"]] = "failed"
            twoFourG_eap = profile_info_dict[fw_model]["twoFourG_WPA2-EAP_SSID"]

        try:
            twoFourG_wpa2 = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                                prof_2g_wpa2_name,
                                                                profile_info_dict[fw_model]["twoFourG_WPA2_SSID"],
                                                                profile_info_dict[fw_model]["twoFourG_WPA2_PSK"],
                                                                "Radius-Accounting-Profile", "wpa2OnlyPSK", "BRIDGE", 1,
                                                                ["is2dot4GHz"])
            print("2.4G WPA2 SSID created successfully - bridge mode")
            client.update_testrail(case_id=test_cases["ssid_2g_wpa2_bridge"], run_id=rid, status_id=1,
                                   msg='2.4G WPA2 SSID created successfully - bridge mode')
            report_data['tests'][key][test_cases["ssid_2g_wpa2_bridge"]] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            twoFourG_wpa2 = "error"
            print("2.4G WPA2 SSID create failed - bridge mode")
            client.update_testrail(case_id=test_cases["ssid_2g_wpa2_bridge"], run_id=rid, status_id=5,
                                   msg='2.4G WPA2 SSID create failed - bridge mode')
            report_data['tests'][key][test_cases["ssid_2g_wpa2_bridge"]] = "failed"
            twoFourG_wpa2 = profile_info_dict[fw_model]["twoFourG_WPA2_SSID"]

        try:
            twoFourG_wpa = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                               prof_2g_wpa_name,
                                                               profile_info_dict[fw_model]["twoFourG_WPA_SSID"],
                                                               profile_info_dict[fw_model]["twoFourG_WPA_PSK"],
                                                               "Radius-Accounting-Profile", "wpaPSK", "BRIDGE", 1,
                                                               ["is2dot4GHz"])
            print("2.4G WPA SSID created successfully - bridge mode")
            client.update_testrail(case_id=test_cases["ssid_2g_wpa_bridge"], run_id=rid, status_id=1,
                                   msg='2.4G WPA SSID created successfully - bridge mode')
            report_data['tests'][key][test_cases["ssid_2g_wpa_bridge"]] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            twoFourG_wpa = "error"
            print("2.4G WPA SSID create failed - bridge mode")
            client.update_testrail(case_id=test_cases["ssid_2g_wpa_bridge"], run_id=rid, status_id=5,
                                   msg='2.4G WPA SSID create failed - bridge mode')
            report_data['tests'][key][test_cases["ssid_2g_wpa_bridge"]] = "failed"
            twoFourG_wpa = profile_info_dict[fw_model]["twoFourG_WPA_SSID"]

        ### Create AP Bridge Profile
        rfProfileId = lab_ap_info.rf_profile
        child_profiles = [fiveG_eap, fiveG_wpa2, fiveG_wpa, twoFourG_eap, twoFourG_wpa2, twoFourG_wpa, rfProfileId]
        if radius_profile != None:
            child_profiles.append(radius_profile)
        print(child_profiles)

        name = "Nightly_Sanity_" + fw_model + "_" + today + "_bridge"

        try:
            create_ap_profile = cloud.create_or_update_ap_profile(cloudSDK_url, bearer, customer_id,
                                                                  command_line_args.default_ap_profile, name, child_profiles)
            test_profile_id = create_ap_profile
            print("Test Profile ID for Test is:",test_profile_id)
            client.update_testrail(case_id=test_cases["ap_bridge"], run_id=rid, status_id=1,
                                   msg='AP profile for bridge tests created successfully')
            report_data['tests'][key][test_cases["ap_bridge"]] = "passed"
        except Exception as ex:
            print(ex)
            logging.error(logging.traceback.format_exc())
            create_ap_profile = "error"
            test_profile_id = profile_info_dict[fw_model]["profile_id"]
            print("Error creating AP profile for bridge tests. Will use existing AP profile")
            client.update_testrail(case_id=test_cases["ap_bridge"], run_id=rid, status_id=5,
                                   msg='AP profile for bridge tests could not be created using API')
            report_data['tests'][key][test_cases["ap_bridge"]] = "failed"

        ### Set Proper AP Profile for Bridge SSID Tests
        ap_profile = cloud.set_ap_profile(equipment_id, test_profile_id, cloudSDK_url, bearer)

        ### Wait for Profile Push
        time.sleep(180)

        ### Check if VIF Config and VIF State reflect AP Profile from CloudSDK
        ## VIF Config
        try:
            ssid_config = profile_info_dict[key]["ssid_list"]
            print("SSIDs in AP Profile:", ssid_config)

            ssid_list = ap_ssh.get_vif_config(command_line_args)
            print("SSIDs in AP VIF Config:", ssid_list)

            if set(ssid_list) == set(ssid_config):
                print("SSIDs in Wifi_VIF_Config Match AP Profile Config")
                client.update_testrail(case_id=test_cases["bridge_vifc"], run_id=rid, status_id=1,
                                       msg='SSIDs in VIF Config matches AP Profile Config')
                report_data['tests'][key][test_cases["bridge_vifc"]] = "passed"
            else:
                print("SSIDs in Wifi_VIF_Config do not match desired AP Profile Config")
                client.update_testrail(case_id=test_cases["bridge_vifc"], run_id=rid, status_id=5,
                                       msg='SSIDs in VIF Config do not match AP Profile Config')
                report_data['tests'][key][test_cases["bridge_vifc"]] = "failed"
        except:
            ssid_list = "ERROR"
            print("Error accessing VIF Config from AP CLI")
            client.update_testrail(case_id=test_cases["bridge_vifc"], run_id=rid, status_id=4,
                                   msg='Cannot determine VIF Config - re-test required')
            report_data['tests'][key][test_cases["bridge_vifc"]] = "error"
        # VIF State
        try:
            ssid_state = ap_ssh.get_vif_state(command_line_args)
            print("SSIDs in AP VIF State:", ssid_state)

            if set(ssid_state) == set(ssid_config):
                print("SSIDs properly applied on AP")
                client.update_testrail(case_id=test_cases["bridge_vifs"], run_id=rid, status_id=1,
                                       msg='SSIDs in VIF Config applied to VIF State')
                report_data['tests'][key][test_cases["bridge_vifs"]] = "passed"
            else:
                print("SSIDs not applied on AP")
                client.update_testrail(case_id=test_cases["bridge_vifs"], run_id=rid, status_id=5,
                                       msg='SSIDs in VIF Config not applied to VIF State')
                report_data['tests'][key][test_cases["bridge_vifs"]] = "failed"
        except:
            ssid_list = "ERROR"
            print("Error accessing VIF State from AP CLI")
            print("Error accessing VIF Config from AP CLI")
            client.update_testrail(case_id=test_cases["bridge_vifs"], run_id=rid, status_id=4,
                                   msg='Cannot determine VIF State - re-test required')
            report_data['tests'][key][test_cases["bridge_vifs"]] = "error"

        ### Set LANForge port for tests
        port = "eth2"

        # print iwinfo for information
        iwinfo = iwinfo_status(command_line_args)
        print(iwinfo)

        ###Run Client Single Connectivity Test Cases for Bridge SSIDs
        # TC5214 - 2.4 GHz WPA2-Enterprise
        test_case = test_cases["2g_eap_bridge"]
        radio = lab_ap_info.lanforge_2dot4g
        sta_list = [lanforge_prefix+"5214"]
        ssid_name = profile_info_dict[fw_model]["twoFourG_WPA2-EAP_SSID"]
        security = "wpa2"
        eap_type = "TTLS"
        try:
            test_result = RunTest.Single_Client_EAP(port, sta_list, ssid_name, radio, security, eap_type, identity,
                                                    ttls_password, test_case, rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        ###Run Client Single Connectivity Test Cases for Bridge SSIDs
        # TC - 2.4 GHz WPA2
        test_case = test_cases["2g_wpa2_bridge"]
        radio = lab_ap_info.lanforge_2dot4g
        station = [lanforge_prefix+"2237"]
        ssid_name = profile_info_dict[fw_model]["twoFourG_WPA2_SSID"]
        ssid_psk = profile_info_dict[fw_model]["twoFourG_WPA2_PSK"]
        security = "wpa2"
        try:
            test_result = Test.Single_Client_Connectivity(port, radio, ssid_name, ssid_psk, security, station,
                                                          test_case,
                                                          rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        # TC - 2.4 GHz WPA
        test_case = test_cases["2g_wpa_bridge"]
        radio = lab_ap_info.lanforge_2dot4g
        station = [lanforge_prefix+"2420"]
        ssid_name = profile_info_dict[fw_model]["twoFourG_WPA_SSID"]
        ssid_psk = profile_info_dict[fw_model]["twoFourG_WPA_PSK"]
        security = "wpa"
        try:
            test_result = Test.Single_Client_Connectivity(port, radio, ssid_name, ssid_psk, security, station,
                                                          test_case,
                                                          rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        # TC - 5 GHz WPA2-Enterprise
        test_case = test_cases["5g_eap_bridge"]
        radio = lab_ap_info.lanforge_5g
        sta_list = [lanforge_prefix+"5215"]
        ssid_name = profile_info_dict[fw_model]["fiveG_WPA2-EAP_SSID"]
        security = "wpa2"
        eap_type = "TTLS"
        try:
            test_result = RunTest.Single_Client_EAP(port, sta_list, ssid_name, radio, security, eap_type, identity,
                                                    ttls_password, test_case, rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        # TC 5 GHz WPA2
        test_case = test_cases["5g_wpa2_bridge"]
        radio = lab_ap_info.lanforge_5g
        station = [lanforge_prefix+"2236"]
        ssid_name = profile_info_dict[fw_model]["fiveG_WPA2_SSID"]
        ssid_psk = profile_info_dict[fw_model]["fiveG_WPA2_PSK"]
        security = "wpa2"
        try:
            test_result = Test.Single_Client_Connectivity(port, radio, ssid_name, ssid_psk, security, station,
                                                          test_case,
                                                          rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        # TC - 5 GHz WPA
        test_case = test_cases["5g_wpa_bridge"]
        radio = lab_ap_info.lanforge_5g
        station = [lanforge_prefix+"2419"]
        ssid_name = profile_info_dict[fw_model]["fiveG_WPA_SSID"]
        ssid_psk = profile_info_dict[fw_model]["fiveG_WPA_PSK"]
        security = "wpa"
        try:
            test_result = Test.Single_Client_Connectivity(port, radio, ssid_name, ssid_psk, security, station,
                                                          test_case,
                                                          rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        logger.info("Testing for " + fw_model + "Bridge Mode SSIDs Complete")
        with open(report_path + today + '/report_data.json', 'w') as report_json_file:
            json.dump(report_data, report_json_file)

        ###########################################################################
        ################# NAT Mode Client Connectivity ############################
        ###########################################################################

        ### Create SSID Profiles
        ssid_template = "templates/ssid_profile_template.json"

        # 5G SSIDs
        try:
            fiveG_eap = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                            prof_5g_eap_name_nat,
                                                            profile_info_dict[fw_model + '_nat']["fiveG_WPA2-EAP_SSID"], None,
                                                            radius_name,
                                                            "wpa2OnlyRadius", "NAT", 1,
                                                            ["is5GHzU", "is5GHz", "is5GHzL"])
            print("5G EAP SSID created successfully - NAT mode")
            client.update_testrail(case_id=test_cases["ssid_5g_eap_nat"], run_id=rid, status_id=1,
                                   msg='5G EAP SSID created successfully - NAT mode')
            report_data['tests'][key][test_cases["ssid_5g_eap_nat"]] = "passed"

        except:
            fiveG_eap = "error"
            print("5G EAP SSID create failed - NAT mode")
            client.update_testrail(case_id=test_cases["ssid_5g_eap_nat"], run_id=rid, status_id=5,
                                   msg='5G EAP SSID create failed - NAT mode')
            report_data['tests'][key][test_cases["ssid_5g_eap_nat"]] = "failed"
            fiveG_eap = profile_info_dict[fw_model + '_nat']["fiveG_WPA2-EAP_profile"]

        try:
            fiveG_wpa2 = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                             prof_5g_wpa2_name_nat,
                                                             profile_info_dict[fw_model + '_nat']["fiveG_WPA2_SSID"],
                                                             profile_info_dict[fw_model + '_nat']["fiveG_WPA2_PSK"],
                                                             "Radius-Accounting-Profile", "wpa2OnlyPSK", "NAT", 1,
                                                             ["is5GHzU", "is5GHz", "is5GHzL"])
            print("5G WPA2 SSID created successfully - NAT mode")
            client.update_testrail(case_id=test_cases["ssid_5g_wpa2_nat"], run_id=rid, status_id=1,
                                   msg='5G WPA2 SSID created successfully - NAT mode')
            report_data['tests'][key][test_cases["ssid_5g_wpa2_nat"]] = "passed"
        except:
            fiveG_wpa2 = "error"
            print("5G WPA2 SSID create failed - NAT mode")
            client.update_testrail(case_id=test_cases["ssid_5g_wpa2_nat"], run_id=rid, status_id=5,
                                   msg='5G WPA2 SSID create failed - NAT mode')
            report_data['tests'][key][test_cases["ssid_5g_wpa2_nat"]] = "failed"
            fiveG_wpa2 = profile_info_dict[fw_model + '_nat']["fiveG_WPA2_profile"]

        try:
            fiveG_wpa = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                            prof_5g_wpa_name_nat,
                                                            profile_info_dict[fw_model + '_nat']["fiveG_WPA_SSID"],
                                                            profile_info_dict[fw_model + '_nat']["fiveG_WPA_PSK"],
                                                            "Radius-Accounting-Profile", "wpaPSK", "NAT", 1,
                                                            ["is5GHzU", "is5GHz", "is5GHzL"])
            print("5G WPA SSID created successfully - NAT mode")
            client.update_testrail(case_id=test_cases["ssid_5g_wpa_nat"], run_id=rid, status_id=1,
                                   msg='5G WPA SSID created successfully - NAT mode')
            report_data['tests'][key][test_cases["ssid_5g_wpa_nat"]] = "passed"
        except:
            fiveG_wpa = "error"
            print("5G WPA SSID create failed - NAT mode")
            client.update_testrail(case_id=test_cases["ssid_5g_wpa_nat"], run_id=rid, status_id=5,
                                   msg='5G WPA SSID create failed - NAT mode')
            report_data['tests'][key][test_cases["ssid_5g_wpa_nat"]] = "failed"
            fiveG_wpa = profile_info_dict[fw_model + '_nat']["fiveG_WPA_profile"]

            # 2.4G SSIDs
        try:
            twoFourG_eap = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                               prof_2g_eap_name_nat,
                                                               profile_info_dict[fw_model + '_nat']["twoFourG_WPA2-EAP_SSID"],
                                                               None,
                                                               radius_name, "wpa2OnlyRadius", "NAT", 1, ["is2dot4GHz"])
            print("2.4G EAP SSID created successfully - NAT mode")
            client.update_testrail(case_id=test_cases["ssid_2g_eap_nat"], run_id=rid, status_id=1,
                                   msg='2.4G EAP SSID created successfully - NAT mode')
            report_data['tests'][key][test_cases["ssid_2g_eap_nat"]] = "passed"
        except:
            twoFourG_eap = "error"
            print("2.4G EAP SSID create failed - NAT mode")
            client.update_testrail(case_id=test_cases["ssid_2g_eap_nat"], run_id=rid, status_id=5,
                                   msg='2.4G EAP SSID create failed - NAT mode')
            report_data['tests'][key][test_cases["ssid_2g_eap_nat"]] = "failed"
            twoFourG_eap = profile_info_dict[fw_model + '_nat']["twoFourG_WPA2-EAP_SSID"]

        try:
            twoFourG_wpa2 = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                                prof_2g_wpa2_name_nat,
                                                                profile_info_dict[fw_model + '_nat']["twoFourG_WPA2_SSID"],
                                                                profile_info_dict[fw_model + '_nat']["twoFourG_WPA2_PSK"],
                                                                "Radius-Accounting-Profile", "wpa2OnlyPSK", "NAT", 1,
                                                                ["is2dot4GHz"])
            print("2.4G WPA2 SSID created successfully - NAT mode")
            client.update_testrail(case_id=test_cases["ssid_2g_wpa2_nat"], run_id=rid, status_id=1,
                                   msg='2.4G WPA2 SSID created successfully - NAT mode')
            report_data['tests'][key][test_cases["ssid_2g_wpa2_nat"]] = "passed"
        except:
            twoFourG_wpa2 = "error"
            print("2.4G WPA2 SSID create failed - NAT mode")
            client.update_testrail(case_id=test_cases["ssid_2g_wpa2_nat"], run_id=rid, status_id=5,
                                   msg='2.4G WPA2 SSID create failed - NAT mode')
            report_data['tests'][key][test_cases["ssid_2g_wpa2_nat"]] = "failed"
            twoFourG_wpa2 = profile_info_dict[fw_model + '_nat']["twoFourG_WPA2_SSID"]

        try:
            twoFourG_wpa = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                               prof_2g_wpa_name_nat,
                                                               profile_info_dict[fw_model + '_nat']["twoFourG_WPA_SSID"],
                                                               profile_info_dict[fw_model + '_nat']["twoFourG_WPA_PSK"],
                                                               "Radius-Accounting-Profile", "wpaPSK", "NAT", 1,
                                                               ["is2dot4GHz"])
            print("2.4G WPA SSID created successfully - NAT mode")
            client.update_testrail(case_id=test_cases["ssid_2g_wpa_nat"], run_id=rid, status_id=1,
                                   msg='2.4G WPA SSID created successfully - NAT mode')
            report_data['tests'][key][test_cases["ssid_2g_wpa_nat"]] = "passed"
        except:
            twoFourG_wpa = "error"
            print("2.4G WPA SSID create failed - NAT mode")
            client.update_testrail(case_id=test_cases["ssid_2g_wpa_nat"], run_id=rid, status_id=5,
                                   msg='2.4G WPA SSID create failed - NAT mode')
            report_data['tests'][key][test_cases["ssid_2g_wpa_nat"]] = "failed"
            twoFourG_wpa = profile_info_dict[fw_model + '_nat']["twoFourG_WPA_SSID"]

        ### Create AP NAT Profile
        rfProfileId = lab_ap_info.rf_profile
        child_profiles = [fiveG_eap, fiveG_wpa2, fiveG_wpa, twoFourG_eap, twoFourG_wpa2, twoFourG_wpa, rfProfileId]
        if radius_profile != None:
            child_profiles.append(radius_profile)
        print(child_profiles)
        name = "Nightly_Sanity_" + fw_model + "_" + today + "_nat"
        try:
            create_ap_profile = cloud.create_or_update_ap_profile(cloudSDK_url, bearer, customer_id,
                                                                  command_line_args.default_ap_profile, name, child_profiles)
            test_profile_id = create_ap_profile
            print("Test Profile ID for Test is:", test_profile_id)
            client.update_testrail(case_id=test_cases["ap_nat"], run_id=rid, status_id=1,
                                       msg='AP profile for NAT tests created successfully')
            report_data['tests'][key][test_cases["ap_nat"]] = "passed"
        except:
            create_ap_profile = "error"
            test_profile_id = profile_info_dict[fw_model + '_nat']["profile_id"]
            print("Error creating AP profile for NAT tests. Will use existing AP profile")
            client.update_testrail(case_id=test_cases["ap_nat"], run_id=rid, status_id=5,
                                       msg='AP profile for NAT tests could not be created using API')
            report_data['tests'][key][test_cases["ap_nat"]] = "failed"

        ###Set Proper AP Profile for NAT SSID Tests
        ap_profile = cloud.set_ap_profile(equipment_id, test_profile_id, cloudSDK_url, bearer)

        ### Wait for Profile Push
        time.sleep(180)

        ###Check if VIF Config and VIF State reflect AP Profile from CloudSDK
        ## VIF Config
        try:
            ssid_config = profile_info_dict[fw_model + '_nat']["ssid_list"]
            print("SSIDs in AP Profile:", ssid_config)

            ssid_list = ap_ssh.get_vif_config(command_line_args)
            print("SSIDs in AP VIF Config:", ssid_list)

            if set(ssid_list) == set(ssid_config):
                print("SSIDs in Wifi_VIF_Config Match AP Profile Config")
                client.update_testrail(case_id=test_cases["nat_vifc"], run_id=rid, status_id=1,
                                       msg='SSIDs in VIF Config matches AP Profile Config')
                report_data['tests'][key][test_cases["nat_vifc"]] = "passed"
            else:
                print("SSIDs in Wifi_VIF_Config do not match desired AP Profile Config")
                client.update_testrail(case_id=test_cases["nat_vifc"], run_id=rid, status_id=5,
                                       msg='SSIDs in VIF Config do not match AP Profile Config')
                report_data['tests'][key][test_cases["nat_vifc"]] = "failed"
        except:
            ssid_list = "ERROR"
            print("Error accessing VIF Config from AP CLI")
            client.update_testrail(case_id=test_cases["nat_vifc"], run_id=rid, status_id=4,
                                   msg='Cannot determine VIF Config - re-test required')
            report_data['tests'][key][test_cases["nat_vifc"]] = "error"
        # VIF State
        try:
            ssid_state = ap_ssh.get_vif_state(command_line_args)
            print("SSIDs in AP VIF State:", ssid_state)

            if set(ssid_state) == set(ssid_config):
                print("SSIDs properly applied on AP")
                client.update_testrail(case_id=test_cases["nat_vifs"], run_id=rid, status_id=1,
                                       msg='SSIDs in VIF Config applied to VIF State')
                report_data['tests'][key][test_cases["nat_vifs"]] = "passed"
            else:
                print("SSIDs not applied on AP")
                client.update_testrail(case_id=test_cases["nat_vifs"], run_id=rid, status_id=5,
                                       msg='SSIDs in VIF Config not applied to VIF State')
                report_data['tests'][key][test_cases["nat_vifs"]] = "failed"
        except:
            ssid_list = "ERROR"
            print("Error accessing VIF State from AP CLI")
            print("Error accessing VIF Config from AP CLI")
            client.update_testrail(case_id=test_cases["nat_vifs"], run_id=rid, status_id=4,
                                   msg='Cannot determine VIF State - re-test required')
            report_data['tests'][key][test_cases["nat_vifs"]] = "error"

        ### Set LANForge port for tests
        port = "eth2"

        # Print iwinfo for logs
        iwinfo = iwinfo_status(command_line_args)
        print(iwinfo)

        ###Run Client Single Connectivity Test Cases for NAT SSIDs
        # TC - 2.4 GHz WPA2-Enterprise NAT
        test_case = test_cases["2g_eap_nat"]
        radio = lab_ap_info.lanforge_2dot4g
        sta_list = [lanforge_prefix+"5216"]
        ssid_name = profile_info_dict[fw_model + '_nat']["twoFourG_WPA2-EAP_SSID"]
        security = "wpa2"
        eap_type = "TTLS"
        try:
            test_result = RunTest.Single_Client_EAP(port, sta_list, ssid_name, radio, security, eap_type, identity,
                                                    ttls_password, test_case, rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        # TC - 2.4 GHz WPA2 NAT
        test_case = test_cases["2g_wpa2_nat"]
        radio = lab_ap_info.lanforge_2dot4g
        station = [lanforge_prefix+"4325"]
        ssid_name = profile_info_dict[fw_model + '_nat']["twoFourG_WPA2_SSID"]
        ssid_psk = profile_info_dict[fw_model + '_nat']["twoFourG_WPA2_PSK"]
        security = "wpa2"
        try:
            test_result = Test.Single_Client_Connectivity(port, radio, ssid_name, ssid_psk, security, station,
                                                          test_case,
                                                          rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        # TC - 2.4 GHz WPA NAT
        test_case = test_cases["2g_wpa_nat"]
        radio = lab_ap_info.lanforge_2dot4g
        station = [lanforge_prefix+"4323"]
        ssid_name = profile_info_dict[fw_model + '_nat']["twoFourG_WPA_SSID"]
        ssid_psk = profile_info_dict[fw_model + '_nat']["twoFourG_WPA_PSK"]
        security = "wpa"
        try:
            test_result = Test.Single_Client_Connectivity(port, radio, ssid_name, ssid_psk, security, station,
                                                          test_case, rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        # TC - 5 GHz WPA2-Enterprise NAT
        test_case = test_cases["5g_eap_nat"]
        radio = lab_ap_info.lanforge_5g
        sta_list = [lanforge_prefix+"5217"]
        ssid_name = profile_info_dict[fw_model + '_nat']["fiveG_WPA2-EAP_SSID"]
        security = "wpa2"
        eap_type = "TTLS"
        try:
            test_result = RunTest.Single_Client_EAP(port, sta_list, ssid_name, radio, security, eap_type, identity,
                                                    ttls_password, test_case, rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        # TC - 5 GHz WPA2 NAT
        test_case = test_cases["5g_wpa2_nat"]
        radio = lab_ap_info.lanforge_5g
        station = [lanforge_prefix+"4326"]
        ssid_name = profile_info_dict[fw_model + '_nat']["fiveG_WPA2_SSID"]
        ssid_psk = profile_info_dict[fw_model]["fiveG_WPA2_PSK"]
        security = "wpa2"
        try:
            test_result = Test.Single_Client_Connectivity(port, radio, ssid_name, ssid_psk, security, station,
                                                          test_case,
                                                          rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        # TC - 5 GHz WPA NAT
        test_case = test_cases["5g_wpa_nat"]
        radio = lab_ap_info.lanforge_5g
        station = [lanforge_prefix+"4324"]
        ssid_name = profile_info_dict[fw_model + '_nat']["fiveG_WPA_SSID"]
        ssid_psk = profile_info_dict[fw_model]["fiveG_WPA_PSK"]
        security = "wpa"
        try:
            test_result = Test.Single_Client_Connectivity(port, radio, ssid_name, ssid_psk, security, station,
                                                          test_case,
                                                          rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        logger.info("Testing for " + fw_model + "NAT Mode SSIDs Complete")
        with open(report_path + today + '/report_data.json', 'w') as report_json_file:
            json.dump(report_data, report_json_file)

        ###########################################################################
        ################# Customer VLAN Client Connectivity #######################
        ###########################################################################

        ### Create SSID Profiles
        ssid_template = "templates/ssid_profile_template.json"

        # 5G SSIDs
        try:
            fiveG_eap = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                            prof_5g_eap_name_vlan,
                                                            profile_info_dict[fw_model + '_vlan']["fiveG_WPA2-EAP_SSID"], None,
                                                            radius_name,
                                                            "wpa2OnlyRadius", "BRIDGE", 100, ["is5GHzU", "is5GHz", "is5GHzL"])
            print("5G EAP SSID created successfully - custom VLAN mode")
            client.update_testrail(case_id=test_cases["ssid_5g_eap_vlan"], run_id=rid, status_id=1,
                                   msg='5G EAP SSID created successfully - Custom VLAN mode')
            report_data['tests'][key][test_cases["ssid_5g_eap_vlan"]] = "passed"

        except:
            fiveG_eap = "error"
            print("5G EAP SSID create failed - custom VLAN mode")
            client.update_testrail(case_id=test_cases["ssid_5g_eap_vlan"], run_id=rid, status_id=5,
                                   msg='5G EAP SSID create failed - custom VLAN mode')
            report_data['tests'][key][test_cases["ssid_5g_eap_vlan"]] = "failed"
            fiveG_eap = profile_info_dict[fw_model + '_vlan']["fiveG_WPA2-EAP_profile"]

        try:
            fiveG_wpa2 = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                             prof_5g_wpa2_name_vlan,
                                                             profile_info_dict[fw_model + '_vlan']["fiveG_WPA2_SSID"],
                                                             profile_info_dict[fw_model + '_vlan']["fiveG_WPA2_PSK"],
                                                             "Radius-Accounting-Profile", "wpa2OnlyPSK", "BRIDGE", 100,
                                                             ["is5GHzU", "is5GHz", "is5GHzL"])
            print("5G WPA2 SSID created successfully - custom VLAN mode")
            client.update_testrail(case_id=test_cases["ssid_5g_wpa2_vlan"], run_id=rid, status_id=1,
                                   msg='5G WPA2 SSID created successfully - custom VLAN mode')
            report_data['tests'][key][test_cases["ssid_5g_wpa2_vlan"]] = "passed"
        except:
            fiveG_wpa2 = "error"
            print("5G WPA2 SSID create failed - custom VLAN mode")
            client.update_testrail(case_id=test_cases["ssid_5g_wpa2_vlan"], run_id=rid, status_id=5,
                                   msg='5G WPA2 SSID create failed - custom VLAN mode')
            report_data['tests'][key][test_cases["ssid_5g_wpa2_vlan"]] = "failed"
            fiveG_wpa2 = profile_info_dict[fw_model + '_vlan']["fiveG_WPA2_profile"]

        try:
            fiveG_wpa = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                            prof_5g_wpa_name_vlan,
                                                            profile_info_dict[fw_model + '_vlan']["fiveG_WPA_SSID"],
                                                            profile_info_dict[fw_model + '_vlan']["fiveG_WPA_PSK"],
                                                            "Radius-Accounting-Profile", "wpaPSK", "BRIDGE", 100,
                                                            ["is5GHzU", "is5GHz", "is5GHzL"])
            print("5G WPA SSID created successfully - custom VLAN mode")
            client.update_testrail(case_id=test_cases["ssid_5g_wpa_vlan"], run_id=rid, status_id=1,
                                   msg='5G WPA SSID created successfully - custom VLAN mode')
            report_data['tests'][key][test_cases["ssid_5g_wpa_vlan"]] = "passed"
        except:
            fiveG_wpa = "error"
            print("5G WPA SSID create failed - custom VLAN mode")
            client.update_testrail(case_id=test_cases["ssid_5g_wpa_vlan"], run_id=rid, status_id=5,
                                   msg='5G WPA SSID create failed - custom VLAN mode')
            report_data['tests'][key][test_cases["ssid_5g_wpa_vlan"]] = "failed"
            fiveG_wpa = profile_info_dict[fw_model + '_vlan']["fiveG_WPA_profile"]

        # 2.4G SSIDs
        try:
            twoFourG_eap = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                               prof_2g_eap_name_vlan,
                                                               profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2-EAP_SSID"],
                                                               None,
                                                               radius_name, "wpa2OnlyRadius", "BRIDGE", 100, ["is2dot4GHz"])
            print("2.4G EAP SSID created successfully - custom VLAN mode")
            client.update_testrail(case_id=test_cases["ssid_2g_eap_vlan"], run_id=rid, status_id=1,
                                   msg='2.4G EAP SSID created successfully - custom VLAN mode')
            report_data['tests'][key][test_cases["ssid_2g_eap_vlan"]] = "passed"
        except:
            twoFourG_eap = "error"
            print("2.4G EAP SSID create failed - custom VLAN mode")
            client.update_testrail(case_id=test_cases["ssid_2g_eap_vlan"], run_id=rid, status_id=5,
                                   msg='2.4G EAP SSID create failed - custom VLAN mode')
            report_data['tests'][key][test_cases["ssid_2g_eap_vlan"]] = "failed"
            twoFourG_eap = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2-EAP_SSID"]

        try:
            twoFourG_wpa2 = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                                prof_2g_wpa2_name_vlan,
                                                                profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2_SSID"],
                                                                profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2_PSK"],
                                                                "Radius-Accounting-Profile", "wpa2OnlyPSK", "BRIDGE", 100,
                                                                ["is2dot4GHz"])
            print("2.4G WPA2 SSID created successfully - custom VLAN mode")
            client.update_testrail(case_id=test_cases["ssid_2g_wpa2_vlan"], run_id=rid, status_id=1,
                                   msg='2.4G WPA2 SSID created successfully - custom VLAN mode')
            report_data['tests'][key][test_cases["ssid_2g_wpa2_vlan"]] = "passed"
        except:
            twoFourG_wpa2 = "error"
            print("2.4G WPA2 SSID create failed - custom VLAN mode")
            client.update_testrail(case_id=test_cases["ssid_2g_wpa2_vlan"], run_id=rid, status_id=5,
                                   msg='2.4G WPA2 SSID create failed - custom VLAN mode')
            report_data['tests'][key][test_cases["ssid_2g_wpa2_vlan"]] = "failed"
            twoFourG_wpa2 = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2_SSID"]

        try:
            twoFourG_wpa = cloud.create_or_update_ssid_profile(cloudSDK_url, bearer, customer_id, ssid_template,
                                                               prof_2g_wpa_name_vlan,
                                                               profile_info_dict[fw_model + '_vlan']["twoFourG_WPA_SSID"],
                                                               profile_info_dict[fw_model + '_vlan']["twoFourG_WPA_PSK"],
                                                               "Radius-Accounting-Profile", "wpaPSK", "BRIDGE", 100,
                                                               ["is2dot4GHz"])
            print("2.4G WPA SSID created successfully - custom VLAN mode")
            client.update_testrail(case_id=test_cases["ssid_2g_wpa_vlan"], run_id=rid, status_id=1,
                                   msg='2.4G WPA SSID created successfully - custom VLAN mode')
            report_data['tests'][key][test_cases["ssid_2g_wpa_vlan"]] = "passed"
        except:
            twoFourG_wpa = "error"
            print("2.4G WPA SSID create failed - custom VLAN mode")
            client.update_testrail(case_id=test_cases["ssid_2g_wpa_vlan"], run_id=rid, status_id=5,
                                   msg='2.4G WPA SSID create failed - custom VLAN mode')
            report_data['tests'][key][test_cases["ssid_2g_wpa_vlan"]] = "failed"
            twoFourG_wpa = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA_SSID"]

        ### Create AP VLAN Profile
        rfProfileId = lab_ap_info.rf_profile
        child_profiles = [fiveG_eap, fiveG_wpa2, fiveG_wpa, twoFourG_eap, twoFourG_wpa2, twoFourG_wpa, rfProfileId]
        if radius_profile != None:
            child_profiles.append(radius_profile)
        print(child_profiles)
        name = "Nightly_Sanity_" + fw_model + "_" + today + "_vlan"

        try:
            create_ap_profile = cloud.create_or_update_ap_profile(cloudSDK_url, bearer, customer_id,
                                                                  command_line_args.default_ap_profile, name, child_profiles)
            test_profile_id = create_ap_profile
            print("Test Profile ID for Test is:", test_profile_id)
            client.update_testrail(case_id=test_cases["ap_vlan"], run_id=rid, status_id=1,
                                       msg='AP profile for VLAN tests created successfully')
            report_data['tests'][key][test_cases["ap_vlan"]] = "passed"
        except:
            create_ap_profile = "error"
            test_profile_id = profile_info_dict[fw_model + '_vlan']["profile_id"]
            print("Error creating AP profile for bridge tests. Will use existing AP profile")
            client.update_testrail(case_id=test_cases["ap_vlan"], run_id=rid, status_id=5,
                                       msg='AP profile for VLAN tests could not be created using API')
            report_data['tests'][key][test_cases["ap_vlan"]] = "failed"

        ### Set Proper AP Profile for VLAN SSID Tests
        ap_profile = cloud.set_ap_profile(equipment_id, test_profile_id, cloudSDK_url, bearer)

        ### Wait for Profile Push
        time.sleep(180)

        ###Check if VIF Config and VIF State reflect AP Profile from CloudSDK
        ## VIF Config
        try:
            ssid_config = profile_info_dict[fw_model + '_vlan']["ssid_list"]
            print("SSIDs in AP Profile:", ssid_config)

            ssid_list = ap_ssh.get_vif_config(command_line_args)
            print("SSIDs in AP VIF Config:", ssid_list)

            if set(ssid_list) == set(ssid_config):
                print("SSIDs in Wifi_VIF_Config Match AP Profile Config")
                client.update_testrail(case_id=test_cases["vlan_vifc"], run_id=rid, status_id=1,
                                       msg='SSIDs in VIF Config matches AP Profile Config')
                report_data['tests'][key][test_cases["vlan_vifc"]] = "passed"
            else:
                print("SSIDs in Wifi_VIF_Config do not match desired AP Profile Config")
                client.update_testrail(case_id=test_cases["vlan_vifc"], run_id=rid, status_id=5,
                                       msg='SSIDs in VIF Config do not match AP Profile Config')
                report_data['tests'][key][test_cases["vlan_vifc"]] = "failed"
        except:
            ssid_list = "ERROR"
            print("Error accessing VIF Config from AP CLI")
            client.update_testrail(case_id=test_cases["vlan_vifc"], run_id=rid, status_id=4,
                                   msg='Cannot determine VIF Config - re-test required')
            report_data['tests'][key][test_cases["vlan_vifc"]] = "error"
        # VIF State
        try:
            ssid_state = ap_ssh.get_vif_state(command_line_args)
            print("SSIDs in AP VIF State:", ssid_state)

            if set(ssid_state) == set(ssid_config):
                print("SSIDs properly applied on AP")
                client.update_testrail(case_id=test_cases["vlan_vifs"], run_id=rid, status_id=1,
                                       msg='SSIDs in VIF Config applied to VIF State')
                report_data['tests'][key][test_cases["vlan_vifs"]] = "passed"
            else:
                print("SSIDs not applied on AP")
                client.update_testrail(case_id=test_cases["vlan_vifs"], run_id=rid, status_id=5,
                                       msg='SSIDs in VIF Config not applied to VIF State')
                report_data['tests'][key][test_cases["vlan_vifs"]] = "failed"
        except:
            ssid_list = "ERROR"
            print("Error accessing VIF State from AP CLI")
            print("Error accessing VIF Config from AP CLI")
            client.update_testrail(case_id=test_cases["vlan_vifs"], run_id=rid, status_id=4,
                                   msg='Cannot determine VIF State - re-test required')
            report_data['tests'][key][test_cases["vlan_vifs"]] = "error"

        ### Set port for LANForge
        port = "vlan100"

        # Print iwinfo for logs
        iwinfo = iwinfo_status(command_line_args)
        print(iwinfo)

        ###Run Client Single Connectivity Test Cases for VLAN SSIDs
        # TC- 2.4 GHz WPA2-Enterprise VLAN
        test_case = test_cases["2g_eap_vlan"]
        radio = lab_ap_info.lanforge_2dot4g
        sta_list = [lanforge_prefix+"5253"]
        ssid_name = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2-EAP_SSID"]
        security = "wpa2"
        eap_type = "TTLS"
        try:
            test_result = RunTest.Single_Client_EAP(port, sta_list, ssid_name, radio, security, eap_type, identity,
                                                    ttls_password, test_case, rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        # TC - 2.4 GHz WPA2 VLAN
        test_case = test_cases["2g_wpa2_vlan"]
        radio = lab_ap_info.lanforge_2dot4g
        station = [lanforge_prefix+"5251"]
        ssid_name = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2_SSID"]
        ssid_psk = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA2_PSK"]
        security = "wpa2"
        try:
            test_result = Test.Single_Client_Connectivity(port, radio, ssid_name, ssid_psk, security, station,
                                                          test_case,
                                                          rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        # TC 4323 - 2.4 GHz WPA VLAN
        test_case = test_cases["2g_wpa_vlan"]
        radio = lab_ap_info.lanforge_2dot4g
        station = [lanforge_prefix+"5252"]
        ssid_name = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA_SSID"]
        ssid_psk = profile_info_dict[fw_model + '_vlan']["twoFourG_WPA_PSK"]
        security = "wpa"
        try:
            test_result = Test.Single_Client_Connectivity(port, radio, ssid_name, ssid_psk, security, station,
                                                          test_case, rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        # TC - 5 GHz WPA2-Enterprise VLAN
        test_case = test_cases["5g_eap_vlan"]
        radio = lab_ap_info.lanforge_5g
        sta_list = [lanforge_prefix+"5250"]
        ssid_name = profile_info_dict[fw_model + '_vlan']["fiveG_WPA2-EAP_SSID"]
        security = "wpa2"
        eap_type = "TTLS"
        try:
            test_result = RunTest.Single_Client_EAP(port, sta_list, ssid_name, radio, security, eap_type, identity,
                                                    ttls_password, test_case, rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        # TC - 5 GHz WPA2 VLAN
        test_case = test_cases["5g_wpa2_vlan"]
        radio = lab_ap_info.lanforge_5g
        station = [lanforge_prefix+"5248"]
        ssid_name = profile_info_dict[fw_model + '_vlan']["fiveG_WPA2_SSID"]
        ssid_psk = profile_info_dict[fw_model]["fiveG_WPA2_PSK"]
        security = "wpa2"
        try:
            test_result = Test.Single_Client_Connectivity(port, radio, ssid_name, ssid_psk, security, station,
                                                          test_case,
                                                          rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        # TC 4324 - 5 GHz WPA VLAN
        test_case = test_cases["5g_wpa_vlan"]
        radio = lab_ap_info.lanforge_5g
        station = [lanforge_prefix+"5249"]
        ssid_name = profile_info_dict[fw_model + '_vlan']["fiveG_WPA_SSID"]
        ssid_psk = profile_info_dict[fw_model]["fiveG_WPA_PSK"]
        security = "wpa"
        try:
            test_result = Test.Single_Client_Connectivity(port, radio, ssid_name, ssid_psk, security, station,
                                                          test_case,
                                                          rid)
        except:
            test_result = "error"
            Test.testrail_retest(test_case, rid, ssid_name)
            pass
        report_data['tests'][key][int(test_case)] = test_result
        print(report_data['tests'][key])

        time.sleep(10)

        logger.info("Testing for " + fw_model + "Custom VLAN SSIDs Complete")

        logger.info("Testing for " + fw_model + "Complete")

        # Add indication of complete TC pass/fail to sanity_status for pass to external json used by Throughput Test
        x = all(status == "passed" for status in report_data["tests"][key].values())
        print(x)

        if x == True:
            sanity_status['sanity_status'][key] = "passed"

        else:
            sanity_status['sanity_status'][key] = "failed"

        ##Update sanity_status.json to indicate there has been a test on at least one AP model tonight
        sanity_status['sanity_run']['new_data'] = "yes"

        print(sanity_status)

        # write to json file
        with open('sanity_status.json', 'w') as json_file:
            json.dump(sanity_status, json_file)

        # write to report_data contents to json file so it has something in case of unexpected fail
        print(report_data)
        with open(report_path + today + '/report_data.json', 'w') as report_json_file:
            json.dump(report_data, report_json_file)

# Dump all sanity test results to external json file again just to be sure
with open('sanity_status.json', 'w') as json_file:
    json.dump(sanity_status, json_file)

# Calculate percent of tests passed for report
for key in ap_models:
    if report_data['fw_available'][key] == "No":
        report_data["pass_percent"][key] = "Not Run"
    else:
        no_of_tests = len(report_data["tests"][key])
        passed_tests = sum(x == "passed" for x in report_data["tests"][key].values())
        print(passed_tests)
        percent = float(passed_tests / no_of_tests) * 100
        percent_pass = round(percent, 2)
        print(key, "pass rate is", str(percent_pass) + "%")
        report_data["pass_percent"][key] = str(percent_pass) + '%'

# write to report_data contents to json file
print(report_data)
with open(report_path + today + '/report_data.json', 'w') as report_json_file:
    json.dump(report_data, report_json_file)

print(".....End of Sanity Test.....")
logger.info("End of Sanity Test run")
