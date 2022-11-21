#!/usr/bin/python3

'''
NAME: lf_check.py

PURPOSE: lf_check.py run tests based on test rig json input, test dut json input,  and test command line inputs

EXAMPLE:

./lf_check.py --json_rig <rig_json> --json_dut <dut_json> --json_test <tests json> --test_suite <suite_name> --path <path to results>
./lf_check.py --json_rig <rig_json> --json_dut <dut_json> --json_test <tests json> --test_suite <suite_name> --path <path to results>  --production

./lf_check.py  --json_rig ct_us_001_rig.json --json_dut ct_001_AX88U_dut.json
    --json_test ct_us_001_tests.json  --suite "suite_wc_dp"  --path '/home/lanforge/html-reports/ct-us-001'


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
1. Using curl
 https://docs.python-requests.org/en/latest/
 https://stackoverflow.com/questions/26000336/execute-curl-command-within-a-python-script - use requests
 curl --user "lanforge:lanforge" -H 'Accept: application/json'
 http://192.168.100.116:8080/radiostatus/all | json_pp  , where --user
 "USERNAME:PASSWORD"

2. (using Python) 
    request_command = 'http://{lfmgr}:{port}/radiostatus/all'.format(lfmgr=self.lf_mgr, port=self.lf_port)
    request = requests.get( request_command, auth=(self.lf_user, self.lf_passwd))
    lanforge_radio_json = request.json()


3. if the connection to 8080 is rejected check : pgrep -af java  , to see the number of GUI instances running

4. getting the lanforge GUI version
curl -H 'Accept: application/json' http://localhost:8080/ | json_pp
{
   "VersionInfo" : {
      "BuildDate" : "Sun 19 Sep 2021 02:36:51 PM PDT",
      "BuildMachine" : "v-f30-64",
      "BuildVersion" : "5.4.4",
      "Builder" : "greearb",
      "GitVersion" : "a98d7fbb8ca4e5c4f736a70e5cc3759e44aba636",
      "JsonVersion" : "1.0.25931"
   },

user@user:~/git/lf-scripts/py-json/LANforge$ curl -H 'Accept: application/json' http://192.168.100.178:8080/ | json_pp | grep -A 7 "VersionInfo"
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 11532  100 11532    0     0  91523      0 --:--:-- --:--:-- --:--:-- 91523
   "VersionInfo" : {
      "BuildDate" : "Wed 09 Mar 2022 12:14:20 PM PST",
      "BuildMachine" : "v-f30-64",
      "BuildVersion" : "5.4.5",
      "Builder" : "greearb",
      "GitVersion" : "0aab99fc6974b6abf805a05dadacf78dec228f94",
      "JsonVersion" : "1.0.26808"
   },
user@user:~/git/lf-scripts/py-json/LANforge$ 


curl -u 'user:pass' -H 'Accept: application/json' http://<lanforge ip>:8080 | json_pp  | grep -A 7 "VersionInfo"

5. for Fedora you can do a:  dnf group list  , to see what all is installed
    dnf group install "Development Tools" for example,  to install a group

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

# Capture the LANforge client output sdtout and stderr
/home/lanforge/LANforgeGUI/lfclient.bash -cli-socket 3990 -s LF_MGR command > >(tee -a stdout.log) 2> >(tee -a stderr.log >&2)

# To get the --raw_line commands
# Build Chamber View Scenario in the GUI and then # copy/tweak what it shows in the 'Text Output' tab after saving and re-opening # the scenario

# issue a shutdown command on the lanforge(s)
#  ssh root@lanforge reboot (need to verify)  or do a shutdown
# send curl command to remote power switch to reboot testbed
#   curl -s http://admin:lanforge@192.168.100.237/outlet?1=CCL -o /dev/null 2>&1
#


'''

from psutil import TimeoutExpired
import requests
import pandas as pd
import paramiko
import shlex
import shutil
import csv
import subprocess
import json
import argparse
from time import sleep
import time
import logging
import socket
import importlib
import platform
import os
import datetime
import sys
import traceback

if sys.version_info[0] != 3:
    print("This script requires Python3")
    exit()


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
lf_report = importlib.import_module("lf_report")
lf_kpi_csv = importlib.import_module("lf_kpi_csv")
logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("lf_logger_config")


# lf_report is from the parent of the current file
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)


# setup logging FORMAT
FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'


