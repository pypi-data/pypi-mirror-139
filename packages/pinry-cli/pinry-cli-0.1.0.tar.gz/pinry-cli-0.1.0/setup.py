# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pinry_cli']
install_requires = \
['click>=8.0.4,<9.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['pinry = pinry_cli:cmd_group']}

setup_kwargs = {
    'name': 'pinry-cli',
    'version': '0.1.0',
    'description': 'Pinry CLI to upload local image to remote Pinry instance',
    'long_description': None,
    'author': 'winkidney',
    'author_email': 'winkidney@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
