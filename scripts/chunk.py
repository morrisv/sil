#! /usr/bin/env python
from __future__ import print_function

import os
import sys
import shutil
import re
import glob

import pandas

from utils import dataframe_to_csv


CHUNK_FILE_RE = '(?P<base>\w*)_(?P<start>[0-9]+)_(?P<stop>[0-9]+).txt'
CHUNK_FILE_PATTERN = re.compile(CHUNK_FILE_RE)


def get_chunk_key(lines, width=None):
    if width is None:
        fmt = 'd'
    else:
        fmt = '0{width:d}d'.format(width=width)
    start = ('{lineno:' + fmt + '}').format(lineno=lines[0])
    stop = ('{lineno:' + fmt + '}').format(lineno=lines[1])

    return '{start}_{stop}'.format(start=start, stop=stop)


def get_chunk_file_name(path, lines, width=None):
    fname = os.path.basename(path)
    (base, ext) = os.path.splitext(fname)

    key = get_chunk_key(lines, width=width)

    return base + '_{key}'.format(key=key) + ext


def parse_chunk_name(fname):
    match = CHUNK_FILE_PATTERN.match(fname)
    if match:
        return (match.groupdict()['base'],
                match.groupdict()['start'],
                match.groupdict()['stop'])
    else:
        return None


def alphabetize_chunk_files(base):
    """Rename data chunk files so the alphabetize in chunk-order.

    Parameters
    ----------
    base : str
        Base name for the chunk files.

    Returns
    -------
    list of str
        List of the new chunk file names.
    """
    (base, ext) = os.path.splitext(base)

    names = []
    for name in glob.glob('{base}*{ext}'.format(base=base, ext=ext)):
        try:
            names.append(parse_chunk_name(name))
        except ValueError:
            pass

    max_width = max([len(parts[2]) for parts in names])

    sources = ['_'.join(parts) + ext for parts in names]
    dests = [get_chunk_file_name(base + ext,
                                 (int(parts[1]), int(parts[2])),
                                 width=max_width) for parts in names]

    for src, dest in zip(sources, dests):
        shutil.move(src, dest)

    return dests


def chunk_data(path, chunksize):
    """Divide a large data file into smaller chunks.

    Parameters
    ----------
    path : str
        Path to the data file.
    chunksize : int
        Number of data lines per chunk.

    Returns
    -------
    list of str
        List of the new chunk file names.
    """
    reader = pandas.read_table(path, chunksize=chunksize, skiprows=0)

    start = 0
    for chunk in reader:
        stop = start + len(chunk) - 1
        dataframe_to_csv(chunk, file=get_chunk_file_name(path, (start, stop)))
        start = stop + 1

    return alphabetize_chunk_files(os.path.basename(path))


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=argparse.FileType('r'),
                        default=sys.stdin, help='Text data file')
    parser.add_argument('--nrows', type=int, default=5000,
                        help='Number of rows per chunk')

    args = parser.parse_args()

    print(os.linesep.join(chunk_data(args.data, args.nrows)))


if __name__ == '__main__':
    main()
