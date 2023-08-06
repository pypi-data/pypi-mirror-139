# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['closedexpressions']

package_data = \
{'': ['*']}

install_requires = \
['mpmath>=1.2.1,<2.0.0', 'numpy>=1.22.2,<2.0.0']

setup_kwargs = {
    'name': 'closedexpressions',
    'version': '0.1.0',
    'description': 'Closed expressions for shot noise processes.',
    'long_description': None,
    'author': 'gregordecristoforo',
    'author_email': 'gregor.decristoforo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
