========================
binance_historical_data
========================

.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/binance_historical_data
   :target: https://img.shields.io/github/last-commit/stas-prokopiev/binance_historical_data
   :alt: GitHub last commit

.. image:: https://img.shields.io/github/license/stas-prokopiev/binance_historical_data
    :target: https://github.com/stas-prokopiev/binance_historical_data/blob/master/LICENSE.txt
    :alt: GitHub license<space><space>

.. image:: https://img.shields.io/pypi/v/binance_historical_data
   :target: https://img.shields.io/pypi/v/binance_historical_data
   :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/binance_historical_data
   :target: https://img.shields.io/pypi/pyversions/binance_historical_data
   :alt: PyPI - Python Version


.. contents:: **Table of Contents**

Short Overview.
=========================
binance_historical_data is a python package (**py>=3.7**)
which makes dumping of historical crypto data from binance server as simple as possible.
**You don't even need to have an account at binance.com to dump all history of crypto data**


| Using this package you will be able to have full binance historical data with only 3 lines of python code
| And if you need to update already dumped data then once again 3 lines of python code will do the job

| **Limitations**: The previous day data appear on binance server a few minutes after 0 a.m. UTC
| So there is a delay in which you can get the data.

Installation via pip:
======================

.. code-block:: bash

    pip install binance_historical_data


How to use it
===========================


Init main object: **data_dumper**
-----------------------------------

.. code-block:: python

    from binance_historical_data import CandleDataDumper

    data_dumper = CandleDataDumper(
        path_dir_where_to_dump=".",
        str_data_frequency="1m",
    )

Arguments:

#. **path_dir_where_to_dump**:
    | (string) Path to folder where to dump the historical data
#. **str_data_frequency**:
    | (string) One of [1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h]

The main method to dump data
-----------------------------

.. code-block:: python

    data_dumper.dump_data(
        list_tickers=None,
        date_start=None,
        date_end=None,
        is_to_update_existing=False,
    )

Arguments:

#. **list_tickers=None**:
    | list
    | Trading pairs for which to dump data
    | if equals to None all **USDT** pairs will be used
#. **date_start=None**:
    | datetime.date
    | The date from which to start dump
#. **date_end=True=None**:
    | datetime.date
    | The last date for which to dump data
#. **is_to_update_existing=False**:
    | bool
    | Flag if you want to update data if it's already exists

Examples
===========================

How to dump all data for all USDT trading pairs
------------------------------------------------

Please be advised that the first data dump for all trading pairs might take some time (~40 minutes)

.. code-block:: python

    data_dumper.dump_data()


How to update data dump and get all new data
----------------------------------------------

.. code-block:: python

    data_dumper.dump_data()


How to update (reload) all data for the asked time period
----------------------------------------------------------

.. code-block:: python

    data_dumper.dump_data(
        date_start=datetime.date(year=2021, month=1, day=1),
        date_end=datetime.date(year=2022, month=1, day=1),
        is_to_update_existing=True
    )


How to get all trading pairs (tickers) from binance
----------------------------------------------------

.. code-block:: python

    print(data_dumper.get_list_all_trading_pairs())


Links
=====

    * `PYPI <https://pypi.org/project/binance_historical_data/>`_
    * `GitHub <https://github.com/stas-prokopiev/binance_historical_data>`_

Project local Links
===================

    * `CHANGELOG <https://github.com/stas-prokopiev/binance_historical_data/blob/master/CHANGELOG.rst>`_.
    * `CONTRIBUTING <https://github.com/stas-prokopiev/binance_historical_data/blob/master/CONTRIBUTING.rst>`_.

Contacts
========

    * Email: stas.prokopiev@gmail.com
    * `vk.com <https://vk.com/stas.prokopyev>`_
    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_

License
=======

This project is licensed under the MIT License.