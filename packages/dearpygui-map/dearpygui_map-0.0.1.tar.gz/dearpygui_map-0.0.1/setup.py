# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dearpygui_map']

package_data = \
{'': ['*']}

install_requires = \
['dearpygui>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'dearpygui-map',
    'version': '0.0.1',
    'description': 'Map widget for Dear PyGui',
    'long_description': None,
    'author': 'Mikko Kouhia',
    'author_email': 'mikko.kouhia@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
