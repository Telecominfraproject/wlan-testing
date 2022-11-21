#!/usr/bin/env python3
"""
Candela Technologies Inc.

Info : Standard Script for Connection Testing -  Creates HTML and pdf report as a result (Used for web-console)

"""
import sys
import os
import importlib
import argparse
import datetime
import time
from test_utility import CreateHTML, StatusMsg
import pdfkit

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm

webconsole_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))


class ConnectionTest(LFCliBase):

    def __init__(self, lfclient_host="localhost", lfclient_port=8080, radio="wiphy1", sta_prefix="sta", start_id=0,
                 num_sta=2,
                 dut_ssid="lexusdut", dut_security="open", dut_passwd="[BLANK]", upstream="eth1", name_prefix="L3Test",
                 session_id="Layer3Test", test_name="Client/s Connectivity Test", pass_criteria=20, _debug_on=False,
                 _exit_on_error=False, _exit_on_fail=False):
        super().__init__(lfclient_host, lfclient_port, _debug=_debug_on, _exit_on_fail=_exit_on_fail)
        self.host = lfclient_host
        self.port = lfclient_port
        self.radio = radio
        self.upstream = upstream
        self.monitor_interval = 1
        self.sta_prefix = sta_prefix
        self.sta_start_id = start_id
        self.pass_criteria = pass_criteria
        self.num_sta = num_sta
        self.name_prefix = name_prefix
        self.ssid = dut_ssid
        self.security = dut_security
        self.password = dut_passwd
        self.session_id = session_id
        self.test_name = test_name
        self.test_duration = 1
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.pass_fail = ""
        self.status_msg = StatusMsg(lfclient_host=self.host, lfclient_port=self.port, session_id=self.session_id)
        station_list = []
        for i in range(0, self.num_sta):
            station_list.append(self.sta_prefix + str(i).zfill(4))
        self.station_data = dict.fromkeys(station_list)
        for i in station_list:
            self.station_data[i] = "None"

        try:
            self.status_msg.update('1', {"data": 'Initializing...', "data": [], "label": "Client Connectivity Time"})
        except:
            pass
        self.reports_path = webconsole_dir+"/reports/" + self.test_name + "_" + self.session_id + '/'


        if not os.path.exists(self.reports_path):
            os.makedirs(self.reports_path)
        self.station_list = LFUtils.portNameSeries(prefix_=self.sta_prefix, start_id_=self.sta_start_id,
                                                   end_id_=self.num_sta - 1, padding_number_=10000, radio=self.radio)
        try:
            self.status_msg.update('2', {"data": 'Initialized...', "data": [], "label": "Client Connectivity Time"})
        except:
            pass

    def precleanup(self):
        sta_list = []
        for i in self.local_realm.station_list():
            if (list(i.keys())[0] == '1.1.wlan0'):
                pass
            elif (list(i.keys())[0] == '1.1.wlan1'):
                pass
            else:
                sta_list.append(list(i.keys())[0])
        for sta in sta_list:
            self.local_realm.rm_port(sta, check_exists=True)
            time.sleep(1)

        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=sta_list,
                                           debug=self.debug)
        try:
            self.status_msg.update('3', {"data": 'Building...', "data": [], "label": "Client Connectivity Time"})
        except:
            pass

    def build(self):

        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template("00")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio, sta_names_=self.station_list, debug=self.debug)
        self.local_realm.wait_until_ports_appear(sta_list=self.station_list)
        self.update(status="build complete")
        try:
            self.status_msg.update('4', {"data": 'Starting...', "data": [], "label": "Client Connectivity Time"})
        except:
            pass

    def update(self, status="None"):
        for i in self.station_list:
            self.station_data[i.split(".")[2]] = \
            self.json_get("port/1/1/" + i.split(".")[2] + "/?fields=ip,ap,down,phantom&cx%20time%20(us)")['interface']
        try:
            self.status_msg.update('5', {"data": 'None', "data": [], "label": "Client Connectivity Time"})
        except:
            pass

    def start(self):
        self.station_profile.admin_up()
        associated_map = {}
        self.ip_map = {}
        cx_time = {}
        self.timeout = 60
        for sec in range(self.timeout):
            for sta_name in self.station_profile.station_names:
                sta_status = self.json_get("port/1/1/" + str(sta_name).split(".")[2] + "?fields=port,alias,ip,ap",
                                           debug_=self.debug)

                if (sta_status is None or sta_status['interface'] is None) or (sta_status['interface']['ap'] is None):
                    continue
                if (len(sta_status['interface']['ap']) == 17) and (sta_status['interface']['ap'][-3] == ':'):
                    associated_map[sta_name] = 1
                if (sta_status['interface']['ip'] != '0.0.0.0'):
                    self.ip_map[sta_name] = 1
            if (len(self.station_profile.station_names) == len(self.ip_map)) and (
                    len(self.station_profile.station_names) == len(associated_map)):
                break
            else:
                time.sleep(1)


        if (len(self.station_profile.station_names) == len(self.ip_map)) and (
                len(self.station_profile.station_names) == len(associated_map)):

            #("Test Passed")
            for sta_name in self.station_profile.station_names:
                sta_status = self.json_get("port/1/1/" + str(sta_name).split(".")[2] + "?fields=cx%20time%20(us)",
                                           debug_=self.debug)
                #(sta_status)
                while sta_status['interface']['cx time (us)'] == 0:
                    sta_status = self.json_get("port/1/1/" + str(sta_name).split(".")[2] + "?fields=cx%20time%20(us)",
                                               debug_=self.debug)
                    # #(sta_status)
                    continue
                cx_time[sta_name] = sta_status['interface']['cx time (us)']
        else:
            for sta_name in self.ip_map.keys():
                sta_status = self.json_get("port/1/1/" + str(sta_name).split(".")[2] + "?fields=cx%20time%20(us)",
                                           debug_=self.debug)
                while sta_status['interface']['cx time (us)'] == 0:
                    sta_status = self.json_get("port/1/1/" + str(sta_name).split(".")[2] + "?fields=cx%20time%20(us)",
                                               debug_=self.debug)
                    # #(sta_status)
                    continue
                cx_time[sta_name] = sta_status['interface']['cx time (us)']
        self.test_result_data = []
        self.keys = ["Client Name", "BSSID", "Channel", "Connection Time (ms)", "DHCP (ms)", "IPv4 Address", "MAC Address", "Mode", "Result"]
        for sta_name in self.station_profile.station_names:
            sta_status = self.json_get(
                "port/1/1/" + str(sta_name).split(".")[2] + "?fields=alias,ap,channel,cx%20time%20(us),ip,mac,mode,dhcp%20(ms)",
                debug_=self.debug)
            self.test_result_data.append(sta_status['interface'])

        offset = 0
        self.chart_data = {}
        for data in self.test_result_data:
            if (int(data["cx time (us)"])/1000 <= self.pass_criteria) and (int(data["cx time (us)"])/1000 > 0):
                self.chart_data[data['alias']] = float(data["cx time (us)"])/1000
                data['Result'] = "PASS"
            else:
                self.chart_data[data['alias']] = float(data["cx time (us)"]) / 1000
                offset +=1
                data['Result'] = "FAIL"
            data["cx time (us)"] = str(float(data["cx time (us)"])/1000)+" / "+str(self.pass_criteria)+"ms"

        objective = 'The Client Connectivity Test is designed to test the Performance of the Access Point. It will tell the Average Connection time that station takes to connect to Wifi Access Point. It will tell you Pass/Fail Criteria and detailed Report for Client Connection'

        if offset == 0:
            summary_result = 'PASS ' + str(len(self.ip_map)) + "/" + str(self.num_sta) + ' Clients are Connected in less than ' + str(self.pass_criteria) + " ms"
            self.pass_fail = "FAIL"
        else:
            summary_result = 'FAIL ' + str(len(self.ip_map)) + "/" + str(self.num_sta) + ' Clients are Connected, and/or Some might got connected in more than ' + str(self.pass_criteria) + " ms"
            self.pass_fail = "FAIL"


        self.html = open(self.reports_path + self.test_name + "_" + self.session_id + ".html", 'w')
        self.html_data = CreateHTML(path=self.reports_path, test_name=self.test_name, time_snap=str(datetime.datetime.now()), dut_ssid=self.ssid, test_conf_data={"Number of Clients":str(self.num_sta)},
                                   objective=objective, test_results={"summary": summary_result, "detail": {"keys": self.keys, "data": self.test_result_data}}, chart_data=self.chart_data,
                                   chart_params={"chart_head": "Client Connection Time", "xlabel": "Clients", "ylabel": "Connection Time"})
        self.html.write(self.html_data.report)
        self.html.close()
        options = {
            "enable-local-file-access": None
        }
        pdfkit.from_file(self.reports_path + self.test_name + "_" + self.session_id + ".html",
                         self.reports_path + self.test_name + "_" + self.session_id + '_report.pdf', options=options)

        try:
            self.status_msg.update('6', {"data": 'None', "data": [], "label": "Client Connectivity Time"})
        except:
            pass

    def stop(self):
        self.station_profile.admin_down()
        LFUtils.wait_until_ports_admin_down(port_list=self.station_profile.station_names)
        try:
            self.status_msg.update('7', {"data": 'None', "data": [], "label": "Client Connectivity Time"})
        except:
            pass
    def postcleanup(self):
        self.station_profile.cleanup(delay=1)
        try:
            self.status_msg.update('8', {"data": 'None', "data": [], "label": "Client Connectivity Time"})
        except:
            pass

