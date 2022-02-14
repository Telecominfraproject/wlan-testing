#!/usr/bin/python3

'''
NAME:
lf_check.py

PURPOSE:
lf_check.py will run a series of tests based on the test TEST_DICTIONARY listed in lf_check_config.ini.
The lf_check_config.ini file is copied from lf_check_config_template.ini and local configuration is made
to the lf_check_config.ini.

EXAMPLE:
lf_check.py

NOTES:
Before using lf_check.py
1. copy lf_check_config_template.ini to the lf_check_config.ini
2. update lf_check_config.ini to enable (TRUE) tests to be run in the TEST_DICTIONARY , the TEST_DICTIONARY needs to be passed in

'''
import datetime
import pprint
import sys
if sys.version_info[0]  != 3:
    print("This script requires Python3")
    exit()


import os
import socket
import logging
import time
from time import sleep
import argparse
import json
import configparser
import subprocess
import csv
import shutil
import os.path

# lf_report is from the parent of the current file
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path,os.pardir))
sys.path.insert(0, parent_dir_path)

#sys.path.append('../')
from lf_report import lf_report
sys.path.append('/')

CONFIG_FILE = os.getcwd() + '/lf_check_config.ini'    
RUN_CONDITION = 'ENABLE'

# setup logging FORMAT
FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'

