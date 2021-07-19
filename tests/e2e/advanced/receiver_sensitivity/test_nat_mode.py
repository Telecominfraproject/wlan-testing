"""

    Performance Test: Receiver Sensitivity Test: nat Mode
    pytest -m "rx_sensitivity_test and nat"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.rx_sensitivity_test, pytest.mark.nat,
              pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something"}]},
    "rf": {
        "is5GHz": {"channelBandwidth": "is20MHz"},
        "is5GHzL": {"channelBandwidth": "is20MHz"},
        "is5GHzU": {"channelBandwidth": "is20MHz"}},
    "radius": False
}


@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestRxSensitivityNAT5G(object):
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs0
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs0_nss1_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.rx_sensitivity(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_RX_SEN_WPA2_5G_MCS0",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs1
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs1_nss1_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 1,
            "nss": 0,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs2
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs2_nss1_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 2,
            "nss": 0,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs3
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs3_nss1_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 3,
            "nss": 0,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs4
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs4_nss1_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 4,
            "nss": 0,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs5
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs5_nss1_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 5,
            "nss": 0,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs6
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs6_nss1_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 6,
            "nss": 0,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs7
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs7_nss1_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 7,
            "nss": 0,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs8
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs8_nss1_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 8,
            "nss": 0,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs9
    @pytest.mark.nss1
    def test_client_wpa2_personal_mcs9_nss1_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 9,
            "nss": 0,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    # Test case for mcs0-9,Nss 2, bw 20MHz

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs0
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs0_nss2_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 0,
            "nss": 1,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs1
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs1_nss2_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 1,
            "nss": 1,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs2
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs2_nss2_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 2,
            "nss": 1,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs3
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs3_nss2_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 3,
            "nss": 1,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs4
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs4_nss2_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 4,
            "nss": 1,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs5
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs5_nss2_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 5,
            "nss": 1,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs6
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs6_nss2_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 6,
            "nss": 1,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs7
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs7_nss2_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 7,
            "nss": 1,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs8
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs8_nss2_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 8,
            "nss": 1,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs9
    @pytest.mark.nss2
    def test_client_wpa2_personal_mcs9_nss2_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 9,
            "nss": 1,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    # Test case for mcs0-9,Nss 3, bw 20MHz

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs0
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs0_nss3_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 0,
            "nss": 2,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs1
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs1_nss3_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 1,
            "nss": 2,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs2
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs2_nss3_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 2,
            "nss": 2,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs3
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs3_nss3_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 3,
            "nss": 2,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs4
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs4_nss3_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 4,
            "nss": 2,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs5
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs5_nss3_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 5,
            "nss": 2,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs6
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs6_nss3_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 6,
            "nss": 2,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs7
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs7_nss3_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 7,
            "nss": 2,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs8
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs8_nss3_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 8,
            "nss": 2,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs9
    @pytest.mark.nss3
    def test_client_wpa2_personal_mcs9_nss3_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 9,
            "nss": 2,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    # Test case for mcs0-9,Nss 4, bw 20MHz

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs0
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs0_nss4_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 0,
            "nss": 3,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs1
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs1_nss4_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 1,
            "nss": 3,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs2
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs2_nss4_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 2,
            "nss": 3,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs3
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs3_nss4_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 3,
            "nss": 3,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs4
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs4_nss4_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 4,
            "nss": 3,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs5
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs5_nss4_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 5,
            "nss": 3,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs6
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs6_nss4_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 6,
            "nss": 3,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs7
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs7_nss4_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 7,
            "nss": 2,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs8
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs8_nss4_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 8,
            "nss": 3,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.mcs9
    @pytest.mark.nss4
    def test_client_wpa2_personal_mcs9_nss4_5g(self, get_vif_state,
                                          lf_test, station_names_fiveg, create_lanforge_chamberview_dut,
                                          get_configuration):
        """Receiver Sensitivity nat Mode
           pytest -m "rx_sensitivity_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        txo_data = {
            "txo_enable": 1,
            "txpower": 255,
            "pream": 3,
            "mcs": 9,
            "nss": 3,
            "bw": 0,
            "retries": 1,
            "sgi": 0
        }
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan, set_txo=txo_data)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, rx_sen=True)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False
