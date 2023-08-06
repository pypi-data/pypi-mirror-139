# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypipublishtest']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypipublishtest',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Nicholas',
    'author_email': 'duzilin@hotmail.co.za',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
