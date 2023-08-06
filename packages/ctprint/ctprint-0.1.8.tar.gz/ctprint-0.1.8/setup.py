# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'ctprint'}

packages = \
['ctprint']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'ctprint',
    'version': '0.1.8',
    'description': "coloring terminal output using '<tags> embedded in strings'",
    'long_description': '<h1 align="center">Hi there! Here a Color-Tagged Print\n<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>\n<p align="center">\n<img src=https://img.shields.io/pypi/v/ctprint.svg?color=%237B1E7A&style=flat-square>\n<img src=https://shields-io-visitor-counter.herokuapp.com/badge?page=https://github.com/saner99/ctprint&color=purple&style=flat-square>\n<img src=https://img.shields.io/github/repo-size/saner99/ctprint?color=g&style=flat-square>\n<img src=https://img.shields.io/github/checks-status/saner99/ctprint/master?color=g&style=flat-square>\n<img src=https://img.shields.io/github/last-commit/saner99/ctprint/master?style=flat-square>\n<img src=https://img.shields.io/github/license/saner99/ctprint?color=g&style=flat-square>\n<img src=https://img.shields.io/pypi/dd/ctprint?label=PyPI%20downloads&style=flat-square>\n<img src=https://img.shields.io/github/release-date/saner99/ctprint?style=flat-square>\n</p>\n<h3 align="center">Cross-platform colorization terminal text using \'&lt;tags> embedded in strings\' (text markup)</h3>\n\n## Installation\n\n```python\npip install ctprint\n```\n_or_\n```python\npoetry add ctprint\n```\n\n## Usage\n\n### Initialization\n\n```python\nfrom ctprint import ctp, ctdecode, cterr, ctlog  # callable\n```\n\n### ctp.help() -> None\n\n_print colored and some interactive help-message. nothing return_\n\n```python\nctp.help()  # print help message\n```\n\n### ctp(*strings: str) -> None\n\n_obj of ctprint. decode `<tags>` in the strings and print it. nothing return_\n\n```python\n# decode <tags> and then print the string\nctp(\'<bw> black text on white background /> default formating\')\n```\n\n<p align="center">\n  <img src="https://user-images.githubusercontent.com/31666804/154970116-1071c2c8-bca0-4da6-8959-0c44259c1803.png" width="100%" title="ctp.help() output"></p>\n  \n### ctdecode( *strings: str) -> str\n_decode `<tags>` in the strings and return it decoded_\n```python\n# decode <tags> in the strings and return decoded string\nstring0 = \' background /> default\'\nstring1 = \' formating\'\nctdecode(\'<bw> black text on white\', string0, string1)\n```\n_return string_\n\n### cterr(exception=None, comment=\'\') -> None\n_exception required. print colored error message from try/except. nothing return_\n```python\ntry:\n    1/0  # any broken line\nexcept Exception as _ex:\n    cterr(_ex)\n```\n<p align="center">\n  <img src="https://user-images.githubusercontent.com/31666804/154970120-48464807-9d99-4833-b873-3453eec656f6.png"></p>\n  \n### ctlog(**vars) -> None\n_vars required. print colored message with names $ values of all **vars. nothibg return_\n\n```python\nvar0 = var1 = 0\n\ndef example_ctlog():\n\n    var2 = \'string val\'\n    var3 = {\'ctp_string\': \'<bg_red><red>red text on red background (NO) >\'}\n\n    # out of the function, var0=var2 - nothing problems.\n    ctlog(var0=var0, var1=var1, var2=var2, var3=var3)\n```\n<p align="center">\n<img src="https://user-images.githubusercontent.com/31666804/154970137-f07b1ca4-f73b-4ffd-a1a1-d49905e502fa.png" width="100%" title="ctp.help() output"></p>\n\n<h2 align ="center"> ctprint.help()</h2>\n<p align="center">\n<img src="https://user-images.githubusercontent.com/31666804/154970057-6f710980-c6c1-470b-a5d8-ac1006b04eda.png" width="100%" title="ctp.help() output">\n<img src="https://user-images.githubusercontent.com/31666804/154970079-d4f150fe-fa74-466c-8e57-576c6b5cb0ce.png" width="100%" title="ctp.help() output[1]">\n<img src="https://user-images.githubusercontent.com/31666804/154970102-ea031f0e-a836-47c8-bf0d-7235a8937f6f.png" width="100%" title="ctp.help() output[2]">\n</p>\n\n\n## Thanks\n- [`colorama - wonderfull lib. Makes ANSI escape character sequences work under MS Windows. `](https://pypi.org/project/colorama/)\n\n',
    'author': 'saner99',
    'author_email': 'it@saner99.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/saner99/ctprint',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
