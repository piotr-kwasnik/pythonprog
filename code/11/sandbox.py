#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
import argparse

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] >>> %(message)s')


def configure_arg_parser():
    """
    Configure command line argument parser
    """

    arg_parser = argparse.ArgumentParser(description='Default {} argparse'.format(__name__),)

    arg_parser.add_argument('-d', '--debug',
                            action='store_true',
                            required=False,
                            help='enable debug mode')

    arg_parser.add_argument('-n', '--dry_run',
                            action='store_true',
                            required=False,
                            help='enable dry run mode')

    return arg_parser


def hello():
    print('Hello World!')


def delay(secs, func):
    logging.debug('Delaying {}() function call by {} secs'.format(func.__name__, secs))
    time.sleep(secs)
    func()


# making use of closure functions to enclose environment so it could be used as delay argument
def add(x, y):
    def do_add():
        logging.debug('Adding {} + {} -> {}'.format(x, y, x+y))
        return x + y
    return do_add


if __name__ == '__main__':

    parser = configure_arg_parser()
    arguments = parser.parse_args()

    if arguments.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    delay(3, hello)
    delay(3, add(3, 4))
