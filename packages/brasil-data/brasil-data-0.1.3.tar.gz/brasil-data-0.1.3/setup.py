# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brdata', 'brdata.cvm']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'cachier>=1.5.3,<2.0.0',
 'lxml>=4.6.4,<5.0.0',
 'pandas>=1.3.5,<2.0.0',
 'random-user-agent>=1.0.1,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'xlrd>=2.0.1,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=4.5.0,<5.0.0']}

setup_kwargs = {
    'name': 'brasil-data',
    'version': '0.1.3',
    'description': 'Fontes de dados do mercado financeiro brasileiro',
    'long_description': None,
    'author': 'Gabriel Guarisa',
    'author_email': 'gabrielguarisa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.12,<3.11',
}


setup(**setup_kwargs)
