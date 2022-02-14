#!/usr/bin/env python3

import sys
import os
import logging
import importlib

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../../")))
lf_sublogger_2 = importlib.import_module("py-scripts.sandbox.lf_sublogger_2")


logger = logging.getLogger(__name__)


def sublogger():
    logger.debug("A DEBUG message from " + __name__)
    logger.info("An INFO message from " + __name__)
    logger.warning("An WARNING message from " + __name__)
    logger.error("An ERROR message from + " + __name__)
    logger.critical("An CRITICAL message from + " + __name__)
    lf_sublogger_2.sublogger()
    logger.error("An ERROR message from + " + __name__)
    lf_sublogger_2.sublogger_2a()
