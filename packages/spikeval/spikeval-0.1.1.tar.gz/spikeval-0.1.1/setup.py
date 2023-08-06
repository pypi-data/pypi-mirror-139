# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spikeval']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.15,<2.0', 'pandas>=1.0,<2.0']

setup_kwargs = {
    'name': 'spikeval',
    'version': '0.1.1',
    'description': 'ML evaluation/validation utilities by Spike',
    'long_description': None,
    'author': 'Martín Villanueva',
    'author_email': 'mavillan@spikelab.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