# lf_check class contains verificaiton configuration and ocastrates the testing.
class lf_check():
    def __init__(self,
                _csv_results,
                _outfile):
        self.lf_mgr_ip = ""
        self.lf_mgr_port = "" 
        self.radio_dict = {}
        self.test_dict = {}
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        self.scripts_wd = os.getcwd()
        self.results = ""
        self.outfile = _outfile
        self.test_result = "Failure"
        self.results_col_titles = ["Test","Command","Result","STDOUT","STDERR"]
        self.html_results = ""
        self.background_green = "background-color:green"
        self.background_red = "background-color:red"
        self.background_purple = "background-color:purple"

        self.http_test_ip = ""
        self.ftp_test_ip = ""
        self.test_ip = ""

        # section TEST_GENERIC 
        self.radio_lf = ""
        self.ssdi = ""
        self.ssid_pw = ""
        self.security = ""
        self.num_sta = ""
        self.col_names = ""
        self.upstream_port = ""

        self.csv_results = _csv_results
        self.csv_results_file = ""
        self.csv_results_writer = ""
        self.csv_results_column_headers = ""
        self.logger = logging.getLogger(__name__)
        self.test_timeout = 120
        self.use_blank_db = "FALSE"
        self.use_factory_default_db = "FALSE"
        self.use_custom_db = "FALSE"
        self.production_run = "FALSE"
        self.email_list_production = ""
        self.host_ip_production = None
        self.email_list_test = ""
        self.host_ip_test = None

    # NOT complete : will send the email results
    def send_results_email(self, report_file=None):
        if (report_file is None):
            print( "No report file, not sending email.")
            return
        report_url=report_file.replace('/home/lanforge/', '')
        if report_url.startswith('/'):
            report_url = report_url[1:]
        # Following recommendation 
        # NOTE: https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-from-nic-in-python
        #command = 'echo "$HOSTNAME mail system works!" | mail -s "Test: $HOSTNAME $(date)" chuck.rekiere@candelatech.com'
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        message_txt = """Results from {hostname}:\\n
http://{ip}/{report}\\n
NOTE: for now to see stdout and stderr remove /home/lanforge from path.\\n
""".format(hostname=hostname, ip=ip, report=report_url)


        mail_subject = "Regression Test [{hostname}] {date}".format(hostname=hostname,
                                                                    date=datetime.datetime.now())
        try:
            if self.production_run == "TRUE":
                msg = message_txt.format(ip=self.host_ip_production)
                command = "echo \"{message}\" | mail -s \"{subject}\" {address}".format(
                    message=msg,
                    subject=mail_subject,
                    ip=self.host_ip_production,
                    address=self.email_list_production)
            else:
                msg = message_txt.format(ip=ip)
                command = "echo \"{message}\" | mail -s \"{subject}\" {address}".format(
                    message=msg,
                    subject=mail_subject,
                    ip=ip, #self.host_ip_test,
                    address=self.email_list_test)

            print("running:[{}]".format(command))
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
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
        self.csv_results_column_headers = ['Test','Command','Result','STDOUT','STDERR'] 
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

    # Functions in this section are/can be overridden by descendants
    # This code reads the lf_check_config.ini file to populate the test variables
    def read_config_contents(self):
        self.logger.info("read_config_contents {}".format(CONFIG_FILE))
        config_file = configparser.ConfigParser()
        success = True
        success = config_file.read(CONFIG_FILE)
        self.logger.info("logger worked")

        if 'LF_MGR' in config_file.sections():
            section = config_file['LF_MGR']
            self.lf_mgr_ip = section['LF_MGR_IP']
            self.lf_mgr_port = section['LF_MGR_PORT']
            self.logger.info("lf_mgr_ip {}".format(self.lf_mgr_ip))
            self.logger.info("lf_mgr_port {}".format(self.lf_mgr_port))

        if 'TEST_NETWORK' in config_file.sections():
            section = config_file['TEST_NETWORK']
            self.http_test_ip = section['HTTP_TEST_IP']
            self.logger.info("http_test_ip {}".format(self.http_test_ip))
            self.ftp_test_ip = section['FTP_TEST_IP']
            self.logger.info("ftp_test_ip {}".format(self.ftp_test_ip))
            self.test_ip = section['TEST_IP']
            self.logger.info("test_ip {}".format(self.test_ip))

        if 'TEST_GENERIC' in config_file.sections():
            section = config_file['TEST_GENERIC']
            self.radio_lf = section['RADIO_USED']
            self.logger.info("radio_lf {}".format(self.radio_lf))
            self.ssid = section['SSID_USED']
            self.logger.info("ssid {}".format(self.ssid))
            self.ssid_pw = section['SSID_PW_USED']
            self.logger.info("ssid_pw {}".format(self.ssid_pw))
            self.security = section['SECURITY_USED']
            self.logger.info("secruity {}".format(self.security))
            self.num_sta = section['NUM_STA']
            self.logger.info("num_sta {}".format(self.num_sta))
            self.col_names = section['COL_NAMES']
            self.logger.info("col_names {}".format(self.col_names))
            self.upstream_port = section['UPSTREAM_PORT']
            self.logger.info("upstream_port {}".format(self.upstream_port))

        if 'TEST_PARAMETERS' in config_file.sections():
            section = config_file['TEST_PARAMETERS']
            self.test_timeout = section['TEST_TIMEOUT']
            self.use_blank_db = section['LOAD_BLANK_DB']
            self.use_factory_default_db = section['LOAD_FACTORY_DEFAULT_DB']
            self.use_custom_db = section['LOAD_CUSTOM_DB']
            self.custom_db = section['CUSTOM_DB']
            self.production_run = section['PRODUCTION_RUN']
            self.email_list_production = section['EMAIL_LIST_PRODUCTION']
            self.host_ip_production = section['HOST_IP_PRODUCTION']
            self.email_list_test = section['EMAIL_LIST_TEST']
            self.host_ip_test = section['HOST_IP_TEST']

        if 'RADIO_DICTIONARY' in config_file.sections():
            section = config_file['RADIO_DICTIONARY']
            self.radio_dict = json.loads(section.get('RADIO_DICT', self.radio_dict))
            self.logger.info("self.radio_dict {}".format(self.radio_dict))

        if 'TEST_DICTIONARY' in config_file.sections():
            section = config_file['TEST_DICTIONARY']
            # for json replace the \n and \r they are invalid json characters, allows for multiple line args 
            try:            
                self.test_dict = json.loads(section.get('TEST_DICT', self.test_dict).replace('\n',' ').replace('\r',' '))
                self.logger.info("TEST_DICTIONARY:  {}".format(self.test_dict))
            except:
                self.logger.info("Excpetion loading TEST_DICTIONARY, is there comma after the last entry?  Check syntax")                

    def load_factory_default_db(self):
        #self.logger.info("file_wd {}".format(self.scripts_wd))
        try:
            os.chdir(self.scripts_wd)
            #self.logger.info("Current Working Directory {}".format(os.getcwd()))
        except:
            self.logger.info("failed to change to {}".format(self.scripts_wd))

        # no spaces after FACTORY_DFLT
        command = "./{} {}".format("scenario.py", "--load FACTORY_DFLT")
        process = subprocess.Popen((command).split(' '), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        # wait for the process to terminate
        out, err = process.communicate()
        errcode = process.returncode

    # Not currently used
    def load_blank_db(self):
        #self.logger.info("file_wd {}".format(self.scripts_wd))
        try:
            os.chdir(self.scripts_wd)
            #self.logger.info("Current Working Directory {}".format(os.getcwd()))
        except:
            self.logger.info("failed to change to {}".format(self.scripts_wd))

        # no spaces after FACTORY_DFLT
        command = "./{} {}".format("scenario.py", "--load BLANK")
        process = subprocess.Popen((command).split(' '), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    def load_custom_db(self,custom_db):
        #self.logger.info("file_wd {}".format(self.scripts_wd))
        try:
            os.chdir(self.scripts_wd)
            #self.logger.info("Current Working Directory {}".format(os.getcwd()))
        except:
            self.logger.info("failed to change to {}".format(self.scripts_wd))

        # no spaces after FACTORY_DFLT
        command = "./{} {}".format("scenario.py", "--load {}".format(custom_db))
        process = subprocess.Popen((command).split(' '), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        # wait for the process to terminate
        out, err = process.communicate()
        errcode = process.returncode

    def run_script_test(self):
        self.start_html_results() 
        self.start_csv_results()

        for test in self.test_dict:
            if self.test_dict[test]['enabled'] == "FALSE":
                self.logger.info("test: {}  skipped".format(test))
            # load the default database 
            elif self.test_dict[test]['enabled'] == "TRUE":
                # Make the command replace ment a separate method call.
                # loop through radios
                for radio in self.radio_dict:
                    # Replace RADIO, SSID, PASSWD, SECURITY with actual config values (e.g. RADIO_0_CFG to values)
                    # not "KEY" is just a word to refer to the RADIO define (e.g. RADIO_0_CFG) to get the vlaues
                    # --num_stations needs to be int not string (no double quotes)
                    if self.radio_dict[radio]["KEY"] in self.test_dict[test]['args']:
                        self.test_dict[test]['args'] = self.test_dict[test]['args'].replace(self.radio_dict[radio]["KEY"],'--radio {} --ssid {} --passwd {} --security {} --num_stations {}'
                        .format(self.radio_dict[radio]['RADIO'],self.radio_dict[radio]['SSID'],self.radio_dict[radio]['PASSWD'],self.radio_dict[radio]['SECURITY'],self.radio_dict[radio]['STATIONS']))

                if 'HTTP_TEST_IP' in self.test_dict[test]['args']:
                    self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('HTTP_TEST_IP',self.http_test_ip)
                if 'FTP_TEST_IP' in self.test_dict[test]['args']:
                    self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('FTP_TEST_IP',self.ftp_test_ip)
                if 'TEST_IP' in self.test_dict[test]['args']:
                    self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('TEST_IP',self.test_ip)

                if 'RADIO_USED' in self.test_dict[test]['args']:
                    self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('RADIO_USED',self.radio_lf)
                if 'SSID_USED' in self.test_dict[test]['args']:
                    self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('SSID_USED',self.ssid)
                if 'SSID_PW_USED' in self.test_dict[test]['args']:
                    self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('SSID_PW_USED',self.ssid_pw)
                if 'SECURITY_USED' in self.test_dict[test]['args']:
                    self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('SECURITY_USED',self.security)
                if 'NUM_STA' in self.test_dict[test]['args']:
                    self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('NUM_STA',self.num_sta)
                if 'COL_NAMES' in self.test_dict[test]['args']:
                    self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('COL_NAMES',self.col_names)
                if 'UPSTREAM_PORT' in self.test_dict[test]['args']:
                    self.test_dict[test]['args'] = self.test_dict[test]['args'].replace('UPSTREAM_PORT',self.col_names)
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
                        self.logger.info("{} loaded between tests with scenario.py --load {}".format(self.custom_db,self.custom_db))
                    except:
                        self.logger.info("custom database failed to load check existance and location")
                else:
                    self.logger.info("no db loaded between tests: {}".format(self.use_custom_db))

                sleep(1) # the sleep is to allow for the database to stablize

                try:
                    os.chdir(self.scripts_wd)
                    #self.logger.info("Current Working Directory {}".format(os.getcwd()))
                except:
                    self.logger.info("failed to change to {}".format(self.scripts_wd))
                cmd_args = "{}".format(self.test_dict[test]['args'])
                command = "./{} {}".format(self.test_dict[test]['command'], cmd_args)
                self.logger.info("command: {}".format(command))
                self.logger.info("cmd_args {}".format(cmd_args))

                if self.outfile is not None:
                    stdout_log_txt = self.outfile
                    stdout_log_txt = stdout_log_txt + "-{}-stdout.txt".format(test)
                    #self.logger.info("stdout_log_txt: {}".format(stdout_log_txt))
                    stdout_log = open(stdout_log_txt, 'a')
                    stderr_log_txt = self.outfile
                    stderr_log_txt = stderr_log_txt + "-{}-stderr.txt".format(test)                    
                    #self.logger.info("stderr_log_txt: {}".format(stderr_log_txt))
                    stderr_log = open(stderr_log_txt, 'a')


                print("running {}".format(command))
                process = subprocess.Popen((command).split(' '), shell=False, stdout=stdout_log, stderr=stderr_log, universal_newlines=True)
                
                try:
                    #out, err = process.communicate()
                    process.wait(timeout=int(self.test_timeout))
                except subprocess.TimeoutExpired:
                    process.terminate()
                    self.test_result = "TIMEOUT"

                    #if err:
                    #    self.logger.info("command Test timed out: {}".format(command))

                #self.logger.info(stderr_log_txt)
                if(self.test_result != "TIMEOUT"):
                    stderr_log_size = os.path.getsize(stderr_log_txt)
                    if stderr_log_size > 0 :
                        self.logger.info("File: {} is not empty: {}".format(stderr_log_txt,str(stderr_log_size)))

                        self.test_result = "Failure"
                        background = self.background_red
                    else:
                        self.logger.info("File: {} is empty: {}".format(stderr_log_txt,str(stderr_log_size)))
                        self.test_result = "Success"
                        background = self.background_green
                else:
                    self.logger.info("TIMEOUT FAILURE,  Check LANforge Radios")
                    self.test_result = "Time Out"
                    background = self.background_purple

                self.html_results += """
                    <tr><td>""" + str(test) + """</td><td class='scriptdetails'>""" + str(command) + """</td>
                <td style="""+ str(background) + """>""" + str(self.test_result) + """ 
                <td><a href=""" + str(stdout_log_txt) + """ target=\"_blank\">STDOUT</a></td>"""
                if self.test_result == "Failure":
                    self.html_results += """<td><a href=""" + str(stderr_log_txt) + """ target=\"_blank\">STDERR</a></td>"""
                elif self.test_result == "Time Out":
                    self.html_results += """<td><a href=""" + str(stderr_log_txt) + """ target=\"_blank\">STDERR</a></td>"""
                    #self.html_results += """<td></td>"""
                else:
                    self.html_results += """<td></td>"""
                self.html_results += """</tr>""" 

                row = [test,command,self.test_result,stdout_log_txt,stderr_log_txt]
                self.csv_results_writer.writerow(row)
                self.csv_results_file.flush()
                #self.logger.info("row: {}".format(row))
                self.logger.info("test: {} executed".format(test))

            else:
                self.logger.info("enable value {} invalid for test: {}, test skipped".format(self.test_dict[test]['enabled'],test))

        self.finish_html_results()        

def main():
    # arguments
    parser = argparse.ArgumentParser(
        prog='lf_check.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            lf_check.py : for running scripts listed in lf_check_config.ini file
            ''',
        description='''\
lf_check.py
-----------

Summary :
---------
for running scripts listed in lf_check_config.ini
            ''')

    parser.add_argument('--outfile', help="--outfile <Output Generic Name>  used as base name for all files generated", default="")
    parser.add_argument('--logfile', help="--logfile <logfile Name>  logging for output of lf_check.py script", default="lf_check.log")

    args = parser.parse_args()    

    # output report.
    report = lf_report(_results_dir_name="lf_check",
                       _output_html="lf_check.html",
                       _output_pdf="lf-check.pdf")

    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    csv_results = "lf_check{}-{}.csv".format(args.outfile,current_time)
    csv_results = report.file_add_path(csv_results)
    outfile = "lf_check-{}-{}".format(args.outfile,current_time)
    outfile_path = report.file_add_path(outfile)

    # lf_check() class created
    check = lf_check(_csv_results = csv_results,
                    _outfile = outfile_path)

    # get the git sha 
    process = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE)
    (commit_hash, err) = process.communicate()
    exit_code = process.wait()
    git_sha = commit_hash.decode('utf-8','ignore')

    # set up logging 
    logfile = args.logfile[:-4]
    print("logfile: {}".format(logfile))
    logfile = "{}-{}.log".format(logfile,current_time)
    logfile = report.file_add_path(logfile)
    print("logfile {}".format(logfile))
    formatter = logging.Formatter(FORMAT)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(logfile, "w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(logging.StreamHandler(sys.stdout)) # allows to logging to file and stdout

    logger.info("commit_hash: {}".format(commit_hash))
    logger.info("commit_hash2: {}".format(commit_hash.decode('utf-8','ignore')))

    check.read_config_contents() # CMR need mode to just print out the test config and not run 
    check.run_script_test()

    # Generate Ouptput reports
    report.set_title("LF Check: lf_check.py")
    report.build_banner()
    report.start_content_div()
    report.set_table_title("LF Check Test Results")
    report.build_table_title()
    report.set_text("git sha: {}".format(git_sha))
    report.build_text()
    html_results = check.get_html_results()
    report.set_custom_html(html_results)
    report.build_custom()
    html_report = report.write_html_with_timestamp()
    print("html report: {}".format(html_report))
    report.write_pdf_with_timestamp()


    report_path = os.path.dirname(html_report)
    parent_report_dir = os.path.dirname(report_path)

    # copy results to lastest so someone may see the latest.
    lf_check_latest_html = parent_report_dir + "/lf_check_latest.html"
    # duplicates html_report file up one directory
    lf_check_html_report = parent_report_dir + "/{}.html".format(outfile)

    # 
    banner_src_png =  report_path + "/banner.png"
    banner_dest_png = parent_report_dir + "/banner.png"
    CandelaLogo_src_png = report_path + "/CandelaLogo2-90dpi-200x90-trans.png"
    CandelaLogo_dest_png = parent_report_dir + "/CandelaLogo2-90dpi-200x90-trans.png"
    report_src_css = report_path + "/report.css"
    report_dest_css = parent_report_dir + "/report.css"
    custom_src_css = report_path + "/custom.css"
    custom_dest_css = parent_report_dir + "/custom.css"
    font_src_woff = report_path + "/CenturyGothic.woff"
    font_dest_woff = parent_report_dir + "/CenturyGothic.woff"

    #pprint.pprint([
    #    ('banner_src', banner_src_png),
    #    ('banner_dest', banner_dest_png),
    #    ('CandelaLogo_src_png', CandelaLogo_src_png),
    #    ('CandelaLogo_dest_png', CandelaLogo_dest_png),
    #    ('report_src_css', report_src_css),
    #    ('custom_src_css', custom_src_css)
    #])

    # copy one directory above
    shutil.copyfile(html_report,            lf_check_latest_html)
    shutil.copyfile(html_report,            lf_check_html_report)

    # copy banner and logo
    shutil.copyfile(banner_src_png,         banner_dest_png)
    shutil.copyfile(CandelaLogo_src_png,    CandelaLogo_dest_png)
    shutil.copyfile(report_src_css,         report_dest_css)
    shutil.copyfile(custom_src_css,         custom_dest_css)
    shutil.copyfile(font_src_woff,          font_dest_woff)

    print("lf_check_latest.html: "+lf_check_latest_html)
    print("lf_check_html_report: "+lf_check_html_report)

    check.send_results_email(report_file=lf_check_html_report)

if __name__ == '__main__':
    main()


