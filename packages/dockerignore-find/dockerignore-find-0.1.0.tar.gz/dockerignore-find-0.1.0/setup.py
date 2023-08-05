# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dockerignore_find']
entry_points = \
{'console_scripts': ['dockerignore-find = dockerignore_find:main']}

setup_kwargs = {
    'name': 'dockerignore-find',
    'version': '0.1.0',
    'description': 'Helper with dockerignore files',
    'long_description': None,
    'author': 'Martin Ortbauer',
    'author_email': 'mortbauer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
