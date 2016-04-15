#! /usr/bin/env python
import sys
import types

import pandas


def read_data_chunk(path, start=0, nrows=5000):
    """Read rows from a data table.
    
    Parameters
    ----------
    path : str
        Path to a data file.
    start : int, optional
        Data row number to start reading from.
    nrows : int, optional
        Number of rows to read.

    Returns
    -------
    DataFrame
        The chunk of data read.
    """
    header = pandas.read_table(path, nrows=0)
    return pandas.read_table(path, skiprows=start + 1,
                             nrows=nrows, names=header.columns)


def dataframe_to_csv(data, file=None):
    """Write a DataFrame as WAIS data file.

    Parameters
    ----------
    data : A DataFrame
        A pandas DataFrame to write.
    file : str or file_like, optional
        File to write data to.
    """
    file = file or sys.stdout

    data.to_csv(file, sep='\t', index=False)


def parse_range_string(range_str):
    """Expand a range string to a list of integers.

    Parameters
    ----------
    range_str : str
        A string indicating a range of integers.

    Returns
    -------
    list of int
        A list on integers contains within the given range.

    Examples
    --------
    >>> parse_range_string('2-6')
    [2, 3, 4, 5, 6]
    >>> parse_range_string('2')
    [2]
    """
    try:
        low, high = range_str.split('-')
    except ValueError:
        if range_str == '':
            return []
        else:
            return [int(range_str)]
    else:
        return range(int(low), int(high) + 1)


def expand_ranges(ranges):
    """Parse a string or iterable for a series of ranges.

    Parameters
    ----------
    ranges : str or list of str
        A list of range strings or a comma-separated list or ranges.

    Returns
    -------
    list of int
        A list on integers contains within the given ranges.

    Examples
    --------
    >>> expand_ranges('2-5,7-10')
    [2, 3, 4, 5, 7, 8, 9, 10]
    >>> expand_ranges(['2-5', '7-10'])
    [2, 3, 4, 5, 7, 8, 9, 10]
    >>> expand_ranges(['2-4,5', '7-10'])
    [2, 3, 4, 5, 7, 8, 9, 10]
    """
    if isinstance(ranges, types.StringTypes):
        ranges = ranges.split(',')
    else:
        return expand_ranges(','.join(ranges))

    all_ints = []
    for range in ranges:
        all_ints += parse_range_string(range)

    return all_ints
