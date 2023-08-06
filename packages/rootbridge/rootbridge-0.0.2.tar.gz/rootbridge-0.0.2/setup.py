# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rootbridge']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rootbridge',
    'version': '0.0.2',
    'description': 'Bridge to the silos.',
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
