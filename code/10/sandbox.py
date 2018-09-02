#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 20:38:50 2018

@author: pio
"""

import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] >>> %(message)s')


# Type validation with property getter and setter in use
class Point(object):

    def __init__(self, x, y):
        self.position_x = x
        self.position_y = y

    @property
    def position_x(self):
        logging.debug('Getting position_x')
        return self._position_x

    @position_x.setter
    def position_x(self, new_x):
        logging.debug('Setting x variable...')
        if isinstance(new_x, int):
            self._position_x = new_x
        else:
            raise TypeError('x needs to be an int')

    @property
    def position_y(self):
        logging.debug('Getting position_y')
        return self._position_y

    @position_y.setter
    def position_y(self, new_y):
        logging.debug('Setting x variable...')
        if isinstance(new_y, int):
            self._position_y = new_y
        else:
            raise TypeError('y needs to be an int')


# Type validation with __setattr__
# Creating constant set of attributes
class Point2(object):

    def __init__(self, x, y):
        self.position_x = x
        self.position_y = y

    def __getattr__(self, item):
        logging.debug('There is no attribute {}'.format(item))

    def __setattr__(self, key, value):
        if key in {'position_x', 'position_y'}:
            if not isinstance(value, int):
                raise TypeError('Point2(): atribute {} needs to be an int type...'.format(key))

        if key not in {'position_x', 'position_y'}:
            raise AttributeError('No attribute: {}'.format(key))

        super().__setattr__(key, value)


# read only wrapper
class ReadOnly(object):

    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, item):
        return getattr(self._obj, item)

    def __setattr__(self, key, value):
        if key == '_obj':
            super().__setattr__(key, value)
        else:
            raise AttributeError('The {} is read only...'.format(key))


# descriptor based type checking system

class Typed(object):
    expected_type = object

    def __init__(self, name):
        # logging.debug('init for {} object'.format(self.expected_type))
        self.name = name

    def __get__(self, instance, owner):
        # logging.debug(str(instance.__dict__))
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if isinstance(value, self.expected_type):
            instance.__dict__[self.name] = value
        else:
            raise TypeError('Expected {} type for {}'.format(self.expected_type, self.name))


class Integer(Typed):
    expected_type = int


class Float(Typed):
    expected_type = float


class String(Typed):
    expected_type = str


class Point3(object):

    name = String('name')
    value = Float('value')
    position_x = Integer('position_x')
    position_y = Integer('position_y')

    def __init__(self, name, value, x, y):
        self.name = name
        self.value = value
        self.position_x = x
        self.position_y = y


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    first_point = Point(11, 33)
    print('first_point position_x value: {}'.format(first_point.position_x))
    print('first_point position_y value: {}'.format(first_point.position_y))
    # Checking int validation
    # first_point = Point('11', 33)

    second_point = Point2(22, 44)
    print('second_point position_x value: {}'.format(second_point.position_x))
    print('second_point position_y value: {}'.format(second_point.position_y))
    # Checking int validation
    # second_point = Point2('11', 4)
    # Checking assignment of non-existing attribute
    # second_point.position_z = 111

    third_point = Point3('secret position', 44.11, 444, 111)
    print('third_point position_x value: {}'.format(third_point.position_x))
    print('third_point position_y value: {}'.format(third_point.position_y))
    # Checking validation
    # third_point = Point3('secret position', 44.11, 444, '111')
    # third_point = Point3('secret position', 44, 444, 111)
    # third_point = Point3(111, 44.11, 444, 111)


    # Check read only wrapper
    read_only = ReadOnly(Point2(33, 44))
    print('read_only position_x value: {}'.format(read_only.position_x))
    print('read_only position_y value: {}'.format(read_only.position_y))
    # read_only.position_x = 111
