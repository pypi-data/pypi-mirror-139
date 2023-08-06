# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mailjet_utils']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.74.1,<0.75.0',
 'gunicorn>=20.1.0,<21.0.0',
 'httptools>=0.3.0,<0.4.0',
 'pydantic[email]>=1.9.0,<2.0.0',
 'uvicorn>=0.17.5,<0.18.0',
 'uvloop>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'mailjet-utils',
    'version': '0.2.0',
    'description': 'A package with models for working with mailjet.',
    'long_description': '\n# Mailjet utils\n',
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.github.com/peder2911/mailjet_utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
