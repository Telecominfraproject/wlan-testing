#!/usr/bin/python3

import logging
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug',
                        type=int,
                        default=2,
                        help="Set logging level, range 0 through 4. 0 is DEBUG, 4 is CRITICAL")

    args = parser.parse_args()
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    logging.basicConfig(level=levels[args.debug])

    logging.debug('This is debug output, level 0')
    logging.info('This is info output, level 1')
    logging.warning('This is warning output, level 2')
    logging.error('This is error output, level 3')
    logging.critical('This is error output, level 4')


if __name__ == "__main__":
    main()