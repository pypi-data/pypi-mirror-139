# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loveliness']

package_data = \
{'': ['*']}

install_requires = \
['libtorrent>=2.0.5,<3.0.0']

setup_kwargs = {
    'name': 'loveliness',
    'version': '0.0.1',
    'description': 'Media cache',
    'long_description': None,
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
