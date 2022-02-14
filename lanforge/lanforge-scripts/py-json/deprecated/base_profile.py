#!/usr/bin/env python3
import datetime
import random
import string
from pprint import pformat


class BaseProfile:
    def __init__(self, local_realm, debug=False):
        self.parent_realm = local_realm
        self.exit_on_error = False
        self.debug = debug or local_realm.debug
        self.profiles = []

    def json_get(self, _req_url, debug_=False):
        return self.parent_realm.json_get(_req_url, debug_=debug_)

    def json_post(self, req_url=None, data=None, debug_=False, suppress_related_commands_=None):
        return self.parent_realm.json_post(_req_url=req_url,
                                           _data=data,
                                           suppress_related_commands_=suppress_related_commands_,
                                           debug_=debug_)

    def parse_time(self, time_string):
        return self.parent_realm.parse_time(time_string)

    def stopping_cx(self, name):
        return self.parent_realm.stop_cx(name)

    def cleanup_cxe_prefix(self, prefix):
        return self.parent_realm.cleanup_cxe_prefix(prefix)

    def rm_cx(self, cx_name):
        return self.parent_realm.rm_cx(cx_name)

    def rm_endp(self, ename, debug_=False, suppress_related_commands_=True):
        self.parent_realm.rm_endp(ename, debug_=debug_, suppress_related_commands_=suppress_related_commands_)

    def name_to_eid(self, eid):
        return self.parent_realm.name_to_eid(eid)

    def set_endp_tos(self, ename, _tos, debug_=False, suppress_related_commands_=True):
        return self.parent_realm.set_endp_tos(ename, _tos, debug_=debug_, suppress_related_commands_=suppress_related_commands_)

    def wait_until_endps_appear(self, these_endp, debug=False):
        return self.parent_realm.wait_until_endps_appear(these_endp, debug=debug)

    def wait_until_cxs_appear(self, these_cx, debug=False):
        return self.parent_realm.wait_until_cxs_appear(these_cx, debug=debug)

    def logg(self, message=None, audit_list=None):
        if audit_list is None:
            self.parent_realm.logg(message)
        for item in audit_list:
            if item is None:
                continue
            message += ("\n" + pformat(item, indent=4))
        self.parent_realm.logg(message)

    @staticmethod
    def replace_special_char(original):
        return original.replace('+', ' ').replace('_', ' ').strip(' ')

    # @deprecate me
    @staticmethod
    def get_milliseconds(timestamp):
        return (timestamp - datetime.datetime(1970, 1, 1)).total_seconds() * 1000

    # @deprecate me
    @staticmethod
    def get_seconds(timestamp):
        return (timestamp - datetime.datetime(1970, 1, 1)).total_seconds()

    @staticmethod
    def read_file(filename):
        filename = open(filename, 'r')
        return [line.split(',') for line in filename.readlines()]

    # Function to create random characters made of letters
    @staticmethod
    def random_chars(size, chars=None):
        if chars is None:
            chars = string.ascii_letters
        return ''.join(random.choice(chars) for _ in range(size))

    # --------------- create file path / find file path code - to be put into functions
    # #Find file path to save data/csv to:
    #     if args.report_file is None:
    #         new_file_path = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-h-%M-m-%S-s")).replace(':',
    #                                                                                         '-') + '-test_ipv4_variable_time'  # create path name
    #         try:
    #             path = os.path.join('/home/lanforge/report-data/', new_file_path)
    #             os.mkdir(path)
    #         except:
    #             curr_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #             path = os.path.join(curr_dir_path, new_file_path)
    #             os.mkdir(path)

    #         if args.output_format in ['csv', 'json', 'html', 'hdf','stata', 'pickle', 'pdf', 'png', 'parquet',
    #                                 'xlsx']:
    #             report_f = str(path) + '/data.' + args.output_format
    #             output = args.output_format
    #         else:
    #             print('Not supporting this report format or cannot find report format provided. Defaulting to csv data file output type, naming it data.csv.')
    #             report_f = str(path) + '/data.csv'
    #             output = 'csv'

    #     else:
    #         report_f = args.report_file
    #         if args.output_format is None:
    #             output = str(args.report_file).split('.')[-1]
    #         else:
    #             output = args.output_format
    #     print("Saving final report data in ... " + report_f)

    #     compared_rept=None
    #     if args.compared_report:
    #         compared_report_format=args.compared_report.split('.')[-1]
    #         #if compared_report_format not in ['csv', 'json', 'dta', 'pkl','html','xlsx','parquet','h5']:
    #         if compared_report_format != 'csv':
    #             print(ValueError("Cannot process this file type. Please select a different file and re-run script."))
    #             exit(1)
    #         else:
    #             compared_rept=args.compared_report
