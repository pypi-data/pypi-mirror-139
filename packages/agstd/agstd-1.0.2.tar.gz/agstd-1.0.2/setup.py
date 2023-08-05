# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['agstd', 'agstd.refraction', 'agstd.sdb', 'agstd.vis']

package_data = \
{'': ['*'], 'agstd.vis': ['pipeline_examples/*']}

install_requires = \
['numpy>=1.22.2,<2.0.0', 'pysqlite3>=0.4.6,<0.5.0', 'tables>=3.7.0,<4.0.0']

setup_kwargs = {
    'name': 'agstd',
    'version': '1.0.2',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
