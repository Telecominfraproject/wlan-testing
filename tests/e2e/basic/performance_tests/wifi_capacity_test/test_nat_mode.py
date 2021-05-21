import pytest
import sys
import time
import lf_wifi_capacity_test
from lf_wifi_capacity_test import WiFiCapacityTest
#import create_station
#from create_station import CreateStation
pytestmark = [pytest.mark.wifi_capacity_test, pytest.mark.nat]

for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../lanforge/lanforge-scripts/{folder}')

sys.path.append(f"../lanforge/lanforge-scripts/py-scripts/tip-cicd-sanity")

sys.path.append(f'../libs')
sys.path.append(f'../libs/lanforge/')

from LANforge.LFUtils import *

'''if 'py-json' not in sys.path:
    sys.path.append('../py-scripts')'''
from sta_connect2 import StaConnect2
from eap_connect import EAPConnect

# @pytest.mark.sanity
@pytest.mark.wifi_capacity_test
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    'setup_profiles, create_profiles',
    [(["NAT"], ["NAT"])],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.usefixtures("create_profiles")
class TestWifiCapacityNatMode(object):

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_client_wpa_2g(self, request, get_lanforge_data, setup_profile_data, instantiate_testrail,
                           instantiate_project, test_cases):
        print("")
        profile_data = setup_profile_data["NAT"]["WPA"]["2G"]
        lanforge_ip = get_lanforge_data["lanforge_ip"]
        lanforge_port = int(get_lanforge_data["lanforge-port-number"])
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        upstream = get_lanforge_data["lanforge_bridge_port"]
        radio = get_lanforge_data["lanforge_2dot4g"]
        station_name = get_lanforge_data["lanforge_2dot4g_station"]
        '''create_station = CreateStation(_host = lanforge_ip,
                                       _port = lanforge_port,
                                       _ssid = ssid,
                                       _password = security_key,
                                       _security = security,
                                       _sta_list = [station_name],
                                       _radio = radio)
        create_station.build()
        time.sleep(20)'''

        PASS = False
        WFC_Test = WiFiCapacityTest(lf_host = lanforge_ip,
                                    lf_port = lanforge_port,
                                    lf_user = "lanforge",
                                    lf_password = "lanforge",
                                    instance_name = "wct_instance",
                                    config_name = "wifi_config",
                                    upstream = f"1.1.{upstream}",
                                    batch_size = "1",
                                    loop_iter = "1",
                                    protocol = "UDP-IPv4",
                                    duration = "3000",
                                    pull_report = True,
                                    load_old_cfg = False,
                                    upload_rate = "10Mbps",
                                    download_rate = "1Gbps",
                                    sort = "interleave",
                                    stations = "1.1.sta0000,1.1.sta0001",
                                    create_stations = True,
                                    radio = radio,
                                    security = security,
                                    paswd = security_key,
                                    ssid = ssid,
                                    enables = [],
                                    disables = [],
                                    raw_lines = [],
                                    raw_lines_file = "",
                                    sets = [],
                                    )
        WFC_Test.setup()
        WFC_Test.run()
        PASS = True
        #WFC_Test.check_influx_kpi(args)
        assert PASS

    @pytest.mark.wpa
    @pytest.mark.fiveg
    def test_client_wpa_5g(self, get_lanforge_data, setup_profile_data):
        profile_data = setup_profile_data["NAT"]["WPA"]["5G"]
        lanforge_ip = get_lanforge_data["lanforge_ip"]
        lanforge_port = int(get_lanforge_data["lanforge-port-number"])
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        upstream = get_lanforge_data["lanforge_bridge_port"]
        radio = get_lanforge_data["lanforge_5g"]
        # Write Your test case Here
        PASS = False
        WFC_Test = WiFiCapacityTest(lf_host=lanforge_ip,
                                    lf_port=lanforge_port,
                                    lf_user="lanforge",
                                    lf_password="lanforge",
                                    instance_name="wct_instance",
                                    config_name="wifi_config",
                                    upstream=f"1.1.{upstream}",
                                    batch_size="1",
                                    loop_iter="1",
                                    protocol="UDP-IPv4",
                                    duration="3000",
                                    pull_report=True,
                                    load_old_cfg=False,
                                    upload_rate="10Mbps",
                                    download_rate="1Gbps",
                                    sort="interleave",
                                    stations="1.1.sta0000,1.1.sta0001",
                                    create_stations=True,
                                    radio=radio,
                                    security=security,
                                    paswd=security_key,
                                    ssid=ssid,
                                    enables=[],
                                    disables=[],
                                    raw_lines=[],
                                    raw_lines_file="",
                                    sets=[],
                                    )
        WFC_Test.setup()
        WFC_Test.run()
        PASS = True
        assert PASS

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_client_wpa2_personal_2g(self, get_lanforge_data, setup_profile_data):
        profile_data = setup_profile_data["NAT"]["WPA2_P"]["2G"]
        lanforge_ip = get_lanforge_data["lanforge_ip"]
        lanforge_port = int(get_lanforge_data["lanforge-port-number"])
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        upstream = get_lanforge_data["lanforge_bridge_port"]
        radio = get_lanforge_data["lanforge_2dot4g"]
        # Write Your test case Here
        PASS = False
        WFC_Test = WiFiCapacityTest(lf_host=lanforge_ip,
                                    lf_port=lanforge_port,
                                    lf_user="lanforge",
                                    lf_password="lanforge",
                                    instance_name="wct_instance",
                                    config_name="wifi_config",
                                    upstream=f"1.1.{upstream}",
                                    batch_size="1",
                                    loop_iter="1",
                                    protocol="UDP-IPv4",
                                    duration="3000",
                                    pull_report=True,
                                    load_old_cfg=False,
                                    upload_rate="10Mbps",
                                    download_rate="1Gbps",
                                    sort="interleave",
                                    stations="1.1.sta0000,1.1.sta0001",
                                    create_stations=True,
                                    radio=radio,
                                    security=security,
                                    paswd=security_key,
                                    ssid=ssid,
                                    enables=[],
                                    disables=[],
                                    raw_lines=[],
                                    raw_lines_file="",
                                    sets=[],
                                    )
        WFC_Test.setup()
        WFC_Test.run()
        PASS = True
        assert PASS

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_client_wpa2_personal_5g(self, get_lanforge_data, setup_profile_data):
        profile_data = setup_profile_data["NAT"]["WPA2_P"]["5G"]
        lanforge_ip = get_lanforge_data["lanforge_ip"]
        lanforge_port = int(get_lanforge_data["lanforge-port-number"])
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        upstream = get_lanforge_data["lanforge_bridge_port"]
        radio = get_lanforge_data["lanforge_5g"]

        # Write Your test case Here
        PASS = False
        WFC_Test = WiFiCapacityTest(lf_host=lanforge_ip,
                                    lf_port=lanforge_port,
                                    lf_user="lanforge",
                                    lf_password="lanforge",
                                    instance_name="wct_instance",
                                    config_name="wifi_config",
                                    upstream=f"1.1.{upstream}",
                                    batch_size="1",
                                    loop_iter="1",
                                    protocol="UDP-IPv4",
                                    duration="3000",
                                    pull_report=True,
                                    load_old_cfg=False,
                                    upload_rate="10Mbps",
                                    download_rate="1Gbps",
                                    sort="interleave",
                                    stations="1.1.sta0000,1.1.sta0001",
                                    create_stations=True,
                                    radio=radio,
                                    security=security,
                                    paswd=security_key,
                                    ssid=ssid,
                                    enables=[],
                                    disables=[],
                                    raw_lines=[],
                                    raw_lines_file="",
                                    sets=[],
                                    )
        WFC_Test.setup()
        WFC_Test.run()
        PASS = True
        assert PASS


