# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osma', 'osma.aggregators', 'osma.sources']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'favicon>=0.7.0,<0.8.0',
 'loguru>=0.5.3,<0.6.0',
 'newsapi-python>=0.2.6,<0.3.0',
 'praw>=7.5.0,<8.0.0',
 'python-frontmatter>=1.0.0,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'tweepy>=4.4.0,<5.0.0']

entry_points = \
{'console_scripts': ['osma = osma.cli:osma']}

setup_kwargs = {
    'name': 'osma',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Mihails Delmans',
    'author_email': 'm.delmans@gmail.com',
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
