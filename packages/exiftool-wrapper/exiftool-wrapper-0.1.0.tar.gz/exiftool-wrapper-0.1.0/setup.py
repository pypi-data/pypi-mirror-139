# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exiftool_wrapper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'exiftool-wrapper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Nils Philippsen',
    'author_email': 'nils@tiptoe.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
