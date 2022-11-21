#!/usr/bin/python3

'''
NAME: lf_check.py 

PURPOSE: lf_check.py run tests based on test rig json input, test dut json input,  and test command line inputs 

EXAMPLE: 

./lf_check.py --json_rig <test rig json> --json_dut <dut_json> --json_test <tests json> --test_suite <suite_name> --path <path to results and db, db table>
./lf_check.py --json_rig <test rig json> --json_dut <dut_json> --json_test <tests json> --test_suite <suite_name> --path <path to results>  --production

./lf_check.py  --json_rig ct_us_001_rig.json --json_dut ct_001_AX88U_dut.json  --json_test ct_us_001_tests.json  --suite "suite_wc_dp"  --path '/home/lanforge/html-reports/ct-us-001'


rig is the LANforge
dut is the device under test
NOTE : if all json data (rig,dut,tests)  in same json file pass same json in for all 3 inputs

NOTES:
Create three json files: 1. discribes rig (lanforge), dut (device under test) and other for the description of the tests

Starting LANforge:
    On local or remote system: /home/lanforge/LANforgeGUI/lfclient.bash -cli-socket 3990 -s LF_MGR 
    On local system the -s LF_MGR will be local_host if not provided

### Below are development Notes ###


NOTES: getting radio information:
1. (Using Curl) curl -H 'Accept: application/json' http://localhost:8080/radiostatus/all | json_pp 
2.  , where --user "USERNAME:PASSWORD"
# https://itnext.io/curls-just-want-to-have-fun-9267432c4b55
3. (using Python) response = self.json_get("/radiostatus/all"), Currently lf_check.py is independent of py-json libraries

4. if the connection to 8080 is rejected check : pgrep -af java  , to see the number of GUI instances running

GENERIC NOTES: 
Starting LANforge:
    On local or remote system: /home/lanforge/LANforgeGUI/lfclient.bash -cli-socket 3990 -s LF_MGR 
    On local system the -s LF_MGR will be local_host if not provided
    Saving stdout and stderr to find LANforge issues
    ./lfclient.bash -cli-socket 3990 > >(tee -a stdout.log) 2> >(tee -a stderr.log >&2)


    On LANforge ~lanforge/.config/autostart/LANforge-auto.desktop is used to restart lanforge on boot.
        http://www.candelatech.com/cookbook.php?vol=misc&book=Automatically+starting+LANforge+GUI+on+login

1. add server (telnet localhost 4001) build info,  GUI build sha, and Kernel version to the output. 
    A. for build information on LANforgeGUI : /home/lanforge ./btserver --version
    B. for the kernel version uname -r (just verion ), uname -a build date
    C. for getting the radio firmware:  ethtool -i wlan0 

# may need to build in a testbed reboot at the beginning of a day's testing...
# seeing some dhcp exhaustion and high latency values for testbeds that have been running 
# for a while that appear to clear up once the entire testbed is power cycled

# Capture the LANforge client output sdtout and stdwrr
/home/lanforge/LANforgeGUI/lfclient.bash -cli-socket 3990 -s LF_MGR command > >(tee -a stdout.log) 2> >(tee -a stderr.log >&2)

# To get the --raw_line commands
# Build Chamber View Scenario in the GUI and then # copy/tweak what it shows in the 'Text Output' tab after saving and re-opening # the scenario

# issue a shutdown command on the lanforge(s)
#  ssh root@lanforge reboot (need to verify)  or do a shutdown 
# send curl command to remote power switch to reboot testbed
#   curl -s http://admin:lanforge@192.168.100.237/outlet?1=CCL -o /dev/null 2>&1
# 
 

'''
import datetime
import sys
import traceback

if sys.version_info[0] != 3:
    print("This script requires Python3")
    exit()

import os
import socket
import logging
import time
from time import sleep
import argparse
import json
import subprocess
import csv
import shlex
import paramiko
import pandas as pd
import requests

# lf_report is from the parent of the current file
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from lf_report import lf_report

sys.path.append('/')

# setup logging FORMAT
FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'


