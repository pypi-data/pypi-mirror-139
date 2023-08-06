# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['client_dercaci']
setup_kwargs = {
    'name': 'client-dercaci',
    'version': '1.0.0',
    'description': '" Client json ==> server ==> modified json "',
    'long_description': None,
    'author': 'Vitlie',
    'author_email': 'dercaci200@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
