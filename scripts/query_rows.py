#! /usr/bin/env python
from __future__ import print_function

import sys

import numpy as np
import pandas

from utils import dataframe_to_csv


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=argparse.FileType('r'),
                        default=sys.stdin, help='Text data file')
    parser.add_argument('query', help='Query expression')

    args = parser.parse_args()

    data = pandas.read_table(args.data)
    dataframe_to_csv(data.query(args.query))


if __name__ == '__main__':
    main()
