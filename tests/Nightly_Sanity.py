#!/usr/bin/python3

import sys

if "libs" not in sys.path:
    sys.path.append("../libs")

from UnitTestBase import *


class NightlySanity:

    def __init__(self, args=None, base=None, lanforge_data=None, Test=None, reporting=None ):

        self.args = args
        self.model = self.args.model
        self.client: TestRail_Client = TestRail_Client(args)
        self.logger = base.logger
        ###Get Cloud Bearer Token
        self.cloud: CloudSDK = CloudSDK(args)
        cloud_type = "v1"
        self.bearer = self.cloud.get_bearer(args.sdk_base_url, cloud_type)
        self.customer_id = "2"
        self.Test = Test
        self.reporting = reporting
        self.lanforge_data = lanforge_data
        if lanforge_data is None:
            exit()
        self.cloud_sdk_models = {
            "ec420": "EC420-G1",
            "ea8300": "EA8300-CA",
            "ecw5211": "ECW5211",
            "ecw5410": "ECW5410",
            "wf188n": "WF188N"
        }

        self.equipment_id = self.args.equipment_id

        self.report_data = dict()

        if self.equipment_id == "-1":
            eq_id = ap_ssh_ovsh_nodec(args, 'id')
            print("EQ Id: %s" % (eq_id))

            # Now, query equipment to find something that matches.
            eq = self.cloud.get_customer_equipment(args.sdk_base_url, self.bearer, self.customer_id)
            for item in eq:
                for e in item['items']:
                    print(e['id'], "  ", e['inventoryId'])
                    if e['inventoryId'].endswith("_%s" % (eq_id)):
                        print("Found equipment ID: %s  inventoryId: %s",
                              e['id'], e['inventoryId'])
                        self.equipment_id = str(e['id'])
        if self.equipment_id == -1:
            print("ERROR:  Could not find equipment-id.")
            exit()


    def setup(self):
        pass

    def create_test_run_session(self):
        today = str(date.today())
        case_ids = list(test_cases.values())
        projId = self.client.get_project_id(project_name=self.args.testrail_project)
        test_run_name = self.args.testrail_run_prefix + self.model + "_" + today + "_" + self.firmware["latest"]
        self.client.create_testrun(name=test_run_name, case_ids=case_ids, project_id=projId,
                                   milestone_id=self.args.milestone,
                                   description="Automated Nightly Sanity test run for new firmware build")
        self.rid = self.client.get_run_id(
            test_run_name=self.args.testrail_run_prefix + self.model + "_" + today + "_" + self.firmware["latest"])
        print("TIP run ID is:", self.rid)

    def start_test(self, do_upgrade=False):

        # Upgrade the Firmware on AP
        if do_upgrade:

            cloudModel = self.cloud_sdk_models[self.args.model]
            pf = self.cloud.do_upgrade_ap_fw(self.bearer, self.args, self.report_data, test_cases, self.client,
                                             self.firmware["latest"], cloudModel, self.args.model,
                                             self.args.jfrog_user_id, self.args.jfrog_user_password, self.rid,
                                             self.customer_id, self.equipment_id, self.logger)
            print(self.report_data)
            if not pf:
                exit()
        if True:
            ###Check AP Manager Status
            manager_status = self.ap_cli_info['state']
            print(manager_status)

            if manager_status != "active":
                print("Manager status is " + manager_status + "! Not connected to the cloud.")
                print("Waiting 30 seconds and re-checking status")
                time.sleep(30)
                ap_cli_info = ssh_cli_active_fw(self.args)
                manager_status = ap_cli_info['state']
                if manager_status != "active":
                    print("Manager status is", manager_status, "! Not connected to the cloud.")
                    print("Manager status fails multiple checks - failing test case.")
                    ##fail cloud connectivity testcase
                    self.client.update_testrail(case_id=self.test_cases["cloud_connection"], run_id=self.rid,
                                                status_id=5,
                                                msg='CloudSDK connectivity failed')
                    self.report_data['tests'][self.model][test_cases["cloud_connection"]] = "failed"
                    print(self.report_data['tests'][self.model])

                else:
                    print("Manager status is Active. Proceeding to connectivity testing!")
                    # TC522 pass in Testrail
                    self.client.update_testrail(case_id=test_cases["cloud_connection"], run_id=self.rid, status_id=1,
                                                msg='Manager status is Active')
                    self.report_data['tests'][self.model][test_cases["cloud_connection"]] = "passed"
                    print(self.report_data['tests'][self.model])
            else:
                print("Manager status is Active. Proceeding to connectivity testing!")
                # TC5222 pass in testrail
                self.client.update_testrail(case_id=test_cases["cloud_connection"], run_id=self.rid, status_id=1,
                                            msg='Manager status is Active')
                self.report_data['tests'][self.model][test_cases["cloud_connection"]] = "passed"
                print(self.report_data['tests'][self.model])
                # Pass cloud connectivity test case

            # Update in reporting
            self.reporting.update_json_report(self.report_data)

            self.ap_object = CreateAPProfiles(self.args, cloud=self.cloud, client=self.client, fw_model=self.model)

            # Logic to create AP Profiles (Bridge Mode)
            self.ap_object.set_ssid_psk_data\
                (ssid_2g_wpa="Nightly-SSID-2G-WPA",
                 ssid_5g_wpa="Nightly-SSID-5G-WPA",
                 psk_2g_wpa= "Nightly_2g_wpa",
                 psk_5g_wpa="Nightly_5g_wpa",
                 ssid_2g_wpa2="Nightly-SSID-2G-WPA2",
                 ssid_5g_wpa2="Nightly-SSID-5G-WPA2",
                 psk_2g_wpa2="Nightly_2g_wpa2",
                 psk_5g_wpa2="Nightly_5g_wpa2")

            print("creating Profiles")
            ssid_template = "TipWlan-Cloud-Wifi"

            if not self.args.skip_profiles:
                if not self.args.skip_radius:
                    # Radius Profile needs to be set here
                    # obj.create_radius_profile(radius_name, rid, key)
                    pass
                self.ap_object.create_ssid_profiles(ssid_template=ssid_template, skip_eap=True)

            print("Create AP with equipment-id: ", self.equipment_id)
            self.ap_object.create_ap_bridge_profile(eq_id=self.equipment_id, fw_model=self.model)
            self.ap_object.validate_changes()

            print("Profiles Created")

            self.test_bridge_mode_2g()
            self.test_bridge_mode_5g()
            # Logic to check Single client Connectivity for EAP

            # Logic to check Single client Connectivity for WPA

            # Logic to check Single client Connectivity for WPA2


            # Logic to create AP Profiles (NAT Mode)
            self.ap_object.set_ssid_psk_data\
                (ssid_2g_wpa="Nightly-SSID-NAT-2G-WPA",
                 ssid_5g_wpa="Nightly-SSID-NAT-5G-WPA",
                 psk_2g_wpa= "Nightly_2g_nat_wpa",
                 psk_5g_wpa="Nightly_5g_nat_wpa",
                 ssid_2g_wpa2="Nightly-SSID-NAT-2G-WPA2",
                 ssid_5g_wpa2="Nightly-SSID-NAT-5G-WPA2",
                 psk_2g_wpa2="Nightly_2g_nat_wpa2",
                 psk_5g_wpa2="Nightly_5g_nat_wpa2")

            print("creating Profiles")
            ssid_template = "TipWlan-Cloud-Wifi"

            if not self.args.skip_profiles:
                if not self.args.skip_radius:
                    # Radius Profile needs to be set here
                    # obj.create_radius_profile(radius_name, rid, key)
                    pass
                self.ap_object.create_ssid_profiles(ssid_template=ssid_template, skip_eap=True)

            print("Create AP with equipment-id: ", self.equipment_id)
            self.ap_object.create_ap_bridge_profile(eq_id=self.equipment_id, fw_model=self.model)
            self.ap_object.validate_changes()




    def setup_report(self):

        self.report_data["cloud_sdk"] = dict.fromkeys(ap_models, "")
        for key in self.report_data["cloud_sdk"]:
            self.report_data["cloud_sdk"][key] = {
                "date": "N/A",
                "commitId": "N/A",
                "projectVersion": "N/A"
            }
        self.report_data["fw_available"] = dict.fromkeys(ap_models, "Unknown")
        self.report_data["fw_under_test"] = dict.fromkeys(ap_models, "N/A")
        self.report_data['pass_percent'] = dict.fromkeys(ap_models, "")

        self.report_data['tests'] = dict.fromkeys(ap_models, "")
        for key in ap_models:
            self.report_data['tests'][key] = dict.fromkeys(test_cases.values(), "not run")

        print(self.report_data)

        self.reporting.update_json_report(report_data=self.report_data)

    def check_fw(self, jfrog=None):

        # This can be kept as a global dictionary
        ap_latest_dict = {
            "ec420": "Unknown",
            "ea8300": "Unknown",
            "ecw5211": "unknown",
            "ecw5410": "unknown"
        }
        self.ap_latest_dict = check_latest_fw(jfrog=jfrog,
                                              ap_latest_dict=ap_latest_dict,
                                              buildid=self.args.build_id)

        try:
            self.ap_cli_info = get_ap_info(self.args)
            self.ap_current_fw = self.ap_cli_info['active_fw']
        except Exception as ex:
            print(ex)
            self.ap_current_fw = None
            logging.error(logging.traceback.format_exc())
            ap_cli_info = "ERROR"
            print("Cannot Reach AP CLI, will not test this variant");
        self.firmware = {
            "latest": self.ap_latest_dict[self.args.model],
            "current": self.ap_current_fw
        }
        return self.firmware

    # lanforge = {
    #     "ip": command_line_args.lanforge_ip_address,
    #     "port": command_line_args.lanforge_port_number,
    #     "prefix": command_line_args.lanforge_prefix,
    #     "2g_radio": command_line_args.lanforge_2g_radio,
    #     "5g_radio": command_line_args.lanforge_5g_radio
    # }

    # dev complete
    def test_bridge_mode_2g(self):

        if not self.args.skip_radius:
            ###Run Client Single Connectivity Test Cases for Bridge SSIDs
            # TC5214 - 2.4 GHz WPA2-Enterprise
            test_case = test_cases["2g_eap_bridge"]
            radio = lanforge_2g_radio
            sta_list = [lanforge_prefix + "5214"]
            ssid_name = ssid_2g_eap;
            security = "wpa2"
            eap_type = "TTLS"
            try:
                test_result = self.Test.Single_Client_EAP(port, sta_list, ssid_name, radio, security, eap_type,
                                                     identity, ttls_password, test_case, rid, client, logger)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, ssid_name, client, logger)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            print(report_data['tests'][key])

            time.sleep(10)

        ###Run Client Single Connectivity Test Cases for Bridge SSIDs
        # TC - 2.4 GHz WPA2
        test_case = test_cases["2g_wpa2_bridge"]
        station = [self.lanforge_data['prefix'] + "2237"]
        ssid_name = self.ap_object.ssid_data['2g']['wpa2']['name']
        ssid_psk = self.ap_object.psk_data['2g']['wpa2']['name']
        security = "wpa2"
        upstream_port = "eth2"
        print(self.lanforge_data['port'])


        try:
            test_result = self.Test.Single_Client_Connectivity(upstream_port=upstream_port,
                                                               radio=self.lanforge_data['2g_radio'],
                                                               ssid=ssid_name,
                                                               passkey=ssid_psk,
                                                               security=security,
                                                               station_name=station, test_case=test_case, rid=self.rid, client=self.client, logger=self.logger)
        except:
            test_result = "error"
            self.Test.testrail_retest(test_case, self.rid, ssid_name, self.client, self.logger)
            pass
        self.report_data['tests'][self.model][int(test_case)] = test_result
        print(self.report_data['tests'][self.model])

        time.sleep(10)

        # TC - 2.4 GHz WPA
        test_case = test_cases["2g_wpa_bridge"]
        station = [self.lanforge_data['prefix'] + "2420"]
        ssid_name = self.ap_object.ssid_data['2g']['wpa']['name']
        ssid_psk = self.ap_object.psk_data['2g']['wpa']['name']
        security = "wpa"
        upstream_port = "eth2"
        print(self.lanforge_data['port'])
        try:
            test_result = self.Test.Single_Client_Connectivity(upstream_port=upstream_port,
                                                               radio=self.lanforge_data['2g_radio'],
                                                               ssid=ssid_name,
                                                               passkey=ssid_psk,
                                                               security=security,
                                                               station_name=station, test_case=test_case, rid=self.rid,
                                                               client=self.client, logger=self.logger)
        except:
            test_result = "error"
            self.Test.testrail_retest(test_case, self.rid, ssid_name, self.client, self.logger)
            pass
        self.report_data['tests'][self.model][int(test_case)] = test_result
        print(self.report_data['tests'][self.model])

        time.sleep(10)

    # dev complete
    def test_bridge_mode_5g(self):

        if not self.args.skip_radius:
            # TC - 5 GHz WPA2-Enterprise
            test_case = self.test_cases["5g_eap_bridge"]
            radio = lanforge_5g_radio
            sta_list = [lanforge_prefix+"5215"]
            ssid_name = ssid_5g_eap
            security = "wpa2"
            eap_type = "TTLS"
            try:
                test_result = Test.Single_Client_EAP(port, sta_list, ssid_name, radio, security, eap_type,
                          identity, ttls_password, test_case, rid, client, logger)
            except:
                test_result = "error"
                Test.testrail_retest(test_case, rid, ssid_name, client, logger)
                pass
            report_data['tests'][key][int(test_case)] = test_result
            print(report_data['tests'][key])

            time.sleep(10)

        # TC 5 GHz WPA2
        test_case = test_cases["5g_wpa2_bridge"]
        station = [self.lanforge_data['prefix'] + "2236"]
        ssid_name = self.ap_object.ssid_data['5g']['wpa2']['name']
        ssid_psk = self.ap_object.psk_data['5g']['wpa2']['name']
        security = "wpa2"
        upstream_port = "eth2"
        try:
            test_result = self.Test.Single_Client_Connectivity(upstream_port=upstream_port,
                                                               radio=self.lanforge_data['5g_radio'],
                                                               ssid=ssid_name,
                                                               passkey=ssid_psk,
                                                               security=security,
                                                               station_name=station, test_case=test_case, rid=self.rid,
                                                               client=self.client, logger=self.logger)
        except:
            test_result = "error"
            self.Test.testrail_retest(test_case, self.rid, ssid_name, self.client, self.logger)
            pass
        self.report_data['tests'][self.model][int(test_case)] = test_result
        print(self.report_data['tests'][self.model])

        time.sleep(10)

        # # TC - 5 GHz WPA
        test_case = test_cases["5g_wpa_bridge"]
        station = [self.lanforge_data['prefix']+"2419"]
        ssid_name = self.ap_object.ssid_data['5g']['wpa']['name']
        ssid_psk = self.ap_object.psk_data['5g']['wpa']['name']
        security = "wpa"
        upstream_port = "eth2"
        try:
            test_result = self.Test.Single_Client_Connectivity(upstream_port=upstream_port,
                                                               radio=self.lanforge_data['5g_radio'],
                                                               ssid=ssid_name,
                                                               passkey=ssid_psk,
                                                               security=security,
                                                               station_name=station, test_case=test_case, rid=self.rid,
                                                               client=self.client, logger=self.logger)
        except:
            test_result = "error"
            self.Test.testrail_retest(test_case, self.rid, ssid_name, self.client, self.logger)
            pass
        self.report_data['tests'][self.model][int(test_case)] = test_result
        print(self.report_data['tests'][self.model])

        time.sleep(10)

        pass



    def test_nat_mode(self):
        pass

    def test_vlan_mode(self):
        pass



