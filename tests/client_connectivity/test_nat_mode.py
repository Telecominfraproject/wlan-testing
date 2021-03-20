import pytest
import sys

for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../lanforge/lanforge-scripts/{folder}')

sys.path.append(f'../libs')
sys.path.append(f'../libs/lanforge/')

from LANforge.LFUtils import *

if 'py-json' not in sys.path:
    sys.path.append('../py-scripts')

import sta_connect2
from sta_connect2 import StaConnect2
import eap_connect
from eap_connect import EAPConnect
import time



@pytest.mark.usefixtures('setup_cloudsdk')
@pytest.mark.usefixtures('upgrade_firmware')
class TestNATModeClientConnectivity(object):

    @pytest.mark.sanity
    @pytest.mark.nat
    @pytest.mark.open
    @pytest.mark.wpa
    @pytest.mark.wpa2
    @pytest.mark.eap
    def test_single_client(self, setup_cloudsdk, upgrade_firmware, setup_nat_mode, disconnect_cloudsdk, get_lanforge_data):
        print("Run Client Connectivity Here - NAT Mode")
        test_result = []
        for profile in setup_nat_mode[3]:
            print(profile)
            if str(profile["ssid_name"]).__contains__("EAP"):
                eap_connect = EAPConnect(get_lanforge_data["lanforge_ip"], 8080)
                eap_connect.upstream_resource = 1
                eap_connect.upstream_port = get_lanforge_data["lanforge_bridge_port"]
                eap_connect.security = "wpa2"
                eap_connect.sta_list = [get_lanforge_data["lanforge_5g_station"]]
                eap_connect.station_names = [get_lanforge_data["lanforge_5g_station"]]
                eap_connect.sta_prefix = get_lanforge_data["lanforge_5g_prefix"]
                eap_connect.ssid = profile["ssid_name"]
                eap_connect.radio = get_lanforge_data["lanforge_5g"]
                eap_connect.eap = "TTLS"
                eap_connect.identity = "nolaradius"
                eap_connect.ttls_passwd = "nolastart"
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
                    test_result.append("PASS")
                else:
                    test_result.append("FAIL")
            else:
                # SSID, Passkey, Security, Run layer3 tcp, udp upstream downstream
                staConnect = StaConnect2(get_lanforge_data["lanforge_ip"], 8080, debug_=False)
                staConnect.sta_mode = 0
                staConnect.upstream_resource = 1
                staConnect.upstream_port = get_lanforge_data["lanforge_bridge_port"]
                staConnect.radio = get_lanforge_data["lanforge_5g"]
                staConnect.resource = 1
                staConnect.dut_ssid = profile["ssid_name"]
                staConnect.dut_passwd = profile["security_key"]
                staConnect.dut_security = profile["security_key"].split("-")[1].split("_")[0].lower()
                staConnect.station_names = [get_lanforge_data["lanforge_5g_station"]]
                staConnect.sta_prefix = get_lanforge_data["lanforge_5g_prefix"]
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
                    test_result.append("PASS")
                else:
                    test_result.append("FAIL")
        print(test_result)
        if test_result.__contains__("FAIL"):
            assert False
        else:
            assert True

