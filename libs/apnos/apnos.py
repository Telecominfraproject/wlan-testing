import paramiko

class APNOS:

    def __init__(self, jumphost_cred=None):
        self.owrt_args = "--prompt root@OpenAp -s serial --log stdout --user root --passwd openwifi"
        if jumphost_cred is None:
            exit()
        self.jumphost_ip = jumphost_cred['jumphost_ip'] # "192.168.200.80"
        self.jumphost_username =jumphost_cred['jumphost_username'] # "lanforge"
        self.jumphost_password = jumphost_cred['jumphost_password'] # "lanforge"
        self.jumphost_port = jumphost_cred['jumphost_port'] # 22


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
        cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (
            '/home', self.owrt_args, '/dev/ttyAP1', 'iwinfo')
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read()
        client.close()
        return output


    def get_vif_config(self):
        client = self.ssh_cli_connect()
        cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (
            '/home', self.owrt_args, '/dev/ttyAP1', "/usr/opensync/bin/ovsh s Wifi_VIF_Config -c")
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read()
        client.close()
        return output


    def get_vif_state(self):
        client = self.ssh_cli_connect()
        cmd = "cd %s/lanforge/lanforge-scripts/ && ./openwrt_ctl.py %s -t %s --action cmd --value \"%s\"" % (
            '/home', self.owrt_args, '/dev/ttyAP1', "/usr/opensync/bin/ovsh s Wifi_VIF_State -c")
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


APNOS_CREDENTIAL_DATA = {
        'jumphost_ip': "192.168.200.80",
        'jumphost_username': "lanforge",
        'jumphost_password': "lanforge",
        'jumphost_port': 22
}
obj = APNOS(jumphost_cred=APNOS_CREDENTIAL_DATA)
print(obj.get_vif_config_ssids())
# print(get_vif_config_ssids())
# print(get_vif_state_ssids())