# lf_check class contains verificaiton configuration and ocastrates the testing.
class lf_check():
    def __init__(self,
                _json_rig,
                _json_dut,
                _json_test,
                _test_suite,
                _json_igg,
                _production,
                _csv_results,
                _outfile,
                _outfile_name,
                _report_path,
                _log_path):
        self.json_rig = _json_rig
        self.json_dut = _json_dut
        self.json_test = _json_test
        self.test_suite = _test_suite
        self.json_igg = _json_igg
        self.production_run = _production
        self.report_path = _report_path
        self.log_path = _log_path
        self.radio_dict = {}
        self.test_dict = {}
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        self.scripts_wd = os.getcwd()
        self.results = ""
        self.outfile = _outfile
        self.outfile_name = _outfile_name
        self.test_result = "Failure"
        self.results_col_titles = ["Test", "Command", "Result", "STDOUT", "STDERR"]
        self.html_results = ""
        self.background_green = "background-color:green"
        self.background_red = "background-color:red"
        self.background_purple = "background-color:purple"
        self.background_blue = "background-color:blue"

        # LANforge information
        self.lanforge_system_node_version = ""
        self.lanforge_kernel_version = ""
        self.lanforge_gui_version_full = ""
        self.lanforge_gui_version = ""

        # meta.txt
        self.meta_data_path = ""

        # lanforge configuration 
        self.lf_mgr_ip = "192.168.0.102"
        self.lf_mgr_port = "8080"
        self.lf_mgr_user = "lanforge"
        self.lf_mgr_pass = "lanforge"
        self.upstream_port = ""


        # results
        self.database_sqlite = ""
        self.test_start_time = ""
        self.test_end_time = ""
        self.duration = ""

        self.http_test_ip = ""
        self.ftp_test_ip = ""
        self.test_ip = ""

        # section DUT
        # dut selection 
        self.dut_set_name = 'DUT_NAME ASUSRT-AX88U'  # note the name will be set as --set DUT_NAME ASUSRT-AX88U, this is not dut_name (see above)

        # dut configuration 
        self.dut_name = "DUT_NAME_NA"  # "ASUSRT-AX88U" note this is not dut_set_name
        self.dut_hw = "DUT_HW_NA"
        self.dut_sw = "DUT_SW_NA"
        self.dut_model = "DUT_MODEL_NA"
        self.dut_serial = "DUT_SERIAL_NA"
        self.dut_bssid_2g = "BSSID_2G_NA"  # "3c:7c:3f:55:4d:64" - this is the mac for the 2.4G radio this may be seen with a scan
        self.dut_bssid_5g = "BSSID_5G_NA"  # "3c:7c:3f:55:4d:64" - this is the mac for the 5G radio this may be seen with a scan
        self.dut_bssid_6g = "BSSID_6G_NA"  # "3c:7c:3f:55:4d:64" - this is the mac for the 6G radio this may be seen with a scan

        self.ssid_2g = ""
        self.ssid_2g_pw = ""
        self.security_2g = ""

        self.ssid_5g = ""
        self.ssid_5g_pw = ""
        self.security_5g = ""

        self.ssid_6g = ""
        self.ssid_6g_pw = ""
        self.security_6g = ""

        self.csv_results = _csv_results
        self.csv_results_file = ""
        self.csv_results_writer = ""
        self.csv_results_column_headers = ""
        self.logger = logging.getLogger(__name__)
        self.test_timeout = 120
        self.test_timeout_default = 120
        self.test_iterations_default = 1
        self.use_blank_db = "FALSE"
        self.use_factory_default_db = "FALSE"
        self.use_custom_db = "FALSE"
        self.email_list_production = ""
        self.host_ip_production = None
        self.email_list_test = ""
        self.host_ip_test = None
        self.email_title_txt = ""
        self.email_txt = ""

        # NOTE:  My influx token is unlucky and starts with a '-', but using the syntax below # with '=' right after the argument keyword works as hoped.
        # --influx_token=

        # DUT , Test rig must match testbed
        self.test_rig = "CT-US-NA"
        self.test_rig_json = ""

        # QA report
        self.qa_report_html = "NA"
        self.database_qa = ""
        self.table_qa = ""

        # database configuration  # database
        self.influx_database_json = ""
        self.influx_database_config = "True"  # default to False once testing done
        self.influx_database_host = "192.168.100.201"  # "c7-grafana.candelatech.com" # influx and grafana have the same host "192.168.100.201"
        self.influx_database_port = "8086"
        self.influx_database_token = "-u_Wd-L8o992701QF0c5UmqEp7w7Z7YOMaWLxOMgmHfATJGnQbbmYyNxHBR9PgD6taM_tcxqJl6U8DjU1xINFQ=="
        self.influx_database_org = "Candela"
        self.influx_database_bucket = "lanforge_qa_testing"
        self.influx_database_tag = 'testbed CT-US-001'  # the test_rig needs to match

        # grafana configuration  #dashboard
        self.dashboard_json_grafana = ""
        self.dashboard_config_grafana = "True"  # default to False once testing done
        self.dashboard_host_grafana = "192.168.100.201"  # "c7-grafana.candelatech.com" # 192.168.100.201
        self.dashboard_port_grafana = "3000"
        self.dashboard_token_grafana = "eyJrIjoiS1NGRU8xcTVBQW9lUmlTM2dNRFpqNjFqV05MZkM0dzciLCJuIjoibWF0dGhldyIsImlkIjoxfQ=="

        # ghost configuration 
        self.blog_json_ghost = ""
        self.blog_config_ghost = False
        self.blog_host_ghost = "192.168.100.153"
        self.blog_port_ghost = "2368"
        self.blog_token_ghost = "60df4b0175953f400cd30650:d50e1fabf9a9b5d3d30fe97bc3bf04971d05496a89e92a169a0d72357c81f742"
        self.blog_authors_ghost = "Matthew"
        self.blog_customer_ghost = "candela"
        self.blog_user_push_ghost = "lanforge"
        self.blog_password_push_ghost = "lanforge"
        self.blog_flag = "--kpi_to_ghost"

        self.test_run = ""

    def get_test_rig(self):
        return self.test_rig

    def check_if_port_exists(self,json_igg):
        queries = dict()
        queries['LANforge Manager'] = 'http://%s:%s' % (self.lf_mgr_ip, self.lf_mgr_port)
        # Frame work not required to use specific databases or presentation
        if json_igg != "":
            queries['Blog Host'] = 'http://%s:%s' % (self.blog_host_ghost, self.blog_port_ghost)
            queries['Influx Host'] = 'http://%s:%s' % (self.influx_database_host, self.influx_database_port)
            queries['Grafana Host'] = 'http://%s:%s' % (self.dashboard_host_grafana, self.dashboard_port_grafana)
        results = dict()
        for key, value in queries.items():
            try:
                ping = requests.get(value).text
                results[key] = [str(ping), value]
            except:
                print('%s not found' % value)
                results[key] = [value, None]
        return results

    def get_scripts_git_sha(self):
        # get git sha
        process = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE)
        (commit_hash, err) = process.communicate()
        exit_code = process.wait()
        print("get_scripts_get_sha exit_code: {exit_code}".format(exit_code=exit_code))
        scripts_git_sha = commit_hash.decode('utf-8', 'ignore')
        return scripts_git_sha

    '''
    self.lf_mgr_ip = "192.168.0.102"
        self.lf_mgr_port = "8080"
        self.lf_mgr_user = "lanforge"
        self.lf_mgr_pass = "lanforge"
        '''
    def get_lanforge_radio_information(self):
        # https://docs.python-requests.org/en/latest/
        # https://stackoverflow.com/questions/26000336/execute-curl-command-within-a-python-script - use requests
        # curl --user "lanforge:lanforge" -H 'Accept: application/json' http://192.168.100.116:8080/radiostatus/all | json_pp  , where --user "USERNAME:PASSWORD"
        request_command = 'http://{lfmgr}:{port}/radiostatus/all'.format(lfmgr=self.lf_mgr_ip,port=self.lf_mgr_port)
        request = requests.get(request_command, auth=(self.lf_mgr_user,self.lf_mgr_pass))
        print("radio request command: {request_command}".format(request_command=request_command))
        print("radio request status_code {status}".format(status=request.status_code))
        lanforge_radio_json = request.json()
        print("radio request.json: {json}".format(json=lanforge_radio_json))
        lanforge_radio_text = request.text
        print("radio request.test: {text}".format(text=lanforge_radio_text))
        return lanforge_radio_json, lanforge_radio_text
        

    def get_lanforge_system_node_version(self):
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(hostname=self.lf_mgr_ip, port=22, username=self.lf_mgr_user, password=self.lf_mgr_pass,
                    allow_agent=False, look_for_keys=False, banner_timeout=600)
        stdin, stdout, stderr = ssh.exec_command('uname -n')
        self.lanforge_system_node_version = stdout.readlines()
        self.lanforge_system_node_version = [line.replace('\n', '') for line in self.lanforge_system_node_version]
        ssh.close()
        time.sleep(1)
        return self.lanforge_system_node_version

    def get_lanforge_kernel_version(self):
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(hostname=self.lf_mgr_ip, port=22, username=self.lf_mgr_user, password=self.lf_mgr_pass,
                    allow_agent=False, look_for_keys=False, banner_timeout=600)
        stdin, stdout, stderr = ssh.exec_command('uname -r')
        self.lanforge_kernel_version = stdout.readlines()
        self.lanforge_kernel_version = [line.replace('\n', '') for line in self.lanforge_kernel_version]
        ssh.close()
        time.sleep(1)
        return self.lanforge_kernel_version

    def get_lanforge_gui_version(self):
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(hostname=self.lf_mgr_ip, port=22, username=self.lf_mgr_user, password=self.lf_mgr_pass,
                    allow_agent=False, look_for_keys=False, banner_timeout=600)
        stdin, stdout, stderr = ssh.exec_command('./btserver --version | grep  Version')
        self.lanforge_gui_version_full = stdout.readlines()
        self.lanforge_gui_version_full = [line.replace('\n', '') for line in self.lanforge_gui_version_full]
        print("lanforge_gui_version_full: {lanforge_gui_version_full}".format(lanforge_gui_version_full=self.lanforge_gui_version_full))
        self.lanforge_gui_version = self.lanforge_gui_version_full[0].split('Version:',maxsplit=1)[-1].split(maxsplit=1)[0]
        self.lanforge_gui_version = self.lanforge_gui_version.strip()
        print("lanforge_gui_version: {lanforge_gui_version}".format(lanforge_gui_version=self.lanforge_gui_version))
        ssh.close()
        time.sleep(1)
        return self.lanforge_gui_version_full

    def get_radio_status(self):
        radio_status = self.json_get("/radiostatus/all")
        print("radio status {radio_status}".format(radio_status=radio_status))

    # NOT complete : will send the email results
    def send_results_email(self, report_file=None):
        if (report_file is None):
            print("No report file, not sending email.")
            return
        report_url = report_file.replace('/home/lanforge/', '')
        if report_url.startswith('/'):
            report_url = report_url[1:]
        qa_url = self.qa_report_html.replace('home/lanforge','')
        if qa_url.startswith('/'):
            qa_url = qa_url[1:]
        # following recommendation 
        # NOTE: https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-from-nic-in-python
        # Mail
        # command to check if mail running : systemctl status postfix
        # command = 'echo "$HOSTNAME mail system works!" | mail -s "Test: $HOSTNAME $(date)" chuck.rekiere@candelatech.com'
        hostname = socket.getfqdn()
        ip = socket.gethostbyname(hostname)

        # a hostname lacking dots by definition lacks a domain name
        # this is not useful for hyperlinks outside the known domain, so an IP address should be preferred
        if hostname.find('.') < 1:
            hostname = ip

        message_txt =""
        if (self.email_txt != ""):
            message_txt = """{email_txt} lanforge target {lf_mgr_ip}
Results from {hostname}:
http://{hostname}/{report}
""".format(email_txt=self.email_txt,lf_mgr_ip=self.lf_mgr_ip,hostname=hostname,report=report_url)
        else:
            message_txt = """Results from {hostname}:
http://{hostname}/{report}""".format(hostname=hostname,report=report_url)

        # Put in report information current two methods supported, 
        message_txt +="""
QA Report Dashboard:
http://{ip_qa}/{qa_url}
NOTE: Diagrams are links in dashboard""".format(ip_qa=ip,qa_url=qa_url)

        if(self.json_igg != "" ):
            message_txt += """
            
Ghost Blog:
http://{blog}:2368""".format(blog=self.blog_host_ghost)
        
        if (self.email_title_txt != ""):
            mail_subject = "{} [{hostname}] {date}".format(self.email_title_txt, hostname=hostname,
                                                           date=datetime.datetime.now())
        else:
            mail_subject = "Regression Test [{hostname}] {date}".format(hostname=hostname, date=datetime.datetime.now())
        try:
            if self.production_run == True:
                msg = message_txt.format(ip=self.host_ip_production)
                # for postfix from command line  echo "My message" | mail -s subject user@candelatech.com
                command = "echo \"{message}\" | mail -s \"{subject}\" {address}".format(
                    message=msg,
                    subject=mail_subject,
                    address=self.email_list_production)
            else:
                msg = message_txt.format(ip=ip)
                command = "echo \"{message}\" | mail -s \"{subject}\" {address}".format(
                    message=msg,
                    subject=mail_subject,
                    address=self.email_list_test)

            print("running:[{}]".format(command))
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True)
            # have email on separate timeout        
            process.wait(timeout=int(self.test_timeout))
        except subprocess.TimeoutExpired:
            print("send email timed out")
            process.terminate()

    def get_csv_results(self):
        return self.csv_file.name

    def start_csv_results(self):
        print("self.csv_results")
        self.csv_results_file = open(self.csv_results, "w")
        self.csv_results_writer = csv.writer(self.csv_results_file, delimiter=",")
        self.csv_results_column_headers = ['Test', 'Command', 'Result', 'STDOUT', 'STDERR']
        self.csv_results_writer.writerow(self.csv_results_column_headers)
        self.csv_results_file.flush()

    def get_html_results(self):
        return self.html_results

    def start_html_results(self):
        self.html_results += """
                <table border="1" class="dataframe">
                    <thead>
                        <tr style="text-align: left;">
                          <th>Test</th>
                          <th>Command</th>
                          <th>Duration</th>
                          <th>Start</th>
                          <th>End</th>
                          <th>Result</th>
                          <th>STDOUT</th>
                          <th>STDERR</th>
                        </tr>
                      </thead>
                      <tbody>
                      """

    def finish_html_results(self):
        self.html_results += """
                    </tbody>
                </table>
                <br>
                <br>
                <br>
                """

    # Read the json configuration 
    # Read the test rig configuration, which is the LANforge system configuration
    # Read the dut configuration, which is the specific configuration for the AP / VAP or other device under test
    # Read the test configuration, replace the wide card parameters
    # Read igg configuration is for Influx, Grafana and Ghost

    # Reading the test rig configuration
    def read_json_rig(self):
        # self.logger.info("read_config_json_contents {}".format(self.json_rig))
        if "test_parameters" in self.json_rig:
            self.logger.info("json: read test_parameters")
            # self.logger.info("test_parameters {}".format(self.json_rig["test_parameters"]))
            self.read_test_parameters()
        else:
            self.logger.info("EXITING test_parameters not in json {}".format(self.json_rig))
            exit(1)

        if "test_network" in self.json_rig:
            self.logger.info("json: read test_network")
            # self.logger.info("test_network {}".format(self.json_rig["test_network"]))
            self.read_test_network()
        else:
            self.logger.info("EXITING test_network not in json {}".format(self.json_rig))
            exit(1)

        if "radio_dict" in self.json_rig:
            self.logger.info("json: read radio_dict")
            # self.logger.info("radio_dict {}".format(self.json_rig["radio_dict"]))
            self.radio_dict = self.json_rig["radio_dict"]
            self.logger.info("self.radio_dict {}".format(self.radio_dict))
        else:
            self.logger.info("EXITING radio_dict not in json {}".format(self.json_rig))
            exit(1)

    # read dut configuration
    def read_json_dut(self):
        if "test_dut" in self.json_dut:
            self.logger.info("json: read test_dut")
            self.read_dut_parameters()
        else:
            self.logger.info("EXITING test_dut not in json {}".format(self.json_dut))
            exit(1)

    # Top Level for reading the tests to run
    def read_json_test(self):
        if "test_suites" in self.json_test:
            self.logger.info("json: read test_suites looking for: {}".format(self.test_suite))
            # self.logger.info("test_suites {}".format(self.json_test["test_suites"]))
            if self.test_suite in self.json_test["test_suites"]:
                self.test_dict = self.json_test["test_suites"][self.test_suite]
                # self.logger.info("self.test_dict {}".format(self.test_dict))
            else:
                self.logger.info("EXITING test_suite {} Not Present in json test_suites: {}".format(self.test_suite,
                                                                                                    self.json_test[
                                                                                                        "test_suites"]))
                exit(1)
        else:
            self.logger.info("EXITING test_suites not in json {}".format(self.json_test))
            exit(1)

    # Top Level for Influx, Grafana, Ghost configuration
    def read_json_igg(self):
        if "test_database" in self.json_igg:
            self.logger.info("json: read test_database")
            # self.logger.info("test_database {}".format(self.json_rig["test_database"]))
            self.read_test_database()
        else:
            self.logger.info("NOTE: test_database not found in json")

        if "test_dashboard" in self.json_igg:
            self.logger.info("json: read test_dashboard")
            # self.logger.info("test_dashboard {}".format(self.json_rig["test_dashboard"]))
            self.read_test_dashboard()
        else:
            self.logger.info("NOTE: test_dashboard not found in json")

        if "test_blog" in self.json_igg:
            self.logger.info("json: read test_blog")
            # self.logger.info("test_blog {}".format(self.json_rig["test_blog"]))
            self.read_test_blog()
        else:
            self.logger.info("NOTE: test_blog not found in json")

    #TODO change code so if parameter is not present then implied to be false
    def read_test_parameters(self):
        if "test_rig" in self.json_rig["test_parameters"]:
            self.test_rig = self.json_rig["test_parameters"]["test_rig"]
        else:
            self.logger.info("test_rig not in test_parameters json")
        if "database_sqlite" in self.json_rig["test_parameters"]:
            self.database_sqlite = self.json_rig["test_parameters"]["database_sqlite"]
        else:
            self.logger.info("database_sqlite not in test_parameters json")
        if "lf_mgr_ip" in self.json_rig["test_parameters"]:
            self.lf_mgr_ip = self.json_rig["test_parameters"]["lf_mgr_ip"]
        else:
            self.logger.info("lf_mgr_ip not in test_parameters json")
        if "lf_mgr_port" in self.json_rig["test_parameters"]:
            self.lf_mgr_port = self.json_rig["test_parameters"]["lf_mgr_port"]
        else:
            self.logger.info("lf_mgr_port not in test_parameters json")
        if "lf_mgr_user" in self.json_rig["test_parameters"]:
            self.lf_mgr_user = self.json_rig["test_parameters"]["lf_mgr_user"]
        else:
            self.logger.info("lf_mgr_user not in test_parameters json")
        if "lf_mgr_pass" in self.json_rig["test_parameters"]:
            self.lf_mgr_pass = self.json_rig["test_parameters"]["lf_mgr_pass"]
        else:
            self.logger.info("lf_mgr_pass not in test_parameters json")
        if "upstream_port" in self.json_rig["test_parameters"]:
            self.upstream_port = self.json_rig["test_parameters"]["upstream_port"]
        else:
            self.logger.info("upstream_port not in test_parameters json")
        if "test_timeout" in self.json_rig["test_parameters"]:
            self.test_timeout = self.json_rig["test_parameters"]["test_timeout"]
            self.test_timeout_default = self.test_timeout
        else:
            self.logger.info("test_timeout not in test_parameters json")
            exit(1)
        if "load_blank_db" in self.json_rig["test_parameters"]:
            self.load_blank_db = self.json_rig["test_parameters"]["load_blank_db"]
        else:
            self.logger.info("load_blank_db not in test_parameters json")
            exit(1)
        if "load_factory_default_db" in self.json_rig["test_parameters"]:
            self.load_factory_default_db = self.json_rig["test_parameters"]["load_factory_default_db"]
        else:
            self.logger.info("load_factory_default_db not in test_parameters json")
            exit(1)
        if "load_custom_db" in self.json_rig["test_parameters"]:
            self.load_custom_db = self.json_rig["test_parameters"]["load_custom_db"]
        else:
            self.logger.info("load_custom_db not in test_parameters json")
            exit(1)
        if "custom_db" in self.json_rig["test_parameters"]:
            self.custom_db = self.json_rig["test_parameters"]["custom_db"]
        else:
            self.logger.info("custom_db not in test_parameters json, if not using custom_db just put in a name")
            exit(1)
        if "email_list_production" in self.json_rig["test_parameters"]:
            self.email_list_production = self.json_rig["test_parameters"]["email_list_production"]
        else:
            self.logger.info("email_list_production not in test_parameters json")
            exit(1)
        if "host_ip_production" in self.json_rig["test_parameters"]:
            self.host_ip_production = self.json_rig["test_parameters"]["host_ip_production"]
        else:
            self.logger.info("host_ip_production not in test_parameters json")
            exit(1)
        if "email_list_test" in self.json_rig["test_parameters"]:
            self.email_list_test = self.json_rig["test_parameters"]["email_list_test"]
            print(self.email_list_test)
        else:
            self.logger.info("email_list_test not in test_parameters json")
            exit(1)
        if "host_ip_test" in self.json_rig["test_parameters"]:
            self.host_ip_test = self.json_rig["test_parameters"]["host_ip_test"]
        else:
            self.logger.info("host_ip_test not in test_parameters json")
            exit(1)
        if "email_title_txt" in self.json_rig["test_parameters"]:
            self.email_title_txt = self.json_rig["test_parameters"]["email_title_txt"]
        else:
            self.logger.info("email_title_txt not in test_parameters json")
        if "email_txt" in self.json_rig["test_parameters"]:
            self.email_txt = self.json_rig["test_parameters"]["email_txt"]
        else:
            self.logger.info("email_txt not in test_parameters json")
            
        # dut_set_name selectes the DUT to test against , it is different then dut_name
        # this value gets set in the test
    def read_dut_parameters(self):
        if "dut_set_name" in self.json_dut["test_dut"]:
            self.dut_set_name = self.json_dut["test_dut"]["dut_set_name"]
        else:
           self.logger.info("dut_set_name not in test_dut json")
        # dut name will set a chamberview scenerio for a DUT which can be selected with dut_set_name
        if "dut_name" in self.json_dut["test_dut"]:
            self.dut_name = self.json_dut["test_dut"]["dut_name"]
        else:
            self.logger.info("dut_name not in test_dut json")

        if "dut_hw" in self.json_dut["test_dut"]:
            self.dut_hw = self.json_dut["test_dut"]["dut_hw"]
        else:
            self.logger.info("dut_hw not in test_dut json")

        if "dut_sw" in self.json_dut["test_dut"]:
            self.dut_sw = self.json_dut["test_dut"]["dut_sw"]
        else:
            self.logger.info("dut_sw not in test_parameters json")

        if "dut_model" in self.json_dut["test_dut"]:
            self.dut_model = self.json_dut["test_dut"]["dut_model"]
        else:
            self.logger.info("dut_model not in test_dut json")

        if "dut_serial" in self.json_dut["test_dut"]:
            self.dut_serial = self.json_dut["test_dut"]["dut_serial"]
        else:
            self.logger.info("dut_serial not in test_dut json")

        if "dut_bssid_2g" in self.json_dut["test_dut"]:
            self.dut_bssid_2g = self.json_dut["test_dut"]["dut_bssid_2g"]
        else:
            self.logger.info("dut_bssid_2G not in test_dut json")

        if "dut_bssid_5g" in self.json_dut["test_dut"]:
            self.dut_bssid_5g = self.json_dut["test_dut"]["dut_bssid_5g"]
        else:
            self.logger.info("dut_bssid_5g not in test_dut json")

        if "dut_bssid_6g" in self.json_dut["test_dut"]:
            self.dut_bssid_6g = self.json_dut["test_dut"]["dut_bssid_6g"]
        else:
            self.logger.info("dut_bssid_6g not in test_dut json")

        if "ssid_6g_used" in self.json_dut["test_dut"]:
            self.ssid_6g = self.json_dut["test_dut"]["ssid_6g_used"]
        else:
            self.logger.info("ssid_6g_used not in test_dut json")

        if "ssid_6g_pw_used" in self.json_dut["test_dut"]:
            self.ssid_6g_pw = self.json_dut["test_dut"]["ssid_6g_pw_used"]
        else:
            self.logger.info("ssid_6g_pw_used not in test_dut json")

        if "security_6g_used" in self.json_dut["test_dut"]:
            self.security_6g = self.json_dut["test_dut"]["security_6g_used"]
        else:
            self.logger.info("security_6g_used not in test_dut json")

        if "ssid_5g_used" in self.json_dut["test_dut"]:
            self.ssid_5g = self.json_dut["test_dut"]["ssid_5g_used"]
        else:
            self.logger.info("ssid_5g_used not in test_dut json")

        if "ssid_5g_pw_used" in self.json_dut["test_dut"]:
            self.ssid_5g_pw = self.json_dut["test_dut"]["ssid_5g_pw_used"]
        else:
            self.logger.info("ssid_5g_pw_used not in test_dut json")

        if "security_5g_used" in self.json_dut["test_dut"]:
            self.security_5g = self.json_dut["test_dut"]["security_5g_used"]
        else:
            self.logger.info("security_5g_used not in test_dut json")

        if "ssid_2g_used" in self.json_dut["test_dut"]:
            self.ssid_2g = self.json_dut["test_dut"]["ssid_2g_used"]
        else:
            self.logger.info("ssid_2g_used not in test_dut json")

        if "ssid_2g_pw_used" in self.json_dut["test_dut"]:
            self.ssid_2g_pw = self.json_dut["test_dut"]["ssid_2g_pw_used"]
        else:
            self.logger.info("ssid_2g_pw_used not in test_dut json")

        if "security_2g_used" in self.json_dut["test_dut"]:
            self.security_2g = self.json_dut["test_dut"]["security_2g_used"]
        else:
            self.logger.info("security_2g_used not in test_dut json")

    def read_test_network(self):
        if "http_test_ip" in self.json_rig["test_network"]:
            self.http_test_ip = self.json_rig["test_network"]["http_test_ip"]
        else:
            self.logger.info("http_test_ip not in test_network json")
            exit(1)
        if "ftp_test_ip" in self.json_rig["test_network"]:
            self.ftp_test_ip = self.json_rig["test_network"]["ftp_test_ip"]
        else:
            self.logger.info("ftp_test_ip not in test_network json")
            exit(1)
        if "test_ip" in self.json_rig["test_network"]:
            self.ftp_test_ip = self.json_rig["test_network"]["test_ip"]
        else:
            self.logger.info("test_ip not in test_network json")
            exit(1)

    # Optional from --json_igg switch 
    # kpi.csv and meta.txt can be read after test run performed holds same data
    def read_test_database(self):
        if "influx_database_config" in self.json_igg["test_database"]:
            self.influx_database_config = self.json_igg["test_database"]["influx_database_config"]
        else:
            self.logger.info("influx_database_config not in test_database json")
        if "influx_database_host" in self.json_igg["test_database"]:
            self.influx_database_host = self.json_igg["test_database"]["influx_database_host"]
        else:
            self.logger.info("influx_database_host not in test_database json")
        if "influx_database_port" in self.json_igg["test_database"]:
            self.influx_database_port = self.json_igg["test_database"]["influx_database_port"]
        else:
            self.logger.info("influx_database_port not in test_database json")
        if "influx_database_token" in self.json_igg["test_database"]:
            self.influx_database_token = self.json_igg["test_database"]["influx_database_token"]
        else:
            self.logger.info("influx_database_token not in test_database json")
        if "influx_database_org" in self.json_igg["test_database"]:
            self.influx_database_org = self.json_igg["test_database"]["influx_database_org"]
        else:
            self.logger.info("influx_database_org not in test_database json")
        if "influx_database_bucket" in self.json_igg["test_database"]:
            self.influx_database_bucket = self.json_igg["test_database"]["influx_database_bucket"]
        else:
            self.logger.info("influx_database_bucket not in test_database json")
        if "influx_database_tag" in self.json_igg["test_database"]:
            self.influx_database_tag = self.json_igg["test_database"]["influx_database_tag"]
        else:
            self.logger.info("influx_database_tag not in test_database json")

    # Optional only if --json_igg switch 
    def read_test_dashboard(self):
        if "dashboard_config_grafana" in self.json_igg["test_dashboard"]:
            self.dashboard_config_grafana = self.json_igg["test_dashboard"]["dashboard_config_grafana"]
        else:
            self.logger.info("dashboard_config_grafana not in test_dashboard json")

        if "dashboard_host_grafana" in self.json_igg["test_dashboard"]:
            self.dashboard_host_grafana = self.json_igg["test_dashboard"]["dashboard_host_grafana"]
        else:
            self.logger.info("dashboard_host_grafana not in test_dashboard json")

        if "dashboard_token_grafana" in self.json_igg["test_dashboard"]:
            self.dashboard_token_grafana = self.json_igg["test_dashboard"]["dashboard_token_grafana"]
        else:
            self.logger.info("dashboard_token_grafana not in test_dashboard json")

    # Optional on if --json_igg switch
    def read_test_blog(self):
        if "blog_config_ghost" in self.json_igg["test_blog"]:
            self.blog_config_ghost = self.json_igg["test_blog"]["blog_config_ghost"]
        else:
            self.logger.info("blog_config_ghost not in test_blog json")

        if "blog_host_ghost" in self.json_igg["test_blog"]:
            self.blog_host_ghost = self.json_igg["test_blog"]["blog_host_ghost"]
        else:
            self.logger.info("blog_host_ghost not in test_blog json")

        if "blog_token_ghost" in self.json_igg["test_blog"]:
            self.blog_token_ghost = self.json_igg["test_blog"]["blog_token_ghost"]
        else:
            self.logger.info("blog_token_ghost not in test_blog json")

        if "blog_authors_ghost" in self.json_igg["test_blog"]:
            self.blog_authors_ghost = self.json_igg["test_blog"]["blog_authors_ghost"]
        else:
            self.logger.info("blog_authors_ghost not in test_blog json")

        if "blog_customer_ghost" in self.json_igg["test_blog"]:
            self.blog_customer_ghost = self.json_igg["test_blog"]["blog_customer_ghost"]
        else:
            self.logger.info("blog_customer_ghost not in test_blog json")

        if "blog_user_push_ghost" in self.json_igg["test_blog"]:
            self.blog_user_push_ghost = self.json_igg["test_blog"]["blog_user_push_ghost"]
        else:
            self.logger.info("blog_user_push_ghost not in test_blog json")

        if "blog_password_push_ghost" in self.json_igg["test_blog"]:
            self.blog_password_push_ghost = self.json_igg["test_blog"]["blog_password_push_ghost"]
        else:
            self.logger.info("blog_password_push_ghost not in test_blog json")

        if "blog_flag" in self.json_igg["test_blog"]:
            self.blog_flag = self.json_igg["test_blog"]["blog_flag"]
        else:
            self.logger.info("blog_flag not in test_blog json")


    def load_factory_default_db(self):
        # self.logger.info("file_wd {}".format(self.scripts_wd))
        try:
            os.chdir(self.scripts_wd)
            # self.logger.info("Current Working Directory {}".format(os.getcwd()))
        except:
            self.logger.info("failed to change to {}".format(self.scripts_wd))

        # no spaces after FACTORY_DFLT
        command = "./{} {}".format("scenario.py", "--load FACTORY_DFLT")
        process = subprocess.Popen((command).split(' '), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)
        # wait for the process to terminate
        out, err = process.communicate()
        errcode = process.returncode
        print("load_factory_default_db errcode: {errcode}".format(errcode=errcode))

    # not currently used
    def load_blank_db(self):
        try:
            os.chdir(self.scripts_wd)
        except:
            self.logger.info("failed to change to {}".format(self.scripts_wd))

        # no spaces after FACTORY_DFLT
        command = "./{} {}".format("scenario.py", "--load BLANK")
        process = subprocess.Popen((command).split(' '), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)
        # wait for the process to terminate
        out, err = process.communicate()
        errcode = process.returncode
        print("load_blank_db errcode: {errcode}".format(errcode=errcode))


    def load_custom_db(self, custom_db):
        try:
            os.chdir(self.scripts_wd)
        except:
            self.logger.info("failed to change to {}".format(self.scripts_wd))

        # no spaces after FACTORY_DFLT
        command = "./{} {}".format("scenario.py", "--load {}".format(custom_db))
        process = subprocess.Popen((command).split(' '), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)
        # wait for the process to terminate
        out, err = process.communicate()
        errcode = process.returncode
        print("load_custome_db errcode: {errcode}".format(errcode=errcode))

    def run_script_test(self):
        self.start_html_results()
        self.start_csv_results()
        print(self.test_dict)

        # loop through radios (For future functionality based on radio)
        for radio in self.radio_dict:
            # This has been changed to reflect the Radio configuriaton of LANforge, for now print
            print("rig json config: RADIO: {radio} DRIVER: {driver} CAPABILITIES {cap} MAX_STA {max_sta} MAX_VAP {max_vap} MAX_VIFS {max_vif}".format(
                radio=self.radio_dict[radio]['RADIO'],driver=self.radio_dict[radio]['DRIVER'],cap=self.radio_dict[radio]['CAPABILITIES'],
                max_sta=self.radio_dict[radio]['MAX_STA'],max_vap=self.radio_dict[radio]['MAX_VAP'],max_vif=self.radio_dict[radio]['MAX_VIFS']))

        # Configure Tests
        for test in self.test_dict:
            if self.test_dict[test]['enabled'] == "FALSE":
                self.logger.info("test: {}  skipped".format(test))
            # load the default database 
            elif self.test_dict[test]['enabled'] == "TRUE":
                #TODO Place test interations here
                if 'iterations' in self.test_dict[test]:
                    self.logger.info("iterations : {}".format(self.test_dict[test]['iterations']))
                    self.test_iterations = int(self.test_dict[test]['iterations'])
                else:
                    self.test_iterations = self.test_iterations_default

                iteration = 0                
                for iteration in range(self.test_iterations):
                    iteration += 1

                    # if args key has a value of an empty string then need to manipulate the args_list to args 
                    # list does not have replace only stings do to args_list will be joined and  converted to a string and placed
                    # in args.  Then the replace below will work.
                    if self.test_dict[test]['args'] == "":
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace(self.test_dict[test]['args'],
                                                                                            ''.join(self.test_dict[test][
                                                                                                        'args_list']))

                    if 'DATABASE_SQLITE' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('DATABASE_SQLITE', self.database_sqlite)
                    if 'HTTP_TEST_IP' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('HTTP_TEST_IP', self.http_test_ip)
                    if 'FTP_TEST_IP' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('FTP_TEST_IP', self.ftp_test_ip)
                    if 'TEST_IP' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('TEST_IP', self.test_ip)

                    if 'LF_MGR_USER' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('LF_MGR_USER', self.lf_mgr_user)
                    if 'LF_MGR_PASS' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('LF_MGR_PASS', self.lf_mgr_pass)

                    if 'LF_MGR_IP' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('LF_MGR_IP', self.lf_mgr_ip)
                    if 'LF_MGR_PORT' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('LF_MGR_PORT', self.lf_mgr_port)

                    # DUT Configuration
                    if 'DUT_NAME' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('DUT_NAME', self.dut_name)
                    if 'DUT_HW' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('DUT_HW', self.dut_hw)
                    if 'DUT_SW' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('DUT_SW', self.dut_sw)
                    if 'DUT_MODEL' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('DUT_MODEL', self.dut_model)
                    if 'DUT_SERIAL' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('DUT_SERIAL', self.dut_serial)

                    if 'DUT_BSSID_2G' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('DUT_BSSID_2G', self.dut_bssid_2g)
                    if 'SSID_2G_USED' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('SSID_2G_USED', self.ssid_2g)
                    if 'SSID_2G_PW_USED' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('SSID_2G_PW_USED', self.ssid_2g_pw)
                    if 'SECURITY_2G_USED' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('SECURITY_2G_USED', self.security_2g)

                    if 'DUT_BSSID_5G' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('DUT_BSSID_5G', self.dut_bssid_5g)
                    if 'SSID_5G_USED' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('SSID_5G_USED', self.ssid_5g)
                    if 'SSID_5G_PW_USED' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('SSID_5G_PW_USED', self.ssid_5g_pw)
                    if 'SECURITY_5G_USED' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('SECURITY_5G_USED', self.security_5g)

                    if 'DUT_BSSID_6G' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('DUT_BSSID_6G', self.dut_bssid_6g)
                    if 'SSID_6G_USED' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('SSID_6G_USED', self.ssid_6g)
                    if 'SSID_6G_PW_USED' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('SSID_6G_PW_USED', self.ssid_6g_pw)
                    if 'SECURITY_6G_USED' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('SECURITY_6G_USED', self.security_6g)


                    if 'NUM_STA' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('NUM_STA', self.num_sta)
                    if 'COL_NAMES' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('COL_NAMES', self.col_names)
                    if 'UPSTREAM_PORT' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('UPSTREAM_PORT',
                                                                                            self.upstream_port)

                    # lf_dataplane_test.py and lf_wifi_capacity_test.py use a parameter --local_path for the location 
                    # of the reports when the reports are pulled.
                    if 'REPORT_PATH' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('REPORT_PATH', self.report_path)

                    # The TEST_BED is the database tag
                    if 'TEST_BED' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('TEST_BED', self.influx_database_tag)

                    # Influx database configuration 
                    if 'influx_database_host' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('influx_database_host',
                                                                                            self.influx_database_host)
                    if 'influx_database_port' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('influx_database_port',
                                                                                            self.influx_database_port)
                    if 'influx_database_token' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('influx_database_token',
                                                                                            self.influx_database_token)
                    if 'influx_database_org' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('influx_database_org',
                                                                                            self.influx_database_org)
                    if 'influx_database_bucket' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('influx_database_bucket',
                                                                                            self.influx_database_bucket)
                    if 'influx_database_tag' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('influx_database_tag',
                                                                                            self.influx_database_tag)
                    if 'DUT_SET_NAME' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('DUT_SET_NAME',
                                                                                            self.dut_set_name)
                    if 'TEST_RIG' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('TEST_RIG', self.test_rig)
                    # end of database configuration                        

                    # dashboard configuration
                    if 'dashboard_host_grafana' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('dashboard_host_grafana',
                                                                                            self.dashboard_host_grafana)
                    if 'dashboard_token_grafana' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('dashboard_token_grafana',
                                                                                            self.dashboard_token_grafana)
                    # end of dashboard configuraiton

                    # blog configuration
                    if 'blog_host_ghost' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('blog_host_ghost', self.blog_host_ghost)
                    if 'blog_token_ghost' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('blog_token_ghost', self.blog_token_ghost)
                    if 'blog_authors_ghost' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('blog_authors_ghost',
                                                                                            self.blog_authors_ghost)
                    if 'blog_customer_ghost' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('blog_customer_ghost',
                                                                                            self.blog_customer_ghost)
                    if 'blog_user_push_ghost' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('blog_user_push_ghost',
                                                                                            self.blog_user_push_ghost)
                    if 'blog_password_push_ghost' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('blog_password_push_ghost',
                                                                                            self.blog_password_push_ghost)
                    if 'BLOG_FLAG' in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('BLOG_FLAG', self.blog_flag)
                    # end of blog configruation

                    if 'timeout' in self.test_dict[test]:
                        self.logger.info("timeout : {}".format(self.test_dict[test]['timeout']))
                        self.test_timeout = int(self.test_dict[test]['timeout'])
                    else:
                        self.test_timeout = self.test_timeout_default

                    if 'load_db' in self.test_dict[test]:
                        self.logger.info("load_db : {}".format(self.test_dict[test]['load_db']))
                        if str(self.test_dict[test]['load_db']).lower() != "none" and str(
                                self.test_dict[test]['load_db']).lower() != "skip":
                            try:
                                self.load_custom_db(self.test_dict[test]['load_db'])
                            except:
                                self.logger.info("custom database failed to load check existance and location: {}".format(
                                    self.test_dict[test]['load_db']))
                    else:
                        self.logger.info("no load_db present in dictionary, load db normally")
                        if self.use_factory_default_db == "TRUE":
                            self.load_factory_default_db()
                            sleep(3)
                            self.logger.info("FACTORY_DFLT loaded between tests with scenario.py --load FACTORY_DFLT")
                        if self.use_blank_db == "TRUE":
                            self.load_blank_db()
                            sleep(1)
                            self.logger.info("BLANK loaded between tests with scenario.py --load BLANK")
                        if self.use_custom_db == "TRUE":
                            try:
                                self.load_custom_db(self.custom_db)
                                sleep(1)
                                self.logger.info("{} loaded between tests with scenario.py --load {}".format(self.custom_db,
                                                                                                             self.custom_db))
                            except:
                                self.logger.info("custom database failed to load check existance and location: {}".format(
                                    self.custom_db))
                        else:
                            self.logger.info("no db loaded between tests: {}".format(self.use_custom_db))

                    sleep(1)  # DO NOT REMOVE the sleep is to allow for the database to stablize
                    try:
                        os.chdir(self.scripts_wd)
                        # self.logger.info("Current Working Directory {}".format(os.getcwd()))
                    except:
                        self.logger.info("failed to change to {}".format(self.scripts_wd))
                    cmd_args = "{}".format(self.test_dict[test]['args'])
                    command = "./{} {}".format(self.test_dict[test]['command'], cmd_args)
                    self.logger.info("command: {}".format(command))
                    self.logger.info("cmd_args {}".format(cmd_args))

                    if self.outfile_name is not None:
                        stdout_log_txt = os.path.join(self.log_path, "{}-{}-stdout.txt".format(self.outfile_name,test))
                        self.logger.info("stdout_log_txt: {}".format(stdout_log_txt))
                        stdout_log = open(stdout_log_txt, 'a')
                        stderr_log_txt = os.path.join(self.log_path, "{}-{}-stderr.txt".format(self.outfile_name,test))
                        self.logger.info("stderr_log_txt: {}".format(stderr_log_txt))
                        stderr_log = open(stderr_log_txt, 'a')

                    # need to take into account --raw_line parameters thus need to use shlex.split 
                    # need to preserve command to have correct command syntax in command output
                    command_to_run = command
                    command_to_run = shlex.split(command_to_run)
                    print("running {command_to_run}".format(command_to_run=command_to_run))
                    self.test_start_time = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")).replace(':','-')
                    print("Test start: {time}".format(time=self.test_start_time))
                    start_time = datetime.datetime.now()
                    try:
                        process = subprocess.Popen(command_to_run, shell=False, stdout=stdout_log, stderr=stderr_log,
                                                   universal_newlines=True)
                        # if there is a better solution please propose,  the TIMEOUT Result is different then FAIL
                        try:
                            if int(self.test_timeout != 0):
                                process.wait(timeout=int(self.test_timeout))
                            else:
                                process.wait()
                        except subprocess.TimeoutExpired:
                            process.terminate()
                            self.test_result = "TIMEOUT"

                    except:
                        print("No such file or directory with command: {}".format(command))
                        self.logger.info("No such file or directory with command: {}".format(command))

                    end_time = datetime.datetime.now()
                    self.test_end_time = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")).replace(':','-')
                    print("Test end time {time}".format(time=self.test_end_time))

                    time_delta = end_time - start_time
                    self.duration = "{day}d {seconds}s {msec} ms".format(
                        day=time_delta.days,seconds=time_delta.seconds,msec=time_delta.microseconds)

                    # If collect meta data is set
                    meta_data_path = ""
                    if self.test_result != "TIMEOUT":
                        stdout_log_size = os.path.getsize(stdout_log_txt)
                        if stdout_log_size > 0:
                            stdout_log_fd = open(stdout_log_txt)
                            #"Report Location:::/home/lanforge/html-reports/wifi-capacity-2021-08-17-04-02-56"
                            #
                            for line in stdout_log_fd:
                                if "Report Location" in line:
                                    meta_data_path = line.replace('"','')
                                    meta_data_path = meta_data_path.replace('Report Location:::','')
                                    meta_data_path = meta_data_path.split('/')[-1]
                                    meta_data_path = meta_data_path.strip()
                                    meta_data_path = self.report_path + '/' + meta_data_path + '/meta.txt'
                                    break
                            stdout_log_fd.close()
                        if meta_data_path != "":
                            meta_data_fd = open(meta_data_path,'w+')
                            meta_data_fd.write('$ Generated by Candela Technologies LANforge network testing tool\n')
                            meta_data_fd.write('$ meta.txt file location\n')
                            meta_data_fd.write("file {path}\n".format(path=meta_data_path))
                            meta_data_fd.write('$ LANforge GUI\n')
                            meta_data_fd.write('gui_version: {gui_version} \n'.format(gui_version=self.lanforge_gui_version))
                            meta_data_fd.write('$ LANforge command\n')
                            meta_data_fd.write("command {command}\n".format(command=command))
                            # split command at test-tag , at rest of string once at the actual test-tag value
                            test_tag = command.split('test_tag',maxsplit=1)[-1].split(maxsplit=1)[0]
                            test_tag = test_tag.replace("'","")
                            meta_data_fd.write('$ LANforge test_tag\n')
                            meta_data_fd.write("test_tag {test_tag}\n".format(test_tag=test_tag))
                            # LANforge information is a list thus [0]
                            meta_data_fd.write('$ LANforge Information\n')
                            meta_data_fd.write("lanforge_system_node {lanforge_system_node}\n".format(lanforge_system_node=self.lanforge_system_node_version[0]))
                            meta_data_fd.write("lanforge_kernel_version {lanforge_kernel_version}\n".format(lanforge_kernel_version=self.lanforge_kernel_version[0]))
                            meta_data_fd.write("lanforge_gui_version_full {lanforge_gui_version_full}\n".format(lanforge_gui_version_full=self.lanforge_gui_version_full[0]))
                            meta_data_fd.close()

                    if self.test_result != "TIMEOUT":
                        stderr_log_size = os.path.getsize(stderr_log_txt)
                        if stderr_log_size > 0:
                            self.logger.info("File: {} is not empty: {}".format(stderr_log_txt, str(stderr_log_size)))
                            text = open(stderr_log_txt).read()
                            if 'Error' in text:
                                self.text_result = "Failure"
                                background = self.background_red
                            else:
                                self.test_result = "Success"
                                background = self.background_green
                        else:
                            self.logger.info("File: {} is empty: {}".format(stderr_log_txt, str(stderr_log_size)))
                            self.test_result = "Success"
                            background = self.background_green
                    else:
                        self.logger.info("TIMEOUT FAILURE,  Check LANforge Radios")
                        self.test_result = "Time Out"
                        background = self.background_purple

                    # Ghost will put data in stderr 
                    if 'ghost' in command or 'lf_qa' in command:
                        if self.test_result != "TIMEOUT":
                            text = open(stderr_log_txt).read()
                            if 'Error' in text:
                                self.test_result = "Failure"
                                background = self.background_red
                            else:
                                self.test_result = "Success"
                                background = self.background_blue
                    if 'lf_qa' in command:
                        line_list = open(stdout_log_txt).readlines()
                        for line in line_list:
                            if 'html report:' in line:
                                self.qa_report_html = line
                                print("html_report: {report}".format(report=self.qa_report_html))
                                break

                        self.qa_report_html = self.qa_report_html.replace('html report: ','')


                    # stdout_log_link is used for the email reporting to have the corrected path
                    stdout_log_link = str(stdout_log_txt).replace('/home/lanforge', '')
                    stderr_log_link = str(stderr_log_txt).replace('/home/lanforge', '')
                    if command.find(' ') > 1:
                        short_cmd = command[0:command.find(' ')]
                    else:
                        short_cmd = command

                    self.html_results += """
                    <tr><td>""" + str(test) + """</td>
                    <td>""" + str(short_cmd) + """</td>
                    <td class='TimeFont'>""" + str(self.duration) + """</td>
                    <td class='DateFont'>""" + str(self.test_start_time) + """</td>
                    <td class='DateFont'>""" + str(self.test_end_time) + """</td>
                    <td style=""" + str(background) + """>""" + str(self.test_result) + """ 
                    <td><a href=""" + str(stdout_log_link) + """ target=\"_blank\">STDOUT</a></td>"""
                    if self.test_result == "Failure":
                        self.html_results += """<td><a href=""" + str(
                            stderr_log_link) + """ target=\"_blank\">STDERR</a></td>"""
                    elif self.test_result == "Time Out":
                        self.html_results += """<td><a href=""" + str(
                            stderr_log_link) + """ target=\"_blank\">STDERR</a></td>"""
                    else:
                        self.html_results += """<td></td>"""
                    
                    self.html_results += """</tr>"""
                    #TODO - plase copy button at end and selectable , so individual sections may be copied
                    if command != short_cmd:
                        '''self.html_results += f"""<tr><td colspan='8' class='scriptdetails'>
                            <span class='copybtn'>Copy</span>
                             <tt onclick='copyTextToClipboard(this)'>{command}</tt>
                             </td></tr>
                             """.format(command=command)'''
                        self.html_results += f"""<tr><td colspan='8' class='scriptdetails'>
                             <tt onclick='copyTextToClipboard(this)'>{command}</tt>
                             </td></tr>
                             """.format(command=command)

                        #nocopy
                        '''
                        self.html_results += f"""<tr><td colspan='8' class='scriptdetails'>
                             <tt>{command}</tt>
                             </td></tr>
                             """.format(command=command)
                        '''                            

                    row = [test, command, self.test_result, stdout_log_txt, stderr_log_txt]
                    self.csv_results_writer.writerow(row)
                    self.csv_results_file.flush()
                    # self.logger.info("row: {}".format(row))
                    self.logger.info("test: {} executed".format(test))

                else:
                    self.logger.info(
                        "enable value {} invalid for test: {}, test skipped".format(self.test_dict[test]['enabled'], test))
        self.finish_html_results()


