#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import argparse
import os
import time
import csv

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


def counter(number):
    while number > 0:
        yield number
        number -= 1


class Counter(object):

    def __init__(self, number):
        self.number = number

    def __iter__(self):
        n = self.number
        while n > 0:
            yield n
            n -= 1


def gen_basics():
    number = 3

    # generator implemented in function, produce output on first call
    gen_func = counter(number)
    print('\nGenerator funct 1st call:')
    for x in gen_func:
        print(x)
    print('\nGenerator funct 2nd call:')
    for x in gen_func:
        print(x)

    # generator implemented in class, might be called many times
    print('\nGenerator class 1st call:')
    gen_class = Counter(number)
    for x in gen_class:
        print(x)
    print('\nGenerator class 2nd call:')
    for x in gen_class:
        print(x)


def follow_file_simple():
    """
    Following file without generator
    """
    print('\nFollowing the file ../Data/stocklog.csv')
    with open('../Data/stocklog.csv', 'r') as f:
        f.seek(0, os.SEEK_END)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue

            row = line.split(',')
            change = float(row[4])
            if change < 0:
                name = row[0]
                price = float(row[1])
                print('{:>10s} {:>10.2f} {:>10.2f}'.format(name, price, change))


# follow file generator
def follow(file_name):
    print('\nFollowing the file {}'.format(file_name))
    with open(file_name, 'r') as f:
        f.seek(0, os.SEEK_END)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line


def follow_file_with_generator():
    """
    Following file with generator
    """

    for line in follow('../Data/stocklog.csv'):
        row = line.split(',')
        change = float(row[4])
        if change < 0:
            name = row[0]
            price = float(row[1])
            print('{:>10s} {:>10.2f} {:>10.2f}'.format(name, price, change))


def grep(names, rows):
    for row in rows:
        if row[0] in names:
            yield row


def parse_stock_data(lines):
    rows = csv.reader(lines)
    types = [str, float, str, str, float, float, float, float, int]
    # type conversion, generator in use
    converted = ([func(val) for func, val in zip(types, row)]
                 for row in rows)

    return converted


if __name__ == '__main__':

    parser = configure_arg_parser()
    arguments = parser.parse_args()

    if arguments.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    #  Generator basics
    # gen_basics()

    #  watching real time data without generator
    # follow_file_simple()

    #  watching real time data with generator
    # follow_file_with_generator()

    # pipeline example:
    lines = follow('../Data/stocklog.csv')
    rows = parse_stock_data(lines)
    matching = grep({'TEST', 'TEST2'}, rows)
    negchange = (row for row in matching if row[4] < 0)
    for row in negchange:
        name = row[0]
        price = row[1]
        change = row[4]
        print('{:>10s} {:>10.2f} {:>10.2f}'.format(name, price, change))

