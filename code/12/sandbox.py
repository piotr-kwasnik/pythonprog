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


# Decorator
def logged(func):
    """
    adds logging to passed function

    :param funct:
    :return: wrapped function
    """

    # logging.debug('Adding logging to {}'.format(func.__name__))

    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Calling: {}()'.format(func.__name__))
        return func(*args, **kwargs)

    return wrapper


# Decorator with parameters
def logged_formatted(fmt):
    """"
    ads formatter to logging function
    """
    def logged(func):
        """
        adds logging to passed function

        :param funct:
        :return: wrapped function
        """

        # logging.debug('Adding logging to {}'.format(func.__name__))

        @wraps(func)
        def wrapper(*args, **kwargs):
            print(fmt.format(func=func))
            return func(*args, **kwargs)

        return wrapper
    return logged


@logged
def add1(x, y):
    logging.debug('adding: {} + {} -> {}'.format(x, y, x + y))
    return x + y


@logged_formatted('Executing: {func.__name__}()')
def add2(x, y):
    logging.debug('adding: {} + {} -> {}'.format(x, y, x + y))
    return x + y


# changing logged to use logged formated as default
logged = logged_formatted('Function call: {func.__name__}()')


@logged
def add3(x, y):
    logging.debug('adding: {} + {} -> {}'.format(x, y, x + y))
    return x + y


@logged
def add4(x, y):
    logging.debug('adding: {} + {} -> {}'.format(x, y, x + y))
    return x + y


if __name__ == '__main__':

    parser = configure_arg_parser()
    arguments = parser.parse_args()

    if arguments.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    # Checking logged decorator
    add1(5, 6)
    # Checking logged_formatter decorator
    add2(5, 6)
    # Checking logged set as logged_formatter decorator
    add3(5, 6)
    add4(5, 6)

