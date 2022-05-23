import time
import pytest
import sys
import allure

if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

pytestmark = [pytest.mark.regression, pytest.mark.interop, pytest.mark.android, pytest.mark.interop_and, pytest.mark.ToggleWifiMode,
              pytest.mark.client_reconnect, pytest.mark.enterprise]

@allure.feature("Maverick")
@pytest.mark.maverick
class TestMaverick(object):
    @pytest.mark.nolme
    def test_ap_maverick(self,request, lf_tools, setup_controller, get_vif_state, get_configuration, get_ap_logs, get_apnos):
        for ap in get_configuration['access_point']:
            cmd = "uci show ucentral"
            print(get_configuration['access_point'])
            ap_ssh = get_apnos(ap, pwd="../libs/apnos/", sdk="2.x")
            gw = ap_ssh.run_generic_command(cmd)
            print("Status:")
            print(gw)
            connected, latest, active = ap_ssh.get_ucentral_status()
            print("Connected:")
            print(connected)
            iwinfo = ap_ssh.get_iwinfo()
            print("iwinfo:")
            print(iwinfo)
            maverick = ap_ssh.set_maverick()
            print("maverick:")
            print(maverick)
            # reboot = ap_ssh.reboot()
            # print("rebooted")
            # print(reboot)
            return True



