#!/usr/bin/env python3

import sys
import os
import logging
import importlib

import time
import importlib

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../../")))
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")
lf_sublogger = importlib.import_module("py-scripts.sandbox.lf_sublogger")


logger = logging.getLogger(__name__)

# example from
# https://gist.github.com/timss/8f03ae681256f21e25f8b0a16327c26c

# another example for using JSON config
# https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/

# loggers hierarchy and log record propagation
# https://stackoverflow.com/questions/50301613/logging-in-python-with-json-configuration-things-get-logged-more-than-once

# root logger compared to named logger
# https://stackoverflow.com/questions/4150148/logging-hierarchy-vs-root-logger

# http://stackoverflow.com/a/24956305/1076493
# filter messages lower than level (exclusive)
class lf_local_log_method:
    def __init__(self):
        # test the local logging
        pass

    def log_local(self):
        logger.debug("A DEBUG message from " + __name__)
        logger.info("An INFO message from " + __name__)
        logger.warning("An WARNING message from " + __name__)
        logger.error("An ERROR message from + " + __name__)
        logger.critical("An CRITICAL message from + " + __name__)

def main():

    # Configure the logging class to configure the root logger 
    # properties
    logger_config = lf_logger_config.lf_logger_config()

    # Example of setting the level to debug for base config
    logger_config.set_level_debug()

    # example of different time stap
    # logger_config.set_asctime()
    logger.info("An INFO message asctime from " + __name__)
    logger.error("An ERROR message asctime from " + __name__)

    # Example of setting up 

    # Example to read the json config
    # set the configuration file 
    logger_config.lf_logger_config_json = "../lf_logger_config.json"
    logger_config.load_lf_logger_config()

    logger.info("An INFO message asctime from " + __name__)
    logger.error("An ERROR message asctime from " + __name__)

    # This design patter is here just for completeness 
    # please use the json configuration for individual
    # module sets
    # example to set level for module - try to use the json
    # logging.getLogger('sublog').setLevel(logging.ERROR)
    # set level for lower level module
    # logging.getLogger('sublog2').setLevel(logging.ERROR)
    # bogus logger.

    # Example does not fail if logger not present
    logging.getLogger('sublog3_pepper').setLevel(logging.ERROR)
    
    lf_sublogger.sublogger()

    # check local logging
    lf_local_log = lf_local_log_method()
    lf_local_log.log_local()

    # check printing to stderr is caught
    print("stderr - Test", file=sys.stderr)

    sys.exit(1)

if __name__ == '__main__':
    main()

