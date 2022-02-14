#!/usr/bin/env python3
"""
Candela Technologies Inc.

Info : Standard Script for Layer 4  Testing
Date :
Author : Shivam Thakur


"""

# script moved to sandbox 11/11/2021 needs work
import sys
import os
import importlib
import argparse
import datetime
import time
import json
import re

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
PortUtils = realm.PortUtils
test_utility = importlib.import_module("py-json.test_utility")
CreateHTML = test_utility.CreateHTML
RuntimeUpdates = test_utility.RuntimeUpdates

webconsole_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))
print(webconsole_dir)


class HTTPTest(LFCliBase):

    def __init__(self, lfclient_host="localhost", lfclient_port=8080, radio="wiphy1", sta_prefix="sta", start_id=0, num_sta=2,
                 dut_ssid="lexusdut", dut_security="open", dut_passwd="[BLANK]", upstream="eth1", name_prefix="L3Test", _test_update="",
                 url="", url_ps=600, session_id="Layer3Test", duration="1m",_debug_on=False, _exit_on_error=False,  _exit_on_fail=False):
        super().__init__(lfclient_host, lfclient_port, _debug=_debug_on, _exit_on_fail=_exit_on_fail)
        print("Test is about to start")
        self.host = lfclient_host
        self.port = lfclient_port
        self.radio = radio
        self.upstream = upstream
        self.monitor_interval = 1
        self.sta_prefix = sta_prefix
        self.sta_start_id = start_id

        self.num_sta = num_sta
        self.name_prefix = name_prefix
        self.ssid = dut_ssid
        self.security = dut_security
        self.password = dut_passwd
        self.session_id = session_id
        self.url = url
        self.urls_ps = url_ps
        self.test_update =_test_update
        self.test_update.send_update({"test_status": '1', "duration_left": "initializing...", "data": 'None'})
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.test_duration = self.local_realm.parse_time(duration)
        self.station_profile = self.local_realm.new_station_profile()
        self.port_util = PortUtils(self.local_realm)
        self.cx_profile = self.local_realm.new_http_profile()
        self.cx_profile.requests_per_ten = self.urls_ps
        self.cx_profile.url = self.url
        self.cx_profile.direction = "dl"
        self.cx_profile.dest = "/dev/null"
        print("Test Setup Initialized")
        self.test_update.send_update({"test_status": '2', "duration_left": "Initialized...", "data": 'None'})

    def precleanup(self):
        print("precleanup started")
        self.station_list = LFUtils.portNameSeries(prefix_=self.sta_prefix, start_id_=self.sta_start_id, end_id_=self.num_sta - 1, padding_number_=10000, radio=self.radio)
        self.cx_profile.cleanup()
        for sta in self.station_list:
            self.local_realm.rm_port(sta, check_exists=True)
        self.cx_profile.cleanup()

        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)
        self.test_update.send_update({"test_status": '3', "duration_left": "building test...", "data": 'None'})
        print("precleanup done")
        pass

    def build(self):
        print("Building Test Configuration")
        self.station_list = LFUtils.portNameSeries(prefix_=self.sta_prefix, start_id_=self.sta_start_id,
                                                   end_id_=self.num_sta - 1, padding_number_=10000, radio=self.radio)

        #self.port_util.set_http(port_name=name, resource=resource, on=True)
        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template("00")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio, sta_names_=self.station_list, debug=self.debug)
        self.local_realm.wait_until_ports_appear(sta_list=self.station_list)
        print("Test Build done")
        self.test_update.send_update({"test_status": '4', "duration_left": "starting test...", "data": 'None'})
        pass

    def start(self, print_pass=False, print_fail=False):
        print("Test is starting")
        self.station_profile.admin_up()
        temp_stas = self.station_profile.station_names.copy()
        if (self.local_realm.wait_for_ip(temp_stas)):
            self._pass("All stations got IPs", print_pass)
        else:
            self._fail("Stations failed to get IPs", print_fail)
            exit(1)
        self.cx_profile.create(ports=self.station_profile.station_names, sleep_time=.5, debug_=self.debug,
                               suppress_related_commands_=None, http=True)
        time.sleep(5)
        self.cx_profile.start_cx()
        try:
            for i in self.cx_profile.get_cx_names():
                while self.local_realm.json_get("/cx/" + i).get(i).get('state') != 'Run':
                    continue
        except Exception as e:
            pass
        print("Test Started")
        self.test_update.send_update({"test_status": '5', "duration_left": "Test started...", "data": 'None'})
        self.cur_time = datetime.datetime.now()
        self.end_time = self.test_duration + self.cur_time
        print(self.end_time-self.cur_time)
        self.start_monitor()
        pass

    def my_monitor(self):
        print("Monitoring Test")
        print(self.end_time - datetime.datetime.now())
        self.test_update.send_update({"test_status": '6', "duration_left": str(self.end_time - datetime.datetime.now()), "data": 'None'})
        if (datetime.datetime.now() > self.end_time):
            self.stop_monitor()
        return self.cx_profile.get_cx_report()

    def stop(self):
        print("Stopping Test")
        self.test_update.send_update({"test_status": '7', "duration_left": "stopping...", "data": "None"})
        self.cx_profile.stop_cx()
        for sta_name in self.station_list:
            data = LFUtils.port_down_request(1, self.local_realm.name_to_eid(sta_name)[2])
            url = "cli-json/set_port"
            self.json_post(url, data)


    def postcleanup(self):
        self.test_update.send_update({"test_status": '8', "duration_left": "finishing...", "data": "None"})
        self.cx_profile.cleanup()
        for sta in self.station_list:
            self.local_realm.rm_port(sta, check_exists=True)
            time.sleep(1)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_list,
                                           debug=self.debug)
        print("Test Completed")

        pass


def main():
    # This has --mgr, --mgr_port and --debug
    parser = LFCliBase.create_basic_argparse(prog="layer4_test.py", formatter_class=argparse.RawTextHelpFormatter, epilog="About This Script")

    # Adding More Arguments for custom use
    #parser.add_argument('--ssid', help='--ssid of DUT', default="WebAP")
    #parser.add_argument('--passwd', help='--passwd of dut', default="[BLANK]")
    #parser.add_argument('--radio', help='--radio to use on LANforge', default="wiphy1")
    #parser.add_argument('--security', help='--security of dut', default="open")
    parser.add_argument('--test_duration', help='--test_duration sets the duration of the test', default="1m")
    parser.add_argument('--session_id', help='--session_id is for websocket', default="local")
    parser.add_argument('--num_client', type=int, help='--num_sta is number of stations you want to create', default=2)
    parser.add_argument('--url_ps', help='--speed you want to monitor traffic with (max is 10G)', default=600)
    parser.add_argument('--url', help='--url on which you want to test HTTP', default="www.google.com")
    parser.add_argument('--test_name', help='--test_name is for webconsole reports', default="HTTP Traffic Test")
    args = parser.parse_args()
    # print(args)
    update = RuntimeUpdates(args.session_id, {"test_status": '0', "data": 'None'})
    # # Start Test
    http_obj = HTTPTest(lfclient_host="192.168.200.12", lfclient_port=args.mgr_port,
                     duration=args.test_duration, session_id=args.session_id,
                     dut_ssid=args.ssid, dut_passwd=args.passwd, dut_security=args.security, num_sta=args.num_client, url_ps=args.url_ps, radio=args.radio, _test_update=update)
    http_obj.precleanup()
    http_obj.build()
    http_obj.start()
    http_obj.monitor()
    http_obj.stop()
    http_obj.postcleanup()
    http_obj.test_update.send_update({"test_status": '8', "duration_left": "generating report...", "data": "None"})
    result_file = open("../py-run/"+args.session_id + ".txt", "r")
    result_data = result_file.readlines()
    final_data = result_data[len(result_data)-1]
    test_detail_data = []
    client_names = []
    timesnap=[]
    obj = re.sub('[\']', '"', final_data)
    data = json.loads(obj)
    for i in data:
        for j in data[i]['endpoint']:
            for k in j:
                client_names.append(k)

    summary_data = dict.fromkeys(client_names)
    count = 0

    for i in summary_data:
        summary_data[i] = 0

    for i in result_data:
        obj = re.sub('[\']', '"', i)
        data = json.loads(obj)
        for j in data:
            timesnap.append(j)
            for k in range(0, len(client_names)):
                if (data[j]['endpoint'][k][client_names[k]]['uc-avg'] == 0):
                    count += 1
                else:
                    summary_data[client_names[k]] = summary_data[client_names[k]] + \
                                                    data[j]['endpoint'][k][client_names[k]]['uc-avg']
    count = len(result_data) - count / len(client_names)
    # print(summary_data)

    for i in summary_data:
        summary_data[i] = summary_data[i]/count
    print("iron ee")
    print(summary_data)

    # Detailed Table Data
    obj = re.sub('[\']', '"', final_data)
    data = json.loads(obj)
    for i in data:
        for j in data[i]['endpoint']:
            for k in j:
                client_names.append(k)
                if (summary_data[k] != 0) and (summary_data[k] < 3000):
                    temp = {"Client Name": k, "Avg. Response Time": str(int(summary_data[k]))+ " ms",
                            "RX Rate": str(int(j[k]['rx rate']) / 8000) + " kbps",
                            "Total URL's": j[k]['total-urls'], "Total Timeouts": j[k]['timeout'],
                            "Total Errors": j[k]['total-err'], "HTTP Range Error": j[k]['http-r'],
                            "HTTP Port Error": j[k]['http-p'], "result": "PASS"}
                else:
                    temp = {"Client Name": k, "Avg. Response Time": str(int(summary_data[k])) + " ms",
                            "RX Rate": str(int(j[k]['rx rate']) / 8000) + " kbps",
                            "Total URL's": j[k]['total-urls'], "Total Timeouts": j[k]['timeout'],
                            "Total Errors": j[k]['total-err'], "HTTP Range Error": j[k]['http-r'],
                            "HTTP Port Error": j[k]['http-p'], "result": "FAIL"}
                test_detail_data.append(temp)

    reports_path = webconsole_dir + "/reports/" + args.test_name + "_" + args.session_id + '/'

    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    html = open(reports_path + args.test_name + "_" + args.session_id + ".html", 'w')

    objective = "The HTTP Traffic Test is designed to test the HTTP Performance of the Access Point. In this Test, Stations are sending HTTP Requests and it is monitoring the response time as a metric"

    count =0
    for i in summary_data:
        if (summary_data[i] < 3000) and (summary_data[i] !=0):
            pass
        else:
            count+=1
    if (count == 0):
        pass_fail = "PASS"
        summary_result = "PASS, All clients are succesfully connected and Passed HTTP Test"
    else:
        pass_fail = "FAIL"
        summary_result = "FAIL, Not All clients are succesfully connected and Passed HTTP Test"

    html_data = CreateHTML(path=reports_path, test_name=args.test_name,
                                time_snap=str(datetime.datetime.now()), dut_ssid=args.ssid,
                                test_conf_data={"Number of Clients": str(args.num_client), "URL": args.url},
                                objective=objective, test_results={"summary": summary_result,
                                                                   "detail": {"keys": ["Client Name",  "Average Response Time", "RX Rate", "Total URL's", "Total Timeouts", "Total Errors", "HTTP Range Error", "HTTP Port Error","Result"],
                                                                              "data": test_detail_data}},
                                chart_data=summary_data,
                                chart_params={"chart_head": "HTTP Response Time", "xlabel": "Time",
                                              "ylabel": "Average Response Time"})
    html.write(html_data.report)
    html.close()



    http_obj.test_update.send_update({"test_status": '10', "duration_left": "done", "data": "None", "result": pass_fail})


if __name__ == '__main__':
    main()
