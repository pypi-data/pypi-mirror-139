# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['langtoxicscore']
setup_kwargs = {
    'name': 'langtoxicscore',
    'version': '0.1',
    'description': 'GetToxicity(string_, models, vectorizers)',
    'long_description': None,
    'author': 'Dmitry Filinov',
    'author_email': 'dm.filinov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
