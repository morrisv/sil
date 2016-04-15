#! /usr/bin/env python
from __future__ import print_function

import sys

import numpy as np
import pandas
import matplotlib as mpl

mpl.use('Qt4Agg')

import matplotlib.pyplot as plt


class PointGetter(object):
    def __init__(self, file=None):
        self._file = file or sys.stdout
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.shift_is_held = False

        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('key_release_event', self.on_key_release)

    def on_pick(self, event):
        if self.shift_is_held:
            this_line = event.artist
            xdata, ydata = this_line.get_xdata(), this_line.get_ydata()
            ind = event.ind[0]
            # print('{x}, {y}'.format(x=xdata[ind], y=ydata[ind]),
            print('{x}'.format(x=xdata[ind]), file=self._file)

    def on_key_press(self, event):
        if event.key == 'shift':
            self.shift_is_held = True

    def on_key_release(self, event):
        if event.key == 'shift':
            self.shift_is_held = False


def read_data_chunk(path, start=0, nrows=5000):
    header = pandas.read_table(path, nrows=0)
    data = pandas.read_table(path, skiprows=start + 1,
                             nrows=nrows, names=header.columns)
    return data


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Text data file')
    parser.add_argument('output', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout, help='Output file')
    parser.add_argument('--nrows', type=int, default=5000,
                        help='Number of rows to read')
    parser.add_argument('--start', type=int, default=0, help='Chunk to read')

    args = parser.parse_args()

    data = read_data_chunk(args.file, start=args.start, nrows=args.nrows)

    y = data.d18o
    x = np.arange(args.start, args.start + len(y))

    pg = PointGetter(file=args.output)
    pg.ax.plot(x, y, 'o', picker=5)
    pg.ax.set_title('Shift-click to select points')

    plt.show()


if __name__ == '__main__':
    main()
