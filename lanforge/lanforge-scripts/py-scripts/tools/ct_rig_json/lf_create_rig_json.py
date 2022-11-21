#!/usr/bin/env python3
'''
File: create lf_rig.json file for --json_rig input to lf_check.py , LANforge traffic generation system
Usage: lf_create_rig_json.py --lf_mgr <lanforge ip> --lf_mgr_port <lanforge port>
'''

import argparse
import logging
import importlib
import os
import sys

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)


sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../../../")))


logger = logging.getLogger(__name__)
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")



class lf_create_rig_json():
    def __init__(self,
                 _file,
                 _lf_mgr,
                 _lf_mgr_port,
                 _lf_user,
                 _lf_passwd,
                 _test_rig,
                 _test_bed,
                 _test_server,
                 _test_db,
                 _upstream_port,
                 _test_timeout
                 ):
        self.file = _file
        self.lf_mgr = _lf_mgr
        self.lf_mgr_port = _lf_mgr_port
        self.lf_user = _lf_user
        self.lf_passwd = _lf_passwd
        self.test_rig = _test_rig
        self.test_bed = _test_bed
        self.test_server = _test_server
        self.test_db = _test_db
        self.upstream_port = _upstream_port
        self.test_timeout = _test_timeout

    # Helper methods
    def create(self):
        file_fd = open(self.file, 'w+')
        rig_json = """
{{
    "{file}":{{
        "Notes":[
            "This json file describes LANforge system used as input for --dut_json for lf_check.py"
        ]
    }},
    "test_rig_parameters":{{
        "TEST_BED": "{test_bed}",
        "TEST_RIG": "{test_rig}",
        "TEST_SERVER": "http://{test_server}/",
        "DATABASE_SQLITE": "./tools/{test_db}",
        "LF_MGR_IP": "{lf_mgr}",
        "LF_MGR_PORT": "{lf_mgr_port}",
        "LF_MGR_USER": "{lf_user}",
        "LF_MGR_PASS": "{lf_passwd}",
        "UPSTREAM_PORT":"{upstream_port}",
        "TEST_TIMEOUT": {test_timeout},
        "EMAIL_LIST_PRODUCTION": "",
        "EMAIL_LIST_TEST": "",
        "EMAIL_TITLE_TXT": "",
        "EMAIL_TXT": ""
    }}
}}

        """.format(file=self.file, lf_mgr=self.lf_mgr, lf_mgr_port=self.lf_mgr_port, lf_user=self.lf_user,
                   lf_passwd=self.lf_passwd, test_rig=self.test_rig, test_bed=self.test_bed, test_server=self.test_server, test_db=self.test_db,
                   upstream_port=self.upstream_port, test_timeout=self.test_timeout)

        file_fd.write(rig_json)
        file_fd.close()

# Feature, Sum up the subtests passed/failed from the kpi files for each run, poke those into the database, and generate a kpi graph for them.


def main():

    parser = argparse.ArgumentParser(
        prog='lf_create_rig_json.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
        lf_create_rig_json.py creates lf_rig.json file for --json_rig input to lf_check.py , LANforge traffic generation system
        NOTE: cannot have extra blank lines at the end of the json to work properly

            ''',
        description='''\
File: create lf_rig.json file for --json_rig input to lf_check.py , LANforge traffic generation system
Usage: lf_create_rig_json.py ----lf_mgr <lanforge ip> --lf_mgr_port <lanforge port>

        ''')
    parser.add_argument('--file', help='--file lf_rig.json , required', required=True)
    parser.add_argument('--lf_mgr', help='--lf_mgr <lanforge ip> required', required=True)
    parser.add_argument('--lf_mgr_port', help='--lf_mgr_port <lanforge port> ', default='8080')
    parser.add_argument('--lf_user', help='--lf_user <lanforge> ', default='lanforge')
    parser.add_argument('--lf_passwd', help='--lf_password <lanforge password> ', default='lanforge')

    parser.add_argument('--test_rig', help='--test_rig <test_rig> ', default='lanforge')
    parser.add_argument('--test_bed', help='--test_bed <test_bed> ', default='lanforge')
    parser.add_argument('--test_server', help='--test_server <test_server_ip> , ip of test reports server can be lanforge ip, default set to lanforge ip input')
    parser.add_argument('--test_db', help='--test_db <test_db> sqlite database,', default='lf_test.db')
    parser.add_argument('--upstream_port', help='--upstream_port <1.1.eth2> need to include self and resource', default='1.1.eth2')
    parser.add_argument('--test_timeout', help='--test_timeout 600', default='600')

    parser.add_argument('--log_level',
                        default=None,
                        help='Set logging level: debug | info | warning | error | critical')

    # logging configuration
    parser.add_argument(
        "--lf_logger_config_json",
        help="--lf_logger_config_json <json file> , json configuration of logger")


    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()

    # set the logger level to debug
    if args.log_level:
        logger_config.set_level(level=args.log_level)

    # lf_logger_config_json will take presidence to changing debug levels
    if args.lf_logger_config_json:
        # logger_config.lf_logger_config_json = "lf_logger_config.json"
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()


    if args.test_server is None:
        _test_server = args.lf_mgr
    else:
        _test_server = args.test_server        
    _file=args.file
    _lf_mgr=args.lf_mgr
    _lf_mgr_port=args.lf_mgr_port
    _lf_user=args.lf_user
    _lf_passwd=args.lf_passwd
    _test_rig=args.test_rig
    _test_bed=args.test_bed
    _test_db=args.test_db
    _upstream_port=args.upstream_port
    _test_timeout=args.test_timeout
    

    rig_json = lf_create_rig_json(_file=_file,
                                  _lf_mgr=_lf_mgr,
                                  _lf_mgr_port=_lf_mgr_port,
                                  _lf_user=_lf_user,
                                  _lf_passwd=_lf_passwd,
                                  _test_rig=_test_rig,
                                  _test_bed=_test_bed,
                                  _test_server=_test_server,
                                  _test_db=_test_db,
                                  _upstream_port=_upstream_port,
                                  _test_timeout=_test_timeout)
    rig_json.create()

    logger.info("created {file}".format(file=_file))


if __name__ == '__main__':
    main()
