=====================
gpsdio sorting plugin
=====================


.. image:: https://travis-ci.org/SkyTruth/gpsdio-csv.svg?branch=master
    :target: https://travis-ci.org/SkyTruth/gpsdio-csv


.. image:: https://coveralls.io/repos/SkyTruth/gpsdio-csv/badge.svg?branch=master
    :target: https://coveralls.io/r/SkyTruth/gpsdio-csv


A driver plugin for `gpsdio <https://github.com/skytruth/gpdsio/>`_ that reads and writes messages in CSV format.


Installing
----------

Via pip:

.. code-block:: console

    $ pip install gpsdio-csv

From master:

.. code-block:: console

    $ git clone https://github.com/SkyTruth/gpsdio-csv
    $ cd gpsdio-csv
    $ pip install .


Developing
----------

.. code-block::

    $ git clone https://github.com/SkyTruth/gpsdio-csv
    $ cd gpsdio-csv
    $ virtualenv venv && source venv/bin/activate
    $ pip install -e .[test]
    $ py.test tests --cov gpsdio_csv --cov-report term-missing
