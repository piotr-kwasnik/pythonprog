#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import argparse

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] >>> %(message)s')


def configure_arg_parser():
    """
    Configure command line argument parser
    """

    arg_parser = argparse.ArgumentParser(description='Default {} argparse'.format(__name__), )

    arg_parser.add_argument('-d', '--debug',
                            action='store_true',
                            required=False,
                            help='enable debug mode')

    arg_parser.add_argument('-dr', '--dry_run',
                            action='store_true',
                            required=False,
                            help='enable dry run mode')

    return arg_parser


class Point1(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        print('Moving point of class: {}'.format(self.__class__.__name__))
        self.x += dx
        self.y += dy


if __name__ == '__main__':

    parser = configure_arg_parser()
    arguments = parser.parse_args()

    if arguments.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    # Basic Point class object
    point1 = Point1(12, 20)
    point1.move(33, 4)

    # Building Point class from scratch
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        print('Moving point of class: {}'.format(self.__class__.__name__))
        self.x += dx
        self.y += dy

    name = "Point2"
    bases = (object, )
    methods = {
        "__init__": __init__,
        "move": move,
    }

    # type(name, bases, dict) -> an ew type
    Point2 = type(name, bases, methods)
    point2 = Point2(55, 66)
    point2.move(11, 70)

    # Metaclass definition
    class MyType(type):
        def __new__(cls, name, bases, methods):
            print('Creating : {}'.format(name))
            print('Bases : {}'.format(bases))
            print('Methods : {}'.format(methods))
            return super().__new__(cls, name, bases, methods)

    Point3 = MyType("Point3", bases, methods)
    point3 = Point3(55, 33)
    point3.move(1, 2)

    # Definition of new class with help of metaclass
    class Point4(metaclass=MyType):

        def __init__(self, x, y):
            self.x = x
            self.y = y

        def move(self, dx, dy):
            print('Moving point of class: {}'.format(self.__class__.__name__))
            self.x += dx
            self.y += dy

    point4 = Point4(11, 22)
    point4.move(1, 2)