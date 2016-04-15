#! /usr/bin/env python
from __future__ import print_function

import os
import sys

import pandas


def concat_files(files):
    chunks = pandas.concat([pandas.read_table(f) for f in files])
    chunks.to_csv(sys.stdout, sep=' ', index=False)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='+', help='Files to concatenate')

    args = parser.parse_args()

    concat_files(args.file)


if __name__ == '__main__':
    main()
