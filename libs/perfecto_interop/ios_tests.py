"""
This file contains functions that represents the Tests we can run on AP using Perfecto real clients
some tests are Client connectivity (For General and Enterprise Security) , Rate Limiting, Captive Portal, MultiPSK
Most of the Functions used are inherited from iOS Libs which consists of Perfecto related Library Functions
Base functions used for all the tests are Wifi_connect and Wifi_disconnect
Wifi_connect is used to connect to a particular ssid that is passed as an argument on the real client
Wifi_disconnect is used to disconnect and forget that particular ssid that is passed as an argument on the real client
get_ip_address is used to get the ip address from the client of the connected ssid
speed_test is used to run the speed test on OOKLA speed test app
"""
from ios_libs import ios_libs


class ios_tests(ios_libs):
    ios_devices = {
        "iPhone-11": {
            "model-iOS": "iPhone-11",
            "bundleId-iOS": "com.apple.Preferences",
            "platformName-iOS": "iOS",
            "bundleId-iOS-Settings": "com.apple.Preferences",
            "bundleId-iOS-Ping": "com.deftapps.ping",
            "browserType-iOS": "Safari",
            "bundleId-iOS-Safari": "com.apple.mobilesafari",
            "platformName-android": "Android",
            "appPackage-android": "com.android.settings",
            "jobName": "Interop-iphone-11",
            "jobNumber": 38
        }
    }

    def __init__(self, perfecto_data=None, dut_data=None, device=None, testcase=None):
        self.perfecto_data = perfecto_data
        self.dut_data = dut_data
        self.device = device
        self.testcase_name = testcase
        self.connData = self.get_ToggleAirplaneMode_data(get_device_configuration=self.perfecto_data[device])

    def client_connect(self, ssid, passkey):
        global ip_address
        self.setup_perfectoMobile = list(self.setup_perfectoMobile_iOS(get_device_configuration=
                                                                       self.perfecto_data[self.device],
                                                                       perfecto_data=self.perfecto_data))
        setup_perfecto_mobile = self.setup_perfectoMobile[0]
        try:
            ssid_with_internet, setup, ssid_found = self.wifi_connect(ssid=ssid, passkey=passkey, setup_perfectoMobile=
                                                      setup_perfecto_mobile, connData=self.connData)
            if ssid_with_internet is not None and ssid_found is True:
                ip_address = self.get_ip_address(ssid, setup, self.connData)
                self.closeApp(self.connData["bundleId-iOS-Settings"], setup)
                self.wifi_disconnect(ssid=ssid, setup_perfectoMobile=setup_perfecto_mobile, connData=self.connData)
                self.teardown()
                print(ip_address, ssid_with_internet)
                if ip_address is not None:
                    return "PASS", "Device got the IP address"
                else:
                    return "FAIL", "Device didn't get the IP address"
                    self.teardown()
            elif ssid_found is False:
                self.teardown()
                return "FAIL", "SSID is not seen in Device"
            else:
                return "FAIL", "SSID didn't get the Internet"
                self.teardown()
        except Exception as e:
            print(e)
            self.teardown()
            return "Fail", "Failed due to exception or Unable to find the API path"

    def enterprise_client_connect(self, ssid, identity, ttls_passwd):
        global ip_address
        self.setup_perfectoMobile = list(self.setup_perfectoMobile_iOS(get_device_configuration=
                                                                       self.perfecto_data[self.device],
                                                                       perfecto_data=self.perfecto_data))
        setup_perfecto_mobile = self.setup_perfectoMobile[0]
        try:
            ssid_with_internet, setup, ssid_found = self.wifi_connect_eap(ssid=ssid, user=identity, ttls_passwd=ttls_passwd,
                                                              setup_perfectoMobile=setup_perfecto_mobile,
                                                              connData=self.connData)
            if ssid_with_internet is not None and ssid_found is True:
                ip_address = self.get_ip_address(ssid, setup, self.connData)
                self.closeApp(self.connData["bundleId-iOS-Settings"], setup)
                self.wifi_disconnect(ssid=ssid, setup_perfectoMobile=setup_perfecto_mobile, connData=self.connData)
                self.teardown()
                print(ip_address, ssid_with_internet)
                if ip_address is not None:
                    return "PASS", "Device got the IP address"
                else:
                    return "FAIL", "Device didn't get the IP address"
                    self.teardown()
            elif ssid_found is False:
                self.teardown()
                return "FAIL", "SSID is not seen in Device"
            else:
                return "FAIL", "SSID didn't get the Internet"
                self.teardown()
        except Exception as e:
            print(e)
            self.teardown()
            return "Fail", "Failed due to exception or Unable to find the API path"

    def client_connectivity_test(self, ssid, security=None, dut_data=None, passkey=None, mode=None, band=None, num_sta=None):
        self.setup_perfectoMobile = list(self.setup_perfectoMobile_iOS(get_device_configuration=
                                                                       self.perfecto_data[self.device],
                                                                       perfecto_data=self.perfecto_data))
        setup_perfecto_mobile = self.setup_perfectoMobile[0]
        try:
            ssid_with_internet, setup, ssid_found = self.wifi_connect(ssid=ssid, passkey=passkey, setup_perfectoMobile=
                                                      setup_perfecto_mobile, connData=self.connData)
            if ssid_with_internet is not None and ssid_found is True:
                self.closeApp(self.connData["bundleId-iOS-Settings"], setup)
                current_result = self.speed_test(setup_perfecto_mobile)
                self.wifi_disconnect(ssid=ssid, setup_perfectoMobile=setup_perfecto_mobile, connData=self.connData)
                self.teardown()
                if current_result is True:
                    return "PASS", "Device connected to SSID and ran Internet speed test"
                else:
                    return "Fail", "Device didn't get connected to SSID"
                    self.teardown()
            elif ssid_found is False:
                self.teardown()
                return "FAIL", "SSID is not seen in Device"
            else:
                return "FAIL", "SSID didn't get the Internet"
                self.teardown()
        except Exception as e:
            print(e)
            self.teardown()
            return "Fail", "Failed due to exception or Unable to find the API path"

    def enterprise_client_connectivity_test(self, ssid, security=None, extra_securities=None, mode=None, band=None,
                                            eap=None, ttls_passwd=None, identity=None, num_sta=None, dut_data=None):
        self.setup_perfectoMobile = list(self.setup_perfectoMobile_iOS(get_device_configuration=
                                                                       self.perfecto_data[self.device],
                                                                       perfecto_data=self.perfecto_data))
        setup_perfecto_mobile = self.setup_perfectoMobile[0]
        try:
            ssid_with_internet, setup, ssid_found = self.wifi_connect_eap(ssid=ssid, user=identity, ttls_passwd=ttls_passwd,
                                                              setup_perfectoMobile=setup_perfecto_mobile,
                                                              connData=self.connData)
            if ssid_with_internet is not None and ssid_found is True:
                self.closeApp(self.connData["bundleId-iOS-Settings"], setup)
                current_result = self.speed_test(setup_perfecto_mobile)
                self.wifi_disconnect(ssid=ssid, setup_perfectoMobile=setup_perfecto_mobile, connData=self.connData)
                self.teardown()
                if current_result is True:
                    return "PASS", "Device connected to SSID and ran Internet speed test"
                else:
                    return "Fail", "Device didn't get connected to SSID"
                    self.teardown()
            elif ssid_found is False:
                self.teardown()
                return "FAIL", "SSID is not seen in Device"
            else:
                return "FAIL", "SSID didn't get the Internet"
                self.teardown()
        except Exception as e:
            print(e)
            self.teardown()
            return "Fail", "Failed due to exception or Unable to find the API path"

    def rate_limiting_test(self, ssid_name, passkey, up_rate, down_rate, instance_name=None, mode=None,download_rate=None,
                           batch_size=None, upload_rate=None, protocol=None, duration=None, move_to_influx=None,
                           dut_data=None, num_stations=None):
        self.setup_perfectoMobile = list(self.setup_perfectoMobile_iOS(get_device_configuration=
                                                                       self.perfecto_data[self.device],
                                                                       perfecto_data=self.perfecto_data))
        setup_perfecto_mobile = self.setup_perfectoMobile[0]
        ssid_with_internet, setup, ssid_found = self.wifi_connect(ssid=ssid_name, passkey=passkey, setup_perfectoMobile=
                                                      setup_perfecto_mobile, connData=self.connData)
        try:
            if ssid_with_internet is not None and ssid_found is True:
                self.closeApp(self.connData["bundleId-iOS-Settings"], setup)
                down_speed, up_speed = self.speed_test(setup_perfecto_mobile)
                self.wifi_disconnect(ssid=ssid_name, setup_perfectoMobile=setup_perfecto_mobile, connData=self.connData)
                self.teardown()
                if down_speed is not None and up_speed is not None:
                    if float(down_speed) < float(down_rate) and float(up_speed) < float(up_rate):
                        return "PASS", "Device connected to SSID and ran rate-limiting test"
                    else:
                        return "Fail", "Failed Rate-limiting test"
                else:
                    return "Fail", "Device didn't get connected to SSID"
                    self.teardown()
            elif ssid_found is False:
                self.teardown()
                return "FAIL", "SSID is not seen in Device"
            else:
                self.teardown()
                return "FAIL", "SSID didn't get the Internet"
        except Exception as e:
            print(e)
            self.teardown()
            return "Fail", "Failed due to exception or Unable to find the API path"

    def toggle_wifi_mode_test(self, ssid, passkey):
        self.setup_perfectoMobile = list(self.setup_perfectoMobile_iOS(get_device_configuration=
                                                                       self.perfecto_data[self.device],
                                                                       perfecto_data=self.perfecto_data))
        setup_perfecto_mobile = self.setup_perfectoMobile[0]
        try:
            ssid_with_internet, setup, ssid_found = self.wifi_connect(ssid=ssid, passkey=passkey,
                                                          setup_perfectoMobile=setup_perfecto_mobile,
                                                          connData=self.connData)
            if ssid_with_internet is not None and ssid_found is True:
                wifi_toggleing = self.toggle_wifi_mode(ssid=ssid, setup_perfectoMobile=setup_perfecto_mobile,
                                                    connData=self.connData)
                self.closeApp(self.connData["bundleId-iOS-Settings"], setup)
                self.wifi_disconnect(ssid=ssid, setup_perfectoMobile=setup_perfecto_mobile, connData=self.connData)
                self.teardown()
                if wifi_toggleing is True:
                    return "PASS", "Connected to same ssid, after toggling the wifi button."
                else:
                    return "FAIL", "Not connected to same ssid, after toggling the wifi button."
            elif ssid_found is False:
                self.teardown()
                return "FAIL", "SSID is not seen in Device"
            else:
                self.teardown()
                return "FAIL", "SSID didn't get the Internet"
        except Exception as e:
            print(e)
            self.teardown()
            return "Fail", "Failed due to exception or Unable to find the API path"

    def enterprise_toggle_wifi_mode_test(self, ssid, identity, ttls_passwd):
        self.setup_perfectoMobile = list(self.setup_perfectoMobile_iOS(get_device_configuration=
                                                                       self.perfecto_data[self.device],
                                                                       perfecto_data=self.perfecto_data))
        setup_perfecto_mobile = self.setup_perfectoMobile[0]
        try:
            ssid_with_internet, setup, ssid_found = self.wifi_connect_eap(ssid=ssid, user=identity,
                                                                          ttls_passwd=ttls_passwd,
                                                                          setup_perfectoMobile=setup_perfecto_mobile,
                                                                          connData=self.connData)
            if ssid_with_internet is not None and ssid_found is True:
                wifi_toggleing = self.toggle_wifi_mode(ssid=ssid, setup_perfectoMobile=setup_perfecto_mobile,
                                                    connData=self.connData)
                self.closeApp(self.connData["bundleId-iOS-Settings"], setup)
                self.wifi_disconnect(ssid=ssid, setup_perfectoMobile=setup_perfecto_mobile, connData=self.connData)
                self.teardown()
                if wifi_toggleing is True:
                    return "PASS", "Connected to same ssid, after toggling the wifi button."
                else:
                    return "FAIL", "Not connected to same ssid, after toggling the wifi button."
            elif ssid_found is False:
                self.teardown()
                return "FAIL", "SSID is not seen in Device"
            else:
                self.teardown()
                return "FAIL", "SSID didn't get the Internet"
        except Exception as e:
            print(e)
            self.teardown()
            return "Fail", "Failed due to exception or Unable to find the API path"

    def toggle_airplane_mode_test(self, ssid, passkey):
        global ip_address
        self.setup_perfectoMobile = list(self.setup_perfectoMobile_iOS(get_device_configuration=
                                                                       self.perfecto_data[self.device],
                                                                       perfecto_data=self.perfecto_data))
        setup_perfecto_mobile = self.setup_perfectoMobile[0]
        try:
            ssid_with_internet, setup, ssid_found = self.wifi_connect(ssid=ssid, passkey=passkey, setup_perfectoMobile=
            setup_perfecto_mobile, connData=self.connData)
            if ssid_with_internet is True and ssid_found is True:
                # ip_address = self.get_ip_address(ssid, setup, self.connData)
                airplane_toggling = self.toggle_airplane_mode(ssid=ssid, setup_perfectoMobile=setup, connData=self.connData)
                self.closeApp(self.connData["bundleId-iOS-Settings"], setup)
                self.wifi_disconnect(ssid=ssid, setup_perfectoMobile=setup_perfecto_mobile, connData=self.connData)
                self.teardown()
                if airplane_toggling is True:
                    return "PASS", "Connected to same ssid, after toggling the airplane button."
                else:
                    return "FAIL", "Not connected to same ssid, after toggling the airplane button."
            elif ssid_found is False:
                self.teardown()
                return "FAIL", "SSID is not seen in Device"
            else:
                self.teardown()
                return "FAIL", "SSID didn't get the Internet"
        except Exception as e:
            print(e)
            self.teardown()
            return "Fail", "Failed due to exception or Unable to find the API path"

    def enterprise_toggle_airplane_mode_test(self, ssid, identity, ttls_passwd):
        global ip_address
        self.setup_perfectoMobile = list(self.setup_perfectoMobile_iOS(get_device_configuration=
                                                                       self.perfecto_data[self.device],
                                                                       perfecto_data=self.perfecto_data))
        setup_perfecto_mobile = self.setup_perfectoMobile[0]
        try:
            ssid_with_internet, setup, ssid_found = self.wifi_connect_eap(ssid=ssid, user=identity,
                                                                          ttls_passwd=ttls_passwd,
                                                                          setup_perfectoMobile=setup_perfecto_mobile,
                                                                          connData=self.connData)
            if ssid_with_internet is True and ssid_found is True:
                airplane_toggling = self.toggle_airplane_mode(ssid=ssid, setup_perfectoMobile=setup, connData=self.connData)
                self.closeApp(self.connData["bundleId-iOS-Settings"], setup)
                self.wifi_disconnect(ssid=ssid, setup_perfectoMobile=setup_perfecto_mobile, connData=self.connData)
                self.teardown()
                if airplane_toggling is True:
                    return "PASS", "Connected to same ssid, after toggling the airplane button."
                else:
                    return "FAIL", "Not connected to same ssid, after toggling the airplane button."
            elif ssid_found is False:
                self.teardown()
                return "FAIL", "SSID is not seen in Device"
            else:
                self.teardown()
                return "FAIL", "SSID didn't get the Internet"
        except Exception as e:
            print(e)
            self.teardown()
            return "Fail", "Failed due to exception or Unable to find the API path"

