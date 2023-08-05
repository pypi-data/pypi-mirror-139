# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['boto_collator_client']
setup_kwargs = {
    'name': 'boto-collator-client',
    'version': '0.2.0',
    'description': 'A boto3 client wrapper that collates each paginated API call into a single result',
    'long_description': None,
    'author': 'Iain Samuel McLean Elder',
    'author_email': 'iain@isme.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
