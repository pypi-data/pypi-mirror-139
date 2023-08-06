# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wikijscmd']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'wikijscmd',
    'version': '0.3.0',
    'description': 'A command line interface (CLI) for wiki.js',
    'long_description': None,
    'author': 'Mark Powers',
    'author_email': 'mark@marks.kitchen',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
