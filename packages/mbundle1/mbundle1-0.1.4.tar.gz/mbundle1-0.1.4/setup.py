# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mbundle1']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.20.1,<3.0.0']

setup_kwargs = {
    'name': 'mbundle1',
    'version': '0.1.4',
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
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
