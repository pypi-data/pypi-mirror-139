# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['binance_historical_data']

package_data = \
{'': ['*']}

install_requires = \
['char>=0.1.2,<0.2.0',
 'local-simple-database>=0.1.10,<0.2.0',
 'mpire>=2.3.3,<3.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'binance-historical-data',
    'version': '0.1.1',
    'description': '',
    'long_description': '========================\nbinance_historical_data\n========================\n\n.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/binance_historical_data\n   :target: https://img.shields.io/github/last-commit/stas-prokopiev/binance_historical_data\n   :alt: GitHub last commit\n\n.. image:: https://img.shields.io/github/license/stas-prokopiev/binance_historical_data\n    :target: https://github.com/stas-prokopiev/binance_historical_data/blob/master/LICENSE.txt\n    :alt: GitHub license<space><space>\n\n.. image:: https://img.shields.io/pypi/v/binance_historical_data\n   :target: https://img.shields.io/pypi/v/binance_historical_data\n   :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/pyversions/binance_historical_data\n   :target: https://img.shields.io/pypi/pyversions/binance_historical_data\n   :alt: PyPI - Python Version\n\n\n.. contents:: **Table of Contents**\n\nShort Overview.\n=========================\nbinance_historical_data is a python package (**py>=3.8**)\nwhich makes download of historical crypto data (prices and volumes) from binance server as simple as it can only be.\n**You don\'t even need to have an account at binance.com to download all history of crypto data**\n\nData is taken from here: https://data.binance.vision/?prefix=data/spot/\n\n| Using this package you will be able to have full historical data of prices and volumes with only 3 lines of python code\n| And if you need to update already downloaded data then once again 3 lines of python code will do the job\n\n\n| **Limitations**: The previous day data appears on binance server a few minutes after 0 a.m. UTC\n| So there is a delay in which you can get the data.\n\nInstallation via pip:\n======================\n\n.. code-block:: bash\n\n    pip install binance_historical_data\n\nHow to use it\n===========================\n\nInitialize main object: **data_dumper**\n---------------------------------------------\n\n.. code-block:: python\n\n    from binance_historical_data import CandleDataDumper\n\n    data_dumper = CandleDataDumper(\n        path_dir_where_to_dump=".",\n        str_data_frequency="1m",\n    )\n\nArguments:\n\n#. **path_dir_where_to_dump**:\n    | (string) Path to folder where to dump the data\n#. **str_data_frequency**:\n    | (string) One of [1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h]\n    | Frequency of price-volume data candles to get\n\nThe one and only method to dump the data\n------------------------------------------\n\n.. code-block:: python\n\n    data_dumper.dump_data(\n        list_tickers=None,\n        date_start=None,\n        date_end=None,\n        is_to_update_existing=False,\n    )\n\nArguments:\n\n#. **list_tickers=None**:\n    | (list) Trading pairs for which to dump data\n    | *if equals to None* - all **USDT** pairs will be used\n#. **date_start=None**:\n    | (datetime.date) The date from which to start dump\n    | *if equals to None* - every trading pair will be dumped from the early begining (the earliest is 2017-01-01)\n#. **date_end=True=None**:\n    | (datetime.date) The last date for which to dump data\n    | *if equals to None* - Today\'s date will be used\n#. **is_to_update_existing=False**:\n    | (bool) Flag if you want to update the data if it\'s already exist\n\nDownloaded data format\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n| path_dir_where_to_dump\n| --> ticker_1 (BTCUSDT)\n| ----> timefrequency (1m)\n| ------> daily\n| --------> BTCUSDT-1m-2022-02-01.csv\n| --------> BTCUSDT-1m-2022-02-02.csv\n| --------> ...\n| ------> monthly\n| --------> BTCUSDT-1m-2017-11.csv\n| --------> BTCUSDT-1m-2017-12.csv\n| --------> ...\n| --> ticker_2 (ETHUSDT)\n| ----> ...\n| --> ...\n\n.csv files columns\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n| "Open time" - Timestamp\n| "Open"\n| "High"\n| "Low"\n| "Close"\n| "Volume"\n| "Close time" - Timestamp\n| "Quote asset volume"\n| "Number of trades"\n| "Taker buy base asset volume"\n| "Taker buy quote asset volume"\n| "Ignore"\n\nExamples\n===========================\n\nHow to dump all data for all USDT trading pairs\n------------------------------------------------\n\nPlease be advised that the first data dump for all trading pairs might take some time (~40 minutes)\n\n.. code-block:: python\n\n    data_dumper.dump_data()\n\nHow to update data (get all new data)\n----------------------------------------------\n\n| It\'s as easy as running the exactly same method **dump_data** once again\n| The **data_dumper** will find all the dates for which data already exists\n| and will try to dump only the new data\n\n.. code-block:: python\n\n    data_dumper.dump_data()\n\nHow to update (reload) data for the asked time period\n----------------------------------------------------------\n\n.. code-block:: python\n\n    data_dumper.dump_data(\n        date_start=datetime.date(year=2021, month=1, day=1),\n        date_end=datetime.date(year=2022, month=1, day=1),\n        is_to_update_existing=True\n    )\n\nHow to get all trading pairs (tickers) from binance\n----------------------------------------------------\n\n.. code-block:: python\n\n    print(data_dumper.get_list_all_trading_pairs())\n\nLinks\n=====\n\n    * `PYPI <https://pypi.org/project/binance_historical_data/>`_\n    * `GitHub <https://github.com/stas-prokopiev/binance_historical_data>`_\n\nProject local Links\n===================\n\n    * `CHANGELOG <https://github.com/stas-prokopiev/binance_historical_data/blob/master/CHANGELOG.rst>`_.\n    * `CONTRIBUTING <https://github.com/stas-prokopiev/binance_historical_data/blob/master/CONTRIBUTING.rst>`_.\n\nContacts\n========\n\n    * Email: stas.prokopiev@gmail.com\n    * `vk.com <https://vk.com/stas.prokopyev>`_\n    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_\n\nLicense\n=======\n\nThis project is licensed under the MIT License.',
    'author': 'stanislav',
    'author_email': 'stas.prokopiev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stas-prokopiev/binance_historical_data',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
