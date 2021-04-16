"""
APNOS Library : Used to execute SSH Commands in AP Using Direct-AP-SSH/ Jumphost-Serial Console

Currently Having Methods:
    1. Get iwinfo
    2. AP Manager Satus
    3. Vif Config ssid's
    4. Vif State ssid's
    5. Get current Firmware

"""

import paramiko


class APNOS:

    def __init__(self, credentials=None):
        self.owrt_args = "--prompt root@OpenAp -s serial --log stdout --user root --passwd openwifi"
        if credentials is None:
            print("No credentials Given")
            exit()
        self.ip = credentials['ip']  # if mode=1, enter jumphost ip else ap ip address
        self.username = credentials['username']  # if mode=1, enter jumphost username else ap username
        self.password = credentials['password']  # if mode=1, enter jumphost password else ap password
        self.port = credentials['port']  # if mode=1, enter jumphost ssh port else ap ssh port
        self.mode = credentials['jumphost']  # 1 for jumphost, 0 for direct ssh
        if self.mode:
            self.tty = credentials['jumphost_tty']  # /dev/ttyAP1

    # Method to connect AP-CLI/ JUMPHOST-CLI
    def ssh_cli_connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("Connecting to jumphost: %s@%s:%s with password: %s" % (
            self.username, self.ip, self.port, self.password))
        client.connect(self.ip, username=self.username, password=self.password,
                       port=self.port, timeout=10, allow_agent=False, banner_timeout=200)

        return client

    # Method to get the iwinfo status of AP using AP-CLI/ JUMPHOST-CLI
    def iwinfo_status(self):
        client = self.ssh_cli_connect()
        cmd = 'iwinfo'
        if self.mode:
            cmd = f"cd /home/lanforge/lanforge-scripts/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                  f"cmd --value \"{cmd}\" "
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read()
        client.close()
        return output

    # Method to get the vif_config of AP using AP-CLI/ JUMPHOST-CLI
    def get_vif_config(self):
        client = self.ssh_cli_connect()
        cmd = "/usr/opensync/bin/ovsh s Wifi_VIF_Config -c"
        if self.mode:
            cmd = f"cd /home/lanforge/lanforge-scripts/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
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
            cmd = f"cd /home/lanforge/lanforge-scripts/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
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
                cmd = f"cd /home/lanforge/lanforge-scripts/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty}" \
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
                cmd = f"cd /home/lanforge/lanforge-scripts/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty}" \
                      f" --action cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            status = str(output.decode('utf-8').splitlines())
            client.close()
        except Exception as e:
            print(e)
            status = "Error"
        return status

