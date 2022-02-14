#!/usr/bin/env python3

"""
NAME: lf_logger_config.py

PURPOSE:

This program is a helper  class for setting up python logger

EXAMPLE:
    At top of all files place
    import logging
    logger = logging.getLogger(__name__)

    At top of file that contains the main program. lf_logger_config.py library has
    methods to configure the "root" logger (not linux root).
    DONOT include in base classes

    lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

    In main program, this will configure the logger with default configuration for all modules
    logger_config = lf_logger_config.lf_logger_config()

    To load a JSON configuration, shown hardcoded as example, uses args to pass in name
    logger_config.lf_logger_config_json = "lf_logger_config.json"
    logger_config.load_lf_logger_config()

    At top of all other files place
    import logging
    logger = logging.getLogger(__name__)

    Then use logger.debug, logger.info, logger.warning, logger.error, logger.critical

    Note: for json the name needs to be the import name py-json.LANforge.LFRequest


    Note: If you attach a handler to a logger and one or more of its ancestors,
        it may emit the same record multiple times. In general,
        you should not need to attach a handler to more than one logger
        - if you just attach it to the appropriate logger which is highest in the logger hierarchy,
        then it will see all events logged by all descendant loggers, provided that their propagate
        setting is left set to True. A common scenario is to attach handlers only to the root logger,
        and to let propagation take care of the rest.

    Additional information:
        https://candelatech.atlassian.net/wiki/spaces/~635833922/pages/982614017/Logging+Lanforge+scripts


LICENSE:
    Free to distribute and modify. LANforge systems must be licensed.
    Copyright 2021 Candela Technologies Inc


INCLUDE_IN_README
"""

import sys
import json
import logging
import logging.config

# gets the root logger
logger = logging.getLogger()

# This class lf_logger_config should only be enstanciated in the main of the program
# not in any anticedents (base objects)
# sets up the default logger class, which may be overwritten by
# a json configuration


class lf_logger_config:
    def __init__(self):

        self.lf_logger_config_json = None
        self.lf_logger_file = None
        # need to remove the handler if using basicConfig and support python 3.7,  3.8 had force = True
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        # for now just configure the output formatting. Basic defaults
        # Change to level=logging.WARNING , also may limit some of the output
        # This is terse output
        logging.basicConfig(handlers=[logging.StreamHandler(stream=sys.stdout)], level=logging.INFO,
                            format='%(created)f %(levelname)-8s %(message)s %(filename)s %(lineno)s')

        # Note: leave basicConfig example for reference for more verbose output
        # logging.basicConfig(handlers=[logging.StreamHandler(stream=sys.stdout)], level=logging.INFO,
        #                     format='%(created)f %(name)s %(levelname)-8s %(filename)s %(lineno)s %(funcName)s  [%(module)s]: %(message)s')
        # Note: leave this for reference
        # logging.basicConfig(handlers=[logging.StreamHandler(stream=sys.stdout)], level=logging.INFO,
        #                    format='%(created)-16f %(name)-8s %(levelname)-12s  %(lineno)-6s %(funcName)-30s [%(module)s]: %(message)s')
        # Note the propagate is tricky in the sence if not set correctly will create duplicate logs output,
        # setting to false
        logging.propagate = False
        print(logging.propagate)

    def set_json(self, json_file):
        if json_file:
            # logger_config.lf_logger_config_json = "lf_logger_config.json"
            self.lf_logger_config_json = json_file
            self.load_lf_logger_config()

    def set_level(self, level):
        if not level:
            return  # no change from defaults

        if level == "debug":
            self.set_level_debug()
        elif level == "info":
            self.set_level_info()
        elif level == "warning":
            self.set_level_warning()
        elif level == "critical":
            self.set_level_warning()
        else:
            print("ERROR:  Invalid log level requested: %s" % (level))

    def set_level_debug(self):
        logging.getLogger().setLevel(logging.DEBUG)

    def set_level_info(self):
        logging.getLogger().setLevel(logging.INFO)

    def set_level_warning(self):
        logging.getLogger().setLevel(logging.WARNING)

    def set_level_error(self):
        logging.getLogger().setLevel(logging.ERROR)

    def set_level_critical(self):
        logging.getLogger().setLevel(logging.CRITICAL)

    # This is left in for now to show another example of formatting.
    def set_asctime(self):
        # we need to remove the handler if using basicConfig and support python 3.7,  3.8 had force = True
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(handlers=[logging.StreamHandler(stream=sys.stdout)], level=logging.DEBUG,
                            format='%(asctime)-16s %(name)-8s %(levelname)-12s  %(lineno)-6s %(funcName)-30s [%(module)s]: %(message)s')
        print(logger.getEffectiveLevel())  # Check what level of messages will be shown

    def load_lf_logger_config(self):
        print("In load_lf_log_config")
        # https://documentation.help/python-3-7-3/logging1.html
        # we need to remove the handler if using basicConfig and support python 3.7,  3.8 had force = True
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig()
        if self.lf_logger_config_json:
            with open(self.lf_logger_config_json, "r") as fd:
                logging.config.dictConfig(json.load(fd))
        else:
            print("self.lf_logg_config not set")
            exit(1)
        # print(logger.getEffectiveLevel())
