# LANForge Python Scripts
This directory contains python scripts useful for unit-tests.  It uses libraries in ../py-json. Please place new tests in this directory. Unless they are libraries, please avoid adding python scripts to ../py-json. Please read https://www.candelatech.com/cookbook/cli/json-python to learn about how to use the LANforge client JSON directly. Review http://www.candelatech.com/scripting_cookbook.php to understand more about scripts in general.

# Getting Started

The first step is to make sure all dependencies are installed in your system by running update_deps.py in this folder.

Please consider using the `LFCliBase` class as your script superclass. It will help you with a consistent set of JSON handling methods and pass and fail methods for recording test results. Below is a sample snippet that includes LFCliBase:

    if 'py-json' not in sys.path:
        sys.path.append('../py-json')
    from LANforge import LFUtils
    from LANforge import lfcli_base
    from LANforge.lfcli_base import LFCliBase
    from LANforge.LFUtils import *
    import realm
    from realm import Realm

    class Eggzample(LFCliBase):
        def __init__(self, lfclient_host, lfclient_port):
            super().__init__(lfclient_host, lfclient_port, debug=True)

    def main():
        eggz = Eggzample("http://localhost", 8080)
        frontpage_json = eggz.json_get("/")
        pprint.pprint(frontpage_json)
        data = {
            "message": "hello world"
        }
        eggz.json_post("/cli-json/gossip", data, debug_=True)

    if __name__ == "__main__":
        main()

The above example will stimulate output on the LANforge client websocket `ws://localhost:8081`. You can monitor system activity over that channel.

## Useful URIs:
* /: provides version information and a list of supported URIs
* /DUT/: Device Under Test records
* /alerts/: port or connection alerts
* /cli-form: post multi-part form data to this URI
* /cli-json: post JSON data to this URI
* /help: list of CLI commands and refence links
* /help/set_port: each CLI command has a command composer
* /cx: connections
* /endp: endpoints that make up connections
* /gui-cli: post multi-part form data for GUI automation
* /gui-json: post JSON data to this URI for GUI automation
* /port: list ports and stations, oriented by shelf, resource and name: `/port/1/1/eth0` is typically your management port
* /stations: entities that are associated to your virtual access points (vAP)
There are more URIs you can explore, these are the more useful ones.

#### Scripts included are:

* `cicd_TipIntegration.py`: battery of TIP tests that include upgrading DUT and executing sta_connect script

* `cicd_testrail.py`:
  * `function send_get`: Issues a GET request (read) against the API.
  * `function send_post`: Issues a write against the API.
  * `function __send_request`:
  * `function get_project_id`: Gets the project ID using the project name
  * `function get_run_id`: Gets the run ID using test name and project name
  * `function update_testrail`: Update TestRail for a given run_id and case_id

* `cicd_testrailAndInfraSetup.py`:
  * class `GetBuild`:
     * function `get_latest_image`: extract a tar file from the latest file name from a URL
     * function run_`opensyncgw_in_docker`:
     * function `run_opensyncgw_in_aws`:
  * class `openwrt_linksys`:
    * function `ap_upgrade`: transfers file from local host to remote host. Upgrade access point with new information (?)
  * class `RunTest`:
    * function `TestCase_938`: checks single client connectivity
    * function `TestCase_941`: checks for multi-client connectivity
    * function `TestCase_939`: checks for client count in MQTT log and runs the clients (?)

* `run_cv_scenario.py`:
   * class `RunCvScenario`: imports the LFCliBase class.
    * function `get_report_file_name`: returns report name
    * function `build`: loads and sends the ports available?
    * function `start`: /gui_cli takes commands keyed on 'cmd' and this function create an array of commands
* `sta_connect.py`:  This function creates a station, create TCP and UDP traffic, run it a short amount of time,
  and verify whether traffic was sent and received.  It also verifies the station connected
  to the requested BSSID if bssid is specified as an argument.
  The script will clean up the station and connections at the end of the test.
    * class `StaConnect(LFCliBase)`:
        * function `get_realm`: returns the local realm
        * function `get_station_url`:
        * function `get_upstream_url`:
        * function `compare_vals`: compares pre-test values to post-test values
        * function `remove_stations`: removes all stations
        * function `num_associated`:
        * function `clear_test_results`:
        * function `run`:
        * function `setup`:
        * function `start`:
        * function `stop`:
        * function `finish`:
        * function `cleanup`:
        * function `main`:
* `sta_connect2.py`: This will create a station, create TCP and UDP traffic, run it a short amount of time,
  and verify whether traffic was sent and received.  It also verifies the station connected
  to the requested BSSID if bssid is specified as an argument. The script will clean up the station and connections at the end of the test.
    * function `get_realm`: returns local realm
    * function `get_station_url`:
    * function `get_upstream_url`:
    * function `compare_vals`: compares pre-test values to post-test values
    * function `remove_stations`: removes all ports
    * function `num_associated`:
    * function `clear_test_results`
    * function `setup`: verifies upstream url, creates stations and turns dhcp on, creates endpoints,
    UDP endpoints,  
    * function `start`:
    * function `stop`:
    * function `cleanup`:
    * function `main`:

