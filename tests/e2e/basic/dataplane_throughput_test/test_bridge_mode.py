import pytest
pytestmark = [pytest.mark.dataplane_throughput_test, pytest.mark.bridge]
import sys

for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../lanforge/lanforge-scripts/{folder}')
import lf_dataplane_test
import time
from lf_dataplane_test import DataplaneTest
import create_station
from create_station import CreateStation


@pytest.mark.dataplane_throughput_test
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    'setup_profiles, create_profiles',
    [(["BRIDGE"], ["BRIDGE"])],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.usefixtures("create_profiles")
class TestDataplaneThroughputBridge(object):

    @pytest.mark.wpa
    @pytest.mark.twog
    def test_client_wpa_2g(self, get_lanforge_data, setup_profile_data):
        profile_data = setup_profile_data["BRIDGE"]["WPA"]["2G"]
        lanforge_ip = get_lanforge_data["lanforge_ip"]
        lanforge_port = int(get_lanforge_data["lanforge-port-number"])
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        upstream = get_lanforge_data["lanforge_bridge_port"]
        radio = get_lanforge_data["lanforge_2dot4g"]
        station_name = get_lanforge_data["lanforge_2dot4g_station"]
        create_station = CreateStation(_host=lanforge_ip,
                                       _port=lanforge_port,
                                       _ssid=ssid,
                                       _password=security_key,
                                       _security=security,
                                       _sta_list=[station_name],
                                       _radio=radio)

        create_station.build()
        time.sleep(20)

        PASS = False
        if create_station.wait_for_ip([station_name]):
            create_station._pass("ALL Stations got IP's", print_=True)

            CV_Test = DataplaneTest(lf_host=lanforge_ip,
                                    lf_port=lanforge_port,
                                    lf_user="lanforge",
                                    lf_password="lanforge",
                                    instance_name="dpt_instance_wpa_2g_bridge",
                                    config_name="dpt_config",
                                    upstream="1.1." + upstream,
                                    pull_report=True,
                                    load_old_cfg=False,
                                    download_speed="85%",
                                    upload_speed="0",
                                    duration="15s",
                                    dut="TIP",
                                    station="1.1."+station_name,
                                    raw_lines="pkts: Custom",
                                    )
            CV_Test.setup()
            CV_Test.run()

            PASS = True
        assert PASS

    @pytest.mark.wpa

    @pytest.mark.fiveg
    def test_client_wpa_5g(self, get_lanforge_data, setup_profile_data):
        profile_data = setup_profile_data["BRIDGE"]["WPA"]["5G"]
        lanforge_ip = get_lanforge_data["lanforge_ip"]
        lanforge_port = int(get_lanforge_data["lanforge-port-number"])
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa"
        upstream = get_lanforge_data["lanforge_bridge_port"]
        radio = get_lanforge_data["lanforge_5g"]
        station_name = get_lanforge_data["lanforge_5g_station"]
        # Write Your test case Here
        create_station = CreateStation(_host=lanforge_ip,
                                       _port=lanforge_port,
                                       _ssid=ssid,
                                       _password=security_key,
                                       _security=security,
                                       _sta_list=[station_name],
                                       _radio=radio)

        create_station.build()
        time.sleep(60)
        PASS = False
        if create_station.wait_for_ip([station_name]):
            create_station._pass("ALL Stations got IP's", print_=True)
            CV_Test = DataplaneTest(lf_host=lanforge_ip,
                                    lf_port=lanforge_port,
                                    lf_user="lanforge",
                                    lf_password="lanforge",
                                    instance_name="dpt_instance_wpa_5g_bridge",
                                    config_name="dpt_config",
                                    upstream="1.1." + upstream,
                                    pull_report=True,
                                    load_old_cfg=False,
                                    download_speed="85%",
                                    upload_speed="0",
                                    duration="15s",
                                    dut="TIP",
                                    station="1.1."+station_name,
                                    raw_lines="pkts: Custom",
                                    )
            CV_Test.setup()
            CV_Test.run()
            PASS = True
        assert PASS


    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_client_wpa2_personal_2g(self, get_lanforge_data, setup_profile_data):
        profile_data = setup_profile_data["BRIDGE"]["WPA2_P"]["2G"]
        lanforge_ip = get_lanforge_data["lanforge_ip"]
        lanforge_port = int(get_lanforge_data["lanforge-port-number"])
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        upstream = get_lanforge_data["lanforge_bridge_port"]
        radio = get_lanforge_data["lanforge_2dot4g"]
        station_name = get_lanforge_data["lanforge_2dot4g_station"]
        create_station = CreateStation(_host=lanforge_ip,
                                       _port=lanforge_port,
                                       _ssid=ssid,
                                       _password=security_key,
                                       _security=security,
                                       _sta_list=[station_name],
                                       _radio=radio)

        create_station.build()
        time.sleep(60)
        PASS = False
        if create_station.wait_for_ip([station_name]):
            create_station._pass("ALL Stations got IP's", print_=True)
            CV_Test = DataplaneTest(lf_host=lanforge_ip,
                                    lf_port=lanforge_port,
                                    lf_user="lanforge",
                                    lf_password="lanforge",
                                    instance_name="dpt_instance_wpa2_p_2g_bridge",
                                    config_name="dpt_config",
                                    upstream="1.1." + upstream,
                                    pull_report=True,
                                    load_old_cfg=False,
                                    download_speed="85%",
                                    upload_speed="0",
                                    duration="15s",
                                    dut="TIP",
                                    station="1.1." + station_name,
                                    raw_lines="pkts: Custom",
                                    )
            CV_Test.setup()
            CV_Test.run()
            PASS = True

        assert PASS

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_client_wpa2_personal_5g(self, get_lanforge_data, setup_profile_data):
        profile_data = setup_profile_data["BRIDGE"]["WPA2_P"]["5G"]
        lanforge_ip = get_lanforge_data["lanforge_ip"]
        lanforge_port = int(get_lanforge_data["lanforge-port-number"])
        ssid = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        upstream = get_lanforge_data["lanforge_bridge_port"]
        radio = get_lanforge_data["lanforge_5g"]
        # Write Your test case Here
        station_name = get_lanforge_data["lanforge_5g_station"]
        create_station = CreateStation(_host=lanforge_ip,
                                       _port=lanforge_port,
                                       _ssid=ssid,
                                       _password=security_key,
                                       _security=security,
                                       _sta_list=[station_name],
                                       _radio=radio)

        create_station.build()
        time.sleep(60)
        PASS = False
        if create_station.wait_for_ip([station_name]):
            create_station._pass("ALL Stations got IP's", print_=True)
            CV_Test = DataplaneTest(lf_host=lanforge_ip,
                                    lf_port=lanforge_port,
                                    lf_user="lanforge",
                                    lf_password="lanforge",
                                    instance_name="dpt_instance_wpa2_p_5g_bridge",
                                    config_name="dpt_config",
                                    upstream="1.1." + upstream,
                                    pull_report=True,
                                    load_old_cfg=False,
                                    download_speed="85%",
                                    upload_speed="0",
                                    duration="15s",
                                    dut="TIP",
                                    station="1.1." + station_name,
                                    raw_lines="pkts: Custom",
                                    )
            CV_Test.setup()
            CV_Test.run()
            PASS = True
        assert PASS