def main():
    parser = argparse.ArgumentParser(description="Nightly Combined Tests", add_help=False)
    parser.add_argument("--default_ap_profile", type=str,
                        help="Default AP profile to use as basis for creating new ones, typically: TipWlan-2-Radios or TipWlan-3-Radios",
                        required=True)
    parser.add_argument("--skip_radius", dest="skip_radius", action='store_true',
                        help="Should we skip the RADIUS configs or not")
    parser.add_argument("--skip_profiles", dest="skip_profiles", action='store_true',
                        help="Should we skip applying profiles?")
    parser.add_argument("--skip_wpa", dest="skip_wpa", action='store_false',
                        help="Should we skip applying profiles?")
    parser.add_argument("--skip_wpa2", dest="skip_wpa2", action='store_false',
                        help="Should we skip applying profiles?")
    parser.add_argument("--skip_eap", dest="skip_eap", action='store_false',
                        help="Should we skip applying profiles?")

    reporting = Reporting(reports_root=os.getcwd() + "/reports/")
    base = UnitTestBase("query-sdk", parser, reporting)
    command_line_args = base.command_line_args

    # cmd line takes precedence over env-vars.
    cloudSDK_url = command_line_args.sdk_base_url  # was os.getenv('CLOUD_SDK_URL')
    local_dir = command_line_args.local_dir  # was os.getenv('SANITY_LOG_DIR')
    report_path = command_line_args.report_path  # was os.getenv('SANITY_REPORT_DIR')
    report_template = command_line_args.report_template  # was os.getenv('REPORT_TEMPLATE')

    ## TestRail Information
    tr_user = command_line_args.testrail_user_id  # was os.getenv('TR_USER')
    tr_pw = command_line_args.testrail_user_password  # was os.getenv('TR_PWD')
    milestoneId = command_line_args.milestone  # was os.getenv('MILESTONE')
    projectId = command_line_args.testrail_project  # was os.getenv('PROJECT_ID')
    testRunPrefix = command_line_args.testrail_run_prefix  # os.getenv('TEST_RUN_PREFIX')

    ##Jfrog credentials
    jfrog = {
        "user": command_line_args.jfrog_user_id,  # was os.getenv('JFROG_USER')
        "pass": command_line_args.jfrog_user_password  # was os.getenv('JFROG_PWD')
    }

    ##EAP Credentials
    eap_cred = {
        "identity": command_line_args.eap_id,
        "ttls_password": command_line_args.ttls_password
    }

    ## AP Credentials
    ap_cred = {
        "username": command_line_args.ap_username
    }

    ##LANForge Information
    lanforge = {
        "ip": command_line_args.lanforge_ip_address,
        "port": command_line_args.lanforge_port_number,
        "prefix": command_line_args.lanforge_prefix,
        "2g_radio": command_line_args.lanforge_2g_radio,
        "5g_radio": command_line_args.lanforge_5g_radio
    }

    build = command_line_args.build_id

    logger = base.logger
    hdlr = base.hdlr

    if command_line_args.testbed == None:
        print("ERROR:  Must specify --testbed argument for this test.")
        sys.exit(1)

    print("Start of Sanity Testing...")
    print("Testing Latest Build with Tag: " + build)
    if command_line_args.skip_upgrade == True:
        print("Will skip upgrading AP firmware...")

    ######Testrail Project and Run ID Information ##############################

    Test = RunTest(lanforge_ip=lanforge["ip"], lanforge_port=lanforge["port"], lanforge_prefix=lanforge["prefix"])

    # sanity_status = json.load(open("sanity_status.json"))
    obj = NightlySanity(args=command_line_args, base=base, lanforge_data=lanforge, Test=Test, reporting=reporting)

    projId = obj.client.get_project_id(project_name=projectId)
    print("TIP WLAN Project ID is:", projId)
    logger.info('Start of Nightly Sanity')

    # get latest revision
    firmware = obj.check_fw(jfrog=jfrog)
    report_data = dict()

    # Check is current fw is there else will skip this variant test
    if (firmware["current"] is not None) and firmware["latest"] != firmware["current"]:
        do_upgrade = obj.cloud.should_upgrade_ap_fw(obj.bearer, obj.args, report_data, firmware["latest"],
                                                    command_line_args.model,
                                                    firmware["current"], logger)

    elif (firmware["current"] is not None) and firmware["latest"] == firmware["current"]:
        do_upgrade = False
        print("AP ia already having Latest Firmware...")

    else:
        print("Skipping this Profile")
        exit()

    # exit()
    # Test till here to verify all connectivity with cloud and ap and fe upgrade logics

    # Create session for Test
    obj.create_test_run_session()

    # Setup Reporting
    obj.setup_report()

    # Start Test
    obj.start_test(do_upgrade=do_upgrade)


if __name__ == "__main__":
    main()
