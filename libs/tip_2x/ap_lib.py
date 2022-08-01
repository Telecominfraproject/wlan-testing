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

    def check_serial_connection(self):
        status = []
        for dut in self.device_under_tests_data:
            if dut["method"] == "serial":
                status.append(self.setup_library_objects[0].check_serial_connection(tty=dut["serial_tty"]))
        if False in status:
            logging.error("Serial port not available. Exiting the Test")
            pytest.exit("Serial port not available. Please check your serial port connection")

    def setup_serial_environment(self):
        status = []
        for dut in self.device_under_tests_data:
            if dut["method"] == "serial":
                status.append(self.setup_library_objects[0].setup_serial_environment())
        if False in status:
            logging.error("Serial port not available. Exiting the Test")
            pytest.exit("Serial port not available. Please check your serial port connection")

    def get_dut_logs(self, idx=0, print_log=True, attach_allure=True):
        output = self.run_generic_command(cmd="logread", idx=idx,
                                          print_log=print_log,
                                          attach_allure=attach_allure,
                                          expected_attachment_type=allure.attachment_type.TEXT)
        return output

    def check_connectivity(self, idx=0, print_log=True, attach_allure=True):
        maverick_status = self.run_generic_command(cmd="/etc/init.d/maverick status", idx=idx,
                                                   print_log=print_log,
                                                   attach_allure=attach_allure,
                                                   expected_attachment_type=allure.attachment_type.TEXT)
        if maverick_status.__contains__("running"):
            logging.error("Maverick is running!!!")
            # Maverick check is happening
            # TODO: add the steps to diagnose the maverick reason, check certificates, wan ip address,
            #  check the partition for certificates and check the /certificates dir. Also check if any of the cert is
            #  missing, if anything is missing, then report that. if everything looks good, please check md5sum of certs
            #  also, try to do a reboot in case everything looks good and post reboot, check the maverick status.
            #  Jitendra
            pytest.exit("Maverick is running, Please check the wan connection and certificates")
        check_iface = self.run_generic_command(cmd="ifconfig up0v0", idx=idx,
                                               print_log=print_log,
                                               attach_allure=attach_allure,
                                               expected_attachment_type=allure.attachment_type.TEXT)
        if check_iface.__contains__("error fetching interface information: Device not found"):
            logging.error(check_iface)
            pytest.exit("up0v0 interface is not available!!!")

        output = self.run_generic_command(cmd="ip neigh show dev up0v0 REACHABLE", idx=idx,
                                          print_log=print_log,
                                          attach_allure=attach_allure,
                                          expected_attachment_type=allure.attachment_type.TEXT)

        if output.__contains__("INCOMPLETE") or output.__contains__("FAILED"):
            logging.error(output)
            pytest.exit("up0v0 interface is failed to have connectivity!!!")

    def get_uci_show(self, param="ucentral", idx=0, print_log=True, attach_allure=True):
        output = self.run_generic_command(cmd="uci show " + param, idx=idx,
                                          print_log=print_log,
                                          attach_allure=attach_allure,
                                          expected_attachment_type=allure.attachment_type.TEXT)

        return output

    def ubus_call_ucentral_status(self, idx=0, print_log=True, attach_allure=True):
        ret_val = dict.fromkeys(["connected", "latest", "active"])
        print(ret_val)
        output = self.run_generic_command(cmd="ubus call ucentral status", idx=idx,
                                          print_log=print_log,
                                          attach_allure=attach_allure,
                                          expected_attachment_type=allure.attachment_type.JSON)
        try_again = False
        try:
            data = dict(json.loads(output.replace("\n\t", "").replace("\n", "")))
        except Exception as e:
            logging.error("error in converting the ubus call ucentral status output to json" + output)
            try_again = True
        if try_again or len(data.keys()) != 3:
            output = self.run_generic_command(cmd="ubus call ucentral status", idx=idx,
                                              print_log=print_log,
                                              attach_allure=attach_allure,
                                              expected_attachment_type=allure.attachment_type.JSON)
            try:
                data = dict(json.loads(output.replace("\n\t", "").replace("\n", "")))
            except Exception as e:
                logging.error("error in converting the ubus call ucentral status output to json" + output)
        if data.keys().__contains__("connected"):
            ret_val["connected"] = True
        if data.keys().__contains__("disconnected"):
            ret_val["connected"] = False
        if data.keys().__contains__("latest"):
            ret_val["latest"] = data.get("latest")
        if data.keys().__contains__("active"):
            ret_val["active"] = data.get("active")

        print(ret_val)
        return ret_val

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

    def run_generic_command(self, cmd="", idx=0, print_log=True, attach_allure=False,
                            expected_attachment_type=allure.attachment_type.TEXT):
        input_command = cmd
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
                    "identifier"] + ":~# " + " -s serial --log stdout --user root --passwd openwifi"
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {owrt_args} -t {self.device_under_tests_data[idx]['serial_tty']} --action " \
                      f"cmd --value \"{cmd}\" "
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            status = output.decode('utf-8').splitlines()
            status.pop(0)
            final_output = '\n'.join(status)
            if print_log:
                logging.info("Output for command: " + input_command + "\n" + final_output)
            if attach_allure:
                allure.attach(name=input_command, body=output, attachment_type=expected_attachment_type)
            client.close()
        except Exception as e:
            logging.error(e)
            final_output = "Error" + str(e)
        return final_output

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
            "host_password": "pumpkin77",  # Endurance@123
            "host_ssh_port": 22,
            "serial_tty": "/dev/ttyAP1",
            "firmware_version": "next-latest"
        }],
        "traffic_generator": {}
    }
    obj = APLIBS(dut_data=basic_1["device_under_tests"])
    # obj.check_serial_connection()
    # obj.setup_serial_environment()
    # obj.run_generic_command("uci show ucentral")
    # obj.get_dut_logs()
    obj.ubus_call_ucentral_status()
