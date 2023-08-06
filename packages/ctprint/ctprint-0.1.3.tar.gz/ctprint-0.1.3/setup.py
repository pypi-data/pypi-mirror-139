# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ctprint']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'ctprint',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'saner99',
    'author_email': 'it@saner99.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
