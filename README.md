# sil
Python scripts for crunching data for the Stable Isotope Lab

## Extract data lines from a file

The following gets just the first 10000 data rows from a data set and
writes them to a new file.

    $ python pick_rows.py 0-9999 < WAIS06AData_icedata.txt > output.txt

Because `pick_rows.py` reads in the entire data set, in this particular case
the following would be faster (and equivalent),

    $ head -n 10001 WAIS06AData_icedata.txt > output.txt

However, `pick_rows.py` can take more complicated ranges. For example,

    $ python pick_rows.py 100-200,300-400 1000-10000 < WAIS06AData_icedata.txt

