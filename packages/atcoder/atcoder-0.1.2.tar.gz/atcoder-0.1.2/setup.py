# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['atcoder']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML',
 'aiodns',
 'aiohttp',
 'beautifulsoup4',
 'cchardet',
 'filesystem-python==0.2.0',
 'lxml',
 'optext-python==0.1.1',
 'pandas',
 'requests',
 'selenium',
 'tqdm']

extras_require = \
{'docs': ['furo',
          'myst-parser',
          'pdoc3',
          'pydata-sphinx-theme',
          'python-docs-theme',
          'sphinx',
          'sphinx-book-theme',
          'sphinx-theme-pd',
          'sphinx_rtd_theme<=2.0.0',
          'sphinxcontrib-mermaid']}

setup_kwargs = {
    'name': 'atcoder',
    'version': '0.1.2',
    'description': 'AtCoder API for Python',
    'long_description': '# AtCoder API for Python.\n\n[![Python package][ci-badge]][ci-url]\n[![readthedocs build status][docs-badge]][docs-url]\n[![pre-commit][pre-commit-badge]][pre-commit-url]\n[![CodeQL][codeql-badge]][codeql-url]\n[![License: MIT][mit-badge]][mit-url]\n[![PyPI version][pypi-badge]][pypi-url]\n[![Github pages][gh-pages-badge]][gh-pages-url]\n\n[ci-badge]: https://github.com/kagemeka/atcoder-python/actions/workflows/python-package.yml/badge.svg\n[ci-url]: https://github.com/kagemeka/atcoder-python/actions/workflows/python-package.yml\n[docs-badge]: https://readthedocs.org/projects/atcoder-python/badge/?version=latest\n[docs-url]: https://atcoder-python.readthedocs.io\n[pre-commit-badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n[pre-commit-url]: https://github.com/pre-commit/pre-commit\n[codeql-badge]: https://github.com/kagemeka/atcoder-python/actions/workflows/codeql-analysis.yml/badge.svg\n[codeql-url]: https://github.com/kagemeka/atcoder-python/actions/workflows/codeql-analysis.yml\n[mit-badge]: https://img.shields.io/badge/License-MIT-blue.svg\n[mit-url]: https://opensource.org/licenses/MIT\n[pypi-badge]: https://badge.fury.io/py/atcoder.svg\n[pypi-url]: https://badge.fury.io/py/atcoder\n[gh-pages-badge]: https://github.com/kagemeka/atcoder-python/actions/workflows/pages/pages-build-deployment/badge.svg\n[gh-pages-url]: https://kagemeka.github.io/atcoder-python\n',
    'author': 'Hiroshi Tsuyuki',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'Hiroshi Tsuyuki',
    'maintainer_email': 'kagemeka1@gmail.com',
    'url': 'https://kagemeka.github.io/atcoder-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
