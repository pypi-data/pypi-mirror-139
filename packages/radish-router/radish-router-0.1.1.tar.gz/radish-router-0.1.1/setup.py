# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['radish']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'radish-router',
    'version': '0.1.1',
    'description': 'RadixTree implementation in python 3.10',
    'long_description': None,
    'author': 'cheetahbyte',
    'author_email': 'bernerdoodle@outlook.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
