# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['theseptatimes']

package_data = \
{'': ['*']}

install_requires = \
['DateTime>=4.4,<5.0',
 'argparse>=1.4.0,<2.0.0',
 'colorama>=0.4.4,<0.5.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'python-Levenshtein>=0.12.2,<0.13.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['tst = TheSeptaTimes.cli:main']}

setup_kwargs = {
    'name': 'theseptatimes',
    'version': '0.0.8',
    'description': 'A Python package to get data from the Septa API',
    'long_description': None,
    'author': 'ZenithDS',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
