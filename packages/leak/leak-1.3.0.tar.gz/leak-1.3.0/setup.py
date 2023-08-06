# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leak']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'rich>=11.2.0,<12.0.0']

entry_points = \
{'console_scripts': ['leak = leak.cli:cli']}

setup_kwargs = {
    'name': 'leak',
    'version': '1.3.0',
    'description': 'Show release information about packages on PyPI',
    'long_description': '## leak\n\n![PyPI](https://img.shields.io/pypi/v/leak?style=flat-square)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/leak?style=flat-square)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/leak?style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/leak?style=flat-square)\n\nShow info about package releases on PyPi.\n\nIf you need to install specific version of package it is useful to know all available versions to have a choice.\n\nJust run\n\n```bash\n$ leak <package_name>\n```\n\nand you will see all releases and some useful statistic about package specified. It will show most recent version, most popular (with highest number of downloads) and some additional information.\n\n### How to install\n\nInstall using pip\n\n```bash\n$ pip install leak\n\n# or to make sure the proper interpreter is used\n$ python -m pip install leak\n```\n\nor directly from github\n\n```bash\n$ git clone git://github.com/bmwant/leak.git\n$ python setup.py install\n```\n\n### Contribution\n\nSee [DEVELOP.md](./DEVELOP.md) to setup your local development environment and create pull request to this repository once new feature is ready.\n\n### License\n\nDistributed under [MIT License](https://tldrlegal.com/license/mit-license).\n',
    'author': 'Misha Behersky',
    'author_email': 'bmwant@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bmwant/leak',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
