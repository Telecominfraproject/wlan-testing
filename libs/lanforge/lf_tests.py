#########################################################################################################
# Used by Nightly_Sanity
# This has different types of old_pytest like Single client connectivity, Single_Client_EAP, testrail_retest
#########################################################################################################

from sta_connect2 import StaConnect2
import time
from eap_connect import EAPConnect


class RunTest:

    def __init__(self, lanforge_data=None, debug=False):
        self.lanforge_ip = lanforge_data["ip"]
        self.lanforge_port = lanforge_data["port"]
        self.twog_radios = lanforge_data["2.4G-Radio"]
        self.fiveg_radios = lanforge_data["5G-Radio"]
        self.ax_radios = lanforge_data["AX-Radio"]
        self.upstream_port = lanforge_data["upstream"]
        self.twog_prefix = lanforge_data["2.4G-Station-Name"]
        self.fiveg_prefix = lanforge_data["5G-Station-Name"]
        self.ax_prefix = lanforge_data["AX-Station-Name"]
        self.staConnect = StaConnect2(self.lanforge_ip, self.lanforge_port, debug_=debug)

    def Client_Connectivity(self, ssid="[BLANK]", passkey="[BLANK]", security="open", station_name=[],
                                   mode="BRIDGE", vlan_id=1, band="twog"):
        '''SINGLE CLIENT CONNECTIVITY using test_connect2.py'''
        self.staConnect.sta_mode = 0
        self.staConnect.upstream_resource = 1
        if mode == "BRIDGE":
            self.staConnect.upstream_port = self.upstream_port
        elif mode == "NAT":
            self.staConnect.upstream_port = self.upstream_port
        else:
            self.staConnect.upstream_port = self.upstream_port + "." + str(vlan_id)
        if band == "twog":
            self.staConnect.radio = self.twog_radios[0]
            self.staConnect.sta_prefix = self.twog_prefix
        if band == "fiveg":
            self.staConnect.radio = self.fiveg_radios[0]
            self.staConnect.sta_prefix = self.fiveg_prefix
        self.staConnect.resource = 1
        self.staConnect.dut_ssid = ssid
        self.staConnect.dut_passwd = passkey
        self.staConnect.dut_security = security
        self.staConnect.station_names = station_name
        self.staConnect.runtime_secs = 40
        self.staConnect.bringup_time_sec = 60
        self.staConnect.cleanup_on_exit = True
        # self.staConnect.cleanup()
        self.staConnect.setup()
        self.staConnect.start()
        print("napping %f sec" % self.staConnect.runtime_secs)
        time.sleep(self.staConnect.runtime_secs)
        self.staConnect.stop()
        self.staConnect.cleanup()
        run_results = self.staConnect.get_result_list()
        for result in run_results:
            print("test result: " + result)
        result = True
        print("Client Connectivity :", self.staConnect.passes)
        if self.staConnect.passes():
            print("client connection to", self.staConnect.dut_ssid, "successful. Test Passed")
        else:
            print("client connection to", self.staConnect.dut_ssid, "unsuccessful. Test Failed")
            result = False
        time.sleep(3)
        return self.staConnect.passes(), result

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
        eap_connect.runtime_secs = 40
        eap_connect.setup()
        eap_connect.start()
        print("napping %f sec" % eap_connect.runtime_secs)
        time.sleep(eap_connect.runtime_secs)
        eap_connect.stop()
        eap_connect.cleanup()
        run_results = eap_connect.get_result_list()
        for result in run_results:
            print("test result: " + result)
        result = True
        print("Single Client Connectivity :", eap_connect.passes)
        if eap_connect.passes():
            print("Single client connection to", ssid_name, "successful. Test Passed")
        else:
            print("Single client connection to", ssid_name, "unsuccessful. Test Failed")
            result = False
        return self.staConnect.passes(), result
