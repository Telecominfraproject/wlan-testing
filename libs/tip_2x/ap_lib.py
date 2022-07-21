import importlib
import json
import logging
import random
import string
import time

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

    def check_serial_connection(self, idx=0, print_log=True, attach_allure=True):
        status = False

        if self.device_under_tests_data[idx]["method"] == "serial":
            status = self.setup_library_objects[idx].check_serial_connection(
                tty=self.device_under_tests_data[idx]["serial_tty"])
        if not status:
            logging.error("Serial port not available. Exiting the Test")
            pytest.exit("Serial port not available. Please check your serial port connection")

    def setup_serial_environment(self, idx=0):
        status = []
        for dut in self.device_under_tests_data:
            if dut["method"] == "serial":
                status.append(self.setup_library_objects[idx].setup_serial_environment())
        if False in status:
            logging.error("Serial port not available. Exiting the Test")
            pytest.exit("Serial port not available. Please check your serial port connection")
        self.exit_from_uboot(idx=idx)
        self.reset_to_default(idx=idx)

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
            # pytest.exit("Maverick is running, Please check the wan connection and certificates")
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
            pytest.fail("up0v0 interface is failed to have connectivity!!!")

    def get_uci_show(self, param="ucentral", idx=0, print_log=True, attach_allure=True):
        output = self.run_generic_command(cmd="uci show " + param, idx=idx,
                                          print_log=print_log,
                                          attach_allure=attach_allure,
                                          expected_attachment_type=allure.attachment_type.TEXT)

        return output

    def restart_ucentral_service(self, idx=0, print_log=True, attach_allure=True):
        output = self.run_generic_command(cmd="/etc/init.d/ucentral restart", idx=idx,
                                          print_log=print_log,
                                          attach_allure=attach_allure,
                                          expected_attachment_type=allure.attachment_type.TEXT)

        return output

    def ubus_call_ucentral_status(self, idx=0, print_log=True, attach_allure=True, retry=5):
        ret_val = dict.fromkeys(["connected", "latest", "active"])
        for i in range(0, retry):
            ret_val = dict.fromkeys(["connected", "latest", "active"])
            output = self.run_generic_command(cmd="ubus call ucentral status", idx=idx,
                                              print_log=print_log,
                                              attach_allure=attach_allure,
                                              expected_attachment_type=allure.attachment_type.JSON)

            try:
                data = dict(json.loads(output.replace("\n\t", "").replace("\n", "")))
            except Exception as e:
                logging.error("error in converting the ubus call ucentral status output to json" + output)
                data = {}
            if (data.keys().__contains__("connected") or data.keys().__contains__("disconnected")) and \
                data.keys().__contains__("latest") and \
                data.keys().__contains__("active"):
                break
            else:
                logging.error("Error in ubus call ucentral status: " + str(output))

        if data.keys().__contains__("connected"):
            ret_val["connected"] = True
        if data.keys().__contains__("disconnected"):
            ret_val["connected"] = False
        if data.keys().__contains__("latest"):
            ret_val["latest"] = data.get("latest")
        if data.keys().__contains__("active"):
            ret_val["active"] = data.get("active")
        return ret_val

    def get_latest_config_recieved(self, idx=0, print_log=True, attach_allure=True):
        r_val = self.ubus_call_ucentral_status(idx=idx)
        latest_json = {}
        if r_val["latest"] is None:
            r_val = self.ubus_call_ucentral_status(idx=idx)
            if r_val["latest"] is None:
                logging.error("ubus call ucentral status has unexpected data")
                return False
        latest_uuid = r_val["latest"]
        output = self.run_generic_command(cmd="cat /etc/ucentral/ucentral.cfg." + str(latest_uuid), idx=idx,
                                          print_log=print_log,
                                          attach_allure=attach_allure,
                                          expected_attachment_type=allure.attachment_type.JSON)
        try:
            data = dict(json.loads(output.replace("\n\t", "").replace("\n", "")))
            logging.info("Latest config is : " + str(data))
            allure.attach(name="cat /etc/ucentral/ucentral.cfg." + str(latest_uuid),
                          body=str(json.dumps(data, indent=2)),
                          attachment_type=allure.attachment_type.JSON)
        except Exception as e:
            data = output
            logging.error("error in converting the output to json" + output)
            try_again = True
            allure.attach(name="cat /etc/ucentral/ucentral.cfg." + str(latest_uuid),
                          body=str(data),
                          attachment_type=allure.attachment_type.JSON)

        return latest_json

    def get_active_config(self, idx=0, print_log=True, attach_allure=False):
        r_val = self.ubus_call_ucentral_status(idx=idx)
        active_json = {}
        if r_val["active"] is None:
            r_val = self.ubus_call_ucentral_status(idx=idx)
            if r_val["active"] is None:
                logging.error("ubus call ucentral status has unexpected data")
                return False
        active_uuid = r_val["active"]
        output = self.run_generic_command(cmd="cat /etc/ucentral/ucentral.cfg." + str(active_uuid), idx=idx,
                                          print_log=print_log,
                                          attach_allure=attach_allure,
                                          expected_attachment_type=allure.attachment_type.JSON)
        try:
            data = dict(json.loads(output.replace("\n\t", "").replace("\n", "")))
            logging.info("Active config is : " + str(data))
            allure.attach(name="cat /etc/ucentral/ucentral.cfg." + str(active_uuid),
                          body=str(json.dumps(data, indent=2)),
                          attachment_type=allure.attachment_type.JSON)
        except Exception as e:
            data = output
            logging.error("error in converting the output to json" + output)
            try_again = True
            allure.attach(name="cat /etc/ucentral/ucentral.cfg." + str(active_uuid),
                          body=str(data),
                          attachment_type=allure.attachment_type.JSON)
        print(data)

        return active_json

    def get_iwinfo(self, idx=0, print_log=True, attach_allure=True):

        # [['ssid_wpa2_2g', 'wpa', 'something', '2G'], ['ssid_wpa2_2g', 'wpa', 'something', '5G']] {'wlan0': [
        # '"ssid_wpa3_p_5g"', '12:34:56:78:90:12', '5G'], 'wlan1': ['"ssid_wpa3_p_2g"','00:03:7F:12:34:56', '5G']}
        iwinfo_output = self.run_generic_command(cmd="iwinfo", idx=idx,
                                                 print_log=print_log,
                                                 attach_allure=attach_allure,
                                                 expected_attachment_type=allure.attachment_type.TEXT)

        return iwinfo_output

    def get_bssid_band_mapping(self, idx=0):
        data = self.get_iwinfo(idx=idx)
        data = str(data).replace(" ", "").split("\n")
        band_info = []
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

    def get_ifconfig(self, idx=0):
        pass

    def verify_certificates(self, idx=0, print_log=False, attach_allure=False):
        cert_files_name = ["cas.pem", "dev-id", "key.pem", "cert.pem"]
        for cert in cert_files_name:
            output = self.run_generic_command(cmd='[ -f /etc/ucentral/' + cert + ' ] && echo "True" || echo "False"',
                                              idx=idx,
                                              print_log=print_log,
                                              attach_allure=attach_allure,
                                              expected_attachment_type=allure.attachment_type.JSON)
            if output == "False":
                logging.error("Certificate " + cert + "is missing from /etc/ucentral/ directory. "
                                                      "Please add valid certificates on AP")
                pytest.exit("Certificate " + cert + "is missing from /etc/ucentral/ directory. "
                                                    "Please add valid certificates on AP")

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

    def get_status(self, idx=0):
        pass

    def exit_from_uboot(self, idx=0):
        if self.is_console_uboot():
            self.run_generic_command(cmd="reset-from-console", idx=idx,
                                     print_log=True,
                                     attach_allure=True,
                                     expected_attachment_type=allure.attachment_type.JSON)

    def is_console_uboot(self, idx=0):
        output = self.run_generic_command(cmd="ubus call ucentral status", idx=idx,
                                          print_log=True,
                                          attach_allure=True,
                                          expected_attachment_type=allure.attachment_type.JSON)
        if output.__contains__("BOOTLOADER-CONSOLE-IPQ6018#"):
            return True
        else:
            return False

    def is_autoreboot_running(self):
        # TODO : Jitendra/Shivam
        pass

    def reboot(self, idx=0):
        output = self.run_generic_command(cmd="reboot", idx=idx,
                                          print_log=False,
                                          attach_allure=False,
                                          expected_attachment_type=allure.attachment_type.JSON)
        return output

    def get_active_firmware(self, idx=0):
        pass

    def reset_to_default(self, idx=0):
        self.run_generic_command(cmd="cd", idx=idx,
                                 print_log=False,
                                 attach_allure=False,
                                 expected_attachment_type=allure.attachment_type.JSON)

    def get_wifi_status(self, idx=0, print_log=True, attach_allure=True):
        output = self.run_generic_command(cmd="wifi status", idx=idx,
                                          print_log=print_log,
                                          attach_allure=attach_allure,
                                          expected_attachment_type=allure.attachment_type.JSON)

        try_again = False
        try:
            data = dict(json.loads(output.replace("\n\t", "").replace("\n", "")))
        except Exception as e:
            data = output
            logging.error("error in converting the ubus call ucentral status output to json" + output)
            try_again = True
        if try_again or len(data.keys()) != 3:
            output = self.run_generic_command(cmd="wifi status", idx=idx,
                                              print_log=print_log,
                                              attach_allure=attach_allure,
                                              expected_attachment_type=allure.attachment_type.JSON)
            try:
                data = dict(json.loads(output.replace("\n\t", "").replace("\n", "")))
            except Exception as e:
                data = output
                logging.error("error in converting the ubus call ucentral status output to json" + output)
        ret_val = data
        return ret_val

    def get_ap_version(self, idx=0, print_log=True, attach_allure=False):
        output = self.run_generic_command(cmd="cat /tmp/ucentral.version", idx=idx,
                                          print_log=print_log,
                                          attach_allure=attach_allure,
                                          expected_attachment_type=allure.attachment_type.JSON)
        return output

    def get_logread(self, start_ref="", stop_ref="", idx=0, print_log=False, attach_allure=False):
        output = self.run_generic_command(cmd="logread", idx=idx,
                                          print_log=print_log,
                                          attach_allure=attach_allure,
                                          expected_attachment_type=allure.attachment_type.JSON)
        log_data = []
        data = output.split("\n")
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

    def dfs(self, idx=0, print_log=True, attach_allure=False):
        type_ = self.device_under_tests_data[idx]["mode"]
        cmd = None
        if type_.lower() == "wifi5":
            cmd1 = '[ -f /sys/kernel/debug/ieee80211/phy1/ath10k/dfs_simulate_radar ] && echo "True" || echo "False"'
            output = self.run_generic_command(cmd=cmd1, idx=idx,
                                              print_log=print_log,
                                              attach_allure=attach_allure,
                                              expected_attachment_type=allure.attachment_type.JSON)

            ret = output.split("\n")
            status_count = int(ret.count("True"))
            logging.info("Status count: " + str(status_count))
            if status_count == 1:
                cmd = "cd && cd /sys/kernel/debug/ieee80211/phy1/ath10k/ && echo 1 > dfs_simulate_radar"
            else:
                cmd = "cd && cd /sys/kernel/debug/ieee80211/phy0/ath10k/ && echo 1 > dfs_simulate_radar"
        elif type_.lower() == "wifi6" or type_.lower() == "wifi6e":
            cmd = f'cd  && cd /sys/kernel/debug/ath11k/ && cd ipq* && cd mac0 && ls && echo 1 > dfs_simulate_radar'
        output = self.run_generic_command(cmd=cmd, idx=idx,
                                          print_log=print_log,
                                          attach_allure=attach_allure,
                                          expected_attachment_type=allure.attachment_type.JSON)
        return output

    def dfs_logread(self, idx=0, print_log=True, attach_allure=False):
        """get simulate radar command logs"""
        type_ = self.device_under_tests_data[idx]["mode"]
        if type_.lower() == "wifi5":
            cmd1 = '[ -f /sys/kernel/debug/ieee80211/phy1/ath10k/dfs_simulate_radar ] && echo "True" || echo "False"'
            output = self.run_generic_command(cmd=cmd1, idx=idx,
                                              print_log=print_log,
                                              attach_allure=attach_allure,
                                              expected_attachment_type=allure.attachment_type.JSON)
            logging.info("DFS logread output: " + str(output))
            if output.__contains__("False"):
                cmd = "cd /sys/kernel/debug/ieee80211/phy0/ath10k/ && logread | grep DFS"
            else:
                cmd = "cd /sys/kernel/debug/ieee80211/phy1/ath10k/ && logread | grep DFS"
            # cmd = "cd /sys/kernel/debug/ieee80211/phy1/ath10k/ && logread | grep DFS"
            # print("cmd: ", cmd)
        elif type_.lower() == "wifi6" or type_.lower() == "wifi6e":
            cmd = f'cd  && cd /sys/kernel/debug/ath11k/ && cd ipq* && cd mac0 && logread | grep DFS'
        try:
            output = self.run_generic_command(cmd=cmd, idx=idx,
                                              print_log=print_log,
                                              attach_allure=attach_allure,
                                              expected_attachment_type=allure.attachment_type.JSON)
            ret = output.split("\n")
            logread = ret[-6:]
            logs = ""
            for i in logread:
                logs = logs + i + "\n"
        except Exception as e:
            print(e)
            logs = ""
        logging.info("Simulate radar logs: " + str(logs))
        return logs


