#########################################################################################################
# Used by Nightly_Sanity
# This has different types of old_pytest like Single client connectivity, Single_Client_EAP, testrail_retest
#########################################################################################################
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)
if "libs" not in sys.path:
    sys.path.append(f'../libs')
for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../../lanforge/lanforge-scripts/{folder}')

sys.path.append(f"../lanforge/lanforge-scripts/py-scripts/tip-cicd-sanity")

sys.path.append(f'../libs')
sys.path.append(f'../libs/lanforge/')
from sta_connect2 import StaConnect2
import time
# from eap_connect import EAPConnect
from test_ipv4_ttls import TTLSTest


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
        self.debug = debug
        self.staConnect = StaConnect2(self.lanforge_ip, self.lanforge_port, debug_=debug)
        print(lanforge_data)

    def Client_Connectivity(self, ssid="[BLANK]", passkey="[BLANK]", security="open", extra_securities=[], station_name=[],
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
        self.staConnect.setup(extra_securities=extra_securities)
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

    def EAP_Connect(self, ssid="[BLANK]", passkey="[BLANK]", security="wpa2", extra_securities=[],
                    mode="BRIDGE", band="twog", vlan_id=100,
                    station_name=[], key_mgmt="WPA-EAP",
                    pairwise="NA", group="NA", wpa_psk="DEFAULT",
                    ttls_passwd="nolastart",
                    wep_key="NA", ca_cert="NA", eap="TTLS", identity="nolaradius"):
        self.eap_connect = TTLSTest(host=self.lanforge_ip, port=self.lanforge_port,
                                    sta_list=station_name, vap=False, _debug_on=self.debug)

        self.eap_connect.station_profile.sta_mode = 0
        self.eap_connect.upstream_resource = 1
        if mode == "BRIDGE":
            self.eap_connect.l3_cx_obj_udp.upstream = self.upstream_port
            self.eap_connect.l3_cx_obj_tcp.upstream = self.upstream_port
        elif mode == "NAT":
            self.eap_connect.l3_cx_obj_udp.upstream = self.upstream_port
            self.eap_connect.l3_cx_obj_tcp.upstream = self.upstream_port
        else:
            self.eap_connect.l3_cx_obj_udp.upstream = self.upstream_port + "." + str(vlan_id)
            self.eap_connect.l3_cx_obj_tcp.upstream = self.upstream_port + "." + str(vlan_id)
        if band == "twog":
            self.eap_connect.radio = self.twog_radios[0]
            # self.eap_connect.sta_prefix = self.twog_prefix
        if band == "fiveg":
            self.eap_connect.radio = self.fiveg_radios[0]
            # self.eap_connect.sta_prefix = self.fiveg_prefix
        # self.eap_connect.resource = 1
        if eap == "TTLS":
            self.eap_connect.ieee80211w = 0
            self.eap_connect.station_profile.set_command_flag("add_sta", "80211u_enable", 0)
            self.eap_connect.identity = identity
            self.eap_connect.ttls_passwd = ttls_passwd
        if eap == "TLS":
            self.eap_connect.key_mgmt = "WPA-EAP-SUITE-B"
            self.eap_connect.station_profile.set_command_flag("add_sta", "80211u_enable", 0)
            self.eap_connect.pairwise = "TKIP"
            self.eap_connect.group = "TKIP"
            self.eap_connect.eap = "EAP-TLS"

        # self.eap_connect.hs20_enable = False
        self.eap_connect.ssid = ssid
        self.eap_connect.password = passkey
        self.eap_connect.security = security
        self.eap_connect.sta_list = station_name
        self.eap_connect.build(extra_securities=extra_securities)
        self.eap_connect.start(station_name, True, True)
        self.eap_connect.stop()
        self.eap_connect.cleanup(station_name)
        return self.eap_connect.passes()


if __name__ == '__main__':
    lanforge_data = {
        "ip": "192.168.200.81",
        "port": 8080,
        "2.4G-Radio": ["wiphy0"],
        "5G-Radio": ["wiphy1"],
        "AX-Radio": ["wiphy2"],
        "upstream": "eth1",
        "2.4G-Station-Name": "wlan0",
        "5G-Station-Name": "wlan0",
        "AX-Station-Name": "ax",
    }
    obj = RunTest(lanforge_data=lanforge_data, debug=False)
    # print(obj.eap_connect.json_get("port/1/1/sta0000?fields=ap,ip"))
    obj.EAP_Connect(station_name=["sta0000", "sta0001"], eap="TTLS", ssid="testing_radius")
