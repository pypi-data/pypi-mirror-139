# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thenet']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'thenet',
    'version': '0.1.0',
    'description': 'The Net, A New Way to Look Into Data',
    'long_description': None,
    'author': 'aarmn',
    'author_email': 'aarmn80@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
