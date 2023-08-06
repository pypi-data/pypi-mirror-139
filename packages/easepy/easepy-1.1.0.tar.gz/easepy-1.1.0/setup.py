# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['easepy']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.2,<2.0.0', 'pyproj>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'easepy',
    'version': '1.1.0',
    'description': 'Python package for working with EASE grids.',
    'long_description': None,
    'author': 'Karl Nordstrom',
    'author_email': 'karl.am.nordstrom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
