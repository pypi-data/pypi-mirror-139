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
{'console_scripts': ['gen_spec = '
                     'yfrake.openapi.generator:generate_openapi_spec']}

setup_kwargs = {
    'name': 'yfrake',
    'version': '0.1.11',
    'description': 'A flexible and agile stock market data scraper and server.',
    'long_description': '# YFrake\n\n<a target="new" href="https://pypi.python.org/pypi/yfrake"><img border=0 src="https://img.shields.io/badge/python-3.7+-blue.svg?label=python" alt="Supported Python versions"></a>\n<a target="new" href="https://pypi.python.org/pypi/yfrake"><img border=0 src="https://img.shields.io/pypi/v/yfrake?label=version" alt="Package version on PyPI"></a>\n<a target="new" href="https://pypi.python.org/pypi/yfrake"><img border=0 src="https://img.shields.io/pypi/dm/yfrake?label=installs" alt="Installs per month"></a>\n<a target="new" href="https://www.codefactor.io/repository/github/aspenforest/yfrake"><img border=0 src="https://img.shields.io/codefactor/grade/github/aspenforest/yfrake?label=code quality" alt="CodeFactor code quality"></a>\n<a target="new" href="https://scrutinizer-ci.com/g/aspenforest/yfrake/"><img border=0 src="https://img.shields.io/scrutinizer/build/g/aspenforest/yfrake" alt="Scrutinizer build inspection"></a>\n<a target="new" href="https://github.com/aspenforest/yfrake/issues"><img border=0 src="https://img.shields.io/github/issues/aspenforest/yfrake" alt="Issues on Github"></a>\n<a target="new" href="https://github.com/aspenforest/yfrake/blob/main/LICENSE"><img border=0 src="https://img.shields.io/github/license/aspenforest/yfrake" alt="License on GitHub"></a>\n<a target="new" href="https://github.com/aspenforest/yfrake/stargazers"><img border=0 src="https://img.shields.io/github/stars/aspenforest/yfrake?style=social" alt="Stars on GitHub"></a>\n\n### Disclaimer\nThe current version of YFrake is usable, but ***not*** production ready.\n\n### Description\nYFrake is a ***flexible*** and ***agile*** stock market data scraper and server [&#91;note1&#93;](#footnote1).\nIt enables developers to build powerful apps without having to worry about maximizing network request throughput [&#91;note2&#93;](#footnote1).\nYFrake can be used as a client to directly return market data or as a ***programmatically controllable server*** to forward data to web clients.\nIn addition, all network requests by YFrake are ***non-blocking***, which means that your program can continue running your code while network requests are in progress.\nThe best part about YFrake is its ***built-in swagger API documentation*** which you can use to perform test queries and examine the returned responses.\n\n\n### Getting Started\n#### Installation\n~~~\npip install yfrake\n~~~\n#### How to import\n~~~\nfrom yfrake import ThreadClient\nfrom yfrake import AsyncClient\nfrom yfrake import Server\n~~~\n#### ThreadClient example\n~~~\nclient = ThreadClient()\nclient.get(\'historical_prices\', symbol=\'msft\', interval=\'1d\', range=\'1y\')\nwhile client.is_busy():\n    # Do other stuff\nif client.is_done() and not client.response.error:\n    print(client.response.data)\n~~~\n#### AsyncClient example\n~~~\nasync def main():\n    resp = await AsyncClient.get_historical_prices(symbol=\'msft\', interval=\'1d\', range=\'1y\')\n    if not resp.error:\n        print(resp.data)\nasyncio.run(main())\n~~~\n#### Server example\n~~~\nServer.start()  # Default address is \'localhost:8888\'\n# Do some other stuff\nServer.stop()  # Kills all server sub-processes.\n~~~\n\n<br/>\n<a id="footnote1"><sup>&#91;note1&#93;:</sup></a> Stock market data is sourced from Yahoo Finance. <br/>\n<a id="footnote2"><sup>&#91;note2&#93;:</sup></a> You still need to know how to gather coroutines when using asyncio to maximize throughput.\n',
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
