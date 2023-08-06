# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrsona']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'pyrsona',
    'version': '0.1',
    'description': '',
    'long_description': '# pyrsona',
    'author': 'John',
    'author_email': 'johnbullnz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/johnbullnz/pyrsona',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
