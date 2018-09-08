#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import argparse
import sys

import holding

from abc import ABC, ABCMeta, abstractmethod

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


def print_table(objects, colnames, formatter):
    """
    Make a nicely formatted table showing attributes from a list of objects
    """

    if not isinstance(formatter, TableFormatter):
        raise TypeError('formatter must be a TableFormatter')

    formatter.headings(colnames)
    for obj in objects:
        rowdata = [str(getattr(obj, colname)) for colname in colnames]
        formatter.row(rowdata)


_formatters = {}


# small factory
def create_formatter(name):
    formatter = _formatters.get(name)
    if not formatter:
        raise ValueError('Unknown format {}\n'
                         'Implemented formatters: {}'.
                         format(name, str(list(_formatters.keys()))))
    return formatter()


# Metaclass to auto-register formatters
class TableMeta(ABCMeta):

    def __init__(cls, clsname, bases, methods):
        super().__init__(clsname, bases, methods)
        if hasattr(cls, 'name'):
            _formatters[cls.name] = cls


# Using metaclass to auto-register to _formatters
class TableFormatter(metaclass=TableMeta):
    def __init__(self, outfile=None):
        if outfile is None:
            outfile = sys.stdout
        self.outfile = outfile

    # Serves a design spec for making tables (use inheritance to customize)
    @abstractmethod
    def headings(self, headers):
        pass

    @abstractmethod
    def row(self, rowdata):
        pass


class TextTableFormatter(TableFormatter):
    name = 'text'

    def __init__(self, outfile=None, width=10):
        super().__init__(outfile)  # Initialize parent
        self.width = width

    def headings(self, headers):
        for header in headers:
            print('{:>{}s}'.format(header, self.width), end=' ', file=self.outfile)
        print(file=self.outfile)

    def row(self, rowdata):
        for item in rowdata:
            print('{:>{}s}'.format(item, self.width), end=' ', file=self.outfile)
        print(file=self.outfile)


class HTMLTableFormatter(TableFormatter):
    name = 'html'

    def headings(self, headers):
        print('<tr>', end='')
        for h in headers:
            print('<th>{}</th>'.format(h), end='')
        print('</tr>')

    def row(self, rowdata):
        print('<tr>', end='')
        for d in rowdata:
            print('<td>{}</td>'.format(d), end='')
        print('</tr>')


class PipeTableFormatter(TableFormatter):
    name = 'pipe'

    def headings(self, headers):
        for h in headers:
            print('{}'.format(h), end='|')
        print()
    def row(self, rowdata):
        for d in rowdata:
            print('{}'.format(d), end='|')
        print()


if __name__ == '__main__':

    parser = configure_arg_parser()
    arguments = parser.parse_args()

    if arguments.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    # Using auto-registered formatter
    formatter = create_formatter('pipe')
    print_table(holding.portfolio, ['name', 'shares', 'price'], formatter)
