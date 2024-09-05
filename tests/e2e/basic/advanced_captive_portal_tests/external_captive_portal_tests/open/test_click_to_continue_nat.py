"""

    External Captive Portal Test: NAT Mode
    pytest -m "external_captive_portal_tests and NAT"

"""
import logging
import re
import time
import allure
import paramiko
import pytest
from tabulate import tabulate

pytestmark = [pytest.mark.external_captive_portal_tests, pytest.mark.NAT, pytest.mark.advanced_captive_portal_tests]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid_ext_cap_portal_open_2g_ctc", "appliedRadios": ["2G"], "security_key": "something",
             "captive": {
                 "auth-mode": "uam",
                 "uam-port": 3990,
                 "uam-secret": "hotsys123",
                 "uam-server": "https://customer.hotspotsystem.com/customer/hotspotlogin.php",
                 "nasid": "AlmondLabs",
                 "auth-server": "radius.hotspotsystem.com",
                 "auth-port": 1812,
                 "auth-secret": "hotsys123",
                 "walled-garden-fqdn": [
                     "*.google.com",
                     "telecominfraproject.com",
                     "customer.hotspotsystem.com",
                     "youtube.com"
                 ]
             }
             }
        ]},
    "rf": {},
    "radius": False
}


@allure.feature("Advanced Captive Portal Test")
@allure.parent_suite("Advanced Captive Portal Tests")
@allure.suite(suite_name="External Captive Portal")
@allure.sub_suite(sub_suite_name="NAT Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestNatModeExternalCaptivePortal(object):
    """
            External Captive Portal Test: NAT Mode
            pytest -m "advanced_captive_portal_tests and NAT and external_captive_portal_tests"
    """

    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.click_to_continue
    @pytest.mark.ow_regression_lf
    @allure.title("Click-to-continue mode with open encryption 2.4 GHz Band NAT mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-14124", name="WIFI-14124")
    def test_nat_open_2g_click_to_continue(self, get_test_library, get_dut_logs_per_test_case,
                                              get_test_device_logs, check_connectivity, setup_configuration,
                                              get_testbed_details, get_target_object):
        """
            NAT Mode External Captive Portal Test with open encryption 2.4 GHz Band
            pytest -m "advanced_captive_portal_tests and external_captive_portal_tests and open and twog and NAT and click_to_continue"
        """
        def run_command_using_ssh(ssh_client, command: str):
            output = ""
            try_count = 1
            while output.strip() == "" and try_count <= 10:
                try:
                    try_count += 1
                    time.sleep(2)
                    logging.info(f"Executing command: {command}")
                    stdin, stdout, stderr = ssh_client.exec_command(command)
                    output = stdout.read().decode()
                except Exception as exc:
                    logging.error(f"Handled Exception while running {command}: {exc}", exc_info=True)

            if output.strip() == "":
                allure.attach(name="No response while running following command:", body=f"{command}")
                raise Exception("No output from command, check test body!")
            return output

        for dut in get_test_library.dut_data:
            get_test_library.pre_cleanup()

            radio_port_name = list(get_test_library.get_radio_availabilities(num_stations_2g=1)[0].keys())[0]
            security = "open"
            station = 'sta_ecp'
            logging.info(f"Creating a station on the configured ssid on {radio_port_name} radio...")
            sta_got_ip = get_test_library.client_connect_using_radio(
                ssid=setup_params_general["ssid_modes"][security][0]["ssid_name"],
                passkey="[BLANK]",
                security="open",
                mode="NAT-WAN",
                radio=radio_port_name,
                station_name=[station],
                attach_port_info=False
            )

            sta_info = get_test_library.json_get(_req_url=f"port/1/1/{station}")
            dict_table_sta = {
                "Key": list(sta_info["interface"].keys()),
                "Value": list(sta_info["interface"].values())
            }
            data_table_sta = tabulate(dict_table_sta, headers='keys', tablefmt='fancy_grid')
            logging.info(f"Stations Data ({station}): \n{data_table_sta}\n")
            allure.attach(name=f"Stations Data ({station})", body=str(data_table_sta))

            if sta_got_ip is False:
                logging.info("Station Failed to get IP")
                pytest.fail("Station Failed to get IP")

            logging.info("Connecting SSH connection...")
            hostname = get_test_library.manager_ip
            port = get_test_library.manager_ssh_port
            username = 'root'
            password = 'lanforge'
            ping_host = "google.com"
            ping_count = 10
            ping_command = f"/home/lanforge/vrf_exec.bash {station} ping -c {ping_count} {ping_host}"
            client = paramiko.SSHClient()
            try:
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname, port=port, username=username, password=password)

                logging.info("Making sure client not getting internet access before UAM authentication...")
                ping_output_pre_authentication = run_command_using_ssh(client, ping_command)

                logging.info(f"\nBefore Captive Portal-UAM authentication:\n{ping_output_pre_authentication}\n")
                allure.attach(name="Before Captive Portal-UAM authentication, station ping response (google.com)",
                              body=str(ping_output_pre_authentication))

                if "100% packet loss" not in ping_output_pre_authentication:
                    logging.info("Client already have internet access before UAM authentication!!!")
                    pytest.fail("Client already have internet access before UAM authentication")
                logging.info("Client do not have internet access before UAM authentication.")

                logging.info("Getting the inet ip address...")
                logging.info(f"AP idx: {get_test_library.dut_data.index(dut)}")
                cmd_output = get_target_object.get_dut_library_object().run_generic_command(
                    cmd="ifconfig up0v0",
                    idx=get_test_library.dut_data.index(dut),
                    attach_allure=False
                )
                ip_pattern = re.compile(r"inet addr:(\d+\.\d+\.\d+\.\d+)")
                match = ip_pattern.search(cmd_output)
                inet_ip_addr = match.group(1)
                logging.info(f"inet ip addr: {inet_ip_addr}")

                expected_location = f"/home/lanforge/vrf_exec.bash {station} curl -I http://{inet_ip_addr}/hotspot/"
                expected_location_output = run_command_using_ssh(client, expected_location)

                challenge_link = re.findall(r'^Location:\s+(.*?)\s*$', expected_location_output, re.MULTILINE)[0]
                logging.info(f"Redirection link: {challenge_link}")

                url_info = {}
                for field in challenge_link.split('?')[1].split('&'):
                    key_val_list = field.split('=')
                    if len(key_val_list) == 2 and len(key_val_list[1]) != 0:
                        url_info[key_val_list[0]] = key_val_list[1]
                logging.info(f"url_info: {url_info}")

                challenge = url_info['challenge']
                nasid = url_info['nasid']
                station_mac = url_info['mac']
                uamport = url_info['uamport']

                link = (
                    f"https://customer.hotspotsystem.com/customer/hotspotlogin.php?name=&email=&company=&address="
                    f"&city=&state=&country=&zip=&phone=&capture_custom_1=&capture_custom_2=&capture_custom_3="
                    f"&capture_custom_4=&capture_custom_5=&ssl-login=&chal={challenge}&uamip={inet_ip_addr}"
                    f"&uamport={uamport}&nasid={nasid}&mac={station_mac}&userurl=&login=login&skin_id="
                    f"&uid={station_mac}&pwd=password&operator={nasid}&location_id=1&lang=en&agree=1"
                )
                expected_302 = f'/home/lanforge/vrf_exec.bash {station} curl -I "{link}"'
                response_302 = run_command_using_ssh(client, expected_302)

                logging.info(f"\n{response_302}")
                allure.attach(name="Expected 302 response: ", body=str(response_302),
                              attachment_type=allure.attachment_type.TEXT)

                link_to_hit = re.findall(r'^Location:\s+(.*?)\s*$', response_302, re.MULTILINE)[0]
                logging.info(f"Link to hit: {link_to_hit}")

                cmd_to_authenticate = f'/home/lanforge/vrf_exec.bash {station} curl "{link_to_hit}"'
                authentication_response = run_command_using_ssh(client, cmd_to_authenticate)

                logging.info(f"\n{authentication_response}\n")
                allure.attach(name="Response from captive portal: ",
                              body=authentication_response, attachment_type=allure.attachment_type.HTML)

                if "<h1> Connected </h1>" not in authentication_response:
                    logging.info("Captive portal authentication Failed")
                    pytest.fail("Captive portal authentication Failed")

                logging.info("Captive portal authentication successful! Checking if client got internet access...")
                ping_output_post_authentication = run_command_using_ssh(client, ping_command)

                logging.info(f"\nAfter Captive Portal-UAM authentication:\n{ping_output_post_authentication}\n")
                allure.attach(name="After Captive Portal-UAM authentication, station ping response (google.com)",
                              body=str(ping_output_post_authentication))

                if "100% packet loss" in ping_output_post_authentication:
                    logging.info("Client did not get internet access even after authentication!!!")
                    pytest.fail("Client did not get internet access even after authentication")
            except Exception as e:
                logging.error(f"Error occurred: {e}", exc_info=True)
                pytest.fail(f"Error occurred: {e}")
            finally:
                client.close()
