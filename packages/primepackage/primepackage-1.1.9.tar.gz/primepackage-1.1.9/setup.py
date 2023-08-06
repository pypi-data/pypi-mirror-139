# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['primepackage']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'primepackage',
    'version': '1.1.9',
    'description': 'A package for the calculation, querying and lsiting of primes. prime products and non trivial zeros',
    'long_description': None,
    'author': 'Jamell Samuels',
    'author_email': 'jamellsamuels@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
