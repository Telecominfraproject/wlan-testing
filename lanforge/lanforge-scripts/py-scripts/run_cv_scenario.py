#!/usr/bin/env python3
# This script will set the LANforge to a BLANK database then it will load the specified database
# and start a graphical report
import logging
import argparse
import importlib
import os
import pprint
import sys
import time
from time import sleep

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm

"""
    cvScenario.scenario_db = args.scenario_db
    if args.cv_test is not None:
        cvScenario.cv_test = args.cv_test
    if args.test_scenario is not None:
        cvScenario.test_scenario = args.test_scenario
"""


class RunCvScenario(LFCliBase):
    def __init__(self, lfhost="localhost", lfport=8080, debug_=False, lanforge_db_=None, cv_scenario_=None,
                 cv_test_=None, test_scenario_=None, report_file_name=None):
        super().__init__(_lfjson_host=lfhost, _lfjson_port=lfport, _debug=debug_, _exit_on_error=True,
                         _exit_on_fail=True)
        self.lanforge_db = lanforge_db_
        self.cv_scenario = cv_scenario_
        self.cv_test = cv_test_
        self.test_profile = test_scenario_
        self.localrealm = Realm(lfclient_host=lfhost, lfclient_port=lfport, debug_=debug_)
        self.report_name = report_file_name
        self.load_timeout_sec = 2 * 60

    def get_report_file_name(self):
        return self.report_name

    def build(self):
        data = {
            "name": "BLANK",
            "action": "overwrite",
            "clean_dut": "yes",
            "clean_chambers": "yes"
        }
        self.json_post("/cli-json/load", data)
        self.wait_for_db_load_and_sync()

        port_counter = 0
        attempts = 6
        alias_map = None
        while (attempts > 0) and (port_counter > 0):
            sleep(1)
            attempts -= 1
            logger.debug("looking for ports like vap+")
            port_list = self.localrealm.find_ports_like("vap+")
            alias_map = LFUtils.portListToAliasMap(port_list)
            port_counter = len(alias_map)

            port_list = self.localrealm.find_ports_like("sta+")
            alias_map = LFUtils.portListToAliasMap(port_list)
            port_counter += len(alias_map)
            if port_counter == 0:
                break

        if (port_counter != 0) and (attempts == 0):
            logger.error("There appears to be a vAP in this database, quitting.")
            logger.error(pprint.pformat(alias_map))
            exit(1)

        data = {
            "name": self.lanforge_db,
            "action": "overwrite",
            "clean_dut": "yes",
            "clean_chambers": "yes"
        }
        self.json_post("/cli-json/load", data)
        self.wait_for_db_load_and_sync()
        self._pass("Loaded scenario %s" % self.lanforge_db, True)
        return True

    def wait_for_db_load_and_sync(self):
        events_response = self.json_get("/events/last")
        if "event" not in events_response:
            raise ValueError("Unable to find last event")
        if "id" not in events_response["event"]:
            pprint.pprint(events_response["event"])
            raise ValueError("bad event format")
        previous_event_id = events_response["event"]["id"]

        # check for scenario (db) load message
        begin_time: int = round(time.time() * 1000)
        load_completed = False
        while not load_completed:
            if time.time() > (begin_time + self.load_timeout_sec):
                logger.error("Unable to load database within %d sec" % self.load_timeout_sec)
                exit(1)
            events_response = self.json_get("/events/since/%s" % previous_event_id)
            pronoun = None
            if "events" in events_response:
                pronoun = "events"
            elif "event" in events_response:
                pronoun = "event"
            if not pronoun:
                logger.debug(pprint.pformat(("events response", events_response)))
                raise ValueError("incorrect events response")
            for event_o in events_response[pronoun]:
                if load_completed:
                    break
                for (key, record) in event_o.items():
                    if "event description" not in record:
                        continue
                    if not record["event description"]:
                        continue
                    if record["event description"].startswith("LOAD COMPLETED at "):
                        logger.info("load completed: %s " % record["event description"])
                        load_completed = True
                        break
            if not load_completed:
                sleep(1)

        blobs_last_updated = begin_time
        status_response = self.json_get("/")
        if "text_records_last_updated_ms" in status_response:
            blobs_last_updated = int(status_response["text_records_last_updated_ms"])
            logger.debug("blobs updated at %d" % blobs_last_updated)
        else:
            begin_time = round(time.time() * 1000)
            logger.info("no text_records_last_updated_ms, using %d " % begin_time)
        # next we will want to sync our text blobs up
        self.json_post("/cli-json/show_text_blob", {
            "type": "ALL",
            "name": "ALL"
        })

        load_completed = False
        while not load_completed:
            sleep(1)
            if time.time() > (begin_time + (6 * 1000)):
                logger.info("waited %d sec for text blobs to update" % self.load_timeout_sec)
                break
            status_response = self.json_get("/")
            if "text_records_last_updated_ms" in status_response:
                updated = int(status_response["text_records_last_updated_ms"])
                logger.debug("text_records updated at %d" % updated)
                if updated > blobs_last_updated:
                    break
            else:
                pprint.pprint(status_response)
            self.json_post("/cli-json/show_text_blob", {
                "type": "ALL",
                "name": "ALL"
            })
        delta: float = (time.time() * 1000) - begin_time
        logger.debug("blobs loaded in %d ms" % delta)

        # next show duts
        self.json_post("/cli-json/show_dut", {"name": "ALL"})
        self.json_post("/cli-json/show_profile", {"name": "ALL"})
        self.json_post("/cli-json/show_traffic_profile", {"name": "ALL"})
        sleep(5)

    def start(self, debug_=False):
        # /gui_cli takes commands keyed on 'cmd', so we create an array of commands
        commands = [
            "cv sync",
            "sleep 4",
            "cv apply '%s'" % self.cv_scenario,
            "sleep 4",
            "cv build",
            "sleep 4",
            "cv is_built",
            "cv sync",
            "sleep 4",
            "cv list_instances",
            "cv create '%s' 'test_ref' 'true'" % self.cv_test,
            "sleep 5",
            "cv load test_ref '%s'" % self.test_profile,
            "sleep 5",
            "cv click test_ref 'Auto Save Report'",
            "sleep 1",
            "cv click test_ref Start",
            "sleep 60",
            "cv get test_ref 'Report Location:'",
            "sleep 5",
            # "cv click test_ref 'Save HTML'",
            "cv click test_ref 'Close'",
            "sleep 1",
            "cv click test_ref Cancel",
            "sleep 1",
            "exit"
        ]
        for command in commands:
            data = {
                "cmd": command
            }
            try:
                debug_par = ""
                if debug_:
                    debug_par = "?__debug=1"
                if command.endswith("is_built"):
                    logger.info("Waiting for scenario to build...", )
                    self.localrealm.wait_while_building(debug_=False)
                    logger.info("...proceeding")
                elif command.startswith("sleep "):
                    nap = int(command.split(" ")[1])
                    logger.info("sleeping %d..." % nap)
                    sleep(nap)
                    logger.info("...proceeding")
                elif command == "cv list_instances":
                    response_json = []
                    logger.debug("running %s..." % command)
                    response = self.json_post("/gui-json/cmd%s" % debug_par,
                                              data,
                                              debug_=debug_,
                                              response_json_list_=response_json)
                    if debug_:
                        logger.debug(pprint.pformat(response))

                # TODO: update report file location
                # elif command.startswith("cv get test_ref 'Report Location:'"),
                #     self.report_file = ...
                else:
                    response_json = []
                    logger.debug("running %s..." % command)
                    self.json_post("/gui-json/cmd%s" % debug_par, data, debug_=False,
                                   response_json_list_=response_json)
                    if debug_:
                        logger.debug(pprint.pformat(response_json))
                    logger.info("...proceeding")
            except Exception as x:
                logger.error(x)

        self._pass("report finished", print_=True)
        return True

    def stop(self):
        logger.warning("Stop method does nothing")
        return True

    def cleanup(self):
        logger.warning("Cleanup method does nothing")
        return True


