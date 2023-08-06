# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orm_alchemy']

package_data = \
{'': ['*']}

install_requires = \
['inflection>=0.5.1,<0.6.0', 'sqlalchemy>=1.4.31,<2.0.0']

setup_kwargs = {
    'name': 'orm-alchemy',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'NamTH',
    'author_email': 'namth2302@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.2,<4.0.0',
}


setup(**setup_kwargs)
