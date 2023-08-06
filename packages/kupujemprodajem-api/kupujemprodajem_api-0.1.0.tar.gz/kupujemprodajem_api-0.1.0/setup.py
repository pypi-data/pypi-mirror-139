# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kupujemprodajem_api']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'lxml>=4.8.0,<5.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'kupujemprodajem-api',
    'version': '0.1.0',
    'description': 'Python Unofficial API Wrapper for KupujemProdajem.com',
    'long_description': None,
    'author': 'innicoder',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
