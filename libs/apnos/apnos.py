"""
APNOS Library : Used to execute SSH Commands in AP Using Direct-AP-SSH/ Jumphost-Serial Console

Currently Having Methods:
    1. Get iwinfo
    2. AP Manager Satus
    3. Vif Config ssid's
    4. Vif State ssid's
    5. Get current Firmware

"""
import json
import string
import time
import random

import paramiko
import pytest
from scp import SCPClient
import os


class APNOS:

    def __init__(self, credentials=None, pwd=os.getcwd(), sdk="2.x"):
        self.serial = credentials['serial']
        self.owrt_args = "--prompt root@OpenAp -s serial --log stdout --user root --passwd openwifi"
        self.sdk = sdk
        if sdk == "2.x":
            self.owrt_args = "--prompt root@" + self.serial + " -s serial --log stdout --user root --passwd openwifi"
        if credentials is None:
            print("No credentials Given")
            exit()
        self.ip = credentials['ip']  # if mode=1, enter jumphost ip else ap ip address
        self.username = credentials['username']  # if mode=1, enter jumphost username else ap username
        self.password = credentials['password']  # if mode=1, enter jumphost password else ap password
        self.port = credentials['port']  # if mode=1, enter jumphost ssh port else ap ssh port
        self.mode = credentials['jumphost']  # 1 for jumphost, 0 for direct ssh

        if 'mode' in credentials:
            self.type = credentials['mode']

        if self.mode:
            self.tty = credentials['jumphost_tty']  # /dev/ttyAP1
            # kill minicom instance
            client = self.ssh_cli_connect()
            cmd = "pgrep 'minicom' -a"
            stdin, stdout, stderr = client.exec_command(cmd)
            a = str(stdout.read()).split("\\n")
            for i in a:
                if i.__contains__("minicom ap" + self.tty[-1]):
                    temp = i.split("minicom")
                    a = temp[0].replace(" ", "")
                    cmd = "kill " + str(a).replace("b'", "")
                    print(cmd)
                    stdin, stdout, stderr = client.exec_command(cmd)
            cmd = '[ -f ~/cicd-git/ ] && echo "True" || echo "False"'
            stdin, stdout, stderr = client.exec_command(cmd)
            output = str(stdout.read())
            
            if output.__contains__("False"):
                cmd = 'mkdir ~/cicd-git/'
                stdin, stdout, stderr = client.exec_command(cmd)
            cmd = '[ -f ~/cicd-git/openwrt_ctl.py ] && echo "True" || echo "False"'
            stdin, stdout, stderr = client.exec_command(cmd)
            output = str(stdout.read())
            if output.__contains__("False"):
                print("Copying openwrt_ctl serial control Script...")
                with SCPClient(client.get_transport()) as scp:
                    scp.put(pwd + '/openwrt_ctl.py', '~/cicd-git/openwrt_ctl.py')  # Copy my_file.txt to the server
            cmd = '[ -f ~/cicd-git/openwrt_ctl.py ] && echo "True" || echo "False"'
            stdin, stdout, stderr = client.exec_command(cmd)
            var = str(stdout.read())
            client.close()
            if var.__contains__("True"):
                print("APNOS Serial Setup OK")
            else:
                print("APNOS Serial Setup Fail")

    # Method to connect AP-CLI/ JUMPHOST-CLI
    def ssh_cli_connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("Connecting to jumphost: %s@%s:%s" % (
            self.username, self.ip, self.port))
        client.connect(self.ip, username=self.username, password=self.password,
                       port=self.port, timeout=10, allow_agent=False, banner_timeout=200)
        return client

    def reboot(self):
        client = self.ssh_cli_connect()

        cmd = "reboot"
        if self.mode:
            cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                  f"cmd --value \"{cmd}\" "
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read()
        client.close()
        return output

    # Method to get the iwinfo status of AP using AP-CLI/ JUMPHOST-CLI

    def get_bssid_band_mapping(self):
        client = self.ssh_cli_connect()
        cmd = 'iwinfo'
        if self.mode:
            cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                  f"cmd --value \"{cmd}\" "
        stdin, stdout, stderr = client.exec_command(cmd)
        data = stdout.read()
        client.close()
        data = str(data).replace(" ", "").split("\\r\\n")
        band_info = []
        client.close()
        for i in data:
            tmp = []
            if i.__contains__("AccessPoint"):
                bssid = i.replace("AccessPoint:", "")
                tmp.append(bssid.casefold())
            elif i.__contains__("MasterChannel"):
                if i.split(":")[2].__contains__("2.4"):
                    tmp.append("2G")
                else:
                    tmp.append("5G")
            else:
                tmp = []
            if tmp != []:
                band_info.append(tmp)
        bssi_band_mapping = {}
        for i in range(len(band_info)):
            if (i % 2) == 0:
                bssi_band_mapping[band_info[i][0]] = band_info[i + 1][0]
        return bssi_band_mapping

    # Method to get the vif_config of AP using AP-CLI/ JUMPHOST-CLI
    def get_vif_config(self):
        client = self.ssh_cli_connect()
        cmd = "/usr/opensync/bin/ovsh s Wifi_VIF_Config -c"
        if self.mode:
            cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                  f"cmd --value \"{cmd}\" "
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read()
        client.close()

        return output

    # Method to get the vif_state of AP using AP-CLI/ JUMPHOST-CLI
    def get_vif_state(self):
        client = self.ssh_cli_connect()
        cmd = "/usr/opensync/bin/ovsh s Wifi_VIF_State -c"
        if self.mode:
            cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                  f"cmd --value \"{cmd}\" "
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read()
        client.close()
        return output

    # Method to get the vif_config ssid's of AP using AP-CLI/ JUMPHOST-CLI
    def get_vif_config_ssids(self):
        stdout = self.get_vif_config()
        ssid_list = []
        for i in stdout.splitlines():
            ssid = str(i).replace(" ", "").split(".")
            if ssid[0].split(":")[0] == "b'ssid":
                ssid_list.append(ssid[0].split(":")[1].replace("'", ""))
        return ssid_list

    # Method to get the vif_state ssid's of AP using AP-CLI/ JUMPHOST-CLI
    def get_ssid_info(self):
        stdout = self.get_vif_state()
        ssid_info_list = []
        info = []
        for i in stdout.splitlines():
            ssid = str(i).replace(" ", "").split(".")
            # print(ssid)
            if ssid[0].split(":")[0] == "b'mac":
                mac_info_list = ssid[0].split(":")
                mac_info_list.pop(0)
                info.append(":".join(mac_info_list).replace("'", ""))
            if ssid[0].split(":")[0] == "b'security":
                security = ssid[0].split(":")[1].split(",")[2].replace("]", "").replace('"', "").replace("'", "")
                print(ssid[0].split(":")[1])
                if security != "OPEN":
                    if security == "WPA-PSK":
                        if ssid[0].split(":")[1].split(",")[6].__contains__("1"):
                            info.append("WPA")
                            security_key = ssid[0].split(":")[1].split(",")[4].replace('"', "").replace("]", "")
                        if ssid[0].split(":")[1].split(",")[6].__contains__("2"):
                            info.append("WPA2")
                            security_key = ssid[0].split(":")[1].split(",")[4].replace('"', "").replace("]", "")
                        if ssid[0].split(":")[1].split(",")[6].__contains__("mixed"):
                            info.append("WPA | WPA2")
                            security_key = ssid[0].split(":")[1].split(",")[4].replace('"', "").replace("]", "")
                    if security == "WPA-SAE":
                        if ssid[0].split(":")[1].split(",")[6].__contains__("3"):
                            info.append("WPA3_PERSONAL")
                            security_key = ssid[0].split(":")[1].split(",")[4].replace('"', "").replace("]", "")
                        if ssid[0].split(":")[1].split(",")[6].__contains__("mixed"):
                            info.append("WPA3_PERSONAL")
                            security_key = ssid[0].split(":")[1].split(",")[4].replace('"', "").replace("]", "")
                    if security == "WPA-EAP":
                        info.append("EAP-TTLS")
                        security_key = ssid[0].split(":")[1].split(",")[4].replace('"', "").replace("]", "")
                    if security == "WPA3-EAP":
                        info.append("EAP-TTLS")
                        security_key = ssid[0].split(":")[1].split(",")[4].replace('"', "").replace("]", "")
                    else:
                        security_key = ssid[0].split(":")[1].split(",")[4].replace('"', "").replace("]", "")
                    info.append(security_key)
                else:
                    info.append("OPEN")
            if ssid[0].split(":")[0] == "b'ssid":
                info.append(ssid[0].split(":")[1].replace("'", ""))
                ssid_info_list.append(info)
                info = []
        print(ssid_info_list)
        return ssid_info_list

    # Get VIF State parameters
    def get_vif_state_ssids(self):
        stdout = self.get_vif_state()
        ssid_list = []
        for i in stdout.splitlines():
            ssid = str(i).replace(" ", "").split(".")
            if ssid[0].split(":")[0] == "b'ssid":
                ssid_list.append(ssid[0].split(":")[1].replace("'", ""))
        return ssid_list

    # Method to get the active firmware of AP using AP-CLI/ JUMPHOST-CLI
    def get_active_firmware(self):
        try:
            client = self.ssh_cli_connect()
            cmd = '/usr/opensync/bin/ovsh s AWLAN_Node -c | grep FW_IMAGE_ACTIVE'
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty}" \
                      f" --action cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            # print(output)
            version_matrix = str(output.decode('utf-8').splitlines())
            version_matrix_split = version_matrix.partition('FW_IMAGE_ACTIVE","')[2]
            cli_active_fw = version_matrix_split.partition('"],[')[0]
            client.close()
        except Exception as e:
            print(e)
            cli_active_fw = "Error"
        return cli_active_fw

    # Method to get the manager state of AP using AP-CLI/ JUMPHOST-CLI
    def get_manager_state(self):
        try:
            client = self.ssh_cli_connect()
            cmd = '/usr/opensync/bin/ovsh s Manager -c | grep status'
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty}" \
                      f" --action cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            status = str(output.decode('utf-8').splitlines())
            # print(output, stderr.read())
            client.close()
        except Exception as e:
            print(e)
            status = "Error"
        return status

    def get_serial_number(self):
        try:
            client = self.ssh_cli_connect()
            cmd = "node | grep serial_number"
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                      f"cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            output = output.decode('utf-8').splitlines()
            serial = output[1].replace(" ", "").split("|")[1]
            client.close()
        except Exception as e:
            print(e)
            serial = "Error"
        return serial

    def get_redirector(self):
        try:
            client = self.ssh_cli_connect()
            cmd = "node | grep redirector_addr"
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                      f"cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            print(output, stderr.read())
            status = output.decode('utf-8').splitlines()
            redirector = status[1].replace(" ", "").split("|")[1]
            client.close()
        except Exception as e:
            print(e)
            redirector = "Error"
        return redirector

    def run_generic_command(self, cmd=""):
        try:
            client = self.ssh_cli_connect()
            cmd = cmd
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                      f"cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            status = output.decode('utf-8').splitlines()
            client.close()
        except Exception as e:
            print(e)
            status = "Error"
        return status

    def get_ucentral_status(self):
        try:
            client = self.ssh_cli_connect()
            cmd = "ubus call ucentral status"
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                      f"cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            print(output)
            if 'latest' not in str(output):
                print("ubus call ucentral status: command has invalid output", str(output))
                connected, latest, active = "Error", "Error1", "Error2"
                return connected, latest, active
            else:
                connected = False
                if "\"connected" in output.decode('utf-8').splitlines()[2]:
                    connected = True
                # connected = output.decode('utf-8').splitlines()[2]
                latest = output.decode('utf-8').splitlines()[3].split(":")[1].replace(" ", "").replace(",", "")
                active = output.decode('utf-8').splitlines()[4].split(":")[1].replace(" ", "").replace(",", "")
            client.close()
        except Exception as e:
            if output.__contains__(b'"connected":'):
                pass
            else:
                pytest.exit("ubus call ucentral status: error" + str(output))
                print(e)
            connected, latest, active = "Error", "Error", "Error"
        return connected, latest, active

    def get_uc_latest_config(self):
        try:
            connected, latest, active = self.get_ucentral_status()
            print()
            client = self.ssh_cli_connect()
            cmd = "cat /etc/ucentral/ucentral.cfg." + latest
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                      f"cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode('utf-8').splitlines()[1]
            print(output)
            json_output = json.loads(output)  # , sort_keys=True)
            print(type(json_output))
            client.close()
        except Exception as e:
            json_output = {}
            print(e)
        return json_output

    def get_uc_active_config(self):
        try:
            connected, latest, active = self.get_ucentral_status()
            client = self.ssh_cli_connect()
            cmd = "cat /etc/ucentral/ucentral.cfg." + active
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                      f"cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode('utf-8').splitlines()[1]
            json_output = json.loads(output)  # , sort_keys=True)
            print(json_output)
            client.close()
        except Exception as e:
            json_output = {}
            print(e)
        return json_output

    def get_interface_details(self):
        r = self.get_wifi_status()
        print(r)
        wifi_info = {}
        if self.sdk == "1.x":
            for i in r:
                for j in r[i]["interfaces"]:
                    encryption = j["config"]["encryption"]
                    if encryption == "psk" or encryption == "psk2" or encryption == "psk-mixed" or \
                            encryption == "sae" or encryption == "sae-mixed":
                        wifi_info[j["ifname"]] = [j["config"]["ssid"], j["config"]["encryption"], j["config"]["key"]]
                    else:
                        wifi_info[j["ifname"]] = [j["config"]["ssid"], j["config"]["encryption"], ""]
            print(wifi_info)
            data = self.get_iwinfo()
            for i in wifi_info.keys():
                wifi_info[i].append(data[i])

            return wifi_info
        if self.sdk == "2.x":
            for i in r:
                for j in r[i]["interfaces"]:
                    encryption = j["config"]["encryption"]
                    if encryption == "psk" or encryption == "psk2" or encryption == "psk-mixed" or \
                            encryption == "sae" or encryption == "sae-mixed":
                        wifi_info[j["ifname"]] = [j["config"]["ssid"], j["config"]["encryption"], j["config"]["key"]]
                    else:
                        wifi_info[j["ifname"]] = [j["config"]["ssid"], j["config"]["encryption"], ""]
            data = self.get_iwinfo()
            print(wifi_info)
            print(data)
            for i in wifi_info.keys():
                wifi_info[i].append(data[i])
            return wifi_info

    def get_wifi_status(self):
        try:

            client = self.ssh_cli_connect()
            cmd = "wifi status"
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                      f"cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)

            output = stdout.read().decode('utf-8')
            data = output.split()
            data.pop(0)
            data.pop(0)
            data.pop(0)
            OUT = "".join(data)
            json_output = json.loads(OUT)
            client.close()
        except Exception as e:
            json_output = False
            print(e)
        return json_output

    def get_iwinfo(self):
        try:
            # [['ssid_wpa2_2g', 'wpa', 'something', '2G'], ['ssid_wpa2_2g', 'wpa', 'something', '5G']]
            # {'wlan0': ['"ssid_wpa3_p_5g"', '12:34:56:78:90:12', '5G'], 'wlan1': ['"ssid_wpa3_p_2g"','00:03:7F:12:34:56', '5G']}
            client = self.ssh_cli_connect()
            cmd = "iwinfo"
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                      f"cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().replace(b":~# iwinfo", b"").decode('utf-8')
            o = output.split()
            iwinfo_bssid_data = {}
            for i in range(len(o)):
                if o[i].__contains__("ESSID"):
                    if o[i + 9].__contains__("2.4"):
                        band = "2G"
                    else:
                        band = "5G"
                    iwinfo_bssid_data[o[i - 1]] = [o[i + 1].replace('"', ''), o[i + 4], band]
            client.close()
        except Exception as e:
            iwinfo_bssid_data = False
            print(e)
        return iwinfo_bssid_data

    def iwinfo(self):
        client = self.ssh_cli_connect()
        cmd = "iwinfo"
        if self.mode:
            cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                  f"cmd --value \"{cmd}\" "
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read().replace(b":~# iwinfo", b"").decode('utf-8')
        o = output
        client.close()
        return o

    def gettxpower(self):
        client = self.ssh_cli_connect()
        cmd = "iw dev | grep txpower"
        if self.mode:
            cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                  f"cmd --value \"{cmd}\" "
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read().replace(b":~# iw dev | grep txpower", b"").decode('utf-8')
        tx_power = output.replace("\t\t", "").split("\r\n")
        tx_power.remove('')
        tx_power.remove('\n')
        cmd = "iw dev | grep Interface"
        if self.mode:
            cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                  f"cmd --value \"{cmd}\" "
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read().replace(b":~# iw dev | grep Interface", b"").decode('utf-8')
        name = output.replace("\t", "").splitlines()
        name.remove('')
        name.pop(-1)
        client.close()
        return tx_power, name

    def get_logread(self, start_ref="", stop_ref=""):
        data = self.logread()
        log_data = []
        data = data.split("\n")
        flag = 0
        for logs in data:
            if logs.__contains__(start_ref):
                flag = 1
            if flag == 1:
                log_data.append(logs)
            if logs.__contains__(stop_ref):
                flag = 0
        ap_logs = "\n".join(log_data)
        return ap_logs

    def logread(self):
        try:
            client = self.ssh_cli_connect()
            cmd = "logread"
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                      f"cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            status = output.decode('utf-8').splitlines()
            logread = status
            logs = ""
            for i in logread:
                logs = logs + i + "\n"
            client.close()
        except Exception as e:
            print(e)
            logs = ""
        return logs

    def get_ap_version_ucentral(self):
        client = self.ssh_cli_connect()
        cmd = "cat /tmp/ucentral.version"
        if self.mode:
            cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                  f"cmd --value \"{cmd}\" "
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read().replace(b":~# cat /tmp/ucentral.version", b"").decode('utf-8')
        client.close()
        return output

    def get_vifc(self):
        client = self.ssh_cli_connect()
        cmd = "vifC"
        if self.mode:
            cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                  f"cmd --value \"{cmd}\" "
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read()
        client.close()
        return output

    def get_vifs(self):
        client = self.ssh_cli_connect()
        cmd = "vifS"
        if self.mode:
            cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                  f"cmd --value \"{cmd}\" "
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read()
        client.close()
        return output

    def get_vlan(self):
        stdout = self.get_vifs()
        vlan_list = []
        for i in stdout.splitlines():
            vlan = str(i.strip()).replace("|", ".").split(".")
            try:
                if not vlan[0].find("b'vlan_id"):
                    vlan_list.append(vlan[1].strip())
            except:
                pass
        return vlan_list

    def get_ap_uci_show_ucentral(self):
        try:
            client = self.ssh_cli_connect()
            cmd = "uci show ucentral"
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                      f"cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            status = output.decode('utf-8').splitlines()
            for i in status:
                if i.startswith("ucentral.config.server="):
                    status = i.split("=")[1]
            client.close()
        except Exception as e:
            print(e)
            status = "Error"
        return status

    def dfs(self):
        if self.type == "wifi5":
            cmd = "cd /sys/kernel/debug/ieee80211/phy1/ath10k/ && echo 1 > dfs_simulate_radar"
            print("cmd: ", cmd)
            if self.mode:
                command = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                          f"cmd --value \"{cmd}\" "
        elif self.type == "wifi6":
            cmd = f'cd  && cd /sys/kernel/debug/ath11k/ && cd ipq* && cd mac0 && ls && echo 1 > dfs_simulate_radar'
            print("cmd: ", cmd)
            if self.mode:
                command = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                          f"cmd --value \"{cmd}\" "
        client = self.ssh_cli_connect()
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read()
        print("hey", output)
        client.close()

    def dfs_logread(self):
        if self.type == "wifi5":
            cmd = "cd /sys/kernel/debug/ieee80211/phy1/ath10k/ && logread | grep DFS"
            print("cmd: ", cmd)
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                      f"cmd --value \"{cmd}\" "
        elif self.type == "wifi6":
            cmd = f'cd  && cd /sys/kernel/debug/ath11k/ && cd ipq* && cd mac0 && logread | grep DFS'
            print("cmd: ", cmd)
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                      f"cmd --value \"{cmd}\" "
        try:
            client = self.ssh_cli_connect()
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            status = output.decode('utf-8').splitlines()
            logread = status[-6:]
            logs = ""
            for i in logread:
                logs = logs + i + "\n"
            client.close()
        except Exception as e:
            print(e)
            logs = ""
        return logs


if __name__ == '__main__':
    obj = {
                "model": "edgecore_eap101",
                "mode": "wifi6",
                "serial": "903cb36ae223",
                "jumphost": True,
                "ip": "10.28.3.103",
                "username": "lanforge",
                "password": "pumpkin77",
                "port": 22,
                "jumphost_tty": "/dev/ttyAP3",
                "version": "release-latest"
            }
    var = APNOS(credentials=obj, sdk="2.x")
    var.run_generic_command(cmd="chmod +x /usr/share/ucentral/wifi_max_user.uc")
    a = var.run_generic_command(cmd="/usr/share/ucentral/wifi_max_user.uc")
    print(a)