def main():
    parser = LFCliBase.create_bare_argparse(prog="connection_test.py", formatter_class=argparse.RawTextHelpFormatter,
                                            epilog="About This Script")

    # Adding More Arguments for custom use
    parser.add_argument('--ssid', help='--ssid of DUT', default="lexusdut")
    parser.add_argument('--passwd', help='--passwd of dut', default="[BLANK]")
    parser.add_argument('--radio', help='--radio to use on LANforge', default="wiphy1")
    parser.add_argument('--security', help='--security of dut', default="open")
    parser.add_argument('--session_id', help='--session_id is for websocket', default=getSessionID())
    parser.add_argument('--test_name', help='--test_name is for webconsole reports', default="Client Connectivity Test")
    parser.add_argument('--num_clients', type=int, help='--num_sta is number of stations you want to create', default=2)
    parser.add_argument('--pass_criteria', type=int, help='--pass_criteria is pass criteria for connection Time', default=300)
    args = parser.parse_args()

    # Start Test
    obj = ConnectionTest(lfclient_host=args.mgr, lfclient_port=args.mgr_port,
                         session_id=args.session_id, test_name=args.test_name,
                         dut_ssid=args.ssid, dut_passwd=args.passwd, dut_security=args.security,
                     num_sta=args.num_clients, radio=args.radio, pass_criteria=args.pass_criteria)
    obj.precleanup()
    obj.build()
    obj.start()
    obj.stop()
    obj.postcleanup()

    # #(obj.chart_data)
    try:
        obj.status_msg.update('10', {"data": 'done...', "data": [], "label": "Client Connectivity Time"})
    except:
        pass
    for i in obj.status_msg.read()['messages']:
        print(i)
def getSessionID():
    x = datetime.datetime.now()
    id = x.strftime("%x").replace("/","_")+"_"+x.strftime("%x") + "_" + x.strftime("%X").split(":")[0] + "_" + x.strftime("%X").split(":")[1] + "_" + x.strftime("%X").split(":")[2]+str(x).split(".")[1]
    id = str(id).replace("/", "_").split("P")[0].replace(" ","")
    return id


if __name__ == '__main__':
    main()
