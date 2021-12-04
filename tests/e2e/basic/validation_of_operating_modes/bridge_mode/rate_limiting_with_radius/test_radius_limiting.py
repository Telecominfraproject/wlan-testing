"""
Rate LImiting with radius Bridge Mode Scenario
"""

import allure
import pytest
from configuration import RATE_LIMITING_RADIUS_SERVER_DATA
from configuration import RATE_LIMITING_RADIUS_ACCOUNTING_DATA

pytestmark = [pytest.mark.regression, pytest.mark.rate_limiting_with_radius, pytest.mark.bridge]


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
             }
             }]},
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
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5849", name="WIFI-5849")
    def test_radius_server_2g_up(self, lf_test, lf_tools, rate_radius_info, rate_radius_accounting_info, station_names_twog):
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
            wct_obj = lf_test.wifi_capacity(instance_name="Test_Radius_2g", mode=mode, vlan_id=vlan,
                                            download_rate="0bps", batch_size="1",
                                            upload_rate="1Gbps", protocol="TCP-IPv4", duration="60000")

            report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
        assert True