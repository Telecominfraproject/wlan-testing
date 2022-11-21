#!/usr/bin/env python3
import sys
import logging
import importlib

logger = logging.getLogger(__name__)
logger_http = logging.getLogger(__name__ + ".http")
logger_json = logging.getLogger(__name__ + ".json")

def sublogger():
    logger.debug("A DEBUG message from " + __name__)
    logger.info("An INFO message from " + __name__)
    logger.warning("An WARNING message from " + __name__)
    logger.error("An ERROR message from + " + __name__)
    logger.critical("An CRITICAL message from + " + __name__)


def sublogger_2a():
    logger_http.debug("A DEBUG message")
    logger_json.debug("A DEBUG message")
    logger_http.info("An INFO message ")
    logger_json.info("An INFO message ")
    logger_http.warning("An WARNING message")
    logger_json.warning("An WARNING message")
    logger_http.error("An ERROR message ")
    logger_json.error("An ERROR message ")
    logger_http.critical("An CRITICAL message")
    logger_json.critical("An CRITICAL message")

