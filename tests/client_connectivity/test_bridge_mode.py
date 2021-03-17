import pytest
import sys
#
#
# for folder in 'py-json', 'py-scripts':
#     if folder not in sys.path:
#         sys.path.append(f'../../lanforge/lanforge-scripts/{folder}')
#
#
# from LANforge.LFUtils import *
#
# # if you lack __init__.py in this directory you will not find sta_connect module#
#
# if 'py-json' not in sys.path:
#     sys.path.append('../../py-scripts')
#
# import sta_connect2
# from sta_connect2 import StaConnect2
import time


@pytest.mark.usefixtures('setup_cloudsdk')
@pytest.mark.usefixtures('update_firmware')
@pytest.mark.bridge_mode_client_connectivity
class TestBridgeModeClientConnectivity(object):

    @pytest.mark.bridge_mode_single_client_connectivity
    @pytest.mark.nightly
    @pytest.mark.nightly_bridge
    def test_single_client(self, setup_cloudsdk, update_firmware, setup_bridge_mode, disconnect_cloudsdk):
        print("Run Client Connectivity Here - BRIDGE Mode")
        for i in setup_bridge_mode:
            for j in i:
                staConnect = StaConnect2("192.168.200.80", 8080, debug_=False)
                staConnect.sta_mode = 0
                staConnect.upstream_resource = 1
                staConnect.upstream_port = "eth1"
                staConnect.radio = "wiphy0"
                staConnect.resource = 1
                staConnect.dut_ssid = j
                staConnect.dut_passwd = "[BLANK]"
                staConnect.dut_security = "open"
                staConnect.station_names = ["sta0000", "sta0001"]
                staConnect.sta_prefix = "sta"
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
                    print("Single client connection to", staConnect.dut_ssid, "successful. Test Passed")
                else:
                    print("Single client connection to", staConnect.dut_ssid, "unsuccessful. Test Failed")

        time.sleep(30)
        if setup_bridge_mode[0] == setup_bridge_mode[1]:
            assert True
        else:
            assert False

    @pytest.mark.bridge_mode_multi_client_connectivity
    def test_multi_client(self, create_vlan_profile):
        print(create_vlan_profile)
        assert 1 == 1

