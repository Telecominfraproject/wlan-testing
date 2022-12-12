import importlib
import json
import logging

import allure
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

    def run_generic_command(self, cmd="", idx=0, print_log=True, attach_allure=False,
                            expected_attachment_type=allure.attachment_type.TEXT):
        input_command = cmd
        logging.info("Executing Command on AP: " + cmd)
        try:
            self.setup_library_objects[idx].kill_all_minicom_process(
                tty=self.device_under_tests_data[idx]["serial_tty"])
            client = self.ssh_cli_connect(ip=self.device_under_tests_data[idx]["host_ip"],
                                          port=self.device_under_tests_data[idx]["host_ssh_port"],
                                          username=self.device_under_tests_data[idx]["host_username"],
                                          password=self.device_under_tests_data[idx]["host_password"],
                                          timeout=10,
                                          allow_agent=False,
                                          banner_timeout=200)
            if self.device_under_tests_data[idx]["method"] == "serial":
                owrt_args = "--prompt root@" + self.device_under_tests_data[idx][
                    "identifier"] + " -s serial --log stdout --user root --passwd openwifi"
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {owrt_args} -t {self.device_under_tests_data[idx]['serial_tty']} --action " \
                      f"cmd --value \"{cmd}\" "
                if print_log:
                    logging.info(cmd)
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            final_output = str(output)
            if not output.__contains__(b"BOOTLOADER-CONSOLE-IPQ6018#"):
                status = output.decode('utf-8').splitlines()
                status.pop(0)
                final_output = '\n'.join(status)
                if print_log:
                    logging.info(cmd)
                    logging.info("Output for command: " + input_command + "\n" + final_output)
                if attach_allure:
                    allure.attach(name=input_command, body=output, attachment_type=expected_attachment_type)
            client.close()
        except Exception as e:
            logging.error(e)
            final_output = "Error: " + str(e)
        return final_output

    def example_function(self, idx=0, print_log=True, attach_allure=True):
        output = self.run_generic_command(cmd="example_command", idx=idx,
                                          print_log=print_log,
                                          attach_allure=attach_allure,
                                          expected_attachment_type=allure.attachment_type.TEXT)
        return output





if __name__ == '__main__':
    basic_05 = {
        "target": "dut_lib_template",
        "controller": {
            "url": "https://sec-qa01.cicd.lab.wlan.tip.build:16001",
            "username": "tip@ucentral.com",
            "password": "OpenWifi%123"
        },
        "device_under_tests": [{
            "model": "cig_wf188n",
            "supported_bands": ["2G", "5G"],
            "supported_modes": ["BRIDGE", "NAT", "VLAN"],
            "wan_port": "1.1.eth2",
            "lan_port": None,
            "ssid": {
                "2g-ssid": "OpenWifi",
                "5g-ssid": "OpenWifi",
                "6g-ssid": "OpenWifi",
                "2g-password": "OpenWifi",
                "5g-password": "OpenWifi",
                "6g-password": "OpenWifi",
                "2g-encryption": "WPA2",
                "5g-encryption": "WPA2",
                "6g-encryption": "WPA3",
                "2g-bssid": "68:7d:b4:5f:5c:31",
                "5g-bssid": "68:7d:b4:5f:5c:3c",
                "6g-bssid": "68:7d:b4:5f:5c:38"
            },
            "mode": "wifi6",
            "identifier": "0000c1018812",
            "method": "serial",
            "host_ip": "localhost",
            "host_username": "lanforge",
            "host_password": "pumpkin77",
            "host_ssh_port": 8842,
            "serial_tty": "/dev/ttyAP1",
            "firmware_version": "next-latest"
        }],
        "traffic_generator": {
            "name": "lanforge",
            "testbed": "basic",
            "scenario": "dhcp-bridge",
            "details": {
                "manager_ip": "localhost",
                "http_port": 8840,
                "ssh_port": 8841,
                "setup": {"method": "build", "DB": "Test_Scenario_Automation"},
                "wan_ports": {
                    "1.1.eth2": {"addressing": "dhcp-server", "subnet": "172.16.0.1/16", "dhcp": {
                        "lease-first": 10,
                        "lease-count": 10000,
                        "lease-time": "6h"
                    }
                                 }
                },
                "lan_ports": {

                },
                "uplink_nat_ports": {
                    "1.1.eth1": {
                        "addressing": "static",
                        "ip": "10.28.2.16",
                        "gateway_ip": "10.28.2.1/24",
                        "ip_mask": "255.255.255.0",
                        "dns_servers": "BLANK"
                    }
                }
            }
        }
    }
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.NOTSET)
    obj = APLIBS(dut_data=basic_05["device_under_tests"])
    # obj.exit_from_uboot()
    # obj.setup_serial_environment()

    # obj.verify_certificates()
    # obj.get_dut_logs()
    # l = obj.get_latest_config_recieved()
    # a = obj.get_active_config()
    # if a == l:
    #     print("a = l")
    # print(obj.get_ap_version())
