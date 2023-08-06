# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pastypy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'pycryptodome>=3.14.1,<4.0.0',
 'requests>=2.27.1,<3.0.0',
 'tomli>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'pastypy',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
