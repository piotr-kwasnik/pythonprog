#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import argparse

from functools import wraps


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


def logged(func):
    """
    adds logging to passed function

    :param funct:
    :return: wrapped function
    """

    logging.debug('Adding logging to {}'.format(func.__name__))

    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Calling: {}()'.format(func.__name__))
        return func(*args, **kwargs)

    return wrapper


@logged
def add(x, y):
    logging.debug('adding: {} + {} -> {}'.format(x, y, x + y))
    return x + y


if __name__ == '__main__':

    parser = configure_arg_parser()
    arguments = parser.parse_args()

    if arguments.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


    add(5, 6)

