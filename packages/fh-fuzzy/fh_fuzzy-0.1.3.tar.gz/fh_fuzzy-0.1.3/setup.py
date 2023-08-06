# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fh_fuzzy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fh-fuzzy',
    'version': '0.1.3',
    'description': 'Toolbox para se trabalhar com a lógica Fuzzy',
    'long_description': None,
    'author': 'Héber R. F Morais',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
