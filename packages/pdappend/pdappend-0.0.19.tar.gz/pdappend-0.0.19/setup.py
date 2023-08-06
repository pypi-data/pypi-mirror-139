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
    'version': '0.0.19',
    'description': 'Append csv, xlsx, and xls files.',
    'long_description': None,
    'author': 'Chris',
    'author_email': 'cnpryer@gmail.com',
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
