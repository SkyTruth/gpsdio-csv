"""
Unittests for `gpsdio_csv.core`.
"""


import tempfile
import gpsdio
import csv
import datetime
import os.path
import json
import random

def randdate():
    return datetime.datetime(
        2014, 1+int(12*random.random()),
        1+int(28*random.random()),
        int(24*random.random()),
        int(60*random.random()),
        int(60*random.random())
        )

def cleanup():
    if os.path.exists('in.msg'):
        os.unlink('in.msg')
    if os.path.exists('out.msg'):
        os.unlink('out.msg')


def test_sort():
    cleanup()
    try:
        with gpsdio.open("test.csv", "w") as f:
            for i in range(0, 1000):
                f.writerow({'timestamp': randdate(), 'lat': 180*random.random()-90.0, 'lon': 360*random.random()-180.0, 'foo': 4711})

        with open("test.csv") as f:
            for row in csv.DictReader(f):
                assert 'timestamp' in row
                assert 'lat' in row
                assert 'lon' in row
                assert 'extra' in row
                extra = json.loads(row['extra'])
                assert 'foo' in extra

        with gpsdio.open('test.csv') as f:
            for row in f:
                print row
                assert isinstance(row['timestamp'], datetime.datetime)
                assert isinstance(row['lat'], float)
                assert 'foo' in row

    finally:
        cleanup()
