# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starling_server',
 'starling_server.cli',
 'starling_server.models',
 'starling_server.starling',
 'starling_server.starling.models']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Sphinx>=4.4.0,<5.0.0',
 'cleo>=0.8.1,<0.9.0',
 'config-path>=1.0.2,<2.0.0',
 'fastapi>=0.74.0,<0.75.0',
 'httpx>=0.22.0,<0.23.0',
 'pydantic>=1.9.0,<2.0.0',
 'sphinx-rtd-theme>=1.0.0,<2.0.0',
 'uvicorn>=0.17.5,<0.18.0']

entry_points = \
{'console_scripts': ['starling-server = starling_server.cli.cli:cli']}

setup_kwargs = {
    'name': 'starling-server',
    'version': '0.1.0',
    'description': 'An API for working with a validated subset of the Starling Bank API',
    'long_description': None,
    'author': 'Richard',
    'author_email': 'richlyon@mac.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
