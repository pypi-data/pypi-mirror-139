# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ctprint', 'ctprint.ctprint', 'ctprint.tests']

package_data = \
{'': ['*'], 'ctprint': ['dist/*']}

install_requires = \
['colorama>=0.4.4,<0.5.0']

entry_points = \
{'console_scripts': ['ctprint = ctprint:main']}

setup_kwargs = {
    'name': 'ctprint',
    'version': '0.1.4',
    'description': "coloring terminal output using '<tags> embedded in strings'",
    'long_description': '<h1 align="center">Hi there! Here a TagsColoredPrint\n<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>\n<h3 align="center">Python script for coloring terminal output using \'<tags> embedded in strings\' (like a simle text markup language)</h3>\n  \n![](https://api.visitorbadge.io/api/VisitorHit?user=saner9999f&repo=ctprint&countColor=%237B1E7A)\n![](https://img.shields.io/github/repo-size/saner99/ctprint?color=g&style=for-the-badge)\n![](https://img.shields.io/github/checks-status/saner99/ctprint/master?color=g&style=for-the-badge)\n![](https://img.shields.io/github/last-commit/saner99/ctprint/master?style=for-the-badge)\n![](https://img.shields.io/github/release-date/saner99/ctprint?style=for-the-badge)\n![](https://img.shields.io/github/stars/saner99/ctprint?style=for-the-badge)\n![](https://img.shields.io/github/forks/saner99/ctprint?style=for-the-badge)\n\n\n## Installation\n\n```python\npip install ctprint\n```\n\n## Usage\n\n### Initialization\n\n```python\n  from ctprint import ctp, ctdecode, cterr, ctlog # callable\n```\n\n### ctp.help()\n\n_print colored and some interactive help-message. nothing return_\n\n```python\nctp.help() # print help message\n```\n\n_output:_\n\n### ctp(string: str)\n\n_obj of ctprint. decode `<tags>` in the string and print it. nothing return_\n\n```python\nctp(\'<bw> black text on white background /> default formating\') # decode <tags> and then print the string\n```\n\n<p align="center">\n  <img src="https://user-images.githubusercontent.com/31666804/154783032-58888b00-d028-4a17-8d6c-bfe34bb8e604.png" width="100%" title="ctp.help() output">\n  \n  ### ctdecode( *strings: str) -> str\n  _decode `<tags>` in the strings and return it decoded_\n  ```python\n  ctdecode(\'<bw> black text on white background /> default formating\') # decode <tags> and then print the string\n  ```\n  _return string_\n  \n  ### cterr(exception=None, comment=\'\') -> None\n  _exception required. print colored error message from try/except. nothing return_\n  ```python\n  try:\n    1/0 #any broken line\n  except Exception as _ex:\n    cterr(_ex)\n  ```\n<p align="center">\n  <img src="https://user-images.githubusercontent.com/31666804/154783196-226b05f0-7401-41a1-8acc-84837140d7a0.png">\n  \n  ### ctlog(**vars) -> None\n  _vars required. print colored message with names $ values of all **vars. nothibg return_\n  \n  ```python\n var0 = var1 = 0\n\ndef example_ctlog():\n\n    var2 = \'string val\'  # out of the try, out of the function, var0=var2 - nothing problems.\n    var3 = {\'ctp_string\': \'<bg_red><red>red text on red background (NO) >\'}\n\n    ctlog(var0=var0, var1=var1, var2=var2, var3=var3)\n\n```\n<p align="center">\n<img src="https://user-images.githubusercontent.com/31666804/154783320-e90bd588-6d1a-4bef-a8c9-542302e30726.png" width="100%" title="ctp.help() output">\n\n## Thanks\n- [`colorama - wonderfull lib makes ANSI escape character sequences work under MS Windows. `](https://pypi.org/project/colorama/)\n\n\n\n<!--\n- [`collide-2d-aabb-aabb`](https://github.com/noffle/collide-2d-aabb-aabb)\n- [`goertzel`](https://github.com/noffle/goertzel)\n- [`twitter-kv`](https://github.com/noffle/twitter-kv) -->\n\n<h2 align ="center"> ctprint.help()</h2>\n<p align="center">\n<img src="https://user-images.githubusercontent.com/31666804/154776452-16a1722a-bd08-4432-af8f-254a5f3d4a41.png" width="100%" title="ctp.help() output">\n<img src="https://user-images.githubusercontent.com/31666804/154778504-3de31e36-4c7b-43fc-820a-727c2a397b20.png" width="100%" title="ctp.help() output[1]">\n<img src="https://user-images.githubusercontent.com/31666804/154778836-3f2168a1-c9ec-4602-ace7-54c429bb4ff5.png" width="100%" title="ctp.help() output[2]">\n</p>\n```\n',
    'author': 'saner99',
    'author_email': 'it@saner99.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/saner99/ctprint',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
