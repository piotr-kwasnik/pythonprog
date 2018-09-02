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


# using closure functions to perform type checking
def typed_property(name, expected_type):
    private_name = '_' + name

    @property
    def property_generator(self):
        logging.debug('Running getter property generator for: {}'.format(name))
        return getattr(self, private_name)

    @property_generator.setter
    def property_generator(self, value):
        logging.debug('Running setter property generator for: {}'.format(name))
        if isinstance(value, expected_type):
            setattr(self, private_name, value)
        else:
            raise TypeError('Expected type for {}: {}'.format(name, expected_type))

    return property_generator


class Point(object):

    position_x = typed_property('position_x ', int)
    position_y = typed_property('position_y ', int)

    def __init__(self, x, y):
        self.position_x = x
        self.position_y = y


Integer = lambda name: typed_property(name, int)
Float = lambda name: typed_property(name, float)
String = lambda name: typed_property(name, str)


class Point2(object):

    position_x = Integer('position_x')
    position_y = Integer('position_y')

    # print(repr(position_y))
    # print(type(position_y))

    def __init__(self, x, y):
        self.position_x = x
        self.position_y = y


if __name__ == '__main__':

    parser = configure_arg_parser()
    arguments = parser.parse_args()

    if arguments.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    # checking basic usage of closure functions
    # delay(3, hello)
    # delay(3, add(3, 4))

    # checking type checking with closure functions
    # first_point = Point(1, 4)
    # first_point = Point(1, '4')
    second_point = Point2(1, 4)
    # second_point = Point2(1, '4')

