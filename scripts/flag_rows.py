#! /usr/bin/env python
from __future__ import print_function

import os
import sys

import numpy as np
import pandas

from utils import dataframe_to_csv, expand_ranges


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=argparse.FileType('r'),
                        default=sys.stdin, help='Text data file')
    parser.add_argument('rows', nargs='*', help='Rows to flag')
    parser.add_argument('--file', type=argparse.FileType('r'), default=[],
                        help='File containing ranges')
    parser.add_argument('--flag', help='Flag to add')

    args = parser.parse_args()

    data = pandas.read_table(args.data)

    rows = expand_ranges(args.rows) + expand_ranges(args.file)
    if rows:
        data.loc[rows, 'flags'] = args.flag
    else:
        data.loc[:, 'flags'] = args.flag

    dataframe_to_csv(data)


if __name__ == '__main__':
    main()
