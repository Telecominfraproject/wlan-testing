"""
This class consists of functions which checks the schema of the configuration for lab
Whether the schema contains all the necessary key-value pairs or not
If not it will inform the required key-value pair
"""
import logging
import re

class SchemaCheck:
    global target_var, dut_keys, tg_keys, testbed_name
    target_var = "tip_2x"
    testbed_name = 'basic'

    def __init__(self, configuration=None):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        self.configuration = configuration
        self.testbed_list = None
        self.len_testbed_list = None
        self.key_check_arr = ['target', 'controller', 'device_under_tests', 'traffic_generator']

    def set_data(self):
        """
        This Function sets the value of how many testbeds are there in the schema input file and stores the number of it
        """
        testbed_list = []
        for key in self.configuration:
            print(key)
            testbed_list.append(key)
        print(testbed_list)
        self.testbed_list = testbed_list
        self.len_testbed_list = len(testbed_list)

    def key_check(self):
        """
        This fun checks the keys of the testbeds present in schema such as target, controller, DUT, traffic generator
        """
        arr = []
        for a in range(self.len_testbed_list):
            for key in self.configuration[self.testbed_list[a]]:
                print(key)
                arr.append(key)
            print(arr)
            if arr == self.key_check_arr:
                arr.clear()
                print("All keys are present in the schema for Testbed")
                logging.info("All keys are present in the schema for Testbed")
            else:
                arr.clear()
                logging.error("Not all the keys required present in schema for Testbed")

    def target_check(self):
        """
        This function checks the global target we have declared is matching in the schema or not
        """
        global target_var
        for a in range(self.len_testbed_list):
            if self.configuration[self.testbed_list[a]]['target'] == target_var:
                logging.info("Target is matching")
            else:
                logging.error("Target variable is not matching")

    def controller_check(self):
        """
        This func checks the keys of Controller such as Url, Username and password
        """
        arr = ['url', 'username', 'password']
        lis = []
        for a in range(self.len_testbed_list):
            for key in self.configuration[self.testbed_list[a]]['controller']:
                lis.append(key)
            print(self.testbed_list[a], '->', lis)
            if lis == arr:
                lis.clear()
                print("All keys are present in the Controller data of schema")
                logging.info("All keys are present in the Controller data of schema")
            else:
                lis.clear()
                logging.error("Not all the Controller keys required present in schema")

    def dut_keys_check(self):
        """
        This func checks DUT keys if every key is present in the schema or not
        """
        global dut_keys
        arr, arr2, arr3 = [], [], []
        dut_keys = ['model', 'supported_bands', 'supported_modes', 'wan_port', 'lan_port', 'ssid', 'mode', 'identifier',
                    'method', 'host_ip', 'host_username', 'host_password', 'host_ssh_port', 'serial_tty',
                    'firmware_version']
        for a in range(self.len_testbed_list):
            for b in range(len(self.configuration[self.testbed_list[a]]['device_under_tests'])):
                for key in self.configuration[self.testbed_list[a]]['device_under_tests'][b]:
                    arr.append(key)
                arr2 = list(set(dut_keys) - set(arr))
                arr3.append(arr2)
                # print(arr3)
                arr.clear()
        for a in range(len(arr3)):
            if len(arr3[a]) == 0:
                logging.info("All keys of DUT are present")
                self.dut_values_check()
            elif len(arr3[a]) == 1:
                if arr3[a][0] == 'ssid':
                    logging.warning("Ssid key is not present", self.testbed_list[a], '->', arr3[a])
                    self.dut_values_check()
                else:
                    logging.error("Required keys of DUT are not present, Please include those", self.testbed_list[a],
                                  '->', arr3[a])
            else:
                logging.error("Not all Keys of DUT required are present", self.testbed_list[a], '->', arr3[a])

    def dut_values_check(self):
        """
        This func checks whether all the values of DUT Keys are valid or not. Use it after dut_keys_check()
        """
        global dut_keys
        print("DUT Key->value Check")
        for a in range(self.len_testbed_list):
            for b in range(len(self.configuration[self.testbed_list[a]]['device_under_tests'])):
                for key, value in self.configuration[self.testbed_list[a]]['device_under_tests'][b].items():
                    # print(key, value)
                    # print(type(value))
                    if key == 'model':
                        if type(value) == str:
                            logging.info("Model key->values are present and eligible")
                        else:
                            logging.error("Model key->values which are present are not eligible", key, '->', value)
                    elif key == 'supported_bands':
                        if type(value) == list:
                            logging.info("Supported bands key->values are present and eligible")
                        else:
                            logging.error("Supported bands key->values which are present are not eligible", key, '->',
                                          value)
                    elif key == 'supported_modes':
                        if type(value) == list:
                            logging.info("Supported modes key->values are present and eligible")
                        else:
                            logging.error("Supported modes key->values which are present are not eligible", key, '->',
                                          value)
                    elif key == 'wan_port':
                        if type(value) == str:
                            logging.info("Wan port key->values are present and eligible")
                        else:
                            logging.error("Wan port key->values which are present are not eligible", key, '->',
                                          value)
                    elif key == 'lan_port':
                        if value is None or type(value) == str:
                            logging.info("Lan port key->values are present and eligible")
                        else:
                            logging.error("Lan port key->values which are present are not eligible", key, '->',
                                          value)
                    elif key == 'ssid':
                        if type(value) == dict:
                            self.ssid_data_check()
                            logging.info("Ssid key->values are present and eligible")
                        else:
                            logging.error("Ssid  key->values which are present are not eligible", key, '->',
                                          value)
                    elif key == 'mode':
                        if type(value) == str:
                            logging.info("Mode key->values are present and eligible")
                        else:
                            logging.error("Mode key->values which are present are not eligible", key, '->',
                                          value)
                    elif key == 'identifier':
                        if type(value) == str and type(value) is not None:
                            logging.info("Identifier key->values are present and eligible")
                        else:
                            logging.error("Identifier key->values which are present are not eligible", key, '->',
                                          value)
                    elif key == 'method':
                        if type(value) == str and (value == 'serial' or value == 'ssh' or value == 'telnet'):
                            logging.info("Method key->values are present and eligible")
                        else:
                            logging.error("Method key->values which are present are not eligible", key, '->',
                                          value)
                    elif key == 'host_ip':
                        if type(value) == str:
                            logging.info("Host IP key->values are present and eligible")
                        else:
                            logging.error("Host IP key->values which are present are not eligible", key, '->',
                                          value)
                    elif key == 'host_username':
                        if type(value) == str:
                            logging.info("Host Username key->values are present and eligible")
                        else:
                            logging.error("Host Username key->values which are present are not eligible", key, '->',
                                          value)
                    elif key == 'host_password':
                        if type(value) == str:
                            logging.info("Host Password key->values are present and eligible")
                        else:
                            logging.error("Host Password key->values which are present are not eligible", key, '->',
                                          value)
                    elif key == 'host_ssh_port':
                        if type(value) == int:
                            logging.info("Host ssh Port key->values are present and eligible")
                        else:
                            logging.error("Host ssh Port key->values which are present are not eligible", key, '->',
                                          value)
                    elif key == 'serial_tty':
                        if type(value) == str:
                            logging.info("Serial tty key->values are present and eligible")
                        else:
                            logging.error("Serial tty key->values which are present are not eligible", key, '->',
                                          value)
                    elif key == 'firmware_version':
                        if type(value) == str:
                            logging.info("Firmware version key->values are present and eligible")
                        else:
                            logging.error("Firmware version key->values which are present are not eligible", key, '->',
                                          value)

    def traffic_generator_keys_check(self):
        """
        THis Func checks the Traffic generator keys are present in the schema or not. It should be called after
        dut_values_check()
        """
        global tg_keys
        tg_keys = ['name', 'testbed', 'scenario', 'details']
        lis = []
        for count in range(self.len_testbed_list):
            for key in self.configuration[self.testbed_list[count]]['traffic_generator']:
                lis.append(key)
            print(self.testbed_list[count], '->', lis)
            if lis == tg_keys:
                lis.clear()
                print("All keys are present in the Traffic generator data of schema")
                logging.info("All keys are present in the Traffic generator data of schema")
                self.traffic_generator_values_check(count)
            else:
                lis.clear()
                logging.error("Not all the Traffic generator keys required are present in schema")

    def ssid_data_check(self):
        """
        This func has to check the Ssid data check in DUT values if SSid key is present in it
        """
        pass

    def traffic_generator_values_check(self, count):
        """
        This func validates the traffic generator values and is called from traffic_generator_keys_check() after 
        keys are checked
        """
        global testbed_name
        logging.info("Traffic generator Key->value check")
        for key, value in self.configuration[self.testbed_list[count]]['traffic_generator'].items():
            if key == 'name':
                if type(value) == str:
                    logging.info("Name key->value are present and Eligible")
                else:
                    logging.error("Name key->values which are present are not eligible", key, '->',
                                  value)
            elif key == 'testbed':
                if type(value) == str and value == testbed_name:
                    logging.info("Testbed key->value are present and Eligible")
                else:
                    logging.error("Testbed key->values which are present are not eligible", key, '->',
                                  value)
            elif key == 'scenario':
                if type(value) == str and (value == 'dhcp-bridge' or value == 'dhcp-external'):
                    logging.info("Scenario key->value are present and Eligible")
                else:
                    logging.error("Scenario key->values which are present are not eligible", key, '->',
                                  value)
            elif key == 'details':
                if type(value) == dict:
                    self.tg_details_data_keys_check(count)
                    logging.info("Details key->value are present and Eligible")
                else:
                    logging.error("Details key->values which are present are not eligible", key, '->',
                                  value)

    def tg_details_data_keys_check(self, count):
        """
        This Func checks the Details data keys of Traffic generator and is called in traffic_generator_values_check()
        after details key is validated there for further validation of details dict
        """
        global tg_details_keys
        tg_details_keys = ['manager_ip', 'http_port', 'ssh_port', 'setup', 'wan_ports', 'lan_ports', 'uplink_nat_ports']
        lis = []
        for key in self.configuration[self.testbed_list[count]]['traffic_generator']['details']:
            lis.append(key)
        print(self.testbed_list[count], '->', lis)
        if lis == tg_details_keys:
            lis.clear()
            print("All keys are present in the Traffic generator Details data of schema")
            logging.info("All keys are present in the Traffic generator Details data of schema")
            self.tg_details_values_check(count)
        else:
            lis.clear()
            logging.error("Not all the Traffic generator Details keys required are present in schema")

    def tg_details_values_check(self, count):
        """
        This Func validates the Details data Values of Traffic generator and is called in tg_details_data_keys_check()
        after details keys are validated
        """
        logging.info("Traffic generator Key->value check")
        for key, value in self.configuration[self.testbed_list[count]]['traffic_generator']['details'].items():
            if key == 'manager_ip':
                if type(value) == str:
                    logging.info("Manager ip  key->value are present and Eligible")
                else:
                    logging.error("Manager ip key->values which are present are not eligible", key, '->',
                                  value)
            elif key == 'http_port':
                if type(value) == int:
                    logging.info("Http port  key->value are present and Eligible")
                else:
                    logging.error("Http port key->values which are present are not eligible", key, '->',
                                  value)
            elif key == 'ssh_port':
                if type(value) == int:
                    logging.info("Ssh port  key->value are present and Eligible")
                else:
                    logging.error("Ssh port key->values which are present are not eligible", key, '->',
                                  value)
            elif key == 'setup':
                if type(value) == dict:
                    key2 = self.configuration[self.testbed_list[count]]['traffic_generator']['details']['setup']
                    value2 = self.configuration[self.testbed_list[count]]['traffic_generator']['details']['setup']['method']
                    if key2 == 'method':
                        if type(value2) == str:
                            if value2 == 'build':
                                logging.info("Method - Build key->value are present and Eligible")
                            elif value2 == 'load':
                                if key2['DB'] == str:
                                    logging.info("Method - Load key->value are present and Eligible")
                        else:
                            logging.error("Method key->values which are present are not eligible", key,
                                          '->',
                                          value)
                    logging.info("Setup  key->value are present and Eligible")
                else:
                    logging.error("Setup key->values which are present are not eligible", key, '->',
                                  value)
            elif key == 'wan_ports':
                if type(value) == dict:
                    self.tg_ports_data_keys_check(key, count)
                else:
                    logging.error("Wan Ports data is not eligible")
            elif key == 'lan_ports':
                if type(value) == dict:
                    # self.tg_ports_data_keys_check(key, count)
                    pass
                else:
                    logging.error("Lan Ports data is not eligible")
            elif key == 'uplink_nat_ports':
                if type(value) == dict:
                    self.tg_ports_data_keys_check(key, count)
                else:
                    logging.error("Uplink nat Ports data is not eligible")

    def tg_ports_data_keys_check(self, key, count):
        """
        This Func validates the Ports data Values of Traffic generator and is called in tg_details_values_check()
        after details values are validated. It will check for patterns like 1.1.eth2
        """
        ports = self.configuration[self.testbed_list[count]]['traffic_generator']['details'][key]
        print("Data of ---------------", key)
        print(ports)
        for key1, value1 in ports.items():
            if type(key1) == str and type(value1) == dict:
                x = re.search("\d.\d.", key1)
                if x is not None:
                    logging.info("Key of", key, "->", key1, "is eligible")
                    self.tg_ports_addressing_check(value1)
                else:
                    logging.error("Key of", key, "->", key1, "is not eligible")
            else:
                logging.error("Key of", key, "->", key1, "is not eligible and is not a string")

    @staticmethod
    def tg_ports_addressing_check(value):
        """
        This function checks the addressing data if values present has ip address pattern or not. It is called in
        tg_ports_data_keys_check()
        """
        print("Value--------------")
        print(value)
        if value['addressing'] == 'static':
            for key, value2 in value.items():
                if key == 'ip':
                    value2 = re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", value2)
                    if value2 is not None:
                        logging.info("Ip is present and eligible in ports")
                elif key == 'gateway_ip':
                    value2 = re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d*$", value2)
                    if value2 is not None:
                        logging.info("Gateway Ip is present and eligible in ports")
                elif key == 'ip_mask':
                    value2 = re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", value2)
                    if value2 is not None:
                        logging.info("Ip Mask is present and eligible in ports")
                elif key == 'dns_servers' and type(value2) == str:
                    logging.info("DNS server is present and eligible in ports")
                elif key == 'addressing':
                    logging.info("Skipping Addressing ,As it is already verified")
                else:
                    logging.error("Please look into the Ports data")
        elif value['addressing'] == 'dynamic':
            pass
        elif value['addressing'] == 'dhcp-server':
            for key, value2 in value.items():
                if key == 'ip':
                    value2 = re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", value2)
                    if value2 is not None:
                        logging.info("Ip is present and eligible in ports")
                elif key == 'gateway_ip':
                    value2 = re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d*$", value2)
                    if value2 is not None:
                        logging.info("Gateway Ip is present and eligible in ports")
                elif key == 'ip_mask':
                    value2 = re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", value2)
                    if value2 is not None:
                        logging.info("Ip Mask is present and eligible in ports")
                elif key == 'dns_servers' and type(value2) == str:
                    logging.info("DNS server is present and eligible in ports")
                elif key == 'addressing':
                    logging.info("Skipping Addressing ,As it is already verified")
                else:
                    logging.error("Please look into the Ports data")


