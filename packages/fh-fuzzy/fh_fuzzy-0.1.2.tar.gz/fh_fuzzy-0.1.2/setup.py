# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fh_fuzzy']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0', 'numpy>=1.22.2,<2.0.0']

setup_kwargs = {
    'name': 'fh-fuzzy',
    'version': '0.1.2',
    'description': 'Pacote para se trabalhar com a lógica fuzzy em python',
    'long_description': None,
    'author': 'Héber Morais',
    'author_email': 'heber.morais@ifpr.edu.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
