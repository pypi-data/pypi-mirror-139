# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clicks']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'clicks',
    'version': '0.0.1',
    'description': 'Metamodern Command Line & Textual User Interfaces',
    'long_description': None,
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
