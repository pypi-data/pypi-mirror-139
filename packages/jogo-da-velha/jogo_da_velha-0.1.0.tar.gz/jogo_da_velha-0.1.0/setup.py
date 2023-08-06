# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jogo_da_velha']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jogo-da-velha',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'esteves-maem',
    'author_email': 'esteves.maem@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
