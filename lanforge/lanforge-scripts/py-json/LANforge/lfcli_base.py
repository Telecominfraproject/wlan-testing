#!env /usr/bin/python
import sys
import os
import importlib
import traceback
# Extend this class to use common set of debug and request features for your script
import pprint
import time
import random
import string
import datetime
import argparse

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

 
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../../")))

LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
LFRequest = importlib.import_module("py-json.LANforge.LFRequest")


class LFCliBase:

    SHOULD_RUN  = 0     # indicates normal operation
    SHOULD_QUIT = 1     # indicates to quit loops, close files, send SIGQUIT to threads and return
    SHOULD_HALT = 2     # indicates to quit loops, send SIGABRT to threads and exit

    # do not use `super(LFCLiBase,self).__init__(self, host, port, _debug)
    # that is py2 era syntax and will force self into the host variable, making you
    # very confused.
    def __init__(self, _lfjson_host, _lfjson_port,
                 _debug=False,
                 _exit_on_error=False,
                 _exit_on_fail=False,
                 _local_realm=None,
                 _proxy_str=None,
                 _capture_signal_list=[]):
        self.fail_pref = "FAILED: "
        self.pass_pref = "PASSED: "
        self.lfclient_host = _lfjson_host
        self.lfclient_port = _lfjson_port
        self.debug = _debug
        # if (_debug):
        #     print("LFCliBase._proxy_str: %s" % _proxy_str)
        self.proxy = {}
        self.adjust_proxy(_proxy_str)

        if (_local_realm is not None):
            self.local_realm = _local_realm

        # if (_debug):
        #     print("LFCliBase._proxy_str: %s" % _proxy_str)
        self.lfclient_url = "http://%s:%s" % (self.lfclient_host, self.lfclient_port)
        self.test_results = []
        self.exit_on_error = _exit_on_error
        self.exit_on_fail = _exit_on_fail
        self.capture_signals = _capture_signal_list
        # toggle using preexec_cli, preexec_method; the preexec_X parameters are useful
        # when you desire the lfclient to check for existance of entities to run commands on,
        # like when developing; you might toggle this with use_preexec = _debug
        # Otherwise, preexec methods use more processing time because they add an extra CLI call
        # into the queue, and inspect it -- typically nc_show_port
        self.suppress_related_commands = None
        self.finish = self.SHOULD_RUN
        self.thread_map = {}

        if len(_capture_signal_list) > 0:
            for zignal in _capture_signal_list:
                self.captured_signal(zignal, self.my_captured_signal)
        #

    def _finish(self):
        """
        call this to indicate SIGQUIT
        """
        self.finish = self.SHOULD_QUIT

    def _halt(self):
        """
        call this to indicate SIGABRT
        """
        self.finish = self.SHOULD_HALT

    def _should_finish(self):
        """
        check this when in a run loop if SIGQUIT has been indicated
        """
        if self.finish == self.SHOULD_RUN:
            return False
        if self.finish == self.SHOULD_QUIT:
            return True
        if self.finish == self.SHOULD_HALT:
            return False

    def _should_halt(self):
        """
        check this when in a run loop if SIGABRT has been indicated
        """
        if self.finish == self.SHOULD_RUN:
            return False
        if self.finish == self.SHOULD_QUIT:
            return False
        if self.finish == self.SHOULD_HALT:
            return True

    def track_thread(self, name, thread):
        if self.thread_map is None:
            self.thread_map = {}
        self.thread_map[name] = thread

    def get_thread(self, name):
        if self.thread_map is None:
            return None
        if name in self.thread_map.keys():
            return self.thread_map[name]
        return None

    def remove_thread(self, name):
        if self.thread_map is None:
            return None
        if name not in self.thread_map.keys():
            return None
        thrud = self.thread_map[name]
        del self.thread_map[name]
        return thrud

    def send_thread_signals(self, signum, fname):
        if len(self.thread_map) < 1:
            print("no threads to signal")
            return
        for (name, thread) in self.thread_map.items():
            if self.debug:
                print("sending signal %s to thread %s" % (signum, name))
            # do a thing

    def my_captured_signal(self, signum):
        """
        Override me to process signals, otherwise superclass signal handler is called.
        You may use _finish() or _halt() to indicate finishing soon or halting immediately.

        :return: True if we processed this signal
        """
        print("my_captured_signal should be overridden")
        return False

    def captured_signal(self, signum):
        """
        Here is your opportunity to decide what to do on things like KeyboardInterrupt or other UNIX signals
        Check that your subclass handled the signal or not. You may use _finish() or _halt() to indicate
        finishing soon or halting immediately. Use signal.signal(signal.STOP) to enable this.
        """
        if self.debug:
            print("Captured signal %s" % signum)
        if self.my_captured_signal(signum):
            if self.debug:
                print("subclass processed signal")
        else:
            if self.debug:
                print("subclass ignored signal")

    def clear_test_results(self):
        self.test_results.clear()

    def json_post(self, _req_url, _data, debug_=False, suppress_related_commands_=None, response_json_list_=None):
        """
        send json to the LANforge client
        :param _req_url: requested url
        :param _data: json data to send
        :param debug_: turn on debugging output
        :param suppress_related_commands_: when False, override self.preexec; when True use
        :param response_json_list_: array for json results in the response object, (alternative return method)
        :return: http response object
        """
        json_response = None
        debug_ |= self.debug
        try:
            lf_r = LFRequest.LFRequest(url=self.lfclient_url,
                                       uri=_req_url,
                                       proxies_=self.proxy,
                                       debug_=debug_,
                                       die_on_error_=self.exit_on_error)
            if suppress_related_commands_ is None:
                if 'suppress_preexec_cli' in _data:
                    del _data['suppress_preexec_cli']
                if 'suppress_preexec_method' in _data:
                    del _data['suppress_preexec_method']
                if 'suppress_postexec_cli' in _data:
                    del _data['suppress_postexec_cli']
                if 'suppress_postexec_method' in _data:
                    del _data['suppress_postexec_method']
            elif suppress_related_commands_ == False:
                _data['suppress_preexec_cli'] = False
                _data['suppress_preexec_method'] = False
                _data['suppress_postexec_cli'] = False
                _data['suppress_postexec_method'] = False
            elif self.suppress_related_commands or suppress_related_commands_:
                _data['suppress_preexec_cli'] = False
                _data['suppress_preexec_method'] = False
                _data['suppress_postexec_cli'] = True
                _data['suppress_postexec_method'] = True

            lf_r.addPostData(_data)
            if debug_:
                LFUtils.debug_printer.pprint(_data)
            json_response = lf_r.json_post(show_error=debug_,
                                          debug=debug_,
                                          response_json_list_=response_json_list_,
                                          die_on_error_=self.exit_on_error)
            if debug_ and (response_json_list_ is not None):
                pprint.pprint(response_json_list_)
        except Exception as x:
            if debug_ or self.exit_on_error:
                print("json_post posted to %s" % _req_url)
                pprint.pprint(_data)
                print("Exception %s:" % x)
                traceback.print_exception(Exception, x, x.__traceback__, chain=True)
            if self.exit_on_error:
                exit(1)
        return json_response

    def json_put(self, _req_url, _data, debug_=False, response_json_list_=None):
        """
        Send a PUT request. This is presently used for data sent to /status-msg for
        creating a new messaging session. It is not presently used for CLI scripting
        so lacks suppress_x features.
        :param _req_url: url to put
        :param _data: data to place at URL
        :param debug_: enable debug output
        :param response_json_list_: array for json results in the response object, (alternative return method)
        :return: http response object
        """
        debug_ |= self.debug
        json_response = None
        try:
            lf_r = LFRequest.LFRequest(url=self.lfclient_url,
                                       uri=_req_url,
                                       proxies_=self.proxy,
                                       debug_=debug_,
                                       die_on_error_=self.exit_on_error)
            lf_r.addPostData(_data)
            if debug_:
                LFUtils.debug_printer.pprint(_data)
            json_response = lf_r.json_put(show_error=self.debug,
                                          debug=debug_,
                                          response_json_list_=response_json_list_,
                                          die_on_error_=self.exit_on_error)
            if debug_ and (response_json_list_ is not None):
                pprint.pprint(response_json_list_)
        except Exception as x:
            if debug_ or self.exit_on_error:
                print("json_put submitted to %s" % _req_url)
                pprint.pprint(_data)
                print("Exception %s:" % x)
                traceback.print_exception(Exception, x, x.__traceback__, chain=True)
            if self.exit_on_error:
                exit(1)
        return json_response

    def json_get(self, _req_url, debug_=False):
        debug_ |= self.debug
        # if debug_:
        #     print("json_get: "+_req_url)
        #     print("json_get: proxies:")
        #     pprint.pprint(self.proxy)
        json_response = None
        # print("----- GET ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ")
        try:
            lf_r = LFRequest.LFRequest(url=self.lfclient_url,
                                       uri=_req_url,
                                       proxies_=self.proxy,
                                       debug_=debug_,
                                       die_on_error_=self.exit_on_error)
            json_response = lf_r.get_as_json(debug_=debug_, die_on_error_=False)
            #debug_printer.pprint(json_response)
            if (json_response is None):
                if debug_:
                    if hasattr(lf_r, 'print_errors'):
                        lf_r.print_errors()
                    else:
                        print("LFCliBase.json_get: no entity/response, check other errors")
                        time.sleep(10)
                return None
        except ValueError as ve:
            if debug_ or self.exit_on_error:
                print("jsonGet asked for " + _req_url)
                print("Exception %s:" % ve)
                traceback.print_exception(ValueError, ve, ve.__traceback__, chain=True)
            if self.exit_on_error:
                sys.exit(1)

        return json_response

    def json_delete(self, _req_url, debug_=False):
        debug_ |= self.debug
        if debug_:
            print("DELETE: "+_req_url)
        json_response = None
        try:
            # print("----- DELETE ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ")
            lf_r = LFRequest.LFRequest(url=self.lfclient_url,
                                       uri=_req_url,
                                       proxies_=self.proxy,
                                       debug_=debug_,
                                       die_on_error_=self.exit_on_error)
            json_response = lf_r.json_delete(debug=debug_, die_on_error_=False)
            print(json_response)
            #debug_printer.pprint(json_response)
            if (json_response is None) and debug_:
                print("LFCliBase.json_delete: no entity/response, probabily status 404")
                return None
        except ValueError as ve:
            if debug_ or self.exit_on_error:
                print("json_delete asked for " + _req_url)
                print("Exception %s:" % ve)
                traceback.print_exception(ValueError, ve, ve.__traceback__, chain=True)
            if self.exit_on_error:
                sys.exit(1)
        # print("----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ")
        return json_response

    @staticmethod
    def response_list_to_map(json_list, key, debug_=False):
        reverse_map = {}
        if (json_list is None) or (len(json_list) < 1):
            if debug_:
                print("response_list_to_map: no json_list provided")
                raise ValueError("response_list_to_map: no json_list provided")
            return reverse_map

        json_interfaces = json_list
        if key in json_list:
            json_interfaces = json_list[key]

        for record in json_interfaces:
            if len(record.keys()) < 1:
                continue
            record_keys = record.keys()
            k2 = ""
            # we expect one key in record keys, but we can't expect [0] to be populated
            json_entry = None
            for k in record_keys:
                k2 = k
                json_entry = record[k]
            # skip uninitialized port records
            if k2.find("Unknown") >= 0:
                continue
            port_json = record[k2]
            reverse_map[k2] = json_entry

        return reverse_map

    def error(self, exception):
        # print("lfcli_base error: %s" % exception)
        pprint.pprint(exception)
        traceback.print_exception(Exception, exception, exception.__traceback__, chain=True)

    def check_connect(self):
        if self.debug:
            print("Checking for LANforge GUI connection: %s" % self.lfclient_url)
        response = self.json_get("/", debug_=self.debug)
        duration = 0
        while (response is None) and (duration < 300):
            print("LANforge GUI connection not found sleeping 5 seconds, tried: %s" % self.lfclient_url)
            duration += 2
            time.sleep(2)
            response = self.json_get("", debug_=self.debug)

        if duration >= 300:
            print("Could not connect to LANforge GUI")
            sys.exit(1)

    #return ALL messages in list form
    def get_result_list(self):
        return self.test_results

    #return ALL fail messages in list form
    def get_failed_result_list(self):
        fail_list = []
        for result in self.test_results:
            if not result.startswith("PASS"):
                fail_list.append(result)
        return fail_list

    #return ALL pass messages in list form
    def get_passed_result_list(self):
        pass_list = []
        for result in self.test_results:
            if result.startswith("PASS"):
                pass_list.append(result)
        return pass_list

    def get_pass_message(self):
        pass_messages = self.get_passed_result_list()
        return "\n".join(pass_messages)

    def get_fail_message(self):
        fail_messages = self.get_failed_result_list()
        return "\n".join(fail_messages)

    def get_all_message(self):
        return "\n".join(self.test_results)

    #determines if overall test passes via comparing passes vs. fails
    def passes(self):
        pass_counter = 0
        fail_counter = 0
        for result in self.test_results:
            if result.startswith("PASS"):
                pass_counter += 1
            else:
                fail_counter += 1
        if (fail_counter == 0) and (pass_counter > 0):
            return True
        return False

    #EXIT script with a fail
    def exit_fail(self, message="%d out of %d tests failed. Exiting script with script failure."):
        total_len=len(self.get_result_list())
        fail_len=len(self.get_failed_result_list())
        print(message %(fail_len,total_len))
        sys.exit(1)

    # use this inside the class to log a failure result and print it if wished
    def _fail(self, message, print_=False):
        self.test_results.append(self.fail_pref + message)
        if print_ or self.exit_on_fail:
            print(self.fail_pref + message)
        if self.exit_on_fail:
            sys.exit(1)

    #EXIT script with a success
    def exit_success(self,message="%d out of %d tests passed successfully. Exiting script with script success."):
        num_total=len(self.get_result_list())
        num_passing=len(self.get_passed_result_list())
        print(message %(num_passing,num_total))
        sys.exit(0)

    def success(self,message="%d out of %d tests passed successfully."):
        num_total=len(self.get_result_list())
        num_passing=len(self.get_passed_result_list())
        print(message %(num_passing,num_total))

    # use this inside the class to log a pass result and print if wished.
    def _pass(self, message, print_=False):
        self.test_results.append(self.pass_pref + message)
        if print_:
            print(self.pass_pref + message)

    def adjust_proxy(self, proxy_str):
        # if self.debug:
        #     print("lfclibase.adjust_proxy: %s" % proxy_str)
        if (proxy_str is None) or (proxy_str == ""):
            return
        if self.proxy is None:
            self.proxy = {}

        if proxy_str.find("http:") > -1:
            self.proxy["http"] = proxy_str
        if proxy_str.find("https:") > -1:
            self.proxy["https"] = proxy_str
        # if self.debug:
        #     print("lfclibase::self.proxy: ")
        #     pprint.pprint(self.proxy)


    def logg2(self, level="debug", mesg=None):
        if (mesg is None) or (mesg == ""):
            return
        print("[{level}]: {msg}".format(level=level, msg=mesg))

    def logg(self,
              level=None,
              mesg=None,
              filename=None,
              scriptname=None):
        if (mesg is None) or (mesg == "") or (level is None):
            return
        userhome=os.path.expanduser('~')
        session = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-h-%M-m-%S-s")).replace(':','-')
        if filename == None:
            try:
                os.mkdir("%s/report-data/%s" % (userhome, session))
            except:
                pass
            filename = ("%s/report-data/%s/%s.log" % (userhome,session,scriptname))
        import logging
        logging.basicConfig(filename=filename, level=logging.DEBUG)
        if level == "debug":
            logging.debug(mesg)
        elif level == "info":
            logging.info(mesg)
        elif level == "warning":
            logging.warning(mesg)
        elif level == "error":
            logging.error(mesg)
    
    @staticmethod
    def parse_time(time_string):
        if isinstance(time_string, str):
            pattern = re.compile("^(\d+)([dhms]$)")
            td = pattern.match(time_string)
            if td is not None:
                dur_time = int(td.group(1))
                dur_measure = str(td.group(2))
                if dur_measure == "d":
                    duration_time = datetime.timedelta(days=dur_time)
                elif dur_measure == "h":
                    duration_time = datetime.timedelta(hours=dur_time)
                elif dur_measure == "m":
                    duration_time = datetime.timedelta(minutes=dur_time)
                elif dur_measure == "ms":
                    duration_time = datetime.timedelta(milliseconds=dur_time)
                elif dur_measure == "w":
                    duration_time = datetime.timedelta(weeks=dur_time)
                else:
                    duration_time = datetime.timedelta(seconds=dur_time)
            else:
                raise ValueError("Cannot compute time string provided: %s" % time_string)
        else:
            raise ValueError("time_string must be of type str. Type %s provided" % type(time_string))
        return duration_time

    # This style of Action subclass for argparse can't do much unless we incorporate
    # our argparse as a member of LFCliBase. Then we can do something like automatically
    # parse our proxy string without using _init_ arguments
    # class ProxyAction(argparse.Action, zelf):
    #     def __init__(self, outter_):
    #         pass
    #     def __call__(self, parser, namespace, values, option_string=None):
    #         zelf.adjust_proxy(values)

    @staticmethod
    def create_bare_argparse(prog=None,
                             formatter_class=argparse.RawTextHelpFormatter,
                             epilog=None,
                             description=None):
        if (prog is not None) or (formatter_class is not None) or (epilog is not None) or (description is not None):
            parser = argparse.ArgumentParser(prog=prog,
                                             formatter_class=formatter_class,
                                             allow_abbrev=True,
                                             epilog=epilog,
                                             description=description)
        else:
            parser = argparse.ArgumentParser()
        optional = parser.add_argument_group('optional arguments')
        required = parser.add_argument_group('required arguments')
        optional.add_argument('--mgr',            help='hostname for where LANforge GUI is running', default='localhost')
        optional.add_argument('--mgr_port',       help='port LANforge GUI HTTP service is running on', default=8080)
        optional.add_argument('--debug', '-d',    help='Enable debugging', default=False, action="store_true")
        optional.add_argument('--proxy',          nargs='?', default=None, # action=ProxyAction,
                              help='Connection proxy like http://proxy.localnet:80 or https://user:pass@proxy.localnet:3128')

        return parser

    # Create argparse with radio, securiy, ssid and passwd required
    # TODO: show example of how to add required or optional arguments from calling class
    @staticmethod
    def create_basic_argparse(prog=None,
                              formatter_class=None,
                              epilog=None,
                              description=None,
                              more_optional=None,
                              more_required=None):
        if (prog is not None) or (formatter_class is not None) or (epilog is not None) or (description is not None):
            parser = argparse.ArgumentParser(prog=prog,
                                             formatter_class=formatter_class,
                                             epilog=epilog,
                                             description=description)
        else:
            parser = argparse.ArgumentParser()
        optional = parser.add_argument_group('optional arguments')
        required = parser.add_argument_group('required arguments')

        #Optional Args
        optional.add_argument('--mgr',            help='hostname for where LANforge GUI is running', default='localhost')
        optional.add_argument('--mgr_port',       help='port LANforge GUI HTTP service is running on', default=8080)
        optional.add_argument('-u', '--upstream_port',
                            help='non-station port that generates traffic: <resource>.<port>, e.g: 1.eth1',
                            default='1.eth1')
        optional.add_argument('--num_stations',   help='Number of stations to create', default=0)
        optional.add_argument('--test_id',        help='Test ID (intended to use for ws events)', default="webconsole")
        optional.add_argument('--debug',          help='Enable debugging', default=False, action="store_true")
        optional.add_argument('--proxy',          nargs='?', default=None,
                              help='Connection proxy like http://proxy.localnet:80 or https://user:pass@proxy.localnet:3128')
        if more_optional is not None:
           for x in more_optional:
               if 'default' in x.keys():
                   optional.add_argument(x['name'], help=x['help'], default=x['default'])
               else:
                   optional.add_argument(x['name'], help=x['help'])

        #Required Args
        required.add_argument('--radio',          help='radio EID, e.g: 1.wiphy2')
        required.add_argument('--security',       help='WiFi Security protocol: < open | wep | wpa | wpa2 | wpa3 >', default="open")
        required.add_argument('--ssid',           help='WiFi SSID for script objects to associate to')
        required.add_argument('--passwd', '--password' ,'--key', help='WiFi passphrase/password/key', default="[BLANK]")

        if more_required is not None:
            for x in more_required:
                if 'default' in x.keys():
                    required.add_argument(x['name'], help=x['help'], default=x['default'])
                else:
                    required.add_argument(x['name'], help=x['help'])

        return parser

    # use this function to add an event You can see these events when watching websocket_client at 8081 port
    def add_event(self,
                  message=None,
                  event_id="new",
                  name="custom",
                  priority=1,
                  debug_=False):
        data = {
            "event_id": event_id,
            "details": message,
            "priority": priority,
            "name": name
        }
        self.json_post("/cli-json/add_event", data, debug_=debug_)

    def read_file(self, filename):
        filename = open(filename, 'r')
        return [line.split(',') for line in filename.readlines()]

    #Function creates random characters made of letters
    def random_chars(self, size, chars=None):
        if chars is None:
            chars = string.ascii_letters
        return ''.join(random.choice(chars) for x in range(size))

    def get_milliseconds(self, timestamp):
        return (timestamp - datetime.datetime(1970,1,1)).total_seconds()*1000

    def get_seconds(self, timestamp):
        return (timestamp - datetime.datetime(1970,1,1)).total_seconds()

    def replace_special_char(self, str):
        return str.replace('+', ' ').replace('_', ' ').strip(' ')

    Help_Mode = """Station WiFi modes: use the number value below:
                auto   : 0,
                a      : 1,
                b      : 2,
                g      : 3,
                abg    : 4,
                abgn   : 5,
                bgn    : 6,
                bg     : 7,
                abgnAC : 8,
                anAC   : 9,
                an     : 10,
                bgnAC  : 11,
                abgnAX : 12,
                bgnAX  : 13
""" 
