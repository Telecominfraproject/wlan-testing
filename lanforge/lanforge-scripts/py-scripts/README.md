# LANForge Python Scripts
This directory contains python scripts to intract with LANforge Wifi and Ethernet Traffic Generators for testing Access Points and other Wifi networks.

## LANforge Python Scripts in py-scripts General Classifications

* create_ - creates network element in LANforge wiphy radio
* lf_ or test_ - performs a test against an Access Point or Wifi network
* other files  are various utilities

## Still not sure what the script does ?
* LANforge scripts support --help , to provide a more detailed description of scripts functionality

## LANforge Python Scripts Directory Structure
* py-scripts - configuration, unit test, module, and library scripts
* cv_examples - bash scripts for ochastrating Chamberview tests 
* py-json - core libraries providing direct intraction with LANforge Traffic Generator
* py-json/LANforge - JSON intraction with LANforge Traffic Generator.
* lanforge_client/ - alpha version of JSON interface to LANforge Traffic Generator.

## Where is the create_basic_argparse and create_bare_argsparse?
* py-json/LANforge/lfcli_base.py 
## Updating scripts python library dependencies 
* for F27 systems from lanforge-scripts run: `pip3 install --user -r python.3.6.requirements.txt --upgrade`
* from lanforge-scripts run:  `pip3 install --user -r requirements.txt --upgrade`
## Scripts accessing Serial ports. 
* to access serial ports add user to `dialout` and `tty` groups to gain access to serial ports without needing root access.
* Most scripts run in user space to use the installed python package and not affect the os python packages.



## References
* https://www.candelatech.com/cookbook/cli/json-python
* http://www.candelatech.com/scripting_cookbook.php


# Getting Started

The first step is to make sure all dependencies are installed in your system.

## Example of running a chamber view test
### example from cv_examples/ferndale_ucentral.bash
* ./create_chamberview_dut.py : Replace arguments with your setup.  Separate your ssid arguments with spaces and ensure the names are lowercase
  * ./create_chamberview_dut.py --lfmgr `${MGR}` --port `${MGR_PORT}` --dut_name `${DUT}` \
  --ssid `"ssid_idx=0 ssid=Default-SSID-2g security=WPA2 password=12345678 bssid=c4:41:1e:f5:3f:24"` \
  --ssid `"ssid_idx=1 ssid=Default-SSID-5gl security=WPA2 password=12345678 bssid=c4:41:1e:f5:3f:25"` \
  --sw_version `"ucentral-01"` --hw_version `ea8450` --serial_num `1001` --model_num `8450`
* ./create_chamberview.py : change the lfmgr to your system, set the radio to a working radio on your LANforge system, same with the ethernet port.  Create/update chamber view scenario and apply and build it. Easiest way to get these lines is to build it in the GUI and then copy/tweak what it shows in the 'Text Output' tab after saving and re-opening the scenario.
  * ./create_chamberview.py --lfmgr `${MGR}` --port `${MGR_PORT}` --delete_scenario \
  --create_scenario `ucentral-scenario` \
  --raw_line `"profile_link 1.1 STA-AC 50 'DUT: $DUT Radio-1' NA wiphy0,AUTO -1 NA"` \
  --raw_line `"profile_link 1.1 STA-AC 50 'DUT: $DUT Radio-1' NA wiphy2,AUTO -1 NA"` \
  --raw_line `"profile_link 1.1 STA-AC 50 'DUT: $DUT Radio-2' NA wiphy1,AUTO -1 NA"` \
  --raw_line `"profile_link 1.1 STA-AC 46 'DUT: $DUT Radio-2' NA wiphy3,AUTO -1 NA"` \
  --raw_line `"profile_link 1.1 upstream-dhcp 1 NA NA $UPSTREAM,AUTO -1 NA" `\
  --raw_line `"profile_link 1.1 uplink-nat 1 'DUT: upstream LAN 192.168.100.1/24' NA $LF_WAN_PORT,$UPSTREAM -1 NA"` \
  --raw_line `"profile_link 1.1 STA-AC 1 'DUT: $DUT Radio-2' NA ALL-AX,AUTO -1 NA"`
* ./lf_wifi_capacity_test.py : Run capacity test on the stations created by the chamber view scenario.
  * ./lf_wifi_capacity_test.py --config_name Custom --pull_report --mgr `${MGR}` \
  --port `${MGR_PORT}` \
  --instance_name `testing` --upstream `1.1.$UPSTREAM` --test_rig `${TESTBED}` --graph_groups `${GROUP_FILE}` \
  --batch_size `"100"` --protocol `"TCP-IPv4"` --duration `20000`


