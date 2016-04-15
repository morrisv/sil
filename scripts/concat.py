#! /usr/bin/env python
from __future__ import print_function

import os
import sys

import pandas

from utils import dataframe_to_csv


def concat_files(files):
    chunks = pandas.concat([pandas.read_table(f) for f in files])
    dataframe_to_csv(chunks)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='+', help='Files to concatenate')

    args = parser.parse_args()

    concat_files(args.file)


if __name__ == '__main__':
    main()
