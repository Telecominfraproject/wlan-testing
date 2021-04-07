import paramiko


class APNOS:

    def __init__(self, credentials=None):
        self.owrt_args = "--prompt root@OpenAp -s serial --log stdout --user root --passwd openwifi"
        if credentials is None:
            exit()
        self.jumphost_ip = credentials['ip']  # "192.168.200.80"
        self.jumphost_username = credentials['username']  # "lanforge"
        self.jumphost_password = credentials['password']  # "lanforge"
        self.jumphost_port = credentials['port']  # 22
        self.mode = credentials['mode']  # 1 for jumphost, 0 for direct ssh

    def ssh_cli_connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("Connecting to jumphost: %s@%s:%s with password: %s" % (
            self.jumphost_username, self.jumphost_ip, self.jumphost_port, self.jumphost_password))
        client.connect(self.jumphost_ip, username=self.jumphost_username, password=self.jumphost_password,
                       port=self.jumphost_port, timeout=10, allow_agent=False, banner_timeout=200)

        return client

    def iwinfo_status(self):
        client = self.ssh_cli_connect()
        if self.mode == 1:
            cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (
                '/home', self.owrt_args, '/dev/ttyAP1', 'iwinfo')
        else:
            cmd = 'iwinfo'
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read()
        client.close()
        return output

    def get_vif_config(self):
        client = self.ssh_cli_connect()
        if self.mode == 1:
            cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (
                '/home', self.owrt_args, '/dev/ttyAP1', "/usr/opensync/bin/ovsh s Wifi_VIF_Config -c")
        else:
            cmd = "/usr/opensync/bin/ovsh s Wifi_VIF_Config -c"
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read()
        client.close()
        return output

    def get_vif_state(self):
        client = self.ssh_cli_connect()
        if self.mode == 1:
            cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (
                '/home', self.owrt_args, '/dev/ttyAP1', "/usr/opensync/bin/ovsh s Wifi_VIF_State -c")
        else:
            cmd = "/usr/opensync/bin/ovsh s Wifi_VIF_State -c"
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read()
        client.close()
        return output

    def get_vif_config_ssids(self):
        stdout = self.get_vif_config()
        ssid_list = []
        for i in stdout.splitlines():
            ssid = str(i).replace(" ", "").split(".")
            if ssid[0].split(":")[0] == "b'ssid":
                ssid_list.append(ssid[0].split(":")[1].replace("'", ""))
        return ssid_list

    def get_vif_state_ssids(self):
        stdout = self.get_vif_state()
        ssid_list = []
        for i in stdout.splitlines():
            ssid = str(i).replace(" ", "").split(".")
            if ssid[0].split(":")[0] == "b'ssid":
                ssid_list.append(ssid[0].split(":")[1].replace("'", ""))
        return ssid_list

    def get_active_firmware(self):
        try:
            client = self.ssh_cli_connect()
            if self.mode == 1:
                cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (
                    '/home', self.owrt_args, '/dev/ttyAP1', '/usr/opensync/bin/ovsh s AWLAN_Node -c | grep FW_IMAGE_ACTIVE')
            else:
                cmd = '/usr/opensync/bin/ovsh s AWLAN_Node -c | grep FW_IMAGE_ACTIVE'
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            # print(output)
            version_matrix = str(output.decode('utf-8').splitlines())
            version_matrix_split = version_matrix.partition('FW_IMAGE_ACTIVE","')[2]
            cli_active_fw = version_matrix_split.partition('"],[')[0]
            client.close()
        except Exception as e:
            cli_active_fw = "Error"
        return cli_active_fw

    def get_manager_state(self):
        try:
            client = self.ssh_cli_connect()
            if self.mode == 1:
                cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (
                    '/home', self.owrt_args, '/dev/ttyAP1', '/usr/opensync/bin/ovsh s Manager -c | grep status')
            else:
                cmd = '/usr/opensync/bin/ovsh s Manager -c | grep status'
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            status = str(output.decode('utf-8').splitlines())
            client.close()
        except Exception as e:
            status = "Error"
        return status

    def get_status(self):
        client = self.ssh_cli_connect()
        if self.mode == 1:
            cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (
                '/home', self.owrt_args, '/dev/ttyAP1', "/usr/opensync/bin/ovsh s Wifi_VIF_State -c")
        else:
            cmd = "/usr/opensync/bin/ovsh s Wifi_VIF_State -c"
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read()
        client.close()
        return output
        pass
#
# APNOS_CREDENTIAL_DATA = {
#         'jumphost_ip': "192.168.200.80",
#         'jumphost_username': "lanforge",
#         'jumphost_password': "lanforge",
#         'jumphost_port': 22
#         'mode': 1
# }
# mode can me 1 for ap direct ssh, and 0 for jumphost
# obj = APNOS(jumphost_cred=APNOS_CREDENTIAL_DATA)
# print(obj.get_active_firmware())
# print(obj.get_vif_config_ssids())
# print(get_vif_config_ssids())
# print(get_vif_state_ssids())
