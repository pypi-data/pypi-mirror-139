# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['shellfish', 'shellfish.aios', 'shellfish.dev', 'shellfish.fs', 'shellfish.sh']

package_data = \
{'': ['*']}

install_requires = \
['aiopen>=0.5.0,<0.6.0',
 'asyncify>=0.7,<0.10',
 'funkify>=0.4.0,<0.5.0',
 'jsonbourne>=0.20.3',
 'listless>=0.1.0',
 'pydantic>=1.9.0,<2.0.0',
 'xtyping>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'shellfish',
    'version': '0.1.2',
    'description': 'shellfish ~ shell & file-system utils',
    'long_description': None,
    'author': 'jesse',
    'author_email': 'jesse@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs/tree/master/libs/shellfish',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