def main():
    # arguments
    parser = argparse.ArgumentParser(
        prog='lf_check.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            lf_check.py : running scripts  
            ''',
        description='''\
lf_check.py
-----------

Summary :
---------
running scripts 

Example :  
./lf_check.py --json_rig rig.json --json_dut dut.json --json_test tests.json --suite suite_test
note if all json data (rig,dut,tests)  in same json file pass same json in for all 3 inputs
---------
            ''')

    parser.add_argument('--dir', help="--dir <results directory>", default="lf_check")
    parser.add_argument('--path', help="--path <results path>", default="/home/lanforge/html-results")
    parser.add_argument('--json_rig', help="--json_rig <rig json config> ", default="", required=True)
    parser.add_argument('--json_dut', help="--json_dut <dut json config> ", default="", required=True)
    parser.add_argument('--json_test', help="--json_test <test json config> ", default="", required=True)
    parser.add_argument('--json_igg', help="--json_igg <influx grafana ghost json config> ", default="")
    parser.add_argument('--suite', help="--suite <suite name>  default TEST_DICTIONARY", default="TEST_DICTIONARY")
    parser.add_argument('--production', help="--production  stores true, sends email results to production email list",
                        action='store_true')
    parser.add_argument('--outfile', help="--outfile <Output Generic Name>  used as base name for all files generated",
                        default="")
    parser.add_argument('--logfile', help="--logfile <logfile Name>  logging for output of lf_check.py script",
                        default="lf_check.log")

    args = parser.parse_args()

    # load test config file information either <config>.json
    json_rig = ""
    try:
        print("args.json_rig {rig}".format(rig=args.json_rig))
        with open(args.json_rig, 'r') as json_rig_config:
            json_rig = json.load(json_rig_config)
    except:
        print("Error reading {}".format(args.json_rig))        

    json_dut = ""
    try:
        print("args.json_dut {dut}".format(dut=args.json_dut))
        with open(args.json_dut, 'r') as json_dut_config:
            json_dut = json.load(json_dut_config)
    except:
        print("Error reading {}".format(args.json_dut))        

    json_test = ""
    try:
        print("args.json_test {}".format(args.json_test))
        with open(args.json_test, 'r') as json_test_config:
            json_test = json.load(json_test_config)
    except:
        print("Error reading {}".format(args.json_test))

    json_igg = ""
    if args.json_igg != "":
        try:
            print("args.json_igg {}".format(args.json_igg))
            with open(args.json_igg, 'r') as json_igg_config:
                json_igg = json.load(json_igg_config)
        except:
            print("Error reading {}".format(args.json_igg))


    # Test-rig information information
    lanforge_system_node_version = 'NO_LF_NODE_VER'
    scripts_git_sha = 'NO_GIT_SHA'
    lanforge_kernel_version = 'NO_KERNEL_VER'
    lanforge_gui_version_full = 'NO_LF_GUI_VER'

    # select test suite 
    test_suite = args.suite
    __dir = args.dir
    __path = args.path

    if args.production:
        production = True
        print("Email to production list")
    else:
        production = False
        print("Email to email list")

    # create report class for reporting
    report = lf_report(_path = __path,
                       _results_dir_name=__dir,
                       _output_html="lf_check.html",
                       _output_pdf="lf-check.pdf")

    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    csv_results = "lf_check{}-{}.csv".format(args.outfile, current_time)
    csv_results = report.file_add_path(csv_results)
    outfile_name = "lf_check-{}-{}".format(args.outfile, current_time)
    outfile = report.file_add_path(outfile_name)
    report_path = report.get_report_path()
    log_path = report.get_log_path()

    # lf_check() class created
    check = lf_check(_json_rig=json_rig,
                     _json_dut=json_dut,
                     _json_test=json_test,
                     _test_suite=test_suite,
                     _json_igg=json_igg,
                     _production=production,
                     _csv_results=csv_results,
                     _outfile=outfile,
                     _outfile_name = outfile_name,
                     _report_path=report_path,
                     _log_path=log_path)

    # set up logging
    logfile = args.logfile[:-4]
    print("logfile: {}".format(logfile))
    logfile = "{}-{}.log".format(logfile, current_time)
    logfile = report.file_add_path(logfile)
    print("logfile {}".format(logfile))
    formatter = logging.Formatter(FORMAT)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(logfile, "w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(logging.StreamHandler(sys.stdout))  # allows to logging to file and stdout

    # read config and run tests
    check.read_json_rig()  #check.read_config
    check.read_json_dut()
    check.read_json_test()
    
    if args.json_igg != "":
        print("Tests need to have influx parameters passed in")
        check.read_json_igg()

    ping_result = check.check_if_port_exists(json_igg)
    for key, value in ping_result.items():
        if value[1] is None:
            print(UserWarning('Check your %s IP address, %s is unreachable' % (key, value[0])))
        else:
            print('%s IP address %s accessible' % (key, value[1]))


    # get sha and lanforge information for results
    # Need to do this after reading the configuration
    try:
        scripts_git_sha = check.get_scripts_git_sha()
        print("git_sha {sha}".format(sha=scripts_git_sha))
    except:
        print("git_sha read exception ")

    try:
        lanforge_system_node_version = check.get_lanforge_system_node_version()
        print("lanforge_system_node_version {system_node_ver}".format(system_node_ver=lanforge_system_node_version))
    except:
        print("lanforge_system_node_version exception")

    try:
        lanforge_kernel_version = check.get_lanforge_kernel_version()
        print("lanforge_kernel_version {kernel_ver}".format(kernel_ver=lanforge_kernel_version))
    except:
        print("lanforge_kernel_version exception, tests aborted check lanforge ip")
        exit(1)

    try:
        lanforge_gui_version_full = check.get_lanforge_gui_version()
        print("lanforge_gui_version_full {lanforge_gui_version_full}".format(lanforge_gui_version_full=lanforge_gui_version_full))
    except:
        print("lanforge_gui_version exception, tests aborted check lanforge ip")
        exit(1)

    try:
        lanforge_radio_json, lanforge_radio_text = check.get_lanforge_radio_information()
        lanforge_radio_formatted_str = json.dumps(lanforge_radio_json, indent = 2)
        print("lanforge_radio_json: {lanforge_radio_json}".format(lanforge_radio_json=lanforge_radio_formatted_str))

        # note put into the meta data
        lf_radio_df = pd.DataFrame(columns = ['Radio','WIFI-Radio Driver','Radio Capabilities','Firmware Version','max_sta','max_vap','max_vifs'])

        for key in lanforge_radio_json:
            if 'wiphy' in key: 
                #print("key {}".format(key))
                #print("lanforge_radio_json[{}]: {}".format(key,lanforge_radio_json[key]))
                driver = lanforge_radio_json[key]['driver'].split('Driver:',maxsplit=1)[-1].split(maxsplit=1)[0]
                try:
                    firmware_version = lanforge_radio_json[key]['firmware version']
                except:
                    print("5.4.3 radio fw version not in /radiostatus/all")
                    firmware_version = "5.4.3 N/A"

                lf_radio_df = lf_radio_df.append(
                    {'Radio':lanforge_radio_json[key]['entity id'],
                    'WIFI-Radio Driver': driver,
                    'Radio Capabilities':lanforge_radio_json[key]['capabilities'],
                    'Firmware Version':firmware_version,
                    'max_sta':lanforge_radio_json[key]['max_sta'],
                    'max_vap':lanforge_radio_json[key]['max_vap'],
                    'max_vifs':lanforge_radio_json[key]['max_vifs']}, ignore_index = True)
        print("lf_radio_df:: {lf_radio_df}".format(lf_radio_df=lf_radio_df))

    except Exception as error:
        print("print_exc(): {error}".format(error=error))
        traceback.print_exc(file=sys.stdout)
        lf_radio_df = pd.DataFrame()
        print("get_lanforge_radio_json exception, no radio data")

    # LANforge and scripts config for results
    lf_test_setup = pd.DataFrame()
    lf_test_setup['LANforge'] = lanforge_system_node_version
    lf_test_setup['kernel version'] = lanforge_kernel_version
    lf_test_setup['GUI version'] = lanforge_gui_version_full
    lf_test_setup['scripts git sha'] = scripts_git_sha

    # Successfully gathered LANforge information Run Tests
    check.run_script_test()

    # generate output reports
    test_rig = check.get_test_rig()
    report.set_title("LF Check: {test_rig} lf_check.py".format(test_rig=test_rig))
    report.build_banner_left()
    report.start_content_div2()
    report.set_obj_html("Objective", "Run QA Tests")
    report.build_objective()
    report.set_table_title("LANForge")
    report.build_table_title()
    report.set_table_dataframe(lf_test_setup)
    report.build_table()
    report.set_table_title("LANForge Radios")
    report.build_table_title()
    report.set_table_dataframe(lf_radio_df)
    report.build_table()
    report.set_table_title("LF Check Test Results")
    report.build_table_title()
    html_results = check.get_html_results()
    report.set_custom_html(html_results)
    report.build_custom()
    report.build_footer()
    report.copy_js()
    html_report = report.write_html_with_timestamp()
    print("html report: {}".format(html_report))
    try:
        report.write_pdf_with_timestamp()
    except:
        print("exception write_pdf_with_timestamp()")

    print("lf_check_html_report: " + html_report)
    check.send_results_email(report_file=html_report)


if __name__ == '__main__':
    main()
