# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ctprint']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ctprint',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'saner99',
    'author_email': 'it@saner99.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
