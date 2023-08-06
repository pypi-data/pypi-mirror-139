# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysimibot']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.14.0,<3.0.0']

entry_points = \
{'console_scripts': ['pysimsimi-cli = pysimibot.pysimibot:Simsimi']}

setup_kwargs = {
    'name': 'pysimibot',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Rafael Lima',
    'author_email': 'rafael.lima3301@gmail.com',
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
