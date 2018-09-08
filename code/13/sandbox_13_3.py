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


class Typed(object):
    expected_type = object

    def __init__(self, name=None):
        self.name = name

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected {}'.format(self.expected_type))
        instance.__dict__[self.name] = value

class Integer(Typed):
    expected_type = int

class Float(Typed):
    expected_type = float

class String(Typed):
    expected_type = str

class Holding(object):
    name = String('name')
    date = String('date')
    shares = Integer('shares')
    price = Float('price')

    def __init__(self, name, date, shares, price):
        self.name = name
        self.date = date
        self.shares = shares
        self.price = price


# Using decorator to provide name detail
def typed(cls):
    for key, value in vars(cls).items():
        if isinstance(value, Typed):
            # print("key: ", key, " value: ", value)
            value.name = key
    return cls

@typed
class Holding2(object):
    name = String()
    date = String()
    shares = Integer()
    price = Float()

    def __init__(self, name, date, shares, price):
        self.name = name
        self.date = date
        self.shares = shares
        self.price = price


# Using the metaclass to fill in Holding class details
class AttributeValidationMeta(type):
    def __new__(meta, name, bases, metchods):
        cls = super().__new__(meta, name, bases, metchods)
        cls = typed(cls)    # Applying typed decorator
        return cls


class AttributeValidation(metaclass=AttributeValidationMeta):
    pass


class Holding3(AttributeValidation):
    name = String()
    date = String()
    shares = Integer()
    price = Float()

    def __init__(self, name, date, shares, price):
        self.name = name
        self.date = date
        self.shares = shares
        self.price = price


# Allowed attribute checking system
def typed_new(cls):
    cls._attributes = set()
    for key, value in vars(cls).items():
        if isinstance(value, Typed):
            value.name = key
            cls._attributes.add(key)
    return cls


class AttributeValidationMeta_new(type):
    def __new__(meta, name, bases, methods):
        cls = super().__new__(meta, name, bases, methods)
        cls = typed_new(cls)    # Apply a class decorator
        return cls


class AttributeValidation_new(metaclass=AttributeValidationMeta_new):
    def __setattr__(self, name, value):
        # Checking allowed attributes
        if name not in self._attributes:
            raise AttributeError('No attribute {}'.format(name))
        super().__setattr__(name, value)


class Holding4(AttributeValidation_new):
    name = String()
    date = String()
    shares = Integer()
    price = Float()

    def __init__(self, name, date, shares, price):
        self.name = name
        self.date = date
        self.shares = shares
        self.price = price


if __name__ == '__main__':

    parser = configure_arg_parser()
    arguments = parser.parse_args()

    if arguments.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    # Descriptor based type checking system
    holding = Holding('IBM', '11.12.2017', 11, 55.1)
    print(holding.name, holding.price)

    # Filling it the name details with help of cls decorator
    holding2 = Holding2('TESCO', '30.12.2017', 1121, 434.0)
    print(holding2.name, holding2.price)

    # Filling it the class details with help of mataclass
    holding3 = Holding3('COM', '30.12.2017', 1121, 434.0)
    print(holding3.name, holding3.price)

    # Checks 'allowed attribute checking system'
    holding4 = Holding4('PIR', '30.12.2017', 1121, 43094.0)
    print(holding4.name, holding4.price)
    # holding4.fake = 33
