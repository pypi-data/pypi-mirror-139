# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yfrake',
 'yfrake.client',
 'yfrake.openapi',
 'yfrake.openapi.specs',
 'yfrake.server']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-swagger3>=0.7,<0.8',
 'aiohttp>=3.8,<4.0',
 'psutil>=5.9,<6.0',
 'pyyaml>=6.0,<7.0',
 'tomli>=2.0,<3.0']

entry_points = \
{'console_scripts': ['generate_swagger_spec = '
                     'yfrake.openapi.generator:generate_openapi_spec']}

setup_kwargs = {
    'name': 'yfrake',
    'version': '0.1.0',
    'description': 'The most flexible Yahoo Finance stock market data scraper and server.',
    'long_description': '# YFrake\nThe most flexible Yahoo Finance stock market data scraper and server.\n',
    'author': 'Mattias Aabmets',
    'author_email': 'mattias.aabmets@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
