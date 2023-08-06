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
 'lxml',
 'pandas',
 'requests',
 'selenium',
 'tqdm']

extras_require = \
{'docs': ['furo', 'myst-parser', 'sphinx']}

setup_kwargs = {
    'name': 'atcoder',
    'version': '0.1.0',
    'description': 'AtCoder API.',
    'long_description': '[![Python package](https://github.com/kagemeka/atcoder-api-python/actions/workflows/python-package.yml/badge.svg)](https://github.com/kagemeka/atcoder-api-python/actions/workflows/python-package.yml)\n[![readthedocs build status](https://readthedocs.org/projects/atcoder-api-python/badge/?version=latest&style=plastic)](https://readthedocs.org/projects/atcoder-api-python/badge/?version=latest&style=plastic)\n\n# AtCoder API for Python.\n\n\n\n## Documentation\nsee https://atcoder-api-python.readthedocs.io\n',
    'author': 'Hiroshi Tsuyuki',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'Hiroshi Tsuyuki',
    'maintainer_email': 'kagemeka1@gmail.com',
    'url': 'https://atcoder.readthedocs.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