if __name__ == '__main__':
    var = {
        "CONFIGURATION": {
            'basic-06': {
                'target': 'tip_2x',
                'controller': {
                    'url': 'https://sec-qa01.cicd.lab.wlan.tip.build:16001',
                    'username': 'tip@ucentral.com',
                    'password': 'OpenWifi%123'
                },
                'device_under_tests': [{
                    'model': 'edgecore_eap102',  # Will be string
                    'supported_bands': ['2G', '5G'],  # ['2G', '5G', '6G']
                    'supported_modes': ['BRIDGE', 'NAT', 'VLAN'],  # Will remain same
                    'wan_port': '1.1.eth2',  # Has to be
                    'lan_port': None,  # Has to be null or none
                    'ssid': {  # Has to be seperate func
                        '2g-ssid': 'OpenWifi',
                        '5g-ssid': 'OpenWifi',
                        '6g-ssid': 'OpenWifi',
                        '2g-password': 'OpenWifi',
                        '5g-password': 'OpenWifi',
                        '6g-password': 'OpenWifi',
                        '2g-encryption': 'WPA2',
                        '5g-encryption': 'WPA2',
                        '6g-encryption': 'WPA3',
                        '2g-bssid': '68:7d:b4:5f:5c:31',
                        '5g-bssid': '68:7d:b4:5f:5c:3c',
                        '6g-bssid': '68:7d:b4:5f:5c:38'
                    },
                    'mode': 'wifi6',  # ['wifi5', 'wifi6', 'wifi6e']
                    'identifier': '903cb39d6918',  # Has to be not Null
                    'method': 'serial',  # Has to be serial, ssh, telnet
                    'host_ip': 'localhost',  # Ip or localhost
                    'host_username': 'lanforge',  # Str
                    'host_password': 'pumpkin77',  # Str
                    'host_ssh_port': 8852,  # Int
                    'serial_tty': '/dev/ttyAP2',  # Str
                    'firmware_version': 'next-latest'  # Str
                }],
                'traffic_generator': {
                    'name': 'lanforge',  # STR
                    'testbed': 'basic',  # [basic, ]
                    'scenario': 'dhcp-bridge',  # dhcp-bridge, dhcp-external
                    'details': {
                        'manager_ip': 'localhost',  # Str or ip
                        'http_port': 8850,  # int
                        'ssh_port': 8851,  # int
                        'setup': {'method': 'build', 'DB': 'Test_Scenario_Automation'},
                        # Method-> build/load, if load-> DB
                        'wan_ports': {  # addressing(dhcp-server, static, dynamic) Subnet-> ip/ cannot be eth2(1.1.eth2)
                            '1.1.eth2': {'addressing': 'dhcp-server', 'subnet': '172.16.0.1/16', 'dhcp': {  # DICT
                                'lease-first': 10,  # int
                                'lease-count': 10000,  # int
                                'lease-time': '6h'  # str
                            }
                                         }
                        },
                        'lan_ports': {

                        },
                        'uplink_nat_ports': {
                            '1.1.eth3': {
                                'addressing': 'static',  # If static -> need ip, g_ip, ip_mask, dns
                                'ip': '10.28.2.17',
                                'gateway_ip': '10.28.2.1/24',
                                'ip_mask': '255.255.255.0',
                                'dns_servers': 'BLANK'
                            }
                        }
                    }
                }
            },
            "advance-03": {
                "target": "tip_2x",
                "controller": {
                    "url": "https://sec-qa01.cicd.lab.wlan.tip.build:16001",
                    "username": "tip@ucentral.com",
                    "password": "OpenWifi%123"
                },
                "device_under_tests": [{
                    "model": "cig_wf196",
                    "supported_bands": ["2G", "5G", "6G"],
                    "supported_modes": ["BRIDGE", "NAT", "VLAN"],
                    "wan_port": "1.3.eth2",
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
                    "mode": "wifi6e",
                    "identifier": "824f816011e4",
                    "method": "serial",
                    "host_ip": "localhost",
                    "host_username": "lanforge",
                    "host_password": "pumpkin77",
                    "host_ssh_port": 8902,
                    "serial_tty": "/dev/ttyAP0",
                    "firmware_version": "next-latest"
                }],
                "traffic_generator": {
                    "name": "lanforge",
                    "testbed": "basic",
                    "scenario": "dhcp-bridge",
                    "details": {
                        "manager_ip": "10.28.3.117",
                        "http_port": 8900,
                        "ssh_port": 8901,
                        "setup": {"method": "build", "DB": "Test_Scenario_Automation"},
                        "wan_ports": {
                            "1.3.eth2": {"addressing": "dhcp-server", "subnet": "172.16.0.1/16", "dhcp": {
                                "lease-first": 10,
                                "lease-count": 10000,
                                "lease-time": "6h"
                            }
                                         }
                        },
                        "lan_ports": {

                        },
                        "uplink_nat_ports": {
                            "1.3.eth3": {
                                "addressing": "static",
                                "ip": "10.28.2.39",
                                "gateway_ip": "10.28.2.1/24",
                                "ip_mask": "255.255.255.0",
                                "dns_servers": "BLANK"
                            }
                        }
                    }
                }
            }
        }
    }
    obj = SchemaCheck(var["CONFIGURATION"])
    obj.set_data()
    obj.key_check()
    obj.target_check()
    obj.controller_check()
    obj.dut_keys_check()
    obj.traffic_generator_keys_check()
