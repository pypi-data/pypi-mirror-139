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
    'version': '0.1.0',
    'description': '',
    'long_description': '========================\nbinance_historical_data\n========================\n\n.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/binance_historical_data\n   :target: https://img.shields.io/github/last-commit/stas-prokopiev/binance_historical_data\n   :alt: GitHub last commit\n\n.. image:: https://img.shields.io/github/license/stas-prokopiev/binance_historical_data\n    :target: https://github.com/stas-prokopiev/binance_historical_data/blob/master/LICENSE.txt\n    :alt: GitHub license<space><space>\n\n.. image:: https://img.shields.io/pypi/v/binance_historical_data\n   :target: https://img.shields.io/pypi/v/binance_historical_data\n   :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/pyversions/binance_historical_data\n   :target: https://img.shields.io/pypi/pyversions/binance_historical_data\n   :alt: PyPI - Python Version\n\n\n.. contents:: **Table of Contents**\n\nShort Overview.\n=========================\nbinance_historical_data is a python package (**py>=3.7**)\nwhich makes dumping of historical crypto data from binance server as simple as possible.\n**You don\'t even need to have an account at binance.com to dump all history of crypto data**\n\n\n| Using this package you will be able to have full binance historical data with only 3 lines of python code\n| And if you need to update already dumped data then once again 3 lines of python code will do the job\n\n| **Limitations**: The previous day data appear on binance server a few minutes after 0 a.m. UTC\n| So there is a delay in which you can get the data.\n\nInstallation via pip:\n======================\n\n.. code-block:: bash\n\n    pip install binance_historical_data\n\n\nHow to use it\n===========================\n\n\nInit main object: **data_dumper**\n-----------------------------------\n\n.. code-block:: python\n\n    from binance_historical_data import CandleDataDumper\n\n    data_dumper = CandleDataDumper(\n        path_dir_where_to_dump=".",\n        str_data_frequency="1m",\n    )\n\nArguments:\n\n#. **path_dir_where_to_dump**:\n    | (string) Path to folder where to dump the historical data\n#. **str_data_frequency**:\n    | (string) One of [1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h]\n\nThe main method to dump data\n-----------------------------\n\n.. code-block:: python\n\n    data_dumper.dump_data(\n        list_tickers=None,\n        date_start=None,\n        date_end=None,\n        is_to_update_existing=False,\n    )\n\nArguments:\n\n#. **list_tickers=None**:\n    | list\n    | Trading pairs for which to dump data\n    | if equals to None all **USDT** pairs will be used\n#. **date_start=None**:\n    | datetime.date\n    | The date from which to start dump\n#. **date_end=True=None**:\n    | datetime.date\n    | The last date for which to dump data\n#. **is_to_update_existing=False**:\n    | bool\n    | Flag if you want to update data if it\'s already exists\n\nExamples\n===========================\n\nHow to dump all data for all USDT trading pairs\n------------------------------------------------\n\nPlease be advised that the first data dump for all trading pairs might take some time (~40 minutes)\n\n.. code-block:: python\n\n    data_dumper.dump_data()\n\n\nHow to update data dump and get all new data\n----------------------------------------------\n\n.. code-block:: python\n\n    data_dumper.dump_data()\n\n\nHow to update (reload) all data for the asked time period\n----------------------------------------------------------\n\n.. code-block:: python\n\n    data_dumper.dump_data(\n        date_start=datetime.date(year=2021, month=1, day=1),\n        date_end=datetime.date(year=2022, month=1, day=1),\n        is_to_update_existing=True\n    )\n\n\nHow to get all trading pairs (tickers) from binance\n----------------------------------------------------\n\n.. code-block:: python\n\n    print(data_dumper.get_list_all_trading_pairs())\n\n\nLinks\n=====\n\n    * `PYPI <https://pypi.org/project/binance_historical_data/>`_\n    * `GitHub <https://github.com/stas-prokopiev/binance_historical_data>`_\n\nProject local Links\n===================\n\n    * `CHANGELOG <https://github.com/stas-prokopiev/binance_historical_data/blob/master/CHANGELOG.rst>`_.\n    * `CONTRIBUTING <https://github.com/stas-prokopiev/binance_historical_data/blob/master/CONTRIBUTING.rst>`_.\n\nContacts\n========\n\n    * Email: stas.prokopiev@gmail.com\n    * `vk.com <https://vk.com/stas.prokopyev>`_\n    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_\n\nLicense\n=======\n\nThis project is licensed under the MIT License.',
    'author': 'stanislav',
    'author_email': 'stas.prokopiev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stas-prokopiev/binance_historical_data',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
