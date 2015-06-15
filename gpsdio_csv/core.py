#!/usr/bin/env python


"""
Core components for gpsdio_csv
"""


import gpsdio.drivers
import csv
import json
import six
from codecs import open as codecs_open

class Csv(gpsdio.drivers.BaseDriver):
    """ A driver for CSV files.

    Arguments:

        cols="colname1,colname2...,colnameN"

    "cols" is the list of columns to add to the CSV file when writing.
    The default column list is available in Csv.cols.

    Default value for cols is

        type,mmsi,timestamp,lon,lat,heading,turn,course,speed,extra

    If a column called "extra" is specified when writing, any columns
    not in the column list will be put in a JSON object serialized
    into that column. If such a column is present when reading the
    JSON object is unpacked and incorporated into the message.
    """


    driver_name = 'CSV'
    extensions = ('csv',)
    modes = ('r', 'w')
    compression = False

    # Default columns to write
    cols = ["type", "mmsi", "timestamp", "lon", "lat", "heading", "turn", "course", "speed", "extra"]

    class _CsvWriter(object):
        def __init__(self, f, cols=[], **kwargs):
            self._f = f
            self._cols = cols
            self._writer = csv.DictWriter(f, cols, **kwargs)
            self._writer.writeheader()

        def convert_row(self, row):
            out = {}
            for col in self._cols:
                if col in row:
                    out[col] = row.pop(col)

            if 'extra' in self._cols:
                out["extra"] = json.dumps(row)

            return out

        def write(self, msg):
            self._writer.writerow(self.convert_row(msg))

        def __getattr__(self, item):
            return getattr(self._f, item)

    class _CsvReader(object):
        def __init__(self, f, **kwargs):
            self._f = f
            self._reader = csv.DictReader(f, **kwargs)

        def __iter__(self): return self

        def next(self):
            res = self._reader.next()
            res.update(json.loads(res.pop('extra', '{}')))
            # CSV casts everything to string, so we have to fix that
            res = gpsdio.schema.export_msg(gpsdio.schema.import_msg(res, skip_failures=True, cast_values=True))
            return res

        def __getattr__(self, item):
            return getattr(self._f, item)

    def __init__(self, f, mode='r', cols=None, **kwargs):
        """Arguments:

            f: An open file object to read or write to/from
            mode: 'r' or 'w' weither to read or write
            cols: a list of column names (as strings) to write
        """ 

        if isinstance(cols, six.string_types):
            cols = cols.split(",")
        if isinstance(f, six.string_types):
            self._f = codecs_open(f, mode=mode)
        else:
            self._f = f
        if cols is None:
            cols = self.cols
        if mode == 'r':
            driver = self._CsvReader(self._f, **kwargs)
        else:
            driver = self._CsvWriter(self._f, cols, **kwargs)
        gpsdio.drivers.BaseDriver.__init__(self, driver)

# Plugin main function that does nothing
def gpsdio_csv(*arg, **kw):
    pass