# lf_check class contains verificaiton configuration and ocastrates the
# testing.
class lf_check():
    def __init__(self,
                 _json_rig,
                 _json_dut,
                 _json_test,
                 _test_suite,
                 _use_test_list,
                 _test_list,
                 _server_override,
                 _db_override,
                 _production,
                 _csv_results,
                 _outfile,
                 _outfile_name,
                 _report_path,
                 _log_path):

        # test configuration
        self.json_rig = _json_rig
        self.json_dut = _json_dut
        self.json_test = _json_test
        self.test_suite = _test_suite
        self.use_test_list = _use_test_list
        self.test_list = _test_list
        self.server_override = _server_override
        self.db_override = _db_override
        self.production_run = _production
        self.report_path = _report_path
        self.log_path = _log_path
        self.test_dict = {}
        # This is needed for iterations and batch testing.
        self.test_dict_original_json = {}
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        # TODO have method to pass in other
        # script directories , currently only top lanforge scripts directory and py-scripts
        self.scripts_wd = os.getcwd()
        self.lanforge_wd = os.path.dirname(os.getcwd())
        self.results = ""
        self.outfile = _outfile
        self.outfile_name = _outfile_name
        self.test_result = "Failure"
        self.tests_run = 0
        self.tests_success = 0
        self.tests_failure = 0
        self.tests_some_failure = 0
        self.tests_timeout = 0
        self.results_col_titles = [
            "Test", "Command", "Result", "STDOUT", "STDERR"]
        self.html_results = ""
        self.background_green = "background-color:green"
        self.background_red = "background-color:red"
        self.background_orange = "background-color:orange"
        self.background_purple = "background-color:purple"
        self.background_blue = "background-color:blue"

        # LANforge information
        self.lanforge_system_node_version = ""
        self.lanforge_fedora_version = ""
        self.lanforge_kernel_version = ""
        self.lanforge_server_version_full = ""
        self.lanforge_server_version = ""
        self.lanforge_gui_version_full = ""
        self.lanforge_gui_version = ""
        self.lanforge_gui_build_date = ""
        self.lanforge_gui_git_sha = ""

        # meta.txt
        self.meta_data_path = ""

        # lanforge configuration
        self.lf_mgr_ip = "192.168.0.102"
        self.lf_mgr_port = "8080"
        # TODO allow for json configuration
        self.lf_mgr_ssh_port = "22"
        self.lf_mgr_user = "lanforge"
        self.lf_mgr_pass = "lanforge"
        self.upstream_port = ""
        self.upstream_alias = ""

        # results
        self.test_server = ""
        self.database_sqlite = ""
        self.suite_start_time = ""
        self.suite_end_time = ""
        self.suite_duration = ""
        self.test_start_time = ""
        self.test_end_time = ""
        self.duration = ""

        self.http_test_ip = ""
        self.ftp_test_ip = ""
        self.test_ip = ""

        # current test running
        self.test = None
        self.report_index = 0
        self.iteration = 0
        self.channel_list = []
        self.channel = 'NA'
        self.nss_list = []
        self.nss = 'NA'
        self.bandwidth_list = []
        self.bandwidth = 'NA'
        self.tx_power_list = []
        self.tx_power = 'NA'

        # section DUT
        # dut selection
        # note the name will be set as --set DUT_NAME ASUSRT-AX88U, this is not
        # dut_name (see above)
        self.dut_set_name = 'DUT_NAME ASUSRT-AX88U'
        self.use_dut_name = "DUT_NAME_NA"  # "ASUSRT-AX88U" note this is not dut_set_name
        self.dut_hw = "DUT_HW_NA"
        self.dut_sw = "DUT_SW_NA"
        self.dut_model = "DUT_MODEL_NA"
        self.dut_serial = "DUT_SN_NA"

        self.dut_wireless_network_dict = {}

        self.csv_results = _csv_results
        self.csv_results_file = ""
        self.csv_results_writer = ""
        self.csv_results_column_headers = ""
        self.logger = logging.getLogger(__name__)
        self.test_timeout = 120
        self.test_timeout_default = 120
        self.test_iterations_default = 1
        self.iteration = 0
        self.use_blank_db = "FALSE"
        self.use_factory_default_db = "FALSE"
        self.use_custom_db = "FALSE"
        self.email_list_production = ""
        self.email_list_test = ""
        self.email_title_txt = ""
        self.email_txt = ""

        # DUT , Test rig must match testbed
        self.test_rig = "CT-US-NA"
        self.test_rig_json = ""

        # QA report
        self.qa_report_html = "NA"
        self.database_qa = ""
        self.table_qa = ""
        self.test_run = ""
        self.hostname = ""

    def get_test_rig(self):
        return self.test_rig

    def get_scripts_git_sha(self):
        # get git sha
        process = subprocess.Popen(
            ["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE)
        (commit_hash, err) = process.communicate()
        exit_code = process.wait()
        self.logger.info(
            "get_scripts_get_sha exit_code: {exit_code}".format(
                exit_code=exit_code))
        scripts_git_sha = commit_hash.decode('utf-8', 'ignore')
        scripts_git_sha = scripts_git_sha.replace('\n', '')
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
        # curl --user "lanforge:lanforge" -H 'Accept: application/json'
        # http://192.168.100.116:8080/radiostatus/all | json_pp  , where --user
        # "USERNAME:PASSWORD"
        request_command = 'http://{lfmgr}:{port}/radiostatus/all'.format(
            lfmgr=self.lf_mgr_ip, port=self.lf_mgr_port)
        request = requests.get(
            request_command, auth=(
                self.lf_mgr_user, self.lf_mgr_pass))
        self.logger.info(
            "radio request command: {request_command}".format(
                request_command=request_command))
        self.logger.info(
            "radio request status_code {status}".format(
                status=request.status_code))
        lanforge_radio_json = request.json()
        self.logger.info("radio request.json: {json}".format(json=lanforge_radio_json))
        lanforge_radio_text = request.text
        self.logger.info("radio request.test: {text}".format(text=lanforge_radio_text))
        return lanforge_radio_json, lanforge_radio_text

    def get_lanforge_system_node_version(self):
        # creating shh client object we use this object to connect to router
        ssh = paramiko.SSHClient()
        # automatically adds the missing host key
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.lf_mgr_ip, port=self.lf_mgr_ssh_port, username=self.lf_mgr_user, password=self.lf_mgr_pass,
                    allow_agent=False, look_for_keys=False, banner_timeout=600)
        stdin, stdout, stderr = ssh.exec_command('uname -n')
        self.lanforge_system_node_version = stdout.readlines()
        self.lanforge_system_node_version = [line.replace(
            '\n', '') for line in self.lanforge_system_node_version]
        ssh.close()
        time.sleep(1)
        return self.lanforge_system_node_version

    def get_lanforge_fedora_version(self):
        # creating shh client object we use this object to connect to router
        ssh = paramiko.SSHClient()
        # automatically adds the missing host key
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.lf_mgr_ip, port=self.lf_mgr_ssh_port, username=self.lf_mgr_user, password=self.lf_mgr_pass,
                    allow_agent=False, look_for_keys=False, banner_timeout=600)
        stdin, stdout, stderr = ssh.exec_command('cat /etc/fedora-release')
        self.lanforge_fedora_version = stdout.readlines()
        self.lanforge_fedora_version = [line.replace(
            '\n', '') for line in self.lanforge_fedora_version]
        ssh.close()
        time.sleep(1)
        return self.lanforge_fedora_version

    def get_lanforge_kernel_version(self):
        # creating shh client object we use this object to connect to router
        ssh = paramiko.SSHClient()
        # automatically adds the missing host key
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.lf_mgr_ip, port=self.lf_mgr_ssh_port, username=self.lf_mgr_user, password=self.lf_mgr_pass,
                    allow_agent=False, look_for_keys=False, banner_timeout=600)
        stdin, stdout, stderr = ssh.exec_command('uname -r')
        self.lanforge_kernel_version = stdout.readlines()
        self.lanforge_kernel_version = [line.replace(
            '\n', '') for line in self.lanforge_kernel_version]
        ssh.close()
        time.sleep(1)
        return self.lanforge_kernel_version

    def get_lanforge_server_version(self):
        # creating shh client object we use this object to connect to router
        ssh = paramiko.SSHClient()
        # automatically adds the missing host key
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.lf_mgr_ip, port=self.lf_mgr_ssh_port, username=self.lf_mgr_user, password=self.lf_mgr_pass,
                    allow_agent=False, look_for_keys=False, banner_timeout=600)
        stdin, stdout, stderr = ssh.exec_command(
            './btserver --version | grep  Version')
        self.lanforge_server_version_full = stdout.readlines()
        self.lanforge_server_version_full = [line.replace(
            '\n', '') for line in self.lanforge_server_version_full]
        self.logger.info("lanforge_server_version_full: {lanforge_server_version_full}".format(
            lanforge_server_version_full=self.lanforge_server_version_full))
        self.lanforge_server_version = self.lanforge_server_version_full[0].split(
            'Version:', maxsplit=1)[-1].split(maxsplit=1)[0]
        self.lanforge_server_version = self.lanforge_server_version.strip()
        self.logger.info("lanforge_server_version: {lanforge_server_version}".format(
            lanforge_server_version=self.lanforge_server_version))
        ssh.close()
        time.sleep(1)
        return self.lanforge_server_version_full

    def get_lanforge_gui_version(self):
        # creating shh client object we use this object to connect to router
        ssh = paramiko.SSHClient()
        # automatically adds the missing host key
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.lf_mgr_ip, port=self.lf_mgr_ssh_port, username=self.lf_mgr_user, password=self.lf_mgr_pass,
                    allow_agent=False, look_for_keys=False, banner_timeout=600)
        stdin, stdout, stderr = ssh.exec_command(
            'curl -H "Accept: application/json" http://{lanforge_ip}:8080 | json_pp  | grep -A 7 "VersionInfo"'.format(lanforge_ip=self.lf_mgr_ip))
        self.lanforge_gui_version_full = stdout.readlines()
        # self.logger.info("lanforge_gui_version_full pre: {lanforge_gui_version_full}".format(lanforge_gui_version_full=self.lanforge_gui_version_full))
        self.lanforge_gui_version_full = [line.replace(
            '\n', '') for line in self.lanforge_gui_version_full]
        # self.logger.info("lanforge_gui_version_full: {lanforge_gui_version_full}".format(lanforge_gui_version_full=self.lanforge_gui_version_full))
        for element in self.lanforge_gui_version_full:
            if "BuildVersion" in element:
                ver_str = str(element)
                self.lanforge_gui_version = ver_str.split(
                    ':', maxsplit=1)[-1].replace(',', '')
                self.lanforge_gui_version = self.lanforge_gui_version.strip().replace('"', '')
                self.logger.info("BuildVersion {}".format(self.lanforge_gui_version))
            if "BuildDate" in element:
                gui_str = str(element)
                self.lanforge_gui_build_date = gui_str.split(
                    ':', maxsplit=1)[-1].replace(',', '')
                self.logger.info("BuildDate {}".format(self.lanforge_gui_build_date))
            if "GitVersion" in element:
                git_sha_str = str(element)
                self.lanforge_gui_git_sha = git_sha_str.split(
                    ':', maxsplit=1)[-1].replace(',', '')
                self.logger.info("GitVersion {}".format(self.lanforge_gui_git_sha))

        ssh.close()
        time.sleep(1)
        return self.lanforge_gui_version_full, self.lanforge_gui_version, self.lanforge_gui_build_date, self.lanforge_gui_git_sha

    def send_results_email(self, report_file=None):
        if (report_file is None):
            self.logger.info("No report file, not sending email.")
            return
        report_url = report_file.replace('/home/lanforge/', '')
        if report_url.startswith('/'):
            report_url = report_url[1:]
        qa_url = self.qa_report_html.replace('/home/lanforge', '')
        if qa_url.startswith('/'):
            qa_url = qa_url[1:]
        # following recommendation
        # NOTE: https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-from-nic-in-python
        # Mail
        # command to check if mail running : systemctl status postfix
        # command = 'echo "$HOSTNAME mail system works!" | mail -s "Test: $HOSTNAME $(date)" chuck.rekiere@candelatech.com'
        self.hostname = socket.getfqdn()
        ip = socket.gethostbyname(self.hostname)

        # a hostname lacking dots by definition lacks a domain name
        # this is not useful for hyperlinks outside the known domain, so an IP
        # address should be preferred
        if self.hostname.find('.') < 1:
            self.hostname = ip

        message_txt = ""
        if (self.email_txt != ""):
            message_txt = """{email_txt} lanforge target {lf_mgr_ip}
Results from {hostname}:
Suite: {suite}
Database: {db}

lf_check Test Suite Report:
http://{hostname}/{report}

""".format(email_txt=self.email_txt, lf_mgr_ip=self.lf_mgr_ip, suite=self.test_suite, db=self.database_sqlite, hostname=self.hostname, report=report_url)


        else:
            message_txt = """Results from {hostname}:
Suite: {suite}
Database: {db}

lf_check Test Suite Report:
http://{hostname}/{report}

""".format(hostname=self.hostname, suite=self.test_suite, db=self.database_sqlite, report=report_url)

        # Put in report information current two methods supported,
        if "NA" not in self.qa_report_html:
            message_txt += """
            
QA Report Dashboard:
http://{ip_qa}/{qa_url}


NOTE: Diagrams are links in dashboard""".format(ip_qa=ip, qa_url=qa_url, qa_url_local=qa_url)

        else:
            message_txt += """
QA Report Dashboard: lf_qa.py was not run as last script of test suite"""

        if (self.email_title_txt != ""):
            mail_subject = "{email} [{hostname}] {suite} {db} {date}".format(email=self.email_title_txt, hostname=self.hostname,
                                                                             suite=self.test_suite, db=self.database_sqlite, date=datetime.datetime.now())
        else:
            mail_subject = "Regression Test [{hostname}] {suite} {db} {date}".format(hostname=self.hostname,
                                                                                     suite=self.test_suite, db=self.database_sqlite, date=datetime.datetime.now())
        try:
            if self.production_run:
                msg = message_txt.format(ip=ip)
                # for postfix from command line  echo "My message" | mail -s
                # subject user@candelatech.com
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

            self.logger.info("running:[{}]".format(command))
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True)
            # have email on separate timeout
            process.wait(timeout=int(self.test_timeout))
        except subprocess.TimeoutExpired:
            self.logger.info("send email timed out")
            process.terminate()

    def start_csv_results(self):
        self.logger.info("self.csv_results")
        self.csv_results_file = open(self.csv_results, "w")
        self.csv_results_writer = csv.writer(
            self.csv_results_file, delimiter=",")
        self.csv_results_column_headers = [
            'Test', 'Command', 'Result', 'STDOUT', 'STDERR']
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

    # Reading the test rig configuration
    def read_json_rig(self):
        # self.logger.info("read_config_json_contents {}".format(self.json_rig))
        if "test_rig_parameters" in self.json_rig:
            self.logger.info("json: read test_rig_parameters")
            # self.logger.info("test_rig_parameters {}".format(self.json_rig["test_rig_parameters"]))
            self.read_test_rig_parameters()
        else:
            self.logger.info(
                "EXITING test_rig_parameters not in json {}".format(
                    self.json_rig))
            self.logger.info(
                "EXITING ERROR test_rig_parameters not in rig json")
            exit(1)

    # read dut configuration
    def read_json_dut(self):
        if "test_dut" in self.json_dut:
            self.logger.info("json: read test_dut")
            self.read_dut_parameters()
        else:
            self.logger.info(
                "EXITING test_dut not in json {}".format(
                    self.json_dut))
            self.logger.info("EXITING ERROR test_dut not in dut json {}")
            exit(1)

    # Top Level for reading the tests to run
    def read_json_test(self):
        if "test_suites" in self.json_test:
            self.logger.info(
                "json: read test_suites looking for: {}".format(
                    self.test_suite))
            # self.logger.info("test_suites {}".format(self.json_test["test_suites"]))
            if self.test_suite in self.json_test["test_suites"]:
                self.test_dict = self.json_test["test_suites"][self.test_suite]
                self.test_dict_original_json = self.json_test["test_suites"][self.test_suite]
                # self.logger.info("self.test_dict {}".format(self.test_dict))
            else:
                self.logger.info(
                    "EXITING test_suite {} Not Present in json test_suites: {}".format(
                        self.test_suite, self.json_test["test_suites"]))
                self.logger.info(
                    "EXITING ERROR test_suite {} Not Present in json test_suites".format(
                        self.test_suite))
                exit(1)
        else:
            self.logger.info(
                "EXITING test_suites not in json {}".format(
                    self.json_test))
            self.logger.info("EXITING ERROR test_suites not in json test")
            exit(1)

    def read_test_rig_parameters(self):
        if "TEST_RIG" in self.json_rig["test_rig_parameters"]:
            self.test_rig = self.json_rig["test_rig_parameters"]["TEST_RIG"]
        else:
            self.logger.info("test_rig not in test_rig_parameters json")

        if self.server_override is None:
            if "TEST_SERVER" in self.json_rig["test_rig_parameters"]:
                self.test_server = self.json_rig["test_rig_parameters"]["TEST_SERVER"]
            else:
                self.logger.info(
                    "TEST_SERVER not in test_rig_parameters json")
        else:
            self.test_server = self.server_override

        if self.db_override is None:
            if "DATABASE_SQLITE" in self.json_rig["test_rig_parameters"]:
                self.database_sqlite = self.json_rig["test_rig_parameters"]["DATABASE_SQLITE"]
            else:
                self.logger.info(
                    "DATABASE_SQLITE not in test_rig_parameters json")
        else:
            self.database_sqlite = self.db_override
        if "LF_MGR_IP" in self.json_rig["test_rig_parameters"]:
            self.lf_mgr_ip = self.json_rig["test_rig_parameters"]["LF_MGR_IP"]
        else:
            self.logger.info("lf_mgr_ip not in test_rig_parameters json")
        if "LF_MGR_PORT" in self.json_rig["test_rig_parameters"]:
            self.lf_mgr_port = self.json_rig["test_rig_parameters"]["LF_MGR_PORT"]
        else:
            self.logger.info("LF_MGR_PORT not in test_rig_parameters json")
        if "LF_MGR_USER" in self.json_rig["test_rig_parameters"]:
            self.lf_mgr_user = self.json_rig["test_rig_parameters"]["LF_MGR_USER"]
        else:
            self.logger.info("LF_MGR_USER not in test_rig_parameters json")
        if "LF_MGR_PASS" in self.json_rig["test_rig_parameters"]:
            self.lf_mgr_pass = self.json_rig["test_rig_parameters"]["LF_MGR_PASS"]
        else:
            self.logger.info("LF_MGR_PASS not in test_rig_parameters json")
        if "UPSTREAM_PORT" in self.json_rig["test_rig_parameters"]:
            self.upstream_port = self.json_rig["test_rig_parameters"]["UPSTREAM_PORT"]
        else:
            self.logger.info("UPSTREAM_PORT not in test_rig_parameters json")
        if "UPSTREAM_ALIAS" in self.json_rig["test_rig_parameters"]:
            self.upstream_alias = self.json_rig["test_rig_parameters"]["UPSTREAM_ALIAS"]
        else:
            self.logger.info("UPSTREAM_ALIAS not in test_rig_parameters json")
        if "TEST_TIMEOUT" in self.json_rig["test_rig_parameters"]:
            self.test_timeout = self.json_rig["test_rig_parameters"]["TEST_TIMEOUT"]
            self.test_timeout_default = self.test_timeout
        else:
            self.logger.info("TEST_TIMEOUT not in test_rig_parameters json")
            exit(1)
        # EMAIL is optional
        if "EMAIL_LIST_PRODUCTION" in self.json_rig["test_rig_parameters"]:
            self.email_list_production = self.json_rig["test_rig_parameters"]["EMAIL_LIST_PRODUCTION"]
        else:
            self.logger.info(
                "EMAIL_LIST_PRODUCTION not in test_rig_parameters json")
        if "EMAIL_LIST_TEST" in self.json_rig["test_rig_parameters"]:
            self.email_list_test = self.json_rig["test_rig_parameters"]["EMAIL_LIST_TEST"]
            self.logger.info(self.email_list_test)
        else:
            self.logger.info("EMAIL_LIST_TEST not in test_rig_parameters json")
        if "EMAIL_TITLE_TXT" in self.json_rig["test_rig_parameters"]:
            self.email_title_txt = self.json_rig["test_rig_parameters"]["EMAIL_TITLE_TXT"]
        else:
            self.logger.info("EMAIL_TITLE_TXT not in test_rig_parameters json")
        if "EMAIL_TXT" in self.json_rig["test_rig_parameters"]:
            self.email_txt = self.json_rig["test_rig_parameters"]["EMAIL_TXT"]
        else:
            self.logger.info("EMAIL_TXT not in test_rig_parameters json")

        # dut_set_name selectes the DUT to test against , it is different then use_dut_name
        # this value gets set in the test
    def read_dut_parameters(self):
        if "DUT_SET_NAME" in self.json_dut["test_dut"]:
            self.dut_set_name = self.json_dut["test_dut"]["DUT_SET_NAME"]
        else:
            self.logger.info("DUT_SET_NAME not in test_dut json")
        # dut name will set a chamberview scenerio for a DUT which can be
        # selected with dut_set_name
        if "USE_DUT_NAME" in self.json_dut["test_dut"]:
            self.use_dut_name = self.json_dut["test_dut"]["USE_DUT_NAME"]
        else:
            self.logger.info("USE_DUT_NAME not in test_dut json")

        if "DUT_HW" in self.json_dut["test_dut"]:
            self.dut_hw = self.json_dut["test_dut"]["DUT_HW"]
        else:
            self.logger.info("DUT_HW not in test_dut json")

        if "DUT_SW" in self.json_dut["test_dut"]:
            self.dut_sw = self.json_dut["test_dut"]["DUT_SW"]
        else:
            self.logger.info("DUT_SW not in test_dut json")

        if "DUT_MODEL" in self.json_dut["test_dut"]:
            self.dut_model = self.json_dut["test_dut"]["DUT_MODEL"]
        else:
            self.logger.info("DUT_MODEL not in test_dut json")

        if "DUT_SN" in self.json_dut["test_dut"]:
            self.dut_serial = self.json_dut["test_dut"]["DUT_SN"]
        else:
            self.logger.info("DUT_SERIAL not in test_dut json")

        if "wireless_network_dict" in self.json_dut["test_dut"]:
            self.wireless_network_dict = self.json_dut["test_dut"]["wireless_network_dict"]
            self.logger.info(
                "self.wireless_network_dict {}".format(
                    self.wireless_network_dict))
        else:
            self.logger.info("wireless_network_dict not in test_dut json")
            exit(1)

    # custom will accept --load FACTORY_DFLT and --load BLANK
    # TODO make a list
    def load_custom_database(self, custom_db):
        try:
            os.chdir(self.scripts_wd)
        except BaseException:
            self.logger.info("failed to change to {}".format(self.scripts_wd))

        # WARNING do not simplify the following constructed command
        # command = "./{} {} {} {}".format("scenario.py", "--mgr {mgr}"\
        #    .format(mgr=self.lf_mgr_ip),"--load {db}".format(db=custom_db),"--action {action}".format(action="overwrite"))
        command = "./{cmd} --mgr {mgr} --load {db} --action {action}".format(
            cmd="scenario.py", mgr=self.lf_mgr_ip, db=custom_db, action="overwrite")
        self.logger.info("command: {command}".format(command=command))

        process = subprocess.Popen((command).split(' '), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)
        # wait for the process to terminate
        out, err = process.communicate()
        errcode = process.returncode
        self.logger.info(
            "load_custom_database out: {out}  errcode: {errcode} err: {err}".format(
                out=out,
                errcode=errcode,
                err=err))
        # DO NOT REMOVE 15 second sleep.
        # After every DB load, the load changes are applied, and part of the apply is to re-build
        # The underlying netsmith objects
        sleep(15)

    def run_script(self):
        # The network arguments need to be changed when in a list
        for index, args_list_element in enumerate(
                self.test_dict[self.test]['args_list']):

            # Note the elements used by ssid_idx need to be on same line in json
            if 'ssid_idx=' in args_list_element:
                # self.logger.info("args_list_element {}".format(args_list_element))
                # get ssid_idx used in the test as an index for the
                # dictionary
                ssid_idx_number = args_list_element.split(
                    'ssid_idx=')[-1].split()[0]
                self.logger.info("ssid_idx_number: {}".format(ssid_idx_number))
                # index into the DUT network index
                idx = "ssid_idx={}".format(ssid_idx_number)
                self.logger.info("idx: {}".format(idx))
                if 'SSID_USED' in args_list_element:
                    self.test_dict[self.test]['args_list'][index] = self.test_dict[self.test]['args_list'][index].replace(
                        'SSID_USED', self.wireless_network_dict[idx]['SSID_USED'])
                if 'SECURITY_USED' in args_list_element:
                    self.test_dict[self.test]['args_list'][index] = self.test_dict[self.test]['args_list'][index].replace(
                        'SECURITY_USED', self.wireless_network_dict[idx]['SECURITY_USED'])
                if 'SSID_PW_USED' in args_list_element:
                    self.test_dict[self.test]['args_list'][index] = self.test_dict[self.test]['args_list'][index].replace(
                        'SSID_PW_USED', self.wireless_network_dict[idx]['SSID_PW_USED'])
                if 'BSSID_TO_USE' in args_list_element:
                    self.test_dict[self.test]['args_list'][index] = self.test_dict[self.test]['args_list'][index].replace(
                        'BSSID_TO_USE', self.wireless_network_dict[idx]['BSSID_TO_USE'])
                if 'WLAN_ID_USED' in args_list_element:
                    self.test_dict[self.test]['args_list'][index] = self.test_dict[self.test]['args_list'][index].replace(
                        'WLAN_ID_USED', self.wireless_network_dict[idx]['WLAN_ID_USED'])

                # use_ssid_idx is ephemeral and used only for
                # variable replacement , remove
                tmp_idx = "use_ssid_idx={}".format(ssid_idx_number)
                if tmp_idx in args_list_element:
                    self.test_dict[self.test]['args_list'][index] = self.test_dict[self.test]['args_list'][index].replace(
                        tmp_idx, '')
                # leave in for checking the command line arguments
                self.logger.info(
                    "self.test_dict[self.test]['args_list']: {}".format(
                        self.test_dict[self.test]['args_list']))
        # Walk all the args in the args list then construct the arguments

        # since there may be multiple iterations or batches need original json syntax for replacements
        self.test_dict[self.test]['args'] = self.test_dict_original_json[self.test]['args'].replace(self.test_dict[self.test]['args'],
                                                                                                    ''.join(self.test_dict[self.test][
                                                                                                        'args_list']))
        if 'DATABASE_SQLITE' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'DATABASE_SQLITE', self.database_sqlite)
        if 'HTTP_TEST_IP' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'HTTP_TEST_IP', self.http_test_ip)
        if 'FTP_TEST_IP' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'FTP_TEST_IP', self.ftp_test_ip)
        if 'TEST_IP' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'TEST_IP', self.test_ip)
        if 'LF_MGR_USER' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'LF_MGR_USER', self.lf_mgr_user)
        if 'LF_MGR_PASS' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'LF_MGR_PASS', self.lf_mgr_pass)
        if 'LF_MGR_IP' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'LF_MGR_IP', self.lf_mgr_ip)
        if 'LF_MGR_PORT' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'LF_MGR_PORT', self.lf_mgr_port)
        # DUT Configuration
        if 'USE_DUT_NAME' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'USE_DUT_NAME', self.use_dut_name)
        if 'DUT_HW' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'DUT_HW', self.dut_hw)
        if 'DUT_SW' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'DUT_SW', self.dut_sw)
        if 'DUT_MODEL' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'DUT_MODEL', self.dut_model)
        if 'DUT_SN' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'DUT_SN', self.dut_serial)
        if 'UPSTREAM_PORT' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace('UPSTREAM_PORT', self.upstream_port)
        if 'UPSTREAM_ALIAS' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace('UPSTREAM_ALIAS', self.upstream_alias)
        # lf_dataplane_test.py and lf_wifi_capacity_test.py use a parameter --local_path for the location
        # of the reports when the reports are pulled.
        if 'REPORT_PATH' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'REPORT_PATH', self.report_path)
        if 'TEST_SERVER' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'TEST_SERVER', self.test_server)
        if 'DUT_SET_NAME' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace('DUT_SET_NAME',
                                                                                          self.dut_set_name)
        if 'TEST_RIG' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'TEST_RIG', self.test_rig)

        # batch parameters in the script
        if 'USE_BATCH_CHANNEL' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'USE_BATCH_CHANNEL', self.channel)

        if 'USE_BATCH_NSS' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'USE_BATCH_NSS', self.nss)

        if 'USE_BATCH_BANDWIDTH' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'USE_BATCH_BANDWIDTH', self.bandwidth)

        if 'USE_BATCH_TX_POWER' in self.test_dict[self.test]['args']:
            self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(
                'USE_BATCH_TX_POWER', self.tx_power)

        self.logger.info("self.test_dict[self.test]['args']: {}".format(self.test_dict[self.test]['args']))

        # END of command line arg processing
        # if self.test_dict[self.test]['args'] == "":
        #     self.test_dict[self.test]['args'] = self.test_dict[self.test]['args'].replace(self.test_dict[self.test]['args'],
        #                                                                                  ''.join(self.test_dict[self.test][
        #                                                                                      'args_list']))
        if 'timeout' in self.test_dict[self.test]:
            self.logger.info(
                "timeout : {}".format(
                    self.test_dict[self.test]['timeout']))
            self.test_timeout = int(
                self.test_dict[self.test]['timeout'])
        else:
            self.test_timeout = self.test_timeout_default
        if 'load_db' in self.test_dict[self.test]:
            self.logger.info(
                "load_db : {}".format(
                    self.test_dict[self.test]['load_db']))
            if str(self.test_dict[self.test]['load_db']).lower() != "none" and str(
                    self.test_dict[self.test]['load_db']).lower() != "skip":
                try:
                    self.load_custom_database(
                        self.test_dict[self.test]['load_db'])
                except BaseException:
                    self.logger.info("custom database failed to load check existance and location: {}".format(
                        self.test_dict[self.test]['load_db']))
        try:
            os.chdir(self.scripts_wd)
            self.logger.info("Current Working Directory {}".format(os.getcwd()))

        except BaseException:
            self.logger.info(
                "failed to change to {}".format(
                    self.scripts_wd))
        cmd_args = "{}".format(self.test_dict[self.test]['args'])
        # TODO the the tx_power went back in the command
        command = "./{} {}".format(
            self.test_dict[self.test]['command'], cmd_args)
        self.logger.info("command: {}".format(command))
        self.logger.info("cmd_args {}".format(cmd_args))

        # TODO this code is always run since there is a default
        # TODO change name to file obj to make more understandable
        if self.outfile_name is not None:
            stdout_log_txt = os.path.join(
                self.log_path, "{}-{}-stdout.txt".format(self.outfile_name, self.test))
            self.logger.info(
                "stdout_log_txt: {}".format(stdout_log_txt))
            stdout_log = open(stdout_log_txt, 'a')
            stderr_log_txt = os.path.join(
                self.log_path, "{}-{}-stderr.txt".format(self.outfile_name, self.test))
            self.logger.info(
                "stderr_log_txt: {}".format(stderr_log_txt))
            # stderr_log = open(stderr_log_txt, 'a')
        # need to take into account --raw_line parameters thus need to use shlex.split
        # need to preserve command to have correct command syntax
        # in command output
        # TODO this is where the batch  needs to itterate
        command_to_run = command
        self.logger.info("command : {command}".format(command=command))
        command_to_run = shlex.split(command_to_run)

        self.logger.info(
            "running {command_to_run}".format(
                command_to_run=command_to_run))
        self.test_start_time = str(datetime.datetime.now().strftime(
            "%Y-%m-%d-%H-%M-%S")).replace(':', '-')
        self.logger.info(
            "Test start: {time} Timeout: {timeout}".format(
                time=self.test_start_time, timeout=self.test_timeout))
        start_time = datetime.datetime.now()
        summary_output = ''
        # have stderr go to stdout
        try:
            summary = subprocess.Popen(command_to_run, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       universal_newlines=True)
        # TODO the looks one directory higher,  there needs to be a way to execute from higher directory.
        except FileNotFoundError:
            # TODO tx_power is one directory up from py-scripts
            self.logger.info("FileNotFoundError will try to execute from lanforge Top directory")
            os.chdir(self.lanforge_wd)
            self.logger.info("Changed Current Working Directory to {}".format(os.getcwd()))
            summary = subprocess.Popen(command_to_run, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       universal_newlines=True)

        except PermissionError:
            self.logger.info("PermissionError on execution of {command}".format(command=command_to_run))

        except IsADirectoryError:
            self.logger.info("IsADirectoryError on execution of {command}".format(command=command_to_run))

        # This code will read the output as the script is running and log 
        for line in iter(summary.stdout.readline, ''):
            self.logger.info(line)
            summary_output += line
        try:
            if int(self.test_timeout != 0):
                summary.wait(timeout=int(self.test_timeout))
            else:
                summary.wait()
        except TimeoutExpired:
            summary.terminate
            self.test_result = "TIMEOUT"
        # TODO will change back to the scripts_wd since a script like tx_power.py will run in the parent directoy to
        # py-scripts
        os.chdir(self.scripts_wd)
        self.logger.info("Current Working Directory {}".format(os.getcwd()))

        # Since using "wait" above the return code will be set. 
        try:
            return_code = summary.returncode 
            if return_code == '0':
                self.logger.info("Script returned pass return code: {return_code} for test: {command}".format(return_code=return_code,command=command_to_run))
            else: 
                self.logger.info("Script returned non-zero return code: {return_code} for test: {command}".format(return_code=return_code,command=command_to_run))

        except BaseException as err:
            self.logger.info("issue reading return code err:{err}".format(err=err))

        self.logger.info(summary_output)
        stdout_log.write(summary_output)
        stdout_log.close()
        end_time = datetime.datetime.now()
        self.test_end_time = str(datetime.datetime.now().strftime(
            "%Y-%m-%d-%H-%M-%S")).replace(':', '-')
        self.logger.info(
            "Test end time {time}".format(
                time=self.test_end_time))
        time_delta = end_time - start_time
        minutes, seconds = divmod(time_delta.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        self.duration = "{day}d {hours}h {minutes}m {seconds}s {msec} ms".format(
            day=time_delta.days, hours=hours, minutes=minutes, seconds=seconds, msec=time_delta.microseconds)
        # If collect meta data is set
        meta_data_path = ""
        # Will gather data even on a TIMEOUT condition as there is
        # some results on longer tests
        # TODO use the summary
        stdout_log_size = os.path.getsize(stdout_log_txt)
        if stdout_log_size > 0:
            stdout_log_fd = open(stdout_log_txt)
            # "Report Location:::/home/lanforge/html-reports/wifi-capacity-2021-08-17-04-02-56"
            #
            for line in stdout_log_fd:
                if "Report Location" in line:
                    self.report_index += 1
                    if self.iteration == self.report_index:
                        meta_data_path = line.replace('"', '')
                        meta_data_path = meta_data_path.replace(
                            'Report Location:::', '')
                        meta_data_path = meta_data_path.split(
                            '/')[-1]
                        meta_data_path = meta_data_path.strip()
                        meta_data_path = self.report_path + '/' + meta_data_path + '/meta.txt'
                        break
            stdout_log_fd.close()
        if meta_data_path != "":
            try:
                meta_data_fd = open(meta_data_path, 'w+')
                meta_data_fd.write(
                    '$ Generated by Candela Technologies LANforge network testing tool\n')
                meta_data_fd.write(
                    "test_run {test_run}\n".format(
                        test_run=self.report_path))
                meta_data_fd.write(
                    "file_meta {path}\n".format(
                        path=meta_data_path))
                meta_data_fd.write(
                    'lanforge_gui_version: {gui_version} \n'.format(
                        gui_version=self.lanforge_gui_version))
                meta_data_fd.write(
                    'lanforge_server_version: {server_version} \n'.format(
                        server_version=self.lanforge_server_version))
                meta_data_fd.write('$ LANforge command\n')
                meta_data_fd.write(
                    "command {command}\n".format(
                        command=command))
                # split command at test-tag , at rest of string once at
                # the actual test-tag value
                test_tag = command.split(
                    'test_tag', maxsplit=1)[-1].split(maxsplit=1)[0]
                test_tag = test_tag.replace("'", "")
                meta_data_fd.write('$ LANforge test tag\n')
                meta_data_fd.write(
                    "test_tag {test_tag}\n".format(
                        test_tag=test_tag))
                # LANforge information is a list thus [0]
                meta_data_fd.write('$ LANforge Information\n')
                meta_data_fd.write(
                    "lanforge_system_node {lanforge_system_node}\n".format(
                        lanforge_system_node=self.lanforge_system_node_version[0]))
                meta_data_fd.write(
                    "lanforge_kernel_version {lanforge_kernel_version}\n".format(
                        lanforge_kernel_version=self.lanforge_kernel_version[0]))
                meta_data_fd.write(
                    "lanforge_fedora_version {lanforge_fedora_version}\n".format(
                        lanforge_fedora_version=self.lanforge_fedora_version[0]))
                meta_data_fd.write(
                    "lanforge_gui_version_full {lanforge_gui_version_full}\n".format(
                        lanforge_gui_version_full=self.lanforge_gui_version_full))
                meta_data_fd.write(
                    "lanforge_server_version_full {lanforge_server_version_full}\n".format(
                        lanforge_server_version_full=self.lanforge_server_version_full[0]))
                meta_data_fd.close()
            except ValueError as err:
                self.logger.critical("unable to write meta {meta_data_path} : {msg})".format(meta_data_path=meta_data_path, msg=err))
            except BaseException as err:
                self.logger.critical("BaseException unable to write meta {meta_data_path} : {msg}".format(meta_data_path=meta_data_path, msg=err))

        # Code for checking if the script passed or failed much of the 
        # code is checking the output.
        # Timeout needs to be reported and not overwriten
        if self.test_result == "TIMEOUT":
            self.logger.info(
                "TIMEOUT FAILURE,  Check LANforge Radios")
            self.test_result = "Time Out"
            background = self.background_purple
        elif return_code == 1:
            self.logger.error("Test returne fail  return code {return_code} for test: {command}".format(return_code=return_code,command=command_to_run))
            self.test_result = "Script retured Fail"
            background = self.background_red
        elif return_code == 2:
            self.logger.error("Incorrect args:  return code {return_code} for test: {command}".format(return_code=return_code,command=command_to_run))
            self.test_result = "Incorrect args"
            background = self.background_orange
        elif return_code != 0:
            self.logger.error("None zero return code:  return code {return_code} for test: {command}".format(return_code=return_code,command=command_to_run))
            self.test_result = "return code {return_code}".format(return_code=return_code)
            background = self.background_orange
        else:
            # TODO use summary returned from subprocess
            if stdout_log_size > 0:
                text = open(stdout_log_txt).read()
                # for 5.4.3 only TestTag was not present
                if 'ERROR:  Could not find component: TestTag' in text:
                    self.test_result = "Success"
                    background = self.background_green
                # probe command for test_ip_variable_time.py has
                # the word alloc error and erros in it
                elif 'alloc error' in text:
                    self.test_result = "Success"
                    background = self.background_green
                # leave the space in after error to not pick up tx
                # errors or rx errors
                elif 'ERROR: ' in text:
                    # TODO check for return code from script
                    if 'New and Old channel width are same' in text:
                        self.test_result = "Success"
                        background = self.background_green
                    else:
                        self.test_result = "Some Tests Failed"
                        background = self.background_orange
                elif 'IndexError: list index out of range' in text:
                    self.test_result = "Test Errors"
                    background = self.background_red
                elif 'ERROR: FAILED ' in text:
                    self.test_result = "Some Tests Failed"
                    background = self.background_orange
                elif 'error ' in text.lower():
                    if 'passes: zero test results' in text:
                        self.test_result = "Success"
                        background = self.background_green
                    else:
                        self.test_result = "Test Errors"
                        background = self.background_red
                elif 'tests failed' in text.lower():
                    self.test_result = "Some Tests Failed"
                    background = self.background_orange
                else:
                    self.test_result = "Success"
                    background = self.background_green
            else:
                # if stdout empty that is a failure also
                self.test_result = "Failure"
                background = self.background_red
        # Total up test, tests success, tests failure, tests
        # timeouts
        self.tests_run += 1
        if self.test_result == "Success":
            self.tests_success += 1
        elif self.test_result == "Failure":
            self.tests_failure += 1
        elif self.test_result == "Some Tests Failed":
            self.tests_some_failure += 1
        elif self.test_result == "Test Errors":
            self.tests_failure += 1
        elif self.test_result == "Incorrect args":
            self.tests_failure += 1
        elif "return code" in self.test_result: 
            self.tests_failure += 1
        elif self.test_result == "TIMEOUT":
            self.tests_timeout += 1
        if 'lf_qa' in command:
            line_list = open(stdout_log_txt).readlines()
            for line in line_list:
                if 'html report:' in line:
                    self.qa_report_html = line
                    self.logger.info(
                        "html_report: {report}".format(
                            report=self.qa_report_html))
                    break
            self.qa_report_html = self.qa_report_html.replace(
                'html report: ', '')
        # stdout_log_link is used for the email reporting to have
        # the corrected path
        abs_path = False
        if abs_path:
            stdout_log_link = str(stdout_log_txt).replace(
                '/home/lanforge', '')
            stderr_log_link = str(stderr_log_txt).replace(
                '/home/lanforge', '')
        # use relative path for reporting
        else:
            stdout_log_basename =  os.path.basename(stdout_log_txt)
            stdout_log_parent_path = os.path.dirname(stdout_log_txt)
            stdout_log_parent_basename = os.path.basename(stdout_log_parent_path)
            stdout_log_link = "./" + stdout_log_parent_basename + "/" + stdout_log_basename

            stderr_log_basename =  os.path.basename(stderr_log_txt)
            stderr_log_parent_path = os.path.dirname(stderr_log_txt)
            stderr_log_parent_basename = os.path.basename(stderr_log_parent_path)
            stderr_log_link = "./" + stderr_log_parent_basename + "/" + stderr_log_basename
                        
        if command.find(' ') > 1:
            short_cmd = command[0:command.find(' ')]
        else:
            short_cmd = command
        self.html_results += """
        <tr><td>""" + str(self.test) + """</td>
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
        # TODO - place copy button at end and selectable , so
        # individual sections may be copied
        if command != short_cmd:
            # Hover and copy button snows up
            self.html_results += f"""<tr><td colspan='8' class='scriptdetails'>
                <span class='copybtn'>Copy</span>
                 <tt onclick='copyTextToClipboard(this)'>{command}</tt>
                 </td></tr>
                 """.format(command=command)
            # TODO - place a point button for not have the copy
            # hover, no copy button
            '''self.html_results += f"""<tr><td colspan='8' class='scriptdetails'>
                 <tt onclick='copyTextToClipboard(this)'>{command}</tt>
                 </td></tr>
                 """.format(command=command)
            '''
            # nocopy - example
            '''
            self.html_results += f"""<tr><td colspan='8' class='scriptdetails'>
                 <tt>{command}</tt>
                 </td></tr>
                 """.format(command=command)
            '''
        row = [
            self.test,
            command,
            self.test_result,
            stdout_log_txt,
            stderr_log_txt]
        self.csv_results_writer.writerow(row)
        self.csv_results_file.flush()
        # self.logger.info("row: {}".format(row))
        self.logger.info("test: {} executed".format(self.test))

    # TODO the command needs to be updated for the batch iterations
    def run_script_test(self):
        self.start_html_results()
        self.start_csv_results()
        # Suite start time
        suite_start_time = datetime.datetime.now()
        self.suite_start_time = str(datetime.datetime.now().strftime(
            "%Y-%m-%d-%H-%M-%S")).replace(':', '-')
        self.logger.info("Suite Start Time {suite_time}".format(
            suite_time=self.suite_start_time))

        # Configure Tests
        for self.test in self.test_dict:

            if ((self.test_dict[self.test]['enabled'] == "TRUE" and self.use_test_list is False) or 
                (self.use_test_list is True and self.test in self.test_list)):
                        
                        
                # TODO Place test interations here
                if 'iterations' in self.test_dict[self.test]:
                    self.logger.info("iterations : {}".format(self.test_dict[self.test]['iterations']))
                    self.test_iterations = int(
                        self.test_dict[self.test]['iterations'])
                else:
                    self.test_iterations = self.test_iterations_default

                if 'batch_channel' in self.test_dict[self.test]:
                    self.logger.info("batch_channel : {batch_channel}".format(batch_channel=self.test_dict[self.test]['batch_channel']))
                    self.channel_list = self.test_dict[self.test]['batch_channel'].split()

                if 'batch_nss' in self.test_dict[self.test]:
                    self.logger.info("batch_nss : {batch_nss}".format(batch_nss=self.test_dict[self.test]['batch_nss']))
                    self.nss_list = self.test_dict[self.test]['batch_nss'].split()

                if 'batch_bandwidth' in self.test_dict[self.test]:
                    self.logger.info("batch_bandwidth : {batch_bandwidth}".format(batch_bandwidth=self.test_dict[self.test]['batch_bandwidth']))
                    self.bandwidth_list = self.test_dict[self.test]['batch_bandwidth'].split()

                if 'batch_tx_power' in self.test_dict[self.test]:
                    self.logger.info("batch_tx_power : {batch_tx_power}".format(batch_tx_power=self.test_dict[self.test]['batch_tx_power']))
                    self.tx_power_list = self.test_dict[self.test]['batch_tx_power'].split()

                # TODO have addional methods
                # in python an empty list returns false .
                # If channel_list and bandwidth_list are populated then
                if self.channel_list and self.nss_list and self.bandwidth_list and self.tx_power_list:
                    for self.channel in self.channel_list:
                        for self.nss in self.nss_list:
                            for self.bandwidth in self.bandwidth_list:
                                # tx_power is passed in as
                                for self.tx_power in self.tx_power_list:
                                    # log may contain multiple runs - this helps put the meta.txt
                                    # in right directory
                                    self.iteration = 0
                                    self.report_index = 0
                                    for self.iteration in range(self.test_iterations):
                                        self.iteration += 1
                                        # Runs the scripts
                                        self.run_script()
                    # once done clear out the lists
                    self.channel_list = []
                    self.nss_list = []
                    self.bandwidth_list = []
                    self.tx_power_list = []
                elif self.channel_list and self.nss_list and self.bandwidth_list and not self.tx_power_list:
                    for self.channel in self.channel_list:
                        for self.nss in self.nss_list:
                            for self.bandwidth in self.bandwidth_list:
                                # tx_power is passed in so run will contain all tx powers from command line
                                # log may contain multiple runs - this helps put the meta.txt
                                # in right directory
                                self.iteration = 0
                                self.report_index = 0
                                for self.iteration in range(self.test_iterations):
                                    self.iteration += 1
                                    # in batch mode need to set the VARIABLES back into the test
                                    # Runs the scripts
                                    self.run_script()
                    self.channel_list = []
                    self.nss_list = []
                    self.bandwidth_list = []
                    self.tx_power_list = []

                elif self.channel_list and self.nss_list and not self.bandwidth_list and not self.tx_power_list:
                    for self.channel in self.channel_list:
                        for self.nss in self.nss_list:
                            # use bandwidth tx_power is passed in from command line
                            # one run will contain all the bandwiths and tx_power settings
                            # log may contain multiple runs - this helps put the meta.txt
                            # in right directory
                            self.iteration = 0
                            self.report_index = 0
                            for self.iteration in range(self.test_iterations):
                                self.iteration += 1
                                # Runs the scripts
                                self.run_script()
                    self.channel_list = []
                    self.nss_list = []
                    self.bandwidth_list = []
                    self.tx_power_list = []
                else:

                    # log may contain multiple runs - this helps put the meta.txt
                    # in right directory
                    self.iteration = 0
                    self.report_index = 0
                    for self.iteration in range(self.test_iterations):
                        self.iteration += 1

                        # Runs the scripts
                        self.run_script()
            # Using use_test_list is True and test is not in test_list
            elif self.use_test_list is True and self.test not in self.test_list:
                self.logger.info("use_test_list set TRUE test: {test} not in {list} skipping".format(test=self.test,list=self.test_list))

            # Test disabled
            elif self.test_dict[self.test]['enabled'] == "FALSE":
                self.logger.info("test: {}  enabled set FALSE test skipped ".format(self.test))

            # enabled flag missing in json
            else:
                self.logger.warning(
                    "enable value {} for test: {} ".format(self.test_dict[self.test]['enabled'], self.test))

        suite_end_time = datetime.datetime.now()
        self.suite_end_time = str(datetime.datetime.now().strftime(
            "%Y-%m-%d-%H-%M-%S")).replace(':', '-')
        self.logger.info("Suite End Time: {suite_time}".format(
            suite_time=self.suite_end_time))
        suite_time_delta = suite_end_time - suite_start_time
        minutes, seconds = divmod(suite_time_delta.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        self.suite_duration = "{day}d {hours}h {minutes}m {seconds}s {msec} ms".format(
            day=suite_time_delta.days, hours=hours, minutes=minutes, seconds=seconds, msec=suite_time_delta.microseconds)
        self.logger.info("Suite Duration:  {suite_duration}".format(
            suite_duration=self.suite_duration))
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

    parser.add_argument(
        '--dir',
        help="--dir <results directory>",
        default="")
    parser.add_argument(
        '--path',
        help="--path <results path>",
        default="/home/lanforge/html-results")
    parser.add_argument(
        '--json_rig',
        help="--json_rig <rig json config> ",
        required=True)
    parser.add_argument(
        '--json_dut',
        help="--json_dut <dut json config> ",
        required=True)
    parser.add_argument(
        '--json_test',
        help="--json_test <test json config> ",
        required=True)
    parser.add_argument(
        '--suite',
        help="--suite <suite name> ",
        required=True)
    parser.add_argument(
        '--use_test_list',
        help='''
            --use_test_list will have lf_check.py look at the <tests list> passed in to run a subset of the tests in a suite
            for targeted testing.
        ''',
        action='store_true'
        )
    parser.add_argument(
        '--test_list',
        help='''
            --test_list <tests list>  pass in a comma separated list, this will allow another method so select,
            specific tests in a test list.
        ''',
        default=[]
        )
    parser.add_argument('--flat_dir', help="--flat_dir , will place the results in the top directory",action='store_true')
    parser.add_argument(
        '--server_override',
        help="--server_override http://<server ip>/  example: http://192.168.95.6/",
        default=None)
    parser.add_argument(
        '--db_override',
        help="--db_override <sqlite db>  override for json DATABASE_SQLITE''",
        default=None)
    parser.add_argument('--production', help="--production  stores true, sends email results to production email list",
                        action='store_true')
    parser.add_argument('--no_send_email', help="--no_send_email  stores true, to not send emails results to engineer or production email list", action='store_true')

    parser.add_argument('--outfile', help="--outfile <Output Generic Name>  used as base name for all files generated",
                        default="")
    parser.add_argument('--logfile', help="--logfile <logfile Name>  logging for output of lf_check.py script",
                        default="lf_check.log")
    parser.add_argument(
        '--update_latest',
        help="--update_latest  copy latest results to top dir",
        action='store_true')
    # logging configuration:
    parser.add_argument("--lf_logger_config_json",
                        help="--lf_logger_config_json <json file> , json configuration of logger")

    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()
    if args.lf_logger_config_json:
        # logger_config.lf_logger_config_json = "lf_logger_config.json"
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()

    # load test config file information either <config>.json
    json_rig = ""
    try:
        logger.info("reading json_rig: {rig}".format(rig=args.json_rig))
        with open(args.json_rig, 'r') as json_rig_config:
            json_rig = json.load(json_rig_config)
    except json.JSONDecodeError as err:
        logger.error("ERROR reading {json}, ERROR: {error} ".format(json=args.json_rig, error=err))
        exit(1)

    json_dut = ""
    try:
        logger.info("reading json_dut: {dut}".format(dut=args.json_dut))
        with open(args.json_dut, 'r') as json_dut_config:
            json_dut = json.load(json_dut_config)
    except json.JSONDecodeError as err:
        logger.error("ERROR reading {json}, ERROR: {error} ".format(json=args.json_dut, error=err))
        exit(1)

    json_test = ""
    try:
        logger.info("reading json_test:  {}".format(args.json_test))
        with open(args.json_test, 'r') as json_test_config:
            json_test = json.load(json_test_config)
    except json.JSONDecodeError as err:
        logger.error("ERROR reading {json}, ERROR: {error} ".format(json=args.json_test, error=err))
        exit(1)

    # Test-rig information information
    lanforge_system_node_version = 'NO_LF_NODE_VER'
    scripts_git_sha = 'NO_GIT_SHA'
    lanforge_fedora_version = 'NO_FEDORA_VER'
    lanforge_kernel_version = 'NO_KERNEL_VER'
    lanforge_server_version_full = 'NO_LF_SERVER_VER'

    # select test suite
    test_suite = args.suite
    if args.dir == "":
        __dir = "lf_check_{suite}".format(suite=test_suite)
    else:
        __dir = args.dir
    __path = args.path

    server_override = args.server_override
    db_override = args.db_override

    if args.production:
        production = True
        logger.info("Email to production list")
    else:
        production = False
        logger.info("Email to email list")

    # create report class for reporting
    report = lf_report.lf_report(_path=__path,
                                 _results_dir_name=__dir,
                                 _output_html="{dir}.html".format(dir=__dir),
                                 _output_pdf="{dir}.pdf".format(dir=__dir))

    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    csv_results = "{dir}-{outfile}-{current_time}.csv".format(dir=__dir, outfile=args.outfile, current_time=current_time)
    csv_results = report.file_add_path(csv_results)
    outfile_name = "{dir}-{outfile}-{current_time}".format(dir=__dir, outfile=args.outfile, current_time=current_time)
    outfile = report.file_add_path(outfile_name)
    if args.flat_dir:
        report_path = report.get_flat_dir_report_path()
    else:
        report_path = report.get_report_path()
       
    log_path = report.get_log_path()

    # Check if a test_list passed as the user would like to do a selected 
    # set of tests from the test list
    use_test_list = args.use_test_list
    test_list = args.test_list
    if use_test_list:
        # if the test_list is empty should probably exit?
        if test_list == []:
            use_test_list = False
            logger.warning("use_testlist set to True yet test list was empty")
        else:
            test_list = args.test_list.split(',')
            logger.info("use_testlist set True test list : {list}".format(list=test_list))

    # lf_check() class created
    check = lf_check(_json_rig=json_rig,
                     _json_dut=json_dut,
                     _json_test=json_test,
                     _test_suite=test_suite,
                     _use_test_list=use_test_list,
                     _test_list=test_list,
                     _server_override=server_override,
                     _db_override=db_override,
                     _production=production,
                     _csv_results=csv_results,
                     _outfile=outfile,
                     _outfile_name=outfile_name,
                     _report_path=report_path,
                     _log_path=log_path)

    # set up logging
    logfile = args.logfile[:-4]
    logger.info("logfile: {}".format(logfile))
    logfile = "{}-{}.log".format(logfile, current_time)
    logfile = report.file_add_path(logfile)
    logger.info("logfile {}".format(logfile))

    # read config and run tests
    check.read_json_rig()  # check.read_config
    check.read_json_dut()
    check.read_json_test()

    # get sha and lanforge information for results
    # Need to do this after reading the configuration
    try:
        scripts_git_sha = check.get_scripts_git_sha()
        logger.info("git_sha {sha}".format(sha=scripts_git_sha))
    except BaseException:
        logger.warning("WARNING: git_sha read exception unable to read")

    try:
        lanforge_system_node_version = check.get_lanforge_system_node_version()
        logger.info("lanforge_system_node_version {system_node_ver}".format(
            system_node_ver=lanforge_system_node_version))
    except BaseException:
        logger.warning("WARNING: lanforge_system_node_version exception")

    try:
        lanforge_fedora_version = check.get_lanforge_fedora_version()
        logger.info("lanforge_fedora_version {fedora_ver}".format(
            fedora_ver=lanforge_fedora_version))
    except BaseException:
        logger.error("ERROR: lanforge_fedora_version exception, tests aborted check lanforge ip")
        exit(1)

    try:
        lanforge_kernel_version = check.get_lanforge_kernel_version()
        logger.info("lanforge_kernel_version {kernel_ver}".format(
            kernel_ver=lanforge_kernel_version))
    except BaseException:
        logger.error("ERROR: lanforge_kernel_version exception, tests aborted check lanforge ip")
        exit(1)

    try:
        lanforge_server_version_full = check.get_lanforge_server_version()
        logger.info("lanforge_server_version_full {lanforge_server_version_full}".format(
            lanforge_server_version_full=lanforge_server_version_full))
    except BaseException:
        logger.error("ERROR: lanforge_server_version exception, tests aborted check lanforge ip")
        exit(1)

    try:
        lanforge_gui_version_full, lanforge_gui_version, lanforge_gui_build_date, lanforge_gui_git_sha = check.get_lanforge_gui_version()
        logger.info("lanforge_gui_version_full {lanforge_gui_version_full}".format(
            lanforge_gui_version_full=lanforge_gui_version_full))
    except BaseException:
        logger.error("ERROR: lanforge_gui_version exception, tests aborted check lanforge ip")
        exit(1)

    try:
        lanforge_radio_json, lanforge_radio_text = check.get_lanforge_radio_information()
        lanforge_radio_formatted_str = json.dumps(
            lanforge_radio_json, indent=2)
        logger.info("lanforge_radio_json: {lanforge_radio_json}".format(
            lanforge_radio_json=lanforge_radio_formatted_str))

        # note put into the meta data
        lf_radio_df = pd.DataFrame(
            columns=[
                'Radio',
                'WIFI-Radio Driver',
                'Radio Capabilities',
                'Firmware Version',
                'max_clients',
                'max_vap',
                'max_sta'])

        for key in lanforge_radio_json:
            if 'wiphy' in key:
                # self.logger.info("key {}".format(key))
                # self.logger.info("lanforge_radio_json[{}]: {}".format(key,lanforge_radio_json[key]))
                driver = lanforge_radio_json[key]['driver'].split(
                    'Driver:', maxsplit=1)[-1].split(maxsplit=1)[0]
                try:
                    firmware_version = lanforge_radio_json[key]['firmware version']
                except BaseException:
                    logger.info("5.4.3 radio fw version not in /radiostatus/all ")
                    firmware_version = "5.4.3 N/A"

                lf_radio_df = lf_radio_df.append(
                    {'Radio': lanforge_radio_json[key]['entity id'],
                     'WIFI-Radio Driver': driver,
                     'Radio Capabilities': lanforge_radio_json[key]['capabilities'],
                     'Firmware Version': firmware_version,
                     'max_sta': lanforge_radio_json[key]['max_sta'],
                     'max_vap': lanforge_radio_json[key]['max_vap'],
                     'max_vifs': lanforge_radio_json[key]['max_vifs']}, ignore_index=True)
        logger.info("lf_radio_df:: {lf_radio_df}".format(lf_radio_df=lf_radio_df))

    except Exception as error:
        logger.error("print_exc(): {error}".format(error=error))
        traceback.print_exc(file=sys.stdout)
        lf_radio_df = pd.DataFrame()
        logger.info("get_lanforge_radio_json exception, no radio data, check for LANforge GUI running")
        exit(1)

    # LANforge and scripts config for results
    lf_test_setup = pd.DataFrame()
    lf_test_setup['LANforge'] = lanforge_system_node_version
    lf_test_setup['fedora version'] = lanforge_fedora_version
    lf_test_setup['kernel version'] = lanforge_kernel_version
    lf_test_setup['server version'] = lanforge_server_version_full
    lf_test_setup['gui version'] = lanforge_gui_version
    lf_test_setup['gui build date'] = lanforge_gui_build_date
    lf_test_setup['gui git sha'] = lanforge_gui_git_sha
    lf_test_setup['scripts git sha'] = scripts_git_sha

    # Successfully gathered LANforge information Run Tests
    check.run_script_test()

    # Add the qa_report_html
    qa_report_html = check.qa_report_html

    # add the python3 version information
    lf_server = pd.DataFrame()
    hostname = socket.getfqdn()
    ip = socket.gethostbyname(hostname)

    lf_server['Server Host Name'] = [hostname]
    lf_server['Server ip'] = [ip]
    lf_server['Server Fedora Version'] = [platform.platform()]
    lf_server['Python3 Version'] = [sys.version]
    lf_server['Python3 Executable'] = [sys.executable]

    lf_suite_time = pd.DataFrame()
    lf_suite_time['Suite Start'] = [check.suite_start_time]
    lf_suite_time['Suite End'] = [check.suite_end_time]
    lf_suite_time['Suite Duration'] = [check.suite_duration]

    lf_test_summary = pd.DataFrame()
    lf_test_summary['Tests Run'] = [check.tests_run]
    lf_test_summary['Success'] = [check.tests_success]
    lf_test_summary['Some Tests Failed'] = [check.tests_some_failure]
    lf_test_summary['Failure'] = [check.tests_failure]
    lf_test_summary['Timeout'] = [check.tests_timeout]

    # generate output reports
    test_rig = check.get_test_rig()
    report.set_title(
        "LF Check: {test_rig}: {suite}".format(
            test_rig=test_rig, suite=test_suite))
    report.build_banner_left()
    report.start_content_div2()
    report.set_obj_html("Objective", "Run QA Tests")
    report.build_objective()
    report.set_table_title("LANForge")
    report.build_table_title()
    report.set_table_dataframe(lf_test_setup)
    report.build_table()
    report.set_table_title("LANForge CICD Server")
    report.build_table_title()
    report.set_table_dataframe(lf_server)
    report.build_table()
    report.set_table_title("LANForge Radios")
    report.build_table_title()
    report.set_table_dataframe(lf_radio_df)
    report.build_table()
    report.set_table_title("LF Check Suite Run")
    report.build_table_title()
    report.set_table_dataframe(lf_suite_time)
    report.build_table()
    if "NA" not in qa_report_html:
        report.set_table_title("LF Check QA ")
        report.build_table_title()

        abs_path = False
        if abs_path:
            qa_url = qa_report_html.replace('/home/lanforge', '')
            logger.info("QA Test Results qa_run custom: {qa_url}".format(qa_url=qa_url))
            report.build_link("QA Test Results", qa_url)
        else:
            # try relative path
            parent_path = os.path.dirname(qa_report_html)
            parent_name = os.path.basename(parent_path)
            qa_report_base_name = os.path.basename(qa_report_html)
            
            qa_url = './' + parent_name + '/' + qa_report_base_name
            logger.info("QA Test Results qa_run custom: {qa_url}".format(qa_url=qa_url))
            report.build_link("QA Test Results", qa_url)


    report.set_table_title("LF Check Suite Summary: {suite}".format(suite=test_suite))
    report.build_table_title()
    report.set_table_dataframe(lf_test_summary)
    report.build_table()
    report.set_table_title("LF Check Suite Results")
    report.build_table_title()
    html_results = check.get_html_results()
    report.set_custom_html(html_results)
    report.build_custom()
    report.build_footer()
    report.copy_js()
    html_report = report.write_html_with_timestamp()
    logger.info("html report: {}".format(html_report))
    try:
        report.write_pdf_with_timestamp()
    except BaseException:
        logger.info("exception write_pdf_with_timestamp()")

    logger.info("lf_check_html_report: " + html_report)
    if args.no_send_email or check.email_list_test == "":
        logger.info("send email not set or email_list_test not set")
    else:
        check.send_results_email(report_file=html_report)
    #
    if args.update_latest:
        report_path = os.path.dirname(html_report)
        parent_report_dir = os.path.dirname(report_path)

        # copy results to lastest so someone may see the latest.
        # duplicates html_report file up one directory is the destination
        html_report_latest = parent_report_dir + "/{dir}_latest.html".format(dir=__dir)

        banner_src_png = report_path + "/banner.png"
        banner_dest_png = parent_report_dir + "/banner.png"
        CandelaLogo_src_png = report_path + "/CandelaLogo2-90dpi-200x90-trans.png"
        CandelaLogo_dest_png = parent_report_dir + "/CandelaLogo2-90dpi-200x90-trans.png"
        CandelaLogo_small_src_png = report_path + "/candela_swirl_small-72h.png"
        CandelaLogo_small_dest_png = parent_report_dir + "/candela_swirl_small-72h.png"
        report_src_css = report_path + "/report.css"
        report_dest_css = parent_report_dir + "/report.css"
        custom_src_css = report_path + "/custom.css"
        custom_dest_css = parent_report_dir + "/custom.css"
        font_src_woff = report_path + "/CenturyGothic.woff"
        font_dest_woff = parent_report_dir + "/CenturyGothic.woff"

        # pprint.pprint([
        #    ('banner_src', banner_src_png),
        #    ('banner_dest', banner_dest_png),
        #    ('CandelaLogo_src_png', CandelaLogo_src_png),
        #    ('CandelaLogo_dest_png', CandelaLogo_dest_png),
        #    ('report_src_css', report_src_css),
        #    ('custom_src_css', custom_src_css)
        # ])

        # copy one directory above
        try:
            shutil.copyfile(html_report, html_report_latest)
        except BaseException:
            logger.info("unable to copy results from {html} to {html_latest}".format(html=html_report, html_latest=html_report_latest))
            logger.info("check permissions on {html_report_latest}".format(html_report_latest=html_report_latest))

        # copy banner and logo up one directory,
        shutil.copyfile(banner_src_png, banner_dest_png)
        shutil.copyfile(CandelaLogo_src_png, CandelaLogo_dest_png)
        shutil.copyfile(report_src_css, report_dest_css)
        shutil.copyfile(custom_src_css, custom_dest_css)
        shutil.copyfile(font_src_woff, font_dest_woff)
        shutil.copyfile(CandelaLogo_small_src_png, CandelaLogo_small_dest_png)

        # print out locations of results
        logger.info("html_report_latest: {latest}".format(latest=html_report_latest))


if __name__ == '__main__':
    main()