* `sta_connect_example.py`: example of how to instantiate StaConnect and run the test

* `sta_connect_multi_example.py`: example of how to instantiate StaConnect and run the test and create multiple OPEN stations,have
some stations using WPA2

* `stations_connected.py`: Contains examples of using realm to query stations and get specific information from them

* `test_ipv4_connection.py`: This script will create a variable number of stations that will attempt to connect to a chosen SSID using a provided password and security type.
  The test is considered passed if all stations are able to associate and obtain IPV4 addresses
  * class `IPv4Test`
    * function `build`: This function will use the given parameters (Number of stations, SSID, password, and security type) to create a series of stations.
    * function `start`: This function will admin-up the stations created in the build phase. It will then check all stations periodically for association and IP addresses.
    This will continue until either the specified timeout has been reached or all stations obtain an IP address.
    * function `stop`: This function will admin-down all stations once one of the ending criteria is met.
    * function `cleanup`: This function will clean up all stations created during the test.
  * command line options :
    * `--mgr`: Specifies the hostname where LANforge is running. Defaults to http://localhost
    * `--mgr_port`: Specifies the port to use when connecting to LANforge. Defaults to 8080
    * `--ssid`: Specifies SSID to be used in the test
    * `--password`: Specifies the password for the SSID to be used in the test
    * `--security`: Specifies security type (WEP, WPA, WPA2, WPA3, Open) of SSID to be used in the test
    * `--num_stations`: Specifies number of stations to create for the test
    * `--radio`: Specifies the radio to be used in the test. Eg wiphy0
    * `--debug`: Turns on debug output for the test
    * `--help`: Displays help output for the script    

* `test_ipv6_connection.py`: This script will create a variable number of stations that will attempt to connect to a chosen SSID using a provided password and security type.
  The test is considered passed if all stations are able to associate and obtain IPV6 addresses
  * class `IPv6Test`
    * function `build`: This function will use the given parameters (Number of stations, SSID, password, and security type) to create a series of stations.
    * function `start`: This function will admin-up the stations created in the build phase. It will then check all stations periodically for association and IP addresses.
    This will continue until either the specified timeout has been reached or all stations obtain an IP address.
    * function `stop`: This function will admin-down all stations once one of the ending criteria is met.
    * function `cleanup`: This function will clean up all stations created during the test.
  * Command line options :
    * `--mgr`: Specifies the hostname where LANforge is running. Defaults to http://localhost
    * `--mgr_port`: Specifies the port to use when connecting to LANforge. Defaults to 8080
    * `--ssid`: Specifies SSID to be used in the test
    * `--password`: Specifies the password for the SSID to be used in the test
    * `--security`: Specifies security type (WEP, WPA, WPA2, WPA3, Open) of SSID to be used in the test
    * `--num_stations`: Specifies number of stations to create for the test
    * `--radio`: Specifies the radio to be used in the test. Eg wiphy0
    * `--debug`: Turns on debug output for the test
    * `--help`: Displays help output for the script

* `test_l3_unicast_traffic_gen.py`: This script will create stations, create traffic between upstream port and stations, run traffic.
The traffic on the stations will be checked once per minute to verify that traffic is transmitted and received.
Test will exit on failure of not receiving traffic for one minute on any station.
  * class `L3VariableTimeLongevity`
    * function `build`: This function will create a group of stations and cross connects that are used in the test.
    * function `start`: This function will admin-up all stations and start traffic over the cross-connects. Values in the cross-connects
      will be checked every minute to verify traffic is transmitted and received.
    * function `stop`: This function will stop all cross-connects from generating traffic and admin-down all stations.
    * function `cleanup`: This function will cleanup all cross-connects and stations created during the test.
  * Command line options:
    * `-d, --test_duration`: Determines the total length of the test. Consists of number followed by letter indicating length
      10m would be 10 minutes or 3d would be 3 days. Available options for length are Day (d), Hour (h), Minute (m), or Second (s)
    * `-t, --endp_type`: Specifies type of endpoint to be used in the test. Options are lf_udp, lf_udp6, lf_tcp, lf_tcp6
    * `-u, --upstream_port`: This is the upstream port to be used for traffic. An upstream port is some data source on the wired LAN or WAN beyond the AP
    * `-r, --radio`: This switch will determine the radio name, number of stations, ssid, and ssid password. Security type is fixed at WPA2.
    Usage of this switch could look like: `--radio wiphy1 64 candelaTech-wpa2-x2048-5-3 candelaTech-wpa2-x2048-5-3`

