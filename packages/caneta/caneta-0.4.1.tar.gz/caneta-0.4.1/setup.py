# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['caneta']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'caneta',
    'version': '0.4.1',
    'description': '',
    'long_description': None,
    'author': 'Madson Dias',
    'author_email': 'madsonddias@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
