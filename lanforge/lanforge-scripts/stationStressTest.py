#!/usr/bin/env python3
import os
import sys
import time

sys.path.append('py-json')
import datetime
from LANforge import LFRequest
from LANforge import LFUtils
import argparse
import re
import emailHelper
from LANforge.lfcli_base import LFCliBase


class StressTester(LFCliBase):
    def __init__(self, lfhost, lfport, _sender="lanforge@candelatech.com", _debug_on=True):
        self.sender = _sender
        super().__init__(lfhost, lfport, False)

    def name_to_eid(self, eid):
        info = []
        if eid is None or eid == "":
            raise ValueError("name_to_eid wants eid like 1.1.sta0 but given[%s]" % eid)
        else:
            if '.' in eid:
                info = eid.split('.')
        return info

    def cleanup(self):
        try:
            sta_json = super().json_get("port/1/1/list?field=alias")['interfaces']
        except TypeError:
            sta_json = None
        cx_json = super().json_get("cx")
        endp_json = super().json_get("endp")

        # get and remove current stations
        if sta_json is not None:
            print("Removing old stations")
            for name in list(sta_json):
                for alias in list(name):
                    if 'sta' in alias:
                        #print(alias)
                        info = self.name_to_eid(alias)
                        req_url = "cli-json/rm_vlan"
                        data = {
                            "shelf": info[0],
                            "resource": info[1],
                            "port": info[2]
                        }
                        #print(data)
                        super().json_post(req_url, data)
                        time.sleep(.5)
        else:
            print("No stations found to cleanup")

        # get and remove current cxs
        if cx_json is not None:
            print("Removing old cross connects")
            for name in list(cx_json):
                if name != 'handler' and name != 'uri':
                    #print(name)
                    req_url = "cli-json/rm_cx"
                    data = {
                        "test_mgr": "default_tm",
                        "cx_name": name
                    }
                    super().json_post(req_url, data)
                    time.sleep(.5)
        else:
            print("No cross connects found to cleanup")

        # get and remove current endps
        if endp_json is not None:
            print("Removing old endpoints")
            for name in list(endp_json['endpoint']):
                #print(list(name)[0])
                req_url = "cli-json/rm_endp"
                data = {
                    "endp_name": list(name)[0]
                }
                #print(data)
                super().json_post(req_url, data)
                time.sleep(.5)
        else:
            print("No endpoints found to cleanup")

    def run(self):
        parser = argparse.ArgumentParser(description="Create max stations for each radio")
        parser.add_argument("--test_duration", type=str,
                            help="Full duration for the test to run. Should be specified by a number followed by a "
                                 "character. d for days, h for hours, m for minutes, s for seconds")
        parser.add_argument("--test_end_time", type=str,
                            help="Specify a time and date to end the test. Should be formatted as "
                                 "year-month-date_hour:minute. Date should be specified in numbers and time "
                                 "should be 24 "
                                 "hour format. Ex: 2020-5-14_14:30")
        parser.add_argument("--report_interval", type=str,
                            help="How often a report is made. Should be specified by a "
                                 "number followed by a character. d for days, h for hours, "
                                 "m for minutes, s for seconds")
        parser.add_argument("--output_dir", type=str, help="Directory to output to")
        parser.add_argument("--output_prefix", type=str,
                            help="Name of the file. Timestamp and .html will be appended to the end")
        parser.add_argument("--email", type=str, help="Email address of recipient")

        args = None
        try:
            args = parser.parse_args()
            if args.test_duration is not None:
                pattern = re.compile("^(\d+)([dhms]$)")
                td = pattern.match(args.test_duration)
                if td is not None:
                    dur_time = int(td.group(1))
                    dur_measure = str(td.group(2))
                    now = datetime.datetime.now()
                    if dur_measure == "d":
                        duration_time = datetime.timedelta(days=dur_time)
                    elif dur_measure == "h":
                        duration_time = datetime.timedelta(hours=dur_time)
                    elif dur_measure == "m":
                        duration_time = datetime.timedelta(minutes=dur_time)
                    else:
                        duration_time = datetime.timedelta(seconds=dur_time)
                else:
                    parser.print_help()
                    parser.exit()

            elif args.test_end_time is not None:
                now = datetime.datetime.now()
                try:
                    end_time = datetime.datetime.strptime(args.test_end_time, "%Y-%m-%d_%H:%M")
                    if end_time < now:
                        parser.print_help()
                        raise ValueError
                    else:
                        cur_time = datetime.datetime.now()
                        duration_time = end_time - cur_time

                except ValueError as exception:
                    print(exception)
                    parser.print_help()
                    parser.exit()

            else:
                parser.print_help()
                parser.exit()

            if args.report_interval is not None:
                pattern = re.compile("^(\d+)([dhms])$")
                ri = pattern.match(args.report_interval)
                if ri is not None:
                    int_time = int(ri.group(1))
                    int_measure = str(ri.group(2))

                    if int_measure == "d":
                        interval_time = datetime.timedelta(days=int_time)
                    elif int_measure == "h":
                        interval_time = datetime.timedelta(hours=int_time)
                    elif int_measure == "m":
                        interval_time = datetime.timedelta(minutes=int_time)
                    else:
                        interval_time = datetime.timedelta(seconds=int_time)
                else:
                    parser.print_help()
                    parser.exit()
            else:
                parser.print_help()
                parser.exit()

            if args.output_dir is not None:
                if not args.output_dir.endswith('/'):
                    output_dir = args.output_dir + '/'
                else:
                    output_dir = args.output_dir
            else:
                parser.print_help()
                parser.exit()

            if args.output_prefix is not None:
                output_prefix = args.output_prefix
            else:
                parser.print_help()
                parser.exit()
            if args.email is not None:
                recipient = args.email
            else:
                parser.print_help()
                parser.exit()

        except Exception as e:
            parser.print_help()
            exit(2)

        super().check_connect()

        stations = []
        radios = {"wiphy0": 200,  # max 200
                  "wiphy1": 200,  # max 200
                  "wiphy2": 64,  # max 64
                  "wiphy3": 200}  # max 200
        # radioName:numStations
        radio_ssid_map = {"wiphy0": "jedway-wpa2-x2048-4-1",
                          "wiphy1": "jedway-wpa2-x2048-5-3",
                          "wiphy2": "jedway-wpa2-x2048-5-1",
                          "wiphy3": "jedway-wpa2-x2048-4-4"}

        ssid_passphrase_map = {"jedway-wpa2-x2048-4-1": "jedway-wpa2-x2048-4-1",
                               "jedway-wpa2-x2048-5-3": "jedway-wpa2-x2048-5-3",
                               "jedway-wpa2-x2048-5-1": "jedway-wpa2-x2048-5-1",
                               "jedway-wpa2-x2048-4-4": "jedway-wpa2-x2048-4-4"}

        padding_num = 1000  # uses all but the first number to create names for stations

        # clean up old stations
        self.cleanup()

        # create new stations
        print("Creating Stations")

        req_url = "cli-json/add_sta"
        for radio, numStations in radios.items():
            for i in range(0, numStations):
                sta_name = "sta" + radio[-1:] + str(padding_num + i)[1:]
                stations.append(sta_name)
                data = {
                    "shelf": 1,
                    "resource": 1,
                    "radio": radio,
                    "sta_name": sta_name,
                    "ssid": radio_ssid_map[radio],
                    "key": ssid_passphrase_map[radio_ssid_map[radio]],
                    "mode": 1,
                    "mac": "xx:xx:xx:xx:*:xx",
                    "flags": 0x400
                }
                # print("Creating station {}".format(sta_name))
                super().json_post(req_url, data)

                time.sleep(0.5)

        # LFUtils.portDhcpUpRequest(1, sta_name)

        time.sleep(10)

        # check eth1 for ip
        eth1_ip = super().json_get("port/1/1/eth1")
        if eth1_ip['interface']['ip'] == "0.0.0.0":
            print("Switching eth1 to dhcp")
            LFUtils.portDownRequest(1, "eth1")
            time.sleep(1)
            req_url = "cli-json/set_port"
            data = {
                "shelf": 1,
                "resource": 1,
                "port": "eth1",
                "current_flags": 0x80000000,
                "interest": 0x4002
            }

            super().json_post(req_url, data)
            # LFUtils.portDhcpUpRequest(1,"eth1")
            time.sleep(5)
            LFUtils.portUpRequest(1, "eth1")

        time.sleep(10)

        # create cross connects
        print("Creating cross connects")
        for sta_name in stations:
            cmd = (
                    "./lf_firemod.pl --action create_cx --cx_name " + sta_name + " --use_ports eth1," + sta_name + " --use_speeds  2600,2600 --endp_type udp > sst.log")
            LFUtils.execWrap(cmd)

        # set stations to dchp up
        print("Turning on DHCP for stations")
        for sta_name in stations:
            # print("Setting {} flags".format(sta_name))
            req_url = "cli-json/set_port"
            data = {
                "shelf": 1,
                "resource": 1,
                "port": sta_name,
                "current_flags": 0x80000000,
                "interest": 0x4002
            }

            super().json_post(req_url, data)
        # LFUtils.portDhcpUpRequest(1,sta_name)

        time.sleep(15)

        # start traffic through cxs
        print("Starting CX Traffic")
        for name in stations:
            cmd = (
                    "./lf_firemod.pl --mgr localhost --quiet 0 --action do_cmd --cmd \"set_cx_state default_tm " + name + " RUNNING\" >> sst.log")
            LFUtils.execWrap(cmd)

        # create weblog for monitoring stations
        cur_time = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        web_log = output_dir + output_prefix + "{}.html".format(cur_time)

        try:
            web_log_file = open(web_log, "w")

        except IOError as err:
            print(err)
            print("Please ensure correct permissions have been assigned in target directory")
            sys.exit()

        top = """<html>
        <head>
        <title>Test report</title>
        <style>
        body, td, p, div, span { font-size: 8pt; }
        h1, h2, h3 { text-align: center; font-family: "Century Gothic",Arial,Helvetica,sans;}
        </style>
        </head>
        <body>
        <h1>Long test on %s</h1>
        <p2>Key</p2>
        <p1 style="background-color:rgb(0,255,0);">All stations associated and with ip</p1>
        <p1 style="background-color:rgb(255,200,0);">All stations associated and at least one without ip</p1>
        <p1 style="background-color:rgb(255,150,150);">No stations associated and without ip</p1>
        <table>
        """ % datetime.date.today()

        web_log_file.write(top)
        web_log_file.close()

        web_log_file = open(web_log, "a")
        web_log_file.write("<tr>\n")

        for name in radios:
            web_log_file.write("<th>{}</th>\n".format(name))

        web_log_file.write("</tr>\n")

        cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        subject = "Station Test Begin Report Notification"
        body = "Report begun at {}\n See {}".format(cur_time, web_log)
        email = emailHelper.writeEmail(body)
        emailHelper.sendEmail(email, self.sender, recipient, subject)

        print("Logging Info to {}".format(web_log))

        cur_time = datetime.datetime.now()
        end_time = cur_time + duration_time

        while cur_time <= end_time:
            web_log_file.write("<tr>\n")
            for radio, numStations in radios.items():
                without_ip = 0
                dissociated = 0
                good = 0

                for i in range(0, numStations):
                    sta_name = "sta" + radio[-1:] + str(padding_num + i)[1:]
                    sta_status = super().json_get("port/1/1/" + sta_name)
                    # print(sta_name)
                    if sta_status['interface']['ip'] == "0.0.0.0":
                        without_ip += 1
                        if sta_status['interface']['ap'] is None:
                            dissociated += 1
                    else:
                        good += 1

                if without_ip and not dissociated:
                    web_log_file.write("<td style=\"background-color:rgb(255,200,0);\">{}/{}</td>\n".format(good,
                                                                                                            numStations))  # without IP assigned
                elif dissociated:
                    web_log_file.write("<td style=\"background-color:rgb(255,150,150);\">{}/{}</td>\n".format(good,
                                                                                                              numStations))  # dissociated from AP
                else:
                    web_log_file.write("<td style=\"background-color:rgb(0,255,0);\">{}/{}</td>\n".format(good,
                                                                                                          numStations))  # with IP and associated

            web_log_file.write("<td>{}</td>\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
            web_log_file.write("</tr>\n")

            cur_time = datetime.datetime.now()
            int_time = cur_time + interval_time
            while cur_time <= int_time:
                # print(cur_time, int_time)
                time.sleep(1)
                cur_time = datetime.datetime.now()
            # sleep(1)
            cur_time = datetime.datetime.now()

        web_log_file.write("</table></body></html>\n")
        web_log_file.close()

        cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        subject = "Station Test End Report Notification"
        body = "Report finished at {} see {}".format(cur_time, web_log)
        email = emailHelper.writeEmail(body)
        emailHelper.sendEmail(email, self.sender, recipient, subject)

        print("Stopping CX Traffic")
        for sta_name in stations:
            cmd = (
                    "./lf_firemod.pl --mgr localhost --quiet 0 --action do_cmd --cmd \"set_cx_state default_tm " + sta_name + " STOPPED\" >> sst.log")
            LFUtils.execWrap(cmd)

        time.sleep(10)

        # remove all created stations and cross connects

        print("Cleaning Up...")
        self.cleanup()

def main():
    lfjson_host = "localhost"
    lfjson_port = 8080
    test = StressTester(lfjson_host, lfjson_port)
    test.run()


if __name__ == "__main__":
    main()
