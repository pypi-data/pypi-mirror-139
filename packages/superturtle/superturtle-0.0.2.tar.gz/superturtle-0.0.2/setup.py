# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['superturtle']

package_data = \
{'': ['*']}

install_requires = \
['easing-functions>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'superturtle',
    'version': '0.0.2',
    'description': "Extensions to Python's turtle",
    'long_description': None,
    'author': 'Chris Proctor',
    'author_email': 'chris@chrisproctor.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
