#!/usr/bin/env python3

"""
NAME: lf_we_can_scan.py


PURPOSE:
    This program is used for scanning the ssid using real client.
    The program will generate an output directory based on date and time in the /home/lanforge/html-reports/  .


EXAMPLE: ./python we_can_scan.py  --mgr 192.168.200.220 --mgr_port 8080 --ssid wecan --security wpa2 --radio wiphy0

Note: To Run this script
    WE-CAN app should be installed on the phone and should be Connected to lanforge server.

LICENSE:
    Free to distribute and modify. LANforge systems must be licensed.
    Copyright 2021 Candela Technologies Inc
"""
import datetime
import sys
import os
import importlib
import pandas as pd

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

import argparse
import time
from lf_report import lf_report

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")

# lf_report = importlib.import_module("py-scripts.lf_report")


class WeCanStaScan(Realm):
    def __init__(self,
                 ssid=None,
                 security=None,
                 password=None,
                 sta_list=None,
                 upstream=None,
                 radio=None,
                 host="localhost",
                 port=8080,
                 resource=1,
                 use_ht160=False,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        if sta_list is None:
            sta_list = []
        super().__init__(lfclient_host=host,
                         lfclient_port=port),
        self.upstream = upstream
        self.host = host
        self.port = port
        self.ssid = ssid
        self.sta_list = sta_list
        self.security = security
        self.password = password
        self.radio = radio
        self.debug = _debug_on
        self.station_profile = self.new_station_profile()
        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password
        self.station_profile.security = self.security
        self.station_profile.debug = self.debug
        self.station_profile.use_ht160 = use_ht160

    def start(self):
        stations = ['wlan0']
        scan_list = {}
        pass_fail = []
        signal_str = []
        full_scan_data = []
        resource_id, phone_name, mac_address, user_name, phone_radio = self.get_resource_data()
        print("Phone Name: ", phone_name)
        print("Resource Id ",resource_id)
        for id in resource_id:
            for port in stations:
                port = LFUtils.name_to_eid(port)
                data = {
                    "shelf": port[0],
                    "resource": id,
                    "port": port[2]
                }
                self.json_post("/cli-json/scan_wifi", data)
                time.sleep(3)
                scan_results = self.json_get(
                    "scanresults/%s/%s/%s" % (data['shelf'], str(data['resource']), data['port']))

                if (scan_results == None):
                    print(f"Unable to scan properly please check it manually (Either in Phontom Mode or Disconnected)")
                    pass_fail.append("Failed")
                    signal_str.append('NA')
                    full_scan_data.append(['Unable to scan properly please check it manually (Real Client is '
                                           'Either in Phantom Mode or Disconnected)'])
                    break
                tmp_ssid = []
                tmp_bss = []
                tmp_signal = []
                for result in scan_results['scan-results']:
                    for name, info in result.items():
                        if info['ssid'] != '':
                            tmp_ssid.append(info['ssid'])
                            tmp_bss.append(info['bss'])
                            tmp_signal.append(info['signal'])
                        if "\\x" not in info['ssid']:
                            scan_list[info['ssid']] = info['signal']
                table = pd.DataFrame({"SSID":tmp_ssid,
                                      "BSSI":tmp_bss,
                                      "Signal":tmp_signal,
                                      }).to_html(index=False)
                full_scan_data.append(table)

                if (self.ssid not in scan_list):
                    print("[FAILED] ssid not found in the scan \nResource id %s is unable to scan the ssid: \" %s \""
                          % (id, self.ssid))
                    pass_fail.append("Failed")
                    signal_str.append('NA')
                    # return None
                else:
                    pass_fail.append("Success")
                    signal_str.append(scan_list[self.ssid])
                    print("[PASSED] for Resouce id ", id)

        # print("All Phones are able scan the provided ssid: ", self.ssid)

        print("Generating Reports ")
        print("RESOURCE ID: ", resource_id, "\nPHONE NAME: ", phone_name, "\nMAC Address: ", mac_address,
              "\nPASS/FAIL: ", pass_fail, "\nSignal: ", signal_str, "\nUser Name: ", user_name,
              "\nPhone Radio: ", phone_radio)
        radio = ["2G/5G" for i in range(len(pass_fail))]

        data = pd.DataFrame({
            'Phone Name': phone_name,
            'User Name': user_name,
            'MAC Address': mac_address,
            'Resource ID': resource_id,
            'Signal Strength': signal_str,
            'Phone Radio': phone_radio,
            'Passed/Failed': pass_fail,
        })
        self.generate_report(data, full_scan_data, phone_name, pass_fail)

    def build(self):
        self._pass("PASS: Station build finished")

    def get_resource_data(self):
        resource_id_list = []
        phone_name_list = []
        mac_address = []
        user_name = []
        phone_radio = []
        eid_data = self.json_get("ports?fields=alias,mac,mode,Parent Dev")
        for alias in eid_data["interfaces"]:
            for i in alias:
                if (int(i.split(".")[1]) > 1 and alias[i]["alias"] == 'wlan0'):
                    resource_id_list.append(i.split(".")[1])
                    resource_hw_data = self.json_get("/resource/" + i.split(".")[0] + "/" + i.split(".")[1])
                    # Getting MAC address
                    mac = alias[i]["mac"]
                    # Getting user name
                    user = resource_hw_data['resource']['user']
                    user_name.append(user)
                    # Getting user Hardware details/Name
                    hw_name = resource_hw_data['resource']['hw version'].split(" ")
                    name = " ".join(hw_name[0:2])
                    phone_name_list.append(name)
                    mac_address.append(mac)
                if int(i.split(".")[1]) > 1 and alias[i]["alias"] == 'wlan0' and alias[i]["parent dev"] == 'wiphy0':
                    phone_radio.append(alias[i]['mode'])
                    # Mapping Radio Name in human readable format
                    # if 'a' in alias[i]['mode']:
                    #     phone_radio.append('2G/5G')
                    # elif 'AUTO' in alias[i]['mode']:
                    #     phone_radio.append("AUTO")
                    # else:
                    #     phone_radio.append('2G')
        return resource_id_list, phone_name_list, mac_address, user_name, phone_radio

    def generate_report(self, dataset, full_scan_data_list, phone_name, pass_fail):
        input_table = pd.DataFrame({
            "Server IP": [self.host],
            "Target SSID": [self.ssid],
            "Security": [self.security],
            "radio": [self.radio],
        })
        save_to_csv = pd.DataFrame(
            {"Phone Name": phone_name,
             "Full Scan List": full_scan_data_list,
             "Pass/Fail": pass_fail, }
        )
        pass_fail_count = []
        pass_count = 0
        fail_count = 0
        for i in pass_fail:
            if i == "Success":
                pass_count += 1
            else:
                fail_count += 1
        pass_fail_count.append(int(pass_count))
        pass_fail_count.append(int(fail_count))

        pie_chart = pd.DataFrame({'Pass/Fail': pass_fail_count}, index=['Success', 'Failed'])

        report = lf_report(_output_html="we-can-scan.html", _output_pdf="we-can-scan.pdf",
                           _results_dir_name="we-can scan result")

        report_path = report.get_path()
        report_path_date_time = report.get_path_date_time()

        print("path: {}".format(report_path))
        print("path_date_time: {}".format(report_path_date_time))

        report.set_title("WE-CAN Real Client Scan ")
        report.build_banner()

        report.start_content_div()
        report.set_text("<h3>Objective:" + "<h4>The scan test in the WE-CAN APP is designed to scan the SSID of the "
                                           "different Access Points in the particular network within its range so all "
                                           "the connected clients in the LANforge WE-CAN server should scan the given "
                                           "SSID within its range")
        report.build_date_time()
        report.build_text()

        report.save_pie_chart(pie_chart)

        report.start_content_div()
        report.set_table_title("<h3>Testing Data (User Input)")
        report.build_table_title()
        report.set_table_dataframe(input_table)
        report.build_table()
        # report.end_content_div()

        report.start_content_div()
        report.set_table_title("<h3>Phone Scan Table ")
        report.build_table_title()
        report.end_content_div()

        report.set_table_dataframe(dataset)
        report.pass_failed_build_table()

        report.start_content_div()
        report.build_chart_title("Pie Chart of Success and Failure")
        report.build_chart("pie-chart.png")

        if len(phone_name) == len(full_scan_data_list):
            for i in range(len(phone_name)):
                tmp_Phone_name = [phone_name[i]]
                tmp_scan_data = [''.join(full_scan_data_list[i])]
                tmp_dataset = pd.DataFrame({
                    'Phone Name': tmp_Phone_name,
                    'Scan List': tmp_scan_data,
                    'Pass/Fail': pass_fail[i],
                })
                report.start_content_div()
                report.set_table_title("<h3>Scan Result for %s" % phone_name[i])
                report.build_table_title()
                report.set_table_dataframe(tmp_dataset)
                report.pass_failed_build_table()
                report.end_content_div()

        # if (all(dataset['Passed/Failed'])):
        #     report.set_text("Description: All the phones are able to scan the given ssid  as we can see from the table")
        # else:
        #     report.set_text(
        #         "Description: Some of the phones are not able to scan the given ssid as we can see from the table")
        # report.start_content_div()
        # report.build_text()

        report.save_csv("we-can-scan.csv", save_to_csv)

        report.build_footer()
        html_file = report.write_html()
        print("returned file {}".format(html_file))
        print(html_file)

        report.write_pdf(_page_size='Legal', _orientation='Portrait')


def main():
    parser = Realm.create_basic_argparse(
        prog='we_can_scan.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        Used to verify if a ssid is available in a scan of a real client(Mobile Phones)
            ''',
        description='''\
        Verifies that wheather a station  is available in a scan of a phone with specified resource id, for each 
        resouce id it performs a scan and compares if given ssid is present in the scan.

        Example:
        ./we_can_scan.py --ssid ssid_for_test --security open --radio wiphy0
        ./we_can_scan.py  --mgr 192.168.200.218 --mgr_port 8080 --ssid Candela-Office --security wpa2 --radio 2G
        ''')

    # parser.add_argument('--mode', help='Used to force mode of stations')
    parser.add_argument('--sta_name',
                        help='Optional: User defined station names, can be a comma or space separated list', nargs='+',
                        default=["sta0000"])
    # parser.add_argument('--radio', help='Radio of real client', nargs='+',
    #                     default=1)

    args = parser.parse_args()

    station_list = args.sta_name
    sta_scan_test = WeCanStaScan(host=args.mgr,
                                 port=args.mgr_port,
                                 sta_list=station_list,
                                 upstream=args.upstream_port,
                                 ssid=args.ssid,
                                 password=args.passwd,
                                 radio=args.radio,
                                 security=args.security,
                                 use_ht160=False,
                                 _debug_on=args.debug)
    sta_scan_test.build()
    if not sta_scan_test.passes():
        print(sta_scan_test.get_fail_message())
        sta_scan_test.exit_fail()

    sta_scan_test.start()
    del sta_scan_test


if __name__ == "__main__":
    main()