* `test_ipv4_l4_urls_per_ten.py`: This script measure the number of urls per ten minutes over layer 4 traffic
  * class `IPV4L4`
    * function `build`: This function will create all stations and cross-connects to be used in the test
    * function `start`: This function will admin-up stations and start all traffic over the cross-connects. It will then measure the amount of traffic that passed through
      the cross-connects every ten minutes. These values are compared to 90% of the chosen target traffic per ten minutes. If this value is exceeded, a pass will occur,
      otherwise, a fail is recorded.      
    * function `stop`: This function will admin-down stations and stop all traffic.
    * function `cleanup`: This function will cleanup any stations or cross-connects associated with the test.
  * Command line options:
    * `--mgr`: Specifies the hostname where LANforge is running. Defaults to http://localhost
    * `--mgr_port`: Specifies the port to use when connecting to LANforge. Defaults to 8080
    * `--ssid`: Specifies SSID to be used in the test
    * `--password`: Specifies the password for the SSID to be used in the test
    * `--security`: Specifies security type (WEP, WPA, WPA2, WPA3, Open) of SSID to be used in the test
    * `--num_stations`: Specifies number of stations to create for the test
    * `--radio`: Specifies the radio to be used in the test. Eg wiphy0
    * `--requests_per_ten`: Configures the number of request per ten minutes
    * `--num_tests`: Configures the number of tests to be run. Each test runs for ten minutes
    * `--url`: Specifies the upload/download, address, and destination. Example: dl http://10.40.0.1 /dev/null
    * `--target_per_ten`: Rate of target urls per ten minutes. 90% of this value will be considered the threshold for a passed test.
    * `--debug`: Turns on debug output for the test
    * `--help`: Displays help output for the script


* `test_ipv4_l4_ftp_urls_per_ten.py`: This script measure the number of urls per ten minutes over layer 4 ftp traffic
  * class `IPV4L4`
    * function `build`: This function will create all stations and cross-connects to be used in the test
    * function `start`: This function will admin-up stations and start all traffic over the cross-connects. It will then measure the amount of traffic that passed through
      the cross-connects every ten minutes. These values are compared to 90% of the chosen target traffic per ten minutes. If this value is exceeded, a pass will occur,
      otherwise, a fail is recorded.      
    * function `stop`: This function will admin-down stations and stop all traffic.
    * function `cleanup`: This function will cleanup any stations or cross-connects associated with the test.
  * Command line options:
    * `--mgr`: Specifies the hostname where LANforge is running. Defaults to http://localhost
    * `--mgr_port`: Specifies the port to use when connecting to LANforge. Defaults to 8080
    * `--ssid`: Specifies SSID to be used in the test
    * `--password`: Specifies the password for the SSID to be used in the test
    * `--security`: Specifies security type (WEP, WPA, WPA2, WPA3, Open) of SSID to be used in the test
    * `--num_stations`: Specifies number of stations to create for the test
    * `--radio`: Specifies the radio to be used in the test. Eg wiphy0
    * `--requests_per_ten`: Configures the number of request per ten minutes
    * `--num_tests`: Configures the number of tests to be run. Each test runs for ten minutes
    * `--url`: Specifies the upload/download, address, and destination. Example: dl http://10.40.0.1 /dev/null
    * `--target_per_ten`: Rate of target urls per ten minutes. 90% of this value will be considered the threshold for a passed test.
    * `--debug`: Turns on debug output for the test
    * `--help`: Displays help output for the script

* `test_generic`:
    * class `GenTest`: This script will create
      * function `build`: This function will create the stations and cross-connects to be used during the test.
      * function `start`: This function will start traffic and measure different values dependent on the command chosen.
        Commands currently available for use: lfping, generic, and speedtest.
      * function `stop`: This function will admin-down stations, stop traffic on cross-connects and cleanup any stations or cross-connects associated with the test.
      * function `cleanup`: This function will remove any stations and cross-connects created during the test.
    * Command line options:
      * `--mgr`: Specifies the hostname where LANforge is running. Defaults to http://localhost
      * `--mgr_port`: Specifies the port to use when connecting to LANforge. Defaults to 8080
      * `--ssid`: Specifies SSID to be used in the test
      * `--password`: Specifies the password for the SSID to be used in the test
      * `--security`: Specifies security type (WEP, WPA, WPA2, WPA3, Open) of SSID to be used in the test
      * `--num_stations`: Specifies number of stations to create for the test
      * `--radio`: Specifies the radio to be used in the test. Eg wiphy0
      * `--upstream_port`: This is the upstream port to be used for traffic. An upstream port is some data source on the wired LAN or WAN beyond the AP
      * `--type`: Specifies type of generic connection to make. (generic, lfping, iperf3-client, speedtest, iperf3-server, lf_curl)
      * `--dest`: Specifies the destination for some commands to use
      * `--interval`: Specifies the interval between tests in the start function
      * `--test_duration`: Specifies the full duration of the test. Consists of number followed by letter indicating length
      10m would be 10 minutes or 3d would be 3 days. Available options for length are Day (d), Hour (h), Minute (m), or Second (s)
      * `--debug`: Turns on debug output for the test
      * `--help`: Displays help output for the script

* `test_ipv4_variable_time.py`:
     * class `IPv4VariableTime`
        * function `__set_all_cx_state`:
        * function `run_test`:
        * function `cleanup`:
        * function `run`:

* `test_wanlink.py`:
   * class `LANtoWAN`
      * function `run_test`:
      * function `create_wanlinks`:
      * function `run`:
      * function `cleanup`:

* `vap_stations_example.py`:
    * class `VapStations`
      * function `run`:
      * function `main`:
