# LANforge Perl, Python, and Shell Scripts #
This is a collection of scripts and scripting libraries designed to work
with LANforge systems. On your LANforge system, these scripts are
typically installed into `/home/lanforge/scripts`. The `LANforge/` sub directory holds
the perl modules (`.pm` files) that are common to the perl scripts.

## LANforge CLI Users Guide:  https://www.candelatech.com/lfcli_ug.php ##
The LANforge CLI Users Guide is a good place to start for understanding scripts

## LANforge on system cli help and cli command composer ##
The LANforge has an on system help / system query, when on LANforge browse to 
http://local_host:8080

The LANforge has an on system cli help and cli command composer 
http://local_host:8080/help 

### Commonly Used ###
The `lf_*.pl` scripts are typically more complete and general purpose
scripts, though some are ancient and very specific.  In particular,
these scripts are more modern and may be a good place to start:

| Name             | Purpose   |
|------------------|-----------|
| `lf_associate_ap.pl`    | LANforge server script for associating virtual stations to an arbitrary SSID |
| `lf_attenmod.pl`        | Query and update CT70X programmable attenuators |
| `lf_firemod.pl`         | Query and update connections (Layer 3) |
| `lf_icemod.pl`          | Query and update WAN links and impairments |
| `lf_portmod.pl`         | Query and update physical and virtual ports |
| `lf_tos_test.py`        | Generate traffic at different QoS and report in spreadsheet |
| `lf_sniff.py`           | Create packet capture files, especially OFDMA /AX captures |

The `lf_wifi_rest_example.pl` script shows how one might call the other scripts from
within a script.

### Examples and Documents ###
Read more examples in the [scripting LANforge](http://www.candelatech.com/lfcli_api_cookbook.php) cookbook.

## Python Scripts ##

When starting to use Python, please run the update_dependencies.py script located in py-scripts to install all necessary dependencies for this library.


### Python Scripts py-json/LANforge ###

Core communication files to LANforge

| Name | Purpose |
|------|---------|
| `add_dut.py`            | defined list of DUT keys, cli equivalent: https://www.candelatech.com/lfcli_ug.php#add_dut  |
| `add_file_endp.py`      | Add a File endpoint to the LANforge Manager.  cli equivalent: add_file_endp https://www.candelatech.com/lfcli_ug.php#add_file_endp |
| `add_l4_endp.py`        |  Add a Layer 4-7 (HTTP, FTP, TELNET, ..) endpoint to the LANforge Manager. cli equivalent: add_l4_endp https://www.candelatech.com/lfcli_ug.php#add_l4_endp |
| `add_monitor.py`        | Add a WIFI Monitor interface. These are useful for doing low-level wifi packet capturing.  cli equivalent: add_monitor https://www.candelatech.com/lfcli_ug.php#add_monitor |
| `add_sta.py`            | Add a WIFI Virtual Station (Virtual STA) interface. cli equivalent: add_sta https://www.candelatech.com/lfcli_ug.php#add_sta |
| `add_vap.py`            | Add a WIFI Virtual Access Point (VAP) interface.  cli equivalent: add_vap https://www.candelatech.com/lfcli_ug.php#add_vap |
| `set_port.py`           | This command allows you to modify attributes on an Ethernet port.  cli equivalent: set_port https://www.candelatech.com/lfcli_ug.php#set_port |
| `lfcli_base.py`          | json communication to LANforge |
| `LFRequest.py`          | Class holds default settings for json requests to LANforge, see: https://gist.github.com/aleiphoenix/4159510|
| `LFUtils.py`            | Defines useful common methods |
| `set_port.py`           | This command allows you to modify attributes on an Ethernet port. These options includes the IP address, netmask, gateway address, MAC, MTU, and TX Queue Length. cli equivalent: set_port https://www.candelatech.com/lfcli_ug.php#set_port |


### Python Scripts py-json/ ###
| Name | Purpose |
|------|---------|
| `base_profile.py`                 | Class: BaseProfile  Use example: py-json/l3_cxprofile2.py used to define generic utility methods to be inherited by other classes |
| `create_wanlink.py`               | Create and modify WAN Links Using LANforge JSON AP : http://www.candelatech.com/cookbook.php?vol=cli&book=JSON:+Managing+WANlinks+using+JSON+and+Python |
| `cv_commands.py`                  | This is a library file used to create a chamber view scenario.  import this file as showed in create_chamberview.py to create a scenario |
| `cv_test_manager.py`              | This script is working as library for chamberview tests.  It holds different commands to automate test. |
| `cv_test_reports.py`              | Class: lanforge_reports  Pulls reports from LANforge |
| `dataplane_test_profile.py`       | Library to Run Dataplane Test: Using lf_cv_base class |
| `dut_profile.py`                  | Class: DUTProfile (new_dut_profile) Use example:  py-scripts/update_dut.py used to updates a Device Under Test (DUT) entry in the LANforge test scenario A common reason to use this would be to update MAC addresses in a DUT when you switch between different items of the same make/model of a DUT |
| `fio_endp_profile.py`             | Class: FIOEndpProfile (new_fio_endp_profile) Use example: py-scripts/test_fileio.py will create stations or macvlans with matching fileio endpoints to generate and verify  fileio related traffic |
| `gen_cxprofile.py`                | Class: GenCXProfile (new_generic_endp_profile) Use example: test_generic.py  will create stations and endpoints to generate traffic based on a command-line specified command type |
| `http_profile.py`                 | Class: HTTPProfile (new_http_profile) Use example: test_ipv4_l4_wifi.py  will create stations and endpoints to generate and verify layer-4 upload traffic |
| `l3_cxprofile.py`                 | Class: L3CXProfile (new_l3_cx_profile)  Use example: test_ipv4_variable_time.py will create stations and endpoints to generate and verify layer-3 traffic |
| `l3_cxprofile2.py`                | Class: L3CXProfile2 (new_l3_cx_profile, ver=2) No current use example, inherits utility functions from BaseProfile, maintains functionality of L3CXProfile |
| `l4_cxprofile.py`                 | Class: L4CXProfile (new_l4_cx_profile) Use example: test_ipv4_l4.py will create stations and endpoints to generate and verify layer-4 traffic |
| `lf_cv_base.py`                   | Class: ChamberViewBase, Base Class to be used for Chamber View Tests, inherited by DataPlaneTest in dataplane_test_profile.py |
| `lfdata.py`                       | Class: LFDataCollection, class used for data collection utility methods |
| `mac_vlan_profile.py`             | Class: MACVLANProfile (new_mvlan_profile) Use example: test_fileio.py will create stations or macvlans with matching fileio endpoints to generate and verify  fileio related traffic. |
| `multicast_profile.py`            | Class: MULTICASTProfile (new_multicast_profile) Use example: test_l3_longevity.py multi cast profiles are created in this test |
| `port_utils.py`                   | Class: PortUtils used to set the ftp or http port |
| `qvlan_profile.py`                | Class: QVLANProfile (new_qvlan_profile) Use example: create_qvlan.py (802.1Q VLAN) |
| `realm.py`                        | Class: The Realm Class is inherited by most python tests.  Realm Class inherites from LFCliBase. The Realm Class contains the configurable components for LANforge,  For example L3 / L4 cross connects, stations.  http://www.candelatech.com/cookbook.php?vol=cli&book=Python_Create_Test_Scripts_With_the_Realm_Class |
| `realm_test.py`                   | Python script meant to test functionality of realm methods |
| `show_ports.py`                   | Python script example of how to check a LANforge json url  |
| `station_profile.py`              | Class: StationProfile (new_station_profile) Use example: most scripts create and use station profiles |
| `test_base.py`                    | Class: TestBase, basic class for creating tests, uses basic functions for cleanup, starting/stopping, and passing of tests |
| `test_group_profile.py`           | Class: TestGroupProfile (new_test_group_profile) Use example: test_fileio.py will create stations or macvlans with matching fileio endpoints to generate and verify  fileio related traffic |
| `test_utility.py`                 | Standard Script for Webconsole Test Utility |
| `vap_profile.py`                  | Class: VAPProfile (new_vap_profile) profile for creating Virtual AP's Use example: create_vap.py |
| `vr_profile2.py`                  | Class: VRProfile (new_vap_profile, ver=2) No current use example, inherits utility functions from BaseProfile |
| `wifi_monitor_profile.py`         | Class: WifiMonitor (new_wifi_monitor_profile) Use example: tip_station_powersave.py This script uses filters from realm's PacketFilter class to filter pcap output for specific packets. |
| `wlan_theoretical_sta.py`         | Class: abg11_calculator Standard Script for WLAN Capaity Calculator  Use example: wlan_capacitycalculator.py |
| `ws-sta-monitor.py`               | Example of how to filter messages from the :8081 websocket |
| `ws_generic_monitor.py`           | Class: WS_Listener web socket listener Use example: ws_generic_monitor_test.py, ws_generic_monitor to monitor events triggered by scripts, This script when running, will monitor the events triggered by test_ipv4_connection.py |



### Python Scripts py-scripts ###

Test scripts and helper scripts

| Name | Purpose |
|------|---------|
| `cicd_TipIntegration.py`           | Facebook TIP infrastructure|
| `cicd_testrail.py`                 | TestRail API binding for Python 3 |
| `cicd_testrailAndInfraSetup.py`    | Facebook TIP infrastructure |
| `connection_test.py`               | Standard Script for Connection Testing -  Creates HTML and pdf report as a result (Used for web-console) |
| `create_bond.py`                   | This script can be used to create a bond |
| `create_bridge.py`                 | Script for creating a variable number of bridges |
| `create_chamberview.py`            | Script for creating a chamberview scenario |
| `create_l3.py`                     | This script will create a variable number of layer3 stations each with their own set of cross-connects and endpoints |
| `create_l4.py`                     | This script will create a variable number of layer4 stations each with their own set of cross-connects and endpoints |
| `create_macvlan.py`                | Script for creating a variable number of macvlans |
| `create_qvlan.py`                  | Script for creating a variable number of qvlans |
| `create_station.py`                | Script for creating a variable number of stations |
| `create_station_from_df.py`        | Script for creating a variable number of stations from a file |
| `create_vap.py`                    | Script for creating a variable number of VAPs |
| `create_vr.py`                     | Script for creating a variable number of bridges |
| `csv_convert.py`                   | Python script to read in a LANforge Dataplane CSV file and output a csv file that works with a customer's RvRvO visualization tool.|
| `csv_processor.py`                 | Python script to assist processing csv files|
| `csv_to_influx.py`                 | Python script to copy the data from a CSV file from the KPI file generated from a Wifi Capacity test to an Influx database|
| `download_test.py`                 | download_test.py will do lf_report::add_kpi(tags, 'throughput-download-bps', $my_value);|
| `event_breaker.py`                 | This file is intended to expose concurrency problems in the /events/ URL handler by querying events rapidly. Please use concurrently with event_flood.py. |
| `event_flood.py`                   | This file is intended to expose concurrency problems in the /events/ URL handler by inserting events rapidly. Please concurrently use with event_breaker.py.|
| `example_security_connection.py`   | This python script creates a variable number of stations using user-input  security
| `ftp_html.py`                      | This FTP Test is used to "Verify that N clients connected on Specified band and can simultaneously download some amount of file from FTP server and measures the time taken by client to Download/Upload the file |
| `grafana_profile.py`               | Class for creating and managing a grafana dashboard |
| `html_template.py`                 | This script is used for DFS Test Report generation |
| `influx.py`                        | Class for communicating with influx |
| `influx2.py`                       | Class for communicating with influx |
| `layer3_test.py`                   | Python script to test and monitor layer 3 connections |
| `layer4_test.py`                   | Python script to test and monitor layer 4 connections |
| `lf_ap_auto_test.py`               | This script is used to automate running AP-Auto tests |
| `lf_dataplane_test.py`             | This script is used to automate running Dataplane tests |
| `lf_dfs_test.py`                   | Test testing dynamic frequency selection (dfs) between an AP connected to a controller and Lanforge|
| `lf_dut_sta_vap_test.py`           | Load an existing scenario, start some layer 3 traffic, and test the Linux based DUT that has SSH server |
| `lf_ftp_test.py`                   | Python script will create stations and endpoints to generate and verify layer-4 traffic over an ftp connection |
| `lf_graph.py`                      | Classes for creating images from graphs using data sets |
| `lf_mesh_test.py`                  | This script is used to automate running Mesh tests |
| `lf_report.py`                     | This program is a helper  class for reporting results for a lanforge python script |
| `lf_report_test.py`                | Python script to test reporting |
| `lf_rvr_test.py`                   | This script is used to automate running Rate-vs-Range tests |
| `lf_snp_test.py`                   | Test scaling and performance (snp) run various configurations and measures data rates |
| `lf_tr398_test.py`                 | This script is used to automate running TR398 tests |
| `lf_wifi_capacity_test.py`         | This is a test file which will run a wifi capacity test |
| `recordinflux.py`                  | recordinflux will record data from existing lanforge endpoints to record to an already existing influx database |
| `run_cv_scenario.py`               | Set the LANforge to a BLANK database then it will load the specified database and start a graphical report |
| `rvr_scenario.py`                  | This script will set the LANforge to a BLANK database then it will load the specified database and start a graphical report |
| `scenario.py`                      | Python script to load a database file and control test groups |
| `sta_connect.py`                   | Create a station, run TCP and UDP traffic then verify traffic was received. Stations are cleaned up afterwards |
| `sta_connect2.py`                  | Create a station, run TCP and UDP traffic then verify traffic was received. Stations are cleaned up afterwards |
| `sta_connect_example.py`           | Example of how to instantiate StaConnect and run the test |
| `sta_connect_multi_example.py`     | Example of how to instantiate StaConnect and run the test |
| `station_layer3.py`                | this script creates one station with given arguments |
| `stations_connected.py`            | Contains examples of using realm to query stations and get specific information from them |
| `test_1k_clients_jedtest.py`       | Python script to test 1k client connections |
| `test_client_admission.py`         | This script will create one station at a time and generate downstream traffic |
| `test_fileio.py`                   | Test FileIO traffic |
| `test_generic.py`                  | Test generic traffic using generic cross-connect and endpoint type |
| `test_ipv4_connection.py`          | Test connections to a VAP of varying security types (WEP, WPA, WPA2, WPA3, Open) |
| `test_ipv4_l4.py`                  | Test layer 4 traffic using layer 4 cross-connect and endpoint type |
| `test_ipv4_l4_ftp_upload.py`       | Test ftp upload traffic |
| `test_ipv4_l4_ftp_urls_per_ten.py` | Test the number of urls per ten minutes in ftp traffic |
| `test_ipv4_l4_ftp_wifi.py`         | Test ftp upload traffic wifi-wifi |
| `test_ipv4_l4_urls_per_ten.py`     | Test urls per ten minutes in layer 4 traffic |
| `test_ipv4_l4_wifi.py`             | Test layer 4 upload traffic wifi-wifi|
| `test_ipv4_ttls.py`                | Test connection to ttls system |
| `test_ipv4_variable_time.py`       | Test connection and traffic on VAPs of varying security types (WEP, WPA, WPA2, WPA3, Open) |
| `test_ipv6_connection.py`          | Test IPV6 connection to VAPs of varying security types (WEP, WPA, WPA2, WPA3, Open) |
| `test_ipv6_variable_time.py`       | Test IPV6 connection and traffic on VAPs of varying security types (WEP, WPA, WPA2, WPA3, Open) |
| `test_l3_WAN_LAN.py`               | Test traffic over a bridged NAT connection |
| `test_l3_longevity.py`             | Create variable stations on multiple radios, configurable rates, PDU, ToS, TCP and/or UDP traffic, upload and download, attenuation |
| `test_l3_powersave_traffic.py`     | Python script to test for layer 3 powersave traffic |
| `test_l3_scenario_throughput.py`   | Load an existing scenario and run the simultaneous throughput over time and generate report and P=plot the G=graph|
| `test_l3_unicast_traffic_gen.py`   | Generate unicast traffic over a list of stations|
| `test_status_msg.py`               | Test the status message passing functions of /status-msg |
| `test_wanlink.py`                  | Python script to test wanlink creation |
| `test_wpa_passphrases.py`          | Python script to test challenging wpa psk passphrases |
| `testgroup.py`                     | Python script to test creation and control of test groups |
| `testgroup2.py`                    | Python script to test creation and control of test groups |
| `tip_station_powersave.py`         | Generate and test for powersave packets within traffic run over multiple stations |
| `update_dependencies.py`           | Python script to update dependencies for various Candelatech python scripts |
| `update_dut.py`                    | This script updates a Device Under Test (DUT) entry in the LANforge test scenario |
| `wlan_capacity_calculator.py`      | Standard Script for WLAN Capacity Calculator |
| `ws_generic_monitor_test.py`       | This example is to demonstrate ws_generic_monitor to monitor events triggered by scripts, This script when running, will monitor the events triggered by test_ipv4_connection.py |

## Perl and Shell Scripts ##

| Name | Purpose |
|------|---------|
| `associate_loop.sh`              | Use this script to associate stations between SSIDs A and B |
| `attenuator_series_example.csv`  | Example of CSV input for a series of attenuator settings |
| `attenuator_series.pl`           | Reads a CSV of attenuator settings and replays them to CT70X programmble attenuator |
| `ftp-upload.pl`                  | Use this script to collect and upload station data to FTP site |
| `imix.pl`                        | packet loss survey tool |
| `lf_associate_ap.pl`             | LANforge server script for associating virtual stations to an chosen SSID |
| `lf_attenmod.pl`                 | This program is used to modify the LANforge attenuator through the LANforge |
| `lf_auto_wifi_cap.pl`            | This program is used to automatically run LANforge-GUI WiFi Capacity tests |
| `lf_cmc_macvlan.pl`              | Stress test sets up traffic types of udp , tcp , continuously starts and stops the connections  |
| `lf_create_bcast.pl`             | creates a L3 broadcast connection |
| `lf_cycle_wanlinks.pl`           | example of how to call lf_icemod.pl from a script |
| `lf_endp_script.pl`              | create a hunt script on a L3 connection endpoint |
| `lf_firemod.pl`                  | queries and modifies L3 connections |
| `lf_generic_ping.pl`             | Generate a batch of Generic lfping endpoints |
| `lf_gui_cmd.pl`                  | Initiate a stress test  |
| `lf_icemod.pl`                   | queries and modified WANLink connections |
| `lf_ice.pl`                      | adds and configures wanlinks |
| `lf_l4_auth.pl`                  | example of scripting L4 http script with basic auth |
| `lf_l4_reset.sh`                 | reset any layer 4 connection that reaches 0 Mbps over last minute |
| `lf_log_parse.pl`                | Convert the timestamp in LANforge logs (it is in unix-time, miliseconds) to readable date |
| `lf_loop_traffic.sh`             | Repeatedly start and stop a L3 connection |
| `lf_macvlan_l4.pl`               | Set up connection types: lf_udp, lf_tcp across 1 real port and many macvlan ports on 2 machines. Then continously starts and stops the connections. |
| `lf_mcast.bash`                  | Create a multicast L3 connection endpoint |
| `lf_monitor.pl`                  | Monitor L4 connections |
| `lf_nfs_io.pl`                   | Creates and runs NFS connections |
| `lf_parse_tshark_log.pl`         | Basic parsing of tshark logs |
| `lf_portmod.pl`                  | Queries and changes LANforge physical and virtual ports |
| `lf_port_walk.pl`                | Creates a series of connections, useful for basic firewall testing |
| `lf_show_events.pl`              | Displays and clears LANforge event log |
| `lf_staggered_dl.sh`             | his script starts a series of Layer-3 connections across a series of stations each station will wait $nap seconds, download $quantity KB and then remove its old CX. |
| `lf_sta_name.pl`                 | Use this script to alter a virtual station names |
| `lf_verify.pl`                   | Creates a basic L3 connection to verify that two ethernet ports are physically connected |
| `lf_voip.pl`                     | Creates series of VOIP connections between two LANforge machines |
| `lf_voip_test.pl`                | Creates series of VOIP connections and runs them |
| `lf_vue_mod.sh`                  | Bash script that wraps common operations for Virtual User Endpoint operations done by `lf_associate_ap` |
| `lf_wifi_rest_example.pl`        | Example script that queries a LF GUI for JSON data and displays a slice of it |
| `lf_zlt_binary.pl`               | Configures a Zero Loss Throughput test |
| `list_phy_sta.sh`                | Lists virtual stations backed by specified physical radio |
| `min_max_ave_station.pl`         | This script looks for min-max-average bps for rx-rate in a station csv data file |
| `multi_routers.pl`               | Routing cleanup script that can be used with virtual routers |
| `print_udev.sh`                  | Prints out Linux Udev rules describing how to name ports by MAC address |
| `sensorz.pl`                     | Displays temperature readings for CPU and ATH10K radios |
| `show-port-from-json.pl`         | Example script showing how to display a slice from a JSON GUI response |
| `station-toggle.sh`              | Use this script to toggle a set of stations on or off |
| `sysmon.sh`                      | grabs netdev stats and timestamp every second or so, saves to logfile.  |
| `test_refcnt.pl`                 | creates MAC-VLANs and curl requests for each |
| `topmon.sh`                      | LANforge system monitor that can be used from cron |
| `wait_on_ports.pl`               | waits on ports to have IP addresses, can up/down port to stimulate new DHCP lease |
| `wifi-roaming-times.pl`          | parses `wpa_supplicant_log.wiphyX` file to determine roaming times |

### LANForge Monitoring ###
From LANforge cli on port 4001 do a 'show_event' to see events from LANforge

### Compatibility ###
Scripts will be kept backwards and forwards compatible with LANforge
releases as much as possible.

### Installation ###
These scripts call each other and rely on the structure of this directory. To use these scripts in other locations,
such as your laptop, either copy the entire scripts directory or do a __git clone__ of this repository. Just copying
one script to a separate directory is going to break its requirements.

### Requirements ###
The perl scripts require the following perl packages to be installed. Most of these
perl packages are available through your repository as `.deb` or `.rpm` packages.

| Perl Package       | RPM              | Required       |
| -------------------|------------------|----------------|
| Net::Telnet        | perl-Net-Telnet |  Yes            |
| JSON               | perl-JSON       |  Yes, for JSON parsing |
| JSON::PrettyPrint  | perl-JSON-PP    |  No, useful for debugging |

| Python3 Package  |  RPM    | Required    |
|-------------------------|-----------|---------------|
| Pexpect                 | python3-pexpect | yes |
| XlsxWriter             | python3-xlsxwriter | yes, Xlsx output |


#### Pip v Pip3 ####
Please use pip3, we are targeting Python 3 with our scripts. If your pip/pip3 repositories have a difficult time connecting,
it's likely that you are trying to download from **pypi.python.org**. This is a deprecated location. Please update
using the **pypi.org** servers. Consider updating your ``~/.pypirc`` file:

````
[distutils]
index-servers =  
    pypi  

[pypi]  
repository: https://upload.pypi.org/legacy/
````


As [described on Python.org](https://packaging.python.org/guides/migrating-to-pypi-org/).

### License ###
Code in this repository is released under the BSD license (see license.txt).


### Support ###
Please contact support@candelatech.com if you have any questions.

_Thanks,
Ben_
