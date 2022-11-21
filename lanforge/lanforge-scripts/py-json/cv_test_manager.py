"""
Note: This script is working as library for chamberview tests.
    It holds different commands to automate test.
"""

import sys
import os
import importlib
import time
import json
from pprint import pprint
import logging

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
cv_test_reports = importlib.import_module("py-json.cv_test_reports")
lf_rpt = cv_test_reports.lanforge_reports
InfluxRequest = importlib.import_module("py-dashboard.InfluxRequest")
influx_add_parser_args = InfluxRequest.influx_add_parser_args
RecordInflux = InfluxRequest.RecordInflux
logger = logging.getLogger(__name__)


def cv_base_adjust_parser(args):
    if args.test_rig != "":
        # TODO:  In future, can use TestRig once that GUI update has propagated
        args.set.append(["Test Rig ID:", args.test_rig])

    if args.test_tag != "":
        args.set.append(["TestTag", args.test_tag])

    if args.influx_host is not None:
        if not args.pull_report:
            print("Specified influx host without pull_report, will enabled pull_request.")
            args.pull_report = True


def cv_add_base_parser(parser):
    parser.add_argument("-m", "--mgr", type=str, default="localhost",
                        help="address of the LANforge GUI machine (localhost is default)")
    parser.add_argument("-o", "--port", type=int, default=8080,
                        help="IP Port the LANforge GUI is listening on (8080 is default)")
    parser.add_argument("--lf_user", type=str, default="lanforge",
                        help="LANforge username to pull reports")
    parser.add_argument("--lf_password", type=str, default="lanforge",
                        help="LANforge Password to pull reports")
    parser.add_argument("-i", "--instance_name", type=str, default="cv_dflt_inst",
                        help="create test instance")
    parser.add_argument("-c", "--config_name", type=str, default="cv_dflt_cfg",
                        help="Config file name")

    parser.add_argument("-r", "--pull_report", action='store_true',
                        help="pull reports from lanforge (by default: False)")
    parser.add_argument("--load_old_cfg", action='store_true',
                        help="Should we first load defaults from previous run of the capacity test?  Default is False")

    parser.add_argument("--enable", action='append', nargs=1, default=[],
                        help="Specify options to enable (set cfg-file value to 1).  See example raw text config for possible options.  May be specified multiple times.  Most tests are enabled by default, except: longterm")
    parser.add_argument("--disable", action='append', nargs=1, default=[],
                        help="Specify options to disable (set value to 0).  See example raw text config for possible options.  May be specified multiple times.")
    parser.add_argument("--set", action='append', nargs=2, default=[],
                        help="Specify options to set values based on their label in the GUI. Example: --set 'Basic Client Connectivity' 1  May be specified multiple times.")
    parser.add_argument("--raw_line", action='append', nargs=1, default=[],
                        help="Specify lines of the raw config file.  Example: --raw_line 'test_rig: Ferndale-01-Basic'  See example raw text config for possible options.  This is catch-all for any options not available to be specified elsewhere.  May be specified multiple times.")

    parser.add_argument("--raw_lines_file", default="",
                        help="Specify a file of raw lines to apply.")

    # Reporting info
    parser.add_argument("--test_rig", default="",
                        help="Specify the test rig info for reporting purposes, for instance:  testbed-01")
    parser.add_argument("--test_tag", default="",
                        help="Specify the test tag info for reporting purposes, for instance:  testbed-01")

    influx_add_parser_args(parser)  # csv_to_influx


