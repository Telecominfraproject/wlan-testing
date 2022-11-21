#!/usr/bin/python3
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# example of how to create a LANforge station                                 -
#                                                                             -
# two examples, first using the URL-Encoded POST                              -
# second using JSON POST data                                                 -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import sys
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()
import argparse
import logging
import time
from time import sleep
import pprint
import LANforge
from LANforge import LFRequest
from LANforge import LFUtils
from LANforge.LFUtils import NA

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def main():
    host = "localhost"
    base_url = "http://%s:8080"%host
    resource_id = 1     # typically you're using resource 1 in stand alone realm
    radio = "wiphy0"
    start_id = 200
    end_id = 202
    padding_number = 10000 # the first digit of this will be deleted
    ssid = "jedway-wpa2-x2048-4-1"
    passphrase = "jedway-wpa2-x2048-4-1"

    parser = argparse.ArgumentParser(description="test creating a station")
    parser.add_argument("-m", "--host", type=str, help="json host to connect to")
    parser.add_argument("-r", "--radio", type=str, help="radio to create a station on")
    parser.add_argument("-a", "--start_id", type=int, help="starting station id")
    parser.add_argument("-b", "--end_id", type=int, help="ending station id")
    parser.add_argument("-s", "--ssid", type=str, help="station ssid")
    parser.add_argument("-p", "--passwd", type=str, help="password for ssid")

    args = None
    try:
      args = parser.parse_args()
      if (args.host is not None):
         host = args.host,
         baseurl = base_url = "http://%s:8080"%host
      if (args.radio is not None):
         radio = args.radio
      if (args.start_id is not None):
         start_id = args.start_id
      if (args.end_id is not None):
         end_id = args.end_id
      if (args.ssid is not None):
         ssid = args.ssid
      if (args.passwd is not None):
         passphrase = args.passwd
    except Exception as e:
      logging.exception(e)
      usage()
      exit(2)

    # station numbers are heavily manipulated strings, often using manual padding
    # sta200 is not sta0200 nor sta00200, and we can format these numbers by adding
    # a 1000 or 10000 to the station id, and trimming the first digit off

    j_printer = pprint.PrettyPrinter(indent=2)
    json_post = ""
    json_response = ""
    found_stations = []
    lf_r = LFRequest.LFRequest(base_url+"/port/1/1/wiphy0")
    wiphy0_json = lf_r.getAsJson()
    if (wiphy0_json is None) or (wiphy0_json['interface'] is None):
        print("Unable to find radio. Are we connected?")
        exit(1)

    # If you need to inspect a radio....
    #print("# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    #print("# radio wiphy0                                              -")
    #print("# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    #LFUtils.debug_printer.pprint(wiphy0_json['interface']['alias'])
    #parent_radio_mac = wiphy0_json['interface']['mac']
    #print("# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Example 1                                                 -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # This section uses URLs /cli-form/rm_vlan, /cli-form/add_sta
    # The /cli-form URIs take URL-encoded form posts
    #
    # For each of the station names, delete them if they exist. It
    # takes a few milliseconds to delete them, so after deleting them
    # you need to poll until they don't appear.
    #
    # NOTE: the ID field of the EID is ephemeral, so best stick to
    # requesting the station name. The station name can be formatted
    # with leading zeros, sta00001 is legal
    # and != {sta0001, sta001, sta01, or sta1}

    desired_stations = LFUtils.portNameSeries("sta", start_id, end_id, padding_number)
    #LFUtils.debug_printer.pprint(desired_stations)
    print("Example 1: will create stations %s"%(",".join(desired_stations)))
    for sta_name in desired_stations:
        url = base_url+"/port/1/%s/%s" % (resource_id, sta_name)
        print("Ex 1: Checking for station : "+url)
        lf_r = LFRequest.LFRequest(url)
        json_response = lf_r.getAsJson(show_error=False)
        if (json_response != None):
            found_stations.append(sta_name)

    for sta_name in found_stations:
        print("Ex 1: Deleting station %s ...."%sta_name)
        lf_r = LFRequest.LFRequest(base_url+"/cli-form/rm_vlan")
        lf_r.addPostData( {
            "shelf":1,
            "resource": resource_id,
            "port": sta_name,
            "suppress_preexec_cli": "yes",
            "suppress_preexec_method": 1
        })
        json_response = lf_r.formPost()
        sleep(0.05) # best to give LANforge a few millis between rm_vlan commands

    LFUtils.waitUntilPortsDisappear(resource_id, base_url, found_stations)

    print("Ex 1: Next we create stations...")
    #68727874560 was previous flags
    for sta_name in desired_stations:
        print("Ex 1: Next we create station %s"%sta_name)
        lf_r = LFRequest.LFRequest(base_url+"/cli-form/add_sta")
        # flags are a decimal equivalent of a hexadecimal bitfield
        # you can submit as either 0x(hex) or (dec)
        # a helper page is available at http://localhost:8080/help/add_sta
        #
        # You can watch console output of the LANforge GUI client when you
        # get errors to this command, and you can also watch the websocket
        # output for a response to this command at ws://localhost:8081
        # Use wsdump ws://localhost:8081/
        #
        # modes are listed at http://<YOUR_LANFORGE>/LANforgeDocs-5.4.1/lfcli_ug.html
        # or at https://www.candelatech.com/lfcli_ug.html
        #
        # mac address field is a pattern for creation: entirely random mac addresses
        # do not take advantage of address mask matchin in Ath10k hardware, so we developed
        # this pattern to randomize a section of octets. XX: keep parent, *: randomize, and
        # chars [0-9a-f]: use this digit
        #
        # If you get errors like "X is invalid hex chara cter", this indicates a previous
        # rm_vlan call has not removed your station yet: you cannot rewrite mac addresses
        # with this call, just create new stations
        lf_r.addPostData( LFUtils.staNewDownStaRequest(sta_name, resource_id=resource_id, radio=radio, ssid=ssid, passphrase=passphrase))
        lf_r.formPost()
        sleep(0.1)

    LFUtils.waitUntilPortsAppear(resource_id, base_url, desired_stations)
    for sta_name in desired_stations:
        sleep(1)
        print("doing portSetDhcpDownRequest on "+sta_name)
        lf_r = LFRequest.LFRequest(base_url+"/cli-form/set_port")
        lf_r.addPostData( LFUtils.portSetDhcpDownRequest(resource_id, sta_name))
        lf_r.formPost()


    # the LANforge API separates STA creation and ethernet port settings
    # We need to revisit the stations we create and amend flags to add
    # things like DHCP or ip+gateway, admin-{up,down}

    LFUtils.waitUntilPortsAppear(resource_id, base_url, desired_stations)
    for sta_name in desired_stations:
        sleep(1)
        print("Ex 1: station up %s"%sta_name)
        lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_port")
        data = LFUtils.portDhcpUpRequest(resource_id, sta_name)
        lf_r.addPostData(data)
        lf_r.jsonPost()


    LFUtils.waitUntilPortsAppear(resource_id, base_url, desired_stations)
    # for sta_name in desired_stations:
    #     print("Ex 1: sta down %s"%sta_name)
    #     lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_port")
    #     lf_r.addPostData(LFUtils.portDownRequest(resource_id, sta_name))
    #     lf_r.jsonPost()
    #     sleep(0.05)
    print("...done with example 1\n\n")
    sleep(4)


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Example 2                                                 -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # uses URLs /cli-json/rm_vlan, /cli-json/add_sta
    # and those accept POST in json formatted text
    desired_stations = []
    found_stations = []
    start_id = 220
    end_id = 222
    desired_stations = LFUtils.portNameSeries("sta", start_id, end_id, padding_number)

    print("Example 2: using port list to find stations")
    sleep(1)
    url = base_url+"/port/1/%s/list?fields=alias" % (resource_id)
    lf_r = LFRequest.LFRequest(url)
    json_response = lf_r.getAsJson()
    if json_response is None:
        raise Exception("no reponse to: "+url)
    port_map = LFUtils.portListToAliasMap(json_response)
    #LFUtils.debug_printer.pprint(port_map)

    for sta_name in desired_stations:
        print("Ex 2: checking for station : "+sta_name)
        if sta_name in port_map.keys():
            #print("found station : "+sta_name)
            found_stations.append(sta_name)

    for sta_name in found_stations:
        print("Ex 2: delete station %s ..."%sta_name)
        lf_r = LFRequest.LFRequest(base_url+"/cli-json/rm_vlan")
        lf_r.addPostData({
                "shelf":1,
                "resource": resource_id,
                "port": sta_name
            })
        lf_r.jsonPost(show_error=False)
        sleep(0.05)

    LFUtils.waitUntilPortsDisappear(resource_id, base_url, found_stations)
    for sta_name in desired_stations:
        print("Ex 2: create station %s"%sta_name)
        lf_r = LFRequest.LFRequest(base_url+"/cli-json/add_sta")
        lf_r.addPostData(LFUtils.staNewDownStaRequest(sta_name, resource_id=resource_id, radio=radio, ssid=ssid, passphrase=passphrase))
        lf_r.jsonPost()
        sleep(1)

    LFUtils.waitUntilPortsAppear(resource_id, base_url, desired_stations)
    # the LANforge API separates STA creation and ethernet port settings
    # We need to revisit the stations we create and amend flags to add
    # things like DHCP or ip+gateway, admin-{up,down}
    for sta_name in desired_stations:
        print("Ex 2: set port %s"%sta_name)
        lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_port")
        data = LFUtils.portDhcpUpRequest(resource_id, sta_name)
        lf_r.addPostData(data)
        lf_r.jsonPost()
        sleep(0.05)

    print("...done with Example 2")
    sleep(1)

    print("Example 3: bring ports up and down")
    sleep(1)
    print("Ex 3: setting ports up...")
    desired_stations.insert(0, "sta0200")
    desired_stations.insert(1, "sta0201")
    desired_stations.insert(2, "sta0202")
    wait_for_these = []
    for sta_name in desired_stations:
        lf_r = LFRequest.LFRequest(base_url+"/port/1/%s/%s?fields=port,device,down"%(resource_id, sta_name))
        json_response = lf_r.getAsJson()
        if json_response['interface']['down'] is 'true':
            url = base_url+"/cli-json/set_port"
            lf_r = LFRequest.LFRequest(url)
            lf_r.addPostData(LFUtils.portDhcpUpRequest(resource_id, sta_name))
            print("setting %s up"%sta_name)
            lf_r.jsonPost()
            wait_for_these.append(sta_name)
    LFUtils.waitUntilPortsAdminUp(resource_id, base_url, wait_for_these)
    sleep(4)
    print("Ex 3: setting ports down...")
    for sta_name in desired_stations:
        lf_r = LFRequest.LFRequest(base_url+"/port/1/%s/%s?fields=port,device,down"%(resource_id, sta_name))
        json_response = lf_r.getAsJson()
        if json_response['interface']['down'] is 'false':
            url = base_url+"/cli-json/set_port"
            lf_r = LFRequest.LFRequest(url)
            lf_r.addPostData(LFUtils.portDownRequest(resource_id, sta_name))
            print("setting %s down"%sta_name)
            lf_r.jsonPost()
            wait_for_these.append(sta_name)
    LFUtils.waitUntilPortsAdminDown(resource_id, base_url, wait_for_these)
    print("...ports are down")
    sleep(4)



    print("Example 4: Modify stations to mode /a")
    sleep(1)
    for sta_name in desired_stations:
        #lf_r = LFRequest.LFRequest(base_url+"/port/1/%s/%s"%(resource_id, sta_name))
        lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_port")
        lf_r.addPostData(LFUtils.portDownRequest(resource_id, sta_name))
        lf_r.jsonPost()
    LFUtils.waitUntilPortsAdminDown(resource_id, base_url, desired_stations)

    for sta_name in desired_stations:
        lf_r = LFRequest.LFRequest(base_url+"/cli-json/add_sta")
        lf_r.addPostData({
            "shelf":1,
            "resource": resource_id,
            "radio": radio,
            "sta_name": sta_name,
            "mode": 1, # 802.11a see http://www.candelatech.com/lfcli_ug.php#add_sta
        })
        print("using add_sta to set %s mode"%sta_name)
        lf_r.jsonPost()
        sleep(0.5)

    for sta_name in desired_stations:
        lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_port")
        lf_r.addPostData(LFUtils.portUpRequest(resource_id, sta_name))
        lf_r.get()
    LFUtils.waitUntilPortsAdminUp(resource_id, base_url, desired_stations)
    print("...done")
    sleep(4)


    print("Example 5: change station encryption from wpa2 to wpa3...")
    sleep(1)
    for sta_name in desired_stations:
        #lf_r = LFRequest.LFRequest(base_url+"/port/1/%s/%s"%(resource_id, sta_name))
        lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_port")
        lf_r.addPostData(LFUtils.portDownRequest(resource_id, sta_name))
        lf_r.get()
    LFUtils.waitUntilPortsAdminDown(resource_id, base_url, desired_stations)

    for sta_name in desired_stations:
        lf_r = LFRequest.LFRequest(base_url+"/cli-json/add_sta")
        lf_r.addPostData({
            "shelf":1,
            "resource": resource_id,
            "radio": radio,
            "sta_name": sta_name,
            "mode": 0, # mode AUTO
            "flags": 1099511627776, # sets use-wpa3
            "flags_mask": 1099511628800 # sets interest in use-wpa3, wpa2_enable (becomes zero)
        })
        print("using add_sta to set %s wpa3"%sta_name)
        lf_r.jsonPost()
        sleep(0.5)

    for sta_name in desired_stations:
        lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_port")
        lf_r.addPostData(LFUtils.portUpRequest(resource_id, sta_name))
        lf_r.get()
    LFUtils.waitUntilPortsAdminUp(resource_id, base_url, desired_stations)
    print("...done")
    sleep(4)


    print("Example 7: alter TX power on %s..."%radio)
    # virtual stations do not have individual tx power states
    sleep(1)
    # see http://www.candelatech.com/lfcli_ug.php#set_wifi_radio
    lf_r = LFRequest.LFRequest(base_url+"/cli-json/set_wifi_radio")
    lf_r.addPostData({
        "shelf":1,
        "resource":resource_id,
        "radio":radio,
        "mode":NA,
        # tx power see: man 8 iwconfig, power is in dBm, auto or off
        "txpower": "auto",
        # meta flag tells lfclient to not check port before issuing command
        "suppress_preexec_method": "true",
    })
    lf_r.jsonPost()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":
   main()
