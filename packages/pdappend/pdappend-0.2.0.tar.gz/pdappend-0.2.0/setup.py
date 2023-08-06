# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdappend']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.4.1,<2.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'xlrd>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['pdappend = pdappend.cli:main',
                     'pdappend-gui = pdappend.gui:main']}

setup_kwargs = {
    'name': 'pdappend',
    'version': '0.2.0',
    'description': 'Append csv, xlsx, and xls files.',
    'long_description': '[![PyPI Latest Release](https://img.shields.io/pypi/v/pdappend)](https://pypi.org/project/pdappend/)\n![tests](https://github.com/cnpryer/pdappend/workflows/ci/badge.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![pdappend](https://img.shields.io/pypi/pyversions/pdappend?color=blue)\n\nThis project is under development.\n\n# pdappend\n\nRun `pdappend` from the command line to append csv, xlsx, and xls files.\n\n## Installation\n\n`pip install pdappend`\n\n## Using `pdappend`\n\nAppend specific files\n\n`pdappend file1.csv file2.csv file3.csv`\n\nAppend specific file types in your directory\n\n`pdappend *.csv`\n\nAppend all `pdappend`-compatible files in your directory\n\n`pdappend .`\n\n## Supported file types\n\n- csv\n- xls\n- xlsx: [Not supported in Python 3.6 environments](https://groups.google.com/g/python-excel/c/IRa8IWq_4zk/m/Af8-hrRnAgAJ?pli=1) (downgrade to `xlrd 1.2.0` or convert to `.xls`)\n\n## Documentation\n\n(TODO)\nSee the [wiki](https://github.com/cnpryer/pdappend/wiki) for more on `pdappend`.\n\n## Contributing\n\nPull requests are welcome!\n',
    'author': 'Chris',
    'author_email': 'cnpryer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cnpryer/pdappend',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
