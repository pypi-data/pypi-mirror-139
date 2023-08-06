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
    'version': '0.1.2',
    'description': 'Closed expressions for shot noise processes.',
    'long_description': '# fpp-closed-expressions\n\nClosed expressions for the most common functions related to shot noise processes.\n\n## installation\nThe package is published to PyPI and can be installed with\n```sh\npip install closedexpressions\n```\n\nIf you want the development version you must first clone the repo to your local machine,\nthen install the project and its dependencies with [poetry]:\n\n```sh\ngit clone https://github.com/uit-cosmo/fpp-closed-expressions\ncd fpp-closed-expresions\npoetry install\n```\n\n## Use\n\nImport functions directly, i.e.:\n\n```Python\nimport closedexpressions as ce\n\npsd = ce.psd(omega, td, l)\n```',
    'author': 'gregordecristoforo',
    'author_email': 'gregor.decristoforo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uit-cosmo/fpp-closed-expressions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
