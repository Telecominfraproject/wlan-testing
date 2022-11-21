#!/usr/bin/env python3
import sys
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)
if 'py-json' not in sys.path:
    sys.path.append('py-json')
import traceback

from LANforge import LFUtils
from LANforge.LFUtils import *
from LANforge.lfcli_base import LFCliBase
from generic_cx import GenericCx

mgrURL = "http://localhost:8080/"
staName = "sta0"
staNameUri = "port/1/1/" + staName
suppress_related = True

class ConnectTest(LFCliBase):
    def __init__(self, lfhost, lfport):
        super().__init__(lfhost, lfport, True)
        super().check_connect()

    # compare pre-test values to post-test values
    @staticmethod
    def CompareVals(_name, preVal, postVal):
        print("Comparing %s" % _name)
        if postVal > preVal:
            print("     Test Passed")
        else:
            print(" Test Failed: %s did not increase after 5 seconds" % _name)

    def run(self):
        print("See home/lanforge/Documents/connectTestLogs/connectTestLatest for specific values on latest test")

        eth1IP = super().json_get("/port/1/1/eth1")
        if eth1IP['interface']['ip'] == "0.0.0.0":
            print("Warning: Eth1 lacks ip address")
            exit(1)

        # Create stations and turn dhcp on
        print("Creating station and turning on dhcp")

        response = super().json_get("/" + staNameUri)
        if response is not None:
            if response["interface"] is not None:
                print("removing old station")
                removePort(1, staName, mgrURL)
                waitUntilPortsDisappear(mgrURL, [staName])
                time.sleep(1)

        url = "cli-json/add_sta"
        data = {
            "shelf": 1,
            "resource": 1,
            "radio": "wiphy0",
            "sta_name": staName,
            "ssid": "jedway-wpa2-x2048-4-4",
            "key": "jedway-wpa2-x2048-4-4",
            "mode": 0,
            "mac": "xx:xx:xx:xx:*:xx",
            "flags": (0x400 + 0x20000 + 0x1000000000)  # create admin down
        }
        super().json_post(url, data, suppress_related_commands_=suppress_related)
        wait_until_ports_appear(mgrURL, [staName], True)
        time.sleep(8)
        reqURL = "cli-json/set_port"
        data = {
            "shelf": 1,
            "resource": 1,
            "port": staName,
            "current_flags": (0x1 + 0x80000000),
            "interest": (0x2 + 0x4000 + 0x800000)  # current, dhcp, down,
        }
        super().json_post(reqURL, data, suppress_related_commands_=suppress_related)
        time.sleep(0.5)
        super().json_post("cli-json/set_port", portUpRequest(1, staName))

        reqURL = "cli-json/nc_show_ports"
        data = {"shelf": 1,
                "resource": 1,
                "port": staName,
                "probe_flags": 1}
        super().json_post(reqURL, data, suppress_related_commands_=suppress_related)
        time.sleep(0.5)
        waitUntilPortsAdminUp(1, mgrURL, [staName])

        duration = 0
        maxTime = 300
        ip = "0.0.0.0"
        while (ip == "0.0.0.0") and (duration < maxTime):
            station_info = super().json_get("/" + staNameUri + "?fields=port,ip")
            LFUtils.debug_printer.pprint(station_info)
            if (station_info is not None) and ("interface" in station_info) and ("ip" in station_info["interface"]):
                ip = station_info["interface"]["ip"]
            if ip == "0.0.0.0":
                duration += 4
                time.sleep(4)
            else:
                break

        if duration >= maxTime:
            print(staName+" failed to get an ip. Ending test")
            print("Cleaning up...")
            removePort(1, staName, mgrURL)
            sys.exit(1)

        print("Creating endpoints and cross connects")

        #==============| ENDPOINT CREATION |=================
        # create l4 endpoint
        url = "/cli-json/add_l4_endp"
        data = {
            "alias": "l4Test",
            "shelf": 1,
            "resource": 1,
            "port": staName,
            "type": "l4_generic",
            "timeout": 1000,
            "url_rate": 600,
            "url": "dl http://localhost/ /dev/null",
            "proxy_port" : "NA"
        }
        super().json_post(url, data, suppress_related_commands_=suppress_related)
        data = {
            "endpoint": "all"
        }
        super().json_post("/cli-json/nc_show_endpoints", data, suppress_related_commands_=suppress_related)
        time.sleep(5)

        # create fileio endpoint
        url = "/cli-json/add_file_endp"
        data = {
            "alias": "fioTest",
            "shelf": 1,
            "resource": 1,
            "port": staName,
            "type": "fe_nfs",
            "directory": "/mnt/fe-test"
        }
        super().json_post(url, data, suppress_related_commands_=suppress_related)
        time.sleep(1)
        data = {
            "endpoint": "all"
        }
        super().json_post("/cli-json/nc_show_endpoints", data)
        time.sleep(1)

        # create generic endpoints
        genl = GenericCx(lfclient_host=self.lfclient_host, lfclient_port=self.lfclient_port)
        genl.createGenEndp("genTest1", 1, 1, staName, "gen_generic")
        genl.createGenEndp("genTest2", 1, 1, staName, "gen_generic")
        genl.setFlags("genTest1", "ClearPortOnStart", 1)
        genl.setFlags("genTest2", "ClearPortOnStart", 1)
        genl.setFlags("genTest2", "Unmanaged", 1)
        genl.setCmd("genTest1", "lfping  -i 0.1 -I %s 10.40.0.1" % staName)
        time.sleep(.05)
        data = {
            "endpoint": "all"
        }
        super().json_post("/cli-json/nc_show_endpoints", data, suppress_related_commands_=suppress_related)

        # create redirects for wanlink
        url = "/cli-json/add_rdd"
        data = {
            "shelf": 1,
            "resource": 1,
            "port": "rdd0",
            "peer_ifname": "rdd1"
        }
        super().json_post(url, data, suppress_related_commands_=suppress_related)

        url = "/cli-json/add_rdd"
        data = {
            "shelf": 1,
            "resource": 1,
            "port": "rdd1",
            "peer_ifname": "rdd0"
        }
        super().json_post(url, data, suppress_related_commands_=suppress_related)
        time.sleep(.05)

        # reset redirect ports
        url = "/cli-json/reset_port"
        data = {
            "shelf": 1,
            "resource": 1,
            "port": "rdd0"
        }
        super().json_post(url, data, suppress_related_commands_=suppress_related)

        url = "/cli-json/reset_port"
        data = {
            "shelf": 1,
            "resource": 1,
            "port": "rdd1"
        }
        super().json_post(url, data, suppress_related_commands_=suppress_related)
        time.sleep(.05)

        # create wanlink endpoints
        url = "/cli-json/add_wl_endp"
        data = {
            "alias": "wlan0",
            "shelf": 1,
            "resource": 1,
            "port": "rdd0",
            "latency": 20,
            "max_rate": 1544000
        }
        super().json_post(url, data, suppress_related_commands_=suppress_related)

        url = "/cli-json/add_wl_endp"
        data = {
            "alias": "wlan1",
            "shelf": 1,
            "resource": 1,
            "port": "rdd1",
            "latency": 30,
            "max_rate": 1544000
        }
        super().json_post(url, data, suppress_related_commands_=suppress_related)
        time.sleep(.05)
        data = {
            "endpoint": "all"
        }
        super().json_post("/cli-json/nc_show_endpoints", data, suppress_related_commands_=suppress_related)

        time.sleep(10)

        #==============| CX CREATION |===================
        # create cx for tcp and udp
        cmd = ("./lf_firemod.pl --action create_cx --cx_name testTCP --use_ports %s,eth1 --use_speeds  360000,"
               "150000 --endp_type tcp > ~/Documents/connectTestLogs/connectTestLatest.log" % staName)
        execWrap(cmd)
        cmd = ("./lf_firemod.pl --action create_cx --cx_name testUDP --use_ports %s,eth1 --use_speeds  360000,"
               "150000 --endp_type udp >> ~/Documents/connectTestLogs/connectTestLatest.log" % staName)
        execWrap(cmd)
        time.sleep(.05)

        # create cx for l4_endp
        url = "/cli-json/add_cx"
        data = {
            "alias": "CX_l4Test",
            "test_mgr": "default_tm",
            "tx_endp": "l4Test",
            "rx_endp": "NA"
        }
        super().json_post(url, data, suppress_related_commands_=suppress_related)
        time.sleep(.05)

        # create fileio cx
        url = "/cli-json/add_cx"
        data = {
            "alias": "CX_fioTest",
            "test_mgr": "default_tm",
            "tx_endp": "fioTest",
            "rx_endp": "NA"
        }
        super().json_post(url, data, suppress_related_commands_=suppress_related)
        time.sleep(.05)

        # create generic cx
        url = "/cli-json/add_cx"
        data = {
            "alias": "CX_genTest1",
            "test_mgr": "default_tm",
            "tx_endp": "genTest1",
            "rx_endp": "genTest2"
        }
        super().json_post(url, data, suppress_related_commands_=suppress_related)
        time.sleep(.05)

        # create wanlink cx
        url = "/cli-json/add_cx"
        data = {
            "alias": "CX_wlan0",
            "test_mgr": "default_tm",
            "tx_endp": "wlan0",
            "rx_endp": "wlan1"
        }
        super().json_post(url, data, suppress_related_commands_=suppress_related)
        time.sleep(.5)
        data = {
            "endpoint": "all"
        }
        super().json_post("/cli-json/nc_show_endpoints", data, suppress_related_commands_=suppress_related)

        cxNames = ["testTCP", "testUDP", "CX_l4Test", "CX_fioTest", "CX_genTest1", "CX_wlan0"]

        # get data before running traffic
        try:
            get_info = {}
            sleep(5)
            get_info['testTCPA'] = super().json_get("/endp/testTCP-A?fields=tx+bytes,rx+bytes")
            get_info['testTCPB'] = super().json_get("/endp/testTCP-B?fields=tx+bytes,rx+bytes")
            get_info['testUDPA'] = super().json_get("/endp/testUDP-A?fields=tx+bytes,rx+bytes")
            get_info['testUDPB'] = super().json_get("/endp/testUDP-B?fields=tx+bytes,rx+bytes")
            get_info['l4Test'] = super().json_get("/layer4/l4Test?fields=bytes-rd")
            get_info['genTest1'] = super().json_get("/generic/genTest1?fields=last+results")
            get_info['wlan0'] = super().json_get("/wl_ep/wlan0")
            get_info['wlan1'] = super().json_get("/wl_ep/wlan1")

            for name in get_info:
                #print("==================\n"+name+"\n====================")
                if 'endpoint' not in get_info[name]:
                    print(get_info[name])
                    raise ValueError ("%s missing endpoint value" % name)

            testTCPATX = get_info['testTCPA']['endpoint']['tx bytes']
            testTCPARX = get_info['testTCPA']['endpoint']['rx bytes']
            testTCPBTX = get_info['testTCPB']['endpoint']['tx bytes']
            testTCPBRX = get_info['testTCPB']['endpoint']['rx bytes']

            testUDPATX = get_info['testUDPA']['endpoint']['tx bytes']
            testUDPARX = get_info['testUDPA']['endpoint']['rx bytes']
            testUDPBTX = get_info['testUDPB']['endpoint']['tx bytes']
            testUDPBRX = get_info['testUDPB']['endpoint']['rx bytes']

            l4TestBR = get_info['l4Test']['endpoint']['bytes-rd']
            genTest1LR = get_info['genTest1']['endpoint']['last results']

            wlan0TXB = get_info['wlan0']['endpoint']['tx bytes']
            wlan0RXP = get_info['wlan0']['endpoint']['rx pkts']
            wlan1TXB = get_info['wlan1']['endpoint']['tx bytes']
            wlan1RXP = get_info['wlan1']['endpoint']['rx pkts']
        except Exception as e:
            print("Something went wrong")
            print(e)
            print("Cleaning up...")
            time.sleep(15)
            LFUtils.removePort(1, staName, mgrURL)
            endpNames = ["testTCP-A", "testTCP-B",
                         "testUDP-A", "testUDP-B",
                         "l4Test", "fioTest",
                         "genTest1", "genTest2",
                         "wlan0", "wlan1"]
            removeCX(mgrURL, cxNames)
            removeEndps(mgrURL, endpNames)
            traceback.print_stack()
            sys.exit(1)

        # start cx traffic
        print("\nStarting CX Traffic")
        for name in range(len(cxNames)):
            cmd = (
                "./lf_firemod.pl --mgr localhost --quiet yes --action do_cmd --cmd \"set_cx_state default_tm %s RUNNING\" >> /tmp/connectTest.log" % (cxNames[name]))
            execWrap(cmd)

        # print("Sleeping for 5 seconds")
        time.sleep(5)

        # show tx and rx bytes for ports

        os.system("echo  eth1 >> ~/Documents/connectTestLogs/connectTestLatest.log")
        cmd = (
            "./lf_portmod.pl --quiet 1 --manager localhost --port_name eth1 --show_port \"Txb,Rxb\" >> ~/Documents/connectTestLogs/connectTestLatest.log")
        execWrap(cmd)
        os.system("echo  %s >> ~/Documents/connectTestLogs/connectTestLatest.log" % staName)
        cmd = (
            "./lf_portmod.pl --quiet 1 --manager localhost --port_name %s --show_port \"Txb,Rxb\" >> ~/Documents/connectTestLogs/connectTestLatest.log" % staName)
        execWrap(cmd)

        # show tx and rx for endpoints PERL
        os.system("echo  TestTCP-A >> ~/Documents/connectTestLogs/connectTestLatest.log")
        cmd = (
            "./lf_firemod.pl --action show_endp --endp_name testTCP-A --endp_vals \"Tx Bytes,Rx Bytes\" >> ~/Documents/connectTestLogs/connectTestLatest.log")
        execWrap(cmd)
        os.system("echo  TestTCP-B >> ~/Documents/connectTestLogs/connectTestLatest.log")
        cmd = (
            "./lf_firemod.pl --action show_endp --endp_name testTCP-B --endp_vals  \"Tx Bytes,Rx Bytes\" >> ~/Documents/connectTestLogs/connectTestLatest.log")
        execWrap(cmd)
        os.system("echo  TestUDP-A >> ~/Documents/connectTestLogs/connectTestLatest.log")
        cmd = (
            "./lf_firemod.pl --action show_endp --endp_name testUDP-A --endp_vals  \"Tx Bytes,Rx Bytes\" >> ~/Documents/connectTestLogs/connectTestLatest.log")
        execWrap(cmd)
        os.system("echo  TestUDP-B >> ~/Documents/connectTestLogs/connectTestLatest.log")
        cmd = (
            "./lf_firemod.pl --action show_endp --endp_name testUDP-B --endp_vals  \"Tx Bytes,Rx Bytes\" >> ~/Documents/connectTestLogs/connectTestLatest.log")
        execWrap(cmd)
        os.system("echo  l4Test >> ~/Documents/connectTestLogs/connectTestLatest.log")
        cmd = (
            "./lf_firemod.pl --action show_endp --endp_name l4Test --endp_vals Bytes-Read-Total >> ~/Documents/connectTestLogs/connectTestLatest.log")
        execWrap(cmd)
        os.system("echo  fioTest >> ~/Documents/connectTestLogs/connectTestLatest.log")
        cmd = (
            "./lf_firemod.pl --action show_endp --endp_name fioTest --endp_vals \"Bytes Written,Bytes Read\" >> ~/Documents/connectTestLogs/connectTestLatest.log")
        execWrap(cmd)
        os.system("echo  genTest1 >> ~/Documents/connectTestLogs/connectTestLatest.log")
        cmd = (
            "./lf_firemod.pl --action show_endp --endp_name genTest1 >> ~/Documents/connectTestLogs/connectTestLatest.log")
        execWrap(cmd)
        os.system("echo  wlan0 >> ~/Documents/connectTestLogs/connectTestLatest.log")
        cmd = (
            "./lf_firemod.pl --action show_endp --endp_name wlan0 --endp_vals \"Rx Pkts,Tx Bytes,Cur-Backlog,Dump File,Tx3s\" >> ~/Documents/connectTestLogs/connectTestLatest.log")
        execWrap(cmd)
        os.system("echo  wlan1 >> ~/Documents/connectTestLogs/connectTestLatest.log")
        cmd = (
            "./lf_firemod.pl --action show_endp --endp_name wlan1 --endp_vals \"Rx Pkts,Tx Bytes,Cur-Backlog,Dump File,Tx3s\" >> ~/Documents/connectTestLogs/connectTestLatest.log")
        execWrap(cmd)

        # stop cx traffic
        print("Stopping CX Traffic")
        for name in range(len(cxNames)):
            cmd = (
                "./lf_firemod.pl --mgr localhost --quiet yes --action do_cmd --cmd \"set_cx_state default_tm %s STOPPED\"  >> /tmp/connectTest.log" % (cxNames[name]))
            execWrap(cmd)
        # print("Sleeping for 15 seconds")
        time.sleep(15)

        # get data for endpoints JSON
        print("Collecting Data")
        try:

            ptestTCPA = super().json_get("endp/testTCP-A?fields=tx+bytes,rx+bytes")
            ptestTCPATX = ptestTCPA['endpoint']['tx bytes']
            ptestTCPARX = ptestTCPA['endpoint']['rx bytes']

            ptestTCPB = super().json_get("/endp/testTCP-B?fields=tx+bytes,rx+bytes")
            ptestTCPBTX = ptestTCPB['endpoint']['tx bytes']
            ptestTCPBRX = ptestTCPB['endpoint']['rx bytes']

            ptestUDPA = super().json_get("/endp/testUDP-A?fields=tx+bytes,rx+bytes")
            ptestUDPATX = ptestUDPA['endpoint']['tx bytes']
            ptestUDPARX = ptestUDPA['endpoint']['rx bytes']

            ptestUDPB = super().json_get("/endp/testUDP-B?fields=tx+bytes,rx+bytes")
            ptestUDPBTX = ptestUDPB['endpoint']['tx bytes']
            ptestUDPBRX = ptestUDPB['endpoint']['rx bytes']

            pl4Test = super().json_get("/layer4/l4Test?fields=bytes-rd")
            pl4TestBR = pl4Test['endpoint']['bytes-rd']

            pgenTest1 = super().json_get("/generic/genTest1?fields=last+results")
            pgenTest1LR = pgenTest1['endpoint']['last results']

            pwlan0 = super().json_get("/wl_ep/wlan0")
            pwlan0TXB = pwlan0['endpoint']['tx bytes']
            pwlan0RXP = pwlan0['endpoint']['rx pkts']
            pwlan1 = super().json_get("/wl_ep/wlan1")
            pwlan1TXB = pwlan1['endpoint']['tx bytes']
            pwlan1RXP = pwlan1['endpoint']['rx pkts']
        except Exception as e:
            print("Something went wrong")
            print(e)
            print("Cleaning up...")
            time.sleep(15)
            reqURL = "/cli-json/rm_vlan"
            data = {
                "shelf": 1,
                "resource": 1,
                "port": staName
            }
            super().json_post(reqURL, data, suppress_related_commands_=suppress_related)

            endpNames = ["testTCP-A", "testTCP-B",
                         "testUDP-A", "testUDP-B",
                         "l4Test", "fioTest",
                         "genTest1", "genTest2",
                         "wlan0", "wlan1"]
            removeCX(mgrURL, cxNames)
            removeEndps(mgrURL, endpNames)
            sys.exit(1)

        # print("Sleeping for 5 seconds")
        time.sleep(5)

        print("\n")
        self.CompareVals("testTCP-A TX", testTCPATX, ptestTCPATX)
        self.CompareVals("testTCP-A RX", testTCPARX, ptestTCPARX)
        self.CompareVals("testTCP-B TX", testTCPBTX, ptestTCPBTX)
        self.CompareVals("testTCP-B RX", testTCPBRX, ptestTCPBRX)
        self.CompareVals("testUDP-A TX", testUDPATX, ptestUDPATX)
        self.CompareVals("testUDP-A RX", testUDPARX, ptestUDPARX)
        self.CompareVals("testUDP-B TX", testUDPBTX, ptestUDPBTX)
        self.CompareVals("testUDP-B RX", testUDPBRX, ptestUDPBRX)
        self.CompareVals("l4Test Bytes Read", l4TestBR, pl4TestBR)
        self.CompareVals("genTest1 Last Results", genTest1LR, pgenTest1LR)
        self.CompareVals("wlan0 TX Bytes", wlan0TXB, pwlan0TXB)
        self.CompareVals("wlan0 RX Pkts", wlan0RXP, pwlan0RXP)
        self.CompareVals("wlan1 TX Bytes", wlan1TXB, pwlan1TXB)
        self.CompareVals("wlan1 RX Pkts", wlan1RXP, pwlan1RXP)
        print("\n")

        # remove all endpoints and cxs
        print("Cleaning up...")
        LFUtils.removePort(1, staName, mgrURL)

        endpNames = ["testTCP-A", "testTCP-B",
                     "testUDP-A", "testUDP-B",
                     "l4Test", "fioTest",
                     "genTest1", "genTest2",
                     "wlan0", "wlan1"]
        removeCX(mgrURL, cxNames)
        removeEndps(mgrURL, endpNames)


# ~class

def main():
    lfclient_host = "localhost"
    lfclient_port = 8080
    test = ConnectTest(lfclient_host, lfclient_port)
    test.run()


if __name__ == "__main__":
    main()
