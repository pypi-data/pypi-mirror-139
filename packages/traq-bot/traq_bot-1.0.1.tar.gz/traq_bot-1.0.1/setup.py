# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['traq_bot']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'traq-bot',
    'version': '1.0.1',
    'description': 'Bot library for traQ',
    'long_description': None,
    'author': 'd_etteiu8383',
    'author_email': 'ysdr83@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9.5,<4.0.0',
}


setup(**setup_kwargs)
