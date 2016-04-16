# sil
Python scripts for crunching data for the Stable Isotope Lab

## Requirements

* pandas 0.18.0
* numexpr 2.5.2
* matplotlib 1.4.3

All of the python scripts read a tabular text file, do something to it, and
writes out a new table, in the same format, to stdout. The input data file is
read through stdin or specified as a file name using the `--data` option.

All commands also accept a `-h` option that prints a brief help message and
exits.

## Examples

Following are some simple examples that use the scripts in the `scripts` folder.
These examples should be executed from within the `scripts` folder.

### Extract data lines from a file

The following gets just the first 10000 data rows from a data set and
writes them to a new file.

    $ python pick_rows.py 0-9999 < WAIS06AData_icedata.txt > output.txt

Because `pick_rows.py` reads in the entire data set, in this particular case
the following would be faster (and equivalent),

    $ head -n 10001 WAIS06AData_icedata.txt > output.txt

However, `pick_rows.py` can take more complicated ranges. For example,

    $ python pick_rows.py 100-200,300-400 1000-10000 < WAIS06AData_icedata.txt
    > output.txt

### Flag rows

Ranges of rows are provided in the same way as with `pick_rows.py` and,
as with `pick_rows.py`, can also be given in a file. The file must contain
a series of ranges, one per line. The following will add the flag `A` to
the given rows (if a `flags` columns doesn't exists, it will be added).

    $ python pick_rows.py 100-200 --file=rows.txt --flag=A < WAIS06AData_icedata.txt > output.txt

The contents of `rows.txt` could be the following::

  300-400
  1000-10000

### Select rows by a query string

Use `query_rows.py` to pick rows based on a logical expression. For example,
the following selects rows that contain an `A` in their `flags` column.

    $ python query_rows.py '"A" in flags' < data_with_flags.txt

Just for fun, here is an example of how you could create the above
`data_with_flags.txt` file.

    $ python flag_rows.py --flag=x < ../data/test_icedata.txt > tmp.txt
    $ python flag_rows.py 100-200 --flag=A < tmp.txt > data_with_flags.txt
    $ python query_rows.py '"A" in flags' < data_with_flags.txt

The first command adds a `flags` column to every row and sets its value to `x`.
The second sets the flags value for rows 100 to 200 (inclusive) to `A`. The
third selects just those rows whose flags contain an `A`.

### Pick points from a graph

You can graphically pick ranges of points (or single points) from a graph with
`pick_points.py`. For example,

    $ python pick_points.py ../data/test_icedata.txt

display the data of `d18o` as points. To choose a range hold down the shift key
and click on two points. The range will be printed to the screen (or, if
specified, a file). Note that you can use these ranges as-is to feed into other
scripts that takes ranges, like `flag_rows.py` or `pick_rows.py`.

If the data file is large, you may want to just look at a portion of it. To do
this, use the `--nrows` and `--start` options to set the start row and the
number of rows to plot.

### Chunk a large file into smaller ones

To divide a large data file into smaller files use `chunk.py`. To following
divides a file into files with 1000 lines each.

    $ python chunk.py --nrows=1000 < ../data/test_icedata.txt

### Concatenate files into a single file

The reverse of `chunk.py`. Concatenate many smaller files into a single file.

    $ python concat.py file.txt file2.txt > big_file.txt
