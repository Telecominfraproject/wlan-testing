import importlib
import logging

import paramiko
import pytest

setup_lib = importlib.import_module("SetupLibrary")
SetupLibrary = setup_lib.SetupLibrary


class APLIBS:
    setup_library_objects = list()
    device_under_tests_data = None

    def __init__(self, dut_data=None):
        if dut_data is None:
            logging.error("Device Under Test Data is Not Specified, Please provide valid DUT Data")
            pytest.exit("Device Under Test Data is Not Specified, Please provide valid DUT Data")
        if type(dut_data) is not list:
            logging.error("Device Under Test Data is Not in list format, Please provide valid DUT Data in list format")
            pytest.exit("Device Under Test Data is Not in list format, Please provide valid DUT Data in list format")
        self.device_under_tests_data = dut_data
        for dut in self.device_under_tests_data:
            self.setup_library_objects.append(SetupLibrary(remote_ip=dut["host_ip"],
                                                           remote_ssh_port=dut["host_ssh_port"],
                                                           remote_ssh_username=dut["host_username"],
                                                           remote_ssh_password=dut["host_password"],
                                                           pwd=""))

    def ssh_cli_connect(self, ip="",
                        port=22,
                        username="",
                        password="",
                        timeout=10,
                        allow_agent=False,
                        banner_timeout=200):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password,
                       port=port, timeout=timeout, allow_agent=allow_agent, banner_timeout=banner_timeout)
        return client

    def check_serial_connection(self):
        status = []
        for dut in self.device_under_tests_data:
            if dut["method"] == "serial":
                status.append(self.setup_library_objects[0].check_serial_connection(tty=dut["serial_tty"]))
        if False in status:
            logging.error("Serial port not available. Exiting the Test")
            pytest.exit("Serial port not available. Please check your serial port connection")

    def get_dut_logs(self, idx=0):
        pass

    def check_wan_connectivity(self, idx=0):
        pass

    def get_uci_show(self, idx=0):
        pass

    def get_uci_show_ucentral(self, idx=0):
        pass

    def check_ubus_call_ucentral_status(self, idx=0):
        pass

    def get_latest_config_recieved(self, idx=0):
        pass

    def get_active_config(self, idx=0):
        pass

    def get_iwinfo(self, idx=0):
        pass

    def get_ifconfig(self, idx=0):
        pass

    def verify_certificates(self, idx=0):
        pass

    def run_generic_command(self, cmd="", idx=0):
        status = True
        for dut in self.device_under_tests_data:
            try:
                client = self.ssh_cli_connect(ip=dut["host_ip"],
                                              port=dut["host_ssh_port"],
                                              username=dut["host_username"],
                                              password=dut["host_password"],
                                              timeout=10,
                                              allow_agent=False,
                                              banner_timeout=200)
                cmd = cmd
                if dut["method"] == "serial":
                    owrt_args = "--prompt root@" + dut["identifier"] + " -s serial --log stdout --user root --passwd openwifi"
                    cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {owrt_args} -t {dut['serial_tty']} --action " \
                          f"cmd --value \"{cmd}\" "
                stdin, stdout, stderr = client.exec_command(cmd)
                output = stdout.read()
                status = output.decode('utf-8').splitlines()
                print(output)
                client.close()
            except Exception as e:
                print(e)
                status = "Error"
        return status

    def get_status(self, idx=0):
        pass

    def exit_from_uboot(self, idx=0):
        pass

    def is_console_uboot(self, idx=0):
        pass

    def is_prompt_available(self, idx=0):
        pass

    def reboot(self, idx=0):
        pass

    def get_active_firmware(self, idx=0):
        pass


if __name__ == '__main__':
    basic_1 = {
        "target": "tip_2x",
        "controller": {
            "url": "https://sec-qa01.cicd.lab.wlan.tip.build:16001",
            "username": "tip@ucentral.com",
            "password": "OpenWifi%123"
        },
        "device_under_tests": [{
            "model": "cig_wf188n",
            "supported_bands": ["2G", "5G"],
            "supported_modes": ["BRIDGE", "NAT", "VLAN"],
            "mode": "wifi6",
            "identifier": "0000c1018812",
            "method": "serial",  # serial/ssh/telnet
            "host_ip": "10.28.3.103",
            "host_username": "lanforge",
            "host_password": "pumpkin77",
            "host_ssh_port": 22,
            "serial_tty": "/dev/ttyAP1",
            "firmware_version": "next-latest"
        }],
        "traffic_generator": {}
    }
    obj = APLIBS(dut_data=basic_1["device_under_tests"])
    obj.run_generic_command("uci show ucentral")
    # obj.setup_serial_environment()
    # obj.check_serial_connection(tty="/dev/ttyUSB0")
    # obj.kill_all_minicom_process(tty="/dev/ttyUSB0")
