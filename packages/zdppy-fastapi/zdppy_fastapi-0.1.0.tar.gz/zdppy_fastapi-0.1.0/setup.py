# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zdppy_fastapi']

package_data = \
{'': ['*']}

install_requires = \
['PyMySQL>=1.0.2,<2.0.0',
 'fastapi>=0.73.0,<0.74.0',
 'html-table>=1.0,<2.0',
 'orjson>=3.6.7,<4.0.0',
 'pandas>=1.4.1,<2.0.0',
 'peewee>=3.14.8,<4.0.0',
 'sqlmodel>=0.0.6,<0.0.7',
 'zdppy-log>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'zdppy-fastapi',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'zhangdapeng',
    'author_email': 'pygosuperman@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
