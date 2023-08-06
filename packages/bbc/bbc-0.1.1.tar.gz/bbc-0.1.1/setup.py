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
    'version': '0.1.1',
    'description': 'utility to check and format bibtex files',
    'long_description': '# bbc\n\n## Synopsis\n\n`bbc` is a tiny utility that checks some basic properties of you bibtex files, orders the entries in an alphabetical order and style them in a uniform way.\n\n## Usage\n\n```bash\nbbc <bib_file> --output=<out_file>\n```\n\nThe formated bibtex is printed in the `<out_file>` file, while error messages on the standard error output.\n\nAdd the flag `--add-todo` to assign a `TODO` value to missing fields which are required for the particular types of entries:\n\n```bash\nbbc <bib_file> --output=<out_file> --add-todo\n```\n\nIf you toggle option `--try-fix`, it will try to find missing ISSN and other informations about journals (from [DBpedia](http://wiki.dbpedia.org/)) or ISBN and other information for books (from [Google Books](books.google.com)).\n\n\n## How to install\n\n1. Clone this project.\n2. Using `pipx` you can install the utility from the main folder:\n\n```bash\npipx install .\n```\n\n## Prerequisities\n\nThis utility uses the following packages.\n\n- [`bibtexparser`](https://github.com/sciunto-org/python-bibtexparser) to parse and print bibtex\n- [`beautifulsoup4`](https://pypi.org/project/beautifulsoup4/) to scrape web pages\n- [`libisbn`](https://github.com/xlcnd/isbnlib) to work ISBNs and Google Books\n- [`SPARQLWrapper`](https://github.com/RDFLib/sparqlwrapper) to query DBpedia\n- [`termcolor`](https://pypi.python.org/pypi/termcolor) to have colored error messages\n- [`pycountry`](https://pypi.org/project/pycountry/) to query countries\n\n## License\n\nThe software is distributed under the [BSD License](https://opensource.org/licenses/BSD-3-Clause).\n\n## Acknowledgments\n\nThis project is based on [prettybib](https://github.com/jlibovicky/prettybib).\n',
    'author': 'tdsimao',
    'author_email': 'tdsimao@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tdsimao/bbc/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
