"""
       Dual Band Performance Test : Bridge Mode
       pytest -m "dual_band_performance_test and bridge"


"""

import os
import allure
import pytest

pytestmark = [pytest.mark.dual_band_performance_test, pytest.mark.bridge,
              pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["is2dot4GHz"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
                 "security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2p_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2p_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@pytest.mark.dual_band_performance_test
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)

@pytest.mark.usefixtures("setup_profiles")
class TestDualbandPerformanceBridge(object):
    """
        pytest -m "dual_band_performance_test and bridge and open and twog  and fiveg"
    """

    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.fiveg
    def test_client_open(self,get_vif_state,create_lanforge_chamberview_dut, lf_test,get_configuration):
        profile_data = setup_params_general["ssid_modes"]["open"]
        ssid_2G = profile_data[0]["ssid_name"]
        ssid_5G = profile_data[1]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        if ssid_2G and ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        dbpt_obj = lf_test.dualbandperformancetest(mode=mode,ssid_2G=ssid_2G,ssid_5G=ssid_5G,
                                   instance_name="dbp_instance_open_bridge",
                                   vlan_id=vlan, dut_name=dut_name)
        report_name = dbpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        entries = os.listdir("../reports/" + report_name + '/')
        pdf = False
        for i in entries:
            if ".pdf" in i:
                pdf = i
        if pdf:
            allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                               name=get_configuration["access_point"][0]["model"] + "_dualbandperfomance")

    """
       pytest -m "dual_band_performance_test and bridge and wpa and twog  and fiveg"
    """
    @pytest.mark.wpa
    @pytest.mark.twog
    @pytest.mark.fiveg
    def test_client_wpa(self, get_vif_state,create_lanforge_chamberview_dut, lf_test,get_configuration):
        profile_data = setup_params_general["ssid_modes"]["wpa"]
        ssid_2G = profile_data[0]["ssid_name"]
        ssid_5G = profile_data[1]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        if ssid_2G and ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        dbpt_obj = lf_test.dualbandperformancetest(mode=mode, ssid_2G=ssid_2G, ssid_5G=ssid_5G,
                                                   instance_name="dbp_instance_wpa_bridge",
                                                   vlan_id=vlan, dut_name=dut_name)
        report_name = dbpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        entries = os.listdir("../reports/" + report_name + '/')
        pdf = False
        for i in entries:
            if ".pdf" in i:
                pdf = i
        if pdf:
            allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                               name=get_configuration["access_point"][0]["model"] + "_dualbandperfomance")

    """
         pytest -m "dual_band_performance_test and bridge and wpa2_personal and twog  and fiveg"
    """
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.fiveg
    def test_client_wpa2_personal(self,get_vif_state,create_lanforge_chamberview_dut,lf_test,get_configuration):
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"]
        ssid_2G = profile_data[0]["ssid_name"]
        ssid_5G = profile_data[1]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "BRIDGE"
        vlan = 1
        if ssid_2G and ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        dbpt_obj = lf_test.dualbandperformancetest(mode=mode, ssid_2G=ssid_2G, ssid_5G=ssid_5G,
                                                   instance_name="dbp_instance_wpa2p_bridge",
                                                   vlan_id=vlan, dut_name=dut_name)
        report_name = dbpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        entries = os.listdir("../reports/" + report_name + '/')
        pdf = False
        for i in entries:
            if ".pdf" in i:
                pdf = i
        if pdf:
            allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                               name=get_configuration["access_point"][0]["model"] + "_dualbandperfomance")