class cv_test(Realm):
    def __init__(self,
                 lfclient_host="localhost",
                 lfclient_port=8080,
                 lf_report_dir=None,
                 debug_=False,
                 ):
        super().__init__(lfclient_host=lfclient_host,
                         lfclient_port=lfclient_port,
                         debug_=debug_
                         )
        self.lf_report_dir = lf_report_dir
        self.report_name = None

    # Add a config line to a text blob.  Will create new text blob
    # if none exists already.
    def create_test_config(self, config_name, blob_test_name, text):
        req_url = "/cli-json/add_text_blob"
        data = {
            "type": "Plugin-Settings",
            "name": str(blob_test_name + config_name),
            "text": text
        }

        logger.info("adding -:%s:- to test config: %s  blob-name: %s" %(text, config_name, blob_test_name))

        self.json_post(req_url, data)

    # Tell LANforge GUI Chamber View to launch a test
    def create_test(self, test_name, instance, load_old_cfg):
        cmd = "cv create '{0}' '{1}' '{2}'".format(test_name, instance, load_old_cfg)
        return self.run_cv_cmd(str(cmd))

    # Tell LANforge chamber view to load a scenario.
    def load_test_scenario(self, instance, scenario):
        cmd = "cv load '{0}' '{1}'".format(instance, scenario)
        self.run_cv_cmd(cmd)

    # load test config for a chamber view test instance.
    def load_test_config(self, test_config, instance):
        cmd = "cv load '{0}' '{1}'".format(instance, test_config)
        self.run_cv_cmd(cmd)

    # start the test
    def start_test(self, instance):
        cmd = "cv click '%s' Start" % instance
        return self.run_cv_cmd(cmd)

    # close test
    def close_test(self, instance):
        cmd = "cv click '%s' 'Close'" % instance
        self.run_cv_cmd(cmd)

    # Cancel
    def cancel_test(self, instance):
        cmd = "cv click '%s' Cancel" % instance
        self.run_cv_cmd(cmd)

    # For auto save report
    def auto_save_report(self, instance):
        cmd = "cv click %s 'Auto Save Report'" % instance
        self.run_cv_cmd(cmd)

    # To get the report location
    def get_report_location(self, instance):
        cmd = "cv get %s 'Report Location:'" % instance
        location = self.run_cv_cmd(cmd)
        return location

    # To get if test is running or not
    def get_is_running(self, instance):
        cmd = "cv get %s 'StartStop'" % instance
        val = self.run_cv_cmd(cmd)
        # pprint(val)
        return val[0]["LAST"]["response"] == 'StartStop::Stop'

    # To save to html
    def save_html(self, instance):
        cmd = "cv click %s 'Save HTML'" % instance
        self.run_cv_cmd(cmd)

    # Check if test instance exists
    def get_exists(self, instance):
        cmd = "cv exists %s" % instance
        val = self.run_cv_cmd(cmd)
        # pprint(val)
        return val[0]["LAST"]["response"] == 'YES'

    # Check if chamberview is built
    def get_cv_is_built(self):
        cmd = "cv is_built"
        val = self.run_cv_cmd(cmd)
        # pprint(val)
        rv = val[0]["LAST"]["response"] == 'YES'
        logger.info("is-built: {rv} ".format(rv=rv))
        return rv

    # delete the test instance
    def delete_instance(self, instance):
        cmd = "cv delete %s" % instance
        self.run_cv_cmd(cmd)

        # It can take a while, some test rebuild the old scenario upon exit, for instance.
        tries = 0
        while True:
            if self.get_exists(instance):
                logger.info("Waiting %i/60 for test instance: %s to be deleted." % (tries, instance))
                tries += 1
                if tries > 60:
                    break
                time.sleep(1)
            else:
                break

        # And make sure chamber-view is properly re-built
        tries = 0
        while True:
            if not self.get_cv_is_built():
                logger.info("Waiting %i/60 for Chamber-View to be built." % tries)
                tries += 1
                if tries > 60:
                    break
                time.sleep(1)
            else:
                break

    # Get port listing
    def get_ports(self, url="/ports/"):
        response = self.json_get(url)
        return response

    def show_text_blob(self, config_name, blob_test_name, brief):
        req_url = "/cli-json/show_text_blob"
        response_json = []
        data = {"type": "Plugin-Settings"}
        if config_name and blob_test_name:
            data["name"] = "%s%s" % (blob_test_name, config_name)  # config name
        else:
            data["name"] = "ALL"
        if brief:
            data["brief"] = "brief"
        self.json_post(req_url, data, response_json_list_=response_json)
        return response_json

    def rm_text_blob(self, config_name, blob_test_name):
        req_url = "/cli-json/rm_text_blob"
        data = {
            "type": "Plugin-Settings",
            "name": str(blob_test_name + config_name),  # config name
        }
        self.json_post(req_url, data)

    def rm_cv_text_blob(self, cv_type="Network-Connectivity", name=None):
        req_url = "/cli-json/rm_text_blob"
        data = {
            "type": cv_type,
            "name": name,  # config name
        }
        self.json_post(req_url, data)

    @staticmethod
    def apply_cfg_options(cfg_options, enables, disables, raw_lines, raw_lines_file):

        # Read in calibration data and whatever else.
        if raw_lines_file != "":
            with open(raw_lines_file) as fp:
                line = fp.readline()
                while line:
                    cfg_options.append(line)
                    line = fp.readline()
            fp.close()

        for en in enables:
            cfg_options.append("%s: 1" % (en[0]))

        for en in disables:
            cfg_options.append("%s: 0" % (en[0]))

        for r in raw_lines:
            cfg_options.append(r[0])

    def build_cfg(self, config_name, blob_test, cfg_options):
        for value in cfg_options:
            self.create_test_config(config_name, blob_test, value)

        # Request GUI update its text blob listing.
        self.show_text_blob(config_name, blob_test, False)

        # Hack, not certain if the above show returns before the action has been completed
        # or not, so we sleep here until we have better idea how to query if GUI knows about
        # the text blob.
        time.sleep(5)

    # load_old_config is boolean
    # test_name is specific to the type of test being launched (Dataplane, tr398, etc)
    #    ChamberViewFrame.java has list of supported test names.
    # instance_name is per-test instance, it does not matter much, just use the same name
    #    throughout the entire run of the test.
    # config_name what to call the text-blob that configures the test.  Does not matter much
    #    since we (re)create it during the run.
    # sets:  Arrany of [key,value] pairs.  The key is the widget name, typically the label
    #    before the entry field.
    # pull_report:  Boolean, should we download the report to current working directory.
    # lf_host:  LANforge machine running the GUI.
    # lf_password:  Password for LANforge machine running the GUI.
    # cv_cmds:  Array of raw chamber-view commands, such as "cv click 'button-name'"
    #    These (and the sets) are applied after the test is created and before it is started.
    def create_and_run_test(self, load_old_cfg, test_name, instance_name, config_name, sets,
                            pull_report, lf_host, lf_user, lf_password, cv_cmds, local_lf_report_dir=None, ssh_port=22,
                            graph_groups_file=None):
        load_old = "false"
        if load_old_cfg:
            load_old = "true"

        start_try = 0
        while True:
            response = self.create_test(test_name, instance_name, load_old)
            if response[0]["LAST"]["response"] == "OK":
                break
            else:
                logger.info("Could not create test, try: %i/60:\n" % start_try)
                pprint(response)
                start_try += 1
                if start_try > 60:
                    logger.error("ERROR:  Could not start within 60 tries, aborting.")
                    exit(1)
                time.sleep(1)

        self.load_test_config(config_name, instance_name)
        self.auto_save_report(instance_name)

        for kv in sets:
            cmd = "cv set '%s' '%s' '%s'" % (instance_name, kv[0], kv[1])
            logger.info("Running CV set command:{cmd}".format(cmd=cmd))
            self.run_cv_cmd(cmd)

        for cmd in cv_cmds:
            logger.info("Running CV set command:{cmd}".format(cmd=cmd))
            self.run_cv_cmd(cmd)

        response = self.start_test(instance_name)
        if response[0]["LAST"]["response"].__contains__("Could not find instance:"):
            logger.error("ERROR:  start_test failed: ", response[0]["LAST"]["response"], "\n")
            # pprint(response)
            exit(1)

        not_running = 0
        while True:
            cmd = "cv get_and_close_dialog"
            dialog = self.run_cv_cmd(cmd)
            if dialog[0]["LAST"]["response"] != "NO-DIALOG":
                logger.info("Popup Dialog:\n")
                logger.info(dialog[0]["LAST"]["response"])

            check = self.get_report_location(instance_name)
            location = json.dumps(check[0]["LAST"]["response"])
            if location != '\"Report Location:::\"':
                logger.info(location)
                location = location.replace('\"Report Location:::', '')
                location = location.replace('\"', '')
                report = lf_rpt()
                logger.info(graph_groups_file)
                if graph_groups_file is not None:
                    filelocation = open(graph_groups_file, 'a')
                    if pull_report:
                        location2 = location.replace('/home/lanforge/html-reports/', '')
                        filelocation.write(location2 + '/kpi.csv\n')
                    else:
                        filelocation.write(location + '/kpi.csv\n')
                    filelocation.close()
                logger.info(location)
                self.lf_report_dir = location
                if pull_report:
                    try:
                        logger.info("Pulling report to directory: %s from %s@%s/%s" %
                                    (local_lf_report_dir, lf_user, lf_host, location))
                        report.pull_reports(hostname=lf_host, username=lf_user, password=lf_password,
                                            port=ssh_port, report_dir=local_lf_report_dir,
                                            report_location=location)
                    except Exception as e:
                        logger.critical("SCP failed, user %s, password %s, dest %s" % (lf_user, lf_password, lf_host))
                        raise e  # Exception("Could not find Reports")
                    break
            else:
                logger.info('Not reporting to kpi file')
                

            # Of if test stopped for some reason and could not generate report.
            if not self.get_is_running(instance_name):
                logger.info("Detected test is not running.")
                not_running += 1
                if not_running > 5:
                    break

            time.sleep(1)
        self.report_name = self.get_report_location(instance_name)
        # Ensure test is closed and cleaned up
        self.delete_instance(instance_name)

        # Clean up any remaining popups.
        while True:
            dialog = self.run_cv_cmd(cmd)
            if dialog[0]["LAST"]["response"] != "NO-DIALOG":
                logger.info("Popup Dialog:\n")
                logger.info(dialog[0]["LAST"]["response"])
            else:
                break

    # Takes cmd-line args struct or something that looks like it.
    # See csv_to_influx.py::influx_add_parser_args for options, or --help.
    def check_influx_kpi(self, args):
        if self.lf_report_dir is None:
            # Nothing to report on.
            logger.info("Not submitting to influx, no report-dir.\n")
            return

        if args.influx_host is None:
            # No influx configured, return.
            logger.info("Not submitting to influx, influx_host not configured.\n")
            return

        logger.info("Creating influxdb connection, host: %s:%s org: %s  token: %s  bucket: %s\n" %
                    (args.influx_host, args.influx_port, args.influx_org, args.influx_token, args.influx_bucket))
        # lfjson_host would be if we are reading out of LANforge or some other REST
        # source, which we are not.  So dummy those out.
        influxdb = RecordInflux(_influx_host=args.influx_host,
                                _influx_port=args.influx_port,
                                _influx_org=args.influx_org,
                                _influx_token=args.influx_token,
                                _influx_bucket=args.influx_bucket)

        # lf_wifi_capacity_test.py may be run / initiated by a remote system against a lanforge
        # the local_lf_report_dir is where data is stored,  if there is no local_lf_report_dir then the test is run directly on lanforge
        if self.lf_report_dir:
            csv_path = "%s/kpi.csv" % self.lf_report_dir
        else:
            kpi_location = self.lf_report_dir + "/" + os.path.basename(self.lf_report_dir)
            # the lf_report_dir is the parent directory,  need to get the directory name
            csv_path = "%s/kpi.csv" % kpi_location

        logger.info("Attempt to submit kpi: ", csv_path)
        logger.info("Posting to influx...\n")
        influxdb.csv_to_influx(csv_path)

        logger.info("All done posting to influx.\n")

    # ************************** chamber view **************************
    def add_text_blob_line(self,
                           scenario_name="Automation",
                           Resources="1.1",
                           Profile="STA-AC",
                           Amount="1",
                           DUT="DUT",
                           Dut_Radio="Radio-1",
                           Uses1="wiphy0",
                           Uses2="AUTO",
                           Traffic="http",
                           Freq="-1",
                           VLAN=""):
        req_url = "/cli-json/add_text_blob"

        text_blob = "profile_link" + " " + Resources + " " + Profile + " " + Amount + " " + "\'DUT:" + " " + DUT \
                    + " " + Dut_Radio + "\' " + Traffic + " " + Uses1 + "," + Uses2 + " " + Freq + " " + VLAN

        if self.debug:
            print("text-blob-line: %s" % (text_blob))

        data = {
            "type": "Network-Connectivity",
            "name": scenario_name,
            "text": text_blob
        }

        self.json_post(req_url, data)

    def pass_raw_lines_to_cv(self,
                             scenario_name="Automation",
                             Rawline=""):
        req_url = "/cli-json/add_text_blob"
        data = {
            "type": "Network-Connectivity",
            "name": scenario_name,
            "text": Rawline
        }
        self.json_post(req_url, data)

        # This is for chamber view buttons

    def apply_cv_scenario(self, cv_scenario):
        cmd = "cv apply '%s'" % cv_scenario  # To apply scenario
        self.run_cv_cmd(cmd)
        logger.info("Applying %s scenario" % cv_scenario)

    def build_cv_scenario(self):  # build chamber view scenario
        cmd = "cv build"
        self.run_cv_cmd(cmd)
        logger.info("Building scenario")

    def get_cv_build_status(self):  # check if scenario is build
        cmd = "cv is_built"
        response = self.run_cv_cmd(cmd)
        return self.check_reponse(response)

    def sync_cv(self):  # sync
        cmd = "cv sync"
        logger.info(self.run_cv_cmd(cmd))

    def run_cv_cmd(self, command):  # Send chamber view commands
        response_json = []
        req_url = "/gui-json/cmd"
        data = {"cmd": command}
        self.json_post(req_url, data, debug_=False, response_json_list_=response_json)
        return response_json

    @staticmethod
    def get_response_string(response):
        return response[0]["LAST"]["response"]

    def get_popup_info_and_close(self):
        cmd = "cv get_and_close_dialog"
        dialog = self.run_cv_cmd(cmd)
        if dialog[0]["LAST"]["response"] != "NO-DIALOG":
            logger.info("Popup Dialog:\n")
            logger.info(dialog[0]["LAST"]["response"])