def main():
    logger_config = lf_logger_config.lf_logger_config()
    lfjson_host = "localhost"
    lfjson_port = 8080
    parser = argparse.ArgumentParser(
        prog="run_cv_scenario.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""LANforge Reporting Script:  Load a scenario and run a RvR report
Example:
./load_ap_scenario.py --lfmgr 127.0.0.1 --lanforge_db 'handsets' --cv_test 'WiFi Capacity' --test_profile 'test-20'
""")
    parser.add_argument("-m", "--lfmgr", type=str, help="address of the LANforge GUI machine (localhost is default)")
    parser.add_argument("-o", "--port", type=int, help="IP Port the LANforge GUI is listening on (8080 is default)")
    parser.add_argument("-d", "--lanforge_db", type=str, help="Name of test scenario database (see Status Tab)")
    parser.add_argument("-c", "--cv_scenario", type=str,
                        help="Name of Chamber View test scenario (see CV Manage Scenarios)")
    parser.add_argument("-n", "--cv_test", type=str, help="Chamber View test")
    parser.add_argument("-s", "--test_profile", type=str, help="Name of the saved CV test profile")
    parser.add_argument("--debug", help='Enable debugging', default=False, action="store_true")
    parser.add_argument("--log_level", help='debug message verbosity', type=str)
    # TODO: update report output file or directory
    # parser.add_argument("--report_file_name", help="name of the report file", type=str)

    args = parser.parse_args()
    if args.lfmgr is not None:
        lfjson_host = args.lfmgr
    if args.port is not None:
        lfjson_port = args.port
    debug = False
    if args.debug is not None:
        debug = args.debug

    report_file_n = "untitled_report"
    if args.report_file_name:
        report_file_n = args.report_file_name

    run_cv_scenario = RunCvScenario(lfjson_host, lfjson_port, debug_=debug, report_file_name=report_file_n)

    if args.lanforge_db is not None:
        run_cv_scenario.lanforge_db = args.lanforge_db
    if args.cv_scenario is not None:
        run_cv_scenario.cv_scenario = args.cv_scenario
    if args.cv_test is not None:
        run_cv_scenario.cv_test = args.cv_test
    if args.test_profile is not None:
        run_cv_scenario.test_profile = args.test_profile
    if args.log_level is not None:
        if args.log_level == 'debug':
            logger_config.set_level_debug()
        elif args.log_level == 'info':
            logger_config.set_level_info()
        elif args.log_level == 'warning':
            logger_config.set_level_warning()
        elif args.log_level == 'error':
            logger_config.set_level_error()
        elif args.log_level == 'critical':
            logger_config.set_level_critical()

    if (run_cv_scenario.lanforge_db is None) or (run_cv_scenario.lanforge_db == ""):
        raise ValueError("Please specificy scenario database name with --scenario_db")

    if not (run_cv_scenario.build() and run_cv_scenario.passes()):
        print("scenario failed to build.")
        print(run_cv_scenario.get_fail_message())
        exit(1)

    if not (run_cv_scenario.start() and run_cv_scenario.passes()):
        print("scenario failed to start.")
        print(run_cv_scenario.get_fail_message())
        exit(1)

    if not (run_cv_scenario.stop() and run_cv_scenario.passes()):
        print("scenario failed to stop:")
        print(run_cv_scenario.get_fail_message())
        exit(1)

    if not (run_cv_scenario.cleanup() and run_cv_scenario.passes()):
        print("scenario failed to clean up:")
        print(run_cv_scenario.get_fail_message())
        exit(1)

    # TODO: report file name is not finished
    # report_file = run_cv_scenario.get_report_file_name()
    # if report_file:
    #    print("Report file saved to: %s" % report_file)
    # else:
    #    print("Report file location missing")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


if __name__ == "__main__":
    main()
