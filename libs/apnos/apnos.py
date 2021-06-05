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
from scp import SCPClient
import os
import allure


class APNOS:

    def __init__(self, credentials=None, pwd=os.getcwd()):
        allure.attach(name="APNOS LIbrary: ", body=str(credentials))
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
            client = self.ssh_cli_connect()
            cmd = '[ -f ~/cicd-git/ ] && echo "True" || echo "False"'
            stdin, stdout, stderr = client.exec_command(cmd)
            if str(stdout.read()).__contains__("False"):
                cmd = 'mkdir ~/cicd-git/'
                client.exec_command(cmd)
            cmd = '[ -f ~/cicd-git/openwrt_ctl.py ] && echo "True" || echo "False"'
            stdin, stdout, stderr = client.exec_command(cmd)
            if str(stdout.read()).__contains__("False"):
                print("Copying openwrt_ctl serial control Script...")
                with SCPClient(client.get_transport()) as scp:
                    scp.put(pwd + 'openwrt_ctl.py', '~/cicd-git/openwrt_ctl.py')  # Copy my_file.txt to the server
            cmd = '[ -f ~/cicd-git/openwrt_ctl.py ] && echo "True" || echo "False"'
            stdin, stdout, stderr = client.exec_command(cmd)
            var = str(stdout.read())
            if var.__contains__("True"):
                allure.attach(name="openwrt_ctl Setup", body=str(var))
                print("APNOS Serial Setup OK")
            else:
                allure.attach(name="openwrt_ctl Setup", body=str(var))
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
        allure.attach(name="AP Reboot", body=str(output))
        return output

    # Method to get the iwinfo status of AP using AP-CLI/ JUMPHOST-CLI
    def iwinfo_status(self):
        client = self.ssh_cli_connect()
        cmd = 'iwinfo'
        if self.mode:
            cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                  f"cmd --value \"{cmd}\" "
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read()
        allure.attach(body=str("VIF Config: " + str(vif_config) + "\n" + "VIF State: " + str(vif_state)),
                      name="SSID Profiles in VIF Config and VIF State: ")
        client.close()
        allure.attach(name="iwinfo Output Msg: ", body=str(output))
        allure.attach(name="iwinfo config Err Msg: ", body=str(stderr))
        return output

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
        allure.attach(name="vif config Output Msg: ", body=str(output))
        allure.attach(name="vif config Err Msg: ", body=str(stderr))

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
        allure.attach(name="vif state Output Msg: ", body=str(output))
        allure.attach(name="vif state Err Msg: ", body=str(stderr))
        return output

    # Method to get the vif_config ssid's of AP using AP-CLI/ JUMPHOST-CLI
    def get_vif_config_ssids(self):
        stdout = self.get_vif_config()
        ssid_list = []
        for i in stdout.splitlines():
            ssid = str(i).replace(" ", "").split(".")
            if ssid[0].split(":")[0] == "b'ssid":
                ssid_list.append(ssid[0].split(":")[1].replace("'", ""))
        allure.attach(name="get_vif_config_ssids ", body=str(ssid_list))
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
                info.append(security)
                if security != "OPEN":
                    security_key = ssid[0].split(":")[1].split(",")[4].replace('"', "").replace("]", "")
                    info.append(security_key)
            if ssid[0].split(":")[0] == "b'ssid":
                info.append(ssid[0].split(":")[1].replace("'", ""))
                ssid_info_list.append(info)
                info = []
        print(ssid_info_list)
        # allure.attach(name="get_vif_state_ssids ", body=str(ssid_list))
        return ssid_info_list

    # Get VIF State parameters
    def get_vif_state_ssids(self):
        stdout = self.get_vif_state()
        ssid_list = []
        for i in stdout.splitlines():
            ssid = str(i).replace(" ", "").split(".")
            if ssid[0].split(":")[0] == "b'ssid":
                ssid_list.append(ssid[0].split(":")[1].replace("'", ""))
        allure.attach(name="get_vif_state_ssids ", body=str(ssid_list))
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
            allure.attach(name="get_active_firmware - Exception ", body=str(e))
            cli_active_fw = "Error"
        allure.attach(name="get_active_firmware ", body=str(cli_active_fw))
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
            allure.attach(name="get_active_firmware - Exception ", body=str(e))
            status = "Error"
        allure.attach(name="get_active_firmware ", body=str(status))
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
            allure.attach(name="get_serial_number output ", body=str(stderr))
            serial = output[1].replace(" ", "").split("|")[1]
            client.close()
        except Exception as e:
            print(e)
            allure.attach(name="get_serial_number - Exception ", body=str(e))
            serial = "Error"
        allure.attach(name="get_serial_number ", body=str(serial))
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
            status = output.decode('utf-8').splitlines()
            allure.attach(name="get_redirector output ", body=str(stderr))
            redirector = status[1].replace(" ", "").split("|")[1]
            client.close()
        except Exception as e:
            print(e)
            allure.attach(name="get_redirector - Exception ", body=str(e))
            redirector = "Error"
        allure.attach(name="get_redirector ", body=redirector)
        return redirector

    def run_generic_command(self, cmd=""):
        allure.attach(name="run_generic_command ", body=cmd)
        try:
            client = self.ssh_cli_connect()
            cmd = cmd
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t {self.tty} --action " \
                      f"cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)
            input = stdin.read().decode('utf-8').splitlines()
            output = stdout.read().decode('utf-8').splitlines()
            error = stderr.read().decode('utf-8').splitlines()
            client.close()
        except Exception as e:
            print(e)
            allure.attach(name="run_generic_command - Exception ", body=str(e))
            input = "Error"
            output = "Error"
            error = "Error"
        allure.attach(name="run_generic_command ", body=input)
        allure.attach(name="run_generic_command ", body=str(output))
        allure.attach(name="run_generic_command ", body=error)
        return [input, output, error]


if __name__ == '__main__':
    obj = {
        'jumphost': True,
        'ip': "192.168.80.99",
        'username': "lanforge",
        'password': "lanforge",
        'port': 22,
        'jumphost_tty': '/dev/ttyAP1',

    }
    var = APNOS(credentials=obj)
    r = var.get_ssid_info()
    print(r)