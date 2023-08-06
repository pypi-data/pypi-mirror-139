# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pythonquerylanguage']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.31,<2.0.0',
 'ipython>=8.0.1,<9.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'pythonquerylanguage',
    'version': '0.1.2',
    'description': 'Python SQL wrapper based on pandas and SQLalchemy',
    'long_description': None,
    'author': 'Pablo Ruiz',
    'author_email': 'pablo.r.c@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
