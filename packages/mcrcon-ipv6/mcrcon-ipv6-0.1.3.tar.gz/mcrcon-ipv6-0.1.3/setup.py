# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcrcon_ipv6']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mcrcon-ipv6',
    'version': '0.1.3',
    'description': 'mcrcon with IPv6 support',
    'long_description': '# MCRcon.py\n\nМодифицированная версия [библиотеки](https://github.com/Uncaught-Exceptions/MCRcon) \nс полной поддержкой IPv6 адресов.\n\n# [pip package](https://pypi.org/project/mcrcon-ipv6/)\n',
    'author': 'firesquare',
    'author_email': 'team@firesquare.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fire-squad/mcrcon',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
