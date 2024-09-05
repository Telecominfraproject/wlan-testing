"""

    External Captive Portal Test: BRIDGE Mode
    pytest -m "external_captive_portal_tests and bridge"

"""
import logging
import re
import time
import allure
import paramiko
import pytest
from tabulate import tabulate
from bs4 import BeautifulSoup

pytestmark = [pytest.mark.external_captive_portal_tests, pytest.mark.bridge, pytest.mark.advanced_captive_portal_tests]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid_ext_cap_portal_open_2g_id_p", "appliedRadios": ["2G"], "security_key": "something",
             "captive": {
                 "auth-mode": "uam",
                 "uam-port": 3990,
                 "uam-secret": "hotsys123",
                 "uam-server": "https://customer.hotspotsystem.com/customer/hotspotlogin.php",
                 "nasid": "AlmondLabs_6",
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
@allure.sub_suite(sub_suite_name="BRIDGE Mode")
@pytest.mark.parametrize(
    'setup_configuration',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_configuration")
class TestBridgeModeExternalCaptivePortal(object):
    """
            External Captive Portal Test: BRIDGE Mode
            pytest -m "advanced_captive_portal_tests and external_captive_portal_tests and bridge"
    """

    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.local_user_and_pass
    @pytest.mark.ow_regression_lf
    @allure.title("Local user/pass mode with open encryption 2.4 GHz Band Bridge mode")
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-13683", name="WIFI-13683")
    def test_bridge_open_2g_local_user_and_pass(self, get_test_library, get_dut_logs_per_test_case,
                                                get_test_device_logs, check_connectivity, setup_configuration,
                                                get_testbed_details, get_target_object):
        """
            BRIDGE Mode External Captive Portal Test with open encryption 2.4 GHz Band
            pytest -m "advanced_captive_portal_tests and external_captive_portal_tests and open and twog and bridge and local_user_and_pass"
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
                mode=setup_params_general["mode"],
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

                link = (f'https://customer.hotspotsystem.com/customer/hotspotlogin.php?ssl-login=&chal={challenge}'
                        f'&uamip={inet_ip_addr}&uamport={uamport}&nasid={nasid}&mac={station_mac}'
                        f'&userurl=ct522-7481%2F&login=login&skin_id=&uid=userr1&pwd=password1')
                html_request = f'/home/lanforge/vrf_exec.bash {station} curl "{link}"'
                html_response = run_command_using_ssh(client, html_request)

                logging.info(f"HTML response containing authentication url:\n{html_response}")
                allure.attach(name="HTML response containing authentication url:", body=str(html_response),
                              attachment_type=allure.attachment_type.TEXT)

                soup = BeautifulSoup(html_response, 'html.parser')
                meta_tag = soup.find('meta', attrs={'http-equiv': 'refresh'})
                content = meta_tag['content']
                authentication_url = "=".join(content.split('=')[1:])

                logging.info(f"Authentication URL extracted from HTML:\n{authentication_url}\n")
                allure.attach(name="Authentication URL extracted from HTML:", body=str(authentication_url))

                cmd_to_authenticate = f'/home/lanforge/vrf_exec.bash {station} curl "{authentication_url}"'
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

            logging.info("Checking throughput speed...")
            wifi_capacity_obj_list = get_test_library.wifi_capacity(mode="BRIDGE",
                                                                    download_rate="10Gbps",
                                                                    upload_rate="56Kbps",
                                                                    protocol="UDP-IPv4",
                                                                    duration="60000",
                                                                    batch_size="1",
                                                                    stations=radio_port_name[:4] + station,
                                                                    add_stations=False,
                                                                    create_stations=False)

            report = wifi_capacity_obj_list[0].report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1] + "/"
            numeric_score = get_test_library.read_kpi_file(column_name=["numeric-score"], dir_name=report)
            expected_throughput = 10
            throughput = {
                "download": [numeric_score[0][0]],
                "upload": [numeric_score[1][0]],
                "total": [numeric_score[2][0]],
                "expected": [f"<= {expected_throughput}"],
                "unit": ["Mbps"],
                "PASS": [numeric_score[2][0] <= expected_throughput]
            }
            data_table = tabulate(throughput, headers='keys', tablefmt='fancy_grid')
            allure.attach(name='Throughput Data', body=data_table)
            logging.info(f"\n{data_table}")

            if not throughput["PASS"][0]:
                logging.info("Throughput exceeded than set threshold")
                pytest.fail("Throughput exceeded than set threshold")
            logging.info("Throughput is within the set threshold")