if __name__ == '__main__':
    perfecto_data = {
        "securityToken": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJpYXQiOjE2MzI4Mzc2NDEsImp0aSI6IjAwZGRiYWY5LWQwYjMtNDRjNS1hYjVlLTkyNzFlNzc5ZGUzNiIsImlzcyI6Imh0dHBzOi8vYXV0aDIucGVyZmVjdG9tb2JpbGUuY29tL2F1dGgvcmVhbG1zL3RpcC1wZXJmZWN0b21vYmlsZS1jb20iLCJhdWQiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwic3ViIjoiODNkNjUxMWQtNTBmZS00ZWM5LThkNzAtYTA0ZjBkNTdiZDUyIiwidHlwIjoiT2ZmbGluZSIsImF6cCI6Im9mZmxpbmUtdG9rZW4tZ2VuZXJhdG9yIiwibm9uY2UiOiI2ZjE1YzYxNy01YTU5LTQyOWEtODc2Yi1jOTQxMTQ1ZDFkZTIiLCJzZXNzaW9uX3N0YXRlIjoiYmRjZTFmYTMtMjlkYi00MmFmLWI5YWMtYjZjZmJkMDEyOTFhIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.5R85_1R38ZFXv_wIjjCIsj8NJm1p66dCsLJI5DBEmks",
        "projectName": "TIP-PyTest-Execution",
        "projectVersion": "1.0",
        "reportTags": "TestTag",
        "perfectoURL": "tip",
        "iPhone-11": {
            "model-iOS": "iPhone-11",
            "bundleId-iOS": "com.apple.Preferences",
            "platformName-iOS": "iOS",
            "bundleId-iOS-Settings": "com.apple.Preferences",
            "bundleId-iOS-Ping": "com.deftapps.ping",
            "browserType-iOS": "Safari",
            "bundleId-iOS-Safari": "com.apple.mobilesafari",
            "platformName-android": "Android",
            "appPackage-android": "com.android.settings",
            "jobName": "Interop-iphone-11",
            "jobNumber": 38
        },
        "iPhone-7": {
            "model-iOS": "iPhone-7",
            "bundleId-iOS": "com.apple.Preferences",
            "platformName-iOS": "iOS",
            "bundleId-iOS-Settings": "com.apple.Preferences",
            "bundleId-iOS-Ping": "com.deftapps.ping",
            "browserType-iOS": "Safari",
            "bundleId-iOS-Safari": "com.apple.mobilesafari",
            "platformName-android": "Android",
            "appPackage-android": "com.android.settings",
            "jobName": "Interop-iphone-7",
            "jobNumber": 38
        }
    }
    access_point = [{
        "model": "edgecore_eap101",
        "supported_bands": ["2G", "5G"],
        "upstream_port": "1.1.eth1",
        "supported_modes": ["BRIDGE", "NAT", "VLAN"],
        "ssid": {
            "2g-ssid": "OpenWifi",
            "5g-ssid": "OpenWifi",
            "6g-ssid": "candela6ghz",
            "2g-password": "OpenWifi",
            "5g-password": "OpenWifi",
            "6g-password": "hello123",
            "2g-encryption": "WPA2",
            "5g-encryption": "open",
            "6g-encryption": "WPA3",
            "2g-bssid": "68:7d:b4:5f:5c:31 ",
            "5g-bssid": "68:7d:b4:5f:5c:3c",
            "6g-bssid": "68:7d:b4:5f:5c:38"
        },
        "mode": "wifi6",
        "identifier": "903cb36ae255",
        "serial_port": True,
        "host_ip": "10.28.3.102",
        "host_username": "lanforge",
        "host_password": "pumpkin77",
        "host_ssh_port": 22,
        "serial_tty": "/dev/ttyAP5",
        "firmware_version": "next-latest"
    }]
    obj = ios_tests(perfecto_data=perfecto_data, dut_data=access_point,device="iPhone-7",
                    testcase="Test_perfecto_check")
    # print(obj.client_connectivity_test(ssid="ssid_wpa2_2g_RL_E3V2240", passkey="something"))
    # print(obj.rate_limiting_test(ssid="ssid_wpa2_2g_RL_1VE7537",passkey="something",up_rate="60",down_rate="10"))
    #print(obj.enterprise_client_connect(ssid="ssid_wpa2_eap_5g", identity="nolaradius", ttls_passwd="nolastart"))
    print(obj.enterprise_toggle_wifi_mode_test(ssid="ssid_wpa_eap_5g_5O05610", identity="nolaradius",
                                               ttls_passwd="nolastart"))
