#########################################################################################################
# Used by Nightly_Sanity
# This has different types of old_pytest like Single client connectivity, Single_Client_EAP, testrail_retest
#########################################################################################################

from sta_connect2 import StaConnect2


class RunTest:

    def __init__(self, lanforge_ip, lanforge_port, lanforge_prefix):
        self.lanforge_ip = lanforge_ip
        self.lanforge_port = lanforge_port
        self.lanforge_prefix = lanforge_prefix

    def Single_Client_Connectivity(self, upstream_port="eth1", radio="wiphy0", ssid="TestAP", passkey="ssid_psk",
                                   security="open",
                                   station_name="sta0000", test_case=None, rid=None, client=None, logger=None):
        '''SINGLE CLIENT CONNECTIVITY using test_connect2.py'''
        self.staConnect = StaConnect2(self.lanforge_ip, self.lanforge_port, debug_=False)
        self.staConnect.sta_mode = 0
        self.staConnect.upstream_resource = 1
        self.staConnect.upstream_port = upstream_port
        self.staConnect.radio = radio
        self.staConnect.resource = 1
        self.staConnect.dut_ssid = ssid
        self.staConnect.dut_passwd = passkey
        self.staConnect.dut_security = security
        self.staConnect.station_names = station_name
        self.staConnect.sta_prefix = self.lanforge_prefix
        self.staConnect.runtime_secs = 10
        self.staConnect.bringup_time_sec = 60
        self.staConnect.cleanup_on_exit = True
        # staConnect.cleanup()
        self.staConnect.setup()
        self.staConnect.start()
        print("napping %f sec" % self.staConnect.runtime_secs)
        time.sleep(self.staConnect.runtime_secs)
        self.staConnect.stop()
        self.staConnect.cleanup()
        run_results = self.staConnect.get_result_list()
        for result in run_results:
            print("test result: " + result)
        # result = 'pass'
        print("Single Client Connectivity :", self.staConnect.passes)
        if self.staConnect.passes() == True:
            print("Single client connection to", self.staConnect.dut_ssid, "successful. Test Passed")
            client.update_testrail(case_id=test_case, run_id=rid, status_id=1, msg='Client connectivity passed')
            logger.info("Client connectivity to " + self.staConnect.dut_ssid + " Passed")
            return ("passed")
        else:
            client.update_testrail(case_id=test_case, run_id=rid, status_id=5, msg='Client connectivity failed')
            print("Single client connection to", self.staConnect.dut_ssid, "unsuccessful. Test Failed")
            logger.warning("Client connectivity to " + self.staConnect.dut_ssid + " FAILED")
            return ("failed")

    def Single_Client_EAP(self, port, sta_list, ssid_name, radio, security, eap_type,
                          identity, ttls_password, test_case, rid, client, logger):
        eap_connect = EAPConnect(self.lanforge_ip, self.lanforge_port, _debug_on=False)
        eap_connect.upstream_resource = 1
        eap_connect.upstream_port = port
        eap_connect.security = security
        eap_connect.sta_list = sta_list
        eap_connect.station_names = sta_list
        eap_connect.sta_prefix = self.lanforge_prefix
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

    def testrail_retest(self, test_case, rid, ssid_name, client, logger):
        client.update_testrail(case_id=test_case, run_id=rid, status_id=4,
                               msg='Error in Client Connectivity Test. Needs to be Re-run')
        print("Error in test for single client connection to", ssid_name)
        logger.warning("ERROR testing Client connectivity to " + ssid_name)
