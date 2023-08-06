# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bbc', 'bbc.anthologies']

package_data = \
{'': ['*']}

install_requires = \
['SPARQLWrapper>=1.8.5,<2.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'bibtexparser>=1.2.0,<2.0.0',
 'isbnlib>=3.10.9,<4.0.0',
 'pycountry>=22.1.10,<23.0.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['bbc = bbc:main']}

setup_kwargs = {
    'name': 'bbc',
    'version': '0.1.0',
    'description': 'utility to check and format bibtex files',
    'long_description': None,
    'author': 'tdsimao',
    'author_email': 'tdsimao@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
