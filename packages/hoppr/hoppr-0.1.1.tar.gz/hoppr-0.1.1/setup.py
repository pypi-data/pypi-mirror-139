# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hoppr']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hopctl = hoppr.main:app']}

setup_kwargs = {
    'name': 'hoppr',
    'version': '0.1.1',
    'description': 'A tool for defining, verifying, and transferring software dependencies between environments.',
    'long_description': None,
    'author': 'LMCO Open Source',
    'author_email': 'open.source@lmco.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/lmco/hoppr/hoppr',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