if __name__ == '__main__':
    basic= {
        "target": "tip_2x",
        "controller": {
            "url": "https://sec-qa01.cicd.lab.wlan.tip.build:16001",
            "username": "tip@ucentral.com",
            "password": "OpenWifi%123"
        },
        "device_under_tests": [{
            "model": "edgecore_eap101",
            "supported_bands": ["2G", "5G"],
            "supported_modes": ["BRIDGE", "NAT", "VLAN"],
            "wan_port": "1.1.eth3",
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
            "identifier": "903cb36c4301",
            "method": "serial",
            "host_ip": "192.168.52.89",
            "host_username": "lanforge",
            "host_password": "lanforge",
            "host_ssh_port": 22,
            "serial_tty": "/dev/ttyUSB0",
            "firmware_version": "next-latest"
        }],
        "traffic_generator": {
            "name": "lanforge",
            "testbed": "basic",
            "scenario": "dhcp-bridge",
            "details": {
                "manager_ip": "192.168.52.89",
                "http_port": 8080,
                "ssh_port": 22,
                "setup": {"method": "build", "DB": "Test_Scenario_Automation"},
                "wan_ports": {
                    "1.1.eth3": {"addressing": "dhcp-server", "subnet": "172.16.0.1/16", "dhcp": {
                        "lease-first": 10,
                        "lease-count": 10000,
                        "lease-time": "6h"
                    }
                                 }
                },
                "lan_ports": {

                },
                "uplink_nat_ports": {
                    "1.1.eth2": {
                        "addressing": "static",
                        "ip": "192.168.52.150",
                        "gateway_ip": "192.168.52.1/24",
                        "ip_mask": "255.255.255.0",
                        "dns_servers": "BLANK"
                    }
                }
            }
        }
    }
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.NOTSET)
    obj = APLIBS(dut_data=basic["device_under_tests"])
    obj.ubus_call_ucentral_status()
    # obj.exit_from_uboot()
    # obj.setup_serial_environment()

    # obj.verify_certificates()
    # obj.get_dut_logs()
    # l = obj.get_latest_config_recieved()
    # a = obj.get_active_config()
    # if a == l:
    #     print("a = l")
    # print(obj.get_ap_version())


