"""
Rate LImiting with radius Bridge Mode Scenario
"""

import allure
import pytest
from configuration import RATE_LIMITING_RADIUS_SERVER_DATA
from configuration import RATE_LIMITING_RADIUS_ACCOUNTING_DATA

pytestmark = [pytest.mark.regression,
              pytest.mark.rate_limiting_with_radius,
              pytest.mark.bridge]


setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_2g_br",
             "appliedRadios": ["2G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 50,
                 "egress-rate": 50
             },
             "radius_auth_data": RATE_LIMITING_RADIUS_SERVER_DATA,
             "radius_acc_data" : RATE_LIMITING_RADIUS_ACCOUNTING_DATA

             },
            {"ssid_name": "ssid_wpa2_5g_br",
             "appliedRadios": ["5G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 50,
                 "egress-rate": 50
             },
             "radius_auth_data": RATE_LIMITING_RADIUS_SERVER_DATA,
             "radius_acc_data" : RATE_LIMITING_RADIUS_ACCOUNTING_DATA
             }
        ]
    },
    "rf": {},
    "radius": False
}


@allure.feature("Bridge MODE Rate Limiting with radius server")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestRateLimitingWithRadiusBridge(object):

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.ow_sanity_lf
    @pytest.mark.twog_upload_per_ssid
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5849", name="WIFI-5849")
    def test_radius_server_2g_upload_per_ssid(self, lf_test, lf_tools, rate_radius_info, rate_radius_accounting_info, station_names_twog):
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        print("authentication", rate_radius_info)
        print("accounting",rate_radius_accounting_info )
        ttls_passwd = rate_radius_info["password"]
        identity = rate_radius_info['user']
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_2g_up_per_ssid", mode=mode, vlan_id=vlan,
                                            download_rate="0bps", batch_size="1",
                                            upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000", raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.twog_download_perssid_persta
    @pytest.mark.ow_sanity_lf
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5850", name="WIFI-5850")
    def test_radius_server_2g_download_perssid_persta(self, lf_test, lf_tools, rate_radius_info, rate_radius_accounting_info,
                                     station_names_twog):
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        print("authentication", rate_radius_info)
        print("accounting", rate_radius_accounting_info)
        ttls_passwd = rate_radius_info["password"]
        identity = rate_radius_info['user']
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel:  Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_2g_down_perssid_persta", mode=mode, vlan_id=vlan,
                                            download_rate="1Gbps", batch_size="1",
                                            upload_rate="0bps", protocol="TCP-IPv4", duration="60000", raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.twog_upload_persta_perclient
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5851", name="WIFI-5851")
    def test_radius_server_2g_upload_persta_perclient_rate(self, lf_test, lf_tools, rate_radius_info, rate_radius_accounting_info,
                                     station_names_twog):
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        print("authentication", rate_radius_info)
        print("accounting", rate_radius_accounting_info)
        ttls_passwd = rate_radius_info["password"]
        identity = rate_radius_info['user']
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel:  Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_2g_up_per_per_client", mode=mode, vlan_id=vlan,
                                            download_rate="0bps", batch_size="1",
                                            upload_rate="2.488Gbps", protocol="TCP-IPv4", duration="60000", raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.twog_upload_download_persta_perclient
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5852", name="WIFI-5852")
    def test_radius_server_2g_upload_download_persta_perclient_rate(self, lf_test, lf_tools, rate_radius_info,
                                                           rate_radius_accounting_info,
                                                           station_names_twog):
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        print("authentication", rate_radius_info)
        print("accounting", rate_radius_accounting_info)
        ttls_passwd = rate_radius_info["password"]
        identity = rate_radius_info['user']
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel:  Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_2g_up_down_per_per_client", mode=mode, vlan_id=vlan,
                                            download_rate="1Gbps", batch_size="1",
                                            upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                            raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.fiveg_download_per_ssid
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5853", name="WIFI-5853")
    def test_radius_server_fiveg_per_ssid_download(self, lf_test, lf_tools, rate_radius_info, rate_radius_accounting_info,
                                                 station_names_fiveg):
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        print("authentication", rate_radius_info)
        print("accounting", rate_radius_accounting_info)
        ttls_passwd = rate_radius_info["password"]
        identity = rate_radius_info['user']
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_5g_down_per_ssid", mode=mode, vlan_id=vlan,
                                            download_rate="1Gbps", batch_size="1",
                                            upload_rate="0bps", protocol="TCP-IPv4", duration="60000",raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.fiveg_upload_per_ssid
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5854", name="WIFI-5854")
    def test_radius_server_fiveg_per_ssid_upload(self, lf_test, lf_tools, rate_radius_info, rate_radius_accounting_info,
                                          station_names_fiveg):
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        print("authentication", rate_radius_info)
        print("accounting", rate_radius_accounting_info)
        ttls_passwd = rate_radius_info["password"]
        identity = rate_radius_info['user']
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_5g_up_per_ssid", mode=mode, vlan_id=vlan,
                                            download_rate="0bps", batch_size="1",
                                            upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000", raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.fiveg_download_per_ssid_per_client
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5855", name="WIFI-5855")
    def test_radius_server_fiveg_per_ssid_perclient_download(self, lf_test, lf_tools, rate_radius_info, rate_radius_accounting_info,
                                                 station_names_fiveg):
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        print("authentication", rate_radius_info)
        print("accounting", rate_radius_accounting_info)
        ttls_passwd = rate_radius_info["password"]
        identity = rate_radius_info['user']
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel:  Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_5g_down_per_ssid_perclient", mode=mode, vlan_id=vlan,
                                            download_rate="1Gbps", batch_size="1",
                                            upload_rate="0bps", protocol="TCP-IPv4", duration="60000",
                                            raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.fiveg_upstream_per_ssid_per_client
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5856", name="WIFI-5856")
    def test_radius_server_fiveg_per_ssid_perclient_upstream(self, lf_test, lf_tools, rate_radius_info,
                                                             rate_radius_accounting_info,
                                                             station_names_fiveg):
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        print("authentication", rate_radius_info)
        print("accounting", rate_radius_accounting_info)
        ttls_passwd = rate_radius_info["password"]
        identity = rate_radius_info['user']
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel:  Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_5g_upstream_per_ssid_perclient", mode=mode,
                                            vlan_id=vlan,
                                            download_rate="0bps", batch_size="1",
                                            upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                            raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.fiveg_upstream__downstream_per_ssid_per_client
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5857", name="WIFI-5857")
    def test_radius_server_fiveg_per_ssid_perclient_upstream_downstream(self, lf_test, lf_tools, rate_radius_info,
                                                             rate_radius_accounting_info,
                                                             station_names_fiveg):
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        print("authentication", rate_radius_info)
        print("accounting", rate_radius_accounting_info)
        ttls_passwd = rate_radius_info["password"]
        identity = rate_radius_info['user']
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel:  Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Download Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_5g_upstream_downstream_per_ssid_perclient", mode=mode,
                                            vlan_id=vlan,
                                            download_rate="1Gbps", batch_size="1",
                                            upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                            raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.twog_per_ssid
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5858", name="WIFI-5858")
    def test_radius_server_2g_per_ssid(self, lf_test, lf_tools, rate_radius_info, rate_radius_accounting_info,
                                              station_names_twog):
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        print("authentication", rate_radius_info)
        print("accounting", rate_radius_accounting_info)
        ttls_passwd = rate_radius_info["password"]
        identity = rate_radius_info['user']
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Total Download Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_2g_per_ssid", mode=mode, vlan_id=vlan,
                                            download_rate="0bps", batch_size="1",
                                            upload_rate="1Gbps", protocol="TCP and UDP IPv4", duration="60000",
                                            raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.fiveg_per_ssid
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5860", name="WIFI-5860")
    def test_radius_server_fiveg_per_ssid(self, lf_test, lf_tools, rate_radius_info, rate_radius_accounting_info,
                                                 station_names_fiveg):
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        print("authentication", rate_radius_info)
        print("accounting", rate_radius_accounting_info)
        ttls_passwd = rate_radius_info["password"]
        identity = rate_radius_info['user']
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel:  Per-Station Upload Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_5g_per_ssid", mode=mode, vlan_id=vlan,
                                            download_rate="1Gbps", batch_size="1",
                                            upload_rate="0bps", protocol="TCP-IPv4", duration="60000",
                                            raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.twog_per_ssid_per_client
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5862", name="WIFI-5862")
    def test_radius_server_2g_per_ssid_per_client(self, lf_test, lf_tools, rate_radius_info, rate_radius_accounting_info,
                                       station_names_twog):
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        print("authentication", rate_radius_info)
        print("accounting", rate_radius_accounting_info)
        ttls_passwd = rate_radius_info["password"]
        identity = rate_radius_info['user']
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel: Per-Station Download Rate:"], ["ul_rate_sel: Per-Station Upload Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_2g_per_ssid_per_client", mode=mode, vlan_id=vlan,
                                            download_rate="1Gbps", batch_size="1",
                                            upload_rate="1Gbps", protocol="TCP and UDP IPv4", duration="60000",
                                            raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @pytest.mark.fiveg_per_ssid_per_client
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5864", name="WIFI-5864")
    def test_radius_server_fiveg_per_ssid_per_client(self, lf_test, lf_tools, rate_radius_info, rate_radius_accounting_info,
                                          station_names_fiveg):
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "fiveg"
        eap = "TTLS"
        print("authentication", rate_radius_info)
        print("accounting", rate_radius_accounting_info)
        ttls_passwd = rate_radius_info["password"]
        identity = rate_radius_info['user']
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel: Per-Station Download Rate:"], ["ul_rate_sel:  Per-Station Upload Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_5g_per_ssid_per_client", mode=mode, vlan_id=vlan,
                                            download_rate="1Gbps", batch_size="1",
                                            upload_rate="0bps", protocol="TCP and UDP IPv4", duration="60000",
                                            raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.twog_per_ssid_down
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5868", name="WIFI-5868")
    def test_radius_server_2g_per_ssid_downstream(self, lf_test, lf_tools, rate_radius_info,
                                                  rate_radius_accounting_info,
                                                  station_names_twog):
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        print("authentication", rate_radius_info)
        print("accounting", rate_radius_accounting_info)
        ttls_passwd = rate_radius_info["password"]
        identity = rate_radius_info['user']
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Total Upload Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_2g", mode=mode, vlan_id=vlan,
                                            download_rate="1Gbps", batch_size="1",
                                            upload_rate="0bps", protocol="TCP and UDP IPv4", duration="60000",
                                            raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.twog
    @pytest.mark.max_upload_user1
    @pytest.mark.wpa2_enterprise
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7618", name="WIFI-7618")
    def test_radius_server_ratelimit_maxupload_groupuser1_2g(self, lf_test, lf_tools, station_names_twog):
        """
            Test: check max-upload ratelimit of group - user1
            pytest -m "wpa2_enterprise and twog and max_upload_user1"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = 'password'
        identity = 'user1'
        allure.attach(name="Max-Upload-User1", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Ratelimit_Radius_group_user1", mode=mode, vlan_id=vlan,
                                            download_rate="0bps", batch_size="1",
                                            upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000",
                                            raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            assert True
        else:
            assert False


    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @pytest.mark.max_download_user1
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-7619", name="WIFI-7619")
    def test_radius_server_ratelimit_maxdownload_groupuser1_2g(self, lf_test, lf_tools, station_names_twog):
        """
            Test: check max-download ratelimit of group - user1
            pytest -m "wpa2_enterprise and twog and max_download_user1"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        security = "wpa2"
        band = "twog"
        eap = "TTLS"
        ttls_passwd = 'password'
        identity = 'user1'
        allure.attach(name="Max-Download-User1", body=str(profile_data["rate-limit"]))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, ieee80211w=0, vlan_id=vlan, cleanup=False)
        print(passes)
        if passes:
            raw_lines = [["dl_rate_sel: Total Download Rate:"], ["ul_rate_sel: Per-Total Download Rate:"]]
            wct_obj = lf_test.wifi_capacity(instance_name="Ratelimit_Radius_group_user1", mode=mode, vlan_id=vlan,
                                            download_rate="1Gbps", batch_size="1",
                                            upload_rate="0bps", protocol="TCP-IPv4", duration="60000",
                                            raw_lines=raw_lines)

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            assert True
        else:
            assert False
